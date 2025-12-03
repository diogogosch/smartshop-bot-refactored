import logging
from openai import AsyncOpenAI
from app.config.settings import settings

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY:
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            logger.warning("OPENAI_API_KEY not found. AI suggestions will be disabled.")

    async def get_suggestions(self, current_items: list[str]) -> list[str]:
        if not self.client:
            return ["(AI Disabled) Apples", "(AI Disabled) Bread", "(AI Disabled) Eggs"]

        try:
            prompt = f"Based on this shopping list: {', '.join(current_items)}, suggest 5 complementary items. Return only the item names separated by commas."
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=60
            )
            content = response.choices[0].message.content
            # Clean up the response
            suggestions = [item.strip().replace('.', '') for item in content.split(',') if item.strip()]
            return suggestions[:5]
        except Exception as e:
            logger.error(f"AI Error: {e}")
            return ["Error generating suggestions"]

ai_service = AIService()
