"""
Central Prompt Manager

This file is the only place that the Gemini client should use
to obtain prompts.

Instead of importing individual templates throughout the project,
everything goes through PromptManager.
"""

from ai.templates.body_analysis import BodyAnalysisTemplate
from ai.templates.workout_prompt import WorkoutPromptTemplate
from ai.templates.diet_prompt import DietPromptTemplate
from ai.templates.progress_prompt import ProgressPromptTemplate


class PromptManager:
    """
    Central prompt routing class.
    """

    # -----------------------------------------------------
    # BODY ANALYSIS
    # -----------------------------------------------------

    @staticmethod
    def body_analysis(profile: dict) -> str:
        """
        Build body analysis prompt.
        """

        return BodyAnalysisTemplate.build(profile)

    # -----------------------------------------------------
    # WORKOUT
    # -----------------------------------------------------

    @staticmethod
    def workout(profile: dict) -> str:
        """
        Build workout generation prompt.
        """

        return WorkoutPromptTemplate.build(profile)

    # -----------------------------------------------------
    # DIET
    # -----------------------------------------------------

    @staticmethod
    def diet(profile: dict) -> str:
        """
        Build diet generation prompt.
        """

        return DietPromptTemplate.build(profile)

    # -----------------------------------------------------
    # PROGRESS
    # -----------------------------------------------------

    @staticmethod
    def progress(
        current_profile: dict,
        previous_profile: dict
    ) -> str:
        """
        Compare two body scans.
        """

        return ProgressPromptTemplate.build(
            current_profile,
            previous_profile
        )

    # -----------------------------------------------------
    # Generic Router
    # -----------------------------------------------------

    @staticmethod
    def get_prompt(task: str, **kwargs) -> str:
        """
        Generic prompt router.

        Supported tasks:

        body_analysis

        workout

        diet

        progress
        """

        task = task.lower()

        if task == "body_analysis":

            return PromptManager.body_analysis(
                kwargs["profile"]
            )

        elif task == "workout":

            return PromptManager.workout(
                kwargs["profile"]
            )

        elif task == "diet":

            return PromptManager.diet(
                kwargs["profile"]
            )

        elif task == "progress":

            return PromptManager.progress(
                kwargs["current_profile"],
                kwargs["previous_profile"]
            )

        else:

            raise ValueError(
                f"Unknown prompt task: {task}"
            )