# Synthesis — `20260829-p-pump-fence`

- **Administrator:** fresh administrator session, no memory of the run
- **Date:** 2026-08-29
- **Mode:** administer
- **Record directory read:** `exploration/stellarator_e2e/studies/20260829-p-pump-fence/`
- **`snapshot.json` sha256 read:** `f59a698e611c36fca7e893d4b2fc3f34c6c542e227fdf47990d4d8e5e701eeea` (matches the value `record.md` § 16 states)

**What this administrator read.** Only this directory: `record.md`, `snapshot.json`, `indicators.json`, `axes.json`, `study.py`, and all seven files under `results/`. Where the record cites another study's record by path, that citation was followed to check a quoted number; nothing else outside the directory was opened. Every number below was recomputed from the committed artifacts unless it is marked as quoted or as missing.

**Confirmation this is a record directory.** It carries `record.md` with the seventeen numbered sections of the record contract, a `snapshot.json` under schema `study-record-snapshot/v1`, and a `results/` tree whose seven files all match, byte for byte, the sha256 digests `snapshot.json` records for them. Read as a record.

---

## 1. What the study set out to do

The owner's question, quoted in § 2: *"With `p_pump` re-based to 195 MW, where does the `recirc_ok` fence move, and what happens to LCOE?"* The contract for an answer was a committed, verified study on the regenerated pinned package that locates the fence and quantifies the LCOE shift at the baseline point against the 1.0 MW record — with an adverse or inconclusive reading explicitly counting as an answer.

So the study owes two things, and they are separable: a **fence location** and an **LCOE shift**. It ran one arm (`arm-package-default`), 948 proposed points over R 4.0–20.0 m (step 0.5) and a 0.80–2.20 m (step 0.05), of which 906 evaluated.

**What was held or assumed, all recorded before the points ran.**

- `p_pump` = 195.0 MW is a **held package input**, not a study axis. No point in this study moves it. `results/oracle_operands.csv` carries `p_pump_MW = 195.0` on all 906 rows and on no other value.
- `availability` held at 0.85, `discount_rate` held at 0.07. Both were declared and traced, then declined by owner ruling `[OWNER 2026-08-29] "decline those"`. The record is straight that the "no sensitivity" rationale is carried precedent from `20260821-power-cycle-ab`, not a fresh argument of this study.
- The window was **adopted, not scanned** — the runbook's step-7 scan was substituted by owner ruling, so that the fence positions subtract against the comparand's on the same grid. Its provenance is recorded as `engineered` in both § 11 and `snapshot.json` `arms[0].window.provenance`.
- 42 points were pre-screened out on `p_net > 0` with the package-owned oracle, under an execution-detail ruling by the orchestrator citing an existing pattern.
- The comparison target is `20260821-power-cycle-ab` `arm-rankine-paper` **at its own pin**, quoted rather than re-run.

The two rulings that most shape the result are the adopted window and the evaluability exclusion. Both are disclosed at the point of use, not buried.

## 2. What it found

**The LCOE half — answered, and with a large number.** At the baseline geometry (R 12.7, a 1.3), `results/points.csv` (`is_baseline_point = True`) and `results/baseline_result.json` both give `lcoe` = 333.0670332813743 and `lcoe_1cfe` = 326.5124757805328. Against the comparand's 275.264 that is **+57.803, +21.0 %**. All six verdicts are `satisfied` at that point in both artifacts. The re-basing moves the objective by a fifth without flipping a verdict there.

**The fence half — located in `a`, unbounded in `R`.** `recirc_ok` is violated at 184 of the 906 evaluated points. Recomputed from `results/points.csv`, the largest violating R at each `a` reproduces § 6's table exactly, from R ≤ 20.0 m at a = 0.80 down to R ≤ 4.0 m at a = 1.70. The comparand's fence was 32 points, bounded at R ≤ 8.0 m for a = 0.80 and gone above a = 1.10 m. So the fence did not merely move; it changed shape — from a small-machine corner to a band that spans the whole R range of the window at small `a` and persists eight grid steps further in `a`.

**And at a = 0.80 the window no longer contains it.** Every R from 4.0 to 20.0 m violates at that minor radius, so the study cannot say where the fence would be if R ran further. The record says this plainly in § 6, § 11, § 15 and § 17 rather than reporting "violated up to R = 20.0" as if 20.0 were a fence.

**No constrained optimum.** The best feasible point is 225.72504 $/MWh at (20.0, 1.65) — recomputed from `results/points.csv`, as are the neighbours 225.79268 at 19.5 and 226.50144 at 17.5. It sits on the window's R edge with the objective still falling, so the record declines to call it an optimum. That refusal is correct and it is the honest reading of its own data.

**Feasibility collapsed.** 370 of 906 feasible = 40.84 % (recomputed), against the comparand's 563 of 948 = 59.4 %. Measured against the 948 originally proposed, 39.03 %.

**The exclusion is itself a result.** 42 points have oracle `p_net` from −154.411 MW at (4.0, 0.80) to −0.899 MW, where the CAS10 land term takes the square root of a negative and the package returns `execution_failed`. `results/excluded_points.csv` carries all 42 with their `p_net` and the reason. The staircase in § 11 reproduces exactly. The boundary is sharp: the smallest `p_net` among the evaluated points is +0.06058 MW at (8.0, 0.85), recomputed from `results/oracle_operands.csv`.

## 3. Framing verdict per axis

| Axis | Proposed | Judged | Administrator's assessment |
|---|---|---|---|
| `R` | search | search, unchanged | **Correct, and the run earned it.** `indicators.json` reports `constraints_reachable` for `net_positive`, `recirc_ok`, `wall_load_ok`, 7 of 8 objectives, 55 modules fired. The run then produced real verdict structure on this axis — 184 `recirc_ok` violations distributed by R. Search framing is what the axis did. |
| `a` | search | search, unchanged | **Correct.** Same indicator reach; the run resolved two fences as functions of `a`. `wall_load_ok` is violated at every a ≥ 1.70 for every R — 353 points, which is exactly the 11 `a` values at and above 1.70 times 33 R values, less the 10 mask-excluded nodes. That arithmetic closes. |
| `availability` | not proposed | not run | Declined by owner ruling; `no_constraint_response` (0 of 6 constraints; objectives `cas72`, `fuel`, `lcoe`, `lcoe_1cfe`) confirmed in `indicators.json`. Held at 0.85 in `snapshot.json`. No account owed and none claimed. |
| `discount_rate` | not proposed | not run | Same: `no_constraint_response` (0 of 6; objectives `cas72`, `lcoe`, `lcoe_1cfe`) confirmed. Held at 0.07. |

Both declined axes carry a model-development finding as the runbook requires, and both correctly cite the comparand's existing ids (`20260821-power-cycle-ab#1`, `#2`) rather than re-minting. The record states outright that the ruling does not discharge the finding.

**The indicator vocabulary is used correctly.** § 8 restates the not-derivable disclosure and does not read `constraints_reachable` as a claim that a constraint responds. No monotonicity claim in the record is sourced to the indicator run; the monotonic recession of the fence in `a` (§ 5, § 6) is read off the executed points, which is legitimate.

## 4. Constraint structure

Recomputed over all 906 evaluated points from `results/points.csv`:

| `source_local_identity` | Result | Administrator's note |
|---|---|---|
| `beta_ok` | satisfied ×906 | Inert. `indicators.json` lists it `constraints_unreachable` for both swept axes, so this is structural, not luck. |
| `peak_field_ok` | satisfied ×906 | Inert, same basis. |
| `tbr_ok` | satisfied ×906 | Inert, same basis. |
| `net_positive` | satisfied ×906 | **Reachable but never violated — and the record is right that this reads misleadingly.** It is satisfied everywhere only because the 42 points where net power goes negative cannot be evaluated at all. See § 15 finding #1 below. |
| `recirc_ok` | violated 184 / satisfied 722 | The fence the study exists to locate. |
| `wall_load_ok` | violated 353 / satisfied 553 | Wall load is 4.16469 MW/m² at a = 1.70 against the 4.05 limit (`results/points.csv`), constant in R to 12 significant figures. `p_pump` does not enter it. |

No `indeterminate` verdicts. Four verdict combinations, recomputed: 370 all-satisfied, 352 wall-load-only, 183 recirc-only, **1 both** — at (4.0, 1.70). The comparand recorded three combinations and stated that no point violates both; following that citation confirms the sentence. That single point is a small but real structural change.

**Gates and verification.** All six preflight gates ran and passed (`results/preflight_results.json`), including the baseline headline reproducing at relative deviation 0.000e+00 with 6 of 6 pinned verdicts matched, and the package git-clean. Verification passed: 48 rows sampled stratified across all 4 observed verdict combinations, 10 channels at tolerance 1e-9, worst relative deviation 6.3463e-16, all six constraints re-derived from the oracle's own operands, zero verdict mismatches, `not_independently_verified` empty (`results/verification_summary.json`). Every figure § 9 and § 13 state matches the artifact. The `snapshot.json` digests match all seven `results/` files and both `indicators.json` and `axes.json`.

**Administrator's reading of the evidence quality.** This record is unusually well closed. Every headline number in §§ 3–6 and § 11 was recomputed here from `results/points.csv`, `results/oracle_operands.csv` and `results/excluded_points.csv`, and every one reproduced — verdict counts, combination counts, fence positions per `a`, feasible fraction, best-feasible point and its two neighbours, wall-load value at the fence, the exclusion staircase, the `p_net` range and the sharp boundary. Nothing in §§ 3–6 was found overstated by the arithmetic.

## 5. Assessment of each § 15 finding

**`#1` — the unevaluable region intrudes 42 points into the studied window (`model`). Sound, and arguably the more important of the two model findings.**
The evidence carries it: 42 rows in `results/excluded_points.csv` with oracle `p_net` from −154.411 to −0.899 MW, and `net_positive` reading satisfied at all 906 remaining points. Following the record's citation, the comparand states `net_positive` satisfied at every one of its 948 points including the (4.0, 0.80) corner at p_net = 8.3 MW — so the same corner going to −154.4 MW here is a genuine change, not a re-description. The finding is stated at the right strength: it routes the mechanism to the existing `20260823-magnet-technology-ab#1` rather than re-minting, and claims only that the region now overlaps the space studies actually sweep.
If anything it is **slightly understated in one respect**: the record notes the misleading reading of `net_positive` in § 4 but the finding text itself does not say that a constraint's clean sheet is being manufactured by the exclusion. A downstream reader who takes "`net_positive`: satisfied at all 906" out of § 4 without the note attached would be misled. The record does attach the note; the finding could carry it too.

**`#2` — the adopted window no longer contains the `recirc_ok` fence (`model`). Sound, and correctly scoped as a window limit rather than a machine result.**
Recomputed: at a = 0.80, all 22 evaluable R values violate; the best feasible point is at R = 20.0, the window's edge, with LCOE still falling (225.725 at 20.0 < 225.793 at 19.5 < 226.501 at 17.5). The disposition — no constrained optimum claimed, widen the window if the R extent is wanted — matches what the data supports exactly. Its home, "runbook step 7 — an inherited window needs a re-check that the fence is still in frame," is the right generalization: the defect is not that the window was adopted but that adoption skipped the check that the adopted frame still bounds the thing being measured.

**`#3` — the annex restates a pinned headline as a stale literal (`process`). Plausible and internally coherent, but this administrator cannot verify it from the record.**
`ANNEX.md` is outside the record directory, so the claim that it contains `275.2642200420774` beside a sentence deferring to `manifest.json`, and that no test reads it, is unverifiable here. What the record *does* support is the premise: the comparand's pinned headline was 275.264 (§ 3, and confirmed at the cited comparand record) and this package's pinned headline is now 333.0670332813743 (`snapshot.json` `manifest.content_used.baseline.headline`, and the preflight baseline gate passing at 0.000e+00 against it). So a literal of the old value stated anywhere as the current pin would indeed be stale. The finding is **sound on its premises and unverifiable on its object** — that is a limit of the administer seam, not a weakness of the finding. Its disposition (filed, not fixed, homed to the annex) is right; a study should not edit package documentation.

**No finding appears overstated.** The stronger observation is about what is *not* in § 15 — see the process finding at the end of § 6 below.

## 6. What the record does not support

Everything here is either a fact this administrator could not recover from the record directory, or a claim the directory's evidence does not carry. The record's own § 17 anticipates most of the first group; the items marked **not in § 17** are ones it does not.

**Facts the record itself declares missing, and this administrator confirms are missing.**

1. **Where the `recirc_ok` fence lies in R at a ≤ 0.85.** The window ends at R = 20.0 m and the fence has not closed there. "Violated up to R = 20.0" at a = 0.80 is a window edge, not a fence position.
2. **A constrained LCOE optimum.** 225.725 $/MWh is the best point *in this window*, on its boundary, with the objective still decreasing.
3. **Anything about the 42 excluded points beyond `p_net` and the reason.** No LCOE, no capital, no verdicts.
4. **Any package-side number at a `p_pump` other than 195 MW.** The 130 and 150 MW figures are the oracle's alone.
5. **A comparand re-run.** All 1.0 MW numbers are quotations at another pin. A difference caused by anything other than `p_pump` would be invisible here.
6. **Any claim about `availability` or `discount_rate`.** Declared, traced, declined, unswept.

**Facts MISSING that § 17 does not list.**

7. **MISSING — the 130 / 150 MW near-fence band table has no artifact in the record.** § 6 reports fence reach 16.0 m and 17.0 m, baseline `rec_frac` 0.26629 and 0.28371, and LCOE 311.122 and 317.554 at those held values. None of those seven numbers appears in any file under `results/`, and none can be recomputed from anything in the directory. The record says in § 13 that the band re-evaluation is oracle-only — that discloses the *method*, not the fact that the numbers were never deposited. This matters because those numbers carry the record's own margin statement: the claim that both headlines survive the whole sourced band rests entirely on figures a cold reader cannot check. The runbook's step 13 requires every number in the report to trace to a committed artifact.
8. **MISSING — the sourced 130–195 MW band for `p_pump` and its attributions.** § 6 attributes ~130 MW to Moscato's 8-loop design and ~150 MW to Cismondi's preliminary 9-loop figure, sourced to "the goal". No artifact in the record carries that band or those citations.
9. **MISSING — `rec_frac` on the excluded set.** § 11 states it runs 1.0027 to 1.8787. `results/excluded_points.csv` carries only `R`, `a`, `reason`, `source`, `p_net_MW` and `p_net_is_complex`. The direction of the claim is implied by `p_net < 0`, but the two endpoint values are not in the record.
10. **MISSING — the provenance of three of the four cells in the 1.0 MW column of § 3.** The column is cited to `20260821-power-cycle-ab/record.md` § 3. Following that citation, `lcoe` = 275.264 is there. `lcoe_1cfe` = 269.862, `p_net` = 915.081 and `rec_frac` = 0.151362 are not in that section, and the comparand's own record states that its per-point `p_net` and `rec_frac` columns are empty and that its corner values come from an oracle scan. The comparand's oracle scan records the baseline as `p_net` 915.1 and `rec_frac` 0.1514 — fewer digits than this record quotes. So the derived cells "−162.668" and "+0.171" are stated to a precision no source reachable through the record's own citation chain carries. This does not touch the headline: the LCOE shift, which is the claim the owner asked for, traces cleanly to 275.264 and reproduces at +21.0 %.
11. **MISSING — the teax revision.** `snapshot.json` `teax.revision` is `"unrecorded"` and `results/verification_summary.json` says the same. A reader who wants to reproduce these numbers has the package fingerprint, the manifest digest and every tool digest, but not the version of the simulation kit that ran them. § 17 does not mention this.
12. **MISSING (minor) — the package identity fields in the snapshot.** `snapshot.json` `package.identity_kind` and `package.identity_digest` are both `null`, though `results/preflight_results.json` and `results/package_identity.json` record kind `sealed` and digest `f97f0848…`. Recoverable from elsewhere in the same directory, so this is a snapshot completeness nit, not a gap in the evidence.
13. **Unexplained (minor) — two package paths.** `indicators.json` records the package at `exploration/stellarator_e2e/pkg/stellarator_tea`; `snapshot.json`, `results/preflight_results.json` and `results/verification_summary.json` all record `exploration/stellarator_e2e/generated`. The fingerprints agree across both (`f08daa7b…` semantic, `f97f0848…` executable), so this administrator's reading is that the two paths denote the same package content. The record does not say so, and nothing inside the directory establishes it.

**Claims the directory's evidence does not license.**

14. **The cross-pin comparison.** § 12 is candid that this record cannot license comparing across the two fingerprints and that the licence lives at the goal layer, in the audited single model delta. The administrator cannot see the goal layer. So the *specific* claim that the +21.0 % shift is attributable to `p_pump` and to nothing else is **not established by this record**; what this record establishes is that LCOE at the baseline geometry is 333.067 under this pin, and that the comparand published 275.264 under its own. That is exactly what § 12 says, and it is the right disclosure — the administrator restates it here because it is the single most quotable number in the study and the one most likely to travel without its caveat.
15. **The stale-annex finding's object**, per § 5 above.

**A process finding this administrator files against the record contract, not against the study.** The record's § 17 is thorough about substantive gaps and silent about artifact gaps. Items 7, 9 and 11 are all cases where the record's prose carries numbers or reproduce-prerequisites that no committed artifact holds, and the runbook's own step 13 and step 15 language ("every number traces to a committed artifact", "state what the record does not contain") points at exactly this. The gap is that § 17 is written as a list of *findings* the study lacks rather than a list of *numbers* the record cannot back. A record-contract check that walked the report's numbers against `results/` would have caught all three.

---

## Headline reading

**Answered, on the question as asked — with one half of the answer bounded by the window and not by the machine.**

The LCOE half is answered outright and verified: +57.803 $/MWh, +21.0 %, at the baseline geometry, with all six verdicts still satisfied there, reproducing from committed artifacts at 0.000e+00 baseline deviation and 6.3e-16 worst verification deviation. The fence half is answered in `a` and **unbounded in R**: the fence grew from a 32-point corner to a 184-point band that reaches the window's largest R at a = 0.80, so the study locates how far the fence moved but not where it now ends. The study says so itself rather than reporting the window edge as a fence, and it declines to claim the constrained optimum that its own best-feasible point would have invited. That refusal is the strongest thing about the record.

