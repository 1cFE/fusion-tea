# Prompt for turning a write-up into its HTML page

Use this prompt to convert a settled markdown support in this directory into its HTML page. It adapts the render, review and inspection stages of the `_my_mental_model_v2` skill (`~/.claude/skills/_my_mental_model_v2/`). In that skill a synthesis agent wrote the explanation and the HTML writer expanded it. Here the owner has already settled each support's story and prose through [writing-prompt.md](writing-prompt.md), so the markdown is the approved explanation, and the page's job is the reading experience and the visual layer.

*(Drafted 2026-09-26 by an agent from `_my_mental_model_v2` at the owner's request; not yet reviewed by the owner.)*

You are the coordinator. You dispatch two agents:

- A **render writer** writes the page plan and the page, and is the only agent that revises them. Its prompt is [html-render-prompt.md](html-render-prompt.md).
- A **reviewer** checks one version of the page. A fresh one runs for every version. Its prompt is [html-review-prompt.md](html-review-prompt.md).

You judge every version, inspect the page in a browser, and talk to the owner. You never write or edit the page, the page plan or the markdown.

Before you start, `docs/write-up/write-up.css` must exist and the owner must have approved it. If it does not, stop and tell the owner.

## Files

| What | Path |
|---|---|
| Source markdown | `docs/write-up/<stem>.md` |
| Page | `docs/write-up/<stem>.html`, beside its markdown so relative figure and evidence links keep working. The Stellaris support is the exception; see the render prompt. |
| Shared stylesheet | `docs/write-up/write-up.css`, approved by the owner before any conversion and linked by every page |
| Page plan | `docs/write-up/html-work/<stem>.page-plan.md` |
| Reviews | `docs/write-up/html-work/<stem>.review.md`, then `<stem>.review-2.md`, `-3`, and so on. Never overwrite a review. |
| Project-local HTML feedback | `docs/write-up/html-feedback.md`. Append-only; entries are written only when the owner asks. |
| Shared feedback (reviewer only) | `~/.claude/skills/_my_mental_model_v2/feedback/html.md` and `~/.claude/skills/_my_mental_model_v2/feedback/synthesis.md` |

## Your standard

You own the quality of everything this conversion shows the owner. Infer their standard from these prompts, [writing-prompt.md](writing-prompt.md), [plan.md](plan.md), their request, and every correction they make during the run.

Read every version of the page as its intended reader: a technical reader who followed a link from the main post and has never seen this repository. A ready page says exactly what the markdown says, is easier to read than the markdown, and every addition earns its place. Reject a page that restyles the markdown where a visual was needed, hides the main story in disclosures, adds visuals that repeat the prose, or lets evidence crowd out the explanation.

Reviewer findings are evidence, not a verdict; a clean review never grants a pass. Advance only when your own reading says the page is ready. Do not lower the bar because of attempt count. If the workflow cannot clear the bar, report the failure and the remaining gap instead of presenting a below-bar page.

## Step 1: Start the render writer

<!-- harness-block: writer-spawn -->
Use the `Agent` tool with no `subagent_type`. Name it `render-<stem>` and record the returned handle. The name is not the handle.
<!-- /harness-block -->

Give it this resolved brief, plus any owner instruction about the page in their words:

```
source:         <absolute path of the markdown>
page:           <absolute path of the HTML>
page plan:      <absolute path of the page plan>
stylesheet:     <absolute path of write-up.css>
read:           docs/write-up/html-render-prompt.md
                docs/write-up/writing-prompt.md
                docs/write-up/plan.md (this support's row and section)
                docs/write-up/html-feedback.md (if present)
first task:     write the page plan only, then stop and report its path
```

## Step 2: Approve the page plan

Read the page plan. Check that it keeps the prose, that each proposed addition has a clear job and a source, and that it carries plan.md's open questions for this support. If it falls short, send one brief to the writer as in Step 4 and read the revision.

Present the ready page plan to the owner in full, with its questions and any proposed prose changes, and wait. Send the writer the owner's approval and every correction in their words, and ask it to render the page.

<!-- harness-block: correction-dispatch -->
Send every message to the writer with `SendMessage`, addressed to the handle you recorded at spawn.
<!-- /harness-block -->

## Step 3: Run a fresh review

Use this step for every version of the page. Choose the next review path. Start a fresh reviewer with only this resolved brief:

```
page:                   <absolute path of the HTML>
stylesheet:             <absolute path of write-up.css>
source markdown:        <absolute path>
page plan:              <absolute path>
writer prompt:          docs/write-up/html-render-prompt.md
your instructions:      docs/write-up/html-review-prompt.md
voice:                  docs/write-up/writing-prompt.md
shared feedback:        ~/.claude/skills/_my_mental_model_v2/feedback/html.md
                        ~/.claude/skills/_my_mental_model_v2/feedback/synthesis.md
project-local feedback: docs/write-up/html-feedback.md (if absent, say "none for this project")
review output path:     <absolute review path>
```

Give it no conversation, owner context or other project sources.

<!-- harness-block: reviewer-spawn -->
Use the `Agent` tool with no `subagent_type`, and `model: "sonnet"`. Name it `review-<stem>`. The reviewer is fresh every time and never a fork.
<!-- /harness-block -->

Confirm that the review file exists. If the review fails, continue to your judgment and note the failed attempt; a failed review neither grants nor denies a pass.

## Step 4: Judge, inspect and revise

Read the source markdown, the page source and the review. Judge the page against the markdown, the render prompt and the approved page plan, with the review as evidence. Then inspect the rendered page yourself with the `browser-inspect` skill:

- Every figure, diagram, table and code block, at desktop width and at phone width: overlap, clipping, missing content, unreadable labels, horizontal overflow.
- Every disclosure, opened.
- The JSON sidecar: console errors and failed loads.
- Links: every in-page link lands on its target, and every relative link resolves to a file, apart from links to supports not yet converted. Check the relative links with a script, not by eye.

If the page is below the bar, write one coherent brief about the whole page. State the outcome the next version must achieve and reference the current review. Send it to the writer, the only agent that may edit the page. Carry any owner correction in their words, and treat it as evidence about their expectations for the whole page and every later judgment in the run. Then return to Step 3 with a fresh reviewer and the next review path. There is no fixed attempt limit. If the writer cannot be reached or stops improving before the page clears the bar, report the failure and the remaining gap, then stop.

Do not present the page until your judgment and the browser inspection both pass. If you cannot inspect it, say so and do not claim it passed.

## Step 5: Present and carry corrections

Present the page path, how to open it, one line per main section on what the page adds, any proposed prose changes and source issues the writer reported, and your remaining concerns.

Owner corrections go to one of two places:

- **Presentation** (layout, visuals, disclosures, navigation): carry their words to the writer and repeat Steps 3 and 4.
- **Prose**: the markdown is the source of truth, so the fix lands in the markdown first, made with the owner through [writing-prompt.md](writing-prompt.md). Then the writer carries it into the page, and Steps 3 and 4 repeat. This keeps the two from drifting.

When the owner accepts the page, update the support's status in plan.md.

## Step 6: Record feedback on request

Offer to record HTML feedback after presenting. Record only what the owner asks to persist, in `docs/write-up/html-feedback.md`. On first write, add a two-line header naming the file and saying entries are append-only. Use this shape, keeping the owner's words verbatim and naming the pattern yourself without turning it into a new rule:

```
## <short pattern name>
Avoid. | Prefer. <one-line direction>
- Bad: `<page instance>`
- Good: `<the owner's corrected form, or say none was given>`
- From: <YYYY-MM-DD>, <stem>.html
```

Promote an entry into these prompts, or into the shared `_my_mental_model_v2` feedback, only when the owner asks. Delete the local entry once it is promoted.
