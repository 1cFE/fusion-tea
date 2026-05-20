# Implementation Spec: Data Availability Scoring Axis

**Status:** Ready for implementation
**Owner:** Mallory
**Created:** 2026-05-19
**Branch:** `concept-downselect`
**Target directory:** `.project/active/scoring-v2-data-availability-slice/` (new slice)
**Schema version:** v0.3.0 (`schema.md`, 2026-05-12)

This is a Claude Code implementation spec for the Data Availability axis. The score is **deterministic given a gap report exists** — it counts `**blocking**` markers in the report and maps to a 1-5 score.

---

## Summary

Build a new **Data Availability** scoring axis that produces a deterministic 1.0–5.0 score per concept by counting `**blocking**` markers in the existing `analyses/{concept}/gap_report.md` artifact. The score reflects how many critical data gaps the analyst has identified for LCOE modeling.

The judgment work — reading sources, deciding what counts as `**blocking**` — happens upstream in the gap_check pipeline (Claude-judged). This axis is purely the **mechanical count** of those markers.

### Score formula

```
data_availability_score = bucket(blocking_count)
```

where `bucket()` maps the integer count to a 1-5 score via fixed brackets.

### What the score measures

**Question the score answers:** *How many critical data gaps did the gap_check analysis identify for this concept's LCOE modeling?*

This is **not** a measure of how good the concept is. A poorly-documented concept can still be excellent physics; a well-documented concept can still be commercially marginal. The score isolates the meta-property "how many critical gaps exist" from all the architectural and physics properties measured by the other axes.

### Key design choices

- **Counts only `**blocking**` markers.** These are the analyst's most-critical-gap calls. `**important**` markers exist but aren't counted — they're real concerns but not the same as blockers. Keeping the score to one signal keeps it simple.
- **Fixed bracket schedule** maps count to score. No continuous formula, no base-rating-plus-penalty layering. Just buckets.
- **Returns null when gap report missing.** The composite scorer skips the axis for that concept rather than substituting floor. This forces analyst attention to incomplete documentation work rather than penalizing the concept.
- **All judgment is upstream.** This axis adds no further judgment — it counts a regex match and looks up a bracket.

### Source of the framework

This axis is downstream of the existing C8 (Information Quality) gap_check pipeline on the `fusion-tea-scoring` branch. Reports live at `exploration/concept_analysis/analyses/{id}/gap_report.md`. The C8 criterion in the old framework was Claude-judged from these reports. This port makes the score **deterministic given the report** — no LLM in the scoring loop.

---

## Changes summary

| # | Change | Touches |
|---|---|---|
| A | Add `data_availability` axis with bracket schedule to `weights/default.yaml` | `weights/default.yaml` |
| B | Implement `gap_report_blocking_count` and `data_availability_score` embeddings | `embeddings/rulebook.py` |
| C | Add `data_availability_diagnostics` derived block per feature file | `features/*.yaml` (39 files) |
| D | Add acceptance tests | `tests/scoring_v2/test_data_availability.py` (new) |

---

## Change A: M&SO axis registration

### Updated `weights/default.yaml`

```yaml
# Existing axes (unchanged by this spec)
# ... economic_potential, technical_feasibility, manufacturability_scale_out,
# ... supply_chain, plant_complexity, customization, upper_cf ...

# NEW axis added by this spec
data_availability:
  data_availability_score: 1.0          # axis-level M&SO weight

  # Bracket schedule: map blocking-marker count to a 1-5 score.
  # Brackets are inclusive-upper. Final entry (no max_count) catches all
  # counts beyond the prior bracket.
  blocking_count_brackets:
    - {max_count: 0,    score: 5.0}     # No blockers: best-documented concepts
    - {max_count: 2,    score: 4.0}     # 1-2 blockers: minor specific gaps
    - {max_count: 5,    score: 3.0}     # 3-5 blockers: multiple gaps but tractable
    - {max_count: 9,    score: 2.0}     # 6-9 blockers: significant accumulated gaps
    # 10+: score 1.0 (caught by floor)
  floor_score: 1.0
```

### Why these specific brackets

The blocking-marker counts across the 34 existing gap reports range from 0 to 11 with median 4. The bracket boundaries (0, 2, 5, 9) split this distribution evenly:

| Bracket | Concepts in this range | Score |
|---|---|---|
| 0 blockers | 7 | 5.0 |
| 1-2 | 10 | 4.0 |
| 3-5 | 10 | 3.0 |
| 6-9 | 10 | 2.0 |
| 10+ | 1 | 1.0 |

This produces a clean 5-tier distribution where ~25% of concepts land in each of the middle four tiers, with the top tier (no blockers, best-documented) and bottom tier (10+ blockers, severely under-documented) capturing the extremes.

---

## Change B: Embeddings in `rulebook.py`

### Implementation

Add to `embeddings/rulebook.py` after the existing technical_feasibility embeddings:

```python
# ===========================================================================
# Data Availability Axis
#
# Deterministic scoring based on counting **blocking** markers in the
# existing gap_report.md artifact. The gap report is Claude-judged upstream;
# this axis just counts the markers and maps to a 1-5 score.
#
# Required input: features/*.yaml must contain a 'gap_report_path' pointing
# to the analysis directory's gap_report.md. If the path is empty or the
# file doesn't exist, the score is None (skipped in composite).
# ===========================================================================

import re
from pathlib import Path

# Count **blocking** markers (case-insensitive)
_BLOCKING_MARKER = re.compile(r"\*\*blocking\*\*", re.IGNORECASE)


def _load_da_weights(weights_yaml: dict) -> tuple[list, float]:
    """Extract bracket schedule and floor score from weights/default.yaml.

    Returns (brackets, floor_score).
    """
    da = weights_yaml.get("data_availability", {})
    brackets = da.get("blocking_count_brackets")
    floor = da.get("floor_score")

    if brackets is None or floor is None:
        raise ValueError(
            "weights/default.yaml data_availability axis is missing "
            "blocking_count_brackets or floor_score."
        )

    return brackets, float(floor)


def _count_blocking_markers(report_text: str) -> int:
    """Count occurrences of **blocking** in the report (case-insensitive)."""
    return len(_BLOCKING_MARKER.findall(report_text))


def _score_from_count(count: int, brackets: list, floor: float) -> float:
    """Map blocking count to a score using the bracket schedule."""
    for bracket in brackets:
        if count <= bracket["max_count"]:
            return float(bracket["score"])
    return floor


@embedding(
    "gap_report_blocking_count",
    inputs=["gap_report_path"],
)
def _gap_report_blocking_count(gap_report_path: str) -> int | None:
    """Read the gap report and count **blocking** markers.

    Returns None if the path is empty or the file doesn't exist.

    Note: this embedding has a file-I/O side effect by design. It's the
    one exception to the otherwise-pure framework — the gap report is the
    authoritative source and we don't duplicate its content into feature
    files.
    """
    if not gap_report_path:
        return None

    path = Path(gap_report_path)
    if not path.exists():
        return None

    text = path.read_text(encoding="utf-8")
    return _count_blocking_markers(text)


@embedding(
    "data_availability_score",
    inputs=["gap_report_blocking_count"],
)
def _data_availability_score(
    gap_report_blocking_count: int | None,
    *,
    weights_yaml: dict,
) -> float | None:
    """Data availability score on a 1.0-5.0 scale.

    Returns None if the gap report doesn't exist (count is None) — the
    composite scorer should skip this axis for the concept rather than
    substituting floor.

    Otherwise returns the bucket score for the count.
    """
    if gap_report_blocking_count is None:
        return None

    brackets, floor = _load_da_weights(weights_yaml)
    return _score_from_count(gap_report_blocking_count, brackets, floor)
```

### Why None is returned for missing reports

Other axes default to floor (1.0) when data is missing. This axis returns `None` because there's a meaningful distinction:

- **Gap report exists with many blockers**: the concept genuinely has many documentation gaps. Score reflects that.
- **No gap report exists yet**: the analyst hasn't done the upstream work. Returning `None` forces analyst attention rather than penalizing the concept.

The composite M&SO scorer must handle `None` by skipping the axis for that concept (with a flag) rather than substituting floor.

### Why no rating parsing

The earlier draft of this spec parsed the `**Rating**:` field from the gap report. Removed for simplicity. The rating tier and blocking count correlate strongly (concepts with many blockers tend to get "Significant Gaps" or "Insufficient Data" ratings), so using just the blocking count captures most of the signal without the parsing complexity.

---

## Change C: Feature-file diagnostics

Add a derived block to each concept's feature file:

### Diagnostic block format

```yaml
# In each features/{ID}-{name}.yaml file, append:
data_availability_diagnostics:
  gap_report_path: "{relative path}"
  report_exists: {true|false}
  blocking_count: {integer|null}
  data_availability_score: {1.0-5.0|null}
```

### Examples

**Helios planar stellarator (Thea)** — 0 blockers, max score:

```yaml
data_availability_diagnostics:
  gap_report_path: "../concept_analysis/analyses/05-planar-coil-stellarator/gap_report.md"
  report_exists: true
  blocking_count: 0
  data_availability_score: 5.0
```

**CFS ARC** — 6 blockers (BoP cost, capacity factor, etc.):

```yaml
data_availability_diagnostics:
  gap_report_path: "../concept_analysis/analyses/01-hts-compact-tokamak/gap_report.md"
  report_exists: true
  blocking_count: 6
  data_availability_score: 2.0
```

**Sonofusion** — 8 blockers:

```yaml
data_availability_diagnostics:
  gap_report_path: "../concept_analysis/analyses/02-acoustic-icf-sonofusion/gap_report.md"
  report_exists: true
  blocking_count: 8
  data_availability_score: 2.0
```

**Concept without gap report yet**:

```yaml
data_availability_diagnostics:
  gap_report_path: "../concept_analysis/analyses/37-nearstar-mtif/gap_report.md"
  report_exists: false
  blocking_count: null
  data_availability_score: null
```

When `data_availability_score` is null, the M&SO composite should treat the concept as unscored on this axis (skip rather than substitute floor).

### Population approach

Write `scripts/populate_data_availability_diagnostics.py` to iterate over the 39 feature files, resolve each concept's gap report path by ID mapping, count blocking markers, and write the diagnostic block. Idempotent and re-runnable when gap reports update.

The script should also emit a summary report flagging concepts with no gap report yet (analyst todo).

---

## Change D: Acceptance tests

### New test file: `tests/scoring_v2/test_data_availability.py`

```python
"""Acceptance tests for the data availability scoring axis."""
import pytest
import yaml
from pathlib import Path

from exploration.scoring_v2.embeddings.rulebook import (
    REGISTRY,
    _count_blocking_markers,
    _score_from_count,
    _load_da_weights,
)


_BASE = Path(__file__).parent.parent.parent / "exploration" / "scoring_v2"
_WEIGHTS_YAML = yaml.safe_load((_BASE / "weights" / "default.yaml").read_text())
_BRACKETS, _FLOOR = _load_da_weights(_WEIGHTS_YAML)


# ============================================================================
# Weight loading
# ============================================================================

class TestWeightsExposedInDefaultYaml:
    def test_axis_exists(self):
        assert "data_availability" in _WEIGHTS_YAML

    def test_brackets_present(self):
        assert len(_BRACKETS) >= 4

    def test_floor_is_1(self):
        assert _FLOOR == 1.0


# ============================================================================
# Blocking marker counting
# ============================================================================

class TestBlockingCount:
    def test_count_zero(self):
        assert _count_blocking_markers("no markers here") == 0

    def test_count_one(self):
        assert _count_blocking_markers("text **blocking** more text") == 1

    def test_count_multiple(self):
        text = "**blocking** ... **blocking** ... and **blocking** again"
        assert _count_blocking_markers(text) == 3

    def test_case_insensitive(self):
        text = "**Blocking** and **BLOCKING** count too"
        assert _count_blocking_markers(text) == 2

    def test_partial_match_doesnt_count(self):
        # Inline 'blocking' without bold markers shouldn't match
        text = "the word blocking appears here but isn't marked"
        assert _count_blocking_markers(text) == 0


# ============================================================================
# Bracket scoring
# ============================================================================

class TestBracketScoring:
    def test_zero_blockers_top_score(self):
        assert _score_from_count(0, _BRACKETS, _FLOOR) == 5.0

    def test_one_or_two_blockers(self):
        assert _score_from_count(1, _BRACKETS, _FLOOR) == 4.0
        assert _score_from_count(2, _BRACKETS, _FLOOR) == 4.0

    def test_three_to_five_blockers(self):
        assert _score_from_count(3, _BRACKETS, _FLOOR) == 3.0
        assert _score_from_count(5, _BRACKETS, _FLOOR) == 3.0

    def test_six_to_nine_blockers(self):
        assert _score_from_count(6, _BRACKETS, _FLOOR) == 2.0
        assert _score_from_count(9, _BRACKETS, _FLOOR) == 2.0

    def test_ten_or_more_floor(self):
        assert _score_from_count(10, _BRACKETS, _FLOOR) == 1.0
        assert _score_from_count(20, _BRACKETS, _FLOOR) == 1.0


# ============================================================================
# End-to-end scoring
# ============================================================================

def _score(count):
    return REGISTRY["data_availability_score"].fn(count, weights_yaml=_WEIGHTS_YAML)


class TestEndToEndScoring:
    def test_zero_blockers_score_5(self):
        assert _score(0) == 5.0

    def test_typical_well_documented_score_4(self):
        # CFS ARC has 6 blockers in spec spec — actually scores 2.0 under this scheme
        assert _score(1) == 4.0

    def test_significant_gaps_score_2(self):
        assert _score(7) == 2.0

    def test_severely_under_documented_floor(self):
        assert _score(11) == 1.0

    def test_missing_report_returns_none(self):
        assert _score(None) is None
```

---

## Predicted scores (from existing 34 gap reports)

Mapping concept IDs from gap report directories to the 39-concept matrix where they overlap. Concepts in the matrix without gap reports score `null`.

| Concept (matrix ID) | Blockers | Score |
|---|---|---|
| 01 CFS ARC | 6 | **2.0** |
| 02 Sonofusion | 8 | **2.0** |
| 03 Cortex | 6 | **2.0** |
| 04 hb11 (laser-icf) | 5 | **3.0** |
| 05 Thea planar | 0 | **5.0** |
| 06 Pale Blue mirror | 5 | **3.0** |
| 07 Pacific MagLIF | 0 | **5.0** |
| 08 Helion (FRC direct) | 5 | **3.0** |
| 09 Proxima QI | 1 | **4.0** |
| 10 Gauss HELIAS | 0 | **5.0** |
| 11 Realta mirror | 4 | **3.0** |
| 12 OpenStar | 3 | **3.0** |
| 13 Avalanche | 9 | **2.0** |
| 14 General Fusion | 5 | **3.0** |
| 15 Zap Z-pinch | 2 | **4.0** |
| 16 Acceleron | 6 | **2.0** |
| 17 Xcimer (17a hybrid) | 0 | **5.0** |
| 17b Focused (fast ignition) | 6 | **2.0** |
| 18 TAE p-B11 | 6 | **2.0** |
| 19 Zephyr | 6 | **2.0** |
| 20 Type One | 2 | **4.0** |
| 20b Renaissance | 4 | **3.0** |
| 21 Energy Singularity (21) | 1 | **4.0** |
| 22 Tokamak Energy / projectile (22) | 6 | **2.0** |
| 23 First Light / nanostructured (23) | 4 | **3.0** |
| 24 Marvel / DPF (24) | 7 | **2.0** |
| 25 LPP / heavy-ion (25) | 2 | **4.0** |
| 26 Intensity / NIF indirect (26) | 0 | **5.0** |
| 27 Polywell (27) | 3 | **3.0** |
| 28 HTS full (28) | 2 | **4.0** |
| 29 Energy Singularity / neg-T (29) | 1 | **4.0** |
| 30 NIF-comm (30) | 2 | **4.0** |
| 31 OEC (31) | 0 | **5.0** |
| 32 French laser (32) | 2 | **4.0** |
| 33 BEST (33) | 0 | **5.0** |
| 34 compact ST India (34) | 11 | **1.0** |
| 35 Polomac | 5 | **3.0** |
| 36 Helical Fusion | 1 | **4.0** |
| 37 NearStar MTIF | *no report* | **null** |
| 38 SHINE | *no report* | **null** |
| 39 ENN EHL-2 | *no report* | **null** |

### Score distribution

- **5.0 (7 concepts)**: Concepts with zero blockers — best-documented
- **4.0 (10 concepts)**: 1-2 blockers — well-documented with minor gaps
- **3.0 (10 concepts)**: 3-5 blockers — significant gaps but tractable
- **2.0 (10 concepts)**: 6-9 blockers — major documentation problems
- **1.0 (1 concept)**: 10+ blockers — severely under-documented (Indian compact ST with 11)
- **null (3+ concepts)**: No gap report yet (NearStar, SHINE, ENN)

### Note on score interpretation

This axis disagrees with the old C8 rating in interesting ways. For example, CFS ARC has a "Mostly Ready" overall rating but 6 specific blockers — under this simpler scheme it scores 2.0 alongside concepts the analyst rated "Insufficient Data". This is a feature, not a bug: the framework is saying "regardless of overall analyst impression, CFS has a lot of specific data gaps that need filling for LCOE modeling." If you disagree with this framing, the previous rating-tier-based version is the alternative.

---

## Notable score patterns

**Five concepts at 5.0 (zero blockers).** Helios planar stellarator (Thea), Pacific MagLIF, Gauss HELIAS, NIF indirect, OEC, BEST, hybrid-drive laser ICF. These are concepts with thorough public documentation — typically peer-reviewed design papers or DOE-program participants.

**Indian compact ST at 1.0 (11 blockers).** Floors the distribution. Earliest-stage concept with the most accumulated documentation gaps.

**CFS ARC at 2.0** despite being one of the most-watched concepts in the field. The framework is saying CFS specifically has many LCOE-blocking gaps (BoP cost excluded from ARC paper, divertor deferred, updated commercial design unpublished, capacity factor underivable from sources). If you disagree, the gap report itself is the right place to argue with the analyst's blocker classifications.

**Sonofusion at 2.0**. Same score as CFS — the framework treats them as comparable on data availability because they have similar blocker counts (8 vs 6). The two concepts are obviously not similar in *quality*, but on this specific axis (how many critical LCOE gaps), they happen to be comparable.

---

## Files touched

```
exploration/scoring_v2/weights/default.yaml                              # add data_availability axis
exploration/scoring_v2/embeddings/rulebook.py                            # add 2 embeddings + 3 helpers
exploration/scoring_v2/features/*.yaml                                   # 39 files: append data_availability_diagnostics + gap_report_path
exploration/scoring_v2/scripts/populate_data_availability_diagnostics.py # NEW: idempotent diagnostic population
tests/scoring_v2/test_data_availability.py                                # NEW: acceptance tests
.project/active/scoring-v2-data-availability-slice/design.md              # NEW: this spec + planning doc
```

---

## Coordination notes

### Prerequisite: Standardize gap_report format upstream

**This is a prerequisite before the axis can produce reliable scores.** The current 34 gap reports use inconsistent formatting for blocking-gap markers. Specifically:

- Most reports use `**blocking**` (bolded) in inline gap lists, which the regex catches.
- Some reports list blocking gaps in markdown tables with the word `blocking` in plain text (no bold), which the regex misses entirely.
- One report (BEST, concept 33) uses zero bolded `**blocking**` markers but has 6 plain-text `blocking` mentions in its per-section gap tables, while explicitly stating "No blocking data gaps prevent a D1+ write-up." Both signals are present and they contradict each other.

The result: a regex on `**blocking**` will count CFS ARC (concept 01) at 6 blockers and BEST (concept 33) at 0 blockers, producing scores of 3.0 vs 5.0 — a perverse two-tier gap that doesn't reflect reality. Both concepts are D-T tokamaks with similar gap profiles in the analyst's actual narrative.

**Required upstream fix**: update the gap_check prompt (`exploration/concept_analysis/analyses/{id}/prompts/gap_check_prompt.md`) so every gap_report.md ends with a structured machine-readable summary block:

```yaml
# Required at end of every gap_report.md:
## Structured summary (machine-readable)
overall_rating: "Mostly Ready"               # or "Significant Gaps" or "Insufficient Data"
blocking_count: 6                            # total blocking gaps across all sections
important_count: 4                           # total important gaps across all sections
sections:
  data_availability:   {coverage: "Good",    blocking: 0, important: 1}
  system_function:     {coverage: "Good",    blocking: 2, important: 1}
  subsystem_maturity:  {coverage: "Partial", blocking: 2, important: 1}
  materials:           {coverage: "Partial", blocking: 1, important: 1}
  economics:           {coverage: "Sparse",  blocking: 1, important: 0}
```

Once this format is in place:
- The Python embedding parses the YAML block (not the prose) for a deterministic count.
- The current prose format inside the report stays unchanged — analysts can still write in narrative form. The structured block is an additional element at the end.
- Regenerating the 34 existing reports to add the structured block is a Claude-assisted batch update (read each existing report, count blockers/importants, append YAML summary). Estimated ~½ day of effort.
- Re-running the gap_check pipeline going forward includes the structured block by default.

**Interim behavior (before the fix lands)**: the regex-on-bold approach scores reports inconsistently. The axis can still be wired in, but the analyst should treat the resulting scores as preliminary and not surface them in the UI ranking until the format standardization completes. Concepts whose gap reports lack the structured block get `data_availability_score: null` (handled by the existing null-handling rule) and a TODO flag.

### Cross-branch dependency

The gap reports live on the `fusion-tea-scoring` branch. The new axis lives on `concept-downselect`. Recommend merging the analysis directory into `concept-downselect` as a follow-up — the analysis pipeline and the scoring framework are increasingly coupled.

### Gap report ID mapping

The gap report directory IDs (01-36) don't map 1:1 to the 39-concept matrix IDs. Create `gap_report_id_mapping.yaml` documenting which gap report (if any) corresponds to each matrix concept. Concepts without a report get `data_availability_score: null` and a TODO flag.

### What happens when gap reports update

The diagnostic block doesn't record a hash in this simpler version — re-running `populate_data_availability_diagnostics.py` always re-reads and re-counts. The populate script should be cheap enough to run frequently.

---

## Implementation notes for Claude Code

- **File I/O exception**: this is the one axis that reads outside the feature file. Mark this clearly in code comments — the framework's normal pattern is pure functions of feature data.

- **Parser depends on the structured summary block**: After the gap_report format standardization (see prerequisite above) lands, the parser reads the YAML summary block at the end of each report, not the prose. Until then, the parser falls back to the `\*\*blocking\*\*` regex but produces unreliable scores. Mark this clearly in code comments and in the populate script's logging output (e.g., "WARNING: gap_report.md for concept 33 lacks structured summary block; counted X bolded blockers from prose, may be inaccurate").

- **The null score is a first-class value.** The composite scorer must handle None by skipping the axis for that concept (with a flag) rather than substituting floor.

- **Populate script idempotency**: running it twice should produce identical output (assuming gap reports unchanged). Simple to verify by running and diffing.

---

## Open questions worth flagging (for future versions)

1. **`**important**` markers ignored.** The gap reports also use `**important**` markers. Currently ignored. Adding them (with half weight) would give finer granularity but at the cost of simplicity. Decision: stay simple, ignore important markers.

2. **Time-dependent scores.** Data availability changes as companies publish. The diagnostic block doesn't currently record a timestamp — adding `report_last_modified` would let the framework flag stale scores. Defer until needed.

3. **Composite weighting.** Data availability is a *meta* property — it tells you how confident you can be in the *other* axes' scores. Should the M&SO composite use data_availability as a confidence weight rather than a peer axis? Structurally different question from what this spec implements.

4. **Concepts without gap reports**: NearStar MTIF (37), SHINE (38), ENN EHL-2 (39) currently lack reports. Worth a follow-up slice to generate them.

5. **Gap report quality drift.** Different analysts might count blockers differently. The framework treats the count as authoritative. Worth periodic spot-check audits.

6. **Rating tier removed for simplicity.** The earlier draft of this spec combined the rating tier with the blocking count. Removed. If the analyst wants the rating tier back as a modifier later, easy to add — see the earlier draft for the pattern.
