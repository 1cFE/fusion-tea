# Design Point Reasoning Trace — 18-p-b11-frc

## 1. Sources walked

- `knowledge/concept_research/18-p-b11-frc/dossier.md` — Synthesized taxonomy summary; confirmed Da Vinci at 50 MWe initial and 350–500 MWe at scale, energy conversion (thermal/steam), magnet type (resistive copper inferred), timeline, and funding history.
- `knowledge/concept_research/18-p-b11-frc/iter-02/sources/tae-djt-merger-davinci-specs.md` — ANS Nuclear Newswire article on the Trump Media / TAE merger (Dec 2025); the authoritative published source for the 50 MWe construction commitment and project timeline.
- `knowledge/concept_research/18-p-b11-frc/iter-02/sources/tae-energy-conversion-clarification.md` — TAE FAQ (tae.com/faq-fusion/); confirms steam turbine as Da Vinci baseline energy conversion; also confirms p-B11 fuel and FRC confinement rationale.
- `knowledge/concept_research/18-p-b11-frc/iter-02/sources/tae-c2w-machine-details.md` — IAEA FEC 2020 paper (Gota et al.) on C-2W/Norman device; provides C-2W plasma parameters and machine geometry; no commercial plant data.
- `knowledge/concept_research/18-p-b11-frc/iter-02/sources/nature-articles-s41467-025-58849-5/output.md` — Nature Communications 2025 paper on NBI-only FRC formation; covers Norm experimental configuration, plasma parameters, and field-reversal physics; no commercial plant electrical output data.
- `knowledge/concept_research/18-p-b11-frc/iter-02/sources/osti-pages-servlets-purl-2441289/output.md` — Nuclear Fusion 2024 paper (Gota et al., OSTI 2441289) on enhanced C-2W performance; confirms Te ~1 keV peak, total plasma energy ~13 kJ, NBI efficiency data; no commercial plant data.
- `knowledge/concept_research/18-p-b11-frc/iter-01/sources/grokipedia-tae-technologies.md` — Grokipedia article on TAE Technologies; comprehensive third-party narrative covering machine history, commercial roadmap (Copernicus → Da Vinci), and 100–500 MWe modular plant vision.
- `knowledge/concept_research/18-p-b11-frc/iter-01/sources/tae-nbi-breakthrough-2025.md` — TAE press release (April 2025) on Norm breakthrough; confirms Copernicus as next-generation device targeting net energy, Da Vinci as first prototype power plant; no new power output figures.
- `knowledge/concept_research/18-p-b11-frc/iter-02/sources/tae-djt-merger-davinci-specs/output.md` — Same merger article, raw extraction; consistent with the `.md` version above.
- `exploration/concept_analysis/analyses/18-p-b11-frc/analysis.md` — Existing analysis document (used for reference/orientation only, per instructions); cross-checks source inventory and confirms 50 MWe as the sole published electrical output figure for any TAE commercial design.

## 2. Candidates surfaced

**Sewer Pipe / Device B / C-1 (1999–2004):** Early laboratory prototypes. No electrical output by design. Not candidates.

**C-2 (2005–2014):** Third-generation experimental FRC device. NBI heating and sustainment validated. No electrical output by design. Not a candidate.

**C-2U (2014–2017):** Fourth-generation upgrade. Demonstrated sustained FRC plasmas at 10+ ms. No electrical output by design. Not a candidate.

**C-2W / Norman (2017–2024):** Fifth-generation device, world's largest compact-toroid device. Separatrix radius 0.4 m, plasma length 2 m, NBI up to 21 MW, plasma lifetime up to ~40 ms. Key recent records: Te ~1 keV peak, total plasma energy ~13 kJ. **No electrical output by design** — this is an experimental physics device whose purpose is to qualify plasma operating modes for Copernicus. No P_native. Not a candidate.

**Norm (2025–present):** Modified version of C-2W with theta-pinch formation sections removed; the machine that achieved the NBI-only FRC formation breakthrough (Nature Communications 2025). Shorter and simpler than Norman. **No electrical output by design** — still an experimental device. Not a candidate.

**Copernicus (planned ~2026 construction):** TAE's sixth-generation device, designed to demonstrate scientific breakeven — net energy production using p-B11. Power supply rated at up to 750 MW bi-directional to support plasma control. This bi-directional power rating is the input power system, not net electrical output; Copernicus is explicitly described as the physics breakeven demonstration step, not an electricity-generating plant. **No net electrical output by design.** Not a candidate.

**Da Vinci — 50 MWe initial design:** Described as TAE's "first prototype power plant" and "first integrated prototype for a hydrogen-boron fusion power plant capable of grid-connected electricity generation." The DJT merger announcement (December 2025, published in ANS Nuclear Newswire) explicitly states: "The combined companies plan to site and begin construction on a **50-MWe** utility-scale fusion power plant in 2026." The TAE FAQ confirms steam turbine electricity generation as the baseline. p-B11 fuel is the declared fuel cycle. P_native = **50 MWe**. This is the only design in TAE's portfolio with a stated net electrical output. Published parameters are limited: power (50 MWe), fuel (p-B11), energy conversion (thermal/steam), and a construction timeline. No geometry, plasma parameters, or engineering architecture are public.

**Da Vinci — 350–500 MWe "at scale" aspiration:** The dossier and press materials mention 350–500 MWe as a scaled commercial target. However, this is described as the long-term scaling outcome of the Da Vinci program, not a separately engineered design with its own published parameters. No geometry or engineering architecture has been published for this scaled version. This is a roadmap aspiration, not an independent design point, and adopting it would require stitching the 50 MWe Da Vinci geometry (if it were published) with a larger power figure — which is forbidden. Not selectable as a standalone candidate.

## 3. Selection

Da Vinci at 50 MWe is the only design in TAE's published portfolio with a stated net electrical output. All predecessor and intermediate machines (Norm, Copernicus) are physics demonstration devices with no electrical output by design. The 350–500 MWe scaled aspiration is not an independently engineered design point and cannot be selected without plant-stitching.

The 50 MWe figure is published in a formal merger announcement (ANS Nuclear Newswire, December 2025), making it a company-committed output figure rather than a back-of-envelope estimate. However, the engineering design underlying that commitment is entirely unpublished — no geometry, plasma parameters, magnet configuration, or capital cost decomposition exists in any public source. The grounding confidence is therefore `low`: this is a company press-announcement commitment, not an engineering whitepaper.

```yaml
proposal:
  concept_id: 18-p-b11-frc
  design_name: "Da Vinci 50 MWe pilot plant (TAE Technologies, December 2025 merger announcement)"
  maturity_tier: paper-concept
  grounding_confidence: low
  p_native_mwe: 50
  primary_sources:
    - knowledge/concept_research/18-p-b11-frc/iter-02/sources/tae-djt-merger-davinci-specs.md
    - knowledge/concept_research/18-p-b11-frc/iter-02/sources/tae-energy-conversion-clarification.md
  selection_rationale: |
    Da Vinci is the only TAE design with a published net electrical output figure. The
    December 2025 Trump Media / TAE merger announcement (ANS Nuclear Newswire) commits to
    "construction on a 50-MWe utility-scale fusion power plant in 2026," making this the
    single selectable design point in the portfolio. All earlier machines (C-2W, Norm,
    Copernicus) are physics demonstrators with no net electrical output by design.
    The 350–500 MWe "at scale" aspiration is a roadmap target without a separate
    engineering architecture; adopting it would require plant-stitching across two distinct
    design specifications, which is forbidden. The p_native_mwe of 50 is the per-plant
    figure; TAE's architecture does not describe Da Vinci as a multi-module design, so
    no module subdivision applies. Grounding confidence is low because the 50 MWe figure
    traces to a merger press announcement, not to a published engineering design; no
    geometry, plasma parameters, or engineering architecture for Da Vinci is in the
    public record.
  alternatives_considered:
    - design: "C-2W / Norman experimental device"
      reason_rejected: "No net electrical output by design; physics demonstrator only"
      sensitivity_implication: "n/a — no P_native exists for this design; cannot substitute for Da Vinci in the comparison"
    - design: "Norm experimental device (modified C-2W)"
      reason_rejected: "No net electrical output by design; experimental breakeven-preparation device"
      sensitivity_implication: "n/a — no P_native exists for this design"
    - design: "Copernicus (sixth-generation device, planned)"
      reason_rejected: "No net electrical output by design; purpose is scientific net-energy demonstration, not grid power"
      sensitivity_implication: "n/a — the 750 MW bi-directional figure is the plasma power supply rating, not an electrical output; no P_native exists"
    - design: "Da Vinci at 350–500 MWe scaled commercial target"
      reason_rejected: "Aspirational roadmap target with no independent engineering architecture; selecting this power figure with no geometry would constitute plant-stitching"
      sensitivity_implication: |
        If a fully engineered 350–500 MWe Da Vinci commercial design were published with
        its own geometry and plasma parameters, P_native would rise substantially from 50
        MWe → fewer modules at 1 GWe → 1 GWe LCOE shifts down. Worth revisiting if TAE
        publishes a detailed commercial plant specification post-Copernicus validation.
```

## 4. Open questions

- **If Copernicus publishes detailed engineering parameters or a stated net-energy output Q value**, the physics viability picture would shift significantly and might provide indirect grounding for Da Vinci's fusion power requirement — though it would not itself become the design point (no electrical output by design).

- **If TAE releases a Da Vinci engineering whitepaper** with plant geometry (major radius, plasma length), NBI system specifications for the commercial plant, and thermal cycle parameters, `p_native_mwe` should be re-verified against those documents and `grounding_confidence` should be upgraded from `low` to `medium` or `high`. The merger announcement commitment alone is insufficient to ground geometry-dependent downstream calculations.

- **If the DJT merger completes and TAE becomes publicly traded (mid-2026 target)**, SEC filings may disclose Da Vinci engineering parameters that are currently proprietary — this is the most likely near-term source of improved grounding.

- **If TAE's announced 2026 construction start is delayed or revised**, the 50 MWe design point may be superseded by a differently sized or configured first plant; the design-point selection should be revisited against any updated merger or SEC filings.

- **The 350–500 MWe aspiration requires resolution**: if TAE publishes an engineering specification for a larger commercial follow-on plant with its own geometry and power, the question of whether the 1 GWe projection should use the 50 MWe pilot or the larger commercial design as the cost-modeling unit would need to be re-examined. The current selection uses 50 MWe with `n_mod = 20` implied for a 1 GWe fleet, which may overstate per-unit capital costs if the commercial design differs substantially from the pilot.