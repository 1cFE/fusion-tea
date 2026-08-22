# Synthesis — 20260821-power-cycle-ab

- **Administrator:** Claude (fresh session, administer mode; no memory of the run)
- **Date:** 2026-08-22
- **`snapshot.json` sha256 as read:** `3df983550962be1963b460ea4f64a7b24969dad4bfdfd5fd57166b7d0fc2d34c` (matches `record.md` § 16)
- **Read:** only files inside this record directory, plus the run-study skill files and `STUDY_POLICY.md` for vocabulary. Nothing else.

How to read this file. Three kinds of sentence appear, kept apart:

- **Recorded** — a fact with a file in this directory behind it. Each one cites the file.
- **Not recorded** — a fact the record does not carry. Collected in the last section.
- **Administrator's reading** — my own interpretation, always labeled as such, with the evidence it rests on.

Every number below that is not quoted from `record.md` was recomputed by me from `results/points.csv` or read from a `results/*.json` file. Where my recomputation disagrees with `record.md`, I say so.

---

## 1. What the study set out to do

**Owner's intent, verbatim** (`record.md` § 2, lines 19–21):

> Compare steam Rankine against sCO2 on the stellarator
> Run sensitivity analysis on other axes for each type
> Try to find a non-intuitive result on the interactions

**How the executor made that runnable** (`record.md` § 2, lines 25–31; marked there as the executor's own):

- "Rankine" and "sCO2" became four fixed value triples of (`eta_th`, `turbine__cost_per_mw`, `heat_rejection__cost_per_mw`), one per arm (`study.py` lines 34–43; `snapshot.json` `arms[].window.bounds.cycle_block`):

  | Arm | `eta_th` | turbine $/MW | heat rejection $/MW |
  |---|---|---|---|
  | `arm-rankine-paper` | 0.333 | 202 840 | 35 060 |
  | `arm-rankine-upstream` | 0.40 | 202 840 | 35 060 |
  | `arm-sco2-eta-only` | 0.47 | 202 840 | 35 060 |
  | `arm-sco2` | 0.47 | 159 080 | 22 580 |

- "Other axes" became `R`, `a`, `availability`, `discount_rate`. The two economic axes were traced, came back `no_constraint_response`, and were declined by the owner before any point ran (`record.md` § 8, lines 155–156). Only `R` and `a` were swept.
- The same (R, a) grid ran under each of the four arms: 33 R values × 29 a values, masked by R > a + 2.25 m, plus the baseline geometry (R 12.7, a 1.3) — 948 points per arm, 3 792 total (`snapshot.json` `arms[].window.bounds.validity_mask`; `results/points.csv` has 3 792 data rows).

**Package and route** (recorded): sealed package `stellarator_tea`, executable fingerprint `7447efea…`, no adapter, glue ledger empty (`results/package_identity.json`; `snapshot.json` `arms[].effective_executable_fingerprint`, `glue_ledger_none: true`). Route: study-local direct API over the stock teax lifecycle (`record.md` § 10, line 192; `study.py` lines 130–136).

---

## 2. What it found

### 2.1 LCOE per arm

Objective channel: `stellarator_09__stellaris__lcoe_calc__lcoe`, $/MWh (`record.md` § 3, line 35; `snapshot.json` `manifest.content_used.objective_catalog[0]`). A second form, `stellarator_09__stellaris__lcoe_1cfe_calc__lcoe`, is exported as the `lcoe_1cfe` column of `results/points.csv`.

Recomputed by me from `results/points.csv` (columns `arm_id`, `R`, `a`, `lcoe`, `feasible`); all four rows agree with `record.md` § 3 lines 40–43 to the digits shown there.

| Arm | LCOE at (R 12.7, a 1.3) | Best feasible LCOE | at (R, a) | Feasible points of 948 |
|---|---|---|---|---|
| `arm-rankine-paper` | 275.264 | 209.000 | (14.0, 1.65) | 563 |
| `arm-rankine-upstream` | 229.191 | 176.477 | (13.5, 1.65) | 578 |
| `arm-sco2-eta-only` | 196.299 | 152.787 | (13.0, 1.65) | 585 |
| `arm-sco2` | 194.638 | 151.187 | (13.0, 1.65) | 585 |

The `arm-rankine-paper` value at the baseline geometry equals the pinned baseline headline 275.2642200420774 (`results/baseline_result.json` `channels`; `snapshot.json` `manifest.content_used.baseline.headline`).

Ordering `arm-sco2` < `arm-sco2-eta-only` < `arm-rankine-upstream` < `arm-rankine-paper` holds at all 948 grid points (recomputed; `record.md` § 3 line 45 says the same).

### 2.2 Splitting the sCO2 difference (the fourth arm's job)

Recomputed from `results/points.csv`:

- At the baseline geometry, η 0.40 → 0.47 with Rankine rates is −32.89 $/MWh (−14.35 %); the sCO2 rates on top of that are a further −1.66 $/MWh (−0.85 %). `record.md` § 3 line 45 gives −32.9 / −14.4 % and −1.7 / −0.8 %, consistent.
- Over points feasible in both arms, the rate effect is −0.48 % to −1.06 % and the efficiency effect −13.3 % to −23.4 % (`record.md` § 3: "−0.5 % and −1.1 %", "−13.3 % and −23.4 %"; consistent).
- Over *all* 948 points, the rate effect reaches −1.33 % (at (5.5, 2.2), an infeasible point). `record.md` § 6 line 125 says "at most 1.1 % of LCOE anywhere in the window". That sentence holds for the feasible region, not the whole window. Minor overstatement; the conclusion it supports (the efficiency dominates the rates) is unaffected.

### 2.3 The two results offered against the owner's third bullet

Both are stated in `record.md` § 6 lines 124–125 as facts of the run, and both reproduce from `results/points.csv`:

- Total capital (`total_capital` column) rises with η at every one of 948 points: paper < upstream < sco2-eta-only. `arm-sco2` has higher total capital than `arm-rankine-upstream` at every point despite cheaper rates. The record's mechanism (CAS23 priced per MWe) is the executor's explanation; the CSV shows the ordering, not the mechanism.
- The efficiency gain is largest where recirculation is heaviest: −43.2 % at (4.0, 0.8), −19.6 % at (6.0, 1.0), −14.4 % at baseline, −13.5 % at (20.0, 1.5). Matches `record.md` § 6 line 125.

**Administrator's reading.** Neither result reverses anything; both are monotone consequences the record itself calls mechanisms of the model. Whether they count as "non-intuitive" is the owner's call. The record says plainly that "nothing non-intuitive found" was an acceptable answer (`record.md` § 2, line 30), and reports no reversal (`record.md` § 17, line 267).

### 2.4 Shape of the objective

- Falls with `a` at every R in every arm toward the wall-load fence; the unconstrained minimum of every arm sits at a = 2.2 with `wall_load_ok` violated (recomputed: (9.0, 2.2) paper, (8.5, 2.2) the other three; `record.md` § 3 line 45 says "a = 2.2, R 8.5–9.0 m").
- Along the a = 1.65 fence, the minimum in R is interior and shallow. Recomputed: LCOE at R 13–15 on the fence lies within 0.16 $/MWh of the arm minimum for paper, 0.17 for upstream, 0.25 for sco2-eta-only, 0.26 for sco2. `record.md` § 3 line 45 says "within 0.1 $/MWh over R 13–15 m" — that is tighter than the data; the four best feasible points of each arm are within 0.055 / 0.076 / 0.062 / 0.068 (`record.md` § 6 line 92 says "within 0.07"; upstream is 0.076). Both are small overstatements of a correct qualitative claim: the optimum is shallow.

---

## 3. Framing verdict per axis

Recorded in `record.md` § 5 (lines 66–82). The arms share one framing table; nothing in the record frames an axis differently per arm, and the arms differ only in the three block values (`study.py` lines 59–71), so the per-arm framing is the same row four times. The table below is the record's; the last column is mine.

| Axis | Indicator (`indicators.json` `groups[].no_constraint_response`, `constraints_reachable`) | Proposed | Judged | Changed? | Administrator's check against `results/points.csv` |
|---|---|---|---|---|---|
| `R` | reachable: `net_positive`, `recirc_ok`, `wall_load_ok` | search | search | no | Verdict structure present: `recirc_ok` violated in a small-R corner whose extent differs by arm; constrained optimum interior in R in every arm. Supported. |
| `a` | reachable: same three | search | search | no | `wall_load_ok` violated at every a ≥ 1.70 for every R in every arm; never at a ≤ 1.65. Supported. |
| `availability` | `no_constraint_response: true` | sensitivity | not run | — | Held at 0.85 in all 3 792 rows (`availability` column). Declined by owner ruling "no sensitivity" (`record.md` § 8 line 155). No framing to judge. |
| `discount_rate` | `no_constraint_response: true` | sensitivity | not run | — | Held at 0.07 in all 3 792 rows. Same ruling (`record.md` § 8 line 156). |
| cycle block (the arms) | reachable: `net_positive`, `recirc_ok` | search | search | no | The block moves only the `recirc_ok` verdict (22 points flip between extreme arms, all in R 4.0–8.0, a 0.80–1.10); every other verdict column is identical across arms at every point. Supported. |

**Policy § 7 H1 band.** The record claims feasible fraction 59–62 % per arm (`record.md` § 5 line 78). Recomputed: 563/948 = 59.4 %, 578/948 = 61.0 %, 585/948 = 61.7 %, 585/948 = 61.7 %. Inside 5–95 %.

**The two declined axes carried the obligations the policy attaches to `no_constraint_response`:** an owner ruling (recorded verbatim, `record.md` § 8 lines 155–156) and a model-development finding each (`record.md` § 8 lines 171–172; findings #1 and #2). An oracle scan of both axes at the baseline geometry exists (`results/oracle_scan.json`: availability 0.50–0.95 moves LCOE 455.1 → 247.6 in the paper arm; discount rate 0.03–0.12 moves it 163.0 → 485.4; no verdict changes). That scan covers three arms, not four, and is not a package run (`results/oracle_scan.json` `note`).

---

## 4. Constraint structure

### 4.1 Identities

Six executing constraints. Qualified identities from `results/baseline_result.json` `verdicts[]` (which also carries `definition_qualified_name`); the same six appear in `results/verification_summary.json` `constraints_rederived[]` and in every `indicators.json` group.

| `constraint_id` | `definition_qualified_name` | `source_local_identity` | Operator, operands (`indicators.json`) |
|---|---|---|---|
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `mfe_viability::'Beta Limit'` | `beta_ok` | `beta_calc__beta` ≤ `beta_limit` |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `mfe_viability::'Net Power Positive'` | `net_positive` | `pb__p_net` > 0.0 |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `mfe_viability::'Conductor Peak Field Limit'` | `peak_field_ok` | `peak_field_calc__B_peak` ≤ `magnet__B_max` |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `mfe_viability::'Economic Recirculating Threshold'` | `recirc_ok` | `pb__rec_frac` ≤ `recirc_ok__threshold` |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `mfe_viability::'TBR Floor'` | `tbr_ok` | `tbr` ≥ `tbr_floor` (bound vs bound) |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `mfe_viability::'Neutron Wall Load Limit'` | `wall_load_ok` | `wall_load_calc__wall_load` ≤ `wall_load_limit` |

The export carries verdicts under the short names only (`results/points.csv` columns `beta_ok` … `wall_load_ok`; `study.py` line 119 `short_verdicts`). The qualified identity is recoverable because `results/baseline_result.json` and `results/verification_summary.json` both list the six `constraint_id` ↔ `source_local_identity` pairs, and `record.md` § 4 does the join. I have taken that join as recorded.

### 4.2 Outcome per arm

Recomputed from `results/points.csv`. No verdict is `indeterminate` anywhere (0 non-`satisfied`/`violated` cells in 3 792 × 6). Matches `record.md` § 4 lines 53–60.

| Constraint (`source_local_identity`) | `arm-rankine-paper` | `arm-rankine-upstream` | `arm-sco2-eta-only` | `arm-sco2` |
|---|---|---|---|---|
| `beta_ok` | satisfied, 948/948 | satisfied, 948/948 | satisfied, 948/948 | satisfied, 948/948 |
| `net_positive` | satisfied, 948/948 | satisfied, 948/948 | satisfied, 948/948 | satisfied, 948/948 |
| `peak_field_ok` | satisfied, 948/948 | satisfied, 948/948 | satisfied, 948/948 | satisfied, 948/948 |
| `recirc_ok` | violated at 32 (R ≤ 8.0 at a 0.8; vanishes above a 1.10) | violated at 17 (R ≤ 6.5; above a 1.00) | violated at 10 (R ≤ 5.5; above a 0.95) | violated at 10 (identical to eta-only) |
| `tbr_ok` | satisfied, 948/948 | satisfied, 948/948 | satisfied, 948/948 | satisfied, 948/948 |
| `wall_load_ok` | violated at 353 (every a ≥ 1.70) | violated at 353 (same points) | violated at 353 (same points) | violated at 353 (same points) |

Three verdict combinations occur, each in every arm: all satisfied; only `wall_load_ok` violated; only `recirc_ok` violated. No point violates both (recomputed; `record.md` § 4 line 60).

Cross-arm identity (recomputed): the `wall_load`, `p_fus`, `magnet_capital`, and `beta` columns are identical across the four arms at every point, and so are the `beta_ok`, `net_positive`, `peak_field_ok`, `tbr_ok`, `wall_load_ok` verdict columns. Only `recirc_ok` differs, and the two η 0.47 arms agree on it at every point. This is what `record.md` § 6 line 120 claims.

**Administrator's reading of why.** `indicators.json` `groups[cycle_block].constraints_reachable` lists only `net_positive` and `recirc_ok`; `beta_ok`, `peak_field_ok`, `tbr_ok`, `wall_load_ok` are under `constraints_unreachable` for that group. So the run's cross-arm identity on those four is what the trace predicted. The record states this as a structural limit (`record.md` § 4 line 60, § 17 line 266). I agree the record could not have found a cycle interaction with those constraints; that is a property of the model's dependency graph as traced, not a result.

Wall load at the fence (recomputed, identical across arms): 4.0354 MW/m² at a = 1.65, 4.1647 at a = 1.70 (`results/points.csv` `wall_load` column). The limit value 4.05 is stated in `record.md` § 4 line 58 but appears in no result artifact as a number; see § 6 below.

### 4.3 Store and fingerprints

- All four arms ran in one store, `store_id` `20260821-power-cycle-ab` (`snapshot.json` `arms[].store_id`, `stores[0]`). Every `arms[].store_id` resolves into `stores[]` (checked).
- All four arms carry the same `effective_executable_fingerprint.value` `7447efea9f20…`, `no_adapter: true` (`snapshot.json` `arms[]`). The store's compatibility tuple carries the same executable fingerprint and semantic fingerprint `1ca93d0c988c…` (`snapshot.json` `stores[0].compatibility_tuple`; `results/verification_summary.json` `stores[0].compatibility`). One fingerprint, shared. `record.md` § 12 discharges the cross-fingerprint nil on that condition; I confirm the condition holds in the snapshot.
- Every `manifest.content_used.fingerprint_names` entry has a key under `fingerprints` (checked). `indicators.axis_declaration.subset` is `false` (`snapshot.json`).
- Every artifact digest in `snapshot.json` `arms[].artifacts`, plus `indicators.json` and `axes.json`, matches the bytes on disk as I read them (checked by sha256).

### 4.4 Gates and verification

- Preflight: six gates, all `pass`, outcome `pass`; sibling scan reports 2 warnings (`electric_plant__cost_per_mw`, `misc_plant__cost_per_mw`) (`results/preflight_results.json` `gates[]`). Baseline headline reproduces at relative deviation 0; 6/6 verdicts match.
- Post-run: package tree git-clean, `pass` (`results/postrun_clean.json`).
- Verification: 12 of 3 792 cases sampled, 3 strata, 10 channels compared at tolerance 1e-9, worst relative deviation 4.0e-16, six verdicts re-derived, `verdict_mismatches: []`, outcome `pass` (`results/verification_summary.json`).
- The sample's per-arm split 3 / 1 / 6 / 2 (`record.md` § 13 line 221) is not a field of the summary. It follows from the sampled case ids and arm-major case order (948 per arm, in the order of `study.py` lines 35–43); I reproduced the same counts that way. It is an inference from two artifacts, not a recorded value.

---

## 5. Findings carried forward

From `record.md` § 15 (lines 243–248). Six findings. None is arm-specific by its text; the column "arms it bears on" is my reading.

| Id | Kind | One line | Home (as recorded) | Arms it bears on (administrator's reading) |
|---|---|---|---|---|
| `#1` | model | Nothing couples availability to core lifetime / replacement outage; the model accepts any capacity factor at any wall load (`no_constraint_response`). | unrouted — candidate modeling item | all four equally; the axis was held at 0.85 in every row |
| `#2` | model | Discount rate is a free multiplier; nothing couples it to construction duration, capital mix, or financing (`no_constraint_response`). | unrouted | all four equally; held at 0.07 in every row |
| `#3` | model | `p_pump` = 1.0 MW held in every arm is far below helium-primary circulator figures; suppresses `rec_frac` in every arm equally, so the A/B is unbiased but `rec_frac` is understated everywhere. | research round (path cited in record) | all four; the `recirc_ok` fence positions in § 4.2 above are conditional on this value |
| `#4` | process | The oracle seam's key map had to grow by four entries before scan/verify could run. | documented seam (path cited in record) | n/a — tooling |
| `#5` | process | `pb__p_net` and `pb__rec_frac` are not recorded in the store; the export shipped five empty columns. | unrouted — evidence-layer question | all four; see § 6 |
| `#6` | process | `record-template.md` carries `**END OF RECORD**` twice; cost three attempts to open the record. | skill (`record-template.md`) | n/a — tooling |

Finding #5 is confirmed by me: the `p_net`, `rec_frac`, `q_eng`, `p_th`, `p_et` columns of `results/points.csv` are empty in all 3 792 rows (`study.py` lines 102–106 declares them).

**Process findings from this read** (mine; not filed in any log — an administrator does not write `DISCOVERY_LOG.md`):

- The record's § 10 line 193 says "three arms … while four axes sweep"; `study.py` lines 3–4 and 33 say the same. The study has four arms and swept two axes (`record.md` § 1 line 10; `snapshot.json` `arms[]` has four entries; `results/points.csv` has only `R` and `a` varying). Stale text that predates the fourth arm and the two declines. It does not change any number.
- `results/verification_summary.json` `teax.revision` is the string `"unrecorded"`, while `snapshot.json` `teax.revision` is `744745f`. The verification tool did not capture the teax revision it ran under; the snapshot's value has no verification-side artifact behind it.
- Three small numeric overstatements in `record.md` (§ 2.2 and § 2.4 above): "within 0.1 $/MWh over R 13–15 m", "four best points within 0.07", "at most 1.1 % anywhere in the window". Each is a correct qualitative claim with a slightly too-tight number. They would be addendum material, not a changed result.

---

## 6. What the record does not support

Each entry is a fact a reader might expect and cannot get from this directory, or a claim the directory's evidence does not carry. Entries marked *(contract)* are defects in what the record contract asked for, not in the executor's care.

1. **Which cycle the Stellaris paper assumes.** Not recorded. The record says the paper names none and "Rankine" is the study's label (`record.md` § 17 line 265). The paper itself is outside the directory.
2. **The physical or commercial attainability of the (R, a) window.** The window is `engineered` (`snapshot.json` `arms[].window.provenance`) — the proof-of-life's choice, reused. No claim that it is the attainable range is supported, and the record says so (`record.md` § 11 line 211).
3. **Boundary positions finer than the grid.** Fences are located at ΔR 0.5 m, Δa 0.05 m. The wall-load fence is somewhere between a = 1.65 and 1.70; the `recirc_ok` fence between listed R values. No inter-node claim is supported (`record.md` § 6 line 87, § 17 line 268).
4. **Per-point values of `p_net`, `rec_frac`, `q_eng`, `p_th`, `p_et`.** Empty in every row of `results/points.csv` (finding #5). The only per-point evidence on net power and recirculating fraction is the two verdict columns. The quoted corner values (p_net 8.3 / 36.2 / 65.5 MW; rec_frac 0.94 / 0.79 / 0.68) come from `results/oracle_scan.json`, a hand-oracle recompute at five points in three arms, not from the package.
5. **The bound values the constraints compare against.** The wall-load limit (4.05 MW/m²), the recirculation threshold (0.5), the TBR value and floor (1.074 / 1.05), and B_max (24.9 T) appear only as prose in `record.md` § 4 lines 55–58. No result artifact in the directory carries them as data; `indicators.json` names the bound keys (`wall_load_limit`, `recirc_ok__threshold`, `tbr`, `tbr_floor`, `magnet__B_max`) but not their values. `results/baseline_result.json` has `peak_field_calc__B_peak` = 24.9 and no `B_max`. *(contract: the record carries verdicts but not the literals they were judged against.)*
6. **Any response on the economic axes from the package.** `availability` and `discount_rate` never moved in any run (`results/points.csv`). The § 8 scan numbers are oracle-only, three-arm, baseline geometry only. No sensitivity statement about the package on these axes is supported.
7. **Any cycle interaction with magnet cost, wall load, β, peak field, or TBR.** The cycle block reaches none of their operands (`indicators.json` `groups[cycle_block].constraints_unreachable`) and the run shows those columns identical across arms. The study could not have found one; absence here is not evidence about a fuller model.
8. **Any cycle × geometry reversal.** The arm ordering is the same at all 948 points. Supported as a fact of this grid; nothing beyond the grid.
9. **Per-arm stratified verification.** The sample is arm-blind (`results/verification_summary.json` `sampling.scheme`); the 3 / 1 / 6 / 2 split is inferred from case order (§ 4.4). No claim that each verdict combination was checked in each arm is supported.
10. **The teax revision verification ran under.** `results/verification_summary.json` records `"unrecorded"`. The snapshot's `744745f` stands on the snapshot alone. *(contract.)*
11. **The store's contents.** `_work/20260821-power-cycle-ab.db` is present on disk in this directory but is declared gitignored and outside the record (`snapshot.json` `stores[0].note`; `record.md` § 17 line 270). I did not open it. Its committed identity is the compatibility tuple and the verification summary's digest of it (`results/verification_summary.json` `stores[0].compatibility.digest`). The 3 792 per-case artifact files under `_work/artifacts/` and the baseline store under `results/_work/` are in the same position.
12. **Whether the record is committed.** The snapshot says `repo_commit` is HEAD at execution and the record is committed after (`snapshot.json` `package.note`). Commit state is not verifiable from inside the directory.
13. **The owner's rulings as events.** The two "no sensitivity" rulings and the "yes" to the fourth arm are recorded as quotes with dates (`record.md` § 2 line 28, § 8 lines 155–156). No transcript or separate artifact carries them; the record's word is the only evidence.
14. **The pre-execution critique as an artifact.** Its verdict and disposition are summarized in `record.md` § 14 line 232. The critique text itself is not in the directory.
15. **Wall-clock and plots.** 9 min 2 s is stated in `record.md` § 17 line 273 only; no artifact. No plots exist; the CSV is the result.
16. **The 1costingFE handshake.** Not run (`record.md` § 17 line 271).
17. **The mechanisms behind the two "non-intuitive" results.** The CSV supports the orderings (§ 2.3). The explanations — CAS23 priced per MWe; recirculation share — are the executor's account of the model (`record.md` § 6 lines 124–125). The `turbine_cost` column rises with η (consistent with the first), but the model's equations are not in the directory, so the mechanism is recorded as argument, not verified here.
