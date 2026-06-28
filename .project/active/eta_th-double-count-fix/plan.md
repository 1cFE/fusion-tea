# Implementation Plan: eta_th / eta_de Double-Count Fix + Canonical Verification Layer

**Status:** Draft
**Created:** 2026-05-22 09:25 PDT
**Last Updated:** 2026-05-22 09:25 PDT

## Source Documents
- **Spec:** `.project/active/eta_th-double-count-fix/spec.md`
- **Design:** `.project/active/eta_th-double-count-fix/design.md` ← component details, architecture, decisions, risks
- **Issue:** [GitHub #30](https://github.com/1cFE/fusion-tea/issues/30)

## Implementation Strategy

**Phasing Rationale:** De-risk the two foundational uncertainties first (Phase 1), then build Layer 1 bottom-up (canonical API → enforcement script → applied propagation), then bolt on Layer 2 last with full regression. Test-first for every code-bearing phase.

**Critical Path:** Phase 1 audit → Phase 2 canonical_params → Phase 3 standardize_eta_th → Phase 4 apply/rerun/resynth → Phase 5 verifier + regression.

**First Proof Point:** Phase 1, concept-11 hand-calc. Plug `(eta_th=0.35, eta_de=0.54)` directly into a forward() call (bypassing standardization) and confirm LCOE moves from 95.4 to ~115-125 $/MWh per issue #30. If outside that band, pause and reread #30 before any code commits.

**Overall Validation Approach:**
- Each code-bearing phase starts with a test stencil
- Each phase has automated checks + manual verification + explicit "What We Know Works"
- Layer 1 is verified deterministically (unit + integration); Layer 2 is verified by schema conformance + smoke fixtures, not by exact-match diffs (LLM non-determinism)

---

## Phase 1: Pre-flight De-risk

### Goal
Collapse the two foundational uncertainties before writing any production code: (a) does the new canonical produce the expected LCOE shift, (b) does the planned regex split cover every kwarg spelling in the 39 `model_setup.py` files.

### Assumption Under Test
- The proposed `(0.35, 0.54)` for "hybrid (thermal + direct)" produces +15-30% LCOE on concept 11 vs current 95.4 $/MWh.
- The pattern anatomy in `design.md#component-overview` covers every `eta_th` / `eta_de` spelling actually used in `analyses/*/model_setup.py`.

### Test Stencil (Write This First)
No test code in this phase — investigation only. The "stencil" is the analytical procedure:

```
# Concept-11 hand-calc check
from costingfe import ConfinementConcept, CostModel, Fuel
model = CostModel(concept=ConfinementConcept.MIRROR, fuel=Fuel.DT)
shared = {<all kwargs from analyses/11-magnetic-mirror/model_setup.py>}
shared["eta_th"] = 0.35   # new canonical
shared["eta_de"] = 0.54   # unchanged
r = model.forward(net_electric_mw=500.0, **shared)
assert 115.0 <= float(r.costs.lcoe) <= 125.0, f"LCOE {r.costs.lcoe} outside expected band"
```

### Changes Required

**See `design.md` for:** the predicted LCOE band (`design.md#research-findings`, `design.md#potential-risks`) and the kwarg-spelling concerns (`design.md#implementation-notes`).

- [ ] **Kwarg-spelling audit:** `grep -nE "eta_th|ETA_TH|thermal_efficiency|eta_de|eta_dec|ETA_DE|ETA_DEC" exploration/concept_analysis/analyses/*/model_setup.py | sort -u`. Catalog every variant. Cross-check against the two patterns in `design.md#component-overview`.
- [ ] **`thermal_efficiency` semantic check:** for any file matching `thermal_efficiency`, read the surrounding comment block. Confirm it means cycle efficiency, not overall plant. Note any ambiguity.
- [ ] **Concept-11 LCOE hand-calc** (test stencil above). Run as a one-off `uv run python` script; do NOT commit the throwaway script.
- [ ] **Append findings to plan.md "Implementation Notes" section** below as `### Phase 1 Findings` — short bullet list: spelling variants found, any ambiguous aliases, concept-11 LCOE result.

### Validation

**Automated:** none (investigation phase).

**Manual:**
- [ ] Hand-calc LCOE lands in [115, 125] $/MWh band → proceed.
- [ ] Hand-calc lands outside band → stop, re-read #30, decide whether canonical values need adjustment before Phase 2.
- [ ] Audit findings note any kwarg-spelling surprises that require pattern changes.

**What We Know Works After This Phase:**
- The chosen canonical values produce the expected LCOE direction and magnitude.
- The regex patterns in `design.md` cover the real-world spelling distribution (or we've adjusted them).

---

## Phase 2: `canonical_params.py` refactor (test-first)

### Goal
Land the new tuple-shape canonical with full test coverage. API consumers downstream depend on this.

### Assumption Under Test
The `(eta_th, eta_de)` tuple shape + twin lookup functions compose cleanly and preserve the case/whitespace/parenthetical-stripping behavior of the current `canonical_eta_th()`.

### Test Stencil (Write This First)

```python
# tests/test_canonical_params.py
def test_canonical_efficiencies_tuple_shape():
    from lib.canonical_params import _CANONICAL_EFFICIENCIES
    for key, val in _CANONICAL_EFFICIENCIES.items():
        assert isinstance(val, tuple) and len(val) == 2
        assert 0.0 <= val[0] <= 1.0 and 0.0 <= val[1] <= 1.0

def test_canonical_eta_th_hybrid_returns_cycle_not_blended():
    from lib.canonical_params import canonical_eta_th, canonical_eta_de
    assert canonical_eta_th("Hybrid (thermal + direct)") == 0.35
    assert canonical_eta_de("Hybrid (thermal + direct)") == 0.54

def test_canonical_eta_th_direct_charged_particle_is_zero():
    from lib.canonical_params import canonical_eta_th, canonical_eta_de
    assert canonical_eta_th("Direct (charged particle)") == 0.0
    assert canonical_eta_de("Direct (charged particle)") == 0.70

def test_case_and_whitespace_normalization():
    from lib.canonical_params import canonical_eta_th
    assert canonical_eta_th("  HYBRID (thermal + direct)  ") == 0.35

def test_removed_keys_raise():
    from lib.canonical_params import canonical_eta_th
    import pytest
    with pytest.raises(ValueError):
        canonical_eta_th("Pulsed power implosion")
```

### Changes Required

**See `design.md` for:** the canonical map contents (`design.md#component-overview` → `canonical_params.py` section, including the illustrative interface snippet) and the keys to drop (`spec.md` FR-3).

- [ ] **Write failing tests** first in `exploration/concept_analysis/scripts/tests/test_canonical_params.py` (or extend existing if present — confirm during Phase 1 audit).
- [ ] **Refactor `exploration/concept_analysis/scripts/lib/canonical_params.py`:**
  - Replace `_CANONICAL_ETA_TH` with `_CANONICAL_EFFICIENCIES: dict[str, tuple[float, float]]` per `spec.md` FR-2.
  - Add private `_lookup(energy_capture) -> tuple[float, float]` that handles normalization + parenthetical fallback (lift from current `canonical_eta_th` logic).
  - Implement `canonical_eta_th(energy_capture) -> float` returning `_lookup(...)[0]`.
  - Implement `canonical_eta_de(energy_capture) -> float` returning `_lookup(...)[1]`.
  - Drop unused keys per `spec.md` FR-3.
  - Update the module docstring to reflect twin-axis canonical.
- [ ] **Leave `canonical_availability`, `canonical_mn`, `canonical_lifetime_yr` untouched.**

### Validation

**Automated:**
- [ ] `uv run pytest exploration/concept_analysis/scripts/tests/test_canonical_params.py -v` → all pass.
- [ ] `uv run pytest exploration/concept_analysis/` → no regressions in sibling tests.

**Manual:**
- [ ] Import sanity check: `uv run python -c "from lib.canonical_params import canonical_eta_th, canonical_eta_de; print(canonical_eta_th('Hybrid (thermal + direct)'), canonical_eta_de('Hybrid (thermal + direct)'))"` from `exploration/concept_analysis/scripts/`.

**What We Know Works After This Phase:**
- Canonical API is correct, well-tested, isolated. No downstream callers updated yet — `standardize_eta_th.py` still uses the old `canonical_eta_th` (still exists, same behavior on remaining keys). Existing scripts unaffected.

---

## Phase 3: `standardize_eta_th.py` two-pass refactor (test-first)

### Goal
Split the single regex into two independent passes (`eta_th` family + `eta_de` family), each writing its respective canonical, each respecting `# DEVIATION:` independently. Idempotent.

### Assumption Under Test
- Two patterns correctly partition the rewrite work — no double-stomp, no missed line.
- DEVIATION on one axis doesn't block standardization of the other.
- Running `--apply` twice on the same input produces a no-op second-run diff.

### Test Stencil (Write This First)

```python
# tests/test_standardize_eta_th.py
def test_two_pass_rewrites_both_axes(tmp_path):
    f = tmp_path / "model_setup.py"
    f.write_text("    eta_th=0.55,\n    eta_de=0.54,\n")
    # ... fixture concept registered as "Hybrid (thermal + direct)" ...
    apply_to_file(f, energy_capture="Hybrid (thermal + direct)")
    text = f.read_text()
    assert "eta_th=0.35" in text and "eta_de=0.54" in text

def test_deviation_on_eta_th_does_not_block_eta_de(tmp_path):
    f = tmp_path / "model_setup.py"
    f.write_text(
        "    eta_th=0.20,  # DEVIATION: physics-forced derating\n"
        "    eta_de=0.50,\n"
    )
    apply_to_file(f, energy_capture="Direct (charged particle)")
    text = f.read_text()
    assert "eta_th=0.20" in text  # unchanged
    assert "eta_de=0.70" in text  # standardized

def test_idempotence(tmp_path):
    # ... write file, apply once, capture diff; apply again; assert no further change
```

### Changes Required

**See `design.md` for:** the two-pattern structure (`design.md#component-overview` → `standardize_eta_th.py` section), invariants (`design.md#required-invariants`, esp. idempotence and DEVIATION independence), and gotchas (`design.md#implementation-notes`).

- [ ] **Write failing tests** in `exploration/concept_analysis/scripts/tests/test_standardize_eta_th.py`.
- [ ] **Refactor `exploration/concept_analysis/scripts/standardize_eta_th.py`:**
  - Define `ETA_TH_PATTERN` (matches `eta_th`/`ETA_TH`/`thermal_efficiency` + optional suffix).
  - Define `ETA_DE_PATTERN` (matches `eta_de`/`eta_dec`/`ETA_DE`/`ETA_DEC` + optional suffix). Must catch both `eta_de` and `eta_dec` spellings per Phase 1 audit.
  - Factor a `_apply_pass(pattern, canonical_value, model_path, energy_capture, axis_name) -> int` helper.
  - Main loop: for each file, run two passes; track rewrites per axis; report both columns.
  - DEVIATION check stays per-line (existing logic).
  - Suppress the `# standardized from X` annotation when the value is already canonical (idempotence).
- [ ] **Update CLI report format** to show both axes per concept (illustrative shape in `design.md#component-overview`).
- [ ] **Do NOT run `--apply` yet** — Phase 4.

### Validation

**Automated:**
- [ ] `uv run pytest exploration/concept_analysis/scripts/tests/test_standardize_eta_th.py -v` → all pass.
- [ ] **Dry-run sanity:** `uv run python exploration/concept_analysis/scripts/standardize_eta_th.py` (no `--apply`) → produces a report; eyeball: 8 affected concepts show deviation, others show match.

**Manual:**
- [ ] Read the dry-run report; confirm exactly the 8 expected concepts (06, 08, 11, 19, 23, 24, 31, 39) appear as deviations.
- [ ] Confirm concept 06 shows as DEVIATION on `eta_th` (existing `# DEVIATION:` annotation must be added in Phase 4 first — for now, expect 06 to show as deviation without DEVIATION protection).

**What We Know Works After This Phase:**
- The enforcement script is correct on fixture files and produces sensible dry-run output on real files. No real `model_setup.py` has been mutated.

---

## Phase 4: Apply + rerun + resynthesize + scoring_framework update

### Goal
Propagate the fix end-to-end: install concept-06 DEVIATION block, run `--apply` across all 39 files, regenerate `model_output.txt` for the 8 affected concepts, regenerate their `synthesis.md`, and replace the `scoring_framework.md` canonical table.

### Assumption Under Test
- Real-world LCOE deltas match the Phase 1 hand-calc within reason.
- Concept 06's DEVIATION block is respected by the new standardizer.
- Score Explorer renders correctly (no schema regression).
- No concept *other* than the 8 expected sees an LCOE shift.

### Test Stencil (Write This First)
No new test code in this phase — Phase 3's tests still hold. The "stencil" is the validation sequence below.

### Changes Required

**See `design.md` for:** the data flow (`design.md#architecture` data-flow paragraph), DEVIATION template (`design.md#implementation-notes`), and `scoring_framework.md` update scope (`design.md#component-overview`).

**Order matters:**

- [ ] **(a) Concept 06 DEVIATION block.** Manually edit `exploration/concept_analysis/analyses/06-magnetic-mirror/model_setup.py` `eta_th` line. Lift wording from `.project/research/feedback_eta_th/06-magnetic-mirror.md` F-1 "Recommendation 1." Comment shape per `design.md#implementation-notes`. Cite both `feedback_eta_th/06-magnetic-mirror.md` and `scoring_framework.md §"Justified deviations"`.
- [ ] **(b) Run standardization.** `uv run python exploration/concept_analysis/scripts/standardize_eta_th.py --apply`. Expect: 7 concepts modified (06 protected by DEVIATION), report shows both axes.
- [ ] **(c) Git status sanity.** `git diff --stat exploration/concept_analysis/analyses/` — exactly the expected files changed.
- [ ] **(d) Regenerate model_output.txt for the 8 affected.** `uv run python exploration/concept_analysis/scripts/rerun_all_models.py --only 06 08 11 19 23 24 31 39`.
- [ ] **(e) Regenerate synthesis.md for the 8 affected.** `uv run python exploration/concept_analysis/scripts/run_analysis.py synthesize --only 06 08 11 19 23 24 31 39 --force`.
- [ ] **(f) Update `exploration/concept_analysis/prompt_templates/config/scoring_framework.md`.** Replace the §"Thermal-to-electric conversion efficiency (η_th)" table with a new §"Energy capture efficiencies (η_th, η_de)" table listing both columns per Energy Capture key. Update the §"Helpers" code block to show `canonical_eta_de` alongside `canonical_eta_th`. Update the 06 deviation example to the new canonical `(0.0, 0.70)`.

### Validation

**Automated:**
- [ ] `uv run python exploration/concept_analysis/scripts/standardize_eta_th.py` (re-run, no `--apply`) → reports zero deviations (idempotence proof on real files).
- [ ] `grep -E "eta_th\s*=\s*0\.(55|70|85)" exploration/concept_analysis/analyses/*/model_setup.py` → matches only inside `# DEVIATION:` annotated lines (or no matches at all).
- [ ] `uv run pytest exploration/concept_analysis/` → no regressions.

**Manual:**
- [ ] For each of the 8 affected concepts: open `model_output.txt`, note the LCOE; open `synthesis.md`, confirm the synthesis LCOE matches. Cross-reference the LCOE delta vs the pre-fix state (use `git show HEAD:<path>` for the prior `model_output.txt`).
- [ ] Concept 11 specifically: confirm new LCOE lands in [115, 125] $/MWh band per Phase 1 hand-calc.
- [ ] Read concept 06's `model_setup.py` DEVIATION block — confirm wording, sources, axis label all clean.
- [ ] **Score Explorer regression check:** `uv run python -m http.server -d docs/ 8421` (or open https://score-explorer.1cf.energy/) + open in browser. Per `CLAUDE.md` use the `browser-inspect` skill: confirm Energy Capture column renders for all 39 concepts; confirm the 8 affected concepts show updated LCOE / composite scores; capture console errors.

**What We Know Works After This Phase:**
- The fix is fully applied and the 8 affected concepts produce LCOE matching costingfe's intended power-balance semantics.
- The framework documentation and the code agree.
- No regressions in Score Explorer or sibling concepts.

---

## Phase 5: Verifier + final regression sweep

### Goal
Build Layer 2 (`verify_canonical_params.py`) and run the full regression sweep.

### Assumption Under Test
- `claude -p` invoked via `lib/claude.py:invoke_claude()` produces JSON conforming to the schema we define.
- The drift report catches a synthetic concept-11-style narrative-vs-value contradiction on a fixture.
- The full project still works end-to-end after Phases 1-4.

### Test Stencil (Write This First)

```python
# tests/test_verify_canonical_params.py
def test_drift_report_flags_narrative_value_contradiction(tmp_path):
    # Fixture: eta_th=0.55 with comments describing 0.36 steam Rankine cycle
    f = tmp_path / "model_setup.py"
    f.write_text(<concept-11-pre-fix snippet>)
    report = verify_file(f, energy_capture="Hybrid (thermal + direct)")
    assert report["narrative_contradictions"], "expected drift flag"

def test_drift_report_passes_clean_file(tmp_path):
    f = tmp_path / "model_setup.py"
    f.write_text(<concept-11-post-fix snippet>)
    report = verify_file(f, energy_capture="Hybrid (thermal + direct)")
    assert not report["narrative_contradictions"]

def test_output_conforms_to_schema():
    schema = json.load(open("scripts/verify_output/schema.json"))
    report = verify_file(<any fixture>, energy_capture=...)
    jsonschema.validate(instance=report, schema=schema)
```

### Changes Required

**See `design.md` for:** the verifier architecture (`design.md#component-overview` → `verify_canonical_params.py` section), the prompt skeleton, output paths, and CLI flags.

- [ ] **Define output schema** `exploration/concept_analysis/scripts/verify_output/schema.json`. Fields per `design.md#component-overview`: `eta_th`, `eta_de`, `deviations[]`, `narrative_contradictions[]`, `missing_kwargs[]`, `confidence_notes[]`. Include `prompt_version` for reproducibility.
- [ ] **Write failing tests** in `exploration/concept_analysis/scripts/tests/test_verify_canonical_params.py`. Use real `claude -p` for at least one smoke test (network-dependent — mark with pytest marker if needed for CI later); unit-test the comparator with mocked LLM output.
- [ ] **Implement `exploration/concept_analysis/scripts/verify_canonical_params.py`:**
  - Reuse `lib/claude.py:invoke_claude()` per `design.md#research-findings`.
  - Templated prompt with `{ec}` and `{schema_path}` placeholders; keep prompt as a module-level constant; include `prompt_version` in output.
  - CLI: `--only`, `--model {sonnet,haiku}` (default sonnet), `--dry-run`, `--cost-cap`.
  - Read-only: never writes under `analyses/`. Outputs `verify_output/drift_report.json` and `verify_output/summary.md`.
- [ ] **Run verifier against all 39 concepts.** Review `verify_output/summary.md`; investigate any flagged drift. Hand-fix concept 11's surrounding narrative if it still disagrees with `eta_th=0.35` (the sourcing originally said 0.36; close to canonical now, but verifier may still flag).
- [ ] **Smoke test on pre-fix snapshot:** check out concept 11's old `model_setup.py` (`git show HEAD~N:<path>` for the appropriate commit), run verifier on it, confirm `narrative_contradictions` is non-empty. Smoke proof that the verifier earns its keep.
- [ ] **Update `.project/CURRENT_WORK.md`** removing #30 from "Open Issues" once verifier-clean.

### Validation

**Automated:**
- [ ] `uv run pytest exploration/concept_analysis/scripts/tests/test_verify_canonical_params.py -v` → all pass (mock unit tests; mark live smoke as `@pytest.mark.live`).
- [ ] Full project pytest: `uv run pytest exploration/` → no regressions.
- [ ] `jsonschema.validate(drift_report, schema)` passes.

**Manual:**
- [ ] Verifier run completes in under 10 minutes for 39 concepts (NFR-1).
- [ ] Verifier cost reported in summary; single-digit dollars (NFR-1).
- [ ] Pre-fix smoke confirms the verifier flags concept 11's narrative-vs-value contradiction.
- [ ] Post-fix run produces a clean drift report (or only minor/expected flags that have been triaged).

**What We Know Works After This Phase:**
- Both layers of the fix are in place. The bug from #30 is closed structurally (canonical shape + regex split) and semantically (LLM audit catches drift). Full regression clean. Ready for PR.

---

## Environment Setup

See `CLAUDE.md` for full environment rules. Key reminders:
- **Always use `uv run python …` / `uv run pytest …`.** Bare `python` will use the wrong venv.
- **`claude -p` stdout pattern:** pipe to file then read (per auto-memory `agentic-mbse Integration`). `lib/claude.py:invoke_claude` already handles this.
- **R2 sync:** not required for this work item (no concept research changes).

## Risk Management

See `design.md#potential-risks` for full risk analysis.

**Phase-specific mitigations:**

- **Phase 1:** Pre-flight may surface unknown kwarg spellings → fold findings into Phase 3 pattern design before code commits.
- **Phase 2:** API churn risk if `canonical_eta_th` callers elsewhere break → grep for callers before refactor; spec keeps the function name, only signature/behavior on dropped keys changes.
- **Phase 3:** Idempotence is easy to break with annotation logic → explicit `test_idempotence` in stencil. Verify in Phase 4 with re-run dry-run.
- **Phase 4:** Concept 11's narrative may still drift slightly from `eta_th=0.35` (sourcing says 0.36) → accept, let verifier flag in Phase 5, hand-fix narrative if flagged.
- **Phase 5:** LLM non-determinism → schema-first comparator; match on structured fields, not free text. Pin Sonnet model version in script.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Findings
[Phase 1 audit results — spelling variants, ambiguous aliases, concept-11 LCOE hand-calc result]

### Phase 1 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

### Phase 2 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

### Phase 3 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

### Phase 4 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

### Phase 5 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

---

**Status**: Draft → In Progress → Complete

**Next Step:** After approval → `/_my_implement` (execute phase by phase)
