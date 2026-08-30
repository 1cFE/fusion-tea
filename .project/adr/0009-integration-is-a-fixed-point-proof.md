---
id: 0009
title: Integration is a fixed-point proof, not a transformation
date: 2026-08-26
owner: Reid W
status: active
amended_by: []
superseded_by: null
provenance: "[AGENT] 2026-08-26"
seams: []
supersedes: null
promoted_to: null
---

## Decision

The seam invokes every producing step **in place** and requires each one to change nothing. A candidate exists only for a package that is already a fixed point of the whole sequence.

Byte movement is judged by the seam's own per-file content digest over the package tree, not by git — git reports clean whatever the bytes do inside an ignored directory, which is exactly where the seam's own gate tests run. Interpreter bytecode caches are excluded, so the seam's digest judges the same file set the repository's own cleanliness gate judges.

A gate that finds movement is a `BLOCKER` naming the producer, and the tree is restored from a pre-gate backup copy before the return is written.

## Why

Integration is the hop between an audited model change and a study that can run against it. The producers that hop needs all exist and all fail closed, but some of them **mutate**: `sysml-codegen generate` rewrites the package, snapshot capture rewrites the snapshot, the manifest re-pin rewrites the manifest. A seam that owned the hop had to decide whether it performs those mutations or checks them.

Two existing constraints closed the question rather than leaving it open. The stock preflight route's sixth gate refuses a package tree that is not git-clean, and the seam may not commit (`spec.md` R-F1). So a candidate can exist only when the whole sequence moved zero bytes in the tracked tree. `spec.md` R-C6 says the same thing from the other side: failure is reported, never repaired, and a seam that regenerates to fix a stale package is repairing.

Decided during the design of GSTH Item 3 (`.project/completed/20260827_goal-integration-seam/design.md`, § Core Concept), grade delegated by the owner at Align (`align.md:8`, "just get it done — you are responsible for quality and alignment").

The alternative shape — perform the mutations, leave a dirty tree, let the operator commit — cannot return a candidate from any single invocation, because the last gate in the sequence refuses a dirty tree. It would be a two-call seam with a human commit between the calls, and one-invocation-one-return (`spec.md` R-A2) would no longer hold.

Proving is also what makes the seam cheap. It composes producers that all already exist, adds no identity scheme, and needs no rollback machinery on the success path, because on the success path there is nothing to roll back.

The consequence is counter-intuitive enough to state in the operator's own words rather than leave implied: **the seam refuses model work that has not yet been regenerated and committed.** That work belongs to the modeling item that made the change — the referent items regenerate, recapture, re-pin and commit in their own phases, *before* audit — and re-running the seam will not change the answer.

## Invariants established

- `scripts/integrate.py` — the seam itself.
- `docs/integration_seam_operator_guide.md` — states the prove-don't-perform boundary in the operator's words.
- `tests/study/conftest.py` (`integration_workspace`) and `tests/study/test_integrate_*.py`.
- `.project/completed/20260827_goal-integration-seam/design.md` — D7, D8, D19–D21 record the mechanism.

- No new identity scheme. The seam names the pin and the fingerprints the producers already compute.
- A refusal at the regeneration, census, snapshot or handwritten-preservation gate is the modeling item's unfinished work. The goal layer reads those conditions as a **prerequisite**, not as a strategy blocker.
- The return is safe to call twice: a re-run on unchanged inputs returns the prior identity or a blocker, never a second conflicting identity.
- Anyone wanting a perform-then-gate seam needs an owner ruling, because it breaks one-invocation-one-return.

## Rejected alternatives

- **The seam performs the mutations and leaves a dirty tree for the operator to commit.** No invocation could then return a candidate; it is a different, two-call contract and would need an owner ruling.
- **The seam commits.** Barred by `spec.md` R-F1; committing and closing modeling work stay with the owner and the modeling PM.
- **`git status` as the byte-movement gate.** Silently vacuous inside the gitignored test workspace — a green suite proving nothing.
- **mtime-based change detection.** Measured: 95 of a package's 153 files move mtime on a byte-identical regeneration, so any mtime detector reports a false positive on every re-run.
- **`git checkout --` plus `unlink` as the restore.** Inoperative in a gitignored tree, which is precisely where the restore test runs.
