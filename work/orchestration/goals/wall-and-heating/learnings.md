# Learnings: wall-and-heating

What this run now knows. Append-only, newest last, ISO dates, never edited in place. An entry is appended **only after** a round review has accepted or corrected the delta the round result proposed (`GOAL_RUNBOOK.md` § The fresh review). Mechanical failures produce no learning.

Learnings of the predecessor goals `operating-point-closure` (L-001..L-006) and `priced-levers` are cited from `goal.md`, not restated here.

## L-001 — At the printed heating level, under the wall fence as bound, the escape is not heating-source efficiency; the level's fate is the wall's

- **Evidence:** `exploration/stellarator_e2e/studies/20260903-wall-and-heating/record.md` § 6 `eta_source_heat`, § 15 #1 (`@2d11ca1b`, Addenda `@31284e05`, `@577a6fa5`); `synthesis.md` § 3; the reviewer's recount with the wall verdict removed (`evidence/round1_review.md` § Grounds 1: minimum required 23.8 MW among 100 MW points passing every other fence, so the level opens at `eta_source` ≈ 0.24). Under the fence as bound: 0 of 240 at 100 MW wall-plug; the 36 sustainment-alone points need at least 87.061 MW coupled (`eta_source_heat` ≥ 0.871 at lossless coupling); the other 204 fail the wall or the ceiling, which efficiency does not reach.
- **Scope:** pin `2649e0ea…`; R 12.7 / a 1.3; the executed windows (I 14–17 MA, T 14.63–22 keV, n 0.9–1.2×) and the scan's 3080 candidates over efficiencies 0.40–0.60; `eta_couple_heat` 1.00; **the wall fence as bound (a flat-wall average against a printed peak)**. No buildability claim.
- **Implication:** the printed level's fate is the wall fence's. A source-efficiency study at the printed level is worth running only if round 2's honest fence *loosens* the wall verdict.
- **Supersedes:** none; refines `priced-levers` L-001 (the deadlock by count is the wall) at the heating side.
- **Accepted by:** round 1 review, 2026-09-04 (corrected from the proposed form, which lacked the fence-as-bound condition).

## L-002 — Whether an efficiency lever pays depends on which quantity is held, and a study asks in both parameterizations before it concludes

- **Evidence:** record § 3, § 6 `eta_source_heat`, § 15 #2; `results/points.csv` arms `arm-transect-eta` (fixed 220 MW wall-plug: LCOE 269.823 → 273.675 over 0.35 → 0.65, heating capital linear in efficiency, the draw constant) and `arm-couple-132` (fixed 132 MW coupled: 317.234 → 255.970 over 0.35 → 0.75, heating capital constant to the dollar); fusion performance bit-identical across efficiency in all 96 (I, T, n) cells.
- **Scope:** this package's heating chain; any conversion-efficiency lever whose cost driver and physics driver are different outputs of one chain.
- **Implication:** a study of a conversion-efficiency lever declares which of the chain's outputs is held (installed hardware or delivered output) and runs both parameterizations when they are different outputs. The first design asked only the forced one.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-04.

## L-003 — The external sources' factors are defined on shaped-wall averages, so transferring any of them needs the area basis; but the machine's own source prints its own 3D peak at its own 100 mm standoff and an average whose basis is not a shaped first wall — establish that basis before choosing the form

- **Evidence:** `evidence/T-001_research_return.md` §§ 3–5 (three registered sources: peaking 1.5–2.1 as a property of the chosen wall; shape factor 1.146–1.303 on the wall-side radius; the 0.30 m standoff); record § 15 #3 with the shadow columns (`results/points.csv`); checkpoint C-001.r2 (the 1.15–1.83× range holds for an unoptimised wall at a 0.30 m standoff; optimised walls give 0.86–1.07); the reviewer's finding 2 (`evidence/round1_review.md`): `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md` lines 231 (plasma surface 940 m²), 241 (peak 4.05 from 3D neutronics on the design's own first wall), 747 (average 2.87), 1295 (first wall at a minimum 100 mm from the plasma) — 2700 × 0.8 / 2.87 = 753 m², below the 940 m² LCFS, numerically a circular torus at R 12.7 m, r 1.5 m; the source-anchored net multiplier is 1.316, the baseline under it 4.088 against 4.05. Verified by the round agent before landing; the same source table also prints "Peak neutron wall power 4.95" (line 748) — two printed peaks for round 2 to reconcile.
- **Scope:** this machine's own source and the three registered external sources; the model's circular-torus area 701.926 m² at the wall-side radius 1.40 m.
- **Implication:** round 2 establishes the 2.87's averaging basis from the source text first, then decides the fence's form, its area basis and the standoff transfer together; discloses the expected baseline verdict change (≈ 4.09 against 4.05) and never tunes it; and restates round 1's 220 MW result under whatever form lands. The 1.15–1.83× shadow range is conditional and the truth can fall outside it in either direction.
- **Supersedes:** none; sharpens `goal.md` § Question's average-vs-peak framing and corrects the unsourced doc comment at `stellarator_plant.sysml:1139-1140`.
- **Accepted by:** round 1 review, 2026-09-04 (corrected from the proposed form, which generalised T-001's finding to the model's own source).

## L-004 — Check the previous pin before claiming an increment is new, and cite committed text for the claim

- **Evidence:** record § 8 (the one new reach is efficiency → `sustainment_ok`; `pre_wi039_indicators.json` beside `indicators.json`), § 14 Honesty (three claims cut back: the structural reach, the interior optimum, the constant-coupled newness), § 12 (36 shared points identical across the boundary); checkpoint C-001.r1 → r2 (the "not new" claim grounded on `860ce7d1`'s model text only when required).
- **Scope:** any increment that retires or restructures entry points on this package.
- **Implication:** an increment's "new" claims are checked against the previous pin's indicator run and its model text before publication; a claim in a permanent row cites committed text (`git show sha:path`), never a scratch-worktree run.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-04.

## L-005 (process) — A multi-field module's output declared as a store channel yields a silent blank column, now four times; the declaration-time guard has the recorded repeats ADR-0003 asks for

- **Evidence:** `20260821-power-cycle-ab#5`, `20260901-sustainment-fence#3`, `20260903-priced-levers#4`, `20260903-wall-and-heating#4` (record § 13, § 15 #4); `ANNEX.md` § Oracle names `pb__*`, `sustain__*`, `heat__*`.
- **Scope:** the evidence store on this package; any calc with more than one output.
- **Implication:** the declaration-time channel-shape guard proposed at `20260903-priced-levers#4` is minted owner-present as a coding-PM item under the run-study epic; until then every study definition exports multi-field outputs oracle-side.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-04.

## L-006 (process) — A study design that looks complete can hide two defects only execution finds: a transect anchored below its own fence, and two arms sharing a point

- **Evidence:** record § 11, § 15 #5, #6; `study.py` (`proposals()` raises on a shared point; `COUPLE_TARGET` re-anchored at the anchor's own 128.64 MW requirement).
- **Scope:** every study definition on this package.
- **Implication:** a study definition asserts no two arms share a point and reads a transect's held level off its anchor's own operands before its points run; when a re-execution follows a design defect, the first execution's `points.csv` is kept beside the record so the finding is evidenced rather than narrated.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-04.

## L-007 (process) — A goal whose § Answered when is a re-grade runs the re-grade as the round's last task, after the study reading is checkpointed

- **Evidence:** trail § T-004 return (decision 4), § T-005, § Round 1 result; `operating-point-closure` round 2 (T-006) as precedent; the reviewer's ruling (ii) in `evidence/round1_review.md`.
- **Scope:** any goal round whose answer condition is a rubric re-grade.
- **Implication:** a task cannot run outside an open round and the review never resumes a closed one, so a result placed before the re-grade would owe the goal's measurement rather than carry it. Candidate runbook clarification for the owner.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-04 (corrected to the claim and its reason, without the handoff narrative).

## L-008 — The clean-room near-miss can be a homograph surfacing in one result set, and the screen holds only when the prompt names it before any fetch

- **Evidence:** trail § T-001 return (decision 3); `knowledge/research/requests/runs/REQ-WALL-02/20260904T035641288429/run.jsonl` (the *Helios* planar-coil paper refused under PROTOCOL §3 without fetching, beside admissible *HELIAS* results); `evidence/T-001_REQ-WALL-0x_prompt.md:26-33`.
- **Scope:** every research request in the stellarator area while the hold-out stands.
- **Implication:** every stellarator-area research prompt names the Helios / HELIAS distinction explicitly, before any fetch; the registry guard fires at registration and cannot help.
- **Supersedes:** none; refines `priced-levers` L-005.
- **Accepted by:** round 1 review, 2026-09-04 (added by the reviewer: the round nominated it and the result dropped it).


## L-009 — Under the honest fence the printed heating level opens only by geometry, and only conditionally: nothing at the design's minor radius at any (R, I, T, n) in the window, and nothing by heating below a source efficiency of 0.92 at the design geometry

- **Evidence:** `exploration/stellarator_e2e/studies/20260904-wall-and-heating/record.md` § 4, § 6 `a`, § 15 #1 (`@9df54941`; Addenda `@9b1a4ef1`, `@a5b0b96a`); `synthesis.md` § 2.1, § 7 (i); `results/points.csv`: 0 feasible of the 501 a-1.3 rows in `arm-fence-p100` (ignited included); 257 feasible driven at a 1.5–2.2, cheapest `c1721` 212.460 (R 14.2, a 2.2, I 15 MA, T 16 keV, n 0.9×); on the grid column (R 12.7, I 15 MA, T 14.63, n 1.0×) the single feasible driven `a` is 1.7 (`c0821`, 257.35). The 0.92: of the 36 sustainment-alone points at 100 MW in `20260903-wall-and-heating/results/points.csv`, 9 pass the honest wall (average × 1.316440857 ≤ 4.05) and the least needs 92.11 MW coupled; this record's a-1.3 sustainment-alone floor is 100.78 MW (150 points). Recounted by the round-2 reviewer, agreeing on every number.
- **Scope:** the WI-041 pin `c1b0f0d1…`; windows R 11.2–17.2, a 1.3–2.2, I 13–18 MA, T 14.63–18 keV, n 0.6–1.0×; `eta_source` 0.50, `eta_couple` 1.00 (optimistic), τ*/τ_E 8. The 0.92 is at (R 12.7, a 1.3) on round 1's grid (I 14–17 MA, T 14.63–22 keV, n 0.9–1.2×); efficiency reaches only `sustainment_ok` at fixed wall-plug. Conditions, each disclosed at the claim site: the held ash-transport ratio (L-010); no bound or price on `a` (the optimum is the window's edge at both levels); the one-sided sustainment fence (every claim on the driven set); the calibration's constancy, bounded by the shadow (257 / 142 driven survivors at 1.15× / 1.83×, the optimum not among the 142). No buildability claim.
- **Implication:** no round spends a study on heating or field alone at the printed level; the next question is whether the `a` the model favours is a machine — the transport facts' aspect-ratio scaling (a research seam) and a bound on `a` (a model item) before any geometry result is more than conditional.
- **Supersedes:** none; refines L-001 with the honest fence in place.
- **Accepted by:** round 2 review, 2026-09-05 (corrected: the 0.92 scoped to the design geometry on round 1's grid; the a-1.3 count given with its denominator).
- **Update 2026-09-06** `[OWNER 2026-09-06, at the close of goal stored-energy-basis]`: the four conditions above stand as written. A fifth, surfaced after this goal's close and since measured: the reading is stored-energy-basis-sensitive. At the paper's own ash rule (WI-042, `work/completed/20260906_WI-042_sourced-helium-ash-profile/`; pin `ec984adc1572…`) the 257-point driven region at 100 MW mostly ignites (235 of 257), the driven set over this window falls to 131, the region's price and place move (cheapest driven 202.19 $/MWh on a restored 13 keV row at R 15.7, a 2.2; over this window alone 221.02), and the design column opens at exactly the pinned baseline point (49.08 MW against 50; peak 3.979; the ceiling at equality; coupling 1.00) and at no grid point. The new reading's own W-sensitivity has no second basis at the rule and stands as a disclosure at the rule's basis (`stored-energy-basis` `learnings.md` L-004, L-005; the `20260904-wall-and-heating#1` rows of 2026-09-05 and 2026-09-06 in `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`).

## L-010 — At a WI-037-class pin the peak wall load rises with `R` at fixed coil current and, at the source's own τ*/τ_E = 8, falls with `a` past the design point through the converged ash; neither pre-WI-037 reading transfers

- **Evidence:** record § 6 `R+tie`, § 6 `a`, § 6 `tau_ratio_ash`, § 15 #7, Addendum item 2; `results/points.csv` column (a 1.3, I 15 MA, T 14.63, n 1.0×, 100 MW): peak 3.752 / 4.179 / 4.541 / 4.846 / 5.102 over R 11.2 → 17.2 — R^0.72 end to end (local 0.86 / 0.74 / 0.65 / 0.56), 0.83 on the scan's 9.7–15.7 (`results/window_scan.json`); column (R 12.7, I 15 MA, T 14.63, n 1.0×): 4.179 → 3.346 over a 1.3 → 2.2 with He/n_e 0.110 → 0.236; `arm-transect-ash` (15 rows): through the scan's best point the wall fails and the plasma ignites at τ 6 (4.512, −61.5 MW) and sustainment fails at 12 (141.9 MW), feasible only at 8; the design-column anchor (the baseline, I 15.4 MA) reads 5.854 → 2.940 and −91.7 → +205.8 MW over 2 → 16. The reversal of the `a`-trend at τ*/τ_E = 4 (4.504 / 5.202 / 5.257 over a 1.3 / 1.8 / 2.2 at R 14.2, I 14 MA, T 16 keV, n 0.8×) is the pre-execution critique's oracle probe (`evidence/round2_T-004_precritique.md` F2), **not an executed point** — the record's two executed τ = 4 points (`c6307`, `c6297`) sit on different columns.
- **Scope:** the WI-041 pin; `iota_23` 0.92 and `f_suppr_ash` 0.50 held (Table-4 facts at A 9.8 carried to A 5.8–6.5; `f_suppr` enters only in the product with τ*/τ_E); the transect's five values per anchor leave the flips unlocated within a factor 0.75–1.5, and the executed optimum's column (a 2.2) is not on it.
- **Implication:** `20260829-p-pump-fence`'s "violated at every a ≥ 1.70" and its constancy in `R` are superseded for WI-037-class packages; any geometry sweep on this package declares `tau_ratio_ash`, `f_suppr_ash` and `iota_23` and states their constancy at the claim site; the τ = 4 reversal is a probe until a study executes it.
- **Supersedes:** `20260829-p-pump-fence` § 6 `a` for WI-037-class pins; closes the `goal.md` § Invariants open-measurement clause.
- **Accepted by:** round 2 review, 2026-09-05 (corrected: the τ = 4 clause marked as the critique's probe).

## L-011 — The lifetime chain prices the wall below its fence value and never bounds it

- **Evidence:** record § 15 #5, Addendum item 1; `synthesis.md` § 3.7; `results/points.csv`: the lifetime charge above the limit runs 0.00–28.03 $/MWh over the 2,667 wall-violated points; size-matched (p_net within ±10 % of the cheapest driven feasible point; wall-alone; driven) `c0716` (R 12.7, a 1.5, 14 MA, 18 keV, n 1.0×; 1.67× the limit, nine replacements) reads 185.92, 26.54 under `c1721` after a charge of 14.07 (0.53); at 220 MW `c3679` (same coordinates) reads 202.37, 17.08 under `c4639` after 15.07 (0.88); the cheapest driven wall-alone point `c1486` (178.73, 1.45×) pays 11.24; the cheapest point in the study `c2892` (147.90, 2.22×) fails beta as well. Availability is 0.85 at every replacement count. Recounted by the round-2 reviewer.
- **Scope:** one size-matched pair per heating level, not neighbours in design space (a 1.5, T 18, n 1.0× against a 2.2, T 16, n 0.9×) — a bound on the wall's price, not a derivative; the chain charges replacement capital only.
- **Implication:** the push-back the rubric names (the owner's 2026-09-04 reading) exists and is too weak to substitute for the fence; the Row-2b coupling (lifetime → availability) is the named follow-on, with a cost-basis review of the replaceable accounts beside it.
- **Supersedes:** none.
- **Accepted by:** round 2 review, 2026-09-05 (corrected: the pair's scope stated).

## L-012 (process) — A one-sided inequality passes points beyond the regime it fences; its feasible set is read only with the sign exported

- **Evidence:** record § 4, § 15 #4; `results/points.csv` `ignited` / `feasible_driven`: 787 ignited points per level; 201 of 458 "feasible" at 100 MW and 198 of 598 at 220; the cheapest feasible point allowing ignition (`c1680`, 200.27, −25.5 MW) undercuts the cheapest driven (212.46). Found by the pre-execution critique probing the oracle (`evidence/round2_T-004_precritique.md` F1, and F2–F4 likewise) where `indicators.json` reported only reachability.
- **Scope:** every study on this package while `sustainment_ok` is one-sided; any fence whose operand can cross zero.
- **Implication:** every study on this package exports `ignited` and reports `feasible_driven`; the pre-execution critique is given the oracle and told to attack the headline.
- **Supersedes:** none.
- **Accepted by:** round 2 review, 2026-09-05 (corrected to one claim; the critique practice carried in the implication).
