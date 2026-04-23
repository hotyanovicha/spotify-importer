#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# Auto-setup if venv or .env is missing
if [ ! -d ".venv" ] || [ ! -f ".env" ]; then
    bash "$DIR/setup.sh"
fi

.venv/bin/python main.py
