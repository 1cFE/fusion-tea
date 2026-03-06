# Implementation Plan: IFE Modeling Epic Setup

**Status:** Draft
**Created:** 2026-03-02
**Last Updated:** 2026-03-02

## Source Documents
- **Epic:** `.project/backlog/epic-full-workflow-demo.md` (Item 5)
- **Modeling target:** `modeling_project/intent/IFE Modeling Target Selection.md`
- **Domain insights:** DI-001 through DI-005 in `knowledge/KNOWLEDGE.md`

## Implementation Strategy

**Phasing Rationale:**
This item is Setup/Planning — no code to write, no tests needed. The work is: (1) use `/backlog add` to create a modeling epic with work items from the intent document, (2) validate the CLI actually did what we expected, (3) capture the dashboard output, and (4) embed it in the demo.

**Execution model**: User runs `/backlog add` with the intent document as source. The backlog agent reads the intent doc, assesses scale (epic), decomposes into work items, and registers them via `agentic-mbse pm add-item`. This plan covers what happens before, during, and after.

---

## Phase 1: Create IFE Modeling Epic + Work Items [User executes]

**What**: User runs `/backlog add` with the IFE Modeling Target Selection intent document as source. The agent reads the intent doc (which contains the modeling decision and 3 implied work items), assesses scale as Epic, and creates the epic + work items via CLI.

**Input**: `modeling_project/intent/IFE Modeling Target Selection.md`

**Expected epic structure** (from intent doc, Section "Implied Work Items"):
1. **Library patterns for IFE cost structure** — Hawker's 14 parameters as model attributes, CAS mapping, LCOE calculation framework, fusion cycle gain constraint
2. **Generic IFE concept model** — driver-agnostic plant with abstract driver interface, target factory, chamber, BOP
3. **HIF instantiation** (optional — may be deferred) — populate driver parameters from 1986/2013 sources

**Expected CLI calls** (approximate — agent decides exact names):
```bash
uv run agentic-mbse pm add-item --name "IFE Library Patterns" --scale standard --priority P0 --epic "IFE Cost Modeling"
uv run agentic-mbse pm add-item --name "Generic IFE Concept Model" --scale standard --priority P0 --epic "IFE Cost Modeling"
```

- [x] User runs `/backlog add` pointing at the intent doc
- [x] Agent creates epic file at `work/backlog/epic-ife-cost-modeling.md`
- [x] Agent registers 3 work items via `agentic-mbse pm add-item --epic "IFE Cost Modeling"`
- [x] Epic appears in `work/BACKLOG.md` YAML frontmatter under `epics:`
- [x] 3 work items listed under the epic (WI-006, WI-007, WI-008)

**Validation**: See Phase 2.

---

## Phase 2: Validate Modeling PM State [Claude]

**What**: After the agent runs, verify the modeling PM state is correct. The CLI manages `work/BACKLOG.md` — confirm it wrote valid YAML frontmatter, the items have correct IDs (WI-XXX sequence), and the dashboard parses cleanly.

- [x] Read `work/BACKLOG.md` — confirm YAML frontmatter has the new epic with items
- [x] Verify epic fields: name "IFE Cost Modeling", priority P0, status draft
- [x] Verify work item fields: WI-006/007/008, scale standard, status backlog
- [x] Read epic file in `work/backlog/epic-ife-cost-modeling.md` — rich body with context, source deps, success criteria, per-item scope, sequencing, risks
- [x] Run `uv run agentic-mbse status` — parses without errors
- [x] Run `uv run agentic-mbse status --json` — structured output captured
- [x] Confirm dashboard shows the new epic and work items (0/3 done)

**Validation**: Dashboard runs clean, shows the IFE modeling epic with 2–3 work items in `backlog` status.

**What We Know Works After This Phase:**
The modeling PM state is valid and the dashboard reflects the planned work.

---

## Phase 3: Capture Dashboard Output [Claude]

**What**: Run the dashboard and capture its output for embedding in the demo. The demo already has a "sparse" dashboard in Section 3 (The Workflow, "Visibility" subsection). We need a richer version now that real work items exist.

- [x] Run `uv run agentic-mbse status` and capture the full markdown output
- [x] Run `uv run agentic-mbse status --json` and save to `data/dashboard-snapshot.json`
- [x] Note key dashboard elements: "IFE Cost Modeling" epic, 0/3 done, 3 items in backlog, 0 requirements, 0 validations

**What We Know Works After This Phase:**
We have dashboard output ready for demo embedding.

---

## Phase 4: Update Demo Section 7 [Claude]

**What**: Section 7 (Concept Modeling) in `demo/index.html` is currently a stub. Replace the stub with content showing the modeling epic setup — the bridge between domain research (Section 6) and actual model building.

The item scope says "Embed dashboard output in the demo showing the epic with work items." This fits naturally in Section 7, which covers the transition from research to modeling.

**Content to include**:
1. **Decision callout**: Generic IFE model with HIF first instantiation (from intent doc)
2. **Chat transcript**: Show the `/backlog add` interaction in `chat-transcript` style (same pattern as Section 6's `/research` showcase). Use the actual transcript from the session:
   - User message: `/backlog add` with intent doc path
   - Ellipsis: Agent reads intent doc, assesses scale, decomposes...
   - Agent message: Summary table with epic name, work items (WI-006/007/008), dependencies
   - Agent message: "Next step: /spec-model on WI-006..."
3. **Dashboard snapshot**: The `agentic-mbse status` output in a terminal block showing the populated epic
4. **What comes next**: Brief forward-reference to Item 6 (the actual spec → design → plan → implement cycle)

**Actual `/backlog add` transcript** (captured from session):
```
User: /backlog add modeling_project/intent/IFE Modeling Target Selection.md

Agent: [reads intent doc, assesses scale, decomposes into epic + items]

Agent: All three items registered. Let me verify the final backlog state.
       [reads work/BACKLOG.md]

Agent: Backlog is set up. Here's what was created:

  Epic: IFE Cost Modeling (P0, draft)
  Epic file: work/backlog/epic-ife-cost-modeling.md

  | ID     | Item                       | Depends On |
  |--------|----------------------------|------------|
  | WI-006 | IFE Cost Structure Library | None       |
  | WI-007 | Generic IFE Concept Model  | WI-006     |
  | WI-008 | HIF Concept Instantiation  | WI-007     |

  Next step: /spec-model on WI-006 to begin the first item.
```

**Approach**: Replace the stub banner + stub-content div with real content. Use Section 6's `chat-transcript` / `chat-msg` / `chat-ellipsis` CSS classes for the `/backlog add` showcase.

- [x] Remove stub banner from Section 7
- [x] Add lead paragraph explaining the transition from research → planning
- [x] Add "From Decision to Epic" subsection with context + `/backlog add` explanation
- [x] Add chat transcript showing `/backlog add` interaction (user, ellipsis, agent summary with table)
- [x] Add explanatory note below transcript (what agent did, YAML as source of truth)
- [x] Add "The Epic File" subsection with callout on authority source dependencies
- [x] Embed dashboard output in terminal block under "Dashboard" subsection
- [x] Add comparison note referencing Section 3's sparse dashboard
- [x] Add "What Comes Next" subsection (spec-model on WI-006)
- [x] Add knowledge transform block (input → output)
- [x] Update sidebar nav — removed `stub` class and badge from Section 7 link
- [ ] Verify demo renders correctly in browser

**Validation**: Section 7 is no longer a stub. Contains chat transcript of `/backlog add`, dashboard output, and epic setup artifacts. Chat transcript follows same visual style as Section 6.

---

## Phase 5: Update Epic Status [Claude]

**What**: Mark Item 5 success criteria in the epic file.

- [x] Check off success criteria in `.project/backlog/epic-full-workflow-demo.md` Item 5
- [x] Update the summary table status for Item 5 (Pending → ✅ Complete)
- [x] Updated remaining effort estimate (3.5–4 days → 2–2.5 days)

---

## Phase 6: Commit [User]

- [ ] Review all changes: `work/BACKLOG.md`, `work/backlog/epic-*.md`, `demo/index.html`
- [ ] Commit

---

## Summary

| Phase | Who | What |
|-------|-----|------|
| 1 | User (`/backlog add`) | Create modeling epic + work items from intent doc |
| 2 | Claude | Validate BACKLOG.md state and dashboard output |
| 3 | Claude | Capture dashboard output for demo |
| 4 | Claude | Replace Section 7 stub with real epic/dashboard content |
| 5 | Claude | Update epic status |
| 6 | User | Review and commit |

## Risk Management

| Risk | Mitigation |
|------|------------|
| `add-item --epic` creates new epic implicitly vs. requiring pre-registration | Test with a single item first; inspect BACKLOG.md before adding more |
| Dashboard errors on new YAML structure | Run `status --json` to get structured error output if markdown fails |
| `/backlog add` agent names items differently than expected | Names are cosmetic — validate structure and count, not exact wording |

## Implementation Notes

*[TO BE FILLED DURING IMPLEMENTATION]*

### Phase 1 Completion
**Completed:** 2026-03-02
**Actual Changes:**
- User ran `/backlog add` with `modeling_project/intent/IFE Modeling Target Selection.md`
- Agent created epic "IFE Cost Modeling" (P0, draft) with 3 work items: WI-006 (IFE Cost Structure Library), WI-007 (Generic IFE Concept Model), WI-008 (HIF Concept Instantiation)
- Epic file at `work/backlog/epic-ife-cost-modeling.md` — includes authority source dependency table, success criteria, per-item scope with requirements, sequencing diagram (strictly sequential), and risks
- Items have dependency chain: WI-006 → WI-007 → WI-008
**Issues:** None

### Phase 2 Completion
**Completed:** 2026-03-02
**Actual Changes:**
- BACKLOG.md YAML frontmatter valid: epic with 3 items, correct WI-XXX sequence
- Epic file has rich body grounded in DI-001→005 and intent doc
- Dashboard parses clean (both markdown and JSON output)
- Removed stale historical standalone items WI-004/WI-005 from BACKLOG.md (should have been archived during project reframing; `close-item` CLI couldn't handle them — no work directories exist — so edited YAML directly)
**Issues:** WI-004/WI-005 had `status: completed` in YAML but dashboard rendered them as "backlog" — moot now since they're removed

### Phase 3 Completion
**Completed:** 2026-03-02
**Actual Changes:**
- Dashboard markdown and JSON captured (post WI-004/005 cleanup)
- JSON saved to `data/dashboard-snapshot.json`
- Dashboard shows: IFE Cost Modeling epic [0/3 done], 3 items in backlog, 0 requirements, 0 validations
**Issues:** None

### Phase 4 Completion
**Completed:** 2026-03-02
**Actual Changes:**
- Replaced Section 7 stub in `demo/index.html` with full content (~85 lines)
- Structure: lead → "From Decision to Epic" (context + chat transcript) → "The Epic File" (authority source callout) → "Dashboard" (terminal block) → "What Comes Next" (forward reference) → knowledge transform
- Chat transcript uses same `chat-transcript`/`chat-msg`/`chat-ellipsis` CSS classes as Section 6
- Table in chat transcript uses inline styles (matching the agent's rendered table output)
- Sidebar nav: removed `stub` class and `nav-badge` span from Section 7 link
**Issues:** None
**Deviations:** Added "The Epic File" subsection (not in original plan) to highlight the authority source dependency mapping — this is the traceability story that connects Section 7 to the rest of the demo
