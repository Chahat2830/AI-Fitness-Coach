from mediapipe.python.solutions import pose
from mediapipe.python.solutions import drawing_utils
from mediapipe.python.solutions import drawing_styles

MP_POSE = pose

POSE = MP_POSE.Pose(
    static_image_mode=True,
    model_complexity=2,
    smooth_landmarks=True,
    enable_segmentation=False,
    min_detection_confidence=0.5,
)

DRAWING_UTILS = drawing_utils
DRAWING_STYLE = drawing_styles
POSE_CONNECTIONS = MP_POSE.POSE_CONNECTIONS

LANDMARK_NAMES = [
    landmark.name.lower()
    for landmark in MP_POSE.PoseLandmark
]