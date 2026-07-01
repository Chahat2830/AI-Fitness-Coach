from dataclasses import dataclass


@dataclass
class BodyMetrics:
    """
    Combines measurements from all three views into
    higher-level fitness metrics.

    These metrics are consumed by:
    - Body Scoring Engine
    - Gemini
    - Workout Generator
    - Progress Tracker
    """

    front: dict
    side: dict
    back: dict

    # ---------------------------------------------------------
    # Helper
    # ---------------------------------------------------------

    def _m(self, view, key, default=0):
        return view.get("measurements", {}).get(key, default)

    def _r(self, view, key, default=0):
        return view.get("derived_ratios", {}).get(key, default)

    def _s(self, view, key, default=0):
        return view.get("bilateral_symmetry", {}).get(key, default)

    # ---------------------------------------------------------
    # Upper Body
    # ---------------------------------------------------------

    def v_taper_index(self):
        """
        Larger is generally better.

        Shoulder / Waist
        """

        return self._r(
            self.front,
            "shoulder_to_waist_ratio"
        )

    # ---------------------------------------------------------

    def shoulder_dominance(self):
        """
        Shoulder relative to hips.
        """

        return self._r(
            self.front,
            "shoulder_to_hip_ratio"
        )

    # ---------------------------------------------------------

    def upper_body_balance(self):

        return self._r(
            self.front,
            "arm_length_to_torso_ratio"
        )

    # ---------------------------------------------------------

    def lower_body_balance(self):

        return self._r(
            self.front,
            "leg_length_to_torso_ratio"
        )

    # ---------------------------------------------------------
    # Posture
    # ---------------------------------------------------------

    def posture_index(self):

        torso = abs(
            self._m(
                self.side,
                "torso_angle_deg"
            )
        )

        pelvis = abs(
            self._m(
                self.side,
                "pelvis_angle_deg"
            )
        )

        spine = abs(
            self._m(
                self.back,
                "spine_angle_deg"
            )
        )

        score = max(

            0,

            100 -

            (

                abs(90 - torso)

                +

                abs(90 - pelvis)

                +

                abs(90 - spine)

            )

        )

        return round(score, 2)

    # ---------------------------------------------------------
    # Symmetry
    # ---------------------------------------------------------

    def overall_symmetry(self):

        values = [

            self._s(
                self.front,
                "upper_arm_symmetry"
            ),

            self._s(
                self.front,
                "forearm_symmetry"
            ),

            self._s(
                self.front,
                "leg_symmetry"
            ),

            self._s(
                self.back,
                "shoulder_symmetry"
            ),

            self._s(
                self.back,
                "hip_symmetry"
            )

        ]

        values = [

            v for v in values

            if v > 0

        ]

        if not values:

            return 0

        return round(

            sum(values)

            /

            len(values),

            2

        )

    # ---------------------------------------------------------
    # Development
    # ---------------------------------------------------------

    def back_development(self):

        return self._r(
            self.back,
            "back_to_hip_ratio"
        )

    # ---------------------------------------------------------

    def chest_development(self):

        shoulder = self._m(
            self.front,
            "shoulder_width_px"
        )

        chest = self._m(
            self.front,
            "chest_width_px"
        )

        if chest == 0:
            return 0

        return round(

            chest / shoulder,

            3

        )

    # ---------------------------------------------------------

    def waist_score(self):

        waist = self._m(
            self.front,
            "waist_width_px"
        )

        shoulder = self._m(
            self.front,
            "shoulder_width_px"
        )

        if shoulder == 0:
            return 0

        return round(

            1 -

            waist / shoulder,

            3

        )

    # ---------------------------------------------------------

    def body_proportion_index(self):

        upper = self.upper_body_balance()

        lower = self.lower_body_balance()

        if lower == 0:

            return 0

        return round(

            upper / lower,

            3

        )

    # ---------------------------------------------------------

    def analysis_quality(self):

        quality = [

            self.front
            .get(
                "analysis_quality",
                {}
            )
            .get(
                "visibility_score",
                0
            ),

            self.side
            .get(
                "analysis_quality",
                {}
            )
            .get(
                "visibility_score",
                0
            ),

            self.back
            .get(
                "analysis_quality",
                {}
            )
            .get(
                "visibility_score",
                0
            )

        ]

        quality = [

            q for q in quality

            if q > 0

        ]

        if not quality:

            return 0

        return round(

            sum(quality)

            /

            len(quality),

            2

        )

    # ---------------------------------------------------------

    def calculate(self):

        return {

            "v_taper_index":

                self.v_taper_index(),

            "shoulder_dominance":

                self.shoulder_dominance(),

            "upper_body_balance":

                self.upper_body_balance(),

            "lower_body_balance":

                self.lower_body_balance(),

            "body_proportion_index":

                self.body_proportion_index(),

            "overall_symmetry":

                self.overall_symmetry(),

            "posture_index":

                self.posture_index(),

            "back_development":

                self.back_development(),

            "chest_development":

                self.chest_development(),

            "waist_score":

                self.waist_score(),

            "analysis_quality":

                self.analysis_quality()

        }