# Brief — spec_review stage — Item 1 (anchor acceptance spec), STELLARATOR-DEMO epic

## What to review

`.project/active/demo-anchor-acceptance-spec/spec.md` — the anchor acceptance bars for the stellarator demo (STELLARATOR-DEMO Item 1). The spec document is the item's deliverable (no design/plan/implement follows); after this review the owner ratifies the consolidated proposal table at its end.

Context to read first:
1. `knowledge/holdout/aries-cs/PROTOCOL.md` — §3 barred paths absolute for this session too
2. `.project/concepts/stellarator-mbse-demo.md` — criteria 3, 4, 8 (the spec must faithfully operationalize these)
3. `.project/research/20260718-205525_anchor-acceptance-evidence-stellarator-demo.md` — the evidence base every number must trace to
4. `.project/backlog/epic_stellarator_mbse_demo.md` — Items 1, 3, 4, 7 (the consumers of these bars)

## Review lenses

1. **Usability by the consuming items.** Could Item 3/4's implementer and Item 7's comparison author apply each bar mechanically, without judgment calls the spec should have made? Flag any bar that two reasonable readers would apply differently. Two candidates the orchestrator already suspects — verify and sharpen rather than take on faith:
   - B-3's pass band is worded three ways ("same order of magnitude", "leading power of ten matches", "within a factor of ~3") that are not the same test. Which single operational test is the bar?
   - B-4 (and B-3) never fix the ratio convention: is the band on model/reference or reference/model, and is "−50%/+100%" symmetric under inversion? An asymmetric band without a fixed direction is ambiguous.
2. **Evidence tracing.** Every [AGENT-PROPOSED] number and [HARD] claim traces to the research doc or a record it cites. Spot-check against the research doc — including whether the spec faithfully carries the float32-floor numbers and the AACE Class 5 band.
3. **Capture fidelity.** Provenance grades used correctly (nothing agent-proposed reads as settled; the [OWNER] criterion-3 ruling carried at its stated force, not amplified or diluted); the G-8 conflict surfaced and NOT resolved; corrections shrink rather than accrete.
4. **Internal consistency.** A-3's boundary vs A-4's acceptance form; B-5 exclusions consistently applied in B-6's conjunction; the ratification table complete (every proposed item present, no proposal hiding outside it).
5. **Concept faithfulness.** The bars operationalize criteria 3/4 as written — especially: a miss fails the anchor and is reported (no soft language), sizing excluded from criterion 4, pre-reveal commitment explicit.
6. **Blind integrity.** Nothing in the spec smuggles an ARIES-CS expectation (the prior-leak bar honored in the spec's own rationale text, not just stated).

## Output

Verdict + findings split **must-fix** vs **nice-to-have**, each with the spec section it targets and a concrete fix suggestion. Save the review to `.project/active/demo-anchor-acceptance-spec/spec-review.md`. Do not edit the spec yourself. End with ARTIFACT: <path>.

## Constraints

- Barred paths per PROTOCOL §3 — do not read them.
- The reserved gate stands: numbers are owner-ratified; your job is whether the *proposals and their bases* are sound and usable, not to re-decide them.
