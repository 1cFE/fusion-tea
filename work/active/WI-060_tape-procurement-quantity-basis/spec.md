---
Status: active
Scale: standard
Epic: null
Owner: codex
Created: 2026-09-15
Updated: 2026-09-15
---
# WI-060: Tape procurement quantity basis

## Problem and supported use

[NEED] Conductor procurement must follow physical tape inventory as geometry, current, reference pack current density and selected conductor envelope vary. The entering model prices ampere-metres independently of reference-density-driven tape volume. Source: owner request captured in work/orchestration/goals/tape-procurement-consistency/goal.md.

## Requirements

- R1 [NEED] Use one traceable dimensionally consistent tape quantity and compatible procurement price basis; distinguish tape length, composite-conductor length and pack-material volume.
- R2 [NEED] Define the supported physical mechanism of a reference-density change and identify alternatives; preserve assumptions and source provenance.
- R3 [NEED] Apply envelope quantity scaling exactly once.
- R4 [NEED] Preserve explicit non-tape material and winding-operation boundaries and existing feasibility semantics.
- R5 [NEED] Explain design-point cost change without tuning to the prior total.
- R6 [NEED] Verify native/model contract, generated implementation and independent oracle at reference and relevant off-design points; leave a study-ready reproducible package.
- R7 [INHERITED] Preserve source quarantine, library/design separation, canonical/twin synchronization, runtime seal and native validation/traceability. Required reading: knowledge/holdout/aries-cs/PROTOCOL.md; modeling_project/REQUIREMENTS.md and MODELING_GUIDE.md.

## Scope and validation

[INFERRED] One coherent native model item covers the material/procurement/grade interfaces and design parameters, generated package and affected independent oracle/consumer tests. Study execution remains a native goal task after integration. Detailed pack/casing fit, absolute critical-current margin and new manufacturing effort are outside this correction.

[INFERRED] Source/math and interface review precede implementation. Test proportional inventory/cost responses to density, envelope, geometry/current, tape dimensions and price; test invalid domains; verify fresh generation and canonical/twin equality; run affected model and study consumers and native integration gates. Compare against the immediately entering package at ccb6d843e79af0e1bb9c2c6eb4d5f0b33ce690f8.

## Preparation checklist

- [x] Preserve entering package identity and matched comparison data before production mutation.
- [x] Record source-backed basis and concrete design, enumerate affected consumers, obtain independent source/math/interface review.
- [x] Implement and validate the reviewed correction; register verification and traceability through native PM.
- [ ] Independently audit integrated outcome and prepare committed package for integration. Independent implementation PASS is recorded; T-004 integration exposed the missing snapshot refresh, now tracked in goal T-005.
