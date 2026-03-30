"use strict";

/**
 * SVG Neighborhood Graph component.
 *
 * Renders a radial layout of a focused concept and its nearest neighbors,
 * with bridge concept nodes for cross-cutting attribute connections.
 *
 * Exported:
 *   NeighborhoodGraph.render(container, focusedConcept, neighbors, registry, callbacks)
 *   NeighborhoodGraph.showBridges(neighborId, bridges)
 *   NeighborhoodGraph.clearBridges()
 *   NeighborhoodGraph.highlightBridge(conceptId)
 *   NeighborhoodGraph.destroy()
 */
var NeighborhoodGraph = (function () {

  // ---------------------------------------------------------------------------
  // Constants
  // ---------------------------------------------------------------------------

  var SVG_NS = "http://www.w3.org/2000/svg";
  var TOP_N = 5;
  var NEIGHBOR_RADIUS_FACTOR = 0.32;
  var BRIDGE_RADIUS_FACTOR = 0.48;
  var BRIDGE_ANGULAR_OFFSET = 0.15; // radians between bridges near same neighbor
  var MAX_LABEL_LEN = 25;

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

  // ---------------------------------------------------------------------------
  // Module state (reset on each render)
  // ---------------------------------------------------------------------------

  var _svg = null;
  var _container = null;
  var _layout = null;
  var _focusedConcept = null;
  var _neighbors = null;
  var _registry = null;
  var _callbacks = null;
  var _edgesGroup = null;
  var _nodesGroup = null;
  var _neighborIndexById = {}; // concept_id -> index in neighbors array
  var _tooltipEl = null;

  // ---------------------------------------------------------------------------
  // DOM helpers
  // ---------------------------------------------------------------------------

  function svgEl(tag, attrs) {
    var node = document.createElementNS(SVG_NS, tag);
    if (attrs) {
      for (var k in attrs) {
        node.setAttribute(k, attrs[k]);
      }
    }
    return node;
  }

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  function truncate(str, maxLen) {
    if (!str) return "";
    return str.length > maxLen ? str.substring(0, maxLen - 1) + "\u2026" : str;
  }

  function familyColor(family) {
    return FAMILY_COLORS[family] || FAMILY_COLORS.NONSTANDARD;
  }

  // ---------------------------------------------------------------------------
  // Layout computation
  // ---------------------------------------------------------------------------

  function computeLayout(width, height, neighborCount) {
    var cx = width / 2;
    var cy = height / 2;
    var base = Math.min(width, height);
    var radius = base * NEIGHBOR_RADIUS_FACTOR;
    var bridgeRadius = base * BRIDGE_RADIUS_FACTOR;
    var neighbors = [];
    for (var i = 0; i < neighborCount; i++) {
      var angle = (i / neighborCount) * 2 * Math.PI - Math.PI / 2;
      neighbors.push({
        x: cx + radius * Math.cos(angle),
        y: cy + radius * Math.sin(angle),
        angle: angle
      });
    }
    return { cx: cx, cy: cy, radius: radius, bridgeRadius: bridgeRadius, neighbors: neighbors };
  }

  function computeBridgePositions(layout, neighborIndex, bridgeCount) {
    var nPos = layout.neighbors[neighborIndex];
    var positions = [];
    for (var i = 0; i < bridgeCount; i++) {
      // Spread bridges around the neighbor's angle
      var offset = (i - (bridgeCount - 1) / 2) * BRIDGE_ANGULAR_OFFSET;
      var angle = nPos.angle + offset;
      positions.push({
        x: layout.cx + layout.bridgeRadius * Math.cos(angle),
        y: layout.cy + layout.bridgeRadius * Math.sin(angle),
        angle: angle
      });
    }
    return positions;
  }

  // ---------------------------------------------------------------------------
  // Tooltip system
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

    // Position near cursor, avoid viewport overflow
    var x = event.clientX + 12;
    var y = event.clientY - 8;
    // Force layout so we can measure
    var rect = _tooltipEl.getBoundingClientRect();
    if (x + rect.width > window.innerWidth) x = event.clientX - rect.width - 12;
    if (y + rect.height > window.innerHeight) y = event.clientY - rect.height;
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

  // Tooltip content builders

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

  function tooltipSimilarityEdge(score, matches, comparable) {
    return Math.round(score * 100) + "% design similarity<br>" +
      matches + "/" + comparable + " attributes match";
  }

  function tooltipBridgeEdge(bridge) {
    var fieldLabel = FIELD_LABELS[bridge.mismatched_field] || bridge.mismatched_field;
    return "Both use " + esc(bridge.query_value) + " for " + esc(fieldLabel);
  }

  function esc(s) {
    if (!s) return "";
    var d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  // ---------------------------------------------------------------------------
  // Edge rendering helpers
  // ---------------------------------------------------------------------------

  function edgeMidpoint(x1, y1, x2, y2) {
    return { x: (x1 + x2) / 2, y: (y1 + y2) / 2 };
  }

  function similarityStrokeWidth(score) {
    // 1.5px at 0.5, 3px at 1.0
    return 1.5 + (score - 0.5) * 3;
  }

  function renderSimilarityEdge(cx, cy, nx, ny, score, matches, comparable) {
    var g = svgEl("g", { "class": "ng-edge ng-edge--similarity" });
    var sw = similarityStrokeWidth(score);

    g.appendChild(svgEl("line", {
      x1: cx, y1: cy, x2: nx, y2: ny,
      "stroke-width": sw
    }));

    var mid = edgeMidpoint(cx, cy, nx, ny);
    var label = svgEl("text", {
      "class": "ng-edge__label",
      x: mid.x, y: mid.y - 6
    });
    label.textContent = Math.round(score * 100) + "%";
    g.appendChild(label);

    // Invisible wider line for hover target
    var hitArea = svgEl("line", {
      x1: cx, y1: cy, x2: nx, y2: ny,
      stroke: "transparent", "stroke-width": 12
    });
    g.appendChild(hitArea);

    g.addEventListener("mouseenter", function (e) {
      showTooltip(e, tooltipSimilarityEdge(score, matches, comparable));
    });
    g.addEventListener("mousemove", function (e) {
      showTooltip(e, tooltipSimilarityEdge(score, matches, comparable));
    });
    g.addEventListener("mouseleave", hideTooltip);

    return g;
  }

  // ---------------------------------------------------------------------------
  // Node rendering helpers
  // ---------------------------------------------------------------------------

  function renderCenterNode(concept, cx, cy) {
    var g = svgEl("g", {
      "class": "ng-node ng-node--center",
      transform: "translate(" + cx + "," + cy + ")"
    });

    var circle = svgEl("circle", {
      r: 32,
      "class": "ng-node__shape",
      fill: familyColor(concept.confinement_family),
      stroke: "rgba(255,255,255,0.6)",
      "stroke-width": 2,
      filter: "url(#center-shadow)"
    });
    g.appendChild(circle);

    var nameText = svgEl("text", { "class": "ng-node__name", dy: 48 });
    nameText.textContent = truncate(concept.name, MAX_LABEL_LEN);
    g.appendChild(nameText);

    g.addEventListener("mouseenter", function (e) {
      showTooltip(e, tooltipCenter(concept));
    });
    g.addEventListener("mousemove", function (e) {
      showTooltip(e, tooltipCenter(concept));
    });
    g.addEventListener("mouseleave", hideTooltip);

    return g;
  }

  function renderNeighborNode(neighbor, pos, callbacks) {
    var conceptId = neighbor.concept_id;
    var concept = _registry[conceptId];
    var score = neighbor.comparison.overall_score;

    var g = svgEl("g", {
      "class": "ng-node ng-node--neighbor",
      "data-concept-id": conceptId,
      transform: "translate(" + pos.x + "," + pos.y + ")"
    });

    var circle = svgEl("circle", {
      r: 22,
      "class": "ng-node__shape",
      fill: familyColor(neighbor.confinement_family),
      stroke: "rgba(255,255,255,0.3)",
      "stroke-width": 1.5
    });
    g.appendChild(circle);

    var nameText = svgEl("text", { "class": "ng-node__name", dy: 34 });
    nameText.textContent = truncate(neighbor.concept_name, MAX_LABEL_LEN);
    g.appendChild(nameText);

    var scoreText = svgEl("text", { "class": "ng-node__score", dy: -30 });
    scoreText.textContent = Math.round(score * 100) + "%";
    g.appendChild(scoreText);

    // Click → compare
    g.addEventListener("click", function (e) {
      e.stopPropagation();
      callbacks.onCompare(conceptId);
    });

    // Double-click → re-center
    g.addEventListener("dblclick", function (e) {
      e.stopPropagation();
      callbacks.onFocus(conceptId);
    });

    // Tooltip
    var tooltipConcept = concept || { name: neighbor.concept_name, confinement_family: neighbor.confinement_family };
    g.addEventListener("mouseenter", function (e) {
      showTooltip(e, tooltipNeighbor(tooltipConcept, score));
    });
    g.addEventListener("mousemove", function (e) {
      showTooltip(e, tooltipNeighbor(tooltipConcept, score));
    });
    g.addEventListener("mouseleave", hideTooltip);

    return g;
  }

  // ---------------------------------------------------------------------------
  // render() — main entry point
  // ---------------------------------------------------------------------------

  function render(container, focusedConcept, neighbors, registry, callbacks) {
    destroy(); // clean up previous graph

    _container = container;
    _focusedConcept = focusedConcept;
    _neighbors = neighbors;
    _registry = registry;
    _callbacks = callbacks;
    _neighborIndexById = {};

    // Determine SVG dimensions from container
    var width = container.clientWidth || 700;
    var height = Math.max(container.clientHeight || 500, 450);

    _layout = computeLayout(width, height, neighbors.length);

    // Create SVG
    _svg = svgEl("svg", {
      viewBox: "0 0 " + width + " " + height,
      "class": "neighborhood-graph",
      preserveAspectRatio: "xMidYMid meet"
    });

    // Defs (drop shadow for center node)
    var defs = svgEl("defs");
    var filter = svgEl("filter", { id: "center-shadow", x: "-50%", y: "-50%", width: "200%", height: "200%" });
    var feDropShadow = svgEl("feDropShadow", {
      dx: 0, dy: 2, stdDeviation: 3, "flood-color": "rgba(0,0,0,0.4)"
    });
    filter.appendChild(feDropShadow);
    defs.appendChild(filter);
    _svg.appendChild(defs);

    // Edge group (rendered first so nodes are on top)
    _edgesGroup = svgEl("g", { "class": "ng-edges" });
    _svg.appendChild(_edgesGroup);

    // Node group
    _nodesGroup = svgEl("g", { "class": "ng-nodes" });
    _svg.appendChild(_nodesGroup);

    // Render similarity edges and neighbor nodes
    for (var i = 0; i < neighbors.length; i++) {
      var n = neighbors[i];
      var pos = _layout.neighbors[i];
      _neighborIndexById[n.concept_id] = i;

      // Edge
      var comp = n.comparison;
      _edgesGroup.appendChild(renderSimilarityEdge(
        _layout.cx, _layout.cy, pos.x, pos.y,
        comp.overall_score, comp.overall_matches, comp.overall_comparable
      ));

      // Node
      _nodesGroup.appendChild(renderNeighborNode(n, pos, callbacks));
    }

    // Render center node (on top of edges and neighbor nodes)
    _nodesGroup.appendChild(renderCenterNode(focusedConcept, _layout.cx, _layout.cy));

    // Background click → deselect
    _svg.addEventListener("click", function () {
      callbacks.onDeselect();
    });

    container.innerHTML = "";
    container.appendChild(_svg);
  }

  // ---------------------------------------------------------------------------
  // Bridge lifecycle
  // ---------------------------------------------------------------------------

  function showBridges(neighborId, bridges) {
    clearBridges();

    if (!_svg || !_layout || !bridges || bridges.length === 0) return;

    var nIdx = _neighborIndexById[neighborId];
    if (nIdx === undefined) return;

    // Highlight the compared neighbor
    var neighborNode = _svg.querySelector('.ng-node--neighbor[data-concept-id="' + neighborId + '"]');
    if (neighborNode) neighborNode.classList.add("ng-node--comparing");

    // Compute bridge positions
    var positions = computeBridgePositions(_layout, nIdx, bridges.length);

    for (var i = 0; i < bridges.length; i++) {
      var bridge = bridges[i];
      var pos = positions[i];
      var concept = _registry[bridge.bridge_concept_id];
      var confinementFamily = concept ? concept.confinement_family : "NONSTANDARD";
      var fieldLabel = FIELD_LABELS[bridge.mismatched_field] || bridge.mismatched_field;

      // Bridge edge (center → bridge)
      var edgeG = svgEl("g", {
        "class": "ng-edge ng-edge--bridge",
        "data-dimension": bridge.dimension,
        style: "opacity:0"
      });

      edgeG.appendChild(svgEl("line", {
        x1: _layout.cx, y1: _layout.cy,
        x2: pos.x, y2: pos.y,
        "stroke-dasharray": "6,4",
        "stroke-width": 1.5
      }));

      var edgeMid = edgeMidpoint(_layout.cx, _layout.cy, pos.x, pos.y);
      var edgeLabel = svgEl("text", {
        "class": "ng-edge__label",
        x: edgeMid.x, y: edgeMid.y - 6
      });
      edgeLabel.textContent = truncate(bridge.query_value, 20);
      edgeG.appendChild(edgeLabel);

      // Invisible hover target for edge
      var edgeHit = svgEl("line", {
        x1: _layout.cx, y1: _layout.cy,
        x2: pos.x, y2: pos.y,
        stroke: "transparent", "stroke-width": 12
      });
      edgeG.appendChild(edgeHit);

      (function (b) {
        edgeG.addEventListener("mouseenter", function (e) {
          showTooltip(e, tooltipBridgeEdge(b));
        });
        edgeG.addEventListener("mousemove", function (e) {
          showTooltip(e, tooltipBridgeEdge(b));
        });
        edgeG.addEventListener("mouseleave", hideTooltip);
      })(bridge);

      _edgesGroup.appendChild(edgeG);

      // Bridge node (diamond)
      var nodeG = svgEl("g", {
        "class": "ng-node ng-node--bridge",
        "data-concept-id": bridge.bridge_concept_id,
        transform: "translate(" + pos.x + "," + pos.y + ")",
        style: "opacity:0"
      });

      var diamond = svgEl("rect", {
        "class": "ng-node__shape",
        x: -14, y: -14, width: 28, height: 28,
        rx: 3,
        transform: "rotate(45)",
        fill: familyColor(confinementFamily),
        stroke: "rgba(255,255,255,0.4)",
        "stroke-width": 1.5
      });
      nodeG.appendChild(diamond);

      var bName = svgEl("text", { "class": "ng-node__name", dy: 28 });
      bName.textContent = truncate(bridge.bridge_concept_name, MAX_LABEL_LEN);
      nodeG.appendChild(bName);

      var bAttr = svgEl("text", { "class": "ng-node__attr", dy: -24 });
      bAttr.textContent = truncate(fieldLabel, 20);
      nodeG.appendChild(bAttr);

      // Bridge node interactions
      (function (bid, b, c) {
        nodeG.addEventListener("click", function (e) {
          e.stopPropagation();
          // Single-click on bridge does nothing special — only dblclick navigates
        });
        nodeG.addEventListener("dblclick", function (e) {
          e.stopPropagation();
          _callbacks.onFocus(bid);
        });
        nodeG.addEventListener("mouseenter", function (e) {
          showTooltip(e, tooltipBridge(b, c || { name: b.bridge_concept_name, confinement_family: confinementFamily }));
        });
        nodeG.addEventListener("mousemove", function (e) {
          showTooltip(e, tooltipBridge(b, c || { name: b.bridge_concept_name, confinement_family: confinementFamily }));
        });
        nodeG.addEventListener("mouseleave", hideTooltip);
      })(bridge.bridge_concept_id, bridge, concept);

      _nodesGroup.appendChild(nodeG);

      // Fade in (after appending so transition triggers)
      (function (eG, nG) {
        requestAnimationFrame(function () {
          eG.style.opacity = "1";
          nG.style.opacity = "1";
        });
      })(edgeG, nodeG);
    }
  }

  function clearBridges() {
    if (!_svg) return;

    // Remove comparing highlight from all neighbors
    var comparing = _svg.querySelectorAll(".ng-node--comparing");
    for (var i = 0; i < comparing.length; i++) {
      comparing[i].classList.remove("ng-node--comparing");
    }

    // Fade out bridge nodes and edges, then remove
    var bridgeNodes = _svg.querySelectorAll(".ng-node--bridge");
    var bridgeEdges = _svg.querySelectorAll(".ng-edge--bridge");

    function removeAfterFade(els) {
      for (var j = 0; j < els.length; j++) {
        els[j].style.opacity = "0";
      }
      // Remove from DOM after transition
      setTimeout(function () {
        for (var j = 0; j < els.length; j++) {
          if (els[j].parentNode) els[j].parentNode.removeChild(els[j]);
        }
      }, 350);
    }

    removeAfterFade(bridgeNodes);
    removeAfterFade(bridgeEdges);
  }

  function highlightBridge(conceptId) {
    if (!_svg) return;
    var node = _svg.querySelector('.ng-node--bridge[data-concept-id="' + conceptId + '"]');
    if (!node) return;
    node.classList.add("ng-node--highlighted");
    setTimeout(function () {
      node.classList.remove("ng-node--highlighted");
    }, 1500);
  }

  // ---------------------------------------------------------------------------
  // Cleanup
  // ---------------------------------------------------------------------------

  function destroy() {
    if (_svg && _svg.parentNode) {
      _svg.parentNode.removeChild(_svg);
    }
    _svg = null;
    _container = null;
    _layout = null;
    _focusedConcept = null;
    _neighbors = null;
    _registry = null;
    _callbacks = null;
    _edgesGroup = null;
    _nodesGroup = null;
    _neighborIndexById = {};
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
    destroy: destroy
  };
})();
