# Concept: Scoring Framework V2 — Features, Embeddings, Scores

**Created:** 2026-05-15
**Status:** Draft

---

## Problem Statement

The current LCOE Downselect scoring system (`exploration/concept_analysis/prompt_templates/config/scoring_framework.md`, PR #13) entangles three distinct activities in a single per-concept LLM pass: extracting objective concept attributes from prose, applying judgement to those attributes, and aggregating judgements into a final score. The pass produces eight C-criteria with sub-factors, but the inputs to those sub-factors are not a fixed schema — Claude re-derives them from synthesis prose each time.

The downstream consequence is that disputes can't be localized. A reviewer who disagrees with a concept's C4 score can't tell whether the disagreement is about a fact ("CAS22 has 12 sub-accounts, not 8"), a judgement rule ("12 sub-accounts should map to score 2, not 3"), or an aggregation choice ("C4 = avg(A,B) gives the wrong weight"). The calibration pass (`calibrate.md` Q1-Q7) exists almost entirely to patch this — Q4 re-checks sub-factor arithmetic, Q6 enforces peer-group consistency, Q3 strips smuggled site-specific adjustments. These are structural symptoms, not normal calibration.

This also blocks public defensibility. The current artifacts trace a score back to a synthesis paragraph and a rubric, but not to a stable set of features that anyone could independently verify. And changing weights — say, downweighting C8 (Data Adequacy) — requires re-running the entire LLM scoring pass, because weights and judgements are produced together.

## Success Criteria

When this work is complete:

1. **Three explicit layers exist as separate artifacts** — A per-concept feature vector, a deterministic embedding stage, and a weight-driven scoring stage. Each is independently inspectable.
2. **Every final score is traceable to a feature set, a named embedding rule ID, and a named weight matrix** — Given any score for any concept, a reader can resolve it to the specific feature values, the specific embedding rule ID (with version) that consumed them, and the named weight matrix that produced the final dimension — without reading prose.
3. **Disputes can be localized to a layer** — The artifacts make it possible for a reviewer to point at a single layer (feature, embedding, weight) as the source of disagreement. The architecture *enables* this localization; in practice disagreements may span layers, and the framework's job is to make the layer-by-layer decomposition mechanical rather than rhetorical.
4. **Re-scoring with different weights does not require re-running the LLM** — Embeddings are persisted; weight changes are a recomputation.
5. **World-facts are shared, not duplicated per concept** — The same JET/ITER/MSRE/sCO2 evidence is cited identically across every concept that references it.
6. **Feature provenance and confidence are explicit per feature** — A reader can see which features are proponent-claimed, which are physics-derived, and which are analyst estimates.
7. **Multiple weight matrices can coexist** — Distinct "bet" scenarios (e.g., "tritium breeding solved at scale," "HTS cost continues to fall," "fusion regulatory framework matures") are expressible as alternative weight matrices over the same embeddings. Concepts can be scored under each scenario without re-extracting features or re-running embeddings.

---

## Why This Shape

- **Key bet:** Separating *what is true about the concept* from *how we judge it* from *how we weight the judgements* is worth the structural overhead. The three activities have different review cadences (features rarely change, judgements are debated occasionally, weights are debated openly) and different audiences (features defend against domain experts, weights defend against stakeholders).
- **Why this shape is promising:** The current system already does this implicitly for C2, C6, and η_th (lookup from `table.csv` → score). V2 generalizes the pattern that works rather than inventing a new one. The remaining criteria become legible by being forced into the same shape.
- **Constraint to preserve downstream:** The layer contracts must be specified before V2 features are enumerated. If features are designed without a clear embedding contract, the system collapses back into V1 — Claude inferring sub-factors at scoring time.

---

## User Stories

### Reviewer disputing a score

**US-1: Localizing a disagreement during a portfolio review**
As a reviewer preparing comments on the next portfolio meeting's score table, when I disagree with concept X's final score I can write a comment scoped to a specific layer ("feature `peak_field_T` is wrong" / "embedding `divertor_evidence_gap` overstates the gap" / "weight on modularization is too high under `default`") rather than a holistic objection, so that the discussion at the meeting is about a single artifact and the resolution is mechanical.

**US-2: Challenging a feature**
As a reviewer, I can point to a specific feature value and ask "what is the evidence for this?" and get a provenance answer (proponent publication, physics derivation, analyst estimate) without re-reading the synthesis.

### Public reader / external skeptic

**US-3: Defending a published ranking**
As an analyst publishing a concept ranking, when a reader emails asking "why is concept B above concept A," I can answer by sending them three pointers — the differing feature values, the embedding rules that turned those features into intermediate quantities, and the weight matrix used — without re-explaining the methodology from scratch each time.

**US-4: Comparing two concepts**
As a reader trying to understand why concept A beat concept B, I can compare their feature vectors and embeddings side by side. If the scores diverge but the features agree, the divergence must come from a judgement rule that I can inspect.

### Analyst running the pipeline

**US-5: Adjusting weights**
As an analyst, I can change the weight matrix and recompute final scores in seconds, without re-running any LLM-based scoring.

**US-6: Grounding a proponent claim**
As an analyst, I can mark a feature as proponent-claimed initially, and later upgrade its provenance to physics-derived as the modeling work catches up — without re-scoring.

### Analyst running a down-select

**US-7: Scoring concepts under a specific bet**
As an analyst preparing a down-select, I can define a scenario ("tritium breeding is solved at scale," "HTS conductor cost continues its decline," "fusion regulatory framework matures into a Part-30-style lighter pathway") as an alternative weight matrix, and score every concept under that scenario. Concepts that win conditional on a specific bet become legible distinct from concepts that win unconditionally.

**US-8: Building a portfolio that spans bets**
As an analyst selecting ~5 concepts for deep-dive, I can read each concept's score vector across N scenarios side by side, and pick a set that wins across diverse bets — not just one set that wins under the default weights. This makes "we picked these five because they each represent a different bet on what becomes true" a defensible portfolio claim.

---

## Key Concepts

### 1. Feature Vector (Layer 1)

A per-concept dictionary of scalar attributes that are deterministic consequences of *what the concept is*, ideally measurable when a plant is built. Each entry is a flat scalar plus a separate confidence/provenance tag.

**Examples (illustrative, not the V2 spec):**
- `fuel = "D-T"` (categorical, confidence: high)
- `confinement_topology = "Tokamak"` (categorical, confidence: high)
- `energy_capture = "Thermal (steam)"` (categorical, confidence: high)
- `peak_field_T = 20.0` (numeric, confidence: medium — design target)
- `aspect_ratio = 3.1` (numeric, confidence: high)
- `driver_capital_share = 0.35` (numeric, confidence: low — analyst estimate)
- `cas22_construction_mode = "site_assembled"` (categorical, confidence: medium)

The artifact (file, schema) carries the *provenance trail* — citation, derivation method, last-reviewed date — but the value itself is a flat scalar. Embeddings consume the value; confidence is available as a separate signal where it matters.

### 2. Evidence Corpus (Shared)

A separate, shared body of world-facts that embeddings can reference. Not per-concept. Examples: "JET 1997 D-T sustained 11 MW for 4 s," "MSRE operated FLiBe at 650 °C, fission spectrum, 1965–1969," "sCO2 Brayton demonstrated at 10 MWe pilot scale." Citations exist once; concepts reference them by ID.

This eliminates the V1 problem of the same external fact drifting between concept dossiers.

### 3. Embedding Vector (Layer 2)

A per-concept vector of intermediate judgements, computed as **deterministic functions of features and the evidence corpus**. Each embedding is a named rule with explicit inputs.

**Examples (illustrative):**
- `scalability_class = lookup(confinement_topology) -> {Tokamak: 2.5, Mirror: 3.5, ...}` — pure function of one feature (this is C2 today).
- `capacity_factor_ceiling = lookup(fuel, operation_mode)` — this is C6 today.
- `divertor_evidence_gap = (plant_peak_heat_flux_target / best_demonstrated_in_corpus)` — uses a feature plus a corpus lookup.
- `modularization_index = sum(cas_capital_share[i] * mode_score[cas_construction_mode[i]])` — pure aggregation over feature vector entries.
- `heritage_floor = lookup(confinement_lineage)` — pure function.
- `monolithic_driver_flag = (driver_capital_share > 0.30) AND (driver_modularization == "monolithic")` — boolean from features.

Rules are **code by default**. An LLM-backed rule is permitted only under an explicit reproducibility contract: pinned model version, fixed prompt, T=0, a recorded divergence-tolerance test, and treatment of divergence across re-runs as a defect to be fixed (by tightening the prompt, splitting the rule, or pushing inputs back into the feature layer). The contract is: **same features + same corpus + same rule version → same embedding, within the declared divergence bound**. Judgement lives in the rules, not in the per-concept execution.

### 4. Score Vector (Layer 3)

A small number of final dimensions computed as a **weight matrix over embeddings**. The weight matrix is its own artifact, separate from features and embeddings.

**Example shape (not the V2 spec):**
- `LCOE_potential = w1 * modularization_index + w2 * scalability_class + w3 * evidence_gap_avg + ...`
- A separate dimension might capture risk concentration, a third readiness, etc.

Changing weights is a config edit; the LLM does not run.

### 5. Scenario-Conditioned Weight Matrices

A scenario is a named alternative weight matrix that expresses a specific "bet." The same features and embeddings are reused; only the weights differ. Each scenario produces its own score vector per concept.

**Examples (illustrative):**
- `default`: balanced weights reflecting current best-estimate priorities.
- `bet:tritium_solved`: zero out weight on tritium-fuel-cycle embeddings; relative weight shifts to architectural and BOP embeddings. Concepts that were dragged down by D-T fuel-cycle risk now rise.
- `bet:hts_cost_decline_continues`: upweight embeddings that benefit from cheap HTS conductor; concepts whose cost story rides on HTS magnetics gain.
- `bet:regulatory_lightens`: upweight embeddings that benefit from a Part-30-style lighter regulatory pathway; downweight regulatory-burden embeddings.
- `bet:supply_chain_capability_gaps_close`: zero out F2.d / F3.a capability-gap penalties; concepts with novel-driver supply problems become viable.

Two consequences follow from this design:
- **A concept's vulnerability is legible.** If concept A wins under `default` but loses under `bet:tritium_solved`, that tells the analyst its advantage was tritium-fuel-cycle-driven, not architectural. The reverse case is just as informative.
- **Portfolio construction can span bets.** Selecting 5 concepts that each win under a different scenario produces a defensible "we hedged across the major open uncertainties" claim. Mapping to the three portfolio frames in `.project/concepts/down_select/concept_part2.md`: scenarios directly serve the **coverage** frame (the bet catalog defines the axes coverage is measured over) and the **uniqueness** frame (a concept that wins under exactly one bet is unique along that bet-axis). Scenarios do *not* by themselves answer the **irreducibility** frame — pairwise "could concept X's deep-dive output be reproduced as a sensitivity branch on concept Y" is a separate analytical step and is out of scope here.

The scenario itself is a named artifact: which embeddings are reweighted, by how much, and a one-paragraph defense of why the scenario represents a meaningful uncertainty. Scenarios are not freeform; they must point to a specific embedding (or set of embeddings) whose weight is changing.

### 6. Where Judgement Lives

- **Feature stage:** judgement about *what to measure* (schema design) and *what value an attribute takes when evidence is ambiguous* (provenance-tagged).
- **Embedding stage:** judgement about *what rule maps features to a reduced quantity*. Encoded in the rule definition, not the execution.
- **Score stage:** judgement about *which embeddings matter and by how much*. Encoded in the weight matrix.

A disagreement that cannot be decomposed into changes at one or more of these three layers is not actionable in V2 — it must first be reduced to a layer-specific claim before debate can proceed.

---

## Scope of Behavior Changes

### New artifacts to create
- Per-concept feature vector files (one per concept, fixed schema, provenance-tagged).
- Shared evidence corpus (world-facts with citations, referenced by ID).
- Embedding rulebook — named rules with input feature list, output, and computation (code or fixed prompt).
- Weight matrix configuration — separate from rulebook, separate from features. Designed to hold multiple named matrices (`default`, `bet:*`) sharing the same embedding-name vocabulary.
- A scenario catalog — named bets, the embeddings each scenario reweights, and a short rationale per scenario.
- A V1→V2 mapping document showing which current C-criteria carry forward and how they decompose.

### Existing artifacts affected
- `prompt_templates/config/scoring_framework.md`: replaced by the three-layer artifacts.
- `prompt_templates/score.md`: replaced by feature-extraction + embedding-execution prompts (or code).
- `prompt_templates/calibrate.md`: most Q1-Q7 steps become unnecessary; the residue (if any) collapses into the embedding rulebook.
- `scripts/lib/scoring.py`: refactored — the C2/C6/heritage lookups become first-class embedding rules in the new framework.

### Behavior changes by workflow stage
- Per-concept scoring: produces a feature vector and (deterministically) an embedding vector. No final score is produced in this pass.
- Aggregation: a separate, fast stage applies the weight matrix to embeddings.
- Calibration: largely replaced by the determinism guarantee. Cross-concept consistency becomes a property of the rulebook, not a post-hoc fixup.

---

## Non-Goals / Out of Scope

- **Enumerating the V2 feature set.** This concept defines the architecture and contracts. The specific features, embedding rules, and weights are a follow-on exercise.
- **Choosing the final score dimensions.** The number and meaning of final dimensions will evolve as embeddings reveal what is discriminating; not pinned here.
- **Changing the investigation strategy.** OVERVIEW.md research questions and comparison axes are unchanged.
- **Retrofitting V1 outputs.** V1 scores remain frozen as a published artifact; V2 starts fresh.
- **Building a UI.** Inspection of features/embeddings/weights can start as plain files.

---

## Assumptions & Prerequisites

- Per-concept research dossiers (under `exploration/concept_analysis/analyses/`) remain the source material for feature extraction.
- The 36-concept set and `table.csv` taxonomy columns are stable enough to seed the feature schema.
- Most current C-criteria can be decomposed into features + embeddings without losing analytical content. A few (e.g., C8 Data Adequacy) may need rethinking, since they describe the *quality of evidence* rather than the concept itself.

## Open Questions

1. Where does C8-style "data adequacy" live? It's a property of the dossier, not the concept. Possibly a separate meta-layer over the feature vector (per-feature confidence already partially answers this).
2. How are *missing* features handled in embeddings — fail loudly, propagate a sentinel, or imply a tier-1 default?
3. Should embeddings that involve LLM evaluation produce a structured rationale alongside the value, or is the reproducibility contract enough?
4. How does V2 coexist with V1 during migration — parallel pipelines, hard cutover, or feature-by-feature?
5. What tooling enforces the contracts? (E.g., a feature-schema validator, an embedding-rule registry, a divergence-test runner for LLM-backed rules.)
6. **Peer-group sanity-checking under determinism.** V1's calibration Q6 enforced peer-group consistency (comparable concepts get comparable scores). Determinism alone doesn't dissolve this concern — if two tokamaks legitimately differ on `aspect_ratio` but score very differently on a derived embedding, the right question is "does the embedding rule discriminate correctly," which is a meta-review of the rulebook, not a calibration of the run. Open whether this becomes (a) a one-time rulebook audit before V2 ships, (b) an ongoing review process, or (c) something the scenario catalog itself surfaces.
7. **Feature schema evolution.** When a feature is renamed, retyped, or added, what happens to (a) already-extracted feature vectors, (b) embedding rules that consume the old name, (c) already-computed scenario score vectors? Likely answer: schemas are versioned, embeddings declare which schema version they consume, and a re-extraction is required when an embedding bumps its consumed-schema-version. Needs spec-level treatment.
8. **Rule and weight matrix versioning.** Embedding rules and weight matrices both need version identifiers so that a stored score vector can be traced to the exact rules and weights that produced it. Format and lifecycle (when does a version bump force a re-run?) are open.

---

## Next-Stage Handoff

**Settled here:**
- Three explicit layers: features → embeddings → scores.
- Features are flat scalars with separate provenance/confidence tags (not tuples).
- World-facts live in a shared evidence corpus, not inlined per concept.
- Embeddings are reproducible: code by default, LLM permitted only under an explicit reproducibility contract (pinned model, fixed prompt, T=0, declared divergence bound, divergence treated as a defect).
- The weight matrix is a separate artifact, independently editable.
- The framework supports multiple named weight matrices (scenarios / bets); the same embeddings feed each one.
- Scenarios directly serve the coverage and uniqueness portfolio frames in `down_select/concept_part2.md`; irreducibility remains a separate analytical step.
- V2 is a refactor, not a patch. V1 scores remain a frozen historical artifact.

**Needs spec next:**
- Concrete schema for the feature vector — required fields, types, provenance tag vocabulary.
- Format for the evidence corpus — entry schema, citation contract, how embeddings reference entries.
- Embedding rulebook format — rule definition, inputs, output type, execution mode (code vs. LLM-with-fixed-prompt).
- Weight matrix format and the small set of final dimensions to start with.
- Scenario / bet catalog format — how scenarios are named, what they reweight, how they reference embedding IDs, and how the scenario-conditioned score outputs are organized for the down-select step.
- A V1→V2 carry-forward map: for each current C-criterion and sub-factor, what features and embeddings replace it.
- A treatment for "data adequacy" (C8) — either repositioned as a meta-property of the feature vector, or kept as its own embedding.

**Decomposition guidance:**
- Likely splits into (a) feature-vector spec + first migration of `table.csv` columns, (b) evidence-corpus spec + seeding from V1 C7 citations, (c) embedding rulebook + porting C2/C6/η_th lookups as the first rules, (d) weight matrix + initial scoring dimensions, (e) per-concept extraction pipeline. Items (a)–(c) can proceed in parallel once contracts are spec'd; (d) and (e) follow.
