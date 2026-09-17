# Stellaris reference oracle input mapping

Status: active. Owner: Codex. Created: 2026-09-16. Scope: bounded prerequisite repair.

[INHERITED: work/orchestration/goals/stellaris-reference-reconciliation/goal.md@5dd9cbd0] The owner requires native/package/oracle agreement for source-conditioned reconstruction and off-reference cases. Study preparation discovered that native public profile exponents and volume shaping have no mapping in the package-owned independent oracle seam; the existing oracle already implements those parameters.

[INFERRED] Add only direct qualified mappings for `plasma__alpha_n`, `plasma__alpha_T` and `plasma__f_shape` to existing oracle inputs of the same names. Keep fail-closed unknown-key behavior and all equations/defaults/criteria. Correct the obsolete cache comment: all profile-integral arguments are cache keys, so varying them remains exact.

[INFERRED] Verify each changed public input reaches the independent calculation, default behavior is unchanged, input overrides do not leak between calls, and the upcoming native study agrees across exact-profile and geometry cases. Independent mapping/control review precedes execution. Native study/result ownership remains in `work/` and `exploration/`; this coding record owns only `oracle_entry.py` and its focused regression test.
