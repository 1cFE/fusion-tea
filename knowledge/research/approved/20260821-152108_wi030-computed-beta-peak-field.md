---
date: 2026-08-21
researcher: Claude (agentic)
topic: wi030-computed-beta-peak-field
tags: [MFE, stellarator, beta, conductor-limit, codegen, study-tooling, WI-030]
research_type: model
---

# WI-030 design research: computed beta and the conductor peak-field limit

**Hold-out compliance.** `knowledge/holdout/aries-cs/PROTOCOL.md` read in full; no barred path (§ 3) was opened. Sources used: the Stellaris Table 2 / Table 5 / Fig. 16 images under `09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/`, the extracted text of the same paper, 1costingFE at `/home/reid/1cfe/1costingfe` (pin `0254385`), sysml-codegen at the pin `8a758e92` (fusion-tea's installed package), the current `models/` tree, and the study tooling under `scripts/study/`.

## Research Question

What does the design of WI-030 (`work/completed/20260822_WI-030_computed-beta-peak-field/spec.md`) need to know that the spec leaves open: the shape the pinned codegen and the study tooling admit for the peak-field constraint (risk R1), the helium/electron exponent choice (R2), the exact bound values and their arithmetic at the verdict boundary, the placement of the new attributes and asserts, and what the regeneration touches (R3, R4).

## Summary

- **R1 splits in two, and the second half fails.** The pinned codegen compiles `B_axis * peak_ratio <= B_max` (spike: zero diagnostics, six catalog entries, margin expression carries the product). But fusion-tea's own study tools reject it: `scripts/study/indicators.py:450-473` and `scripts/study/verify.py:174-200` admit only `feature_ref` and `literal` operands and raise on `operator`. The spec's success criterion "preflight 6/6 and verify pass" cannot be met with arithmetic in the predicate without editing `scripts/study/`, which is out of scope. **Recommendation: a small library calc `'Conductor Peak Field'` (`B_peak = B_axis * peak_ratio`) and a plain comparison `B_peak <= B_max` — the `wall_load_ok` shape.** The spec's own fallback, but as a calc rather than a plant attribute, so the Level 2/6 offender list stays unchanged.
- **Two arithmetic traps in the spec's numbers.** (1) `peak_ratio = 2.7667` gives `9.0 × 2.7667 = 24.9003 > 24.9`: the design point reads **violated**. Bind the float64 value of 24.9/9.0, `2.7666666666666666`; then `9.0 × peak_ratio == 24.9` exactly and the margin is `0.0` as the spec expects (verified on the generated predicate). (2) The LTS check "B = 4.70 satisfied" is wrong by the same rounding: `4.70 × 24.9/9.0 = 13.0033 > 13.0`. The exact LTS ceiling is `13.0 × 9.0 / 24.9 = 4.6988 T`; use **4.69 T** (satisfied, margin +0.024) in SV-036 and Item 6.
- **Beta at Point A: 0.026834 (−2.8 % vs the printed 2.76 %)** with the electron exponent 0.596 from the printed vol-av/peak pair and helium on the fuel exponent 0.33. Point B with the same recipe (its own pair gives `alpha_n_e = 0.6366`): **0.028691 (+2.1 % vs 2.81 %)**. Both inside the ±3.5 % band; computed by the generated module in the spike, bit-identical to the closed form.
- **Exponent evidence.** The Fig. 16 density panel digitizes to `alpha_n,e = 0.62` (rms 0.03, 111 px), corroborating the pair-derived 0.596 independently. The helium curve cannot be digitized (dotted, 29 usable pixels, no fit). The fuel exponent 0.33 stays (WI-022). The other two defensible helium choices bracket the result: He on the electron exponent gives −3.3 % (band edge); He from volume quasineutrality (`alpha_He = 4.03`) gives −6.3 % (outside the band). Fig. 16's own electron and fuel curves are not quasineutral at the edge (electrons fall below D+T), so no exponent set reproduces every printed number at once; the pressure-weighted choice is what matters, and helium is 6 % of the pressure.
- **Standard beta form validated; 1costingFE's tokamak form is not the reference.** `beta = 2 μ0 Σ_s n_s0 T_s0 e_keV / (1 + α_n,s + α_T) / B²` reproduces the printed value within 3 %. 1costingFE's `compute_beta_N` (`tokamak.py:117-126`) uses `μ0 · n_e · (T_e + n_i_frac · T_i) / B²` — half the standard `2 μ0 p / B²` (its docstring's "reduces to 2μ0 n T / B²" reduction is the half-form). Cite it as a cross-check only, with the factor disclosed; at the Stellaris point the half-form would give 1.34 %, clearly not the printed 2.76 %.
- **Placement.** `peak_ratio` and `B_max` belong on the library `'Magnet System'` part def (`mfe_power_core.sysml:65-91`; AD-007 puts every concept-agnostic magnet parameter there), bound in the instance's `part :>> magnet {}` block; the assert sits at plant level beside `net_positive`/`recirc_ok` so every MFE instance gets the conductor check. Entry-point names are then `magnet__peak_ratio` / `magnet__B_max` (spike-confirmed), a one-line rename in Item 6's design table (`run-study-first-consumer/design.md:210-211` writes them bare).
- **Regeneration footprint (spike-measured).** Entry points 166 → 173 (−`beta`, +`n_e0`, `T_e0`, `n_He0`, `alpha_n_e`, `magnet__peak_ratio`, `magnet__B_max`, +library defaults `beta_calc__mu0`, `beta_calc__e_keV`); outputs 72 → 74 (`beta_calc__beta`, `peak_field_ok__…__evaluation`); the `beta` study axis and its known-answer fixture `tests/study/data/beta.expected.json` retire and need a replacement axis.

## Detailed Findings

### 1. The codegen admits the arithmetic predicate; the study tools do not

**Spike.** The 14 MFE files were materialized into a scratch tree with `tests/model_families.materialize_canonical_subset` and edited with the prototype below, then generated with the installed pin (`uv run sysml-codegen generate --models … --output … --package-name stellarator_tea --overwrite`, sysml-codegen 0.1.1 at `8a758e92`, the same `GenerationConfig` path `tests/models/test_model_family_spines.py:125-133` uses).

Prototype edits (the design should reproduce them, then change the constraint shape per § 2):

| file | edit |
|---|---|
| `analyses/mfe_plasma_scaling.sysml` | `calc def 'Volume-Averaged Beta'`: ten bound formals (`n_e0_in`, `T_e0_in`, `n_D0_in`, `n_T0_in`, `n_He0_in`, `T_i0_in`, `alpha_n_in`, `alpha_n_e_in`, `alpha_T_in`, `B_in`), then the two defaulted constants `mu0 = 1.25663706212e-6`, `e_keV = 1.602176634e-16` declared last (ledger rule D13); intermediates `p_e`, `p_fuel`, `p_He`, `p_avg`; `out attribute beta : Real = 2.0 * mu0 * p_avg / (B_in ** 2)` |
| `analyses/mfe_viability.sysml` | `constraint def 'Conductor Peak Field Limit'` with `B_axis * peak_ratio_in <= B_max_in` |
| `cost_structure/mfe_power_core.sysml` | `'Magnet System'` gains `attribute peak_ratio : Real;` and `attribute B_max : Real;` |
| `designs/generic_mfe/mfe_plant.sysml` | plant attributes `n_e0`, `T_e0`, `n_He0`, `alpha_n_e` (no defaults, like `n_e`); `calc beta_calc : 'Volume-Averaged Beta'` reading `magnet.B` (the `magnet_cost` idiom, `mfe_plant.sysml:282-289`); `assert constraint peak_field_ok` after `recirc_ok` with `in B_axis = magnet.B; in peak_ratio_in = magnet.peak_ratio; in B_max_in = magnet.B_max;` |
| `designs/stellarator_09/stellarator_plant.sysml` | `:>> peak_ratio = 2.7666666666666666; :>> B_max = 24.9;` in the magnet block; `:>> n_e0 = 5.06e20; :>> T_e0 = 15.40; :>> n_He0 = 0.56e20; :>> alpha_n_e = 0.596;` after `alpha_T`; the `attribute beta : Real = 0.0276 {…}` block deleted; `beta_ok` rewired `in beta_in = beta_calc.beta;` |

**Generation result:** exit 0, no readiness diagnostics, 61 modules, 173 parameters, 74 outputs, `constraint_catalog.concrete_entries` = 6 with `excluded_records` = 0. The new entry is `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` (the hash suffix is the catalog's; it will differ once the predicate shape changes). The generated predicate (`modules/constraints/predicates.py:99-101`) is `_cmp('<=', (B_axis * peak_ratio_in), B_max_in)` with `source_margin = _norm0(B_max_in - (B_axis * peak_ratio_in))`, i.e. `predicate_compiler.py:160-176` (ARITHMETIC_OPS) and `:260-281` (`margin_expression` compiling both sides through `_compile_numeric`) do what the Item 6 research said. `'Volume-Averaged Beta'` is `AUTO_IMPLEMENTED = True` (pure arithmetic; no handwritten rung). Chains into constraint `in` bindings (`magnet.B`, `magnet.peak_ratio`) are fine — the profile's chain block (`agentic_mbse/sysml/executable_profile.py:376-396`) applies to chains inside a predicate body, and explicitly names "bind it to a constraint formal in the usage" as the admitted form.

**Study tooling result.** Running `indicators.predicate_operands` on the spike contract: the five existing constraints parse; `peak_field_ok` raises `IndicatorError: unknown predicate operand kind 'operator'` (`scripts/study/indicators.py:469-472`, the docstring at `:453-454` states the restriction). `verify.py:193-197` (`derive_verdict`) raises the same way. Both are upstream of the spec's MR-WI030-5 validation (`preflight.py gates` 6/6, `verify.py` pass); `.project/active/stellarator-model-migration` holds `git diff -- scripts/study/` empty as a standing bar (`AFTER_MIGRATION_RECORD.md:114`), and Item 6 owns the run-study capability. So the arithmetic shape is admissible to codegen and inadmissible to this item.

### 2. The admissible shape: a calc output compared to a bound limit

`wall_load_ok` is the precedent (`stellarator_plant.sysml:855-858, 878-881`): a library calc forward-computes the quantity, the constraint def compares two plain formals. For the peak field:

- `calc def 'Conductor Peak Field'` in `mfe_plasma_scaling.sysml` (or `mfe_magnet_cost.sysml`, beside the only other consumer of `B`): `in B_axis_in`, `in peak_ratio_in`, `out B_peak = B_axis_in * peak_ratio_in`. Concept-agnostic; MR-4 doc cites the Table 2 image for the ratio's meaning (peak-on-winding / axis-averaged) and the 1costingFE `MagnetProperties.b_max` docstring (`defaults.py:597-603`, "peak field ceiling at the conductor") for the quantity being bounded.
- `constraint def 'Conductor Peak Field Limit'`: `in B_peak`, `in B_max_in`, predicate `B_peak <= B_max_in`.
- Plant: `calc peak_field_calc : 'Conductor Peak Field' { in B_axis_in = magnet.B; in peak_ratio_in = magnet.peak_ratio; }` and `assert constraint peak_field_ok { in B_peak = peak_field_calc.B_peak; in B_max_in = magnet.B_max; }`.

Consequences: the indicator tool then classifies `peak_field_ok` as computed-vs-bound with `magnet__B` reaching it through the module graph (the same mechanism that makes `wall_load_ok` reachable from the density keys), which is the honest reachability Item 6's study wants. The oracle binding for `B_peak` is a channel (`peak_field_calc__B_peak`), for `B_max_in` an input (`magnet__B_max`). One extra output channel (`peak_field_calc__B_peak`), 75 outputs total.

Why not the spec's literal fallback (a plant attribute `B_peak = magnet.B * peak_ratio`): a plant-level arithmetic attribute is exactly what the Level 2/6 offender list counts (the six pre-existing offenders are the plant-level capital rollups, `VALIDATION_MATRIX.md:59`); the spec requires zero introduced. The `:>> G = 78.95…` literal in the instance (`stellarator_plant.sysml:128-131`) records the related codegen rule: redefinition expressions are dropped, so the ratio cannot be written `:>> peak_ratio = 24.9 / 9.0` either.

### 3. Boundary arithmetic at the design point and the LTS arm

Float64 facts (checked both in plain Python and on the generated predicate):

| binding | product | verdict | margin |
|---|---|---|---|
| `peak_ratio = 2.7667` (spec literal), `B = 9.0`, `B_max = 24.9` | 24.9003 | **violated** | −3.0e-4 |
| `peak_ratio = 2.7666666666666666` (= `24.9/9.0`), `B = 9.0`, `B_max = 24.9` | 24.9 exactly | satisfied | 0.0 |
| same ratio, `B_max = 13.0`, `B = 9.0` | 24.9 | violated | −11.9 |
| same ratio, `B_max = 13.0`, `B = 4.70` | 13.0033 | **violated** | −3.3e-3 |
| same ratio, `B_max = 13.0`, `B = 4.69` | 12.9757 | satisfied | +0.0243 |

So: bind `2.7666666666666666` with a doc stating it is `24.9 / 9.0` in IEEE-754 double (the Table 2 image pair), and amend SV-036 / the spec's success criterion from `B = 4.70` to `B = 4.69` (exact ceiling 4.6988 T). The `_norm0` normalization in the compiled margin (`predicate_compiler.py:262-268`) is what makes the boundary read `0.0`, not `-0.0`. Beta at 4.69 T is 0.0988 (spec: "≈ 0.10"), `beta_ok` violated as intended.

### 4. Beta: values, species, and exponents

**Inputs (Table 5 image, `images/page_009_table_0.png`).** Point A: `n_e0 = 5.06e20`, `n_He0 = 0.56e20`, `n_D0 = n_T0 = 1.96e20`, `T_e0 = 15.40`, `T_i0 = 14.63`, vol-av `n_e = 3.17e20`, vol-av beta 2.76 %, `B_0 = 9.0`. Point B: `6.89e20`, `0.83e20`, `2.60e20` ×2, `12.25`, `11.64`, vol-av `n_e = 4.21e20`, beta 2.81 %. The extracted text's Table 5 (`stellaris-design-details.md:722-755`) is garbled (4.55 / 5.77 peak electron density, 24.60 ion temperature, 1.5 m minor radius): the image is the authority, as `SOURCE_INDEX.md:179-189` already records.

**Form.** With `n(ρ) = n0 (1−ρ²)^α_n`, `T(ρ) = T0 (1−ρ²)^α_T` and `dV/V = 2ρ dρ`, `⟨n T⟩ = n0 T0 / (1 + α_n + α_T)` (the `u = 1−ρ²` substitution in `mfe_plasma_scaling.sysml:142-143`). Thermal beta against the axis-averaged field: `beta = 2 μ0 e_keV Σ_s n_s0 T_s0 / (1 + α_n,s + α_T) / B²`, species {e, D, T, He}, ions at `T_i0`, electrons at `T_e0`. Tungsten (`n_W/n_e = 7.76e-6`, Table 5) is negligible.

**Exponents.**
- `α_T = 1.19` for all species: the Fig. 16 temperature panel digitizes to 1.19 for electrons (rms 0.021, 105 px), D and T alike (re-run of `work/completed/20260718_WI-022_predictive-confinement/prototype/digitize_fig16.py`). Spec A1 resolved: shared exponent, no separate electron value in the source.
- `α_n,e`: from the printed pair, `5.06 / 3.17 = 1.596 → 0.596`. Independent digitization of the Fig. 16 electron curve gives 0.62 (rms 0.030, 111 px). Bind 0.596 (a derivation from two printed numbers, reproducible by a reader) and cite the digitization as corroboration. Point B's pair gives 0.6366; the oracle's Point-B check overrides `alpha_n_e` with that value (the same recipe applied to Point B), which is why `alpha_n_e` must be an entry point.
- `α_n,fuel = 0.33` (WI-022, unchanged).
- `α_n,He`: the Fig. 16 helium curve is a red dotted line; red-pixel tracking recovers 29 pixels with no monotone profile, so no fit. The quasineutrality route (volume averages: `3.17 = 3.92/1.33 + 1.12/(1+α_He)` → `α_He = 4.03`) is internally consistent with the printed `⟨n_e⟩` but steep, and its beta (0.02587, −6.3 %) falls outside the spec's band. Sharing the fuel exponent (0.33) is the "ash follows the ions" reading and gives −2.8 %; sharing the electron exponent gives −3.3 %.

**Results (generated module, `mu0 = 1.25663706212e-6`, `e_keV = 1.602176634e-16`):**

| recipe (α_n,e / α_n,He) | Point A (printed 0.0276) | Point B, own α_n,e (printed 0.0281) | Point B, A's α_n,e |
|---|---|---|---|
| **0.596 / 0.33 (recommended)** | **0.026834 (−2.77 %)** | **0.028691 (+2.10 %)** | 0.028907 (+2.87 %) |
| 0.596 / 0.596 | 0.026680 (−3.33 %) | 0.028510 (+1.45 %) | 0.028719 (+2.22 %) |
| 0.62 / 0.33 | 0.026721 (−3.21 %) | 0.028691 (+2.10 %) | 0.028778 (+2.41 %) |
| 0.33 / 0.33 (all fuel) | 0.028302 (+2.54 %) | 0.028691 (+2.10 %) | 0.030495 (+8.53 %) |
| 0.596 / 4.03 (quasineutral) | 0.025873 (−6.26 %) | 0.027558 (−1.93 %) | 0.027774 (−1.16 %) |

The recommended recipe sits inside ±3.5 % at both points with the other helium choice (−3.3 %) as the recorded tolerance, which is the R2 disposition the spec asks for. A thermal-only beta slightly under the printed total is the expected sign: the paper models fast-particle pressure separately (Table 4 `f_p`, `stellaris-design-details.md:698-705`; "fast particle pressures are modeled", line 708) and the printed ⟨β⟩ is the equilibrium value.

**Constants.** `mu0 = 1.25663706212e-6` matches the model's existing default in `'Magnet Coil Cost'` (`mfe_magnet_cost.sysml:41`); 1costingFE carries `1.25663706127e-6` (`tokamak.py:37`, CODATA 2022), a 7e-10 relative difference. Use the model's value for internal consistency and disclose the upstream one. `e_keV = 1.602176634e-16` is exact (`tokamak.py:36,40`), and is the same constant behind `E_fus = 2.817e-12` (`physics.py:31`).

### 5. Sources and citations for every new value (MR-WI030-4)

| value | binding | Source / Ref |
|---|---|---|
| `n_e0 = 5.06e20` | instance | Table 5 image `page_009_table_0.png`, "Peak el. density", Point A |
| `T_e0 = 15.40` | instance | same image, "Peak el. temperature", Point A |
| `n_He0 = 0.56e20` | instance | same image, "Peak helium ash density", Point A |
| `alpha_n_e = 0.596` | instance | derived: same image, vol-av 3.17 / peak 5.06 → `1/(1+α) = 3.17/5.06`; corroborated by Fig. 16 digitization (`…pdf-9-0.png`, 0.62, rms 0.03) |
| `magnet.peak_ratio = 2.7666666666666666` | instance | Table 2 image `page_002_table_0.png`: 24.9 T peak conductor / 9.0 T axis-averaged; the literal is `24.9/9.0` in float64 (redefinition expressions are dropped by the pin) |
| `magnet.B_max = 24.9` | instance, **[OWNER 2026-08-21]** | Table 2 image "Peak conductor magnetic field strength"; doc discloses `defaults.py:611` REBCO engineering ceiling 23.0 T and the ruling |
| `mu0`, `e_keV` | library defaults | `mfe_magnet_cost.sysml:41` (same μ0); `tokamak.py:36-40` (exact SI `e`) |
| `beta = 0.0276` | doc cross-check only | Table 5 image "Vol. av. beta [%]" 2.76 (A), 2.81 (B) |

Item 6's Nb3Sn arm values (`B_max = 13.0`, `defaults.py:613`; `B ≤ 4.69`) stay in Item 6.

### 6. What regeneration touches (R3, R4)

- **Contract.** Parameters 166 → 173; `stellarator_09__stellaris__beta` gone; the six design attributes and two library defaults listed in the Summary present (names spike-confirmed, with the `magnet__` prefix for the two magnet facts). With the § 2 shape, outputs 72 → 75 (`beta_calc__beta`, `peak_field_calc__B_peak`, `peak_field_ok__<hash>__evaluation`). The `beta_ok` constraint id keeps its hash only if its predicate and bindings are unchanged in IR terms; the catalog fingerprint and both package fingerprints change regardless.
- **Census and twin.** `tests/models/data/mfe_census.json` is bound to the semantic fingerprint and lists entry points by type; recapture from the first clean package (the spine test's own rule, `test_model_family_spines.py:349-353`). `exploration/stellarator_e2e/models/` must be byte-identical to `models/` (`test_canonical_files_equal_the_family_twin_byte_for_byte`); edit once, copy, never hand-sync.
- **Study fixtures.** `tests/study/data/axes.known_answers.json` declares a `beta` axis (`stellarator_09__stellaris__beta`, "bound-vs-bound") and `beta.expected.json` is its known answer. The axis cannot survive; the design should name its replacement (a `B` axis on `magnet__B` is the natural successor: it now reaches `beta_ok` through `beta_calc` and `peak_field_ok` through `peak_field_calc`, and is what Item 6 sweeps). Re-derivation follows the migration's Phase 3 procedure (`stellarator-model-migration/plan.md:532`): `test_fixture_binding` fails first on the old fingerprint, by design.
- **Manifest.** `studies/manifest.json`: `recorded_provenance` fingerprints, `indicator_inputs` digest over the contract plus the five `inputs/*.json` and `pipelines/pipeline.yaml`, `baseline.verdicts` gains `peak_field_ok: satisfied`, `objective_catalog` gains `beta_calc__beta` (Item 6 D9 also wants `magnet_capital`, a data-only row Item 6 can add itself).
- **Oracle.** `verify_stellaris.py::compute` adds the beta closed form and `B_peak`; `oracle_entry.py::ORACLE_OUTPUT_TO_CHANNEL` maps `beta` → `…beta_calc__beta` and `B_peak` → `…peak_field_calc__B_peak`; `OPERAND_BINDINGS` gains the `peak_field_ok__<hash>` row (`B_peak` channel, `B_max_in` input `…magnet__B_max`) and `beta_ok`'s `beta_in` flips from `{"kind": "input", "key": …beta}` to `{"kind": "channel", "key": …beta_calc__beta}`. `run_stellaris_single.py::EXPECTED_VERDICTS` gains the sixth name.
- **Snapshot.** `stellarator.snapshot.json` recaptured (`capture_instance_graph_snapshot`, the spine test imports it).
- **Headline.** Beta is not in the cost or power chain and the new constraint is satisfied, so LCOE 275.264220, total capital 16,129,706,216.04, p_net 915.081088, q_eng 6.606662, rec_frac 0.151362 and magnet capital must reproduce to the cent (`AFTER_MIGRATION_RECORD.md:36-48`).

## Code/Model References

- `models/library/analyses/mfe_plasma_scaling.sysml:132-219` (profile forms, `u` substitution), `:221-256` (`'Neutron Wall Load'`, the calc-then-compare precedent)
- `models/library/analyses/mfe_viability.sysml:40-58` (`'Beta Limit'`), `:60-77` (`'Neutron Wall Load Limit'`)
- `models/library/cost_structure/mfe_power_core.sysml:65-91` (`'Magnet System'`; AD-007)
- `models/designs/generic_mfe/mfe_plant.sysml:160-194` (profile attributes and `calc fusion`), `:282-289` (`magnet_cost` reads `magnet.B`), `:792-799` (plant-level asserts)
- `models/designs/stellarator_09/stellarator_plant.sysml:90-148` (magnet block), `:385-447` (profile referents), `:826-834` (bound beta), `:855-858, 874-881` (`wall_load_calc`, asserts)
- `scripts/study/indicators.py:450-473`, `scripts/study/verify.py:127-200` (operand kinds admitted)
- `/home/reid/1cfe/sysml-codegen` at `8a758e92`: `generation/predicate_compiler.py:52, 160-176, 260-281`; `agentic_mbse/sysml/executable_profile.py:331-334, 376-396`
- `/home/reid/1cfe/1costingfe/src/costingfe/defaults.py:596-619` (`MAGNET_TABLE`), `layers/tokamak.py:36-40, 117-126` (constants; half-form beta_N)
- `tests/model_families.py:111-120`, `tests/models/test_model_family_spines.py:125-133, 349-353`
- `exploration/stellarator_e2e/studies/oracle_entry.py:120-160`, `verify_stellaris.py:168-203`, `run_stellaris_single.py:33-39`
- Images: `…/images/page_002_table_0.png` (Table 2), `page_009_table_0.png` (Table 5), `stellaris-high-field-quasi-isodynamic-stellarator.pdf-9-0.png` / `-9-1.png` (Fig. 16 density / temperature)

## Architecture/Modeling Insights

- **"Admitted by codegen" and "admitted by the study route" are two gates.** The catalog profile is wider than the tools that read it. Any predicate shape beyond `leaf <op> leaf` needs either the calc-then-compare rewrite or a study-tooling change. Worth a sentence in the run-study skill or the policy; not this item's job.
- **Calc-then-compare is the reachability-friendly shape anyway.** A lever reaches a constraint only through module-graph edges; arithmetic inside a predicate hides the dependency from the indicator tool even where the tool could parse it.
- **Boundary-exact verdicts need boundary-exact literals.** When an owner binds a limit equal to the design value, the bound geometry fact must be the float64 quotient, not a 5-digit rounding. The doc should say so where the literal lives.
- **Thermal beta from the source's own peaks lands 2–3 % under the printed equilibrium beta.** That sign is physics (fast-particle pressure excluded), not error; the tolerance band should keep carrying the reason.

## Feasibility Assessment

Feasible within the codegen envelope and with `scripts/study/` untouched, using the § 2 shape. Every executable expression is `+ − × ÷ **`; defaults declared last; no function invocation; the beta calc auto-implements (no handwritten rung, no impl sha to guard beyond the existing two). Prerequisite unchanged from the spec: the stellarator-model-migration certification (SC2, SC11 open) since this item regenerates on the same pin. No owner ruling is newly required; two spec corrections are (below).

## Recommendations

1. **Constraint shape:** `'Conductor Peak Field'` calc + plain `B_peak <= B_max_in` comparison (§ 2). Record the arithmetic-predicate form as the rejected alternative with the `indicators.py:469` reason.
2. **Literals:** `peak_ratio = 2.7666666666666666`; SV-036 and the spec's LTS check at **`B = 4.69`** (exact ceiling 4.6988 T). Both are spec amendments the design should make explicit and the owner should see.
3. **Exponents:** `alpha_n_e = 0.596` (pair-derived, digitization-corroborated), helium on the fuel exponent; record −3.3 % (helium on the electron exponent) as the tolerance. Point-B verification overrides `alpha_n_e = 0.6366` by the same recipe.
4. **Placement:** `peak_ratio`, `B_max` on `'Magnet System'`; `peak_field_calc` and `peak_field_ok` in `mfe_plant.sysml`; `beta_calc` and the four electron/helium attributes in `mfe_plant.sysml`; `beta_ok` stays in the instance, rewired. Tell Item 6 the two keys carry the `magnet__` prefix.
5. **Study axis:** replace the retired `beta` axis with a `B` axis (`magnet__B`) in `axes.known_answers.json` and its known answer.
6. **Beta doc:** cite 1costingFE's `compute_beta_N` only as a cross-check with its factor-of-two disclosed; the Basis is the standard `2 μ0 ⟨p⟩ / B²` validated against the printed 2.76 %.

## Open Questions

- Whether the printed ⟨β⟩ includes the modeled fast-particle pressure (Table 4 `f_p = 0.2` is an assumption on alpha/total pressure; the text does not say whether Table 5's beta is thermal or total). Not needed to proceed; the ±3.5 % band covers it either way.
- The 1costingFE `compute_beta_N` half-form (`tokamak.py:117-126`) looks like an upstream defect in the tokamak path. Outside this item (stellarator instance never calls it); worth a 1costingFE filing when the tokamak instantiation arrives.
- Whether the run-study capability should admit `operator` operands in `indicators.py`/`verify.py` in a later item, so future constraints can be written as one-line inequalities without a helper calc.
