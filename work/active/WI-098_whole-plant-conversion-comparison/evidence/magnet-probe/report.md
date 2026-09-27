# T-002 exact magnet-offer development probe

[AGENT] The exact prescribed offer completed natively and repaired the local fit/current inadequacy, but failed the unchanged cold and intercept cryoplant capacities. It is not an adequate complete-plant offer. No second offer, tuning or retry was executed. Empirical field extrapolation remains active.

## Execution and identity

- Runtime: `.codex-test/run python work/active/WI-098_whole-plant-conversion-comparison/evidence/magnet-probe/probe.py > work/active/WI-098_whole-plant-conversion-comparison/evidence/magnet-probe/run.log 2>&1`.
- Evaluator: `exploration/stellarator_e2e/studies/study_route.py:230` strict package loader and PreparedEvaluator; `:290` stock StudyRunner, persistent development store `native/wi098-magnet-development-probe.db`.
- Package: `exploration/stellarator_e2e/generated`; executable fingerprint `83ea3b6cf99f5fda6045e7e03b5d430ede91abbe8aa41262c2f9f5aba8663d23`; catalog fingerprint `64882ac8da537bd35fc35b6b575b85792bc0fde94e5a42af853d6ba942a7c279`. Full seal metadata is `package-identity.json`.
- Exactly two completed cases: baseline c0000 and prescribed offer c0001. Complete outputs, constraint verdicts, evidence digest and actual proposal maps are in `native-cases.json`; declared full default/override maps are in `baseline-inputs.json` and `offer-inputs.json`. Underlying native store/artifacts are retained.
- Only three chosen inputs changed: `magnet__winding_pack__wp_side=0.54`, `magnet__winding_pack__fit_aspect_ratio=0.19`, `magnet__casing__interior_y=1.30`. R/a, coil radial allocation, turns, current, all capabilities, material factors and other defaults were held.
- Baseline reproduces all1352 retained WI-080 numeric outputs and67 constraint verdicts exactly; `baseline-parity.json` records comparison. This proves control replay, not independent alternate numerical verification.
- All528 protected model/package files were unchanged; `preservation.json`. The existing runtime emitted Boolean serialization warnings; native execution completed and baseline parity remained exact.

## Native results

| Channel | Baseline | Offer | Difference |
|---|---:|---:|---:|
| Magnet capital, mixed-source model dollars | 1707443242.26 | 2642377329.65 | 934934087.391 |
| Tape capital, assumed dollars | 731571428.571 | 1646035714.29 | 914464285.714 |
| Non-tape materials, mixed-source dollars | 15954709.3744 | 35898096.0924 | 19943386.718 |
| Winding fabrication, estimated2026 dollars | 750415091.66 | 750415091.66 | 0 |
| Insulation capital, model dollars | 421131.967264 | 947546.926344 | 526414.95908 |
| Minimum fit margin, m | -0.12 | 0.0046194570488 | 0.124619457049 |
| Current margin, A | -26282.5961881 | 3364.15857688 | 29646.7547649 |
| Cold winding volume, m3 | 136.56 | 307.26 | 170.7 |
| Stress, Pa | 650000000 | 433333333.333 | -216666666.667 |
| Strain | 0.00216666666667 | 0.00144444444444 | -0.000722222222222 |
| Refrigeration electric power, MW | 2.13776210923 | 2.58172408698 | 0.44396197775 |
| Cold-stage capacity margin, W | 0 | -6145.56901444 | -6145.56901444 |
| Intercept capacity margin, W | 0 | -951.080985563 | -951.080985563 |
| Selected cryoplant cost, model dollars | 31478692.1211 | 31478692.1211 | 0 |
| Axis field, T | 9 | 9 | 0 |
| Peak field, T | 24.9 | 24.9 | 0 |
| Conductor field extrapolated | 1 | 1 | 0 |
| Native fusion source, MW | 2652.56326252 | 2652.56326252 | 0 |
| Native blanket source heat, MW | 3125.93227708 | 3125.93227708 | 0 |
| Native coupled heating, MW | 49.0796007879 | 49.0796007879 | 0 |
| Native net electric, MW | 850.065300667 | 849.62133869 | -0.443961977749 |
| Facility capital, model dollars | 799758795.94 | 799758795.94 | 0 |

## Constraint outcomes

| Constraint | Baseline | Offer |
|---|---|---|
| `cold_stage_capacity_ok__93eb65dcc5b55e0b` | satisfied | violated |
| `divertor_heat_ok__26b4658f9fdfd7b7` | violated | violated |
| `facility_occupancy_ok__2c505953d2466dad` | violated | violated |
| `intercept_stage_capacity_ok__9025ac10e1f2a085` | satisfied | violated |
| `reference_conductor_current_ok__3cf239a7cdc0f2f0` | violated | satisfied |
| `tbr_ok__2cd198f674d413e4` | violated | violated |
| `water_electric_capacity_ok__da93435fdb1e0e2d` | violated | violated |
| `wp_fit_ok__a25ca6a0161f6339` | violated | satisfied |

[AGENT] Both headline verdicts remain violated. The offer adds cold-stage and intercept-stage capacity failures. Local conductor-current and fit failures become satisfied. Divertor heat, breeding, and the retained facility-occupancy/cooling-water equality failures remain. All67 actual constraint verdicts remain in the native record.

## Scope, cost and physical interpretation

[INHERITED: code] The larger selected pack flows into cold volume, tape/non-tape procurement, insulation, current density, stress and strain through `models/library/cost_structure/mfe_power_core.sysml:186–338`. Fit uses `mfe_winding_pack_fit.sysml`; current uses `mfe_conductor_current.sysml`. Cold inventory and exposed cryogenic demand feed the existing supplied-capability screens in `models/library/structure/mfe_plant_systems.sysml:450–635`.

[AGENT] The additional magnet capital is an accounted inventory change under inherited mixed money conventions, not a new USD2025 qualified quote. Winding length, turns and winding-operation cost remain fixed while material volume grows2.25×. The larger transverse casing does not itself increase supplied support/casing mass or change building footprint: the existing local-fit definition explicitly lacks those links. Unchanged structure/facility costs therefore do not prove that this larger physical offer needs no additional support or space.

[AGENT] Added refrigeration demand is0.443961977750MW. The cryoplant purchase remains the old supplied amount despite inadequate cold/intercept capacity. Any new cryoplant is a separately selected, priced offer needing its own review; this probe supplies neither its rating nor price. It must not be called an automatically repaired reactor.

[AGENT] R/a, axis9T and peak24.9T remain unchanged; field_extrapolated remains1. The current calculation executes under the retained allowed-extrapolation input, but20–24T is its stated empirical prediction range. This probe does not establish supported field performance or global manufactured fit. The native baseline plasma/fusion/source conditions remain unchanged; no2500/2800/3000MW supplied-source condition was executed here.

## Analytical lower-current question; no second execution

[AGENT] At independently supplied46kA with the same308turns and geometry, coil excitation would be14.168MA-turn. The existing axis/peak-field equations scale linearly with current, yielding8.28T axis and22.908T peak, inside the declared20–24T conductor range. This is analytical arithmetic only. It changes magnetic field and therefore plasma confinement/sustainment consumers in a full Stellaris run. A supplied-source study could declare the source independently, but must state that changed operating field and retain all offered-capability checks. No46kA case was run.

## Disposition

[AGENT] Exact offer fails additional material cryogenic capacity. Stop this prototype branch at the declared result. It may inform an explicit future selected offer and common-core remediation cost sensitivity after fresh review; it does not establish an adequate core or permission to rank an unsupported field case.

## Exact cryoplant offer handoff

| Public input key | Held baseline and probe value |
|---|---:|
| `stellarator_09__stellaris__cryoplant__purchase_cost_per_module` | 31478692.121086925 |
| `stellarator_09__stellaris__cryoplant__rated_cold_W` | 21933.902368719853 |
| `stellarator_09__stellaris__cryoplant__rated_cryogenic_ambient_K` | 300.0 |
| `stellarator_09__stellaris__cryoplant__rated_cryogenic_cold_K` | 20.0 |
| `stellarator_09__stellaris__cryoplant__rated_cryogenic_intercept_K` | 77.0 |
| `stellarator_09__stellaris__cryoplant__rated_direct_electric_MW` | 0.0 |
| `stellarator_09__stellaris__cryoplant__rated_intercept_W` | 41599.953939961626 |

[AGENT] At the executed50kA offer, required cold-stage duty is28079.471383156567W and intercept duty42551.034925524917W. These are demands, not selected replacement capacities. Selecting new capacities must use independent explicit values and a separately supplied purchase quote; increasing ratings alone leaves the old31478692.121086925-dollar quote unchanged. The source condition in this probe remains3125.9322770825056MW blanket heat,2652.5632625175904MW calculated fusion and49.07960078792678MW coupled heating. These are not the proposed supplied-source main-study loads.

[AGENT analytical, unexecuted] The author-proposed48kA excitation at held turns/geometry implies23.904T peak and8.64T axis, inside the stated20–24T conductor prediction range. Lead/intercept heating changes with current, so the executed50kA duties above are useful evidence but are not the exact unexecuted48kA demands. No additional alternative was run.
