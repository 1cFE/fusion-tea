Now let me compile the verified findings for all 12 columns.

---

## Verification Results — Magnetized Target Fusion - Pneumatic Compression (D-T)

All 12 columns from Iteration 1 have been verified. No values changed. Several values gained additional citations from newly found sources (2025 FST paper, IAEA FEC 2025 abstract, LM26 milestone reports).

### Confinement Family
- **Value**: `MIF`
- **Confidence**: high
- **Citation**: https://generalfusion.com/fusion-technology/; IAEA FEC 2025 abstract (Hildebrand et al.) — explicitly "Magnetized Target Fusion"
- **Notes**: Confirmed. MTF/MIF synonymous. General Fusion is the canonical example of MIF — magnetized plasma compressed by external mechanical driver at intermediate density/timescale between MCF and ICF.

### Confinement Concept
- **Value**: `Magnetized target (pneumatic)`
- **Confidence**: high
- **Citation**: FST 2025 paper (DOI: 10.1080/15361055.2025.2526266) — "array of pneumatic piston drivers"; schema vocabulary match
- **Notes**: Confirmed. The 2025 FST paper uses "pneumatic piston drivers" explicitly for the commercial design. LM26 demo uses electromagnetic theta-pinch of solid lithium as a surrogate, but the commercial concept is pneumatic/mechanical.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: FST 2025 paper — "spherical torus of deuterium-tritium plasma"; IAEA FEC 2025 — LM26 running with deuterium fuel
- **Notes**: Confirmed. D-T fuel cycle with tritium breeding integral to design. LM26 demo uses deuterium only (no tritium in demo).

### Primary Heating
- **Value**: `Mechanical compression`
- **Confidence**: high
- **Citation**: https://generalfusion.com/fusion-technology/; APS 2018 overview — compression raises plasma from ~0.1 keV to 10 keV; cavity volume reduced by 3 orders of magnitude
- **Notes**: Confirmed. Compression parameters from APS 2018: density 10²² → 10²⁵ ions/m³, temperature 0.1 keV → 10 keV, magnetic field 2 T → 200 T. Initial plasma formed by Marshall gun (coaxial plasma gun) as a compact toroid (spheromak-like), but the primary heating to fusion conditions is purely from mechanical compression.

**Correction to iter-01 note**: The plasma is described as a "compact toroid" or "spherical torus" in the literature, not a "spherical tokamak." The PI3 APS paper title references "spherical tokamak program" but the plasma configuration is technically a compact toroid formed by a Marshall gun. The IAEA FEC 2025 abstract and FST 2025 paper both use "spherical torus." This is a terminology distinction — it does not affect the schema value.

### Energy Capture
- **Value**: `Thermal (steam)`
- **Confidence**: high
- **Citation**: https://interestingengineering.com/energy/steam-driven-nuclear-fusion-reactor — liquid metal through heat exchanger → steam → turbine; piston steam recycling
- **Notes**: Confirmed. No evidence of sCO2 or other advanced power conversion cycles being considered. Steam Rankine cycle is consistent with the piston design (steam also powers the pistons in a partially self-sustaining loop). The 2025 FST paper focuses on fuel cycle, not power conversion, so no new data on this column.

### Plasma State
- **Value**: `Compressed`
- **Confidence**: high
- **Citation**: IAEA FEC 2025 — "compressional heating"; APS 2018 overview — 3 orders of magnitude volume compression
- **Notes**: Confirmed. Plasma driven to fusion conditions by implosion. LM26 April 2025 results confirmed ion temperature and density increases during compression.

### Magnet Type
- **Value**: `Self-confined`
- **Confidence**: high
- **Citation**: Wikipedia (General Fusion) — "magnetic fields supported by internal plasma currents and eddy currents in the wall"; schema definition for MTF
- **Notes**: Confirmed. The compact toroid has self-generated magnetic fields. Commercial compression is mechanical (pistons), not magnetic coils. LM26 uses electromagnetic theta-pinch coils for compression (as a demo surrogate), but these are not confinement magnets — they drive the liner.

### Tritium Breeding
- **Value**: `Liquid metal wall`
- **Confidence**: high
- **Citation**: FST 2025 paper (DOI: 10.1080/15361055.2025.2526266) — evaluates both PbLi and pure Li as liquid metal wall/breeder; https://generalfusion.com/fusion-technology/
- **Notes**: Confirmed and strengthened. The 2025 FST paper provides the strongest confirmation — it's a dedicated study of tritium fuel cycle for General Fusion's MTF power plant using liquid metal walls. Both lead-lithium eutectic (LLE) and pure lithium (Li) remain under evaluation for the commercial plant. The `Liquid metal wall` schema value covers both compositions. TBR analysis differs: Li design has >60% of tritium inventory in blanket; LLE design has >80% in isotope separation system.

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: high
- **Citation**: https://generalfusion.com/fusion-technology/ — liquid metal wall absorbs neutrons, breeds fuel, provides heat transfer; FST 2025 paper confirms dual-purpose liquid metal
- **Notes**: Confirmed. The liquid metal serves triple duty: compression medium, neutron shield, and tritium breeder. This is the canonical example of "integrated blanket/shield" — no separate blanket and shield structures.

### Operation Mode
- **Value**: `Pulsed`
- **Confidence**: high
- **Citation**: IAEA FEC 2025 — pulsed compression events; https://generalfusion.com/fusion-technology/
- **Notes**: Confirmed. Each cycle: inject plasma → compress → fusion burn → reset. Compression timescale ~1 ms. Well below 5-minute quasi-steady threshold.

### Repetition Rate
- **Value**: `~1 Hz`
- **Confidence**: high
- **Citation**: https://generalfusion.com/fusion-demo-plant/; https://hackaday.com/2025/03/27/general-fusion-claims-success-with-magnetized-target-fusion/ — "~1 cycle per second"
- **Notes**: Confirmed. All sources consistently cite ~1 Hz for the commercial target. LM26 currently operates at much lower rate (approximately once per day). The original "1-10 Hz" range from early descriptions appears to have narrowed to ~1 Hz in current planning.

### Driver Technology
- **Value**: `Pneumatic pistons + liquid metal`
- **Confidence**: high
- **Citation**: FST 2025 paper — "pneumatic piston drivers"; https://generalfusion.com/fusion-technology/; schema example vocabulary
- **Notes**: Confirmed. Steam-driven pistons compress a vortex of liquid metal (Li or PbLi) around the plasma. The 2025 FST paper confirms "pneumatic piston drivers" terminology and adds that the commercial cavity is ~4 m diameter.

---

## Remaining Gaps

No schema-level gaps remain. All 12 columns are at high confidence with multiple corroborating sources.

**Minor enrichments from this iteration**:

1. **Commercial power output**: Now confirmed as **300 MWe** (from General Fusion's commercialization page), resolving the previous "150,000 homes" estimate.

2. **Liquid metal composition**: The 2025 FST paper confirms both Li and PbLi are still under evaluation. Neither has been selected for the commercial plant. This is a Stage 2 modeling consideration, not a schema gap.

3. **Plasma terminology correction**: The compact toroid is a "spherical torus" (per IAEA FEC 2025 and FST 2025), not a "spherical tokamak" as loosely stated in iter-01. This doesn't affect any schema values.

4. **Commercial cavity scale**: ~4 m diameter (from FST 2025 paper). LM26 is 50% scale of commercial plasma.

5. **Compression parameters** (from APS 2018 overview): density 10²² → 10²⁵ ions/m³, temperature 0.1 → 10 keV, B-field 2 → 200 T, volume compressed by 3 orders of magnitude.

## Sources Consulted

**New sources found this iteration:**
1. [FST 2025: Fuel Cycles for Li and PbLi Walls in MTF Power Plant](https://www.tandfonline.com/doi/full/10.1080/15361055.2025.2526266) — peer-reviewed, confirms pneumatic pistons, ~4 m cavity, both Li/PbLi under evaluation
2. [IAEA FEC 2025: LM26 Abstract (Hildebrand et al.)](https://conferences.iaea.org/event/392/contributions/35891/attachments/19864/33918/IAEA%20FEC%202025%20LM26%20Abstract%20-%20Hildebrand.pdf) — 50% scale, 10 keV target, Lawson criterion 2026 target
3. [General Fusion: LM26 First Plasma Compression (April 2025)](https://generalfusion.com/post/watch-general-fusions-lm26-achieves-first-plasma-compression/) — lithium compression milestone
4. [General Fusion: Peer-reviewed Confinement Time](https://generalfusion.com/post/peer-reviewed-publication-confirms-plasma-energy-confinement-time-for-lm26/) — >10 ms energy confinement
5. [General Fusion: LM26 Assembly Complete](https://generalfusion.com/post/building-the-future-of-energy-lm26-assembly-complete/)
6. [General Fusion: Commercialization Path](https://generalfusion.com/commercialization-path/) — 300 MWe target
7. [APS 2018: MTF at General Fusion Overview (PDF)](https://generalfusion.com/wp-content/uploads/2022/04/aps-2018-magnetized-target-fusion-overview.pdf) — compression parameters
8. [APS: PI3 Plasma Injector Progress (PDF)](https://generalfusion.com/wp-content/uploads/2022/04/aps-recent-progress-plasma-injector-3-spherical-tokamak-program.pdf)
9. [General Fusion Wikipedia](https://en.wikipedia.org/wiki/General_Fusion) — Marshall gun, compact toroid details
10. [Innovation News Network: First MTF Plasma](https://www.innovationnewsnetwork.com/canadas-general-fusion-achieves-first-magnetised-target-fusion-plasma/56354/)

**Previously cited sources (confirmed still valid):**
11. [General Fusion Technology Page](https://generalfusion.com/fusion-technology/)
12. [COMSOL: Compressing Timeline to Fusion Future](https://www.comsol.com/story/compressing-the-timeline-to-a-fusion-future-141951)
13. [Interesting Engineering: Steam-Powered Piston System](https://interestingengineering.com/energy/steam-driven-nuclear-fusion-reactor)
14. [Hackaday: General Fusion Claims Success](https://hackaday.com/2025/03/27/general-fusion-claims-success-with-magnetized-target-fusion/)
15. [Fusion Conclusion: How GF Reactor Will Work](https://www.fusionconclusion.com/how-general-fusions-reactor-will-work-or-wont/)
16. [Metal Tech News: Plasma Compressed with Lithium](https://www.metaltechnews.com/story/2025/05/14/tech-bytes/general-fusion-compresses-plasma-with-lithium/2278.html)
