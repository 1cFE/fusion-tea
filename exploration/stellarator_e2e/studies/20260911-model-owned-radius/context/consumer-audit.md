# Audit: Current study consumers for model-owned major radius (T-024)

**Verdict:** Certify

**Audited:** 2026-09-11 PDT / 2026-09-12 UTC

**Branch:** `test/codex-native-skills`

**Commit:** `f5737119a65ef8dd9306589e499260c127e97bb7`; implementation review range `f07015bb..HEAD`, including parent corrections `dbba6262` and `56b06a58`.

## The Point

The audited model has one operational plant radius, but its current independent oracle and study consumers still represented a second magnet radius. A normal R-only proposal therefore needed consumer-side coordination to describe the intended plant. This migration must let the native model own that connection, carry the same operational radius into the independent arithmetic, refuse the retired input, and reproduce current metadata without changing the audited model, physical assumptions, financial equations or historical evidence. The complete baseline and off-design frozen controls are the numerical reference; a baseline-only agreement would miss the original defect.

## Summary

The current migration meets SC-1–4 within its stated scope. Independent execution reproduced 233 targeted passes, 580 broad-replay passes and 97 individually matched inherited historical failures, with four deliberate write-safety deselections. Baseline and ordinary R-only14 match the frozen controls across all 158 native scalars and nineteen native responses; every one of the 141 declared oracle channels agrees within the existing tolerance.

This certificate covers current consumer behavior and preservation, not full process compliance or physical validity. The original seven-file quarantine hashing violation remains recorded; the corrected guard was independently verified without reopening quarantined sources.

## Product Judgment

**This is the right bounded piece of work.** The fresh product-lens ledger is **DISPOSED**, with no unresolved owner/HARD contradiction. The full independent verdict and all seven smell assessments are appended in [product-lens.md](product-lens.md); fresh-agent provenance and the oracle written before WORK inspection are retained under [audit-evidence/](audit-evidence/). No earlier item ledger or linked Epic gate was present.

Two structural smells fired and are explicitly disposed here:

- **audit-F1 — correctness depends on downstream knowledge of an internal representation.** New kept tests load coverage and executable verification from active PM paths (`tests/study/test_major_radius.py:49`, `:80`, `:115`; `implementation/check_controls.py:20`). Archiving either item will break those reads. **Disposition: deferred to completion preparation, before either affected path moves.** The authorized task certifies the current retained package and explicitly excludes close/archive; the active paths exist and all affected tests executed. This does not certify archival readiness. Move the reusable test helper and frozen test data into a durable test home, or otherwise resolve the dependency, before closing the items; no such fix was made here.
- **audit-F2 — two representations must be manually kept synchronized.** The handwritten oracle remains an arithmetic mirror. **Disposition: accepted for the existing demo scope**, re-derived against ADR-0010's separately graded carry ruling and arithmetic-independence rationale. Its value is independent computation at the same plant inputs; this audit checks all mapped channels at an off-design point as well as baseline. No permanent cross-concept mirror or enlarged supported interface is approved.

The duplicated graph expectations were examined separately. `implementation/refresh_metadata.py:66` writes JSON fixtures and `:75` derives the embedded `FIXTURE_CONTRACT` from the same native report. They reproduce together and do not require manual synchronization when that producer is used. They supply continuity/reproduction evidence, not two independent proofs of correctness. The independent arithmetic and immutable WI-051 numerical controls supply the separate evidence. Synthetic generic-tie tests do not introduce an alternate current physical route or exempt equal/zero retired inputs.

## Findings

### Plan completion

The implemented phase is verified, subject to the recorded process incident and certification limits below. Current oracle/adapter/route changes, native metadata reproduction, ordinary and adverse runtime controls, generic tie preservation, historical failure classification and permitted-surface preservation all have independent evidence. No placeholder implementation or silent numerical fallback was found in the changed production code.

The phase's original preservation step did execute forbidden byte reads. Its checked box records that the preservation work occurred; it is not a certificate that the no-read rule was obeyed. The existing incident note remains essential. Only the four verified SC checkboxes and independent audit-gate checkbox are newly marked; no goal, epic, CURRENT_WORK or item status text was edited.

### Spec conformance

| Criterion | Result and evidence |
|---|---|
| SC-1 | Met under the corrected scope. `verify_stellaris.py:111`, `:548`, `:553`, `:560`, `:566`, `:673` use plant R for sustainment, axis field, bore factor, stored energy, winding and procurement. Fixed anchors remain unchanged. `oracle_entry.py:467` rejects the retired flat key before conversion; `:490` rejects the local alias before updating globals; direct `compute()` refuses the alias at `verify_stellaris.py:510`. Kept tests exercise alone/equal/conflicting/zero/non-convertible flat submissions and local aliases. Independent AST extraction of the entering mapping verifies exactly 100→99, the sole retired-key removal and unchanged surviving mappings. All 147 unmapped native inputs still refuse. |
| SC-2 | Met. `study_route.py:89` constructs no radius tie/injection; `:101` rejects retired proposals before conversion, and the current manifest has no ties or retired baseline key. Actual `{}` and `{R:14}` controls match all 158 frozen scalars, including both LCOEs. All 141 oracle channels compare individually, with worst relative deviation `2.209043823690201e-16`. The native response maps match all nineteen frozen responses exactly, including eighteen authored verdicts and the aggregate. Current verification rederives all eighteen predicates. Independent geometry ratios and five invalid unified-radius cases pass; publication refuses failed cases. |
| SC-3 | Met for current consumers. The inspected native fingerprint/baseline/indicator APIs reproduce the manifest, five graph fixtures and embedded graph expectations byte-for-byte in isolated output copies. Measured census is 246 inputs, eighteen constraints and 28 feature-reference operands; R reaches 87 modules/165 channels. Targeted tests pass 233/233. Broad replay passes 580 and reproduces precisely the 97 inherited historical failures; all 95 author-reported restored tests pass independently. Current missing/altered bindings, channels, verdicts and publication failure paths execute in that replay. |
| SC-4 | Met for the preservation and bounded-audit contract. All 246 generated package files exactly match WI-051's audited final manifest, whose bytes also match `641c1051`. Protected model/direct-caller/model-test/shared-tool/history/WI-051 evidence surfaces remain unchanged. The sole difference from the implementation's 14,363-file permitted baseline is CURRENT_WORK, already modified at audit entry and preserved. No integration, pin, committed study, source adoption, model regeneration or close was performed. ANNEX documents model-owned radius, unsupported coverage and retained engineering/financial limits. Full quarantine compliance is expressly not certified. |

**Parent correction `dbba6262`: verified.** The initial full-adapter demand was agent-authored and contradicted the measured inherited interface. The correction preserves all previously supported mappings rather than silently expanding or narrowing supported behavior. `audit-evidence/independent-checks.json` derives the old map directly from `f07015bb`, independently of the author's coverage fixture. The original failing full-coverage test and failed logs remain unchanged. The 147 unsupported inputs and seventeen independent-oracle output omissions are limitations, not resolved coverage defects.

**Frozen-control authority: verified, with the existing chronology caveat.** The four frozen control files match their recorded digests and entering git objects. `expectations.json` matches the handoff digest `a16c0731e81230060d6c74d0cc93189445ba7f4c06bb002ab2338fe07b25648a`. No expected numbers were regenerated. WI-051's handoff states that the extra raw representation was captured after prototype generation and the original helper had no successful entering baseline; this audit does not reverse those disclosures.

### Design conformance

Implementation follows the current-consumer-only architecture. Five former magnet operands and sustainment now use plant R in the independent oracle; reusable model formals and fixed reference anchors remain unchanged. The native probe independently checks all nine plant-R edges, exact baseline report/response maps, off-design controls and adverse component behavior. Metadata refresh uses existing producers and was evaluated through isolated write redirection rather than mutating current fixtures during audit.

The measured semantic identity is `15ed665c374729a984f29fa753f444677805939ffb195933419b3489debbd47e`; executable identity is `cbdb2a365f39c7863a038a48ba10356a783d3af3ab61b020c8bbba50cfcab37c`; indicator digest is `609e6cca0a4f329e834b52369a425541ca167bfdfe8608879d900a27ccedf06d`. No identity was promoted to an integration candidate or historical pin.

### Code integrity

**Quarantine incident — verified violation, corrected recurrence path.** The retained original helper `implementation/protect-before-quarantine-fix.py:19` enumerates tracked paths without excluding quarantine, then `:32` reads bytes for SHA256. Existing original metadata contains seven quarantined entries. This was unauthorized source-byte access even though only opaque digest metadata was emitted. The inspected helper and consumer diff show no extraction of scientific content or use of that content in radius equations; this limited observation is not proof about every prior action or reasoning step.

The parent correction excludes quarantine at `implementation/protect.py:24`, before the byte read at `:33`, and filters old metadata at `:43`. A synthetic test verified the ordering before broad permitted reads. Actual corrected-helper execution then made 14,363 permitted reads and zero quarantine attempts under a resolved-path read guard, with writes redirected to `audit-evidence/guard-real/`. The old helper was never executed by this audit and quarantined source files were not reopened. Original helper, manifests and failed evidence remain intact. **Disposition:** corrected for this permitted-surface verification; the historical violation remains, with no claim of full stage quarantine compliance or new source authority.

**Historical failures — retained, not excused by unchanged source alone.** `audit-evidence/replay-comparison.json` compares each of 97 current failures with both retained entering and author replay XML: identical node, failure status and exact failure message. These are the historical publication/exporter failures, not new radius deltas. All 95 reported restorations were rerun and passed. Old-revision execution was not repeated; retained XML is the historical comparison source.

**Helper writes — bounded during audit.** `implementation/refresh_metadata.py:71` and `:97` rewrite repository fixtures/test code despite receiving a work-directory argument. Audit used `metadata_isolated.py` to redirect every known metadata target to new copies and reject other text writes. All seven outputs reproduce exactly. This caller is a metadata producer, not a read-only check; future users must retain equivalent isolation or byte-preservation controls.

## Certification

Certify SC-1–4 for the current bounded migration, with the product-lens dispositions above. Evidence includes actual baseline/R14 native and oracle runs, independent mapping/ratio/control checks, exact native metadata reproduction, negative/publication controls, per-node replay comparison and permitted-file/package preservation. [commands.md](audit-evidence/commands.md) records invocations and outcomes; the original failed audit preservation attempt is retained separately.

The baseline primary/1cfe-form LCOEs are `224.26923288439` / `220.0125640803369`; R14 is `250.89832244487582` / `246.2018206142481`. Baseline violates divertor heat; R14 also violates wall load, sustainment and loop capacity. Neither is a feasible-plant certification. The fixed-target divertor constraint, radius-scaled reported shadow, held efficiencies, installed-capacity costing, engineering scaling/omissions, financial/calendar assumptions and original F07 remain unresolved at their existing scope. Native component probes reproduce negative peak fields and equality division failures; they establish no general physical domain.

**Not checked:** Integration/regeneration/candidate gates, model-validation batteries, primary-worktree state, committed study execution, physical-source adequacy, finance validity, broad arbitrary sweeps, the 147 unsupported oracle inputs, independent computation of the seventeen omitted scalar channels, or archival readiness. Four broad-replay nodes were deselected to avoid default repository output writes, historical SQLite mutation and temporary cleanliness probes; they are named in the command record. No global-green or full quarantine-compliance claim is made. No quarantined scientific content was inspected. Existing historical-failure causes were compared and localized, not repaired. WI-051 production/audit evidence remains protected and is not re-certified as a new model audit.

**Next required action:** Parent reviews this bounded certificate and incident disclosure before any separately authorized integration work. Resolve audit-F1's active-path dependency before either affected item is archived. This audit performs neither action.
