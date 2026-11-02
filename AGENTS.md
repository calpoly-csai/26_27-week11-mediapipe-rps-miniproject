# Build / verify
- Python 3.12 venv: `python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt`
- Setup check: `.venv/bin/python check_setup.py` (webcam check needs macOS camera permission)
- Starter: `.venv/bin/python main.py`; finished game: `.venv/bin/python main.py --solution`
- No camera: `main.py --images DIR`. Headless test: `--max-seconds N`.
- `main.py` and `check_setup.py` are never edited by attendees; `solution/` is the answer key.
