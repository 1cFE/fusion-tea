"""Loading criteria L1–L5: the file picker, error loads, and replace-on-reload."""

import viewer_snapshots as vs
from edge_oracle import calcs, load_fixture
from viewer_harness import calc_node_count, load_snapshot, panel_node_id, show_calc


def banner_text(page) -> str:
    assert page.is_visible("[data-role=error-banner]")
    return page.text_content("[data-role=error-banner]")


def assert_nothing_drawn(page) -> None:
    assert page.evaluate("() => window.modelVizApp.cy.elements().length") == 0
    assert page.evaluate("() => window.modelVizApp.model") is None
    assert panel_node_id(page) is None
    assert page.eval_on_selector_all("#calc-names option", "os => os.length") == 0


def test_fixture_loads_via_picker(viewer_page, fixture_path):
    assert viewer_page.get_attribute("body", "data-load-state") == "empty"
    assert (
        viewer_page.evaluate("() => document.querySelector('[data-role=snapshot-input]').type")
        == "file"
    )
    assert load_snapshot(viewer_page, fixture_path) == "ready"
    viewer_page.click("[data-action=expand-all]")
    assert calc_node_count(viewer_page) == 77  # WI-057 (2026-09-13): feat/demo-maturation's WI-050 operating_heat (+1 calc, +3 outputs, +2 bound attributes)
    assert viewer_page.is_hidden("[data-role=error-banner]")


def test_wrong_version_rejected(viewer_page, tmp_path):
    path = vs.write(vs.wrong_version(load_fixture()), tmp_path / "v2.json")
    assert load_snapshot(viewer_page, path) == "error"
    text = banner_text(viewer_page)
    assert "instance-graph/v3" in text and "instance-graph/v2" in text
    assert_nothing_drawn(viewer_page)


def test_not_a_snapshot_rejected(viewer_page, tmp_path):
    path = vs.write(vs.no_version(load_fixture()), tmp_path / "no_version.json")
    assert load_snapshot(viewer_page, path) == "error"
    assert "not a codegen snapshot" in banner_text(viewer_page)
    assert_nothing_drawn(viewer_page)


def test_non_json_rejected(viewer_page, tmp_path):
    path = vs.write_bytes(vs.non_json_bytes(), tmp_path / "picked_by_mistake.pdf")
    assert load_snapshot(viewer_page, path) == "error"
    assert "not a JSON file" in banner_text(viewer_page)
    assert_nothing_drawn(viewer_page)


def test_v3_without_calcs_rejected(viewer_page, tmp_path):
    path = vs.write(vs.no_calcs_list(load_fixture()), tmp_path / "no_calcs.json")
    assert load_snapshot(viewer_page, path) == "error"
    assert "without a calcs list" in banner_text(viewer_page)
    assert_nothing_drawn(viewer_page)


def test_missing_calc_field_names_itself(viewer_page, tmp_path):
    path = vs.write(vs.calc_without_node_id(load_fixture(), 3), tmp_path / "no_node_id.json")
    assert load_snapshot(viewer_page, path) == "error"
    assert "calcs[3].node_id" in banner_text(viewer_page)
    assert_nothing_drawn(viewer_page)


def test_null_calc_entry_rejected(viewer_page, tmp_path):
    path = vs.write(vs.null_calc_entry(load_fixture(), 5), tmp_path / "null_calc.json")
    assert load_snapshot(viewer_page, path) == "error"
    assert "Calc entry 5 is not an object" in banner_text(viewer_page)
    assert_nothing_drawn(viewer_page)


def test_second_load_replaces_first(viewer_page, fixture_path, tmp_path):
    original = load_fixture()
    names = {c["display_name"] for c in calcs(original)}
    assert load_snapshot(viewer_page, fixture_path) == "ready"
    show_calc(viewer_page, calcs(original)[0]["node_id"])
    assert panel_node_id(viewer_page) is not None

    path = vs.write(vs.renamed(original), tmp_path / "renamed.json")
    assert load_snapshot(viewer_page, path) == "ready"
    assert panel_node_id(viewer_page) is None, "the panel starts empty after a reload"
    viewer_page.click("[data-action=expand-all]")
    labels = viewer_page.evaluate(
        "() => window.modelVizApp.cy.nodes('[kind=\"calc\"]').map(n => n.data('label'))"
    )
    assert len(labels) == 77  # WI-057 (2026-09-13): feat/demo-maturation's WI-050 operating_heat (+1 calc, +3 outputs, +2 bound attributes)
    assert all(label.startswith("renamed_") for label in labels)
    assert not names & set(labels)
    options = viewer_page.eval_on_selector_all("#calc-names option", "os => os.map(o => o.value)")
    assert all(o.startswith("renamed_") for o in options) and len(options) == 77  # WI-057 (2026-09-13): feat/demo-maturation's WI-050 operating_heat (+1 calc)

    fuel_handling = next(c for c in calcs(original) if c["display_name"] == "fuel_handling")
    show_calc(viewer_page, fuel_handling["node_id"])
    shown = viewer_page.eval_on_selector_all(
        "[data-role=panel] [data-role=calc-name], [data-role=panel] .calc-link",
        "els => els.map(e => e.textContent)",
    )
    assert len(shown) > 1
    assert all(text.startswith("renamed_") for text in shown)


def test_bad_load_after_good_clears(viewer_page, fixture_path, tmp_path):
    assert load_snapshot(viewer_page, fixture_path) == "ready"
    show_calc(viewer_page, calcs(load_fixture())[0]["node_id"])
    path = vs.write_bytes(vs.non_json_bytes(), tmp_path / "bad.json")
    assert load_snapshot(viewer_page, path) == "error"
    assert_nothing_drawn(viewer_page)
    assert viewer_page.evaluate("() => window.modelVizApp.state.selected") is None


def test_same_file_repick_reloads(viewer_page, fixture_path):
    assert load_snapshot(viewer_page, fixture_path) == "ready"
    assert viewer_page.get_attribute("body", "data-load-seq") == "1"
    assert load_snapshot(viewer_page, fixture_path) == "ready"
    assert viewer_page.get_attribute("body", "data-load-seq") == "2"
