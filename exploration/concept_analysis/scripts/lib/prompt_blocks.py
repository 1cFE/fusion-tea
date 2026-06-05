"""Pre-rendered prompt blocks built from a concept record (Item 8, Phase 3).

The template engine (`lib/templating.py`) has no loops, so anything the analyze /
model-setup prompts would otherwise have to *derive* (the design-point selection
block, the per-archetype canonical-account schema, the comparables list, the
fit-grade override-count rubric) is rendered here in code and passed in as a
substitution variable. The discipline lives at the variable boundary; the
prompts just consume the rendered string.

Shared by `run_analysis.py::_build_common_vars` (analyze) and
`loop.py::build_model_vars` (model-setup) so the two stages render the design
point and account schema identically.
"""

from __future__ import annotations

from lib.canonical_accounts import (
    ALL_CONFINEMENT_CONCEPT_ENUMS,
    fit_grade_band,
    get_canonical_accounts,
    render_account_block,
)
from lib.canonical_spec_keys import (
    get_canonical_spec_keys,
    render_spec_keys_block,
)


def design_point_block(concept: dict) -> str:
    """Render the top-of-body Design Point selection block (read-only).

    Sources the selection fields from the concept's joined ``design_point`` row
    (the same data the orchestrator writes into frontmatter), not from the
    analysis file — so it is available at cold-start before any analysis.md
    exists. Returns an honest placeholder when no design-point row exists yet.
    """
    dp = concept.get("design_point")
    if not dp:
        return (
            "## Design Point\n\n"
            "(No design-point row for this concept yet — selection is "
            "upstream-pending. Do not invent one.)"
        )

    sources = [s.strip() for s in (dp.get("primary_sources") or "").split(";") if s.strip()]
    src_lines = (
        "\n".join(f"  - {s}" for s in sources)
        if sources
        else "  - (none recorded in the design-point trace)"
    )
    return (
        "## Design Point\n\n"
        f"- Name: {dp.get('design_name', '')}\n"
        f"- Maturity: {dp.get('maturity_tier', '')}\n"
        f"- P_native: {dp.get('p_native_mwe', '')} MWe\n"
        f"- Grounding: {dp.get('grounding_confidence', '')}\n"
        f"- Primary sources:\n{src_lines}\n\n"
        "(Selection fields are orchestrator-fixed from the design-point table. "
        "Copy them verbatim; you are forbidden to edit them. The quantitative "
        "description of this plant belongs in Section 5.)"
    )


def canonical_accounts_block(concept: dict) -> str:
    """Render the per-archetype canonical 1costingFE account schema.

    Filtered to the concept's ``archetype_enum`` so the prompt cannot invite an
    override on an account the archetype does not touch. Returns an honest note
    (not a fabricated default list) when the concept has no archetype mapping.
    """
    enum = (concept.get("archetype_enum") or "").strip()
    if enum not in ALL_CONFINEMENT_CONCEPT_ENUMS:
        return (
            "(No 1costingFE archetype mapping for this concept — the canonical "
            "account schema does not apply. Do not propose account-coded overrides.)"
        )
    return render_account_block(get_canonical_accounts(enum))


def canonical_spec_keys_block(concept: dict) -> str:
    """Render the per-archetype canonical ``spec`` field glossary.

    Companion to ``canonical_accounts_block``. Tells the LLM at the moment it
    is authoring the ``spec`` dict what each field means, what units it
    expects, what a typical value range looks like, and which common
    confusions to avoid (``p_input`` vs ``p_fus``, ``B`` vs ``b_center``,
    ``e_driver_mj`` not in kJ, etc.). Filtered to the concept's
    ``archetype_enum`` so the LLM does not see ``chamber_length`` on a tokamak
    or ``e_driver_mj`` on a stellarator.

    The glossary is the prevention half of the concept-05/09 fix — the F9
    validator in ``validators.py`` is the detection half.
    """
    enum = (concept.get("archetype_enum") or "").strip()
    if enum not in ALL_CONFINEMENT_CONCEPT_ENUMS:
        return (
            "(No 1costingFE archetype mapping for this concept — the "
            "canonical spec-key glossary does not apply. Freeform concepts "
            "do not consume `spec`.)"
        )
    return render_spec_keys_block(get_canonical_spec_keys(enum))


def comparables_block(concept: dict) -> str:
    """Render the fixed Comparables list (frontmatter-sourced, upstream-fixed)."""
    comps = concept.get("comparables") or []
    if not comps:
        return "(No comparable concept in the corpus for this design point.)"
    return "\n".join(f"- {c}" for c in comps)


def fit_grade_band_line(concept: dict) -> str:
    """Render the one-line expected-override-count rubric for the LLM (FR-8).

    Sourced from ``FIT_GRADE_OVERRIDE_BAND`` (the single source) via
    ``fit_grade_band`` so the ``High → 0–4 / Med → 3–8 / Low → 6–12`` numbers do
    not drift between the analyze prompt, the assessment prompt, and the code.
    """
    grade = (concept.get("fit_grade") or "").strip()
    band = fit_grade_band(grade)
    if band is None:
        return (
            "(No archetype-fit grade for this concept — the override-count band "
            "does not apply.)"
        )
    low, high = band
    return (
        f"Archetype-Fit is {grade} → expect {low}–{high} enabled overrides. "
        "Flag in your output if your count falls outside this band."
    )
