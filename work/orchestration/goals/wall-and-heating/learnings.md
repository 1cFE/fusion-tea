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

