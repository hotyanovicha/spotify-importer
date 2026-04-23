#!/bin/bash

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "----------------------------------------------------------------------------------------------------"
echo "                              SPOTIFY IMPORTER — SETUP"
echo "----------------------------------------------------------------------------------------------------"

if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 is not installed."
    echo "Install Python 3.10+ and run setup again."
    exit 1
fi

if ! python3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"; then
    echo "Error: Python 3.10+ is required."
    echo "Current version: $(python3 --version 2>&1)"
    exit 1
fi

# Create virtual environment if needed
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

if ! .venv/bin/python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"; then
    echo "Error: .venv was created with Python older than 3.10."
    echo "Remove .venv and run setup again with Python 3.10+."
    exit 1
fi

echo "Installing dependencies..."
.venv/bin/pip install -q --upgrade pip
.venv/bin/pip install -q -r requirements.txt
echo "Dependencies installed."

# Create .env from example if missing
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ""
    echo "Created .env — fill in your API keys:"
    echo ""

    read -p "  Spotify Client ID:     " spotify_id
    read -p "  Spotify Client Secret: " spotify_secret
    read -p "  Gemini API Key:        " gemini_key

    sed -i '' "s/your_spotify_client_id/$spotify_id/" .env
    sed -i '' "s/your_spotify_client_secret/$spotify_secret/" .env
    sed -i '' "s/your_gemini_api_key/$gemini_key/" .env

    echo ""
    echo ".env configured."
else
    echo ".env already exists, skipping key setup."
fi

echo ""
echo "Setup complete. Run the importer with:"
echo "  ./run.sh"
echo "----------------------------------------------------------------------------------------------------"
