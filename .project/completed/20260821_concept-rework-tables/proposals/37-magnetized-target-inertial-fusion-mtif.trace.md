# Design Point Reasoning Trace — 37-magnetized-target-inertial-fusion-mtif

## 1. Sources walked

- `knowledge/concept_research/37-magnetized-target-inertial-fusion-mtif/dossier.md` — synthesized column-by-column assessment; confirmed overall concept parameters and flagged absence of any net electrical output or design-point power
- `knowledge/concept_research/37-magnetized-target-inertial-fusion-mtif/iter-01/sources/nearstar-website-summary.md` — NearStar corporate site extraction; provided driver parameters (50 g capsule, 10 km/s, >1 MJ, 1 Hz), fuel (D-D), first wall (molten Pb), and roadmap (~5 yr to break-even, ~10 yr to prototype power plant); no electrical output figure
- `knowledge/concept_research/37-magnetized-target-inertial-fusion-mtif/iter-01/sources/nearstar-mtif-technical-overview.md` — secondary extraction of NearStar public materials (learn-more page + Fusion Energy Base profile); the only source to name an electrical figure: "Stated scalability: 50 MW to 1 GW+"; explicitly notes "No published energy gain, net power, capital cost, or LCOE figures in public materials"
- `knowledge/concept_research/37-magnetized-target-inertial-fusion-mtif/iter-02/sources/nearstar-energy-capture-research.md` — iter-02 targeted pull on energy capture; confirmed coal-plant retrofit strategy (steam Rankine); no additional electrical output figures
- `knowledge/concept_research/37-magnetized-target-inertial-fusion-mtif/iter-02/sources/nationalacademies-read-18289-chapter-5/output.md` — National Academies IFE technology chapter; provides IFE target fabrication benchmarks ($0.25–$0.30/target floor) used in analysis.md but contains no NearStar-specific design point
- `knowledge/concept_research/37-magnetized-target-inertial-fusion-mtif/iter-02/sources/iopscience-10-1088-1741-4326-ac2dbe/output.md` — extraction failed (bot-wall at IOP); no content recovered
- `exploration/concept_analysis/analyses/37-magnetized-target-inertial-fusion-mtif/analysis.md` — existing D1+ analysis; read for source inventory and cross-reference; explicitly confirms "Net electrical output: [unknown] | No data in available sources" — not used as a primary source

## 2. Candidates surfaced

**NearStar MTIF lower-end scale, 50 MWe**
— Source: `iter-01/sources/nearstar-mtif-technical-overview.md`, "Stated scalability: 50 MW to 1 GW+". This is the lower bound of the company's stated scalability range for the MTIF concept. It is a marketing claim, not an engineering design point: no named plant, no published geometry, no power conversion efficiency, no capital cost estimate, no simulation output, and no gain target supporting the figure. The company has no published whitepaper, preprint, or conference paper; the only technical disclosure is its corporate website. Maturity: pre-break-even-experiment stage (company roadmap: "break-even experiments ~5 years, prototype power plant ~10 years"). Does not qualify as `proposed-commercial` or `pilot-demonstrator`; closest to `paper-concept`, though even that tier normally implies a journal article or whitepaper exists. Electrical output implied: 50 MWe.

**NearStar MTIF upper-end scale, 1 GW+**
— Same source, same scalability claim. The upper bound of the same company marketing range. No engineering basis distinguishable from the lower bound — both are aspirational scalability assertions. Electrical output implied: nominally ≥1,000 MWe, but this is a round aspirational ceiling, not a design specification.

**No other named designs exist.** NearStar has not published a separate pilot plant design, a commercial plant design, or any phase-differentiated operating scenario. The entire published design space is captured by the single scalability claim above.

## 3. Selection

The selection rule requires picking the most-mature design with the best published quantitative data. Neither end of the scalability range constitutes an engineered design point, but the 50 MWe lower bound is the more conservative and more near-term-plausible figure, and 50 MWe is the smallest unit that could plausibly represent a "first-of-kind" commercial-scale design rather than a round maximum aspiration. The rule specifies that any electrical figure traceable to a company source should be used rather than routing to freeform; the 50 MWe figure from `nearstar-mtif-technical-overview.md` satisfies that test. Grounding confidence is `low`: the figure traces to a marketing scalability claim with no supporting geometry, gain target, efficiency, or engineering parameters of any kind.

```yaml
proposal:
  concept_id: 37-magnetized-target-inertial-fusion-mtif
  design_name: "NearStar MTIF concept — lower bound of company-stated 50 MW–1 GW+ scalability range"
  maturity_tier: paper-concept
  grounding_confidence: low
  p_native_mwe: 50
  primary_sources:
    - knowledge/concept_research/37-magnetized-target-inertial-fusion-mtif/iter-01/sources/nearstar-mtif-technical-overview.md
    - knowledge/concept_research/37-magnetized-target-inertial-fusion-mtif/iter-01/sources/nearstar-website-summary.md
  selection_rationale: |
    The only electrical output figure in the entire source base is a single
    company-stated scalability range of "50 MW to 1 GW+" from the NearStar
    technical overview page. There is no named plant design, no published
    whitepaper, no engineering parameters, no gain target, and no net power
    estimate for any specific design. The 50 MWe lower bound is selected as the
    design point because it is the most conservative and nearest-term figure in
    the range; the 1 GW+ ceiling is a round aspirational maximum with no
    additional grounding. Grounding confidence is low: this P_native is a
    marketing scalability assertion, not an engineering design output — the
    company explicitly has no published net power, gain, or capital cost
    figures. This row exists to keep MTIF in the comparison with a full
    asterisk; the 1 GWe LCOE projection derived from it has no physics or
    engineering anchor and should be treated as a placeholder.
  alternatives_considered:
    - design: "NearStar MTIF upper-end scale (1 GW+ ceiling of same scalability claim)"
      reason_rejected: "aspirational ceiling of a marketing range; no additional grounding over the 50 MW lower bound and less likely to represent a near-term design target"
      sensitivity_implication: "If picked instead, P_native rises by a factor of ~20 → n_mod at 1 GWe collapses toward 1 → 1 GWe LCOE shifts dramatically down, but the figure would be even less grounded than the 50 MWe selection and represents a maximum aspiration rather than any design. Not worth probing until NearStar publishes a specific commercial plant specification."
```

## 4. Open questions

- **The only blocking question is whether NearStar publishes any engineering design point at all.** If a whitepaper, DOE program disclosure, ARPA-E milestone filing, or conference abstract appears naming a specific plant P_native with associated gain target or thermal efficiency, the 50 MWe placeholder should be replaced immediately — it has no intrinsic validity.
- **The scalability claim's basis is unknown.** "50 MW to 1 GW+" may reflect a per-shot yield assumption × rep rate, a coal-plant retrofit sizing constraint, or simply a marketing range. If NearStar discloses the energy balance derivation underlying this range, the lower bound may shift substantially in either direction.
- **Break-even milestone.** NearStar's own roadmap places break-even experiments ~5 years out (from 2026). If break-even is demonstrated at any gain, a back-calculation of implied P_native for a 1 Hz plant becomes feasible and would upgrade the grounding confidence from low to medium. Watch for: APS-DPP abstract submissions from UAH/Texas A&M HVIL collaborators, or a DOE Milestone-Based Fusion Development Program application.
- **D-D ignition feasibility.** If any independent simulation or experimental result establishes whether magnetized D-D compression to ignition conditions is physically achievable at this driver energy, the entire design-point framing may need revision — a negative result would make any P_native moot; a positive result with a gain estimate would provide the first physics anchor for the comparison.