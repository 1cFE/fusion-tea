/**
 * override_panel.js — Analyst override inspection drawer.
 *
 * One reusable, surface-agnostic panel that surfaces a concept's analyst cost
 * override registry. Opened from any ★ (CAS rows / treemap tiles / CapEx compare
 * bars) focused on a single account, or from the hero "(N entries)" chip showing
 * the whole registry. Reads only data already on the concept payload — never
 * fetches (INV-1).
 *
 * Form: a fixed right-side drawer (not anchored to the trigger), so it renders
 * identically from DOM rows, SVG tiles, a Plotly canvas, and a text chip, on both
 * the concept page and /compare. Lifecycle mirrors parameter_card.js: module-level
 * singleton, dismiss on Escape / overlay-click / close button.
 *
 * Public API:
 *   showOverridePanel({ records, focusAccount, conceptName })
 *   hideOverridePanel()
 *
 * Depends on: explorer.css (.override-panel* classes).
 */

"use strict";

// Singletons — only one drawer open at a time.
let _overrideDrawer = null;
let _overrideOverlay = null;
let _overrideDismissOnEscape = null;

/** Dismiss and remove any currently-open override drawer. Safe when none open. */
function hideOverridePanel() {
  if (_overrideDrawer) {
    _overrideDrawer.remove();
    _overrideDrawer = null;
  }
  if (_overrideOverlay) {
    _overrideOverlay.remove();
    _overrideOverlay = null;
  }
  if (_overrideDismissOnEscape) {
    document.removeEventListener("keydown", _overrideDismissOnEscape);
    _overrideDismissOnEscape = null;
  }
}

/** Create element with optional CSS class and text. */
function _opEl(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

/** Format a per-module M$ value, always tagged with its native scale so it does
 *  not read as contradicting the 1 GWe cost tables. */
function _opFormatValue(value) {
  if (!Number.isFinite(value)) return "not recorded";
  const n = value.toLocaleString("en-US", { maximumFractionDigits: 1 });
  return `${n} M$`;
}

/**
 * Render one labelled field. When `value` is null/empty, render an explicit
 * "not recorded" state instead of hiding the row (FR-6 — no silent vanish).
 */
function _opField(label, value, { pre = false } = {}) {
  const row = _opEl("div", "override-panel__field");
  row.appendChild(_opEl("div", "override-panel__field-label", label));
  const has = value != null && String(value).trim() !== "";
  const valEl = _opEl(
    "div",
    "override-panel__field-value" +
      (has ? (pre ? " override-panel__field-value--pre" : "") : " override-panel__field-value--missing"),
    has ? String(value) : "not recorded",
  );
  row.appendChild(valEl);
  return row;
}

/** Build one override card. */
function _opCard(rec) {
  const card = _opEl(
    "div",
    "override-panel__card" + (rec.enabled ? "" : " override-panel__card--disabled"),
  );

  // Heading: "C220103 — Magnets / Coils" + applied/not-applied tag.
  const head = _opEl("div", "override-panel__card-head");
  const title = _opEl("div", "override-panel__account");
  title.appendChild(_opEl("span", "override-panel__account-code", rec.account));
  if (rec.account_name) {
    title.appendChild(_opEl("span", "override-panel__account-name", `— ${rec.account_name}`));
  }
  head.appendChild(title);
  head.appendChild(
    _opEl(
      "span",
      "override-panel__tag " +
        (rec.enabled ? "override-panel__tag--applied" : "override-panel__tag--not-applied"),
      rec.enabled ? "applied" : "not applied",
    ),
  );
  card.appendChild(head);

  // Value, scale-labelled — but suppress the scale tag when the value itself is
  // not recorded, so the row never reads "not recorded native per-module scale" (m3).
  const valueRow = _opEl("div", "override-panel__value-row");
  const hasValue = Number.isFinite(rec.value);
  valueRow.appendChild(
    _opEl(
      "span",
      "override-panel__value" + (hasValue ? "" : " override-panel__value--missing"),
      _opFormatValue(rec.value),
    ),
  );
  if (hasValue) {
    valueRow.appendChild(
      _opEl("span", "override-panel__value-scale", "native per-module scale"),
    );
  }
  card.appendChild(valueRow);

  // Provenance.
  card.appendChild(_opField("Provenance", rec.provenance));
  // Source (free-text citation; rendered as text this phase).
  card.appendChild(_opField("Source", rec.source));
  // Rationale (multi-paragraph — preserve whitespace).
  card.appendChild(_opField("Rationale", rec.rationale, { pre: true }));
  // Cost basis.
  card.appendChild(_opField("Cost basis", rec.cost_basis));
  // Blocked-by — only meaningful for not-applied entries.
  if (!rec.enabled) {
    card.appendChild(_opField("Blocked by", rec.blocked_by));
  }

  return card;
}

/**
 * Open the override inspection drawer.
 *
 * @param {object} opts
 * @param {Array<object>} opts.records       OverrideRecord list from the concept payload.
 * @param {string} [opts.focusAccount]       CAS code to focus on (a single ★). When
 *                                           omitted, shows the whole registry.
 * @param {string} [opts.conceptName]        Shown in the drawer header.
 */
function showOverridePanel({ records, focusAccount, conceptName } = {}) {
  hideOverridePanel();

  const all = Array.isArray(records) ? records : [];

  let shown = all;
  if (focusAccount) {
    const key = String(focusAccount).toLowerCase();
    shown = all.filter((r) => String(r.account).toLowerCase() === key);
  } else {
    // Whole registry: enabled first, then not-applied.
    shown = all.slice().sort((a, b) => (a.enabled === b.enabled ? 0 : a.enabled ? -1 : 1));
  }

  // Overlay (click to dismiss).
  const overlay = _opEl("div", "override-panel__overlay");
  overlay.addEventListener("click", hideOverridePanel);
  document.body.appendChild(overlay);
  _overrideOverlay = overlay;

  // Drawer.
  const drawer = _opEl("div", "override-panel");
  drawer.setAttribute("role", "dialog");
  drawer.setAttribute("aria-modal", "true");
  drawer.setAttribute("aria-label", "Analyst cost adjustments");

  const header = _opEl("div", "override-panel__header");
  const titles = _opEl("div", "override-panel__titles");
  titles.appendChild(_opEl("div", "override-panel__title", "Analyst cost adjustments"));
  const subBits = [];
  if (conceptName) subBits.push(conceptName);
  if (focusAccount && shown.length) {
    subBits.push(shown[0].account);
  } else {
    // Break down applied vs not-applied so the header never collides with the
    // hero chip's enabled-only count (e.g. chip "1 entry" → "1 applied · 1 not
    // applied" rather than a bare "2 entries"). See m1.
    const applied = shown.filter((r) => r.enabled).length;
    const notApplied = shown.length - applied;
    const parts = [];
    if (applied) parts.push(`${applied} applied`);
    if (notApplied) parts.push(`${notApplied} not applied`);
    subBits.push(parts.length ? parts.join(" · ") : "no entries");
  }
  titles.appendChild(_opEl("div", "override-panel__subtitle", subBits.join(" · ")));
  header.appendChild(titles);

  const close = _opEl("button", "override-panel__close", "×");
  close.setAttribute("aria-label", "Close");
  close.addEventListener("click", hideOverridePanel);
  header.appendChild(close);
  drawer.appendChild(header);

  const body = _opEl("div", "override-panel__body");
  if (shown.length === 0) {
    body.appendChild(
      _opEl(
        "div",
        "override-panel__empty",
        focusAccount
          ? "No analyst override recorded for this account."
          : "No analyst overrides recorded for this concept.",
      ),
    );
  } else {
    for (const rec of shown) body.appendChild(_opCard(rec));
  }
  drawer.appendChild(body);

  document.body.appendChild(drawer);
  _overrideDrawer = drawer;

  _overrideDismissOnEscape = (e) => {
    if (e.key === "Escape") hideOverridePanel();
  };
  document.addEventListener("keydown", _overrideDismissOnEscape);
}
