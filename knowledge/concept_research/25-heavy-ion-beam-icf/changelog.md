# Heavy Ion Beam ICF (D-T) — Changelog

## Iteration 1 — 2026-03-07

### Changes
- **Created dossier from scratch** (first iteration)
- Confinement Family: set to `IFE` (high confidence)
- Confinement Concept: set to `Heavy ion beam ICF` (high confidence)
- Fuel: set to `D-T` (high confidence)
- Primary Heating: set to `Heavy ion beam` (high confidence)
- Energy Capture: set to `Thermal (steam)` (medium confidence) — inferred from HIBALL and HYLIFE-II designs
- Plasma State: set to `Compressed` (high confidence)
- Magnet Type: set to `None (IFE)` (high confidence)
- Tritium Breeding: set to `Li blanket (unspecified)` (medium confidence) — HIBALL uses LiPb, HYLIFE-II uses FLiBe; no company selection
- Neutron Management: set to `Integrated blanket/shield` (medium confidence) — both historical designs use integrated liquid blankets
- Operation Mode: set to `Pulsed` (high confidence)
- Repetition Rate: set to `~10 Hz` (medium confidence) — historical designs at 5-6 Hz, closest vocabulary match
- Driver Technology: set to `Linear induction accelerator` (high confidence)
- **Company verification failed**: "Intensity Energy" not found in any public database (FIA, Crunchbase, LinkedIn, ARPA-E, DOE, Wikipedia, news)
- **Sources saved**: 2 source files in iter-01/sources/

### Gap Assessment
- **Columns still incomplete**: Energy Capture (medium), Tritium Breeding (medium), Neutron Management (medium), Repetition Rate (medium)
- **Critical gap**: Company existence unverified — all design choices inferred from national lab studies, not company disclosures
- **Recommendation**: Another iteration could search for recent (2020s) HIF publications and check for new startups. However, if "Intensity Energy" is a placeholder, medium confidence from historical studies may be the ceiling for several columns. A targeted search for modern HIF power plant studies (post-2020) could potentially upgrade Energy Capture if sCO2 is now the reference.

## Iteration 2 — 2026-03-07

### Changes
- **Repetition Rate**: medium → high confidence. 2020 review paper (arxiv 2005.07520) directly states "~10-15 Hz" for HIF reactors, confirming the ~10 Hz vocabulary value. HIBALL 4-chamber x 5 Hz design also supports system-level ~10+ Hz rate.
- **Energy Capture**: citation strengthened with explicit OSTI report title "Improved HYLIFE-II heat transport system and steam power plant". Added note about MHD+Steam hybrid evaluation. Confidence remains medium (historical designs, not company disclosure).
- **Company**: "Intensity Energy" now definitively unverifiable — confirmed absent from FIA 2025 survey of 53 fusion companies. Almost certainly a placeholder. No private company of any name pursues HIF commercially.
- **Summary**: updated with lab experiment status (NDCX-II operational, FAIR/SIS100 commissioning 2025)
- **Key Sources**: added NDCX-II, FAIR/SIS100, and FIA 2025 survey

### Gap Assessment
- **Columns still incomplete**: Energy Capture (medium), Tritium Breeding (medium), Neutron Management (medium)
- **Recommendation**: No further iterations recommended. The medium-confidence values cannot reach high confidence without an actual company making design choices. The technology fundamentals are well-characterized from decades of national lab work.
