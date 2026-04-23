# Spotify Importer

Simple tool to import a text playlist into Spotify using AI.

## Before You Start

- Python 3.10+
- Spotify Developer app
- Gemini API key

## Step 1. Install Dependencies

```bash
bash setup.sh
```

This script will:
- check Python version
- create `.venv`
- install dependencies
- create `.env` if missing
- ask for your keys

## Step 2. Set Redirect URI in Spotify

In your Spotify app settings, add this Redirect URI:

`http://127.0.0.1:9999`

Important: it must exactly match `SPOTIFY_REDIRECT_URI` in `.env`.

## Step 3. Run the App

```bash
bash run.sh
```

The app opens at `http://localhost:8501`.

## Step 4. Import Your Playlist

1. Paste your track list
2. Choose: create a new playlist or add to an existing one
3. If using existing playlist, paste its Spotify URL or playlist ID
4. Click `Import to Spotify`

## Troubleshooting

1. Check Python version:

```bash
python3 --version
```

It must be `3.10+`.

2. If your virtual environment was created with an older Python, recreate it:

```bash
rm -rf .venv
bash setup.sh
```
