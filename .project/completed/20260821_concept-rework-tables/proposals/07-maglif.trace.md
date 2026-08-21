# Design Point Reasoning Trace — 07-maglif

## 1. Sources walked

- `knowledge/concept_research/07-maglif/dossier.md` — top-level synthesized summary; confirmed companies (Pacific Fusion, Fuse Energy Technologies), the 250 MWe commercial scenario, and that neither company has published a detailed commercial plant design
- `knowledge/concept_research/07-maglif/iter-02/dossier.md` — full differentiation table dossier; confirmed DS specs (156 modules, ~80 MJ, 60+ MA), no P_native for the DS, and the Fuse hybrid fusion-fission note
- `knowledge/concept_research/07-maglif/iter-02/sources/z-ife-sand2006-7148-thermal-cycles.md` — Olson et al. 2006, SAND2006-7148, Z-IFE power plant final report; the only published systems-level cost model for a MagLIF-class commercial plant; provides P_native, thermal cycle, driver architecture, and COE as a function of rep rate
- `knowledge/concept_research/07-maglif/iter-01/sources/z-ife-power-plant-concept.md` — Derzon et al. 2000, SAND2000-3132J, "An Inertial-Fusion Z-Pinch Power Plant Concept"; establishes 4 m radius / 8 m tall cylindrical chamber, 80 cm FLiBe blanket, 20 cm 6061-T6 Al first wall, 1–30 GJ yields at 0.01–0.1 Hz, RTL concept
- `knowledge/concept_research/07-maglif/iter-02/sources/pacific-fusion-interview-fusion-report.md` — Will Regan (Pacific Fusion President) interview; DS architecture details; confirmed the 250 MWe scenario source
- `knowledge/concept_research/07-maglif/iter-03/sources/ans-news-2025-04-24-article-6980-pacific-fusion-fusing/output.md` — ANS article April 2025; primary source for the LeChien 250 MWe quote; confirmed DS is a gain-demonstration machine, not a power plant
- `knowledge/concept_research/07-maglif/iter-03/sources/pacificfusion-updates-experimental-breakthrough-by-pacific/output.md` — Feb 2026 blog post on self-magnetizing target breakthrough; confirmed DS targets net facility gain by 2030; no commercial plant parameters
- `knowledge/concept_research/07-maglif/iter-03/sources/pacificfusion-updates-founders-letter/output.md` — founders' letter October 2024; confirmed D-T fuel, no commercial plant design published
- `knowledge/concept_research/07-maglif/iter-02/sources/fuse-energy-not-boring-details.md` — Not Boring deep dive; Apeiron I hybrid fusion-fission parameters (~20 MW fusion → ~3,000 MWth → ~1 GWe); TITAN I specs
- `knowledge/concept_research/07-maglif/iter-03/sources/arxiv-2504-10680/output.md` — AMPS paper abstract; confirmed DS specs and net facility gain target; no commercial plant P_native stated
- `exploration/concept_analysis/analyses/07-maglif/analysis.md` — existing D1+ analysis; used as reference for source locations only; design-point choice not preserved

## 2. Candidates surfaced

**Pacific Fusion DS (Demonstration System)**
156 modules, ~80 MJ stored, 60+ MA in ~100 ns, 73m × 80m footprint. Targets net facility gain (Q_facility > 1) by 2030. The DS chamber is a deionized water tank — no thermal cycle, no electrical generation. This is a gain demonstration, not a commercial power plant. No P_native by design. Does not qualify.

**Pacific Fusion "~250 MWe" commercial scenario**
P_native: ~250 MWe. Source: Keith LeChien (CTO), April 2025 ANS article: "One attractive combination would let us produce about 250 net MWe with a very compact footprint of 25 acres or less." One sentence from a public interview with no published geometry, no thermal cycle, no driver architecture. The company's own stated aspiration but with no engineering basis. Maturity tier: paper-concept. Grounding if selected: `low`.

**Z-IFE reference plant, 10-chamber 0.1 Hz baseline (Olson et al. 2006, SAND2006-7148)**
P_native: 1000 MWe (total plant). The only published systems-level cost model for a MagLIF/Z-pinch-class commercial power plant. Architecture: one LTD driver (~$372M, 12,600 cavities), 12 chambers (10 active in rotation at 0.1 Hz each), FLiBe thick-liquid-wall chamber (4 m radius, 80 cm FLiBe sphere, 20 cm 6061-T6 Al first wall), steel RTL, combined Brayton-Rankine thermal cycle at 42% efficiency. D-T fuel. COE: ~20 ¢/kWeh. Full published cost model including driver scaling law and indirect cost structure (93.6% indirect factor). Maturity tier: paper-concept.

**Z-IFE optimized case, 1-chamber 0.5 Hz, frozen-FLiBe RTL (Olson et al. 2006)**
P_native: 1000 MWe. Same plant architecture but single-chamber, 0.5 Hz, and frozen-FLiBe RTL (eliminating the 170 MWe steel-RTL remanufacturing parasitic load). COE: 7.0 ¢/kWeh. Requires frozen-FLiBe RTL technology — undemonstrated in 2006, still undemonstrated today. Grounding if selected: `low`.

**Z-IFE economy-of-scale case, 2-chamber 0.5 Hz, 2000 MWe (Olson et al. 2006)**
P_native: 2000 MWe. Two-chamber economy-of-scale variant. COE: 5.7 ¢/kWeh. Larger plant than the reference. Maturity tier: paper-concept. Grounding: `medium`.

**Fuse Energy Apeiron I (hybrid fusion-fission)**
P_native: ~1000 MWe (confirmed by Sandia SAND2006-6590: 20 MW fusion → 3,000 MWth → ~1 GWe at ~30% conversion; 150× amplification). Architecture: MagLIF fusion neutrons driving fission in a uranium/actinide fluid blanket. Hybrid design — not pure MagLIF commercial power. Applicable only if concept scope includes Fuse's hybrid path. Maturity tier: paper-concept.

## 3. Selection

The Z-IFE reference plant, 10-chamber 0.1 Hz baseline (Olson et al. 2006, SAND2006-7148) is selected. It is the only design in this concept's portfolio with published geometry, power, fuel, thermal cycle, and a systems-level cost model. Pacific Fusion's 250 MWe scenario is the company's own stated target but is an informal back-of-envelope scenario with no engineering basis — grounding would be `low`, and there is nothing to anchor the downstream `analyze` step against. The DS has no electrical output by design. The Z-IFE study was authored by Sandia National Laboratories, whose Z Machine program is the experimental foundation for MagLIF; Pacific Fusion's CRADA with Sandia and the AMPS paper (arXiv:2504.10680) build directly on this heritage, making it the most authoritative available reference for commercial plant architecture. P_native = 1000 MWe for the full reference plant — the LTD driver is shared across 10 chambers in rotation, so the plant is designed as a single integrated unit rather than replicated modules; the plant total is the natural P_native.

```yaml
proposal:
  concept_id: 07-maglif
  design_name: "Z-IFE reference plant, 10-chamber 0.1 Hz baseline (Olson et al. 2006, SAND2006-7148)"
  maturity_tier: paper-concept
  grounding_confidence: medium
  p_native_mwe: 1000
  primary_sources:
    - knowledge/concept_research/07-maglif/iter-02/sources/z-ife-sand2006-7148-thermal-cycles.md
    - knowledge/concept_research/07-maglif/iter-01/sources/z-ife-power-plant-concept.md
  selection_rationale: |
    The Z-IFE reference plant (SAND2006-7148, Olson et al. 2006) is the only published
    systems-level cost model for a MagLIF/Z-pinch-class commercial power plant and is
    therefore the most mature design with the best published quantitative data. It
    documents chamber geometry (4 m radius, 80 cm FLiBe blanket, 20 cm 6061-T6 Al
    first wall), driver architecture (LTD, 12,600 cavities, $372M), thermal cycle
    (combined Brayton-Rankine at 42%), D-T fuel, and COE as a function of rep rate.
    Pacific Fusion's 250 MWe commercial scenario is the company's stated aspirational
    target but traces to a single informal CTO interview quote with no published
    geometry, thermal cycle, or engineering architecture — grounding would be low.
    The DS has no electrical output by design. The 10-chamber 0.1 Hz baseline is the
    study's explicitly designated reference case. P_native = 1000 MWe for the full
    reference plant; the LTD driver is shared across 10 chambers in rotation, making
    the whole plant the natural replication unit rather than a per-chamber module.
  alternatives_considered:
    - design: "Pacific Fusion DS (Demonstration System)"
      reason_rejected: no electrical output by design; pure gain demonstrator
      sensitivity_implication: "n/a — the DS has no P_native and cannot be used as a design point."
    - design: "Pacific Fusion '~250 MWe' commercial scenario (LeChien, April 2025)"
      reason_rejected: single informal CTO quote; no published engineering parameters
      sensitivity_implication: >
        If picked instead, P_native drops substantially (250 vs 1000 MWe) → more
        modules at 1 GWe → 1 GWe LCOE shifts up. The Z-IFE study shows the 500 MWe
        case sits above 10 ¢/kWeh at all modeled rep rates, so a 250 MWe first plant
        would carry materially higher LCOE than the 1000 MWe reference. This is the
        most consequential sensitivity in the candidate set; if Pacific Fusion publishes
        a 250 MWe plant design with engineering parameters, re-select.
    - design: "Z-IFE optimized case, 1-chamber 0.5 Hz, frozen-FLiBe RTL (Olson et al. 2006)"
      reason_rejected: relies on frozen-FLiBe RTL technology that was undemonstrated in 2006 and remains undemonstrated today
      sensitivity_implication: >
        If picked instead, P_native is unchanged (1000 MWe) but the assumed rep rate
        is higher (0.5 vs 0.1 Hz) → same module count but substantially lower COE
        (7.0 vs ~20 ¢/kWeh). Worth probing once frozen-FLiBe RTL technology is
        validated; if demonstrated, would materially improve the 1 GWe LCOE estimate.
    - design: "Z-IFE economy-of-scale case, 2-chamber 0.5 Hz, 2000 MWe (Olson et al. 2006)"
      reason_rejected: larger-plant economy-of-scale variant rather than the reference design point
      sensitivity_implication: >
        If picked instead, P_native rises (2000 MWe) → fewer modules at 1 GWe →
        1 GWe LCOE shifts down (5.7 vs ~20 ¢/kWeh). Captures the upper bound of
        economies of scale from the study; worth probing if commercial deployment
        targets multi-GWe scale.
    - design: "Fuse Energy Apeiron I (hybrid fusion-fission)"
      reason_rejected: hybrid fusion-fission architecture; not pure MagLIF commercial power
      sensitivity_implication: >
        If picked instead, P_native is similar (~1000 MWe) but the power cycle is
        fundamentally different (150× fission amplification at Q << 1). The LCOE
        structure would differ substantially — no tritium breeding blanket required,
        but a uranium/actinide fission circuit instead. Applicable if the concept
        scope is extended to include Fuse's near-term hybrid path, which does not
        require full fusion ignition.
```

## 4. Open questions

- **Pacific Fusion commercial plant design**: The company's explicit commercial target is ~250 MWe with ≤25 acres, but no engineering design exists. If Pacific Fusion publishes a commercial plant design (expected post-DS net-gain milestone in the mid-2030s), the design point should be revised away from the Z-IFE 1000 MWe reference — P_native would likely drop substantially and LCOE would shift up relative to the baseline.
- **IMG driver cost at plant scale**: The Z-IFE $372M LTD driver figure does not apply to Pacific Fusion's IMG architecture. The arxiv roadmap paper identifies the need for a 5–10× cost reduction in energy storage and switching from ~$5/J current commercial pricing. If Pacific Fusion or a government program publishes IMG cost estimates at 60+ MA scale, the driver account — 96% of direct driver capital in the Z-IFE reference — would need to be updated, potentially changing COE by a factor of 2–5× in either direction.
- **DS net-gain results and commercial roadmap (2030 target)**: A successful DS demonstration would likely trigger publication of a commercial plant design with a specific P_native. This is the single most important watch item for design-point revision — DS success followed by a published commercial design would force re-selection away from the Z-IFE reference.
- **Frozen-FLiBe RTL validation**: The Z-IFE 0.5 Hz optimized case (7.0 ¢/kWeh) depends on frozen-FLiBe RTL, which remains undemonstrated. If demonstrated, the 0.5 Hz case becomes credible and the operating scenario selection should be revisited — the LCOE estimate would shift from ~20 ¢/kWeh to ~7 ¢/kWeh without changing P_native.

---

**Key call**: The 250 MWe Pacific Fusion scenario was the main competing candidate. It was rejected because a single back-of-envelope CTO statement does not provide sufficient engineering basis to anchor a cost projection — the downstream `analyze` step would have nothing to work against. The Z-IFE 1000 MWe reference is the right anchor even though it predates Pacific Fusion and uses a different driver technology; the `medium` grounding and the 4× scale difference from Pacific Fusion's stated target are honestly flagged in the open questions.

---

The proposal selects the **Z-IFE reference plant, 10-chamber 0.1 Hz baseline** at **P_native = 1000 MWe**. The critical watch item is Pacific Fusion publishing a commercial plant design after the DS milestone — that would force a re-selection to ~250 MWe with a corresponding upward revision to the LCOE estimate.