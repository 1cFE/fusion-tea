VERDICT: FINDINGS

### F-1: Fuel cost calculation error inflates LCOE by ~$70/MWh
- **Target:** Model CAS80 fuel account and model_setup.py fuel consumption formula
- **Category:** model
- **Finding:** The model reports CAS80 fuel cost as $27.4M/yr for 2,739 kg B-11/yr, making fuel 26.75% of LCOE (~$72/MWh). This directly contradicts the analysis (Section 5), which states B-11 fuel cost is negligible (<$1/MWh). Physical check: at 390 MW fusion power and 8.7 MeV per reaction, B-11 consumption is ~160 kg/yr — roughly 17× less than the model computes. Even using the model's inflated quantity, natural boron at $2–5/kg totals ~$5,500–14,000/yr, not $27.4M/yr — implying an effective price of ~$10,000/kg in the model. The error misrepresents one of p-B11's defining TEA advantages (near-zero fuel cost), distorts the LCOE cost breakdown, and adds ~$70/MWh across all branches.
- **Recommendation:** Fix the fuel consumption calculation in model_setup.py using reaction energy 8.7 MeV = 1.394 × 10⁻¹² J/reaction and reactor thermal output to derive B-11 mass per year (~160 kg/yr at 390 MW fusion power). Apply a realistic B-11 price of $2–50/kg (natural boron to lightly enriched). After correction, fuel should appear as a negligible line item (<1% of LCOE), consistent with the analysis text. Rerun all branches and sensitivity sweeps.
- **Priority:** blocking

### F-2: Bremsstrahlung radiation loss fraction fixed at 15% — the #1 physics unknown is not swept
- **Target:** Sensitivity sweep set in model_setup.py; Section 2 Challenge 1
- **Category:** model
- **Finding:** The analysis correctly identifies bremsstrahlung power balance as the most critical physics challenge, noting it "can rival or exceed the fusion alpha power output" at Da Vinci conditions. Yet the model fixes f_rad = 0.15 across all scenarios and excludes it from all six sensitivity sweeps. At fully thermalized Maxwellian p-B11 conditions, f_rad could realistically exceed 0.80–1.0+, making Branch A the only outcome regardless of Q_plasma. TAE's non-Maxwellian T_i >> T_e strategy specifically aims to suppress bremsstrahlung — the degree of suppression achieved is the central undemonstrated claim. Keeping f_rad fixed understates the model's sensitivity to the concept's most uncertain parameter and decouples the sensitivity sweeps from the analysis's central technical bet.
- **Recommendation:** Add f_rad as a seventh sensitivity sweep spanning 0.05 to 0.90. Show LCOE and P_net at each value; identify the f_rad threshold above which Branch A is forced (P_net ≤ 0) at the baseline Q_plasma. Add a Q_plasma × f_rad viability grid analogous to the existing Q_plasma × η_NBI grid (sweep #7), converting the qualitative bremsstrahlung discussion in Section 2 Challenge 1 into a quantitative viability boundary.
- **Priority:** important

### F-3: Steam-mode economic inferiority claim not quantified against a D-T reference
- **Target:** Section 7 cross-concept notes and scenario comparison table
- **Category:** analysis
- **Finding:** Section 7 asserts "Steam-only p-B11 FRC is economically inferior to any D-T concept with equivalent Q_plasma" — an important positioning claim. This is argued logically (aneutronic structural savings cannot overcome a 60-point efficiency gap in steam mode) but is not demonstrated with a reference number. The scenario comparison table shows Branch B at ~$268/MWh and Branch C at ~$79/MWh but provides no D-T anchor. Without at least an order-of-magnitude reference — e.g., what the Helion D-He3 FRC exemplar estimates, or a generic D-T compact tokamak at Q=15 — the reader cannot assess whether the aneutronic structural advantages (no breeding blanket, no shielding, hands-on maintenance) could partially offset the efficiency penalty, or how large the gap is in $/MWh.
- **Recommendation:** Add a single reference row to the scenario comparison table for a D-T FRC or comparable concept at Q=15, steam Rankine, with a rough LCOE range drawn from the Helion D-He3 exemplar (~4 ¢/kWh) or another D-T analysis in the pipeline. Label it clearly as a rough reference, not a validated comparison. This anchors the "steam-mode p-B11 is uncompetitive" conclusion with an order-of-magnitude number and identifies what Q_plasma (if any) would close the gap given the aneutronic structural savings.
- **Priority:** minor
