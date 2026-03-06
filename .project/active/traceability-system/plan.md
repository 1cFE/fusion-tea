# Implementation Plan: Traceability Citation System

**Status:** Draft
**Created:** 2026-03-02
**Last Updated:** 2026-03-02

## Source Documents
- **Spec:** `.project/active/traceability-system/spec.md`
- **Design:** `.project/active/traceability-system/design.md` — See here for component details, data model, regex patterns, algorithm pseudocode

## Implementation Strategy

**Phasing Rationale:**
Parsers are the foundation — if citations don't parse correctly, nothing downstream works. Validators build on parsed citations. Chain walking builds on both. Reporter/CLI is the output layer with the least risk. Integration is last because it touches project docs and requires a working script.

Each phase writes test fixtures and tests first, then implementation. All 6 fixture directories are created in Phase 1 since they're small and needed across phases.

**Overall Validation Approach:**
- Each phase starts with tests (pytest)
- Run: `uv run python -m pytest tests/test_trace_audit.py -v`
- Final validation: `uv run python scripts/trace_audit.py` on real repo

---

## Phase 1: Data Model + Test Fixtures + Parsers

### Goal
Establish the dataclasses, all test fixtures, and both parsers (SysML + markdown). This is first because every later phase depends on parsed `Citation` objects.

### Test Stencil (Write This First)
```python
class TestSysmlParser:
    def test_single_citation(self, fixtures_dir):
        citations = parse_sysml_file(fixtures_dir / "valid_chain" / "test.sysml")
        assert len(citations) == 1
        assert citations[0].source == "analysis.md"  # relative within fixture
        assert citations[0].ref is not None

    def test_multi_citation(self, fixtures_dir):
        citations = parse_sysml_file(fixtures_dir / "multi_citation" / "test.sysml")
        assert len(citations) == 2

    def test_bold_syntax(self, fixtures_dir):
        # **Source**: style from archived models
        citations = parse_sysml_file(fixtures_dir / "valid_chain" / "test.sysml")
        assert len(citations) >= 1

class TestMarkdownParser:
    def test_blockquote_citation(self, fixtures_dir):
        citations = parse_markdown_file(fixtures_dir / "section_anchor" / "test.md")
        assert len(citations) == 1
        assert citations[0].source is not None

    def test_no_false_positives(self, fixtures_dir):
        # A markdown file with regular blockquotes but no citations
        citations = parse_markdown_file(fixtures_dir / "valid_chain" / "source.md")
        # source.md is a terminus — no outgoing citations
        assert len(citations) == 0
```

### Changes Required

**See `design.md` for:**
- Data model (5 dataclasses) → `design.md#data-model`
- Shared regex patterns → `design.md#component-1-parsers`
- SysML parser algorithm → `design.md#parse_sysml_filepath-path---listcitation`
- Markdown parser algorithm → `design.md#parse_markdown_filepath-path---listcitation`

**Specific file changes:**

#### 1. Test Fixtures
**Directory:** `tests/fixtures/trace/` (NEW — all 6 fixture sets)

- [ ] `valid_chain/test.sysml` — part def with doc comment citing `analysis.md`
- [ ] `valid_chain/analysis.md` — markdown with blockquote citation to `source.md`
- [ ] `valid_chain/source.md` — terminal file (no citations, just content)
- [ ] `broken_link/test.sysml` — doc comment citing `nonexistent/file.md`
- [ ] `section_anchor/test.md` — blockquote citation with `Ref: ## Cost Scaling`
- [ ] `section_anchor/target.md` — file with `## Cost Scaling` heading
- [ ] `line_anchor/test.sysml` — doc comment with `Ref: L10-20`
- [ ] `line_anchor/target.md` — file with at least 20 lines
- [ ] `cycle/a.md` — cites `b.md`
- [ ] `cycle/b.md` — cites `a.md`
- [ ] `multi_citation/test.sysml` — doc comment with two citation blocks (blank-line separated)
- [ ] `multi_citation/source_a.md` — cited by first block
- [ ] `multi_citation/source_b.md` — cited by second block

#### 2. Test File
**File:** `tests/test_trace_audit.py` (NEW — write first)
- [ ] Create file with `fixtures_dir` fixture pointing to `tests/fixtures/trace/`
- [ ] `TestSysmlParser` class — single citation, multi-citation, bold syntax
- [ ] `TestMarkdownParser` class — blockquote citation, no false positives on terminus files

#### 3. Implementation
**File:** `scripts/trace_audit.py` (NEW)
- [ ] Imports: `argparse`, `dataclasses`, `json`, `pathlib`, `re`, `sys`
- [ ] 5 dataclasses: `Citation`, `ValidationResult`, `ChainNode`, `UncitedElement`, `AuditReport`
- [ ] Shared regex constants: `RE_SOURCE`, `RE_REF`, `RE_BASIS`, `RE_DOC_BLOCK`
- [ ] `parse_sysml_file()` — doc block extraction, citation group splitting, field extraction
- [ ] `parse_markdown_file()` — blockquote detection, field extraction

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/test_trace_audit.py::TestSysmlParser -v` → All pass
- [ ] `uv run python -m pytest tests/test_trace_audit.py::TestMarkdownParser -v` → All pass

**Manual:**
- [ ] Inspect fixture files — confirm they look like realistic citations
- [ ] Verify `parse_sysml_file` returns correct `origin_line` values (not just that citations parse)

**What We Know Works After This Phase:**
Both parsers correctly extract citations from SysML doc comments and markdown blockquotes. Bold and plain syntax both work. Multi-citation blocks split correctly. No false positives on terminal files.

---

## Phase 2: Validators

### Goal
Source path resolution and anchor validation. Builds on parsed `Citation` objects from Phase 1.

### Test Stencil (Write This First)
```python
class TestResolveSourcePath:
    def test_relative_path_exists(self, fixtures_dir):
        path, external = resolve_source_path("analysis.md", fixtures_dir / "valid_chain")
        assert path is not None
        assert not external

    def test_relative_path_missing(self, fixtures_dir):
        path, external = resolve_source_path("nonexistent.md", fixtures_dir)
        assert path is None
        assert not external

    def test_absolute_path_external(self, tmp_path):
        target = tmp_path / "ext.py"
        target.write_text("x = 1")
        path, external = resolve_source_path(str(target), tmp_path)
        assert path is not None
        assert external

class TestResolveAnchor:
    def test_line_anchor_valid(self, fixtures_dir):
        valid, error = resolve_anchor("L10-20", fixtures_dir / "line_anchor" / "target.md")
        assert valid is True

    def test_line_anchor_out_of_range(self, fixtures_dir):
        valid, error = resolve_anchor("L999", fixtures_dir / "line_anchor" / "target.md")
        assert valid is False
        assert "lines" in error

    def test_section_anchor_valid(self, fixtures_dir):
        valid, error = resolve_anchor("## Cost Scaling", fixtures_dir / "section_anchor" / "target.md")
        assert valid is True

    def test_section_anchor_missing(self, fixtures_dir):
        valid, error = resolve_anchor("## Nonexistent", fixtures_dir / "section_anchor" / "target.md")
        assert valid is False
```

### Changes Required

**See `design.md` for:**
- `resolve_source_path()` signature and logic → `design.md#component-2-validators`
- `resolve_anchor()` signature and logic → `design.md#resolve_anchorref-str-file_path-path---tuplebool-str--none`
- Section heading matching rules → `design.md#component-2-validators` (bottom)

**Specific file changes:**

#### 1. Tests
**File:** `tests/test_trace_audit.py` (MODIFY)
- [ ] Add `TestResolveSourcePath` class — relative exists, relative missing, absolute external, absolute missing
- [ ] Add `TestResolveAnchor` class — line valid, line out of range, section valid, section missing, no ref (None), unrecognized format

#### 2. Implementation
**File:** `scripts/trace_audit.py` (MODIFY)
- [ ] `resolve_source_path(source, repo_root)` — absolute vs relative detection, existence check
- [ ] `resolve_anchor(ref, file_path)` — line number regex, section heading search, None passthrough
- [ ] `validate_citation(citation, repo_root)` — orchestrates the above, returns `ValidationResult`

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/test_trace_audit.py::TestResolveSourcePath -v` → All pass
- [ ] `uv run python -m pytest tests/test_trace_audit.py::TestResolveAnchor -v` → All pass
- [ ] Full suite still passes: `uv run python -m pytest tests/test_trace_audit.py -v`

**What We Know Works After This Phase:**
Source paths resolve correctly (repo-relative and absolute). Anchors validate for both line numbers and section headings. Missing files/anchors produce clear error messages.

---

## Phase 3: Chain Walker

### Goal
Transitive chain resolution with cycle detection and parse caching. The trickiest algorithm — depends on parsers + validators.

### Test Stencil (Write This First)
```python
class TestChainWalker:
    def test_valid_three_node_chain(self, fixtures_dir):
        root = fixtures_dir / "valid_chain"
        citations = parse_sysml_file(root / "test.sysml")
        chains = walk_chains(citations, root)
        assert len(chains) == 1
        assert not chains[0].is_broken
        # Chain: test.sysml -> analysis.md -> source.md (terminus)
        assert len(chains[0].children) >= 1

    def test_broken_chain(self, fixtures_dir):
        root = fixtures_dir / "broken_link"
        citations = parse_sysml_file(root / "test.sysml")
        chains = walk_chains(citations, root)
        assert any(c.is_broken for c in chains[0].children)

    def test_cycle_detection(self, fixtures_dir):
        root = fixtures_dir / "cycle"
        citations = parse_markdown_file(root / "a.md")
        chains = walk_chains(citations, root)
        # Should terminate, not loop. Cycle node flagged.
        assert any(node.is_cycle for node in _flatten_nodes(chains))
```

### Changes Required

**See `design.md` for:**
- `walk_chains()` algorithm pseudocode → `design.md#component-3-chain-walker`
- Per-branch visited set behavior → `design.md#component-3-chain-walker` (Key behaviors)
- Parse caching strategy → `design.md#component-3-chain-walker`

**Specific file changes:**

#### 1. Tests
**File:** `tests/test_trace_audit.py` (MODIFY)
- [ ] Add `TestChainWalker` class — valid 3-node chain, broken chain, cycle detection
- [ ] Add helper `_flatten_nodes(chains)` to recursively collect all ChainNodes for assertion

#### 2. Implementation
**File:** `scripts/trace_audit.py` (MODIFY)
- [ ] `walk_chains(root_citations, repo_root)` — entry point, builds nodes from each root citation
- [ ] `_build_node(file_path, repo_root, visited, parse_cache)` — recursive builder with cycle detection
- [ ] `_is_parseable(path)` — checks `.sysml` or `.md` suffix
- [ ] `_get_or_parse(file_path, parse_cache)` — memoized parsing dispatch (sysml vs md)

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/test_trace_audit.py::TestChainWalker -v` → All pass
- [ ] Full suite still passes

**Manual:**
- [ ] Verify cycle fixture doesn't hang (test completes in < 1s)

**What We Know Works After This Phase:**
Transitive chains resolve correctly through multiple file types. Cycles are detected and reported. Broken mid-chain links are flagged. Parse cache prevents redundant file reads.

---

## Phase 4: Coverage Checker + Reporter + CLI

### Goal
Wire everything together: cost element detection heuristic, human-readable + JSON output, argparse CLI, exit code logic.

### Test Stencil (Write This First)
```python
class TestCoverageChecker:
    def test_detects_uncited_costed_component(self, fixtures_dir):
        # Need a fixture with a CostedComponent that has no Source: in its doc
        elements = find_uncited_cost_elements([fixtures_dir / "valid_chain" / "test.sysml"])
        # valid_chain/test.sysml HAS a citation, so should not be flagged
        assert len(elements) == 0

class TestFullPipeline:
    def test_clean_run_exit_zero(self, fixtures_dir):
        result = subprocess.run(
            ["uv", "run", "python", "scripts/trace_audit.py", str(fixtures_dir / "valid_chain")],
            capture_output=True, text=True
        )
        assert result.returncode == 0

    def test_broken_link_exit_nonzero(self, fixtures_dir):
        result = subprocess.run(
            ["uv", "run", "python", "scripts/trace_audit.py", str(fixtures_dir / "broken_link")],
            capture_output=True, text=True
        )
        assert result.returncode != 0
        assert "Broken" in result.stdout

    def test_json_report_written(self, fixtures_dir, tmp_path):
        json_path = tmp_path / "report.json"
        subprocess.run(
            ["uv", "run", "python", "scripts/trace_audit.py",
             str(fixtures_dir / "valid_chain"), "--json", str(json_path)],
            capture_output=True
        )
        assert json_path.exists()
        data = json.loads(json_path.read_text())
        assert "citations_found" in data
```

### Changes Required

**See `design.md` for:**
- Coverage checker approach → `design.md#component-4-coverage-checker`
- Reporter output format → `design.md#component-5-reporter`
- CLI argparse structure → `design.md#component-6-cli`
- Count derivation from `validations` list → `design.md#print_summaryreport-auditreport---none`

**Specific file changes:**

#### 1. Tests
**File:** `tests/test_trace_audit.py` (MODIFY)
- [ ] Add `TestCoverageChecker` class — detects uncited elements, doesn't flag cited elements
- [ ] Add `TestFullPipeline` class — subprocess invocations testing exit code, stdout, JSON output
- [ ] Import `subprocess` and `json` at top

#### 2. Implementation
**File:** `scripts/trace_audit.py` (MODIFY)
- [ ] `find_uncited_cost_elements(sysml_files)` — regex heuristic for `:> 'Costed Component'` / `:> CostedComponent` + cost calc defs
- [ ] `print_summary(report)` — human-readable stdout per design format; derive counts from `report.validations`
- [ ] `write_json_report(report, output_path)` — JSON serialization (dataclass → dict)
- [ ] `collect_files(paths)` — glob `**/*.sysml` and `**/*.md` from scan paths
- [ ] `parse_args()` — argparse per design
- [ ] `main()` — orchestrate: collect → parse → validate → walk chains → coverage → report → exit code
- [ ] Module-level `DEFAULT_SCAN_PATHS` constant

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/test_trace_audit.py -v` → All pass (full suite)
- [ ] `uv run python scripts/trace_audit.py tests/fixtures/trace/valid_chain/` → Exit 0, clean output
- [ ] `uv run python scripts/trace_audit.py tests/fixtures/trace/broken_link/` → Exit 1, broken link reported

**Manual:**
- [ ] Review stdout format — matches design's sample output
- [ ] Review JSON report — contains all fields, chain trees serialize correctly

**What We Know Works After This Phase:**
Complete script works end-to-end. Exit codes are correct. JSON and stdout reports are produced. Coverage checker finds uncited elements as warnings.

---

## Phase 5: Integration

### Goal
Update MR-4 enforcement, verify clean run on the real (mostly empty) repo, confirm no false positives.

### Changes Required

#### 1. MR-4 Update
**File:** `modeling_project/REQUIREMENTS.md` (MODIFY)
- [ ] Update MR-4 enforcement method to reference `scripts/trace_audit.py`
- [ ] Wording per `design.md#integration-strategy`: "Run `uv run python scripts/trace_audit.py` — all citations must resolve, exit code 0."

#### 2. Real Repo Validation
- [ ] Run `uv run python scripts/trace_audit.py` (default scope) → Exit 0, no false positives
- [ ] Verify `data/trace_audit_report.json` is written and valid JSON
- [ ] Confirm empty-repo summary is clean: `Citations found: 0`, no broken links, no uncited warnings

### Validation

**Automated:**
- [ ] `uv run python scripts/trace_audit.py` → Exit 0
- [ ] Full test suite: `uv run python -m pytest tests/test_trace_audit.py -v` → All pass

**What We Know Works After This Phase:**
Script is integrated into the project's quality infrastructure. MR-4 has a concrete enforcement mechanism. The script runs clean on the current repo.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: Fixtures include both bold (`**Source**:`) and plain (`Source:`) syntax to validate regex flexibility
- **Phase 3**: Cycle fixture is a tight 2-node loop — tests must complete in < 1s to confirm no infinite recursion
- **Phase 5**: Empty repo is the degenerate case — 0 citations, 0 elements. Reporter must handle gracefully.

## Implementation Notes

_To be filled during implementation._

### Phase 1 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

### Phase 2 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

### Phase 3 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

### Phase 4 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

### Phase 5 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**
