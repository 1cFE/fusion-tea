# Heavy Ion Beam Fusion — Recent Research Compilation (Iter-02)

## Source Summary

This document compiles findings from iter-02 web research on heavy ion beam ICF, focusing on:
1. Verifying/updating existing dossier values
2. Searching for "Intensity Energy" as a company
3. Finding recent (2020s) developments in HIF

---

## Company Verification: "Intensity Energy"

**Result**: Still unverifiable. Multiple targeted searches conducted:
- `"Intensity Energy" fusion` — no results
- `"Intensity Energy" company fusion accelerator ion beam` — no results
- FIA 2025 member lists — 53 companies participated in 2025 survey; no "Intensity Energy" found
- The only "Intensity" company found is **Intensity Infrastructure Partners**, a midstream natural gas pipeline company (not fusion)

**Conclusion**: "Intensity Energy" remains unverifiable as a fusion company. Likely a placeholder name in the original concept list.

---

## Key Technical Parameters (Confirmed/Updated)

### Driver Efficiency
- **30-40% wall-plug efficiency** — confirmed by multiple sources:
  - arxiv 2005.07520: "HIBs are generated with a high driver efficiency of ~30-40%"
  - Wikipedia (Heavy ion fusion): "approximately 30 to 40% of the input energy into the beam"
  - Compare to lasers at ~1-15%

### Repetition Rate
- **Historical designs**: HIBALL 5 Hz/chamber, HYLIFE-II 6-8 Hz
- **Modern estimates**: arxiv 2005.07520 states "~10-15 Hz" for future HIF reactors
- **Conclusion**: Update from "~10 Hz" is well-supported. The 10-15 Hz range from recent literature better reflects current targets.

### Target Gain
- Required gain: ~50-70 for a 1 GWe plant (arxiv 2005.07520)
- HYLIFE-II nominal: gain of 70 at 5 MJ → 350 MJ per shot

### Energy Conversion
- HYLIFE-II explicitly uses **steam Rankine cycle** (confirmed by OSTI 7368768 "improved heat transport system and steam power plant")
- Multi-unit HYLIFE-II study (OSTI 10170594) also evaluated **MHD + Steam** hybrid: "direct MHD conversion of plasma from target blanket shells"
- HIBALL: also steam cycle with LiPb heat transport
- **No modern HIF study found specifying sCO2** — this remains speculative

### Blanket Designs
- HIBALL: LiPb (lead-lithium), TBR ~1.195
- HYLIFE-II: FLiBe (Li₂BeF₄) molten salt thick liquid jets
  - Eliminated intermediate heat exchangers in improved design
  - 30-year chamber lifetime with no first wall replacement
  - Tritium inventory: 0.5 g in molten salt, 140 g in tube wall metal

---

## Current Experimental Programs

### NDCX-II (LBNL, USA)
- Neutralized Drift Compression Experiment II
- Induction linac accelerating Li⁺ ions to 3.5 MeV
- Compresses 500 ns pulse to ~1 ns in 15 meters
- Primary purpose: warm dense matter studies (WDM) at ~10,000 K
- Also relevant to HIF target physics
- Collaboration: LBNL, LLNL, PPPL (HIFS-VNL)
- Status: operational since ~2012, incremental upgrades

### FAIR (GSI, Darmstadt, Germany)
- Facility for Antiproton and Ion Research
- SIS100 accelerator commissioning planned 2025
- Will deliver up to 5×10¹¹ uranium ions
- Heating targets to 30-50 eV in ~100 ns pulses
- Relevant for benchmarking HIF driver parameters and target designs
- First beams for science experiments expected 2025

### Other Facilities
- HIAF (China) — Heavy Ion Research Facility
- KEK (Japan) — induction accelerator for HIF studies

---

## Multi-Unit Plant Concept (OSTI 10170594)

- Multiple HYLIFE-II target chambers sharing single RIA driver and target factory
- Evaluated both conventional steam BoP and advanced MHD+Steam hybrid
- Learning curve benefits across duplicated components
- Optimized for minimum cost of electricity and hydrogen production

---

## No New Private Companies Found

Despite extensive searching of:
- FIA member lists (2025 report, 53 companies)
- Crunchbase, LinkedIn (searched in iter-01)
- ARPA-E and DOE award databases
- Conference proceedings (APS-DPP, IAEA FEC)
- News and press releases

**No private company pursuing heavy ion beam ICF was identified.** The technology remains in the national lab/academic research phase. Key active researchers are at LBNL, LLNL, GSI/FAIR, and universities in Japan and China.
