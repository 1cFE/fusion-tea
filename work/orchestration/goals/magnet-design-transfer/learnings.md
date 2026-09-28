# Learnings: magnet-design-transfer

Append-only, newest last. Entries are added only after a fresh round review accepts or corrects a proposed learning delta. No accepted learnings yet.

## L-001 — Material composition needs the verified image — 2026-09-13

[AGENT] Table 7's inspected image gives tape stack 9%, copper jacket 35%, solder 12%, steel 36% and helium 8%. The inherited WI-036/backlog mixture and current material-parts documentation disagree with it. Those inherited values cannot establish a material-cost basis. The image supports the corrected composition; it does not approve replacing the item's insulation scope or establish a quantified insulation inventory. Evidence: `work/active/WI-040_winding-pack-mass-cost/basis.md@817f21ff`; the cited local image is unpinned, no native digest. Accepted by fresh Round 1 review, `evidence/R1-review.md`.

## L-002 — A missing mass term does not prove missing procurement — 2026-09-13

[AGENT] The existing winding account's ampere-metre formula contains no material-mass input, but its fabrication multiplier names insulation and cooling among its contents. Clean native evidence does not resolve whether procurement is included. Adding explicit material costs requires an accounting basis for that split; absence of a mass term alone cannot justify the addition. Evidence: `models/library/analyses/mfe_magnet_cost.sysml@4ca1f299`; `work/completed/20260901_WI-035_magnet-closure/design.md@384e380e`, D4 and Risk 4. Accepted by fresh Round 1 review, `evidence/R1-review.md`.

## L-003 — Explicit replacement accounting does not establish savings — 2026-09-13

[AGENT] WI-040's replacement winding account makes material inventory, tape procurement and winding operations separately checkable. It does not establish the procurement content of the old unsplit multiplier or demonstrate savings. Unquantified manufacturing terms and ambiguous inherited unit-price content remain limits. This extends L-002 without resolving its historical uncertainty. Evidence: `work/active/WI-040_winding-pack-mass-cost/design.md@173ac157`; `work/analysis/20260914-045431_audit_WI-040.md@0d077258`; reference reconciliation in `exploration/stellarator_e2e/studies/20260913-magnet-design-transfer/synthesis.md@1792edf6`. Accepted by fresh Round 2 review, `evidence/R2-review.md`.

## L-004 — This priced transfer requires the fixed reference inventory basis — 2026-09-13

[AGENT] In the implemented estimate, holding reference density, construction, composition and unit economics fixed lets the selected-envelope quantity multiplier increase tape volume and tape procurement proportionally as geometry/current change. Actual field demand remains separate from selected capacity. Independently reducing reference density increases tape volume without a corresponding tape-price increase, so such changes require a newly justified price/inventory basis before they represent a priced same-technology transfer. This is an applicability condition of the implemented model. Evidence: `work/active/WI-038_conductor-grade-lever/basis.md@48417c9e`; independent density counterexample in `work/analysis/20260914-054500_audit_WI-038.md@aa3e1f3d`; frozen study `@fa195fa4`. Accepted with clarified scope by fresh Round 2 review, `evidence/R2-review.md`.

## L-005 — Engineered-window consistency does not qualify a design range — 2026-09-13

[AGENT] The study's numerical agreement supports conditional transfer relationships at the sampled points. It does not establish a source-qualified geometry or conductor interval. All five fully passing points rely on extrapolated selected envelopes, while configuration-specific geometry, absolute conductor margin, pack/casing fit and manufacturing coverage remain unverified. Denser sampling of these unchanged equations cannot supply that evidence. Evidence: `exploration/stellarator_e2e/studies/20260913-magnet-design-transfer/record.md@fa195fa4`; `transfer-claim.md@1792edf6`; the prior missing-configuration-input account in `work/completed/20260908_WI-044_magnet-chain-sees-coil-bore/spec.md@0b5de534`. Accepted by fresh Round 2 review, `evidence/R2-review.md`.
