"""
Generate 05_eval_results.png from eval/metrics.json using matplotlib.
Creates a professional metrics dashboard with summary cards and comparison bar charts.
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR = Path(__file__).resolve().parent.parent
METRICS_JSON = BASE_DIR / "eval" / "metrics.json"
OUTPUT_PNG = BASE_DIR / "docs" / "screenshots" / "05_eval_results.png"

def generate_chart():
    OUTPUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    with open(METRICS_JSON, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    fig = plt.figure(figsize=(14, 8), dpi=200, facecolor="#0f172a")
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.2], hspace=0.35, wspace=0.25)

    # Title
    fig.suptitle("Hinglish Smart Writing Assistant • Benchmark Evaluation Dashboard",
                 fontsize=18, fontweight="bold", color="#f8fafc", y=0.96)

    # Subplot 1: Metric KPI cards
    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_facecolor("#1e293b")
    ax1.axis("off")

    cards = [
        {"title": "Translit Top-1 Acc", "val": f"{metrics['transliteration_exact_match_acc']*100:.1f}%", "sub": "Exact word match", "color": "#38bdf8"},
        {"title": "Transliteration CER", "val": f"{metrics['transliteration_cer']*100:.2f}%", "sub": "Character error rate", "color": "#fb7185"},
        {"title": "End-to-End Deva CER", "val": f"{metrics['e2e_devanagari_cer']*100:.2f}%", "sub": "Sentence phonetics", "color": "#34d399"},
        {"title": "Translation BLEU", "val": f"{metrics['e2e_translation_bleu']:.1f}", "sub": "SacreBLEU vs Ref", "color": "#a78bfa"},
        {"title": "Translation chrF", "val": f"{metrics['e2e_translation_chrf']:.1f}", "sub": "Character n-gram score", "color": "#facc15"},
    ]

    for idx, card in enumerate(cards):
        x = 0.02 + idx * 0.198
        rect = patches.FancyBboxPatch((x, 0.1), 0.175, 0.8, boxstyle="round,pad=0.03",
                                      facecolor="#0f172a", edgecolor=card["color"], linewidth=1.5,
                                      transform=ax1.transAxes)
        ax1.add_patch(rect)
        ax1.text(x + 0.087, 0.68, card["title"], ha="center", va="center",
                 fontsize=10, fontweight="bold", color="#94a3b8", transform=ax1.transAxes)
        ax1.text(x + 0.087, 0.42, card["val"], ha="center", va="center",
                 fontsize=20, fontweight="black", color=card["color"], transform=ax1.transAxes)
        ax1.text(x + 0.087, 0.22, card["sub"], ha="center", va="center",
                 fontsize=8, color="#64748b", transform=ax1.transAxes)

    # Subplot 2: Quality Metrics Bar Chart
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_facecolor("#1e293b")
    labels = ["Translit Acc", "Deva 1-CER", "Trans chrF", "Trans BLEU"]
    values = [
        metrics["transliteration_exact_match_acc"] * 100,
        (1.0 - metrics["e2e_devanagari_cer"]) * 100,
        metrics["e2e_translation_chrf"],
        metrics["e2e_translation_bleu"]
    ]
    colors = ["#38bdf8", "#34d399", "#facc15", "#a78bfa"]
    bars = ax2.bar(labels, values, color=colors, width=0.55, edgecolor="#ffffff", linewidth=0.5)
    ax2.set_title("Linguistic Quality Scores (Scale 0 - 100)", fontsize=12, fontweight="bold", color="#f1f5f9", pad=12)
    ax2.set_ylim(0, 105)
    ax2.grid(axis="y", linestyle="--", alpha=0.2, color="#94a3b8")
    ax2.tick_params(colors="#cbd5e1", labelsize=10)
    for spine in ax2.spines.values():
        spine.set_color("#475569")
    for bar in bars:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 2, f"{h:.1f}", ha="center", va="bottom",
                 fontsize=10, fontweight="bold", color="#f8fafc")

    # Subplot 3: Latency per Pipeline Stage
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_facecolor("#1e293b")
    stages = ["Transliteration\n(IndicXlit)", "Improvement\n(LLM/Linguistic)", "Translation\n(IndicTrans2)"]
    latencies = [
        metrics["avg_latency_transliteration_ms"],
        metrics["avg_latency_improvement_ms"],
        metrics["avg_latency_translation_ms"]
    ]
    bar_colors = ["#38bdf8", "#818cf8", "#f43f5e"]
    bars3 = ax3.barh(stages, latencies, color=bar_colors, height=0.45, edgecolor="#ffffff", linewidth=0.5)
    ax3.set_title("Average Processing Latency (ms per sentence)", fontsize=12, fontweight="bold", color="#f1f5f9", pad=12)
    ax3.grid(axis="x", linestyle="--", alpha=0.2, color="#94a3b8")
    ax3.tick_params(colors="#cbd5e1", labelsize=10)
    for spine in ax3.spines.values():
        spine.set_color("#475569")
    for bar in bars3:
        w = bar.get_width()
        ax3.text(w + 3, bar.get_y() + bar.get_height()/2, f"{w:.1f} ms", ha="left", va="center",
                 fontsize=10, fontweight="bold", color="#f8fafc")

    plt.savefig(OUTPUT_PNG, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print("Saved evaluation dashboard to:", OUTPUT_PNG)

if __name__ == "__main__":
    generate_chart()
