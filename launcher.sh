#!/bin/bash
# cli-translation-overlay — launcher wrapper
# Finds the project directory and starts the overlay.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="${SCRIPT_DIR}"

# If installed system-wide, icons are here
export ICON_PATH="${PROJECT_DIR}/icons/cli-translation-overlay.png"

cd "${PROJECT_DIR}" || exit 1
exec python3 overlay.py "$@"
