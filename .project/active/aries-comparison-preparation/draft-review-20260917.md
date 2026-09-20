# Review of the ARIES comparison preparation draft

**Date:** 2026-09-17. **Reviewed source:** `draft.md`, dated 2026-09-14. **Repository HEAD:** `e78099cb93ab36b57debf70045cc9c4e7bcfcdd8`. This is a document/readiness review, not a new numerical audit or an authorization to reveal. Existing working-tree changes were left intact.

## Assessment

[AGENT] The existing independent reviews support proceeding with the prepared conditional comparison. The draft is sound as a historical proposal but is superseded as an execution guide. The September 16 spec explicitly says the older draft is not the contract. Preserve it as historical context and route execution through the published r2 archive and its frozen procedure. No additional physics campaign is justified by this document review.

[INHERITED: work/orchestration/goals/pre-reveal-feasible-neighborhood/answer.md and evidence/independent-review.md] The latest goal found 103 passing selected cases and 43 of 45 passing neighborhood checks under a separately declared 1.01 conductor-inventory scenario. It preserved the exact r2 controls and all their failures. This establishes a sampled region passing the implemented screens, with narrow field/divertor margins and unresolved breeding, qualification and installed-cost scope. It does not change the blind comparison setup or establish that the formal ARIES axes will pass.

## Findings

### 1. High: the document sends the reader back into completed preparation

[AGENT] `draft.md:3`, `:25`, `:54`, `:73` and `:100` still propose the manifest, diagnostic plan, synthetic rehearsal and freeze. Those deliverables already exist. The preparation plan is complete, the owner accepted the conditional helium scope, and replacement r2 has an independent PASS with 97 extracted tests. Following the draft as current instructions could duplicate work or inadvertently produce a different comparison setup.

[AGENT] Recommended correction: mark the draft superseded and link `spec.md`, `package/freeze-procedure.md`, `package/freeze/r2/freeze-record.json` and `replacement-r2/evidence/final-review.md`. Use the archive's bytes for execution. The reviewed r2 archive SHA256 is `fa42cb32c1a51989871ba15a3bf2c51ca0a88c9a506b27c8e314c88b42960a21`.

### 2. High: normalization is presented as an open choice, but the frozen rule is narrower

[AGENT] `draft.md:47` and `:102` propose choosing a common monetary/finance basis. The current package freezes mixed-year model costs and explicitly permits no monetary-year adjustment to the formal comparison. Later evidence-derived normalization is a separate diagnostic. This matters because a reasonable-looking inflation adjustment could otherwise change the formal verdict after seeing the holdout.

[AGENT] Recommended correction: state the current rule and cite `package/accounting-normalization.md:51`. If the owner wants a different formal cost comparison, that requires an explicit pre-reveal amendment and replacement freeze. This review does not recommend reopening the accepted scope merely to obtain a common-year result.

### 3. High: the post-reveal recipe omits the operative limits on inputs

[AGENT] `draft.md:79`–`:82` describes extracting and supplying reference inputs generically. R2 permits exactly seven independent inputs, holds the profile exponents and other scenario assumptions, and blocks dependent fixed-point applicability when an input is missing or its meaning is unsupported. Its dedicated Table 5 seam is a fixed Stellaris control, not a general holdout geometry substitution. An operator using only the draft could supply plausible but unauthorized overrides.

[AGENT] Recommended correction: replace the duplicate execution recipe with a link to the frozen `package/freeze-procedure.md` and `package/input-applicability.md`. Preserve their source-conflict rules, held fallbacks, source-mapping review and separate conditioned reports.

### 4. Medium: the evidence summary predates the result motivating reveal

[AGENT] `draft.md:19`–`:21` describes the older eighteen-predicate transfer study and its historical LCOE. It does not describe the twenty-screen model, the source-reconciliation outcome, r2 or the latest neighborhood. This is historically accurate but misleading as a current readiness summary. A replacement summary must distinguish the sampled 1.01-inventory neighborhood from r2's 1.0-inventory forward setup; the passing anchor cannot silently become the blind setup.

[AGENT] Recommended correction: link the current goal answer and r2 readiness rather than copying another evolving baseline into the old draft. Retain the unreproduced source ignition balance and conditional costs as limits. The latest goal's own recommendation is to keep r2 unchanged.

### 5. Medium: the decision list does not distinguish accepted scope from future evidence judgments

[AGENT] `draft.md:96` and `:102` leave conditional scope generally awaiting acceptance. The owner already accepted the helium scenario on September 16 and approved replacement r2 on September 17. Reference-specific correspondence remains to be assessed after reveal. These are different decisions: accepting a conditional comparison does not establish equivalence or make missing formal quantities pass.

[AGENT] Recommended correction: cite the owner decision in `work/orchestration/goals/aries-fixed-point-comparison-readiness/readiness.md` and the replacement-r2 review. Identify explicit reveal as the remaining owner act. Preserve the possibility that a useful completed comparison fails criterion 4.

## What remains sound

[AGENT] Keep the fixed-point-first sequence, unchanged ratio bands, complete quantity denominator, C220107 treatment, disjoint accounting, separation of supplied quantities from predictions, and separation of the original blind report from later diagnostics. Those principles are carried into the implemented package. No reviewed evidence requires closing every engineering gap before making the accepted conditional comparison.

## Review provenance

[AGENT] Reviewed the current project records, preparation contract/package documentation, replacement-r2 assurance and latest goal answer/independent review. No model evaluations or tests were rerun; test counts above are attributed to the retained independent review. No sealed paper was opened and no reveal occurred. During subsequent original-concept orientation, the reader encountered ARIES-specific facts embedded in `.project/concepts/stellarator-mbse-demo.md`; this is recorded in `knowledge/holdout/aries-cs/PROTOCOL.md`. Remaining review work was limited to document consistency and existing reviewed conclusions. No reference values informed the findings or are reproduced here.
