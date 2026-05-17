# Changelog: Laser ICF - Nanostructured Target (p-B11)

## Iteration 1 — 2026-03-07

### Changes
- Created dossier from scratch (no prior dossier existed)
- **Confinement Family**: set to `IFE` (high confidence) — confirmed from both company websites
- **Confinement Concept**: set to `Laser ICF (ultrashort pulse)` (high confidence) — femtosecond (Marvel) and picosecond (HB11) pulses
- **Fuel**: set to `p-B11` (high confidence) — confirmed from baseline and both companies
- **Primary Heating**: set to `Laser (ultrashort pulse)` (high confidence) — non-thermal acceleration mechanism
- **Energy Capture**: set to `Hybrid (thermal + direct)` (medium confidence) — Marvel explicitly hybrid; HB11 has conflicting statements (direct conversion in papers vs. steam on website)
- **Plasma State**: set to `Compressed` (medium confidence) — best schema fit but imprecise for non-thermal block ignition
- **Magnet Type**: set to `None (IFE)` (high confidence) — HB11's laser-generated 10 kT field is driver-created, not external magnets
- **Tritium Breeding**: set to `N/A (aneutronic)` (high confidence)
- **Neutron Management**: set to `Minimal (aneutronic)` (high confidence)
- **Operation Mode**: set to `Pulsed` (high confidence)
- **Repetition Rate**: set to `~10 Hz` (medium confidence) — Marvel targets 10 Hz, HB11 targets 1 Hz
- **Driver Technology**: set to dual description covering both companies (medium confidence)
- New sources: Marvel Fusion website/patent, HB11 Energy website, Hora et al. arXiv, J. Fusion Energy 2023 paper

### Gap Assessment
- **Columns still incomplete**: Energy Capture (HB11 contradiction), Plasma State (schema fit), Driver Technology (efficiency data missing)
- **Recommendation**: A second iteration could target (1) HB11's most recent technical publications or investor materials to resolve the energy conversion contradiction, (2) IFSA or CLEO conference proceedings for laser wall-plug efficiency data, and (3) any published reactor conceptual designs from either company. Medium priority — 8 of 12 columns are high-confidence and the remaining gaps are company-divergence or schema-fit issues rather than missing data.

## Iteration 2 — 2026-03-07

### Changes
- **Energy Capture**: Resolved HB11 contradiction. HB11 has definitively pivoted to `Thermal (steam)` per current website ("conventional steam cycle generator"). Marvel remains `Hybrid (thermal + direct)`. Composite value unchanged but notes updated to reflect resolved divergence.
- **Plasma State**: Confidence strengthened by HB11's own language ("dynamically compressed Boron fuel"). Value unchanged (`Compressed`, medium confidence).
- **Driver Technology**: HB11 description updated — now "thousands of commercial lasers" (DPSSL, ~10% wall-plug efficiency target) replacing earlier single petawatt laser descriptions. HB11 targets updated from "solid HB11 cylinder" to in-house low-density foam targets (10x more efficient at proton acceleration). Value updated to `Femtosecond DPSSL (Marvel Fusion); multi-laser DPSSL array + foam targets (HB11 Energy)`.
- **Fuel**: Notes updated — HB11 now uses foam targets instead of solid cylinders.
- **Tritium Breeding / Neutron Management**: Notes enriched with UNSW collaboration confirming steel construction possible in aneutronic environment.
- **Overall confidence**: Upgraded from `medium` to `medium-high` — all 12 columns confirmed, major contradiction (Energy Capture) resolved, new supporting evidence for Plasma State.
- New sources: EU CORDIS CFE-NANO project, CALA LION 2 inauguration, UNSW/HB11 collaboration, CA-PROBONO COST Action, optics.org EUR50M extension.

### Gap Assessment
- **Columns still incomplete**: Energy Capture (company divergence — resolved but composite value oversimplifies), Plasma State (schema fit issue), Repetition Rate (undemonstrated targets), Driver Technology (Marvel wall-plug efficiency unknown)
- **Recommendation**: Low priority for further iteration. All 12 columns have values with medium or high confidence. Remaining gaps are (1) schema limitations (Plasma State), (2) company divergence that may warrant concept splitting rather than more research (Energy Capture), and (3) data that won't be available until facilities commission (Repetition Rate, ATLAS mid-2026). A third iteration is unlikely to yield significant improvements unless targeting IFSA/CLEO conference proceedings for laser efficiency data.
