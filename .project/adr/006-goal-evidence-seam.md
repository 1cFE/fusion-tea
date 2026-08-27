---
status: accepted
date: 2026-08-25
deciders: [Reid W]
grade: "[OWNER] 2026-08-23"
supersedes: none
amends: CLAUDE.md:73
---

# ADR-006: Goal artifacts may cite `.project/` by path and digest; each PM is still mutated only through its own operations

## Context

The repository runs two project-management systems — the coding PM in `.project/` and the modeling PM in `work/` — and CLAUDE.md tells agents "**CRITICAL: Do not cross-reference between them.**" (`CLAUDE.md:73`). The goal layer lives in `work/orchestration/` and needs to cite coding-PM artifacts as evidence; existing practice already did so, in the WI-029 orchestration brief. The owner ruled the seam on 2026-08-23 (`.project/concepts/goal-strategy-task-harness-design-review.md` § Resolutions, "Goal evidence seam (P5)").

## Decision

Goal input references may cite `.project/` artifacts **by path and digest**, and the reverse direction is equally permitted. Each PM remains mutable only through its own native operations.

The digest is `<path>@<commit-sha>` for tracked artifacts — git already supplies a content digest, so no new mechanism is needed. Where a native hash does not exist, the citation says so rather than inventing one:

- **Study stores** (gitignored `_work/`): cite the committed record directory `@<sha>`, whose `snapshot.json` carries the resolved store identity, fingerprints, and tool and oracle source digests. The native record is the hash.
- **R2-synced research binaries** (gitignored): cite the tracked extracted markdown `@<sha>`, whose frontmatter carries `content_hash_sha256:` for direct extractions.
- **Anything with no native hash**, including `knowledge/MANIFEST.jsonl` entries: cite by path with the words "unpinned; no native digest" in the citation, so a reader can see the citation pins nothing.

Citing is not mirroring. No goal artifact copies or restates the other system's state.

## Rationale

The blanket ban was written to stop the two PMs' *state* from being mirrored, which is a real failure — two records of one work item that disagree. It was not written to stop evidence from being read across. Read as written, it forbids the goal layer from citing the very artifacts it exists to reason about, and it already contradicted committed practice.

The digest is what makes a citation honest. A path alone says "look over there"; a path plus a commit sha says which version was read. Reserving mutation to native operations is what keeps the ban's original purpose intact.

## Rejected alternatives

- **Mirrored PM state** — the failure the original ban was aimed at, and still forbidden.
- **A blanket citation ban** — forbids evidence along with mirroring, and contradicts existing practice.
- **A goal-layer digest scheme for untracked evidence** — that is a mechanism the hardening bar covers; the citation says "unpinned" instead.

## Affected seams

- `CLAUDE.md:73` — the "do not cross-reference" rule, amended to "do not cross-reference *state*" with the citation permission and this record named.
- `work/orchestration/GOAL_RUNBOOK.md` — how a citation is written.
- Both PMs' operations, which are unchanged.

## Consequences

The citation digest is read by a *person*, to see which version was cited. It is not the authority digest on the hardening path (ADR-003), which a *procedure* compares to decide whether work is still authorized. Same word, different function — and the goal layer's invariant is explicit that no goal procedure compares or recomputes a cited digest.

That reconciliation of two owner texts is an `[INFERRED]` reading, challenged by re-deriving it against the hardening table, not by re-asking the owner. The digest requirement itself stays owner-graded.
