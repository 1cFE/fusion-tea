"use strict";

/**
 * Constellation scatter plot component.
 *
 * Uses Plotly to render the 2D MDS projection of concept similarity.
 * One trace per confinement family for legend grouping and coloring.
 *
 * Exported:
 *   Constellation.render(container, data, onConceptClick)
 *   Constellation.highlight(conceptId)
 */
var Constellation = (function () {
  var _container = null;
  var _data = null;
  var _selectedId = null;

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

  function render(container, constellationData, onConceptClick) {
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
      margin: { l: 30, r: 20, t: 30, b: 30 },
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
        orientation: "h",
        y: -0.05,
        font: { size: 11 }
      },
      hovermode: "closest",
      dragmode: "pan"
    };

    var config = {
      responsive: true,
      displayModeBar: false,
      scrollZoom: true
    };

    Plotly.newPlot(container, traces, layout, config);

    // Click handler
    container.on("plotly_click", function (eventData) {
      if (eventData.points && eventData.points.length > 0) {
        var pt = eventData.points[0];
        var conceptId = pt.customdata;
        if (conceptId && onConceptClick) {
          onConceptClick(conceptId);
        }
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
    var update = {};

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

  return {
    render: render,
    highlight: highlight
  };
})();
