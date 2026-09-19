# Fuel inventory, startup supply and processing demand

The model now calculates all three quantities from explicit operating and fuel-system assumptions. At the reference operating point, the represented system holds **4.418 kg of tritium**, requires **4.400 kg of initial external supply including a conservative decay allowance**, and processes **7.743 kg of tritium per operating day**. The [fresh independent review](evidence/final-review-and-grade.md) assigns **R10.P = 2**, meeting the unchanged target. These are conditional estimates for the represented equipment and storage. They do not establish a complete plant inventory, available external supply or fuel self-sufficiency.

## What the calculation represents

The [flow and storage diagram](evidence/current-trace.md) traces injection, plasma burn, exhaust cleanup and isotope separation, usable storage, blanket release and extraction. Tritium is tracked separately from deuterium. Equal deuterium and tritium atom flows have different masses. Helium, carrier gases, impurities and liquid-metal circulation are outside the reported hydrogen-isotope throughput.

For tritium burn rate B and burn fraction f, injection is B/f and exhaust is injection minus burn. The inherited recovery fraction applies to that exhaust. Its unrecovered fraction leaves permanently at the combined processor outlet; it is not also circulating stock. Blanket production comes from the existing achieved-breeding calculation, with extraction efficiency applied once at the extraction outlet. The calculation retains the inherited 99% isotope-recovery interpretation of a feedstock-cost factor as an explicit conditional assumption, not a measured process performance.

## Fuel held during operation

At 2,652.56 MW of fusion power, 5% burn fraction and 99% exhaust recovery, nominal equipment stock equals inlet flow multiplied by residence time. Plasma stock instead integrates the existing density profile. Residence time is how long material remains in a stage.

| Represented stock | Reference assumption | Tritium held, kg |
|---|---|---:|
| Injection equipment | 20 minutes of injected flow | 0.113197 |
| Plasma | Existing density profile and plasma volume | 0.000308 |
| Combined cleanup and isotope separation | 4 hours of exhaust flow, before recovery loss | 1.290447 |
| Breeder zone | 1 day of gross bred flow | 0.488227 |
| Extraction equipment | 1 day of gross bred flow, before extraction loss | 0.488227 |
| Working storage buffer | Zero additional residence in the minimum-stock scenario | 0 |
| **Minimum working inventory** | Sum of the six represented stocks | **2.380405** |
| Separate interruption reserve | 25% of injected flow for 24 hours | 2.037548 |
| **Working inventory plus reserve** | Represented system total | **4.417953** |

The [source and assumption register](../../../active/WI-069_fuel-inventory-and-startup/design.md) separates literature scenarios from modeling choices. The [registered research](../../../../knowledge/research/pending/20260919-074901_fuel-inventory-residence-startup.md) supplies combined cleanup/separation residence scenarios of 1.3–5 hours, injection residence of 20–30 minutes, breeder-zone residence of 0.1–1 day, and extraction scenarios ranging from an ideal online limit to 1–5 days. The quarter-stream, 24-hour reserve is a source analysis choice, not a plant requirement. The selected serial stages and deterministic return delays are agent modeling choices; the source uses compartment kinetics.

These residence scenarios do not qualify the proposed helium/PbLi system. Wall retention, permeation, bypass, detritiation and other unsupported hold-up remain unresolved contributions. The word “total” refers to the represented boundary. It is not an assurance that omitted stocks are zero.

## Initial supply needed to start

Startup means immediate, constant full-power operation from a defined initial state. Feed equipment and plasma are prefilled; the declared working-buffer and reserve floors are present. Exhaust processing and breeding stages start empty. Recycled fuel first returns after 4 hours, and bred fuel after 2 days. This represents return delays, not an ignition ramp or detailed commissioning schedule.

The initial purchase covers **0.113505 kg prefill + 2.037548 kg reserve + 2.247415 kg maximum cumulative supply deficit = 4.398468 kg** before decay. A conservative decay bound adds **0.001656 kg**, giving **4.400124 kg**. The deficit calculation checks every return-time breakpoint and the declared horizon. A longer horizon is available when continuing net consumption needs to be represented.

The operating inventory is not added again to startup supply. Injected fuel fills the exhaust processor, and in-plant breeding fills the breeder and extraction stages. That is why initial external supply can be slightly below the eventual operating stock. The decay allowance accounts for its own decay and gross breeding over the horizon; it is a conservative mass bound with assumed replenishment access, not an exact transient minimum.

## Running capacity and recurring fuel demand

The combined processor must handle **7.742681 kg T/day**, equivalent to **12.911794 kg D+T/day**, whenever the plant runs at the reference point. Injection equipment handles **8.150190 kg T/day**. Annual availability must not reduce these equipment capacities.

The existing maintenance calendar gives 90.2778% availability at this point, producing **2,551.321 kg T/year** of processor load. Permanent exhaust-recovery loss is **0.077427 kg T per operating day**, or **25.513 kg/year**. Maintaining the declared inventory through shutdowns requires **0.248386 kg/year** of decay replacement. A separate passive-shutdown calculation reports exponential stock decay when replacement stops; it is not mixed into the maintained-stock calendar policy.

Gross production at the mean achieved breeding ratio slightly exceeds the computed reference annual demand, giving a signed balance of **−0.835780 kg/year** of external makeup. This conditional arithmetic does not demonstrate adequate breeding: the existing conservative breeding screen still fails. Computing inventory raises the unchanged required-breeding formula from 1.19 to **1.191670**, while the existing lower breeding estimate is **1.186146**. Fuel-processing costs and the reference LCOE of **$273.455/MWh** are unchanged.

The [costing interface](evidence/throughput-interface.md) identifies named outputs, units, isotope basis, module basis and applicability flag. Equipment pricing still needs concentration, purity, design margin, carrier-flow and installed-price information; this goal supplies throughput and stock quantities.

## Study and verification

The [26-case native study](../../../../exploration/stellarator_e2e/studies/20260919-fuel-inventory-and-startup/record.md), frozen in local commit `3529f6c8`, varies 15 public input axes and retains every result. Its [report](../../../../exploration/stellarator_e2e/studies/20260919-fuel-inventory-and-startup/report.md) and [numeric table](../../../../exploration/stellarator_e2e/studies/20260919-fuel-inventory-and-startup/results/points.csv) show the main drivers:

- **Burn fraction sets circulating demand.** At fixed fusion power, changing the assumed burn fraction from 2.5% to 10% reduces processor load from 15.893 to 3.668 kg T/day. Held inventory falls from 7.927 to 2.663 kg. These are performance sensitivities, not demonstrated operating improvements.
- **Residence times set equipment stock and return delays.** Changing combined processing residence from 1.3 to 5 hours raises total held stock from 3.547 to 4.741 kg and conservative startup supply from 3.538 to 4.720 kg, without changing required throughput.
- **Reserve policy is a large independent choice.** Supplying a full day of interrupted circulating flow instead of one quarter raises total held stock to 10.531 kg. The selected fast and slow combined scenarios give 1.091 and 7.090 kg held, and 1.087 and 7.063 kg conservative startup supply. The complete finite list spans 1.091–10.531 kg held. This is not a confidence interval or a physical bound.
- **A startup purchase cannot cure a continuing deficit.** At 95% extraction efficiency, annual external shortfall is 7.208 kg. Extending startup coverage ten days beyond both return streams raises conservative initial supply from 4.400 to 4.629 kg, with operating stock and capacity unchanged. Reduced availability also leaves decay running while breeding stops; the 90% unplanned-downtime case has a small positive annual shortfall despite the reference mean-breeding surplus.

The scenarios support a useful estimate of represented stock and its drivers. Source uncertainty prevents a qualified complete-plant inventory or procurement requirement. No case passes every whole-plant screen. At reference, the divertor, conductor-current, conservative breeding and winding-pack fit screens fail; these results remain in the study.

All **23,556 mapped scalar comparisons and 650 predicate comparisons pass**, including all 70 new inventory/startup/throughput outputs at every case. The 906 mapped scalar outputs comprise 892 numeric quantities and 14 Boolean flags; 22 inherited numeric outputs remain exported native evidence outside the oracle map. The [audited implementation](../../../active/WI-069_fuel-inventory-and-startup/audit.md) has 75 passing author domain tests, 195 passing affected oracle tests, 700 off-reference native/oracle scalar comparisons and a strict 70-output baseline comparison. Independent source-image, conservation, startup-breakpoint, limiting-case and numerical-domain reviews supplement software agreement. Two mechanical study-verification retries corrected output counting and integer/float input joins; neither changed the model, cases or raw results.

The [native integration return](evidence/integration/integration_return.json) accepts local candidate `956444b5d440238857911a0406e6d3f51ddcbf2e`, with semantic fingerprint `1d97071e32b40888ef206f0c403250a28a9ecfad7e921797546f0a3ddcc0c1ef` and executable fingerprint `e19b63a03be3a00ebd5cec4ce4ed06a082f5bb7ed89b736aed06feaea8d1e319`. Its manifest gate explicitly does not check read-set coverage. Static validation still fails at inherited L2/L6 diagnostics; three additional pure-EXPOSE diagnostics resolve in the generated runtime and are [classified explicitly](../../../active/WI-069_fuel-inventory-and-startup/evidence/static-classification.md). Static validation is not claimed to pass.

Formal goal closure remains the owner's decision. ARIES remains sealed, the published r2 comparison is preserved, and no merge or push is part of this work.
