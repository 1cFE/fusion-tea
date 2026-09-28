# Owner brief — verbatim

[OWNER-VERBATIM] Issued 2026-09-26 through `/run-goal`. Retained unchanged; the goal's contract (`../goal.md`) is derived from it.

---

A. Demonstrate usable combinations

  Start by identifying the choices the implemented models actually expose: plasma profiles, coolant arrangements, conversion systems, equipment selections
  and operating parameters.

  Then:

  - Map which alternatives have compatible interfaces and physical operating ranges.
  - Select combinations we have not already used for Stellaris or ARIES.
  - Assemble and evaluate them using existing definitions.
  - Record which combinations execute, which satisfy the evaluated engineering checks, and which require new model behavior.

  That last distinction matters. If assembling every new combination requires another custom calculation, we have found a limit in reuse. If the same
  definitions work with different partners, we have direct evidence that the usable design space expanded.

  We should not promise a steam/Brayton substitution before checking that their heat-supply interfaces and operating ranges are compatible.

  B. Test interactions between design choices

  Choose a few questions where considering one parameter at a time could give the wrong answer. For example:

  - Does the preferred recuperator effectiveness depend on the blanket’s heat-source temperatures? Recovering more exhaust heat may improve cycle efficiency
    while making it harder to accept lower-temperature reactor heat.

  - Does increasing coolant flow help enough to justify its equipment and power demands? More heat removal need not mean more net electricity or lower LCOE.
  - Does a change in plasma profile alter which equipment becomes limiting? The same downstream equipment should reveal how a core choice changes fuel-
    processing and cooling requirements.

  Run paired or small factorial studies: vary the choices together, explain any ranking reversals, and check whether the explanation survives reasonable
  assumption changes. A finding need not be surprising to a specialist; it needs to reveal something the individual component calculations would conceal.

  The stopping condition should be concrete: demonstrate several previously untested, compatible combinations without new physics definitions; characterize
  the failed combinations; and explain at least one tested interaction—or report that none was established.
