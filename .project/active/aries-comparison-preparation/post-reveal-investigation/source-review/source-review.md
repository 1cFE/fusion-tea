# Published ARIES magnetic fields

[AGENT] ARIES reports **5.70 T on axis and 15.08 T maximum on the coils** in Lyon's systems paper, printed p708 Table IV. The latter is the relevant published quantity to place beside the model's reported conductor-field diagnostic of 56.62 T. These are different designs and presently unqualified field mappings; their difference is not a same-design model error measurement. [Inspected table](images/Lyon-page-14.png).

## What the papers actually report

| Source and location | Axis field | Peak coil field | Meaning and design context |
|---|---:|---:|---|
| Lyon, p708 Table IV | 5.70 T | 15.08 T | Final reference systems point: major radius 7.75 m, ribbon winding section 0.194 × 0.743 m. |
| Najmabadi, p657 Table I | 5.7 T | 15.1 T | Reference overview; axis field carries angle brackets and peak is Bmax. Values are consistent with the systems table at printed precision. |
| Ku, p677 coil-design discussion | 5.7 T | approximately 15 T | Explicit maximum in the winding pack, with the same ribbon dimensions and 18 modular coils in three shape/current families. |

[AGENT] Lyon p696 defines Bmax as the maximum field on the modular-coil winding pack. The denominator in its field ratio is the bracketed axis field, ⟨Baxis⟩. Thus the approximately 5.7 T number is a representative/averaged on-axis quantity, not a maximum experienced by the conductor. The inspected passages do not establish the exact averaging weight or a separate volume-average magnetic field. Do not substitute an RMS or volume-average plasma field for either quantity. [Definition page](images/Lyon-page-02.png), [overview table](images/Najmabadi-page-02.png).

[AGENT] The 16 T number on Lyon p708 is a design constraint, not the achieved operating maximum. The text explicitly places the achieved maximum below that constraint. Ku p677 Figure 5 normalizes another field-line plot to a Fourier component of 1.0 T; that plotting normalization is also not the reactor's axis or peak operating field. [Ku page](images/Ku-page-04.png).

[AGENT] The reference technology is Nb3Sn. Ku p677 links it to the high winding-pack field, and Najmabadi p669 specifies approximately 4 K operation. The investigated model instead retains its REBCO product at 20 K. Neither the reference operating point nor its Nb3Sn design limit licenses extending the model's REBCO performance approximation. [Technology page](images/Najmabadi-page-14.png).

## The reference field was already captured

[INHERITED: committed original evidence] At `829539f5eb7fde217d18318d1646a5e47103812c`, `current-readiness/revealed-results/c2-source-outputs/source-values.json` already recorded 15.08 T under `rows.peak_field`, citing Lyon p708 Table IV. The full repository path and immutable identity are in [field-candidates.json](field-candidates.json).

[AGENT] The latest comparison also retained that source record in [source-values-historical.json](../../post-reveal-results/post-reveal-v1/source-evidence/source-values-historical.json) and in the `peak_field` row of [observation-map.json](../../post-reveal-results/post-reveal-v1/source-evidence/observation-map.json). That row says the native model prediction is unavailable and scientific model validity is false. The missing comparison result arose from failed execution; it was not a missing reference datum. This audit makes the previously recorded reference explicit and rechecks its page images.

## Why geometry matters

[AGENT] The papers themselves show that the peak-to-axis ratio depends on winding geometry. Lyon p697 Table I gives ARE ratios of 4.02, 2.63, 2.10, 1.85, 1.70 and 1.59 for square winding sections with sides 0.2, 0.3, 0.4, 0.5, 0.6 and 0.8 m. These are a geometry study, not the reference ribbon section. Ku explicitly marks its square-section example as outside the reference design. This evidence supports auditing geometric applicability; it does not supply an automatically transferable multiplier. [Ratio table](images/Lyon-page-03.png).

[AGENT] Ku p677 and Lyon p697 identify 18 modular coils in three families. Lyon's introductory p695 prose instead says 24 coils. Preserve that source inconsistency; the explicit configuration table and physics discussion support 18 for the compared reference, but do not silently harmonize all paper revisions. The model's held turns/current and coil geometry do not reconstruct those families. The source's aggregate family currents do not resolve separate reference-coil turns and per-turn current.

[INHERITED: Raffray p726] The engineering paper warns that component analyses used somewhat different system parameters at different times and were not always rerun. The retained [historical extraction](Raffray-page-01-historical.md) provides that revision caution. This audit selects Lyon's systems Table IV as the primary field observation and retains overview/physics values as corroboration; it does not merge their subsystem dimensions into a new design.

[AGENT] Conclusion for the write-up: the reference coil maximum is about 15 T, and it was known in the retained comparison evidence. The approximately 56.62 T diagnostic belongs to a partially reference-specified model point with held equipment and an under-review field law. Explain and audit that calculation before interpreting the numerical gap. No source value was inserted into a model input, no field law changed, and no forward request executed in this source audit.

## Verification record

[AGENT] Used the PDF-analysis skill. Reused four exact committed page images and rendered two targeted pages from retained source PDFs at 200 DPI, then inspected all six images directly. [field-candidates.json](field-candidates.json) carries seven numeric field/limit candidates, physical definitions, printed precision, page indices, image/PDF hashes, prior capture pointers and the limits on averaging and comparability. Context extracts retain original Git paths in the verification record. No fresh web source or different paper revision was introduced.
