# Implementation Plan: Ontology v3 Adoption (No Renumbering)

**Status:** Complete (all 4 phases executed 2026-05-17)
**Created:** 2026-05-17
**Last Updated:** 2026-05-17
**Branch:** `ontology-update` @ `8db3ed2` (single commit after planning commit `244ca24`)

## Source Documents

- **Spec:** [spec.md](spec.md)
- **Design:** [design.md](design.md) ← component details, bets, invariants, risks
- **Research:** [.project/research/20260517_ontology_v3_delta.md](../../research/20260517_ontology_v3_delta.md)

## Implementation Strategy

**Phasing rationale.** This is a content migration, not a feature build. The test-first principle maps onto **validation gates**: each phase ends with a check that proves an assumption before we invest in the next phase. The phasing front-loads the only thing that can realistically fail — schema-enum compatibility on the new CSV — and keeps the verbatim file pulls (cheap, low-risk) batched at the end.

**Critical path:**
```
Phase 1: prove schema parses → Phase 2: cherry-pick scoring + regex →
Phase 3: pull remaining verbatim files → Phase 4: docs + regen + commit
```

**First proof point.** End of Phase 1: `seed_registry.py` runs against the translated CSV and emits a 40-entry `concept_registry.json` with no enum-validation errors. If this fails, the design assumption that the Blanket Config schema swap is value-mappable row-by-row is wrong, and we escalate before doing any other work.

**Overall validation approach.**
- Each phase has a validation gate that must pass before moving on.
- The final commit is **not made** until Phase 4. All intermediate work sits in the working tree so a failure at any gate can be unwound by `git restore`.
- One single commit at the end (FR-1), with attribution trailer.

---

## Phase 1: De-Risk the Schema Swap

### Goal

Prove the new CSV parses cleanly through the v3 taxonomy enums before any other work happens. This is the only step where reality can disagree with the design.

### Assumption Under Test

Mallory's `BlanketConfig` enum and the schema swap (drop `Plasma State`/`Tritium Breeding`/`Neutron Management`, add `Blanket Config`) are value-mappable row-by-row from her CSV onto our IDs without producing enum-validation failures in `seed_registry.py`.

### Validation Gate (Write This First)

The end-of-phase command and expected outcome:

```bash
# Must succeed with no enum-validation errors:
uv run python exploration/concept_explorer/seed_registry.py

# Must print 40:
python -c "import json; d=json.load(open('exploration/concept_explorer/data/concept_registry.json')); print(len(d['concepts']))"

# Must run the translator twice with identical output (idempotence baked into script):
uv run python exploration/phase_1a/translate_csv_to_ours.py
cmp exploration/concept_analysis/table.csv exploration/phase_1a/table.csv  # FR-5
```

### Changes Required

**See `design.md` for:**
- CSV translation logic → [design.md#csv-translation-logic](design.md#csv-translation-logic)
- 26/30 fan-out detail → [design.md#implementation-notes](design.md#implementation-notes)
- Required invariants → [design.md#required-invariants](design.md#required-invariants)

**Files:**

- [ ] **Snapshot Mallory's CSV** to `exploration/phase_1a/_mallory_table.csv`:
  ```bash
  git show origin/fix/concept-renumbering-robustness:exploration/concept_analysis/table.csv \
    > exploration/phase_1a/_mallory_table.csv
  ```
- [ ] **Pull Mallory's parser + enum stack verbatim** (needed before the CSV will parse):
  ```bash
  git checkout origin/fix/concept-renumbering-robustness -- \
    exploration/concept_explorer/taxonomy_models.py \
    exploration/concept_explorer/seed_registry.py \
    exploration/concept_explorer/similarity.py
  ```
- [ ] **Write `exploration/phase_1a/translate_csv_to_ours.py`** (NEW, ~80 LOC). Per design:
  - `RENUMBER_MAP` dict literal (16 entries from spec.md lines 70–90).
  - Read `_mallory_table.csv` + current `exploration/concept_analysis/table.csv` (for identity columns of our 26/30).
  - Dispatch: drop Pranos; emit row 23 → our 22; emit row 31 twice → our 26 and our 30 with identity-column overlay; emit rows 37/38/39 verbatim; renumber-map for all others.
  - Write `exploration/concept_analysis/table.csv` and `exploration/phase_1a/table.csv` byte-identical.
  - **Idempotence guard inside the script:** after writing, re-run dispatch and assert byte-identical output before exit.
- [ ] **Run the translator.** Inspect the diff: row count, ID column, Blanket Config column presence.
- [ ] **Run `seed_registry.py`.** This is the gate.

### Validation

**Automated:**
- [ ] `wc -l exploration/concept_analysis/table.csv` → `41` (header + 40 rows)
- [ ] `head -1 exploration/concept_analysis/table.csv` contains `Blanket Config`, not `Plasma State`/`Tritium Breeding`/`Neutron Management`
- [ ] `awk -F, 'NR>1 {print $1}' exploration/concept_analysis/table.csv | sort` — all our 37 retained IDs + 37/38/39, no Pranos
- [ ] `cmp exploration/concept_analysis/table.csv exploration/phase_1a/table.csv` → success
- [ ] `uv run python exploration/concept_explorer/seed_registry.py` → exit 0, no enum errors
- [ ] `concept_registry.json` has 40 entries

**Manual sanity check** (per design):
- [ ] Inspect row `17a-laser-icf-hybrid-drive` — renumber path (Mallory's 27 → ours 17a)
- [ ] Inspect row `26-laser-icf-indirect-drive` — 26/30 fan-out: v3 columns from Mallory's row 31, Concept Name / Company / Driver Technology / Research ID from our main
- [ ] Inspect row `37-magnetized-target-inertial-fusion-mtif` — new-row verbatim path

**What we know works after this phase:**
- The v3 schema + Mallory's enums accept our ID set without modification.
- The translation script is idempotent and reproducible.
- The riskiest assumption in the design is collapsed.

**Escalation:** if `seed_registry.py` errors on enum mismatch, capture the offending row + value, stop, and revisit the design before continuing.

---

## Phase 2: Cherry-Pick `scoring.py` and `standardize_eta_th.py`

### Goal

Apply Mallory's two patches that survived the `main` refactor: her architecture-driven C2 classification logic (`scoring.py`) and her η_th regex extension (`standardize_eta_th.py`). These are the only synthesized-merge files; everything else in Phase 3 is verbatim.

### Assumption Under Test

Mallory's classification additions to `scoring.py` (lines 86 onward in her version) can be grafted onto main's slim `scoring.py` (which has no inline `_CANONICAL_ETA_TH`/`canonical_eta_th()`) without behavioral regression. Her regex enhancement in `standardize_eta_th.py` actually catches the 4+ concepts main's regex misses.

### Validation Gate (Write This First)

```bash
# scoring.py: behavioral smoke — detect_c2_category runs against a sample concept
uv run python -c "
from exploration.concept_analysis.scripts.lib import scoring
# pick any concept dict from concept_registry.json and call detect_c2_category
"

# standardize_eta_th.py: confirm regex catches the variants
uv run python exploration/concept_analysis/scripts/standardize_eta_th.py --dry-run
# Expected: touches concepts 19, 25, 27, 36 (the ones main's regex misses)
```

### Changes Required

**See `design.md` for:**
- Bet 2 patch boundaries → [design.md#bet-2](design.md#bet-2-scoringpy-and-standardize_eta_thpy-are-two-clean-cherry-pick-patches-no-value-reconciliation)
- Risk on dropped regex extension → [design.md#potential-risks](design.md#potential-risks)

**Files:**

- [ ] **`exploration/concept_analysis/scripts/lib/scoring.py`** — keep main's content as the base. Diff Mallory's version against main's: everything from `detect_c2_category` onward (her `_derive_peer_group`, modified `apply_heritage_credit`, and any downstream changes) is the patch. Apply by hand or via `git show origin/fix/concept-renumbering-robustness:.../scoring.py` and merging the bottom half. Do **not** add back `_CANONICAL_ETA_TH` or `canonical_eta_th()` — they live in `canonical_params.py`.
- [ ] **`exploration/concept_analysis/scripts/standardize_eta_th.py`** — keep main's version (already imports from `canonical_params`). Apply Mallory's regex enhancement: extend the variable-name pattern to `_?(?:eta_th|...)(?:_[A-Za-z0-9]+)*` so it catches `_ETA_TH_CENTRAL`, `eta_dec`, `ETA_DEC`. Do **not** revert the `canonical_params` import.
- [ ] **`canonical_params.py`** — untouched (η_th table is byte-identical to Mallory's; verified in design).
- [ ] **`run_analysis.py`** — explicitly NOT pulled (design Bet; main is schema-agnostic).

### Validation

**Automated:**
- [ ] Import smoke: `uv run python -c "from exploration.concept_analysis.scripts.lib import scoring; print(scoring.detect_c2_category)"`
- [ ] `uv run python exploration/concept_analysis/scripts/standardize_eta_th.py --dry-run` reports touches on **at least** concepts 19, 25, 27, 36 (regex extension proof)
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py status` → exit 0 (FR-12)

**Manual:**
- [ ] PR-review-style read of the `scoring.py` diff: confirm main's `canonical_availability`, `canonical_mn` references (if any) survive, and Mallory's classification block is present in full
- [ ] Confirm `git diff origin/fix/concept-renumbering-robustness -- exploration/concept_analysis/scripts/lib/scoring.py` is non-empty (expected per Bet 2)

**What we know works after this phase:**
- Mallory's classification refactor is integrated without losing main's canonical-params extraction.
- The regex extension is preserved and verified to act on the right concepts.

---

## Phase 3: Pull Remaining Verbatim Files

### Goal

Batch-pull the 13 remaining files that are clean verbatim copies — no main-side conflicts.

### Assumption Under Test

None — these files are unmodified on main since the merge-base (verified in design Research Findings). This phase is mechanical.

### Validation Gate

```bash
for f in <list of 13 files>; do
  git diff origin/fix/concept-renumbering-robustness -- "$f" | head -1 || echo "DIFF for $f"
done
# Expected: empty output (every file matches Mallory byte-for-byte, with the one exception below)
```

### Changes Required

**See `design.md` for:**
- Component overview / file inventory → [design.md#component-overview](design.md#component-overview)
- 2-line note exception on `CONCEPT_ONTOLOGY.md` → [design.md#component-overview](design.md#component-overview)

**Files (single batch checkout):**

```bash
git checkout origin/fix/concept-renumbering-robustness -- \
  exploration/concept_analysis/scripts/lib/concepts.py \
  exploration/concept_analysis/scripts/lib/claude.py \
  exploration/concept_analysis/scripts/rerun_all_models.py \
  exploration/concept_analysis/C2_SCORING.md \
  exploration/concept_explorer/static/js/taxonomy_card.js \
  exploration/concept_explorer/static/js/view_categorical.js \
  exploration/phase_1a/schema.md \
  exploration/phase_1a/CONCEPT_ONTOLOGY.md \
  exploration/phase_1a/CONCEPT_CATEGORIES_PROPOSAL.md \
  exploration/phase_1a/RECLASSIFIED_CONCEPTS.md \
  exploration/phase_1a/SCHEMA_REVISION_PROPOSALS.md \
  exploration/phase_1a/concept_ontology_v3.png \
  exploration/phase_1a/generate_ontology_chart.py \
  exploration/phase_1a/generate_ontology_md.py
```

- [ ] Run the batch checkout.
- [ ] For each file: `git diff origin/fix/concept-renumbering-robustness -- <path>` → empty (FR-2, FR-3).

### Validation

**Automated:**
- [ ] Loop the diff check above; all empty
- [ ] `git status` shows the staged changes match the expected file set, no surprises

**What we know works after this phase:**
- All 13 verbatim files are at Mallory's content.
- Phase 2 + Phase 3 together complete buckets A (code + docs) of the spec.

---

## Phase 4: Mapping Doc, Note Prepend, Final Regen, Commit

### Goal

Add the new ID-mapping doc, prepend the 2-line note on `CONCEPT_ONTOLOGY.md`, regenerate the explorer JSON one last time (in case anything changed since Phase 1), run the full acceptance check, and produce the single commit.

### Assumption Under Test

The full set of FRs and acceptance criteria pass against the final state. (At this point the design's assumptions are all collapsed; this phase is verification + ceremony.)

### Validation Gate

The spec's full acceptance-criteria block (spec.md §Acceptance Criteria).

### Changes Required

**See `design.md` for:**
- ID_MAPPING.md content sketch → [design.md#component-overview](design.md#component-overview)
- Note prepend exception → [design.md#component-overview](design.md#component-overview)

**Files:**

- [ ] **Write `exploration/phase_1a/ID_MAPPING.md`** (NEW):
  - Section 1: renumbering map (the 16-row table from spec.md lines 70–90)
  - Section 2: orphan-directory note for `knowledge/concept_research/20-modular-hts-stellarator/` — has unique pre-split content, deferred to Item 6
  - Section 3: pointer to `CONCEPT_ONTOLOGY.md` for v3 design rationale
- [ ] **Prepend a 2-line note** to the top of `exploration/phase_1a/CONCEPT_ONTOLOGY.md` pointing readers to `ID_MAPPING.md`. **This is the documented exception** to FR-3 verbatim guarantee; call it out in the commit body.
- [ ] **Re-run** `uv run python exploration/concept_explorer/seed_registry.py` to refresh `concept_registry.json` + `decision_tree.json` against the final tree (idempotent vs. Phase 1, but cheap insurance).
- [ ] **Stage and commit** in one atomic commit on `ontology-update`:
  ```
  git add exploration/concept_analysis/table.csv \
          exploration/phase_1a/table.csv \
          exploration/phase_1a/_mallory_table.csv \
          exploration/phase_1a/translate_csv_to_ours.py \
          exploration/phase_1a/ID_MAPPING.md \
          exploration/phase_1a/CONCEPT_ONTOLOGY.md \
          exploration/phase_1a/CONCEPT_CATEGORIES_PROPOSAL.md \
          exploration/phase_1a/RECLASSIFIED_CONCEPTS.md \
          exploration/phase_1a/SCHEMA_REVISION_PROPOSALS.md \
          exploration/phase_1a/schema.md \
          exploration/phase_1a/concept_ontology_v3.png \
          exploration/phase_1a/generate_ontology_chart.py \
          exploration/phase_1a/generate_ontology_md.py \
          exploration/concept_analysis/scripts/lib/scoring.py \
          exploration/concept_analysis/scripts/lib/concepts.py \
          exploration/concept_analysis/scripts/lib/claude.py \
          exploration/concept_analysis/scripts/standardize_eta_th.py \
          exploration/concept_analysis/scripts/rerun_all_models.py \
          exploration/concept_analysis/C2_SCORING.md \
          exploration/concept_explorer/taxonomy_models.py \
          exploration/concept_explorer/seed_registry.py \
          exploration/concept_explorer/similarity.py \
          exploration/concept_explorer/static/js/taxonomy_card.js \
          exploration/concept_explorer/static/js/view_categorical.js \
          exploration/concept_explorer/data/concept_registry.json \
          exploration/concept_explorer/data/decision_tree.json
  ```
- [ ] **Commit message** (HEREDOC):
  ```
  feat: adopt ontology v3 schema, new concepts, and architecture-driven classification (no renumbering)

  Adopts the v0.3.0 ontology *content* from origin/fix/concept-renumbering-robustness
  while keeping our existing concept IDs. Cherry-picks 18 files of Mallory's content
  plus a translated CSV; no directory renames.

  Buckets:
  - A (code/docs): 13 files verbatim; scoring.py and standardize_eta_th.py
    carry Mallory's classification + regex patches on top of main's canonical_params
    refactor (lib/canonical_params.py is unchanged — Mallory's η_th table is
    byte-identical to main's).
  - B (CSV): translate_csv_to_ours.py rewrites Mallory's CSV onto our ID scheme;
    drops Pranos; splits row 23 (First Light) and adds row 37 (NearStar);
    fans Mallory's row 31 onto our 26 + 30 (identity columns preserved).
  - C (ID mapping): new ID_MAPPING.md + 2-line note prepended to CONCEPT_ONTOLOGY.md
    (the note is the one documented exception to verbatim-pull).
  - D (regen): concept_registry.json + decision_tree.json regenerated.

  Out of scope (deferred): Item 3 code-gap closure (phase_2a/column_map.py,
  _HIERARCHY, ConfinementFamily enum, templates, neighborhood_graph.js,
  parameter_display_registry.yaml, taxonomy tests, oneoff_3d_clustering
  funding/cadence maps); Item 4 ontology decisions (HB11 Fast-vs-Ultrashort,
  Heating Type / Driver Type CSV-vs-MD authority); Item 5 new-concept analyses;
  Item 6 Pranos + 20-modular-hts-stellarator orphan cleanup.

  Co-developed-with: Mallory Snowden <mallory.snowden@astera.org>
  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
  ```

### Validation (Full Acceptance Sweep)

**Automated (run all):**
- [ ] All Bucket A diff checks empty except the two synthesized files + `CONCEPT_ONTOLOGY.md` (spec §AC Code/docs)
- [ ] All Bucket B/C CSV checks (header, row count = 41, ID set, no Pranos, two Inertia rows, row 22 First Light only, row 37 exists, `cmp` equal, `ID_MAPPING.md` exists)
- [ ] `uv run python exploration/concept_explorer/seed_registry.py` exits 0
- [ ] `concept_registry.json` has 40 entries
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py status` exits 0
- [ ] `git diff --name-only --diff-filter=R main -- exploration/concept_analysis/analyses/ knowledge/concept_research/` empty
- [ ] `git diff --name-only main -- 'exploration/concept_analysis/analyses/**/synthesis.md' 'exploration/concept_analysis/analyses/**/analysis.md' 'exploration/concept_analysis/analyses/**/model_output.txt'` empty
- [ ] `git diff --name-only main -- 'exploration/concept_analysis/scores/' 'exploration/concept_explorer/data/*.json'` shows only `concept_registry.json` and `decision_tree.json`
- [ ] One single commit on `ontology-update` after `244ca24`
- [ ] Commit message contains `Co-developed-with: Mallory Snowden` trailer

**Manual:**
- [ ] Skim the commit diff in one pass; confirm ~27 files and no surprises

**What we know works after this phase:**
- Item 2 is complete. Items 3, 4, 5 can be picked up against this commit as their baseline.

---

## Risk Management

**See [design.md#potential-risks](design.md#potential-risks)** for the canonical risk list.

**Phase-specific mitigations:**

- **Phase 1** (schema gate): if `seed_registry.py` errors, capture the offending row+column and revisit before any other phase. Do not push forward. This is the only phase that can invalidate the design.
- **Phase 2** (regex extension drop): the regex enhancement is small and easy to miss during the merge. Validation explicitly checks for touches on concepts 19/25/27/36.
- **Phase 3** (verbatim pulls): low-risk; loop diff-check catches any contamination.
- **Phase 4** (final commit): the 2-line prepended note on `CONCEPT_ONTOLOGY.md` is the only deliberate verbatim violation — documented in the commit body so it isn't mistaken for drift.

---

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-05-17
**Changes:**
- Snapshot Mallory CSV → `exploration/phase_1a/_mallory_table.csv` (40 rows incl. header).
- Pulled `taxonomy_models.py`, `seed_registry.py`, `similarity.py` from Mallory verbatim.
- Wrote `exploration/phase_1a/translate_csv_to_ours.py` (~180 LOC incl. comments) with RENUMBER_MAP + UNCHANGED_IDS, 26/30 fan-out (identity columns from our CSV), split-22 (First Light), Pranos defensive drop, idempotence guard, CRLF terminators matching Mallory's CSV.
- Ran translator → 40 rows, byte-identical mirror to `exploration/phase_1a/table.csv`.
- `seed_registry.py` exited 0; emitted 40 concepts. **Gate passed**: schema swap is value-mappable row-by-row.
**Issues:** None.
**Deviations:**
- Plan said `RENUMBER_MAP` is 16 entries; in code I split it into `RENUMBER_MAP` (14 actually-renumbered Mallory IDs) + `UNCHANGED_IDS` (20 Mallory IDs whose numeric prefix is identical on both sides). The two-table structure is more explicit; total mapping coverage matches the spec's 16-row delta plus unchanged IDs.

### Phase 2 Completion
**Completed:** 2026-05-17
**Changes:**
- `lib/scoring.py` ← Mallory's version with the `_CANONICAL_ETA_TH` dict + `canonical_eta_th()` function stripped (those now live in `canonical_params.py`, which main already extracted and which is byte-identical to Mallory's table). `re` import retained — used by `extract_yaml_blocks`.
- `standardize_eta_th.py` ← main's version + Mallory's regex extension: pattern now allows `_?` prefix, `_[A-Za-z0-9]+` suffixes, and `eta_dec`/`ETA_DEC`. Kept main's `from lib.canonical_params import canonical_eta_th`. Dry-run confirmed regex catches concepts 19, 25, 27, 36 (the variants main missed).
- `canonical_params.py` untouched (Mallory's η_th table is byte-identical).
**Issues:** None.
**Deviations:** None.

### Phase 3 Completion
**Completed:** 2026-05-17
**Changes:** Single `git checkout origin/fix/concept-renumbering-robustness -- ...` batch pulled the 14 verbatim files listed in the plan (13 files + `concept_ontology_v3.png`).
**Issues:** Loop diff-check passed for all 13 expected verbatim files (`concepts.py`, `claude.py`, `rerun_all_models.py`, `C2_SCORING.md`, `taxonomy_models.py`, `seed_registry.py`, `similarity.py`, `taxonomy_card.js`, `view_categorical.js`, `schema.md`, `CONCEPT_ONTOLOGY.md`, `CONCEPT_CATEGORIES_PROPOSAL.md`, `RECLASSIFIED_CONCEPTS.md`, `SCHEMA_REVISION_PROPOSALS.md`, `generate_ontology_chart.py`, `generate_ontology_md.py`, plus the PNG).
**Deviations:** None.

### Phase 4 Completion
**Completed:** 2026-05-17
**Changes:**
- Wrote `exploration/phase_1a/ID_MAPPING.md` with renumber table, fan-out explanation, orphan note, provenance.
- Prepended 2-line note to `CONCEPT_ONTOLOGY.md` pointing to `ID_MAPPING.md` (documented exception to FR-3 verbatim guarantee).
- Re-ran `seed_registry.py` → 40 entries, idempotent vs Phase 1.
- Full acceptance sweep: row count 41, `Blanket Config` in header, no Pranos, two Inertia rows, row 22 First Light only, row 37 present, `cmp` clean, no renames under `analyses/`/`concept_research/`, no regenerated synthesis/analysis/model_output artifacts, only `concept_registry.json` + `decision_tree.json` under `concept_explorer/data/`.
**Issues:**
- `run_analysis.py status` initially failed with `ImportError: FREEFORM_CONCEPTS`. Cause: Mallory's `lib/concepts.py` (pulled verbatim in Phase 3) no longer exports that constant — her code derives freeform via `_is_freeform_architecture(concept)`. Main's `run_analysis.py` imported `FREEFORM_CONCEPTS` but never used it (orphan from an earlier refactor). Resolved by removing the dead import — a 1-line surgical edit, much smaller than pulling Mallory's full +127 LOC version. FR-12 now passes.
**Deviations:**
- `run_analysis.py` is not literally untouched as the design said. The single change is removing one dead-import line; the file is otherwise main's version. Documented in commit body.

---

**Status:** Complete
**Next:** `/_my_audit_implementation`, then archive to `.project/completed/`. Item 3 of ONTOLOGY-V3 is now unblocked.
