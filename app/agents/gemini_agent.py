import google.generativeai as genai
from loguru import logger
import json
from typing import Dict, Any

class GeminiAgent:
    def __init__(self, api_key: str):
        if not api_key or api_key == "AIzaSyBJPyoshFpql_B242f_FDxIqnrRT_qfgmQ":
            logger.warning("Gemini API Key is missing or invalid. Agent will not function.")
            self.model = None
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            logger.info("Gemini Agent initialized successfully.")

    async def summarize_text(self, text: str) -> Dict[str, Any]:
        """Summarizes medical report text using Gemini."""
        if not self.model:
            raise ValueError("Gemini API key not configured.")

        logger.info("Summarizing medical report with Gemini...")
        
        prompt = f"""
        Summarize the following medical report in simple patient-friendly language. 
        Highlight abnormal findings and provide general educational explanation only. 
        Do not provide medical prescriptions.

        Report Text:
        {text}

        Your response must be a valid JSON object with the following fields:
        - summary: A detailed summary of the report.
        - disclaimer: "This summary is for educational purposes only and does not replace professional medical consultation."

        Respond ONLY with the JSON object.
        """

        try:
            response = await self.model.generate_content_async(prompt)
            
            # Clean up the response text to ensure it's valid JSON
            resp_text = response.text.strip()
            if resp_text.startswith("```json"):
                resp_text = resp_text[7:-3].strip()
            elif resp_text.startswith("```"):
                resp_text = resp_text[3:-3].strip()
            
            try:
                data = json.loads(resp_text)
            except json.JSONDecodeError:
                import re
                json_match = re.search(r'\{.*\}', resp_text, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group())
                else:
                    raise ValueError("Could not parse JSON from Gemini response.")
                    
            logger.info("Gemini summarization successful.")
            return data
            
        except Exception as e:
            logger.error(f"Gemini Summarization Failed: {str(e)}")
            raise e


