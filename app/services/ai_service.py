import logging
from typing import List
from app.config.settings import settings

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.api_key = settings.openai_api_key
    
    async def get_suggestions(self, history: List[str]) -> List[str]:
        try:
            if not self.api_key:
                return self._defaults()
            
            import openai
            openai.api_key = self.api_key
            prompt = f"Suggest 5 items based on: {', '.join(history[:10])}"
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip().split('\n')
        except Exception as e:
            logger.error(f"AI error: {e}")
            return self._defaults()
    
    def _defaults(self) -> List[str]:
        return ["Milk", "Bread", "Eggs", "Butter", "Cheese", "Tomatoes", "Lettuce", "Chicken"]

ai_service = AIService()
