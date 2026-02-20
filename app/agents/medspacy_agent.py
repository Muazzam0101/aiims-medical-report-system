import medspacy
from medspacy.visualization import visualize_ent
from app.config import MEDSPACY_MODEL_PATH
import spacy

class MedspacyAgent:
    def __init__(self):
        # medspacy.load() can take a path to a custom model or just use the default
        # Since the models are in /models/medspacy-master, we load from there
        try:
            # Medspacy usually wraps a spacy model
            self.nlp = medspacy.load(str(MEDSPACY_MODEL_PATH))
        except Exception as e:
            print(f"Warning: Could not load medspaCy model from {MEDSPACY_MODEL_PATH}. Falling back to default.")
            self.nlp = medspacy.load()

    async def extract_entities(self, text: str):
        doc = self.nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start_char": ent.start_char,
                "end_char": ent.end_char,
                "is_negated": ent._.is_negated if hasattr(ent._, "is_negated") else False,
                "is_uncertain": ent._.is_uncertain if hasattr(ent._, "is_uncertain") else False,
                "is_historical": ent._.is_historical if hasattr(ent._, "is_historical") else False,
            })
        return entities
