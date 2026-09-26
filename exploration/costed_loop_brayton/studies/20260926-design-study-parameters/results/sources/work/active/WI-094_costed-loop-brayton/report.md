# WI-094 report: costed loop-Brayton assembly

**Status:** implemented and reviewed (fresh implementation review PASS with three notes, 2026-09-26); integration seam CANDIDATE. The item stays `active` until the goal's study (`20260926-design-study-parameters`) has run on the package; closure is the owner's.

## What was built

- `models/designs/costed_loop_brayton/costed_loop_brayton.sysml`: package `costed_loop_brayton`, root part `plant`, the WI-093 C-1 assembly with unchanged bindings and values plus the ARIES purchase, fuel, ledger and lifecycle definitions instantiated from existing definitions only (design § 1, § 3).
- `exploration/costed_loop_brayton/{build,run,verify}.py`, the generated package `costed_loop_brayton_tea/` at a fixed point (executable `a4c7a87136fe3ea373fb02a899ed8262a800a7443891db986411f00f26c8aeea`, semantic `76c68dde7a4de41987be07ecd3ac3bdf814c6ef1895f3ad8d2250275cf9bdee7`), `costed_loop_brayton.snapshot.json`, `census.json` (163 entry points).
- Study tooling under `exploration/costed_loop_brayton/studies/`: `study_route.py`, `interface_data.py` (163 entry keys, 245 channels, 9 constraints), `oracle_entry.py` (fresh worker; 244 catalogued channels, nine operand bindings), `manifest.json` (pin `53f48a7e563b7cacf81a0ca2fc14ab5c5a146aab2360482effb33031a0e0fd51`, six declared absolute tolerance classes), `prepare_interface.py`, `execute_study.py`, `study_support.py`, `flow_ratio_config.py`, `axes.json`, `ANNEX.md`, `DISCOVERY_LOG.md`.
- Registration: the `costed_loop_brayton` collection in `tests/model_families.py`.

Commits: `72fb8c08` (part 1: assembly, package, cases, controls), `1c4d1894` (part 2: interface record, composer, verifier rule), `1d0ef2ef` (part 3: oracle, manifest, axes, configuration).

## Acceptance against the spec

| Req | Evidence | Outcome |
|---|---|---|
| R1 reuse only | `evidence/build-hashes.json`: 24 copied bodies, every one `prefix_only`, `reviewed_body_ast_unchanged`, `fixed_point: true`; no new definition in the assembly (design § 5; review Q1: three bodies diffed, only the import prefix differs) | met |
| R2 held-equal constants | assembly parts `fusion_source`, `rest_of_plant`, `replacement_scope`, `fuel_inventory`, `annual_om`, `finance` with their bases in the doc lines; values equal the contract § 3 / § 6 | met |
| R3 MR-7 roles | purchases bind `quantity_in` to the sibling screen's `selected_rating` / `selected_area` (review Q4: the I-A receipts keep the violated compressor and helium-duty screens with the booked price of the selected rating; the I-R purchases equal reference × selected / reference with the extrapolated flag on the five ratings and off for the exchanger) | met |
| R4 grades | design § 3 table and the assembly doc lines carry `[INHERITED: …]` / `[ASSUMED]` per value (review: seen in the design table and the exchanger doc line, not checked on every assembly line) | met, partial check |
| R5 control replay | `evidence/native_runs/summary.json`: four positive-net controls `control_exact: true` (131 channels, 8 verdicts each); the 4,000 kg/s control refused at `lifecycle_cashflow_accounts_impl.py:15` with `LCOE undefined for nonpositive net electricity` (review Q2 compared three channels against the sealed receipt) | met |
| R6 single-counted cost boundary, identities | `evidence/verification-summary.json` `passed: true` over 7 evaluated cases; `verify.py` recomputes purchases, capital chain, annual accounts, replacement count and the eleven-contribution sum in Decimal from stored inputs and outputs (review Q3) | met |
| R7 study tooling and CANDIDATE | `work/orchestration/goals/design-study-parameters/evidence/integration-t004/integration_return.json`: CANDIDATE, ten gates pass (pinned packages, teax `8d877460`, regeneration moved no byte, 43 handwritten files byte-identical, census recaptured, model-family spine, manifest pin, six preflight gates, oracle parity with every verdict re-derived, lineage); the oracle agrees with all seven evaluated development receipts at relative deviation below 1e-11 on every channel except the closure residual (absolute ≤ 5.8e-9 MW, inside its declared 1e-7 MW class) and refuses the 4,000 kg/s case | met |
| R8 registration and preservation | `tests/model_families.py` collection of eleven library files plus the design file (review Q5); `…/evidence/preservation-check-t004-{build,run,seam}.json` `passed: true`, 20,973 protected files unchanged | met |

## Development cases (USD2004; no-credit convention)

| Case | Net MW | Unmet MW | Overnight | LCOE USD/MWh | Checks |
|---|---|---|---|---|---|
| `c1-aries-ratios-reselected-ratings` (starting point, I-R) | 426.579 | 0 | 4,873,104,037.11 | 1,559.44 | 9 of 9 satisfied |
| `c1-aries-ratios-aries-ratings` (starting point, I-A) | 426.579 | 0 | 4,350,208,470.00 | 1,548.04 | compressor, helium-duty and rejection screens violated |
| `best-screen-point-reselected` (2,500 / 1.45, I-R) | 575.617 | 0 | 4,873,104,037.11 | 1,155.67 | 9 of 9 satisfied |
| `best-screen-point-aries-ratings` (2,500 / 1.45, I-A) | 575.617 | 0 | 4,350,208,470.00 | (stored) | compressor and helium-duty screens violated |
| `starting-point-fuel-term-wired` (S2 input override) | 424.789 | 0 | 4,873,104,037.11 | (stored) | 9 of 9 satisfied |
| `c1-flow4000-reselected-ratings` | refused | | | | lifecycle body: nonpositive net |

The full receipts are `evidence/native_runs/<case>/result.json`.

## Review notes and dispositions

Fresh implementation review: `work/orchestration/goals/design-study-parameters/evidence/implementation-review.md` (PASS). Notes:

1. `summary.json` records `refusing_module: null` for the refused control because `run.py` looks for a package-qualified key in the traceback text, which names a file path. Disposition: accepted as a receipt-format gap; the stored traceback names `lifecycle_cashflow_accounts_impl.py:15`, which is the refusing module; the receipts are left byte-stable rather than regenerated for one label.
2. `verify.py` takes the control verdicts from `summary.json` rather than re-reading the sealed receipts. Disposition: accepted as a disclosure; the sealed-receipt comparison is `run.py`'s, and the reviewer's three-channel check is the independent confirmation on one case.
3. The I-A starting point also violates the rejection screen (−120.7 MW), consistent with the sealed WI-093 baseline. Disposition: reported, carried into the study reading of inventory I-A.

Earlier reviews: design review PASS with five notes applied (`…/evidence/design-review.md`); contract review FINDINGS then PASS on version 2 (`…/evidence/contract-review.md`).

## Replay

From the repository root through the launcher:

```
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python exploration/costed_loop_brayton/run.py --root /tmp/wi094-replay'
.codex-test/run python exploration/costed_loop_brayton/verify.py --runs /tmp/wi094-replay --out-dir /tmp/wi094-replay
```

The build (`build.py`) regenerates the package from the staged sources and asserts the fixed point; the integration seam invocation is recorded in `…/evidence/integration-t004/integrate.log`.
