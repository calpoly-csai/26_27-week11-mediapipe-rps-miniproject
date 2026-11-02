# Rock Paper Scissors with MediaPipe

Play rock paper scissors against your computer using your real hand. A pre-trained Google
model (MediaPipe Gesture Recognizer) runs locally on your webcam. You write the code that
connects the model to the game.

## 1. Install
**Fastest (macOS/Linux):** `git clone <repo-url> && cd rps-mediapipe && ./setup.sh` — installs uv, Python 3.12 and the packages, then runs the checker. Then skip to step 2 (use `.venv/bin/python main.py`).

Manual steps:
1. **Python 3.12** (3.10–3.13 work; newer may not have MediaPipe wheels yet).
   - Windows: <https://www.python.org/downloads/release/python-3128/> — **tick "Add Python to PATH"** in the installer.
   - macOS/Linux: usually preinstalled; check `python3 --version`.
2. **Git**: <https://git-scm.com/downloads> (Windows).
3. Clone and set up:
   ```
   git clone <repo-url> && cd rps-mediapipe
   python -m venv .venv
   .venv\Scripts\activate          # Windows
   source .venv/bin/activate       # macOS / Linux
   pip install -r requirements.txt
   python check_setup.py
   ```
   **Win:** every line says OK and your webcam light turns on.

**macOS camera permission:** the first run asks for camera access for your terminal / VS Code.
If you denied it: System Settings → Privacy & Security → Camera → enable it, then restart the app.

## 2. Run the starter
`python main.py` — press SPACE to start. The countdown works; at "Shoot!" you see `???`
and a "TODO" note. Q quits, R restarts. See the finished game: `python main.py --solution`.

## 3. How a gesture recognizer works
1. Find the hand in the image. 2. Place 21 landmarks (knuckles, fingertips). 3. A classifier
decides which gesture those points form, with a confidence score (`Victory`, 0.92).
Google already **trained** this model; we only **use** it. It runs offline on your laptop.
Built-in gestures: `Closed_Fist, Open_Palm, Pointing_Up, Thumb_Down, Thumb_Up, Victory, ILoveYou, None`.

## 4. Your steps
Each step ends with something changing on screen. Docs:
<https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer/python>

| Step | File | What to do | Win |
|---|---|---|---|
| 4 | `gestures.py` | `load_recognizer()` and `recognize()`: load the model, run it on the frame, return `(name, score)`, and print it | Terminal prints `Closed_Fist 0.94` as you move your hand |
| 5 | `gestures.py` | `gesture_to_move()`: Closed_Fist→rock, Open_Palm→paper, Victory→scissors, else `None` (also if score < `CONFIDENCE_THRESHOLD`) | Your move shows instead of `???` |
| 6 | `game.py` | `computer_move()` and `decide_winner()` | A real round works |
| 7 | `game.py` | `Scoreboard.record / is_game_over / champion` (first to 3) | Full game |
| 8 | both | Test edge cases (two hands, frame edge, bad light, thumbs up); tune the threshold | Showdown! |

Tip: run `python main.py --show-gesture` to see the live label on screen.
Stuck? Compare with `solution/`.

## 5. Troubleshooting
- `pip` / `python` not found (Windows): reinstall Python with "Add to PATH" ticked, or try `py`.
- Black window / camera error: see macOS permission above; close Zoom/Teams; try `--camera 1`.
- Hand not detected: face a light source, plain background, hand fully in frame.
- No webcam: pair up, or add photos to `sample_images/` and run `python main.py --images sample_images`.

## 6. Extensions
- **Level 2:** sounds, animations, best-of-5, win streaks, draw the 21 landmarks.
- **Level 3:** two-player mode; a cheating computer that reads your hand before "Shoot!"; Lizard-Spock with a custom model (MediaPipe Model Maker).
- **Level 4:** an opponent that learns your patterns, a leaderboard, a browser version with MediaPipe JS.
