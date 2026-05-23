# Product Backlog

Prioritized list of epics and features.

**Last Updated**: 2026-05-17

---

## Priority Legend

- **P0**: Critical - Blocking, do immediately
- **P1**: High - Important, do soon
- **P2**: Medium - Valuable, do when possible
- **P3**: Low - Nice to have, do eventually

---

## In Progress

| Epic | Priority | Status | Started | Notes |
|------|----------|--------|---------|-------|
| Knowledge Database Integration | P1 | In Progress | 2026-02-06 | Items 1-3 complete, pipeline proven. Items 4-5 archived (blocked on user action, infrastructure works). |
| Source Extraction Fix & Re-extraction | P0 | Draft | 2026-03-29 | HTML extraction broken (tables, images, quality). Fix upstream → re-extract → clean .orig.md. |
| Pipeline Hardening (ad-hoc) | P0 | **Complete 2026-04-11** | 2026-04-05 | 6 items archived (pipeline-hardening, output-validation-retry, concept-landscape-context, orig-md-research, feedback-routing-fix, explorer-merge). Analysis pipeline now safe for batch runs. |
| Ontology v3 Migration | P0 | In Progress | 2026-05-17 | 6 items, ~5.5–8d. Item 1 complete (PR #15 merged 2026-05-17). Next: Item 2 — branch off `main`, merge `fix/concept-renumbering-robustness`. File: `epic_ontology_v3_migration.md`. |

---

## P1 - High Priority

### Knowledge Database Integration

**Priority**: P1
**Effort**: ~4-5 days (4 items + ongoing)
**Status**: In Progress (infrastructure complete)

Zotero → pyzotero → agentic-mbse extract → SOURCE_INDEX.md pipeline. Batch automation script works. 6+ sources ingested. Ready to scale when new sources are needed.

**Items**:
- [x] Item 1: Zotero API De-Risk (0.5 day) - Complete 2026-02-06
- [x] Item 2: Single-Source E2E Pipeline (1 day) - Complete 2026-02-06
- [x] Item 3: Ingestion Automation Script (1.5 days) - Complete 2026-02-09
- [~] Item 4: First Corpus Ingestion — Abandoned (superseded by IFE source ingestion)
- [x] Item 5: Extraction Pipeline Integration — Complete 2026-02-27 (script modernized for v4 pipeline)

**File**: `epic-knowledge-database-integration.md`

---

## Active Work Items

| Item | Priority | Status | Location |
|------|----------|--------|----------|
| Batch Pipeline Run | P0 | Not started; unblocked by pipeline-hardening | `.project/active/batch-pipeline-run/` |
| Loop Dry-Run Symmetry | P2 | Spec only (2026-04-10); LOW complexity follow-up | `.project/active/loop-dry-run-symmetry/` |
| Traceability System | P1 | Spec + plan complete, awaiting prioritization | `.project/active/traceability-system/` |

### Availability-standardization follow-ups (2026-05-17)

From the availability standardization (commit `45c9db5`); details in `.project/research/20260517-availability-policy-affected-concepts.md`.

| Item | Priority | Description |
|------|----------|-------------|
| Refresh synthesis.md for standardized concepts (availability + eta_th-fix + pulsed-conversion-refactor) | P2 | `synthesis.md` prose still cites pre-standardization availability + LCOE numbers across three waves: (a) 13 concepts from the 2026-05-17 availability standardization; (b) 17 concepts from the 2026-05-22 eta_th-double-count-fix (issue #30) — IDs: 01, 05, 07, 09, 11, 17a, 20a, 20b, 21, 23, 25, 28, 29, 30, 33, 36, 39; (c) 2 concepts from the 2026-05-23 pulsed-conversion-refactor — IDs: 08 (FRC INDUCTIVE_DEC), 31 (laser ICF THERMAL hybrid). For (c), synthesize runs were attempted on 2026-05-23 and both timed out at 900s (the same `claude -p` timeout described below); prior synth files were restored from git and remain stale relative to the new model wiring until this batch runs. Most are Review-Status-gated out of automatic synthesize. Refresh via `uv run python exploration/concept_analysis/scripts/run_analysis.py synthesize <ids> --force --skip-review-gate` once other concept-analysis fixes are batched. **Tooling note (2026-05-22)**: an attempted single-concept synth regen (concept 11) timed out at 900s and removed the partial frontmatter-only file; either bump synthesize timeout (`run_analysis.py` calls `claude -p` with a 900s wall-clock) or investigate why concept 11's synthesis prompt now takes >15min on Sonnet. Spending tokens on this alone is wasteful — bundle with the next batch synthesis pass. |
| Investigate 20a capital-side availability coupling | P3 | After the availability standardization, concept 20a's overnight cost moved ~+3.5% from a 2.3% availability drop. Pure 1/availability should leave overnight cost unchanged. Either a costingfe IDC/escalation behavior or a 20a-specific override. Add a perturbation test that sweeps availability ±5% and prints overnight cost — if a real coupling, document; if a bug in 20a's overrides, fix. Other concepts may have the same silent issue. |
| Non-D-T availability policy + standardize | P2 | The availability standardization script filtered to D-T. Four non-D-T concepts (`04` p-B11 pulsed, `06` p-B11 steady mirror, `08` D-He³ pulsed FRC, `23` p-B11 pulsed) were skipped. The current `scoring_framework.md` table says "D-D / D-³He / p-¹¹B → 0.85" with reasoning "Same MCF basis", which implies non-D-T should be 0.85 regardless of pulsed/steady. The `canonical_availability` helper currently returns 0.75 for any pulsed family regardless of fuel — contradicts the policy text. Decide actual policy, update helper, run the standardize pass for these 4 concepts. |
| Concept 09 dual-site availability refactor | P3 | `09-qi-stellarator-hts/model_setup.py` has availability in two coupled sites: `_SHARED[availability]=0.88` (costingfe forward call, line 205) and `_AVAILABILITY_BASE=0.88` (custom replacement-cost calc, line 173 — comment says "matches _SHARED below"). Pre-marked as `# DEVIATION:` so the standardize script skipped 09. Either (a) refactor to a single `AVAILABILITY` constant used in both sites and move to canonical 0.85, or (b) promote to Tier-A retain at 0.88 if `helios-stellarator-comparison.md` 88% citation qualifies as a sourced commitment. |
| Audit script for "DEFAULT" labels vs actual values | P3 | Walk every concept's `model_setup.py`, parse all kwargs, flag any value with a `# DEFAULT` comment whose actual value doesn't match the costingfe library default (or the canonical_eta_th/canonical_availability lookup). Report-only, no auto-fix. ~30-line script parallel in shape to `standardize_eta_th.py`. Surfaces silent drift before it becomes a policy dispute. Motivated by inflation_rate=0.0245 case in `.project/research/20260517-081444_model-setup-inconsistencies.md` §2. |
| ~~Structural refactor of 08 + 31 to use `pulsed_conversion=INDUCTIVE_DEC`~~ ✅ DONE 2026-05-22 | ~~P1~~ | Landed via `.project/active/pulsed-conversion-refactor-08-31/`. 08 → `INDUCTIVE_DEC` (eta_dec=0.90, eta_th=0). 31 → `THERMAL` hybrid (eta_th=0.44, eta_de=0.44, f_dec=0.30) via `pulsed_thermal_forward` native f_dec/eta_de support. All conversion-related DEVIATIONs removed. Costingfe API gap surfaced as separate item (next row). |
| costingfe: add `eta_de` + `f_dec` to PULSED family auto-diff sensitivity list | P3 | `costingfe/model.py:932-941` lists `eta_dec` + `f_pdv` (INDUCTIVE_DEC params) for the PULSED family elasticity table but not `eta_de` + `f_dec` (used when PULSED concepts call `pulsed_thermal_forward` with hybrid wiring). STEADY_STATE family at line 897 does include `eta_de`. Surfaced by concept 31 (first PULSED concept to use the hybrid `pulsed_thermal_forward(f_dec, eta_de, ...)` path) — its engineering elasticity table omits eta_de despite the forward physics being live. One-line addition. Forward physics is unaffected; this only completes the sensitivity-report coverage. Logged from `.project/active/pulsed-conversion-refactor-08-31/` Phase 3 root-cause investigation. |
| `f_dec` audit on the 8 issue-#30 concepts | P2 | Per-concept `f_dec` values were chosen by authors when `eta_de` meant "overall plant blend." Now that PR #31 has restored DEC-channel-only semantics, those `f_dec` values may be miscalibrated — some authors may have tuned `f_dec` against the wrong `eta_de` meaning. Concept 11 is a known counterexample (always wired correctly, hence the smaller-than-expected +9% delta); the other 7 (06, 08, 19, 23, 24, 31, 39) have not been audited. **Sequence after the PR #31 cleanup techniques are proven**: for each of the 8 concepts, check whether `f_dec` is sourced from device physics (D-T 20% alpha fraction, charged-particle fraction of P_fus, etc.) or appears to be a tuning knob; if the latter, flag for re-derivation. Reuse the same `analyze --feedback --add-passes 1` pattern from `.project/active/eta-th-pr31-cleanup/`. Issue #30 explicitly placed `f_dec` out of scope so this is a separate work item; potential impact is non-trivial LCOE corrections on top of PR #31's deltas. |
| End-to-end LCOE smoke-test on PR #31 big movers | P2 | PR #31's Phase-1 hand-calc verified concept 11 against the predicted band, but the other 16 LCOE deltas (including +31% on concept 39 and +4% on concept 30 laser-icf-nif-commercialization) were not independently verified — they're derived outputs trusted because canonical changed and costingfe computed something. Risk: a sign-error or unit-mismatch in costingfe's `p_dee = f_dec * eta_de * p_transport` calculation would produce plausible-looking but wrong numbers, with no test to catch it. **Add a small smoke test** that hand-derives expected `p_et = eta_th * p_th + f_dec * eta_de * p_transport` from the canonical and confirms it matches `model_output.txt` within tolerance for concepts 39, 17a, 30 (top-3 deltas). ~30 minutes scoping; catches an entire class of "math wrong, test passed" failure for future canonical changes. |
| Revert standardizer damage on concepts 19 + 24 (custom physics) | P1 | `standardize_eta_th.py` in PR #31 rewrote dataclass field defaults `eta_dec: float = X` on concepts 19 (orbital-levitated-dipole) and 24 (dense-plasma-focus) because the regex doesn't distinguish costingfe kwargs from custom dataclass fields. Both concepts use custom physics (no `costingfe.forward()` call) so the canonical doesn't semantically apply. Damage: 19 central bumped 0.57 → 0.70 (now ABOVE the LO/HI sweep at 0.57/0.65, sweep contrast inverted); 24 central bumped 0.85 → 0.70 (now BELOW the LO/HI sweep at 0.80/0.85, sweep contrast inverted). Fix sequence: (a) land custom-physics detector in standardizer + verifier per `.project/active/eta-th-pr31-cleanup/` FR-8/FR-9, (b) run `analyze --feedback --add-passes 1` on 19 + 24 with feedback instructing the agent to restore central `eta_dec` to the file's own well-cited source value (19: 0.57 per "50–65% upper bound for 14.7 MeV protons"; 24: 0.85 per LPPFusion energy-recovery-linac analogy), preserving the `# standardized from X` annotation as historical context, (c) confirm sweep contrasts are coherent post-revert. Verifier flagged both as `narrative_contradiction` in the PR #31 sweep but the root cause is the standardizer mis-applying canonical to non-canonical files. |
| Revisit sensitivity-sweep intent + audit for flattening | P2 | The `standardize_*.py` scripts use line-anchored regex that doesn't distinguish `model.forward(...)` canonical kwargs from values inside scenario/sensitivity sweep dicts (e.g. `"Conservative": Params(thermal_efficiency=0.32)`, `"Optimistic": Params(thermal_efficiency=0.40)`). Known damage: 27-polywell `model_setup.py` lines 947/963 had sweep values 0.38/0.45 flattened to canonical 0.35 by `standardize_eta_th.py`, collapsing the Conservative/Optimistic contrast — its `synthesis.md` now presents three "scenarios" with effectively identical inputs. Likely other concepts affected (15-sheared-flow, 35-polomac, 02-acoustic so far not flattened but vulnerable). Tasks: (a) write up the *intent* of these sweep blocks (are they meant to feed multi-run sensitivity output? scenario comparison tables in synthesis? something else?), (b) audit all `analyses/*/model_setup.py` for sweep-block patterns and check whether prior `standardize_*.py --apply` runs flattened any of them (`grep` for `# standardized from` inside dict-literal or scenario-named blocks), (c) decide policy — either teach the standardizer to skip sweep blocks (AST-aware or scenario-name heuristic) or require sweep blocks to carry `# DEVIATION: scenario sweep` annotations. Motivated by `.project/active/eta_th-double-count-fix/` Phase 1 audit. |

---

## Completed

| Epic | Completed | Duration | Notes |
|------|-----------|----------|-------|
| Visualization POC Sprint | 2026-01-19 | 2 days | Full Cytoscape.js pipeline, 23+ tests |
| Cost Modeling Patterns De-Risking | 2026-03-06 | ~2 months | Learnings handed off to sysml-codegen, all changes implemented |
| End-to-End Pipeline De-Risking | 2026-03-06 | ~5 weeks | Solar+battery pipeline proven, codegen enhancements in open PR |
| Full Workflow Demo | 2026-03-06 | 5 days | Interactive HTML explainer + IFE modeling demo |

---

## Ideas / Future Considerations

- MFE concept modeling (next stage after IFE)
- Cross-concept comparison tooling
- Traceability audit automation (blocked on traceability-system implementation)
