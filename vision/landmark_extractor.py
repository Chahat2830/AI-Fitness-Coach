import numpy as np

class LandmarkExtractor:
    """
    Translates Ultralytics YOLO COCO keypoint coordinate vectors into the 
    standardized 33-node topology format expected by the downstream AI fitness coach analytics.
    """
    def extract(self, results):
        # Ensure tracking instances exist inside the frame
        if not results or len(results) == 0 or results[0].keypoints is None:
            return None

        # Extract normalized coordinates (xy) and confidence scores (conf)
        keypoints_obj = results[0].keypoints
        xy = keypoints_obj.xy[0].cpu().numpy()     # Shape: (17, 2) -> Pixel x, y coordinates
        xyn = keypoints_obj.xyn[0].cpu().numpy()   # Shape: (17, 2) -> Normalized x, y coordinates
        
        # Pull confidence tracking score matrix safely
        if keypoints_obj.conf is not None:
            conf = keypoints_obj.conf[0].cpu().numpy() # Shape: (17,)
        else:
            conf = np.ones(17, dtype=np.float32) * 0.9

        # Map basic overlapping COCO indices directly to target positions
        # COCO: [0: nose, 1: L_eye, 2: R_eye, 3: L_ear, 4: R_ear, 5: L_shoulder, 6: R_shoulder, 
        #        7: L_elbow, 8: R_elbow, 9: L_wrist, 10: R_wrist, 11: L_hip, 12: R_hip, 
        #        13: L_knee, 14: R_knee, 15: L_ankle, 16: R_ankle]
        coco_to_mp_map = {
            0: 0,   # Nose
            1: 2,   # Left Eye
            2: 5,   # Right Eye
            3: 7,   # Left Ear
            4: 8,   # Right Ear
            5: 11,  # Left Shoulder
            6: 12,  # Right Shoulder
            7: 13,  # Left Elbow
            8: 14,  # Right Elbow
            9: 15,  # Left Wrist
            10: 16, # Right Wrist
            11: 23, # Left Hip
            12: 24, # Right Hip
            13: 25, # Left Knee
            14: 26, # Right Knee
            15: 27, # Left Ankle
            16: 28  # Right Ankle
        }

        # Initialize an empty array for 33 nodes with structural fallback defaults
        landmarks = []
        node_data = {}

        # Set default values for all 33 indices
        for i in range(33):
            node_data[i] = {"x": 0.5, "y": 0.5, "z": 0.0, "visibility": 0.0}

        # Fill in direct mappings from the YOLO prediction tensor
        for coco_idx, mp_idx in coco_to_mp_map.items():
            node_data[mp_idx] = {
                "x": float(xyn[coco_idx][0]),
                "y": float(xyn[coco_idx][1]),
                "z": 0.0,
                "visibility": float(conf[coco_idx])
            }

        # --- EXTENDED STRUCTURAL SYNTHESIS (INTERPOLATION) ---
        # 1. Fill in missing inner-eye boundaries safely using nose positions
        node_data[1] = node_data[2]   # Left Eye Inner
        node_data[3] = node_data[2]   # Left Eye Outer
        node_data[4] = node_data[5]   # Right Eye Inner
        node_data[6] = node_data[5]   # Right Eye Outer

        # 2. Map mouth lines using nose vector offsets
        node_data[9] = {"x": node_data[0]["x"] - 0.01, "y": node_data[0]["y"] + 0.02, "z": 0.0, "visibility": node_data[0]["visibility"]}
        node_data[10] = {"x": node_data[0]["x"] + 0.01, "y": node_data[0]["y"] + 0.02, "z": 0.0, "visibility": node_data[0]["visibility"]}

        # 3. Project hand extremities (pinky, index, thumb) outward relative to wrist position
        for wrist_idx, pinky, index, thumb, offset in [(15, 17, 19, 21, -0.02), (16, 18, 20, 22, 0.02)]:
            node_data[pinky] = {"x": node_data[wrist_idx]["x"] + offset, "y": node_data[wrist_idx]["y"] + 0.02, "z": 0.0, "visibility": node_data[wrist_idx]["visibility"]}
            node_data[index] = {"x": node_data[wrist_idx]["x"] + offset, "y": node_data[wrist_idx]["y"] + 0.03, "z": 0.0, "visibility": node_data[wrist_idx]["visibility"]}
            node_data[thumb] = {"x": node_data[wrist_idx]["x"] + (offset * 0.5), "y": node_data[wrist_idx]["y"] + 0.01, "z": 0.0, "visibility": node_data[wrist_idx]["visibility"]}

        # 4. Project foot foundations (heels and toes) downward relative to ankles
        for ankle_idx, heel, toe, offset in [(27, 29, 31, -0.02), (28, 30, 32, 0.02)]:
            node_data[heel] = {"x": node_data[ankle_idx]["x"], "y": node_data[ankle_idx]["y"] + 0.02, "z": 0.0, "visibility": node_data[ankle_idx]["visibility"]}
            node_data[toe] = {"x": node_data[ankle_idx]["x"] + offset, "y": node_data[ankle_idx]["y"] + 0.04, "z": 0.0, "visibility": node_data[ankle_idx]["visibility"]}

        # Compile everything into a structured JSON dictionary layout
        for idx in range(33):
            landmarks.append({
                "id": idx,
                "x": node_data[idx]["x"],
                "y": node_data[idx]["y"],
                "z": node_data[idx]["z"],
                "visibility": node_data[idx]["visibility"]
            })

        return landmarks