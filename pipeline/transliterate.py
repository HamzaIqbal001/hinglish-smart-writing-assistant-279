"""
Transliteration pipeline module using AI4Bharat IndicXlit.
Converts Roman script Hinglish text into Devanagari Hindi script.
"""

import time
import torch

# Fix for PyTorch >= 2.6 where weights_only defaults to True, breaking fairseq models
_orig_load = torch.load
def _safe_load(*args, **kwargs):
    if "weights_only" not in kwargs:
        kwargs["weights_only"] = False
    return _orig_load(*args, **kwargs)
torch.load = _safe_load

from ai4bharat.transliteration import XlitEngine

_ENGINE = None

def get_translit_engine():
    global _ENGINE
    if _ENGINE is None:
        # beam_width=4 provides high accuracy while keeping inference fast
        _ENGINE = XlitEngine(src_script_type="roman", beam_width=4, rescore=False)
    return _ENGINE

def transliterate_text(text: str) -> dict:
    """
    Transliterate Roman-script Hinglish text to Devanagari script.
    
    Returns:
        dict: {
            "output": str (Devanagari text),
            "latency": float (seconds)
        }
    """
    if not text or not text.strip():
        return {"output": "", "latency": 0.0}
    
    engine = get_translit_engine()
    start_time = time.perf_counter()
    devanagari_text = engine.translit_sentence(text.strip(), "hi")
    elapsed = time.perf_counter() - start_time
    
    return {
        "output": devanagari_text,
        "latency": elapsed
    }
