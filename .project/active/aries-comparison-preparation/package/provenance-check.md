# Applicability and B-7 provenance receipt

[AGENT] Prepared 2026-09-16 by the bounded applicability task. This receipt records local inspection, not a native external-research return or an independent final comparison audit. Only the quarantine protocol was read within the holdout; no ARIES-specific values were sought or loaded. No model, package, immutable study or source registry was changed.

## B-7 local PDF fidelity

[INHERITED: `.project/completed/20260821_demo-anchor-acceptance-spec/spec.md`, B-7] The admissible source is `knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/arxiv-2602-19389/raw.pdf`, printed page 28, zero-based PDF page 27, Table 3. Raw PDF SHA256 independently rechecked: `a471a9b54c22bf29c6fbc4744eb73ba63418fbbceb5519e20b006cf29fcf0c02`.

[AGENT] Independently viewed the page render, now retained at `evidence/aace-paper-page28.png`, and compared its table with `evidence/aace-paper-page28.md`. Render SHA256: `1c649769bb0a3e2ee5d814ecbce251a7d70439ccc39132aa7762a1af7500c01e`; extracted page SHA256: `8b1f38152f481e770010f64f60ada682d56eea901d4792bbc4a323b36a4f6e99`. The earlier generation command and page selection are retained in `work/orchestration/goals/aries-fixed-point-comparison-readiness/evidence/grounding-aace-check.md`. These retained page artifacts, the page locator and digests provide the local fidelity receipt; the original full PDF remains at its source path.

| Table row | Definition maturity | Low accuracy range | High accuracy range |
|---|---|---|---|
| Class 5 | 0%–2% | −30% to −50% | +30% to +100% |
| Class 4 | 1%–15% | −15% to −30% | +20% to +50% |
| Class 3 | 10%–40% | −10% to −20% | +10% to +30% |
| Class 2 | 30%–75% | −5% to −15% | +5% to +20% |
| Class 1 | 65%–100% | −3% to −10% | +3% to +15% |

[AGENT] The render confirms the extraction's Class 5 endpoints and caption's 80% confidence description. Its footnote permits wider asymmetric ranges with novelty, scope ambiguity and limited data. This checks extraction fidelity; it does not establish this model's probabilistic accuracy or maturity classification.

## Primary-reference caveat

[INHERITED: grounding-aace-check.md] The grounding author consulted the official public sample of [AACE International Recommended Practice 18R-97, Cost Estimate Classification System—As Applied in Engineering, Procurement, and Construction for the Process Industries](https://web.aacei.org/docs/default-source/toc/toc_18r-97.pdf), August 7, 2020 revision. The recorded primary-source observation is that printed page 3 gives Class 5's low range as −20% to −50%, while retaining +30% to +100% high; printed page 2 describes a guideline and excludes power-generating facilities. This differs from the local paper's Class 5 low range. This task independently checked the local PDF/image, not the external sample; no native external-research receipt exists and none is claimed.

[AGENT] Cite 18R-97 as conceptual-estimate background with the process-industry scope limitation. The project band remains the ratified model/reference interval [0.5,2] for component costs, with no AACE certification, formal whole-plant classification or empirically demonstrated 80% coverage. Derived-quantity endpoints remain [1/3,3]. Neither caveat changes those endpoints or C220107's required exclusion/footnote.

## R2 applicability and source update

[AGENT] The original B-7 page fidelity and scope caveat above are reused; no new AACE source research was needed. The historical full receipt is retained in history/r1/provenance-check.md. Its former coolant gate was resolved by the owner, and subsequent clean-source reconciliation corrected HCLL attribution. The physical helium model remains an accepted conditional scenario, not a source-faithful water-blanket reproduction.

[AGENT] R2 keeps246 underlying stellarator defaults, seven independent-input rules, and adds exact-profile forward overrides0.35/1.2 to selected sizing1/reserve1. Seven conditioned seams now include the grouped Table5 geometry/field control. Shape/current derived from supplied volume/field do not validate those supplied outputs. Source input fields remain unpopulated for the held-out reference.

[AGENT] Source/equation classification is in work/orchestration/goals/stellaris-plasma-power-balance/reconciliation.md; original synchrotron normalization was registered through REQ-STELLARIS-PLASMA-SYNC-01. Pending research remains pending. No production plasma correction was justified; the exact Point-A radiation/energy implementation remains missing. Original retained source-page witnesses, review records and current oracle mappings are included in r2.

[AGENT] Two exact-mode native receipts and their oracle/operand checks replace the former unmatched-point question; see selected-mode-check.json and table5-conditioned-check.json. Raw current-boundary mismatches remain. Source conditioning earns no independent credit; existing validation/qualification limitations are summarized in evidence-reuse.md.
