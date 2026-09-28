# Source-check brief — reading of Malang, Schnauder and Tillack 1998 (fresh reviewer)

You are a fresh, independent reviewer with no prior context. Read only the files named here (paths relative to `/home/reid/1cfe/fusion-tea`). Budget: at most 12 tool calls and a 400-word return written to `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/malang98-reading-review.md`. Do not load CLAUDE.md, AGENTS.md, runbooks, trails or other goal directories. Do not run anything. Sign as "fresh source-check reviewer (Malang 1998), 2026-09-25".

## Exact question

Does `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/malang98-reading.md` state what the registered source actually says about heat delivery to the Brayton cycle (one lithium loop through one intermediate heat exchanger with stated terminals; no divertor or second loop; efficiency from To/Ts, pressure-loss ratio and component efficiencies), with correct page, figure and table citations, and does its "established / not established" section stay within the source and the owner's framing?

## Entry files

1. `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/malang98-reading.md` — the reading under review.
2. `knowledge/sources/combination_of_a_self_cooled_liquid_metal_breeder_blanket/raw.pdf` — the 7-page typeset paper (read pages 561–567; the extraction `output.md` scrambles the title and the p. 564 equation, so prefer the PDF). Page renders for checking figures: `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/malang98-p562.png`, `malang98-p563.png`, `malang98-p565.png`.
3. `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/ref15-reading.md` § 1 (the citing paper's use of this source; for the lineage claim in § 2 only).
4. `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/owner-supplement-r4.md` — the owner's framing (the lumped-heater explanation is not established until supported by the source; the current calculations are preserved).

## Checks

1. Figure labels (§ 0): confirm from the renders which diagram sits under which caption on pp. 562 and 565 and whether the reading's description of the swap is right.
2. Every `[SOURCE]` and `[SOURCE-FIG]` statement in § 1: quote-check against the PDF; note any paraphrase that adds meaning, any wrong page, and any number that differs.
3. The absence claim (no divertor, no second primary loop, no per-loop duties, no exchanger network; only IHX, recuperator, intercoolers and heat-rejection HX): search the paper for "divertor", "first wall", "loop", "exchanger", "parallel", "series" and report every occurrence.
4. § 2 and § 3: is the lineage statement (Malang → Schleicher → Raffray) supported by `ref15-reading.md` § 1 as cited; does "the natural inheritance of the method" overreach the owner's qualification; is "does not address it" the right bounded result?

## Return format

Verdict `PASS`, `FINDINGS` or `OWNER_GATE`; one line per check; numbered findings with severities (blocking / correct-before-use / note); what the review did not cover.
