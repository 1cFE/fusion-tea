---
Status: draft
Created: 2026-09-07
Updated: 2026-09-07
Related Artifacts:
  Spec: ./spec.md
---

# WI-044 Design — the magnet chain sees the coil bore

Three sourced shapes, each anchored at the design point, make the conductor peak field, the stored magnetic energy and the casing mass respond to the coil bore; the aspect ratio is reported. Written under goal `minor-radius` round 1, task T-001; the form is `[AGENT] (ratified by owner, 2026-09-07)` (`goal.md` § Reserved gates 1–2). Prototyped in the tracked model files (this session, 2026-09-07) and validated at Levels 1–6 with the pre-change residue; the arithmetic prototyped in `prototype/proto.py`.

## Overview

Today the peak field is the axis field times a held ratio, the casing mass is a held 63 t, and nothing in the magnet chain reads the coil bore (spec § Current state). After this item:

- `'Conductor Peak Field'` multiplies the held ratio by the eq.-39 bore factor `R / (R − a_coil)` normalised at the reference geometry, so the printed pair is reproduced exactly at the design point and the peak rises as the bore grows;
- a new `'Coil Set Stored Energy'` scales the printed 111 GJ by `(I / I_ref)² (a_coil / a_coil_ref)² (R_ref / R)` (thesis eq. 2.82 with `W = ½ L I²`);
- a new `'Magnet Casing Mass'` scales the 63 t floor by `(W_mag / W_mag_ref)^0.78` (eq. 56) and feeds `'Magnet Structure Cost'` through the existing `magnet.m_casing` attribute, now bound by reference;
- `'Plasma Geometry'` reports `A = R / a`; `'MFE Radial Build'` exposes the coil-centre radius the shapes take.

Five anchor attributes appear on `'Magnet System'` (`m_casing_ref`, `W_mag_ref`, `I_ref`, `R_ref`, `a_coil_ref`); the held `m_casing` binding retires. At the baseline every channel is bit-identical (§ Expected baseline behaviour). Off the design point the conductor ceiling catches every `a` above 1.3 on the design column and the casing account rises about 1.5× at `a` 2.2; at the cheapest committed machine the larger R absorbs the bore (§ Off-design predictions).

## Research findings

- **The equations, read from the images this session** (`spec.md` § Why this item exists lists the paths): eq. 39 `B_max(A_wp) = μ0 I N / (R − a_coil) × (a0(C) + R a1(C) / √A_wp)`; eq. 2.82 `L = L(C) (a_coil² / â_coil²)(R̂ / R)`; eq. 2.81 `U = 2 E_stoTF / (τ_Q I) = L I / (τ_Q N_TF)`, i.e. `E_stoTF = L I² / (2 N_TF)` per coil; eq. 56 `M_struct = 1.348 W_mag^0.78` with no units printed (`output.md` L605–609 around it name no unit). The Table 2 render carries a 1.3, R 12.7, A 9.8, 9.0 T, 24.9 T, 15.4 MA, 48 coils, 111 GJ.
- **The executed baseline peak field is already one ulp under 24.9.** The computed axis field is `8.999999999999998` (WI-035 D2, low side bound), and `8.999999999999998 × 2.7666666666666666 = 24.899999999999995` in float64 (`prototype/proto.py`). The instance comment's "9.0 × peak_ratio == 24.9 exactly" is true of the literal 9.0, not of the executed product; `peak_field_ok` reads satisfied at the baseline because the product is one ulp *low*. This matters for the anchor form: the new form must reproduce `24.899999999999995`, not 24.9 — which it does when the normalised bore factor is exactly 1.0 (D3).
- **The radial build's coil-centre radius at a 1.3 is `3.1500000000000004`** in the generated summation order (`vacuum_or = a + vacuum_t`, then eight cumulative additions, then `+ coil_t / 2.0`); `vessel_or` is `3.0000000000000004`. The anchor `a_coil_ref` is bound as that float so the ratio `a_coil / a_coil_ref` is exactly 1.0 at the design point (the `k_link` / `j_wp` convention of binding the float that reproduces the executed pair).
- **Table 8 sums the per-coil energies to 110.58 GJ** against Table 2's rounded 111 (`evidence/grounding_sources/report.md` § Q3, the render `stellaris_p23_table8.png`). Table 2 is the anchor; the 0.4 % is disclosed at the binding.
- **The paper's own build to the coil centre is 1.50 m** from the LCFS (Fig. 34 render), so the paper's `a_coil` is about 2.80 m; this model's 1costingFE layer stack gives 3.15 m at the coil centre. The offset is absorbed by the anchor: only ratios to the reference enter any shape.
- **The codegen envelope.** `'Winding Pack Sizing'` already emits `** 0.5`; the radial build emits `** 2` and chains of intermediate attributes as Python locals in source order (`generated/modules/mfe_plasma_scaling/mfe_radial_build.py:155–182`). The three new forms use a ratio, `** 2` and `** 0.78`; no manual stage is touched.
- **The oracle is rewritten by model items** (`git log -- exploration/stellarator_e2e/verify_stellaris.py`: WI-039, WI-041, WI-042 each rewrote it from the design). Its `IN` dict lists `magnet_m_casing` and `magnet_peak_ratio`; its `compute()` builds the radial build, `B_peak = B_axis * p["magnet_peak_ratio"]` (`:410`) and `magnet_structure` from `magnet_m_casing` (`:477`). `oracle_entry.py` maps entry keys (`:72`, `:76`) and channels (`:142`, `:147`).
- **Two spine facts read by tests:** `tests/models/test_beta_peak_field.py` checks that `'Conductor Peak Field'` carries `B_axis_in` and `peak_ratio_in` (still true; it passed on the prototype, 5 / 5) and that everything after `'Volume-Averaged Beta'` in `mfe_plasma_scaling.sysml` carries no numeric literal on an executable line except `1.25663706212e-6` and `2.0` — the rewritten peak-field calc carries none (the `2.0` in `r_coil_centre` sits in the radial build, before the beta calc).

## Design decisions

### D1 — The coil bore each shape takes is the coil-centre radius, `rb.r_coil_centre = vessel_or + coil_t / 2`. `[AGENT]`
Eq. 39 defines `a_coil` as "the average minor coil radius" (Lion 2021 L455) and eq. 2.82 uses the same symbol for the filamentary coil set; Stellaris states its coil facts at the centre filament (Table 3 render: "Coil information provided in this table refers to the center filament"). The radial build already carries `coil_t`, so the coil-centre radius is one new out attribute. The existing `r_coil = vessel_or` stays what it is — the 1costingFE conductor-quantity bore read by `'Magnet Coil Cost'` — and is not re-pointed; the two bores are two quantities and the model text says so. Rejected alternative: reuse `r_coil` (no radial-build change; 0.15 m under the literal quantity). The difference off the design point is ~0.05 % in the bore factor per 0.1 m of `a` and ~1 % in `W_mag` at `a` 2.2 (spec's paired table); consistency and the literal reading decide it.

### D2 — Eq. 39's winding-pack term is not carried. `[AGENT]`
`a1(C)` is unprinted and the corpus offers no second anchor to separate it from `a0(C)`; carrying it would need a value the corpus lacks, which the goal forbids defaulting (§ Invariants). The calc's doc text says the term is not carried and why. If a later item prices the conductor by the bore (WI-040 / WI-038), the term can be revisited with a sourced anchor.

### D3 — The anchor is the printed ratio times a normalised bore factor, with the factors as intermediate attributes. `[AGENT]`
`B_peak = B_axis × peak_ratio × bore_norm`, `bore_norm = bore_factor / bore_factor_ref`, `bore_factor = R / (R − a_coil)`, `bore_factor_ref = R_ref / (R_ref − a_coil_ref)`. At the design point `bore_factor` and `bore_factor_ref` are the same expression on the same floats, so `bore_norm` is exactly 1.0 and the executed product is `(B_axis × peak_ratio) × 1.0 = 24.899999999999995` — bit-identical to today (`proto.py`: `bore_norm 1.0`, `B_peak == old True`). The intermediates fix the operation order so no ulp search is needed and `peak_ratio` survives as the printed anchor with its meaning ("the peak/axis ratio at the reference geometry"). Rejected alternatives: fold the reference factor into a new held `k_peak` (an unprinted number replacing a printed one — worse provenance, and an ulp search to reproduce the product); write `B_axis × peak_ratio × bore_factor / bore_factor_ref` without intermediates (left-to-right evaluation would compute `(24.9 × 1.3298…) / 1.3298…`, not guaranteed to round back).

### D4 — Placement: the peak field changed in place; the stored energy in `mfe_magnet_field`; the casing mass in `mfe_magnet_cost`; the aspect ratio in `'Plasma Geometry'`; the coil-centre radius in `'MFE Radial Build'`. `[AGENT]`
Changing `'Conductor Peak Field'` in place keeps the module-graph edge `peak_field_calc__B_peak` that the oracle seam, the operand bindings, three fences and every committed study key on (`oracle_entry.py:142`, `:246`); a sibling would leave a dormant calc and rename the channel. The stored energy is a coil-set field quantity (beside `'Coil Set Axis Field'`); the casing mass is a cost-account operand (beside `'Magnet Structure Cost'`). The aspect ratio is a geometry output, so it lives with the volume and becomes the channel `geom__A` without a plant-level derived expression (ADR-002).

### D5 — `magnet.m_casing` stays a `'Magnet System'` attribute, bound by reference to the computed mass (the WI-036 `wp_side` pattern); five anchor attributes appear. `[AGENT]`
The generic plant binds `:>> m_casing = casing_mass.m_casing`, so `'Magnet Structure Cost'` reads `magnet.m_casing` unchanged and the attribute keeps its name and meaning while ceasing to be an entry point. The anchors `m_casing_ref`, `W_mag_ref`, `I_ref`, `R_ref`, `a_coil_ref` are new attributes bound in the instance. Census prediction: 205 → **209** (`magnet__m_casing` retires; five appear; `magnet__peak_ratio` stays). New channels: `geom__A`, `rb__r_coil_centre`, `stored_energy__W_mag`, `casing_mass__m_casing`. Rejected alternative: retire the attribute and wire the calc output straight into the structure-cost calc (changes the structure calc's binding and loses the part-level quantity).

### D6 — No defaults on the anchors; the generic plant binds by reference and the one concrete instance binds every anchor. `[AGENT]`
The existing magnet facts (`peak_ratio`, `B_max`, `k_link`, …) carry no defaults and every instance binds them; the anchors follow the same convention. "Dormant-safe" (MR-WI044-9) is met structurally: the library calcs carry no concept value, the abstract generic plant compiles with the attributes unbound, and the IFE designs do not import the MFE magnet chain. A second MFE instance (the tokamak half of epic Item 3) will bind its own anchors as it binds its own `peak_ratio`.

### D7 — The oracle derives the three channels independently from the sourced shapes; the seam publishes the new keys. `[AGENT]`
`verify_stellaris.py`: `IN` drops `magnet_m_casing` and gains the five anchors; `compute()` adds `r_coil_centre`, the two bore factors and `bore_norm`, rewrites `B_peak`, adds `W_mag`, `m_casing` and `A`, and reads `m_casing` in `magnet_structure`; the return dict gains `W_mag`, `m_casing`, `r_coil_centre`, `A`. `oracle_entry.py`: `ENTRY_KEY_TO_ORACLE_INPUT` drops `magnet__m_casing`, gains the five; `ORACLE_OUTPUT_TO_CHANNEL` gains the four channels. `OPERAND_BINDINGS` is unchanged (no verdict added; `peak_field_ok` keeps its channel key). The oracle's arithmetic is written from this design's equations, not copied from the generated module (MR-WI044-8).

### D8 — The restatement is written before regeneration, in the plan, and commits first; predictions precede execution. `[AGENT]`
The WI-041/042/043 shape: commit A carries the model edits, the twins, spec, design, plan (with the MR-WI044-11 restatement and the P1–P3 predictions) and `evidence/baseline_before/`; commit B the regenerated package, the oracle, the seam, the re-pin, the fixtures, the SV and trace rows, `evidence/baseline_after/` and `evidence/offdesign_points/`; commit C the `tests/study` run of record.

## Proposed design

### Changed: `calc def 'Conductor Peak Field'` — `models/library/analyses/mfe_plasma_scaling.sysml` (prototyped)
Formals: `B_axis_in`, `peak_ratio_in`, `R_in`, `a_coil_in`, `R_ref_in`, `a_coil_ref_in` (all `Real`, no defaults). Intermediates: `bore_factor`, `bore_factor_ref`, `bore_norm`. Output: `B_peak = B_axis_in * peak_ratio_in * bore_norm`. Doc: the eq.-39 shape, the anchoring, the term not carried (D2), the bore taken (D1), the exact-1.0 property, the sources (Table 2 image; eq. 39 image with L455; defaults.py b_max).

### Changed: `calc def 'MFE Radial Build'` — same file (prototyped)
`out attribute r_coil_centre : Real = vessel_or + coil_t_in / 2.0;` with its comment (D1). Every existing output unchanged.

### Changed: `calc def 'Plasma Geometry'` — same file (prototyped)
`out attribute A : Real = R_in / a_in;` — reported, not held, asserted on by nothing (reserved gate 1).

### New: `calc def 'Coil Set Stored Energy'` — `models/library/analyses/mfe_magnet_field.sysml` (prototyped)
Formals: `I_coil`, `a_coil`, `R0`, `W_mag_ref`, `I_ref`, `a_coil_ref`, `R_ref`. Output: `W_mag = W_mag_ref * (I_coil / I_ref) ** 2 * (a_coil / a_coil_ref) ** 2 * (R_ref / R0)`. Doc: eq. 2.82 and 2.81 with L1480 and L764; the anchoring; the configuration limit.

### New: `calc def 'Magnet Casing Mass'` — `models/library/analyses/mfe_magnet_cost.sysml` (prototyped)
Formals: `W_mag`, `W_mag_ref`, `m_casing_ref`. Output: `m_casing = m_casing_ref * (W_mag / W_mag_ref) ** 0.78`. Doc: eq. 56 with L607 and L609; the constant absorbed by the anchor because no units are printed; the seam inherited from the reference. `'Magnet Structure Cost'`: doc text says `m_casing` is computed; formals and expression unchanged.

### Changed: `part def 'Magnet System'` — `models/library/cost_structure/mfe_power_core.sysml` (prototyped)
`m_casing` kept with a "computed since WI-044" comment; five new attributes `m_casing_ref`, `W_mag_ref`, `I_ref`, `R_ref`, `a_coil_ref`; the `peak_ratio` comment says "at the reference geometry".

### Changed: `models/designs/generic_mfe/mfe_plant.sysml` (prototyped)
`magnet`: `:>> m_casing = casing_mass.m_casing`. `peak_field_calc`: the four geometry inputs (`magnet.R0`, `rb.r_coil_centre`, `magnet.R_ref`, `magnet.a_coil_ref`). New `calc stored_energy : 'Coil Set Stored Energy'` and `calc casing_mass : 'Magnet Casing Mass'` after it. `magnet_structure_cost` unchanged (comment only).

### Changed: `models/designs/stellarator_09/stellarator_plant.sysml` (prototyped)
`peak_ratio` comment extended (the anchor; the executed one-ulp fact; a 1.4 reads 25.16 T). `m_casing = 63000.0` → `m_casing_ref = 63000.0` with the D5 doc and the WI-044 note. New bindings with docs citing the renders: `W_mag_ref = 111000000000.0` (Table 2; Table 8's 110.58 disclosed), `I_ref = 15400000.0`, `R_ref = 12.7`, `a_coil_ref = 3.1500000000000004` (the executed layer sum; the paper's 2.80 m and the absorbed offset disclosed). One disclosure block (MR-WI044-6 (a)–(e)): the unprinted coefficients; the coil–plasma distance bound not modelled (`f_geo`); the transport facts as point-A facts; the wall-peak calibration constant; the fence-catching not a sourced bound.

### Twins: `exploration/stellarator_e2e/models/analyses/{mfe_plasma_scaling,mfe_magnet_field,mfe_magnet_cost}.sysml`, `cost_structure/mfe_power_core.sysml`, `designs/generic_mfe/mfe_plant.sysml`, `designs/stellarator_09/stellarator_plant.sysml` — copied byte-for-byte (implementation phase 1).

### Changed: `exploration/stellarator_e2e/verify_stellaris.py`, `studies/oracle_entry.py` (D7; implementation phase 3)

### Re-derived (D5, D8): `stellarator.snapshot.json`, `studies/manifest.json` (fingerprints; the verdict list unchanged; headline expected unchanged), `tests/models/data/mfe_census.json` (expect 209), the six `tests/study/data/*.expected.json`, `test_known_answers.py` (`EXPECTED_SEMANTIC_FINGERPRINT`, `FIXTURE_CONTRACT`), `generated/**`.

## Cross-file bindings

| Input | Bound to | Source file |
|---|---|---|
| `peak_field_calc.R_in` | `magnet.R0` | `mfe_plant.sysml` |
| `peak_field_calc.a_coil_in` | `rb.r_coil_centre` | `mfe_plant.sysml` ← `'MFE Radial Build'` |
| `peak_field_calc.R_ref_in`, `a_coil_ref_in` | `magnet.R_ref`, `magnet.a_coil_ref` | instance bindings |
| `stored_energy.{I_coil, a_coil, R0}` | `magnet.I_coil`, `rb.r_coil_centre`, `magnet.R0` | `mfe_plant.sysml` |
| `stored_energy.{W_mag_ref, I_ref, a_coil_ref, R_ref}` | the instance anchors | `stellarator_plant.sysml` |
| `casing_mass.W_mag` | `stored_energy.W_mag` | `mfe_plant.sysml` |
| `casing_mass.{W_mag_ref, m_casing_ref}` | the instance anchors | `stellarator_plant.sysml` |
| `magnet.m_casing` | `casing_mass.m_casing` (reference redefinition) | `mfe_plant.sysml` |
| `magnet_structure_cost.m_casing` | `magnet.m_casing` (unchanged) | `mfe_plant.sysml` |

Dataflow stays unidirectional: geometry (`rb`) → field (`field_calc`, `peak_field_calc`, `stored_energy`) → structural (`wp_stress`, `cond_strain`, `casing_mass`) → cost (`magnet_structure_cost`, `magnet_capital_rollup`). No new imports: the three files already import `ScalarValues`; the plant already imports the three analysis packages.

## Expected baseline behaviour (MR-WI044-7; stated before regeneration)

At the pinned baseline (`R` 12.7, `a` 1.3, `I_coil` 15.4 MA, ten verdicts satisfied, LCOE 322.31843948570247):

- `bore_norm = 1.0` exactly; `peak_field_calc__B_peak = 24.899999999999995` (bit-identical to today's executed value); `wp_stress__sigma_wp = 650000000.0`, `cond_strain__eps_cond = 0.0021666666666666666` unchanged.
- `stored_energy__W_mag = 111000000000.0` exactly; `casing_mass__m_casing = 63000.0` exactly; `magnet_structure_cost__cost = 54432000.0` bit-identical; the rollup, `total_capital`, LCOE bit-identical.
- New channels: `rb__r_coil_centre = 3.1500000000000004`, `geom__A = 9.76923076923077` (12.7 / 1.3).
- Every other channel bit-identical; all ten verdicts unchanged, `peak_field_ok` still at its one-ulp-low equality.

If any existing channel differs, the implementation stops and derives why (`goal.md` § Invariants). The one prediction that is *not* an identity: the `tests/study` fixture contract on the `a` axis, which today reaches no magnet channel and after this item reaches the peak field, the stress and strain operands, the stored energy, the casing mass, the structure cost and the rollup (the report is the source; the plan records what it actually was).

## Off-design predictions (MR-WI044-8; `prototype/proto_results.json`; the implementation executes them)

| Point | `B_peak` [T] | `sigma_wp` [MPa] | `eps_cond` | `W_mag` [GJ] | `m_casing` [t] | structure cost [$M] | Verdicts |
|---|---|---|---|---|---|---|---|
| P0 baseline (R 12.7, a 1.3, 15.4 MA) | 24.9 (−1 ulp) | 650.0 | 0.2167 % | 111.00 | 63.00 | 54.43 | ten satisfied |
| P1 (R 12.7, a 1.4, 15.4 MA) | 25.163 | 656.9 | 0.2190 % | 118.16 | 66.15 | 57.15 | `peak_field_ok` **violated** |
| P2 (R 12.7, a 2.2, 15.4 MA) | 27.491 | 717.6 | 0.2392 % | 183.49 | 93.24 | 80.56 | `peak_field_ok` **violated**; stress and strain satisfied |
| P3 `c2823` (R 15.7, a 2.2, 13 MA) | 17.231 (was 17.003) | 413.3 | 0.1378 % | 105.77 | 60.67 | 52.42 (was 54.43) | none changed |

`bore_norm`: 1.010582 / 1.104046 / 1.013382 at P1 / P2 / P3. The other verdicts at P1–P3 depend on the plasma chain (P1 and P2 are ignited on the design column at the WI-043 pin, `burn_hold_ok` violated from a 1.5 — Probe A) and are read from the execution, not predicted here; the identity claimed is that every non-magnet channel at P1–P3 equals the WI-043 pin's value at the same coordinates (the item touches nothing else). Executed with the plasma levers of the committed record (`c2823`: 13 keV, n 1.0×, 100 MW; the design-column points at the baseline's `n_e0` and `T_i0`).

## Validation plan

1. Levels 1–3 pass on `models/` with no new Level 2 warning; Levels 4–6 residue equal to the pre-change run (Level 6: 236 issues / 207 design attrs). *Done on the prototype.*
2. `tests/models` after the twin sync: 48 / 13 or better, every delta explained (the spine test on the peak-field formals passes as written).
3. Regeneration: `New: 2` (the two calc modules), `Regenerated` only on the changed non-manual calcs (peak field, radial build, geometry, plant), every handwritten impl preserved byte-identical, no `backup/` dir, seal clean.
4. The baseline diff (MR-WI044-7): every channel bit-identical; four new channels at their predicted values; ten verdicts; single-runner parity 10 / `full_satisfaction`; the oracle gate passes.
5. P1–P3 executed through `study_route.run_points` with proposals in the committed record's `point()` shape; the magnet channels equal the predictions to 1e-9 relative; every non-magnet channel equals the WI-043 pin's value at the same coordinates; the oracle re-derives the three channels and the three fences with 0.0 relative deviation.
6. Re-pin by producers; census 209 with the predicted key delta; fixtures re-derived; `tests/study` green apart from the branch's known fail-closed set (75 at entry).
7. SV-060 (baseline identity), SV-061 (the three anchors at the design point), SV-062 (off-design behaviour with oracle parity) `passing`; trace rows for the two new calcs, the two new outputs and the five anchors.

## Validation report (prototype, 2026-09-07)

- `uv run agentic-mbse validate models --complete` (`prototype/validate_complete.txt`): Level 1 pass (0 errors); Level 2 the 12 pre-existing literal-binding warnings, none new; Levels 3, 4, 5 pass; Level 6 236 issues / 207 design attrs checked — identical to the WI-043 run. **Prototype: PASS.**
- `prototype/proto.py` → `proto_results.json`: `a_coil_ref = 3.1500000000000004`; at P0 `bore_norm == 1.0`, `B_peak == 24.899999999999995 == old`, `W_mag == 111000000000.0`, `m_casing == 63000.0`, structure cost `== old`; P1–P3 as tabled.
- `tests/models/test_beta_peak_field.py`: 5 passed on the prototyped library.
- Files created / modified (tracked tree only; the twins untouched until phase 1): `mfe_plasma_scaling.sysml`, `mfe_magnet_field.sysml`, `mfe_magnet_cost.sysml`, `mfe_power_core.sysml`, `mfe_plant.sysml`, `stellarator_plant.sysml`.

## Implementation checklist (phased; the plan carries the checkboxes)

1. Twins synced; Levels 1–3; `tests/models`.
2. The MR-WI044-11 restatement and the P1–P3 predictions in the plan; `evidence/baseline_before/` from the unchanged package; commit A.
3. Regeneration; the oracle and the seam rewritten (D7); the single runner's comments restated; the baseline diff; P1–P3 executed and deposited.
4. Re-pin (snapshot → manifest → census → fixtures → single runner); batteries; SV and trace rows; commit B.
5. `tests/study` run of record; commit C.

## Risks

1. **`bore_norm` is not exactly 1.0 in the generated module** (the codegen reorders or folds the intermediates). *Likelihood: low.* The radial build's intermediates are emitted verbatim in order. *Mitigation:* the baseline diff catches it at once; the fix is the operation order, never the anchor value; if the codegen cannot preserve the order, that is a `PREREQUISITE` return naming codegen.
2. **The regeneration re-stencils a manual stage.** *Likelihood: very low* — no manual calc's inputs change. *Mitigation:* the `gotcha_codegen_manual_stage_regen` recipe if `Regenerated` names one.
3. **The fixture contract's prediction on the `a` axis is wrong in detail.** *Mitigation:* re-derived from the report; the phase record says what it was.
4. **A literal count of channels or entry points hides somewhere.** *Mitigation:* the batteries; each restated from the live package with a dated comment.
5. **A reader takes P1's violation as "the model bounds `a` at 1.3".** *Mitigation:* the disclosure block (e) and the goal's invariant; the study reports the fence as a consequence of the anchored shapes.

## Approval

The owner delegated the modelling judgement at grounding (`goal.md` § Reserved gates); this design proceeds to `/plan-model` under that delegation, as WI-043 did. The fresh round review is the independent check; `/review-model` is available if the owner wants one before the round closes.
