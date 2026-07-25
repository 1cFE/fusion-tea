---
Status: completed
Scale: trivial
Epic: none (standalone)
Owner: reid
Created: 2026-07-18
Updated: '2026-07-25'
---

# WI-026: Pytest Baseline Re-Record

## Overview

The model test suite (`tests/models/`) has carried an 11-failed baseline since WI-019: 1 `test_foundation` element-count test + 10 `test_power_balance` tests that target the pre-WI-009 model layout (an `Alpha Power Calc` and file paths that no longer exist). Every item since has run with the weak bar "tally unchanged vs 11/18/14/0" instead of green.

Registered at the WI-025 Align (2026-07-18, deliberately out of WI-025 scope). Sequencing ruled [OWNER] 2026-07-25: immediately after WI-029 close, before demo Item 5 (studies). Pick-up ruling (recorded in the demo epic Board housekeeping): fix-vs-retire decided at pick-up — **decided: fix.** The stale tests are rewritten against the current model layout (the power-balance file covers the model spine; deleting coverage there would be retiring the wrong thing).

## Requirements

- MR-WI026-1: `uv run pytest tests/models/ -q` exits with **0 failed, 0 errors** (green baseline). Skips may remain.
- MR-WI026-2: The rewritten tests preserve the originals' intent (file existence, calc-def existence, interface inputs/outputs, documentation presence) but target the current layout (`models/library/analyses/mfe_power_balance.sysml`, `'MFE Power Balance Calc'`, and the current foundation element set).
- MR-WI026-3: No model (`.sysml`) file changes — tests conform to the model, never the reverse.
- MR-WI026-4: Currently-passing and skipped tests untouched.

## Out of Scope

- New test coverage beyond refreshing the stale set.
- The exec-pipeline / handshake test tiers (their bars live with the demo items).

## Completion Record

**Executed 2026-07-25.** `uv run pytest tests/models/ -q` → **30 passed / 13 skipped / 0 failed / 0 errors**, stable across repeat runs (was 11 failed / 18 passed / 14 skipped). Two files changed, both under `tests/models/` (132 insertions, 71 deletions); no model files touched (MR-WI026-3 verified via `git status`).

- **Fix-not-retire executed**: all 10 stale `test_power_balance` tests rewritten intent-preserving against the current layout — power balance lives at `models/library/analyses/mfe_power_balance.sysml`; the old standalone `Alpha Power Calc`, `fuel_type` parameterization, and generic `Power Balance Calc`/`power_balance.sysml` genuinely no longer exist (alpha inlined as `p_alpha = (3.52/17.58)·p_nrl`, D-T fixed, single MFE calc), so those tests now assert the collapse/inline rather than the vanished constructs. Required-input list re-recorded to the current 15 (dropped `fuel_type`/`fpcppf`, added `p_pump`).
- `test_foundation_element_counts` re-pointed from stale ≥13/≥6/≥12 counts to named-membership asserts (`CAS Scope`, `Economic Parameter`, `Costed Component`) with the slimming rationale documented in the docstring.
- Side effect: the shared `POWER_BALANCE_DIR` path fix un-skipped `test_power_balance_parses_without_errors`, which now passes (hence 30 passed, 13 skipped).
- **Standing-bar consequence**: the per-item pytest bar changes from "tally unchanged vs 11/18/14/0" to **green (0 failed / 0 errors)** for all subsequent items.
