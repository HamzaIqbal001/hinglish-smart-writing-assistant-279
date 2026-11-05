"""
Converts docs/REPORT.md into a high-quality PDF docs/REPORT.pdf using Playwright.
"""

from pathlib import Path
import markdown
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_MD = BASE_DIR / "docs" / "REPORT.md"
REPORT_PDF = BASE_DIR / "docs" / "REPORT.pdf"

CSS = """
@page {
    size: A4;
    margin: 20mm;
}
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.5;
    color: #1e293b;
    font-size: 11pt;
}
h1 {
    color: #0f172a;
    font-size: 20pt;
    border-bottom: 2px solid #3b82f6;
    padding-bottom: 6px;
    margin-bottom: 12px;
}
h2 {
    color: #1e3a8a;
    font-size: 14pt;
    margin-top: 18px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
}
h3 {
    color: #1e40af;
    font-size: 12pt;
    margin-top: 14px;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 9.5pt;
}
th, td {
    border: 1px solid #cbd5e1;
    padding: 6px 10px;
    text-align: left;
}
th {
    background-color: #f1f5f9;
    font-weight: 600;
}
tr:nth-child(even) {
    background-color: #f8fafc;
}
code {
    background-color: #f1f5f9;
    color: #0f172a;
    padding: 2px 4px;
    border-radius: 4px;
    font-size: 9pt;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}
pre {
    background-color: #0f172a;
    color: #f8fafc;
    padding: 10px;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 8.5pt;
}
pre code {
    background-color: transparent;
    color: inherit;
    padding: 0;
}
hr {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 16px 0;
}
"""

def export_pdf():
    with open(REPORT_MD, "r", encoding="utf-8") as f:
        md_text = f.read()

    html_content = markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>{CSS}</style>
</head>
<body>
{html_content}
</body>
</html>"""

    tmp_html = BASE_DIR / "docs" / "_temp_report.html"
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(full_html)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file://{tmp_html.resolve()}")
        page.pdf(
            path=str(REPORT_PDF),
            format="A4",
            print_background=True,
            margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"}
        )
        browser.close()

    tmp_html.unlink()
    print("Successfully exported report to:", REPORT_PDF)

if __name__ == "__main__":
    export_pdf()
