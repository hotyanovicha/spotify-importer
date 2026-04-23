#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 is not installed."
    echo "Install Python 3.10+ and run again."
    exit 1
fi

if ! python3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"; then
    echo "Error: Python 3.10+ is required."
    echo "Current version: $(python3 --version 2>&1)"
    exit 1
fi

# Auto-setup if venv or .env is missing
if [ ! -d ".venv" ] || [ ! -f ".env" ]; then
    bash "$DIR/setup.sh"
fi

if ! .venv/bin/python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"; then
    echo "Error: .venv uses Python older than 3.10."
    echo "Delete .venv and run setup again."
    exit 1
fi

echo "Opening Spotify Importer at http://localhost:8501"
.venv/bin/streamlit run app.py --server.headless false
