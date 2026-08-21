# Implementation Plan: Three-Forward Contract — `generic` / `native` / `result_1gw`

**Status:** Complete
**Created:** 2026-05-31
**Last Updated:** 2026-05-31

## Source Documents
- **Spec:** `.project/active/concept-rework-three-forward-contract/spec.md`
- **Design:** `.project/active/concept-rework-three-forward-contract/design.md` ← component details, decisions, invariants, and the AST/test/doc edit inventories (Appendices A–C)

## Implementation Strategy

**Phasing Rationale:** Build outward from the contract's numeric core. Phase 1 fixes the helper (the source of truth) and pins the new `native` oracle; Phase 2 makes the validators recognize that shape; Phase 3 proves a real generated file conforms end-to-end; Phase 4 aligns the prose. Each phase only depends on the ones before it.

**Critical Path:** helper return shape + `native` number (P1) → validator recognition of that shape (P2) → a conforming `model_setup.py` passes both validators (P3) → docs match (P4).

**First Proof Point:** P1 — `run_native_and_1gw` returns `(native, result_1gw)` with `native` pinned from a real run and `result_1gw` still ≈ 584.5 (byte-for-byte invariant). See `design.md#required-invariants`.

**Overall Validation Approach:** test-first each phase; `uv run python -m pytest` for code phases; `grep` hygiene gate for the doc phase. No phase may perturb the `result_1gw` number.

**Environment:** all Python via `uv run` (see CLAUDE.md). Test dir: `exploration/concept_analysis/scripts/`.

---

## Phase 1: Helper + helper tests

### Goal
Replace the helper's overrides-off `result` with the overrides-on `native` forward; return `(native, result_1gw)`. Update `generic_reference` docstring and `print_cas_breakdown` to the three-forward shape. Pin the new `native` oracle.

### Assumption Under Test
The `native` forward (`net=P_native, n_mod=1, cost_overrides=<enabled>, override_reference_mw=P_native`) yields a stable number, and `result_1gw` is unperturbed by the helper edit.

### De-risk step 0 (do first)
Run the real model once to capture `native` LCOE (overrides-on at 233 MWe) and the per-account values — this is the new oracle constant every test keys off. See `design.md#next-stage-handoff` ("De-risk first").

### Test Stencil (Write This First)
```python
class TestOracle:
    def test_oracle_concept01(self):
        model = _tokamak_model()
        generic = generic_reference(model, ARC_SPEC, P_NATIVE)
        native, result_1gw = run_native_and_1gw(model, ARC_SPEC, ARC_OVERRIDES, P_NATIVE)
        assert generic.costs.lcoe == pytest.approx(174.5, abs=0.5)      # overrides OFF
        assert native.costs.lcoe == pytest.approx(<PINNED>, abs=0.5)    # overrides ON, 233 MWe
        assert result_1gw.costs.lcoe == pytest.approx(584.5, abs=0.5)   # unchanged

    def test_empty_overrides_native_equals_generic(self):
        model = _tokamak_model()
        generic = generic_reference(model, ARC_SPEC, P_NATIVE)
        native, _ = run_native_and_1gw(model, ARC_SPEC, [], P_NATIVE)
        assert native.costs.lcoe == pytest.approx(generic.costs.lcoe)   # empty registry ⇒ equal
```

### Changes Required

**See `design.md` for:** `#architecture` (surface 1), `#component-overview`, `#implementation-notes`, `#required-invariants`.

#### 1. Test file
**File:** `exploration/concept_analysis/scripts/test_model_setup_helpers.py`
- [x] Capture the `native` oracle constant (de-risk step 0) and fill `<PINNED>`. → **629.0** $/MWh.
- [x] Rewrite `TestOracle` (unpack `native, result_1gw`; add `generic` assertion).
- [x] `test_empty_overrides_is_library_bare` → add `native == generic` assertion (keep `result_1gw ≈ 137.2`).
- [x] Invert `test_native_call_omits_override_kwargs` (`:152`) → `test_native_call_passes_overrides`: the `native` (P_native) call now carries `cost_overrides` and `override_reference_mw=P_native`.
- [x] `test_native_equals_projection` (`:201`): rename locals; logic unchanged (`P_native=1000`).
- [x] `TestPrintCasBreakdown`: call `print_cas_breakdown(generic, native, result_1gw, overrides)`; keep `test_emits_grepable_lcoe_line` green.

#### 2. Helper
**File:** `exploration/concept_analysis/scripts/lib/model_setup_helpers.py` (per `design.md#architecture` surface 1)
- [x] `run_native_and_1gw`: replace `result = generic_reference(...)` with a `native = model.forward(net=p_native, n_mod=1, cost_overrides=enabled_overrides(overrides), override_reference_mw=p_native, availability=..., lifetime_yr=..., noak=noak, **spec)` call; `return native, result_1gw`. Leave the `result_1gw` call untouched.
- [x] `generic_reference`: rewrite docstring (now produces module-level `generic`; no longer "the same forward `run_native_and_1gw` issues for `result`").
- [x] `print_cas_breakdown`: signature → `(generic, native, result_1gw, overrides)`; three CAS columns (`generic` / `native` / `1 GWe`); keep the `LCOE:` headline line first and grepable.
- [x] Module + `run_native_and_1gw` docstrings: "four-step" / "native = bare reference" → three-forward framing.

### Validation
**Automated:**
- [x] `uv run python -m pytest exploration/concept_analysis/scripts/test_model_setup_helpers.py` → pass (13 passed)
- [x] Confirm `result_1gw ≈ 584.5` assertion still green (byte-for-byte invariant)

**Manual:**
- [x] Run the prototype/concept-01 setup; eyeball the three-column print block (generic ≤ native pattern as overrides apply)

**What We Know Works After This Phase:** the three forward numbers, their relationships (empty ⇒ `generic==native`; `P_native=1000` ⇒ `native==result_1gw`), and that `result_1gw` is unchanged.

---

## Phase 2: Validators + validator tests

### Goal
Teach `validate_model_setup_contract` the four-name / two-binding shape and `validate_override_registry` the `generic`-frame rule.

### Assumption Under Test
The AST recognition accepts the `generic = generic_reference(...)` line and the `native, result_1gw = run_native_and_1gw(...)` tuple, and the frame check rejects exactly `{native, result_1gw, result}` without flagging legitimate forms.

### Test Stencil (Write This First)
```python
def test_contract_requires_native():
    src = THREE_FORWARD_SETUP.replace("native, result_1gw =", "result_1gw =")  # drop native
    assert validate_model_setup_contract(src).valid is False

def test_registry_frame_rule():
    assert _registry_with("0.70 * generic.costs.cas21").valid is True
    for bad in ("native", "result_1gw", "result"):
        r = _registry_with(f"0.70 * {bad}.costs.cas21")
        assert r.valid is False and "generic" in r.fix_message
```

### Changes Required
**See `design.md#appendix-a--validator-ast-edits-for-the-plan`** for the exact node-match edits.

**Specific file changes:**
- [x] `lib/validators.py:542` — required names → `("model", "generic", "native", "result_1gw")`; update `missing` message.
- [x] `lib/validators.py:555–567` — helper-form match → `native, result_1gw = run_native_and_1gw(...)` tuple; add a `generic = generic_reference(...)` binding check (hard requirement, both modes); kept inline-form for non-strict.
- [x] `lib/validators.py:518–519,574–577` — docstrings/messages → three-forward.
- [x] `lib/validators.py:742` — `if "result_1gw" in referenced:` → `if referenced & {"native", "result_1gw", "result"}:`; message names `generic`.
- [x] `lib/validators.py:662,735–736,746–748,761–762` — "native `result`" → "`generic`".
- [x] `test_validators.py` — contract fixtures bind all four names; added failing fixtures (missing `native`; two-forward residue; generic-not-via-helper). Registry fixtures: accept `generic.*`; reject `native.*` / `result_1gw.*` / `result.*`.
- [x] `test_loop_wiring.py` — `HELPER_FORM` / `INLINE_FORM` fixtures → three-forward (test-local, Appendix B scope).
- [x] **(deviation, user-approved)** Updated 3 shipped concept-01 helper-form files (`analyses/01-.../model_setup.py` + `iter-1` + `iter-2`) to three-forward — they call the changed helper at module level and would otherwise crash on import. See Phase 2 Completion note.

### Validation
**Automated:**
- [x] `uv run python -m pytest exploration/concept_analysis/scripts/test_validators.py` → pass (90)
- [x] Full suite: `uv run python -m pytest exploration/concept_analysis/scripts/` → 410 passed; only 4 **pre-existing** `test_concepts_v2.py` failures remain (confirmed pre-existing via git-stash bisect — unrelated to this item, about pending-concept design points).

**Manual:**
- [x] Both validators recognize the three-forward helper + inline fixtures; reject two-forward residue and `native`/`result_1gw`/`result` frames.

**What We Know Works After This Phase:** the validators enforce the three-forward contract and reject the two-forward residue and wrong-frame relative overrides.

---

## Phase 3: Prompt templates + end-to-end integration proof

### Goal
Repoint the prompt templates from the interim optional-`ref` form to the mandatory `generic` line, and prove a real concept-01 three-forward `model_setup.py` passes both validators (acceptance tests 1 & 2).

### Assumption Under Test
The shape the prompts instruct produces a file that passes the Phase 2 validators (prompt ↔ validator agreement).

### Test Stencil (Write This First)
```python
def test_concept01_threeforward_passes_contract():
    src = (FIXTURES / "concept01_model_setup.py").read_text()
    assert validate_model_setup_contract(src, strict_helper_only=True).valid
    assert validate_override_registry(src).valid
```

### Changes Required
**See `design.md#architecture`** (surface 5 / prompt notes) and **`#appendix-c`**.

**Specific file changes (unwind the interim local `ref` edits → mandatory `generic`):**
- [x] `prompt_templates/model_setup_costingfe.md` — `generic = generic_reference(...)` now **mandatory** (Step 2b); `generic_reference` imported unconditionally; Hard Rule 1 (names `model`/`generic`/`native`/`result_1gw`), Hard Rule 2 (`native, result_1gw = ...` + mandatory `generic` line), Hard Rule 5 (relative refs `generic`, reject `native`/`result_1gw`/`result`), Hard Rule 7 (three forwards), the `print_cas_breakdown(generic, native, result_1gw, overrides)` call, the structure heading, and four-step → three-forward all updated.
- [x] `prompt_templates/config/account_walkthrough.md` — relative `value` references `generic` (dropped `ref`); rejects `native`/1 GWe.
- [x] `prompt_templates/output_template.md` — relative-expression example → `generic.costs.cas21`; reject note → `native`/`result_1gw`.
- [x] Added `tests/fixtures/concept01_model_setup.py` (three-forward, faithful ARC conversion + one `generic`-relative override) and wired `TestThreeForwardIntegration` (2 tests) in `test_validators.py`.
- [x] **FOUND beyond Appendix C (user-approved to handle):** `model_setup_costingfe_edit.md` → three-forward edit contract (mandatory `generic`, `native, result_1gw = ...`, 4-arg print, relative refs `generic`); `config/assessment_checklist.md` §5 → three-forward checklist (`generic`/`native`/`result_1gw`). `feedback/power_standardization_costingfe.md` **investigated, left untouched**: orphaned legacy artifact from PR #6 (obsolete post-hoc `_ALPHA` scaling), not wired into the current pipeline (no loader, no filename references) — flagged as a safe retire candidate for separate cleanup, NOT a three-forward rename.

### Validation
**Automated:**
- [x] `uv run python -m pytest exploration/concept_analysis/scripts/test_validators.py` → 92 passed (incl. 2 integration tests)

**Manual:**
- [x] `uv run python tests/fixtures/concept01_model_setup.py` → runs; prints grepable `LCOE: 563.6 $/MWh` headline + `generic`/`native` lines + three-column block; both validators pass (strict contract + registry).

**What We Know Works After This Phase:** a generated-shape file conforms to the contract end-to-end; the prompt instructions and validators agree.

---

## Phase 4: Doc/spec alignment (FR-8)

### Goal
Update the design doc, epic, and Item 8/9/10 specs to the three-forward contract; remove all two-forward `result` contract language.

### Assumption Under Test
None — hygiene/consistency (acceptance test 6).

### Validation-as-test (write the gate first)
```bash
# Acceptance test 6: no remaining two-forward `result` contract references.
grep -rn "result, result_1gw\|module-level .result.\|reads .result.\|four-step" \
  .project/concepts/concept-analysis-rework-design.md \
  .project/backlog/epic_concept_analysis_rework.md \
  .project/active/concept-rework-{prompt-templates,model-critic,explorer-pilot}/  # → expect no contract hits
```

### Changes Required
**See `design.md#appendix-c--fr-8-documentation-surface-for-the-plan`** for the line-level inventory.

- [x] `concept-analysis-rework-design.md` — four-step → three-forward (five-step) inline example (added the `native` forward, renamed `result`→`generic`); Override Entry references `generic` (rejects `native`/`result_1gw`); module-level contract → `model/generic/native/result_1gw`; `model_critic` reads the three forward objects; `concept_explorer` contract updated.
- [x] `epic_concept_analysis_rework.md` — `:34` Future State bullet → three-forward (five-step); `:47`/`:48` success criteria → three-forward + `model/generic/native/result_1gw`; `:19` Critical Success Factor verified (about `result_1gw`, unchanged — left). Item 7 retrospective got a superseding annotation; Item 8 retrospective + the relative-override-fix note got forward-pointers. **Genuinely-historical Item 1/6 `[x]` records left verbatim** (accurate history; Appendix C scoped only forward-looking lines).
- [x] `concept-rework-prompt-templates/spec.md` + `design.md` (Item 8) — all four-step → three-forward; FR-10 (five-step + mandatory `generic`), FR-11 (`model/generic/native/result_1gw`), FR-14 (relative refs `generic`, reject `native`/`result_1gw`), FR-15/16; helper signature `→ (native, result_1gw)`; design code block + key statements updated.
- [x] `concept-rework-model-critic/spec.md` (Item 9) — four-step → three-forward; critic reads the live `generic`/`native`/`result_1gw` objects (FR-8 + edge cases). **Code untouched** (works against the converted 01 file; verified by full suite).
- [x] `concept-rework-explorer-pilot/spec.md` + `design.md` (Item 10) — contract surface → `model/generic/native/result_1gw`; FR-3 fail-loud framing updated (no `result` to fall back to); design diagram → three-forward. **Explorer code untouched** (regeneration out of scope).

### Validation
**Automated:**
- [x] Grep gate run over the must-be-clean surface (design doc, helper, validators, Item 8/9/10 spec.md, Item 10 design.md) → **CLEAN** (no two-forward `result`/four-step contract hits). Remaining epic hits are historical `[x]`/retrospective records (Items 1/6/7/8) + the Item 7 superseding annotation; "reads `result_1gw`" hits are correct three-forward usage. Item 8 `plan.md`/`pilot_report.md` historical logs left as-is (not in the acceptance-test-6 spec surface).
- [x] Full scripts suite → **419 passed**, 5 skipped, 4 pre-existing unrelated `test_concepts_v2.py` failures.

**Manual:**
- [x] Design doc inline example + epic Future State/Success Criteria reviewed for coherence.

**What We Know Works After This Phase:** every contract-bearing document describes the three-forward shape; acceptance test 6 passes.

---

## Environment Setup
**See CLAUDE.md** — all Python via `uv run`; tests under `exploration/concept_analysis/scripts/`.

## Risk Management
**See `design.md#potential-risks`.**

**Phase-Specific Mitigations:**
- **P1:** assert `result_1gw ≈ 584.5` stays green (byte-for-byte); keep `test_emits_grepable_lcoe_line` green (headline order).
- **P2:** forbid only `{native, result_1gw, result}` in the frame check — leave other runtime names permissive.
- **P3:** the integration fixture is the prompt↔validator agreement check; if it fails, the prompt shape is wrong, not the validator.
- **P4:** read each grep hit — distinguish contract language from incidental `result_1gw`/`effective_result` code identifiers.

## Implementation Notes
[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-05-31

**De-risk (step 0) — pinned oracle (real model, concept 01):**
- `generic` LCOE = **174.45** $/MWh (overrides off, 233 MWe)
- `native` LCOE = **628.99** $/MWh (overrides on, 233 MWe) ← new pinned oracle (≈629.0)
- `result_1gw` LCOE = **584.54** $/MWh (overrides on, 1 GWe) — unchanged
- Confirmed `native == native_no_ref`: passing `override_reference_mw=P_native` is a no-op at design scale (ratio 1.0) → resolves spec Open Question 3; pass it explicitly for uniformity.

**Changes Made:**
- `lib/model_setup_helpers.py`: module docstring → three-forward framing; `generic_reference` docstring rewritten (produces module-level `generic`); `run_native_and_1gw` now issues the overrides-ON `native` forward directly (no longer recomputes `generic_reference`) and returns `(native, result_1gw)`; `enabled` bound once and shared by both forwards; `print_cas_breakdown` signature → `(generic, native, result_1gw, overrides)` with three CAS columns and three-column CAS22 detail; grepable `LCOE:` headline kept first.
- `test_model_setup_helpers.py`: module-docstring oracle updated; import `generic_reference`; `TestOracle.test_oracle_concept01` asserts all three forwards (generic 174.5 / native 629.0 / result_1gw 584.5); `test_empty_overrides_is_library_bare` asserts `native == generic`; inverted `test_native_call_omits_override_kwargs` → `test_native_call_passes_overrides`; `test_native_equals_projection` locals renamed; `TestPrintCasBreakdown` passes all three forwards.

**Issues Encountered:** none.

**Deviations from Plan:** none. (The plan's `<PINNED>` placeholder resolved to 629.0; `native > result_1gw` here because the large absolute overrides dominate at the 233 MWe single-module scale and spread out under replication — expected, not a regression.)

### Phase 2 Completion
**Completed:** 2026-05-31

**Changes Made:**
- `lib/validators.py` — `validate_model_setup_contract`: required names → `model/generic/native/result_1gw`; added a hard `generic = generic_reference(...)` binding check (both modes); helper-form recognition now matches the `native, result_1gw = run_native_and_1gw(...)` tuple; kept the inline form as the non-strict escape hatch (governs only how `native`/`result_1gw` bind — `generic` is always via the helper); docstrings + strict/non-strict messages reframed. `validate_override_registry`: frame check now forbids the set `{native, result_1gw, result}` (was just `result_1gw`), error message names `generic`; docstring + comments reframed.
- `test_validators.py` — `HELPER_FORM_TEXT` → three-forward; new `INLINE_FORM_TEXT` (generic via generic_reference, native/result_1gw inline); failing fixtures `MISSING_NATIVE`, `TWO_FORWARD_RESIDUE`, `GENERIC_NOT_VIA_HELPER`; `MISSING_RESULT_1GW`/`INLINE_NO_NET_1000`/`HAS_DEFAULT_COMMENT` rebuilt to three-forward; registry `RESULT_RELATIVE_VALUE`→`GENERIC_RELATIVE_VALUE` (accept), added `NATIVE_VALUE`/`RESULT_VALUE` (reject); prototype kept only as the registry oracle (constant overrides still valid).
- `test_loop_wiring.py` — `HELPER_FORM`/`INLINE_FORM` fixtures → three-forward.

**Decisions:**
- **`generic` must be bound via `generic_reference()`** in both strict and non-strict modes (per design Appendix A). The "inline form" escape hatch now governs only `native`/`result_1gw`. Consequence: a fully hand-rolled file can't satisfy the contract — acceptable, since the standalone `generic` line is mandatory anyway (FR-1 / Decision 1).
- The Phase 0 prototype (`concept-rework-prototype/artifacts/model_setup.py`) is two-forward; it is no longer a valid *contract* fixture but remains the registry oracle (its overrides are constants).

**Issues Encountered / Deviation (user-approved):**
- The `print_cas_breakdown` arity change (3→4 args) and the `run_native_and_1gw` return-shape change broke the **only 3 shipped files that call the helper at module level**: `analyses/01-hts-compact-tokamak/model_setup.py` and its `iter-1`/`iter-2`. They crashed on import → `test_critic_inputs.py::test_collect_happy_path` failed. The design's Non-Goals carve shipped files out ("keep `result` until regenerated"), but that directive conflicts with the mandated helper-signature change for these 3 files (the other 38 concepts use inline forwards and are untouched). **User approved Option A**: convert the 3 files to three-forward (add `generic = generic_reference(...)`; `native, result_1gw = run_native_and_1gw(...)`; 4-arg `print_cas_breakdown`; sensitivity on `generic.params` — behavior-preserving, since the old `result` was overrides-off). `result_1gw` stays 584.5, so the explorer's primary number and the live-vs-static drift check are unperturbed.

### Phase 3 Completion
**Completed:** 2026-05-31

**Changes Made:**
- Flipped the 3 named prompt templates from the interim optional-`ref` form to the mandatory `generic` line (see checkboxes above). All `ref`→`generic`; "four-step"→"three-forward"; contract names + Hard Rules updated.
- Added `tests/fixtures/concept01_model_setup.py` (clean three-forward ARC conversion: spec/model/`generic`/overrides/`native,result_1gw` tuple/4-arg print; includes one `0.70 * generic.costs.cas21` relative override to exercise the generic-frame path). It passes `validate_model_setup_contract(strict)` + `validate_override_registry`, and runs (grepable `LCOE:` headline). Wired `TestThreeForwardIntegration` in `test_validators.py` (acceptance tests 1 & 2 — prompt↔validator agreement).

**Scope finding (pending user decision — raised at Phase 3 checkpoint):**
Three additional prompt files (NOT in the design's Appendix C surface) still carry two-forward/`result` contract language:
1. `model_setup_costingfe_edit.md` — feedback-pass (edit) counterpart of the model-setup prompt; "Preserve the four-step contract", lists the old shape. *Recommend update* (mechanical four-step→three-forward; direct sibling of the file just edited).
2. `config/assessment_checklist.md` §5 — checks "four-step helper form (`result, result_1gw = ...`)" and "`result` reflects real computation". *Recommend update* (would otherwise grade against the wrong contract).
3. `feedback/power_standardization_costingfe.md` — an *obsolete* post-hoc economy-of-scale scaling finding (`_ALPHA=0.6`, `scaled_headline`), explicitly "do NOT add `result_native`/duplicate forward()". This predates and contradicts the two-knob/three-forward contract. *Recommend retire (separate decision), not rename.*

**Resolution (user-approved 2026-05-31):** updated #1 and #2 to the three-forward contract. Investigated #3: it is an **orphaned legacy artifact** (PR #6 "Power standardization") — no code references its filename, no `feedback/` template loader exists in `scripts/lib`, and its `scaled_headline` mechanism appears only in old shipped concept files. Left untouched here; flagged as a safe retire candidate for a separate cleanup item (editing it to three-forward would be nonsensical — it describes a different, obsolete mechanism). Prompt-template set is otherwise clean of two-forward/`result` contract residue.

**Issues Encountered:** none in the defined Phase 3 scope.

### Phase 4 Completion
**Completed:** 2026-05-31

**Changes Made:**
- **Design doc** (`concept-analysis-rework-design.md`): `model_setup.py` section rewritten to the three-forward (five-step) inline example — added the overrides-on `native` forward, renamed the overrides-off forward `result`→`generic`; Override Entry references `generic` and rejects `native`/`result_1gw`; module-level contract → `model/generic/native/result_1gw`; `model_critic` reads the three forward objects; `concept_explorer` contract updated (`result_1gw` primary, `generic`/`native` available).
- **Epic** (`epic_concept_analysis_rework.md`): Future State + Success Criteria → three-forward and `model/generic/native/result_1gw`; Critical Success Factor verified (left — about the unchanged `result_1gw`). Added a superseding annotation to the Item 7 section and forward-pointers to the Item 8 implementation summary and the relative-override-ordering-fix note (the artifacts this corrective item changed). Left Items 1/6 `[x]` retrospectives verbatim as accurate history.
- **Item 8 spec + design**: all "four-step"→"three-forward"; FR-10 (five-step structure with mandatory `generic`), FR-11 (four module names), FR-14 (relative refs `generic`), FR-15/16; helper signature `→ (native, result_1gw)`; design code block gained the `generic` line and `native, result_1gw =` tuple.
- **Item 9 spec**: four-step→three-forward; critic reads the live `generic`/`native`/`result_1gw` objects. Code untouched (the shipped critic works against the converted 01 file — full suite green).
- **Item 10 spec + design**: contract surface → `model/generic/native/result_1gw`; FR-3 fail-loud framing (no `result` fallback target under three-forward); design data-flow diagram → three-forward. Explorer code untouched.
- **Minor**: `validators.py:423` docstring tuple example `result, result_1gw`→`native, result_1gw` (keeps the validators surface clean per acceptance test 6).

**Acceptance test 6 (hygiene gate):** the must-be-clean surface (design doc, helper, validators, Item 8/9/10 `spec.md`, Item 10 `design.md`) is **clean**. Remaining grep hits are: (a) historical `[x]`/retrospective records in the epic (Items 1/6/7/8) — accurate history, not current-contract description, and Appendix C scoped only the forward-looking lines; (b) correct "reads `result_1gw`" usages; (c) Item 8 `plan.md`/`pilot_report.md` implementation logs (outside the spec's acceptance-test-6 surface). Each was read and classified, per the plan's mitigation.

**Issues Encountered:** none. **Deviations:** the epic/Item-8 *retrospective* lines were annotated (superseding pointers) rather than rewritten, to avoid falsifying completed-work history — consistent with the epic's existing "superseded/RESOLVED" convention and Appendix C's forward-looking scope.

---

**Status:** ~~Draft → In Progress →~~ **Complete (2026-05-31)**
