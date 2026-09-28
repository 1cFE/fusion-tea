# Learnings: priced-levers

What this run now knows. Append-only, newest last, ISO dates, never edited in place. An entry is appended **only after** a round review has accepted or corrected the delta the round result proposed (`GOAL_RUNBOOK.md` § The fresh review). Mechanical failures produce no learning.

Learnings L-001..L-006 of the predecessor goal `operating-point-closure` are cited from `goal.md`, not restated here.

## L-001 — At the printed 50 MW and held geometry, the machine sustains itself under the conductor ceiling only where the wall stops it, and the one cheap candidate left is ceiling-blocked

- **Evidence:** `exploration/stellarator_e2e/studies/20260903-priced-levers/` record § 4/§ 15 #1 + Addendum A.3 (`@30b651f0`), `synthesis.md` § 2.2, `results/points.csv` + `results/oracle_operands.csv` (reviewer recount, `evidence/round1_review.md`): 141 of 240 p50 points sustain; all 30 that also clear the ceiling fail the wall (27 wall-alone, ≥1.42× over 4.05); 6 ceiling-alone, three of them (`c0148/c0164/c0180`: I 17 MA, T 17 keV, n 1.0×, B_peak 27.49 T, σ ≤ 789 MPa, required heating 22.4 MW) at 262.08–262.16 $/MWh against the 110 MW optimum 271.359, before the conductor grade is charged (T-001 basis, `evidence/T-001_research_return.md` § 5: ×1.06–1.16 in tape for that step).
- **Scope:** pin `6262dbf4…`, R 12.7 / a 1.3 (geometry not swept), T 14.63–19 keV, n 0.8–1.4×, `B_max` held at 24.9, the wall fence as bound (average operand, peak limit).
- **Implication:** by count the wall is the blocker at 50 MW; by cost the conductor ceiling is. WI-038 decides which, and runs *after* the wall fence is made honest, because a tighter wall fence may close both escapes. No future session reads WI-038 as "a minor fence".
- **Supersedes:** refines `operating-point-closure` L-005; supersedes `goal.md` § Amendment 2026-09-02's "raising `B_max` alone opens no feasible region at 50 MW" at this pin.
- **Accepted by:** round 1 review, 2026-09-03 (corrected from the proposed form, which read the count as the whole answer).

## L-002 — A lever is priced only when the cost account that owns the material it moves responds, and `indicators.json` shows that before any point runs

- **Evidence:** `20260903-priced-levers/indicators.json` (`j_wp` reaches `lcoe`, `total_capital`, `cas72` through the cryoplant, and not `magnet_capital`); record § 6 `j_wp`, § 8 MD-2, § 15 #2 (magnet capital delta exactly zero over a 2.33× swing; LCOE 0.100%); `work/active/WI-036_winding-pack-sizing/design.md` D8 (~85% of the pack's mass has no cost account); `evidence/T-007_precritique.md` MAJOR 1.
- **Scope:** this package; any lever whose consequence is a mass or a volume.
- **Implication:** a study scope names the account that should carry what the lever moves and confirms the lever reaches it in the indicator run; reaching LCOE through a side channel is not pricing.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-03 (corrected).

## L-003 — A held axis inherited from a prior study can decide a fence conclusion

- **Evidence:** `evidence/T-007_precritique.md` MAJOR 2; record § 6 `T_i0`, § 12, § 15 #5, Addendum A.5. Holding T at 14.63 keV (the predecessor's grid slice) produced the "conductor ceiling is the last fence" pre-registration; sweeping T overturned it. Restricting to the 14.63 keV slice raises the best feasible LCOE from 271.359 to 288.004.
- **Scope:** the 16.645 $/MWh is the difference of two window- or fence-bounded optima, not a slope; the 110 MW optimum is window-bounded in T (18 keV) and `j_wp` (130) with the wall 0.007 MW/m² away.
- **Implication:** every fence study on this package sweeps T with a window that extends past 18 keV until the wall catches it, and checks inherited holds for load-bearing before pre-registering. The fresh pre-execution critique is what caught it; it is load-bearing, not ceremony.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-03 (accepted with one tightening).

## L-004 — `sigma_allow` is not a lever, and the reason is the conductor, not the steel

- **Evidence:** `evidence/T-002_criterion_return.md` §§ 3–5 and the registered sources: read as a peak check the steel rule would allow ~1000 MPa (Titus IAEA 2018 `output.md:99,468`; the category assignment is a reading, not a sourced statement); the conductor's axial limit re-tightens at nearly the same place (SuperOx 0.45–0.47%, Barth 2015 `output.md:173,197`); transverse limits the model cannot see are ~200× tighter (Zhai FNSF `output.md:41`). The two-check form is built (WI-036) and inert at 0.4% (study maximum 0.286%, Addendum A.1).
- **Scope:** this design's winding pack; the REBCO/316LN pair; strain limits bracketed by 4.2 K and 77 K measurements (the 20 K source, Pierro 2019, is queued).
- **Implication:** no strategy opens a region by moving the stress fence. A 0.2% conductor limit would flip the baseline (0.217%) and 323 of 439 points — a disclosed verdict change if ever adopted. The tape-vs-Lorentz asymmetry (×1.12 / ×1.45 for 24.9 → 30 T, T-001) is WI-038's pricing input and lives in L-001's pointer.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-03 (corrected to one claim).

## L-005 — The hold-out guard cannot protect a session from what a research subagent already read

- **Evidence:** `evidence/T-002_criterion_return.md` § 6; `knowledge/research/requests/runs/REQ-036-03/20260903T181625261847/return.json` `queued[]` (`arXiv:2409.01925`, `term:aries-cs matched 4x`). The registry guard fires at registration; the subagent's fetch precedes it.
- **Scope:** the research seam as built; every research subagent spawn.
- **Implication:** research subagent instructions carry the clean-room screen before any fetch; a refusal is recorded durably and surfaced to the owner, never absorbed. Open owner ruling: PROTOCOL §6 on `arXiv:2409.01925` (leave refused, or grant); nothing depends on it.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-03 (accepted as written).

## L-006 — Write the task scope and start before invoking `/run-study`, and run `tests/study/test_records.py` before the study commit

- **Evidence:** this round: T-007 ran and was committed with no scope or start line (`trail.md` § T-007 scope, reconstructed after the fact); the record failed two closure checks at resume and carried five prose misstatements caught only by the fresh administrator's recount (record Addendum A/B; `synthesis.md` § 6); the `snapshot.json` repair that followed is a recorded defect against step 15, not a precedent.
- **Scope:** every goal round that ends in a committed study.
- **Implication:** the scope and start lines precede the run-study intake; `test_records.py` runs before the record commit; the administrator's recount is load-bearing.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-03 (title corrected; body accepted).
