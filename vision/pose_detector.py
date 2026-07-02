import streamlit as st
import cv2

# 1. Direct structural import to bypass the broken 'solutions' dynamic attribute proxy
try:
    import mediapipe as mp
    from mediapipe.python.solutions import pose as mp_pose
except ImportError:
    # Fallback for local environments or different wheel distributions
    import mediapipe as mp
    mp_pose = mp.solutions.pose

class PoseDetector:
    """
    Encapsulates MediaPipe Pose Topology configuration.
    """
    
    def __init__(self):
        # 2. Use the directly imported module instead of trying to look up mp.solutions
        self.mp_pose = mp_pose
        
        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=False,
            min_detection_confidence=0.5
        )

    def detect(self, image):

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = self.pose.process(rgb)

        return results