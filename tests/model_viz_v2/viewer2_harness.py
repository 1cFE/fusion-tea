"""Page helpers for the model viewer v2 tests: open the page, load a file, read what cy draws.

The name is unique across tests/ (design D43). v1's harness is imported as a namespace module,
never by bare name, so the two folders can collect together.

Identities (design § Validation Approach): a calc node is its node_id, a part node is
occ:<occurrence_id>, and the part node with a null occurrence_id is the literal unscoped.
"""

import hashlib
from pathlib import Path

from tests.model_viz import viewer_harness as v1_harness

REPO = Path(__file__).resolve().parents[2]
VIEWER2_HTML = REPO / "src/model_viz/viewer2/index.html"
V1_HTML = v1_harness.VIEWER_HTML
FIXTURE = REPO / "tests/model_viz/fixtures/stellarator.snapshot.json"
# Plan PD10: its own literal, asserted equal to v1's pin in test_harness_v2.py.
FIXTURE_SHA256 = "8e79aa4e489e7bcf1be8e24796a77a6df3acbbf8b327b3eb6b961e96b55bf9ae"
VIEWPORT = {"width": 1400, "height": 900}
INSTALL_HELP = v1_harness.INSTALL_HELP
TOLERANCE = 0.5

# A JS function body mapping a cy node to its test identity.
IDENTITY_JS = """n => n.data('kind') === 'calc' ? n.data('node_id')
  : (n.data('occurrence_id') === null ? 'unscoped' : 'occ:' + n.data('occurrence_id'))"""


def fixture_digest() -> str:
    return hashlib.sha256(FIXTURE.read_bytes()).hexdigest()


class PageProblemsV2:
    """Page errors, console errors, http(s) requests, and the warnings v2 polices (plan PD11):
    Cytoscape's "invalid endpoints" warning (an undrawn edge) and any style-mapping warning."""

    WARNING_MARKERS = ("invalid endpoints", "style", "mapping")

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
        elif msg.type == "warning" and any(m in msg.text.lower() for m in self.WARNING_MARKERS):
            self.items.append(f"console.warning: {msg.text}")

    def _on_request(self, request):
        if request.url.startswith(("http:", "https:")):
            self.items.append(f"network request: {request.url}")

    def assert_clean(self):
        assert not self.items, "viewer2 page problems:\n" + "\n".join(self.items)


def open_v2(browser):
    page = browser.new_page(viewport=VIEWPORT)
    page.set_default_timeout(15000)
    problems = PageProblemsV2(page)
    page.goto(VIEWER2_HTML.as_uri(), wait_until="load")
    page.wait_for_function("() => window.modelVizApp !== undefined", timeout=5000)
    return page, problems


def load_snapshot(page, path) -> str:
    """Pick a file through the real file input; return the page's load state afterwards."""
    seq = int(page.get_attribute("body", "data-load-seq"))
    page.set_input_files("input[type=file][data-role=snapshot-input]", str(path))
    page.wait_for_function("s => Number(document.body.dataset.loadSeq) > s", arg=seq)
    return page.get_attribute("body", "data-load-state")


def _eval_nodes(page, body: str):
    """Evaluate a JS body with cy and ident(n) in scope."""
    return page.evaluate(
        f"() => {{ const cy = window.modelVizApp.cy; const ident = {IDENTITY_JS}; {body} }}"
    )


def drawn_parts(page) -> dict[str, str | None]:
    """Part identity -> drawn parent's identity (None at the top)."""
    rows = _eval_nodes(
        page,
        """return cy.nodes('[kind="part"]').map(n =>
             [ident(n), n.parent().nonempty() ? ident(n.parent()) : null]);""",
    )
    return dict(rows)


def drawn_calcs(page) -> dict[str, str | None]:
    """Calc node_id -> drawn parent's identity."""
    rows = _eval_nodes(
        page,
        """return cy.nodes('[kind="calc"]').map(n =>
             [ident(n), n.parent().nonempty() ? ident(n.parent()) : null]);""",
    )
    return dict(rows)


def drawn_edges(page) -> list[tuple[str, str]]:
    rows = _eval_nodes(page, "return cy.edges().map(e => [ident(e.source()), ident(e.target())]);")
    return sorted(tuple(r) for r in rows)


def drawn_edge_weights(page) -> list[int]:
    return page.evaluate("() => window.modelVizApp.cy.edges().map(e => e.data('bindings').length)")


def drawn_labels(page) -> dict[str, str]:
    return dict(_eval_nodes(page, "return cy.nodes().map(n => [ident(n), n.data('label')]);"))


def node_id_of(page, ident: str) -> str:
    """The cy element id drawn for an identity."""
    ids = page.evaluate(
        f"""i => {{ const ident = {IDENTITY_JS};
             const nodes = window.modelVizApp.cy.nodes();
             return nodes.filter(n => ident(n) === i).map(n => n.id()); }}""",
        ident,
    )
    assert len(ids) == 1, f"expected one drawn node for {ident}, found {ids}"
    return ids[0]


def is_closed(page, ident: str) -> bool:
    return page.evaluate(
        "id => window.modelVizApp.cy.getElementById(id).data('collapsed')", node_id_of(page, ident)
    )


def toggle(page, ident: str) -> None:
    page.evaluate("id => window.modelVizApp.toggleContainer(id)", node_id_of(page, ident))


def selected(page):
    return page.evaluate("() => window.modelVizApp.state.selected")


def viewport(page) -> dict:
    vp = page.evaluate(
        "() => ({zoom: window.modelVizApp.cy.zoom(), pan: window.modelVizApp.cy.pan()})"
    )
    return {
        "zoom": round(vp["zoom"], 6),
        "pan": {"x": round(vp["pan"]["x"], 6), "y": round(vp["pan"]["y"], 6)},
    }


def _boxes(page, opts: str) -> dict[str, dict]:
    rows = _eval_nodes(
        page,
        f"""return cy.nodes().map(n => {{ const b = n.boundingBox({opts});
             const box = {{x1: b.x1, y1: b.y1, x2: b.x2, y2: b.y2, closed: !!n.data('collapsed')}};
             return [ident(n), box]; }});""",
    )
    return dict(rows)


def body_boxes(page) -> dict[str, dict]:
    """Identity -> drawn body box in model coordinates, labels and overlays excluded."""
    return _boxes(page, "{includeLabels: false, includeOverlays: false}")


def label_boxes(page) -> dict[str, dict]:
    """Identity -> label-inclusive box in model coordinates, overlays excluded (I26)."""
    return _boxes(page, "{includeLabels: true, includeOverlays: false}")


def click_rendered_point(page, x: float, y: float) -> None:
    """A real mouse click at a point in the graph pane's rendered coordinates."""
    width, height = page.evaluate(
        "() => [window.modelVizApp.cy.width(), window.modelVizApp.cy.height()]"
    )
    assert 0 < x < width and 0 < y < height, f"point ({x}, {y}) is outside the graph pane"
    box = page.locator("[data-role=graph-pane]").bounding_box()
    page.mouse.click(box["x"] + x, box["y"] + y)


def click_node(page, ident: str) -> None:
    """A real click at the centre of a node's rendered body."""
    box = page.evaluate(
        "id => window.modelVizApp.cy.getElementById(id)"
        ".renderedBoundingBox({includeLabels: false})",
        node_id_of(page, ident),
    )
    click_rendered_point(page, (box["x1"] + box["x2"]) / 2, (box["y1"] + box["y2"]) / 2)


_CLEAR_POINT_JS = """
  ([id, which]) => {
    const cy = window.modelVizApp.cy;
    const node = cy.getElementById(id);
    const b = which === 'label'
      ? node.boundingBox({includeNodes: false, includeEdges: false,
                          includeLabels: true, includeOverlays: false})
      : node.boundingBox({includeLabels: false, includeOverlays: false});
    const blocked = which === 'label' ? []
      : node.children().map(k => k.boundingBox({includeLabels: true, includeOverlays: false}));
    const segs = [];
    cy.edges().forEach(e => {
      const pts = [e.sourceEndpoint(), ...(e.segmentPoints() || []), e.targetEndpoint()];
      for (let i = 0; i + 1 < pts.length; i++) segs.push([pts[i], pts[i + 1]]);
    });
    const near = (x, y, [p, q]) => {
      const dx = q.x - p.x, dy = q.y - p.y, len = dx * dx + dy * dy;
      const dot = ((x - p.x) * dx + (y - p.y) * dy) / len;
      const t = len === 0 ? 0 : Math.max(0, Math.min(1, dot));
      return Math.hypot(x - (p.x + t * dx), y - (p.y + t * dy)) * cy.zoom() < 6;
    };
    const margin = which === 'label' ? 1 : 6;
    const step = Math.max(1, 2 / cy.zoom());
    const pan = cy.pan(), z = cy.zoom();
    for (let y = b.y1 + margin; y < b.y2 - margin; y += step) {
      for (let x = b.x1 + margin; x < b.x2 - margin; x += step) {
        const inBox = k => x > k.x1 - 3 && x < k.x2 + 3 && y > k.y1 - 3 && y < k.y2 + 3;
        if (blocked.some(inBox)) continue;
        if (segs.some(seg => near(x, y, seg))) continue;
        const rx = x * z + pan.x, ry = y * z + pan.y;
        if (rx <= 1 || ry <= 1 || rx >= cy.width() - 1 || ry >= cy.height() - 1) continue;
        return {x: rx, y: ry};
      }
    }
    return null;
  }
"""


def _click_clear_point(page, ident: str, which: str) -> None:
    """Click a point inside a node's label or body that no child box and no drawn edge covers, and
    that lies inside the pane. An edge running over a compound's label is what makes this needed."""
    point = page.evaluate(_CLEAR_POINT_JS, [node_id_of(page, ident), which])
    assert point is not None, f"no clear point in {ident}'s {which}"
    click_rendered_point(page, point["x"], point["y"])


def click_label(page, ident: str) -> None:
    """A real click on a node's label, clear of any edge drawn over it."""
    _click_clear_point(page, ident, "label")


def click_empty_part_area(page, ident: str) -> None:
    """A real click inside an open part's body where no child box, label or edge is drawn."""
    _click_clear_point(page, ident, "body")


# Edge occlusion (owner ruling 2026-09-15): with dagre and v1's straight edges an edge path is the
# segment from its source endpoint to its target endpoint, so this test is exact.
_EDGE_HIT_JS = """
  () => {
    const cy = window.modelVizApp.cy;
    function segHitsRect(x1, y1, x2, y2, r) {
      let t0 = 0, t1 = 1; const dx = x2 - x1, dy = y2 - y1;
      const clips = [[-dx, x1 - r.x1], [dx, r.x2 - x1], [-dy, y1 - r.y1], [dy, r.y2 - y1]];
      for (const [p, q] of clips) {
        if (p === 0) { if (q < 0) return false; }
        else { const t = q / p;
          if (p < 0) { if (t > t1) return false; if (t > t0) t0 = t; }
          else { if (t < t0) return false; if (t < t1) t1 = t; } }
      }
      return t1 - t0 > 1e-6;
    }
    const calcs = cy.nodes('[kind="calc"]').toArray();
    const bodyOpts = {includeLabels: false, includeOverlays: false};
    const boxes = new Map(calcs.map(n => [n.id(), n.boundingBox(bodyOpts)]));
    let count = 0;
    cy.edges().forEach(e => {
      const pts = [e.sourceEndpoint(), ...(e.segmentPoints() || []), e.targetEndpoint()];
      const hit = calcs.some(n => {
        if (n.same(e.source()) || n.same(e.target())) return false;
        const r = boxes.get(n.id());
        for (let i = 0; i + 1 < pts.length; i++)
          if (segHitsRect(pts[i].x, pts[i].y, pts[i + 1].x, pts[i + 1].y, r)) return true;
        return false;
      });
      if (hit) count++;
    });
    return count;
  }
"""

_CROSSINGS_JS = """
  () => {
    const cy = window.modelVizApp.cy;
    const paths = cy.edges().map(
      e => [e.sourceEndpoint(), ...(e.segmentPoints() || []), e.targetEndpoint()]);
    function crosses(a, b, c, d) {
      const s1x = b.x - a.x, s1y = b.y - a.y, s2x = d.x - c.x, s2y = d.y - c.y;
      const den = -s2x * s1y + s1x * s2y;
      if (den === 0) return false;
      const s = (-s1y * (a.x - c.x) + s1x * (a.y - c.y)) / den;
      const t = (s2x * (a.y - c.y) - s2y * (a.x - c.x)) / den;
      return s > 1e-6 && s < 1 - 1e-6 && t > 1e-6 && t < 1 - 1e-6;
    }
    let count = 0;
    for (let i = 0; i < paths.length; i++)
      for (let j = i + 1; j < paths.length; j++) {
        let hit = false;
        for (let a = 0; a + 1 < paths[i].length && !hit; a++)
          for (let b = 0; b + 1 < paths[j].length && !hit; b++)
            if (crosses(paths[i][a], paths[i][a + 1], paths[j][b], paths[j][b + 1])) hit = true;
        if (hit) count++;
      }
    return count;
  }
"""


def edges_behind_boxes(page) -> int:
    """Drawn edges whose path passes behind the body box of a calc that is not one of its
    endpoints. The spike measured v1's calc graph at 58 of 142 with the same code."""
    return page.evaluate(_EDGE_HIT_JS)


def crossings(page) -> int:
    """Pairs of drawn edges that cross. The spike measured v1's calc graph at 338."""
    return page.evaluate(_CROSSINGS_JS)


def backward_edges(page) -> list[tuple[str, str]]:
    """Drawn edges whose target box centre is not right of its source's (dagre draws none)."""
    rows = _eval_nodes(
        page,
        """const opts = {includeLabels: false, includeOverlays: false};
           return cy.edges().filter(e => {
             const s = e.source().boundingBox(opts), t = e.target().boundingBox(opts);
             return (s.x1 + s.x2) / 2 >= (t.x1 + t.x2) / 2 - 0.5;
           }).map(e => [ident(e.source()), ident(e.target())]);""",
    )
    return sorted(tuple(r) for r in rows)


OVERLAP = 0.5


def _drawn_ancestors(parents: dict[str, str | None]) -> dict[str, set[str]]:
    out = {}
    for ident in parents:
        found, current = set(), parents[ident]
        while current is not None:
            found.add(current)
            current = parents[current]
        out[ident] = found
    return out


def overlaps_and_outside(page) -> tuple[list[tuple[str, str]], list[str]]:
    """Pairs of drawn body boxes that overlap without one containing the other in the drawn tree,
    and children whose body box leaves their parent's body box.

    Body boxes, not label-inclusive ones: an open compound's label sits in the band above its body,
    outside it, exactly as v1 draws an expanded group, so a label-inclusive test would be wrong.
    """
    parents = {**drawn_parts(page), **drawn_calcs(page)}
    above = _drawn_ancestors(parents)
    boxes = body_boxes(page)
    bodies = boxes
    idents = sorted(boxes)
    overlaps = []
    for i, a in enumerate(idents):
        for b in idents[i + 1 :]:
            if a in above[b] or b in above[a]:
                continue
            A, B = boxes[a], boxes[b]
            dx = min(A["x2"], B["x2"]) - max(A["x1"], B["x1"])
            dy = min(A["y2"], B["y2"]) - max(A["y1"], B["y1"])
            if dx > OVERLAP and dy > OVERLAP:
                overlaps.append((a, b))
    outside = []
    for ident, parent in parents.items():
        if parent is None:
            continue
        C, P = boxes[ident], bodies[parent]
        if (
            C["x1"] < P["x1"] - OVERLAP
            or C["x2"] > P["x2"] + OVERLAP
            or C["y1"] < P["y1"] - OVERLAP
            or C["y2"] > P["y2"] + OVERLAP
        ):
            outside.append(ident)
    return overlaps, outside


# --- drag and spacing (owner additions 2026-09-15) ----------------------------------------------


def drag_node(page, ident: str, dx: float, dy: float) -> None:
    """A real mouse drag of a node's body by (dx, dy) rendered pixels."""
    box = page.evaluate(
        "id => window.modelVizApp.cy.getElementById(id)"
        ".renderedBoundingBox({includeLabels: false})",
        node_id_of(page, ident),
    )
    x, y = (box["x1"] + box["x2"]) / 2, (box["y1"] + box["y2"]) / 2
    pane = page.locator("[data-role=graph-pane]").bounding_box()
    page.mouse.move(pane["x"] + x, pane["y"] + y)
    page.mouse.down()
    page.mouse.move(pane["x"] + x + dx, pane["y"] + y + dy, steps=12)
    page.mouse.up()


def edge_endpoints(page) -> dict[tuple[str, str], tuple[float, float, float, float]]:
    """Each drawn edge's source and target endpoints in model coordinates."""
    rows = _eval_nodes(
        page,
        """return cy.edges().map(e => { const s = e.sourceEndpoint(), t = e.targetEndpoint();
             return [ident(e.source()), ident(e.target()), s.x, s.y, t.x, t.y]; });""",
    )
    return {(r[0], r[1]): (r[2], r[3], r[4], r[5]) for r in rows}


def spacing(page) -> float:
    return page.evaluate("() => window.modelVizApp.state.scale")


def set_spacing(page, value: float) -> None:
    """Move the Spacing range control the way a modeler does."""
    page.fill("[data-role=spacing]", str(value))


def reset_layout(page) -> None:
    page.click("[data-action=reset-layout]")


def drawn_calc_font(page) -> float:
    """cy zoom × the calc style font size, the text size the modeler sees (spec § Readability)."""
    return page.evaluate(
        """() => { const cy = window.modelVizApp.cy;
             return cy.zoom() * parseFloat(cy.nodes('[kind="calc"]')[0].style('font-size')); }"""
    )


# --- panels, Find, navigation (plan Phase 2) --------------------------------------------------


def open_v1(browser):
    """v1's page at v2's viewport, policed by v2's page problems (plan Phase 2 § conftest)."""
    page = browser.new_page(viewport=VIEWPORT)
    page.set_default_timeout(15000)
    problems = PageProblemsV2(page)
    page.goto(V1_HTML.as_uri(), wait_until="load")
    page.wait_for_function("() => window.modelVizApp !== undefined", timeout=5000)
    return page, problems


def calc_key(page, node_id: str) -> str:
    key = page.evaluate("id => window.modelVizApp.model.keyByNodeId.get(id)", node_id)
    assert key is not None, f"calc {node_id} is not in the loaded model"
    return key


def show_calc(page, node_id: str) -> None:
    page.evaluate("key => window.modelVizApp.showCalc(key)", calc_key(page, node_id))


def show_part(page, occurrence_id: str | None) -> None:
    page.evaluate("occ => window.modelVizApp.showPart(occ)", occurrence_id)


def panel_calc_node_id(page) -> str | None:
    return page.get_attribute("[data-role=panel]", "data-calc-node-id")


def panel_part(page) -> str | None:
    return page.get_attribute("[data-role=panel]", "data-part-occurrence-id")


def panel_placeholder(page) -> str | None:
    return page.text_content("[data-role=panel] p.placeholder")


def panel_toggle(page) -> dict | None:
    """The panel's Collapse/Expand button: its word and data-part-collapsed, or None."""
    return page.evaluate(
        """() => {
             const b = document.querySelector('[data-role=panel] button[data-action=toggle-part]');
             if (b === null) return null;
             return {text: b.textContent, collapsed: b.dataset.partCollapsed}; }"""
    )


def has_clear_control(page) -> bool:
    return page.query_selector("[data-role=panel] [data-action=clear-selection]") is not None


def search(page, query: str) -> None:
    """Type into the Find box and press Enter."""
    page.fill("[data-role=search-input]", query)
    page.press("[data-role=search-input]", "Enter")


def search_status(page) -> str:
    return page.text_content("[data-role=search-status]")


def css_str(value: str) -> str:
    """Quote a raw string for a CSS attribute selector value."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def collapsed_occurrences(page) -> set[str]:
    return set(page.evaluate("() => window.modelVizApp.state.collapsedOccurrences"))


def rendered_centre_offset(page, ident: str) -> tuple[float, float]:
    """How far a node's rendered body centre is from the graph pane's centre, in pixels."""
    return tuple(
        page.evaluate(
            """id => { const cy = window.modelVizApp.cy;
                 const opts = {includeLabels: false, includeOverlays: false};
                 const b = cy.getElementById(id).renderedBoundingBox(opts);
                 return [(b.x1 + b.x2) / 2 - cy.width() / 2,
                         (b.y1 + b.y2) / 2 - cy.height() / 2]; }""",
            node_id_of(page, ident),
        )
    )


def focus(page, ident: str) -> None:
    """Centre a node in the pane at zoom >= 1, as v1's focusNode does, so a real click lands on a
    readable box instead of on a 4 px sliver of the fitted picture."""
    page.evaluate(
        """id => { const cy = window.modelVizApp.cy;
             cy.zoom(Math.max(cy.zoom(), 1.0)); cy.center(cy.getElementById(id)); }""",
        node_id_of(page, ident),
    )


def fits_pane(page, ident: str, level: float) -> bool:
    """Whether the node's box, labels included, would fit in the pane at a zoom (v1's fitsPane)."""
    return page.evaluate(
        """([id, z]) => { const cy = window.modelVizApp.cy;
             const b = cy.getElementById(id).boundingBox();
             return b.w * z <= cy.width() && b.h * z <= cy.height(); }""",
        [node_id_of(page, ident), level],
    )


def fully_inside_pane(page, ident: str) -> bool:
    """v1's navigation check (tests/model_viz/test_navigation.py): the node's rendered box, labels
    included, lies wholly inside the graph pane."""
    box = page.evaluate(
        "id => window.modelVizApp.cy.getElementById(id).renderedBoundingBox()",
        node_id_of(page, ident),
    )
    width, height = page.evaluate(
        "() => [window.modelVizApp.cy.width(), window.modelVizApp.cy.height()]"
    )
    return box["x1"] >= 0 and box["y1"] >= 0 and box["x2"] <= width and box["y2"] <= height


def zoom(page) -> float:
    return page.evaluate("() => window.modelVizApp.cy.zoom()")


def set_zoom(page, level: float) -> None:
    """Set cy's zoom, discarding the return value.

    The braces matter. ``cy.zoom(level)`` returns the Cytoscape core for chaining, and an arrow
    function that returns it makes Playwright serialise the whole core object graph: ~10 s and a
    multi-gigabyte renderer allocation per call. The void form costs ~0.05 s.
    """
    page.evaluate("z => { window.modelVizApp.cy.zoom(z); }", level)


# --- reach classes (plan Phase 3) --------------------------------------------------------------

_CLASS_JS = """const cls = e => {
  const names = e.classes().filter(c => c.startsWith('mv-') && c !== 'mv-selected');
  if (names.length > 1) throw new Error('more than one reach class on ' + e.id());
  return names.length === 0 ? null : names[0]; };"""


def drawn_classes(page) -> dict:
    """What the page draws, in the oracle's shape: {"nodes": identity -> reach class or None,
    "edges": (source, target) -> class, "selected": the identity carrying mv-selected}."""
    out = _eval_nodes(
        page,
        f"""{_CLASS_JS}
            const marked = cy.elements('.mv-selected').map(e => ident(e));
            return {{
              nodes: cy.nodes().map(n => [ident(n), cls(n)]),
              edges: cy.edges().map(e => [ident(e.source()), ident(e.target()), cls(e)]),
              selected: marked,
            }};""",
    )
    assert len(out["selected"]) <= 1, f"more than one selected element: {out['selected']}"
    return {
        "nodes": dict(out["nodes"]),
        "edges": {(row[0], row[1]): row[2] for row in out["edges"]},
        "selected": out["selected"][0] if out["selected"] else None,
    }


def reach_section(page) -> dict:
    """The panel's reach section: each direction's heading count and its groups (D38, A9)."""
    return page.evaluate(
        """() => {
             const section = document.querySelector(
               '[data-role=panel] section[data-section=reach]');
             if (section === null) return null;
             const read = (name) => {
               const box = section.querySelector(`[data-reach=${name}]`);
               const heading = box.querySelector('.reach-heading');
               return {
                 heading: heading.textContent,
                 colour: getComputedStyle(heading).color,
                 groups: [...box.querySelectorAll('.reach-group')].map(group => ({
                   path: group.dataset.partPath,
                   calcs: [...group.querySelectorAll('button.calc-link[data-calc-key]')]
                     .map(link => link.textContent),
                 })),
               };
             };
             return {upstream: read('upstream'), downstream: read('downstream')};
           }"""
    )
