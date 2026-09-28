# Round 2 thermal requirements: original-source reading and proposed boundary

[AGENT] Thermal author, 2026-09-27. This is a source/interface recommendation, not independent review or implementation. Authority: owner-supplement-r2.md. Original retained page images were viewed directly; no quarantined PDF or external source was opened. The brief’s `source-check.md` resolves to `source-check-review.md` in the earlier reconciliation goal. WI-086 remains under `work/active/`.

## Recommendation

Adopt a named **N-R conditional source family**: preserve N’s source partition, primary flows, heat capacities, recovered pump heat, selected equipment and hot caps; add exact primary return targets of He 659.15 K, PbLi 724.15 K and divertor He 846.15 K. These targets are **[AGENT] design requirements informed by Raffray’s nominal component inlet temperatures**, not source-established requirements of the earlier N family. The source duty split, divertor flow and cycle settings differ from N. Do not claim to reproduce the published ARIES point.

For each primary loop, require `H_required = R_target + Q_delivered / C_primary`, with `C_primary = mass_flow * cp / 1e6` in MW/K. `Q_delivered` already includes the inherited recovered pump heat. Require the calculated hot state to stay at or below the existing supplied hot cap, and require all of that duty to be removed. Report the return residual and actual hot state separately. Do not infer a higher hot cap or larger flow from failed duty.

This is sufficient to invalidate the previous leading 2200 and 2300 MW cases under a clearly stated thermal requirement, independently of exchanger conductance or connections: the unchanged divertor stream needs 711.263 and 717.040 °C, respectively, above its 700 °C cap. Both architectures fail that condition. This is an applicable negative result, not an invitation to relax the return requirement or enlarge equipment automatically.

**One material interpretation remains unresolved: applying the cited 30 K to actual individual exchanger terminals.** The source does not uniquely supply a six-terminal requirement. Do not implement a claimed source-derived 30 K pass by comparing mixed streams that do not exchange heat. Recommended owner decision before claiming any new preferred passing case: adopt a 30 K minimum at both actual terminals of each exchanger as an explicit conservative **new conditional design requirement**, or provide/authorize a different branch-specific minimum-approach specification. The first option is straightforward to audit but is stronger than what can be proved from the retained source; its provenance must remain [AGENT, if ratified]. The alternative is to resolve the branch requirements through additional supported engineering/source work. The leading-case hot-cap failures can be established while that decision is pending.

## Original evidence and applicability

All paths in this table refer to retained post-reveal evidence already admitted by the project. Printed numbers are source facts; their use in N-R is a separate design choice.

| Original evidence | Directly observed fact | What it supports / does not support |
|---|---|---|
| `work/active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p737.png`, Table III | One row reads “HX temperature difference between hot and cold legs” with value 30 °C. The same table separately lists recuperator effectiveness 0.95, pressure loss 0.045, turbine efficiency 0.93 and compressor efficiency 0.89. | A source cycle/HX temperature-difference parameter. It is not a recuperator approach. The row does not say “minimum,” identify six terminal checks or state an off-design control law. |
| `work/active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p736.png`, Fig. 12 inset | “Typical Fluid Temperatures in HX”: cycle He 355→707 °C; blanket He 385→460 °C; PbLi 464→737 °C; divertor He 571→700 °C. The illustrated cold-bank endpoint is 385−355=30 K; the illustrated hottest-bank endpoint is 737−707=30 K. | The 30 K can be located at the two ends of the illustrated composite temperature diagram. The image does not specify all intermediate branch temperatures or all individual terminal differences. Its numbers differ from Tables II/V and are explicitly typical. |
| Same Fig. 12, physical schematic | All cycle flow passes the blanket-He exchanger, then splits between PbLi and divertor exchangers, then mixes before the cycle. Primary circuits remain separate. No primary bypass or pump is drawn. | Confirms the actual network. Does not establish branch flow split, branch outlet equality, pump placement or bypass control. |
| `work/active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p734.png`, Table II | He inlet / first-wall outlet / module outlet 386/430/456 °C; PbLi inlet/outlet 451/738 °C. He flow 3261 kg/s; PbLi flow 26860 kg/s. He thermal removal 1192 MW includes 141 MW friction and 111 MW conducted from PbLi; He pumping power 156 MW. PbLi duty 1444 MW is net of approximately 111 MW transferred to He; PbLi pump power approximately 1–10 kW. | Nominal component operating temperatures and source-case duties. These are not stated inlet bounds, general setpoint requirements or N operating conditions. Distinguish 156 MW electric from 141 MW recovered fluid heat. |
| `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/raffray-p741.png`, Table V and nearby text | Divertor He inlet/outlet 573/700 °C; flow 283 kg/s; thermal power 186 MW including 24 MW friction; pumping approximately 27 MW. Text describes inlet/outlet approximately 570/700 °C fitting the overall exchanger/Brayton scheme. | Nominal source divertor condition. N uses 500 kg/s, 10 MW pumping and 9 MW recovery, so imposing 573 °C on N is an explicit transferred requirement, not the original source point. |
| `raffray-p737.png`, right-column thermal-hydraulic optimization paragraph | Friction power from blanket/divertor He flow is added to fusion thermal power for the cycle calculation. | Recovered friction belongs in cycle-delivered duty once. Does not locate where in the primary loop that heat is added relative to a named inlet sensor. |

The whole cited source scenario is not internally reconstructible from these numbers and the assumed per-branch exchanger model. That earlier finding remains a limit on source interpretation; it is not authority to discard any individual condition. Prior independent checks are `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/{source-check-review,q1-thermal-cycle-review}.md`; the present recommendation comes from the images above, with those records used as navigation and context.

## Where a 30 K check may compare the wrong temperatures

For an actual counterflow exchanger, the terminal differences are `H_HX_in − T_secondary_out` and `R_HX_out − T_secondary_in`. Those are the two fluid pairs that exchange heat at opposite ends.

| Candidate comparison | Source applicability and required distinction |
|---|---|
| Blanket-He cold outlet minus whole-cycle heater inlet | A genuine local cold-terminal difference only if the quoted primary temperature is the actual exchanger outlet. Fig. 12’s cold-bank endpoint can be interpreted this way without a primary bypass. With a hot bypass and mixing, the maintained mixed return is warmer than the active exchanger outlet and cannot substitute for it. |
| PbLi hot inlet minus mixed turbine-inlet temperature | Matches the illustrated hottest-bank endpoint, but in the network the mixed turbine inlet is generally different from the actual PbLi branch outlet. Passing this difference does not prove a 30 K PbLi hot-terminal approach. In series the final PbLi secondary outlet is the turbine inlet, so the distinction disappears. |
| Divertor hot inlet minus mixed turbine inlet | Not a local exchanger terminal in the network. Fig. 12 prints divertor hot 700 °C while mixed cycle outlet is 707 °C; treating this as a local terminal would falsely imply heat crossing. The divertor branch may leave cooler than the PbLi branch and then mix. |
| Thirty kelvin on all six local terminals | An unambiguous and inspectable engineering specification if explicitly adopted. It is not uniquely established by Table III or Fig. 12; the blanket-He hot terminal and the intermediate branch endpoints are not fully given. |
| A bank-level 30 K difference plus passive local heat flow | Faithful as a limited composite-boundary diagnostic, but it leaves unspecified engineering minimum approaches on internal terminals. It cannot be relabeled as all-exchanger thermal adequacy, and is insufficient to discharge the owner’s requested choice of thermal requirements for preferred cases. |

Therefore keep the source’s two illustrated bank differences as labelled diagnostics. If a per-exchanger minimum is adopted, implement it using the actual active-stream temperatures. Do not use a mixed primary return, mixed turbine inlet or the existing hot-cap bound in place of the required local state.

## Primary return convention and pump heat

The diagrams show primary coolant circulating from reactor component to exchanger and back, but omit pumps and detailed pressure/enthalpy states. The table values are labelled reactor component inlets/outlets. A mathematically closed N-R comparison can adopt their inlet values at the lumped primary cold-return boundary, with all deposition, exchange and recovered friction inside the subsequent heat-addition leg. This convention uses the original branch accounting unchanged and specifies the maintained return explicitly. It does not assert that the original paper identifies a physical pre-pump sensor at exactly that temperature.

The source’s printed temperature spans approximately include the full exchanger duties, including friction. Using the inherited constant cp for a check:

| Loop at source flow | `flow*cp*(hot−inlet)` | Printed exchanger duty | Return inferred from hot minus full duty/C |
|---|---:|---:|---:|
| He, 3261 kg/s, cp 5193 | 1185.406 MW | 1192 MW including 141 MW friction | 385.611 °C versus printed 386 °C |
| PbLi, 26860 kg/s, cp 190 | 1464.676 MW | 1444 MW | 455.051 °C versus printed 451 °C |
| Divertor He, 283 kg/s, cp 5193 | 186.642 MW | 186 MW including 24 MW friction | 573.437 °C versus printed 573 °C |

[DERIVED] These calculations use model cp assumptions, especially PbLi 190 J/kg/K, not a recovered source equation of state. The mismatches are not numerical tolerances or permission to tune a setpoint. They show why the rounded source case must not be imposed as an exact many-variable reconstruction. They also provide no justification for subtracting recovered heat a second time from a cold-return target already defined at the aggregate-loop boundary.

**Alternative convention, if explicitly wanted:** define the supplied 573 °C as a post-pump reactor inlet, with all N divertor pump recovery deposited in an upstream pump. Then exchanger return is `573 − 9/2.5965 = 569.533795 °C`, and reactor hot temperature is `573 + (Q_delivered−9)/2.5965`. This is a different heat-location model. The current source images do not choose it. Under this convention the maximum N source load rises from 2005.037 to 2065.037 MW; the 2200 and 2300 MW leaders still fail the 700 °C hot limit. For N He the analogous recovered-heat rise is 8.326260 K. Do not silently switch between conventions as the result changes.

## Conditional N-R requirements and immediate consequences

[AGENT] Proposed explicit roles under MR-7:

| Quantity | Role |
|---|---|
| Source power and existing N partition | Supplied scenario choices; the prescribed common-load family |
| Primary total flows and cp | Existing supplied settings; no required-flow calculation becomes a pump selection |
| Returns He 659.15 K / PbLi 724.15 K / divertor 846.15 K | Newly adopted exact N-R design targets at the specified aggregate cold-return boundary; source-informed agent choice |
| Hot caps He 729.15 K / PbLi 1011.15 K / divertor 973.15 K | Existing supplied upper bounds; source nominal outlets used as assumptions, not material qualification |
| Actual hot states | Calculated from target return and delivered duty, including pump recovery once |
| UA/areas, installed ratings and prices | Existing independently supplied inventory; unchanged |
| Primary bypass, if introduced | Explicit operating control and hardware assumption requiring design review; never an unrecorded relaxation of local terminal checks |
| Minimum local approaches | Requirements awaiting the interpretation decision above; do not infer them from whichever result passes |

For N, duties at unchanged primary flows are `Q_He = 0.41164*P + 141`, `Q_PbLi = 0.56636*P`, `Q_div = 0.15*P + 29` MW. The divertor constant is supplied 20 MW deposited auxiliary heat plus 9 MW recovered pump heat. These relationships are inherited N assumptions, not Raffray’s source duty partition.

| Supplied fusion | Divertor duty | Actual hot at 573 °C return | Against 700 °C cap |
|---|---:|---:|---|
| 1835.4512830147435 MW original N | 304.317692 MW | 690.203040 °C | Pass this source-side condition |
| 2000 MW | 329.000000 MW | 699.709031 °C | Pass with 0.290969 K hot margin |
| 2200 MW | 359.000000 MW | 711.263046 °C | Fail by 11.263046 K |
| 2300 MW | 374.000000 MW | 717.040054 °C | Fail by 17.040054 K |

The exact algebraic divertor source-side upper load is 2005.036667 MW for this conditional family. It is an upper bound from the declared return/flow/hot-cap relationship, not a tested economic optimum, and passing below it still requires actual exchanger and cycle checks. He and PbLi analogous bounds are 2537.183243 and 2586.121548 MW; the divertor condition binds first. These bounds are independent of exchanger area and cycle split. Buying more exchanger area cannot repair a violated source-side temperature span at unchanged primary flow and return.

## Control and adequacy checks required before a preferred case

An existing calculation that freely derives primary hot/return temperatures from exchanger transfer does not enforce fixed N-R returns. Simply adding a post hoc equality may make almost every operating point fail without representing how the plant maintains its returns. Any control solution must be explicit, with actual exchanger-stream states and heat balances reported.

A primary hot bypass is one possible control assumption: total source flow stays supplied; only a fraction traverses the exchanger; its colder outlet mixes with bypassed hot coolant to maintain the required return. It can reduce heat transfer when the full-flow installed exchanger overcools a source. It cannot cure `H_required > H_cap`, insufficient installed conductance or an actual terminal difference below an adopted minimum. The bypass fraction, active primary flow, active HX outlet and mixed return must all be distinct outputs. No blanket promise that bypass will make every point feasible is justified.

At minimum, an accepted case must show all duty removed; exact maintained return within a predeclared numerical residual tolerance; actual hot state within supplied cap; positive local temperature ordering and the adopted finite terminal requirements; fixed inventory/rating checks; complete energy accounting and positive net electricity. The tolerance verifies the solve, not physical deviation from the target. No threshold is selected to admit the previous winner. The source/thermal findings do not authorize changing equipment or costs.

## Decision and scope boundary

The N-R aggregate return convention is a defensible routine conditional modeling choice if recorded and independently reviewed. It maintains the architecture question and exposes a consequential source-side limit. Making a claim that these are mandatory temperatures of the original N family, or that the full Raffray point has been reconstructed, would change the meaning and is unsupported.

The six-terminal mapping of the source’s 30 K is genuinely unresolved. Recommend presenting one explicit decision to the owner: “For this conditional comparison, should each primary heat exchanger maintain at least 30 K at both actual terminals? That is a conservative study requirement derived from the source’s 30 K parameter; the source itself only demonstrates the bank endpoints.” If adopted, evaluate it even if the current hardware/control cannot satisfy it. If not adopted, obtain a concrete per-branch requirement before asserting practical thermal adequacy of a preferred case. Do not substitute zero or a tiny accepted residual for the missing requirement.

A strictly source-configured alternative would also change primary divertor flow, heat partition, deposited heating, recuperation and other assumptions. That would be a separately named comparison requiring explicit scope agreement, not a repair of N-R. No implementation or new source request was performed here.
