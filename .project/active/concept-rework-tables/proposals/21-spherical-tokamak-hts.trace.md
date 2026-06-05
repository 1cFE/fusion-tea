# Design Point Reasoning Trace — 21-spherical-tokamak-hts

## 1. Sources walked

- `knowledge/concept_research/21-spherical-tokamak-hts/dossier.md` — synthesized summary; used for orientation and identification of key sources.
- `knowledge/concept_research/21-spherical-tokamak-hts/iter-03/sources/tokamak-energy-st-e1-dpp2025-abstract.md` — APS DPP 2025 overview abstract (Maartensson et al.); defines ST-E1 Revision D: R=5.0m, A=2.3, B=5.25T, 450–750 MWe, TBR=1.2, outboard liquid lithium blanket.
- `knowledge/concept_research/21-spherical-tokamak-hts/iter-02/sources/tokamak-energy-st-e1-design-evolution.md` — World Nuclear News article covering DPP 2024 early parameters: A=2.0, R=4.25m, B=4.25T (superseded initial iteration).
- `knowledge/concept_research/21-spherical-tokamak-hts/iter-02/sources/tokamak-energy-roadmap.md` — ANS Nuclear News on ST80-HTS announcement; documents 2022 "up to 200 MWe" aspirational target.
- `knowledge/concept_research/21-spherical-tokamak-hts/iter-04/sources/prnewswire-news-releases-tokamak-energy-announces-st80-hts/output.md` — Oct 2022 press release; confirms "up to 200 MW" and ST80-HTS as demonstrator with no electrical output.
- `knowledge/concept_research/21-spherical-tokamak-hts/iter-04/sources/theengineer-content-news-tokamak-energy-st80-hts-hailed-as/output.md` — The Engineer (2022); confirms ST80-HTS design and "up to 200MW" aspirational figure.
- `knowledge/concept_research/21-spherical-tokamak-hts/iter-03/sources/tokamak-energy-ec-heating-pilot-plant.md` — Alieva et al. EPJ 2026; peer-reviewed subsystem paper confirming ST-E1 FPP is the active design basis with EC-only flat-top heating.
- `knowledge/concept_research/21-spherical-tokamak-hts/iter-03/sources/tokamak-energy-demo4-magnets.md` — Demo4 press release (Nov 2025); magnet validation milestone, not a commercial design point.
- `knowledge/concept_research/21-spherical-tokamak-hts/iter-04/sources/tokamakenergy-our-fusion-energy-and-hts-technology-fusion/output.md` — TE technology page; company context only, no new design parameters.
- `knowledge/concept_research/21-spherical-tokamak-hts/iter-04/sources/tokamakenergy-about-us-fusion-energy-high-temperature/output.md` — TE about-us page; company structure and funding, no design parameters.
- `knowledge/concept_research/21-spherical-tokamak-hts/iter-01/sources/pulsed-spherical-tokamak-paper.md` — Gryaznevich et al. MDPI Plasma 2022; introduces ST280-5T generic study device (R0=2.8m, A=1.9, Bt=5T, Pf=800 MW thermal) — academic parametric device, not a TE commercial candidate.
- `knowledge/concept_research/21-spherical-tokamak-hts/iter-01/sources/tokamak-energy-overview.md` — TE homepage; general company description, no design parameters.
- `exploration/concept_analysis/analyses/21-spherical-tokamak-hts/analysis.md` — prior analysis; used for source identification only. Confirmed DPP 2024 early parameters (A=2.0, R=4.25m, 85 MWe) and Revision D as final design point.

## 2. Candidates surfaced

**ST-E1 Revision D (DPP 2025) — SELECTED**
- `P_native`: 450–750 MWe net (range; "depending on technology and physics assumptions" — uncertainty bounds on a single design, not distinct named phases)
- Geometry: R=5.0m, A=2.3, B=5.25T on-axis
- Fuel: D-T; Blanket: outboard-only liquid lithium, TBR=1.2
- Maturity: Pre-conceptual design point, documented in APS DPP 2025 abstract and EPJ 2026 subsystem paper
- Published: machine geometry, field strength, output range, blanket type and TBR, heating approach (EC-only flat-top), maintenance scheme compatibility
- Not published: Q value, fusion power, thermal cycle type, auxiliary heating power, capital cost

**ST-E1 early design (DPP 2024 iteration)**
- `P_native`: 85 MWe net (per prior analysis citing design-evolution source)
- Geometry: A=2.0, R=4.25m, B=4.25T
- Maturity: Superseded initial iteration, disclosed as starting point not final design

**ST-E1 2022 aspirational target ("up to 200 MWe")**
- `P_native`: "up to 200 MW" per 2022 press release and media
- Geometry: None published at this stage
- Maturity: Pre-design aspirational figure; predates all engineering iterations; no geometry or engineering basis

**ST80-HTS (bridging demonstrator)**
- `P_native`: None — physics demonstrator, no net electrical output by design
- Disqualifier: Does not qualify as a design point per selection rule

**ST280-5T (Gryaznevich et al. 2022 academic study device)**
- `P_native`: implied ~200 MWe net from 800 MW thermal (not explicitly stated; placeholder efficiency assumed)
- Maturity: Generic parametric study device; not a Tokamak Energy named commercial plant; no engineering architecture attached
- Disqualifier: Academic study device, not a committed TE commercial design

## 3. Selection

ST-E1 Revision D, technology-conservative case (450 MWe), is selected. It is the most-mature design in Tokamak Energy's portfolio with published quantitative data: the final pre-conceptual design point documented at APS DPP 2025, with published geometry, field, fuel, and blanket. The DPP 2025 abstract states 450–750 MWe "depending on technology and physics assumptions" — a single design with uncertainty bounds, not distinct named phases. The lower bound (450 MWe) is the technology-conservative anchor, traces directly to the primary source, and does not require optimistic assumptions not yet validated at hardware level.

```yaml
proposal:
  concept_id: 21-spherical-tokamak-hts
  design_name: "ST-E1 Revision D, technology-conservative case (Maartensson et al., DPP 2025)"
  maturity_tier: paper-concept
  grounding_confidence: medium
  p_native_mwe: 450
  primary_sources:
    - knowledge/concept_research/21-spherical-tokamak-hts/iter-03/sources/tokamak-energy-st-e1-dpp2025-abstract.md
    - knowledge/concept_research/21-spherical-tokamak-hts/iter-02/sources/tokamak-energy-st-e1-design-evolution.md
    - knowledge/concept_research/21-spherical-tokamak-hts/iter-03/sources/tokamak-energy-ec-heating-pilot-plant.md
  selection_rationale: |
    ST-E1 Revision D is Tokamak Energy's final pre-conceptual design point, documented at APS DPP 2025
    (Maartensson et al.), with published geometry (R=5.0m, A=2.3, B=5.25T on-axis), fuel (D-T),
    and blanket (outboard liquid lithium, TBR=1.2). The published net power range is 450–750 MWe
    depending on technology and physics assumptions; this is not a multi-phase design but a single
    architecture with uncertainty bounds. The lower bound (450 MWe) is selected as the
    technology-conservative anchor: it traces directly to the published primary source and does not
    require optimistic assumptions not yet validated at hardware level. This design supersedes all
    earlier ST-E1 iterations and is the basis for Tokamak Energy's DOE Milestone-Based Fusion
    Development Program work.
  alternatives_considered:
    - design: "ST-E1 Revision D, technology-optimistic case (750 MWe)"
      reason_rejected: "same design, upper uncertainty bound; requires optimistic technology and physics assumptions not yet validated"
      sensitivity_implication: >
        If picked instead, P_native rises substantially (750 vs. 450 MWe) → fewer modules at 1 GWe →
        1 GWe LCOE shifts down. Worth probing if Tokamak Energy publishes an engineering basis for the
        optimistic assumptions (e.g., higher thermal efficiency, higher Q).
    - design: "ST-E1 early design, DPP 2024 iteration (A=2.0, R=4.25m, ~85 MWe)"
      reason_rejected: "superseded earlier iteration; replaced by Revision D after the company's own six-month design cycle"
      sensitivity_implication: >
        If picked instead, P_native drops substantially (85 vs. 450 MWe) → many more modules at 1 GWe
        → 1 GWe LCOE shifts up significantly. Not a viable pick — the company explicitly discarded
        this design point; it represents the start of the design process, not the outcome.
    - design: "ST-E1 2022 aspirational target (up to 200 MWe)"
      reason_rejected: "pre-design aspirational figure with no published geometry; predates all engineering iterations"
      sensitivity_implication: >
        If picked instead, P_native is lower (200 vs. 450 MWe) → more modules at 1 GWe → 1 GWe LCOE
        shifts up. Not a viable pick — this figure lacks any engineering basis and has been implicitly
        superseded by Revision D's published range.
    - design: "ST80-HTS bridging demonstrator"
      reason_rejected: "physics demonstrator with no net electrical output by design; disqualified by selection rule"
      sensitivity_implication: "n/a — no P_native exists for this device"
```

## 4. Open questions

- **Power range resolution**: The 450–750 MWe range is wide (factor of 1.67×). If Tokamak Energy publishes a more specific design point from detailed engineering studies — or explicitly names the technology assumptions bounding the two ends — the selected P_native should be revisited. A single committed value would upgrade `grounding_confidence` to `high`.
- **Thermal cycle disclosure**: The power conversion cycle (steam Rankine vs. sCO2 Brayton) is undisclosed after four research iterations. Disclosure would materially affect the thermal efficiency underpinning the 450–750 MWe range.
- **Q value / fusion power**: Not published. If a future subsystem paper discloses the plasma gain or fusion power target, the 450 MWe lower bound can be cross-checked for internal consistency.
- **ST80-HTS experimental results (2026 target)**: If ST80-HTS meets its performance targets, Tokamak Energy may update the ST-E1 design point. Post-ST80-HTS revision could shift P_native in either direction.
- **Design phase progression**: ST-E1 was explicitly "pre-conceptual" at DPP 2025. A transition to conceptual or preliminary design — expected as DOE Milestone milestones are met — would likely bring published engineering parameters and a more committed P_native. This is the highest-probability path to upgrading `grounding_confidence` from `medium` to `high`.

---

**Key selection decisions to flag for human review:**

1. **450 MWe vs. 750 MWe**: The 450–750 MWe range is inherently ambiguous — the document doesn't name a "conservative" case vs. an "optimistic" case; it just states the range. Picking 450 is a judgment call (technology-conservative anchor); a verifier might reasonably prefer 600 MWe (midpoint) or argue the choice is arbitrary without further source evidence distinguishing the two ends.

2. **`medium` vs. `low` grounding**: The design has published geometry and a fuel/blanket architecture, pushing toward `medium`, but the power is a range not a committed value and key parameters (Q, thermal efficiency) are unpublished. If the verifier reads `medium` as requiring a committed single power value, this could be downgraded to `low`.