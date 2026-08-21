# Synthesis

- **Role:** administrator (run-study skill, administer mode)
- **Date:** 2026-08-20
- **`snapshot.json` digest read:** nil — the directory has no `snapshot.json`
- **Record contract status:** pre-contract directory. No `record.md`, `snapshot.json`, `indicators.json`, or `results/`. The "is this a record" check was waived by the caller. Every file present was treated as the committed evidence.
- **Files read, with sha256 as read:**
  - `design_search_R_a.csv` — `0f248b83c104ee69b7ffa63c507d0be82be029b7e64def4a3d80e10166b8022b`
  - `availability_sweep.csv` — `9239bbcd7179ee39a9f187470757ae0389b5e9e1a99efd71d888ce0d50111a70`
  - `verification_summary.json` — `b4706e0b39a975a5ef87fbcb675aac023b7aff258f042f2f4e4135c6432e09e8`
  - `run_design_search.py` — `d14109596cbc9abcaa6cb67d3b2386409935b8c2d1cd55576d35f86c62f7d907` (read, not executed)
  - `make_report.py` — `0fb91762343d33dd3eb7995deee9995a54bc654286eedac0969602d0358130bf` (read, not executed)
  - `report.html` — `2b31b6451d2d73cfb93e25e06002459ca0d2ca9723c8d7421469ca7941e7f778`
  - `.gitignore` — one line, `_work/`

**How to read the evidence grades below.** Three kinds of file are in the directory and they carry different weight. The two CSVs and `verification_summary.json` are outputs: numbers I can recompute from. `report.html` is the executor's rendered account; its numbers trace to the CSVs through `make_report.py`, its prose does not. The two `.py` files are the executor's declared procedure: they say what was *meant* to run, and a script in a directory is not evidence that it ran. Where a claim rests only on a script or on report prose, I say so.

---

## 1. What the study set out to do

The directory carries no verbatim owner intake (no `record.md` § 2). The closest statement of purpose is the executor's own, in `run_design_search.py` lines 1-11 and `report.html` under "What this is":

- Run a first end-to-end design search on the stellarator demo model ("Stellaris, concept-09") through the stock teax study layer, with no hand-rolled sweep loop (`run_design_search.py` lines 4-7).
- Two studies:
  - **A.** A 2D grid over major radius R and minor radius a, recording LCOE and five viability verdicts per point (`run_design_search.py` lines 9-10).
  - **B.** A 1D sweep over availability at baseline geometry (`run_design_search.py` line 11).
- The script calls this "epic Item 5, first cut" (`run_design_search.py` line 5) and the report calls it "a proof of life" and "a first cut of the demo epic's design-search items, not their close-out" (`report.html`, "What this does not prove"). Which epic, and what Item 5 asked for, is not in the directory.

Whose words the goal is in — owner or executor — is not recorded. Everything above reads as the executor's framing of the task.

## 2. What it found

All numbers here are recomputed from the CSVs unless marked otherwise.

**Study A — the (R, a) grid** (`design_search_R_a.csv`, 948 data rows)

- Swept values: R from 4.0 to 20.0 m in 0.5 m steps (33 values) plus one off-grid point at R = 12.7; a from 0.80 to 2.20 m in 0.05 m steps (29 values). The script declares these windows at `run_design_search.py` lines 123-124.
- 947 grid points plus one appended baseline point (R = 12.7, a = 1.3). The script excludes 10 grid cells as geometrically invalid where R ≤ a + 2.25 (`run_design_search.py` lines 113-118, 326-331); 33×29 − 10 + 1 = 948, which matches the row count.
- 563 of 948 rows are feasible (all five verdicts satisfied), 59%.
- 385 verdict violations in total: 353 `wall_load_ok` violated, 32 `recirc_ok` violated. `beta_ok`, `tbr_ok`, and `net_positive` are satisfied on every row. No row violates more than one constraint.
- Baseline row: R = 12.7, a = 1.3, LCOE 275.2642200420774, feasible. This agrees with the pinned value the script carries (`PINNED_LCOE = 275.264220042`, `run_design_search.py` line 112) to every digit the pin states.
- Best feasible point: R = 14.0, a = 1.65, LCOE 208.999716608809 (−24% vs baseline), wall load 4.0354, fusion power 4880 MW, total capital 2.211e10. This is the same point `make_report.py` line 32 selects and `report.html` reports in its stat tile.
- Cheapest point regardless of feasibility: R = 9.0, a = 2.2, LCOE 162.93, wall load 5.459, `wall_load_ok` violated.
- Most expensive point: R = 4.0, a = 0.8, LCOE 7154.77 (`recirc_ok` violated).

**Study B — the availability sweep** (`availability_sweep.csv`, 19 data rows)

- Availability 0.500 to 0.950 in 0.025 steps at R = 12.7, a = 1.3 (windows at `run_design_search.py` line 125; geometry from `BASELINE`, line 111).
- LCOE falls monotonically from 455.10 to 247.56 across the 19 points. Every other recorded channel (wall load, fusion power, plasma volume, total/magnet/overnight capital) is constant across the sweep.
- All 19 rows are feasible. No verdict changes anywhere in the sweep.
- The 0.85 row reproduces the same LCOE as the study A baseline row, 275.2642200420774.
- `report.html` ("The availability sweep") says there is a "slope kink near 0.775" caused by "the scheduled-replacement count stepping (a ceiling function in the model)". The CSV supports a kink: the per-step LCOE change is −10.26 (0.725→0.750), then −8.18 (0.750→0.775), then −8.97 (0.775→0.800), so the step size is not smoothly decreasing there. The *cause* named in the report is not checkable from anything in the directory.

**Verification** (`verification_summary.json`)

- 12 rows sampled per study, seed 20260816, stratified by verdict combination with the remainder random.
- Five channels checked (lcoe, p_fus, magnet_capital, total_capital, wall_load) at tolerance 1e-9; worst relative deviation 5.67e-16.
- `verdicts_rederived: true`, `package_git_clean: true`.
- Its `glue_note` states that three glue-fed inputs (CAS27 per-point, cas28, n_mod) are identical by construction on both sides and not independently verified.
- Note on weight: the JSON is written by `run_design_search.py` lines 415-422 after that script's own asserts pass. `verdicts_rederived` and `package_git_clean` are literals the script writes on success (lines 419), not captured observations. The JSON existing is evidence the verify command ran to completion under the script as written; it is not an independent log of what each gate saw.

## 3. Framing verdict per axis

The record carries no framing table (no `record.md` § 5), and no file in the directory uses the `search | sensitivity` vocabulary. What follows is my reading from the data and the executor's own language, marked as such.

| Axis | Executor's language | What the data shows | Administrator's reading |
|---|---|---|---|
| R | "design search", "causal geometry lever" (`run_design_search.py` lines 9-10) | Feasible structure with a boundary: `wall_load_ok` flips along a, and `recirc_ok` fences the small-R, small-a corner (see § 4). | Consistent with a **search** framing. Not recorded as such by the executor. |
| a | same as R | same as R | Consistent with a **search** framing. Not recorded as such. |
| availability | "sweep", "operations lever" (`run_design_search.py` line 11) | LCOE responds monotonically; no constraint responds anywhere in the window; all non-LCOE channels are constant. | Consistent with a **sensitivity** framing. **No boundary claim is supported.** Whether an indicator run classified this axis as `no_constraint_response`, and whether the user ruled on it before execution, is not recorded (see § 6). |

Proposed-versus-judged framing, and whether it changed, cannot be recovered.

## 4. Constraint structure

Only short verdict names are recorded. The export deliberately truncates the qualified id: `short_verdicts` at `run_design_search.py` lines 298-299 keeps `cid.rsplit("__", 2)[-2]`. The qualified `constraint_id` and `source_local_identity` for every constraint are therefore not in the directory.

| Short name (as exported) | Status over study A (948 rows) | Status over study B (19 rows) | Where it goes violated (study A) |
|---|---|---|---|
| `wall_load_ok` | 353 violated, 595 satisfied | all satisfied | Every row with a ≥ 1.7 m, at every R from 4.0 to 20.0. Every row with a ≤ 1.65 is satisfied. The recorded wall load is at most 4.0354 on satisfied rows and at least 4.1647 on violated rows, so the bound sits between those two values. `report.html` states the limit as 4.05 MW/m² and calls it "sourced"; that number is not in any data file. |
| `recirc_ok` | 32 violated, 916 satisfied | all satisfied | R from 4.0 to 8.0 and a from 0.8 to 1.1 — the small-machine corner. The feasible a-band's lower edge rises as R falls: a ≥ 0.80 at R ≥ 8.5, a ≥ 0.85 at R = 7.5-8.0, up to a ≥ 1.15 at R = 4.0. `report.html` states the predicate as Q_eng ≥ 2; the script's verify step reads the threshold from a package input (`run_design_search.py` line 367). Neither the threshold value nor Q_eng itself is in the directory. |
| `net_positive` | all satisfied | all satisfied | Never violated in either window. |
| `beta_ok` | all satisfied | all satisfied | Never violated. `report.html` says beta is a bound design input whose verdict cannot move on these axes; the verify step re-derives it from two package inputs (`run_design_search.py` line 369). The inputs are not in the directory. |
| `tbr_ok` | all satisfied | all satisfied | Same situation as `beta_ok` (`run_design_search.py` line 370). |

The shape this gives, from the data alone: within the window, the feasible region is a band a ∈ [lower edge, 1.65] at every R, where the upper edge is set by `wall_load_ok` and is flat in R, and the lower edge is set by `recirc_ok` only for R ≤ 8.0. The best feasible LCOE sits on the wall-load edge (a = 1.65). LCOE keeps falling past that edge (cheapest infeasible point is at a = 2.2), which is what `report.html` means by the wall-load limit being "the active fence". That reading is supported by the CSV.

The five constraints are asserted in `report.html` to be "exactly what the model already asserted"; the directory has nothing that lists the model's constraint set independently of the CSV columns.

## 5. Findings carried forward

No findings register exists (no `record.md` § 15), so nothing has an id, a kind, a disposition, or a home. The items below are what the executor's files flag, plus process findings from this read. They are carried forward as candidates, unrouted, for whoever acts on this synthesis.

**Model-development findings the executor's files state**

- Availability has no constraint pushing back in the model. Nothing in either output changes except LCOE. What *should* push back is not named in the directory.
- No confinement-scaling constraint exists in the model, so nothing asks whether the assumed plasma is achievable at each geometry; profiles, heating power, cryo loads, and magnet shape factor are held at baseline at every point (`report.html`, "What this does not prove").
- Beta and TBR are bound design inputs; their verdicts cannot flip on any of the three axes (`report.html`, same section).
- The levelization calc lacks a guard for interest rate approaching inflation rate, which is why interest rate was not swept (`report.html`, same section).
- CAS27 special-materials capital cannot be wired cross-part in the package and is harness-supplied per point (`run_design_search.py` lines 36-45; `verification_summary.json` `glue_note`).
- The package has untied duplicated input keys beyond the three declared axes (interest rate ×4, operational years ×4, "and others"), so only R, a, and availability are safe to sweep (`report.html`, same section).
- Only single-field float channels land in the study store at this toolchain version; net electric power and Q_eng reach the record only through their verdicts (`run_design_search.py` lines 127-131; `report.html`).

**Process findings the executor's files state**

- The package runs under an era pin (teax commit `fa0e06a`, worktree `/home/reid/1cfe/teax-v1-era`) behind a scoped seal exception for two files (`run_design_search.py` lines 21-25, 29-33, 156-184; `report.html`, "Reproduce"). Regenerating on the current toolchain is described as parked upstream work.
- The sweep window is engineered by oracle pre-scan, and the 59% feasible fraction is a property of the window, not a finding about stellarators (`run_design_search.py` lines 120-122; `report.html`).
- The expansion-completeness check is name-based and cannot find semantic duplicates under different names; `magnet__R0` rides with R as a hand-declared tie (`run_design_search.py` lines 16-19, 217-224).
- Open items named by the executor: the instance-swap A/B study, the formal review and policy-ratification step, and the search-process animation (`report.html`, "What this does not prove").

**Process findings from this read, against the record contract** (the runbook says a fact the administrator cannot recover is a defect in the contract, not the read)

- The study was committed without any of the four contract files, so every fact in § 6 below is unrecoverable by construction. The directory is an output bundle, not a record.
- The export drops qualified constraint identity on purpose (`run_design_search.py` lines 298-299). The contract's § 4 requires recovering it; a future export should keep `constraint_id` and `source_local_identity` in the CSV.
- `verification_summary.json` writes gate outcomes as literals on success rather than as captured observations, so a reader cannot tell what the gates saw.

## 6. What the record does not support

Each entry is a fact the runbook expects an administrator to recover, or a claim the files make, that the directory does not carry. "Not recorded" means no file in the directory states it.

1. **Owner intake, verbatim.** No goal or scope in the owner's words. Not recorded.
2. **Study id, package name, execution date, and executor identity.** The script uses two internal ids (`stellarator-design-search-ra-v1`, `stellarator-availability-sweep-v1`, `run_design_search.py` lines 335, 342) and `report.html` is dated 2026-08-16 in its eyebrow line. No `<YYYYMMDD>-<goal-slug>` study id, no package path or `package_name` beyond the string `"stellarator_tea"` passed to a loader (line 269), no repo commit, no executor. Not recorded.
3. **Framing per axis, as proposed and as judged.** Not recorded. § 3 above is my reading, not the executor's.
4. **Indicator results.** No `indicators.json`. Whether any axis was classified `no_constraint_response` or `constraints_reachable`, whether any axis was proposed and declined, and the not-derivable disclosure, are all absent.
5. **User rulings on `no_constraint_response` axes.** The availability data shows no constraint responding. Whether an indicator said so, and whether the user ruled on that axis before any point ran, is not recorded.
6. **Pre-execution framing critique and all review outcomes.** No named lens, verdict, or disposition. `report.html` itself says "the formal review and policy-ratification step" remains open.
7. **Qualified constraint identities.** `constraint_id` and `source_local_identity` for all five constraints. Dropped on export (§ 4).
8. **Constraint bounds as values.** The wall-load limit (report prose says 4.05), the recirculation threshold, the beta limit, and the TBR floor are read from package inputs by the verify script and never written to the directory. The CSV brackets the wall-load bound between 4.0354 and 4.1647; it does not state it.
9. **Preflight gate outcomes as observations.** The baseline gate, key-validation gate, and git-clean gate are asserts in `run_design_search.py` (lines 229-234, 247-253, 348-358). What they observed is not logged. The only trace is `verification_summary.json`'s success literals and the CSV baseline row agreeing with the pinned constant. The manifest/package fingerprint gate and the suffix-sibling scan are not present in any form.
10. **Snapshot values.** No `snapshot.json`: no fingerprints (sealed, semantic, indicator-input), no manifest digest, no store compatibility tuple, no effective executable fingerprint, no artifact digests, no tool revisions, no teax revision beyond the short hash `fa0e06a` in a docstring.
11. **Verification tool revision and the oracle's identity.** The oracle is named `verify_stellaris.py` and imported from a parent directory (`run_design_search.py` lines 73-75). It is not in the directory, and no digest of it is recorded. The claim that it is "a line-by-line pure-Python mirror … written independently of the generated code" (`report.html`, "Verification") cannot be checked.
12. **Sample membership for verification.** Which 24 rows were sampled is reconstructible only by re-running the script with the seed. The rows are not listed.
13. **The per-point study store.** The `.db` files live under `_work/`, which `.gitignore` excludes. Per-point inputs, the full channel set, and the qualified verdicts are therefore not in the directory; only the exported CSV columns are.
14. **The glue ledger as values.** Three rungs are described in prose (`run_design_search.py` lines 27-45) and the report. No arm-scoped ledger with keys and digests exists; the two glue-edited package files and their hashes are not in the directory.
15. **Window provenance as a checkable value.** The script says the windows are "engineered … by oracle pre-scan" (lines 120-122). What was scanned and what the scan showed is not recorded.
16. **The cause of the availability kink.** `report.html` attributes the slope change near 0.775 to a ceiling function in the replacement schedule. The CSV shows the kink; nothing in the directory shows the mechanism.
17. **Cross-fingerprint correlation.** With one arm per study and no fingerprints recorded, there is nothing to state and no explicit nil is recorded either.
18. **Model-development finding ids, dispositions, and homes.** Every finding in § 5 is unrouted because no register exists. No `DISCOVERY_LOG.md` rows can be joined to this directory.
19. **The model's constraint set, stated independently of the output.** `report.html` says the five constraints are "exactly what the model already asserted". The directory has no model artifact, contract, or manifest to confirm the set or its predicates.
20. **Evidence that the scripts ran as written.** The two `.py` files are procedure, not log. The CSVs and JSON are consistent with the scripts having run (row counts, baseline value, column names), but there is no run log, stdout capture, or timestamp tying a given script revision to a given output.
