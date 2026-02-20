🏥 AIIMS – AI-Powered Medical Report Simplification System

An AI-driven web application designed to help patients understand their medical reports in simple, structured language.

The system processes uploaded medical reports using clinical NLP models and generates patient-friendly explanations along with risk assessment.

🚀 Features
📄 Medical Report Upload & Analysis

Upload PDF or image medical reports

Text extraction using OCR / PDF parser

Clinical entity recognition

Risk level classification (Low / Moderate / High)

Highlight abnormal findings

Structured medical explanation

Medical disclaimer integration

🤖 AI Medical Chatbot

Backend-integrated chatbot model

Real-time responses

Clean conversational UI

Educational medical explanations

Safe-response design (no prescriptions)

🏗️ Tech Stack
Frontend

HTML

Tailwind CSS

JavaScript

Fetch API

Backend

FastAPI

Python

medspaCy

ClinicalBERT

BioBERT

pytesseract (OCR)

PyMuPDF / pdfplumber

🧠 System Architecture
User Upload
      ↓
FastAPI Backend
      ↓
Text Extraction (PDF / OCR)
      ↓
medspaCy → ClinicalBERT → BioBERT
      ↓
Risk Classification & Explanation
      ↓
Frontend Display
🧠 Model Usage

This system integrates three specialized clinical AI models to process and analyze medical reports.

1️⃣ medspaCy – Clinical Entity Extraction

medspaCy is used for clinical Natural Language Processing (NLP) on medical reports.

It is responsible for:

Extracting laboratory parameters (e.g., Hemoglobin, WBC, Creatinine)

Identifying symptoms and diagnoses

Detecting negations (e.g., “no infection”)

Understanding clinical context within the report

This allows the system to convert unstructured medical text into structured clinical entities.

2️⃣ ClinicalBERT – Risk Classification & Clinical Understanding

ClinicalBERT is a transformer-based language model trained on clinical text.

It is used for:

Understanding the overall medical context of the report

Classifying risk levels (Low / Moderate / High)

Estimating confidence scores for predictions

Interpreting clinical severity patterns

This model helps determine the overall health risk based on extracted findings.

3️⃣ BioBERT – Biomedical Entity Recognition

BioBERT is a domain-specific BERT model trained on biomedical literature.

It is responsible for:

Identifying biomedical terms and disease associations

Linking lab parameters with possible medical conditions

Extracting medically relevant terminology

Enhancing semantic understanding of biomedical content

This improves the accuracy of clinical tagging and medical insight generation.

🔄 Combined Workflow

The models work together in a structured pipeline:

Text is extracted from the uploaded medical report.

medspaCy extracts structured clinical entities.

ClinicalBERT analyzes severity and predicts risk level.

BioBERT enriches biomedical understanding.

The system combines outputs to generate a structured explanation for the patient.

This multi-model architecture ensures medically relevant, context-aware, and structured output.

📂 Project Structure
aiims-medical-report-system/
│
├── frontend/
│   ├── index.html
│   ├── upload.html
│   ├── dashboard.html
│   ├── chatbot.html
│   ├── css/
│   ├── js/
│
├── backend/
│   ├── main.py
│   ├── agents/
│   ├── models/
│
└── README.md
⚙️ Installation (Backend)

Install dependencies:

pip install -r requirements.txt

Run backend:

uvicorn main:app --reload

Open API documentation:

http://127.0.0.1:8000/docs
🌐 Deployment

Frontend:

Vercel (Static Deployment)

Backend:

FastAPI (Local Network / Cloud Server)

⚠️ Disclaimer

This system provides AI-generated summaries and clinical insights for educational purposes only.
It does not replace professional medical consultation, diagnosis, or treatment.

Always consult a qualified healthcare provider.



🌍 Live Deployment

Frontend is deployed on Vercel:

🔗 https://aiims-medical-report-system-one.vercel.app/

📊 PPT Link:
https://drive.google.com/drive/folders/1V72_NsAXSpS0TDq6v6JUcqaqDZV-f4l1?usp=drive_link
