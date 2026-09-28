# Owner direction after round 2 — 2026-09-26

[OWNER-VERBATIM]

> The return-condition check found a missing physical requirement. Documenting it does not establish that the reported operating points satisfy it.
>
> The problem is clear in the check file (work/orchestration/goals/design-study-parameters/evidence/return-condition-check.md):
>
> - The loop requires helium to return at 561.94 K.
> - The starting case returns it at 513.12 K, almost 49 K too cold.
> - The best case is much closer, but still differs by 0.70 K.
> - The table still labels these cases "passing" because the implemented checks omit this requirement.
>
> "More consistent" is not the same as satisfying the loop balance. The claim of a 171 MW improvement also compares against a starting configuration that does not satisfy that balance.
>
> Two conclusions in the handoff therefore go too far:
>
> - "The boundary points are exactly consistent" needs an executed, verified boundary point. The listed cases do not demonstrate one.
> - "Without reordering it" does not establish that the ranking survives enforcing the requirement. Adding a bypass changes the flows through the exchanger and can change its performance.
>
> The next step should be a small continuation of this goal:
>
> 1. Choose how the loop maintains its return temperature: through consistent operating settings, or through an explicitly modeled bypass/control arrangement.
> 2. Enforce that relationship in the calculation and checks. Do not choose a physical tolerance simply to admit the observed residual.
> 3. Re-evaluate the starting configuration and leading alternatives, refining the study near the relevant boundary.
> 4. Recompute the performance and cost comparison using cases that satisfy the completed loop model.
>
> The numerical verification and seal are useful, but they certify agreement with the implemented equations. They do not resolve this missing relationship.
