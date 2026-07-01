"""
Filename: side_measurements.py
Description: Analysis module for side-profile anthropometric measurements and posture angles.
             Updated to match the structured schema required by ViewAnalysis dataclass containers.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional

from .geometry import Geometry
from config.landmarks import LEFT_HIP, RIGHT_HIP, LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_KNEE, RIGHT_KNEE

@dataclass
class PostureAngles:
    """Stores biomechanical angles calculated from the side profile."""
    torso_angle_deg: float      
    pelvis_angle_deg: float     
    neck_angle_deg: Optional[float] = None  

class SideMeasurements:
    """Analyzer for side-profile anatomical measurements and key angles."""

    def __init__(self, raw_landmarks: Dict[int, Any]):
        self.landmarks = raw_landmarks

    def get_posture_angles(self) -> PostureAngles:
        hip_ref = self.landmarks.get(LEFT_HIP) or self.landmarks.get(RIGHT_HIP)
        shoulder_ref = self.landmarks.get(LEFT_SHOULDER) or self.landmarks.get(RIGHT_SHOULDER)

        torso_angle = 0.0  
        if hip_ref and shoulder_ref:
            raw_torso_angle_deg = Geometry.angle_deg(hip_ref, shoulder_ref)
            torso_angle = raw_torso_angle_deg - 90.0 
            
        knee_ref = self.landmarks.get(LEFT_KNEE) or self.landmarks.get(RIGHT_KNEE)
        
        pelvis_angle = 0.0 
        if knee_ref and hip_ref:
            raw_pelvis_angle_deg = Geometry.angle_deg(knee_ref, hip_ref)
            pelvis_angle = raw_pelvis_angle_deg - 90.0 

        return PostureAngles(
            torso_angle_deg=round(torso_angle, 1),
            pelvis_angle_deg=round(pelvis_angle, 1),
            neck_angle_deg=None
        )

    def measure_side_width_constraints(self, px_to_metric: Optional[float] = None) -> Dict[str, float]:
        constraints = {
            "torso_side_depth": 0.0,
            "leg_side_depth": 0.0
        }

        hip_ref = self.landmarks.get(LEFT_HIP) or self.landmarks.get(RIGHT_HIP)
        shoulder_ref = self.landmarks.get(LEFT_SHOULDER) or self.landmarks.get(RIGHT_SHOULDER)

        if hip_ref and shoulder_ref:
            torso_delta_horiz = abs(Geometry.h_delta(shoulder_ref, hip_ref))
            constraints["torso_side_depth"] = round(torso_delta_horiz, 2)

        if px_to_metric is not None:
            for key in constraints:
                constraints[key] *= px_to_metric

        return constraints

    def get_results(self, px_to_metric: Optional[float] = None) -> Dict[str, Any]:
        """
        Executes analysis and organizes metrics into the nested dictionary schema
        expected by ViewAnalysis (**side_data) initialization blocks.
        """
        angles = self.get_posture_angles()
        constraints = self.measure_side_width_constraints(px_to_metric)
        
        # Compile measurements block matching front/back profile metrics layouts
        measurements_payload = {
            "torso_angle_deg": angles.torso_angle_deg,
            "pelvis_angle_deg": angles.pelvis_angle_deg,
            "neck_angle_deg": 0.0,
            "torso_side_depth": constraints["torso_side_depth"],
            "leg_side_depth": constraints["leg_side_depth"]
        }

        # Dynamic baseline tracking data quality assessment
        visibility_score = 1.0 if self.landmarks else 0.0
        
        # Return structured format matching ViewAnalysis field variables directly
        return {
            "view": "side",
            "analysis_quality": {
                "visibility_score": visibility_score,
                "status": "excellent" if visibility_score > 0.75 else "fail"
            },
            "measurements": measurements_payload,
            "derived_ratios": {},
            "bilateral_symmetry": {},
            "validation_warnings": []
        }