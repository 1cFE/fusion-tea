# Product Backlog

Prioritized list of epics and features.

**Last Updated**: 2026-05-28

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
| Concept-Analysis Pipeline Rework | P0 | Draft | 2026-05-30 | 11 items, ~10–14d. Phase 0 throwaway probes (prototype + stability + critic acuity) before plumbing. Two-layer split, two-knob 1 GWe NOAK, override registry, standalone `model_critic`. File: `epic_concept_analysis_rework.md`. |

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
| Refresh synthesis.md for 13 standardized concepts | P2 | `synthesis.md` prose still cites pre-standardization availability + LCOE numbers; iteration loop flagged most with `Stale: true` in frontmatter. Refresh via `uv run agentic-mbse … synthesize <concept>` (or equivalent in run_analysis.py) once other concept-analysis fixes are batched. Spending tokens on this alone is wasteful — bundle with the next batch synthesis pass. |
| Investigate 20a capital-side availability coupling | P3 | After the availability standardization, concept 20a's overnight cost moved ~+3.5% from a 2.3% availability drop. Pure 1/availability should leave overnight cost unchanged. Either a costingfe IDC/escalation behavior or a 20a-specific override. Add a perturbation test that sweeps availability ±5% and prints overnight cost — if a real coupling, document; if a bug in 20a's overrides, fix. Other concepts may have the same silent issue. |
| Non-D-T availability policy + standardize | P2 | The availability standardization script filtered to D-T. Four non-D-T concepts (`04` p-B11 pulsed, `06` p-B11 steady mirror, `08` D-He³ pulsed FRC, `23` p-B11 pulsed) were skipped. The current `scoring_framework.md` table says "D-D / D-³He / p-¹¹B → 0.85" with reasoning "Same MCF basis", which implies non-D-T should be 0.85 regardless of pulsed/steady. The `canonical_availability` helper currently returns 0.75 for any pulsed family regardless of fuel — contradicts the policy text. Decide actual policy, update helper, run the standardize pass for these 4 concepts. |
| Concept 09 dual-site availability refactor | P3 | `09-qi-stellarator-hts/model_setup.py` has availability in two coupled sites: `_SHARED[availability]=0.88` (costingfe forward call, line 205) and `_AVAILABILITY_BASE=0.88` (custom replacement-cost calc, line 173 — comment says "matches _SHARED below"). Pre-marked as `# DEVIATION:` so the standardize script skipped 09. Either (a) refactor to a single `AVAILABILITY` constant used in both sites and move to canonical 0.85, or (b) promote to Tier-A retain at 0.88 if `helios-stellarator-comparison.md` 88% citation qualifies as a sourced commitment. |
| Audit script for "DEFAULT" labels vs actual values | P3 | Walk every concept's `model_setup.py`, parse all kwargs, flag any value with a `# DEFAULT` comment whose actual value doesn't match the costingfe library default (or the canonical_eta_th/canonical_availability lookup). Report-only, no auto-fix. ~30-line script parallel in shape to `standardize_eta_th.py`. Surfaces silent drift before it becomes a policy dispute. Motivated by inflation_rate=0.0245 case in `.project/research/20260517-081444_model-setup-inconsistencies.md` §2. |

### PR #33 (data availability refresh) follow-ups (2026-05-28)

| Item | Priority | Description |
|------|----------|-------------|
| Refresh deployed Score Explorer UI after PR #33 | P2 | After PR #33 merges, mirror `tools/score_explorer/{index.html,data/concepts.json,data/weights.json}` → `docs/score-explorer/` and commit + push to main. Same straight-copy pattern as PR #28 (initial deploy) and PR #29 (TF correction refresh). Without this, the live URL at https://1cfe.github.io/fusion-tea/score-explorer/ will continue to show the pre-#32 data availability scores even though `tools/score_explorer/data/concepts.json` already has the refreshed values. Single commit, byte-level mirror of three files, ~5 min. |

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
