"""Navigation criteria N1–N2, the search box, and real canvas clicks (P1's "clicking a calc node").

Panel links, the search box and the canvas are driven with real Playwright input. Expected
targets and groups come from the raw snapshot.
"""

from edge_oracle import calc_by_name, calcs, load_fixture, path_of, producer_bindings
from viewer_harness import (
    calc_key,
    container_id_for_path,
    css_str,
    group_collapsed,
    panel_node_id,
    selected_node_ids,
    show_calc,
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
