# Offered thermal capability implementation

[AGENT] Implements the released `round2/architecture-review.md` contract. The machine-readable binding and migration contract is `capability-contract.json` beside this record. It specifies 49 new offered-rating/state inputs, 32 scalar screens, five state comparisons, four demand-conversion occurrences and nine new guarded calculation seeds. The earlier IHX assertion is additional. Source model and canonical twin changes are complete; native generation, numerical capture agreement, independent oracle migration and final acceptance remain coordinator-owned.

## Behavior

The generic screen checks finite nonnegative supplied rating and active demand. It retains the raw rating-minus-demand margin and reports separate applicable, supported, evaluation-defined and capacity-result outputs. Its constraint requires evaluation-defined at least one and margin at least zero. Unsupported and inactive results never obtain affirmative capacity credit. Physical qualification flags in the underlying equipment calculations remain unchanged.

Helium, salt, steam, water and cryogenic packages compare finite actual conditions against separately supplied point conditions. State identity uses the reviewed fixed eight-ULP rule: finite values with exact equality or absolute difference at most eight times their larger ULP. The multiplier is hard-coded, with no tolerance input or absolute floor. This is a point-rating restriction, not an inferred operating envelope. Helium additionally requires the actual primary-loop mode; salt requires the actual secondary-energy mode. Their mode inputs must be numeric zero or one. Disabled equipment and zero mode return not applicable, unsupported and undefined before condition arithmetic. Steam/water use actual active outputs. Intercept refrigeration also requires its thermal-inventory demand to be available. Gross electric and represented magnet electrical screens claim only the named real-power ceiling; they introduce no voltage, reactive-power or DC-current qualification.

Rating values reside on their component or package owners. HP/LP flow and shaft ratings, steam-generator/reheater conductance, condenser rating and feed/condensate pump ratings belong to the existing child component occurrences. The electric gross rating has one owner and is shared with the WI-079 price law. WI-079 separately owns package purchase amounts. Supplying a different rating at the same quoted/assumed amount describes a different hypothetical offer, not a predicted free upgrade.

## Generation findings repaired

The first generic helper exposed literal scale/divisor/offset values as public design inputs. It was replaced with three fixed-purpose calculations: cold MW to W with factor 1000000 inside the body, pump outlet-minus-inlet pressure, and total salt-pump electricity divided by actual machine count. Salt conversion uses the derived salt applicability (equipment enabled and actual secondary-energy mode one), and short circuits when inactive to avoid dividing dormant zero carriers. No caller-controlled conversion coefficient remains in the contract.

The parser treats `defined` as reserved. Calculation outputs use `evaluation_defined`; owned EXPOSE names still end in `_defined`, and formal bindings are unchanged. The single-output calculation ABI is a scalar float; multi-output wrappers return values in generated schema order. Native package generation remains the check of that ABI.

A mechanical wrapper annotation edit temporarily corrupted an old cooling dictionary index. Focused old-output tests detected it, it was corrected, and all seed tests pass again. The historical WI-078 seed remains untouched.

## Evidence and remaining acceptance

- `.codex-test/run agentic-mbse validate --level=1 models/`: 48 files, zero errors and warnings after the fixed-purpose conversion/mode corrections.
- `.codex-test/run python -m pytest tests/models/test_supplied_thermal_capability.py -q -k 'not native'`: 31 passed, 37 native cases deselected pending generation. Tests exercise every offered-state condition, adjacent/eight-ULP/nine-ULP state boundaries, strict adjacent-number capacity margins, inactive/unsupported behavior, invalid values, zero-count dormant conversion and preserved IHX outputs/cost behavior.
- The same test file defines 32 per-dimension native offer cases and five native state-mismatch cases. Missing public inputs or native assertions fail fixture admission; there are no missing-interface skips. Additional integrated demand perturbations and package replacement offers remain the coordinator's acceptance scope.

The independently reviewed fixed eight-ULP identity rule accommodates nearby binary representations of point conditions. Differences exceeding that rule must be surfaced and investigated; the rule must not be widened to obtain a passing result. Capacity margins remain strict and unsnapped. Entering defaults are explicitly assumed offers captured at checkpoint 53a0366a, not vendor ratings; native matching still requires verification.

Numeric output keys in `capability-contract.json` use the actual native calculation producer (`owner__name_capability__margin` and `__evaluation_defined`). Source EXPOSE aliases remain the plant constraint formal bindings; the route does not emit those aliases as separate numeric channels. The contract records both without substituting one for the other.

A fresh generation attempt found a semantic input-order mismatch that syntax-only L1 did not detect: helium/salt usages listed mode before enabled, while their definitions declared enabled before mode. Their usage bindings now follow definition order. No interface names, equations or seed ABI changed. Direct `syside.try_load_model` over all 40 canonical twin files reports zero parser and zero semantic errors. A kept semantic regression now covers this failure; the focused non-native selection passes 32 tests with 37 native cases deselected. This supersedes syntax-only evidence for binding type correctness; full code generation remains coordinator-owned.
