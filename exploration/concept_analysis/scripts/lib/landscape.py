"""Build inline concept landscape for prompt injection."""

import re
from pathlib import Path

from lib.paths import ANALYSES_DIR
from lib.state import get_concept_state, get_extraction_state, get_iteration_summary


# Columns to exclude from the landscape table (internal infrastructure).
# The legacy-table path contributes the first set; the ConceptRecord path
# (load_concepts) contributes the snake_case canonical + structural keys, so the
# landscape renders the legacy display aliases (Concept Name / Company /
# Confinement Family) rather than duplicating them or trying to stringify the
# nested `comparables` (list) / `design_point` (dict) fields.
_EXCLUDE_COLUMNS = {
    "Research ID", "_id", "_num", "_research_id",
    # ConceptRecord canonical storage + structural fields:
    "concept_id", "concept_num", "research_id", "concept_name", "company",
    "confinement_family", "confinement_subfamily", "fuel", "driver_class",
    "conversion_path", "fit_grade", "archetype_enum", "fuel_enum",
    "fit_rationale", "comparables", "design_point", "in_freeform_routes",
}


def build_concept_landscape(
    concepts: list[dict],
    exclude_id: str | None = None,
    analyses_dir: Path = ANALYSES_DIR,
) -> str:
    """Build inline markdown concept landscape for prompt injection.

    Groups by status tier: approved → in-progress → gap-checked → not-started.
    Includes all taxonomy columns plus pipeline status and extraction flag.
    """
    # Collect rows with state info
    rows = []
    for c in concepts:
        cid = c["_id"]
        if cid == exclude_id:
            continue
        state = get_concept_state(cid, analyses_dir)
        base_state = state.rstrip("*")
        iter_summary = get_iteration_summary(cid, analyses_dir)
        ext_state = get_extraction_state(cid)
        iter_count = extract_iter_count(iter_summary)
        rows.append({
            "concept": c,
            "base_state": base_state,
            "stale": state.endswith("*"),
            "iter_summary": iter_summary or "",
            "iter_count": iter_count,
            "ext_state": ext_state,
        })

    # Group into tiers
    approved = [r for r in rows if r["base_state"] == "approved"]
    in_progress = [r for r in rows if r["base_state"] in ("iterating", "reviewed", "synthesized")]
    gap_checked = [r for r in rows if r["base_state"] == "gap-checked"]
    not_started = [r for r in rows if r["base_state"] == "not-started"]

    # Sort within tiers
    approved.sort(key=lambda r: r["concept"]["_id"])
    in_progress.sort(key=lambda r: (-r["iter_count"], r["concept"]["_id"]))
    gap_checked.sort(key=lambda r: r["concept"]["_id"])
    not_started.sort(key=lambda r: r["concept"]["_id"])

    # Determine taxonomy columns from first concept
    if not concepts:
        return ""
    tax_cols = [k for k in concepts[0] if k not in _EXCLUDE_COLUMNS]

    total = len(rows)
    parts = [
        f"## Concept Landscape ({total} concepts)\n",
        "Use this catalog for nearest-neighbor identification and cross-concept positioning.",
        "Approved concepts have full analyses available; I{N} indicates N completed iterations.\n",
    ]

    if approved:
        parts.append("### Approved (primary cross-reference pool)\n")
        parts.append(_render_table(approved, tax_cols, show_iterations=True))

    if in_progress:
        parts.append("\n### In Progress (by maturity)\n")
        parts.append(_render_table(in_progress, tax_cols, show_iterations=True))

    if gap_checked:
        parts.append("\n### Gap-Checked\n")
        parts.append(_render_table(gap_checked, tax_cols, show_iterations=False))

    if not_started:
        parts.append("\n### Not Started\n")
        parts.append(_render_table(not_started, tax_cols, show_iterations=False))

    return "\n".join(parts)


def _render_table(rows: list[dict], tax_cols: list[str], show_iterations: bool) -> str:
    """Render a markdown table for a tier of concepts."""
    # Build header
    headers = list(tax_cols)
    if show_iterations:
        headers += ["Iterations", "Extracted"]
    else:
        headers += ["Extracted"]

    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join("---" for _ in headers) + "|")

    ext_symbols = {"not-extracted": "", "extracted": "E", "stale": "E*"}

    for r in rows:
        c = r["concept"]
        # Coerce to str — records may carry non-string values under excluded
        # keys, and defensive stringification keeps the table render crash-proof.
        vals = [str(c.get(col, "")) for col in tax_cols]
        if show_iterations:
            vals.append(r["iter_summary"])
        vals.append(ext_symbols.get(r["ext_state"], ""))
        lines.append("| " + " | ".join(vals) + " |")

    return "\n".join(lines)


def extract_iter_count(iter_summary: str | None) -> int:
    """'iter-3/PASS' → 3, None → 0."""
    if not iter_summary:
        return 0
    m = re.match(r"iter-(\d+)", iter_summary)
    return int(m.group(1)) if m else 0
