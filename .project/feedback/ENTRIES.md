# Feedback Entries

Append-only log of agent learnings, tagged by pack target. Newest at the bottom.

The rules for writing an entry are in `README.md`, in this directory. Do not rewrite or reorder existing entries.

---

## [_my_design] 2026-09-17

**Wrong:** Silently omitted spec requirements and buried half-sentence CYA deferrals in the design.
**Right:** Ask the user explicitly before omitting any spec-required item, with context for why it might be dropped.
**Learning:** Stop and confirm before writing any artifact that intentionally skips a requirement. Never bury an omission as cover.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [_my_implement] 2026-09-17

**Wrong:** Bare `git commit` after `git add` swept owner-staged files into a work item commit.
**Right:** Always `git commit -m ... -- <paths>` with explicit pathspec; verify with `git show --stat HEAD`.
**Learning:** The owner keeps their own files staged; a bare commit sweeps them in. Always commit with an explicit pathspec.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [_my_spec] 2026-09-17

**Wrong:** Treated a brief directive ("match the xlsx") as authoritative and propagated a bad inference through spec→design without checking the actual data.
**Right:** When a brief directive creates friction with actual constraints, stop and ask a one-line confirmation before committing.
**Learning:** Pre-flight check every brief directive against actual file/data state before propagating it through artifacts.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [_my_status] 2026-09-17

**Wrong:** Rolling handoffs carried item details but dropped the governing concept doc; assessed progress against the wrong epic.
**Right:** Before answering progress or next-work questions, locate and read the governing concept doc.
**Learning:** Every handoff and status assessment must name and read its governing artifact. Rolling handoffs lose the frame.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [html-explainer] 2026-09-17

**Wrong:** Proposed "the record is the product" as the core insight for an explainer.
**Right:** Lead with the demonstrated capability and its results; process/record mechanics are subordinate credibility detail.
**Learning:** The demonstrated capability is the story. Machinery that makes it credible is a supporting layer, never the thesis.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [_my_spec] 2026-09-17

**Wrong:** Overwrote an implemented v1 design.md with new work for the same feature area.
**Right:** Always create a new directory for new work items; append addenda to implemented specs, never overwrite them.
**Learning:** Existing specs are immutable history. New work gets a new directory even if it touches the same code.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [_my_design] 2026-09-17

**Wrong:** Invented family-average lookups, default rows, and coverage-extending heuristics for missing input data.
**Right:** Skip the concept or zero the value when input is missing; the user fixes missing data themselves.
**Learning:** Never paper over data gaps with fallbacks. The owner manages data completeness, not the agent.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [markdown-formatting] 2026-09-17

**Wrong:** Inserted hard line breaks at ~80 characters in markdown prose.
**Right:** One paragraph = one line. Match existing file convention; default to unwrapped.
**Learning:** Hard-wrapping buys nothing and makes diffs noisy. Let the editor soft-wrap.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [_my_close] 2026-09-17

**Wrong:** Repeatedly listed "merge and push" as an open owner-held item in summaries and handoffs.
**Right:** Do not mention merging the working branch. The branch is the working branch; merge is not a pending decision.
**Learning:** Never list merge as an open or owner-held item unless the owner explicitly asks about it.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [_my_implement] 2026-09-17

**Wrong:** Used the AskUserQuestion tool for questions that needed nuanced answers.
**Right:** NEVER use the AskUserQuestion tool — blanket prohibition, no exceptions. Ask in plain prose always.
**Learning:** The chip/radio format is reductive. The user hates it categorically. Always ask in flowing text.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [run-goal] 2026-09-17

**Wrong:** Treated agent-grade scope notes as owner rulings and let them gate work.
**Right:** Check origin and provenance of any ruling before citing it as a gate. Agent notes must never harden into owner rulings.
**Learning:** Nothing is sacred — question recorded rulings. Ask when a fence looks load-bearing but has no owner provenance.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [_my_implement] 2026-09-17

**Wrong:** Jumped to code fixes without discussing diagnosis first.
**Right:** Explain evidence and reasoning, then wait for direction before writing any code.
**Learning:** Diagnose and explain before writing. Don't write code until explicitly asked.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [working-voice] 2026-09-17

**Wrong:** Dense jargon, structural framing, narrative dressing, clever-sounding prose.
**Right:** Short direct sentences, concrete nouns, define terms on first use, verify against code before explaining.
**Learning:** Ornate writing erodes trust. Plain language signals real understanding. Say the thing simply.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [_my_spec] 2026-09-17

**Wrong:** Asked design-level questions (mechanism, thresholds, placement) during spec scoping.
**Right:** Spec captures what-and-why; defer how-and-where to design. Test: "if I answered this with a reasonable default, would the spec change?" No → defer.
**Learning:** Don't pull design decisions forward into spec scoping. The boundary keeps each stage's concerns clean.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [_my_implement] 2026-09-17

**Wrong:** Unit tests with mocks passed while 22 bugs existed at module boundaries.
**Right:** Integration seam tests that cover failure chains end-to-end. Mock only at process boundary.
**Learning:** Test what happens when wrong data flows through module boundaries, not isolated happy paths.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [_my_design] 2026-09-17

**Wrong:** Formalized a workaround for a platform bug into a draft policy.
**Right:** Re-derive inherited "known hazards" against current artifacts; surface as a defect if a workaround maintains an invariant the platform declares.
**Learning:** Workaround smell = bug. Stop and flag as a defect; never formalize a workaround into a pattern.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [_my_implement] 2026-09-17

**Wrong:** Used `.claude/worktrees/` default path for git worktrees.
**Right:** `git worktree add ../{repo}-{name}` as a sibling directory parallel to the repo.
**Learning:** Sibling path is discoverable and conventional; `.claude/worktrees/` is buried and non-standard for this project.
**Source:** migrated from the native memory store, triaged 2026-09-17.
