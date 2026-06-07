/**
 * ontology_palette.js — the shared ontology color + facet vocabulary (A2).
 *
 * Three exports, all consumed by B1's matrix and C1's constellation (no widget
 * in Theme A):
 *   - window.ontologyPalette  family + per-dimension color maps
 *   - window.facetModel       the facetable dimensions, each value→{label,color}
 *   - window.filterState      the selected-facets schema + helpers
 *
 * SINGLE COLOR AUTHORITY: every color is read from the CSS `:root` tokens in
 * explorer.css via getComputedStyle — no color hex is hard-coded in JS. This is
 * the A2 dedup: the former 5× copies of FAMILY_COLORS (constellation, graph,
 * view_capex/summary/sensitivity) now all read `ontologyPalette.family`, which
 * resolves to the same `--color-badge-*` tokens the CSS badges use → zero visual
 * change. Dimension colors trace to concept_ontology_v3.png (its generator's
 * PALETTES dict; see the :root comment). Loaded after the stylesheet, before the
 * surface scripts.
 */

"use strict";

(function () {
  var rootStyle = getComputedStyle(document.documentElement);

  /** Read a :root custom property; warn loudly if it's missing (no silent ""). */
  function tok(name) {
    var v = rootStyle.getPropertyValue(name).trim();
    if (!v) console.error("[ontology_palette] missing CSS token: " + name);
    return v;
  }

  var NA = tok("--onto-na");
  var TBD = tok("--onto-tbd");

  // Family — derived from the CSS authority so no family hex lives in JS.
  var family = {
    MFE: tok("--color-badge-mfe"),
    IFE: tok("--color-badge-ife"),
    MIF: tok("--color-badge-mif"),
    NONSTANDARD: tok("--color-badge-nonstandard"),
  };

  // Dimension palettes, keyed by the taxonomy enum VALUE (taxonomy_models.py).
  var fuel = {
    DT: tok("--onto-fuel-dt"),
    DD: tok("--onto-fuel-dd"),
    DHe3: tok("--onto-fuel-dhe3"),
    PB11: tok("--onto-fuel-pb11"),
    OTHER: NA,
  };
  var magnet = {
    "HTS (wound)": tok("--onto-magnet-hts-wound"),
    "HTS (3D stellarator)": tok("--onto-magnet-hts-3d"),
    "HTS (planar array)": tok("--onto-magnet-hts-planar"),
    "HTS (levitated dipole)": tok("--onto-magnet-hts-dipole"),
    LTS: tok("--onto-magnet-lts"),
    "LTS+HTS": tok("--onto-magnet-lts-hts"),
    Resistive: tok("--onto-magnet-resistive"),
    None: tok("--onto-magnet-none"),
    Electrostatic: tok("--onto-magnet-electrostatic"),
    "N/A": NA,
    TBD: TBD,
    Unknown: NA,
  };
  var driver = {
    Magnetic: tok("--onto-driver-magnetic"),
    "Magnetic pinch": tok("--onto-driver-magnetic-pinch"),
    "DPSSL Laser": tok("--onto-driver-dpssl-laser"),
    "Gas Laser": tok("--onto-driver-gas-laser"),
    "Ion/particle beam": tok("--onto-driver-ion-beam"),
    "Mechanical/kinetic": tok("--onto-driver-mechanical"),
    Electrostatic: tok("--onto-driver-electrostatic"),
    Other: tok("--onto-driver-other"),
    TBD: TBD,
  };
  var capture = {
    "Thermal (steam)": tok("--onto-capture-thermal-steam"),
    "Thermal (unspecified)": tok("--onto-capture-thermal-unspec"),
    "Thermal (sCO2)": tok("--onto-capture-thermal-sco2"),
    "Direct (inductive)": tok("--onto-capture-direct-inductive"),
    "Direct (charged particle)": tok("--onto-capture-direct-charged"),
    "Hybrid (thermal + direct)": tok("--onto-capture-hybrid"),
    TBD: TBD,
  };
  var blanket = {
    "Liquid metal": tok("--onto-blanket-liquid-metal"),
    "Molten salt": tok("--onto-blanket-molten-salt"),
    "Solid breeder": tok("--onto-blanket-solid-breeder"),
    "Other/hybrid": tok("--onto-blanket-other-hybrid"),
    "N/A (no tritium)": NA,
    "N/A (non-power)": NA,
    TBD: TBD,
  };
  var opMode = {
    "Steady-state": tok("--onto-opmode-steady"),
    "Quasi-steady": tok("--onto-opmode-quasi-steady"),
    Pulsed: tok("--onto-opmode-pulsed"),
    TBD: TBD,
  };
  var repRate = {
    "Sub-Hz": tok("--onto-reprate-sub-hz"),
    "~1 Hz": tok("--onto-reprate-1hz"),
    "~10 Hz": tok("--onto-reprate-10hz"),
    "High (>10 Hz)": tok("--onto-reprate-high"),
    kHz: tok("--onto-reprate-khz"),
    Unknown: NA,
  };
  var fitGrade = {
    High: tok("--onto-fit-high"),
    Med: tok("--onto-fit-med"),
    Low: tok("--onto-fit-low"),
    None: tok("--onto-fit-none"),
  };
  var hasCostModel = {
    true: tok("--onto-hascost-true"),
    false: tok("--onto-hascost-false"),
  };

  var ontologyPalette = {
    family: family,
    fuel: fuel,
    magnet: magnet,
    driver: driver,
    capture: capture,
    blanket: blanket,
    opMode: opMode,
    repRate: repRate,
    fitGrade: fitGrade,
    hasCostModel: hasCostModel,
    na: NA,
    tbd: TBD,
  };

  // ---- Facet model ---------------------------------------------------------
  // Each facet: {key, label, field, values:[{value,label,color}]}. `field` is
  // the concept-payload attribute the facet reads (for B1/C1 filtering).

  var FUEL_LABELS = { DT: "D-T", DD: "D-D", DHe3: "D-He3", PB11: "p-B11", OTHER: "Other" };
  var FAMILY_LABELS = {
    MFE: "Magnetic (MFE)",
    IFE: "Inertial (IFE)",
    MIF: "Magneto-Inertial (MIF)",
    NONSTANDARD: "Non-Standard",
  };

  function valuesFrom(palette, labels) {
    return Object.keys(palette).map(function (v) {
      return { value: v, label: (labels && labels[v]) || v, color: palette[v] };
    });
  }

  var facetModel = [
    { key: "family", label: "Confinement Family", field: "confinement_family", values: valuesFrom(family, FAMILY_LABELS) },
    { key: "fuel", label: "Fuel", field: "fuel", values: valuesFrom(fuel, FUEL_LABELS) },
    { key: "magnet", label: "Magnet", field: "magnet_type", values: valuesFrom(magnet, null) },
    { key: "driver", label: "Driver", field: "driver_type", values: valuesFrom(driver, null) },
    { key: "capture", label: "Energy Capture", field: "energy_capture", values: valuesFrom(capture, null) },
    { key: "blanket", label: "Blanket", field: "blanket_config", values: valuesFrom(blanket, null) },
    { key: "opMode", label: "Operation Mode", field: "operation_mode", values: valuesFrom(opMode, null) },
    { key: "repRate", label: "Repetition Rate", field: "repetition_rate", values: valuesFrom(repRate, null) },
    { key: "fitGrade", label: "Archetype Fit", field: "fit_grade", values: valuesFrom(fitGrade, null) },
    {
      key: "hasCostModel",
      label: "Cost Model",
      field: "has_cost_model",
      values: [
        { value: "true", label: "Has cost model", color: hasCostModel.true },
        { value: "false", label: "No cost model", color: hasCostModel.false },
      ],
    },
  ];

  // ---- Filter-state model --------------------------------------------------
  // Schema: { <facetKey>: Set<value> }. Empty selection on a facet = no
  // constraint. Matching is AND across facets, OR within a facet. No widget.

  function createFilterState() {
    var s = {};
    facetModel.forEach(function (f) {
      s[f.key] = new Set();
    });
    return s;
  }
  function toggleFilter(state, key, value) {
    if (!state[key]) state[key] = new Set();
    if (state[key].has(value)) state[key].delete(value);
    else state[key].add(value);
    return state;
  }
  function isFilterEmpty(state) {
    return facetModel.every(function (f) {
      return !state[f.key] || state[f.key].size === 0;
    });
  }
  /**
   * @param state        a filter state from createFilterState()
   * @param facetValues  {<facetKey>: <value>} extracted from one concept
   * @returns true if the concept passes the filter
   */
  function matchesFilter(state, facetValues) {
    return facetModel.every(function (f) {
      var sel = state[f.key];
      if (!sel || sel.size === 0) return true;
      return sel.has(facetValues[f.key]);
    });
  }

  var filterState = {
    create: createFilterState,
    toggle: toggleFilter,
    isEmpty: isFilterEmpty,
    matches: matchesFilter,
  };

  window.ontologyPalette = ontologyPalette;
  window.facetModel = facetModel;
  window.filterState = filterState;
})();
