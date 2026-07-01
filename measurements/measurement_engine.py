"""
Filename: measurement_engine.py
Description: The central orchestrator that manages and aggregates raw anatomical 
             measurements from multiple viewpoints (Front, Side, Back).
"""

from typing import Dict, Any, Optional
import json

# --- FIXED SUBFOLDER RELATIVE IMPORTS ---
from .front_measurements import FrontMeasurements
from .back_measurements import BackMeasurements
from .side_measurements import SideMeasurements  
from .geometry import Geometry


class MeasurementState:
    """Stores the active analysis objects and results for current views."""
    def __init__(self):
        self.front: Optional[Dict[str, Any]] = None
        self.back: Optional[Dict[str, Any]] = None
        self.side: Optional[Dict[str, Any]] = None
        # The calculated conversion factor (pixels per metric unit)
        self.px_to_metric: Optional[float] = None 


class MeasurementEngine:
    """The central hub for organizing, calculating, and aggregating anthropometric data."""

    def __init__(self):
        self._raw_landmarks_data: Dict[str, Dict[int, Any]] = {}
        self._state = MeasurementState()

    def reset(self):
        """Resets structural storage frames to avoid state leakage between calculations."""
        self._raw_landmarks_data = {}
        self._state = MeasurementState()

    def load_user(self, name: str, age: int, gender: str, height_cm: float, weight_kg: float, goal: str):
        """Placeholder matching structural context signatures expected by AnalysisService."""
        pass

    def set_view_landmarks(self, view: str, landmarks_json: str):
        """
        Ingests the raw JSON landmarks string for a specific view.
        
        Args:
            view (str): 'front', 'back', or 'side'.
            landmarks_json (str): The raw JSON output from PosePipeline.
        """
        try:
            landmarks_dict = json.loads(landmarks_json)
            # MediaPipe uses string keys for integers; cast them back to int indices.
            if isinstance(landmarks_dict, list):
                # Handle list of dict landmark structures safely
                self._raw_landmarks_data[view.lower()] = {int(lm["id"]): lm for lm in landmarks_dict if "id" in lm}
            else:
                self._raw_landmarks_data[view.lower()] = {int(k): v for k, v in landmarks_dict.items()}
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            print(f"[Error] Failed to parse landmarks for view '{view}': {e}")
            self._raw_landmarks_data[view.lower()] = {}

    def calculate_px_to_metric(self, actual_height_metric: float, view: str = 'front'):
        """
        Calculates the pixel-to-metric conversion factor based on user's known height.
        """
        landmarks = self._raw_landmarks_data.get(view.lower())
        if not landmarks:
            print(f"[Warning] Cannot calibrate conversion: No landmarks for {view} view.")
            return

        # Simple top-to-bottom bounding fallback calculation using layout coordinates
        all_y = [lm["y"] for lm in landmarks.values() if "y" in lm]
        if all_y:
            pixel_height = max(all_y) - min(all_y)
            if pixel_height > 0:
                self._state.px_to_metric = actual_height_metric / pixel_height
                print(f"[Info] Calibration successful: {self._state.px_to_metric:.4f} units/px.")
                return
        
        print(f"[Warning] Calibration parameters uncalculated. Default scaling activated.")
        self._state.px_to_metric = 1.0

    def process_all(self, front_lms: Optional[list], side_lms: Optional[list], back_lms: Optional[list]):
        """
        Calculates all views at once to keep full compatibility with 
        the active execution loops inside your AnalysisService.
        """
        if front_lms:
            self._raw_landmarks_data['front'] = {int(lm["id"]): lm for lm in front_lms if "id" in lm}
        if side_lms:
            self._raw_landmarks_data['side'] = {int(lm["id"]): lm for lm in side_lms if "id" in lm}
        if back_lms:
            self._raw_landmarks_data['back'] = {int(lm["id"]): lm for lm in back_lms if "id" in lm}

        # Fallback calibration run
        self.calculate_px_to_metric(175.0, view='front' if front_lms else ('side' if side_lms else 'back'))
        self.run_analysis()
        return self

    def run_analysis(self):
        """
        Executes viewpoint-specific analysis engines based on the ingested landmarks map.
        """
        px_to_metric = self._state.px_to_metric

        # --- 1. Process Front View ---
        front_landmarks = self._raw_landmarks_data.get('front')
        if front_landmarks:
            # Instantiate the actual full class class wrapper found in your front_measurements.py
            front_analyzer = FrontMeasurements(front_landmarks)
            self._state.front = front_analyzer.calculate()

        # --- 2. Process Side View ---
        side_landmarks = self._raw_landmarks_data.get('side')
        if side_landmarks:
            side_analyzer = SideMeasurements(side_landmarks)
            self._state.side = side_analyzer.get_results(px_to_metric)

        # --- 3. Process Back View ---
        back_landmarks = self._raw_landmarks_data.get('back')
        if back_landmarks:
            # Instantiate the actual layout analyzer defined in your back_measurements.py
            back_analyzer = BackMeasurements(back_landmarks)
            self._state.back = back_analyzer.calculate()

    def get_results(self) -> Dict[str, Any]:
        """Aggregates results metrics into unified cross-view dictionary wrappers."""
        return self.to_dict()

    def to_dict(self) -> Dict[str, Any]:
        """Converts structural states into clean serializable properties."""
        return {
            "user": {},
            "front": self._state.front if self._state.front else {},
            "side": self._state.side if self._state.side else {},
            "back": self._state.back if self._state.back else {},
            "calibration_factor": self._state.px_to_metric
        }