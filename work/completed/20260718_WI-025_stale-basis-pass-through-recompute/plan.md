---
Status: complete
Created: 2026-07-18
Updated: '2026-07-18'
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-025 Plan: STALE-BASIS Pass-Through Recompute

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — demo model-development session; §3 barred paths must not be read, cited, or opened. This item's admissible source set is 1costingFE only (`/home/reid/1cfe/1costingfe`, pin `0254385`, read-only).

Owner rulings (all recorded in spec §Checkpoint Rulings; no further owner stop planned before audit): Ruling 1 confirmed the three-account forward-computed scope with conventions preserved as found. Ruling 2 confirmed SV-032 records the WI-025 executed headline and SV-030/SV-031 stand untouched as historical records. Ruling 3 confirmed the successor-bar escalation path — the design's D6 re-derivation concludes the structure forces edits **only inside** `set_1cfe_inputs`'s injection map, so escalation is **not triggered**; if implement discovers otherwise, that is a hard STOP and owner escalation, never absorbed. Item close (`pm close-item`) is owner-held; committing is orchestrator-held — neither is a plan step.

## Source Documents

- Design (primary, approved): `./design.md` — D1–D7, Proposed Design §1–5, Research Findings (formula re-verification, exactness proof, snapshot/codegen spike, validation baseline, staged-subset quirk), Validation Plan, expected-headline values
- Spec (contract): `./spec.md` — MR-WI025-1..6, Success Criteria 1–5, Checkpoint Rulings 1–3, Evidence tables
- Alignment brief: `work/orchestration/stale-basis-recompute.md`
- Epic: `work/backlog/epic-mfe-cost-modeling.md`
- Executed template: `work/completed/20260718_WI-024_recirc-power-derivation/plan.md` (phase spine, content-hash pattern, Implementation Record convention — the executed record this plan's baseline moves from)

## Design Summary

Three new library calc defs appended to `models/library/analyses/mfe_account_costs.sysml` — `'Buildings Cost'` (CAS21, exact 6-term grouped collapse of the 18-building loop), `'Preconstruction Cost'` (CAS10, pre-contingency subtotal), `'Annual OM Cost'` (CAS70, unlevelized) — replace the model's last three STALE BASIS literals with forward computations of the model's own powers. The generic plant gains 8 concept-input attributes plus 3 calc usages; the Stellaris instance binds the 8 values (all $-conversions of pinned 1costingFE constants, DT/FOAK/n_mod = 1 frozen as documented constants) and retires the three STALE BASIS annotations. Expected executed headline (design, oracle-rollup-exact — evidence anchors, never targets to fit): **CAS21 $640,475,006.17, CAS10 $34,391,496.77, CAS70 $52,517,269.06/yr → total $12,638,857,665.74 (+0.296%), LCOE $203.647152/MWh (+$2.1751); p_net 915.081088, q_eng 6.606662, rec_frac 0.151362, and magnet capital all unchanged** (costs do not feed the power balance; the denominator does not move).

## Prototype Baseline (from the design Validation Report, re-verified at plan time)

- **Design-stage spikes: ALL PASS** (scratch trees, no repo file touched): canonical-tree L1 = 0 over 22 files with the L2–L6 offender list exactly the 6 pre-existing, content-identical, line-shifted; staged-tree snapshot classifies all three modules FULLY_COMPILABLE with all power feeds as chains and the `lcoe_calc__annual_om` settable leaf gone; V11 bridge reports exactly 3 offenders; 1costingFE-side exactness evaluation at the executed powers agrees with the forward forms (CAS21/CAS70 bit-identical at float64, CAS10 within 1 ulp; full CAS10 = subtotal × 1.10 exactly, confirming the pre-contingency convention).
- **Plan-time re-verifications (at HEAD `72f7d054`; working tree carries only the expected uncommitted WI-025 spec/design + registration):** sysml-codegen HEAD still `6db3212`; 1costingFE checkout at pin `0254385`; `preserve_handwritten=True` still at `exploration/stellarator_e2e/bridge_v11_generate.py:108`; WI-022 handwritten impl sha256 `8d23574793c34314c67b68b8e0f4ec438d3e2d9f92060eb4094a8d46c0794a9f` (identical to the WI-024 record); SV-032 registered `pending` at `modeling_project/VALIDATION_MATRIX.md:58`; `mfe_account_costs.sysml` canonical and staged twins byte-identical (303 lines each); `mfe_plant.sysml` already imports `mfe_account_costs::*` (:9) — **no import edit needed this item**.
- **Level 4–6 issues:** none introduced; the bar everywhere below is L1 = 0 over the **22-file** set (append-only — no new file this item), offender list exactly the 6 pre-existing (`mfe_plant.sysml:353/359/364` pre-edit, expected to print at **:389/:395/:400** post-edit — the design-predicted shift from the inserted attribute/calc block; `ife_plant.sysml:33/41`, `hif_plant.sysml:205`), zero new — **compare the offender list, not level-summary flags** (known hif L2-section attribution, WI-023/024 precedent).
- **Staged-subset quirk (design Research Findings — do not chase):** validating the staged e2e subset alone reports a different pre-existing 5-error set, with the `preconstruction_capital` entry re-classing to an ADR-002 Rule-3 message under this change (count unchanged, 5→5). The MR-WI025-5 bar runs `validate models --complete` on the canonical set only.
- **Known twin divergences (mirroring gates account for these):** `mfe_plant.sysml` staged twin — 3 DEMO NOTE divergences (WI-015); `stellarator_plant.sysml` staged twin — the commented-out viability-assert block; `mfe_account_costs.sysml` twins byte-identical. All WI-025 edit regions sit outside the divergent regions (design D7, patch-proven on both trees).
- **Regen-flow gotcha (carried from WI-024):** `sysml-codegen snapshot` with `--design-path-filter` produces 8 spurious V11 offenders. The Phase 4 snapshot must be **unfiltered**; control: the bridge must report exactly 3 offenders.

## Phasing Approach

Seven phases, the design's Implementation Checklist order: library calc defs → generic plant → instance → regen → oracle/runner → handshake/regressions → close-out. Library before usages, generic plant before the instance that binds its attributes (bottom-up). **Canonical and staged twins are edited together within each model phase** (Phases 1–3) with the mirroring diff checked per phase — the staged tree is what the Phase 4 snapshot reads. Model edits precede regen (the snapshot bakes bindings); oracle edits precede the execute (the runner gates bit-exact against the oracle); the handshake injection edit comes after the bit-exact execute so it lands on a proven pipeline.

**Line numbers below are pre-edit anchors, verified current at `72f7d054`.** All design anchors verified un-drifted at plan time (stale literals :280/:594/:643, STALE BASIS :270/:602/:648, generic-plant :98-99/:342/:366/:394/:401, oracle :102-108/:195-210/:223-228, runner :93-94/:193/:246/:281-283, handshake :243/:369-371). Match edits on content; use the numbers to orient.

## Validation Strategy

- **Per phase:** L1–L3 after every model-file edit (Phases 1–2); full L1–L6 offender-list compare + mirroring diffs after all model edits (Phase 3); regen self-checks (Phase 4); bit-exact execute (Phase 5); handshake byte-identity + IFE/pytest regressions (Phase 6).
- **Environment:** all Python via `uv run` — never bare python. License via `set -a && source ~/1cfe/fusion-tea/.env && set +a` before any validate/snapshot/bridge invocation. Validation via `uv run agentic-mbse validate models --level N` / `--complete`. Pipeline execution and handshake use the exec-venv interpreter directly (by design): `/home/reid/1cfe/fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python`.
- **Final:** spec Success Criteria 1–5 verified explicitly in Phase 7; SV-032 → passing with executed values; SV-030/SV-031 untouched (Ruling 2); SV-016 untouched entirely (q_eng does not move this item — spec Out of Scope).

---

## Phase 1 — Library calc defs (append to `mfe_account_costs.sysml`, canonical + staged identical)

**Overview**: append the three concept-agnostic calc defs to the existing account-costs library file. First because everything downstream uses them. No new file this item — the 22-file set is unchanged.

**Design reference**: design "Proposed Design §1. Library calc defs" (the complete stencils — use verbatim, including the doc comments with MR-4 Source/Ref/Basis blocks), decisions **D1** (grouped 6-term exact collapse; per-building table lives in the instance binding docs), **D2** (placement: this file's charter; fuel/FOAK-keyed values are undefaulted concept inputs, calibration constants are defaulted inputs with 1cfe citations — the `'Blanket Cost'` pattern), **D5** (`om_direct` additive term, default 0.0 — the handshake identity path).

**Files**: REFINE `models/library/analyses/mfe_account_costs.sysml` (append); REFINE `exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml` (staged twin, byte-identical).

**Checklist**:

- [x] Pre-edit: `diff` the two twins → byte-identical (verified at plan time; re-confirm). *(Confirmed at HEAD `72f7d054`, 303 lines each.)*
- [x] Append `calc def 'Buildings Cost'` from the design §1 stencil verbatim: 6 undefaulted base-sum inputs + 4 power inputs, defaulted `n_mod` 1.0 / `p_fus_ref` 2300.0 / `p_the_ref` 1100.0 / `p_th_ref` 2500.0 / `p_et_ref` 1100.0, `out cost` with the 6-term expression, full doc (raw/pre-contingency convention, exact-grouping basis, p_the = p_et no-DEC note, MR-4 block citing costs.py:83-144 + costing_constants.yaml:175-197).
- [x] Append `calc def 'Preconstruction Cost'` from the stencil verbatim: undefaulted `fixed_precon`, `p_net` input, defaulted `n_mod` 1.0 / `land_intensity` 0.25 / `land_cost` 10000.0 / `ref_net_power` 1000.0, `out cost`, full doc (PRE-CONTINGENCY subtotal, costs.py:79 contingency deliberately not carried, MR-4 block citing costs.py:52-80 + yaml:8,:15-23).
- [x] Append `calc def 'Annual OM Cost'` from the stencil verbatim: undefaulted `om_ref`, `p_net` input, defaulted `n_mod` 1.0 / `ref_net_power` 1000.0 / `alpha` 0.5 / `om_direct` 0.0, `out annual_om`, full doc (UNLEVELIZED, CAS71/72 Stage-3 out of scope, om_direct identity-path note, MR-4 block citing costs.py:319-357 + yaml:272,:8).
- [x] Apply the identical append to the staged twin; `diff` the two files → byte-identical. *(cp then diff — identical, 417 lines each.)*
- [x] Add three traceability-matrix rows (`data/traceability_matrix.csv`, the `'Cryoplant Electrical Power'` codebase-sourced convention — Confidence/Assumptions empty): `'Buildings Cost'` / `'Preconstruction Cost'` / `'Annual OM Cost'`, File `models/library/analyses/mfe_account_costs.sysml`, Type calc_def, Source_Type codebase, Source_Document `1costingFE @ 0254385`, Source_Location `costs.py:83-144; costing_constants.yaml:175-197` / `costs.py:52-80; costing_constants.yaml:8,15-23` / `costs.py:319-357; costing_constants.yaml:272,8`, Last_Verified 2026-07-18.
- [x] Validate: `set -a && source ~/1cfe/fusion-tea/.env && set +a && uv run agentic-mbse validate models --level 1` → **22 files, 0 errors**; then `--level 2` and `--level 3`. Expected transient: up to three "Unused calc def" WARNs until the Phase 2 usages land (WI-024 Phase 1 precedent); re-check clean after Phase 2. *(L1: 22 files, 0 errors. L2: exactly the 3 transient Unused-calc-def WARNs (:304/:356/:387) + the 3 pre-existing hif_plant WARNs. L3: 0 cycles, PASS.)*

**Test requirements**: none new beyond the L1–L3 checkpoint — the calc defs' structural test is the Phase 4 snapshot classification (FULLY_COMPILABLE, spike-proven) and the Phase 5 bit-exact execute.

**Validation checkpoint**: L1 = 0 over 22 files; L2/L3 clean apart from the documented transient WARNs; twins byte-identical.

**Completion gate**: both twins carry the three stencils exactly; validation clean; three matrix rows present.

## Phase 2 — Generic plant wiring (canonical + staged, identical region edits)

**Overview**: wire the three calcs into the generic MFE plant — 8 concept-input attributes, 3 calc usages, and the three output rewires (buildings part, preconstruction attribute, annual_om attribute). `direct_capital`, `total_capital`, `lcoe_calc`, and the rollup calcs are **untouched** (the tracked offender lines stay content-identical). No import edit — `mfe_account_costs::*` is already imported (:9, verified at plan time).

**Design reference**: design "Proposed Design §2. Generic plant" (the attribute-block and calc-usage stencils), decisions **D3** (self-named alias chains for p_the/p_th/p_et — zero new glue, spike-proven; dotted `fusion.p_fus` and `pb.p_net`; n_mod and calibration refs left as defaulted calc inputs, not plant-bound) and **D4** (buildings keeps its part via the turbine idiom; `preconstruction_capital` and `annual_om` become attribute-mediated chains; `lcoe_calc`'s `in annual_om = annual_om` untouched).

**Files**: REFINE `models/designs/generic_mfe/mfe_plant.sysml`; REFINE `exploration/stellarator_e2e/models/designs/generic_mfe/mfe_plant.sysml` (same regions).

**Baseline anchors** (canonical, pre-edit): buildings part :98 (`part buildings : 'Buildings';`), precon attribute :99 (`attribute preconstruction_capital : Real;  // CAS10/20 pass-through`), misc_cost calc block :342, `direct_capital` sum :366 (untouched), annual_om attribute :394 (`// CAS70 O&M pass-through [$/yr] (WI-011)`), `lcoe_calc` `in annual_om = annual_om;` :401 (untouched).

**Checklist**:

- [x] Rewire :98 → `part buildings : 'Buildings' { :>> capital_cost = buildings_cost.cost; }` (turbine idiom, D4); comment/doc line per design §2 ("forward-computed (WI-025)", pass-through wording retired). *(Multi-line part-body form matching the sibling turbine/electric parts; single 2-line region comment covering CAS21/CAS10 forward + CAS27 still pass-through.)*
- [x] Rewire :99 → `attribute preconstruction_capital : Real = precon_cost.cost;` with the same doc treatment.
- [x] Rewire :394 → `attribute annual_om : Real = om_cost.annual_om;`; comment updated (no longer "pass-through (WI-011)").
- [x] After the misc_cost block (:342 region): add the design §2 stencil verbatim — 6 `bldg_*_base` attributes + `calc buildings_cost : 'Buildings Cost'` (6 base bindings, `in p_fus = fusion.p_fus`, self-named `in p_the = p_the` / `in p_th = p_th` / `in p_et = p_et`); `precon_fixed_base` attribute + `calc precon_cost : 'Preconstruction Cost'` (`in fixed_precon = precon_fixed_base`, `in p_net = pb.p_net`); `om_annual_ref` attribute + `calc om_cost : 'Annual OM Cost'` (`in om_ref = om_annual_ref`, `in p_net = pb.p_net`), with the block comments from the stencil.
- [x] Confirm no edit to `direct_capital` (:366 region), `total_capital`, `lcoe_calc` (:401), or any rollup calc — expression text unchanged (D4: offender lines must stay content-identical). *(git diff grep over rollup/lcoe identifiers: no touched lines.)*
- [x] Apply every edit, region-identical, to the staged twin; full-file `diff` canonical vs staged → **only the 3 known DEMO NOTE divergences remain**; every WI-025 edit region byte-identical. *(Diff shows exactly the 3 WI-015 DEMO NOTE regions: direct_capital, total_capital, assert-constraints.)*
- [x] Validate: env sourced, `uv run agentic-mbse validate models --level 1` → 22 files, 0 errors; `--level 3` clean (dataflow is instance literals + pb/fusion outputs → account calcs → rollup, no cycle — design "Cross-File Bindings"); Phase-1 transient WARNs cleared. *(L1: 22/0. L3: 0 cycles. L2 issues 3 = the pre-existing hif WARNs only; unused defs 0.)*

**Test requirements**: no new test files; the chain classifications are re-proven at Phase 4 (snapshot) and Phase 5 (execute).

**Validation checkpoint**: L1 = 0 over 22 files; L3 clean; mirroring diff shows only the known divergences.

**Completion gate**: all edits present in both twins; validation clean; rollup/lcoe/direct_capital lines verifiably untouched.

## Phase 3 — Stellaris instance bindings + STALE BASIS retirement (canonical + staged), full validation

**Overview**: replace the three stale literals with the 8 cited concept-input bindings, retire the three STALE BASIS annotations, state each account's post-WI-025 basis in its doc, and refresh the headline block. Then run the full ladder — this is the last model-text phase.

**Design reference**: design "Proposed Design §3. Stellaris instance" (the three region stencils with representative MR-4 docs — the six CAS21 base-sum docs each list member buildings with yaml line cites and the addition spelled out, the WI-024 `vol_cold` COMPUTED-doc pattern), decisions **D1** (per-building table carried in binding docs) and **D7** (docs state which powers each account tracks + the preserved convention; headline re-baseline + history line).

**Files**: REFINE `models/designs/stellarator_09/stellarator_plant.sysml`; REFINE `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml` (same regions).

**Baseline anchors** (canonical, pre-edit, verified at `72f7d054`): headline doc block :49-70; buildings region :262-281 (literal `:>> capital_cost = 613650000.0` at :280, STALE BASIS at :270); preconstruction region :594-614 (literal at :594, STALE BASIS at :602); annual_om region :643-660 (literal at :643, STALE BASIS at :648).

**Checklist**:

- [x] Buildings region (:262-281): replace the `:>> capital_cost = 613650000.0` override and its STALE BASIS doc with the design §3 stencil — region comment (forward-computed via buildings_cost tracking p_fus/p_the/p_th/p_et; p_the = p_et no-DEC, costs.py:104; exact grouped collapse of the 18-building DT column, cryogenics included for SC coils; DT/n_mod = 1 frozen; STALE BASIS retired with the old $613.65M pre-WI-019 basis stated) + the six bindings `bldg_fixed_base = 168500000.0` / `bldg_fus_base = 288000000.0` / `bldg_staff_base = 9000000.0` / `bldg_the_base = 58000000.0` / `bldg_th_base = 26000000.0` / `bldg_et_base = 29000000.0`, each with its full member-building MR-4 doc (yaml line cites per the design stencil pattern: :177,183-185,188-189,195,197 / :179-181,186 / :187 / :191 / :192,196 / :193-194). *(All six full MR-4 docs written; scale-line cites re-verified against the pin — costs.py:103-106 refs, :121-130 scale_map, :127-129 staff sqrt, :137 SC gate, yaml sums re-added.)*
- [x] Preconstruction region (:594-614): replace the `:>> preconstruction_capital = 33896000.0` binding with `:>> precon_fixed_base = 32000000.0` + the design §3 doc (32 M$ adder breakdown; tracks computed p_net via precon_cost; pre-contingency convention preserved, CAS29 applies once; STALE BASIS retired with the old $33.896M p_net = 575.3 basis stated; MR-4 cites yaml:15-23, costs.py:52-80 with :79 not carried).
- [x] Annual-O&M region (:643-660): replace the `:>> annual_om = 41641000.0` binding with `:>> om_annual_ref = 54900000.0` + the design §3 doc (om_cost_dt 54.9 M$/yr; tracks computed p_net via om_cost; unlevelized, CAS71/72 documented Stage-3 refinements; STALE BASIS retired with the old $41.641M/yr p_net = 575.3 basis stated; MR-4 cites yaml:272, costs.py:319-357).
- [x] `grep -n "STALE BASIS"` both instance copies → **zero hits** (the complete set retired; MR-WI025-1). *(Deviation, recorded: the design stencils' retirement statements read "STALE BASIS retired:", which greps as a hit. Reworded to "Stale basis retired:" in all three docs, both copies — content identical, marker string gone; grep-zero holds.)*
- [x] Headline doc block (:49-70): re-baseline to the expected executed values (total $12.6389B, LCOE $203.647, magnet share 50.03%; p_net/q_eng/rec_frac lines unchanged); append the WI-025 history line (forward-computed the last three pass-through accounts, retiring the final STALE BASIS annotations). Final numbers confirmed against the Phase 5 execution. *(WI-024 history clause gained its ~$201.47/MWh closing value; WI-025 line appended with $12.60B -> $12.64B, ~$203.65/MWh. Note: the history line's "STALE BASIS annotations" phrase reads "STALE\n BASIS" across a line break, so the single-line grep stays zero.)*
- [x] Apply every edit, region-identical, to the staged twin; full-file `diff` → **only the known viability-assert divergence remains**. *(Applied via git apply of the canonical patch; diff shows only the viability-assert block.)*
- [x] Full validation: env sourced, `uv run agentic-mbse validate models --complete` → **L1 = 0 over 22 files; offender list exactly the 6 pre-existing** — `ife_plant.sysml:33/41`, `hif_plant.sysml:205`, and the three `mfe_plant.sysml` offenders content-identical at the design-predicted shifted lines (**:353→389, :359→395, :364→400**), zero new, no diagnostic names a WI-025 element. Compare the offender list, not level-summary flags. **Do not gate on the staged-subset run** (documented quirk — canonical set only). *(Exactly 6 ERRORs, content-identical, mfe_plant at :389/:395/:400 as predicted; L1 22/0; L3 0 cycles; L5 100% doc coverage; summary flags L2 ❌/L6 ❌ from the known pre-existing attribution — offender list is the bar.)*

**Test requirements**: the full-ladder offender-list compare is this phase's regression test.

**Validation checkpoint**: mirroring diffs + L1–L6 offender-list bar met exactly; zero STALE BASIS hits.

**Completion gate**: all instance edits present in both twins with their MR-4 citations; ladder bar exact. Any new offender is stop-and-diagnose, not proceed.

## Phase 4 — Regen (unfiltered snapshot + V11 bridge)

**Overview**: regenerate the pipeline artifacts from the staged models. Generated files and the snapshot move only through regen — never hand-edited.

**Design reference**: design "Proposed Design §5. Regen" and "Research Findings — Snapshot/codegen mechanics" (the expected key-diff surface, offender count, auto-impl classification); risk rows "Regen run with `--design-path-filter`" and "Regen clobbers the WI-022 handwritten impl".

**Checklist**:

- [x] Pre-regen: confirm `preserve_handwritten=True` still at `exploration/stellarator_e2e/bridge_v11_generate.py:108`; confirm the WI-022 impl hash still `8d23574793c34314c67b68b8e0f4ec438d3e2d9f92060eb4094a8d46c0794a9f` (`sha256sum generated/handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py`). *(Both confirmed.)*
- [x] Pre-regen: confirm `~/1cfe/sysml-codegen` HEAD is still `6db3212`. If it moved, run the design's control first — unedited-tree snapshot + bridge must reproduce exactly 3 offenders before regenerating from the edited tree. *(HEAD `6db3212`; its working tree carries uncommitted mods (pre-existing, same state as plan-time verification); the 3-offender bridge control passed, so no control re-run needed.)*
- [x] Env: `cd ~/1cfe/sysml-codegen && set -a && source ~/1cfe/fusion-tea/.env && set +a`.
- [x] Snapshot the staged models with **NO `--design-path-filter`** (the documented gotcha): `sysml-codegen snapshot -m <staged models dir> -o /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/stellarator.snapshot.json` — plain, unfiltered, the WI-022/023/024 flow. *(Written; warnings only the known cross-part manual_required set.)*
- [x] Bridge: `uv run python /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/bridge_v11_generate.py` (from the sysml-codegen dir) → **exactly 3 V11 offenders** (`contingency__direct_subtotal`, `indirect__direct_cost`, `lcoe_calc__total_capital`), bridged, 0 after bridge, package emitted. **On 8+ offenders: stop**, re-run the unedited-tree control, surface before proceeding. *(Exactly 3, the known rollup keys; 0 after bridge; package emitted.)*
- [x] Verify generated-inputs key diff (design expected surface): `generated/inputs/system_design.json` **+8** leaves — the 6 `buildings_cost__*_base` at the instance $ values, `precon_cost__fixed_precon` 32000000.0, `om_cost__om_ref` 54900000.0 — and **`lcoe_calc__annual_om` gone** (the −4 includes the 3 known `mfe_plant__…__p_th/p_the/p_et` glue fields, the post-run regen-reset re-added by runner glue — WI-023/024 record); `mfe_plant_params.json` **+13** defaulted-input leaves (per-calc `n_mod`s, `buildings_cost` refs, land constants, `om_cost__alpha`, `om_cost__om_direct`, `ref_net_power`s). *(Exact match, both files; bridge keys in the expected placeholder transit state pending the Phase 5 run.)*
- [x] Verify the pipeline yaml wires the chains: buildings powers ← `pb__p_et/p_the/p_th` + `fusion__p_fus`; precon/om `p_net` ← `pb__p_net`; `lcoe_calc.annual_om` ← `om_cost__annual_om.root` (the spike-proven attribute-mediated chain). *(All confirmed in `generated/pipelines/mfe_stellarator.yaml` :289-341.)*
- [x] Verify the **3 new impls** are `AUTO_IMPLEMENTED = True` (pure arithmetic, no handwritten stubs) and `IMPLEMENTATION_BACKLOG.md` still lists exactly 1 function (DT_Fusion_Power). *(All three True; backlog "Total: 1 functions". Emitted statement forms captured for the Phase 5 oracle mirror.)*
- [x] Verify WI-022 handwritten-impl **content** survival (existence is not enough): `dt_fusion_power_impl.py` hash identical to the pre-regen record; `AUTO_IMPLEMENTED = False` intact. *(Hash `8d2357…794a9f` unchanged; False intact.)*
- [x] Confirm zero hand-edits under `generated/` or in the snapshot (`git status` shows only regen-produced changes). Known regen-resets are re-applied by runner glue on execute — **diff `generated/` after a Phase 5 run, not straight after regen** (WI-023 record). *(git status: only regen-produced modifications + the 3 new impl files.)*

**Test requirements**: the verify checkboxes are this phase's tests.

**Validation checkpoint**: 3 offenders exactly; +8/+13 key surface exact with `lcoe_calc__annual_om` gone; 3 auto-impls; backlog still 1; WI-022 impl content-identical; no hand-edits.

**Completion gate**: all regen verifications pass. If the handwritten impl changed: stop, restore from git, diagnose — never re-fill by hand.

## Phase 5 — Oracle + runner re-baseline, bit-exact execute

**Overview**: make the oracle compute the three accounts forward (mirroring the generated statement forms verbatim), re-target the runner's channels, glue, and headline story, and run the generated pipeline bit-exact against the oracle. The design's expected headline is the evidence anchor — any deviation is stop-and-surface, never a retarget.

**Design reference**: design **D7** (oracle IN-dict surgery, runner channel harvest, glue-2 form, headline retarget, CAS-table label change) and "Proposed Design §4" (oracle mirrors the generated statement forms verbatim — the forward forms in Research Findings are association-identical to the emitted impls); "Research Findings" expected headline (the implement evidence anchors, oracle-rollup-exact).

**Baseline anchors**: `verify_stellaris.py` — stale constants :102-108 (`buildings_capital` :102, `preconstruction_capital` :103, `annual_om` :108), rollup :195-210, return dict :223-228. `run_stellaris.py` — `BUILDINGS`/`PRECON` constants :93-94, glue-2 :193, headline block :246-262, success string, CAS table :281-283.

**Checklist**:

- [x] `verify_stellaris.py` IN dict: **drop** `buildings_capital`, `preconstruction_capital`, `annual_om`; **add** the eight concept inputs (6 `bldg_*_base` sums, `precon_fixed_base` 32000000.0, `om_annual_ref` 54900000.0) plus the new defaulted constants (`bldg_p_fus_ref` 2300.0, `land_intensity` 0.25, `land_cost` 10000.0, `ref_net_power` 1000.0, `om_alpha` 0.5, `om_direct` 0.0), with WI-025 comments; **reuse** the existing `p_th_ref` 2500 and `p_et_ref` 1100 entries (design D7 — verify they exist before adding duplicates). *(Both existed at :93 and were reused — p_et_ref serves p_the_ref too, same 1100.0, commented.)*
- [x] `verify_stellaris.py`: compute the three accounts mirroring the generated statement forms **verbatim** (check against the emitted impl bodies from Phase 4 — the WI-024 parenthesization-check precedent); feed the rollup (:195-210) from the computed values where the constants sat; expose all three in the return dict for the runner's per-channel checks (planned this item — the WI-024 deviation-3 precedent, now a first-class step). *(Emitted bodies read from the three impl files; oracle mirrors their parenthesization exactly. Return keys `buildings`/`precon`/`annual_om` — the old `preconstruction` key renamed to match CH.)*
- [x] `run_stellaris.py`: **delete** the `BUILDINGS`/`PRECON` harness constants (:93-94); add `buildings` / `precon` / `annual_om` channels to `CH` (keys named to match the oracle dict keys so the check loop picks them up — the WI-024 deviation-2 lesson, planned this item); glue-2 (:193) becomes `direct = powercore + bop + a[CH["buildings"]] + a[CH["precon"]] + SPECIAL` (the SPECIAL-harvest precedent).
- [x] `run_stellaris.py`: per-channel bit-exact checks for all three new account channels vs the oracle (SV-032's "computed output" witness). *(Dedicated check loop after the per-account block.)*
- [x] `run_stellaris.py` headline block (:246-262) + success string: rewrite the comment story for WI-025 (three accounts forward-computed, STALE BASIS retired; WI-024 values as the "was" line); retarget asserts to the WI-025 headline (total ≈ 12.64 $B, LCOE ≈ 203.6 $/MWh; p_net/q_eng/rec_frac/magnet targets unchanged).
- [x] `run_stellaris.py` CAS table (:281-283): rows 21/10 read the harvested channels and drop the "(pass-thru)" labels; row 27 (SPECIAL) keeps its pass-through label — it is not this item's scope.
- [x] Execute: `cd exploration/stellarator_e2e && /home/reid/1cfe/fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python run_stellaris.py` → **bit-exact vs the updated oracle at rel 1e-9 on every channel including the three new account channels**, per-account capital, rollup, LCOE; headline checks green. *(Zero failures; ALL CHECKS PASSED.)*
- [x] Verify the executed values against the design's expected headline (evidence anchors, not targets to fit): CAS21 **$640,475,006.17**, CAS10 **$34,391,496.77**, CAS70 **$52,517,269.06/yr**; total **$12,638,857,665.74** (+0.296%), LCOE **$203.647152/MWh** (+$2.1751); denominator invariant — p_net **915.081088**, q_eng **6.606662**, rec_frac **0.151362**; magnet capital **$6,323,469,946.33** and share ≈ 50.03%; V/p_fus/p_th/p_et unchanged. *(Executed: buildings 640,475,006.165738 / precon 34,391,496.769624 / annual_om 52,517,269.060943; direct 9,247,944,633.471426; total 12,638,857,665.744282; LCOE 203.647152; p_net 915.081088 / q_eng 6.606662 / rec_frac 0.151362; magnet 6,323,469,946.334225 (50.03%); V 425.000014 / p_fus 2748.056877 / p_th 3238.120923 / p_et 1078.294267 unchanged — every anchor hit exactly.)*
- [x] Confirm the Phase 3 headline-doc numbers match the executed values in both model copies (on any mismatch fix both copies, re-run L1, surface the discrepancy in the record). *(Headline $12.64B / $203.647 / 50.03% match the executed values at stated precision.)*

**Test requirements**: the rel-1e-9 compare is the integration test; the headline asserts are the sanity band.

**Validation checkpoint**: run output — zero rel-1e-9 failures, all headline checks green, executed values recorded for Phase 7.

**Completion gate**: bit-exact pass at the design's expected values. Any deviation from the expected table is stop-and-surface (the same oracle produced both).

## Phase 6 — Handshake successor bar + regressions

**Overview**: land the one D6 injection-map edit under the standing successor bar and prove Anchor A still reproduces byte-identically; then the unrelated-surface regressions. The design concluded no edit outside the injection map is forced — this phase proves it or stops.

**Design reference**: design **D6** (channel-by-channel safety trace: the vanished `lcoe_calc__annual_om` leaf forces the one edit, which lands inside `set_1cfe_inputs`; the new `buildings_cost__cost`/`precon_cost__cost` channels are consumed by nothing in the handshake — glue :369-371 keeps feeding 1cfe's own `costs_musd` and stays untouched; report byte-identical) and "Validation Plan" items 5–6. Owner authorization: spec §Checkpoint Rulings, Ruling 3.

**Baseline anchors**: `handshake_1costingfe.py` — `set_1cfe_inputs` :153, `lcoe_calc__annual_om` injection :243 (the edit), rollup-glue 1cfe pass-through reads :369-371 (**untouched — outside the injection map**), tautological pass-through rows :422-426 (untouched).

**Checklist**:

- [x] Edit **only within the `set_1cfe_inputs` injection map**: replace :243 `f"{P}lcoe_calc__annual_om": refs["annual_om_unlevelized_musd"] * M,` with the D6 identity injection — `f"{P}om_cost__om_ref": 0.0` in the sd block and `f"{P}om_cost__om_direct": refs["annual_om_unlevelized_musd"] * M` in the mp block (defaulted-input keys are settable there — the `blanket_cost__alpha` precedent) — plus the edit comment (the chain computes `0.0·(p_net/1000)^0.5 + v = v`, exact in IEEE arithmetic; WI-024 D7 executed precedent). **No comparison-logic change anywhere in the script; glue :369-371 and rows :422-426 untouched.**
- [x] `git diff exploration/stellarator_e2e/handshake_1costingfe.py` shows only injection-map hunks inside `set_1cfe_inputs`, nothing else. **If the run forces any edit outside the injection map: STOP — blocker, owner escalation per Ruling 3, never absorbed.** *(Two hunks, both inside `set_1cfe_inputs` (sd block :239 region, mp block :294 region); no edit outside the injection map was forced — escalation not triggered, as D6 concluded.)*
- [x] Run: `cd exploration/stellarator_e2e && /home/reid/1cfe/fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python handshake_1costingfe.py` → clean run, generated inputs restored. *(Clean; "[cleanup] restored generated input JSONs + pipeline YAML".)*
- [x] `git diff exploration/stellarator_e2e/handshake_comparison.json` → **empty** (SV-025 power channels + SV-026 account gap byte-identical). Non-empty diff is stop-and-surface — never reconcile by editing comparison logic. *(0 diff lines — byte-identical.)*
- [x] IFE regression SV-023: run `exploration/ife_e2e/run_anchors.py` (exec-venv interpreter) — anchors unchanged: **252.30 / 68.69 / 270.12 $/MWh; Meier 4.735 c/kWh** (no IFE file touched). *(252.29996307 / 68.69020165 / 270.12117794; Meier 4.73540355; gain-100 perturbation 216.55528392; ALL ANCHOR CHECKS PASSED rel 1e-6.)*
- [x] Model-test tally unchanged vs the spec's operative baseline: env sourced, `uv run pytest tests/models/ -q` → **11 failed / 18 passed / 14 skipped / 0 errors** (twice-verified environmental baseline; the bar is tally-unchanged, not green — baseline re-record is WI-026, out of scope). *(Exactly 11/18/14/0; FAILED set = 1 test_foundation + 10 test_power_balance IDs, the recorded pre-existing stale-path debt profile.)*

**Test requirements**: handshake byte-identity and SV-023 are the regression suite for this item.

**Validation checkpoint**: empty `handshake_comparison.json` diff; injection-map-only script diff; anchors exact; pytest tally identical.

**Completion gate**: all gates pass with the handshake edit confined to the injection map. The Ruling-3 escalation path is the only exit from a forced out-of-map edit.

## Phase 7 — Close-out records, final integration & validation

**Overview**: flip SV-032 with the executed record, land the headline records, and verify every spec Success Criterion. SV-030/SV-031 are not touched (Ruling 2). Item close and commit are **not** steps here (owner-held / orchestrator-held).

**Design reference**: design "Validation Plan" item 7; spec Success Criteria 1–5 and Checkpoint Ruling 2.

**Checklist**:

- [x] SV-032 → passing: `uv run agentic-mbse pm update-validation SV-032 --status passing`; update the `modeling_project/VALIDATION_MATRIX.md:58` row with an EXECUTED block carrying the Phase 5 values (the three account values, direct/total capital, LCOE; denominator invariance p_net/q_eng/rec_frac and magnet capital unchanged to the cent; handshake byte-identical under the successor bar; L1–L6 offender list = 6 pre-existing; WI-022 impl content-hash survival) — the SV-030/031 EXECUTED-block convention. *(EXECUTED block appended to the criteria cell; CLI flip successful.)*
- [x] Confirm SV-030 and SV-031 rows untouched (`git diff` shows no change to their rows — Ruling 2: historical records stand). *(Matrix diff = the SV-032 row only.)*
- [x] Confirm SV-016 untouched entirely (q_eng did not move; spec Out of Scope — no note, no reword). *(No SV-016 change in the diff.)*
- [x] Headline records: instance doc block confirmed at Phase 5 (both copies); update `.project/CURRENT_WORK.md` to the WI-025 executed headline (all three STALE BASIS annotations retired; mark NOT closed / NOTHING committed). *(New top entry in Active Work.)*
- [x] Append the Implementation Record to this plan (section below — executed values, validation results, deviations/judgment calls, quarantine transparency note).

**Final integration & validation** (spec Success Criteria, verified explicitly):

- [x] **SC-1 / SV-032**: the three accounts are computed outputs tracking the model's computed powers (runner per-channel checks), mirroring the pinned formulas exactly; executed headline recorded; bit-exact rel 1e-9 (Phase 5); denominator and magnet capital unchanged. *(buildings/precon/annual_om channels all OK at rel 1e-9; SV-032 passing with the EXECUTED block.)*
- [x] **SC-2 (MR-WI025-2)**: exactness stands proven — the design-stage 1cfe-side evaluation (CAS21/CAS70 bit-identical at f64, CAS10 1 ulp) is the record; the implement-side witness is the oracle mirroring the generated statement forms verbatim with the bit-exact gate (Phase 5). *(Oracle mirrors checked against the three emitted impl bodies; zero rel-1e-9 failures.)*
- [x] **SC-3 (MR-WI025-5)**: L1–L6 offender list = the 6 pre-existing at the shifted lines, zero new (Phase 3); regen with WI-022 handwritten-impl content survival, 3 offenders, +8/+13 surface (Phase 4); bit-exact rel 1e-9 (Phase 5); IFE anchors and pytest tally unchanged (Phase 6); mirroring per-edit-region (Phases 1–3).
- [x] **SC-4**: SV-025/026 byte-identical under the successor bar — empty `handshake_comparison.json` diff, edit confined to the injection map; no out-of-map edit was forced (or it was escalated, never absorbed) (Phase 6). *(No out-of-map edit forced — D6's conclusion held.)*
- [x] **SC-5 (MR-WI025-3/4/6)**: zero STALE BASIS hits in both instance copies; each account's doc states the powers it tracks and the preserved convention (CAS10 pre-contingency, CAS21 raw, CAS70 unlevelized; DT/FOAK/n_mod = 1 frozen); every changed value carries an MR-4 Source/Ref/Basis citation resolving to 1costingFE @ `0254385` file:line; no ARIES-CS-informed source read or cited (inspect the Phase 1–3 doc stencils; quarantine note in the record). *(All doc stencils from the approved design, cites re-verified against the pin; grep-zero on both copies.)*

**Completion gate**: every Success Criterion checked; SV-032 passing with the executed record; SV-030/031/016 untouched; records written. Then stop — hand back to the orchestrator (audit → owner close → commit).

---

## Feasibility Concerns

| concern | disposition |
|---|---|
| Ruling-3 escalation (handshake edit forced outside the injection map) | Design D6 concludes not triggered — the only forced edit (the vanished `lcoe_calc__annual_om` leaf) lands inside `set_1cfe_inputs`; the new account channels are consumed by nothing in the handshake. Phase 6 gate: if reality disagrees, STOP and escalate to the owner — pre-agreed path, never absorbed |
| Regen run with `--design-path-filter` → 8 spurious offenders | The carried WI-024 gotcha. Phase 4 command is unfiltered by instruction; hard control gate: bridge reports exactly 3 offenders or the phase stops and runs the unedited-tree control |
| sysml-codegen HEAD moves before implement | Verified still `6db3212` at plan time; Phase 4 re-checks and runs the control first if it moved |
| Oracle/impl statement-form drift breaks bit-exactness | Oracle mirrors the generated statement forms verbatim, checked against the Phase 4 emitted impl bodies (WI-024 parenthesization-check precedent); runner gates every channel at rel 1e-9 including the three new ones |
| Regen clobbers the WI-022 handwritten impl | `preserve_handwritten=True` re-verified at plan time (bridge_v11_generate.py:108); content hash recorded (`8d2357…794a9f`) and checked pre/post-regen; stop-and-restore on mismatch |
| Executed numbers differ from the design's expected headline | Very low — the expected values are oracle-rollup-exact and the same oracle is the implement gate; any deviation is stop-and-surface, never a silent retarget (Phase 5 gate) |
| Implement gates on the staged-subset validation and chases the reclassified precon message | Documented quirk (design Research Findings): the 5-error staged-subset set re-classes one entry, count unchanged. The bar is `validate models --complete` on the canonical set — Phases 1–3 say so explicitly |
| Offender line numbers shift | Design predicts :353→389/:359→395/:364→400 from the inserted generic-plant block. The bar is content-identity of the offender list; numbers orient only (WI-024 precedent, match-on-content) |
| `mfe_plant.sysml` staged twin not byte-identical | Known WI-015 DEMO NOTE divergences (3 regions); the Phase 2 gate is "only known divergences remain, edit regions byte-identical" — all WI-025 edit regions sit outside them (design D7, patch-proven both trees) |
| Instance twin not byte-identical | Known viability-assert divergence only; same per-edit-region gate (Phase 3) |
| pytest red at baseline | Pre-existing, unrelated; the operative bar is tally-unchanged vs **11/18/14/0** (spec ruling — the twice-verified environmental baseline; re-record is WI-026, out of scope) |
| Float32 vs float64 confusion at exactness checks | The pipeline and oracle run float64; 1cfe's runtime is float32 by its own design. The exactness record (design Research Findings) already separates the two — implement compares pipeline vs oracle at rel 1e-9, never pipeline vs 1cfe-f32 |
| n_mod frozen at 1 leaves 3 per-calc leaves for a future multi-module concept | Accepted design trade (D3), documented at the bindings — no plan action |
| Traceability matrix | Three calc-def rows added (Phase 1, the codebase-sourced row convention); instance literals record citations in model doc comments per the WI-020→024 lineage — no per-literal matrix rows |

---

## Implementation Record

**Implemented 2026-07-18.** All seven phases executed in order; every gate passed on first run. No escalation triggered — the D6 handshake conclusion held (no edit outside the `set_1cfe_inputs` injection map was forced). Item NOT closed and NOTHING committed (owner-held / orchestrator-held, per the plan header).

**Model change (as designed, D1–D7):**
- Library (`models/library/analyses/mfe_account_costs.sysml` + byte-identical staged twin, 303 → 417 lines): three calc defs appended from the design §1 stencils verbatim — `'Buildings Cost'` (6 base-sum + 4 power inputs; defaulted n_mod 1.0 / p_fus_ref 2300 / p_the_ref 1100 / p_th_ref 2500 / p_et_ref 1100), `'Preconstruction Cost'` (fixed_precon + p_net; defaulted n_mod / land_intensity 0.25 / land_cost 10000 / ref_net_power 1000), `'Annual OM Cost'` (om_ref + p_net; defaulted n_mod / ref_net_power / alpha 0.5 / om_direct 0.0). Three traceability-matrix rows added (`data/traceability_matrix.csv`, codebase-sourced convention).
- Generic plant (`models/designs/generic_mfe/mfe_plant.sysml` + staged twin, region-identical): buildings part → turbine idiom (`:>> capital_cost = buildings_cost.cost`), `preconstruction_capital` and `annual_om` → attribute-mediated chains (`= precon_cost.cost` / `= om_cost.annual_om`); 8 concept-input attributes + 3 calc usages after the misc_cost block (self-named p_the/p_th/p_et alias chains, dotted `fusion.p_fus` and `pb.p_net`). `direct_capital`/`total_capital`/`lcoe_calc`/rollup calcs untouched (offender lines content-identical, line-shifted).
- Stellaris instance (`models/designs/stellarator_09/stellarator_plant.sysml` + staged twin, region-identical): the three stale literals ($613.65M / $33.896M / $41.641M/yr) replaced by the 8 cited bindings — six `bldg_*_base` sums (168.5 / 288 / 9 / 58 / 26 / 29 M$ × 1e6, each with its full member-building MR-4 doc, yaml line cites re-verified against the pin), `precon_fixed_base` 32 M$ × 1e6, `om_annual_ref` 54.9 M$/yr × 1e6; each doc states the powers the account now tracks and the preserved convention (CAS21 raw, p_the = p_et no-DEC; CAS10 pre-contingency, CAS29 applies once; CAS70 unlevelized, CAS71/72 Stage-3), with the old stale basis stated in the retirement note. Headline doc re-baselined ($12.64B / $203.647 / 50.03%) + WI-025 history line. **STALE BASIS grep-zero in both copies.**

**Regen (never hand-edited):** unfiltered snapshot (NO `--design-path-filter`) over the staged models at sysml-codegen `6db3212` → `bridge_v11_generate.py`. **Exactly 3 V11 offenders** (contingency__direct_subtotal, indirect__direct_cost, lcoe_calc__total_capital), bridged, 0 after bridge, package emitted. `system_design.json`: +8 (6 `buildings_cost__*_base`, `precon_cost__fixed_precon` 32000000.0, `om_cost__om_ref` 54900000.0), `lcoe_calc__annual_om` gone; `mfe_plant_params.json`: +13 defaulted-input leaves. Pipeline yaml chain-wires buildings ← pb__p_et/p_the/p_th + fusion__p_fus.root, precon/om ← pb__p_net, lcoe_calc.annual_om ← om_cost__annual_om.root. Three new impls AUTO_IMPLEMENTED = True; `IMPLEMENTATION_BACKLOG.md` still exactly 1 function. WI-022 handwritten impl **content-hash unchanged** through regen (sha256 `8d235747…794a9f` before and after; AUTO_IMPLEMENTED = False intact). Post-run, the bridge keys carry the WI-025 executed rollup (9,247,944,633.47 / 12,638,857,665.74) and the 3 glue schema fields are re-added — the committed post-run state pattern.

**Executed headline (bit-exact vs oracle, rel 1e-9, zero failures, incl. the three new account channels):** CAS21 buildings **$640,475,006.165738**, CAS10 preconstruction **$34,391,496.769624**, CAS70 annual O&M **$52,517,269.060943/yr**; direct **$9,247,944,633.471426**, total **$12,638,857,665.744282** (+0.296%), **LCOE $203.647152/MWh** (+$2.1751). Denominator invariant: p_net **915.0810878595104**, q_eng **6.606662**, rec_frac **0.151362**, p_cryo 0.864352, V 425.000014 / p_fus 2748.056877 / p_th 3238.120923 / p_et 1078.294267 — all unchanged; magnet **$6,323,469,946.334225** (share 50.03%) identical to the WI-023/024 record to the cent. Every value matches the design's oracle-rollup-exact expected table exactly (evidence anchors hit, nothing fitted).

**Validation:**
- L1 = 0 over 22 files after every model phase; L3 0 cycles; L5 100% doc coverage; full ladder offender list = **exactly the 6 pre-existing** — `hif_plant.sysml:205`, `ife_plant.sysml:33/41`, and the three `mfe_plant.sysml` derived-expression offenders printed at **:389/:395/:400** (the design-predicted +36 shift from the inserted WI-025 attribute/calc block; content identical), zero new, no diagnostic names a WI-025 element. Summary flags L2 ❌/L6 ❌ from the known pre-existing attribution (WI-023/024 precedent). Transient Phase-1 "Unused calc def" WARNs (×3) cleared when the Phase-2 usages landed. Staged-subset run not gated (documented quirk).
- Mirroring: library twins byte-identical; generic-plant twin diff = only the 3 known WI-015 DEMO NOTE divergences; instance twin diff = only the viability-assert block. All WI-025 edit regions byte-identical across twins.
- Handshake (standing successor bar, Ruling 3): `handshake_1costingfe.py` edited **only** within the `set_1cfe_inputs` injection map — two hunks: sd block replaces the vanished `lcoe_calc__annual_om` injection with `om_cost__om_ref: 0.0`; mp block adds `om_cost__om_direct: refs["annual_om_unlevelized_musd"] * M` (IEEE-exact identity path, WI-024 D7 precedent). No comparison-logic change; glue :369-371 and pass-through rows untouched. Run clean; `git diff handshake_comparison.json` **empty** (SV-025/026 byte-identical).
- IFE SV-023: ALL ANCHOR CHECKS PASSED rel 1e-6 (252.29996307 / 68.69020165 / 270.12117794 $/MWh; Meier 4.73540355 c/kWh; gain-100 perturbation 216.55528392 moved as expected).
- Pytest: **11 failed / 18 passed / 14 skipped / 0 errors** — tally identical to the spec's operative baseline; FAILED set = 1 test_foundation + 10 test_power_balance IDs (the recorded pre-existing stale-path debt profile).
- SV-032 → **passing** with the EXECUTED block (matrix row appended per the SV-030/031 convention). SV-030/SV-031 rows untouched (matrix diff = the SV-032 row only; Ruling 2). SV-016 untouched entirely (q_eng did not move). `.project/CURRENT_WORK.md` headline updated (NOT closed / NOTHING committed).

**Deviations / judgment calls (all surfaced, none absorbed):**
1. **"STALE BASIS" grep-zero vs the design stencil wording.** The design §3 stencils phrase the retirement notes "STALE BASIS retired: …", which greps as a hit against the plan's grep-zero gate. Reworded to "Stale basis retired:" in all three docs (both copies) — content identical, marker string gone. The headline history line's "…retiring the final STALE BASIS annotations" happens to split "STALE / BASIS" across a line break, so the single-line grep is zero there too; noted for transparency, not engineered to evade the gate's intent (it is a history statement, not a live annotation).
2. Generic-plant buildings part written in the multi-line part-body form (matching the sibling turbine/electric_plant parts) rather than the design bullet's one-line form — formatting only, parse-identical; the resulting offender-line shift (+36) matched the design's spike prediction exactly.
3. Oracle return-dict key `preconstruction` renamed to `precon` to match the runner CH key (the WI-024 deviation-2 lesson, planned this item as "keys named to match"); `buildings`/`annual_om` added. Only `run_stellaris.py` consumes the oracle dict — grep-verified.
4. Section-header comment above the buildings region ("PASS-THROUGH DIRECT ACCOUNTS") retitled to the CAS21 forward-computed region comment, and the CAS10/CAS27 lead comment amended to say CAS10 forward (WI-025) / CAS27 forward (WI-021) — corrections amend the stale pass-through wording rather than accreting beside it (capture-fidelity law 3).
5. `~/1cfe/sysml-codegen` working tree carries uncommitted modifications (HEAD `6db3212` as required; same state as the plan-time verification). The 3-offender bridge control passed, so the unedited-tree control procedure was not triggered.

**Quarantine transparency:** no grep in this session matched lines under `knowledge/holdout/**` or any PROTOCOL §3 barred path; no barred artifact was read or cited. Sources touched: the spec/design/plan artifacts, the pinned 1costingFE checkout (`/home/reid/1cfe/1costingfe` @ `0254385`, read-only — `costs.py` :52-80/:83-144/:319-357 and `costing_constants.yaml` :8/:12/:15-23/:175-197/:272, re-verifying the doc cites), and repo model/pipeline files. PROTOCOL.md itself read as Required Reading.

**Handed back to the orchestrator**: `/audit-models` → owner `pm close-item WI-025` → commit.
