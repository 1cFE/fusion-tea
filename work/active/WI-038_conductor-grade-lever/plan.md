---
Status: active
Created: 2026-09-13
Updated: 2026-09-13
Related Artifacts: spec.md, design.md, basis.md
---

# WI-038 implementation plan

- [x] Reuse the existing work item; inspect audited WI-040, registered conductor evidence and original page-5 image; document relative-law derivation, reference economics and extrapolation in `basis.md`.
- [x] Complete fresh design-critique recheck before production edits. Review PASS after R1/R2 corrections: fixed reference density and removal of the unsupported 15 T lower-bound claim. ABI unchanged. SV-101 registered pending. Separate WI-040 late-consumer audit recheck precedes production.
- [x] Capture the entering 174-channel/18-verdict baseline. Implement the library calculation, typed seed, physical attributes and bindings in the conductor analysis, magnet structure/cost definition and stellarator instance. Only live sizing and procurement consume effective values; both legacy price paths remain unchanged. All 41 new component/public tests pass.
- [x] Synchronize MFE twins and family ownership; regenerate using all fifteen prior normative seeds plus one new seed. Current oracle/mappings and snapshot/census/manifest/derived fixtures are coherent. Exact fresh generation and baseline reconciliation pass: 174 old channels and eighteen verdicts unchanged; three outputs added; all 161 oracle channels agree. Seven cumulative model-source guards are retained, including WI-040 predecessors.
- [x] Verify named-wrapper domains, reference neutrality and public transfer identities; run affected model/current-consumer regressions and applicable validation levels. Models 889 passed/13 inherited skips; broad consumers 890 passed/one inherited skip/six stale fingerprint failures, followed by 22 passing targeted known-answer checks. Source endpoint/locator repairs changed only documentation; syntax/token proof and fresh baseline reconciliation retain numerical evidence. No added/removed L2/L6 diagnostic identity.
- [x] Obtain positive independent native audit, repair findings, and return evidence to goal T-004. Independent PASS at `48417c9e`; see `audit.md`. Goal integration/study and owner-held close/archive are separate.

## Evidence mapping

| Outcome | Check and expected observation | Basis | Evidence/status |
|---|---|---|---|
| MR-WI038-1/5 | Original source image and reference basis; approximate exponent .6 at 20 K with fit interval unreported in the inspected paragraph; anchor 24.9 T beyond the approximately 24 T visible measurement endpoint; 20–30 T only a sensitivity window | `basis.md`, source Fig. 1a and PDF p. 5 | source inspection and fresh design recheck pass; implementation audit corrected endpoint wording |
| MR-WI038-2 | At fixed current and geometry, pack volume, each material mass/cost, residual tape volume and tape cost scale by q; side scales √q, stress/strain by inverse √q; winding operations unchanged | inverse critical-current law, mass identity, existing stress equation | public perturbations pass in 41-test XML |
| MR-WI038-3 | Change envelope without actual field and actual field without envelope; peak-field verdict compares distinct quantities | purchased capacity versus operating demand | crossed current/envelope public cases pass |
| MR-WI038-4 | Exact equality of all entering channels and verdicts at q = 1; ungraded comparisons unchanged when only envelope varies | normalized relation and explicit consumer bindings | baseline-reconciliation.json: 174 exact channels/eighteen verdicts; legacy invariance checks pass |
| MR-WI038-6 | Resolving source comments, physical ownership, byte-identical twins, preserved seeds, fresh package and oracle agreement | MR-3/4, AD-007/008, WI-040 wrapper lesson | exact 261-file fresh generation; seven cumulative source guards; 161 oracle comparisons; independent audit PASS |
| MR-WI038-7 | Nonpositive/non-finite fields, exponent or density; negative/non-finite price; overflow and underflow refuse deliberately; zero price valid | declared arithmetic contract | component/wrapper domain tests pass |
| MR-WI038-2/5 | Priced-transfer test/study protocol holds reference j_wp at 118.8271604938272 A/mm², economic reference field, composition and coil-set shape/distribution factors fixed; an independent density perturbation is not labeled a priced same-technology transfer | `review.md` R1 and corrected `basis.md` | public tests hold these references; later goal study must retain this condition |

## Work ownership

Preparation author owns this item's four documents. Coordinator owns global PM/verification registration, baseline, current generation recipe/metadata, integration and goal records. Production model, oracle and test ownership will be assigned after critique with the fixed ABI. Authors preserve other workers' edits and do not regenerate the shared package concurrently.
