# Independent input review

[AGENT] **PASS for execution of the exact adopted request**, 2026-09-20, reviewer `/root/source_review`. No substantive transcription or quantity-definition error requires changing the request. This verdict permits the input-review gate to close; execution authorization comes from the owner's subsequent instruction to execute the adopted prompt. The reviewer did not author the adopted mapping, source selection, model, package, or request, and performed no physical model execution.

## Reviewed identities

The request SHA256 is `d5cdb3751ceb00ed52851ce5f232ada5f0f2dbf1b97adf9157d5dfb530a05560`. The authoritative repository location is `.project/active/aries-comparison-preparation/post-reveal-preparation/mapping/proposed-reference-request.json`. The accepted archive identity is `d65d6ea44517dba3d9012d06706e74fe3006247e2809f6b4bdd64edd85ab5a7a`, as bound in adoption.json. The coordinator separately owns archive restoration and execution verification.

I recomputed and matched every artifact SHA256 listed in adoption.json. I compared all seven retained mapping-evidence files byte for byte with `git show 829539f5eb7fde217d18318d1646a5e47103812c:<git_path>`, using the paths in mapping/evidence/index.json. All seven also matched the index SHA256 values. These include all four directly viewed page images and the original independent review, original source findings, and original input records. The original evidence commit remains the authority for their historical state.

I read the twelve generated input JSON files directly from the adopted tar archive, checked their inventory hashes, merged their 704 public keys, and verified that the 701 held values equal their archived values exactly. The three request keys are disjoint from the held inventory and together cover all 704 keys. All eight control defaults in contract.json match the archived generated inputs. No original aggregate ampere-turn input was added to the request.

## Source and definition findings

I directly inspected `mapping/evidence/lyon-p701.png`, `lyon-p702.png`, `lyon-p708.png`, and `najmabadi-p657.png`; their exact reviewed bytes are the index hashes verified against the original Git objects.

| Quantity | Finding |
|---|---|
| Major radius 7.75 m | Lyon printed p708 Table IV states 7.75 m. Najmabadi p657 Table I corroborates the average major radius. Admission as a nominal scalar is supported; plasma shape and volume correspondence are not established. |
| Minor radius 1.70 m | Najmabadi p657 Table I directly states averaged minor radius 1.70 m. Dividing rounded aspect ratio into major radius would be a weaker reconstruction. The source's average radius is accepted only with the contract's explicit geometric limitations. |
| Peak ion temperature 11.83 keV | Lyon p708 Table IV states central plasma temperature 11.83 keV. Lyon p701 explicitly assumes equal ion and electron temperatures; p702 Figure 12 shows the temperature maximum centrally. This supports the peak-ion scalar without substituting the source temperature profile. The density-averaged 6.55 keV is a different quantity. |
| Peak electron density held at 5.06e20 m^-3 | Lyon p708 gives central electron density 3.84e20 m^-3 and volume average 4.01e20 m^-3; p702 Figure 12 has an off-axis maximum. Neither tabulated number is a peak. Holding the package value is consistent with this request's decision not to reconstruct a peak from p701 Equation 3. This does not prove that a future source investigation could never establish a peak. |
| Exterior allocation 0.3 m and clear cavity 0.4 m held | The original source findings and independently reviewed coil evidence distinguish Raffray p744 Figure 23 winding-pack and integrated supporting-tube dimensions from a single-coil exterior envelope and a clear cavity including clearance. The retained decisions support holding these quantities; I did not newly inspect the coil images or transfer any coil dimensions. |
| Installed turns 308 and per-turn current 50000 A held | Ku's three family aggregate currents, as retained in the original source records and independent review, do not identify installed reference-coil turns and separate per-turn current. Their product remains calculated. No division or inversion from a desired magnetic field is justified. |

The retained source findings explicitly preserve the 18-versus-24-coil discrepancy, rounded aspect-ratio differences, and subsystem design revisions produced at different times. These unresolved facts do not alter the three accepted scalars. They prevent treating this request as a reconstruction of one fully specified ARIES plant. Coil evidence in this review is inherited from the retained original records; the four plasma/overview page readings above were independently repeated.

## Conditions carried into reporting

[INHERITED: adopted mapping and execution prompt] All 701 held inputs remain supplied package assumptions, including conductor technology and temperature, profiles, coil family geometry, equipment capacities, inventory, prices, availability and finance. The five held comparison controls are included in that inventory. A supplied or held alias earns no prediction credit. Completion of arithmetic cannot establish reference design feasibility or independent prediction of installed reference costs.

[INHERITED: domain-readiness answer and adopted execution prompt] The subsequent scientific review must retain fixed breeding geometry, conductor temperature/field support, equipment point ratings without qualified off-design maps, coupled cycle endpoint restrictions, incomplete plasma and cost correlations, hypothetical equipment offers, mixed money years, structural qualification, and bounded file-read verification. This input review certifies neither those domains nor future numerical outputs.

[AGENT] No request correction is proposed. Preserve the exact request bytes and historical preparation fields stating execution was then unauthorized. Record the new owner authorization separately. Numerical refusal or disagreement is an outcome to retain, not a reason to change this reviewed request.
