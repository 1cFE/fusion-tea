---
Status: active
Scale: standard
Epic: ARIES model transfer experiment
Owner: reid
Created: 2026-09-21
Updated: 2026-09-21
---

# Nominal Brayton component cycle

[INHERITED: coordinator assignment, 2026-09-21] Implement a forward ideal-gas helium cycle with independently supplied flow, three independently supplied compressor ratios and fixed offered capacities. Source and approximation inventory: `work/orchestration/aries-transfer-experiment/power-conversion-scope.md`. This is a reduced nominal scenario, not exact source reconstruction or qualified off-design equipment performance.

## Inputs and authority

[AGENT] Visually verified Raffray p736 Figs12/13 and p737 TableIII/Fig14 in WI-086 evidence. TableIII supplies nominal compressor efficiency 0.89, turbine efficiency 0.93, recuperator effectiveness 0.95, maximum pressure 15 MPa, total compression ratio 3.5, total friction pressure drop divided by maximum pressure 0.045 and lowest temperature 35 C. Fig12 supplies nominal turbine inlet 707 C and comparison-only heater inlet 355 C. Published gross/net efficiencies 0.43/0.39 are comparison-only. Fig13 depicts two turbines while TableIII says one expansion stage; this model represents their equivalent fluid expansion without claiming a shaft split.

[AGENT] Independently selected inputs are flow 1000 kg/s, inlet/loop-return pressure 15/3.5 MPa, three ratios each equal to the numerical cube root of 3.5, compressor inlet and both intercooler targets 308.15 K, turbine inlet 980.15 K, cp 5193 J/(kg K), gamma 5/3, the above efficiencies/effectiveness and nominal pressure-loss fraction 0.045. Equal ratios, ideal intercooling and assigning all loss upstream of expansion are explicit agent assumptions. Ratios are supplied separately; perturbing one never rebalances another. The maximum compressor pressure and total ratio are calculated, with source15 MPa/3.5 comparisons outside the model. cp/gamma use the ideal-helium approximation documented with NASA/NIST authority pointers in `knowledge/research/pending/20260907-163520_primary-loop-cycle-closure-prework.md`, section D.

[AGENT] Supply fixed hypothetical aggregate compressor shaft capacity 1100 MW, external heater capacity 2000 MW and total rejected-heat capacity 1200 MW, under assumed supported conditions. These agent choices are not source equipment ratings. Selected flow and ratios never resize to satisfy heat availability, shaft balance or capacity. Electrical conversion/mechanical losses, blanket/divertor exchanger matching, installed cost and net plant electricity remain unqualified. No coupling to WI-083 or automatic heat/flow coupling to WI-086.

## Component architecture and equations

[AGENT] Six generic calculations are proposed: ideal-gas compressor, ideal-gas expander, fixed-outlet thermal conditioning, equal-capacity recuperator, fractional pressure loss and cycle ledger. The design owns three compressors, two intercoolers, one pressure-loss boundary, equivalent turbine, recuperator, external heater, precooler and ledger. All use shared selected flow and fluid properties. Each consumer binds preceding exposed state outputs. Shared loop-return pressure closes the pressure path without a solved flow or pressure split.

[AGENT] Compression: `pout=pin*r`; `Tout=Tin*(1+(r^((gamma-1)/gamma)-1)/eta)`; positive shaft demand `mdot*cp*(Tout-Tin)/1e6`. First compressor takes selected inlet pressure/temperature; subsequent stages take preceding calculated pressure and cooled temperature. Cooler pressure is unchanged. Expansion: `Tout=Tin*(1-eta*(1-(pout/pin)^((gamma-1)/gamma)))`; positive produced shaft work `mdot*cp*(Tin-Tout)/1e6`. Its inlet pressure is calculated last-compressor pressure times `(1-loss_fraction)`; outlet pressure is selected loop return. Its inlet temperature remains independently supplied.

[AGENT] Thermal conditioning calculates signed heat into fluid `q=mdot*cp*(target-Tin)/1e6`, exposing the target outlet temperature. Cooling occurrences require target<=Tin; heating requires target>Tin. The same generic relation takes an explicit role flag restricted to heating/cooling, preserving sign semantics. Cooling heat is negative; ledger converts it to positive rejection. This avoids arbitrary public negation coefficients. Recuperation calculates `q=eps*mdot*cp*(Thot-Tcold)/1e6`, `Tcoldout=Tcold+eps*(Thot-Tcold)`, `Thotout=Thot-eps*(Thot-Tcold)`. Its inlets are computed final compressor and turbine outlet states, with no caller-supplied substituted outputs.

[AGENT] The heater goes from calculated recuperator cold outlet to supplied turbine inlet; precooler goes from calculated recuperator hot outlet to supplied first-compressor inlet. Ledger sums the three compressor demands, sums the negatives of both intercooler and precooler signed heats, subtracts compressor demand from turbine work, and exposes efficiency `net_shaft/heater_heat` and signed conservation residual `heater_heat-rejection-net_shaft`. The ledger must preserve negative net shaft outcomes and signed residuals. Source gross electrical efficiency is a different boundary from calculated net fluid shaft efficiency.

[AGENT] Three unchanged `Offered Capacity Screen` and `Offered Equipment Capacity` occurrences consume calculated compressor demand, heater heat and rejection respectively, with independent ratings/support flags. Definitions and carried executable implementation remain unchanged except package import prefix. No forced reuse of the DEMO flow-sizing/loss model, empirical cycle-efficiency correlation or steam-cycle state model.

[AGENT] The ledger independently requires each cooling heat<=0, heater heat>0 and compressor/turbine work>=0. This enforces the assembly's heating/cooling roles even if a public generic role flag is changed. Only the net shaft output and energy residual may be signed freely.

## Domain and native verification

[AGENT] Require all inputs/outputs finite; absolute temperatures, flow, cp and pressures positive; gamma>1; compressor ratios>=1; isentropic efficiencies in (0,1]; recuperator effectiveness in [0,1]; pressure-loss fraction in [0,1), with actual turbine inlet>outlet pressure; recuperator hot>=cold inlet; cooler target<=inlet; heater target>inlet; heater heat>0 before efficiency division. Refuse arithmetic overflow. No clamping, silently bypassed recuperator or inferred equipment qualification. Signed net shaft and residuals are allowed.

- [x] Source/design review accepts equations, source bindings, reduced topology and nominal assumptions before edits.
- [x] Implement generic definitions, connected component occurrences and three unchanged capacity screens; generate and seal isolated native package.
- [x] Execute nominal cycle and compare states, pressure continuity, heat/work and conservation with independent arithmetic; retain source heater-inlet and efficiency differences without fitting.
- [x] Increase selected flow with capacities fixed, verifying extensive quantities scale while efficiency remains constant; independently lower each offered rating to produce meaningful shortage.
- [x] Perturb one compressor ratio without rebalancing the others; perturb turbine inlet temperature and verify downstream calculated states/work.
- [x] Exercise nominal support false and invalid/nonfinite domains, and verify conservation plus signed ledger diagnostics.
- [x] Preserve source and reuse hashes, meaningful attempts and generated interface; run scoped validation and obtain independent completion review.

[AGENT] Native package follows the approved SysML/codegen/typed-completion/TEAx route from WI-086. Source images remain durably referenced and will be copied into item evidence. Parent owns registry/log/commit actions. Successful execution supports this declared idealized component model only; source temperatures and efficiencies are not independent prediction validation.

[AGENT] Implementation evidence: nine supported native scenarios, 306 independent Decimal comparisons and 21 native refusals pass. L1–L5 pass; forty plain EXPOSE L6 diagnostics remain, with exact locations and successful generated execution recorded in report.md. Independent completion review accepts the bounded result and the named static exceptions.
