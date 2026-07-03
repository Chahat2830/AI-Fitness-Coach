import cv2

# Try importing MediaPipe modules safely. If it fails due to Python 3.14+, trigger manual rendering.
try:
    import mediapipe as mp
    import mediapipe.python.solutions.drawing_utils as mp_drawing
    import mediapipe.python.solutions.pose as mp_pose_solution
    MEDIAPIPE_AVAILABLE = True
except (ImportError, AttributeError):
    MEDIAPIPE_AVAILABLE = False


class LandmarkVisualizer:
    """
    Handles drawing pose landmarks onto image frames with a native OpenCV fallback
    to prevent application crashes on unsupported cloud runtimes (Python 3.14+).
    """

    def __init__(self):
        if MEDIAPIPE_AVAILABLE:
            self.drawer = mp_drawing
            self.pose = mp_pose_solution
            # Map structural skeletal connection pairs safely from MediaPipe
            self.connections = self.pose.POSE_CONNECTIONS
        else:
            self.drawer = None
            self.pose = None
            # Standard MediaPipe Pose Topology Connection pairs for drawing manual lines
            self.connections = [
                (11, 12), (11, 13), (13, 15), (12, 14), (14, 16), # Upper Body / Arms
                (11, 23), (12, 24), (23, 24),                     # Torso / Hips
                (23, 25), (25, 27), (24, 26), (26, 28)            # Legs / Lower Body
            ]

    def draw(self, image, results):
        output = image.copy()

        # 1. Check if landmarks are present in the results payload
        if not results or not hasattr(results, 'pose_landmarks') or not results.pose_landmarks:
            return output

        # 2. Standard MediaPipe Drawing Track
        if MEDIAPIPE_AVAILABLE and self.drawer is not None:
            self.drawer.draw_landmarks(
                output,
                results.pose_landmarks,
                self.connections,
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

        # 3. Clean OpenCV Manual Rendering Fallback (Runs on Python 3.14 Containers)
        else:
            h, w, _ = output.shape
            landmarks = results.pose_landmarks.landmark
            pixel_coords = {}

            # Convert normalized coordinate vectors to explicit scale pixel points
            for idx, lm in enumerate(landmarks):
                # Only map highly visible tracking coordinates to avoid noisy artifacts
                if hasattr(lm, 'visibility') and lm.visibility < 0.5:
                    continue
                cx, cy = int(lm.x * w), int(lm.y * h)
                pixel_coords[idx] = (cx, cy)

            # Draw Skeletal Tracking Connection Lines (Red)
            for start_idx, end_idx in self.connections:
                if start_idx in pixel_coords and end_idx in pixel_coords:
                    cv2.line(
                        output, 
                        pixel_coords[start_idx], 
                        pixel_coords[end_idx], 
                        color=(255, 0, 0),   # BGR Red
                        thickness=2
                    )

            # Draw Joint Keypoints Overlay (Green)
            for idx, coord in pixel_coords.items():
                cv2.circle(
                    output, 
                    coord, 
                    radius=4, 
                    color=(0, 255, 0),       # BGR Green
                    thickness=-1             # Solid Fill
                )

            return output