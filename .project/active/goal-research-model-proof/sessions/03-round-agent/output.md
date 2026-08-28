Round 1 is open, T-001 ran and returned, and the trail stops at a handoff. One file written: `work/orchestration/goals/p-pump-basis/trail.md`. No commits, no writes anywhere else.

## What the task found

**Outcome: `COMPLETE`.** The repository does support a sourced `p_pump` — but a narrower claim than DI-008 makes.

**The value.** At the baseline point on the comparison pin, `p_pump` = **203 MW** as a held scalar (6.279 % of the model's computed `p_th`), or **210 MW** if made a computed fraction and closed self-consistently. Against the held 1.0 MW that is ~200×. So the first half of the goal's question has an answer: 1.0 MW is not defensible for a helium-primary loop at this scale.

**Only one of DI-008's three figures actually answers the question.** Read at their cited lines:

- **Cismondi 2017** is the one — same paragraph carries both the blanket-deposited power and the helium pumping power, for a loop at 80 bar, matching Stellaris's 8 MPa helium. Ingested, unregistered.
- **ARIES-ACT does not apply.** Its blanket is self-cooled LiPb; the helium is *divertor* coolant. Its 1–2 % is not a helium-primary-loop datum.
- **Moscato is not in the repository** — the only helium-primary pumping-system *design*, and the only source that would give a band rather than a point.

**So DI-008's 2–6 % band is not supported by what the repository holds.** One point, one source. This bears directly on the 60–190 vs 30–190 discrepancy the grounding session logged: the 30 MW end is the ARIES-ACT leg, and that leg is coolant-mismatched.

**The denominator moved.** DI-008 says "blanket thermal power," but the model has no blanket-only channel, and `mn·p_neutron` is not that quantity (0.96 × `p_fus`, against DEMO's blanket deposition at 1.173 × `p_fus`). The model's `p_th` less recovered pumping heat is 1.178 × `p_fus` — a 0.5 % match to the source's denominator. So the fraction goes on `p_th`.

**Effect, and its limits.** A hand reconstruction from the committed `p_fus` channel reproduces the study's own baseline `rec_frac` (0.1514) and `p_net` (915.1 MW) exactly, so it is checked. At 203 MW, `rec_frac` goes 0.151 → 0.330 (η 0.333) and 0.116 → 0.242 (η 0.47); `p_net` falls 18.5 % / 11.6 %. No verdict flips at baseline. It does *not* say where the `recirc_ok` fence moves, and LCOE is not hand-derivable — `p_th` feeds nine cost accounts directly, so a package run is still needed.

## Decisions

Four goal-level decisions, each with the five fields, in the return. In short:

- **D-1, denominator → `p_th`** — execution detail, round agent, nothing changed.
- **D-2, the band is not natively supported** — **premise surprise**, surfaced to the owner, not resolved. It cuts against DI-008, which the strategy declared it works against.
- **D-3, scalar vs computed shape** — reserved gate 2, referred. Both forms reported with their arithmetic.
- **D-4, nothing landed, no source registered, no item minted** — reserved gates 3 and 4 plus the general gate, referred.

## Dispositions proposed

- **`20260821-power-cycle-ab#3`** — `model fix`, routed to this goal, not yet answered. Its "~100×" is really ~200×. No work item minted; that is a `work/` write under the general gate.
- **`#5` and `#10`** — touched by the reconstruction, already disposed, already routed outside this goal. No new row proposed, with the reasoning stated so the checkpoint reviewer can disagree with the judgment rather than have to spot it.

## Stop

`handoff`. The checkpoint on this reading and these dispositions needs a fresh session — this one authored them. Two things also point at the owner directly: the D-2 premise surprise, and the three reserved gates the answer now runs into.