# Changelog: Levitated Dipole (D-T)

## Iteration 1 -- 2026-03-07

### Changes
- Created dossier from scratch (no prior dossier existed)
- All 12 differentiation columns populated from research
- **Operation Mode**: Baseline "Continuous" (from CSV) changed to `Quasi-steady` -- power plant is pulsed by cryogen limits with >95% duty cycle
- **Primary Heating**: Determined to be `RF (ICRH)` (not ECRH as might be assumed from LDX heritage)
- **Fuel**: Confirmed `D-T` per OpenStar's own arxiv paper, contradicting Wikipedia's claim of D-D
- **Published Machine/Plant?**: Updated from "No" (CSV baseline) to "Yes" -- arxiv 2602.20564 presents detailed D-T power plant design
- 3 primary sources saved to `iter-01/sources/`

### Gap Assessment
- **Columns still incomplete**: Energy Capture (medium), Plasma State (medium), Tritium Breeding (medium)
- **Recommendation**: Another iteration is unlikely to resolve remaining gaps. All three medium-confidence columns are limited by information OpenStar has not yet published (balance of plant details, explicit Q values, finalized blanket design). Recommend marking this concept as complete for Phase 1a purposes and revisiting if OpenStar publishes follow-up papers.

## Iteration 2 -- 2026-03-07

### Changes
- **Plasma State**: `Burning` (medium) -> `Sustained` (high). Significant correction. Detailed re-reading of arXiv 2602.20564 power balance equations confirms the reactor requires continuous external heating (Paux is essential in Eq. 9), designs for fixed Qsci (not ignition), and alpha power in the good-curvature region is "entirely balanced by radiation losses." ICRH/ECRH/NBI described as "required," not supplementary. Per schema, this is "Sustained" not "Burning."
- **Primary Heating notes**: Added ICRH efficiency detail ("approaching 70%") and corrected Junior ECRH power to "<50 kW"
- **Tritium Breeding notes**: Added detail that ceramic selected over liquid metal for thickness reasons despite steady-state operation allowing liquid metal
- **Operation Mode notes**: Added cryogenic slushy rapid docking detail from OpenStar website
- **Confinement Concept notes**: Added prototype roadmap (Tahi ~2028, Maui ~2031, Tama Nui commercial)
- **Overall confidence**: Upgraded from `medium` to `high` -- all columns now high confidence except Energy Capture and Tritium Breeding (both medium due to genuinely unpublished details, not research gaps)
- 8 new sources consulted (news coverage, OpenStar website technical pages, arXiv HTML re-read)

### Gap Assessment
- **Columns still incomplete**: Energy Capture (medium), Tritium Breeding (medium)
- **Recommendation**: No further iterations recommended. Both remaining medium-confidence columns are limited by genuinely unpublished information (balance of plant cycle, blanket cooling scheme), not by insufficient research. Plasma State gap from iter-01 has been resolved (corrected to Sustained, high). This concept is complete for Phase 1a purposes.
