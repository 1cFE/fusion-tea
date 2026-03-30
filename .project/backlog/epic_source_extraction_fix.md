# Epic: Source Extraction Fix & Re-extraction

**Epic ID**: SOURCE-FIX
**Status**: Draft
**Priority**: P0
**Created**: 2026-03-29
**Estimated Effort**: ~3-5 days

---

## Executive Summary

The agentic-mbse HTML extraction (trafilatura backend) produces broken tables from arxiv HTML sources — parameter names are stripped, rows are misaligned, and the output is unusable for analysis. Fix the upstream extraction, re-run all affected sources, and clean up leftover `.orig.md` files from the previous source-replacement work.

---

## Why This Epic?

**Current State**:
- Arxiv HTML table extraction is broken: parameter names stripped, row alignment lost, units orphaned (see `arxiv-2411-06644-confinement-predictions.md` Table 3)
- Images from HTML sources are not saved locally
- General HTML extraction quality is poor beyond just tables
- `.orig.md` files from source-replacement confuse analysis agents (they match `sources/*.md` glob)

**Future State**:
- HTML extraction produces usable tables with parameter names, units, and correct alignment
- Images from HTML sources are saved alongside extracted markdown
- All arxiv HTML (and potentially all HTML) sources re-extracted with fixed tooling
- No `.orig.md` files cluttering the source directories

---

## Dependency Chain

Items must be completed in order:

1. **Fix upstream extraction** (agentic-mbse repo) — blocking everything else
2. **Re-run extractions** — depends on #1
3. **Clean up .orig.md files** — depends on #2 (need re-extracted files before deleting originals)

---

## Backlog Items

### Item 1: Fix agentic-mbse HTML Extraction (upstream)
**Effort**: 1-3 days
**Repo**: `~/1cfe/agentic-mbse`
**Scope**:
- [ ] Fix table extraction from arxiv HTML (parameter names, row alignment, units)
- [ ] Add local image saving for HTML extractions
- [ ] General HTML extraction quality improvements
- [ ] Test against `arxiv-2411-06644` as reference case

**Known bad output**: Tables have empty parameter columns, orphaned unit rows (`m-3`), missing section headers within tables.

**Reference**: https://arxiv.org/html/2411.06644v1#S4.T3

### Item 2: Re-run Source Extractions
**Effort**: 1-2 days
**Repo**: `fusion-tea`
**Scope**:
- [ ] Re-run all arxiv HTML source extractions with fixed tooling
- [ ] Evaluate whether all HTML sources need re-extraction (not just arxiv)
- [ ] Restart/continue from `.project/active/source-replacement/plan.md`
- [ ] Verify table quality in re-extracted output

**Depends on**: Item 1

### Item 3: Clean Up .orig.md Files
**Effort**: 0.5 day
**Repo**: `fusion-tea`
**Scope**:
- [ ] Delete all `.orig.md` files across `exploration/` source directories
- [ ] Verify no pipeline breakage from removal
- [ ] Confirm analysis agents no longer pick up stale originals

**Depends on**: Item 2

---

## Success Criteria

- [ ] Table 3 from arxiv-2411-06644 renders with correct parameter names, values, and units
- [ ] HTML images saved locally alongside markdown
- [ ] All arxiv HTML sources re-extracted and usable
- [ ] No `.orig.md` files remain in source directories
- [ ] Analysis pipeline agents get clean source data
