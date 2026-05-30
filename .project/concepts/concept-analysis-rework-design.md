# Design: Concept-Analysis Pipeline Rework

**Status:** Proposed
**Owner:** Reid
**Created:** 2026-05-30

---

## Overview

The concept-analysis pipeline today produces per-concept cost estimates that look comparable but aren't. The cause is a tangle: the plant being modeled is described inconsistently within each concept, and the cost-model setup files re-derive work the costing library can already do — drifting from library updates and burying analyst judgment in code without a clear discipline for when that judgment is warranted.

This design splits the work into two layers — **specifying one named plant** per concept, then **projecting its cost at one standardized scale** — and reorganizes the per-concept setup files so the library carries the default story and the analyst's role is to record specific, evidence-backed departures from it. Cross-concept comparison becomes apples-to-apples by construction.

---

## Problem

Per-concept cost numbers are placed side by side in the comparison view and labeled the same thing, but they aren't. Within any single concept's analysis, the geometry comes from one source, the performance numbers from another, the cost anchors from a third — and the result is run through the cost model as if all three described the same plant. They don't. Some are pilot-plant scales, some are longer-term targets, some are FOAK demonstrators. The composite plant the cost number ends up describing does not exist as a coherent design anywhere.

The setup files compound this. The costing library already computes most accounts from geometry, physics, fuel, and archetype. The current template encourages every setup file to re-pass dozens of library defaults as if they were deliberate choices — freezing values that should track library updates. On top of that, analysts add cost adjustments without a clear standard for when adjusting beats accepting the library's number. The result is a set of files where it is effectively impossible to tell which numbers are the analyst's deliberate departure from the library's default story and which are accidental, stale, or unjustified.

Cross-concept comparison breaks for a third reason: each concept reaches "1 GWe NOAK" by a different mechanism — some at native scale, some by single-knob output-power scaling on a frozen sub-scale module, some not scaled at all — but they are all displayed under the same label.

---

## Goals

- Make every concept describe exactly one named plant; the question "what plant did we model?" has a one-sentence answer.
- Make every concept's cost projection use the same standardized scaling mechanism to the same target scale, so comparison is apples-to-apples by construction.
- Make the costing library the default story for every cost account; require evidence to overturn it.
- Make every analyst departure from the library a single accountable entry: what is changing, what evidence supports it, how it was reasoned, and a flag a reviewer can flip off to see what the library says.
- Pre-compute the upfront comparison structure (archetype mapping, fit grade, comparables) so review uses deterministic data instead of runtime judgment.
- Make critical review a standalone capability that can run against any concept at any time, independent of pipeline state.

## Non-Goals

- Replacing the costing library or extending it with new archetype categories.
- Modeling concepts whose archetype mapping is "none" — those stay in the deferred freeform branch.
- Projecting physics or performance forward from a demonstrator to a commercial scale — we take the company at its word on whatever named design we adopt.
- Modifying the downstream comparison-view tool's contract for reading per-concept results.
- Deriving cost analogues across concepts automatically — cross-concept reasoning stays under human (and critic) judgment.

---

## Design Principles

### 1. Specification and cost projection are separate layers.

What plant are we modeling, and what would it cost at standard scale, are two different questions. The first fixes the design point — one named unit, at its native scale and maturity, taken at the company's word. The second runs that design point through one standardized scaling mechanism. Mixing the two — letting the cost projection's target distort the specification, or letting the specification's native scale leak into the projection — is the root cause of the current incomparability.

### 2. The library carries the default story.

The costing library, given the design point's geometry and physics and an archetype mapping, can compute most cost accounts. That is the default story. The analyst's job is not to re-derive it; it is to identify the specific places where evidence from the company shows the library is wrong for this concept, and to record exactly that. Anything written that just repeats the library's default is noise.

### 3. Determinism upstream beats judgment downstream.

Anything that can be settled by a pre-computed project-level table — what archetype a concept maps to, how well that mapping fits, who the concept's comparables are — should be settled there. Asking the analyzing or reviewing agent to invent these at runtime makes every concept's review subtly different and harder to audit.

### 4. Every override is one accountable, toggleable claim.

Each departure from the library is a single named entry with: the account being changed, the value or multiplicative adjustment, an enabled flag, the kind of evidence backing it (directly stated by the company, or derived by the analyst from company statements), the source citation, and the rationale. A reviewer flips one flag and sees the library's answer for that account on this exact plant.

### 5. Compare like-for-like at one standardized scale.

Cross-concept comparison happens at one fixed projection — a hypothetical 1 GWe NOAK plant — reached by the same scaling mechanism for every concept. A small-module concept does not get to look small; it is honestly costed at the replication count needed to reach 1 GWe, with each module held at its own native operating point. Concepts that genuinely could scale up a single machine are conservatively over-costed, not under-costed, by this rule.

---

## Architectural Bets

- The two-knob library scaling — output power for the shared plant, module count for the reactor island — carries the entire cost projection. No parallel cost rollup, no ad-hoc scaling helpers in the per-concept files.
- The costing library is the cost source of truth. The per-concept setup files contribute only the specification and a small set of provenance-marked overrides.
- Three upfront project-level tables (archetype mapping, fit grade, comparables) replace the runtime LLM judgments they currently substitute for. Determinism here makes every downstream review consistent.
- The critic is a standalone tool, not a pipeline stage. The pipeline loop has one fewer moving part, and the critic can be run against any concept's artifacts at any time, regardless of loop state.

---

## Core Model

*Register shift: code-level identifiers from here down.*

### Design Point Block

A structured section inside each `analysis.md`, positioned immediately adjacent to the LCOE-parameters section. Fields: design name, maturity tier, native plant power `P_native`, key geometry / physics / performance values, primary source citations. Every parameter in the surrounding LCOE-parameters section describes the same unit named here.

### Project-Level Tables (upstream input — assumed to exist)

Three tables, populated and maintained outside this rework's scope:

- **Ontology table** — one row per concept; confinement type, fuel, taxonomy traits.
- **Archetype-fit table** — one row per concept; the `ConfinementConcept` enum value, and a fit grade (`High` / `Med` / `Low` / `None`). `None` routes to the freeform branch (out of scope).
- **Comparables table** — one row per concept; the comparable-concept set, derived from the ontology and the 1costingFE family by the orchestrator.

### `model_setup.py`

A short, ordered four-step script. The order is load-bearing — the native pass produces the library values that the override step reasons against.

```python
# 1. Specification — design-point inputs (geometry / physics / performance).
#    Only values deliberately taken from the design point; library defaults
#    are not re-passed.
spec = dict(R0=..., plasma_t=..., elon=..., eta_th=..., ...)
P_native = ...   # design-point net electric power, MWe

model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

# 2. Native forward — library's bare answer for the specified plant,
#    single module. Gives the analyst the per-account values they
#    need to reason about when defining overrides.
result = model.forward(net_electric_mw=P_native, n_mod=1, noak=True, **spec)

# 3. Override registry — entries written with `result`'s computed
#    accounts in hand. Each entry is a final per-module value at
#    design-point reference; the reasoning chain (including any
#    arithmetic against the library's computed value) is in rationale.
overrides = [
    {"account": "C220103", "value": 6901.0, "enabled": True,
     "provenance": "direct", "source": "...", "rationale": "..."},
    ...
]

# 4. 1 GWe NOAK forward — the standardized cost projection. Library
#    scales each override from the design-point reference to the
#    target (net=1000, n_mod=1000/P_native).
result_1gw = model.forward(
    net_electric_mw=1000,
    n_mod=1000 / P_native,
    noak=True,
    cost_overrides={o["account"]: o["value"] for o in overrides if o["enabled"]},
    override_reference_mw=P_native,
    **spec,
)
```

Module-level contract for `concept_explorer`: `model`, `result`, `result_1gw` are all importable at module level. No change from today.

### Override Entry

A single registry record:

```python
{
    "account":    "C220103",
    "value":      6901.0,            # at design-point per-module
    "enabled":    True,
    "provenance": "direct",          # or "derived"
    "source":     "<citation>",
    "rationale":  "<short prose>",
}
```

`value` is always a plain number at design-point per-module. If the analyst's reasoning is "70% of the library's computed value of $X," the analyst does the multiplication at write-time, writes the resulting number, and captures the chain in `rationale`. The registry does not carry an expression language.

Toggle semantics: when `enabled=False`, the entry is omitted from the `cost_overrides` dict passed to `forward()`, and the library computes that account from specification.

### `model_critic`

A standalone tool, invoked by name against any concept directory. Reads the design point block, override registry, archetype-fit grade, comparables, and the two result objects. Writes one document: headline issues with brief rationale up top, detailed reasoning traces below. Writes nothing else. Downstream use of the document is the user's call.

### `concept_explorer` contract (preserved)

The downstream comparison tool continues to read `model`, `result`, and `result_1gw` as module-level attributes of each `model_setup.py`. No change.

---

## Required Invariants

### 1costingFE preconditions

- `n_mod` accepts any positive real value, not only integers ≥ 1.
- `forward(net_electric_mw=N, n_mod=M)` sizes the shared plant (BOP + plant-wide reactor auxiliaries) for total power `N` and replicates the reactor island `M` times, each module solved at per-module power `N/M`.
- Every cost override is interpreted at the design-point reference (`override_reference_mw = P_native`, single-module). The library scales each to the call's `(net_electric_mw, n_mod)` per the account's own scaling law. This holds uniformly for per-module reactor-island accounts and for plant-total accounts.
- An applied override fully replaces the computed value at its layer. No fudge factors, no silent fallbacks.

### Pipeline invariants

- Every `analysis.md` contains exactly one design point block. Every LCOE-relevant parameter on the page describes the unit named in that block.
- Every `model_setup.py` exposes `model`, `result`, and `result_1gw` at module level.
- `result_1gw` is reached by the two-knob call at `net_electric_mw = 1000`. No other mechanism produces `result_1gw`.
- `model_setup.py` does not pass any library default as if it were a deliberate input. It passes only the design point's specification and the override registry.
- Every override is a complete registry entry (all six fields). No bare numbers passed into `cost_overrides`.
- `Comparables:` frontmatter is populated by the orchestrator from the comparables table. The analyzing agent does not edit it.
- `model_critic` runs against any concept directory at any time, with no dependency on pipeline state.

---

## How It Works

### Running the pipeline on a concept

The orchestrator populates the concept's frontmatter from the upstream tables (`Comparables:`, archetype-fit grade). The `analyze` stage produces an `analysis.md` containing a design point block (one named plant, native scale, source-cited), the LCOE-relevant parameters describing exactly that plant, and the analyst prose framing what is different about this concept vs. its archetype family and its comparables. The `model_setup` stage produces a `model_setup.py` that passes the design point's parameters inline to `forward()`, defines an override registry of any company-data-backed cost departures, and runs `forward()` twice — once at native and once via the two-knob 1 GWe call. The `assess` stage checks the override count against the archetype-fit grade and runs the deterministic comparables sanity-check on the per-account breakdown of `result_1gw`.

### A reviewer toggling an override off

The reviewer opens the `model_setup.py`, flips `enabled: False` on one entry, re-runs the script, and sees the new `result_1gw` with the library computing that account from specification. The downstream comparison view sees the new result on the next sync but is unaffected mid-run.

### Running `model_critic` against any concept

The reviewer invokes `model_critic <concept-id>`. The critic reads that concept's artifacts (active or archived) and writes a review document — headline issues up top, detailed reasoning below. The reviewer decides whether to act on it, feed it back into the loop via the existing feedback mechanism, share it, or set it aside.

### `concept_explorer` pulling results

The explorer imports each `model_setup.py` and reads `model`, `result`, and `result_1gw`. For every concept, `result_1gw` is at exactly 1000 MWe, reached by the same two-knob mechanism. Cross-concept comparison is apples-to-apples.

---

## Edge Cases and Failure Modes

- **Native power far below 1 GWe.** `n_mod = 1000 / P_native` is large; the reactor island is heavily replicated. Per-module operating point is exactly native; cost is conservative against any honest scale-up of a single machine. The concept is honestly priced, not under-priced.
- **Native power = 1000 MWe.** `n_mod = 1`; the two-knob call collapses to the single-module reference. `result` and `result_1gw` are equal.
- **Company has only a sub-scale demo with no power production.** The demo is still the design point; `P_native` is whatever the demo's stated electrical output would be at its target operating point. A demo that produces no electricity by design has no `P_native` and routes to the freeform branch (deferred).
- **Archetype fit is `None`.** Routes to the deferred freeform branch and is asterisked in the comparison view.
- **High archetype-fit concept with many overrides.** Surfaced by the `assess` stage as a red flag; resolved by the analyst or escalated via `model_critic`.
- **Low archetype-fit concept with zero overrides.** Same — flagged as suspicious (likely hiding work).
- **Multiple published designs from the same company.** Resolved by the rule: most-mature with best published data; whitepaper-only long-term targets qualify.

---

## Vocabulary

- **Design point** — the one named unit being specified by a concept, at its native scale and maturity, taken at the company's word.
- **Specification inputs** — geometry, physics, and performance kwargs to `forward()`. They describe the design point. Not overrides.
- **Override** — a deliberate departure from a library-computed cost account, recorded as one registry entry.
- **Cost projection** — the standardized cost of the design point at 1 GWe NOAK, computed by the two-knob `forward()` call. The cross-concept comparison number.
- **Two-knob scaling** — `net_electric_mw` sizes the shared plant; `n_mod` replicates the reactor island.
- **Provenance** — the kind of evidence supporting an override: `direct` (company states the value) or `derived` (analyst reasons from company statements).
- **Archetype fit** — a project-level grade (`High` / `Med` / `Low` / `None`) for how well a concept maps to its assigned `ConfinementConcept` enum.
- **Comparables** — the pre-computed set of nearest-neighbor concepts, supplied by the orchestrator.
- **Replication floor** — the assumption that scaling to 1 GWe happens by module replication, not by sizing a single larger machine.

---

## Validation Strategy

- Every `model_setup.py` produces `result_1gw` at exactly `net_electric_mw = 1000`.
- For each concept, comparing override count against archetype-fit grade flags inconsistencies (`High` + many overrides, `Low` + zero overrides).
- Toggling all overrides off in any `model_setup.py` produces the library's bare answer for that concept's specified plant.
- For any account with no override, the per-account value in `result_1gw` matches the two-knob library scaling of the native single-module reference.
- The downstream comparison view extracts the same field set from every concept's `result_1gw`.
- `model_critic` runs cleanly against an archived concept whose pipeline state is gone — proving its independence from loop state.

---

## Next-Stage Handoff

**Settled here:**
- Two-layer split (specification vs cost projection) and the two-knob mechanism reaching one fixed 1 GWe NOAK target.
- The 1costingFE invariants the rework depends on (listed in Required Invariants).
- Override entry shape (six fields) and toggle semantics.
- `model_critic` as a standalone sibling tool, not a loop stage.
- Design-point selection rule: most-mature with best published data; whitepaper-only long-term targets qualify.
- Single justification discipline: company-data-backed only. Library-mismatch cases route via archetype-fit grade or the freeform branch.
- `concept_explorer` contract preserved.

**Spec/design detail still needed next:**
- Precise schema and field list for the design point block.
- Python data structure for the override registry and the helper that converts it to a `cost_overrides` dict.
- `model_critic` review artifact format.
- Shared utility module for the two-knob forward pattern and the override registry helpers.
- The deterministic comparables sanity-check: which per-account statistics and outlier flags it computes.
- Migration rollout shape (pilot vs. all-at-once) and pilot success criteria.

**First risk to de-risk:**
- The two 1costingFE preconditions that require library changes (non-integer `n_mod`; consistent override scaling under the two-knob call) — verify they hold or are achievable cleanly before the migration pilot. Without them, the entire cost-projection invariant fails.

---

## Summary

The rework hinges on one move: separate "what plant is this?" from "what would that plant cost at 1 GWe NOAK?". The first is specified once, taken at the company's word. The second is computed by one standardized scaling mechanism for every concept. Between the two, the costing library carries the default cost story; the analyst contributes a small set of accountable, toggleable, company-data-backed departures. Cross-concept comparison becomes apples-to-apples by construction, and analyst judgment is auditable per-entry instead of buried in the code.
