---
Status: complete
Created: 2026-09-22
Updated: '2026-09-22'
---

# Integrated heat/electricity design

Related Artifacts: spec.md; plan.md; ../../orchestration/goals/aries-integrated-heat-electricity/evidence/owner-brief.md

All choices in this design are [AGENT] proposals unless a source or inherited authority is identified. They remain challengeable. This file is the item's sole assumptions register.

## Architecture and chosen paths

Add `models/library/analyses/integrated_heat_electricity.sysml` and one assembly `models/designs/aries_cs_integrated/plant.sysml`. Use `exploration/aries_integrated/` for tracked staging, `build.py`, native completions, test driver, scenario inputs and the generated package `aries_integrated`. Existing files are imported or staged unchanged. Do not edit the original transfer cases or shared definitions.

The physical occurrences are plasma, source selector, fuel processing, heat deposition, blanket helium, blanket PbLi, divertor helium, primary exchangers, three compressors/two intercoolers, pressure loss, recuperator, equivalent turbine, precooler, generator/auxiliaries and plant ledger. Exposed scalar exchanges establish the steady-state behavioral interfaces. The function chain is power production → particle demand/deposition → branch heat delivery → heat exchange/conversion → plant electrical export. Capacity checks belong to the equipment occurrences consuming calculated demand.

The exchanger approximation has cycle helium pass successively through blanket-He, divertor-He and PbLi heaters. This is an explicit simplified topology, not a reproduction of Raffray Fig. 12's PbLi/divertor branch arrangement. It retains three separate source duties and primary states. The staged heating order uses lower-temperature heat first. A bounded scalar closure inside one generic native calculation solves the cycle's thermal feedback; the generated graph remains acyclic. No caller performs plant arithmetic.

## Producer choice and source partition

The selector receives calculated WI-083 fusion power, independently supplied reference fusion power and a selector restricted to 0 (source) or 1 (calculated). It requires finite, strictly positive selected fusion power before exposing that power and the mode. The unchanged `Fuel Cycle Flows` definition divides its required breeding ratio by burn rate; therefore zero selected fusion power is outside this integrated assembly's domain even though the upstream plasma component permits it. Both fuel and heat bind the selector's exposed output. The unselected calculated producer may still evaluate because the graph is eager; invalid unused plasma inputs can therefore refuse either mode. This runtime limitation must be recorded rather than claiming lazy mode isolation.

Nominal partition: neutron power `N=0.8*P`, charged power `A=0.2*P`, multiplied neutron heat `M*N`, blanket deposition `M*N + f_rad*A`, divertor deposition `(1-f_rad)*A + H`, and separately exposed other sink initially zero. Here `H` is supplied deposited auxiliary heat. Split blanket deposition into helium fraction `f_He` and remaining PbLi. A supplied inter-coolant transfer `X=x*P` is owned once and enters PbLi with minus and He with plus. Reuse `Coolant Branch Heat` for both branches. Divertor duty adds its recovered friction once. Expose nuclear multiplication gain `(M-1)*N` explicitly; it is physical source energy additional to fusion power, not a disappearing ledger residual. No alpha loss is counted twice: all charged energy is allocated by this simplified deposition model, whose confinement/radiation transport is unverified.

The separate Raffray accounting scenario selects supplied pre-exchange depositions 940/1555 MW, exchange 111 MW and He friction 141 MW, reproducing WI-086 boundary accounting. Its divertor deposition is an explicitly assumed separate input, not derived from the 2496-MW blanket total. Expose its implied source-energy mismatch against `P + multiplication_gain + H` rather than forcing closure. This scenario is the literal source-accounting diagnostic; it cannot independently validate the nominal partition law.

## Interface and variable-role contract

All powers and heat duties are MW, all temperatures K, pressures MPa, mass flow kg/s, cp J/(kg K), UA MW/K, particle rates atoms/s. Heat/work are positive in their named direction; residuals and net export are signed. The implementation uses documented Real interfaces consistent with the existing components.

| Owner → consumer | Interface meaning | Role / sign / provenance |
|---|---|---|
| Imported plasma → selector | Calculated fusion power | Calculated MW, nonnegative; unchanged WI-083 |
| Selector → fuel and deposition | Selected fusion power and producer code | Calculated strictly positive MW / code; source value chosen only in explicit source mode |
| Fuel → processing and auxiliaries | Exhaust demand | Calculated atoms/s; unchanged fuel balance; processing electrical law assumed |
| Deposition → three coolant branches | Separate deposited heat; sole inter-coolant exchange | Calculated MW in nominal mode; supplied source reconstruction in literal heat mode |
| Pumps → branches and electricity | Electrical demand and recovered friction | Independently chosen MW and fraction; recovered fraction in [0,1], remainder losses |
| Branches → thermal closure | Available heat | Calculated nonnegative MW; source accounting retained separately |
| Primary hardware → closure | Selected flow, cp, UA, bulk hot-temperature limit | Chosen kg/s, J/(kg K), MW/K, K; no inferred resizing |
| Cycle hardware → compressors/closure | Selected flow, ratios, pressure, efficiencies | Chosen values; ratios individually exposed; no rebalancing |
| Closure → turbine, recuperator and heater ledger | Calculated turbine inlet, actual branch transfers, primary/secondary temperatures, unmet heat | Calculated state; positive heat into cycle; unmet nonnegative |
| Turbine/compressors → generator | Produced shaft work and compression demand | Calculated MW; compression debited before generation once |
| Generator/auxiliaries → plant ledger | Electrical production, each auxiliary demand, net export | Calculated MW; signed net permitted |
| Ratings → capacity screens | Independently offered component capacities | Chosen MW or atoms/s; graph exposes demand, margin and definedness |

Every cross-part consumer binds producer EXPOSE attributes. Local input names differ from owner attributes. Definitions contain calculations; case files contain choices and wiring. A numeric flag uses 1=supported/true, 0=unsupported/false, never a fabricated passing value for unavailable science.

## Heat-driven recuperated cycle

Reuse the three compressors, two fixed-outlet intercoolers, fractional pressure-loss and expander definitions/completions from WI-087. Their chosen input roles and domains remain unchanged. Let `Tc` be calculated last-compressor outlet, `C=mdot_cycle*cp/1e6`, and `k=1-eta_t*(1-(p_return/p_turbine)^((gamma-1)/gamma))`. Thus turbine exhaust is `k*Tt`. Repeating this coefficient relation inside the closure is a documented equation copy for the analytic dependency break, not unchanged component reuse. Actual turbine work comes from the unchanged expander driven by the solved `Tt`; check its exhaust against `k*Tt`.

Use a declared passive recuperator with an explicit bypass: `R(Tt)=Tc+eps_r*max(k*Tt-Tc,0)`. Heat recovered is `C*(R-Tc)`; exhaust after recuperation is `k*Tt-(R-Tc)`. Bypass state is graph-owned. This extends the WI-087 recuperator's domain with a real operating policy; it is a new generic calculation, not a change to that definition. It permits heat-poor scenarios without negative recuperator heat. There is no hidden active heater.

For each primary exchanger, `Ch=mdot_primary*cp_primary/1e6`, `Cmin=min(Ch,C)`, `Cr=Cmin/max(Ch,C)`, `NTU=UA/Cmin`. Counterflow effectiveness is `(1-exp(-NTU*(1-Cr)))/(1-Cr*exp(-NTU*(1-Cr)))`; use `NTU/(1+NTU)` at equal capacity rates. This is the standard constant-property counterflow energy-balance solution, adopted here as an explicit engineering approximation. Independent review must check its math and domain. `K=eps_hx*Cmin` is an actual capability calculated from chosen hardware.

At candidate cycle-heater inlet `R`, visit the three exchangers in the declared order. For exchanger i with cycle inlet `Ti`, hot bound `Li` and available source heat `Qi`, calculate `qcap_i=K_i*max(Li-Ti,0)`, `qi=min(Qi,qcap_i)`, and `Ti_next=Ti+qi/C`. The min/max express a finite capability and bypass, not sizing. The actual primary hot inlet needed for transferred heat is `Ti+qi/K_i`; its return is that hot inlet minus `qi/Ch_i`. For zero UA, transfer is zero and primary operating state is undefined; expose definedness=0, not an arbitrary temperature. The available hot-bound margin and unmet heat `Qi-qi` are outputs. If unmet heat is positive, the calculated primary state describes only the removable portion; the plant fails steady heat removal and the model makes no thermal-storage or invented heat-dump claim.

Solve `F(Tt)=C*(Tt-R(Tt))-sum(qi(R(Tt)))=0` by bounded bisection inside the typed closure, bracket `[Tc,max(Tc,L1,L2,L3)]`. With 0<k<1 and 0<=eps_r<=1, `R` is nondecreasing with slope below one. Since `K<=C`, the staged heater map remains nondecreasing and total accepted heat is nonincreasing with inlet temperature; F is strictly increasing and the bracket has opposite signs. Stop on heat residual below 1e-8 MW or an absolute temperature bracket below 1e-10 K; cap 100 iterations and refuse failure. The numerical algorithm is an operating-state solver, never a equipment-selection policy. Expose closure residual/iterations and verify monotonic/bracket assumptions at runtime.

Use the unchanged expander with solved turbine inlet. A new passive recuperator completion reports recovered heat and both outlet temperatures; compare its results with the closure state. Reuse fixed-outlet precooling to the supplied 308.15 K sink if its inlet is at least that sink; otherwise refuse this cooling-only domain. New integrated ledger permits zero cycle heat and signed net shaft without division by zero; efficiency then has definedness=0. Test zero transferred heat with positive selected fusion power and zero UA, independently of the fuel domain. Such a point may still refuse the cooling-only precooler domain; exercise the ledger's zero-heat handling directly if so, and retain the integrated refusal. WI-087's ledger requires strictly positive heat, so it is not unchanged reused over this larger domain.

## Electrical and energy ledgers

Mechanical drive architecture follows the equivalent WI-087 shaft: `Wnet=Wt-sum(Wc)`. Generated electrical export before plant auxiliaries is `G=eta_g*max(Wnet,0)`; if Wnet<0, shaft import is `-min(Wnet,0)/eta_motor`. Generator loss is `(1-eta_g)*max(Wnet,0)` and motor loss is `(1/eta_motor-1)*max(-Wnet,0)`. This explicit motor path retains negative-output operation honestly.

`Pnet=G-Pshaft_import-Pprimary_pumps-Pheat_electric-Pcryo-Pfuel-Pcontrol-Pother`. Cycle compressor work is already in Wnet and is never subtracted again. `Pheat_electric=H/eta_heat`; its unrecovered electrical loss is `Pheat_electric-H`. `Pfuel` is a fixed assumed base plus a supplied coefficient times actual tritium exhaust; both contributions are exposed. Cryo/control/other are separate supplied loads. These demands have assumption support flags, not claims of physical calculation.

Expose branch ledger residual, nuclear/deposition residual, cycle residual `Qaccepted-Qrejected-Wnet`, electrical residual and whole-plant residual. Whole-plant sink includes direct other heat, unremoved source heat (as unmet duty, explicitly not physical rejection), cycle rejection, generator/motor losses, unrecovered pump/heating losses and dissipated cryo/fuel/control/other electricity. The algebraic boundary is `Pfusion+nuclear_gain = Pnet + all_sinks`. Export/import sign is preserved. The source-accounting scenario also exposes its nonzero deposition residual separately and never declares it closed by tolerance. Ledger tolerance is from spec R7; source rounding differences are comparison residuals, not numerical tolerance adjustments.

## Single source and assumption register

Original images viewed for this design: WI-086 `evidence/raffray-p734.png`; WI-087 `evidence/raffray-p736.png` and `raffray-p737.png`; WI-088 `evidence/lyon-p716.png`. These retained post-reveal sources are authorized by the owner brief. Source values and agent assumptions below never share a scientific identity merely because they appear in the same scenario.

| ID | Basis and nominal values | Range / affected result / replacement condition |
|---|---|---|
| S1 | Lyon Table VII reference: fusion 2436 MW, gross electricity 1253 MW, thermal efficiency 43%, 1-GW-electric table basis | Comparison only except selected source-mode fusion. Calculated plasma keeps WI-083 profile values unchanged. Replace comparison only with a clearly named published configuration. |
| S2 | Raffray Table II: blanket deposition reconstruction 940/1555 MW; transfer 111 MW; He electrical pump 156 MW, recovered friction 141 MW; primary He flow 3261 kg/s; PbLi flow 26860 kg/s; He module outlet 456 C, PbLi outlet 738 C | Literal source-accounting inputs. Do not scale them and call them literal. Table's 2496-MW blanket heat differs by 1 MW from reconstructed deposition; retain residual. |
| S3 | Raffray Table III: compressor eta .89, turbine eta .93, recuperator .95, nominal total ratio 3.5, cycle pressure-loss fraction .045, cold sink 308.15 K; Fig12 divertor hot 700 C | Source-informed nominal constant-property assumptions only; independently chosen per-stage ratios 1.5182944859378311. Source max pressure and ratio remain comparison values. |
| A1 | Nominal partition M=1.16 from Raffray neutron multiplier, f_rad=.25, f_He=.38, x=.04; deposited auxiliary heating H=20 MW | M 1–1.25; fractions 0–1; x 0–.06 with nonnegative branch duty. Affects heat/net, absent transport constraints disclosed. Replace with source-qualified deposition/transport. |
| A2 | Nominal primary pump electricity He156/PbLi .01/divertor10 MW; recovered He fraction 141/156, PbLi0, divertor .9 | Pump loads 0–2x nominal, recovery 0–1. Constant at fixed chosen flow; no hydraulic law. Affects heat/electricity. Replace with pressure-drop/efficiency maps. |
| A3 | Nominal cycle flow 1400 kg/s; cp5193, gamma5/3; return pressure15/3.5 MPa; recuperator eps .80 | Flow1000–1800, eps .6–.95; diagnostic sensitivity, no machine-map claim. Literal source-input scenario uses eps .95. Chosen independently without fitting published output. |
| A4 | Primary flow He3261/PbLi26860/divertor500 kg/s; cp He5193/PbLi190 J/(kg K); UA each50 MW/K; hot bounds729.15/1011.15/973.15 K in respective He/PbLi/divertor owners | UA0–100; flow .5–1.5x; cpPbLi170–220. Supplied cp, UA and divertor flow are assumptions. Temperatures are bulk bounds inferred from nominal source outlets, not material qualification. Replace with real-fluid/HX design data. |
| A5 | Generator eta .98, motor eta .95, heating efficiency .5; cryo10 MW, fuel base5 MW plus 1e-22 MW/(atom/s) exhaust coefficient, control5 MW, other5 MW | Efficiencies .3–1 as applicable; each unmodeled load0–2x nominal. Assumed boundary laws; no optimization of unresisted choices. Replace with subsystem demand models. |
| A6 | Offered ratings: blanket He1500/PbLi1800/divertor800 MW heat duty; compressor1600 MW; turbine3500 MW; rejection2500 MW; generator1800 MW; fuel processing3e22 atoms/s | Independently chosen hypothetical scalar capacity; low/high tests at fixed demand. Support assumed for these scalar screens only; real equipment qualification absent. No cost response claimed. |
| A7 | Nominal-source-assumed uses selector0, P2436 and nominal partition; nominal-calculated uses selector1 with untouched WI-083 profiles and all other nominal choices | Two modes of one assembly. No refitting; source-dependent results retain source-conditioned label. |
| A8 | literal-Lyon-source-input uses P2436, nominal partition assumptions and source recuperator .95; literal-Raffray-accounting uses P2365, literal S2 heat mode, eps .95, H20 and separately assumed divertor deposition .15*2365+20 MW | Best literal reconstructions at their named source boundaries, not complete published plant replicas. Missing values remain A inputs. Retain unmet heat, comparison discrepancy and source-energy residual; never modify into nominal. |
| A9 | Magnet support0, breeding support0, deposition-law qualification0, hydraulic/HX material/machine-map qualification0; assumed scalar screen support1 | Native numeric outputs distinguish unsupported science from computed accounting and failed hardware. Substitute values never flip support to1. |

Nominal choices are starting scenarios, not optimized hardware. If initial execution fails a required numerical domain or leaves unmet heat, preserve that attempt and revise only a declared assumption with a reason and review of changed semantics. Changing a chosen UA/flow to create a separate sufficient-equipment case is an explicit scenario, not an automatic design policy.

## Reuse/change table

| Existing asset | Planned reuse / change |
|---|---|
| WI-083 plasma case, density/profile definitions, reaction kernel and typed integration | Stage/import unchanged; completion package-prefix rewrite plus typed interface adapter when required by stock smart regeneration; preserve original body AST and record both hashes |
| WI-085 fuel chain | Reuse exact `Fuel Cycle Flows` definition/generated behavior; new occurrence binds selector rather than fixed imported plasma. Preserve fuel assumptions, expose outputs. |
| WI-086 branch heat and dual ledger | Exact definitions and completion bodies reused for He/PbLi; new partition supplies their inputs. Divertor and full-plant ledger are additions. |
| WI-087 compressors, coolers, expander, pressure loss | Exact definitions and completion bodies reused; turbine input now solved by new closure. |
| WI-087 recuperator/ledger | Equation lineage retained; new passive bypass and zero-heat-aware ledger are additions, not unchanged reuse. |
| Offered capacity screens/constraints | Exact generic definition/completion reused for every new selected rating. |
| Existing build route | Same stock generator, handwritten completion preservation, seal and TEAx execution; add native integration snapshot/census contract. No separate Python plant implementation. |

## Verification and review questions

The review must decide whether the sequential exchanger approximation and operating closure conserve energy with fixed hardware, whether source modes retain honest source boundaries, and whether the electrical/thermal losses close without subtracting compressors/pumps twice. Check bypass, zero-UA and signed shaft behavior separately. Acceptance tests must inspect the actual generated entry keys and bindings so mode selection, chosen hardware and calculated states are distinguishable. Every advertised residual/comparison should be native, including Lyon gross/net differences and Raffray blanket source discrepancy. Unsupported states cannot pass engineering adequacy.
