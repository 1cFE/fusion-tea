# Independent T02 constituent source review

[AGENT] 2026-09-21. Initial focused source review of retained primary Lyon Table VIII, printed p718 (`source-Lyon-page-25.png`), adjacent p717 (`source-Lyon-page-24.png`), p697 geometry discussion and independently rendered p699 (`review-lyon-p699.png` beside this record). Author scope/design was not yet available; implementation acceptance is not issued.

## Source distinctions and permitted arithmetic

[INHERITED: Lyon pp717–718] Table VIII is explicitly the LiPb/SiC blanket/shield alternative. It is not the LiPb/ferritic-steel/helium reference. Adjacent prose explains that Table VIII unit costs in 2004 dollars apply to complex machined shapes. Calling those numbers raw commodity prices would lose their source meaning. They do not alone establish total installed system costs or a mapping to a parent cost account.

[INHERITED: Table VIII] Composition fractions are volume fractions; radial depths are centimetres; densities are kg/m^3; prices are 2004 dollars/kg; coverage is area percent. The first-wall/full-blanket recipe is 25 cm, 65.4% coverage, 21% SiC/SiC structure with density 3200 and rate 510, plus 79% LiPb enriched 70% with density 8897 and rate 17.1. The 70% enrichment is a separate material descriptor, not another volume factor.

[AGENT] Under an explicitly planar extrusion approximation, per square metre of this covered region the volume is 0.25 m^3, SiC mass is 168 kg, and LiPb mass is 1757.1575 kg. The source-rate subtotal is 115727.39325 dollars of 2004 per covered m^2. If the supplied area instead means the whole reference surface, multiply by coverage 0.654 exactly once. A real 3D volume reconstruction additionally needs geometric offsets/Jacobians; surface times depth is not established as exact by the table.

[AGENT] Coverage fractions overlap across radial layers. The lateral split 65.4% + 10.6% + 24% is 100%, but the second blanket repeats the first region and blanket-behind-divertor repeats the divertor region. Summing all row coverage as one partition would double-count area. Tapered depth ranges require an explicitly supplied spatial distribution or selected effective depth; a midpoint is an assumption, not a measured average.

[INHERITED: Table VIII] Water and liquid-helium constituent rows have blank density/rate cells. Those blanks do not establish zero mass or zero cost. Shared-looking composition cells across shield/coil rows require careful row-group interpretation before a wider recipe inventory is implemented. Footnote `a` identifies replaced components; it does not specify replacement timing or a lifecycle multiplier.

## Reference geometry evidence

[INHERITED: Lyon p699 Fig. 5] The reference LiPb/FS geometry instead labels full blanket/shield and divertor as 61% + 15% = 76% of first-wall area, with a 24% tapered region. Its nominal full blanket depth is 54 cm plus separately drawn 4-cm first wall; tapered blanket, ferritic shield, WC shield, manifolds and back wall are distinct. These reference labels must not be combined with the alternative Table VIII's 65.4%/10.6% and SiC recipe without explicitly selecting a mixed synthetic scenario.

[AGENT] A bounded constituent-volume/mass/source-rate calculator can be implemented with supplied area or volume, clearly defined coverage, composition, densities and rates. It would demonstrate accounting and inventory arithmetic under those inputs, not neutronics, qualified material selection, actual reference installed cost or LCOE. The proposal must state whether it targets a labeled alternative-table unit recipe or a source-supported reference recipe. Source/design review remains pending that choice.

## WI-084 reference recipe and design disposition

[AGENT] Accepted for implementation against `work/active/WI-084_aries-sector-constituent-inventory/spec.md`. Independently inspected Table II p706 (author's durable `evidence/lyon-p706.png`) and costing/geometry discussion p705 (`review-lyon-p705.png` beside this review). Table II supports the actual reference's full, behind-divertor and tapered blanket recipes, including their 65.4%/10.6%/24% coverage, 54.3/35/25–54.3-cm thicknesses, volume fractions and all three specified density/rate pairs. The missing helium density/rate remains explicitly unquantified.

[AGENT] Table II's SiC inserts cost 101 USD2004/kg; Table VIII's SiC/SiC structure costs 510. The new reference contract correctly keeps them distinct and defers the alternative. The source supports average thickness times midpoint area, with that area scaled from the last closed flux surface; the chosen 1-m^2 full-coverage midpoint bases are therefore explicit normalized scenario inputs, not recovered plant geometry. Taper endpoints remain selected sensitivities. The coverage conflict with Fig. 5 is retained without mixing inputs; chronology between figure and table has not been established, so describing one as older is unsupported.

[AGENT] The four-definition design has appropriate ownership: region volume, constituent inventory, recipe summary and region aggregation. Child output bindings provide an auditable path to partial assembly totals. Finite/domain guards, fraction closure even at zero volume, independent arithmetic and public area/thickness/price perturbations are suitable acceptance checks. Supplied dimensions and prices remain choices under MR-7. No equipment selection or physical adequacy is implied.

[AGENT] Price/account limit: p705 explicitly allocates enriched LiPb to account 26 special materials. Summing LiPb and structural constituent rates is permissible as a named source-rate subtotal; that combined subtotal must not silently become the blanket's installed account or be added again as special materials. Source-rate mass pricing is not a whole-component account reconciliation. No implementation acceptance is issued yet; actual typed guards, assembly edges and aggregate outputs remain to be verified.
