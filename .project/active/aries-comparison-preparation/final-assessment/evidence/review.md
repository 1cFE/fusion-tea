# Independent assessment review

[AGENT] Fresh non-author review under `audit-models`, 2026-09-20. Scope: finish the retained ARIES comparison against original B-2–B-8 without changing models, input choices or scenarios. The examined model is the frozen `post-reveal-v1` archive, SHA256 `d65d6ea44517dba3d9012d06706e74fe3006247e2809f6b4bdd64edd85ab5a7a`; the retained diagnostic report is SHA256 `25a779df33560e33171f61b1c5fe598c78fba5af8b8b7d1db9851a8af0d0d529`. Reporting checkpoint: `5f8658b6ee4c183fb30ad429af7b9b334e60a164` plus the final reporting artifacts identified by [review-checks.json](review-checks.json). **PASS for this completed reporting scope.** Final report, costs, replay instructions and preservation receipt are included in the examined hashes.

## Findings and criterion review

[AGENT] The substantive assessment is supported. No unresolved material finding in the examined source/model interpretations. The overall comparison does not pass; a positive review here concerns accurate completion of reporting, not engineering qualification.

| Criterion | Independent finding |
|---|---|
| B-2 subsystem correspondence | **Fail is defensible.** I challenged whether an omitted circuit inside an existing heat-transport subsystem warrants failure of the broad checklist. Raffray p734 assigns 1,444 MW to PbLi heat removal, and p736 Figure 12 shows its separate exchanger branch. The frozen model's blanket-to-primary-loop binding and helium/HITEC equipment do not represent that branch. This supports a first-order missing ARIES correspondence. It does not mean the model lacks overall heat-removal capability. |
| B-2 radial sequence | **Qualitative pass supported.** Lyon p699 Figure 5 and the cumulative-radius model retain the prescribed order. Local sectors, thicknesses and fit remain unqualified; this pass cannot certify geometry. |
| B-2 cost coverage | **Unresolved is supported.** Account families are present, but several equipment and aggregate boundaries cannot be reconciled. The report correctly distinguishes Najmabadi's 26/27 numbering from Lyon's 27/26 numbering. |
| B-3 quantities | **Not established is supported.** Checked all 35 dispositions and producer identities. Lyon pp696/699/708 identify the pack dimensions; the two ratios and area product describe selected geometries, without independent sizing credit. Source mass is not model volume, and bundled plant-plus-cryogenic electricity is not a cryogenic-only denominator. |
| B-4 costs | **Not established is supported.** Checked all 35 rows and 21 printed candidates against Lyon pp707/709. Nominal ratios remain descriptive across mixed or unresolved price years and equipment scopes. Frozen bindings distinguish supplied purchases, selected cost classes and inventory calculations. The large winding ratio is a transfer-assumption finding, not an established cost overprediction. |
| B-5/B-5a | C220107 remains excluded and visible, including ancestor disclosure. Selected geometry earns no optimization credit. |
| B-6/B-8 | Axis verdicts and model/reference ratios are explicit. The 276-row denominator is preserved. Numerical non-comparability is not mislabeled as a formal pass or accuracy failure. |
| B-7 | Reuse of the existing local raw-PDF fidelity receipt is appropriate. Its external AACE scope observation remains inherited. The report claims neither fresh standard verification nor probabilistic accuracy certification. |

## Independent checks and limits

[AGENT] Directly viewed eight retained images: Najmabadi p663; Lyon pp696, 699, 707, 708 and 709; Raffray pp734 and 736. Reviewed frozen/live model identity and relevant heat-transport, pack-fit and cost producers. The source numbering discrepancy was surfaced during review and is now explicit in the final cost/report prose. Initial assembly replay differed after a concurrent C220108 wording update; regeneration resolved it without changing numerical evidence.

[AGENT] Ran `.codex-test/run python .project/active/aries-comparison-preparation/final-assessment/evidence/review-checks.py` because final integrated reporting, preservation and replay needed an independent receipt. It verifies all 276 original rows exactly, all 70 reviewed numerical rows and their producers, all 52 frozen model files, and all 1,322 protected files. Quantity and assembly replay match exactly; the cost script's three outputs reproduce byte-for-byte in a temporary directory. Counts are 21 nominal cost pairs: eight inside the original interval, three below and ten above, including excluded C220107. No supported-prediction credit is introduced.

[AGENT] Independently checked the report's 103 field-unaffected rows: 24 selected/supplied, 35 quantity dispositions, 35 cost dispositions, eight retained diagnostics and one undefined breeding diagnostic (`achieved_tbr`). The separate domain limitation remains visible; field independence has not been promoted into model-definedness or scientific validity.

[AGENT] No plant execution or full regression rerun was needed for these reporting-only changes. Prior diagnostic/runtime review retains its original scope. The validation matrix's existing MFE physical and relationship criteria are not newly resolved by this comparison; no registry status was changed. This review does not qualify field physics, breeding geometry, equipment offers, manufacturing scope, price escalation or full-plant LCOE.
