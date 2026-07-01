import json


class ProgressPromptTemplate:
    """
    Compare two body scans and generate progress analysis.
    """

    @staticmethod
    def build(current_profile: dict,
              previous_profile: dict):

        payload = {

            "previous_scan": previous_profile,

            "current_scan": current_profile

        }

        scans = json.dumps(
            payload,
            indent=4
        )

        return f"""
You are an AI Fitness Progress Analyst.

Compare these two body scans.

{scans}

Tasks:

1. Compare body score.

2. Compare posture.

3. Compare symmetry.

4. Compare body proportions.

5. Identify improvements.

6. Identify regressions.

7. Suggest next priorities.

Return ONLY JSON.

Schema:

{{
    "overall_progress":"",

    "improved_areas":[],

    "declined_areas":[],

    "unchanged_areas":[],

    "score_difference":0,

    "next_focus":[],

    "motivation":""
}}

Return ONLY JSON.
"""