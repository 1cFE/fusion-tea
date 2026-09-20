# WI-073 bounded structure proposal

Date: 2026-09-19. [AGENT] Proposed architecture only. The prototype's state choices, performance assumptions, property method and cost coverage await independent source/math review. This note approves none of them. No model or executable was changed.

## Recommendation

Keep the existing `turbine` occurrence as the CAS23 owner. Give it one state-resolved library calculation and named physical component occurrences whose properties and exchanges are tied to that calculation. The physical water circuit is closed; the executable calculation graph remains directed and acyclic. Ports describe physical exchanges and do not execute equations in the current generator.

Existing anchors: `models/designs/generic_mfe/mfe_subsystems.sysml:266` owns turbine inputs, cycle analysis and CAS23 cost; `models/library/analyses/mfe_power_cycle.sysml:4` supplies the current manual-interface precedent; `models/library/structure/mfe_interfaces.sysml:4` states port/connection execution limits; `modeling_project/MODELING_PROCESS.md:46` requires connected requirements, behavior, structure and analysis.

## Components, functions and interfaces

Add reusable component/interface definitions in the library, with the matched-cycle assembly under the existing turbine owner. Use named occurrences rather than indexed collections. The minimal proposed occurrences are `main_steam_generator`, `hp_turbine`, `reheater`, `lp_turbine`, `open_feedwater_heater`, `condenser`, `condensate_pump`, `feedwater_pump` and `generator`. HP/LP turbines and the two pumps can share reusable definitions. Each occurrence identifies its function and has actual input/output state or power properties bound to the cycle analysis; an empty part with a descriptive name would add no useful evidence.

| Component | Function and bound properties |
|---|---|
| Main steam generator | Feedwater heating/evaporation/superheating; inlet/outlet state, steam flow, heat duty and minimum temperature gap |
| HP turbine | First expansion; inlet/outlet state, total flow, extraction flow and shaft work |
| Reheater | Heat remaining steam; inlet/outlet state, remaining flow, duty and minimum gap |
| LP turbine | Final expansion; inlet/outlet state, remaining flow, shaft work and exhaust quality |
| Open feedwater heater | Mix extraction steam and pumped condensate; both inlet flows/enthalpies, outlet state and mass/energy residual |
| Condenser | Condense LP exhaust; inlet/outlet state, remaining flow and rejected heat |
| Condensate/feedwater pumps | Raise liquid pressure; inlet/outlet state, pumped flow, fluid work and electrical demand separately |
| Generator | Convert combined expansion shaft work to gross electricity; shaft input, gross output and conversion loss |

Extend `mfe_interfaces.sysml` with a water/steam stream type carrying pressure, temperature, mass flow, specific enthalpy and entropy, and a one-direction stream port. Keep quality as a component/state diagnostic with explicit applicability; it is not defined for every stream. Add shaft-power and heat-duty ports only where those exchanges are actually connected. Reuse the existing electric port. Make units explicit, including the current thermal stream's kelvin convention versus prototype Celsius.

Connect the water path through main SG → HP → reheater → LP → condenser → condensate pump → open heater → feedwater pump → main SG, with HP extraction connected separately to the open heater. Connect both turbine shaft outputs to generator inputs. The salt supply splits between main SG and reheater and returns mixed to heat transport; record and expose branch duties/flows and the shared supply/return assumptions, rather than implying serial salt heating. A connection diagram must agree with the actual split selected by physical review.

Keep cooling-water circulation and final environmental rejection under existing `heat_rejection` (CAS25), whose present scope includes circulating water (`mfe_subsystems.sysml:351`). Add the condenser/rejection thermal exchange and electric supply to its circulation pump. The condenser remains CAS23. No new subcomponent capital costs are implied: existing account pricing remains aggregate, with SG/reheater coverage explicitly unresolved until the cost-source review.

## Calculation ownership and the executable graph

Add the state-resolved manual `calc def` to the library analysis layer, and instantiate it within the matched turbine assembly. Its scalar inputs come from owned component assumptions and cooling producer EXPOSEs. Its declared scalar outputs cover named states, component duties/work/flows, losses, gross generation, cycle-pump demand and residuals. Bind component result properties from those outputs. Component-owned assumptions feed the solver; result attributes do not feed back as independent inputs. This represents a simultaneous physical solve inside one manual module rather than creating a codegen module for every physical component.

Expose cooling's available conversion heat, salt supply/return temperatures and flow at `heat_transport`, then bind turbine inputs to those attributes. Current relevant outputs are in `mfe_cooling_equipment.sysml:164,254,264`. Distinguish per-circuit flow from plant total before binding. Expose solver results at turbine level with pure aliases for downstream consumers. Keep one-hop cross-part references; no arithmetic on EXPOSE outputs in design attributes. These are the supported patterns in `.agentic-mbse/patterns/plant-idiom.md:328,399` and `modeling_project/MODELING_GUIDE.md:29,45`.

Required dependency order: source heat → primary loop → cooling equipment/energy addition → matched cycle → cooling-water rejection calculation → plant electric accounting → costs. Put the prototype's cooling-water flow/pump closure in the downstream rejection calculation if that function is retained. It consumes condenser heat and identified losses; it does not set the cycle's condenser condition through feedback. That condition remains an independently selected, reviewed design assumption.

Remove the matched-mode back-edge currently expressed by `heat_transport.cooling_cycle_argument = turbine.cycle_argument` (`mfe_plant.sysml:86`), consumed by equipment at `mfe_plant_systems.sysml:198`. Move the comparison diagnostic downstream of both producers, or bind it to an independently owned steam-temperature selection if its existing meaning is preserved. Do not substitute a solver output into that existing equipment input: equipment also produces the cycle's heat and salt state.

## Electrical and legacy contract

Expose `gross_electric`, `cycle_pump_electric`, `condenser_heat` and conversion losses distinctly. The existing gross electric port carries generator output before condensate/feedwater pump subtraction. Supply those pumps through a turbine electric-input port connected to `electric_plant.recirculating`. Supply cooling-water pumps through heat rejection's own electric input. Existing primary/salt pump demand remains owned by heat transport.

Change plant accounting to select explicit matched-cycle gross production and add each new pump demand once to recirculation. Preserve a cycle-net diagnostic separately. Feeding cycle-net efficiency into current `p_the = eta_th * p_th` and then subtracting those pumps again would double count them. Existing equations and cost routing are at `mfe_power_balance.sysml:143,157` and `mfe_plant.sysml:195`. CAS23/CAS24 gross-power cost drivers retain their declared meaning; heat rejection's inherited thermal-power cost proxy must not silently become condenser-duty pricing.

Preserve the historical fit/direct modes and their formulas under an explicit legacy route. Prefer a matched-cycle specialization/redefinition of the turbine owner so other generic MFE consumers do not acquire mandatory new state inputs. If implementation uses one manual module with a numeric mode selector instead, the branch must occur before property evaluation, with declared inactive-output semantics and mode-specific checks; multiplying invalid matched results by zero is insufficient. Existing `cycle_live` means fit-versus-held efficiency and must not silently acquire a third meaning. The legacy domain-product predicate and cycle-argument output remain legacy diagnostics, not evidence of matched-cycle validity.

## Evidence still required

This is a bounded repository inspection, not a parse/codegen prototype or independent physical approval. Implementation must probe the chosen specialization/manual-module route, verify every component-to-analysis binding and port meaning, and test strict mode handling, gross/net accounting and the acyclic dependency order. Select physical-domain constraints after source review; connect them to WI-073 requirements and executed verification evidence. The properties, efficiencies, salt split, cooling-water scenario and steam-generator cost coverage remain open on their own merits.

## Bounded codegen probe: practical route

[AGENT] Follow-up probe artifacts are under `evidence/structure-probe/`; `probe.py` generates isolated toy packages, `generation-results.json` records generation outcomes, and `execute_probe.py` supplies a deliberately trivial manual calculation. These artifacts change no canonical, staged or production package files. This is structural evidence, not a steam-property implementation or validation of the physical proposal.

The additive route generates: keep the legacy calc, add a manual matched calc with an explicit numeric enable input, and expose its primitive scalar outputs. The generated sink consumes the matched output channel, while the component's bound enthalpy and the state/pump outputs do not become entry points. The fixture has only two entry points (raw legacy input and enable). The negative literal property input is emitted as a constant arithmetic module. All real design assumptions used as independent calc inputs still need a deliberate entry-point census; output aliases do not make those assumptions disappear.

Directly retyping a turbine subtype and replacing its already-bound gross alias fails parsing with `feature-value-overriding`. A second attempted calc-type replacement also fails direction/binding conformance; that failure does not establish that every specialization shape is unsupported. It does establish that specialization is not a drop-in replacement for the current hard-bound cycle aliases. Prefer the demonstrated additive route for WI-073 rather than making structural retyping a prerequisite.

Concrete recommendation: retain `cycle_live` and the current legacy calculation contract, add `matched_cycle_enabled` defaulting to zero in the generic owner, and set it explicitly in the stellarator assembly. Put the enable branch inside the handwritten matched implementation before any property lookup or state-domain evaluation. Return documented inactive diagnostics and zero incremental pump demand when disabled; keep legacy gross selection in a small library selection calc or the same manual boundary. Preserve legacy fit outputs and checks under their original names, with explicit applicability for new checks. Do not infer inactivity from zero heat or multiply an invalid calculation by zero. Primitive scalar state outputs should remain outputs, and child component properties should bind to them rather than becoming free scalar state inputs.

The generated graph is eager: upstream producers still execute before the disabled branch. Therefore the branch cannot protect a separate upstream property module, an invalid old fit, or an invalid cooling producer. All optional property work must be inside the guarded manual module; inherited legacy inputs must retain their historically valid domain when that old fit remains on the graph. The execution probe is designed to verify disabled invalid-property handling, enabled behavior and explicit invalid-mode refusal; consult `execution-results.json` if present and `execution.log` for its actual result. The first attempt lacked the documented TEAx import path; the rerun uses the operator guide's `packages/teax-simkit` path. Production generic/historical regression and the actual turbine assembly still require separate verification.
