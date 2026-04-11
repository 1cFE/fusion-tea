## Iteration 1 — 2026-03-22

### Changes Applied
- PA-1: analysis.md §Section 5 table "Net plant electrical output (estimated)" Value/Range — replaced "~300–500 MWe" with "~5 MWe" and added "(far below 1 GW company target by ~190×)" — agree
- PA-2: model_setup.py CAS21 cost_override — corrected override value from $420M to $443M (= $511M − $68M) and updated comment to show correct arithmetic — agree
- PA-3: model_setup.py line 137 comment — replaced "Rounded to 0.1 MW to avoid numerical zero in framework" with "Rounded up by ~1000× from 0.0001 MW (100 W physical) to avoid numerical zero in framework. Impact on results negligible (<0.01% of total driver power)." — agree
- PA-4: analysis.md §Section 5 table "Total company funding" Source column — changed from "§FusionXInvest Profile" to "§Adelaide Laser Partnership (2025); §FusionXInvest Profile" — agree
- PA-5: analysis.md §Section 5 table "Neutron fraction" Source — changed from "hb11-technology-page.md §Key Technical Details" to "[nuclear physics constant]" and added clarifying note to Notes column; model_setup.py blanket_t and mn Source comments updated from technology page citation to "[nuclear physics constant — p-B11 primary reaction aneutronic; neutrons only from secondary reactions (D-D, n-B11, etc.)]" — agree
- PA-6: model_setup.py line 1 docstring — corrected "1costingfe model setup" to "1cfe model setup" — agree

### Changes Skipped
(none — all decisions were agree)
