# Independent verifier status

The accepted design equations and reviewed cryogenic correction are implemented in `exploration/whole_plant_conversion/verify.py`, `oracle_whole_plant.py` and retained oracle support. The verifier imports no production numerical body. Final development comparison passes. All 498 historical replay cases also pass; see `verification-report.md` for complete numerical evidence.

## Evidence completed

- `conversion-port-manifest.json` and `conversion-port-check.json`: the previously verified conversion oracle was ported with reversible namespace, package and source-path changes. Its six source files were unchanged; 116 gas/loop outputs were bit-exact under the namespace substitution. The retained 498-case study was not rerun.
- `capture-check.json` and `capture-report.md`: 93 independent geometry, current, material, procurement and cryogenic outputs agree with the exact 48 kA native capture. The supplied 35.5 W/m³ assumption is explicit; transport and global-construction qualification remain zero.
- `semantic-checks.json`: 69 independent equation checks pass, including every common capital leaf and branch slot, fuel mass balances, isotope recovery/extraction effects, strict event horizons and zero discount.
- `authored-checks.json`: 48 authored-binding checks pass, including source2500/2800 demand changes with capital invariant, isolated branch quote changes, mean nuclear heating35.5/50/80 W/m³ and extra cold10/13 kW. These checks confirm downstream refrigeration, auxiliary heat and export propagation. They are oracle checks, not native execution receipts.
- `oracle_fuel_inventory.py` is a byte-identical copy of the previously independent deterministic-delay startup inventory oracle at `exploration/stellarator_e2e/oracle_fuel_inventory.py`.

## Numerical conventions

Every native scalar output is required to have an independent equation, except solver iteration diagnostics. Every native predicate is checked using independently derived operands and the authored predicate definition. The public adapter exposes `evaluate`, `operand_bindings`, `comparison_catalog` and `absolute_tolerances` for the stock study verifier. Generated scalar `.root` references are mapped to their scalar output channels.

Relative agreement is1e-9. New normalized isotope residuals use1e-12 absolute tolerance, cost cancellation residuals1e-4 USD2025, and power residuals1e-9 MW. Existing conversion solver residual classes retain their prior tolerances. These are arithmetic cancellation tolerances; capacity predicates receive no margin tolerance beyond the declared native domain convention for tiny primary motor cancellation. Costs, masses, duties and each predicate operand are also compared individually.

## Current limits

The source is conditional and unqualified. The fixed capture establishes local model checks under its declared assumptions, not qualified plasma sustainment or global construction. Nuclear heating is an uncertain independent demand. The hot-source multiplier applies to blanket/shield heat and excludes cryogenic deposition, so the reviewed heating scenarios leave source inversion and fuel demand unchanged. Independent arithmetic does not establish the physical validity of that transfer.

The final generated public surface has 637 inputs, 1,192 independently compared scalar outputs, four solver iteration diagnostics and 125 predicates. The 35-case development battery passes; the independent integration review remains required before main-study ranking.
