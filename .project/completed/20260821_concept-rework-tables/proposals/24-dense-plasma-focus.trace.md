# Design Point Reasoning Trace — 24-dense-plasma-focus

## 1. Sources walked

- `knowledge/concept_research/24-dense-plasma-focus/dossier.md` — synthesized dossier; orientation to LPPFusion's Focus Fusion portfolio, key milestones, and what each source covers
- `knowledge/concept_research/24-dense-plasma-focus/iter-01/sources/lerner-2023-jfe-paper.md` — Lerner et al. (2023) J. Fusion Energy 42:7; peer-reviewed overview; contains the authoritative commercial generator concept with the 5 MW figure, repetition rate reasoning, and capital cost estimate
- `knowledge/concept_research/24-dense-plasma-focus/iter-01/sources/lerner-2024-frontiers-pB11-prep.md` — Lerner & Hassan (2024) Frontiers in Physics; FF-2B experimental preparations; describes the current experimental device; no commercial design-point data
- `knowledge/concept_research/24-dense-plasma-focus/iter-02/sources/lppfusion-technology-focus-fusion-energy-dpf-device/output.md` — LPPFusion technology page; operating physics and direct conversion; no new P_native data
- `knowledge/concept_research/24-dense-plasma-focus/iter-02/sources/lppfusion-investing-in-lppfusion-executive-summary/output.md` — LPPFusion investor executive summary; repeats the 5 MW / small-room / mass-producible framing
- `knowledge/concept_research/24-dense-plasma-focus/iter-02/sources/lppfusion-investing-in-lppfusion-our-plan-to-net-energy/output.md` — LPPFusion net energy plan; defines Phase 1 (net energy demo), Phase 2 (5 MW prototype generator), Phase 3 (commercialization) roadmap
- `knowledge/concept_research/24-dense-plasma-focus/iter-02/sources/lppfusion-proton-boron-p11b-fuel-arrives/output.md` — fuel procurement news post; no design-point data

## 2. Candidates surfaced

**FF-2B experimental device (current)**
Active laboratory device: megampere-class DPF, 2.8 cm anode radius, beryllium electrodes, up to 2.7 MA / 115 kJ stored energy. Phase 1 research device. No net electrical output by design — target is 30 kJ net fusion yield per shot as a scientific milestone. Does not qualify.

**Phase 1 net-energy demonstrator (no separate named design)**
The Phase 1 milestone is demonstrating 30 kJ net fusion yield per shot in FF-2B. This is a scientific milestone, not a power generator; the 30 kJ refers to fusion yield, not electrical output. Does not qualify.

**Phase 2 / commercial Focus Fusion generator (5 MWe)**
Described in Lerner et al. 2023 JFE (section "Steps from Net Energy to Commercialization") and corroborated by the company's "Net Energy Plan" and "Executive Summary" pages:
- Net electric: ~25 kJ per pulse × ~200 Hz = 5 MW electric
- Rep rate ~200 Hz limited by electrode cooling (~10 kW/cm² at anode tip, helium cooling)
- Direct conversion: ion beam via decelerator (~2/3 energy), x-rays via multilayer photoelectric device (~1/3)
- No thermal cycle; ~3 tons, ~30 m³, fits in a small room
- Capital cost ~$500,000 ($0.10/W), mass-producible
- Fuel: p-B11 (decaborane), ~5 kg/year per unit

This is the **only** named commercial electrical design in LPPFusion's public portfolio.

## 3. Selection

The Phase 2 / commercial Focus Fusion generator (5 MWe) is selected as the design point — it is the only candidate with a stated net electrical output. The selection rule is uncontested.

```yaml
proposal:
  concept_id: 24-dense-plasma-focus
  design_name: "Focus Fusion commercial generator (Lerner et al. 2023)"
  maturity_tier: paper-concept
  grounding_confidence: low
  p_native_mwe: 5.0
  primary_sources:
    - knowledge/concept_research/24-dense-plasma-focus/iter-01/sources/lerner-2023-jfe-paper.md
    - knowledge/concept_research/24-dense-plasma-focus/iter-02/sources/lppfusion-investing-in-lppfusion-our-plan-to-net-energy/output.md
  selection_rationale: |
    The Focus Fusion commercial generator is the only LPPFusion design with a stated net
    electrical output: ~25 kJ net electrical per pulse at ~200 Hz repetition, yielding 5 MW.
    Both figures are computed in the Lerner 2023 JFE paper from first-principles cooling limits
    and energy balance estimates; no separate engineered architecture document exists.
    The 5 MW unit is described consistently across the peer-reviewed literature and company
    public communications as the Phase 2 prototype and subsequent commercial product.
    No other named commercial design exists in this portfolio. Grounding confidence is
    low because P_native traces to back-of-envelope scaling arguments in a physics paper,
    not to a documented engineering design with committed geometry and validated power balance.
  alternatives_considered:
    - design: "FF-2B experimental device"
      reason_rejected: "physics research device, no net electrical output by design"
      sensitivity_implication: "n/a — not a power generator design"
    - design: "Phase 1 net-energy demonstrator"
      reason_rejected: "scientific milestone device (30 kJ fusion yield target), no electrical output by design"
      sensitivity_implication: "n/a — not a power generator design"
```

## 4. Open questions

- **Engineering parameters for the commercial generator** are absent from all sources — electrode geometry, capacitor bank specs, energy conversion device designs. If LPPFusion publishes these as part of a Phase 2 engineering program, grounding confidence could upgrade and P_native could shift.
- **The 200 Hz repetition rate** is load-bearing for the 5 MW figure. It is derived solely from a cooling limit estimate. If that limit proves optimistic or pessimistic in actual engineering, P_native moves proportionally — no fixed committed geometry anchors it independently.
- **The 25 kJ net electrical per pulse** depends on conversion efficiency claims (~80–85% beam decelerator, ~80% x-ray photoelectric), neither of which has been demonstrated at scale. If conversion efficiency is lower, P_native falls below 5 MW at 200 Hz.
- **No independent engineering review** of the 5 MW design appears in the literature. The x-ray photoelectric conversion device has never been built; this is the highest-risk component in the power balance.
- **LPPFusion has not yet demonstrated net fusion energy** (Phase 1 milestone, FF-2B still in R&D). The Phase 2 generator concept will almost certainly be revised substantially once Phase 1 experimental data is available.

---

**Key call**: `p_native_mwe: 5.0`, `grounding_confidence: low`, `maturity_tier: paper-concept`. The 5 MW is the only published P_native anywhere in the LPPFusion portfolio, but it is a back-of-envelope projection from cooling limit + conversion efficiency estimates in a physics paper, not a documented engineering design. The `low` grounding flag is the honest label, and the open questions section flags exactly what would change this call.

Approve the write to save this to `exploration/concept_analysis/analyses/24-dense-plasma-focus/design-points/baseline.md`?