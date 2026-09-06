# Review notes — 20260905-135058_harness-pipeline.md

artifact: /home/reid/1cfe/fusion-tea/.project/mental-alignment/runs/20260905-135058_harness-pipeline.md
question:
```text
See .project/concepts/physical-innovation-narrative.md

I need you to build out a $my-mental-model to help capture **what the harness and pipeline is** at the high level. Scope: the different descrete tools, scripts, and "agents" (commands) that form our capabilities.

I can imagine a few views to help explain this:
- Structurally:
  - Identifying what each component IS, and where it lives. A lightweight breakdown structure across agentic-mbse, fusion-tea, sysml-codegen, teax
- Behaviorally: how do these components interact. starting at the highest level ("run-goal") down to the smaller stuff (scripts to help run the harness for work tracking)
  - It would be great to all get a feel for "agents invoking agents". e.g. is there a way to visualize that?
- A worked example. E.g. following work/narratives/20260904-184254Z-operating-point-closure.md which had multiple "rounds", modified the models, run studies
```
reviewed against: /home/reid/.agents/skills/my-mental-model/design_synthesis.md, /home/reid/.agents/skills/my-mental-model/feedback/synthesis.md, /home/reid/1cfe/fusion-tea/.project/mental-alignment/feedback-synthesis.md

## Things to reconsider

1. Define or replace workflow terms before they appear in the TLDR. “Round agent,” “native workflow,” “fresh review,” “promoted package version,” “integration pin,” and “administrator” all carry system-specific meaning before the body explains some of them. The TLDR must stand alone for a reader who has seen none of the sources. — TLDR, especially bullets 1, 3, and 4 (cites: Design Synthesis § TLDR; Rules 1, 4, and 5)

2. Name the helper-agent definitions and the command-to-helper edges that the proposed session diagram will draw. The artifact says modeling commands “can request helper agents” and groups the definitions as “SysML, KerML, Syside, validation, and debugging helpers,” but the owner explicitly asked to understand agents invoking agents. Generic categories leave the render agent without concrete nodes or invocation paths. — §§ 2–3 (cites: Design Synthesis § Narrative body, “Narrative logic is clear”; Rule 6, “Name the members”; owner’s behavioral-view request)

3. Replace the meta opening in the repository section with the organizing principle itself. “The structural view should group components…” describes how the document should present the answer, while the next sentences contain the answer. — § 2, opening paragraph (cites: Design Synthesis Rules 3, 5, and 6; Shared feedback, “Document as its own subject”)

4. Make the 110 MW measurement self-contained. In “At 110 MW it contains feasible points,” the antecedent of “it” could be the grid, the reviewed study, or the studied window, and the sentence does not say how many of the nine total feasible points belong to 110 MW. — § 5, Measurement paragraph (cites: Design Synthesis Rules 1 and 9; Shared feedback, “Clause the reader already has” does not justify relying on earlier context for the missing subject)

5. Rewrite “The important feedback was both architectural and physical” as the two concrete findings already stated after the colon. The abstract classification adds a decoding step and repeats what the rest of the sentence says plainly. — § 5, paragraph after Measurement (cites: Design Synthesis Rules 1 and 3; Shared feedback, “Abstraction performing a verb” and “Clause the reader already has”)

## Techniques worth considering

6. Put a compact vocabulary key immediately before the interaction table: session/agent, command or skill, specialist-agent definition, deterministic script, and stored artifact. The artifact defines three of these in prose, but the structural and behavioral views repeatedly distinguish all five. A small comparison would let the reader decode the later arrows once. — § 3, before the relationship table (cites: Design Synthesis Rules 6 and 11)

7. Turn the requested adversarial pass into concrete challenges in Judgment before render rather than leaving it only as a suggestion to commission another reviewer. The project feedback asks for a skeptical-domain-expert review with FAIR / UNFAIR-BUT-EXPECTED / DEFUSED verdicts and approved findings folded into a correction pass. — Judgment, Suggested spot checks (cites: Project-local feedback, 2026-08-23 adversarial review entry)
