---
Status: active
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-09-03
Updated: '2026-09-03'
---

# WI-039: Heating System Structure — the wall-plug to plasma-coupled power chain as real model structure

Minted at the close of goal `operating-point-closure` (2026-09-02) as one of two escape routes; grounded and scoped under goal `wall-and-heating`, round 1 (`heating-chain-first`), task T-002 (`work/orchestration/goals/wall-and-heating/trail.md` § T-002 scope). The owner reserved no gates for this goal and re-ruled the delegation for it `[OWNER 2026-09-03, ruling 5]`; merge, push, and work-item close remain owner-held. Requirements below are outcome-level — mechanism is deferred to design.

**A note on this item's title.** The minted name — "Sources, Transmission, Launchers" — describes rubric Row 4's **S3** cost anchor. That is **not this item's bar.** R4.S is already scored 2 and 2 is its written target; R4.**P** is scored 1 against a written target of 2. This item closes the *physics* gap. S3-shaped cost splitting may be built where the engineering genuinely wants it, but it is not required, and S2 must not be broken reaching for it (see MR-WI039-6).

## Why this item exists

Rubric Row 4's physics cell grades **1** against a written target of **2** (`.project/active/demo-depth-rubric/grading.md@fc80e5b2` cell R4.P). The grader's reason, and the author's agreement with it, are on the record:

> "the row's P2 anchor requires a computed wall-plug → coupled-power *chain*; a held ratio dividing one held constant inside another subsystem's sum derives nothing, and no chain element exists as a model object." (`grading.md` § Disagreement records, G1 / R4.P)

And the grader's own statement of what would close it:

> "P2 needs a computed wall-plug → coupled-power chain with a stated deposition assumption verified in execution; no such calc def exists (the seam would need at minimum a heating-chain calc whose output re-derives when efficiencies or delivered power change independently)." (`grading.md` cell R4.P, `why_not_next`)

The P2 anchor, verbatim, from the frozen rubric (`rubric.md@dc0f0b6d` Row 4): **"Wall-plug → coupled-power chain computed with a stated deposition assumption, verified."**

Heating is not a bookkeeping detail in this model. Two committed studies measured installed heating power moving the sustainment fence: 0 of 240 points feasible at the printed 50 MW, 87 of 192 at 110 MW. The quantity that decides feasibility is currently a held constant divided by another held constant, inside a sum belonging to a different subsystem.

## Current state

- **`p_input = 50.0`** — installed **plasma-coupled** heating power, held (`models/designs/stellarator_09/stellarator_plant.sysml:636-638`). The WI-037 correction in its doc comment is explicit that this is coupled power, not wall-plug, and that `sustainment_ok` compares it coupled-to-coupled (`:1122`).
- **`eta_pin = 0.5`** — held (`:648`). Its doc comment already records the factorisation: `eta_source_ecrh 0.50` (`costing_constants.yaml:105`) `x eta_couple 1.0` (`steady_state_stellarator.yaml:15`). **The factors exist in the source; they do not exist in the model.**
- **The only heating arithmetic in the entire model:** `p_input_in` added into `p_th` (`models/library/analyses/mfe_power_balance.sysml:117-121`) and `p_input_in / eta_pin_in` inline inside the `recirculating` sum (`:136`). That inline division is the whole "chain".
- **Cost:** `'Heating Cost'` (`models/library/analyses/mfe_account_costs.sysml:196`), a linear per-method sum; ECRH-only mix with NBI/ICRF/LHCD zeroed (`stellarator_plant.sysml:821-845`), `heating_ecrh_per_mw = 5282900.0`, `p_ecrh = 50.0`. Runtime: `heating_cost__cost` = $264.145M = 5282900 x 50 exactly. **This cell is at target and works.**
- **Structure:** `part def 'Heating and CD'` (`models/library/cost_structure/mfe_power_core.sysml:138`) carries `capital_cost` and nothing else. The heating system has no physics attributes of any kind.
- **The oracle mirrors the model's own form** — `verify_stellaris.py:391-392` computes `recirculating` with the same inline `p_input / eta_pin`. Parity against it today would be a tautology.

## What must be true afterward (requirements)

#### MR-WI039-1: The heating chain exists as a computed chain of model objects
The model SHALL carry a heating-power chain in which wall-plug electrical power, the source (wall-plug → delivered) stage, the coupling/deposition stage, and plasma-coupled power are **separately named quantities** related by executed arithmetic, such that the chain's outputs re-derive when any efficiency or any power in it changes independently. *Priority:* P0. *Rationale:* the P2 anchor and the grader's stated `why_not_next`. *Validation:* a fresh grader can point at the chain elements by path and line; perturbing one efficiency changes the dependent outputs in execution. *Source:* `rubric.md@dc0f0b6d` Row 4 P2; `grading.md@fc80e5b2` R4.P and G1.

#### MR-WI039-2: The lumped `eta_pin` is replaced by its factors, and no factor is invented
The chain SHALL use the factors the pinned source actually publishes — a per-method source efficiency (`eta_source_ecrh = 0.50`, ITER gyrotron procurement basis, `defaults.py:104-108` / `costing_constants.yaml:105`) and a per-concept coupling efficiency (`eta_couple = 1.0`, `steady_state_stellarator.yaml:15`) — and SHALL NOT introduce any additional stage carrying a number that no admissible source publishes. *Priority:* P0. *Rationale:* the pinned 1costingFE defines `eta_pin = eta_source x eta_couple` and **nothing else**; there is no transmission-efficiency figure in it, so a three-stage chain would require inventing one. *Validation:* every efficiency in the chain resolves to a source citation under MR-4, or to MR-WI039-3. *Source:* MR-4; `goal.md` § Invariants ("a missing input is surfaced with options, never defaulted").

#### MR-WI039-3: The deposition assumption is stated, not defaulted
`eta_couple = 1.0` SHALL be carried as an **explicitly stated assumption** — named in the model text with what it asserts (that all delivered ECRH power couples to the plasma), why it is defensible for this concept, and what would change if it were not 1.0 — or replaced by a sourced coupling figure. It SHALL NOT remain a silent inherited default. *Priority:* P0. *Rationale:* the P2 anchor's words are "with a **stated** deposition assumption"; a default that nobody wrote down is not a stated assumption, and this is the single most likely way to build the chain and still miss the anchor. *Validation:* the assumption is legible in the model's doc comments and surfaced in the design as a named judgment. *Source:* `rubric.md@dc0f0b6d` Row 4 P2; goal `wall-and-heating` § T-002 scope, narrower constraint (i).

#### MR-WI039-4: The power balance consumes the chain instead of doing the arithmetic inline
`recirculating` SHALL consume a computed wall-plug heating power from the chain rather than performing `p_input / eta_pin` inline (`mfe_power_balance.sysml:136`). *Priority:* P0. *Rationale:* the grader's objection is precisely that the only arithmetic is "a held ratio inside another subsystem's sum"; leaving the division where it is leaves the objection standing however much structure is added elsewhere. *Validation:* the inline division is gone; `q_eng` and `rec_frac` still execute and their baseline values are explained (unchanged, or changed with the reason shown). *Source:* `grading.md@fc80e5b2` G1.

#### MR-WI039-5: Verification is independent, not a mirror
The independent oracle (`exploration/stellarator_e2e/verify_stellaris.py`) SHALL compute the heating chain **itself**, from the same inputs, by its own arithmetic — not by re-using the model's generated form. *Priority:* P0. *Rationale:* the anchor's last word is "verified", and a parity check between two copies of the same expression verifies nothing. The oracle today mirrors the model's inline division (`:391-392`). *Validation:* the oracle's chain is written independently and agrees with the model at the baseline within the established tolerance. *Source:* `rubric.md@dc0f0b6d` Row 4 P2 ("verified"); goal § T-002 scope, narrower constraint (ii). **Flag for promotion to PR-XXX:** "an independent check that re-uses the checked expression is not a check" is a durable project rule, not a WI-039 fact.

#### MR-WI039-6: The cost cell stays at its target
`'Heating Cost'` SHALL continue to follow installed heating power with its source basis, and the baseline heating capital SHALL remain explainable against the committed $264.145M (unchanged, or changed with the derivation shown). *Priority:* P0. *Rationale:* R4.S = 2 is **at** its written target; a physics increment that breaks a met cost cell trades a gain for a loss. *Validation:* `heating_cost__cost` at the baseline, derived and stated. *Source:* `grading.md@fc80e5b2` R4.S.

#### MR-WI039-7: The library stays concept-agnostic
Chain definitions SHALL live in `models/library/`; ECRH-specific values, the concept's coupling assumption, and the heating mix SHALL live in `models/designs/stellarator_09/`. *Priority:* P0. *Rationale:* MR-3. *Validation:* no concept value appears in a library file. *Source:* MR-3; AD-004.

#### MR-WI039-8: Every value is sourced, and no fallback is introduced
Every quantitative value SHALL carry a `Source`/`Ref`/`Basis` citation resolving to a repository file or the pinned 1costingFE (`0254385`). Where an input is missing, it SHALL be surfaced with options — never defaulted, never filled with a family average or a literature typical value. *Priority:* P0. *Rationale:* MR-4 and the owner's standing ruling. *Validation:* traceability audit over the changed elements. *Source:* MR-4; `goal.md` § Invariants.

#### MR-WI039-9: Entry-point changes are restated across the committed studies, never silently broken
If this item retires or restructures `p_input`, `p_ecrh`, or `eta_pin` as settable entry points, the affected committed studies — `20260901-sustainment-fence` and `20260903-priced-levers`, both of which swept the `p_input`/`p_ecrh` tie declared in `manifest.json` — SHALL be **restated**, in the MR-WI037-7 / MR-WI036-11 shape, **before** regeneration, with every changed expectation **re-derived from live evidence** rather than patched to match. *Priority:* P0. *Rationale:* the last two entry-point retirements each cost roughly 30 fixture re-derivation sites, and a fixture patched to match a new number is not evidence of anything. *Validation:* the restatement exists and names each affected study, fixture, and expectation with its derivation. *Source:* `goal.md` § Invariants (comparison-meaning stake); `operating-point-closure` L-006.

#### MR-WI039-10: The sustainment requirement is not tuned
`sustainment_ok`'s violated baseline (90.6 MW required against 50 MW installed) SHALL NOT be resolved, relaxed, or fitted by this item. *Priority:* P0. *Rationale:* it is the disclosed, explained W-form fidelity residual, and this item changes what installed power costs and how it reaches the plasma — not what the plasma requires. *Validation:* the fence's form and its baseline verdict are unchanged, or any change is disclosed and explained. *Source:* `goal.md` § Invariants; `operating-point-closure` L-001/L-005.

#### MR-WI039-11: The wall-load fence is untouched
No element of the wall-load chain (`wall_load_calc`, `wall_area`, `wall_load_limit`, `wall_load_ok`) SHALL be changed by this item. *Priority:* P0. *Rationale:* goal `wall-and-heating` round 1 § T-002 scope exclusion (1) — the wall research (T-001) returned this round, and acting on it here would move comparison meaning mid-round and put one round's study on two questions. *Validation:* the diff touches no wall-load element. *Source:* goal § T-002 scope.

## Scope boundaries

**In scope.** A heating-power chain definition in `models/library/analyses/` (the natural home is alongside or inside the power-balance analysis; the design chooses); the `'Heating and CD'` part def in `models/library/cost_structure/mfe_power_core.sysml:138` gaining the physics attributes the chain needs, if the design wants the chain to hang off the costed component; the instance bindings and concept values in `models/designs/stellarator_09/stellarator_plant.sysml`; the `recirculating` term in `models/library/analyses/mfe_power_balance.sysml:136`; the oracle's own independent chain in `exploration/stellarator_e2e/verify_stellaris.py`; the study-fixture restatements MR-WI039-9 requires.

**Out of scope.** The wall-load fence (MR-WI039-11). Solving *required* heating from the plasma's response, or a port/coupling/geometry limit pushing back — that is Row 4's **P3**, which the rubric states rides on Row 1's confinement closure and which is not this item's bar. Separate cost accounts for sources, transmission and launchers (R4.S3), and replacement logic for heating components — buildable if the engineering wants it, but not required and not at the cost of MR-WI039-6. Current drive: the concept is ECRH-only with no current drive, sourced (`stellarator_plant.sysml:821-837`), and this item does not add one. Fueling and plasma control, which share Row 4's title but have no representation to extend and no grade gap identified against them. `p_pump`, `eta_p`, and the other recirculating terms.

## Success criteria

**Functional.** The chain's elements exist as named model objects with wall-plug power, the two efficiency stages, and plasma-coupled power all addressable; the model regenerates through the pinned codegen and executes at the baseline; changing an efficiency or a power in isolation changes the dependent outputs.

**Quality.** SysML validation levels pass per the **model-validation** skill; `tests/models` and `tests/study` green; traceability audit clean over the changed elements.

**Verification.** The oracle computes the chain independently and agrees at the baseline; `heating_cost__cost` is derived and stated (MR-WI039-6); `q_eng` / `rec_frac` at the baseline are stated as unchanged or explained; every changed committed-study expectation carries its derivation (MR-WI039-9).

**Grade.** The goal's § Answered when (a) is measured by a **fresh non-author** re-grade against `rubric.md@dc0f0b6d` from a pointer-only evidence map — not by this item and not by its author. This spec's job is to make the anchor's full text pointable.

**SV entries.** To be created at design time, when the chain's shape is fixed and the checkable quantity is known. Creating an SV row against a mechanism that does not exist yet would be a guess.

## Assumptions & risks

1. **The chain is two-stage, not three.** *Confidence: high.* The pinned source publishes `eta_source` and `eta_couple` and no transmission figure. A transmission stage would need a source; there isn't one, and MR-WI039-2 forbids inventing it. **Risk if wrong:** none to the grade — the anchor names a chain, not a stage count.
2. **`eta_couple = 1.0` can be defended as a stated assumption rather than sourced.** *Confidence: medium.* It is the pinned source's own per-concept value for ECRH, and MR-WI039-3 requires it be written down as an assumption with its reasoning. **Risk if wrong:** a grader reads "stated deposition assumption" as requiring a sourced coupling figure. *Mitigation:* state it fully and visibly; if the design judges it insufficient, surface it as an option rather than defaulting past it.
3. **Retiring `p_input` as an entry point is the expensive part, not the physics.** *Likelihood: high. Impact: high.* Two committed studies swept the `p_input`/`p_ecrh` tie. MR-WI039-9 governs; the design decides how much entry-point restructuring is actually needed, and the cheapest honest option is a legitimate answer.
4. **The baseline `q_eng` may move.** *Likelihood: low. Impact: medium.* If the chain reproduces `p_input / eta_pin` exactly, nothing moves. If the design's structure changes the arithmetic at all, `q_eng`, `rec_frac`, and every study expectation resting on them move with it. Disclosed and derived, never fitted.

## Traceability

**Upstream.** `rubric.md@dc0f0b6d` Row 4 (P2 anchor, S2 anchor, and the row's target note); `grading.md@fc80e5b2` cells R4.P / R4.S and grader note G1 with its disagreement record; goal `wall-and-heating` `goal.md` § Answered when (a) and § Invariants, `trail.md` § Round 1 strategy revision and § T-002 scope; DI-002 (CAS22.1.4 is MFE-divergent); MR-3, MR-4; AD-001, AD-004, AD-006.

**Source basis.** Pinned 1costingFE `0254385`: `defaults.py:96-108` (per-method installed-power rates; `eta_pin = eta_source x eta_couple`; `eta_source_ecrh = 0.50` on an ITER gyrotron procurement basis), `costing_constants.yaml:105`, `steady_state_stellarator.yaml:15` (`eta_couple = 1.0`), `layers/cas22.py:446-459` (C220104). Concept basis: `stellaris-design-details.md` Table 2 image (required plasma-coupled ECRH power 50 MW; ECRH-only, no current drive).

**Downstream impacts.** `models/library/analyses/mfe_power_balance.sysml` (`recirculating`, and every consumer of `q_eng` / `rec_frac`); `models/designs/stellarator_09/stellarator_plant.sysml`; the generated package and its `manifest.json` entry points; `exploration/stellarator_e2e/verify_stellaris.py`; committed studies `20260901-sustainment-fence` and `20260903-priced-levers` under MR-WI039-9; `tests/models` and `tests/study` fixtures.

## Open decisions (for design)

1. **Which quantity is the entry point** — the sourced plasma-coupled 50 MW with wall-plug computed forward from it, or wall-plug with coupled power computed down. The source publishes the *coupled* number; a wall-plug entry point would make the sourced value an output of a derived input. The design decides and states why.
2. **Where the chain lives** — inside the power-balance analysis, in its own library analysis file, or hung off the `'Heating and CD'` part def.
3. **How much entry-point retirement to take on**, against MR-WI039-9's restatement cost. The cheapest honest option is a legitimate answer.
4. **Whether `eta_couple = 1.0` is stated or sourced** (MR-WI039-3), and whether the design judges a stated assumption sufficient for the anchor.

## Related artifacts

Goal: `work/orchestration/goals/wall-and-heating/` (`goal.md`, `trail.md` § Round 1). Epic: `work/backlog/epic-mfe-cost-modeling.md`. Rubric and grades: `.project/active/demo-depth-rubric/`. Sibling escape route, sequenced after this goal's wall half and after WI-040: WI-038. Design, plan, implementation: to be created.

## Amendments

None.
