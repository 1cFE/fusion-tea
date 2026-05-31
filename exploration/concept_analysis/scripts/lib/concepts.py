"""Concept table loading, resolution, and 1costingfe mapping.

Two loaders live here, by design:

* ``load_concepts()`` — the orchestrator's record loader. Joins the four Item 5
  tables (ontology / archetype_fit / comparables / design_point) on
  ``concept_id`` and augments one display field (``Company``) from the legacy
  table. This is the single place anything asks "what archetype / family /
  comparables / design point / routing state" for a concept.
* ``load_legacy_table()`` — residual-fields source. Scoring and heatmap still
  read legacy-only architecture columns (Fuel, MFE Topology, …) that the four
  new tables intentionally do not carry. Retired once scoring v2 migrates.
"""

import csv
import re
from pathlib import Path

from lib.paths import (
    ARCHETYPE_FIT_PATH,
    COMPARABLES_PATH,
    COSTINGFE_EXAMPLES_DIR,
    DESIGN_POINT_PATH,
    FREEFORM_ROUTES_PATH,
    ONTOLOGY_PATH,
    TABLE_PATH,
)

# ---------------------------------------------------------------------------
# Enum-keyed 1costingFE library hints (rehomed from COSTINGFE_MAPPING)
# ---------------------------------------------------------------------------
# A library fact keyed on the ConfinementConcept enum: which worked example the
# model-setup prompt imitates. Most enums share dt_tokamak.py; only the few with
# a dedicated example differ. Tiny by design — Item 8 may collapse this into a
# single canonical in-prompt example and drop the map. Kept inline (not a new
# module) until then. The retired COSTINGFE_MAPPING's `defaults` (auto-loaded by
# the library from the enum) and `notes` (migrated to archetype_fit.fit_rationale)
# are not reproduced here. FUEL_MAPPING is gone — fuel_enum is already DT/DD/etc.
ENUM_LIBRARY_HINTS: dict[str, dict] = {
    "TOKAMAK": {"example": "dt_tokamak.py"},
    "STELLARATOR": {"example": "dt_stellarator.py"},
    "MIRROR": {"example": "dt_mirror.py"},
    "PULSED_FRC": {"example": "dhe3_pulsed_frc.py"},
}
# Every other enum imitates the tokamak worked example (closest available).
_DEFAULT_LIBRARY_HINT = {"example": "dt_tokamak.py"}


def get_costingfe_library_hints(record: dict) -> dict:
    """Assemble the costingfe model-setup library hints for a concept.

    Returns ``{example_path, costingfe_concept, costingfe_fuel}`` from the
    record's ``archetype_enum`` + ``fuel_enum`` and ``ENUM_LIBRARY_HINTS``. The
    enum values are already in library form (``TOKAMAK`` / ``DT`` / …) — no
    translation. Replaces ``get_costingfe_mapping`` (per-concept) + the
    ``FUEL_MAPPING`` translator.
    """
    enum = record.get("archetype_enum", "") or ""
    hint = ENUM_LIBRARY_HINTS.get(enum, _DEFAULT_LIBRARY_HINT)
    return {
        "example_path": str(COSTINGFE_EXAMPLES_DIR / hint["example"]),
        "costingfe_concept": enum,
        "costingfe_fuel": record.get("fuel_enum", "") or "",
    }


def get_model_path(record: dict) -> str:
    """Select the model-setup template path for a concept (FR-1).

    Fit-grade-only: ``costingfe`` for any ``fit_grade != "None"`` (including
    ``pending-design-point`` concepts), ``freeform`` for ``None``. This is the
    template-selection function (``loop.py`` model-setup) — it answers "which
    template", not "may this concept run now". The strict runnability gate is a
    *separate* predicate, ``is_costingfe_runnable`` (design.md Invariant #7);
    do NOT unify them — that would route every pending concept to freeform.

    Returns: 'costingfe' | 'freeform'
    """
    return "costingfe" if record.get("fit_grade") != "None" else "freeform"


def get_comparison_status(record: dict) -> str:
    """Compute the four-state routing status from three sources (FR-4).

    Consults ``fit_grade`` (archetype mappability), ``design_point`` membership
    + ``grounding_confidence`` (data quality), and ``in_freeform_routes``
    (judged-freeform discriminator). Returns one of:

      * ``freeform-deferred``   — ``fit_grade == None`` OR judged freeform
        (in ``design_point_freeform_routes.md``). Out of scope to model.
      * ``pending-design-point`` — mappable, but no design-point row yet and not
        judged freeform. Transient: Item 5's batch hasn't reached it. Distinct
        from ``freeform-deferred`` so a concept awaiting data is not mistaken
        for one judged out of scope.
      * ``costingfe-asterisked`` — runnable, design-point grounding is ``low``.
      * ``costingfe``           — runnable, design-point grounding ∈ {high, medium}.
    """
    if record.get("fit_grade") == "None":
        return "freeform-deferred"
    if record.get("in_freeform_routes"):
        return "freeform-deferred"
    dp = record.get("design_point")
    if dp is None:
        return "pending-design-point"
    grounding = (dp.get("grounding_confidence") or "").strip().lower()
    return "costingfe-asterisked" if grounding == "low" else "costingfe"


def is_costingfe_runnable(record: dict) -> bool:
    """Strict gate: may a costingfe stage chain actually run on this concept?

    True iff ``get_comparison_status(record) ∈ {costingfe, costingfe-asterisked}``
    — i.e. mappable AND a design-point row exists. Used ONLY by
    ``regenerate-concept``'s refusal guard (design.md Invariant #7). A
    ``pending-design-point`` concept is ``get_model_path == "costingfe"`` but
    ``is_costingfe_runnable == False``: it would pick the costingfe template if a
    stage ran, but the only stage-chain runner refuses it with a clear reason.
    """
    return get_comparison_status(record) in {"costingfe", "costingfe-asterisked"}


def load_legacy_table(csv_path: Path = TABLE_PATH) -> list[dict]:
    """Load the legacy concept table from CSV. Returns list of concept dicts.

    Residual fields only — do not extend. The four Item 5 tables are the source
    of truth for every routing/comparison/framing field; this loader survives
    only for (a) scoring/heatmap's legacy architecture columns (Fuel, MFE
    Topology, …) and (b) ``load_concepts``' one-field ``Company`` augment, until
    scoring v2 retires it.

    Each dict has all CSV columns plus:
      - _id: the ID column value (e.g., '01-hts-compact-tokamak')
      - _num: the numeric prefix (e.g., '01', '17a')
      - _research_id: Research ID column (Phase 1a dir) or _id
    """
    concepts = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["_id"] = row["ID"]
            # Extract numeric prefix: '01' from '01-hts-compact-tokamak',
            # '17a' from '17a-laser-icf-hybrid-drive'
            m = re.match(r"^(\d+[a-z]?)-", row["ID"])
            row["_num"] = m.group(1) if m else row["ID"]
            # Research ID maps to Phase 1a directory (for split concepts like 17a/17b)
            row["_research_id"] = row.get("Research ID") or row["_id"]
            concepts.append(row)
    return concepts


# ===========================================================================
# Concept record loader — the four-table join (orchestrator source of truth)
# ===========================================================================

# Canonical storage is snake_case; the legacy capitalized keys below are
# populated ONCE at record construction and treated as read-only views over the
# canonical fields (design.md Invariant #4). Never mutated, never the source of
# truth. Retired once scoring/heatmap/cmd_list/cmd_status migrate to canonical.
_LEGACY_ALIAS_MAP = {
    "concept_id": "_id",
    "concept_num": "_num",
    "research_id": "_research_id",
    "concept_name": "Concept Name",
    "company": "Company",
    "confinement_family": "Confinement Family",
}


def _read_csv_by_id(path: Path, key: str = "concept_id") -> dict[str, dict]:
    """Read a table CSV into a dict keyed on ``key``. Missing file → empty."""
    out: dict[str, dict] = {}
    if not Path(path).exists():
        return out
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            out[row[key]] = row
    return out


def _split_comparables(raw: str) -> list[str]:
    """Split the ``; ``-separated comparables cell into a clean list.

    Empty cell → ``[]`` (honest "no comparable in corpus", not an error).
    """
    raw = (raw or "").strip()
    if not raw:
        return []
    return [tok.strip() for tok in raw.split(";") if tok.strip()]


def load_freeform_routes() -> set[str]:
    """Parse the judged-freeform concept_ids out of the freeform-routes log.

    This is the discriminator between ``pending-design-point`` (transient —
    Item 5's batch hasn't reached the row) and ``freeform-deferred`` (permanent,
    by judgment — Item 5 logged the concept as having no P_native anywhere).

    The log is created lazily by Item 5's proposal batch; a missing file means
    "no concepts judged freeform yet" and MUST return an empty set, not raise.
    """
    if not Path(FREEFORM_ROUTES_PATH).exists():
        return set()
    text = Path(FREEFORM_ROUTES_PATH).read_text(encoding="utf-8")
    # Concept_id grammar: two-digit prefix, optional letter, slug body.
    return set(re.findall(r"\b(\d{2}[a-z]?-[a-z][a-z0-9-]+)", text))


def _build_record(
    cid: str, ont: dict, af: dict, comp: dict, dp: dict | None,
    legacy: dict, in_freeform: bool,
) -> dict:
    """Assemble one ConceptRecord from the joined table rows."""
    m = re.match(r"^(\d+[a-z]?)-", cid)
    num = m.group(1) if m else cid
    record = {
        # --- canonical snake_case storage (source of truth) ---
        "concept_id": cid,
        "concept_num": num,
        "research_id": legacy.get("Research ID") or cid,
        "concept_name": ont.get("concept_name", "") or legacy.get("Concept Name", ""),
        "company": legacy.get("Company", ""),  # one-field augment from legacy table
        "confinement_family": ont.get("confinement_family", ""),
        "confinement_subfamily": ont.get("confinement_subfamily", ""),
        "fuel": ont.get("fuel", ""),
        "driver_class": ont.get("driver_class", ""),
        "conversion_path": ont.get("conversion_path", ""),
        "fit_grade": af.get("fit_grade", ""),
        "archetype_enum": af.get("confinementconcept_enum", ""),
        "fuel_enum": af.get("fuel_enum", ""),
        "fit_rationale": af.get("fit_rationale", ""),
        "comparables": _split_comparables(comp.get("comparables", "")),
        "design_point": dict(dp) if dp else None,
        "in_freeform_routes": in_freeform,
    }
    # Read-only legacy aliases, populated once from canonical fields.
    for canon, legacy_key in _LEGACY_ALIAS_MAP.items():
        record[legacy_key] = record[canon]
    return record


def load_concepts() -> list[dict]:
    """Load the joined concept records — the orchestrator's source of truth.

    Joins ontology / archetype_fit / comparables / design_point on
    ``concept_id`` and augments ``Company`` from the legacy table. One record per
    ``archetype_fit.csv`` row. Pure function of disk-resident CSVs — no LLM, no
    network (design.md Invariant #2). Missing ``design_point_freeform_routes.md``
    is treated as an empty set.
    """
    ontology = _read_csv_by_id(ONTOLOGY_PATH)
    archetype = _read_csv_by_id(ARCHETYPE_FIT_PATH)
    comparables = _read_csv_by_id(COMPARABLES_PATH)
    design_points = _read_csv_by_id(DESIGN_POINT_PATH)
    legacy = {r["_id"]: r for r in load_legacy_table()}
    freeform = load_freeform_routes()

    records = []
    for cid, af in archetype.items():  # one record per archetype_fit row
        records.append(_build_record(
            cid,
            ontology.get(cid, {}),
            af,
            comparables.get(cid, {}),
            design_points.get(cid),
            legacy.get(cid, {}),
            cid in freeform,
        ))
    return records


def resolve_one(concepts: list[dict], query: str) -> list[dict]:
    """Resolve a single query to matching concepts.

    Matches against: numeric prefix (01, 17a), full ID, slug portion,
    or partial company name (case-insensitive).
    Returns list of matches (0, 1, or many).
    """
    q = query.strip()

    # Exact ID match
    for c in concepts:
        if c["_id"] == q:
            return [c]

    # Numeric prefix match (e.g., '01' or '17a')
    for c in concepts:
        if c["_num"] == q:
            return [c]

    # Slug match — query matches the part after the numeric prefix
    for c in concepts:
        slug = c["_id"].split("-", 1)[1] if "-" in c["_id"] else ""
        if slug == q:
            return [c]

    # Partial name or company (case-insensitive)
    ql = q.lower()
    matches = [
        c
        for c in concepts
        if ql in c["Concept Name"].lower() or ql in c.get("Company", "").lower()
    ]
    return matches


def resolve_concepts(
    args: list[str], concepts: list[dict], *, family: str | None = None, all_remaining: bool = False,
    target_state: str | None = None,
) -> list[dict]:
    """Resolve CLI concept arguments to a list of concept dicts.

    Handles: numeric IDs, full IDs, partial names, --all, --family.
    target_state: for --all filtering, skip concepts already at this state.
    """
    from lib.state import get_concept_state

    if all_remaining:
        result = concepts
        if family:
            result = [c for c in result if c.get("Confinement Family", "") == family]
        if target_state:
            result = [
                c for c in result
                if get_concept_state(c["_id"]) != target_state
            ]
        return result

    if family and not args:
        return [c for c in concepts if c.get("Confinement Family", "") == family]

    resolved = []
    for q in args:
        matches = resolve_one(concepts, q)
        if len(matches) == 0:
            raise ValueError(f"No concept matching '{q}'")
        elif len(matches) > 1:
            detail = ", ".join(f"{m['_id']}: {m['Concept Name']}" for m in matches)
            raise ValueError(
                f"Ambiguous query '{q}' matched {len(matches)} concepts: {detail}"
            )
        resolved.append(matches[0])

    if family:
        resolved = [c for c in resolved if c.get("Confinement Family", "") == family]

    return resolved
