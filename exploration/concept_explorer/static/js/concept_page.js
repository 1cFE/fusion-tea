/**
 * concept_page.js — Concept profile page controller.
 *
 * Orchestrates data fetching, section rendering, and slider-driven recompute
 * for a single fusion concept.  CONCEPT_ID is injected by the server-rendered
 * template as a global constant.
 *
 * Depends on:
 *   - parameter_card.js  (showParameterCard, hideParameterCard)
 *   - tornado.js         (renderTornado)
 *   - cas_breakdown.js   (renderCASBreakdown)
 *   - explorer.css       (badge/card/section classes)
 */

"use strict";

(function () {
  // ---------------------------------------------------------------------------
  // Confinement family display metadata
  // ---------------------------------------------------------------------------

  /** @type {Record<string, {label: string, cls: string}>} */
  const FAMILY_META = {
    MFE: { label: "MFE", cls: "badge badge-mfe" },
    IFE: { label: "IFE", cls: "badge badge-ife" },
    MIF: { label: "MIF", cls: "badge badge-mif" },
    NONSTANDARD: { label: "Non-std", cls: "badge badge-nonstandard" },
  };

  const CONFIDENCE_BADGE = {
    high:   { symbol: "✓", cls: "badge badge-confidence badge-confidence--high",   label: "High confidence" },
    medium: { symbol: "~", cls: "badge badge-confidence badge-confidence--medium", label: "Medium confidence" },
    low:    { symbol: "?", cls: "badge badge-confidence badge-confidence--low",    label: "Low confidence" },
  };

  const SEVERITY_CLS = {
    high:   "badge badge-severity badge-severity--high",
    medium: "badge badge-severity badge-severity--medium",
    low:    "badge badge-severity badge-severity--low",
  };

  // ---------------------------------------------------------------------------
  // DOM helpers
  // ---------------------------------------------------------------------------

  /** Create element with optional CSS class and text. */
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
  // Hero section
  // ---------------------------------------------------------------------------

  /**
   * Render concept identity hero.
   * @param {HTMLElement} heroEl
   * @param {Object} concept  ConceptData
   */
  function renderHero(heroEl, concept) {
    heroEl.innerHTML = "";

    const left = el("div", "hero__info");

    // Illustration or placeholder
    if (concept.illustration != null) {
      const img = document.createElement("img");
      img.className = "hero__illustration";
      img.src = `/static/images/concepts/${concept.illustration}`;
      img.alt = `${concept.name} illustration`;
      img.loading = "eager";
      heroEl.appendChild(img);
    } else {
      const ph = el("div", "hero__illustration hero__illustration--placeholder");
      ph.setAttribute("aria-hidden", "true");
      heroEl.appendChild(ph);
    }

    // Name
    left.appendChild(el("h1", "hero__name", concept.name));

    // Meta row: family badge + company
    const meta = el("div", "hero__meta");
    const familyInfo = FAMILY_META[concept.confinement_family] ?? {
      label: concept.confinement_family,
      cls: "badge badge-nonstandard",
    };
    const familyBadge = el("span", familyInfo.cls, familyInfo.label);
    meta.appendChild(familyBadge);
    if (concept.company != null) {
      meta.appendChild(el("span", "hero__company", concept.company));
    }
    left.appendChild(meta);

    heroEl.appendChild(left);
  }

  // ---------------------------------------------------------------------------
  // Headline economics card
  // ---------------------------------------------------------------------------

  /**
   * Render headline economics into the headline card container.
   * Called on initial load and again after each compute response.
   *
   * @param {HTMLElement} cardEl
   * @param {Object} headline  HeadlineEconomics
   * @param {Object|null} parameterMetadata  Map of paramName → ParameterMetadata (for confidence)
   */
  function renderHeadlineCard(cardEl, headline, parameterMetadata) {
    cardEl.innerHTML = "";

    const grid = el("div", "headline-grid");

    function stat(label, value, unit) {
      const cell = el("div", "headline-stat");
      cell.appendChild(el("span", "headline-stat__value", value));
      cell.appendChild(el("span", "headline-stat__unit", unit));
      cell.appendChild(el("span", "headline-stat__label", label));
      return cell;
    }

    grid.appendChild(stat("LCOE", headline.lcoe_per_mwh.toFixed(1), "$/MWh"));
    grid.appendChild(stat("Overnight Cost", headline.overnight_cost_per_kw.toFixed(0), "$/kW"));
    grid.appendChild(stat("Net Power", headline.p_net_mw.toFixed(0), "MW"));
    grid.appendChild(stat("Q_eng", headline.q_eng.toFixed(2), ""));
    grid.appendChild(stat("Capacity Factor", (headline.capacity_factor * 100).toFixed(1), "%"));

    cardEl.appendChild(grid);
  }

  // ---------------------------------------------------------------------------
  // Narrative sections
  // ---------------------------------------------------------------------------

  /**
   * Render narrative sections (key bets, eliminated costs, novel costs).
   * Only called when narrative is non-null.
   *
   * @param {HTMLElement} sectionEl
   * @param {HTMLElement} contentEl
   * @param {Object} narrative  NarrativeData
   */
  function renderNarrative(sectionEl, contentEl, narrative) {
    contentEl.innerHTML = "";

    function renderList(heading, items) {
      if (!items || items.length === 0) return;
      const block = el("div", "narrative-block");
      block.appendChild(el("h3", "narrative-block__heading", heading));
      const ul = el("ul", "narrative-list");
      for (const item of items) {
        ul.appendChild(el("li", "narrative-list__item", item));
      }
      block.appendChild(ul);
      contentEl.appendChild(block);
    }

    renderList("Key Bets", narrative.key_bets);
    renderList("Eliminated Costs", narrative.eliminated_costs);
    renderList("Novel Costs", narrative.novel_costs);

    sectionEl.style.display = "";
  }

  // ---------------------------------------------------------------------------
  // Risks table
  // ---------------------------------------------------------------------------

  /**
   * Render risks table rows.
   * Only called when narrative is non-null and has risks.
   *
   * @param {HTMLElement} sectionEl
   * @param {HTMLElement} tbodyEl
   * @param {Array<Object>} risks  list of {description, severity, retirement_path?}
   */
  function renderRisks(sectionEl, tbodyEl, risks) {
    tbodyEl.innerHTML = "";

    for (const risk of risks) {
      const row = document.createElement("tr");
      row.className = "risks-table__row";

      // Severity badge
      const sevTd = document.createElement("td");
      sevTd.className = "risks-table__cell risks-table__cell--severity";
      const sev = (risk.severity || "").toLowerCase();
      const badge = el("span", SEVERITY_CLS[sev] || "badge badge-severity", risk.severity || "");
      sevTd.appendChild(badge);

      // Description
      const descTd = document.createElement("td");
      descTd.className = "risks-table__cell";
      descTd.textContent = risk.description || "";

      // Retirement path (optional)
      const pathTd = document.createElement("td");
      pathTd.className = "risks-table__cell risks-table__cell--muted";
      pathTd.textContent = risk.retirement_path || "—";

      append(row, sevTd, descTd, pathTd);
      tbodyEl.appendChild(row);
    }

    sectionEl.style.display = "";
  }

  // ---------------------------------------------------------------------------
  // Slider controls
  // ---------------------------------------------------------------------------

  /**
   * Render parameter sliders for costingfe-backed concepts with sensitivity data.
   * Only called when concept has model_setup (costingfe) and has_sensitivities.
   *
   * @param {HTMLElement} slidersSectionEl  The wrapping section (shown/hidden)
   * @param {HTMLElement} containerEl       Where slider rows go
   * @param {Object} parameterMetadata      Map of paramName → ParameterMetadata
   * @param {Object} sensitivities          SensitivityAnalysis (engineering + financial)
   * @param {Function} onSliderChange       Called with updated overrides dict on debounced change
   */
  function renderSliders(slidersSectionEl, containerEl, parameterMetadata, sensitivities, onSliderChange) {
    containerEl.innerHTML = "";

    // Only render sliders for params that have metadata + range
    const allKeys = [
      ...Object.keys(sensitivities.engineering || {}),
      ...Object.keys(sensitivities.financial || {}),
    ];
    const sliderKeys = allKeys.filter((k) => parameterMetadata[k]?.range);

    if (sliderKeys.length === 0) return;

    // Current override values (keyed by paramName); starts at baseline
    const currentOverrides = {};
    for (const key of sliderKeys) {
      currentOverrides[key] = parameterMetadata[key].baseline;
    }

    let debounceTimer = null;

    for (const key of sliderKeys) {
      const meta = parameterMetadata[key];
      const [lo, hi] = meta.range;
      const baseline = meta.baseline;

      const row = el("div", "slider-row");

      // Label: display name + current value in display units
      const labelEl = el("label", "slider-row__label");
      labelEl.htmlFor = `slider-${key}`;
      const nameSpan = el("span", "slider-row__name", meta.display_name);
      const valueSpan = el("span", "slider-row__value");

      function updateValueLabel(val) {
        const display = val * (meta.display_multiplier || 1);
        valueSpan.textContent = `${display.toFixed(3)} ${meta.display_unit || ""}`.trim();
      }
      updateValueLabel(baseline);

      append(labelEl, nameSpan, valueSpan);

      // Range input
      const input = document.createElement("input");
      input.type = "range";
      input.id = `slider-${key}`;
      input.className = "slider-row__input";
      input.min = String(lo);
      input.max = String(hi);
      input.step = String((hi - lo) / 200);  // 200 steps across range
      input.value = String(baseline);
      input.setAttribute("aria-label", meta.display_name);

      // Capture key for closure
      const paramKey = key;
      input.addEventListener("input", (e) => {
        const newVal = parseFloat(e.target.value);
        currentOverrides[paramKey] = newVal;
        updateValueLabel(newVal);

        // Debounce: wait 200ms after last drag event
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
          onSliderChange({ ...currentOverrides });
        }, 200);
      });

      append(row, labelEl, input);
      containerEl.appendChild(row);
    }

    slidersSectionEl.style.display = "";
  }

  // ---------------------------------------------------------------------------
  // State reporting
  // ---------------------------------------------------------------------------

  /**
   * POST current explorer state to /api/state.
   * Fire-and-forget: errors are logged but not surfaced to the user.
   */
  function postState(conceptId, sliderOverrides, comparisonSet) {
    fetch("/api/state", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        current_concept_id: conceptId,
        slider_overrides: sliderOverrides,
        comparison_set: comparisonSet,
      }),
    }).catch((err) => {
      console.warn("[concept_page] POST /api/state failed:", err);
    });
  }

  // ---------------------------------------------------------------------------
  // Main init
  // ---------------------------------------------------------------------------

  async function init() {
    // CONCEPT_ID is injected by the server into the page template
    const conceptId = typeof CONCEPT_ID !== "undefined" ? CONCEPT_ID : null;
    if (!conceptId) {
      console.error("[concept_page] CONCEPT_ID not defined");
      return;
    }

    const loadingEl  = document.getElementById("loading-state");
    const errorEl    = document.getElementById("error-state");
    const contentEl  = document.getElementById("concept-content");

    // Guarantee loading state visible
    loadingEl.style.display = "";
    contentEl.style.display = "none";
    errorEl.style.display = "none";

    // Parallel fetch: concept data + manifest + parameter index
    let concept, _manifest, parameterIndex;
    try {
      const [conceptResp, manifestResp, paramIndexResp] = await Promise.all([
        fetch(`/api/concepts/${conceptId}`),
        fetch("/api/manifest"),
        fetch("/api/parameter_index"),
      ]);

      if (!conceptResp.ok) throw new Error(`Concept fetch returned ${conceptResp.status}`);
      if (!manifestResp.ok) throw new Error(`Manifest fetch returned ${manifestResp.status}`);
      // Parameter index is best-effort — whiskers degrade gracefully if absent
      if (paramIndexResp.ok) {
        parameterIndex = await paramIndexResp.json();
      } else {
        console.warn("[concept_page] /api/parameter_index returned", paramIndexResp.status, "— whiskers disabled");
        parameterIndex = null;
      }

      concept   = await conceptResp.json();
      _manifest = await manifestResp.json();
    } catch (err) {
      console.error("[concept_page] fetch failed:", err);
      loadingEl.style.display = "none";
      errorEl.style.display = "";
      return;
    }

    // Update breadcrumb with actual name
    const breadcrumbNameEl = document.getElementById("breadcrumb-name");
    if (breadcrumbNameEl) breadcrumbNameEl.textContent = concept.name;
    document.title = `${concept.name} — Fusion TEA`;

    // ---- Hero ----
    renderHero(document.getElementById("hero"), concept);

    // ---- Headline card ----
    const headlineCardEl = document.getElementById("headline-card");
    if (concept.cost_model) {
      renderHeadlineCard(headlineCardEl, concept.cost_model.headline, concept.parameter_metadata);
    }

    // ---- Narrative ----
    if (concept.narrative != null) {
      renderNarrative(
        document.getElementById("narrative-section"),
        document.getElementById("narrative-content"),
        concept.narrative
      );

      const risks = concept.narrative.risks || [];
      if (risks.length > 0) {
        renderRisks(
          document.getElementById("risks-section"),
          document.getElementById("risks-tbody"),
          risks
        );
      }
    }

    // ---- Tornado + CAS (only when cost model present) ----
    const sensitivitySectionEl = document.getElementById("sensitivity-section");
    const casSectionEl         = document.getElementById("cas-section");
    const tornadoMount         = document.getElementById("tornado-mount");
    const casMount             = document.getElementById("cas-mount");

    if (concept.cost_model != null) {
      // Sensitivity section: always shown when cost model present;
      // renderTornado handles the null-sensitivities standalone placeholder.
      sensitivitySectionEl.style.display = "";
      renderTornado(tornadoMount, {
        sensitivities: concept.cost_model.sensitivities,
        parameterMetadata: concept.parameter_metadata || {},
        // ParameterIndex provides per-parameter cross-concept elasticities for whiskers.
        // tornado.js checks populationContext.parameters — ParameterIndex matches this shape.
        populationContext: parameterIndex,
        topN: 15,
        onParameterClick: async (paramName, meta) => {
          let crossConceptData = null;
          try {
            const resp = await fetch(`/api/parameters/${encodeURIComponent(paramName)}`);
            if (resp.ok) crossConceptData = await resp.json();
          } catch (e) {
            console.warn("[concept_page] parameter fetch failed:", e);
          }
          // showParameterCard is defined in parameter_card.js
          // Use the tornado bar element as anchor — fall back to tornadoMount
          showParameterCard(tornadoMount, {
            paramName,
            sensitivity: concept.cost_model.sensitivities
              ? (concept.cost_model.sensitivities.engineering[paramName]
                 || concept.cost_model.sensitivities.financial[paramName]
                 || null)
              : null,
            metadata: meta,
            crossConceptData,
          });
        },
      });

      // CAS breakdown
      casSectionEl.style.display = "";
      renderCASBreakdown(casMount, {
        cas: _casToPlain(concept.cost_model),
        cas22_detail: concept.cost_model.cas22_detail || {},
      });
    }

    // ---- Slider controls (costingfe + has_sensitivities only) ----
    const isCostingfe = concept.sources && concept.sources.model_setup != null;
    if (isCostingfe && concept.has_sensitivities && concept.cost_model?.sensitivities) {
      const slidersSectionEl = document.getElementById("sliders-section");
      const slidersContainerEl = document.getElementById("sliders-container");
      const headlineLoadingEl  = document.getElementById("headline-loading");
      const computeErrorEl     = document.getElementById("compute-error");

      renderSliders(
        slidersSectionEl,
        slidersContainerEl,
        concept.parameter_metadata || {},
        concept.cost_model.sensitivities,
        async (overrides) => {
          // Hide old error; show loading on headline card
          computeErrorEl.style.display = "none";
          headlineLoadingEl.style.display = "";

          try {
            const resp = await fetch("/api/compute", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ concept_id: conceptId, overrides }),
            });

            if (!resp.ok) {
              const detail = await resp.json().catch(() => ({ detail: `HTTP ${resp.status}` }));
              throw new Error(detail.detail || `HTTP ${resp.status}`);
            }

            const newCostModel = await resp.json();

            // Update headline card only (tornado bars stay at baseline)
            renderHeadlineCard(headlineCardEl, newCostModel.headline, concept.parameter_metadata);

            // Re-render CAS breakdown with updated values
            renderCASBreakdown(casMount, {
              cas: _casToPlain(newCostModel),
              cas22_detail: newCostModel.cas22_detail || {},
            });

            // Report updated slider state
            postState(conceptId, overrides, []);
          } catch (err) {
            console.error("[concept_page] compute failed:", err);
            computeErrorEl.textContent = `Compute error: ${err.message}`;
            computeErrorEl.style.display = "";
          } finally {
            headlineLoadingEl.style.display = "none";
          }
        }
      );
    }

    // ---- Report initial state ----
    postState(conceptId, {}, []);

    // ---- Atomically reveal content ----
    loadingEl.style.display = "none";
    contentEl.style.display = "";
  }

  // ---------------------------------------------------------------------------
  // Helper: flatten CostModelData top-level CAS fields into plain {key: CASAccount} dict
  // ---------------------------------------------------------------------------

  /**
   * The CAS stacked bar chart expects an object of the form
   * { cas10: {name, cost_m_usd, overridden}, cas21: ..., ... }.
   * CostModelData (from the API) has each CAS account as a direct field, so
   * we just extract those 17 keys into one dict.
   *
   * @param {Object} costModel  CostModelData from API
   * @returns {Object}
   */
  function _casToPlain(costModel) {
    const CAS_KEYS = [
      "cas10", "cas21", "cas22", "cas23", "cas24", "cas25",
      "cas26", "cas27", "cas28", "cas29", "cas30",
      "cas40", "cas50", "cas60", "cas70", "cas80", "cas90",
    ];
    const out = {};
    for (const k of CAS_KEYS) {
      if (costModel[k] != null) out[k] = costModel[k];
    }
    return out;
  }

  // ---------------------------------------------------------------------------
  // Boot
  // ---------------------------------------------------------------------------

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
