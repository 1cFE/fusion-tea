# Design: Concept Trace Pipeline

**Status:** Proposed
**Owner:** Reid W
**Created:** 2026-05-03
**Updated:** 2026-05-03 — reframed around C1-C8 inheritance

---

## Overview

A pipeline that turns the existing per-concept fusion analyses *plus the calibrated C1-C8 sub-scores* into structured stage-gate assessments — one per concept, combining numerical/categorical factor judgments with focused narrative — to feed the down-selection methodology defined in `.project/concepts/down_select/concept_part2.md`. Two ideas anchor the design: the assessment is composed bottom-up from atomic factor judgments rather than generated whole, so iteration on rubric quality is cheap; and the C1-C8 pipeline has already produced calibrated outputs that map onto roughly half the Stage-gate factor surface, so the new pipeline inherits that work rather than re-scoring it.

---

## Problem

The down-selection methodology asks each fusion concept how it would pass through four sequential commercialization gates, where each gate carries its own dominant failure modes and ecosystem leverage opportunities. Producing this assessment by hand for ~38 concepts is impractical at the required depth; doing it as a single monolithic prompt per concept makes inconsistency between concepts inevitable, because the model has no anchored reference to score against and no constrained interface forcing it to agree with itself across reruns.

The closest existing infrastructure — the C1-C8 composite scoring pipeline — answers a different question (which concepts rank highest on a global score) than the down-selection methodology asks (where does each concept die, and what carries it along). Its output is a single weighted aggregate per concept; Stage-gate produces a per-concept narrative trace plus a 2D coordinate (dominant failure mode × dominant leverage). The two are different deliverables.

But the C1-C8 *inputs* and *intermediate calibrated sub-scores* overlap meaningfully with Stage-gate's factor surface. C3 (supply chain learning) covers the underlying signal in F2.d / F3.a / F4.c; C1 (modularization) covers F3.b / F4.d; the C7 risk matrix's 14 cells cover the F-carriers (tritium, first-wall, HTS) directly; C8 covers data sufficiency. Roughly half the factors have direct or near-direct C1-C8 coverage. The C1-C8 pipeline has also already done the cross-concept Pass-2 calibration walk (Q1-Q7: peer-group medians, sub-factor arithmetic checks, mandatory-binary overrides, anti-leniency, audit-trailed adjustments) — work the new pipeline would otherwise need to redo.

A useful pipeline must therefore (a) inherit the calibrated C1-C8 outputs where the mapping is strong, (b) fresh-score only the gap (FOAK affordability, regulatory factors, distinct E-factors), and (c) let the assessment evolve as anchors and rubrics tighten. Iteration cost has to be proportional to what changed: tightening one factor's anchor or one C1-C8 sub-score should rerun only the affected work, not invalidate everything across thirty-eight concepts.

---

## Goals

- Deliver per-concept stage-gate assessments that combine pole-identified factor judgments with focused narrative tailored to the methodology's failure-mode and leverage axes
- Inherit calibrated C1-C8 sub-scores where the factor mapping is strong; fresh-score only the coverage gap
- Keep judgment consistent across concepts via inheritance from the already-calibrated C1-C8 surface and via shared anchored rubrics where fresh scoring is required
- Make iteration on prompt design cheap — a change to one factor's anchor or one upstream C1-C8 score should rerun only the affected work
- Compose the assessment bottom-up so atomic outputs can be reread, reused, or selectively regenerated without rebuilding the whole trace
- Enable cross-concept calibration as a discrete second pass for the fresh-scored factors (the inherited factors inherit calibration)

## Non-Goals

- Replacing the existing concept-analysis pipeline — this consumes its outputs, doesn't replicate them
- Producing new domain knowledge — works from existing analyses, extracted explorer data, and a one-time ecosystem-research artifact for E-factors
- Implementing the spanning selection algorithm itself — emits the coordinates the spanning algorithm reads
- Replicating the C1-C8 composite ranking as an output — different methodology, different deliverable. C1-C8's calibrated *inputs* are reused; its single-aggregate-per-concept *output* is not

---

## Design Principles

### 1. Compose the assessment; don't generate it whole.

The trace is built bottom-up from atomic factor judgments. Each judgment knows about itself and one concept; nothing more. The narrative composition layer reads what the factors said and arranges them into a story — it never reopens a scoring decision. This separation lets us iterate on factor judgment and narrative voice independently, and constrains the model: the narrative cannot drift from the scores because it never sees the underlying evidence directly.

### 2. Anchor every judgment.

Every prompt is anchored. For inherited factors, the anchor is the calibrated C1-C8 sub-score and the cross-concept Pass-2 calibration rationale that produced it — Claude reads a known-good number with a known-good justification and identifies the pole. For fresh factors, the anchor is a literature passage plus a concrete rubric tied to known reference cases (solar PV, US nuclear, specific fusion concepts whose scores have been calibrated). Without anchors, "subjective but quantified" collapses into noise.

### 3. File state is the truth.

Every artifact lives on disk in a known location with a known schema. Staleness is computed from input hashes and template versions; reruns regenerate only what's stale. No in-memory state survives between runs. Inherited factors hash both the factor template and the upstream C1-C8 source artifact, so a recalibration of C3 mid-pipeline correctly invalidates F2.d / F3.a / F4.c outputs across all concepts.

### 4. Claude judges; Python arranges.

Anything that can be computed deterministically — composing a stage narrative's structural skeleton, identifying the lowest-stakes-weighted factor as dominant failure mode, formatting the trace document — is Python. Anything requiring judgment against literature or rationale — pole-identifying an inherited factor, scoring a fresh factor — is Claude. This bounds the surface where regression can occur and follows the discipline already established in the C1-C8 pipeline.

### 5. Inherit calibrated work; fresh-score only the gap.

Where C1-C8 sub-scores already cover a factor's underlying signal — supply chain, modularization, plant complexity, evidence-tier risk per function, data adequacy — the new pipeline reads the calibrated value plus its rationale and asks Claude to *identify the pole* (failure vs. leverage) and *tag slack/bottleneck per stage*, not to re-score the underlying signal. Where C1-C8 has no coverage (FOAK affordability, regulatory state, distinct E-factors), the pipeline fresh-scores from anchored rubrics. Two factor classes, one composition framework above them.

---

## Architectural Bets

- **Three composable layers, not one monolithic prompt.** Atomic factor judgment → stage narrative → concept assembly. The alternative — one big prompt that produces the whole trace — would be cheaper to build but impossible to iterate on factor-by-factor and impossible to keep consistent across concepts.
- **Two factor classes, one schema.** Inherited factors stage-decompose calibrated C1-C8 sub-scores via pole identification; fresh factors fill the coverage gap. Their templates have different shapes but their JSON outputs share a schema and their stage-narrative consumers don't care which class produced a given factor.
- **Pole identification, not re-scoring, on inherited factors.** Claude reads a calibrated sub-score plus its rationale, tags pole (failure / leverage) on ecosystem-relational F-factors, tags slack/bottleneck where applicable, and decomposes a single signal across stages where the C1-C8 score collapses three eras into one number (canonical case: C3 → F2.d / F3.a / F4.c). The calibrated value is treated as ground truth — Claude doesn't argue with it.
- **Templates and inputs are content-addressed; outputs declare what produced them.** Lets staleness be computed mechanically rather than guessed, and lets reruns target the exact slice that changed without manual bookkeeping. Inherited factors include the upstream C1-C8 artifact in the hash chain.
- **Calibration concept first; full sweep last.** Anchor the rubric on one well-documented concept (01-hts-compact-tokamak); validate the prompts produce sensible pole identifications and fresh scores; only then run on all 38. Premature scaling burns Claude calls on prompts that will change.

---

## Core Model

### Factor

The atomic judgment unit. One factor template + one concept's evidence → one factor JSON containing the per-stage assessment for that factor: pole (failure / leverage) where applicable, slack/bottleneck tag where applicable, score (1-5) for fresh factors only, rationale, confidence, and the calibrated-source coordinates (which C1-C8 artifact, if any, anchored the assessment). Factor codes (`F2.a`, `F3.d`, `E2.a`, etc.) come from `concept_part2.md`. A factor knows nothing about other factors, other stages, or other concepts. Stored at `traces/{concept_id}/factors/{factor_code}.json`.

**Two factor classes:**

- **Inherited factors.** Map onto a calibrated C1-C8 sub-score or a C7 risk-matrix cell. Template inputs: the calibrated value, its sub-factor rationale from synthesis Section 8, the matching cross-concept calibration adjustments rows from `scores/calibrated_scores.md`, and a pointer to the relevant analysis section. Template task: identify pole, tag slack/bottleneck, decompose across stages where the inherited signal is stage-collapsed. Cheap, consistent by inheritance. Canonical examples: F3.b inherits C1 sub-factor 1 (construction mode); F2.d / F3.a / F4.c jointly inherit C3.A/B/C; the F-carriers lift directly from C7 risk-matrix rows.
- **Fresh factors.** No C1-C8 coverage. Template inputs: anchored rubric, analysis sections, and (for E-factors) the cross-concept ecosystem-research artifact. Template task: score from evidence in the original design's shape, then pole-identify. Canonical examples: F2.a (FOAK capital), F2.b (build time), F2.c / F3.d (regulatory), all E-factors.

### Stage Narrative

A composer, not a scorer. Reads the four-to-six factor JSONs for one stage and writes a 200-400 word narrative plus dominant-failure and dominant-leverage tags for that stage. The stage prompt is constrained: it never reopens factor decisions, only arranges what the factor layer produced. Doesn't care whether a factor was inherited or fresh — both classes produce the same JSON shape. Stored at `traces/{concept_id}/stages/stage-{N}.md`.

### Concept Trace

The assembled output. A markdown document combining the four stage narratives, the carriers narrative, a Stage-1 discount entry, and a one-paragraph executive summary identifying the concept's dominant failure mode and dominant leverage across all stages. Built mostly mechanically from stage outputs. Stored at `traces/{concept_id}/trace.md` with a sidecar `coords.json` containing the dominant-coordinate identifiers for the spanning algorithm to read.

### Anchor Library

The shared body of literature passages, reference-case scoring examples, and few-shot calibration examples for *fresh factors*. Inherited factors don't need anchors — their anchor is the calibrated C1-C8 value. Lives in one location and is referenced by fresh-factor templates via the existing `{{@path}}` inclusion syntax. When an anchor passage updates, every fresh-factor template that references it transitively invalidates dependent outputs.

### C1-C8 Source Artifacts

The set of upstream files inherited factors read. Hashed for staleness. Includes:
- `exploration/concept_analysis/scores/calibrated_scores.json` — Pass-2 calibrated C1-C8 per concept
- `exploration/concept_analysis/scores/calibrated_scores.md` — adjustments report (concept × question × criterion × original × adjusted × justification)
- `exploration/concept_analysis/analyses/{concept_id}/synthesis.md` — Section 8 sub-factor breakdown tables, C7 risk matrix, YAML scores block

### Run Manifest

Per-concept record of which template versions, which input file hashes, and which C1-C8 source-artifact hashes produced each artifact. Drives staleness computation. When a factor template changes, the manifest tells the runner which factors are stale; when a concept's analysis or its calibrated C1-C8 score changes, which factors and stages need rerun. Stored at `traces/{concept_id}/manifest.json`.

---

## Required Invariants

### Composition

- A factor template produces exactly one factor JSON; never two.
- A stage narrative consumes only factor JSONs (and a stage prompt template). It never reads concept analyses, explorer JSONs, or C1-C8 artifacts directly.
- The dominant-coordinate identification in `coords.json` derives mechanically from factor outputs; it is not a Claude judgment.
- For inherited factors that stage-decompose a single C1-C8 sub-score, the per-stage decompositions must aggregate-back to within tolerance of the source value (the reconstruction invariant — see Validation Strategy).

### State and staleness

- Every artifact records the template hash, input hashes, and (for inherited factors) the upstream C1-C8 source-artifact hash that produced it.
- A change to a template invalidates exactly the artifacts produced from that template version.
- A change to a concept's input analysis invalidates that concept's factor artifacts but not other concepts'.
- A change to a calibrated C1-C8 sub-score invalidates inherited factors that read it (across all concepts whose factor used the changed sub-score), plus their downstream stages and concept assemblies. Fresh factors are unaffected.

### Output schema

- Every factor JSON validates against the factor schema before being written.
- For fresh factors, score values are integers 1-5; confidence values are an enum (high / medium / low).
- For inherited factors, the calibrated-source coordinates field is required (which C1-C8 artifact and which sub-key).
- Pole tags appear on ecosystem-relational F-factors only; slack/bottleneck tags appear only where `concept_part2.md` defines them.

---

## How It Works

### Initial run for a single concept

The runner walks the factor template directory, executes each factor's prompt, validates and writes the factor JSON. The prompt's input depends on the factor's class:

- **Inherited factors** receive the calibrated C1-C8 sub-score (from `calibrated_scores.json`), the synthesis Section 8 sub-factor breakdown and rationale (or the relevant C7 risk-matrix row), the matching cross-concept calibration adjustments rows from `calibrated_scores.md`, and a pointer to the relevant analysis section. Claude pole-identifies, slack/bottleneck-tags, and stage-decomposes — not re-score.
- **Fresh factors** receive an anchored rubric, the relevant analysis sections, and (for E-factors) the cross-concept ecosystem-research artifact. Claude scores from evidence in the original design's shape, then pole-identifies.

After all factors for one stage are present, the stage narrative prompt runs against those JSONs and writes the stage markdown. After all stages are present, the concept assembler reads stages and produces the trace and coords. Each step is independent; failures at one factor don't block others.

### Iteration: tweaking one factor's anchor (fresh)

The user edits the anchor passage referenced by, say, the F2.c factor template. The runner detects the changed hash, marks all F2.c factor outputs across concepts as stale, marks all stage-2 narratives as stale (downstream of those factors), marks all concept assemblies as stale. Invoking the runner with no concept filter regenerates only the stale slice. Other stages survive untouched.

### Iteration: a C1-C8 recalibration changes an upstream sub-score (inherited)

The C1-C8 calibration is rerun and `calibrated_scores.json` updates. The runner hashes the new value, marks every inherited factor that reads it as stale (could span F2.d / F3.a / F4.c if C3 changed for one concept), marks dependent stages and concept assemblies stale. Fresh factors and the C1-C8 → factor mapping itself are unaffected. The per-concept rerun cost is bounded by which factors actually inherited from the changed sub-score.

### Iteration: improving a stage rollup template

The stage-2 narrative template changes. Factor JSONs are unaffected. All stage-2 narratives across concepts regenerate; concept assemblies depending on them regenerate. The dominant Claude expense (factor judgment) is preserved.

### Cross-concept calibration pass (fresh factors only)

After all concepts have factor JSONs, an optional calibration pass runs on a per-fresh-factor matrix (e.g., all 38 concepts' F2.a scores side-by-side). Inherited factors don't need this — they inherited C1-C8's Pass-2 calibration. Modeled on the C1-C8 calibration walk: arithmetic checks for fresh sub-factors, peer-group median pulls (peer groups defined per-factor where they differ from C1-C8's defaults), revert-or-keep audit. Adjustments applied by editing factor JSONs directly; manifest records that the artifact was post-calibration-adjusted with provenance.

---

## Edge Cases and Failure Modes

- **Concept has insufficient data for a fresh factor.** Confidence flag set low; rationale notes the gap. Factor still produces a best-estimate score but flags itself for human review. Down-selection algorithm can choose to filter low-confidence-dominant concepts.
- **Inherited factor's upstream C1-C8 sub-score has low confidence (e.g., calibration flagged it).** Inheriting factor records the flag in its rationale; downstream pole identification carries the caveat forward.
- **C1-C8 recalibration mid-pipeline.** Manifest hashing detects the changed source artifact; affected inherited factors regenerate. No silent inconsistency.
- **Two concepts produce identical fresh-factor scores from clearly different evidence.** Surfaces in the cross-concept fresh-factor calibration pass; addressed by tightening the rubric anchor and rerunning.
- **Reconstruction invariant violation on an inherited factor.** Stage decompositions aggregate-back outside tolerance of the source C1-C8 value. Two cases: (a) template bug (the decomposition rule is wrong); (b) the C1-C8 score genuinely doesn't decompose cleanly for this concept (e.g., C3 was scored against fleet-era reasoning while F2.d wants FOAK-era reasoning, and the analysis evidence diverges sharply). Surface as a review item rather than auto-correcting.
- **Stage narrative attempts to introduce new judgment claims.** Validators reject narratives that mention pole or score values not present in the input factor JSONs.
- **A new factor is added.** Existing concepts get missing-factor markers in their manifest; targeted rerun fills only the new factor.
- **Schema evolution.** New required field on factor JSON breaks old artifacts; manifest records schema version per artifact and runner can detect old-schema artifacts and rerun them.
- **The C1-C8 → factor mapping itself changes (e.g., F4.b is reassigned from inherited to fresh).** Treated as a template-class change; affected factor outputs regenerate from the new template shape.

---

## Vocabulary

- `factor` — atomic judgment unit, one of the F-factors or E-factors from `concept_part2.md`, codes like `F2.c` or `E3.a`
- `factor template` — prompt + (anchor or C1-C8 source pointer) + rubric for one factor; lives at `templates/factors/{code}.md`
- `factor JSON` — output of a factor template applied to one concept; schema-validated
- `inherited factor` — factor whose underlying signal is already covered by a calibrated C1-C8 sub-score; template's job is pole identification and stage decomposition, not re-scoring
- `fresh factor` — factor with no C1-C8 coverage; template scores from anchored rubric over analysis evidence
- `pole identification` — for ecosystem-relational F-factors, tagging whether the concept lands on the failure or leverage pole of the axis
- `stage decomposition` — for inherited factors that map a stage-collapsed C1-C8 sub-score (e.g., C3) onto multiple stage-gate factors (e.g., F2.d / F3.a / F4.c), the per-stage assignment of pole + slack/bottleneck for the inherited signal
- `calibrated sub-score` — the post-Pass-2 C1-C8 value (`scores/calibrated_scores.json`), used as ground truth for inherited factors
- `stage narrative` — composed markdown for one stage of one concept, derived only from that stage's factor JSONs
- `concept trace` — full assembled markdown document for one concept
- `coords.json` — sidecar containing the concept's dominant failure mode and dominant leverage identifiers
- `anchor` — for fresh factors only: literature passage or reference-case scoring example referenced by one or more factor templates
- `manifest` — per-concept record of template versions, input hashes, C1-C8 source-artifact hashes, and run history
- `slack / bottleneck` — qualifier on ecosystem-relational F-factors indicating whether the underlying supply ecosystem has headroom or is contested
- `reconstruction invariant` — for inherited factors that stage-decompose, the per-stage decompositions must aggregate-back to within tolerance of the source C1-C8 value

---

## Validation Strategy

- **Single-concept calibration.** Run on 01-hts-compact-tokamak; manually inspect inherited-factor pole identifications and fresh-factor scores against expected reference values; iterate prompts until calibration is satisfactory.
- **Contrasting-concept smoke test.** Run on 07-maglif and 08-frc-w-direct-conversion; verify factor outputs meaningfully diverge from the calibration concept where the underlying evidence diverges.
- **Reconstruction smoke test for inherited factors.** Per-stage decompositions of an inherited C1-C8 sub-score should aggregate-back to within tolerance of the source value: F2.d-pole + F3.a-pole + F4.c-pole stage-decompositions should reconstruct C3; F-carrier outputs should be consistent with the C7 risk matrix cells they reference. Drift surfaces a template bug or a concept where the C1-C8 score genuinely doesn't decompose cleanly.
- **Schema validation on every factor output.** Reject artifacts that don't conform.
- **Cross-concept consistency review for fresh factors only.** After the full sweep, the calibration pass flags inconsistencies; discrepancy rate is a measurable quality indicator over time. Inherited factors inherit C1-C8's calibration and don't need this pass.
- **Manual spot-checks at the trace layer.** Read 3-5 traces end-to-end; verify each actually narrates the down-selection question rather than restating the underlying analysis or the underlying C1-C8 score.

---

## Next-Stage Handoff

**Settled here:**
- Three-layer composition (factor → stage → concept).
- Output locations and the per-concept directory structure under `exploration/concept_trace/traces/{concept_id}/`.
- Reuse of the existing pipeline's runtime infrastructure (`lib/templating.py`, `lib/claude.py`, `lib/step_runner.py`, `lib/state.py`, `lib/validators.py`).
- Reuse of C1-C8 calibrated sub-scores and calibration adjustments as inherited-factor inputs; fresh scoring restricted to the coverage gap.
- Two factor classes (inherited / fresh) sharing one schema and one composition framework above them.
- For inherited factors, the operation is pole identification + stage decomposition, not re-scoring; the calibrated value is treated as ground truth.
- Dominant-coordinate identification is mechanical, not Claude-judged.
- Factor codes and stage definitions inherited from `concept_part2.md`.

**Spec/design detail still needed next:**
- **Inherited / fresh partition table.** Factor-by-factor: which C1-C8 artifact each inherited factor reads (synthesis Section 8 YAML / sub-factor table / C7 cell / calibration adjustments) and what the per-stage decomposition rule is. Sketched in chat; not yet captured here.
- Exact factor JSON schema — must accommodate both inherited (calibrated-source coordinates, pole, slack/bottleneck, no score) and fresh (1-5 score, pole, slack/bottleneck) shapes under one schema with a `class` discriminator.
- Anchor library structure for fresh factors — single source file vs. per-factor anchor file; inclusion-by-reference vs. inline copy at template-render time.
- For fresh factors, whether the input is the full analysis or pre-extracted sections.
- Cross-concept ecosystem-research artifact for E-factors — adjacent-industry market data per critical component (REBCO / FLiBe / pulsed-power / IMG / high-power lasers / etc.). One-time research shared across concepts; format and storage TBD.
- Manifest format and exact staleness-detection algorithm — must hash both the factor template and the C1-C8 source artifact for inherited factors.
- Tolerance for the reconstruction invariant on inherited factors.
- CLI surface — what subcommands the runner exposes, mirroring or diverging from `run_analysis.py`'s pattern.

**First risks to de-risk:**
- For inherited factors: pole identification + stage decomposition on a calibrated C1-C8 sub-score is more stable than fresh scoring would be (the calibrated value is anchored and Claude's judgment surface is narrower). If pole identification drifts run-to-run on the same input, the inheritance hypothesis is wrong and we'd need to re-score even where C1-C8 covers the surface.
- For fresh factors: anchored prompts produce stable, defensible scores on the calibration concept without rubric drift. Same risk shape as the original design.
- The reconstruction invariant on the canonical decomposition (C3 → F2.d / F3.a / F4.c on 01-hts-compact-tokamak) — does the stage-decomposed signal aggregate back cleanly, or does the C1-C8 score's stage-collapse make this unrecoverable?

---

## Summary

A three-layer pipeline that turns existing concept analyses and the calibrated C1-C8 sub-scores into structured stage-gate assessments. Inherited factors lift and decompose the C1-C8 work via pole identification; fresh factors fill the coverage gap (FOAK affordability, regulatory state, distinct E-factors). Atomic factor outputs compose upward into stage narratives and concept traces. File-based state with content-addressed staleness — including hashes of upstream C1-C8 source artifacts — lets iteration cost be proportional to what changed. The bet is that the C1-C8 calibration is robust enough to anchor pole identification, that the coverage gap is small enough to fresh-score affordably, and that the resulting two-class architecture is meaningfully simpler than re-scoring everything from raw analyses would have been.
