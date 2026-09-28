---
Status: complete
Created: 2026-09-04
Updated: '2026-09-05'
Related Artifacts:
  Spec: ./spec.md
---

# WI-041 Design — the source-anchored wall-load fence

Designed under goal `wall-and-heating`, round 2, task T-002. The spec's four open decisions are settled here with their reasoning and cost, because the round review reads this file to check that the increment stayed inside its scope and that no number was tuned.

## Overview

Today the model divides neutron power by a circular-torus area and compares that **average** with the source's printed **peak** limit. This design adds two small library calcs — a calibration computed from six printed source facts, and the peak as the average times that calibration — moves the wall chain up to the generic plant so both the fence and the lifetime calc can read the peak, and makes the lifetime calc's wall-load operand an explicit input bound to the peak. The average survives untouched as a reported quantity.

At the source's own design point the computed peak equals the printed peak by construction. At the model's baseline, whose fusion power is 0.94 % above the source's 2700 MW, the peak reads 4.088 against 4.05 and the fence flips to violated. That is the expected result, disclosed here and never tuned. CAS72 rises 37 % because the core now lives 4.40 full-power years instead of 5.80 and is replaced five times instead of four.

## Research findings

**The source prints one peak and no usable average basis** (`work/orchestration/goals/wall-and-heating/evidence/round2_T-001_source_basis.md`). Peak 4.05 MW/m² at ~2700 MW on the design's own CAD first wall (Table 2 image; Fig. 33's 0–4 MW/m² scale). The 2.87 average has no stated basis and is not a wall average by the source's own cited definition. The printed radii are 12.7 m and 1.3 m (Tables 1, 2, 5 images); the minimum plasma-to-wall standoff is 100 mm (line 1295); the averaged SOL gap is 16.6 cm (Fig. 34). The model already carries R 12.7, a 1.3, kappa 1.0 and `vacuum_t` 0.10 — the source's minimum standoff.

**Lifetime is set by the peak** (T-001 § 4). Table 6 derives the first-wall lifetime (~4–6 FPY) from the peak first-wall DPA; [240] states "the lifetime of the blanket is determined by the peak loads". The model's fluence chain at the source's peak gives 18 / 4.05 = 4.44 FPY, inside the band.

**The model's wall chain is split across two files.** The average is instantiated only in the stellarator instance (`stellarator_plant.sysml:1149`), while the lifetime calc is wired in the generic plant (`mfe_plant.sysml:898-907`) and computes its own neutron power from `fusion.p_fus`, the plant attribute `ash_frac` and `rb.wall_area`. For the peak to reach both consumers, the chain has to live where the lifetime calc lives.

**Two ash-fraction conventions coexist today.** The average uses the calc's default 0.2002; the lifetime calc uses the instance's exact 0.2002275 (`stellarator_plant.sysml:1100`, bound exactly "because the CAS72 chain is compared under A-2 at 1e-6" — the 1costingFE handshake, broken since the migration). They differ by 3.4 × 10⁻⁵ relative. Recomputed from the recorded baseline: CAS72 at the average-with-0.2002 would read 95,901,232 against the recorded 95,898,253.

**The codegen envelope** (migration ledger; WI-039 design): arithmetic only inside calc defs, `+ - * / **`; every calc-input binding a bare attribute reference or a calc output; defaulted formals declared last. The lifetime calc is a manual stage whose handwritten impl is preserved across regeneration and edited by hand.

**The channel name survives a move.** Channels are named by the instance path, not by where the usage is declared: `cas72_calc` is declared in the generic plant and its channel is `stellarator_09__stellaris__cas72_calc__cost`. Moving `wall_load_calc` to the generic plant under the same usage name keeps `stellarator_09__stellaris__wall_load_calc__wall_load`, which seven study definitions, `study_route.py`, `oracle_entry.py` and a test fixture read by name.

## Design decisions

### D1 — The wall chain moves up to the generic plant, dormant-safe by an additive direct term. `[AGENT]`

**The decision.** `wall_load_calc` (the average), `wall_peak_cal` (the calibration) and `wall_peak_calc` (the peak) are declared in `'MFE Power Plant'`, beside `fusion`. Seven plant attributes carry the calibration's inputs with dormant defaults: `wall_peak_q_ref 0.0`, `wall_peak_p_fus_ref 1.0`, `wall_peak_R_ref 1.0`, `wall_peak_a_ref 1.0`, `wall_peak_kappa_ref 1.0`, `wall_peak_standoff_ref 0.0`, `wall_peak_calibration_direct 1.0`. With those defaults the calibration is 0 × A / p + 1 = 1.0 and the peak equals the average, so a concept that anchors to no source keeps today's fence semantics exactly. The stellarator instance binds the six source facts and zeroes the direct term.

**Why not leave the chain in the instance.** The lifetime calc is generic and must read the peak; an instance-level calc cannot feed a generic-level binding. Moving the chain is the only way one peak reaches both the fence and the lifetime calc.

**Why the direct term and not a defaulted calibration.** A calibration computed from six facts cannot default to 1.0 by defaulting its inputs — no natural defaults make q × A / p_n equal one. The additive direct term is the pattern this repository already uses twice for exactly this problem (WI-024 `p_cryo`, WI-039 `p_coupled_direct`), and following it costs nothing.

**What it costs.** Seven new entry points (the census moves); the instance's own `wall_load_calc` declaration is deleted because the generic one is inherited under the same name.

### D2 — The lifetime calc takes the wall load as an explicit input, bound to the peak. `[AGENT]`

**The decision.** `'Levelized Replacement Cost'` loses `p_fus`, `ash_frac_in` and `firstwall_area` and gains `in attribute q_n_in : Real` — the wall load that sets lifetime. The generic plant binds it to `wall_peak_calc.wall_load_peak`. The handwritten impl and the oracle mirror take `q_n` directly.

**The alternative, and why it loses.** Keeping the interface and adding a multiplicative `peaking_in` (default 1.0) is a smaller edit and needs no retirement. It loses on legibility and on consistency: the peak would then be computed twice — once for the fence, once inside the lifetime calc — with two ash-fraction conventions, so the fence's operand and the lifetime's operand would differ by 3.4 × 10⁻⁵ and a reviewer would rightly ask which is the peak. With an explicit input there is one peak, computed once, and "the lifetime operand is the peak" is a visible binding a reader can point at, which is what the round-1 review asked for.

**What retires with it.** The plant attribute `ash_frac` (`mfe_plant.sysml:893`) and its exact instance redefinition (`stellarator_plant.sysml:1100`) have no reader once the lifetime calc stops computing its own neutron power. Both retire. The exact binding's stated purpose — a 1e-6 comparison of the CAS72 chain against 1costingFE — is moot: the handshake it served has been broken since the migration (WI-039 plan § MR-WI039-9), and the peak operand departs from 1costingFE's average-based chain by design. The sustainment calc's own `sustain__ash_frac_in` is untouched.

**Convention change, stated.** The lifetime chain's neutron fraction moves from the exact 0.79977 to the wall-load calc's 0.7998. At the baseline that is a 3.4 × 10⁻⁵ relative change in the operand, folded into the declared CAS72 move and named in the restatement.

### D3 — The calibration's decomposition lives in doc text, not in attributes. `[AGENT]`

The calibration could be carried as a peaking factor times an area ratio (T-001 § 5 option a) with the source's damage peaking 1.77 and a derived 945 m² wall area as attributes. It is carried instead as one computed quantity from six printed facts (option b), with the decomposition and the external 1.5–2.1 band written into the instance's doc comment as the plausibility bounds the strategy asked for. Reason: option (a) puts two inferred numbers into the model — a DPA-to-NWL transfer the source only calls "relative", and a wall area the source never prints — where option (b) puts none. The bounds are still on the record where a reviewer looks.

### D4 — The constancy assumption is stated once, in the library, and the instance says what it means for this machine. `[AGENT]`

The library calc's doc carries the assumption (the calibration is fixed at the source's design point; the wall's peaking and shape factors are taken constant over sweeps). The instance's doc says what it means here: a sweep of R or a moves the peak through the model's own `wall_area` while the wall's shape is assumed to scale with it; a re-shaped wall would need a new anchor. The study carries a shadow column at the external band so the sensitivity is data.

### D5 — The doc-text corrections ride this regeneration. `[AGENT]`

A doc-text change re-pins the package, so the three stale comments the round owes are corrected here rather than in a separate item: the WI-022 cross-check comment (rewritten to what T-001 established), the two archived WI-039 paths, and the EI-5 dormant-mode sentence in the heating chain's library doc.

## Proposed design

### New: `calc def 'Neutron Wall Load Peak Calibration'` — `models/library/analyses/mfe_plasma_scaling.sysml` (prototyped)

| quantity | kind | units | meaning |
|---|---|---|---|
| `q_peak_ref` | in | MW/m² | the source's printed peak neutron wall load |
| `p_fus_ref` | in | MW | the source's fusion power at that peak; never 0 |
| `R_ref`, `a_ref`, `kappa_ref`, `standoff_ref` | in | m, m, 1, m | the source's radii, elongation and minimum standoff — the model's own wall-area convention at the source's point |
| `calibration_direct` | in | 1 | additive direct term; 1.0 leaves a dormant concept at peak = average |
| `ash_frac_in` | in, default 0.2002 | 1 | must equal the paired average's value; declared last |
| `pi` | in, default 3.14159265358979 | 1 | declared last (migration ledger D13) |
| `A_ref` | attribute | m² | `kappa_ref · 4π² · R_ref · (a_ref + standoff_ref)` |
| `p_n_ref` | attribute | MW | `p_fus_ref · (1 − ash_frac_in)` |
| `calibration` | out | 1 | `q_peak_ref · A_ref / p_n_ref + calibration_direct` |

### New: `calc def 'Neutron Wall Load Peak'` — same file (prototyped)

`in wall_load`, `in calibration_in`; `out wall_load_peak = wall_load · calibration_in`.

### Changed: `calc def 'Levelized Replacement Cost'` — `models/library/analyses/mfe_account_costs.sysml`

- `in p_fus`, `in ash_frac_in`, `in firstwall_area` are **removed**; `in attribute q_n_in : Real;` (the wall load that sets lifetime [MW/m²]) replaces them, declared where `p_fus` was.
- The doc's chain drops its first two lines (`p_neutron`, `q_n`) and says the operand arrives computed — the plant binds the peak, because the source and its cited method set lifetime by the peak. The WI-029 note about computing the neutron power inside the calc is deleted (its reason is gone), not amended.
- The handwritten impl `generated/handwritten/mfe_account_costs/levelized_replacement_cost_impl.py`: `levelized_replacement_cost(cost_per_event, q_n, fluence_limit, availability, interest_rate, operational_years)`; the two dropped lines go; `run_levelized_replacement_cost` reads `inputs.q_n_in`. Its docstring says the operand is the peak and why.

### Changed: `constraint def 'Neutron Wall Load Limit'` — `mfe_viability.sysml:60-77`

Doc text only: the operand is the computed **peak** ('Neutron Wall Load Peak'), the limit the source's printed peak, both on the source's wall basis; the Ref line adds the Table 6 lifetime rows and drops nothing.

### Changed: `models/library/analyses/mfe_heating_chain.sysml:30-35`

One sentence (EI-5): a dormant concept must bind `eta_source` to its former lumped efficiency as well as the direct powers, or its recirculating draw equals its coupled power with no conversion loss.

### Changed: `models/designs/generic_mfe/mfe_plant.sysml`

After the `fusion` calc:

```sysml
        // ---- Neutron wall load: average, source-anchored calibration, peak (WI-041) ----
        calc wall_load_calc : 'Neutron Wall Load' {
            in p_fus = fusion.p_fus;
            in wall_area = rb.wall_area;
        }
        // Reference facts for the peak calibration. Dormant by default: a concept
        // with no source peak leaves q_ref at 0 and the direct term at 1.0, so
        // the calibration is 1.0 and the peak equals the average.
        attribute wall_peak_q_ref : Real default 0.0;
        attribute wall_peak_p_fus_ref : Real default 1.0;
        attribute wall_peak_R_ref : Real default 1.0;
        attribute wall_peak_a_ref : Real default 1.0;
        attribute wall_peak_kappa_ref : Real default 1.0;
        attribute wall_peak_standoff_ref : Real default 0.0;
        attribute wall_peak_calibration_direct : Real default 1.0;
        calc wall_peak_cal : 'Neutron Wall Load Peak Calibration' {
            in q_peak_ref = wall_peak_q_ref;
            in p_fus_ref = wall_peak_p_fus_ref;
            in R_ref = wall_peak_R_ref;
            in a_ref = wall_peak_a_ref;
            in kappa_ref = wall_peak_kappa_ref;
            in standoff_ref = wall_peak_standoff_ref;
            in calibration_direct = wall_peak_calibration_direct;
        }
        calc wall_peak_calc : 'Neutron Wall Load Peak' {
            in wall_load = wall_load_calc.wall_load;
            in calibration_in = wall_peak_cal.calibration;
        }
```

`cas72_calc`: `in q_n_in = wall_peak_calc.wall_load_peak;` replaces the three neutron-power bindings; `attribute ash_frac` (`:893`) and its comment are removed.

### Changed: `models/designs/stellarator_09/stellarator_plant.sysml`

- The instance's `calc wall_load_calc` block (`:1149-1152`) is **deleted** — the generic one is inherited under the same name and channel.
- `:>> ash_frac = 0.2002275312855518` (`:1100-1110`) is **deleted** (D2).
- Six bindings, each citing its page image: `:>> wall_peak_q_ref = 4.05` (Table 2 image, "Peak neutron wall load"; 3D on the design's own first wall at 2700 MW by [240]'s method, Fig. 33); `:>> wall_peak_p_fus_ref = 2700.0` (Table 2 image, "Peak fusion power ~2700"; Fig. 33 caption "at 2700 MW fusion power"); `:>> wall_peak_R_ref = 12.7` and `:>> wall_peak_a_ref = 1.3` (Table 2 image); `:>> wall_peak_kappa_ref = 1.0` (the model's own convention, `kappa` at `:472`); `:>> wall_peak_standoff_ref = 0.10` (line 1295, the minimum 100 mm — the source's *averaged* SOL gap is 16.6 cm, Fig. 34, and the model's `vacuum_t` is the minimum; the calibration absorbs the difference at the design point); `:>> wall_peak_calibration_direct = 0.0` (the chain is live).
- The instance doc on `wall_peak_q_ref` carries D3's decomposition cross-check and D4's meaning for this machine: calibration 1.3164 = p_f × (A_torus / A_wall); the source's own damage peaking 3.9 / 2.2 = 1.77 (Fig. 38) implies a wall area of about 945 m², the printed 940 m² plasma surface plus a standoff; the round-1 external band p_f 1.5–2.1 (Lion, Häußler, Beidler) implies 800–1120 m². The 4.05 / 2.87 = 1.41 ratio is not a peaking factor.
- The cross-check comment (`:1126-1143`) is rewritten: the average 3.105 is the model's circular-torus average at the minimum standoff; the source's 2.87 has no stated basis (equal to fusion power over the printed 940 m² plasma surface to three figures) and is not comparable to it; the source's peak is 4.05 on its own wall; the model's peak reads 4.088 at its 0.94 % fusion-power excess — **violated, disclosed**.
- `wall_load_limit`'s doc drops the 4.95 hedge and cites the Table 2 image and the Table 5 image's absence of any peak row.
- `wall_load_ok`: `in wall_load = wall_peak_calc.wall_load_peak;` with a comment stating the disclosed baseline verdict.
- Exposed: `attribute neutron_wall_load_peak : Real = wall_peak_calc.wall_load_peak;` and `attribute wall_peak_calibration : Real = wall_peak_cal.calibration;` beside `neutron_wall_load` (`:1192`).
- `:700,703`: the WI-039 design path → `work/completed/20260904_WI-039_heating-system-structure/design.md`.

### Changed: `exploration/stellarator_e2e/verify_stellaris.py` and `studies/oracle_entry.py`

The oracle carries the six reference facts and the direct term in `IN`, computes its own `A_ref`, `p_n_ref`, `calibration`, `wall_load_peak` from this design's table, hands its own peak to `_oracle_levelized_replacement_cost(cost_per_event, q_n, …)`, drops `ash_frac` from `IN`, and returns `wall_peak_calibration` and `wall_load_peak` as channels. `oracle_entry.py` maps the seven new entry keys, drops `ash_frac`, and maps the two new channels.

## Cross-file bindings

| consumer | input | source |
|---|---|---|
| `wall_load_calc` (generic) | `p_fus`, `wall_area` | `fusion.p_fus`, `rb.wall_area` |
| `wall_peak_cal` (generic) | six refs + direct term | plant attributes, bound per concept |
| `wall_peak_calc` (generic) | `wall_load`, `calibration_in` | `wall_load_calc.wall_load`, `wall_peak_cal.calibration` |
| `cas72_calc` (generic) | `q_n_in` | `wall_peak_calc.wall_load_peak` (was `p_fus`, `ash_frac`, `rb.wall_area`) |
| `wall_load_ok` (instance) | `wall_load` | `wall_peak_calc.wall_load_peak` (was `wall_load_calc.wall_load`) |
| `neutron_wall_load` (instance) | — | `wall_load_calc.wall_load`, unchanged |

Dataflow stays unidirectional: geometry and fusion → average → peak → fence and lifetime. No new imports (`mfe_plasma_scaling` is already imported by both plants).

## Expected baseline behaviour

Derived in the round-2 session's scratch run from the recorded baseline (`evidence/T-003_baseline_result.json`) and the calc's own equations; every number below is a prediction the implementation checks, not a target it fits.

| quantity | today | after | why |
|---|---|---|---|
| `neutron_wall_load` (average) | 3.105376639 | 3.105376639 | untouched |
| `wall_peak_calibration` | — | 1.316440857 | 4.05 × 701.9262650 / (2700 × 0.7998) |
| `neutron_wall_load_peak` | — | 4.088044684 | 3.105376639 × 1.316440857 = 4.05 × 2725.363 / 2700 |
| `wall_load_ok` | satisfied | **violated** | 4.088 > 4.05, by the 0.94 % fusion-power excess |
| CAS72 core life | 5.796 FPY, 4 replacements | 4.403 FPY, 5 replacements | 18 / 4.088 |
| `cas72_calc__cost` | 95,898,253 | 131,494,480 | +35,596,226 (+37.1 %); includes the 3.4 × 10⁻⁵ convention change of D2 |
| `lcoe_calc__lcoe` | 307.08712043 | up by ΔCAS72 / annual MWh | derived at implementation from the oracle's annual energy |
| every heating number, the other eight verdicts, all capital accounts | — | unchanged | nothing upstream of them moved |

**If anything else moves, it is a finding to derive, not a number to fit.**

## Validation plan

1. Parse and Levels 1–3 on the three changed library files and the two plants (done for the prototype: Level 1 clean).
2. Codegen through the pinned generator with `--smart-regen --preserve-handwritten`; confirm the two new modules appear, the lifetime wrapper's input schema changes to `q_n_in`, and the handwritten impl is preserved (then edited by hand).
3. Execute at the baseline; compare every row of the table above.
4. The design-point identity from channels: `neutron_wall_load_peak × wall_peak_p_fus_ref / p_fus = wall_peak_q_ref` (4.088044684 × 2700 / 2725.3631229 = 4.05), because the baseline geometry equals the reference geometry — SV row.
5. The oracle written from this design agrees at the baseline on the average, the calibration, the peak, CAS72 and LCOE.
6. Perturbation for independence: `wall_peak_q_ref` 4.05 → 4.50 alone moves the calibration, the peak, the fence margin, CAS72 and LCOE in both the model and the oracle; the average does not move.
7. Lifetime-by-peak reproduction: 18 / 4.05 = 4.44 FPY at the source's own point, inside the source's ~4–6 FPY — SV row.
8. `tests/models` and `tests/study` green; six fixtures re-derived by running the tool; the census re-derived from a live generation; the manifest's `wall_load_ok` expectation flipped with its derivation beside it.

## Risks

1. **The pinned codegen refuses the dormant arithmetic or the moved usage.** *Likelihood: low.* Same envelope as WI-039's chain. *Mitigation:* a `MECHANICAL_FAILURE` with a retry inside the cap; the form is not changed to dodge a tool.
2. **A missed reader of `ash_frac` or of the instance's deleted `wall_load_calc` becomes a silent zero.** *Mitigation:* grep before deleting; baseline parity is the backstop (the average is predicted bit-identical).
3. **The restatement is larger than budgeted.** Seven study definitions read the wall-load channel by name and keep working; their `wall_load_ok` verdicts and `cas72` values change meaning, which the restatement states rather than re-runs. Six fixtures re-derive mechanically.
4. **A fresh reviewer reads the six-fact calibration as a relabel of 1.316.** *Mitigation:* the identity SV; the decomposition and the external band in the instance doc.

## Prototype and validation report

**Prototype: PASS.** The two calc defs written into `models/library/analyses/mfe_plasma_scaling.sysml` (lines 257–339) and validated with `uv run agentic-mbse validate models` (SysIDE licence sourced).

- **Level 1 (syntax): 0 errors, 0 warnings across all 25 SysML files.**
- **Level 2 (structural): two new warnings, both expected** — `Unused calc def: 'Neutron Wall Load Peak Calibration'` and `Unused calc def: 'Neutron Wall Load Peak'`; nothing consumes them until implementation. The 12 other Level-2 issues are the pre-existing placeholder literal bindings in `mfe_plant.sysml`, untouched.
- Levels 3–6 are implementation gates (the runner stops at Level 2's first failure).

**What the prototype confirms.** The intermediate attributes and the additive direct term parse; every input is a bare formal; the defaulted formals are declared last.

**What it does not confirm**, and implementation must: codegen generating the two modules and re-shaping the lifetime wrapper; the baseline table; the oracle's independent agreement; the perturbation.

**Files created:** none. **Files modified:** `models/library/analyses/mfe_plasma_scaling.sysml` (prototype; not yet copied to the twin).

## Approval

Settled by the round agent under goal `wall-and-heating`, which reserved no gates and ruled the fence's form the round agent's on sourced evidence `[OWNER 2026-09-03, ruling 5]`. D1 and D2 are the load-bearing judgments; D2 carries a real cost (a manual-stage interface change and one retired entry point), and its rejected alternative is written above so the round review can challenge it by re-derivation.
