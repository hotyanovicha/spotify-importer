#!/usr/bin/env python3

from importer import SpotifyImporter, SEPARATOR


def read_multiline_input(prompt: str) -> str:
    print(prompt)
    print("(Paste text, then press Enter twice to finish)")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        lines.append(line)
        if len(lines) >= 2 and lines[-1] == "" and lines[-2] == "":
            break
    return "\n".join(lines)


def main():
    print(SEPARATOR)
    print(" SPOTIFY PLAYLIST IMPORTER ".center(100, "-"))
    print(SEPARATOR)

    text = read_multiline_input("Paste your playlist:")
    importer = SpotifyImporter()
    tracks = importer.parse_playlist_text(text)

    if not tracks:
        print("No tracks found in the pasted text. Make sure the format is:")
        print("  1. Artist — **Song Title**")
        return

    print(SEPARATOR)
    print(f"Parsed {len(tracks)} tracks:")
    for i, t in enumerate(tracks, start=1):
        print(f"  {i}. {t['artist']} — {t['song']}")

    print(SEPARATOR)
    print("[1] Create new playlist")
    print("[2] Add to existing playlist")
    while True:
        match input("Your choice: ").strip():
            case "1":
                playlist_name = input("Playlist name: ").strip() or "Imported Playlist"
                mode = "new"
                break
            case "2":
                mode = "existing"
                break
            case _:
                print("Please enter 1 or 2.")

    print("Connecting to Spotify...")
    importer.login()

    if mode == "new":
        playlist_id = importer.create_playlist(playlist_name)
        print(f"Playlist created and opened in browser.")
    else:
        playlist_id = importer.get_existing_playlist()

    print(SEPARATOR)
    print("Searching and importing tracks...")
    print(SEPARATOR)
    found, not_found = importer.import_tracks(tracks, playlist_id)

    print(SEPARATOR)
    print(f"Done! Added {len(found)}/{len(tracks)} tracks.")
    if not_found:
        print(f"\nNot found ({len(not_found)}):")
        for t in not_found:
            print(f"  - {t['artist']} — {t['song']}")
    print(SEPARATOR)


if __name__ == "__main__":
    main()
