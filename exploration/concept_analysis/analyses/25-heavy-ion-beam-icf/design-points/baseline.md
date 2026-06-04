# Design Point Reasoning Trace — 25-heavy-ion-beam-icf

## 1. Sources walked

- `knowledge/concept_research/25-heavy-ion-beam-icf/dossier.md` — synthesized two-iteration summary; identified HYLIFE-II and HIBALL as the two published HIF power plant designs, confirmed no current commercial developer, pointed to key source files
- `knowledge/concept_research/25-heavy-ion-beam-icf/iter-01/sources/hif-technology-overview.md` — compiled technical overview from iter-01 research; contains the quantitative parameters for both HIBALL (3.8 GWe, KfK-3202) and HYLIFE-II (940 MWe baseline, citing OSTI 7021072), driver specifications, blanket types, cost estimates
- `knowledge/concept_research/25-heavy-ion-beam-icf/iter-01/sources/intensity-energy-search-results.md` — documentation of the failed company verification; confirms "Intensity Energy" does not exist as a fusion company
- `knowledge/concept_research/25-heavy-ion-beam-icf/iter-02/sources/hif-recent-research-compilation.md` — iter-02 web research compilation; confirms HYLIFE-II 6–8 Hz rep rate, HIBALL 5 Hz per chamber, multi-unit HYLIFE-II scaling study (OSTI 10170594) reaching ~1,934 MWe across multiple chambers sharing one driver, and absence of any new commercial developers
- `knowledge/concept_research/25-heavy-ion-beam-icf/iter-02/sources/arxiv-1511-06508.md` — arxiv abstract page only; confirms HIF driver efficiency ~30–40% and ~1 GWe electricity as target, but no power-plant design data beyond what the overview already contains
- `knowledge/concept_research/25-heavy-ion-beam-icf/iter-02/sources/osti-servlets-purl-901970.md` — OSTI 901970, the Z-IFE (Z-pinch) power plant report; not a HIF source and not cited further
- `knowledge/concept_research/25-heavy-ion-beam-icf/iter-02/sources/transat-h2020-wp-content-uploads-2019-11-giegerich.md` — KIT lithium-6 supply paper; discusses blanket lithium enrichment requirements generally, not HIF-specific plant design, not cited further

## 2. Candidates surfaced

**HYLIFE-II baseline single-chamber design (LLNL, early 1990s; OSTI 7021072)**
- P_native: 940 MWe
- Driver: 5 MJ recirculating induction accelerator (~$570M direct cost estimate)
- Blanket: FLiBe thick liquid jets (combined breeding + shielding + first-wall protection)
- Rep rate: 6 Hz; target gain: ~70 (350 MJ yield from 5 MJ input)
- Published LCOE: 6.5 c/kWh baseline (early-1990s dollars)
- Maturity: full national lab power plant conceptual design study with economic analysis
- Data quality: detailed engineering parameters, cost estimate, blanket design

**HYLIFE-II multi-chamber scaled study (OSTI 10170594)**
- Multiple target chambers sharing a single recirculating induction accelerator driver
- Plant total: ~1,934 MWe across multiple chambers
- Per-chamber electric output: still ~940 MWe (same chamber, driver replicated to share fixed costs)
- Also evaluated MHD+Steam hybrid energy conversion
- This is a scaling/economics study layered on top of the baseline design, not an independent plant design with different engineering parameters

**HIBALL (KfK-3202, Germany/US, 1985)**
- P_native: 3,800 MWe plant total
- Driver: 10 GeV Bi²⁺ linear induction accelerator (~3 km), 4 chambers at 5 Hz each (20 Hz system rate)
- Blanket: LiPb, TBR ~1.195
- Per-chamber breakdown is not explicitly stated as a standalone design; only the multi-chamber plant total of 3.8 GWe is documented
- Maturity: full conceptual power plant study, but older (1985) and substantially larger scale
- Data quality: published but less detailed economic analysis than HYLIFE-II; 40 years old

## 3. Selection

HYLIFE-II at the 940 MWe baseline single-chamber design is the selection. It is the more recently published, more economically detailed design. The baseline represents a complete, integrated plant (one accelerator driver + one target chamber + FLiBe blanket + steam Rankine cycle) and is the natural replication unit for the 1 GWe comparison.

HIBALL's plant total (3.8 GWe) makes it ill-suited as a P_native: `n_mod = 1000/3800 < 1`, implying the 1 GWe plant could not even field one HIBALL unit. A per-chamber breakout of HIBALL is not explicitly documented as a standalone design in the source files, so using it would require inferring an unlisted value. HYLIFE-II is unambiguous.

The multi-chamber HYLIFE-II scaling study (OSTI 10170594) adds chambers to reach ~1,934 MWe but does not redefine the per-chamber engineering. The natural module — driver + chamber — remains 940 MWe; the scaling study varies the number of modules.

```yaml
proposal:
  concept_id: 25-heavy-ion-beam-icf
  design_name: "HYLIFE-II baseline single-chamber design (LLNL, OSTI 7021072)"
  maturity_tier: proposed-commercial
  grounding_confidence: high
  p_native_mwe: 940
  primary_sources:
    - knowledge/concept_research/25-heavy-ion-beam-icf/iter-01/sources/hif-technology-overview.md
    - knowledge/concept_research/25-heavy-ion-beam-icf/iter-02/sources/hif-recent-research-compilation.md
  selection_rationale: |
    HYLIFE-II is the most completely documented HIF power plant design in the public literature,
    with published engineering parameters (5 MJ driver, FLiBe blanket, 6 Hz rep rate), a direct
    cost estimate for the accelerator driver ($570M), and an LCOE estimate of 6.5 c/kWh (early-1990s
    dollars) in the LLNL final report (OSTI 7021072). The baseline single-chamber design at 940 MWe
    represents a complete, self-contained plant (recirculating induction driver + one target chamber
    + FLiBe blanket + steam Rankine cycle) and is the natural replication unit. HIBALL was rejected
    because its documented output is a 3.8 GWe multi-chamber plant total, which is inoperable as a
    P_native for the 1 GWe normalization (n_mod < 1), and no standalone per-chamber design was
    documented separately.
  alternatives_considered:
    - design: "HIBALL plant (KfK-3202, 1985) — 3.8 GWe multi-chamber total"
      reason_rejected: plant total is far above 1 GWe normalization point; no standalone per-chamber design documented; older design (1985) with less detailed economics than HYLIFE-II
      sensitivity_implication: "if a future search finds an explicit single-chamber HIBALL design point (~950 MWe estimated from 4-chamber total), P_native would be comparable to HYLIFE-II → modest effect on n_mod, but blanket choice changes from FLiBe to LiPb → cost structure shift worth probing if HIBALL per-chamber design is recovered"
    - design: "HYLIFE-II multi-chamber scaling study (OSTI 10170594) — ~1,934 MWe plant total"
      reason_rejected: not a standalone design; the multi-chamber study layers economics on the same 940 MWe chamber — treating the plant total as P_native would inflate the module size beyond what the underlying engineering describes
      sensitivity_implication: "if the multi-chamber plant total (1,934 MWe) were mistakenly used as P_native, n_mod at 1 GWe drops below 1 — the 1 GWe normalization cannot be reached with a single unit; this variant is relevant only for fleet-level cost learning studies, not the 1 GWe LCOE comparison"
```

## 4. Open questions

- **OSTI 7021072 not extracted directly**: The HYLIFE-II final report (OSTI 7021072) is cited in the compiled `hif-technology-overview.md` but was not extracted as a standalone source file in this repo. If extraction reveals a different net electric output than the 940 MWe figure (e.g., a gross/net distinction, or a later revised edition), the design point would need to be updated.
- **HIBALL per-chamber breakdown**: KfK-3202 describes a 4-chamber plant totaling 3.8 GWe. If the original report documents individual chamber output, that value might constitute a distinct candidate closer to 950 MWe. Recovering it would not displace HYLIFE-II (which has better economics documentation) but would confirm or refute the directional sensitivity noted for HIBALL above.
- **Post-1990s HIF power plant studies**: No post-2000 engineering-level HIF power plant design was found in two research iterations. If a more recent national lab study (e.g., an updated HYLIFE-II with modern materials or sCO₂ conversion) emerges, it would immediately supersede the 1990s baseline and could shift P_native, blanket type, and cost structure.
- **"Intensity Energy" company**: If at any point this company is identified as a real entity with a published design, re-evaluate whether it has a named plant with a documented P_native that should displace the national-lab HYLIFE-II baseline as the design point.