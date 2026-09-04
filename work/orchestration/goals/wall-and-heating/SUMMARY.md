# Goal `wall-and-heating` — plain-language summary

**What this file is.** A running, human-readable account of what this goal has actually done, written for someone picking it up cold or coming back after a gap. Updated as rounds progress.

**What it is not.** Not a contract artifact and not evidence. `trail.md` remains the record of what happened and what was decided; `goal.md` remains the question and its invariants; `evidence/` holds the artifacts claims cite. If this file and any of those ever disagree, they are right and this is stale. Nothing should ever cite this file as a source.

**Why it exists.** The goal layer has a designated slot for a round's result — `### Round N result` in `trail.md` — but it is a structured record with eight prescribed fields, built for a fresh reviewer checking claims against evidence. There is no designated home for prose that reconstructs the plot. The owner asked for one on 2026-09-04, having gone agent-to-agent long enough to lose the thread.

---

## The question this goal exists to answer

At its printed heating power, the stellarator model has no workable operating point. Two fences stop it: the neutron load on the first wall, and whether the plasma can be sustained by the heating installed. Both fences were thin.

- **The wall fence measured the wrong thing.** It compares an *average* neutron load, computed over a smooth circular donut, against a limit the source published as a *peak* on a real shaped wall. Two different quantities.
- **The heating system had no structure.** Three fixed numbers and one division buried inside another subsystem's arithmetic. Nothing you could call a chain from wall-plug electricity to power in the plasma.

The goal is to make both honest. What the model then says about which escape is cheaper is a *result*, not the goal.

## Round 1 — `heating-chain-first` (open)

**The strategy, and why this order.** Do the heating half first: it has a written grading target, it needs no outside sources, and its result holds regardless of what the wall fix later does. Start the wall half's *research* in the same round anyway, because research has latency — so the next round opens with sources already in hand rather than waiting on them.

### What happened, in order

**The wall research came back with sources, and reframed the problem.** Two fresh sessions worked the research seam. Three papers are now registered in the repository. The useful finding was not the number originally sought: **every published stellarator wall-load average is taken over a real, shaped, three-dimensional wall, and the model integrates over a plain circular torus that is 15–30% too small.** So neither candidate fix — computed peak against the peak limit, or average against a sourced average — is honest until the *area* is corrected. That is a sharper statement of the defect than the goal was grounded on. Recorded for scale and not as a prediction: applying the corrections these sources support would push the baseline wall load past its limit. A tightening fence is a legitimate result to disclose; the goal explicitly forbids tuning it away.

**The heating system became real structure (WI-039).** Wall-plug electricity → gyrotron conversion → power coupled into the plasma, with every stage a named quantity that recomputes when anything upstream moves. The coupling assumption that used to be an invisible default is now written down, including which direction it is optimistic in. **The baseline did not move**: same cost, same LCOE, same nine constraint verdicts. The model got more honest without the answer shifting, which is the outcome to want.

**The package was pinned.** The integration seam passed all ten gates on the first run. That fixed version is what the study ran against.

**A study ran — 639 points, four arms.** Before it ran, a fresh session was asked to attack the design. It returned nine findings and was right about the big ones.

### What the study found

**At the printed heating power, nothing works.** Zero feasible points out of 240. Better gyrotrons do not rescue it — the gap needs roughly double the efficiency anyone can build.

**Whether heating efficiency is worth paying for depends entirely on which quantity you hold fixed.**

| held fixed | what better efficiency does to cost |
|---|---|
| the installed hardware (wall-plug power) | makes it slightly **worse** — you buy plasma heating you do not need |
| what the plasma receives (coupled power) | makes it **much better** — about 61 $/MWh across the plausible range, by drawing less electricity for the same result |

Same model, opposite answers. The first study design asked only the first question, which makes efficiency look worthless. The critique is why the second one got asked at all.

**The caveat that governs the economics.** Every economic number at the higher heating level is really set by the broken wall fence, not by heating. The cheapest "feasible" point sits at 98.8% of the wall limit and fails once the corrections from the research are applied. That correction is carried in the output data as shadow columns rather than as a footnote, so a later wall fix cannot quietly invalidate this round's conclusions without anyone noticing.

### Claims that were cut back before publication

Three times this round a claim was checked and turned out to be too strong. Each correction made the claim smaller and sounder. Recorded here because the round's whole purpose is producing something that survives an independent grader, and an inflated claim is worse than no claim.

1. **"Both efficiencies and the wall-plug power now reach the sustainment fence."** The pre-change model's heating power already reached it. The one genuinely new reach is the *source efficiency* reaching that fence.
2. **"There is an interior efficiency optimum."** There is not. It was a fence edge: the comparison was between the best point at each efficiency, which are different operating points.
3. **"Efficiency paying at constant coupled power is new."** It is not — the old model could produce the same falling curve. What is new is that the *fixed-hardware* experiment became expressible at all, because wall-plug power was previously not a quantity in the model but an expression over two constants.

### Still to do before this round closes

The study record write-up, an independent check of the reading, the formal round result, and the fresh non-author re-grade that decides whether the heating half hit its target.

### The wall half is deliberately untouched

The obvious question is why the wall fence was not fixed while its research was in hand. Because a round may promote only one package version and commit only one study, and changing the fence mid-round would move what "better" means while a study was running against it — making results before and after incomparable. That is one of the six conditions that force a round to close. So the research ran now and the fence itself waits for a round opened for it, whose strategy is written by the fresh reviewer at this round's close.
