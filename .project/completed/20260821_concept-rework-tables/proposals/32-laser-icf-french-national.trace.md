# Design Point Reasoning Trace — 32-laser-icf-french-national

## 1. Sources walked

- `knowledge/concept_research/32-laser-icf-french-national/dossier.md` — synthesized concept summary; used for orientation and to identify which sources carry quantitative data
- `knowledge/concept_research/32-laser-icf-french-national/iter-01/sources/genf-website-technology.md` — GenF technology page; states "designed to deliver 1GW of power" for the 2050s commercial reactor; confirms 10 Hz target injection
- `knowledge/concept_research/32-laser-icf-french-national/iter-01/sources/genf-icf-article.md` — GenF ICF article (Besaucèle, *Photoniques* 2024); explains direct-drive rationale and the power-plant block diagram; no independent P_native number
- `knowledge/concept_research/32-laser-icf-french-national/iter-01/sources/aip-advances-ribeyre-2025.md` — Ribeyre et al. (2025) *AIP Advances* 15, 095013; co-authored by GenF employees; builds a parametric reactor model for a 1 GWe direct-drive plant; provides assumed efficiencies, operating parameters, and derived chamber size
- `knowledge/concept_research/32-laser-icf-french-national/iter-01/sources/taranis-project-details.md` — CNRS TARANIS project announcement; describes the three-phase development timeline (Phase 1 2024–2027, Phase 2 2028–2035, demonstrator first megawatts 2040, commercial 2050); no P_native for the demonstrator
- `knowledge/concept_research/32-laser-icf-french-national/iter-01/sources/genf-news-timeline.md` — GenF news page; confirms 550-shot experimental campaign at ELI Beamlines (August 2025); no new P_native data
- `knowledge/concept_research/32-laser-icf-french-national/iter-01/sources/arpa-e-sites-default-files-migrated-a05-zuegel.md` — Zuegel ARPA-E 2023 presentation on DPSSL drivers for IFE; background on laser driver requirements for IFE; no GenF-specific design-point data
- `knowledge/concept_research/32-laser-icf-french-national/iter-01/sources/osti-servlets-purl-1833260.md` — Scott et al. 2021 (LA-UR-21-22970), shock ignition LPI paper with Casner (CELIA/CEA); plasma physics background; no GenF commercial plant data
- `knowledge/concept_research/32-laser-icf-french-national/iter-01/sources/power-technology-features-enriched-lithium-and-the-race-for.md` — lithium enrichment trade article; mentions GenF in passing; no P_native data
- `knowledge/concept_research/32-laser-icf-french-national/iter-01/sources/neimagazine-analysis-enriched-lithium-and-advanced-nuclear.md` — NEI Magazine on Assystem/TARANIS partnership; organizational context only; no P_native data

## 2. Candidates surfaced

**Candidate A — GenF 2050 commercial plant (TARANIS end-state)**
- Stated P_native: 1 GW of power — the GenF technology page reads "The commercial reactor will enter service in the 2050's, design to deliver 1GW of power." The Ribeyre et al. (2025) paper, co-authored by GenF employees (Besaucèle and Chesneau), explicitly builds its reactor model around "Pe,grid = 1 GWe" as the reference output and uses this to constrain target gain and driver energy. The paper models a single-chamber design (not multi-module) with a reference operating point: Ed = 3 MJ laser driver, G ≈ 120, rr = 10 Hz, ηd = 7–10%, ηth = 40%, chamber radius ~8 m. This is a single-module architecture; the GenF website and Ribeyre paper describe one reactor chamber, not a fleet of smaller modules.
- Maturity status: paper-concept — GenF is in Phase 1 (modeling and simulation) through 2027. No committed engineering architecture or hardware exists for the commercial plant. The "1 GW" figure is a stated long-term target confirmed in a parametric reactor model paper.
- What's published: power output (1 GWe), fuel (DT direct-drive), repetition rate (10 Hz), driver energy reference (3 MJ), chamber radius estimate (~8 m derived from x-ray fluence constraint), assumed laser driver efficiency (~7–10% DPSSL), thermal conversion efficiency (~40%), target gain (~120). No chamber geometry with engineering tolerances, blanket engineering design, structural specification, or laser hardware architecture.

**Candidate B — TARANIS demonstrator (2040 first-megawatts unit)**
- Stated P_native: none. The CNRS TARANIS announcement says the demonstrator "devrait produire ses premiers mégawatts en 2040" ("first megawatts in 2040"). "Premiers mégawatts" is a qualitative milestone, not a specific electrical output. No source assigns a number to this machine.
- Maturity status: not yet defined — the demonstrator is a planned Phase 3 output, with no published specifications. It is described as a sub-commercial scale proof-of-energy unit, but no P_native has been committed publicly.
- What's published: existence of a planned demonstrator at a future dedicated installation; first output in 2040; no further details.

## 3. Selection

Candidate A (the GenF 2050 commercial plant at 1 GWe) is the only candidate with a stated P_native in any source. Candidate B (the TARANIS demonstrator) has no specific P_native anywhere in the source tree — "premiers mégawatts" is a directional milestone, not a design-point number. By the selection rule, if any number traces to a company source or company-cited paper, it qualifies at `grounding_confidence: low`. Here, 1 GWe traces to both the GenF technology page and to a peer-reviewed reactor model paper co-authored by GenF employees. The Ribeyre et al. (2025) paper is explicitly a parametric systems analysis with placeholder efficiencies ("ηd = 10% seems realistic," "ηth = 40% seems a reasonable value") rather than a committed engineering design. No named plant with a completed engineering architecture exists at this stage — GenF has not exited Phase 1. Accordingly, `grounding_confidence: low` is the honest assessment: the number is traceable but the design point has no committed geometry or engineering architecture beneath it.

```yaml
proposal:
  concept_id: 32-laser-icf-french-national
  design_name: "GenF TARANIS commercial reactor, 2050 target (GenF website / Ribeyre et al. 2025)"
  maturity_tier: paper-concept
  grounding_confidence: low
  p_native_mwe: 1000
  primary_sources:
    - knowledge/concept_research/32-laser-icf-french-national/iter-01/sources/genf-website-technology.md
    - knowledge/concept_research/32-laser-icf-french-national/iter-01/sources/aip-advances-ribeyre-2025.md
  selection_rationale: |
    The GenF 2050 commercial plant is the only design in the portfolio with a stated P_native:
    the technology page commits to "1GW of power" for a single-chamber commercial reactor entering
    service in the 2050s, and Ribeyre et al. (2025), co-authored by GenF employees, explicitly
    builds its reactor systems model around Pe,grid = 1 GWe as the reference output. The design
    is a single-module architecture (one reaction chamber at 10 Hz, not a fleet of smaller units),
    so P_native is the full plant output at 1000 MWe. The TARANIS Phase 3 demonstrator is the
    only other candidate but has no published P_native — "premiers mégawatts" in 2040 is a
    milestone description, not a design-point number.
  alternatives_considered:
    - design: "TARANIS demonstrator, 2040 (first-megawatts unit)"
      reason_rejected: no specific P_native published; "premiers mégawatts" is a qualitative
        milestone with no committed electrical output
      sensitivity_implication: >
        If a P_native were later published for the demonstrator (likely in the range of
        tens to low hundreds of MWe), it would be substantially lower than 1000 MWe →
        more modules at 1 GWe → 1 GWe LCOE shifts up relative to the commercial-plant
        selection. Worth revisiting when GenF publishes demonstrator specifications (expected
        post-2027 after Phase 1 completes).
```

## 4. Open questions

- **1 GW — electric or thermal?** The GenF technology page says "1GW of power" without specifying electrical vs. thermal. The Ribeyre et al. paper uses Pe,grid = 1 GWe as the reference, treating this as net electrical output to the grid. If the website means 1 GWth, the actual P_native would be ~400 MWe (assuming ηth ≈ 40%), which would double n_mod and substantially shift the 1 GWe LCOE upward. This ambiguity would force a re-selection of the P_native value if resolved as thermal rather than electric.
- **Demonstrator P_native post-Phase 1:** The CNRS announcement states Phase 1 concludes with a digital twin by 2027–2028, after which demonstrator design begins. If GenF publishes the demonstrator's rated electrical output (expected between 2027 and 2035), the demonstrator may become the better-grounded design point for comparison purposes, and the 2050 commercial target should be revisited in favor of the demonstrator.
- **Commercial plant architecture refinement:** Ribeyre et al. derive a chamber radius of ~8 m from an x-ray fluence constraint, but this is a single-parameter estimate from an idealized model. If GenF publishes an updated chamber architecture (multi-beam geometry, blanket configuration) post-Phase 1, the design point's grounding would upgrade from `low` to at least `medium` and the derived parameters should be updated.
- **Driver energy and gain at operating point:** The paper presents Ed = 3 MJ and G ≈ 120 as a reference, not a committed design. If GenF converges on a different operating point (e.g., shock ignition at Ed ≈ 1.5 MJ or 2 ω operation) the engineering gain assumptions feeding capital cost would change. This doesn't change P_native but affects cost model completeness.