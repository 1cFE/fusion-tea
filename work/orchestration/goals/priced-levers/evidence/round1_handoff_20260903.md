# Handoff — goal `priced-levers`: close round 1, then ground the wall-load / heating goal

Written 2026-09-03 by the round-1 agent of goal `priced-levers`, repo `/home/reid/1cfe/fusion-tea`, branch `feat/demo-maturation`. Nothing is merged or pushed — those are owner-held, as is work-item close.

Every claim below is marked **[verified]** (checked in this session, with the artifact that shows it) or **[carried]** (from a prior artifact or another agent's report, not re-checked here).

---

## Focus

Two jobs, in this order. **Do not skip the first — the second depends on its output.**

1. **Close round 1 of goal `priced-levers`.** The committed study is done; the round is not. What is still owed is listed under "Where round 1 actually stands" below. It includes two mandatory fresh-session gates that the round agent cannot satisfy for itself.
2. **Ground a new goal covering the neutron wall load and the heating-system structure**, owner-directed this session: *"we need to create a new goal for the wall-load and the heating structure."* Start at `work/orchestration/GOAL_RUNBOOK.md` § Grounding a goal.

---

## Context

- Goal directory: `work/orchestration/goals/priced-levers/` — `goal.md` (grounded 2026-09-02, with a dated Amendment), `trail.md`, `learnings.md` (**empty — no learning has been accepted yet**), `evidence/`.
- Procedure: `work/orchestration/GOAL_RUNBOOK.md`. Decisions behind it: `.project/adr/0001`–`0007`.
- The committed study: `exploration/stellarator_e2e/studies/20260903-priced-levers/` (`record.md`, `snapshot.json`, `axes.json`, `indicators.json`, `study.py`, `scan.py`, `results/`). Committed at `76876b82`.
- The predecessor goal, closed 2026-09-02: `work/orchestration/goals/operating-point-closure/`. Its round reviews are the standard for this one.
- The model item this round built: `work/active/WI-036_winding-pack-sizing/` (spec, design, plan). **Still `active` — closing it is owner-held.**
- Rubric and grades: `.project/active/demo-depth-rubric/` (`rubric.md@dc0f0b6d` is the frozen yardstick).

**Clean room is in force.** `knowledge/holdout/aries-cs/PROTOCOL.md` §§1–3. This session had one clean-room event — see Key Discoveries #7.

---

## Where round 1 actually stands

**[verified]** Tasks T-001 … T-007 are recorded in `trail.md` with returns, except T-007 (the study), whose return is **not yet written**. Round 1 is **open**.

Still owed, in order:

1. **Write the T-007 return** in `trail.md` — outcome, evidence refs, the goal-level reading, and the decision blocks. The study's own findings are in `record.md` § 15; do not restate them, cite them.
2. **The pre-execution disposition checkpoint (C-001).** `GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint. A **fresh non-author session** must review the study reading and its proposed dispositions **before any semantic follow-up executes**. This session cannot satisfy it — spawn a non-author session and deposit its spawn prompt as evidence (precedent: `evidence/T-007_precritique_prompt.md`, and the predecessor's `evidence/round2_C-001_checkpoint_prompt.md`).
3. **Discovery-log dispositions.** `20260903-priced-levers#1`…`#5` were appended by this session as **first-sighting rows** (executor's own act, study runbook step 14). The round owes joined **disposition** rows under the same ids before it closes — append only, never edit a sighting (ADR-0004). Also check whether the round's evidence touched `20260901-sustainment-fence#1` and `#4` (it did — they are WI-038/WI-039's lineage) and dispose them too. **No touched row may return unrouted.**
4. **Write the round 1 result** — `## Round 1 result — <date>` with intent, task sequence, last semantic outcome, derived stop reason, evidence refs, the proposed learning delta, and finding dispositions. Stop trigger is 1 (a valid study reading).
5. **The fresh round review.** Another non-author session reads the round end to end and returns `PASS` / `FINDINGS` / `OWNER_GATE`, then either recommends the owner-held close or writes the round-2 strategy. **An agent may not review a round it authored any part of.**

---

## Key Discoveries

**1. The deadlock at the printed 50 MW is the neutron wall load, not the magnets. [verified]**
`record.md` § 15 finding #1; `results/points.csv`. 27 of 240 points at 50 MW are blocked by `wall_load_ok` **alone** — at I 15.4 MA, T 17–18 keV, n 1.2×, the machine needs 26.3–36.3 MW of sustained heating against 50 installed (satisfied, with margin) and sits at B_peak 24.90 against the 24.9 T ceiling (satisfied), while wall load reads 5.76–6.46 against a 4.05 limit. Only **6** points are blocked by the conductor ceiling alone. `wall_load_ok` is violated **264 / 439** across the whole study — the dominant fence.
**Consequence for the new goal:** the machine can burn at the printed power; it cannot survive doing so. A conductor grade does not touch this.

**2. WI-038 (conductor-grade lever) addresses a fence that blocks six points. [verified]**
Direct consequence of #1. The previous goal minted WI-038 and WI-039 from the presumption that the conductor ceiling was the binding escape. That presumption is now measured and largely wrong. **Do not ground a goal on WI-038 without re-reading `record.md` § 4 and § 15 first.** WI-039 (heating structure) is untouched by this and still stands.

**3. The winding-pack sizing lever is real physics and almost no economics. [verified]**
`record.md` § 6 (`j_wp` observed response) and § 15 finding #2. A 2.33× swing in pack cross-section moves cold volume 270.45 → 115.91 m³ and cryoplant capital $20.98M → $16.00M, while **magnet capital is unchanged at $5,401.0M — delta exactly zero** — and LCOE moves 0.100%. Conductor cost is ampere-metre-proportional and blind to cross-section; ~85% of the pack (steel, insulation, copper, helium) has **no cost home in the model**. This finding is **`unrouted`** and is a live candidate for the new goal or a WI-036 follow-on.

**4. `cond_strain_ok`, added by WI-036, is inert. [verified]**
Violated **0 / 439**; max strain 0.235% against a 0.400% limit. It *is* reachable from both field levers (so not structurally dead like `tbr_ok`) and it *would* bind at a 0.2% limit — the value other projects enforce, and the model holds the limit settable. `record.md` § 15 finding #3.

**5. Holding an axis silently decides the answer. [verified — this is the session's most transferable lesson]**
The first study design held `T_i0` at 14.63 keV, inherited unexamined from the predecessor's grid arms, and pre-registered that the conductor ceiling would be the last fence standing. The pre-execution critique caught it; sweeping T overturned the conclusion. T is also worth **16.645 $/MWh** at the feasible optimum (`record.md` § 15 finding #5). **When you inherit a held value from a prior study, check whether it is load-bearing for your conclusion.**

**6. The fresh pre-execution critique earned its cost. [verified]**
It returned **MAJOR** with 3 major + 5 minor findings, all accepted, and it changed the study's conclusion — not just its presentation. Full text: `work/orchestration/goals/priced-levers/evidence/T-007_precritique.md`. Treat the critique gate as load-bearing, not ceremony.

**7. Clean-room event — a source was refused and its content had already reached the session. [verified]**
`scripts/source_registry.py` refused `arXiv:2409.01925` with `term:aries-cs matched 4x`. The refusal is durable in `knowledge/research/requests/runs/REQ-036-03/*/return.json` `queued[]`. **The research subagent had already fetched and reported that paper's contents before the guard ran** — the guard fires at registration, search happens before it. It is not registered, not cited, and none of its numbers are used anywhere. Recorded in `evidence/T-002_criterion_return.md` § 6. The owner has not ruled on the PROTOCOL §6 exception path; the executor's call was to leave it refused because nothing load-bearing depended on it. **This is a structural gap worth knowing: the hold-out guard cannot protect a session from what a subagent already read.**

**8. Research done this session, reusable. [verified]** Four sources registered under `knowledge/sources/`: Molodyk 2021 (REBCO J_E at 20 K, Jc ∝ B^−0.6), PPPL-5297 (the 666 vs 800 MPa allowables verbatim), Bottura & Bordini 2025 (REBCO $/kA·m), Barth 2015 (irreversible strain by manufacturer — SuperOx, the tape this design specifies, is the weakest of five at 0.45–0.47%), Titus IAEA 2018 (ITER stress categories: 666 MPa membrane, 1.0–1.333 GPa peak), Zhai FNSF (transverse tape limit ~200 MPa).

**9. Two named research gaps, both queued and durable. [verified]** Pierro et al. 2019 (IEEE, paywalled) is the only identified source measuring REBCO irreversible strain *through* 20 K — everything used is bracketed by 4.2 K and 77 K. And no open source publishes $/kA·m as a function of field. Both are in the seam run returns.

**10. Toolchain gotchas. [verified]**
- The pinned codegen **refuses an expression in a calc input binding** (`SI_EXPRESSION_SOURCE_UNSUPPORTED`). Put arithmetic inside a calc.
- The independent oracle `exploration/stellarator_e2e/verify_stellaris.py` must be updated to compute any new chain **itself** — that is what makes bit-exact parity evidence rather than tautology.
- The evidence store records only single-field float channels. Declaring a multi-field module output as a store channel produces a **silent empty column**, not an error (`record.md` § 15 finding #4).
- `tests/study` leaves `.integration_workspace` behind on failure and the next run refuses; `rm -rf .integration_workspace` before each run.
- Environment: `uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env …`, plus `PYTHONPATH=$HOME/1cfe/teax/packages/teax-simkit:$PWD/exploration/stellarator_e2e/pkg` when driving the package or oracle directly.

**11. Battery state at handoff. [verified]** `tests/models` 48 passed / 13 skipped; `tests/study` 353 passed / 1 skipped, zero failures. Integration seam returned `CANDIDATE`, pin `6262dbf42c709600dc03736d8c54058c9a08ec4369ccd0327a26474cd34be784`, all ten gates pass.

---

## For the new goal — what the evidence already supports

**[verified] The wall-load half has a measured, specific starting point.** `wall_load_limit` = 4.05 and the operand is computed, but wall **area** comes from the radial build and neither `R` nor `a` was swept here (`record.md` § 17). Machine size is the obvious untested lever, and this study says so explicitly rather than implying it.

**[verified] A known model defect sits directly in that path.** The radial build carries `coil_t = 0.30` (1costingFE geometry default) while the winding pack is `wp_side ≈ 0.36` m computed — two independent, inconsistent statements of coil radial extent with no relation between them. WI-036 deliberately excluded reconciling it because it moves vessel, blanket and shield volumes at once (`work/active/WI-036_winding-pack-sizing/spec.md` § Scope boundaries). **A wall-load/geometry goal will hit this immediately.**

**[carried] WI-039 (Heating System Structure) is unstarted and its target is unchanged.** `work/BACKLOG.md`, status `backlog`. Rubric Row 4's written target is **P2** and R4.P currently grades 1; R4.S already grades 2, at target. The P3 raise was deferred to the next rubric version `[OWNER 2026-09-02]`. **Do not write an answered-when against the unwritten P3 bar.**

**[verified] The heating half needs no research seam.** The pinned 1costingFE carries per-method installed-power rates and `eta_pin = eta_source × eta_couple` with `eta_source_ecrh = 0.50` (`defaults.py:96-108`) — enough for Row 4's P2 anchor.

**[verified] Heating is now load-bearing in a way the gap report does not reflect.** `gap-report.md@fc80e5b2` puts Row 4 in Band C, "no measured leverage, no constraint role of its own". Installed heating is the axis that decides feasibility in both fence studies. The gap report predates that and this session did not re-run it.

---

## Suggested Skills

- **`/run-goal`** — the entry point for both jobs. It picks the mode; for job 1 you are in `review`/`round` mode on `priced-levers`, for job 2 in `ground` mode on a new slug.
- **`/_my_ask_me`** — the owner takes goal-grounding rulings one at a time; this is the precedent path for the answered-when and gate proposals.
- **`/run-study`** — only once a new round has a pin and a study question. Not before.
- **`/backlog`** or `uv run agentic-mbse pm add-item` — if the new goal mints work items. Minting is a selection act; check whether the owner wants it owner-present.
- **Do not** invoke `/_my_quick_edit` for anything in `models/` — model changes go through the modelling PM with its validation levels.

---

## Open Questions

1. **[owner] Does `goal.md` § Answered when need an amendment?** Its conductor half — "a committed study exhibits the `B_max` lever with its cost and stress consequence chain active" — was framed around a fence that blocks 6 points. The heating half (R4.P = 2) is untouched and still right. A dated amendment, not an edit.
2. **[owner] Is round 1 closed on this study, or does it continue?** The runbook closes a round on a valid study reading (trigger 1), and this is one. The round-2 strategy would then be authored by the fresh reviewer.
3. **[owner] Where does `20260903-priced-levers#2` (the winding pack's missing cost home) route?** Currently `unrouted`. Candidates: a WI-036 follow-on, or absorb it into the new goal.
4. **[owner] The clean-room exception on `arXiv:2409.01925`** (Key Discovery #7) — grant under PROTOCOL §6, or leave refused. Nothing depends on it.
5. **[owner] Does WI-038 stay in the backlog as-is?** It is not wrong, but it is now known to address a minor fence. It may deserve a note recording that, so a future session does not pick it up on the old presumption.
6. **[open] Should the new goal be one goal or two?** Wall-load and heating structure are independent physics with independent work items. The owner's words were "a new goal for the wall-load and the heating structure" — singular "goal", two subjects. Worth one clarifying question at grounding: the predecessor goal `priced-levers` carried two halves and it worked, but the halves shared one question ("are these levers priced honestly") and these two may not.
