# Implementation Plan: `model_critic` Standalone Tool

**Status:** Draft
**Created:** 2026-05-31
**Last Updated:** 2026-05-31

## Source Documents

- **Spec:** [`./spec.md`](./spec.md)
- **Design:** [`./design.md`](./design.md) ← architecture, component shapes, key decisions, invariants, risks all live here

## Implementation Strategy

**Phasing Rationale:** Extract the shared classifier first (lowest-risk, unblocks downstream refusal logic and isolates regen-regression failure mode). Then build the pure `critic_inputs` loader where the bulk of the test weight lives. Then stand up the orchestrator skeleton + prompt template behind `--dry-run` only — this is the prompt-iteration gate, the load-bearing piece per [`design.md#next-stage-handoff`](./design.md#next-stage-handoff). Add real Claude wiring + full tests once the prompt is stable. Close with archived-concept FR-2 acceptance.

**Critical Path:** Phase 1 (classifier) → Phase 2 (loader) → Phase 3 (prompt + dry-run) → Phase 4 (real call + tests) → Phase 5 (archived acceptance).

**First Proof Point:** `model-critic 01-arc-tokamak --dry-run` printing a rendered prompt with all four FR-6b deterministic-flag blocks present and FR-5's scope boundary visible on hand-read (end of Phase 3).

**Overall Validation Approach:** Each phase opens with tests; each phase ends with an explicit verification of what it proved. Manual hand-read gates exist for the prompt (Phase 3) and the Claude output (Phase 4) because LLM acuity can't be unit-tested.

---

## Phase 1: Shared `Runnability` classifier extraction

### Goal

Lift `_regen_refusal_reason`'s four-state branches into a shared `lib/concepts.Runnability` enum + `runnability(record) -> Runnability` function; rewire `cmd_regenerate_concept` to dispatch on the enum, preserving its existing refusal copy verbatim. See [`design.md#component-overview`](./design.md#component-overview) (concepts.py extension) and [`design.md#key-bets--decisions`](./design.md#key-bets--decisions) (the "shared classifier, not shared message" decision).

### Assumption Under Test

Regen's existing behavior survives the enum-dispatch extraction unchanged — no copy drift, no edge-case regression in the four-state logic.

### Test Stencil (Write This First)

```python
# scripts/test_runnability.py  (new)

def test_runnability_costingfe_runnable(make_record):
    rec = make_record(fit_grade="High", design_point={"p_native_mwe": 233})
    assert runnability(rec) is Runnability.RUNNABLE

def test_runnability_freeform_deferred_by_fit_grade(make_record):
    rec = make_record(fit_grade="None")
    assert runnability(rec) is Runnability.FREEFORM_DEFERRED

def test_runnability_freeform_deferred_by_routes(make_record):
    rec = make_record(fit_grade="High", in_freeform_routes=True, design_point=None)
    assert runnability(rec) is Runnability.FREEFORM_DEFERRED

def test_runnability_pending_design_point(make_record):
    rec = make_record(fit_grade="High", in_freeform_routes=False, design_point=None)
    assert runnability(rec) is Runnability.PENDING_DESIGN_POINT
```

### Changes Required

**See `design.md` for:** [Component Overview — `scripts/lib/concepts.py` extension](./design.md#component-overview); [Key Bets & Decisions — shared classifier](./design.md#key-bets--decisions).

- [ ] `scripts/test_runnability.py` (NEW) — implement stencil + cover all four enum values from `get_comparison_status`.
- [ ] `scripts/lib/concepts.py` — add `Runnability` enum (4 values: `RUNNABLE`, `FREEFORM_DEFERRED`, `PENDING_DESIGN_POINT`, `NOT_COSTINGFE`) and `runnability(record) -> Runnability`. Implementation thinly wraps `get_comparison_status`; no new logic.
- [ ] `scripts/run_analysis.py:1521` (`_regen_refusal_reason`) — rewrite as a one-line `match`/`if-elif` dispatch on `runnability(record)`, mapping each enum value to regen's existing refusal phrasing **verbatim**. Do not change message strings.

### Validation

**Automated:**
- [ ] `uv run python -m pytest exploration/concept_analysis/scripts/test_runnability.py -v` → all pass
- [ ] `uv run python -m pytest exploration/concept_analysis/scripts/ -v` → no regressions (regen tests in particular must still pass with identical refusal messages)

**Manual:**
- [ ] Run `uv run python exploration/concept_analysis/scripts/run_analysis.py regenerate-concept <some-freeform-cid> --dry-run` → confirm stderr message is identical to pre-change behavior (capture before/after).

**What We Know Works After This Phase:** The four-state classifier is callable from anywhere; regen still works; `cmd_model_critic` has its refusal predicate ready to consume in Phase 3.

---

## Phase 2: `critic_inputs` loader + `format_check_block`

### Goal

Build the pure I/O + check-orchestration module. `collect(record) -> CriticInputs` populates all fields; `format_check_block(name, result) -> str` renders the one canonical block shape. See [`design.md#component-overview`](./design.md#component-overview) (critic_inputs.py), [`design.md#implementation-notes`](./design.md#implementation-notes) (CriticInputs dataclass, flag block format, live-import mechanism, drift threshold).

### Assumption Under Test

All four FR-6b checks can be invoked uniformly against real artifacts and produce consistent serialization regardless of underlying type (`ValidationResult` vs. dict) or runtime failure (raised exception, import failure, missing input).

### Test Stencil (Write This First)

```python
# scripts/test_critic_inputs.py  (new)

def test_collect_happy_path(record_01_arc):
    inputs = collect(record_01_arc)
    assert inputs.import_status == "imported OK"
    assert inputs.live_result_1gw is not None
    assert isinstance(inputs.enabled_count, int)
    assert inputs.dpc.valid is True            # 3-leg coherence holds for 01
    assert inputs.drift_flag is None           # no drift expected for active concept

def test_collect_broken_model_setup_falls_back(record_with_broken_setup):
    inputs = collect(record_with_broken_setup)
    assert "SyntaxError" in inputs.import_status
    assert inputs.live_result_1gw is None
    assert inputs.enabled_count is None
    assert inputs.contract.valid is False      # validator catches the SyntaxError leg

def test_collect_drift_flag_fires_above_threshold(record_with_stale_output):
    inputs = collect(record_with_stale_output)
    assert inputs.drift_flag is not None
    assert "2%" in inputs.drift_flag or "drift" in inputs.drift_flag.lower()

def test_format_check_block_uniform_shape_validation_result(passing_vr):
    block = format_check_block("dpc", passing_vr)
    assert block.startswith("### dpc")
    assert "status: ok" in block

def test_format_check_block_uniform_shape_sanity_dict_with_error(sanity_error_dict):
    block = format_check_block("sanity", sanity_error_dict)
    assert "status: error" in block
```

### Changes Required

**See `design.md` for:** [CriticInputs dataclass fields](./design.md#implementation-notes); [Flag block format](./design.md#implementation-notes); [Live-import mechanism](./design.md#implementation-notes); [Drift threshold (2%, exposed as `DRIFT_THRESHOLD`)](./design.md#implementation-notes); [Invariant 3 — uniform check-result serialization](./design.md#required-invariants).

- [ ] `scripts/test_critic_inputs.py` (NEW) — implement stencil. Add fixtures for: real `01-arc-tokamak` record, synthetic concept dir with broken `model_setup.py`, synthetic concept dir whose `model_output.txt` reports an LCOE diverging >2% from a stubbed live `result_1gw.lcoe`.
- [ ] `scripts/lib/critic_inputs.py` (NEW):
  - [ ] `CriticInputs` dataclass — fields per [design.md Implementation Notes](./design.md#implementation-notes).
  - [ ] `DRIFT_THRESHOLD = 0.02` module constant.
  - [ ] `format_check_block(name, result) -> str` — the single owner of the block format string.
  - [ ] `_normalize_check(name, callable, *args, **kwargs) -> ValidationResult | dict` — invokes a check, replaces raised exception with synthetic `ValidationResult(valid=False, …, details="check raised: <type>")` per [design.md Invariant 3](./design.md#required-invariants).
  - [ ] `_try_import(model_setup_path) -> (module | None, import_status_str)` — `importlib.util` + broad `except Exception` per [design.md Implementation Notes — live-import mechanism](./design.md#implementation-notes).
  - [ ] `_parse_static_lcoe(model_output_txt) -> float | None` — extracts headline LCOE for drift comparison.
  - [ ] `_detect_drift(live_lcoe, static_lcoe) -> str | None` — returns drift-flag text when `abs(live-static)/static > DRIFT_THRESHOLD`.
  - [ ] `collect(record) -> CriticInputs` — orchestrates the above. Sources `enabled_count` via `len(model_setup_helpers.enabled_overrides(module.overrides))` on live-import success, `None` otherwise.

### Validation

**Automated:**
- [ ] `uv run python -m pytest exploration/concept_analysis/scripts/test_critic_inputs.py -v` → all pass
- [ ] `uv run python -m pytest exploration/concept_analysis/scripts/ -v` → no regressions

**Manual:**
- [ ] One-off REPL: `from lib.critic_inputs import collect; from lib.concepts import load_concepts; rec = next(r for r in load_concepts() if r["concept_id"]=="01-arc-tokamak"); inputs = collect(rec)` → inspect every field is populated; print `format_check_block("dpc", inputs.dpc)` and confirm it renders the documented shape.

**What We Know Works After This Phase:** All bundle inputs assemble from a real concept dir with correct values; the format helper produces the contracted block shape; edge cases (broken import, drift, raised exception) are deterministic.

---

## Phase 3: Orchestrator skeleton + prompt template + `--dry-run` prompt iteration

### Goal

Wire `cmd_model_critic` up through `--dry-run` only (no Claude call yet). Draft `prompt_templates/model_critic.md` per spec FR-5 (artifact-vs-source boundary, selection-as-fixed-input) and FR-6b (reason-on-top-of-flags). Render against `01-arc-tokamak`, hand-inspect, iterate. See [`design.md#next-stage-handoff`](./design.md#next-stage-handoff) for the "de-risk first" directive.

### Assumption Under Test

The reshaped prompt actually directs the LLM at judgment-on-top-of-flags rather than re-derivation, and respects the artifact-vs-source scope boundary that Phase 0's draft violated. Verifiable by reading the rendered prompt text.

### Test Stencil (Write This First)

```python
# scripts/test_model_critic.py  (new — Phase 3 portion)

def test_dry_run_prints_rendered_prompt_with_all_flag_blocks(capsys, record_01_arc):
    rc = run(record_01_arc, model=None, timeout=900, dry_run=True, now=fixed_now())
    out = capsys.readouterr().out
    assert rc == 0
    for block in ("### dpc", "### contract", "### count_smell", "### sanity"):
        assert block in out
    # No file written under analyses/01-arc-tokamak/
    assert not any(p.name.startswith("critic_review_") for p in concept_dir("01-arc-tokamak").iterdir())

def test_dry_run_refusal_freeform(record_freeform):
    rc = run(record_freeform, dry_run=True)
    assert rc != 0  # refusal exit; distinct message asserted via capsys.err
```

### Changes Required

**See `design.md` for:** [Architecture diagram](./design.md#architecture); [Component Overview — orchestrator, prompt template, run_analysis extension](./design.md#component-overview); [Implementation Notes — prompt template variables, `--dry-run` semantics](./design.md#implementation-notes); spec [§Reshape Obligations](./spec.md) (FR-5 a/b) and spec FR-6b.

- [ ] `scripts/test_model_critic.py` (NEW — Phase 3 portion only) — implement dry-run stencil + freeform refusal test.
- [ ] `prompt_templates/model_critic.md` (NEW) — draft per spec FR-5 and FR-6b. Uses the variable set documented in [design.md Implementation Notes](./design.md#implementation-notes): `{{concept_id}}`, `{{fit_grade}}`, `{{comparables}}`, `{{design_point_block}}`, `{{analysis_md}}`, `{{model_setup_py}}`, `{{model_output_txt}}`, `{{deterministic_flags}}`, `{{import_status}}`. Headline output structure from Phase 0 prototype prompt preserved.
- [ ] `scripts/agents/model_critic.py` (NEW — skeleton):
  - [ ] `run(record, *, model, timeout, dry_run, now) -> int` signature per [design.md Architecture](./design.md#architecture).
  - [ ] `--dry-run` branch: call `critic_inputs.collect`, render template via `templating.fill_template`, print to stdout, return 0.
  - [ ] Non-dry-run branch: stub `raise NotImplementedError("Phase 4")` for now.
  - [ ] Refusal branch: `runnability(record)` dispatch with critic-specific copy for `FREEFORM_DEFERRED` and `PENDING_DESIGN_POINT` (distinct messages per spec FR-7).
- [ ] `scripts/run_analysis.py` — add `cmd_model_critic(records, args)` + `model-critic` subparser (single positional `concept`, `--model`, `--timeout`, `--dry-run`). Pattern mirrors `cmd_regenerate_concept` at `run_analysis.py:1548`.

### Validation

**Automated:**
- [ ] `uv run python -m pytest exploration/concept_analysis/scripts/test_model_critic.py -v` → Phase 3 tests pass
- [ ] `uv run python -m pytest exploration/concept_analysis/scripts/ -v` → no regressions

**Manual (the prompt de-risk gate):**
- [ ] Run `uv run python exploration/concept_analysis/scripts/run_analysis.py model-critic 01-arc-tokamak --dry-run > /tmp/critic_prompt.md`
- [ ] Hand-read `/tmp/critic_prompt.md` against these checks:
  - All four FR-6b blocks present (`### dpc`, `### contract`, `### count_smell`, `### sanity`), each with `status` / `summary` / `detail` lines.
  - Design Point block contains the table-row plant name + `P_native` as a fixed input.
  - Prompt prose explicitly tells the agent NOT to second-guess source selection (FR-5a scope boundary).
  - Prompt prose explicitly tells the agent NOT to re-debate plant selection (FR-5b).
  - Prompt prose explicitly directs the agent to interpret fired flags, not re-derive them.
- [ ] If any of the above is weak: iterate prompt prose (cap iteration at ~3 cycles per [Phase Strategy risks](#risks-phase-specific)); re-render; re-read.
- [ ] Run `model-critic <some-freeform-cid> --dry-run` → confirm refusal message is critic-specific and distinct from regen's wording.
- [ ] Run `model-critic <some-pending-cid> --dry-run` → confirm distinct refusal message vs freeform case.

**What We Know Works After This Phase:** The rendered prompt is on track to satisfy spec FR-5 + FR-6b; refusal paths emit distinct messages; the orchestrator scaffold is ready to be filled in.

---

## Phase 4: Real Claude call + atomic write + full orchestrator tests

### Goal

Wire `invoke_claude`, atomic-write versioned output, mocked-Claude tests for all happy and error paths. Make one real Claude call against `01-arc-tokamak`, hand-read output, compare to Phase 0 prototype review for substance. See [`design.md#architecture`](./design.md#architecture) (steps 3–4), [`design.md#required-invariants`](./design.md#required-invariants) (Invariants 2, 5).

### Assumption Under Test

Acuity is preserved or improved against the Phase 0 baseline now that the deterministic flags backstop the LLM. The structural plumbing (atomic write, versioned filename, error-path zero-write) holds under all branches.

### Test Stencil (Write This First)

```python
# scripts/test_model_critic.py  (extension)

def test_real_invocation_writes_versioned_file(record_01_arc, mock_invoke_claude, tmp_concept_dir):
    mock_invoke_claude.return_value = InvokeResult("# stub review\nbody", "", 0)
    rc = run(record_01_arc, model="sonnet", timeout=900, dry_run=False, now=lambda: "20260601-120000")
    assert rc == 0
    assert (tmp_concept_dir / "critic_review_20260601-120000.md").exists()

def test_claude_failure_writes_no_file(record_01_arc, mock_invoke_claude, tmp_concept_dir):
    mock_invoke_claude.return_value = InvokeResult("", "boom", 1)
    rc = run(record_01_arc, dry_run=False, now=lambda: "20260601-120000")
    assert rc != 0
    assert not (tmp_concept_dir / "critic_review_20260601-120000.md").exists()

def test_rerun_preserves_prior_reviews(record_01_arc, mock_invoke_claude, tmp_concept_dir):
    mock_invoke_claude.return_value = InvokeResult("# review A", "", 0)
    run(record_01_arc, dry_run=False, now=lambda: "20260601-120000")
    mock_invoke_claude.return_value = InvokeResult("# review B", "", 0)
    run(record_01_arc, dry_run=False, now=lambda: "20260601-130000")
    files = sorted(p.name for p in tmp_concept_dir.glob("critic_review_*.md"))
    assert files == ["critic_review_20260601-120000.md", "critic_review_20260601-130000.md"]
```

### Changes Required

**See `design.md` for:** [Architecture steps 3–4](./design.md#architecture); [Invariants 2, 5, 6](./design.md#required-invariants); [Implementation Notes — atomic write](./design.md#implementation-notes); spec [Acceptance Criteria](./spec.md).

- [ ] `scripts/test_model_critic.py` — extend with the three stencils above + tests for: missing concept dir (hard error), distinct refusal messages on each non-runnable state (FR-7), and verifying `{{deterministic_flags}}` injection survives end-to-end.
- [ ] `scripts/agents/model_critic.py` — replace Phase 3's `NotImplementedError` stub:
  - [ ] Call `claude.invoke_claude(prompt, cwd, model, timeout)`.
  - [ ] On `result.returncode == 0` and non-empty stdout: atomic write via tempfile + `os.replace` to `analyses/<cid>/critic_review_<now()>.md`.
  - [ ] On any failure path (rc≠0, empty stdout): return non-zero exit, write nothing, surface stderr.
- [ ] Hand-acceptance: run `uv run python exploration/concept_analysis/scripts/run_analysis.py model-critic 01-arc-tokamak --model sonnet` → one real Claude call. Read the output file; compare to `.project/active/concept-rework-prototype/artifacts/critic_review.md`. Substance should be preserved or improved; structural shape will differ (flags now pre-computed).

### Validation

**Automated:**
- [ ] `uv run python -m pytest exploration/concept_analysis/scripts/test_model_critic.py -v` → all pass
- [ ] `uv run python -m pytest exploration/concept_analysis/scripts/ -v` → no regressions
- [ ] Spec acceptance criteria 1, 3, 4, 5, 6, 7, 8 (the automatable ones) verified by test names.

**Manual (the acuity gate):**
- [ ] Read the real Claude output against `concept-rework-prototype/artifacts/critic_review.md`:
  - At least one substantive judgment-shaped issue surfaced (or explicit "I found nothing" per the prompt instruction).
  - No re-derivation of facts already in the deterministic-flag blocks.
  - No out-of-scope sourcing critiques (FR-5a scope boundary holds in actual output).
- [ ] Run `model-critic <some-freeform-cid>` (non-dry) → exits non-zero, no file written, refusal message printed.

**What We Know Works After This Phase:** The full critic runs end-to-end against an active concept; spec acceptance criteria 1–8 all pass; manual acuity gate cleared.

---

## Phase 5: Archived-concept simulation + close-out

### Goal

Simulate archival per spec FR-2 definition (delete `iter-*/` under a concept dir); re-invoke; verify equivalence. Confirm full project test suite green. Document acceptance.

### Assumption Under Test

"Archived" really is just absence of `iter-*/` — no hidden dependency on iteration state surfaces in the critic.

### Test Stencil (Write This First)

```python
# scripts/test_model_critic.py  (final extension)

def test_archived_concept_invocation_equivalent(record_01_arc, mock_invoke_claude, tmp_concept_dir):
    # Pre-condition: tmp_concept_dir contains analysis.md, model_setup.py,
    # model_output.txt, and at least one iter-*/ subdirectory.
    for iter_dir in tmp_concept_dir.glob("iter-*"):
        shutil.rmtree(iter_dir)
    mock_invoke_claude.return_value = InvokeResult("# archived review", "", 0)
    rc = run(record_01_arc, dry_run=False, now=lambda: "20260601-140000")
    assert rc == 0
    assert (tmp_concept_dir / "critic_review_20260601-140000.md").exists()
```

### Changes Required

**See `design.md` for:** [Invariant 1 — no loop-state dependency](./design.md#required-invariants); spec [FR-2 acceptance test](./spec.md).

- [ ] `scripts/test_model_critic.py` — add the archived-concept stencil.
- [ ] No source changes expected. If the test fails, that's signal that an undocumented `iter-*/` read exists in `critic_inputs` — fix it there.
- [ ] Hand-acceptance: pick a passing concept dir (e.g. the one from Phase 4), back up its `iter-*/` somewhere safe, delete the originals, run `model-critic <cid>` → equivalent output. Restore the iter dirs after.
- [ ] Update plan.md Implementation Notes with completion timestamps and any deviations.

### Validation

**Automated:**
- [ ] `uv run python -m pytest exploration/concept_analysis/scripts/test_model_critic.py -v` → archived-concept test passes
- [ ] `uv run python -m pytest exploration/concept_analysis/scripts/ -v` → entire suite green (regen + critic + all the rest)

**Manual:**
- [ ] Hand-acceptance per above (with iter backup/restore).
- [ ] Spec acceptance criterion checklist: walk every checkbox in `spec.md#acceptance-criteria` against actual behavior; any failures route back to the appropriate phase.

**What We Know Works After This Phase:** Spec FR-2 (archived-concept invocation) is acceptance-passed; the feature is shippable.

---

## Environment Setup

**See CLAUDE.md for full environment rules.** Key: use `uv run python …` and `uv run python -m pytest …`; never bare `python`/`pytest`. Tests live under `exploration/concept_analysis/scripts/test_*.py` — pattern-match existing test files for fixture conventions.

---

## Risk Management

**See [`design.md#potential-risks`](./design.md#potential-risks) for full risk analysis.**

**Phase-Specific Mitigations:**

- **Phase 1**: Copy drift on regen refusal messages — regen's existing tests are the regression net; map every enum value to existing phrasing verbatim, no rewording.
- **Phase 2**: Drift threshold (2%) might be wrong for real data — exposed as `DRIFT_THRESHOLD` constant; revisit after Phase 4's real run on `01-arc-tokamak`.
- **Phase 3**: Prompt iteration is open-ended — cap at ~3 hand-review cycles before moving on. If 3 cycles don't get the prompt clean, that's signal the FR-5/FR-6b reshape is harder than expected — surface it then; don't pre-budget.
- **Phase 4**: Acuity regression vs Phase 0 prototype is hard to detect automatically — manual hand-read against `concept-rework-prototype/artifacts/critic_review.md` is the explicit gate; if substance regressed, route back to Phase 3 prompt iteration.
- **Phase 5**: An undocumented `iter-*/` read would manifest here as a fixture failure — fix in `critic_inputs.py`, not by working around in the orchestrator.

---

## Implementation Notes

*TO BE FILLED DURING IMPLEMENTATION*

### Phase 1 Completion
**Completed:** 2026-05-31
**Actual Changes:**
- `scripts/lib/concepts.py` — added `Runnability` enum (4 values) + `runnability(record)` wrapper over `get_comparison_status`.
- `scripts/run_analysis.py` — imported `Runnability` + `runnability`; rewrote `_regen_refusal_reason` as an enum dispatch preserving every refusal string verbatim (incl. the `fit_grade == "None"` sub-branch inside `FREEFORM_DEFERRED`).
- `scripts/test_runnability.py` (NEW, 9 tests) — covers all four enum values + regen refusal copy preservation for all three non-runnable states + None-on-runnable.

**Issues:** Full-suite pytest shows 4 pre-existing `StopIteration` failures in `test_concepts_v2.py` (`test_load_concepts_pending_concept_has_no_design_point`, `test_four_state_on_real_records`, `test_make_frontmatter_pending_omits_design_point_fields`, `test_regenerate_concept_refuses_pending_with_reason`). All four fail because zero pending-design-point concepts exist in the current corpus (Item 5's batch completed). NOT caused by Phase 1 changes — confirmed by inspecting the test bodies (each does `next(... if design_point is None ...)`). Not in Phase 1 scope to fix.

**Deviations:** None. Regen `--dry-run` against `02-acoustic-icf-sonofusion` (freeform fit_grade=None) emits the verbatim pre-change message: `fit_grade=None — freeform, out of scope to model (Item 11)`.

### Phase 2 Completion
**Completed:** 2026-05-31
**Actual Changes:**
- `scripts/lib/critic_inputs.py` (NEW) — `CriticInputs` dataclass, `DRIFT_THRESHOLD=0.02`, `format_check_block` (single owner of block shape, dispatches on `ValidationResult` vs dict), `_try_import` (broad-Exception live import), `_parse_static_lcoe`, `_detect_drift`, `_normalize_check` (synthesizes failure VR on raised exceptions), and `collect(record, *, sanity_check=...)` orchestrator. `sanity_check` is dependency-injected to avoid a circular import on the top-level `sanity_check_comparables` module.
- `scripts/test_critic_inputs.py` (NEW, 12 tests) — covers happy path against real reference concept, broken-setup fallback, drift-flag firing, drift detection boundary cases, format_check_block uniform shape (4 result variants), unit tests for `_parse_static_lcoe` and `_detect_drift`.

**Issues:**
- Plan stencil references `01-arc-tokamak` but the real reference concept is `01-hts-compact-tokamak`; used the real ID. Noted as a stencil-text issue, not a content issue.
- Sanity-check integration: importing `sanity_check_comparables.sanity_check` at the top of `lib/critic_inputs.py` would create a partial circular-import risk because that module imports from `lib/*`. Resolved by making `sanity_check` an injected callable parameter to `collect`; the orchestrator (Phase 3) wires the real one in.
- `enabled_count`-cannot-be-computed case: `check_override_count_vs_fit_grade` requires an int, but we can't get one if the live import failed. Synthesized a `ValidationResult(valid=False, …, details="check raised: ImportFailure")` block in that case — keeps the prompt block shape uniform per Invariant 3.

**Deviations:** None.

### Phase 3 Completion
**Completed:** 2026-05-31 (pending hand-read gate)
**Actual Changes:**
- `prompt_templates/model_critic.md` (NEW) — productionized from the Phase 0 draft with the three structural reshapes: (a) FR-5a "What you ARE / are NOT reviewing" boundary up top, calling out source-quality and design-point-selection as out-of-scope; (b) FR-5b "Design Point is a fixed input from the upstream table; check coherence, do not re-debate" framing; (c) FR-6b "Deterministic checks have already fired — your job is judgment on top" section with per-check guidance on what *not* to re-derive and what kind of reasoning the flag should prompt instead. Reasoning spine re-pointed at the residual judgment surface; output-format template preserved from Phase 0.
- `scripts/agents/__init__.py` (NEW, empty) + `scripts/agents/model_critic.py` (NEW) — `run(record, *, model, timeout, dry_run, now)` orchestrator. Refusal copy lives in a tool-local `_REFUSAL_COPY` dict keyed on `Runnability`; freeform and pending get distinct, critic-specific messages (verified distinct from regen's wording by inspection). `_render_prompt` builds the variable bag including `_design_point_block` (renders the design_point.csv row) and `_deterministic_flags_block` (concatenates `format_check_block` calls plus optional drift block). Non-dry-run path raises `NotImplementedError("Phase 4")` per plan.
- `scripts/run_analysis.py` — `cmd_model_critic` + `model-critic` subparser added (single positional `concept`, `--model`, `--timeout`, `--dry-run`); dispatch entry registered.
- `scripts/test_model_critic.py` (NEW, 6 tests) — covers dry-run prompt content (all 4 flag blocks + FR-5a/FR-5b/FR-6b prose), no-file-written invariant, freeform refusal (distinct copy), Phase 4 stub raising NotImplementedError, end-to-end CLI dry-run, end-to-end CLI refusal.

**Issues:**
- **Stdout contamination bug found and fixed during the hand-read gate.** `model_setup.py` files run `print_cas_breakdown(...)` at module load, and `sanity_check_comparables.sanity_check` re-imports every comparable's `model_setup.py` for outlier stats. Both leaked CAS tables to stdout, contaminating the rendered-prompt output of `--dry-run`. Fixed in `lib/critic_inputs.py:_try_import` and in `collect()`'s sanity-check call by wrapping each in `contextlib.redirect_stdout(io.StringIO())` (and stderr for sanity_check, which prints WARN lines). Verified: dry-run now produces 754 lines starting with the prompt header, 0 bytes on stderr.
- **No pending-design-point concept exists in the corpus** (zero of them survived Item 5's batch). Could not run the planned `model-critic <some-pending-cid> --dry-run` hand-test. The unit tests still cover the refusal-copy distinction (via the enum keying in `_REFUSAL_COPY`); the CLI smoke test confirms refusals exit non-zero with the expected message text.

**Deviations:**
- Plan stencil references concept `01-arc-tokamak`; real ID is `01-hts-compact-tokamak`. Plan-stencil typo, not a deviation in behavior.

**Prompt iteration log:** 1 cycle. First-draft prompt rendered cleanly after the stdout-suppression bug fix; structurally satisfies FR-5a, FR-5b, FR-6b on hand-read. No prose iteration was needed (the cap was 3 cycles).

**Hand-read gate output:** `/tmp/critic_prompt.md` (754 lines). All four `### dpc / ### contract / ### count_smell / ### sanity` blocks present with canonical `status / summary / detail` shape; on the reference concept three are `ok` and `sanity` is `flagged` with 15 outlier accounts itemized. Design-Point block carries the named plant (`ARC 2015 Conservative Pilot phase (Sorbom et al.)`) and `p_native_mwe: 233` as a fixed input. Scope-boundary prose explicit at lines 13–15. "Reason on top" framing explicit at lines 17–28. **Hand-read gate PASSES from my side; user review required before Phase 4 wires the real Claude call.**

### Phase 4 Completion
**Completed:** 2026-05-31
**Actual Changes:**
- `scripts/agents/model_critic.py` — replaced `NotImplementedError` stub with full real-Claude path: missing-concept-dir guard (rc=2), `invoke_claude` call with cwd at the concept dir, failure handling (rc≠0 or empty stdout → no write, surface stderr), timestamp-versioned filename via the injectable `now` callable, atomic write via `_atomic_write` (tempfile in concept_dir + `os.replace` — POSIX-atomic). Imports: added `os`, `tempfile`, `lib.claude.invoke_claude`.
- `scripts/test_model_critic.py` — extended with 7 new tests: `tmp_analyses` fixture (repoints `ANALYSES_DIR` in both `lib/critic_inputs` and `agents/model_critic`); real_invocation writes versioned file; Claude failure writes no file; empty-stdout-with-rc=0 still writes no file; rerun preserves prior reviews; deterministic flags reach `invoke_claude` end-to-end (FR-6b plumbing); missing concept dir → rc=2 with no Claude call; pending refusal copy distinct from freeform (FR-7). All 12 model_critic tests pass.

**Issues:**
- First real call (default 900s timeout) hit the timeout limit. Retry with `--timeout 1800` completed in ~10 minutes (started 19:17, wrote at 19:27). Likely transient API slowness — not reproducible from the prompt size (67KB, well within sonnet's window). Cost ~$0.30-$0.50 estimated. The 15-minute default is too tight for this prompt under unfavorable conditions — operators should consider `--timeout 1800` as the practical default for `model-critic` calls.
- Full suite after Phase 4 wiring: 405 pass / 4 fail. The 4 failures are the same pre-existing `StopIteration` data-state issues from Phases 1-3 (zero pending-design-point concepts in corpus). No new regressions.

**Deviations:** None.

**Real Claude call output:** `exploration/concept_analysis/analyses/01-hts-compact-tokamak/critic_review_20260531-192707.md` (13.5KB, exit 0).

**Acuity comparison vs Phase 0:** **Substance preserved AND improved.** Phase 0 surfaced 4 headlines, 3 of which were mechanical issues the deterministic layer would have caught (P_native mismatch — now `dpc status: ok` because the artifact was fixed; provenance mislabeling — fixed; orphaned overrides — implicitly cleaned up). The new critic correctly does NOT regurgitate the fixed issues; the `dpc ok / contract ok / count_smell ok` blocks let it acknowledge the deterministic layer and skip past. The 3 new headlines are genuinely judgment-shaped — interpreting 15 sanity outliers as "3 independent signals + 12 derivative echoes" with a cross-account arithmetic catch on C220101 ($143.8M + $196.2M + $208.3M = $548M approaching median); identifying a label-confusion concern (Section 7's "native design point ≈ 199 $/MWh" reading as ARC's estimate when it's the library baseline); and re-prioritizing the gap inventory using the elasticity sensitivity output (−0.92 availability beats the magnet cost sensitivity in LCOE impact, deserves headline rather than buried-in-list treatment). FR-5a (no out-of-scope sourcing critique) and FR-5b (no design-point-selection re-debate) both explicitly honored in "What I deliberately did not say." The "reason on top of flags" framing of FR-6b produced exactly the upgrade in interpretive depth the spec bet on.

### Phase 5 Completion
**Completed:** —
**Actual Changes:** —
**Issues:** —
**Deviations:** —
**Spec acceptance walkthrough:** [link to checklist outcome]

---

**Status**: Draft
