# Product Backlog

Prioritized list of epics and features.

**Last Updated**: 2026-08-21

---

## Priority Legend

- **P0**: Critical - Blocking, do immediately
- **P1**: High - Important, do soon
- **P2**: Medium - Valuable, do when possible
- **P3**: Low - Nice to have, do eventually

---

## Flagged — don't lose

| Item | Priority | Description |
|------|----------|-------------|
| Test cleanup: one-plant assumptions and migration-era asserts | P1 | Reshape `tests/models/test_self_binding_replacement.py`: it generates the *whole* `models/` tree and hard-codes the IFE plant's census (23 entry points / 18 design attributes, the 11 renamed keys, the 7 un-renamed). Split into one census per design family (IFE now, MFE after the stellarator migration), each generated from its own tree or subset; keep the regression-guard asserts (zero refusals, live == snapshot, mutation every-and-only), drop or quarantine the one-time D-5 rename asserts. While there, sweep `tests/` for other tests that encode "models/ holds one plant" or pin a toolchain-migration moment rather than a behavior. Surfaced 2026-08-21 by the stellarator-demo reconciliation research (`.project/research/20260820-221835_stellarator-demo-reconciliation-plan.md` § 2). Do it in the migration PR, not before — the MFE census needs a package that actually generates. |
| Revert the six scalar-function rewrites in the stellarator model once codegen admits them | P2 | `[OWNER 2026-08-21]` chose "rewrite now, file upstream, revert later" for the six `sqrt`/`max`/`min`/`floor` sites (`models/library/analyses/mfe_plasma_scaling.sysml:194`, `mfe_account_costs.sysml:816, 820, 830-832`) that block regeneration on the pinned codegen. When `[SCALAR-FUNCTION-VOCABULARY]` (sysml-codegen `BACKLOG.md:36-41`) lands and fusion-tea's codegen pin moves past it, restore the original function calls and regenerate. Exact pre-rewrite text is in git at the migration PR's parent. |
| `uv.lock` on main is not regenerable — fix upstream and re-pin | P1 | `uv lock` cannot resolve `pyproject.toml` from scratch (uv 0.8.22 / 0.9.5 / 0.10.0, online or offline): at the pinned commit, sysml-codegen's `pyproject.toml` declares `agentic-mbse = { path = "../agentic-mbse" }` under `[tool.uv.sources]`, and uv resolves a relative path inside a *git* source as a subdirectory of that checkout, which does not exist. The stop-parser pin commits (`510d8208`…`8cb0b838`) edited the lock by text substitution and only ever ran `uv lock --check`, which verifies consistency, not resolvability. Consequence: no dependency can be added to fusion-tea without hand-editing the lock (done once, verified by `uv lock --check`, for `jsonschema` on 2026-08-21 — see `.project/active/stellarator-demo-landing/plan.md` Phase 1 notes). Fix: sysml-codegen drops or workspace-scopes the relative source; fusion-tea re-pins through the provenance chain (`tests/test_dependency_provenance.py`). Surfaced 2026-08-21. |
| Review codegen-generated artifacts: what belongs in git vs ignored | P1 | `[OWNER 2026-08-21]` "there is a LOT of data generated during the codegen process" — decide, per artifact class, tracked vs ignored vs regenerable-on-demand, then apply it in one cleanup commit + `.gitignore`. Census on `main` at `d0e4398d` (tracked files / bytes): `exploration/stellarator_e2e/generated/` 140 / 737 KB (the sealed package — hash-verified by teax, so it is either tracked or regenerated from the snapshot with a license); `stellarator.snapshot.json` 1 / 637 KB (license-free regeneration input); `exploration/stellarator_e2e/outputs/` **300 / 68 KB tracked despite the ignore rule added 2026-08-21** (predate it); `exploration/stellarator_e2e/study/` 8 / 654 KB (proof-of-life evidence, keep); `exploration/ife_e2e/generated/` 46 / 136 KB; `exploration/ife_e2e/outputs/` 72 / 19 KB (3 named fixture dirs + residue); `exploration/pipeline_spike/` 274 / 409 KB; `data/ife_sweep/` 3 / 1.35 MB. No `__pycache__`/`.pyc` tracked. Classes to rule on: sealed packages, snapshots, handwritten impls (must stay), generated `tests/`, per-run output dirs (keep only named fixtures), study stores (`study/_work/` already ignored), sweep data. Output: a short policy section in `exploration/README.md` or CLAUDE.md, the `.gitignore` rules, and the cleanup commit. Coordinate with the migration PR, which regenerates the stellarator package. |

---

## In Progress

| Epic | Priority | Status | Started | Notes |
|------|----------|--------|---------|-------|
| Knowledge Database Integration | P1 | In Progress | 2026-02-06 | Items 1-3 complete, pipeline proven. Items 4-5 archived (blocked on user action, infrastructure works). |
| Source Extraction Fix & Re-extraction | P0 | Draft | 2026-03-29 | HTML extraction broken (tables, images, quality). Fix upstream → re-extract → clean .orig.md. |
| Pipeline Hardening (ad-hoc) | P0 | **Complete 2026-04-11** | 2026-04-05 | 6 items archived (pipeline-hardening, output-validation-retry, concept-landscape-context, orig-md-research, feedback-routing-fix, explorer-merge). Analysis pipeline now safe for batch runs. |
| Ontology v3 Migration | P0 | In Progress | 2026-05-17 | 6 items, ~5.5–8d. Item 1 complete (PR #15 merged 2026-05-17). Next: Item 2 — branch off `main`, merge `fix/concept-renumbering-robustness`. File: `epic_ontology_v3_migration.md`. |
| Concept-Analysis Pipeline Rework | P0 | Draft | 2026-05-30 | 11 items (~10–14d) + 1 aspirational Phase 3. Phase 0 throwaway probes (prototype + stability + critic acuity) before plumbing. Two-layer split, two-knob 1 GWe NOAK replication floor + aspirational native-scale supplement, override registry, standalone `model_critic`. File: `epic_concept_analysis_rework.md`. |
| Explorer UX v3 — Provenance & Coherence | P1 | Draft | 2026-06-06 | Phase 1 (2 items, ~3–3.5d): slider/tornado/headline coherence (option c toggle) → override-inspection surface. J2/J3 "why is this number, can I trust it?" spine. Later phases (per-account decomposition, family/comparables, landing reframe, maturity panel) not yet decomposed. File: `epic_explorer_ux_v3.md`. Research: `.project/research/20260605-150329_concept-explorer-ux-user-journeys.md`. |
| Stellarator MBSE Full Demo | P0 | On Hold | 2026-07-18 | On hold by owner 2026-08-19. Items 1–4 complete (handshake to 1costingFE: LCOE 275.264220, 5/5 verdicts). The Run-Study Capability epic owns the A/B proof; this epic consumes that evidence if resumed. File: `epic_stellarator_mbse_demo.md`. |
| Run-Study Capability | P1 | In Progress | 2026-08-19 | Items 1–5 complete and audited (2026-08-20). Item 6 (first A/B consumer + policy cutover) runs **after the stellarator model migration** `[OWNER 2026-08-21]`, on the stock teax route. File: `epic_run_study_capability.md`. |

---

## P1 - High Priority

### Run-Study Capability

**Priority**: P1
**Effort**: ~6–9 days (6 items)
**Status**: In Progress — Items 1–5 complete and audited 2026-08-20; Item 6 after the stellarator model migration `[OWNER 2026-08-21]`

Turn the verified proof-of-life study discipline into a durable `run-study` skill, runbook, policy, package-agnostic tools, and evidence-complete records. This epic owns the first A/B proof while the Stellarator MBSE Demo epic is on hold.

**Items**:
- [x] Item 1: Indicator Reachability Spike — complete 2026-08-19
- [x] Item 2: Skill, Runbook, and Record Contract — complete 2026-08-20
- [x] Item 3: Indicator Tool and Package Manifest — complete 2026-08-20
- [x] Item 4: Quality Tools and Era Adapter Promotion — complete 2026-08-20
- [x] Item 5: Cold-Pickup Administrator Exercise — complete 2026-08-20 (owner-approved)
- [ ] Item 6: First A/B Consumer and Policy Cutover — after migration (stock route, no era adapter)

**File**: `epic_run_study_capability.md`

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
| run_analysis.py CLI Step Semantics | P1 | Paused — spec drafted 2026-06-05, never started, filed 2026-08-20. `analyze` and `model-setup` present as peers but overlap; `regenerate-concept` chains them so the weaker model-setup path overwrites the loop's output. Still present on `main` (`run_analysis.py:1449`, `:1312`). | `.project/active/run-analysis-cli-step-semantics/` |

### Availability-standardization follow-ups (2026-05-17)

From the availability standardization (commit `45c9db5`); details in `.project/research/20260517-availability-policy-affected-concepts.md`.

| Item | Priority | Description |
|------|----------|-------------|
| Refresh synthesis.md for 13 standardized concepts | P2 | `synthesis.md` prose still cites pre-standardization availability + LCOE numbers; iteration loop flagged most with `Stale: true` in frontmatter. Refresh via `uv run agentic-mbse … synthesize <concept>` (or equivalent in run_analysis.py) once other concept-analysis fixes are batched. Spending tokens on this alone is wasteful — bundle with the next batch synthesis pass. |
| Investigate 20a capital-side availability coupling | P3 | After the availability standardization, concept 20a's overnight cost moved ~+3.5% from a 2.3% availability drop. Pure 1/availability should leave overnight cost unchanged. Either a costingfe IDC/escalation behavior or a 20a-specific override. Add a perturbation test that sweeps availability ±5% and prints overnight cost — if a real coupling, document; if a bug in 20a's overrides, fix. Other concepts may have the same silent issue. |
| Non-D-T availability policy + standardize | P2 | The availability standardization script filtered to D-T. Four non-D-T concepts (`04` p-B11 pulsed, `06` p-B11 steady mirror, `08` D-He³ pulsed FRC, `23` p-B11 pulsed) were skipped. The current `scoring_framework.md` table says "D-D / D-³He / p-¹¹B → 0.85" with reasoning "Same MCF basis", which implies non-D-T should be 0.85 regardless of pulsed/steady. The `canonical_availability` helper currently returns 0.75 for any pulsed family regardless of fuel — contradicts the policy text. Decide actual policy, update helper, run the standardize pass for these 4 concepts. |
| Concept 09 dual-site availability refactor | P3 | `09-qi-stellarator-hts/model_setup.py` has availability in two coupled sites: `_SHARED[availability]=0.88` (costingfe forward call, line 205) and `_AVAILABILITY_BASE=0.88` (custom replacement-cost calc, line 173 — comment says "matches _SHARED below"). Pre-marked as `# DEVIATION:` so the standardize script skipped 09. Either (a) refactor to a single `AVAILABILITY` constant used in both sites and move to canonical 0.85, or (b) promote to Tier-A retain at 0.88 if `helios-stellarator-comparison.md` 88% citation qualifies as a sourced commitment. |
| Audit script for "DEFAULT" labels vs actual values | P3 | Walk every concept's `model_setup.py`, parse all kwargs, flag any value with a `# DEFAULT` comment whose actual value doesn't match the costingfe library default (or the canonical_eta_th/canonical_availability lookup). Report-only, no auto-fix. ~30-line script parallel in shape to `standardize_eta_th.py`. Surfaces silent drift before it becomes a policy dispute. Motivated by inflation_rate=0.0245 case in `.project/research/20260517-081444_model-setup-inconsistencies.md` §2. |

### Explorer-rework-unblock follow-ups (2026-06-05)

Surfaced by the first end-to-end run after `explorer-rework-unblock` landed. None are explorer bugs — they are concept-side data issues that the previous `result` guard had short-circuited and were never observed in production. Spec: `.project/active/explorer-rework-unblock/spec.md`.

| Item | Priority | Description |
|------|----------|-------------|
| Fix 5 concept-side model_setup.py bugs + re-extract | P1 | Five concepts produce concept-side errors during/after extraction. **04 (laser-icf)**: `model_setup.py` passes `p_input` to laser_ife's forward(), which no longer accepts it (`ValueError: forward() got unknown parameter(s) for concept laser_ife: p_input`); update spec to library-current kwargs. **17b (laser-icf-fast-ignition)**: `result_1gw` missing at module level — concept not yet on the three-forward contract; regenerate via rework Item 11 or hand-port to `run_native_and_1gw`. **27 (polywell)** and **39 (st-cs-free-pb11)**: routing disagreement — `Comparison-Status: freeform-deferred` in frontmatter but `model_setup.py` still has `CostModel + from costingfe` (stale costingfe shape from before the concept was deferred); either delete the stale module or regenerate as freeform. **38 (particle-accelerator-driven-fusion)**: freeform script emits `lcoe_USD_per_MWh = float("inf")` (facility produces no electricity); extraction writes a JSON with `lcoe_per_mwh: None` after JSON serialization, which fails Pydantic validation at server startup. Either guard `_freeform_to_explorer_dict` against non-finite values or make 38's freeform model produce a finite sentinel. After fixes, run `uv run python exploration/concept_explorer/extract_explorer_data.py --skip-narrative` and confirm all 40 concepts write valid `data/{id}.json` AND `uv run python exploration/concept_explorer/server.py` starts cleanly. Current state: 35 of 40 extract to a server-loadable JSON. |

| Item | Priority | Description |
|------|----------|-------------|
| Refresh deployed Score Explorer UI after PR #33 | P2 | After PR #33 merges, mirror `tools/score_explorer/{index.html,data/concepts.json,data/weights.json}` → `docs/{index.html,data/concepts.json,data/weights.json}` and commit + push to main. Same straight-copy pattern as PR #28 (initial deploy) and PR #29 (TF correction refresh). Without this, the live URL at https://scoring.1cf.energy/ (and https://1cfe.github.io/fusion-tea/) will continue to show the pre-#32 data availability scores even though `tools/score_explorer/data/concepts.json` already has the refreshed values. Single commit, byte-level mirror of three files, ~5 min. |

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
