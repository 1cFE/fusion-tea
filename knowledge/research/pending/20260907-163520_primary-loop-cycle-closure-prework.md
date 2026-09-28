---
date: 2026-09-07
researcher: Codex
topic: Primary-loop and power-cycle closure for stellarator demo maturation
tags: [stellarator, primary-loop, thermal-hydraulics, power-cycle, clean-room]
research_type: domain-and-model
status: pending-review
---

# Primary-loop and power-cycle prework — model-facing clean room

**Date:** 2026-09-07. **Status:** Research draft for coordinator synthesis; no model, study, registry, or PM state changed. **Decision grade:** All proposed model forms, defaults, acceptance thresholds, scope, and effort estimates below are `[AGENT]`; source observations are evidence, not owner decisions. This is research for status-report recommendation 3, not a completed grading or an approved implementation design.

## Answer and recommended scope

A small, credible primary-loop model is feasible now. Start with a representative helium circuit that calculates coolant temperature rise, pressure losses, circulator fluid work and electricity, heat delivered to conversion, and a temperature-dependent cycle efficiency. Make the thermal operating window, pressure margin, compressor capacity, and heat-exchanger approach explicit verdicts. The strongest existing source supplies all the quantities needed for an independent check at a published EU DEMO loop point. It does not supply Stellaris's plant layout or a validated off-design transfer law.

The minimum useful increment can advance physical depth (R7/R8 P) without completing structural/cost depth (S). Pump, piping, and heat-exchanger children only earn structural credit when their counts, sizes, and costs have explicit ownership. The existing primary-coolant cost decreases when pumping reduces net electrical output; leaving that formula in place must be recorded as a cost limitation, and a pipe-diameter or loop-count optimum must not be advertised until the changed equipment is priced or bounded.

The owner already corrected the historical scope reading: a real loop calculation needs no reopening of WI-033 (`.project/concepts/stellarator-demo-maturation.md:141`). WI-033's rejected fraction form remains a useful warning: the same pumping fraction across changing geometry is not a substitute for a flow/pressure calculation. Anchor A is historical evidence, with no reproduction obligation (`:132`).

## Current seams and consequences

| Surface | Verified current behavior | Consequence for implementation |
|---|---|---|
| `models/designs/stellarator_09/stellarator_plant.sysml:720` | `eta_th=0.333`; comment calls it steam-cycle efficiency | The published paper assumes simple 1/3 conversion and does not identify a cycle. Correct source wording when touching this attribute. |
| `models/designs/stellarator_09/stellarator_plant.sysml:723` | `eta_p=0.5`, described as pumping-power capture efficiency | This is recovered heat per electrical pump MW, not circulator isentropic efficiency. It cannot be reused as compressor efficiency. |
| `models/designs/stellarator_09/stellarator_plant.sysml:726` | `p_pump=195 MW` held, settable, with historical ~130 MW lower comparator | Retain this as a named historical comparison arm; replace the live source with loop electricity only after defining what the loop includes. |
| `models/designs/generic_mfe/mfe_plant.sysml:382`, `:460` | Three scalar attributes feed the power-balance calc | A clean insertion seam exists, but the new thermal and work outputs need distinct meaning. |
| `models/library/analyses/mfe_power_balance.sysml:121` | `p_th = mn*p_neutron + p_alpha + p_input + eta_p*p_pump` | Pump heat is already included once. A new IHX duty that includes pump heat must not also receive this addition. |
| `models/library/analyses/mfe_power_balance.sysml:126`, `:140` | Gross generation is `eta_th*p_th`; recirculation subtracts full `p_pump` plus subsystem fraction, heating wall plug, cryo and other loads | Primary electric demand belongs here once. Secondary-cycle compressors/feed pumps belong inside net cycle efficiency. |
| `models/designs/generic_mfe/mfe_plant.sysml:95`, `:700` | Turbine is a part; coolant is an aggregate calc, not a pump/pipe/IHX assembly | Adding scalar calculations alone leaves structural depth shallow. |
| `models/library/analyses/mfe_account_costs.sysml:526` | Coolant cost = primary base × plant net MW / 1000 + intermediate base × (plant thermal MW / 3500)^0.55 | At fixed heat, poorer circulation lowers the primary account by reducing net MW. This is an empirical plant-size cost proxy, not the cost of the circuit being studied. |
| `models/designs/generic_mfe/mfe_plant.sysml:593`, `:603` | Turbine cost uses thermal-electric MW; heat-rejection cost uses total thermal MW | Physical rejected heat should be a new published channel. Reusing the old rate on a new rejected-heat basis requires a rebase; changing the operand alone misapplies its calibration. |
| `/home/reid/1cfe/1costingfe/src/costingfe/defaults.py:577` at `02543850089be175ea7c28b92a8b2a4184e1637e` | Cycle presets carry three fields only: efficiency, turbine rate, heat-rejection rate | Existing Rankine/sCO2 comparison is a preset comparison. It has no primary-loop or IHX dependency. |

The historical materiality is supported by the status report and the closed p-pump-basis goal, not recomputed at current tip here. A fresh implementation study must publish its own baseline and no-change reconstruction before attributing differences. The newer evidence-status research confirms that all three upstream numeric-evidence repairs merged on 2026-09-06, and the current burn-control study uses repaired TEAx and evidence schema v3 with its heating and sustainment outputs persisted. The remaining 75 failures are downstream publication-contract/signature coverage across seven exporters; executor-revision capture is a separate bookkeeping gap. Neither reopens the numeric projection defect. Source: `.project/research/20260907-161438_numeric-evidence-merge-and-demo-follow-through.md`, read fully for this update.

## Source readiness and limitations

The sources below are admissible for model-facing work. No sealed PDF, barred Helios/Waganer/Araiinejad artifact, or concept09 analysis was opened. Registered Cismondi and Moscato extracts were checked for ARIES-CS matches; none. Stellaris raw PDF is explicitly admissible under PROTOCOL. The selected generic PROCESS pages and power source have no `ARIES` matches in web-find checks. NASA, NIST, and Sandia sources are generic thermodynamics/property/software references. Search results for unrelated fusion designs were not followed.

### A. Stellaris: useful local boundary, not a complete circuit

The authoritative raw PDF, p.16, §2.7 and Fig.27, gives helium at 8 MPa and 350°C entering the plasma-facing part of the first wall; its computed outlet remains below 370°C. It explicitly excludes the other two sides of the module. Fig.27 gives roughly one-metre channels and conceptual square channel geometry. Those temperatures must not be promoted into a complete-blanket outlet or cycle hot-side temperature. The paper names HCLL as the precedent for this local cooling design. Its conclusion lists blanket thermal-stress analysis and pumping estimates as future work (raw PDF p.31). The earlier approved WI-031 research already verified that its 1/3 conversion is a simple assumption and that it names no cycle (`knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md`, §2).

Local authority: `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf`. The PDF text of pp.3,16–17,31 is the authority for these claims; extracted tables are not an independent witness. Confidence: high for what the paper modeled, low for transfer to a full primary circuit. Missing: blanket flow routing, loop count, channel count, pipe route, blanket total coolant rise, component losses, compressor specification, and an actual PCS choice.

### B. Moscato: the strongest executable comparison

Authority: registered `knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/output.md`, plus `raw.pdf` pp.5–7. PDF pp.6–7 were rendered and visually checked in this session. Original source URL: https://scipub.euro-fusion.org/wp-content/uploads/eurofusion/WPBOPCPR18_20276_submitted.pdf (registered source; read locally, not refetched today).

| Quantity | Published value or derived check | Locator | Confidence and applicability |
|---|---|---|---|
| Coolant/pressure | Helium, 8 MPa | output:79, PDF p.5 | High for DEMO reference; pressure alone does not establish Stellaris equivalence. |
| Blanket temperatures | 300→500°C, FW and breeder in series | output:79 | High for old HCPB configuration; not Stellaris data. |
| Blanket source heat / total flow | 2101.7 MW / 2025.7 kg/s | output:81 | High published design values. Implied average cp = 5.1876 kJ/(kg K), a useful independent energy-balance check. |
| Circuit count | 3 inboard + 6 outboard loops | output:89–91 | High for DEMO; do not impose tokamak inboard/outboard structure on Stellaris. |
| Equipment per loop | Two compressors, one IHX, one hot and one cold leg | output Table1:105–113, PDF p.6 | High for that layout. Compressors share duty; they do not each receive total loop flow. |
| Old total loss, IB / OB | (214+62+87.9)=363.9 kPa / (174+56.6+85.1)=315.7 kPa | output:151–153; PDF p.6 Table3 | High arithmetic. Separate blanket, external pipe, and IHX contributions. |
| Circulator unit power, IB / OB | 6.8 / 7.5 MW | output:154; PDF p.6 Table3 | High published values; wording alone does not resolve motor-electrical versus fluid/shaft boundary. |
| Old total circulation | 3×2×6.8 + 6×2×7.5 = 130.8 MW, 6.22% of blanket source heat | Previous rows; WI-033 verification record §3 | Medium derived; only an external check, never the implementation formula. |
| IHX duty per loop, IB / OB | 208.1 / 267.8 MW | output Table2:128; PDF p.6 | High published. Whole IHX duty = 2231.1 MW. |
| IHX cold-end helium, IB / OB | 287.7 / 289.3°C | output Table2:129; PDF p.6 | High; it is colder than the 300°C blanket inlet, consistent with subsequent compression heating. |
| IHX secondary temperatures | HITEC salt 270→465°C | output:121 and Table2:130 | High for DEMO's intermediate storage circuit, not a steady stellarator requirement. |
| IHX heat-transfer surface | ~87300 m² total | output:141 | Source warns of tritium permeation consequence; cannot freely make the approach temperature vanish. |
| External pipe layout | ~4 km, hot DN1300/cold DN1100, hot wall up to 65 mm | output:99–103, PDF pp.5–6 | High nominal design figures. DN is not an exact hydraulic bore; total route length is not one circuit's serial length. |
| Near-term changes | 8 homogeneous loops; outlet ~520°C | output:158; PDF pp.6–7 | New configuration, not an uncertainty bar on an unchanged circuit. |
| Near-term losses | Blanket IB/OB 156/107 kPa, external IB/OB 44.6/93.6 kPa; IHX STHE/CWHE 63.1/33.7 kPa | raw PDF p.7 Table4 only | High visual read; each parallel path totals 263.7 kPa for STHE or 234.3 kPa for CWHE. Do not add IB and OB drops in series. |
| Near-term unit circulation | 5.9 MW STHE / 5.2 MW CWHE | raw PDF p.7 Table4 | High visual read. 16 units give 94.4/83.2 MW using the retained two-compressor count, as WI-033 recorded. |

Two source traps matter. Table2 actually prints the IHX pressure-drop unit as MPa; Table3 prints the same 87.9/85.1 numbers as kPa. The physically consistent table is Table3: 87.9 MPa cannot be a pressure loss in the stated 8 MPa loop. This is a source-table inconsistency, not an extraction correction. Table4's body is absent from the registered markdown, so all its values must cite the raw page.

An independent energy check is promising: total IHX duty minus blanket source heat is 2231.1−2101.7=129.4 MW, close to 130.8 MW total stated circulator power (1.4 MW difference, 0.06% of IHX duty). `[AGENT inference]` This strongly supports including circulator heat in the hot loop, rather than treating all circulation work as an external heat loss. It does not determine motor efficiency or justify a precise calibration without resolving circuit duty splits and source rounding.

### C. Cismondi: why transfer is plausible, and why percentages are weak

Registered source `knowledge/sources/progress_in_eu_breeding_blanket_design_and_integration/output.md:172` explicitly describes HCPB PHTS as representative of HCLL. At `:174` it gives ~150 MW helium pumping at 2389 MW blanket deposition and the pipe-size/layout lever (~9 km toward ~3 km with larger piping). This is a conceptual unoptimized arrangement the authors expected to improve. Original URL: https://scipub.euro-fusion.org/wp-content/uploads/eurofusion/WPPMICPR17_17709_submitted-4.pdf. Confidence: high for reported design statements; medium for transferring circuit class; low for transferring a constant percentage to geometry sweeps.

DI-008's amendment must survive capture: ~1% plant circulation comes from a mixed He/LiPb design; the ~2% number was divertor-relative, not plant-relative. The helium-primary blanket evidence is roughly 4–6%, but this is neither a physical feasibility bound nor a universal coolant penalty. No DI amendment is performed here.

### D. Public primary engineering/code sources

NASA gives the ideal-gas compressor specific-work relation with compressor efficiency, `w = cp*T_in*(r^((gamma−1)/gamma)−1)/eta_is`. It supports the equation below, not the choice of efficiency or a particular helium compressor. [NASA compressor thermodynamics](https://www.grc.nasa.gov/www/k-12/airplane/compth.html), accessed 2026-09-07.

NIST's helium gas table gives cp about 20.786 J/(mol K); using molecular mass 4.002602 g/mol gives about 5193 J/(kg K). Treat this as the ideal-gas approximation. An 8 MPa property check remains useful before setting model tolerances; the paper-derived 5187.6 value differs by roughly 0.1%. [NIST JANAF helium](https://janaf.nist.gov/tables/He-001.html), [NIST helium WebBook](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7440597&Mask=1), accessed 2026-09-07 (JANAF page opened; molecular-weight entry from primary-site search).

PROCESS separates mechanical primary pumping, electrical pump demand/losses, heat deposited in each cooled component, and conversion. Its cycle code explicitly accounts for secondary pumping inside efficiency and excludes primary pumping from that efficiency. The Rankine correlation is `eta=0.1802*ln(T_turb/K)−0.7823−delta_eta`; the sCO2 relation is `eta=0.4347*ln(T_turb/K)−2.5043`. Both use an assumed 20 K hot-end drop. Code ranges are 657–915 K and 408–1023 K; documentation shifts endpoints by 0.15 K. Select and cite one version, and fail closed beyond it. [PROCESS power.py](https://raw.githubusercontent.com/ukaea/PROCESS/main/process/models/power.py), lines 1769–1887, accessed 2026-09-07. The code identifies an internal Harrington cycle-correlations workbook; this research has not retrieved it. These are not independently validated Stellaris cycle predictions.

A fixed published authority is now available: Kovari et al., *PROCESS: a systems code for fusion power plants—Part 2: Engineering*, FED 104 (2016), Table4, journal p.17/PDF p.9, visually inspected at `/tmp/lifetime-process-p9.png`. It prints the same two coefficient sets using `ln(T2_C+273)`, with secondary-inlet ranges 384–642°C for helium-primary Rankine and 135–750°C for sCO2, a 20°C primary/secondary approach, and divertor temperatures 150°C versus T2 respectively. The surrounding text attributes Rankine modeling to Dostal with a 0.0179 benchmark adjustment and sCO2 modeling to CCFE/industry; the low-temperature-divertor correction remains separate. The tabulated fit is the resulting correlation, so do not subtract another 0.0179 from it. [Published paper, DOI 10.1016/j.fusengdes.2016.01.007](https://scientific-publications.ukaea.uk/wp-content/uploads/Preprints/CCFE-PR1605.pdf). Use the printed fit literally, or select the current Kelvin implementation deliberately: `T2_C+273` and physically converted `T2_K=T2_C+273.15` are different numerical contracts. Do not combine the paper's Celsius endpoints with current-code evaluation without recording the conversion/version choice. The literal 273 is a fit convention, not a replacement for physical Celsius-to-kelvin conversion elsewhere.

The documented steam treatment carries a low-temperature divertor penalty; the sCO2 branch assumes divertor heat at the turbine-side temperature. These are different heat assumptions. Applying both to an undifferentiated total-heat number creates an unfair cycle comparison. [PROCESS power requirements](https://ukaea.github.io/PROCESS/eng-models/power-requirements/), §§ Plant thermal efficiency and power production, accessed 2026-09-07.

PROCESS also provides component-level flow/loss methods and an enthalpy-based circulation calculation. Its built-in feedback correction has a particular temperature/heat boundary; copy neither that denominator nor its pressure convention without re-deriving the local circuit. The source explicitly distinguishes blanket-inlet pressure from pump-inlet pressure in alternative models. [PROCESS blanket library](https://ukaea.github.io/PROCESS/source/reference/process/models/blankets/blanket_library/), `coolant_pumping_power`, and [HCPB source](https://ukaea.github.io/PROCESS/source/reference/process/models/blankets/hcpb/), mechanical-with-pressure-drop branch, accessed 2026-09-07.

For friction, Sandia exposes the Haaland model; PROCESS also exposes it but its helper uses a `radius_channel` argument in the roughness term, so blindly copying it risks a radius/diameter mismatch. Use an explicit hydraulic diameter in a re-derived implementation and verify with a known pipe case. [Sandia Aria Haaland](https://www.sandia.gov/files/sierra/Aria_Users_5_26/command_summary/ariamat_auto/Friction_Factor/Haaland.html), [PROCESS pumping helpers](https://ukaea.github.io/PROCESS/source/reference/process/models/engineering/pumping/), accessed 2026-09-07.

Readiness limitation: the new web sources and the retained PROCESS2016 PDF are not registered in this repo. Browser access worked; terminal networking could not resolve api.github.com, and the browser API commit request failed. The published PDF now supplies fixed, hashed authority for the cycle correlations; a moving `main` URL is no longer their sole basis. If using current PROCESS implementation details beyond that published table, still establish its revision/byte hash. Register the chosen source/version before implementation. No registration or author contact was attempted.

## Smallest credible model candidate

### 1. Own the heat before solving the loop

Define external reactor heat `Q_source = mn*P_neutron + P_alpha + P_heat_coupled` [MW]. This deliberately excludes recovered circulation. Split it into heat delivered to the helium blanket/FW circuit, divertor/other high-grade circuits, and unrecovered/low-grade heat. Initially an explicit partition with a bounded sensitivity is acceptable; calling every neutron, alpha, heating, and pump MW blanket heat is not.

Do not add `P_rad` on top of `P_alpha+P_heat_coupled`: in the current collapsed balance radiation and transported heat are alternate destinations of those same joules. This source ledger is a shared dependency with the divertor breadth work. If the model keeps one effective high-grade loop initially, publish that approximation and a heat-partition arm; do not claim spatial cooling coverage.

### 2. Solve a circuit with named states

Use three states: 1 = IHX outlet/compressor inlet; 2 = compressor outlet/blanket inlet; 3 = blanket outlet/IHX inlet. Inputs are blanket source heat `Q_b` [MW], loop mass flow `mdot` [kg/s], inlet target `T2` [K], compressor discharge pressure `p2` [Pa], loop geometry/loss coefficients, and separate compressor efficiency `eta_is` and drive efficiency `eta_drive`.

For a positive-flow operating point with constant cp:

```text
T3 = T2 + 1e6*Q_b/(mdot*cp)
p1 = p2 - dp_loop
r = p2/p1
T1 = T2 / (1 + (r^((gamma-1)/gamma)-1)/eta_is)
W_fluid = mdot*cp*(T2-T1)/1e6
P_loop_electric = W_fluid/eta_drive
Q_IHX = Q_b + W_fluid - Q_loop_loss
P_drive_loss = P_loop_electric - W_fluid
```

This form holds the blanket-inlet temperature through the secondary-side cooling/control boundary and computes the compressor-inlet temperature needed to achieve it. The IHX must be capable of that temperature; the state equation is not evidence of a feasible heat exchanger. For a cold-side boundary held at T1 instead, compute T2 from compression and T3 from the blanket rise; choose one mode before implementation, not independent inputs for all three temperatures.

The closed energy check is `Q_IHX + Q_loop_loss + P_drive_loss = Q_b + P_loop_electric`. If fraction `chi` of drive loss enters a recoverable hot circuit, add `chi*P_drive_loss` to that circuit and subtract it from external loss. Keep that recovery fraction separate from isentropic efficiency. In this candidate, compressor inefficiency largely heats the fluid; only drive losses and explicit external loop loss leave the modeled primary fluid.

**Code-generation dependency order:** external source heat and chosen flow determine T3; nominal component density evaluated from known T2/T3 and nominal circuit pressure determines pressure loss; pressure loss and held T2 determine T1 and fluid/electric work; source heat plus work determines IHX duty; heat duty and the resulting hot temperature determine cycle output. There is no edge from the final `p_th` back to pumping or mass flow. Do not evaluate an IHX loss density from the yet-unknown T1 in this first approximation; use and name its nominal reference state. A more precise state-dependent calculation would need an analytic closure or an explicit inner solve, not a hidden cycle in the SysML calc graph. Similarly, a sized-flow mode uses the blanket-only relation `mdot=1e6*Q_b/(cp*DeltaT_blanket)`; using the pump-inclusive IHX duty in that same relation would introduce spurious feedback and the wrong temperature span.

Primary pressure loss is a sum along one hydraulic path, not a sum across parallel branches:

```text
A_flow = N_parallel*pi*D_h^2/4                 # round-channel equivalent [m²]
v = mdot/(rho*A_flow)                         # [m/s]
Re = rho*v*D_h/mu                            # dimensionless
dp_component = (f_D*L/D_h + sum(K))*rho*v^2/2 # [Pa]
dp_loop = dp_blanket + dp_hot_pipe + dp_IHX + dp_cold_pipe
```

For initial P-depth scope, measured/design nominal component resistance can replace unknown small-channel detail: `dp = dp_ref*(mdot/mdot_ref)^2*(rho_ref/rho)`, explicitly a constant-loss-coefficient approximation about a reference layout. Each of blanket, piping, and IHX retains its own resistance. This computes loss from flow and is different from assuming pumping proportional to thermal power. Use modest flow excursions with a sensitivity to the resistance law until more geometry is sourced. A broad R/a extrapolation is not warranted merely because the nominal point matches.

Where pipe geometry is known, use Darcy/Haaland with the diameter convention stated: `f_D = [-1.8 log10((eps/(3.7*D_h))^1.11 + 6.9/Re)]^-2` in fully developed turbulent flow. A minimum implementation can reject transition/laminar points instead of inventing continuity outside its selected regime. Ideal gas `rho=p/(R_He*T)` and constant cp are candidate approximations; use segment-mean temperatures and nominal pressure, and bound the error when pressure drop is small relative to absolute pressure. A validated property package/table can replace these without changing state ownership.

### 3. Make conversion conditional on the heat source

The first cycle increment should use one documented temperature-dependent Rankine correlation, or a small verified property-based Rankine model if the temperature domain requires it. sCO2 can be a second arm after matching the heat partition and sink assumptions. Export turbine-side hot temperature, cycle efficiency, gross electricity, internal cycle work convention, external primary pumping, net electricity, and rejected heat.

Use `T_turb_hot <= T3−DeltaT_hot_min`; if there is a real intermediate salt loop, include both exchanger approaches, not a single inherited 20 K step. A counterflow IHX feasibility check needs positive hot- and cold-end approaches. With specified secondary inlet/outlet temperatures, `LMTD=(dT_hot−dT_cold)/ln(dT_hot/dT_cold)` and `UA_required=Q_IHX/LMTD` [MW/K]. A fixed/maximum UA or a priced area makes the approach resist design changes. Without UA, pin the source approach and report the exchanger as a bounded assumption.

`P_cycle_net = eta_cycle_net * Q_to_cycle` already includes cycle internal compressors/feed pumps. The candidate's plant-gross channel means cycle-net power before external plant auxiliaries, not gross generator-terminal output; its name and comparison mapping must carry that distinction. Plant net subtracts primary circulation and other external electric demand once. `Q_reject_cycle = Q_to_cycle−P_cycle_net`; low-grade and motor losses join the total rejection separately.

An illustrative code-correlation calculation, not a plant prediction: at a 500°C blanket outlet and 20 K hot approach, zero divertor penalty gives Rankine 41.14% versus sCO2 37.53%; at 520°C, 41.61% versus 38.67%. The upstream unconditional 47% sCO2 preset therefore cannot be assumed valid at the same temperatures. Applying the Rankine fit to Stellaris's local <370°C FW outlet would be below its fit domain. This does not determine which cycle is better for the eventual plant; it demonstrates why temperature and heat-grade compatibility matter.

### 4. Domain and feasibility conditions

All temperatures in calculations are kelvin; pressure is absolute Pa; thermal/electrical power channels are named and in MW; viscosity is Pa·s; cp is J/(kg K); flow is kg/s. Required domains are positive cp, pressure and active flow; `p2>dp_loop>=0`; `0<eta_is,eta_drive<=1`; nonnegative source heat; valid material/coolant temperature windows; allowed Reynolds and Mach regimes; positive IHX approaches; allowed cycle-correlation temperature and `0<=eta_cycle<1`. Define a zero-source/no-flow mathematical case rather than dividing by zero; it does not represent maintenance shutdown, whose decay heat, cooling, cryogenics and imported electricity need separate duties. Pin permissible compressor pressure ratio, rated flow/work and allowable outlet/material temperatures before optimization. Availability integrates operating energy over time; it does not derate the online flow, pump, or heat-exchanger capacity needed at full power.

Bulk helium temperature alone does not verify EUROFER metal temperature. A first-wall thermal resistance/film calculation needs local wall heat flux, channel hydraulic geometry, conductivity and a transfer coefficient or correlation. The first P3 claim should say whether it checks a coolant operating window only or a material limit. Do not name a coolant-outlet constraint as a metal-temperature fence.

## Options, tradeoffs, and work boundaries

| Option | What it answers | What stays limited | Estimated scope `[AGENT]` |
|---|---|---|---|
| Bound existing held assumptions | How much headline power/cost moves across documented circulation and cycle scenarios | No flow or temperature feedback; no R7 physical closure | One bounded study after publication contract is ready; useful fallback if design transfer remains unresolved. |
| Representative circuit + temperature-compatible cycle | Whether a heat/flow operating point can be cooled and converted within stated loop capacity and temperature limits | Plant layout and equipment costing remain approximate; no unrestricted size optimization | Recommended first goal: source/contract round, model+integration round, then checked study. Roughly 2–4 focused engineering sessions plus review, depending on property/codegen support. |
| Pump/piping/IHX design and cost assembly | Layout/diameter/loop-count tradeoffs with power and equipment consequences | Detailed transient/safety licensing analysis outside conceptual-design scope | Follow-on S3 effort: explicit component sourcing and sizing; roughly 3–6 additional sessions, with unit-cost evidence the largest uncertainty. |
| Full thermal-cycle optimizer/CFD | Detailed cycle topology, recuperators, turbomachinery and thermal hydraulics | Much larger parameter and validation burden | Not needed for the first credible seam closure; would consume the goal on another systems-code implementation. |

The sizing/cost assembly should have a primary-system parent and explicit circulator, hot/cold pipe/manifold, and IHX children. Counts belong to the assembly; each component owns physical capacity and its cost law. Pipe cost must respond to length, bore, pressure-rated wall and material; pump cost to installed unit capacity and count; IHX cost to duty/area/material/pressure. No admissible source read here gives enough current equipment prices to set those rates confidently. Retaining the upstream aggregate as an explicitly bounded estimate is acceptable while seeking rates, but the aggregate must not coexist with fully counted replacement children in CAS22.

## Acceptance cases and study design

1. **Published thermal check.** Recover 2101.7 MW at 2025.7 kg/s and 200 K rise using a cp/property choice justified independently. With ideal helium cp≈5193, expected discrepancy is around 0.1%, not an excuse to fit cp to every case.
2. **Published hydraulic bookkeeping.** Old reference losses: 363.9/315.7 kPa. Near-term STHE/CWHE paths: 263.7/234.3 kPa. Verify serial versus parallel composition independently; no whole-plant-flow-per-pump error.
3. **Published work and heat.** Reconstruct 130.8 MW total compressor nameplate/duty figure and 2231.1 MW total IHX duty from counts. Compare calculated work only after defining the source boundary and compressor efficiency. Do not use the same number both to fit an efficiency and to claim validation. Report the 129.4 MW extra IHX heat as a consistency check with the 1.4 MW residual.
4. **Thermodynamic unit tests.** Zero pressure drop gives zero compressor work; reducing drive efficiency increases electricity without changing fluid work under the defined boundary; compressor heating and motor loss sum to electric input; high-grade source and recovered pump heat counted once; cycle internals subtracted once.
5. **Off-design physics.** At fixed loop geometry, larger mass flow lowers blanket temperature rise and raises pressure/work demand; at fixed flow, larger blanket load raises outlet temperature. Larger piping lowers its pressure-drop contribution, not blanket/IHX loss. Larger area or more loops must meet declared structural/cost or bound consequences before being an optimizer lever.
6. **Failures as outputs.** Unphysical pressure, nonpositive active flow, temperature/approach violations, compressor overload and fit-domain failures produce explicit excluded/violated cases. No extrapolated efficiency silently clamped to a plausible number.
7. **Package/study publication.** Every new heat/work/temperature/loss output must be nonblank and independently checked in the exported record. Pin model/package/source data/executor; run the relevant model and study checks. Existing historical records remain comparisons at their own pins.

Suggested first study holds the selected feasible plasma/geometry point fixed, compares the historical 195 MW / 0.333 assumption with the new loop baseline, then varies independent engineering levers. Use flow (e.g. 0.8/1.0/1.2 of reference), component-loss uncertainty, inlet temperature, and IHX approach within validated bounds. These example multipliers are `[AGENT]` study design, not sourced operating limits. Include separate old/near-term layout scenarios from Moscato rather than treating their component values as interchangeable random draws. Report temperature, work, net power and validity for each point; add a matched-heat cycle arm only after resolving the low-grade heat partition. The eventual geometry transfer study should change R/a together with loop routing/count/length assumptions and display the mapping, rather than hide a constant loop behind a geometry sweep.

Practical completion criterion proposal: at least one sourced reference circuit closes mass/heat/work checks; design changes move primary electrical demand and conversion through stated equations; every evaluated point has domain and capacity verdicts; a small independently checked study distinguishes thermal/hydraulic limitations from cost limitations. R7/R8 grades are assigned by the fresh grader, not this research.

## Dependencies and remaining research

- Register/pin the generic NASA/NIST/PROCESS references through the native source seam; retain local PDF page witnesses and source-table discrepancy in citations.
- Choose the Stellaris representative-loop topology and heat partition explicitly. The current source set can establish a reasonable envelope, not a uniquely determined plant design. This is a modeling assumption to review, not a missing source number to hallucinate.
- Resolve compressor unit power boundary and nominal efficiency from the referenced Moscato preliminary-design paper or another clean primary circulator design source. The published thermal checks already narrow what is consistent; motor efficiency remains a separate parameter.
- Check helium cp/rho/viscosity against a property authority across the chosen pressure/temperature window; settle whether constant properties are adequate before setting quantitative validation tolerance.
- Choose the cycle authority and valid temperature interval, including low-grade divertor treatment, exchanger count, cold-side sink, and whether a fitted cycle penalty is inherited or newly bounded.
- For S3, obtain current pump/pipe/IHX component cost sources and avoid double-counting the upstream coolant subtotal. Until then keep equipment variables bounded and refrain from economic optimum claims over unpriced layout choices.
- Coordinate heat ownership with divertor/fuel-cycle breadth research and geometry transfer with WI-044. Current v3 numeric persistence is repaired; new studies must adopt the shared required-channel contract, while the seven historical exporter adapters and general executor-revision capture need their separate follow-through. Those publication tasks do not prevent work on the physics/source contract.

## Proposed insight candidates — no DI IDs allocated

1. **Primary-loop work and recoverable heat need separate boundaries.** Context: full electric circulator demand is a parasitic while fluid work enters loop heat; motor losses need their own recovery assumption. Model implication: publish fluid work, electric draw and recovered heat independently. Analysis implication: zero/low pumping fractions cannot be compared without heat and denominator definitions. Refines the application of DI-008; it does not replace its historical source correction.
2. **Cycle independence is conditional on fixed primary temperatures and heat duty.** Context: DI-007 accurately describes the three-field preset and the separation of secondary compressor work. A physical IHX/cycle model can change primary temperature requirements and thus flow/pumping. Model implication: keep the existing preset claim scoped to the old model; permit only explicit thermal-interface dependencies in the new one. Analysis implication: cycle arms share the primary circuit only when their boundary conditions are actually equal. Proposed refinement, not a contradiction requiring silent DI replacement.
3. **Stellaris's published coolant outlet is a local first-wall result.** Context: <370°C applies to the modeled plasma-facing segment at 350°C inlet, not the complete breeder loop. Model implication: source complete-loop temperatures separately or label their transfer as an assumption. Analysis implication: a high-efficiency cycle cannot be justified by that local temperature statement.
4. **Helium-circuit architecture changes pumping by changing hydraulic losses.** Context: Moscato's distinct circuit designs change piping/IHX loss, outlet temperature, loop count, and unit power. Model implication: component resistance and capacity respond to flow and architecture; percentage ranges are checks. Analysis implication: a 4–6% envelope is not a plant-wide physical law or a geometry scaling exponent.
5. **A coolant cost tied to net electricity cannot price hydraulic design choices.** Context: the current primary coolant proxy falls when circulation losses rise. Model implication: physical loop design needs equipment costs or explicit bounds. Analysis implication: a lower calculated LCOE along an unpriced pipe/loop axis is model incompleteness, not an economic result.

## Focused handoff file list

Essential full reads for a successor: `.claude/commands/research.md`; `.claude/skills/source-traceability/SKILL.md`; `knowledge/holdout/aries-cs/PROTOCOL.md`; `.project/reports/2026-09-07-1549-status-report.md`; `.project/concepts/stellarator-demo-maturation.md`; `models/library/analyses/mfe_power_balance.sysml`; `knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/output.md` plus raw PDF pp.5–7; `work/completed/20260828_WI-033_p-pump-rebase/spec.md` and `verification_record.md`; `knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md`; `knowledge/KNOWLEDGE.md` DI-007 and DI-008 including its amendment.

Cited excerpts rather than entire-file requests: `.project/backlog/epic_stellarator_mbse_demo.md` criterion/Item10 context; `work/orchestration/goals/p-pump-basis/trail.md` § Goal close and pressure/fraction derivation at the C-001 checkpoint; `models/designs/stellarator_09/stellarator_plant.sysml:356`, `:720`, `:994`; `models/designs/generic_mfe/mfe_plant.sysml:95`, `:382`, `:454`, `:593`, `:700`; `models/library/analyses/mfe_account_costs.sysml:526`; local 1costingFE `defaults.py:577` and `layers/physics.py:290`; Cismondi output:172–174; Stellaris raw PDF pp.3,16–17,31; online PROCESS `power.py:1769` and the named pumping functions/pages above. The cited line numbers refer to the files inspected on 2026-09-07 and should be rechecked after edits.

URLs actually opened or searched are recorded in §D. Additional unsuccessful access attempts: https://api.github.com/repos/ukaea/PROCESS/commits/main (browser error; terminal DNS failure), https://ukaea.github.io/PROCESS/eng-models/pumping/ (unavailable; correct generated helper page used instead), https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/compressor-thermodynamics/ (unavailable; NASA legacy primary page found instead), https://webbook.nist.gov/cgi/cbook.cgi?ID=C7440597&Mask=1&Units=SI (unavailable; JANAF page and WebBook search used). No new source files were ingested and no authority was contacted.

### Retained verification artifacts and exact source identities

- Moscato registered `raw.pdf`: SHA256 `75f2417ab3d005af0599251e3b81739b6bcae99c1d6ac5b1cd0116d7194ffba4`. Rendered page witnesses remain at `/tmp/moscato-primary-check-6.png` (SHA256 `62b45c85a96c8ee2f65e57c520dee390a1139bb6a172780e3db6c98d08303ec8`) and `/tmp/moscato-primary-check-7.png` (SHA256 `7d16030157503849d50ddd55c7a9aa2d3db517c3805db9ce8424b8c04dfe5bb4`). Produced with `pdftoppm -f 6 -l 7 -scale-to 1600 -png`; the stable registered PDF is enough to recreate them if /tmp is cleared.
- Cismondi registered `raw.pdf`: SHA256 `dd240e3cbbec185112b1aef9340739ee7c624d3684b26d703062c89d772dffa2`.
- Stellaris authoritative KIT mirror `tmpissrtbos/raw.pdf`: SHA256 `7fd72c1242ce3a17a9c4b9a4597fcb9ff5296b942b2d8343a0b463539d8d3865`.
- All three registered-source hashes rechecked with `sha256sum` on 2026-09-07. The retained PROCESS2016 publisher PDF at `/tmp/lifetime-process-engineering.pdf` has SHA256 `f1acb2ed2d10c31bb82f4b8d6fcf5b8d7800d06d4bc465e19f305726d9f916f1`, independently rechecked here. URL: https://scientific-publications.ukaea.uk/wp-content/uploads/Preprints/CCFE-PR1605.pdf. The lifetime research agent screened its text for `aries.?cs|waganer|araiinejad|helios` with zero matches; this agent then visually inspected Table4 and adjacent fit-provenance text on `/tmp/lifetime-process-p9.png`. This is section-level admissible evidence, not a claim that keyword screening alone proves the entire paper clean. No current-code commit pin was established; use the immutable paper contract for the correlation or explicitly pin a chosen code variant.
