"use strict";

/**
 * Constellation scatter plot component.
 *
 * Uses Plotly to render the 2D MDS projection of concept similarity.
 * One trace per confinement family for legend grouping and coloring.
 *
 * Exported:
 *   Constellation.render(container, data, onConceptClick, onDoubleClick)
 *   Constellation.highlight(conceptId)
 */
var Constellation = (function () {
  var _container = null;
  var _data = null;
  var _selectedId = null;

  // Debounced click state for double-click detection
  var _clickTimer = null;
  var _lastClickId = null;
  var DBLCLICK_DELAY = 300;

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

  function render(container, constellationData, onConceptClick, onDoubleClick, onCtrlClick) {
    _container = container;
    _data = constellationData;
    _selectedId = null;

    // Group points by family
    var byFamily = {};
    var points = constellationData.points;
    for (var i = 0; i < points.length; i++) {
      var p = points[i];
      var fam = p.confinement_family;
      if (!byFamily[fam]) byFamily[fam] = [];
      byFamily[fam].push(p);
    }

    // Build one trace per family
    var traces = [];
    var families = ["MFE", "IFE", "MIF", "NONSTANDARD"];
    for (var f = 0; f < families.length; f++) {
      var fam = families[f];
      var pts = byFamily[fam] || [];
      if (pts.length === 0) continue;

      traces.push({
        x: pts.map(function (p) { return p.x; }),
        y: pts.map(function (p) { return p.y; }),
        text: pts.map(function (p) { return p.name; }),
        customdata: pts.map(function (p) { return p.concept_id; }),
        mode: "markers",
        type: "scatter",
        name: FAMILY_LABELS[fam] || fam,
        marker: {
          color: FAMILY_COLORS[fam] || "#6b7280",
          size: 10,
          opacity: 0.85,
          line: { width: 1, color: "rgba(255,255,255,0.2)" }
        },
        hovertemplate: "<b>%{text}</b><extra>" + (FAMILY_LABELS[fam] || fam) + "</extra>"
      });
    }

    var layout = {
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(0,0,0,0)",
      font: { color: "#8b949e", family: "-apple-system, BlinkMacSystemFont, sans-serif" },
      margin: { l: 30, r: 120, t: 30, b: 30 },
      xaxis: {
        showgrid: true,
        gridcolor: "rgba(48,54,61,0.5)",
        zeroline: false,
        showticklabels: false,
        title: ""
      },
      yaxis: {
        showgrid: true,
        gridcolor: "rgba(48,54,61,0.5)",
        zeroline: false,
        showticklabels: false,
        title: ""
      },
      legend: {
        orientation: "v",
        x: 1.02,
        y: 1,
        font: { size: 13 }
      },
      hovermode: "closest",
      dragmode: "pan",
      annotations: []
    };

    var config = {
      responsive: true,
      displayModeBar: false,
      scrollZoom: true,
      doubleClick: false // disable Plotly's built-in double-click zoom reset
    };

    Plotly.newPlot(container, traces, layout, config);

    // Click handler with debounced double-click detection
    container.on("plotly_click", function (eventData) {
      if (!eventData.points || eventData.points.length === 0) return;

      var pt = eventData.points[0];
      var conceptId = pt.customdata;
      if (!conceptId) return;

      // Ctrl/Cmd+click: selection tray (short-circuits debounce)
      var nativeEvent = eventData.event;
      if (nativeEvent && (nativeEvent.metaKey || nativeEvent.ctrlKey)) {
        if (onCtrlClick) onCtrlClick(conceptId, nativeEvent);
        return;
      }

      if (_clickTimer && _lastClickId === conceptId) {
        // Second click on same point within delay — double-click
        clearTimeout(_clickTimer);
        _clickTimer = null;
        _lastClickId = null;
        if (onDoubleClick) onDoubleClick(conceptId);
      } else {
        // First click — start timer
        if (_clickTimer) clearTimeout(_clickTimer);
        _lastClickId = conceptId;
        _clickTimer = setTimeout(function () {
          _clickTimer = null;
          _lastClickId = null;
          // Single-click: highlight in constellation
          if (onConceptClick) onConceptClick(conceptId);
        }, DBLCLICK_DELAY);
      }
    });
  }

  function highlight(conceptId) {
    if (!_container || !_data) return;
    _selectedId = conceptId;

    var points = _data.points;
    // Build size and opacity arrays per family group
    var byFamily = {};
    for (var i = 0; i < points.length; i++) {
      var p = points[i];
      if (!byFamily[p.confinement_family]) byFamily[p.confinement_family] = [];
      byFamily[p.confinement_family].push(p);
    }

    var families = ["MFE", "IFE", "MIF", "NONSTANDARD"];
    var traceIdx = 0;

    for (var f = 0; f < families.length; f++) {
      var fam = families[f];
      var pts = byFamily[fam] || [];
      if (pts.length === 0) continue;

      var sizes = [];
      var opacities = [];
      for (var j = 0; j < pts.length; j++) {
        if (pts[j].concept_id === conceptId) {
          sizes.push(16);
          opacities.push(1.0);
        } else {
          sizes.push(10);
          opacities.push(conceptId ? 0.5 : 0.85);
        }
      }

      Plotly.restyle(_container, {
        "marker.size": [sizes],
        "marker.opacity": [opacities]
      }, [traceIdx]);

      traceIdx++;
    }
  }

  /**
   * Update visual ring indicators on selected constellation dots.
   */
  function updateTrayIndicators(selectedIds) {
    if (!_container || !_data) return;

    var idSet = {};
    for (var i = 0; i < selectedIds.length; i++) {
      idSet[selectedIds[i]] = true;
    }

    var points = _data.points;
    var byFamily = {};
    for (var k = 0; k < points.length; k++) {
      var p = points[k];
      if (!byFamily[p.confinement_family]) byFamily[p.confinement_family] = [];
      byFamily[p.confinement_family].push(p);
    }

    var families = ["MFE", "IFE", "MIF", "NONSTANDARD"];
    var traceIdx = 0;

    for (var f = 0; f < families.length; f++) {
      var fam = families[f];
      var pts = byFamily[fam] || [];
      if (pts.length === 0) continue;

      var lineWidths = [];
      var lineColors = [];
      for (var j = 0; j < pts.length; j++) {
        if (idSet[pts[j].concept_id]) {
          lineWidths.push(3);
          lineColors.push("#e6edf3");
        } else {
          lineWidths.push(1);
          lineColors.push("rgba(255,255,255,0.2)");
        }
      }

      Plotly.restyle(_container, {
        "marker.line.width": [lineWidths],
        "marker.line.color": [lineColors]
      }, [traceIdx]);

      traceIdx++;
    }
  }

  return {
    render: render,
    highlight: highlight,
    updateTrayIndicators: updateTrayIndicators
  };
})();
