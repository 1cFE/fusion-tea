# Implementation Plan: Pipeline Glue — Frontmatter, `concepts.py`, CLI Subcommands

**Status:** Complete (2026-05-31)
**Created:** 2026-05-31
**Last Updated:** 2026-05-31

## Source Documents

- **Spec:** [`spec.md`](spec.md) ← acceptance tests, FR-1…FR-8, four-state routing table
- **Design:** [`design.md`](design.md) ← architecture, component overview, bets, invariants, risks
- **Epic:** [`../../backlog/epic_concept_analysis_rework.md`](../../backlog/epic_concept_analysis_rework.md) (Item 6)

> This plan **does not repeat** design details. For component structure, data flow, dispatch split, key bets, invariants, and risks, follow the design.md links.

## Implementation Strategy

**Phasing rationale (5 phases):**

1. De-risk the silent-failure class (frontmatter parser round-trip) and land the data foundation (`load_concepts`).
2. Land pure routing functions on top of the foundation — no callers yet, so the C1-class disagreement bug can be pinned by regression test before any caller can drift.
3. Rewrite `make_frontmatter` and delete the old routing surface (`COSTINGFE_MAPPING`, `FAMILY_KEY_MAP`, `_is_freeform_architecture`, `FUEL_MAPPING`, etc.) — compile errors then force every downstream caller in Phases 4-5 to consume the new contract.
4. Wire `loop.py` (3 sites) + symmetric prompt belt-and-suspenders (Item 6↔8 hazard B). Loop is the highest-blast-radius integration; green-before-CLI-refactor is the discipline.
5. CLI dispatch split (C2), `init-tables`, `regenerate-concept`, cleanup.

**Critical path:** parser → loader → routing predicates → frontmatter rewrite → loop wiring → CLI.

**First proof point:** Phase 1's parser round-trip test. If `parse_frontmatter` doesn't yield `list[str]` for a block-list `Comparables:` field, the frontmatter contract is wrong and the parser is fixed before Phase 2 begins.

**Overall validation:** test-first per phase; the spec's acceptance tests are the end-of-Phase-5 gate.

---

## Phase 1 — Parser de-risk + `load_concepts()` foundation

### Goal

Prove `parse_frontmatter` round-trips block-list YAML lists. Land `load_concepts()` that joins the four new tables + `Company` augment from `load_legacy_table()` + `design_point_freeform_routes.md` membership, keyed on `concept_id`. Rename `load_table` → `load_legacy_table`.

### Assumption Under Test

- Block-list `Comparables:` parses to `list[str]` (no flow-list workaround needed).
- Joining four CSVs + one legacy augment on `concept_id` produces a record per `archetype_fit.csv` row with canonical snake_case storage and read-only legacy aliases.
- Missing `design_point_freeform_routes.md` is treated as empty set, not error.

### Test Stencil (write first)

```python
# test_concepts_v2.py

def test_parse_frontmatter_block_list_round_trip(tmp_path):
    p = tmp_path / "a.md"
    p.write_text("---\nID: 01-x\nComparables:\n  - 21-a\n  - 28-b\n---\nbody\n")
    fm = parse_frontmatter(p)
    assert fm["Comparables"] == ["21-a", "28-b"]

def test_load_concepts_basic_join():
    records = load_concepts()
    by_id = {r["concept_id"]: r for r in records}
    r01 = by_id["01-hts-compact-tokamak"]
    assert r01["fit_grade"] == "High"
    assert r01["archetype_enum"] == "TOKAMAK"
    assert r01["confinement_family"] == "MFE"
    assert r01["comparables"] == [
        "21-spherical-tokamak-hts", "28-hts-tokamak-full-hts",
        "29-negative-triangularity-tokamak", "33-state-backed-tokamak-best",
    ]
    assert r01["design_point"]["p_native_mwe"] == "233"
    assert r01["design_point"]["grounding_confidence"] == "high"
    # Company augmented from legacy table
    assert r01["company"]
    # Legacy aliases are read-only views over canonical
    assert r01["Confinement Family"] == r01["confinement_family"]
    assert r01["_id"] == r01["concept_id"]

def test_load_concepts_pending_concept_has_no_design_point():
    records = {r["concept_id"]: r for r in load_concepts()}
    # Pick any High/Med-fit concept without a design_point.csv row today
    pending = next(r for r in records.values()
                   if r["fit_grade"] != "None" and r["design_point"] is None
                   and r["concept_id"] not in load_freeform_routes())
    assert pending["design_point"] is None

def test_load_concepts_missing_freeform_routes_file_is_empty_set(monkeypatch, tmp_path):
    # Point freeform_routes path at a nonexistent file; should not raise
    monkeypatch.setattr("lib.concepts.FREEFORM_ROUTES_PATH", tmp_path / "missing.md")
    records = load_concepts()
    assert len(records) > 0  # still loads
```

### Changes Required

**See `design.md` for:** [Component Overview → `lib/concepts.py`](design.md#libconceptspy--rewrite), [Architecture → Data flow](design.md#data-flow), [Invariants #1, #4, #6](design.md#required-invariants).

**Specific files:**

#### 1. Test file (NEW)
**File:** `exploration/concept_analysis/scripts/test_concepts_v2.py`
- [ ] Write the 4 test stencils above
- [ ] Add: pending vs. freeform-deferred distinguishability test (synthetic freeform_routes entry)

#### 2. `lib/concepts.py` rewrite (foundation only — predicates land in Phase 2)
- [ ] Rename `load_table` → `load_legacy_table`; add one-line "residual fields only — do not extend" comment
- [ ] Add `FREEFORM_ROUTES_PATH` constant pointing at `exploration/concept_analysis/tables/design_point_freeform_routes.md`
- [ ] Add `load_freeform_routes() -> set[str]` — parses concept_ids out of the markdown log; missing file → empty set
- [ ] Add `load_concepts() -> list[dict]` — joins `ontology`/`archetype_fit`/`comparables`/`design_point` on `concept_id`; augments `company` from legacy; attaches `design_point: dict | None` and `in_freeform_routes: bool`
- [ ] Add `_LEGACY_ALIAS_MAP` and apply once at record build (read-only view discipline per Invariant #4)
- [ ] Do **not yet** remove `COSTINGFE_MAPPING`/`FAMILY_KEY_MAP`/`_is_freeform_architecture`/`get_costingfe_mapping`/`_get_subcategory`/`FUEL_MAPPING` — removal is Phase 3 (keeps current callers compiling between phases)

### Validation

**Automated:**
- [ ] `uv run python -m pytest exploration/concept_analysis/scripts/test_concepts_v2.py -v` → all green
- [ ] `uv run python -m pytest exploration/concept_analysis/scripts/test_validators.py` → no regressions
- [ ] `uv run python -c "from lib.concepts import load_concepts; print(len(load_concepts()))"` → matches `wc -l` of `archetype_fit.csv` minus header

**Manual:**
- [ ] Inspect a printed record for `01-hts-compact-tokamak` — confirm shape and alias correctness

**What we know works:** Parser handles the frontmatter list shape we'll emit in Phase 3; records carry every field downstream phases need; missing freeform-routes file is graceful.

---

## Phase 2 — Routing predicates (pure functions)

### Goal

Land `get_model_path` (fit-grade-only per FR-1), `get_comparison_status` (four states), `is_costingfe_runnable` (strict gate). Pin the C1-class regression: `get_model_path` and `is_costingfe_runnable` *intentionally disagree* for pending concepts.

### Assumption Under Test

Four-state computation matches spec acceptance test 2 (amended). `get_model_path` returns `costingfe` for pending concepts (per FR-1); `is_costingfe_runnable` returns False for them. The two functions are not unified — that's the bug class to prevent.

### Test Stencil (write first)

```python
def test_get_model_path_is_fit_grade_only():
    # FR-1: costingfe for any fit_grade != None, including pending
    assert get_model_path(_rec(fit_grade="High", design_point=None)) == "costingfe"
    assert get_model_path(_rec(fit_grade="None")) == "freeform"

def test_is_costingfe_runnable_is_strict():
    runnable = _rec(fit_grade="High", design_point={"grounding_confidence": "high"})
    pending  = _rec(fit_grade="High", design_point=None, in_freeform_routes=False)
    deferred = _rec(fit_grade="None")
    assert is_costingfe_runnable(runnable) is True
    assert is_costingfe_runnable(pending) is False
    assert is_costingfe_runnable(deferred) is False

def test_get_model_path_and_is_costingfe_runnable_disagree_for_pending():
    # C1-class regression pin: do not unify these two predicates
    pending = _rec(fit_grade="High", design_point=None, in_freeform_routes=False)
    assert get_model_path(pending) == "costingfe"
    assert is_costingfe_runnable(pending) is False

def test_four_state_computation():
    # Per spec acceptance test 2 (amended): 01 High/high, 14 Med/high, 08 Low/medium → costingfe
    # synthetic low grounding → costingfe-asterisked; None → freeform-deferred;
    # synthetic freeform_routes entry on High → freeform-deferred; pending → pending-design-point
    assert get_comparison_status(_rec(fit_grade="High", dp_grounding="high"))  == "costingfe"
    assert get_comparison_status(_rec(fit_grade="Low",  dp_grounding="low"))   == "costingfe-asterisked"
    assert get_comparison_status(_rec(fit_grade="None"))                       == "freeform-deferred"
    assert get_comparison_status(_rec(fit_grade="High", in_freeform_routes=True)) == "freeform-deferred"
    assert get_comparison_status(_rec(fit_grade="High", design_point=None))    == "pending-design-point"
```

### Changes Required

**See `design.md` for:** [Bet 2 — four-state routing](design.md#bet-2--comparison-status-as-the-routing-state-field-with-four-states-get_model_path-and-the-runnable-predicate-are-separate-open-question-resolved), [Invariant #7](design.md#required-invariants).

**Specific files:**

#### 1. Test file
**File:** `test_concepts_v2.py`
- [ ] Add `_rec(...)` helper that builds a minimal record dict
- [ ] Implement the 4 test stencils above

#### 2. `lib/concepts.py` — pure functions
- [ ] Add `get_model_path(record) -> "costingfe" | "freeform"` — `costingfe` iff `record["fit_grade"] != "None"`; docstring names *one* valid caller class (template selection in `loop.py`)
- [ ] Add `get_comparison_status(record) -> str` — four-state table; reads `fit_grade`, `design_point` presence + `grounding_confidence`, `in_freeform_routes`
- [ ] Add `is_costingfe_runnable(record) -> bool` — True iff `get_comparison_status(record) in {"costingfe", "costingfe-asterisked"}`; docstring names *one* valid caller class (`regenerate-concept`'s guard)

### Validation

**Automated:**
- [ ] All Phase 2 tests green
- [ ] Phase 1 tests still green

**Manual:**
- [ ] Print `(concept_id, get_model_path, get_comparison_status, is_costingfe_runnable)` for all records — eyeball that 01/08/14 are runnable, 02/16/35/38 are freeform-deferred, and the remaining ~33 are `pending-design-point` with `get_model_path == "costingfe"` (the intentional disagreement)

**What we know works:** Spec FR-1 + FR-4 satisfied in isolation. The C1 regression is pinned by a test that will fail if anyone tries to unify the two predicates.

---

## Phase 3 — `make_frontmatter` rewrite + remove old routing surface

### Goal

Rewrite `make_frontmatter` to take a record and emit the new orchestrator-owned block. Delete `COSTINGFE_MAPPING`, `FAMILY_KEY_MAP`, `_is_freeform_architecture`, `get_costingfe_mapping`, `_get_subcategory`, `FUEL_MAPPING`. Inline `ENUM_LIBRARY_HINTS` + `get_costingfe_library_hints` in `concepts.py`.

### Assumption Under Test

Golden frontmatter output for 01 (full), a pending concept (DP fields omitted, `Comparison-Status: pending-design-point`), a None-grade concept (`Comparables: []`, `Comparison-Status: freeform-deferred`). After deletion, no compilation breakage outside `loop.py` (Phase 4) and `run_analysis.py` (Phase 5) — i.e., nothing else imports the removed symbols.

### Test Stencil (write first)

```python
def test_make_frontmatter_full_record_01():
    records = {r["concept_id"]: r for r in load_concepts()}
    fm = make_frontmatter(records["01-hts-compact-tokamak"])
    expected = textwrap.dedent("""\
        ---
        ID: 01-hts-compact-tokamak
        Concept: HTS Compact Tokamak (Commonwealth Fusion / ARC)
        Company: Commonwealth Fusion Systems
        Status: draft
        Created: ...        # date — assert prefix
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
    # Strip Created line for comparison
    assert _strip_created(fm) == _strip_created(expected)
    assert "Reuses:" not in fm

def test_make_frontmatter_pending_omits_design_point_fields():
    rec = _pending_record_from_load_concepts()
    fm = make_frontmatter(rec)
    assert "Comparison-Status: pending-design-point" in fm
    for field in ("Design-Point-Name", "Design-Point-Maturity", "P-Native", "Grounding-Confidence"):
        assert f"{field}:" not in fm

def test_make_frontmatter_none_grade():
    rec = _record_by_id("02-acoustic-icf-sonofusion")
    fm = make_frontmatter(rec)
    assert "Archetype:" in fm and "Archetype: \n" in fm + "\n"  # empty
    assert "Archetype-Fit: None" in fm
    assert "Comparison-Status: freeform-deferred" in fm
    assert "Comparables: []" in fm

def test_make_frontmatter_round_trips_through_parser(tmp_path):
    rec = _record_by_id("01-hts-compact-tokamak")
    p = tmp_path / "a.md"
    p.write_text(make_frontmatter(rec) + "body\n")
    fm = parse_frontmatter(p)
    assert fm["Comparables"] == rec["comparables"]
    assert fm["Comparison-Status"] == "costingfe"
```

### Changes Required

**See `design.md` for:** [Component Overview → `lib/frontmatter.py`](design.md#libfrontmatterpy--make_frontmatter-rewrite), [Bet 3 — enum-keyed library hints](design.md#bet-3--enumlibrary-hints-rehomed-to-a-tiny-enum-keyed-map-inline-in-conceptspy-open-question-resolved), [Implementation Notes — list shape](design.md#implementation-notes).

**Specific files:**

#### 1. Tests
**File:** `test_concepts_v2.py` (extend) and a new section in or alongside (current) `test_frontmatter` if one exists
- [ ] Implement the 4 stencils above
- [ ] Helper `_strip_created` to omit the date line from comparison

#### 2. `lib/frontmatter.py:make_frontmatter`
- [ ] Rewrite to take a `record` dict and emit the new block per design
- [ ] Block-list (not flow-list) emission for `Comparables:` — invariant #3 + 1-line code comment
- [ ] Omit the 4 design-point fields when `record["design_point"] is None`
- [ ] `make_frontmatter`'s signature change is dict→dict; the legacy capitalized keys are still readable on the record via aliases, so this is backwards-source-compatible

#### 3. `lib/concepts.py` — removals + ENUM hints inline
- [ ] Delete `COSTINGFE_MAPPING`, `FAMILY_KEY_MAP`, `_is_freeform_architecture`, `get_costingfe_mapping`, `_get_subcategory`, `FUEL_MAPPING`
- [ ] Add inline (clearly demarcated section) `ENUM_LIBRARY_HINTS: dict[str, dict]` keyed on `ConfinementConcept` enum, with `example` filenames (4-6 entries, mostly `dt_tokamak.py`; specials per old map)
- [ ] Add `get_costingfe_library_hints(record) -> dict` — assembles `{example_path, costingfe_concept, costingfe_fuel}` from `record["archetype_enum"]`, `record["fuel_enum"]`, and `ENUM_LIBRARY_HINTS`

### Validation

**Automated:**
- [ ] All Phase 3 tests green
- [ ] `uv run python -c "import lib.concepts; import lib.frontmatter"` — no import errors
- [ ] `grep -n "COSTINGFE_MAPPING\|FAMILY_KEY_MAP\|_is_freeform_architecture\|get_costingfe_mapping\|FUEL_MAPPING" exploration/concept_analysis/scripts/lib/` → only matches in `loop.py` / `run_analysis.py` (cleaned in Phases 4-5)

**Manual:**
- [ ] Eyeball `make_frontmatter` output for one record of each state (full / pending / none-grade)
- [ ] Confirm the round-trip test (Phase 1's parser ↔ Phase 3's emitter) passes — this closes the silent-corruption loop the design called out as de-risk-first

**What we know works:** Frontmatter contract end-to-end (emit + parse). Old routing surface compile-removed; remaining references are quarantined to two files Phases 4-5 update.

---

## Phase 4 — `loop.py` integration + symmetric prompt belt-and-suspenders

### Goal

Update three call sites in `loop.py`. Ship `defaults_path: ""` / `mapping_notes: ""` placeholders (Item 6↔8 hazard A mitigation). Replace `prompt_templates/analysis_v2.md:112-120`'s "Edit Reuses" paragraph with the orchestrator-owned note (hazard B — symmetric mitigation).

### Assumption Under Test

`loop.py` continues to compile and the existing loop-related tests pass. Records (as built in Phase 1) are shape-compatible with every `concept[...]` access at the three call sites and every site downstream of `_run_*` that reads from the passed dict (verified via test + grep). Templates render without KeyError under the placeholder values.

> **Verify in this phase** (carry-forward from design's critical assessment): whether the loop currently passes a legacy-table dict or already a record-shaped dict at `loop.py:419`. If legacy, the alias-as-view discipline from Phase 1 makes the existing call site work unchanged once `loop.py` is invoked with records (which Phase 5 wires).

### Test Stencil (write first)

```python
def test_loop_make_frontmatter_call_site_accepts_record(tmp_path):
    # Simulate loop._init_analysis_file (or equivalent) writing frontmatter
    record = _record_by_id("01-hts-compact-tokamak")
    out = tmp_path / "analysis.md"
    out.write_text(make_frontmatter(record))
    fm = parse_frontmatter(out)
    assert fm["ID"] == "01-hts-compact-tokamak"

def test_loop_model_setup_vars_render_with_empty_defaults_placeholder():
    # vars_dict with defaults_path="" and mapping_notes="" must not blow up
    # the template's variable substitution
    record = _record_by_id("01-hts-compact-tokamak")
    hints = get_costingfe_library_hints(record)
    vars_dict = _build_model_setup_vars_costingfe(record, hints)  # extracted helper or inline
    assert vars_dict["defaults_path"] == ""
    assert vars_dict["mapping_notes"] == ""
    assert vars_dict["costingfe_concept"] == "TOKAMAK"
    assert vars_dict["costingfe_fuel"] == "DT"

def test_analysis_v2_prompt_has_no_edit_reuses_step():
    text = Path("exploration/concept_analysis/prompt_templates/analysis_v2.md").read_text()
    assert "Reuses" not in text
    assert "Comparables" in text  # the orchestrator-owned note mentions the renamed field
```

### Changes Required

**See `design.md` for:** [Component Overview → `lib/loop.py`](design.md#liblooppy--minimal-touch), [Interim assumption + Risks](design.md#interim-assumption-no-real-costingfe-runs-between-items-6-and-8).

**Specific files:**

#### 1. Tests
**File:** `test_concepts_v2.py` (extend)
- [ ] Implement the 3 stencils above

#### 2. `lib/loop.py` — three sites
- [ ] **Line 21** — `from lib.concepts import get_costingfe_mapping, get_model_path, FUEL_MAPPING` → `from lib.concepts import get_costingfe_library_hints, get_model_path`
- [ ] **Line 419** — `make_frontmatter(concept)` → `make_frontmatter(record)` (no semantic change; record carries legacy aliases)
- [ ] **Lines 712-738** — `mapping = get_costingfe_mapping(concept)` → `hints = get_costingfe_library_hints(record)`; `vars_dict["example_path"]` from `hints["example_path"]`; `vars_dict["costingfe_concept"]` from `hints["costingfe_concept"]`; `vars_dict["costingfe_fuel"]` from `hints["costingfe_fuel"]`; set `vars_dict["defaults_path"] = ""` and `vars_dict["mapping_notes"] = ""` as placeholders (Item 8 removes both ends in one commit)
- [ ] **Line 442 comment** — drop the "Claude may have updated Reuses" remark; replace with one line noting orchestrator-owned fields per Invariant #3

#### 3. `prompt_templates/analysis_v2.md:112-120`
- [ ] Replace the "Step 2: Update Reuses (if applicable)" paragraph with: `Comparables`, `Confinement-Family`, `Archetype`, `Archetype-Fit`, `Comparison-Status`, and the four `Design-Point-*` fields are orchestrator-owned and pre-populated from the upstream tables — do not edit them.
- [ ] Audit the rest of `analysis_v2.md` for `Reuses` references (renumber/remove cross-references)

### Validation

**Automated:**
- [ ] All Phase 4 tests green
- [ ] Phases 1-3 tests still green
- [ ] `uv run python -c "from lib import loop"` — no import errors
- [ ] `grep -n 'Reuses' exploration/concept_analysis/prompt_templates/analysis_v2.md` → 0 hits

**Manual:**
- [ ] Inspect the three changed loop.py sites; confirm `vars_dict` shape against the existing template's `{{var}}` references (don't break the variable substitution)
- [ ] Render the model-setup template with the new vars (a one-line `templating.render()` call) — no KeyError

**What we know works:** Loop integration green; orchestrator-owned fields are explicitly orchestrator-owned in the prompt; symmetric Item 6↔8 mitigations land together.

---

## Phase 5 — CLI dispatch split + `init-tables` + `regenerate-concept` + final cleanup

### Goal

Split `run_analysis.py`'s top-level dispatch per the design's table (orchestrator handlers ← records; scoring/heatmap handlers ← legacy table). Add `init-tables` and `regenerate-concept` subcommands. Remove stale `make_frontmatter` import (`run_analysis.py:46`). Confirm `grep -r 'Reuses' lib/` is clean.

### Assumption Under Test

Scoring/heatmap/calibrate handlers see the **same input shape they see today** (legacy table dicts) — Phase 5 changes their loader but not their consumed-shape. `init-tables` exits 0 on the current repo; injecting a missing `ontology`/`archetype_fit` row produces a non-zero exit with a specific report. `regenerate-concept --dry-run 01-hts-compact-tokamak` prints the stage sequence; refuses pending concepts with a `pending-design-point` reason.

### Test Stencil (write first)

```python
def test_dispatch_split_scoring_receives_legacy_table_shape():
    # cmd_score / cmd_calibrate / cmd_heatmap / cmd_extract_scores receive
    # rows with the legacy capitalized columns (Fuel, MFE Topology, etc.)
    rows = load_legacy_table()
    assert "Fuel" in rows[0] and "Confinement Family" in rows[0]
    # Sanity: a scoring helper that reads "Fuel" returns non-empty for a known row
    r01 = next(r for r in rows if r["_id"] == "01-hts-compact-tokamak")
    assert r01.get("Fuel")  # would be empty if a record had been passed in

def test_init_tables_passes_on_current_repo():
    rc = subprocess.run(["uv", "run", "python",
        "exploration/concept_analysis/scripts/run_analysis.py", "init-tables"],
        capture_output=True, text=True)
    assert rc.returncode == 0, rc.stderr

def test_init_tables_fails_on_missing_ontology_row(monkeypatch, tmp_path):
    # Point ontology at a CSV missing one of the on-disk concept dirs
    monkeypatch.setattr("lib.paths.ONTOLOGY_PATH", _csv_without_row(tmp_path, "01-hts-compact-tokamak"))
    rc = _run_init_tables()
    assert rc.returncode != 0
    assert "01-hts-compact-tokamak" in rc.stderr

def test_regenerate_concept_dry_run_runnable():
    rc = _run("regenerate-concept", "--dry-run", "01-hts-compact-tokamak")
    assert rc.returncode == 0
    assert "gap-check" in rc.stdout and "analyze" in rc.stdout
    assert "model-setup" in rc.stdout

def test_regenerate_concept_refuses_pending_with_reason():
    pending_id = _any_pending_concept_id()
    rc = _run("regenerate-concept", "--dry-run", pending_id)
    assert rc.returncode != 0
    assert "pending-design-point" in rc.stderr

def test_regenerate_concept_refuses_none_grade_with_reason():
    rc = _run("regenerate-concept", "--dry-run", "02-acoustic-icf-sonofusion")
    assert rc.returncode != 0
    assert "fit_grade=None" in rc.stderr or "freeform" in rc.stderr
```

### Changes Required

**See `design.md` for:** [CLI dispatch split](design.md#cli-dispatch-split--records-vs-legacy-table), [Subcommand sequence — regenerate-concept](design.md#subcommand-sequence--regenerate-concept), [Component Overview → run_analysis.py](design.md#run_analysispy--two-new-subcommands-dispatch-split).

**Specific files:**

#### 1. Tests
**File:** `test_concepts_v2.py` (extend) — or split out a `test_run_analysis_cli.py` if dispatch tests grow
- [ ] Implement the 6 stencils above
- [ ] Helper `_run(*args) -> CompletedProcess` for subcommand invocations

#### 2. `run_analysis.py` — dispatch + subcommands + cleanup
- [ ] **Line 46** — remove the stale `make_frontmatter` import
- [ ] **Line 1527** — replace `table = load_table()` with a 6-line dispatch branch that chooses `load_concepts()` vs. `load_legacy_table()` per the design's split table
- [ ] Add `cmd_init_tables(args)` — walks `knowledge/concept_research/` filtering `^\d+[a-z]?-`; reports missing/extra rows in `ontology.csv` and `archetype_fit.csv` (strict fail); summarizes `design_point.csv` and `design_point_freeform_routes.md` coverage (warning-only)
- [ ] Add `cmd_regenerate_concept(args)` — resolves the record; refuses unless `is_costingfe_runnable(record)` with a state-specific reason (matches the design's subcommand-sequence diagram); on `--dry-run`, prints the stage sequence and writes a temp frontmatter; on real run, calls existing `cmd_gap_check` (unless `--keep-gap-report`), `cmd_analyze`, `cmd_model_setup`, `cmd_review`, `cmd_synthesize`, `cmd_score`, `cmd_approve` directly
- [ ] Add subparsers for the two new subcommands

#### 3. Final sweep
- [ ] `grep -rn 'Reuses' exploration/concept_analysis/scripts/lib/` → 0 live hits (comments noting the rename are acceptable)
- [ ] `grep -rn 'COSTINGFE_MAPPING\|FAMILY_KEY_MAP\|_is_freeform_architecture\|get_costingfe_mapping\|FUEL_MAPPING' exploration/concept_analysis/scripts/` → 0 hits

### Validation

**Automated:**
- [ ] All Phase 5 tests green
- [ ] Phases 1-4 tests still green
- [ ] `uv run python -m pytest exploration/concept_analysis/scripts/test_*.py -v` → all green (no regressions in scoring/heatmap test paths)
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py init-tables` → exit 0
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py regenerate-concept --dry-run 01-hts-compact-tokamak` → exit 0, prints stage sequence

**Manual:**
- [ ] Walk through every spec acceptance test in [`spec.md`](spec.md) — confirm each one is exercised by an automated test or a manual command above
- [ ] `regenerate-concept --dry-run` against one pending concept (e.g. `05`) and one None-grade concept (e.g. `02`) — confirm state-specific refusal messages
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py list` — runs unchanged (record-shaped input, legacy aliases let it work)
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py score --help` (or a real `score` invocation if cheap) — confirms the scoring handlers received legacy-table input as designed

**What we know works:** Every spec acceptance test passes. CLI is end-to-end runnable. The C2 dispatch split is verified by scoring/heatmap tests remaining green.

---

## Environment Setup

**See [CLAUDE.md](../../../CLAUDE.md)** — always `uv run python`, never bare `python`. Test runner is `uv run python -m pytest`.

## Risk Management

**See [`design.md#potential-risks`](design.md#potential-risks)** for the full risk catalog.

**Phase-specific mitigations** (in addition to the design's):
- **Phase 1:** If `parse_frontmatter` fails the round-trip test, fix the parser first — do not work around with flow-list emission. The parser is shared infrastructure and fixing it once is cheaper than special-casing emit/consume sites later.
- **Phase 2:** The `get_model_path` ↔ `is_costingfe_runnable` disagreement test is the regression pin. Any future refactor that "simplifies by unifying" will trip it; do not delete the test without re-opening Bet 2.
- **Phase 3:** The compile-removal forces Phases 4-5 to consume the new contract — but if any unaudited consumer of `COSTINGFE_MAPPING` exists outside `loop.py` / `run_analysis.py`, Phase 3 breaks it. Mitigation: the grep check at the end of Phase 3 quarantines.
- **Phase 4:** `loop.py` is the highest-blast-radius file. Run the *existing* loop tests after the change (not just new tests) — that's the regression net.
- **Phase 5:** The C2 scoring-corruption class is silent (empty strings, not exceptions). The Phase 5 test that asserts `r01.get("Fuel")` is non-empty after dispatch is the regression pin — if a future refactor pipes records into scoring, this test catches the silent zeroing.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION — leave empty now]

### Phase 1 Completion
**Completed:** 2026-05-31
**Actual Changes:**
- Added table-path constants to `lib/paths.py`: `TABLES_DIR`, `ONTOLOGY_PATH`, `ARCHETYPE_FIT_PATH`, `COMPARABLES_PATH`, `DESIGN_POINT_PATH`, `FREEFORM_ROUTES_PATH`.
- `lib/concepts.py`: renamed `load_table` → `load_legacy_table` (added "residual fields only — do not extend" docstring); added `_LEGACY_ALIAS_MAP`, `_read_csv_by_id`, `_split_comparables`, `load_freeform_routes()`, `_build_record()`, `load_concepts()`. Old routing surface (`COSTINGFE_MAPPING` etc.) left intact per phasing.
- `run_analysis.py`: import + call site updated `load_table` → `load_legacy_table` (line 51, 1527) to keep the module compiling between phases.
- `test_concepts_v2.py` (NEW): 8 Phase-1 tests (parser round-trip, join, empty-comparables, pending vs. freeform, missing-file graceful, freeform-routes parsing, legacy-table topology columns).

**Issues:**
- `design_point.csv` actually has **4** rows now (01/06/08/14), not the 3 (01/08/14) the plan assumed. `06-magnetic-mirror` is `fit_grade=Low` + `grounding=low` → a *real* `costingfe-asterisked` fixture (used in later phases instead of relying solely on synthetic rows).

**Deviations:**
- `confinement_family` alias for concepts 16/38 is now `OTHER` (ontology) vs. legacy `Non-Standard`. Affects only `--family` filter labels for those two; arguably more correct. Noted, not blocking.
- Performed the `load_legacy_table` rename's caller update in `run_analysis.py` during Phase 1 (rather than deferring) so each phase stays independently green — Phase 5 reworks that call site for the dispatch split anyway.

### Phase 2 Completion
**Completed:** 2026-05-31
**Actual Changes:**
- `lib/concepts.py`: replaced `get_model_path(concept)` body in place with the fit-grade-only version (`costingfe` iff `fit_grade != "None"`); added `get_comparison_status(record)` (four-state) and `is_costingfe_runnable(record)` (strict gate, delegates to `get_comparison_status`). `_is_freeform_architecture` is now unused (Phase 3 deletes it); `get_costingfe_mapping`/`_get_subcategory`/`FAMILY_KEY_MAP`/`COSTINGFE_MAPPING` stay (loop still uses them until Phase 4).
- `test_concepts_v2.py`: added `_rec()` helper + 6 Phase-2 tests including the C1 disagreement pin and real-record four-state checks (using 06 as a real `costingfe-asterisked` fixture).

**Issues:**
- Replacing `get_model_path` semantics is **not** caller-free: `loop.py:712` calls it. The shared loop test fixture (`_fake_claude.ConceptFixture.concept`) had no `fit_grade`, so it newly routed to `costingfe` → `get_costingfe_mapping` ValueError, breaking 5 loop tests (3 staleness + 2 external-feedback). Fixed in lock-step by adding `fit_grade: "None"` to the fixture (restores its prior freeform routing under the new contract). This is the spec's "existing tests updated where they assert old routing" case.

**Deviations:**
- The plan framed Phase 2 predicates as "pure functions, no callers yet." `get_model_path` is actually a pre-existing function with a live caller (`loop.py`); its in-place replacement is what forced the fixture update above. No design change — just a more honest accounting than "no callers."
- **Environment note:** `design_point.csv` is being actively appended by a background proposal batch (rows for 06/11/… landed mid-implementation). Tests that touch real records derive expectations from current table membership rather than hardcoding, to stay robust against the moving table. A non-atomic rewrite by that batch can momentarily make the CSV absent — a transient external race, not a code defect.

### Phase 3 Completion
**Completed:** 2026-05-31
**Actual Changes:**
- `lib/frontmatter.py`: rewrote `make_frontmatter(record)` to emit the orchestrator-owned block (Confinement-Family, Archetype, Archetype-Fit, Comparison-Status, block-list Comparables or `[]`, and the four Design-Point fields only when a DP row exists). Reads canonical keys with legacy-alias fallback. Added `from lib.concepts import get_comparison_status` (no circular import — concepts doesn't import frontmatter).
- `lib/concepts.py`: deleted `_is_freeform_architecture` (zero callers since Phase 2); added `ENUM_LIBRARY_HINTS` (4 entries: TOKAMAK/STELLARATOR/MIRROR/PULSED_FRC) + `_DEFAULT_LIBRARY_HINT` + `get_costingfe_library_hints(record)`; imported `COSTINGFE_EXAMPLES_DIR`.
- `test_concepts_v2.py`: +5 Phase-3 tests (golden 01, pending omits DP fields, none-grade degradation, parser round-trip, hint assembly for 01/08).

**Issues:**
- None. (`dt_stellarator.py` now exists in the 1costingFE examples dir, so STELLARATOR gets a real example instead of the old "tokamak is closest" fallback — a small improvement over the retired map.)

**Deviations:**
- **Re-sequenced the deletions** rather than deleting the whole old routing surface in Phase 3 (the plan's "compile-error forcing function"). `get_costingfe_mapping`/`_get_subcategory`/`FUEL_MAPPING` still have a live caller (`loop.py`) and `COSTINGFE_MAPPING`/`FAMILY_KEY_MAP` are still imported by `run_analysis.py`, so deleting them now would red the suite. Instead each symbol is deleted in the phase that removes its last caller (loop → Phase 4; run_analysis import → Phase 5). Identical end state, but every phase stays green — better fit for "stop on failure" than intentional interim breakage.

### Phase 4 Completion
**Completed:** 2026-05-31
**Actual Changes:**
- `lib/loop.py`: import line → `get_costingfe_library_hints, get_model_path` (dropped `get_costingfe_mapping`, `FUEL_MAPPING`); costingfe `vars_dict` now uses `hints["example_path"/"costingfe_concept"/"costingfe_fuel"]` with `defaults_path=""` and `mapping_notes=""` placeholders (hazard A); removed now-unused `COSTINGFE_DEFAULTS_DIR`/`COSTINGFE_EXAMPLES_DIR` imports; updated the line-442 "Reuses" comment to the orchestrator-owned-fields note.
- `lib/concepts.py`: deleted `FUEL_MAPPING`, `get_costingfe_mapping`, `_get_subcategory` (loop was their last caller). `COSTINGFE_MAPPING`/`FAMILY_KEY_MAP` remain (run_analysis still imports them → Phase 5).
- `prompt_templates/analysis_v2.md`: replaced the "Step 2: Update Reuses" paragraph with a "frontmatter is orchestrator-owned — do not edit it" note (hazard B). 0 `Reuses` hits remain in the template.
- `lib/landscape.py`: made `build_concept_landscape` record-safe — excluded ConceptRecord canonical/structural keys from the landscape columns and `str()`-coerced cell values, so it renders the legacy display aliases without crashing on `comparables`(list)/`design_point`(dict). (Pre-emptive: cmd_analyze receives records in Phase 5.)
- `test_concepts_v2.py`: +3 Phase-4 tests (frontmatter call-site round-trip, costingfe vars with placeholders, prompt has no Edit-Reuses step). Verified `model_setup_costingfe.md` renders with the placeholder vars — no unresolved `{{...}}`.

**Issues:**
- The shared loop fixture already carried `fit_grade: "None"` (added in Phase 2), so it routes freeform and `make_frontmatter(fixture)` works via alias fallback — no further fixture change needed for the new emitter.

**Deviations:**
- Kept loop.py's local variable name `concept` (the plan suggested renaming to `record`). It's a record at runtime once Phase 5 wires it; renaming the parameter cascades through many call sites for zero behavior change, so I left it and relied on `make_frontmatter`'s canonical-with-alias-fallback reads. Noted for clarity.
- Folded the `build_concept_landscape` record-safety fix in here (the Phase-4 task) rather than Phase 5; it's independent of the dispatch flip and harmless to land early.
- Only remaining `Reuses` token in `lib/` is a docstring rename-note in `frontmatter.py` — explicitly allowed by the spec ("comments noting the rename are acceptable").

### Phase 5 Completion
**Completed:** 2026-05-31
**Actual Changes:**
- `run_analysis.py`: removed `COSTINGFE_MAPPING`/`FAMILY_KEY_MAP` imports; added `get_comparison_status`, `is_costingfe_runnable`, `load_concepts`, `load_freeform_routes` + the table-path constants; added `import tempfile`. Added `_csv_ids`, `_disk_concept_ids`, `_validate_tables`, `_freeform_from`, `cmd_init_tables`, `_regen_refusal_reason`, `_regen_namespace`, `cmd_regenerate_concept`. Added `init-tables` and `regenerate-concept` subparsers. Rewrote `main()` with the loader dispatch split (`LEGACY_TABLE_COMMANDS = {score, calibrate, extract-scores, heatmap}` → `load_legacy_table()`; everything else → `load_concepts()`).
- `lib/concepts.py`: deleted `COSTINGFE_MAPPING` and `FAMILY_KEY_MAP` (last importer removed).
- `test_concepts_v2.py`: +9 Phase-5 tests (dispatch-split C2 pin, init-tables pass + two failure modes via in-process `_validate_tables`, regenerate dry-run runnable, keep-gap-report skip, three state-specific refusals).

**Verification (spec acceptance tests):** all exercised — `get_model_path` fit-grade-only + four-state computation (`test_get_model_path_*`, `test_four_state_*`); `make_frontmatter` full/pending/none (`test_make_frontmatter_*`); `init-tables` pass/fail (`test_init_tables_*` + live CLI exit 0); `regenerate-concept` dry-run + state-specific refusals (`test_regenerate_concept_*` + live CLI); dispatch split (`test_dispatch_split_*`); no live `Reuses` in `lib/`; full suite green (**289 passed, 5 skipped**).

**Issues:**
- `init-tables` reports design-point coverage as warning-only (5/36 mappable have rows today; 31 pending; 0 judged-freeform) and exits 0 — correct mid-batch behavior per FR-5/Bet 5.

**Deviations:**
- **Kept the `make_frontmatter` import in `run_analysis.py`** (plan said remove it as stale). It is no longer stale: `regenerate-concept --dry-run` calls it to write a temp frontmatter as the end-to-end wiring check. Removing it would force a duplicate/shell-out.
- The real (non-dry-run) `regenerate-concept` path is implemented (rm of prior artifacts + direct `cmd_*` sequencing via a constructed Namespace) but is **not unit-tested** — a real run needs LLMs and valid Item 7/8 outputs (the spec's dry-run boundary). It is genuine sequencing code, not a stub.
- `init-tables` failure modes are tested in-process via `_validate_tables(...)` with a synthetic fixture rather than `subprocess`+`monkeypatch` (which don't compose across the process boundary); the happy path uses the real CLI subprocess. Same coverage, deterministic.

---

**Status:** Draft → In Progress → **Complete** (2026-05-31 — all 5 phases landed; 289 passed / 5 skipped)
