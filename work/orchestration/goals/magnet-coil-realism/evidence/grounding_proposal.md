# Grounding proposal — magnet-coil-realism (2026-09-14)

The owner asked `[OWNER-VERBATIM 2026-09-14]` "Please look at the models and past goals (use subagents). I'd like you to propose a high-value goal to advance the model realism". Three fresh survey agents read the models, the goal layer and the grading/audit evidence; their reports are summarized in the proposal below (the survey transcripts are session-local and not deposited; every claim the goal relies on is re-verified in `grounding_probe/summary.md` or cited to a tracked artifact in `goal.md`).

## The proposal as put

Verified in the model files: winding length is still major radius times a held factor (`mfe_magnet_field.sysml:169`), and the cryoplant load counts only nuclear heating plus a fixed joint term.

**Where the model's realism actually stops.** The chain now computes most of the plant from the levers. What remains unrealistic falls into three kinds. Missing capabilities: achieved breeding, tritium plant, buildings, loop equipment costs. Fences where both sides are constants: breeding, cycle domain, heating efficiencies. And magnet channels that exist but do not follow the coil the model builds. The owner's 2026-09-13 feedback rules out the first kind as the next goal. The second kind is small. The third is the highest-value repair.

**Proposed goal: the magnet sees its own coil.** Question: does the magnet's winding length, cold load and structure follow the coil the model builds, and does correcting them change which machine the model favours?

Why this one:
- Magnets are the largest cost channel. $1.62B of $4.53B CAS22. Tape ($804M) and fabrication ($750M) both scale with winding length.
- Winding length is blind to the minor radius. It is 1.97 × R, anchored so the printed 25 m reproduces at R = 12.7 m. A modular coil's circumference is set by its bore, not the major radius. So fattening the plasma raises fusion power while the winding length does not move. That is the likely reason every committed optimum sits at the top of the `a` window. The minor-radius goal made peak field, stored energy and casing see the bore, but left length as R-only, and closed with "is the minor radius the model favours a machine?" open.
- The cold load is far too small to be real. 0.86 MW electric and $16.7M cryoplant for a 48-coil, 111 GJ HTS set. Current leads (96 at 50 kA), thermal-shield radiation and support conduction are absent, and the uplift factor is an admitted lower bound.
- Structure is priced as raw steel. 48 × 63 t printed floor × $6/kg × 3.0 = $54M, about 3 % of winding cost, with no inter-coil structure.
- The reveal will test exactly this. Anchor B names coil mass as a geometry-direct quantity expected within 2×. Audit finding F14 is open. The magnet-design-transfer goal just closed on "conditional numerical transfer, not engineering qualification", with casing basis and fit named as where transfer stops.
- It is repair, not gap-filling. Every channel exists. The shapes are wrong.

Shape of the goal, one model increment per round, one pin and one study each:
1. Winding length from the coil bore: shape factor × 2π × coil radius, anchored to 25 m at the design bore. The source's "approximately 7 × 5 × 10 m" bounds the shape. Read the existing R × a × I_coil window for where the cheapest machine moves.
2. Cryoplant heat inventory: lead conduction, shield radiation, support conduction, each sourced or surfaced with options, never defaulted. Reconcile with the held 15 MW coil-cooling term. The queued Pierro 2019 20 K source is the starting point.
3. Structure content and price: a fabricated cryogenic casing rate and an inter-coil mass term.

Invariants: no re-anchoring toward printed numbers beyond the design-point calibration. Costs: the 1costingFE comparison drifts further, already ruled not a maturation duty. Risk: per-coil circumferences are unprinted, so the shape factor stays one held constant.

**Alternatives set aside.** Cost-account reconciliation (F08, F09, F11, R12.S) has the highest reveal stakes by audit count, but it is accounting declaration rather than realism, and it is the continuation the owner pushed back on. Breeding and tritium cover three of the six below-target rubric cells, but there is no admissible neutronics source in the repo, so it is a build from nothing. Dropping the power-ratio multiplier on the volume-priced blanket, shield and vessel accounts is cheap and probably right, but that form is 1costingFE's own, so it is a disagreement with the source rather than a repair; carried as a round-4 candidate. Making the breeding and cycle-domain fences compare a computed operand is a trivial-scale item that could ride along; the breeding fence would flip the baseline to violated by 0.116.

## The ruling

`[OWNER-VERBATIM 2026-09-14]` "ok agreed, draft the goal file and /run-goal".

Read as: the proposal's form (three increments in the order length → cryo → structure), its anchoring approach, and its set-aside alternatives are `[AGENT] (ratified by owner, 2026-09-14)`; the slug `magnet-coil-realism` is `[AGENT]`, not named by the owner, renamable before a round opens; no reserved gate beyond the structural ones was named (the last five goals' precedent).
