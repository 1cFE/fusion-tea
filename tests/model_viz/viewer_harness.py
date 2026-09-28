"""Page helpers for the model-viz viewer tests: open the page, load a file, drive the app.

Kept out of conftest.py because tests/ holds several conftest modules and a test cannot import
"conftest" by name without ambiguity. The name is unique across tests/ (namespace tree).
"""

import hashlib
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
VIEWER_HTML = REPO / "src/model_viz/viewer/index.html"
FIXTURE = REPO / "tests/model_viz/fixtures/stellarator.snapshot.json"
FIXTURE_SHA256 = "8e79aa4e489e7bcf1be8e24796a77a6df3acbbf8b327b3eb6b961e96b55bf9ae"  # WI-057 (2026-09-13): the nested snapshot, re-applied onto feat/demo-maturation
INSTALL_HELP = (
    "The model_viz tests need Playwright and Chromium. Install them with:\n"
    "  uv sync --extra e2e\n"
    "  uv run playwright install chromium"
)


def fixture_digest() -> str:
    return hashlib.sha256(FIXTURE.read_bytes()).hexdigest()


class PageProblems:
    """Collects page errors, console errors and http(s) requests from one page (plan PD7)."""

    def __init__(self, page):
        self.items: list[str] = []
        page.on("pageerror", self._on_page_error)
        page.on("console", self._on_console)
        page.on("request", self._on_request)

    def _on_page_error(self, err):
        self.items.append(f"page error: {err}")

    def _on_console(self, msg):
        if msg.type == "error":
            self.items.append(f"console.error: {msg.text}")

    def _on_request(self, request):
        if request.url.startswith(("http:", "https:")):
            self.items.append(f"network request: {request.url}")

    def assert_clean(self):
        assert not self.items, "viewer page problems:\n" + "\n".join(self.items)


def open_viewer(browser, viewport=None):
    page = browser.new_page(viewport=viewport or {"width": 1600, "height": 1000})
    problems = PageProblems(page)
    page.goto(VIEWER_HTML.as_uri(), wait_until="load")
    page.wait_for_function("() => window.modelVizApp !== undefined")
    return page, problems


def load_snapshot(page, path) -> str:
    """Pick a file through the real file input; return the page's load state afterwards."""
    seq = int(page.get_attribute("body", "data-load-seq"))
    page.set_input_files("input[type=file][data-role=snapshot-input]", str(path))
    page.wait_for_function("s => Number(document.body.dataset.loadSeq) > s", arg=seq)
    return page.get_attribute("body", "data-load-state")


def calc_key(page, node_id: str) -> str:
    key = page.evaluate("id => window.modelVizApp.model.keyByNodeId.get(id)", node_id)
    assert key is not None, f"calc {node_id} is not in the loaded model"
    return key


def show_calc(page, node_id: str) -> None:
    page.evaluate("key => window.modelVizApp.showCalc(key)", calc_key(page, node_id))


def calc_node_count(page) -> int:
    return page.evaluate("() => window.modelVizApp.cy.nodes('[kind=\"calc\"]').length")


def container_id_for_path(page, path: str) -> str:
    """The container drawn for a source-file group path (reads cy only to find the id)."""
    ids = page.evaluate(
        """p => window.modelVizApp.cy.nodes('[kind="container"]')
             .filter(n => n.data('group_path') === p).map(n => n.id())""",
        path,
    )
    assert len(ids) == 1, f"expected one container for {path}, found {ids}"
    return ids[0]


def toggle_group(page, path: str) -> None:
    page.evaluate("id => window.modelVizApp.toggleContainer(id)", container_id_for_path(page, path))


def group_collapsed(page, path: str) -> bool:
    cid = container_id_for_path(page, path)
    return page.evaluate("id => window.modelVizApp.cy.getElementById(id).data('collapsed')", cid)


def selected_node_ids(page) -> list[str]:
    return page.evaluate(
        "() => window.modelVizApp.cy.nodes(':selected').map(n => n.data('node_id'))"
    )


def panel_node_id(page) -> str | None:
    return page.get_attribute("[data-role=panel]", "data-calc-node-id")


def css_str(value: str) -> str:
    """Quote a raw string for a CSS attribute selector value."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def switch_view(page, view: str) -> None:
    """Switch views through the real View select."""
    page.select_option("[data-role=view-select]", view)


def part_id_for_occurrence(page, occurrence_id: str) -> str:
    """The part node drawn for an occurrence id (reads cy only to find the id)."""
    ids = page.evaluate(
        """occ => window.modelVizApp.cy.nodes('[kind="part"]')
             .filter(n => n.data('occurrence_id') === occ).map(n => n.id())""",
        occurrence_id,
    )
    assert len(ids) == 1, f"expected one drawn part for {occurrence_id}, found {ids}"
    return ids[0]


def toggle_part(page, occurrence_id: str) -> None:
    part_id = part_id_for_occurrence(page, occurrence_id)
    page.evaluate("id => window.modelVizApp.toggleContainer(id)", part_id)


def click_rendered_point(page, x: float, y: float) -> None:
    """A real mouse click at a point in the graph pane's rendered coordinates."""
    width, height = page.evaluate(
        "() => [window.modelVizApp.cy.width(), window.modelVizApp.cy.height()]"
    )
    assert 0 < x < width and 0 < y < height, f"point ({x}, {y}) is outside the graph pane"
    box = page.locator("[data-role=graph-pane]").bounding_box()
    page.mouse.click(box["x"] + x, box["y"] + y)


def click_element_centre(page, element_id: str) -> None:
    box = page.evaluate(
        "id => window.modelVizApp.cy.getElementById(id).renderedBoundingBox()", element_id
    )
    click_rendered_point(page, (box["x1"] + box["x2"]) / 2, (box["y1"] + box["y2"]) / 2)


def view_geometry(page) -> dict:
    """Zoom, pan and every drawn non-compound node's model position, read from cy.

    Compound nodes are left out: layout never places them. Cytoscape derives a compound's centre
    from its children's boxes, so a selection border on a child shifts it by a fraction of a pixel
    although nothing was laid out.
    """
    return page.evaluate(
        """() => {
             const cy = window.modelVizApp.cy;
             const positions = {};
             cy.nodes().filter(n => !n.isParent())
               .forEach(n => { positions[n.id()] = n.position(); });
             return {zoom: cy.zoom(), pan: cy.pan(), positions};
           }"""
    )
