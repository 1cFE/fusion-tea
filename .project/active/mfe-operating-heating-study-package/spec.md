# MFE operating-heating study package

Status: Approved for implementation under T-017.

## Problem and authority

[NEED] The owner requested remediation of `.project/reports/20260907-fusion-model-audit.md` through run-goal and said “yes ground and proceed.” [INHERITED] T-017 at `392219a8` routes current package migration after the independently audited WI-050 repair (`work/active/WI-050_mfe-coherent-operating-heating/audit.md@55456198`). The current study adapters and metadata still describe the former heating interface. The native model handoff names the outstanding consumers.

## Requirements and success criteria

All implementation requirements below are [INFERRED] from the audited interface and existing native study contract. They remain agent decisions.

- [ ] SC-1: The current route publishes the audited operating-heating channels and all 18 individual assertions. The independent oracle adapter binds all assertion operands correctly, including four scalar efficiency assertions, installed-capacity sustainment and signed burn hold. Actual baseline/reserve/demand controls agree with the independent oracle at the existing tolerance.
- [ ] SC-2: Current metadata and manifest identities derive through existing native producers and reproduce without changes. Exact assertion identities, 247 public inputs, 28 feature references, reachability and unreachable sets derive from the current generated graph. Historical records remain at their own identities.
- [ ] SC-3: Actual package-dependent consumer tests pass, including the four modules named by the model handoff and relevant route tests. Missing-binding, altered-channel and verdict-mismatch failures remain effective. No test silently skips required TEAx execution or substitutes stale fixture metadata.
- [ ] SC-4: The audited model, generated package, retained evidence, historical studies and shared tooling remain unchanged. The annex describes the current interface and remaining limitations. A fresh independent coding audit certifies this scope before integration.

## Scope and limits

Own current package metadata/manifest, `studies/oracle_entry.py`, `studies/study_route.py`, `studies/ANNEX.md`, affected `tests/study/` modules/fixtures and a package-local metadata helper if the existing producer requires a caller. Reuse stock metadata, identity, loader, store, verifier and indicator APIs. A derived identity is preparation, not candidate promotion. Do not change model arithmetic, finance, scope, thresholds, historical studies/discovery rows, generated code or shared producer implementations. Return a prerequisite if those are needed.

Explicit spec/design reviews are skipped for this migration to a separately audited interface. Actual current-route tests and fresh coding audit supply the relevant independent checks. Native stages use the exposed delegation interface per `.agentic-mbse/codex.md`.
