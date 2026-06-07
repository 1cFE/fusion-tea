/**
 * parameter_card.js — Parameter detail popover for tornado chart click events.
 *
 * Shows a dismissible popover anchored near a clicked element, displaying:
 * - Display name + baseline value (with display_multiplier applied)
 * - Source citation (omitted when absent)
 * - Assumed parameter range
 * - Confidence badge (? for low, ~ for medium, ✓ for high)
 * - Modeling note
 * - Category badge (color-coded per design system)
 * - "Also sensitive" section (cross-concept, sorted by |elasticity| desc)
 *
 * Depends on: explorer.css (badge/card classes), DOM layout with body element.
 */

"use strict";

// Active card element and its dismiss listeners — module-level singletons so
// only one card is visible at a time.
let _activeCard = null;
let _dismissOnClickOutside = null;
let _dismissOnEscape = null;

// Confidence badge display:
//   low → "?"  (uncertain, hatched in charts)
//   medium → "~" (approximate)
//   high → "✓" (well-established)
const CONFIDENCE_BADGE_SYMBOL = {
  low: "?",
  medium: "~",
  high: "✓",
};

const CONFIDENCE_BADGE_CLASS = {
  low: "badge-confidence--low",
  medium: "badge-confidence--medium",
  high: "badge-confidence--high",
};

// Category CSS modifier matches explorer.css `.badge-category--{slug}` classes.
const CATEGORY_BADGE_CLASS = {
  "shared-baseline": "badge-category--shared-baseline",
  "well-established": "badge-category--well-established",
  "key-innovation": "badge-category--key-innovation",
  "concept-unique": "badge-category--concept-unique",
  "high-risk": "badge-category--high-risk",
};

const CATEGORY_LABEL = {
  "shared-baseline": "Shared Baseline",
  "well-established": "Well Established",
  "key-innovation": "Key Innovation",
  "concept-unique": "Concept Unique",
  "high-risk": "High Risk",
};

/**
 * Dismiss and remove any currently-active parameter card.
 * Safe to call when no card is shown.
 */
function hideParameterCard() {
  if (_activeCard) {
    _activeCard.remove();
    _activeCard = null;
  }
  if (_dismissOnClickOutside) {
    document.removeEventListener("click", _dismissOnClickOutside, true);
    _dismissOnClickOutside = null;
  }
  if (_dismissOnEscape) {
    document.removeEventListener("keydown", _dismissOnEscape);
    _dismissOnEscape = null;
  }
}

/**
 * Format a baseline value by applying display_multiplier then appending unit.
 * Returns a string like "70%" or "1.2 GJ/kg".
 *
 * Why multiply before display: baselines are stored in model-native units
 * (e.g., 0.70 for 70%) but users expect human-readable units.
 */
function _formatBaseline(baseline, multiplier, unit) {
  const multiplied = baseline * (multiplier != null ? multiplier : 1);
  // Use toPrecision(4) to avoid floating-point noise, then parseFloat to trim trailing zeros.
  const formatted = String(parseFloat(multiplied.toPrecision(4)));
  return unit ? `${formatted}\u202F${unit}` : formatted; // narrow no-break space before unit
}

/**
 * Format a range pair [low, high] with unit.
 */
function _formatRange(range, multiplier, unit) {
  if (!range || range.length !== 2) return null;
  const m = multiplier != null ? multiplier : 1;
  const lo = parseFloat((range[0] * m).toPrecision(4));
  const hi = parseFloat((range[1] * m).toPrecision(4));
  return unit ? `[${lo}\u202F–\u202F${hi}]\u202F${unit}` : `[${lo}\u202F–\u202F${hi}]`;
}

/**
 * Position the card near `anchor` without overflowing the viewport.
 * Tries right-of-anchor first; falls back to left if it would clip.
 */
function _positionCard(card, anchor) {
  const rect = anchor.getBoundingClientRect();
  const vw = window.innerWidth;
  const vh = window.innerHeight;
  const cardW = card.offsetWidth || 320; // measured after append
  const cardH = card.offsetHeight || 200;

  // Preferred: just to the right of the anchor, vertically centered
  let left = rect.right + 8;
  let top = rect.top + rect.height / 2 - cardH / 2;

  // Clamp to viewport
  if (left + cardW > vw - 8) {
    // Fall back to left side
    left = rect.left - cardW - 8;
  }
  if (left < 8) left = 8;
  if (top < 8) top = 8;
  if (top + cardH > vh - 8) top = vh - cardH - 8;
  if (top < 8) top = 8;

  card.style.left = `${left}px`;
  card.style.top = `${top}px`;
}

/**
 * Build the card DOM element. Does not attach it to the document.
 */
function _buildCard(options) {
  const { paramName, sensitivity, metadata, crossConceptData } = options;

  const card = document.createElement("div");
  card.className = "parameter-card";
  card.setAttribute("role", "dialog");
  card.setAttribute("aria-modal", "false");
  card.setAttribute("aria-label", metadata.display_name || paramName);

  // ── Name row ──────────────────────────────────────────────────────────────
  const nameEl = document.createElement("div");
  nameEl.className = "parameter-card__name";
  nameEl.textContent = metadata.display_name || paramName;
  card.appendChild(nameEl);

  // ── Baseline value ────────────────────────────────────────────────────────
  const baselineEl = document.createElement("div");
  baselineEl.className = "parameter-card__baseline";
  baselineEl.textContent =
    "Baseline: " +
    _formatBaseline(
      sensitivity.baseline,
      metadata.display_multiplier,
      metadata.display_unit
    );
  card.appendChild(baselineEl);

  // ── Category badge ────────────────────────────────────────────────────────
  const categoryEl = document.createElement("div");
  categoryEl.className = "parameter-card__section";
  const catBadge = document.createElement("span");
  catBadge.className =
    "badge badge-category " +
    (CATEGORY_BADGE_CLASS[metadata.category] || "");
  catBadge.textContent =
    CATEGORY_LABEL[metadata.category] || metadata.category;
  categoryEl.appendChild(catBadge);
  card.appendChild(categoryEl);

  // ── Confidence badge ──────────────────────────────────────────────────────
  const confSection = document.createElement("div");
  confSection.className = "parameter-card__section";
  const confLabel = document.createElement("div");
  confLabel.className = "parameter-card__section-label";
  confLabel.textContent = "Confidence";
  confSection.appendChild(confLabel);
  const confBadge = document.createElement("span");
  confBadge.className =
    "badge badge-confidence " +
    (CONFIDENCE_BADGE_CLASS[metadata.confidence] || "");
  confBadge.textContent =
    (CONFIDENCE_BADGE_SYMBOL[metadata.confidence] || metadata.confidence) +
    " " +
    (metadata.confidence ? metadata.confidence.charAt(0).toUpperCase() + metadata.confidence.slice(1) : "");
  confSection.appendChild(confBadge);
  card.appendChild(confSection);

  // ── Range ─────────────────────────────────────────────────────────────────
  if (metadata.range) {
    const rangeFormatted = _formatRange(
      metadata.range,
      metadata.display_multiplier,
      metadata.display_unit
    );
    if (rangeFormatted) {
      const rangeSection = document.createElement("div");
      rangeSection.className = "parameter-card__section";
      const rangeLabel = document.createElement("div");
      rangeLabel.className = "parameter-card__section-label";
      rangeLabel.textContent = "Assumed Range";
      rangeSection.appendChild(rangeLabel);
      const rangeVal = document.createElement("div");
      rangeVal.className = "parameter-card__range";
      rangeVal.textContent = rangeFormatted;
      rangeSection.appendChild(rangeVal);
      card.appendChild(rangeSection);
    }
  }

  // ── Modeling note ─────────────────────────────────────────────────────────
  if (metadata.modeling_note) {
    const noteEl = document.createElement("div");
    noteEl.className = "parameter-card__note";
    noteEl.textContent = metadata.modeling_note;
    card.appendChild(noteEl);
  }

  // ── Source citation (omit entirely when absent) ───────────────────────────
  if (metadata.source) {
    const srcEl = document.createElement("div");
    srcEl.className = "parameter-card__source";
    srcEl.textContent = "Source: " + metadata.source;
    card.appendChild(srcEl);
  }

  // ── "Also sensitive" section ──────────────────────────────────────────────
  // Only shown when crossConceptData is provided and has at least one entry
  // for another concept (i.e., the concept list is non-empty).
  if (
    crossConceptData &&
    Array.isArray(crossConceptData.concepts) &&
    crossConceptData.concepts.length > 0
  ) {
    const alsoSection = document.createElement("div");
    alsoSection.className = "parameter-card__also-sensitive";

    const alsoLabel = document.createElement("div");
    alsoLabel.className = "parameter-card__section-label";
    alsoLabel.textContent = "Also Sensitive";
    alsoSection.appendChild(alsoLabel);

    // Sort by descending |elasticity|
    const sorted = crossConceptData.concepts
      .slice()
      .sort((a, b) => Math.abs(b.elasticity) - Math.abs(a.elasticity));

    const list = document.createElement("ul");
    list.className = "parameter-card__concept-list";

    sorted.forEach((entry) => {
      const item = document.createElement("li");
      item.className = "parameter-card__concept-item";

      const link = document.createElement("a");
      link.className = "parameter-card__concept-link";
      link.href = `/concept/${entry.concept_id}`;
      link.textContent = conceptLabel(entry).text;

      const elasticityEl = document.createElement("span");
      elasticityEl.className = "parameter-card__elasticity";
      // Show elasticity to 2 decimal places with sign
      const e = entry.elasticity;
      elasticityEl.textContent =
        (e >= 0 ? "+" : "") + parseFloat(e.toFixed(2));

      item.appendChild(link);
      item.appendChild(elasticityEl);
      list.appendChild(item);
    });

    alsoSection.appendChild(list);
    card.appendChild(alsoSection);
  }

  return card;
}

/**
 * Show a parameter detail card anchored near `anchor`.
 *
 * Dismisses any previously-shown card first (only one card at a time).
 *
 * @param {HTMLElement} anchor - Element to anchor the popover near.
 * @param {object} options
 * @param {string} options.paramName
 * @param {{ elasticity: number, baseline: number }} options.sensitivity
 * @param {object} options.metadata
 * @param {object|null} [options.crossConceptData]
 */
function showParameterCard(anchor, options) {
  // Dismiss any existing card before showing a new one
  hideParameterCard();

  const card = _buildCard(options);
  document.body.appendChild(card);

  // Position after appending so offsetWidth/Height are available
  _positionCard(card, anchor);

  _activeCard = card;

  // Dismiss on Escape keydown
  _dismissOnEscape = (e) => {
    if (e.key === "Escape") hideParameterCard();
  };
  document.addEventListener("keydown", _dismissOnEscape);

  // Dismiss on click outside — use capture so it fires before card's own listeners.
  // Delay one tick to avoid the click that opened the card from immediately closing it.
  setTimeout(() => {
    _dismissOnClickOutside = (e) => {
      if (_activeCard && !_activeCard.contains(e.target)) {
        hideParameterCard();
      }
    };
    document.addEventListener("click", _dismissOnClickOutside, true);
  }, 0);
}
