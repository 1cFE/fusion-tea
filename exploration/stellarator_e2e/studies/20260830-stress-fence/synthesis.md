# Synthesis — 20260830-stress-fence

- **Administrator:** fresh administrator subagent, 2026-08-30
- **Date:** 2026-08-30
- **snapshot.json sha256 read:** `98209df3ef1326dc4f6d35054ac0cfaa8dad515bf0d04ee5e960eb0d1e4c1efb` (recomputed by this administrator; matches `record.md` § 16)

This synthesis is written from the record directory only: `record.md`, `snapshot.json`, `indicators.json`, `axes.json`, `study.py`, and `results/*`. Facts are labeled recorded, recounted (recomputed here from committed artifacts), or the administrator's interpretation.

## What the study set out to do

The owner's question, quoted verbatim in `record.md` § 2: where does the new structural fence bind in (R, a, B) space, and do feasibility and the constrained optimum move once field is derived rather than cited.

The executor's marked additions (`record.md` § 2): the B axis is executed as `I_coil` (the WI-035 lever; B = k·I at fixed geometry), the `a` axis is declined and held at 1.3 m so the grid matches the `20260829-p-pump-fence` comparand's row, and coil sizing runs as a second arm — a 1-D `wp_side` transect at the baseline to locate the `wp_stress_ok` flip.

Two arms in one store (`record.md` § 1, `snapshot.json` arms[]): `arm-grid-R-I` (R 4.0–20.0 step 0.5 × I_coil 2.0–26.0 MA step 0.5, wp_side held 0.36 m) and `arm-transect-wp-side` (wp_side 0.20–0.52 m step 0.02 excluding 0.36, at the baseline point). Both windows are declared `engineered`, chosen after the oracle scan in `results/window_scan.json`.

## What it found

- Baseline (R 12.7 m, I_coil 15.4 MA, wp_side 0.36 m): LCOE **304.482 $/MWh**, feasible on all seven constraints. Recounted: `results/points.csv` baseline row and `results/baseline_result.json` both give 304.48161969642837, matching the manifest pin copied into `snapshot.json`.
- Constrained minimum over the feasible grid: **236.634 $/MWh at (R = 20.0 m, I_coil = 18.0 MA)**. Recounted from `results/points.csv`: min feasible LCOE = 236.63382224068812 at exactly that point.
- The optimum sits on the `beta_ok` floor at the R window edge. Recounted: at (20.0, 17.5 MA) `beta_ok` is violated; (20.0, 18.0 MA) is the lowest feasible I in that column.
- LCOE falls monotonically toward large R along the floor. Recounted: per-R minimum feasible LCOE decreases strictly from 341.1 (R 8.0) to 236.6 (R 20.0), with 243.1 at R 17.5 and best I rising 16.0 → 18.0 MA over R 17.5 → 20.0 — the § 3 numbers reproduce.
- The record itself scopes the optimum claim (`record.md` § 3): the R = 20 corner is the engineered window's edge, and the decomposed magnet capital does not grow with R at fixed I (held `c_coil`, finding #1), so "optimum at large R" is a statement about this package inside this frame, not a design recommendation.
- The binding ceiling changes identity along R: conductor limit (`peak_field_ok`) for R ≤ 15.0 m, both ceilings at 15.5–16.0 m, stress limit (`wp_stress_ok`) alone for R ≥ 16.5 m. Recounted exactly from `results/points.csv` by checking which constraint is violated at the first grid point above each R's feasible I band.
- Feasibility begins at R = 8.0 m; every point at R ≤ 7.5 violates `recirc_ok` at every I. Recounted; and `results/oracle_operands.csv` shows rec_frac is a single value per R (I-invariant), crossing the 0.5 threshold between R 7.5 (0.5106) and R 8.0 (0.4826) — the kill is recirculation economics, and the field window there is open (2–5 points per low-R row satisfy the three field fences, recounted).
- The `wp_side` transect flips `wp_stress_ok` **between 0.28 m (835.7 MPa, violated) and 0.30 m (780.0 MPa, satisfied)**. Recounted from `results/points.csv` (sigma_wp 835.7e6 / 780.0e6 Pa); 5 of 16 transect points infeasible, all below the flip; the closed form 650 × 0.36 / 800 = 0.2925 m lands inside the bracket; `results/window_scan.json` `wp_side_transect` shows the same flip.
- Along the whole transect LCOE and the decomposed magnet capital are constant (304.482 $/MWh, 5.401032e9). Recounted — this is the executed evidence behind finding #2 that `wp_side` is cost-free in this package.
- Administrator recount, not stated in the record: 201 of 1,617 grid points are feasible (12.4%).
- Administrator's interpretation: the § 6 claim "the band at R 12.7 is I ∈ [11.5, 15.0] MA on the grid" is loose — R = 12.7 is not a grid row; the [11.5, 15.0] band is the R = 12.5 grid row's (recounted exactly). The off-grid baseline at (12.7, 15.4 MA) is feasible on the conductor fence as stated.

## Framing verdict per axis

All three swept axes were proposed `search` and judged `search`, unchanged (`record.md` § 5).

- `I_coil` — search, upheld: a two-sided feasible band (beta floor below, conductor/stress ceiling above) at every feasible R. Recounted: bands exist at every R ≥ 8.0 and the floor is `beta_ok` at each.
- `R+tie` — search, upheld: fence structure in R (recirc kill at low R, band widening with R, ceiling identity handover at R ≈ 16 m). Recounted as above.
- `wp_side` — search, upheld: the boundary was found where sought (flip between 0.28 and 0.30 m). Recounted.
- Declined axes: `a` (held 1.3 m, the comparand row), `availability` (held 0.85), `discount_rate` (held 0.07). The last two traced `no_constraint_response` in `indicators.json` (recounted: `constraints_reachable` empty, `no_constraint_response` true for both); neither was executed, so no ruling was owed under the fail-closed condition of the runbook's step 4, and the record says why no new model-gap finding is minted (§ 8).

## Constraint structure

Grid = 1,617 points, transect = 16, baseline appended once, 0 excluded (`record.md` § 4). Recounted: `results/points.csv` has 1,634 rows (1,617 grid + 1 baseline + 16 transect); `results/excluded_points.csv` is header-only; `results/verification_summary.json` cases_total = cases_completed = 1634.

All seven § 4 verdict counts reproduce exactly from `results/points.csv` (grid excluding the baseline row; transect separately):

| constraint | recorded | recounted |
|---|---|---|
| `beta_ok` | violated 586 / satisfied 1031 (grid) | 586 / 1031 — match; transect all 16 satisfied |
| `net_positive` | satisfied 1617 + 16 | match |
| `peak_field_ok` | violated 772 / satisfied 845 (grid) | 772 / 845 — match; transect all satisfied |
| `recirc_ok` | violated 392 / satisfied 1225 (grid) | 392 / 1225 — match |
| `tbr_ok` | satisfied everywhere | match (structurally inert, held-vs-held per the record) |
| `wall_load_ok` | satisfied everywhere in-window | match |
| `wp_stress_ok` | violated 660 / satisfied 957 (grid); violated 5 / satisfied 11 (transect) | 660 / 957 and 5 / 11 — match |

Structure, as recorded in § 4/§ 6 and confirmed by recount: `recirc_ok` is the sole killer of R ≤ 7.5; `beta_ok` is the floor of every feasible band; `peak_field_ok` is the ceiling through R 15.0; `wp_stress_ok` is the binding ceiling from R 16.5 up (shared at 15.5–16.0). The bounds in `results/oracle_operands.csv` are constant across all 1,634 rows (beta 0.05, wall load 4.05, B_max 24.9 T, sigma_allow 800 MPa, recirc 0.5).

Baseline-on-fence statement (`record.md` § 13): B_peak 24.899999999999995 vs B_max 24.9, by construction (design D2), disclosed as a design fact; stress margin 23% at baseline. Recounted: the two operand values reproduce from `results/points.csv` and `results/oracle_operands.csv`, and (800 − 650)/650 = 23.1%. The recorded margin figure "5.3e-15 T" does not reproduce: 24.9 − 24.899999999999995 = 3.55e-15 in float64. Administrator's interpretation: both figures are ulp-scale and the claim's substance (on-fence by design) stands; the stated digit is wrong.

Verification (`record.md` § 13, `results/verification_summary.json`): outcome pass; 12 rows sampled stratified over 9 observed verdict combinations; 12 channels vs the package-owned oracle, worst relative deviation 4.37e-16; all seven constraints re-derived from published operand bindings with zero verdict mismatches; `not_independently_verified` empty. The summary's own sha256 matches `snapshot.json` arms[].verification.summary_sha256 (recounted). The record states what verification did not cover: the 1,622 unsampled rows, and the sourcing of the held coil-set facts (the oracle mirrors the model's literals).

Preflight (`record.md` § 9, `results/preflight_results.json`): all six gates ran, all pass — declared keys (7 across 6 groups), sibling scan, identity (sealed digest `75f90a24…` recomputed, zero glue), manifest currency, baseline headline (relative deviation 0.000e+00, 7/7 verdicts), package git-clean. Recounted: the preflight file's recorded input digests match this directory's `axes.json`, `results/package_identity.json`, and `results/baseline_result.json` hashes.

Integrity recount: every artifact digest in `snapshot.json` arms[].artifacts matches the file on disk (all 8 results files), and `indicators.json` and `axes.json` match their snapshot-recorded digests. Route per § 10: study-local direct-API (`study.py`, committed in this directory), no adapter, glue ledger none — consistent with `results/package_identity.json` (empty allowed-modified and adapter lists).

## Findings carried forward

From `record.md` § 15, both `model` kind, both `unrouted` (stated home: modeling item under the MFE Cost Modeling epic):

- `20260830-stress-fence#1` — the decomposed magnet capital does not respond to R at fixed I (held `c_coil` = 25 m winding circumference over a 5× size range; `f_set` held); the optimum-in-R claim rides partly on a cost-decomposition artifact. Disclosed at the claim sites (§ 3, § 11).
- `20260830-stress-fence#2` — `wp_side` reaches zero objectives: it moves only the stress operand, so escaping the stress fence by enlarging the pack is cost-free, which no real design change is. The zero-objective indicator trace is in `indicators.json` (recounted: `objectives_reachable` for `wp_side` is empty) and the flat transect LCOE/magnet-capital columns in `results/points.csv` are the executed evidence.

Review outcomes (§ 14): one pre-execution framing critique, findings none blocking — 1 MAJOR (the R-optimum confound, disposed by scoping the claim and minting the finding) and 6 minor/info, each with a stated disposition landing in § 3, § 6, § 8, § 11, or § 13.

Internal inconsistency, administrator-found: § 14's disposition says the held-`c_coil` gap was "minted as finding `20260830-stress-fence#3`", but the § 15 register carries only #1 and #2, and #1 is the c_coil gap (§ 3 also cites #1 for it). The administrator's reading is that "#3" in § 14 is a stale number for what became #1; the record does not say so itself. This is a defect in the record, filed here as a process observation against the record contract.

## What the record does not support

- The comparand agreement claim — "identical per-R to the comparand (99/99 verdict agreement)" for the three field-independent fences (§ 4, § 6) — cannot be verified from this directory: no `20260829-p-pump-fence` rows are in the record. Recorded claim, unverifiable here by design (only paths inside the record may be read).
- Whether the two findings' first-sighting rows actually exist in `DISCOVERY_LOG.md` — the log is outside the record. § 15 asserts the ids are used verbatim there; unverifiable here.
- The pre-execution critique document itself — § 14 records its verdict and dispositions, but the critique text is not a committed artifact in this directory.
- The exact § 14 finding id ("#3") — contradicted by § 15 as noted above; which numbering was intended is not recoverable from the record.
- The § 13 margin figure 5.3e-15 T — does not reproduce from the recorded operands (recomputed 3.55e-15 T); the correct digit is not recoverable from the record beyond the administrator's recomputation.
- The per-point store (`_work/.../20260830-stress-fence.db`) — outside the record and uncommitted, as § 17 states; `results/points.csv` and `results/oracle_operands.csv` are the committed per-point evidence and were sufficient for every recount above.
- The package path is spelled two ways inside the record: `exploration/stellarator_e2e/pkg/stellarator_tea` (`snapshot.json` package and indicators sections; the verify command) and `exploration/stellarator_e2e/generated` (`results/package_identity.json`, `results/preflight_results.json` inputs, `results/verification_summary.json` package block). All fingerprints agree (`75f90a24…` throughout), so the administrator's reading is that both names resolve to the same sealed tree, but the record never says so.
- `results/verification_summary.json` records `teax.revision` as "unrecorded"; `snapshot.json` carries `744745f8…`. The snapshot value is the committed one; the summary's gap is noted as found.
- Everything § 17 already declares absent: no (R, a) plane (a held 1.3 m — the wall-load fence is never located here), no availability or discount-rate response, no magnet-capital-vs-R response (absent by construction, finding #1), no absolute-LCOE comparison across the WI-035 re-baseline (333.067 → 304.482 headline shift is recorded but the pre-WI-035 side is not in this directory), and no confinement response to field — "the optimum sits on the beta floor" is a fact about this package.
- The sourcing of the held oracle/model literals (`k_link`, `k_sigma`, `f_set`, `c_coil`) — § 13 states this lives in the WI-035 item record, outside this directory; verification here covers transcription and execution only.
