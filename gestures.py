"""Gesture recognition -- YOUR CODE (steps 4 and 5).

main.py shows '???' for any function below that still raises NotImplementedError.
Delete the `raise` line in each function once you've written it.

Docs: https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer/python
Built-in gestures: Closed_Fist, Open_Palm, Pointing_Up, Thumb_Down, Thumb_Up,
                   Victory, ILoveYou, None
"""
from pathlib import Path

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

MODEL_PATH = Path(__file__).resolve().parent / "models" / "gesture_recognizer.task"
CONFIDENCE_THRESHOLD = 0.6  # step 8: tune this


def load_recognizer(image_mode=False):
    """Load the model and return a GestureRecognizer.

    TODO (step 4): build options and create the recognizer. Skeleton:

        options = vision.GestureRecognizerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=str(MODEL_PATH)),
            running_mode=vision.RunningMode.VIDEO,   # IMAGE if image_mode
        )
        return vision.GestureRecognizer.create_from_options(options)
    """
    raise NotImplementedError


def recognize(recognizer, frame_bgr, timestamp_ms, image_mode=False):
    """Run the recognizer on one webcam frame.

    Return (gesture_name, confidence) for the top gesture, or None if no hand.

    TODO (step 4): skeleton:

        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = recognizer.recognize_for_video(image, int(timestamp_ms))
        # (use recognizer.recognize(image) when image_mode is True)
        # result.gestures is a list (one entry per hand) of lists of categories.
        # Each category has .category_name and .score.

    Also print the gesture and score so you can see what the model sees.
    """
    raise NotImplementedError


def gesture_to_move(name, score):
    """Map a gesture to 'rock', 'paper' or 'scissors'.

    Closed_Fist -> rock, Open_Palm -> paper, Victory -> scissors.
    Return None for anything else, or if score < CONFIDENCE_THRESHOLD.

    TODO (step 5)
    """
    raise NotImplementedError
