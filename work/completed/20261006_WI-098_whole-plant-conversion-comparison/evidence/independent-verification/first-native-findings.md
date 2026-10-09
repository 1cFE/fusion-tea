# First native integration check

The first31-case development battery has29 evaluated cases and2 domain refusals. Each evaluated case has1192 independently checked scalar outputs and125 predicates; four solver iteration diagnostics are excluded. `native-check-first.json` retains one discrepancy in every evaluated case. `native-behaviors-first.json` records71 passing cross-case checks. This is preliminary evidence before the final selected cryoplant interface and regeneration.

## F1: captured winding stress margin uses the source peak as an allowable

Native `supplied_core.evaluate.stress_margin_Pa` is250,640,000 Pa, corresponding to650 MPa minus399.36 MPa. The independent result is400,640,000 Pa, corresponding to800 MPa minus399.36 MPa. The retained capture input `magnet.casing.sigma_allow` is800 MPa; `models/designs/generic_mfe/mfe_plant.sysml:861–871` explicitly binds that allowable to the winding stress predicate. The650 MPa source number calibrates peak stress and is not the retained allowable. The author was asked to correct the captured margin. No oracle value or tolerance was changed to copy this discrepancy.

## Other results

Every other scalar and every predicate agrees across the29 evaluated cases. Negative extra cold heat and fractional lifetime are refused by both native execution and the independent equations. Both matched2500 MW and2800 MW cases satisfy all125 predicates and retain source, nuclear-transport and global-construction qualification0. The3000 MW case fails divertor and primary-pressure checks. Cryogenic80 W/m³ and extra13 kW cases fail cold capacity. Stock, processing, primary pressure, auxiliary rejection, operating net, annual net-grid energy, outage allowance, capture identity and path-count adversaries fail their intended checks.

Demand-only source and cryogenic changes preserve installed capital. Additional refrigerator electricity reaches export and standby demand, while refrigerator electricity plus extracted heat reaches the auxiliary sink without a duplicate coil-drive heat term. A gas quote change leaves common and steam capital unchanged. Lower extraction raises external tritium demand while keeping Li6 replenishment unchanged; lower recovery raises deuterium purchases.

## Replay

`.codex-test/run python work/active/WI-098_whole-plant-conversion-comparison/evidence/independent-verification/check_native.py work/active/WI-098_whole-plant-conversion-comparison/evidence/development/native/cases.json --out work/active/WI-098_whole-plant-conversion-comparison/evidence/independent-verification/native-check-first.json`

`.codex-test/run python work/active/WI-098_whole-plant-conversion-comparison/evidence/independent-verification/check_native_behaviors.py work/active/WI-098_whole-plant-conversion-comparison/evidence/development/native/cases.json --out work/active/WI-098_whole-plant-conversion-comparison/evidence/independent-verification/native-behaviors-first.json`

The receipt hashes identify the preliminary source rows. Final regeneration changes package identity and requires a new receipt rather than overwriting the meaning of this finding.
