# Learnings: cryo-volume-basis

What this run now knows.

Append-only, newest last, ISO dates, never edited in place. An entry is appended **only after** a round review has accepted or corrected the delta the round result proposed (`GOAL_RUNBOOK.md` § The fresh review). Mechanical failures produce no learning.

Each entry is one claim.

## L-001 — `total_kAm` is a cost proxy, not a count of winding ampere-turn-metres

- **Evidence:** `models/library/analyses/mfe_magnet_cost.sysml@8f3b510c:44` — `total_kAm = G * B * R0 * r_coil / (mu0 * 1000.0)`, with `G = 78.95683520871486` equal to `8π²` to all printed digits. The calc therefore factorises exactly into `I_link × L_proxy`, where `I_link = 2πR₀B/μ₀` is the Ampère's-law current linking the magnetic axis and `L_proxy = 4π r_coil` is a stand-in length built from the coil **bore** radius, which falls out of the radial build (`models/designs/stellarator_09/stellarator_plant.sysml@ba5c9945:138-139`; the binding itself is `models/designs/generic_mfe/mfe_plant.sysml@ba5c9945:51,320` — `r_coil = rb.r_coil`). At the Stellaris design point `I_link = 5.71500e8 A`, `L_proxy = 37.6991 m`, and the product is `2.15450e7 kA·m`. Round 1 review recomputed the factorisation independently.
- **Scope:** the MFE magnet cost calc as built, at any design point. The factorisation is algebraic, not a fit, so it does not depend on the Stellaris values. It says nothing about whether `L_proxy` is a good cost proxy — only that it is not a winding length.
- **Implication:** any strategy that wants a conductor volume or a conductor length out of this package must supply a winding length. The package carries none: neither coil count nor coil circumference nor `J_eng` appears anywhere under `models/` (grep, re-run at review).
- **Supersedes:** `none`.
- **Accepted by:** round 1 review, 2026-08-26. Accepted as proposed.

## L-002 — Ampère's law on the magnetic axis is a lower bound on modular-stellarator coil current, not an estimate of it

- **Evidence:** substituting Stellaris's own winding geometry — 48 coils (`stellarator_plant.sysml@ba5c9945:570` doc, raw.pdf sec. 2.9) at a 25 m typical circumference — gives total ampere-turn-metres `I_link × 25 m = 1.42875e10 A·m`, and DI-010's sourced REBCO band 112–124 A/mm² (`knowledge/KNOWLEDGE.md@ffa5c54c` DI-010) yields **127.57 / 121.08 / 115.22 m³** at 112 / 118 / 124, against the geometric anchor 136.56 m³. Reproducing the anchor needs **104.62 A/mm²**, below the sourced band. Read the other way, the winding packs carry **7.0 % to 18.5 %** more ampere-turn-metres than the axis-linking law accounts for. All figures recomputed at round 1 review.
- **Scope:** modular stellarator coil topology, at this design point and this sourced band. **The physical reading is this round's inference, not a sourced result** — that a modular quasi-isodynamic coil set's shaping currents largely do not link the axis is the most plausible explanation for the residual's sign and size, and no source in the repository states it. It is agent-grade and is challenged by re-deriving against the arithmetic above, not by asking the owner. Not established for tokamak TF coils, where the axis-linking law is closer to the whole story.
- **Implication:** a cold volume computed from carried quantities lands *below* a geometric anchor by roughly the size of the effect being modelled, so the tolerance must be wide — the honest band is 7.0–18.5 %, and the upper end is the one that sets it. A tight tolerance is obtainable only by calibrating a form factor at the design point, and a value calibrated to the point it is validated against cannot be validated.
- **Supersedes:** `none`.
- **Accepted by:** round 1 review, 2026-08-26. Accepted with a correction: the proposal stated the residual as "7–18 %", rounding its own upper bound down, and did not mark the modular-shaping-current explanation as an inference. Both corrected above.

## L-003 — the case for computing this volume is arm B, not arm A

- **Evidence:** arm A's held 136.56 m³ carries an independent double cross-check in its own doc (`models/designs/stellarator_09/stellarator_plant.sysml@ba5c9945:570` — each winding-pack side² equals turns × (20 mm)² against the Table 8 turns row; the no-casing masses 128.7 t × 8 = 1029.6 t over 136.56 m³ imply 7539 kg/m³, consistent with the Table 7 material mix), where the ampere-turn route is a provable lower bound (L-002). Arm B's 390 m³ is a hand ratio taken off arm A's held number — `136.56 × (118/21.5) × (4.69/9.0)` at `exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/study.py:38-42`, with the arm key at `:44-47`.
- **Scope:** this comparison and this package.
- **Implication:** the goal's answer should be argued on what computing does for the comparison — arm B's volume deriving from the same formula at Nb₃Sn's own `J_eng` and ceiling field, instead of being a hand ratio anchored on arm A — not on arm A's accuracy. A round that argues it on arm A's accuracy is arguing the weaker case.
- **Supersedes:** `none`.
- **Accepted by:** round 1 review, 2026-08-26. Accepted as proposed.
