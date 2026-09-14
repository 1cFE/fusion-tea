// Shell: the Cytoscape instance. Draws what the view function returns; holds no viewer state.
window.ModelViz = window.ModelViz || {};

ModelViz.graph = (function () {
  const LAYOUT = { name: "dagre", rankDir: "LR", nodeSep: 20, rankSep: 60, edgeSep: 5, padding: 20, animate: false, fit: true };
  const HIGHLIGHT = "#d9480f";

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
    { selector: "node[kind='calc']:selected", style: { "border-color": HIGHLIGHT, "border-width": 3 } },
    { selector: "node.mv-neighbour", style: { "border-color": HIGHLIGHT, "border-width": 2 } },
    { selector: "edge.mv-highlight", style: { "line-color": HIGHLIGHT, "target-arrow-color": HIGHLIGHT } },
  ];

  // handlers: { onCalcTap(key), onContainerTap(containerId) }
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
      if (target.data("kind") === "calc") handlers.onCalcTap(target.id());
      else handlers.onContainerTap(target.id());
    });

    cy.on("mouseover", "node[kind='container']", (evt) => {
      const data = evt.target.data();
      containerElement.title = data.mode === "source" ? data.group_path || "no source file recorded" : data.occurrence_id || "no occurrence recorded";
    });
    cy.on("mouseout", "node[kind='container']", () => {
      containerElement.title = "";
    });
    window.addEventListener("resize", () => cy.resize());

    function render(elements) {
      cy.batch(() => {
        cy.elements().remove();
        cy.add(elements);
      });
      if (elements.length > 0) cy.layout(LAYOUT).run();
    }

    function clearSelection() {
      const all = cy.elements();
      all.selectify();
      all.unselect();
      all.removeClass("mv-neighbour mv-highlight");
      all.unselectify();
    }

    // Mark one calc selected and highlight its visible edges and their other ends.
    // A calc inside a collapsed container is not drawn, so nothing is marked.
    function selectCalc(key) {
      clearSelection();
      const all = cy.elements();
      all.selectify();
      const node = cy.getElementById(key);
      if (node.nonempty()) {
        node.select();
        const edges = node.connectedEdges();
        edges.addClass("mv-highlight");
        edges.connectedNodes().difference(node).addClass("mv-neighbour");
      }
      all.unselectify();
    }

    // Zoom to at least 1.0 and centre the calc in the pane (design D6, same tick, no animation).
    function focusCalc(key) {
      const node = cy.getElementById(key);
      if (node.empty()) throw new Error(`Calc ${key} is not drawn, so it cannot be centred.`);
      cy.zoom(Math.max(cy.zoom(), 1.0));
      cy.center(node);
    }

    function fit() {
      cy.fit(undefined, LAYOUT.padding);
    }

    return { cy, render, clearSelection, selectCalc, focusCalc, fit };
  }

  return { create };
})();
