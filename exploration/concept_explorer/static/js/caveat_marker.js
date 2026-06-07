/**
 * caveat_marker.js — the single honest-caveat device (Theme A / A3).
 *
 * Replaces the ~5 copy-pasted low-grounding ⚠ markers (each with its own
 * duplicated tooltip string) with one component. It covers every caveat
 * dimension in one consistent marker + plain-language hover (FR-A3.1/A3.2):
 *
 *   - asterisk      low grounding / single-source (the existing
 *                   `asterisk_in_comparison` signal; its tooltip already folds
 *                   single-source into low-grounding)
 *   - fitGrade      archetype fit — flagged when the RECORDED grade is "None"
 *                   (no costing-library archetype matches the concept)
 *   - missing       a named field that is NOT recorded — rendered as an explicit
 *                   "not recorded" caveat rather than a silent vanish (FR-A3.3)
 *
 * `caveatMarker(inputs)` always returns an object (so `.title`/`.any` are safe
 * to read); `.element()` / `.html()` yield null / "" when no caveat applies.
 * Loaded as a plain global BEFORE the surface scripts; `window.caveatMarker`.
 */

"use strict";

(function () {
  var GLYPH = "⚠"; // ⚠

  var ASTERISK_MSG =
    "Low grounding: design-point rests on company-stated or single-source " +
    "numbers — interpret the cost number with caution.";
  var FIT_NONE_MSG =
    "Archetype fit: None — no costing-library archetype matches this concept, " +
    "so its cost model is bespoke and less constrained.";

  function escapeAttr(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/"/g, "&quot;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  /**
   * @param {Object} inputs
   * @param {boolean} [inputs.asterisk]  low-grounding / single-source signal
   * @param {string}  [inputs.fitGrade]  "High"|"Med"|"Low"|"None"|null
   * @param {string}  [inputs.missing]   human label of an unrecorded field
   * @returns {{any:boolean, title:string, glyph:string,
   *            element:function():(HTMLElement|null), html:function():string}}
   */
  function caveatMarker(inputs) {
    inputs = inputs || {};
    var reasons = [];
    if (inputs.asterisk) reasons.push(ASTERISK_MSG);
    if (inputs.fitGrade === "None") reasons.push(FIT_NONE_MSG);
    if (inputs.missing) reasons.push(inputs.missing + " not recorded.");

    var any = reasons.length > 0;
    var title = reasons.join("  ·  ");

    return {
      any: any,
      title: title,
      glyph: GLYPH,
      /** DOM <span class="caveat-marker"> or null when no caveat applies. */
      element: function () {
        if (!any) return null;
        var span = document.createElement("span");
        span.className = "caveat-marker";
        span.textContent = GLYPH;
        span.title = title;
        span.setAttribute("aria-label", title);
        return span;
      },
      /** HTML string (leading space) for innerHTML sinks, or "" when none. */
      html: function () {
        if (!any) return "";
        var t = escapeAttr(title);
        return (
          ' <span class="caveat-marker" title="' +
          t +
          '" aria-label="' +
          t +
          '">' +
          GLYPH +
          "</span>"
        );
      },
    };
  }

  window.caveatMarker = caveatMarker;
})();
