#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# Auto-setup if venv or .env is missing
if [ ! -d ".venv" ] || [ ! -f ".env" ]; then
    bash "$DIR/setup.sh"
fi

echo "Opening Spotify Importer at http://localhost:8501"
.venv/bin/streamlit run app.py --server.headless false
