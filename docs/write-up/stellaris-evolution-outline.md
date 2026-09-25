# Part 4, support 1: Modeling Stellaris

Outline for discussion. Supports [the main post](fusion-tea-exploratory-modeling.md).

[OWNER, 2026-09-25] The viewer is the page. This narrative is added to it as context, because most readers will step through the frames and not read a separate piece. So each beat below has to work as a short note beside the frames it covers, and the five pushes are also how the 28 frames get grouped on the slider.

1. **The setup.** The demo asks whether an AI working in this harness can build a model that teaches us something, and whether its modeling judgement can be trusted. We gave it one documented design point, the Stellaris stellarator, and held ARIES back for the test in support 2.
   - The starting model was a translated costing model: 55 calculations, 6 checks, most of the physics typed in as numbers copied from the paper and from 1costingFE.
   - The standing rule was never "match the paper." It was: replace a typed-in number with a calculation that reproduces the paper's inputs, then let the outputs disagree.

2. **How to read the record.** 28 goals changed the model between late August and September 20, and the viewer lets the reader step through every one. The story is five pushes in different directions, and this piece walks the pushes and shows one goal from each up close.
   - Where it ended: 199 calculations, 67 checks, 76 parts.
   - The cost number never converged. Every swing has a recorded reason, and that is what the reader should take from the chart.

3. **Push one: make the checks honest.** The first eight goals took the paper's operating point and asked whether the machine as written could hold it. Every typed-in number replaced by a calculation made the paper's design look worse, and that is the model telling the truth, not drifting.
   - Pumping power was carried over at 1 MW; the sources say 195. Cost rose 21 percent in one step.
   - The magnets got a field, a stress limit and a cost from the coil design. The plasma got a confinement relation and a heating requirement. The paper's 50 MW could not hold any point in the sweep.
   - The helium ash goal found the stored-energy error and brought heating to 49.08 MW against 50. Then most "feasible" points turned out to be ignited plasmas, so a new check ruled them out. Part 3 walks this goal; here it is one frame.

4. **Push two: rebuild the plant around it.** Three goals replaced the last plant-wide multipliers with calculations, repaired a 20-finding audit, and restructured the model into nested physical parts without changing a number.
   - Cost fell from 322 to 225 per MWh when pumping power, cycle efficiency and availability were computed instead of held, and a new divertor heat check failed at the design point.
   - The restructuring is the frame where the diagram changes shape and nothing else moves: every output matched on every sweep point checked.

5. **Push three: the magnet, all the way down.** Eight goals priced the winding pack by its tape, made winding length and cold load follow the coil, and added fit and current-margin checks. The reference design fails both new checks, and the feasible region nearly closed.
   - The winding pack needs 370 mm of casing and has 250. The conductor carries 50 kA against an estimated 29.65 kA critical current.
   - Several goals here closed as bounded negatives: the evidence does not qualify a design range, or no sampled point passes every constraint. Those closures are the judgement the demo set out to test.

6. **Push four: the rest of the plant, and what it costs.** Six goals took breeding, cooling equipment, buildings, fuel inventory and fuel processing from allowances to sized equipment, then graded the estimate.
   - Cooling went from a 205 million dollar allowance to an 8.2 billion dollar equipment estimate, and cost from 150 to 311 per MWh. This is the largest move in the record and the one to explain most carefully.
   - The blanket as designed breeds too little tritium, and thicker blankets break the field limit.
   - The estimate graded itself as a provisional Class 5, with cooling, magnets and facilities holding 73 percent of direct cost.

7. **Push five: getting ready for the test.** The last three goals made the model something a comparison could run on: a real steam cycle, supplied design choices that evaluation no longer overrides, and an honest statement of how far the model can be evaluated.
   - Net electricity fell from 1,009 to 850 MW once the steam cycle used the actual salt temperature.
   - The last goal's answer is that the intended size range exceeds what the model supports. Hand off to support 2.

8. **What the record says about the questions.** Did the model teach us anything, and can the judgement be trusted? The first answer is a short list of things nobody typed in; the second is the pattern of goals that closed without an answer.
   - What the model surfaced: the pumping-power error, the ash profile, ignited plasmas, the wall load binding before the magnets, the casing that does not fit, cooling dominating cost.
   - Judgement: the goals that stopped, redirected or answered "no," each with the reason recorded, and the owner rulings that closed them.
   - The limit: the model is honest about the paper's design, not right about it. Support 2 is the test of that.

Open: five pushes with one goal each, or one thread (sustainment and heating) carried through and the rest left to the viewer? The main post says nine goals and ten studies; that count is from mid-September and the viewer's 28 is current.
