# Spotify Importer

Simple tool to import a text playlist into Spotify using AI.

## Before You Start

- Python 3.10+
- Spotify Developer app
- Gemini API key

Quick links:
- Spotify Developer Dashboard: [https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
- Gemini API key: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

## Quick Start (install -> get keys -> fill env -> run)

1. Install dependencies and create `.env`:

```bash
bash setup.sh
```

2. Go to Spotify Dashboard, create an app, copy:
- `Client ID` -> `SPOTIFY_CLIENT_ID`
- `Client Secret` -> `SPOTIFY_CLIENT_SECRET`

3. In Spotify app settings, add Redirect URI:
- `http://127.0.0.1:9999`
- It must exactly match `SPOTIFY_REDIRECT_URI` in `.env`

4. Go to Gemini API page, create API key, copy:
- API key -> `GEMINI_API_KEY`

5. Run the app:

```bash
bash run.sh
```

The app opens at `http://localhost:8501`.

## Separate Block: How to Create `.env`

`setup.sh` creates `.env` from `.env.example` automatically.

### Option A: Automatic (recommended)

```bash
bash setup.sh
```

The script asks for:
- Spotify Client ID
- Spotify Client Secret
- Gemini API Key

### Option B: Manual

```bash
cp .env.example .env
```

Then open `.env` and fill values:
- `SPOTIFY_CLIENT_ID`: Spotify Dashboard -> your app -> `Client ID`
- `SPOTIFY_CLIENT_SECRET`: Spotify Dashboard -> your app -> `View client secret`
- `SPOTIFY_REDIRECT_URI`: `http://127.0.0.1:9999` (and add same URI in Spotify app settings)
- `GEMINI_API_KEY`: Google AI Studio API key page
- `GEMINI_MODEL`: keep default `gemini-2.5-flash-lite`

Example `.env`:

```env
SPOTIFY_CLIENT_ID=your_real_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_real_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:9999
GEMINI_API_KEY=your_real_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash-lite
```

## What `setup.sh` Does

- checks Python version
- creates `.venv`
- installs dependencies
- creates `.env` if missing
- asks for your keys

## Import Your Playlist

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
