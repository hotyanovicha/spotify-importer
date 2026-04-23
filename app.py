#!/usr/bin/env python3

import re

import streamlit as st

from importer import SpotifyImporter


def extract_playlist_id(value: str) -> str | None:
    text = value.strip()
    if not text:
        return None

    if text.startswith("spotify:playlist:"):
        parts = text.split(":")
        return parts[-1] if parts[-1] else None

    match = re.search(r"open\.spotify\.com/playlist/([A-Za-z0-9]+)", text)
    if match:
        return match.group(1)

    if re.fullmatch(r"[A-Za-z0-9]+", text):
        return text

    return None


st.set_page_config(page_title="Spotify Playlist Importer", layout="centered")

st.title("Spotify Playlist Importer")
st.write("Paste tracks line-by-line, choose destination, and import.")

playlist_text = st.text_area(
    "Track list",
    height=260,
    placeholder=(
        "Miles Davis - So What\n"
        "John Coltrane - Giant Steps\n"
        "Dave Brubeck - Take Five\n"
        "Herbie Hancock - Cantaloupe Island"
    ),
)

mode = st.radio(
    "Destination",
    ["Create a new playlist", "Add to an existing playlist"],
    horizontal=True,
)

playlist_name = ""
existing_playlist_input = ""

if mode == "Create a new playlist":
    playlist_name = st.text_input("New playlist name", value="Jazz Imports")
else:
    existing_playlist_input = st.text_input(
        "Existing playlist URL or ID",
        placeholder="https://open.spotify.com/playlist/<id>",
    )

existing_playlist_id = extract_playlist_id(existing_playlist_input)
ready = bool(playlist_text.strip()) and (
    (mode == "Create a new playlist" and bool(playlist_name.strip()))
    or (mode == "Add to an existing playlist" and bool(existing_playlist_id))
)

if st.button("Import to Spotify", type="primary", disabled=not ready):
    try:
        importer = SpotifyImporter()

        with st.spinner("Parsing tracks with AI..."):
            tracks = importer.parse_with_ai(playlist_text)

        if not tracks:
            st.error("No tracks were parsed. Try cleaner input, one track per line.")
            st.stop()

        st.info(f"Parsed {len(tracks)} track(s).")

        with st.spinner("Connecting to Spotify..."):
            importer.login()

        if mode == "Create a new playlist":
            with st.spinner("Creating playlist..."):
                playlist_id = importer.create_playlist(playlist_name.strip())
            st.success(f"Playlist created: {playlist_name.strip()}")
        else:
            playlist_id = existing_playlist_id
            st.success("Using existing playlist.")

        found = []
        not_found = []
        progress = st.progress(0)

        for index, track in enumerate(tracks, start=1):
            artist, song = track["artist"], track["song"]
            results = importer.sp.search(q=f"{artist} {song}", type="track", limit=5)
            items = results["tracks"]["items"]

            if not items:
                st.write(f"[NOT FOUND] {artist} - {song}")
                not_found.append(track)
                progress.progress(index / len(tracks))
                continue

            best_match = importer.pick_best_match(artist, song, items)
            if best_match is None:
                st.write(f"[NOT FOUND] {artist} - {song}")
                not_found.append(track)
                progress.progress(index / len(tracks))
                continue

            importer.sp.playlist_add_items(playlist_id, [best_match["id"]])
            matched_artist = best_match["artists"][0]["name"] if best_match.get("artists") else artist
            matched_name = best_match.get("name", song)
            st.write(f"[ADDED] {artist} - {song} -> {matched_artist} - {matched_name}")
            found.append(track)
            progress.progress(index / len(tracks))

        st.success(f"Done. Added {len(found)}/{len(tracks)} tracks.")

        if not_found:
            st.warning(f"Not found: {len(not_found)}")
            for track in not_found:
                st.write(f"- {track['artist']} - {track['song']}")

    except Exception as exc:
        st.error(f"Error: {exc}")
