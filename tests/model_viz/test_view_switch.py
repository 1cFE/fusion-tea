"""View criteria V1–V5: both views after one load, switching without a reload, per-view state,
and loads and load errors landing in whichever view is active."""

import re

import pytest
import viewer_snapshots as vs
from edge_oracle import (
    calc_by_name,
    calcs,
    displayed_edges,
    expected_edges,
    group_paths,
    load_fixture,
    producer_bindings,
)
from structure_oracle import occurrences
from viewer_harness import (
    calc_key,
    click_element_centre,
    container_id_for_path,
    css_str,
    load_snapshot,
    panel_node_id,
    part_id_for_occurrence,
    selected_node_ids,
    show_calc,
    switch_view,
    toggle_group,
    toggle_part,
    view_geometry,
)


def occurrence_by_segment(snap, segment: str) -> str:
    (found,) = [o["occurrence_id"] for o in occurrences(snap) if o["display_segment"] == segment]
    return found


def app_state(page) -> dict:
    return page.evaluate("() => window.modelVizApp.state")


def count_nodes(page, selector: str) -> int:
    return page.evaluate("s => window.modelVizApp.cy.nodes(s).length", selector)


def test_both_views_available(fixture_page):
    page = fixture_page
    select = "[data-role=view-select]"
    assert page.is_enabled(select)
    options = page.evaluate("s => [...document.querySelector(s).options].map(o => o.value)", select)
    assert options == ["calcs", "structure"]
    assert page.get_attribute("body", "data-view") == "calcs"

    switch_view(page, "structure")
    assert page.get_attribute("body", "data-view") == "structure"
    assert count_nodes(page, '[kind="part"]') == 19
    assert count_nodes(page, '[kind!="part"]') == 0
    assert page.is_disabled("[data-role=mode-select]")

    switch_view(page, "calcs")
    assert page.get_attribute("body", "data-view") == "calcs"
    assert count_nodes(page, '[kind="part"]') == 0
    assert count_nodes(page, '[kind="container"]') > 0
    assert page.is_enabled("[data-role=mode-select]")


def test_switch_never_reloads(fixture_page):
    page = fixture_page
    seq = page.get_attribute("body", "data-load-seq")
    page.evaluate("() => { window.__heldModel = window.modelVizApp.model; }")
    for i in range(10):
        switch_view(page, "structure" if i % 2 == 0 else "calcs")
        assert page.get_attribute("body", "data-load-seq") == seq
        assert page.evaluate("() => window.modelVizApp.model === window.__heldModel")
        assert page.evaluate("() => window.modelVizApp.cy.nodes().length") > 0


def test_per_view_state_survives(fixture_page):
    snap = load_fixture()
    page = fixture_page
    page.click("[data-action=expand-all]")
    path = group_paths(snap)[0]
    toggle_group(page, path)
    calc = next(c for c in calcs(snap) if c["source_file"] != path)["node_id"]
    show_calc(page, calc)
    calc_state = app_state(page)
    assert calc_state["collapsed"] == [container_id_for_path(page, path)]

    switch_view(page, "structure")
    magnet = occurrence_by_segment(snap, "magnet")
    turbine = occurrence_by_segment(snap, "turbine")
    magnet_pid = part_id_for_occurrence(page, magnet)
    blanket_pid = part_id_for_occurrence(page, occurrence_by_segment(snap, "blanket"))
    toggle_part(page, magnet)
    click_element_centre(page, part_id_for_occurrence(page, turbine))
    structure_state = app_state(page)["structure"]
    assert structure_state == {"collapsed": [blanket_pid], "selected": turbine}

    switch_view(page, "calcs")
    after = app_state(page)
    assert (after["collapsed"], after["selected"]) == (
        calc_state["collapsed"],
        calc_state["selected"],
    )
    assert panel_node_id(page) == calc
    assert selected_node_ids(page) == [calc]

    switch_view(page, "structure")
    assert app_state(page)["structure"] == structure_state
    assert magnet_pid not in app_state(page)["structure"]["collapsed"]
    selected = page.evaluate(
        "() => window.modelVizApp.cy.nodes(':selected').map(n => n.data('occurrence_id'))"
    )
    assert selected == [turbine]


_CENTRE_INSIDE_PANE_JS = """key => {
  const cy = window.modelVizApp.cy;
  const b = cy.getElementById(key).renderedBoundingBox();
  const x = (b.x1 + b.x2) / 2, y = (b.y1 + b.y2) / 2;
  return x > 4 && y > 4 && x < cy.width() - 4 && y < cy.height() - 4;
}"""


def binding_with_consumer_in_pane(page, snap) -> tuple[str, str, str]:
    """A (consumer, input name, producer) binding whose consumer's centre is inside the pane."""
    for consumer, input_name, producer, _output in producer_bindings(snap):
        if producer != consumer and page.evaluate(_CENTRE_INSIDE_PANE_JS, calc_key(page, consumer)):
            return consumer, input_name, producer
    raise AssertionError("no consumer calc is inside the pane")


def test_same_view_is_a_no_op(fixture_page):
    """D27 and I9: a click, a link or a setView that stays in the active view never refits."""
    snap = load_fixture()
    page = fixture_page
    page.click("[data-action=expand-all]")
    page.evaluate("() => window.modelVizApp.cy.zoom(1.5)")
    before = view_geometry(page)

    # A real click on a drawn calc in the calc view: zoom, pan and every position stay.
    consumer, input_name, producer = binding_with_consumer_in_pane(page, snap)
    click_element_centre(page, calc_key(page, consumer))
    assert panel_node_id(page) == consumer
    assert view_geometry(page) == before

    # A panel link to a calc that is already drawn: zoom and positions stay; the pan may move.
    page.click(f"[data-input-kind=producer][data-input-name={css_str(input_name)}] [data-calc-key]")
    assert panel_node_id(page) == producer
    after_link = view_geometry(page)
    assert (after_link["zoom"], after_link["positions"]) == (before["zoom"], before["positions"])

    # setView to the active view touches nothing, not even the search box or the panel.
    page.fill("[data-role=search-input]", "typed but not searched")
    panel_html = page.inner_html("[data-role=panel]")
    page.evaluate("() => window.modelVizApp.setView('calcs')")
    assert view_geometry(page) == after_link
    assert page.input_value("[data-role=search-input]") == "typed but not searched"
    assert page.inner_html("[data-role=panel]") == panel_html

    # In the structure view, a real click on a drawn leaf part: zoom, pan and positions stay.
    switch_view(page, "structure")
    turbine = occurrence_by_segment(snap, "turbine")
    structure_before = view_geometry(page)
    click_element_centre(page, part_id_for_occurrence(page, turbine))
    assert app_state(page)["structure"]["selected"] == turbine
    assert view_geometry(page) == structure_before


def test_calc_view_after_round_trip(fixture_page):
    snap = load_fixture()
    page = fixture_page
    switch_view(page, "structure")
    switch_view(page, "calcs")
    everything = set(group_paths(snap))
    assert displayed_edges(page) == expected_edges(snap, everything)
    path = group_paths(snap)[0]
    toggle_group(page, path)
    assert displayed_edges(page) == expected_edges(snap, everything - {path})


def write_wrong_version(tmp):
    return vs.write(vs.wrong_version(load_fixture()), tmp / "v2.json")


def write_no_version(tmp):
    return vs.write(vs.no_version(load_fixture()), tmp / "no_version.json")


def write_non_json(tmp):
    return vs.write_bytes(vs.non_json_bytes(), tmp / "picked_by_mistake.pdf")


@pytest.mark.parametrize(
    ("write_bad", "message"),
    [
        (write_wrong_version, "instance-graph/v2"),
        (write_no_version, "not a codegen snapshot"),
        (write_non_json, "not a JSON file"),
    ],
    ids=["wrong_version", "no_version", "non_json"],
)
def test_load_errors_in_structure_view(viewer_page, fixture_path, tmp_path, write_bad, message):
    page = viewer_page
    assert load_snapshot(page, fixture_path) == "ready"
    show_calc(page, calc_by_name(load_fixture(), "total_capital")["node_id"])
    switch_view(page, "structure")
    assert load_snapshot(page, write_bad(tmp_path)) == "error"
    assert page.is_visible("[data-role=error-banner]")
    assert message in page.text_content("[data-role=error-banner]")
    assert page.evaluate("() => window.modelVizApp.cy.elements().length") == 0
    assert page.evaluate("() => window.modelVizApp.model") is None
    assert page.get_attribute("[data-role=panel]", "data-part-occurrence-id") is None
    assert page.get_attribute("[data-role=panel]", "data-calc-node-id") is None
    assert page.is_visible("[data-role=panel] .placeholder")
    options = page.eval_on_selector_all("#calc-names option, #part-paths option", "os => os.length")
    assert options == 0
    assert page.is_disabled("[data-role=view-select]")
    assert page.get_attribute("body", "data-view") == "structure"
    assert app_state(page)["structure"] == {"collapsed": [], "selected": None}

    # The next good load lands in the view that stayed active (I15).
    assert load_snapshot(page, fixture_path) == "ready"
    assert count_nodes(page, '[kind="part"]') == 19


def test_search_follows_view(fixture_page):
    snap = load_fixture()
    page = fixture_page
    assert page.text_content("[data-role=search-label]") == "Find calc"
    assert page.get_attribute("[data-role=search-input]", "list") == "calc-names"
    page.fill("[data-role=search-input]", "capital")
    page.press("[data-role=search-input]", "Enter")
    assert page.text_content("[data-role=search-status]").endswith("calcs match")

    switch_view(page, "structure")
    assert page.text_content("[data-role=search-label]") == "Find part"
    assert page.get_attribute("[data-role=search-input]", "list") == "part-paths"
    assert page.input_value("[data-role=search-input]") == ""
    assert page.text_content("[data-role=search-status]") == ""
    paths = page.eval_on_selector_all("#part-paths option", "os => os.map(o => o.value)")
    assert len(paths) == len(occurrences(snap))
    assert "stellaris/magnet/coil" in paths

    page.fill("[data-role=search-input]", "coil")
    switch_view(page, "calcs")
    assert page.text_content("[data-role=search-label]") == "Find calc"
    assert page.get_attribute("[data-role=search-input]", "list") == "calc-names"
    assert page.input_value("[data-role=search-input]") == ""


_SHOWN_NAME_TEXTS_JS = """() => {
  const panel = document.querySelector('[data-role=panel]');
  const texts = [...panel.querySelectorAll(
    '[data-role=part-name], [data-role=part-path], [data-role=type-name], [data-role=calc-name],'
    + ' .calc-link, .part-link, [data-owner] > h4, .attr-name,'
    + ' li[data-value-kind=calc-bound] [data-role=value-cell] .port,'
    + ' li[data-output-name] > .port, li[data-input-kind] > .port')].map(e => e.textContent);
  for (const el of panel.querySelectorAll('[data-owner], [data-attr-name], [data-output-name]')) {
    for (const key of ['owner', 'attrName', 'outputName']) {
      if (el.dataset[key] !== undefined) texts.push(el.dataset[key]);
    }
  }
  return texts;
}"""


def original_names_in(texts, names) -> set[str]:
    """Original names that stand as whole tokens in the texts, not behind the renamed_ prefix."""
    found = set()
    joined = "\n".join(texts)
    for name in names:
        if re.search(rf"(?<![\w']){re.escape(name)}(?![\w'])", joined):
            found.add(name)
    return found


def names_on_screen(page, snap) -> list[str]:
    """Every name-carrying text in both views, both datalists, and the panels of blanket, the root
    and the calc fuel_handling."""
    texts = []
    for view in ("structure", "calcs"):
        switch_view(page, view)
        page.click("[data-action=expand-all]")
        texts += page.evaluate("() => window.modelVizApp.cy.nodes().map(n => n.data('label'))")
    texts += page.eval_on_selector_all(
        "#calc-names option, #part-paths option", "os => os.map(o => o.value)"
    )
    for segment in ("blanket", "stellaris"):
        occ = next(
            o["occurrence_id"]
            for o in occurrences(snap)
            if o["display_segment"].removeprefix(vs.PREFIX) == segment
        )
        page.evaluate("id => window.modelVizApp.showPart(id)", occ)
        texts += page.evaluate(_SHOWN_NAME_TEXTS_JS)
    fuel = next(
        c for c in calcs(snap) if c["display_name"].removeprefix(vs.PREFIX) == "fuel_handling"
    )
    show_calc(page, fuel["node_id"])
    texts += page.evaluate(_SHOWN_NAME_TEXTS_JS)
    return texts


@pytest.mark.parametrize("active", ["calcs", "structure"])
def test_second_load_replaces_both_views(viewer_page, fixture_path, tmp_path, active):
    page = viewer_page
    original = load_fixture()
    names = vs.shown_names(original)
    assert load_snapshot(page, fixture_path) == "ready"
    # The reader finds the original names on the first load, so an empty result later is real.
    assert original_names_in(names_on_screen(page, original), names)

    page.evaluate(
        "id => window.modelVizApp.showPart(id)", occurrence_by_segment(original, "blanket")
    )
    show_calc(page, calc_by_name(original, "total_capital")["node_id"])
    switch_view(page, active)
    renamed = vs.renamed_everything(original)
    assert load_snapshot(page, vs.write(renamed, tmp_path / "renamed.json")) == "ready"

    assert page.get_attribute("body", "data-view") == active
    assert page.is_visible("[data-role=panel] .placeholder")
    assert page.get_attribute("[data-role=panel]", "data-part-occurrence-id") is None
    assert page.get_attribute("[data-role=panel]", "data-calc-node-id") is None
    assert app_state(page)["selected"] is None
    assert app_state(page)["structure"]["selected"] is None

    texts = names_on_screen(page, renamed)
    assert len(texts) > 100
    assert original_names_in(texts, names) == set()
    # The renamed root still names its type: its usage owner matched after the rename.
    assert "renamed_mfe_plant::renamed_'MFE Power Plant'" in texts
