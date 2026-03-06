# Plan: IFE Domain Research

**Status**: Complete (pending commit)
**Epic**: Full Workflow Demo (Item 4)
**Created**: 2026-03-02

---

## Overview

Research 3+ IFE sources to produce DI-XXX entries covering cost structure, LCOE parameters, and sensitivity rankings. Identify which IFE sub-concept has the richest data for the modeling exercise.

**Execution model**: This is primarily a research execution task. Claude prepares research prompts; the user runs `/research`; Claude inspects results and populates demo artifacts.

---

## Phase 1: Run IFE Research Session [User executes]

**What**: A single comprehensive `/research` session that covers the three highest-value IFE sources against the investigation's research questions.

**Sources to research** (ordered by priority):
1. **Hawker 2020** — 14-parameter technology-agnostic IFE LCOE model, Monte Carlo sensitivity analysis
2. **HIF Economics 1986** (Meier/Hogan/Bangerter) — parametric COE model for heavy-ion IFE plants, driver cost scaling
3. **AMPS 2025** (Pacific Fusion) — modern high-yield pulser-driven IFE, explicit cost projections

**Research prompt** (as run by user):

> I want to plan out the modeling of my IFE system. This research will be the basis for our first pass of the model structure. Search across all relevant sources.
>
> **Design Concept**
> - Please synthesize the IFE concept into a logical process
>   - Identify the key behavioral and structural components that drive the effectiveness of the system
> - Provide any hierarchical breakdowns within IFE that is provided in the sources
>
> **Cost Background**
> - What are the major cost categories for an IFE power plant? How do they map to the CAS framework (CAS20-series)?
> - Which cost categories are IFE-specific (driver, target factory, chamber) vs. shared with MFE (BOP, buildings, indirect costs)?
> - How does driver type (laser vs. heavy-ion vs. pulser) change the cost structure?
>
> **LCOE**
> - What LCOE values do these sources project, and under what assumptions?
> - What are the key input parameters for IFE LCOE calculation? (Hawker identifies 14 — enumerate them with units and typical ranges)
> - How do the three sources' economic models compare in structure and assumptions?

- [x] User runs `/research` with the prompt above
- [x] Research document saved to `knowledge/research/pending/`
- [x] DI-XXX insight candidates proposed for approval

**Validation**: Research document exists, covers all 3 sources, contains quantitative findings with citations.

---

## Phase 2: Review and Approve Research [User + Claude]

**What**: Inspect the research output. Ensure DI-XXX candidates are well-structured and cover the key areas.

**Expected DI-XXX coverage** (5+ entries):
- DI: IFE cost structure — which CAS categories apply, what's shared vs. divergent from MFE
- DI: Hawker's 14 LCOE parameters — enumeration with units, ranges, sensitivity rankings
- DI: HIF driver cost scaling — relationships from the 1986 parametric study
- DI: IFE LCOE ranges — projected values from each source with stated assumptions
- DI: High-sensitivity high-uncertainty parameters — the critical modeling parameters for IFE

- [x] Inspect research document for completeness and accuracy
- [x] Fixed YAML frontmatter (was markdown bold, converted to `---` delimited YAML)
- [x] Review DI-XXX candidates — all 5 accepted (DI-001 through DI-005)
- [x] Approved research moved to `knowledge/research/approved/`
- [x] DI-XXX entries appended to `knowledge/KNOWLEDGE.md`

**Validation**: KNOWLEDGE.md has 5+ IFE-related DI-XXX entries with source citations.

---

## Phase 3: Write Modeling Target Recommendation [Claude]

**What**: Based on the research findings, write a recommendation for which IFE sub-concept to model first, with rationale grounded in data availability.

**Candidates** (from epic):
- **Generic IFE** (Hawker's 14-parameter model) — broadest, technology-agnostic, good for demonstrating sensitivity analysis but less specific on subsystem costs
- **Heavy Ion Beam IFE** — two dedicated papers (1986, 2013), well-defined driver cost structure, parametric scaling relationships
- **Laser indirect-drive IFE** — AMPS 2025 + Xcimer 2026, most current data, explicit cost projections

**Evaluation criteria**:
- Data richness: which sub-concept has the most quantitative cost data at CAS level?
- Parameter completeness: can we populate the 14 Hawker parameters for this sub-concept?
- Source quality: which sources provide the most concrete, citable numbers?
- Demo value: which makes the most compelling modeling exercise?

- [x] Write recommendation with rationale
- [x] Captured as intent document: `modeling_project/intent/IFE Modeling Target Selection.md`
- [x] User reviewed and approved

**Decision**: Generic driver-agnostic IFE model (Hawker 14-parameter framework) with HIF as first instantiation. Rationale and implied work items documented in intent artifact.

**Validation**: Written recommendation exists, grounded in DI-XXX entries, covers all three candidates.

---

## Phase 4: Populate Demo Section 6 [Claude]

**What**: Update `demo/index.html` section 6 (Domain Research) with real artifacts showing the knowledge transformation: PDF text → structured DI-XXX insights.

**Content to include**:
- The research question/prompt that was used (shows how research is directed)
- Example of raw source content → extracted insight (before/after showing the transformation)
- 2-3 representative DI-XXX entries rendered in the demo (showing the structured format)
- The modeling target recommendation
- Summary stats: X sources researched, Y insights extracted, Z parameters identified

**Approach**: Replace the stub banner with real content. Follow the patterns established in sections 1-5.

- [x] Remove stub banner from section 6
- [x] Add research process walkthrough content (chat-transcript style)
- [x] Embed representative DI-XXX entries (DI-001, DI-002 full; DI-003–005 in expandable)
- [x] Add modeling target recommendation (callout with decision)
- [x] Added report structure highlight (YAML frontmatter + section outline + source citations)
- [x] Added knowledge transformation trace chain (sources → report → insights → decision)
- [x] Updated sidebar nav (removed stub marker)
- [x] Verify demo renders correctly in browser
- [x] Added "View full report" button + dialog with rendered report content

**Validation**: Section 6 is no longer a stub. Contains real artifacts from the research work.

---

## Phase 5: Commit [User]

- [ ] Review all changes: KNOWLEDGE.md, research artifacts, demo/index.html
- [ ] Commit

---

## Summary

| Phase | Who | What |
|-------|-----|------|
| 1 | User runs `/research` | Execute research session against 3 IFE sources |
| 2 | User + Claude | Review research output, approve DI-XXX entries |
| 3 | Claude | Write modeling target recommendation |
| 4 | Claude | Populate demo section 6 with real artifacts |
| 5 | User | Review and commit |
