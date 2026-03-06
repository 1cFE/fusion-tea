# Spec: Traceability Citation System

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-03-02 09:55 PST
**Complexity:** MEDIUM
**Branch:** init-demo

---

## Business Goals

### Why This Matters

The credibility of cross-concept fusion techno-economic comparison depends entirely on whether a reader can verify any number they encounter. LLM agents perform significant portions of the research and modeling, making hallucination a real risk. The current traceability approach — agentic-mbse Level 5 checks only that a doc comment *exists* — provides no actual verification.

This system defines a parseable citation format, enforces it across artifact types, and provides a script that can walk transitive reference chains to produce a deterministic traceability report. It replaces aspirational traceability requirements with scriptable enforcement.

### Success Criteria

- [ ] A single script invocation produces a report showing which parameters are fully traced, which have broken chains, and which are missing citations entirely
- [ ] The citation format is simple enough that an LLM agent can produce correct citations without special tooling
- [ ] Transitive chains resolve correctly: SysML comment → synthesis doc → research report → source extraction
- [ ] MR-4 in REQUIREMENTS.md can reference this system's checks as its enforcement mechanism
- [ ] No human judgment required for the structural traceability check (content quality is separate)

### Priority

Foundational infrastructure. Defines the citation format that all downstream modeling work must follow. Must be specified before production models are built (aligns with MR-6 "patterns before production" and PR-3 "documented patterns before production models").

---

## Problem Statement

### Current State

1. **agentic-mbse Level 5 validation** checks only that doc comments exist — not their content. A comment saying "TODO: add source" passes.
2. **MR-4** (cost parameter source citation) says "validation should check that cost parameters have source metadata" but no such validation exists.
3. **The traceability requirement in OVERVIEW.md** says "a reader can trace any number back to its origin" but punts on mechanism.
4. **The old traceability_matrix.csv** approach required manual population via `pm trace-element` CLI calls and was never connected to validation. It's now archived.
5. **No consistent citation format** exists across artifact types. SysML comments, research docs, and work items each use ad-hoc references.

### Desired Outcome

A unified citation format used across all artifact types (SysML, markdown in `knowledge/research/`, markdown in `work/`), enforced by a script that can:
- Parse citations from any supported file type
- Follow transitive reference chains across files
- Report completeness, broken links, and missing citations
- Run in CI or as a pre-commit check

---

## Scope

### In Scope

- **Citation format definition** — a parseable pattern for embedding source references in SysML doc comments and markdown files
- **Supported artifact types (V1)**:
  - SysML doc comments (`models/**/*.sysml`)
  - Markdown in `knowledge/research/` (research reports, synthesis docs)
  - Markdown in `work/` (modeling specs, designs, plans — modeling decisions need citations too)
- **Anchor types** — citations MAY use file path + line numbers OR file path + section heading anchors
- **Chain terminus** — any committed file in the repo (or an absolute path to a known external codebase like PyFECONS) is a valid chain endpoint
- **Audit script** (`scripts/trace_audit.py`) — parses, walks chains, reports
- **Report output** — human-readable summary + structured data (JSON or similar) for downstream tooling

### Out of Scope

- Modifications to agentic-mbse (Level 5 or otherwise) — downstream abstraction after this stabilizes
- Automated citation population — this defines and checks the format, doesn't fill it in
- Content quality assessment — the script checks structural traceability (does the citation resolve?), not whether the cited value is correct
- Confidence scoring or quality grading — may be added later as an optional field
- Traceability matrix CSV generation — the audit report may inform one later, but generating a specific CSV schema is not a goal
- Citations in KNOWLEDGE.md DI-XXX entries or REQUIREMENTS.md — not V1; can be added later if useful

### Edge Cases & Considerations

- **Line number drift**: Markdown synthesis docs will be edited; line numbers become stale. Section heading anchors are the preferred citation target for mutable files. Line numbers are appropriate for stable files (source extractions, PyFECONS code).
- **Extracted source structure**: Source extractions live in `knowledge/sources/{slug}/output.md`. These are stable (re-extraction replaces the whole file). Line number citations into these are reliable.
- **External codebases**: PyFECONS at `/home/reid/PyFECONS` is a valid citation target. The audit script SHOULD verify the path exists but SHOULD NOT fail if the external codebase is unavailable (report as "unverifiable — external").
- **Empty chains**: A file with no outgoing citations is a valid chain terminus. The script should not flag terminal nodes as errors.
- **Circular references**: A cites B which cites A. The script MUST detect and report cycles rather than looping.

---

## Requirements

### Citation Format

#### FR-1: Parseable Citation Pattern

All citations MUST use a structured, regex-parseable pattern. The pattern MUST be consistent across SysML doc comments and markdown files, differing only in the comment delimiters of the host format.

The citation pattern MUST include:

| Field | Required | Description |
|-------|----------|-------------|
| `Source` | MUST | Repo-relative file path (or absolute path for external codebases) to the cited artifact |
| `Ref` | SHOULD | Location within the source file — line number(s) or section heading anchor |
| `Basis` | SHOULD | Brief description of what was derived and how (e.g., "CAS22 cost breakdown for compact tokamak", "Scaled from ITER using R^2.5") |

**Rationale for keeping it minimal**: Three fields. `Source` is the machine-checkable link. `Ref` narrows to the specific location. `Basis` is the human-readable explanation. Additional fields (confidence, assumptions, last-verified) MAY be added as the system matures but are not V1 requirements.

#### FR-2: Direct File Reference Required

The `Source` field MUST be a direct file path — either:
- **Repo-relative**: `knowledge/sources/hsu_et_al/output.md`, `knowledge/research/approved/some-analysis.md`, `work/active/feature/design.md`
- **Absolute (external)**: `/home/reid/PyFECONS/pyfecons/costing/calculations/PowerBalance.py`

The `Source` field MUST NOT be an abstract identifier (e.g., "Hsu et al. 2020", "DI-005", "PyFECONS"). It MUST be a path that the audit script can resolve to an actual file.

**Rationale**: Abstract identifiers require a lookup table to resolve. File paths are self-resolving. This is what makes the audit script simple and deterministic.

#### FR-3: Anchor Types for Ref Field

The `Ref` field MUST support two anchor types:

1. **Line numbers**: `L42` (single line), `L42-58` (range). Appropriate for stable files (source extractions, external code).
2. **Section headings**: `## Section Name` or `### Subsection Name`. Appropriate for mutable markdown files where line numbers would drift.

The audit script MUST validate both anchor types:
- Line references: the file has at least that many lines
- Section references: the heading text exists in the file

#### FR-4: SysML Doc Comment Format

In SysML doc comments, citations MUST appear as structured fields within the comment body:

```sysml
part def SomeComponent :> CostedComponent {
    doc /*
        Description of what this component represents.

        Source: knowledge/sources/hsu_et_al/output.md
        Ref: L145-162
        Basis: CAS22.01 magnet system cost from Table 3
    */

    attribute capital_cost : CostValue;
}
```

Multiple citations in a single doc comment MUST be separated by a blank line between citation blocks:

```sysml
doc /*
    Hybrid costing approach combining two sources.

    Source: knowledge/sources/hsu_et_al/output.md
    Ref: L145-162
    Basis: Base cost scaling from Table 3

    Source: knowledge/research/approved/magnet-cost-analysis.md
    Ref: ## Scaling Assumptions
    Basis: Adjusted scaling exponent for high-field magnets
*/
```

#### FR-5: Markdown Citation Format

In markdown files, citations MUST use the same field names within a fenced block or structured pattern that is visually distinct from prose and machine-parseable.

The specific delimiter for markdown citations SHALL be a blockquote with plain-text field names (no brackets):

```markdown
The capital cost for the magnet system is estimated at $450M based on
scaling from ITER experience.

> Source: knowledge/sources/hsu_et_al/output.md
> Ref: L145-162
> Basis: CAS22.01 magnet system cost scaled from Table 3

This estimate assumes high-temperature superconducting magnets...
```

**Rationale for plain blockquote fields**: Renders visibly in all markdown viewers. Visually distinct from prose. Uses the exact same field names and format as SysML doc comments (FR-4), so one regex pattern works for both. The `[Source]:` syntax was rejected because it collides with markdown's link reference definition syntax (`[label]: url`), which causes some renderers to silently hide the citation.

Multiple citations follow the same blank-line separation as SysML:

```markdown
> Source: knowledge/sources/hsu_et_al/output.md
> Ref: L145-162
> Basis: Base cost from Table 3

> Source: /home/reid/PyFECONS/pyfecons/costing/calculations/CAS220101.py
> Ref: L34-50
> Basis: Scaling law implementation
```

### Chain Walking

#### FR-6: Transitive Chain Resolution

The audit script MUST follow citation chains transitively. If file A cites file B, and file B cites file C, the script MUST report the full chain A → B → C.

Each link in the chain is validated independently:
- A's citation of B: does B exist? Does the anchor resolve?
- B's citation of C: does C exist? Does the anchor resolve?

A broken link at any point in the chain MUST be reported, with the full chain-so-far shown for context.

#### FR-7: Chain Terminus

Any committed file in the repo — or a valid absolute path to an external codebase — is a valid chain terminus. A file with no outgoing citations is not an error; it is the end of the chain.

The audit script MUST NOT require that chains reach a specific "root" file type (e.g., source extractions). A chain may legitimately terminate at:
- A source extraction (`knowledge/sources/*/output.md`)
- An external codebase file (`/home/reid/PyFECONS/...`)
- A hand-written assumptions document with no further citations
- Any other committed file

#### FR-8: Cycle Detection

The audit script MUST detect circular references (A → B → A, or longer cycles) and report them as errors rather than looping infinitely.

### Audit Script

#### FR-9: Scan and Report

The audit script (`scripts/trace_audit.py`) MUST:

1. **Scan** all files in the configured scope (V1: `models/**/*.sysml`, `knowledge/research/**/*.md`, `work/**/*.md`)
2. **Extract** all citations from scanned files
3. **Validate** each citation:
   - Source file exists (or is reported as external/unverifiable)
   - Ref anchor resolves (line count or heading match)
4. **Walk chains** from each citation origin to chain terminus
5. **Report** results in both:
   - Human-readable summary to stdout
   - Structured output (JSON) to a file

#### FR-10: Report Content

The audit report MUST include:

- **Coverage summary**: files scanned, citations found, chains complete, chains broken
- **Broken links**: each broken citation with file, line, the Source value that failed to resolve, and reason (file not found, anchor not found, cycle detected)
- **Complete chains**: each fully-resolved chain from origin to terminus (in the structured output; summary can abbreviate)
- **Uncited elements**: [INFERRED] SysML elements that have cost attributes but no citations in their doc comments. This is the "coverage gap" check — the equivalent of what Level 5 should do but doesn't.

#### FR-11: Exit Code

The audit script MUST exit with:
- `0` if all citations resolve (source files exist, anchors valid)
- Non-zero if any broken links are found (source file missing or anchor not resolved)

Uncited cost-bearing elements (detected by the coverage checker) produce **warnings** in the report but do NOT affect the exit code. Rationale: coverage detection is heuristic-based and the repo will have incomplete coverage during development. Broken links are deterministic errors that indicate real problems. Coverage enforcement can be tightened in a future version.

This enables use in CI or pre-commit hooks.

#### FR-12: Configurable Scope

The audit script SHOULD accept command-line arguments to override the default scan paths. This allows running the check on a subset of files during development.

---

## Acceptance Criteria

### Core Functionality

- [ ] Citation format is defined and documented (this spec, plus a short reference in REQUIREMENTS.md or a pattern doc)
- [ ] `scripts/trace_audit.py` exists and runs via `uv run python scripts/trace_audit.py`
- [ ] Script correctly parses citations from SysML doc comments
- [ ] Script correctly parses citations from markdown blockquote citations
- [ ] Script resolves repo-relative file paths
- [ ] Script resolves absolute paths (external codebases) — reports "unverifiable" if path doesn't exist
- [ ] Script validates line number anchors (file has enough lines)
- [ ] Script validates section heading anchors (heading exists in file)
- [ ] Script follows transitive chains and reports full paths
- [ ] Script detects and reports circular references
- [ ] Script identifies SysML cost-bearing elements missing citations
- [ ] Script produces human-readable stdout summary
- [ ] Script produces structured JSON output
- [ ] Script returns appropriate exit code

### Integration

- [ ] MR-4 enforcement method in REQUIREMENTS.md is updated to reference this script
- [ ] Running the script on the current (empty) repo produces a clean report (no false positives)
- [ ] Script works with `uv run python scripts/trace_audit.py` (no additional dependencies beyond what's in pyproject.toml, or additions are documented)

### Validation with Test Fixtures

- [ ] At least one test fixture: a small SysML file with citations pointing to a small markdown file that itself cites another file — verifying 3-node chain walking works
- [ ] At least one test fixture: a broken citation (file doesn't exist) — verifying error reporting
- [ ] At least one test fixture: a section heading anchor that resolves correctly
- [ ] At least one test fixture: a circular reference — verifying cycle detection

---

## Related Artifacts

- **Plan:** `.project/active/traceability-system/plan.md` (to be created)
- **REQUIREMENTS.md:** `modeling_project/REQUIREMENTS.md` — MR-4 enforcement to be updated after implementation
- **OVERVIEW.md:** `modeling_project/OVERVIEW.md` — Traceability Requirements section defines the *what*; this spec defines the *how*
- **Archived traceability approach:** `archive/data/traceability_matrix.csv`, `archive/modeling_project/VALIDATION_MATRIX.md`

---

**Next Steps:** After approval, proceed to `/_my_design` or directly to `/_my_plan` (implementation is straightforward enough that design may be optional — user's call).
