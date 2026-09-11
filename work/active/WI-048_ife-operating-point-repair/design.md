---
Status: accepted
Created: 2026-09-10
Updated: 2026-09-10
Related Artifacts:
  Spec: ./spec.md
---

# IFE operating point repair design

## Overview and decisions

[AGENT] Use one computed HIF operating point for both Hawker and Meier cost formulas. Keep the printed Osiris operating table as historical reference facts, not as a second independently adjustable cost denominator. Parent accepted this design direction on 2026-09-10. This changes the physical inputs of the Meier comparison, while preserving its monetary and finance conventions.

[AGENT] Use printed gain 87 as the executable gain input. Beam energy 5 MJ therefore produces computed yield 435 MJ. Preserve historical gain 87 and historical yield 432 MJ explicitly; their independent rounding is not an equality constraint. Gain remains a useful study input. Choosing 86.4 instead would reproduce the printed yield, but would replace a directly reported gain with a derived baseline. Both are defensible; this design prefers the printed gain and labels the resulting calculation honestly.

[AGENT] Expose bank energy from the existing Meier driver-cost calculation and bind inherited driver energy to it. Bind the driver's rate to the plant frequency. These become derived quantities, not separately settable entries. Keep the old attribute names where possible to limit interface churn.

[AGENT] Price only strictly positive net output. A shared, tiny handwritten quotient implements the unsupported conditional; the model still owns all physical and economic arithmetic. Parent authorized this native manual-calculation route after the generator limitation was surfaced. Price zero with validity zero is an invalid-price sentinel. Supported consumers must require a satisfied net-generation verdict and validity one before ranking either price.

## Research findings and source facts

The source record in `work/orchestration/goals/fusion-audit-remediation/evidence/round1_source_check.md` verifies the Osiris table image. The source has beam 5 MJ, gain 87, yield 432 MJ, frequency 4.6 Hz, efficiency 0.28, fusion 1987 MW, thermal 2504 MW, conversion efficiency 0.45, gross 1127 MW, driver 82 MW, auxiliary 45 MW, net 1000 MW and cost 5.6 in 1992 cents/kWh. These are [INHERITED] image-verified reference facts. Implementation must preserve them in clearly named `osiris_reference_*` attributes or a named reference part and explanatory current documentation. Historical documents remain unchanged. Such facts need not become generated study inputs merely to be preserved.

The design author visually verified Meier Eq. 5 at `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/images/page_004_eq_0.png`: `(0.32 + 0.088 E_d)(1.25 + 0.05 N_c)(1 + 0.0088(v − 5))` billion dollars. Its beam-energy convention and frequency factor match the existing calculation. No coefficients change. Hawker's existing Eqs. 2.12–2.16 power balance is retained: cooling power equals driver power. The 1.15 blanket factor and 0.90 availability are later modeling assumptions, not historical Osiris facts.

`modeling_project/ARCHITECTURE.md` AD-001/003/004/006 supports plain Real values with documented units, a closed-form DCF, reusable analysis definitions and separate parameter metadata. [AGENT] Item-specific AD-003 structural departure (R-001, accepted by parent on 2026-09-10): retain one unchanged closed-form DCF arithmetic core and move its final division to the shared guarded quotient because the pinned generator cannot compile the conditional guard. Finance conventions are unchanged. This bounded decision does not amend AD-003 or project requirements. The existing IFE definition placement stays unchanged under the item's bounded scope. Definitions introduced here belong in library analyses. The family has eleven source files; three shared foundation/cost hierarchy files remain untouched.

## Proposed elements and equations

| Element and location | Meaning and interface | Requirement |
|---|---|---|
| `Meier HIF Driver Cost`, `models/library/analyses/hif_economics.sysml` | Promote `bank_energy_joules` to output; bank J = beam MJ × 1e6 / efficiency. Gamma = direct driver dollars / bank J. Existing procurement equation unchanged. | MR-WI048-2/3 |
| HIF driver, `models/designs/hif_ife/hif_driver.sysml` | Efficiency 0.28; energy EXPOSE = Meier bank output; beam remains authoritative. | MR-WI048-1/2 |
| HIF plant, `models/designs/hif_ife/hif_plant.sysml` | Frequency 4.6 Hz, gain 87, thermal efficiency 0.45. Driver rate binds plant frequency. Historical reference facts are separately named. | MR-WI048-1/3 |
| `IFE LCOE`, `models/library/analyses/ife_lcoe.sysml` | Retain 14 inputs and DCF arithmetic. Publish fusion/thermal/gross/driver/other/net powers, power conversions and fractions. Replace final quotient with discounted-cost and discounted-energy outputs. | MR-WI048-4/6 |
| `Generating Electricity Price`, same library file | Inputs numerator, denominator, actual net power W. Outputs price and numeric generating indicator (1/0). Manual normative behavior: if net W > 0, price = numerator/denominator and indicator=1; otherwise price=0 and indicator=0. Numerator/denominator units are those of the bound cost channel. | MR-WI048-5/7 |
| `Positive Net Generation`, `models/library/analyses/fusion_cycle.sysml` | One Real net-power formal and strict `net_power > 0.0` predicate. Bind asserted `net_positive` to actual published net W. | MR-WI048-5 |
| Generic plant, `models/designs/generic_ife/ife_plant.sysml` | Instantiate `hawker_price`, expose `lcoe`, powers and named driver/total fractions. Retain old `recirculating_fraction` as documented driver-only compatibility alias. Retain eta-gain gate but identify it as heuristic. | MR-WI048-5/6 |
| Meier cost chain, HIF plant and economics library | Bind reactor thermal GW and Meier net GW to computed outputs. Publish existing annualized-cost numerator and energy denominator, then instantiate `meier_price`; keep plant `meier_coe` alias. | MR-WI048-4/7 |

For bank energy E, beam energy B, gain G, frequency f, blanket multiplier M and conversion efficiency t: fusion power = B×G×f; thermal = M×fusion; gross = t×thermal; driver = E×f; other = driver; net = gross−driver−other. Energy units in these equations are joules, powers watts. Driver fraction = driver/gross; total fraction = (driver+other)/gross. All are computed within the library calculation. Publish thermal/net GW conversions there, not as arithmetic on another calc's output in the design layer.

Annual shots remain 31557600×f×availability, lifetime years = lifetime shots / annual shots. Driver construction dollars = gamma×E and annual replacement dollars = that cost / lifetime years. Preserve the existing 365.25-day shot convention and 8760-hour energy convention; changing these is outside this repair.

## Bindings and channel contract

Data flows beam/efficiency/frequency → Meier bank/procurement → Hawker power/DCF → both price quotients and net assertion. Meier reactor cost depends on Hawker thermal power; Meier denominator depends on Hawker net power. No path returns from a price to physics.

| Consumer | Supplier |
|---|---|
| `driver.energy` | `driver.meier_cost.bank_energy_joules` |
| `driver.pulse_rate_ref` | plant `frequency` |
| `lcoe_calc.driver_energy`, `driver_cost_constant` | driver energy and gamma EXPOSE attributes |
| `thermal_power_gw`, `net_electric_power_gw` | `lcoe_calc` GW outputs |
| `hawker_price` numerator/denominator/net | DCF discounted cost/discounted energy/net W |
| `meier_price` numerator/denominator/net | Meier annualized cost/energy denominator; same net W |
| `net_positive.net_power` | plant net W EXPOSE |

Imports remain library-to-library or design-to-library. HIF plant additionally imports the quotient definition from `ife_lcoe`. Existing two Meier literals may become named plant attributes for reactor units=1 and target factory direct cost=0.1 billion 1988 dollars; this also removes the existing L2 placeholder warnings.

The standalone `driver.energy`, driver rate and Meier thermal/net power entry keys retire. Their exposed attributes remain. Raw `lcoe_calc__lcoe` and `meier_coe_calc__coe_cents_kwh` channels retire; guarded `hawker_price__price` and `meier_price__price` replace them, each paired with `__generating`. Add physical outputs and the net assertion channel. All exact channel censuses and mutation expectations must migrate deliberately, including actual TEAx consumers and standalone scripts. The current pin renders manual Boolean outputs as float, so declare the production validity indicator as Real with explicit 0/1 semantics instead of promising Boolean transport.

## Cost basis and corrected baseline

Hawker still reports dollars/MWh using its mixed inherited 1988-dollar-derived cost coefficients and generic Hawker target costs, 8% DCF discount, five construction years and forty operation years. Meier still reports 1988 cents/kWh using 8.3% fixed charge plus 3% O&M, 1.83 capital multiplier and 8760 hours/year. Both use availability 0.90 and computed net 0.871231785714 GW. The historical 5.6 in 1992 cents/kWh is a printed reference only; numerical proximity is not validation or monetary normalization.

Prototype baseline: bank 17.8571428571 MJ; computed yield 435 MJ; fusion 2001 MW; thermal 2301.15 MW; gross 1035.5175 MW; driver and other each 82.1428571429 MW; net 871.231785714 MW; driver fraction 0.079325416657; total fraction 0.158650833314; driver procurement 0.98452224 billion dollars; gamma 55.13324544 dollars/J; Hawker 240.666460639551 dollars/MWh; Meier 5.589991561584082 cents/kWh. These are generated prototype results, not a completed independent baseline audit. Implementation must add an independent arithmetic oracle and explain movements against the old baseline.

## Prototype and validation report

Prototype source and repeatable scripts live in `prototype/`. `build.py` materializes only the canonical IFE subset and edits the prototype copy. Its early attempted conditional is removed by later transformations; `conditional-failure.txt` preserves the actual failure. The prototype source is an architecture probe and retains stale inherited doc comments; it is not production-ready source to copy wholesale.

Installed `sysml-expert` verified conditional language semantics but found the pinned arithmetic renderer does not support conditionals/comparisons. Actual exact generation independently failed with `SI_EVIDENCE_INCOMPLETE`. The accepted replacement uses an output-only manual calc and the standard handwritten directory. `execute.py` generates, installs `price_impl.py`, regenerates with `preserve_handwritten=True`, then uses sealed `ProvisionalPackageLoader`, `PreparedEvaluator` and `CandidateBridge`. No exporter or compiler was patched. Smart regeneration rejected the initially untyped implementation signature and replaced it with a stub; implementation must retain the generated typed signature when using smart regeneration. The tested preserve-only regeneration route succeeds.

`prototype/validation.txt`: Levels 1–3 PASS, zero parser errors/warnings, zero structural issues, zero cycles. Level 4 PASS: two admitted numerical gates, 100% executable share. Level 5 PASS: 29 documented definitions. Level 6 reports legacy EXPOSE/static-extraction limitations and the intentional manual calculation; public exact generation is separately demonstrated. Do not label whole-tree L6 clean.

`prototype/execution.json` and `execution.txt` record seven real public evaluations: baseline, beam 10 MJ, efficiency 0.35, rate 5 Hz, negative-net counterexample, exactly zero net and positive neighbor. Negative and zero preserve the passing eta-gain heuristic but emit violated net-generation verdicts with both validity indicators zero and sentinel prices zero. Positive neighboring net passes. Gamma×bank identity, power balance, beam doubling and procurement ratio are asserted at relative 1e-9 and absolute 1e-6 W for near-zero arithmetic. The exact-zero fixture uses 5 Hz; at 4.6 Hz cancellation leaves 5.96e-8 W, correctly positive under the literal strict predicate. Do not use that rounded fixture as a zero-boundary test.

## Implementation and acceptance work

- [ ] Implement source facts and library outputs, quotient contract and net constraint with complete current citations; declare numeric 0/1 validity honestly.
- [ ] Wire HIF energy/rate and common power denominators; expose all required powers/fractions and preserve compatibility aliases.
- [ ] Synchronize IFE twin only; generate supported package, implement the tiny typed handwritten quotient and verify native regeneration preserves it and seals.
- [ ] Migrate exact consumer/channel expectations and scripts; require valid price plus satisfied net verdict when using results. A printed sentinel alone is insufficient.
- [ ] Add independent baseline and mutation arithmetic, annual shots/lifetime/capital/replacement checks, exact source literals, negative/zero/positive public execution, live/snapshot parity and family checks.
- [ ] Record all validation levels and skipped/pre-existing failures; request fresh independent review/audit against MR-WI048-1–8 and SV-073–075.

## Risks and approval

[AGENT] The manual implementation becomes a required shipped artifact. Fresh package tests must install it by the supported completion workflow rather than assume automatic arithmetic generation covers it. Source-only parity tests can compare generated stencils; executable comparisons must complete both packages before loading. Cost consumers that ignore constraints must also test the generating indicator before ranking. Such consumers must be found during implementation.

[AGENT] Zero-net rounding is a test-fixture concern, not permission to change strict greater-than semantics. Use an exactly representable boundary and report near-zero absolute residuals. Gross-zero, invalid efficiency, and discount-zero domain hardening are outside these fixtures and are not silently expanded into this repair.

[AGENT] Parent accepted this design for planning on 2026-09-10 under the owner-approved alignment, with R-001 incorporated above. The common physical balance, native handwritten quotient and bounded AD-003 departure remain agent-originated decisions. No owner reserved gates were exercised.
