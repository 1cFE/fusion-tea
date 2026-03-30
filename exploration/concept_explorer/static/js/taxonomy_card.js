"use strict";

/**
 * Taxonomy card and comparison panel components.
 *
 * Exported:
 *   TaxonomyCards.renderTaxonomyCard(container, concept)
 *   TaxonomyCards.selectBridges(bridges)
 *   TaxonomyCards.buildComparison(focused, neighbor, similarityResult)
 *   TaxonomyCards.renderNeighborList(container, nearest, onCompare, activeId)
 *   TaxonomyCards.renderComparison(container, focused, neighbor, result, selectedBridges, allNearest, onBridgeHighlight, onCompare)
 *   TaxonomyCards.setRegistry(registry)
 */
var TaxonomyCards = (function () {

  var FAMILY_BADGE_CLS = {
    MFE: "badge badge-mfe",
    IFE: "badge badge-ife",
    MIF: "badge badge-mif",
    NONSTANDARD: "badge badge-nonstandard"
  };

  var ATTR_DISPLAY = [
    { field: "fuel", label: "Fuel" },
    { field: "primary_heating", label: "Heating" },
    { field: "energy_capture", label: "Energy Capture" },
    { field: "plasma_state", label: "Plasma State" },
    { field: "magnet_type", label: "Magnets" },
    { field: "tritium_breeding", label: "Tritium" },
    { field: "neutron_management", label: "Neutrons" },
    { field: "operation_mode", label: "Operation" },
    { field: "repetition_rate", label: "Rep Rate" }
  ];

  var DIMENSION_LABELS = {
    plasma_physics: "Plasma",
    engineering: "Engineering",
    fuel_cycle: "Fuel Cycle",
    operations: "Operations"
  };

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  /**
   * Build hierarchy badges (family + topology/driver + sub-type).
   */
  function buildHierarchyBadges(concept) {
    var badges = el("div", "taxonomy-card__badges");

    // Family badge
    var famCls = FAMILY_BADGE_CLS[concept.confinement_family] || "badge badge-nonstandard";
    badges.appendChild(el("span", famCls, concept.confinement_family));

    // Topology / driver / method
    var hier = concept.mfe_topology || concept.ife_driver || concept.mif_method || concept.non_standard_mechanism;
    if (hier) {
      badges.appendChild(el("span", "badge", hier));
    }

    // Sub-type
    var sub = concept.tokamak_shape || concept.stellarator_type || concept.laser_approach;
    if (sub) {
      badges.appendChild(el("span", "badge", sub));
    }

    return badges;
  }

  /**
   * Render the taxonomy card for a concept.
   */
  function renderTaxonomyCard(container, concept) {
    container.innerHTML = "";
    var card = el("div", "taxonomy-card");

    // Header
    var header = el("div", "taxonomy-card__header");
    header.appendChild(el("div", "taxonomy-card__name", concept.name));
    if (concept.company) {
      header.appendChild(el("div", "taxonomy-card__company", concept.company));
    }
    header.appendChild(buildHierarchyBadges(concept));
    card.appendChild(header);

    // Attribute rows
    var attrs = el("div", "taxonomy-card__attrs");
    for (var i = 0; i < ATTR_DISPLAY.length; i++) {
      var def = ATTR_DISPLAY[i];
      var val = concept[def.field];

      var row = el("div", "taxonomy-card__attr");
      row.appendChild(el("span", "taxonomy-card__label", def.label));

      var valEl;
      if (val === null || val === undefined) {
        valEl = el("span", "taxonomy-card__value taxonomy-card__value--na", "\u2014"); // —
      } else if (val === "TBD" || val === "Unknown") {
        valEl = el("span", "taxonomy-card__value taxonomy-card__value--tbd", val);
      } else {
        valEl = el("span", "taxonomy-card__value", val);
      }
      row.appendChild(valEl);
      attrs.appendChild(row);
    }
    card.appendChild(attrs);

    // Driver technology (de-emphasized)
    if (concept.driver_technology) {
      var driver = el("div", "taxonomy-card__driver");
      driver.appendChild(el("span", "taxonomy-card__label", "Driver: "));
      driver.appendChild(document.createTextNode(concept.driver_technology));
      card.appendChild(driver);
    }

    // Cost model link
    if (concept.cost_model_id) {
      var link = document.createElement("a");
      link.className = "taxonomy-card__link";
      link.href = "/concept/" + concept.cost_model_id;
      link.textContent = "View cost model \u2192";
      card.appendChild(link);
    }

    // Confidence
    var confRow = el("div", "taxonomy-card__attr");
    confRow.style.borderBottom = "none";
    confRow.style.marginTop = "var(--space-2)";
    confRow.appendChild(el("span", "taxonomy-card__label", "Confidence"));
    confRow.appendChild(el("span", "taxonomy-card__value", concept.confidence));
    card.appendChild(confRow);

    container.appendChild(card);
  }

  // ---------------------------------------------------------------------------
  // Field labels (human-readable) and TBD sentinels
  // ---------------------------------------------------------------------------

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

  var TBD_VALUES = { "TBD": true, "Unknown": true };

  // ---------------------------------------------------------------------------
  // Bridge selection algorithm (FR-10)
  // ---------------------------------------------------------------------------

  var MAX_BRIDGES = 3;

  /**
   * Select at most MAX_BRIDGES bridges, each covering a different mismatched
   * field, prioritized by overall similarity to the focused concept.
   */
  function selectBridges(bridges) {
    if (!bridges || bridges.length === 0) return [];

    var sorted = bridges.slice().sort(function (a, b) {
      return (b.bridge_overall_similarity || 0) - (a.bridge_overall_similarity || 0);
    });

    var selected = [];
    var coveredFields = {};

    for (var i = 0; i < sorted.length && selected.length < MAX_BRIDGES; i++) {
      var b = sorted[i];
      if (!coveredFields[b.mismatched_field]) {
        coveredFields[b.mismatched_field] = true;
        selected.push(b);
      }
    }

    return selected;
  }

  // ---------------------------------------------------------------------------
  // Comparison builder
  // ---------------------------------------------------------------------------

  /**
   * Build comparison row data from the focused concept, neighbor concept,
   * and similarity result. Returns an array of row objects.
   */
  function buildComparison(focused, neighbor, similarityResult) {
    var comp = similarityResult.comparison;
    var bridges = similarityResult.bridges || [];
    var rows = [];

    // Build a bridge lookup by mismatched field
    var bridgeByField = {};
    for (var b = 0; b < bridges.length; b++) {
      bridgeByField[bridges[b].mismatched_field] = bridges[b];
    }

    for (var d = 0; d < comp.dimensions.length; d++) {
      var dim = comp.dimensions[d];

      // Mismatched fields first
      for (var m = 0; m < dim.mismatched_fields.length; m++) {
        var field = dim.mismatched_fields[m];
        var focusedVal = focused[field];
        var neighborVal = neighbor ? neighbor[field] : null;

        // Skip N/A and TBD
        if (focusedVal == null || neighborVal == null) continue;
        if (TBD_VALUES[String(focusedVal)] || TBD_VALUES[String(neighborVal)]) continue;

        var bridge = bridgeByField[field] || null;
        rows.push({
          field: field,
          label: FIELD_LABELS[field] || field,
          match: false,
          focusedValue: String(focusedVal),
          neighborValue: bridge ? bridge.similar_value : String(neighborVal),
          bridge: bridge,
          dimension: dim.dimension
        });
      }

      // Matched fields
      for (var k = 0; k < dim.matched_fields.length; k++) {
        var mfield = dim.matched_fields[k];
        var val = focused[mfield];
        if (val == null || TBD_VALUES[String(val)]) continue;

        rows.push({
          field: mfield,
          label: FIELD_LABELS[mfield] || mfield,
          match: true,
          value: String(val),
          dimension: dim.dimension
        });
      }
    }

    return rows;
  }

  // ---------------------------------------------------------------------------
  // Neighbor list (FOCUSED state)
  // ---------------------------------------------------------------------------

  /**
   * Render a compact neighbor list in the comparison container.
   * @param {Element} container
   * @param {Array} nearest - similarity results array
   * @param {Function} onCompare - callback(conceptId)
   * @param {string} [activeId] - currently compared neighbor (for highlight)
   */
  function renderNeighborList(container, nearest, onCompare, activeId) {
    container.innerHTML = "";
    if (!nearest || nearest.length === 0) return;

    var wrapper = el("div", "neighbor-list");
    wrapper.appendChild(el("h3", "neighbor-list__title", "Similar Concepts"));
    wrapper.appendChild(el("p", "neighbor-list__hint", "Click a concept to see how they compare"));

    for (var i = 0; i < nearest.length; i++) {
      var entry = nearest[i];
      var row = el("div", "neighbor-entry");
      row.setAttribute("data-concept-id", entry.concept_id);
      if (entry.concept_id === activeId) {
        row.className += " neighbor-entry--active";
      }

      var famCls = FAMILY_BADGE_CLS[entry.confinement_family] || "badge badge-nonstandard";
      row.appendChild(el("span", famCls, entry.confinement_family));
      row.appendChild(el("span", "neighbor-entry__name", entry.concept_name));
      row.appendChild(el("span", "neighbor-entry__score",
        Math.round(entry.comparison.overall_score * 100) + "%"));

      (function (cid) {
        row.addEventListener("click", function () {
          onCompare(cid);
        });
      })(entry.concept_id);

      wrapper.appendChild(row);
    }

    container.appendChild(wrapper);
  }

  // ---------------------------------------------------------------------------
  // Comparison table (COMPARING state)
  // ---------------------------------------------------------------------------

  /**
   * Render the field-by-field comparison panel.
   * @param {Element} container
   * @param {Object} focused - focused concept from registry
   * @param {Object} neighbor - neighbor concept from registry
   * @param {Object} similarityResult - the SimilarityResult for this neighbor
   * @param {Array} selectedBridges - bridges already selected by selectBridges()
   * @param {Array} allNearest - all nearest neighbors (for "other neighbors" list)
   * @param {Function} onBridgeHighlight - callback(conceptId)
   * @param {Function} onCompare - callback(conceptId) for other neighbor clicks
   */
  function renderComparison(container, focused, neighbor, similarityResult,
                            selectedBridges, allNearest, onBridgeHighlight, onCompare) {
    container.innerHTML = "";

    var panel = el("div", "comparison-panel");

    // Header
    var header = el("div", "comparison-panel__header");
    var h3 = el("h3", null, "Comparing with " + (similarityResult.concept_name || ""));
    header.appendChild(h3);
    var scoreEl = el("span", "comparison-panel__score",
      Math.round(similarityResult.comparison.overall_score * 100) + "% match");
    header.appendChild(scoreEl);
    panel.appendChild(header);

    // Build comparison rows
    var rows = buildComparison(focused, neighbor, similarityResult);

    // Build a lookup of selected bridges by field
    var selectedByField = {};
    if (selectedBridges) {
      for (var s = 0; s < selectedBridges.length; s++) {
        selectedByField[selectedBridges[s].mismatched_field] = selectedBridges[s];
      }
    }

    // Separate diffs and matches
    var diffs = [];
    var matches = [];
    for (var i = 0; i < rows.length; i++) {
      if (rows[i].match) matches.push(rows[i]);
      else diffs.push(rows[i]);
    }

    // Differences section
    if (diffs.length > 0) {
      var diffSection = el("div", "comparison-section comparison-section--diff");
      diffSection.appendChild(el("h4", "comparison-section__title",
        diffs.length + " Difference" + (diffs.length > 1 ? "s" : "")));

      for (var d = 0; d < diffs.length; d++) {
        var row = diffs[d];
        var rowEl = el("div", "comparison-row comparison-row--diff");

        rowEl.appendChild(el("div", "comparison-row__label", row.label));

        var vals = el("div", "comparison-row__values");
        vals.appendChild(el("span", "comparison-row__value comparison-row__value--self", row.focusedValue));
        vals.appendChild(el("span", "comparison-row__vs", "vs"));
        vals.appendChild(el("span", "comparison-row__value comparison-row__value--other", row.neighborValue));
        rowEl.appendChild(vals);

        // Bridge reference (only for selected bridges)
        var selBridge = selectedByField[row.field];
        if (selBridge) {
          var bridgeDiv = el("div", "comparison-row__bridge");
          bridgeDiv.appendChild(document.createTextNode("Also uses " + row.focusedValue + ": "));

          var ref = el("a", "bridge-ref");
          ref.setAttribute("data-concept-id", selBridge.bridge_concept_id);
          ref.setAttribute("data-action", "highlight-bridge");
          ref.textContent = selBridge.bridge_concept_name + " ";

          // Family badge on bridge ref
          var bridgeConcept = null;
          if (typeof _registry !== "undefined" && _registry) {
            bridgeConcept = _registry[selBridge.bridge_concept_id];
          }
          var bridgeFam = bridgeConcept ? bridgeConcept.confinement_family : null;
          if (bridgeFam) {
            var bBadge = el("span",
              FAMILY_BADGE_CLS[bridgeFam] || "badge badge-nonstandard",
              bridgeFam);
            bBadge.style.fontSize = "10px";
            bBadge.style.verticalAlign = "middle";
            ref.appendChild(bBadge);
          }

          (function (cid) {
            ref.addEventListener("click", function (e) {
              e.preventDefault();
              e.stopPropagation();
              if (onBridgeHighlight) onBridgeHighlight(cid);
            });
          })(selBridge.bridge_concept_id);

          bridgeDiv.appendChild(ref);
          rowEl.appendChild(bridgeDiv);
        }

        diffSection.appendChild(rowEl);
      }
      panel.appendChild(diffSection);
    }

    // Matches section
    if (matches.length > 0) {
      var matchSection = el("div", "comparison-section comparison-section--match");
      matchSection.appendChild(el("h4", "comparison-section__title",
        matches.length + " matching attribute" + (matches.length > 1 ? "s" : "")));

      for (var j = 0; j < matches.length; j++) {
        var mrow = matches[j];
        var mEl = el("div", "comparison-row comparison-row--match");
        mEl.appendChild(el("span", "comparison-row__label", mrow.label));
        mEl.appendChild(el("span", "comparison-row__value", mrow.value));
        mEl.appendChild(el("span", "comparison-row__check", "\u2713"));
        matchSection.appendChild(mEl);
      }
      panel.appendChild(matchSection);
    }

    // Other neighbors (compact list)
    if (allNearest && allNearest.length > 1) {
      var others = allNearest.filter(function (n) {
        return n.concept_id !== similarityResult.concept_id;
      });
      if (others.length > 0) {
        var otherList = el("div", "neighbor-list neighbor-list--compact");
        otherList.appendChild(el("h4", "neighbor-list__title", "Other Neighbors"));

        for (var k = 0; k < others.length; k++) {
          var other = others[k];
          var oRow = el("div", "neighbor-entry");
          oRow.setAttribute("data-concept-id", other.concept_id);

          var oFamCls = FAMILY_BADGE_CLS[other.confinement_family] || "badge badge-nonstandard";
          oRow.appendChild(el("span", oFamCls, other.confinement_family));
          oRow.appendChild(el("span", "neighbor-entry__name", other.concept_name));
          oRow.appendChild(el("span", "neighbor-entry__score",
            Math.round(other.comparison.overall_score * 100) + "%"));

          (function (cid) {
            oRow.addEventListener("click", function () {
              if (onCompare) onCompare(cid);
            });
          })(other.concept_id);

          otherList.appendChild(oRow);
        }
        panel.appendChild(otherList);
      }
    }

    container.appendChild(panel);
  }

  // ---------------------------------------------------------------------------
  // Module-level registry reference (set by orchestrator via setRegistry)
  // ---------------------------------------------------------------------------

  var _registry = null;

  function setRegistry(registry) {
    _registry = registry;
  }

  // ---------------------------------------------------------------------------
  // Public API
  // ---------------------------------------------------------------------------

  return {
    renderTaxonomyCard: renderTaxonomyCard,
    selectBridges: selectBridges,
    buildComparison: buildComparison,
    renderNeighborList: renderNeighborList,
    renderComparison: renderComparison,
    setRegistry: setRegistry
  };
})();
