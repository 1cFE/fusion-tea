# Magnetic-field qualification: result and next dependency

**We cannot yet qualify the field calculation for the published Stellaris coil family. The missing inputs are now specific: the original coil curves and plasma boundary, plus the finite winding-pack placement and a matching field-evaluation definition.** The method is available; the acquired data are insufficient to apply and validate it for this configuration. No field equation or empirical range was changed.

## What we established

- The primary paper specifies **six different coil families**, their currents, turns and square pack dimensions. Those tables do not specify the three-dimensional coil paths. The paper says its data are available on request. [Local source inventory](evidence/local-inventory.md).
- The published peak fields come from a **finite-pack magnetic calculation**. One axis/peak-field pair cannot determine the effect of independently changing pack size. Eight exact algebra checks demonstrate this ambiguity; an independent reviewer reproduced them. [Proof and limits](evidence/identifiability.json).
- The six family columns are **not six pack-size experiments**. Each family has a different shape/current and interacts with the other coils. Fitting one response curve across those columns would not identify the missing pack-size dependence.
- Proportional current changes at fixed geometry and complete geometric scaling have justified **relative** responses under a linear magnetostatic assumption. They do not validate the absolute calibration or establish that arbitrary scalar-radius changes preserve the real coil geometry. [Supported-use contract](capability-contract.md).

## What the public-data search found

The official public CAD repository describes a simplified **scaled W7-X** model. It is not evidence for the named Stellaris baseline. A newer author dataset is a real lead, but its inspected landing page and filename preview do not establish that it contains the baseline inputs or finite winding-pack definitions. [Initial search](evidence/external-inventory.md).

A focused follow-up acquired a pinned author script that explicitly loads `tests/test_files/input.stellaris` and `tests/test_files/coils.stellaris`. It describes the plasma boundary as available on request. It loads original coils separately from the alternative coils it optimizes and writes. Neither original input file was acquired. The uninspected archive remains unresolved; we are not claiming that these files are unavailable publicly. [Follow-up and exact source lines](evidence/external-followup.md).

The associated paper hit the existing source-registry hold-out screen and was not added to the shared source library. The isolated author script was registered normally. The [acquisition workflow](../../../../.claude/commands/research-acquire.md) states, “A hold-out match is never yours to waive.” This is a limitation of that acquisition path, not evidence that the dataset lacks the needed inputs. No rejected paper was cropped or re-registered to bypass the decision.

## What can be claimed now

The current field values remain calculations of the declared approximation, with scientific applicability unqualified. The completed partial assessment already carries that limitation through its dependencies. There is no new corrected magnetic field, validated wider design envelope or supported LCOE from this work.

The qualification review is complete with an unresolved data dependency. **The field-model repair itself is not complete.** Designing a new coil family, digitizing a rendering or choosing coefficients to reproduce a field value would change the question rather than supply the missing evidence.

## Recommended next action

Obtain and authenticate the original `input.stellaris` and `coils.stellaris` files, then obtain the pack frames and reference field setup needed for conductor peaks. I prepared an [unsent data-request draft](data-request-draft.md). The published data-availability statement and named files make this a concrete request. Screened inspection of the remaining author archive is another acquisition route; it is not yet a verified source of those inputs.

Once the data arrive, the [capability contract](capability-contract.md) specifies the calculation and checks: signed family-current superposition, finite conductor geometry, axis convention, independent pack-size response, numerical convergence and separate validation points. Geometry, current and winding packs remain supplied design choices. A different publicly available coil set would require an explicit choice of a different design.

## Evidence

[Independent scientific review](evidence/review.md) · [write-up findings](findings.md) · [pending research record](../../../../knowledge/research/pending/20260920-195420_stellaris-field-qualification.md). Source captures, acquisition failures and unresolved candidates are retained. No plant rerun, shared-runtime change, source-field substitution, external message, push or merge occurred.
