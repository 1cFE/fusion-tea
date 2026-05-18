"use strict";

/**
 * Cytoscape.js Neighborhood Graph component — Model-View architecture.
 *
 * GraphModel:  Pure data structure built once from the full similarity report.
 *              Holds all nodes (center, neighbors, bridges — deduplicated) and
 *              all edges (similarity, bridge — with multi-field labels merged).
 *
 * GraphView:   Cytoscape wrapper. Renders all elements from the model. After
 *              initial layout settles, hides bridge elements. State transitions
 *              are visibility toggles (show/hide), not DOM mutations (add/remove).
 *
 * Exported:
 *   NeighborhoodGraph.render(container, focusedConcept, report, registry, callbacks)
 *   NeighborhoodGraph.compare(neighborId)
 *   NeighborhoodGraph.clearComparison()
 *   NeighborhoodGraph.highlightBridge(conceptId)
 *   NeighborhoodGraph.getBridgesForNeighbor(neighborId)
 *   NeighborhoodGraph.resize()
 *   NeighborhoodGraph.destroy()
 */
var NeighborhoodGraph = (function () {

  // ---------------------------------------------------------------------------
  // Constants
  // ---------------------------------------------------------------------------

  var FAMILY_COLORS = {
    MFE: "#3b82f6",
    IFE: "#a855f7",
    MIF: "#f59e0b",
    NONSTANDARD: "#6b7280"
  };

  var FAMILY_LABELS = {
    MFE: "Magnetic (MFE)",
    IFE: "Inertial (IFE)",
    MIF: "Magneto-Inertial (MIF)",
    NONSTANDARD: "Non-Standard"
  };

  var FIELD_LABELS = {
    fuel: "Fuel Type",
    primary_heating: "Primary Heating",
    magnet_type: "Magnet Type",
    energy_capture: "Energy Capture",
    blanket_config: "Blanket Config",
    operation_mode: "Operation Mode",
    repetition_rate: "Repetition Rate"
  };

  var DIMENSION_EDGE_COLORS = {
    plasma_physics: "#60a5fa",
    engineering: "#34d399",
    fuel_cycle: "#fbbf24",
    operations: "#a78bfa"
  };

  var DBLCLICK_DELAY = 300;

  // ---------------------------------------------------------------------------
  // Module state
  // ---------------------------------------------------------------------------

  var _model = null;
  var _cy = null;
  var _container = null;
  var _registry = null;
  var _callbacks = null;
  var _tooltipEl = null;
  var _clickTimer = null;
  var _lastClickId = null;
  var _activeNeighborId = null;

  // ---------------------------------------------------------------------------
  // Helpers
  // ---------------------------------------------------------------------------

  function familyColor(family) {
    return FAMILY_COLORS[family] || FAMILY_COLORS.NONSTANDARD;
  }

  function esc(s) {
    if (!s) return "";
    var d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  // ---------------------------------------------------------------------------
  // Tooltip
  // ---------------------------------------------------------------------------

  function showTooltip(event, content) {
    if (!_tooltipEl) {
      _tooltipEl = document.createElement("div");
      _tooltipEl.className = "tooltip";
      document.body.appendChild(_tooltipEl);
    }
    _tooltipEl.innerHTML = content;
    _tooltipEl.style.display = "";
    _tooltipEl.style.opacity = "1";

    var x = event.originalEvent.clientX + 12;
    var y = event.originalEvent.clientY - 8;
    var rect = _tooltipEl.getBoundingClientRect();
    if (x + rect.width > window.innerWidth) x = event.originalEvent.clientX - rect.width - 12;
    if (y + rect.height > window.innerHeight) y = event.originalEvent.clientY - rect.height;
    if (x < 0) x = 4;
    if (y < 0) y = 4;

    _tooltipEl.style.left = x + "px";
    _tooltipEl.style.top = y + "px";
  }

  function hideTooltip() {
    if (_tooltipEl) {
      _tooltipEl.style.display = "none";
      _tooltipEl.style.opacity = "0";
    }
  }

  function tooltipCenter(concept) {
    var lines = ["<strong>" + esc(concept.name) + "</strong>"];
    if (concept.company) lines.push(esc(concept.company));
    var hier = concept.mfe_topology || concept.ife_driver || concept.mif_method || concept.non_standard_mechanism;
    var famLabel = FAMILY_LABELS[concept.confinement_family] || concept.confinement_family;
    lines.push(esc(famLabel) + (hier ? " &middot; " + esc(hier) : ""));
    return lines.join("<br>");
  }

  function tooltipNeighbor(concept, score) {
    var famLabel = FAMILY_LABELS[concept.confinement_family] || concept.confinement_family;
    return "<strong>" + esc(concept.name) + "</strong><br>" +
      esc(famLabel) + " &middot; " + Math.round(score * 100) + "% similar<br>" +
      "<span style='color:#6e7681;font-size:11px'>Click to compare &middot; Double-click to explore</span>";
  }

  function tooltipBridgeNode(concept) {
    var famLabel = FAMILY_LABELS[concept.confinement_family] || concept.confinement_family;
    return "<strong>" + esc(concept.name) + "</strong><br>" +
      esc(famLabel) + "<br>" +
      "<span style='color:#6e7681;font-size:11px'>Double-click to explore</span>";
  }

  // ---------------------------------------------------------------------------
  // GraphModel — Pure data structure
  // ---------------------------------------------------------------------------

  function buildGraphModel(focusedConcept, report, registry) {
    var model = {
      centerConceptId: focusedConcept.concept_id,
      nodes: {},
      edges: {},
      _bridgesByNeighbor: {}
    };

    // ---- Stage 1: center node + neighbor nodes + similarity edges ----

    model.nodes[focusedConcept.concept_id] = {
      id: focusedConcept.concept_id,
      type: "center",
      label: focusedConcept.name,
      family: focusedConcept.confinement_family,
      score: null,
      bridgeForNeighbors: []
    };

    var nearest = report.nearest;
    for (var i = 0; i < nearest.length; i++) {
      var n = nearest[i];

      model.nodes[n.concept_id] = {
        id: n.concept_id,
        type: "neighbor",
        label: n.concept_name,
        family: n.confinement_family,
        score: n.comparison.overall_score,
        bridgeForNeighbors: []
      };

      var simEdgeId = "sim:" + n.concept_id;
      model.edges[simEdgeId] = {
        id: simEdgeId,
        type: "similarity",
        source: focusedConcept.concept_id,
        target: n.concept_id,
        score: n.comparison.overall_score,
        matches: n.comparison.overall_matches,
        comparable: n.comparison.overall_comparable
      };
    }

    // ---- Stage 2: bridge nodes + edges with deduplication ----

    for (var i = 0; i < nearest.length; i++) {
      var n = nearest[i];
      var bridges = n.bridges || [];
      model._bridgesByNeighbor[n.concept_id] = [];

      for (var j = 0; j < bridges.length; j++) {
        var bridge = bridges[j];
        var bridgeConceptId = bridge.bridge_concept_id;

        // Node deduplication
        if (model.nodes[bridgeConceptId]) {
          var existingNode = model.nodes[bridgeConceptId];
          if (existingNode.type === "bridge") {
            if (existingNode.bridgeForNeighbors.indexOf(n.concept_id) === -1) {
              existingNode.bridgeForNeighbors.push(n.concept_id);
            }
          }
          // If it's center or neighbor, don't change type — it stays always-visible
        } else {
          var bridgeConcept = registry[bridgeConceptId] || {};
          model.nodes[bridgeConceptId] = {
            id: bridgeConceptId,
            type: "bridge",
            label: bridge.bridge_concept_name,
            family: bridgeConcept.confinement_family || "NONSTANDARD",
            score: bridge.bridge_overall_similarity,
            bridgeForNeighbors: [n.concept_id]
          };
        }

        // Edge deduplication — multi-field merging
        var edgeKey = "br:" + n.concept_id + ":" + bridgeConceptId;
        if (model.edges[edgeKey]) {
          var existingEdge = model.edges[edgeKey];
          existingEdge.fields.push(bridge.mismatched_field);
          existingEdge.queryValues[bridge.mismatched_field] = bridge.query_value;
          existingEdge.similarValues[bridge.mismatched_field] = bridge.similar_value;
        } else {
          var qv = {};
          qv[bridge.mismatched_field] = bridge.query_value;
          var sv = {};
          sv[bridge.mismatched_field] = bridge.similar_value;

          model.edges[edgeKey] = {
            id: edgeKey,
            type: "bridge",
            source: focusedConcept.concept_id,
            target: bridgeConceptId,
            neighborId: n.concept_id,
            fields: [bridge.mismatched_field],
            dimension: bridge.dimension,
            queryValues: qv,
            similarValues: sv
          };
        }

        // Per-field record for the comparison panel
        model._bridgesByNeighbor[n.concept_id].push({
          conceptId: bridgeConceptId,
          conceptName: bridge.bridge_concept_name,
          field: bridge.mismatched_field,
          queryValue: bridge.query_value,
          similarValue: bridge.similar_value,
          dimension: bridge.dimension,
          edgeId: edgeKey
        });
      }
    }

    // ---- Stage 3: query methods ----

    model.getNeighborIds = function () {
      var ids = [];
      for (var id in model.nodes) {
        if (model.nodes[id].type === "neighbor") ids.push(id);
      }
      return ids;
    };

    model.getBridgesForNeighbor = function (neighborId) {
      return model._bridgesByNeighbor[neighborId] || [];
    };

    model.getBridgeNodeIdsForNeighbor = function (neighborId) {
      var entries = model._bridgesByNeighbor[neighborId] || [];
      var seen = {};
      var ids = [];
      for (var i = 0; i < entries.length; i++) {
        var cid = entries[i].conceptId;
        // Only include nodes that are bridge-type (neighbors are already visible)
        if (!seen[cid] && model.nodes[cid] && model.nodes[cid].type === "bridge") {
          seen[cid] = true;
          ids.push(cid);
        }
      }
      return ids;
    };

    model.getBridgeEdgeIdsForNeighbor = function (neighborId) {
      var entries = model._bridgesByNeighbor[neighborId] || [];
      var seen = {};
      var ids = [];
      for (var i = 0; i < entries.length; i++) {
        var eid = entries[i].edgeId;
        if (!seen[eid]) {
          seen[eid] = true;
          ids.push(eid);
        }
      }
      return ids;
    };

    return model;
  }

  // ---------------------------------------------------------------------------
  // Cytoscape stylesheet
  // ---------------------------------------------------------------------------

  function buildStylesheet() {
    return [
      // Center node
      {
        selector: "node.center",
        style: {
          "background-color": "data(color)",
          "width": 64,
          "height": 64,
          "label": "data(label)",
          "font-size": "14px",
          "font-weight": "bold",
          "color": "#e6edf3",
          "text-outline-color": "#0d1117",
          "text-outline-width": 2,
          "text-valign": "bottom",
          "text-margin-y": 8,
          "text-wrap": "ellipsis",
          "text-max-width": "140px",
          "border-width": 2,
          "border-color": "rgba(255,255,255,0.6)",
          "z-index": 10
        }
      },
      // Neighbor node
      {
        selector: "node.neighbor",
        style: {
          "background-color": "data(color)",
          "width": 44,
          "height": 44,
          "label": "data(label)",
          "font-size": "13px",
          "color": "#c9d1d9",
          "text-outline-color": "#0d1117",
          "text-outline-width": 2,
          "text-valign": "bottom",
          "text-margin-y": 6,
          "text-wrap": "ellipsis",
          "text-max-width": "130px",
          "border-width": 1.5,
          "border-color": "rgba(255,255,255,0.3)",
          "cursor": "pointer",
          "z-index": 5
        }
      },
      // Neighbor hover
      {
        selector: "node.neighbor:active, node.neighbor:grabbed",
        style: {
          "border-width": 2.5,
          "border-color": "rgba(255,255,255,0.6)"
        }
      },
      // Comparing neighbor highlight
      {
        selector: "node.neighbor.comparing",
        style: {
          "border-width": 3,
          "border-color": "#e6edf3",
          "overlay-opacity": 0.08,
          "overlay-color": "#ffffff"
        }
      },
      // Bridge node (diamond)
      {
        selector: "node.bridge",
        style: {
          "background-color": "data(color)",
          "width": 36,
          "height": 36,
          "shape": "diamond",
          "label": "data(label)",
          "font-size": "12px",
          "color": "#8b949e",
          "text-outline-color": "#0d1117",
          "text-outline-width": 1.5,
          "text-valign": "bottom",
          "text-margin-y": 6,
          "text-wrap": "ellipsis",
          "text-max-width": "120px",
          "border-width": 1.5,
          "border-color": "rgba(255,255,255,0.4)",
          "border-style": "dashed",
          "cursor": "pointer",
          "z-index": 4,
          "opacity": 0
        }
      },
      // Selection tray indicator (neighbor or center in tray)
      {
        selector: "node.in-tray",
        style: {
          "border-width": 3,
          "border-color": "#e6edf3",
          "border-style": "double"
        }
      },
      // Bridge highlight pulse
      {
        selector: "node.bridge.highlighted",
        style: {
          "border-width": 3,
          "border-color": "#e6edf3",
          "overlay-opacity": 0.15,
          "overlay-color": "#ffffff"
        }
      },
      // Similarity edge
      {
        selector: "edge.similarity",
        style: {
          "width": "data(weight)",
          "line-color": "rgba(139,148,158,0.4)",
          "curve-style": "bezier",
          "label": "data(label)",
          "font-size": "10px",
          "color": "#6e7681",
          "text-outline-color": "#0d1117",
          "text-outline-width": 1.5,
          "text-rotation": "autorotate",
          "text-margin-y": -8
        }
      },
      // Bridge edge
      {
        selector: "edge.bridge",
        style: {
          "width": 1.5,
          "line-color": "data(edgeColor)",
          "line-style": "dashed",
          "line-dash-pattern": [6, 4],
          "curve-style": "bezier",
          "label": "data(label)",
          "font-size": "10px",
          "color": "#6e7681",
          "text-outline-color": "#0d1117",
          "text-outline-width": 1.5,
          "text-rotation": "autorotate",
          "text-margin-y": -8,
          "opacity": 0
        }
      }
    ];
  }

  // ---------------------------------------------------------------------------
  // Build Cytoscape elements from GraphModel
  // ---------------------------------------------------------------------------

  function buildElements(model) {
    var elements = [];
    var radius = 200;

    // Compute neighbor positions (for initial layout hints)
    var neighborIds = model.getNeighborIds();
    var neighborPositions = {};
    for (var i = 0; i < neighborIds.length; i++) {
      var angle = (i / neighborIds.length) * 2 * Math.PI - Math.PI / 2;
      neighborPositions[neighborIds[i]] = {
        x: radius * Math.cos(angle),
        y: radius * Math.sin(angle)
      };
    }

    // ---- Nodes ----

    for (var id in model.nodes) {
      var node = model.nodes[id];
      var position;
      var classes;

      if (node.type === "center") {
        position = { x: 0, y: 0 };
        classes = "center";
      } else if (node.type === "neighbor") {
        position = neighborPositions[id] || { x: 0, y: 0 };
        classes = "neighbor";
      } else {
        // Bridge: initial position toward associated neighbors
        var bfn = node.bridgeForNeighbors;
        var avgX = 0, avgY = 0, count = 0;
        for (var k = 0; k < bfn.length; k++) {
          var np = neighborPositions[bfn[k]];
          if (np) { avgX += np.x; avgY += np.y; count++; }
        }
        if (count > 0) { avgX /= count; avgY /= count; }
        var bAngle = Math.atan2(avgY, avgX);
        var bDist = 160;
        position = { x: bDist * Math.cos(bAngle), y: bDist * Math.sin(bAngle) };
        classes = "bridge";
      }

      elements.push({
        data: {
          id: id,
          label: node.label,
          color: familyColor(node.family),
          score: node.score,
          family: node.family
        },
        classes: classes,
        position: position
      });
    }

    // ---- Edges ----

    for (var edgeId in model.edges) {
      var edge = model.edges[edgeId];

      if (edge.type === "similarity") {
        var sw = 1.5 + (edge.score - 0.5) * 3;
        elements.push({
          data: {
            id: edge.id,
            source: edge.source,
            target: edge.target,
            label: Math.round(edge.score * 100) + "%",
            weight: Math.max(sw, 1.5),
            score: edge.score,
            matches: edge.matches,
            comparable: edge.comparable
          },
          classes: "similarity"
        });
      } else {
        // Bridge edge — build combined field label
        var fieldLabels = [];
        var tooltipParts = [];
        for (var fi = 0; fi < edge.fields.length; fi++) {
          var f = edge.fields[fi];
          var fl = FIELD_LABELS[f] || f;
          fieldLabels.push(fl);
          tooltipParts.push("Shares " + esc(fl) + ": " + esc(edge.queryValues[f]));
        }
        var combinedLabel = fieldLabels.join(" + ");
        var edgeColor = DIMENSION_EDGE_COLORS[edge.dimension] || "#6e7681";

        elements.push({
          data: {
            id: edge.id,
            source: edge.source,
            target: edge.target,
            label: combinedLabel,
            edgeColor: edgeColor,
            tooltipContent: tooltipParts.join("<br>"),
            neighborId: edge.neighborId
          },
          classes: "bridge"
        });
      }
    }

    return elements;
  }

  // ---------------------------------------------------------------------------
  // render()
  // ---------------------------------------------------------------------------

  function render(container, focusedConcept, report, registry, callbacks) {
    destroy();

    _container = container;
    _registry = registry;
    _callbacks = callbacks;
    _activeNeighborId = null;

    container.innerHTML = "";

    // Build model and elements
    _model = buildGraphModel(focusedConcept, report, registry);
    var elements = buildElements(_model);

    _cy = cytoscape({
      container: container,
      elements: elements,
      style: buildStylesheet(),
      layout: {
        name: "cose",
        animate: true,
        animationDuration: 500,
        fit: true,
        padding: 50,
        nodeRepulsion: function (node) {
          return node.hasClass("bridge") ? 4000 : 8000;
        },
        idealEdgeLength: function (edge) {
          return edge.hasClass("bridge") ? 140 : 180;
        },
        edgeElasticity: function () { return 100; },
        gravity: 0.25,
        numIter: 200,
        initialTemp: 200,
        coolingFactor: 0.95,
        randomize: false,
        stop: function () {
          // After layout settles, hide all bridge elements.
          // Bridges had opacity:0 from the stylesheet during layout (invisible
          // but participating in the force simulation). Now hide them so they
          // don't receive pointer events until explicitly shown via compare().
          if (_cy) _cy.elements(".bridge").hide();
        }
      },
      minZoom: 0.3,
      maxZoom: 3,
      wheelSensitivity: 0.3,
      boxSelectionEnabled: false,
      autounselectify: true
    });

    // --- Event handlers ---

    // Neighbor: single-click (debounced) → compare, double-click → re-center
    _cy.on("tap", "node.neighbor", function (evt) {
      var conceptId = evt.target.id();

      // Ctrl/Cmd+click: selection tray (short-circuits debounce)
      var nativeEvent = evt.originalEvent;
      if (nativeEvent && (nativeEvent.metaKey || nativeEvent.ctrlKey)) {
        if (callbacks.onCtrlClick) callbacks.onCtrlClick(conceptId, nativeEvent);
        return;
      }

      if (_clickTimer && _lastClickId === conceptId) {
        clearTimeout(_clickTimer);
        _clickTimer = null;
        _lastClickId = null;
        callbacks.onFocus(conceptId);
      } else {
        if (_clickTimer) clearTimeout(_clickTimer);
        _lastClickId = conceptId;
        _clickTimer = setTimeout(function () {
          _clickTimer = null;
          _lastClickId = null;
          callbacks.onCompare(conceptId);
        }, DBLCLICK_DELAY);
      }
    });

    // Bridge: double-click → re-center
    _cy.on("tap", "node.bridge", function (evt) {
      var conceptId = evt.target.id();

      if (_clickTimer && _lastClickId === conceptId) {
        clearTimeout(_clickTimer);
        _clickTimer = null;
        _lastClickId = null;
        callbacks.onFocus(conceptId);
      } else {
        if (_clickTimer) clearTimeout(_clickTimer);
        _lastClickId = conceptId;
        _clickTimer = setTimeout(function () {
          _clickTimer = null;
          _lastClickId = null;
        }, DBLCLICK_DELAY);
      }
    });

    // Center node: Ctrl/Cmd+click only → selection tray
    _cy.on("tap", "node.center", function (evt) {
      var conceptId = evt.target.id();
      var nativeEvent = evt.originalEvent;
      if (nativeEvent && (nativeEvent.metaKey || nativeEvent.ctrlKey)) {
        if (callbacks.onCtrlClick) callbacks.onCtrlClick(conceptId, nativeEvent);
      }
    });

    // Background click → deselect
    _cy.on("tap", function (evt) {
      if (evt.target === _cy) {
        callbacks.onDeselect();
      }
    });

    // Tooltips
    _cy.on("mouseover", "node.center", function (evt) {
      showTooltip(evt, tooltipCenter(focusedConcept));
    });
    _cy.on("mouseout", "node.center", function () { hideTooltip(); });

    _cy.on("mouseover", "node.neighbor", function (evt) {
      var node = evt.target;
      var conceptId = node.id();
      var concept = registry[conceptId] || { name: node.data("label"), confinement_family: "NONSTANDARD" };
      showTooltip(evt, tooltipNeighbor(concept, node.data("score")));
    });
    _cy.on("mouseout", "node.neighbor", function () { hideTooltip(); });

    _cy.on("mouseover", "node.bridge", function (evt) {
      var node = evt.target;
      var conceptId = node.id();
      var concept = registry[conceptId] || { name: node.data("label"), confinement_family: node.data("family") || "NONSTANDARD" };
      showTooltip(evt, tooltipBridgeNode(concept));
    });
    _cy.on("mouseout", "node.bridge", function () { hideTooltip(); });

    _cy.on("mouseover", "edge.similarity", function (evt) {
      var edge = evt.target;
      var content = Math.round(edge.data("score") * 100) + "% design similarity<br>" +
        edge.data("matches") + "/" + edge.data("comparable") + " attributes match";
      showTooltip(evt, content);
    });
    _cy.on("mouseout", "edge.similarity", function () { hideTooltip(); });

    _cy.on("mouseover", "edge.bridge", function (evt) {
      var edge = evt.target;
      showTooltip(evt, edge.data("tooltipContent") || "");
    });
    _cy.on("mouseout", "edge.bridge", function () { hideTooltip(); });
  }

  // ---------------------------------------------------------------------------
  // Comparison lifecycle — visibility toggles
  // ---------------------------------------------------------------------------

  function compare(neighborId) {
    if (!_cy || !_model) return;

    // 1. Hide any previously visible bridges (instant)
    _cy.elements(".bridge").hide().style("opacity", 0);
    _cy.nodes(".comparing").removeClass("comparing");

    // 2. Highlight the compared neighbor
    var neighborNode = _cy.getElementById(neighborId);
    if (!neighborNode.empty()) {
      neighborNode.addClass("comparing");
    }

    // 3. Show bridge nodes for this neighbor
    var bridgeNodeIds = _model.getBridgeNodeIdsForNeighbor(neighborId);
    for (var i = 0; i < bridgeNodeIds.length; i++) {
      var node = _cy.getElementById(bridgeNodeIds[i]);
      if (!node.empty()) {
        node.show();
        node.animate({ style: { opacity: 1 } }, { duration: 250 });
      }
    }

    // 4. Show bridge edges for this neighbor
    var bridgeEdgeIds = _model.getBridgeEdgeIdsForNeighbor(neighborId);
    for (var i = 0; i < bridgeEdgeIds.length; i++) {
      var edge = _cy.getElementById(bridgeEdgeIds[i]);
      if (!edge.empty()) {
        edge.show();
        edge.animate({ style: { opacity: 1 } }, { duration: 250 });
      }
    }

    _activeNeighborId = neighborId;
  }

  function clearComparison() {
    if (!_cy || !_activeNeighborId) return;

    _cy.nodes(".comparing").removeClass("comparing");

    var bridges = _cy.elements(".bridge").filter(":visible");
    bridges.animate(
      { style: { opacity: 0 } },
      {
        duration: 200,
        complete: function () { bridges.hide(); }
      }
    );

    _activeNeighborId = null;
  }

  function highlightBridge(conceptId) {
    if (!_cy) return;
    var node = _cy.getElementById(conceptId);
    if (node.empty()) return;

    node.addClass("highlighted");
    setTimeout(function () {
      node.removeClass("highlighted");
    }, 1500);
  }

  // ---------------------------------------------------------------------------
  // Model queries (delegated)
  // ---------------------------------------------------------------------------

  function getBridgesForNeighbor(neighborId) {
    if (!_model) return [];
    return _model.getBridgesForNeighbor(neighborId);
  }

  // ---------------------------------------------------------------------------
  // Selection tray indicators
  // ---------------------------------------------------------------------------

  function updateTrayIndicators(selectedIds) {
    if (!_cy) return;
    var idSet = {};
    for (var i = 0; i < selectedIds.length; i++) {
      idSet[selectedIds[i]] = true;
    }
    _cy.nodes(".neighbor, .center").forEach(function (node) {
      if (idSet[node.id()]) {
        node.addClass("in-tray");
      } else {
        node.removeClass("in-tray");
      }
    });
  }

  // ---------------------------------------------------------------------------
  // Resize / Destroy
  // ---------------------------------------------------------------------------

  function resize() {
    if (_cy) {
      _cy.resize();
      _cy.fit(null, 50);
    }
  }

  function destroy() {
    if (_clickTimer) {
      clearTimeout(_clickTimer);
      _clickTimer = null;
    }
    _lastClickId = null;
    _activeNeighborId = null;

    if (_cy) {
      _cy.destroy();
      _cy = null;
    }
    _model = null;
    _container = null;
    _registry = null;
    _callbacks = null;
    hideTooltip();
  }

  // ---------------------------------------------------------------------------
  // Public API
  // ---------------------------------------------------------------------------

  return {
    render: render,
    compare: compare,
    clearComparison: clearComparison,
    highlightBridge: highlightBridge,
    getBridgesForNeighbor: getBridgesForNeighbor,
    updateTrayIndicators: updateTrayIndicators,
    resize: resize,
    destroy: destroy
  };
})();
