# Model Architecture

Structural decisions about how the domain is decomposed into model packages. These are the architectural choices that shape the model ecosystem — decisions that outlive any single work item and that new work must respect.

*Previous decisions (AD-001 through AD-005) archived to `archive/modeling_project/ARCHITECTURE.md`.*

**Scope.** This file owns *model*-architecture decisions, numbered `AD-XXX`. Repository, orchestration, and tooling decisions are numbered `ADR-NNN` and live in `.project/adr/` (see its `README.md`). An `ADR-NNN` citation resolves there; an `AD-XXX` citation resolves here.

---

## AD-001: Plain `Real` for All Numeric Values

**Decision**: Use `Real` for all numeric values. Document units in doc comments.

**Rationale**: Custom monetary unit definitions (for $, $/MWh, $/J) are complex and untested with syside's quantity arithmetic. Getting the structure right matters more than compile-time unit checking for this first modeling pass.

**Trade-off**: No compile-time dimensional analysis. Mitigated by doc comment conventions per MR-4.

**Upgrade path**: When MFE modeling begins and the library is shared more broadly, typed quantities can be added as an enhancement.

**Origin**: WI-006 DD-1

---

## AD-002: `attribute def` Bundles Parameter Metadata

**Decision**: Bundle value/min/max/sensitivity into a reusable `attribute def 'Economic Parameter'`. Each parameter is an attribute of this type with `:>>` feature redefinition for setting values.

**Rationale**: Machine-readable metadata (not just doc comments). Supports future programmatic access to ranges and sensitivities for Monte Carlo or sensitivity analysis via codegen.

**Alternative rejected**: Simple `Real` attributes with ranges only in doc comments — not machine-readable, can't be validated or iterated programmatically.

**Origin**: WI-006 DD-2

---

## AD-003: Closed-Form DCF for LCOE Calculation

**Decision**: Express Hawker's DCF as a closed-form ratio using present value factors, implemented in a single `calc def`.

**Rationale**: SysML v2 calc defs do not support iteration/looping. The closed-form is mathematically equivalent to the year-by-year sum (geometric series) for constant annual cost/energy streams, which is exactly Hawker's model structure.

**Verified**: `(1+d)**n` exponentiation parses correctly in syside.

**Origin**: WI-006 DD-3

---

## AD-004: Library Subdirectory Organization

**Decision**: Three subdirectories under `models/library/`: `foundation/`, `cost_structure/`, `analyses/`.

**Rationale**: Follows MODELING_GUIDE.md package structure convention. Separates concerns: base types → domain structure → calculations. Scales to future additions (MFE parameters, additional analyses).

**Origin**: WI-006 DD-4

---

## AD-005: CAS Hierarchy as Typed Part Def Specializations

**Decision**: Each CAS level 2 account is a `part def` specializing `'CAS Account'` which specializes `'Costed Component'`. Scope classification via `'CAS Scope'` enum attribute.

**Rationale**: Type-safe — downstream users instantiate `'CAS22 Power Core'`, not a generic account with a string code. The specialization hierarchy mirrors the CAS tree. Scope classification as enum (not doc comment) is queryable.

**Alternative rejected**: Single generic `'CAS Account'` with string code — no type safety.

**Origin**: WI-006 DD-5

---

## AD-006: Parameters Separate from Calculation

**Decision**: `ife_cost_parameters.sysml` defines the 14 parameters with metadata. `ife_lcoe.sysml` defines the calculation. The calc def takes 14 `Real` inputs, not an `'IFE Cost Parameters'` part.

**Rationale**: The calc def is pure math — it doesn't need to know about the parameter metadata (ranges, sensitivities). This separation means the calc can be reused with any parameter source (including concept-specific values that override defaults). WI-007 wires them together.

**Origin**: WI-006 DD-6

---

## AD-007: Magnet System Defined in the Library, Not the Design Layer

**Decision**: The MFE `'Magnet System'` costed component and the MFE-divergent CAS22 sub-account types (22.1.3 magnets, 22.1.4 heating/current-drive, 22.1.8 divertor) are concept-agnostic `part def`s in `models/library/cost_structure/mfe_power_core.sysml` — not design-layer types as the IFE epic placed its subsystems.

**Rationale**: MR-3's own example states "a magnet system definition works for any MFE concept," so it belongs in the concept-agnostic library. The magnet system is fully parameterized (B, R0, r_coil, G, coil_markup, cost_per_kAm) with no concept values; WI-011 binds tokamak/stellarator values via `:>>`. This is a deliberate, more MR-3-consistent choice than the IFE precedent.

**Alternative rejected**: Placing the magnet system in the design layer (IFE precedent) — would duplicate the definition per concept and understate its concept-agnostic nature.

**Origin**: WI-009 (registered 2026-07-13)

---

## AD-008: Physical Structure in `library/structure/`; Definitions Own Their Template Calcs

**Decision**: Physical, non-costed part definitions (the plasma, the first wall, the modular coil, the winding pack, the coil casing, the primary heat transport, the cryoplant, the fuel cycle, the vacuum pumping) and the interface definitions (item and port defs) live in `models/library/structure/`, a fourth library folder beside `foundation/`, `cost_structure/` and `analyses/` (AD-004). A part definition owns the template calcs whose subject it computes and imports the analysis packages it needs. Every calc output read across a part boundary is an EXPOSE attribute on the definition (`attribute B_peak : Real = peak_field_calc.B_peak;`); a value from another part enters through an input attribute the plant binds in the usage (`part magnet : 'Magnet System' { :>> r_coil_centre = rb.r_coil_centre; }`). An EXPOSE a trade study may replace is declared `default` — a swap seam — so a variant definition specializing the base can rebind it to its own calc; the instance swaps by retyping the part. Ports and `connect` statements declare the energy and material topology and are declarative for codegen. The CAS account hierarchy stays the cost view (AD-005): costed components keep their types and `capital_cost`; sub-parts are plain definitions.

**Rationale**: AD-004's folders separate base types, cost structure and calculations; physical structure is a fourth concern. Definition-owned calcs are the only placement under which a variant definition can replace a formula: a value bound with `=` on a definition is final under syside, a redefining calc usage matches parameters positionally and cannot re-bind them, and only a `default` seam is rebindable (`work/active/WI-057_stellaris-structural-decomposition/prototype/redefinition_probe/`). The arrangement is number-neutral by construction and by diff: every channel, verdict and the LCOE identical to the entering pin through a contract-derived rename ledger across three commits, and a variant's formula moves the priced LCOE only when its own facts do (`prototype/swap/results/`).

**Alternative rejected**: calcs on the plant's part usages (the pre-WI-057 form, and the prototype's Stage B) — number-neutral too, but a variant can then only relabel, never re-price; keeping physical definitions in `cost_structure/` — a category mismatch that would grow with every part.

**Origin**: WI-057 (goal `structural-decomposition` round 1, registered 2026-09-13)
