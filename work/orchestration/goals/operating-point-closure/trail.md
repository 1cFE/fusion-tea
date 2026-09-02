# Trail: operating-point-closure

What happened, and what was decided. Append-only, newest entry last, ISO dates; no entry is ever edited in place — corrections are `### Amendment` entries. This file logs judgment, not routine stage motion; native workflows keep their own stage records and are cited, never restated. Procedure: `work/orchestration/GOAL_RUNBOOK.md`.

Goal grounded 2026-09-01 (`goal.md`, owner-present session). No round open.

## Round 1 — solve-the-operating-point

### Strategy revision — 2026-09-01

- **Approach:** close the operating point in three linked moves, physics from the admissible Stellaris source, executable through the established Rung-B handwritten codegen seam: (1) an ISS04 confinement-time calc (`stellaris-design-details.md` Eq. A.7 with the `f_ren` multiplier, image `page_031_eq_5.png`) from machine quantities — a, R, ι, the WI-035-derived B, density — and heating power; (2) a steady-state power-balance closure that solves peak temperature from field, density, and external heating (alpha heating from the existing Bosch-Hale machinery plus P_aux, balanced against W/τ_E), retiring held temperature as an entry point so fusion power, beta, and wall load respond to the machine; (3) pushback on computed operands: `beta_ok`'s operand becomes fully machine-responsive through the solved temperature, and a density or confinement-quality limit is added if and only if an admissible printed basis exists — no fallbacks.
- **Assumptions:** Eq. A.7/A.8 and the parameters they need (ι, f_ren) survive image verification in the admissible source; an iterative/fixed-point solve is implementable and oracle-guardable in the handwritten codegen stage (WI-022 `dt_fusion_power` precedent — numerical integration already lives there); P3 is reachable with temperature solved and density kept as a design lever (the Row-1 anchor asks the relation to *link* field and heating to density and temperature, not to solve every quantity); ι and f_ren are held sourced machine/quality facts, the k_link pattern.
- **Abandonment conditions:** the solve cannot be made convergent and verifiable across the study domain; a load-bearing quantitative basis fails image verification with no admissible substitute (surfaced with honest options, never defaulted); or the Row-1 anchor reading proves contestable such that only a rubric revision (owner-gated, concept OQ6) could settle it — that goes to the owner through the close rule, not around them.
- **Intended model increment:** library calc defs for ISS04 τ_E and the power-balance temperature solve; the plasma spine rewired so fusion power, beta, and wall load consume the solved temperature; the beta/density/power pushback asserted on computed operands; instance rebinds in `stellarator_09`; entry-point retirement with the committed-study restatement duty (goal invariants).
- **Intended study question:** with the operating point solved from the machine, is field rewarded — does the constrained optimum leave the beta floor (the `20260823-magnet-technology-ab#4` pathology) — and where do the confinement-linked limits bind over (B, density, P_aux) and (R, a)?

### T-001 scope

- **Objective:** register the modeling work item and produce its spec for the operating-point-closure model increment.
- **Why now:** the goal is grounded (`goal.md`, 2026-09-01 — uncommitted this session, operator holds commits; unpinned until the grounding commit lands); a standard-scale modeling change enters the native modeling PM at the spec stage, and the spec is where the increment's outcome-level shape gets fixed.
- **Scope:** authorized — `pm add-item` under the modeling PM, `work/active/WI-XXX_*/spec.md`, VALIDATION_MATRIX entries through `pm add-validation`; excluded — design/plan/implement stages, any `models/` edit, any source ingestion, discovery-log writes.
- **Inputs:** `goal.md` (no narrower constraint).
- **Done when:** the spec exists, requirements-complete at outcome level, and is presented to the owner in-session; under the 2026-09-01 delegation the round agent may approve progression if the owner does not rule.
- **Stop when:** a discovered prerequisite, a strategy blocker, an owner gate, or a declared limit.

### T-001 start — 2026-09-01

Task T-001 under § T-001 scope: mint the operating-point-closure modeling work item through the modeling PM (`pm add-item`) and write its spec at `work/active/WI-XXX_operating-point-closure/spec.md`. Expected artifacts: one new `work/BACKLOG.md` row, one `spec.md`, SV rows via `pm add-validation`.

### T-001 return — 2026-09-01

- **Outcome:** `COMPLETE`. Both halves of § T-001 scope's done-when hold on disk — the work item exists and its spec is written — and the spec is presented to the owner in-session with the two delegation-ruled decisions surfaced for override.
- **Evidence:**
  - `work/BACKLOG.md` — `WI-037` "Operating-Point Closure: ISS04 Confinement Solve, Machine-Responsive Temperature", `scale: standard`, `priority: P0`, under the MFE Cost Modeling — Tokamak & Stellarator epic; minted by `pm add-item`.
  - `work/active/WI-037_operating-point-closure/spec.md` — seven outcome-level requirements (MR-WI037-1..7): τ_E computed from machine and heating via ISS04 with sourced held f_ren/ι; temperature solved from the steady-state power balance, convergent-or-loud, held temperatures retired; a beta/density/power limit pushing back on a fully machine-responsive operand with the field-reward channel structurally present; library/instance split; image-verified citations, no fallbacks; standing rulings preserved at their real width (no confinement gate — the concept's 2026-09-01 correction cited as authority); entry-point/committed-study restatement before any regeneration. § Open decisions records the two agent rulings under the 2026-09-01 delegation.
  - `modeling_project/VALIDATION_MATRIX.md` — SV-041/042/043 added `pending` via `pm add-validation`, one per functional requirement. The parser's 'Invalid Type' warnings (escaped text in pre-existing rows) predate this task and were not touched.
- **Reading:** the increment has a native, auditable contract and nothing under `models/` moved. The comparison-meaning stake (retiring held temperatures changes what every committed study that held them means) is carried as MR-WI037-7, the WI-035 restatement shape. Discovery row `20260823-magnet-technology-ab#4` is touched as evidence but no disposition row is appended yet: its honest routing ("routed → WI-037") becomes real when the increment lands, and the round owes the disposition before it closes.
- **Decision:** trigger — the spec's two outcome-shaping calls (lever direction; ash treatment) have no owner gate to stop at. Decision and reason — rule them as the round agent under the owner's 2026-09-01 delegation ("no gates. you must use your best engineering and modeling judgement"): (1) solve temperature, keep density as the design lever — temperature is what confinement physics determines at a given machine and density, and the anchor's density-limit pushback presumes density is choosable; held T_i0/T_e0 retire with the restatement duty; (2) ash stays a held, disclosed referent — the source's own ash treatment is a heuristic suppression factor, and coupling it needs a further held-fact chain this increment does not carry. Both surfaced to the owner in-session for override. Tier — execution detail (under recorded delegation). Who decided — the round agent, 2026-09-01. What changed — `work/active/WI-037_operating-point-closure/spec.md` § Open decisions.
- **Decision:** trigger — nothing is committed. Decision and reason — the operator holds commits (round-1 precedent at goals `cryo-volume-basis`/`magnet-closure`); the working tree carries the goal directory, the WI-037 spec, and the two op-written registry files. Tier — execution detail. Who decided — the round agent, 2026-09-01. What changed — `none`.

**Next task:** not chosen — picked after the owner has seen the spec (design is the native next stage; under the delegation the round agent may proceed if the owner does not rule otherwise).

### Owner directive — 2026-09-01

The owner, in session: full execution of the goal is delegated to the round agent ("take ownership and accountability, and execute the entire goal") `[OWNER-VERBATIM 2026-09-01]`. Merge, push, work-item close, and the goal-close ruling remain owner-held (`GOAL_RUNBOOK.md` § What this is, and what it is not). Fresh-session gates (disposition checkpoint, round review, the answered-when re-grade) are satisfied by spawned non-author sessions with spawn prompts deposited as evidence — the magnet-closure round-2 grader precedent (`work/orchestration/goals/magnet-closure/evidence/round2_T-001_grader_prompt.md`). Commits on the working branch are working practice; the operator rules the merge.

### T-002 scope

- **Objective:** produce the WI-037 design — mechanisms for the three moves (ISS04 τ_E calc, steady-state temperature solve, machine-responsive pushback), every quantitative basis image-verified, under the spec's § Open decisions rulings.
- **Why now:** the spec is complete and presented; design is the native next stage and the place the balance form, solve architecture, lever set, tolerances, and the density-limit admissibility question get fixed.
- **Scope:** authorized — `work/active/WI-037_operating-point-closure/design.md`, source/image verification reads, throwaway prototypes outside `models/`; excluded — plan/implement stages, any edit under `models/` or `exploration/`, source ingestion, discovery-log writes.
- **Inputs:** `work/active/WI-037_operating-point-closure/spec.md`, `goal.md` (no narrower constraint).
- **Done when:** design.md exists, requirements-complete against MR-WI037-1..7, values image-verified, solve architecture prototyped enough to state convergence behavior honestly.
- **Stop when:** a discovered prerequisite (e.g. a value failing image verification with no admissible substitute), a strategy blocker, or a declared limit.

### T-002 start — 2026-09-01

Task T-002: write the WI-037 design through the native design stage. Native target: `work/active/WI-037_operating-point-closure/design.md`. Expected artifacts: one design document plus prototype scratch outside the repo trees.

### T-002 return — 2026-09-01

- **Outcome:** `STRATEGY_BLOCKER`. The design was not written: prototyping the solve before fixing mechanisms (the § T-002 scope's stated purpose) fired the strategy's declared abandonment condition — "the solve cannot be made convergent and verifiable across the study domain." No edit under `models/` occurred; WI-037's spec stands as written pending the next round's strategy.
- **Evidence:** `work/orchestration/goals/operating-point-closure/evidence/T-002_prototype/` — `NOTES.md` (findings, with every basis image-verified against the iter-02 raw PDF or page images and cited), scripts, and raw outputs. Uncommitted at write time; committed with this round's close.
- **Reading.** Two-sided result. (a) The forward physics chain validates against the printed Stellaris point A with nothing fitted: ISS04 τ_E −0.1% (with n19 read as line-averaged, its "usual meaning"), composed radiation −0.1% (brems + W-line + Albajar sync vs printed photon power), A.5/A.6 ash chain +3.6%, quasi-neutral p_fus +0.7%; the one outlier is the stored-energy form (+9.2%), amplified ×2.56 by the closure into the dominant balance residual. (b) The solve-T architecture is unworkable here: the printed point is ~90 MW short of self-sustaining and sits on the unstable branch; at the baseline machine no stable feasible burn exists inside the conductor-ceiling/stress/wall/beta limits; and the burn attractor amplifies power residuals ~×3 into temperature. A solved-T baseline is unevaluable at the current machine, and study sweeps would carry large no-burn voids — the p-pump-fence evaluability lesson at scale.
- **Decision:** trigger — prototype findings 3 and 4 (`NOTES.md`) fire the declared abandonment condition. Decision and reason — return `STRATEGY_BLOCKER` and close the round rather than silently re-architecting mid-round: the strategy's intended model increment ("power-balance temperature solve") is refuted by evidence, and the runbook closes a round when the strategy's premise is wrong; the successor architecture (forward sustainment fence) is recorded in `NOTES.md` § Consequence as input to the next strategy, which the fresh reviewer authors, not this session. Tier — premise surprise. Who decided — the round agent, 2026-09-01. What changed — the evidence directory; this trail.
- **Decision:** trigger — the prototype needed ι_{2/3}, absent from every table. Decision and reason — read it from Fig. 11(a) at s = 2/3 on the design-β curve (0.92 ± 0.01), bracketed by the printed axis/edge values 0.86/0.98 — an image-verification act (the WI-022 Fig-16 digitization precedent), not a default; the 0.41 exponent makes the read tolerance ±0.45% in τ_E. Tier — execution detail. Who decided — the round agent, 2026-09-01. What changed — `NOTES.md` § Verified bases.

## Round 1 result — 2026-09-01

- **Intent:** unmet — the round set out to land a solved-T operating-point closure and close Row 1; it lands a bounded negative on the architecture plus a validated forward physics chain. Unmet is a legitimate result.
- **Task sequence:** T-001 (mint WI-037 + spec) `COMPLETE` · T-002 (design, prototype-first) `STRATEGY_BLOCKER`.
- **Last semantic outcome:** `STRATEGY_BLOCKER` (T-002).
- **Stop reason:** last outcome `STRATEGY_BLOCKER` + no limit reached → round closes on trigger 2 (strategy blocker: the premise "P3 is reachable with temperature solved" is refuted at this machine by the round's own evidence).
- **Evidence refs:** `work/active/WI-037_operating-point-closure/spec.md` (T-001); `work/BACKLOG.md` WI-037 row; `modeling_project/VALIDATION_MATRIX.md` SV-041..043 (pending); `work/orchestration/goals/operating-point-closure/evidence/T-002_prototype/` (NOTES.md, scripts, outputs); all committed with this close (this branch, operator holds merge/push).
- **Learning delta (proposed):**
  - L-001: The Stellaris appendix closure (A.3 balance, A.7/A.8 ISS04 with P = W/τ_E, A.5/A.6 ash) is fully admissible and reproduces the printed point-A τ_E, photon power, ash density, and fusion power to ≤4% each with nothing fitted, provided ISS04's n19 is read as line-averaged (vol-av misses τ_E by −23%); the model's analytic W-form (+9.2%) is the dominant fidelity gap and enters conducted loss as W^2.56.
  - L-002: A solved-T operating point is the wrong architecture for this model state: no stable feasible burn exists at the baseline machine inside its own limits, the printed point sits on the unstable branch ~90 MW short of self-sustaining, and near-marginal attractors amplify power error ~×3 into temperature. Forward sustainment (required-aux vs installed, a power limit per the Row-1 anchor) is exact everywhere, keeps studies restatable, and leaves the baseline evaluable.
  - L-003: With confinement in the chain, field is rewarded (loss ∝ B^−2.15 effective) and the reward immediately collides with the conductor ceiling and the WI-035 stress fence — the `magnet-ab#4` pathology becomes a real three-way trade instead of a free descent to the beta floor.
- **Finding dispositions:** discovery row `20260823-magnet-technology-ab#4` was touched as evidence (T-001, T-002). No disposition row is appended: the round landed no model change, so the finding has not moved; its routing target (WI-037) exists but is `backlog`-stage work. The row stays open; the next round owes the disposition when the increment lands. No other open row was touched.

### Round 1 review — 2026-09-01

- **Reviewer:** fresh non-author session, spawned from the deposited prompt (`evidence/round1_review_prompt.md`); no context inherited; clean room honored. Full review text deposited at `evidence/round1_review.md` — the review of record; this entry summarizes.
- **Verdict:** `FINDINGS` — the round's substance stands; three correctable defects.
- **Checks (all performed, per the deposited text):** every cited ref opened and confirmed; strategy fidelity confirmed (prototype-before-design is what surfaced the blocker); task scopes held (commit `2df2c548` touched only the authorized paths, nothing under `models/`); no retries; the `STRATEGY_BLOCKER` classification independently reproduced (scripts re-run; required-aux curve recomputed — minimum ≈72.6 MW at point-A density, dg/dT > 0 at the printed point confirmed); the cross-check table verified to the digit against deposited and re-run outputs; sources re-verified against page images and the iter-02 raw PDF (including the discovery that the iter-02 `output.md` Table 3 extraction is itself garbled — raw PDF governs); no cited artifact moved outside its task.
- **Findings:** (a) discovery row `20260823-magnet-technology-ab#4` was touched and left `unrouted` — ADR-0004 owed a routing disposition at close (disposition ≠ resolution); round 2 appends it as an early act. (b) NOTES.md finding 1's "≈140 MW" is wrong — the evidenced figure is ≈90 MW (the trail and L-002 already carry the correct number). (c) `op_landscape_output.txt` was a crash traceback (script run from the wrong directory), not results.
- **Learning delta:** L-001 accepted; L-002 accepted with one correction (the ash chain is itself a damped fixed point — "exact everywhere" applies to the sustainment balance, not every sub-quantity); L-003 accepted. Appended to `learnings.md` with this entry.
- **Constraints carried forward:** eight, listed in `evidence/round1_review.md` § 4 — chiefly: amend MR-WI037-2/-3 and SV-042/043 before any implementation (the solved-T phrasing is refuted; dated amendment, never silent); append the #4 disposition; repair the two evidence defects; record the MR-WI037-7 restatement before regeneration; the expected `sustainment_ok` violation at baseline (≈90 vs 50 MW) is the one explained verdict change, recorded, never fitted.
- **Next:** the reviewer authored the Round 2 strategy revision (ADR-0002); it opens Round 2 below, transcribed verbatim with attribution.

### Amendment 2026-09-01 — amends evidence/T-002_prototype/NOTES.md finding 1 and the landscape output (review findings b, c)

Recorded here because evidence files, once cited by a closed round, are corrected by amendment note rather than edited in place. (1) NOTES.md finding 1's "≈140 MW sustained coupled heating" overstates: the deposited g = −89.6 MW at p_aux = 0 means ≈90 MW sustained coupled heating is required at the printed point; ≈140 MW is the transient access requirement near T = 12 keV. (2) `op_landscape_output.txt` as committed at `2df2c548` is a `FileNotFoundError` traceback (wrong working directory at capture); a valid in-place re-run is deposited alongside as `op_landscape_output_rerun.txt` — the reviewer independently confirmed the re-run supports the round's claims (fd=1.0 minimum aux 56.3 MW with held ash; higher densities burn only into wall/beta violations). The dead capture is retained unedited.

## Round 2 — forward-sustainment

### Strategy revision — 2026-09-01

Authored by the round-1 fresh reviewer per ADR-0002 (`evidence/round1_review.md` § 5); transcribed verbatim by the round agent. This trail copy is operative.

- **Approach:** forward sustainment, adopting NOTES.md § Consequence with amendments. Temperature and density stay design levers; the machine pushes back through power. Three moves: (1) ISS04 τ_E as a library calc from machine quantities and stored energy — the source's own closed form τ_E = (C·W^−0.61)^(1/0.39) with C = 0.134·f_ren·a^2.28·B^0.84·ι_{2/3}^0.41·n19^0.54·R^0.64, n19 line-averaged from the model's profile family, ι_{2/3} = 0.92 ± 0.01 and f_ren = 1.0 held image-verified facts; (2) required sustained heating p_aux_required = p_rad + W/τ_E − f_α·p_α computed from the validated chain (composed radiation: brems + W-line + Albajar sync per pinned 1costingFE forms; alpha heating from the existing Bosch-Hale machinery) and asserted against installed coupled heating as an executable power limit — the Row-1 anchor's third pushback class, with a fully machine-responsive operand (responds to B as ≈B^−2.15 through the closed form, and to n, T, a, R, ι); (3) ash and fuel computed forward from A.5/A.6 plus quasi-neutrality — n_He from the damped fixed point (converge-or-fail-loudly, oracle-guarded, the WI-022 seam pattern), n_D = n_T from quasi-neutrality with Z_eff and n_W/n_e held — retiring n_D0/n_T0/n_He0 as entry points while n_e0 and T_i0 remain levers (T_e0 through the held 0.95 ratio). Before any model edit, the WI-037 spec and SV-042/043 are amended to this architecture (carried constraint 1) and the `#4` disposition row lands (constraint 2). Weighed against the Row-1 P3 anchor's exact text: "a confinement/transport relation links field and heating to density and temperature" — ISS04 inside the sustainment balance is precisely a relation linking field and heating to the (n, T) choice; "and a beta, density, or power limit pushes back on the choice" — the power limit pushes back directly, and `beta_ok` continues to. The anchor says *links*, not *solves*; round 1 proved that at this machine "solves" is not evaluable, so the linking-plus-pushback form is not a retreat but the only architecture under which the anchor's conjunction can be evidenced in execution.
- **Assumptions:** the composed radiation chain and ISS04 closed form transplant from prototype to the handwritten codegen seam without new physics inputs (all bases already image-verified in T-002); the ash fixed point is a benign contraction across the study domain, guarded by fail-loud; the anchor reading above — a grader may instead read Row 1's summary line ("field and heating *determine* density and temperature") as requiring a solved point; density-limit pushback (Sudo) remains conditional on an admissible printed formula surviving image verification, and is omitted with the gap surfaced otherwise — never defaulted.
- **Abandonment conditions:** the sustainment computation cannot be realized convergent-and-verifiable in the codegen seam (including a non-contracting ash fixed point over the study domain); a load-bearing basis fails image verification with no admissible substitute; a fresh grader contests the "links, not solves" anchor reading — that goes to the owner through the rubric-revision path (concept OQ6) and the close rule, not around them; or the committed-study restatement cannot be honestly written (comparison meaning would move — trigger 3).
- **Intended model increment:** amended WI-037 (spec + SV rows first): library calc defs for line-averaged density, ISS04 τ_E (closed form), composed radiation, and required sustained heating; forward ash/quasi-neutral fuel chain retiring n_D0/n_T0/n_He0; a `sustainment_ok` (power-limit) constraint with computed operand asserted in the viability set; instance rebinds in `stellarator_09` (including the coupled-power citation fix at `:553`); entry-point retirement with the MR-WI037-7 restatement recorded before regeneration. Expected and disclosed: the baseline reads `sustainment_ok` violated (≈90 vs 50 MW), explained by the W-form fidelity gap — recorded, not fitted.
- **Intended study question:** with the sustainment fence active, is field rewarded — does the constrained optimum leave the beta floor (the `20260823-magnet-technology-ab#4` pathology) — and where do the power, beta, wall-load, conductor-ceiling, and stress fences bind over (I_coil/B, n_e0, T_i0) and geometry, i.e., is the three-way trade of L-003 visible in a committed study?

No future task list. One pin, one committed study, close on the first valid reading.

### T-001 scope

- **Objective:** discharge the review's pre-implementation constraints — amend the WI-037 spec (MR-WI037-2/-3, § Open decisions 2) and SV-042/043 to the forward-sustainment architecture, and append the owed `20260823-magnet-technology-ab#4` disposition row.
- **Why now:** carried constraints 1 and 2 of the round-1 review bar any implementation until these land; they are the round's entry ticket.
- **Scope:** authorized — `work/active/WI-037_operating-point-closure/spec.md` (dated amendment), `modeling_project/VALIDATION_MATRIX.md` SV-042/043 description amendments (dated, format-preserving, parser-verified — no add/remove of rows), one appended disposition row in `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` under the existing id; excluded — any edit under `models/`, design/plan/implement stages, source ingestion.
- **Inputs:** `evidence/round1_review.md` § 4 constraints 1–2; `goal.md` (no narrower constraint).
- **Done when:** spec amendment recorded; SV-042/043 read the sustainment contract with the amendment dated; the disposition row appended; `agentic-mbse status` parses clean (no new warnings).
- **Stop when:** a discovered prerequisite, a strategy blocker, or a declared limit.

### T-001 start — 2026-09-01

Task T-001 (round 2): spec/SV amendment + disposition row. Native targets: WI-037 spec, VALIDATION_MATRIX, DISCOVERY_LOG. Expected artifacts: amended spec § Amendments, two amended SV descriptions, one appended log row.

### T-001 return — 2026-09-01 (round 2)

- **Outcome:** `COMPLETE`. All three targets landed: the spec carries the dated forward-sustainment amendment (MR-WI037-2/-3 rewritten, § Open decisions 2 re-ruled to computed ash, § Amendments records the supersession and its evidence); SV-042/043 descriptions amended in place with the 2026-09-01 marker (format-preserving; `agentic-mbse status` parses with no new warning class — the two 'rel dev' Invalid-Type warnings and the epic-status warnings predate this task); the `20260823-magnet-technology-ab#4` disposition row is appended (`model fix` — routed → WI-037 under this goal, increment not yet landed).
- **Evidence:** `work/active/WI-037_operating-point-closure/spec.md` § Amendments; `modeling_project/VALIDATION_MATRIX.md` SV-042/043; `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` (newest #4 row).
- **Reading:** the review's carried constraints 1–3 are discharged (the evidence repairs landed with the review commit); implementation is now unblocked. The known spec-frontmatter/backlog status warning ("spec Status='active' overrides BACKLOG.md status='backlog'") is the parser's documented resolution order, matching the WI-035 pattern; not repaired here.
- **Decision:** trigger — SV descriptions cannot be amended through a pm operation (`update-validation` is status-only). Decision and reason — amend the two rows by direct format-preserving edit with a dated marker, verified by the parser, rather than minting SV-044/045 (which would orphan two permanently-pending rows) or treating the gap as a seam repair (no seam contract exists for description amendment; the magnet-closure hand-edit revert concerned *adding* rows, for which an operation exists). Tier — execution detail. Who decided — the round agent, 2026-09-01. What changed — `modeling_project/VALIDATION_MATRIX.md` SV-042/043.

**Next task:** T-002 — the WI-037 design under the amended spec.

### T-002 scope (round 2)

- **Objective:** produce the WI-037 design under the amended spec — mechanisms for the sustainment chain (line-averaged density, ISS04 closed form, composed radiation, required sustained heating, forward ash/quasi-neutral fuel), the `sustainment_ok` constraint, wiring, retirement mechanics, tolerances, and discretization/convergence contracts.
- **Why now:** T-001 discharged the amend-first constraints; design is the native next stage.
- **Scope:** authorized — `work/active/WI-037_operating-point-closure/design.md`, reads anywhere admissible, throwaway prototypes outside `models/`; excluded — plan/implement, edits under `models/` or `exploration/`, source ingestion, discovery-log writes.
- **Inputs:** amended `spec.md`; round-2 strategy revision; round-1 evidence (image verification already performed there is cited, not redone).
- **Done when:** design.md exists, requirements-complete against amended MR-WI037-1..7, with stated tolerances and their bases, the executable-seam contract fixed, and the retirement/restatement mechanics named.
- **Stop when:** prerequisite, strategy blocker, or declared limit.

### T-002 start — 2026-09-01 (round 2)

Task T-002 (round 2): write the WI-037 design. Native target: `work/active/WI-037_operating-point-closure/design.md`.

### T-002 return — 2026-09-01 (round 2)

- **Outcome:** `COMPLETE`. `work/active/WI-037_operating-point-closure/design.md` exists, requirements-complete against amended MR-WI037-1..7: eight decisions (D1 one-calc coupled block; D2 handwritten seam with the normative discretization/convergence contract; D3 the `sustainment_ok` power limit, coupled-to-coupled; D4 wiring by reference redefinition; D5 retirement/lever set; D6 per-stage tolerances with bases; D7 the MR-WI037-7 restatement; D8 decision records for what is deliberately not done), four risks with fallbacks, file list. All quantitative bases cite the round-1 image verification rather than repeating it; the Sudo density limit is recorded as omitted-with-surfaced-gap (formula not admissibly printed).
- **Evidence:** `work/active/WI-037_operating-point-closure/design.md`; prototype backing at `evidence/T-002_prototype/` (round 1).
- **Reading:** the design keeps every standing ruling intact, adds pushback without moving the baseline physics point (D7: computed values reproduce the held ones to sub-percent at the printed levers), and localizes all new executable risk in one oracle-mirrored impl. Design approved under the 2026-09-01 delegation; recorded in the design header.
- **Decision:** trigger — where to put the ash↔W↔τ_E fixed point. Decision and reason — one calc def owns the coupled block with every stage exposed as an output (D1): splitting would expose partial iterations to the network; legibility is preserved by per-stage outputs and the documented semantic. Tier — execution detail. Who decided — the round agent, 2026-09-01. What changed — design.md D1/D2.

**Next task:** T-003 — plan + implement through the native PM.

### T-003 scope (round 2)

- **Objective:** land the WI-037 model increment — plan, then the model edits in both trees plus the handwritten impl — through the native plan/implement stages, validated.
- **Why now:** spec amended, design approved under delegation; implement is the native next stage and everything upstream is settled.
- **Scope:** authorized — `work/active/WI-037_operating-point-closure/plan.md`; edits under `models/` and the byte-identical `exploration/stellarator_e2e/models/` twins per the design's file list; the handwritten impl under `exploration/stellarator_e2e/generated/handwritten/`; `tests/models` census re-derivation if the suite instructs it; VALIDATION_MATRIX status updates through `pm` operations. Excluded — package regeneration/verification/pinning (the `integrate` seam, a later task), study execution, source ingestion, discovery-log writes, merge/push/item close.
- **Inputs:** amended `spec.md`, `design.md` (approved), round-2 strategy; `goal.md`.
- **Done when:** edits landed identically in both trees; L1 clean with the offender list unchanged; `tests/models` green (census re-derived if instructed); the implementation record written into plan.md.
- **Stop when:** prerequisite, strategy blocker, or declared limit.

### T-003 start — 2026-09-01 (round 2)

Task T-003 (round 2): plan + implement WI-037. Native targets: plan.md; `mfe_plasma_sustainment.sysml` (new), `mfe_viability.sysml`, `mfe_plant.sysml`, `stellarator_plant.sysml`, twins, handwritten impl. Expected artifacts: plan.md with implementation record; the increment on disk in both trees.

### T-003 return — 2026-09-01 (round 2)

- **Outcome:** `COMPLETE`. The § T-003 scope done-when holds in full: edits landed identically in both trees (diff-verified), L1 clean with the offender set identical to the HEAD baseline (verified by a true-baseline sweep via stash), `tests/models` 48 passed / 13 skipped with the census re-derived from the new package per the suite's own instruction string, and the implementation record is written into `plan.md`.
- **Evidence:** `work/active/WI-037_operating-point-closure/plan.md` § Implementation record; the four model files + twins; `exploration/stellarator_e2e/generated/handwritten/mfe_plasma_sustainment/plasma_sustainment_impl.py`; `tests/model_families.py`, `tests/models/data/mfe_census.json` (fingerprint `5b9abdfc…`, 193 entry points).
- **Reading:** the increment is on disk and self-consistent: the impl reproduces the round-1 prototype at the full discretization contract (p_aux_required 89.544 MW at point-A levers — the expected `sustainment_ok` violation, disclosed at the assert site), the generation tests prove the new model generates clean, and the retirement/held-fact census delta is exactly the designed set (−4 entry points, +8 held facts, +3 calc defaults). Comparison-meaning consequences are recorded at the binding sites and in design D7; the formal restatement rides the integrate return.
- **Decision:** trigger — the census fixture is fingerprint-bound and the suite failed with "re-derive from the new package". Decision and reason — re-derive now via the test module's own `_generate`/`_contract` helpers (the suite's stated resolution; generation is hermetic in tmp) rather than defer the whole suite-green state to integrate; the integrate seam's census gate re-verifies freshness against the real regeneration. Tier — execution detail. Who decided — the round agent, 2026-09-01. What changed — `tests/models/data/mfe_census.json`, `tests/model_families.py`.

**Next task:** T-004 — the `integrate` seam (regeneration → verification → pin), including the oracle mirror and caller-order verification.

### T-004 scope (round 2)

- **Objective:** produce one study-ready `CANDIDATE` pin for the WI-037 increment through the native `integrate` seam — regeneration, oracle extension for the sustainment calc, verification, pin — or a named `BLOCKER`.
- **Why now:** the increment is landed and validated at model level (T-003); a round is bounded by one promoted pin, and the study (T-005) needs it.
- **Scope:** authorized — the regeneration outputs under `exploration/stellarator_e2e/generated/`, the oracle/runner extensions the seam's procedure requires, `scripts/integrate.py` invocation per `docs/integration_seam_operator_guide.md`, the MR-WI037-7 restatement record; excluded — study execution, any further `models/` semantic change (a needed one is a `PREREQUISITE` return), merge/push.
- **Inputs:** T-003's landed increment; the seam guide; `goal.md` invariants (one pin per round).
- **Done when:** `integrate.py` returns exactly one `CANDIDATE` with fingerprints, deposited as goal evidence; the restatement recorded before the regeneration is accepted.
- **Stop when:** a named `BLOCKER` that requires semantic rework (→ next task decides), prerequisite, or declared limit.

### T-004 start — 2026-09-01 (round 2)

Task T-004 (round 2): invoke the integrate seam for the WI-037 increment. Native target: `exploration/stellarator_e2e/generated/` + `scripts/integrate.py`. Expected artifact: one CANDIDATE pin return (deposited under evidence/), or a named BLOCKER.

### T-004 return — 2026-09-01 (round 2)

- **Outcome:** `COMPLETE`. The seam returned a **`CANDIDATE`**: pin `35e922c5cc15eacabf301e6007b94e7dee1bfe1f45f6c23c24233098f0125289`, semantic `5b9abdfc…`, executable `41e06ecb…`, package `exploration/stellarator_e2e/generated`, all ten gates `pass` (regeneration byte-stable, handwritten 66/66 preserved, census 193 entry points as bound, spine suite green, manifest pin recomputed, six preflight gates, oracle parity with every verdict re-derived — including the expected-violated `sustainment_ok` — lineage as named).
- **Evidence:** `work/orchestration/goals/operating-point-closure/evidence/T-004_integration_return.json` (+ `T-004_verification_summary.json`), copied from the transient out-dir (magnet-closure precedent). Commits: `728d1263` (audited item state, T-003), `ff807d3d` (regeneration hop: package regen + reseal, snapshot recaptured, manifest re-pinned, oracle seam + independent oracle extended with the sustainment mirror at parity rel 0.0, known-answer fixtures re-derived, 8-constraint suite constants, MR-WI037-7 restatement), `5bea8964` (remaining suite constants). `tests/study`: 348+2 passed in the seam environment (the lone teax-probe failure reproduces only under an externally exported PYTHONPATH; it passes in the seam's own environment). `tests/models`: green via the seam's spine gate.
- **New baseline headline (bit-exact against the extended oracle before pinning, never fitted):** LCOE 304.482 → **307.087** $/MWh, p_fus 2748.06 → **2725.36 MW** (computed quasi-neutral fuel −0.83%), total capital $14.574B → $14.543B; verdict set 7 → **8**, `sustainment_ok` **violated** at baseline (p_aux_required 90.605 MW vs 50 installed — the disclosed W-form-dominated residual), all others satisfied.
- **Goal-level reading.** The round's one pin exists and is proven — and the regeneration's own reachability re-derivation produced the goal's structural evidence early: the I_coil (field) lever now reaches `sustainment_ok`, `net_positive`, `recirc_ok`, `wall_load_ok` and the fuel/replacement/capital objectives through the ISS04 chain — the mechanical close of `20260823-magnet-technology-ab#4` ("field never rewarded"); R and a gained `beta_ok` + `sustainment_ok` through the ash→fuel chain; availability/interest_rate still reach nothing (the Row 11 finding stands, correctly untouched). The R+tie test's objective-subset assertion flipped to equality — the tie's added value is now purely fence-side — recorded in the test with its explanation, evidence over expectation.
- **Decision:** trigger — first single-runner pass failed on stale anchors and a seal violation. Decision and reason — the seal violation was the handwritten impl edited after sealing (reseal by regeneration, retry mechanical); the nine anchors were re-derived from the verified execution only after bit-exact oracle parity held (never patched-to-match), with the pre-WI-037 values left in git history. Tier — execution detail. Who decided — the round agent, 2026-09-01. What changed — `run_stellaris_single.py` anchors + verdict gate, `ff807d3d`.
- **Decision:** trigger — a stale `.integration_workspace` from a timeout-killed test run poisoned every integrate fixture. Decision and reason — remove and re-run; classified mechanical (identical task/inputs/meaning). Tier — execution detail. Who decided — the round agent, 2026-09-01. What changed — none (untracked directory removed).

**Next task:** T-005 — the round's one committed study, per the strategy's intended question.

### T-005 scope (round 2)

- **Objective:** execute the round's one committed study against the T-004 candidate pin — the strategy's intended question: with the sustainment fence active, is field rewarded (does the constrained optimum leave the beta floor — the `magnet-ab#4` pathology), and where do the power, beta, wall-load, conductor-ceiling, and stress fences bind over the field lever (I_coil), the operating-point levers (n_e0, T_i0), and heating (p_input) — is the L-003 three-way trade visible in a committed record?
- **Why now:** the pin exists and is proven (T-004); a valid study reading is the round's closing trigger; no abandonment condition is triggered.
- **Scope:** authorized — the record directory `exploration/stellarator_e2e/studies/20260901-sustainment-fence/` per the run-study skill (execute mode), first-sighting discovery-log rows at the runbook's step, the study commit. Excluded — any `models/` or library/tool edit, rubric edits, the re-grade, disposition rows for prior studies' findings (the round result owes those), any second study or pin.
- **Inputs:** the candidate (`evidence/T-004_integration_return.json`, pin `35e922c5…`); `goal.md` invariants (comparisons against this pin; SV-016 untouched); `.claude/skills/run-study/` runbook + `modeling_project/STUDY_POLICY.md`.
- **Done when:** a committed study record with its § 15 findings register and log rows — an adverse or disappointing reading still closes the round.
- **Stop when:** an axis traces `no_constraint_response` needing a ruling the delegation does not cover, a mechanical failure past the retry cap, or a strategy blocker.

### T-005 start — 2026-09-01 (round 2)

Task T-005: execute study `20260901-sustainment-fence` through the run-study runbook against pin `35e922c5…`. Native targets: the record directory, DISCOVERY_LOG first-sighting rows, one study commit. Expected artifact: the committed record.

### T-005 return — 2026-09-01 (round 2)

- **Outcome:** `COMPLETE`. The round's one committed study exists: `exploration/stellarator_e2e/studies/20260901-sustainment-fence/` at commit `1d28454f` — record, snapshot, indicators, four results CSVs, verification summary, four § 15 findings with joined DISCOVERY_LOG rows. `tests/study/test_records.py`: 16 passed.
- **Evidence:** the record directory (all claims cite `results/`); pre-execution critique deposited at `evidence/T-005_precritique.md` (verdict MAJOR, all seven findings dispositioned before any point ran — record § 14).
- **Reading (executor-level; the fresh administrator's synthesis is the reading of record):** the strategy's question is answered in the committed evidence. (a) Field is rewarded: I_coil reaches all seven constraints and the fusion chain; the p=110 feasible optimum (LCOE 293.468) sits at beta 0.0311 — **off the 0.05 beta floor** — bounded below by `sustainment_ok` and above by the conductor ceiling. The `magnet-ab#4` pathology is inverted: the fence that stops field is magnet technology, not plasma stability. (b) The L-003 three-way trade is visible: sustainment relief vs conductor ceiling vs stress, with the p=50 slice's pre-registered empty feasible set showing the deadlock at the printed installed power. (c) The machine's honest state: no feasible operating point at 50 MW installed anywhere in the swept space; feasibility needs ≥ ~91 MW installed or a conductor-grade change.
- **Decision:** trigger — the store cannot carry the six sustainment quantities (multi-field module, the pb__* limitation), discovered when the first export shipped empty columns. Decision and reason — correct pre-commit by oracle-side export (the documented pb precedent), disclose in record § 13/§ 15 (#3) and the ANNEX; not a retry (no point re-ran; the export pass is not the task's meaning). Tier — execution detail. Who decided — the round agent, 2026-09-01. What changed — `study.py` exports, `oracle_operands.csv`, ANNEX § Oracle.

**Next:** the study.read seam — a fresh administrator writes the synthesis; then the goal-level dispositions go to the pre-execution checkpoint before the re-grade task.

### Checkpoint C-001.r1 — 2026-09-01

- **Reviewer:** fresh non-author session (third session of the round's gate chain: not the executor, not the administrator).
- **Reading reviewed:** `20260901-sustainment-fence/synthesis.md` (the administrator's reading of record) + record § 15/Addendum.
- **Dispositions reviewed:** `evidence/T-005_proposed_dispositions.md` (r1).
- **Verdict:** `REVISE`.
- **Revision:** 1 of 2. The reviewer independently recounted the crux evidence and upheld all five readings — including the hardest, the `20260823-magnet-technology-ab#4` discharge ("field rewarded by the physics and capped by the conductor — the inversion of the sighted mechanism"), with a not-final caution to carry onto the appended row. Required changes: dispositions 2 and 5 must bear an ADR-0004 class (`model fix`) with status/actor named (the C-001.r2 and rows-53/54 precedents), and class-bearing rows for `#1` and `#4` must be promised at round close. Author revised in place as § Revision r2 of the same document.
