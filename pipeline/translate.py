"""
Translation pipeline module using AI4Bharat IndicTrans2.
Translates Hindi Devanagari text to English.
Model: ai4bharat/indictrans2-indic-en-dist-200M (using 200M distilled checkpoint with IndicTransToolkit).
"""

import os
import time
import torch
from dotenv import load_dotenv

load_dotenv()

_TOKENIZER = None
_MODEL = None
_PROCESSOR = None
_DEVICE = None

def get_translation_model():
    global _TOKENIZER, _MODEL, _PROCESSOR, _DEVICE
    if _MODEL is None:
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        from IndicTransToolkit import IndicProcessor

        _DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        hf_token = os.getenv("HF_TOKEN", None)

        # We first check if the official gated checkpoint is accessible,
        # otherwise use the verified open mirror benfranklinms/indictrans2-indic-en-dist-200M
        candidate_models = [
            "benfranklinms/indictrans2-indic-en-dist-200M",
            "ai4bharat/indictrans2-indic-en-dist-200M"
        ]
        if hf_token:
            candidate_models.reverse()

        last_err = None
        for model_id in candidate_models:
            try:
                _TOKENIZER = AutoTokenizer.from_pretrained(
                    model_id,
                    trust_remote_code=True,
                    token=hf_token
                )
                dtype = torch.float16 if _DEVICE == "cuda" else torch.float32
                _MODEL = AutoModelForSeq2SeqLM.from_pretrained(
                    model_id,
                    trust_remote_code=True,
                    torch_dtype=dtype,
                    token=hf_token
                ).to(_DEVICE)
                _MODEL.eval()
                break
            except Exception as e:
                last_err = e
                continue
        
        if _MODEL is None:
            raise RuntimeError(f"Failed to load IndicTrans2 model: {last_err}")
            
        _PROCESSOR = IndicProcessor(inference=True)

    return _TOKENIZER, _MODEL, _PROCESSOR, _DEVICE

def translate_to_english(text: str) -> dict:
    """
    Translate Hindi text to English using IndicTrans2.
    
    Returns:
        dict: {
            "output": str (English translation),
            "latency": float (seconds)
        }
    """
    if not text or not text.strip():
        return {"output": "", "latency": 0.0}

    tokenizer, model, processor, device = get_translation_model()

    start_time = time.perf_counter()
    sentences = [text.strip()]
    batch = processor.preprocess_batch(sentences, src_lang="hin_Deva", tgt_lang="eng_Latn")
    inputs = tokenizer(batch, padding="longest", truncation=True, max_length=256, return_tensors="pt").to(device)

    with torch.inference_mode():
        outputs = model.generate(**inputs, num_beams=4, max_new_tokens=256)

    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    translations = processor.postprocess_batch(decoded, lang="eng_Latn")
    elapsed = time.perf_counter() - start_time

    return {
        "output": translations[0] if translations else "",
        "latency": elapsed
    }
