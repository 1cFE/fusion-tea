# Epic: Source Extraction Fix & Re-extraction

> **Archived 2026-08-21** — Abandoned — superseded by source-replacement + orig-md-research (2026-04-11). Status audit: `.project/reports/2026-08-21-1339-status-report.md`.

**Epic ID**: SOURCE-FIX
**Status**: Draft
**Priority**: P0
**Created**: 2026-03-29
**Estimated Effort**: ~3-5 days

---

## Executive Summary

The previous source-replacement run (concepts 01-22) used trafilatura for HTML extraction, which mangled scientific tables and equations. Arxiv HTML now routes through pandoc in agentic-mbse. Validate the fix is sufficient, define quality gates so we don't redo this again, re-run all affected sources, and clean up leftover `.orig.md` files.

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

### Item 1: Validate & Fix Extraction Quality (upstream + here)
**Effort**: 1-2 days
**Repo**: `~/1cfe/agentic-mbse` + `fusion-tea`
**Scope**:
- [ ] Validate arxiv HTML extraction quality now that arxiv routes through pandoc
- [ ] Test against `arxiv-2411-06644` Table 3 as reference case — must have parameter names, units, correct row alignment
- [ ] Validate image saving works for HTML extractions
- [ ] Validate general HTML quality (list markers, equations, structured content)
- [ ] Fix any remaining issues found during validation
- [ ] Define quality gate criteria so we don't have to redo extractions again

**Context**: Previous source-replacement (concepts 01-22) used trafilatura for HTML, which mangled scientific tables/equations. Arxiv links now route through pandoc extraction. This item validates the fix is sufficient before re-running.

**Reference bad output**: `exploration/phase_1a/research/11-magnetic-mirror/iter-01/sources/arxiv-2411-06644-confinement-predictions.md`
**Source URL**: https://arxiv.org/html/2411.06644v1#S4.T3

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
- [ ] Quality gate criteria defined and documented — extraction validated before bulk re-run
- [ ] HTML images saved locally alongside markdown
- [ ] All arxiv HTML (and affected HTML) sources re-extracted and usable
- [ ] No `.orig.md` files remain in source directories
- [ ] Analysis pipeline agents get clean source data
