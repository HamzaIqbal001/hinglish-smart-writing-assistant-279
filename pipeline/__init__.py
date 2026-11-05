"""
Hinglish Smart Writing Assistant Pipeline.
Integrates:
1. Transliteration (AI4Bharat IndicXlit)
2. Phrasing Improvement (LLM / BharatGen / Qwen2.5 with linguistic fallback)
3. Translation (AI4Bharat IndicTrans2 200M distilled)
"""

from .transliterate import transliterate_text
from .improve import improve_phrasing
from .translate import translate_to_english

__all__ = ["transliterate_text", "improve_phrasing", "translate_to_english"]
