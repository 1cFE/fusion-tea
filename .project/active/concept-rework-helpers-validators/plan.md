# Implementation Plan: Shared `model_setup` Helpers + Validator Rework

**Status:** Draft
**Created:** 2026-05-31
**Last Updated:** 2026-05-31

## Source Documents
- **Spec:** [`spec.md`](spec.md)
- **Design:** [`design.md`](design.md) ← component details, decisions, invariants, gotchas live here

## Implementation Strategy

**Phasing Rationale:**
Phase 1 builds the helper first because the whole item rests on it reproducing the re-pinned oracle, and because it emits the **helper-form `model_setup.py` fixture** the Phase 2 contract validator needs as its second oracle (the prototype is only the inline form). Phase 2 then adds the two output-gate validators that read `model_setup.py` text. Phase 3 adds the two coherence checks (pure over CSV + code, independent but logically downstream). Phase 4 writes the FR-8 handoff doc. Nothing wires into the live loop — see [design.md#core-concept](design.md#core-concept).

**Critical Path:**
helper (oracle) → helper-form fixture → contract/registry validators → coherence checks → signal contract doc.

**First Proof Point:**
Phase 1 test reproducing **native 174.5 / 1 GWe bare 137.2 / 1 GWe all-on 584.5 $/MWh** for concept 01 (`P_native=233`) against the fixed library, with a spy confirming the file passes no financial defaults.

**Overall Validation Approach:**
- Each phase starts with tests; the prototype + the re-pinned oracle are the truth source ([design.md#validation-approach](design.md#validation-approach)).
- All new code is pure functions / library surface — no loop wiring, so "no regressions" = the existing `test_validators.py` (retained validators) stays green.

**Environment:** `uv run python -m pytest <path>` from `exploration/concept_analysis/scripts/` (tests import `lib.*`). Always `uv run` per CLAUDE.md.

---

## Phase 1: Helpers module + tests

### Goal
Create `lib/model_setup_helpers.py` with the four-step API and prove it reproduces the re-pinned oracle. De-risks the load-bearing assumption everything else depends on.

### Assumption Under Test
The helper, sourcing `availability`/`lifetime_yr` from library defaults (not hardcoding), reproduces the oracle — and passes *no* financial defaults (`interest_rate`/`inflation_rate`/`construction_time_yr`) from the per-concept layer. See [design.md#architecture](design.md#architecture) (helper call shapes) and [design.md#key-bets--decisions](design.md#key-bets--decisions) (Decisions 2–4).

### Test Stencil (Write This First)
```python
def test_oracle_concept01():
    model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
    result, result_1gw = run_native_and_1gw(model, ARC_SPEC, ARC_OVERRIDES, 233.0)
    assert result.costs.lcoe == pytest.approx(174.5, abs=0.5)        # native
    assert result_1gw.costs.lcoe == pytest.approx(584.5, abs=0.5)    # all-on

def test_no_financial_defaults_from_caller():
    spy = SpyModel()  # records forward() kwargs
    run_native_and_1gw(spy, ARC_SPEC, [], 233.0)
    for call in spy.calls:
        assert "interest_rate" not in call and "inflation_rate" not in call
        assert call["availability"] == 0.85 and call["lifetime_yr"] == 40.0  # library-sourced
        assert call["n_mod"] == (1 if call["net_electric_mw"] == 233.0 else pytest.approx(1000/233.0))

def test_p_native_1000_collapses():
    r, r1 = run_native_and_1gw(model, SPEC, [], 1000.0)
    assert r.costs.lcoe == pytest.approx(r1.costs.lcoe)  # n_mod==1, native==projection
```

### Changes Required

**See [design.md#component-overview](design.md#component-overview) for the API; [design.md#implementation-notes](design.md#implementation-notes) for the library-sourced-defaults gotcha.**

#### 1. Test file
**File:** `exploration/concept_analysis/scripts/test_model_setup_helpers.py` (NEW — write first)
- [x] `ARC_SPEC` / `ARC_OVERRIDES` fixtures from the prototype (`R0=3.3, plasma_t=1.13, elon=1.84, eta_th=0.46, p_input=38.6`; the 4 six-field overrides).
- [x] Oracle test (174.5 / 137.2 bare / 584.5 all-on), no-defaults spy test, `p_native==1000` collapse, `enabled_overrides` filter + last-wins-on-duplicate, empty-overrides projection.

#### 2. Helper module
**File:** `exploration/concept_analysis/scripts/lib/model_setup_helpers.py` (NEW)
- [x] `Override` TypedDict (six fields, [design.md#component-overview](design.md#component-overview)).
- [x] `enabled_overrides(overrides) -> dict[str, float]`.
- [x] `run_native_and_1gw(model, spec, overrides, p_native, *, noak=True)`: resolve `A = default_availability(model.concept)`, `L = CostingInput.model_fields["lifetime_yr"].default`; issue native (`n_mod=1`) + projection (`net=1000, n_mod=1000/p_native, override_reference_mw=p_native`) forwards with `A`/`L`; return `(result, result_1gw)`.
- [x] `print_cas_breakdown(result, result_1gw, overrides)`: native-vs-1GWe CAS table + the grep-able `LCOE: <n> $/MWh` line ([design.md#required-invariants](design.md#required-invariants) #7).

### Validation
**Automated:**
- [x] `uv run python -m pytest test_model_setup_helpers.py` → all pass (13 passed)
- [x] `uv run python -m pytest test_validators.py` → no regressions (untouched) (68 passed)

**Manual:**
- [x] Helper output confirmed grep-able: `TestPrintCasBreakdown.test_emits_grepable_lcoe_line` runs the headline through `run_model`'s exact regex `LCOE:\s*([\d.]+)\s*\$/MWh` and asserts the first match == 584.5.

**What We Know Works After This Phase:**
The two-knob call shape and the oracle hold against the fixed library; the helper is the production target for Item 8.

---

## Phase 2: Output-gate validators + tests

### Goal
Add `validate_model_setup_contract` and `validate_override_registry` to `lib/validators.py`, gating `model_setup.py` *shape* via AST.

### Assumption Under Test
The AST checks pass both conformant forms (inline prototype + helper-form fixture from Phase 1) and fail each documented breakage. See [design.md#implementation-notes](design.md#implementation-notes) (dual-form recognition, AST walk, registry value rule) and [design.md#key-bets--decisions](design.md#key-bets--decisions) (Decisions 1, 3, 5).

### Test Stencil (Write This First)
```python
def test_contract_accepts_both_forms():
    assert validate_model_setup_contract(PROTOTYPE_TEXT).valid           # inline forward(net=1000)
    assert validate_model_setup_contract(HELPER_FORM_TEXT).valid         # run_native_and_1gw unpack

def test_contract_strict_rejects_inline():
    r = validate_model_setup_contract(PROTOTYPE_TEXT, strict_helper_only=True)
    assert not r.valid  # Item-8 mode

def test_contract_failures():
    assert not validate_model_setup_contract(MISSING_RESULT_1GW).valid
    assert not validate_model_setup_contract(INLINE_NO_NET_1000).valid
    assert "DEFAULT" in validate_model_setup_contract(HAS_DEFAULT_COMMENT).details

def test_registry():
    assert validate_override_registry(PROTOTYPE_TEXT).valid               # 4-entry, six-field
    assert not validate_override_registry(MISSING_PROVENANCE).valid
    assert not validate_override_registry(NONNUMERIC_VALUE).valid         # ast.literal_eval -> not int|float
    assert not validate_override_registry(PROVENANCE_GUESS).valid
    assert not validate_override_registry(DUP_ACCOUNT).valid
```

### Changes Required
**See [design.md#component-overview](design.md#component-overview) and [design.md#implementation-notes](design.md#implementation-notes).**

- [x] `test_validators.py`: add `TestModelSetupContract`, `TestOverrideRegistry`; reuse `PROTOTYPE_TEXT` (read the prototype file) + a `HELPER_FORM_TEXT` constant (the Phase-1 throwaway, inlined as a fixture) + minimal broken-variant strings.
- [x] `lib/validators.py`: `validate_model_setup_contract(text, *, strict_helper_only=False, warn_on_default_comments=True)` — module-level `model`/`result`/`result_1gw`; dual-form `result_1gw` recognition; `tokenize`-based `# DEFAULT:` line set; `details` names matched form.
- [x] `lib/validators.py`: `validate_override_registry(text)` — `overrides` = list of `ast.Dict`; six fields; `ast.literal_eval(value) ∈ {int,float}` (BinOp → error); `provenance ∈ {direct,derived}`; no dup `account`.

### Validation
**Automated:**
- [x] `uv run python -m pytest test_validators.py` → all pass (new + retained) (86 passed)

**Manual:**
- [x] Covered by `TestModelSetupContract.test_accepts_inline_prototype` (prototype → valid) + `test_rejects_inline_without_net_1000` (`net_electric_mw=500` → invalid with a clear message).

**What We Know Works After This Phase:**
`model_setup.py` shape is structurally enforceable for both the current prototype and the Item-8 helper form, with the strict switch ready for Item 8.

---

## Phase 3: Coherence checks + tests

### Goal
Add `validate_design_point_coherence` and `check_override_count_vs_fit_grade` — cross-artifact / advisory checks (not chained, not loop-wired; [design.md#key-bets--decisions](design.md#key-bets--decisions) Decision 5).

### Assumption Under Test
The coherence check flags the exact Phase 0 operator error and passes when legs agree; count-vs-grade thresholds match the acceptance behavior. See [design.md#implementation-notes](design.md#implementation-notes) (coherence inputs, thresholds).

### Test Stencil (Write This First)
```python
ROW = {"concept_id": "01-...", "p_native_mwe": 233}

def test_design_point_coherence():
    assert validate_design_point_coherence("01-...", MS_233, ROW).valid          # two legs agree
    assert not validate_design_point_coherence("01-...", MS_400, ROW).valid      # Phase-0 error
    # provenance mismatch on a shared account when analysis.md leg supplied
    assert not validate_design_point_coherence("01-...", MS_233, ROW, ANALYSIS_DERIVED).valid

def test_count_vs_grade():
    assert check_override_count_vs_fit_grade("High", 4).valid and not _flagged("High", 4)
    assert _flagged(check_override_count_vs_fit_grade("High", 12))
    assert _flagged(check_override_count_vs_fit_grade("Low", 0))
```

### Changes Required
**See [design.md#component-overview](design.md#component-overview).**
- [x] `test_validators.py`: add `TestDesignPointCoherence`, `TestOverrideCountVsFitGrade`; `MS_233`/`MS_400` = minimal modules differing only in `P_native`; assert `details` carries the flag while `valid` stays `True` for the advisory count check.
- [x] `lib/validators.py`: `validate_design_point_coherence(concept_id, model_setup_text, design_point_row, analysis_md_text=None)` — AST `P_native` from code; `design_point_row["p_native_mwe"]`; ≤0.1% rel tolerance; provenance agreement on shared accounts; third leg `None`-gated.
- [x] `lib/validators.py`: `check_override_count_vs_fit_grade(fit_grade, enabled_count)` — named thresholds (`_HIGH_FIT_MANY_THRESHOLD=8`, Low/Med zero); advisory `ValidationResult` (`valid=True`, flag in `details`).

### Validation
**Automated:**
- [x] `uv run python -m pytest test_validators.py` → all pass (111 across all suites)

**Manual:**
- [x] Real-data check: prototype `model_setup.py` (233) vs `design_point.csv` row 01 (233) → valid (2-leg); bump to `P_native=400` → flagged (`model_setup=400 vs design_point=233`). Real `archetype_fit` grade High + 4 overrides → quiet.

**What We Know Works After This Phase:**
The high-leverage `P_native` operator error and the count-vs-grade smell are catchable deterministically; checks are ready for Item 8/9 to wire into assess / `model_critic`.

---

## Phase 4: signal_contract.md + epic nit

### Goal
Write the FR-8 handoff doc so Item 8 can swap the regex parsers without stranding loop control; log the stale-doc nit.

### Assumption Under Test
The four producer return shapes are fully specified — Item 8's parser implementer does not guess. See [design.md#component-overview](design.md#component-overview) (signal contract table) and [design.md#research-findings](design.md#research-findings) (coupling table).

### Changes Required
- [x] `signal_contract.md` (NEW, this dir): the coupling table + the four return shapes (`parse_verdict_from_feedback`→`tuple[str,int]`; `has_model_category_findings`→`bool`; review verdict→`"PROCEED"|"REVISE"`; `parse_proposed_actions`→`list[dict]` with the nine keys) + the exact wire point (`loop.py:638` output gates; assess/`model_critic` for coherence). Lift directly from the design — no new analysis.
- [x] Epic nit: appended the `override_reference_mw` stale-line correction (lines 128/152/206 of `concept-analysis-rework.md`) as a "Tracked nits" block under Item 7 in `epic_concept_analysis_rework.md` (no pre-existing nit list — created the block). Also logged the `params.n_mod` dict-vs-object wording nit.

### Validation
**Manual:**
- [x] Re-read `signal_contract.md` against the design's coupling table → all five coupling rows + all four producer return shapes carried over verbatim; each consumer has a named producer + return shape. Added a "what removal looks like" sequence and the FR-9-not-discharged caveat.

**What We Know Works After This Phase:**
Item 8 has an unambiguous contract to implement against; Item 7 is complete.

---

## Risk Management

**See [design.md#potential-risks](design.md#potential-risks).**

**Phase-Specific Mitigations:**
- **Phase 1:** library-sourced defaults already de-risked (model.concept accessible; `default_availability(TOKAMAK)=0.85`; lifetime default `40.0`; oracle measured = 174.5/137.2/584.5). If a number drifts, the library moved — re-pin and note it.
- **Phase 2:** both `model_setup.py` forms (inline prototype + helper-form fixture) in the test matrix so the dual-form path can't silently pass only one; `# DEFAULT:` heuristic is warn-only.
- **Phase 3:** third coherence leg is `None`-gated — ship two-leg now, don't build the `analysis.md` parser against an Item-8 format that doesn't exist yet.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-05-31
**Actual Changes:**
- Created `exploration/concept_analysis/scripts/lib/model_setup_helpers.py` — `Override` TypedDict (6 fields), `enabled_overrides`, `run_native_and_1gw`, `print_cas_breakdown`. `availability` via `default_availability(model.concept)`; `lifetime_yr` via module-level `_LIBRARY_LIFETIME_YR = CostingInput.model_fields["lifetime_yr"].default` (= 40.0). Projection always passes `override_reference_mw=p_native` (no-op with empty overrides).
- Created `exploration/concept_analysis/scripts/test_model_setup_helpers.py` — 13 tests across `TestOracle`, `TestForwardKwargShape`, `TestPNative1000Collapses`, `TestEnabledOverrides`, `TestPrintCasBreakdown`.
- **Oracle re-confirmed against the fixed library at lt=40:** native 174.5, 1 GWe bare 137.2, 1 GWe all-on 584.5 $/MWh. `default_availability(TOKAMAK)=0.85`, `(MIRROR)=0.87`.

**Issues:** None. `result.params` is a **dict** (`params["n_mod"]`), not an object — the design's "`result_1gw.params.n_mod`" wording is slightly off. Out of scope here (explorer = Item 10); flagged to the user. Helper returns only the tuple, so unaffected.

**Deviations:**
- `print_cas_breakdown` leads with the **1 GWe projection** LCOE as the grep-able headline (`LCOE: <n> $/MWh`) and reports the native figure on a distinct `Native LCOE =` line. Reason: `run_model` (loop.py:676) uses `re.search` (first match) for a display string; leading with the projection makes the standardized cross-concept number the headline. Prototype printed native first — intentional change.
- Manual check discharged via the `capsys` unit test rather than a throwaway file (same regex, stronger assertion: also checks the matched value == 584.5).

### Phase 2 Completion
**Completed:** 2026-05-31
**Actual Changes:**
- `lib/validators.py`: added `import ast/io/tokenize`; added `validate_model_setup_contract` and `validate_override_registry` plus AST helpers (`_target_names`, `_module_bindings`, `_is_call_to_name`, `_is_forward_call`, `_kwarg_equals`, `_default_comment_linenos`, `_forward_kwarg_linenos`, `_dict_literal_fields`). Module-level constants `_REQUIRED_OVERRIDE_FIELDS`, `_VALID_PROVENANCE`. No existing validators touched (regex set untouched per Decision 1).
- `test_validators.py`: added `TestModelSetupContract` (9 tests) + `TestOverrideRegistry` (9 tests), `PROTOTYPE_TEXT` (read from prototype), `HELPER_FORM_TEXT` fixture, broken-variant strings.

**Issues:** None.

**Deviations:**
- Added an `EXPRESSION_VALUE` (BinOp `5150 * 1.34`) variant test in addition to the stencil's `NONNUMERIC_VALUE` (string) — the design's "no expression language" rule (BinOp → error) deserved its own coverage. `ast.literal_eval` raises `ValueError` on `*`, caught as the pre-compute error.

### Phase 3 Completion
**Completed:** 2026-05-31
**Actual Changes:**
- `lib/validators.py`: added `validate_design_point_coherence` and `check_override_count_vs_fit_grade` + helpers (`_close`, `_module_pnative`, `_override_provenance_map`, `_analysis_provenance_map`) and constants (`_HIGH_FIT_MANY_THRESHOLD=8`, `_PNATIVE_REL_TOL=0.001`, account/provenance/P_native regexes).
- `test_validators.py`: `TestDesignPointCoherence` (5 tests) + `TestOverrideCountVsFitGrade` (7 tests), `_flagged` helper, `MS_233`/`MS_400`/`ROW`/`ANALYSIS_DERIVED` fixtures.
- Real-data manual check passed (prototype/233 coherent, /400 flagged, High+4 quiet).

**Issues / Design-Plan tension (flagged to user):** The design's risk note says ship "parser stub + two-leg tests now" and "don't build the analysis.md parser against an Item-8 format that doesn't exist yet," but the plan's Phase 3 stencil includes a provenance-mismatch test that *requires* a working third-leg parser (`ANALYSIS_DERIVED`). Resolution: implemented a **minimal, explicitly-provisional** analysis.md scraper (`_analysis_provenance_map` + `_ANALYSIS_PNATIVE_RE`) — line-level account↔provenance association, not the full Design Point block — gated entirely behind `analysis_md_text is not None` so the **two-leg path remains the default/live shape**. The format is documented as provisional; Item 8 finalizes it. This satisfies the plan's test while honoring the design's "two-leg default, third leg None-gated" intent and keeping the parser minimal (the risk mitigation).

**Deviations:**
- Added `test_three_legs_agree` and `test_boundary_high_eight_quiet` beyond the stencil (positive third-leg path; the strictly-greater-than threshold boundary). `None` fit grade treated as quiet (not in the documented flag combos).

### Phase 4 Completion
**Completed:** 2026-05-31
**Actual Changes:**
- Created `.project/active/concept-rework-helpers-validators/signal_contract.md` — coupling table (5 rows), producer return-shape table (4 producers), wire points (`loop.py:638` output gates; assess/`model_critic` coherence), and the removal sequence.
- `.project/backlog/epic_concept_analysis_rework.md` — added a "Tracked nits" block under Item 7 (the `override_reference_mw` stale lines + the `params.n_mod` wording nit).

**Issues:** No pre-existing "nit list" in the epic — created a "Tracked nits" block under the Item 7 section as the natural home.

**Deviations:** None of substance. Folded in the `params.n_mod` dict-vs-object nit discovered in Phase 1 (beyond the planned single nit) since it's the same kind of tracked-correction.

---

**Status:** Draft → In Progress → **Complete**
