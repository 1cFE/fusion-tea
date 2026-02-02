# Concepts & Vision

High-level vision, interaction patterns, and UI concepts for the Fusion Model Visualization Interface.

## Vision Statement

> A conversational, visual interface that makes fusion system models accessible to domain engineers - enabling them to explore, understand, and evolve complex techno-economic models through natural dialogue with an AI assistant, without requiring SysML expertise.

## Core Principles

### 1. Model as Conversation Partner

The interface should feel like having a knowledgeable colleague who can:
- Show you any part of the system on demand
- Explain relationships and trade-offs
- Make changes when you describe what you want
- Generate visuals for your presentations

**Not:** A complex CAD tool that requires training to operate.

### 2. Views That Adapt to Questions

Different questions need different perspectives:
- "What's in the blanket system?" → Structural decomposition
- "How does heat flow through the plant?" → Functional/physics view
- "What drives the LCOE?" → Cost breakdown view

The agent should select and configure views to best answer the question.

### 3. Progressive Disclosure

Start simple, allow drilling down:
- Initial view shows major subsystems
- Click/ask to expand details
- Complexity revealed on demand, not all at once

### 4. Export-First Communication

Every view should be exportable for communication:
- What you see is what you get in exports
- Easy path from exploration to presentation

---

## Information Architecture

### View Types

```
┌─────────────────────────────────────────────────────────────┐
│                    STRUCTURAL VIEW                          │
│  "What contains what"                                       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Fusion Power Plant                                   │   │
│  │  ├── Tokamak Core                                    │   │
│  │  │    ├── Plasma Chamber                             │   │
│  │  │    ├── First Wall                                 │   │
│  │  │    ├── Blanket System                             │   │
│  │  │    │    ├── Breeding Blanket [16]                 │   │
│  │  │    │    └── Coolant Manifold                      │   │
│  │  │    └── Magnet System                              │   │
│  │  │         ├── TF Coils [16]                         │   │
│  │  │         ├── PF Coils [6]                          │   │
│  │  │         └── CS Coils [1]                          │   │
│  │  ├── Balance of Plant                                │   │
│  │  │    ├── Heat Exchangers                            │   │
│  │  │    ├── Turbine Generator                          │   │
│  │  │    └── Cooling Towers                             │   │
│  │  └── Auxiliary Systems                               │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    FUNCTIONAL VIEW                          │
│  "What connects to what, what flows where"                  │
│                                                             │
│      ┌──────────┐    heat    ┌──────────┐    steam         │
│      │  Plasma  │ ─────────► │ Blanket  │ ─────────►       │
│      └──────────┘            └──────────┘                   │
│           │                       │                         │
│           │ neutrons              │ tritium                 │
│           ▼                       ▼                         │
│      ┌──────────┐            ┌──────────┐                   │
│      │  First   │            │ Tritium  │                   │
│      │  Wall    │            │ Recovery │                   │
│      └──────────┘            └──────────┘                   │
│                                                             │
│  [Shows ports, connections, flow directions]                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      COST VIEW                              │
│  "What drives the economics"                                │
│                                                             │
│  LCOE: $45/MWh                                              │
│  ├── Capital (70%) ████████████████████░░░░░░ $31.50       │
│  │    ├── Magnets (35%)    ███████░░░░░░░░░░░ $11.03       │
│  │    ├── Blanket (20%)    ████░░░░░░░░░░░░░░  $6.30       │
│  │    ├── Structures (15%) ███░░░░░░░░░░░░░░░  $4.73       │
│  │    └── Other (30%)      ██████░░░░░░░░░░░░  $9.45       │
│  ├── O&M (20%)     █████░░░░░░░░░░░░░░░░░░░░░  $9.00       │
│  └── Fuel (10%)    ██░░░░░░░░░░░░░░░░░░░░░░░░  $4.50       │
│                                                             │
│  [Treemap, Sankey, or bar breakdown options]                │
└─────────────────────────────────────────────────────────────┘
```

### Layered Overlays (on Structural View)

When useful, multiple aspects can be shown simultaneously:

```
┌────────────────────────────────────────────┐
│  Blanket System                            │
│  ┌──────────────────────────────────────┐  │
│  │  Breeding Blanket [16]               │  │
│  │  ─────────────────────────           │  │
│  │  Cost: $394M (24.6% of total)   ◄── Cost overlay
│  │                                      │  │
│  │  ┌────────┐    Li6    ┌────────┐    │  │
│  │  │Neutron │ ────────► │Tritium │    │◄── Physics overlay
│  │  │Capture │           │Breeding│    │  │
│  │  └────────┘           └────────┘    │  │
│  │                                      │  │
│  └──────────────────────────────────────┘  │
└────────────────────────────────────────────┘
```

---

## Interaction Patterns

### Pattern 1: Conversational Exploration

```
┌─────────────────────────────────────────────────────────────┐
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                      │   │
│  │              [DIAGRAM VIEW AREA]                     │   │
│  │                                                      │   │
│  │    Currently showing: Structural view of             │   │
│  │    Tokamak Core, expanded to show Magnet System      │   │
│  │                                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Agent: The TF coils are the most expensive magnet    │   │
│  │ component at $180M, primarily due to the             │   │
│  │ superconducting wire cost. I've highlighted them     │   │
│  │ in the diagram above.                                │   │
│  │                                                      │   │
│  │ Would you like me to break down the TF coil costs,   │   │
│  │ or compare with the PF coil costs?                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ You: What makes the TF coils so expensive?           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [────────────────────────────────────────────] [Send]      │
│   Ask about the model...                                    │
└─────────────────────────────────────────────────────────────┘
```

### Pattern 2: Action Requests

```
User: "Add a backup cooling system to the blanket"

Agent: I'll add a backup cooling system to the blanket.
       Let me work on that...

       [━━━━━━━━━━░░░░░░░░░░] 40%
       Exploring existing cooling patterns...

       [━━━━━━━━━━━━━━━━░░░░] 80%
       Creating backup cooling system definition...

       ✓ Complete! I've added:
       - BackupCoolingSystem part def in library/definitions/blanket.sysml
       - Instance in designs/catf/plant.sysml
       - Cost model with $12M estimate

       [Diagram updates to show new component]

       The backup cooling system is now connected to the
       blanket. Would you like me to explain the cost
       assumptions or adjust the design?
```

### Pattern 3: Export Flow

```
┌─────────────────────────────────────────────────────────────┐
│  Export Current View                                   [X]  │
│  ───────────────────────────────────────────────────────    │
│                                                             │
│  Format:   ○ PNG   ○ SVG   ● Interactive HTML               │
│                                                             │
│  Include:  ☑ Structural relationships                       │
│            ☑ Cost annotations                               │
│            ☐ Physics flows                                  │
│                                                             │
│  Title:    [Tokamak Core Cost Breakdown_______________]     │
│                                                             │
│  Description:                                               │
│  [Cost breakdown of tokamak core subsystems for_____]       │
│  [Q2 2026 design review.____________________________]       │
│                                                             │
│  Resolution: ○ Standard   ● High (print quality)            │
│                                                             │
│                              [Cancel]  [Export]             │
└─────────────────────────────────────────────────────────────┘
```

---

## Layout Concepts

### Main Interface Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│  Fusion TEA                                    [Export ▼]  [⚙]       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                                                                 │  │
│  │                                                                 │  │
│  │                                                                 │  │
│  │                        DIAGRAM CANVAS                          │  │
│  │                                                                 │  │
│  │                     (zoomable, pannable)                       │  │
│  │                                                                 │  │
│  │                                                                 │  │
│  │                                                                 │  │
│  ├────────────────────────────────────────────────────────────────┤  │
│  │ View: [Structural ▼]  Layers: [☑ Costs] [☐ Physics]  Zoom: 75% │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ Agent                                              [Clear chat] │  │
│  │ ──────────────────────────────────────────────────────────────  │  │
│  │ 🤖 Showing the structural view of the Tokamak Core. The        │  │
│  │    magnet system contains 16 TF coils, 6 PF coils, and the     │  │
│  │    central solenoid.                                            │  │
│  │                                                                 │  │
│  │ You: What's the total mass of the magnets?                      │  │
│  │                                                                 │  │
│  │ 🤖 The total magnet mass is 2,340 tonnes:                      │  │
│  │    - TF Coils: 1,800 tonnes (16 × 112.5 tonnes each)           │  │
│  │    - PF Coils: 420 tonnes                                       │  │
│  │    - CS: 120 tonnes                                             │  │
│  │    I've added mass annotations to the diagram.                  │  │
│  │ ──────────────────────────────────────────────────────────────  │  │
│  │ [Ask about the model...___________________________________] [→] │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

### Responsive Behavior

- **Large screens (1920px+):** Chat panel can be docked to side
- **Medium screens (1280-1920px):** Chat panel below diagram (shown above)
- **Diagram can be maximized** to full screen for detailed exploration

---

## Agent Capabilities

The agent should be able to:

### Visualization Commands (internal)

| Capability | Description | Example Trigger |
|------------|-------------|-----------------|
| `focus(element)` | Zoom/pan to center on element | "Show me the TF coils" |
| `highlight(elements)` | Visually emphasize elements | "Which parts are most expensive?" |
| `expand(element)` | Show children of a container | "What's inside the blanket?" |
| `collapse(element)` | Hide children | "Zoom out to system level" |
| `setView(type)` | Switch view type | "Show me the cost breakdown" |
| `toggleLayer(layer)` | Show/hide overlay | "Add physics flows to this view" |
| `annotate(element, text)` | Add explanatory label | "Label the main cost drivers" |
| `compare(a, b)` | Side-by-side view | "Compare CATF vs stellarator costs" |

### Model Commands (via existing agent)

| Capability | Description | Example Trigger |
|------------|-------------|-----------------|
| Explore | Search and analyze model | "How is LCOE calculated?" |
| Add component | Create new part | "Add a backup power system" |
| Modify values | Change parameters | "Increase blanket thickness to 1.2m" |
| Run analysis | Execute calculations | "What's the LCOE with these changes?" |

---

## Technical Considerations

### Rendering Approach

Options to evaluate:
1. **D3.js** - Maximum flexibility, custom layouts
2. **Cytoscape.js** - Graph-focused, good for relationships
3. **React Flow** - Modern, good for hierarchical diagrams
4. **Mermaid** - Simple, markdown-based (limited interactivity)

Recommendation: Start with **Cytoscape.js** or **React Flow** for balance of capability and development speed.

### Model Parsing

- Use **syside** to parse SysML v2 → AST
- Transform AST to visualization-friendly graph structure
- Cache parsed models; re-parse on file changes

### Agent Integration

```
┌─────────────┐     WebSocket      ┌─────────────┐
│   Browser   │ ◄───────────────► │   Server    │
│   (React)   │                    │  (Node.js)  │
└─────────────┘                    └──────┬──────┘
                                          │
                                   ┌──────▼──────┐
                                   │ Claude Code │
                                   │   (Agent)   │
                                   └──────┬──────┘
                                          │
                                   ┌──────▼──────┐
                                   │  Git Repo   │
                                   │  (Models)   │
                                   └─────────────┘
```

### Git Integration

- Watch `.sysml` files for changes
- On commit, re-parse and push updated graph to browser
- Consider file system watcher + debounce for rapid changes

---

## MVP Scope

For initial implementation, prioritize:

### Must Have (MVP)
- [ ] Structural view with expand/collapse
- [ ] Cost overlay on structural view
- [ ] Natural language query input
- [ ] Agent-controlled focus/highlight
- [ ] PNG export
- [ ] Re-render on git commit

### Should Have (v1.1)
- [ ] Functional/physics view
- [ ] Interactive HTML export
- [ ] View history (undo/redo)
- [ ] Agent progress indicator

### Could Have (Future)
- [ ] Side-by-side comparison
- [ ] Saved view configurations
- [ ] Custom annotations
- [ ] Design variant management
