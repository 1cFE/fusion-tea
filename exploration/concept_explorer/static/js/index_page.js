/**
 * index_page.js — Entry view grid for the Fusion TEA Concept Explorer.
 *
 * Fetches GET /api/manifest, groups concepts by status ("approved" vs
 * "in_progress"), and renders concept cards into the pre-existing DOM
 * sections.  Never shows a partial grid: either the loading state or the
 * complete grid is visible, never both.
 */

"use strict";

(function () {
  // ---------------------------------------------------------------------------
  // Confinement family badge label and CSS class
  // ---------------------------------------------------------------------------

  /** @type {Record<string, {label: string, cls: string}>} */
  const FAMILY_META = {
    mfe: { label: "MFE", cls: "badge badge-mfe" },
    ife: { label: "IFE", cls: "badge badge-ife" },
    mif: { label: "MIF", cls: "badge badge-mif" },
    nonstandard: { label: "Non-std", cls: "badge badge-nonstandard" },
  };

  // ---------------------------------------------------------------------------
  // Confidence badge
  // ---------------------------------------------------------------------------

  /** @type {Record<string, {label: string, cls: string}>} */
  const CONFIDENCE_META = {
    high: { label: "High confidence", cls: "badge badge-confidence badge-confidence--high" },
    medium: { label: "Medium confidence", cls: "badge badge-confidence badge-confidence--medium" },
    low: { label: "Low confidence", cls: "badge badge-confidence badge-confidence--low" },
  };

  // ---------------------------------------------------------------------------
  // DOM helpers
  // ---------------------------------------------------------------------------

  /** Create a DOM element with optional attributes and text content. */
  function el(tag, attrs, text) {
    const node = document.createElement(tag);
    if (attrs) {
      for (const [k, v] of Object.entries(attrs)) {
        if (k === "class") node.className = v;
        else node.setAttribute(k, v);
      }
    }
    if (text != null) node.textContent = text;
    return node;
  }

  // ---------------------------------------------------------------------------
  // Card builder
  // ---------------------------------------------------------------------------

  /**
   * Build a concept card element from a ConceptManifestEntry.
   *
   * @param {Object} entry  ConceptManifestEntry from the manifest API
   * @returns {HTMLElement}
   */
  function buildCard(entry) {
    const card = el("div", { class: "concept-card", role: "button", tabindex: "0" });
    card.setAttribute("aria-label", `View ${entry.name}`);

    // Navigate on click or Enter/Space keyboard activation
    function navigate() {
      window.location.href = `/concept/${entry.concept_id}`;
    }
    card.addEventListener("click", navigate);
    card.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        navigate();
      }
    });

    // Illustration thumbnail (only when non-null)
    if (entry.illustration != null) {
      const img = el("img", {
        class: "concept-card__illustration",
        src: `/static/images/concepts/${entry.illustration}`,
        alt: `${entry.name} illustration`,
        loading: "lazy",
      });
      card.appendChild(img);
    }

    // Name
    card.appendChild(el("div", { class: "concept-card__name" }, entry.name));

    // Meta row: confinement family badge + company
    const meta = el("div", { class: "concept-card__meta" });

    const familyInfo = FAMILY_META[entry.confinement_family] ?? {
      label: entry.confinement_family.toUpperCase(),
      cls: "badge badge-nonstandard",
    };
    const familyBadge = el("span", { class: familyInfo.cls }, familyInfo.label);
    meta.appendChild(familyBadge);

    if (entry.asterisk_in_comparison) {
      const marker = el(
        "span",
        {
          class: "low-grounding-marker",
          title:
            "Low grounding: design-point rests on company-stated or single-source " +
            "numbers — interpret the cost number with caution.",
          "aria-label": "Low-grounding design point",
        },
        "⚠",
      );
      meta.appendChild(marker);
    }

    if (entry.company != null) {
      meta.appendChild(el("span", { class: "concept-card__company" }, entry.company));
    }
    card.appendChild(meta);

    // Indicators row: LCOE, confidence badge, sensitivity indicator
    // Only rendered when there is something to show.
    const indicators = el("div", { class: "concept-card__indicators" });

    if (entry.has_cost_model && entry.lcoe_per_mwh != null) {
      indicators.appendChild(
        el(
          "span",
          { class: "concept-card__lcoe" },
          `${entry.lcoe_per_mwh.toFixed(1)} $/MWh`
        )
      );
    }

    if (entry.confidence != null) {
      const confInfo = CONFIDENCE_META[entry.confidence] ?? null;
      if (confInfo != null) {
        indicators.appendChild(el("span", { class: confInfo.cls }, confInfo.label));
      }
    }

    if (entry.has_sensitivities) {
      // Unicode sigma (Σ) as a low-weight indicator that sensitivity data exists.
      // Screen-reader label provided via aria-label.
      const sensIcon = el("span", { class: "badge badge-nonstandard", "aria-label": "Has sensitivity data" }, "Σ");
      indicators.appendChild(sensIcon);
    }

    // Only append indicators row when it has content
    if (indicators.children.length > 0) {
      card.appendChild(indicators);
    }

    return card;
  }

  // ---------------------------------------------------------------------------
  // Grid renderer
  // ---------------------------------------------------------------------------

  /**
   * Populate a grid element with concept cards.
   *
   * @param {HTMLElement} gridEl      The .concept-grid container
   * @param {Object[]}    entries     Filtered ConceptManifestEntry array
   * @param {string}      emptyLabel  Text for the empty-state div when no entries
   */
  function populateGrid(gridEl, entries, emptyLabel) {
    // Clear any prior content (e.g. server-rendered placeholder)
    gridEl.innerHTML = "";

    if (entries.length === 0) {
      const empty = el("div", { class: "concept-grid--empty" }, emptyLabel);
      gridEl.appendChild(empty);
      return;
    }

    const fragment = document.createDocumentFragment();
    for (const entry of entries) {
      fragment.appendChild(buildCard(entry));
    }
    gridEl.appendChild(fragment);
  }

  // ---------------------------------------------------------------------------
  // Main init
  // ---------------------------------------------------------------------------

  async function init() {
    const loadingEl = document.getElementById("loading-state");
    const groupsEl = document.getElementById("concept-groups");
    const errorEl = document.getElementById("error-state");

    // Guarantee: loading state visible, groups hidden until ready.
    loadingEl.style.display = "";
    groupsEl.style.display = "none";
    errorEl.style.display = "none";

    let manifest;
    try {
      const resp = await fetch("/api/manifest");
      if (!resp.ok) {
        throw new Error(`Server returned ${resp.status}`);
      }
      manifest = await resp.json();
    } catch (err) {
      console.error("Failed to fetch manifest:", err);
      loadingEl.style.display = "none";
      errorEl.style.display = "";
      return;
    }

    const approved = manifest.concepts.filter((c) => c.status === "approved");
    const inProgress = manifest.concepts.filter((c) => c.status === "in_progress");

    populateGrid(
      document.getElementById("grid-approved"),
      approved,
      "No approved concepts yet."
    );
    populateGrid(
      document.getElementById("grid-in-progress"),
      inProgress,
      "No concepts in progress."
    );

    // Atomically swap: hide loading, show complete grid.
    loadingEl.style.display = "none";
    groupsEl.style.display = "";
  }

  // Run after DOM is ready (script is at end of body, but guard anyway).
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
