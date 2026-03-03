# Implementation Plan: IFE Cost Model — Spec Through Implementation

**Status:** In Progress (Phase 5 remaining)
**Created:** 2026-03-02
**Last Updated:** 2026-03-03

## Source Documents
- **Epic:** `.project/backlog/epic-full-workflow-demo.md` (Item 6)
- **Modeling epic:** `work/backlog/epic-ife-cost-modeling.md` (WI-006, WI-007, WI-008)
- **Modeling target:** `modeling_project/intent/IFE Modeling Target Selection.md`
- **Domain insights:** DI-001 through DI-005 in `knowledge/KNOWLEDGE.md`

## Implementation Strategy

**Phasing Rationale:**
This item is a meta-workflow — the user runs modeling PM commands (`/spec-model`, `/design-model`, `/plan-model`, `/implement-model`) and this plan defines what to verify and capture between each step. The modeling commands do the actual work; this plan ensures the artifacts, PM state, and demo content are correct at each checkpoint.

Three work items run sequentially through the full cycle. WI-006 gets the deepest verification and demo capture (it's the "from scratch" showcase). WI-007 and WI-008 get lighter verification with capture focused on progression and output.

**Overall Validation Approach:**
- After each modeling PM command, verify: artifact exists, frontmatter correct, PM state updated
- After implement phases, verify: SysML files created, validation run, results captured
- Demo capture happens alongside verification — same artifacts serve both purposes

---

## Phase 1: WI-006 — IFE Cost Structure Library (Full Cycle)

This is the primary demo showcase. Capture everything.

### 1a: Spec (`/spec-model` on WI-006)

**User runs**: `/spec-model` targeting WI-006 (IFE Cost Structure Library)

**Verify after:**
- [ ] `work/active/WI-006_ife_cost_structure_library/spec.md` exists
- [ ] Spec frontmatter: `Status: active`, `Scale: standard`, `Epic: "IFE Cost Modeling"`
- [ ] `work/BACKLOG.md` updated: WI-006 status changed from `backlog` to `active`
- [ ] Spec content traces to DI-001→005 (Hawker parameters, CAS mapping, fusion cycle gain)
- [ ] Spec defines what SysML elements to create and their acceptance criteria
- [ ] `uv run agentic-mbse status` shows WI-006 as active, stage "speccing"

**Capture for demo:**
- [ ] Screenshot or excerpt of the spec showing requirements traced to DI-XXX entries
- [ ] Dashboard output showing WI-006 transitioned to active

### 1b: Design (`/design-model` on WI-006)

**User runs**: `/design-model` targeting WI-006

**Verify after:**
- [ ] `work/active/WI-006_ife_cost_structure_library/design.md` exists
- [ ] Design references the spec and proposes SysML architecture (part defs, calc defs, attribute structure)
- [ ] Design addresses MR-3 (library definitions are concept-agnostic)
- [ ] Design addresses MR-4 (citation format for quantitative values)
- [ ] `uv run agentic-mbse status` shows WI-006 stage as "designing"

**Capture for demo:**
- [ ] Excerpt of design showing SysML architecture decisions (e.g., Hawker parameter structure, CAS mapping approach)

### 1c: Plan (`/plan-model` on WI-006)

**User runs**: `/plan-model` targeting WI-006

**Verify after:**
- [ ] `work/active/WI-006_ife_cost_structure_library/plan.md` exists
- [ ] Plan has phased implementation with validation checkpoints
- [ ] Plan references design.md for SysML structure
- [ ] `uv run agentic-mbse status` shows WI-006 stage as "implementing" (plan exists = ready to implement)

**Capture for demo:**
- [ ] Plan phase structure overview (showing the validation-at-each-step approach)

### 1d: Implement (`/implement-model` on WI-006)

**User runs**: `/implement-model` targeting WI-006

**Verify after:**
- [ ] SysML files created in `models/library/` (expected: `ife_cost_parameters.sysml`, `cas_ife.sysml`, `lcoe_calculation.sysml` or similar)
- [ ] SysML files parse cleanly: `uv run syside check models/library/<file>.sysml`
- [ ] Validation levels run (at minimum Levels 1-3):
  - Level 1: Parse — no syntax errors
  - Level 2: Resolve — no unresolved references
  - Level 3: Constraints — model constraints satisfied
- [ ] All 14 Hawker parameters exist as typed attributes with ranges and sensitivity metadata
- [ ] CAS mapping covers shared and IFE-specific accounts
- [ ] LCOE calculation framework exists
- [ ] Fusion cycle gain constraint (eta*G > 10) present
- [ ] Quantitative values carry MR-4 citations
- [ ] WI-006 status updated to `completed` in BACKLOG.md (or done via `/status close`)
- [ ] `uv run agentic-mbse status` reflects completion

**Capture for demo:**
- [ ] Validation output (pass/fail per level — both outcomes are demo content)
- [ ] SysML excerpt showing a representative element (e.g., Hawker parameter def with citation)
- [ ] Dashboard showing WI-006 complete, WI-007 ready

**What We Know Works After Phase 1:**
The full modeling PM cycle (spec → design → plan → implement) works end-to-end. Library patterns for IFE cost modeling exist and pass validation. The PM state correctly tracks the work item through its lifecycle.

---

## Phase 2: WI-007 — Generic IFE Concept Model (Full Cycle)

Lighter verification — focus on what's new (model uses library, produces LCOE output).

### 2a–2c: Spec → Design → Plan

**User runs**: `/spec-model`, `/design-model`, `/plan-model` on WI-007 sequentially

**Verify after each:**
- [ ] Artifact exists in `work/active/WI-007_generic_ife_concept_model/`
- [ ] WI-007 status tracks through the lifecycle in BACKLOG.md
- [ ] Spec/design reference WI-006 library elements (not duplicating them)
- [ ] Design includes: abstract driver interface, target factory as OpEx, chamber, BOP, power balance
- [ ] Dashboard shows WI-007 progressing

### 2d: Implement (`/implement-model` on WI-007)

**User runs**: `/implement-model` targeting WI-007

**Verify after:**
- [ ] SysML files created in `models/designs/generic_ife/` (or similar)
- [ ] Model imports/uses library elements from WI-006
- [ ] Validation Levels 1-3 run
- [ ] Model produces LCOE output within Hawker's $25–120/MWh range for default parameters
- [ ] Abstract driver interface exists (parameterized by eta, gamma, E_d, N_d)
- [ ] Target factory modeled as operating cost
- [ ] Power balance: fusion cycle gain, recirculating power fraction
- [ ] Cost rollup through CAS hierarchy
- [ ] WI-007 completed in BACKLOG.md

**Capture for demo:**
- [ ] SysML excerpt showing concept model using library patterns (the reuse story)
- [ ] LCOE output for default parameters (the "it produces numbers" moment)
- [ ] Validation results

**What We Know Works After Phase 2:**
The library-to-design pattern works. A generic IFE plant model produces LCOE estimates from 14 parameters. The concept model correctly uses library definitions without duplicating them.

---

## Phase 3: WI-008 — HIF Concept Instantiation (Full Cycle)

Focus on the output — real cost numbers from real source data.

### 3a–3c: Spec → Design → Plan

**User runs**: `/spec-model`, `/design-model`, `/plan-model` on WI-008 sequentially

**Verify after each:**
- [ ] Artifact exists in `work/active/WI-008_hif_concept_instantiation/`
- [ ] Spec/design reference Meier 1986 and Bangerter 2013 as authority sources
- [ ] Design specializes the generic IFE model (not rebuilding from scratch)
- [ ] HIF driver cost formula present: C_d = (0.32 + 0.088·E_d) × (1.25 + 0.05·N_c) × (1 + 0.0088·(v−5))
- [ ] Dashboard tracks WI-008

### 3d: Implement (`/implement-model` on WI-008)

**User runs**: `/implement-model` targeting WI-008

**Verify after:**
- [ ] SysML files in `models/designs/hif_ife/` (or similar)
- [ ] Model specializes generic IFE from WI-007
- [ ] HIF-specific parameters populated from sources:
  - Driver efficiency 20–30%
  - Target gain curves (distributed radiator, close-coupled, x-target)
  - Rep rate 5–10 Hz
  - Driver cost formula with all 3 factors
- [ ] All parameters cite source with MR-4 format
- [ ] Validation Levels 1-3 run
- [ ] COE cross-validation: compare output against Meier 1986 projections (3.9–5.8 cents/kWh at 1.0 GWe, 1988$)
  - Match = great. Deviation = document and explain why.
- [ ] WI-008 completed in BACKLOG.md
- [ ] Full epic "IFE Cost Modeling" status updated (all 3 items done)

**Capture for demo:**
- [ ] HIF cost output — the numbers, with traceability chain (model → DI-XXX → source document → page)
- [ ] COE cross-validation result (match or explained deviation)
- [ ] Final validation results across all 3 work items
- [ ] Final dashboard showing epic 3/3 complete

**What We Know Works After Phase 3:**
The full modeling pipeline from library → generic concept → concrete instantiation works. HIF cost numbers are produced and cross-validated against reference literature. Traceability chain is complete from model output back to source documents.

---

## Phase 4: Demo Section 7 Update

### Goal
Populate the "Concept Modeling" section of `demo/index.html` with the artifacts captured in Phases 1–3. Section 7 already has epic setup content from Item 5 — this adds the actual modeling pipeline showcase below it.

### Content Structure

Section 7 should show the modeling pipeline in action with these sub-sections:

1. **The Modeling Pipeline** — Brief explanation: each work item goes through spec → design → plan → implement, with validation at every gate. Show the `/spec-model` → ... → `/implement-model` command sequence.

2. **Spec Phase Showcase** — Chat transcript of `/spec-model` on WI-006 (same visual style as Sections 5–6). Highlight: requirements traced to DI-XXX entries.

3. **Design & Plan** — Lighter treatment. Key excerpt from design showing SysML architecture decisions. Plan phase structure showing validation checkpoints.

4. **Implementation & Validation** — The core demo content:
   - SysML excerpt showing a representative model element (parameter with citation, cost rollup)
   - Validation output (all levels, pass and fail)
   - Terminal block showing validation commands and results

5. **The Output** — Cost numbers! LCOE breakdown, HIF COE cross-validation result. The payoff of the entire pipeline.

6. **Traceability Chain** — Visual showing: Source PDF → Extraction → DI-XXX → Spec → Model Parameter → Cost Output. The knowledge transformation story for the full pipeline.

### Changes

- [x] Add modeling pipeline showcase content to Section 7 in `demo/index.html`
- [x] Use captured artifacts from Phases 1–3 (chat transcripts, SysML excerpts, validation output, cost numbers)
- [x] Follow existing CSS patterns (chat-transcript, terminal-block, callout, knowledge-transform)
- [ ] Verify demo renders correctly in browser

---

## Phase 5: Epic & PM State Updates

- [ ] Check off Item 6 success criteria in `.project/backlog/epic-full-workflow-demo.md`
- [ ] Update Item 6 status in the summary table (Pending → ✅ Complete)
- [ ] Update remaining effort estimate in epic
- [ ] Run final `uv run agentic-mbse status` and `uv run agentic-mbse status --json`
- [ ] Save final dashboard to `data/dashboard-snapshot.json` (overwrite previous)
- [ ] Commit all changes

---

## Decision Points

These are moments where we may need to adjust course:

| Decision Point | When | Options |
|---------------|------|---------|
| WI-008 scope | After WI-007 completes | Full HIF instantiation vs. defer to Item 7 if time-tight |
| Validation failures | During any implement phase | Fix and re-run vs. document as-is (failures are demo content) |
| Demo depth | After Phase 3 | Deep showcase of all 3 WIs vs. WI-006 deep + WI-007/008 summarized |
| Section 7 structure | Phase 4 | Depends on what artifacts we actually captured — plan adjusts to reality |

## Risk Management

| Risk | Mitigation |
|------|------------|
| `/spec-model` or other commands produce unexpected output | Document what happened; adjust verification checklist |
| SysML validation fails at Level 1 (parse) | Fix syntax issues inline; this IS the demo workflow |
| BACKLOG.md state not updated by commands | Check after each command; use CLI (`pm close-item`) if needed |
| WI-006 takes longer than expected, squeezing WI-007/008 | WI-006 is the primary showcase; WI-007/008 can be lighter if needed |
| HIF COE doesn't match Meier projections | Expected — document deviation and explain (year-dollar basis, model simplification, etc.) |

## Implementation Notes

*[TO BE FILLED DURING IMPLEMENTATION]*

### Phase 1 Completion
**Completed:** 2026-03-02
**Actual Changes:**
- Full spec→design→plan→implement cycle completed for WI-006 (IFE Cost Structure Library)
- 6 SysML files created in `models/library/{foundation,cost_structure,analyses}/`:
  - `economic_parameter.sysml` — `'Economic Parameter'` attribute def + `'CAS Scope'` enum
  - `costed_component.sysml` — `'Costed Component'` abstract part def
  - `cas_hierarchy.sysml` — 9 CAS level 2 part defs with scope classification
  - `ife_cost_parameters.sysml` — 14 Hawker parameters with metadata
  - `ife_lcoe.sysml` — closed-form DCF LCOE calc def (14+2 inputs, 13 intermediates, 1 return)
  - `fusion_cycle.sysml` — recirculating power calc + viability constraint (eta*G >= 10)
- All 6 files pass syside check (Levels 1-3)
- Spec (9 modeling requirements), design (6 design decisions, validation report), plan (2 phases) — all complete with checked-off checklists
- 6 architectural decisions registered in ARCHITECTURE.md (AD-001 through AD-006)
- 5 SV entries in VALIDATION_MATRIX.md, all passing
- models/README.md updated with library catalog
- WI-006 closed and archived to `work/completed/20260302_WI-006_ife-cost-structure-library/`
- BACKLOG.md: WI-006 completed, epic status active, 1/3 done
**Issues:** None
**Deviations:**
- Work item archived to `work/completed/` on close (plan assumed it would stay in `work/active/` — the close command moves it)
- Design included a full prototyping + validation cycle that produced the final SysML files, so plan phases were refinement (citation audit) and project integration rather than new file creation

### Phase 2 Completion
**Completed:** 2026-03-02
**Actual Changes:**
- Full spec→design→plan→implement cycle completed for WI-007 (Generic IFE Concept Model)
- 2 SysML files in `models/designs/generic_ife/`:
  - `ife_subsystems.sysml` — 5 CAS22 L3 sub-accounts, abstract `'IFE Driver'` (4 params, no defaults), `'Target Factory'`, `'Reaction Chamber'` with `'Wall Type'` enum
  - `ife_plant.sysml` — `'IFE Power Plant'` composing 3 subsystems, all 14 Hawker params bound to `'IFE LCOE'` calc, recirculating power + viability constraint
- All 8 files (6 library + 2 design) pass syside check together
- Library files unmodified (clean git diff)
- Verification script `scripts/verify_ife_lcoe.py` — mirrors SysML calc, HIF design point $68.69/MWh (PASS within $25-120)
- DI-006 captured: LCOE nonlinearity (center-of-range params ≠ center LCOE)
- VALIDATION_MATRIX.md: SV-006 through SV-010 all passing (10 total)
- Spec (13 requirements), design (6 decisions, prototype), plan (2 phases) — all complete
- WI-007 closed and archived to `work/completed/20260302_WI-007_generic-ife-concept-model/`
**Issues:**
- Duplicate WI-009 "HIF Concept Instantiation" appeared in BACKLOG.md — needs cleanup
- BACKLOG.md status for WI-008 not updated to `active` even though spec.md exists with Status: active (dashboard caught mismatch)
**Deviations:**
- Design phase produced complete prototype (same pattern as WI-006), so plan phases were review/verify rather than new file creation

### Phase 3 Completion
**Completed:** 2026-03-03
**Actual Changes:**
- Full spec→design→plan→implement cycle completed for WI-008 (HIF Concept Instantiation)
- 3 new files:
  - `models/library/analyses/hif_economics.sysml` — 4 Meier calc defs (driver cost, reactor cost, total capital, COE) per ADR-002
  - `models/designs/hif_ife/hif_driver.sysml` — Concrete `'HIF Driver'` :> `'IFE Driver'`, Meier cost formula wired via EXPOSE (gamma), Osiris baseline params
  - `models/designs/hif_ife/hif_plant.sysml` — Osiris 1.0 GWe HIF plant, dual cost outputs (Hawker LCOE + Meier COE), all 14 params bound
- All 11 files pass syside check -Werror (0 errors, 0 warnings)
- No upstream files modified (library + generic_ife clean)
- `scripts/verify_hif_costs.py` — verification script, all SV checks pass
- `data/traceability_matrix.csv` — 7 HIF element rows
- VALIDATION_MATRIX.md: SV-011→015 all passing (15 total, 0 failing, 0 pending)
- models/README.md: Design Catalog section added
- Spec (11 requirements), design (7 decisions, A2 resolution, prototype, dataflow diagram), plan (2 phases, all checked)
- DI-006 captured during WI-007 (LCOE nonlinearity)
- Key domain finding: Hawker LCOE at Osiris HIF params = $270/MWh (target cost dominance at 3.5 Hz, $10/target)
  vs Meier COE = 4.74 cents/kWh ≈ $47/MWh (different model structure)
- WI-008 still active (not closed, per user direction)
**Issues:**
- Duplicate WI-009 was created and cleaned up (agent used `add-item` instead of status update — documented in Phase 2 notes)
**Deviations:**
- Design produced complete prototype (same pattern as WI-006/007)
- New library file (`hif_economics.sysml`) added per ADR-002 (calc defs in library) — this was not a modification of existing library files

### Phase 4 Completion
**Completed:** 2026-03-03
**Actual Changes:**
- Restructured Section 7 of `demo/index.html` to align with Stage 2 sub-processes from "The Workflow" (Section 3)
- Split into two main sub-sections: **Planning** (epic setup, backlog add, initial 0/3 dashboard) and **Execution** (modeling pipeline showcase)
- Added 7 new sub-sections under Execution:
  - "What a Spec Looks Like" — WI-006 spec YAML frontmatter + 7-row requirements table traced to DI-XXX/MR-X
  - "What a Design Looks Like" — 6 design decisions table + file structure tree
  - "What a Plan Looks Like" — Phase structure with validation checkpoints
  - "The SysML Models" — Two code excerpts: `ife_cost_parameters.sysml` (parameter metadata pattern) and `hif_driver.sysml` (concrete specialization pattern)
  - "Validation" — syside check terminal block + 5-of-15 validation matrix table
  - "Requirements Compliance" — MR-1 through MR-6 compliance table with evidence column
  - "Dashboard: After Completion" — actual dashboard output (3/3 done, 15/15 passing)
- Updated knowledge transformation trace chain to show full pipeline (intent → epic → spec/design/plan → SysML → validations)
- Used existing CSS patterns throughout: `report-highlight`, `terminal`, `table-wrap`, `callout`, `trace-chain`, `card`
**Issues:** None
**Deviations:**
- Plan originally proposed 6 sub-sections (pipeline, spec showcase, design & plan, implementation & validation, output, traceability chain). Actual structure is 7 sub-sections reorganized around "what does each artifact look like" + validation + compliance + dashboard, per user direction
- Removed "What Comes Next" transition text (no longer needed — execution content follows directly)
- The "Output" sub-section (cost numbers, LCOE breakdown) deferred to Item 7 (Visualization & Demo Completion)

### Phase 5 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**
