# Part 4a: Modeling Stellaris

Supports [the main post](https://1cf.energy/exploratory-modeling/). The viewer is the page; these notes are context for its frames. Part 3, [the full harness](part-3-harness.html), explains goals and rounds.

We started with a model that could price the Stellaris design but mostly just repeated the paper's numbers back to us. Over about a month, we ran 28 goals against it to turn the model into something that actually computes the plant from its design: from 55 calculations, 6 checks and 14 parts to 199, 67 and 76.

## Six themes in the model’s evolution

Looking back over those goals, they generally fall within six themes.

### 1. Replacing typed-in numbers with physics

The starting model was mostly fixed numbers from the paper and from 1costingFE: key system attributes (like field strength) were not modeled as a function of design parameters (like coil current). A typical goal took one of those attributes and modeled it from its design parameters, anchored so that it still reproduces the paper at the design point.

- The magnetic field is modeled from the coil count, coil current and major radius (frame 3, [record](../../../work/orchestration/goals/magnet-closure/trail.md)).
- The heating required to sustain the plasma is modeled from field, density and temperature through the ISS04 confinement scaling (frame 4, [record](../../../work/orchestration/goals/operating-point-closure/trail.md)).
- Pumping power is modeled from the coolant flow and pressure loss, cycle efficiency from the power cycle, and availability from the maintenance calendar (frame 10, [record](../../../work/orchestration/goals/plant-closure/trail.md)).
- Tritium breeding is modeled from blanket thickness, using five OpenMC neutron-transport runs (frame 21, [answer](../../../work/orchestration/goals/computed-tritium-breeding/answer.md)). Net electricity is modeled from the salt heat and temperature through a steam cycle (frame 27, [answer](../../../work/orchestration/goals/current-model-comparison-readiness/answer.md)).

### 2. Making the model push back

Modeling an attribute is not enough. The model also has to say when a design choice is not feasible. So we run studies: sweep the design parameters, see what LCOE is sensitive to, and find where the engineering limits are. If a sweep shows that a parameter can change cost without ever hitting a limit, then the model is missing a physical constraint. Modeling that constraint becomes the next goal.

- The recirculating-power limit barely fired, at 32 of 948 swept points, because pumping power was 1 MW, a 1costingFE default 130 to 195 times too low. At the sourced 195 MW it fires at 184 points, and the design point's cost rose 21 percent (frame 2, [record](../../../work/orchestration/goals/p-pump-fence/trail.md)).
- Raising the magnetic field added cost but improved nothing, because field reached no plasma calculation, so the cheapest point always sat at the lowest field the beta limit allowed. With confinement scaling, field now buys sustainment (frame 4, [study](../../../exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/record.md)).
- More coil current was free. We sized the winding pack from the current, so more current meant a bigger, more stressed coil and a larger cold mass (frame 5, [record](../../../work/orchestration/goals/priced-levers/trail.md)). Frame 28 made the pack a supplied design choice, so more current now raises its stress and current density instead of its size.
- Operating points kept passing even when plasma self-heating exceeded the modeled losses, because the model checked that the installed heating was enough but not whether there was already too much heat to balance. We added a power-balance check under the model's assumptions. It marks 1,113 of the 1,839 passing sampled points as failing, leaving 726, and the failing points stay in the results. The check does not rule out ignition: a point that needs exactly zero heating passes. Evaluating the failing points properly would need burn-control mechanisms the model does not represent (frame 8, [record](../../../work/orchestration/goals/burn-control/trail.md)).
- A fatter plasma cost nothing at the magnet. We made the coil bore set the peak field and casing mass, and the fattest plasmas at the paper's radius failed the conductor limit (frame 9, [record](../../../work/orchestration/goals/minor-radius/trail.md)). Frame 28 made casing mass a supplied input, but the bore still sets the peak field.
- Nothing checked that the winding pack fits its casing or that the conductor has current margin. We added both. The reference design fails both under the assumed casing walls, insulation and tape performance: 370 mm of pack in 250 mm of casing, and 29.65 kA of critical current against 50 kA operating (frames 16 and 17, [fit](../../../work/orchestration/goals/winding-pack-casing-fit/answer.md), [current](../../../work/orchestration/goals/absolute-conductor-current-margin/answer.md)).

### 3. Making cost follow the design

Modeling the physics does not fix the costing: an account can still be a lump sum that ignores the design. We wanted each account to follow the equipment, priced by quantity, with installation and, for equipment that wears out, spares and replacements. These goals also sized that equipment from the calculated demand (like heat exchangers from heat load). Frame 28 made the equipment a supplied choice, checked against that demand. The cooling goal is the largest LCOE move in the run.

- Cooling: replacing a single $205M allowance with priced circulators, pumps, piping and heat exchangers raised the estimate to $8.2B, and LCOE from 150 to 311 $/MWh, on the 18-circuit study case. About $7.4B of that is primary piping and heat exchangers, priced from assumed dimensions and nuclear-grade stainless fabrication (frame 22, [answer](../../../work/orchestration/goals/installed-cooling-equipment-costs/answer.md)). We had modeled an all-helium blanket, while a reviewer pointed to a helium/water split in Stellaris, so the figure shows what drives cost in the configuration we chose, not what Stellaris's cooling should cost.
- Buildings sized from the equipment they hold and the maintenance they support (frame 23, [answer](../../../work/orchestration/goals/layout-based-facilities/answer.md)). Fuel processing cost scales with throughput (frame 25, [answer](../../../work/orchestration/goals/throughput-based-fuel-processing-costs/answer.md)).
- The winding pack's single cost multiplier was replaced by material inventory, tape procurement and winding operations, and a later goal priced the tape by its purchased length (frames 13 and 15, [claim](../../../work/orchestration/goals/magnet-design-transfer/transfer-claim.md), [answer](../../../work/orchestration/goals/tape-procurement-consistency/answer.md)).
- Then we graded the estimate's maturity and where the cost concentrates: a Class 5 conceptual estimate, with cooling, magnets and facilities at 73 percent of direct cost (frame 26, [answer](../../../work/orchestration/goals/cost-estimate-maturity-and-uncertainty/answer.md)).

### 4. Following the engineering design pattern

Inputs are choices an engineer would make (like coil current or exchanger area), and the model calculates the consequences of those choices in causal order. The model must not size equipment to meet a demand, because then it has decided which parameters are free instead of the engineer. We broke this rule without noticing, and the ARIES reveal caught it.

- Restructured 14 flat parts into 23 nested physical parts with ports, so a subsystem can be swapped for a trade study. Every output stayed identical (frame 12, [record](../../../work/orchestration/goals/structural-decomposition/trail.md)).
- Several calculations sized magnet inventory, facilities, fuel processing and cooling equipment from demand. Those became inputs, with 33 capacity checks that fail when the supplied equipment is too small (frame 28, [answer](../../../work/orchestration/goals/preserve-model-design-choices/answer.md)).

### 5. Reconciling against Stellaris

Once an attribute is modeled, its value can differ from the paper. We trace each difference to its cause rather than tuning it away, since the cause might be our model, our reading of the paper, or the paper itself.

- Stored energy was 9 percent above the paper, because the helium ash had been given the fuel's flat profile. With the paper's profile rule, required heating dropped from 90.6 to 49.1 MW against 50 installed, and the last 2.7 percent of the gap is the paper's own (frame 7, [record](../../../work/orchestration/goals/stored-energy-basis/trail.md)). Part 3 walks this goal.
- The wall-load check compared a flat-wall average to the paper's peak limit. Now it computes the peak, which the design failed narrowly, 4.088 against 4.05 MW/m², until the ash fix (frame 6, [record](../../../work/orchestration/goals/wall-and-heating/trail.md)).
- Checked whether our reference is one coherent published design point. It is not, and each remaining difference was classified by cause (comments only, so no frame; [answer](../../../work/orchestration/goals/stellaris-reference-reconciliation/answer.md)).

### 6. Fixing defects

All of this adds code, and code has bugs, so some goals were repairs.

- An audit found 20 findings: heating demand confused with installed capacity, a duplicated major radius, finance formulas that divided by zero at equal interest and inflation rates, missing range checks (frame 11, [record](../../../work/orchestration/goals/fusion-audit-remediation/trail.md)).
- A conductor cost multiplier applied twice (frame 15, [answer](../../../work/orchestration/goals/tape-procurement-consistency/answer.md)).

## Model limits

The models are still limited to the ranges they were built for. For example, the conductor performance model, which gives the current the superconducting tape can carry at a given field, is only valid for peak fields between 20 and 32 T, and the tritium breeding calculation was built from neutron-transport runs at the Stellaris radius, so it only covers blanket thicknesses of 0.6 to 1.0 m at that radius (frame 29, [answer](../../../work/orchestration/goals/model-evaluation-domain-readiness/answer.md)). Expanding the design space the model can handle is more work to be done. We look at this question further in [Part 4b](part-4b-aries-test.html).
