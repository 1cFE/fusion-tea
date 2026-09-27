"""Navigation criteria N1–N2, the search box, and real canvas clicks (P1's "clicking a calc node").

Panel links, the search box and the canvas are driven with real Playwright input. Expected
targets and groups come from the raw snapshot.
"""

from edge_oracle import calc_by_name, calcs, load_fixture, path_of, producer_bindings
from structure_oracle import attributes_of, displayed_parts, occurrences
from structure_oracle import path_of as part_path_of
from viewer_harness import (
    calc_key,
    container_id_for_path,
    css_str,
    group_collapsed,
    load_snapshot,
    open_viewer,
    panel_node_id,
    part_id_for_occurrence,
    selected_node_ids,
    show_calc,
    switch_view,
    toggle_group,
)


def cross_group_bindings(snap) -> list[tuple[str, str, str, str]]:
    """Bindings (snapshot order) whose producer and consumer sit in different source files."""
    return [b for b in producer_bindings(snap) if path_of(snap, b[0]) != path_of(snap, b[2])]


def pane_offset(page) -> tuple[float, float]:
    box = page.locator("[data-role=graph-pane]").bounding_box()
    return box["x"], box["y"]


def rendered_box(page, element_id: str) -> dict:
    box = page.evaluate(
        "id => window.modelVizApp.cy.getElementById(id).renderedBoundingBox()", element_id
    )
    assert box is not None
    return box


def pane_size(page) -> tuple[float, float]:
    return tuple(
        page.evaluate("() => [window.modelVizApp.cy.width(), window.modelVizApp.cy.height()]")
    )


def click_rendered_point(page, x: float, y: float) -> None:
    width, height = pane_size(page)
    assert 0 < x < width and 0 < y < height, f"point ({x}, {y}) is outside the graph pane"
    ox, oy = pane_offset(page)
    page.mouse.click(ox + x, oy + y)


def click_element_centre(page, element_id: str) -> None:
    box = rendered_box(page, element_id)
    click_rendered_point(page, (box["x1"] + box["x2"]) / 2, (box["y1"] + box["y2"]) / 2)


def click_calc_on_canvas(page, node_id: str) -> None:
    click_element_centre(page, calc_key(page, node_id))


def fully_inside_pane(page, node_id: str) -> bool:
    box = rendered_box(page, calc_key(page, node_id))
    width, height = pane_size(page)
    return box["x1"] >= 0 and box["y1"] >= 0 and box["x2"] <= width and box["y2"] <= height


def assert_arrived(page, snap, node_id: str) -> None:
    assert panel_node_id(page) == node_id
    assert selected_node_ids(page) == [node_id]
    assert not group_collapsed(page, path_of(snap, node_id))
    assert fully_inside_pane(page, node_id)


def test_panel_link_navigation(fixture_page):
    snap = load_fixture()
    page = fixture_page
    page.click("[data-action=expand-all]")
    start = calc_by_name(snap, "total_capital")
    show_calc(page, start["node_id"])

    upstream_input = next(i for i in start["inputs"] if i["edge"]["kind"] == "producer")
    producer = upstream_input["edge"]["target"]["calculation"]
    page.click(
        f"[data-input-kind=producer][data-input-name={css_str(upstream_input['name'])}] "
        "[data-calc-key]"
    )
    assert_arrived(page, snap, producer)

    consumer = next(c for c, _, p, _ in producer_bindings(snap) if p == producer)
    page.click(f"[data-role=panel] [data-consumer-node-id={css_str(consumer)}]")
    assert_arrived(page, snap, consumer)


def test_hidden_target_upstream(fixture_page):
    snap = load_fixture()
    page = fixture_page
    consumer, input_name, producer, _output = cross_group_bindings(snap)[0]
    page.click("[data-action=collapse-all]")
    toggle_group(page, path_of(snap, consumer))
    assert group_collapsed(page, path_of(snap, producer))
    click_calc_on_canvas(page, consumer)
    assert panel_node_id(page) == consumer
    page.click(
        f"[data-input-kind=producer][data-input-name={css_str(input_name)}]"
        f"[data-producer-node-id={css_str(producer)}] [data-calc-key]"
    )
    assert_arrived(page, snap, producer)
    assert not group_collapsed(page, path_of(snap, consumer))


def test_hidden_target_downstream(fixture_page):
    snap = load_fixture()
    page = fixture_page
    consumer, input_name, producer, output = cross_group_bindings(snap)[-1]
    page.click("[data-action=collapse-all]")
    toggle_group(page, path_of(snap, producer))
    assert group_collapsed(page, path_of(snap, consumer))
    click_calc_on_canvas(page, producer)
    assert panel_node_id(page) == producer
    page.click(
        f"[data-output-id={css_str(output)}] [data-consumer-node-id={css_str(consumer)}]"
        f"[data-input-name={css_str(input_name)}]"
    )
    assert_arrived(page, snap, consumer)


_CONTAINER_BACKGROUND_POINT_JS = """
(id) => {
  const cy = window.modelVizApp.cy;
  const box = cy.getElementById(id);
  const b = box.renderedBoundingBox();
  const kids = box.children().map(c => c.renderedBoundingBox());
  const margin = 6;
  const clearOfKids = (x, y) => kids.every(k =>
    x < k.x1 - margin || x > k.x2 + margin || y < k.y1 - margin || y > k.y2 + margin);
  const pan = cy.pan(), zoom = cy.zoom();
  const onlyContainer = (x, y) => {
    const mx = (x - pan.x) / zoom, my = (y - pan.y) / zoom;
    const hits = cy.renderer().findNearestElements(mx, my, true, false);
    return hits.length > 0 && hits[0].id() === id;
  };
  for (let y = b.y1 + 25; y < b.y2 - 8; y += 4) {
    for (let x = b.x1 + 8; x < b.x2 - 8; x += 4) {
      if (clearOfKids(x, y) && onlyContainer(x, y)) return [x, y];
    }
  }
  return null;
}
"""


def test_canvas_gestures(fixture_page):
    snap = load_fixture()
    page = fixture_page
    path = "root-0/analyses/mfe_magnet_field.sysml"
    members = [c for c in calcs(snap) if c["source_file"] == path]
    assert len(members) >= 5
    page.click("[data-action=collapse-all]")
    container = container_id_for_path(page, path)

    # (1) Click a collapsed container: it expands.
    click_element_centre(page, container)
    assert not group_collapsed(page, path)

    # (2) Click a calc inside it: panel, selection, and the container stays expanded.
    target = members[0]["node_id"]
    click_calc_on_canvas(page, target)
    assert panel_node_id(page) == target
    assert selected_node_ids(page) == [target]
    assert not group_collapsed(page, path)
    assert page.evaluate(
        "k => window.modelVizApp.cy.getElementById(k).nonempty()", calc_key(page, target)
    )

    # (3) Click the container's own background, clear of every child: it collapses.
    point = page.evaluate(_CONTAINER_BACKGROUND_POINT_JS, container)
    assert point is not None, "no background point inside the expanded container"
    click_rendered_point(page, *point)
    assert group_collapsed(page, path)
    assert panel_node_id(page) == target, "the panel keeps showing the selection"


def test_search_box(fixture_page):
    snap = load_fixture()
    page = fixture_page
    target = calc_by_name(snap, "cas22_capital")["node_id"]
    page.click("[data-action=collapse-all]")
    assert group_collapsed(page, path_of(snap, target))
    page.fill("[data-role=search-input]", "cas22_capital")
    page.press("[data-role=search-input]", "Enter")
    assert_arrived(page, snap, target)

    page.fill("[data-role=search-input]", "no_such_calc_anywhere")
    page.press("[data-role=search-input]", "Enter")
    assert page.text_content("[data-role=search-status]") == "no calc matches"
    assert panel_node_id(page) == target

    assert not [c for c in calcs(snap) if c["display_name"].lower() == "capital"]
    several = [c for c in calcs(snap) if "capital" in c["display_name"].lower()]
    assert len(several) > 1
    page.fill("[data-role=search-input]", "capital")
    page.press("[data-role=search-input]", "Enter")
    assert page.text_content("[data-role=search-status]") == f"{len(several)} calcs match"
    assert panel_node_id(page) == target

    options = page.eval_on_selector_all("#calc-names option", "os => os.map(o => o.value)")
    assert sorted(options) == sorted(c["display_name"] for c in calcs(snap))


def test_navigate_unknown_key(fixture_page):
    page = fixture_page
    page.evaluate("() => window.modelVizApp.navigateTo('nope')")
    assert page.is_visible("[data-role=missing-calc]")
    assert "nope" in page.text_content("[data-role=missing-calc]")
    assert panel_node_id(page) is None
    assert selected_node_ids(page) == []


# --- Structure view: part gestures, cross-view links, part search (design D19, D21, D22) ---


def occurrence_at(snap, path: str) -> str:
    (found,) = [
        o["occurrence_id"]
        for o in occurrences(snap)
        if part_path_of(snap, o["occurrence_id"]) == path
    ]
    return found


def structure_state(page) -> dict:
    return page.evaluate("() => window.modelVizApp.state.structure")


def panel_part(page) -> str | None:
    return page.get_attribute("[data-role=panel]", "data-part-occurrence-id")


def selected_parts(page) -> list[str]:
    return page.evaluate(
        "() => window.modelVizApp.cy.nodes(':selected').map(n => n.data('occurrence_id'))"
    )


def box_inside_pane(page, element_id: str) -> bool:
    """The element's rendered box, label included, lies inside the graph pane."""
    box = rendered_box(page, element_id)
    width, height = pane_size(page)
    return box["x1"] >= 0 and box["y1"] >= 0 and box["x2"] <= width and box["y2"] <= height


def assert_part_arrived(page, occurrence_id: str) -> None:
    assert page.get_attribute("body", "data-view") == "structure"
    assert structure_state(page)["selected"] == occurrence_id
    assert panel_part(page) == occurrence_id
    assert selected_parts(page) == [occurrence_id]
    assert box_inside_pane(page, part_id_for_occurrence(page, occurrence_id))


def test_part_canvas_gestures(fixture_page):
    snap = load_fixture()
    page = fixture_page
    switch_view(page, "structure")
    root = occurrence_at(snap, "stellaris")
    magnet = occurrence_at(snap, "stellaris/magnet")
    coil = occurrence_at(snap, "stellaris/magnet/coil")

    # (1) The background of the expanded root: selected, panel open, nothing hidden or shown.
    visible = displayed_parts(page)
    point = page.evaluate(_CONTAINER_BACKGROUND_POINT_JS, part_id_for_occurrence(page, root))
    assert point is not None, "no background point inside the expanded root"
    click_rendered_point(page, *point)
    assert (structure_state(page)["selected"], panel_part(page)) == (root, root)
    assert displayed_parts(page) == visible

    # (2) Collapsed magnet: it expands and is selected.
    magnet_pid = part_id_for_occurrence(page, magnet)
    assert magnet_pid in structure_state(page)["collapsed"]
    click_element_centre(page, magnet_pid)
    assert magnet_pid not in structure_state(page)["collapsed"]
    assert (structure_state(page)["selected"], panel_part(page)) == (magnet, magnet)
    assert coil in {occ for occ, _parent in displayed_parts(page)}

    # (3) Leaf magnet/coil: its panel, and the visible set stays.
    visible = displayed_parts(page)
    click_element_centre(page, part_id_for_occurrence(page, coil))
    assert (structure_state(page)["selected"], panel_part(page)) == (coil, coil)
    assert page.text_content("[data-role=panel] [data-role=part-path]") == "stellaris/magnet/coil"
    assert displayed_parts(page) == visible
    assert page.query_selector("[data-role=panel] [data-action=toggle-part]") is None

    # (4) The panel's Collapse button on magnet collapses it and keeps it selected.
    page.evaluate("id => window.modelVizApp.showPart(id)", magnet)
    assert page.text_content("[data-action=toggle-part]") == "Collapse"
    page.click("[data-role=panel] [data-action=toggle-part]")
    assert magnet_pid in structure_state(page)["collapsed"]
    assert coil not in {occ for occ, _parent in displayed_parts(page)}
    assert (structure_state(page)["selected"], panel_part(page)) == (magnet, magnet)
    assert selected_parts(page) == [magnet]
    assert page.get_attribute("[data-action=toggle-part]", "data-part-collapsed") == "true"
    assert page.text_content("[data-action=toggle-part]") == "Expand"


def test_calc_link_from_part_panel(fixture_page):
    snap = load_fixture()
    page = fixture_page
    switch_view(page, "structure")
    page.evaluate("id => window.modelVizApp.showPart(id)", occurrence_at(snap, "stellaris/blanket"))
    link = page.query_selector("[data-section=part-calcs] [data-calc-key]")
    key = link.get_attribute("data-calc-key")
    node_id = page.evaluate("k => window.modelVizApp.model.byKey.get(k).nodeId", key)
    link.click()
    assert page.get_attribute("body", "data-view") == "calcs"
    assert page.evaluate("() => window.modelVizApp.state.selected") == key
    assert panel_node_id(page) == node_id
    assert selected_node_ids(page) == [node_id]
    assert fully_inside_pane(page, node_id)


_ROW_IN_PANEL_VIEW_JS = """id => {
  const panel = document.querySelector('[data-role=panel]');
  const row = [...panel.querySelectorAll('li[data-attr-node-id]')]
    .find(li => li.dataset.attrNodeId === id);
  const p = panel.getBoundingClientRect(), r = row.getBoundingClientRect();
  return r.top >= p.top && r.bottom <= p.bottom;
}"""


def attr_bound_row(snap, source_path: str, name: str) -> dict:
    (row,) = [r for r in attributes_of(snap, occurrence_at(snap, source_path)) if r["name"] == name]
    assert row["kind"] == "attr-bound"
    return row


def follow_attr_link(page, row: dict) -> None:
    page.click(f"li[data-attr-node-id={css_str(row['node_id'])}] [data-target-occurrence-id]")


def test_attribute_link_to_part(fixture_page):
    snap = load_fixture()
    page = fixture_page
    switch_view(page, "structure")
    magnet = occurrence_at(snap, "stellaris/magnet")
    magnet_pid = part_id_for_occurrence(page, magnet)
    page.click("[data-action=collapse-all]")

    # turbine.n_mod is bound to the root's n_mod; the root is drawn, collapsed, and stays so.
    page.evaluate("id => window.modelVizApp.showPart(id)", occurrence_at(snap, "stellaris/turbine"))
    row = attr_bound_row(snap, "stellaris/turbine", "n_mod")
    root = occurrence_at(snap, "stellaris")
    assert row["binding"]["target_occurrence_id"] == root
    follow_attr_link(page, row)
    assert_part_arrived(page, root)
    assert page.evaluate(_ROW_IN_PANEL_VIEW_JS, row["binding"]["target_attr_node_id"])

    # An attribute bound into collapsed magnet: navigation opens magnet (and nothing else).
    inside = [
        (path, r)
        for o in occurrences(snap)
        for path in [part_path_of(snap, o["occurrence_id"])]
        for r in attributes_of(snap, o["occurrence_id"])
        if r["kind"] == "attr-bound"
        and part_path_of(snap, r["binding"]["target_occurrence_id"]).startswith("stellaris/magnet/")
    ]
    assert inside, "the fixture binds an attribute into a magnet part"
    source_path, row = inside[0]
    page.click("[data-action=collapse-all]")
    page.evaluate("id => window.modelVizApp.showPart(id)", occurrence_at(snap, source_path))
    assert magnet_pid in structure_state(page)["collapsed"]
    follow_attr_link(page, row)
    assert_part_arrived(page, row["binding"]["target_occurrence_id"])
    assert magnet_pid not in structure_state(page)["collapsed"]
    assert page.evaluate(_ROW_IN_PANEL_VIEW_JS, row["binding"]["target_attr_node_id"])


def test_navigate_to_part_larger_than_pane(browser, fixture_path):
    """A part too big for the pane at zoom 1.0 is fitted, so its label shows (design § Navigation
    to a part)."""
    page, problems = open_viewer(browser, viewport={"width": 900, "height": 700})
    snap = load_fixture()
    assert load_snapshot(page, fixture_path) == "ready"
    switch_view(page, "structure")
    page.click("[data-action=expand-all]")
    root = occurrence_at(snap, "stellaris")
    root_pid = part_id_for_occurrence(page, root)
    box = page.evaluate("id => window.modelVizApp.cy.getElementById(id).boundingBox()", root_pid)
    assert box["w"] > pane_size(page)[0], "the root must be wider than the pane at zoom 1.0"
    page.evaluate("() => window.modelVizApp.cy.zoom(2)")
    page.evaluate("id => window.modelVizApp.navigateToPart(id)", root)
    assert_part_arrived(page, root)
    assert page.evaluate("() => window.modelVizApp.cy.zoom()") < 1.0
    page.close()
    problems.assert_clean()


def search(page, query: str) -> None:
    page.fill("[data-role=search-input]", query)
    page.press("[data-role=search-input]", "Enter")


def test_part_search(fixture_page):
    snap = load_fixture()
    page = fixture_page
    switch_view(page, "structure")
    magnet_pid = part_id_for_occurrence(page, occurrence_at(snap, "stellaris/magnet"))
    assert magnet_pid in structure_state(page)["collapsed"]

    search(page, "coil")
    coil = occurrence_at(snap, "stellaris/magnet/coil")
    assert page.text_content("[data-role=search-status]") == ""
    assert magnet_pid not in structure_state(page)["collapsed"]
    assert_part_arrived(page, coil)

    search(page, "nothing_here")
    assert page.text_content("[data-role=search-status]") == "no part matches"
    assert panel_part(page) == coil

    paths = [part_path_of(snap, o["occurrence_id"]) for o in occurrences(snap)]
    assert not [p for p in paths if p == "heat" or p.split("/")[-1] == "heat"]
    several = [p for p in paths if "heat" in p]
    assert len(several) > 1
    search(page, "HEAT")
    assert page.text_content("[data-role=search-status]") == f"{len(several)} parts match"
    assert panel_part(page) == coil


def test_navigate_part_unknown(fixture_page):
    page = fixture_page
    page.evaluate("() => window.modelVizApp.navigateToPart('nope')")
    assert page.get_attribute("body", "data-view") == "structure"
    assert page.is_visible("[data-role=missing-part]")
    assert "nope" in page.text_content("[data-role=missing-part]")
    assert panel_part(page) is None and panel_node_id(page) is None
    assert structure_state(page)["selected"] is None
    assert selected_parts(page) == []
