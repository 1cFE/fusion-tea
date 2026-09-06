# Review — 20260905-142327_harness-pipeline.md

artifact: /home/reid/1cfe/fusion-tea/.project/mental-alignment/runs/20260905-142327_harness-pipeline.md
question: I want you to RESUME the $my-mental-model for .project/mental-alignment/runs/20260905-135058_harness-pipeline.md

I am not happy with the current iteration. For reference, see:
- .project/concepts/physical-innovation-narrative.md
- .project/research/20260905_1cfe-writing-style.md
- .project/research/20260905_1cfe-writing-style-sources/README.md
In addition to the usual guidance for the mental model. Start a fresh agent to fully revise the synthesis to improve the content and the writing.
reviewed against: /home/reid/.agents/skills/my-mental-model/design_synthesis.md, /home/reid/.agents/skills/my-mental-model/feedback/synthesis.md, /home/reid/1cfe/fusion-tea/.project/mental-alignment/feedback-synthesis.md

## Findings

1. The TLDR stops being self-contained in its third bullet. It introduces four repository names and “executable packages” before explaining any of them, so a reader with none of the sources learns an ownership inventory instead of the plain mechanism. Rewrite this bullet around the necessary separation between engineering description, translation, and repeated calculation; introduce repository names later as examples of who performs those jobs. — lines 38–42, especially line 40 (cites: Design Synthesis, TLDR: “Use no loaded terms. Use no term you have not already given the reader”; shared feedback, “Structure presented as an inventory”)

2. The document repeatedly gives abstractions human actions, which recreates the writing pattern the shared feedback explicitly says to sweep from the whole artifact. Examples include “it also asks more of the conductor,” “A physical model adds a separate question,” “The engineering relationship now participates,” “The next session needs the reasoning,” and “the current constraint … shows the comparison.” Give each action to the engineer, agent, calculation, or physical quantity that actually performs it. — lines 48, 52, 66, 80, and 92 (cites: shared feedback, “Abstraction performing a verb”; Design Synthesis rules 1 and 4)

3. Inline provenance regularly makes otherwise clear claims hard to read once. The nested labels and citations at the ends of paragraphs often contain several authorities, aliases, section symbols, and interpretations in one bracket, such as the annotations after the harness purpose, software-to-systems boundary, executable construction, and worked-example setup. Preserve the required provenance, but move it into short standalone provenance lines or split mixed authorities into separate statements so the narrative sentence remains plain. — lines 50, 52, 64, 88, 90, 92, 94, 98, and 100 (cites: Design Synthesis, opening first-read test; narrative requirement to note provenance; rules 1 and 4)

4. Many source pointers do not provide a line range even though the narrative standard requires a follow-up location with “file path, section, line range.” References such as “opening,” “§ Data Flow,” “§ Project Structure,” and several goal/runbook section names leave the reader or render agent to search long files. Add line ranges to the referenced definitions and claims, retaining section names where they help orientation. — lines 50, 54, 60, 62, 68, 74–80, 88–100, and 121–139 (cites: Design Synthesis, narrative body requirement to point to “file path, section, line range”)

5. The first section introduces `1costingFE` and `ARIES-CS` without defining either, and neither term carries the later explanation. This interrupts the motivating thread with project-internal vocabulary and leaves a new reader unable to tell what comparison is proposed. Explain each in plain words and connect it directly to the decision-quality goal, or remove the paragraph from the skeleton and leave it for the render’s detail layer. — line 54 (cites: Design Synthesis rules 1 and 4; “The same words the HTML will use”; shared feedback, “Material that maps to no item in the owner's outline”)
