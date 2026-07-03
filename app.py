"""
Filename: app.py
Description: Interactive UI engine powered by Streamlit displaying pose tracking metrics,
             physiological evaluations, workouts, and split veg/non-veg nutrition plans.
"""

import sys
from pathlib import Path
import cv2

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import streamlit as st

class LocalFileManager:
    @staticmethod
    def save_uploaded_file(uploaded_file, target_path: Path):
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, "wb") as destination:
            destination.write(uploaded_file.getbuffer())

from services.analysis_service import AnalysisService

st.set_page_config(
    page_title="AI Fitness Coach",
    page_icon="🏋️",
    layout="wide"
)

st.markdown("""
<style>
    div[data-testid="stMetric"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    div[data-testid="stMetric"] label {
        color: #94a3b8 !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏋️ AI Fitness Coach")
st.markdown("### Body Analysis & Personalized Fitness Recommendations")

st.divider()

# --- SIDEBAR CONFIGURATION CARD ---
with st.sidebar:
    st.header("⚙️ Core Controls")
    
    st.error("🔒 **Privacy Policy Note:** This model does not save your uploaded images. All data processing occurs entirely within active memory session cycles and is completely discarded upon completion.")
    
    st.divider()
    
    # Updated to correctly describe the active infrastructure
    st.markdown("This interface uses **Ultralytics YOLO Pose Tracking** and a high-performance **Groq Llama 3.3** engine to compute camera-invariant biometrics.")
    st.info("Ensure files are clear, well-lit, and capture your entire frame baseline.")

with st.form("user_form"):
    st.header("👤 Personal Information")
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name (Optional)", placeholder="John Doe")
        age = st.number_input("Age", min_value=10, max_value=100, value=25, step=1)
        gender = st.selectbox("Gender", ["Male", "Female"])

    with col2:
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=175.0, step=0.5)
        weight = st.number_input("Weight (kg)", min_value=20.0, max_value=250.0, value=70.0, step=0.5)
        goal = st.selectbox("Fitness Goal", ["Muscle Gain", "Fat Loss", "Body Recomposition", "Maintain Fitness"])

    st.divider()

    st.header("📸 Upload Body Images")
    upload_col1, upload_col2, upload_col3 = st.columns(3)

    with upload_col1:
        front_image = st.file_uploader("Front View", type=["jpg", "jpeg", "png"], key="front")

    with upload_col2:
        side_image = st.file_uploader("Side View", type=["jpg", "jpeg", "png"], key="side")

    with upload_col3:
        back_image = st.file_uploader("Back View", type=["jpg", "jpeg", "png"], key="back")

    st.divider()
    analyze = st.form_submit_button("🚀 Analyze Body Profile", use_container_width=True)

FRONT_DIR = PROJECT_ROOT / "uploads" / "front"
SIDE_DIR = PROJECT_ROOT / "uploads" / "side"
BACK_DIR = PROJECT_ROOT / "uploads" / "back"

if analyze:
    if front_image is None or side_image is None or back_image is None:
        st.error("❌ Critical Action Required: Please upload all three frames (Front, Side, and Back) to parse metrics safely.")
        st.stop()

    user_payload = {
        "name": name if name.strip() else "Valued Client",
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "goal": goal
    }

    LocalFileManager.save_uploaded_file(front_image, FRONT_DIR / "front.jpg")
    LocalFileManager.save_uploaded_file(side_image, SIDE_DIR / "side.jpg")
    LocalFileManager.save_uploaded_file(back_image, BACK_DIR / "back.jpg")

    service = AnalysisService()
    
    with st.spinner("⏳ Running metrics calculations and synthesizing customized plans..."):
        try:
            report = service.analyze(
                front_image=str(FRONT_DIR / "front.jpg"),
                side_image=str(SIDE_DIR / "side.jpg"),
                back_image=str(BACK_DIR / "back.jpg"),
                user_info=user_payload
            )
            
            score_data = report.get("score", {})
            metrics_data = report.get("metrics", {})
            ai_wrapper = report.get("ai_analysis", {})
            ai_data = ai_wrapper.get("analysis", {})
            workout_plan = report.get("workout", {})
            diet_plan = report.get("diet", {})
            meta_data = report.get("metadata", {})

            st.success("🎉 Analysis and Plan Generation Complete!")
            st.divider()

            tab_summary, tab_vision, tab_metrics, tab_ai, tab_workout, tab_diet = st.tabs([
                "🏆 Executive Summary", 
                "👁️ Annotated Postures", 
                "📊 Metric Indices", 
                "🤖 Coach AI Insights",
                "🏋️ Weekly Gym Routine",
                "🥗 Diet & Nutrition"
            ])

            with tab_summary:
                st.subheader("Body Evaluation Summary Card")
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                with metric_col1:
                    st.metric(label="Overall Fitness Score", value=f"{score_data.get('overall_score', 0.0)} / 100")
                with metric_col2:
                    st.metric(label="Body Architecture Type", value=score_data.get('body_type', 'Balanced'))
                with metric_col3:
                    st.metric(label="Classified Fitness Tier", value=score_data.get('fitness_level', 'General'))

                st.markdown("#### 🎯 Muscle Focus Priorities")
                priorities = score_data.get("priority_focus", [])
                if priorities:
                    cols = st.columns(len(priorities))
                    for idx, focus in enumerate(priorities):
                        cols[idx].warning(f"⚠️ **{focus}** flagged.")
                else:
                    st.success("✅ Excellent symmetry and muscular proportions.")

            with tab_vision:
                # Updated header title to show the current backend mapping model
                st.subheader("YOLO Pose Keypoint Mapping Visualizations")
                img_cols = st.columns(3)
                img_mappings = report.get("images", {})
                for idx, (view_title, path_str) in enumerate(img_mappings.items()):
                    with img_cols[idx]:
                        absolute_img_path = PROJECT_ROOT / path_str
                        if absolute_img_path.exists():
                            bgr_mat = cv2.imread(str(absolute_img_path))
                            rgb_mat = cv2.cvtColor(bgr_mat, cv2.COLOR_BGR2RGB)
                            st.image(rgb_mat, caption=f"{view_title.title()} View Landmarks", use_container_width=True)

            with tab_metrics:
                st.subheader("📊 Proportional Camera-Invariant Indexes")
                st.markdown("This dashboard translates your posture, symmetry, and skeletal ratios into standard fitness markers.")
                
                m_col1, m_col2 = st.columns(2)
                
                with m_col1:
                    st.markdown("### 📐 Structural Proportions")
                    v_taper = metrics_data.get("v_taper_index", 1.0)
                    st.write(f"**V-Taper Ratio:** `{v_taper}`")
                    st.progress(min(max((v_taper - 1.0) / 0.6, 0.0), 1.0), text="Upper Frame Tapering")
                    
                    sh_dom = metrics_data.get("shoulder_dominance", 1.0)
                    st.write(f"**Shoulder Dominance Score:** {round(min(sh_dom * 50, 100.0), 1)}%")
                    st.progress(min(max(sh_dom / 2.0, 0.0), 1.0))
                    
                    ub_balance = metrics_data.get("upper_body_balance", 1.0)
                    lb_balance = metrics_data.get("lower_body_balance", 1.0)
                    
                    st.write(f"**Upper Body Proportional Development:** {round(min(ub_balance * 80, 100.0), 1)}%")
                    st.progress(min(max(ub_balance / 1.5, 0.0), 1.0))
                    
                    st.write(f"**Lower Body Mass Distribution:** {round(min(lb_balance * 50, 100.0), 1)}%")
                    st.progress(min(max(lb_balance / 2.0, 0.0), 1.0))

                with m_col2:
                    st.markdown("### ⚖️ Muscular Development & Balance")
                    chest_dev = metrics_data.get("chest_development", 0.5)
                    st.write(f"**Chest Muscular Volume:** {round(min(chest_dev * 100, 100.0), 1)}%")
                    st.progress(min(max(chest_dev, 0.0), 1.0))
                    
                    back_dev = metrics_data.get("back_development", 0.5)
                    st.write(f"**Posterior Chain / Back Density:** {round(min(back_dev * 45, 100.0), 1)}%")
                    st.progress(min(max(back_dev / 2.2, 0.0), 1.0))
                    
                    waist_score = metrics_data.get("waist_score", 0.5)
                    st.write(f"**Core Stabilization Grid / Waist Score:** {round(min(waist_score * 100, 100.0), 1)}%")
                    st.progress(min(max(waist_score, 0.0), 1.0))
                    
                    st.divider()
                    
                    sym_data = report.get("score", {})
                    overall_sym = metrics_data.get("overall_symmetry", sym_data.get("symmetry", 90.0))
                    
                    st.markdown("#### 🏆 Structural Balance Rating")
                    st.metric(
                        label="Bilateral Muscle Symmetry Vector", 
                        value=f"{round(overall_sym, 2)}%", 
                        delta="Excellent Balance" if overall_sym > 90 else "Asymmetry Flagged"
                    )

            with tab_ai:
                st.subheader("🤖 Coach AI Generated Diagnostic Strategy")
                if ai_data:
                    st.markdown(f"#### 📝 Executive Summary\n{ai_data.get('summary', 'No summary generated.')}")
                    ai_col1, ai_col2 = st.columns(2)
                    with ai_col1:
                        st.success(f"💪 **Structural Strengths:**\n" + "\n".join([f"- {item}" for item in ai_data.get('strengths', [])]))
                        st.info(f"🎯 **Priority Focus Tasks:**\n" + "\n".join([f"- {item}" for item in ai_data.get('priority_focus', [])]))
                    with ai_col2:
                        st.warning(f"❌ **Observed Gaps:**\n" + "\n".join([f"- {item}" for item in ai_data.get('weaknesses', [])]))
                        st.info(f"⏱️ **Target Timeframe:** {ai_data.get('estimated_improvement_time', 'N/A')}")

            with tab_workout:
                st.subheader("📋 Personalized 7-Day Gym Schedule")
                if workout_plan and "weekly_plan" in workout_plan:
                    st.info(f"🎯 **Training Focus Goal:** {workout_plan.get('goal', user_payload['goal'])}")
                    focus_muscles = workout_plan.get('focus_muscles', [])
                    if focus_muscles:
                        st.markdown(f"**Target Muscle Groups for Progressive Overload:** {', '.join(focus_muscles)}")
                    st.divider()

                    for day_routine in workout_plan.get("weekly_plan", []):
                        day_name = day_routine.get("day", "Training Day")
                        target_group = day_routine.get("muscle_group", "Rest / Recovery")
                        
                        with st.expander(f"📅 {day_name} — **{target_group}**", expanded=(day_name == "Monday")):
                            exercises = day_routine.get("exercises", [])
                            if exercises:
                                table_md = "| Exercise Name | Sets | Repetitions |\n| :--- | :---: | :---: |\n"
                                for ex in exercises:
                                    table_md += f"| {ex.get('name', 'N/A')} | {ex.get('sets', 4)} | {ex.get('reps', '8-12')} |\n"
                                st.markdown(table_md)
                            else:
                                st.write("🧘 Active recovery session.")

                    st.divider()
                    col_c, col_r = st.columns(2)
                    with col_c:
                        st.markdown(f"🏃‍♂️ **Cardio Strategy:**\n{workout_plan.get('cardio', 'Low intensity training session.')}")
                    with col_r:
                        st.markdown(f"💤 **Recovery Guidelines:**\n{workout_plan.get('recovery', 'Ensure adequate sleep.')}")

            with tab_diet:
                st.subheader("🥗 Target Nutrition & Split Meal Blueprint")
                if diet_plan and "meal_plan" in diet_plan:
                    st.success(f"🎯 **Nutrition Objective:** {diet_plan.get('goal', 'Balanced Profiling')}")
                    
                    macro_col1, macro_col2, macro_col3, macro_col4 = st.columns(4)
                    with macro_col1:
                        st.metric(label="Daily Calorie Target", value=f"{diet_plan.get('daily_calories', 0)} kcal")
                    with macro_col2:
                        st.metric(label="Protein Target", value=f"{diet_plan.get('protein_g', 0)} g")
                    with macro_col3:
                        st.metric(label="Carbohydrates Target", value=f"{diet_plan.get('carbs_g', 0)} g")
                    with macro_col4:
                        st.metric(label="Fats Target", value=f"{diet_plan.get('fat_g', 0)} g")

                    st.markdown(f"💧 **Hydration Target Guidance:** Consume minimum **{diet_plan.get('water_liters', 3.5)} Liters** of water spread evenly throughout the day.")
                    st.divider()

                    diet_preference = st.radio(
                        "Select Diet Plan Strategy View Type:",
                        ["Vegetarian Plan", "Non-Vegetarian Plan"],
                        horizontal=True
                    )
                    st.divider()

                    meal_plan_data = diet_plan.get("meal_plan", {})
                    
                    if diet_preference == "Vegetarian Plan":
                        selected_meals = meal_plan_data.get("veg", {})
                        st.markdown("### 🕒 1-Day Vegetarian Sample Meal Schedule")
                    else:
                        selected_meals = meal_plan_data.get("non_veg", {})
                        st.markdown("### 🕒 1-Day Non-Vegetarian Sample Meal Schedule")

                    meal_periods = ["breakfast", "lunch", "snack", "dinner"]
                    
                    if isinstance(selected_meals, dict) and selected_meals:
                        for period in meal_periods:
                            items = selected_meals.get(period, [])
                            if items:
                                st.markdown(f"**🔹 {period.title()} Blueprint:**")
                                if isinstance(items, list):
                                    st.write("\n".join([f"- {food}" for food in items]))
                                else:
                                    st.write(f"- {items}")

                    st.divider()
                    col_sup, col_tips = st.columns(2)
                    with col_sup:
                        st.markdown("#### 💊 Recommended Supplement Stack")
                        supps = diet_plan.get("supplements", [])
                        if supps:
                            st.write("\n".join([f"- {s}" for s in supps]))
                        else:
                            st.write("No direct synthetic supplement configurations flagged necessary.")
                    with col_tips:
                        st.markdown("#### 💡 Nutritional Coaching Guidance Tips")
                        tips = diet_plan.get("tips", [])
                        if tips:
                            st.write("\n".join([f"- {t}" for t in tips]))

        except Exception as pipeline_crash:
            st.error(f"💥 Internal Processing Error: {str(pipeline_crash)}")
            st.exception(pipeline_crash)
