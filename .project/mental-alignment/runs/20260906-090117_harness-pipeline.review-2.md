# Review — 20260906-090117_harness-pipeline.md

artifact: /home/reid/1cfe/fusion-tea/.project/mental-alignment/runs/20260906-090117_harness-pipeline.md
question: |
  I want you to RESUME the $my-mental-model for .project/mental-alignment/runs/20260905-135058_harness-pipeline.md

  I am not happy with the current iteration. For reference, see:
  - .project/concepts/physical-innovation-narrative.md
  - .project/research/20260905_1cfe-writing-style.md
  - .project/research/20260905_1cfe-writing-style-sources/README.md
  In addition to the usual guidance for the mental model. Start a fresh agent to fully revise the synthesis to improve the content and the writing.
reviewed against: /home/reid/.agents/skills/my-mental-model/design_synthesis.md, /home/reid/.agents/skills/my-mental-model/feedback/synthesis.md, /home/reid/1cfe/fusion-tea/.project/mental-alignment/feedback-synthesis.md

## Findings

1. The explanation still uses “the harness supports branching” as a label instead of saying what must branch and why — §2, paragraph beginning “The harness supports branching, exploration, and rapid iteration.” An engineer needs to hear that an agent makes a candidate change to a textual plant model on a branch so it can test the field-to-heating relationship without overwriting the reviewed baseline; then it can bring that exact change to review. “Supports” gives an abstraction the verb, and “branching, exploration, and rapid iteration” is an unconnected inventory. This is the owner’s explicit complaint, and it violates the requirement to give the verb to the actor and explain important structure through its reason. (cites: shared feedback, “Abstraction performing a verb”; design_synthesis.md rules 4 and 6)

2. Section 2’s heading, “Adding the missing physics,” is a generic activity heading. Its concrete finding is that the stellarator model charged for a stronger magnet without modeling the field’s effect on plasma confinement. Put that fact in the heading. The present heading could sit above almost any model revision. (cites: shared feedback, “Heading that names what is present”; design_synthesis.md rules 2 and 3)

3. The central code-generation explanation names the translation steps but never gives the reader the decision that produced them — §3, paragraphs 1–2. It needs the causal chain the feedback asks for: engineers revise a hardware model in SysML; a study must sweep design inputs through an executable calculator; therefore the project generates a standalone Python package. Then explain the real boundary: ordinary SysML expressions can be translated, while the required-heating numerical solver stays in maintained Python with its SysML inputs, outputs, and equation documentation. As written, “translates … and wires its calculations together” is an implementation inventory, not a reason to understand the split. (cites: shared feedback, “Structure presented as an inventory”; design_synthesis.md rules 5–7)

4. “A study repeats this evaluation across selected inputs” (§3) flattens the important distinction between changing a candidate design and changing the model itself. State it directly: within one study, magnetic field, density, and installed heating vary while the checked package version fixes the equations; changing an equation or adding a missing relationship is a separate model revision that must be reviewed before a new study. The next paragraph partly implies this through version pinning, but it makes the reader reconstruct the point. (cites: design_synthesis.md rules 3, 6, and 8; shared feedback, “Structure presented as an inventory”)

5. Section 3’s heading, “Running the plant calculations,” describes an activity rather than the consequence that makes the section matter. A reader should get the section’s point from the heading: a reported electricity cost is insufficient when the same design fails the installed-heating or conductor limit. The section itself says this in paragraph 3. (cites: shared feedback, “Heading that names what is present”; design_synthesis.md rules 2 and 3)

6. Section 4 repeatedly makes records and commands act in place of the people and files involved: “The records make this reasoning available,” “The goal file preserves,” and “It gives an agent the instructions” in the dropdown. Name the concrete handoff: an agent writes the goal, task trail, evidence links, and conclusion to files; the next agent reads those files and checks the linked artifact. The owner has specifically rejected this Claude-ish abstraction pattern. (cites: shared feedback, “Abstraction performing a verb”; design_synthesis.md rule 4)

7. The historical example ends its consequence in vague work language — §5, “The owner directed follow-up work toward both.” “Both” forces the reader to recover two different investigations from the preceding sentences, and “follow-up work” says no more than “that work.” Name the actions: investigate how much additional conductor field capability is needed, and compare that change against a larger installed heating system and its recirculating electricity cost. (cites: shared feedback, “Count standing in for the members” and “Abstraction performing a verb”; design_synthesis.md rules 1, 3, and 4)

8. Several sentences preserve an agent’s vague category where concrete nouns are already available: “those connections form a model” (§1), “the relevant workflow and tools” (§4), and “what came back” (§4). Replace each with the named components or evidence at that point: component equations and limits; the research/modeling/study workflow; and a source finding, reviewed model change, or study verdict. This is a document-wide sweep, not a line edit, because the owner’s feedback says this voice is “riddled” through a draft when it appears. (cites: shared feedback, “Abstraction performing a verb”; project-local feedback, 2026-08-23; design_synthesis.md rules 1 and 4)
