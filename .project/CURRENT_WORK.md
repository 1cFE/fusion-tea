# Current Work

**Last Updated**: 2026-04-04

---

## Active Work

### Concept Explorer — Taxonomy Visualizer (shipped, assessing next steps)

**Status**: Core features landed, evaluating UX and feature gaps
**Location**: `exploration/concept_explorer/`
**Branch**: `ralph/concept-explorer`

Built Mar 29: taxonomy data layer (38 concepts), similarity engine, interactive frontend with tree view, constellation scatter plot, taxonomy cards, and Cytoscape neighborhood graph (model-view architecture). 140+ tests passing.

**Components**:
- Data: `taxonomy_models.py`, `similarity.py`, `seed_registry.py`
- API: 7 taxonomy endpoints in `server.py`
- Frontend: `taxonomy.js` (orchestrator), `taxonomy_card.js`, `neighborhood_graph.js`, `constellation.js`, `tree_view.js`

### Phase 2a: Generative Reasoning Tree (paused)

**Status**: Round 0 complete, awaiting Round 1 (L1→L2 expansion)
**Location**: `exploration/phase_2a/`

Infrastructure built and tested. Round 0 expanded root → 5 confinement options, 22 constraints. L0 constraints are all novel physics-level variables — table validation meaningful at L2+.

### Traceability System (on hold)

**Status**: Spec + plan written, awaiting prioritization
**Location**: `.project/active/traceability-system/`

---

## Remaining Active Work Items

- `automated-concept-analysis` — status unknown
- `constraint-atms-spike` — status unknown
- `iterative-analysis-loop` — status unknown
- `source-replacement` — status unknown
- `traceability-system` — spec + plan written, on hold

---

## Recently Completed

### [2026-03-29] Concept Taxonomy & Interactive Explorer
4 work items archived (2 complete, 2 superseded). See `CHANGELOG.md`.

### [2026-03-06] Project Cleanup
9 active items and 4 epics archived. Infrastructure phase complete.

---

## Up Next

1. Assess taxonomy visualizer UX — identify rough edges and feature gaps
2. Phase 2a Round 1+ — expand L1→L2→L3, validate constraints
3. Traceability system implementation (when prioritized)
