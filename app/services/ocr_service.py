import logging
from typing import List, Dict, Any
from app.config.settings import settings

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self):
        self.api_key = settings.google_vision_api_key
    
    async def process_receipt(self, image_data: bytes) -> Dict[str, Any]:
        try:
            if not self.api_key:
                return self._dummy_receipt()
            
            from google.cloud import vision
            client = vision.ImageAnnotatorClient()
            image = vision.Image(content=image_data)
            response = client.document_text_detection(image=image)
            
            text = response.full_text_annotation.text
            items = self._parse_items(text)
            
            return {"success": True, "items": items, "text": text}
        except Exception as e:
            logger.error(f"OCR error: {e}")
            return {"success": False, "items": []}
    
    def _parse_items(self, text: str) -> List[Dict]:
        items = []
        for line in text.split('\n'):
            line = line.strip()
            if line and any(c.isdigit() for c in line):
                parts = line.rsplit(' ', 1)
                if len(parts) == 2:
                    try:
                        price = float(parts[1].replace('$', '').replace('R$', ''))
                        items.append({"name": parts[0], "price": price})
                    except ValueError:
                        pass
        return items
    
    def _dummy_receipt(self) -> Dict:
        return {
            "success": True,
            "items": [{"name": "Milk", "price": 5.50}],
            "text": "Sample receipt"
        }

ocr_service = OCRService()
