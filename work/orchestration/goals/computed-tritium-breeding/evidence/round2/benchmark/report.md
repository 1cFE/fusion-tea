# OKTAVIAN approximate integral benchmark

[AGENT] 2026-09-18. Both baseline transport reconstructions are consistent with the revised experimental totals within one reported experimental standard deviation. This supports the Li reaction tally and lead-multiplier transport chain in an approximate spherical assembly. It does not validate the conceptual plant geometry or bound its physical uncertainty. Exact experimental containment, access holes and source characteristics remain unreconstructed.

## Evidence and reconstruction

The original primary proceedings source is `knowledge/sources/iaea_indc_nds_281_original_neutron_multiplication_benchmark/`, SHA256 `6df35c07b049385d326f0a71cee069b464d9a4b848cc6ad7717fb4be8616a2c0`. I visually inspected PDF pp.89–92 (printed pp.87–90): natural metallic lithium, 60 cm outer radius, 10 cm central source void, either Li from radius 10–60 cm or Pb from 10–20 cm followed by Li from 20–60 cm. Printed p.88 explicitly names a stainless-steel vessel. Figure 1, retained as `source-figure-p90.png`, shows source/beam and 45-degree access paths, but lacks sufficient dimensions for a complete reconstruction. A full concentric sphere is the declared approximation.

The revised measurements are Table 1.1 of `knowledge/sources/iaea_oktavian_tritium_breeding_benchmark_1994_text_rendering/`: Li TBR 0.685, relative standard deviation 5.6%; PbLi 0.530, relative standard deviation 6.0%. Original text URL: https://www-nds.iaea.org/fendl2/validation/benchmarks/jaerim94014/oktavian/tbr/readme.txt . Its Li/PbLi results use lithium-carbonate pellets; integration of measured local rates was assisted by the theoretical spatial distribution. They are not wholly model-independent integral calorimetric measurements. The more model-dependent TLD conversion and covariance procedure applies to other listed assemblies, not these two primary comparisons. Source-strength normalization contributes a shared systematic uncertainty, so the two tests are not statistically independent. The original proceedings' preliminary 0.73 and 0.62 (printed p.88) are not used as the revised targets.

`preexecution.md` records geometry, baseline assumptions, comparisons and sensitivities before results. There was no post-result adjustment. Room-temperature Li density 0.534 g/cm³ and Li6 atomic fraction 0.0759 subsequently received independent support from `knowledge/sources/compendium_of_material_composition_data_for_radiation/`, PNNL Rev.2 card 192, PDF p.161/printed p.144 (visually checked by materials reader). The Pb baseline used 11.34 g/cm³; the PNNL card 189 gives 11.35 g/cm³. The 0.088% density difference remains disclosed; neither value establishes the experimental sample's density. Casing material, thickness and source energy remain reconstruction assumptions.

## Execution and comparison

`run_benchmarks.py` ran OpenMC 0.15.2 with the isolated runtime's ENDF/B-VIII.0 processed data, fixed source, 294 K material temperature, 40 batches × 10,000 histories per case. Eighteen cases completed, totaling 7.2 million histories. The default source is an isotropic 14.1 MeV point at the centre. The exterior boundary at 60 cm is vacuum; this is valid for the isolated convex sphere because an outward trajectory cannot re-enter it through empty space. Tritium `(n,Xt)` is scored in lithium, by Li6, Li7 and total, per source neutron. No non-lithium tritium is credited.

| Assembly | Calculated TBR | MC standard error | Experiment ± standard deviation | C/E | Difference / combined σ |
|---|---:|---:|---:|---:|---:|
| Li baseline | 0.697859 | 0.000489 | 0.685 ± 0.03836 | 1.0188 | +0.335 |
| PbLi baseline | 0.504131 | 0.000478 | 0.530 ± 0.03180 | 0.9512 | −0.813 |

The last column combines only experimental standard deviation and Monte Carlo standard error by root sum square. It does not turn unsourced reconstruction choices into a probabilistic uncertainty. Baseline residuals are +0.012859 and −0.025869 T/source respectively. The independent-seed repeats differ by 0.622 and 0.189 combined Monte Carlo standard deviations. Li6+Li7 agrees with total to floating-point precision; details and data hashes are in `checks.json`. The analytical lithium volumes are 900,589.894 cm³ and 871,268.363 cm³. Runs completed successfully without a transport abort; stdout was suppressed by the runner, so this evidence does not separately certify absence of nonfatal runtime warnings.

## Predeclared sensitivities retained

| Variation | Li TBR | PbLi TBR |
|---|---:|---:|
| Independent seed | 0.698290 | 0.503997 |
| Source 14.0 MeV | 0.699104 | 0.504048 |
| Source 14.8 MeV | 0.688730 | 0.502756 |
| Li density 0.50 g/cm³ | 0.654389 | 0.464394 |
| Li density 0.56 g/cm³ | 0.731549 | 0.535145 |
| Li6 atom fraction 0.074 | 0.696462 | 0.498770 |
| Li6 atom fraction 0.080 | 0.700882 | 0.515456 |
| Illustrative 0.2 cm casing at inner/outer lithium boundaries | 0.691945 | 0.507837 |

The low-density PbLi case has C/E 0.8762 and −2.063 combined standard deviations: it fails the predeclared two-standard-deviation consistency diagnostic. It is preserved as an adverse material sensitivity, not used to replace the baseline. All other declared cases pass that diagnostic. The sampled ranges, 0.654389–0.731549 and 0.464394–0.535145, are scenario spreads; they are neither confidence intervals nor bounds on experimental reconstruction error. Casing uses declared Fe/Cr/Ni mass fractions 70/19/11% at 8 g/cm³ and displaces lithium; it is not an exact stainless vessel card.

## Acceptance scope and remaining gaps

[AGENT] Accept this as a limited independent integral check of the transport implementation. Retain the 4.9% low PbLi baseline residual rather than rescaling reaction rates. The source's older nuclear-data comparison itself varies with library (printed p.89); the present run uses one library, so no modern nuclear-data uncertainty has been quantified.

[AGENT] Exact experimental density, impurity/isotope assays, vessel thickness and composition, source target/beam structure, access-hole dimensions, and angular/energy source distributions remain missing. Angular anisotropy alone does not affect the concentric-sphere integral, but its coupling to missing openings may matter. Source-direction and opening biases are unquantified. No graphite case was added without validating its thermal-scattering treatment. The tests do not validate LiPb alloy composition, enriched lithium, helium/steel mixtures, toroidal leakage, stellarator shape, or port placement. Those require the separate plant sensitivities and method review. Agreement must not be reused as calibration or a blanket uncertainty bound.

Reproduction from repository root: `work/orchestration/goals/computed-tritium-breeding/evidence/round2/runtime/run work/orchestration/goals/computed-tritium-breeding/evidence/round2/benchmark/run_benchmarks.py`; then run `summarize.py` through the same launcher. `results.json` preserves all cases, `execution.log` the numerical receipts, and each `runs/<case>/` retains its model XML, statepoint, summary and hashes. Existing result files are reused; remove a selected case's result file only when intentionally rerunning that case in a separate reviewed workflow.
