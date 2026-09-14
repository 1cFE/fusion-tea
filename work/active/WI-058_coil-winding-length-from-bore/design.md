---
Status: complete
Created: 2026-09-14
Updated: 2026-09-14
Related Artifacts:
  Spec: ./spec.md
---

# WI-058 Design — the winding length follows the coil bore

One sourced shape, anchored at the design point, makes the coil winding circumference follow the coil-centre radius the radial build produces; the major radius drops out of the length; one held constant (the printed 25 m) replaces one held constant (the shape factor over `R`). Written under goal `magnet-coil-realism` round 1, task T-001; the form is `[AGENT] (ratified by owner, 2026-09-14)` (`goal.md` § Reserved gates 1–2). Prototyped through the entering oracle (`prototype/proto.py`, `proto_results.json`) and the tracked model files validated at Levels 1–6 with the pre-change residue.

## Overview

Today `c_coil = k_coil × R0` (spec § Current state). After this item:

- `'Coil Winding Length'` takes `a_coil` (the coil-centre minor radius), `c_coil_ref` and `a_coil_ref`, and computes `c_coil = c_coil_ref * (a_coil / a_coil_ref)`;
- `'Modular Coil'` carries `c_coil_ref` (the printed typical circumference at the reference bore) in place of `k_coil`;
- `'Magnet System'` binds the calc to its wired `r_coil_centre` and the coil's two anchors; the instance binds `c_coil_ref = 25.0` with the § 2.9 cite and the disclosure of the implied shape factor and of what `R` no longer does;
- the oracle computes the same form from `r_coil_centre`; the seam maps `magnet__coil__c_coil_ref` and drops `magnet__coil__k_coil`.

At the baseline every channel is bit-identical (§ Expected baseline behaviour). Off the design point the winding procurement, the cold volume, the conductor length and the legacy account scale with the bore and are invariant in `R` at fixed `a` (§ Off-design predictions).

## Research findings

- **Where the corpus puts the coil's size.** Stellaris § 2.9 (`stellaris-design-details.md@e5a2cb23` L1862): "approximate size of 7 × 5 × 10 m, with a typical circumference of 25 m". The model's coil-centre radius at the design point is 3.1500000000000004 m (WI-044 D1; `rb__r_coil_centre`), so the 7 × 5 m coil face sits on a 6.3 m bore and 25 m is 1.263 × the circle at the centre radius (2π × 3.15 = 19.79 m; a plane 7 × 5 m rectangle has perimeter 24 m). No per-coil circumference is printed (WI-036 D3 already recorded this); Table 8 prints per-coil tape lengths and turn counts, whose ratio is a circumference per coil only under an assumption about grading, so it is not used as a second anchor.
- **How PROCESS scales coil length.** Lion 2021 L118 (`…systems_code_process/output.md@d4059ef1`): "extrapolations of the reference point C in … the major overall size of the machine (coil and plasma size), the minor plasma radius `a` at constant coil radius, and the total magnetic field strength"; L120: "the coil number and the coil shapes are considered fixed … and only the overall size of the coils is scaled". So in PROCESS a coil has one scale parameter (its size, at fixed shape), the coil size rides with the overall machine size, and `a` never changes the coil. The thesis (L643–645) repeats the prescription. Neither prints a coil-length formula; the length is implicit in the fixed-shape scaling.
- **Which coupling this build has.** 'MFE Radial Build' sets the coil bore as `a` plus a fixed layer stack (WI-021), and WI-044 made the peak field, stored energy and casing mass read the coil-centre radius. So here the coil's size follows the plasma; PROCESS's "`a` at constant coil radius" is the case this build cannot express (it needs the coil–plasma distance `d_pc(C)` and `f_geo`, WI-044 disclosure (i)). Given the build's coupling, a fixed-shape coil scaled to its bore has circumference ∝ bore radius. Under uniform scaling (R and `a` together at fixed aspect ratio) `a_coil / a_coil_ref = R / R_ref` and the two forms coincide, so PROCESS's own scans are reproduced.
- **What grows with `R` at fixed bore.** The toroidal coil–coil spacing (2πR / N). PROCESS treats it as a clearance constraint — "the minimal distance between two central coil filaments `d_min(C)` … scales linearly with the major radius" (§ 3.10, L621) — not as a length term. A non-planar coil's toroidal excursion is part of its fixed shape and scales with the coil, not with the spacing. No source gives an excursion term in `R`; the model text says "none" with this reason (MR-WI058-3).
- **The design-point float.** `1.968503937007874 × 12.7 == 25.0` is `True` in float64 (`prototype/proto.py` line 1 of output), so today's executed `c_coil` is exactly 25.0 and the conductor length 321,600 m exactly. The new form gives `25.0 × (3.1500000000000004 / 3.1500000000000004) = 25.0 × 1.0 = 25.0` — no ulp search (D3).
- **The winding length is auto-implemented.** `generated/handwritten/mfe_magnet_field/coil_winding_length_impl.py` carries `AUTO_IMPLEMENTED = True` and the body `inputs.k_coil * inputs.R0` generated from the expression; the regeneration rewrites it from the new expression. No manual stage is touched (the `gotcha_codegen_manual_stage_regen` recipe does not trigger).
- **What moves at the harness's R 14 point.** The prototype (`prototype/r14_differing_channels.json`) lists the 44 channels that differ at `R` 14, `a` 1.3 between the entering form and the bore form: the winding chain (−9.29 %), the magnet rollup (−9.0 %), the cryoplant electrical (−3.9 %) and capital, the power balance (`p_net` +3.3e-5, `rec_frac`, `q_eng`), the net-power-scaled accounts (precon, owner, O&M, other RPE, fuel handling, coolant; ≤ 2.6e-5) and the capital rollups down to both LCOEs (−2.1 %). Zero channels differ at the design point.

## Design decisions

### D1 — The bore the length takes is the coil-centre radius, `rb.r_coil_centre`. `[AGENT]`
The same bore WI-044 gave the peak field, the stored energy and the casing mass (D1 there: Stellaris states its coil facts at the centre filament). The winding pack is centred on that filament, so its circumference is measured there. `r_coil = vessel_or` stays the 1costingFE conductor-quantity bore for 'Magnet Coil Cost' and is not re-pointed.

### D2 — The form is the anchored ratio, not a shape factor times 2π. `[AGENT]`
`c_coil = c_coil_ref * (a_coil / a_coil_ref)`. The held constant is the printed 25 m (better provenance than a derived 1.263); the ratio is exactly 1.0 at the design point on the same floats; no `2π` literal and no second constant enter. The implied shape factor `c_coil_ref / (2π a_coil_ref) = 1.2631344689832962` is disclosed in the doc comments as the coil's departure from a circle, not bound. Rejected: `k_shape × 2π × r_coil_centre` with `k_shape` bound (an unprinted number replacing a printed one, and a product that need not round back to 25.0).

### D3 — `R` does not enter; the model text says so and why. `[AGENT]`
MR-WI058-3 and the research findings. The calc keeps no `R0` formal. The doc comment names the clearance PROCESS checks and this model does not, so the limit is visible at the calc.

### D4 — Placement: the calc changes in place; `k_coil` retires; `c_coil_ref` appears on 'Modular Coil'. `[AGENT]`
Changing 'Coil Winding Length' in place keeps the module and the channel `magnet__coil_length__c_coil` every consumer keys on. `c_coil_ref` sits beside `a_coil_ref`, `R_ref`, `I_ref` on the coil part (the WI-044 anchor convention). Census: 265 → **265** (`magnet__coil__k_coil` retires; `magnet__coil__c_coil_ref` appears); channels unchanged (196). No new imports.

### D5 — No defaults on the anchor; the instance binds it. `[AGENT]`
`c_coil_ref` has no default (MR-WI058-9); the generic plant binds nothing new (it already wires `r_coil_centre`); the one concrete instance binds 25.0.

### D6 — The oracle derives the length from the design's equation; the seam publishes the key change. `[AGENT]`
`verify_stellaris.py`: `IN` drops `magnet_k_coil`, gains `magnet_c_coil_ref = 25.0`; `compute()` sets `c_coil = p["magnet_c_coil_ref"] * (r_coil_centre / p["magnet_a_coil_ref"])` after `r_coil_centre` (already computed). `oracle_entry.py`: the entry map drops `magnet__coil__k_coil`, gains `magnet__coil__c_coil_ref`. `OPERAND_BINDINGS` and the channel map are unchanged.

### D7 — Consumers are restated by identity or from the live package, each with a dated comment; none patched to match. `[AGENT]`
- `tests/study/test_domain_consumers.py`: the three `k_coil × R` length identities become `c_coil_ref × r_coil_centre / a_coil_ref` (the oracle output `r_coil_centre` is on every row); for the `R` 14 control row, the winding-length descendants are checked by identity (the winding chain from the new length; the cryoplant from the new cold volume; `p_net` shifted by the cryoplant delta; the net-power-scaled accounts by their own power law on the oracle's `p_net`; the rollups additive), the rest exactly as frozen.
- `tests/models/current_mfe_regressions.py`: the WI-051 replay's frozen R 14 expectations for the winding-length descendants (declared as `WI058_R14_RESTATED`, the oracle names of the 44-channel list less those already restated by WI-040) are replaced by the current oracle's values; the `coil_length__c_coil` ratio expectation becomes 1.0; the `coil_length` `R0` edge and the standalone `R0`-consumer row are removed from the replay; the contract delta gains `k_coil` removed and `c_coil_ref` added; the receipts (`model-hashes.json`, `package-hashes.json`) are read from this item's `evidence/`.
- `tests/models/test_mfe_major_radius.py`: `coil_length` leaves the `R0`-consumer parametrisation; a WI-058 test asserts the calc's formals are `a_coil`, `c_coil_ref`, `a_coil_ref`, the design-point identity, the bore response and the `R`-invariance through the generated module and the oracle.
- `tests/models/test_structure_translation.py`: the live parameter set equals the ledger's less `k_coil` plus `c_coil_ref` (declared).
- `tests/study/data/*.expected.json`, `test_known_answers.py`: re-derived by the indicator report (the `a` axis now reaches the winding chain, the cryoplant and the power balance; the `R` axis no longer fires `coil_length`).
- `tests/model_viz/viewer_harness.py`: the snapshot hash re-pinned after recapture.

### D8 — The restatement and the predictions are written before regeneration, in the plan, and commit first. `[AGENT]`
The WI-044 shape: commit A carries the model edits, the twins, spec, design, plan (with the predictions) and `evidence/baseline_before/`; commit B the regenerated package, the oracle, the seam, the re-pin, the restated tests, the SV and trace rows, `evidence/baseline_after/` and `evidence/offdesign_points/`; commit C the `tests/study` run of record.

## Proposed design

### Changed: `calc def 'Coil Winding Length'` — `models/library/analyses/mfe_magnet_field.sysml`
Formals: `a_coil`, `c_coil_ref`, `a_coil_ref` (all `Real`, no defaults). Output: `c_coil = c_coil_ref * (a_coil / a_coil_ref)`. Doc: the bore form; the anchoring; the implied shape factor disclosed; `R` does not enter and why (PROCESS's prescription; the clearance not carried); sources (Stellaris § 2.9; Lion 2021 L118–120, § 3.10; WI-044 D1).

### Changed: `part def 'Modular Coil'` — `models/library/structure/mfe_magnet_parts.sysml`
`k_coil` retires; `c_coil_ref : Real` appears ("printed typical winding circumference [m] at the reference bore a_coil_ref (WI-058)"); the `c_coil` comment updated; the part doc's "(major radius, geometry factor, winding circumference and shape factor…)" reworded.

### Changed: `part def 'Magnet System'` — `models/library/cost_structure/mfe_power_core.sysml`
`calc coil_length : 'Coil Winding Length' { in a_coil = r_coil_centre; in c_coil_ref = coil.c_coil_ref; in a_coil_ref = coil.a_coil_ref; }` with the WI-058 comment; the WI-036 comment above it reworded.

### Changed: `models/designs/generic_mfe/mfe_plant.sysml`
Comment only: the WI-036 note ("j_wp and k_coil are the settable levers") reworded to name `c_coil_ref` and the bore.

### Changed: `models/designs/stellarator_09/stellarator_plant.sysml`
`:>> k_coil = 1.9685039370078741 { … }` → `:>> c_coil_ref = 25.0 { doc … }` with the § 2.9 cite (the sentence; the `7 × 5 × 10 m`), the WI-044 bore (`a_coil_ref` 3.1500000000000004; the paper's own 2.80 m coil-centre distance absorbed by the ratio, as WI-044 disclosed), the implied 1.2631… shape factor, and the "typical but approximate" weak link. The WI-044 disclosure block gains one clause: (iv) the winding length follows the bore at fixed shape; the toroidal coil–coil clearance at fixed bore and growing `R` is not checked.

### Twins: `exploration/stellarator_e2e/models/{analyses/mfe_magnet_field, structure/mfe_magnet_parts, cost_structure/mfe_power_core, designs/generic_mfe/mfe_plant, designs/stellarator_09/stellarator_plant}.sysml` — copied byte-for-byte (implementation phase 1).

### Changed: `exploration/stellarator_e2e/verify_stellaris.py`, `studies/oracle_entry.py` (D6; phase 3); the consumers of D7 (phase 3–4).

### Re-derived (D4, D8): `stellarator.snapshot.json`, `studies/manifest.json`, `tests/models/data/mfe_census.json` (265, the key swap), the five `tests/study/data/*.expected.json`, `test_known_answers.py` (`EXPECTED_SEMANTIC_FINGERPRINT`, `FIXTURE_CONTRACT`), `generated/**`, `evidence/{model,package}-hashes.json`.

## Cross-file bindings

| Input | Bound to | Source file |
|---|---|---|
| `coil_length.a_coil` | `r_coil_centre` (the 'Magnet System' attribute the plant wires from `rb.r_coil_centre`) | `mfe_power_core.sysml`; `mfe_plant.sysml` (existing wire) |
| `coil_length.c_coil_ref` | `coil.c_coil_ref` | instance binding `stellarator_plant.sysml` |
| `coil_length.a_coil_ref` | `coil.a_coil_ref` | instance binding (WI-044) |
| `coil.c_coil` | `coil_length.c_coil` (unchanged) | `mfe_power_core.sysml` |
| `wp_volume.c_coil`, `winding_procurement.c_coil`, `winding_pack_cost.c_coil` | `coil_length.c_coil` / `coil.c_coil` (unchanged) | `mfe_power_core.sysml` |

Dataflow stays unidirectional: geometry (`rb`) → `coil_length` → cold volume / ampere-metres → procurement, cryoplant → power balance → cost. `coil_length` now sits after the radial build in the execution order, where `peak_field_calc` and `stored_energy` already are.

## Expected baseline behaviour (MR-WI058-2; stated before regeneration)

At the pinned baseline (`R` 12.7, `a` 1.3, 15.4 MA, 17 of 18 verdicts satisfied, LCOE 142.50725862880648): `coil_length__c_coil = 25.0` exactly; `wp_volume__vol_winding_pack = 136.55999999999997`, `winding_procurement__conductor_length = 321600.0`, `winding_procurement__cost = 1570369801.0347085`, `winding_pack_cost__cost = 5346600000.0`, `cryo_elec__p_elec = 0.8643515999999999`, `magnet_capital_rollup__capital_cost = 1624801801.0347085`, every other channel bit-identical; 18 verdicts unchanged. The prototype confirms: zero channels differ at the design point (`proto_results.json` P0, "every channel identical: True"). If any existing channel differs, the implementation stops and derives why.

## Off-design predictions (MR-WI058-5; `prototype/proto_results.json`; the implementation executes them)

| Point | `a_coil` [m] | ratio | `c_coil` [m] | procurement [$M] | legacy [$M] | `p_cryo` [MW] | magnet capital [$M] | LCOE [$/MWh] (pin → new) |
|---|---|---|---|---|---|---|---|---|
| P0 baseline (R 12.7, a 1.3) | 3.1500000000000004 | 1.0 | 25.0 | 1570.37 | 5346.60 | 0.8643516 | 1624.80 | 142.507258629 → same |
| P1 (R 12.7, a 1.4) | 3.2500000000000004 | 1.0317460317460319 | 25.793650793650798 | 1620.22 | 5516.33 | 0.875124666667 | 1677.37 | 133.079555591 → 134.045816769 |
| P2 (R 12.7, a 2.2) | 4.050000000000001 | 1.2857142857142858 | 32.142857142857146 | 2019.05 | 6874.20 | 0.9613092 | 2099.61 | 122.509796833 → 129.349933886 |
| P3 (R 15.7, a 1.3) | 3.1500000000000004 | 1.0 | 25.0 | 1570.37 | 5346.60 | 0.8643516 | 1616.50 | 209.511809621 → 201.021337169 |
| P4 (R 15.7, a 2.2) | 4.050000000000001 | 1.2857142857142858 | 32.142857142857146 | 2019.05 | 6874.20 | 0.9613092 | 2087.33 | 155.43373937 → 156.356236257 |
| P5 (R 11.43, a 1.3) | 3.1500000000000004 | 1.0 | 25.0 | 1570.37 | 5346.60 | 0.8643516 | 1629.46 | 136.447344404 → 140.280018085 |

Exact floats in `proto_results.json`. The peak field, the stress, the strain, the stored energy and the casing mass do not move at any point (they do not read the length); `p_th` does not move; `p_net` moves by the cryoplant delta only. Every point executes at the package defaults except `R`, `a` and `availability_direct = 0`. The verdicts other than the three magnet fences and the recirculating fence are read from the execution.

## Validation plan

1. Levels 1–3 on `models/` with no new Level-2 warning; Levels 4–6 residue equal to the pre-change run. *Done on the prototype (§ Validation report).*
2. `tests/models` after the twin sync: 889 / 13 at entry; the deltas are the D7 restatements, each explained.
3. Regeneration: `Regenerated` on `coil_winding_length` and the plant modules only; every handwritten impl preserved byte-identical; no `backup/`; seal clean.
4. The baseline diff: every channel bit-identical; 18 verdicts; the single runner's anchors green; the oracle gate passes.
5. P1–P5 through `study_route.run_points`; the magnet channels equal the predictions to 1e-9 relative; the oracle seam at 0.0 relative on the winding chain and the cryoplant; P3 and P5 equal P0 on every winding channel to the double.
6. Re-pin by producers; census 265 with the key swap; fixtures re-derived; `tests/study` green apart from the branch's known fail-closed set; `tests/model_viz` green on the re-pinned hash.
7. SV rows (baseline identity; bore response and `R`-invariance; oracle parity) `passing`; trace rows for the changed calc and `c_coil_ref`.

## Validation report (prototype, 2026-09-14)

- `prototype/proto.py` → `proto_results.json`: `1.968503937007874 × 12.7 == 25.0`; P0 every channel identical; P1–P5 as tabled; `k_shape = 1.2631344689832962`.
- `prototype/r14_diff.py` → `r14_differing_channels.json`: 44 channels differ at R 14 / a 1.3, 0 at the design point.
- `prototype/validate_complete.txt`: recorded in implementation phase 1 after the model edits (Levels 1–6).

## Risks

1. **A consumer counts entry points by literal or names `k_coil`.** *Mitigation:* the batteries; the grep of the three spellings (`gotcha_repin_after_regeneration`, renaming entry keys); each restated with a comment.
2. **The WI-051 replay's frozen expectations at R 14 hide a descendant not in the declared set.** *Mitigation:* the set is derived from the oracle diff (44 channels) and the harness fails loudly on any undeclared drift; a miss is a declared-set fix, never a tolerance change.
3. **The `a` axis's fixture contract changes more than predicted.** *Mitigation:* re-derived from the report; the plan records what it was.
4. **A reader takes the `R`-invariance as "bigger machines need no more conductor".** *Mitigation:* the doc comment names the clearance not carried; the goal's study reads `R` and `a` together.

## Approval

The owner delegated the modelling judgement at grounding (`goal.md` § Reserved gates); this design proceeds to `/plan-model` under that delegation, as WI-044 did. The fresh round review is the independent check.
