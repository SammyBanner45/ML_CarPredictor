#!/bin/bash
# Run the Car Price Predictor using the project's virtual environment.
# Usage: ./run.sh
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
"$SCRIPT_DIR/venv/bin/python3" "$SCRIPT_DIR/app.py"
