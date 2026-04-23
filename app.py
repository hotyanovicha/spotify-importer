#!/usr/bin/env python3

import streamlit as st
from importer import SpotifyImporter

st.set_page_config(page_title="Spotify Playlist Importer", page_icon="🎵", layout="centered")

st.title("🎵 Spotify Playlist Importer")
st.caption("Вставь список треков — программа найдёт их в Spotify через Gemini AI.")

# ── Playlist text input ───────────────────────────────────────────────────────

playlist_text = st.text_area(
    "Плейлист:",
    height=300,
    placeholder=(
        "1. MellSher — **X**\n"
        "2. Kai Angel — **Limousine Music**\n"
        "3. GUF, Баста — **Баста / Гуф**\n"
        "..."
    ),
)

tracks = []
if playlist_text.strip():
    tracks = SpotifyImporter.parse_playlist_text(playlist_text)
    if tracks:
        with st.expander(f"Найдено треков: {len(tracks)}"):
            for i, t in enumerate(tracks, 1):
                st.write(f"{i}. {t['artist']} — {t['song']}")
    else:
        st.warning("Треки не распознаны. Ожидаемый формат: `1. Артист — **Название**`")

# ── Mode selection ────────────────────────────────────────────────────────────

st.divider()
mode = st.radio(
    "Действие:",
    ["Создать новый плейлист", "Добавить в существующий"],
    horizontal=True,
)

playlist_name = ""
if mode == "Создать новый плейлист":
    playlist_name = st.text_input("Название нового плейлиста:", value="Imported Playlist")

# ── Load existing playlists ───────────────────────────────────────────────────

selected_playlist_id = None

if mode == "Добавить в существующий":
    if st.button("Загрузить мои плейлисты из Spotify"):
        with st.spinner("Подключаюсь к Spotify…"):
            try:
                importer = SpotifyImporter()
                importer.login()
                playlists = importer.sp.user_playlists(importer.current_user["id"])["items"]
                st.session_state["playlists"] = {p["name"]: p["id"] for p in playlists}
                st.session_state["importer"] = importer
            except Exception as e:
                st.error(f"Ошибка подключения: {e}")

    if "playlists" in st.session_state:
        playlist_names = list(st.session_state["playlists"].keys())
        chosen = st.selectbox("Выбери плейлист:", playlist_names)
        selected_playlist_id = st.session_state["playlists"][chosen]

# ── Import button ─────────────────────────────────────────────────────────────

st.divider()

ready = bool(tracks) and (
    (mode == "Создать новый плейлист" and playlist_name.strip())
    or (mode == "Добавить в существующий" and selected_playlist_id)
)

if st.button("🚀 Импортировать в Spotify", type="primary", disabled=not ready):
    try:
        # Reuse already-authenticated importer or create a new one
        if "importer" in st.session_state:
            importer = st.session_state["importer"]
        else:
            importer = SpotifyImporter()
            with st.spinner("Подключаюсь к Spotify… (первый раз откроется браузер для авторизации)"):
                importer.login()

        # Create or get playlist
        if mode == "Создать новый плейлист":
            with st.spinner("Создаю плейлист…"):
                playlist_id = importer.create_playlist(playlist_name.strip())
            st.success(f"Плейлист «{playlist_name}» создан и открыт в браузере.")
        else:
            playlist_id = selected_playlist_id

        # Import with live progress
        found = []
        not_found = []

        with st.status("Ищу треки…", expanded=True) as status:
            for t in tracks:
                artist, song = t["artist"], t["song"]
                results = importer.sp.search(q=f"{artist} {song}", type="track", limit=5)
                items = results["tracks"]["items"]

                if not items:
                    st.write(f"✗ {artist} — {song}")
                    not_found.append(t)
                    continue

                match = importer.pick_best_match(artist, song, items)
                if match is None:
                    st.write(f"✗ {artist} — {song}")
                    not_found.append(t)
                    continue

                importer.sp.user_playlist_add_tracks(
                    importer.current_user["id"], playlist_id, [match["id"]]
                )
                matched_artist = match["artists"][0]["name"] if match.get("artists") else artist
                matched_name = match.get("name", song)
                st.write(f"✓ **{artist} — {song}** → {matched_artist} — {matched_name}")
                found.append(t)

            label = f"Готово: добавлено {len(found)} из {len(tracks)}"
            status.update(label=label, state="complete")

        # Summary
        if not_found:
            st.warning(f"Не найдено ({len(not_found)}):")
            for t in not_found:
                st.write(f"- {t['artist']} — {t['song']}")

    except Exception as e:
        st.error(f"Ошибка: {e}")
