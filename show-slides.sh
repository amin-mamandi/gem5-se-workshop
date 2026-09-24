#!/usr/bin/env bash
# Build the slides and serve them in the browser.
set -euo pipefail
cd "$(dirname "$0")"

npm run build
echo "Open http://127.0.0.1:8000/dist/index.html"
python3 -m http.server 8000 --bind 127.0.0.1
