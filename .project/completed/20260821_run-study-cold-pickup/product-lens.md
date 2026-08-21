## spec — 2026-08-20 — rev cfffcc3a (`.project/active/run-study-cold-pickup/spec.md`)
Epic: RUN-STUDY
Epic-gate references (owner grade, preserved; references only): `epic-F1` [DO] cold pickup must be proved on a new capability-compliant record, the legacy exercise alone is insufficient — FIXED (Item 6 owns that proof; Item 5 is the legacy gap exercise). `epic-F2` [DO] the record contract must require LCOE plus qualified constraint identity and status — FIXED (Item 2 + epic criterion 3).
Sources absent: `.project/adr/` and `.project/product/` do not exist (0 entries); README and `docs/` carry no run-study statement. The oracle below is derived from the concept, the prior concept, and the epic's owner-graded criteria.
Point (re-derived): A second agent, given only the committed study record and nothing from the executing session, recovers the framing per axis, the LCOE result, every executing constraint's named outcome, and findings traceable to committed evidence; whatever that reader needed and the record did not carry is a defect in the record contract, and every model or process finding the work produces is indexed with a disposition and a destination.   [source: `.project/concepts/run-study-skill.md` Owner's Words (roles, verbatim) + Success Criteria 4; `.project/backlog/epic_run_study_capability.md` Success Criteria 3 and 4 ([OWNER]); `.project/concepts/study-driven-model-development.md` Owner's Words ("make the log of discoveries an explicit deliverable"), grade: owner]
Falsifier: After Item 5 closes, Item 6's fresh administrator needs a fact the template never asked for that the legacy directory could have exposed; or Item 5's synthesis cites anything outside `exploration/stellarator_e2e/study/`; or a finding Item 5 produced reaches epic close with no disposition or no destination.
Checked, no finding:
- Tracked-only evidence surface does not narrow the claim. Every owner-grade statement says "committed" / "only that record" (concept SC4, epic CSF and criterion 3); `_work/` is gitignored and absent from a fresh clone. The restriction errs toward exposing more absences, not fewer; the dropped qualified constraint ids become a correctly reported limitation (contract already requires them, runbook step 9).
- The four facts the spec's synthesis must state match the owner's list exactly (framing per axis, LCOE, named constraint outcomes, evidence-backed findings); the gap/limitation split matches the design's "a gap is not a reason to soften the contract" and drops no owner-stated fact.
Findings:
- spec-F1 [DO]    A gap that is real but not load-bearing (bucket = template or runbook, not applied) has no stated disposition: SC3 gives every absence a destination, SC4 gives a disposition only to load-bearing gaps, SC3 only to limitations ("no action"). The owner's obligation is disposition and destination for every process finding; the contract's own form is "Home never blank, `unrouted` is a stated state" (runbook step 15). — `.project/backlog/epic_run_study_capability.md` Success Criteria 4 (owner) — disposition: BLOCK. Clears with one line in SC3/SC4: every gap entry, load-bearing or not, carries a disposition (applied | deferred to <home> | dropped, with reason).
- spec-F2 [DO]    The spec's recommended indexing home leaves Item 5's findings un-indexed in the discovery log and relies on Item 6 "to seed the log with" them, an obligation neither this spec nor the epic's Item 6 scope records (Item 6 lists only the A/B record's own log entry). The reason given, "the administrator does not write the discovery log", constrains the administrator, not this item: the runbook says a synthesis finding "is filed by whoever acts on the synthesis", which here is Item 5's implementer applying the gaps. — `.project/backlog/epic_run_study_capability.md` Success Criteria 4 (owner); `.project/concepts/study-driven-model-development.md` Owner's Words (owner-verbatim) — disposition: BLOCK. Owner picks one: (a) Item 5 creates `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` and its implementer files the rows (Record column carries the legacy directory path in place of a study id, stated as such); or (b) the spec makes the handoff an explicit Item 5 deliverable that Item 6 consumes, and the epic's Item 6 scope names it.
- spec-F3 [DO]    The directory-only rule is graded `[HARD]` (external-constraint vocabulary) though it is owner-originated: concept SC4 "given only the committed study record ... without consulting the executing session" and the roles quote. It belongs at `[NEED]` carrying that cite, so later stages challenge it by asking the owner rather than treating it as an external fact. — capture-fidelity absorb mapping, my inference (AGENT) — disposition: DISPOSE-and-proceed; regrade in place.
Smells: none fired (spec stage; the §4 smells are design-review and audit tripwires).
Gate: BLOCKED (spec-F1, spec-F2)

### Dispositions — 2026-08-20 (spec author)
- spec-F1: FIXED — Success Criteria 4 reworded: every gap entry, load-bearing or not, carries a disposition (`applied` | `deferred to <home>` | `dropped, <reason>`).
- spec-F3: FIXED — directory-only rule regraded `[HARD]` → `[NEED]` with the concept SC4 cite.
- spec-F2: OPEN — awaiting owner pick between (a) Item 5 creates `DISCOVERY_LOG.md` and files its rows, or (b) an explicit Item 5 → Item 6 handoff deliverable named in the epic's Item 6 scope. Gate stays BLOCKED until dispositioned.
- spec-F2: DISPOSED by owner ruling (2026-08-20) — the finding conflated two things. `gaps.md` entries are contract-check results (a one-time verification of the Item 2 template), not study findings; they get no discovery-log row and Item 5 creates no log. Model findings appear in Item 5 only as content the synthesis reports with cites; routing and indexing them is out of scope here (Item 6 owns the log). Spec amended: Problem (two senses of "gap"), Known Requirements, Non-Goals; open question removed.
- Gate: CLEAR (F1 fixed, F2 disposed by owner, F3 fixed).

## audit — 2026-08-20 — rev a27e882c

Point (re-derived): A fresh administrator must recover the study framing, LCOE result, named constraint outcomes, and evidence-backed findings from the committed record alone; anything missing stays explicit rather than being imported or inferred.   [source: `.project/concepts/run-study-skill.md` Owner’s Words (roles) + Success Criterion 4, grade: owner]
Falsifier: A fresh administrator given only a template-conforming record cannot recover a required fact or must consult an external file to understand the evidence behind it.
Findings:
- audit-F1 [DO] The G1 amendment records the oracle’s `tool-source-digest/v1` as only `{recipe, digest}`, omitting the named `files[]` that defines what this digest covers; the emitted digest contract and its tests require `{recipe, digest, files}`, so a template-conforming record cannot tell a cold reader which oracle sources were pinned. The same hand-written truncation exists under `tools[].source_digest`, and all 273 tests pass because none checks the template against the emitted shape. Concrete falsifier: fill `snapshot.json` exactly from `record-template.md`, then ask an administrator which files the oracle digest covers without leaving the record; the record cannot answer. — `.project/concepts/run-study-skill-design.md` “The study record” and Required Invariants (agent/ratified) — disposition: DISPOSE-and-proceed; before Item 6, carry the full `{recipe, digest, files[]}` shape in both template locations and add a contract check against the emitted shape.
Smells: **1. Two representations must be manually kept synchronized** fired; the hand-written snapshot digest shape has diverged from the producer/test contract and is the basis of audit-F1. Smells 3, 4, 5, and 6 did not fire.
Gate: BLOCKED (spec-F1, spec-F2)

## audit — 2026-08-20 — rev owner walkthrough 1

Point (re-derived): A fresh administrator must recover the study framing, LCOE result, named constraint outcomes, and evidence-backed findings from the committed record alone; anything missing stays explicit rather than being imported or inferred.   [source: `.project/concepts/run-study-skill.md` Owner’s Words (roles) + Success Criterion 4, grade: owner]
Falsifier: A fresh administrator given only the committed record cannot recover a required study fact without outside study evidence.
Findings: None.
Resolves:
- audit-F1: DEFERRED — authority: owner — basis: the oracle's role in a general study is conceptually unsettled; G1 is non-load-bearing for this cold-pickup exercise, so its exact fingerprint shape is a future Align question rather than an Item 5 certification blocker. This also disposes the associated smell for Item 5.
Gate: BLOCKED (spec-F1, spec-F2)

## audit — 2026-08-20 — rev owner walkthrough 2

Point (re-derived): A cold administrator uses only committed study evidence, keeps recorded facts, missing facts, and labeled interpretation distinct, and exposes any contract gaps before the first compliant study. [source: `.project/concepts/run-study-skill.md`, grade: owner]
Falsifier: The synthesis imports or reconstructs missing evidence, or a fact needed to recover framing, LCOE, named constraint outcomes, or findings remains absent from the contract without a recorded disposition.
Findings: None.
Smells: None unresolved; smell 1 was disposed with `audit-F1` in the prior owner-authorized resolution.
Resolves:
- `spec-F1`: FIXED — authority: owner — basis: spec Success Criterion 4 now requires a disposition for every gap, and `gaps.md` records dispositions for G1 and G2.
- `spec-F2`: DEFERRED — authority: owner — basis: Item 5 tests the record contract and does not own discovery-log creation or model-finding routing; Item 6 owns that log.
Gate: CLEAR
