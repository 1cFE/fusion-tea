# Design Point Reasoning Trace — 13-electrostatic-hybrid

## 1. Sources walked

- `knowledge/concept_research/13-electrostatic-hybrid/dossier.md` — synthesized Phase 1a summary; used for orientation and to identify which source files contain relevant quantitative claims; confirmed overall data confidence is medium-low
- `knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/avalanche-cwfest2023-blog.md` — CWFest 2023 conference presentation transcript (CEO Robin Langtry); the best public technical document; defines the Q≈1 operating point (~1 kW fusion power at 300 kV / 0.4 T), and the CEO explicitly names "five kilowatts, 10 kilowatts" as the first commercial scale step after Q>1
- `knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/avalanche-orbitron-page.md` — Orbitron product page; states "developing a 1-100kWe compact fusion machine called 'The Orbitron'" and "packaged as a single cell from 5kW to 100s of kW capacity"; primary source for the P_native range
- `knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/avalanche-29m-raise-2026.md` — $29M Series A press release (2026); confirms Q>1 DT test program, FusionWERX facility (licensing expected 2027), and superconducting magnets as long-lead equipment; no P_native for any commercial design
- `knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/avalanche-300kv-press-release.md` — 300 kV milestone press release; confirms steady-state 300 kV achieved at 3 W feedthrough draw, 4.7 MV/m field gradient; CEO states "300,000 Volts is the ideal energy for fusing D-T in our compact machine"; no electrical output figure
- `knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/osti-pages-servlets-purl-2582151.md` — full text of AIP Advances 14(8), 085025 (2024); confirms device geometry (~10 cm anode radius), cathode voltage range (100–300 kV), magnetic field (0.05–0.1 T current / 0.5 T SC target), and PIC simulation results on space-charge mitigation; physics paper, no commercial design point
- `knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/avalanche-fusionwerx-grant.md` — $10M Washington State grant announcement; confirms FusionWERX as a neutron production facility with tritium handling capability; no electrical output by design
- `knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/prnewswire-news-releases-avalanche-energy-announces-new.md` — PRNewswire FusionWERX facility announcement; confirms MoU with Fusion Fuel Cycles, hot cells, integrated tritium management; no P_native
- `knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/ui-2023aps-dpptp1006m-abstract.md` — APS DPP 2023 abstract on ion loading; reports deuterium ions confined at >100 keV in initial tests; no commercial P_native
- `knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/ui-2023aps-dppyo8010l-abstract.md` — APS DPP 2023 scientific overview abstract; states ">1×10^13 n/s" neutron source target for FusionWERX capability; no P_native
- `knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/talk-polywell-orbitron-paper-discussion.md` — Talk-Polywell forum thread (August 2024); community speculation on operating mode and "5 kWe pulsed" estimate; not an authoritative source, confirms no P_native exists in the open record as of mid-2024
- `exploration/concept_analysis/analyses/13-electrostatic-hybrid/analysis.md` — D1+ analysis; used as reference context for understanding what sources exist; not used as a primary source for design-point selection per protocol

## 2. Candidates surfaced

**Neo prototype (current hardware)**
Neo is Avalanche's first Orbitron prototype, operating at approximately 100 kV and 0.05 T with permanent magnets. The APS DPP 2023 abstract reports deuterium ions confined at energies exceeding 100 keV. No electrical output by design — the device is a plasma confinement and diagnostics test bed. P_native: none.

**Marty prototype (current hardware, targeting 300 kV)**
Marty is Avalanche's second Orbitron prototype, designed to reach 300 kV cathode voltage. The 300 kV steady-state milestone was achieved in 2025 (300 kV press release). The CWFest 2023 blog defines the Q≈1 operating point for this device class: 600 W cathode + 400 W ion guns = 1,000 W input → ~1 kW fusion power → Q≈1 as the near-term ceiling. No electrical output by design — at Q=1, net electrical output after thermal conversion (≤30% at device scale) is −0.7 kWe. The device is a physics demonstrator targeting the Q>1 threshold. P_native: none.

**FusionWERX next-generation device (~2027, planned)**
The FusionWERX facility in Richland, WA is the planned Q>1 DT test program site, with tritium licensing expected in 2027 ($29M press release, FusionWERX grant). The stated goal is "demonstrating the world's first net-energy compact fusion system," but FusionWERX is explicitly a commercial neutron production facility and test infrastructure; near-term revenue comes from selling neutrons, not electricity. No electrical output by design. P_native: none.

**Orbitron commercial module — 5 kWe lower bound (aspirational, paper-concept)**
The Orbitron product page states the company is "developing a 1-100kWe compact fusion machine called 'The Orbitron'" and that "The Orbitron can be packaged as a single cell from 5kW to 100s of kW capacity, grouped together however needed to get to megawatt-scale clean energy solutions." The CWFest 2023 blog independently gives the CEO's description of the first commercial scale step after Q>1: "you scale up in terms of voltage and magnetic field, you start making, five kilowatts, 10 kilowatts. Now you start to have a really interesting small scale fusion machine." Two sources anchor 5 kWe as a named point in the commercial range. No engineering design, geometry, or hardware program is tied to this output level. P_native: 5 kWe (0.005 MWe).

**Orbitron commercial module — 100 kWe upper bound (aspirational, paper-concept)**
The same product page states "1-100kWe" as the commercial module range, implying 100 kWe as the upper bound. This figure has no independent textual anchor in the technical sources — only the product page mentions it, and no source elaborates on what device configuration or operating point produces 100 kWe. P_native: 100 kWe (0.1 MWe), grounded by one source only.

## 3. Selection

Three of the five candidates (Neo, Marty, FusionWERX) are physics demonstrators or neutron production facilities with no electrical output by design and do not qualify as design points per the selection rule. The two remaining candidates are both aspirational commercial ranges with no engineering backing. The 5 kWe lower bound is preferred over the 100 kWe upper bound because it is anchored by two independent source references (product page + CEO statement in CWFest 2023), while 100 kWe appears in only one source with no technical elaboration. The 5 kWe value also aligns with the CEO's explicit description of it as the "really interesting" first commercial scale after Q>1, making it the most conservative and most near-term-credible of the available figures.

```yaml
proposal:
  concept_id: 13-electrostatic-hybrid
  design_name: "Orbitron commercial module — lower bound (Avalanche Energy product page / CWFest 2023)"
  maturity_tier: paper-concept
  grounding_confidence: low
  p_native_mwe: 0.005
  primary_sources:
    - knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/avalanche-orbitron-page.md
    - knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/avalanche-cwfest2023-blog.md
  selection_rationale: |
    All three Avalanche hardware designs (Neo, Marty, FusionWERX device) are physics demonstrators or
    neutron production facilities with no electrical output by design and do not qualify as design
    points. The only published P_native figures come from the aspirational commercial product page
    (1–100 kWe per module; "from 5kW to 100s of kW capacity") and the CEO's CWFest 2023 statement
    identifying 5–10 kWe as the first commercial scale step after Q>1. The 5 kWe lower bound is
    anchored by both sources and is selected over the 100 kWe upper bound as the more grounded
    value — it appears in two independent texts and is described as the immediate next commercial
    milestone. No engineering design exists; there is no committed geometry, fuel cycle design, or
    hardware program tied to this output level. P_native is the per-module value; the commercial
    architecture is explicitly modular (many units stacked to megawatt-scale aggregate output).
  alternatives_considered:
    - design: "Neo prototype"
      reason_rejected: "Physics demonstrator with no electrical output by design"
      sensitivity_implication: |
        No P_native — cannot establish a design-point. If a net-electric demonstration were derived
        from Neo-class hardware, per-module output would be sub-kWe (the physics target is ~1 kW
        fusion at Q≈1, with conversion losses making net electricity deeply negative at this scale),
        pushing n_mod far above 200,000 modules at 1 GWe and making any comparison figure illustrative
        only.
    - design: "Marty prototype (Q≈1 DT physics target, 300 kV / 0.4 T)"
      reason_rejected: "Physics demonstrator with no electrical output by design; at Q=1 the device is net-negative electrically after any realistic thermal conversion"
      sensitivity_implication: |
        No P_native as a commercial design. The Marty operating point (1 kW fusion in, 1 kW input)
        implies net-negative electricity at any thermal conversion efficiency below 100%. If the Q>1
        DT demonstration at FusionWERX yields a credible scaling law to net-positive operation, the
        commercial design point would be reset from first principles — no directional estimate is
        possible without that scaling result.
    - design: "FusionWERX facility device (Q>1 DT test program, 2027)"
      reason_rejected: "Explicitly a neutron production and test facility; no electrical output by design"
      sensitivity_implication: |
        No P_native. FusionWERX is the most likely trigger for a mandatory re-selection: if the Q>1
        test program demonstrates net electricity and Avalanche publishes a commercial design derived
        from it, this design point must be replaced. The direction and magnitude of the shift cannot
        be estimated without the test result.
    - design: "Orbitron commercial module — upper bound (100 kWe)"
      reason_rejected: "Upper bound of product-page range; only one source mentions this value, with no technical elaboration or engineering anchor"
      sensitivity_implication: |
        If picked instead, P_native rises 20× (0.1 MWe vs. 0.005 MWe) → n_mod falls from ~200,000
        to ~10,000 modules at 1 GWe → 1 GWe LCOE shifts substantially downward as per-module fixed
        costs spread over far fewer units. Worth revisiting if Avalanche publishes an engineering
        design anchored at higher per-module output.
```

## 4. Open questions

- **Q>1 DT demonstration at FusionWERX (2027+)**: This is the decisive watch event. If Avalanche publishes a net-electric result or a commercial design derived from the Q>1 test program, this design point must be re-selected from scratch. The 5 kWe figure has no engineering basis and will be superseded by any published engineering design.
- **Commercial cell architecture specification**: If Avalanche publishes a technical roadmap that names a specific per-module geometry, operating point, and expected electrical output, the 5 kWe lower bound should be replaced with the published engineering value regardless of direction.
- **Scaling law from Q≈1 (1 kW fusion) to commercial (5+ kWe electrical)**: The CWFest 2023 blog implies 5–10 kWe requires scaling beyond the 300 kV / 0.4 T operating point. If follow-on publications characterize this scaling law, P_native should be re-derived from first principles rather than taken from a marketing range.
- **Energy conversion method at kWe module scale**: The product page states "thermal cycle, utilizing turbines," which is not viable at 5 kWe. If Avalanche discloses a specific small-module conversion approach (thermoelectric or otherwise), the effective electrical P_native may be lower than the stated fusion power target, changing the credible per-module output and the design point.

---

**Verifier note on the selection boundary**: This concept sits at the threshold between "pick with `grounding_confidence: low`" and "route to freeform." The ruling factor is the product page and CWFest 2023 blog, which together name 5 kWe as a specific figure traceable to company communications. If a verifier concludes these aspirational marketing figures do not constitute a published P_native for the purposes of this protocol, the correct routing is freeform on the grounds that all leading hardware designs are neutron-production devices with no electrical design point, and the commercial product is too underspecified to assign a defensible single number.