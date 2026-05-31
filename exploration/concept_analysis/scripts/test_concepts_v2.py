#!/usr/bin/env python3
"""Tests for the table-driven concept record pipeline (Item 6 — pipeline glue).

Covers, phase by phase:
  Phase 1 — parse_frontmatter block-list round-trip; load_concepts() join.
  Phase 2 — get_model_path / get_comparison_status / is_costingfe_runnable.
  Phase 3 — make_frontmatter(record) rewrite + library-hint assembly.
  Phase 4 — loop.py call-site shape + symmetric prompt mitigation.
  Phase 5 — CLI dispatch split + init-tables + regenerate-concept.

The four upstream tables (ontology / archetype_fit / comparables / design_point)
are the source of truth; these tests pin the deterministic table reads.
"""

import subprocess
import sys
import textwrap
import time
from pathlib import Path

from lib.concepts import (
    FREEFORM_ROUTES_PATH,
    get_comparison_status,
    get_costingfe_library_hints,
    get_model_path,
    is_costingfe_runnable,
    load_concepts,
    load_freeform_routes,
    load_legacy_table,
)
from lib.frontmatter import make_frontmatter, parse_frontmatter

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

_UNSET = object()
_RUN_ANALYSIS = Path(__file__).resolve().parent / "run_analysis.py"


def _by_id() -> dict:
    return {r["concept_id"]: r for r in load_concepts()}


def _rec(fit_grade="High", design_point=_UNSET, dp_grounding=None,
         in_freeform_routes=False, **extra):
    """Build a minimal record dict for routing-predicate tests."""
    if dp_grounding is not None:
        dp = {"grounding_confidence": dp_grounding}
    elif design_point is not _UNSET:
        dp = design_point
    else:
        dp = None
    rec = {
        "fit_grade": fit_grade,
        "design_point": dp,
        "in_freeform_routes": in_freeform_routes,
    }
    rec.update(extra)
    return rec


def _strip_created(text: str) -> str:
    """Drop the volatile ``Created:`` line for golden comparison."""
    return "\n".join(l for l in text.splitlines() if not l.startswith("Created:"))


def _run(*cli_args, retries=4):
    """Invoke run_analysis.py as a subprocess. Retries to dodge the transient
    window where Item 5's background batch is rewriting design_point.csv."""
    last = None
    for _ in range(retries):
        last = subprocess.run(
            [sys.executable, str(_RUN_ANALYSIS), *cli_args],
            capture_output=True, text=True,
        )
        if "missing table file" not in (last.stderr + last.stdout):
            return last
        time.sleep(0.3)
    return last


# ===========================================================================
# Phase 1 — parser de-risk + load_concepts() foundation
# ===========================================================================


def test_parse_frontmatter_block_list_round_trip(tmp_path):
    p = tmp_path / "a.md"
    p.write_text("---\nID: 01-x\nComparables:\n  - 21-a\n  - 28-b\n---\nbody\n")
    fm = parse_frontmatter(p)
    assert fm["Comparables"] == ["21-a", "28-b"]


def test_load_concepts_basic_join():
    by_id = _by_id()
    r01 = by_id["01-hts-compact-tokamak"]
    assert r01["fit_grade"] == "High"
    assert r01["archetype_enum"] == "TOKAMAK"
    assert r01["confinement_family"] == "MFE"
    assert r01["comparables"] == [
        "21-spherical-tokamak-hts",
        "28-hts-tokamak-full-hts",
        "29-negative-triangularity-tokamak",
        "33-state-backed-tokamak-best",
    ]
    assert r01["design_point"]["p_native_mwe"] == "233"
    assert r01["design_point"]["grounding_confidence"] == "high"
    # Company augmented from the legacy table.
    assert r01["company"]
    # Legacy aliases are read-only views over canonical storage.
    assert r01["Confinement Family"] == r01["confinement_family"]
    assert r01["_id"] == r01["concept_id"]
    assert r01["Concept Name"] == r01["concept_name"]
    assert r01["Company"] == r01["company"]


def test_load_concepts_one_record_per_archetype_fit_row():
    import csv as _csv
    from lib.paths import ARCHETYPE_FIT_PATH

    with open(ARCHETYPE_FIT_PATH, newline="", encoding="utf-8-sig") as f:
        n_rows = sum(1 for _ in _csv.DictReader(f))
    assert len(load_concepts()) == n_rows


def test_load_concepts_empty_comparables_is_empty_list():
    # 02-acoustic-icf-sonofusion has an empty comparables cell (None-grade).
    assert _by_id()["02-acoustic-icf-sonofusion"]["comparables"] == []


def test_load_concepts_pending_concept_has_no_design_point():
    by_id = _by_id()
    freeform = load_freeform_routes()
    pending = next(
        r for r in by_id.values()
        if r["fit_grade"] != "None"
        and r["design_point"] is None
        and r["concept_id"] not in freeform
    )
    assert pending["design_point"] is None


def test_load_concepts_missing_freeform_routes_file_is_empty_set(monkeypatch, tmp_path):
    monkeypatch.setattr("lib.concepts.FREEFORM_ROUTES_PATH", tmp_path / "missing.md")
    assert load_freeform_routes() == set()
    records = load_concepts()
    assert len(records) > 0
    assert all(r["in_freeform_routes"] is False for r in records)


def test_load_freeform_routes_parses_concept_ids(monkeypatch, tmp_path):
    log = tmp_path / "design_point_freeform_routes.md"
    log.write_text(textwrap.dedent("""\
        # Freeform routes (by judgment)

        Concepts with no source-traceable P_native anywhere.

        - `06-magnetic-mirror` — Fisch: purely theoretical; no published P_native
        - 27-polywell — no electrical output published
        """))
    monkeypatch.setattr("lib.concepts.FREEFORM_ROUTES_PATH", log)
    routes = load_freeform_routes()
    assert "06-magnetic-mirror" in routes
    assert "27-polywell" in routes


def test_load_legacy_table_still_carries_topology_columns():
    rows = load_legacy_table()
    assert "Fuel" in rows[0]
    assert "Confinement Family" in rows[0]
    r01 = next(r for r in rows if r["_id"] == "01-hts-compact-tokamak")
    assert r01.get("Fuel")


# ===========================================================================
# Phase 2 — routing predicates (pure functions)
# ===========================================================================


def test_get_model_path_is_fit_grade_only():
    # FR-1: costingfe for any fit_grade != None, including pending.
    assert get_model_path(_rec(fit_grade="High", design_point=None)) == "costingfe"
    assert get_model_path(_rec(fit_grade="None")) == "freeform"


def test_is_costingfe_runnable_is_strict():
    runnable = _rec(fit_grade="High", design_point={"grounding_confidence": "high"})
    pending = _rec(fit_grade="High", design_point=None, in_freeform_routes=False)
    deferred = _rec(fit_grade="None")
    assert is_costingfe_runnable(runnable) is True
    assert is_costingfe_runnable(pending) is False
    assert is_costingfe_runnable(deferred) is False


def test_get_model_path_and_is_costingfe_runnable_disagree_for_pending():
    # C1-class regression pin: do NOT unify these two predicates.
    pending = _rec(fit_grade="High", design_point=None, in_freeform_routes=False)
    assert get_model_path(pending) == "costingfe"
    assert is_costingfe_runnable(pending) is False


def test_four_state_computation():
    assert get_comparison_status(_rec(fit_grade="High", dp_grounding="high")) == "costingfe"
    assert get_comparison_status(_rec(fit_grade="High", dp_grounding="medium")) == "costingfe"
    assert get_comparison_status(_rec(fit_grade="Low", dp_grounding="low")) == "costingfe-asterisked"
    assert get_comparison_status(_rec(fit_grade="None")) == "freeform-deferred"
    assert get_comparison_status(_rec(fit_grade="High", in_freeform_routes=True)) == "freeform-deferred"
    assert get_comparison_status(_rec(fit_grade="High", design_point=None)) == "pending-design-point"


def test_four_state_on_real_records():
    # 01 High/high → costingfe; 06 Low/low → costingfe-asterisked (real DP row);
    # 08 Low/medium, 14 Med/high → costingfe; None-grade → freeform-deferred.
    by_id = _by_id()
    assert get_comparison_status(by_id["01-hts-compact-tokamak"]) == "costingfe"
    assert get_comparison_status(by_id["06-magnetic-mirror"]) == "costingfe-asterisked"
    assert get_comparison_status(by_id["08-frc-w-direct-conversion"]) == "costingfe"
    assert get_comparison_status(
        by_id["14-magnetized-target-fusion-pneumatic-compression"]) == "costingfe"
    assert get_comparison_status(by_id["02-acoustic-icf-sonofusion"]) == "freeform-deferred"
    pending = next(r for r in by_id.values()
                   if r["fit_grade"] != "None" and r["design_point"] is None
                   and not r["in_freeform_routes"])
    assert get_comparison_status(pending) == "pending-design-point"
    assert get_model_path(pending) == "costingfe"
    assert is_costingfe_runnable(pending) is False


def test_runnable_iff_has_design_point_row():
    # Runnability == "has a design-point row" (all DP-row concepts are mappable
    # and non-freeform). Derive the expectation from the table itself so the
    # test is robust against Item 5's still-running design-point batch.
    by_id = _by_id()
    has_dp = {cid for cid, r in by_id.items() if r["design_point"] is not None}
    runnable = {cid for cid, r in by_id.items() if is_costingfe_runnable(r)}
    assert runnable == has_dp
    assert {"01-hts-compact-tokamak",
            "14-magnetized-target-fusion-pneumatic-compression"} <= runnable


# ===========================================================================
# Phase 3 — make_frontmatter rewrite + enum library hints
# ===========================================================================


def test_make_frontmatter_full_record_01():
    fm = make_frontmatter(_by_id()["01-hts-compact-tokamak"])
    expected = textwrap.dedent("""\
        ---
        ID: 01-hts-compact-tokamak
        Concept: HTS Compact Tokamak (Commonwealth Fusion / ARC)
        Company: Commonwealth Fusion Systems
        Status: draft
        Created: STRIPPED
        Approved-Date:
        Confinement-Family: MFE
        Archetype: TOKAMAK
        Archetype-Fit: High
        Comparison-Status: costingfe
        Comparables:
          - 21-spherical-tokamak-hts
          - 28-hts-tokamak-full-hts
          - 29-negative-triangularity-tokamak
          - 33-state-backed-tokamak-best
        Design-Point-Name: ARC 2015 Conservative Pilot phase (Sorbom et al.)
        Design-Point-Maturity: paper-concept
        P-Native: 233
        Grounding-Confidence: high
        ---
    """)
    assert _strip_created(fm) == _strip_created(expected)
    assert "Reuses" not in fm


def test_make_frontmatter_pending_omits_design_point_fields():
    by_id = _by_id()
    rec = next(r for r in by_id.values()
               if r["fit_grade"] != "None" and r["design_point"] is None
               and not r["in_freeform_routes"])
    fm = make_frontmatter(rec)
    assert "Comparison-Status: pending-design-point" in fm
    for field in ("Design-Point-Name", "Design-Point-Maturity",
                  "P-Native", "Grounding-Confidence"):
        assert f"{field}:" not in fm
    assert "Confinement-Family:" in fm
    assert "Archetype-Fit:" in fm


def test_make_frontmatter_none_grade():
    fm = make_frontmatter(_by_id()["02-acoustic-icf-sonofusion"])
    assert any(l.rstrip() == "Archetype:" for l in fm.splitlines())  # empty
    assert "Archetype-Fit: None" in fm
    assert "Comparison-Status: freeform-deferred" in fm
    assert "Comparables: []" in fm
    assert "Design-Point-Name:" not in fm


def test_make_frontmatter_round_trips_through_parser(tmp_path):
    rec = _by_id()["01-hts-compact-tokamak"]
    p = tmp_path / "a.md"
    p.write_text(make_frontmatter(rec) + "body\n")
    fm = parse_frontmatter(p)
    assert fm["Comparables"] == rec["comparables"]
    assert fm["Comparison-Status"] == "costingfe"
    assert fm["ID"] == "01-hts-compact-tokamak"
    assert fm["P-Native"] == "233"


def test_get_costingfe_library_hints_assembly():
    by_id = _by_id()
    h01 = get_costingfe_library_hints(by_id["01-hts-compact-tokamak"])
    assert h01["costingfe_concept"] == "TOKAMAK"
    assert h01["costingfe_fuel"] == "DT"
    assert h01["example_path"].endswith("dt_tokamak.py")

    h08 = get_costingfe_library_hints(by_id["08-frc-w-direct-conversion"])
    assert h08["costingfe_concept"] == "PULSED_FRC"
    assert h08["costingfe_fuel"] == "DHE3"
    assert h08["example_path"].endswith("dhe3_pulsed_frc.py")


# ===========================================================================
# Phase 4 — loop.py integration + symmetric prompt mitigation
# ===========================================================================


def test_loop_make_frontmatter_call_site_accepts_record(tmp_path):
    # loop.py:419 writes make_frontmatter(record) at cold start.
    record = _by_id()["01-hts-compact-tokamak"]
    out = tmp_path / "analysis.md"
    out.write_text(make_frontmatter(record))
    fm = parse_frontmatter(out)
    assert fm["ID"] == "01-hts-compact-tokamak"
    assert fm["Comparison-Status"] == "costingfe"


def test_loop_model_setup_vars_use_library_hints_and_empty_placeholders(tmp_path):
    from lib.loop import build_model_vars

    record = _by_id()["01-hts-compact-tokamak"]
    (tmp_path / "analysis.md").write_text("# D1+ Analysis\n")
    result = build_model_vars(record, tmp_path / "model_setup.py", tmp_path,
                              standalone=True)
    assert result is not None
    template_name, vars_dict = result
    assert template_name == "model_setup_costingfe.md"
    # Item 6→8 hazard A: placeholders, not real paths.
    assert vars_dict["defaults_path"] == ""
    assert vars_dict["mapping_notes"] == ""
    assert vars_dict["costingfe_concept"] == "TOKAMAK"
    assert vars_dict["costingfe_fuel"] == "DT"
    assert vars_dict["example_path"].endswith("dt_tokamak.py")


def test_analysis_v2_prompt_has_no_edit_reuses_step():
    from lib.paths import TEMPLATES_DIR

    text = (TEMPLATES_DIR / "analysis_v2.md").read_text(encoding="utf-8")
    assert "Reuses" not in text
    assert "Comparables" in text  # orchestrator-owned note names the renamed field


# ===========================================================================
# Phase 5 — CLI dispatch split + init-tables + regenerate-concept
# ===========================================================================


def test_dispatch_split_scoring_receives_legacy_table_shape():
    # C2 regression pin: scoring handlers must see legacy capitalized columns.
    rows = load_legacy_table()
    assert "Fuel" in rows[0] and "Confinement Family" in rows[0]
    r01 = next(r for r in rows if r["_id"] == "01-hts-compact-tokamak")
    assert r01.get("Fuel")  # empty if a record had been passed in


def test_init_tables_passes_on_current_repo():
    rc = _run("init-tables")
    assert rc.returncode == 0, rc.stderr


def test_init_tables_fails_on_missing_ontology_row(tmp_path):
    from run_analysis import _validate_tables

    research = tmp_path / "research"
    research.mkdir()
    (research / "01-x").mkdir()
    (research / "02-y").mkdir()
    (tmp_path / "ontology.csv").write_text(
        "concept_id,concept_name\n01-x,X\n02-y,Y\n")
    # archetype_fit.csv omits 02-y → strict failure.
    (tmp_path / "archetype_fit.csv").write_text(
        "concept_id,confinementconcept_enum,fuel_enum,fit_grade\n01-x,TOKAMAK,DT,High\n")
    (tmp_path / "comparables.csv").write_text("concept_id,comparables\n01-x,\n")
    (tmp_path / "design_point.csv").write_text("concept_id,grounding_confidence\n")

    errors, _summary = _validate_tables(
        research, tmp_path / "ontology.csv", tmp_path / "archetype_fit.csv",
        tmp_path / "comparables.csv", tmp_path / "design_point.csv",
        tmp_path / "missing_freeform.md",
    )
    assert any("02-y" in e and "archetype_fit" in e for e in errors), errors


def test_init_tables_fails_on_missing_table_file(tmp_path):
    from run_analysis import _validate_tables

    research = tmp_path / "research"
    research.mkdir()
    errors, _ = _validate_tables(
        research, tmp_path / "nope_ontology.csv", tmp_path / "nope_af.csv",
        tmp_path / "nope_comp.csv", tmp_path / "nope_dp.csv",
        tmp_path / "nope_freeform.md",
    )
    assert errors and all("missing table file" in e for e in errors)


def test_regenerate_concept_dry_run_runnable():
    rc = _run("regenerate-concept", "--dry-run", "01-hts-compact-tokamak")
    assert rc.returncode == 0, rc.stderr
    assert "gap-check" in rc.stdout
    assert "analyze" in rc.stdout
    assert "model-setup" in rc.stdout


def test_regenerate_concept_keep_gap_report_skips_gap_check():
    rc = _run("regenerate-concept", "--dry-run", "--keep-gap-report",
              "01-hts-compact-tokamak")
    assert rc.returncode == 0, rc.stderr
    assert "gap-check" not in rc.stdout
    assert "analyze" in rc.stdout


def test_regenerate_concept_refuses_pending_with_reason():
    by_id = _by_id()
    pending = next(cid for cid, r in by_id.items()
                   if r["fit_grade"] != "None" and r["design_point"] is None
                   and not r["in_freeform_routes"])
    rc = _run("regenerate-concept", "--dry-run", pending)
    assert rc.returncode != 0
    assert "pending-design-point" in rc.stderr


def test_regenerate_concept_refuses_none_grade_with_reason():
    rc = _run("regenerate-concept", "--dry-run", "02-acoustic-icf-sonofusion")
    assert rc.returncode != 0
    assert "fit_grade=None" in rc.stderr or "freeform" in rc.stderr


def test_regenerate_concept_refuses_unknown_with_reason():
    rc = _run("regenerate-concept", "--dry-run", "99-does-not-exist")
    assert rc.returncode != 0
    assert "archetype_fit" in rc.stderr
