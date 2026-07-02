import cv2
import mediapipe as mp
# Direct namespace import to completely bypass the dynamic solutions attribute crash
import mediapipe.python.solutions.pose as mp_pose_solution

class PoseDetector:
    """
    Encapsulates MediaPipe Pose Topology configuration using secure direct library routing.
    """
    
    def __init__(self):
        # 1. Assign the directly imported module solution
        self.mp_pose = mp_pose_solution
        
        # 2. Initialize the actual MediaPipe Pose tracking layout engine
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