#!/usr/bin/env python3

import re
import json
import webbrowser

import openai
import spotipy
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

SEPARATOR = "-" * 100
_PLAYLIST_RE = re.compile(r"^\d+\.\s+(.+?)\s+[—–-]+\s+\*\*(.+?)\*\*", re.MULTILINE)


class SpotifyImporter:

    def __init__(self):
        self.sp = None
        self.current_user = None

    def login(self):
        self.sp = spotipy.Spotify(
            auth_manager=spotipy.SpotifyOAuth(
                client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:9999"),
                scope="playlist-modify-private,playlist-read-private",
            )
        )
        self.current_user = self.sp.current_user()
        assert self.current_user is not None

    @staticmethod
    def parse_playlist_text(text: str) -> list[dict]:
        tracks = []
        for match in _PLAYLIST_RE.finditer(text):
            tracks.append({"artist": match.group(1).strip(), "song": match.group(2).strip()})
        return tracks

    def pick_best_match(self, artist: str, song: str, candidates: list) -> dict | None:
        if not candidates:
            return None

        lines = []
        for i, c in enumerate(candidates):
            c_artist = c["artists"][0]["name"] if c.get("artists") else "?"
            c_name = c.get("name", "?")
            c_album = c.get("album", {}).get("name", "?")
            lines.append(f"{i}. {c_name} — {c_artist} ({c_album})")

        candidates_text = "\n".join(lines)
        prompt = (
            f"I'm looking for the song: {artist} — {song}\n\n"
            f"Here are Spotify search results:\n{candidates_text}\n\n"
            f'Which result is the correct match? Reply ONLY with JSON: {{"match": <index>}} or {{"match": null}} if none fit.'
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=20,
            )
            raw = response["choices"][0]["message"]["content"].strip()
            data = json.loads(raw)
            idx = data.get("match")
            if idx is None:
                return None
            return candidates[int(idx)]
        except Exception as e:
            print(f"  [!] OpenAI error, using first result: {e}")
            return candidates[0]

    def import_tracks(self, tracks: list[dict], playlist_id: str) -> tuple[list, list]:
        found = []
        not_found = []

        for t in tracks:
            artist = t["artist"]
            song = t["song"]
            query = f"{artist} {song}"

            results = self.sp.search(q=query, type="track", limit=5)
            items = results["tracks"]["items"]

            if not items:
                print(f"  [✗] {artist} — {song}")
                not_found.append(t)
                continue

            match = self.pick_best_match(artist, song, items)
            if match is None:
                print(f"  [✗] {artist} — {song}")
                not_found.append(t)
                continue

            self.sp.user_playlist_add_tracks(self.current_user["id"], playlist_id, [match["id"]])
            matched_artist = match["artists"][0]["name"] if match.get("artists") else artist
            matched_name = match.get("name", song)
            print(f"  [✓] {artist} — {song}  →  {matched_artist} — {matched_name}")
            found.append({"requested": t, "matched": match})

        return found, not_found

    def create_playlist(self, name: str) -> str:
        all_playlists = self.sp.user_playlists(self.current_user["id"])
        existing_names = {p["name"].lower() for p in all_playlists["items"]}

        playlist_name = name
        suffix = 2
        while playlist_name.lower() in existing_names:
            playlist_name = f"{name} {suffix}"
            suffix += 1

        playlist = self.sp.user_playlist_create(
            self.current_user["id"], name=playlist_name, public=False
        )
        webbrowser.open(playlist["uri"])
        return playlist["id"]

    def get_existing_playlist(self) -> str:
        all_playlists = self.sp.user_playlists(self.current_user["id"])
        items = all_playlists["items"]

        print(SEPARATOR)
        for i, p in enumerate(items, start=1):
            print(f"  {i}. {p['name']}")
        print(SEPARATOR)

        while True:
            choice = input("Select playlist number: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(items):
                return items[int(choice) - 1]["id"]
            print(f"Please enter a number between 1 and {len(items)}.")
