# Concept: Automated Concept Analysis

**Created:** 2026-03-20
**Status:** Draft

---

## Problem Statement

The Fusion TEA project has 38 fusion concepts that each need a qualitative concept analysis (per the concept analysis brief). Approximately 9 have been completed by hand, leaving ~29 remaining. The manual process — researching each concept across multiple dimensions (data availability, modeling challenges, subsystem maturity, materials/supply chain) — takes significant analyst time and produces variable depth depending on who writes it and what sources they find.

Each concept already has a Phase 1a dossier with structured data across 12 differentiation columns, citations, confidence levels, and extracted source documents. This existing data is a strong starting point but doesn't cover the deeper qualitative assessment the brief requires. The analysis also needs to be scoped broadly enough to capture the key parameters, cost drivers, and data points that would feed a future Deliverable 2 (quantitative LCOE model).

The remaining ~29 concepts need to be analyzed consistently, with systematic identification of data gaps and source needs, at a pace that manual analysis cannot sustain.

---

## Success Criteria

When this work is complete:

1. **Holdout validation passes** — For 2-3 concepts done by hand but withheld from the agent, the agent-produced analysis is scored against the human version on four dimensions: (a) factual accuracy — same key facts, no fabricated claims; (b) gap identification — agent finds ≥80% of the same data gaps the human identified; (c) LCOE parameter capture — same quantitative values extracted, with correct citations; (d) analytical depth — key insights and challenges surfaced. A holdout "passes" if no major factual errors and ≥3 of 4 dimensions are rated adequate by a reviewer.

2. **Consistent output structure** — Every agent-produced analysis follows the same section structure, covers all required dimensions, and uses the same quality standards (confidence ratings, citation practices, gap documentation).

3. **Data gap inventory is actionable** — Each analysis explicitly identifies: (a) what data was found, (b) what data is missing but needed for LCOE modeling, (c) what specific PDFs/papers/sources would fill the gaps, and (d) whether the gap is "truly unknown," "proprietary," or "not yet sourced." Source recommendations reference only publications that exist in the Phase 1a sources, known databases (e.g., OSTI, arXiv), or are flagged as "unverified suggestion — confirm before searching."

4. **LCOE-relevant parameters are captured** — Beyond the qualitative narrative, each analysis extracts and structures the quantitative parameters needed for Deliverable 2: published cost estimates, performance targets (Q, power output, efficiency), component lifetimes, maintenance intervals, capacity factor assumptions, and scaling basis. Every quantitative value carries a citation back to a specific source. Values without citation are flagged as "estimated" or "inferred" with basis stated.

5. **Agent output is reviewable, not final** — The agent produces a draft that a human can review and refine, not a black-box final product. The human review checkpoint is explicit in the workflow. Review time will vary by concept data richness — the target is that the agent does the synthesis work and the human validates rather than rewrites.

6. **Cross-concept consistency** — Concepts that share subsystems, physics, or cost structures (e.g., two D-T tokamaks, or two concepts using FLiBe blankets) use consistent assumptions unless a stated reason justifies divergence. Reused models and assumptions are explicitly attributed to their source analysis. A reviewer can trace any shared assumption back to where it was first established and approved.

7. **Approval gate is enforced** — Only explicitly approved analyses enter the reuse pool. The agent never references its own draft output or unapproved analyses from other concepts as authoritative input.

8. **Thin-data concepts handled gracefully** — For concepts where Phase 1a confidence is low or data is sparse (Opaque/Limited availability), the agent produces a shorter analysis that honestly reflects what's known, explicitly states what cannot be assessed, and provides a more detailed gap report. It does not fill gaps with plausible-sounding but unsupported claims.

---

## User Stories

### Analysis Production

**US-1: Run analysis for a single concept**
As a researcher, I can point the agent at a specific concept (e.g., "06-magnetic-mirror") and get a draft qualitative analysis that covers all brief sections, so that I can review and refine it instead of writing from scratch.

**US-2: Run analysis for a batch of concepts**
As a researcher, I can run gap checks across all remaining concepts in one batch, review the consolidated gap report, then run full analyses in a second batch, so that human review happens at two natural batch boundaries rather than per-concept.

**US-3: Compare agent output to hand-done analysis**
As a project lead, I can compare agent-produced holdout analyses against the human versions side-by-side, so that I can assess quality and decide whether the agent output meets the bar.

### Data Gap Management

**US-4: Get a gap report before full analysis**
As a researcher, I can run a "gap check" mode that reviews existing Phase 1a data and identifies what additional sources would improve the analysis, so that I can download PDFs and extract them before the full analysis run.

**US-5: Review and act on gap inventory**
As a researcher, I can see a structured list of missing data per concept with specific source recommendations (paper titles, URLs, company publications), so that I can efficiently prioritize which sources to acquire.

### Approval & Reuse

**US-6: Approve a completed analysis**
As a reviewer, I can mark a reviewed D1+ analysis as "approved" (via a deliberate action — status change, directory move, or similar), so that it becomes part of the reuse pool for subsequent concept analyses.

**US-7: Agent references prior approved work**
As a researcher, when I run the agent on concept N, it reads all previously approved analyses and reuses shared assumptions, models, and cross-references where applicable, so that the set of analyses is internally consistent rather than independently derived.

**US-8: See what was reused vs. novel**
As a reviewer, I can see which parts of an analysis were informed by or adapted from a prior approved analysis (e.g., "BOP cost model adapted from concept 01"), so that I can verify the reuse is appropriate and trace assumption provenance.

### Quality Assurance

**US-9: Validate via holdout comparison**
As a project lead, I can run the agent on holdout concepts, then score the output against the human version on the four holdout dimensions (factual accuracy, gap identification, LCOE parameter capture, analytical depth), so that I have an objective basis for deciding if the agent output meets the quality bar before running the full batch.

---

## Key Concepts

### 1. Expanded Deliverable 1 ("D1+")

The agent produces a qualitative analysis following the brief's Deliverable 1 structure — but expanded to systematically capture the quantitative parameters and cost driver data that Deliverable 2 would need. This means the analysis not only narrates data availability and challenges, but also extracts and structures:
- Published capital cost estimates or analogues (by CAS category where possible)
- Operating cost drivers with any available quantitative basis
- Energy conversion pathway specifics (cycle type, efficiency claims)
- Capacity factor assumptions and maintenance intervals
- Performance targets (Q, fusion power, plant output)
- Scaling basis (published plant studies, system code outputs)

This structured data capture transforms D1 from a narrative-only document into a structured assessment that directly feeds D2 scoping.

### 2. Two-Phase Workflow (Gap Check → Full Analysis)

Rather than running the full analysis blindly, the workflow has an explicit checkpoint:

**Phase A — Gap Check**: Agent reviews existing Phase 1a data (dossier, extracted sources, schema) and produces a gap report: what's covered, what's missing, what specific sources would help. Human reviews, downloads/extracts additional sources if warranted.

**Phase B — Full Analysis**: Agent produces the complete D1+ analysis using all available data. Human reviews the draft (~15-30 min per concept).

This two-phase approach avoids wasted effort analyzing concepts where critical data is missing and gives the human a natural intervention point.

### 3. Phase 1a Data as Foundation

Each concept already has:
- A structured dossier with 12 column values, per-cell confidence, citations, and notes
- 1-3 extracted source documents per iteration (markdown from PDFs/websites)
- A changelog documenting corrections across iterations
- Gap documentation identifying what couldn't be resolved

The agent starts here — not from scratch. The existing data provides the factual foundation; the agent's job is to synthesize it into the broader qualitative assessment and identify what additional information is needed for the deeper analysis.

### 4. Grounded Analysis (Anti-Hallucination)

The highest-risk failure mode is the agent confidently stating technical facts or quantitative values that aren't in the source material. This is especially dangerous for D1+ quantitative parameter capture, where a fabricated cost estimate or performance target could propagate into D2 models.

Mitigations:
- **Source-grounded claims only**: Every factual claim must trace to a specific Phase 1a source or extracted document. Claims without citation are flagged as "inferred" with reasoning stated.
- **No fabricated source recommendations**: Gap reports only recommend sources that appear in Phase 1a citations, known databases (arXiv, OSTI), or are explicitly flagged as "unverified — confirm existence before searching."
- **Honest uncertainty**: When data doesn't exist, the analysis says so. Thin sections are acceptable; plausible-sounding fabrication is not.
- **Reviewer protocol**: Human review focuses on verifying citations actually support the claims made, not re-researching the topic. The agent's job is to make this verification easy by providing specific source references.

### 5. Formal Approval Lifecycle

Each D1+ analysis has an explicit status: **draft** → **approved**. The mechanism (status header in the document, directory move, or both) is an implementation detail, but the behavior is:

- Agent output always starts as a draft
- A human reviews and may edit the draft
- The human explicitly marks it as approved (not implicit — requires a deliberate action)
- Only approved analyses are visible to the agent as reusable prior work (see concept 6)
- The approval status is machine-readable so the agent and batch tooling can distinguish draft from approved

This creates a clear quality gate: nothing propagates into the reuse pool or downstream work until a human has signed off.

### 6. Cumulative Reuse Across Concepts

On the Nth concept analysis, the agent should read and reference all previously **approved** analyses. Fusion concepts share significant common ground — balance of plant, tritium breeding approaches, magnet technologies, thermal cycles, cost estimation methodologies, and LCOE model structures recur across concepts. Reuse is preferred over independent re-derivation because it:

- **Prevents divergent assumptions** — if two D-T tokamak variants use different BOP cost assumptions for no reason, that's a bug. The agent should adopt consistent assumptions across related concepts and explicitly note when/why it departs.
- **Enables cross-referencing** — "This concept uses FLiBe blanket breeding, similar to CFS (see concept 01 analysis). Key differences: ..."
- **Accumulates shared models** — mathematical models, cost estimation approaches, or efficiency calculations developed for one concept can be reused or adapted for related concepts rather than re-derived from scratch.
- **Builds progressively** — earlier analyses for well-documented concepts (e.g., CFS tokamak, NIF) establish patterns that accelerate analysis of less-documented concepts in the same family.

This means concept ordering matters. Well-documented, data-rich concepts should be analyzed first within each confinement family, so their approved analyses serve as foundations for thinner concepts. The batch workflow should account for this ordering rather than treating all concepts as independent.

### 7. Holdout Validation

2-3 of the hand-done analyses are withheld from the agent (it doesn't see them as exemplars). The agent produces its own analysis for these concepts, and the team compares agent vs. human output. This tests:
- Factual accuracy (does the agent get the same facts?)
- Analytical depth (does the agent surface the same insights?)
- Gap identification (does the agent find the same missing data?)
- LCOE-relevant parameter extraction (does it capture the same numbers?)

---

## Scope of Behavior Changes

### New artifacts to create
- Automated analysis runner (script, prompt, or agent configuration — implementation TBD in design phase)
- Per-concept D1+ analysis output files (in `exploration/concept_analysis/`)
- Per-concept gap reports (Phase A output)
- Holdout comparison report with scoring on the four validation dimensions

### Existing artifacts to use (read-only)
- `exploration/phase_1a/research/NN-concept-name/dossier.md` — per-concept structured data
- `exploration/phase_1a/research/NN-concept-name/iter-XX/sources/` — extracted source documents
- `exploration/phase_1a/schema.md` — controlled vocabulary and rules
- `exploration/concept_analysis/concept_analysis_brief.md` — the analysis brief

### Workflow stages
- **Gap check**: New capability — agent reviews existing data and produces actionable gap report
- **Full analysis**: New capability — agent synthesizes Phase 1a data + approved prior analyses + sources into D1+ write-up
- **Human review + approval**: Reviewer edits draft, then explicitly approves — analysis enters the reuse pool
- **Cumulative batch**: Concepts analyzed in a deliberate order (data-rich first per family), with each approved analysis available to subsequent runs
- **Holdout comparison**: Structured comparison of agent vs. human output on four scoring dimensions

---

## Out of Scope

- **Deliverable 2 implementation** — The LCOE model code itself is not built here. D1+ captures the inputs and parameters D2 would need, but doesn't produce the model.
- **Automated source acquisition** — The agent identifies what sources are needed but doesn't download PDFs or access paywalled content. That's a human step at the checkpoint.
- **Schema evolution** — The Phase 1a schema (v0.2.3) is treated as fixed input. If the agent finds concepts that don't fit the schema, it flags them but doesn't propose schema changes.
- **Phase 2a integration** — The reasoning tree work is a separate analytical track. D1+ analyses don't need to reference or validate against the constraint registry.
- **Fully autonomous end-to-end pipeline** — Human review after gap check and after full analysis are explicit design points, not automation gaps to close later.

---

## Assumptions & Prerequisites

- Hand-done exemplars will be provided for the agent to learn the expected quality bar
- The list of which concepts have been done by hand (vs. remaining) will be provided
- 2-3 hand-done concepts will be designated as holdouts for validation
- Phase 1a dossiers exist for all 38 concepts with at least 1 iteration of research
- Extracted source documents in `iter-XX/sources/` are readable markdown
- **Primary data source is Phase 1a** — the agent synthesizes from existing dossiers and extracted sources. Web search may be used to verify or supplement but is not the primary research method. This keeps output reproducible and grounded in curated data.
- `uv run` environment is available for any scripting

## Open Questions

1. What is the exact output format for D1+ analyses? Should it mirror the brief's section structure exactly, or is a modified structure acceptable if it better serves D2 data capture?
2. For the gap check phase, what's the threshold for "worth downloading a new source"? Should the agent be conservative (flag everything) or selective (only flag gaps that would materially change the analysis)?
3. For academic/government concepts without an active company (e.g., NIF commercialization, state-backed tokamaks), should the analysis structure adapt, or use the same template with "N/A" for company-specific sections?

---

## Decomposition Guidance

This concept naturally splits into 4-5 work items:

1. **Output template + exemplar calibration** — Define the D1+ output format using hand-done exemplars as calibration targets. Define the approval mechanism. Test on 1-2 known-good concepts.

2. **Gap check capability** — Build the Phase A workflow: review Phase 1a data, produce structured gap report. Test on a few concepts.

3. **Full analysis pipeline with reuse** — Build the Phase B workflow: read Phase 1a data + approved prior analyses, produce D1+ analysis with reuse attribution, save as draft. Include holdout validation runs.

4. **Concept ordering strategy** — Determine the optimal analysis order across the ~29 remaining concepts (data-rich first per family). This informs the batch execution sequence.

5. **Batch execution + review** — Run across remaining concepts in order, with approve-then-continue loop. Iterate on prompt if systematic issues appear.

Items 1-2 can proceed in parallel. Item 3 depends on 1. Items 4-5 depend on 2 and 3.
