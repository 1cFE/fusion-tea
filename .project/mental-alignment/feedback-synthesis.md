# Project-local feedback — synthesis (mental-alignment)
Entries are appended, never rewritten; each records the owner's words verbatim about one synthesis artifact.

## 2026-08-23 — .project/mental-alignment/runs/20260823-151503_run-study-e2e-explainer.md
"this is the Claude-speak I absolutely abhor. Just say the thing, not a stupid, abstract description of the thing. did no one teach you that titles should have MEANING??"
[AGENT] Section titles must state their content — the finding, the mechanism, the number — never an abstract description of the section's function. Applies to the synthesis skeleton's titles and binds the rendered page's titles.

## 2026-08-23 — .project/mental-alignment/runs/20260823-151503_run-study-e2e-explainer.md
"I'm thinking we could benefit from a very critical review. like someone who doesn't want to just glaze our little toy project -- what would they poke at? think up a prompt, then run it through a fable subagent, and come back to me with what you learn"
[AGENT] Before render, commission an adversarial review of the synthesis by a fresh subagent with a skeptical-domain-expert persona and repo access, verdicts graded FAIR / UNFAIR-BUT-EXPECTED / DEFUSED; fold approved findings back in as a correction pass. On this run it caught overclaims (non-independent oracle, undemonstrated compositionality, inflated counts) the synthesis had inherited from its own artifacts' framing.
