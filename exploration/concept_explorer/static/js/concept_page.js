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
  // Collapsible section helper
  // ---------------------------------------------------------------------------

  /**
   * Wire one section header to toggle its body open/closed and set initial state.
   * The section's `.is-collapsed` class drives both chevron rotation and body
   * display (see `.section.is-collapsed` rules in explorer.css).
   *
   * Idempotent — calling twice on the same section just re-applies the open state
   * and re-binds the click handler (cleared via cloneNode on the header).
   *
   * @param {HTMLElement} sectionEl  the <section class="section"> wrapper
   * @param {boolean} defaultOpen
   */
  function makeCollapsible(sectionEl, defaultOpen) {
    if (!sectionEl) return;
    sectionEl.classList.toggle("is-collapsed", !defaultOpen);
    const header = sectionEl.querySelector(".section__header");
    if (!header) return;
    // Clone-replace to drop any prior listener on this header
    const fresh = header.cloneNode(true);
    header.parentNode.replaceChild(fresh, header);
    fresh.addEventListener("click", () => {
      sectionEl.classList.toggle("is-collapsed");
    });
  }

  /**
   * Set the right-aligned hint text on a section header.
   * Pass an object `{ text, changed }` to render a "X CHANGED" pill when
   * `changed` is true (used by the Sensitivity header on slider drag).
   */
  function setSectionHint(sectionEl, hintConfig) {
    if (!sectionEl) return;
    const hintEl = sectionEl.querySelector(".section__hint");
    if (!hintEl) return;
    const text = typeof hintConfig === "string" ? hintConfig : (hintConfig?.text ?? "");
    const changed = typeof hintConfig === "object" && hintConfig?.changed === true;
    hintEl.textContent = text;
    hintEl.classList.toggle("section__hint--changed", changed);
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

    const heroLabel = conceptLabel(concept);
    const left = el("div", "hero__info");

    // Illustration or placeholder
    if (concept.illustration != null) {
      const img = document.createElement("img");
      img.className = "hero__illustration";
      img.src = `/static/images/concepts/${concept.illustration}`;
      img.alt = `${heroLabel.name} illustration`;
      img.loading = "eager";
      heroEl.appendChild(img);
    } else {
      const ph = el("div", "hero__illustration hero__illustration--placeholder");
      ph.setAttribute("aria-hidden", "true");
      heroEl.appendChild(ph);
    }

    // Name — visible #code handle + canonical Name (Fuel), via conceptLabel,
    // + the one honest-caveat marker. The concept page is the richest surface,
    // so it also flags an *unrecorded* archetype fit ("not recorded") rather
    // than letting an absent grade vanish (FR-A3.3).
    const nameEl = el("h1", "hero__name");
    nameEl.appendChild(heroLabel.codeChip());
    nameEl.appendChild(document.createTextNode(" " + heroLabel.name));
    const heroCaveat = caveatMarker({
      asterisk: concept.asterisk_in_comparison,
      fitGrade: concept.fit_grade,
      missing: concept.fit_grade == null ? "Archetype fit" : null,
    }).element();
    if (heroCaveat) nameEl.appendChild(heroCaveat);
    left.appendChild(nameEl);

    // Meta row: family badge + company
    const meta = el("div", "hero__meta");
    const familyInfo = FAMILY_META[concept.confinement_family] ?? {
      label: concept.confinement_family,
      cls: "badge badge-nonstandard",
    };
    const familyBadge = el("span", familyInfo.cls, familyInfo.label);
    meta.appendChild(familyBadge);
    // Company intentionally hidden on the profile page (anonymized explorer,
    // 2026-06-08): the "Example: <Company>" disclaimer appears only on the
    // entry surfaces (matrix + pipeline cards). Profile / compare / cost-
    // landscape views render the technical descriptor only.
    left.appendChild(meta);

    heroEl.appendChild(left);
  }

  // ---------------------------------------------------------------------------
  // Analyst-override toggle (Phase 3)
  // ---------------------------------------------------------------------------

  /**
   * Mount the "Apply analyst cost adjustments" toggle into the hero block.
   * Idempotent — replaces any prior toggle. The "(N entries)" count is inert
   * low-emphasis text (Item 2 makes it a clickable inspection trigger). When
   * `disabled` (empty registry), the checkbox is non-interactive with hover
   * text. Freeform concepts never call this (INV-5).
   *
   * @param {HTMLElement} heroEl
   * @param {Object} opts
   * @param {number} opts.count       enabled override count (drives the toggle)
   * @param {number} [opts.recordCount] total registry entries (enabled + not).
   *   When 0 enabled but >0 total (a disabled-only concept), the chip reads
   *   "(N not applied)" instead of a contradictory "(0 entries)". See m2.
   * @param {boolean} opts.checked    initial state (default-on)
   * @param {boolean} opts.disabled   true when count === 0
   * @param {Function} opts.onChange  (checked: boolean) => void
   * @param {Function} [opts.onCountClick] when set, the count chip becomes a
   *   clickable trigger that opens the override inspection panel with the whole
   *   registry (Item 2). Omitted when the concept has no records.
   */
  function mountOverrideToggle(heroEl, { count, recordCount, checked, disabled, onChange, onCountClick }) {
    const prior = heroEl.querySelector(".override-toggle");
    if (prior) prior.remove();

    const wrap = el("div", "override-toggle");
    if (disabled) wrap.classList.add("override-toggle--disabled");

    const label = el("label", "override-toggle__label");
    if (disabled) {
      label.title =
        "No analyst cost adjustments for this concept — nothing to apply or remove.";
    }

    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.className = "override-toggle__checkbox";
    cb.checked = checked && !disabled;
    cb.disabled = disabled;
    cb.addEventListener("change", () => {
      if (typeof onChange === "function") onChange(cb.checked);
    });
    label.appendChild(cb);

    label.appendChild(el("span", "override-toggle__text", "Apply analyst cost adjustments"));
    // Label reflects what the toggle applies (enabled count). For a disabled-only
    // concept (0 enabled, but ≥1 not-applied entry to read) the "(0 entries)"
    // text would contradict the still-clickable chip, so show "(N not applied)".
    const total = recordCount != null ? recordCount : count;
    let entries;
    if (count > 0) {
      entries = count === 1 ? "1 entry" : `${count} entries`;
    } else if (total > 0) {
      entries = `${total} not applied`;
    } else {
      entries = "0 entries";
    }
    const countEl = el("span", "override-toggle__count", `(${entries})`);
    if (typeof onCountClick === "function") {
      countEl.classList.add("override-toggle__count--clickable");
      countEl.setAttribute("role", "button");
      countEl.setAttribute("tabindex", "0");
      countEl.title = "Inspect the analyst's cost adjustments";
      // The count sits inside the <label>; stop the click/keydown from toggling
      // the checkbox — it opens the inspection panel instead.
      countEl.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        onCountClick();
      });
      countEl.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          e.stopPropagation();
          onCountClick();
        }
      });
    }
    label.appendChild(countEl);
    wrap.appendChild(label);

    wrap.appendChild(
      el(
        "p",
        "override-toggle__subtitle",
        "On: the analyst's accountable cost story. " +
          "Off: the costing library's bare answer for this architecture.",
      ),
    );

    heroEl.appendChild(wrap);
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

    // Update breadcrumb + title via the one naming helper (#NN Name (Fuel))
    const lbl = conceptLabel(concept);
    const breadcrumbNameEl = document.getElementById("breadcrumb-name");
    if (breadcrumbNameEl) breadcrumbNameEl.textContent = lbl.text;
    document.title = `${lbl.text} — Fusion TEA`;

    // ---- Hero ----
    const heroEl = document.getElementById("hero");
    renderHero(heroEl, concept);

    // Override inspection panel (Item 2). One handler shared by every ★ trigger
    // (CAS rows + treemap tiles, across the initial render and all recompute
    // paths) and by the hero "(N entries)" chip. Reads the records already on the
    // concept payload — never fetches.
    const overrideRecords = concept.overrides || [];
    function openOverridePanel(focusAccount) {
      showOverridePanel({
        records: overrideRecords,
        focusAccount,
        conceptName: lbl.name,
      });
    }

    // Refresh the CAS section header hint ("Total Capital: N M$") from a cost
    // model. Called at init and from every recompute path (slider, mode toggle,
    // reset) so the header summary tracks the live breakdown total instead of
    // the load-time value (Item 1-FU1). One shared helper keeps the slider and
    // toggle paths consistent — half-fixing only one would make them disagree
    // about whether the hint tracks live state.
    function _refreshCASHint(costModel) {
      if (!costModel) return;
      setSectionHint(
        document.getElementById("cas-section"),
        `Total Capital: ${_fmtMoneyM(_sumCASCapital(costModel))}`,
      );
    }

    // ---- Sticky headline ----
    // The "mode baseline" is the current LCOE function's headline with sliders at
    // baseline: the extraction-time analyst-applied headline on load, and the
    // toggle's compute response after an analyst-overrides mode switch (Phase 3,
    // INV-2). Slider deltas and Reset are measured against it, so toggling the
    // mode never leaves a phantom delta on the headline.
    const stickyEl = document.getElementById("sticky-headline");
    let modeBaselineHeadline = concept.cost_model?.headline ?? null;
    let modeBaselineCostModel = concept.cost_model ?? null;
    // Toggle state (Phase 3, FR-SO5). Default on → analyst-applied LCOE drives
    // headline + sliders + tornado; this is what makes the loaded headline match
    // the stored value (FR-SO1). Rides every /api/compute call.
    let applyOverrides = true;
    let tornadoHandle = null; // captured below when renderTornado runs (used by Reset)
    // `sources.model_setup` was removed from the served payload in efa8e88
    // (paths are derived from concept_id server-side now). Gate on model_type
    // instead — "costingfe" identifies the same concepts that previously had
    // a model_setup source path.
    const isCostingfeForSticky = concept.model_type === "costingfe";
    const hasSlidersForSticky =
      isCostingfeForSticky
      && concept.has_sensitivities
      && concept.cost_model?.sensitivities != null;
    renderStickyHeadline(stickyEl, {
      concept,
      headline: modeBaselineHeadline,
      hasSliders: hasSlidersForSticky,
      // Reset puts the UI back into the page-load state (sliders at baseline,
      // sticky bar showing the extraction-time headline with no delta, CAS
      // breakdown showing the original cost model). It does NOT call /api/compute
      // — going through compute would surface the unscaled-result mismatch and
      // briefly flash a phantom delta.
      onReset: () => {
        if (tornadoHandle && typeof tornadoHandle.reset === "function") {
          tornadoHandle.reset();
        }
        updateStickyHeadline(stickyEl, modeBaselineHeadline, modeBaselineHeadline);
        setResetEnabled(stickyEl, false);
        // Revert the CAS breakdown to the current mode's baseline cost model
        // (extraction-time applied model, or the bare model after a toggle).
        const casMountForReset = document.getElementById("cas-mount");
        if (casMountForReset && modeBaselineCostModel) {
          renderCASBreakdown(casMountForReset, {
            cas: _casToPlain(modeBaselineCostModel),
            cas22_detail: modeBaselineCostModel.cas22_detail || {},
            onOverrideClick: openOverridePanel,
          });
          _refreshCASHint(modeBaselineCostModel);
        }
        // Clear the "N CHANGED" pill on the Sensitivity header.
        setSectionHint(
          document.getElementById("sensitivity-section"),
          { text: "Drag any slider — top numbers will update", changed: false },
        );
        postState(conceptId, {}, []);
      },
    });
    stickyEl.style.display = "";

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

      const headlineLoadingEl = document.getElementById("headline-loading");
      const computeErrorEl    = document.getElementById("compute-error");

      // Track baseline-vs-current state so the Reset button enables only when
      // at least one slider has been moved. Compares overrides to baselines
      // by parameter name.
      function _countChanged(overrides) {
        if (!overrides) return 0;
        let n = 0;
        for (const [k, v] of Object.entries(overrides)) {
          const base = concept.parameter_metadata?.[k]?.baseline;
          if (Number.isFinite(base) && Math.abs(v - base) > 1e-9) n++;
        }
        return n;
      }
      const _hasNonBaseline = (o) => _countChanged(o) > 0;

      // Refresh the Sensitivity section header hint based on override count.
      const sensitivitySectionElForHint = document.getElementById("sensitivity-section");
      function _updateSensitivityHint(overrides) {
        const n = _countChanged(overrides);
        if (n === 0) {
          setSectionHint(sensitivitySectionElForHint,
            { text: "Drag any slider — top numbers will update", changed: false });
        } else {
          setSectionHint(sensitivitySectionElForHint,
            { text: `${n} CHANGED`, changed: true });
        }
      }

      // Which precomputed sensitivity set the tornado describes — applied
      // (default) vs library-bare — selected by the toggle (INV-2). Falls back
      // to applied when no bare set was emitted (e.g. empty registry → equal).
      function _selectedSensitivities() {
        if (!concept.cost_model) return null;
        if (applyOverrides) return concept.cost_model.sensitivities ?? null;
        return (
          concept.cost_model.sensitivities_bare
          ?? concept.cost_model.sensitivities
          ?? null
        );
      }

      // Compute callback: tornado.js fires this debounced with the current
      // overrides map after a slider drag (and once per Reset, with all values
      // back at baseline). Updates the sticky headline + CAS breakdown. The
      // recompute uses whichever LCOE function the toggle selects, measured
      // against the current mode's baseline.
      async function onSliderChange(overrides) {
        if (computeErrorEl) computeErrorEl.style.display = "none";
        if (headlineLoadingEl) headlineLoadingEl.style.display = "";
        // Reset button reflects "any slider moved" state.
        setResetEnabled(stickyEl, _hasNonBaseline(overrides));
        // Sensitivity header gets a "N CHANGED" pill when overrides exist.
        _updateSensitivityHint(overrides);
        try {
          const resp = await fetch("/api/compute", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              concept_id: conceptId,
              overrides,
              apply_analyst_overrides: applyOverrides,
            }),
          });
          if (!resp.ok) {
            const detail = await resp.json().catch(() => ({ detail: `HTTP ${resp.status}` }));
            throw new Error(detail.detail || `HTTP ${resp.status}`);
          }
          const newCostModel = await resp.json();
          updateStickyHeadline(stickyEl, newCostModel.headline, modeBaselineHeadline);
          renderCASBreakdown(casMount, {
            cas: _casToPlain(newCostModel),
            cas22_detail: newCostModel.cas22_detail || {},
            onOverrideClick: openOverridePanel,
          });
          _refreshCASHint(newCostModel);
          postState(conceptId, overrides, []);
        } catch (err) {
          console.error("[concept_page] compute failed:", err);
          if (computeErrorEl) {
            computeErrorEl.textContent = `Compute error: ${err.message}`;
            computeErrorEl.style.display = "";
          }
        } finally {
          if (headlineLoadingEl) headlineLoadingEl.style.display = "none";
        }
      }

      // (Re)render the tornado from the toggle-selected sensitivity set. Re-call
      // rebuilds it from scratch with sliders at baseline — exactly the
      // mode-switch semantics (Decision A). Reassigns the Reset-button handle.
      function renderTornadoForMode() {
        tornadoHandle = renderTornado(tornadoMount, {
          sensitivities: _selectedSensitivities(),
          parameterMetadata: concept.parameter_metadata || {},
          // ParameterIndex provides per-parameter cross-concept elasticities for whiskers.
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
            const sel = _selectedSensitivities();
            // showParameterCard is defined in parameter_card.js
            showParameterCard(tornadoMount, {
              paramName,
              sensitivity: sel
                ? (sel.engineering[paramName] || sel.financial[paramName] || null)
                : null,
              metadata: meta,
              crossConceptData,
            });
          },
          onSliderChange: hasSlidersForSticky ? onSliderChange : null,
        });
      }
      renderTornadoForMode();

      // CAS breakdown
      casSectionEl.style.display = "";
      renderCASBreakdown(casMount, {
        cas: _casToPlain(concept.cost_model),
        cas22_detail: concept.cost_model.cas22_detail || {},
        onOverrideClick: openOverridePanel,
      });

      // Mode switch: one compute call (new headline + CAS) plus a client-side
      // tornado re-render, applied together in this single handler so no surface
      // is briefly out of sync (INV-2). Sliders return to baseline (Decision A).
      async function onModeSwitch() {
        if (computeErrorEl) computeErrorEl.style.display = "none";
        if (headlineLoadingEl) headlineLoadingEl.style.display = "";
        try {
          const resp = await fetch("/api/compute", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              concept_id: conceptId,
              overrides: {},
              apply_analyst_overrides: applyOverrides,
            }),
          });
          if (!resp.ok) {
            const detail = await resp.json().catch(() => ({ detail: `HTTP ${resp.status}` }));
            throw new Error(detail.detail || `HTTP ${resp.status}`);
          }
          const newCostModel = await resp.json();
          // New mode baseline; all three surfaces follow it atomically.
          modeBaselineHeadline = newCostModel.headline;
          modeBaselineCostModel = newCostModel;
          updateStickyHeadline(stickyEl, newCostModel.headline, modeBaselineHeadline);
          renderCASBreakdown(casMount, {
            cas: _casToPlain(newCostModel),
            cas22_detail: newCostModel.cas22_detail || {},
            onOverrideClick: openOverridePanel,
          });
          _refreshCASHint(newCostModel);
          renderTornadoForMode();
          setResetEnabled(stickyEl, false);
          _updateSensitivityHint({});
          postState(conceptId, {}, []);
        } catch (err) {
          console.error("[concept_page] mode switch failed:", err);
          if (computeErrorEl) {
            computeErrorEl.textContent = `Compute error: ${err.message}`;
            computeErrorEl.style.display = "";
          }
        } finally {
          if (headlineLoadingEl) headlineLoadingEl.style.display = "none";
        }
      }

      // Override toggle (FR-SO6 / INV-5): only for costingfe-backed concepts
      // (model_setup present). Active when the registry is non-empty; disabled
      // (with hover text) when empty. Freeform concepts (model_setup null) get
      // no toggle at all.
      if (isCostingfeForSticky) {
        mountOverrideToggle(heroEl, {
          count: concept.analyst_override_count || 0,
          recordCount: overrideRecords.length,
          checked: applyOverrides,
          disabled: (concept.analyst_override_count || 0) === 0,
          onChange: (checked) => {
            applyOverrides = checked;
            onModeSwitch();
          },
          // The chip opens the whole registry (enabled + not-applied). Present
          // whenever any record exists — including disabled-only concepts whose
          // enabled count is 0 but whose not-applied entries are worth reading.
          onCountClick: overrideRecords.length > 0 ? () => openOverridePanel() : undefined,
        });
      }
    }

    // ---- Wire collapsibles + initial hint text ----
    const sections = {
      narrative:   document.getElementById("narrative-section"),
      risks:       document.getElementById("risks-section"),
      cas:         document.getElementById("cas-section"),
      sensitivity: document.getElementById("sensitivity-section"),
    };

    if (concept.narrative) {
      makeCollapsible(sections.narrative, false);
      const bits = [];
      if (concept.narrative.key_bets?.length)         bits.push("key bets");
      if (concept.narrative.eliminated_costs?.length) bits.push("eliminated costs");
      if (concept.narrative.novel_costs?.length)      bits.push("novel costs");
      setSectionHint(sections.narrative, bits.length ? bits.join(" · ") : "");
    }

    const risks = concept.narrative?.risks || [];
    if (risks.length > 0) {
      makeCollapsible(sections.risks, false);
      const nHigh = risks.filter((r) => (r.severity || "").toLowerCase() === "high").length;
      const hint = `${risks.length} risk${risks.length === 1 ? "" : "s"}` +
                   (nHigh > 0 ? ` · ${nHigh} high` : "");
      setSectionHint(sections.risks, hint);
    }

    if (concept.cost_model) {
      makeCollapsible(sections.cas, false);
      _refreshCASHint(concept.cost_model);

      makeCollapsible(sections.sensitivity, true);
      // Sensitivity hint stays at the template default ("Drag any slider…")
      // until onSliderChange flips it to "N CHANGED".
    }

    // ---- Report initial state ----
    postState(conceptId, {}, []);

    // ---- Atomically reveal content ----
    loadingEl.style.display = "none";
    contentEl.style.display = "";

    // Agentic Research Key Findings — fire-and-forget, never blocks the page.
    // Renders below the sensitivity section: synthesis exec summary (TL;DR)
    // followed by full analysis.md, whichever are available. Concepts with
    // neither file show an honest placeholder.
    _renderFindings(conceptId);
  }

  /** Fetch and render the Agentic Research Key Findings section. */
  async function _renderFindings(conceptId) {
    const sectionEl = document.getElementById("findings-section");
    const mountEl = document.getElementById("findings-mount");
    if (!sectionEl || !mountEl) return;
    let payload;
    try {
      const resp = await fetch(`/api/concepts/${conceptId}/findings`);
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      payload = await resp.json();
    } catch (err) {
      console.warn("[concept_page] findings fetch failed:", err);
      return;
    }
    const parts = [];
    if (payload.exec_summary_html) {
      parts.push(
        '<div class="findings-tldr"><div class="findings-tldr__label">TL;DR — Executive Summary</div>'
        + payload.exec_summary_html
        + "</div>",
      );
    }
    if (payload.analysis_html) {
      var label = payload.analysis_from_archive
        ? '<div class="findings-full__label">Full Analysis '
          + '<span class="findings-full__archive-tag" title="Pre-rework archived analysis '
          + '— content may reference earlier model parameters. The active model_setup.py '
          + 'is the authoritative current state.">(archived, pre-rework)</span></div>'
        : '<div class="findings-full__label">Full Analysis</div>';
      parts.push(
        '<div class="findings-full">'
        + label
        + payload.analysis_html
        + "</div>",
      );
    }
    if (parts.length === 0) {
      parts.push(
        '<p class="findings-empty">Research synthesis not yet available for this concept. '
        + "See <code>model_setup.py</code> in the concept directory for the design-point "
        + "rationale and parameter choices.</p>",
      );
    }
    mountEl.innerHTML = parts.join("");
    sectionEl.style.display = "";
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

  /** Sum across all CAS top-level accounts; matches the "Total capital + annualized"
   *  number rendered by cas_breakdown.js (sum of every present cas* account). */
  function _sumCASCapital(costModel) {
    return Object.values(_casToPlain(costModel)).reduce(
      (s, a) => s + (Number.isFinite(a?.cost_m_usd) ? a.cost_m_usd : 0), 0,
    );
  }

  /** Format a M$ value as "16,975 M$" or "999 M$" — matches CAS widget convention. */
  function _fmtMoneyM(v) {
    if (!Number.isFinite(v)) return "—";
    return `${v.toLocaleString("en-US", { maximumFractionDigits: 0 })} M$`;
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
