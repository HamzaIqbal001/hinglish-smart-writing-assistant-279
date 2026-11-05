"""
Hinglish Smart Writing Assistant
University Mini Project (CS3235 - AI4Bharat & BharatGen Mini Project #4)
Gradio Web Application
"""

import os
import gradio as gr
from pipeline import transliterate_text, improve_phrasing, translate_to_english

EXAMPLES = [
    ["mujhe kal subah meeting ke liye jaana hai", True, True],
    ["project ki deadline agle hafte tak extend ho gayi hai", True, True],
    ["kya yahan free WiFi connection available hai?", True, True],
    ["tension mat lo sab jugaad ho jaayega", True, True],
    ["kya aap bata sakte hain ki agla metro kab aayega?", True, True],
]

def process_hinglish(text: str, improve_flag: bool, translate_flag: bool):
    """
    Executes the 3-stage Hinglish processing pipeline:
    1. Transliteration (Roman -> Devanagari via AI4Bharat IndicXlit)
    2. Phrasing improvement (Devanagari -> Clean Hindi via LLM/Linguistic engine)
    3. Translation (Hindi -> English via AI4Bharat IndicTrans2)
    """
    if not text or not text.strip():
        return "", "", "", "Please enter some Hinglish text to begin."

    # Stage 1: Transliteration
    t_res = transliterate_text(text)
    native_script = t_res["output"]
    t_latency = t_res["latency"]

    # Stage 2: Phrasing Improvement (Optional)
    improved_script = ""
    i_latency = 0.0
    i_backend = ""
    if improve_flag:
        i_res = improve_phrasing(native_script)
        improved_script = i_res["output"]
        i_latency = i_res["latency"]
        i_backend = i_res.get("backend", "default")
    else:
        improved_script = "(Phrasing improvement disabled)"

    # Stage 3: Translation to English (Optional)
    english_translation = ""
    tr_latency = 0.0
    if translate_flag:
        # Translate improved Hindi if available, otherwise native script
        source_for_trans = improved_script if (improve_flag and improved_script) else native_script
        tr_res = translate_to_english(source_for_trans)
        english_translation = tr_res["output"]
        tr_latency = tr_res["latency"]
    else:
        english_translation = "(English translation disabled)"

    # Summary timing
    status_msg = (
        f"⚡ Execution Metrics: "
        f"Transliteration: {t_latency*1000:.1f}ms | "
        f"Improvement: {i_latency*1000:.1f}ms ({i_backend or 'N/A'}) | "
        f"Translation: {tr_latency*1000:.1f}ms"
    )

    return native_script, improved_script, english_translation, status_msg

custom_css = """
.container { max-width: 960px; margin: auto; padding: 20px; }
.title-box { text-align: center; margin-bottom: 20px; }
.output-box textarea { font-size: 1.15rem !important; font-family: 'Noto Sans Devanagari', sans-serif, system-ui; }
.badge { display: inline-block; background-color: #2563eb; color: white; padding: 3px 10px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
"""

with gr.Blocks(title="Hinglish Smart Writing Assistant") as demo:
    with gr.Column(elem_classes="container"):
        with gr.Row(elem_classes="title-box"):
            gr.Markdown(
                """
                # 🇮🇳 Hinglish Smart Writing Assistant
                ### CS3235 Mini Project #4 • AI4Bharat & BharatGen
                Convert casual Roman-script Hinglish into **Devanagari**, polish it into **Natural Hindi**, and optionally translate to **English**.
                """
            )

        with gr.Row():
            with gr.Column(scale=5):
                input_box = gr.Textbox(
                    label="Input: Roman-script Hinglish Text",
                    placeholder="Type Hinglish here (e.g., mujhe kal subah meeting ke liye jaana hai)...",
                    lines=3
                )
                with gr.Row():
                    toggle_improve = gr.Checkbox(label="Improve Phrasing", value=True)
                    toggle_translate = gr.Checkbox(label="Translate to English", value=True)
                with gr.Row():
                    btn_submit = gr.Button("🚀 Process Text", variant="primary", scale=2)
                    btn_clear = gr.Button("🧹 Clear", scale=1)

            with gr.Column(scale=5):
                status_bar = gr.Markdown("Ready to process input.")
                out_native = gr.Textbox(
                    label="1. Native Script (Devanagari Transliteration)",
                    lines=2,
                    interactive=False,
                    elem_classes="output-box"
                )
                out_improved = gr.Textbox(
                    label="2. Improved Hindi (Clean, Polished Phrasing)",
                    lines=2,
                    interactive=False,
                    elem_classes="output-box"
                )
                out_english = gr.Textbox(
                    label="3. English Translation",
                    lines=2,
                    interactive=False,
                    elem_classes="output-box"
                )

        gr.Markdown("### 💡 Clickable Examples")
        gr.Examples(
            examples=EXAMPLES,
            inputs=[input_box, toggle_improve, toggle_translate],
            outputs=[out_native, out_improved, out_english, status_bar],
            fn=process_hinglish,
            cache_examples=False
        )

        btn_submit.click(
            fn=process_hinglish,
            inputs=[input_box, toggle_improve, toggle_translate],
            outputs=[out_native, out_improved, out_english, status_bar]
        )

        def clear_fields():
            return "", "", "", "", "Ready to process input."

        btn_clear.click(
            fn=clear_fields,
            inputs=[],
            outputs=[input_box, out_native, out_improved, out_english, status_bar]
        )

        gr.Markdown(
            """
            ---
            **Pipeline Architecture**:
            - **Transliteration**: AI4Bharat IndicXlit (`ai4bharat-transliteration`, lang `hi`)
            - **Phrasing Improvement**: BharatGen Param1 / Qwen2.5-1.5B-Instruct & linguistic post-processor
            - **Translation**: AI4Bharat IndicTrans2 (`ai4bharat/indictrans2-indic-en-dist-200M`)
            """
        )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False, theme=gr.themes.Soft(), css=custom_css)
