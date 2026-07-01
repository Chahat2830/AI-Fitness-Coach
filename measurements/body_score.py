from dataclasses import dataclass


@dataclass
class BodyScore:
    """
    Rule-based body scoring engine.

    Input:
        BodyMetrics.calculate()

    Output:
        Individual scores
        Overall score
        Body type
    """

    metrics: dict

    # ---------------------------------------------------------
    # Helper
    # ---------------------------------------------------------

    def _clip(self, value, low=0, high=100):
        return max(low, min(high, round(value, 2)))

    # ---------------------------------------------------------
    # Shoulder Score
    # ---------------------------------------------------------

    def shoulder_score(self):

        ratio = self.metrics.get("shoulder_dominance", 0)

        if ratio >= 1.60:
            return 100
        elif ratio >= 1.45:
            return 90
        elif ratio >= 1.30:
            return 80
        elif ratio >= 1.15:
            return 70
        else:
            return 60

    # ---------------------------------------------------------
    # Chest Score
    # ---------------------------------------------------------

    def chest_score(self):

        ratio = self.metrics.get("chest_development", 0)

        if ratio >= 0.95:
            return 100
        elif ratio >= 0.90:
            return 90
        elif ratio >= 0.85:
            return 80
        elif ratio >= 0.80:
            return 70
        else:
            return 60

    # ---------------------------------------------------------
    # Waist Score
    # ---------------------------------------------------------

    def waist_score(self):

        value = self.metrics.get("waist_score", 0)

        return self._clip(value * 100)

    # ---------------------------------------------------------
    # Posture Score
    # ---------------------------------------------------------

    def posture_score(self):

        return self._clip(
            self.metrics.get("posture_index", 0)
        )

    # ---------------------------------------------------------
    # Symmetry Score
    # ---------------------------------------------------------

    def symmetry_score(self):

        return self._clip(
            self.metrics.get("overall_symmetry", 0)
        )

    # ---------------------------------------------------------
    # Back Score
    # ---------------------------------------------------------

    def back_score(self):

        ratio = self.metrics.get(
            "back_development",
            0
        )

        if ratio >= 1.50:
            return 100
        elif ratio >= 1.35:
            return 90
        elif ratio >= 1.20:
            return 80
        elif ratio >= 1.05:
            return 70
        else:
            return 60

    # ---------------------------------------------------------
    # Legs Score
    # ---------------------------------------------------------

    def leg_score(self):

        ratio = self.metrics.get(
            "lower_body_balance",
            0
        )

        score = ratio * 60

        return self._clip(score)

    # ---------------------------------------------------------
    # Arms Score
    # ---------------------------------------------------------

    def arm_score(self):

        ratio = self.metrics.get(
            "upper_body_balance",
            0
        )

        score = ratio * 100

        return self._clip(score)

    # ---------------------------------------------------------
    # Body Type
    # ---------------------------------------------------------

    def body_type(self):

        taper = self.metrics.get(
            "v_taper_index",
            0
        )

        posture = self.metrics.get(
            "posture_index",
            0
        )

        if taper >= 1.60 and posture >= 90:
            return "Elite V-Taper"

        elif taper >= 1.45:
            return "Athletic"

        elif taper >= 1.30:
            return "Balanced"

        elif taper >= 1.10:
            return "Average"

        else:
            return "Straight"

    # ---------------------------------------------------------
    # Overall Score
    # ---------------------------------------------------------

    def overall_score(self):

        scores = [

            self.shoulder_score(),

            self.chest_score(),

            self.back_score(),

            self.arm_score(),

            self.leg_score(),

            self.waist_score(),

            self.posture_score(),

            self.symmetry_score()

        ]

        return round(

            sum(scores) / len(scores),

            2

        )

    # ---------------------------------------------------------
    # Fitness Level
    # ---------------------------------------------------------

    def fitness_level(self):

        score = self.overall_score()

        if score >= 95:
            return "Elite"

        elif score >= 90:
            return "Advanced"

        elif score >= 80:
            return "Intermediate"

        elif score >= 70:
            return "Beginner"

        else:
            return "Needs Improvement"

    # ---------------------------------------------------------
    # Priority Muscles
    # ---------------------------------------------------------

    def improvement_priority(self):

        priority = []

        if self.shoulder_score() < 80:
            priority.append("Shoulders")

        if self.chest_score() < 80:
            priority.append("Chest")

        if self.back_score() < 80:
            priority.append("Back")

        if self.arm_score() < 80:
            priority.append("Arms")

        if self.leg_score() < 80:
            priority.append("Legs")

        if self.posture_score() < 80:
            priority.append("Posture")

        return priority

    # ---------------------------------------------------------
    # Final Output
    # ---------------------------------------------------------

    def calculate(self):

        return {

            "overall_score":

                self.overall_score(),

            "fitness_level":

                self.fitness_level(),

            "body_type":

                self.body_type(),

            "scores": {

                "shoulders":

                    self.shoulder_score(),

                "chest":

                    self.chest_score(),

                "back":

                    self.back_score(),

                "arms":

                    self.arm_score(),

                "legs":

                    self.leg_score(),

                "waist":

                    self.waist_score(),

                "posture":

                    self.posture_score(),

                "symmetry":

                    self.symmetry_score()

            },

            "priority_focus":

                self.improvement_priority()

        }