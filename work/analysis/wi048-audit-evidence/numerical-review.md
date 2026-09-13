# WI-048 independent numerical and source review

[AGENT] Fresh read-only numerical/source inspection on 2026-09-10. Personally viewed both required source images. Read the six canonical changed SysML files, item spec/design and original F01–F03 report. No holdout material accessed. Independently recomputed the new baseline using `.codex-test/run python` and year-by-year discounted cash flows rather than importing an existing oracle. This report is evidence, not production remediation or owner acceptance.

## Findings and applicability

**Blocking MR-WI048-1 source-provenance gap:** `models/designs/hif_ife/hif_plant.sysml:131` still derives the retained alpha estimate from corrupted **2.054 GWt**. Alpha=2000 may remain an inherited estimate within the approved finance scope, but its current explanation presents the erroneous operating basis as valid. The adjacent $0.73B/$1.34B/$1340 derivation inherits that basis. This does not demonstrate a defect in the repaired executable power chain; it prevents certifying all affected current source claims as repaired.

**Related source locator gaps:** `hif_plant.sysml:47,69,123` cite Hawker “Table 1” for parameters. In `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md`, Table 1 at line 106 compares electricity generation technologies; parameter definitions are Table 2 at line 155; sampling ranges occur at lines 443–469. In particular the model's claim **“Table 1 (parameter d, default 0.08)”** at `hif_plant.sysml:123` is not established by that source locator. The actual discount range is 2–12% at source line 443. The retained 0.08 input can be identified as an inherited modeling choice without changing finance. Blanket=1.15 and target=$10 likewise remain selected assumptions rather than exact facts proven by the cited Table 1.

Discrepancy thresholds apply only to equivalent bases. Current thermal, gross, other-parasitic and net powers deliberately implement the accepted common Hawker operating balance, while historical Osiris facts are reference transcriptions. Their differences below are design-specific distinctions, not numerical FAIL verdicts. Monetary outputs also have different finance/year-dollar conventions. Numerical proximity to printed 5.6 does not validate either calculated price.

## Reference paths

| Alias | Path |
|---|---|
| H | `models/designs/hif_ife/hif_plant.sysml` |
| D | `models/designs/hif_ife/hif_driver.sysml` |
| E | `models/library/analyses/hif_economics.sysml` |
| L | `models/library/analyses/ife_lcoe.sysml` |
| P | `models/designs/generic_ife/ife_plant.sysml` |
| F | `models/library/analyses/fusion_cycle.sysml` |
| O | `knowledge/sources/energy_from_inertial_fusion/images/page_007_table_0.png` |
| M | `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md` |
| W | `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md` |

## Osiris transcription and computed distinctions

All thirteen historical literal rows match O exactly. Image row names are the source locators; an image has no text line numbers.

| Quantity | Current executable value | Historical Osiris value | Model location and distinction |
|---|---:|---:|---|
| Beam MJ | 5 | 5 | H:36; reference H:233; exact |
| Gain | 87 | 87 | H:94; reference H:234; exact |
| Yield MJ | 435 | 432 | L:60; reference H:235; +0.69444%, deliberately computed with rounded gain |
| Frequency Hz | 4.6 | 4.6 | H:85; reference H:236; exact |
| Driver efficiency | 0.28 | 28% | D:85; reference H:237; exact |
| Fusion MW | 2001 | 1987 | L:64; reference H:238; +0.70458%, gain/yield rounding |
| Thermal MW | 2301.15 | 2504 | L:65; reference H:239; −8.10104%, later blanket=1.15 |
| Thermal efficiency | 0.45 | 45% | H:105; reference H:240; exact |
| Gross electric MW | 1035.5175 | 1127 | L:67; reference H:241; −8.11735%, common computed balance |
| Driver electric MW | 82.142857142857 | 82 | L:68; reference H:242; +0.17422%, rounding |
| Other/auxiliary MW | 82.142857142857 | 45 | L:70; reference H:243; +82.53968%, Hawker cooling approximation |
| Net MW | 871.231785714286 | 1000 | L:71; reference H:244; −12.87682%, computed balance |
| COE | Hawker 240.666460639551 $/MWh; Meier 5.589991561584084 cents/kWh | 5.6 in 1992 cents/kWh | H:245 reference; different finance/dollar cases |

Historical rounding residuals: 5×87=435 versus printed 432; 432×4.6=1987.2 versus printed 1987; 2504×0.45=1126.8 versus 1127; 1127−82−45=1000 exactly. Both rounded gain and yield are preserved rather than imposing an exact identity between the printed numbers.

## Other quantitative inputs and constants

| Input/constant | Current value | Model and source evidence |
|---|---:|---|
| Chambers; reactor units | 1; 1 | H:37,164; scenario selections; parameter meanings M:184,134 |
| Availability | 0.90 | H:76; `knowledge/sources/accelerators_for_inertial_fusion_energy_production/output.md:672`; later assumption |
| Driver lifetime shots | 6e9 | D:88; same accelerator source :672; requirement at 5 Hz/40 yr/90%, retained fixed lifetime |
| Blanket multiplier | 1.15 | H:70; selected later Hawker value; W:386 gives 0.6–1.4 range, not exact 1.15 |
| Target cost | $10/shot | H:53; inherited generic assumption, not Osiris table fact; cited Table 1 wrong |
| Yield cost | $5e6/GJ | H:71; W:570 includes $5 M/GJ scenario; W:467 range $0.5–50 M/GJ |
| Plant cost alpha | $2000/kWe | H:128; explicitly estimated; W:445 range $1000–6000; stale 2.054 rationale H:131 |
| O&M epsilon | $65/kWe-year | H:143; adjusted estimate; M:101 supports 3% basis, not exact $65 |
| DCF discount | 0.08 | H:116; inherited choice; W:443 range 2–12%; Table 1 does not substantiate stated default |
| Construction/operation years | 5 / 40 | L:50–51; W:148 exact match |
| Shots year seconds | 31557600 | L:85; intentional retained Julian-year convention; W:332 uses 365 days=31536000 |
| Energy annual hours | 8760 | L:114; W:152 uses 365 days, matches |
| Target factory direct $B | 0.1 | H:165; M:166–167 matches |
| Driver coefficients | 0.32, 0.088, 1.25, 0.05, 0.0088, reference 5 Hz | E:33–35; personally verified `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/images/page_004_eq_0.png`; M:180 |
| Reactor coefficients | 0.66 $B, 1.67 GWt, exponent 0.49, unit factors 0.72/0.28 | E:63–64; M:122,131,136 |
| Total/direct multiplier | 1.83 | E:83; M:102,113 exact |
| Annual capital charge | 0.113 = 0.083+0.03 | E:109; M:99–102 exact |
| COE conversion | 0.0876 | E:110; M:78 exact |
| Economic heuristic | eta×gain ≥10 | F:46–48; separately identified heuristic |
| Generation threshold | net W >0 | F:60; strict derived rule, P:150 binds actual priced balance |
| Invalid sentinel and validity | price=0, generating=0 | L:143–149 documents contract; positive generation indicator=1 |

## Independent new-baseline arithmetic

The independent calculation used beam=5e6 J, efficiency=.28, gain=87, rate=4.6, availability=.9, the source-verified Meier procurement equation, and the retained finance assumptions. Hawker cost was evaluated as five discounted annual construction payments plus forty discounted annual operating payments, divided by the corresponding forty annual energy payments. This independently checks the closed-form discount factors. Displayed rounding should not be treated as extra model precision.

| Output | Recomputed value | Model formula |
|---|---:|---|
| Bank energy J | 17,857,142.857142854 | E:39–40 |
| Gamma $/J | 55.13324544000002 | E:42 |
| Driver direct capital $ | 984,522,240.0000001 | E:32; L:92 |
| Driver fraction | 0.079325416656751 | L:73 |
| Total fraction | 0.158650833313502 | L:74 |
| Annual shots | 130,648,464 | L:85 |
| Driver lifetime yr | 45.92476494786804 | L:89 |
| Annual driver replacement $ | 21,437,719.738306563 | L:93 |
| Hawker initial capital $ | 2,729,160,811.428571 | L:100–103 before division by construction years |
| Annual operating $ | 1,384,552,425.809735 | L:108–110 |
| Annual energy MWh | 6,868,791.398571427 | L:114 |
| Meier reactor direct $B | 0.7722641595500556 | E:63–64 |
| Meier total capital $B | 3.397919111176602 | E:83 |
| Hawker LCOE $/MWh | 240.666460639551 | Independent year-by-year sum |
| Meier COE cents/kWh | 5.589991561584084 | Independent M Eq.1 evaluation |

No old baseline was freshly recomputed in this bounded subtask. The original audit at `.project/reports/20260907-fusion-model-audit.md:70` reports old Hawker net 592.312 MW and independent Meier denominator 1000 MW; these are inherited historical evidence, not newly certified numerical results. The new computation above agrees with the design's prototype headline values. The parent audit owns comparison against generated execution and the implementation's old/new evidence.

## F02 and F03 structural checks

F02: authoritative beam/efficiency derives bank at E:39 and D:87. Plant frequency binds procurement rate at H:38. Generic LCOE consumes that bank/rate at P:121,123. Meier thermal/net values consume computed powers at H:161–162,176,206. The formerly disconnected identities are repaired in the canonical model structure. Beam 5→10 scales procurement exactly 1.5789473684210527 and bank/yield 2×. Efficiency .28→.35 scales bank demand 0.8× with beam/yield fixed. Rate 4.6→5 scales powers/shots 5/4.6 and procurement by 1/0.99648. These are algebraic dependency checks; generated mutation execution remains separate evidence.

F03: net positivity binds the actual LCOE balance; the driver-only compatibility alias is explicit at P:173–174. At eta=.1, gain=100, blanket=.6 and thermal efficiency=.3, the heuristic passes but cycle gain=1.8 and net=−0.2×bank×rate. The strict rule fails. Source W:369–376 explicitly describes the factor two as an arbitrary allowance for driver plus equal cooling power. The handwritten completion and public generated verdict checks belong to the parent's execution review; this subtask does not claim to have rerun them.
