# Concept: Concept-Analysis Pipeline Rework

**Created:** 2026-05-30
**Status:** Draft

---

## Problem Statement

Per-concept LCOE estimates are not currently comparable to each other. Two interlocking failure modes cause this:

1. **The "what plant are we specifying?" question has no single answer.** Within a single `analysis.md`, geometry comes from one source (often a published company design), performance numbers come from another (sometimes a longer-term target, sometimes a FOAK demonstrator), and cost anchors come from a third. `model_setup.py` then runs the cost model with `noak=True` against this mixed bag. The pipeline conflates two things that should be separate: the **specification** of one specific plant (taken at the company's word) and the **cost projection** of that design scaled to 1 GWe NOAK. When concepts are placed side by side, what looks like an apples-to-apples NOAK comparison is actually a mix of pilot-plant scales, target-plant physics, and NOAK contingency factors.

2. **`model_setup.py` files stomp 1costingFE.** The library has earned the authority to compute most cost accounts from geometry, physics, fuel, and archetype — but the current prompt encourages every `model_setup.py` to explicitly pass dozens of engineering parameters with `# DEFAULT: framework value` comments, freezing YAML defaults into hardcoded values that no longer track library updates. Cost overrides are applied without a clear "is the library wrong, or am I just second-guessing it?" discipline. The freeform branch (concepts that don't map to a `ConfinementConcept` enum) goes further and reimplements the entire CAS rollup in parallel, hand-copying library constants.

The reasoning is baked deeply into ~39 `analysis.md` files, the same number of `model_setup.py` files, and their iter-N artifact trees. Untangling it surgically is harder than rebuilding per concept against a stricter methodology. The research data in `knowledge/concept_research/` (dossiers, sources, extracted documents) is the hard-won part and stays. The pipeline templates, validators, frontmatter schema, and per-concept generated artifacts get rebuilt.

## Success Criteria

When this work is complete:

1. **Single specified plant per concept** — Every `analysis.md` specifies one specific unit (named design, maturity tier, primary source citations), and every geometry/physics/performance parameter used downstream describes *that same unit at its native scale and maturity*. A reader can answer "what plant are we specifying?" in one sentence. This is the specification; what gets costed is a projection of it (see #2).

2. **Costs are a projection: as if the specified plant were scaled to 1 GWe NOAK** — Every concept produces a `result_1gw` by running the library at `net_electric_mw=1000`, `noak=True`, with the reactor island replicated to 1 GWe via `n_mod` while each module is held at the specified plant's native operating point (see Concept 6). This is the cross-concept comparison number; the concept_explorer consumes it. The cost result is explicitly a hypothetical projection — *what would it cost if this design were scaled to a 1 GWe nth-of-a-kind plant?* — not a claim about what the company will actually build.

3. **Library defaults are authoritative** — `model_setup.py` files pass only parameters that are deliberately overridden from a company source. Re-passing a YAML default is an antipattern; the prompt enforces omission.

4. **Override discipline is checkable** — Every cost override is one entry in a named, toggleable structure with a single justification class ("backed by company data, direct or estimated-with-rationale"). A reviewer can flip any override off and see the un-customized library answer.

5. **Comparables are deterministic and upfront** — Each concept's nearest neighbors are derived from a project-level ontology/archetype-fit table before `analyze` runs; the frontmatter field is `Comparables:` (not `Reuses:`), populated by the orchestrator, not the analyzing agent.

6. **Archetype-fit grade gates override expectations** — Each concept is pre-labeled High / Med / Low / None for how well its closest 1costingFE archetype fits. Review and `model_critic` use this as the expected-override-count baseline.

7. **`model_critic` is on-demand and produces a single readable review artifact** — A standalone critical-review agent invokable at any time against any concept's artifacts. Emits one review document: headline issues with high-level rationale up top, then a detailed section with full reasoning traces. The user decides what to do with it (read for context, feed back via `--feedback`, share with collaborators, etc.) — that's not the agent's concern.

8. **Existing `concept_explorer` contract preserved** — `model` and `result` (or `result_1gw`) remain importable at module level from each `model_setup.py`; the explorer's data extraction does not need to change.

---

## Why This Shape

- **Key bet:** Two clean layers. **Specification:** we spec one plant — the named unit, at its native scale and maturity, taken at the company's word. We do not project physics or performance forward to NOAK. **Costing:** we estimate the cost *as if that design were scaled to 1 GWe NOAK*, by holding each module at the specified plant's native operating point and replicating it to 1 GWe (Concept 6). Cross-concept comparability collapses to a cost-layer projection problem; physics variance between concepts is accepted as part of comparing real designs honestly.

- **Why this shape is promising:** The hardest part (sourcing, extraction, dossiers) stays untouched. The library already does the work we keep duplicating; we're moving from "agent guesses what to override" to "library is authoritative unless company data says otherwise." Pre-computing the ontology / archetype-fit / comparables tables turns three runtime-LLM judgments into deterministic data the prompts can read — making both analysis and review more consistent and the cost of each cheaper.

- **Constraint to preserve downstream:** The `model` / `result` (or `result_1gw`) module-level contract consumed by `concept_explorer/extract_explorer_data.py` is the wire to the visualization layer. Anything we do must keep that contract intact, or extend it backwards-compatibly.

---

## Methodology Spine

All the moving parts above (design point, ontology, comparables, archetype-fit, override registry, model_critic) exist to serve one linear methodology, anchored on a counterfactual: **the library is the default story; every override answers "why is the library wrong for this specific concept?"** The burden of proof sits on overriding, not on accepting library defaults.

The spine, in order:

1. **Spec one plant** — pick the named design point; take the company at its word for geometry / physics / performance at native scale and maturity.
2. **Family-delta vs comparables** — name what is *different* about this concept versus its archetype family and its pre-populated nearest neighbors. Differences are the surface area for customization; similarities should not be customized.
3. **Override candidates** — the deltas surface candidate cost-account overrides ("compact footprint → CAS21 may differ," "novel driver → CAS22.07 may differ"). At this stage they are candidates, not commitments.
4. **Fit-grade bounds the count** — the archetype-fit grade (High / Med / Low) sets the expected magnitude of override count. High-fit concepts proposing many overrides are doing something suspicious; Low-fit concepts with zero overrides are probably hiding work.
5. **Company-data gates each** — every surviving override must be backed by company data (direct or indirect-with-rationale). Anything that fails this gate falls back to the library default. Structural zeros the library already handles don't count as overrides.
6. **Toggle records it** — each surviving override is one named entry with an in-file `enabled` flag, source citation, and justification. The structure makes the chain auditable and the counterfactual ("what if we flipped this off?") reproducible.

`model_critic` walks this same spine in reverse: are the toggled overrides justified by company data? Does the override count match the fit grade? Are the right deltas being customized? Is the spec'd plant coherent?

---

## User Stories

### Analyst (running the pipeline on a concept)

**US-1: Start clean against a stricter methodology**
As an analyst, I can run the new pipeline on a concept and get a fresh `analysis.md` and `model_setup.py` whose structure forces me (and the LLM) to name the design point, identify the archetype fit, and only override what company data actually supports — without having to untangle prior reasoning.

**US-2: See the specified plant explicitly**
As an analyst, I can read any `analysis.md` and immediately find the named design point being specified, its maturity tier, and the primary sources, positioned right next to the LCOE parameters that quantify it — distinct from the 1 GWe NOAK cost projection produced in `model_setup.py`.

**US-3: Invoke a critical second opinion at any time**
As an analyst, I can run `model_critic` against any concept's artifacts without waiting for a fixed pipeline phase, and get back one readable review document — headline issues with rationale up top, full reasoning traces below. What I do with it (skim, act on, feed back via `--feedback`) is my call.

### Reviewer (assess / review / human-in-loop)

**US-4: Sanity-check against comparables**
As a reviewer, I can compare a concept's CAS breakdown against its pre-computed comparables and an overall physics-based judgment, and flag overrides that look unjustified given the concept's archetype-fit grade.

**US-5: Toggle overrides off in-file during pipeline review**
As a reviewer, I can edit a `model_setup.py` to flip any single override's `enabled` flag (or all of them), re-run the script, and see the library's un-customized answer — to test whether each override is doing real work. This is a deliberate pipeline-review action; the explorer is not affected unless I commit the change.

### Cross-concept consumer (explorer / downselect)

**US-6: Compare like-for-like**
As a downselect participant, I can compare LCOE across concepts at a consistent "as if scaled to 1 GWe NOAK" projection, knowing every concept has been put through the same library scaling rather than some being native, some being post-hoc napkin-scaled, and some mixing FOAK physics with NOAK cost factors.

---

## Key Concepts

### 1. Design Point (the specification)

The named, specific unit being **specified** — a particular published design, or for early companies a stated longer-term target. *Not* a NOAK projection; not rescaled; not adjusted. The plant as the company describes it, at its native scale and maturity. Lives inside `analysis.md` as a structured block positioned immediately adjacent to the LCOE-relevant parameters section, because the parameters *are* the design point's quantitative description and must match it 1:1. Fields: design name, maturity tier (paper concept / pilot demonstrator / proposed commercial), key geometry+physics+performance values, primary source citations. Multiple sources are allowed if they describe the same unit; mixing sources that describe different units is the antipattern this construct exists to prevent. The cost projection to 1 GWe NOAK happens in `model_setup.py` (see Concept 6); the design point itself is *not* a NOAK plant.

### 2. Ontology Table (project-level)

Deterministic, one row per concept: confinement type, fuel, and the taxonomy traits that drive comparability. Pre-computed and stable; not regenerated by the analyzing agent. Drives both `Comparables:` and the archetype-fit assessment.

### 3. Archetype-Fit Table (project-level)

For each concept: which 1costingFE `ConfinementConcept` enum value it maps to, and a fit grade — High (override count should be near zero), Med (a few targeted overrides expected), Low (many overrides; loose fit), None (no enum fits — falls into the deferred freeform branch). The grade is the gate that `model_critic` and `review` use to judge whether the number of overrides is reasonable.

### 4. Comparables

Replaces the current `Reuses:` frontmatter field. Populated upfront by the orchestrator from the ontology table; the analyzing agent does not edit it. Drives sanity-check review ("does this concept's CAS22 sit reasonably next to its three comparables?") and informs the analysis prose ("what's *different* about this concept versus its family / nearest neighbors").

### 5. Override Discipline

A single category: every cost override must be backed by company data. Provenance is either direct (whitepaper $/J, stated $/m²) or indirect-with-rationale (company touts reduced footprint → we derive a cost delta and document the chain). Structural zeros that the library already handles via the concept enum are not overrides — they should not appear. Each override is one entry in a named structure inside `model_setup.py` with an `enabled: bool` flag, account, value-or-callable, source citation, and justification. **The toggle is in-file and operated by a human reviewing the pipeline:** flip a flag in the source, re-run the script, see the impact. This is a pipeline-review affordance, *not* a live-explorer control — the explorer always consumes the baseline result with overrides applied as specified in the file.

### 6. Cost Projection to 1 GWe NOAK

The cost number we compare across concepts is *not* a cost estimate for the specified plant. It is a projection: **what would this design cost if it were scaled up to a 1 GWe nth-of-a-kind plant?** The projection uses two of the library's scaling knobs *together*, because neither alone scales a design honestly to 1 GWe:

- **`net_electric_mw` (output-power scaling)** drives the power balance and prices everything that scales with plant output — the balance of plant (CAS23–26) and the plant-wide reactor auxiliaries (coolant, cryoplant, rad-waste, fuel handling, I&C; C220200–C220700). These are sized **once for the whole 1 GWe plant** and get genuine economies of scale.
- **`n_mod` (module count)** replicates the reactor island — the machine itself: coils, blanket, driver, vessel, structure (C220101–C220112). This knob is *required* because output-power scaling **does not move geometry-driven accounts**: the radial build is a fixed input, so component volumes don't grow with target power, and the coil account (C220103) has *no* power term at all — it is invariant under `net_electric_mw`. Without `n_mod`, scaling a small design to 1 GWe would freeze its magnet cost at the native-machine value (the single largest cost for magnetic concepts). `n_mod` instead scales the machine linearly by replication.

**The rule, applied uniformly to every concept:** call `forward(net_electric_mw=1000, n_mod=1000/P_native, noak=True, ...)`, where `P_native` is the specified plant's net electric power. Because the library computes per-module power as `net_electric_mw / n_mod`, this holds **each module at exactly the specified plant's native operating point** (`1000 / (1000/P) = P`) — so the validated physics and geometry are used at the scale they were specified for — while the reactor island is replicated by a factor of `1000/P` to reach 1 GWe. Every concept ends up compared at exactly 1000 MWe. `model_setup.py` also runs a native single-module call (`net_electric_mw=P, n_mod=1`) as the self-consistent reference; the 1 GWe NOAK result is what `concept_explorer` consumes. Sweeps and what-if scenarios are still printed for uncertainty, but the standardized projection baseline is fixed.

**What this deliberately does and does not model.** This holds every concept to a *replication floor*: a 50 MWe module becomes twenty 50 MWe modules, not one larger machine sized for 1 GWe with sub-linear $/W magnets. Concepts that genuinely could scale up a single machine are therefore costed conservatively (over-, not under-costed) — and that is accepted, because sizing a new machine to a target power is beyond what we can model from a single design point. `n_mod` is surfaced per concept so a reader can see when a concept is being held to the replication floor rather than a physical scale-up.

**`override_reference_mw` IS passed, set to `P_native`.** Each override `value` is written at design-point per-module (i.e. one module at native power). Passing `override_reference_mw=P_native` to the two-knob call tells the library that frame explicitly, so it scales each override from "one module at native" to the call's `(net=1000, n_mod=1000/P_native)` target per the account's own scaling law. Item 4 of the rework epic landed the `_scale_overrides` fix (`1costingfe a2153ad`) that makes this reference frame correct; without that fix the library's reference forward ran at the caller's `n_mod` and silently inflated power-dependent overrides. The three-way invocation inconsistency that previously plagued the per-concept files is resolved not by dropping `override_reference_mw` but by *always* passing it at `P_native` — the call shape is now uniform across every concept.

**Required library change — non-integer `n_mod`.** `1000/P_native` is generally fractional, but `1costingFE` currently declares `n_mod: int = Field(default=1, ge=1, strict=True)` (`validation.py:90`), which rejects floats. Every actual use of `n_mod` in the library is continuous arithmetic (multiply / divide / `sqrt` — no indexing, `range`, or modulo), so relaxing the field to a positive float (`gt=0`) is a one-line change plus a test. With it, `n_mod = 1000/P` lands each module *exactly* at native power and the plant *exactly* at 1 GWe. Without it, `n_mod` must be rounded to the nearest integer (choosing the integer that puts per-module power closest to native), which pushes per-module power off native by a bounded amount — worst for native powers in the ~500–900 MWe band. This rework **assumes the float change is made**; it is the one library modification this work depends on.

### 7. `model_critic` Agent

A standalone, on-demand devil's-advocate agent. Invokable against any concept at any time, independent of where that concept sits in the loop. Produces **one review artifact** designed to be highly readable: headline issues with high-level rationale up top, then a detailed section with full reasoning traces. What the user does with it — read it for context, hand-edit it and feed it back via `--feedback`, share it for human review — is outside the agent's scope.

---

## Scope of Behavior Changes

### New artifacts to create
- **Project-level ontology table** — one source-of-truth for confinement type, fuel, taxonomy traits per concept
- **Project-level archetype-fit table** — concept → `ConfinementConcept` + fit grade (High/Med/Low/None)
- **Project-level comparables derivation** — function/script populating `Comparables:` frontmatter from the ontology table
- **Deterministic comparables sanity-check** — a script that computes the per-account comparison statistics and outlier flags from each concept's `result_1gw` and its comparables. The flags are an input to the LLM reviewer, which performs the assessment; the script computes and flags, it does not assess.
- **Design-point block** inside `analysis.md` (new structured section positioned with the LCOE parameters)
- **`model_critic` agent** — standalone invokable, emits one readable review artifact (headline issues + detailed reasoning traces)
- **Shared `model_setup` utilities** — helpers for the native + 1 GWe dual-forward pattern (computing `n_mod = 1000/P_native` and issuing both `forward()` calls), override registry/toggle structure, CAS-breakdown printing

### Existing artifacts to modify
- `analysis_v2.md` prompt — restructured to drive essence → ontology → comparables → design point → LCOE parameters (parameters scoped to what 1costingFE expects for the mapped archetype)
- `output_template.md` — restructured for the new section ordering and the design-point block
- `model_setup_costingfe.md` prompt — flip the discipline: omit library defaults, pass only deliberate overrides, use the toggleable override registry, always produce `result_1gw` via the two-knob `forward(net=1000, n_mod=1000/P_native, override_reference_mw=P_native, …)` call (override `value`s are at design-point per-module; `override_reference_mw=P_native` makes that reference frame explicit so the library scales correctly)
- `frontmatter.py` — rename `Reuses:` → `Comparables:`, populated upfront not at runtime
- `validators.py` — drop the fragile FINDING/VERDICT regex where new prompt formats make it unnecessary; replace with parsing that's robust to LLM formatting variation
- `loop.py` — register `model_critic` as a substitutable feedback-producer (likely a small change; the architecture already supports this)

### Behavior changes by workflow stage
- **Analyze:** must produce a design-point block; parameters tied to what the mapped archetype expects; nearest-neighbors framing comes from the deterministic comparables, not LLM judgment.
- **Model setup:** uses library defaults aggressively; overrides are explicit-and-toggleable, justified by company data only; always produces both native and 1 GWe results; freeform path deferred (out of scope this rework).
- **Assess (in-loop) / Review (post-loop):** add a comparables sanity-check whose statistics and outlier flags are computed **deterministically** (the script above); the LLM reviewer **assesses** those flags rather than computing them. Also add a physics-based judgment pass; use archetype-fit grade as the expected-override baseline.
- **`model_critic` (on-demand):** new agent any human can invoke at any time; emits one readable review artifact (headline issues + detailed reasoning traces). Downstream use is the user's choice.
- **Synthesize / Score:** unchanged in this rework (downstream and largely independent).

### Per-concept artifacts touched during migration
- Delete and regenerate: `analysis.md`, `model_setup.py`, `iter-*/`, `synthesis.md`, `gap_report.md`, `review.md`, `model_output.txt`, `address_log.md`, `research_log.json`, `prompts/`
- Preserve: everything under `knowledge/concept_research/` (dossiers, sources, extracted documents)

---

## Non-Goals / Out of Scope

- **Freeform-branch rework.** Concepts that don't map to a `ConfinementConcept` enum get asterisked in the comparison; their `model_setup.py` files are not part of this rework. (Deferred; revisited only if the asterisked set turns out to be too important to leave in its current state.)
- **Extending 1costingFE with new enum values.** No new archetypes; the library is taken as-is *except* for the one required change noted in Assumptions — relaxing `n_mod` to accept non-integer values.
- **Projecting FOAK physics forward to NOAK.** Out of scope — we take companies at their word on geometry/physics/performance for whatever named design point we adopt.
- **Restructuring `synthesize` and `score`.** These are downstream and largely independent; touched only as needed for the frontmatter rename or to consume the standardized 1 GWe result.
- **Replacing the existing `concept_explorer`.** The contract (`model`, `result` / `result_1gw` at module level) is preserved.
- **Cross-concept auto-derivation of cost analogues.** Reviewers (human or `model_critic`) use comparables; we don't try to auto-propagate cost values.

---

## Assumptions & Prerequisites

- 1costingFE library defaults are trusted as authoritative for everything except deliberately company-data-backed overrides.
- The native→1 GWe cost projection is achieved by `net_electric_mw=1000` + `n_mod=1000/P_native` — output-power scaling for the shared plant (BOP + plant-wide auxiliaries), module replication for the reactor island, each module held at native operating point. Verified against the library's per-account scaling and `n_mod` handling (`model.py:105`, `cas22.py:451–453`, `costs.py`, `economics.py`).
- **Prerequisite library change:** `1costingFE` must accept non-integer `n_mod` — relax `validation.py:90` from `int … strict=True` to a positive float (`gt=0`). One-line change plus a test; all `n_mod` arithmetic in the library is already continuous. Without it the projection falls back to integer-rounded `n_mod` with a bounded per-module-power error (worst in the ~500–900 MWe native band). This is the single library dependency of the rework.
- Existing `knowledge/concept_research/` dossier + source structure is preserved and good enough as-is.
- The `concept_explorer` module-level contract is fixed and any rework must keep it.
- The existing substitutable-feedback-producer architecture in `loop.py` is the right home for `model_critic`; no fundamental loop restructure is needed.

## Open Questions

1. **Table file format and location** — CSV? YAML? Markdown with frontmatter? Project root, `knowledge/`, or `exploration/concept_analysis/`?
2. **Override registry exact shape** — list of named dicts, dict-of-dicts, dataclass? (Toggle mechanism is settled: in-file `enabled: bool` flag, human edits and re-runs.)
3. **Migration rollout** — pilot on 3–5 concepts spanning High/Med/Low archetype-fit before batch regenerating the remaining ~35, or all-at-once cutover once the templates land?
4. **Validation enforcement for archetype-fit** — should `model_critic` (or `assess`) emit a warning when a High-fit concept has more than N overrides, or is that purely advisory in the critique prose?
5. **Shared utility surface area** — what's in the shared module and what stays per-concept? Where's the boundary that helps without becoming its own framework?
6. **Asterisk handling for freeform concepts** — do they continue to appear in the explorer with a clear "non-comparable" flag, or are they removed from the comparison view entirely?

---

## Next-Stage Handoff

**Settled here:**
- Two clean layers: **specification** (one named design point per concept, native scale and maturity, taken at company's word) vs **cost projection** (as if that design were scaled to 1 GWe NOAK)
- Design point lives inside `analysis.md` adjacent to LCOE parameters; cost projection happens in `model_setup.py`
- 1 GWe NOAK is the standardized cost projection basis; achieved via `net_electric_mw=1000` + `n_mod=1000/P_native` (shared plant scaled by output power; reactor island replicated by module count, each module held at native operating point). `override_reference_mw=P_native` is passed, declaring that override `value`s are written at design-point per-module so the library scales them correctly. Depends on relaxing `1costingFE` `n_mod` to non-integer and on the `_scale_overrides` `n_mod=1` reference-call fix (both landed by Item 4 of the rework epic)
- Override discipline is one category (company-data-backed, direct or estimated-with-rationale), expressed via a named structure with in-file `enabled` flags — toggled by a human reviewer editing the file and re-running the script, not via a live-explorer control
- `Comparables:` replaces `Reuses:` and is populated deterministically upfront
- Archetype-fit (High/Med/Low/None) is deterministic and pre-computed; gates override expectations
- `model_critic` is on-demand and emits one readable review artifact (headline issues + detailed reasoning traces); it is not a fixed pipeline phase, and how the user uses the output is outside its scope
- Freeform branch is deferred; asterisked concepts remain in current state
- `concept_explorer` `model`/`result` module-level contract is preserved
- "Start fresh per concept": existing per-concept generated artifacts (`analysis.md`, `model_setup.py`, `iter-*/`, etc.) are deleted; `knowledge/concept_research/` is preserved

**Needs spec next:**
- The `1costingFE` non-integer `n_mod` change (relax `validation.py:90`) — small but a hard dependency; sequence it before the migration pilot
- Exact schema and field list for the design-point block
- File format and location for ontology / archetype-fit / comparables tables
- Override registry data structure and toggle mechanism at the call site
- `model_critic` review artifact format spec (headline-issues section + detailed reasoning section structure)
- Shared `model_setup` utility module API
- Comparables sanity-check: which statistics and flags it computes, and how they are presented to the LLM reviewer
- Migration rollout shape (pilot vs all-at-once) and the criteria for declaring the pilot a success
- New analysis.md section ordering and the precise design-point block placement

**Decomposition guidance:**
Likely 4–5 epics:
1. **Tables & schemas** — ontology, archetype-fit, comparables; design-point block schema; frontmatter migration
2. **Prompts & templates** — new `analysis_v2.md`, `output_template.md`, `model_setup_costingfe.md` reflecting the new methodology
3. **Shared utilities & override registry** — the `1costingFE` non-integer `n_mod` change (prerequisite); `model_setup` helper module; native + 1 GWe dual-forward pattern (`n_mod = 1000/P_native`); toggleable override structure
4. **`model_critic` agent** — standalone invokable, one readable review artifact (headline + detailed traces)
5. **Migration & pilot** — regenerate 3–5 pilot concepts spanning fit grades; validate explorer continues to consume outputs; then batch the rest. Strip fragile validator regex as the new artifact formats make it unnecessary.
