# Learnings: magnet-design-transfer

Append-only, newest last. Entries are added only after a fresh round review accepts or corrects a proposed learning delta. No accepted learnings yet.

## L-001 — Material composition needs the verified image — 2026-09-13

[AGENT] Table 7's inspected image gives tape stack 9%, copper jacket 35%, solder 12%, steel 36% and helium 8%. The inherited WI-036/backlog mixture and current material-parts documentation disagree with it. Those inherited values cannot establish a material-cost basis. The image supports the corrected composition; it does not approve replacing the item's insulation scope or establish a quantified insulation inventory. Evidence: `work/active/WI-040_winding-pack-mass-cost/basis.md@817f21ff`; the cited local image is unpinned, no native digest. Accepted by fresh Round 1 review, `evidence/R1-review.md`.

## L-002 — A missing mass term does not prove missing procurement — 2026-09-13

[AGENT] The existing winding account's ampere-metre formula contains no material-mass input, but its fabrication multiplier names insulation and cooling among its contents. Clean native evidence does not resolve whether procurement is included. Adding explicit material costs requires an accounting basis for that split; absence of a mass term alone cannot justify the addition. Evidence: `models/library/analyses/mfe_magnet_cost.sysml@4ca1f299`; `work/completed/20260901_WI-035_magnet-closure/design.md@384e380e`, D4 and Risk 4. Accepted by fresh Round 1 review, `evidence/R1-review.md`.
