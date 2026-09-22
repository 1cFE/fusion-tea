# Conditional integrated ARIES design comparisons

[AGENT] The studies answer the bounded design question under the declared model assumptions. [Independent final review](evidence/final-review.md) passes and accepts the positive conditional goal. Formal goal closure remains owner-held.

Reducing both selected exchanger areas from 50,000 to 45,000 m² lowers modeled overnight capital by 17.381059 million USD2004 and default LCOE by 0.381913 USD2004/MWh. Calculated net electricity and gross tritium makeup remain unchanged. This small purchased-equipment saving survives all 21 tested one-at-a-time assumption settings in both supply scenarios. It does not establish exchanger geometry, hydraulics or a minimum adequate area.

The larger apparent benefit at lower density depends on assumed breeder supply. The near-threshold case produces less electricity and worsens no-credit LCOE, while feed100 eliminates external purchases. Its advantage reverses under several tested assumptions. It is not evidence of better physical efficiency, improved breeding or a qualified operating optimum.

## Paired candidate results

Every candidate is evaluated under no breeding credit (new feed 0; incremental service charge 0) and assumed net usable breeder feed of 100 kg/calendar year with a 30 million USD2004/year service charge. Internal exhaust recycling is already credited before the gross makeup requirement. Feed is new supply after extraction losses, not recycled exhaust; it is not multiplied by availability again. Neither feed nor service charge is optimized. Excess feed is curtailed without revenue.

The **423.106794 MW case remains the assumed integrated baseline**. All following representatives pass the evaluated checks under default assumptions; scientific qualification remains unsupported.

| Physical configuration | Supply | Net MW | Annual MWh | Gross T kg/calendar year | Assumed feed kg/year | External T kg/year | LCOE USD2004/MWh |
|---|---|---:|---:|---:|---:|---:|---:|
| Assumed integrated baseline | no-credit | 423.106794 | 3150453.189 | 104.667707 | 0 | 104.667707 | 1119.408083 |
| Assumed integrated baseline | feed100-service30m | 423.106794 | 3150453.189 | 104.667707 | 100 | 4.667707 | 176.686569 |
| Both exchangers 45,000 m² | no-credit | 423.106794 | 3150453.189 | 104.667707 | 0 | 104.667707 | 1119.026170 |
| Both exchangers 45,000 m² | feed100-service30m | 423.106794 | 3150453.189 | 104.667707 | 100 | 4.667707 | 176.304656 |
| 45,000 m² each; density 4.875e20 m⁻³ | no-credit | 349.596229 | 2603093.523 | 99.527499 | 0 | 99.527499 | 1295.085963 |
| 45,000 m² each; density 4.875e20 m⁻³ | feed100-service30m | 349.596229 | 2603093.523 | 99.527499 | 100 | 0.000000 | 159.581252 |
| 45,000 m² each; density 5.25e20 m⁻³ | no-credit | 575.711005 | 4286744.141 | 115.338520 | 0 | 115.338520 | 897.084346 |
| 45,000 m² each; density 5.25e20 m⁻³ | feed100-service30m | 575.711005 | 4286744.141 | 115.338520 | 100 | 15.338520 | 204.250834 |

[Complete candidate ledger](evidence/candidate-ledger.csv) reports all 266 study rows, including every candidate's net electricity, gross requirement, assumed feed, purchases, curtailment, service charge, selected exchanger inventory/UA/purchase cost, all eleven LCOE contributions and adverse verdicts. Its [provenance](evidence/candidate-ledger-provenance.json) points to native-derived accounting and frozen snapshots. Each study retains complete native inputs/outputs, not only this presentation subset.

## What caused the changes

The area-only reduction changes purchased quantity, UA and capital through the native graph. At the same density it changes neither accepted heat nor net electricity within the tested window. Its default LCOE reduction comprises 0.372200 from financed capital, 0.006059 from other-equipment overhaul and 0.004567 from gross terminal expense, partly offset by a 0.000913 smaller salvage credit. Pump demand does not change because the model has no area-dependent hydraulic relation. The price law is a provisional linear selected-quantity estimate, not a procurement quote.

At density 4.875e20 m⁻³ and reduced areas, gross makeup falls to 99.527499 kg/calendar year. Feed100 then requires no external purchases and curtails 0.472501 kg/year. Relative to the default baseline, net power falls by 73.510565 MW and the nonfuel/non-supply contribution subtotal rises by 25.337011 USD2004/MWh. The external-tritium contribution falls by 44.447958 while the fixed service charge costs an additional 2.002310 per MWh because less electricity is produced. The deuterium contribution increases by 0.003321 USD2004/MWh. The resulting 17.105317 price reduction is conditional fuel accounting, not a physical performance improvement.

At density 5.25e20 m⁻³, modeled net output increases at fixed hardware and no-credit LCOE falls. Gross tritium makeup increases too, and feed100 requires 15.338520 kg/year external purchases. This raises its default conditional LCOE despite more electricity. Confinement, controllability and actual operating capability are not qualified by this prescribed-density calculation.

## Assumption robustness

The final study compares each representative with the baseline under the **same** uncertainty setting and supply scenario. It uses ten OAT groups: separate He/PbLi U, neutron multiplication, helium deposition fraction, inter-coolant exchange, other electrical load, correlated HX price factors, availability, external T price and real discount rate. Exact units, full entry groups and engineered levels are in the [record](../../../../exploration/aries_integrated/studies/20260922-aries-integrated-design-robustness/record.md) and config. The two HX price factors share an explicitly chosen uncertainty multiplier; they are not the same physical equipment variable.

- The reduced-area design retains lower conditional LCOE in all 42 matched comparisons (21 settings × two supplies), with savings of 0.190957–0.636126 USD2004/MWh. Power and fuel remain unchanged at each matched setting.
- The near-feed-floor case is more expensive without breeding credit in every tested setting. Its feed100 advantage reverses at neutron multiplier 1.0, availability 0.75 and external T price 10 million USD2004/kg.
- The high-density case is cheaper without breeding credit in every tested setting. Its default feed100 disadvantage reverses at availability 0.75 and T price 10 million USD2004/kg.

These are bounded conditional responses, not probability distributions or joint-uncertainty robustness. External T price changes startup stock capital as well as recurring purchases. Availability changes annual electricity and fuel demand against a fixed calendar-year feed, so its rank reversals are partly supply-threshold effects. Discount and HX price factors have no modeled constraint response; their missing financing/credit and price/quality relationships were recorded before execution under the owner's sensitivity authorization. No unsupported efficiency assumption was optimized.

## Records, plots and preserved failures

| Study | Native cases | Pass all evaluated checks | Adverse cases | Freeze |
|---|---:|---:|---:|---|
| [Local response](../../../../exploration/aries_integrated/studies/20260922-aries-integrated-local-response/report.md) | 24 | 14 | 10 | a396a2e0 |
| [Coupled design](../../../../exploration/aries_integrated/studies/20260922-aries-integrated-coupled-design/report.md) | 68 | 58 | 10 | d976da47 |
| [Assumption robustness](../../../../exploration/aries_integrated/studies/20260922-aries-integrated-design-robustness/report.md) | 174 | 168 | 6 | d57ee5cd |

Across the three records, PNG/PDF plots show electricity, fuel, LCOE contributions and evaluated margins; each retains complete margin and verdict data. The [coupled grid](../../../../exploration/aries_integrated/studies/20260922-aries-integrated-coupled-design/plots/coupled-grid.png) separates the two supply scenarios and states its per-panel scales. Missing scientific qualification is explicit. All attempted native cases are retained; there were no evaluator retries or domain refusals in these three declared windows.

The helium/PbLi 5,000 m² controls fail heat removal and are outside the provisional cost-comparison window; they are diagnostic, not economical candidates. All three original source configurations retain heat-removal failures; literal Raffray also retains its balance failure. Their finite LCOEs do not make them acceptable designs. Separate negative-energy/financial refusals retained in the [predecessor lifecycle study](../aries-integrated-lcoe/answer.md) remain valid boundary evidence; they were not converted into successful rows or silently discarded.

## Source-conditioned reference and unmatched source values

The native financial-only reference substitutes supplied 1,000 MW and already-financed 5.055774 billion USD2004 capital, with second construction financing guarded at zero. Its baseline LCOE is 473.951454 without breeding credit and 75.079576 with feed100/service30m. It retains the integrated fuel throughput and expense assumptions, so it is a separate supplied reference, not reconstruction of a source plant.

| Published quantity | Source value/boundary | Why comparison remains unmatched |
|---|---|---|
| LCOE | 77.6 USD2004/MWh | Supply, finance, equipment and recurring-expense scope differ; proximity to 75.079576 is not validation. |
| Net output | 1,000 MW | Native predictive baseline calculates 423.106794 MW under mixed declared assumptions; the reference branch supplies 1,000 MW. |
| Operating life | 40 full-power years | Current model uses 40 calendar years; source availability convention remains unresolved. |
| Terminal allowance | 0.5 USD1992/MWh | Current model uses dated USD2004 terminal capital fractions; no silent price-year conversion. |
| Replacement total | 966 million USD2004; rounded 75 million × 13 = 975 million | Source schedule/scope differs from six dated modeled blanket/divertor/LiPb events. |

Retained primary page checks and source interpretations are in the [source-boundary review](../aries-integrated-lcoe/evidence/source-boundary.md). No source result was used to fit the design-study outputs.

## Machinery, assumptions and remaining engineering work

This goal adds **no model equations, library definitions, generated package changes or hidden equipment-selection policy**. It reuses the integrated assembly, selected-inventory cost/capability paths, native lifecycle accounts, stock loader/StudyRunner, independent oracle and exact full-map exporter. Actual adaptation consists of two thin study-support/reporting modules, record-specific configuration/analysis scripts, complete study records and review/preservation evidence. Scenario maps are explicit alternatives; model math is not duplicated in an external plant model. No arbitrary reuse percentage or minimum-change claim is made.

The existing [equipment assumption register](../../../completed/20260922_WI-090_aries-integrated-equipment-and-costs/design.md) and [lifecycle register](../../../completed/20260922_WI-091_aries-integrated-lifecycle-cost/design.md) remain authoritative. New engineered windows and analysis roles live in study configs and the [dependency audit](evidence/dependency-audit.md). Constant USD2004, one construction-financing adjustment, dated replacement cashflows excluding the reserve, complete terminal expense/salvage and maintained-stock accounting are preserved. Feed/service and unsupported efficiencies are not optimization axes.

The dominant remaining assumptions are tritium supply/price and extraction-service capability, followed by thermal deposition/conversion premises and capital/finance boundaries. Actual exchanger geometry, hydraulic/MHD losses and material qualification could invalidate the apparent area saving. Machine maps, confinement/control, magnets/conductor and breeding remain unverified. A qualified design recommendation needs those models/evidence; the present positive goal is a conditional comparison, not a scientifically feasible ARIES plant or a global optimum.

## Identity, verification and replay

The executable remains `d13f4153accc48a3d6533a2d29a8e8b6b7cecd86644c322bb64f59fa402e419b`; semantic fingerprint `419e6e3d7ba46320a1f88b5f478d36abb5ead85d2ecb6fcdb7aff5fcb2c1e131`. All studies reuse the unchanged all-ten-gates CANDIDATE from f4ea4795 under TEAx revision `8d877460ac4f6f264561d916e40c1708adb13397`, with fresh per-study gates/axis declarations. Sealed package archives and exact runtime identity accompany each snapshot.

All 266 cases are checked over 364 scalar channels and 14 predicates: 96,824 scalar and 3,724 predicate comparisons. Every case publishes 546 numeric outputs. This verifies numerical translation and recorded verdicts, not scientific assumptions. Independent local/coupled/robustness reviews replay six/eight/eight selected cases exactly. The final review also checks all 266 ledger rows and 126 matched robustness comparisons. All 9,387 protected original/predecessor files remain unchanged. Entry and final isolated Stellaris regressions match all 1,352 outputs and 68 responses exactly. The inherited full-validator result remains four levels passed/two failed under reviewed L2/L6 exceptions; no new model validation pass is claimed merely from study execution.

Replay instructions are record-local: [local](../../../../exploration/aries_integrated/studies/20260922-aries-integrated-local-response/replay.md), [coupled](../../../../exploration/aries_integrated/studies/20260922-aries-integrated-coupled-design/replay.md), [robustness](../../../../exploration/aries_integrated/studies/20260922-aries-integrated-design-robustness/replay.md). Use isolated copies and exact retained proposals/manifests; never execute into frozen records. Native execution/verification commands and reporting-only scripts are retained. The goal trail preserves one presentation-only freeze retry and the coupled record-deposition ordering deviation; neither reran or altered a native case.
