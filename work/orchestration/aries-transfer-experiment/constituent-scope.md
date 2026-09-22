# T02: source constituent and sector inventory proposal

[INHERITED: coordinator assignment, 2026-09-21] Build a meaningful source-supported constituent/sector inventory through the native model route. Preserve independently supplied geometry and distinguish the FS/He reference from the SiC alternative. [AGENT] The evidence supports both reference and alternative recipes. The next increment need not stop at the alternative, but it must stop short of a whole-plant volume claim.

## Recommended build

[AGENT] Model the reference's three blanket regions: full blanket, blanket behind the divertor, and tapered blanket. Give each region an independently supplied midpoint-area basis and thickness. Calculate represented volume, constituent volume, non-helium mass and source-year constituent price sum. Show the helium volume separately as an unquantified mass/cost contribution. Add a distinct SiC-alternative full-blanket recipe case for controlled comparison per equal supplied volume; do not combine the recipes into one plant.

[AGENT] Two small concept-neutral calculations are needed: a covered layer volume identity, and a constituent mass/price identity. The assembly owns region and material occurrences. Aggregate from their actual calculated outputs. No temperature, power or fit result silently selects thickness, area or composition. This is a new constituent model using familiar physical identities, not reuse of an existing cost proxy under renamed materials.

## Source evidence checked

[AGENT] Directly inspected Table VIII, printed p718, retained image `.project/active/aries-comparison-preparation/alternative-point-screen/evidence/source-Lyon-page-25.png`; Table II, printed p706, rendered from zero-index PDF page 12 to `/tmp/aries-constituent-p706.png`; and Fig5 p699 in the retained `outputs-page-05.png`. The PDF is `.project/active/aries-comparison-preparation/post-reveal-results/post-reveal-v1/source-evidence/retained/knowledge/holdout/aries-cs/08-FST-Lyon.pdf`. The new item's evidence should retain the p706 render and PDF hash. Existing retained image numbering is not a reliable substitute for the PDF index: `outputs-page-13.png` is p707, not Table II p706.

| Component recipe | Thickness and coverage | Volume fractions | Densities kg/m3; unit prices USD2004/kg |
|---|---|---|---|
| FS/He reference full blanket, Table II | 0.543 m; 0.654 | LiPb 0.79; SiC inserts 0.07; ferritic steel 0.06; helium 0.08 | LiPb 8897, 17.1; inserts 3200, 101; steel 7800, 103; helium density and price blank |
| FS/He reference blanket behind divertor, Table II | 0.35 m; 0.106 | LiPb 0.75; inserts 0.09; steel 0.08; helium 0.08 | Same constituent values as reference full blanket |
| FS/He reference tapered blanket, Table II | 0.25–0.543 m; 0.24 | LiPb 0.76; inserts 0.08; steel 0.08; helium 0.08 | Same constituent values as reference full blanket |
| SiC alternative first wall/full blanket, Table VIII | 0.25 m; 0.654 | SiC/SiC structure 0.21; LiPb 0.79 | SiC/SiC 3200, 510; LiPb 8897, 17.1 |

[AGENT] The source distinguishes SiC inserts at 101 USD2004/kg from SiC/SiC structure at 510 USD2004/kg. Table II and VIII fractions are by volume. The source's p705 §VI says prices describe complex machined shapes in year 2004 dollars; therefore these are source component rates, not raw commodity prices or installed plant costs. Do not add a fabrication factor without a separate basis.

[AGENT] The three lateral blanket fractions sum to one. Other table rows overlap these regions in depth; summing every row's area fraction would double-count coverage. Reference first wall is a separate Table II component while the alternative row explicitly includes first wall. Consequently a full-blanket recipe comparison is not a complete equal-functional-scope blanket-system cost comparison. The initial assembly excludes first wall, divertor hardware, second blanket, back walls, shields, manifolds and supports from the reference-region sum; none is inferred zero.

[AGENT] Fig5 gives the qualitative full/tapered arrangement, but its caption's older 61%+15%=76% subdivision differs from Table II's 65.4%+10.6%=76%. Use the quantitative Table II recipe under a named Table-II case; do not silently merge the figure's split into it. The overall tapered fraction agrees at 24%.

## Geometry support and its limit

[AGENT] Lyon p705 §VI.A states that component volumes are average thickness times midpoint area, with midpoint area scaled from LCFS area by midpoint distance divided by average plasma radius. Existing `MFE Radial Build` (`models/library/analyses/mfe_plasma_scaling.sysml:52`) uses uniform torus shells and CAS aggregate boundaries. It cannot supply the source's nonuniform sector volumes unchanged. The published 728 m2 wall area is not automatically the required LCFS or layer-midpoint area.

[AGENT] Proposed first execution uses a named normalized geometry scenario: full-coverage midpoint-area bases of 1 m2 for each of the three reference regions, multiplied by the table coverage fractions. The tapered thickness is an independently chosen scalar tested at 0.25 m and 0.543 m. These are endpoint sensitivity cases, not claims that either endpoint is the actual regional mean. No unsupported arithmetic mean is silently introduced. Outputs are inventories of that explicitly supplied geometry, not totals for ARIES.

[AGENT] An additional equal-unit-volume pair evaluates 1 m3 of reference full-blanket recipe and 1 m3 of alternative full-blanket recipe. This separates material composition from geometric scope. Full reference reconstruction still needs authenticated LCFS area/average radius and layer-midpoint positions, source-consistent average taper thickness or its distribution, and clarification of stacked blanket/first-wall boundaries. The missing helium state/density and pricing must remain unquantified rather than entered as zero.

## Existing definition assessment

| Candidate | Decision |
|---|---|
| `Winding Pack Material Inventory`, `mfe_winding_pack_cost.sysml:4` | Do not reuse by relabeling. It owns copper/solder/steel/helium, ideal-gas helium and residual tape volume. It requires composition sum below one. Those semantics do not fit the source blanket recipes. |
| `Blanket Cost` and `Shield Cost`, `mfe_account_costs.sysml:72,102` | Do not reuse as constituent pricing. They multiply aggregate volume by a thermal-power scaling law; supplied material inventory would then change cost with demand. |
| `Magnet Structure Cost`, `mfe_magnet_cost.sysml:157` | Multiplication is familiar but the support/casing ownership and rate factors are specific. A generic constituent calculation is clearer than forcing SiC or PbLi through a steel-support formal. |
| `MFE Radial Build`, `mfe_plasma_scaling.sysml:52` | Useful later for explicitly approximate torus cases, but it does not reproduce the source midpoint-area/sector geometry. |
| `Costed Component`, `models/library/foundation/costed_component.sysml` | Its interface can be reused when a future bounded account rollup is defined; do not call a partly priced material sum installed capital merely to reuse the interface. |

## Proposed analysis contract and acceptance

[AGENT] A covered-layer calculation owns `volume = area_basis * coverage * thickness`, with supplied area in m2, coverage in [0,1], thickness in m and calculated volume in m3. A constituent calculation owns `constituent_volume = volume * fraction`, `mass = constituent_volume * density`, and `source_price_sum = mass * unit_price`, with supplied volume fraction, kg/m3 density and USD2004/kg rate. All numerical inputs must be finite; geometry, fractions and rates nonnegative; density strictly positive. Helium has a volume-only representation, not a fake zero-density/priced constituent. Composition closure is checked at the recipe level, separately from partial mass/cost coverage.

[AGENT] The exact generic-definition count and aggregation shape can be finalized in the native item: a fixed small sum definition or an already-supported occurrence aggregation may be required. Prefer actual material-child outputs and an explicit represented/unquantified fraction over a monolithic hard-coded recipe function. No new physical performance closure is needed. Independent source/design review should check table transcription, region overlap, price semantics and the partial-inventory output names before implementation.

[AGENT] Acceptance: generate and execute reference unit-volume and alternative unit-volume cases; execute the normalized three-region reference at both taper endpoints; double supplied area and show doubled inventory/prices with unchanged recipe and thickness; vary only one supplied constituent price and show unchanged geometry/mass; verify fractions and unquantified helium volume; reject nonfinite/negative inputs and invalid recipe closure through native execution. Independent arithmetic should check material identities and region sums. No adequacy pair applies because the model evaluates a supplied inventory and contains no capacity or required-equipment selection. MR-7 review must confirm that selected dimensions remain inputs.

[AGENT] This closes a useful part of T02: source-supported constituent decomposition and an executable sector assembly under explicit geometry. It does not close actual reference total inventory, installation costs, breeding, structural adequacy or LCOE.
