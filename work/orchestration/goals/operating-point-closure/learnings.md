# Learnings: operating-point-closure

What this run now knows. Append-only, newest last, ISO dates, never edited in place. An entry is appended **only after** a round review has accepted or corrected the delta the round result proposed (`GOAL_RUNBOOK.md` § The fresh review). Mechanical failures produce no learning.

No entries yet.

## L-001 — The Stellaris appendix closure is admissible and reproduces the printed point A to ≤4% with nothing fitted

- **Evidence:** `evidence/T-002_prototype/NOTES.md` cross-check table + `op_solve_final_output.txt` (goal directory, committed `2df2c548`); equation images `page_031_eq_1..7.png`; iter-02 raw PDF; reviewer reproduction in `evidence/round1_review.md` § 2.
- **Scope:** the A.3 balance, A.7/A.8 ISS04 (P = W/τ_E substitution), A.5/A.6 ash chain, and the composed brems + W-line + Albajar radiation, at the Stellaris point A. ISS04's n19 must be read as line-averaged (vol-av misses τ_E by −23%). The model's analytic W-form (+9.2% vs printed 504.65 MJ) is the dominant fidelity gap and enters conducted loss as W^2.56.
- **Implication:** later strategies build on this chain as-is; any residual at the printed point is attributed first to the W-form, and W is never tuned to the printed value.
- **Supersedes:** none. **Accepted by:** round 1 review, 2026-09-01.
- **Update 2026-09-06** `[OWNER 2026-09-06, at the close of goal stored-energy-basis]`: the Scope and Implication lines above stand as written at their date. What is now known: "the model's analytic W-form (+9.2% vs printed 504.65 MJ) is the dominant fidelity gap" measured against a printed number no admissible source reproduces — the paper's own rules on its printed peaks give 518.3 MJ and its printed β row implies 567 (`stored-energy-basis` `learnings.md` L-002); the gap was the helium-ash profile shape in the pressure integral, about 6 % against the paper's own rules, not the integral form (L-003); WI-042 fixed it at the paper's own rule (`work/completed/20260906_WI-042_sourced-helium-ash-profile/`; L-004, L-007). "Attributed first to the W-form" now reads "to the profile family in the W integral"; "W is never tuned to the printed value" stands unchanged.

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

## L-004 — The Row-1 P3 anchor is satisfiable by forward sustainment; the "links vs determine" tension is rubric wording for the owner

- **Evidence:** `.project/active/demo-depth-rubric/grading-r1-regrade.md` (R1.P = 3 at `rubric.md@dc0f0b6d`, the anchor reading in the cell record and the contestable-anchor note); goal trail § Round 2 strategy revision (the committed reading); `evidence/round2_review.md` § 3.
- **Scope:** rubric v1 Row 1 as written. The anchor table's test ("links … and pushes back") is met by the sustainment architecture with temperature and density as levers; the row preamble's "determine" wording is the owner's to reconcile (owner-gated rubric revision path, both model states re-scored if taken).
- **Implication:** later rounds and rubric versions treat the anchor table as the operative test; nothing pre-settles the owner's preamble reading.
- **Supersedes:** none. **Accepted by:** round 2 review, 2026-09-01.

## L-005 — At the printed installed heating the baseline machine has no feasible operating point; the constrained optimum at 110 MW sits off the beta floor

- **Evidence:** `20260901-sustainment-fence` record §§ 3/4/6 + Addendum, `synthesis.md` (administrator recount), `results/points.csv` (reviewer recount: 0/176 feasible at p=50; best feasible 293.46793 $/MWh at beta 0.031091, I ∈ [15.0, 15.4] MA bounded by `sustainment_ok` below and `peak_field_ok` above).
- **Scope:** the baseline machine (R 12.7, a 1.3, wp_side 0.36) over the swept (I_coil, n_e0, T_i0, p_input) space at pin `35e922c5…`. Precision bound (review correction): the ~91 MW sustainment threshold is oracle-derived (required 90.6 MW at baseline); the **committed** resolution is one grid step — the fence flips between p = 90 and 100 MW and the committed feasible transect points sit at p ≥ 100.
- **Implication:** field is rewarded and the binding technology is the magnet (conductor grade), not plasma stability; the machine's evidenced escapes from the 50 MW deadlock are ≥ ~100 MW installed heating or a conductor-grade change — the two close-proposal routes (`#1`, `#4`).
- **Supersedes:** refines L-003 (the trade is now committed-study fact, not scan prediction). **Accepted by:** round 2 review, 2026-09-01.

## L-006 — Entry-point retirement costs a wide, budgetable fixture re-derivation surface

- **Evidence:** T-004 diff (`ff807d3d`, `5bea8964`): nine runner anchors, six known-answer fixtures, the census, suite constants, manifest, ANNEX — ~30 sites; the recorded ordering (anchors re-derived only after bit-exact oracle parity); the flipped R+tie test assertion carrying its own explanation.
- **Scope:** any future retirement of settable entry points in this package.
- **Implication:** integrate-task scopes name the fixture/suite surface explicitly (review constraint 6), and the re-derivation discipline stays "from live evidence, never patched to match".
- **Supersedes:** none. **Accepted by:** round 2 review, 2026-09-01.
