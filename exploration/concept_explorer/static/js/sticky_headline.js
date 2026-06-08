/**
 * sticky_headline.js — Sticky compact headline bar with reset button.
 *
 * Renders identity (name + family badge + company) and four headline stat pills
 * (LCOE / Overnight / Net Power / Capacity Factor) into a sticky bar pinned
 * below the topnav. Each pill carries a delta indicator that shows direction
 * vs. baseline once any slider moves.
 *
 * For standalone concepts (no sliders), the Reset button is omitted entirely.
 *
 * Public API:
 *   renderStickyHeadline(container, { concept, headline, hasSliders, onReset })
 *   updateStickyHeadline(container, headline, baselineHeadline)
 *   setResetEnabled(container, enabled)
 */

"use strict";

(function () {
  const FAMILY_LABELS = {
    MFE: "MFE",
    IFE: "IFE",
    MIF: "MIF",
    NONSTANDARD: "Non-std",
  };

  // Stats rendered into the sticky bar; order matters (left → right).
  // Each entry exposes how to extract the value from a `headline` object,
  // its display unit, and a fixed-decimal precision.
  const STATS = [
    {
      key: "lcoe",
      label: "LCOE",
      unit: "$/MWh",
      get: (h) => h.lcoe_per_mwh,
      fmt: (v) => v.toFixed(1),
    },
    {
      key: "overnight",
      label: "Overnight Cost",
      unit: "$/kW",
      get: (h) => h.overnight_cost_per_kw,
      fmt: (v) => v.toFixed(0),
    },
    {
      key: "net_power",
      label: "Net Power",
      unit: "MW",
      get: (h) => h.p_net_mw,
      fmt: (v) => v.toFixed(0),
    },
    {
      key: "capacity_factor",
      label: "Capacity Factor",
      unit: "%",
      // Headline reports the fraction; sticky shows percent.
      get: (h) => h.capacity_factor * 100,
      fmt: (v) => v.toFixed(1),
    },
  ];

  // ---------------------------------------------------------------------------

  /**
   * Render the sticky headline DOM into `container`.
   *
   * @param {HTMLElement} container
   * @param {Object}   options
   * @param {Object}   options.concept       — { name, company, confinement_family }
   * @param {Object|null} options.headline   — initial headline object; null on render means "no cost model"
   * @param {boolean}  options.hasSliders    — when false, omit the Reset button entirely
   * @param {Function} [options.onReset]     — invoked when Reset is clicked
   */
  function renderStickyHeadline(container, { concept, headline, hasSliders, onReset }) {
    container.innerHTML = "";
    container.classList.add("sticky-headline");
    // Freeform/standalone concepts compute LCOE in custom code with non-comparable
    // assumptions; we suppress the LCOE pill value to prevent misleading
    // cross-concept comparison. Other stats (overnight, net power, capacity
    // factor) remain visible — they're physical quantities, not model-relative.
    container.dataset.suppressLcoe =
      concept && concept.model_type === "standalone" ? "1" : "0";

    // --- Identity (#code + name + badge + company) ---
    const lbl = conceptLabel(concept);
    const crumb = _el("div", "sticky-headline__crumb");
    const crumbName = _el("span", "sticky-headline__crumb-name");
    crumbName.appendChild(lbl.codeChip());
    crumbName.appendChild(document.createTextNode(" " + lbl.name));
    crumb.appendChild(crumbName);

    const familyKey = _familyKey(concept.confinement_family);
    if (familyKey) {
      const badge = _el(
        "span",
        `sticky-headline__badge sticky-headline__badge--${familyKey.toLowerCase()}`,
        FAMILY_LABELS[familyKey] || familyKey,
      );
      crumb.appendChild(badge);
    }

    // Company hidden in the sticky headline (anonymized explorer, 2026-06-08).
    container.appendChild(crumb);

    // --- Stat pills ---
    const suppressLcoe = container.dataset.suppressLcoe === "1";
    for (const stat of STATS) {
      container.appendChild(
        _buildStatPill(stat, headline, suppressLcoe && stat.key === "lcoe"),
      );
    }

    // --- Reset (only when sliders exist) ---
    if (hasSliders) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "sticky-headline__reset";
      btn.textContent = "Reset";
      btn.disabled = true;
      btn.dataset.role = "reset";
      btn.addEventListener("click", () => {
        if (typeof onReset === "function") onReset();
      });
      container.appendChild(btn);
    }
  }

  /**
   * Update the four stat pills from a new headline. `baselineHeadline` drives
   * the delta indicator (direction + percentage vs. baseline).
   *
   * @param {HTMLElement} container
   * @param {Object} headline
   * @param {Object} baselineHeadline
   */
  function updateStickyHeadline(container, headline, baselineHeadline) {
    if (!headline) return;
    const suppressLcoe = container.dataset.suppressLcoe === "1";
    for (const stat of STATS) {
      const pill = container.querySelector(
        `.sticky-headline__pill[data-stat="${stat.key}"]`,
      );
      if (!pill) continue;
      const valueEl = pill.querySelector(".sticky-headline__pill-value");
      const deltaEl = pill.querySelector(".sticky-headline__pill-delta");

      if (suppressLcoe && stat.key === "lcoe") {
        valueEl.textContent = "—";
        deltaEl.textContent = "";
        deltaEl.classList.add("sticky-headline__pill-delta--neutral");
        continue;
      }

      const current  = stat.get(headline);
      const baseline = baselineHeadline ? stat.get(baselineHeadline) : null;
      if (Number.isFinite(current)) {
        valueEl.textContent = stat.fmt(current);
      }
      _renderDelta(deltaEl, baseline, current);
    }
  }

  /**
   * Toggle the Reset button's disabled state. No-op if Reset isn't present
   * (standalone concept).
   */
  function setResetEnabled(container, enabled) {
    const btn = container.querySelector('.sticky-headline__reset[data-role="reset"]');
    if (btn) btn.disabled = !enabled;
  }

  // ---------------------------------------------------------------------------
  // Internal helpers
  // ---------------------------------------------------------------------------

  function _buildStatPill(stat, headline, suppressValue) {
    const pill = _el("div", "sticky-headline__pill");
    pill.dataset.stat = stat.key;

    const row = _el("div", "sticky-headline__pill-row");
    const value = _el("span", "sticky-headline__pill-value");
    if (suppressValue) {
      value.textContent = "—";
    } else if (headline && Number.isFinite(stat.get(headline))) {
      value.textContent = stat.fmt(stat.get(headline));
    } else {
      value.textContent = "—";
    }
    row.appendChild(value);

    const unit = _el("span", "sticky-headline__pill-unit", stat.unit);
    row.appendChild(unit);

    const delta = _el("span", "sticky-headline__pill-delta sticky-headline__pill-delta--neutral");
    row.appendChild(delta);

    pill.appendChild(row);
    pill.appendChild(_el("div", "sticky-headline__pill-label", stat.label));
    return pill;
  }

  function _renderDelta(deltaEl, baseline, current) {
    deltaEl.classList.remove(
      "sticky-headline__pill-delta--up",
      "sticky-headline__pill-delta--down",
      "sticky-headline__pill-delta--neutral",
    );
    if (!Number.isFinite(baseline) || baseline === 0 || !Number.isFinite(current)) {
      deltaEl.textContent = "";
      deltaEl.classList.add("sticky-headline__pill-delta--neutral");
      return;
    }
    const dPct = ((current - baseline) / baseline) * 100;
    if (Math.abs(dPct) < 0.05) {
      deltaEl.textContent = "";
      deltaEl.classList.add("sticky-headline__pill-delta--neutral");
      return;
    }
    if (dPct > 0) {
      deltaEl.textContent = ` \u25B2${dPct.toFixed(1)}%`;
      deltaEl.classList.add("sticky-headline__pill-delta--up");
    } else {
      deltaEl.textContent = ` \u25BC${Math.abs(dPct).toFixed(1)}%`;
      deltaEl.classList.add("sticky-headline__pill-delta--down");
    }
  }

  function _familyKey(raw) {
    if (!raw) return null;
    const upper = String(raw).toUpperCase();
    if (FAMILY_LABELS[upper]) return upper;
    return "NONSTANDARD";
  }

  function _el(tag, cls, text) {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  // Expose globals (no module system in this codebase)
  window.renderStickyHeadline = renderStickyHeadline;
  window.updateStickyHeadline = updateStickyHeadline;
  window.setResetEnabled = setResetEnabled;
})();
