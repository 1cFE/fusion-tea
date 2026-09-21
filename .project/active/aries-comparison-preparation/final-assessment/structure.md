# Structural comparison with ARIES-CS

[INHERITED] The acceptance criterion is [B-2](../../../completed/20260821_demo-anchor-acceptance-spec/spec.md): all three correspondences must be present, and an absent first-order subsystem fails the structural axis. [AGENT] Verdict: **structural similarity does not pass**. The model represents every broad category named in B-2, but it omits ARIES's separate PbLi heat-removal circuit. Its radial sequence corresponds at the requested level. Its cost-account families are broadly present, but several published account boundaries remain unresolved. This is a comparison of the supplied Stellaris-derived design under three transferred reference inputs, not a reconstruction of ARIES equipment.

## Identity and evidence

[AGENT] All 52 model files in the adopted `post-reveal-v1` archive match the live files byte-for-byte. The archive SHA256 is `d65d6ea44517dba3d9012d06706e74fe3006247e2809f6b4bdd64edd85ab5a7a`; executable fingerprint is `83ea3b6cf99f5fda6045e7e03b5d430ede91abbe8aa41262c2f9f5aba8663d23`. [Identity receipt](evidence/structure-identities.json) records each file hash and the four directly inspected source images. Accordingly, the live source locations below describe the frozen structure used by the retained partial assessment. No plant evaluation, input change or model change was made for this assessment.

[AGENT] Source abbreviations below link to retained images, inspected directly: [N663: Najmabadi p663 Table II](../post-reveal-results/post-reveal-v1/source-evidence/retained/knowledge/holdout/aries-cs/extracted/20260920-r3/08-FST-Najmabadi/outputs-page-08.png); [L699: Lyon p699 Figure 5](../post-reveal-results/post-reveal-v1/source-evidence/retained/knowledge/holdout/aries-cs/extracted/20260920-r3/08-FST-Lyon/outputs-page-05.png); [R734: Raffray p734 Table II and §V.E](../post-reveal-results/post-reveal-v1/source-evidence/retained/knowledge/holdout/aries-cs/extracted/20260920-r3/08-FST-Raffray/outputs-page-09.png); [R736: Raffray p736 Figures 12–13](../post-reveal-results/post-reveal-v1/source-evidence/retained/knowledge/holdout/aries-cs/extracted/20260920-r3/08-FST-Raffray/outputs-page-11.png). Engineering-paper parameters were not all synchronized to the final systems point; the [retained source review](../post-reveal-investigation/source-review/source-review.md) records that caution. The figures establish architecture without combining their numbers into a new plant.

## Subsystem correspondence

[AGENT] “Matched” below means a recognizable functional subsystem exists. It does not establish equal technology, geometry, performance or scope of component costing. The frozen instance is [stellarator_plant.sysml](../../../../models/designs/stellarator_09/stellarator_plant.sysml); its inherited composition is [generic_mfe/mfe_plant.sysml](../../../../models/designs/generic_mfe/mfe_plant.sysml).

| ARIES subsystem and source | Frozen model location | Verdict and consequence |
|---|---|---|
| Plasma and magnetic confinement; N663 discussion | Instance `plasma`, line 886; `magnet`, line 115 | **Matched** functional categories. The held density, temperature, turns/current and selected conductor do not reconstruct the reference plasma/coils. |
| Modular magnet system and supports; N663 22.1.3, L699 | Instance `magnet.coil`, line 201; `winding_pack`, line 320; `casing`, line 496 | **Matched** magnet function. A selected modular-coil/pack/casing representation is not the published three coil families and separate strongback/intershell construction. Those subcomponent equivalences remain unresolved. |
| First wall, blanket, shield and primary support; N663 22.1.1/.2/.5, L699 | Instance `blanket`, line 560; `first_wall`, 601; `shield`, 661; `structure`, 682 | **Matched** broad components. Uniform shell geometry does not represent ARIES's separate full and tapered sectors, back walls and local shields. |
| Vacuum containment/pumping; N663 22.1.6, L699 | Instance `vessel`, line 702; `vacuum_pumping`, 1615 | **Matched** functions. Vessel capital alone cannot be assumed to equal the reference vacuum-system account. |
| Heating, electrical supplies and divertor; N663 22.1.4/.7/.8 | Instance `heating`, line 1026; `power_supplies`, 721; `divertor`, 1121 | **Matched** broad functions. No equation or supplied purchase becomes an independently reconstructed ARIES design. |
| Blanket PbLi loop, blanket He loop and divertor He loop; R734/R736 | Instance `heat_transport`, line 1147; library `mfe_plant_systems.sysml`, primary-loop calculation at 323 | **Mismatch.** The model has a primary helium circuit and HITEC intermediate equipment; it does not have the reference's separate PbLi heat-removal circuit or its separate hot-side exchanger branch. The reference explicitly assigns 1,444 MW of heat removal to PbLi in this engineering case. This is a first-order omission, not a minor pipe-detail difference. |
| Recuperated helium Brayton conversion with three compressor stages; R736 | Instance `turbine`, line 743; steam generator, reheater, HP/LP steam turbines, condenser and pumps at 756–794 | **Matched** power-conversion function; **mismatch** in equipment topology. The selected model is a steam Rankine system. This difference alone need not fail a broad subsystem checklist, but it prevents component-level equivalence. |
| Electrical plant, miscellaneous BOP, heat rejection, buildings; N663 21/24/25/26 | Instance lines 838, 874, 848 and 1623 respectively | **Matched** broad functions. Published account numbers require the crosswalk below. |

[AGENT] B-2 subsystem verdict: **mismatch/fail** because the separate PbLi heat-removal branch is absent. This applies the criterion's first-order-omission clause; it does not require identical equipment in every subsystem. The source's large heat duty and separate exchanger branch are the reasons for treating this omission as first-order.

## Radial-build ordering

[AGENT] B-2 radial verdict: **matched/pass at the stated qualitative level**. L699 visibly orders plasma → SOL → first wall → full or tapered blanket → shields → vessel → magnet. The model's [cumulative-radius equations](../../../../models/library/analyses/mfe_plasma_scaling.sysml), lines 102–113, order plasma minor radius → vacuum stand-off → first wall → blanket → reflector → high-temperature shield → structure → assembly gap → vessel → coil. The model's vacuum stand-off is the functional counterpart of the source's SOL clearance for this geometric checklist; it is not an SOL transport prediction.

[AGENT] The coil-bore output is the vessel outer radius (same file, line 138). The intervening reflector/support/gap layers do not reverse the required order. ARIES adds separate manifolds and locally varying steel/tungsten-carbide shield sections; the model adds an outer low-temperature shield. Neither difference establishes a reversal of the checklist's sequence. This pass does not certify the thicknesses, three-dimensional clearances or tapered blanket coverage, and it does not remove the retained winding-pack fit violation.

## Cost-account coverage and crosswalk

[AGENT] The model implements CAS10 preconstruction, CAS21 buildings, CAS22 core/tail accounts, CAS23–26 BOP, CAS27 materials, CAS28 digital twin, CAS29 contingency, CAS30 indirect, CAS40 owner, CAS50 supplementary, CAS60 financing and CAS70/80 annual costs. Their executed composition is in [generic_mfe/mfe_plant.sysml](../../../../models/designs/generic_mfe/mfe_plant.sysml), lines 435–834. CAS60 is a reported financing line under the model's chosen cash-flow convention; presence does not authorize adding it again to overnight cost.

| N663 reference account | Model semantic correspondence | Verdict |
|---|---|---|
| 20 land and land rights | Land term within CAS10 preconstruction | **Unresolved scope.** Reference account 20 is not model `cas20_capital`, which is a direct-capital aggregate including contingency. Model CAS10 also has fixed adders. |
| 21 structures/site facilities | `buildings.capital_cost` | **Matched family**; facility-detail equivalence unestablished. |
| 22.1.1 first wall/blanket/reflector; .2 shield; .3 magnets; .4 heating; .5 structure | Corresponding `blanket`, `shield`, `magnet`, `heating`, `structure` capital accounts | **Matched families**; reference back-wall/manifold/cryostat/support allocation is not proven equal to these model boundaries. |
| 22.1.6 reactor vacuum systems, unless integral elsewhere | `vessel` and `vacuum_pumping` functions | **Unresolved cost scope.** The core-capital sum at lines 462–467 includes vessel capital; a separate pumping function does not demonstrate a separately complete vacuum-equipment cost. |
| 22.1.7 power supply/switching/storage | `power_supplies.capital_cost` | **Matched family**, with the existing C220107 supplied-cost disclosure retained. |
| 22.1.8 impurity control | `divertor.capital_cost` | **Matched function**, narrower model label; complete scope unresolved. |
| 22.1.9 direct conversion and 22.1.10 ECRH breakdown, both reported zero | No separate equivalent selected accounts | **Not a demonstrated first-order omission** at this reference point. Model C220110 instead denotes remote handling; matching these by numeric suffix would be wrong. |
| 22.1 reactor equipment; 22 total reactor plant | Core and tail sums, lines 462–582 | **Unresolved aggregation.** The model separately adds remote handling and installation; no source allocation proves equality to the printed subtotals. |
| 22.2 main heat transfer/transport | `heat_transport.coolant_cost` | **Matched account function; mismatched plant scope** because the dual-coolant topology differs. |
| 23 turbine plant; 24 electric plant | `turbine`, `electric_plant` | **Matched families**, different cycle equipment. |
| 25 miscellaneous; 26 heat rejection | Model `misc_plant` CAS26; `heat_rejection` CAS25 | **Matched by title, mismatched numbering.** See [cas_hierarchy.sysml](../../../../models/library/cost_structure/cas_hierarchy.sysml), lines 87–109. |
| 27 special materials | `special_materials_capital` | **Matched family**, inventory boundary needs independent reconciliation. |
| 90 direct cost excluding contingency | Model pre-contingency direct aggregate plus the appropriate land term and scope adjustments | **Unresolved scope.** It is not model CAS90 annualized capital or the library's separately named CAS90 indirect-cost class. |
| CAS40/50/60/70/80 | Present model owner/supplementary/financing/O&M/fuel machinery | **Model coverage present; reference account breakdown unavailable in N663.** Missing source entries are not zero. |

[AGENT] B-2 cost-coverage verdict: **unresolved; no pass**. The model has the required broad account machinery. A title-based crosswalk recovers several clear correspondences, including the reversed 25/26 numbering. Complete account-to-account equivalence cannot be claimed while vacuum, cryostat/manifold allocation and aggregate scope remain unresolved. This is more specific than declaring the entire structural axis unknown, and it does not force the reference's physical-component table into a fictitious one-to-one CAS map.

[AGENT] The overall structural verdict remains fail from the established heat-transport omission, independently of unresolved costing. No cost ratio or engineering-feasibility conclusion is inferred from these structural verdicts.
