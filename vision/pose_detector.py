import streamlit as st
import cv2
import mediapipe as mp

class PoseDetector:
    """
    Encapsulates MediaPipe Pose Topology configuration.
    """
    
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        
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