from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from app.config import BIOBERT_PATH
import torch

class BioBertAgent:
    def __init__(self):
        try:
            # Try loading from local path first
            model_path = str(BIOBERT_PATH)
            # Check if local config exists to ensure it's a valid model folder
            if not (BIOBERT_PATH / "config.json").exists():
                from app.config import HF_BIOBERT_ID
                model_path = HF_BIOBERT_ID
                print(f"Local BioBERT files missing at {BIOBERT_PATH}. Falling back to {HF_BIOBERT_ID}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForTokenClassification.from_pretrained(model_path)
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            self.nlp = pipeline("ner", model=self.model, tokenizer=self.tokenizer, device=0 if torch.cuda.is_available() else -1)
        except Exception as e:
            print(f"Error loading BioBERT model: {str(e)}")
            raise e

    async def extract_biomedical_entities(self, text: str):
        # BioBERT for NER
        results = self.nlp(text)
        
        # Clean up results for JSON serialization
        entities = []
        for res in results:
            entities.append({
                "entity": res["entity"],
                "score": float(res["score"]),
                "word": res["word"],
                "start": res["start"],
                "end": res["end"]
            })
            
        return entities
