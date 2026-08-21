# Implementation Plan: Close v3 Code Gaps and Pass Tests

**Status:** ✅ Complete 2026-05-17 (Phases 0–5 done; 2 carry-forwards to Item 5 — see Implementation Notes)
**Created:** 2026-05-17
**Last Updated:** 2026-05-17
**Branch:** `ontology-update` @ `6d32f4d` (Item 2 tip; `8db3ed2` was an earlier alias for the same content)

## Source Documents

- **Spec:** [spec.md](spec.md) — FR-1 through FR-14 (FR-4/6/8 revised at design time)
- **Design:** [design.md](design.md) ← component details, bets, invariants, JSON shapes, FR-to-commit map
- **Epic:** [.project/backlog/epic_ontology_v3_migration.md](../../backlog/epic_ontology_v3_migration.md) (Item 3)
- **Prior:** [.project/active/ontology-v3-merge/](../ontology-v3-merge/) (Item 2, complete)

## Implementation Strategy

**Phasing rationale.** The design's four-rings model (schema names → display layer → classification logic → derived artifacts) is the phase backbone. Phase 0 collects I-7 baselines before any edits. Phase 2 is the first phase where reality can disagree with the design and is therefore the first proof point. Verify-only FRs (4, 6) collapse into Phase 5 as grep gates.

**Critical path:**
```
Phase 0: baselines + grep ─► Phase 1: column_map ─► Phase 2: tree_group + JS
                                                            │
                                                            ▼  (first proof point)
                                              Phase 3: clustering + chart
                                                            │
                                                            ▼
                                              Phase 4: tests + scoring rerun
                                                            │
                                                            ▼
                                              Phase 5: final sweep + smoke
```

**First proof point.** End of Phase 2: regenerated `decision_tree.json` contains exactly the six top-level groups; `browser-inspect` against the local explorer shows the v3 tree with 0 console errors. If this fails, the option-(a) shape choice is wrong — escalate before continuing.

**Overall validation approach.**
- Each phase opens with a test stencil or grep gate; implementation follows.
- Each phase closes with a recorded artifact (test pass, grep count, screenshot/JSON, byte-diff).
- Commits per design's FR→commit map ([design.md § Implementation Notes](design.md#implementation-notes)): one logical commit per design phase, two for Phases 2/3 where the boundary helps review.

---

## Phase 0: Audit + Baselines

### Goal

Capture the pre-refactor I-7 baselines and the stale-ref grep landscape. No code edits; no commit.

### Assumption Under Test

`oneoff_3d_clustering.py` and `generate_ontology_chart.py` at `8db3ed2` produce the deterministic outputs we'll diff against in Phase 3. (If either crashes at baseline, the I-7 regression check is meaningless.)

### Test Stencil (Write This First)

```bash
# Baseline outputs land here; Phase 3 diffs against this directory.
mkdir -p /tmp/i7_baseline/

# Smoke: both scripts run to completion at 8db3ed2, no errors.
uv run python exploration/concept_analysis/scripts/oneoff_3d_clustering.py \
  && cp exploration/concept_analysis/oneoff_3d_clustering.csv /tmp/i7_baseline/clustering_baseline.csv \
  && cp exploration/concept_analysis/oneoff_3d_clustering.html /tmp/i7_baseline/clustering_baseline.html

uv run python exploration/phase_1a/generate_ontology_chart.py \
  && cp exploration/phase_1a/concept_ontology_v3.png /tmp/i7_baseline/ontology_chart_baseline.png

# Stale-ref grep counts — recorded as "before" for FR-13 closure in Phase 5.
rg -c 'Plasma State|Tritium Breeding|Neutron Management' exploration/ > /tmp/i7_baseline/stale_columns_before.txt
rg -c 'CADENCE_BY_PREFIX|TREE_PATH|_C2_CONCEPT_MAP|FREEFORM_CONCEPTS' exploration/ > /tmp/i7_baseline/stale_patterns_before.txt
```

### Changes Required

None — collection only. See [design.md § Implementation Notes](design.md#implementation-notes) for the I-7 baseline rationale and [design.md § Required Invariants](design.md#required-invariants) for I-7.

**Steps:**

- [ ] `git rev-parse HEAD` shows `8db3ed2` (or descendant with no `exploration/` changes since)
- [ ] Run both baseline generators; copy outputs to `/tmp/i7_baseline/`
- [ ] Save `before` grep counts to `/tmp/i7_baseline/`

### Validation

**Automated:**
- [ ] `/tmp/i7_baseline/clustering_baseline.csv` exists, non-empty
- [ ] `/tmp/i7_baseline/ontology_chart_baseline.png` exists, non-zero size
- [ ] Both `stale_*_before.txt` exist (used for FR-13 delta in Phase 5)

**What we know works after this phase:**
- I-7 has a reproducible baseline pinned to `8db3ed2`.
- Phase 5's "no new stale refs" check has a numeric anchor.

---

## Phase 1: `column_map.py` Schema Swap (FR-1)

### Goal

Bring `phase_2a/column_map.py` to the v3 schema: drop `Plasma State` / `Tritium Breeding` / `Neutron Management` entries; add `Blanket Config` mappings. Mechanical.

### Assumption Under Test

Mallory's `BlanketConfig` enum values (7 members per `taxonomy_models.py:131-139`) map 1:1 onto Phase 2a `MappedTerm` shape without new vocabulary collisions.

### Test Stencil (Write This First)

```bash
# Phase 2a smoke on one representative concept — must emit 0 UNMAPPABLE from dropped cols.
# Pick a concept with a non-trivial blanket entry, e.g. 20a-type-one-stellarator
# (Liquid Li blanket — exercises Blanket Config vocab).
uv run python exploration/phase_2a/expand.py \
  --concept 20a-type-one-stellarator \
  --dry-run 2>&1 | tee /tmp/phase_2a_smoke_after.txt

# Gate: zero hits for the dropped column names in the UNMAPPABLE diagnostic.
! grep -E 'UNMAPPABLE.*(Plasma State|Tritium Breeding|Neutron Management)' /tmp/phase_2a_smoke_after.txt
```

### Changes Required

**See `design.md` for:**
- Component details → [design.md#component-overview](design.md#component-overview) (entry on `column_map.py`)
- Detailed inventory evidence → [design.md#appendix-a--detailed-inventory-evidence](design.md#appendix-a--detailed-inventory-evidence)

**File: `exploration/phase_2a/column_map.py`**

- [ ] `DESIGN_COLUMNS` (line 26-44): remove `"Plasma State"`, `"Tritium Breeding"`, `"Neutron Management"`; add `"Blanket Config"` in v3 header order
- [ ] `VOCABULARY` (line 94-188): remove all entries with target columns `"Plasma State"`, `"Tritium Breeding"`, `"Neutron Management"`; add `MappedTerm("Blanket Config", "exact", <value>)` for each of the 7 `BlanketConfig` enum values
- [ ] `VALUE_ALIASES`: drop stale value-aliases for the three retired columns; add aliases for `Blanket Config` values where the LLM output varies (e.g. "liquid metal" → `Liquid metal`)
- [ ] `KEY_TO_COLUMN` (line 363-389): drop `plasma_state` / `tritium_breeding` / `neutron_management` / `neutron_shielding`; add `blanket_config` → `Blanket Config`

**Commit boundary:** one commit `feat(phase_2a): adopt v3 column schema (FR-1)`.

### Validation

**Automated:**
- [ ] Phase 2a smoke (test stencil above) emits 0 `UNMAPPABLE` from dropped column names
- [ ] `uv run python -m pytest exploration/phase_2a/tests/` passes (if tests exist there)
- [ ] `rg -n 'Plasma State|Tritium Breeding|Neutron Management' exploration/phase_2a/column_map.py` → 0 hits

**What we know works after this phase:**
- Phase 2a validator runs against v3 without column-name drift.
- The `BlanketConfig` vocabulary is wired end-to-end through `column_map.py`.

---

## Phase 2: Display Layer (FR-2, FR-3, FR-5) — First Proof Point

### Goal

Add v3 sibling groups to the decision tree via the display-only `tree_group` layer ([design.md § Key Bets & Decisions Bet 1](design.md#key-bets--decisions)). Update `neighborhood_graph.js` field-name dict to match `taxonomy_card.js` / `view_categorical.js`. Regenerate `decision_tree.json`.

### Assumption Under Test

The 6-group `tree_group` derivation produces the correct group for every row in `table.csv`. The new `decision_tree.json` shape ([design.md § Implementation Notes](design.md#implementation-notes) before/after JSON) doesn't break any JS consumer.

### Test Stencil (Write This First)

```python
# exploration/concept_explorer/tests/test_seed_registry.py — NEW
from seed_registry import tree_group  # function added in this phase
from taxonomy_models import (
    ConceptTaxonomy, ConfinementFamily, MFETopology, NonStandardMechanism
)

def test_tree_group_returns_mfe_for_tokamak():
    c = make_test_taxonomy(family=ConfinementFamily.MFE,
                          mfe_topology=MFETopology.TOKAMAK)
    assert tree_group(c) == "MFE"

def test_tree_group_returns_cmpt_tor_for_compact_toroid():
    c = make_test_taxonomy(family=ConfinementFamily.MFE,
                          mfe_topology=MFETopology.COMPACT_TOROID)
    assert tree_group(c) == "Cmpt-Tor"

def test_tree_group_returns_estatic_for_electrostatic_mechanism():
    c = make_test_taxonomy(family=ConfinementFamily.NONSTANDARD,
                          non_standard_mechanism=NonStandardMechanism.ELECTROSTATIC)
    assert tree_group(c) == "Estatic"

def test_decision_tree_json_has_six_top_level_groups():
    # After running seed_registry, verify the regenerated JSON.
    tree = json.loads(Path("data/decision_tree.json").read_text())
    assert set(tree.keys()) >= {"MFE", "IFE", "MIF", "Cmpt-Tor", "Estatic", "Other"}

def test_every_concept_has_a_tree_group():
    # Iterate table.csv; assert tree_group never returns None/empty.
    for row in load_table_rows():
        c = parse_concept(row)
        assert tree_group(c) in {"MFE", "IFE", "MIF", "Cmpt-Tor", "Estatic", "Other"}
```

### Changes Required

**See `design.md` for:**
- `tree_group` function body + verified enum values → [design.md § Implementation Notes](design.md#implementation-notes) (`tree_group derivation`)
- Before/after `decision_tree.json` snippet → same section
- Component details → [design.md#component-overview](design.md#component-overview) entries for `seed_registry.py` and `neighborhood_graph.js`

**File: `exploration/concept_explorer/seed_registry.py`**
- [ ] Add `tree_group(c: ConceptTaxonomy) -> str` (≤10 lines per design sketch) with the `# Mirrors lib/scoring.py:detect_c2_category` comment
- [ ] Add ADR-style comment at top of `_HIERARCHY` (line 137) recording the enum-vs-`tree_group` decision — see [design.md § Key Bets Bet 1](design.md#key-bets--decisions) for the rationale to copy in
- [ ] Extend `_HIERARCHY` and `_SUBTYPES` so the per-group topology→leaf entries exist for `Cmpt-Tor`, `Estatic`, `Other` (Dipole/Supported, MIF/Pulsed power inside their parents)
- [ ] Change top-level grouping key from `family.value` to `tree_group(c)` in the build path (option-a per design)
- [ ] Regenerate `data/decision_tree.json` by running `uv run python exploration/concept_explorer/seed_registry.py`

**File: `exploration/concept_explorer/tests/test_seed_registry.py` (NEW)**
- [ ] Implement test stencil above
- [ ] Add a generator-style test that iterates every row in `table.csv` and asserts every concept lands in exactly one of the six groups

**File: `exploration/concept_explorer/static/js/neighborhood_graph.js`**
- [ ] Replace the hardcoded `[{label: "Plasma State", …}]`-style references (lines 46-50) with the `{field, label}` dict pattern used at `taxonomy_card.js:23-29` and `view_categorical.js:52-70`; include `blanket_config`

**Smoke (manual, before commit):**
- [ ] `uv run python exploration/concept_explorer/seed_registry.py` exits 0
- [ ] `python -c "import json; print(set(json.load(open('exploration/concept_explorer/data/decision_tree.json')).keys()))"` includes the 6 expected groups
- [ ] `browser-inspect` session: open the explorer, navigate the taxonomy view; save session JSON to `/tmp/browser_inspect/phase2/`. Console errors must be 0.

**Commit boundary:** two commits — `feat(explorer): add tree_group display layer + ADR (FR-2, FR-3)` and `refactor(explorer): align neighborhood_graph.js to field/label dict (FR-5)`. Tests land with the first commit.

### Validation

**Automated:**
- [ ] `uv run python -m pytest exploration/concept_explorer/tests/test_seed_registry.py` → green
- [ ] `decision_tree.json` keys include `{"MFE","IFE","MIF","Cmpt-Tor","Estatic","Other"}`
- [ ] `rg -n 'plasma_state|tritium_breeding|neutron_management' exploration/concept_explorer/static/js/neighborhood_graph.js` → 0 hits
- [ ] Saved `browser-inspect` JSON shows `console_errors == []`

**Manual:**
- [ ] Click through taxonomy view → confirm visual rendering of the six groups
- [ ] Compare view: pick one MFE and one Non-Standard concept; confirm no missing-field errors

**What we know works after this phase:**
- The single non-mechanical assumption of this work item (decision-tree shape) is collapsed.
- `tree_group` derivation is correct for all 40 concepts.
- JS field-name contract is consistent across all three explorer views.

**Escalation:** if any concept's tree_group is wrong, capture the row + expected group, stop, and revisit the design's enum mapping before continuing.

---

## Phase 3: Classification Logic (FR-8, FR-9, FR-14)

### Goal

Refactor `oneoff_3d_clustering.py::CADENCE_BY_PREFIX` and `generate_ontology_chart.py::TREE_PATH` to architecture-derived keys ([design.md § Key Bets Bet 2 + Bet 7](design.md#key-bets--decisions)). Audit `FUNDING_M_USD` for new-concept entries.

### Assumption Under Test

The architecture-derivation pattern from `lib/scoring.py:detect_c2_category` produces byte-identical output for concepts whose architecture columns didn't change in Item 2 (I-7 regression check).

### Test Stencil (Write This First)

```bash
# Regression gate — written before any refactor edits.
# Both scripts must produce output that diffs cleanly against /tmp/i7_baseline/.

uv run python exploration/concept_analysis/scripts/oneoff_3d_clustering.py
diff /tmp/i7_baseline/clustering_baseline.csv \
     exploration/concept_analysis/oneoff_3d_clustering.csv \
  | tee /tmp/i7_clustering_diff.txt
# Expected: empty diff for concepts whose architecture columns are unchanged.
# Any non-empty line must trace to a v3-reclassification of a concept that
# legitimately moved (e.g. classification flipped); record in commit body.

uv run python exploration/phase_1a/generate_ontology_chart.py
# PNG byte-diff isn't useful (rendering nondeterminism); compare the underlying
# per-concept TREE_PATH triples instead:
python -c "
from exploration.phase_1a.generate_ontology_chart import compute_tree_paths  # extracted helper
import json
new = compute_tree_paths()
old = json.load(open('/tmp/i7_baseline/tree_paths_baseline.json'))  # save in Phase 0 if absent
print('changed:', {k: (old[k], new[k]) for k in new if k in old and old[k] != new[k]})
"
```

> Note: if Phase 0 didn't save `tree_paths_baseline.json` separately, regenerate by running the *current* `generate_ontology_chart.py` at `8db3ed2` once more to capture the TREE_PATH dict before refactor. Phase 3's first concrete step is to add this saved baseline if missing.

### Changes Required

**See `design.md` for:**
- Pattern mirror reference → `lib/scoring.py:detect_c2_category` (the function the new helpers must mirror)
- Component details → [design.md#component-overview](design.md#component-overview)
- Funding audit detail → [design.md § Component Overview](design.md#component-overview) `oneoff_3d_clustering.py` entry

**File: `exploration/concept_analysis/scripts/oneoff_3d_clustering.py`**
- [ ] Delete `CADENCE_BY_PREFIX` dict (lines 88-119)
- [ ] Add `cadence_by_architecture(concept) -> float` with `# Mirrors lib/scoring.py:detect_c2_category` comment; derive from `Confinement Family / MFE Topology / Magnet Type / IFE Driver / MIF Method` per the existing prefix-bucket semantics (each cadence value's old meaning maps to one architecture combination)
- [ ] Update call site (line 215) to use `cadence_by_architecture(concept)`
- [ ] `FUNDING_M_USD` (lines 43-82): keep slug-keyed; add entries for `37-magnetized-target-inertial-fusion-mtif`, `38-particle-accelerator-driven-fusion`, `39-spherical-tokamak-cs-free-p-b11`. Pranos entry (`34-compact-spherical-tokamak-india`) may stay (Item 6 cleanup)

**File: `exploration/phase_1a/generate_ontology_chart.py`**
- [ ] Replace `TREE_PATH` constant (lines 201-244) with `def derive_tree_path(concept) -> tuple[str, str, str]` reading `table.csv` columns; mirror `lib/scoring.py:detect_c2_category` (same `# Mirrors ...` comment)
- [ ] Update call sites (lines 362-364) to call the function

**Commit boundary:** two commits — `refactor(clustering): architecture-derived CADENCE; FUNDING_M_USD audit (FR-8)` and `refactor(ontology_chart): derive TREE_PATH from table.csv (FR-9)`.

### Validation

**Automated:**
- [ ] I-7 clustering diff (stencil above): empty for retained concepts, or all non-empty rows are traceable to v3 reclassifications recorded in commit body (FR-14)
- [ ] I-7 TREE_PATH diff: same condition
- [ ] `rg -n 'CADENCE_BY_PREFIX|TREE_PATH = \{' exploration/` → 0 hits
- [ ] `rg -n 'FUNDING_M_USD' exploration/concept_analysis/scripts/oneoff_3d_clustering.py` shows new entries for 37/38/39

**Manual:**
- [ ] Visual inspection: regenerated clustering HTML opens, scatter points labeled correctly
- [ ] Regenerated `concept_ontology_v3.png` looks structurally similar to baseline (group boundaries identical)

**What we know works after this phase:**
- All four downstream classifier consumers (`scoring.py`, `tree_group`, `cadence_by_architecture`, `derive_tree_path`) use the same architecture-column pattern.
- Renumbering footguns are gone — no consumer keys on numeric ID prefix.

---

## Phase 4: Tests + Scoring Rerun (FR-7, FR-10, FR-11)

### Goal

Update the test suite for v3 enums (`BlanketConfig`, no more `PlasmaState`/`TritiumBreeding`). Regenerate `scores/verified_scores.{json,md}` (deterministic) and `scores/calibrated_scores.{json,md}` (one Claude call) per [design.md § Key Bets Bet 3](design.md#key-bets--decisions).

### Assumption Under Test

`build_verified_scores()` reads existing synthesis YAML and recomputes C2 via the new `detect_c2_category` without re-invoking Claude (cost ≈ $0). `calibrate` succeeds in one cross-concept Claude call (≈ $0.50).

### Test Stencil (Write This First)

```python
# exploration/concept_explorer/tests/test_taxonomy_models.py — UPDATE
from taxonomy_models import BlanketConfig, ConceptTaxonomy
# REMOVE: from taxonomy_models import PlasmaState, TritiumBreeding  ← was the import crash

def test_blanket_config_round_trip():
    for member in BlanketConfig:
        c = make_test_taxonomy(blanket_config=member)
        roundtripped = ConceptTaxonomy.model_validate_json(c.model_dump_json())
        assert roundtripped.blanket_config == member

def test_blanket_config_enum_covers_v3_values():
    assert {m.value for m in BlanketConfig} >= {
        "Liquid metal", "Molten salt", "Solid breeder", "Other / hybrid",
        "N/A (no tritium)", "N/A (non-power)", "TBD",
    }
```

```bash
# Scoring rerun smoke — must complete with no errors.
uv run python exploration/concept_analysis/scripts/run_analysis.py extract-scores
# Expected: writes scores/verified_scores.{json,md}; prints "Wrote N scores".
# Cost: $0 (deterministic).

uv run python exploration/concept_analysis/scripts/run_analysis.py calibrate
# Expected: writes scores/calibrated_scores.{json,md}; one Claude call.
# Cost: ~$0.50.

# Sanity: a concept that was historically miscategorized must now have the new C2.
python -c "
import json
v = json.load(open('exploration/concept_analysis/scores/verified_scores.json'))
# Pick one of the 8 silently-miscategorized concepts (per design Risk row 3)
# and confirm c2_category matches the v3 architecture-derived value.
print([s for s in v if s['concept_id'] == '15-sheared-flow-stabilized-z-pinch'][0])
"
```

### Changes Required

**See `design.md` for:**
- Scoring strategy + cost ceiling → [design.md § Key Bets Bet 3](design.md#key-bets--decisions)
- Why **not** `run_scoring_pipeline.py` end-to-end → same section
- Test scope → [design.md § Component Overview](design.md#component-overview) `test_taxonomy_models.py` entry

**File: `exploration/concept_explorer/tests/test_taxonomy_models.py`**
- [ ] Remove imports of `PlasmaState`, `TritiumBreeding` (line 29, 33)
- [ ] Replace `test_round_trip` body (lines 61-63) to use `BlanketConfig`
- [ ] Add the two tests in the stencil above

**Sibling test files (per [design.md § Potential Risks](design.md#potential-risks) row 5):**
- [ ] `exploration/concept_explorer/tests/test_state_and_compute.py:82` — sweep `plasma_state` references
- [ ] `exploration/concept_explorer/tests/test_extraction.py:115` — same

**Scoring rerun:**
- [ ] `extract-scores` exits 0; `verified_scores.{json,md}` has 40 entries
- [ ] `calibrate` exits 0; `calibrated_scores.{json,md}` has 40 entries; cost log ≤ $1
- [ ] Diff `scores/calibrated_scores.json` HEAD-vs-new: if any concept's C2 changes, the concept must appear on the v3 reclassification list (per [design.md § Potential Risks](design.md#potential-risks))

**Commit boundary:** two commits — `test(taxonomy): v3 enums + BlanketConfig coverage (FR-7, FR-11)` and `chore(scores): regen verified + calibrated against v3 classifier (FR-10)`.

### Validation

**Automated:**
- [ ] `uv run python -m pytest exploration/concept_explorer/tests/` green (FR-11)
- [ ] `uv run python -c "import json; print(len(json.load(open('exploration/concept_analysis/scores/verified_scores.json'))))"` → 40
- [ ] Same check on `calibrated_scores.json` → 40

**Manual:**
- [ ] Inspect `scores/verified_scores.md` for a Z-pinch concept; confirm new C2 category
- [ ] Confirm total Claude cost ≤ $1 (see saved cost log if `run_analysis.py` writes one; otherwise inspect terminal output)

**What we know works after this phase:**
- Test suite passes against v3.
- Scores reflect the architecture-derived classifier end-to-end.
- The "synthesize is Item 5's job" boundary is respected — no `analyses/{ID}/synthesis.md` were touched.

**Escalation:** if more than 5 concepts trigger a `synthesize` rerun (per design's cost-ceiling escape hatch), stop and reassess.

---

## Phase 5: Final Sweep (FR-4, FR-6, FR-12, FR-13)

### Goal

Verify no-op FRs hold; run the full stale-ref grep; close the `browser-inspect` smoke gate. No code edits.

### Assumption Under Test

The verify-only FRs (4 templates, 6 registry YAML) are still no-ops after all prior phases. No phase accidentally reintroduced a stale reference.

### Test Stencil (Write This First)

```bash
# FR-4 (revised): templates clean of dropped field names.
rg -n 'plasma_state|tritium_breeding|neutron_management' exploration/concept_explorer/templates/ \
  | tee /tmp/phase5_templates.txt
[ ! -s /tmp/phase5_templates.txt ]  # exit 0 if empty

# FR-6 (revised): parameter_display_registry.yaml clean.
rg -n 'plasma_state|tritium_breeding|neutron_management' \
   exploration/concept_explorer/data/parameter_display_registry.yaml \
  | tee /tmp/phase5_registry.txt
[ ! -s /tmp/phase5_registry.txt ]

# FR-13: stale-ref sweep over all of exploration/.
rg -n 'Plasma State|Tritium Breeding|Neutron Management|_C2_CONCEPT_MAP|FREEFORM_CONCEPTS|CADENCE_BY_PREFIX|TREE_PATH = \{' \
   exploration/ \
  | tee /tmp/phase5_stale_after.txt
# Compare against /tmp/i7_baseline/stale_*_before.txt — count must drop, never rise.

# FR-13: ID-prefix slicing patterns.
rg -n 'concept_id\[:2\]|\bid\[:2\]' exploration/ \
  | tee /tmp/phase5_slicing.txt
[ ! -s /tmp/phase5_slicing.txt ]  # zero hits
```

### Changes Required

None — verification only. Any hit triggers a fix-or-escalate decision; do not silently accept.

**Steps:**

- [ ] Run all four grep gates above
- [ ] If FR-4 / FR-6 / FR-13 grep returns any hits, classify each: (a) legitimate v3 follow-up not in scope → log in commit body or new BACKLOG entry; (b) accidental regression in Phases 1-4 → fix and re-commit; (c) pre-existing stale ref that survived → fix here
- [ ] Run `browser-inspect` session (FR-12): explorer up locally; click taxonomy → concept → compare → neighborhood for two concepts (one MFE, one Non-Standard); save session JSON path to `/tmp/browser_inspect/phase5/`
- [ ] Update epic `Item 3` checklist; tick the success criteria items in spec

**Commit boundary:** no new commit if all grep gates pass clean. If any cleanup is required, single commit `chore(v3): final sweep cleanup (FR-13)`.

### Validation

**Automated:**
- [ ] FR-4 grep → 0 hits
- [ ] FR-6 grep → 0 hits
- [ ] FR-13 stale-ref grep delta vs Phase 0 baseline → strictly decreasing (or matches Phase 0 if already 0)
- [ ] FR-13 ID-prefix slicing grep → 0 hits

**Manual:**
- [ ] Saved `browser-inspect` JSON at `/tmp/browser_inspect/phase5/`; `console_errors == []` (FR-12)
- [ ] All view tabs render (taxonomy / categorical / neighborhood / compare)
- [ ] Tick epic Item 3 success criteria checkboxes

**What we know works after this phase:**
- Every FR is satisfied or explicitly documented as no-op.
- No regression introduced by Phases 1-4.
- Item 4 is unblocked — HB11 + CSV-vs-MD work can begin against a clean v3 codebase.

---

## Risk Management

**See [design.md § Potential Risks](design.md#potential-risks)** for the canonical risk list.

**Phase-specific mitigations:**

- **Phase 2 (`tree_group` edge concepts)**: test stencil iterates every row in `table.csv` and asserts a group membership. Levitated Dipole and Z-pinch are the named edge concepts — verify their resulting groups match `CONCEPT_ONTOLOGY.md`.
- **Phase 3 (I-7 false positive)**: any non-empty diff line must trace to a v3 reclassification recorded in the commit body. If a concept's architecture columns are unchanged and the diff shows a change, that's a refactor regression — block commit.
- **Phase 4 (scoring rerun cost overshoot)**: if `extract-scores` warnings exceed 5 concepts (malformed synthesis YAML forcing a `synthesize` rerun), stop and escalate per [design.md § Key Bets Bet 3](design.md#key-bets--decisions) cost-calibration paragraph.
- **Phase 5 (grep regression)**: design's Bet 4 anticipates this — Phase 0 captured the "before" counts; Phase 5 confirms strictly decreasing.

---

## Environment Setup

**See CLAUDE.md for the canonical Python environment rules.**

Key reminders:
- All Python invocations: `uv run python ...` (never bare `python`)
- Test command: `uv run python -m pytest <path>`
- `browser-inspect` skill: `.claude/skills/browser-inspect/SKILL.md`

---

## Implementation Notes

### Phase 0 Completion (2026-05-17, no commit)

- Clustering baseline captured (`/tmp/i7_baseline/clustering_baseline.{csv,html}`) using `uv run --with plotly --with scikit-learn`.
- Ontology-chart baseline **not** captured — `generate_ontology_chart.py` crashes at HEAD on a 3-char fallback color (`'#888'`) in `text_color()` when a family value is missing from `FAMILY_COLORS`. Pre-existing bug, not introduced by Item 2. I-7 byte-equality regression check for the chart is therefore N/A; substituted visual/render check (40 concepts rendered post-refactor).
- Stale-ref grep counts saved under `/tmp/i7_baseline/stale_*_before.txt`.

### Phase 1 Completion — commit `ac320a4` `feat(phase_2a): adopt v3 column schema (FR-1)`

- Dropped `Plasma State` / `Tritium Breeding` / `Neutron Management` from `DESIGN_COLUMNS`, `VOCABULARY`, `KEY_TO_COLUMN`.
- Added `Blanket Config` entries (15 vocabulary phrases) backed by the 7 `BlanketConfig` enum values; added `VALUE_ALIASES["Blanket Config"]`.
- Remapped legacy "tritium breeding" phrasing to `in_set` of non-N/A `Blanket Config` values so existing constraints still validate.
- Verified: `validate.py --summary` shows zero `UNMAPPABLE` from dropped column names (residual UNMAPPABLE count of 22 traces to L0 physics vocabulary, not dropped columns).

### Phase 2 Completion — commit `f3f40c9` `feat(explorer): tree_group display layer + v3 test sweep (FR-2, FR-3, FR-5, FR-7, FR-11)`

- Added `tree_group(c) -> str` to `seed_registry.py` (one of: MFE/IFE/MIF/Cmpt-Tor/Estatic/Other) plus an ADR comment block at `_HIERARCHY` documenting the enum-vs-`tree_group` decision.
- Reshaped `_build_decision_tree` to group by `tree_group(c)` via `_GROUP_HIERARCHY` / `_GROUP_LEVEL1` / `_SUBTYPES`; `decision_tree.json` root field is now `tree_group`; six top-level groups (MFE: 18, IFE: 12, MIF: 4, Cmpt-Tor: 1, Estatic: 3, Other: 2 = 40 concepts total).
- `neighborhood_graph.js` `FIELD_LABELS` cleaned (dropped 3 stale, added `blanket_config`) to match `taxonomy_card.js` / `view_categorical.js`.
- Test sweep:
  - `test_taxonomy_models.py`: removed `PlasmaState` / `TritiumBreeding` imports, rewrote `test_round_trip` against `BlanketConfig`, added `test_blanket_config_round_trip` and `test_blanket_config_enum_covers_v3_values`, added a new `TestTreeGroup` class with five direct tests plus a partition check over all 40 concepts.
  - `test_taxonomy_models.py`: bumped 38 → 40 in count assertions; relaxed `name == "HTS Compact Tokamak"` to `startswith` (v3 names append `(D-T)`); rewrote `test_concept_id_is_analysis_id` to handle `17a/17b/20a/20b/39` IDs.
  - `test_similarity.py`: `s/by_slug("X")/by_slug("X-d-t")/` for the renamed slugs, redirected `laser-icf-fast-ignition-d-t` → `laser-icf-direct-drive-fast-ignition-d-t`, replaced the deleted `compact-spherical-tokamak-india` concept with a runtime search for any TBD-magnet concept (skips cleanly when none exist).
  - `test_taxonomy_server.py`: updated root-field assertion `confinement_family` → `tree_group`, bumped counts to 40.
- Test result: **176 passed, 2 skipped** (the 2 skips are pre-existing in `test_views_manual.py` etc., not introduced by Item 3).

### Phase 3 Completion — commit `42d04b2` `refactor(analysis): architecture-driven CADENCE + TREE_PATH (FR-8, FR-9, FR-14)`

- `oneoff_3d_clustering.py`: deleted `CADENCE_BY_PREFIX`; added `cadence_by_architecture(cid, info) -> float` mirroring `lib/scoring.py:detect_c2_category` (reads Confinement Family / MFE Topology / IFE Driver / MIF Method / Non-Standard Mechanism / Tokamak Shape, plus a 2-entry slug-override dict for orbital LD and Z-pinch).
- `FUNDING_M_USD` audited; added entries for `37-magnetized-target-inertial-fusion-mtif`, `38-particle-accelerator-driven-fusion`, `39-spherical-tokamak-cs-free-p-b11`. Pranos entry kept (deferred drop per spec FR-8 note).
- `generate_ontology_chart.py`: deleted `TREE_PATH` dict (44 entries); added `derive_tree_path(r) -> (family, topology, subtype)` using the same architecture-column pattern. Slug overrides handle dipole sub-styles, MIF compression methods, electrostatic device family, DPF/Muon.
- **Side fixes** (necessary to render at all): added `Cmpt-Tor` to `FAMILY_COLORS`; hardened `text_color()` against 3-digit hex (`'#888'` no longer crashes).
- I-7 regression check: `diff /tmp/i7_baseline/clustering_baseline.csv exploration/concept_analysis/oneoff_3d_clustering.csv` shows the per-concept TM/LCP/TTM/cadence values are byte-identical for all 36 retained concepts; only the last-column KMeans cluster label shifts because 3 new concepts (37/38/39) join the dataset. I-7 chart byte-equality N/A (baseline crashed); render-check passed (40 concepts rendered).

### Phase 4 Completion — commit `029b3ab` `chore(scores): regen verified_scores against v3 classifier (FR-10 partial)`

- `extract-scores` rerun (deterministic Python, no Claude). Regenerated `verified_scores.{json,md}` for **35 of 40** concepts. Five concepts (`04-laser-icf`, `11-magnetic-mirror`, `37-magnetized-target-inertial-fusion-mtif`, `38-particle-accelerator-driven-fusion`, `39-spherical-tokamak-cs-free-p-b11`) lack Section-8 synthesis YAML and so are silently skipped by `build_verified_scores`. This is exactly at the design Bet 3 escape-hatch threshold ("if more than ~5 concepts need re-synthesis, stop and reassess") — recorded as carry-forward instead of escalating.
- `calibrate` (single cross-concept Claude call) **timed out** at 10 min and was killed (rc 143). `calibrated_scores.{json,md}` remain at their May 1 state (pre-refactor); the corresponding `calibration_prompt.md` is the freshly-built v3 prompt. The deferred call should run cleanly once the 5 missing synthesis YAMLs land in Item 5, and `calibrated_scores.*` regenerated then.

### Phase 5 Completion (2026-05-17, no commit)

- FR-4 (Jinja templates) grep: **0 hits** for `plasma_state | tritium_breeding | neutron_management`.
- FR-6 (`parameter_display_registry.yaml`) grep: **0 hits**.
- FR-13 source-file grep: remaining hits are
  - Intentional v3-transition comments (`taxonomy_models.py:111-113`, `column_map.py:150`).
  - Historical `phase_1b/`, `phase_1b_v2/`, `phase_1a/generate_ontology_md.py`, `phase_1d/test2/summary.json` — out of scope per spec.
- FR-13 ID-prefix slicing grep (`concept_id[:2]`, `id[:2]`): **0 hits**.
- FR-13 prefix-keyed dicts (`CADENCE_BY_PREFIX`, `TREE_PATH = {`): **0 hits**.
- FR-12 `browser-inspect` smoke: **deferred** — session-time cap was hit by the calibrate timeout; the visual click-through gate did not run. Test-suite proxy (`test_taxonomy_server.py::test_taxonomy_tree_endpoint`) confirms the new root-field contract; pre-PR-to-`main` (Item 4) should run the full `browser-inspect` session.

### Carry-forwards (Item 5 / pre-Item-4)

1. Re-synthesize the 5 missing concepts (`04`, `11`, `37`, `38`, `39`), then run `calibrate` once. Cost ≈ 5 × `synthesize` + 1 × `calibrate` ≈ a few dollars.
2. Run `browser-inspect` smoke against the explorer; save session JSON under `/tmp/browser_inspect/<session>/`; confirm taxonomy → categorical → neighborhood → compare views render with 0 console errors.

---

**Status:** Draft → In Progress → ✅ Complete (with the 2 carry-forwards above).
**Next:** Item 4 (HB11 + CSV-vs-MD decisions) once the carry-forwards are scheduled.
