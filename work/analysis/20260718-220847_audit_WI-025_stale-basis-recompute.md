# Audit Report — WI-025 stale-basis-pass-through-recompute (work item audit)

**Date**: 2026-07-18 | **Auditor**: independent audit session (did not implement the work)
**Scope**: work item WI-025 (`work/active/WI-025_stale-basis-pass-through-recompute/`), uncommitted working-tree changes on `feat/stellarator-mbse-demo` at HEAD `72f7d054`
**Verdict**: **PASS** — all six MR-WI025 requirements satisfied, all five spec Success Criteria met, all three Checkpoint Rulings honored, all plan completion gates re-verified. No blocking or non-blocking findings. Five note-level observations below.

## Executive Summary

WI-025 retires the model's last three STALE BASIS accounts by rebinding them as forward-computed functions of the model's own powers: three new library calc defs in `models/library/analyses/mfe_account_costs.sysml` — `'Buildings Cost'` (CAS21, exact 6-term grouped collapse of the 1costingFE 18-building DT loop), `'Preconstruction Cost'` (CAS10 pre-contingency subtotal), `'Annual OM Cost'` (CAS70 unlevelized) — wired in the generic plant (8 concept-input attributes + 3 calc usages) and bound at the Stellaris instance with full MR-4 docs. The auditor independently re-derived all three formulas and every constant from the pinned 1costingFE (`0254385`), re-ran the grouping arithmetic from a from-scratch 18-building table transcription, re-executed the pipeline, handshake, full validation ladder, IFE regression, and pytest, independently recomputed the rollup and LCOE with own arithmetic, and re-verified every citation, hash, twin diff, and record. Every executed number matches the design's oracle-rollup-exact expected table and the plan's Implementation Record to the last printed digit. The Ruling-3 successor bar held (injection-map-only handshake edit, comparison JSON byte-identical). The clean-room quarantine held. Working tree verified byte-identical (status + diff sha256) before and after all audit re-runs.

## Executed Evidence (re-run by the auditor, not taken from the implementation record)

| check | result |
|---|---|
| `run_stellaris.py` (exec venv) | ALL CHECKS PASSED, rel 1e-9 vs oracle on every channel including the three new account channels (`buildings`/`precon`/`annual_om`), zero failures |
| CAS21 / CAS10 / CAS70 | $640,475,006.165738 / $34,391,496.769624 / $52,517,269.060943 per yr — bit-exact vs oracle, and matching the auditor's own from-scratch arithmetic (below) |
| direct / total capital | $9,247,944,633.471426 / $12,638,857,665.744282 (+0.296% vs WI-024) |
| LCOE | $203.647152/MWh (+$2.175087 vs WI-024's $201.472065 — auditor's own delta arithmetic) |
| denominator invariance | p_net 915.081088, q_eng 6.606662, rec_frac 0.151362, p_cryo 0.864352, V 425.0000, p_fus 2748.056877, p_th 3238.120923, p_et 1078.294267 — all unchanged; magnet $6,323,469,946.334225 (printed share 50.0%, 50.03% at 4 s.f.) identical to the WI-023/024 record to the cent |
| independent rollup recompute | auditor's own arithmetic from per-account channel values (contingency 0.10, indirect 0.20×8/6, CRF at d=0.07/N=30, IDC (1.07)^4, E = 8760×p_net×0.85) reproduces total $12,638,857,665.744282 and LCOE $203.647152 exactly |
| `agentic-mbse validate models --complete` | L1 = 0 errors, 0 warnings over **22 files**; total ERROR list exactly 6: `mfe_plant.sysml:389/395/400` (auditor diffed HEAD :350-368 region vs worktree :386-404 — CONTENT-IDENTICAL, pure +36 shift from the WI-025 attribute/calc insertion), `ife_plant.sysml:33/41`, `hif_plant.sysml:205`; zero new, no diagnostic names a WI-025 element; L1/L3/L4/L5 pass (L5 66/66 documented); L2 ❌/L6 ❌ summary flags are the known pre-existing attribution (WI-023/024 precedent) |
| `handshake_1costingfe.py` diff | exactly TWO hunks (`@@ -239,8` and `@@ -286,6`), both inside `set_1cfe_inputs` (:153-304): sd block replaces the vanished `lcoe_calc__annual_om` injection with `om_cost__om_ref: 0.0`; mp block adds `om_cost__om_direct: refs["annual_om_unlevelized_musd"] * M` — the D6 IEEE identity path (0·x = 0, 0 + v = v). Rollup glue and tautological pass-through rows untouched (not in the diff). Zero comparison-logic change — the Ruling-3 successor bar holds exactly |
| handshake re-run | clean (net_electric 1,000.0001 both sides; generated inputs restored); `git diff handshake_comparison.json` = 0 lines (SV-025/026 byte-identical) |
| IFE regression `run_anchors.py` (re-run) | 252.29996307 / 68.69020165 / 270.12117794 $/MWh; Meier 4.73540355 c/kWh; gain-100 perturbation 216.55528392 — SV-023 anchors unchanged |
| pytest `tests/models/` | **11 failed / 18 passed / 14 skipped / 0 errors** — tally identical to the spec's operative baseline; failed set = 1 `test_foundation` + 10 `test_power_balance` (the recorded pre-existing profile) |
| WI-022 handwritten reactivity impl | sha256 `8d23574793c34314c67b68b8e0f4ec438d3e2d9f92060eb4094a8d46c0794a9f` — matches the plan record; `AUTO_IMPLEMENTED = False` intact; `preserve_handwritten=True` at `bridge_v11_generate.py:108`; sysml-codegen HEAD `6db3212` |
| regen artifacts | `system_design.json`: +8 leaves (6 `buildings_cost__*_base` at the instance $ values, `precon_cost__fixed_precon` 32000000.0, `om_cost__om_ref` 54900000.0), `lcoe_calc__annual_om` GONE; `mfe_plant_params.json`: +13 defaulted-input leaves (5 buildings refs/n_mod, 4 om, 4 precon) + the 3 bridge keys at the WI-025 executed rollup (the committed post-run state pattern); pipeline yaml chain-wires buildings ← `pb__p_et/p_the/p_th` + `fusion__p_fus.root` (:298-301), precon/om ← `pb__p_net` (:315/:328), `lcoe_calc.annual_om` ← `om_cost__annual_om.root` (:341); 3 new impls `AUTO_IMPLEMENTED = True` (both markers each); `IMPLEMENTATION_BACKLOG.md` still exactly 1 function; `__init__.py`/schemas/tests/snapshot diffs all regen-shaped (module registry gains the three `*_CostModule`s; snapshot carries the new calc defs) — no hand-edit indicators anywhere under `generated/` |
| working-tree idempotency | `git diff` sha256 `222cc109…` and `git status --porcelain` sha256 `124083a8…` identical before and after all audit re-runs — nothing dirtied |

## Formula Fidelity (re-derived from the pinned 1costingFE, auditor's own reads and arithmetic)

All formulas and constants re-read at `/home/reid/1cfe/1costingfe` @ `0254385` (repo verified at the pin):

- **CAS21** (`costs.py:83-144`): scale_map :121-130 with refs `ref_gross_power_mwe` 1100 for p_et and p_the (:103-104, "= p_et, no DEC" printed in the source at :104), P_TH_REF 2500 (:105), P_FUS_REF 2300 (:106), staff = sqrt(p_et_tot/ref) (:127-129), cryogenics SC-gated (:137), returned raw (:86-88). The auditor transcribed the 18-building DT table from `costing_constants.yaml:175-197` independently and re-derived the group sums: fixed **168.5** (85+9+14+3.5+17+5+14+21), p_fus **288** (138+104+29+17), staff **9**, p_the **58**, p_th **26** (17+9), p_et **29** (17+12) — 8+4+1+1+2+2 = 18 buildings, table exhausted, every building linear in exactly one basis. The grouped 6-term form and the full 18-term loop agree at the executed powers to 1 ulp in the auditor's own float64 evaluation (summation-order effect only; the collapse is exact algebra, not a fit). Model/impl/oracle all carry the 6-term form with identical parenthesization.
- **CAS10** (`costs.py:52-80`): land = land_intensity·sqrt(p_net·n_mod·ref_net)·land_cost (constants yaml:21/:22/:8) + six adders 3+5+2+20+1+1 = **32 M$** (yaml:15-23, FOAK :16, licensing_cost_dt :23); contingency added at :79 — deliberately not carried (pre-contingency subtotal convention, doc states it).
- **CAS70** (`costs.py:319-357`, annual line :353): om_cost_dt 54.9 M$/yr (yaml:272) × (p_net·n_mod/1000)^0.5; CAS71/72 not carried (unlevelized convention, doc states it).
- **Honesty check — stale literals reproduce** (auditor's arithmetic): CAS21 at p_et=p_the=896.8/p_th=2693.1/p_fus=2700 → 613.6502 M$ (bound $613.650M ✓); CAS10 at p_net=575.3 → 33.8962 M$ ✓; CAS70 at 575.3 → 41.6408 M$/yr ✓. The retirement notes state these old bases correctly.
- **Executed values reproduce** (auditor's arithmetic at the full-precision executed powers): CAS21 $640,475,006.17, CAS10 $34,391,496.76962399, CAS70 $52,517,269.060942635 — matching the executed channels at the printed precision (CAS10 within 1 ulp of the pipeline value, association order).
- **Frozen dimensions**: DT (every fuel-keyed constant used is the dt entry), FOAK (`plant_studies_foak` 20 in the 32 M$ sum), n_mod = 1 as defaulted calc inputs with freeze docs at the calc defs and bindings. **Conventions**: CAS21 raw, CAS10 pre-contingency, CAS70 unlevelized — each stated in the calc-def doc and the instance binding doc. **p_the = p_et** documented in the calc-def doc, the instance region comment, and the oracle comment.
- **Oracle mirrors the emitted impls verbatim**: the auditor compared the three generated impl return statements (`buildings_cost_impl.py:100`, `preconstruction_cost_impl.py`, `annual_om_cost_impl.py`) against the oracle's forward forms side by side — parenthesization identical, term for term.

## STALE BASIS Retirement & Doc Honesty (MR-WI025-4)

- `grep -rn "STALE BASIS"` over `models/` and `exploration/stellarator_e2e/models/`: **zero hits** (both trees).
- Single-word `STALE` remains once per instance copy (:70, both) — the headline history line "retiring the final STALE / BASIS annotations" split across a line break. It is a history statement, not an annotation, and the Implementation Record's deviation 1 discloses it transparently (see observation 1).
- Each account's replacement doc states: which computed powers it now tracks (CAS21 p_fus/p_the/p_th/p_et; CAS10/CAS70 p_net), the preserved convention, the frozen dimensions, and the retired literal with its old basis. All MR-4 `Source / Ref / Basis` citations spot-resolved by the auditor at the pin: yaml:177/183-185/188-189/195/197, :179-181/186, :187, :191, :192/196, :193-194 (per-group member-building cites — every line number matches the table read); costs.py:103-106/:121-130/:127-129/:137/:52-80(:79)/:319-357(:353)/:64/:109-112 — all resolve to the claimed content.

## MR Verification

| requirement | status | evidence |
|---|---|---|
| MR-WI025-1 (forward-computed, tracking computed powers; literals replaced; STALE BASIS retired) | PASS | three calc defs + plant wiring + instance bindings; runner channels `buildings_cost__cost`/`precon_cost__cost`/`om_cost__annual_om` executed bit-exact; grep-zero on "STALE BASIS" both trees |
| MR-WI025-2 (exactness — mirrors 1costingFE, not a fit) | PASS | auditor's independent 18-building loop vs grouped form: agreement to 1 ulp at f64 (algebraically exact grouping, from-scratch table transcription); design-stage 1cfe-side evaluation on record (CAS21/CAS70 bit-identical at f64, CAS10 1 ulp, full CAS10 = subtotal × 1.10); implement-side witness: oracle mirrors emitted forms verbatim + rel 1e-9 gate |
| MR-WI025-3 (conventions + frozen dimensions preserved) | PASS | CAS10 pre-contingency / CAS21 raw / CAS70 unlevelized each verified against costs.py and stated in the docs; DT/FOAK/n_mod=1 frozen as documented constants; p_the = p_et documented at the calc def, instance, and oracle |
| MR-WI025-4 (honest re-baselining of every consumer) | PASS | oracle computes the accounts forward (constants dropped from IN); runner headline retargeted to WI-025 (asserts re-run green); regen-only generated artifacts (+8/+13 surface verified); SV-032 executed record matches the auditor's run; SV-030/031 stand (matrix diff = SV-032 row only); docs state post-WI-025 bases |
| MR-WI025-5 (standing bars; handshake successor bar) | PASS | L1 0/0 over 22; offender list exactly the 6 pre-existing, content-verified across the +36 shift, zero new; regen with WI-022 impl hash survival; pipeline bit-exact; IFE anchors exact; pytest tally 11/18/14/0; twins per-edit-region identical; handshake two injection-map hunks only, comparison JSON byte-identical |
| MR-WI025-6 (MR-4 citations; clean-room) | PASS | every changed value/doc carries Source/Ref/Basis resolving to the pin (spot-resolved above); +3 traceability-matrix rows (codebase convention); no barred source read or cited (see Quarantine) |

## Spec Success Criteria

1. **SV-032** — PASS. Three accounts are computed outputs tracking the computed powers, bit-exact vs the re-baselined oracle at rel 1e-9 (re-executed by the auditor); executed headline in the matrix row matches the auditor's run exactly; denominator and magnet capital unchanged to the cent; row `passing` with the EXECUTED block.
2. **Exactness proven** — PASS. Design-stage 1cfe-side evaluation on record and independently corroborated by the auditor's own loop-vs-grouped arithmetic; oracle/impl statement forms verified identical.
3. **Standing bars** — PASS. All re-run: ladder offender list exact, regen integrity (hash, +8/+13, 3 auto-impls, backlog 1), bit-exact execute, IFE anchors, pytest tally, mirroring.
4. **Handshake** — PASS under the Ruling-3 successor bar: edits confined to `set_1cfe_inputs`'s injection map (two hunks, D6 identity path); no out-of-map edit was forced (D6's conclusion held); `handshake_comparison.json` git diff empty after the auditor's re-run.
5. **Docs** — PASS. STALE BASIS annotations retired (grep-zero); each doc states powers tracked + preserved convention; MR-4 citations to 1costingFE @ `0254385` throughout, spot-resolved.

## Checkpoint-Ruling Fidelity

- **Ruling 1 (three-account scope, conventions as found, DT/FOAK/n_mod=1 frozen)**: diff surface is exactly the three accounts + their support structure; no other account touched; conventions verified preserved. PASS.
- **Ruling 2 (SV-032 records the executed headline; SV-030/031 stand)**: matrix diff is the single SV-032 line; SV-030/SV-031/SV-016 rows byte-untouched. PASS.
- **Ruling 3 (successor-bar escalation path)**: no injection-map-external edit was forced; the one forced edit (vanished `lcoe_calc__annual_om` leaf) landed inside the map; escalation correctly not triggered. PASS.

## Records

- **SV-032** `passing` with executed values identical to the auditor's re-run. **SV-030/SV-031** untouched (historical records stand). **SV-016** untouched entirely (`pending`, q_eng did not move). No status mutations made by this audit (item close is owner-held).
- **Traceability matrix**: three new calc-def rows, codebase-sourced convention (`1costingFE @ 0254385`), locations matching the calc-def docs.
- **`work/BACKLOG.md`**: WI-025 (epic) + WI-026 (standalone, the owner-ruled pytest re-record split) registered — the spec-stage registrations, in scope.
- **`.project/CURRENT_WORK.md`**: new WI-025 top entry; every number matches the executed values; correctly marked NOT closed / NOTHING committed.
- **Plan**: 56 checked boxes, 0 unchecked; Implementation Record complete and accurate — every claim the auditor re-derived (hashes, offender lines, executed values, the five recorded deviations) checks out; all five deviations are real, surfaced, and benign.
- **Mirroring**: `mfe_account_costs.sysml` twins byte-identical (417 lines); `mfe_plant.sysml` twins differ only by the 3 known WI-015 DEMO NOTE regions (direct_capital, total_capital, assert-constraints); `stellarator_plant.sysml` twins differ only by the viability-assert block. All WI-025 edit regions byte-identical across twins.
- **Scope**: `git status`/`git diff --stat` surface = exactly the spec's In-scope list plus the sanctioned registrations and regen artifacts; no surprises.

## Findings

No blocking findings. No non-blocking findings.

**Observations (no action required for WI-025):**

1. **[observation] The retired marker survives as a line-break-split history mention.** The headline history line reads "…retiring the final STALE\nBASIS annotations" (instance :69-70, both copies), so single-line grep-zero holds while a multiline search would still match the phrase. It is a history statement, not a live annotation, and the Implementation Record's deviation 1 discloses both the "Stale basis retired:" rewording and this split explicitly. Honest; no action.
2. **[observation] Generated impl docstrings mangle the MR-4 markers** (`**Source**` → `*Source**`) in all three new impls — the same pre-existing codegen doc-transcription cosmetic the WI-024 audit noted; the model doc comments are intact.
3. **[observation] BACKLOG.md lists WI-025 as `status: backlog`** while its spec is `active`; the dashboard resolves this with the established "spec.md Status overrides BACKLOG.md" warning, identical in kind to the pre-existing WI-009/010/018 warnings. Status flips at owner close via `pm close-item`. Established convention, not a defect.
4. **[observation] The oracle reuses its existing `p_et_ref` entry for the p_the term** (design D7 said reuse; both are 1100.0, no-DEC, and the comment says so). Behavior is bit-identical to the impl's separate `p_the_ref` default; fine.
5. **[observation] "Bit-identical" grouping claims are association-order-sensitive.** The auditor's own table-order 18-term loop differs from the grouped form by 1 ulp at f64; the design's bit-identical claim is against 1cfe's own dict-order loop and is corroborated, not contradicted, by this — the operative guarantees (algebraic exactness, design-stage 1cfe-side agreement ≤1 ulp, pipeline-vs-oracle rel 1e-9) all hold with margin.

## Quarantine

No PROTOCOL §3 barred path was opened in this audit (sources read: the pinned 1costingFE `costs.py`/`costing_constants.yaml`, in-repo model/pipeline/work artifacts — all admissible; PROTOCOL.md itself as Required Reading). A grep of the full working-tree diff and the new WI-025 artifacts for "aries"/"holdout" found only the PROTOCOL Required-Reading/compliance lines and the substring coincidence `reactor_auxiliaries`. The Implementation Record's quarantine disclosure is consistent with what the auditor observed.

## Audit Metadata

- Models audited: `models/library/analyses/mfe_account_costs.sysml` (+staged twin), `models/designs/generic_mfe/mfe_plant.sysml` (+twin), `models/designs/stellarator_09/stellarator_plant.sysml` (+twin); oracle/runner/handshake/generated artifacts under `exploration/stellarator_e2e/`
- Baseline source: 1costingFE @ `0254385` (`src/costingfe/layers/costs.py`, `src/costingfe/data/defaults/costing_constants.yaml`) — this item's sole admissible source set
- Thresholds: rel 1e-9 (pipeline vs oracle), byte-identity (handshake JSON; library twins), exact offender-list match (L1–L6), auditor's own float64 arithmetic for formula/grouping/rollup recomputation
- Everything in "Executed Evidence" was re-run by the auditor; nothing in this report relies solely on the implementing agent's self-report. Working tree verified byte-identical (git diff + status sha256) before and after all audit re-runs.
