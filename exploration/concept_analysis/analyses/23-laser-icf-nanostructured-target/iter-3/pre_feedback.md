VERDICT: FINDINGS

Source: portfolio audit 20260607-145539, finding #4 (high). This is the override-layer mirror of the CAS21 issue: a whole-plant cost being multiplied by module count when it should be held flat.

### F-1: Whole-plant fixed-dollar overrides (laser driver, target factory) are multiplied by module count in the 1 GWe projection
- **Target:** analyses/23-laser-icf-nanostructured-target/model_setup.py:128-164 (C220104 driver $2000M, C220108 target factory $200M); lib/model_setup_helpers.py (CAS22 replication by n_mod)
- **Category:** model
- **Finding:** The native plant is 100 MWe, so the 1 GWe projection sets n_mod = round(1000/100) = 10 and multiplies native CAS22 (C220000 = $2286.0M) by ~9.9087, giving $22,651.4M (matches the probe to the dollar). The two hand-entered overrides sit inside that CAS22 base and are multiplied along with everything else: the $2000M laser driver becomes ~$19.8B and the $200M target factory becomes ~$2B. The code itself states (lines 128-164) that these "do not scale with module count" and "must represent the full 1 GWe plant" — but the projection ignores that written intent. About $19,599M of plant capital exists only because of this multiplication — roughly 57% of the reported $34,621/kW overnight cost and the reason the headline is 793.2 $/MWh while the rest of the laser-IFE family sits at 55-94 $/MWh. (Red-herring to ignore: CAS70 is NOT 2000× the norm — it goes $109.1M→$992.9M and is a reduction; CAS80 $231.7M→$2316.7M is a library-computed symptom of the inflated CAS22, not a separate defect.)
- **Recommendation:** Hold the two whole-plant overrides flat across modules (do not let them ride the ×n_mod CAS22 replication). The value itself is well-sourced — $1.5B LLNL full-plant driver requirement (`osti-servlets-purl-15013230/output.md` line 61) × 1.33 immaturity premium = $2000M, ~500 lasers/plant per `optics-news-16-4-4` — so keep the dollar figure and fix the scaling, not the value. Re-run and report where the 1 GWe LCOE actually lands (expected ~340 $/MWh) rather than estimating.
- **Priority:** blocking

### F-2: Confirm no other large fixed-dollar overrides on this concept ride the same multiplication
- **Target:** analyses/23-laser-icf-nanostructured-target/model_setup.py overrides list
- **Category:** model
- **Finding:** The defect is structural (any whole-plant absolute override inside the replicated CAS22 base inflates ×n_mod). After fixing F-1, verify every remaining override on this concept is either genuinely per-module or correctly held at plant level.
- **Recommendation:** Audit each override's intended frame (per-module vs whole-plant) and confirm the projection treats it accordingly; document the frame in each rationale.
- **Priority:** important
