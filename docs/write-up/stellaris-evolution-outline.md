# Part 4, support 1: Modeling Stellaris

Outline for discussion. Supports [the main post](fusion-tea-exploratory-modeling.md).

[OWNER, 2026-09-25] The viewer is the page. This narrative is added to it as context, because most readers will step through the frames and not read a separate piece. So each beat below has to work as a short note beside the frames it covers, and the groups are also how the 28 frames get grouped on the slider.

1. **Where we started.** The starting model was our SysML version of the team's costing engine, 1costingFE, set up at the Stellaris design point. It reproduced 1costingFE's cost accounts to one part in a million. That proved the machinery could reproduce another tool's arithmetic, and we decided that was all it proved. 55 equations, 6 constraints, and most physical quantities typed in from the paper or from 1costingFE defaults.
   - The ARIES papers were kept out of the repo for the test in support 2.
   - We stopped caring about matching 1costingFE at this point. From here the model was free to disagree with it.

2. **What the viewer shows.** 28 goals changed the model between August 27 and September 20. Each frame is one goal: what it asked, what changed, and what the numbers did. The rest of these notes explain why each group of goals was run, because the order was not arbitrary. Each group came from a different reason to distrust the model.
   - By the end: 199 equations, 67 constraints, 76 parts.
   - LCOE at the design point jumps around, from 275 to 333 to 142 to 319 $/MWh. Each jump is one model change the frame names. Do not read the chart as a fit converging on an answer.

3. **Frames 2 and 3: the first studies found numbers nothing checked.** The first parameter sweeps in August were meant to test the study tooling. Instead they turned up inputs that nothing in the model pushed back on. Pumping power was 1 MW, a 1costingFE default about 150 times too low. The magnetic field cost money but bought nothing, so every optimizer run drove to the lowest field allowed.
   - Fixing pumping power to the sourced 195 MW raised LCOE 21 percent and moved the recirculating-power limit across most of the sweep window.
   - Rule that came out of this: when you sweep something and nothing pushes back, the model is underdeveloped there. That rule picked the next goals.

4. **Frames 4 and 5: a yardstick for "good enough."** We were not going to spend the one blind comparison on a model nobody believed in. So we wrote a rubric, without reading ARIES: twelve subsystems, each scored on physics (is it held, calculated, or constrained) and on cost depth (a lump, a parametric cost, or sized parts). Graded the model, took the worst gaps first.
   - Magnets were first. Field, stress limit and cost now come from coil current and geometry instead of cited constants.
   - Plasma was second. The heating needed to sustain the plasma now comes from a confinement scaling. Result: with the paper's 50 MW installed, no point in the sweep works, and the design point itself needs about 90 MW.

5. **Frames 6 to 10: chasing the 90 MW.** The plasma result was either a real finding or a modeling error, and the next five goals were about telling which. This is the stretch where the model pushed back hardest and each goal was picked by the last goal's result.
   - First, price the two ways out. A higher-field conductor and more installed heating were both free in the model. Once they cost something, the wall load, not the magnet, was what blocked most designs. So fix the wall-load check, which was comparing an average to a peak limit.
   - Then trace the 90 MW itself. The stored energy was 9 percent above the paper because the helium ash had the wrong profile. Fixing that from the paper's own rule brought the requirement to 49 MW against 50. Part 3 walks this goal.
   - Then the re-run sweep showed most passing points were ignited plasmas, which the model had no constraint for. Added one. Then made a fatter plasma cost something at the magnet, since that was the other free lever.

6. **Frames 11 to 13: the rest of the plant was still typed in.** With the plasma and magnets computed, the headline cost was still set by three fixed multipliers: pumping power, cycle efficiency and availability. And a fresh audit of both models had found 20 defects. And the SysML was a flat list of 14 parts that did not read as a machine.
   - Computing the three multipliers from the design dropped LCOE from 322 to 225 $/MWh. A new divertor heat check fails at the design point.
   - The audit repairs and the restructure into 23 nested parts changed no numbers. Every output matched, on every sweep point checked. The restructure exists so a subsystem can be swapped for a trade study.

7. **Frames 14 to 21: can the magnet model leave the design point?** ARIES is a different machine. The question for the comparison was whether the magnet costs and limits respond sensibly away from the Stellaris point, or only reproduce it. Eight goals priced the winding pack by tape length, made winding length and cryo load follow the coil bore, and added two checks: does the pack fit its casing, and does the conductor carry its current with margin.
   - The Stellaris magnet fails both. The pack needs 370 mm radially and the casing has 250. Operating current 50 kA against an estimated 29.65 kA critical current.
   - Several goals ended with no: the evidence does not support a design range, no sampled point passes every constraint. Those are answers. The goal closed on them and the next one opened.

8. **Frames 22 to 27: finishing the rubric before the comparison.** Six rubric cells were still below target. Six goals in two days took breeding, cooling equipment, buildings, tritium inventory and fuel processing from cost allowances to sized equipment, then one goal graded the whole estimate. Then a readiness goal confirmed all 23 cells at target and adopted the comparison package.
   - Cooling is the one to explain. A $205M allowance became $8.2B of sized pumps, piping and exchangers, and LCOE went from 150 to 311 $/MWh.
   - The 0.80 m blanket breeds too little tritium. Thicker blankets pass breeding and break the field limit.
   - The estimate graded itself a Class 5 conceptual estimate. Cooling, magnets and buildings are 73 percent of direct cost.

9. **Frames 28 and 29: the reveal failed, and why.** On September 20 we opened ARIES and ran the comparison. It stopped on the first calculation: the field came out at 56.6 T, outside the conductor model's range. The investigation found the real problem: several calculations sized equipment to meet demand instead of evaluating the equipment the designer supplied. That is the opposite of what the method is for. We branched from the pre-reveal code and ran two repair goals.
   - Magnet geometry, facility size, processor throughput and cooling purchases became inputs the model evaluates. 33 capacity checks added.
   - The last goal's answer: the size range ARIES needs is outside what the breeding and conductor models support. Support 2 picks up from there.

10. **What this shows.** The rubric worked as a yardstick for depth. Every cell reached target, nothing was tuned to the paper, and along the way the model found things we did not put in: the pumping power, the ash profile, the ignited plasmas, the magnet that does not fit, cooling dominating cost. What the rubric did not measure was whether the model respected the method's one rule, that the designer chooses and the model evaluates. Depth scores passed while that rule was being broken. That is the lesson support 2 starts from.

Open: this is ten beats, one over the harness outline. Beats 4 and 5 could merge. The main post says nine goals and ten studies; that count is from mid-September and the viewer's 28 is current.
