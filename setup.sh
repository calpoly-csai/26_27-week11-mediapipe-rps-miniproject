#!/usr/bin/env bash
# One-command setup: ./setup.sh   (installs uv if needed, Python 3.12, packages, runs the checker)
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi

uv venv --python 3.12 --allow-existing .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python check_setup.py || true

echo
echo "Done. Run the game with:  .venv/bin/python main.py"
