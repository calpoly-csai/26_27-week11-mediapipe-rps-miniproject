# Rock Paper Scissors with MediaPipe

Play rock paper scissors against your computer using your real hand. A pre-trained Google
model (MediaPipe Gesture Recognizer) runs locally on your webcam. You write the code that
connects the model to the game.

## 1. Install
**Fastest — one command** (installs git-free if needed, uv, Python 3.12 and the packages, then runs the checker):

macOS / Linux (Terminal):
```
curl -fsSL https://raw.githubusercontent.com/calpoly-csai/week11-mediapipe-rps-miniproject/main/setup.sh | bash
```
Windows (PowerShell):
```
irm https://raw.githubusercontent.com/calpoly-csai/week11-mediapipe-rps-miniproject/main/setup.ps1 | iex
```
Then `cd week11-mediapipe-rps-miniproject` and skip to step 2. Run the game with `.venv/bin/python main.py` (macOS/Linux) or
`.venv\Scripts\python.exe main.py` (Windows).

Manual steps:
1. **Python 3.12** (3.10–3.13 work; newer may not have MediaPipe wheels yet).
   - Windows: <https://www.python.org/downloads/release/python-3128/> — **tick "Add Python to PATH"** in the installer.
   - macOS/Linux: usually preinstalled; check `python3 --version`.
2. **Git**: <https://git-scm.com/downloads> (Windows).
3. Clone and set up:
   ```
   git clone https://github.com/calpoly-csai/week11-mediapipe-rps-miniproject.git && cd week11-mediapipe-rps-miniproject
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

**No webcam (or camera won't open)?** Play with the 8 included hand photos instead:
`python main.py --images sample_images`. Each SPACE shows the next photo, and the model
reads the hand in it just like a webcam frame. Try `python main.py --solution --images sample_images`
to see it working. Add your own `.jpg`/`.png` hand photos to that folder too.

## 3. How a gesture recognizer works
1. Find the hand in the image. 2. Place 21 landmarks (knuckles, fingertips). 3. A classifier
decides which gesture those points form, with a confidence score (`Victory`, 0.92).
Google already **trained** this model; we only **use** it. It runs offline on your laptop.
Built-in gestures: `Closed_Fist, Open_Palm, Pointing_Up, Thumb_Down, Thumb_Up, Victory, ILoveYou, None`.

## 4. Your steps
Each step ends with something changing on screen. **New to OpenCV / MediaPipe? Read
[GUIDE.md](GUIDE.md):** it explains what every library call does, what the model returns,
and walks through each step with tests and common mistakes. Official docs:
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
- No webcam: `python main.py --images sample_images` (8 hand photos included; see section 2), or pair up.

## 6. Extensions
- **Level 2:** sounds, animations, best-of-5, win streaks, draw the 21 landmarks.
- **Level 3:** two-player mode; a cheating computer that reads your hand before "Shoot!"; Lizard-Spock with a custom model (MediaPipe Model Maker).
- **Level 4:** an opponent that learns your patterns, a leaderboard, a browser version with MediaPipe JS.
