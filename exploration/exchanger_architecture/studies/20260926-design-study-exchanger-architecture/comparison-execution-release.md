# Comparison execution release

2026-09-26. [AGENT] Narrow corrective and preparation review by the same independent reviewer. Reuses the substantive coverage in `comparison-review.md` and the corrective document coverage in `comparison-review-r2.md`; neither historical review is changed.

**Verdict: PASS for the prepared comparison, conditional on the pre-execution record completion below and continued gate validity. No additional owner gate is required.** This releases the reviewed conditional downstream study, not a scientifically qualified plant recommendation.

## Checks completed

The reviewer independently compared actual JSON input maps using `.codex-test/run python` assertions. `baseline-control.json` equals the complete sealed `nominal-calculated` row. The prepared `control-calculated-N` input map equals the original map exactly. The `control-supplied-N` alias resolves to a retained main case and differs only in producer mode, 1 to 0, and supplied fusion, 2436 to 1835.4512830147435 MW. Every main/control case retains pressure loss 0.045. F1 is resolved in both the contract and executable preparation.

The final proposal contains 648 unique cases and two aliases. All 648 have finite independent-oracle evaluations and remain retained; none was refused. Engineering failures remain in the proposal rather than being removed by the economic selection. The selection chooses best passing tested operating settings, preserves ties within 0.01 MW, and does not resize equipment. Added zero-tritium-price cases reprice the common input used for both initial inventory and annual purchase. Native execution and independent numerical verification remain subsequent obligations.

All six preflight gates pass: declared keys, sibling scan, identity, manifest currency, baseline headline and clean package. The unchanged executable fingerprint is `f739dbce67699b7adfae7c1adf5599ab7c30e85987caad53e0f8affd9b880ce4`.

All ten indicator groups are valid with `no_constraint_response=false`. Source load, architecture, cycle flow and branch split are correctly framed as search; source-mode replay and U, pressure-loss, pump-mode/power and fuel-price scenarios are sensitivities. A possible path through a module does not establish real constraint response. In particular, a fuel-price change does not create engineering resistance or qualify tritium supply.

## Conditions before native main execution

1. Replace the preparation placeholders in record sections 2, 5, 6, 7 and 8 with the declared intake, framing and indicator interpretation, including the missing actual fuel-price resistance and supply qualification. The owner already requested tests of fuel assumptions; this is an agent-selected endpoint within that authority. Amend the axis-plan wording accordingly or add an explicit correction identifying the earlier wording.
2. Preserve the reviewed finite candidate set and failed-case ledger. Continue only while preflight identity/cleanliness checks remain valid. Newly added physical axes or changed accounting require applicable review; routine reporting corrections do not.
3. Verify every executed retained point through the declared oracle and exact predicate comparison before interpreting results. Keep primary hot/return and terminal differences labeled native diagnostic outputs, outside the current independent oracle catalog. All economic rankings still require positive net output and every implemented engineering predicate to pass.

## Reviewed evidence identity

All paths below are relative to `exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture/`.

| Artifact | SHA256 at review |
|---|---|
| `proposed-points.json` | `259b2ae07fdcdaecd55861c6cb31f93bc067ad2a5a1b79c82f3e09751de65bdd` |
| `axis-plan.json` | `824499f17ad82215b78ee7d2d75ddab6381304c5bd8eeaa849cfb32f81b49fcb` |
| `indicators.json` | `323bfe7c98e94c1336dd0e581c4b20d339cc18ff780297cbde8fec83f74c2607` |
| `oracle-window-scan.json` | `eab8f0bdee274ae8a375689a4b2bfcd060a977c600a4dc9dd8fe31c01eb80fb0` |
| `preparation/preflight_results.json` | `85b82081f17dcf13e9db82c42366027c5b45004ae41022b00cb5787a61c05e9d` |

The promised framing/authority record edits may change their own digests without changing this reviewed numerical proposal. The coordinator records their completion; another review turn is unnecessary for those specified corrections.
