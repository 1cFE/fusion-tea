# T09: a nominal forward Brayton component assembly

[INHERITED: coordinator assignment, 2026-09-21] Continue the transfer experiment with an executable power-conversion increment, preserving independent flow and equipment selections. [AGENT] Implement a reduced ideal-gas helium Brayton assembly with three compression stages, two intercoolers, equivalent expansion, recuperation and heat/work accounting. The retained source supports this topology and nominal operating parameters. It does not supply enough detail to reconstruct the exact source machine or qualify equipment away from that point.

## Source evidence and unresolved structure

[AGENT] Visually inspected Raffray p736 Figs12/13 and p737 TableIII/Fig14, retained as `work/active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p736.png` and `raffray-p737.png`. This engineering case remains separate from Lyon's 2436 MW systems reference and WI-083. No upstream fusion or WI-086 heat total automatically sets cycle mass flow or delivered heat.

| Source quantity | Published value | Proposed treatment |
|---|---:|---|
| Compression stages | 3 | Three actual compressor occurrences |
| Expansion stages | 1 | One equivalent expansion occurrence; Fig13 separately depicts compressor and generator turbines, whose pressure/work split is unspecified |
| Compressor / turbine efficiency | 0.89 / 0.93 | Supplied nominal isentropic efficiencies, not off-design maps |
| Recuperator effectiveness | 0.95 | Supplied constant equal-capacity-rate effectiveness |
| Maximum cycle pressure | 15 MPa | Selected compressor discharge pressure |
| Total compression ratio | 3.5 | Selected total ratio; equal stage ratios are an agent assumption |
| Fractional cycle pressure loss | 0.045 of maximum pressure | Supplied total; its location is missing |
| Lowest cycle helium temperature | 35 C | Compressor inlet and ideal intercooler outlet boundary |
| Cycle He leaving heat exchangers | 707 C, Fig12 | Supplied turbine inlet temperature; not independently predicted |
| Cycle He entering heat exchangers | 355 C, Fig12 | Comparison-only published state, not simultaneously imposed on recuperator output |
| HX hot/cold difference | 30 C | Source context; full three-primary-stream exchanger network remains outside this increment |
| Gross / net efficiency | approximately 0.43 / 0.39 | Comparison-only values; never calculation inputs or acceptance calibration targets |

[AGENT] The source omits individual compressor ratios, intercooler approaches/losses, distribution of cycle pressure loss, generator/mechanical efficiency, split between the two drawn turbines, selected cycle mass flow and machine maps. A declared idealized forward case can proceed despite these gaps. It cannot claim exact source reproduction, independently predicted turbine inlet temperature, generator output or plant net efficiency.

## Concrete forward contract

[AGENT] Select helium flow 1000 kg/s independently of any available reactor heat. Supply cp = 5193 J/(kg K) and gamma = 5/3 as constant ideal-helium approximations already documented in `knowledge/research/pending/20260907-163520_primary-loop-cycle-closure-prework.md`, section D, with retained NASA compressor and NIST JANAF authority pointers. Their use at this temperature/pressure is an approximation, not a real-fluid property validation. New turbine and recuperator relations need focused physical review before implementation; compressor thermodynamics reuse an established equation, not an unchanged existing executable definition.

[AGENT] Supply three equal stage ratios whose product is 3.5, and restore the first two stage outlets to 308.15 K through ideal intercoolers. Assign the source's total pressure loss to one equivalent hot-side loss element, giving turbine inlet pressure `15*(1-0.045)` MPa and outlet pressure `15/3.5` MPa. This allocation is an explicit scenario assumption, not a recovered source pressure map. Compressors, coolers and expansion carry the same independently selected flow. The model must retain pressure continuity and heat/work dependencies between owners.

[AGENT] Each compressor calculates `Tout = Tin*(1+(r^((gamma-1)/gamma)-1)/etaC)` and shaft demand `mdot*cp*(Tout-Tin)`. Equivalent expansion calculates `Tout = Tin*(1-etaT*(1-(pout/pin)^((gamma-1)/gamma)))` and shaft production `mdot*cp*(Tin-Tout)`. The equivalent turbine represents combined fluid expansion, without predicting the source's separate shaft arrangement.

[AGENT] The recuperator consumes calculated final-compressor and turbine outlet temperatures. For equal heat-capacity rates, transferred heat is `effectiveness*mdot*cp*(Thot-Tcold)`, with corresponding calculated hot/cold outlets. Reject reversed thermal ordering rather than silently bypassing the recuperator. The external heater derives required heat from the calculated recuperator cold outlet to the supplied turbine inlet temperature. The precooler derives rejected heat from the recuperator hot outlet to the selected lowest temperature. Two intercooler duties, precooler duty, external heater duty, turbine production and three compressor demands feed a signed cycle conservation ledger.

[AGENT] Derived useful output is net fluid shaft work and its ratio to required external heat. It is not electrical output: omitted mechanical/generator losses remain unquantified. Compare the computed heater-inlet temperature with printed 355 C and report the difference; compare idealized shaft efficiency with printed gross efficiency only with their differing boundaries visible. Do not tune parameters to erase differences. Do not compute source net 0.39 without the omitted source circuits and electrical boundary.

## Reuse, change units and validation

[AGENT] Existing `mfe_primary_loop.sysml` combines heat-driven flow sizing with DEMO loss scaling and a reverse compressor temperature boundary; it is unsuitable unchanged. `mfe_power_cycle.sysml` is a fitted secondary-cycle efficiency relation. `mfe_matched_steam_cycle.sysml` contains water/steam states and extraction/reheat architecture. None supplies this Brayton component chain unchanged. Reuse the unchanged `Offered Capacity Screen` and `Offered Equipment Capacity` from `mfe_viability.sysml` for independently supplied compressor shaft-demand, heater-duty and heat-rejection ceilings under explicitly assumed conditions. Capability ratings remain fixed when selected flow or temperatures change. These scalar screens do not qualify real equipment.

[AGENT] Minimum new semantic units are generic ideal-gas compression, ideal-gas expansion, fixed-outlet cooling, equal-capacity recuperation and cycle heat/work aggregation. A heater may share a signed temperature-change heat relation if its role and nonnegative demand domain remain explicit. One design owns the three compressors, two intercoolers, equivalent turbine, recuperator, heater, precooler and accounting occurrence. Repeated compressor/cooler instances must have real downstream consumers. Avoid a single opaque efficiency calculation or an unnecessary general cycle framework.

[AGENT] Generate and seal an isolated native package through the established route. Verify stage pressure products, Kelvin conversions, dimensional heat/work balances, recuperator heat equality and signed whole-cycle energy residual against independent arithmetic. Vary selected flow while keeping ratings unchanged: extensive heat/work should scale linearly and idealized efficiency should remain constant. Vary pressure ratio and inlet temperature to demonstrate calculated state response. Exercise adequate/inadequate supplied capacities and refuse invalid pressures, efficiency/effectiveness, temperatures, reversed recuperator ordering and nonfinite inputs. Published source efficiencies are diagnostics, not pass/fail targets.

[AGENT] This is a bounded nominal cycle implementation plus unchanged generic capacity reuse. It advances T09 beyond supplied efficiency accounting while leaving real-fluid accuracy, detailed source shaft topology, exchanger matching to all three primary circuits, equipment maps, electrical losses and installed costs open. Next step is a canonical item contract and focused source/design review before model edits.
