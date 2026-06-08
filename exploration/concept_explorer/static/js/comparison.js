/**
 * comparison.js — Comparison page controller (v2).
 *
 * Two comparison modes:
 *   - Integrated (1–3 concepts): dual side-by-side panels with independent view selectors
 *   - Landscape  (1–6 concepts): single view selector, responsive concept grid
 *
 * URL-driven state: /compare?mode=integrated&concepts=arc,sparc&left=categorical&right=summary
 *
 * VIEW_REGISTRY: Items 3a/3b register render functions here; shell falls back to placeholders.
 *
 * Carries over: fetchManifest, fetchConcept, conceptCache, postState, FAMILY_META
 */

"use strict";

(function () {
  // ---------------------------------------------------------------------------
  // Constants
  // ---------------------------------------------------------------------------

  const MAX_INTEGRATED = 3;
  const MAX_LANDSCAPE = 6;
  const VALID_VIEWS = ["categorical", "summary", "capex", "sensitivity"];
  const DEFAULT_LEFT = "categorical";
  const DEFAULT_RIGHT = "summary";
  const DEFAULT_VIEW = "categorical";

  // ---------------------------------------------------------------------------
  // Display metadata (carried over from v1)
  // ---------------------------------------------------------------------------

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

  // ---------------------------------------------------------------------------
  // View Registry — Items 3a/3b register render functions here
  // ---------------------------------------------------------------------------

  const VIEW_REGISTRY = {
    categorical:  { label: "Categorical",  renderIntegrated: null, renderLandscape: null },
    summary:      { label: "Summary",      renderIntegrated: null, renderLandscape: null },
    capex:        { label: "CapEx",        renderIntegrated: null, renderLandscape: null },
    sensitivity:  { label: "Sensitivity",  renderIntegrated: null, renderLandscape: null },
  };

  // Expose globally so Items 3a/3b scripts can register renderers
  window.VIEW_REGISTRY = VIEW_REGISTRY;

  // ---------------------------------------------------------------------------
  // State
  // ---------------------------------------------------------------------------

  let _state = {
    concepts: [],          // Ordered concept IDs (validated against manifest)
    mode: "integrated",    // "integrated" | "landscape"
    left: DEFAULT_LEFT,    // View for integrated left panel
    right: DEFAULT_RIGHT,  // View for integrated right panel
    view: DEFAULT_VIEW,    // View for landscape mode
  };

  /** @type {Object|null} ConceptManifest fetched on init. */
  let manifest = null;

  /**
   * @type {string[]} Concept IDs in the order the cost-landscape chart displays
   * them (tree-grouped, LCOE-ascending within band). Used to order the picker
   * and to filter out concepts the cost landscape excludes (freeform /
   * non-grounded / no cost model). Populated by init() after fetching the
   * landscape + taxonomy data.
   */
  let pickerOrder = [];

  /** @type {Record<string, Object>} Lazily populated ConceptData cache. */
  let conceptCache = {};

  /** @type {boolean} Whether the inline concept picker is open. */
  let pickerOpen = false;

  // ---------------------------------------------------------------------------
  // DOM helpers
  // ---------------------------------------------------------------------------

  function el(tag, cls, text) {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  // Item 10 / Bet 2: render an amber warning glyph next to the concept name
  // when the orchestrator routed the concept as costingfe-asterisked
  // (Grounding-Confidence: low). Used wherever a concept name is rendered.
  // Returns null when no marker is needed so callers can pass the result to
  // `append()` unconditionally.
  function lowGroundingMarker(concept) {
    if (!concept) return null;
    // Delegate to the one honest-caveat device (A3): low-grounding asterisk +
    // archetype-fit None, consistent glyph/hover. Returns null when no caveat
    // applies, so callers can pass the result to append() unconditionally.
    return caveatMarker({
      asterisk: concept.asterisk_in_comparison,
      fitGrade: concept.fit_grade,
    }).element();
  }

  function append(parent, ...children) {
    for (const c of children) {
      if (c != null) parent.appendChild(c);
    }
    return parent;
  }

  // ---------------------------------------------------------------------------
  // API helpers (carried over from v1)
  // ---------------------------------------------------------------------------

  function postState() {
    fetch("/api/state", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        current_concept_id: null,
        slider_overrides: {},
        comparison_set: [..._state.concepts],
        timestamp: "",
      }),
    }).catch((err) => console.warn("[compare] POST /api/state failed:", err));
  }

  async function fetchManifest() {
    const resp = await fetch("/api/manifest");
    if (!resp.ok) throw new Error(`manifest fetch failed: ${resp.status}`);
    return resp.json();
  }

  async function fetchConcept(conceptId) {
    if (conceptCache[conceptId]) return conceptCache[conceptId];
    const resp = await fetch(`/api/concepts/${conceptId}`);
    if (!resp.ok) throw new Error(`concept ${conceptId} fetch failed: ${resp.status}`);
    const data = await resp.json();
    conceptCache[conceptId] = data;
    return data;
  }

  // ---------------------------------------------------------------------------
  // URL State Manager
  // ---------------------------------------------------------------------------

  /**
   * Parse URL query parameters into a state object with defaults applied.
   */
  function parseUrl() {
    const params = new URLSearchParams(window.location.search);

    const conceptsRaw = params.get("concepts") || "";
    const concepts = conceptsRaw.split(",").filter((s) => s.length > 0);

    const modeRaw = params.get("mode");
    let mode;
    if (modeRaw === "integrated" || modeRaw === "landscape") {
      mode = modeRaw;
    } else {
      // Auto-select based on concept count (FR-4)
      mode = concepts.length > MAX_INTEGRATED ? "landscape" : "integrated";
    }

    const leftRaw = params.get("left");
    const left = VALID_VIEWS.includes(leftRaw) ? leftRaw : DEFAULT_LEFT;

    const rightRaw = params.get("right");
    const right = VALID_VIEWS.includes(rightRaw) ? rightRaw : DEFAULT_RIGHT;

    const viewRaw = params.get("view");
    const view = VALID_VIEWS.includes(viewRaw) ? viewRaw : DEFAULT_VIEW;

    return { concepts, mode, left, right, view };
  }

  /**
   * Write current state to URL via history.replaceState.
   * Only includes non-default values to keep URLs clean.
   */
  function syncUrl() {
    const params = new URLSearchParams();

    if (_state.concepts.length > 0) {
      params.set("concepts", _state.concepts.join(","));
    }
    if (_state.concepts.length > 0) {
      params.set("mode", _state.mode);
    }

    // Only include view params if not defaults
    if (_state.mode === "integrated") {
      if (_state.left !== DEFAULT_LEFT) params.set("left", _state.left);
      if (_state.right !== DEFAULT_RIGHT) params.set("right", _state.right);
    } else {
      if (_state.view !== DEFAULT_VIEW) params.set("view", _state.view);
    }

    const qs = params.toString();
    const url = qs ? `${window.location.pathname}?${qs}` : window.location.pathname;
    history.replaceState(null, "", url);
  }

  /**
   * Validate and correct state against the manifest.
   * Returns { state, warnings } where warnings is an array of strings.
   */
  function validateAndCorrect(state) {
    const warnings = [];
    const validIds = new Set(manifest.concepts.map((c) => c.concept_id));

    // Filter concepts to those present in manifest
    const validConcepts = [];
    const invalidConcepts = [];
    for (const id of state.concepts) {
      if (validIds.has(id)) {
        validConcepts.push(id);
      } else {
        invalidConcepts.push(id);
      }
    }
    if (invalidConcepts.length > 0) {
      warnings.push(`Skipped unknown concept(s): ${invalidConcepts.join(", ")}`);
    }

    // Enforce MAX_LANDSCAPE
    if (validConcepts.length > MAX_LANDSCAPE) {
      warnings.push(`Trimmed to ${MAX_LANDSCAPE} concepts (maximum)`);
      validConcepts.length = MAX_LANDSCAPE;
    }

    state.concepts = validConcepts;

    // FR-6: auto-correct integrated with >MAX_INTEGRATED concepts
    if (state.mode === "integrated" && state.concepts.length > MAX_INTEGRATED) {
      state.mode = "landscape";
      warnings.push("Switched to Landscape mode (too many concepts for Integrated)");
    }

    return { state, warnings };
  }

  // ---------------------------------------------------------------------------
  // Concept Bar — chips + add button (FR-20)
  // ---------------------------------------------------------------------------

  function renderConceptBar() {
    const barEl = document.getElementById("concept-bar");
    barEl.innerHTML = "";

    for (const conceptId of _state.concepts) {
      const concept = conceptCache[conceptId];
      if (!concept) continue;

      const chip = el("div", "comparison-chip");

      const familyInfo = FAMILY_META[concept.confinement_family] ?? {
        label: concept.confinement_family,
        cls: "badge badge-nonstandard",
      };
      const badge = el("span", familyInfo.cls, familyInfo.label);

      const chipLbl = conceptLabel(concept);
      const nameSpan = document.createElement("span");
      nameSpan.appendChild(chipLbl.codeChip());
      nameSpan.appendChild(document.createTextNode(" " + chipLbl.name));

      const removeBtn = el("button", "comparison-chip__remove");
      removeBtn.setAttribute("aria-label", `Remove ${chipLbl.text} from comparison`);
      removeBtn.textContent = "×";
      removeBtn.addEventListener("click", () => removeConcept(conceptId));

      append(chip, badge, nameSpan, lowGroundingMarker(concept), removeBtn);
      barEl.appendChild(chip);
    }

    // Show add button when below max
    if (_state.concepts.length < MAX_LANDSCAPE) {
      const addBtn = el("button", "comparison-add-btn");
      addBtn.textContent = "+ Add concept";
      addBtn.addEventListener("click", () => {
        if (pickerOpen) {
          closePicker();
        } else {
          openPicker();
        }
      });
      barEl.appendChild(addBtn);
    }
  }

  // ---------------------------------------------------------------------------
  // Concept Picker — add concepts inline (FR-20–22)
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

  function renderPickerList() {
    const listEl = document.getElementById("picker-list");
    listEl.innerHTML = "";

    const selectedSet = new Set(_state.concepts);
    // pickerOrder mirrors the cost-landscape chart (tree-grouped, LCOE-asc
    // within band) and excludes concepts the chart excludes (freeform /
    // non-grounded / no cost model). Resolve each ID back to its manifest
    // entry; skip any that are no longer in the manifest (defensive).
    const byId = {};
    manifest.concepts.forEach((c) => {
      byId[c.concept_id] = c;
    });
    const available = pickerOrder
      .map((id) => byId[id])
      .filter((entry) => entry && !selectedSet.has(entry.concept_id));

    // Count header
    const countEl = el("div", "text-muted text-xs");
    countEl.style.cssText = "padding: 0 var(--space-3); margin-bottom: var(--space-2);";
    countEl.textContent = `${_state.concepts.length} of ${MAX_LANDSCAPE} selected`;
    listEl.appendChild(countEl);

    if (_state.concepts.length >= MAX_LANDSCAPE) {
      listEl.appendChild(
        el("p", "text-muted text-sm", "Maximum concepts selected.")
      );
      return;
    }

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
      const pickLbl = conceptLabel(entry);
      item.setAttribute("role", "option");
      item.setAttribute("aria-label", `Add ${pickLbl.text}`);

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
      nameSpan.appendChild(pickLbl.codeChip());
      nameSpan.appendChild(document.createTextNode(" " + pickLbl.name));

      const familyInfo = FAMILY_META[entry.confinement_family] ?? {
        label: entry.confinement_family,
        cls: "badge badge-nonstandard",
      };
      const familyBadge = el("span", familyInfo.cls, familyInfo.label);

      // Picker reads from the manifest, which does not currently carry
      // asterisk_in_comparison — surfacing the asterisk here would require
      // extending ConceptManifestEntry. Out of Phase 2 scope.
      append(item, nameSpan, familyBadge);

      // Company hidden in the compare picker (anonymized explorer, 2026-06-08).

      item.addEventListener("click", () => addConcept(entry.concept_id));
      listEl.appendChild(item);
    }
  }

  async function addConcept(conceptId) {
    if (_state.concepts.length >= MAX_LANDSCAPE) return;
    if (_state.concepts.includes(conceptId)) return;

    try {
      await fetchConcept(conceptId);
    } catch (err) {
      console.error("[compare] Failed to fetch concept:", conceptId, err);
      return;
    }

    _state.concepts.push(conceptId);

    // Auto-switch to landscape if exceeding integrated max
    if (_state.concepts.length > MAX_INTEGRATED && _state.mode === "integrated") {
      _state.mode = "landscape";
    }

    syncUrl();
    postState();
    closePicker();
    renderAll();
  }

  function removeConcept(conceptId) {
    _state.concepts = _state.concepts.filter((id) => id !== conceptId);
    // Don't force switch back to integrated on removal — keep current mode
    syncUrl();
    postState();
    renderAll();
  }

  // ---------------------------------------------------------------------------
  // Mode Toggle (FR-4–6)
  // ---------------------------------------------------------------------------

  function renderModeToggle() {
    const toggleEl = document.getElementById("mode-toggle");
    const count = _state.concepts.length;
    const hasConcepts = count > 0;

    toggleEl.style.display = hasConcepts ? "" : "none";
    if (!hasConcepts) return;

    const intBtn = document.getElementById("mode-integrated");
    const lndBtn = document.getElementById("mode-landscape");

    // Labels with count
    intBtn.textContent = `Integrated (${count})`;
    lndBtn.textContent = `Landscape (${count})`;

    // Integrated disabled when > MAX_INTEGRATED
    const intDisabled = count > MAX_INTEGRATED;
    intBtn.disabled = intDisabled;

    // Active styling
    if (_state.mode === "integrated") {
      intBtn.className = "btn btn--primary";
      lndBtn.className = "btn btn--ghost";
    } else {
      intBtn.className = "btn btn--ghost";
      lndBtn.className = "btn btn--primary";
    }
  }

  // ---------------------------------------------------------------------------
  // View Selector Utility
  // ---------------------------------------------------------------------------

  /**
   * Populate a <select> element with VIEW_REGISTRY options.
   * @param {HTMLSelectElement} selectEl
   * @param {string} selectedValue — currently selected view key
   * @param {string|null} disabledValue — view key to disable (for mutual exclusion)
   */
  function populateViewSelect(selectEl, selectedValue, disabledValue) {
    selectEl.innerHTML = "";
    for (const [key, view] of Object.entries(VIEW_REGISTRY)) {
      const option = document.createElement("option");
      option.value = key;
      option.textContent = view.label;
      if (key === selectedValue) option.selected = true;
      if (key === disabledValue) option.disabled = true;
      selectEl.appendChild(option);
    }
  }

  // ---------------------------------------------------------------------------
  // View Dispatch & Placeholder (FR-15, FR-16)
  // ---------------------------------------------------------------------------

  /**
   * Build concept data array from current state for rendering.
   */
  function getConceptDataArray() {
    return _state.concepts
      .map((id) => conceptCache[id])
      .filter(Boolean)
      .map((c) => ({
        concept_id: c.concept_id,
        name: c.name,
        confinement_family: c.confinement_family,
        data: c,
      }));
  }

  /**
   * Render view content into a container. Dispatches to registered renderer
   * or falls back to placeholder.
   */
  function renderViewContent(container, viewName, concepts, mode) {
    container.innerHTML = "";
    const view = VIEW_REGISTRY[viewName];
    if (!view) {
      renderPlaceholder(container, viewName, concepts);
      return;
    }

    if (mode === "integrated" && view.renderIntegrated) {
      view.renderIntegrated(container, concepts);
    } else if (mode === "landscape" && view.renderLandscape) {
      // For landscape, concepts is a single concept object
      view.renderLandscape(container, concepts, {
        allConcepts: getConceptDataArray(),
        sharedScales: {},
      });
    } else {
      renderPlaceholder(container, viewName, concepts);
    }
  }

  /**
   * Render placeholder card confirming data routing (FR-16).
   * @param {HTMLElement} container
   * @param {string} viewName
   * @param {Object|Object[]} concepts — single concept or array
   */
  function renderPlaceholder(container, viewName, concepts) {
    const view = VIEW_REGISTRY[viewName];
    const label = view ? view.label : viewName;
    const conceptArr = Array.isArray(concepts) ? concepts : [concepts];

    const card = el("div", "compare-placeholder");

    const heading = el("div", null, label);
    heading.style.cssText = "font-size: var(--font-size-md); font-weight: 600; color: var(--color-text-secondary);";
    card.appendChild(heading);

    const subtitle = el("div", null, "View renderer not yet registered");
    subtitle.style.cssText = "font-size: var(--font-size-xs); margin-bottom: var(--space-3);";
    card.appendChild(subtitle);

    for (const c of conceptArr) {
      const row = document.createElement("div");
      row.style.cssText = "display: flex; align-items: center; gap: var(--space-2);";

      const familyInfo = FAMILY_META[c.confinement_family] ?? {
        label: c.confinement_family,
        cls: "badge badge-nonstandard",
      };
      const rowLbl = conceptLabel(c);
      const rowName = el("span", null);
      rowName.appendChild(rowLbl.codeChip());
      rowName.appendChild(document.createTextNode(" " + rowLbl.name));
      append(
        row,
        el("span", familyInfo.cls, familyInfo.label),
        rowName
      );
      card.appendChild(row);
    }

    container.appendChild(card);
  }

  // ---------------------------------------------------------------------------
  // Integrated Layout (FR-7–10)
  // ---------------------------------------------------------------------------

  function renderIntegrated() {
    document.getElementById("compare-integrated").style.display = "";
    document.getElementById("compare-landscape").style.display = "none";

    const concepts = getConceptDataArray();

    // Populate view selectors with mutual exclusion
    const selectLeft = document.getElementById("select-left");
    const selectRight = document.getElementById("select-right");

    populateViewSelect(selectLeft, _state.left, _state.right);
    populateViewSelect(selectRight, _state.right, _state.left);

    // Render panel contents
    renderViewContent(document.getElementById("content-left"), _state.left, concepts, "integrated");
    renderViewContent(document.getElementById("content-right"), _state.right, concepts, "integrated");
  }

  function renderLandscape() {
    document.getElementById("compare-landscape").style.display = "";
    document.getElementById("compare-integrated").style.display = "none";

    const concepts = getConceptDataArray();

    // Populate view selector
    const selectLandscape = document.getElementById("select-landscape");
    populateViewSelect(selectLandscape, _state.view, null);

    // Build grid
    const gridEl = document.getElementById("landscape-grid");
    gridEl.innerHTML = "";

    // Grid class based on concept count
    gridEl.className = "compare-landscape-grid";
    if (concepts.length === 1) {
      gridEl.classList.add("compare-landscape-grid--1up");
    } else if (concepts.length <= 3) {
      gridEl.classList.add("compare-landscape-grid--2up");
    } else {
      gridEl.classList.add("compare-landscape-grid--3up");
    }

    for (const concept of concepts) {
      const cell = el("div", "compare-landscape-cell");

      // Cell header: #code + name + family badge
      const header = el("div", "compare-landscape-cell__header");
      const familyInfo = FAMILY_META[concept.confinement_family] ?? {
        label: concept.confinement_family,
        cls: "badge badge-nonstandard",
      };
      const cellLbl = conceptLabel(concept);
      const cellName = el("span", null);
      cellName.appendChild(cellLbl.codeChip());
      cellName.appendChild(document.createTextNode(" " + cellLbl.name));
      append(
        header,
        cellName,
        lowGroundingMarker(concept),
        el("span", familyInfo.cls, familyInfo.label),
      );
      cell.appendChild(header);

      // Cell content area
      const content = el("div", "compare-landscape-cell__content");
      renderViewContent(content, _state.view, concept, "landscape");
      cell.appendChild(content);

      gridEl.appendChild(cell);
    }
  }

  // ---------------------------------------------------------------------------
  // Render orchestrator
  // ---------------------------------------------------------------------------

  function renderAll() {
    const hasConcepts = _state.concepts.length > 0;

    document.getElementById("empty-state").style.display = hasConcepts ? "none" : "";

    renderConceptBar();
    renderModeToggle();

    if (hasConcepts) {
      if (_state.mode === "integrated") {
        renderIntegrated();
      } else {
        renderLandscape();
      }
    } else {
      document.getElementById("compare-integrated").style.display = "none";
      document.getElementById("compare-landscape").style.display = "none";
    }
  }

  // ---------------------------------------------------------------------------
  // Initialisation
  // ---------------------------------------------------------------------------

  async function init() {
    const loadingEl = document.getElementById("loading-state");
    const errorEl = document.getElementById("error-state");
    const warningEl = document.getElementById("warning-banner");
    const contentEl = document.getElementById("compare-content");

    loadingEl.style.display = "";
    contentEl.style.display = "none";
    errorEl.style.display = "none";
    warningEl.style.display = "none";

    // Step 1-2: Fetch manifest + the same payloads the cost landscape uses,
    // so the picker can list concepts in the chart's order and omit those the
    // chart excludes (freeform / non-grounded / no cost model).
    let registry, tree, landscape;
    try {
      const payloads = await Promise.all([
        fetchManifest(),
        fetch("/api/taxonomy/registry").then((r) => r.json()),
        fetch("/api/taxonomy/tree").then((r) => r.json()),
        fetch("/api/cost-landscape").then((r) => r.json()),
      ]);
      manifest = payloads[0];
      registry = payloads[1];
      tree = payloads[2];
      landscape = payloads[3];
    } catch (err) {
      console.error("[compare] Failed to load manifest:", err);
      loadingEl.style.display = "none";
      errorEl.style.display = "";
      return;
    }

    // Build the cost-landscape display order: same tree grouping + within-band
    // LCOE-ascending sort the chart applies. Concepts not in landscape.concepts
    // (freeform / non-grounded / no cost model) are dropped, matching the
    // chart's exclusion rule.
    try {
      const costById = {};
      (landscape.concepts || []).forEach((c) => {
        costById[c.concept_id] = c;
      });
      const joined = matrixData.joinConcepts(manifest, registry);
      const rows = joined
        .filter((r) => costById[r.concept_id])
        .map((r) => Object.assign({}, r, { cost: costById[r.concept_id] }));
      const bands = matrixData.project(
        rows,
        { groupBy: "tree", sortKey: "code", sortDir: "asc", filter: null },
        tree,
      );
      bands.forEach((b) => {
        b.rows.sort((a, b) => {
          const la = a.cost.lcoe,
            lb = b.cost.lcoe;
          if (la !== lb) return la - lb;
          return String(a.concept_id) < String(b.concept_id) ? -1 : 1;
        });
      });
      pickerOrder = [];
      bands.forEach((b) => {
        b.rows.forEach((r) => pickerOrder.push(r.concept_id));
      });
    } catch (err) {
      console.warn("[compare] cost-landscape ordering failed, falling back to manifest order:", err);
      pickerOrder = manifest.concepts.map((c) => c.concept_id);
    }

    // Step 3: Parse URL and validate
    const parsed = parseUrl();
    const { state: corrected, warnings } = validateAndCorrect(parsed);
    _state = corrected;

    // Step 4: Show warnings
    if (warnings.length > 0) {
      warningEl.textContent = warnings.join(" · ");
      warningEl.style.display = "";
    }

    // Step 5: Fetch concept data for all valid IDs (parallel)
    if (_state.concepts.length > 0) {
      const results = await Promise.allSettled(
        _state.concepts.map((id) => fetchConcept(id))
      );
      // Remove concepts that failed to fetch
      const failed = [];
      for (let i = results.length - 1; i >= 0; i--) {
        if (results[i].status === "rejected") {
          failed.push(_state.concepts[i]);
          _state.concepts.splice(i, 1);
        }
      }
      if (failed.length > 0) {
        const msg = `Failed to load: ${failed.join(", ")}`;
        warningEl.textContent = warningEl.style.display === "none"
          ? msg
          : warningEl.textContent + " · " + msg;
        warningEl.style.display = "";
      }
    }

    // Step 6: Write corrected state back to URL
    syncUrl();

    // Step 7: Sync comparison_set to server (fire-and-forget)
    postState();

    // Step 8-9: Show content, wire events, render
    loadingEl.style.display = "none";
    contentEl.style.display = "";

    // Wire close-picker button
    document.getElementById("close-picker").addEventListener("click", closePicker);

    // Close picker on click-outside
    document.addEventListener("click", (e) => {
      if (!pickerOpen) return;
      const pickerEl = document.getElementById("concept-picker");
      if (pickerEl.contains(e.target)) return;
      if (document.getElementById("concept-bar").contains(e.target)) return;
      closePicker();
    });

    // Wire mode toggle buttons
    document.getElementById("mode-integrated").addEventListener("click", () => {
      if (_state.concepts.length > MAX_INTEGRATED) return;
      _state.mode = "integrated";
      syncUrl();
      renderAll();
    });
    document.getElementById("mode-landscape").addEventListener("click", () => {
      _state.mode = "landscape";
      syncUrl();
      renderAll();
    });

    // Wire integrated view selectors
    document.getElementById("select-left").addEventListener("change", (e) => {
      _state.left = e.target.value;
      syncUrl();
      // Update mutual exclusion on right dropdown
      populateViewSelect(document.getElementById("select-right"), _state.right, _state.left);
      // Re-render left panel only
      renderViewContent(
        document.getElementById("content-left"),
        _state.left,
        getConceptDataArray(),
        "integrated"
      );
    });
    document.getElementById("select-right").addEventListener("change", (e) => {
      _state.right = e.target.value;
      syncUrl();
      // Update mutual exclusion on left dropdown
      populateViewSelect(document.getElementById("select-left"), _state.left, _state.right);
      // Re-render right panel only
      renderViewContent(
        document.getElementById("content-right"),
        _state.right,
        getConceptDataArray(),
        "integrated"
      );
    });

    // Wire landscape view selector
    document.getElementById("select-landscape").addEventListener("change", (e) => {
      _state.view = e.target.value;
      syncUrl();
      // Re-render all landscape cells (scoped to grid container)
      const concepts = getConceptDataArray();
      const cells = document.getElementById("landscape-grid")
        .querySelectorAll(".compare-landscape-cell__content");
      cells.forEach((cell, i) => {
        if (concepts[i]) {
          renderViewContent(cell, _state.view, concepts[i], "landscape");
        }
      });
    });

    renderAll();
  }

  // ---------------------------------------------------------------------------
  // popstate — browser back/forward
  // ---------------------------------------------------------------------------

  window.addEventListener("popstate", () => {
    if (!manifest) return;
    const parsed = parseUrl();
    const { state: corrected } = validateAndCorrect(parsed);
    _state = corrected;
    // Only replaceState if validation changed something, to preserve history entries
    const parsed2 = parseUrl();
    if (corrected.concepts.join(",") !== parsed2.concepts.join(",") ||
        corrected.mode !== parsed2.mode) {
      syncUrl();
    }
    renderAll();
  });

  // ---------------------------------------------------------------------------
  // Boot
  // ---------------------------------------------------------------------------

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
