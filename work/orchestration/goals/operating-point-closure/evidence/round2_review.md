# Round 2 review — full text (fresh non-author session, 2026-09-01)

Deposited verbatim by the round agent from the reviewer session's final return. Spawn prompt: `evidence/round2_review_prompt.md`. The trail's § Round 2 review entry summarizes and cites this file; this file is the review of record.

---

**Verdict: FINDINGS** — the round's substance stands in full and § Answered when is genuinely met pending the owner's two conjunct readings. The findings below are correctable records-hygiene defects; none reopens the round, changes a number, or weakens the re-grade. I recommend the owner-held close, with the packet at the end.

## 1. Grounds

I re-derived the crux evidence myself rather than trusting the trail: from `results/points.csv` I recounted 334 evaluated points, exactly 9 feasible, best feasible LCOE 293.46793 at (I_coil 15 MA, T_i0 14.63 keV, p_input 110 MW), beta 0.031091 against the 0.05 limit — off the beta floor; 0 feasible of 176 p=50 rows, with all 29 sustainment-satisfying p=50 points over the conductor ceiling; and all eight violation counts (219/155/119/101/96/69/0/0) match the record and synthesis to the digit. I re-ran the battery: `tests/models` 48 passed / 13 skipped; `tests/study` 270 passed / 84 skipped in my environment (the extra skips are env-gated tests the seam environment runs; zero failures anywhere). The fresh grader's R1.P = 3 at rubric sha `dc0f0b6d` (confirmed unmoved since 2026-08-30) rests on evidence I opened independently.

## 2. The checks

**Refs resolve and say what the trail claims.** Opened every cited artifact: `goal.md` (grounded, all five field classes filled), the amended WI-037 spec (§ Amendments records the forward-sustainment supersession, dated, never silent), `design.md` (D1–D8 as the T-002 return describes), `plan.md` (implementation record + the MR-WI037-7 restatement, present *before* the regeneration commit — plan restatement landed in `728d1263`/`ff807d3d` order as required), `T-004_integration_return.json` (CANDIDATE, pin `35e922c5…`, semantic `5b9abdfc…`, executable `41e06ecb…`, all ten named gates `pass`), the committed study at `1d28454f` + addendum/synthesis at `62a1fa7b`, `T-005_precritique.md` (MAJOR, seven findings, all dispositioned in record § 14 and visible in the executed design), `T-005_proposed_dispositions.md` (+ § Revision r2, appended not edited — `fbb6dad3` is +10/−0), the grader prompt, and `grading-r1-regrade.md` (same rubric sha, model `fbf70093`, package `41e06ecb…`, protocol-§7 delta valid). VALIDATION_MATRIX SV-041/042/043 read the amended sustainment contract and now `passing`.

**Goal and strategy fidelity.** The round pursued the reviewer-authored forward-sustainment strategy exactly: T-001 discharged the amend-before-implement constraints (spec MR-WI037-2/3, SV-042/043, the owed `magnet-ab#4` routing row — log row of `c17c4694`) before any design or model edit; the three strategy moves are the shipped D1–D5; one pin, one committed study; the study question is the strategy's intended question verbatim (record § 2). No abandonment condition fired: the grader *concurred* with the "links, not solves" anchor reading and routed the preamble tension to the owner rather than contesting the grade — which is the strategy's own prescribed path, not an abandonment.

**Task scopes (all six).** T-001, T-002, T-003, T-006 footprints match their scopes file-for-file (verified per commit). Two scopes deserve naming:

- **T-004's regeneration hop (49 files across `ff807d3d`/`5bea8964`).** Everything under `generated/` (including the handwritten impl's return-tuple reorder — that is the caller-order verification T-003 explicitly deferred to integrate, not a physics change; I read the diff), the oracle/runner extensions (`oracle_entry.py`, `verify_stellaris.py`, `run_stellaris*.py`), the manifest re-pin, snapshot, and the plan restatement are inside the authorized list. **Outside the list as written:** the `tests/study` fixture and constant re-derivations (6 expected.json files, ~6 test modules, `study_route.py`'s constraint count) — the ~30 sites L-006 names. This is drift to name, not to punish: it was disclosed in the return and commit messages, required by the seam's own battery gates, and re-derived from live evidence with the pre-WI-037 values left in history (I confirmed the anchors were re-derived only after oracle parity, per the recorded decision). The magnet-closure T-004 has the identical shape. Correction: integrate-task scopes should authorize the fixture/suite surface explicitly from now on.
- **T-005's study-layer edits outside the record directory** — `manifest.json` (the p_ecrh declared tie), `oracle_entry.py` (+1 key), `ANNEX.md` (§ Baseline pin correction, § Oracle naming `sustain__*` — verified present at `ANNEX.md:91`). All three are the invoked run-study runbook's own writes: tie declaration is the runbook's step-2 discipline, the oracle key-map growth is the documented seam pattern with two prior log rows (`power-cycle-ab#4`, `magnet-tech-ab#5`), and the ANNEX corrections discharge precritique findings 5 and 3 before execution. Authorized through "per the run-study skill (execute mode)"; not drift. Same correction as above: name the study-layer write surface in future study-task scopes.
- Minor: the SV-041..043 status flips at T-006 were the round agent's act on the grader's EI-5, through the native op, recorded as a decision — defensible under the delegation, but T-006's authorized list didn't carry it.

**Retry classification — the zero-retries claim holds.** The runbook's retry protocol attaches to a `MECHANICAL_FAILURE` *return*, and no task returned one. The T-004 reseal (impl edited after sealing → reseal by regeneration) and stale-workspace removal happened inside the task before its return and are recorded as decision fields — and the reseal followed a real content change (the caller-order alignment), so a "retry" framing would actually be wrong: inputs were not identical. The T-005 re-export re-ran no point; the export pass is not the task's meaning. Both classifications are correct against the runbook definition, and both are disclosed rather than buried.

**Checkpoint sequence.** C-001.r1 `REVISE` → C-001.r2 `PASS`, two separate trail entries, resubmission appended as § Revision r2 (no in-place edit — diff verified), cap respected, and the gated follow-up (T-006) executed only after PASS. The r1 pushback (ADR-0004 class-bearing requirement on dispositions 2 and 5) is real reviewer behavior, not rubber-stamping.

**Discovery rows — all five landed, and the movement claims are honest.** `20260823-magnet-technology-ab#4`: class-bearing `model fix` **discharged** row (log row 64) with the not-final caution carried — and the finding genuinely moved: mechanism structurally closed (I_coil reachability), study-demonstrated (optimum off the beta floor), re-grade-measured. `20260901-sustainment-fence#1` and `#4`: class-bearing `model fix` rows in the r2-ruled form (rows 65–66), honestly marked not-minted pending the owner/selection act. `#2`: sighting row carries the standing WI-034 route (third sighting; nothing moved, accounted). `#3`: `declared seam`, and the ANNEX § Oracle naming it promises is actually there. No touched row returns unrouted.

**External mutation.** `git log` over every cited path: rubric unmoved since `dc0f0b6d`, `grading.md` since `fc80e5b2`, the concept since `81a4fee8`; every model, matrix, log, and study path moved only in this round's own commits, each inside its task. Nothing moved outside its task.

**Findings (the corrections):**

1. **T-004 scope under-authorization** of the tests/study fixture surface (above) — name that surface in future integrate scopes; no rework owed.
2. **The C-001 checkpoint's spawn prompt was not deposited.** The owner directive says the fresh-session gates — disposition checkpoint included — are satisfied by spawned sessions "with spawn prompts deposited as evidence." The two review prompts and the grader prompt are deposited; the checkpoint's is not (nor, less critically, the administrator's or precritique session's — those are study-layer gates). C-001's freshness rests on the trail's assertion plus its observable pushback behavior. Deposit checkpoint prompts from now on; if this round's prompt survives, deposit it by dated addition.
3. **Design D7 prose slip:** "all three are non-reproducible" then names four studies. The plan's MR-WI037-7 restatement has it right (four). Correct by dated note whenever design.md is next touched; the authoritative restatement is unaffected.
4. **SV-041/042/043 bookkeeping:** the Requirement and evidence-location columns are empty where sibling rows (SV-038..040) carry them (`MR-WI037-1/2/3`; impl spot-check / oracle parity / committed study). Fill via the matrix's native path when next touched.
5. **Carried from the grader, filed at source, not new:** `verification_summary.json`'s `not_independently_verified` field is empty while six sustainment quantities are oracle-derived on both sides (EI-1); the teax revision is unrecorded in the study directory; EI-3's stale prototype-vintage comments ride the next regeneration-for-cause.

## 3. Learning delta rulings

- **L-004: ACCEPTED.** The grader's cell record independently reaches the "links … and pushes back" reading and satisfies both conjuncts on evidence I verified; the residual "links vs determine" tension is correctly routed to the owner as rubric wording, and L-004 as written does not pre-settle it.
- **L-005: ACCEPTED, one precision correction to append.** All numbers verified by my own recount. Correction: the "~91 MW" threshold is oracle-derived (p_aux_required 90.6 constant along the transect); the *committed* resolution is one grid step — `sustainment_ok` flips between p = 90 and 100 MW, and the committed feasible transect points sit at p ≥ 100. The synthesis says exactly this; L-005 should carry it so the threshold's precision is never overread.
- **L-006: ACCEPTED.** The ~30 re-derivation sites are visible in the T-004 diff (9 runner anchors, 6 known-answer fixtures, census, suite constants, manifest, ANNEX); "re-derived from live evidence, never patched to match" is supported by the recorded ordering (anchors after bit-exact parity) and the flipped R+tie assertion carrying its explanation in the test.

## 4. Constraints carried forward

1. Standing rulings, unchanged: one pin + one study per round; SV-016 recorded against, never fitted; no `p_pump` fraction form; `vol_cold_cryo` settable; Anchor A closed at its pin; clean room in full.
2. The four prior committed studies are not reproducible as written at pin `35e922c5…` (MR-WI037-7 restatement); their records stand at their own pins; any replay drops the retired keys and re-reads fixed-operating-point findings.
3. The disclosed, never-tuned baseline `sustainment_ok` violation (90.6 vs 50 MW, W-form-dominated) is the one explained verdict change — a finding, not a failure; do not "fix" it.
4. No sustainment-fact sensitivity exists yet; an f_ren ± arm would materially move the ~91 MW threshold (the grader's why_not_next names this for P4).
5. The Sudo density limit remains a surfaced gap (formula not admissibly printed); the route is research-seam ingestion of Sudo 1990, never a default.
6. Scope-writing hygiene: name the fixture/suite surface in integrate scopes and the study-layer writes (manifest ties, ANNEX, oracle map) in study scopes; deposit every gate session's spawn prompt.
7. WI-034 (CAS10 land term) now has three committed sightings; its priority case strengthens.

## 5. Recommendation — owner-held close

(Recommendation and close packet as returned; the trail's § Round 2 review entry and the round agent's close packet to the owner carry it.)
