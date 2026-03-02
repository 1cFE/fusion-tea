# Modeling Requirements

Project-specific rules that all modeling work must follow. These extend the standard rules in [MODELING_GUIDE.md](MODELING_GUIDE.md) with requirements derived from the investigation scope ([OVERVIEW.md](OVERVIEW.md)).

Previous requirements (PR-001 through PR-007) archived to `archive/modeling_project/REQUIREMENTS.md`.

---

## Modeling Requirements

These define the patterns that all SysML v2 models in this project MUST follow. They exist to enable cross-concept comparison, maximize reuse, and maintain traceability.

### MR-1: CAS Hierarchy as Primary Cost Decomposition

All models MUST use the CAS (Cost Account Structure) hierarchy as the primary cost decomposition.

- **Rationale**: CAS is the one structural pattern known to work across MFE, IFE, and MIF concepts. It's the standard used by ARPA-E, the ARIES program, and industry-standard costing tools. Using a common decomposition is what makes cross-concept comparison possible.
- **What it enables**: Direct comparison of where money goes across concepts at the same structural level (CAS20 → CAS21-29 breakdown). Validation against industry-standard costing benchmarks where overlap exists.
- **Enforcement**: Model review — every cost-bearing element must map to a CAS category. Validation tooling should verify CAS coverage.

*Carries forward the useful core of archived DI-001.*

### MR-2: Standard Costed Component Interface

All cost-bearing components MUST implement a standard costed component interface with at minimum: `capital_cost`, and cost breakdown categories sufficient for cross-concept comparison.

- **Rationale**: A uniform interface is what enables automated cost rollup, cross-concept comparison, and systematic validation. Without it, each concept model is a one-off.
- **What it enables**: Aggregation up the CAS tree. Apples-to-apples comparison at any CAS level. Automated reporting and visualization. The traceability audit script (see MR-4) uses the presence of cost attributes to identify elements that require citations.
- **Enforcement**: Model validation — every part that contributes to cost must specialize the costed component interface. The specific attributes beyond `capital_cost` will be refined during modeling pattern development (MR-6).

*Carries forward the useful core of archived DI-003.*

### MR-3: Library Concept-Agnostic, Designs Concept-Specific

Library definitions (`models/library/`) MUST be concept-agnostic. Concept-specific values, assemblies, and parameters MUST live in `models/designs/{concept}/`.

- **Rationale**: Clean separation enables reuse. A turbine plant definition works for any thermal conversion concept. A magnet system definition works for any MFE concept. Only the parameterization and assembly differ.
- **What it enables**: Significant reuse across concepts — analysis of existing fusion costing codebases suggests ~60% of definitions are shared. New concepts reuse library definitions and only add concept-specific parts.
- **Enforcement**: Review — no reactor-type-specific parameter values in `library/`. Designs import from library and specialize; library never imports from designs.

*Carries forward the principle from archived AD-002.*

### MR-4: Traceable Citations on All Quantitative Values

All quantitative values in models — cost parameters, physics constants, material properties, performance assumptions, geometric values — MUST carry structured citations that resolve to source files in the repository or external codebases. Citations use the project's standard citation format:

| Field | Required | Description |
|-------|----------|-------------|
| `Source` | MUST | Repo-relative file path or absolute path to cited artifact |
| `Ref` | SHOULD | Location within source — line number(s) (`L42`, `L42-58`) or section heading (`## Section Name`) |
| `Basis` | SHOULD | What was derived and how (e.g., "CAS22 cost breakdown from Table 3", "Scaled from ITER using R^2.5") |

**Key rules:**
- `Source` MUST be a direct file path, not an abstract identifier (e.g., `knowledge/sources/hsu_et_al/output.md`, not "Hsu et al. 2020")
- Citations in SysML use doc comment fields. Citations in markdown use blockquote markers. See the traceability system spec for format details.
- Citations form transitive chains: a SysML model may cite a synthesis document, which cites a research report, which cites a source extraction. Each link must resolve.
- Parameters without source data MUST NOT be silently invented. They must be marked with explicit basis (e.g., `Basis: [ASSUMED] — industry typical value, no concept-specific data available`).

**Rationale**: LLM agents perform significant portions of the research and modeling. Without machine-checkable citations, there is no way to verify whether a number is sourced or hallucinated — and this applies equally to a plasma temperature, a material thermal conductivity, or a cost scaling factor. File paths are self-resolving — no lookup table needed.

**What it enables**: Automated traceability auditing. A reader can trace any number to its origin. Systematic updates when new sources are ingested.

**Enforcement**: `scripts/trace_audit.py` — scans models and documentation, parses citations, walks chains, and reports coverage gaps and broken links. See `.project/active/traceability-system/spec.md` for full system specification.

*Carries forward the useful core of archived DI-014. Supersedes the archived `data/traceability_matrix.csv` approach.*

### MR-5: Standard Output Schema for Cross-Concept Comparison

Models SHOULD produce a standard set of outputs that enables cross-concept comparison along the defined comparison axes (see [OVERVIEW.md](OVERVIEW.md#comparison-axes)).

- **Rationale**: The comparison axes (LCOE, capital cost by CAS, capacity factor, fuel cycle economics, technology readiness, estimation confidence, sensitivity-risk profile) are only useful if every concept model produces comparable outputs.
- **What it enables**: Automated cross-concept reporting. Dashboard visualizations. Consistent comparison methodology.
- **Enforcement**: To be defined. The output schema cannot be fully specified until taxonomy and concept analysis identify what's comparable. This requirement establishes the intent; the schema gets refined during modeling pattern work.
- **Current status**: Intent defined. Specific fields TBD — will be informed by taxonomy (what dimensions matter) and concept analysis (what's actually comparable across approaches).

### MR-6: Modeling Patterns Defined Before Production Models

The project SHOULD define documented modeling patterns — templates, conventions, and worked examples — for common structures BEFORE building production models. Pattern definition is a distinct step from model construction.

- **Rationale**: The archived coffee maker and solar battery demos proved that pattern validation prevents rework. Discovering that a cost rollup pattern doesn't work after building 5 concept models is far more expensive than validating the pattern once on a small example.
- **What it enables**: Consistent model structure across concepts. Faster concept modeling (follow the pattern, don't reinvent). Reduced risk of structural errors.
- **Enforcement**: Review — production models should reference the pattern document that governs their structure. Patterns should be validated with small examples before use in production.
- **Current status**: Intent defined. Pattern documents will be produced during the transition from taxonomy/concept analysis to model construction (see Investigation Process in OVERVIEW.md). The traceability citation format (MR-4) is one such pattern — defined before production use.

---

## Process Requirements

These define how the investigation progresses. The full process narrative is in [OVERVIEW.md — Investigation Process](OVERVIEW.md#investigation-process). These requirements are the enforceable subset.

### PR-1: Taxonomy Before Modeling

The investigation MUST begin with taxonomy development (Stage 1) before selecting specific modeling targets (Stage 2).

- **Rationale**: Without a framework for organizing the concept space, modeling choices are arbitrary. The taxonomy identifies what's shared vs. divergent, which directly determines the library/designs split and the reuse strategy.
- **What it produces**: A classification of the fusion concept space, informed by domain literature, that organizes ~36+ concepts along meaningful dimensions.
- **Enforcement**: No concept modeling work items should be created until a taxonomy artifact exists and has been reviewed.

### PR-2: Concept Analysis Identifies Shared vs. Divergent Structure

The taxonomy stage MUST include a concept analysis phase — identifying what cost structures, physics models, and engineering parameters are shared across concepts vs. where they fundamentally diverge.

- **Rationale**: This is the bridge between "we understand the landscape" and "we know how to model it." The concept analysis directly informs MR-3 (what goes in library vs. designs) and MR-6 (what patterns are needed).
- **What it produces**: A structured comparison identifying shared elements (candidates for library definitions) and divergent elements (candidates for concept-specific designs).
- **Enforcement**: Concept analysis must be a committed artifact, not just chat analysis. It must be referenced when creating modeling patterns (PR-3).

### PR-3: Documented Patterns Before Production Models

Based on the concept analysis, the process MUST produce documented modeling patterns BEFORE production modeling begins.

- **Rationale**: Patterns encode the shared structure identified in concept analysis into reusable, validated templates. Building production models without validated patterns risks inconsistency and rework.
- **What it produces**: Pattern documents with worked examples, validation results, and guidance on where concept-specific specialization occurs. The traceability citation format (MR-4) is an example of this: a documented pattern with defined format, usage examples, and enforcement tooling.
- **Enforcement**: Aligns with MR-6. Production models should reference their governing pattern document.

### PR-4: Iterative Process with Feedback Loops

The process SHOULD accommodate iteration — both within each stage's internal cycle and between stages.

- **Rationale**: Research reveals taxonomy gaps. Concept analysis reveals literature gaps. Modeling reveals pattern gaps. A rigid linear process breaks when reality doesn't match the plan.
- **What it enables**: The cycle structure described in OVERVIEW.md — Information Gathering → Work → Analysis, with feedback loops from Work and Analysis back to Information Gathering.
- **Enforcement**: Not directly enforceable as a rule. This is a process principle. Enforcement is cultural: when a gap is identified, the response is to loop back (ingest more sources, revise taxonomy, update patterns) rather than paper over it.

### PR-5: Committed Artifacts at Every Phase

Each phase of the process MUST produce committed artifacts. Knowledge transforms are visible — a reader can see what went in and what came out at every step.

- **Rationale**: Chat analysis evaporates between sessions. Committed artifacts survive. The traceability chain (PDFs → extractions → domain insights → taxonomy → concept analysis → patterns → models → results) only works if every link is a real, committed file.
- **What it produces**: The artifact chain described in OVERVIEW.md's Investigation Process.
- **Verification**: The traceability audit script (MR-4) provides partial verification — it checks that citation chains between committed artifacts resolve correctly. Full coverage requires review, since not all artifacts are citation-linked (e.g., taxonomy → concept analysis is a logical dependency, not necessarily a file citation).
- **Artifact types per phase**:
  - Source ingestion: extracted documents in `knowledge/sources/`, registered in SOURCE_INDEX.md
  - Domain research: DI-XXX entries in KNOWLEDGE.md, research docs in `knowledge/research/`
  - Taxonomy: classification artifact (format TBD) committed to repo
  - Concept analysis: comparison artifact committed to repo
  - Modeling patterns: pattern documents committed to repo
  - Model construction: SysML files in `models/`, passing validation, with citations per MR-4
  - Analysis: output data in `data/`, visualizations committed

---

**Last Updated**: 2026-03-02
