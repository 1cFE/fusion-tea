# Synthesis (hand route) — `20260829-p-pump-fence`

- **Administrator:** hand operator, route-equivalence exercise (GSTH Item 6, Phase 6). A session that did not execute this study.
- **Date:** 2026-08-29
- **`snapshot.json` sha256 read:** `f59a698e611c36fca7e893d4b2fc3f34c6c542e227fdf47990d4d8e5e701eeea` (recomputed with `sha256sum`; matches `record.md` § 16)
- **Scope of this read:** the record directory only — `record.md`, `snapshot.json`, `indicators.json`, `axes.json`, `results/`, `ADDENDUM-2026-08-29-artifacts.md`, `addendum/`. No package, no manifest, no discovery log, no work items.
- **Disclosure:** written before opening the committed `synthesis.md`. It is not a blind read, and cannot be — the record directory contains an addendum that cites the first administrator's numbered findings. See § 6.

## 1. What the study set out to do

Record.md § 2 carries the owner's question verbatim: with `p_pump` re-based to 195 MW, where does the `recirc_ok` fence move, and what happens to LCOE. The answer contract, also quoted there, requires a committed verified study on the regenerated pinned package that locates the fence **and** quantifies the LCOE shift at the baseline point against the 1.0 MW record, with an adverse or inconclusive reading still counting as an answer.

Two halves, and the record addresses both. The comparand is named in § 2 as `20260821-power-cycle-ab` arm `arm-rankine-paper`, chosen because the package's own held `eta_th` and cost rates are that arm.

## 2. What it found

**My reading class: a valid, positive reading that answers both halves, with one bounded limit on the fence half.** It is not adverse and not inconclusive. The LCOE half is answered exactly; the fence half is answered in position and character over most of the window and is explicitly unbounded in R at small `a`.

**The LCOE half (§ 3).** At the baseline geometry (R 12.7 m, a 1.3 m), `lcoe` moves 275.264 → 333.067 $/MWh, **+57.803, +21.0 %**; `lcoe_1cfe` 269.862 → 326.512, also +21.0 %; `p_net` 915.081 → 752.413 MW; `rec_frac` 0.151362 → 0.322514. I recomputed the 195 MW column from `results/points.csv`: the single `is_baseline_point = True` row is at R 12.7, a 1.3 with `lcoe` 333.0670332813743. It reproduces exactly. All six verdicts stay satisfied at that point — a fifth added to the objective with no verdict flip there.

**The fence half (§ 6).** I recomputed the whole geography from `results/points.csv` and it reproduces row for row: `recirc_ok` violated at 184 points, and the largest violating R at each `a` matches § 6's table at all nineteen values of `a` (a = 0.80 → R 20.0 with 22 points, down to a = 1.70 → R 4.0 with 1 point).

The fence did not merely move; it changed kind. At 1.0 MW the comparand recorded a small-machine corner — violated at R ≤ 8.0 m at a = 0.80, 32 points, gone above a = 1.10 m. At 195 MW it spans the window's entire R range at a = 0.80 and persists to a = 1.70 m. **That is the study's central finding, and it is a scale change, not a shift.**

**The evaluability boundary (§ 11), which I read as the second real result.** 948 points proposed, 42 pre-screened out because `p_net` < 0 makes the CAS10 land term take the square root of a negative. I confirmed from `results/excluded_points.csv`: 42 rows, `p_net` from −154.411 to −0.899 MW. The comparand evaluated all 948 at 1.0 MW with `net_positive` satisfied everywhere. So the unevaluable region was entirely outside the evaluated space at 1.0 MW and now intrudes 42 points into it. **My reading:** this is a stronger statement about the re-basing than the verdict counts are, because those 42 points are where the machine fails hardest and they are exactly the ones the model cannot speak about.

**Verdict counts (§ 4).** Recomputed from `results/points.csv`: all satisfied 370, only `wall_load_ok` violated 352, only `recirc_ok` violated 183, both violated 1 — matching § 4 exactly. Feasible fraction 370/906 = 40.8 %, against the comparand's 563/948 = 59.4 %. The both-violated combination does not occur in the comparand at all.

**Best feasible LCOE.** 225.72504062332928 at (R 20.0, a 1.65), recomputed. The record does not call it an optimum, and § 3 gives the reason: it sits on the window's largest R with the objective still falling (225.725 at 20.0, 225.793 at 19.5). I agree with that refusal; it is the honest reading.

## 3. Framing verdict per axis

Four axes declared in `axes.json`, two swept.

| Axis | Framing | Indicator (`indicators.json`, § 8) | My verdict on the framing |
|---|---|---|---|
| `R` | search | `constraints_reachable` — `net_positive`, `recirc_ok`, `wall_load_ok` | **Correct, and the run bears it out.** A search framing owes feasible structure, and § 6 delivers a fence table per `a`. |
| `a` | search | `constraints_reachable`, same three | **Correct.** The feasible band is bounded from both sides — `wall_load_ok` above, `recirc_ok` below — which is structure only a search framing would report. |
| `availability` | declared, traced, declined | `no_constraint_response` (0/6) | **Appropriate.** Declined by recorded owner ruling `[OWNER 2026-08-29]`, held at 0.85, and the model-development finding is carried under the comparand's existing id `20260821-power-cycle-ab#1` rather than re-minted. |
| `discount_rate` | declared, traced, declined | `no_constraint_response` (0/6) | **Appropriate**, same shape, carried under `20260821-power-cycle-ab#2`. |

`R` carries a declared `tie` key, `stellarator_09__stellaris__magnet__R0`, alongside the `fan_out` key `stellarator_09__stellaris__R`. **My reading:** this is the one declaration that could not have been found by scanning, and `axes.json`'s note says it is declared identically to the comparand's so the two fence positions are comparable key for key. That is what makes the "how far did the fence move" question answerable at all.

Both search-framed axes correctly record their sensitivity sections as not applicable, and both declined axes record no claim in either section.

## 4. Constraint structure

Six constraints, named by `source_local_identity` with qualified `constraint_id` in § 4.

- **Two respond.** `recirc_ok` (184 violated / 722 satisfied) is the fence the study was run to locate. `wall_load_ok` (353 / 553) is violated at every a ≥ 1.70 m for every R, identical to the comparand — wall load depends on `a` at fixed profiles and `p_pump` does not enter it.
- **Three are inert by construction.** `beta_ok`, `peak_field_ok` and `tbr_ok` are satisfied at all 906, and § 4 says why for each: no axis here touches `magnet__B` or the profiles, B_peak sits at B_max, TBR is a bound input.
- **One is misleading, and the record says so itself.** `net_positive` reads satisfied at all 906 **only because the 42 points where it would fail cannot be evaluated**. § 4 flags this and § 15 files it. **My reading:** this is the most important single line in the constraint table. A reader who takes "satisfied at all 906" at face value draws the opposite conclusion from the correct one, and the record is right to refuse to let that stand unqualified.
- No verdict is `indeterminate`.

**Verification (§ 13).** Passed: 48 rows sampled stratified by verdict combination, 10 channels against the independent oracle at 1e-9 tolerance, worst deviation 6.35e-16, zero verdict mismatches, `not_independently_verified` empty. § 13 also states four things verification did *not* cover — the 42 excluded points, the oracle-derived operand columns, the 130/150 MW band, and `p_fus`. **My reading:** stating the non-coverage at that granularity is what makes the "passed" credible.

**Preflight (§ 9).** All six gates ran and passed, each with its own detail. The identity gate's digest `f97f0848…` is the same executable fingerprint the record carries throughout, and the baseline gate reproduces the pinned headline at relative deviation 0.000e+00.

## 5. Findings carried forward

Three in § 15, each with an id, a kind, a disposition and a non-blank home.

1. **`#1` (model)** — the unevaluable region intrudes 42 points into the standard window. Disposition: excluded and disclosed as an evaluability bound; the underlying `sqrt(p_net)` mechanism stays routed under `20260823-magnet-technology-ab#1` and is not re-minted. Home: a modeling item — the guard must survive a net-negative point.
2. **`#2` (model)** — the adopted window no longer contains the `recirc_ok` fence. Disposition: stated as a window limit, no constrained optimum claimed. Home: runbook step 7 — an inherited window needs a re-check that the fence is still in frame. **My reading:** this is the finding with the longest reach, because it is about the study procedure rather than this package. Adopting a comparand's window buys grid comparability and silently inherits the assumption that the fence is still in frame. Here that assumption failed and only the fence table's shape revealed it.
3. **`#3` (process)** — `ANNEX.md § Baseline pin` restates a pinned headline as a literal that went stale on re-pinning, detected by no test. Filed, not fixed. Home: the documented seam.

The record also carries an **addendum** (`ADDENDUM-2026-08-29-artifacts.md` plus three CSVs under `addendum/`) depositing artifacts for numbers the record stated without depositing, and correcting two values that live inside `snapshot.json` in prose rather than by editing it — so the quoted sha256 stays true for the three places that cite it. **My reading:** that is the right call, and the addendum argues it explicitly rather than assuming it.

## 6. What the record does not support

Mandatory section. Everything I could not recover, plus the claims the directory does not carry.

**Carried from § 17, and I confirm each is genuinely absent from the directory:**

- Where the `recirc_ok` fence lies in R at a ≤ 0.85. "Violated up to R = 20.0" at a = 0.80 is the window's edge, not a fence position. I verified from `points.csv` that R = 20.0 is the largest R present.
- A constrained LCOE optimum. 225.725 is the best point in this window, not a minimum.
- Anything about the 42 excluded points beyond `p_net` and the reason — no LCOE, no capital, no verdicts. Confirmed against `excluded_points.csv`.
- Any package-side number at a `p_pump` other than 195 MW. The 130 and 150 MW figures are the oracle's.
- A comparand re-run. The 1.0 MW numbers are quoted from another record at its own pin.
- Any claim about `availability` or `discount_rate`.
- Monotonicity claims from the indicator run.

**Additional limits I found, which § 17 does not list:**

- **The comparand's numbers are unverifiable from inside this directory.** Every 1.0 MW figure — 275.264, 915.081, the 32-point fence, 563/948 — is quoted from `20260821-power-cycle-ab/record.md`, which is outside the record directory. An administrator reading this directory only takes them on the executor's word. Since one half of the answer contract is a *shift* against those numbers, **half of the study's headline result is not checkable at the administrator's scope.** This is a limit of the record contract, not of the study; I file it as a process observation against the contract, per the administer instructions.
- **The comparability licence is external by design.** § 12 states plainly that the cross-fingerprint comparison is licensed at the goal layer and not by this record. Correct and honest, but it means the directory cannot answer "is this comparison legitimate" on its own.
- **`indicators.json` carries no per-axis indicator field at the top level.** The classifications (`constraints_reachable`, `no_constraint_response`) reach the reader through `record.md` § 8, not as a directly readable field in the JSON under an `indicator` key. The traceability holds through the prose; a reader looking for a machine-readable per-axis verdict does not find one in the shape § 8's table implies.
- **This read is not blind, and no second read of this record can be.** `ADDENDUM-2026-08-29-artifacts.md` sits in the record directory and cites the first administrator's `synthesis.md` § 6 items 7, 9, 10, 11, 12 and 13 by number. Any later administrator obeying "read the record directory" is therefore told that a prior synthesis existed and which of its findings were accepted, before writing a word. The runbook says a second administrator's read is "a separate opinion, not a revision of someone else's" — an addendum living inside the read scope works against that. I record it as a process finding against the record contract, not as a defect of this record, whose addendum was written the way step 15 requires.
- **The snapshot's own corrected values are prose-only.** By the addendum's deliberate choice, `snapshot.json` still carries the superseded teax revision and identity kind. A tool reading the snapshot mechanically gets the stale values; only a human reading the addendum gets the true ones. The addendum states this and gives its reason; I note it because it is a real limit on the snapshot as a machine-readable artifact.

**Nothing else was missing.** Every number in §§ 3, 4, 6 and 11 that I attempted to recompute from `results/` reproduced exactly.
