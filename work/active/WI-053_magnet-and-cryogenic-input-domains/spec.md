---
Status: active
Scale: standard
Epic: standalone
Owner: native-modeling-author
Created: 2026-09-13
Updated: 2026-09-13
---

# Magnet and cryogenic input domains

The two existing calculations can return physically reversed values or divide by zero for invalid clearance or temperatures. Users need deliberate local invalid-input rejection, distinct from an evaluated engineering failure.

[INHERITED] Alignment and scope come from `work/orchestration/goals/fusion-audit-remediation/trail.md`, Round 8 and T-034, and `evidence/T-034_domains/author-brief.md@5c5dd1cc`. The bounded repair prioritization is agent judgment under the owner's enclosing remediation authorization. Original counterexamples and source authority are in `evidence/T-028_assessment/f01-f07.md`, F07. No new source values are adopted.

- MR-053-1 [INHERITED]: Conductor Peak Field SHALL reject live clearance R_in−a_coil_in <= 0 and reference clearance R_ref_in−a_coil_ref_in <= 0 deliberately before bore arithmetic, through the supported calculation and native plant routes.
- MR-053-2 [INHERITED]: Cryoplant Electrical Power SHALL reject violations of 0 < T_cold < T_amb deliberately before COP arithmetic.
- MR-053-3 [INHERITED]: Valid arithmetic, reference/baseline outputs, signed diagnostics, dormant and additive direct-power controls, existing finance and public formals SHALL retain their meanings.
- MR-053-4 [INFERRED]: Regression evidence SHALL include original negative/equality clearances, zero/negative/reversed/equal temperatures, independent valid identities and affected full-plant execution, with issue-level attribution of existing failures.

The calculation definitions, family twins, native executable completion and focused tests are in scope. Consumer/oracle and shared-tool work belongs to the coordinator's separately scoped task. Broader F07 domains, calibrated geometry bounds and engineering feasibility remain unresolved. No study, integration, pin, historical rewrite or closure is part of this item. Source/Ref/Basis citations and plain Real conventions follow MR-3/MR-4 and AD-001/AD-004.
