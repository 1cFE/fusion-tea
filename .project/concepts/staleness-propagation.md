# Design: Staleness Propagation in the Stage1 Analysis Loop

**Status:** Proposed
**Owner:** Reid
**Created:** 2026-04-19

---

## Overview

A fusion concept is described by a chain of derived artifacts — an analysis document, a cost-model script, a review, a synthesis, and an export consumed by a separate explorer tool. Each carries a freshness signal meant to tell a reader whether the artifact still reflects its upstream inputs. Today that signal is noise: freshly regenerated files carry stale markers, and genuinely out-of-date files look indistinguishable from fresh ones.

This design restores the signal by making it symmetric. Staleness is *set* only on downstream artifacts that were **not** regenerated in the current step, and it is *cleared* by the producer that writes an artifact from current upstream. The system stops guessing and starts telling the truth.

---

## Problem

A fusion concept's pipeline produces several artifacts with a producer/consumer relationship: the analysis document is the root, and every other artifact is derived from it (directly or transitively). When the root changes, some downstream artifacts may no longer reflect it — they are stale. The pipeline has always carried a per-artifact stale signal for exactly this purpose.

The signal has stopped carrying information. Whenever the root analysis is modified, the pipeline stamps every downstream artifact as stale — including artifacts that were regenerated from the new root in the very same step. At the same time, regenerating a downstream artifact does not clear the stamp: a producer writes a fresh file and leaves the stale marker from the prior generation in place. The result is that freshly derived artifacts carry "stale" markers, and genuinely out-of-date artifacts look no different from fresh ones. A reader — human or automation — cannot tell which state a given artifact is actually in, so the signal gets ignored or worked around, which defeats its purpose.

The cause is a missing distinction. The pipeline knows when the root moved, but it has no record of whether a given downstream moved with it. Propagation treats every root change the same, regardless of what the caller just regenerated, and there is no symmetric operation when a producer writes a fresh artifact. Both halves of the signal — set and clear — must become conditional on what was actually regenerated, for the signal to be worth reading again.

---

## Goals

- Make the stale signal trustworthy: if an artifact is marked stale, it really is out of date.
- Make regeneration restore freshness: the act of writing an artifact from current upstream declares it fresh, immediately and durably.
- Keep downstream artifacts visibly stale when the root changes but they do not.
- Support the standalone feedback flow where the root is edited without regenerating anything downstream.
- Let the status display read the signal directly, without heuristics or workarounds.

## Non-Goals

- Automatic regeneration. The signal informs; it does not trigger work.
- Content-based freshness (hashes, timestamps, upstream identity). Deterministic marker-on-artifact is sufficient.
- Detecting out-of-band hand edits to the root analysis document. A human edit outside the sanctioned commands is out of scope.
- Multi-step cascade logic beyond direct downstream propagation. If the root moves, all downstream below it are stamped in one call; no ordered chain of partial invalidations.

---

## Design Principles

### 1. Producer owns freshness

The component that writes an artifact is responsible for declaring its freshness. That covers both sides: writing a fresh file clears any prior stale marker on the same path; leaving a file alone while its upstream moves leaves the stale marker for someone else to set. Freshness is not a separate concern bolted on after the fact — it is part of the write.

### 2. Propagation is scoped by what was just regenerated

A blanket "stamp all downstream" propagation is always wrong, because it does not know what the caller just wrote. Every propagation call must name the set of artifacts regenerated in the current step, and exempt them. When the caller cannot name that set, the propagator cannot run.

### 3. Markers live with the artifact

The freshness state of an artifact is recorded on the artifact itself, not in an external store. This keeps the signal visible in diffs, survives file moves, requires no registry, and lets any reader inspect the state with a single file read. The cost is three marker formats (one per artifact kind); the benefit is zero synchronization debt.

### 4. The caller declares intent

No global defaults, no implicit downstream lists, no "usually you mean these three files." The component invoking propagation must pass both the reason for the staleness event and the set of artifacts it just regenerated. A propagator with implicit knowledge is a propagator that silently drifts.

---

## Architectural Bets

- **Explicit regeneration set over implicit defaults.** Every propagation call is auditable at the call site — no hunting through the library to figure out what gets stamped.
- **Producer-owned clearing over a separate sweep.** Write-and-declare-fresh is a single operation. There is no later step that could forget.
- **Marker-on-artifact over a metadata registry.** Three small format conventions (one per artifact kind) beat one shared database that everyone has to keep in sync.
- **No content-based freshness.** The system accepts that out-of-band hand edits are invisible; in exchange, it stays deterministic, grep-able, and simple.

---

## Core Model

*Register shifts here — identifiers and field names are welcome below.*

### Artifact

A file in the canonical concept directory that has a defined producer and a defined set of upstream inputs. The set of tracked artifacts: `analysis.md` (root), `model_setup.py`, `review.md`, `synthesis.md`, and the explorer JSON export. Per-iteration `iter-N/` files are *not* artifacts in this sense — they are immutable history.

### Artifact graph

Derivation relationships, read as "depends on":
- `model_setup.py` ← `analysis.md`
- `review.md` ← `analysis.md`, `model_setup.py`
- `synthesis.md` ← `analysis.md`, `review.md`
- explorer JSON ← `analysis.md`

For the purpose of in-loop propagation, all four are treated as direct downstream of `analysis.md`; finer-grained edges (review → synthesis) are future work.

### Producer

The code path that writes an artifact: loop steps (`_run_cold_start`, `_run_feedback_pass`, `_run_model_in_iteration`, `_update_canonical_files`) and standalone commands (`cmd_analyze`, `cmd_model_setup`, `cmd_review`, `cmd_synthesize`, plus the explorer extractor). Every producer owns its artifact's freshness on successful write.

### Regeneration set

The set of artifacts the current step successfully wrote to their canonical location. Passed explicitly to the propagator. Inside the loop: always includes `analysis.md` after the analyze step; includes `model_setup.py` only when `_update_canonical_files` promoted it (i.e. `model_ok=True`). Outside the loop: `analyze --feedback` passes `{analysis.md}`; the other standalone commands do not propagate at all.

### Staleness marker

The format-specific token carried on the artifact: `# STALE: {reason}` as the first line of a `.py`; `Stale: true` / `Stale-Reason: {reason}` in the YAML frontmatter of a `.md`; a `{num}.json.stale` sidecar next to the explorer JSON. One marker per artifact; no marker means fresh.

### Staleness propagator

A single function: given (reason, regeneration_set), stamp every downstream artifact in the canonical directory that is **not** in the regeneration set. Idempotent — already-stamped files stay stamped. Never touches artifacts listed in the regeneration set.

---

## Diagram

```
                  analysis.md  (root)
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
 model_setup.py    review.md      explorer JSON
                       │
                       ▼
                  synthesis.md

Propagation rule on root change, given regenerated = R:
  for node in {model_setup, review, synthesis, explorer}:
    if node not in R: stamp(node)
```

---

## Required Invariants

### Propagation
- The propagator never stamps an artifact whose path is in the caller's regeneration set.
- Inside the loop, the regeneration set always includes `analysis.md` and includes `model_setup.py` iff the just-completed iteration had `model_ok=True` (i.e. `_update_canonical_files` actually promoted it).
- Standalone `analyze --feedback` calls the propagator with regeneration set = `{analysis.md}` — every other downstream gets stamped.

### Clearing
- A producer that successfully writes artifact X must clear X's stale marker as part of the write — not in a later step, not conditionally on a flag.
- `_update_canonical_files` clears the canonical `model_setup.py` stale marker iff it promotes the iter-N copy (`model_ok=True`). When `model_ok=False`, it neither promotes nor clears.
- `--force` on a standalone producer implies clearing the marker (the write happens, so clearing follows from the producer rule).

### Source of truth
- An artifact's freshness is `not has_marker(path)`. No external registry, frontmatter field on the root, or heuristic is consulted.
- The status-display reader reads the marker only. It never infers freshness from iteration counts, timestamps, or verdicts.

---

## How It Works

### Scenario 1 — In-loop iteration reaches PASS

Analyze regenerates `analysis.md`. Model-setup regenerates `iter-N/model_setup.py` with `model_ok=True`. `_update_canonical_files` promotes the iter-N copy to canonical **and clears the marker** on canonical `model_setup.py`. Assess writes the verdict. The propagator is called with regeneration set `{analysis.md, model_setup.py}`, so it stamps only `review.md`, `synthesis.md`, and the explorer JSON. PASS exits. Canonical `model_setup.py` is fresh; review/synthesis/explorer are correctly flagged as needing rework.

### Scenario 2 — In-loop iteration with `model_ok=False`

Analyze regenerates `analysis.md`. Model-setup fails (`model_ok=False`). `_update_canonical_files` does **not** promote; canonical `model_setup.py` is whatever it was before the iteration, derived from an older `analysis.md`. The propagator is called with regeneration set `{analysis.md}`. It stamps `model_setup.py` (correctly — it no longer matches the new root), along with review, synthesis, and explorer.

### Scenario 3 — Standalone `analyze --feedback`

The user edits `analysis.md` via the feedback path; no downstream artifact is regenerated. The command calls the propagator with regeneration set `{analysis.md}`. Model-setup, review, synthesis, and explorer JSON are all stamped. This matches what has always been intended for this flow.

### Scenario 4 — Standalone `model-setup --force` on a stamped file

The command writes a fresh `model_setup.py` and, as part of the write, clears the `# STALE:` line. No propagation runs — nothing upstream changed. Other downstream artifacts retain whatever marker they had; their freshness is their own producers' responsibility.

### Scenario 5 — Standalone `review --force` with a fresh root

The command writes a fresh `review.md` with `Stale: false` in its frontmatter. No propagation. Synthesis and explorer JSON are unaffected.

---

## Edge Cases and Failure Modes

- **Out-of-band hand edits to `analysis.md`.** No producer runs; propagator not invoked; downstream appears fresh when it is not. Acknowledged gap. Users editing the root directly must follow with the feedback path or a regeneration pass. Not worth detecting automatically in v1.
- **Explorer JSON regenerated by the explorer pipeline.** That pipeline is a producer; it must delete its own `.stale` sidecar on write. Non-compliant producers silently re-introduce the original bug in their slice.
- **Review-to-synthesis edge.** If `review.md` is regenerated without the root changing, `synthesis.md` should become stale (it depends on review). The current propagator is root-keyed only; this transitive edge is future work. Flagged, not blocking.
- **`--force` semantics.** `--force` skips the exists-check *and* implies clearing the marker, because the write happens. There is no separate "force but leave marker" mode.
- **Model script writes but model run fails (standalone).** The `.py` is still fresh; the marker clears on write. The run failure is orthogonal to file freshness.
- **Missing artifact.** If a downstream artifact doesn't exist on disk, the propagator skips it (idempotent). Creation freshens it via its producer.

---

## Vocabulary

- `artifact` — a file in the canonical concept directory with a defined producer and upstream inputs.
- `root` — `analysis.md`; the upstream of all other tracked artifacts.
- `upstream` / `downstream` — positions in the artifact graph.
- `producer` — the code that writes an artifact; owns clearing on write.
- `regeneration set` — artifacts successfully written to their canonical path in the current step; passed to the propagator as an exemption list.
- `staleness marker` — the format-specific token carried on the artifact itself (`# STALE:` line / `Stale: true` frontmatter / `.stale` sidecar).
- `propagator` — the function that stamps non-regenerated downstream when the root moves.
- `fresh` — predicate "artifact has no marker." The only freshness signal in the system.

---

## Validation Strategy

- **Regression — PASS iteration leaves canonical fresh.** Run the loop end-to-end with the fake-Claude harness; assert canonical `model_setup.py` does not begin with `# STALE:`.
- **Regression — failing iteration marks canonical stale.** Force `model_ok=False`; assert canonical `model_setup.py` begins with `# STALE:` after the iteration.
- **Regression — PASS iteration stamps review/synthesis.** Pre-seed `review.md` and `synthesis.md`; after PASS, assert `Stale: true` in both frontmatters.
- **Unit — propagator respects regeneration set.** Call `propagate_staleness(reason, regenerated={model_setup.py})`; assert `model_setup.py` is untouched.
- **Unit — producers clear on write.** Pre-stamp each artifact kind; invoke its producer; assert marker gone.
- **Unit — standalone feedback stamps everything.** Run `analyze --feedback` with all four downstream present; assert all four are stamped.
- **Smoke — clean-tree audit.** After a full pipeline run on the test concept, grep for `# STALE:` / `Stale: true` / `.stale` — none should appear on artifacts that were part of the regeneration set at the final step.

---

## Next-Stage Handoff

**Settled here:**
- Producer-owned clearing is the contract; no separate "clear_staleness" step.
- The propagator takes an explicit regeneration set; no implicit defaults.
- Marker-on-artifact is retained (three formats, one per kind).
- In-loop regeneration set: always `{analysis.md}`; add `model_setup.py` iff `model_ok=True`.
- Out-of-band hand edits to the root are acknowledged as a known gap, not a v1 problem.

**Spec/design detail still needed next:**
- Exact signature for the propagator (positional regeneration set or keyword? path objects or names?).
- Enumeration of every producer call site and the clearing step to add there.
- `--force` semantics written into each standalone command consistently.
- A small helper for stripping the `# STALE:` line and the `Stale:` frontmatter field without corrupting surrounding content.
- Decision on whether the review-to-synthesis transitive edge is in scope for this change or deferred.

**First risk to de-risk:**
- Marker-stripping correctness. Each marker format has whitespace/position subtleties (first-line `.py` comment, YAML field ordering, sidecar file deletion). A small focused test battery on the strip helpers should land before anything else, because every producer depends on them.

---

## Summary

The pipeline conflated two distinct conditions — "upstream moved" and "downstream is out of date" — and collapsed them into a single unconditional stamp, with no symmetric clear. This design separates them: the propagator takes a regeneration set and only stamps artifacts outside it; every producer clears its own marker on write. The signal becomes accurate by construction, the in-loop bug disappears as a special case, and the standalone feedback flow keeps working unchanged.
