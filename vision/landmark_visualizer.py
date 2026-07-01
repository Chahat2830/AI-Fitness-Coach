import cv2
import mediapipe as mp


class LandmarkVisualizer:

    def __init__(self):

        self.drawer = mp.solutions.drawing_utils

        self.pose = mp.solutions.pose

    def draw(self, image, results):

        output = image.copy()

        if results.pose_landmarks:

            self.drawer.draw_landmarks(

                output,

                results.pose_landmarks,

                self.pose.POSE_CONNECTIONS,

                self.drawer.DrawingSpec(
                    color=(0, 255, 0),
                    thickness=3,
                    circle_radius=4,
                ),

                self.drawer.DrawingSpec(
                    color=(255, 0, 0),
                    thickness=2,
                ),
            )

        return output