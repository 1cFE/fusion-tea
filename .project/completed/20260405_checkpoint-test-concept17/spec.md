# Spec: Checkpoint Test — Concept 17 (Laser ICF Direct Drive)

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-03-29 14:11 PDT
**Complexity:** MEDIUM
**Branch:** design-space-explore

---

## Business Goals

### Why This Matters
Two pipeline features — source replacement (Item 1) and source addition (Item 3) — have been implemented but not fully end-to-end tested with real Claude calls and real extraction. This checkpoint validates both features against concept 17 (laser-icf-direct-drive), which has freshly replaced sources in iter-02.

### Success Criteria
- [x] `stage1-all` completes on concept 17 with replaced sources (no errors, analysis produced) — ran individual stages: gap-check, analyze (3-pass, PASS), model-setup (LCOE $101.6/MWh), review (has-actions)
- [x] `add-source` successfully extracts and places the Xcimer whitepaper — 1,092 lines, 89KB, companion dir + symlink correct
- [x] `update-analysis` incorporates the new source and the analysis visibly changes — 3 findings applied to `analysis.md` (58KB, 39 whitepaper-term mentions)
- [x] Spot checks confirm specific Xcimer whitepaper content appears in the updated analysis — 6/8 PASS, 1 PARTIAL, 1 FAIL (≥5 required)

### Priority
High — validation debt on freshly completed Items 1 and 3.

---

## Problem Statement

### Current State
- Concept 17 has replaced sources in `iter-02/sources/` (3 sources: focused-energy-callahan-interview, hylife-energy-conversion-notes, xcimer-science-page)
- The `add-source` and `update-analysis` commands were implemented and code-reviewed but the manual test items in the plan (Phase 2 lines 155-161, Phase 3 lines 231-239) were deferred
- No end-to-end validation that replaced sources produce a clean analysis, or that the source addition pipeline works with real extraction

### Desired Outcome
Confidence that both pipelines work end-to-end with real data, and a documented record of what changed.

---

## Scope

### In Scope
1. Run `stage1-all` on concept 17 with its current (replaced) sources
2. Add the Xcimer commercialization whitepaper via `add-source`
3. Run `update-analysis` to incorporate the new source
4. Diff and spot-check the analysis before/after source addition

### Out of Scope
- Testing URL-based source addition (PDF only in this test)
- Testing other concepts besides 17
- Fixing bugs found (document them, fix separately)
- Testing `--force` re-extraction

### Edge Cases & Considerations
- The Xcimer whitepaper (28 pages, 21.6MB) is a substantial PDF with figures and tables — tests the extraction pipeline under realistic load
- Concept 17 already has an `xcimer-science-page` source — the new whitepaper should add significantly more detail, making diffs detectable
- The existing analysis already discusses Xcimer's HDD approach from the science page — spot checks should focus on **new** quantitative detail only available in the whitepaper

---

## Requirements

### Functional Requirements

#### Test 1: Re-analysis with Replaced Sources

1. **FR-1**: Run each stage individually on concept 17a (Xcimer / hybrid drive). Each stage MUST complete without errors: gap-check, analyze, model-setup, review. Inspect output after each stage.

   > **Note:** Concept 17 was split into 17a (Xcimer, hybrid direct drive) and 17b (Focused Energy, fast ignition). Both share the `17-laser-icf-direct-drive` research directory. This test targets **17a** since the Xcimer whitepaper is the new source. The pipeline uses `_research_id` to resolve to the shared directory.

2. **FR-2**: Save a copy of the analysis output (`iter-02/output.md`) before the next test, so we have a baseline for diffing.

#### Test 2: Source Addition (Item 3 Manual Tests)

3. **FR-3**: Run `add-source 17 ~/1cfe/XEC-20260224-Commercialization-of-LFE-Whtppr-SHARED-24-FEB-26.pdf`. Command MUST:
   - Create a companion directory in `iter-02/sources/` with a slugified name
   - Produce `output.md` inside the companion directory
   - Create a symlink `<name>.md` pointing to `<name>/output.md`
   - Include provenance artifacts (`raw.pdf`, `metrics.json`)

4. **FR-4**: Verify the new source is discoverable: `find_sources("17-laser-icf-direct-drive")` MUST include the new source.

#### Test 3: Update Analysis (Item 3 Manual Tests)

5. **FR-5**: Run `update-analysis 17 --sources <new-source-name>`. Command MUST:
   - Create a `feedback_update_<ts>.md` file with F-N format findings
   - Modify `iter-02/output.md` (the analysis) to incorporate findings
   - Save audit trail prompts (`source_integration_prompt_<ts>.md`, `update_analysis_prompt_<ts>.md`)

6. **FR-6**: Downstream staleness SHOULD be propagated (if applicable artifacts exist).

#### Test 4: Diff and Spot Checks

7. **FR-7**: Diff the analysis before and after `update-analysis`. The diff MUST be non-trivial (not just whitespace or timestamp changes).

8. **FR-8**: Spot-check the updated analysis against the Xcimer whitepaper. The following specific claims from the paper SHOULD appear in or influence the updated analysis (check at least 5 of these 8):

   | # | Whitepaper Claim | Paper Location | What to Look For in Analysis |
   |---|---|---|---|
   | SC-1 | KrF excimer laser cost: $100-120/J FOAK, $60-80/J NOAK | p18-20, Table 1 | Specific $/J laser cost figures for Xcimer (existing analysis only has generic "low-cost" from science page) |
   | SC-2 | DPSSL comparison: $700-1,000/J long-term best-case | p9-12 | Comparative cost framing against solid-state alternatives |
   | SC-3 | Two-beam architecture (vs NIF's 192) with <1 m² total aperture | p12 | Beam count and aperture specifics for Xcimer |
   | SC-4 | HYLIFE-based thick-liquid-wall chamber (FLiBe/FLiNaK) | p22-24 | Chamber design details beyond generic "thick-liquid wall" |
   | SC-5 | Target capsule gain >200 at 10 MJ coupling energy | p20-21 | Gain target and energy coupling specifics |
   | SC-6 | Roadmap: Phoenix→Anvil→Vulcan→Athena (Q2 2026→2035) | p25-28 | Named milestones with dates and energy scales |
   | SC-7 | Wall-plug efficiency >5% (vs NIF's 0.5%) | p12 | Efficiency comparison between KrF and NIF/DPSSL |
   | SC-8 | Tritium inventory <200g commercial, TBR ~1.05 with FLiBe | p24 | Tritium breeding and inventory specifics |

---

## Acceptance Criteria

### Test 1: Re-analysis
- [x] `stage1-all 17` completes without errors — ran as individual stages, all exit 0
- [x] Analysis output exists at `iter-02/output.md` (142 lines, differentiation table) + `analyses/17a-.../analysis.md` (435 lines, detailed analysis)

### Test 2: Source Addition
- [x] Companion directory created with `output.md`, `metrics.json` (note: no `raw.pdf` — see bug log)
- [x] Symlink exists and resolves correctly (`readlink` confirms `<name>/output.md`)
- [x] New source discoverable in `ls` alongside 3 existing sources

### Test 3: Update Analysis
- [x] `feedback_update_*.md` exists with F-N format (2 files: dry-run + full)
- [x] `source_integration_prompt_*.md` and `update_analysis_prompt_*.md` saved
- [x] `analysis.md` modified with whitepaper content (note: spec said `output.md` but pipeline correctly targets `analysis.md`)

### Test 4: Spot Checks
- [x] Diff is non-trivial (435-line analysis with 39 whitepaper-specific term mentions)
- [x] 6 of 8 spot checks pass (+ 1 partial) — exceeds ≥5 threshold
- [x] Failures documented: SC-6 partial (Anvil/Vulcan missing), SC-8 fail (TBR/tritium specifics from unextracted source)

### Bug Documentation
- [x] Documented in plan.md Bug/Issue Log: (1) no `raw.pdf` provenance copy [Low], (2) spec assumed `output.md` modified but pipeline correctly targets `analysis.md` [Info]

---

## Execution Notes

### Commands (in order)

```bash
# Test 1: Re-analysis with replaced sources
cp exploration/phase_1a/research/17-laser-icf-direct-drive/iter-02/output.md \
   /tmp/concept17-baseline-analysis.md
uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all 17

# Test 2: Source addition
uv run python exploration/concept_analysis/scripts/run_analysis.py \
  add-source 17 ~/1cfe/XEC-20260224-Commercialization-of-LFE-Whtppr-SHARED-24-FEB-26.pdf

# Verify source placement
ls -la exploration/phase_1a/research/17-laser-icf-direct-drive/iter-02/sources/

# Test 3: Update analysis
uv run python exploration/concept_analysis/scripts/run_analysis.py \
  update-analysis 17 --sources <new-source-name>

# Test 4: Diff
diff /tmp/concept17-baseline-analysis.md \
     exploration/phase_1a/research/17-laser-icf-direct-drive/iter-02/output.md
```

### Cost Estimate
- `stage1-all`: ~$1-2 (Sonnet, multiple agent calls)
- `add-source` extraction: ~$1-2 (28-page PDF via agentic-mbse extract)
- `update-analysis`: ~$0.50-1 (two Claude calls: pre-pass + feedback-pass)
- **Total**: ~$3-5

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_concept_analysis_v2.md` (Items 1 and 3)
- **Source Addition Plan:** `.project/active/source-addition/plan.md` (deferred manual tests)
- **Concept Directory:** `exploration/phase_1a/research/17-laser-icf-direct-drive/`
- **Test PDF:** `~/1cfe/XEC-20260224-Commercialization-of-LFE-Whtppr-SHARED-24-FEB-26.pdf`

---

**Next Steps:** Execute tests in order. Document results inline under a "Test Results" section appended to this spec.
