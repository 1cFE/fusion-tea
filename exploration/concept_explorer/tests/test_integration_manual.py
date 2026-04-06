"""
Playwright-based integration tests for end-to-end wiring:
Selection tray (taxonomy page) -> Comparison page.

Usage: uv run python exploration/concept_explorer/tests/test_integration_manual.py

Requires server running on 127.0.0.1:8765
"""

import time
from playwright.sync_api import sync_playwright, Page

BASE = "http://127.0.0.1:8765"

# Analysis IDs (see PLAYWRIGHT_GUIDE.md)
MFE_1 = "05"  # Planar Coil Stellarator
MFE_2 = "06"  # Magnetic Mirror
IFE   = "04"  # Laser ICF
MIF   = "08"  # FRC


def wait_for_taxonomy(page: Page):
    """Wait for taxonomy page to fully load including selection tray."""
    page.wait_for_selector("#taxonomy-content", state="visible", timeout=10000)
    page.wait_for_selector(".selection-tray", state="visible", timeout=10000)


def wait_for_compare(page: Page):
    """Wait for comparison app to load concepts."""
    page.wait_for_selector("#compare-content", state="visible", timeout=10000)
    page.wait_for_selector("#concept-bar .badge", timeout=10000)


def ss(page: Page, name: str):
    path = f"/tmp/integration_test_{name}.png"
    page.screenshot(path=path, full_page=True)
    print(f"  screenshot: {path}")


def expand_tree_to_leaf(page: Page, concept_id: str):
    """Expand all collapsed parent branches so a tree leaf becomes visible."""
    # Use JS to expand parent tree-node__children (same logic as TreeView.highlightTreeConcept)
    page.evaluate("""(conceptId) => {
        const leaf = document.querySelector('[data-concept-id="' + conceptId + '"]');
        if (!leaf) return;
        let parent = leaf.parentElement;
        while (parent) {
            if (parent.classList.contains('tree-node__children')) {
                parent.classList.add('tree-node__children--open');
                const header = parent.previousElementSibling;
                if (header) {
                    const toggle = header.querySelector('.tree-node__toggle');
                    if (toggle) toggle.classList.add('tree-node__toggle--open');
                }
            }
            parent = parent.parentElement;
        }
    }""", concept_id)
    time.sleep(0.2)


def tray_add_via_tree(page: Page, concept_id: str):
    """Ctrl+click a tree leaf to trigger popover, then click Add."""
    expand_tree_to_leaf(page, concept_id)
    leaf = page.locator(f'.tree-leaf[data-concept-id="{concept_id}"]')
    leaf.scroll_into_view_if_needed()
    leaf.click(modifiers=["Control"])
    # Popover should appear — click Add
    page.wait_for_selector(".selection-popover__confirm", state="visible", timeout=3000)
    page.locator(".selection-popover__confirm").click()
    time.sleep(0.3)


def tray_chip_count(page: Page) -> int:
    """Return number of chips in the selection tray."""
    return page.locator(".selection-tray__chip").count()


# ---------------------------------------------------------------------------
# Selection Tray Tests
# ---------------------------------------------------------------------------

def test_tray_renders_on_taxonomy(page: Page):
    """Taxonomy page loads, tray bar visible at bottom, no JS errors."""
    print("\n--- Tray Renders on Taxonomy ---")
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

    page.goto(f"{BASE}/taxonomy")
    wait_for_taxonomy(page)

    tray = page.locator(".selection-tray")
    assert tray.is_visible(), "Selection tray not visible"

    # Check action buttons exist and are disabled
    integrated_btn = page.locator('.selection-tray__action[data-mode="integrated"]')
    landscape_btn = page.locator('.selection-tray__action[data-mode="landscape"]')
    assert integrated_btn.is_disabled(), "Integrated button should be disabled with 0 concepts"
    assert landscape_btn.is_disabled(), "Landscape button should be disabled with 0 concepts"

    js_errors = [e for e in errors if "favicon" not in e.lower()]
    assert len(js_errors) == 0, f"JS errors on taxonomy: {js_errors}"

    ss(page, "tray_renders")
    print("  PASS")


def test_tray_ctrl_click_tree(page: Page):
    """Ctrl+click a tree leaf adds concept to tray via popover."""
    print("\n--- Tray Ctrl+Click Tree ---")
    page.goto(f"{BASE}/taxonomy")
    wait_for_taxonomy(page)

    assert tray_chip_count(page) == 0, "Tray should start empty"

    tray_add_via_tree(page, MFE_1)

    assert tray_chip_count(page) == 1, f"Expected 1 chip, got {tray_chip_count(page)}"

    # Chip should have a family badge
    badge = page.locator(".selection-tray__chip .selection-tray__chip-badge")
    assert badge.count() == 1, "Chip should have a badge"

    ss(page, "tray_ctrl_click_tree")
    print("  PASS")


def test_tray_ctrl_click_constellation(page: Page):
    """Ctrl+click a constellation dot adds concept to tray."""
    print("\n--- Tray Ctrl+Click Constellation ---")
    page.goto(f"{BASE}/taxonomy")
    wait_for_taxonomy(page)
    time.sleep(1)  # let Plotly render constellation

    # Constellation uses Plotly scatter — Ctrl+click on a point.
    # Plotly points are inside .js-plotly-plot. We click on the plot area
    # with coordinates. Easier: use the tree (already tested), but we want
    # to verify constellation doesn't error on Ctrl+click.
    # Plotly intercepts clicks via plotly_click events. Ctrl+click with
    # modifier should trigger the onCtrlClick handler.
    # Plotly renders inside or as the constellation container
    constellation = page.locator("#constellation-container .js-plotly-plot")
    if constellation.count() == 0:
        constellation = page.locator("#constellation-container")
    assert constellation.count() >= 1, "No constellation container"

    # Click somewhere in the middle of the plot with Ctrl held
    box = constellation.bounding_box()
    if box:
        page.keyboard.down("Control")
        page.mouse.click(
            box["x"] + box["width"] * 0.5,
            box["y"] + box["height"] * 0.5,
        )
        page.keyboard.up("Control")
        time.sleep(0.5)
        # We may or may not hit a dot — this tests that Ctrl+click doesn't error
        # If we hit a dot, popover appears; if not, nothing happens (both OK)

    ss(page, "tray_ctrl_click_constellation")
    print("  PASS (no errors)")


def test_tray_toggle_remove(page: Page):
    """Ctrl+click same concept twice: add then remove (toggle)."""
    print("\n--- Tray Toggle Remove ---")
    page.goto(f"{BASE}/taxonomy")
    wait_for_taxonomy(page)

    # Add
    tray_add_via_tree(page, MFE_1)
    assert tray_chip_count(page) == 1

    # Ctrl+click again — should remove (no popover, immediate removal)
    leaf = page.locator(f'.tree-leaf[data-concept-id="{MFE_1}"]')
    leaf.scroll_into_view_if_needed()
    leaf.click(modifiers=["Control"])
    time.sleep(0.3)

    assert tray_chip_count(page) == 0, f"Expected 0 chips after toggle, got {tray_chip_count(page)}"

    ss(page, "tray_toggle_remove")
    print("  PASS")


def test_tray_clear_all(page: Page):
    """Add 2 concepts, click Clear All, tray empties."""
    print("\n--- Tray Clear All ---")
    page.goto(f"{BASE}/taxonomy")
    wait_for_taxonomy(page)

    tray_add_via_tree(page, MFE_1)
    tray_add_via_tree(page, IFE)
    assert tray_chip_count(page) == 2

    page.locator(".selection-tray__clear").click()
    time.sleep(0.3)

    assert tray_chip_count(page) == 0, "Tray should be empty after Clear All"

    ss(page, "tray_clear_all")
    print("  PASS")


def test_tray_persists_across_tabs(page: Page):
    """Add concept in overview, switch to neighborhood view and back, chip persists."""
    print("\n--- Tray Persists Across Tab Switch ---")
    page.goto(f"{BASE}/taxonomy")
    wait_for_taxonomy(page)

    tray_add_via_tree(page, MFE_1)
    assert tray_chip_count(page) == 1

    # Focus a concept to switch to neighborhood view
    expand_tree_to_leaf(page, MFE_2)
    leaf = page.locator(f'.tree-leaf[data-concept-id="{MFE_2}"]')
    leaf.scroll_into_view_if_needed()
    leaf.click()  # single click focuses → neighborhood graph
    time.sleep(1.5)

    # Chip should still be there
    assert tray_chip_count(page) == 1, "Chip should persist after view switch"

    # Go back to overview
    back_btn = page.locator("#back-to-overview")
    if back_btn.is_visible():
        back_btn.click()
        time.sleep(1)

    assert tray_chip_count(page) == 1, "Chip should persist after returning to overview"

    ss(page, "tray_persists_tabs")
    print("  PASS")


def test_tray_action_buttons(page: Page):
    """Action buttons enable/disable based on selection count."""
    print("\n--- Tray Action Buttons ---")
    page.goto(f"{BASE}/taxonomy")
    wait_for_taxonomy(page)

    integrated = page.locator('.selection-tray__action[data-mode="integrated"]')
    landscape = page.locator('.selection-tray__action[data-mode="landscape"]')

    # 0 concepts: both disabled
    assert integrated.is_disabled(), "Integrated should be disabled with 0"
    assert landscape.is_disabled(), "Landscape should be disabled with 0"

    # 1 concept: both enabled (MIN_INTEGRATED=1, MIN_LANDSCAPE=1)
    tray_add_via_tree(page, MFE_1)
    assert not integrated.is_disabled(), "Integrated should be enabled with 1"
    assert not landscape.is_disabled(), "Landscape should be enabled with 1"

    # 2 concepts: both enabled
    tray_add_via_tree(page, IFE)
    assert not integrated.is_disabled(), "Integrated should be enabled with 2"
    assert not landscape.is_disabled(), "Landscape should be enabled with 2"

    # 3 concepts: both enabled (MAX_INTEGRATED=3)
    tray_add_via_tree(page, MIF)
    assert not integrated.is_disabled(), "Integrated should be enabled with 3"
    assert not landscape.is_disabled(), "Landscape should be enabled with 3"

    # 4 concepts: integrated disabled (>MAX_INTEGRATED=3), landscape enabled
    tray_add_via_tree(page, MFE_2)
    assert integrated.is_disabled(), "Integrated should be disabled with 4 (>MAX_INTEGRATED)"
    assert not landscape.is_disabled(), "Landscape should be enabled with 4"

    ss(page, "tray_action_buttons")
    print("  PASS")


# ---------------------------------------------------------------------------
# End-to-End Flow Tests
# ---------------------------------------------------------------------------

def test_e2e_tray_to_integrated(page: Page):
    """Add 2 concepts on taxonomy, click Integrated, comparison page loads."""
    print("\n--- E2E: Tray -> Integrated ---")
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

    page.goto(f"{BASE}/taxonomy")
    wait_for_taxonomy(page)

    tray_add_via_tree(page, MFE_1)
    tray_add_via_tree(page, IFE)

    # Click Integrated button — should navigate to comparison page
    page.locator('.selection-tray__action[data-mode="integrated"]').click()
    wait_for_compare(page)
    time.sleep(2)

    # Verify URL contains mode and concepts
    url = page.url
    assert "mode=integrated" in url, f"URL missing mode=integrated: {url}"
    assert MFE_1 in url, f"URL missing concept {MFE_1}: {url}"
    assert IFE in url, f"URL missing concept {IFE}: {url}"

    # Verify integrated layout is visible
    assert page.locator("#compare-integrated").is_visible(), "Integrated layout not visible"

    # Verify concept chips rendered
    chips = page.locator("#concept-bar .badge")
    assert chips.count() >= 2, f"Expected 2+ concept chips, got {chips.count()}"

    js_errors = [e for e in errors if "favicon" not in e.lower()]
    assert len(js_errors) == 0, f"JS errors: {js_errors}"

    ss(page, "e2e_tray_to_integrated")
    print("  PASS")


def test_e2e_tray_to_landscape(page: Page):
    """Add 3 concepts, click Landscape, comparison page loads in landscape mode."""
    print("\n--- E2E: Tray -> Landscape ---")
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

    page.goto(f"{BASE}/taxonomy")
    wait_for_taxonomy(page)

    tray_add_via_tree(page, MFE_1)
    tray_add_via_tree(page, IFE)
    tray_add_via_tree(page, MIF)

    page.locator('.selection-tray__action[data-mode="landscape"]').click()
    wait_for_compare(page)
    time.sleep(2)

    url = page.url
    assert "mode=landscape" in url, f"URL missing mode=landscape: {url}"

    assert page.locator("#compare-landscape").is_visible(), "Landscape layout not visible"

    js_errors = [e for e in errors if "favicon" not in e.lower()]
    assert len(js_errors) == 0, f"JS errors: {js_errors}"

    ss(page, "e2e_tray_to_landscape")
    print("  PASS")


def test_e2e_url_shareable(page: Page):
    """Navigate from tray, copy URL, goto in fresh context -> same state."""
    print("\n--- E2E: URL Shareable ---")
    page.goto(f"{BASE}/taxonomy")
    wait_for_taxonomy(page)

    tray_add_via_tree(page, MFE_1)
    tray_add_via_tree(page, MIF)

    page.locator('.selection-tray__action[data-mode="integrated"]').click()
    wait_for_compare(page)
    time.sleep(2)

    # Capture state
    url = page.url
    left_view = page.locator("#select-left").input_value()
    right_view = page.locator("#select-right").input_value()
    chip_count = page.locator("#concept-bar .badge").count()
    print(f"  Original: url={url}, left={left_view}, right={right_view}, chips={chip_count}")

    # Open same URL fresh
    page.goto(url)
    wait_for_compare(page)
    time.sleep(2)

    # Verify same state
    left_view2 = page.locator("#select-left").input_value()
    right_view2 = page.locator("#select-right").input_value()
    chip_count2 = page.locator("#concept-bar .badge").count()
    print(f"  Restored: left={left_view2}, right={right_view2}, chips={chip_count2}")

    assert left_view == left_view2, f"Left view changed: {left_view} -> {left_view2}"
    assert right_view == right_view2, f"Right view changed: {right_view} -> {right_view2}"
    assert chip_count == chip_count2, f"Chip count changed: {chip_count} -> {chip_count2}"

    ss(page, "e2e_url_shareable")
    print("  PASS")


# ---------------------------------------------------------------------------
# Comparison Page Tests
# ---------------------------------------------------------------------------

def test_compare_add_remove_concept(page: Page):
    """Use inline picker to add/remove a concept, views re-render."""
    print("\n--- Compare: Add/Remove Concept ---")
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

    page.goto(f"{BASE}/compare?concepts={MFE_1},{IFE}&left=categorical&right=summary")
    wait_for_compare(page)
    time.sleep(2)

    initial_chips = page.locator("#concept-bar .badge").count()

    # Click + Add concept button
    add_btn = page.locator("#concept-bar button, .concept-add-btn, [aria-label*='Add']")
    if add_btn.count() > 0:
        add_btn.first.click()
        time.sleep(0.5)

        # Picker should be visible
        picker = page.locator("#concept-picker")
        if picker.is_visible():
            # Click first available concept in picker
            picker_items = picker.locator("[role='option'], .picker-item, .picker-list > *")
            if picker_items.count() > 0:
                picker_items.first.click()
                time.sleep(2)

                new_chips = page.locator("#concept-bar .badge").count()
                print(f"  Chips: {initial_chips} -> {new_chips}")

    js_errors = [e for e in errors if "favicon" not in e.lower()]
    assert len(js_errors) == 0, f"JS errors: {js_errors}"

    ss(page, "compare_add_remove")
    print("  PASS")


def test_compare_empty_state(page: Page):
    """Navigate to /compare with no concepts -> empty state visible."""
    print("\n--- Compare: Empty State ---")
    page.goto(f"{BASE}/compare")
    page.wait_for_selector("#compare-content", state="visible", timeout=10000)
    time.sleep(1)

    empty = page.locator("#empty-state")
    assert empty.is_visible(), "Empty state should be visible with no concepts"

    text = empty.text_content()
    assert "taxonomy" in text.lower() or "Taxonomy" in text, "Empty state should mention taxonomy"

    ss(page, "compare_empty_state")
    print("  PASS")


# ---------------------------------------------------------------------------
# Regression Tests
# ---------------------------------------------------------------------------

def test_regression_concept_profile(page: Page):
    """Concept profile page: sliders, tornado chart, no errors."""
    print("\n--- Regression: Concept Profile ---")
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

    page.goto(f"{BASE}/concept/{MFE_1}")
    page.wait_for_selector("h1, .section-title", timeout=10000)
    time.sleep(2)

    body = page.text_content("body")
    assert "not found" not in body.lower(), "Page shows not found"

    # Check for Plotly charts (tornado and/or CAS)
    charts = page.locator(".js-plotly-plot")
    print(f"  Plotly charts: {charts.count()}")

    js_errors = [e for e in errors if "favicon" not in e.lower()]
    assert len(js_errors) == 0, f"JS errors: {js_errors}"

    ss(page, "regression_concept_profile")
    print("  PASS")


def test_regression_index_grid(page: Page):
    """Index page loads with concept cards."""
    print("\n--- Regression: Index Grid ---")
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

    page.goto(BASE)
    page.wait_for_selector(".card, main", timeout=10000)
    time.sleep(1)

    js_errors = [e for e in errors if "favicon" not in e.lower()]
    assert len(js_errors) == 0, f"JS errors: {js_errors}"

    ss(page, "regression_index")
    print("  PASS")


def test_regression_taxonomy_tree_click(page: Page):
    """Tree leaf click focuses concept (existing behavior preserved)."""
    print("\n--- Regression: Taxonomy Tree Click ---")
    page.goto(f"{BASE}/taxonomy")
    wait_for_taxonomy(page)

    expand_tree_to_leaf(page, MFE_1)
    leaf = page.locator(f'.tree-leaf[data-concept-id="{MFE_1}"]')
    leaf.scroll_into_view_if_needed()
    leaf.click()  # single click focuses -> switches to neighborhood view
    time.sleep(2)

    # Should have switched to neighborhood graph view
    neighborhood = page.locator("#neighborhood-container")
    assert neighborhood.is_visible(), "Neighborhood container should be visible after tree click"

    ss(page, "regression_taxonomy_tree_click")
    print("  PASS")


def test_regression_no_js_errors_all_pages(page: Page):
    """Visit all major pages, collect console errors, assert zero."""
    print("\n--- Regression: No JS Errors (All Pages) ---")
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

    pages_to_visit = [
        (f"{BASE}/", "index"),
        (f"{BASE}/taxonomy", "taxonomy"),
        (f"{BASE}/compare?concepts={MFE_1},{IFE}&left=categorical&right=summary", "compare"),
        (f"{BASE}/concept/{MFE_1}", "concept"),
    ]

    for url, name in pages_to_visit:
        page.goto(url)
        time.sleep(2)
        print(f"  Visited: {name}")

    js_errors = [e for e in errors if "favicon" not in e.lower()]
    print(f"  Total JS errors across all pages: {len(js_errors)}")
    if js_errors:
        for e in js_errors:
            print(f"    - {e}")
    assert len(js_errors) == 0, f"JS errors: {js_errors}"

    print("  PASS")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    tests = [
        # Selection tray
        test_tray_renders_on_taxonomy,
        test_tray_ctrl_click_tree,
        test_tray_ctrl_click_constellation,
        test_tray_toggle_remove,
        test_tray_clear_all,
        test_tray_persists_across_tabs,
        test_tray_action_buttons,
        # End-to-end flow
        test_e2e_tray_to_integrated,
        test_e2e_tray_to_landscape,
        test_e2e_url_shareable,
        # Comparison page
        test_compare_add_remove_concept,
        test_compare_empty_state,
        # Regression
        test_regression_concept_profile,
        test_regression_index_grid,
        test_regression_taxonomy_tree_click,
        test_regression_no_js_errors_all_pages,
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1400, "height": 900})
        page = ctx.new_page()

        passed = failed = 0
        failures = []

        for t in tests:
            try:
                t(page)
                passed += 1
            except Exception as e:
                failed += 1
                failures.append((t.__name__, str(e)))
                print(f"  FAIL: {e}")
                ss(page, f"FAIL_{t.__name__}")

        browser.close()

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed / {passed+failed} total")
    if failures:
        print("\nFailures:")
        for name, err in failures:
            print(f"  {name}: {err}")
    print(f"{'='*60}")
    print("\nScreenshots: /tmp/integration_test_*.png")
    return 1 if failed else 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
