# Synthesis — 20260823-magnet-technology-ab

- **Administrator:** Claude (fresh subagent, administer mode; no memory of the run)
- **Date:** 2026-08-23
- **`snapshot.json` sha256 as read:** `c016680fb4daa4eb9bdc22d5bcbffe6023a2d898a2811fad246accbf8c4c0d13` (matches `record.md:273`)
- **Read:** only this directory — `record.md`, `snapshot.json`, `indicators.json`, `axes.json`, `study.py` (read, not executed), `results/*.json`, `results/*.csv`, and a listing of `results/_work/` and `__pycache__/`. The package symlink under `results/_work/pkg_link/` was not followed.
- **Conventions.** "Recorded" means a file in this directory says it. "Administrator's reading" means my own interpretation or recount, labeled as such. "Not recorded" means no file here carries it. Line numbers are `record.md` lines unless another file is named.

## 1. What the study set out to do

The owner asked for three things, quoted verbatim at `record.md:19-21`: compare REBCO against Nb3Sn magnets on the stellarator, run sensitivity on other axes for each, and look for a non-intuitive interaction.

The executor turned that into (`record.md:27-30`):

- Two arms that differ only in a four-key "conductor block": conductor cost, coil operating temperature, peak-field ceiling, and winding-pack cold volume. `arm-rebco` is the package as built (50 $/kA·m, 20 K, 24.9 T, 136.56 m³); `arm-nb3sn` is 7 $/kA·m, 4.5 K, 13.0 T, 390 m³ (`snapshot.json` `arms[].window.bounds.conductor_block`; `study.py:44-48`). The 390 m³ is an executor derivation, held constant over the sweep and disclosed as exact only at arm B's 4.69 T ceiling (`record.md:27`, finding #2 at `record.md:259`).
- Two swept axes common to both arms: on-axis field `B` (74 values, 3.0–10.0 T) and a plasma-density scale factor applied to four species peaks together (56 values, 0.36–1.26× Point A). 4,144 points per arm, 8,288 in all (`snapshot.json` `arms[].window`; `study.py:59-65`).
- Temperature, `R`, and `a` were proposed, traced, and declined; they are held at package values (`record.md:68-69`; `axes.json` groups `temperature`, `R`, `a`).

Package: `stellarator_tea`, sealed executable fingerprint `7447efea…`, semantic fingerprint `1ca93d0c…` (`snapshot.json` `fingerprints`; `results/package_identity.json`). No adapter, no glue (`snapshot.json` `arms[].glue_ledger_none: true`; `results/package_identity.json` `glue_ledger: []`; `record.md:217`).

## 2. What it found

### Store and fingerprint

Both arms ran in one store, `20260823-magnet-technology-ab`, under one compatibility tuple (`snapshot.json` `stores[0]`; both `arms[].store_id` resolve to it). Both arms carry the same effective executable fingerprint `7447efea…` with the explicit no-adapter nil (`snapshot.json` `arms[].effective_executable_fingerprint`). So the arms share a fingerprint, and the record discharges cross-fingerprint correlation with the stated nil "single fingerprint — no cross-arm correlation needed" (`record.md:230`). The store file itself is outside this directory (`snapshot.json` `stores[0].path` and `.note`; `record.md:288`).

### LCOE result by qualified channel

Objective channel: `stellarator_09__stellaris__lcoe_calc__lcoe`, $/MWh; `stellarator_09__stellaris__lcoe_1cfe_calc__lcoe` is exported alongside as `lcoe_1cfe` (`record.md:34`; `results/points.csv` columns `lcoe`, `lcoe_1cfe`).

| Arm | LCOE at (9.0 T, 1.00×) | Feasible there | Best feasible LCOE | Where | Unconstrained minimum |
|---|---|---|---|---|---|
| `arm-rebco` | 275.264 | yes | 204.104 | (7.0 T, 1.12×) | 134.084 at (3.0 T, 1.26×), infeasible |
| `arm-nb3sn` | 138.766 | no — `peak_field_ok` violated | none; 0 of 4,144 feasible | — | 107.404 at (3.0 T, 1.26×), infeasible |

Source: `record.md:37-42`; every value recomputed by me from `results/points.csv` (administrator's recount, § 6 below). The `arm-rebco` design-point value equals the pinned baseline headline 275.2642200420774 (`results/baseline_result.json` `channels`; `snapshot.json` `manifest.content_used.baseline.headline`).

Shape of the objective (`record.md:42`; confirmed on every row and column of both arms in my recount): LCOE rises strictly with `B` at every density and falls strictly with density at every `B`, in both arms. `arm-nb3sn` is cheaper than `arm-rebco` at all 4,144 grid points, and has no feasible point; the record states plainly that its LCOE ordering "is not a result" (`record.md:42`, `record.md:112`, `record.md:287`).

### Headline results as the record states them

- **`arm-rebco`:** feasible region is 1,002 of 4,144 points (24.2 %), bounded by three fences — `beta_ok` below (a B-fence rising with density), `peak_field_ok` above at 9.0 T, `wall_load_ok` at density ≥ 1.14×, `recirc_ok` at density ≤ 0.49× (`record.md:57`, `record.md:88-100`). The constrained optimum is at (7.0 T, 1.12×), 204.1 $/MWh, 26 % below the design point, on the beta and wall-load fences at once (`record.md:90`, `record.md:100`).
- **`arm-nb3sn`:** no feasible point. The conductor ceiling allows B ≤ 4.69 T; at 4.69 T the beta limit allows density ≤ 0.50× while the recirculation threshold requires ≥ 0.51×; the two fences cross inside one grid hundredth (`record.md:110`). The record attributes the closure to the cryogenic load (7.01 MW vs 0.86 MW) rather than the ceiling alone: `arm-rebco` is feasible at the same (4.69 T, 0.50×) node (`record.md:110`, `record.md:117`).
- **Three "interaction" facts**, stated as mechanisms of this package and not as physics claims (`record.md:114-118`): the design field 9.0 T is never optimal because B buys only magnet capital and beta margin (no confinement closure, finding #4); the conductor temperature, not the ceiling alone, empties `arm-nb3sn`; the wall-load and recirculation fences are B- and conductor-independent apart from one density row, so the conductor only decides how much of a plasma-set shape lies under its ceiling.
- **Policy H1** (feasible fraction within 5–95 % for a search-framed study): holds for `arm-rebco` (24.2 %), falsified for `arm-nb3sn` (0 %), which the record reports as a physics result of this package rather than a parameterization failure (`record.md:110`, finding #8 at `record.md:265`).

## 3. Framing verdict per axis

All from `record.md:63-79`. No axis reported `no_constraint_response` (`indicators.json` `groups[].no_constraint_response` is `false` for all six groups), so no owner ruling was required and the model-development-findings table carries the stated nil (`record.md:180`, `record.md:187`).

| Axis | Proposed | Judged | Changed | Indicator (`indicators.json`) | Basis as recorded |
|---|---|---|---|---|---|
| `B` | search | search | no | `constraints_reachable`: `beta_ok`, `peak_field_ok`; objectives `beta`, `lcoe`, `lcoe_1cfe`, `magnet_capital`, `total_capital` | Two fences found exactly where each ceiling puts them; beta fence rises with density; LCOE monotone in B so the optimum sits on the beta fence (`record.md:65`, `record.md:75`) |
| `density` | search | search | no | `constraints_reachable`: `beta_ok`, `net_positive`, `recirc_ok`, `wall_load_ok` | Three fences found (wall load, recirculation, beta diagonal); optimum on the wall-load fence (`record.md:66`, `record.md:76`) |
| conductor block | not framed — the arm definition | not framed | no | `constraints_reachable`: `net_positive`, `peak_field_ok` (as bound `B_max`), `recirc_ok` | Moved `peak_field_ok` at 2,240 points and `recirc_ok` at 74; moved no physics channel (`record.md:67`, `record.md:77`) |
| `temperature` | declined by executor | not run | — | `constraints_reachable`: `beta_ok`, `net_positive`, `recirc_ok`, `wall_load_ok` | No confinement closure pushes back on temperature itself; held at 14.63 / 15.40 keV (`record.md:68`, `record.md:78`) |
| `R` (with tie `magnet__R0`) | declined by executor | not run | — | `constraints_reachable`: `net_positive`, `recirc_ok`, `wall_load_ok` | Geometry was the prior study's axis pair; held at 12.7 m (`record.md:69`, `record.md:79`) |
| `a` | declined by executor | not run | — | same three as `R` | as `R`; held at 1.3 m |

Per-axis accounts: both swept axes are search-framed and owe feasible structure, which § 6 of the record supplies (`record.md:85-100`); their sensitivity halves carry the stated nil (`record.md:93`, `record.md:103`). The declined axes carry "not applicable" nils on both halves (`record.md:123-139`). The conductor block's "feasible structure" half is used for the arm comparison (`record.md:105-118`).

**Administrator's reading.** The framing tables are internally consistent with the indicator file: every constraint the record names as reached by an axis appears in that group's `constraints_reachable` list in `indicators.json`, and `B`'s reach is indeed limited to `beta_ok` and `peak_field_ok` (its `constraints_unreachable` lists the other four). The not-derivable disclosure is present in both `indicators.json` (`not_derivable`) and the record (`record.md:173-178`). Monotonicity of LCOE in B and density is therefore a fact of the run, established by the executor's recount (`record.md:248`) and by mine, not by any indicator.

## 4. Constraint structure

Six executing constraints, identified by `constraint_id` and `source_local_identity` in `results/baseline_result.json` `verdicts[]` (with `definition_qualified_name`) and `results/verification_summary.json` `constraints_rederived[]`. Per-arm outcomes are from `record.md:48-57`; every count below was reproduced from `results/points.csv` in my recount. No verdict reads `indeterminate` anywhere in `points.csv` (only `satisfied` and `violated` occur).

| `constraint_id` | `source_local_identity` | `arm-rebco` | `arm-nb3sn` | Findings citing it |
|---|---|---|---|---|
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | violated 1,997 / satisfied 2,147 | identical to `arm-rebco` at every point | #4 (`record.md:261`) — B reaches no plasma channel but β |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | satisfied 4,144 | satisfied 4,144 | #1 (`record.md:258`) — can never read `violated`; #7 (`record.md:264`) — floor probe evidence outside `results/` |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | violated 448 (B ≥ 9.125 T) / satisfied 3,696 | violated 2,688 (B ≥ 4.70 T) / satisfied 1,456 | #3 (`record.md:260`) — `B_max` enters only as a verdict bound; no thickness/stress coupling |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | violated 888 (density ≤ 0.49×) / satisfied 3,256 | violated 962 (density ≤ 0.50×) / satisfied 3,182 | #2 (`record.md:259`) — held cold volume overstates arm B's cryo load below 4.69 T; #6 (`record.md:263`) — its operand `rec_frac` is oracle-side only |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | satisfied 4,144 | satisfied 4,144 | none; recorded as inert, bound-vs-bound (`record.md:54`; `indicators.json` `bound_vs_bound: true`) |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | violated 518 (density ≥ 1.14×) / satisfied 3,626 | identical to `arm-rebco` at every point | none directly; #8 (`record.md:265`) concerns the per-arm H1 reading that the fences produce |

Where the arms differ: `peak_field_ok` at 2,240 points (all in 4.70–9.0 T, every density) and `recirc_ok` at 74 points (the 0.50× row, one per B value); the other four verdicts are identical at every point, as are the channels `beta`, `B_peak`, `p_fus`, and `wall_load` (`record.md:52-55`, `record.md:108`; confirmed in my recount). The bounds each verdict was judged against ride in `results/oracle_operands.csv` and are constant per arm: `beta_limit` 0.05, `wall_load_limit` 4.05, `recirc_threshold` 0.5, `tbr` 1.074 / `tbr_floor` 1.05, `B_max` 24.9 (`arm-rebco`) / 13.0 (`arm-nb3sn`).

Verdict combinations: 9 per arm, 11 in total, 7 common; "all satisfied" and "only `wall_load_ok` violated" occur only in `arm-rebco`; "`beta_ok` + `peak_field_ok`" and "`beta_ok` + `peak_field_ok` + `wall_load_ok`" only in `arm-nb3sn` (`record.md:57`; reproduced).

**Administrator's reading of the `arm-nb3sn` closure.** The record's mechanism (`record.md:110`) checks out against `points.csv` and `oracle_operands.csv`: the 115 Nb3Sn points that satisfy both `peak_field_ok` and `beta_ok` all violate `recirc_ok`; the 936 that satisfy `peak_field_ok`, `recirc_ok`, and `wall_load_ok` all violate `beta_ok` (lowest β 0.0504). At the (4.69 T, 0.50×) node the oracle-side `rec_frac` is 0.494 for `arm-rebco` and 0.516 for `arm-nb3sn`, straddling 0.5. The attribution to the cryogenic load is the record's argument; the artifacts show the two `p_cryo` values (0.864 vs 7.008 MW, constant per arm in `points.csv`) and the two `rec_frac` values, which is consistent with it, but `p_cryo` itself is not oracle-verified by name (`record.md:238` item 1).

## 5. Findings carried forward

Eight findings in `record.md:258-265`, ids `20260823-magnet-technology-ab#1`–`#8`. Each has a kind, a disposition, and a home or a stated `unrouted`; none is blank.

| Id | Kind | One line | Home as recorded |
|---|---|---|---|
| #1 | model | `net_positive` can never read `violated`: the CAS10 land term takes √p_net, so a net-negative point fails to evaluate before any verdict is written | modeling item, `'Preconstruction Cost'`; not minted |
| #2 | model | Cold volume is a held input; arm B's 390 m³ is exact only at its ceiling and overstates its cryo load below it; should follow from ampere-turns and J_eng | modeling item under the MFE cost epic; unrouted |
| #3 | model | No coil-thickness, radial-build, or stress coupling; `B_max` is only a verdict bound | policy § 4 R1 → modeling item; unrouted |
| #4 | model | No confinement closure: B has no path to fusion power or the power balance, temperature is free; so field is never rewarded and the optimum is the lowest B the beta limit allows | policy § 4 R3 → modeling item; unrouted |
| #5 | process | The oracle seam's key map needed three new entries before scan or verify could run (recurrence) | documented seam, `ANNEX.md § Oracle` |
| #6 | process | `points.csv` carries no `case_id`; its join to `oracle_operands.csv` is by row order within arm | study-definition convention |
| #7 | process | The density-floor probe points live in a discarded scratch store; evidence of the evaluability limit is not in `results/` | runbook step 7 |
| #8 | process | Policy H1 is stated per study; in an A/B one arm can be in band while the other is empty by physics | policy § 7 |

Three of the four model findings (#2, #3, #4) are `unrouted`; that is a stated state, not a blank (`record.md:267-268`). Whether the matching `DISCOVERY_LOG.md` rows exist cannot be checked from this directory (§ 7, entry 1).

## 6. Administrator's checks (labeled)

Everything in this section is my own work on the directory's files, not something the executor recorded.

**Digests.** Every `results/` file the snapshot lists under `arms[].artifacts` has the sha256 the snapshot gives it, and so do `study.py` and `axes.json`. `indicators.json` has the sha256 the snapshot records. The snapshot digest at `record.md:273` matches the file. The fingerprint-completeness rule holds: the three names under `manifest.content_used.fingerprint_names` are the three keys under `fingerprints`. `indicators.axis_declaration.subset` is `false`.

**Gates.** `results/preflight_results.json` records six gates, all `pass`, with the identity and baseline gates naming the two documents they read; `results/postrun_clean.json` records the post-run cleanliness pass. The baseline headline reproduced at relative deviation 0 and 6/6 verdicts matched.

**Verification.** `results/verification_summary.json` records `outcome: pass`, 8,288 of 8,288 cases completed, 48 sampled across 11 strata, worst relative deviation 4.27e-16, all six constraints re-derived with `verdict_mismatches: []`. I mapped the 48 sampled case ids onto `points.csv` (via `oracle_operands.csv`, which carries `case_id`) and confirmed the worst-case value (`c7054`, `total_capital` 8925909619.29) matches the `points.csv` row for `arm-nb3sn` at (7.25 T, 1.24×). That mapping also confirms the 24 / 24 arm split stated at `record.md:236`.

**Recount of `points.csv`.** Per-arm verdict counts, feasible counts, the design-point and best-feasible LCOE values, both unconstrained minima, the fence positions quoted in `record.md:50-55` and `record.md:88-100`, the strict monotonicity of LCOE in both axes, the cross-arm identity of `beta`, `B_peak`, `p_fus`, `wall_load`, the 2,240 + 74 differing points, the eleven combinations and their arm membership, the 1.74 $/MWh-per-0.125-T slope at 1.12×, the 37-point feasible columns at B ≥ 7.0 T, and the `feasible` column's consistency with the six verdicts all reproduce. Two statements did not; see § 7 entries 9 and 10.

**Re-derived verdicts from `oracle_operands.csv`.** Joining by arm and then by row order within arm, `rec_frac ≤ 0.5` reproduces the store's `recirc_ok` and `p_net > 0` reproduces `net_positive` at every one of 8,288 rows, in both arms. Minimum `p_net` is 18.89 MW (`arm-rebco`) and 12.74 MW (`arm-nb3sn`), at the 0.36× floor, as `record.md:51` says. One caution the record does not spell out: the two files list the arms in opposite order (`points.csv` is sorted with `arm-nb3sn` first, `study.py:118`; `oracle_operands.csv` is in case order with `arm-rebco` first, `c0000`–`c4143`). A positional join over the whole file is wrong; a join by arm then row order is right, which is what `record.md:46` and finding #6 describe.

**Axis declaration at gate time vs now.** `results/preflight_results.json` `input_digests.axis_declaration` is `0d2c37b2…` and its detail says "12 declared keys across 5 groups"; the `axes.json` in this directory is `0db9ac02…` with 6 groups and 14 keys. The record states this (`record.md:198`: the temperature group was added afterwards for its indicator only). So the temperature group's two keys were traced by `indicators.json` (which records the `0db9ac02…` declaration and `group_valid: true` for all six groups) but never passed through the preflight declared-keys gate. Since temperature was not swept, nothing in `results/` depends on this. The pre-gate `axes.json` is not in the directory.

**Directory hygiene.** `results/_work/` holds the baseline point's store (`stellarator-baseline-point-v1.db`, named in `results/baseline_result.json` `executed_under.store_id`), one artifact json, an empty `staging/` subdirectory, and `pkg_link/stellarator_tea`, a symlink to a path outside this directory. `__pycache__/study.cpython-312.pyc` is also present. None of these appears in `snapshot.json` `arms[].artifacts` or in `record.md` § 17.

## 7. What the record does not support

Every fact that could not be recovered from this directory, and every claim its evidence does not carry. Entries 9 and 10 are record statements the artifacts contradict; the rest are absences or scoping limits.

1. **Discovery-log rows for #1–#8.** `DISCOVERY_LOG.md` is outside the directory. That a row exists for each finding (runbook step 14's fail-closed condition) is not checkable here.
2. **The pre-execution critique itself.** Only the executor's summary of its verdict and the five changes applied survives (`record.md:247`). The critic's text, and the "branch-name remark" the executor says was wrong, are not in the directory.
3. **Evidence that the package fails below ~0.35× density.** The four scratch package probes were discarded (finding #7, `record.md:264`; `record.md:280`). What the directory holds is the oracle's own view: `results/oracle_scan.json` marks (9.0 T, 0.34×) in `arm-nb3sn` as `evaluable: false` with the note "p_net < 0: sqrt in CAS10 goes complex; execution_failed in the package", while the same point in `arm-rebco` is `evaluable: true` with `p_net` 4.5 MW. No package artifact shows an `execution_failed` case. The `net_positive` fence is therefore located by neither arm's package run.
4. **The store.** `snapshot.json` `stores[0].path` points beside, not inside, the directory; the store's bytes have no digest anywhere (the verification summary digests the compatibility tuple, `results/verification_summary.json` `stores[0].compatibility.digest`, not the file). `results/points.csv` is an export; the per-case inputs, the `predicate_ir`, and the store's own verdict records are not in the directory.
5. **Sources of the Nb3Sn block values and of the cold-volume derivation.** `defaults.py:613`, `costing_constants.yaml:57`, DI-009, DI-010, and the "Table 5 image" are cited by path (`record.md:27`, `record.md:149`; `study.py:36-39`) and not carried. The 390 m³ derivation (5.5× at equal ampere-turns, × 4.69/9.0) can be re-run arithmetically from `record.md:27` but its two inputs (the 15–28 and 112–124 A/mm² ranges) rest on a source outside the directory.
6. **The owner's 2026-08-22 ruling that `availability` and `discount_rate` have "no sensitivity".** Cited to another study's record (`record.md:28`, `record.md:180`); not in this directory. Both are held (`snapshot.json` `arms[].window.bounds.availability`, `.discount_rate`) and the record names them as "not proposed", so no ruling was owed here; the prior ruling's text is simply not recoverable.
7. **The teax revision.** `results/verification_summary.json` `teax.revision` reads `"unrecorded"`. `snapshot.json` `teax.revision` gives `744745f`, which `record.md:238` item 4 describes as the executor's own `git rev-parse`; no tool output in the directory carries it.
8. **By-name oracle verification of `p_cryo` and `p_fus`.** Disclosed absent (`record.md:238` item 1): neither is in `channels_checked` of `results/verification_summary.json`. `p_cryo` is the one channel through which the arms differ in the power balance, and the attribution of `arm-nb3sn`'s closure to the cryogenic load (`record.md:110`, `record.md:117`) rests on it. It is verified only indirectly, through the `lcoe` parity and the re-derived `recirc_ok` / `net_positive` verdicts.
9. **"31 points at 1.00×" (`record.md:90`).** `results/points.csv` has 20 feasible `arm-rebco` points at density 1.00×, at B = 6.625 to 9.0 T in 0.125 T steps. The band is as stated; the count is not. Nothing else in the record depends on the number.
10. **"Every combination in every arm that has one was sampled" (`record.md:236`).** Not supported. Mapping the 48 sampled case ids onto `points.csv` (my § 6 check) gives 7 of `arm-rebco`'s 9 combinations sampled (missing: `peak_field_ok` + `wall_load_ok` violated; `peak_field_ok` + `recirc_ok` violated) and 8 of `arm-nb3sn`'s 9 (missing: only `recirc_ok` violated). All 11 combinations were sampled across the store, which is what the arm-blind scheme (`snapshot.json` `arms[].verification.sampling_scheme`) guarantees; per-arm coverage of every combination is not something the scheme promised or the sample delivered. The record's own next sentence, and `record.md:289`, already say the scheme did not set out to check each combination in each arm; the stronger sentence before it overreaches.
11. **The axis declaration the preflight gate read.** `results/preflight_results.json` names digest `0d2c37b2…` (5 groups, 12 keys); the directory's `axes.json` is `0db9ac02…` (6 groups, 14 keys). The gated version is not in the directory, and the temperature group's keys were never run through the declared-keys gate (they were traced by `indicators.json` only). Recorded at `record.md:198`; the missing file is the gap.
12. **A key-based join between `results/points.csv` and `results/oracle_operands.csv`.** Finding #6: `points.csv` has no `case_id`. The join is by arm and then row order, and the two files order the arms oppositely (§ 6). I verified the join at every row by re-deriving two verdicts, as the executor did (`record.md:248`); that check is not carried by any artifact, and a reader who joins positionally across the whole file gets 148 wrong `recirc_ok` rows.
13. **`results/_work/` and `__pycache__/`.** The baseline point's store and artifact json, an empty staging directory, a symlink to the package outside this directory, and a compiled `study.py` are present, undigested, and unmentioned in `snapshot.json` `arms[].artifacts` and `record.md` § 17. The symlink means the directory is not self-contained as a tree. Runbook step 15's condition that "a result artifact has no digest" would read these files, if they count as result artifacts, as a defect; the record does not say whether they do.
14. **Identity of `snapshot.json` `package.path` with the gated path.** The snapshot says `exploration/stellarator_e2e/pkg/stellarator_tea` and explains in a note that it is an alias of `exploration/stellarator_e2e/generated`, the path every `results/` document names. The alias relation is asserted by that note only; nothing in the directory demonstrates it.
15. **Wall-clock.** "20 min 17 s, 0.147 s/point" (`record.md:291`) has no artifact behind it.
16. **A like-for-like LCOE comparison of the conductors.** No common feasible point exists (`record.md:287`). Every `arm-nb3sn` LCOE in the record is at a point its own verdicts reject; "cheaper at every point" is a fact of the grid and not a result about the conductor.
17. **Fence positions finer than the grid.** ΔB 0.125 T (0.05 T across 4–5 T), Δdensity 0.02× (0.01× across 0.40–0.60×) (`record.md:286`). "4.69 T" is a chosen node; "1.14×" and "0.49×" are first-violated nodes.
18. **`arm-nb3sn` infeasibility at any other geometry, temperature, or cold volume.** `R`, `a`, `T_i0`, `T_e0` are held; the recirculation fence that closes the arm is geometry-dependent per the record (`record.md:282`); the 390 m³ is held and overstates the cryo load below 4.69 T (finding #2). The result is a statement about (12.7 m, 1.3 m, 14.63/15.40 keV, 390 m³) only.
19. **Any claim about real stellarators or real conductors.** The "B is never worth its price" result follows from the package having no confinement closure (`record.md:283`, finding #4); the held `f_carnot_cryo` 0.20, `peak_ratio` 2.7667, and `p_pump` 1.0 MW are disclosed as unsourced-for-this-comparison or optimistic (`record.md:284-285`). The window is engineered (`snapshot.json` `arms[].window.provenance`), so a result at a window edge is a result about the window (`record.md:226`).
20. **The 1costingFE handshake.** Not run; outside the study contract (`record.md:290`).

Entries 1, 3, 4, 7, 11, 12, 13, and 15 are facts a reader would expect the record contract to carry and cannot find in the directory. Per the runbook, those are defects in the record contract rather than in this read; entries 9 and 10 are defects in the record's statements, which an addendum can correct without touching any artifact.
