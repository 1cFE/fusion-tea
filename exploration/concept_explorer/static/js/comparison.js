/**
 * comparison.js — Comparison view controller.
 *
 * Manages a set of up to 4 selected concepts and renders side-by-side
 * sensitivity tornado charts, CAS cost breakdowns, and a headline economics table.
 *
 * Data is fetched lazily: the manifest on page load, each concept's full data
 * only when it is added to the comparison set.  The comparison set is synced to
 * POST /api/state on every add/remove.
 *
 * Depends on:
 *   - tornado.js       (renderTornado)
 *   - cas_breakdown.js (renderCASBreakdown)
 *   - explorer.css     (badge, tab, comparison-* classes)
 */

"use strict";

(function () {
  // ---------------------------------------------------------------------------
  // State
  // ---------------------------------------------------------------------------

  /** @type {string[]} Selected concept IDs, ordered by insertion. Max 4. */
  let comparisonSet = [];

  /** @type {Record<string, Object>} Lazily populated ConceptData cache. */
  let conceptCache = {};

  /** @type {Object|null} ConceptManifest fetched on init. */
  let manifest = null;

  /** @type {string} Currently active tab name. */
  let activeTab = "sensitivity";

  /** @type {boolean} Whether the inline concept picker is open. */
  let pickerOpen = false;

  // ---------------------------------------------------------------------------
  // Display metadata (mirrors concept_page.js — confinement_family enum values
  // are uppercase in ConceptData, lowercase in ConceptManifestEntry)
  // ---------------------------------------------------------------------------

  /** Maps both uppercase (ConceptData) and lowercase (manifest) family values. */
  const FAMILY_META = {
    MFE: { label: "MFE", cls: "badge badge-mfe" },
    IFE: { label: "IFE", cls: "badge badge-ife" },
    MIF: { label: "MIF", cls: "badge badge-mif" },
    NONSTANDARD: { label: "Non-std", cls: "badge badge-nonstandard" },
    mfe: { label: "MFE", cls: "badge badge-mfe" },
    ife: { label: "IFE", cls: "badge badge-ife" },
    mif: { label: "MIF", cls: "badge badge-mif" },
    nonstandard: { label: "Non-std", cls: "badge badge-nonstandard" },
  };

  const CONFIDENCE_BADGE = {
    high: { label: "High", cls: "badge badge-confidence badge-confidence--high" },
    medium: { label: "Med", cls: "badge badge-confidence badge-confidence--medium" },
    low: { label: "Low", cls: "badge badge-confidence badge-confidence--low" },
  };

  // Top-level CAS account keys — must match models.py CAS_NAMES ordering
  const CAS_KEYS = [
    "cas10", "cas21", "cas22", "cas23", "cas24", "cas25",
    "cas26", "cas27", "cas28", "cas29", "cas30",
    "cas40", "cas50", "cas60", "cas70", "cas80", "cas90",
  ];

  // ---------------------------------------------------------------------------
  // DOM helpers
  // ---------------------------------------------------------------------------

  /** Create element with optional className and text content. */
  function el(tag, cls, text) {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  /** Append multiple children to a parent. */
  function append(parent, ...children) {
    for (const c of children) {
      if (c != null) parent.appendChild(c);
    }
    return parent;
  }

  // ---------------------------------------------------------------------------
  // API helpers
  // ---------------------------------------------------------------------------

  /**
   * Sync comparison set to server state.
   * Fires-and-forgets — comparison view doesn't depend on the server ACK.
   */
  function postState() {
    fetch("/api/state", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        current_concept_id: null,
        slider_overrides: {},
        comparison_set: [...comparisonSet],
        timestamp: "",
      }),
    }).catch((err) => console.warn("[compare] POST /api/state failed:", err));
  }

  async function fetchManifest() {
    const resp = await fetch("/api/manifest");
    if (!resp.ok) throw new Error(`manifest fetch failed: ${resp.status}`);
    return resp.json();
  }

  /**
   * Fetch and cache a concept's full data.
   * Returns cached copy if already fetched.
   */
  async function fetchConcept(conceptId) {
    if (conceptCache[conceptId]) return conceptCache[conceptId];
    const resp = await fetch(`/api/concepts/${conceptId}`);
    if (!resp.ok) throw new Error(`concept ${conceptId} fetch failed: ${resp.status}`);
    const data = await resp.json();
    conceptCache[conceptId] = data;
    return data;
  }

  // ---------------------------------------------------------------------------
  // Concept add / remove
  // ---------------------------------------------------------------------------

  /**
   * Add a concept to the comparison set.
   * Fetches concept data lazily before adding.
   * No-op if already in set or at max 4.
   */
  async function addConcept(conceptId) {
    if (comparisonSet.length >= 4) return;
    if (comparisonSet.includes(conceptId)) return;

    try {
      await fetchConcept(conceptId);
    } catch (err) {
      console.error("[compare] Failed to fetch concept:", conceptId, err);
      return;
    }

    comparisonSet.push(conceptId);
    postState();
    closePicker();
    renderAll();
  }

  function removeConcept(conceptId) {
    comparisonSet = comparisonSet.filter((id) => id !== conceptId);
    postState();
    renderAll();
  }

  // ---------------------------------------------------------------------------
  // Concept picker open / close
  // ---------------------------------------------------------------------------

  function openPicker() {
    pickerOpen = true;
    renderPickerList();
    document.getElementById("concept-picker").style.display = "";
  }

  function closePicker() {
    pickerOpen = false;
    document.getElementById("concept-picker").style.display = "none";
  }

  // ---------------------------------------------------------------------------
  // Selector chips
  // ---------------------------------------------------------------------------

  function renderSelector() {
    const chipsEl = document.getElementById("selected-chips");
    chipsEl.innerHTML = "";

    for (const conceptId of comparisonSet) {
      const concept = conceptCache[conceptId];
      if (!concept) continue;

      const chip = el("div", "comparison-chip");

      const nameSpan = document.createElement("span");
      nameSpan.textContent = concept.name;

      const removeBtn = el("button", "comparison-chip__remove");
      removeBtn.setAttribute("aria-label", `Remove ${concept.name} from comparison`);
      removeBtn.textContent = "×";
      removeBtn.addEventListener("click", () => removeConcept(conceptId));

      append(chip, nameSpan, removeBtn);
      chipsEl.appendChild(chip);
    }

    // Show add button when fewer than 4 concepts selected
    if (comparisonSet.length < 4) {
      const addBtn = el("button", "comparison-add-btn");
      addBtn.textContent = "+ Add concept";
      addBtn.addEventListener("click", () => {
        if (pickerOpen) {
          closePicker();
        } else {
          openPicker();
        }
      });
      chipsEl.appendChild(addBtn);
    }
  }

  // ---------------------------------------------------------------------------
  // Concept picker list
  // ---------------------------------------------------------------------------

  function renderPickerList() {
    const listEl = document.getElementById("picker-list");
    listEl.innerHTML = "";

    const available = manifest.concepts.filter(
      (entry) => !comparisonSet.includes(entry.concept_id)
    );

    if (available.length === 0) {
      listEl.appendChild(
        el("p", "text-muted text-sm", "All concepts are already selected.")
      );
      return;
    }

    for (const entry of available) {
      const item = document.createElement("div");
      item.style.cssText =
        "display: flex; align-items: center; gap: var(--space-2);" +
        " padding: var(--space-2) var(--space-3); border-radius: var(--radius-sm);" +
        " cursor: pointer; transition: background-color 0.12s;";
      item.setAttribute("role", "option");
      item.setAttribute("aria-label", `Add ${entry.name}`);

      item.addEventListener("mouseenter", () => {
        item.style.backgroundColor = "var(--color-surface-2)";
      });
      item.addEventListener("mouseleave", () => {
        item.style.backgroundColor = "";
      });

      const nameSpan = document.createElement("span");
      nameSpan.style.flex = "1";
      nameSpan.style.fontSize = "var(--font-size-sm)";
      nameSpan.style.color = "var(--color-text-primary)";
      nameSpan.textContent = entry.name;

      const familyInfo = FAMILY_META[entry.confinement_family] ?? {
        label: entry.confinement_family,
        cls: "badge badge-nonstandard",
      };
      const familyBadge = el("span", familyInfo.cls, familyInfo.label);

      append(item, nameSpan, familyBadge);

      if (entry.company) {
        const company = el("span", "text-muted text-xs", entry.company);
        item.appendChild(company);
      }

      item.addEventListener("click", () => addConcept(entry.concept_id));
      listEl.appendChild(item);
    }
  }

  // ---------------------------------------------------------------------------
  // Tab switching
  // ---------------------------------------------------------------------------

  function switchTab(tabName) {
    activeTab = tabName;
    document.querySelectorAll(".tab-btn[data-tab]").forEach((btn) => {
      const isActive = btn.dataset.tab === tabName;
      btn.classList.toggle("tab-btn--active", isActive);
      btn.setAttribute("aria-selected", String(isActive));
    });
    document.querySelectorAll(".tab-panel").forEach((panel) => {
      panel.classList.toggle("tab-panel--active", panel.id === `tab-${tabName}`);
    });
    renderActiveTab();
  }

  function renderActiveTab() {
    if (activeTab === "sensitivity") renderSensitivity();
    else if (activeTab === "cas") renderCAS();
    else if (activeTab === "headline") renderHeadline();
  }

  // ---------------------------------------------------------------------------
  // Utility: resolve a parameter display name across loaded concepts.
  // Why: parameter_metadata may be sparse — search all loaded concepts for the first hit.
  // ---------------------------------------------------------------------------

  function getDisplayName(paramName) {
    for (const conceptId of comparisonSet) {
      const concept = conceptCache[conceptId];
      if (concept && concept.parameter_metadata && concept.parameter_metadata[paramName]) {
        return concept.parameter_metadata[paramName].display_name || paramName;
      }
    }
    return paramName;
  }

  // ---------------------------------------------------------------------------
  // Sensitivity Tab
  // ---------------------------------------------------------------------------

  /**
   * Render aligned tornado charts for all concepts with sensitivity data.
   *
   * Alignment strategy:
   * 1. Build a union parameter set across all eligible concepts.
   * 2. Classify each param as shared (≥2 concepts) or unique (exactly 1 concept).
   * 3. Sort each group by max |elasticity| descending across the set.
   * 4. Call renderTornado() for each concept with filtered sensitivities and
   *    topN = orderedParams.length (union size).
   * 5. Use Plotly.relayout to force the same categoryarray and x-axis range on
   *    every chart — this is what produces visual row alignment.
   * 6. Add gap marker traces (scatter, open-diamond symbol) for shared parameters
   *    absent in a given concept.  These are visually distinct from zero-value bars.
   */
  function renderSensitivity() {
    const contentEl = document.getElementById("sensitivity-content");
    contentEl.innerHTML = "";

    const concepts = comparisonSet.map((id) => conceptCache[id]).filter(Boolean);
    if (concepts.length === 0) return;

    const eligible = concepts.filter((c) => c.has_cost_model && c.has_sensitivities);
    const ineligible = concepts.filter((c) => !c.has_cost_model || !c.has_sensitivities);

    // Warn for ineligible concepts (no sensitivity data)
    if (ineligible.length > 0) {
      const notice = el("div", "error-state");
      notice.style.marginBottom = "var(--space-4)";
      const reasons = ineligible.map((c) => {
        const why = !c.has_cost_model ? "no cost model" : "no sensitivity data";
        return `${c.name} (${why})`;
      });
      notice.textContent = `Sensitivity unavailable for: ${reasons.join("; ")}`;
      contentEl.appendChild(notice);
    }

    if (eligible.length === 0) {
      contentEl.appendChild(
        el(
          "p",
          "text-muted text-sm",
          "None of the selected concepts have sensitivity data."
        )
      );
      return;
    }

    // Build union parameter set
    const paramCounts = {};           // paramName → count of eligible concepts that have it
    const paramMaxAbsElasticity = {}; // paramName → max |elasticity| across all concepts

    for (const concept of eligible) {
      const sens = concept.cost_model.sensitivities;
      const allParams = {
        ...(sens.engineering || {}),
        ...(sens.financial || {}),
      };
      for (const [paramName, entry] of Object.entries(allParams)) {
        paramCounts[paramName] = (paramCounts[paramName] || 0) + 1;
        const absE = Math.abs(entry.elasticity);
        if (paramMaxAbsElasticity[paramName] == null || absE > paramMaxAbsElasticity[paramName]) {
          paramMaxAbsElasticity[paramName] = absE;
        }
      }
    }

    // Shared: ≥2 concepts have the parameter; unique: exactly 1 concept has it
    const sharedParams = Object.keys(paramCounts).filter((p) => paramCounts[p] >= 2);
    const uniqueParams = Object.keys(paramCounts).filter((p) => paramCounts[p] === 1);

    // Sort each group by max |elasticity| descending across the set
    sharedParams.sort((a, b) => paramMaxAbsElasticity[b] - paramMaxAbsElasticity[a]);
    uniqueParams.sort((a, b) => paramMaxAbsElasticity[b] - paramMaxAbsElasticity[a]);

    // Shared first, then unique — this is the uniform order for all tornado charts
    const orderedParams = [...sharedParams, ...uniqueParams];

    // Compute shared x-axis range: max |elasticity| across all eligible concepts
    let maxAbsE = 0;
    for (const concept of eligible) {
      const sens = concept.cost_model.sensitivities;
      for (const e of Object.values(sens.engineering || {})) {
        if (Math.abs(e.elasticity) > maxAbsE) maxAbsE = Math.abs(e.elasticity);
      }
      for (const e of Object.values(sens.financial || {})) {
        if (Math.abs(e.elasticity) > maxAbsE) maxAbsE = Math.abs(e.elasticity);
      }
    }
    const xRange = maxAbsE > 0 ? maxAbsE * 1.15 : 1.0;

    // Shared height so rows align across columns
    const chartHeight = Math.max(300, orderedParams.length * 28 + 120);

    // Section heading
    if (sharedParams.length > 0) {
      const heading = document.createElement("div");
      heading.style.cssText =
        "display: flex; align-items: baseline; gap: var(--space-3); margin-bottom: var(--space-3);";
      const h3 = el("h3", "section-title");
      h3.style.fontSize = "var(--font-size-base)";
      h3.textContent = "Shared Parameters";
      const sub = el(
        "span",
        "text-muted text-xs",
        `${sharedParams.length} params present in ≥2 concepts — sorted by max |elasticity|` +
          (uniqueParams.length > 0
            ? `; ${uniqueParams.length} concept-unique param(s) below`
            : "")
      );
      append(heading, h3, sub);
      contentEl.appendChild(heading);
    }

    // Grid: one column per eligible concept
    const gridEl = document.createElement("div");
    const cols = Math.min(eligible.length, 4);
    gridEl.style.cssText =
      `display: grid; grid-template-columns: repeat(${cols}, 1fr);` +
      " gap: var(--space-4); align-items: start;";
    contentEl.appendChild(gridEl);

    // Build display-name list for the shared categoryarray.
    // Plotly renders category axis bottom→top, so the last entry in categoryarray
    // appears at the top of the chart — we reverse the display order here.
    const displayNames = orderedParams.map((p) => getDisplayName(p));
    const plotlyCategoryArray = [...displayNames].reverse();

    for (const concept of eligible) {
      const colEl = document.createElement("div");

      // Column header: concept name + family badge
      const header = document.createElement("div");
      header.style.cssText =
        "display: flex; align-items: center; gap: var(--space-2); margin-bottom: var(--space-2);";

      const nameEl = el("span", null, concept.name);
      nameEl.style.cssText =
        "font-weight: 600; font-size: var(--font-size-sm); color: var(--color-text-primary);";

      const familyInfo = FAMILY_META[concept.confinement_family] ?? {
        label: concept.confinement_family,
        cls: "badge badge-nonstandard",
      };
      append(header, nameEl, el("span", familyInfo.cls, familyInfo.label));
      colEl.appendChild(header);

      // Mount point for the tornado chart
      const mountEl = document.createElement("div");
      mountEl.id = `tornado-compare-${concept.concept_id}`;
      colEl.appendChild(mountEl);
      gridEl.appendChild(colEl);

      // Build filtered sensitivities — include only params from the union set.
      // Why: renderTornado sorts by |elasticity|; without filtering it would show
      // params in a different order than the shared union, breaking alignment.
      const allConceptParams = {
        ...(concept.cost_model.sensitivities.engineering || {}),
        ...(concept.cost_model.sensitivities.financial || {}),
      };
      const filteredEng = {};
      const filteredFin = {};
      for (const p of orderedParams) {
        if (concept.cost_model.sensitivities.engineering?.[p]) {
          filteredEng[p] = concept.cost_model.sensitivities.engineering[p];
        } else if (concept.cost_model.sensitivities.financial?.[p]) {
          filteredFin[p] = concept.cost_model.sensitivities.financial[p];
        }
      }

      renderTornado(mountEl, {
        sensitivities: { engineering: filteredEng, financial: filteredFin },
        parameterMetadata: concept.parameter_metadata || {},
        topN: orderedParams.length,
        // No onParameterClick in comparison view — no parameter card popovers here
        onParameterClick: null,
      });

      // Force shared axis ordering and range so all columns are visually aligned.
      // This overrides whatever categoryarray renderTornado computed from sorted order.
      Plotly.relayout(mountEl, {
        "yaxis.categoryarray": plotlyCategoryArray,
        "yaxis.categoryorder": "array",
        "xaxis.range": [-xRange, xRange],
        height: chartHeight,
      });

      // Gap markers: add for shared parameters this concept is missing.
      // NEVER use a zero-value bar — gap markers are visually distinct open shapes
      // so reviewers can tell "parameter absent" from "parameter has zero elasticity".
      const missingShared = sharedParams.filter((p) => !(p in allConceptParams));
      if (missingShared.length > 0) {
        const gapDisplayNames = missingShared.map((p) => getDisplayName(p));
        Plotly.addTraces(mountEl, {
          type: "scatter",
          x: Array(missingShared.length).fill(0),
          y: gapDisplayNames,
          mode: "markers",
          name: "n/a",
          marker: {
            symbol: "diamond-open",
            color: "rgba(107, 114, 128, 0.40)",
            size: 8,
            line: { width: 2, color: "rgba(107, 114, 128, 0.45)" },
          },
          hovertemplate: "%{y}: not applicable to this concept<extra></extra>",
          showlegend: true,
          legendrank: 9999,
        });
      }
    }
  }

  // ---------------------------------------------------------------------------
  // CAS Tab
  // ---------------------------------------------------------------------------

  /**
   * Render side-by-side CAS breakdown charts with a shared x-axis scale.
   * Only concepts with a cost model are shown; concepts without cost data are noted.
   */
  function renderCAS() {
    const contentEl = document.getElementById("cas-content");
    contentEl.innerHTML = "";

    const concepts = comparisonSet.map((id) => conceptCache[id]).filter(Boolean);
    const eligible = concepts.filter((c) => c.has_cost_model && c.cost_model);
    const ineligible = concepts.filter((c) => !c.has_cost_model || !c.cost_model);

    if (ineligible.length > 0) {
      const notice = el("div", "error-state");
      notice.style.marginBottom = "var(--space-4)";
      notice.textContent =
        "No CAS data for: " + ineligible.map((c) => c.name).join(", ");
      contentEl.appendChild(notice);
    }

    if (eligible.length === 0) {
      contentEl.appendChild(
        el("p", "text-muted text-sm", "No selected concepts have cost model data.")
      );
      return;
    }

    // Shared x-axis scale: max total capital cost across all eligible concepts.
    // Why: aligned x-axes make it easy to compare absolute cost magnitudes at a glance.
    let maxTotal = 0;
    for (const concept of eligible) {
      const total = CAS_KEYS.reduce(
        (sum, key) => sum + (concept.cost_model[key]?.cost_m_usd || 0),
        0
      );
      if (total > maxTotal) maxTotal = total;
    }
    const sharedScale = maxTotal > 0 ? maxTotal : null;

    // Grid of CAS charts
    const gridEl = document.createElement("div");
    const cols = Math.min(eligible.length, 4);
    gridEl.style.cssText =
      `display: grid; grid-template-columns: repeat(${cols}, 1fr);` +
      " gap: var(--space-4); align-items: start;";
    contentEl.appendChild(gridEl);

    for (const concept of eligible) {
      const colEl = document.createElement("div");

      // Column header
      const header = document.createElement("div");
      header.style.cssText =
        "display: flex; align-items: center; gap: var(--space-2); margin-bottom: var(--space-2);";

      const nameEl = el("span", null, concept.name);
      nameEl.style.cssText =
        "font-weight: 600; font-size: var(--font-size-sm); color: var(--color-text-primary);";

      const familyInfo = FAMILY_META[concept.confinement_family] ?? {
        label: concept.confinement_family,
        cls: "badge badge-nonstandard",
      };
      append(header, nameEl, el("span", familyInfo.cls, familyInfo.label));
      colEl.appendChild(header);

      // CAS mount point
      const mountEl = document.createElement("div");
      colEl.appendChild(mountEl);
      gridEl.appendChild(colEl);

      // Build cas object from the flat cost_model properties
      const casObj = {};
      for (const key of CAS_KEYS) {
        if (concept.cost_model[key]) {
          casObj[key] = concept.cost_model[key];
        }
      }

      renderCASBreakdown(mountEl, {
        cas: casObj,
        cas22_detail: concept.cost_model.cas22_detail || {},
        sharedScale,
      });
    }
  }

  // ---------------------------------------------------------------------------
  // Headline Tab
  // ---------------------------------------------------------------------------

  /**
   * Render a comparison table: one row per metric, one column per concept.
   */
  function renderHeadline() {
    const contentEl = document.getElementById("headline-content");
    contentEl.innerHTML = "";

    const concepts = comparisonSet.map((id) => conceptCache[id]).filter(Boolean);
    if (concepts.length === 0) return;

    // Metric row definitions
    const rows = [
      {
        label: "LCOE",
        render: (c) => {
          if (!c.has_cost_model || !c.cost_model?.headline) return "—";
          const v = c.cost_model.headline.lcoe_per_mwh;
          return v != null ? `${v.toFixed(1)} $/MWh` : "—";
        },
      },
      {
        label: "Overnight Cost",
        render: (c) => {
          if (!c.has_cost_model || !c.cost_model?.headline) return "—";
          const v = c.cost_model.headline.overnight_cost_per_kw;
          return v != null ? `${v.toFixed(0)} $/kW` : "—";
        },
      },
      {
        label: "P_net",
        render: (c) => {
          if (!c.has_cost_model || !c.cost_model?.headline) return "—";
          const v = c.cost_model.headline.p_net_mw;
          return v != null ? `${v.toFixed(0)} MW` : "—";
        },
      },
      {
        label: "Q_eng",
        render: (c) => {
          if (!c.has_cost_model || !c.cost_model?.headline) return "—";
          const v = c.cost_model.headline.q_eng;
          return v != null ? v.toFixed(2) : "—";
        },
      },
      {
        label: "Capacity Factor",
        render: (c) => {
          if (!c.has_cost_model || !c.cost_model?.headline) return "—";
          const v = c.cost_model.headline.capacity_factor;
          return v != null ? `${(v * 100).toFixed(0)}%` : "—";
        },
      },
      {
        label: "Confidence",
        // Confidence lives on the manifest entry, not ConceptData
        render: (c) => {
          const entry = manifest.concepts.find((m) => m.concept_id === c.concept_id);
          if (!entry || !entry.confidence) return { text: "—" };
          const info = CONFIDENCE_BADGE[entry.confidence];
          if (!info) return { text: entry.confidence };
          return { badge: true, label: info.label, cls: info.cls };
        },
      },
    ];

    const table = document.createElement("table");
    table.className = "comparison-table";

    // Header row: "Metric" column + one column per concept
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");

    const metricTh = document.createElement("th");
    metricTh.textContent = "Metric";
    headerRow.appendChild(metricTh);

    for (const concept of concepts) {
      const th = document.createElement("th");
      th.style.fontFamily = "var(--font-sans)";
      th.style.fontWeight = "600";
      th.style.color = "var(--color-text-primary)";

      const link = document.createElement("a");
      link.href = `/concept/${concept.concept_id}`;
      link.textContent = concept.name;
      link.style.color = "inherit";
      th.appendChild(link);

      const familyInfo = FAMILY_META[concept.confinement_family];
      if (familyInfo) {
        const badge = el("span", familyInfo.cls, familyInfo.label);
        badge.style.marginLeft = "var(--space-2)";
        th.appendChild(badge);
      }

      headerRow.appendChild(th);
    }

    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Data rows
    const tbody = document.createElement("tbody");

    for (const row of rows) {
      const tr = document.createElement("tr");

      const labelTd = document.createElement("td");
      labelTd.style.fontFamily = "var(--font-sans)";
      labelTd.style.color = "var(--color-text-muted)";
      labelTd.style.fontSize = "var(--font-size-xs)";
      labelTd.style.textTransform = "uppercase";
      labelTd.style.letterSpacing = "0.07em";
      labelTd.style.whiteSpace = "nowrap";
      labelTd.textContent = row.label;
      tr.appendChild(labelTd);

      for (const concept of concepts) {
        const td = document.createElement("td");
        const val = row.render(concept);

        if (val && typeof val === "object" && val.badge) {
          td.appendChild(el("span", val.cls, val.label));
        } else if (val && typeof val === "object") {
          td.textContent = val.text || "—";
        } else {
          td.textContent = val || "—";
        }

        tr.appendChild(td);
      }

      tbody.appendChild(tr);
    }

    table.appendChild(tbody);
    contentEl.appendChild(table);
  }

  // ---------------------------------------------------------------------------
  // Full page render (selector + active tab content)
  // ---------------------------------------------------------------------------

  function renderAll() {
    renderSelector();

    const hasConcepts = comparisonSet.length > 0;
    document.getElementById("empty-state").style.display = hasConcepts ? "none" : "";
    document.getElementById("tabs-section").style.display = hasConcepts ? "" : "none";

    if (hasConcepts) {
      renderActiveTab();
    }
  }

  // ---------------------------------------------------------------------------
  // Initialisation
  // ---------------------------------------------------------------------------

  async function init() {
    const loadingEl = document.getElementById("loading-state");
    const errorEl = document.getElementById("error-state");
    const contentEl = document.getElementById("compare-content");

    loadingEl.style.display = "";
    contentEl.style.display = "none";
    errorEl.style.display = "none";

    try {
      manifest = await fetchManifest();
    } catch (err) {
      console.error("[compare] Failed to load manifest:", err);
      loadingEl.style.display = "none";
      errorEl.style.display = "";
      return;
    }

    loadingEl.style.display = "none";
    contentEl.style.display = "";

    // Wire tab buttons
    document.querySelectorAll(".tab-btn[data-tab]").forEach((btn) => {
      btn.addEventListener("click", () => switchTab(btn.dataset.tab));
    });

    // Wire close-picker button
    document.getElementById("close-picker").addEventListener("click", closePicker);

    // Close picker on click-outside
    document.addEventListener("click", (e) => {
      if (!pickerOpen) return;
      const pickerEl = document.getElementById("concept-picker");
      // If click is inside the picker or on the chips area (which holds the add button),
      // don't close — the add-button click handler manages its own open/close toggle.
      if (pickerEl.contains(e.target)) return;
      if (document.getElementById("selected-chips").contains(e.target)) return;
      closePicker();
    });

    // Initial render with empty set
    renderAll();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
