# Source-check brief — reading of Raffray's Ref. 15 (fresh reviewer)

You are a fresh, independent reviewer with no prior context. Read only the files named here (paths relative to `/home/reid/1cfe/fusion-tea`). Budget: at most 12 tool calls and a 400-word return written to `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/ref15-reading-review.md`. Do not load CLAUDE.md, AGENTS.md, runbooks, trails or other goal directories. Do not run anything. Sign as "fresh source-check reviewer (Ref. 15), 2026-09-25".

## Exact question

Does `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/ref15-reading.md` state what the registered source actually says about heat delivery to the Brayton cycle, with correct page and figure citations, and does its "established / not established" section stay within the source? In particular: is it correct that the source's only heat-source representation is the single block of Fig. 1 with the turbine inlet temperature as an independent input and the return temperature as a dependent variable, and that no per-branch exchanger, terminal difference or branch duty appears anywhere in the five pages?

## Entry files

1. `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/ref15-reading.md` — the reading under review.
2. `knowledge/sources/schleicher_raffray_wong_2001_an_assessment_of_the_brayton/output.md` — the extracted text (read it all; it is about 3,000 words), and the page images in `…/images/` (view `tmp4tmb42zq.pdf-0002-03.png` for Fig. 1, `tmp4tmb42zq.pdf-0002-05.png` for Fig. 2's T-S plot, `tmp4tmb42zq.pdf-0003-01.png` for the efficiency figure). If a claim needs the original layout, `…/raw.pdf` is the captured PDF (5 pages).
3. `work/active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p737.png` — Raffray's Table III (for the mapping in § 2 of the reading) and `raffray-p736.png` (Fig. 12 and its inset).
4. `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/owner-supplement-r4.md` — the owner's framing (the lumped-heater explanation is not established until supported by the source; the current calculations are preserved).

## Checks

1. Every `[SOURCE]` and `[SOURCE-FIG]` statement in the reading: quote-check against `output.md` or the image; note any paraphrase that adds meaning.
2. The `[DERIVED]` absence claim (no per-branch exchangers, duties, temperatures or terminal differences anywhere): search the whole text for "exchanger", "blanket", "divertor", "duty", "approach", "pinch", "ΔT" and report every occurrence and whether it contradicts the claim.
3. The mapping in § 2: does Raffray's Table III list the same independent variables as the source's Table 1 and Fig. 1, and is "738 − 30 ≈ 707 °C" a fair reading of the "HX temperature difference between hot and cold legs 30 °C" row together with the Fig. 12 inset, or an inference the reading should label more cautiously?
4. § 3: does "supported at the methodology level" overreach the owner's qualification, and is the "does not resolve" conclusion the right bounded result?

## Return format

Verdict `PASS`, `FINDINGS` or `OWNER_GATE`; one line per check; numbered findings with severities (blocking / correct-before-use / note); what the review did not cover.
