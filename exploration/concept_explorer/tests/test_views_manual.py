"""
Playwright-based acceptance tests for Categorical & Summary views.
Covers Phase 1-3 checklist items from the implementation plan.

Usage: uv run python exploration/concept_explorer/tests/test_views_manual.py

Requires server running on 127.0.0.1:8765
"""

import time
from playwright.sync_api import sync_playwright, Page

BASE = "http://127.0.0.1:8765"

# All 4 concepts use analysis IDs. All have cost models.
# 04 = Laser ICF p-B11 Fast Ignition (IFE)
# 05 = Planar Coil Stellarator (MFE)
# 06 = Magnetic Mirror p-B11 (MFE)
# 08 = FRC w/ Direct Conversion (MIF)
MFE_1 = "05"  # Planar Coil Stellarator
MFE_2 = "06"  # Magnetic Mirror
IFE   = "04"  # Laser ICF
MIF   = "08"  # FRC


def wait_for_compare(page: Page):
    """Wait for comparison app to load concepts."""
    page.wait_for_selector("#compare-content", state="visible", timeout=10000)
    # Wait for concept chips to appear in the concept bar
    page.wait_for_selector("#concept-bar .badge", timeout=10000)


def ss(page: Page, name: str):
    path = f"/tmp/view_test_{name}.png"
    page.screenshot(path=path, full_page=True)
    print(f"  screenshot: {path}")


def test_cat_integrated_2mfe(page: Page):
    """Categorical integrated: 2 MFE concepts, diff/match rows, MFE-only fields."""
    print("\n--- Categorical Integrated (2 MFE) ---")
    page.goto(f"{BASE}/compare?concepts={MFE_1},{MFE_2}&left=categorical")
    wait_for_compare(page)
    time.sleep(1.5)  # taxonomy fetch

    left = page.locator("#content-left")
    table = left.locator("table.comparison-table")
    assert table.count() == 1, "No comparison table"

    headers = table.locator("thead th")
    print(f"  Headers: {[h.text_content().strip() for h in headers.all()]}")
    assert headers.count() >= 3

    rows = table.locator("tbody tr")
    row_count = rows.count()
    diff_count = table.locator("tbody tr.diff").count()
    match_count = table.locator("tbody tr.match").count()
    print(f"  Rows: {row_count} (diff={diff_count}, match={match_count})")
    assert row_count >= 10
    assert diff_count + match_count == row_count

    text = table.text_content()
    assert "MFE Topology" in text, "MFE Topology missing"
    assert "IFE Driver" not in text, "IFE Driver should not appear"
    assert "MIF Method" not in text, "MIF Method should not appear"

    assert table.locator("thead .badge-mfe").count() >= 2

    ss(page, "cat_integrated_2mfe")
    print("  PASS")


def test_cat_integrated_cross_family(page: Page):
    """Categorical integrated: MFE + IFE shows cross-family fields."""
    print("\n--- Categorical Integrated (MFE + IFE) ---")
    page.goto(f"{BASE}/compare?concepts={MFE_1},{IFE}&left=categorical")
    wait_for_compare(page)
    time.sleep(1.5)

    table = page.locator("#content-left table.comparison-table")
    text = table.text_content()
    assert "IFE Driver" in text, "IFE Driver should appear"
    assert "MFE Topology" in text, "MFE Topology should appear"

    # Check inapplicable cells show dash
    na_cells = table.locator("td.val--na").count()
    print(f"  N/A cells (inapplicable): {na_cells}")
    assert na_cells >= 1, "Expected inapplicable cells with dash"

    ss(page, "cat_integrated_cross_family")
    print("  PASS")


def test_cat_integrated_all_families(page: Page):
    """Categorical integrated: MFE + IFE + MIF shows all family-specific fields."""
    print("\n--- Categorical Integrated (all families) ---")
    page.goto(f"{BASE}/compare?concepts={MFE_1},{IFE},{MIF}&left=categorical")
    wait_for_compare(page)
    time.sleep(1.5)

    table = page.locator("#content-left table.comparison-table")
    text = table.text_content()
    assert "MFE Topology" in text
    assert "IFE Driver" in text
    assert "MIF Method" in text

    ss(page, "cat_integrated_all_families")
    print("  PASS")


def test_cat_landscape(page: Page):
    """Categorical landscape: per-concept attribute cards, inapplicable fields omitted."""
    print("\n--- Categorical Landscape ---")
    page.goto(f"{BASE}/compare?concepts={MFE_1},{IFE}&left=categorical")
    wait_for_compare(page)
    time.sleep(1)

    page.click("#mode-landscape")
    time.sleep(1.5)

    grid = page.locator("#landscape-grid")
    cards = grid.locator(".taxonomy-card__attrs")
    print(f"  Cards: {cards.count()}")
    assert cards.count() >= 2

    attrs = grid.locator(".taxonomy-card__attr")
    print(f"  Total attr rows: {attrs.count()}")
    assert attrs.count() >= 10

    ss(page, "cat_landscape")
    print("  PASS")


def test_cat_mode_switch(page: Page):
    """Categorical: switch landscape -> integrated re-renders table."""
    print("\n--- Categorical Mode Switch ---")
    page.goto(f"{BASE}/compare?concepts={MFE_1},{MFE_2}&left=categorical")
    wait_for_compare(page)
    time.sleep(1)

    page.click("#mode-landscape")
    time.sleep(1)
    page.click("#mode-integrated")
    time.sleep(1.5)

    table = page.locator("#content-left table.comparison-table")
    assert table.count() == 1, "Table should re-render after mode switch"

    ss(page, "cat_mode_switch")
    print("  PASS")


def test_summary_integrated(page: Page):
    """Summary integrated: Plotly chart + metrics table with real values."""
    print("\n--- Summary Integrated ---")
    page.goto(f"{BASE}/compare?concepts={MFE_1},{MIF}&right=summary")
    wait_for_compare(page)
    time.sleep(2)

    right = page.locator("#content-right")

    plotly = right.locator(".js-plotly-plot")
    print(f"  Plotly charts: {plotly.count()}")
    assert plotly.count() >= 1

    table = right.locator("table.comparison-table--summary")
    assert table.count() == 1, "Missing metrics table"

    rows = table.locator("tbody tr")
    print(f"  Table rows: {rows.count()}")
    assert rows.count() >= 6  # 5 metrics + CAS driver

    text = table.text_content()
    assert "Top CAS" in text, "Missing Top CAS row"

    ss(page, "summary_integrated")
    print("  PASS")


def test_summary_landscape(page: Page):
    """Summary landscape: per-concept charts with synced axes."""
    print("\n--- Summary Landscape (3 concepts) ---")
    # Landscape uses `view` param (single view), not left/right
    page.goto(f"{BASE}/compare?concepts={MFE_1},{IFE},{MIF}&view=summary&mode=landscape")
    wait_for_compare(page)
    time.sleep(1)

    # If not already in landscape, click the button
    if page.locator("#landscape-grid").is_visible():
        pass
    else:
        page.click("#mode-landscape")
    time.sleep(2)

    # Select summary in landscape dropdown if not already
    landscape_select = page.locator("#select-landscape")
    if landscape_select.is_visible() and landscape_select.input_value() != "summary":
        landscape_select.select_option("summary")
        time.sleep(2)

    grid = page.locator("#landscape-grid")
    charts = grid.locator(".js-plotly-plot")
    print(f"  Plotly charts: {charts.count()}")
    assert charts.count() >= 3, f"Expected 3+ charts, got {charts.count()}"

    metrics = grid.locator(".summary-metric-row")
    print(f"  Metric rows: {metrics.count()}")
    assert metrics.count() >= 15  # 5+ per concept

    ss(page, "summary_landscape")
    print("  PASS")


def test_both_views_side_by_side(page: Page):
    """Integrated: categorical left + summary right simultaneously."""
    print("\n--- Both Views Side by Side ---")
    page.goto(f"{BASE}/compare?concepts={MFE_1},{IFE},{MIF}&left=categorical&right=summary")
    wait_for_compare(page)
    time.sleep(2)

    left_table = page.locator("#content-left table.comparison-table")
    right_chart = page.locator("#content-right .js-plotly-plot")
    right_table = page.locator("#content-right table.comparison-table--summary")

    assert left_table.count() == 1, "Categorical table missing"
    assert right_chart.count() >= 1, "Summary chart missing"
    assert right_table.count() == 1, "Summary metrics table missing"

    ss(page, "both_views")
    print("  PASS")


def test_view_switching_no_errors(page: Page):
    """Rapid view switching: no JS errors, no stale DOM."""
    print("\n--- Rapid View Switching ---")
    page.goto(f"{BASE}/compare?concepts={MFE_1},{MIF}&left=categorical&right=summary")
    wait_for_compare(page)
    time.sleep(2)

    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

    # Mutual exclusion: left and right can't show the same view.
    # 4 views: categorical, summary, capex, sensitivity
    # Start: left=categorical, right=summary
    # To swap, use a third view as intermediate.
    page.locator("#select-right").select_option("capex")  # free up "summary"
    time.sleep(0.5)
    page.locator("#select-left").select_option("summary")
    time.sleep(0.5)
    page.locator("#select-right").select_option("categorical")
    time.sleep(0.5)
    # Swap back
    page.locator("#select-right").select_option("capex")  # free up "categorical"
    time.sleep(0.5)
    page.locator("#select-left").select_option("categorical")
    time.sleep(0.5)
    page.locator("#select-right").select_option("summary")
    time.sleep(0.5)
    # Mode toggle
    page.click("#mode-landscape")
    time.sleep(1)
    page.click("#mode-integrated")
    time.sleep(1)

    js_errors = [e for e in errors if "favicon" not in e.lower()]
    print(f"  Console errors: {js_errors}")
    assert len(js_errors) == 0, f"JS errors: {js_errors}"

    ss(page, "view_switching")
    print("  PASS")


def test_url_persistence(page: Page):
    """URL state survives refresh."""
    print("\n--- URL Persistence ---")
    page.goto(f"{BASE}/compare?concepts={MFE_1},{MIF}&left=categorical&right=summary")
    wait_for_compare(page)
    time.sleep(2)

    page.reload()
    wait_for_compare(page)
    time.sleep(2)

    left_val = page.locator("#select-left").input_value()
    right_val = page.locator("#select-right").input_value()
    print(f"  After refresh: left={left_val}, right={right_val}")
    assert left_val == "categorical"
    assert right_val == "summary"

    assert page.locator("#content-left table.comparison-table").count() == 1
    assert page.locator("#content-right .js-plotly-plot").count() >= 1

    ss(page, "url_persistence")
    print("  PASS")


def test_full_flow_4_concepts(page: Page):
    """All 4 concepts, both views, both modes, no errors."""
    print("\n--- Full Flow (4 concepts) ---")
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

    page.goto(f"{BASE}/compare?concepts={MFE_1},{MFE_2},{IFE},{MIF}&left=categorical&right=summary")
    wait_for_compare(page)
    time.sleep(3)

    ss(page, "full_4_integrated")

    page.click("#mode-landscape")
    time.sleep(3)

    ss(page, "full_4_landscape")

    js_errors = [e for e in errors if "favicon" not in e.lower()]
    print(f"  Console errors: {js_errors}")
    assert len(js_errors) == 0, f"JS errors: {js_errors}"
    print("  PASS")


def test_regression_concept_page(page: Page):
    """Concept profile page still works."""
    print("\n--- Regression: Concept Page ---")
    page.goto(f"{BASE}/concept/{MFE_1}")
    page.wait_for_selector("h1, .section-title", timeout=10000)
    time.sleep(1)
    body = page.locator("body").text_content()
    assert "not found" not in body.lower(), "Page shows not found"
    ss(page, "regression_concept")
    print("  PASS")


def test_regression_taxonomy(page: Page):
    """Taxonomy page still works."""
    print("\n--- Regression: Taxonomy Page ---")
    page.goto(f"{BASE}/taxonomy")
    page.wait_for_selector("table, .card, main", timeout=10000)
    time.sleep(1)
    ss(page, "regression_taxonomy")
    print("  PASS")


def test_regression_index(page: Page):
    """Index page still works."""
    print("\n--- Regression: Index ---")
    page.goto(BASE)
    page.wait_for_selector(".card, main", timeout=10000)
    time.sleep(1)
    ss(page, "regression_index")
    print("  PASS")


def main():
    tests = [
        test_cat_integrated_2mfe,
        test_cat_integrated_cross_family,
        test_cat_integrated_all_families,
        test_cat_landscape,
        test_cat_mode_switch,
        test_summary_integrated,
        test_summary_landscape,
        test_both_views_side_by_side,
        test_view_switching_no_errors,
        test_url_persistence,
        test_full_flow_4_concepts,
        test_regression_concept_page,
        test_regression_taxonomy,
        test_regression_index,
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
    print("\nNote: 'no cost model' tests skipped — all 4 available concepts have cost models.")
    print("Screenshots: /tmp/view_test_*.png")
    return 1 if failed else 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
