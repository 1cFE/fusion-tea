# Round 2 review — goal `wall-and-heating` (fresh reviewer, 2026-09-05)

**Reviewer:** fresh non-author session spawned from the deposited prompt (`evidence/round2_review_prompt.md`, `1928925b`); no context inherited; not the round agent, not the critique, not the administrator, not the checkpoint session. Worked only from the repository at HEAD `1928925b` on `feat/demo-maturation`. Nothing under `knowledge/holdout/` was opened. No file edited; no state-changing git command run.

**What I read, in the prompt's order:** `GOAL_RUNBOOK.md` (the named sections); `goal.md`; `trail.md` § Round 1 review through § Round 2 result; `evidence/round1_review.md` § Constraints carried forward and § Close packet; `learnings.md` L-001..L-008; every `evidence/round2_*` file; the WI-041 spec, design and plan (with its § MR-WI041-11 restatement, phase records and § Spec success criteria); the changed model text in `mfe_plasma_scaling.sysml`, `mfe_account_costs.sysml`, `mfe_viability.sysml`, `mfe_heating_chain.sysml`, `mfe_plant.sysml`, `stellarator_plant.sysml`; the study directory `20260904-wall-and-heating/` (record with both Addenda, synthesis, snapshot, axes, indicators, study/scan/edges definitions, every `results/` artifact); the 2026-09-04 rows of `DISCOVERY_LOG.md` and `git show 8906d4e7`; ADR-0004; the Stellaris extraction at lines 158–166, 224–245, 718–752, 1293–1308, 1576–1610, 1720–1730, 1752–1770, 1776–1786, 1808–1840, its `decisions.json`, and the seven page images the T-001 return names; the method paper (`…_2/output.md`) at lines 86–94, 296–304, 364–368.

**What I ran:** `uv run python` recounts over `results/points.csv`, `oracle_operands.csv`, `excluded_points.csv`, `window_scan.json`, and round 1's `points.csv`/`oracle_operands.csv` (scripts in the scratchpad, not deposited); `git log` on every cited path; `cmp` on all 17 twin files; the three batteries (§ 8).

---

## Verdict: `FINDINGS`

The round stays closed and every task's evidence stands. Every number I recounted from `results/` agrees with the record as corrected by its two Addenda, with the synthesis, and with the trail — I found no evidence error. The findings are: one contract conflict the round result itself introduced into the trail (F1, owner-ruled); corrections to the proposed learning delta (L-010's τ = 4 clause rests on a critique probe, not executed data; L-013 rejected; L-009 and L-011 scoped); two form departures from round-1 practice (no joined rows under `#6`/`#8`; the checkpoint's in-place revision); and two readability notes. None reopens a task.

**Grounds.**

1. Every cited ref resolves and says what the trail claims (§ 1). The 458 / 201 / 257 split, `c1721` at 212.460, `c0821` at 257.35, zero feasible at a 1.3, the fifteen transect rows, the re-read's 384 / 152 / 91 → 26, `c0550` → 5.271 violated, `c0584` → 378.556, the shadows 257 / 142, the size-matched 26.54 / 17.08 against 14.07 / 15.07, R^0.72, the ceiling's structure, and the baseline's five changed channels all reproduce from the data.
2. The strategy was pursued in its declared order with one pin and one committed study; assumption (2) failed in letter and nothing depended on it (§ 2).
3. Every task stayed inside its scope or amended it before the work; the T-004 amendment is a legitimate critique-driven extension (§ 3).
4. Zero goal-level retries, correctly classified (§ 4).
5. The checkpoint sequence respected the cap; one form point (§ 5, F5).
6. Seventeen joined rows landed, each class-bearing, each moving or saying it did not; two of the round's own sightings got no joined row (§ 6, F4).
7. No cited artifact moved outside its task (§ 7).
8. Batteries green at HEAD: `tests/models` 48 / 13, `tests/study` 362 / 1 (the +3 over the claimed 359 are the new record's three parametrized instances), `test_records.py` 25; the goal-contract test has two failures, and **one of them is the round's** (§ 8, F1).
9. § Answered when (b)(i) is met by WI-041 and (b)(ii) is answered by the committed study; the four conditions are disclosed facts of the model the contract accepts (§ 9).

---

## 1. Every cited ref resolves — recounts

All from `results/points.csv` (6,311 rows) joined to `results/oracle_operands.csv` on `case_id`; "alone" = that verdict `violated`, the other eight `satisfied`; "driven" = `feasible` and not `ignited`. Multipliers: n 1.0× = 5.06e20.

| Claim (trail / record) | Recount | Agrees |
|---|---|---|
| Arms 2,974 / 2,962 / 360 / 15; 6,376 proposed, 65 excluded, 6,311 evaluated | same; exclusions 54 `non-positive fuel` + 11 complex (`TypeError`), 27 at 100 MW / 38 at 220 | yes |
| 100 MW: 458 feasible, 201 of those ignited, **257 driven**; 220 MW: 598 / 198 / 400; re-read 24 / 0 / 24; transect 0 / 8 / 0 | same (the transect's "8" is ignited among all fifteen) | yes |
| `c1721` 212.460 at R 14.2, a 2.2, I 15 MA, T 16 keV, n 0.9×; peak 4.030; 7.4 MW required; 5 replacements; 24.3 $/MWh CAS72 | 212.45952; 4.554e20; 4.03007; 7.44 MW; core life 4.466 FPY; n_rep 5; 24.27; p_net 1,571.9 MW; cheapest feasible allowing ignition `c1680` 200.27 (−25.5 MW) | yes |
| Design column (R 12.7, I 15 MA, T 14.63, n 1.0×): peak 4.179 / 4.123 / 3.955 / 3.846 / 3.603 / 3.346; p_aux 102.7 / 54.0 / 47.6 / 58.2 / 103.5 / 176.5; only `c0821` (a 1.7, 257.35) feasible driven | same, `c0621`…`c1121`; He/n_e 0.110 → 0.236 | yes |
| 0 feasible at a 1.3 at 100 MW | 0 of 501 rows (5 ignited, none feasible) | yes |
| Transect: fifteen rows, feasible only at τ = 8 (the anchors' grid members); through the scan's best point 6.157 / 5.202 / 4.512 / 3.246 / 2.743 and −331.1 / −174.0 / −61.5 / +141.9 / +221.2 | all fifteen rows match (`c6296`–`c6310`); design-column anchor is the baseline at I 15.4 MA | yes |
| Re-read: 384 matched, averages bit-identical, 152 flip, 91 → 26 all driven, CAS72 +22–118 M$/yr, LCOE +7.2–10.1 | 384 on (I, T, n, η); worst relative deviation 0.0; 88 stay / 152 flip / 144 stay violated; 26 feasible, 26 driven; +22.2–117.7; +7.24–10.07; the reviewer's 1.316 re-read of round 1 also gives 26 | yes |
| `c0550` → 5.271 violated; `c0584` → 378.556 | `c6222`: avg 4.0036775 identical, peak 5.2706, LCOE 267.159 → 275.879, CAS72 150.85 → 212.26 M$/yr (7 replacements); `c6256`: 371.005 → 378.556, feasible driven, CAS72 93.30 → 128.25 | yes |
| Shadow survivors 257 / 142; `c2278` 254.44; optimum 3.061 → 5.60 at 1.83× | 257 / 142; 254.4375; 3.06134 × 1.83 = 5.6023, `violated`; 204 feasible (any) survive the high end | yes |
| Size-matched wall price 26.54 / 17.08 against charges 14.07 / 15.07 (0.53 / 0.88) | 100 MW: `c0716` (R 12.7, a 1.5, 14 MA, 18 keV, n 1.0×; 1.67× the limit, 9 replacements) 185.92, 28 of 85 driven wall-alone points inside ±10 % p_net; 220 MW: `c3679` 202.37, 59 of 208 | yes |
| `c1096` 160.0 wall-alone ignited (1.5×, charge 12); `c1486` 178.73 driven (charge 11.24); `c2892` 147.9 fails beta too | 160.002, 1.549×, 12.27, ignited; 178.727, 1.453×, 11.24; 147.899, 2.22×, `beta_ok` violated; charge range 0.003–28.03 | yes |
| R^0.72 end to end on the executed design column, flattening 0.86 → 0.56; 0.83 on the scan | (a 1.3, I 15 MA, T 14.63, n 1.0×): 3.752 / 4.179 / 4.541 / 4.846 / 5.102 → 0.716; local 0.858 / 0.743 / 0.646 / 0.564; scan 9.7–15.7: 0.827 | yes |
| Ceiling (Addendum 2): violated at (11.2: 14–18 MA), (12.7: 16, 18), (14.2: 18); nowhere at R ≥ 15.7 or 13 MA | over 5,936 geometry rows: 239/239, 239/239, 230/230, 195/195 at R 11.2 for 14/15/16/18 MA; 240/240, 232/232 at 12.7 for 16/18; 240/240 at 14.2 for 18; 0 everywhere else | yes |
| 11 ceiling-alone at a 1.3 / 100 MW, cheapest 333.39; `c0429` 225.63 | 11, all R 11.2, 333.393; `c0429` (R 11.2, a 2.0, 14 MA, T 16, n 1.0×) 225.631, p_aux 40.9 | yes |
| Baseline `c2973`: calibration 1.3164408571, peak 4.0880446844, CAS72 131,494,480, LCOE 313.513412, `wall_load_ok` violated | 1.31644085710; 4.088044684423419; 131,494,479.61; 313.5134115016116; violated (and `sustainment_ok`); average 3.105376639; p_fus 2,725.363 (0.94 % over 2,700) | yes |
| T-002: exactly five channels differ from the WI-039 pin | `cas72_calc__cost`, `lcoe_calc__lcoe`, `lcoe_1cfe_calc__lcoe`, `wall_peak_cal__calibration` (new), `wall_peak_calc__wall_load_peak` (new); verdict diff `wall_load_ok` only; T-002 and T-003 baselines identical; executed under `d4be3951…` | yes |
| 0.92 efficiency sentence | round 1's 100 MW arm: 36 sustainment-alone points (min 87.06 MW); 9 pass the honest wall (average × 1.316440857 ≤ 4.05); least needs 92.11 MW → η 0.921; this grid's a-1.3 sustainment-alone floor 100.78 MW (150 points) | yes |
| Constraint counts § 4 | wall 2,667 (1,190 / 1,189 / 279 / 9), alone 1,060; sustainment 2,450, alone 904; field 1,615, alone 476; recirc 822, alone 139; beta 736, alone 2; stress 427, alone 0; three inert | yes |
| Scan § 11: 70 of 7,154 feasible at 100 MW, best 233.433 at (14.2, 1.8, 14 MA, 16 keV, 0.8×), a 1.5–1.8; 151 of 7,145 at 220, best 259.844; 101 errors all at R 9.7 | same; feasible T 14.63–16 only | yes |
| Verification / preflight | outcome `pass`, 13 channels, worst 4.62e-16, 9 constraints re-derived, 0 mismatches over 6,311 cases; preflight 6/6; snapshot counts 6,376 / 6,311 / 65 / 1,080; every arm carries `effective_executable_fingerprint`; `record.md` contains no `<` | yes |
| T-003 return | `CANDIDATE`, ten gates `pass`, pin `c1b0f0d1…`, semantic `d468f3b6…`, executable `d4be3951…`, teax `744745f8…`; census 207; 74 handwritten files byte-identical | yes |

**The source (check (i)).** The page images say what T-001 says: Table 2 (`page_002_table_0.png`) prints minor radius 1.3, major 12.7, plasma surface 940 m², required plasma-coupled ECRH 50 MW, peak fusion ~2700, **peak neutron wall load 4.05**; Table 1 agrees on 1.3 / 12.7; Table 5 (`page_009_table_0.png`) prints 1.3 / 12.74, surface 327, fusion 2700, av. neutron wall power 2.87 / 2.87, τ*/τ_E 8.00, and **no peak row** — the extracted "4.95" at line 748 is a rewrite artifact (`decisions.json`: page 9 `claude_replace`; pages 2, 8 and 20 likewise); Table 6 (`page_020_table_0.png`) prints peak first-wall DPA 10.7 DPA/FPY and first-wall lifetime ~4–6 FPY, and **no wall-load row** (the extracted "~1.5 W/m²" is an artifact); Fig. 33's colour scale runs 0–4 MW/m²; Fig. 34 prints the 16.6 cm SOL; Fig. 38's caption prints peak 3.9 / mean 2.2 DPA/GWf/yr; line 1295 prints the 100 mm minimum standoff; lines 1811–1813 the ~4 FPY at 42.8 DPA. The method paper defines the NWL as neutron power per first-wall area (line 92), the peaking factor as q_max over the wall average (line 302), and calls the NWL the proxy that sets first-wall and blanket lifetime (line 88). 2700 / 940 = 2.872 reproduces the 2.87; 2160 / 940 = 2.30 is the most the wall average can be. T-001's three answers stand on the printed pages.

---

## 2. Goal and strategy fidelity

The strategy's declared order was: establish the 2.87's basis from the source → one model increment (like with like; CAS72 operand decided explicitly; round 1's 220 MW result restated before regeneration) → one pin → the (b)(ii) study over `R`+tie, `a`, `n_e0`, `T_i0` with `I_coil` at two heating levels. Round 2 ran T-001 → T-002 → T-003 → T-004 in exactly that order, with one promoted pin (`c1b0f0d1…`, T-003) and one committed study (`9df54941`, T-004). No task was run under a second pin; nothing was executed before the pin.

**The six assumptions, as the result reports them and as I find them:**

1. *The source's own peak is admissible and the right limit* — held. It is Table 2's printed 3D value on the design's own wall; the model already carried it as `wall_load_limit`.
2. *A reference-radius correction alone puts the average on the source's basis once that basis is established* — **failed in letter, as the result says.** The source states no basis; the only printed radius is 1.3 m; no printed standoff reaches 1.5 m. The strategy's fallback (the shaped-wall route, then the bounded negative) was not triggered because the evidence supported a third, fully sourced form: an identity at the source's design point, N = 4.05 × 701.926 / 2160 = 1.3164, which is mathematically the strategy's "reference-area correction × net peaking factor" collapsed into one computed quantity with both inferred factors removed. The approach (source-anchored, computed peak against the printed peak, external sources as bounds) is intact. The form was the round agent's to decide (§ Reserved gates ruling 5) and it was surfaced as a decision with its reasoning. Accepted.
3. *Verdict-class change plus the CAS72 operand; committed studies restated at the MR-WI037-7 shape* — held: restatement (a)–(f) in commit A; six fixtures re-derived; census 199 → 207.
4. *Lifetime operand decided explicitly with its convention stated* — held (D2; the peak; the 3.4 × 10⁻⁵ convention change named).
5. *`R` reaches wall load and its effect is measurable* — held (R^0.72 on the executed column).
6. *Heating stays as WI-039 left it* — held: every heating channel bit-identical at the baseline; `eta_couple_heat` 1.00; the only heating-file change is the EI-5 doc sentence the T-002 objective authorized.

---

## 3. Task scopes

**T-001.** Inside scope: read-only; one evidence file; no registration, no model or knowledge edit. Rulings on (i): the 2.87 has no stated basis — right; it is not a wall average by the source's cited definition — right (the wall average cannot exceed 2.30); it equals fusion power over the printed 940 m² to three figures — right; the only printed peak is 4.05 and the "4.95" row does not exist — right (Table 5 image); lifetime is set by the peak — right (Table 6 image; text; method paper line 88). **The extraction-artifact finding is right in substance and slightly over-attributed in wording:** the round-1 review derived r = 1.5 m arithmetically (753 m² at R 12.7) and did not cite line 227; T-001's sentence that the radius "came from the extraction's rewritten Table 2 row" is an inference — the honest statement is that the arithmetic coincides with a rewritten value the images contradict (0.8 × 940 = 752.0 against 4π²·12.7·1.5 = 752.06). The conclusion — there is no printed radius to correct to — is unaffected (F6).

**T-002.** Inside scope. The model diff touches only the wall chain, the lifetime operand, the retired `ash_frac` binding and the three authorized doc corrections; `p_fus`, geometry, `wall_area`, `wall_load_limit` 4.05 and every heating number are unchanged (verified on the T-002 baseline). Rulings on (ii): the form is the honest one under (b)(i) — a computed peak (the model's average × a calibration the model computes from six page-image facts, verified in `mfe_plasma_scaling.sysml:257-349` and the six bindings at `stellarator_plant.sysml:1169-1216`) against the printed peak, both on the source's wall basis at the design point, with the constancy assumption written in the library doc and the instance doc (MR-WI041-7) and `calibration_direct` dormant at 0.0. "Made honest is not made looser": the fence tightened from average ≤ 4.05 to average ≤ 3.0765, the baseline flipped to violated at 4.088, and nothing at the limit, the calibration, the power or the geometry was adjusted — the manifest's expectation is flipped, SV-051 records it, and the design's prediction table was written before the number existed. The exact `ash_frac` retirement is derived (its only reader was the CAS72 chain's internal neutron power; the sustainment calc's own default untouched). Disclosed and left alone. The one deviation is recorded honestly: the manifest's verdict schema cannot carry the derivation note MR-WI041-5 asked for (plan § Phase 6).

Ruling on (iii): the § MR-WI041-11 restatement is in commit A (`df6dc964`, 12:00) — `git show df6dc964:…/plan.md` carries it at line 213 — and the regenerated package is in commit B (`cb355321`, 12:15). Written where the round-1 constraint required, before regeneration. T-004's re-read arm confirms it exactly: all 384 points reproduce the average, 26 survive, and the reviewer's 1.316 re-read of round 1's own file gives the same 26.

**T-003.** Inside scope: the seam ran once, performed nothing, returned `CANDIDATE` on ten gates; the seven return documents are deposited; nothing under `models/`, `exploration/` or the work item changed.

**T-004.** Ruling on (iv): the amendment is a **legitimate extension, not drift**, on the round-1 ruling (i) precedent. Its three changes are critique-driven (F2, F5, F3/F4), disclosed by a dated `### Amendment` under the open round, change no pin, no question and no comparison meaning, and are each bounded: the τ*/τ_E arm is a sensitivity transect claiming no boundary; the re-read arm is the predecessor's committed grid, not a new efficiency sweep; the two shadows are labelled columns beside the executed numbers. One limit of the record, stated as a constraint rather than a finding: the scope, start, amendment and record were committed together at `9df54941` (16:40), so "before any point ran" is attested by the trail and § 14 and consistent with disk (critique 14:59 → axes/indicators 15:02 → `study.py` 15:21 → `points.csv` 16:32), but not demonstrable from git. Ruling on (v): the held axes are traced — `axes.json` declares 14 groups (the six swept plus `eta_source_heat`, `eta_couple_heat`, `j_wp`, `B_max`, `wall_peak_q_ref`, `f_suppr_ash`, `iota_23`), `indicators.json` ran over all 14 with `no_constraint_response` false everywhere, and the record § 8 carries a ruling per declined group; the six `wall_peak_*` facts are asserted per case through the calibration channel to 1e-9 (`study.py` `export()`). The round-1 sweep rules held: `a` brackets 1.70 (1.3–2.2); `R` with its tie; `I_coil` under the ceiling (18 MA caught at R ≤ 14.2); `j_wp` held and asserted; `B_max` declined; T interior at 100 MW (16 keV), and at 220 MW at the window's bottom with the 13 keV bracket carried by the committed transects at the scan's anchor and disclosed as such.

---

## 4. Retry classification

Zero goal-level retries, correctly. Under the runbook a retry follows a `MECHANICAL_FAILURE` return with task, inputs, scope and meaning identical; none of the four events was a return.

- **The killed launch, re-launched detached:** a native execution restart inside T-004 before any point ran and before any store existed; disclosed in record § 17 and the T-004 return. Not a retry; a native-stage correction. It consumed no cap.
- **The codegen re-stencil and hand restoration:** the first regeneration exited 0 and did what it documents; the second regeneration sealed the restored impl byte-identically (the seam's handwritten-preservation gate later confirmed 74 files). A native-stage correction inside the implement stage, recorded as a gotcha. Not a retry.
- **Commit B's sweep and amendment (`9ebf9f08` → `cb355321`):** a git-handling slip corrected the same minute; `9ebf9f08` is reachable from no branch; the owner's staged blobs were restored and the working tree untouched. Neither a retry nor a native-stage correction of the work — a process slip, disclosed. Nothing to reclassify.
- **The 65 excluded proposals:** neither. The evaluability pre-screen recorded each with its reason (`excluded_points.csv`) and the closure's validity edge is filed as `#8`.

---

## 5. The checkpoint sequence

C-001.r1 `REVISE` → the author's second Addendum and an in-place revision of the dispositions file marked `[r2]` → resubmitted to the same session → r2 `PASS`. The cap (2 revisions / 3 submissions) was respected: two submissions. The runbook's letter — "each submission is a new `rK` entry; never amend a previous one" — governs the trail's checkpoint entries, and both entries exist unamended with the r1 entry listing what changed. The dispositions **file**, however, no longer carries r1's text: it was replaced in place, and r1's wording survives only at `9b1a4ef1`. Round 1 kept r1 and appended `§ Revision r2`, which is the better form because "the sequence of submissions is the record of the disagreement" is then readable in the file. Not a violation; a form point carried forward (F5). I verified from `git diff 9b1a4ef1 a5b0b96a` that the revision touched only the dispositions file, the record (Addendum 2 appended) and the trail — no sighting row.

---

## 6. Discovery rows

Seventeen joined rows landed at `8906d4e7` (log lines 118–134), each with a class from the ADR-0004 set, a status, a responsible actor and a concrete next reference; no touched row returns `unrouted`; no sighting row was edited (the diff is 17 pure insertions). Row by row:

- `20260904-wall-and-heating#1` `model fix` — the (b)(ii) answer with its four conditions and the design-`a` / 0.92 sentence; discharges nothing by itself; actor the owner at the close. Moved: the round result carries it. Right.
- `#2` `research` — open; the transect's two limits stated; actor the owner at the close (mint or carry). Moved: the request is named and homed (`knowledge/research/requests/`, to be minted). Right.
- `#3` `model fix` — open, two candidates not minted; the sighting's over-read corrected in the row (the shadow does not move the optimum interior — I confirmed the shadow minimum per `a` still falls to 2.2). Right.
- `#4` `model fix` — open; candidate named. Right.
- `#5` `model fix` — open; corrected cheapest points; standing at `20260821-power-cycle-ab#1`. Right.
- `#7` `model fix — none owed; discharged as a measurement` — the executed 0.72 beside the scan's 0.83; to L-010. Right (the r1 row carried no class; fixed at r2).
- **`#6` and `#8`: no joined row.** The sighting rows carry a class, a status, an actor and a next reference (`#6`: discharged by WI-041; `#8`: `declared seam`, the ANNEX candidate), and the newest-row-wins reading returns the same state either way. But ADR-0004's mechanism is "a goal round records dispositions by **appending** a row", the sighting is the executor's account, and round 1 appended under all seven of its own sightings including its `#4` (declared seam) and its `#5`/`#6` (closed in-study). Round 2's omission is a departure in form, not substance (F4): append one row each at the landing of this review, as round 1 did on its F4.
- `20260821-power-cycle-ab#1`: routed from `unrouted` to the goal's named follow-on `[OWNER 2026-09-03, ruling 4]`, with the measured consequence (the chain's 0.53 / 0.88) and the actor named. The model changed nothing; the route moved. Right — and it was the log's oldest `unrouted` row.
- `20260901-sustainment-fence#1`: the question the previous row left to round 2 is decided — the 262 candidate (`20260903-priced-levers` `c0180`) re-reads at 3.8861 × 1.31644 = 5.116 against 4.05, wall-closed; the ceiling's structure as recounted; `c0429` at 225.63 does not undercut 212.46. The row moves and says what changed. Right.
- `20260903-wall-and-heating#4`: the home moved by owner ruling to a suspected code bug in `.project/backlog/BACKLOG.md` § Flagged; the class stays `declared seam` for study practice. Right.
- `20260903-wall-and-heating#1`, `#3`, `20260903-priced-levers#1`: discharged at the wall half, with the conditions carried and the radial-build defect named as untouched. Right — the fence is built and measured, which is what those rows routed to round 2 for.
- `20260830-stress-fence#1`: re-sighted on `a`; the row says it changes nothing and names the carrier (`#3`). Right.
- `20260903-priced-levers#5`, `20260903-wall-and-heating#5`, `#6`, `#7`: applied or unchanged, each saying so. Right.

---

## 7. External mutation

`git log` over every cited path (listed in the checks above). Nothing moved outside its task:

- The study record was amended after `9df54941` by two Addenda (`9b1a4ef1`, `a5b0b96a`), both inside T-004's window (return at `f51b2915`), both appended under the study runbook's step-15 mechanism with `results/`, `snapshot.json` and the definitions untouched — the same ruling the round-1 reviewer gave. Not external mutation.
- The WI-041 item record last moved at `7bd87cb7` (the T-002 return), before the T-003 pin at `55c1f0ac`; it is unchanged since. Its status is `active`; close is owner-held.
- The twins: all 17 `.sysml` files under `exploration/stellarator_e2e/models/` are byte-identical to their canonical files (`cmp` per file); the three IFE-only library files and two IFE design directories have no twin by design (the spine test governs).
- `manifest.json`, `mfe_census.json`, `tests/study/data/`, the generated package, `stellarator.snapshot.json`, `verify_stellaris.py`, `oracle_entry.py`, `VALIDATION_MATRIX.md`, `traceability_matrix.csv`: last moved at `cb355321`, inside T-002. `tests/study/test_verify.py` at `7bd87cb7` (the disclosed planted-mismatch restatement), inside T-002.
- `goal.md` unchanged since grounding (`f937be2c`; Amendments: none). `learnings.md` unchanged since the round-1 review (`b5d50ba0`), correctly.
- `DISCOVERY_LOG.md`: `9df54941` (eight sightings) and `8906d4e7` (seventeen rows); the two earlier same-day rows (`646f062f`, `006acf55`) are the owner-present session's, before round 2's tasks.
- The owner's two commits (`368c37e5`, `f690b0cd`) touched `.project/`, `tests/orchestration/`, the narratives directory and **deleted `goals/wall-and-heating/SUMMARY.md`** — an owner act in the goal directory that no round-2 task cited; it voids nothing. They also added the contract test that F1 is about.
- `evidence/` gained `1928925b` (this review's prompt) after the result — the round agent's deposit, not a task artifact.

---

## 8. The battery

Run at HEAD `1928925b` with the prompt's exact invocations:

- `tests/models` (env sourced): **48 passed / 13 skipped** — matches the claim.
- `tests/study` (no `PYTHONPATH`; `.integration_workspace` removed first): **362 passed / 1 skipped** in 458 s. The round claims 359 / 1 at `cb355321`; the difference is exactly the three `test_records.py` instances parametrized over the new record directory (8 records × 3 + 1 = 25), which did not exist at `cb355321`. Consistent.
- `tests/study/test_records.py`: **25 passed** — matches.
- `tests/orchestration/test_goal_contract.py`: **27 passed / 2 failed.** The round reported 28 / 1 with the failure on the owner's untracked narrative. At HEAD there are two failures and only one is the owner's: `test_shipped_narratives_meet_the_snapshot_contract` fails on the untracked `20260904-234255Z-goal-overview.md` in the narratives directory (its first line is not the contract's heading). **`test_narratives_are_separate_from_the_goal_contract` fails on `trail.md` line 381** — the Round 2 result's evidence-refs bullet, which names that narrative's full path to explain the first failure, and the owner's test (added at `368c37e5`/`f690b0cd`, between T-003 and the record) asserts that no `goal.md`, `trail.md` or `learnings.md` contains the narratives directory's path. The round ran the test after `8906d4e7` (28 / 1, honestly reported) and then wrote the result entry at `f51b2915`, which introduced the string. See F1.

---

## 9. § Answered when, word by word

**(b)(i)** — *"the wall-load fence compares like with like — a computed peak operand against the printed peak limit … with the choice, its basis, and any verdict change at the baseline stated and never tuned away."* **Met by WI-041.** The operand is `wall_peak_calc.wall_load_peak` (`stellarator_plant.sysml:1243`), computed as the model's average times a calibration the model computes from six page-image facts; the limit is the printed 4.05; both are peaks on the source's own wall basis at the design point (SV-050: peak × 2700 / p_fus = 4.05 to float precision). The choice is stated (design D1–D5, the constraint def's doc, the rewritten cross-check block); its basis is stated (six citations to page images; the constancy assumption in the library and instance docs; the decomposition bounds as cross-checks); the verdict change is stated (violated at 4.088 by the 0.94 % fusion-power excess; SV-051; the manifest flipped) and nothing was tuned. The one honest qualification is built into the form: off the design point the "peak" carries the design point's peaking and shape factors (MR-WI041-7), which the study bounded with the shadow.

**(b)(ii)** — *"One committed study at a promoted pin sweeps the levers that reach wall load in this model (the geometry pair `R` and `a`, the power-density levers `n_e0` and `T_i0`, with `I_coil` and `p_input`) and reports whether a feasible region exists at the printed 50 MW installed, its LCOE, and what the machine pays to get under the wall through the consequence chain the model already carries."*

- *One committed study at a promoted pin:* `20260904-wall-and-heating` at `9df54941`, at the pin `c1b0f0d1…`, preflight 6/6, verification pass. Yes.
- *Sweeps `R` and `a`, `n_e0` and `T_i0`, with `I_coil` and `p_input`:* `R` with its tie, `a`, `n_e0`, `T_i0`, `I_coil` swept. **On `p_input` and "the printed 50 MW installed":** Table 2 prints "Required plasma-coupled ECRH power 50 MW", so the printed 50 MW is *plasma-coupled*; the goal's "installed" was the word for the model's then entry point `p_input = 50.0`, which `goal.md` § Grounding evidence itself labels plasma-coupled. WI-039 retired `p_input` as an entry point (restated, per § Invariants) and made `p_wallplug_heat` the entry, with coupled = wall-plug × `eta_source` × `eta_couple`. So the contract's `p_input` **is the coupled power**, and 100 MW wall-plug at the held 0.50 with the disclosed coupling 1.00 **is the contract's printed level** — the reading the round-1 review's constraint 1 fixed and the owner let stand. The question is asked *at* that level, so `p_input` is carried at it, with 220 MW as the strategy's second question; that satisfies "with … `p_input`" as I read it. The coupling at 1.00 is the optimistic end of a held assumption, disclosed at every claim.
- *Reports whether a feasible region exists:* **discharged** — yes, 257 driven points at a 1.5–2.2 m; **no** at the design's a 1.3 anywhere in the window, and no at 220 MW below 378.556 at the design geometry. The honest answer has both halves and the record states both.
- *Its LCOE:* **discharged** — 212.460 $/MWh at `c1721`, with the disclosure that the point sits on the `a` window's edge (so the number is an upper bound on an axis the model does not floor) and that the price survives the 1.15× end of the calibration band and not the 1.83× end (254.44).
- *What the machine pays through wall load → lifetime → CAS72:* **discharged** — per point as the lifetime charge above the limit (0–28 $/MWh over the violated points), size-matched as 14.07 / 15.07 against the wall's 26.54 / 17.08, with the finding that the chain never bounds the design and understates by construction (availability held).

*Are the four conditions disclosed facts of the model, or gaps that leave the question open?* The contract asks what happens "in this model" and "through the consequence chain the model already carries". (1) The held ash-transport ratio is a Table-4 input the model has carried since WI-037; the study measured that the sign of the `a`-response turns on it — a disclosed fact of the model, with the physical question (its aspect-ratio scaling) routed to research. (2) `a` unbounded and unpriced is a disclosed gap of the model; the record reads the optimum as an edge and prices the bore as a shadow — the report is honest about what the model lacks, and the contract does not ask the study to supply it. (3) The one-sided fence is handled: every claim is on the driven set. (4) The constancy assumption is WI-041's stated form, bounded by the shadow. None of the four leaves any of the three report obligations undischarged; each is a fact the record states at the claim site. **So (b)(ii) is answered, and the conditional positive is the honest form of the answer.** What remains open — whether the `a` the model favours is a machine — is a different question, which neither § Question nor § Answered when asks.

The close is the owner's (§ Close rule): "on the § Answered when condition, or by redirect at any round boundary." Both halves are met on my reading; the owner may weigh that the positive is on a re-shaped machine and the machine as designed does not open at the printed level at all — that reading is also in the record, plainly, and the owner can close on it or redirect.

---

## Findings

**F1 — The round result put the narratives directory's path into `trail.md`, and the owner's contract test now fails on the trail (material; owner-ruled).** `trail.md:381` (the Round 2 result's evidence-refs bullet) names the untracked goal-overview narrative by its full path. `tests/orchestration/test_goal_contract.py::test_narratives_are_separate_from_the_goal_contract` asserts that no `goal.md`, `trail.md` or `learnings.md` contains that directory's path. The round's "28 passed / 1 failed" was true when it ran (after `8906d4e7`); the entry written afterwards at `f51b2915` introduced the second failure. This is a premise conflict: the runbook's append-only rule bars editing the entry, and the owner's test bars the string. It is not the round agent's to resolve. Options for the owner: (a) rule a surgical redaction of that one path from the result entry, recorded by a dated amendment; (b) leave the trail as is and accept the failing assertion with the reason recorded; (c) relax the test to exempt citations. I recommend (a): the citation carries nothing the trail needs. Until ruled, **no goal file may gain that string** — the trail summary of this review must refer to the narrative by its basename, as this review does.

**F2 — L-010's "(at τ*/τ_E = 4 it rises)" rests on the critique's oracle probe, not executed data.** The reversal at τ = 4 (4.504 / 5.202 / 5.257 over a 1.3 / 1.8 / 2.2) is from `round2_T-004_precritique.md` F2, probed at R 14.2, I 14 MA, T 16 keV, n 0.8×. The record's only executed τ = 4 points are `c6307` (design column, a 1.3, 5.110) and `c6297` (the best column, a 1.8, 5.202), on different columns — there is no executed `a`-trend at τ = 4. The checkpoint already noted the probe is outside the record for `#2`; the learning must carry the same mark. Corrected below.

**F3 — L-013 rejected.** Two unrelated tooling gotchas (the second regeneration; the bare commit), each already recorded where it acts (WI-041 plan § Phase 5 / § Phase 6; the owner's auto-memory). Not one claim a later strategy acts on. The codegen point is carried as a constraint.

**F4 — `20260904-wall-and-heating#6` and `#8` got no joined row.** ADR-0004's mechanism is an appended row; round 1 appended under every one of its own sightings. Substance unaffected (the sightings carry class, status, actor, next reference; the checkpoint passed them). Land one joined row each at this review's landing, as round 1 did on its F4.

**F5 — The checkpoint's r1 text is no longer in the dispositions file.** Round 1's `§ Revision r2` form keeps the disagreement readable in the file; round 2's in-place `[r2]` marks leave r1 recoverable only at `9b1a4ef1`. Not a violation of the runbook's letter (the trail's `rK` entries are separate and unamended). Carried as a constraint.

**F6 — T-001's provenance sentence for the 1.5 m radius over-attributes.** The round-1 review derived r = 1.5 m from the arithmetic; the extraction's rewritten "1.5" coincides with it rather than being where it "came from". Substance right: 1.5 is printed nowhere and the images print 1.3.

**F7 — "Design column" names two columns.** The `a`-sweep's design column is the grid column at I 15 MA (`c0621`…`c1121`); the transect's design-column anchor is the baseline at I 15.4 MA (`c2973`). The numbers are right everywhere; a reader of § 6 should know that "the machine as designed is feasible and driven at a = 1.7" is at 15 MA, not the design's 15.4 MA. Record is frozen; no edit — noted for the next record's vocabulary.

---

## Learning delta rulings (the forms to append to `learnings.md`)

## L-009 — Under the honest fence the printed heating level opens only by geometry, and only conditionally: nothing at the design's minor radius at any (R, I, T, n) in the window, and nothing by heating below a source efficiency of 0.92 at the design geometry

- **Evidence:** `exploration/stellarator_e2e/studies/20260904-wall-and-heating/record.md` § 4, § 6 `a`, § 15 #1 (`@9df54941`; Addenda `@9b1a4ef1`, `@a5b0b96a`); `synthesis.md` § 2.1, § 7 (i); `results/points.csv`: 0 feasible of the 501 a-1.3 rows in `arm-fence-p100` (ignited included); 257 feasible driven at a 1.5–2.2, cheapest `c1721` 212.460 (R 14.2, a 2.2, I 15 MA, T 16 keV, n 0.9×); on the grid column (R 12.7, I 15 MA, T 14.63, n 1.0×) the single feasible driven `a` is 1.7 (`c0821`, 257.35). The 0.92: of the 36 sustainment-alone points at 100 MW in `20260903-wall-and-heating/results/points.csv`, 9 pass the honest wall (average × 1.316440857 ≤ 4.05) and the least needs 92.11 MW coupled; this record's a-1.3 sustainment-alone floor is 100.78 MW (150 points). Recounted by the round-2 reviewer, agreeing on every number.
- **Scope:** the WI-041 pin `c1b0f0d1…`; windows R 11.2–17.2, a 1.3–2.2, I 13–18 MA, T 14.63–18 keV, n 0.6–1.0×; `eta_source` 0.50, `eta_couple` 1.00 (optimistic), τ*/τ_E 8. The 0.92 is at (R 12.7, a 1.3) on round 1's grid (I 14–17 MA, T 14.63–22 keV, n 0.9–1.2×); efficiency reaches only `sustainment_ok` at fixed wall-plug. Conditions, each disclosed at the claim site: the held ash-transport ratio (L-010); no bound or price on `a` (the optimum is the window's edge at both levels); the one-sided sustainment fence (every claim on the driven set); the calibration's constancy, bounded by the shadow (257 / 142 driven survivors at 1.15× / 1.83×, the optimum not among the 142). No buildability claim.
- **Implication:** no round spends a study on heating or field alone at the printed level; the next question is whether the `a` the model favours is a machine — the transport facts' aspect-ratio scaling (a research seam) and a bound on `a` (a model item) before any geometry result is more than conditional.
- **Supersedes:** none; refines L-001 with the honest fence in place.
- **Accepted by:** round 2 review, 2026-09-05 (corrected: the 0.92 scoped to the design geometry on round 1's grid; the a-1.3 count given with its denominator).

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

**L-013 — rejected** (F3). Not appended.

---

## Constraints carried forward

For whatever follows — the owner's close, a redirect, or a new goal on the geometry question:

1. Every geometry claim on this package carries the τ*/τ_E, `f_suppr_ash` and `iota_23` constancy condition at the claim site until the aspect-ratio research request lands (L-010); a τ = 4 `a`-trend is a probe until executed.
2. Every study on this package exports `ignited` and reports on `feasible_driven` (L-012).
3. `a` is not read as a design lever until it is bounded or priced (`#3`); any window on `a` discloses its edge; the magnet-bore shadow is a shadow, not a price.
4. The calibration is re-anchored, never swept; a re-shaped machine needs a new anchor (WI-041 D4); the wall-anchor shadow bounds the anchor's value, not its constancy.
5. A trail entry never carries a path under the narratives directory (the owner's contract test; F1) — and the summary of this review in the trail must not either.
6. The checkpoint's revision keeps r1's text in the file and appends the revision as a section (the round-1 form; F5).
7. Every id the round's evidence touches gets an appended row, including the round's own sightings that discharge or declare in the sighting (F4).
8. The task scope, start line and any amendment are committed before execution, so "before any point ran" is in git, not only in the trail.
9. A manual-stage interface change is regenerated twice; the codegen's backup directory is deleted before the second run (WI-041 plan § Phase 5).
10. Commits carry an explicit pathspec — the owner keeps files staged.
11. Carried unchanged from round 1: any baseline verdict change disclosed and never tuned; the record contract (no `<`; `effective_executable_fingerprint` on every arm; `test_records.py` before the commit); no two arms share a point; a transect's held level read off its anchor's operands; multi-field outputs exported oracle-side; every fresh gate a spawned non-author session with its prompt deposited first.

---

## Close packet — for the owner to rule on

1. **The (b) ruling.** (b)(i) is met by WI-041. (b)(ii) is answered by `20260904-wall-and-heating`: the three report obligations are discharged, and the four conditions are disclosed facts of the model the contract accepts. The alternative reading — that a positive on a re-shaped machine is not "the machine" — is also in the record, plainly; the owner closes on § Answered when or redirects.
2. **WI-041 close** through the modelling PM: `uv run agentic-mbse pm close-item WI-041`; archive to `work/completed/`; a trail amendment redirecting citations (the WI-039 precedent); the spec's `Status: active` reconciled at close. The plan's phases are already ticked with their records and § Spec success criteria verified.
3. **Three model candidates, not minted** (one-pin/one-study bound): a bound on the minor radius and a re-anchoring rule for the calibration (`#3`); a coil-bore term in the magnet chain's winding length and casing mass (`#3`, the WI-036 seam, WI-036 archived); a second sustainment inequality `p_aux_required ≥ 0` or a burn-control lever (`#4`). Plus the follow-on `goal.md` already names: the lifetime → availability coupling (`#5`, `20260821-power-cycle-ab#1`, Row 2b). Mint or carry.
4. **One research request:** the aspect-ratio scaling of τ*/τ_E, helium suppression and the ISS04 iota in QI stellarators (`#2`), through `scripts/research_seam.py`, with the Helios/HELIAS screen in the prompt (L-008).
5. **Added by this review:** (a) the F1 ruling on the trail string — redact by dated amendment, accept the failing assertion, or relax the test; (b) two joined rows under `20260904-wall-and-heating#6` and `#8` (F4) and the L-009..L-012 landing in `learnings.md`, both the round agent's acts on this review; (c) if the owner wants the geometry question pursued, ground it as its own goal ("is the minor radius the model favours a machine?") with its own § Answered when — it is outside this goal's § Question, and a round 3 here would be a plan, not an experiment; (d) a coding-PM tooling note: the study manifest's verdict schema cannot carry a derivation beside a flipped expectation (WI-041 plan § Phase 6) — worth a backlog line, not a ruling.

---

## Recommendation

**Close the goal on § Answered when.** The heating half was met in round 1 and confirmed by the owner; the wall half is now met on both of its clauses — the fence compares a computed peak with the printed peak on the source's own basis, with its basis and its violated baseline stated and untuned, and one committed study at one promoted pin reports, over every lever the contract names, that a feasible driven region exists at the printed level at 212.46 $/MWh but only at a minor radius 1.15–1.7× the design's, never at the design's own, and that the lifetime chain charges 0.53–0.88 of what the wall is worth and bounds nothing. Every one of those numbers reproduces from `results/` and every condition on them is a disclosed fact of the model, not an open obligation. What is left — whether the larger machine is real — is a new question with three named model candidates and one research request already homed, and it is better grounded as its own goal than run as a round 3 under a contract it does not belong to. Round 2 of 6; the goal has room, but the reason to close is that it is answered.
