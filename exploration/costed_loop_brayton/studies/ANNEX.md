# Package annex — costed_loop_brayton

[AGENT] Goal `design-study-parameters`, WI-094. This package is the WI-093 C-1 assembly (the Stellaris helium primary loop feeding the ARIES three-stage Brayton chain) with the ARIES purchase, fuel, ledger and lifecycle definitions instantiated on it from existing definitions only; its comparison contract is `work/orchestration/goals/design-study-parameters/evidence/comparison-contract.md` (v2, fresh-reviewed). Identities are recorded in `../census.json`, `../costed_loop_brayton.snapshot.json` and `interface_data.py`; the package's own manifest is `manifest.json` beside this file.

## Baseline pin

The manifest's baseline point is the contract's starting point: the C-1 design values with the re-selected inventory I-R (compressor 3,200, turbine 7,000, generator 3,600, heat rejection 5,000, helium duty 3,500 MW; exchanger 50,000 m²), cycle flow 2,500 kg/s, stage ratio 1.5182944859378311, every other input at its design default. Its headline is `costed_loop_brayton__plant__lifecycle_price__evaluate__lcoe` (no-breeding-credit convention), and every one of its nine checks is expected satisfied. The receipt behind it is `work/active/WI-094_costed-loop-brayton/evidence/native_runs/c1-aries-ratios-reselected-ratings/result.json`, whose C-1 channels equal the sealed WI-093 receipt exactly. Stock strict loader, `PreparedListStrategy` and `StudyRunner` through `study_route.py`; glue ledger none; no runtime adapter.

## Declared ties

None. The three stage ratios (`compressor_1__selected_ratio`, `compressor_2__selected_ratio`, `compressor_3__selected_ratio`) are three independent chosen inputs; a study that moves them together declares that as a scenario (the ARIES designer's equal-stage choice), not as a physical tie, in its own `axes.json` note.

## Oracle

`oracle_entry.py` (manifest `oracle` block) is an independent re-derivation of the loop, the Brayton stages, the single-branch closure, the electrical balance, the screens, the purchases, the capital chain, the fuel chain, the replacement schedule, the ledger and the lifecycle accounts, publishing `operand_bindings()` for the nine constraints (two operands are input attributes: the energy tolerance and the rated loop flow) and `comparison_catalog()` for the channels it re-derives; the manifest's objective catalog is that catalog. It reuses the key-agnostic ARIES arithmetic helpers `equipment_oracle.py` and `lifecycle_oracle.py` by import and imports nothing from any generated package. It checks the implementation of the model's assumptions, not their scientific qualification.

## Validity masks

None. Refusals in the candidate range are the bodies' own guards: nonpositive net electricity refuses the lifecycle price (`LCOE undefined for nonpositive net electricity`), and a recuperator hot side colder than the precooler target refuses the Brayton conditioning stage (`cooler outlet must not exceed inlet`). A study scans its candidate range with the oracle first and reports the refused points as the scanned edge (runbook step 7).

## Interpretation

Within one inventory every LCOE numerator term is a constant of a flow/ratio sweep (contract § 6, reviewed), so the operating ranking by LCOE is the ranking by net electricity; the cost side decides the value of a net gain and the comparison between inventories. Fixed machine efficiencies are a declared model assumption (contract § 8 a): the operating claim is scoped to the region near the 2,500 kg/s design flow, and rankings between flows far from it are model exploration. Absolute LCOE is conditional on the rest-of-plant constant and the no-credit fuel convention; paired delta-LCOE at equal fuel is the comparison.

## Replay

Use each frozen record's `replay.md` in an isolated directory with its sealed package and exact licensed runtime; never rerun into a frozen record. The development cases replay through `../run.py --root <scratch>` and verify through `../verify.py --runs <scratch> --out-dir <scratch>`.
