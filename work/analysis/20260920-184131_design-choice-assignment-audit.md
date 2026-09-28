# Where the model chooses design quantities automatically

## Scope and governing intent

[OWNER-VERBATIM] “As soon as you start introducing ‘sizing’, then you are basically pre-defining which design parameters are ‘free’ and which are ‘derived’. this is explicitly what we wanted to avoid.” Source: September 20, 2026 conversation. [OWNER] The out-of-range field limitation should be described as a conductor-performance-model limitation.

[AGENT] Read-only focused audit of canonical model bindings and current executable calculations for magnets, cooling, facilities, fuel processing/inventory, heating, cryogenics and conversion. This is not a complete inventory of every fixed input/output assignment, nor a numerical rerun. No held-out reference values inform this report. The distinction is between calculating a physical consequence, reporting a requirement, and choosing the installed design to satisfy a requirement. A directional equation is not by itself proof of an automatic adequacy assumption, but it does encode a choice of inputs and outputs.

## Summary

[AGENT] This is not isolated to current-driven winding sizing. At least three equipment families contain explicit automatic design selection: magnet winding inventory/geometry, facility storage allocation, and fuel-processing capacity. Cooling and conversion additionally fix flow from thermal duty and selected temperatures. Cryogenic and turbine costs follow calculated demand/output without independently chosen installed equipment ratings. These are different forms of fixed model assumptions and should not be counted as identical defects.

[AGENT] Other calculations preserve a demand-versus-capacity distinction: installed heating against sustainment demand; intermediate heat-exchanger required area against fixed installed area; independent magnet cavity dimensions against the calculated winding envelope. Passing the depth rubric does not establish compliance with the owner's stated modeling principle.

## Confirmed equipment selection

| Area | Encoded choice | Evidence |
| --- | --- | --- |
| Legacy winding geometry | Winding side is sqrt(coil ampere-turns / selected current density)/1000. The model explicitly removes side as an entry point. Current density becomes a design input instead of evaluating it from independently chosen geometry. | `models/library/analyses/mfe_magnet_field.sysml:90`; `models/library/cost_structure/mfe_power_core.sysml:218` |
| Field-grade winding enlargement | Selected field envelope automatically changes relative conductor quantity and effective density. The enlarged pack determines purchased tape volume. This is an additional design rule, not merely a conductor performance evaluation. | `models/library/analyses/mfe_conductor_grade.sysml:4`; `models/library/cost_structure/mfe_power_core.sysml:211` |
| Current-driven conductor inventory | Available tape current and allowed loading determine required tape count, conductor area and pack area. The selected effective density drives actual winding dimensions and inventory. The inventory multiplier leaves a degree of freedom but still requires at least the calculated inventory. | `models/library/analyses/mfe_conductor_current.sysml:39`; `models/library/cost_structure/mfe_power_core.sysml:123`; `:221`; `exploration/stellarator_e2e/generated/handwritten/mfe_conductor_current/current_driven_pack_sizing_impl.py:25` |
| Facilities | Capacity mode 1 allocates clean/buffer/storage positions from calendar demand, then computes building dimensions and cost. Mode 0 instead uses specified capacities and can report shortfalls. Therefore the choice to resize is explicit in a mode, but the selected mode still makes design decisions automatically. | `exploration/stellarator_e2e/generated/handwritten/mfe_facilities/facility_layout_impl.py:245`; `models/designs/stellarator_09/stellarator_plant.sysml:1564` |
| Fuel processing | Installed processing capacity = running D+T exhaust flow × capacity margin; margin must be at least 1 and the selected value is 1.0. Equipment cost scales from that capacity. There is no independently chosen insufficient processor rating in this formulation. | `exploration/stellarator_e2e/generated/handwritten/mfe_fuel_cycle/fuel_processing_cost_impl.py:23`; `:31`; `models/library/structure/mfe_plant_systems.sysml:540`; `models/designs/stellarator_09/stellarator_plant.sysml:1456` |

## Other fixed choices requiring separate treatment

- Primary helium flow is calculated as heat duty/(cp × selected temperature rise), then used for pumping power. That fixes a flow/temperature-rise assignment; it does not solve an arbitrary chosen pump/pipe operating point. Loop count remains an independent parameter and equipment screens can still fail. Evidence: `models/library/analyses/mfe_primary_loop.sysml:6`.
- Secondary salt flow follows heat duty and a fixed temperature window, feeding pump operation and cost. Intermediate heat-exchanger installed area remains fixed; required area is a separate comparison, so do not classify the exchanger itself as automatically enlarged. Evidence: `models/library/analyses/mfe_cooling_equipment.sysml:4`; `models/library/structure/mfe_plant_systems.sysml:239`.
- Steam flow closes the matched cycle's heat/enthalpy balance. This is operating-point selection, not a separate installed turbine/steam-generator rating checked against demand. Required conductance outputs are diagnostics. Evidence: `exploration/stellarator_e2e/generated/handwritten/mfe_matched_steam_cycle/matched_steam_cycle_impl.py:228`; component bindings at `models/designs/generic_mfe/mfe_subsystems.sysml:419,437,469`.
- Cooling-water flow similarly follows rejected heat and a selected temperature rise, including pump work. Calculated pump operation is bound to the pump part; it does not represent an independent installed rating. Evidence: `models/designs/generic_mfe/mfe_subsystems.sysml:688`; `exploration/stellarator_e2e/generated/handwritten/mfe_matched_steam_cycle/cooling_water_rejection_impl.py:43`.
- Cryogenic electrical requirement feeds aggregate cryoplant cost; turbine output feeds a power-based turbine cost. These imply demand-matched costing but do not contain detailed physical equipment sizing. Evidence: `models/library/structure/mfe_plant_systems.sysml:328,387,393`; turbine account bindings in `models/designs/generic_mfe/mfe_subsystems.sysml:609`; cost formulas at `models/library/analyses/mfe_account_costs.sysml:257,594`.
- Fuel working stocks follow flow × residence time and reserve policies. This does not choose tank hardware or compare against installed storage capacity. Lifecycle replacements follow modeled lifetime and an assumed replacement policy. Classify these as inventory/operating-policy assumptions, not automatically as hardware resizing. Evidence: `models/library/analyses/mfe_fuel_cycle.sysml:93`.

## Patterns that preserve an explicit check

- Heating: independently installed wall-plug power and efficiency produce available coupled power; a sustainment constraint checks it against demand. Evidence: `models/designs/stellarator_09/stellarator_plant.sysml:2115`.
- Heat exchanger: installed area and required area remain separate; capacity can fail rather than resizing the exchanger. Evidence: `models/library/structure/mfe_plant_systems.sysml:239`.
- Magnet casing: allocated radial space and transverse cavity width are independent. The cavity is not enlarged to fit the winding. However the winding inside it is automatically sized, so this is a mixed pattern. Evidence: `models/library/analyses/mfe_winding_pack_fit.sysml:4`.

## Implication and recommended follow-up

[AGENT] The code itself documents the architectural change: `mfe_power_core.sysml:218` says winding side stops being an entry point and becomes a consequence of current and selected current density. This predates the latest conductor sizing addition. Switching off current-driven mode therefore does not restore independently selected winding dimensions.

[AGENT] Replacing that with a different permanently fixed choice of independent inputs would not, by itself, resolve the owner's broader concern. A follow-up should inventory the physical relations, admissible variable choices, empirical validity domains, installed capacities and scenario policies separately, then make calculation direction and any automatic design selection explicit. This report does not authorize a particular solver architecture or rewrite.

[AGENT] The depth rubric measures represented detail and constraint coupling, and explicitly uses sizing language in several targets (`.project/active/demo-depth-rubric/rubric.md:99`). It does not certify preservation of selectable design variables. The 23/23 result should not be cited as evidence that this architectural requirement was met. The conductor's field validity restriction is a separate performance-model limitation; changing variable selection alone will not extend its scientific support.

## Review coverage

[AGENT] Two independent read-only code inspections covered cooling/facilities/cryogenics and fuel/heating/cycle/lifecycle. The coordinator inspected magnet equations and bindings and synthesized the distinctions above. No parser, numerical study or regression suite was run; this is a source-level architecture audit.
