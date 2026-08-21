---
Status: complete
Created: 2026-07-18
Updated: '2026-07-18'
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-024 Plan: Recirculating-Power Derivation — Cryoplant Electrical Chain

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — demo model-development session; §3 barred paths must not be read, cited, or opened.

Owner rulings (all recorded in spec §Checkpoint Rulings; no further owner stop before close): Ruling 1 ratified Option (a) — cryo-electrical derivation only, other slots untouched. Ruling 2 delegated slot placement, double-counting resolution, COP treatment, winding-volume route, and unprinted-loads treatment to design (resolved as D1–D6, design approved). Ruling 3 accepted the D7 handshake successor bar ([OWNER] 2026-07-18, post-design): `handshake_1costingfe.py` edited only within the `set_1cfe_inputs` injection map, no comparison-logic change, `git diff exploration/stellarator_e2e/handshake_comparison.json` empty after the run — this supersedes the spec's original "handshake unedited" wording, so Phase 6 is unblocked. Item close (`pm close-item`) is owner-held; committing is orchestrator-held — neither is a plan step.

## Source Documents

- Design (primary, approved): `./design.md` — D1–D7, Proposed Design §1–5, Research Findings (spike evidence + regen gotcha), Validation Plan, expected-headline table
- Spec (contract): `./spec.md` — MR-WI024-1..6, Success Criteria 1–4, Checkpoint Rulings 1–3
- Alignment brief: `work/orchestration/recirc-power-derivation.md`
- Epic: `work/backlog/epic-mfe-cost-modeling.md`
- Executed templates: `work/completed/20260718_WI-023_magnet-field-errata-B9/plan.md` (phase spine, content-hash pattern, Implementation Record convention); `work/completed/20260718_WI-022_predictive-confinement/plan.md` (calc-def + regen precedent)

## Design Summary

One new library calc def, `'Cryoplant Electrical Power'` (`models/library/analyses/mfe_cryo_plant.sysml`), computes the cryoplant wall-plug electrical from the cold-mass heat load: `p_cold = (q_nuc·vol_cold·1e-6 + p_fixed)·f_uplift`, `cop = f_carnot·T_cold/(T_amb − T_cold)`, `p_elec = p_cold/cop + p_direct`. The generic plant gains 7 dormant chain attributes plus a `cryo_elec` usage, and the one pb rewire `in p_cryo = cryo_elec.p_elec` lands the derived value in the `p_cryo` slot (D1); the Stellaris instance binds the chain (q_nuc 35.5 SOURCED, vol_cold 136.56 COMPUTED, p_fixed 0.0075 SOURCED, f_uplift 1.0 D6 seam, T_cold 20 SOURCED, T_amb 300 assumption, f_carnot 0.20 THE assumption, p_cryo direct term 0.0 — the 1cfe 0.8 default retired, D2) and rescopes `p_tf = 0.0` from stopgap to modeled zero. Expected executed headline (oracle-exact, design Research Findings table): **p_cryo 0.8643516, p_net 915.081088, q_eng 6.606662, rec_frac 0.151362, LCOE 201.472065; V/p_fus/p_th/p_et and all capital unchanged to the cent**.

## Prototype Baseline (from the design Validation Report, re-verified at plan time)

- **End-to-end spike: PASS** (design-stage, scratch copy of the staged tree — no repo file touched): L1–L3 clean parse; snapshot classified `cryo_elec` as 8 literal leaves + `pb.p_cryo` chain → `cryo_elec.p_elec`; bridge produced **exactly 3 V11 offenders**, package emitted; generated `cryoplant_electrical_power_impl.py` AUTO_IMPLEMENTED; executed bit-equal to the oracle mirror at the Stellaris point (`0.8643515999999999`) and exactly `0.8` at the handshake identity point (D7's executed proof); generated-inputs key diff exactly the designed surface (+8 `cryo_elec__*`, −`pb__p_cryo`, −3 known glue fields).
- **Plan-time re-verifications (at `1237f1c5`):** sysml-codegen HEAD still `6db3212` (the spike-verified commit); `preserve_handwritten=True` still set at `exploration/stellarator_e2e/bridge_v11_generate.py:108`; WI-022 handwritten impl sha256 `8d23574793c34314c67b68b8e0f4ec438d3e2d9f92060eb4094a8d46c0794a9f` (identical to the WI-023 record); SV-031 registered `pending` in `modeling_project/VALIDATION_MATRIX.md:57`.
- **Level 4–6 issues:** none introduced; the L1–L6 bar everywhere below is L1 = 0 over the **22-file** set (21 + the new library file), offender list exactly the 6 pre-existing (`mfe_plant.sysml:329/335/340`, `ife_plant.sysml:33/41`, `hif_plant.sysml:205`), zero new — **compare the offender list, not level-summary flags** (the validator prints the hif offender under its L2 section; verified pre-existing at WI-023).
- **Known twin divergences (mirroring gates account for these):** `stellarator_plant.sysml` staged twin — the commented-out viability-assert block only (WI-023 record). `mfe_plant.sysml` staged twin — three DEMO NOTE divergences (direct_capital and total_capital converted to plain inputs; assert-constraint blocks commented out; WI-015 findings), verified present at plan time at staged lines 340–349/370–374/399–405. All WI-024 edit regions sit outside the divergent regions.
- **Regen-flow gotcha (design Research Findings):** `sysml-codegen snapshot` run with `--design-path-filter stellarator_09` drops the analyses/generic-plant attribute groups and produces 8 spurious V11 offenders. The snapshot at Phase 4 must be **unfiltered**. Control: the bridge must report exactly 3 offenders; on 8+ stop and run the design's control procedure (unedited-tree snapshot + bridge) before touching anything.

## Phasing Approach

Seven phases, the design's Implementation Checklist order: library calc def → generic plant → instance → regen → oracle/runner → handshake/regressions → close-out. Library before usages, generic plant before the instance that overrides its attributes (bottom-up). **Canonical and staged twins are edited together within each model phase** (Phases 1–3), with the mirroring diff checked at each phase — not deferred to a separate mirror phase — because the staged tree is what the Phase 4 snapshot reads. Model edits precede regen (the snapshot bakes bindings); oracle edits precede the execute (the runner gates bit-exact against the oracle); the handshake injection edit comes after the bit-exact execute so it lands on a proven pipeline.

**Line numbers below are pre-edit anchors, verified current at `1237f1c5`.** Two design-doc anchors drifted (STALE BASIS blocks: design said :510/:557, current :518/:562) — match edits on content, use the numbers to orient.

## Validation Strategy

- **Per phase:** L1–L3 after every model-file edit (Phases 1–2); full L1–L6 offender-list compare + mirroring diffs after all model edits (Phase 3); regen self-checks (Phase 4); bit-exact execute (Phase 5); handshake byte-identity + IFE/pytest regressions (Phase 6).
- **Environment:** all Python via `uv run` — never bare python. License via `set -a && source ~/1cfe/fusion-tea/.env && set +a` before any validate/snapshot/bridge invocation. Validation via `uv run agentic-mbse validate models --level N` / `--complete` (syside has no standalone CLI in this venv). Pipeline execution and handshake use the exec-venv interpreter directly (by design): `/home/reid/1cfe/fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python`.
- **Final:** spec Success Criteria 1–4 verified explicitly in Phase 7; SV-031 → passing with executed values; q_eng recorded against SV-016 with the band untouched.

---

## Phase 1 — Library calc def (canonical + staged, identical)

**Overview**: create the one new library file carrying the concept-agnostic calc def. First because everything downstream imports it.

**Design reference**: design "Proposed Design §1. Library calc def" (the complete file stencil — use it verbatim, including the doc comment with the MR-4 Source/Ref/Basis block), decisions **D3** (additive `p_direct`, no conditional; dormant-safe defaults; `f_carnot` defaults 1.0 per the WI-022 `T_i0` precedent) and **D4** (Carnot × fraction form).

**Files**: NEW `models/library/analyses/mfe_cryo_plant.sysml`; NEW `exploration/stellarator_e2e/models/analyses/mfe_cryo_plant.sysml` (staged twin, byte-identical).

**Checklist**:

- [x] Create `models/library/analyses/mfe_cryo_plant.sysml` from the design §1 stencil: package `mfe_cryo_plant`, `calc def 'Cryoplant Electrical Power'`, 8 `in` attributes with the dormant defaults (q_nuc 0.0, vol_cold 0.0, p_fixed 0.0, f_uplift 1.0, T_cold 20.0, T_amb 300.0, f_carnot 1.0, p_direct 0.0), intermediates `p_cold`/`cop_carnot`/`cop`, `out p_elec`, full doc comment (semantics-witness Ref to `physics.py:321-323` and `steady_state_dipole.yaml:52-53`, Basis "concept-agnostic (MR-3)").
- [x] Create the staged twin `exploration/stellarator_e2e/models/analyses/mfe_cryo_plant.sysml`, byte-identical; `diff` the two files → identical.
- [x] Add the traceability-matrix row for the new calc def (`data/traceability_matrix.csv`, WI-019 library-calc-def convention — cf. the existing `'MFE Power Balance Calc'` row): Element `'Cryoplant Electrical Power'`, File `models/library/analyses/mfe_cryo_plant.sysml`, Type calc_def, Source codebase `1costingFE @ 0254385`, Location `physics.py:321-323; steady_state_dipole.yaml:52-53 (slot semantics)`.
- [x] Validate: `set -a && source ~/1cfe/fusion-tea/.env && set +a && uv run agentic-mbse validate models --level 1` → **22 files**, 0 errors, 0 warnings; then `--level 2` and `--level 3` clean for the new package. *(L1: 22 files, 0/0. L3: 0 circular deps. L2: only the pre-existing `hif_plant.sysml:205` offender plus a transient WARN "Unused calc def: 'Cryoplant Electrical Power'" — expected until the Phase 2 usage lands; re-checked clean after Phase 2.)*

**Test requirements**: none new beyond the L1–L3 checkpoint — the calc def's structural test is the Phase 4 snapshot classification and the Phase 5 bit-exact execute (spike-proven).

**Validation checkpoint**: L1 = 0 over 22 files; L2/L3 clean; twin byte-identical.

**Completion gate**: both copies exist and match the design stencil exactly; validation clean; matrix row present.

## Phase 2 — Generic plant wiring (canonical + staged, identical region edits)

**Overview**: wire the chain into the generic MFE plant — import, 7 dormant plant attributes, the `cryo_elec` calc usage, the `p_cryo` re-doc, and the single pb rewire. The power-balance calc def and the recirculating-sum formula are untouched.

**Design reference**: design "Proposed Design §2. Generic plant" (the attribute-block and calc-usage stencils), decisions **D1** (derived value lands in the p_cryo slot) and **D3** (dormant-default idiom; `in p_direct = p_cryo` makes the existing attribute the additive direct term).

**Files**: REFINE `models/designs/generic_mfe/mfe_plant.sysml`; REFINE `exploration/stellarator_e2e/models/designs/generic_mfe/mfe_plant.sysml` (same regions).

**Baseline anchors** (canonical, pre-edit): import block :2–10; power-balance input attributes :180–195 (`attribute p_cryo : Real;` at :195, comment "cryogenic pumping" — never 1cfe's semantics, `types.py:231` says "Cryogenic system power"); `calc pb` block :197–213 (`in p_cryo = p_cryo;` at :212).

**Checklist**:

- [x] Add `private import mfe_cryo_plant::*;` to the import block (:2–10).
- [x] Re-doc `attribute p_cryo : Real` (:195) → `attribute p_cryo : Real default 0.0;  // directly-specified cryoplant electrical [MW] (additive direct term, WI-024)` per design §2.
- [x] Add the seven chain attributes with dormant defaults and the block comment, per the design §2 stencil: `q_nuc_cryo 0.0`, `vol_cold_cryo 0.0`, `p_fixed_cryo 0.0`, `f_uplift_cryo 1.0`, `T_cold_cryo 20.0`, `T_amb_cryo 300.0`, `f_carnot_cryo 1.0`.
- [x] Add `calc cryo_elec : 'Cryoplant Electrical Power' { ... }` with the 8 `in` bindings per the design §2 stencil (`in p_direct = p_cryo;` last).
- [x] Rewire the one pb input (:212): `in p_cryo = p_cryo;` → `in p_cryo = cryo_elec.p_elec;`. No other pb line changes.
- [x] Apply every edit, region-identical, to the staged twin; full-file `diff` canonical vs staged → **only the three known DEMO NOTE divergences remain** (direct_capital/total_capital plain-input conversions, commented assert-constraint block); every WI-024 edit region byte-identical. *(Diff shows exactly the three known divergences, nothing else.)*
- [x] Validate: env sourced, `uv run agentic-mbse validate models --level 1` → 22 files, 0 errors; `--level 3` clean (no cycle from the new chain — dataflow is instance literals → cryo_elec → pb, design "Cross-File Bindings"). *(L1 22/0/0; L3 0 circular deps; the Phase-1 transient unused-calc-def WARN cleared — L2 issue set back to the pre-existing 3.)*

**Test requirements**: the dormant-path property (a concept binding nothing computes p_elec = 0/cop + 0 = 0) is by-construction from the defaults; the executable proof is Phase 5. No new test files.

**Validation checkpoint**: L1 = 0 over 22 files; L2/L3 clean; mirroring diff shows only the known divergences.

**Completion gate**: all six edits present in both twins; validation clean; no other pb or sum-formula line touched.

## Phase 3 — Stellaris instance bindings + docs (canonical + staged), full validation

**Overview**: bind the chain in the concept-09 instance, rescope the p_tf doc to a modeled zero, retire the 0.8 default with its double-counting doc, extend the p_tfcool coverage doc, refresh the headline, and append the STALE BASIS notes. Then run the full ladder — this is the last model-text phase.

**Design reference**: design "Proposed Design §3. Stellaris instance" (the complete p_cryo-region stencil with all eight binding docs — use verbatim; the p_tf and p_tfcool doc content specifications), decisions **D2** (retirement + disjoint reading + conservative-direction residual), **D5** (vol_cold 136.56 arithmetic and cross-checks in the binding doc), **D6** (f_uplift = 1.0 lower-bound seam, cited to the design ruling, not a fake source).

**Files**: REFINE `models/designs/stellarator_09/stellarator_plant.sysml`; REFINE `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml` (same regions).

**Baseline anchors** (canonical, pre-edit, verified at `1237f1c5`): headline doc block :49–66; mapping-traps note :68–73; `p_tf = 0.0` block :434–454; `p_tfcool = 15.0` :455–463; `p_cryo = 0.8` :464–466; STALE BASIS blocks :518 and :562 (drifted from the design's :510/:557 — match on content). Buildings STALE BASIS (:268) untouched — its basis is p_et/p_th, which do not move.

**Checklist**:

- [x] p_tf doc rewrite (:434–454): deferral stopgap → modeled zero per design §3 — SC coils draw no steady-state resistive drive (1cfe `recirc_power_factor = 0.0`, `defaults.py:611-614`); the ~7.5 kW joint dissipation is heat at 20 K inside the chain (`p_fixed_cryo`), not coil electrical; current-lead/power-supply standing losses unprinted, part of the documented lower bound; one history line compresses the WI-023 phantom-111 story; MR-4 cite raw.pdf §2.9 + defaults.py:611-614. The WI-023 forward-pointer sentences (":447–448 p_tfcool/p_cryo still carry…") resolve to their settled statements.
- [x] p_cryo region rewrite (:464–466): replace the `0.8` binding with the design §3 stencil verbatim — `:>> p_cryo = 0.0` (retirement doc, D2) plus the seven chain bindings with their full cited docs: `q_nuc_cryo = 35.5` (Table 6 image), `vol_cold_cryo = 136.56` (D5 arithmetic + both cross-checks), `p_fixed_cryo = 0.0075` (§2.9 joints), `f_uplift_cryo = 1.0` (D6 lower-bound seam), `T_cold_cryo = 20.0` (§2.9/2.8 + 1cfe corroboration), `T_amb_cryo = 300.0` (D4 standard-ambient), `f_carnot_cryo = 0.20` (THE assumption, D4 doc with the 15–30%-of-Carnot basis stated in words).
- [x] p_tfcool doc extension (:455–463): binding stays 15.0; doc gains the post-WI-024 coverage statement per design §3 (disjoint read — 1cfe carries p_cool and p_cryo side by side; undocumented upstream composition; any cryo-compressor share is a conservative-direction overlap, documented not silently resolved) — MR-WI024-3.
- [x] Headline doc block (:49–66): re-baseline to the expected executed values (p_net 915.081, rec_frac 0.15136, q_eng 6.6067, LCOE 201.472; total/magnet capital lines unchanged); append the WI-024 history line (derived the cryo parasitic load, retired the 0.8 default, rescoped p_tf to a modeled zero). Final numbers confirmed against the Phase 5 execution. *(WI-023 history entry gains its settled net 915.145 / ~$201.46 values.)*
- [x] Mapping-traps note (:68–73): unchanged unless the p_tf rescope makes a trap sentence stale — design §3 folds any change into the same rewrite; no new traps invented. *(Inspected: the three traps are r_coil/sigma_v/B — none touches p_tf; note left unchanged.)*
- [x] STALE BASIS blocks (current :518, :562): append the WI-024 move in the established style (p_net 915.145 → 915.081, negligible at the stated precision; the pass-through recompute remains the sequenced follow-on item). *(Both blocks; buildings block :270 untouched.)*
- [x] Apply every edit, region-identical, to the staged twin; full-file `diff` → **only the known viability-assert divergence remains**. *(Verified — diff shows only the assert-block divergence.)*
- [x] Full validation: env sourced, `uv run agentic-mbse validate models --complete` → **L1 = 0 over 22 files; offender list exactly the 6 pre-existing** (`mfe_plant.sysml:329/335/340`, `ife_plant.sysml:33/41`, `hif_plant.sysml:205`), zero new, no diagnostic names a WI-024 element. Compare the offender list, not level-summary flags (known hif L2-section attribution). *(Executed: L1 = 0 over 22 files; exactly 6 ERRORs — `hif_plant.sysml:205`, `ife_plant.sysml:33/41`, and the three mfe_plant derived-expression offenders now printed at :353/:359/:364 — the pre-edit :329/:335/:340 shifted by the 24 lines the WI-024 attribute/calc block inserts above them; content identical (direct_capital/bop/powercore rollup expressions), zero new, no WI-024 element named. L3/L4/L5 pass; summary flags L2 ❌/L6 ❌ from the known pre-existing attribution, as at WI-023.)*

**Test requirements**: the full-ladder offender-list compare is this phase's regression test.

**Validation checkpoint**: mirroring diff + L1–L6 offender-list bar met exactly.

**Completion gate**: all instance edits present in both twins with their MR-4 citations; ladder bar exact. Any new offender is stop-and-diagnose, not proceed.

## Phase 4 — Regen (unfiltered snapshot + V11 bridge)

**Overview**: regenerate the pipeline artifacts from the staged models. Generated files and the snapshot move only through regen — never hand-edited.

**Design reference**: design "Proposed Design §5. Regen" and "Research Findings — Snapshot-flow gotcha" (the NO `--design-path-filter` rule and the 3-offender control); risk rows "Regen run with the design-path-filter flag" and "Regen clobbers the WI-022 handwritten impl". Flow references: `exploration/stellarator_e2e/CODEGEN_FINDINGS.md:29` ("Reproduce") and `bridge_v11_generate.py` header.

**Checklist**:

- [x] Pre-regen: confirm `preserve_handwritten=True` still at `exploration/stellarator_e2e/bridge_v11_generate.py:108`; confirm the WI-022 impl hash still `8d23574793c34314c67b68b8e0f4ec438d3e2d9f92060eb4094a8d46c0794a9f` (`sha256sum generated/handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py`). *(Both confirmed.)*
- [x] Pre-regen: confirm `~/1cfe/sysml-codegen` HEAD is still `6db3212`. If it moved, run the design's control procedure first — unedited-tree snapshot + bridge must reproduce exactly 3 offenders before regenerating from the edited tree. *(Still `6db3212`.)*
- [x] Env: `cd ~/1cfe/sysml-codegen && set -a && source ~/1cfe/fusion-tea/.env && set +a`.
- [x] Snapshot the staged models with **NO `--design-path-filter`** (the documented gotcha): `sysml-codegen snapshot -m <staged models dir> -o /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/stellarator.snapshot.json` — plain, unfiltered, exactly as the WI-022/023 flow.
- [x] Bridge: `uv run python /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/bridge_v11_generate.py` (from the sysml-codegen dir) → **exactly 3 V11 offenders** (`contingency__direct_subtotal`, `indirect__direct_cost`, `lcoe_calc__total_capital`), bridged, package emitted. **If 8+ offenders appear, the flag or toolchain drifted: stop**, re-run the unedited-tree control per the design's procedure, and surface before proceeding. *(Exactly 3 — the known rollup keys; bridged; "V11 offenders after bridge: 0"; package emitted.)*
- [x] Verify generated inputs: `generated/inputs/system_design.json` carries the 8 `cryo_elec__*` leaves (q_nuc, vol_cold, p_fixed, f_uplift, T_cold, T_amb, f_carnot, p_direct at the instance values) and **no** `pb__p_cryo` key; pipeline yaml wires `p_cryo` from `…cryo_elec__p_elec`. *(All 8 present at 35.5 / 136.56 / 0.0075 / 1.0 / 20.0 / 300.0 / 0.2 / 0.0; zero `pb__p_cryo` hits; yaml:207 `p_cryo: float stellarator_09__stellaris__cryo_elec__p_elec.root`.)*
- [x] Verify `generated/.../cryoplant_electrical_power_impl.py` is `AUTO_IMPLEMENTED = True` (pure arithmetic, no handwritten stub); `IMPLEMENTATION_BACKLOG.md` still lists exactly 1 function (DT_Fusion_Power). *(AUTO_IMPLEMENTED = True at `generated/handwritten/mfe_cryo_plant/cryoplant_electrical_power_impl.py:3`; backlog table has exactly 1 unchecked function row, DT_Fusion_Power.)*
- [x] Verify WI-022 handwritten-impl **content** survival (existence is not enough): `dt_fusion_power_impl.py` hash identical to the pre-regen record; `AUTO_IMPLEMENTED = False` intact. *(sha256 identical `8d2357…794a9f`; AUTO_IMPLEMENTED = False at :31.)*
- [x] Confirm zero hand-edits under `generated/` or in the snapshot (`git status` shows only regen-produced changes). Known regen-resets (3 bridge keys → placeholder, 4 BOP power wirings → pre-glue refs, 3 harness-glue schema fields) are re-applied by runner glue on execute — **diff `generated/` after a Phase 5 run, not straight after regen** (WI-023 record). *(git status under `generated/` + snapshot: 9 paths, all regen-produced — modified `__init__.py`, `mfe_plant_params.json`, `system_design.json`, `mfe_stellarator.yaml`, `system_design.py`, `test_implementations_runnable.py`, snapshot; new `handwritten/mfe_cryo_plant/` and `modules/mfe_cryo_plant/`. No hand edits.)*

**Test requirements**: the verify checkboxes are this phase's tests.

**Validation checkpoint**: 3 offenders exactly; cryo leaves present, `pb__p_cryo` gone; auto-impl; WI-022 impl content-identical; no hand-edits.

**Completion gate**: all regen verifications pass. If the handwritten impl changed: stop, restore from git, diagnose — never re-fill by hand.

## Phase 5 — Oracle + runner re-baseline, bit-exact execute

**Overview**: mirror the chain in the oracle, add the derived-p_cryo channel to the runner, retarget the headline story, and run the generated pipeline bit-exact against the oracle.

**Design reference**: design "Proposed Design §4. Oracle + runner" (the generated statement forms to mirror **verbatim**: `cop_carnot = T_cold/(T_amb - T_cold)`; `cop = f_carnot * cop_carnot`; `p_cold = ((q_nuc * vol_cold) * 1e-06 + p_fixed) * f_uplift`; `p_cryo = p_cold/cop + p_direct`) and "Research Findings" expected-headline table (the implement targets, oracle-exact).

**Baseline anchors**: `verify_stellaris.py` — `IN` dict :49, parasitic literals :69–70 (`p_cryo=0.8` at :70), recirc sum :150. `run_stellaris.py` — `P` :73, `CH` :76–90, WI-023 comment block :232–243, headline checks :244–258, success string :294–295.

**Checklist**:

- [x] `verify_stellaris.py`: add the chain inputs to `IN` (q_nuc_cryo 35.5, vol_cold_cryo 136.56, p_fixed_cryo 0.0075, f_uplift_cryo 1.0, T_cold_cryo 20.0, T_amb_cryo 300.0, f_carnot_cryo 0.20, p_cryo_direct 0.0) with WI-024 comments; replace the `p_cryo=0.8` literal with the chain mirror using the design §4 statement forms verbatim, feeding the recirc sum (:150) where the literal sat. *(Statement forms verified against the generated impl body :127-130 — identical parenthesization; oracle also exposes `p_cryo` in its return dict for the runner's new channel check.)*
- [x] `run_stellaris.py`: add the derived channel `cryo=f"{P}cryo_elec__p_elec"` to `CH` and a per-channel bit-exact check of derived p_cryo vs the oracle (SV-031's "computed output" witness). *(CH key named `p_cryo` to match the oracle dict key so the physics-spine check loop picks it up — same channel, trivial naming deviation noted in the record.)*
- [x] `run_stellaris.py` :232–243: rewrite the comment block for WI-024 (derived cryo chain, retired 0.8 default, p_tf modeled zero; WI-023 values as the "was" line).
- [x] `run_stellaris.py` :244–258 + :294–295: retarget the headline story WI-023 → WI-024 (targets p_net 915.1, rec_frac 0.151, q_eng 6.61, LCOE 201.5 all sit inside the existing tolerance bands — retargeted for the record, per design §4); success string updated.
- [x] Execute: `cd exploration/stellarator_e2e && /home/reid/1cfe/fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python run_stellaris.py` → **bit-exact vs the updated oracle at rel 1e-9 on every channel including the new derived-p_cryo channel**, per-account capital, rollup, LCOE; headline checks green. *(ALL CHECKS PASSED; zero rel-1e-9 failures; p_cryo channel OK.)*
- [x] Verify the executed values against the design's oracle-exact table: p_cryo **0.8643516**, p_net **915.081088**, q_eng **6.606662**, rec_frac **0.151362**, LCOE **201.472065**; V 425.0 / p_fus 2748.06 / p_th 3238.12 / p_et 1078.29 unchanged; **total $12,601,519,645.07 and magnet $6,323,469,946.33 unchanged to the cent** (capital reads no parasitic slot). *(Executed: p_cryo 0.8643515999999999; p_net 915.0810878595104; q_eng 6.606661728940606; rec_frac 0.1513623734691124; LCOE 201.4720654967192; V 425.000014 / p_fus 2748.056877 / p_th 3238.120923 / p_et 1078.294267; total 12,601,519,645.065952 / magnet 6,323,469,946.334225 — identical to the WI-023 record to the cent.)*
- [x] Confirm the Phase 3 headline-doc numbers match the executed values in both model copies (they are oracle-exact; on any mismatch fix both copies, re-run L1, and surface the discrepancy in the record). *(Match — 915.081 / 0.15136 / 6.6067 / 201.472; no fix needed.)*

**Test requirements**: the rel-1e-9 compare is the integration test; the headline asserts are the sanity band.

**Validation checkpoint**: run output — zero rel-1e-9 failures, all headline checks green, executed values recorded for Phase 7.

**Completion gate**: bit-exact pass at the design's expected values. Any deviation from the expected table is stop-and-surface, not a retarget (the same oracle produced both).

## Phase 6 — Handshake successor bar + regressions

**Overview**: land the D7 injection-map edit under the owner-accepted successor bar and prove Anchor A still reproduces byte-identically; then the unrelated-surface regressions.

**Design reference**: design **D7** (the exact injection replacement and the identity-path argument, with executed spike proof) and "Validation Plan" items 5–6. Owner authorization: spec §Checkpoint Rulings, Ruling 3 (successor bar accepted — this phase is not waiting on any further sign-off).

**Baseline anchors**: `handshake_1costingfe.py` — `set_1cfe_inputs` :153, `pb__p_tf` injection :216 (untouched), `pb__p_cryo` injection :219 (the edit), `magnet__B` :271 (untouched).

**Checklist**:

- [x] Edit **only within the `set_1cfe_inputs` injection map**: replace :219 `f"{P}pb__p_cryo": pb["p_cryo"],` with the D7 successor injection — `f"{P}cryo_elec__q_nuc": 0.0, f"{P}cryo_elec__vol_cold": 0.0, f"{P}cryo_elec__p_fixed": 0.0, f"{P}cryo_elec__p_direct": pb["p_cryo"],` — plus the edit comment (baked f_uplift/T/f_carnot values are inert at zero heat; identity path is exact in IEEE arithmetic). **No comparison-logic change anywhere in the script.**
- [x] `git diff exploration/stellarator_e2e/handshake_1costingfe.py` shows exactly the one injection-map hunk, nothing else. *(1 hunk at :216-226, injection map only.)*
- [x] Run: `cd exploration/stellarator_e2e && /home/reid/1cfe/fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python handshake_1costingfe.py`. *(Ran clean; net_electric 1,000.0001 both sides +0.00%; wrote handshake_comparison.json; generated inputs restored to pre-handshake state.)*
- [x] `git diff exploration/stellarator_e2e/handshake_comparison.json` → **empty** (SV-025 six power channels + SV-026 account gap byte-identical to the WI-023 record). *(Empty — 0 diff lines.)*
- [x] IFE regression SV-023: run `exploration/ife_e2e/run_anchors.py` (exec-venv interpreter) — anchors unchanged: **252.30 / 68.69 / 270.12 $/MWh; Meier 4.735 c/kWh** (no IFE file touched). *(ALL ANCHOR CHECKS PASSED rel 1e-6; 270.12117794; Meier 4.73540355; perturbation check 216.55528392 moved as expected.)*
- [x] Viability unchanged: no viability constraint reads p_cryo (design "Cross-File Bindings" grep); beta/TBR static bindings untouched, wall load unchanged from the Phase 5 channels. *(Zero p_cryo hits in mfe_viability.sysml; wall_load executed 3.131235, identical to WI-023.)*
- [x] Model-test tally unchanged vs baseline: env sourced, `uv run pytest tests/models/ -q` → **2 failed / 10 passed / 13 skipped / 18 errors** (pre-existing, unrelated — the bar is tally-unchanged, not green). *(SURFACED DEVIATION — the recorded tally no longer reproduces in the current environment, independent of WI-024: a pristine worktree at HEAD `1237f1c5` also yields **11 failed / 18 passed / 14 skipped / 0 errors** — the 18 syside lazy-import setup errors no longer occur, so those tests now run and fail on their stale-path expectations. Control evidence: WI-024 tree and pristine-HEAD failure SETS diffed — byte-identical (11 FAILED node IDs, all test_foundation/test_power_balance stale-path/interface expectations). The gate's operative bar — WI-024 introduces no test change — passes exactly; the environment drift is surfaced in the Implementation Record and the session report, not absorbed.)*

**Test requirements**: handshake byte-identity and SV-023 are the regression suite for this item.

**Validation checkpoint**: empty `handshake_comparison.json` diff; single-hunk script diff; anchors exact; pytest tally identical.

**Completion gate**: all gates pass with the handshake edit confined to the injection map. Any non-empty `handshake_comparison.json` diff is stop-and-surface — never reconcile by editing comparison logic.

## Phase 7 — Close-out records, final integration & validation

**Overview**: flip SV-031 with executed values, record q_eng against SV-016 without touching the band, land the headline records, and verify every spec Success Criterion. Item close and commit are **not** steps here (owner-held / orchestrator-held).

**Design reference**: design "Validation Plan" item 7; spec **MR-WI024-6** (record, never fit) and §Success Criteria 1–4.

**Checklist**:

- [x] SV-031 → passing: `uv run agentic-mbse pm update-validation SV-031 --status passing`; update the `modeling_project/VALIDATION_MATRIX.md:57` row with the Phase 5 executed values (derived p_cryo 0.8643516 MW as a computed chain output; p_net 915.081, rec_frac 0.151362, q_eng 6.6067, LCOE 201.472; capital unchanged; handshake byte-identical under the Ruling-3 successor bar; L1–L6 offender list = 6 pre-existing; WI-022 impl content-hash survival). *(CLI flip + EXECUTED block appended to the row; Source/Method cells filled per the SV-028/030 convention — WI-024 spec MR-WI024-1..6 / run_stellaris.py.)*
- [x] SV-016 (`VALIDATION_MATRIX.md:42`, pending): append a dated WI-024 note to the Description cell — q_eng 6.609 → 6.6067 at the derived parasitic power, still below the ~10–40 band; the derived value is a documented lower bound (D6) — flag for owner. **Do not adjust, resolve, or reword the band; status stays pending** (MR-WI024-6). *(Dated note appended to the Description cell only; band, status, and all other cells untouched.)*
- [x] Headline records: instance doc block confirmed at Phase 5 (both copies); update `.project/CURRENT_WORK.md` to the WI-024 executed headline (note the STALE-BASIS pass-through recompute as the sequenced next item at the settled p_net). *(New top entry in Active Work; marked NOT closed / NOTHING committed.)*
- [x] Append the Implementation Record to this plan (section below — executed values, validation results, deviations/judgment calls, quarantine transparency notes if any grep touched barred-path match lines).

**Final integration & validation** (spec Success Criteria, verified explicitly):

- [x] **SC-1 / SV-031**: derived p_cryo is a computed chain output (runner channel check), every link graded per the spec provenance table with the two assumption parameters explicit (f_carnot 0.20, T_amb 300; f_uplift 1.0 seam); executed headline recorded; bit-exact rel 1e-9 (Phase 5). *(p_cryo channel `cryo_elec__p_elec` OK at rel 1e-9; executed 0.8643515999999999.)*
- [x] **SC-2**: L1–L6 offender list = the 6 pre-existing, zero new (Phase 3); regen with WI-022 handwritten-impl content survival (Phase 4); pipeline bit-exact rel 1e-9 (Phase 5); IFE anchors and pytest tally unchanged (Phase 6). *(Pytest: failure SET unchanged vs pristine HEAD; the recorded tally itself no longer reproduces in the current environment — surfaced deviation, Phase 6 note + Implementation Record.)*
- [x] **SC-3**: SV-025/026 byte-identical under the Ruling-3 successor bar — empty `handshake_comparison.json` diff, edit confined to the injection map (Phase 6).
- [x] **SC-4**: every affected slot doc states its post-WI-024 coverage — p_tf modeled zero, p_cryo derived (0.8 retired), p_tfcool disjoint-read residual (Phase 3, MR-WI024-3); no silent defaults anywhere in the chain (MR-WI024-2); q_eng recorded against SV-016 and flagged (this phase).
- [x] All changed values carry MR-4 Source/Ref/Basis citations resolving to Stellaris images/raw.pdf, 1costingFE @ `0254385`, or a dated design/checkpoint ruling for assumption parameters; no ARIES-CS-informed source read or cited (MR-WI024-5 — inspect the Phase 1–3 doc stencils). *(All doc stencils taken from the approved design verbatim; assumption parameters cite the dated design rulings D4/D6, never a fake source. No barred path read; see the quarantine note in the record.)*

**Completion gate**: every Success Criterion checked; SV-031 passing; SV-016 flagged with band untouched; records written. Then stop — hand back to the orchestrator (audit → owner close → commit).

---

## Feasibility Concerns

| concern | disposition |
|---|---|
| Handshake successor bar acceptance | **Resolved before this plan**: spec Checkpoint Ruling 3 ([OWNER] 2026-07-18) accepted the D7 bar — Phase 6 executes it, no pause |
| Regen run with `--design-path-filter` → 8 spurious offenders | The design's documented gotcha. Phase 4 command is unfiltered by instruction; hard control gate: bridge reports exactly 3 offenders or the phase stops and runs the unedited-tree control procedure |
| sysml-codegen HEAD moves before implement | Verified still `6db3212` at plan time; Phase 4 re-checks and runs the control procedure first if it moved |
| Oracle/impl statement-form drift breaks bit-exactness | Oracle mirrors the generated statement forms verbatim (design §4, spike-proven bit-equal); runner gates every channel at rel 1e-9 including the new cryo channel |
| Regen clobbers the WI-022 handwritten impl | `preserve_handwritten=True` re-verified at plan time (bridge_v11_generate.py:108); content hash recorded (`8d2357…794a9f`) and checked post-regen; stop-and-restore on mismatch (WI-023 pattern) |
| Executed numbers differ from the design-stage oracle run | Very low — the design's expected table is oracle-exact and the same oracle is the implement gate; any deviation is stop-and-surface, never a silent retarget (Phase 5 gate) |
| `mfe_plant.sysml` staged twin is not byte-identical | Known WI-015 DEMO NOTE divergences (3 regions, verified at plan time); the Phase 2 mirroring gate is "only known divergences remain, edit regions byte-identical" — all WI-024 edit regions sit outside the divergent regions |
| Line-number drift | Anchors verified at `1237f1c5`; two design anchors already drifted (STALE BASIS :510/:557 → :518/:562) — edits match on content, numbers orient only; per-phase diffs catch mirroring slips |
| `pytest tests/models/` red at baseline | Pre-existing and unrelated (stale path expectations + syside lazy-import setup errors). The bar is tally-unchanged (2 failed / 10 passed / 13 skipped / 18 errors), same as WI-022/023 |
| Circumference approximation biases vol_cold | Certain but bounded (design risk row): 25 m is printed-but-approximate, documented as the weak link in the D5 binding doc with the mass cross-check; error flows linearly into a ~0.86 MW term — no plan action beyond the doc stencil |
| Derived value understates the true cryo load | Certain by construction (the paper defers the full inventory): D6 lower-bound treatment — f_uplift = 1.0 seam with the verbatim deferral quote; the item's claim is "derived from what the source prints, with stated assumptions" |
| q_eng still below SV-016's band | Certain: 6.6067 vs ~10–40. Recorded and flagged at Phase 7, never fitted (MR-WI024-6) |
| Traceability matrix | One calc-def row added (Phase 1, WI-019 library convention); instance literals record citations in model doc comments per the WI-020→023 lineage — no per-literal matrix rows |

---

## Implementation Record

**Implemented 2026-07-18.** All seven phases executed in order; every gate passed on first run except the Phase-6 pytest tally, whose recorded baseline no longer reproduces in the current environment (surfaced below with control evidence — not a WI-024 effect). Item NOT closed and NOTHING committed (owner-held / orchestrator-held, per the plan header).

**Model change (as designed, D1–D6):**
- NEW `models/library/analyses/mfe_cryo_plant.sysml` + byte-identical staged twin: package `mfe_cryo_plant`, `calc def 'Cryoplant Electrical Power'` from the design §1 stencil verbatim (8 dormant-default inputs, p_cold/cop_carnot/cop intermediates, out p_elec, full MR-4 doc). Traceability-matrix row added (`data/traceability_matrix.csv`, WI-019 library-calc-def convention).
- Generic plant (`models/designs/generic_mfe/mfe_plant.sysml` + staged twin, region-identical): `import mfe_cryo_plant::*`; `p_cryo` re-doc'd to the additive direct term with `default 0.0`; 7 chain attributes with dormant defaults; `calc cryo_elec` usage with the 8 bindings (`in p_direct = p_cryo` last); the one pb rewire `in p_cryo = cryo_elec.p_elec`. Power-balance calc def and recirc-sum formula untouched.
- Stellaris instance (`models/designs/stellarator_09/stellarator_plant.sysml` + staged twin, region-identical): p_tf doc rescoped from deferral stopgap to modeled zero (SC coil set; 1cfe `recirc_power_factor = 0.0`; joints counted as 20 K heat; WI-023 history compressed to one parenthetical); `:>> p_cryo = 0.0` retirement doc (D2) + the 7 chain bindings with the design's cited docs verbatim (q_nuc 35.5 SOURCED, vol_cold 136.56 COMPUTED w/ D5 arithmetic + both cross-checks, p_fixed 0.0075 SOURCED, f_uplift 1.0 D6 lower-bound seam, T_cold 20 SOURCED, T_amb 300 assumption, f_carnot 0.20 THE assumption); p_tfcool doc gains the D2 disjoint-read coverage statement; headline re-baselined + WI-024 history line; both pass-through STALE BASIS blocks appended (915.145 → 915.081, negligible at stated precision); mapping-traps note inspected, unchanged (no trap touches p_tf). Buildings STALE BASIS untouched.

**Regen (never hand-edited):** unfiltered snapshot (NO `--design-path-filter`, per the design gotcha) over the staged models at sysml-codegen `6db3212` → `bridge_v11_generate.py`. **Exactly 3 V11 offenders** (contingency__direct_subtotal, indirect__direct_cost, lcoe_calc__total_capital), bridged, 0 after bridge, package emitted. `system_design.json`: +8 `cryo_elec__*` leaves (35.5 / 136.56 / 0.0075 / 1.0 / 20.0 / 300.0 / 0.2 / 0.0), `pb__p_cryo` gone; yaml wires `p_cryo` ← `cryo_elec__p_elec` (yaml:207). `cryoplant_electrical_power_impl.py` AUTO_IMPLEMENTED = True (pure arithmetic); `IMPLEMENTATION_BACKLOG.md` still exactly 1 function (DT_Fusion_Power). WI-022 handwritten impl **content-hash unchanged** through regen (sha256 `8d235747…794a9f` before and after; AUTO_IMPLEMENTED = False intact). `mfe_plant_params.json` transited the known regen-reset state and returned to the committed post-run state after the Phase-5 execute + handshake cleanup (WI-023 record's expected behavior).

**Executed headline (bit-exact vs oracle, rel 1e-9, zero failures, incl. the new derived-p_cryo channel):** p_cryo **0.8643515999999999 MW** (chain-derived; spike-identical), p_net **915.0810878595104 MW**, rec_frac **0.1513623734691124**, q_eng **6.606661728940606**, LCOE **$201.4720654967192/MWh**; V 425.000014 / p_fus 2748.056877 / p_th 3238.120923 / p_et 1078.294267 / wall_load 3.131235 unchanged; total **$12,601,519,645.065952** and magnet **$6,323,469,946.334225** (50.2%) identical to the WI-023 record to the cent. All values match the design's oracle-exact expected table exactly.

**Validation:**
- L1 = 0 over 22 files after every model phase; L3 0 cycles; full ladder offender list = **exactly the 6 pre-existing** — `hif_plant.sysml:205`, `ife_plant.sysml:33/41`, and the three `mfe_plant.sysml` derived-expression offenders, printed at **:353/:359/:364** (the baseline :329/:335/:340 shifted by the 24 lines the WI-024 attribute/calc block inserts above them; content identical), zero new, no diagnostic names a WI-024 element. Summary flags L2 ❌/L6 ❌ from the known pre-existing attribution (WI-023 precedent). Transient Phase-1 WARN ("Unused calc def") cleared when the Phase-2 usage landed.
- Mirroring: generic-plant twin diff = only the 3 known WI-015 DEMO NOTE divergences; instance twin diff = only the viability-assert block; library file byte-identical in both trees.
- Handshake (Ruling-3 successor bar): `handshake_1costingfe.py` edited **only** within the `set_1cfe_inputs` injection map — single hunk replacing the `pb__p_cryo` injection with the D7 identity path (`cryo_elec__q_nuc/vol_cold/p_fixed = 0.0`, `cryo_elec__p_direct = pb["p_cryo"]`); no comparison-logic change. Run clean; `git diff handshake_comparison.json` **empty** (SV-025/026 byte-identical).
- IFE SV-023: ALL ANCHOR CHECKS PASSED rel 1e-6 (252.30 / 68.69 / 270.12117794 $/MWh; Meier 4.73540355 c/kWh; gain-100 perturbation 216.55528392 moved as expected).
- Viability: zero `p_cryo` hits in `mfe_viability.sysml`; beta/TBR static bindings untouched; wall_load 3.131235 executed, unchanged.
- SV-031 → **passing** with the EXECUTED block (matrix row updated; Source/Method cells filled per convention). **SV-016 flagged, band untouched** (dated note in the Description cell only): q_eng 6.609 → 6.6067, still below ~10–40; derived value is a documented lower bound (D6). `.project/CURRENT_WORK.md` headline updated (STALE-BASIS recompute noted as the sequenced next item at the settled p_net).

**Deviations / judgment calls (all surfaced, none absorbed):**
1. **Pytest tally (Phase 6 gate) — environment drift, not a WI-024 effect.** The recorded baseline (2 failed / 10 passed / 13 skipped / 18 errors) no longer reproduces: the current environment yields **11 failed / 18 passed / 14 skipped / 0 errors** on BOTH the WI-024 tree and a pristine worktree at HEAD `1237f1c5` (control run, worktree removed after). The 18 syside lazy-import setup errors no longer occur, so those tests now execute and fail on their pre-existing stale-path/interface expectations (test_foundation + test_power_balance — the WI-019-surfaced broken-test debt). Control evidence: the FAILED node-ID sets of the two runs were diffed — **byte-identical** (11 IDs). The gate's operative bar — WI-024 introduces no test change — passes exactly; the stale recorded tally is surfaced here and in the session report rather than silently re-baselined.
2. Runner CH key named `p_cryo` (not the plan's literal `cryo=`) so the physics-spine check loop picks the channel up alongside the oracle's `p_cryo` dict key — same channel (`{P}cryo_elec__p_elec`), same bit-exact check; naming-only deviation.
3. The oracle's return dict gained `p_cryo=p_cryo` (not an explicitly planned edit) — required for the runner's per-channel check of the derived value; mirrors how every other checked channel is exposed.
4. L1–L6 offender line numbers for `mfe_plant.sysml` print at :353/:359/:364 vs the recorded :329/:335/:340 — pure line shift from the inserted WI-024 block, content-identical offenders (the plan's own match-on-content rule applied).
5. Traceability-matrix Confidence/Assumptions cells left empty for the new calc-def row, matching the existing `'MFE Power Balance Calc'` codebase-sourced row exactly.

**Quarantine transparency:** no grep in this session matched lines under `knowledge/holdout/**` or any PROTOCOL §3 barred path; no barred artifact was read or cited. All sources touched: the design/spec/plan artifacts, 1costingFE-cited doc stencils (copied verbatim from the approved design), and repo model/pipeline files.

**Handed back to the orchestrator**: `/audit-models` → owner `pm close-item WI-024` → commit.
