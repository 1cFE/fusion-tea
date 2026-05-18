# Design: Deterministic Concept Scoring (V2)

**Status:** Proposed
**Owner:** Reid
**Created:** 2026-05-17

---

## Overview

A three-layer architecture for scoring fusion concepts: per-concept features feed deterministic embedding rules, which feed weighted sums into a small set of final dimensions. Weights live in separately editable matrices so the same embeddings can be evaluated under multiple "bet" scenarios. The whole system is designed so that adding an embedding, changing a weight, or correcting a feature each cost roughly what they ought to — not a full re-run of the whole portfolio.

---

## Problem

The current scoring system mixes three activities — extracting attributes from prose, applying judgement to those attributes, and aggregating judgements into a score — into a single per-concept pass. When a reviewer disputes a score, no one can tell whether the disagreement is about a fact, a rule, or a weight. When the weighting needs to change to reflect a different strategic bet, the whole pass has to run again. When the same external evidence is needed by multiple concepts, it gets duplicated and drifts between dossiers.

The upstream concept doc settles that those three activities must be separated into layers. What is still open is the *design shape* of those layers — what each one is responsible for, what shape its outputs take, how concepts move through them, and what the code framework looks like in enough detail that iteration costs are predictable. This design commits to that shape.

The specific risk it must avoid is the silent re-entanglement of layers: a feature that is really a judgement in disguise, a rule that smuggles in weights, a scenario that changes embedding values instead of weights. Each of these failure modes looks like the system working until a reviewer disagrees and the conversation collapses back into prose.

---

## Goals

- Let a reviewer point at one layer as the source of any score disagreement and resolve it without re-running anything else.
- Make adding a new judgement axis cost a rule definition plus targeted feature work, not a portfolio rescore.
- Make changing how we weight what we value a configuration edit, not a model run.
- Score the same concepts under multiple strategic bets without re-extracting any inputs.
- Cite shared world-facts once across the portfolio rather than per concept.
- Carry confidence and provenance alongside every input so the trustworthiness of a score is inspectable.

## Non-Goals

- Enumerating the final set of features, embeddings, or weights. This design commits to shapes; the catalog is a follow-on.
- Replacing the per-concept research dossier. Dossiers remain the source material from which features are extracted.
- Retrofitting V1 scores. V1 outputs remain a frozen historical artifact.
- Building a UI. Inspection is plain files at this stage.

---

## Design Principles

### 1. Three layers, three artifacts, three review cadences

Features describe what is true about a concept. Embeddings describe how we judge it. Weights describe how we value the judgements. Each is its own artifact, edited at its own cadence: features change rarely as evidence updates; embedding rules change occasionally as the analysis matures; weights change frequently as scenarios and strategic priorities shift. Collapsing two of these into one artifact reintroduces the entanglement this whole design exists to prevent.

### 2. Judgement lives in features and rules, never in execution

A feature value is something a domain expert can verify by reading one paragraph of the dossier. An embedding rule is a function whose inputs and computation are inspectable. Once both are written, executing them produces no new judgement. If running the pipeline twice yields different outputs from the same inputs, the system has a defect — not a calibration need.

### 3. Fine-grained embeddings; aggregation stays a weighted sum

Embeddings decompose far enough that any plausible strategic bet can be expressed by reweighting them rather than rewriting them. Aggregation within a score dimension is a weighted sum of embeddings — no maxes, mins, or gating built into the score layer. Binding-constraint semantics, if needed, are encoded as embeddings that produce large penalties under specific weight choices, not as hidden operators in the aggregation.

### 4. Evidence quality is reported, not aggregated

How confident we are in a score is a separate readout derived from per-feature provenance. Folding confidence into the score numbers conflates "is the answer good" with "do we know the answer."

### 5. Iteration cost matches edit scope

Editing a weight costs a recomputation. Editing a rule costs a recomputation. Editing a feature costs a targeted re-extraction for that feature across concepts plus a recomputation. Nothing costs a full LLM rescore of the portfolio unless the dossier itself has changed.

---

## Architectural Bets

- **Three score dimensions** — Economic Potential, Technical Feasibility, Manufacturability & Scale-Out — instead of mirroring V1's eight criteria. Fewer dimensions force each one to be a coherent answer to one question; scenarios cut across them rather than reshape them.
- **Pure weighted sum aggregation** even where some embeddings have binding-constraint semantics. The bet is that pushing penalties into embedding outputs keeps the score layer trivially auditable; gating operators would make weights non-additive and scenarios harder to reason about.
- **Features are flat scalars or categoricals, never narrative judgements.** The bet is that this is enough to express every embedding we need; the cost is that some attributes that would be quick to write as a sentence become a coding scheme with enumerated levels.
- **One file per concept for features; one shared file for evidence.** The natural unit of editorial review is one concept at a time, while world-facts need exactly one canonical version that all concepts reference.
- **Feature extraction is pluralist by source.** A feature can be looked up from the taxonomy table, parsed from a cost-model output, extracted from narrative prose under a pinned-prompt LLM, or entered by an analyst. The bet is that letting each feature pick its source keeps the framework honest — we don't pretend every feature comes from prose, and we don't force structured-data features through an LLM. The cost is a per-feature declaration of which extractor it uses.

---

## Core Model

The register shifts here — file names and types are appropriate from this point.

### Feature Vector — `features/{concept_id}.yaml`

One file per concept. Each entry is a flat scalar or categorical value plus a provenance tag (`taxonomy`, `proponent`, `physics_derived`, `analyst_estimate`) and a confidence level. The file is the *only* source of per-concept inputs to embeddings. Feature names, types, and enumerations live in a separate schema file that validates these files.

**Responsible for:** holding what is true about the concept.
**Not responsible for:** applying any judgement about what those values mean.

### Evidence Corpus — `evidence/corpus.yaml`

A single shared file of world-facts: demonstrated triple products by (fuel, confinement), JET sustained-power records, MSRE operating envelope, sCO2 cycle demonstrations, etc. Each entry has an ID, a value, units, a citation, and a date. Embeddings reference entries by ID.

**Responsible for:** cross-concept facts that should never drift between concepts.
**Not responsible for:** any per-concept attribute.

### Embedding Rulebook — `embeddings/rulebook.py`

One pure function per embedding. Inputs: a feature vector and optionally corpus IDs. Output: a scalar plus a version tag. Rules are code by default. An LLM-backed rule is permitted only under a reproducibility contract declared in the rulebook header — pinned model, fixed prompt, T=0, declared divergence bound.

**Responsible for:** deterministically mapping features and evidence to intermediate quantities.
**Not responsible for:** knowing how its output gets weighted.

### Weight Matrices — `weights/{scenario}.yaml`

Each file maps embedding IDs to weights within each of the three score dimensions. `default.yaml` is the baseline; `bet_*.yaml` files are alternative scenarios. The embedding-name vocabulary is shared across all matrices.

**Responsible for:** encoding strategic priorities.
**Not responsible for:** producing embedding values.

### Score Computation — `score.py`

A single script. Loads features, corpus, rulebook, and a named weight matrix; evaluates every embedding; computes weighted sums per dimension; writes a score table plus a per-dimension evidence-quality readout derived from input feature confidences.

**Responsible for:** composing the layers.
**Not responsible for:** any layer's content.

### Feature Extraction — `extract.py`

A dispatcher rather than a single extraction strategy. Each feature in the schema declares an *extractor*:

- `taxonomy` — lookup from `table.csv` by `concept_id` and column name.
- `cost_model` — structured parse from `model_setup.py` parameters or `model_output.md` cost-structure outputs (e.g. CAS line items, capex shares).
- `llm` — pinned-prompt categorical or scalar extraction from `analysis.md` / `synthesis.md` / iter-checkpoints under a reproducibility contract (pinned model, fixed prompt, T=0, declared divergence bound, divergence treated as a defect).
- `manual` — analyst-entered, used when no automated source is feasible.

Re-running `extract.py {concept_id} {feature_name}` invokes only the declared extractor for that feature. The judgement in an `llm` extractor lives in the coding scheme (what enum values exist and what they mean), not in the execution — a domain expert can verify any LLM-extracted feature by reading the cited paragraph.

**Responsible for:** populating feature files from heterogeneous concept inputs.
**Not responsible for:** deciding what features should exist or what their valid values are.

---

## Diagram

```
   SOURCES                              EXTRACTORS
   ──────────────────────────────       ───────────────────
   table.csv                       ──>  taxonomy lookup    ──┐
   model_setup.py / model_output.md ──> structured parse   ──┤
                                                             ├──> features/{concept_id}.yaml
   analysis.md / synthesis.md      ──>  llm (pinned prompt)──┤                    │
   analyst entries                 ──>  manual             ──┘                    │
                                                                                  │
                            evidence/corpus.yaml ─────────────────────────────────┤
                                                                                  │
                       embeddings/rulebook.py ──> score.py ────────────────────── ┤── score table
                                                                                  │
                       weights/{scenario}.yaml ───────────────────────────────────┘
```

---

## Required Invariants

### Layer separation
- A feature value is a scalar or categorical, never a narrative string requiring interpretation.
- An embedding rule consumes only declared feature names and corpus IDs.
- Weight matrices reference embedding IDs that exist in the rulebook; the loader fails on any unknown ID.

### Determinism
- Same features + same corpus + same rulebook version → byte-identical embedding outputs for code rules; outputs within the declared bound for LLM-backed rules.
- Same embeddings + same weight matrix → byte-identical score table.

### Iteration cost
- Re-scoring under a different weight matrix invokes no LLM call.
- Re-extracting one feature does not invalidate other features for the same concept.

### Provenance
- Every feature value carries a provenance tag and confidence level.
- Every cited world-fact resolves to exactly one entry in the corpus.

### Scenario discipline
- Scenarios differ from `default.yaml` only in weights, never in embedding values or feature values.

---

## How It Works

### Scoring all concepts under the default scenario
The analyst runs `score.py`. The script loads every concept's features, the corpus, and the rulebook; evaluates every embedding for every concept; applies `weights/default.yaml`; writes a score table with one row per concept and one column per dimension, plus an evidence-quality column. Runtime is seconds.

### Scoring under an alternative bet
The analyst runs `score.py --scenario bet_tritium_solved`. No extraction, no rule change — only the weight matrix differs. The output is a parallel score table that can be diffed against the default to surface which concepts depend on tritium-fuel-cycle weighting for their ranking.

### Adding a new embedding
The analyst writes a new function in `rulebook.py`, declaring which features it consumes. If those features already exist in the per-concept files, scoring is rerun and that's it. If a new feature is needed, the schema is extended and `extract.py` is run for the new feature across concepts (one targeted LLM call per concept), then scoring is rerun.

### A reviewer disputes a score
The reviewer reads the score table, sees concept A scored higher than expected on Manufacturability, and traces it to a single embedding. They inspect that embedding's input features. The objection scopes to one of three layers — "feature is wrong for this concept," "the rule overweights this construction mode," or "the weight on this embedding is too high under default" — and the resolution is mechanical.

---

## Edge Cases and Failure Modes

- **A feature is genuinely uncertain across the dossier.** Provenance becomes `analyst_estimate` with confidence `low`. The value still goes in; the evidence-quality readout downgrades the score's reliability. Embeddings do not branch on confidence.
- **An embedding needs a value not derivable from any feature.** This is a smell — the feature schema is incomplete. The fix is to add the feature, not to put narrative reasoning into the rule.
- **An LLM-backed rule diverges across re-runs beyond its declared bound.** Treated as a defect. The fix is to tighten the prompt, split the rule, or push inputs back into the feature layer — never to widen the bound silently.
- **A scenario wants to change an embedding value, not just its weight.** Disallowed. If an embedding's value should change under a bet, the embedding is conflating two things and needs to be split into two embeddings with separate weights.
- **A feature value changes after scoring is published.** Feature files are versioned; the score table records the feature commit it was computed against. Re-running produces an updated table; the old one remains as a frozen artifact.
- **A feature's source upgrades over time.** A feature initially populated by `llm` from prose may later become derivable as a `cost_model` parse once modeling work catches up. The schema's extractor declaration is updated, re-extraction runs, and the provenance tag on the value shifts (e.g. `proponent` → `physics_derived`). No embedding rule or weight changes.

---

## Vocabulary

- `feature`: a scalar or categorical attribute of one concept, with provenance and confidence.
- `evidence entry`: a world-fact in the shared corpus, referenced by ID across concepts.
- `embedding`: a pure function from features (and optional evidence IDs) to a scalar judgement quantity.
- `weight matrix` / `scenario`: a named mapping of embedding IDs to weights within each score dimension.
- `score dimension`: one of three final aggregated outputs — Economic Potential, Technical Feasibility, Manufacturability & Scale-Out.
- `evidence quality`: a per-dimension readout derived from input feature confidences; not aggregated into the score.
- `provenance tag`: the source kind for a feature value — taxonomy, proponent, physics-derived, or analyst-estimate.
- `extractor`: the per-feature strategy declared in the schema for how its value is populated — `taxonomy`, `cost_model`, `llm`, or `manual`.

---

## Validation Strategy

- Schema validation on every feature file: enum values, required fields, type checks.
- Rulebook unit tests: each embedding function tested on a small set of input vectors with known expected outputs.
- Determinism harness: re-run scoring twice; outputs must be byte-identical for code rules.
- Scenario sanity check: for each `bet_*.yaml`, confirm the embeddings it reweights are ones whose semantics actually shift under that bet (one-paragraph defense alongside the matrix).
- Cross-concept smell test: peer-group review of any embedding where two structurally similar concepts produce very different outputs — does the rule discriminate correctly, or is a feature mis-coded?

---

## Next-Stage Handoff

**Settled here:**
- Three score dimensions; pure weighted sum within each.
- Fine-grained embeddings; judgement lives in features and rules.
- Layer artifacts: features/, evidence/, embeddings/, weights/, score.py, extract.py.
- Evidence quality is a meta readout, not an aggregated dimension.
- Scenarios reweight only — never override embedding or feature values.

**Spec/design detail still needed next:**
- The feature schema (names, types, enums, required vs optional).
- The initial embedding catalog and rule definitions.
- The default weight matrix and the first bet scenarios.
- The `extract.py` prompt template and per-feature prompt specifications.
- The score-table output format.

**First risk to de-risk:**
- Modularity as a worked example. Build `plant_level_modularity` and `component_modularity` end-to-end — features, rules, weights, output — for a small set of concepts. If the existing xlsx family-multiplier collapses to ≈1.0 once features are fully coded, the embedding granularity is right. If it doesn't, the granularity needs to go deeper before the rest is built.

---

## Summary

The design commits to three artifact layers (features, embeddings, weights) producing three score dimensions, with evidence quality as a separate readout and scenarios as alternative weight matrices over the same embeddings. The core insight: by keeping aggregation a pure weighted sum and pushing all judgement into features and rules, every disagreement becomes localizable to a layer, and every iteration costs only what it should.
