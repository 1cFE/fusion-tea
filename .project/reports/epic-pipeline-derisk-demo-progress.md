# Epic Progress: Pipeline De-Risk & Demonstration

**Epic**: `work/backlog/epic-pipeline-derisk-demo.md` | **Timebox**: 2026-07-04 → 2026-07-18 | **Branch**: `epic/pipeline-derisk-demo`
**Orchestration**: main session orchestrates; subagents execute item stages; orchestrator owns git, quality gates, and this report.

## Status Board

| Item | Name | Status | Notes |
|------|------|--------|-------|
| WI-013 | Pipeline Execution Spike | **wave 1 — running** | subagent launched 07-04 |
| WI-014 | SysML Wiring Construct Validation | **wave 1 — running** | subagent launched 07-04 |
| WI-015 | IFE End-to-End Demonstration | blocked on WI-013 | starts when spike proves plumbing |
| WI-016 | H2 Probe (blind derivation + differential) | **wave 1 — running (derivation phase)** | firewalled agent; comparison phase is a later, separate agent |
| WI-017 | Dossier & Explainer | rolling — dossier seeded | finalizes last |

**WI-009 (MFE library)**: paused per user 2026-07-04 (spec.md Status set to `paused`). Its design.md stays as-is; the WI-016 firewall excludes it.

## Log

### 2026-07-04 — Epic start
- Meta-review completed: `.project/research/20260704-120000_pipeline-hypothesis-meta-review.md` (the epic's motivating analysis)
- Epic authored and registered; items WI-013–017 added to BACKLOG.md under "Pipeline De-Risk & Demonstration" (P0)
- Item 4 reshaped per user direction: blind derivation from the full `knowledge/concept_research/` corpus + pretraining, with 1costingfe as held-out answer key
- Branch `epic/pipeline-derisk-demo` created
- Wave 1 launched (3 parallel subagents): WI-013 spike, WI-014 constructs, WI-016 derivation phase
- Firewall for WI-016 derivation: whitelist = `knowledge/concept_research/`, `knowledge/sources/`, `knowledge/SOURCE_INDEX.md`, pretraining. Excluded: 1costingfe repo, WI-009 artifacts, the meta-review, `archive/models/` (PyFECONS port), `exploration/concept_analysis/` computed values.

## Quality Gates (orchestrator-enforced before any item closes)

1. Item has spec.md in `work/active/WI-XXX_*/` (light is fine; scope + success criteria + firewall/protocol where applicable)
2. All `.sysml` deliverables pass `uv run syside check` (Level 1) minimum; Levels 2–3 where applicable
3. Numeric claims verified against stated anchors (SV-008 for WI-015; hand-computed expectations for WI-013)
4. Findings filed, not worked around: codegen/teax gaps recorded in the item's findings doc with repo pointers
5. Every item ships its written record (findings/process doc) — documentation is a deliverable
6. Git: one commit per meaningful milestone, orchestrator-authored; subagents never commit

## Decisions & Escalations

- (none yet)

## Hypothesis Evidence Tracker (feeds WI-017 dossier)

| Hypothesis | Evidence so far | Status |
|-----------|----------------|--------|
| H1 agentic modeling | IFE epic (prior); this epic adds the SV-008 oracle via WI-015 | partial |
| H2 research loop | pending WI-016 | untested → in progress |
| H3 SysML methodology | pending WI-014 (wiring constructs) | partial |
| H4 executable exploration | pending WI-013/015 | untested → in progress |
