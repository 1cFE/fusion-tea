# Critique: 01-hts-compact-tokamak

## Defects (must-fix before publication)
- F2.d hedges its pole commitment: "**leverage pole with REBCO-slack for FOAK, hard-bottleneck on tritium/Li-6/Be lines**" — this is a split-along-sublines dodge rather than a committed pole. The rubric requires a single committed pole; if the split is principled, it needs explicit justification that REBCO and tritium are separately scored (and the trace's own logic — "REBCO is the dominant CAPEX line" — actually argues for a clean leverage-pole commit).
- F4.b is labeled "**Mixed, weighted toward R&D-driven**" — hedged without an explicit pole/mechanism commitment of the kind the rubric demands; "mixed" then resolved to R&D would be acceptable, but the wording leaves it ambiguous.
- F4.c is labeled "**Mixed**" then in the dominant-failure line resolved to failure pole — the pole commit should appear in the F4.c assessment itself, not be deferred.
- Dominant Stage-2 failure factor uses "with Stage 3 F3.a (tritium) as a close second" — the rubric's dominant-coordinate naming should be ONE factor; this is the "X with Y as close second" pattern flagged as a dodge unless genuinely close, and the trace does not justify closeness, it just asserts it.
- Dominant leverage similarly hedged: "Stage 2 / E2.a, with Stage 4 F4.a as the long-horizon equivalent" — two factors named without a closeness justification.
- Numeric inconsistency on REBCO pricing: F2.d states "$144–792/kA-m (2014) to ~$100/kA-m (2025)" but the methodology brief and Stage-4 references cite "$20/m in 2025 vs. $36–198/m in 2014" ($/m, not $/kA-m). The trace mixes units between F2.d and the cross-stage carrier ("$100/kA-m vs. $10/kA-m commercial target"); reviewer cannot reconcile whether 5,730 km @ $100/kA-m is consistent with the FOAK CAPEX number.
- REBCO capacity numerics drift: F2.d says "~3,500–4,000 km/yr globally" and "FOAK consumes ~1.5 yr of global supply" (5,730/4,000 ≈ 1.4 — OK), but F3.a says "10-plant 2035 fleet implies ~100,000 km" (should be ~57,300 km if linearly scaled from 5,730/plant). The 100,000 km figure is unexplained.
- Stage-4 REBCO demand claim "50 GWe ARC fleet would need ~125,000 km/yr" — no derivation given; not anchored to the ecosystem brief excerpt provided.
- F3.a pole commit "**Leverage pole, bottleneck-likely**" then immediately complicated by "FLiBe/Be/Li-6 supply remains failure-pole-bottleneck" and "tritium is the sharpest constraint" — same sublining defect as F2.d; the dominant-failure attribution then points to "F3.a (failure-pole sub-line: tritium)" which contradicts the pole assignment on the same factor.

## Soft issues (optional polish)
- F3.b uses "mixed" with a numeric anchor (60–70%) — acceptable as intrinsic characterization but not flagged with a methodology code distinction; this one is fine, just adjacent to the broader hedging pattern.
- "F3.c" assessment ends with a judgment but doesn't commit a pole — intrinsic F-factors don't have poles, so this is fine, worth noting only because the trace's pole discipline is uneven elsewhere.
- "Output format implication: 1costingfe extension" follows from the data shape, not from the dominant coordinates (F2.a failure / E2.a leverage) — the deep-dive Q1 (capacity factor) and Q3 (tritium fleet ramp) follow cleanly; Q2 follows directly. The format recommendation is reasonable but is justified by data availability, not by the trace's dominant-coordinate output — worth noting.
- Cross-stage carrier "fuel-ecosystem R&D position" is treated as universally positive; no failure-pole framing where the D-T cohort's shared dependency could also be a shared-failure carrier.

## Overall verdict
- Not publication-ready as a worked example: the pole-commitment discipline on F2.d, F3.a, F4.b, F4.c and the dual-factor naming of both dominant coordinates collectively undermine the trace's role in demonstrating how the rubric is supposed to discipline hedging — the single biggest blocker is the sublined "leverage-pole-but-also-failure-pole" treatment of the ecosystem-relational F-factors at Stages 2–3.
