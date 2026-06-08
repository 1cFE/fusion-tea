/**
 * concept_label.js — the single canonical naming helper (Theme A / A1).
 *
 * Every surface that names a concept goes through `conceptLabel()` instead of
 * reading `.name` directly, so the four-strings divergence the spine fixes
 * cannot recur. The server already stamps the canonical `Name (Fuel)` onto the
 * `name` field of every payload (manifest entry, ConceptData, ConceptTaxonomy,
 * similarity report, constellation point) via `resolve_identity` — this helper
 * is the front-end half: it pairs that name with the visible `#code` handle
 * (FR-A1.2) and formats both consistently for DOM, Plotly, and Cytoscape sites.
 *
 * Loaded as a plain global (no ES modules in this app) BEFORE every page's
 * surface scripts; exposed as `window.conceptLabel`.
 */

"use strict";

(function () {
  /**
   * Resolve a concept-like payload to its canonical label parts + formatters.
   *
   * @param {Object} c  Any payload with `concept_id` (or `code`) and `name`:
   *                    ConceptManifestEntry, ConceptData, ConceptTaxonomy,
   *                    constellation point, similarity neighbor, etc.
   * @returns {{
   *   code: string, name: string, codeText: string, text: string,
   *   codeChip: function(): HTMLElement
   * }}
   *   - `code`     the concept code (e.g. "01", "17a") — empty if absent
   *   - `name`     the canonical `Name (Fuel)` (server-stamped)
   *   - `codeText` the visible code handle, e.g. "#17a" (empty if no code)
   *   - `text`     "#NN Name (Fuel)" for string contexts (Plotly/Cytoscape/HTML)
   *   - `codeChip()` a `<span class="concept-code">#NN</span>` DOM element
   */
  function conceptLabel(c) {
    const code = (c && (c.concept_id != null ? c.concept_id : c.code)) || "";
    const name = (c && c.name) || code || "";
    // Anonymized display (2026-06-08): concept-numbering chips and prefixes
    // are stripped everywhere so the explorer presents concepts generically
    // (by their technical descriptor + scale, not by analyst-assigned #NN).
    // Surfaces continue to call codeChip() / codeText for back-compatible
    // layout — these now return an empty inline element / empty string
    // respectively, so existing DOM construction does not crash and chart
    // tick labels collapse cleanly.
    return {
      code,
      name,
      codeText: "",
      text: name,
      codeChip() {
        // Return a no-op span so callers that appendChild() still work,
        // but the chip takes no visible space.
        return document.createDocumentFragment();
      },
    };
  }

  window.conceptLabel = conceptLabel;
})();
