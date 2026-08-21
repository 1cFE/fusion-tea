# Design Point Reasoning Trace — 29-negative-triangularity-tokamak

## 1. Sources walked

- `knowledge/concept_research/29-negative-triangularity-tokamak/dossier.md` — synthesized concept summary; identifies Firefly Fusion as the named company but flags very early-stage status (founded 2024, minimal public technical detail) and points to MANTA (Rutherford et al. 2024) as the closest published NT reference design
- `knowledge/concept_research/29-negative-triangularity-tokamak/iter-01/sources/greyb-firefly-interview.md` — GreyB / Scouted interview with Firefly CEO Rustem Ospanov; gives R=2–2.5 m, B=10–12 T, Q>5, P_fusion=50–100 MW, P_heat=20–30 MW; no net electric output stated
- `knowledge/concept_research/29-negative-triangularity-tokamak/iter-01/sources/firefly-fusion-diii-d-collaboration.md` — DIII-D collaboration page describing LUCIOLE prototype with copper magnets; LUCIOLE is a sub-scale prototype, not a commercial plant
- `knowledge/concept_research/29-negative-triangularity-tokamak/iter-01/sources/ball-balestri-ohmic-nt-paper.md` — Balestri, Ball, Coda 2024 academic feasibility study of ohmic-only NT operation at compact high-field parameters; no committed plant design or electric output
- `knowledge/concept_research/29-negative-triangularity-tokamak/iter-01/sources/venture-kick-profile.md` — Firefly funding profile; no reactor parameters
- `knowledge/concept_research/29-negative-triangularity-tokamak/iter-01/sources/fusion-energy-base-profile.md` — Firefly company profile; confirms phased magnet strategy (copper → HTS) but no plant-scale design
- `knowledge/concept_research/29-negative-triangularity-tokamak/iter-02/sources/firefly-website-2026.md` — Firefly website (March 2026); team/advisor bios, no technical parameters disclosed
- `knowledge/concept_research/29-negative-triangularity-tokamak/iter-02/sources/manta-reference-design.md` — Rutherford et al. 2024 MANTA paper (MIT PSFC / Columbia / GA collaboration); full integrated NT FPP design with Pfus=450 MW, Pth=530 MW, Pe,net=90 MWe, R0=4.55 m, B0=11 T, REBCO HTS, FLiBe blanket, TBR=1.15, ICRF 40 MW heating, pulsed (~15 min), overnight cost $3.4B
- `knowledge/concept_research/29-negative-triangularity-tokamak/iter-04/sources/arxiv-2401-15217.md` — Guizzo et al. 2024 vertical-stability assessment for NT pilot plants; methods paper, no standalone plant design with P_native
- `knowledge/concept_research/29-negative-triangularity-tokamak/iter-04/sources/arxiv-2405-01514.md` — Schwartz et al. 2024 maintenance strategy / grid value paper; uses fusion plants as economic case studies, not an NT plant design
- `knowledge/concept_research/29-negative-triangularity-tokamak/iter-04/sources/arxiv-2501-14682.md` — Guizzo et al. 2025 small (R0=1 m, B=3 T, Ip=0.75 MA, copper TF) NT controllability test stand; explicitly a pre-conceptual experiment, no electric output by design
- `knowledge/concept_research/29-negative-triangularity-tokamak/iter-04/sources/osti-servlets-purl-1127358.md` and `osti-servlets-purl-1178069.md` — ARIES-ACT power plant studies (Kessel et al.); positive-triangularity reference plants in the corpus for cross-comparison of ARIES-class plant integration but not NT designs
- `knowledge/concept_research/29-negative-triangularity-tokamak/iter-04/sources/qedfusion-lib-report-aries-act-ucsd-cer-13-01.md` — Waganer 2013 ARIES cost-account documentation; cost-methodology source, not an NT design

## 2. Candidates surfaced

**MANTA (Rutherford et al. 2024 — MIT PSFC / Columbia / General Atomics)**
Negative-triangularity ARC-class NASEM-compliant fusion pilot plant. Fully integrated published design with Pfus=450 MW, Pth=530 MW, Pe,net=90 MWe, electricity gain Qe ≈ 2.4, plasma Q=11.5, R0=4.55 m, a=1.2 m, B0=11 T, δ=−0.5, REBCO HTS demountable TF coils, FLiBe immersion blanket (TBR=1.15), ICRF heating at 40 MW / 110 MHz with 3He minority, pulsed (~15 min burns / 2 min inter-pulse), and overnight cost $3.4B. Explicitly framed as a pilot plant (not a commercial plant) meeting NASEM "Bringing Fusion to the U.S. Grid" requirements. Maturity tier: paper-concept (academic / collaboration design study). P_native: 90 MWe.

**Firefly Fusion commercial plant (named company in dossier)**
Founded 2024; compact high-field NT tokamak with R=2–2.5 m, B=10–12 T, HTS magnets at commercial scale, targeting Q>5 with 50–100 MW fusion power and 20–30 MW heating input. The company has not published a commercial-plant electric output. The 50–100 MW figure is fusion power, not net electric, and is given as a target band rather than a committed design point. No internally complete geometry-power-fuel-engineering tuple exists for any one named Firefly unit. P_native: not published.

**LUCIOLE prototype (Firefly's near-term demonstrator)**
Sub-scale prototype with copper actively-cooled magnets, intended for rapid iteration and DIII-D collaboration on NT physics. Explicitly a prototype, not a power plant; no electrical output by design. Disqualifies as a design point per the selection rule.

**Balestri / Ball / Coda 2024 ohmic-only NT feasibility scenario**
Academic study exploring whether compact high-field NT tokamaks could operate with ohmic heating alone (no auxiliary heating). Scenario calculation in a physics paper; no committed plant geometry, no balance-of-plant, no electric output. P_native: not stated.

**Guizzo et al. 2025 NT controllability test stand (arxiv 2501.14682)**
R0=1 m, a=0.27 m, B=3 T, Ip=0.75 MA, 16 copper demountable TF coils. Explicitly a pre-conceptual experiment for testing simulation/control software, not a power plant. No electric output by design.

**ARIES-ACT (Kessel et al. 2014)**
Positive-triangularity ARIES power plant study. Cross-referenced in the corpus for cost methodology and ARIES-class integration but not an NT design; out of scope as a design point for this concept.

## 3. Selection

The MANTA NT fusion pilot plant (Rutherford et al. 2024) is selected as the design point. Firefly Fusion is the named commercial company in the concept dossier, but Firefly has not published a commercial-plant net electric output, geometry-power-fuel tuple, or engineering specification for any internally complete named unit; only fusion-power target bands (50–100 MW Pfus) appear in interviews, and the only Firefly hardware named with parameters is the LUCIOLE sub-scale prototype, which has no electrical output by design. Plant-stitching (e.g., adopting MANTA's electric output with Firefly's geometry, or Firefly's fusion-power band with MANTA's balance of plant) is forbidden under the selection rule. MANTA is the only NT design in the corpus that is internally complete and published — it has a fully self-consistent integrated design with geometry, magnet design, blanket, ICRF heating, balance of plant, and a computed Pe,net of 90 MWe, framed explicitly as a NASEM-compliant fusion pilot plant. Grounding confidence is `high` because the MANTA paper publishes geometry + power + fuel + extensive engineering parameters (magnet design, neutronics, blanket TBR, balance-of-plant, economics) for one named unit; the cost projection has solid published engineering ground under it. The MANTA paper does not present multiple operating phases of the same machine, so there is no per-phase phase-pick to defend. The architecture is a single tokamak unit (not multi-module), so P_native = the full 90 MWe plant output.

```yaml
proposal:
  concept_id: 29-negative-triangularity-tokamak
  design_name: "MANTA NT Fusion Pilot Plant (Rutherford et al. 2024)"
  maturity_tier: paper-concept
  grounding_confidence: high
  p_native_mwe: 90
  primary_sources:
    - knowledge/concept_research/29-negative-triangularity-tokamak/iter-02/sources/manta-reference-design.md
    - knowledge/concept_research/29-negative-triangularity-tokamak/iter-01/sources/greyb-firefly-interview.md
  selection_rationale: |
    MANTA (Rutherford et al. 2024) is selected as the NT-tokamak design point because it is the
    only NT plant in the corpus with a fully self-consistent, internally complete published design:
    Pe,net = 90 MWe (computed via integrated balance-of-plant modeling), Pfus = 450 MW, R0=4.55 m,
    B0=11 T, δ=−0.5, REBCO HTS demountable TF coils, FLiBe immersion blanket (TBR=1.15), and ICRF
    heating. Firefly Fusion — the named NT commercial company in the dossier — has not published
    a commercial-plant net electric output or an internally complete design tuple; its disclosures
    are fusion-power target bands (50–100 MW Pfus) plus a sub-scale prototype (LUCIOLE) with no
    electrical output by design, and adopting MANTA's geometry with Firefly's targets would be
    plant-stitching. MANTA is a single-unit pilot plant (not multi-module), so P_native = 90 MWe
    is the full plant output.
  alternatives_considered:
    - design: "Firefly Fusion commercial NT tokamak (R=2–2.5 m, 50–100 MW Pfus band)"
      reason_rejected: no published net electric power; no internally complete geometry-power-fuel-engineering tuple for a named commercial unit
      sensitivity_implication: >
        If Firefly publishes a commercial-plant design with its own P_native, the design point
        should be revisited. Firefly's compact high-field geometry (R=2–2.5 m, B=10–12 T) is
        substantially smaller than MANTA (R=4.55 m, B=11 T), which would likely imply a lower
        P_native per unit → more modules at 1 GWe → 1 GWe LCOE shifts up. Worth probing when
        Firefly publishes engineering parameters for a commercial plant.
    - design: "LUCIOLE prototype (Firefly near-term demonstrator)"
      reason_rejected: sub-scale prototype with no electrical output by design; explicitly a precursor, not a power plant
      sensitivity_implication: "n/a — LUCIOLE has no P_native by design and cannot be used as a design point."
    - design: "Balestri / Ball / Coda 2024 ohmic-only NT feasibility scenario"
      reason_rejected: academic feasibility study, no committed plant geometry or balance of plant, no stated electric output
      sensitivity_implication: >
        If a follow-on study develops the ohmic-only NT concept into an integrated plant design
        with published net electric power, P_native could shift in either direction (ohmic-only
        eliminates auxiliary heating power but typically implies more compact, lower-fusion-power
        operation). Worth probing if a quantitative ohmic-only NT plant design is published.
    - design: "Guizzo et al. 2025 NT controllability test stand (R0=1 m, B=3 T)"
      reason_rejected: pre-conceptual experiment for control-software validation; no electrical output by design
      sensitivity_implication: "n/a — pre-conceptual experiment with no P_native by design."
    - design: "ARIES-ACT (Kessel et al. 2014)"
      reason_rejected: positive-triangularity ARIES power plant study; not an NT design
      sensitivity_implication: "n/a — wrong concept family (PT, not NT)."
```

## 4. Open questions

- **Firefly commercial-plant disclosure**: If Firefly Fusion publishes engineering parameters for a commercial NT tokamak (geometry + magnet design + balance of plant + Pe,net), the design point should be revisited. Firefly's compact (R=2–2.5 m) target is structurally different from MANTA's (R=4.55 m) and would force re-selection. This is the highest-priority watch item.
- **MANTA → commercial NT plant extrapolation**: MANTA is explicitly a pilot plant, not a commercial unit; the authors note that further optimization is possible for absolute performance. If the MANTA collaboration or a successor team publishes a follow-on commercial-scale NT design that supersedes MANTA in the corpus, the design point should move there.
- **Power-conversion cycle for MANTA**: MANTA's 90 MWe net assumes the balance-of-plant configuration described in the paper (Qe ≈ 2.4). If subsequent analyses publish materially different conversion efficiencies for the MANTA thermal cycle, the 90 MWe figure could shift and the design point P_native should be updated accordingly.
