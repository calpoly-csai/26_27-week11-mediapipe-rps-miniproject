"""Run this first: python check_setup.py"""
import platform
import sys
from pathlib import Path

problems = 0


def ok(msg):
    print(f"  OK    {msg}")


def bad(msg, fix):
    global problems
    problems += 1
    print(f"  FAIL  {msg}\n        -> {fix}")


v = sys.version_info
if (3, 10) <= v[:2] <= (3, 13):
    ok(f"Python {v.major}.{v.minor}.{v.micro}")
else:
    bad(f"Python {v.major}.{v.minor} is not supported by MediaPipe",
        "Install Python 3.12 from https://www.python.org/downloads/release/python-3128/")

try:
    import cv2
    ok(f"opencv-python {cv2.__version__}")
except ImportError:
    cv2 = None
    bad("opencv-python is not installed", "pip install -r requirements.txt")

try:
    import mediapipe as mp
    ok(f"mediapipe {mp.__version__}")
except ImportError:
    mp = None
    bad("mediapipe is not installed", "pip install -r requirements.txt")

model = Path(__file__).resolve().parent / "models" / "gesture_recognizer.task"
if not model.exists():
    bad("models/gesture_recognizer.task is missing", "Re-clone the repo (git pull) so the model file is included")
elif mp is not None:
    try:
        from mediapipe.tasks import python as mp_python
        from mediapipe.tasks.python import vision
        vision.GestureRecognizer.create_from_options(vision.GestureRecognizerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=str(model))))
        ok("gesture model loads")
    except Exception as e:  # noqa: BLE001
        bad(f"model failed to load: {e}", "Re-clone the repo; if it persists, ask a helper")

if cv2 is not None:
    cap = cv2.VideoCapture(0)
    if cap.isOpened() and cap.read()[0]:
        ok("webcam works")
        cap.release()
    else:
        hint = ("System Settings > Privacy & Security > Camera: enable your terminal / VS Code, "
                "then restart it" if platform.system() == "Darwin"
                else "Close other apps using the camera and check camera privacy settings")
        bad("could not read from the webcam", hint + ". No webcam? Use: python main.py --images sample_images")

print("\nAll good!" if not problems else f"\n{problems} problem(s) to fix.")
sys.exit(1 if problems else 0)
