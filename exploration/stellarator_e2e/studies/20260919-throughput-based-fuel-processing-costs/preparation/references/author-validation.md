# WI-070 implementation evidence

The active stellarator account now consumes WI-069 per-module running D+T exhaust, applies the four reviewed source rows and direct installation, and multiplies identical module costs by module count. The full selected C220500 enters CAS22 once. Its old $120,746,472.201428 power proxy remains an explicit legacy output and dormant route. The attached processor stock remains per module; its selected capital interface is plant-total and also works in legacy mode.

At the unchanged native baseline, purchased/fabricated equipment is $20,443,419.58326817 and direct installation is $2,342,809.820525226, totaling $22,786,229.403793395 in 2025 CPI purchasing power before generic charges. The current CAS29 rate is 0.1; the freight exclusion is therefore $2,577,090.802577749. Total capital changes from $18,059,442,217.470905 to $17,918,171,013.726093. Headline LCOE changes from $273.4546494372188/MWh to $271.5843199172948/MWh. These are conditional limited-scope estimates, not current procurement quotes or proof of plant feasibility.

## Identity and accounting

`baseline-delta.json` records 928 entering versus 956 current outputs, 906 versus 934 independently mapped outputs, 28 added channels and no removals. Exactly 13 entering channels change, all in the declared financial path. All 25 constraint IDs and their verdicts are unchanged; the 26th response key is the synthetic headline. Full entering/current response sets are retained. There is no new engineering constraint.

The public input contract has 489 entries, an increase of the 19 explicitly declared source/configuration parameters. The 27 processing outputs and one installation freight-exclusion output are independently mapped. A false source-conditions declaration keeps diagnostic costs but exposes applicability zero. Undefined breeding preserves physical plasma exhaust and a conditional processing estimate while the inherited breeding verdict fails. Disabled inventory with active processing refuses execution.

C220500 owns the local controls included in its four packages. C220700 retains an explicit, distinct supervisory/plasma account with its unchanged coefficient labeled an uncalibrated residual allowance. This agent allocation establishes modeled single ownership; it does not claim historical price decomposition. Existing civil facilities, recurring fuel, startup proxy, tax, insurance, indirects and finance keep their documented scopes. Freight excludes process installation and its CAS29 contingency; source equipment remains under the inherited freight proxy.

## Verification

- `source-domain-tests.log`: 172 tests pass against both the independent helper and production seed, including all 27 outputs against 60-digit Decimal arithmetic, dated source rows, source/current capacity anchors, module/margin/price/zero limits, invalid flags and finite domains.
- `affected-tests-reconciled.log`: 263 tests pass, covering public operating-flow/price/date/margin scenarios, every mapped output, all nonfinancial-output invariants, unchanged verdicts, undefined breeding, disabled inventory, source-condition applicability, typed module scaling and zero limit, calendar independence, actual supplementary shipping/contingency consumers, inherited fuel inventory and facility regressions. The 46 warnings are retained pytest/Pydantic warnings, not skipped checks.
- `family-tests.log`: 13 tests pass, including canonical/twin identity, fresh generation and current public ABI/census.
- `generation-final.log`: two fresh generated packages match byte-for-byte. There are 36 normative seeds: 34 inherited bodies unchanged, one existing shipping guard changed and one new processing body. `candidate-seeds.json` and `changed-seeds.json` retain exact hashes. `cumulative-generation-changes.json` compares all 67 generated-file changes against audited WI-069, rather than only the final documentation regeneration.
- `repin-final.log`, `baseline.json`: native baseline agrees across all 934 oracle-mapped scalars; manifest producer metadata, structural snapshot and census match this package. No historical study record was rewritten.
- `native-validation.log`, `static-delta.json`, `static-classification.md`: complete native validation exits 1. L1/L3/L4/L5 pass; L2 retains exactly its 10 issue identities; L6 adds three pure EXPOSE dot-reference errors and removes none, increasing 1,079 to 1,082. This is a documented static limitation with separate executable binding evidence, not a validator pass.

## Test repairs and limitations

Original failed runs remain in `native-processing-tests.log`, `affected-tests.log` and `affected-tests-final.log`. The first three failures omitted the existing CAS90 financing output from a test's financial-change set. The next failures were direct wrapper calls missing explicit generated formals or reading a single scalar with `.cost` instead of `.root`. The last three were old facility expectations: two frozen WI-068 monetary replays now explicitly select legacy processing; the facility-disabled oracle freight expectation includes the separately active process-installation exclusion. No production equation changed to satisfy these failures, and physical comparisons were retained.

The initial regeneration rejected handwritten functions without explicit tuple return annotations. The corrected typed signatures preserve the reviewed calculation bodies and satisfy the generator's strict signature preservation. The independent reviewer also found negative-legacy-price and Boolean-numeric domain differences in the oracle; those were repaired with additional counterexamples before release.

Independent implementation audit, coordinator native integration and focused native study remain downstream obligations. No git, goal or study execution was performed by this author. Existing package manifest changes are explicitly authorized producer metadata.

Native verification records SV-117 and SV-118 are marked passing after these executed checks. This is author verification, not independent audit or goal closure.
