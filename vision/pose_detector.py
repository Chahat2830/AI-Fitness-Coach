import streamlit as st
import cv2
import numpy as np
# Direct import to bypass the dynamic solutions routing error entirely
import mediapipe.python.solutions.pose as mp_pose_solution

class PoseDetector:
    def __init__(self):
        # 1. Assign the directly imported module solution
        self.mp_pose = mp_pose_solution
        
        # 2. Initialize the actual MediaPipe Pose tracking object
        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,       # High-performance tracking
            enable_segmentation=False,
            min_detection_confidence=0.5
        )
        
        # 3. Initialize drawing utilities if your service uses them
        import mediapipe.python.solutions.drawing_utils as mp_drawing
        self.mp_drawing = mp_drawing