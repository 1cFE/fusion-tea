---
Status: active
Created: 2026-09-25
Updated: '2026-09-25'
---

# Plan — network heat-driven closure

Related Artifacts: spec.md; design.md. Owner: goal coordinator (author); fresh reviewers for design and implementation. Preserve concurrent edits; use `.codex-test/run` for all Python/modeling commands.

- [ ] Write spec/design with the MR-7 role table, equations, migration and validation plan; obtain fresh independent design review (goal `evidence/design-review.md`).
- [ ] Add `Network Heat Driven Closure` definition and completion; rebind the assembly's `heat_exchangers` part with `network_mode` (default 0) and `pbli_split_fraction`; leave the reviewed definition in place.
- [ ] Build on the stock route (`exploration/aries_integrated/build.py`, evidence path updated to this item), verify fixed-point regeneration, run the development checks (a)–(f), write the migration report.
- [ ] Re-pin the live study manifest; run scoped validation; check the goal preservation manifest and isolated Stellaris replay.
- [ ] Obtain fresh independent implementation review of executed behaviour (mode-0 exactness, mode-1 network, split pair, MR-7 compliance).
- [ ] Hand the coherent package to the goal for the integration seam and one committed study.

| Acceptance | Verification | Evidence |
|---|---|---|
| R1 | Mode-1 outputs published and traced through turbine/recuperator/ledger at C3 inputs; scratch-check agreement | development receipts |
| R2 | Mode-0 replay of 4 canonical + 27 sealed points, all 546 outputs ≤ 1e-12 relative, verdicts exact | migration report |
| R3 | Split triple 0.55 / 0.85 / 0.98 at fixed hardware: PbLi unmet falls from ≈ 197 to ≈ 56 MW, divertor unmet appears at 0.98; helium stage binds in mode 1 at C3 | development receipts |
| R4 | Preservation manifest and Stellaris replay | goal evidence |
| R5 | Fixed point, migration report, re-pinned manifest, CANDIDATE | build receipts, integration return |
| R6 | Refusals and closure diagnostics | development receipts |
