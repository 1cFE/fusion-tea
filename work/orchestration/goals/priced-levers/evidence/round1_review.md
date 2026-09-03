# Round 1 review — goal `priced-levers` — the review of record

Fresh non-author session, 2026-09-03, spawned from the deposited prompt `round1_review_prompt.md`; no inherited context. Deposited verbatim by the round agent (the reviewer edits no file). Trail entry: `trail.md` § Round 1 review.

---

**Verdict: FINDINGS**

The round is valid: every number I recounted reproduces, every cited artifact resolves and says what the trail claims, the seven dispositions landed as class-bearing rows, the battery is green, and the checkpoint sequence is intact. The findings are corrections to the round's *reading*, not to its evidence. The largest one changes what the owner should be told: the round result reads the study as "the deadlock is the wall, not the magnets, so WI-038 is not the lead." That holds by count. It does not hold by cost. The study's own `points.csv` contains a 50 MW point blocked by nothing but the conductor ceiling at **262.08 $/MWh, 3.4% under the 110 MW optimum (271.359), before the conductor grade is charged**. Nobody in the chain (record, synthesis, dispositions, checkpoint, round result, draft goal) reports it.

## Grounds

1. **F1 (reading, material).** L-001, the `20260901-sustainment-fence#1` disposition row, and the draft goal's ruling 3 all say the conductor escape is closed or minor. The data: at 50 MW, 6 points are ceiling-alone; three of them (`c0148/c0164/c0180`: I 17 MA, T 17 keV, n 1.0×, B_peak 27.49 T, σ 656–789 MPa, strain 0.263%, wall 3.886, required heating 22.4 MW) read 262.08–262.16 $/MWh. The 110 MW optimum reads 271.359. T-001's own basis prices the 24.9 → 27.49 T step at ×1.06 (α = 0.6) to ×1.16 (α = 1.5) in tape. The conductor-grade escape is **untested, not negative**. The wall-alone points, by contrast, sit ≥1.42× over the wall limit and are not candidates.
2. **F2 (reading).** The round result's "bounded negative on the field escape" is a bounded negative on the *pack-sizing* lever only (WI-036: relief nearly free, opens nothing with `B_max` held). The strategy's study question named both fences priced; one was.
3. **F3 (premise superseded, unrecorded).** `goal.md` § Amendment 2026-09-02 says "raising `B_max` alone opens no feasible region at 50 MW". At this pin with T swept, raising it to ≥27.49 T opens the three points above with no stress relief needed. The round noticed the T-held artifact for the ceiling-vs-wall question and not for this one.
4. **F4 (process).** T-007's scope and start were written after execution. The reconstruction is honest; the lapse had real costs (below).
5. **F5 (defect recorded).** `snapshot.json` was edited after commit. Acceptable as done; a defect against step 15 all the same (below).
6. **F6 (minor).** Citation imprecisions in the draft goal and chain map (below).

## Checks

### Cited refs

Opened and confirmed: all commits `0288d099`…`523df924`, `aa638133`, `76876b82`, `30b651f0`; cited shas `62a1fa7b f9663df8 dd0b5896 81a4fee8 dc0f0b6d fc80e5b2 0cf0cf41 6bc81157 728d1263 7cb6a48d efd6befc 4f3dd511` all resolve. Seven registered sources exist under `knowledge/sources/` with `output.md`, MANIFEST and SOURCE_INDEX entries; five seam runs (`REQ-038-01/02`, `REQ-036-01/02/03`) with `return.json`; REQ-036-03 `queued[]` carries the arXiv:2409.01925 refusal (`term:aries-cs matched 4x`) and Pierro 2019.

Quoted lines verified verbatim: PPPL-5297 `output.md:95-99` (666 / "Optimistic … 800 MPa") and `:137` (reallocation of cross-section); Titus IAEA `:75` (Sm 666, yield only), `:99` (2.0Sm peak; 1.5Sm "where local plasticity may affect insulation bonding"), `:468` ("1GPa Peak, 666 PM"); Barth `:167/:173/:197` (SuperOx 0.45–0.47% at 4.2 K/19 T, delaminates); Molodyk `:85/:101` (over 1000 A/mm² at 20 K, 20 T) and `:93` (α ≈ 0.6 at 20 K, pinning force saturates ~15 T); Bottura `:97` (150–200 USD/kA·m); Zhang `:79/:104` (77 K, ≤400 mT); Zhai `:41` (~200 MPa transverse). 1costingFE at `0254385`: `defaults.py:96-108`, `:609-617` (`rebco_hts b_max=23.0`), `costing_constants.yaml:56` (50 $/kA·m "aggressive NOAK target"), `:153` (fluence 18).

Model lines verified: `stellarator_plant.sysml:1061-1077` (flat-wall-average cross-check comment), `:1079-1081` (`wall_load_limit = 4.05`, peak), `:1103-1106`, `:636`, `:648`, `:842`, `:510`, `:472`, `:498-502`; `mfe_plasma_scaling.sysml:52`; `mfe_plasma_sustainment.sysml:26-30` (ISS04 with `R^0.64`, the checkpoint's correction); `mfe_power_balance.sysml:136`; `mfe_account_costs.sysml:196`. T-006 return: `CANDIDATE`, ten gates pass, pin `6262dbf4…`, census 197, teax `744745f8`. `VALIDATION_MATRIX` SV-044..047 present. BACKLOG: WI-036 `active` with the goal named; WI-038/039 `backlog`. `grading.md@fc80e5b2`: R2a 3, R2b 2, R2c 1, R4.P 1, R4.S 2. `p-pump-fence/synthesis.md:69` ("constant in R to 12 significant figures") and `:49-50`.

**Imprecisions (F6):** draft goal cites `mfe_account_costs.sysml:794` for `core_lifetime_FPY`; the calc def is at `:796`, the line at `:803`. `R1_model_chain_map.md` cites `data/defaults/costing_constants.yaml:56`; the path is `src/costingfe/data/defaults/costing_constants.yaml`. Draft goal § Question says the model "reads 3.13 at the design point" (the WI-022 doc comment); the pinned baseline row `c0064` reads 3.105.

### Recounts (mine, from `results/points.csv` + `oracle_operands.csv`)

| Quantity | Trail / record+Addendum | Recount |
|---|---|---|
| Violations wall / peak / sust / stress / recirc / beta / strain / net / tbr | 264/144/132/32/15/3/0/0/0 | same |
| Points per arm, feasible | 240/192/7; 0/87/7 = 94 | same; `feasible` = all nine satisfied on every row |
| p50 wall-alone / ceiling-alone / sust-alone | 27 / 6 / 12 | same |
| p50 sustain-satisfied; clear sust+ceiling and fail wall | 141; 30 of 30 | same |
| The 27's span | I {15.0, 15.4}, T {17,18,19}, n {1.2,1.4}, wall 5.76–9.23, heating −47.8…+49.3, negative at 12 | same |
| Optimum | `c0381` 271.359 @ 15.2 MA, j 130, T 18, n 0.9, wall 4.043 | same |
| 14.63 keV slice best; delta | 288.004; 16.645 | same (`c0275`) |
| Transect magnet capital / LCOE / vol_cold / cryo | 5,401,032,000 flat; 365.572→365.206; 270.45→115.91; 20.98M→16.00M | same |
| Max strain (study / transect); points over 0.2% | 0.286% (`c0224`) / 0.235%; 323 | same |
| `wp_stress_ok` violations | 32, all 18 MA, p50 | same |
| Wall load vs I at T 14.63, n 1.0, j 90, p 50 | 3.1748 → 2.6835 (15→18 MA) | same |
| Baseline `c0064` | 307.087, strain 0.217%, sustainment violated | same |
| Predecessor recount (R1): p50 rows / sust-ok / peak-ok / stress-ok / two-fence-only / cheapest | 176 / 29 / 0 / 0 / 11 / 332.95 | same |
| Indicators: `j_wp` objectives; `B_max`, `sigma_allow`, `eps_cond_allow` | no `magnet_capital`; 1 constraint / 0 objectives | same |

**Not in any artifact:** the 6 ceiling-alone points' LCOE (262.08–393.07; three at 262.08–262.16); ceiling overshoot 1.10–1.17× vs wall overshoot ≥1.42×; the 12-point region blocked only by ceiling and/or stress, cheapest 262.08 (the R1 "two-fence" region at this pin: 11 points at 332.95 became 12 at 262.08 once T was swept).

### Goal and strategy fidelity

Round 1 pursued the declared priced-field-lever strategy: research (T-001/T-002), move (1) WI-036 through spec/design/implement (T-003..T-005), integrate (T-006), move (3) the study (T-007). Move (2), WI-038, was never executed.

**Reading of the narrowing:** legitimate, not drift. It was declared at the T-001 return ("move (2) narrows…") after a recorded premise surprise, it respected the one-pin bound, and the study declined `B_max` as a traced pure fence-relaxer (record § 8), which is the right call for an unpriced lever. **But** the narrowing left the strategy's study question ("with the field lever priced on both fences…") half-answered, and the round result then claimed the whole ("bounded negative on the field escape"). The abandonment condition is conjunctive and is not met (a labelled-extrapolation basis exists); the result's "met on its second half" is loose. The round closed on trigger 1 regardless, so the close stands; the over-claim is F2.

T-002 was not in the strategy's three moves. It was owner-directed in session, scoped before start, and served the strategy's premise. Not drift.

### Task scopes T-001..T-006

Each task's commit file list stays inside its scope: `c845da9d`/`8817c207` touched only `knowledge/`; `efd6befc` BACKLOG + spec + VALIDATION_MATRIX; `c15078be` design only; `4f3dd511`/`7f0e41e7`/`d35e9571` models, staged twin, generated, `verify_stellaris.py`, `oracle_entry.py`, `study_route.py`, manifest, ANNEX, `tests/` (all named in T-005's scope per carried constraint 6); `1de78121` evidence only. No `sigma_allow` change anywhere. No discovery-log write before T-007.

### T-007: the after-the-fact scope

**What it cost.** (a) The authorization record was written by the person checking the work against it, so the reviewer inherits a circularity: the reconstruction could only fit the work. (b) The executing session ended after `76876b82` with no return and no stop, which is the interruption case the start line exists to leave a trace for; the resumer found the task only because the record named itself "task T-007". (c) Step 15's fail-closed check was not run before commit: two record-contract failures, and a `snapshot.json` edit after commit followed (F5). (d) Five prose misstatements in the record were caught only by the fresh administrator. (e) The retry question below is undecidable from the goal trail alone; the study record is the only witness.

**Is the reconstruction honest?** Yes. It is marked in three places, names its sources (T-006's named next task, strategy move (3), the owner's verbatim intake at record § 2), and its exclusions check out: `aa638133` and `76876b82` touched only the study directory and the log's five sighting rows; no `models/` edit, no WI-038 work, no second pin, no disposition rows. The resumer also followed § Resuming an interruption correctly (native artifacts as truth, missing return written).

**For future rounds:** a scope and start line precede `/run-study`, and `tests/study/test_records.py` runs before a record is committed. L-006 says this; I accept it as a carried constraint below.

### Retry classification

**Ruling: not a goal-level retry.** The runbook's retry is a `MECHANICAL_FAILURE` return followed by a new `### T-00N start`. T-007 never returned; the blank `aux_cooling__cryo_cost` column was corrected inside the study seam's own steps (a harness export declaration in `study.py:214-215,312`), and the pin, windows, points and question were identical. It counts against no cap. The boundary: had the first execution been *committed*, a re-execution would have been a second study in the round, and would have had to be classed a retry or a violation of the one-study bound. It was not committed. The disclosure in the T-007 return and record § 13/§ 15 #4 is what makes this rulable; the after-the-fact start line is why it had to be ruled here rather than read off the trail.

### Checkpoint sequence

C-001.r1 `REVISE` → C-001.r2 `PASS`, both entries present in the trail; 1 of 2 revisions used; spawn prompt deposited. `T-007_proposed_dispositions.md` keeps the r1 text above § Revision r2, and the r1 row 1 still carries the withdrawn "`R` cancels" sentence, which is proof it was not edited in place. The reviewer's correction is right: `mfe_plasma_sustainment.sysml:26-30` carries `R^0.64` in ISS04 and `points.csv` shows the `I_coil` route (3.1748 → 2.6835). Note: both submissions and the appended rows landed in one commit (`523df924`), so git does not independently witness the r1→r2 order; the document does. The checkpoint reviewer's own return is not deposited as a file, matching the predecessor's practice; the runbook requires the trail entry, which exists.

### Discovery rows

Seven disposition rows appended 2026-09-03 (`DISCOVERY_LOG.md:74-80`), `523df924` +7/−0 on the log, sightings (`:69-73`) untouched. Each row carries class, status, responsible actor, concrete next reference, `Checkpoint C-001.r2 PASS`, and a Home. Did each finding move?

- `#1` `model fix`: from "candidate follow-on" to a drafted goal with a three-part next reference and a corrected mechanism. Moved.
- `#2` `model fix`: from `unrouted` to a proposal with two named homes and a decision owner. Moved, but only to a pending choice (draft ruling 6).
- `#3` `research`: gains the queued Pierro fetch and the 0.286% correction. Moved.
- `#4` `declared seam`: second recorded failure of the class plus a named hardening candidate (the ADR-0003 record). Moved.
- `#5` `declared seam` (re-classed at checkpoint): a study-design constraint in the draft goal and runbook step 7. Moved.
- `20260901-sustainment-fence#1` `model fix`: premise re-measured with T swept. Moved, **but the row's "is not the lead" is the over-read of F1.** A row is never edited; the correction goes into WI-038's annotation (draft ruling 7) and into any later row under this id.
- `20260901-sustainment-fence#4` `model fix`: consumer moved to a drafted goal; numbers sharpened. Moved, thinly.

No touched row returns unrouted.

### Did any cited native artifact move outside its task?

`git log` over `models/`, `work/active/WI-036_*`, the study directory, `DISCOVERY_LOG.md`, `work/BACKLOG.md`, `VALIDATION_MATRIX.md`, `knowledge/`, `tests/`, the staged twin, `verify_stellaris.py`, `oracle_entry.py`, `ANNEX.md`, and the two predecessor records: every commit falls inside the task that cited it; the `20260901-sustainment-fence` and `20260829-p-pump-fence` records have not moved. Working tree clean.

**The `snapshot.json` edit at `30b651f0` — ruling.** Step 15 says `snapshot.json` is never edited. The diff is eighteen added lines and nothing removed: `arms[].effective_executable_fingerprint` on each of three arms, value equal to the sealed fingerprint the snapshot already carried; digest `838ec6a9…` → `59049340…`, both named in § 16 and Addendum B.2, with the synthesis stamping the old digest. **Record it as a defect against step 15, with the edit accepted as done.** The root defect is that the fail-closed check did not run before the commit, so the record was committed failing its own contract. The repair adds no evidence and changes no value; it makes explicit an identity already present. Leaving it would have failed every future study battery on this record. It is not precedent: an additive, identity-only, disclosed repair after a skipped closure check is the only shape this covers, and the fix is procedural (L-006), not a new rule.

### Battery (re-run here)

- `tests/models`: **48 passed, 13 skipped** (11.2 s).
- `tests/study`: **356 passed, 1 skipped**, zero failures (7 min 23 s).

Both match the round result's counts.

### § Answered when

**(a) heating half:** untouched. R4.P still 1. Nothing in this round bears on it.

**(b) conductor half:** not met as written. The `B_max` cost consequence chain is not active (MD-1: one inequality, nothing else); the stress chain is (WI-036). The sourced-negative branch is not met either: a labelled extrapolation basis exists (Molodyk α ≈ 0.6 at 20 K; the 8↔20 T bracket). What the evidence adds is that the question inside (b) is now *sharp*: a specific candidate at 50 MW is blocked by the ceiling alone and reads cheaper than the heating escape before pricing. That is exactly what WI-038 was minted to charge, and this study did not charge it.

**Continue or close by redirect?** Plainly: **close by redirect, with the conductor half recorded as open, not negative.** Two reasons for closing now rather than running round 2 on WI-038: the owner's same-day direction points at wall and heating; and the wall fence as bound compares a flat-wall average against a printed peak limit, so an honest wall fence may close *both* escapes (3.886 × 1.41 ≈ 5.5 and 4.043 × 1.41 ≈ 5.7, both over 4.05, if the source's peak-to-average ratio transfers). Pricing the conductor step before the wall fence is honest would measure a comparison that may not survive. WI-038 belongs after the wall half, and the close packet must say so in words that do not let a future session read WI-038 as "minor fence". The alternative (round 2 on the conductor half) is written out below in case the owner would rather finish (b) first; all its inputs are in hand.

### The `wall-and-heating` draft

**Grounding evidence: honest.** The wall-fence shape claim reads off the model text as stated; the `R`/ISS04 correction is carried; `R+tie` 8/9 and `a` 5/9 match `indicators.json`; p-pump-fence citations, grading cells, 1costingFE lines, and the pinned baseline (nine verdicts, `sustainment_ok` violated, `cond_strain_ok` satisfied) all verify. The [AGENT] 1.41 arithmetic is labelled as scale, not claim.

**Restating vs citing:** it carries (a) verbatim with the inheritance marker and ruling 3 on the redirect, which is right for a self-contained answered-when. The § Invariants ISS04 paragraph should cite `priced-levers/evidence/T-007_proposed_dispositions.md § Revision r2` as the correction's record alongside the model lines. The three imprecisions in F6 apply.

**The seven rulings:** the right set, with two corrections and one addition.

1. Slug: fine.
2. One goal or two: right question; one goal is defensible. Add for the owner: the heating half needs no research seam and is grade-shaped, so it is the cheaper first round; the wall half likely needs a research round first. The first strategy should choose explicitly.
3. **Must be corrected before the owner rules.** Its justification says priced-levers' "conductor half is answered in the sourced-negative direction (the conductor ceiling alone blocks 6 of 240 p50 points; the escape is not conductor grade)". Replace with: the conductor half is *redirected open* — the cheapest 50 MW candidate is ceiling-blocked at 262.08 vs 271.359, unpriced; WI-038 prices it and follows the wall half.
4. Yardstick: right.
5. Gates re-ruled, not inherited: right.
6. Routing of `#2`: right; WI-036 follow-on is the sensible recommendation.
7. WI-038 annotation: right, and the annotation text must carry the candidate (`c0180`: 262.08 $/MWh at 27.49 T, 10% over the ceiling, 22.4 MW required against 50, tape ×1.06–1.16), not "minor fence".
8. **Missing:** none for the new goal itself. The clean-room §6 ruling on arXiv:2409.01925 and the WI-036 close belong to priced-levers' close packet, below.

## Learning delta rulings

- **L-001 — corrected.** *At the printed 50 MW and held geometry, the machine sustains itself under the conductor ceiling only where the wall stops it, and the one cheap candidate left is ceiling-blocked.* Evidence: 141/240 sustain at 50 MW; all 30 that also clear the ceiling fail the wall (27 wall-alone, ≥1.42× over 4.05); 6 ceiling-alone, three of them (`c0148/c0164/c0180`, I 17 MA, T 17 keV, n 1.0×, B_peak 27.49 T, σ ≤ 789 MPa, required heating 22.4 MW) at 262.08–262.16 $/MWh against the 110 MW optimum 271.359, before the conductor grade is charged (T-001 basis: ×1.06–1.16 in tape for that step). Scope: pin `6262dbf4`, R 12.7 / a 1.3, T 14.63–19 keV, n 0.8–1.4×, `B_max` held, wall fence as bound. Implication: by count the wall is the blocker at 50 MW; by cost the conductor ceiling is; WI-038 decides which, and runs after the wall fence is made honest because a tighter wall fence may close both escapes. Refines L-005; supersedes `goal.md` § Amendment's "raising `B_max` alone opens no feasible region at 50 MW" at this pin.
- **L-002 — corrected.** *A lever is priced only when the cost account that owns the material it moves responds, and `indicators.json` shows that before any point runs.* Evidence: `j_wp` reaches `lcoe`, `total_capital`, `cas72` (through cryo) and not `magnet_capital`; magnet capital delta exactly zero over 2.33×; ~85% of the pack's mass has no account (design D8). Implication: a study scope names the account that should carry what the lever moves and confirms the lever reaches it; reaching LCOE through a side channel is not pricing.
- **L-003 — accepted, one tightening.** Keep as proposed. Add: 16.645 $/MWh is the difference of two window- or fence-bounded optima, not a slope; the 110 MW optimum is window-bounded in T (18 keV) and `j_wp` (130) with the wall 0.007 MW/m² away, so "wide enough" means the next window extends past 18 keV until the wall catches it.
- **L-004 — corrected to one claim.** *`sigma_allow` is not a lever, and the reason is the conductor, not the steel.* Evidence: read as a peak check the steel rule would allow ~1000 MPa (Titus IAEA `:99/:468`; the category assignment is a reading, not a sourced statement); the conductor's axial limit re-tightens at nearly the same place (SuperOx 0.45–0.47%, Barth `:173/:197`); transverse limits the model cannot see are ~200× tighter (Zhai `:41`; Lu 2025 unregistered). Implication: no strategy opens a region by moving the stress fence; the two-check form is built and inert at 0.4% (study max 0.286%); a 0.2% limit would flip the baseline (0.217%) and 323/439 points, a disclosed verdict change if ever adopted. The tape-vs-Lorentz asymmetry (×1.12 / ×1.45 for 24.9 → 30 T) is WI-038's pricing input and lives in L-001's pointer, not as a separate learning.
- **L-005 — accepted as written.** Add the open owner ruling: PROTOCOL §6 on arXiv:2409.01925 (leave refused, or grant).
- **L-006 — corrected title, body accepted.** *Write the task scope and start before invoking `/run-study`, and run `tests/study/test_records.py` before the study commit.* Evidence: this round (no T-007 scope/start; two record-contract failures; five misstatements caught only by the administrator's recount). Implication as proposed, plus: the administrator's recount is load-bearing.

## Constraints carried forward

1. Standing rulings, unchanged: one pin + one study per round; SV-016 recorded against, never fitted; `p_pump` held settable; `vol_cold_cryo` settable (verified surviving in the 197-key census); Anchor A closed; clean room in full.
2. Five prior committed studies are not reproducible as written at `6262dbf4…` (MR-WI036-11 restatement); any replay drops `wp_side`/`c_coil`, re-reads `vol_cold_cryo`, expects nine verdicts.
3. The baseline's `sustainment_ok` violation stands; `cond_strain_ok` is satisfied at 0.217% and flips at a 0.2% limit — any change to `eps_cond_allow` is a disclosed verdict change.
4. `sigma_allow` is not a lever (L-004). `B_max` is a free inequality (MD-1); no study at this pin sweeps it until WI-038 gives it a consequence.
5. T is a search axis in every fence study on this package, with a window past 18 keV (L-003 / `#5`).
6. Scope-writing hygiene (predecessor constraint 6) plus L-006: scope and start before `/run-study`; `test_records.py` before the study commit; every gate session's spawn prompt deposited.
7. Research subagents carry the clean-room screen before any fetch (L-005).
8. Account reachability is checked in `indicators.json` before a lever is called priced (L-002).
9. Geometry is unmeasured for wall load at this pin; `R`'s sign is open; the wall fence compares an average operand to a peak limit.
10. Study-tooling debt filed beside `#4`: `verification_summary.json` lists nothing under `not_independently_verified` while three oracle-side-only classes exist; `teax.revision` unrecorded; a declaration-time channel-shape guard is the named hardening candidate.
11. The `snapshot.json` repair is a recorded defect, not a precedent.

## Recommendation: owner-held close by redirect, with this packet

**The answer to the goal's question as the evidence stands.** Conductor grade: half real. The structural half of the field lever is now physics (σ ∝ √I; cold volume drives the cryoplant) and almost no economics (magnet capital flat to the dollar over 2.33× cross-section; LCOE 0.100%) because ~85% of the pack's mass has no cost account. The conductor-grade half (`B_max`) is still a free inequality. Heating: untouched; one linear line and a held ratio. At 50 MW and this geometry no feasible point exists (0/240; 0/3072 in the scan). The most common sole blocker is the wall (27 of 240; 264/439 overall), and every point that sustains under the ceiling exceeds the wall limit by ≥42%. The cheapest sole-blocked candidate is ceiling-blocked at 262.08 $/MWh (17 MA, 17 keV, 27.49 T), 3.4% under the 110 MW optimum before the conductor is charged; the sourced tape penalty for that step is ×1.06–1.16. So the model still answers "which escape is cheaper" for free in the conductor's favour. Making the wall fence honest may close both escapes; it does not change their order.

**Owner rulings the close needs:**
1. Close `priced-levers` by redirect at the round-1 boundary: (a) moves to `wall-and-heating`; (b) is recorded **open**, not negative, with WI-038 as its vehicle, sequenced after the wall half.
2. WI-038's backlog annotation, verbatim candidate: "`20260903-priced-levers` `c0180`: I 17 MA, T 17 keV, n 1.0×, p 50 MW, B_peak 27.49 T vs 24.9 ceiling, all other verdicts satisfied, 262.08 $/MWh vs 271.359 at 110 MW, conductor unpriced; tape ×1.06–1.16 (T-001). Run after the wall fence is honest."
3. `wall-and-heating` ruling 3's justification corrected per F1 before grounding; ruling 7's annotation as above; the three F6 imprecisions fixed.
4. WI-036: close (implemented, battery green, pin promoted, study committed, D8 disclosed), or hold open pending the `#2` cost-home follow-on (draft ruling 6). Recommendation: close; mint the follow-on separately.
5. PROTOCOL §6 on arXiv:2409.01925: leave refused (nothing depends on it) or grant.
6. Accept the corrected learning delta above into `learnings.md` at the close (the review writes it; nothing has been appended yet).

**Not-final cautions.** The 262 candidate is one (I, T, n) cell at 1 MA / 1 keV / 0.1× resolution; its required heating comes from the oracle side (not independently verified, like every `p_aux_required`); the `B_max` basis above 20 T is a labelled extrapolation licensed to the SuperOx family; the 110 MW optimum is window-bounded in T and `j_wp`; the wall fence's operand and limit are not the same quantity; `#2` means pack relief is still nearly free, so any 50 MW candidate's stress margin costs nothing to buy.

**If the owner prefers to finish (b) first — round 2 strategy, `priced-conductor-ceiling`:** one item, WI-038: `cost_per_kAm` becomes a function of required peak field by the T-001 composition (quantity ∝ 1/J_E(B), J_E ∝ B^−α, α = 0.6 held and sourced to Molodyk, labelled extrapolation above 20 T, SuperOx-licensed), with the Lorentz consequence already landing through WI-036's σ(B_peak); `B_max` stays settable with its basis stated. Study: p = 50 arm over I 16–18 MA × T 16–18 keV × n 0.9–1.1× × `j_wp` with `B_max` swept as a priced axis; question: does the priced conductor escape at 50 MW undercut 271.359. Abandon if the composition needs any defaulted number. Six rounds remain; this is one. I do not recommend it ahead of the wall half, for the reason given.
