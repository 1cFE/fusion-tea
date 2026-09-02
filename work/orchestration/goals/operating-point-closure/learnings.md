# Learnings: operating-point-closure

What this run now knows. Append-only, newest last, ISO dates, never edited in place. An entry is appended **only after** a round review has accepted or corrected the delta the round result proposed (`GOAL_RUNBOOK.md` § The fresh review). Mechanical failures produce no learning.

No entries yet.

## L-001 — The Stellaris appendix closure is admissible and reproduces the printed point A to ≤4% with nothing fitted

- **Evidence:** `evidence/T-002_prototype/NOTES.md` cross-check table + `op_solve_final_output.txt` (goal directory, committed `2df2c548`); equation images `page_031_eq_1..7.png`; iter-02 raw PDF; reviewer reproduction in `evidence/round1_review.md` § 2.
- **Scope:** the A.3 balance, A.7/A.8 ISS04 (P = W/τ_E substitution), A.5/A.6 ash chain, and the composed brems + W-line + Albajar radiation, at the Stellaris point A. ISS04's n19 must be read as line-averaged (vol-av misses τ_E by −23%). The model's analytic W-form (+9.2% vs printed 504.65 MJ) is the dominant fidelity gap and enters conducted loss as W^2.56.
- **Implication:** later strategies build on this chain as-is; any residual at the printed point is attributed first to the W-form, and W is never tuned to the printed value.
- **Supersedes:** none. **Accepted by:** round 1 review, 2026-09-01.

## L-002 — A solved-T operating point is the wrong architecture at this model state; forward sustainment is the workable form

- **Evidence:** `evidence/T-002_prototype/NOTES.md` findings 1–4 (with the ≈90 MW correction, trail amendment 2026-09-01); `op_solve_final_output.txt`; reviewer's independent required-aux recomputation (`evidence/round1_review.md` § 2).
- **Scope:** the stellarator_09 baseline machine under its own limits (conductor ceiling B_axis ≤ 9.0, stress, wall load, beta). No stable feasible burn exists there; the printed point sits on the unstable branch ≈90 MW short of self-sustaining; near-marginal attractors amplify power error ~×3 into temperature. Forward sustainment (p_aux_required = p_rad + W/τ_E − f_α·p_α vs installed, a power limit per the Row-1 anchor) is exact for the balance itself — the ash chain inside it remains a damped fixed point (reviewer's correction) — keeps studies restatable, and leaves the baseline evaluable.
- **Implication:** rounds pursue the sustainment form; a solved-T rung is revisited only at a machine state where a stable feasible burn window exists inside the limits.
- **Supersedes:** none. **Accepted by:** round 1 review, 2026-09-01.

## L-003 — With confinement in the chain, field is rewarded and immediately collides with the conductor ceiling and the stress fence

- **Evidence:** `evidence/T-002_prototype/NOTES.md` finding 5 + `op_solve_final_output.txt` field-reward map; conductor/stress arithmetic verified by the reviewer against `stellarator_plant.sysml:157-165,205` and `20260830-stress-fence/synthesis.md:26`.
- **Scope:** loss ∝ B^−2.15 effective (printed A.8); at B = 10 T a feasible burn exists (n×0.85) but B_peak 27.7 > 24.9 breaches the held conductor ceiling and σ ≈ 802 > 800 MPa breaches the WI-035 stress limit at current wp_side; wp_side relief exists.
- **Implication:** the `20260823-magnet-technology-ab#4` pathology (field never rewarded, optimum at the beta floor) becomes a three-way trade — confinement reward vs conductor ceiling vs stress — which the round-2 study should exhibit as binding fences.
- **Supersedes:** none. **Accepted by:** round 1 review, 2026-09-01.
