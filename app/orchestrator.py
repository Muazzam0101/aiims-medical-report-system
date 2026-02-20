import time
from loguru import logger
from app.agents.gemini_agent import GeminiAgent
from app.agents.text_extraction_agent import TextExtractionAgent
from app.config import GEMINI_API_KEY

class Orchestrator:
    def __init__(self):
        logger.info("Initializing Orchestrator with Gemini and Extraction support...")
        self.gemini_agent = GeminiAgent(GEMINI_API_KEY)
        self.text_agent = TextExtractionAgent()
        logger.info("Orchestrator ready.")

    async def analyze_report(self, file_path: str):
        start_time = time.time()
        logger.info(f"Starting analysis for file: {file_path}")
        
        try:
            # 1. Extract Text
            logger.info("Step 1: Extracting text from file...")
            extracted_text = await self.text_agent.extract_text(file_path)
            
            if not extracted_text.strip():
                logger.warning(f"No text extracted from file: {file_path}")
                return {
                    "summary": "Could not extract any readable text from the provided report. Please ensure the file is clear and high-resolution.",
                    "disclaimer": "Analysis failed due to poor text quality.",
                    "meta": {"processing_time": time.time() - start_time, "file_processed": file_path, "engine": "Extraction Failure"}
                }

            # 2. Summarize with Gemini
            if self.gemini_agent.model:
                logger.info("Step 2: Summarizing text with Gemini...")
                results = await self.gemini_agent.summarize_text(extracted_text)
                
                processing_time = time.time() - start_time
                results["meta"] = {
                    "processing_time": processing_time,
                    "file_processed": file_path,
                    "engine": "Gemini 2.0 Flash"
                }
                return results
            else:
                logger.error("Gemini model is not initialized.")
                return {
                    "summary": "Gemini AI is not configured. Please add a valid API key to config.py.",
                    "disclaimer": "Analysis unavailable.",
                    "meta": {"processing_time": time.time() - start_time, "file_processed": file_path, "engine": "None"}
                }
            
        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}")
            raise e

