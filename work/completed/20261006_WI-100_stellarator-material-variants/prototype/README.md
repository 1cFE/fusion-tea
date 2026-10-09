# WI-100 prototype — probes P1–P5 (design § 7)

Run 2026-09-30 by the T-015 implementer, before the build, on scratch copies in the session scratchpad (WI-057 prototype discipline). No repository model tree, twin, package or study was touched. Sources to re-run are in `sources/`; generated evidence is in `evidence/`.

| Probe | Question | Outcome | Fallback |
|---|---|---|---|
| [P1](P1-cross-part-seams.md) | Do plant-definition consumers follow rebound cryoplant seams and the owner-qualified `winding_cost` read? | **Pass** on all five reads | none; H6 not applied |
| [P2](P2-double-retype.md) | Two sub-part retypes in one copied instance | **Pass** for the retypes; **refused** for any package with two or more `'MFE Power Plant'` instances (`REGISTRY_CLASS_NAME_COLLISION`) | K21: per-instance packages from the same staged tree |
| [P3](P3-def-level-literals.md) | Are def-level literals in the specializations entry keys? | **Emitted** (`rebco_law_enabled`, `inventory_enabled`, and K10's `intercept_demand_available`) | none; the route refuses the two final keys (K11) |
| [P4](P4-conditional-calc.md) | Does `'REBCO Shape Branch'` auto-implement? | **No**; the `if` form is refused at exact-route validation | the design's handwritten fallback body, with the equation in the def doc |
| [P5](P5-per-case-time.md) | Per-case time for three plants | about 1.5 s per plant; one plant per case after the P2 fallback | K21 (taken for P2's reason) |

A preview of the § 1.5 regression ran on the same scratch tree: the hunked reference alone, at the pin's 704 inputs plus the three new keys at their neutral defaults, reproduced all 1,352 pin outputs and 67 verdicts bit for bit, with exactly one added output (`magnet__conductor_current__evaluation_defined = 1.0`) and exactly the three declared new entry keys. The build repeats this in the repository and records it under `../build/regression/`.

No probe produced a refusal that the design's stated fallbacks cannot absorb. The P2 fallback is a structural change to the package layout (three packages, three manifests, three seam pins), recorded in `../implementation-notes.md` for the coordinator.
