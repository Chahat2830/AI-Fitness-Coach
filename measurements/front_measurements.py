"""
Filename: front_measurements.py
Description: Extracts raw pixel coordinates and camera-invariant proportional ratios from the front viewpoint.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.landmarks import NOSE, LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_ELBOW, RIGHT_ELBOW, LEFT_WRIST, RIGHT_WRIST, LEFT_HIP, RIGHT_HIP, LEFT_KNEE, RIGHT_KNEE, LEFT_ANKLE, RIGHT_ANKLE
# --- FIXED RELATIVE IMPORT ---
from .geometry import Geometry

class UpperBodyMeasurements:
    @staticmethod
    def get_shoulder_width(landmarks):
        left = Geometry.point(landmarks, LEFT_SHOULDER)
        right = Geometry.point(landmarks, RIGHT_SHOULDER)
        return Geometry.horizontal_distance(left, right)

    @staticmethod
    def get_hip_width(landmarks):
        left = Geometry.point(landmarks, LEFT_HIP)
        right = Geometry.point(landmarks, RIGHT_HIP)
        return Geometry.horizontal_distance(left, right)

    @staticmethod
    def get_torso_length(landmarks):
        shoulder_mid = Geometry.midpoint(Geometry.point(landmarks, LEFT_SHOULDER), Geometry.point(landmarks, RIGHT_SHOULDER))
        hip_mid = Geometry.midpoint(Geometry.point(landmarks, LEFT_HIP), Geometry.point(landmarks, RIGHT_HIP))
        return Geometry.distance(shoulder_mid, hip_mid)

    @staticmethod
    def get_neck_width(shoulder_width):
        return 0.35 * shoulder_width

    @staticmethod
    def estimate_horizontal_span(landmarks, vertical_pct):
        left_shoulder = Geometry.point(landmarks, LEFT_SHOULDER)
        left_hip = Geometry.point(landmarks, LEFT_HIP)
        right_shoulder = Geometry.point(landmarks, RIGHT_SHOULDER)
        right_hip = Geometry.point(landmarks, RIGHT_HIP)

        left_pt = (
            left_shoulder[0] + vertical_pct * (left_hip[0] - left_shoulder[0]),
            left_shoulder[1] + vertical_pct * (left_hip[1] - left_shoulder[1])
        )
        right_pt = (
            right_shoulder[0] + vertical_pct * (right_hip[0] - right_shoulder[0]),
            right_shoulder[1] + vertical_pct * (right_hip[1] - right_shoulder[1])
        )
        return Geometry.horizontal_distance(left_pt, right_pt)

class ArmMeasurements:
    @staticmethod
    def get_left_segments(landmarks):
        shoulder = Geometry.point(landmarks, LEFT_SHOULDER)
        elbow = Geometry.point(landmarks, LEFT_ELBOW)
        wrist = Geometry.point(landmarks, LEFT_WRIST)
        upper = Geometry.distance(shoulder, elbow)
        forearm = Geometry.distance(elbow, wrist)
        return upper, forearm, (upper + forearm)

    @staticmethod
    def get_right_segments(landmarks):
        shoulder = Geometry.point(landmarks, RIGHT_SHOULDER)
        elbow = Geometry.point(landmarks, RIGHT_ELBOW)
        wrist = Geometry.point(landmarks, RIGHT_WRIST)
        upper = Geometry.distance(shoulder, elbow)
        forearm = Geometry.distance(elbow, wrist)
        return upper, forearm, (upper + forearm)

class LegMeasurements:
    @staticmethod
    def get_left_leg_length(landmarks):
        hip = Geometry.point(landmarks, LEFT_HIP)
        knee = Geometry.point(landmarks, LEFT_KNEE)
        ankle = Geometry.point(landmarks, LEFT_ANKLE)
        return Geometry.distance(hip, knee) + Geometry.distance(knee, ankle)

    @staticmethod
    def get_right_leg_length(landmarks):
        hip = Geometry.point(landmarks, RIGHT_HIP)
        knee = Geometry.point(landmarks, RIGHT_KNEE)
        ankle = Geometry.point(landmarks, RIGHT_ANKLE)
        return Geometry.distance(hip, knee) + Geometry.distance(knee, ankle)

class FrontMeasurements:
    def __init__(self, landmarks, user_height=None):
        self.landmarks = landmarks

    def _calculate_quality_metrics(self):
        if not self.landmarks:
            return {"visibility_score": 0.0, "status": "fail"}
        weighted_indices = {
            LEFT_SHOULDER: 0.20, RIGHT_SHOULDER: 0.20, LEFT_HIP: 0.15, RIGHT_HIP: 0.15,
            LEFT_KNEE: 0.075, RIGHT_KNEE: 0.075, LEFT_WRIST: 0.075, RIGHT_WRIST: 0.075,
            NOSE: 0.025, LEFT_ELBOW: 0.025, RIGHT_ELBOW: 0.025
        }
        total_score = sum(self.landmarks[idx].get("visibility", 0.0) * w for idx, w in weighted_indices.items() if idx in self.landmarks)
        return {"visibility_score": round(total_score, 2), "status": "excellent" if total_score >= 0.85 else ("good" if total_score >= 0.65 else "poor")}

    def _extract_measurements(self):
        sh_width = UpperBodyMeasurements.get_shoulder_width(self.landmarks)
        return {
            "shoulder_width_px": sh_width,
            "neck_width_px": UpperBodyMeasurements.get_neck_width(sh_width),
            "chest_width_px": UpperBodyMeasurements.estimate_horizontal_span(self.landmarks, 0.25),
            "waist_width_px": UpperBodyMeasurements.estimate_horizontal_span(self.landmarks, 0.65),
            "hip_width_px": UpperBodyMeasurements.get_hip_width(self.landmarks),
            "torso_length_px": UpperBodyMeasurements.get_torso_length(self.landmarks),
            "left_upper_arm_px": ArmMeasurements.get_left_segments(self.landmarks)[0],
            "left_forearm_px": ArmMeasurements.get_left_segments(self.landmarks)[1],
            "left_arm_total_px": ArmMeasurements.get_left_segments(self.landmarks)[2],
            "right_upper_arm_px": ArmMeasurements.get_right_segments(self.landmarks)[0],
            "right_forearm_px": ArmMeasurements.get_right_segments(self.landmarks)[1],
            "right_arm_total_px": ArmMeasurements.get_right_segments(self.landmarks)[2],
            "left_leg_length_px": LegMeasurements.get_left_leg_length(self.landmarks),
            "right_leg_length_px": LegMeasurements.get_right_leg_length(self.landmarks)
        }

    def _compute_ratios(self, m):
        avg_arm = (m["left_arm_total_px"] + m["right_arm_total_px"]) / 2.0
        avg_leg = (m["left_leg_length_px"] + m["right_leg_length_px"]) / 2.0
        t_len = m["torso_length_px"]
        return {
            "shoulder_to_hip_ratio": round(m["shoulder_width_px"] / m["hip_width_px"], 3) if m["hip_width_px"] > 0 else 0.0,
            "shoulder_to_chest_ratio": round(m["shoulder_width_px"] / m["chest_width_px"], 3) if m["chest_width_px"] > 0 else 0.0,
            "shoulder_to_waist_ratio": round(m["shoulder_width_px"] / m["waist_width_px"], 3) if m["waist_width_px"] > 0 else 0.0,
            "waist_to_hip_ratio": round(m["waist_width_px"] / m["hip_width_px"], 3) if m["hip_width_px"] > 0 else 0.0,
            "arm_length_to_torso_ratio": round(avg_arm / t_len, 3) if t_len > 0 else 0.0,
            "leg_length_to_torso_ratio": round(avg_leg / t_len, 3) if t_len > 0 else 0.0,
        }

    def _evaluate_symmetry(self, m):
        return {
            "upper_arm_symmetry": round(Geometry.symmetry(m["left_upper_arm_px"], m["right_upper_arm_px"]), 2),
            "forearm_symmetry": round(Geometry.symmetry(m["left_forearm_px"], m["right_forearm_px"]), 2),
            "leg_symmetry": round(Geometry.symmetry(m["left_leg_length_px"], m["right_leg_length_px"]), 2),
        }

    def calculate(self):
        raw_m = self._extract_measurements()
        return {
            "view": "front",
            "analysis_quality": self._calculate_quality_metrics(),
            "measurements": {k: round(v, 2) for k, v in raw_m.items()},
            "derived_ratios": self._compute_ratios(raw_m),
            "bilateral_symmetry": self._evaluate_symmetry(raw_m),
            "validation_warnings": []
        }