# Design Point Reasoning Trace — 12-levitated-dipole

## 1. Sources walked

- `knowledge/concept_research/12-levitated-dipole/dossier.md` — synthesized two-iteration summary; used to orient to key sources and confirm concept overview (D-T, HTS levitated dipole, OpenStar Technologies roadmap)
- `knowledge/concept_research/12-levitated-dipole/iter-01/sources/arxiv-2602-20564-dt-dipole-power-plants.md` — Simpson et al. (2026), "Deuterium-Tritium Levitated Dipole Fusion Power Plants" (arXiv 2602.20564); primary authority for all design-point parameters including net electric power, geometry, magnet specs, neutronics, and plant power balance for Reactor A (208 MWe) and Reactor B (74.5 MWe)
- `knowledge/concept_research/12-levitated-dipole/iter-01/sources/arxiv-2508-17691-junior-design-results.md` — Chisholm et al. (2026), "Design and initial results from the Junior Levitated Dipole Experiment" (arXiv 2508.17691); Junior prototype specs (5.2 m vacuum vessel, 5.6 T REBCO core magnet, no electrical output by design); confirms Junior is a physics demonstrator
- `knowledge/concept_research/12-levitated-dipole/iter-01/sources/openstar-prototype-roadmap.md` — IEEE Spectrum (Feb 2025), "A New Fusion Prototype Floats Into Action"; CEO Mataira quotes on commercial scale aspiration ("25–50 MW units for data centers" and "multigigawatt units"), confirms Junior is not an electrical design point
- `knowledge/concept_research/12-levitated-dipole/iter-02/sources/openstar-2026-funding-tahi-timeline.md` — Bloomberg (Feb 2026), "Nuclear Fusion Startup Claims Major Advance in New Zealand Trial"; NZ$35M funding, roadmap confirmation (Junior → Tahi → Maui → Tama Nui), Tama Nui described as "may produce 50 to 200 megawatts of electricity" — no engineering parameters

## 2. Candidates surfaced

**Junior prototype (OpenStar, operational 2024–present)**
No electrical output by design. A proof-of-concept physics demonstrator focused on validating the HTS flux pump and achieving levitated plasma confinement. 5.2 m vacuum vessel, 5.6 T REBCO core magnet, <50 kW ECRH heating. Explicitly stated to be a precursor for fusion-relevant experiments in Tahi. Does not qualify as a design point.

**Reactor A — Simpson et al. 2026 (arXiv 2602.20564)**
Net electric power: 208 MWe, computed in Table 9: fusion power 667 MW → thermal 741 MW → total electrical 296 MW → minus cryogenics (−1.31 MW) and auxiliary heating wall power (−63.6 MW) = 208 MWe. Grid-scale plant optimized under a maximum overnight capital cost constraint (baseline = 1.0 relative). Full engineering parameters published: core magnet outer radius 7.1 m, first wall radius 20.6 m, vacuum vessel radius 25.9 m; peak field 23.0 T; magnet stored energy 20.8 GJ; 4,320 km REBCO tape; mass inventory (Table 5); plasma equilibrium (Table 6); neutronics (Table 8); power balance (Table 9). Paper notes: "Reactor A being the larger device allows it to impose lower performance targets on Tahi, implying that a Qsci = 15 Reactor A can be achieved with Bohm-like scaling." Required energy confinement time τ_e = 3.5 s.

**Reactor B — Simpson et al. 2026 (arXiv 2602.20564)**
Net electric power: 74.5 MWe, computed in Table 9: fusion power 237 MW → thermal 264 MW → net 74.5 MWe. Smaller design optimized under a maximum overnight capital cost constraint of 0.5× Reactor A, intended to reduce FOAK capital cost exposure. Same paper, equally complete engineering parameters: core magnet radius 6.1 m, first wall radius 16.9 m, vacuum vessel radius 21.8 m; peak field 21.8 T; 2,550 km REBCO tape. Paper notes Reactor B is "more suited for industrial applications instead of standalone grid power generation" and requires higher Tahi performance (τ_e = 5.9 s required; Bohm-like scaling from LDX is insufficient, unlike for Reactor A).

**Tama Nui (OpenStar aspirational commercial target, ~2035+)**
Bloomberg (2026): "may produce 50 to 200 megawatts of electricity." No published geometry, no published engineering parameters, no named design point within the range. The 50–200 MWe span is a CEO-level aspirational statement, not a design specification. Does not qualify as a design point under the selection rule.

## 3. Selection

Reactor A from Simpson et al. (2026) is selected. It is the most-mature design with the best published quantitative data: the paper provides full geometry, power balance, magnet design, neutronics, and material inventory for a grid-scale commercial plant. Reactor A is the more conservative of the two published designs — it requires lower confinement performance from Tahi to reach Qsci = 15 (Bohm-like scaling from LDX is sufficient), and the paper uses it as the primary comparison point against ARC and ITER. Reactor B's lower capital cost is appealing as a FOAK choice but demands better plasma performance from Tahi and is oriented toward industrial rather than grid applications; it is rejected in favor of the more achievable design for the cost comparison baseline.

```yaml
proposal:
  concept_id: 12-levitated-dipole
  design_name: "OpenStar Reactor A — Simpson et al. 2026 (arXiv 2602.20564)"
  maturity_tier: proposed-commercial
  grounding_confidence: high
  p_native_mwe: 208
  primary_sources:
    - knowledge/concept_research/12-levitated-dipole/iter-01/sources/arxiv-2602-20564-dt-dipole-power-plants.md
    - knowledge/concept_research/12-levitated-dipole/iter-01/sources/arxiv-2508-17691-junior-design-results.md
  selection_rationale: |
    Reactor A (208 MWe net) is the more conservative of the two design points published in
    Simpson et al. (2026): it requires lower confinement performance from the Tahi demonstration
    device (τ_e = 3.5 s, achievable with Bohm-like scaling from LDX) than Reactor B (τ_e = 5.9 s),
    making it the more credible commercial-scale baseline. The paper provides full engineering
    parameters — geometry, magnet design, neutronics, and plant power balance — placing it in the
    same data-quality tier as ARC 2015. Reactor B was rejected because the paper explicitly
    positions it for industrial rather than grid applications and it demands superior plasma
    performance not yet demonstrated. Tama Nui (50–200 MWe) was rejected because no engineering
    design point has been published. The architecture is a single-module plant; P_native is the
    plant output.
  alternatives_considered:
    - design: "OpenStar Reactor B — Simpson et al. 2026 (arXiv 2602.20564), 74.5 MWe"
      reason_rejected: "lower overnight capital cost optimization produces a sub-grid-scale industrial design that requires better Tahi confinement performance than Reactor A"
      sensitivity_implication: "if picked instead, P_native drops substantially (74.5 vs 208 MWe) → more modules required at 1 GWe → 1 GWe LCOE shifts up. Worth probing if Tahi shows only Bohm-like scaling and the FOAK cost advantage of the smaller plant becomes dominant."
    - design: "Tama Nui aspirational commercial target (50–200 MWe range, no engineering design point)"
      reason_rejected: "CEO-level aspirational range with no published geometry or engineering parameters; not an engineered design point"
      sensitivity_implication: "if a Tama Nui design point is eventually published, P_native could fall anywhere in the 50–200 MWe range → sensitivity direction depends on whether the published value lands above or below 208 MWe. Revisit on publication."
    - design: "Junior prototype (OpenStar, 2024–present)"
      reason_rejected: "physics demonstrator with no electrical output by design"
      sensitivity_implication: "n/a — no P_native exists for this design"
```

## 4. Open questions

- **Tama Nui engineering design**: If OpenStar publishes engineering parameters for Tama Nui (the fourth-generation commercial device), revisit the design-point selection. A published Tama Nui with geometry and P_native could displace Reactor A as the primary design point if it represents a more committed commercial target.
- **Tahi performance validation**: The paper's Reactor A viability is predicated on Tahi achieving Bohm-like confinement scaling from LDX. If Tahi results (expected ~2028) fall below the required double products in Figure 22, the Q = 15 assumption for Reactor A breaks down and the design's techno-economic grounding weakens materially — this is the most significant near-term watch-item for this selection.
- **Absolute cost figures withheld**: Simpson et al. deliberately omit absolute overnight capital cost and LCOE values, presenting only relative constraints. If OpenStar publishes their cost model in a future paper, the cost projection for Reactor A can be anchored against the company's own estimate rather than pure analogue-based reconstruction.
- **Thermal conversion cycle unspecified**: No published source identifies whether Reactor A uses a Rankine or sCO₂ Brayton cycle. The paper assumes 40% electrical conversion efficiency as a generic value. Resolution would require a future OpenStar publication covering balance-of-plant, and would not change the design-point selection but would affect downstream cost modeling.

---

The document is ready to save to `exploration/concept_analysis/analyses/12-levitated-dipole/design-points/proposal.md`. A few notes on the key judgment calls:

**Why Reactor A over Reactor B**: The paper's own Discussion section is decisive — Reactor A achieves Qsci = 15 with Bohm-like scaling from LDX, while Reactor B requires better-than-Bohm performance. Both have identical data quality, so the more achievable design wins as the cost comparison baseline.

**Why `proposed-commercial` over `paper-concept`**: Reactor A is a published commercial-scale plant (208 MWe grid power) with documented engineering parameters including detailed geometry, magnet specs, and full power balance. The maturity tier vocabulary distinguishes `proposed-commercial` from `paper-concept` precisely by the presence of "documented engineering parameters" — this design has them at a depth comparable to ARC 2015.

**Why `grounding_confidence: high`**: Tables 5–9 in the paper cover geometry, magnet design, plasma equilibrium, neutronics, and plant power balance. This is an unusually complete disclosure for a company at OpenStar's stage, and the 208 MWe figure traces directly to a computed power balance, not an aspirational estimate.