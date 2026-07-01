import json


class DietPromptTemplate:
    """
    Prompt template for personalized nutrition planning.
    Provides automated structural splits for both Vegetarian and Non-Vegetarian pathways.
    """

    @staticmethod
    def build(profile: dict):

        payload = {
            "user": profile.get("user", {}),
            "score": profile.get("score", {})
        }

        profile_json = json.dumps(
            payload,
            indent=4
        )

        return f"""
You are an expert certified sports nutritionist.

User Profile & Metrics:
{profile_json}

Generate a comprehensive nutrition plan tailored to the user's fitness goal. 
Because dietary preferences vary among gym members, you MUST provide two distinct meal plans inside the JSON response: 
one completely Vegetarian (Veg) option and one Non-Vegetarian (Non-Veg) option.

Requirements:
1. Calculate optimal daily target calories based on user goal.
2. Estimate macronutrient split targets (Protein, Carbs, Fats in grams).
3. Suggest hydration metrics (minimum daily water in liters).
4. Create a 1-day sample meal schedule split into two clear tracking objects: 'veg' and 'non_veg'.
5. Recommend a clean supplement stack if useful for their goal.
6. Provide expert nutritional coaching tips.

Return ONLY valid JSON matching the exact schema below. Do NOT wrap it in markdown block formatting.

Schema:
{{
    "goal": "",
    "daily_calories": 0,
    "protein_g": 0,
    "carbs_g": 0,
    "fat_g": 0,
    "water_liters": 0.0,
    "meal_plan": {{
        "veg": {{
            "breakfast": [],
            "lunch": [],
            "snack": [],
            "dinner": []
        }},
        "non_veg": {{
            "breakfast": [],
            "lunch": [],
            "snack": [],
            "dinner": []
        }}
    }},
    "supplements": [],
    "tips": []
}}

Return ONLY JSON. Do not include introductory text or trailing notes.
"""