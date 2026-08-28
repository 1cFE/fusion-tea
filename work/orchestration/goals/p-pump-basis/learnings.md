# Learnings: p-pump-basis

What this run now knows.

Append-only, newest last, ISO dates, never edited in place. An entry is appended **only after** a round review has accepted or corrected the delta the round result proposed (`GOAL_RUNBOOK.md` § The fresh review). Mechanical failures produce no learning.

Each entry is one claim.

## L-001 — The repository's helium-pumping evidence spans ~1–6 % of thermal power, and the spread is blanket architecture first and loop optimization second; the helium-primary-blanket subset is ~4–6 %.

- **Evidence:** Cismondi 2017, ~150 MW of helium pumping against 2389 MW deposited in the EU DEMO HCPB blanket at 80 bar — 6.3 % (`knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/scipub-wp-content-uploads-eurofusion-wppmicpr17-17709.md@0bf791d1:174,176`). Moscato 2018, ≈131 MW against 2101.7 MWth for the same blanket, and 83–94 MW for a near-term eight-loop redesign — 6.2 % and ~4 %, at second-order grade because the source PDF is not ingested and the figures are read from an approved research artifact rather than a source line (`knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md@ffa5c54c:43`). ARIES-ACT, ~1 % of total thermal power for He and LiPb together (`knowledge/concept_research/33-state-backed-tokamak-best/iter-02/sources/osti-servlets-purl-1178069.md@aff7a2f9:100,290`).
- **The two axes, kept apart.** The 4 % against 6 % gap is optimization: two layouts of the same EU DEMO helium loop, and the source says so — accurate design studies are on-going to cut the pressure drop, with larger pipes taking the loop from ~9 km to ~3 km (`…@0bf791d1:176`). The ~1 % against ~6 % gap is not optimization. ARIES-ACT's blanket is dual-cooled PbLi with about half the heat removed by helium, at He:LiPb thermal power ratios of 27:73 and 49:51 (`…@aff7a2f9:157,197`); a machine that carries half its blanket heat in liquid metal is a different architecture, not a better-tuned version of the same one.
- **A correction to DI-008 this run found.** DI-008's 2 % floor is a divertor-relative figure read as a plant-relative one. `…@aff7a2f9:100` reads "a total pumping power for He and LiPb of ~1% of the total thermal power (~2% to 3% of thermal power in the He-cooled divertor)" — the parenthetical's denominator is divertor thermal power, since a subset loop cannot be 2–3 % of plant thermal power while the whole is ~1 % of it, and `:175`'s 12 MW of divertor helium at `Ppump/Pthermal` ≈ 2 % only closes against a divertor-scale denominator. So the ~60 MW end of DI-008's Stellaris band has no figure behind it, and the 60–190 vs 30–190 discrepancy `goal.md` § Grounding evidence logged resolves in the research file's favour. Amending DI-008 is reserved gate 4 and is not done.
- **Scope:** helium-cooled blankets at EU DEMO / Stellaris scale. The ~4–6 % subset holds for HCPB and, on the source's own statement that "the HCPB PHTS can be also be considered representative for the HCLL concept" (`…@0bf791d1:174`), for Stellaris's HCLL blanket. Not established for any other coolant, nor for a machine whose helium share of blanket heat is small.
- **Implication:** a re-based `p_pump` carries a factor-of-1.5 range that no further reading of these three sources will close, because the range is two design points and not a measurement spread. Closing it needs a loop design, which is reserved gate 5 and a different goal. A number quoted from this evidence to better than one significant figure is false precision.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-08-28. Corrected on accept: the proposed claim attributed the whole spread to optimization, which is right within EU DEMO and wrong across machines.

## L-002 — A missing power-balance operand column is recoverable post hoc when the record commits the driving channel and every other term of the sum is bound.

- **Evidence:** `rec_frac` and `p_net` reconstruct at all 3,792 rows of `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/results/points.csv@0d176a8c` from its `p_fus` and `eta_th` columns plus the design's bound inputs, with no oracle and no re-run. Verified against `results/oracle_scan.json@ffa5c54c` at the baseline (0.1514 / 915.1 at η 0.333, 0.1160 / 1345.4 at η 0.47) and at both grid corners (R=4, a=0.8 → 0.9424 / 8.3; R=20, a=2.2 → 0.0572 / 4529.2). Reproduces exactly. Re-derived independently by the round 1 review.
- **Scope:** this package as configured. It fails the moment any recirculating term becomes geometry-dependent. `p_cryo` is recoverable only because every cryo input is bound (`models/library/analyses/mfe_cryo_plant.sysml@8f3b510c:47-52` on inputs at `models/designs/stellarator_09/stellarator_plant.sysml@ba5c9945:567-600`), returning 0.8643516 MW at every grid point.
- **Implication:** discovery row `20260821-power-cycle-ab#5` is a cost, not a wall, for this package. A later round can locate a `rec_frac` fence from committed evidence without promoting a pin. It cannot locate an LCOE fence that way, which is L-003.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-08-28.

## L-003 — `p_th` is a cost driver as well as a power-balance quantity, so a power-balance input reaches LCOE by two paths, not one.

- **Evidence:** nine cost accounts take `p_th` directly in `models/designs/generic_mfe/mfe_plant.sysml@ba5c9945` — lines 330, 338, 366, 405, 431, 505, 515, 526, 544, covering blanket, shield, divertor, heat rejection, buildings, coolant, auxiliary cooling, waste and I&C. `p_pump` enters `p_th` through the `eta_p·p_pump` term (`models/library/analyses/mfe_power_balance.sysml@8f3b510c:119`). Count confirmed independently at both checkpoints and at the round 1 review; line 430 takes `p_the` and is not among them.
- **Scope:** the MFE plant spine as built.
- **Implication:** an LCOE effect cannot be estimated from `p_net` alone, so any LCOE question about `p_pump` needs a package run. `goal.md` § Invariants names only the `p_net` path and should be amended by the operator to name both; any future goal-level channel statement about a power-balance input has the same obligation.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-08-28.
