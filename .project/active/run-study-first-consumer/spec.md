# Spec: Run-Study First Consumer (RUN-STUDY Item 6)

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-08-21 13:58
**Complexity:** HIGH
**Branch:** `feat/run-study-first-consumer` (off `main` `8d6c443b`, migration PR #107 merged)

---

## Problem

The run-study capability (Items 1–5) has never been used end to end. Every obligation it formalized was proven on pieces: tools against known answers, the record contract against a pre-capability study, the administrator on a directory that was not a record. No study has been invoked with a goal-only prompt, run on the stock teax route, committed a capability-compliant record, and been handed to a fresh administrator. Until one has, the epic's critical success factor is unproven: **[OWNER]** "A short-prompt study reaches the proof-of-life's verification and reporting floor, and a fresh administrator can synthesize it from the committed record alone."

The study that proves it is the demo's magnet-technology A/B comparison. **[OWNER-VERBATIM 2026-08-19]** "I'm fine with this epic owning the A/B proof -- the demo epic is on hold." The model migration (2026-08-21) removed the last blocker: the package is sealed at runtime contract 2.0.0, runs on stock teax `744745f` with no adapter, and the CAS27 verification hole is closed.

Three things this item also settles because the first consumer is where they land (Align 2026-08-21, `align.md`):
- The study policy is ratified and moves to its durable home; the skill and runbook stop citing an active-work draft.
- The comparison was chosen by research (`.project/research/20260821-141439_item6-ab-candidates.md`). **[OWNER] 2026-08-21:** two studies, two records: (1) HTS REBCO (20 K) vs LTS Nb3Sn (4.5 K) magnets, and (2) steam Rankine vs sCO2 power conversion. Study 2 needs no model change. Study 1 is only honest with a computed beta and a peak-field constraint, because today B enters the model only through magnet cost and beta is a bound input, so an LTS arm at the Stellaris geometry runs with nothing objecting. That modeling is a `work/` item and runs while study 2 executes.
- The oracle's role is decided. **[OWNER-VERBATIM 2026-08-21]** "check 1 ONLY FOR THIS DEMO -- once it is demonstrated, I don't want to have to keep two sets of equations."

## Success Criteria

- [ ] `modeling_project/STUDY_POLICY.md` exists: the draft policy moved whole, plus an axis-forces section, H1's 5–95% bar scoped to search-framed studies, and the two dispositions from the Align (oracle is a generated-code fidelity check for this demo only and leaves the study contract afterward; the 1costingFE handshake is outside the study contract, used when a direct comparison is readily possible). The owner approved the final draft before it was committed. Every citation in `SKILL.md`, `runbook.md`, the concepts, and the epic points at the new path; the draft path is gone.
- [ ] The design records, for each of the two studies, the arms, the block of values that moves together with each value's source, the per-arm sweep shape, and the indicator results for the block. The owner's ruling on each is recorded.
- [ ] A `work/` modeling item exists for study 1's prerequisites (computed volume-averaged beta replacing the bound `beta`; peak-field constraint `B × 2.767 ≤ B_max` with the REBCO ceiling bound at 24.9 T), and study 1 does not execute until that item closes and the package is regenerated and re-pinned. Study 2 executes on the current sealed package and does not wait.
- [ ] A research round in the modeling PM runs before either study executes, targeting the unsourced values the research named (sCO2 primary pumping power; arm-A eta_th provenance; fraction-of-Carnot at 4.5 K; Nb3Sn winding-pack volume). Each value is either sourced with a citation or recorded as a disclosed hold; none is defaulted.
- [ ] Each study is invoked with the owner's goal and scope only (no process, verification, or reporting instructions) and completes under the runbook. The record lives at `exploration/stellarator_e2e/studies/<study-id>/` with every template section filled, one arm per section, each arm naming its store and complete compatibility tuple, and the cross-fingerprint correlation stated or its nil discharged.
- [ ] Every `no_constraint_response` axis carries the owner's ruling and a model-development finding in the record before any point ran.
- [ ] Every point ran through the stock teax lifecycle on the direct-API route (`studies/study_route.py` or its successor); the package is git-clean after the run; the record states LCOE and the qualified identity and `satisfied | violated | indeterminate` status of every executing constraint, per arm.
- [ ] Oracle verification ran (runbook steps 7 and 10) with its outcome recorded, and every channel the oracle did not compare is named in the record.
- [ ] For each record, a fresh-context administrator, reading only the record directory, writes `synthesis.md` that recovers each arm's framing, LCOE, named constraint outcomes, and evidence-backed findings; every fact it could not recover is listed under "What the record does not support".
- [ ] At least one proof-of-life process lesson reaches the first study executed from exactly one home (e.g. stratified verification sampling from `scripts/study/verify.py`), and its record cites that home instead of re-deriving the lesson (epic criterion 4, second half). The second study executed cites at least one finding or lesson from the first record through the discovery log.
- [ ] `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` exists and indexes every model and process finding from the study with disposition and home.
- [ ] The record's oracle digest carries `{recipe, digest, files[]}` in both template locations and a contract check against the emitted shape exists (Item 5 gap G1).
- [ ] A backlog row exists for retiring the oracle from the study contract (runbook gates, manifest requirement, tests) after this item closes.
- [ ] `tests/study` and `tests/models` stay green; no regression to the after-migration record's evidence.

## Known Requirements

- **[HARD]** Stock teax `744745f`'s CLI builds only a Cartesian `GridStrategy` (`simkit/study/config.py:126`). A swap block that moves more than one key together must run on the direct-API route (`StudyRunner` + `PreparedListStrategy`).
- **[HARD]** teax refuses a store whose compatibility tuple does not match the study definition; `preflight.py` and `verify.py` refuse a package that is not git-clean or whose manifest fingerprint disagrees with the package on disk. A regenerated package re-pins `manifest.json` and the known-answer fixtures before any study step passes.
- **[HARD]** `knowledge/holdout/aries-cs/` is sealed (`PROTOCOL.md`, `status: sealed`). The design's research into a second magnet arm, and any new modeling it triggers, never reads, cites, or derives from that material. ARIES-CS is the one public LTS stellarator design with costing, so this is the case the protocol exists for.
- **[HARD]** The runbook fails closed at step 4: an axis reported `no_constraint_response` cannot reach execution without a recorded user ruling.
- **[NEED]** The invocation carries only the owner's goal and scope, in the owner's words, kept verbatim in the record (concept SC-1, `[OWNER]`).
- **[NEED]** Two studies, two records: REBCO vs Nb3Sn magnets, and Rankine vs sCO2 conversion (`[OWNER]` 2026-08-21, `align.md` § 2a). A four-arm crossed study is not required.
- **[NEED]** The REBCO peak-field ceiling is bound at 24.9 T, the value Stellaris designs to, not the upstream 23.0 T (`[OWNER]` 2026-08-21).
- **[NEED]** Missing second-arm values are pursued by a research round in the modeling PM before execution; what it cannot source is a disclosed hold (`[OWNER]` 2026-08-21: "in our `work/` we can add an automated research cycle to try to source more data").
- **[NEED]** Every value for a second arm comes from a source the owner accepts and carries its citation; an agent default is never used (no-fallbacks rule; `modeling_project/OVERVIEW.md` Traceability Requirements). The owner's ruling on the comparison covers its sources, not only its arms.
- **[NEED]** New modeling, if needed, runs as its own `work/` item and Item 6 pauses until it closes (`[OWNER]` 2026-08-21: "Item 6 should PAUSE and the modeling change should be executed through the `work/` item").
- **[NEED]** The policy is ratified whole and moved; the owner reviews the final draft before it is committed (`[OWNER]` 2026-08-21).
- **[NEED]** Oracle verification runs for this demo and not as a standing study obligation afterward; no second set of equations is maintained for studies in general (`[OWNER-VERBATIM]`, Problem).
- **[NEED]** The 1costingFE handshake never gates a study; it is run when a direct comparison is readily possible (`[OWNER]` 2026-08-21: "I do not want to constrain what we can model by what that library can model").
- **[NEED]** "Nothing pushes back" on a requested axis is returned to the owner as a model-underdevelopment finding with the ruling, never gated or relabeled (concept, `[OWNER]`).
- **[NEED]** A fresh administrator synthesizes from the record alone (concept SC-4, `[OWNER]`).
- **[INHERITED]** One store per complete teax compatibility tuple; arms in one study definition share a store; a cross-fingerprint A/B states the correlation in the record, never in a merged store (`run-study-skill-design.md:129`, agent, ratified 2026-08-19).
- **[INHERITED]** The record shape is arm-scoped for every field that can differ between arms (`run-study-contract` design D4 as amended by MF2).
- **[INHERITED]** Every value the harness supplies that the model does not is disclosed; on this package that is "glue ledger: none" (`ANNEX.md`).
- **[INFERRED]** Whether `magnet_capital` and `p_fus` join the oracle's compared channels (a data-only addition to the manifest's objective catalog) or are disclosed as uncovered is decided at design; a magnet study moves magnet capital first, so the disclosure is not cosmetic.
- **[INFERRED]** The item's branch is cut from `main` after the migration PR merges; running on the migration branch would couple this item to that PR's review.

## Non-Goals

- Visualization or search-process animation (demo epic Item 6).
- Optimizer or adaptive study strategies; grids and prepared lists only.
- Closing model gaps inside this item: a gap the design or the study finds becomes a `work/` item (the pause rule) or a discovery-log row, never an in-item model edit.
- Retiring the oracle from the study contract in this item. The disposition is recorded in the policy and the retirement is filed as a follow-up; changing the runbook's gates while the study that exercises them is running would make the record's evidence ambiguous about which contract it ran under.
- Rewriting `handshake_1costingfe.py` for the 2.0.0 package (BACKLOG row, P3, demo epic evidence).
- Resuming the demo epic.

## Open Questions / Deferred to design

- **Each study's block and sweep shape.** The research names the candidate blocks (`align.md` § 2a; research doc § per candidate). The design fixes the exact keys per arm, the per-arm sweep (the research suggests density per arm, plus B for the Nb3Sn arm), and the windows, and brings the indicator results and any `no_constraint_response` ruling to the owner before the plan runs a point.
- **Whether study 2 runs before or after the research round completes** for the sCO2 pumping-power value, or runs with it as a disclosed hold.
- **The `work/` item's exact shape** (one item for beta + peak-field, or two), and whether the research round is its own `work/` item or a phase of the modeling item.
- **Oracle coverage** for the channels the comparison moves (`[INFERRED]` above).
- **How the fresh administrator is spawned** (a subagent with no conversation context, or a separate session) and how "fresh" is evidenced in the record.
- **The axis-forces section's content** for the policy, distilled from runbook steps 2–4 and the concept's SC-2.
- **Execution-route module:** whether `studies/study_route.py` runs the A/B as is or needs an arm-aware entry; the runbook's route rationale is recorded after the route is exercised (step 8).
- **Invocation wording.** The owner's goal-and-scope text is given at execution time, after the design's research; the spec does not draft it.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_run_study_capability.md` — Item 6
- **Align record:** `.project/active/run-study-first-consumer/align.md` (decisions 2026-08-21, starting facts for design)
- **Required Reading:** `.project/concepts/run-study-skill.md`; `.project/concepts/run-study-skill-design.md`; `.project/active/demo-study-parameterization-policy/policy.md`; `.project/backlog/epic_stellarator_mbse_demo.md` (Item 5 historical scope and the on-hold boundary); Items 1–5 outputs under `.project/completed/20260821_run-study-*/`; teax study docs at `744745f`
- **Capability surfaces:** `.claude/skills/run-study/{SKILL,runbook,record-template}.md`; `scripts/study/`; `exploration/stellarator_e2e/studies/{ANNEX.md,manifest.json,study_route.py,oracle_entry.py}`
- **Research:** `.project/research/20260821-141439_item6-ab-candidates.md` (the four candidates, ranking, modeling changes, second-arm data tables)
- **Migration evidence:** `exploration/stellarator_e2e/studies/AFTER_MIGRATION_RECORD.md`
- **Product lens:** `.project/active/run-study-first-consumer/product-lens.md`
- **Design:** `.project/active/run-study-first-consumer/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`. The design covers both studies and the two `work/` prerequisites (research round; modeling item), and returns to the owner with per-study blocks and indicator results before anything is planned.
