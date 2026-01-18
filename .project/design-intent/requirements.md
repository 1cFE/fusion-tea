# Requirements

Requirements derived from user stories and design decisions.

## Functional Requirements

### FR-1: Model Visualization

| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| FR-1.1 | System shall render SysML v2 models as interactive diagrams | MUST | US-1.1 |
| FR-1.2 | System shall display structural/composition relationships (part containment hierarchy) | MUST | US-1.2 |
| FR-1.3 | System shall display functional/physics relationships (connections, flows, interfaces) | MUST | US-1.3 |
| FR-1.4 | System shall display cost relationships (cost rollup from components to system) | MUST | US-1.4 |
| FR-1.5 | System shall support switching between distinct view types | MUST | US-1.5 |
| FR-1.6 | System shall support overlaying multiple relationship types on one diagram | SHOULD | US-1.6 |
| FR-1.7 | System shall allow zooming and panning within diagrams | MUST | US-3.5 |
| FR-1.8 | System shall allow expanding/collapsing hierarchical nodes | MUST | US-3.5 |
| FR-1.9 | System shall display tooltips with element details on hover | SHOULD | US-3.6 |

### FR-2: Agent Interaction

| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| FR-2.1 | System shall accept natural language queries from users | MUST | US-1.7 |
| FR-2.2 | System shall relay user requests to an agent for model changes | MUST | US-1.8 |
| FR-2.3 | System shall display agent progress/status during tasks | MUST | US-1.9 |
| FR-2.4 | System shall automatically re-render diagrams when agent commits changes | MUST | US-1.10 |
| FR-2.5 | System shall support "what-if" exploration queries | SHOULD | US-1.12 |
| FR-2.6 | System shall support side-by-side comparison of design variants | SHOULD | US-1.13 |

### FR-3: Agent-Assisted Visualization

| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| FR-3.1 | Agent shall modify diagram view in response to questions (zoom, highlight, filter) | MUST | US-2.1, US-2.2, US-2.3 |
| FR-3.2 | Agent shall add annotations to diagrams to explain answers | SHOULD | US-2.4 |
| FR-3.3 | Agent shall provide narration explaining view changes | MUST | US-2.5 |
| FR-3.4 | System shall maintain conversation context for follow-up questions | MUST | US-2.7 |
| FR-3.5 | System shall support undo/redo of view changes | SHOULD | US-2.8 |
| FR-3.6 | System shall allow saving named view configurations | COULD | US-2.9 |

### FR-4: Export Generation

| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| FR-4.1 | System shall export current view as PNG image | MUST | US-3.1 |
| FR-4.2 | System shall export current view as SVG image | SHOULD | US-3.1 |
| FR-4.3 | System shall support high-resolution/publication-quality export | SHOULD | US-3.2 |
| FR-4.4 | System shall export interactive HTML files | MUST | US-3.4 |
| FR-4.5 | Interactive HTML exports shall work without server/installation | MUST | US-3.7 |
| FR-4.6 | System shall allow selecting which layers to include in export | SHOULD | US-3.8 |
| FR-4.7 | System shall allow adding title/description to exports | SHOULD | US-3.9 |
| FR-4.8 | System shall support saving export presets | COULD | US-3.10 |

---

## Non-Functional Requirements

### NFR-1: Usability

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| NFR-1.1 | Interface shall not require SysML knowledge to use | MUST | Primary users are domain engineers, not SysML experts |
| NFR-1.2 | New users shall be able to perform basic tasks within 10 minutes | SHOULD | Minimize onboarding friction |
| NFR-1.3 | Interface shall provide example queries/prompts | SHOULD | Help users discover capabilities |
| NFR-1.4 | Diagrams shall use intuitive engineering notation where possible | SHOULD | Match users' mental models |

### NFR-2: Performance

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| NFR-2.1 | Initial diagram render shall complete within 5 seconds for typical models | SHOULD | Exploration should feel responsive |
| NFR-2.2 | View changes (zoom, pan, toggle) shall respond within 200ms | SHOULD | Maintain sense of direct manipulation |
| NFR-2.3 | Agent-initiated view changes shall animate smoothly | SHOULD | Help users track what changed |

### NFR-3: Accessibility

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| NFR-3.1 | Interface shall support keyboard navigation | SHOULD | Accessibility best practice |
| NFR-3.2 | Color schemes shall be colorblind-friendly | SHOULD | ~8% of male users have color vision deficiency |
| NFR-3.3 | Diagrams shall have sufficient contrast ratios | SHOULD | WCAG 2.1 compliance |

### NFR-4: Compatibility

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| NFR-4.1 | Application shall run in modern web browsers (Chrome, Firefox, Safari, Edge) | MUST | Web-based platform decision |
| NFR-4.2 | Application shall work on desktop screen sizes (1280px+ width) | MUST | Primary use case |
| NFR-4.3 | Interactive HTML exports shall work offline | MUST | Stakeholders may not have internet access |

### NFR-5: Integration

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| NFR-5.1 | System shall read models from local git repository | MUST | Models stored in git |
| NFR-5.2 | System shall detect git commits to trigger re-render | MUST | Agent workflow produces commits |
| NFR-5.3 | System shall integrate with existing agent (Claude Code) for queries | MUST | Leverage existing agentic infrastructure |
| NFR-5.4 | System shall use syside for model parsing | SHOULD | Consistent with existing toolchain |

---

## Constraints

| ID | Constraint | Rationale |
|----|------------|-----------|
| C-1 | No direct model editing via diagrams | Keeps scope manageable; model changes go through agent |
| C-2 | Models remain in SysML v2 textual format | Source of truth; enables version control |
| C-3 | Must work with existing git-based workflow | Team already uses git for collaboration |

---

## Open Questions

| ID | Question | Impact |
|----|----------|--------|
| OQ-1 | How to handle large models with 100+ components? | Performance, layout algorithms |
| OQ-2 | How to represent uncertainty/ranges in visualizations? | Visualization design |
| OQ-3 | Should agent have direct access to visualization state, or work through API? | Architecture |
| OQ-4 | How to handle models that fail to parse? | Error handling, UX |
| OQ-5 | What level of diagram customization is needed (colors, shapes, layout)? | Scope, complexity |
