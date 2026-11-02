#!/usr/bin/env bash
# One-command setup (macOS/Linux). Clones the repo, installs uv + Python 3.12 + packages, runs the checker.
#   curl -fsSL https://raw.githubusercontent.com/YOUR_GITHUB_USER/rps-mediapipe/main/setup.sh | bash
# Also works from inside an existing clone:  ./setup.sh
set -euo pipefail

REPO_URL="https://github.com/YOUR_GITHUB_USER/rps-mediapipe.git"
DIR="rps-mediapipe"

# Inside a clone already? (requirements.txt next to this script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"
if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/requirements.txt" ]; then
  cd "$SCRIPT_DIR"
else
  command -v git >/dev/null 2>&1 || { echo "git is required: https://git-scm.com/downloads"; exit 1; }
  [ -d "$DIR" ] || git clone "$REPO_URL" "$DIR"
  cd "$DIR"
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi

uv venv --python 3.12 --allow-existing .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python check_setup.py || true

echo
echo "Done. cd $(basename "$PWD") and run:  .venv/bin/python main.py"
