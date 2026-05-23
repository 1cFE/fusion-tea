## Implementation Plan: Inject SOURCE_INDEX.md into gap-check prompt

**Status:** Draft
**Created:** 2026-05-22
**Last Updated:** 2026-05-22

## Source Documents

- **Issue:** https://github.com/1cFE/fusion-tea/issues/27 — "Gap check only consults phase 1a research sources"
- **Spec / design:** none (small systemic fix; the issue body is the spec)
- **Reference artifact:** `exploration/concept_analysis/analyses/01-hts-compact-tokamak/gap_report.md` — the surgical fix that this work generalizes. Revision header documents the blind spot and what the corrected output looks like.

## Background (one paragraph)

`cmd_gap_check` in `exploration/concept_analysis/scripts/run_analysis.py:195` builds the gap-check prompt by passing `find_sources(rid)` into the `{{source_file_list}}` slot of `prompt_templates/gap_check.md`. `find_sources()` (`scripts/lib/sources.py:9`) only scans `knowledge/concept_research/<concept>/iter-*/sources/*.md`. The fleet-wide source pool in `knowledge/sources/` (registered in `knowledge/SOURCE_INDEX.md`, 12 entries) is invisible to the agent, so an ingested-but-not-concept-scoped source — e.g. Araiinejad & Shirvan 2025 — cannot influence the gap assessment. `blocking_count` from the gap report is now load-bearing input to the Data Availability scoring axis (`exploration/scoring_v2/scripts/populate_data_availability.py`), so understated reports translate directly into understated scores.

## Implementation Strategy

**Phasing Rationale:**
The fix is small (one template edit + one prompt-fill change). The risk is *not* in writing the code; it is in (a) whether the LLM actually integrates the general-pool sources when given them, and (b) whether forcing a regeneration causes unrelated sections to drift in ways that move `blocking_count` for the wrong reasons. So Phase 1 is the smallest end-to-end test that exposes both risks on one concept; Phase 2 is the human verification that decides whether to fleet-roll-out.

**Critical Path:**

1. Edit template + `cmd_gap_check` to inject `SOURCE_INDEX.md` content alongside the concept-scoped source list.
2. Run `gap-check 33 --force` (after stashing the existing report).
3. Manually diff and judge.

**First Proof Point:**
The regenerated `analyses/33-state-backed-tokamak-best/gap_report.md` cites at least one source from `knowledge/sources/` (e.g. `tea_dt_mfe_cost_analysis`, ARIES) that the prior report did not cite, AND reclassifies at least one of its current blockers (BoP / capital / O&M / capacity factor) on the basis of that source — mirroring the concept-01 outcome.

**Overall Validation Approach:**
Manual review against a saved baseline copy of the prior gap report. No automated tests added — this is a prompt-engineering change whose correctness is judged by a human reading two markdown reports side by side.

---

## Phase 1: Hand-test the injection on concept 33

### Goal
Land the smallest code change that makes `SOURCE_INDEX.md` visible to gap-check, regenerate concept 33's gap report, and inspect the result.

### Assumption Under Test
The LLM, given a list of repo-wide TEA sources in addition to the concept-scoped sources, will (a) recognize the relevant ones and (b) integrate them into the gap assessment well enough to reclassify gaps that those sources actually address. If this fails for concept 33 — which sits in the same family as concept 01 and has the same kind of blockers — the systemic fix is the wrong shape and we need the lint-script alternative from issue #27 instead.

### Test Concept Choice
**`33-state-backed-tokamak-best`** — D-T MFE tokamak, `blocking_count: 4`. The current `gap_report.md` lists BoP, capital cost, O&M, and capacity factor as blocking — exactly the gap profile that `tea_dt_mfe_cost_analysis` (Araiinejad & Shirvan 2025) resolved for concept 01. Has not been surgically revised, so it is a clean test of whether systemic injection reproduces the concept-01 outcome organically.

### Test Stencil (Write This First)
No automated test for this phase — the artifact under test is a markdown report. The "stencil" is the manual acceptance checklist:

```text
Acceptance for Phase 1 regeneration of analyses/33-state-backed-tokamak-best/gap_report.md:

1. The new report cites at least one source from knowledge/sources/ that
   the prior report did not cite.
2. At least one of the prior blocking gaps (BoP, capital, O&M, CF) is
   downgraded or removed, with the new source named in the justification.
3. blocking_count in the trailing structured block reflects the new
   count.
4. No section drifts in a way that introduces a NEW blocking gap that
   the prior report did not have AND that is not justified by new
   content from a general-pool source.
5. The Overall Readiness rating and Summary read coherently — no
   internal contradictions between sections.
```

### Changes Required

#### 1. `exploration/concept_analysis/prompt_templates/gap_check.md`

Add a new section between the existing "Extracted Source Documents" block and "Reference Documents":

- [ ] Add `### Fleet-Wide TEA / Cost Analog Sources` subsection
- [ ] Insert `{{source_index_content}}` placeholder
- [ ] Add one paragraph of guidance: these are repo-wide sources not scoped to this concept; the agent should consult them when they are relevant cost analogs or methodology references, cite them by repo path, and prefer concept-scoped sources for concept-specific claims
- [ ] Update the "Read each source document" instruction in step 2 to also cover the fleet-wide list, with a caveat that not every fleet source will be relevant to every concept

#### 2. `exploration/concept_analysis/scripts/run_analysis.py`

In `cmd_gap_check` (line 195) where `fill_template` is called:

- [ ] Read `knowledge/SOURCE_INDEX.md` into a string
- [ ] Pass it as `source_index_content` in the template fill dict
- [ ] Decide the path constant: add `SOURCE_INDEX_PATH = REPO_ROOT / "knowledge" / "SOURCE_INDEX.md"` near the existing `BRIEF_PATH` / `SCHEMA_PATH` constants for symmetry

#### 3. Preserve baseline before regeneration

- [ ] `cp exploration/concept_analysis/analyses/33-state-backed-tokamak-best/gap_report.md /tmp/gap_report_33_baseline.md`
- [ ] Capture `blocking_count` and the four blocking gaps from the baseline (write them into the Implementation Notes section below before running the regeneration)

#### 4. Regenerate

- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py gap-check 33 --force`
- [ ] Confirm exit status 0 and that the new `gap_report.md` mtime is fresh

### Validation

**Automated:**
- [ ] Script exits 0; file is rewritten; trailing `blocking_count: N` block parses (eyeball — no parser change is needed for Phase 1)

**Manual (this is the load-bearing validation):**
- [ ] Diff `/tmp/gap_report_33_baseline.md` vs. the new report (`diff -u` for skim; full read for judgment)
- [ ] Walk the 5-item acceptance checklist above
- [ ] If any new source from `knowledge/sources/` is cited, verify it actually says what the new report claims it says (open the extracted `.md`, spot-check the cited claims)
- [ ] If `blocking_count` moved, verify the delta is justified by general-pool source content, not by the LLM rewording or rejudging the original concept-scoped sources

**What We Know Works After This Phase:**
The plumbing carries `SOURCE_INDEX.md` into the prompt, AND on at least one representative D-T MFE concept the LLM actually used the general-pool sources to revise its gap assessment. If validation fails, Phase 2 does not start — we revisit the design (e.g. lint-script alternative from issue #27).

**Decision gate at end of Phase 1:**
- ✅ Acceptance checklist clean → proceed to a fresh `/_my_plan` for Phase 2 (fleet roll-out + scoring rerun)
- ⚠️ Mixed (the injection worked but report drifted on unrelated sections) → narrow the prompt (e.g. instruct the LLM to mark which sections it changed and why) before fleet roll-out
- ❌ Injection had no effect, or effect was wrong → revert template change, open a follow-up to implement the lint-script alternative

---

## Phase 2: Fleet-wide regeneration + per-concept diff capture

### Goal
Regenerate `gap_report.md` for all 40 remaining concepts (concept 33 already done in Phase 1; concept 01 was surgically revised on 2026-05-20 and should be regenerated alongside the rest to remove the special-case status) and capture per-concept diffs against the prior baseline so that every deviation is recorded, not silently absorbed.

### Assumption Under Test
Per-concept LLM judgment drift on regeneration stays within the tolerable envelope observed in Phase 1 (±1 on `blocking_count`, with most movement attributable to new fleet citations rather than rejudgment of existing concept-scoped content). If any single concept moves `blocking_count` by ≥3 with no fleet-source justification, that's a signal the prompt needs narrowing before continuing.

### Changes Required

#### 1. Baseline snapshot
- [ ] `mkdir -p /tmp/gap_baselines_2026-05-22`
- [ ] Copy all current `analyses/*/gap_report.md` files into the snapshot dir (preserve concept-id-named filenames)
- [ ] Record the baseline `blocking_count` for each concept in a small CSV at `.project/active/gap-check-source-index/phase2_baselines.csv` (columns: `concept_id,baseline_blocking_count,baseline_important_count,baseline_overall_rating`) — extract with a one-off awk/grep over the snapshot

#### 2. Regenerate
- [ ] Skip concept 33 (already done as Phase 1 artifact)
- [ ] Run `uv run python exploration/concept_analysis/scripts/run_analysis.py gap-check <id> --force` for each remaining concept. Drive this with a small shell loop; capture stdout/stderr per concept under `/tmp/gap_baselines_2026-05-22/<concept_id>.log` so failures are traceable
- [ ] Note: each call is ~3-5 minutes wall time × 40 concepts ≈ 2-3 hours total. Run sequentially (rate-limit safety); no need to parallelize
- [ ] After each run, immediately confirm the new file has a parseable `## Structured summary` with `blocking_count:` — if not, mark that concept and continue; revisit at the end (Phase 1 caught one such failure mode; the template fix should prevent it but verify)

#### 3. Per-concept diff capture
- [ ] For each concept, produce a structured deviation record at `.project/active/gap-check-source-index/diffs/<concept_id>.md` containing:
  - `blocking_count` baseline → new, with delta
  - `important_count` baseline → new, with delta
  - List of fleet sources newly cited (greps for `knowledge/sources/` and `PyFECONS` against the diff)
  - List of blocking-tier changes (gaps that moved into or out of `blocking` criticality) — each annotated with: justified-by-fleet-source / judgment-drift / other
  - Free-text "notes" field for anything weird
- [ ] Build a summary table at `.project/active/gap-check-source-index/phase2_summary.md` with one row per concept: `concept_id | baseline_blocking | new_blocking | Δ | fleet_sources_cited | judgment_drift_flags`
- [ ] This capture is what makes Phase 3 acceptance reviewable in a single sitting

### Validation

**Automated:**
- [ ] All 40 regenerations exit 0 (or the failures list is short and traceable)
- [ ] All 41 final `gap_report.md` files (40 regenerated + concept 33 from Phase 1) parse cleanly for `blocking_count` via `_structured_blocking_count`
- [ ] `uv run python exploration/scoring_v2/scripts/populate_data_availability.py` runs to completion and updates `gap_report_path` + the data-availability scoring block for every concept

**Manual:**
- [ ] Skim `phase2_summary.md` — flag any concept with |Δ blocking_count| ≥ 3 for closer inspection
- [ ] Spot-check 3-5 concepts at random by opening their diff file and the underlying `gap_report.md` to confirm the deviation record is faithful

**What We Know Works After This Phase:**
Every concept has been re-run through the systemic-fix pipeline; every deviation from baseline is recorded in a per-concept file; the summary table is the input artifact for Phase 3 acceptance review.

---

## Phase 3: Acceptance review of all deviations

### Goal
Walk the full set of per-concept diffs and decide, deviation by deviation, whether each one is acceptable. Produce a single ACCEPTANCE.md that either signs off the fleet regeneration or lists the concepts that need targeted intervention before downstream scoring is recomputed.

### Assumption Under Test
The total set of deviations is small enough to review in one sitting (a few hundred line-level diff entries across 41 concepts) AND the user-judged "acceptable noise" envelope from the Phase 1 decision gate holds across the fleet.

### Known Deviation Classes (carry forward from Phase 1)

These are pre-categorized so the acceptance review knows what to expect and doesn't re-litigate the same call:

1. **Fleet-source downgrades** (e.g. concept 33 O&M `blocking → important` via ARIES-ACT/TEA analog). **Default: accept** — this is the intended effect of the systemic fix.
2. **Fleet-source reclassifications** (e.g. capital cost `truly-unknown → derivable` because a fleet analog now exists). **Default: accept**.
3. **Judgment-drift upgrades on unrelated content** (e.g. concept 33 tritium supply `important → blocking` with no fleet-source justification). **Default: accept as noise** per user direction (2026-05-22). Flag for the record but do not roll back. Threshold for re-litigation: any single concept with ≥2 such upgrades OR a fleet-wide pattern of the same kind of upgrade (would indicate a prompt issue, not noise).
4. **`blocking_count` unchanged but composition shifted** (e.g. concept 33: one downgrade cancelled one upgrade, net = 4). **Default: accept**; note that the Data Availability score doesn't move, but the underlying gap list is different.
5. **Coherence regressions** (internal contradictions, broken citations, hallucinated sources). **Default: reject** — flag for surgical fix or re-regeneration on the affected concept.
6. **Missing `## Structured summary` block** (Phase 1 caught this once before the template fix). **Default: re-regenerate that concept** — should not occur post-template-fix, but verify.

### Test Stencil
No test code. The acceptance review is a structured human walk:

```text
For each concept in phase2_summary.md:
  Open .project/active/gap-check-source-index/diffs/<concept_id>.md
  Walk each "blocking-tier change" entry:
    Classify against the 6 known classes above
    If class 1-4, mark "accept" with one-line rationale
    If class 5-6, mark "reject" and capture the specific issue
  Aggregate: any concept with ≥1 class-5 reject goes into the "needs intervention" list
Compute fleet aggregates:
  Net blocking_count delta across all concepts (sum of Δ)
  Count of concepts whose Data Availability tier (1-5) would change
  Top 5 concepts by absolute Δ
```

### Changes Required

#### 1. Acceptance write-up
- [ ] Create `.project/active/gap-check-source-index/ACCEPTANCE.md` with:
  - One-line verdict (accept fleet regeneration / accept-with-exceptions / reject)
  - Aggregate metrics (net Δ, tier-change count, top movers)
  - Per-deviation-class counts (how many of each of the 6 classes appeared)
  - "Needs intervention" list (concept_id + issue) — empty if clean
  - Explicit sign-off line: `Accepted by: <user>  Date: YYYY-MM-DD`

#### 2. Targeted fixes for any class-5 rejects
- [ ] For each concept in the "needs intervention" list, choose between:
  - Surgical edit (Claude-assisted, like the concept 01 fix on 2026-05-20)
  - Single-concept regeneration with a narrower prompt
  - Manual edit by the analyst
- [ ] Document the chosen approach per concept in ACCEPTANCE.md

#### 3. Downstream scoring recompute (only after acceptance is signed)
- [ ] Rerun `uv run python exploration/scoring_v2/scripts/populate_data_availability.py`
- [ ] Run the scoring composite (whatever command the v3 pipeline uses for axis composition — check with `exploration/scoring_v2/` README or recent PR if unfamiliar)
- [ ] Diff the resulting per-concept Data Availability scores against pre-Phase-2 scores; record any tier changes
- [ ] If Score Explorer is consuming the scores, refresh the deployed `docs/score-explorer/` copy

### Validation

**Automated:**
- [ ] `populate_data_availability.py` exits 0
- [ ] Score recompute exits 0
- [ ] No concept ends up with `gap_report_path = null` in the populated features (would indicate a missing/broken report)

**Manual:**
- [ ] ACCEPTANCE.md is signed
- [ ] Tier-change list in ACCEPTANCE.md matches the actual computed score deltas (sanity check that the deviation record predicted the score impact)
- [ ] Spot-check 2-3 concepts whose Data Availability tier changed by opening their new `gap_report.md` and the resulting score block; confirm the score reflects the new content

**What We Know Works After This Phase:**
The systemic fix is fully rolled out; every deviation has been seen by a human; Data Availability scores reflect the corrected gap reports; the issue can be closed with a link to ACCEPTANCE.md as the audit trail.

---

## Out of scope for this plan

- Changing the gap_check prompt template beyond the SOURCE_INDEX injection + structured-block requirement (e.g. the "easily parsable" reformat the colleague mentioned — separate work)
- Adding the lint-script alternative from issue #27 — only relevant if the systemic-fix approach had failed at Phase 1
- Re-running upstream Phase 1a research iterations (the systemic fix deliberately avoids touching `iter-*/sources/` — fleet pool injection is read-only)

---

## Environment Setup

See `CLAUDE.md`. Relevant for this work:

- Always `uv run python ...` — never bare `python`
- `gap-check` is a non-deterministic Sonnet call; rerunning with `--force` will rewrite the full report
- Concept research binaries are gitignored / R2-backed but not needed here — gap-check reads the `.md` extractions in `knowledge/sources/<source>/` and `knowledge/concept_research/<concept>/iter-*/sources/`, both of which are in git

---

## Risk Management

**The actual risks all live in Phase 1's validation, not in the code change. They are:**

- **LLM ignores the new section.** Mitigation: the template guidance explicitly tells the agent these are repo-wide sources to consult; the acceptance check catches this.
- **LLM hallucinates citations from `SOURCE_INDEX.md` without reading the underlying `.md`.** Mitigation: acceptance step 4 spot-checks claimed citations against the actual extracted source files.
- **Unrelated sections drift and `blocking_count` moves for the wrong reason.** Mitigation: full-text diff against baseline; decision gate explicitly allows for prompt narrowing before fleet roll-out.
- **Concept 33 turns out to be a bad test case (e.g. its blockers are not the kind general-pool sources can address).** Mitigation: if Phase 1 outcome is ambiguous, retry on a second concept (candidates: any other D-T MFE tokamak / stellarator with BoP-style blockers) before declaring failure.

---

## Implementation Notes

### Phase 1 baseline capture
**Captured:** 2026-05-22, copied to `/tmp/gap_report_33_baseline.md`
**Baseline `blocking_count`:** 4
**Baseline blocking gaps** (from §5 Missing Parameters table):
1. Plant electrical output (CFEDR/PFPP) — not-yet-sourced
2. Capital cost breakdown (by subsystem) — proprietary / not-yet-sourced
3. O&M costs — not-yet-sourced
4. Capacity factor / availability (power plant) — derivable

### Phase 1 Completion
**Completed:** 2026-05-22

**Actual Changes:**
- `exploration/concept_analysis/scripts/lib/paths.py` — added `SOURCE_INDEX_PATH` constant
- `exploration/concept_analysis/scripts/run_analysis.py` — imported `SOURCE_INDEX_PATH`; in `cmd_gap_check` read `SOURCE_INDEX.md` and pass `source_index_path` + `source_index_content` into the template fill dict
- `exploration/concept_analysis/prompt_templates/gap_check.md` — added "Fleet-Wide TEA / Cost Analog Sources" section between concept-scoped sources and Reference Documents; updated step-2 instruction to mention selective fleet-wide reading; **also mandated the `## Structured summary` YAML block in the Output Format section** (pre-existing template bug — the block was not required, so the regenerated report dropped it; caught and fixed by re-regenerating)
- `exploration/concept_analysis/analyses/33-state-backed-tokamak-best/gap_report.md` — regenerated twice (first run dropped structured block; second run after template fix is the final artifact)

**Acceptance checklist outcome:**
1. ✅ New report cites fleet-wide sources the baseline did not: `knowledge/sources/tea_dt_mfe_cost_analysis/`, `knowledge/sources/aries_cost_account_documentation/` (ARIES-ACT, `osti-1178069.md`), LLNL TBB (`osti-1305833.md`). Heavy integration in §1, §3, §4, §5.
2. ✅ Prior blocking gap downgraded: **O&M cost moved blocking → important** (§5, line 127 — derivable via ARIES-ACT or PROCESS per-kWe scaling). **Capital cost reclassified** from `proprietary / not-yet-sourced` to `not-yet-sourced (but derivable using ARIES-ACT/TEA analogs at ~50% uncertainty)`.
3. ✅ `blocking_count: 4` in `## Structured summary`; parseable by `_structured_blocking_count` in `exploration/scoring_v2/embeddings/rulebook.py:1145`.
4. ⚠️ **One new blocking gap appeared, not attributable to fleet-source content.** "Tritium supply details for BEST D-T operations" upgraded from important (baseline) → blocking (new run), classified `proprietary` and justified as a key O&M driver. This is debatable — BEST is experimental and has no LCOE — and the upgrade is LLM judgment drift, not a result of the SOURCE_INDEX injection (no fleet source introduced this concern). Net `blocking_count` is unchanged at 4 only because one downgrade (O&M) cancelled one upgrade (tritium).
5. ✅ Report reads coherently; no internal contradictions.

**Decision gate: ✅ proceed, with one observation.**
The plumbing works. The LLM did selectively read fleet sources and integrate them in the right places (§5 LCOE Parameters, §3 Subsystem Maturity). Real downgrades occurred and are clearly tied to the new sources. The tritium upgrade is a known risk we flagged in advance (LLM judgment drift on unrelated content under `--force` regeneration), is not caused by the injection itself, and didn't move `blocking_count`. Phase 2 (fleet roll-out) can proceed via a fresh plan; we should accept that per-concept noise of ±1 on `blocking_count` from judgment drift is part of the cost of regeneration and review diffs accordingly.

**Deviations from plan:**
- Discovered that the gap-check template never required the `## Structured summary` block (40/41 prior reports had it by LLM convention, not by spec). First regeneration dropped it, breaking `_structured_blocking_count` parsing. Patched the template to make the block mandatory and regenerated. Net: the template now enforces what was previously a convention — an unplanned but small improvement that should be carried into Phase 2.
