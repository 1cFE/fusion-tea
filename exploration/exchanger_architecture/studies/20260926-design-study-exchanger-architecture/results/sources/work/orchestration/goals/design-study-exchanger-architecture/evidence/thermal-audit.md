# Thermal audit: series versus series-then-parallel

[AGENT] Bounded audit, 2026-09-26. This is source inspection and a 32-point native scratch screen, not independent review or a sealed goal study. Existing packages, studies and model files were read only. No external source or quarantined material was opened.

## Finding and recommended comparison

The prior 45.224 MW network shortfall at density 5.5e20 is caused by the chosen 0.85 split starving the divertor stream. Splits 0.55–0.80 tested here remove all heat at identical hardware and match the series case's 735.759 MW net. At 5.6e20, series leaves 21.424 MW in PbLi; network splits 0.65, 0.75 and 0.80 remove all heat and produce 801.863 MW net. Both arrangements fail at 5.75e20 across the tested splits. This supplies a useful bounded question: how much load extension remains after fairly varying common operating choices and applying explicit thermal assumptions?

[AGENT] Recommend a **downstream supplied-load comparison anchored to the N calculated-profile case**. The original ARIES profile model computes fusion power from imposed density, temperature, species and volume. It has no heating/sustainment calculation. Its 20 MW auxiliary deposited heat is consistently charged as 40 MW electric, but the model cannot establish that this heating sustains the imposed profiles. Importing the WI-093 Stellaris sustainment chain would add consequential assumptions and is unnecessary for a downstream architecture question. Keep the exact N calculated-profile replay as provenance; use source mode 0 for the main supplied-load family, with explicitly stated inherited deposition fractions and 20 MW heating. The resulting branch duties and calculated hot/return temperatures describe a conditional downstream boundary, not a realizable blanket family.

## Named starting point and hardware

The starting point is **N: inherited ARIES calculated-profile nominal, WI-092 series closure**. Exact map: `exploration/aries_integrated/studies/20260926-aries-design-choice-interactions/results/cases.json`, stored case `N-control` (config alias `b3-N-amp5.00e20-hol0.66-net0`). Its producer mode is 1 (calculated), and its heat mode is 0 (partition relation). The corresponding source model is `exploration/aries_integrated/input_models/plasma_integration.sysml`; live plant is `models/designs/aries_cs_integrated/plant.sysml`.

| Quantity | N value / status |
|---|---|
| Supplied plasma shape | amplitude 5e20 m^-3; edge ratio 0.1; hollowness 0.66; density exponents 12 and 1; temperature axis/edge 11.83/0.2 keV, exponents 2 and 1; helium fraction 0.0335; D fraction 0.5; volume 444 m³, measure exponent 2; field 5.7 T |
| Calculated fusion | 1835.4512830147435 MW |
| Deposited auxiliary heating | supplied 20 MW; efficiency 0.5; electric 40 MW; 20 MW loss |
| Delivered He / PbLi / divertor heat | 896.545166 / 1039.526189 / 304.317692 MW; total 2240.389047 MW |
| Cycle | helium 1400 kg/s; cp 5193 J/kg/K; gamma 5/3; 308.15 K cooler target; three ratios 1.51829448594; compressors 0.89; turbine 0.93; recuperator 0.8; pressure-loss fraction 0.045 |
| Primary He / PbLi / divertor flow | 3261 / 26860 / 500 kg/s; respective cp 5193 / 190 / 5193 J/kg/K |
| Primary hot-temperature caps | He 729.15 K; PbLi 1011.15 K; divertor 973.15 K; caps, not supplied operating temperatures |
| Exchangers | each 50000 m² and U 1000 W/m²/K; each UA 50 MW/K |
| Selected duty capacities | He 1500 MW; PbLi 1800 MW; divertor 800 MW |
| Selected machines/rejection | compressor 1600 MW; turbine 3500 MW; generator 1800 MW; rejection 2500 MW |
| Output | turbine inlet 788.637518 K; gross 655.354927 MW; compressor demand 1372.850948 MW; net 423.106794 MW; cycle rejection 1571.659530 MW; all implemented checks satisfied |
| Auxiliary load | 232.248133 MW including pumps 166.01 MW, heating 40 MW, cryo 10 MW, fuel 6.238133 MW, control 5 MW and other 5 MW |

The 891 MW alternative belongs to the separately declared source-supported/reselected scenario with different flow, recuperation, source partition and compressor offer. Do not use it as another operating point of N without enumerating every difference.

## Physical connection graphs

```text
Series cycle stream:
compressors → recuperator cold side → He HX → divertor HX → PbLi HX → turbine

Network cycle stream:
compressors → recuperator cold side → He HX → split
                                             ├─ s × flow → PbLi HX ────┐
                                             └─ (1−s) × flow → div HX ─┤
                                                       ideal mixing ←─┘ → turbine

Both: turbine → recuperator hot side → precooler → compressors
Primary sides: independent He / PbLi / divertor coolant streams, one per exchanger.
```

Source: `exploration/aries_integrated/native_completions/network_heat_driven_closure_impl.py`; reviewed direction and split roles: `work/completed/20260925_WI-092_aries-parallel-exchanger-network/design.md`. Each stage uses counterflow effectiveness from supplied UA and capacity rates. Transfer is the smaller of supplied duty and capability at the hot cap. In series the next stage gets the preceding outlet. In network, PbLi and divertor get the same He-stage outlet; their capacity rates are `s*C` and `(1-s)*C`. Mixing is ideal and pressure losses are not branch-specific. Bisection solves the recuperator/turbine temperature feedback; it does not choose hardware or split.

If both architectures remove exactly the same duty at the same cycle flow, ratios and efficiencies, their total cycle heat balance gives the same turbine inlet, gross and net power. Architecture then changes thermal feasibility and primary states, with no intrinsic electric benefit in this implementation. A benefit arises when one architecture permits a different passing operating choice or load, or when architecture-specific costs/losses are represented.

## Heating, source and return coupling

- The profile quadrature lives in `exploration/aries_integrated/aries_integrated/handwritten/supplied_profile_plasma/supplied_profile_plasma_impl.py`. It returns fusion, density, temperature, pressure and stored energy. There is no sustainment requirement or heating adequacy verdict in this assembly.
- `integrated_heat_source_impl.py` partitions fusion into 80% neutron and 20% charged power. With N multipliers, blanket heat is `1.16*0.8*P + 0.25*0.2*P`; 38% goes to He, 62% PbLi; `0.04*P` is exchanged from PbLi to He. Divertor gets `0.75*0.2*P + 20`. Pump friction adds recovered heat once. These are inherited assumed relations, not new blanket predictions.
- The plant binds the same deposited auxiliary heat into `generator_auxiliaries` (`plant.sysml:379`); the electrical balance divides by efficiency, and the ledger retains heating losses, generator/motor losses, rejected heat, pump recovery/loss and other auxiliaries (`integrated_plant_ledger_impl.py`). Thus the 20 MW assumption is consistently accounted for; its plasma adequacy is unknown.
- Primary hot temperature is calculated as `secondary_in + transferred/K`; primary return is `hot − transferred/Ch`. For heat-removal failures these states describe only the removed portion. A primary hot cap must never be reported as the actual hot temperature.
- N series actual hot/return pairs are He 605.212/552.270 K, PbLi 852.807/649.114 K, divertor 720.998/603.795 K. No fixed primary return requirement is exposed, and no return-condition constraint exists in this assembly. The WI-095 Stellaris loop return condition is a different source model and cannot be imported as an ARIES requirement.
- Missing return requirements cannot be certified satisfied. The main contract should state the downstream boundary explicitly, retain these calculated states, and show the externally required return condition as unqualified. If a claimed closed blanket loop needs specified returns, supplying supported return constraints and solving their coupled states/control becomes a model dependency.
- WI-093 C-2 does contain the Stellaris required-heating channel, but leaves it disconnected: its documented values include 49.1 MW nominal, 66.7 MW lower density, and −14.9 MW peaked profile. Reusing that assembly would introduce the unresolved heating interpretation rather than repair N by wiring an existing N output. Evidence: `work/completed/20260926_WI-093_combination-assemblies/report.md` §2 C-2.

## Scratch evidence and missing checks

The scratch script called the stock `study_route.run_points` on complete copies of N inputs. Domain declared before execution: amplitudes 5.0, 5.5, 5.6, 5.75e20; series once at each amplitude, plus network splits 0.55, 0.65, 0.75, 0.80, 0.85, 0.90, 0.95. All other inputs stay exact. It records 32 cases and every native verdict. No native model arithmetic was replaced.

| Fusion MW | Series unmet MW | Network tested behavior |
|---|---:|---|
| 1835.451 | 0 | splits 0.55–0.85 tested pass; 0.90/0.95 fail divertor |
| 2220.896 | 0 | 0.55–0.80 tested pass, same 735.759 MW net; 0.85 leaves 45.224 MW divertor |
| 2302.390 | 21.424 PbLi | 0.65/0.75/0.80 pass all implemented checks, 801.863 MW net; 0.55 fails PbLi, ≥0.85 fails divertor |
| 2427.384 | 149.872 PbLi | all tested fail; smallest tested unmet 38.873 MW at 0.75 (13.36 He + 25.52 PbLi) |

These are sampled results, not optimized boundaries. There is no extra operating freedom for series in this scratch screen; a main comparison must provide equal cycle flow and pressure-ratio choices.

**Temperature approaches are the most consequential missing screen.** N series hot/cold terminal differences in K are He 1.418/71.793, PbLi 64.169/3.461, divertor 75.345/0.0003168. The passing 2302.390 MW network at split 0.75 has He 1.722/87.185, PbLi 35.113/18.747 and divertor 0.01610/61.807. Native constraints do not require a positive engineering minimum beyond the counterflow equation's passive condition. The prior reconciliation source summary cites 30 K, but that source condition is not automatically a requirement on the assumed N design. Declare any minimum as a source condition or explicit sensitivity, never choose it merely to admit a desired result. Finite-UA stage behavior at a hot cap does not on its own guarantee a specified minimum approach.

Other missing qualification: branch hydraulics and split achievability; differential branch pressure losses/pumping; material temperature limits beyond assumed bulk caps; primary return requirements; machine maps; blanket heating/deposition validation; plasma sustainment; recuperator physical inventory/cost. The package explicitly publishes zero support flags for deposition, hydraulics, materials, machine maps, magnets and breeding. All-checks-passing is not scientific qualification.

## Minimal main screen and exact execution paths

[AGENT: coordinator direction] Main comparison will use a supplied fusion family over 1650–2600 MW, flows 1300, 1400, 1500 and 1600 kg/s, and network splits 0.50, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85 and 0.90. The exact load grid belongs in the comparison contract before execution. Series gets every common load/flow combination and the same other settings; network gets those plus its split. Keep the complete N inventory, primary flows, source fractions, supplied 20 MW deposited heat and efficiencies. The source boundary does not claim sustained plasma. Preserve the N replay and B3 controls as provenance. Do not trigger automatic model repairs from this audit.

Use the exposed keys under `aries_integrated_plant__`: `source__producer_mode=0`, `source__reference_fusion_mw` for load; `cycle__selected_flow`; all three `compressor_N__selected_ratio`; `heat_exchangers__network_mode`; `heat_exchangers__pbli_split_fraction`. Preserve `deposition__heat_mode=0` for the declared partition relation. Do not independently vary deposition, primary temperature and flow and call the set a physically closed blanket.

Before claiming an architecture range extension, examine the thermal-boundary implications of the chosen approach requirement. Postprocessing may flag terminal differences, but it cannot simulate a changed approach/control law or new return control. If that law is required for a credible comparison, define and independently review an additive variant. UA uncertainty can be screened with the existing `*_hx__assumed_u` at fixed area as performance uncertainty; changing area is a separately priced hardware decision. Pump-law sensitivity, pressure loss and heat-transfer assumptions can change the operating boundary; choose a small subset of passing/boundary controls after the first screen.

Executable infrastructure:

- `exploration/aries_integrated/studies/study_route.py`: `run_points(study_id, complete_input_maps, work_dir)` uses the stock native evaluator and SQLite store. Identity and complete entry maps are checked.
- `exploration/aries_integrated/studies/interactions_support.py`: existing `prepare`, `scan`, `baseline`, `execute` CLI commands; `--record`, `--config`, and `--integration-return` are the arguments. It reuses `reconciliation_support.proposals` and the committed predecessor executor. Reuse through a goal-owned wrapper/config; do not write another study into a historical record or repin the historical package.
- `exploration/aries_integrated/studies/interactions_reporting.py`: inspect its output-channel map for per-stage duty, capacity, net power and fuel channels. Reporting does not generate physics.
- Authoritative implementation for stage physics: `exploration/aries_integrated/native_completions/network_heat_driven_closure_impl.py`; source partition: sibling `integrated_heat_source_impl.py`; energy check: sibling `integrated_plant_ledger_impl.py`; generated runtime counterparts are under `aries_integrated/handwritten/integrated_heat_electricity/`.

Replay this audit (outputs stay in `/tmp`; rerun uses the compatible retained store):

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python work/orchestration/goals/design-study-exchanger-architecture/evidence/thermal-screen.py > /tmp/thermal-screen-result.json'
```

Retained artifacts: `evidence/thermal-screen.py`, `evidence/thermal-screen-result.json` (inputs, baseline channels and 32 summarized native cases); native scratch store and package link remain in `/tmp/thermal-screen-run/`. The JSON is scratch evidence, not an immutable native study seal or independent numerical verification. The next native study must store complete outputs, failures and identity, verify them, and seal through the prescribed goal/study workflow.
