"""
Filename: back_measurements.py
Description: Extracts structural metrics from the back viewpoint.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.landmarks import LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_HIP, RIGHT_HIP, LEFT_KNEE, RIGHT_KNEE, LEFT_ANKLE, RIGHT_ANKLE, LEFT_WRIST, RIGHT_WRIST
# --- FIXED RELATIVE IMPORT ---
from .geometry import Geometry

class BackMeasurements:
    def __init__(self, landmarks, user_height=None):
        self.landmarks = landmarks

    def _calculate_quality_metrics(self):
        if not self.landmarks:
            return {"visibility_score": 0.0, "status": "fail"}
        key_indices = [LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_HIP, RIGHT_HIP, LEFT_KNEE, RIGHT_KNEE, LEFT_ANKLE, RIGHT_ANKLE]
        score = sum(self.landmarks[idx].get("visibility", 0.0) for idx in key_indices if idx in self.landmarks) / len(key_indices)
        return {"visibility_score": round(score, 2), "status": "good" if score >= 0.75 else "poor"}

    def calculate(self):
        if not self.landmarks:
            return {"view": "back", "analysis_quality": {"visibility_score": 0.0, "status": "fail"}, "measurements": {}, "derived_ratios": {}, "bilateral_symmetry": {}, "validation_warnings": ["Missing landmarks"]}

        l_shoulder = Geometry.point(self.landmarks, LEFT_SHOULDER)
        r_shoulder = Geometry.point(self.landmarks, RIGHT_SHOULDER)
        l_hip = Geometry.point(self.landmarks, LEFT_HIP)
        r_hip = Geometry.point(self.landmarks, RIGHT_HIP)

        shoulder_mid = Geometry.midpoint(l_shoulder, r_shoulder)
        hip_mid = Geometry.midpoint(l_hip, r_hip)

        measurements = {
            "back_width_px": round(Geometry.horizontal_distance(l_shoulder, r_shoulder), 2),
            "hip_width_px": round(Geometry.horizontal_distance(l_hip, r_hip), 2),
            "spine_angle_deg": round(Geometry.angle(hip_mid, shoulder_mid), 2)
        }

        l_arm_len = Geometry.distance(l_shoulder, Geometry.point(self.landmarks, LEFT_WRIST))
        r_arm_len = Geometry.distance(r_shoulder, Geometry.point(self.landmarks, RIGHT_WRIST))

        return {
            "view": "back",
            "analysis_quality": self._calculate_quality_metrics(),
            "measurements": measurements,
            "derived_ratios": {"back_to_hip_ratio": round(measurements["back_width_px"] / measurements["hip_width_px"], 3) if measurements["hip_width_px"] > 0 else 0.0},
            "bilateral_symmetry": {
                "shoulder_symmetry": round(Geometry.symmetry(l_shoulder[1], r_shoulder[1]), 2), 
                "hip_symmetry": round(Geometry.symmetry(l_hip[1], r_hip[1]), 2),           
                "arm_length_symmetry": round(Geometry.symmetry(l_arm_len, r_arm_len), 2)
            },
            "validation_warnings": []
        }