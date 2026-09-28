# Grounding proposal and ruling — goal `minor-radius` — 2026-09-07

The proposal put to the owner in one message, the owner's two questions, the answer, and the ruling. Deposited so the provenance of every `[AGENT] (ratified by owner, 2026-09-07)` call in `goal.md` § Reserved gates is readable without the chat. The owner's words are verbatim; the agent's messages are reproduced as sent, lightly trimmed of formatting only.

## 1. The investigation that preceded it

The session picked up `/tmp/handoff-20260907-154834.md` (written at the `burn-control` close on the owner's instruction `[OWNER-VERBATIM 2026-09-07]` "then write a /_my_handoff with instructions for what to investigate to propose options for the next goal"), read the goal artifacts it lists, and ran two fresh agents in parallel: a source-reading agent (local corpus, clean room) on whether the minor radius is a free lever, what bounds it, and how the transport facts depend on aspect ratio — `grounding_sources/report.md`; and an oracle-probe agent on the minor-radius transect (all channels) and the two-dimensional start-up map at the design geometry and at the cheapest machine — `grounding_probe/summary.md`.

## 2. The proposal (agent, 2026-09-07)

**Recommendation.** Next goal: settle whether the minor radius is a real design lever — the backlog item WI-044, run as a one-round goal — because it decides whether the demo's headline design-search result is a machine or an artifact, and the evidence to ground it is already in hand.

**The problem in plain words.** Every study optimum sits at the top of the minor-radius window (a = 2.2 m). The cheapest feasible machine, 202 $/MWh at R 15.7 m, a 2.2 m, has an aspect ratio of 7.1. The Stellaris design has 9.8. Nothing in the model pushes back on a fat plasma: the probe confirmed that ten channels do not move with the minor radius at all (on-axis field, peak field, coil stress and strain, cold volume, cryo power, magnet capital, heating capital, coupled heating). Only the plasma gets bigger and cheaper per watt.

**What the sources say.** The professional stellarator systems code (PROCESS, Lion 2021 and the 2023 thesis) treats aspect ratio as a fixed property of the coil configuration. Its Table 2 marks aspect ratio "fixed input parameter" and major radius "iteration parameter"; the minor radius is derived. No published run sweeps the minor radius at fixed major radius. The Stellaris paper's own Appendix C says a lower aspect ratio would be a different configuration, not a bigger plasma in the same coils. The one sourced constraint that does bound the minor radius is the coil-to-plasma distance: it must fit the blanket, shield, vessel, gaps, and half a coil (about 1.4 to 1.5 m in Stellaris), and it shrinks as the plasma grows inside a fixed coil set. Where the sources price a bigger coil bore, they do it through stored magnetic energy and structure mass, and the peak field on the conductor rises as the bore grows.

**What that does to the current answer.** Near the source's aspect ratio, the cheapest feasible point in the committed study is 283.61 $/MWh (R 14.2, a 1.5, 16 MA, 17 keV). Only 47 of the 307 feasible points at the printed heating sit near aspect ratio 9.8. So the "202 $/MWh cheapest machine" rests on a geometry no source supports, and the gap to a supported one is about 80 $/MWh.

**Two forms the goal could take, decided at grounding:** (1) hold the aspect ratio as a configuration fact (recommended at the time): the minor radius becomes R divided by 9.8, sourced to the paper; the design search runs over R, current, density, and temperature; retires a study lever. (2) Keep the lever and make the magnets see the coil bore: add the three sourced scalings — peak field rising with the bore, stored energy with the bore squared, structure mass from stored energy; the sources give no coil-bore price guaranteed to move the optimum interior, and the earlier linear shadow did not.

**Cost.** One round, on the burn-control pattern: a model item, one pin, one study re-reading the window, the machine as designed restated. The last three goals each took one to three days.

**The other candidates.** The start-up heating requirement (new result: the best two-dimensional start-up path at the design geometry peaks at 77 MW coupled against 50 installed, the two regions under 50 MW disconnected; 59 MW at the cheapest machine) — second choice. The transport facts' aspect-ratio scaling — a bounded negative; no admissible source gives one. A sourced burn-control lever — still nothing. The branch sign as a model channel — a small item. Housekeeping to file: fail-closed coverage for the two newest records, the executor revision in the pin identity, the reveal-readiness condition the maturation concept requires.

**Said plainly.** The maturation concept says goals should target the rubric's ranked gaps; the last two goals moved no rubric grade; the open big gaps are the primary coolant loop (Row 7) and lifetime feeding availability plus tritium breeding (Rows 2b, 2c, 11). The minor-radius goal will not move a grade either. Recommended first anyway, because every depth goal's study reads the same window, and today that window's answer is set by an unsourced lever.

## 3. The owner's questions `[OWNER-VERBATIM 2026-09-07]`

> Hold the aspect ratio as a configuration fact (recommended).
>
> at what level will this be set? I would much prefer the underlying model to be freely set so we would be able to vary this in a study. are we setting this within just the stellaris instance?
>
> And it seems like option 2 is more productive in terms of advancing the engineering modeling, is that right?

## 4. The answer (agent, 2026-09-07)

**Where the aspect ratio would be set.** In the Stellaris instance only, as a settable input like R, with the library deriving the minor radius from it. Nothing in the library would hard-code 9.8, so a study could still sweep it. But that exposes what option 1 really is: it changes which knob the study turns by default, not what the model knows. Sweeping the aspect ratio at fixed R is the same move as sweeping the minor radius at fixed R, and the model would still have nothing that pushes back on it. If the geometry is to be freely settable, option 1 buys almost nothing on its own.

**Is option 2 more productive for the engineering modeling?** Yes, and given the stated preference it is the right choice. It adds computed relationships that respond to the minor radius instead of a held fact: the peak field on the conductor from coil geometry (today the on-axis field times a held ratio calibrated at the design point; the sourced form has the field on the coil rising as the coil bore grows toward the major radius; anchored at the design point the way the wall-peak calibration was); stored magnetic energy from the coil bore (the sourced scaling grows with the bore squared at fixed current and major radius); coil structure mass from stored energy (an empirical law the systems code uses, feeding the existing casing-structure cost account). All three forms live in the library, concept-agnostic; the Stellaris anchors and the coil bore from the radial build live in the instance. Two caveats: how hard it pushes is not known until the study runs (on the design column the peak-field factor rises about 10 percent from a 1.3 to a 2.2, enough to break the conductor ceiling; at the cheapest machine's larger major radius only about 1 percent; whether a 2.2 still wins is what the study measures); and the configuration coefficients are not printed, so each term is anchored at the design point and scaled by the sourced shape, with the model text saying so and saying the transport facts are still point-A facts carried to other geometries. Revised recommendation: option 2, with the aspect ratio reported as a derived quantity rather than held, and the minor radius left free for studies.

## 5. The ruling `[OWNER-VERBATIM 2026-09-07]`

> ok go with option 2, /run-goal ground

Read as: the form is option 2 as described in § 4 (the magnet chain sees the coil bore through the three sourced shapes; the minor radius stays a free lever; the aspect ratio reported, not held); the goal is grounded now. The owner did not name the slug; `minor-radius` is the agent's call, ratifiable or renamable before any round opens.
