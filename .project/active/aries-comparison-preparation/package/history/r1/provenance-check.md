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

## Current applicability verification

[AGENT] The exact 246 current stellarator input keys/defaults were read directly from the generated input JSON, and all seven permitted independent keys, six conditioned seam groups and selected-mode keys resolve to it. `input-rules.json` preserves the full default map and its SHA256 for freeze verification. The selected forward override is current sizing only; it does not import the older studies' allocation, loop count or inventory reserve. Source/package integrity beyond this bounded read belongs to the coordinator's lineage/freeze checks.

[AGENT] Rechecked current blanket comments and live circuit/cycle bindings against the grounding coolant review and the clean source's explicit HCLL-precedent/water-breeding statements. The attribution conflict remains present. The package discloses it and leaves the recorded owner gate intact. It neither corrects model documentation nor certifies source-faithful cooling. Hydraulic/cycle, conductor and lifecycle handwritten guards were read to verify the conditioned seam limitations in `input-applicability.md`.

[AGENT] No new physical evaluations were performed. Prior native/oracle checks establish conditional numerical response under their own exact inputs, with adverse constraints, sixteen unmapped scalar channels and the documented exact-current-boundary behavior retained. A receipt for the selected default-plus-current-sizing combination must be identified by the coordinator or explicitly verified once if absent; transfer-anchor success is not evidence for a different operand set.

[AGENT] Exact operand reuse check: merged every `results/native-cases.json` case with its own `preparation/package-inputs/stellarator_plant_params.json` defaults in `20260915-joint-magnet-sizing` and `20260916-bounded-feasibility-transfer`, then compared all 246 current keys against defaults plus `sizing_mode=1`. Neither store contains an exact match. The nearest joint current-sized geometry case uses reserve 1.01 and predates the target-capture input; the bounded current-sized reference uses sixteen loops and reserve 1.01. Unless another exact receipt is found, one pre-freeze execution of the selected operand set is necessary to verify the chosen mode. It is not a search or a feasibility requirement; preserve all resulting failures, including exact-current-boundary behavior.
