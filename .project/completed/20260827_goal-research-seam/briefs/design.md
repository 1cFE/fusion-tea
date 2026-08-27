# Brief → /_my_design — goal-research-seam (GSTH Item 2)

Design the native research acquisition and registration seam against the approved spec.

## Authoritative inputs

- `.project/active/goal-research-seam/spec.md` — the approved contract. Its four return classes, requirement grades, and decide/defer split are settled; do not relitigate requirements.
- `.project/active/goal-research-seam/align.md` — owner rulings.
- `.project/active/goal-research-seam/spec-review.md` — review + resolutions, for context on why requirements read as they do.
- `.project/research/20260822-120756_research-extraction-harness.md` §5 — reusable patterns P1–P10.

## Your job: take a position on every deferred question (spec § Open Questions)

1. **Manifest identity mechanism** `[OWNER-delegated to design: "make sure you use your judgement"]` — content hash vs URL key vs push-through-Zotero. Justify against duplicate detection (R-B3), Zotero compatibility (R-B1c), and re-fetch/verify provenance (R-B5). Record as an ADR candidate (R-F2: filed to Item 1's ADR home at coordination time — do not create that home).
2. **Entry surface location** — command vs skill vs script for both the standalone registration op (R-B0) and the research surface (R-C1). The upstream symlinked `/research` must not be edited in place.
3. **Request/return artifact homes and formats** — including where the R-D5/R-D6 durable negative lives and how a later invocation finds it by request. Respect the two-PM rule.
4. **Holdout content-scan mechanics** — the minimum in-code check before a registry write (R-D1/R-D2/R-D4). PROTOCOL.md's barred set is the source; be precise about what is scanned and what matches.
5. **Rollback implementation** — staging vs transactional order vs compensating delete, across the three artifacts (source dir, index block, manifest row); satisfy R-B8 atomicity.
6. **Limit enforcement** — prompt text vs counted by the surface (R-A2/R-A5). Lean-first: don't build machinery the first build doesn't need, but the limit must end the invocation inside the contract.
7. **Negative-result lifetime and override** — what a caller does to legitimately re-search (R-D6's recorded override reason).
8. **Slug/title derivation** for URL sources and collision behavior against `resolve_slug`.
9. **Fixture shape for the offline chain proof** (R-E1/R-E2) — how a fixture URL exercises extract→holdout→register without network (injected raw artifact, stubbed capture boundary, or local server). Verify what `agentic-mbse extract` actually allows before choosing; do not design against an imagined interface.

## Hard rules

- **Verify before designing on it.** Read the actual code: `scripts/zotero_ingest.py`, `scripts/zotero_lib.py`, `agentic-mbse` extract CLI (`~/1cfe/agentic-mbse/src/agentic_mbse/cli/extract_cli.py` — read-only; it is pinned, changes are upstream filings), `run_analysis.py add-source` rollback referent, `knowledge/holdout/aries-cs/PROTOCOL.md`, the WI-031 index blocks (`knowledge/SOURCE_INDEX.md:190-218`). The spec's two verified writer defects (no manifest row on local-PDF path; missing index anchor) need explicit design positions (R-B1a/b).
- **No fallbacks.** Never design default/fallback values for missing inputs; a missing required input is a `BLOCKER` return, not a guess. (Standing owner rule.)
- **A workaround that maintains an invariant by hand is a bug**, not a design element — if you hit one, flag it, don't formalize it.
- **Prototype cheap, not speculative**: if a design choice hinges on how `extract` behaves on an edge (e.g., file:// URLs, `--save-source` layout), run it once against a scratch dir and record the observed behavior rather than assuming.
- Stay out of Item 1's files (CLAUDE.md, run-study runbook, DISCOVERY_LOG, GOAL_RUNBOOK, ADR home). Cite the epic, not Item 1's in-flight artifacts.
- Include a test design: how R-E1..E6 are realized (test files, fixtures, which existing suites are the affected regressions).
- Working-voice: plain, decomposed, every decision with its reason and rejected alternative.

Write `design.md` at `.project/active/goal-research-seam/design.md`. End with `ARTIFACT: <path>`.
