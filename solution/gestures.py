"""Gesture recognition -- SOLUTION version."""
from pathlib import Path

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "gesture_recognizer.task"
CONFIDENCE_THRESHOLD = 0.6

GESTURE_TO_MOVE = {
    "Closed_Fist": "rock",
    "Open_Palm": "paper",
    "Victory": "scissors",
}


def load_recognizer(image_mode=False):
    """Load the model. VIDEO mode (default) tracks hands across frames."""
    options = vision.GestureRecognizerOptions(
        base_options=mp_python.BaseOptions(model_asset_path=str(MODEL_PATH)),
        running_mode=vision.RunningMode.IMAGE if image_mode else vision.RunningMode.VIDEO,
        num_hands=1,
    )
    return vision.GestureRecognizer.create_from_options(options)


def recognize(recognizer, frame_bgr, timestamp_ms, image_mode=False):
    """Return (gesture_name, confidence) for the top gesture, or None if no hand."""
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    if image_mode:
        result = recognizer.recognize(image)
    else:
        result = recognizer.recognize_for_video(image, int(timestamp_ms))
    if not result.gestures:
        return None
    top = result.gestures[0][0]
    return top.category_name, top.score


def gesture_to_move(name, score):
    """Map a gesture to 'rock'/'paper'/'scissors', or None if unknown/low confidence."""
    if score < CONFIDENCE_THRESHOLD:
        return None
    return GESTURE_TO_MOVE.get(name)
