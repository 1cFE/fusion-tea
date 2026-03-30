"use strict";

/**
 * Cytoscape.js Neighborhood Graph component.
 *
 * Renders a force-directed layout of a focused concept and its nearest neighbors,
 * with bridge concept nodes for cross-cutting attribute connections.
 *
 * Exported:
 *   NeighborhoodGraph.render(container, focusedConcept, neighbors, registry, callbacks)
 *   NeighborhoodGraph.showBridges(neighborId, bridges)
 *   NeighborhoodGraph.clearBridges()
 *   NeighborhoodGraph.highlightBridge(conceptId)
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
    plasma_state: "Plasma State",
    magnet_type: "Magnet Type",
    energy_capture: "Energy Capture",
    tritium_breeding: "Tritium Breeding",
    neutron_management: "Neutron Management",
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

  var _cy = null;
  var _container = null;
  var _focusedConcept = null;
  var _neighbors = null;
  var _registry = null;
  var _callbacks = null;
  var _tooltipEl = null;
  var _clickTimer = null;
  var _lastClickId = null;

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

  function tooltipBridge(bridge, concept) {
    var famLabel = FAMILY_LABELS[concept.confinement_family] || concept.confinement_family;
    var fieldLabel = FIELD_LABELS[bridge.mismatched_field] || bridge.mismatched_field;
    return "<strong>" + esc(concept.name || bridge.bridge_concept_name) + "</strong><br>" +
      esc(famLabel) + "<br>" +
      "Shares " + esc(fieldLabel) + ": " + esc(bridge.query_value) + "<br>" +
      "<span style='color:#6e7681;font-size:11px'>Double-click to explore</span>";
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
  // Build graph elements
  // ---------------------------------------------------------------------------

  function buildElements(focusedConcept, neighbors) {
    var elements = [];
    var cx = 0, cy = 0;
    var radius = 200;

    // Center node
    elements.push({
      data: {
        id: "center",
        label: focusedConcept.name,
        color: familyColor(focusedConcept.confinement_family),
        conceptId: focusedConcept.concept_id
      },
      classes: "center",
      position: { x: cx, y: cy },
      locked: false
    });

    // Neighbor nodes + similarity edges
    for (var i = 0; i < neighbors.length; i++) {
      var n = neighbors[i];
      var angle = (i / neighbors.length) * 2 * Math.PI - Math.PI / 2;
      var concept = _registry[n.concept_id] || { name: n.concept_name, confinement_family: n.confinement_family };
      var score = n.comparison.overall_score;
      var sw = 1.5 + (score - 0.5) * 3; // 1.5px at 0.5, 3px at 1.0

      elements.push({
        data: {
          id: "n-" + n.concept_id,
          label: n.concept_name,
          color: familyColor(n.confinement_family),
          conceptId: n.concept_id,
          score: score
        },
        classes: "neighbor",
        position: {
          x: cx + radius * Math.cos(angle),
          y: cy + radius * Math.sin(angle)
        }
      });

      elements.push({
        data: {
          id: "e-sim-" + n.concept_id,
          source: "center",
          target: "n-" + n.concept_id,
          label: Math.round(score * 100) + "%",
          weight: Math.max(sw, 1.5),
          score: score,
          matches: n.comparison.overall_matches,
          comparable: n.comparison.overall_comparable
        },
        classes: "similarity"
      });
    }

    return elements;
  }

  // ---------------------------------------------------------------------------
  // render()
  // ---------------------------------------------------------------------------

  function render(container, focusedConcept, neighbors, registry, callbacks) {
    destroy();

    _container = container;
    _focusedConcept = focusedConcept;
    _neighbors = neighbors;
    _registry = registry;
    _callbacks = callbacks;

    container.innerHTML = "";

    var elements = buildElements(focusedConcept, neighbors);

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
        nodeRepulsion: function () { return 8000; },
        idealEdgeLength: function () { return 180; },
        edgeElasticity: function () { return 100; },
        gravity: 0.25,
        numIter: 200,
        initialTemp: 200,
        coolingFactor: 0.95,
        randomize: false
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
      var node = evt.target;
      var conceptId = node.data("conceptId");

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
      var node = evt.target;
      var conceptId = node.data("conceptId");

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
      var conceptId = node.data("conceptId");
      var concept = registry[conceptId] || { name: node.data("label"), confinement_family: "NONSTANDARD" };
      showTooltip(evt, tooltipNeighbor(concept, node.data("score")));
    });
    _cy.on("mouseout", "node.neighbor", function () { hideTooltip(); });

    _cy.on("mouseover", "node.bridge", function (evt) {
      var node = evt.target;
      var bridge = node.data("bridgeData");
      var concept = registry[node.data("conceptId")] || {
        name: bridge.bridge_concept_name,
        confinement_family: node.data("family") || "NONSTANDARD"
      };
      showTooltip(evt, tooltipBridge(bridge, concept));
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
  // Bridge lifecycle
  // ---------------------------------------------------------------------------

  function showBridges(neighborId, bridges) {
    clearBridges(true);

    if (!_cy || !bridges || bridges.length === 0) return;

    var neighborNode = _cy.getElementById("n-" + neighborId);
    if (neighborNode.empty()) return;

    // Highlight the compared neighbor
    neighborNode.addClass("comparing");

    var centerPos = _cy.getElementById("center").position();
    var neighborPos = neighborNode.position();

    // Compute bridge positions relative to center↔neighbor
    var dx = neighborPos.x - centerPos.x;
    var dy = neighborPos.y - centerPos.y;
    var baseAngle = Math.atan2(dy, dx);
    var dist = Math.sqrt(dx * dx + dy * dy) * 1.4;
    var angularSpread = 0.15;

    for (var i = 0; i < bridges.length; i++) {
      var bridge = bridges[i];
      var concept = _registry[bridge.bridge_concept_id];
      var confinementFamily = concept ? concept.confinement_family : "NONSTANDARD";
      var fieldLabel = FIELD_LABELS[bridge.mismatched_field] || bridge.mismatched_field;

      var offset = (i - (bridges.length - 1) / 2) * angularSpread;
      var angle = baseAngle + offset;
      var bx = centerPos.x + dist * Math.cos(angle);
      var by = centerPos.y + dist * Math.sin(angle);

      var edgeColor = DIMENSION_EDGE_COLORS[bridge.dimension] || "#6e7681";
      var tooltipContent = "Both use " + esc(bridge.query_value) + " for " + esc(fieldLabel);

      var nodeId = "b-" + bridge.bridge_concept_id + "-" + i;
      var edgeId = "e-bridge-" + bridge.bridge_concept_id + "-" + i;

      _cy.add([
        {
          group: "nodes",
          data: {
            id: nodeId,
            label: bridge.bridge_concept_name,
            color: familyColor(confinementFamily),
            conceptId: bridge.bridge_concept_id,
            bridgeData: bridge,
            family: confinementFamily
          },
          classes: "bridge",
          position: { x: bx, y: by },
          locked: true
        },
        {
          group: "edges",
          data: {
            id: edgeId,
            source: "center",
            target: nodeId,
            label: bridge.query_value.length > 20 ? bridge.query_value.substring(0, 19) + "\u2026" : bridge.query_value,
            edgeColor: edgeColor,
            tooltipContent: tooltipContent
          },
          classes: "bridge"
        }
      ]);

      // Animate fade-in
      (function (nId, eId) {
        setTimeout(function () {
          var bNode = _cy.getElementById(nId);
          var bEdge = _cy.getElementById(eId);
          if (!bNode.empty()) bNode.animate({ style: { opacity: 1 } }, { duration: 300 });
          if (!bEdge.empty()) bEdge.animate({ style: { opacity: 1 } }, { duration: 300 });
        }, 50);
      })(nodeId, edgeId);
    }
  }

  function clearBridges(synchronous) {
    if (!_cy) return;

    // Remove comparing class from all neighbors
    _cy.nodes(".comparing").removeClass("comparing");

    var bridgeNodes = _cy.nodes(".bridge");
    var bridgeEdges = _cy.edges(".bridge");

    if (synchronous || bridgeNodes.empty()) {
      bridgeEdges.remove();
      bridgeNodes.remove();
    } else {
      bridgeNodes.animate({ style: { opacity: 0 } }, { duration: 250 });
      bridgeEdges.animate({ style: { opacity: 0 } }, { duration: 250 });
      setTimeout(function () {
        _cy.nodes(".bridge").remove();
        _cy.edges(".bridge").remove();
      }, 300);
    }
  }

  function highlightBridge(conceptId) {
    if (!_cy) return;
    // Find bridge nodes matching this concept (may have index suffix)
    var nodes = _cy.nodes(".bridge").filter(function (node) {
      return node.data("conceptId") === conceptId;
    });
    if (nodes.empty()) return;

    nodes.addClass("highlighted");
    setTimeout(function () {
      nodes.removeClass("highlighted");
    }, 1500);
  }

  // ---------------------------------------------------------------------------
  // Resize
  // ---------------------------------------------------------------------------

  function resize() {
    if (_cy) {
      _cy.resize();
      _cy.fit(null, 50);
    }
  }

  // ---------------------------------------------------------------------------
  // Cleanup
  // ---------------------------------------------------------------------------

  function destroy() {
    if (_clickTimer) {
      clearTimeout(_clickTimer);
      _clickTimer = null;
    }
    _lastClickId = null;

    if (_cy) {
      _cy.destroy();
      _cy = null;
    }
    _container = null;
    _focusedConcept = null;
    _neighbors = null;
    _registry = null;
    _callbacks = null;
    hideTooltip();
  }

  // ---------------------------------------------------------------------------
  // Public API
  // ---------------------------------------------------------------------------

  return {
    render: render,
    showBridges: showBridges,
    clearBridges: clearBridges,
    highlightBridge: highlightBridge,
    resize: resize,
    destroy: destroy
  };
})();
