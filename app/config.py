import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Model Paths
MODELS_DIR = BASE_DIR / "models"
MEDSPACY_MODEL_PATH = MODELS_DIR / "medspacy-master"
CLINICAL_BERT_PATH = MODELS_DIR / "clinicalBERT-master"
BIOBERT_PATH = MODELS_DIR / "biobert-master"

# Hugging Face Model Fallbacks (Used if local files are missing)
HF_CLINICAL_BERT_ID = "emilyalsentzer/Bio_ClinicalBERT"
HF_BIOBERT_ID = "dmis-lab/biobert-v1.1"
HF_MEDSPACY_MODEL = "en_core_sci_sm" # Scientific spacy model

# Application Settings
UPLOAD_DIR = BASE_DIR / "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# API Settings
HOST = "0.0.0.0"
PORT = 8000

# OCR Settings
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe" # Windows default

# Gemini AI Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAPFo7GNYEQKh8_pml_q4UryLG8dAnribM")

# Create directories if they don't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
