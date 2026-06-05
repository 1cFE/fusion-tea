VERDICT: FINDINGS

### F-1: Reflect `mn=1.10` (canonical) throughout analysis.md and synthesis.md
- **Target:** `analysis.md` (Sections 2 / Modeling Approach / Section 5 parameter table); `synthesis.md` (any line citing `M_b=1.15`, `mn=1.15`, or the `800 × 1.15 = 920 MW` derivation).
- **Category:** analysis
- **Finding:** `model_setup.py` previously used `mn = 1.15` (HCPB+Be central estimate of the 1.10–1.20 range). The new policy in `prompt_templates/config/scoring_framework.md` §"Blanket energy multiplication" requires a Tier-A external cite for non-canonical `mn`. No such cite is available in-file (only an unspecified "1.10–1.20 range" rationale). The model has been reverted to the D-T canonical `mn = 1.10` and re-run (`model_output.txt` regenerated). The narrative in `analysis.md` and `synthesis.md` is now out of sync — they still cite `M_b = 1.15`, the derivation `800 × 1.15 = 920 MW`, and the implied η_th = 45% that follows from that.
- **Recommendation:**
  1. Update `analysis.md` Section 5 parameter table `mn` row to **1.10** with note: "canonical for D-T per scoring_framework.md §Blanket energy multiplication; HCPB+Be 1.15 variant reserved as sensitivity excursion pending external cite."
  2. Rework the §"Thermal-to-electric efficiency derivation" passage (analysis.md ~§2.1, lines around 81–95): replace `800 × 1.15 = 920 MW` with `800 × 1.10 = 880 MW thermal`. The implied η_th follows: gross thermal 880 MW, recirculating ~65 MWe ⇒ gross electric ≈ 415 MWe ⇒ η_th ≈ 415/880 ≈ 47%. Note that this brings the implied η_th into closer alignment with Rankine practice but is still uncertain; `eta_th=0.40` in `model_setup.py` is intentionally conservative.
  3. Update any synthesis.md prose citing `M_b=1.15` (lines 46, 228 (C5), 247 (F7)) to `M_b=1.10` and to `800 × 1.10 = 880 MW thermal`. The HCPB technology description (Be multiplier, TBR=1.30, EU-DEMO heritage) stays — only the multiplication factor shifts.
  4. Update the headline LCOE figures in any analysis prose to the regenerated `model_output.txt` values (LCOE 312.5 $/MWh at 350 MWe; cross-concept 1 GW LCOE 153.5 $/MWh). The availability sweep range 279–329 $/MWh is unchanged in structure.
  5. In §"Modeling Approach" or §"Sources of Uncertainty", add one sentence: "Central case uses the canonical D-T blanket multiplication factor 1.10 (no dedicated multiplier credit). HCPB+Be designs may yield 1.10–1.20 in EU-DEMO neutronics literature; a Tier-A cite would justify reverting to 1.15 as a central case."
- **Priority:** important
- **LCOE delta:** ~3–5% downward shift (thermal power reduced by 4.3%, partly offset by reduced overnight scaling on blanket size). Pure-magnitude check available in regenerated `model_output.txt`.
