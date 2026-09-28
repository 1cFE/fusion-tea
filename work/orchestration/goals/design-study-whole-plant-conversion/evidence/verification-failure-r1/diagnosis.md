# Verification failure: independent diagnosis

The review target is the [combined numerical repair proposal](../numerical-repair-r2-proposal.md). This document records the independent diagnosis and supporting experiments.

[AGENT] The failed 2,496-point record has 11 off-tolerance scalar comparisons in five cases. All 312,000 predicate derivations agree. The scan covers all 2,975,232 declared scalar comparisons using the unchanged stock verifier rules. There are no evaluation errors. Before/after hashes confirm that the native package, original receipts, proposals, manifest, and installed oracle files stayed unchanged. See [discrepancies.json](discrepancies.json), [case-checks.json](case-checks.json), and [channel-statistics.json](channel-statistics.json).

## Two distinct numerical causes

| Cases | Failed channels | Cause established by independent evidence |
|---|---|---|
| c2436–c2439, four cryogenic capacity brackets | `cold_margin_W` and `extra_cold_capacity_W` | Subtraction near zero amplifies native/independent binary64 rounding differences of 7.28e-12 to 1.46e-11 W. The margins are only about ±0.0030726 W. All signs and capacity predicates agree. |
| c1868, gas-favourable gas offer at 2,500 MW, flow 2,500 kg/s, stage ratio 1.8, service offer 40/40/60 | Precooler `min_gap`, `required_ua`, and `ua_residual` | The independent Brent outlet-temperature stop is too loose near the 0.000142318 K terminal gap. High-precision integration establishes that the native solve is more accurate. |

The cryogenic failures have relative deviations up to 4.736e-9 against the unchanged 1e-9 limit, with no declared absolute allowance. The precooler UA difference is 7.411e-8 MW/K. It exceeds both the relative limit for required UA and the existing 1e-8 MW/K absolute allowance for the UA residual. These are failed checks; their small physical effects do not waive the recorded acceptance rules.

## Independent precooler adjudication

[AGENT] An 80-digit Decimal reference integrates heat divided by the temperature gap over each retained piecewise-linear water enthalpy interval. It solves the outlet root to a bracket narrower than 1e-65 K. A repeat at 60 digits agrees within 4.23e-42 across the reported reference outputs. It imports no native calculation body. Native and oracle intermediate input maps at this component are identical. See [high_precision_cooler.py](high_precision_cooler.py) and [high-precision-cooler.json](high-precision-cooler.json).

| Quantity | High-precision reference | Native error | Original oracle error |
|---|---:|---:|---:|
| Water outlet, °C | 39.11820057461559871919686 | +2.20046e-14 K | −1.93909e-12 K |
| Minimum gap, K | 0.00014231813401648357743 | +7.32803e-16 K | +1.96183e-12 K |
| Required UA, MW/K | 60 | −2.84501e-11 MW/K | −7.41400e-8 MW/K |

Propagating the reference component outputs through the independent downstream equations changes gas net export by 2.84e-14 MW. The case remains at −38.9510768455 MW net export, with `economic_defined=0`, and the large conversion balance residual remains 2305.136979316 MW. Seven applicable gas predicates already exclude this offer. The failed point remains part of the declared catalog and must remain numerically verifiable.

## Proposed independent solver correction

[AGENT] Change only the independent cooler's Brent stopping precision from `xtol=1e-11, rtol=1e-14` to `xtol=math.nextafter(0.0, 1.0), rtol=4*math.ulp(1.0)`, retaining Brent's method, its independent water-temperature integral, property data, equations, and existing iteration limit. This resolves the root to the available binary64 precision rather than terminating at a temperature error that produces an excessive UA residual. It changes solver accuracy, not the study acceptance tolerances.

A diagnostic process temporarily applied these stopping arguments without editing the installed oracle. It found outlet 39.11820057461562 °C and independent UA residual −2.83507e-11 MW/K. All 1,192 scalar comparisons and 125 predicates for c1868 then pass the unchanged rules. The native cooler body needs no correction. See [brent_precision_probe.py](brent_precision_probe.py) and [brent-precision-probe.json](brent-precision-probe.json). This experiment is evidence for the proposed correction; it does not replace stock verification of a reviewed implementation.

## Proposed cryogenic bracket replacement

[AGENT] For the new record only, replace the four points at the retained independent capacity threshold ±1e-5 W/m³ with threshold ±0.01 W/m³. Retain the center 75.43260142820313 W/m³, both supported source loads, zero extra structural heat, the same selected hardware, and both branch aliases. The replacement heat inputs are 75.42260142820312 and 75.44260142820313 W/m³. The bracket width is 0.02 W/m³; it remains an engineering capacity diagnostic rather than a nuclear heating uncertainty interval.

| Offset from threshold, W/m³ | Approximate margin magnitude, W | Largest local native/independent relative difference across both affected outputs |
|---:|---:|---:|
| 0.00001, failed original | 0.0030726 | 4.736e-9 |
| 0.0001 | 0.030726 | 4.736e-10 |
| 0.001 | 0.30726 | 3.552e-11 |
| 0.01, recommended | 3.0726 | 4.736e-12 |

The recommended offset gives about 211 times the observed headroom against the unchanged relative limit. The local calculation preserves the passing lower side and failing upper side for both source loads. It reproduces the original recorded native margins when given the original points. These proposed points have not been executed natively. See [conditioning_probe.py](conditioning_probe.py) and [conditioning-probe.json](conditioning-probe.json).

## Review boundary

The combined proposal owns the exact edits and regression gates. This investigation changed no installed oracle, native body, generated package, manifest, study proposal, or acceptance tolerance. The diagnostic experiments have no repaired-study acceptance authority. The original failed record remains evidence.
