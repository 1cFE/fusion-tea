# Spec: Goal Narrative Snapshots

**Status:** Implementation Complete — Pending Audit
**Owner:** Reid W
**Created:** 2026-09-04T10:25:24-07:00
**Complexity:** LOW
**Branch:** feat/demo-maturation

---

## Problem

The goal layer is an authoritative operating record whose three contract files cite native evidence rather than retelling it. A human-facing engineering narrative has a different job: it restates the evidence in plain language, selects the causal story, and identifies useful visuals. Keeping that derived account inside a goal directory makes it look authoritative and gives one directory conflicting mutability and citation rules.

The owner needs these narratives to be optional but easy to invoke, stored outside orchestration, and repeatable at meaningful milestones. A later narrative must sit beside an earlier one so a reader can see how the engineering story changed after another round instead of mistaking a rewritten living summary for the historical account.

The three worked examples establish the quality bar as well as the content scope. They are short, sectioned, conclusion-led, source-linked accounts with an at-a-glance summary, a causal visual, compact quantitative tables where useful, explicit limits, and a visual evidence index. The wall-and-heating example also demonstrated the failure this work must contain: its living status prose fell behind the authoritative trail during the same session.

## Success Criteria

- [x] A user can explicitly invoke a separate narrative skill for a goal without entering or changing `/run-goal`, and the invocation creates one new timestamped Markdown file outside `work/orchestration/`.
- [x] Two normal invocations for the same goal produce two chronologically sortable files; the first remains unchanged and neither invocation overwrites an existing file.
- [x] A generated narrative follows the worked example's eight-section scope, is easy to skim, contains no large prose blocks, uses helpful visuals, and is fewer than 250 lines in full.
- [x] Every narrative uses the worked examples' `Goal status`, `Narrative cutoff`, and `Review status` metadata, labels any dirty-source snapshot provisional, preserves mixed source-review states, and states its non-authoritative status clearly enough that a reader cannot mistake it for goal state or a review verdict.
- [x] Every narrative makes goal-level closure explicit; a closed goal shows the authoritative close date and either an explicit close time or a clearly labeled rough Git commit-time proxy.
- [x] Quantitative and decision-bearing claims resolve to authoritative evidence at the declared cutoff, and all local links resolve from the narrative's new location.
- [x] The three existing drafts are represented as timestamped snapshots outside the goal directories, the stale wall account is regenerated from a coherent cutoff, and live references to the deleted `SUMMARY.md` are repaired.
- [x] Focused checks protect the objective contract: separation, filename/no-overwrite behavior, required headings, paragraph and file limits, metadata and authority warning, at least one purposeful visual, and valid source links; the skill's author checklist covers interpretive quality that cannot be judged mechanically.

## Known Requirements

- **[NEED] NAR-01 — Separate and optional:** Human-facing goal narratives are produced by a separate, user-invocable skill and live outside `work/orchestration/`; no goal or round requires one. Source: `.project/concepts/goal-narrative-snapshots.md` § Owner's Words and § Next-Stage Handoff.
- **[NEED] NAR-02 — Discoverable:** The capability is not hidden; a user asking to narrate or summarize a goal can discover and explicitly invoke the narrative skill. Source: owner statement captured in `.project/concepts/goal-narrative-snapshots.md` § Owner's Words.
- **[NEED] NAR-03 — Chronological filenames:** Every output uses `YYYYMMDD-HHMMSSZ-<canonical-goal-slug>.md`, with the timestamp in UTC, so ordinary filename sorting exposes chronology. Source: owner statement captured in `.project/concepts/goal-narrative-snapshots.md` § Owner's Words; exact grammar and timezone are the minimal implementation choice resolved during specification.
- **[NEED] NAR-04 — Repeatable snapshots:** Running the narrator again for the same goal creates another file rather than replacing the earlier narrative. Round 1 and round 2 are examples of useful cutoffs, not the only allowed cutoffs. If the exact target already exists, creation fails visibly rather than overwriting or inventing another naming scheme. Source: owner statement and `[EXAMPLE]` captured in `.project/concepts/goal-narrative-snapshots.md` § Owner's Words.
- **[NEED] NAR-05 — Fixed content scope:** Every narrative uses these H2 sections in this order: `At a glance`; `Starting point and motivation`; `Story in one picture`; `Research learnings`; `Model changes`; `Study results`; `Outcome and follow-on issues`; `Evidence and visual index`. Topic-specific H3 headings remain free to state the actual conclusions. Source: owner direction “Scope: see the headers we use,” verified across the three worked examples.
- **[NEED] NAR-06 — Skimmable:** A reader can recover the starting problem, the important change, the measured outcome, and the remaining limit by scanning headings, bold-led bullets, visuals, and compact tables or lists; the narrative contains no large uninterrupted blocks of prose. Source: owner direction and the worked examples.
- **[INFERRED] NAR-07 — Prose-block ceiling:** An ordinary prose paragraph contains no more than 60 words; lists, tables, diagrams, and code or equation blocks do not count as prose paragraphs. The ceiling is derived from the worked examples, whose longest ordinary paragraph is 59 words.
- **[INFERRED] NAR-08 — Conclusion-led structure:** `At a glance` is a short set of bold-led bullets, and topic-specific H3 headings state conclusions rather than generic topics. Technical terms are defined in plain language on first use. Basis: the three worked examples.
- **[NEED] NAR-09 — Interpretive visuals:** The narrative uses a diagram, table, plot, or other compact visual wherever it makes a causal chain, sequence, constraint interaction, or repeated-field comparison easier to interpret than prose alone. Source: owner direction.
- **[INFERRED] NAR-10 — Purposeful, evidenced visuals:** `Story in one picture` contains at least one visual that carries an interpretive relationship rather than decoration. Each included visual states what it shows, stays inside the evidence, and cites its authoritative source; adjacent prose does not merely repeat it. Basis: all three worked examples.
- **[NEED] NAR-11 — Line limit:** Each complete narrative is fewer than 250 source lines, including headings, blank lines, tables, and fenced visual blocks. Source: owner direction.
- **[INFERRED] NAR-12 — Honest empty scope:** When a required section has no applicable research, model change, study, or follow-on evidence at the chosen cutoff, it states that bounded absence briefly instead of inventing content or dropping the header. Basis: fixed scope plus the goal contract's honest-empty-round rule.
- **[INFERRED] NAR-13 — One authoring contract:** The narrative skill is the sole procedural contract. Any directory README is pointer-only and does not duplicate the skill's rules. Source: `.project/concepts/goal-narrative-snapshots.md` § One authoring contract.
- **[INFERRED] NAR-14 — One-way authority:** A narrative may cite and summarize goal and native records but is never evidence, state, authorization, a review verdict, or an authoritative input cited by those records. Source: `.project/concepts/goal-narrative-snapshots.md` § Success Criteria.
- **[INFERRED] NAR-15 — Coherent source basis:** Creation starts from `goal.md`, `trail.md`, and `learnings.md` at one declared repository cutoff and follows their cited native records at that cutoff. Earlier narratives, `CURRENT_WORK.md`, summaries, and orientation prose are not evidence inputs. Source: `.project/concepts/goal-narrative-snapshots.md` § Success Criteria.
- **[OWNER] NAR-16 — Dirty sources are allowed but provisional:** Relevant uncommitted source content does not block creation. The narrative records the base commit, says that uncommitted source content was included, and labels the cutoff provisional. It does not imply that the exact source state is recoverable from Git. Source: owner decision 2026-09-04 through `my-ask-me`.
- **[INFERRED] NAR-17 — Worked-example metadata:** The header retains `Goal status`, `Narrative cutoff`, and `Review status`. `Review status` describes the review state of the summarized authoritative records; when those records have mixed review states, the narrative enumerates them in that field or labels the affected claims beside the prose. The feature adds no separate narrative-review vocabulary or lifecycle. Basis: the three worked examples, the owner preference for a simple action, and product-lens finding spec-F1.
- **[INFERRED] NAR-18 — Claim-local citations:** A quantitative or decision-bearing claim links its authoritative evidence in the same paragraph, table note, or visual caption. `Evidence and visual index` aids navigation but does not replace claim-local citations. Basis: the worked examples' citation pattern and the skimmability requirement.
- **[INFERRED] NAR-19 — Unsupported claims remain visible:** `Outcome and follow-on issues` states what the sources do not support at the cutoff; missing evidence stays missing rather than being recovered from another narrative or orientation summary. Source: the concept and `.claude/skills/run-study/runbook.md` § Administer.
- **[INFERRED] NAR-20 — No correction lifecycle:** Goal advancement always produces a new snapshot. Correcting a factual error in an existing Markdown file is an ordinary targeted edit, not a narrator mode or lifecycle. Basis: the owner's repeated-snapshot requirement and the preference for a simple action.
- **[INHERITED] NAR-21 — Goal contract unchanged:** `/run-goal`, `GOAL_RUNBOOK.md`, and the three authoritative goal-file templates acquire no narrative lifecycle, role, gate, or dependency. Source: `.project/adr/0003-lean-first-persistence.md`, `.claude/skills/run-goal/SKILL.md`, and `.project/product/0001-goal-round-native-operability.md`.
- **[INFERRED] NAR-22 — Migration timestamps are honest:** The three untracked worked examples receive their migration timestamps when placed in `work/narratives/`; their headers retain the actual evidence cutoff and do not claim an unrecoverable historical generation time. Basis: the filename describes snapshot creation, while the separate cutoff field describes source chronology.
- **[INFERRED] NAR-23 — Objective checks and human judgment stay separate:** Automated checks cover deterministic structure and boundaries. The skill requires the author to judge whether the narrative is easy to skim and whether each visual materially improves interpretation; a passing structural check is not a quality verdict. Basis: the owner-stated quality requirements.
- **[INFERRED] NAR-24 — Minimal mechanism:** The feature adds no automatic post-round dispatch, mutable `latest` pointer, narrative registry, synchronization mechanism, HTML publication step, correction mode, or narrative review gate. Source: `.project/concepts/goal-narrative-snapshots.md` § Non-Goals and the specification question pass.
- **[NEED] NAR-25 — Visible goal closure:** `Goal status` makes the goal-level closure state unmistakable. When the goal is closed, the narrative also shows the close date and rough time. A closed round, accepted learning, or reviewer recommendation is not reported as goal closure; closure requires the owner's close ruling in the authoritative trail. Source: owner request 2026-09-04.
- **[INFERRED] NAR-26 — Honest close-time proxy:** The close entry supplies the authoritative calendar date and disposition. Until the goal contract records a time, the commit that introduced the close entry supplies only a rough time, labeled `Git commit-time proxy` with its commit id. If no such commit is available, the time is reported unavailable rather than inferred. Basis: owner-ratified recommendation 2026-09-04; the stronger status contract is deferred to `.project/backlog/BACKLOG.md`.

## Non-Goals

- Changing goal grounding, task execution, checkpoint, review, learning, close, or resume behavior.
- Making a narrative authoritative or using it to certify a goal, round, study, or model.
- Automatically producing a narrative after every round or requiring one for every goal.
- Generating or publishing an HTML explainer.
- Retrofitting completed concepts, designs, audits, or product promises with narrative references.
- Building a current-state index, `latest` alias, registry, dispatcher, or synchronization system.

## Resolved Decisions

- **[INFERRED] Naming:** Use UTC `YYYYMMDD-HHMMSSZ-<canonical-goal-slug>.md`; fail visibly on an exact collision and never overwrite.
- **[OWNER] Dirty sources:** Allow them and label the snapshot provisional, including the base commit and an explicit statement that uncommitted source content was read.
- **[INFERRED] Citations:** Keep quantitative and decision-bearing citations beside the claim block they support.
- **[INFERRED] Metadata:** Keep the three worked-example fields and do not add a narrative-review lifecycle; enumerate or locally label mixed source-review states instead of flattening them.
- **[INFERRED] Migration:** Use migration time for the filename and preserve the evidence cutoff separately in the header.
- **[INFERRED] Quality checks:** Test objective rules; require author judgment for skimmability and whether visuals help.
- **[INFERRED] Closure metadata:** Treat only an owner close entry in the trail as goal closure. Show its date and disposition, and label a Git-derived rough time as a proxy rather than artifact authority.
- **[INFERRED] Process:** Skip technical design. The change is a bounded authoring skill and file migration with no new runtime architecture or cross-component interface.

---

## Related Artifacts

- **Concept:** `.project/concepts/goal-narrative-snapshots.md`
- **Worked Examples:** `work/narratives/20260904-184254Z-operating-point-closure.md`; `work/narratives/20260904-184254Z-priced-levers.md`; `work/narratives/20260904-184254Z-wall-and-heating.md`
- **Goal Contract:** `work/orchestration/GOAL_RUNBOOK.md`; `.claude/skills/run-goal/SKILL.md`; `.project/adr/0003-lean-first-persistence.md`; `.project/adr/0006-goal-evidence-seam.md`
- **Product Lens:** `.project/active/goal-narrative-snapshots/product-lens.md`

---

**Next Steps:** Run `my-audit` as a fresh certification pass, then close the item if the audit is clean.
