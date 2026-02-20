from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from app.config import CLINICAL_BERT_PATH

class ClinicalBertAgent:
    def __init__(self):
        try:
            # Try loading from local path first
            model_path = str(CLINICAL_BERT_PATH)
            # Check if local config exists to ensure it's a valid model folder
            if not (CLINICAL_BERT_PATH / "config.json").exists():
                from app.config import HF_CLINICAL_BERT_ID
                model_path = HF_CLINICAL_BERT_ID
                print(f"Local ClinicalBERT files missing at {CLINICAL_BERT_PATH}. Falling back to {HF_CLINICAL_BERT_ID}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            self.model.eval()
        except Exception as e:
            print(f"Error loading ClinicalBERT model: {str(e)}")
            raise e

    async def classify_risk(self, text: str):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=1)
            confidence, label_idx = torch.max(probabilities, dim=1)
            
        # Mapping labels (assuming a standard risk classification schema or custom trained)
        # For demonstration, we'll use Low, Moderate, High
        labels = ["Low", "Moderate", "High"]
        risk_level = labels[label_idx.item()] if label_idx.item() < len(labels) else "Unknown"
        
        return {
            "risk_level": risk_level,
            "confidence_score": float(confidence.item())
        }
