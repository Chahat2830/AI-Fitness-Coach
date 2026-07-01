"""
Filename: analysis_service.py
Description: Orchestration service layer managing computer vision calculations and 
             consolidated single-call Groq Cloud fitness template evaluation.
"""

import sys
from pathlib import Path
import time
import logging
import json

# Enforce strict local directory hierarchy constraints
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from vision.pose_pipeline import PosePipeline
from measurements.measurement_engine import MeasurementEngine
from ai.gemini import GeminiCoach
from ai.parser import GeminiParser
from reporting.report_builder import ReportBuilder
from reporting.report_exporter import ReportExporter

from measurements.body_metrics import BodyMetrics     
from measurements.body_score import BodyScore         
from measurements.body_profile import BodyProfile

logging.basicConfig(level=logging.INFO)


class AnalysisService:
    """Complete, resilient multi-view engine execution pipeline."""

    def __init__(self):
        self.pipeline = PosePipeline()
        self.engine = MeasurementEngine()
        self.gemini = GeminiCoach()

    def _process_view(self, image_path, view_name):
        """Processes an image, resolving paths absolutely for strict backend precision."""
        annotated = PROJECT_ROOT / "outputs" / "annotated" / f"{view_name}.jpg"
        json_file = PROJECT_ROOT / "outputs" / "json" / f"{view_name}.json"

        annotated.parent.mkdir(parents=True, exist_ok=True)

        _, landmarks = self.pipeline.process_image(
            image_path=str(image_path),
            annotated_output=str(annotated),
            json_output=str(json_file)
        )
        return landmarks

    def analyze(self, front_image, side_image, back_image, user_info):
        """Orchestrates vision processing, scoring, and optimized single-call AI profiling."""
        start_time = time.time()
        self.engine.reset()
        
        pipeline_warnings = []

        # Step 1: Image Traversal Point Mapping
        try:
            front_lms = self._process_view(front_image, "front")
        except Exception as e:
            front_lms = None
            pipeline_warnings.append("Front-view image processing failed.")

        try:
            side_lms = self._process_view(side_image, "side")
        except Exception as e:
            side_lms = None
            pipeline_warnings.append("Side-view image processing failed.")

        try:
            back_lms = self._process_view(back_image, "back")
        except Exception as e:
            back_lms = None
            pipeline_warnings.append("Back-view image processing failed.")

        # Step 2: Compute measurements through Engine
        if front_lms:
            self.engine.set_view_landmarks("front", json.dumps({lm["id"]: lm for lm in front_lms}))
        if side_lms:
            self.engine.set_view_landmarks("side", json.dumps({lm["id"]: lm for lm in side_lms}))
        if back_lms:
            self.engine.set_view_landmarks("back", json.dumps({lm["id"]: lm for lm in back_lms}))

        self.engine.calculate_px_to_metric(user_info.get("height", 175.0), view='front' if front_lms else 'side')
        self.engine.run_analysis()
        raw_results = self.engine.get_results()

        # Populate internal state profile dataclass container structures
        profile = BodyProfile()
        profile.update_user(
            name=user_info.get("name", "User"),
            age=user_info.get("age", 20),
            gender=user_info.get("gender", "Male"),
            height=user_info.get("height", 170.0),
            weight=user_info.get("weight", 60.0),
            goal=user_info.get("goal", "Maintain Fitness")
        )
        
        if "front" in raw_results: profile.update_front(raw_results["front"])
        if "side" in raw_results: profile.update_side(raw_results["side"])
        if "back" in raw_results: profile.update_back(raw_results["back"])

        metrics = BodyMetrics(raw_results.get("front", {}), raw_results.get("side", {}), raw_results.get("back", {})).calculate()
        score = BodyScore(metrics).calculate()

        if "scores" in score:
            profile.update_score(score["scores"])
        else:
            profile.update_score(score)
            
        updated_profile_dict = profile.to_dict()
        updated_profile_dict["metrics"] = metrics

        # Step 4: Executing Unified Groq Query Handler Node
        ai_status = "completed"
        ai_data, workout_data, diet_data = {}, {}, {}
        
        # --- FIX: Initialize variable to an empty string to prevent UnboundLocalError ---
        raw_master_payload = ""
        
        try:
            raw_master_payload = self.gemini.analyze_all_in_one(updated_profile_dict)
            
            # Parse response block
            master_json = json.loads(raw_master_payload)
            
            ai_data = master_json.get("analysis", {})
            workout_data = master_json.get("workout", {})
            diet_data = master_json.get("diet", {})
            
        except Exception as master_err:
            logging.error(f"Groq Cloud generation failed: {str(master_err)}")
            ai_status = "failed"
            
            # Surface specific configuration guidance if the payload stayed empty
            if not raw_master_payload:
                ai_data = {
                    "summary": f"⚠️ **Groq Connection Failed:** {str(master_err)}.\n\n"
                               f"**Troubleshooting:** Make sure you installed `python-dotenv` via `pip install python-dotenv`, "
                               f"and verify that your `.env` file contains a valid `GROQ_API_KEY`."
                }
            else:
                ai_data = {
                    "summary": f"⚠️ **JSON Parsing Mismatch:** {str(master_err)}.\n\n"
                               f"Raw output slice: {raw_master_payload[:200]}"
                }

        elapsed_sec = time.time() - start_time

        # Compile report packaging through ReportBuilder pattern
        builder = ReportBuilder()
        
        report = (
            builder
            .set_user(updated_profile_dict["user"])
            .set_measurements({
                "front": updated_profile_dict["front"],
                "side": updated_profile_dict["side"],
                "back": updated_profile_dict["back"]
            })
            .set_metrics(metrics)
            .set_score(score)
            .set_ai({
                "ai_status": ai_status,
                "analysis": ai_data
            })
            .set_workout(workout_data if "weekly_plan" in workout_data else {"weekly_plan": [], "plan": workout_data})
            .set_diet(diet_data if "meal_plan" in diet_data else {"meal_plan": {}, "plan": diet_data})
            .set_images({
                "front": "outputs/annotated/front.jpg",
                "side": "outputs/annotated/side.jpg",
                "back": "outputs/annotated/back.jpg"
            })
            .build()
        )

        report.metadata.processing_time_sec = round(elapsed_sec, 2)
        report_output_path = PROJECT_ROOT / "outputs" / "reports" / "latest_report.json"
        ReportExporter.export_json(report, report_output_path)

        # Convert to dictionary layout and explicitly merge data for app.py fallback
        report_dict = report.to_dict()
        if "workout" not in report_dict or not report_dict["workout"]:
            report_dict["workout"] = workout_data
        if "diet" not in report_dict or not report_dict["diet"]:
            report_dict["diet"] = diet_data
            
        return report_dict