# Triage Native Memory Entries

A one-time-per-repo sweep. Read each entry in this repo's native memory store, decide which `.project/` home the fact belongs in, file it there, and drop what carries no value.

This file is not a command and not a skill. Reference it directly when you are ready to triage.

## Before you start

Re-run `scripts/init-project.sh` in this repo — **plain, not `--force`**. It merges any missing registers and scripts without touching user data. Several repos predate the feedback and execution registers and have no `adr/`, `product/`, or filing scripts; the re-init adds them.

## Find the native memory store

The harness keeps a per-project memory directory at `~/.claude/projects/<project-path-slug>/memory/`. The `MEMORY.md` index in that directory lists the entries with one-line descriptions. Read the index first; read individual entries only when the description does not tell you enough to route.

The harness recreates this directory after deletion, so cleaning it once does not keep it clean.

## Route each entry

For each entry, decide which home it belongs in. The density bar and the boundary between homes are in `.project/execution/README.md` — read it once before routing any entries. It names all five homes and what belongs in each.

File through each home's own rules, not through the register's:

- **Decision** → `.project/adr/README.md` for the format, `.project/scripts/adr.sh new <slug>` to file. The **Why** section is required. If you cannot reconstruct a genuine Why from the memory note, it is not a decision record — file a ticket in the pack repo (`agentic-project-init`) instead, since a fact important enough to record but with no reconstructable reasoning is evidence of a missing home.
- **Promise** → `.project/product/README.md` for the format, `.project/scripts/product.sh new <slug>` to file.
- **Pack-prompt correction** → `.project/feedback/README.md` for the format, append to `.project/feedback/ENTRIES.md`.
- **Execution fact** → `.project/execution/README.md` for the format, append to `.project/execution/ENTRIES.md`.
- **Project context** → `CLAUDE.md`. Add it where it fits.

Never hand-mint an id. If `adr.sh` or `product.sh` is missing, the repo needs the re-init above.

## What does not fit

An entry that is genuinely important and fits none of the five homes is evidence of a missing home. That becomes a ticket against the pack repo (`agentic-project-init`), not against the repo being triaged — the homes are pack concerns.

An entry that carries no value — stale, redundant, or too vague to act on — is dropped. No record of the drop is needed.

## Provenance

Every entry the triage files carries a `Source:` line:

```
**Source:** migrated from the native memory store, triaged YYYY-MM-DD.
```

This keeps agent-written and owner-migrated entries distinguishable in the log.
