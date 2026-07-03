import cv2

class LandmarkVisualizer:
    """
    Renders skeletal tracking links and joint positions onto body profile image frames.
    Uses native OpenCV logic to bypass dynamic cloud rendering components completely.
    """
    def __init__(self):
        # Explicit connection pairs matching standard MediaPipe joint indices
        self.connections = [
            (11, 12), (11, 13), (13, 15), (12, 14), (14, 16), # Shoulders, Elbows, Wrists
            (11, 23), (12, 24), (23, 24),                     # Torso / Upper Waist Grid
            (23, 25), (25, 27), (24, 26), (26, 28),            # Hips, Knees, Ankles
            (27, 29), (28, 30), (29, 31), (30, 32)            # Feet Foundations
        ]

    def draw(self, image, results):
        output = image.copy()

        # Safely exit if no tracking targets were identified
        if not results or len(results) == 0 or results[0].keypoints is None:
            return output

        h, w, _ = output.shape
        keypoints_obj = results[0].keypoints
        xy = keypoints_obj.xy[0].cpu().numpy()     # Pixel coordinates
        
        if keypoints_obj.conf is not None:
            conf = keypoints_obj.conf[0].cpu().numpy()
        else:
            conf = [0.9] * len(xy)

        # Map COCO values back to the expected visualization indices
        coco_to_mp_map = {
            0: 0, 1: 2, 2: 5, 3: 7, 4: 8, 5: 11, 6: 12, 7: 13,
            8: 14, 9: 15, 10: 16, 11: 23, 12: 24, 13: 25, 14: 26, 15: 27, 16: 28
        }

        # Convert tracking arrays into pixel tuples
        pixel_coords = {}
        for coco_idx, pt in enumerate(xy):
            if conf[coco_idx] < 0.4:  # Filter out tracking points with low confidence
                continue
            cx, cy = int(pt[0]), int(pt[1])
            mp_idx = coco_to_mp_map.get(coco_idx)
            if mp_idx is not None:
                pixel_coords[mp_idx] = (cx, cy)

        # Draw structural skeletal lines (Deep Sky Blue)
        for start_idx, end_idx in self.connections:
            if start_idx in pixel_coords and end_idx in pixel_coords:
                cv2.line(
                    output,
                    pixel_coords[start_idx],
                    pixel_coords[end_idx],
                    color=(235, 206, 135),  # BGR Sky Blue
                    thickness=3,
                    lineType=cv2.LINE_AA
                )

        # Draw coordinate tracking markers (Bright Green)
        for idx, coord in pixel_coords.items():
            cv2.circle(
                output,
                coord,
                radius=5,
                color=(50, 205, 50),       # BGR Lime Green
                thickness=-1
            )

        return output