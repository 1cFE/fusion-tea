# AI-Enabled MBSE Platform Workflow

## Overview

This document describes the workflow for an AI-enabled Model-Based Systems Engineering (MBSE) platform, organized into three main stages with a unified UX + Visualization layer.

**General Flow:** RESEARCH → MODEL → SIMULATE

---

## RESEARCH

> How a user **collects** and **organizes** external data for consumption or consideration in modeling.

### Actions
- Ingest a specific research paper
- Use external literature research tools
- Capture conversation notes

### Impacts
- Basis for new design concepts to model
- Improve current models (e.g. improve physics or costing)
- Increase quality of sources + traceability of models; justify existing assumptions

### Challenges
- How to keep data organized
- How to get user qualification and prioritization of the data
  - i.e. is this a trusted source? How heavily should we rely on it?

### Outputs
- `DATABASE`
- `MODELING PM (New Items)`

---

## MODEL

> How a user **manages agentic updates** to sysml models.

### Actions
- Process "features" from the modeling backlog
- Provide input and guidance to resolve ambiguities or conflicts

### Impacts
- Updates (e.g. new component definitions) to 'library'
- Updates to existing design concepts in 'designs'
- New design concepts

### Challenges
- Model version control
- Regression testing
- Make sure updates to library doesn't break old designs

### Outputs
- `MODELING PM (Updates)`
- `SYSML MODELS`

---

## SIMULATE

> How a user **numerically executes** modeled designs to calculate LCOE. 2-stage process. 

### Codegen

> How a user generates/updates the executable simulation code.

#### Actions
- Initiate automated generation from SysML models
- Inserts specialized physics code for more complex systems

#### Impacts
- Fully executable python created
- All inputs clearly parameterized with JSON files

#### Challenges
- Version synchronization
- Wrapping more complex physics

#### Outputs
- `TEAx Python`
- `Design Parameters (JSON)`

### Sim

> How a user runs analyses and studies on particular designs.

#### Actions
- Execute single simulations
- Run parameter sweeps and sensitivity analyses
- Initiate AI-led parametric design optimization

#### Impacts
- Side-by-side design comparisons
- Cost / LCOE breakdowns

#### Challenges
- Structure output standardization
- Results working with visualization

#### Outputs
- `Numerical Results Database`

---

## UX + VISUALIZATION

> UX design with visualization achieve the goals of each stage. And because workflows are not always linear, a key feature is the ability to highlight any context and use to initiate action for any other stage.

### RESEARCH

#### UX
- Read and comment on papers
- Modify tags (e.g. "precedence")
- AI search & synthesis
- Highlight pieces of data → create modeling work item

#### Visualize
- Input Data Explorer

---

### MODEL

#### UX
- Manage stages of agentic modeling:
  - Review spec
  - Input for design alternatives
  - Review model changes
  - [OPEN] Need to help manage git??
  - Initiate new work items (e.g. based on review)

#### Visualize
- Model Structural View
- Model Behavioral / Physics View

---

### SIMULATE: Codegen

#### UX
- Design selection for codegen
- View of design parameters
- [NOTE: any custom code writing likely deferred to an IDE]
- Overview of what designs are "compiled" for execution

---

### SIMULATE: Sim

#### UX
- Define, set up, and run studies

#### Visualize
- Costing / LCOE model overlays
- Study results plots & tables

---

## Summary

| Stage | Outputs |
|-------|---------|
| Research | `DATABASE`, `MODELING PM (New Items)` |
| Model | `MODELING PM (Updates)`, `SYSML MODELS` |
| Simulate: Codegen | `TEAx Python`, `Design Parameters (JSON)` |
| Simulate: Sim | `Numerical Results Database` |
