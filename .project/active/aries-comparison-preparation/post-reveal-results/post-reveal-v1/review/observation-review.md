# Independent source and observation review

[AGENT] **PASS for reporting the retained failed attempt with these observations**, 2026-09-20, reviewer `/root/source_review`. No observation or source-transcription correction is required. The reviewer authored neither the observations nor source decisions, and performed no physical evaluation. This is approval of an accurate failure comparison record, not scientific adequacy or plant feasibility.

## Exact reviewed artifacts

| Artifact relative to this result register | SHA256 |
|---|---|
| observations.json | `e4305c2dafef62f5e0d0151dd11eb3c82b3d530ba50fe108632b5c9fd30a958e` |
| source-decisions.md | `894c0282a926fa49494006d18202f7d32c89fb6d1225bef5eff9751aae2cb105` |
| source-evidence/index.json | `e730ef77bb48c54404b88f276714131f1ff69d7d8b92306c309f2c9a731b960a` |
| source-evidence/observation-map.json | `c1ecb3aee402048edb66064e74f21189a5b8312af2f4c18458656cfd587515b2` |
| attempts/first-forward/result.json | `8a0e2385b3305ef746d78f9feac262c24b62e46010ca9ed71b81d9eeb98751de` |
| attempts/first-forward/model-export.json | `3b874cf6963b1a50a12641195939fb23b6b7d6eaecd9bf5173b2af9f63881500` |

## Native evidence and coverage

The retained native state is `execution_failed`. Its nonretryable module failure is `stellarator_09__stellaris__magnet__conductor_current`: `ValueError: REBCO Conductor Current: B_peak outside 20..32 T; actual=56.61785714285713 T at 20.0 K`. Native outputs and verdicts are empty; the failure record lists no partial artifacts. The field printed in the exception is a diagnostic operand, not an exported numerical prediction.

I checked all 276 observation IDs against the native export and untouched observation template. Every model-side field is unchanged, every model value remains null, and every model-valid flag is false. All native export rows say `execution_not_completed` and carry no independent prediction credit. Observation execution state is `failed`; its constraints remain the native empty map. I counted 67 expected predicates in the archived generated model contract. They are all unevaluated, rather than 67 passes or violations. No downstream power, cost or LCOE value is available.

The historical `conditioned` observation-schema label is consistent with the adopted reporting route. It does not name a second scenario. The report route overlays current supplied/held roles, binds model observations to retained native availability, replaces the historical constraint list with all 67 current predicate identities, and retains the post-reveal designation.

## Source evidence and definitions

I verified all 25 retained source-evidence files against their recorded SHA256 and original Git objects at `829539f5eb7fde217d18318d1646a5e47103812c`. I directly inspected the retained output images of Lyon pp699, 707, 708 and 709; Najmabadi p663; and Raffray pp734, 736 and 737. The input review separately inspected Lyon pp701, 702 and 708 and Najmabadi p657. No new PDF extraction was needed.

The worksheet retains 52 contextual numerical candidates: the original 50 plus the two admitted radius scalars. I checked every unit scaling recorded in observation-map.json against the resulting reference value and unit; all match, and none introduces currency-year adjustment. Three structural rows retain qualitative evidence. The remaining numerical rows preserve unavailable reference data. A contextual value is not an admitted matched prediction when the model result is unavailable.

The checked source distinctions are retained correctly:

- Lyon p707 Table III supplies whole-account costs in 2004 million dollars. Lyon p709 Table VI has narrower component scopes. Shield includes back wall and manifolds; vacuum includes cryostat. Coil-plus-structure whole accounts include scope beyond modular-only figures. The source account-name mapping preserves the discrepancy in account numbers between Lyon and Najmabadi. Parent and child amounts are not independent amounts to add together.
- C220107 remains power-supply account context subject to the unchanged aggregate exclusions and disclosures. The inherited C220103 scope-label typo remains disclosed; neither issue earns independent credit or establishes scope equivalence.
- Lyon p708 gives 2436 MW fusion, 2916 MW thermal, 1253 MW gross and 1000 MW net electricity, with 253 MW recirculation. The rounded component-load and radiation discrepancies remain visible. Raffray p734's 156 MW blanket pumping, 141 MW friction heat, 1192 MW helium heat removal, 3261 kg/s flow and 0.30 MPa pressure drop use a different engineering analysis and physical boundary.
- Raffray pp736–737 shows a Brayton compressor turbine and generator turbine. Its 0.43 gross efficiency does not establish the held model's steam-cycle correspondence. Lyon p709 Nb3Sn costs and support masses do not establish correspondence to the held REBCO product, casing, turns or per-turn current.
- Najmabadi p663 states 7.76 cents/kWh in 2004 dollars and assumed availability 85%. Conversion to 77.60 dollars/MWh and 0.85 preserves those meanings. The two LCOE rows reuse this same supporting source value; they are not separate independent benchmarks or feasible plant prices.
- Lyon p699's full and tapered blanket sectors and local shielding support only a qualified structural reading. A general subsystem counterpart is plausible; exact radial arrangement, geometry and accounting coverage remain unresolved. Source breeding performance does not qualify the held model's fixed breeding geometry.

## Disposition

[AGENT] The observations are suitable for the adopted report command. All numerical comparisons must remain blocked by unavailable model predictions. Preserve the conductor-domain refusal as the adverse outcome and all 67 predicates as unevaluated. The source worksheet adds useful reference context without replacing native evidence or treating held offers as predictions. Further physical execution requires another owner decision; report replay does not.

## Final report acceptance

[AGENT] **PASS** for the emitted machine report and the reviewed scientific narrative in report.md. Machine report SHA256: `0e0efc96b9343c8139cd42645a9c612197aa198d6e4ffb3dfb81f7d32deaf551`. Its receipt matches retained report bytes. All 276 rows are blocked, every ratio is null, every independent-credit flag is false, accounting checks are blocked, native predicates are empty, and constraints are incomplete. The narrative accurately reports the conductor-domain refusal, unavailable LCOE, held inputs, source limits and absence of a physical impossibility finding. The machine `physical_feasibility: false` denotes failure to establish feasibility in this failed execution; it is not a proof of physical impossibility.

[AGENT] Two editorial finalization points were sent to the coordinator: label the retained first-forward link as this post-reveal attempt rather than the original attempt, and replace the pending report/review-link sentence with final links after replay. Neither changes scientific content or the accepted observation bytes. Replay verification is independently owned and is not claimed by this review.
