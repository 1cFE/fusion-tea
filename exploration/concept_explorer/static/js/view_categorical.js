/**
 * view_categorical.js — Categorical comparison view.
 *
 * Compares taxonomy attributes across selected concepts.
 *   - Integrated mode: single comparison table (concepts as columns, fields as rows)
 *   - Landscape mode: per-concept attribute card
 *
 * Data source: /api/taxonomy/registry (fetched once, cached).
 * Registers on window.VIEW_REGISTRY.categorical.
 */

"use strict";

(function () {
  // ---------------------------------------------------------------------------
  // DOM helpers (same pattern as comparison.js:89-101)
  // ---------------------------------------------------------------------------

  function el(tag, cls, text) {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  function append(parent, ...children) {
    for (const c of children) {
      if (c != null) parent.appendChild(c);
    }
    return parent;
  }

  // ---------------------------------------------------------------------------
  // Constants
  // ---------------------------------------------------------------------------

  const FAMILY_META = {
    MFE: { label: "MFE", cls: "badge badge-mfe" },
    IFE: { label: "IFE", cls: "badge badge-ife" },
    MIF: { label: "MIF", cls: "badge badge-mif" },
    NONSTANDARD: { label: "Non-std", cls: "badge badge-nonstandard" },
  };

  /**
   * All taxonomy fields in display order.
   * `applicableTo` — if set, the field is only relevant when the concept's
   * confinement_family matches. Inapplicable fields render "—"; applicable
   * but null fields render "N/A".
   */
  const TAXONOMY_FIELDS = [
    // Hierarchical
    { field: "confinement_family", label: "Confinement" },
    { field: "mfe_topology",      label: "MFE Topology",     applicableTo: "MFE" },
    { field: "tokamak_shape",     label: "Tokamak Shape",    applicableTo: "MFE" },
    { field: "stellarator_type",  label: "Stellarator Type", applicableTo: "MFE" },
    { field: "ife_driver",        label: "IFE Driver",       applicableTo: "IFE" },
    { field: "laser_approach",    label: "Laser Approach",   applicableTo: "IFE" },
    { field: "mif_method",        label: "MIF Method",       applicableTo: "MIF" },
    { field: "non_standard_mechanism", label: "Mechanism",   applicableTo: "NONSTANDARD" },
    // Cross-cutting
    { field: "fuel",              label: "Fuel" },
    { field: "primary_heating",   label: "Primary Heating" },
    { field: "energy_capture",    label: "Energy Capture" },
    { field: "plasma_state",      label: "Plasma State" },
    { field: "magnet_type",       label: "Magnet Type" },
    { field: "tritium_breeding",  label: "Tritium Breeding" },
    { field: "neutron_management", label: "Neutron Mgmt" },
    { field: "operation_mode",    label: "Operation Mode" },
    { field: "repetition_rate",   label: "Rep Rate" },
    { field: "driver_technology", label: "Driver Tech" },
    // Metadata
    { field: "confidence",        label: "Confidence" },
  ];

  // ---------------------------------------------------------------------------
  // Taxonomy data cache
  // ---------------------------------------------------------------------------

  /** @type {Record<string, Object>|null} concept_id → taxonomy object */
  let _taxonomyCache = null;

  async function ensureTaxonomy() {
    if (_taxonomyCache) return _taxonomyCache;
    const resp = await fetch("/api/taxonomy/registry");
    if (!resp.ok) throw new Error("Failed to fetch taxonomy registry");
    const data = await resp.json();
    _taxonomyCache = {};
    for (const c of data.concepts) {
      const key = c.concept_id;
      _taxonomyCache[key] = c;
    }
    return _taxonomyCache;
  }

  // ---------------------------------------------------------------------------
  // Helpers
  // ---------------------------------------------------------------------------

  /**
   * Filter TAXONOMY_FIELDS to those visible for a given set of concepts.
   * Hierarchical sub-type fields are shown only when at least one concept
   * in the comparison has a matching confinement_family.
   */
  function getVisibleFields(concepts, taxonomyData) {
    const familiesPresent = new Set();
    for (const c of concepts) {
      const tax = taxonomyData[c.concept_id];
      if (tax) familiesPresent.add(tax.confinement_family);
    }

    return TAXONOMY_FIELDS.filter((f) => {
      if (!f.applicableTo) return true;
      return familiesPresent.has(f.applicableTo);
    });
  }

  /**
   * Determine cell state for a taxonomy value.
   * Returns { text, cls } for rendering.
   */
  function cellState(value, field, conceptFamily) {
    // Inapplicable hierarchical field
    if (field.applicableTo && field.applicableTo !== conceptFamily) {
      return { text: "\u2014", cls: "val--na" }; // "—"
    }
    // Null on applicable field
    if (value === null || value === undefined) {
      return { text: "N/A", cls: "val--tbd" };
    }
    // TBD / Unknown string
    if (value === "TBD" || value === "Unknown") {
      return { text: value, cls: "val--tbd" };
    }
    // Normal value
    return { text: String(value), cls: null };
  }

  /**
   * Check whether all concept values for a field are the same.
   */
  function allMatch(concepts, taxonomyData, field) {
    const vals = concepts.map((c) => {
      const tax = taxonomyData[c.concept_id];
      return tax ? tax[field.field] : null;
    });
    // Treat null/undefined as equivalent for matching purposes
    const normalized = vals.map((v) =>
      v === null || v === undefined ? "__null__" : String(v)
    );
    return new Set(normalized).size <= 1;
  }

  // ---------------------------------------------------------------------------
  // Integrated mode — comparison table
  // ---------------------------------------------------------------------------

  function renderIntegratedTable(container, concepts, taxonomyData) {
    const fields = getVisibleFields(concepts, taxonomyData);

    const table = el("table", "comparison-table");

    // Header
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    headerRow.appendChild(el("th", "attr-label", "Attribute"));

    for (const c of concepts) {
      const th = document.createElement("th");
      const familyInfo = FAMILY_META[c.confinement_family] ?? {
        label: c.confinement_family,
        cls: "badge badge-nonstandard",
      };
      append(th, el("span", null, c.name + " "), el("span", familyInfo.cls, familyInfo.label));
      headerRow.appendChild(th);
    }

    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Body
    const tbody = document.createElement("tbody");

    for (const field of fields) {
      const tr = document.createElement("tr");

      // Diff/match row highlighting
      const match = allMatch(concepts, taxonomyData, field);
      tr.className = match ? "match" : "diff";

      // Label cell
      tr.appendChild(el("td", "attr-label", field.label));

      // Value cells
      for (const c of concepts) {
        const tax = taxonomyData[c.concept_id];
        const value = tax ? tax[field.field] : null;
        const state = cellState(value, field, c.confinement_family);

        const td = el("td", state.cls, state.text);
        if (!state.cls) {
          // Normal value — use text-col class (non-mono font for taxonomy strings)
          td.className = "text-col";
        }
        tr.appendChild(td);
      }

      tbody.appendChild(tr);
    }

    table.appendChild(tbody);
    container.appendChild(table);
  }

  // ---------------------------------------------------------------------------
  // Landscape mode — attribute card
  // ---------------------------------------------------------------------------

  function renderLandscapeCard(container, concept, taxonomyData) {
    const tax = taxonomyData[concept.concept_id];
    if (!tax) {
      container.appendChild(el("div", "view-no-data", "No taxonomy data available"));
      return;
    }

    const card = el("div", "taxonomy-card__attrs");

    for (const field of TAXONOMY_FIELDS) {
      // Skip inapplicable hierarchical fields entirely in landscape mode
      if (field.applicableTo && field.applicableTo !== tax.confinement_family) {
        continue;
      }

      const value = tax[field.field];
      const state = cellState(value, field, tax.confinement_family);

      const row = el("div", "taxonomy-card__attr");
      row.appendChild(el("span", "taxonomy-card__label", field.label));

      const valCls = state.cls === "val--na"
        ? "taxonomy-card__value taxonomy-card__value--na"
        : state.cls === "val--tbd"
          ? "taxonomy-card__value taxonomy-card__value--tbd"
          : "taxonomy-card__value";
      row.appendChild(el("span", valCls, state.text));

      card.appendChild(row);
    }

    container.appendChild(card);
  }

  // ---------------------------------------------------------------------------
  // Render entry points (async — handle taxonomy fetch internally)
  // ---------------------------------------------------------------------------

  function renderIntegrated(container, concepts) {
    container.innerHTML = "";
    const loading = el("div", "text-muted text-sm", "Loading taxonomy\u2026");
    container.appendChild(loading);

    ensureTaxonomy()
      .then((taxonomyData) => {
        container.innerHTML = "";
        renderIntegratedTable(container, concepts, taxonomyData);
      })
      .catch((err) => {
        console.error("[categorical] Failed to load taxonomy:", err);
        container.innerHTML = "";
        container.appendChild(el("div", "view-no-data", "Failed to load taxonomy data"));
      });
  }

  function renderLandscape(container, concept, _syncContext) {
    container.innerHTML = "";
    const loading = el("div", "text-muted text-sm", "Loading\u2026");
    container.appendChild(loading);

    ensureTaxonomy()
      .then((taxonomyData) => {
        container.innerHTML = "";
        renderLandscapeCard(container, concept, taxonomyData);
      })
      .catch((err) => {
        console.error("[categorical] Failed to load taxonomy:", err);
        container.innerHTML = "";
        container.appendChild(el("div", "view-no-data", "Failed to load taxonomy data"));
      });
  }

  // ---------------------------------------------------------------------------
  // Register on VIEW_REGISTRY
  // ---------------------------------------------------------------------------

  window.VIEW_REGISTRY.categorical.renderIntegrated = renderIntegrated;
  window.VIEW_REGISTRY.categorical.renderLandscape = renderLandscape;
})();
