# Design Point Reasoning Trace — 03-laser-icf-liquid-jet-target

## 1. Sources walked

- `knowledge/concept_research/03-laser-icf-liquid-jet-target/dossier.md` — synthesized concept summary; oriented source selection; flagged absence of experimental results, energy capture architecture, and any named reactor design; confirmed overall confidence as "low"
- `knowledge/concept_research/03-laser-icf-liquid-jet-target/iter-01/sources/arxiv-2503-nanoshell-paper.md` — Kharzeev, Levitt, Trallero-Herrero 2025 (arXiv:2503.15531), "Fusion in a Nanoshell"; co-authored by Jacob Levitt of Cortex Fusion Systems; the primary technical reference; provides the reactor scenario projection including P_fusion ~ 1 MW, Q ~ 100, κ ~ 30%, and D-D fuel
- `knowledge/concept_research/03-laser-icf-liquid-jet-target/iter-01/sources/cortex-fusion-website.md` — Cortex Fusion Systems website (accessed March 2026); lists eleven patent applications by title and number; confirms D2O liquid-jet delivery mechanism and femtosecond laser approach; no electrical power numbers stated
- `knowledge/concept_research/03-laser-icf-liquid-jet-target/iter-01/sources/arxiv-2308-levitt-quantum-control.md` — Levitt 2023 (arXiv:2308.07417); describes an entirely different mechanism — laser-assisted ¹⁶O(2p,γ)¹⁸Ne radiative capture in ordinary water via quantum anti-Zeno effect; no D-D fusion, no nanoshells, no plasma; assessed as a distinct concept, not a design variant for this concept
- `knowledge/concept_research/03-laser-icf-liquid-jet-target/iter-01/sources/kHz-liquid-sheet-fusion-paper.md` — Knight et al. 2024 (HPLSE, Cambridge); independent experiment demonstrating ~10^5 D-D neutrons/second from a 1 kHz laser on thin D2O sheets; no Cortex affiliation, no electrical output by design

## 2. Candidates surfaced

**Candidate A: Nano-Sun 1 MHz reactor scenario (arXiv:2503.15531)**

The "Released energy" section projects: at f = 1 MHz with 10^6 nanoshells/pulse, P_fusion ~ 1 MW (eq. 14). With κ ≈ 30% and P_laser = 3 kW, Q ~ 100 (eq. 16). Net electrical output ≈ 0.30 MWe. Fuel: D-D (liquid D2O). The paper calls this the "potentially practical fusion reactor" scenario and acknowledges "many practical challenges exist." No named plant, no geometry, no chamber design, no engineering parameters. The plasmonic fusion physics is unvalidated and unreviewed.

**Candidate B: Modern Small Modular Hybrid Fusion-Fission Reactor (US patent application 63/792,117)**

Listed by title on the Cortex website. Patent text not available in research materials. P_native cannot be established from the title alone.

**Candidate C: D2O-Moderated Hybrid Fusion-Fission Reactor with Direct Brayton Cycle (US patent application 63/802,958)**

Listed by title on the Cortex website. More specific engineering concept implied by title (Brayton cycle). Patent text not available. P_native cannot be established.

**Candidate D: Levitt 2023 quantum-Zeno ¹⁶O(2p,γ)¹⁸Ne water fusion reactor (arXiv:2308.07417)**

Entirely different mechanism — laser-controlled nuclear tunneling in ordinary water. Section 3 discusses break-even conditions requiring ~10^12 fusion events per laser pulse but states no MWe output. A different concept from the D-D nanoshell design, not an alternative design point for it.

**Candidate E: kHz liquid-sheet neutron source (Knight et al., HPLSE 2024)**

Tabletop neutron source by an independent group. No Cortex affiliation. No electrical output by design.

## 3. Selection

Candidates B and C cannot be evaluated (patent text unavailable). Candidates D and E are disqualified: D has no stated MWe output and is a different mechanism; E is not a Cortex design and produces no electricity.

Candidate A is the only source in the Cortex portfolio with an implied electrical output figure traceable to a Cortex company paper. The 0.30 MWe figure derives from a back-of-envelope feasibility scenario in an unreviewed preprint with unvalidated physics and placeholder efficiencies. The freeform route is not taken because the selection rule requires literally no electrical output figure of any kind, and the nanoshell paper does project one in a company-attributed source.

```yaml
proposal:
  concept_id: 03-laser-icf-liquid-jet-target
  design_name: "Nano-Sun 1 MHz reactor scenario (Kharzeev, Levitt, Trallero-Herrero 2025, arXiv:2503.15531)"
  maturity_tier: paper-concept
  grounding_confidence: low
  p_native_mwe: 0.30
  primary_sources:
    - knowledge/concept_research/03-laser-icf-liquid-jet-target/iter-01/sources/arxiv-2503-nanoshell-paper.md
    - knowledge/concept_research/03-laser-icf-liquid-jet-target/iter-01/sources/cortex-fusion-website.md
  selection_rationale: |
    The nanoshell preprint (arXiv:2503.15531), co-authored by Cortex founder Jacob Levitt, is the only
    Cortex-attributed source with an implied electrical output. Its "Released energy" section projects
    P_fusion ~ 1 MW at f = 1 MHz and N_s-p = 10^6 nanoshells/pulse. With the paper's stated electrical
    conversion efficiency κ ~ 30% and laser power consumption 3 kW, net electrical output is approximately
    0.30 MWe (Q ~ 100). No named reactor design exists anywhere in the Cortex public record; this number
    is a back-of-envelope scenario calculation in a theoretical preprint whose core physics (plasmonic
    field enhancement producing fusion) is unvalidated and unreviewed. Two hybrid fusion-fission SMR
    patent applications (US 63/792,117, US 63/802,958) listed on the company website may describe more
    mature and higher-output designs, but their content is not available in the current research materials.
  alternatives_considered:
    - design: "Modern Small Modular Hybrid Fusion-Fission Reactor (US patent application 63/792,117)"
      reason_rejected: "Patent text not available in research materials; P_native cannot be established from title alone"
      sensitivity_implication: >
        If the patent describes an SMR-scale design, P_native could rise substantially — SMR-class outputs
        in the 50–300 MWe range are typical for this technology class → far fewer modules at 1 GWe → 1 GWe
        LCOE shifts down materially. Ingesting this patent would likely force a re-selection and change the
        comparison number by 2–3 orders of magnitude.
    - design: "D2O-Moderated Hybrid Fusion-Fission Reactor with Direct Brayton Cycle (US patent application 63/802,958)"
      reason_rejected: "Patent text not available in research materials; P_native cannot be established from title alone"
      sensitivity_implication: >
        Same direction as US 63/792,117 — if P_native is at SMR scale (50–300 MWe), the 1 GWe LCOE shifts
        down substantially. The Brayton cycle specification suggests a more complete engineering concept;
        if distinct design parameters appear in this patent, it may supersede US 63/792,117 as the
        preferred design point.
    - design: "Levitt 2023 quantum-Zeno ¹⁶O(2p,γ)¹⁸Ne water fusion reactor (arXiv:2308.07417)"
      reason_rejected: "Entirely different fusion mechanism from D-D nanoshell concept; no stated P_native in MWe"
      sensitivity_implication: >
        Not a directly comparable alternative — represents a different concept row, not a different power
        level of the same design. No directional sensitivity for the D-D nanoshell design point.
    - design: "kHz liquid-sheet neutron source demonstrator (Knight et al., HPLSE 2024)"
      reason_rejected: "Independent academic experiment with no Cortex affiliation; neutron source with no electrical output"
      sensitivity_implication: "n/a — not a power plant design and not a Cortex concept."
```

## 4. Open questions

- **Hybrid Fusion-Fission SMR patent content (US 63/792,117 and US 63/802,958)**: These patent applications likely contain the most engineering-complete designs Cortex has produced. If either states an electrical output and reactor parameters, the design point should be replaced: a 50–300 MWe SMR-scale design would cut module count at 1 GWe by 2–3 orders of magnitude relative to the 0.30 MWe selection and make the comparison number meaningful.

- **Validation of plasmonic fusion mechanism**: The 0.30 MWe figure rests entirely on an unvalidated cross-section enhancement. Kharzeev et al. acknowledge that the fusion mean free path exceeds the nanoshell radius and that ionization damping is unquantified. If independent experiments fail to reproduce significant fusion enhancement from irradiated gold nanoshells, the concept has no viable design point and the row should route to freeform.

- **Repetition rate achievability**: The scenario requires 1 MHz laser repetition. Commercial femtosecond lasers currently reach hundreds of kHz; at 1 kHz operation P_fusion drops by ~1000× to below 1 kWe. Whether 1 MHz at the required intensity is achievable with commercially available sources is unresolved in the paper.

- **Energy capture architecture**: κ = 30% is a placeholder with no grounding in a disclosed blanket or energy recovery design. Any disclosed energy capture architecture could shift P_native up or down depending on actual conversion efficiency.

---

**Summary of the call**: The concept routes to a `grounding_confidence: low` selection rather than freeform because the nanoshell preprint (a Cortex company paper) contains a calculable implied electrical output (~0.30 MWe). The number is an asterisked placeholder — back-of-envelope scenario physics, unreviewed, unvalidated — and the most consequential watch item is whether either of the two hybrid fusion-fission SMR patent applications contains an actual engineered design point that would force a re-selection.