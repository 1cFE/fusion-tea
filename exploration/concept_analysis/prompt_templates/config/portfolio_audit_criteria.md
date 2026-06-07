# Portfolio-audit criteria

These are the things to look for when you check whether a whole cohort of fusion
concepts makes sense together. They guide your judgment — they are not a
checklist to tick off. Use them to decide what is worth investigating, then
follow your nose. You are trusted to direct your own investigation.

The headline number for every concept is its **1 GWe LCOE** (levelized cost of
electricity, dollars per MWh, projected to a common 1-GWe plant size so concepts
of different native sizes can be compared). Most of the digest is built to let
you compare that number, and the cost accounts (CAS) underneath it, across
concepts.

## 1. Family-internal coherence

Concepts in the same family (and especially the same subfamily) are built on the
same physics and should mostly land in the same neighborhood. A tokamak that
costs three times its tokamak neighbors needs a reason you can point to.

Look for:
- One concept in a family whose LCOE sits far outside the rest of its family,
  with no obvious design reason.
- A single cost account (say CAS22, the reactor plant) that is the lone driver of
  a family outlier — the rest of the accounts look normal but one is way off.
- Two concepts that are nearly the same architecture but land far apart, or two
  that are very different but land suspiciously identical.

## 2. Cross-family magnitude ordering

Different families have different physics, and that should show up as a sensible
ordering of cost. If the ordering is backwards from what the physics implies,
that is worth a hard look.

Look for:
- A family that is widely expected to be harder or less mature coming out
  cheaper than a more mature family, with no explanation.
- Headline numbers that are all bunched together across families that should
  differ — which can mean the model isn't actually capturing the differences.
- Numbers that are simply implausible for fusion — far below the cheapest
  credible clean-energy source, or far above anything anyone would build.

## 3. Source traceability on the big cost drivers

The accounts that dominate a concept's cost are the ones whose sources matter
most. A huge cost driven by a hand-entered override (a number the analyst pinned
in place of the library's own estimate) should trace to a real, checkable source.

Look for:
- A dominant cost account whose value comes from an override with thin, vague, or
  missing source backing.
- An override whose stated value doesn't square with the source it cites.
- A concept leaning on many overrides to hit its number — the more the analyst
  had to hand-tune, the less the result is the model talking.

## 4. Sensitivity behavior under perturbation

A number you can trust shouldn't swing wildly when you nudge an input a little,
and shouldn't be suspiciously flat either. You can import a concept's model and
re-run it with a changed input to see how the answer moves (see the probe and
perturbation instructions in your main prompt).

Look for:
- A headline number that moves far more than proportionally when you change one
  ordinary input — a sign the result is balanced on a knife edge.
- A number that barely moves no matter what you change — a sign an override or a
  fixed value is pinning it, and the model underneath isn't really doing the work.
- Sensitivities that differ sharply between two concepts that should behave alike.

## A note on what NOT to flag

- Do not flag a concept whose model is marked **stale** in the digest
  (`model_stale: true`) for a number discrepancy — its recorded numbers may not
  reflect its current code. Either skip it or note it as "cannot audit — model
  output is stale, needs a re-run." Use the probe to get fresh numbers if you
  need them.
- Do not flag a concept whose model failed to import (`import_status` starts with
  "error") for a sensitivity finding — you can't run it. Note the import failure
  and move on.
- A real, well-sourced design reason for an outlier is not a finding. The goal is
  to catch numbers that don't hang together, not to punish concepts for being
  genuinely different.
