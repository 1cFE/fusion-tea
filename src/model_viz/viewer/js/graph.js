// Shell: the Cytoscape instance. Draws what the view function returns; holds no viewer state.
window.ModelViz = window.ModelViz || {};

ModelViz.graph = (function () {
  const LAYOUT = { name: "dagre", rankDir: "LR", nodeSep: 20, rankSep: 60, edgeSep: 5, padding: 20, animate: false, fit: true };
  const HIGHLIGHT = "#d9480f";
  const PART = ModelViz.structure.constants;

  function labelWidth(ele, charWidth, minimum) {
    return Math.max(minimum, ele.data("label").length * charWidth + 16);
  }

  const STYLE = [
    {
      selector: "node[kind='calc']",
      style: {
        shape: "round-rectangle",
        label: "data(label)",
        "font-size": 10,
        "text-valign": "center",
        "text-halign": "center",
        width: (ele) => labelWidth(ele, 6, 40),
        height: 22,
        "background-color": "#ffffff",
        "border-color": "#666666",
        "border-width": 1,
      },
    },
    {
      selector: "node[kind='container']",
      style: {
        shape: "round-rectangle",
        label: "data(label)",
        "font-size": 12,
        "font-weight": "bold",
        "text-valign": "top",
        "text-halign": "center",
        "background-color": "#eaf1fb",
        "border-color": "#4a78b5",
        "border-width": 1.5,
        "border-style": "solid",
        padding: 12,
      },
    },
    { selector: "node[kind='container'][container_kind='design']", style: { "background-color": "#fbf1e6", "border-color": "#b5793a", "border-style": "dashed" } },
    {
      selector: "node[kind='container'][container_kind='ungrouped'], node[kind='container'][container_kind='unscoped']",
      style: { "background-color": "#f3f3f3", "border-color": "#888888", "border-style": "dotted" },
    },
    {
      selector: "node[kind='container'][?collapsed]",
      style: { "text-valign": "center", "font-size": 11, width: (ele) => labelWidth(ele, 7, 60), height: 34 },
    },
    {
      selector: "edge",
      style: {
        width: (ele) => Math.min(1 + 0.75 * (ele.data("weight") - 1), 5),
        "line-color": "#999999",
        "target-arrow-color": "#999999",
        "target-arrow-shape": "triangle",
        "arrow-scale": 0.8,
        "curve-style": "bezier",
      },
    },
    {
      selector: "node[kind='part']",
      style: {
        shape: "round-rectangle",
        label: "data(label)",
        "font-size": PART.FONT_PX,
        "line-height": PART.LINE_H / PART.FONT_PX,
        "text-wrap": "wrap",
        "text-valign": "center",
        "text-halign": "center",
        "background-color": "#eef3f8",
        "border-color": "#5b7db1",
        "border-width": 1,
      },
    },
    // Box sizes come from structure.js on element data (D26); compound parts carry none (PD9).
    { selector: "node[kind='part'][width]", style: { width: "data(width)", height: "data(height)" } },
    {
      selector: "node[kind='part']:parent",
      style: {
        "text-valign": "top",
        // Lift the label by the clearance LABEL_BAND reserves above the two label lines.
        "text-margin-y": -(PART.LABEL_BAND - PART.LINES * PART.LINE_H),
        "background-color": "#f7f9fc",
        "background-opacity": 1,
        "border-width": 1.5,
        padding: PART.PARENT_PAD,
      },
    },
    { selector: "node[kind='part'][?collapsed]", style: { "background-color": "#dfe7f1", "border-style": "dashed" } },
    { selector: "node[kind='calc']:selected, node[kind='part']:selected", style: { "border-color": HIGHLIGHT, "border-width": 3 } },
    { selector: "node.mv-neighbour", style: { "border-color": HIGHLIGHT, "border-width": 2 } },
    { selector: "edge.mv-highlight", style: { "line-color": HIGHLIGHT, "target-arrow-color": HIGHLIGHT } },
  ];

  // handlers: { onCalcTap(key), onContainerTap(containerId), onPartTap(partId) }
  function create(containerElement, handlers) {
    const cy = cytoscape({
      container: containerElement,
      elements: [],
      style: STYLE,
      layout: { name: "preset" },
      minZoom: 0.05,
      maxZoom: 4,
      boxSelectionEnabled: false,
    });

    // Taps bubble from a calc to its compound parent; dispatch once on the tapped element only.
    cy.on("tap", (evt) => {
      const target = evt.target;
      if (target === cy || !target.isNode()) return;
      const kind = target.data("kind");
      if (kind === "calc") handlers.onCalcTap(target.id());
      else if (kind === "part") handlers.onPartTap(target.id());
      else handlers.onContainerTap(target.id());
    });

    cy.on("mouseover", "node[kind='container']", (evt) => {
      const data = evt.target.data();
      containerElement.title = data.mode === "source" ? data.group_path || "no source file recorded" : data.occurrence_id || "no occurrence recorded";
    });
    cy.on("mouseover", "node[kind='part']", (evt) => {
      containerElement.title = evt.target.data("path");
    });
    cy.on("mouseout", "node[kind='container'], node[kind='part']", () => {
      containerElement.title = "";
    });
    window.addEventListener("resize", () => cy.resize());

    // opts.layout: a Cytoscape layout; the calc view's dagre layout when omitted (D26).
    function render(elements, opts) {
      const layout = opts === undefined ? LAYOUT : opts.layout;
      cy.batch(() => {
        cy.elements().remove();
        cy.add(elements);
      });
      if (elements.length > 0) cy.layout(layout).run();
    }

    function clearSelection() {
      const all = cy.elements();
      all.selectify();
      all.unselect();
      all.removeClass("mv-neighbour mv-highlight");
      all.unselectify();
    }

    // Mark one node selected and highlight its visible edges and their other ends.
    // A node inside a collapsed container is not drawn, so nothing is marked.
    function selectNode(id) {
      clearSelection();
      const all = cy.elements();
      all.selectify();
      const node = cy.getElementById(id);
      if (node.nonempty()) {
        node.select();
        const edges = node.connectedEdges();
        edges.addClass("mv-highlight");
        edges.connectedNodes().difference(node).addClass("mv-neighbour");
      }
      all.unselectify();
    }

    // Zoom to at least 1.0 and centre the node in the pane (design D6, same tick, no animation).
    function focusNode(id) {
      const node = cy.getElementById(id);
      if (node.empty()) throw new Error(`Node ${id} is not drawn, so it cannot be centred.`);
      cy.zoom(Math.max(cy.zoom(), 1.0));
      cy.center(node);
    }

    // Whether the node's box, labels included, fits inside the pane at a zoom.
    function fitsPane(id, zoom) {
      const box = drawnNode(id).boundingBox();
      return box.w * zoom <= cy.width() && box.h * zoom <= cy.height();
    }

    // Fit the view to one node, labels included.
    function fitNode(id) {
      cy.fit(drawnNode(id), LAYOUT.padding);
    }

    function drawnNode(id) {
      const node = cy.getElementById(id);
      if (node.empty()) throw new Error(`Node ${id} is not drawn.`);
      return node;
    }

    function fit() {
      cy.fit(undefined, LAYOUT.padding);
    }

    return { cy, render, clearSelection, selectNode, focusNode, fitsPane, fitNode, fit };
  }

  return { create };
})();
