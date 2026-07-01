"""
Filename: geometry.py
Description: Pure mathematical layout utility module handling vector, angle, and symmetry deviations.
             Updated to safely accept both dictionary and tuple point representations.
"""

import math

class Geometry:
    """Geometry utility class for body measurement calculations."""

    @staticmethod
    def _to_xy(p):
        """
        Helper method to normalize coordinates safely.
        Converts {"x": value, "y": value} or (x, y) into a consistent float tuple.
        """
        if isinstance(p, dict):
            return float(p.get("x", 0.0)), float(p.get("y", 0.0))
        return float(p[0]), float(p[1])

    @staticmethod
    def point(landmarks, index):
        """Return (x, y) coordinates for a landmark index map."""
        lm = landmarks[index]
        return (float(lm["x"]), float(lm["y"]))

    @staticmethod
    def distance(p1, p2):
        x1, y1 = Geometry._to_xy(p1)
        x2, y2 = Geometry._to_xy(p2)
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    def horizontal_distance(p1, p2):
        x1, _ = Geometry._to_xy(p1)
        x2, _ = Geometry._to_xy(p2)
        return abs(x2 - x1)

    @staticmethod
    def vertical_distance(p1, p2):
        _, y1 = Geometry._to_xy(p1)
        _, y2 = Geometry._to_xy(p2)
        return abs(y2 - y1)

    @staticmethod
    def midpoint(p1, p2):
        x1, y1 = Geometry._to_xy(p1)
        x2, y2 = Geometry._to_xy(p2)
        return ((x1 + x2) / 2, (y1 + y2) / 2)

    @staticmethod
    def angle(p1, p2):
        """Calculates absolute canvas orientation angle in degrees."""
        x1, y1 = Geometry._to_xy(p1)
        x2, y2 = Geometry._to_xy(p2)
        return math.degrees(math.atan2(y2 - y1, x2 - x1))

    @staticmethod
    def angle_deg(p1, p2):
        """Calculates relative angle deviation matching posture parameters."""
        x1, y1 = Geometry._to_xy(p1)
        x2, y2 = Geometry._to_xy(p2)
        return abs(math.degrees(math.atan2(y2 - y1, x2 - x1)))

    @staticmethod
    def h_delta(p1, p2):
        """Returns direct horizontal delta distance component."""
        x1, _ = Geometry._to_xy(p1)
        x2, _ = Geometry._to_xy(p2)
        return x2 - x1

    @staticmethod
    def symmetry(left, right):
        if max(left, right) == 0:
            return 0.0
        diff = abs(left - right)
        score = (1 - diff / max(left, right)) * 100
        return round(score, 2)

    @staticmethod
    def find_superior_coordinate(landmarks, coord='y'):
        """Finds highest anatomical bounds (e.g., top eye/nose baseline)."""
        values = [lm[coord] for lm in landmarks.values() if coord in lm]
        return min(values) if values else None

    @staticmethod
    def find_inferior_coordinate(landmarks, coord='y'):
        """Finds lowest anatomical bounds (e.g., ankle/heel baseline)."""
        values = [lm[coord] for lm in landmarks.values() if coord in lm]
        return max(values) if values else None