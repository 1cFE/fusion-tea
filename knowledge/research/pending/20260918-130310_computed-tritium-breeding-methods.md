# Computed breeding: physical methods and applicability

## Question and scope

[OWNER] Can achieved tritium production be calculated from the retained stellarator blanket configuration, independently checked, and compared with a justified requirement that constrains design? The unchanged target is R2c.P3 at rubric revision dc0f0b6dc6512b29e1307da647f3a508a1f5356d. This report investigates physical methods before implementation. Recommendations are [AGENT]; source statements are attributed below. It does not approve a blanket redesign, change the model or claim target completion.

ARIES remains sealed. Neither the excluded stellarator-demo concept nor barred derivatives were read. Admissibility follows `knowledge/holdout/aries-cs/PROTOCOL.md`. New primary sources passed the native registry screen. Broad research request REQ-computed-tritium-breeding-01 used six queries and three capture attempts; a specific thesis candidate then received its own one-capture request REQ-computed-tritium-breeding-02. The first request's failed URL receipt remains queued even though downloading and registering the same PDF locally succeeded. No operator retrieval is needed for that receipt.

## What the current model means

Achieved TBR is an input of 1.074, while the existing predicate checks only a fixed 1.05 floor. TBR means tritium atoms produced in the blanket per fusion reaction consuming one tritium atom. The fuel calculation independently computes the production needed under its loss assumptions, but its negative margin is not asserted. Trace: `work/orchestration/goals/computed-tritium-breeding/evidence/current-trace.md`, supported by current SysML, generated pipeline, feasibility predicates and oracle mappings.

The retained scenario explicitly uses helium-primary PbLi with a generic 0.80 m breeding layer, 0.20 m reflector and 0.05 m first wall. Its blanket-account volume also includes first wall and reflector, so that volume is not pure breeder inventory. Changing thickness changes build, coil geometry, capital and replacement costs; it does not currently change breeding. A physics implementation must share the actual layer choices, own material/enrichment inputs, expose calculated production to the fuel and feasibility consumers, and update executable/oracle dependency classification.

## Original Stellaris is a different physical blanket

Lion et al. (2025), original PDF pp.17–19, describes water-cooled PbLi, separate helium first-wall cooling, 73.5% PbLi /12.5% water /14% EUROFER97 by volume and 70% lithium-6 enrichment. Mean first-wall and breeding thicknesses are approximately 3 cm and 43.1 cm. Its three-dimensional neutron-transport result is 1.1070 ± 0.0002 before a separate 3% heating-port allowance gives 1.074. The statistical uncertainty is not total predictive uncertainty. A one-dimensional exponential in the paper concerns fast-neutron shielding, not TBR.

These facts were visually checked against original pages by the source researcher and independent reviewer. Durable authority: `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf`. The current model already discloses the conditional transfer from water/PbLi to its helium alternative. Older DI-007/DI-008 wording cannot establish the original source's blanket coolant; any knowledge-index correction belongs in a separately approved native insight operation.

## Methods investigated

| Candidate | Useful evidence | Current applicability limit |
|---|---|---|
| Published Stellaris result or shielding exponential | Full source configuration and one 3D breeding result | One point cannot justify a geometry law; shielding attenuation is not tritium production |
| PROCESS HCPB correlation | Existing material/build-dependent reduced model | Solid ceramic breeder differs from PbLi; adopting it changes technology |
| Lyytinen2024 thickness scan | Genuine DCLL transport response over 25–75 cm and a separate Serpent2/MCNP6 comparison | Current 80 cm breeder exceeds scan; materials, surrounding layers and geometry differ; code benchmark is a different assembly |
| Shimwell2019 HCLL surrogate | PbLi enrichment and poloidal channel-height response with coupled wall/plate dimensions | Missing current internal structure and transfer evidence; current 50 mm wall exceeds source law's range; printed plate coefficient is inconsistent |
| Martinez2012 HCLL neural network | Complete 26-input, nine-hidden-neuron executable coefficients, source examples and independent 3D transport comparison | Source-domain tokamak model; current build violates multiple bounds; stellarator transfer uncertainty unestablished |
| New reduced transport | Reaction-rate production from explicit materials and geometry could retain current technology/build | Needs material specification, nuclear data, benchmark reproduction and quantified geometric reduction; not installed in current runtime |

The source researcher assessed internal literature first; detailed evidence and original-page inspection records are in `evidence/internal-source-assessment.md` under the goal. Fresh review is `evidence/method-review.md`.

## What the acquired sources add

Lyytinen et al. (2024), DOI 10.1088/1741-4326/ad4f9f, provides a five-point DCLL thickness curve and a Serpent2–MCNP6 comparison. Figure 6 reproduces an earlier publication; those are not two independent datasets. The cross-code test uses a simpler LiPb assembly than the later DCLL scan. It is useful computational evidence, not experimental validation of the retained plant. Registered at `knowledge/sources/proof_of_principle_of_parametric_stellarator_neutronics/`.

Shimwell et al. (2019), Nuclear Fusion 59 046019, Figure 6, gives TBR 1.235 at 90% lithium-6 enrichment and 34.5 mm PbLi poloidal height. Its maximum 1.278 ± 0.010 is a reported surrogate 5σ interval, not a total reactor uncertainty. The original printed Eq.2 has a discrepancy: 10/(1.1×274)=0.03318, while the numerical coefficient printed is3.332. Neither silently correcting the publication nor using the larger coefficient is justified for model integration. Registered at `knowledge/sources/multiphysics_analysis_with_cad_based_parametric_breeding/`; original PDF page 8 was visually inspected.

Martínez Arroyo (2012), *Development of a surrogate model for simplified neutronic calculations involved in the design stage of a thermonuclear fusion reactor*, uses a two-dimensional surface-preserving tokamak model for global TBR and a separate one-dimensional model for local quantities. Its Appendix B.7 prints normalization, weights and evaluation code. Thus a missing transport installation does not prevent testing this surrogate. Original PDF page 61 Table 4-4 compares reduced and 3D DEMO TBR over ten cases, with deviations from −1.29% to +1.42%. That limited comparison is physical-model evidence distinct from copying the neural-network implementation; it does not bound stellarator error. Registered at `knowledge/sources/neutronic_fusion_thesis_martinez_arroyo_javier/`.

The published surrogate domain includes 2–4 cm first wall and 30–60 cm inboard breeder. The retained build has 5 cm and 80 cm respectively. Clipping these inputs to fit would change the design, while unrestricted evaluation would conceal extrapolation. The source-domain executable probe is recorded separately; no output from it is the retained stellarator's achieved breeding.

## Requirement and production are separate

The existing atom balance is `T_required = [B + (1-r)(B/f-B) + lambda*I + G]/(eta*B)`. Here B is burn rate; f is single-pass burn fraction; r is recovered fraction of exhausted fuel; I is inventory subject to decay; G is inventory-growth/reserve demand; eta is extraction of newly bred tritium. Production in the blanket, recovery of unburned exhaust and extraction from breeder are different streams.

At f=0.05, each atom burned requires injecting 20 atoms and exhausting 19. Assuming r=0.99 loses 0.19 atoms permanently. With unity breeder extraction and zero decay/growth, required production is 1.19. Held 1.074 passes the old floor by 0.024 but misses this conditional requirement by 0.116. The calculation is reproduced by `evidence/threshold-check.py` and JSON under the goal, independently reviewed. The 0.99 number originated in feedstock costing, not validated isotope recovery. This is a conditional inconsistency, not proof of the physical plant's deficit.

[AGENT] Retain the 1.05 design floor and a separately named physical-balance requirement rather than silently choosing the smaller threshold or adding an unexplained blanket reserve twice. Before asserting a self-sufficiency claim, establish physical recovery/extraction assumptions and label unresolved inventory/reserve terms. A conservative conditional screen may be useful, but must state the scenario it judges. Do not tune recovery to restore passing designs.

## Recommendation and next step

[AGENT] Reproduce and test the published HCLL surrogate in its own domain before deciding how much it can contribute. Preserve explicit domain refusals for the current build. For the retained design, define isotope/material cards, architecture and geometry mapping, then acquire or generate transport evidence covering the actual build. Use source cases withheld from fitting to test reduced-geometry error and maintain separate numerical, nuclear-data and applicability uncertainty.

[OWNER] Changing blanket technology or intended plant concept is reserved. The fresh reviewer returns OWNER_GATE for plant integration and releases source-domain reproduction. The coordinator has surfaced the physical-target choice: retain the present helium/PbLi build and develop matching evidence; authorize an explicit HCLL redesign; or target original water/PbLi with its plant consequences. Owner choice cannot itself validate scientific transfer.

No admissible method is yet qualified for the current plant. This does not prove that an adequate method is unavailable. It records precise missing evidence and a tested candidate; it does not close the breeding gap or meet P3.

## Executed source-domain check

The recovered appendix network computes raw TBR 1.1352853788 at the thesis reference inputs, compared with the separately printed final-module result 1.13509. The difference is +0.0001953788 (about 0.0172%); it has not been tuned away. Appendix B.7 labels its example `Rn_9_0`, whereas the selection record names trial 1. That is a possible explanation, not an established resolution. Applying the source's reduction and network-error allowance gives 1.1165440665, compared with printed 1.11635116861. These are source-domain diagnostics only.

The same recovered network gives 1.0828576245 at lithium-6 fraction 0.70 and 1.1113864481 at 0.80, with all other reference inputs held. Inboard breeder thicknesses 35 and 55 cm give 1.1053023249 and 1.1583014259. An 80 cm inboard layer is rejected by the explicit input-domain check. Failed/excluded input is preserved. This demonstrates real configuration response and a functioning research executable; it does not establish the stellarator's response, coupled costs or P2/P3.

Reproduction evidence: `work/orchestration/goals/computed-tritium-breeding/evidence/hcll_surrogate_probe.py`, `hcll-surrogate-probe-results.txt` and `hcll-surrogate-assessment.md`. The researcher compared all 253 weights and four normalization arrays between direct PDF text and registered extraction, and viewed the original code pages. The independent reviewer separately checks the implementation. No native plant study, generated package change, model work item or new study-ready pin has been produced because physical applicability precedes those stages.

## Independent probe review

The fresh reviewer matched every published coefficient against original PDF text and compiled the original C++ evaluation function. It agrees with the recovered Python implementation within 2.3e-16 over five checked cases. This is software verification of the example network, not physical validation or resolution of the final-module discrepancy. The thesis's final-network error statistics have not been independently established for this example network; the reported corrected output is therefore a diagnostic using the published correction, not a qualified lower bound. See the dated probe addendum in `work/orchestration/goals/computed-tritium-breeding/evidence/method-review.md`.
