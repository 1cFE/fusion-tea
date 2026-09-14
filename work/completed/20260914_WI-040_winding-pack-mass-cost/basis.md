# WI-040 source and accounting basis

## Material-table conflict

[AGENT, verified 2026-09-13] The source image `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png` reads tape stack 9%, copper jacket 35%, solder 12%, steel 36%, helium (cooling) 8%. These sum to 100%. This image is local untracked evidence; unpinned, no native digest identified for this inspection. The tracked prior WI-035 design records the same image reading at `work/completed/20260901_WI-035_magnet-closure/design.md`, Source verification.

The adjacent text table in `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md:1874` instead reports conductor 15%, copper 10%, insulation 45%, steel 26%, helium 4%. WI-036 design D8's 85% non-conductor claim and the current `models/library/structure/mfe_magnet_parts.sysml` winding-pack documentation repeat that incorrect basis. The source prose describes a non-insulated winding with insulation between pancakes; that does not establish a 45% insulation volume.

[AGENT, adopted 2026-09-13 under the owner's autonomous-judgment delegation] Price the four non-tape materials in the source image and disclose the absence of a quantified insulation inventory. This does not claim tape procurement has zero mass; its existing cost basis is ampere-metres and remains separately accounted.

## Existing accounting

`models/library/analyses/mfe_magnet_cost.sysml` 'Winding Pack Cost' prices coil-set ampere-metres at `cost_per_kAm`, then multiplies by `f_wp_fab`. WI-035 design D4 identifies that multiplier as 3.5 times 1.9; the source comment for 3.5 names winding, insulation, cooling, jointing and test. The current 'Magnet Structure Cost' separately prices coil casing mass, and 'Magnet Capital' sums winding and casing accounts.

[AGENT] This creates an unresolved accounting question: explicit material costs cannot be assumed absent merely because the algebra has no material-mass term. The source's fabrication content must be checked before an additive account is selected. Read-only delegated investigation brief: `work/orchestration/goals/magnet-design-transfer/evidence/T-001_accounting-reader-prompt.md@ff3030b5`.

The reader returned no documented procurement/fabrication split and reported a quarantine exposure during a later upstream-document screen. The incident is recorded in `knowledge/holdout/aries-cs/PROTOCOL.md` §6 without the datum. The reader made no changes and is retired from model-facing decisions. Its proposed accounting alternatives are not adopted as design authority. The coordinator's directly inspected clean evidence above is sufficient to keep the split unresolved.

## Current structural boundary

The current library separates 'Modular Coil', 'Winding Pack' and 'Coil Casing' in `models/library/structure/mfe_magnet_parts.sysml`; 'Magnet System' owns the analytical assembly in `models/library/cost_structure/mfe_power_core.sysml`. AD-008 governs additions. The cryoplant receives total cold volume, which includes a separate additional-cold-volume input. Material accounting must use the computed winding volume, not that total.
