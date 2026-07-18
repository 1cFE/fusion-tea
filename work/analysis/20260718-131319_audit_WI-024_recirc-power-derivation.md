# Audit Report — WI-024 recirc-power-derivation (work item audit)

**Date**: 2026-07-18 | **Auditor**: independent audit session (did not implement the work)
**Scope**: work item WI-024 (`work/active/WI-024_recirc-power-derivation/`), uncommitted working-tree changes on `feat/stellarator-mbse-demo` at HEAD `1237f1c5`
**Verdict**: **POSITIVE** — all six MR-WI024 requirements satisfied, all four spec Success Criteria met, all three Checkpoint Rulings honored, all plan completion gates re-verified. No blocking or material findings. Four note-level observations below.

## Executive Summary

WI-024 replaces the WI-023 `p_tf = 0.0` deferral stopgap with a modeled cryoplant-electrical derivation chain: a new concept-agnostic library calc def (`models/library/analyses/mfe_cryo_plant.sysml`) computes the cryoplant wall-plug power from winding-pack nuclear heating × computed winding volume + joint losses, through a fraction-of-Carnot COP, landing in the `p_cryo` slot (design D1); the 1costingFE 0.8 MW generic default is retired (D2) and `p_tf` is rescoped to a modeled zero. The auditor independently re-read the source page images and the published PDF, recomputed the winding-volume and chain arithmetic from scratch, re-executed the pipeline, handshake, full validation ladder, IFE regression, and the pytest control (including an independent pristine-worktree comparison), and re-verified every 1costingFE citation at the pin. Every executed number matches the design's oracle-exact expected table and the plan's Implementation Record bit for bit. The clean-room quarantine held.

## Executed Evidence (re-run by the auditor, not taken from the implementation record)

| check | result |
|---|---|
| `run_stellaris.py` (exec venv) | ALL CHECKS PASSED, rel 1e-9 vs oracle on every channel including the new derived-p_cryo channel, zero failures |
| derived p_cryo | 0.8643515999999999 MW (chain output `cryo_elec__p_elec`, bit-exact vs oracle) |
| p_net / q_eng / rec_frac | 915.0810878595104 MW / 6.606661728940606 / 0.1513623734691124 — match the design's expected table exactly |
| LCOE | $201.4720654967192/MWh — matches |
| total / magnet capital | $12,601,519,645.065952 / $6,323,469,946.334225 (50.2%) — identical to the WI-023 record to the cent (capital reads no parasitic slot) |
| unchanged channels | V 425.000014, p_fus 2748.056877, p_th 3238.120923, p_et 1078.294267, wall_load 3.131235 |
| `handshake_1costingfe.py` re-run | ran clean (net_electric 1,000.0001 both sides); `git diff handshake_comparison.json` = 0 lines (SV-025/026 byte-identical); working tree byte-identical before and after all audit re-runs (status + diff sha256 compared) |
| handshake script diff | exactly ONE hunk (`@@ -216,7 +216,15 @@`), entirely inside `set_1cfe_inputs`'s injection map — `pb__p_cryo` leaf replaced by the D7 identity path (`cryo_elec__q_nuc/vol_cold/p_fixed = 0.0`, `cryo_elec__p_direct = pb["p_cryo"]`); `pb__p_tf` :216 and `magnet__B` untouched; zero comparison-logic change — the Ruling-3 successor bar holds exactly |
| `agentic-mbse validate models --complete` | L1 = 0 errors, 0 warnings over **22 files**; total ERROR list exactly 6: `mfe_plant.sysml:353/359/364` (the three derived-expression rollup offenders — auditor compared HEAD :329-343 vs worktree :353-366, expression text content-identical, pure +24-line shift from the WI-024 attribute/calc insertion), `ife_plant.sysml:33/41`, `hif_plant.sysml:205`; zero new, no diagnostic names a WI-024 element; L3/L4/L5 pass; L2 ❌/L6 ❌ summary flags are the known pre-existing attribution (WI-023 precedent) |
| IFE regression `run_anchors.py` (re-run) | 252.29996307 / 68.69020165 / 270.12117794 $/MWh; Meier 4.73540355 c/kWh; gain-100 perturbation 216.55528392 — SV-023 anchors unchanged |
| pytest `tests/models/` (WI-024 tree) | 11 failed / 18 passed / 14 skipped / 0 errors |
| pytest pristine-worktree control (auditor's own worktree at `1237f1c5`, same interpreter) | 11 failed / 18 passed / 14 skipped / 0 errors; FAILED node-ID sets diffed — **byte-identical** (11 IDs, all test_foundation/test_power_balance stale-path expectations). The implementer's control claim is independently CONFIRMED: the tally drift vs the recorded 2f/10p/13s/18e baseline is environmental (the 18 syside lazy-import setup errors no longer occur), not a WI-024 effect. WI-024's test surface is clean |
| WI-022 handwritten reactivity impl | sha256 `8d23574793c34314c67b68b8e0f4ec438d3e2d9f92060eb4094a8d46c0794a9f` — matches the plan's pre-regen record; `AUTO_IMPLEMENTED = False` intact; `preserve_handwritten=True` at `bridge_v11_generate.py:108` |
| regen artifacts | `system_design.json`: all 8 `cryo_elec__*` leaves at the instance values (35.5 / 136.56 / 0.0075 / 1.0 / 20.0 / 300.0 / 0.2 / 0.0), zero `pb__p_cryo` hits; yaml wires `p_cryo: float …cryo_elec__p_elec.root` (:207); `cryoplant_electrical_power_impl.py` `AUTO_IMPLEMENTED = True`; `IMPLEMENTATION_BACKLOG.md` exactly 1 unchecked function (DT_Fusion_Power); snapshot/`__init__.py`/schemas/tests diffs all regen-shaped (module registry gains `Cryoplant_Electrical_PowerModule`; "20 → 21 calculation definitions"); `mfe_plant_params.json` not modified (returned to committed state as recorded) |

## Source Fidelity (re-derived)

All values re-read from page images or the published PDF by the auditor — never the text extractions (per spec §Extraction errata).

- **Table 6 image** (`iter-01/sources/stellaris-design-details/images/page_020_table_0.png`, read directly): "Mean cryogenic nuclear heating (winding pack) [W/m³] **35.5**". ✓
- **Table 8 image** (`page_022_table_0.png`, read directly): turns 324/324/289/289/256/225; cross-section side lengths **360/360/340/340/320/300 mm**; no-casing masses 24.2/25.4/21.6/21.5/19.0/17.0 t; total energy 110.58 GJ (2.76 GJ per coil). ✓
- **Table 7 image** (`page_021_table_0.png`, read directly): tape stack 9 / copper jacket 35 / solder 12 / steel 36 / helium 8 %. ✓
- **Published PDF** (`iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf`, pdftotext by the auditor), all cited quotes present verbatim: "a typical circumference of 25 m" (§2.9); "we select a square winding pack"; "Each turn is sized at 20 mm × 20 mm"; "the operating temperature (Top) is set to 20 K"; "cooled to 20 K using supercritical helium channels at 15–20 bar"; "48 coils divided into four periods, with each period containing 12 coils: six independent and six mirrored" (→ ×8 per unique coil); "10 W per joint … approximately 7.5 kW steady-state losses for the entire stellarator coil set … negligible"; the lower-bound deferral "…should be smaller than the total nuclear heating of the coils, the coil cases, and the remaining 20 K cooled parts of the support structure, which will be examined in future studies"; §2.8 "average value of 35.5 W/m³", EU DEMO ~50 W/m³ peak reference, and the qualitative-only cryo-efficiency remark (no COP number anywhere — confirming the A4 no-admissible-value finding). ✓
- **Winding-volume arithmetic recomputed from scratch**: turns × (0.02 m)² reproduces every Table 8 side² exactly (324×4 cm² = 0.36², 289×4 = 0.34², 256×4 = 0.32², 225×4 = 0.30²); Σ side² = 2(0.36²)+2(0.34²)+0.32²+0.30² = 0.6828 m²; × 8 × 25 m = **136.56 m³** exactly. Mass cross-check: 128.7 t × 8 = 1029.6 t → 7539.5 kg/m³, plausible for the Table 7 mix. ✓
- **Chain arithmetic recomputed** (both in plain form and in the generated impl's exact statement forms): p_cold = (35.5 × 136.56 × 1e-6 + 0.0075) × 1.0 = 0.01234788 MW; COP = 0.20 × 20/280 = 1/70; p_elec = **0.8643515999999999** MW — IEEE-bit-identical to the executed channel and the recorded value. The oracle mirror in `verify_stellaris.py` uses the generated impl's parenthesization verbatim (compared side by side). ✓
- **1costingFE @ `0254385`** (repo verified at the pin, clean): `defaults.py:610-612` `rebco_hts` `recirc_power_factor=0.0, cryo_temp_k=20.0` (SC grades all 0.0; copper 2.0e-4) — the :611-614 cites resolve; `steady_state_stellarator.yaml:17-24` prints f_sub 0.03, p_coils 3.0, **p_cool 15.0 and p_cryo 0.8 side by side** (D2's disjoint-read basis confirmed in the source); `steady_state_dipole.yaml:52-53` "Cryogenic wall-plug power [MW] (neon slush at 24.6 K, eta_cryo ~1.25%; Reactor A Table 9)" — cited as slot-semantics witness only, value not used anywhere; `types.py:229-231` p_coils/p_cool/p_cryo slot docs as cited; `physics.py:321-323` recirculating sum includes p_cryo as cited. ✓

## Assumption Honesty (MR-WI024-2)

- `f_carnot_cryo = 0.20` — doc states explicitly that no admissible source prints a 20 K COP, cites the design ruling D4 (2026-07-18, sanctioned by spec Checkpoint Ruling 2), states the engineering basis in words (15–30%-of-Carnot band, 0.20 at the conservative end → 70 W_e/W), and names W7-X and the dipole eta_cryo comment as value-inadmissible/shape-only. PASS.
- `T_amb_cryo = 300.0` — cited to the D4 ruling as a standard-ambient assumption, no fake source. PASS.
- `f_uplift_cryo = 1.0` — explicit lower-bound seam, doc quotes the paper's future-studies deferral, states "Cited to the design ruling, not a source". PASS.
- No silent defaults: all 8 chain inputs are explicitly bound at the instance with citations; the library calc def's dormant defaults are inert on the dormant path (zero heat → p_elec = p_direct exactly) and documented as such. No W7-X or dipole value appears as a value anywhere in the chain (grep + doc inspection). PASS.

## MR Verification

| requirement | status | evidence |
|---|---|---|
| MR-WI024-1 (derived, not bound; chain modeled; placement per ratified scope) | PASS | new calc def + `cryo_elec` usage + pb rewire `in p_cryo = cryo_elec.p_elec` (`mfe_plant.sysml`); p_cryo executes as a chain output (runner channel bit-exact); recirc-sum formula untouched |
| MR-WI024-2 (every link sourced/computed/explicit assumption; no silent defaults; no inadmissible values) | PASS | per-link verification above; provenance grades in the binding docs match the spec table (q_nuc/p_fixed/T_cold SOURCED, vol_cold COMPUTED, f_carnot/T_amb/f_uplift explicit assumptions) |
| MR-WI024-3 (double-counting ruling implemented and documented) | PASS | p_cryo retirement doc (D2) at the instance; p_tfcool doc gains the disjoint-read coverage statement with the conservative-direction residual; p_tf doc rescoped to modeled zero naming where the joint loss went |
| MR-WI024-4 (standing bars; handshake per the Ruling-3 successor bar) | PASS | auditor re-ran validation (offender list exactly the 6 pre-existing, content-verified across the line shift), regen integrity checks, pipeline (bit-exact), handshake (single injection-map hunk, empty comparison diff), IFE anchors, pytest control (independently confirmed) |
| MR-WI024-5 (MR-4 citations resolve; clean-room) | PASS | every cited image/PDF/1cfe target verified on disk and content-checked at the pin; assumption parameters cite dated rulings; no barred source read or cited (see Quarantine) |
| MR-WI024-6 (SV-016 recorded against, never fitted) | PASS | SV-016 diff is a dated note appended to the Description cell only; band "~10-40", status `pending`, and all other cells untouched; q_eng 6.6067 recorded and flagged |

## Spec Success Criteria

1. **SV-031** — PASS. p_cryo is a computed chain output (executed by the auditor, bit-exact at rel 1e-9 on the `cryo_elec__p_elec` channel); every link graded; executed headline recorded in the matrix row and matches the auditor's run exactly; matrix row `passing` with the EXECUTED block.
2. **Standing bars** — PASS. L1 = 0 / 22 files; offender list = the 6 pre-existing, zero new; regen with WI-022 impl content survival (hash-verified); pipeline bit-exact; IFE anchors exact; pytest failure-set unchanged vs pristine HEAD (independently controlled; see finding 1 on the stale recorded tally).
3. **Handshake** — PASS under the owner-accepted Ruling-3 successor bar: script edit confined to the `set_1cfe_inputs` injection map (one hunk), comparison logic untouched, `handshake_comparison.json` git diff empty after the auditor's re-run.
4. **Docs** — PASS. All three affected slot docs state post-WI-024 coverage; no silent defaults; q_eng recorded against SV-016 and flagged for the owner.

## Checkpoint-Ruling Fidelity

- **Ruling 1 (Option (a) only)**: p_pump/p_trit/p_house/f_sub bindings untouched (diff-verified); only p_tf/p_tfcool/p_cryo docs and the chain touched. PASS.
- **Ruling 2 (design resolves placement/COP/volume/uplift with documented basis)**: D1–D6 each carry documented bases in the design and in the binding docs. PASS.
- **Ruling 3 (handshake successor bar)**: executed exactly as ratified; the plan correctly records that Phase 6 needed no further sign-off. PASS.

## Records

- **SV-031** `passing` with executed values identical to the auditor's re-run. **SV-016** `pending`, band and wording untouched, dated WI-024 note in the Description cell only (the sanctioned flag). No status mutations made by this audit (item close is owner-held).
- **Traceability matrix**: one new calc-def row (`'Cryoplant Electrical Power'`, codebase-sourced, 1costingFE @ 0254385) matching the `'MFE Power Balance Calc'` row convention; instance literals cite in model doc comments per the recorded WI-020→023 convention.
- **`.project/CURRENT_WORK.md`**: new WI-024 top entry; every number matches the executed values; correctly marked NOT closed / NOTHING committed; STALE-BASIS recompute named as the sequenced next item.
- **Plan Implementation Record**: complete and accurate — every claim the auditor re-derived (hashes, offender lines, executed values, deviation list) checks out; the five recorded deviations are all real, surfaced, and benign.
- **Mirroring**: library file byte-identical in both trees; `mfe_plant.sysml` twins differ only by the 3 known WI-015 DEMO NOTE divergences; `stellarator_plant.sysml` twins differ only by the viability-assert block (single hunk 717,729c717,722).

## Findings

No blocking findings. No material findings.

**Notes (no action required for WI-024):**

1. **[note] The recorded pytest baseline "2 failed / 10 passed / 13 skipped / 18 errors" is stale in the current environment** (now 11f/18p/14s/0e on both trees; syside lazy-import setup errors no longer occur, so 9 more stale-expectation tests execute and fail). The implementer surfaced this with a pristine-worktree control; the auditor reproduced that control independently (own worktree at `1237f1c5`, byte-identical FAILED-ID sets) — WI-024's test surface is clean. Future items should re-baseline the recorded tally (and ideally fix the WI-019-surfaced broken-test debt); until then the operative bar is failure-set-unchanged, not the stale tally.
2. **[note] Generated impl docstring mangles the MR-4 markers** (`**Source**` → `*Source**` in `cryoplant_electrical_power_impl.py`) — a codegen doc-transcription cosmetic in a generated artifact; the model doc comment is intact. Pre-existing generator behavior, not a WI-024 defect.
3. **[note] Two implementer deviations from plan literals** — runner CH key named `p_cryo` instead of `cryo`, and the oracle return dict gaining `p_cryo` — are both recorded in the Implementation Record and are what make the SV-031 channel check work. Correctly surfaced, no issue.
4. **[note] Table 8 prints per-coil peak field 24.6 T vs Table 2/§2.9's 24.9 T** — both printed in the paper, already recorded in the spec errata as not load-bearing; repeated here so no future session flags it as new.

## Quarantine

No PROTOCOL §3 barred path was opened in this audit (sources read: the three iter-01 table images, the iter-02 raw.pdf, 1costingFE at the pin — all admissible). A grep of the full working-tree diff and the new WI-024 artifacts for barred-path references found none; the only "aries"/"holdout" matches are the PROTOCOL Required-Reading lines, the implementer's quarantine-transparency note, and a substring coincidence ("Scope Bound**aries**"). The implementation record's own quarantine disclosure is consistent with what the auditor observed.

## Audit Metadata

- Models audited: `models/library/analyses/mfe_cryo_plant.sysml` (+staged twin), `models/designs/generic_mfe/mfe_plant.sysml` (+twin), `models/designs/stellarator_09/stellarator_plant.sysml` (+twin); oracle/runner/handshake/generated artifacts under `exploration/stellarator_e2e/`
- Baseline sources: Stellaris Table 6/7/8 images (iter-01), publikationen raw.pdf (iter-02), 1costingFE @ `0254385`
- Thresholds: rel 1e-9 (pipeline vs oracle), byte-identity (handshake JSON; twin library file), exact offender-list match (L1–L6), IEEE bit-identity (chain arithmetic recompute)
- Everything in "Executed Evidence" was re-run by the auditor; nothing in this report relies solely on the implementing agent's self-report. Working tree verified byte-identical (status + diff sha256) before and after all audit re-runs; the auditor's control worktree was removed after use.
