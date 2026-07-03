import cv2
import numpy as np
from ultralytics import YOLO

class PoseDetector:
    """
    High-performance human posture topology tracking engine powered by Ultralytics YOLO.
    Bypasses MediaPipe legacy libraries to maintain native Python 3.14+ cloud compatibility.
    """
    def __init__(self):
        # Initializes the model weights. The file will automatically download locally on first execution.
        self.model = YOLO("yolo11n-pose.pt")

    def detect(self, image):
        """
        Runs object inference on a BGR image frame and returns structural keypoint tracking tensors.
        """
        # Run inference. verbose=False prevents console logs from cluttering the Streamlit console.
        results = self.model(image, verbose=False)
        return results