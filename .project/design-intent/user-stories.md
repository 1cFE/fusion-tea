# User Stories

## Use Case 1: Agentic Model Development Management

The primary interface for domain engineers to participate in model development without needing SysML expertise.

### Viewing Model State

**US-1.1** As a domain engineer, I want to see the current model structure as a diagram so that I can understand what has been built without reading SysML code.

**US-1.2** As a domain engineer, I want to see structural/composition relationships (what contains what) so that I understand the part hierarchy of the fusion plant.

**US-1.3** As a domain engineer, I want to see functional/physics relationships (what connects to what, what flows where) so that I understand how subsystems interact.

**US-1.4** As a domain engineer, I want to see cost rollup relationships so that I understand how component costs aggregate to system costs.

**US-1.5** As a domain engineer, I want to toggle between different view types (structural, functional, cost) so that I can focus on what's relevant to my current question.

**US-1.6** As a domain engineer, I want to see layers/overlays on a single diagram so that I can understand multiple aspects simultaneously when helpful.

### Agent Interaction

**US-1.7** As a domain engineer, I want to ask the agent questions in natural language so that I don't need to learn specialized query syntax.

**US-1.8** As a domain engineer, I want to initiate model changes through the agent (e.g., "add a backup cooling system") so that I can contribute to model development without writing SysML.

**US-1.9** As a domain engineer, I want to see the agent's progress as it works on a task so that I know what's happening and can redirect if needed.

**US-1.10** As a domain engineer, I want the diagram to automatically update when the agent commits changes so that I always see the current state.

**US-1.11** As a model developer, I want to see agent actions in real-time so that I can monitor and debug the development process.

### Exploration

**US-1.12** As a domain engineer, I want to ask "what-if" questions (e.g., "what happens to LCOE if we increase blanket thickness?") so that I can explore design trade-offs.

**US-1.13** As a domain engineer, I want to compare two design variants side-by-side so that I can understand the differences.

---

## Use Case 2: Agent-Assisted Visualization

The agent modifies the diagram dynamically to help answer user questions.

### Dynamic View Modification

**US-2.1** As a domain engineer, I want to ask a question and have the diagram zoom to the relevant subsystem so that I can see the context for the answer.

**US-2.2** As a domain engineer, I want the agent to highlight specific relationships when answering questions so that I can see what it's referring to.

**US-2.3** As a domain engineer, I want the agent to show/hide layers based on my question so that irrelevant information doesn't clutter the view.

**US-2.4** As a domain engineer, I want the agent to annotate the diagram with explanatory text so that I understand what I'm looking at.

### Narrated Changes

**US-2.5** As a domain engineer, I want the agent to explain what it's highlighting and why so that I learn the model structure over time.

**US-2.6** As a domain engineer, I want to see a brief summary of view changes so that I understand what the agent did.

**US-2.7** As a domain engineer, I want to ask follow-up questions that build on the current view so that exploration feels like a conversation.

### View History

**US-2.8** As a domain engineer, I want to undo/redo view changes so that I can go back to a previous perspective.

**US-2.9** As a domain engineer, I want to save a particular view configuration so that I can return to it later.

---

## Use Case 3: Export Generation

Generate artifacts for communication with broader audiences.

### Static Exports

**US-3.1** As a domain engineer, I want to export the current view as a PNG/SVG image so that I can include it in presentations.

**US-3.2** As a domain engineer, I want to export at publication quality (high resolution, clean styling) so that figures look professional.

**US-3.3** As a domain engineer, I want to export with or without annotations so that I can choose the right level of detail.

### Interactive Exports

**US-3.4** As a domain engineer, I want to export an interactive HTML file so that stakeholders can explore the model without special software.

**US-3.5** As a domain engineer, I want the interactive export to support basic navigation (zoom, pan, expand/collapse) so that stakeholders can explore on their own.

**US-3.6** As a domain engineer, I want the interactive export to include tooltips with key data so that stakeholders can see details on hover.

**US-3.7** As a stakeholder, I want to view interactive exports in a web browser without installing anything so that I can easily access shared models.

### Export Configuration

**US-3.8** As a domain engineer, I want to choose which layers/views to include in an export so that I can tailor output to the audience.

**US-3.9** As a domain engineer, I want to add a title and description to exports so that context is preserved.

**US-3.10** As a domain engineer, I want to save export presets so that I can quickly regenerate standard figures.

---

## Cross-Cutting Concerns

### Onboarding

**US-X.1** As a new user, I want a brief tutorial on how to interact with the interface so that I can get started quickly.

**US-X.2** As a new user, I want example questions I can ask the agent so that I understand what's possible.

### Performance

**US-X.3** As a domain engineer, I want the diagram to load within a few seconds so that exploration feels responsive.

**US-X.4** As a domain engineer, I want view changes to animate smoothly so that I can follow what's changing.

### Accessibility

**US-X.5** As a user, I want keyboard navigation support so that I can use the interface without a mouse.

**US-X.6** As a user, I want sufficient color contrast and colorblind-friendly palettes so that diagrams are readable.
