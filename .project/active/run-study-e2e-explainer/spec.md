# Spec: End-to-End Explainer for the Run-Study A/B Demo

**Status:** Approved [OWNER 2026-08-23]
**Owner:** Reid W
**Created:** 2026-08-23 11:14
**Complexity:** MEDIUM
**Branch:** `feat/run-study-first-consumer` (sequenced before Item 6 Phase 4; branch choice for the work itself is the plan's)

---

## Problem

The run-study capability now has two certified A/B studies on the Stellaris package (`exploration/stellarator_e2e/studies/20260821-power-cycle-ab/`, `.../20260823-magnet-technology-ab/`). Every artifact that explains them is written for an insider: the runbook, the record template, the records themselves, the plan. Nothing shows an outside reader *how the chain works end to end* — a SysML v2 model becomes a sealed Python package, the package runs under teax, a study sweeps it, and an A/B result comes out with named constraint verdicts.

**[OWNER 2026-08-23]** "I feel like there is a gap in the epic and study plan. Specifically, I need a RIGOROUS and deep HTML explainer. It needs to convey, by example, HOW this end-to-end work." The explainer is to be done **before Item 6 Phase 4** (close), while the two studies and their context are fresh and on the branch.

The reader **[OWNER 2026-08-23]**: an outside party with "vague concept of SysMLv2 from our prior publications, and only has knowledge about fusion-tea from prior publications." Not a fusion-TEA specialist; not a user of this repo.

Scope ruling **[OWNER 2026-08-23]**: "I want this for the studies we just completed. do not worry about the other Item 8." The stellarator demo epic's write-up item (handshake framing, ARIES-CS hold-out) is not this item's concern.

What "end-to-end" covers **[OWNER-VERBATIM 2026-08-23]**, asked whether the page must show how the study itself ran (prompt → axes → indicators and rulings → preflight → execution → verification → record → cold synthesis → discovery log) and not only how a model becomes numbers: "absolutely fucking yes -- this is explanation BY EXAMPLE. SHOW how this works. DEMONSTRATE the value." The page has two layers, both by worked example: the toolchain (model → package → teax → A/B result) and the study process that ran on it (the run-study capability, which is what the epic built).

## Success Criteria

- [ ] A reader matching the profile above, given only the page, can answer: what each of the four components does (agentic-mbse, sysml-codegen, teax, fusion-tea); how a SysML model turned into the inputs the package consumes; what those inputs looked like; how the two A/B comparisons were executed; what each study found, in LCOE and in named constraint outcomes.
- [ ] The same reader can also answer, for at least one study: what the owner's prompt was; what the agent declared and what the indicators said before any point ran; what rulings the owner was asked for and why; what preflight and verification checked; what the record is and why it is immutable; how a second agent with no session memory reproduced the numbers from the record alone and what it corrected; what the studies taught about the model (the discovery-log findings, with their homes). The page answers these with the studies' real artifacts as exhibits, not with a description of the procedure.
- [ ] The reader can say, in their own words, what the capability bought: a short prompt became a verified, cold-readable, auditable A/B result, and the misses it surfaced became filed model-development work. If the page cannot make that case from the two studies, that is a finding against the page, not against the studies.
- [ ] That claim is tested the way the epic tests its records: one fresh subagent with the reader profile, given the page alone (no repo access), answers a fixed question list; every answer traces to a page section. Misses are findings, fixed before close.
- [ ] The page opens with the conclusion and the mental model (pyramid); every later section deepens the same progression rather than introducing a new one.
- [ ] An always-visible navigation guide lets the reader jump to any section and shows which section they are in.
- [ ] The required technical elements are each present and findable from the nav: an interactive representation of the model; the costed-component pattern; the physics models; the A/B execution; the codegen → inputs step; the inputs, organized against the model they parameterize.
- [ ] The study-process elements are each present and findable from the nav, as exhibits from the committed records: the verbatim intake; `axes.json` and the indicator output; the owner rulings and the declined axes; the preflight gates; the verification summary (what was sampled, what was re-derived, the worst deviation); the record's structure; the administrator brief and `synthesis.md`; the discovery-log rows these studies produced.
- [ ] Every quantitative claim on the page traces to a committed artifact (a record section, `results/` file, `model_contract.json`, or `inputs/*.json`), and the page says where.
- [ ] The page says, per study, what the model computed and what the study harness supplied or assumed: the engineered windows (`arms[].window` provenance), the five `pb__*` channels the store does not record (study 2 finding #5), the evaluability floor at negative net power (study 1), and each record's addenda corrections. Honesty floor, distinct from the numbers-match floor above (product-lens spec-F2).
- [ ] Readability bar: no paragraph longer than a few sentences; mental frameworks set up as bullets or tables; diagrams/charts carry the structure; every key term defined at first use; expected follow-up questions answered in collapsible sections.
- [ ] The page renders from a fresh checkout with no build server and passes a `browser-inspect` check (nav works, no console errors, visuals render, responsive).

## Known Requirements

Owner's criteria, verbatim where stated (the list is the owner's; grouping is mine):

- **[NEED]** "Must tell a coherent story that is approachable from an outside party": brief background for the overall SysML-driven TEA modeling; the main components ("agentic, sysml-codegen, teax, and then fusion-tea"); the goals for this demo ("show it works with a toy example").
- **[NEED]** "Must follow all best practices for technical explainers": simple explanations; highly readable — "no blocks of text", "use bullet points and tables to set up mental frameworks", "maximize use of other visuals as well (diagrams, charts and such)"; "No loaded jargon: any key terms get defined".
- **[NEED]** "'Consulting style pyramid': important information up front. Later sections can walk through the same progression but providing more detail or a specific angle. Answering expected questions with more detail: use collapsible sections."
- **[NEED]** "Must have an always-visible navbar guide so the reader can jump around, and also understand where they are in the explainer."
- **[NEED]** Technical elements which "MUST be present": an interactive model representation; use of the costed-component pattern; the physics models; an explanation of how the A/B comparisons were executed, how the sysml-codegen → inputs step was done, and what the inputs looked like ("ideally organized with the models").
- **[NEED]** The page is written for the stated reader (vague SysML v2 from prior publications, fusion-tea from prior publications only).
- **[NEED]** Subject is the two completed studies; the page lives in the studies folder, `exploration/stellarator_e2e/studies/`, beside the records it explains.
- **[HARD]** `knowledge/holdout/` is never read, cited, or referenced (`knowledge/holdout/aries-cs/PROTOCOL.md`). The explainer must not carry ARIES-CS comparison content; it does not exist and is barred.
- **[HARD]** Study records are immutable once committed (`.claude/skills/run-study/runbook.md`; corrections go in addenda). The explainer reads the records and `results/`; it does not edit them. Numbers quoted must match the record *as corrected by its addenda*, since both records carry corrections.
- **[HARD]** The explainer must be self-contained to render: single-file or multi-file static HTML with inline or relative assets, no server, no build step (the `html-explainer` skill's contract; `docs/demo/*.html` precedent).
- **[INHERITED]** Follow the `html-explainer` skill: a markdown story outline reviewed with the owner before HTML; 1cFE styling; ~1500-line target / 2000-line ceiling per file, split into a multi-page set when exceeded (`.claude/skills/html-explainer/SKILL.md`).
- **[INHERITED]** Run-study Item 6 Phase 4 does not start until this item closes (`.project/active/run-study-first-consumer/plan.md`, gate to be added there).
- **[NEED]** The page demonstrates the run-study capability by example: the study-process layer (intake → axes and indicators → rulings → preflight → execution → verification → immutable record → fresh-administrator synthesis → discovery log) is shown on the two real studies, with their artifacts as exhibits (`[OWNER-VERBATIM 2026-08-23]`, Problem).
- **[INFERRED]** Verification is explained at the level the reader needs to believe the numbers: the oracle fidelity check on generated code and `verify.py`'s stratified re-derivation; the oracle's retirement after Item 6 is stated so the page does not present it as permanent.
- **[INFERRED]** The facts the page relies on are these, and they bound its content: the `Costed Component` abstract part def (`models/library/foundation/costed_component.sysml:4-19`) with the CAS hierarchy specializing it (`modeling_project/ARCHITECTURE.md` AD-005, AD-007); the six plasma calcs plus power balance, cryo, magnet cost, accounts, LCOE DCF, viability (`exploration/stellarator_e2e/models/analyses/*.sysml`, generated twins under `generated/modules/`); the package contract (`generated/contracts/model_contract.json`, 173 parameters as `design_attribute` / `library_default` / `usage_literal`, six constraint ids) and input files (`generated/inputs/*_params.json`, flat `<design>__<usage>__<attr>` keys); the arm blocks and `study_route.run_points` as the A/B mechanism (`studies/*/study.py`, `studies/study_route.py:180`).
- **[INFERRED]** Figures and any data embedded in the page regenerate from the committed artifacts by script, not hand-edited (the demo epic's "regeneration path" rule, applied here because the records are the source of truth).

## Non-Goals

- The 1costingFE handshake narrative, forward-pass vs inverse-solver framing, and the ARIES-CS hold-out — those belong to the on-hold demo epic's write-up and are out of scope here `[OWNER 2026-08-23]`.
- A blog post or any hosting/publishing beyond a static page in the repo.
- A new or reduced "toy" model: the toy example is the Stellaris package and its two studies as they stand.
- Changes to the run-study tools, runbook, records, or the model package. This item writes and reads; it does not modify the capability (Item 6 invariant I1 still holds on the branch).
- A general SysML-structure viewer product. The interactive model representation serves this page; whether it is reusable is a design choice, not a requirement.
- Re-running either study.

## Open Questions / Deferred to design

- What "interactive model representation" is mechanically: a clickable part/calc tree with inputs attached per node, an expandable structure graph (the Cytoscape proof of concept at `proof_of_concept/cytoscape_demo.html` is a precedent), or something else. Design decides; the requirement is that a reader can explore the model's structure and see inputs where they attach.
- Single page with a sidebar vs a multi-page set with shared nav. Depth argues for multi-page; the nav criterion holds either way.
- Which figures are interactive (hover per point on the feasible-region maps) vs static, and what library renders them within the self-contained constraint.
- How the "same progression at more depth" is laid out: one spine with depth tiers, or a spine plus per-angle chapters.
- The fixed question list for the fresh-reader test, and whether it is kept in the item dir as a reusable fixture.
- Whether this item runs on `feat/run-study-first-consumer` or its own branch off it (plan).
- Which prior publications the reader is assumed to have seen (candidates: `docs/demo/index.html`, `docs/concept-pipeline/pipeline.md`); affects how much background is restated vs linked.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_run_study_capability.md` — new item (Item 7) to be added there at approval; it also gates Item 6 Phase 4
- **Required Reading:** `.project/active/run-study-first-consumer/{spec,design,plan}.md`; `.project/concepts/run-study-skill.md` (owner's words on roles and the record seam); `.claude/skills/run-study/{SKILL,runbook,record-template}.md`; the two records and their addenda, `axes.json`, `indicators.json`, `results/`, `synthesis.md`, and the administrator briefs under `.project/active/run-study-first-consumer/briefs/`; `exploration/stellarator_e2e/studies/{ANNEX,DISCOVERY_LOG}.md`; `.claude/skills/html-explainer/{SKILL,explainer-guidelines}.md`; `modeling_project/ARCHITECTURE.md` (AD-002, AD-005, AD-006, AD-007); `exploration/stellarator_e2e/STAGED_MODELS.md`
- **Research:** none filed; the component map gathered at spec time is in the `[INFERRED]` facts item above
- **Product-lens:** `.project/active/run-study-e2e-explainer/product-lens.md`
- **Design:** `.project/active/run-study-e2e-explainer/design.md` (to be created)

---

**Next Steps:** After approval, add the epic row and the Phase 4 gate line, then `/_my_design`.
