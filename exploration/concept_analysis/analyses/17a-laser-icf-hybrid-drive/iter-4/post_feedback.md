VERDICT: FINDINGS

### F-1: Walkthrough concludes "No override" but registry enables four accounts
- **Target:** Section 5b (Override Candidates) — walkthrough prose vs. override registry
- **Category:** analysis
- **Finding:** The per-account walkthrough is the accountability mechanism that justifies each enabled override. For four accounts it reaches the opposite conclusion from the registry:
  - **C220101**: walkthrough ends "No override — insufficient cost data." Registry: `enabled: true, value: 0.40 * generic.costs.C220101`.
  - **C220102**: walkthrough ends "No override." Registry: `enabled: true, value: 0.30 * generic.costs.C220102`.
  - **CAS21**: walkthrough ends "No override." Registry: `enabled: true, value: 1.25 * generic.costs.cas21`.
  - **CAS27**: walkthrough ends "No override — no company-grounded figure." Registry: `enabled: true, value: 92.0`.
  These are not borderline cases — the walkthrough text actively reasons against enabling each one. The effect is material: the four accounts move fleet overnight cost by roughly $250–350M net. Either revise each walkthrough paragraph to justify the derived override, or disable the override so the library default stands.
- **Recommendation:** For each of the four accounts, make the walkthrough text and the registry entry consistent. If the derived estimate is retained, the walkthrough paragraph must close with a positive justification ("Derived override enabled — rationale: …") rather than "No override." If no justification survives scrutiny, disable and remove from the registry.
- **Priority:** blocking

### F-2: C220104 rationale calls $560M a NOAK figure, but model output implies additional NOAK learning drives effective per-module cost below the company's NOAK floor
- **Target:** Section 5b C220104 rationale and `model_setup.py` overrides list
- **Category:** model
- **Finding:** The rationale explicitly states the override uses "the NOAK midpoint ($70/J × 8 MJ = $560M) to align with the NOAK cost basis used across the model." However, the model output shows the 1 GWe fleet value for C220104 is $740M. At n_mod ≈ 2.5–3 modules, this yields a per-module effective NOAK cost of $247–$296M ≈ $30–37/J — below Xcimer's published NOAK floor of $60/J. The framework's NOAK learning curve appears to be applied on top of a value the rationale declares is already NOAK, producing a double-discounted laser cost that is inconsistent with the company's own stated NOAK floor. The LCOE impact is meaningful: correcting to a true NOAK per-module cost of $560M would raise fleet C220104 from $740M to roughly $1,260–$1,400M, adding ~$70–90/MWh to the 1 GWe LCOE.
- **Recommendation:** Decide which frame the override represents. If $560M is the company's published NOAK cost per module and should be the floor (not subject to additional learning), document that and adjust the override or the framework call to prevent double-discounting. If $560M is intended as a FOAK anchor and framework NOAK learning is appropriate, change the rationale to say so explicitly and recompute — the FOAK midpoint from Table 1 is ~$880M ($110/J × 8 MJ). Either path needs a consistent rationale that does not call the value NOAK while the model applies further NOAK adjustment below the company's stated floor.
- **Priority:** important

### F-3: Three Class-U CAS22 sub-account overrides use wrong anchor path
- **Target:** `model_setup.py` overrides list (C220101, C220102, C220108 entries)
- **Category:** model
- **Finding:** Overrides on C220101, C220102, and C220108 anchor their relative values to `generic.costs.C220101`, `generic.costs.C220102`, and `generic.costs.C220108`. Per the override semantics, CAS22 reactor-island sub-accounts (C2201xx) must anchor to `generic.cas22_detail["C2201xx"]` — only non-CAS22 rollups live under `generic.costs`. The native values happen to be identical through both paths today (0.40 × 110.7 = 44.3, 0.30 × 77.3 = 23.2, 0.60 × 147.9 = 88.7 — all confirmed by model output), so there is no current numerical impact. But using the wrong accessor path violates the stated policy and will silently break if `generic.costs` and `generic.cas22_detail` ever diverge.
- **Recommendation:** In `model_setup.py`, replace `generic.costs.C220101`, `generic.costs.C220102`, and `generic.costs.C220108` with `generic.cas22_detail["C220101"]`, `generic.cas22_detail["C220102"]`, and `generic.cas22_detail["C220108"]` respectively. Verify the values are unchanged after the fix.
- **Priority:** minor
