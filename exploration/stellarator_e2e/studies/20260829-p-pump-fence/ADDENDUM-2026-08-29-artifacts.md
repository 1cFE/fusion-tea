# Addendum — 2026-08-29 — the numbers the record stated and did not deposit

**Addendum to:** `record.md` of study `20260829-p-pump-fence`
**Author:** the study's executor session, GSTH Item 6, goal `p-pump-fence` round 1
**Raised by:** the fresh administrator's `synthesis.md` § 6, items 7, 9, 11, 12, 13 and 10
**Why an addendum and not an edit:** `.claude/skills/run-study/runbook.md` step 15 — once committed, a record is corrected by appending, and `snapshot.json`, `indicators.json` and `results/` are never edited.

## What this addendum does and does not touch

**Nothing already committed changes.** `record.md`, `snapshot.json`, `indicators.json`, `axes.json`, `study.py` and all seven files under `results/` stay byte-identical. This file is new, and the three artifacts it deposits are new, under a new `addendum/` directory.

**`snapshot.json` is deliberately not edited, and its quoted sha256 stands.** Items 11 and 12 below are corrections to values that live *inside* the snapshot. Editing it would change its sha256 `f59a698e611c36fca7e893d4b2fc3f34c6c542e227fdf47990d4d8e5e701eeea`, which is quoted in three committed places — `record.md` § 16, the administrator's `synthesis.md` header, and the goal trail's `### T-004 return` — and every one of those citations would silently become wrong. So the corrected values are stated here in prose, and the snapshot keeps the values it was committed with. A reader who wants the true teax revision or the true identity kind reads this file; a reader checking the snapshot's digest against any of the three citations still gets a match.

**The three new artifacts are self-certifying.** Each is listed below with its own sha256, computed at the time this addendum was written. They are not in `snapshot.json`'s `results` map and were never intended to be — that map is frozen at the seven files the run deposited.

**The `studies/2026*` byte-unchanged invariant, read explicitly.** `goal.md` § Invariants says "Committed prior records are not touched — `exploration/stellarator_e2e/studies/2026*` stays byte-unchanged," and the path this addendum writes matches that glob. Surfacing the tension rather than assuming it away: the invariant's own heading is **"Committed prior records"** and its stated reason is that older records' pins no longer match the live package, so a comparison that needs the old numbers must read them out of the old record. This round's own record is not a prior record and carries no stale pin — it *is* the current pin. `.project/active/goal-integration-study-proof/plan.md` § "Two standing constraints on every phase" says the same thing in the same words and for the same reason: "do not touch any directory under `exploration/stellarator_e2e/studies/2026*` … Their pins will no longer match the live package after Phase 1." The invariant protects `20260821-power-cycle-ab` and `20260823-magnet-technology-ab`, and both remain byte-unchanged. Correcting this round's own record by the mechanism the runbook prescribes for it is the intent, not an exception to it. If a later reader disagrees, the glob is what should be narrowed, not this addendum reverted.

---

## Item 7 — the 130 / 150 MW near-fence band table now has an artifact

`record.md` § 6's near-fence re-evaluation stated seven numbers that no committed file held. The administrator was right to call this a step-13 violation, and it was the most load-bearing of the gaps because the record's whole margin statement rests on it.

**Deposited:** `addendum/near_fence_band.csv` — sha256 `de43653be639a892ebec0f6bfdd999d7aa6e758dff772968f5714bc6bd2e5dff`

| `p_pump` held | `recirc_ok` violated up to R at a = 0.80 | baseline `rec_frac` | baseline `p_net` (MW) | baseline `lcoe` | shift vs 275.2642200420774 |
|---|---|---|---|---|---|
| 130.0 MW | 16.0 m | 0.26629 | 806.915 | 311.122 | +13.03 % |
| 150.0 MW | 17.0 m | 0.28371 | 790.145 | 317.554 | +15.36 % |
| 195.0 MW | 20.0 m | 0.32251 | 752.413 | 333.067 | +21.00 % |

Every figure reproduces what § 6 stated. The 195.0 MW row is the package's own held value and its `lcoe` matches `results/points.csv` at `is_baseline_point = True` and the pinned baseline gate.

**Also deposited:** `addendum/near_fence_knife_edge_points.csv` — sha256 `8e1389f1aa9430462917cc894e8daff9321681bd440343bf1856595fb6c0e903` — the four grid points § 6 names as deciding the fence at the fourth decimal, each across all three band values. It carries the fact that most qualifies the margin statement: (16.0, 0.90) and (9.0, 1.20) read `violated` at 195 MW and `satisfied` at both 130 and 150 MW, so an individual fence *position* is band-sensitive even though the fence's *scale* is not.

**Derivation, stated so the numbers can be recomputed rather than trusted.** Each row is the independent oracle `verify_stellaris.py` driven through the package-owned seam `oracle_entry.py`, at the study's own held `availability` = 0.85 and `discount_rate` = 0.07, with the oracle's module-global `p_pump` set to the stated value for the duration of the call and restored afterwards. The fence reach is the largest `R` in `study_route.R_VALUES` at a = 0.80 whose `rec_frac` exceeds the 0.5 threshold and whose `p_net` is positive and real — points that are unevaluable are skipped rather than counted as satisfied. `p_pump` is read from the oracle rather than swept in the package: **no package run exists at 130 or 150 MW**, the source column of the artifact says so on every row, and `p_pump` remains a held input that no point of the committed study moves.

**Where the band comes from.** ~130–195 MW is the goal's sourced range, not this study's: `work/orchestration/goals/p-pump-fence/goal.md` and, behind it, `models/designs/stellarator_09/stellarator_plant.sysml:502`'s doc comment, which records ~130 MW as the documented lower bound (Moscato's near-term 8-loop design) and Cismondi's ~150 MW as a preliminary figure for one unoptimized layout. This discharges the administrator's item 8, which asked where the band and its attributions live: outside the record, and now cited by path from inside it.

## Item 9 — `rec_frac` on the excluded set now has an artifact

`record.md` § 11 stated that `rec_frac` runs 1.0027 to 1.8787 across the 42 excluded points. `results/excluded_points.csv` carries `R`, `a`, `reason`, `source`, `p_net_MW` and `p_net_is_complex`, and not `rec_frac`.

**Deposited:** `addendum/excluded_points_rec_frac.csv` — sha256 `46981ba687ac2b62f055c6c3bd1d7757a52d6f673866a11491224f5147e0870e` — 42 rows joining `results/excluded_points.csv` on `(R, a)`, each carrying `rec_frac` at the package's held `p_pump` = 195.0 MW. Range reproduces exactly: **1.0027 to 1.8787**. Every row is above 1.0, which is the substantive point — recirculating power exceeds gross electric everywhere in the excluded region, so these are not marginal points that happened to fail a numeric guard.

## Item 11 — the teax revision, recorded

`snapshot.json` `teax.revision` reads `"unrecorded"` and `results/verification_summary.json` says the same. The value was **not unavailable**. It is:

> `744745f895677f3344b9884627369a6a47ed987f`

It was in hand throughout: gate 1 of every `scripts/integrate.py` invocation this round reported "teax is at 744745f895677f3344b9884627369a6a47ed987f, matching the expected," including run 5, the invocation that returned the `CANDIDATE` this study ran against (`work/orchestration/goals/p-pump-fence/evidence/integration-run-5/integration_return.json`). Recording it as unrecorded was an executor error and not a limit of the tooling. The administrator was right to call it a reproduce prerequisite rather than a nicety: a reader had the package fingerprint, the manifest digest and every tool digest, and not the version of the simulation kit that produced the numbers. That reader now has it here.

## Item 12 — the snapshot's null identity fields, corrected in prose

`snapshot.json` `package.identity_kind` and `package.identity_digest` are both `null`. The values exist in the same directory and are:

- **kind:** `sealed`
- **digest:** `f97f084818723224bdd7f604a63e1941dadeb3e99af0cca3c9c6d30280d312f0`

Source: `results/package_identity.json` → `identity.kind` and `identity.digest`, corroborated by `results/preflight_results.json`'s identity gate. The cause of the nulls is mundane and worth naming so it is not mistaken for a missing fact: the snapshot builder read `kind` and `digest` at the identity document's top level, and both live one level down under `identity`. As the administrator says, this is snapshot completeness rather than a gap in the evidence — everything needed was already committed inside the record directory.

## Item 13 — the two package paths, stated, no repair

`indicators.json` records the package at `exploration/stellarator_e2e/pkg/stellarator_tea`; `snapshot.json`, `results/preflight_results.json` and `results/verification_summary.json` record `exploration/stellarator_e2e/generated`. The administrator's reading — that the two denote the same content, because the fingerprints agree across both — is correct, and here is what establishes it:

**`exploration/stellarator_e2e/pkg/stellarator_tea` is a tracked symlink to `../generated`.** The two paths are the same directory. The tools differ in whether they resolve it: `scripts/study/preflight.py` and `verify.py` resolve before digesting, because the identity verifier forbids a symlink as the package root, while `indicators.py` records the path it was handed. Both spellings appear because the seam's own documented invocation names the `pkg/` alias.

No repair. The addendum states it, which is what the administrator asked for — nothing inside the record directory established it, and now something does.

## Item 10 — the over-precise cells in the 1.0 MW column

`record.md` § 3's comparison column cites `20260821-power-cycle-ab/record.md` § 3 for four cells. Only one of them is there. The corrected attribution:

| Cell | Value as printed in § 3 | Where it actually comes from | Correction |
|---|---|---|---|
| `lcoe` 275.264 | 275.264 | the comparand's § 3 `arm-rankine-paper` row | **Correct as cited.** The +21.0 % headline rests on this cell alone and is unaffected by everything below. |
| `lcoe_1cfe` 269.862 | 269.862 | not in the comparand's § 3 | Attribution wrong; the comparand does not publish this cell in the cited section. |
| `p_net` 915.081 | 915.081 | the comparand's oracle scan, which records 915.1 | **Over-precise.** Three digits claimed beyond the source. Should read ≈915.1, and the derived shift ≈−162.7 MW rather than −162.668. |
| `rec_frac` 0.151362 | 0.151362 | the comparand's oracle scan, which records 0.1514 | **Over-precise.** Should read ≈0.1514, and the derived shift ≈+0.171. |

The two derived cells the record prints — `−162.668` and `+0.171` — inherit that over-precision and should be read as ≈−162.7 MW and ≈+0.17. The administrator's judgement that this "does not touch the headline" is correct and is repeated here so a reader of the addendum does not over-correct: the LCOE shift, which is the claim the owner asked for, traces cleanly to 275.264 and reproduces at +21.0 %.

## What this addendum does not do

- It does not re-open any finding in `record.md` § 15, and it does not add one. The type error the goal round found in finding `20260829-p-pump-fence#2` — it is typed `model` and the defect is in the study process — is recorded in the goal trail and in that finding's discovery-log disposition, not corrected here, because § 15 is frozen and its id is what the log joins on.
- It does not touch the excluded points' other channels. The package produces no LCOE, no capital and no verdicts there, and that remains true.
- It deposits no package-side run at 130 or 150 MW. Producing one would mean regenerating the package at a different held value, which is outside this study.
