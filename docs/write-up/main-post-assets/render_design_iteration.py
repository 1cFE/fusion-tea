"""Render design-iteration.html to design-iteration.png at 2x for the Substack post.

Run: uv run python docs/write-up/main-post-assets/render_design_iteration.py
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 900, "height": 900}, device_scale_factor=2)
    page.goto((HERE / "design-iteration.html").as_uri())
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(300)
    page.locator("#fig .frame").screenshot(path=str(HERE / "design-iteration.png"))
    browser.close()
