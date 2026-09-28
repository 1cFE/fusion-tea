# Evidence map — Row 1 re-grade (pointers only)

**Author:** the WI-037 author (goal `operating-point-closure` round 2), 2026-09-01. Per the grading protocol § 2 this map carries pointers and no proposed scores; the grader cites what it actually read. The v1 map (`evidence-map.md`) still covers the other rows; this file adds the post-WI-037 Row-1 surfaces.

## The yardstick

- `rubric.md@dc0f0b6d` § Row 1 (the P ladder; the row's L3 anchor is the operative test) and § Grading protocol. **Provenance caution:** the row's gate note ("Rung C … a goal at this row proposes reopening it to the owner") is stale text — corrected at `.project/concepts/stellarator-demo-maturation.md` § Corrections — 2026-09-01, which is the authority; the rubric awaits its next owner-gated version. The anchors themselves are unaffected.
- Prior cell for the delta: `grading.md` § Row 1 (`R1.P` = 2, its `why_not_next`), and `R1.S` (`not_applicable`).

## Declared structure (canonical models/)

- `models/library/analyses/mfe_plasma_sustainment.sysml` — 'Plasma Sustainment' (the chain: line-averaged density, ISS04 closed form, A.5/A.6 damped ash fixed point with quasi-neutral fuel, composed radiation, required sustained heating; the doc carries the normative executable semantic and the discretization/convergence contract).
- `models/library/analyses/mfe_viability.sysml` — 'Sustainment Limit' (the power-limit constraint def, at the end of the file).
- `models/designs/generic_mfe/mfe_plant.sysml` — the `sustain` calc wiring (reads `magnet.B`, the derived field), the fusion/beta rebinds to `sustain.{n_D0,n_T0,n_He0,T_e0}`, the retired plant attributes (retirement comments in place).
- `models/designs/stellarator_09/stellarator_plant.sysml` — the two retirement notes (search "WI-037 retirement note"), the eight held sustainment facts with image-verified citation docs (search "Sustainment held facts"), the corrected `p_input` doc (plasma-coupled), and `assert constraint sustainment_ok` with its expected-violation disclosure.
- Codegen-seam rule reminder: the executable meaning is the handwritten impl — `exploration/stellarator_e2e/generated/handwritten/mfe_plasma_sustainment/plasma_sustainment_impl.py` (both the declaration and the impl are citable per the rubric's scoring rules).

## Runtime and executed behavior

- Package identity: `work/orchestration/goals/operating-point-closure/evidence/T-004_integration_return.json` (CANDIDATE, ten gates) — semantic `5b9abdfc…`, executable `41e06ecb…`, pin `35e922c5…`.
- Baseline: `exploration/stellarator_e2e/studies/20260901-sustainment-fence/results/baseline_result.json` — eight verdicts (`sustainment_ok` violated at the printed levers, disclosed/explained) and the sustain channels; the oracle-side per-point operands in `results/oracle_operands.csv` (the store's multi-field limitation, record § 13).
- Entry-point census: `tests/models/data/mfe_census.json` (n_D0/n_T0/T_e0/n_He0 absent; the eight held facts present; 193 entry points).

## Load-bearing study evidence

- `exploration/stellarator_e2e/studies/20260901-sustainment-fence/record.md` §§ 3, 4, 6, 8, 13, 15 + Addendum; `synthesis.md` (the administrator's independent recount — the reading of record); `results/points.csv`, `results/window_scan.json`.
- `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` — the `20260823-magnet-technology-ab#4` row history (sighting → unblocking → routing) and the four `20260901-sustainment-fence#…` rows.
- Round-1 physics validation (prototype, reviewer-reproduced): `work/orchestration/goals/operating-point-closure/evidence/T-002_prototype/NOTES.md` + trail § Round 1 review; goal `learnings.md` L-001..L-003.

## Item record and validation

- `work/active/WI-037_operating-point-closure/` — spec (amended 2026-09-01: forward-sustainment architecture; § Open decisions), design (D1–D8, esp. D6 tolerances with bases), plan § Implementation record + § MR-WI037-7 restatement.
- `modeling_project/VALIDATION_MATRIX.md` — SV-041/042/043 (amended descriptions) and status.
- Goal context: `work/orchestration/goals/operating-point-closure/goal.md` § Question / § Answered when; `learnings.md`; the trail's Round 2 strategy revision (the anchor reading it committed to: "links, not solves" — the grader weighs the anchor text itself, not the strategy's argument).
