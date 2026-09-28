// Shell: the Cytoscape instance for v2's one picture. Lays the picture out with dagre, left to
// right, on v1's constants and v1's edge look, and re-runs that layout on every redraw.
//
// Owner ruling 2026-09-15: "I think the v1_dagre_fit is the best. the right angle arrows just get
// lost no matter what -- really hard to see anything. the dagre has clear patterns your eyes can
// follow." The band packer, the pinned rooms and the taxi routing that stood here are retired; the
// layout is now v1's dagre and nothing about the picture's geometry is pinned.
window.ModelViz = window.ModelViz || {};

ModelViz.graph2 = (function () {
  // v1's calc-graph layout (src/model_viz/viewer/js/graph.js): dagre LR at its constants, fitting
  // after every run. Spacing multiplies the two separations and nothing else.
  const LAYOUT = { name: "dagre", rankDir: "LR", nodeSep: 20, rankSep: 60, edgeSep: 5, padding: 20, animate: false, fit: true };
  const FIT_PADDING = LAYOUT.padding;

  // Box text. Calc boxes carry two lines (name, module tag), so they are taller than v1's one-line
  // calc boxes; everything else is v1's calc-graph stylesheet.
  const CALC_FONT_PX = 10;
  const CALC_LINE_H = 11;
  const PART_FONT_PX = 12;
  const PART_LINE_H = 16;
  const PARENT_PAD = 12;
  // One font family for the stylesheet and any measurement (B3): Cytoscape's default.
  const FONT_FAMILY = "Helvetica Neue, Helvetica, sans-serif";

  // D37's reach colours; the panel's Upstream and Downstream headings carry them as the key (A9).
  const UP = "#1971c2";
  const DOWN = "#2f9e44";
  const BOTH = "#9c36b5";
  // v1 draws its edges at #999999; a shade darker so a thin line still reads over the pale fills.
  const EDGE_LINE = "#8a8a8a";

  const lines = (ele) => ele.data("label").split("\n");

  function labelWidth(ele, charWidth, minimum) {
    return Math.max(minimum, Math.max(...lines(ele).map((line) => line.length)) * charWidth + 16);
  }

  const STYLE = [
    {
      selector: "node[kind='calc']",
      style: {
        shape: "round-rectangle",
        label: "data(label)",
        "font-family": FONT_FAMILY,
        "font-size": CALC_FONT_PX,
        "line-height": CALC_LINE_H / CALC_FONT_PX,
        "text-wrap": "wrap",
        "text-valign": "center",
        "text-halign": "center",
        width: (ele) => labelWidth(ele, 6, 40),
        height: (ele) => lines(ele).length * CALC_LINE_H + 8,
        "background-color": "data(fill)",
        "border-color": "#666666",
        "border-width": 1,
      },
    },
    {
      // A closed part, or a part that owns no calc and has no children: one leaf box.
      selector: "node[kind='part']",
      style: {
        shape: "round-rectangle",
        label: "data(label)",
        "font-family": FONT_FAMILY,
        "font-size": PART_FONT_PX,
        "line-height": PART_LINE_H / PART_FONT_PX,
        "text-wrap": "wrap",
        "text-valign": "center",
        "text-halign": "center",
        "text-events": "yes",
        width: (ele) => labelWidth(ele, 7, 60),
        height: (ele) => lines(ele).length * PART_LINE_H + 12,
        "background-color": "#eef3f8",
        "border-color": "#5b7db1",
        "border-width": 1.5,
      },
    },
    {
      // An open part: a compound whose size Cytoscape derives from its children, as v1 draws an
      // expanded group. The label sits in the band above the body.
      selector: "node[kind='part']:parent",
      style: {
        "text-valign": "top",
        "text-margin-y": -2,
        "font-weight": "bold",
        "background-color": "#f7f9fc",
        "background-opacity": 1,
        padding: PARENT_PAD,
      },
    },
    { selector: "node[kind='part'][?collapsed]", style: { "background-color": "#dfe7f1", "border-style": "dashed" } },
    {
      // v1's edge look: a straight line (a lone bezier between two boxes is straight), the same
      // triangle arrowhead at 0.8 scale, and v1's width from the merged binding count.
      selector: "edge",
      style: {
        width: (ele) => Math.min(1 + 0.75 * (ele.data("weight") - 1), 5),
        "line-color": EDGE_LINE,
        "target-arrow-color": EDGE_LINE,
        "target-arrow-shape": "triangle",
        "arrow-scale": 0.8,
        "curve-style": "bezier",
      },
    },
    // Reach (D37) and selection: colour, opacity, overlay and z-index only, never a size (I27).
    { selector: "node.mv-upstream", style: { "border-color": UP, "z-index": 5 } },
    { selector: "node.mv-downstream", style: { "border-color": DOWN, "z-index": 5 } },
    { selector: "node.mv-both", style: { "border-color": BOTH, "z-index": 5 } },
    { selector: "node.mv-member", style: { "border-color": "#495057", "z-index": 5 } },
    { selector: "node.mv-dim", style: { opacity: 0.2, "z-index": 0 } },
    { selector: "node.mv-selected", style: { "border-color": "#d9480f", "overlay-color": "#d9480f", "overlay-opacity": 0.12, "overlay-padding": 3, "z-index": 20 } },
    // After the base edge rule: Cytoscape's later rule wins, so these must follow it.
    { selector: "edge.mv-upstream", style: { "line-color": UP, "target-arrow-color": UP, "z-index": 10 } },
    { selector: "edge.mv-downstream", style: { "line-color": DOWN, "target-arrow-color": DOWN, "z-index": 10 } },
    { selector: "edge.mv-both", style: { "line-color": BOTH, "target-arrow-color": BOTH, "z-index": 10 } },
    { selector: "edge.mv-dim", style: { opacity: 0.12, "z-index": 0 } },
  ];

  const CLASS_NAMES = "mv-upstream mv-downstream mv-both mv-member mv-dim mv-selected";

  // handlers: { onCalcTap(key), onPartTap(partId), onBackgroundTap() }
  function create(containerElement, handlers) {
    const cy = cytoscape({
      container: containerElement,
      elements: [],
      style: STYLE,
      layout: { name: "preset" },
      minZoom: 0.05,
      maxZoom: 4,
      boxSelectionEnabled: false,
      // Boxes are draggable. A drag is the modeler's explicit act; the next layout run replaces it.
      autoungrabify: false,
    });

    // Taps bubble from a calc to its compound parents; dispatch once, on the tapped element only.
    cy.on("tap", (evt) => {
      const target = evt.target;
      if (target === cy) handlers.onBackgroundTap();
      else if (target.isNode() && target.data("kind") === "calc") handlers.onCalcTap(target.id());
      else if (target.isNode() && target.data("kind") === "part") handlers.onPartTap(target.id());
    });
    cy.on("mouseover", "node[kind='part']", (evt) => {
      containerElement.title = evt.target.data("path");
    });
    cy.on("mouseover", "node[kind='calc']", (evt) => {
      containerElement.title = evt.target.data("source_file") || "no source file recorded";
    });
    cy.on("mouseout", "node", () => {
      containerElement.title = "";
    });
    window.addEventListener("resize", () => cy.resize());

    // Replace the drawn elements and re-run the layout, as v1 does after every collapse change.
    // `scale` multiplies dagre's node and rank separations (the Spacing control).
    function render(elements, scale) {
      cy.batch(() => {
        cy.elements().remove();
        cy.add(elements);
      });
      if (elements.length === 0) return;
      const factor = scale === undefined ? 1 : scale;
      cy.layout({ ...LAYOUT, nodeSep: LAYOUT.nodeSep * factor, rankSep: LAYOUT.rankSep * factor }).run();
    }

    // D37, I28: replace every reach class, then mark the selection (or its representative).
    function applyClasses(classMap, selectedId) {
      cy.batch(() => {
        cy.elements().removeClass(CLASS_NAMES);
        for (const [id, name] of classMap) cy.getElementById(id).addClass(name);
        if (selectedId !== null) cy.getElementById(selectedId).addClass("mv-selected");
      });
    }

    function drawnNode(id) {
      const node = cy.getElementById(id);
      if (node.empty()) throw new Error(`Node ${id} is not drawn.`);
      return node;
    }

    // Whether a node's box, labels included, fits inside the pane at a zoom (v1's fitsPane).
    function fitsPane(id, zoomLevel) {
      const box = drawnNode(id).boundingBox();
      return box.w * zoomLevel <= cy.width() && box.h * zoomLevel <= cy.height();
    }

    // v1's focus rule (graph.js focusNode): zoom to at least 1.0 and centre the node in the pane.
    function focusNode(id) {
      const node = drawnNode(id);
      cy.zoom(Math.max(cy.zoom(), 1.0));
      cy.center(node);
    }

    function fitNode(id) {
      cy.fit(drawnNode(id), FIT_PADDING);
    }

    // v1's navigation viewport rule (app.js navigateToPart): centre at zoom >= 1, or fit the box
    // when it is too big for the pane at that zoom.
    function revealNode(id) {
      if (fitsPane(id, Math.max(cy.zoom(), 1.0))) focusNode(id);
      else fitNode(id);
    }

    function fit() {
      cy.fit(undefined, FIT_PADDING);
    }

    return { cy, render, applyClasses, fitsPane, focusNode, fitNode, revealNode, fit };
  }

  return { LAYOUT, FIT_PADDING, CALC_FONT_PX, FONT_FAMILY, COLOURS: { UP, DOWN, BOTH }, create };
})();
