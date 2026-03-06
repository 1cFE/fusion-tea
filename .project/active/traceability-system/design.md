# Design: Traceability Citation System

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-03-02 10:15 PST
**Commit:** 72099ea
**Branch:** init-demo

## Overview

A single Python script (`scripts/trace_audit.py`) that parses structured citations from SysML doc comments and markdown files, validates that cited files and anchors exist, walks transitive reference chains, and produces a traceability report.

## Related Artifacts

- **Spec:** `.project/active/traceability-system/spec.md`
- **Plan:** `.project/active/traceability-system/plan.md` (to be created)
- **REQUIREMENTS.md:** `modeling_project/REQUIREMENTS.md` — MR-4 enforcement to be updated

---

## Research Findings

### Existing SysML Doc Comment Patterns

The archived models already use structured citation fields in doc comments, with bold markdown syntax:

```sysml
doc /*
    Cost Account Structure (CAS) categories for fusion plant costing.

    **Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/categories/
    **Reference**: modeling_pm/research/20260123-pyfecons-library-mapping-strategy.md
    **Last Updated**: 2026-01-26
*/
```

Found in: `archive/models/library/foundation/costing.sysml:22-38`, `archive/models/tests/solar_battery/library.sysml:267-281`, `archive/models/tests/coffee_maker/library.sysml:2-8`.

The existing convention uses `**Source**:` (bold) rather than the spec's `Source:` (plain). Both are parseable — the regex can handle either.

### SysML AST Access (syside)

agentic-mbse's `SysideAdapter` (`~/1cfe/agentic-mbse/src/agentic_mbse/sysml/syside_adapter.py`) provides:
- `elements_of_type(model, "PartDefinition")` — iterate typed elements
- `load_model(paths)` — parse SysML files into an AST
- Doc comment text is available via `element.owned_elements` → `Documentation.body` (a plain string)

However, syside is a heavy dependency (slow to load, fails on files with syntax errors). For V1, **regex parsing on raw file text** is more appropriate — it's fast, has no external dependency, and works on files with syntax errors.

### Cost-Bearing Element Detection

The `Costed Component` pattern is well-defined in the archived models (`archive/models/library/foundation/costing.sysml:88-123`):
- `abstract part def 'Costed Component'` with `capital_cost`, `raw_material_cost`, `fabrication_cost`, `installation_cost`
- Leaf parts specialize with `:> 'Costed Component'` or `:> CostedComponent`
- Calc defs with cost outputs (e.g., `total_cost`, `material_cost`)

A regex heuristic can detect these without syside: look for `:> 'Costed Component'` or `:> CostedComponent` in part definitions.

### Existing Script Patterns (fusion-tea)

From `scripts/zotero_ingest.py` and `scripts/zotero_lib.py`:
- `argparse` for CLI, with mode-selection flags
- `pathlib.Path` throughout, never `os.path`
- Module-level `Path` constants for directory locations
- `print()` for user output (2-space indent for detail lines)
- Stats dict accumulation → summary print
- `NamedTuple` for structured data containers
- Type hints on public function signatures

### Test Patterns

- `tests/conftest.py` provides pytest fixtures
- Test files in `tests/` use standard pytest conventions
- Standalone test scripts also exist in `scripts/`

---

## Design Decision: Markdown Citation Syntax

The spec proposes `> [Source]: path` inside blockquotes. This has a **rendering problem**: `[Source]: path` is valid markdown link reference definition syntax. Some renderers will interpret it as an invisible link definition rather than visible text — the citation would silently disappear in rendered output.

**Proposed change**: Use the same plain-text field names in blockquotes, without brackets:

```markdown
> Source: knowledge/sources/hsu_et_al/output.md
> Ref: L145-162
> Basis: CAS22.01 magnet system cost scaled from Table 3
```

This:
- Renders visibly in all markdown renderers (it's just a blockquote with text)
- Uses the exact same field names and format as SysML doc comments
- Is parseable with the same regex patterns
- Has no collision with any standard markdown syntax
- Visually distinct from prose (the `Source:` / `Ref:` / `Basis:` prefix pattern)

The parser recognizes a citation block as: a blockquote line starting with `Source:` (the required field), optionally followed by `Ref:` and `Basis:` lines in the same blockquote. This is distinctive enough to avoid false positives — normal prose blockquotes rarely start with `Source:`.

---

## Proposed Design

### Architecture

```
scripts/trace_audit.py  (~350-450 lines, single file)
│
├─ Data Model           Citation, ValidationResult, ChainNode, AuditReport
├─ Parsers              parse_sysml_file(), parse_markdown_file()
├─ Validators           validate_citation(), resolve_anchor()
├─ Chain Walker          walk_chains()
├─ Coverage Checker     find_uncited_cost_elements()
├─ Reporter             print_summary(), write_json_report()
└─ CLI                  main(), parse_args()
```

Single file, no companion library. All parsing is regex-based — no syside or markdown-parsing library dependency. The only imports are stdlib (`argparse`, `pathlib`, `re`, `json`, `dataclasses`, `sys`).

### Data Model

```python
@dataclass
class Citation:
    """A single citation extracted from a file."""
    source: str          # File path (repo-relative or absolute)
    ref: str | None      # Anchor: "L42-58" or "## Section Name"
    basis: str | None    # Human explanation
    origin_file: Path    # File containing this citation
    origin_line: int     # Line number of the Source: field

@dataclass
class ValidationResult:
    """Result of validating a single citation."""
    citation: Citation
    source_exists: bool
    source_resolved: Path | None   # Resolved absolute path (or None)
    anchor_valid: bool | None      # None if no Ref field
    anchor_error: str | None       # Reason anchor failed
    external: bool                 # True if absolute path outside repo

@dataclass
class ChainNode:
    """One node in a transitive citation chain."""
    file: Path
    citations: list[Citation]      # Citations found in this file
    children: list['ChainNode']    # Next hops (one per citation)
    is_terminus: bool              # No outgoing citations
    is_cycle: bool                 # Back-reference detected
    is_broken: bool                # Source didn't resolve
    error: str | None

@dataclass
class UncitedElement:
    """A cost-bearing SysML element with no citation in its doc comment."""
    file: Path
    line: int
    element_name: str

@dataclass
class AuditReport:
    """Complete audit results."""
    files_scanned: int
    citations_found: int
    validations: list[ValidationResult]  # One per citation — replaces separate counts/errors
    chains: list[ChainNode]              # Root nodes of all chains
    uncited_elements: list[UncitedElement]
```

### Component 1: Parsers

Two parser functions, same output type (`list[Citation]`), same field-extraction regex.

**Shared citation field regex** (used by both parsers):

```python
# Matches Source:/Ref:/Basis: with optional ** bold markers
RE_SOURCE = re.compile(r'^\s*\*{0,2}Source\*{0,2}:\s*(.+)$', re.MULTILINE)
RE_REF = re.compile(r'^\s*\*{0,2}Ref(?:erence)?\*{0,2}:\s*(.+)$', re.MULTILINE)
RE_BASIS = re.compile(r'^\s*\*{0,2}Basis\*{0,2}:\s*(.+)$', re.MULTILINE)
```

Note: `Ref` and `Reference` are both accepted. The existing archived models use `Reference`; the spec defines `Ref`. Accepting both costs nothing and avoids needless enforcement of one spelling.

#### `parse_sysml_file(file_path: Path) -> list[Citation]`

1. Read file text
2. Find all `doc /* ... */` blocks via regex: `doc\s*/\*(.*?)\*/` (dotall)
3. Track line offsets so each doc block maps to its line number in the file
4. Within each doc block, split on blank lines to find citation groups (a group starts with a `Source:` line)
5. Extract `Source`, `Ref`, `Basis` fields from each group
6. Return list of `Citation` objects

**Doc block regex**: The SysML `doc` keyword is followed by `/*` ... `*/`. This is distinct from regular `/* ... */` comments (which lack the `doc` prefix). We parse only `doc` comments, not bare comments.

```python
RE_DOC_BLOCK = re.compile(r'doc\s*/\*(.*?)\*/', re.DOTALL)
```

#### `parse_markdown_file(file_path: Path) -> list[Citation]`

1. Read file text, split into lines
2. Identify blockquote citation blocks: consecutive `>` lines where the first `>` line contains `Source:`
3. A citation block ends at a non-blockquote line or a blank line within the blockquote followed by a new `Source:` line (which starts a new citation)
4. Extract `Source`, `Ref`, `Basis` from the blockquote lines (strip leading `> `)
5. Return list of `Citation` objects

**Recognition heuristic**: A blockquote line is a citation start if it matches `^>\s*\*{0,2}Source\*{0,2}:\s*`. This is distinctive enough — normal prose blockquotes very rarely start with `Source:`.

### Component 2: Validators

#### `resolve_source_path(source: str, repo_root: Path) -> tuple[Path | None, bool]`

Returns `(resolved_path, is_external)`.

- If `source` starts with `/`: treat as absolute path. `is_external = True`. Return path if exists, else `None`.
- Otherwise: join with `repo_root`. `is_external = False`. Return path if exists, else `None`.

#### `resolve_anchor(ref: str, file_path: Path) -> tuple[bool, str | None]`

Returns `(valid, error_message)`.

- If `ref` is None: return `(True, None)` — no anchor to validate.
- If `ref` matches `L(\d+)(?:-(\d+))?`:
  - Read file, count lines
  - Check start line ≤ line count (and end line ≤ line count if range)
  - Return `(False, "File has N lines, citation references line M")` on failure
- If `ref` starts with `#`:
  - Read file text
  - Search for a markdown heading matching the text after `#`s (case-insensitive, whitespace-normalized)
  - Return `(False, "Heading 'X' not found in file")` on failure
- Otherwise: return `(False, "Unrecognized anchor format: ...")`.

**Section heading matching**: The `Ref` field may include the `#` prefix (`## Section Name`) or just the heading text. The matcher normalizes both: strips `#` prefix and whitespace, compares case-insensitively against headings found in the file (which are lines matching `^#{1,6}\s+(.+)$`).

### Component 3: Chain Walker

#### `walk_chains(root_citations: list[Citation], repo_root: Path) -> list[ChainNode]`

Builds the citation graph starting from each citation found in the scanned files.

```
Algorithm:
  parse_cache: dict[Path, list[Citation]] = {}  # memoize per-file parsing

  function build_node(file_path, visited_set):
      if file_path in visited_set:
          return ChainNode(file=file_path, is_cycle=True)

      visited_set.add(file_path)

      citations = get_or_parse(file_path, parse_cache)
      children = []
      for citation in citations:
          resolved = resolve_source_path(citation.source, repo_root)
          if resolved is None:
              children.append(ChainNode(file=citation.source, is_broken=True))
          elif is_parseable(resolved):  # .sysml or .md
              children.append(build_node(resolved, visited_set.copy()))
          else:
              children.append(ChainNode(file=resolved, is_terminus=True))

      visited_set.discard(file_path)  # allow same file in different branches
      return ChainNode(file=file_path, citations=citations, children=children)
```

Key behaviors:
- **Per-branch visited set**: `visited_set.copy()` at each branch. The same file can appear in different chains (A→C and B→C are both valid), but not within a single chain (A→B→A is a cycle).
- **Parse caching**: Each file is parsed at most once, results cached in `parse_cache`.
- **Parseable files**: `.sysml` and `.md` files are parsed for further citations. All other file types (`.py`, `.csv`, etc.) are treated as termini.
- **External files**: Absolute paths are validated for existence but treated as termini (not followed further, since they're outside the repo).

### Component 4: Coverage Checker

#### `find_uncited_cost_elements(sysml_files: list[Path]) -> list[dict]`

Regex heuristic to find SysML elements that appear to be cost-bearing but have no citation in their doc comment.

**Approach**: Scan each `.sysml` file for part definitions that specialize `Costed Component` (via `:> 'Costed Component'` or `:> CostedComponent`). For each match, look backward in the file for the nearest `doc /*` block. If no doc block or the doc block has no `Source:` field, flag it.

Also scan for `calc def` elements with cost-related outputs (`capital_cost`, `total_cost`, `material_cost`, `lcoe`). Same backward-search for doc comment with citation.

This is a heuristic — it may miss some patterns or flag false positives. That's acceptable for V1. The output is informational (warnings), not hard failures. The exit code check (FR-11) only fails on broken citations, not missing coverage.

**Decision**: Uncited elements produce warnings, not errors. This keeps the exit code useful for CI (broken links = real problems, missing coverage = aspirational). Coverage enforcement can be tightened later.

### Component 5: Reporter

#### `print_summary(report: AuditReport) -> None`

Counts are derived from `report.validations`:
- **Valid**: `source_exists and (anchor_valid is not False)`
- **Broken**: `not source_exists or anchor_valid is False`
- **Unverifiable**: `external and not source_exists`

Human-readable stdout output:

```
Traceability Audit
==================

Scanned: 12 files (5 .sysml, 7 .md)
Citations found: 23
  Valid: 20
  Broken: 2
  Unverifiable (external): 1

Broken Citations:
  models/library/definitions/magnets.sysml:45
    Source: knowledge/sources/nonexistent/output.md
    Error: File not found

  work/active/catf-model/design.md:78
    Source: knowledge/research/approved/magnet-analysis.md
    Ref: ## Cost Scaling
    Error: Heading 'Cost Scaling' not found in file

Coverage:
  Cost-bearing elements: 8
  With citations: 6
  Missing citations: 2
    models/library/definitions/blanket.sysml:30  part def 'Blanket' :> 'Costed Component'
    models/library/definitions/shield.sysml:15   part def 'Shield' :> 'Costed Component'

Result: FAIL (2 broken citations)
```

#### `write_json_report(report: AuditReport, output_path: Path) -> None`

Structured JSON for downstream tooling. Contains full chain trees, all validation results, all uncited elements. Written to a configurable path (default: `data/trace_audit_report.json`).

### Component 6: CLI

```python
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit traceability citations across SysML and markdown files."
    )
    parser.add_argument(
        "paths", nargs="*", default=None,
        help="Specific files or directories to scan (default: models/ knowledge/research/ work/)"
    )
    parser.add_argument(
        "--json", default="data/trace_audit_report.json",
        help="Path for JSON report output"
    )
    parser.add_argument(
        "--no-chains", action="store_true",
        help="Skip transitive chain walking (faster, validate citations only)"
    )
    parser.add_argument(
        "--no-coverage", action="store_true",
        help="Skip uncited element detection"
    )
    return parser.parse_args()
```

Default scan paths (when no positional args):

```python
DEFAULT_SCAN_PATHS = [
    Path("models"),
    Path("knowledge/research"),
    Path("work"),
]
```

File collection: recursively glob `**/*.sysml` and `**/*.md` within each scan path.

### Usage

```bash
# Full audit (default scope)
uv run python scripts/trace_audit.py

# Audit specific files
uv run python scripts/trace_audit.py models/library/definitions/magnets.sysml

# Audit specific directory
uv run python scripts/trace_audit.py work/active/catf-model/

# Fast mode: validate citations only, no chain walking
uv run python scripts/trace_audit.py --no-chains

# Custom JSON output path
uv run python scripts/trace_audit.py --json /tmp/trace_report.json
```

---

## Potential Risks

1. **Regex false positives in markdown**: A blockquote starting with `Source:` that isn't a citation. Mitigation: unlikely in practice; if it becomes an issue, require `Source:` + `Ref:` together as a citation signal.

2. **Cost element heuristic misses**: The regex for detecting cost-bearing elements may miss unconventional patterns. Mitigation: the coverage check is informational (warnings), not blocking. Can be refined as real models are built.

3. **Large file performance**: Chain walking on a large repo could be slow if many files are parsed. Mitigation: parse cache ensures each file is read at most once. For V1 scope (dozens of files, not thousands), performance is not a concern.

4. **Line number drift**: Citations using `L42-58` will break when the cited file is edited. Mitigation: the audit script will catch these (that's the point). Section heading anchors are recommended for mutable files. This is a feature, not a bug — stale line numbers should be caught and updated.

## Integration Strategy

- **MR-4 enforcement**: After implementation, update `modeling_project/REQUIREMENTS.md` MR-4 enforcement method to: "Run `uv run python scripts/trace_audit.py` — all citations must resolve, exit code 0."
- **CI/pre-commit**: The script's exit code enables future integration as a pre-commit hook or CI check. Not wired up in V1, but the interface is ready.
- **Modeling workflow**: When building models (future work items), the citation format is the contract. LLM agents producing SysML will include `Source:` / `Ref:` / `Basis:` in doc comments. The audit script validates their output.

## Validation Approach

### Test Fixtures

Create `tests/fixtures/trace/` with small test files:

1. **`valid_chain/`** — 3-file chain: `test.sysml` → `analysis.md` → `source.md`. All citations valid. Verifies: parsing, chain walking, terminus detection.
2. **`broken_link/`** — `test.sysml` cites a non-existent file. Verifies: broken link detection and error reporting.
3. **`section_anchor/`** — `test.md` cites another `.md` with a `## Section` anchor. Verifies: heading anchor resolution.
4. **`line_anchor/`** — `test.sysml` cites a file with `L10-20` anchor. Verifies: line number anchor resolution.
5. **`cycle/`** — `a.md` → `b.md` → `a.md`. Verifies: cycle detection.
6. **`multi_citation/`** — `test.sysml` with two citation blocks in one doc comment. Verifies: multi-citation parsing.

### Test File

`tests/test_trace_audit.py` — pytest tests using the fixtures:
- Test each parser independently (SysML, markdown)
- Test anchor resolution (line numbers, section headings, invalid)
- Test chain walking (valid chain, broken chain, cycle)
- Test the full audit pipeline on each fixture directory
- Test exit code behavior

---

**Next Step:** After approval → `/_my_plan` for implementation phasing
