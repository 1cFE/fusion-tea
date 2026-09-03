# Proposed goal-level dispositions — round 1, after the `20260903-priced-levers` reading

Author: the resuming round-1 session, 2026-09-03 (the session that executed the study wrote no T-007 return; this session wrote it — trail § T-007 return). Status: **PROPOSED** — nothing below executes until a fresh checkpoint reviewer passes it (`GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint). No semantic follow-up task is gated behind this checkpoint inside round 1: the round closes on this reading (trigger 1). What the checkpoint gates is the **disposition rows** these proposals become and the **round result** that cites them, and, downstream, the grounding of the owner-directed new goal that three of these rows route into.

The reading of record is the fresh administrator's `exploration/stellarator_e2e/studies/20260903-priced-levers/synthesis.md` (spawn prompt `evidence/T-007_administrator_prompt.md`) together with the committed record's § 15 **as corrected by the record's Addendum of 2026-09-03** (five prose statements the administrator's recount caught, each re-derived by this session before the addendum was written; no finding's id, class, count or reading changed). This document does not restate either; it cites.

## Rows the round's evidence touched

Seven rows: the five this study sighted, and the two predecessor rows whose lineage this round was grounded on (`goal.md` § Consumer names them; any round whose evidence touches them owes a disposition).

### 1. `20260903-priced-levers#1` — at the printed 50 MW the deadlock is sustainment against neutron wall load, not the conductor ceiling

- **Reading relied on:** record § 4 (`wall_load_ok` violated 264 / 439, the dominant fence), § 6 (`T_i0`, `n_e0`), § 15 #1 (27 of 240 p50 points blocked by `wall_load_ok` alone; 6 by `peak_field_ok` alone) with Addendum A.3's corrected span for the 27 (I 15.0–15.4 MA, T 17–19 keV, n 1.2–1.4×, wall load 5.76–9.23, required heating −47.8 to +49.3 MW — negative at 12 of 27), § 17 ("No claim that the conductor ceiling is irrelevant"; "No geometry claim — `R` and `a` were declined").
- **Class:** `model fix`.
- **Status:** routed → **the owner-directed new goal** ("we need to create a new goal for the wall-load and the heating structure", owner in session 2026-09-03, per the round-1 handoff). Drafted this session at `work/orchestration/goals/wall-and-heating/goal.md`, status `draft` — it authorizes no task until the owner grounds it. **Not minted as a work item this round:** the round is at its one-pin/one-study bound and minting is a selection act at grounding.
- **Responsible:** the owner at the new goal's grounding; the new goal's round-1 agent thereafter.
- **Concrete next reference, in the order the evidence supports:** (a) the fence's shape — the operand is a flat-wall **average** (`stellarator_plant.sysml:1064-1077`, "the model's flat-wall average vs the source's shaped-wall average") compared against a printed **peak** design value (`wall_load_limit = 4.05`, doc comment at `:1079-1081`: "peak neutron wall load 4.05 MW/m²"); (b) in this model wall load does not depend on `R` at all — `wall_area = kappa·4π²·R·vacuum_or` (`mfe_plasma_scaling.sysml:52`) and `p_fus ∝ V ∝ R·a²`, so `R` cancels, which the p-pump-fence record measured ("constant in R to 12 significant figures", `20260829-p-pump-fence/synthesis.md:69`); the geometry lever on wall load is `a` and the power-density levers are `n_e0`, `T_i0`; (c) the known radial-build defect in the same path — `coil_t = 0.30` held (`:510`) beside the computed `wp_side ≈ 0.36`, excluded from WI-036 by design (`work/active/WI-036_winding-pack-sizing/spec.md` § Scope boundaries).
- **What changed by this disposition:** the escape from the 50 MW deadlock is re-located from conductor grade to the wall. WI-038's premise is demoted by measurement (row 6 below). Nothing under `models/` changes.

### 2. `20260903-priced-levers#2` — the winding-pack sizing lever is physics without economics

- **Reading relied on:** record § 6 `j_wp` (magnet capital $5,401.0M at every transect point — delta exactly zero; cryoplant $20.98M → $16.00M; LCOE 0.100%), § 8 MD-2, § 15 #2; the cause disclosed before the study at `work/active/WI-036_winding-pack-sizing/design.md` D8.
- **Class:** `model fix`.
- **Status:** **not minted — routed as a proposal to the owner** (round-1 handoff open question 3). Two candidate homes, for the owner to choose between: a WI-036 follow-on item that gives the pack's non-conductor mass (steel, insulation, copper, helium — ~85% of the pack per D8) a cost account, on the shape precedent of the WI-035 casing-structure account; or absorption into the new goal if magnet-mass costing enters its scope. Until the owner chooses, the finding **stands at WI-036** as a disclosed state (D8), and WI-036's close is owner-held.
- **Responsible:** the owner at the next selection act.
- **Concrete next reference:** design D8; record § 6 `j_wp`; the WI-035 casing account as the template.
- **What changed:** nothing in the model; the missing cost home moves from a design disclosure to a measured consequence with a proposed route.

### 3. `20260903-priced-levers#3` — `cond_strain_ok` is inert at the 0.4% limit

- **Reading relied on:** record § 4 and § 15 #3 as corrected by the record Addendum A.1 (violated 0 / 439; the study-wide maximum strain is **0.286%** — the record's 0.235% was the transect's — against 0.400%; reachable from both field levers; the limit is settable), and the Addendum's sharpened 0.2% remark: at a 0.2% limit 323 of 439 points **and the pinned baseline itself (0.217%)** would violate; § 17 ("an `eps_cond_allow` arm at 0.2% would make finding #3's inert constraint bind. Neither was run.").
- **Class:** `research`.
- **Status:** **queued.** The value of the limit is a source question, and the one identified source measuring REBCO irreversible strain *through* 20 K (Pierro et al. 2019, IEEE TAS, paywalled) is durably queued for an operator fetch in the REQ-036-03 return (`knowledge/research/requests/runs/REQ-036-03/20260903T181625261847/return.json` `queued[]`). Until it lands, 0.4% stands on the registered Barth 2015 measurement (SuperOx 0.45–0.47% at 4.2 K) and the constraint stays live, reachable, and inert — disclosed at WI-036.
- **Responsible:** the operator (the fetch); the next fence study's executor (an `eps_cond_allow` sensitivity arm at 0.2%, which the record names as the study that would show whether the limit matters).
- **Concrete next reference:** the REQ-036-03 queue entry; record § 17.
- **What changed:** nothing in the model. The class is `research` rather than `model fix` because no model object is wrong: the check exists, computes, and reaches the levers; what is open is the number it compares against.

### 4. `20260903-priced-levers#4` — a declared store channel came back empty, silently (process)

- **Reading relied on:** record § 13, § 15 #4; the class already declared at `ANNEX.md` § Oracle and in `20260901-sustainment-fence#3` (disposed `declared seam`) and `20260821-power-cycle-ab#5` (disposed `declared seam` 2026-08-28, the upstream sysml-codegen / teax evidence-layer question).
- **Class:** `declared seam`.
- **Status:** **closed for this goal**, with one new fact filed. The multi-field limitation is the documented class and this goal owes nothing further on it. What is new in this sighting is the *failure mode*: the store accepted a multi-field declaration and produced a blank column with no gate, and the ANNEX's prose did not prevent the repeat. That is the recorded failure the hardening rule asks for (ADR-0003) before a mechanism is promoted. **Proposed, not minted:** a declaration-time guard in the study tooling (`scripts/study/`) that refuses a declared store channel which does not resolve to a single-field float channel — a coding-PM item under the run-study epic, minted owner-present.
- **Responsible:** not this goal; the run-study tooling owner. Executor-side, the study already corrected it (oracle-side export, re-executed; no blank left, no value invented).
- **Concrete next reference:** this sighting plus `20260901-sustainment-fence#3` as the two recorded repeats; `ANNEX.md` § Oracle.
- **What changed:** the cryo-cost column is exported oracle-side (`results/oracle_operands.csv`); the class gains a second sighting and a named hardening candidate.

### 5. `20260903-priced-levers#5` — the temperature axis is worth 16.645 $/MWh at the feasible optimum, and the optimum sits at the top of the swept window

- **Reading relied on:** record § 6 `T_i0`, § 12 (the licensed LCOE comparison at the 14.63 keV slice: 288.004 vs 271.359), § 15 #5, § 17 ("No statement about T_i0 … above 19 keV").
- **Class:** `model fix` — **the nearest of the four ADR-0004 classes, and the reviewer may re-class it.** The finding names no model defect: radiation losses are composed inside the sustainment calc (`mfe_plasma_sustainment.sysml:34-48`, bremsstrahlung + line + synchrotron), so nothing that should bound temperature is missing from the model. What it names is a **frame** defect in two studies' designs — the predecessor held T at 14.63 keV inside its feasible grid, and this study's window put the p110 optimum on its upper edge (18 keV) so the T optimum is not located.
- **Status:** **carried, not minted** — no model object changes. The finding routes two ways: into the round-1 learning delta (the transferable lesson: an inherited held value can decide a fence conclusion), and into the new goal's grounding evidence as a standing study-design constraint (T is a search axis in any fence study on this package, with a window wide enough that the optimum is interior or a fence catches it).
- **Responsible:** the round-1 review (learning acceptance); the next fence study's executor (the window).
- **Concrete next reference:** record § 6 `T_i0` and § 17; the new goal draft § Grounding evidence.
- **What changed:** nothing in the model; a study-design constraint is now recorded where the next study's author will read it.

### 6. `20260901-sustainment-fence#1` — the 50 MW deadlock (sighting: ISS04 relief vs the REBCO ceiling; minted → WI-038 2026-09-02)

- **Reading relied on:** this study's § 15 #1 and § 17 first bullet; `evidence/T-001_research_return.md` § 5 result 2 (24.9 → 30 T costs ×1.12 in tape and ×1.45 in Lorentz stress — cheap in conductor, expensive in structure); record § 8 (`B_max` reaches one constraint and zero objectives — a pure fence-relaxer as bound).
- **Class:** `model fix` (unchanged from the 2026-09-02 mint row).
- **Status:** **premise re-measured; WI-038 stays minted, unstarted, and is not the lead.** The sighting read the deadlock as sustainment against the conductor ceiling; with temperature swept, the ceiling alone blocks 6 of 240 p50 points and the wall alone 27 (`results/points.csv`). The ceiling still binds — 144 of 439 verdicts, and the p110 feasible band is bounded above by it — so WI-038 is not wrong; it addresses the fence that is not the wall at the printed power. This round did not de-mint or annotate WI-038: the backlog row is owner-held ground.
- **Responsible:** the owner — proposed ruling at the new goal's grounding (round-1 handoff open question 5): leave WI-038 as-is, or annotate its row so a future session does not pick it up on the pre-T-sweep presumption.
- **Concrete next reference:** `20260903-priced-levers#1` (row 1 above), which is where the deadlock's escape now routes.
- **What changed:** the finding moved — its mechanism is measured as two fences with the wall dominant, and its follow-on is re-routed from a conductor-grade item to a wall-load/heating goal.

### 7. `20260901-sustainment-fence#4` — installed heating is pure cost once sustainment is met (minted → WI-039 2026-09-02)

- **Reading relied on:** this study's § 15 #1 (the wall-limited p50 points need 26.3–36.3 MW of sustained heating against 50 installed) and § 6 `p_input+tie` (0 / 240 feasible at 50 MW, 87 / 192 at 110 MW — installed heating decides feasibility in both fence studies); `goal.md` § Answered when (a) and § Grounding evidence on the gap report's stale Band C reading.
- **Class:** `model fix` (unchanged from the mint row).
- **Status:** **WI-039 stays minted and unstarted; its target is unchanged; it becomes the heating half of the owner-directed new goal.** Row 4's written target stays P2 (`[OWNER 2026-09-02]`); the P3 raise rides the next rubric version. This round touched no heating model object.
- **Responsible:** the owner at the new goal's grounding — with one ruling surfaced there and not here: the heating half is also `priced-levers` § Answered when (a), so grounding it in the new goal redirects this goal's heating half (§ Close rule permits close by redirect at a round boundary) or leaves two goals owning one half. The new goal draft states the recommendation; the owner rules.
- **Concrete next reference:** `work/orchestration/goals/wall-and-heating/goal.md` (draft) § Answered when (a); `work/BACKLOG.md` WI-039.
- **What changed:** the finding's consumer moved from "a future goal" to a drafted one; nothing else.

## What this checkpoint gates

No task inside round 1 — the round closes on this reading. It gates: the seven disposition rows above being appended to `DISCOVERY_LOG.md` under their ids; the round-1 result citing them; and the learning delta the result proposes (the reviewer of *this* checkpoint rules on readings and dispositions only; the learning delta is the round review's to accept).

## What the author asks the reviewer to scrutinize hardest

- Row 1's reading of the fence's shape (average operand vs peak limit) is taken from the model's own doc comments at the cited lines, not measured by this study. Confirm the lines say what is claimed before it reaches the new goal's grounding.
- Row 5's class. If `model fix` is the wrong word for an information-only finding, name the right one; the author could not make any of the four fit cleanly and says so rather than hiding it.
- Rows 6 and 7 are dispositions on another goal's rows, written by this goal. Confirm that "premise re-measured, item stays minted" is a disposition that moves the finding under ADR-0004 and not a restatement.

## Revision r2 — 2026-09-03 (after checkpoint C-001.r1: REVISE)

The r1 verdict passed rows 2, 3 and 4 as written and upheld every count. Rows 1, 5, 6 and 7 each needed one bounded change. The r1 text above stands as the record of the disagreement; the forms below supersede the named wording only.

**1′. `20260903-priced-levers#1` — next reference (b) replaced; "What changed" qualified.** The r1 text said wall load does not depend on `R` in this model because `R` cancels between `p_fus` and `wall_area`, and inferred that the geometry lever on wall load is `a`. **That is false at pin `6262dbf4`, and it is withdrawn.** The wall-load calc alone does cancel `R` (`p_fus ∝ V ∝ R·a²` over `wall_area ∝ R·(a + vacuum_t)`), but since WI-037 the fuel peak densities are no longer held: they come from quasi-neutrality with the converged helium-ash balance, whose confinement time is ISS04, `τ_E ∝ a^2.28 · B^0.84 · R^0.64` (`models/library/analyses/mfe_plasma_sustainment.sysml:26-30`), with `B_axis ∝ I_coil / R` — so `R` reaches `p_fus` by two routes that do not cancel against `wall_area`. This study measures the field half of that coupling directly: at fixed T 14.63 keV, n 1.0×, `j_wp` 90, p 50, wall load falls **3.1748 → 2.6835 MW/m²** and `p_fus` 2786 → 2355 MW as `I_coil` goes 15 → 18 MA (`results/points.csv`), and `I_coil` reaches `wall_load_ok` in `indicators.json`. The p-pump-fence constancy in `R` (`synthesis.md:69`) was measured at a pre-WI-037 pin where `n_D0` and `n_T0` were held, and does not transfer. **The sign and size of `R`'s effect on wall load at this pin are unmeasured.** The corrected next reference (b): the geometry pair `R` and `a` both reach the wall fence through confinement as well as area, with the direction and size in `R` an open measurement for the new goal's first study. "What changed" is qualified: the escape is re-located from conductor grade to the wall **at the held geometry** (record § 17 makes no geometry claim).

**5′. `20260903-priced-levers#5` — class `declared seam`** (was `model fix`), on the exact precedent of `20260829-p-pump-fence#2` (`DISCOVERY_LOG.md:42`: an inherited window that no longer contained the fence, typed `model` by the record and dispositioned `declared seam` to the run-study skill's maintainer at runbook step 7). Row 5 is the same kind — a study-frame defect (held T; window-edge optimum) declared as a standing study-design constraint. Concrete next reference gains `.claude/skills/run-study/runbook.md` step 7 (fix the window from a scan that covers every searched axis, and widen until the optimum is interior or a fence catches it) alongside the new goal's invariant. Status, actor and the other references unchanged.

**6′. `20260901-sustainment-fence#1` — one phrase labelled.** "The p110 feasible band is bounded above by `peak_field_ok`" is an **inference**, not an observation: `peak_field_ok` is violated at 0 of 192 points in `arm-search-p110`. The inference is sound because `B_peak` is a function of `I_coil` alone (24.9 T at 15.4 MA, 25.87 T at 16 MA, one value per current across both arms, `results/points.csv`), and the administrator flagged it (`synthesis.md` § 3, § 6). The row carries the label. Also stated, per the reviewer's recommendation: "premise re-measured" is a measurement at this pin with T swept, not a feasibility-structure comparison across the WI-036 semantic boundary, which record § 12 does not license.

**7′. `20260901-sustainment-fence#4` — two items corrected.** (i) The "Reading relied on" quoted the pre-Addendum cell (26.3–36.3 MW against 50 installed). Addendum A.3 supersedes it: the 27 wall-alone points need **−47.8 to +49.3 MW of sustained heating, negative at 12 of 27** — twelve need no auxiliary heating at all, and the top of the span nearly exhausts the installed 50 MW. For a heating-structure finding that is the relevant span. (ii) "Installed heating decides feasibility in both fence studies" over-read a two-level sensitivity axis on which the record makes no boundary claim (§ 6). Corrected to what § 6 licenses: installed heating moves the sustainment fence — 0 of 240 feasible at 50 MW, 87 of 192 at 110 MW — and at 50 MW, 141 of 240 points satisfy sustainment and none is feasible, because the sustaining points are wall-blocked. Heating does not by itself decide feasibility.

**Downstream, same revision:** the draft `work/orchestration/goals/wall-and-heating/goal.md` carried the withdrawn `R` sentence as an Invariant and the over-read heating phrase in § Grounding evidence; both are corrected in the draft to match 1′ and 7′, and its § Answered when (b)(ii) lever list now names the geometry pair `R` and `a` rather than excluding `R`.
