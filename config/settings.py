from pathlib import Path
from dotenv import load_dotenv
import os

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Project Root
# -----------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# Folder Paths
# -----------------------------
UPLOADS_DIR = ROOT_DIR / "uploads"

FRONT_UPLOAD = UPLOADS_DIR / "front"
SIDE_UPLOAD = UPLOADS_DIR / "side"
BACK_UPLOAD = UPLOADS_DIR / "back"

OUTPUTS_DIR = ROOT_DIR / "outputs"

ANNOTATED_DIR = OUTPUTS_DIR / "annotated"
JSON_DIR = OUTPUTS_DIR / "json"
REPORT_DIR = OUTPUTS_DIR / "reports"

DATABASE_DIR = ROOT_DIR / "database"

# -----------------------------
# Gemini API
# -----------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# -----------------------------
# Image Settings
# -----------------------------
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]

# -----------------------------
# Create Missing Directories
# -----------------------------
for folder in [
    FRONT_UPLOAD,
    SIDE_UPLOAD,
    BACK_UPLOAD,
    ANNOTATED_DIR,
    JSON_DIR,
    REPORT_DIR,
]:
    folder.mkdir(parents=True, exist_ok=True)