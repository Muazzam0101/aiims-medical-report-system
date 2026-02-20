import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from app.config import TESSERACT_CMD
import os

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

class TextExtractionAgent:
    def __init__(self):
        pass

    async def extract_text(self, file_path: str) -> str:
        extension = os.path.splitext(file_path)[1].lower()
        
        if extension == ".pdf":
            return await self._extract_from_pdf(file_path)
        elif extension in [".jpg", ".jpeg", ".png"]:
            return await self._extract_from_image(file_path)
        else:
            raise ValueError(f"Unsupported file type: {extension}")

    async def _extract_from_pdf(self, file_path: str) -> str:
        text = ""
        try:
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text()
            
            # If no text found, try OCR on the PDF pages
            if not text.strip():
                text = await self._ocr_pdf(doc)
            
            doc.close()
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
        
        return self._clean_text(text)

    async def _extract_from_image(self, file_path: str) -> str:
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
        except Exception as e:
            raise Exception(f"Failed to extract text from image: {str(e)}")
        
        return self._clean_text(text)

    async def _ocr_pdf(self, doc) -> str:
        text = ""
        for page in doc:
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text += pytesseract.image_to_string(img)
        return text

    def _clean_text(self, text: str) -> str:
        # Basic cleaning: remove extra whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)
