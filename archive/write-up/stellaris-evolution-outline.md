# Part 4, support 1: Modeling Stellaris

Outline for discussion. Supports [the main post](fusion-tea-exploratory-modeling.md).

[OWNER, 2026-09-25] The viewer is the page. This narrative is added to it as context. [OWNER, 2026-09-26] The narrative is organized by what drove the model's evolution, not by chronology. Six themes; the viewer carries the sequence.

Lead: We started with a model that could price the Stellaris design but mostly just repeated the paper's numbers back to us. Over about a month, we ran 28 goals against it to turn the model into something that actually computes the plant from its design. Looking back over those goals, they generally fall within six themes. 

1. **Replacing typed-in numbers with physics.** The starting model was mostly fixed numbers from the paper and from 1costingFE: key system attributes (like field strength) were not modeled as a function of design parameters (like coil current). A typical goal took one of those attributes and modeled it from its design parameters, then checked that the result still matched the paper at the design point.
   - Magnetic field from coil current and geometry (frame 3).
   - Heating required to sustain the plasma from a confinement scaling (frame 4).
   - Pumping power, cycle efficiency and availability from the coolant loop, the power cycle and the maintenance calendar (frame 10).
   - Tritium breeding from blanket thickness, via neutron-transport runs (frame 21). Net electricity from a steam cycle at the actual salt temperature (frame 27).

2. **Making the model push back.** Modeling an attribute is not enough. The model also has to say when a design choice is not feasible. So we run studies: sweep the design parameters, see what LCOE is sensitive to, and find where the engineering limits are. If a sweep shows that a parameter can change cost without ever hitting a limit, then the model is missing a physical constraint. Modeling that constraint becomes the next goal.
   - The recirculating-power limit never fired, because pumping power was 150 times too low. Fixed (frame 2).
   - Raising the magnetic field added cost but improved nothing, because field reached no plasma calculation. We added confinement scaling, so field now buys sustainment (frame 4).
   - A higher-field conductor was free. Now coil size follows coil current, so higher field means a bigger, heavier, more stressed coil (frame 5).
   - Most feasible points were ignited plasmas the heating system could not control. We added a burn-control constraint (frame 8).
   - A fatter plasma cost nothing at the magnet. Now the coil bore sets the peak field and casing mass (frame 9).
   - Nothing checked that the winding pack fits its casing or that the conductor has current margin. We added both. Stellaris fails both (frames 16, 17).

3. **Making cost follow the design.** Modeling the physics does not fix the costing: an account can still be a lump sum that ignores the design. We wanted each account to follow the equipment, sized by the calculated demand (like heat exchangers by heat load) and priced by quantity, with installation, spares and replacements. These goals cause the largest LCOE moves in the viewer.
   - Cooling: a $205M allowance became sized circulators, pumps, piping and exchangers at $8.2B (frame 22).
   - Buildings sized from the equipment they hold and the maintenance they support (frame 23). Fuel processing cost scales with throughput (frame 25).
   - Winding pack priced by tape length instead of a multiplier (frames 13, 15).
   - Then we graded the estimate's maturity and where the cost concentrates (frame 26).

4. **Following the engineering design pattern.** Inputs are choices an engineer would make (like coil current or exchanger area), and the model calculates the consequences of those choices in causal order. The model must not size equipment to meet a demand, because then it has decided which parameters are free instead of the engineer. We broke this rule without noticing, and the ARIES reveal caught it.
   - Restructured into nested physical parts with ports, so a subsystem can be swapped for a trade study (frame 12).
   - Several calculations sized magnet inventory, facilities and cooling equipment from demand. Those became inputs, with 33 capacity checks that fail when the supplied equipment is too small (frame 28).
   - Measured how wide a design range the model can evaluate within the ranges its fits are valid over (frame 29).

5. **Reconciling against Stellaris.** Once an attribute is modeled, its value can differ from the paper. We trace each difference to its cause rather than tuning it away, since the cause might be our model, our reading of the paper, or the paper itself.
   - Stored energy was 9 percent above the paper, because the helium ash had been given the fuel's flat profile. With the paper's profile rule, required heating dropped from 90.6 to 49.1 MW against 50 installed (frame 7). Part 3 walks this goal.
   - The wall-load check compared a flat-wall average to the paper's peak limit. Now it computes the peak (frame 6).
   - Checked that our reference is one coherent published design point and classified each remaining difference (comments only, so no frame).

6. **Fixing defects.** All of this adds code, and code has bugs, so some goals were repairs.
   - An audit found 20 defects: heating demand confused with installed capacity, a duplicated major radius, finance formulas that failed at zero interest rate, missing range checks (frame 11).
   - A conductor cost multiplier applied twice (frame 15).

Close: Frame 29 asks how far this model can go. Support 2 is what happened when we tried.
