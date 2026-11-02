"""Rock Paper Scissors with your hand. Run: python main.py

You don't edit this file. Edit gestures.py and game.py.
Options:  --camera N   --images DIR   --show-gesture   --solution
"""
import argparse
import sys
import time
from pathlib import Path

import cv2

parser = argparse.ArgumentParser()
parser.add_argument("--camera", type=int, default=0, help="camera index")
parser.add_argument("--images", metavar="DIR", help="use photos from DIR instead of the webcam")
parser.add_argument("--show-gesture", action="store_true", help="show live gesture label")
parser.add_argument("--solution", action="store_true", help="use the finished code in solution/")
parser.add_argument("--max-seconds", type=float, default=0, help=argparse.SUPPRESS)  # for tests
args = parser.parse_args()

if args.solution:
    from solution import game, gestures
else:
    import game
    import gestures

WINDOW = "Rock Paper Scissors"
FONT = cv2.FONT_HERSHEY_SIMPLEX
PHASES = ["Rock...", "Paper...", "Scissors...", "Shoot!"]
PHASE_SECS = 0.7
SAMPLE_DELAY = 0.3   # seconds after "Shoot!" appears when we read your hand
RESULT_SECS = 2.5

WAITING, COUNTDOWN, RESULT, GAME_OVER = "waiting", "countdown", "result", "game_over"


def text(img, s, y, scale=1.0, color=(255, 255, 255), x=None):
    """Draw text horizontally centered (or at x) with a dark outline."""
    (w, _), _ = cv2.getTextSize(s, FONT, scale, 2)
    px = (img.shape[1] - w) // 2 if x is None else x
    cv2.putText(img, s, (px, y), FONT, scale, (0, 0, 0), 5, cv2.LINE_AA)
    cv2.putText(img, s, (px, y), FONT, scale, color, 2, cv2.LINE_AA)


HAND_CONNECTIONS = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8),
                    (5, 9), (9, 10), (10, 11), (11, 12), (9, 13), (13, 14), (14, 15), (15, 16),
                    (13, 17), (17, 18), (18, 19), (19, 20), (0, 17)]


def draw_landmarks(img, pts):
    """Draw the 21 hand landmarks (normalized x, y) and the bones between them."""
    h, w = img.shape[:2]
    px = [(int(x * w), int(y * h)) for x, y in pts]
    for a, b in HAND_CONNECTIONS:
        cv2.line(img, px[a], px[b], (255, 255, 255), 2, cv2.LINE_AA)
    for p in px:
        cv2.circle(img, p, 5, (0, 200, 0), -1, cv2.LINE_AA)


def attempt(todos, name, fn, *a, **kw):
    """Call fn; if it's still a TODO, remember the file name and return None."""
    try:
        return fn(*a, **kw), True
    except NotImplementedError:
        todos.add(name)
        return None, False


class Source:
    """Webcam, or a folder of photos."""

    def __init__(self):
        self.images = None
        if args.images:
            folder = Path(args.images)
            exts = {".jpg", ".jpeg", ".png"}
            files = sorted(p for p in folder.glob("*") if p.suffix.lower() in exts)
            if not files:
                sys.exit(f"No .jpg/.png images found in {folder}")
            self.images = [cv2.imread(str(p)) for p in files]
            self.images = [cv2.resize(i, (960, 720)) for i in self.images if i is not None]
            self.i = -1
            self.next_image()
        else:
            self.cap = cv2.VideoCapture(args.camera)
            if not self.cap.isOpened():
                sys.exit("Could not open the webcam. Run check_setup.py for help "
                         "(on macOS, allow camera access for your terminal/VS Code).")

    def next_image(self):
        self.i = (self.i + 1) % len(self.images)
        self.current = self.images[self.i]

    def read(self):
        if self.images:
            return self.current.copy()
        ok, frame = self.cap.read()
        if not ok:
            return None
        return cv2.flip(frame, 1)  # mirror so it feels natural

    def release(self):
        if not self.images:
            self.cap.release()


def main():
    source = Source()
    image_mode = bool(args.images)
    todos = set()

    recognizer, ok = attempt(todos, "gestures.py", gestures.load_recognizer, image_mode=image_mode)
    if not ok:
        recognizer = None

    board = game.Scoreboard()
    state, state_t = WAITING, time.time()
    start = time.time()
    last_ts = -1
    last_rec = None          # latest (name, score) or None
    sampled = False
    p_move = c_move = winner = None
    msg = ""
    champion = None

    while True:
        frame = source.read()
        if frame is None:
            print("Lost the camera.")
            break
        now = time.time()
        if args.max_seconds and now - start > args.max_seconds:
            break

        # --- gesture recognition on every frame ---
        if recognizer is not None:
            ts = max(last_ts + 1, int((now - start) * 1000))
            last_ts = ts
            res, ok = attempt(todos, "gestures.py", gestures.recognize, recognizer, frame, ts,
                              image_mode=image_mode)
            if ok:
                last_rec = res
            else:
                recognizer = None  # stop retrying a stub every frame

        # --- state machine ---
        elapsed = now - state_t
        if state == COUNTDOWN:
            idx = min(int(elapsed / PHASE_SECS), len(PHASES) - 1)
            if idx == 3 and elapsed - 3 * PHASE_SECS >= SAMPLE_DELAY and not sampled:
                sampled = True
                p_move, c_move, winner, msg, champion = play_round(board, last_rec, todos)
                state, state_t = RESULT, now
        elif state == RESULT and elapsed > RESULT_SECS:
            if champion is not None or (not todos and board.is_game_over()):
                state = GAME_OVER
            else:
                state = WAITING
            state_t = now

        # --- drawing ---
        h, w = frame.shape[:2]
        pts = getattr(gestures, "last_landmarks", None)  # set by the solution's recognize()
        if pts and recognizer is not None:
            draw_landmarks(frame, pts)
        if state == WAITING:
            text(frame, "Press SPACE to play", h // 2, 1.3)
        elif state == COUNTDOWN:
            text(frame, PHASES[min(int(elapsed / PHASE_SECS), 3)], h // 2, 2.2, (0, 255, 255))
        elif state in (RESULT, GAME_OVER):
            draw_result(frame, p_move, c_move, winner, msg)
            if state == GAME_OVER:
                who = "YOU WIN!" if champion == "player" else "COMPUTER WINS"
                text(frame, who, h // 2 + 80, 1.8, (0, 255, 0) if champion == "player" else (0, 0, 255))
                text(frame, "R = play again   Q = quit", h // 2 + 130, 0.8)

        text(frame, f"You {board.player}  -  {board.computer} Computer", 40, 0.9, x=20)
        text(frame, f"First to {game.WINS_NEEDED}", 70, 0.6, x=20)
        if args.show_gesture:
            label = f"{last_rec[0]} {last_rec[1]:.2f}" if last_rec else "no hand"
            text(frame, label, h - 20, 0.8, (255, 200, 0), x=20)
        if todos:
            text(frame, "TODO: finish " + ", ".join(sorted(todos)), h - 45, 0.6, (80, 80, 255))
        if last_rec is None and recognizer is not None and state == COUNTDOWN:
            text(frame, "(no hand seen)", h - 20, 0.6, (0, 165, 255))

        cv2.imshow(WINDOW, frame)
        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), 27):
            break
        if key == ord(" ") and state == WAITING:
            if source.images:
                source.next_image()
            state, state_t, sampled, last_rec = COUNTDOWN, time.time(), False, None
        if key == ord("r") and state in (GAME_OVER, WAITING):
            board = game.Scoreboard()
            champion = p_move = c_move = winner = None
            state, state_t = WAITING, time.time()

    source.release()
    cv2.destroyAllWindows()


def play_round(board, rec, todos):
    """Turn the recognized gesture into a move, play the round, update the score."""
    if rec is None:
        p_move = None
        if "gestures.py" not in todos:
            return None, None, None, "No hand seen - try again!", None
    else:
        p_move, ok = attempt(todos, "gestures.py", gestures.gesture_to_move, *rec)
        if ok and p_move is None:
            return None, None, None, f"Unclear gesture ({rec[0]} {rec[1]:.2f}) - try again!", None
    c_move, _ = attempt(todos, "game.py", game.computer_move)
    winner = None
    if p_move and c_move:
        winner, _ = attempt(todos, "game.py", game.decide_winner, p_move, c_move)
    champion = None
    if winner:
        _, ok = attempt(todos, "game.py", board.record, winner)
        if ok:
            over, ok2 = attempt(todos, "game.py", board.is_game_over)
            if ok2 and over:
                champion, _ = attempt(todos, "game.py", board.champion)
    msg = {"player": "You win the round!", "computer": "Computer wins the round",
           "tie": "Tie!"}.get(winner, "")
    return p_move, c_move, winner, msg, champion


def draw_result(frame, p_move, c_move, winner, msg):
    h, w = frame.shape[:2]
    if p_move is None and c_move is None and winner is None and msg:
        text(frame, msg, h // 2, 1.0, (0, 165, 255))
        return
    text(frame, f"You: {p_move or '???'}", h // 2 - 60, 1.4, x=40)
    text(frame, f"Computer: {c_move or '???'}", h // 2 - 60, 1.4, x=w // 2 + 20)
    if winner is None:
        text(frame, "Winner: ???", h // 2, 1.2, (0, 165, 255))
    else:
        color = {"player": (0, 255, 0), "computer": (0, 0, 255)}.get(winner, (255, 255, 255))
        text(frame, msg, h // 2, 1.2, color)


if __name__ == "__main__":
    main()
