# Policy: how to build a sane, consistent, coherent 1 GWe LCOE estimate

**Date**: 2026-06-06
**Author**: Claude (with Reid)
**Scope**: `costingfe` `.forward()` semantics → rules for the 1 GWe headline number
**Companion**: `.project/research/20260606-093951_override-scaling-semantics-by-account-class.md` (the step-by-step mechanics), `2026-05-30-1gw-scaling-and-override-interpretation.md` (prior)

---

## The goal and the decision (read this first)

Every concept gets **one** comparable number: LCOE for a **1 GWe NOAK plant**. The
goal is an **honest attempt at a low LCOE** by scaling the concept up to that
1 GWe total.

We anchor every concept on a **real, published design point** at its native scale
(`P_native`). Because of that, the way we reach 1 GWe is a **decision, not a cost
optimization**: we **replicate** the real design point into a fleet of identical
modules — we do **not** extrapolate the physics model to a single, hypothetical
1 GWe monolith we have no design basis for.

So "is monolithic or replicated cheaper?" is **not a question we ask.** We always
replicate. (Monolithic scale-up is a possible future mode — see the note at the
end — but only once we trust the physics model to scale to 1 GWe.)

This doc states (1) what each flavor of `.forward()` means, by cost class, and
(2) the rules for assembling the fair, coherent, modular 1 GWe number.

---

## Part 1 — The two knobs, and the flavors of `.forward()`

`.forward()` has two size knobs:

- **`net_electric_mw`** — the **whole plant's** net electric output.
- **`n_mod`** — how many reactor **modules** the plant is built from.
- The model derives **per-module power = `net_electric_mw / n_mod`** and computes
  every cost line for *one module at that power*, then combines.

| call | meaning | per-module power | used? |
|---|---|---|---|
| **`forward(net=P, n_mod=1)`** | one reactor of size `P` — the **design point** / native machine | `P` | yes — `generic_reference`, native |
| **`forward(net=1000, n_mod=N)`**, `N = round(1000/P)` | **REPLICATED** 1 GWe: a fleet of `N` modules, each still size `P` | `P` | **yes — the headline** |
| **`forward(net=1000, n_mod=1)`** | **MONOLITHIC** 1 GWe: one extrapolated 1000 MWe reactor | 1000 | **no — future work only** |

`run_native_and_1gw()` runs the design point (native) and the **replicated**
projection, with overrides on. The replicated projection **is** the headline.

---

## Part 2 — The three cost classes

What `n_mod` does to a line depends only on its physical class.

### Class S — Shared / fixed (amortizable)
**Accounts:** CAS10 (site, permits, licensing), CAS21 (buildings), CAS28 (digital
twin), CAS40 (owner's costs / pre-op staff), CAS70 (O&M staff).
**Nature:** a **site** needs these once, however many modules it runs. A fleet
shares the buildings, licence, control room, and operating crew.
**In the library:** computed per module and **not** multiplied by `n_mod` — so the
replicated route **charges them once**. That single charge *is* the amortization
that gives a small machine its fair shot.

### Class U — Per-unit (replicate + learn)
**Accounts:** CAS22 reactor-island sub-accounts `C2201xx` (blanket, coils,
structure, heating, vacuum, remote handling…), and CAS80 fuel.
**Nature:** one per module. `N` modules → `N` reactor cores.
**In the library:** multiplied by `n_mod`. Going modular forgoes the
economy-of-scale of one big core; `noak=True` credits **mass-production learning**
(many identical units get cheaper) as the offset.

### Class P — Power-proportional (size-invariant per MWh)
**Accounts:** CAS23 (turbine), CAS24 (electrical), CAS25 (misc), CAS26 (heat
rejection), CAS27 (special materials), plant-wide CAS22 sub-accounts
(`C2202xx`–`C2207xx`: cooling, waste…).
**Nature:** scale with the **total** plant power.
**In the library:** value is the same whether you replicate or not (verified —
CAS24 = 126.3 either way). No ambiguity.

---

## Part 3 — What replication does, per class (concept 24, 5 MWe → 1 GWe)

Replicated projection (`forward(1000, 200)`), library defaults, no overrides:

```
class  account              value ($M)   what replication did
S      CAS21 buildings           138.4   charged ONCE (the fixed-building floor), amortized over 1 GWe
S      CAS40 owner's               1.4   charged once
S      CAS70 O&M                   2.4   charged once
U      CAS22 reactor island      594.5   200 cores (x n_mod), with NOAK learning
P      CAS23 turbine             296.5   scales to 1 GWe total
P      CAS24 electrical          126.3   scales to 1 GWe total
-----------------------------------------------------------------------------
       TOTAL CAPITAL            2046.6
       LCOE                       20.98  $/MWh
```

This is the honest-low modular estimate: the **Class-S shared costs are amortized
across the whole fleet** (charged once, not 200×), Class-U cores are built `N`
times with learning, and Class-P scales with output. Every number traces back to
the **real native design point** — nothing is extrapolated.

---

## Part 4 — The rules

### Rule 1 — Always replicate. (No route choice.)
The 1 GWe headline is **always** `forward(net=1000, n_mod=round(1000/P), noak=True)`.
We never use the monolithic flavor for the headline. The reason is physical
realism, not cost: the specs are a real design point at `P_native`, so a fleet of
that real module is defensible, whereas a 1000 MWe monolith is an extrapolation we
have no design basis (or validated physics) for.

### Rule 2 — Let each class fall where it lands in the replicated run
- **Class S (shared):** the library charges these **once** — keep it that way.
  This is the amortization. Do **not** multiply a shared cost by `n_mod` (a fleet
  does not build 200 separate control rooms); doing so is always wrong and
  catastrophic to LCOE.
- **Class U (per-unit):** these multiply by `n_mod` — correct, you build `N`
  cores. Keep `noak=True` so mass-production learning is credited (this is what
  offsets the loss of single-core economy of scale; without it the modular
  penalty is unfair).
- **Class P (power-proportional):** scales to the 1 GWe total automatically.

### Rule 3 — Write overrides in the modular frame, by class
Every relative override `M * generic.costs.X` (with `generic` at native) means
**"M of the library's natural answer for that account in the replicated 1 GWe
fleet."** Concretely:

| you override… | the value you write is… | the framework then… |
|---|---|---|
| a CAS22 sub-account `C2201xx` (U) | **one module's** M$ | multiplies by `n_mod` → fleet total |
| a power-proportional top-level CAS23–26 (P) | native-frame M$ or `M * generic` | scales by `n_mod` → `M *` = M of the full plant |
| CAS21 buildings (S, top-level) | the **once-charged** shared M$ | uses it as-is (not replicated) |

**Anchor the rationale to the same frame as the value.** Under the modular
decision, the baseline is *"the library's default for a fleet of this device,"*
**not** *"a conventional 1 GWe monolithic plant."* Writing a value against the
native `generic` while justifying it against a monolithic plant is the silent
inconsistency this investigation surfaced — and under the always-replicate policy
the monolithic baseline simply does not exist, so don't invoke it.

---

## Part 5 — Summary recipe

For every concept:

1. Build the design point at `P_native` (real specs) → `generic_reference`.
2. Headline = `run_native_and_1gw(...)` → the **replicated** 1 GWe projection,
   `noak=True`. No route choice.
3. Write overrides in each account's class frame (Part 4, Rule 3); keep every
   rationale's baseline on the modular fleet, not a monolith.
4. Leave Class S charged once, Class U replicated, Class P scaled to total.

Result: a 1 GWe estimate that is **fair** (small machines amortize shared costs
over a fleet and get NOAK learning on the units), **coherent** (one architecture —
modular — applied to every account), and **consistent** (override values and
rationales share the modular baseline), and that is **anchored entirely to a real
design point**.

---

## NOTE — Future mode: monolithic scale-up (needs validation first)

A second way to reach 1 GWe is the **monolithic** flavor, `forward(net=1000,
n_mod=1)` — extrapolate the single machine to one 1000 MWe reactor. It would change
the answer in two ways: shared facilities (Class S) get sized for a real 1 GWe
plant rather than charged at the module floor, and the reactor island (Class U)
gets single-core economy of scale instead of replication. For concept 24 the
monolithic route gives LCOE **27.88** vs the replicated **20.98** — but the point
is **not** the number; it is that the two are different *architectures*.

We are **not** using this mode yet, for one reason: **we do not yet trust the
physics model to scale a real design point up to 1 GWe as a single unit.** The
power balance back-solves fusion power, driver energy, etc. at 1000 MWe, and that
extrapolation is unvalidated for these concepts. Before monolithic scale-up can be
offered as an option it must be **tested and validated** — confirm the power
balance and the per-account scaling laws stay physical from `P_native` to 1 GWe,
per concept archetype.

Related open item: even within the replicated route, the Class-S shared facilities
are charged at the **module-scale fixed floor** (e.g. CAS21 ≈ 138 M$). Whether a
1 GWe fleet's shared infrastructure should be larger than that floor is a sizing
question whose only principled answer (size it for the 1 GWe site) runs through the
same monolithic forward — so it, too, waits on the scale-up validation above.
(Also: CAS40/CAS70 are not overridable today — `1cFE/1costingfe#106`.)
