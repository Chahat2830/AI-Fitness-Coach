import streamlit as st
import cv2

# Safely import the sub-module components directly to bypass Python 3.14 dynamic attribute bugs
try:
    import mediapipe as mp
    from mediapipe.python.solutions import pose as mp_pose
except ImportError:
    # Fallback for local environments or different wheel distributions
    import mediapipe as mp
    mp_pose = mp.solutions.pose

class PoseDetector:
    """
    Encapsulates MediaPipe Pose Topology configuration safely.
    """
    
    def __init__(self):
        # Assign the safely imported module reference
        self.mp_pose = mp_pose
        
        # Initialize the baseline model tracking solution
        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=False,
            min_detection_confidence=0.5
        )

    def detect(self, image):
        """
        Processes a BGR image frame and extracts MediaPipe pose tracking landmarks.
        """
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb)
        return results