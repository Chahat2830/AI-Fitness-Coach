"""
Gemini Response Parser

Responsibilities
----------------
1. Remove markdown formatting.
2. Extract JSON from the response.
3. Parse JSON safely.
4. Validate required fields.
5. Return consistent output.
"""

import json
import re
import logging
from typing import Dict, Any


logging.basicConfig(level=logging.INFO)


class GeminiParser:

    # ---------------------------------------------------------
    # Expected schema
    # ---------------------------------------------------------

    REQUIRED_KEYS = [

        "summary",

        "body_type",

        "overall_condition",

        "strengths",

        "weaknesses",

        "posture",

        "symmetry",

        "priority_focus",

        "recommendations",

        "estimated_improvement_time",

        "motivation"

    ]

    # ---------------------------------------------------------
    # Remove Markdown
    # ---------------------------------------------------------

    @staticmethod
    def remove_markdown(text: str) -> str:

        text = text.strip()

        text = re.sub(
            r"```json",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"```",
            "",
            text
        )

        return text.strip()

    # ---------------------------------------------------------
    # Extract JSON
    # ---------------------------------------------------------

    @staticmethod
    def extract_json(text: str) -> str:
        """
        Extract JSON object from mixed text.
        """

        start = text.find("{")

        end = text.rfind("}")

        if start == -1 or end == -1:

            raise ValueError(
                "No JSON object found."
            )

        return text[start:end + 1]

    # ---------------------------------------------------------
    # Parse
    # ---------------------------------------------------------

    @classmethod
    def parse(cls, response: str) -> Dict[str, Any]:

        try:

            cleaned = cls.remove_markdown(
                response
            )

            json_text = cls.extract_json(
                cleaned
            )

            data = json.loads(
                json_text
            )

            cls.validate(data)

            return {

                "success": True,

                "data": data,

                "error": None

            }

        except Exception as e:

            logging.exception(e)

            return {

                "success": False,

                "data": None,

                "error": str(e)

            }

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    @classmethod
    def validate(cls, data: Dict):

        missing = []

        for key in cls.REQUIRED_KEYS:

            if key not in data:

                missing.append(key)

        if missing:

            raise ValueError(

                f"Missing fields: {missing}"

            )

    # ---------------------------------------------------------
    # Pretty Print
    # ---------------------------------------------------------

    @staticmethod
    def pretty(data: Dict):

        return json.dumps(

            data,

            indent=4,

            ensure_ascii=False

        )

    # ---------------------------------------------------------
    # Safe Access
    # ---------------------------------------------------------

    @staticmethod
    def get(data: Dict, key, default=None):

        return data.get(key, default)