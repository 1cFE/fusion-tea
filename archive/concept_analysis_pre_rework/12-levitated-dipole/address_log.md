## Iteration 1 — 2026-03-22

### Changes Applied
- PA-1: Replaced "at keV plasma temperatures" with "at sub-keV plasma temperatures (hundreds of eV)" in analysis.md §Section 2 (Confinement Scaling, first paragraph) — agree
- PA-2: Updated funding source from "NZ Regional Development Fund" to "NZ Regional Infrastructure Fund" in analysis.md §Section 1 (Company transparency paragraph) — agree
- PA-3: Updated analysis.md §Section 5 ICRH wall-plug efficiency table row to cite JET/EAST published literature as primary source, with arXiv paper as context for ICRH vs. ECRH selection; updated model_setup.py `icrh_wall_plug_efficiency` docstring to clarify the figure derives from JET/EAST literature and the preprint provides selection context — agree
- PA-4: Clarified the flux pump energy timeline in analysis.md §Section 3: 95 kJ (0.095 MJ) was the world record at time of Junior paper publication (arXiv 2508.17691, 2025); 170 kJ is a subsequent milestone per the prototype roadmap — agree
- PA-5: Added inline citation `[openstar-prototype-roadmap.md §Lab Experiments]` to RT-1 peaked density profiles claim in analysis.md §Section 1 (Experimental heritage paragraph) — agree
- PA-6: Qualified the 1 MW-year/m² fluence threshold in analysis.md §Section 2 (Sacrificial Coil section) to note it is stated for tungsten shield replacement, with the ~1-year coil replacement cycle derived from coil design lifetime in that environment; updated §Section 5 parameter table Notes column accordingly — agree
- PA-7: Updated model_setup.py `thermal_efficiency` docstring to state η_th = 0.38 gives P_net ≈ 212 MWe vs. published 208 MWe, and that exact match requires η_th ≈ 37.5%; retained 38% as the round-number central estimate within the uncertainty band — agree
- PA-8: Replaced the TBR-derived justification for M = 1.10 in model_setup.py `blanket_energy_multiplication` docstring with: M = 1.10 is the 1costingfe standard D-T assumption (conservative); TBR and M are independent parameters; full accounting gives M ≈ 1.15–1.30; value may underestimate P_th by ~10–20%, making LCOE a lower bound — agree

### Changes Skipped
(none — all 8 decisions were agree)
