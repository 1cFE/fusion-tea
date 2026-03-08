Integration complete. Here's the summary:

**Files written:**
- `table.csv` — 31 rows (22 existing + 10 new IFE concepts)
- `citations.csv` — 372 rows (252 existing + 120 new)
- `checkpoints/checkpoint-05.md` — consistency analysis and recommendations

**Key findings:**

1. **3 major overlap/split issues** need upstream decision:
   - Concepts 26 + 30 overlap heavily (both Inertia indirect drive) — recommend merging
   - Concept 17 has fundamental within-row divergence (Xcimer vs Focused Energy) — recommend splitting
   - HB11 Energy appears in both concept 04 and 23 — recommend consolidating

2. **3 vocabulary issues** flagged for schema v0.3:
   - `Heavy shielding (14 MeV)` misapplied to D-D concept (2.45 MeV neutrons)
   - `N/A (aneutronic)` label misleading for D-D fuel
   - No vocabulary for Xcimer's hybrid direct drive or helium Brayton cycle

3. **IFE pattern**: All 10 concepts share Compressed/None (IFE)/Pulsed — these columns don't discriminate within IFE but remain valuable for cross-family comparison. Driver technology and repetition rate are the primary within-IFE differentiators.

4. **Commercial viability flags**: First Light pivoted away from projectile ICF (no active pursuer), "Intensity Energy" is likely a placeholder (not verified), Cortex Fusion is highly speculative (low confidence, no experimental results).
