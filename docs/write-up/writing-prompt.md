# Prompt for writing and revising technical explainers

Use this prompt when helping revise the public write-ups in this directory. It captures the owner's writing preferences established while revising `sysml-codegen-model-evaluation.md`. The instructions below paraphrase owner-stated preferences and agent recommendations explicitly accepted during that session. They are guidance for explaining the intended argument, not a substitute for understanding it.

## Understand the story before editing

Read the article and any relevant handoff. State the intended story in plain language before proposing substantial changes. Establish what the reader should understand, why they should care, and how the technology serves that purpose. Preserve that argument while improving the prose.

For the model-evaluation article, the purpose is rapid engineering iteration and trade studies. Numerical parameters, categorical component or material choices, and plant architecture require different mechanisms for representing and evaluating alternatives. Codegen and TEAx turn those choices into performance, cost, and engineering-check results that inform the next design decision. Reuse supports that purpose; it is not the whole story.

## Work one section at a time

When asked to review a section, read its current text and assess how it advances the intended story. Identify what already works, where the explanation loses the reader, and what should change. Explain the reason for each substantive recommendation. Offer short sample passages when they make the proposed direction concrete.

When the owner asks you to apply the recommendations, edit the section in the article so they can read it in context. Keep the scope to the agreed changes and any explicitly agreed relocation of supporting detail. Do not use feedback on one section as a reason to rewrite the whole article.

## Establish the problem before the example

Begin a technical section with a brief, general statement of the problem or step it addresses. Explain why that step is needed, then introduce the example that demonstrates it. An operation on a specific component is not enough context by itself.

For example, the accepted opening to the component-modeling section is:

> We begin by defining a component’s calculations and connecting their inputs and outputs to the plant model.

The magnet example follows that scope sentence. Similarly, the component-selection section first explains why varying numerical inputs cannot explore behavior absent from the current component model, then introduces the blanket's more detailed breeding calculation.

These are examples of the explanation pattern, not required wording. Titles should identify the engineering purpose or technical subject. “Exploring the design space: parameters, components, and architecture” gives useful context; “What do we want to change?” does not.

## Develop the causal explanation

Give each paragraph one point, and make its sentences develop that point. Short sentences alone do not create clarity. The reader should understand why one fact leads to the next, rather than having to connect a sequence of loosely related statements.

Explain the need before naming the mechanism. Component and material choices are categorical and do not fit naturally into a numerical sweep; that motivates alternative definitions and selecting their usages. A calculation needs another calculation's result; that motivates dependencies and execution order. A study explores many input combinations; that motivates constraints for identifying engineering failures.

Use a brief forward reference when the motivation depends on material explained later. For example, tell the reader that a later study will sweep broad ranges of inputs when introducing constraints. Preserve that connection without explaining the whole study prematurely.

Introduce a physical component's role before its quantities or implementation details. Explain what the blanket does before discussing its breeding surrogate. Explain what the magnet calculation answers before introducing coil attributes.

## Show enough machinery to make the process imaginable

Explain what the program actually does. “Codegen constructs a graph” is insufficient without explaining that it identifies component occurrences, finds their calculations, and follows input connections to supplying parameters or calculated outputs.

Keep definitions and usages distinct when that distinction explains the mechanism. Follow values through a complete example: where the plant supplies them, how a calculation usage binds them to an equation, and how the result becomes available to other calculations. Do not lose one part of that chain while shortening the prose.

Introduce technical terms after explaining their meaning in ordinary language. Explain code through the decisions and behavior it expresses. In a wiring example, prioritize which calculation runs, where its inputs come from, and where its output goes. Long identifiers, wrapper types, and internal bookkeeping deserve attention only when they help the reader understand that behavior.

## Keep examples focused and evidence intact

Use one strong example to develop a point. The blanket surrogate explains the need for custom computation more directly than input checks around a simple arithmetic function. Avoid adding a second example that interrupts the main explanation without advancing it.

Introduce figures with the question they help answer. Explain their main causal chain afterward. Captions should help readers interpret marks, arrows, assumptions, and result limits; detailed verification records can live in linked evidence notes.

Keep qualifications that change what the reader may conclude. Historical study costs remain historical. Passing modeled constraints does not establish unmodeled physical feasibility. Preserve distinctions between supported sweeps, external optimization, and capabilities not yet implemented. Move secondary implementation details or complete held-input lists into linked notes when agreed, preserving their content and sources.

Do not simplify a claim into something technically different. In the magnet example, selected ampere-turns and geometry produce field. In the blanket example, selecting a richer component model demonstrates added model detail, not a demonstrated material substitution. Check the retained evidence when a proposed edit would change such a claim.

## Finish on what the reader can now do or understand

End a section by explaining what the completed step enables and how that prepares the next step. Finish the article by returning to the engineering purpose: evaluate choices, see what improves and what fails, investigate, revise the model, and study again.

Before saving, read the section as someone unfamiliar with the implementation. Can they identify the problem, follow the mechanism, and understand the result on one reading? If not, repair the explanation rather than merely cutting words.

Keep Markdown paragraphs and list items on one source line. Preserve local links, figures, and technical evidence. Report edits briefly so the owner can return to reading the article in context.
