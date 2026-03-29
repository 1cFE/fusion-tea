"use strict";

/**
 * Taxonomy card and similarity card components.
 *
 * Exported:
 *   TaxonomyCards.renderTaxonomyCard(container, concept)
 *   TaxonomyCards.renderSimilarityCard(container, report, onConceptClick)
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

  /**
   * Build a single similarity entry (one neighbor).
   */
  function buildSimilarityEntry(entry, onConceptClick) {
    var wrapper = el("div", "similarity-entry");
    wrapper.setAttribute("role", "button");
    wrapper.setAttribute("tabindex", "0");

    // Header: name + badge + score
    var header = el("div", "similarity-entry__header");
    var nameEl = el("span", "similarity-entry__name", entry.concept_name);
    var famCls = FAMILY_BADGE_CLS[entry.confinement_family] || "badge badge-nonstandard";
    var badge = el("span", famCls, entry.confinement_family);
    badge.style.flexShrink = "0";
    var score = el("span", "similarity-entry__score",
      Math.round(entry.comparison.overall_score * 100) + "%");

    header.appendChild(nameEl);
    header.appendChild(badge);
    header.appendChild(score);
    wrapper.appendChild(header);

    // Dimension bars
    var dims = el("div", "similarity-entry__dims");
    var dimList = entry.comparison.dimensions;
    for (var i = 0; i < dimList.length; i++) {
      var d = dimList[i];
      var bar = el("div", "similarity-bar");

      var label = el("span", "similarity-bar__label",
        DIMENSION_LABELS[d.dimension] || d.dimension);

      var track = el("div", "similarity-bar__track");
      var fill = el("div", "similarity-bar__fill");
      var pct = d.comparable > 0 ? (d.matches / d.comparable * 100) : 0;
      fill.style.width = pct + "%";
      track.appendChild(fill);

      var ratio = el("span", "similarity-bar__ratio",
        d.matches + "/" + d.comparable);

      bar.appendChild(label);
      bar.appendChild(track);
      bar.appendChild(ratio);
      dims.appendChild(bar);
    }
    wrapper.appendChild(dims);

    // Bridges
    if (entry.bridges && entry.bridges.length > 0) {
      for (var b = 0; b < entry.bridges.length; b++) {
        var bridge = entry.bridges[b];
        var bridgeEl = el("div", "similarity-bridge");

        var fieldLabel = el("span", "similarity-bridge__field",
          "Differs on " + bridge.mismatched_field.replace(/_/g, " ") + " \u2192 ");
        bridgeEl.appendChild(fieldLabel);

        var conceptLink = el("span", "similarity-bridge__concept",
          bridge.bridge_concept_name);
        conceptLink.setAttribute("data-concept-id", bridge.bridge_concept_id);
        conceptLink.addEventListener("click", (function (cid) {
          return function (e) {
            e.stopPropagation();
            if (onConceptClick) onConceptClick(cid);
          };
        })(bridge.bridge_concept_id));
        bridgeEl.appendChild(conceptLink);

        wrapper.appendChild(bridgeEl);
      }
    }

    // Click to select this neighbor
    function select() {
      if (onConceptClick) onConceptClick(entry.concept_id);
    }
    wrapper.addEventListener("click", select);
    wrapper.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        select();
      }
    });

    return wrapper;
  }

  /**
   * Render the similarity card for a concept's nearest neighbors.
   */
  function renderSimilarityCard(container, report, onConceptClick) {
    container.innerHTML = "";
    if (!report || !report.nearest || report.nearest.length === 0) return;

    var card = el("div", "similarity-card");
    card.appendChild(el("div", "similarity-card__title", "Similar Concepts"));

    for (var i = 0; i < report.nearest.length; i++) {
      card.appendChild(buildSimilarityEntry(report.nearest[i], onConceptClick));
    }

    container.appendChild(card);
  }

  return {
    renderTaxonomyCard: renderTaxonomyCard,
    renderSimilarityCard: renderSimilarityCard
  };
})();
