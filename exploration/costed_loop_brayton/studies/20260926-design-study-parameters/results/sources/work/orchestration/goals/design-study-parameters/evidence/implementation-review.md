# Implementation review: WI-094 costed loop-Brayton (fresh, executed evidence)

**Verdict: PASS** (three notes, none correct-before-use). Scope: the brief's five questions against `spec.md` R1–R8 and `design.md` § 1, 3, 4, 6, 7; `report.md` did not exist at review time. Nothing was run.

## 1. Reuse rule — met

`build-hashes.json`: 24 bodies, all `prefix_only: true`, `typed_adapter: false`, `reviewed_body_ast_unchanged: true`; `fixed_point: true`; `sources` and `staged` digests identical for all 12 files, and I recomputed the canonical files' sha256 today: all 12 match. The flag is earned: `build.py:152-156` regenerates twice and asserts equal tree hashes before writing the receipt. I diffed three bodies (`lifecycle_cashflow_accounts_impl.py`, `primary_coolant_loop_impl.py`, `selected_inventory_purchase_impl.py`): only `from aries_integrated.` / `from stellarator_tea.` → `from costed_loop_brayton_tea.` lines differ.

## 2. Control replay — met

`summary.json`: four positive-net controls `control_exact: true` (131 channels, 8 verdicts each, zero differences); the 4,000 kg/s case refused with `LCOE undefined for nonpositive net electricity`. I compared `c1-aries-ratios-reselected-ratings` against the sealed receipt: `net_electric` 426.57863661707336, `unmet_heat` 0.0, `q_ihx` 3301.2132114869937, equal under the prefix map. The stored traceback shows the raise in `lifecycle_cashflow_accounts_impl.py:15`.

## 3. Identities — met

`verification-summary.json`: `passed: true`, 7 cases, `failures: []`, tree clean. `verify_case` (`verify.py:69-152`) recomputes from stored inputs and outputs in Decimal: each purchase as reference cost × factor × selected / reference with the 0.5–1.5 flag, priced total, direct, indirect, contingency, owner, overnight, export MWh, tritium makeup and cost, annual operating, replacement count, the eleven contributions summing to `lcoe_sum`, and `lcoe_sum` = `lifecycle_price.lcoe`. Not a self-comparison.

## 4. MR-7 on executed evidence — compliant for the affected scope

`best-screen-point-aries-ratings` and `c1-aries-ratios-aries-ratings`: compressor screen violated (margins −560.8 / −851.5 MW), helium-duty screen violated (−1801.2 MW), while the booked purchases are 78,639,500 and 32,403,166.67 at `purchased_quantity` = the selected 1,600 / 1,500, `extrapolated` 0. The assembly binds `quantity_in = compressor_capacity.selected_rating` (`costed_loop_brayton.sysml:519`; 595 for helium duty; `selected_area` at 186): purchases read the chosen rating, never a demand. I-R receipt: compressor 157,279,000 (×2.0), turbine 251,646,400, generator 94,367,400, rejection 112,172,000, helium duty 75,607,388.89 (×2.333), each `extrapolated` = 1; exchanger 58,325,700 at ratio 1.0, `extrapolated` = 0. Six of six.

## 5. Preservation and registration — met

`preservation-check-t004-build.json`, `-run.json` (and `-seam.json`): `passed: true`, 20,973 protected files, none changed or missing. `tests/model_families.py:194-207` lists exactly the eleven staged library files plus the design file, in build order.

## Findings

- note: the 4,000 kg/s receipt records `refusing_module: null`. `run.py:56-58` looks for a `costed_loop_brayton__…` key in the traceback, which names a file path instead. Design § 6 promises the refusing module; the stored traceback carries it, the summary field does not.
- note: `verify.py:169-176` checks the controls from `summary.json`'s `controls` block, so `controls_exact` restates run.py's comparison rather than re-reading the sealed receipts. My three-channel check covers one case independently.
- note: `c1-aries-ratios-aries-ratings` also violates `rejection_capacity__capacity_ok` (−120.7 MW), consistent with the sealed baseline; reported, not hidden.

## Missing evidence / uncertainty

- R7 (study tooling, integration CANDIDATE) not assessed: the brief excludes the oracle and manifest.
- R4 grading seen only in the design table and the exchanger doc line, not every value in the assembly.
- The refused control compares zero C-1 channels by construction; the bit-exact claim rests on the four positive-net cases.
- Bodies diffed: 3 of 24; the rest rest on the build's AST assertion and recorded digests.
