#!/bin/bash

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "----------------------------------------------------------------------------------------------------"
echo "                              SPOTIFY IMPORTER — SETUP"
echo "----------------------------------------------------------------------------------------------------"

# Create virtual environment if needed
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
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
