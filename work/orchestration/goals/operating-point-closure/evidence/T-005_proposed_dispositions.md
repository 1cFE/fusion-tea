# Proposed goal-level dispositions — round 2, after the `20260901-sustainment-fence` reading

Author: the round agent (2026-09-01). Status: PROPOSED — nothing below executes until a fresh checkpoint reviewer passes it (`GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint). The semantic follow-up task gated behind this checkpoint is T-006, the fresh Row-1 re-grade.

## Rows the round's evidence touched

1. **`20260823-magnet-technology-ab#4`** (no confinement closure; field never rewarded; optimum driven to the beta floor). Current log state: `model fix` — routed → WI-037 (this round's T-001 row). **Proposed: discharged by the landed increment, with the study as the closing evidence.** The mechanism the sighting names is structurally closed: B now reaches fusion power and the power balance through ISS04 (reachability: I_coil → 7 constraints and the fuel/replacement objectives, `indicators.json`), and the committed study shows the constrained optimum at beta 0.0311 vs the 0.05 limit — off the beta floor, bounded instead by `sustainment_ok` below and the conductor ceiling above (record § 3/§ 6). Proposed log row: `model fix — discharged by WI-037 at pin 35e922c5; closing evidence 20260901-sustainment-fence record § 3/§ 6; the residual trade (field vs conductor grade) is finding 20260901-sustainment-fence#1`. Appended at round close if the checkpoint passes.
2. **`20260901-sustainment-fence#1`** (no feasible operating point at 50 MW installed; sustainment/ceiling deadlock). **Proposed: carried as the round result's central negative finding; home = the goal's round result now, candidate follow-on named (conductor-grade arm or heating-system item) but NOT minted this round** — the round is at its one-pin/one-study bound, and the routing choice (magnet-technology axis vs Row-4 heating item) deserves the next strategy's argument, not a rushed mint.
3. **`20260901-sustainment-fence#2`** (CAS10 land term, third sighting). **Proposed: no new action — the standing WI-034 route holds;** the new sighting strengthens its priority case, recorded in the round result.
4. **`20260901-sustainment-fence#3`** (multi-field store limitation). **Proposed: closed as declared seam** — ANNEX § Oracle now names `sustain__*`; nothing further owed.
5. **`20260901-sustainment-fence#4`** (heating is pure cost; Row 4 unblocked). **Proposed: stays `unrouted` with the Row-4 pointer** — same reasoning as #1's follow-on: minting belongs to the next goal-selection act (the grade→goal loop), which the re-grade feeds.

## The follow-up task this gates

T-006: fresh non-author Row-1 re-grade against `rubric.md@dc0f0b6d` (the goal's § Answered when). The reading it rests on: the sustainment chain links field and heating to density and temperature (ISS04 executable at every point), and a power limit pushes back with a fully computed operand — demonstrated binding in a committed study (fence anatomy § 4; the optimum's bounds § 3).

## Revision r2 — 2026-09-01 (after checkpoint C-001.r1: REVISE)

The r1 verdict upheld all five readings and dispositions 1/3/4; dispositions 2 and 5 failed ADR-0004's disposition-class requirement as worded. Corrected forms, superseding the r1 wording for #1 and #4 only:

2′. **`20260901-sustainment-fence#1`** — class **`model fix`**, status **routed as a close proposal, not minted**; responsible actor: the owner at the goal-close ruling, with the next strategy author executing the mint. Concrete next reference: the choice between a conductor-grade (B_max) arm study and a rubric-Row-4 heating-system item — `model fix` because the finding names model structure both candidate routes repair (the machine's only escapes from the deadlock are an unmodeled conductor-grade lever consequence chain or a heating system with structure); the round is at its one-pin/one-study bound, so minting is the next selection act's. **A class-bearing log row in this form is appended at round close** (the rows-53/54 template).

5′. **`20260901-sustainment-fence#4`** — class **`model fix`**, status **not minted, pending the grade→goal selection act**; responsible actor: the owner/next strategy author at the re-grade-fed selection. Concrete next reference: rubric Row 4 (heating-system structure; its P3 deferral "rides on row 1" is unblocked by this goal). The Home column retains unrouted-with-pointer per the C-001.r2 precedent; the disposition itself bears the class. **A class-bearing log row in this form is appended at round close.**

Also adopted from r1's notes: the `#4`-discharge row will carry the not-final caution (WI-037 close and goal close stay owner-held), and disposition 4's wording is read as "nothing further owed *by this goal*" (the upstream store limitation stands under `20260821-power-cycle-ab#5`).
