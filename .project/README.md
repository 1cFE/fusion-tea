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
2. **Update BACKLOG.md** via `/_my_status` command - reorganize, set priorities
3. **Epic decomposition** (before or after prioritization, e.g., to estimate effort):
   - Organize into **parts** if needed (logical groupings)
   - Break down into **items** with numbering (e.g., `4.2` = Part 4, Item 2)

---

### 3. Epic Execution

Iterate through items in the epic. Each item runs the standard pipeline of `/_my_*` stages.

**For the canonical, current flow and when/how to use each stage, run `/_my_pipeline`** (installed
with claude-pack). This README does not carry its own copy of the sequence — `/_my_pipeline` is the
single source, so it can't go stale here.

**As the epic progresses**: Add or insert new items as you learn more. Follow the same process for each.

---

### 4. Epic Cleanup

1. **Check** for all completed active items
2. **Move items** to `completed/` using `git mv`, prefixed with date stamp (e.g., `git mv .project/active/item_name .project/completed/20251223_item_name`)
3. **Move epic** to `completed/` using `git mv` with date stamp (e.g., `git mv .project/backlog/epic_name.md .project/completed/20251223_epic_name.md`)
4. **Update docs**: `CURRENT_WORK.md`, `BACKLOG.md`, and `completed/CHANGELOG.md`

---

## Key Files

| File | Purpose |
|------|---------|
| `CURRENT_WORK.md` | What's active RIGHT NOW - single source of truth |
| `product/INDEX.md` | Generated index of implemented product promises — what the product is for (convention: `product/README.md`) |
| `adr/INDEX.md` | Generated index of load-bearing decisions (convention: `adr/README.md`) |
| `feedback/ENTRIES.md` | Append-only log of agent learnings, tagged by pack target (convention: `feedback/README.md`) |
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
├── adr/                      # Decision records (append-only, script-managed)
├── product/                  # Product promise ledger (append-only, script-managed)
├── feedback/                 # Agent learnings for the owner to act on (append-only)
├── scripts/                  # Utility scripts (adr.sh, product.sh, get-metadata.sh)
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

This README does not carry a command catalog — a copy here would drift. Two live sources:

- **`/_my_pipeline`** — the canonical stage map and when to use each stage.
- **The toolkit README's Command Reference** (in the agentic-project-init repo) — one line per command, including shortcuts, modes, and project-management helpers.

---

**Last Updated**: Template
