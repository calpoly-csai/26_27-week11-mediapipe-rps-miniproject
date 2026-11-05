# Guide: what the code does and why

The README tells you what to build. This guide explains the unfamiliar parts: the libraries, the model's output, and each step in detail. You can read it before the workshop or come back to it later.

## 1. How the program fits together

`main.py` runs the game loop. You never edit it. It calls *your* functions at fixed moments:

```
startup ─► load_recognizer()                       gestures.py   (once)

every frame (~30/s):
  webcam ─► frame ─► recognize(frame) ─► ("Closed_Fist", 0.94)    gestures.py
                                            │  main.py keeps the latest one
"Shoot!" (once per round)                   ▼
  gesture_to_move("Closed_Fist", 0.94) ─► "rock"                  gestures.py
  computer_move()                      ─► "paper"                 game.py
  decide_winner("rock", "paper")       ─► "computer"              game.py
  board.record("computer"), board.is_game_over(), board.champion()  game.py
```

| Function | Called | Gets | Returns |
|---|---|---|---|
| `load_recognizer(image_mode)` | once at startup | `True` if using `--images` | a recognizer object |
| `recognize(recognizer, frame, ts, image_mode)` | every frame | a BGR numpy image, a timestamp in ms | `(name, score)` or `None` |
| `gesture_to_move(name, score)` | at "Shoot!" | what `recognize` returned | `"rock"`/`"paper"`/`"scissors"` or `None` |
| `computer_move()` | at "Shoot!" | nothing | a random move |
| `decide_winner(player, computer)` | at "Shoot!" | two moves | `"player"`/`"computer"`/`"tie"` |
| `Scoreboard.record / is_game_over / champion` | after each round | the winner | updates and reports the score |

Unfinished functions still `raise NotImplementedError`. `main.py` catches that and shows `???` plus a TODO note, so the game runs at every stage of the workshop.

## 2. The libraries in 60 seconds

**OpenCV (`cv2`)** handles the camera and images.
- `cv2.VideoCapture(0)` opens the webcam, and `.read()` returns one frame. `main.py` does this for you.
- A frame is a **numpy array** of shape `(height, width, 3)`: one number from 0 to 255 per colour channel, per pixel.
- OpenCV orders the channels **B, G, R** (blue first), which is a historical quirk. Almost everything else, MediaPipe included, uses **R, G, B**. `cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)` swaps them.

**MediaPipe Tasks** provides Google's ready-made, pre-trained models that run locally (no internet). Every MediaPipe task follows the same 4-step pattern:

1. **Options:** describe what you want (`GestureRecognizerOptions`: which model file, which running mode).
2. **Create:** load the model (`GestureRecognizer.create_from_options(options)`). This is slow, so do it once.
3. **Run:** give it an `mp.Image` (`recognize_for_video(image, timestamp)` or `recognize(image)`).
4. **Read the result:** a plain Python object holding lists of answers.

**The model file** `models/gesture_recognizer.task` bundles three models that run in sequence:
- hand detector: where is the hand?
- landmark model: puts 21 points on the hand;
- gesture classifier: which gesture do those points form, and how sure is it?

**Running modes**
- `VIDEO`: a stream of frames. After the first frame, MediaPipe *tracks* the hand rather than searching the whole image each time, which is faster and less jittery. It needs a timestamp that always increases, so it knows how much time passed between frames.
- `IMAGE`: each picture is independent and there's no timestamp. Used by `--images`.
- (`LIVE_STREAM` also exists. It's asynchronous with callbacks, and this project doesn't use it.)

## 3. What the recognizer returns

`print(result)` gives something like this (values shortened):

```
GestureRecognizerResult(
  gestures=[[Category(index=-1, score=0.94, display_name='', category_name='Closed_Fist')]],
  handedness=[[Category(index=0, score=0.98, display_name='Right', category_name='Right')]],
  hand_landmarks=[[NormalizedLandmark(x=0.52, y=0.71, z=0.0, ...), ... 21 total]],
  hand_world_landmarks=[[Landmark(x=0.01, y=0.08, z=0.02, ...), ... 21 total]],
)
```

- Each field is a **list with one entry per hand**. With no hand in view, every list is empty (`gestures=[]`).
- `gestures[0]` holds the first hand's guesses, **best guess first**, so `gestures[0][0]` is the answer you want. Read `.category_name` (e.g. `'Closed_Fist'`) and `.score` (0.0 to 1.0).
- `hand_landmarks[0]` holds the 21 points. `x` and `y` are **normalized**: 0 to 1 across the image width and height, so `x * width` gives the pixel column. `z` is depth relative to the wrist.
- `hand_world_landmarks` holds the same points in metres. This project doesn't need them.

Landmark numbering (useful for the extensions):

```
0 wrist
thumb 1-4    index 5-8    middle 9-12    ring 13-16    pinky 17-20
(tips are 4, 8, 12, 16, 20)
```

## 4. Step by step

### Step 4: `load_recognizer()` and `recognize()` (gestures.py)
**Goal:** the terminal prints what the model sees, live.

**What to write:**
- `load_recognizer`: build the options (model path and running mode), then return `GestureRecognizer.create_from_options(options)`. Use `RunningMode.IMAGE` when `image_mode` is True, and `VIDEO` otherwise.
- `recognize`:
  1. convert BGR to RGB;
  2. wrap the array in `mp.Image`;
  3. run the right method for the mode;
  4. if `result.gestures` is empty, return `None`;
  5. otherwise take `result.gestures[0][0]`, print its name and score, and return `(name, score)`.

**How to test:** `python main.py`. The terminal should print lines like `Closed_Fist 0.94` as you move your hand, and `None` when you hide it. `--show-gesture` puts the same label on screen.

**Common mistakes:**
- `IndexError: list index out of range` means you indexed `gestures[0]` while no hand was visible. Check for an empty list first.
- `Input timestamp must be monotonically increasing` means you called `recognize_for_video` with a timestamp that didn't go up. Pass main.py's `timestamp_ms` as an `int`.
- `Task is not initialized with the image mode` (or `video mode`) means you used `recognize()` on a VIDEO recognizer, or the reverse. The method must match the mode.
- Gestures always come out `None` or weak: did you skip the BGR→RGB conversion?
- `???` still shows: you left the `raise NotImplementedError` line in.

### Step 5: `gesture_to_move()` (gestures.py)
**Goal:** your move shows on screen instead of `???`.

**What to write:**
1. If `score < CONFIDENCE_THRESHOLD`, return `None`.
2. Otherwise translate the name: `Closed_Fist` → rock, `Open_Palm` → paper, `Victory` → scissors, anything else → `None`. A dict with `.get(name)` covers the "anything else" case automatically.

**Why a threshold?** `score` is the model's confidence. A score of 0.4 usually means a half-formed or blurry gesture. Returning `None` makes main.py say "Unclear gesture, try again!" instead of playing a move you didn't mean.

**How to test:** press SPACE, show a fist at "Shoot!", and `You: rock` appears.

### Step 6: `computer_move()` and `decide_winner()` (game.py)
**Goal:** a full round works.
- `random.choice(MOVES)` picks a random list item.
- `decide_winner`: handle the tie first, then decide who wins. Plain if-statements work. A dict of "what beats what" (`{"rock": "scissors", ...}`) is shorter.

**How to test:** play a round; the screen says who won.

### Step 7: `Scoreboard` (game.py)
**Goal:** first to 3 wins the game.
- `record`: add 1 to `self.player` or `self.computer`. Ties add nothing.
- `is_game_over`: either counter is at least `WINS_NEEDED`.
- `champion`: return whoever reached `WINS_NEEDED`, or `None`.

**How to test:** play until someone reaches 3. "YOU WIN!" or "COMPUTER WINS" appears, and R restarts.

### Step 8: Edge cases and tuning
Try these with `--show-gesture` on: two hands, a hand half off-screen, a dark room, thumbs up, scissors held sideways.
- Weak scores on gestures you meant to make? Lower `CONFIDENCE_THRESHOLD`.
- Wrong moves being accepted? Raise it.

## 5. Glossary
- **Landmark:** one of 21 points the model places on the hand (a knuckle, a fingertip, the wrist).
- **Classification:** the model's answer to "which gesture is this?" (`category_name`).
- **Score / confidence:** how sure the model is, from 0.0 to 1.0.
- **Threshold:** the minimum score you accept as a real move.
- **Running mode:** VIDEO (a tracked stream) or IMAGE (independent pictures).
- **Timestamp:** milliseconds since start. VIDEO mode uses it to track the hand over time.
- **BGR / RGB:** colour channel order. OpenCV uses BGR, MediaPipe uses RGB.
- **Normalized coordinates:** positions from 0 to 1 instead of pixels, so they work at any image size.
