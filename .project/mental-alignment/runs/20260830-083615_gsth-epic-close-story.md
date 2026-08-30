---
question: "Please see .project/backlog/epic_goal_strategy_task_harness.md — We have completed this epic, and are in the process of closing it. I want a very clear, understandable story for: What was done; How we expanded or enhanced our TEA process; How we demonstrated the capabilities — Specifics around the tests and outcomes. MUST be plainly explained so a general audience understands the model enhancements and experiments."
date: 2026-08-30 08:36
policy: discovered
shape: checkpoint
evidence:
  - .project/backlog/epic_goal_strategy_task_harness.md
  - .project/CURRENT_WORK.md (§ GSTH, § Recently Completed — Items 1, 2, 4, 5 close summaries)
  - .project/completed/20260830_goal-integration-study-proof/epic_evidence.md (read at rev d6b7b400, pre-archive path; amended at 8fc1cbb0)
  - .project/completed/20260830_goal-integration-study-proof/route_equivalence.md
  - .project/completed/20260830_goal-integration-study-proof/product-lens.md (close-F1 block and its 8fc1cbb0 resolution)
  - work/completed/20260828_WI-033_p-pump-rebase/verification_record.md
  - work/orchestration/goals/p-pump-fence/goal.md and learnings.md
  - exploration/stellarator_e2e/studies/20260829-p-pump-fence/synthesis.md
  - git log (close-F1 repair f3249f7c; resolution 8fc1cbb0; archive e4e895a1)
  - adversarial review by a fresh subagent (per feedback-synthesis.md), findings folded in 2026-08-30
code_inspected: "not inspected — the seams (scripts/source_registry.py, research_seam.py, integrate.py) and study code are named from records, not read; test counts and study numbers are quoted from committed records and regression transcripts, not re-run"
limits: "Item 3's audit and the Item 1/4 archives were read via their CURRENT_WORK close summaries, not in full; briefs/ (20 stage briefs) and the eight Item 5 transcripts skipped; the p-pump-basis goal directory skipped (its outcome is carried in WI-033's record and CURRENT_WORK)"
---

# GSTH epic close — the story

## 1. What was built: a paper trail that lets a stranger run the investigation

The TEA project already had good specialist tools before this epic: research a source, edit the SysML plant model, regenerate the cost package, sweep it in a study, read the results. What it did not have was anything connecting them. *Why* one step should follow another — which question is being pursued, what the last result decided, whether the current plan still holds — lived in the builder's head and chat history. If the builder walked away mid-run, the run died.

The epic built the **goal layer**: for each question the project pursues, one directory (`work/orchestration/goals/{goal}/`) holding three plain-text files — `goal.md` (the question, the evidence it rests on, and a written contract for what counts as an answer), `trail.md` (an append-only log of every task, decision, and result), and `learnings.md` (lessons accepted only after independent review) — plus a shared runbook (`work/orchestration/GOAL_RUNBOOK.md`) that a human and an AI agent follow identically. A goal cannot start until it is "grounded" — five field classes present and non-hollow: grounding evidence, answer contract, invariants, limits, reserved owner gates (`GOAL_RUNBOOK.md` § Grounding a goal) — and every round of work ends with a review by a fresh session that had no part in the work.

Two deliberate design choices, both owner rulings (`.project/concepts/goal-strategy-task-harness-design-review.md` § Resolutions): the files **cite** the specialist workflows' own records rather than copying them, and **no automation machinery** (event ledgers, retry logic, dispatchers) may be added unless a recorded run failure proves plain files failed. Across all three proof runs, roughly two dozen failures were recorded — every one caught by the route's existing defenses: a fresh session, a reviewer, an existing gate or test battery, or the operator reading files. Nothing earned promotion; the epic ships almost no control code. *(Visual: a layer diagram — specialist workflows below, three goal files + runbook above, arrows labeled "cite, never copy.")*

Provenance: the contract is Item 1, closed 2026-08-27 (`.project/completed/20260827_goal-harness-contract/`); the lean-first rule and its verdicts are ADR-003 with dated amendments.

## 2. Two process repairs: research and integration each became one honest command

Two steps in the TEA loop still ran on hand-copied patterns. The epic replaced both with "seams" — single producer-owned operations with an unambiguous return (Items 2 and 3, both closed 2026-08-27).

- **Research seam** (`scripts/source_registry.py` + `scripts/research_seam.py`): registering a source used to mean shell steps and hand-edited index files. Now one operation captures a URL or PDF and writes the citable file, content hashes, manifest row, and index entry together — or rolls back leaving nothing. It returns exactly one of REGISTERED / OPERATOR_QUEUE / BOUNDED_NEGATIVE (a durable "we searched and found nothing", so the search isn't silently repeated) / BLOCKER, computed from receipts on disk, not from what an agent claims. The ARIES-CS holdout quarantine is enforced in code with no waiver flag. Tested: 150 tests, including rollback, duplicate detection, and holdout refusal (`.project/completed/20260827_goal-research-seam/`).
- **Integration seam** (`scripts/integrate.py` entry): turning an audited model edit into a study-ready cost package used to be a hand-followed sequence scattered across work-item plans. Now one invocation runs regeneration and about ten gates (lineage, preflight, independent verification) and returns exactly one pinned, fingerprinted candidate package — or a named blocker. It fails closed on anything dirty or drifted (`.project/completed/20260827_goal-integration-seam/`, audit POSITIVE).

*(Visual: a two-row table — seam, old manual pattern, new single call, possible returns.)*

## 3. Experiment 1 — strangers can start, resume, and close a goal (Item 4)

The first proof asked: does the paper trail actually work for someone who didn't build it? Thirteen cold sessions across twelve fresh agents — none the builder — grounded a real goal (`work/orchestration/goals/cryo-volume-basis/`). The rehearsal question was itself real modeling substance: the magnet coils sit in a cryogenic cold mass the cryoplant must hold near 4 K, and the model already computes how much electrical current the coils carry — given the current density the superconductor sustains (DI-010), the winding-pack volume follows. Should the model *derive* that cold volume instead of holding a hand-entered number? (`goal.md` § Question, restating discovery row `20260823-magnet-technology-ab#2`.) Specific tests and outcomes (`.project/completed/20260827_goal-cold-pickup-proof/`, audit verdict Certify):

- **Grounding gate probed per field class**: a deliberately incomplete goal draft was refused for 2 of the 5 required field classes; the other 3 sailed through. The measurement was not hidden — the runbook was amended to a written five-class rule on that evidence (owner disposition 2026-08-27).
- **Kill-and-resume**: a task was killed mid-run after its write-ahead start; a different fresh session resumed from the files on disk alone, found the already-landed work, and did not repeat it.
- **Fresh review**: a session with no memory of the run reviewed the closed round. One honest miss: the deliberately seeded reviewer test (a planted scope drift) was neutralized before it reached the reviewer — the covering branch was declared before the run. The reviewer instead caught a *real* organic drift, so the faculty is demonstrated; the designed test is not.

Ordering claims throughout are git-ancestry checks, not timestamps. *(Visual: timeline of the 13 sessions with the kill/resume arc marked.)*

## 4. Experiment 2 — a real model error found, criticized, and fixed: p_pump 1.0 → 195 MW (Item 5 + WI-033)

The second proof ran on a genuine open error, and this is where the epic touched the TEA model itself. The model (`models/designs/stellarator_09/stellarator_plant.sysml`) describes a whole stellarator power plant: plasma physics feeding a power balance, the power balance feeding costed subsystems, the costs rolling up to LCOE. One of its inputs, **p_pump**, is the power for the compressors that push helium coolant through the breeding blanket to carry off ~3.2 GW of fusion heat. Helium is a gas — thin stuff — so moving enough of it to carry that heat takes serious compressor work: the EU-DEMO sources put it near 6 % of thermal power (~150 MW), where water does the same job for ~15 MW. The model carried **1.0 MW** — a water-like placeholder in a helium-cooled plant, roughly **two orders of magnitude low** — and both committed A/B studies had been built on it.

- The goal round (`p-pump-basis`, closed 2026-08-28) wrote a reading and proposed dispositions; a fresh non-author critic **refused** the first version (C-001.r1) with three required changes; the author revised and passed on r2. That is the owner's pre-execution checkpoint binding and releasing on a live round for the first time — the thing Item 5 exists to prove. Honest limit: the repository itself answered the basis question, so the research seam's request path never ran; 4 of 9 criteria were recorded as non-exercised or retired rather than dressed up (`.project/completed/20260828_goal-research-model-proof/`, audit POSITIVE).
- **WI-033** then landed the fix in the modeling PM: two EU-DEMO sources (Cismondi: "~150 MW" helium pumping; Moscato: loop-by-loop compressor data re-deriving to ~131 MW, near-term 83–94 MW) registered through the new research seam — zero hand-edited index entries — and **p_pump set to 195.0 MW** in both model twins, first-order re-derived in the verification record (`work/completed/20260828_WI-033_p-pump-rebase/verification_record.md`).
- Why 195 and why a held number: 195.0 is 6 % of the baseline computed thermal power (3238.1 MW → 194.3, rounded), set by **owner ruling** at the top of the sourced band, erring against the direction the model had been optimistic. It stays a *held, settable input* rather than a computed fraction of p_th — also an owner ruling — because a computed fraction would assert a linearity across swept geometries that no source establishes, and would retire a lever two committed studies sweep (doc comment at `stellarator_plant.sysml:502-523`).

*(Visual: visualize the physical system and the math — the helium coolant loop: plasma → blanket absorbing neutron heat → helium circulators → steam plant, annotated water ~15 MW vs helium ~150 MW; and a number line of the sourced band 83–195 MW with the old 1.0 MW marker far off scale and the landed 195 at the 6 %-of-p_th mark. The critic loop — refuse → revise → pass → execute — as a secondary strip.)*

## 5. Experiment 3 — the full loop, and what the fix does to the economics (Item 6)

The final proof drove the corrected model through the entire chain: integrate → study → fresh reading → criticized closure. Evidence map: `.project/active/goal-integration-study-proof/epic_evidence.md`.

**Integration**: five seam invocations before a candidate. The first two refusals were the seam working as designed — a not-yet-regenerated package (the exact stale-package detection WI-033 relied on) and tree hygiene. The next two surfaced the real finding: an audited input change reaches the package by regeneration, but five hand-maintained expectations of the package's output (manifest headline, independent oracle's held value, an anchor gate, a pinned test constant, an annex literal) were all stale. Four fell to mechanisms — integrate's preflight and verification gates, and the test battery twice — but **the fifth was found only by a person reading the annex for an unrelated reason**, recorded as learning L-001 and as the strongest case for a future expectation-coverage checker, which was deliberately not built. Run 5 returned exactly one verified candidate pin.

**The study** (`exploration/stellarator_e2e/studies/20260829-p-pump-fence/`, 906 of 948 grid points evaluated over major radius R 4–20 m and minor radius a 0.8–2.2 m). A fresh administrator reproduced every recomputable headline number exactly; the study's own verification harness reports worst deviation 6.3×10⁻¹⁶ over 48 sampled rows; and the administrator also found three prose numbers with no committed artifact behind them — repaired by addendum and accepted as learning L-004 ("a record can be arithmetically perfect and still fail its own contract"). What it found:

- **LCOE at the baseline design rose +21 %** (275.3 → 333.1 $/MWh), and the physics of why is the model's power-balance chain (`models/library/analyses/mfe_power_balance.sysml:119-147`): fusion heat plus half the pump work (the model recovers 50 % of it as coolant heat) makes thermal power p_th; p_th makes gross electricity at the turbine efficiency; then the plant pays its own bills — coils, pumps, cryogenics, heating — out of that gross, and only the remainder is sold. A 195 MW pump bill therefore hits **twice**: it inflates p_th, and nine capital cost accounts scale with p_th (more heat means physically bigger blankets, heat exchangers, turbine plant — p-pump-basis learning L-003); and it inflates the recirculating sum, shrinking net power. Cost up, saleable output down — both ends of the LCOE ratio move the wrong way.
- **The feasible region collapsed from 59 % to 41 %** of the swept grid. The window is machine geometry: R, the radius of the torus ring (4–20 m), and a, the thickness of the plasma tube (0.8–2.2 m) — sweeping them asks "how big a machine must this be?" Bigger plasma makes more fusion power, but the ~195 MW pump bill is a held input, nearly size-independent, so small machines spend an outsized share of their output running their own pumps. The recirculation fence (`rec_frac` ≤ 0.5 — no more than half the gross electricity consumed internally) accordingly swallowed the small-machine region: from a 32-point corner to a 184-point band that at a = 0.80 m spans the entire R range — the study says plainly it is unbounded there rather than faking a fence at the window edge. (The other active fence, wall load at a ≥ 1.70 m, is untouched by p_pump — thick plasmas push heat flux past the 4.05 MW/m² wall limit regardless.)
- **The best feasible LCOE, 225.7 $/MWh, sits on the window's edge** with the objective still falling, so the record refuses to call it an optimum.
- **A model defect surfaced**: 42 points with negative net power crash (the CAS10 land cost takes √p_net) before the net-power constraint can report "violated". Disclosed as a result, routed by owner ruling to backlog item **WI-034** — not patched in-round.

The critic refused the first checkpoint again (r1 → revise → r2 pass); the fresh round review returned FINDINGS with the answer upheld and corrected three learnings before accepting them; seven joined disposition rows closed every touched finding; the owner closed the goal. *(Visual: visualize the math — a power-flow (Sankey) diagram of the balance chain, fusion heat → p_th → gross electricity → split into recirculating (coils, pumps, cryo, heating) vs net-to-grid, drawn side by side at p_pump = 1.0 and 195 MW; and the R×a design-space map colored by verdict region — feasible, recirculation-fenced, wall-load-fenced, unevaluable — before and after the re-basing, baseline point marked.)*

## 6. Route equivalence, and where the close actually stands

The last claim — human and agent can operate the same contract — was tested by a fresh session playing a human operator, following the runbook literally in an isolated worktree (`route_equivalence.md`). Outcome: **byte-identical** candidate pin and fingerprints, identical return classes, every headline number reproduced, met on all five comparison dimensions — *and* the exercise found the two places the written pattern failed a stranger: the operator guide would have **mis-closed the round as a strategy blocker** over a checkout-path mismatch that was really an environment setting (F-1), and `uv run` cannot honor the sealed toolchain from a second checkout, forcing an undocumented interpreter workaround (F-2).

The project's own close review (product-lens, 2026-08-30) then did its job: it **blocked the close on close-F1**, because the evidence table said "met" while the falsifier — a documented-route operator hitting an undocumented correction — had actually occurred. The block was resolved the same morning, the right way: the guide and environment contract were repaired (`f3249f7c`: checkout carve-out on the toolchain-drift row; the sealed-interpreter exception documented), and a **fresh guide-only operator re-ran the isolated integration and reproduced the CANDIDATE** — same pin, all ten gates, verdict "guide alone sufficed, no undocumented correction at any step" (`8fc1cbb0`, session `0d76b3a4`). Lens gate CLEAR; Item 6 closed and archived to `.project/completed/20260830_goal-integration-study-proof/` (`e4e895a1`). All six GSTH items are now complete; the audit is POSITIVE (fresh session, battery reproduced 574 passed / 14 skipped). What remains is close-out bookkeeping — the epic file's Lessons Learned section is still TBD — and the shipping gate: `/_my_pre_pr`, then one PR carrying WI-033 + Item 6 on `feat/wi033-p-pump-rebase`. *(Visual: two panels — the five-dimension hand-vs-agent comparison table with the byte-identical pin highlighted, and a gate timeline of the close arc: falsifier occurs → lens BLOCKS → guide repaired → guide-only re-run passes → CLEAR → archived.)*

**The one-paragraph version for a general audience.** We built a written procedure that lets anyone — a new person or a fresh AI session — pick up a research question about our fusion cost model, run it through evidence-gathering, model changes, and design-space studies, and hand it off mid-stream, with every claim checked by someone who didn't make it. We proved it three times, on progressively more real work. Along the way it caught and fixed a real error of roughly two orders of magnitude (~130–195× against the sourced band) in the model's coolant pumping power, and the corrected model says the reference stellarator's electricity is about 21 % more expensive and its viable design space about a third smaller than we previously recorded — which is the system working: the process exists to make the numbers trustworthy, and it just made two committed studies' numbers honestly obsolete.

# Judgment

**Concerns**

- The research seam's request/return bookkeeper (`research_seam.py` open→log→close) has **never run end to end** — both live rounds found the answer without it. Only the registration write door has live evidence (WI-033). The records say this plainly (epic_evidence § 3), but any story claiming "the research seam is proven" overclaims.
- `assert_read_set_covered` at integrate gate 6 has no live evidence on any invocation that reached it, and nothing else covers it (filed, epic_evidence § 3).
- Route equivalence carries a declared limit that survives the close: `study.execute` was fixture-substituted, and the close-F1 re-run re-proved integration only. No one proved a hand operator would produce the same 906 points (steps 7–15 not walked); "same contract" holds for grounding/integrate/read/review, not the sweep itself.
- The record-contract class is real: the study record needed an addendum for uncommitted prose numbers (L-004), and that addendum sits inside the administrator's read scope, so no second administrator of this record can be blind (route-equivalence F-3). "Every claim checked by someone who didn't make it" holds once per record, not repeatably.
- The stale-expectation class (5 artifacts, 1 caught only by an unaided human read) bounds how much the gates can be trusted; the obvious checker was correctly deferred, but it is the sharpest open risk to the next model change.
- The epic's demonstrated TEA-model substance is one parameter correction plus its consequences. That is real and quantified, but most of the epic is process; the story should not imply broad model enhancement.

**Unresolved uncertainty**: the epic-level Lessons Learned section is still TBD in the epic file; the pre_pr gate has not run on the branch. Both are named remainders, not open questions about the evidence.

**Disagreements between sources**: none open. The one that existed — epic_evidence criterion 5 ("met") vs the product-lens ("BLOCKED") — has been closed `[OWNER 2026-08-30]`: the `8fc1cbb0` resolution amended the evidence to the failure-then-repair story and cleared the block. CURRENT_WORK (rev d6b7b400) predates the close commits; git log is the current truth.

**Suggested spot checks**: read the `8fc1cbb0` re-run verdict in the archived product-lens resolution block; re-run the regression stencil from epic_evidence § 1; open `results/points.csv` and recompute the +21 % baseline shift and the 370/906 feasible count.

# Appendix — the numbers in one place

| Quantity | Before (1.0 MW record) | After (195 MW) | Where |
|---|---|---|---|
| p_pump (helium pumping power) | 1.0 MW | 195.0 MW | `models/designs/stellarator_09/stellarator_plant.sysml`; WI-033 |
| Baseline LCOE | 275.264 $/MWh | 333.067 $/MWh (+21.0 %) | study § 2 / `results/baseline_result.json` |
| Feasible fraction of swept grid | 563/948 = 59.4 % | 370/906 = 40.84 % | study synthesis § 2 |
| recirc_ok violations | 32 points (corner, R ≤ 8 m at a = 0.8) | 184 points (band; unbounded in R at a = 0.80) | study § 6 |
| Best feasible LCOE | — | 225.725 $/MWh at (R 20.0, a 1.65), window edge, not an optimum | study § 2 |
| Excluded (negative net power, model crash) | — | 42 points, p_net −154.4 to −0.9 MW → WI-034 | `results/excluded_points.csv` |

Source basis for 195 MW: Cismondi (~150 MW helium vs ~15 MW water); Moscato loop data → 130.8 MW full-loop / 83–94 MW near-term band (~4–6 % of thermal power; better than one significant figure is false precision — learning L-001 of p-pump-basis). Both registered via the native seam, receipts `39bd3b41` / `891b95bc`. Neither source states 195 MW directly: the landed value is 6 % of the baseline thermal power (3238.1 MW), set by **owner ruling** at the top of the sourced ~130–195 MW band, deliberately erring against the direction the model had been optimistic (`work/orchestration/goals/p-pump-basis/trail.md` Ruling 3; doc comment `[OWNER 2026-08-28]` at `models/designs/stellarator_09/stellarator_plant.sysml:523`).

Test/verification tallies quoted from records: canonical battery 574 passed / 14 skipped; `tests/research` 150 passed; model-family spines 13/13; registry verify 0 faults / 3 known legacy; study verification 48 sampled rows, 10 channels at 1e-9, worst deviation 6.3463e-16, zero verdict mismatches.

# Renders

## 2026-08-30 09:07 — 20260830-083615_gsth-epic-close-story_resumed.html
path: .project/mental-alignment/runs/20260830-083615_gsth-epic-close-story_resumed.html
wall clock: 7m 10s (dispatch 09:00:31 → completion ~09:07:41; file on disk 09:07)
tokens: runtime states 205,760 cumulative for the agent at render completion; 144,563 was the cumulative before render dispatch
owner quality: asked at presentation; response pending

## 2026-08-30 09:22 — 20260830-083615_gsth-epic-close-story_fresh.html
path: .project/mental-alignment/runs/20260830-083615_gsth-epic-close-story_fresh.html
wall clock: 14m 46s (dispatch 09:07:44 → completion ~09:22:30; file on disk 09:22)
tokens: runtime states 236,800 for the agent
owner quality: asked at presentation; response pending
