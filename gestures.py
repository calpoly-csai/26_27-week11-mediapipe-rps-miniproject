"""Gesture recognition -- YOUR CODE (steps 4 and 5).

How main.py uses this file (you don't call these yourself):
  1. load_recognizer()  -- once, at startup. Loads the AI model.
  2. recognize()        -- on EVERY webcam frame (~30 times a second).
                           Returns what the model sees, e.g. ("Closed_Fist", 0.94).
  3. gesture_to_move()  -- once per round, at "Shoot!". Turns that gesture into a move.

main.py shows '???' for any function below that still raises NotImplementedError.
Delete the `raise` line in each function once you've written it.

New to OpenCV / MediaPipe? GUIDE.md explains every library call used here.
Docs: https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer/python
Built-in gestures: Closed_Fist, Open_Palm, Pointing_Up, Thumb_Down, Thumb_Up,
                   Victory, ILoveYou, None
"""
from pathlib import Path

import cv2                                   # OpenCV: webcam, images, drawing
import mediapipe as mp                       # MediaPipe: Google's on-device AI models
from mediapipe.tasks import python as mp_python   # BaseOptions (which model file to load)
from mediapipe.tasks.python import vision         # GestureRecognizer and its options

# The model file. A .task file bundles three models: one finds the hand, one places
# 21 landmarks on it, and one classifies the gesture those landmarks form.
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

    What each line does:
      - GestureRecognizerOptions(...) is a settings object. Nothing runs yet; you're
        just describing the recognizer you want.
      - BaseOptions(model_asset_path=...) says which model file to load. It needs a
        plain string, hence str(MODEL_PATH).
      - running_mode picks how frames are handled:
          VIDEO: frames are a continuous stream. MediaPipe tracks the hand from one
                 frame to the next instead of searching the whole image each time,
                 which is faster and steadier. Needs a timestamp per frame.
          IMAGE: every picture is independent. main.py uses this with --images,
                 so pick IMAGE when image_mode is True.
      - create_from_options(options) actually loads the model into memory and returns
        the recognizer. This is the slow part, which is why main.py calls it only once.

    Optional: add num_hands=1 to the options so only one hand is tracked.
    """
    raise NotImplementedError


def recognize(recognizer, frame_bgr, timestamp_ms, image_mode=False):
    """Run the recognizer on one webcam frame.

    Return (gesture_name, confidence) for the top gesture, or None if no hand.

    Inputs (main.py passes these in):
      recognizer   -- what load_recognizer() returned
      frame_bgr    -- one webcam image: a numpy array of shape (height, width, 3),
                      one number 0-255 per colour channel per pixel
      timestamp_ms -- milliseconds since the program started; always increasing

    TODO (step 4): skeleton:

        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = recognizer.recognize_for_video(image, int(timestamp_ms))
        # (use recognizer.recognize(image) when image_mode is True)
        # result.gestures is a list (one entry per hand) of lists of categories.
        # Each category has .category_name and .score.

    What each line does:
      1. cv2.cvtColor(..., COLOR_BGR2RGB): OpenCV stores colours as Blue-Green-Red,
         MediaPipe expects Red-Green-Blue. Skip this and the model sees a wrongly
         coloured hand and does worse.
      2. mp.Image(...) wraps the numpy array in MediaPipe's own image type. SRGB
         means "normal 8-bit RGB colour".
      3. recognize_for_video(image, timestamp) runs all three models on the frame.
         The timestamp tells VIDEO mode how much time passed since the last frame, so
         it can track the hand. It must be an int and must go up every call (main.py
         already guarantees that). In IMAGE mode there's no timeline, so it's just
         recognizer.recognize(image).

    What `result` looks like (print(result) to see yours):

        GestureRecognizerResult(
          gestures=[                       # one list per hand found
            [Category(score=0.94, category_name='Closed_Fist', ...)]  # best guess first
          ],
          handedness=[[Category(category_name='Right', ...)]],  # left or right hand
          hand_landmarks=[[NormalizedLandmark(x=0.52, y=0.71, z=0.0), ...]],  # 21 points
          hand_world_landmarks=[...],      # same 21 points in metres (not needed)
        )

      - result.gestures[0]    -> the first hand's guesses
      - result.gestures[0][0] -> that hand's best guess; use .category_name and .score
      - No hand in the frame?  result.gestures is an empty list [], so gestures[0]
        would crash with IndexError. Check `if not result.gestures:` and return None.

    Also print the gesture and score so you can see what the model sees.
    """
    raise NotImplementedError


def gesture_to_move(name, score):
    """Map a gesture to 'rock', 'paper' or 'scissors'.

    Closed_Fist -> rock, Open_Palm -> paper, Victory -> scissors.
    Return None for anything else, or if score < CONFIDENCE_THRESHOLD.

    Inputs: exactly what recognize() returned, e.g. name="Victory", score=0.88.
      score is the model's confidence, 0.0 (no idea) to 1.0 (certain). A low score
      means a half-formed or blurry gesture; returning None makes main.py say
      "Unclear gesture - try again!" instead of guessing.

    TODO (step 5): check the score first, then translate the name. A dict such as
    {"Closed_Fist": "rock", ...} with .get(name) handles "anything else -> None" for free.
    """
    raise NotImplementedError
