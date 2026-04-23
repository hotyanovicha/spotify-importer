# Spotify Importer

Import a playlist from plain text into Spotify using Google Gemini for track matching.

## Requirements

- Python 3.10 or newer

## Setup

### 1. Install dependencies

```bash
bash setup.sh
```

Or manually:

```bash
python3 -m venv .venv  # python3 must be 3.10+
.venv/bin/pip install -r requirements.txt
```

### 2. Configure environment variables

Copy `.env` and fill in your credentials:

```bash
cp .env .env.local  # or edit .env directly
```

| Variable | Where to get it |
|---|---|
| `SPOTIFY_CLIENT_ID` | [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) — create an app, copy **Client ID** |
| `SPOTIFY_CLIENT_SECRET` | Same app page — copy **Client Secret** |
| `SPOTIFY_REDIRECT_URI` | Set to `http://localhost:9999` in the app's **Redirect URIs** settings |
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/app/apikey) — create an API key |
| `GEMINI_MODEL` | Model name, e.g. `gemini-2.0-flash` (default) |

#### Spotify app setup

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and log in.
2. Click **Create app**.
3. Fill in a name and description, then add `http://localhost:9999` to **Redirect URIs**.
4. Copy **Client ID** and **Client Secret** into `.env`.

#### Gemini API key

1. Open [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Click **Create API key**.
3. Copy the key into `.env`.

## Run

```bash
bash run.sh
```

Opens the app at [http://localhost:8501](http://localhost:8501).
