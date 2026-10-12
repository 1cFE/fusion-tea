"""Manual layout walk for the model-viz viewer (plan Phase 5). Screenshots land beside this file.

Run from the repo root: uv run python .project/active/model-viz/evidence/manual_walk.py
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "tests/model_viz"))

from viewer_harness import (  # noqa: E402
    FIXTURE,
    calc_key,
    container_id_for_path,
    load_snapshot,
    open_viewer,
)

ACCOUNT_COSTS = "root-0/analyses/mfe_account_costs.sysml"


def click_element(page, element_id):
    drawn = page.evaluate("id => window.modelVizApp.cy.getElementById(id).nonempty()", element_id)
    assert drawn, f"{element_id} is not drawn, so it cannot be clicked"
    box = page.evaluate(
        "id => window.modelVizApp.cy.getElementById(id).renderedBoundingBox()", element_id
    )
    pane = page.locator("[data-role=graph-pane]").bounding_box()
    page.mouse.click(
        pane["x"] + (box["x1"] + box["x2"]) / 2, pane["y"] + (box["y1"] + box["y2"]) / 2
    )


def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page, problems = open_viewer(browser)
        assert load_snapshot(page, FIXTURE) == "ready"
        page.screenshot(path=HERE / "01_all_collapsed.png")

        click_element(page, container_id_for_path(page, ACCOUNT_COSTS))
        page.screenshot(path=HERE / "02_account_costs_expanded.png")

        target = page.evaluate(
            "() => window.modelVizApp.model.calcs.find(c => c.name === 'fuel_handling').nodeId"
        )
        click_element(page, calc_key(page, target))
        page.screenshot(path=HERE / "03_cost_calc_selected.png")

        link = page.locator("[data-role=panel] [data-input-kind=producer] [data-calc-key]").first
        print("upstream link:", link.text_content())
        link.click()
        page.screenshot(path=HERE / "04_after_upstream_link.png")

        page.click("[data-action=expand-all]")
        page.screenshot(path=HERE / "05_all_expanded.png")

        print("page problems:", problems.items)
        browser.close()


if __name__ == "__main__":
    main()
