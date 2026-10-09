The design review is in: `.project/active/explorer-api-contract-gate/design-review.md` (verdict Revise). Its product-lens findings are in `product-lens.md` and folded into the review's M7 and M8.

The orchestrator's resolutions are in the review's **Resolutions** section, keyed by finding ID. Revise `design.md` to apply every resolution. The orchestrator adjusted three of the reviewer's proposals, so follow the Resolutions text, not the review body, where they differ:

- **M1:** the disappearance rule doesn't apply to parameter `concepts[]` lists; only the unlisted-ID rule does.
- **M6:** Phase 1 replays code churn as well as data churn, using each commit's own explorer tree where it loads, and its pass line is a fraction with a floor.
- **m8:** add one range-endpoint slider body for the first eligible concept only.

Constraints:

- Keep the main body readable in one pass. Move inventories and tables to appendices if the body grows past ~350 lines.
- Keep the provenance grades honest. M7's exceptions are orchestrator-grade. Only "pushes that would break the website don't deploy" is owner-ratified.
- Update the Next-Stage Handoff and the Validation section to match.
- Do not commit. When done, finish with the ARTIFACT line and a short list of what changed, keyed by finding ID.
