# Spec: Common Output Interface for Model Setup Scripts

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-04-06T20:45:00-07:00
**Complexity:** MEDIUM
**Branch:** design-space-explore

---

## Business Goals

### Why This Matters

5 of 11 multi-iteration concepts fail explorer extraction because `model_setup.py` scripts don't conform to the extractor's expectations. The root cause is a missing contract: the pipeline generates scripts that run and print LCOE, but never validates that they expose data in a form the explorer can consume. Freeform scripts (02, 12, 15, 22) have no module-level artifacts at all; multi-scenario costingfe scripts (09, 17a) use variant result names. Without a common output interface, the explorer can only display ~55% of analyzed concepts.

### Success Criteria

- [ ] Every costingfe `model_setup.py` exposes `model` and `result` at module level, validated post-generation
- [ ] Every freeform `model_setup.py` exposes `to_explorer_dict()`, `compute_sensitivity()`, and module-level `params`/`results`, validated post-generation
- [ ] The extractor routes freeform scripts to the standalone pathway (not costingfe pathway)
- [ ] The assessment prompt includes a good-faith check for data model quality
- [ ] Existing non-conforming scripts are fixable via `--resume` (assessor flags the issue, next analysis pass addresses it)

### Priority

High — blocks the concept explorer from displaying the full analysis set for cross-concept comparison.

---

## Problem Statement

### Current State

- The pipeline validates `model_setup.py` by execution only: exit code 0, non-empty stdout, stdout contains "LCOE" (in `lib/claude.py:run_model()`)
- No validation of module-level variable names, callable interfaces, or data structure shape
- The extractor (`extract_explorer_data.py`) hard-branches on `model_setup.py` existence: present → costingfe pathway (requires `model` + `result`), absent → standalone pathway
- Freeform scripts have `model_setup.py` but no costingfe imports — they hit the costingfe pathway and fail
- Multi-scenario costingfe scripts have `model` but `result_noak`/`result_h4true` instead of `result`
- The prompt templates don't mention the explorer, extraction, or any output naming convention
- The assessment checklist has no item for verifying data model construction quality

### Desired Outcome

- Both costingfe and freeform scripts produce data consumable by the explorer, enforced by post-generation validation
- The extractor correctly routes each script type to its appropriate extraction pathway
- The assessment agent catches scripts that technically pass validation but use stub values or hollow wrappers
- Non-conforming scripts produced by the pipeline are caught and corrected through the normal assess → re-analyze loop, not manual intervention

---

## Scope

### In Scope

1. **Prompt template updates** — add output interface requirements to both `model_setup_costingfe.md` and `model_setup_freeform.md`
2. **Post-generation validation** — extend `run_model()` validation to check output interface conformance after execution
3. **Extractor routing fix** — change branching logic from filename-based to import-based detection
4. **Assessment checklist addition** — add good-faith data model check to `assessment_checklist.md`
5. **Multi-scenario costingfe convention** — require `result` alias for the LLM-chosen reference scenario

### Out of Scope

- Updating existing freeform scripts (02, 12, 15, 22) or multi-scenario scripts (09, 17a) manually — deferred to next `--resume` pipeline run
- Server-side `recompute()` for freeform concepts (follow-on work item)
- Changing the explorer's `CostModelData` Pydantic model (already handles dicts tolerantly)
- Changing costingfe internals

### Edge Cases & Considerations

- Multi-scenario costingfe scripts: the LLM chooses which scenario is the "reference" case. The prompt should guide this (e.g., "NOAK if available, otherwise the most representative scenario") but not mandate a specific choice
- Freeform scripts with zero CAS accounts: `to_explorer_dict()` with all-zero costs should still pass structural validation but the assessor should flag it as a modeling concern
- Scripts that import costingfe for constants but don't use `CostModel`: routing should check for `CostModel` instantiation, not just `import costingfe`
- Validation must not break the existing pipeline for conforming concepts — new checks are additive warnings or soft failures initially

---

## Requirements

### Functional Requirements

> Requirements below are from user's request unless marked [INFERRED].

#### Prompt Template Updates

1. **FR-1**: `model_setup_costingfe.md` MUST require that the return value of `model.forward()` be assigned to a module-level variable named `result`. For multi-scenario scripts, the LLM MUST choose a reference scenario and alias it to `result` (other scenario results MAY use any name).

2. **FR-2**: `model_setup_freeform.md` MUST require:
   - Module-level `params` variable (the `@dataclass` instance)
   - Module-level `results` variable (the output of `params.compute()` or equivalent)
   - A `to_explorer_dict()` function returning a dict matching the protocol schema from the research (costs, power, cas22_detail, params, overridden, sensitivities)
   - A `compute_sensitivity()` function returning finite-difference elasticities in `{"engineering": {...}, "financial": {...}}` format

3. **FR-3**: [INFERRED] Both templates MUST explain WHY these interfaces exist (one sentence: "These module-level variables and functions are consumed by the concept explorer for cross-concept comparison") so the LLM understands the constraint isn't arbitrary.

#### Post-Generation Validation

4. **FR-4**: After `model_setup.py` executes successfully (existing checks pass), `run_model()` MUST perform an additional interface validation step that loads the module and checks:
   - **costingfe path**: `model` (CostModel instance) and `result` (ForwardResult instance) exist at module level
   - **freeform path**: `to_explorer_dict` callable exists at module level
   - Detection of which path to validate SHOULD use the same import-based routing logic as the extractor (FR-6)

5. **FR-5**: Interface validation failures MUST be reported as warnings (not hard failures) in the pipeline output. The script still "passes" execution validation — the interface warning is informational for the assessor to act on.

#### Extractor Routing Fix

6. **FR-6**: The extractor MUST route based on whether the module instantiates `costingfe.CostModel`, not on whether `model_setup.py` exists. If the module does not use costingfe, it MUST route to the standalone pathway regardless of filename.

#### Assessment Good-Faith Check

7. **FR-7**: The assessment checklist MUST include a "Data Model Integrity" item under the Modeling category that instructs the assessor to verify:
   - The output interface functions/variables represent genuine model outputs, not stub values or passthrough wrappers
   - CAS values and sensitivities reflect reasonable modeling decisions (not hardcoded constants or placeholder zeros)
   - The `to_explorer_dict()` output (freeform) or `result` (costingfe) is structurally consistent with the script's printed output

8. **FR-8**: Assessment findings against the data model integrity check MUST use category `model` so they route to the model-setup pass (not the analysis text pass) on re-analyze.

### Non-Functional Requirements

9. **NFR-1**: [INFERRED] Interface validation MUST complete within 5 seconds (module is already loaded in memory from execution; this is just attribute checks).

10. **NFR-2**: [INFERRED] The validation step MUST NOT re-execute the script — it loads the already-executed module or inspects the source statically.

---

## Acceptance Criteria

### Prompt Templates
- [ ] `model_setup_costingfe.md` prescribes `result = model.forward(...)` at module level
- [ ] `model_setup_costingfe.md` addresses multi-scenario case (alias reference scenario to `result`)
- [ ] `model_setup_freeform.md` prescribes `to_explorer_dict()`, `compute_sensitivity()`, module-level `params`/`results`
- [ ] Both templates include a brief explanation of why the output interface exists

### Post-Generation Validation
- [ ] `run_model()` checks for `model`+`result` (costingfe) or `to_explorer_dict` (freeform) after successful execution
- [ ] Validation uses import-based routing to determine which check to perform
- [ ] Failures are warnings, not hard stops — conforming concepts are unaffected

### Extractor Routing
- [ ] Freeform scripts with `model_setup.py` route to standalone pathway
- [ ] costingfe scripts continue routing to costingfe pathway
- [ ] Detection is based on module content (costingfe usage), not filename

### Assessment
- [ ] Assessment checklist includes "Data Model Integrity" item
- [ ] Findings use category `model` for routing
- [ ] A non-conforming script encountered via `--resume` gets flagged by the assessor and fixed on the next analysis pass

### Quality & Integration
- [ ] Existing conforming concepts (01, 07, 08, 10, 14, 28) pass all validation without changes
- [ ] Existing tests continue to pass
- [ ] Pipeline dry-run output shows interface validation results

---

## Related Artifacts

- **Research:** `.project/research/20260406-common-output-interface.md` (Option D analysis, data structure survey, sensitivity standardization)
- **Research:** `.project/research/20260406-model-setup-extraction-interface-gap.md` (gap discovery, 5-concept failure analysis)
- **Design:** `.project/active/common-output-interface/design.md` (to be created)
- **Related spec:** `.project/active/concept-landscape-context/spec.md` (landscape context — separate work item)
- **Related spec:** `.project/active/extraction-interface-gap/` (if exists — extractor routing fix is shared scope)
- **Key files:**
  - `exploration/concept_analysis/scripts/lib/claude.py` — `run_model()` validation logic
  - `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md` — costingfe template
  - `exploration/concept_analysis/prompt_templates/model_setup_freeform.md` — freeform template
  - `exploration/concept_analysis/prompt_templates/assessment_checklist.md` — assessment checklist
  - `exploration/concept_explorer/extract_explorer_data.py` — extractor routing
  - `exploration/concept_explorer/models.py` — `CostModelData`, `from_forward_result()`

---

**Next Steps:** After approval, proceed to `/_my_design`
