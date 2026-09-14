# Fresh administrator synthesis

Administrator: `/root/transfer_administrator`, fresh native study administrator. Date: 2026-09-13 local session date. Frozen record read: `fa195fa4`. SHA256 of the committed [snapshot.json](snapshot.json): `2b1c664cec6543fd52117388f704732d4d6c634c372a9bc154664c883e3b59cb`.

Evidence access was confined to this record directory. Instruction and launcher files were read only to follow the administrator procedure. Calculations below read committed bytes; no model or oracle was rerun. Recorded facts and this administrator's interpretations are distinguished below.

## What the study set out to do

[OWNER-VERBATIM, as captured] “Within a documented geometry and conductor-technology range, do magnet sizing, operating limits, and component costs respond consistently enough to support a defensible design-point transfer?” The recorded order was “WI-040 first, then WI-038”. The executor translated that question into one conditional sensitivity arm with four causal levers, holding reference winding-pack current density, composition, temperature, coil configuration factors and unit economics fixed. This narrower executable interpretation is agent-originated. [record.md §2](record.md), [protocol.md](protocol.md).

The engineered grid contains 108 combinations: major radius 11.43/12.7/13.97 m, minor radius 1.17/1.3/1.43 m, coil current 14/15.4/17 MA and selected field envelope 20/24.9/27.5/30 T. The complete oracle scan retained every candidate without a mask. Numerical evaluability and the stated radial non-self-intersection inequality do not establish a source-qualified geometry range. The record reports native CLI execution, no adapter or supplied model quantities, one executable lineage, and no era pin. [snapshot.json](snapshot.json), [results/window-decision.json](results/window-decision.json), [record.md §§9–12](record.md).

## What it found

**Administrator's reading:** the record supports consistent conditional propagation through the implemented magnet sizing, operating screens and component accounts. It does not establish engineering-qualified design transfer. This distinction follows from both the retained numerical evidence and the specific missing geometry, conductor and manufacturing evidence. [results/cases.json](results/cases.json), [context/transfer-evidence-assessment.md](context/transfer-evidence-assessment.md).

All 108 cases completed. The objective `stellarator_09__stellaris__lcoe_calc__lcoe` spans 123.634303490505–244.9761615585503 dollars/MWh, including rejected cases. Five cases satisfy all modeled predicates, with LCOE 137.24935736588782–144.3092847210595 dollars/MWh. The pinned baseline is 142.50725862880648 dollars/MWh and violates the divertor-heat predicate. These are sampled results, not optima. [results/cases.json](results/cases.json), [results/summary.json](results/summary.json), [results/baseline_result.json](results/baseline_result.json).

The five fully satisfied cases are recoverable without outside evidence:

| Case suffix | R (m) | a (m) | Current (MA) | Selected envelope (T) |
|---|---:|---:|---:|---:|
| c0014 | 11.43 | 1.3 | 14 | 27.5 |
| c0015 | 11.43 | 1.3 | 14 | 30 |
| c0019 | 11.43 | 1.3 | 15.4 | 30 |
| c0058 | 12.7 | 1.3 | 17 | 27.5 |
| c0059 | 12.7 | 1.3 | 17 | 30 |

Every case uses the prefix `20260913-magnet-design-transfer:`. All five selected envelopes exceed the approximately 24 T endpoint reported for the inspected 20 K measurements. Even the 24.9 T normalization point is extrapolated. [results/cases.json](results/cases.json), [context/WI038-basis.md](context/WI038-basis.md).

**Independent record checks:** I recomputed all 17,388 native-versus-retained-oracle scalar comparisons and all 1,944 retained verdict comparisons. The largest relative scalar deviation is 3.0938283708360177e-13, matching the record. Every case contains 177 numeric outputs; the oracle comparison covers 161, leaving the explicitly listed sixteen outside that map. I joined all 108 output sets to their raw native artifacts and checked all CSV output/verdict values against the cases. All 128 result-artifact digests and 53 context-file digests matched. These checks verify relationships among frozen artifacts, not the physical validity of shared equations. The separate generic verifier records 25 channels and eighteen re-derived predicates across all cases. [results/exhaustive-oracle.json](results/exhaustive-oracle.json), [results/verification_summary.json](results/verification_summary.json), [results/cases.json](results/cases.json), [results/points.csv](results/points.csv), [context-digests.json](context-digests.json).

**Reference reconciliation:** at the reference, the quantity factor is 1, effective density is 118.8271604938272 A/mm², pack side is 0.36 m and pack volume is 136.56 m³. The selected pack account is $804.000000 million tape + $15.954709 million external materials + $750.415092 million winding operations = $1,570.369801 million. Adding $54.432000 million casing gives $1,624.801801 million selected magnet capital. I checked these additive relations throughout the grid. The $5,346.6 million legacy winding account and $6,323.469946 million older magnet comparison remain distinct comparison channels; they are not additional selected costs. Equality of the conductor normalization at q=1 is by construction and does not validate the inherited tape price. [results/baseline_result.json](results/baseline_result.json), [results/cases.json](results/cases.json), [context/WI040-design.md](context/WI040-design.md), [context/WI038-basis.md](context/WI038-basis.md).

**Demand versus capacity:** actual peak field is operating demand; the selected envelope is purchased capacity. I checked that the peak-field verdict agrees with demand ≤ capacity at every point. Across all 27 matched envelope groups, increasing capacity from 20 to 30 T leaves actual peak field unchanged and increases pack volume by `(30/20)^0.6`, or 27.542%. Winding operations remain exactly unchanged. This follows the recorded conductor-length estimate, while larger-cross-section manufacturing effort remains unpriced. [results/cases.json](results/cases.json), [protocol.md](protocol.md), [context/WI038-basis.md](context/WI038-basis.md), [context/WI040-design.md](context/WI040-design.md).

## The framing verdict per axis

All four axes were proposed as sensitivity and retained that framing after execution. I agree with that reading: observed grid responses locate outcomes, but do not resolve continuous boundaries or establish a design recommendation. All indicators say `constraints_reachable`; none says `no_constraint_response`, none was declined, and none required the conditional owner ruling. The indicator establishes possible paths only. [record.md §§5–8](record.md), [indicators.json](indicators.json).

| Axis | Proposed → judged | Recorded matched endpoint response and interpretation |
|---|---|---|
| R | sensitivity → sensitivity | Pack volume/procurement/operations rise 22.222%; side stays fixed; actual peak field and stress fall about 23.2–23.8%. Magnet capital rises about 20.5–21.0%; LCOE rises 4.048–53.548%. Plant interactions contribute to LCOE. |
| a | sensitivity → sensitivity | Pack sizing/procurement stay fixed; actual field and stress rise 2.432–3.190%; casing raises magnet capital 0.328–0.582%. LCOE falls 14.135–35.217% on these endpoint pairs. |
| I_coil | sensitivity → sensitivity | Volume, tape procurement and operations rise 21.429%; side rises 10.195%; stress rises 33.808%. LCOE response ranges from −28.984% to +5.715%, showing dependence on the other axes. |
| B_max | sensitivity → sensitivity | Volume and material/tape procurement rise 27.542%; side rises 12.935%; stress/strain fall 11.453%. Fixed operations temper selected pack cost growth to 13.476%; LCOE rises 2.371–3.882%. Actual field, stored energy, casing mass and ungraded comparison costs stay fixed. |

These are finite endpoint comparisons, not continuous monotonicity claims. Joint violation coordinates are retained in the CSV, and per-value counts in the summary do not isolate causal attribution. [results/summary.json](results/summary.json), [results/points.csv](results/points.csv).

## The constraint structure

I independently recounted the following populations from the committed cases. Each row carries the qualified identity and source-local identity. There are five aggregate-satisfied and 103 aggregate-violated cases, with no indeterminate verdicts. [results/cases.json](results/cases.json), [context/constraint_catalog.json](context/constraint_catalog.json).

| constraint_id | source_local_identity | Satisfied / violated |
|---|---|---:|
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | beta_ok | 108 / 0 |
| `stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58` | burn_hold_ok | 80 / 28 |
| `stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60` | cond_strain_ok | 108 / 0 |
| `stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3` | cycle_domain_ok | 108 / 0 |
| `stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7` | divertor_heat_ok | 48 / 60 |
| `stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7` | heating_couple_positive_ok | 108 / 0 |
| `stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650` | heating_couple_upper_ok | 108 / 0 |
| `stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5` | heating_source_positive_ok | 108 / 0 |
| `stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f` | heating_source_upper_ok | 108 / 0 |
| `stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852` | loop_capacity_ok | 64 / 44 |
| `stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945` | loop_pressure_ok | 108 / 0 |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | net_positive | 108 / 0 |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | peak_field_ok | 60 / 48 |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | recirc_ok | 104 / 4 |
| `stellarator_09__stellaris__sustainment_ok__77add152ed8eafce` | sustainment_ok | 56 / 52 |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | tbr_ok | 108 / 0 |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | wall_load_ok | 72 / 36 |
| `stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0` | wp_stress_ok | 92 / 16 |

The envelope reduces peak-field violations from 25 of 27 matched points at 20 T to three at 30 T, and stress violations from seven to three. Other plant limitations persist. Satisfaction of these predicates does not establish conductor operating margin, casing fit, manufacturing adequacy or the validity of held coolant and structural premises. [results/summary.json](results/summary.json), [record.md §4](record.md).

## Findings carried forward

All three findings are recorded as model findings. Their dispositions and routed homes are recoverable from the record; no discovery-log access or new disposition is needed for this reading. [record.md §15](record.md).

- `20260913-magnet-design-transfer#1`: conditional relative-grade and geometry responses agree across the grid, with only five fully satisfied cases. Recorded disposition: retain conditional transfer evidence without a recommendation or optimum. Its assessment home is copied as [context/transfer-evidence-assessment.md](context/transfer-evidence-assessment.md).
- `20260913-magnet-design-transfer#2`: increasing envelope increases material/tape quantities by 27.542% while all 27 matched winding-operation charges remain fixed. Recorded disposition: retain the length-only limitation and unpriced cross-section effort. Its design home is copied as [context/WI040-design.md](context/WI040-design.md).
- `20260913-magnet-design-transfer#3`: every fully satisfied case relies on extrapolated selected capacity; predicate passes do not establish operating margin, fit or complete non-overlapping manufacturing cost. Recorded disposition: retain extrapolation, fabricated-steel price ambiguity, missing insulation/cabling and NOAK price limits. Its basis/design homes are copied as [context/WI038-basis.md](context/WI038-basis.md) and [context/WI040-design.md](context/WI040-design.md).

## What the record does not support

**Record-contract assessment:** no material defect found. Intent, proposed and judged framing, objective, all qualified constraint populations, findings, verification scope and engineering limits are recoverable inside the directory. The absent evidence below is explicitly disclosed; it cannot be supplied by this reading. [record.md §17](record.md).

- Independent physical or source validation: the directory contains inherited source/accounting summaries and exact locators, not complete original PDFs or vendor sites. I can recover what those summaries report, including corrected 35/12/36/8% external-material fractions and 9% residual tape, but cannot freshly authenticate the original images or measurements here. Numerical agreement verifies implemented arithmetic against retained oracle arithmetic. [context/WI038-basis.md](context/WI038-basis.md), [context/WI040-design.md](context/WI040-design.md).
- A qualified geometry or conductor range: configuration-specific geometry coefficients/spacing, installed absolute current margin, angle/strain degradation, and a supported exponent fit interval are absent. Fixed 20 K reference scaling and extrapolated envelopes cannot supply them. [context/transfer-evidence-assessment.md](context/transfer-evidence-assessment.md), [context/WI038-basis.md](context/WI038-basis.md).
- Buildable pack/casing geometry or complete structural adequacy: anchored casing and stress estimates do not establish fit or detailed support performance. [context/transfer-evidence-assessment.md](context/transfer-evidence-assessment.md).
- A complete factory cost or proof of zero overlap: tape is purchased as composite tape, while the four material accounts cover external fractions. That accounting boundary is explicit. It does not resolve fabricated-steel price wording, the transferred winding-rate/nonplanarity assumptions, fixed cable additions, insulation, larger-cross-section effort, the aggressive NOAK tape target, solder/bulk procurement proxies, helium ideal-gas limits or inconsistent plant price years. [context/WI040-design.md](context/WI040-design.md), [context/transfer-evidence-assessment.md](context/transfer-evidence-assessment.md).
- Oracle coverage of all 177 outputs: sixteen remain outside the general map. Recorded algebraic identities cover some relationships without converting every omission into independent oracle coverage. [results/exhaustive-oracle.json](results/exhaustive-oracle.json), [results/identity-checks.json](results/identity-checks.json).
- Standalone model reproduction, a continuous feasible boundary, an optimum, or goal closure: the full executable runtime is not contained here, sampled extrema do not resolve a search, and the administrator has no owner-close authority. [snapshot.json](snapshot.json), [record.md §§5,17](record.md).
