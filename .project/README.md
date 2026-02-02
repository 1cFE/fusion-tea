# Project Management

This folder contains project planning, tracking, and documentation.

---

## Workflow Overview

### 1. Accumulating Backlog

**Collecting Needs**:
- **Research & Analysis**: Running research reports, web searches, collecting data to understand what needs to be done
- **During Development**: Issues identified while running/writing code
- **External PM**: Requirements from external project management systems

**Creating Epics**:
- Capture outcomes and goals
- Note known pieces of work (details come later during decomposition)

---

### 2. Prioritization

1. **User prioritizes** using their own methods
2. **Update BACKLOG.md** via `/project-manage` command - reorganize, set priorities
3. **Epic decomposition** (before or after prioritization, e.g., to estimate effort):
   - Organize into **parts** if needed (logical groupings)
   - Break down into **items** with numbering (e.g., `4.2` = Part 4, Item 2)

---

### 3. Epic Execution

Iterate through items in the epic:

| Step | Action | Output |
|------|--------|--------|
| **1. Start** | Create item folder under `active/` | `active/{item_name}/` |
| **2. Spec** | Define what needs to be done | `spec.md` |
| **3. Design** | Research codebase, identify all code changes | `design.md` |
| **4. Plan** | Plan implementation in Phases, include tests | `plan.md` |
| **5. Implement** | Execute plan, one phase at a time | Code changes |
| **6. Review** | Review work (can happen at any stage) | Feedback/approval |

**As the epic progresses**: Add or insert new items as you learn more. Follow the same process for each.

---

### 4. Epic Cleanup

1. **Check** for all completed active items
2. **Move items** to `completed/`, prefixed with date stamp (e.g., `20251223_item_name/`)
3. **Move epic** to `completed/` with date stamp (e.g., `20251223_epic_name.md`)
4. **Update docs**: `CURRENT_WORK.md`, `BACKLOG.md`, and `completed/CHANGELOG.md`

---

## Key Files

| File | Purpose |
|------|---------|
| `CURRENT_WORK.md` | What's active RIGHT NOW - single source of truth |
| `backlog/BACKLOG.md` | Prioritized list of epics |
| `backlog/epic_*.md` | Individual epic definitions |

---

## Folder Structure

```
.project/
├── CURRENT_WORK.md           # Active work tracking
├── backlog/
│   ├── BACKLOG.md            # Prioritized epic list
│   └── epic_*.md             # Epic definitions
├── active/
│   └── {item_name}/          # Work-in-progress items
│       ├── spec.md
│       ├── design.md
│       └── plan.md
├── completed/
│   ├── {date}_{item_name}/   # Archived items
│   └── epic_*.md             # Archived epics
├── research/                 # Deep investigations
└── reports/                  # Status reports
```

---

## Item Numbering

Items within an epic use hierarchical numbering:
- `1`, `2`, `3` - Simple sequential items
- `4.1`, `4.2`, `4.3` - Items within Part 4
- Parts group related items logically

---

## Commands

### Development Workflow

| Command | Purpose |
|---------|---------|
| `/_my_research` | Deep codebase exploration and feasibility analysis |
| `/_my_spec` | Feature requirements definition with business goals |
| `/_my_design` | Technical design for code implementation |
| `/_my_plan` | Create phased implementation plan with tests |
| `/_my_implement` | Execute approved plan with validation |
| `/_my_quick_edit` | Fast changes that don't need full workflow |

### Review & Quality

| Command | Purpose |
|---------|---------|
| `/_my_code_review` | Audit implementation against spec/design |
| `/_my_code_quality` | Run comprehensive quality checks |

### Project Management

| Command | Purpose |
|---------|---------|
| `/_my_project_manage` | Status review, gap analysis, backlog management |
| `/_my_project_find` | Quick lookup of project context |
| `/_my_git_manage` | Git workflow, worktrees, conflict resolution |

### Memory & Context

| Command | Purpose |
|---------|---------|
| `/_my_capture` | Mark conversation for later memorization |
| `/_my_memorize` | Create structured memory from capture |
| `/_my_recall` | Search past conversations |
| `/_my_review_compact` | Review before compaction |

---

**Last Updated**: Template
