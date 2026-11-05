"""
Automated screenshot capture for Hinglish Smart Writing Assistant using Playwright.
Captures:
- docs/screenshots/01_home.png
- docs/screenshots/02_transliteration.png
- docs/screenshots/03_improve_and_translate.png
- docs/screenshots/04_code_mixed_example.png
"""

import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = BASE_DIR / "docs" / "screenshots"

def capture_all():
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        print("Navigating to Gradio app at http://localhost:7860 ...")
        page.goto("http://localhost:7860", wait_until="networkidle", timeout=30000)
        time.sleep(2)

        # 01_home.png: Initial application state
        home_path = SCREENSHOTS_DIR / "01_home.png"
        page.screenshot(path=str(home_path), full_page=True)
        print("Captured:", home_path)

        # 02_transliteration.png: Transliteration only
        # Uncheck Improve Phrasing and Translate to English
        page.locator("label:has-text('Improve Phrasing') input[type='checkbox']").uncheck()
        page.locator("label:has-text('Translate to English') input[type='checkbox']").uncheck()
        page.locator("textarea[data-testid='textbox']").first.fill("mujhe kal subah meeting ke liye jaana hai")
        page.locator("button:has-text('Process Text')").click()
        
        # Wait for native script output
        time.sleep(2)
        translit_path = SCREENSHOTS_DIR / "02_transliteration.png"
        page.screenshot(path=str(translit_path), full_page=True)
        print("Captured:", translit_path)

        # 03_improve_and_translate.png: All steps active
        page.locator("label:has-text('Improve Phrasing') input[type='checkbox']").check()
        page.locator("label:has-text('Translate to English') input[type='checkbox']").check()
        page.locator("button:has-text('Process Text')").click()

        time.sleep(3)
        imp_path = SCREENSHOTS_DIR / "03_improve_and_translate.png"
        page.screenshot(path=str(imp_path), full_page=True)
        print("Captured:", imp_path)

        # 04_code_mixed_example.png: Code-mixed input
        page.locator("textarea[data-testid='textbox']").first.fill("project ki deadline agle hafte tak extend ho gayi hai")
        page.locator("button:has-text('Process Text')").click()

        time.sleep(3)
        cm_path = SCREENSHOTS_DIR / "04_code_mixed_example.png"
        page.screenshot(path=str(cm_path), full_page=True)
        print("Captured:", cm_path)

        browser.close()
        print("All screenshots successfully captured!")

if __name__ == "__main__":
    capture_all()
