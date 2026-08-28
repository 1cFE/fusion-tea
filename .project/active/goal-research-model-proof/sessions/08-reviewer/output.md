Round 1 review is written to `trail.md`, and the accepted learning delta is appended to `learnings.md`. No commits; nothing else on disk was touched.

## Verdict: `FINDINGS`

Two findings, neither reopening the round nor touching its conclusion. The round's answer holds: **1.0 MW is not defensible for a helium-primary loop at this scale**, and the repository supports ~4–6 % of thermal power — ~130–195 MW held at the baseline point.

**What I recomputed independently** (not checked against the trail's working): the baseline balance from `p_fus` = 2748.06 reproduces the study's own 0.1514 / 915.1 and 0.1160 / 1345.4; 4 % → 129.5 held / 132.1 computed, 6 % → 194.3 / 200.3; the `#5` reconstruction recipe from `points.csv` alone reproduces both grid corners exactly (0.9424 / 8.3 and 0.0572 / 4529.2); nine `p_th` cost accounts, exactly nine; `p_pump` still 1.0 in both homes of a byte-identical twin; `tests/study/test_records.py` passes 7.

**Finding 1 — a load-bearing citation is off by two lines.** The HCPB-representative-for-HCLL statement and the 80 bar figure are at `…wppmicpr17-17709.md:174`, not `:176` as the r2 return and the result both say. That statement is the *warrant* for transporting an HCPB ratio to Stellaris's HCLL blanket — it replaced the pressure match as the argument — and both checkpoints repeated the wrong line without checking it. Correction only.

**Finding 2 — Ruling 3 lands the top of the range against the round's own reading.** The r2 return concluded Cismondi's ~150 MW is preliminary and that "the low end is the direction of travel"; Ruling 3 then recommends ~195 MW without engaging that. The precedent it cites (`f_uplift_cryo`) parameterizes the unquantified remainder rather than picking an end. I endorsed the recommendation but put the choice back to the owner explicitly.

**The three things you asked me to weigh:**

- **Discovery rows — complete.** `#3` and `#5` appended correctly (`#5`'s Home really did read `unrouted`, so ADR-004 fired and the r2 acceptance is on the right ground), `#10` concurred, `#1`/`#2` reasoned out. I also checked `#4`, `#6`–`#9`, `#11` and the magnet-study unrouted rows myself; none is touched. One note: `#7` sits closer to what this reconstruction did than "nothing else was touched" implies, though it carries a real Home so no obligation fires.
- **The counter-reading — rejected.** The model increment was declared in advance as propose-not-land, so not landing it is fidelity. The study question was genuinely unreached but unreachable inside this round by the goal's own gates. I kept one point from it: the strategy should not have declared a study question its own gates made unreachable — carried into round 2 as a constraint.
- **The unreviewed round-close finding — confirmed.** DI-008's 2 % floor is divertor-relative, on two independent grounds: a subset loop can't be 2–3 % of plant thermal while the He+LiPb whole is ~1 %, and `:175`'s 12 MW at 2 % only closes against a ~600 MW divertor denominator, not ACT2's ~2500 MWth. That settles the 60–190 vs 30–190 discrepancy in the research file's favour.
- **Trigger 6 — stands.** Trigger 4 was the close call; the round isn't *waiting* on a gate, because § Answered when makes a trail-only answer complete by design.

**Learning delta:** all three accepted, L-001 corrected — it attributed the whole ~1–6 % spread to optimization, but the ~1 % leg is a blanket-architecture difference (dual-cooled, ~half the heat in helium), not a better-tuned version of the same loop. I folded the DI-008 divertor correction into it and fixed a "factor-of-two" that is a factor of 1.5, recorded in a dated amendment so the change isn't silent.

**Recommendation to the owner: close `p-pump-basis` as answered**, on three rulings — correct DI-008's floor and band without narrowing its basis; keep `p_pump` a held settable input, re-based; land ~195 MW with ~130 MW as the documented lower bound, register Cismondi, ingest Moscato. "Keep 1.0 MW" was tested and is not available at any end of the range.