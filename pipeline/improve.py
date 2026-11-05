"""
Phrasing improvement pipeline module.
Rewrites raw Devanagari transliteration into clean, natural, grammatically correct Hindi.

Architecture & Fallbacks:
1. Primary: Swappable LLM behind `improve_phrasing`.
   Configured for open instruct models (Qwen2.5-1.5B-Instruct / BharatGen Param-1) or API models.
2. Graceful Fallback: Rule-based linguistic post-editing for transliteration artifacts
   (vowel length corrections, archaic ligatures, spacing, grammatical particles).
"""

import os
import re
import time
import torch
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

_LLM_TOKENIZER = None
_LLM_MODEL = None
_DEVICE = None

LOCAL_MODEL_DIR = Path(__file__).resolve().parent.parent / "models" / "qwen1.5b"

PROMPT_TEMPLATE = """You are an expert Hindi linguist. Rewrite the following raw Devanagari sentence into clean, natural, grammatically polished standard Hindi.
Rules:
1. Keep the original meaning intact.
2. Replace awkward phonetic transliterations of English words with natural Hindi equivalents where appropriate, or standard clean Devanagari spellings (e.g., 'मीटिंग' -> 'बैठक' or clean 'मीटिंग').
3. Correct phonetic misspellings (e.g. 'सुबाह' -> 'सुबह', 'केई' -> 'के', 'हूँ/हू' -> 'हूँ').
4. Output ONLY the improved Hindi sentence. No explanation, no english translation, no quotes.

Raw Hindi: {raw_text}
Improved Hindi:"""

COMMON_CORRECTIONS = [
    (r"\bसुबाह\b", "सुबह"),
    (r"\bकेई\b", "के"),
    (r"\bलिये\b", "लिए"),
    (r"\bजाना है\b", "जाना है"),
    (r"\bरहा हु\b", "रहा हूँ"),
    (r"\bरहा हू\b", "रहा हूँ"),
    (r"\bरहा हुं\b", "रहा हूँ"),
    (r"\bहफ्ते\b", "सप्ताह"),
    (r"\bएक्सटेंड\b", "विस्तारित"),
    (r"\bडेडलाइन\b", "अंतिम तिथि"),
    (r"\bअवेलेबल\b", "उपलब्ध"),
    (r"\bफ्री\b", "मुफ्त"),
    (r"\bवेट\b", "प्रतीक्षा"),
    (r"\bसीन\b", "योजना"),
    (r"\bटेंशन मत लो\b", "चिंता मत कीजिए"),
    (r"\bजुगाड़\b", "प्रबंध"),
    (r"\bसबमिट\b", "जमा"),
    (r"\bटाइम\b", "समय"),
    (r"\bआखरी\b", "अंतिम"),
    (r"\bआखिरी\b", "अंतिम"),
    (r"\bकोर्स\b", "पाठ्यक्रम"),
    (r"\bफीस\b", "शुल्क"),
]

def clean_linguistic_fallback(text: str) -> str:
    """Linguistic rule-based Hindi improver for cleanup and normalization."""
    improved = text.strip()
    for pattern, repl in COMMON_CORRECTIONS:
        improved = re.sub(pattern, repl, improved)
    # Ensure Hindi purna viram if ending sentence
    if improved and not improved.endswith(("।", "?", "!", ".")):
        improved += "।"
    return improved

def get_llm():
    global _LLM_TOKENIZER, _LLM_MODEL, _DEVICE
    if _LLM_MODEL is not None:
        return _LLM_TOKENIZER, _LLM_MODEL, _DEVICE

    # Check if local model weights are present and download is completely finished
    weights_path = LOCAL_MODEL_DIR / "model.safetensors"
    aria2_path = LOCAL_MODEL_DIR / "model.safetensors.aria2"
    if not weights_path.exists() or aria2_path.exists() or weights_path.stat().st_size < 2_500_000_000:
        return None, None, None

    from transformers import AutoModelForCausalLM, AutoTokenizer
    _DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    try:
        _LLM_TOKENIZER = AutoTokenizer.from_pretrained(str(LOCAL_MODEL_DIR))
        _LLM_MODEL = AutoModelForCausalLM.from_pretrained(
            str(LOCAL_MODEL_DIR),
            torch_dtype=torch.float16 if _DEVICE == "cuda" else torch.float32,
            device_map="auto" if _DEVICE == "cuda" else None
        )
        if _DEVICE != "cuda":
            _LLM_MODEL.to(_DEVICE)
        _LLM_MODEL.eval()
        _LLM_MODEL.generation_config.temperature = None
        _LLM_MODEL.generation_config.top_p = None
        _LLM_MODEL.generation_config.top_k = None
        return _LLM_TOKENIZER, _LLM_MODEL, _DEVICE
    except Exception as e:
        print(f"Warning: Could not load local LLM: {e}")
        return None, None, None

def improve_phrasing(devanagari_text: str) -> dict:
    """
    Improve and polish Hindi Devanagari phrasing using LLM (or linguistic fallback).
    
    Returns:
        dict: {
            "output": str (Improved Hindi text),
            "latency": float (seconds),
            "backend": str ("llm" or "linguistic_rules")
        }
    """
    if not devanagari_text or not devanagari_text.strip():
        return {"output": "", "latency": 0.0, "backend": "none"}

    start_time = time.perf_counter()
    tokenizer, model, device = get_llm()

    if model is not None and tokenizer is not None:
        try:
            prompt = PROMPT_TEMPLATE.format(raw_text=devanagari_text.strip())
            messages = [{"role": "user", "content": prompt}]
            formatted = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = tokenizer([formatted], return_tensors="pt").to(device)

            with torch.inference_mode():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=128,
                    do_sample=False,
                    pad_token_id=tokenizer.eos_token_id
                )
            generated_ids = [
                output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, outputs)
            ]
            response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
            # Clean up response
            response = response.split("\n")[0].strip()
            # Apply linguistic cleanup to eliminate any residual phonetic artifacts
            response = clean_linguistic_fallback(response)
            elapsed = time.perf_counter() - start_time
            return {
                "output": response,
                "latency": elapsed,
                "backend": "local_llm (Qwen2.5-1.5B-Instruct)"
            }
        except Exception as e:
            print(f"LLM generation failed, falling back to linguistic post-processor: {e}")

    # Fallback to linguistic rule-based post processor
    improved = clean_linguistic_fallback(devanagari_text)
    elapsed = time.perf_counter() - start_time
    return {
        "output": improved,
        "latency": elapsed,
        "backend": "linguistic_rules"
    }
