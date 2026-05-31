# Design Point Reasoning Trace — 04-laser-icf

## 1. Sources walked

- `knowledge/concept_research/04-laser-icf/dossier.md` — synthesized summary; used for orientation and to identify which sources carry quantitative claims; confirmed no named commercial plant exists
- `knowledge/concept_research/04-laser-icf/iter-01/sources/hb11-patent-reactor-design.md` — US Patent US10410752B2 (Hora 2018); defines reactor geometry, laser specs, per-shot energy, and energy conversion approach; the only document in the portfolio with a self-consistent reactor architecture
- `knowledge/concept_research/04-laser-icf/iter-01/sources/hb11-technology-page.md` — HB11 website (2021 vintage); describes ~1 Hz repetition rate, 1 GW baseload aspiration, and original direct electrostatic energy conversion claim
- `knowledge/concept_research/04-laser-icf/iter-01/sources/hb11-company-overview.md` — HB11 company overview (general stage/funding context)
- `knowledge/concept_research/04-laser-icf/iter-01/sources/hb11-osaka-experiment-2022.md` — Batani et al. 2022 Osaka LFEX result; experimental context only (10^10 alpha/sr, 4 orders below breakeven)
- `knowledge/concept_research/04-laser-icf/iter-02/sources/hb11-technology-page-2025.md` — HB11 website (2025 vintage); confirms pivot to "conventional steam cycle generator," aspirational 1 GW target; content extremely brief in extraction
- `knowledge/concept_research/04-laser-icf/iter-02/sources/hb11-recent-developments-2024-2025.md` — DOE INFUSE grant, Adelaide USPL collaboration; no plant-level numbers
- `knowledge/concept_research/04-laser-icf/iter-02/sources/hb11-newatlas-article.md` — New Atlas 2020 interview; McKenzie describes aspirational reactor concept with direct energy conversion; no P_native
- `knowledge/concept_research/04-laser-icf/iter-03/sources/link-10-1007-s10894-023-00349-9/output.md` — McKenzie et al. 2023, "HB11—Understanding Hydrogen-Boron Fusion as a New Clean Energy Source," *J. Fusion Energ.* 42, 17; company-authored peer-reviewed paper; contains HB11's formal technoeconomic model with explicit 500 MW scenario calculation — the most specific P_native traceable to a company publication
- `knowledge/concept_research/04-laser-icf/iter-03/sources/hb11-our-technology/output.md` — HB11 technology page (2026 extraction); effectively empty extraction (16 lines), no quantitative content
- `knowledge/concept_research/04-laser-icf/iter-03/sources/power-technology-features-hb11-the-australian-start-up/output.md` — Power Technology 2020 interview with McKenzie; describes aspirational reactor form-factor (compact sphere, direct charge collection), no P_native
- `knowledge/concept_research/04-laser-icf/iter-03/sources/fusionxinvest-company-profile-4353-hb11-energy/output.md` — FusionXInvest profile; locked behind paywall; general description only
- `knowledge/concept_research/04-laser-icf/iter-03/sources/prnewswire-news-releases-hb11-energy-receives-grant-from-us/output.md` — DOE INFUSE grant press release; stage/partnership context, no P_native
- `knowledge/concept_research/04-laser-icf/iter-03/sources/globenewswire-news-release-2025-02-10-3023820-0-en-general/output.md` — General Atomics TINEX announcement; confirms HB11 membership in the DOE IFE industry council, not HB11-specific design data
- `knowledge/concept_research/04-laser-icf/iter-03/sources/newatlas-energy-hb11-laser-fusion-demonstration/output.md` — New Atlas 2022; Osaka LFEX result, no plant specs
- `knowledge/concept_research/04-laser-icf/iter-03/sources/interestingengineering-energy-hb11-joins-largest-laser-lab/output.md` — IE 2024; ELI ERIC partnership; no plant specs
- `knowledge/concept_research/04-laser-icf/iter-03/sources/unsw-newsroom-news-2020-02-pioneering-technology-promises/output.md` — UNSW newsroom 2020; patent announcements; mentions aspirational "compact sphere" form-factor; no P_native
- `knowledge/concept_research/04-laser-icf/iter-03/sources/hb11-wp-content-uploads-2025-03/` — Raw PDF (unextracted); only images present; could not be read as text; may contain more recent whitepaper content (noted as open question below)

## 2. Candidates surfaced

**Candidate A — Patent reactor unit (US10410752B2, Hora 2018)**
- Architecture: single reaction chamber with HB11 cylindrical fuel body (1 cm × 0.2 mm), capacitor-coil kT magnetic field, 30 kJ picosecond laser pulse, direct electrostatic conversion at −1.4 MV via Faraday cage
- Per-shot output: 1 GJ gross fusion energy per reaction at 1 Hz, yielding ~714 A discharge at −1.4 MV (~1 GW gross electrical per chamber by the patent's own numbers)
- P_native: No commercial plant P_native is stated. The patent describes a single reaction unit and mentions "a plurality of reaction chambers operated alternately for quasi-continuous operation" but gives no plant-level aggregation or net electrical figure. The 1 GJ/shot at 1 Hz is gross per unit; wall-plug losses for the laser system are not deducted.
- Maturity: pre-commercial paper concept (2018); architecture antedates the "thousands of commercial lasers" approach now described on the company website
- Disqualified: the patent never states a net MWe for a plant — it describes a single reaction module

**Candidate B — HB11 technoeconomic model scenario, 500 MWe (McKenzie et al. 2023)**
- Source: McKenzie et al., *J. Fusion Energ.* 42, 17 (2023) — company-authored, peer-reviewed, co-signed by most of HB11's scientific leadership
- The paper's commercialisation section states: "Assuming a recirculating power fraction of 10%, a 500 MW power plant would require 50 MW to drive the laser system that would produce an average laser power output of 10 MW (ignoring energy usage by the other subsystems)."
- P_native: 500 MWe (the paper refers to this as the plant's rated output; 50 MW recirculates to the laser system)
- The 500 MW is a worked scenario calculation — not a committed or named design. No geometry, no plant architecture, no fuel cycle throughput specified.
- Maturity: paper-concept (worked example within technoeconomic model)
- Grounding: low — scenario projection; no committed plant, no engineering architecture

**Candidate C — HB11 website 1 GW baseload target (company communications 2021–2025)**
- Stated on multiple iterations of hb11.energy: "1 GW baseload power using arrays of thousands of commercial lasers"
- P_native implied: 1000 MWe
- No published engineering parameters of any kind — purely aspirational marketing communications
- Maturity: aspirational target in company communications

**Non-qualifying (physics demonstrators with no electrical output by design):** current laser experiments (LFEX Osaka 2022, ELI Beamlines, LLE/Rochester INFUSE); Adelaide USPL collaboration.

## 3. Selection

HB11 Energy has no named commercial plant design with engineering parameters anywhere in its published portfolio. The most specific P_native traceable to a company source is the 500 MWe scenario in McKenzie et al. 2023 (*J. Fusion Energ.*), a company-authored peer-reviewed technoeconomic paper. Per the selection guidance, any electrical output figure traceable to a company source qualifies as a design point with `grounding_confidence: low`, rather than routing to freeform. The 500 MW scenario is selected over the 1 GW website aspiration because it appears in a peer-reviewed publication tied to explicit technoeconomic assumptions (η = 20% laser wall-plug efficiency, f = 0.10 recirculating power fraction), making it the more specific and citable figure.

```yaml
proposal:
  concept_id: 04-laser-icf
  design_name: "HB11 Energy 500 MWe technoeconomic model scenario (McKenzie et al. 2023)"
  maturity_tier: paper-concept
  grounding_confidence: low
  p_native_mwe: 500
  primary_sources:
    - knowledge/concept_research/04-laser-icf/iter-03/sources/link-10-1007-s10894-023-00349-9/output.md
    - knowledge/concept_research/04-laser-icf/iter-01/sources/hb11-patent-reactor-design.md
  selection_rationale: |
    No named commercial plant design exists in HB11 Energy's published portfolio. The most
    specific electrical output figure traceable to a company source is the 500 MWe scenario
    used in McKenzie et al. 2023 (J. Fusion Energ. 42:17), HB11's formal peer-reviewed
    technoeconomic paper, where 500 MW is the baseline for calculating recirculating power
    requirements (f = 0.10, η = 20% laser efficiency). This is a scenario calculation, not a
    committed plant design — there is no accompanying geometry, named architecture, or fuel
    cycle throughput for the 500 MW figure. The company's 1 GW website target is rejected as
    a marketing aspiration with no published parameters of any kind. The patent reactor
    (US10410752B2) is rejected as a P_native source because it describes a single reaction
    unit with no commercial plant-level aggregation or net electrical figure. The 500 MWe is
    treated as a single-plant value; there is no documented multi-module architecture in the
    sources, so n_mod = 1000/500 = 2 in the 1 GWe projection. The design point is asterisked
    as poorly grounded in the comparison view.
  alternatives_considered:
    - design: "Patent reactor concept, single unit (US10410752B2, Hora 2018)"
      reason_rejected: "No net P_native stated for a commercial plant; describes one reaction
        chamber with gross per-shot energy but no plant-level aggregation or net electrical
        figure"
      sensitivity_implication: |
        If the per-chamber patent architecture were used to derive a P_native (e.g. 1 GJ/shot
        at 1 Hz with direct electrostatic conversion → several hundred MWe net per chamber
        depending on assumed efficiency), the resulting p_native_mwe could be in a broadly
        similar range to 500 MWe depending on assumed laser recirculating power. Direction of
        change is uncertain — no net figure is specified. Worth revisiting only if a plant-level
        analysis of the patent architecture is published with an explicit net figure.
    - design: "HB11 website 1 GW baseload target (company communications 2021–2025)"
      reason_rejected: "Purely aspirational marketing communications with no engineering
        parameters; less specific than McKenzie 2023 scenario which carries explicit
        technoeconomic assumptions"
      sensitivity_implication: |
        If picked instead, P_native would rise substantially from 500 to 1000 MWe → only one
        module needed at 1 GWe scale → 1 GWe LCOE would shift down (fixed reactor island costs
        spread over a larger single plant). Worth probing if the company ever publishes
        engineering parameters for a 1 GW design, at which point the 1 GW target would
        supersede the 2023 scenario.
```

## 4. Open questions

- **Unextracted 2025 whitepaper (`iter-03/sources/hb11-wp-content-uploads-2025-03/raw.pdf`)**: A 2025 HB11 whitepaper PDF is present in the research directory but was not extracted to text — only images were generated. If this whitepaper contains a specific commercial plant design or a more recent P_native target, it would replace the McKenzie 2023 scenario as the primary source and could change the selection entirely.

- **Mehlhorn 2024 perspective paper** (*Physics of Plasmas* 31(2), 2024): Co-authored by HB11's lead theoretician; a 50-year IFE retrospective from KMS Fusion to HB11. Not extracted from PDF. Could contain an updated technoeconomic model or plant-level target that supersedes the McKenzie 2023 scenario.

- **Phys. Rev. Research 2025 paper** (PhysRevResearch.7.013230): 2025 experimental paper with novel targets; not extracted. If the new target results represent a significant yield improvement, the company may have updated its commercial scale target.

- **TINEX/DOE FIRE submission**: HB11 joined the TINEX IFE industry council (DOE FIRE Collaboratives, Feb 2025). Industry council membership typically involves characterizing a commercial plant concept for DOE review. If HB11 has made a submission with a plant-level target, that figure would supersede the 2023 scenario.

- **Direct vs. steam conversion pivot**: The patent (2018) and early communications (2020) described direct electrostatic conversion of alpha particles; the 2025 website explicitly states "conventional steam cycle generator." The McKenzie 2023 paper discusses both options. A future publication committing to a specific conversion pathway with efficiency data could materially shift the implied plant size.

---

The document is complete. To save it, please approve the write to `exploration/concept_analysis/analyses/04-laser-icf/design-points/proposal.md`.

**Key decisions explained:** HB11 Energy has no named commercial plant anywhere in its portfolio — the company is pre-ignition (4 orders of magnitude below breakeven). The only citable electrical output figure in a company-authored publication is the "500 MW power plant" worked example in McKenzie et al. 2023 (*J. Fusion Energ.*), used to illustrate their technoeconomic model's recirculating power requirement. That scenario is selected with `grounding_confidence: low` rather than routing to freeform, per the guidance that any traceable number qualifies. The 1 GW website aspiration and the patent's per-unit energy numbers are rejected as alternatives — both lack the specificity of the 2023 paper's scenario. The unextracted 2025 whitepaper PDF is the most significant open question: if it contains an updated plant target, the selection should be revisited.