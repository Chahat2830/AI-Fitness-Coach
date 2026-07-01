import cv2
import mediapipe as mp


class PoseDetector:
    """
    Detects human pose landmarks using MediaPipe.
    """

    def __init__(self):
        self.mp_pose = mp.solutions.pose

        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            smooth_landmarks=True,
            enable_segmentation=False,
            min_detection_confidence=0.5,
        )

    def detect(self, image):

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = self.pose.process(rgb)

        return results