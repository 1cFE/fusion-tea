Round 1 is closed and handed off. Two files written: the trail, and the two joined disposition rows in `DISCOVERY_LOG.md`. `learnings.md` untouched, no commits.

## Dispositions landed

Both rows appended under their existing ids, exactly as the passed proposals stated them — `#3` as `model fix`, `#5` as `declared seam`. `tests/study/test_records.py` passes 7, so the multi-row join under one id holds. Before writing the `#5` row I re-ran the reconstruction recipe myself rather than inheriting the checkpoint's corner check: it reproduces `oracle_scan.json` exactly at the baseline and at both grid corners (0.9424 / 8.3 and 0.0572 / 4529.2).

## The close trigger, derived

**Trigger 6 — the goal answered.** No limit fired (zero retries, one of two revisions used, round 1 of 6). The last semantic outcome was `COMPLETE`, so trigger 2 doesn't apply; the channel was traced, not widened, so trigger 3 doesn't. I tested trigger 4 explicitly and it does not apply: the round met three reserved gates and referred all three, but it was not *waiting* on any of them — `T-001`'s scope excluded every gated action before the work began, and § Answered when calls a trail-only answer complete. This closes the round, not the goal; the close stays owner-held.

**Intent: met**, with the counter-reading recorded — no model increment landed and no study ran, and the review can take "unmet" on those.

## One thing newer than the passing checkpoint

The checkpoint pointed at a line neither prior entry had cited. I read it: ARIES-ACT reports "~1% of the total thermal power ... (~2% to 3% of thermal power **in the He-cooled divertor**)". So **DI-008's 2 % floor is a divertor-relative figure read as plant-relative** — which also settles the 60–190 vs 30–190 discrepancy `goal.md` logged, in the research file's favour. It strengthens D-2; it is unreviewed, and the result flags it as such.

I also read the two lines behind the strongest objection to my own number: ACT2 removes about half its blanket heat with helium (49:51 He:LiPb) and still reports ~1 % at plant level. That is stated in the result beside the conclusion, not omitted from it.

## Recommendation to the owner — three rulings

1. **DI-008 (gate 4).** Correct its 2 % floor (a misread) and its Stellaris band (computed against the paper's 3150 MWth, not the model's `p_th`). **Do not** narrow the basis to 4–6 % — ARIES-ACT's ~1 % is real, and excluding it would hide the best evidence against this round's own number.
2. **The shape (gate 2).** Keep `p_pump` a held, settable input, re-based. The two forms differ ~3 %, far inside source precision; internalizing costs an axis in two committed studies; and the fraction form asserts a linearity across swept geometry that no source establishes. The argument *against* is stated too: a held scalar is only right at the geometry it was derived at, which is the real case for internalizing.
3. **The value and sources (gates 3, 4).** Land ~195 MW (6 % of `p_th`) in both twin homes via a minted work item, with ~130 MW recorded as a documented lower bound rather than averaging to a number no source states. Register Cismondi; ingest the Moscato PDF. A "keep 1.0 MW" ruling is not available — it fails at every end of the range, including ARIES-ACT's ~1 %.

Round 2, if the gates open, hits the unrepaired `integrate` seam: a fence measurement needs a pinned package, which is a `PREREQUISITE` return. The `rec_frac` half could be answered without a pin by the L-002 recipe; the LCOE half could not.

Three learning claims are proposed, not appended. The fresh round review is next.