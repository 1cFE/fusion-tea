# Current Round 2 residual dispositions

[AGENT] This is the current interpretation of the repaired interface, based on the independently released Round 2 architecture and the generated contract. It supersedes the current-use interpretation of affected R09–R12/R14 descriptions in the accepted WI-074 record. It does not rewrite that historical record or upgrade an inherited decision into an owner-originated requirement. Final integrated acceptance is PASS at checkpoint fce788412fa53384688642dbc7deee9ee66431f2; see the goal answer and evidence/round2/final-review.md.

[INHERITED: WI-074 residual-dispositions.md] The prior physical assumptions and scientific limits remain unless this document identifies a specific implemented replacement. A direct consumer proves that an input reaches a calculation; it does not prove empirical validity, equipment qualification or adequate capacity.

## Interface coverage

[AGENT] [Current coverage](evidence/current-interface-coverage.json) joins all 704 generated inputs to 1,121 direct pipeline consumer edges. No current input lacks a consumer. It retains the classifications of all 597 entering inputs, including the 11 explicitly retired price helpers. The current interface contains 586 retained inputs and 118 additions: 49 supplied ratings/rating conditions, 27 procurement inputs, 40 administrative Boolean masks and two single-module formals. The electric-plant gross rating also drives its linear price law; it is counted once among the 49 physical offer fields. The procurement inputs comprise five supplied package amounts and 22 cost classes.

[AGENT] Exact added and retired names, generated consumers and source hashes are in the coverage record. Prior classifications are copied as explicitly inherited evidence, including their historical wording. Their current interpretation follows this document. Scope and final acceptance are separate from structural coverage.

## R01

[INHERITED: WI-074 R01] The chosen torus dimensions and layer thicknesses determine geometry by the existing identities. No layer is enlarged to make a thermal, breeding or magnetic screen pass. Arbitrary independently specified shapes remain outside this parameterization. Geometry still affects represented volume-priced costs.

## R02

[INHERITED: WI-074 R02] Density, temperature, profiles, composition and selected magnetic state determine fusion, radiation and auxiliary heating demand. They do not select installed heating hardware. The specified-state plasma and transport assumptions remain; passing the installed heating screen does not establish ignition or validate the transport model.

[AGENT] Six retained propagation cases verify that density changes alter source heat, primary-loop requirements and downstream steam/rejection requirements at fixed offered equipment. Heating demand and the existing native sustainment predicate agree with independent arithmetic. See [propagation acceptance](evidence/propagation-acceptance.json).

## R03

[INHERITED: WI-074 R03] Chosen blanket thickness and the existing bounded neutron-transport interpolation determine the conditional breeding estimate. The numerical lower estimate is compared with the design floor and maintained-stock fuel requirement. No automatic blanket thickening or unsupported breeding credit is introduced.

[AGENT] Changed plasma demand reaches breeding production and the native `tbr_ok` predicate in the propagation evidence. Existing source-transfer and geometry limits remain. A supplied turbine or cryogenic offer cannot qualify breeding.

## R04

[INHERITED: WI-074 R04] The divertor retains its fixed-profile heat ledger and peak-load comparison. Peak-equivalent area is a diagnostic, not an independently purchased target area. Independent footprint, full target geometry and lifetime qualification remain absent.

[AGENT] Capital now consumes the selected divertor package dollar amount. The replacement event uses that amount while the existing load-dependent calendar remains active. This changes price ownership, not divertor physics. Demand still reaches the peak-load screen and its native verdict; changing the package price does not make the thermal screen pass.

## R05

[INHERITED: WI-074 R05] Exhaust boundary conditions still determine required effective pumping speed. Installed vacuum pump/duct conductance, an offered-speed comparison and a corresponding procurement account remain absent. This is a demand calculation only.

## R06

[INHERITED: WI-074 R06] Fuel stock remains an explicit maintained nominal stream-times-residence/buffer/reserve scenario. It is not independent offered active inventory, tank capacity or proof of reserve adequacy. Dormant held-inventory compatibility does not establish active supplied-stock evaluation.

## R07

[INHERITED: WI-074 R07] Startup deficit and conservative prefill remain requirements rather than purchased external supply. Productive-time processing and calendar-time decay remain distinct. The repaired legacy fuel-handling price class does not add fuel-stock purchasing, supply assurance or detailed startup transients.

## R08

[INHERITED: WI-074 R08] The calendar retains the explicit replace-at-fluence-limit policy and its downtime/restart assumptions. Demand may change event timing, productive life and annualized replacement cost. Fixed offered equipment does not freeze the operating calendar or turn it into arbitrary schedule optimization.

[AGENT] The selected divertor offer supplies its replacement cost. Fixed-demand and changed-price evidence belongs to WI-079; the thermal propagation record verifies fixed cooling purchase, spares and modeled replacement equipment cost under the selected load perturbations.

## R09

[AGENT] Turbine, heat rejection, cryoplant, power supplies and divertor capital consume independently supplied package dollar amounts. Their captured defaults are assumed offers, not vendor quotations. The package scope and declared rating conditions describe a hypothetical offered specification. Changing a rating at unchanged price is a different hypothetical offer, not evidence that a physical upgrade is free. No live demand-based sizing or fallback selects these amounts.

[AGENT] Blanket, shield, vessel and residual structure retain represented geometry plus independent procurement classes in their inherited price laws. Other cost allowances use supplied design classes rather than operating demand. Their source scaling, currency and scope limits remain. They do not establish a missing capacity or a complete bill of materials. The electric-plant cost retains its single gross-MWe rating law and only a real-power capacity screen; reactive power, fault duty and detailed distribution hardware remain unresolved.

## R10

[AGENT] Legacy grouped facilities, preconstruction, cooling and fuel-handling price paths now use supplied procurement classes. Their selectors still determine whether a legacy or detailed account contributes. Dormant legacy inputs remain compatibility assumptions with real calculation consumers; their presence does not imply active capacity evaluation. Detailed supplied facility, processor and cooling choices from Round 1 remain in force.

## R11

[AGENT] Operating primary-loop, salt-loop, steam and cooling-water balances still compute required flow, pressure rise, pumping work, exchanger conductance and heat rejection. New scalar screens compare these requirements with the selected ratings. Signed margins remain raw rating minus demand. No tolerance changes the physical pass criterion. State identity allows the reviewed finite eight-ULP comparison solely to avoid false state mismatch between equivalent floating-point calculation paths.

[AGENT] Helium and salt screens apply only when their represented equipment and corresponding operating mode are active. Matched steam and cooling-water checks require their computed active states. Declared temperatures, pressures and other exposed state facts govern support. Missing UA availability, an inactive mode or an unsupported point state yields no affirmative capacity credit. The IHX geometry-based margin is now included in the native assertion inventory.

[AGENT] The retained density perturbations change helium suction state, so the helium point offer becomes unsupported. Salt return state stays fixed, allowing salt and steam rating checks to remain defined while their demand changes. This is observed propagation, not a newly assumed off-design envelope. Pump curves, compressor maps, exchanger pressure design, complete auxiliary heat sinks and site/tower qualification remain absent. The model keeps equipment/site qualification flags false.

## R12

[AGENT] Cold-stage and intercept loads now have independently supplied watt ratings at declared cold/shield/ambient temperatures. The direct electrical term has its own limited electrical screen; its unspecified cold-stage equivalent remains unresolved. No watts-at-one-temperature transfer is inferred. The selected cryoplant package amount is independent of operating COP and heat load; auxiliary cooling retains a separate selected thermal cost class.

[AGENT] At fixed temperatures, the retained support-conductance perturbation changes cold/intercept loads and margins. Separate cold and shield Carnot-fraction perturbations change electricity without changing physical loads, ratings or purchase amounts. These checks do not add a refrigerator performance map, complete auxiliary heat allocation or structural qualification of the thermal support geometry.

## R13

[INHERITED: WI-074 R13] Installed source/coupled heating capacity stays separate from operating heating demand. The existing zero-direct-term stellarator configuration is covered by the retained propagation cases. Generic simultaneous direct delivered/coupled terms still lack an independently qualified consistency relation outside that active configuration.

## R14

[AGENT] Accounting identities, financial rates, construction duration, operating lifetime and availability policies remain. Staff/operating allowances and the repaired startup/decommissioning and other price proxies use supplied cost classes. Actual energy, fuel use and the load-dependent calendar may still change with operating demand. Consequently LCOE may change even when every equipment purchase amount stays fixed. Fixed hardware does not mean fixed operating cost or fixed economic performance.

## Administrative flags

[AGENT] Forty generated Boolean literals are explicitly mapped as credit-withholding masks, separate from physical offers. Thirty-nine are scalar-screen masks and one enables the cryogenic state check. False makes the affected result undefined and prevents an affirmative capacity verdict. These masks cannot replace computed state support, UA availability or a negative capacity margin. All 40 false-flag cases were compared with native execution in `tests/models/test_offered_capability_flag_native.py`. Public visibility is an emitter artifact, not a new scientific choice.

## Single-module scope

[AGENT] Two new package cost formals expose module count for power supplies and divertor. The supplied-package seeds reject values other than one. Existing module-count inconsistencies remain outside this repair; no general multiple-module capability or cost claim is made.

## R15

[INHERITED: WI-074 R15] Supplied constants, thresholds and domain assumptions remain explicit. Passing a scalar screen does not establish omitted physics or equipment qualification. The new administrative masks and single-module formals have the narrower meanings above.

## M75

[INHERITED: WI-074 M75] Round 1 supplied magnet dimensions, inventories and masses remain selected design choices. Material/field/current/strain and topology or structural qualification limits remain unchanged.

## F76

[INHERITED: WI-074 F76] Round 1 supplied facility geometry, parcel, package counts and positions remain evaluated choices. The repaired legacy price classes do not qualify structures, detailed handling equipment or omitted services.

## F77

[INHERITED: WI-074 F77] Fuel-processing capacity remains independently supplied. Source applicability and cost-source bounds remain separate from capacity adequacy.

## C78

[INHERITED: WI-074 C78] Cooling purchase points and purchased coolant stocks remain independent of operating demand. Round 2 adds conditional offered-capability screens without introducing off-design machine maps or changing inherited cost-source limits.

## Acceptance boundary

[AGENT] This census establishes complete current input-to-consumer coverage and records the revised semantic limits. The targeted propagation and public-mask tests provide bounded native evidence. Full regression accounting and complete native/oracle verification are retained in evidence/validation-summary.json; all ten committed native integration gates pass in integration/seam/integration_return.json. Final independent integrated acceptance is PASS in the goal evidence/round2/final-review.md. This document does not mark the goal complete or claim that every plant screen passes.
