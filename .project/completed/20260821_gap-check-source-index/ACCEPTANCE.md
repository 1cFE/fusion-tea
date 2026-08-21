# Acceptance Review

**Status:** Accepted (2026-05-22)
**Scope:** Fleet regeneration of `gap_report.md` for 40 active concepts after SOURCE_INDEX injection (issue #27 systemic fix)
**Final pass:** Phase 3 (strict-read prompt), all 40 active concepts regenerated, preambles stripped.

---

## Final verdict (Phase 3)

Phase 2 (first fleet regen) exposed a bug: SOURCE_INDEX injection made the LLM *aware* of fleet sources but didn't reliably make it *read* them — 23/40 concepts only mentioned fleet sources in §6 recommendations without opening them, biasing `blocking_count` high. Concept 01 was the clearest case (regen produced `blocking_count: 4` with the LLM stating *"tea_dt_mfe_cost_analysis has not been read but is directly applicable"*).

The template was patched to make source reading **mandatory** (open-or-disqualify-with-reason, no deferral), Write-tool usage forbidden (was clobbering full reports with summaries), and preambles suppressed (post-processed via `strip_preambles.py` for residual non-compliance).

After Phase 3 regen across all 40 active concepts:
- **All 40 reports** parse cleanly (`## Structured summary` block present, `blocking_count` extractable).
- **Σ Δblocking_count vs. Phase 2 = -51** (mean -1.27 per concept) — the LLM is now reading fleet sources and applying real downgrades.
- **Concept 01** independently arrived at `blocking_count: 1`, matching the original surgical-fix analyst judgment from 2026-05-20.
- **26/40 concepts** changed Data Availability tier; the aggregate shift is upward (16 +1, 4 +2, 6 -1), reflecting that concepts now properly get credit for fleet-wide cost analogs.

### Manual spot-check of the surprising deviations

Six concepts manually inspected — `35-polomac` (-7), `31-laser-icf-oec` (-5), `21-spherical-tokamak-hts` (4→0), `07-maglif` (+3), `11-magnetic-mirror` (+3), `12-levitated-dipole` (Phase 2 0-without-reading corrected to 2-with-reading). All defensible:

- Big downgrades trace to either (a) gap deduplication (35) or (b) specific fleet-source numeric integration (31: Hawker $25-100/MWh, Xcimer <$100/J; 21: $8,800-22,200/kW, ARIES CAS).
- Upgrades (07, 11) trace to more granular gap enumeration after deeper source reading (AMPS commercial-chamber deferral, Realta no-plant-study).
- No hallucinated blockers; no magical downgrades.

The Phase 3 reports are accepted as the new fleet baseline. Downstream `populate_data_availability.py` can be rerun to refresh scoring.

---

## Historical record (Phase 2 — superseded)

The remainder of this document records the Phase 2 audit that motivated the Phase 3 redo. Retained for traceability.

---

## TL;DR (Phase 2 — superseded)

The systemic fix worked at the plumbing level (all 40 reports regenerated cleanly; all have parseable `## Structured summary` blocks). The LLM's *behavior* on fleet sources is **inconsistent**:

- **15 concepts** (~38%): fleet sources integrated into §1-5 gap tables (classes 1, 2) — the intended effect.
- **23 concepts** (~58%): fleet sources listed in §6 Source Recommendations only, not opened during the gap assessment (classes 1a, 2a). The injection made the LLM *aware* of fleet sources but did not consistently make it read them.
- **2 concepts** (~5%): no fleet citations at all — legitimate non-applicability for exotic concepts (16-muon-catalyzed, 19-orbital-levitated-dipole).

**Net `blocking_count` delta across the fleet: +9** (i.e. very small at the aggregate level). 14 of 40 concepts changed Data Availability tier (mostly ±1).

**Recommended verdict:** **Accept with one exception** — concept 01 is a known information regression (the surgical fix from 2026-05-20 was partially clobbered). Decide whether to revert concept 01 to its surgical-fix baseline or accept the regen.

---

## Aggregate metrics

| Metric | Value |
|--------|-------|
| Concepts regenerated | 40 (of 41 in `analyses/`; concept 34 orphaned — out of scope) |
| Reports with parseable `blocking_count` | 40/40 |
| Net Σ Δ `blocking_count` | +9 |
| Concepts with `blocking_count` unchanged | 11 |
| Concepts within \|Δ\| ≤ 2 | 28 (70%) |
| Concepts with \|Δ\| ≥ 3 (Phase 2 flag threshold) | 10 |
| Concepts with Data Availability tier change | 14 (35%) |
| Concepts where DA tier dropped by 2 | 2 (`31-laser-icf-oec-architecture`, `38-particle-accelerator-driven-fusion`) |
| Concepts where DA tier rose by 2 | 1 (`12-levitated-dipole`) |

---

## Per-deviation-class counts

| Class | Count | Notes |
|-------|-------|-------|
| 1 — fleet-downgrade (integrated AND Δ<0) | 5 | Intended effect. Accept. |
| 2 — fleet-reclassify (integrated, Δ≥0) | 10 | Tier-within reclassification. Accept. |
| 1a — recommend-only downgrade SUSPECT | 7 | Δ<0 without integration. **Inspect** (see below). |
| 2a — recommend-only (Δ≥0) | 16 | Injection partial-failure but harmless. Accept. |
| 3 — no fleet, small drift (\|Δ\|≤2) | 2 | Accept as noise (concepts 16, 19 — exotic, no applicable fleet source). |
| 5 — regression (lost prior integration) | 1 | Concept 01. **Inspect.** |

Full per-concept table: see `phase2_summary.md`.

---

## Concepts flagged for inspection

### Concept 01 — `01-hts-compact-tokamak` — **CLASS 5 REGRESSION**

- **Baseline `blocking_count`: 1** (after surgical fix from 2026-05-20 that integrated `tea_dt_mfe_cost_analysis/` and downgraded 3 of 4 blockers to important).
- **New `blocking_count`: 4** (Δ=+3, tier 4 → 3).
- **Root cause:** The regenerated report explicitly states (line 172): *"`tea_dt_mfe_cost_analysis` (already in source index): This D-T MFE cost analysis at `knowledge/sources/tea_dt_mfe_cost_analysis/` has not been read but is directly applicable... Should be read before constructing the quantitative LCOE model."* The LLM was aware of the source via the SOURCE_INDEX injection but **did not open it during this regeneration**. The 4 blockers it now lists (full plant capital cost, capacity factor, scheduled maintenance, tritium startup inventory) are the same gaps the surgical fix had downgraded.
- **Options:**
  - **(a) Revert** `analyses/01-hts-compact-tokamak/gap_report.md` to the snapshot at `/tmp/gap_baselines_2026-05-22/01-hts-compact-tokamak.md` — preserves the surgical-fix knowledge, but the report's "Revision 2026-05-20 — surgical regeneration" header now sits inside a fleet-systemic-fix branch, which is a slight historical inconsistency.
  - **(b) Re-regenerate concept 01 alone** with a stronger prompt addendum (e.g. "before classifying any LCOE gap as blocking, you MUST open and read any fleet source flagged in §6 if it could plausibly address that gap") — addresses the root cause for future regenerations too.
  - **(c) Accept the regen** as the new normal — concept 01 loses the special-case status, the systemic fix gives a weaker answer than the surgical fix did, and the analyst can re-do the surgical pass downstream if it matters.

**Recommendation: (a) Revert.** Reason: the surgical fix's content was correct and is documented; re-running with a prompt addendum (option b) introduces a one-off process change for a single concept and the LLM may still not comply; option (c) accepts a known information loss.

### Class 1a SUSPECT (`recommend-only-downgrade`) — 7 concepts

These all dropped `blocking_count` by 1-3 without integrating any fleet source into §1-5 of the report. Either the LLM downgraded based on awareness of fleet sources without actually reading them, or these are class-3 judgment drift that happened to coincide with fleet sources being recommended in §6.

| concept | bc baseline → new | Δ |
|---------|-------------------|---|
| `11-magnetic-mirror`                  | 4 → 3 | -1 |
| `18-p-b11-frc`                        | 8 → 5 | -3 |
| `22-projectile-icf`                   | 7 → 5 | -2 |
| `23-laser-icf-nanostructured-target`  | 7 → 6 | -1 |
| `27-polywell`                         | 7 → 6 | -1 |
| `30-laser-icf-nif-commercialization`  | 5 → 4 | -1 |
| `39-spherical-tokamak-cs-free-p-b11`  | 8 → 7 | -1 |

**Recommendation: accept as noise** per the Phase 1 decision rule for judgment-drift downgrades. Reason: 6 of 7 are within ±1; `18-p-b11-frc` is the only large mover (-3). Even for `18`, the new report retains 5 blockers in §5, so the data-availability story isn't materially overstated. Spot-check `18-p-b11-frc` only if anyone wants a 5-minute sanity look at the rationale.

### Class 2 / 2a concepts that crossed a tier boundary upward — 4 concepts

These had `blocking_count` drop enough to move Data Availability tier up by 1-2. Two have integrated fleet sources (class 2); two are recommend-only (class 2a, suspicious).

| concept | bc baseline → new | Δtier | class | notes |
|---------|-------------------|-------|-------|-------|
| `12-levitated-dipole`                 | 4 → 0 | +2 | 2a | Suspicious — went to 0 blockers with fleet sources cited as §6 recommendations only |
| `18-p-b11-frc`                        | 8 → 5 | +1 | 1a | Suspicious (already flagged above) |
| `25-heavy-ion-beam-icf`               | 2 → 0 | +1 | 1  | Integrated fleet sources; accept |
| `30-laser-icf-nif-commercialization`  | 5 → 4 | +1 | 1a | Already flagged above |
| `39-spherical-tokamak-cs-free-p-b11`  | 8 → 7 | +1 | 1a | Already flagged above |

**Concept 12 is the most suspicious upward mover** (tier 3 → 5, the highest possible). Worth a 5-minute sanity look — but baseline already had `Mostly Ready` with 4 blockers, and the new report is internally coherent (lists 5 important gaps; reframes blockers as derivable analogue work). Plausible that the LLM made a defensible judgment call. Recommend spot-check but lean accept.

### Class 1a / 2 concepts that crossed a tier boundary downward — 7 concepts

These had `blocking_count` rise enough to move Data Availability tier down by 1-2.

| concept | bc baseline → new | Δtier | class |
|---------|-------------------|-------|-------|
| `01-hts-compact-tokamak`              | 1 → 4 | -1 | 5 (regression — see above) |
| `03-laser-icf-liquid-jet-target`      | 7 → 8 | -1 | 2a |
| `04-laser-icf`                        | 4 → 7 | -1 | 2a |
| `09-qi-stellarator-hts`               | 2 → 3 | -1 | 2a |
| `10-large-scale-stellarator`          | 0 → 2 | -1 | 2 |
| `31-laser-icf-oec-architecture`       | 4 → 8 | -2 | 2 |
| `36-helical-coil-stellarator`         | 1 → 4 | -1 | 2 |
| `37-magnetized-target-inertial-fusion-mtif` | 6 → 9 | -1 | 2 |
| `38-particle-accelerator-driven-fusion` | 4 → 8 | -2 | 2a |

**Pattern:** most of these are LLM finding MORE blockers in the new run, often while citing fleet sources (class 2) — the fleet sources help the LLM identify gaps it didn't see before, even if the same sources don't fully fill them. This is a legitimate outcome of regeneration. **Recommend accept** for all except concept 01.

---

## Concept 34 — out of scope

`34-compact-spherical-tokamak-india` is orphaned (has `analyses/` dir but no row in `table.csv`). Per analyst direction (2026-05-22), concept 34 is being deprecated as insufficient data to pursue; no action taken in this work item. Its `gap_report.md` is unchanged from baseline (`blocking_count: 12`).

---

## Pre-existing template fix

Phase 1 surfaced that `gap_check.md` never required the `## Structured summary` YAML block — 40/41 reports had it by LLM convention. The template now mandates it (`prompt_templates/gap_check.md`). All 40 Phase 2 regenerations produced the block. Net: a previously-fragile convention is now spec.

---

## Sign-off

If accepting the recommended actions:

- [ ] Revert `analyses/01-hts-compact-tokamak/gap_report.md` to `/tmp/gap_baselines_2026-05-22/01-hts-compact-tokamak.md`
- [ ] Run `uv run python exploration/scoring_v2/scripts/populate_data_availability.py` to repopulate the Data Availability scoring block
- [ ] Spot-check `12-levitated-dipole` and `18-p-b11-frc` (5 minutes each) — accept or flag for surgical follow-up
- [ ] Commit on `fix/gap-check-source-index-injection`, open PR, close issue #27

**Accepted by:** _<analyst>_
**Date:** _YYYY-MM-DD_
**Exceptions / overrides:** _<list any concept-specific decisions that differ from above>_
