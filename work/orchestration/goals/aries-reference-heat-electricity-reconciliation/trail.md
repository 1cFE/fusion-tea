# Trail: ARIES reference heat-to-electricity reconciliation

Append-only, newest entry last, ISO dates. No entry is edited in place; corrections are dated amendments. Native artifacts own execution evidence; entries cite them.

## Round 1 — replay-contract-attribution

### Strategy revision — 2026-09-25

- **Approach:** reproduce the historical source-conditioned cases against the current package; write the reference-case contract from primary page images and have each new source reading independently checked; declare the materiality budget with focused review; then commit one diagnostic study on the unchanged package that isolates candidate causes one at a time (recuperation, cycle flow, exchanger conductance, hot-side bounds, auxiliary-load definitions) and in combination, before any model change.
- **Assumptions:** the current package reproduces the frozen numbers up to recorded input differences; Lyon Table IV and its text supply a complete electrical boundary (thermal, gross, recirculating, net); the sequential closure exposes enough branch-level transferred/unmet heat and temperatures to locate the thermal inadequacy.
- **Abandonment conditions:** the replay differs from frozen evidence for reasons not explained by recorded input differences; primary pages do not support a consistent target; a needed comparison quantity cannot be expressed on the current package without a model change (that work moves to a later round); an owner gate or a declared cap.
- **Intended model increment:** none; the package stays pinned this round.
- **Intended study question:** which single justified assumption changes, and which combination, account for the unmet heat and the gross/net difference against the Lyon reference when the published fusion power is supplied and hardware is held fixed?

### T-001 scope

- **Objective:** establish the current-package baseline for the four canonical scenarios and record entry preservation.
- **Why now:** grounding shows the live scenario runner sets pump modes the frozen study did not; the historical table cannot be adopted until reproduced against the actual package.
- **Scope:** read-only replay of the `run.py` scenarios and the frozen-study variants into a scratch directory; channel extraction and comparison with `results/cases.json@8e6fb2f2`; entry preservation manifest. No package, model, frozen-record or study writes.
- **Inputs:** `goal.md`; `exploration/aries_integrated/run.py@96914299`; the frozen record; `evidence/build-preservation-manifest.py`.
- **Done when:** every canonical case is reproduced, or its difference from the frozen record is attributed to a recorded input difference, with branch-level heat/temperature and ledger channels tabulated for the source-conditioned cases.
- **Stop when:** the package cannot load through the documented runtime (mechanical), or a reserved gate binds.

### T-001 start — 2026-09-25

T-001 · current `aries_integrated` package through the documented `.codex-test/run` runtime, outputs in scratch · `evidence/replay-canonical.py` and `evidence/t001-replay-summary.json`. Coordinator executes directly.
