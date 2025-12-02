"""Internationalization (i18n) handler for multi-language support."""
import json
from pathlib import Path
from typing import Dict, Optional

class I18n:
    """Manages translations for multiple languages."""
    
    def __init__(self):
        self.translations: Dict[str, Dict[str, str]] = {}
        self.default_lang = "en"
        self._load_translations()
    
    def _load_translations(self) -> None:
        """Load all translation files from the translations directory."""
        trans_dir = Path(__file__).parent.parent / "translations"
        if not trans_dir.exists():
            return
        
        for lang_file in trans_dir.glob("*.json"):
            lang = lang_file.stem
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.translations[lang] = json.load(f)
            except Exception as e:
                print(f"Error loading {lang} translations: {e}")
    
    def get(self, key: str, lang: Optional[str] = None, **kwargs) -> str:
        """Get translated string with optional variable substitution.
        
        Args:
            key: Translation key
            lang: Language code (defaults to user's language or 'en')
            **kwargs: Variables for string formatting
        
        Returns:
            Translated string or key if translation not found
        """
        if lang is None:
            lang = self.default_lang
        
        if lang not in self.translations:
            lang = self.default_lang
        
        text = self.translations.get(lang, {}).get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except KeyError:
                return text
        return text
    
    def set_default_lang(self, lang: str) -> None:
        """Set the default language."""
        if lang in self.translations or lang in ["en", "pt", "es"]:
            self.default_lang = lang

# Global instance
i18n = I18n()
