# Skeleton dry run — the record template filled against the proof-of-life

**Phase:** 2 of `.project/active/run-study-contract/plan.md`
**Date:** 2026-08-19
**Material read (read-only):** `exploration/stellarator_e2e/study/` — `run_design_search.py`, `make_report.py`, `report.html`, `design_search_R_a.csv`, `availability_sweep.csv`, `verification_summary.json`; plus `.project/active/demo-proof-of-life/plan.md`.

## What this is

The draft template's seventeen sections, filled from the proof-of-life's committed facts and nothing else. A section that fills only by inventing a fact, or by remembering the executing session, is recorded as **NO SOURCE** — filling it from memory is exactly the failure the record contract exists to prevent.

**A gap here is not a reason to soften the contract** (`design.md:346`). It is the honest distance between the pre-capability record and the contract, and it is input to Item 5. Only a section that cannot be filled *by any compliant study* is a structural defect.

## One structural observation, before the sections

The proof-of-life ran **two studies** in one work item — the (R, a) grid and the availability sweep — with two study ids, two stores, and two CSVs. Under the contract these are two records, not two arms of one: arms are variants of the same question, and these are different questions. The mapping is the executor's call and the contract makes it, correctly, at record-path naming time. Recorded here because a reader coming from the proof-of-life will expect one record and owes themselves the choice. Sections below are filled against **the grid study** unless noted; the sweep is noted where its answer differs.

---

## Section-by-section

### §1 Study header — PARTIAL

- Package, date, executor, mode: **SOURCE** — `demo-proof-of-life/plan.md:1-6` (date 2026-08-16, executing session as executor); package `exploration/stellarator_e2e/generated/`.
- Study id: **NO SOURCE.** The proof-of-life has two internal study ids passed to `StudyDefinition` (`run_design_search.py:266,273`) and no directory-level id, because there is no study directory. Recoverable only by minting one now, which is invention.
- Arms: **fills as nil** — single arm.

### §2 Intake — FILLS

**SOURCE:** `demo-proof-of-life/plan.md:3`, owner mandate verbatim: "produce something visual, understandable, readable; do not stop until there is something to show." Scope is at `:5` (fusion-tea only; sysml-codegen untouched). The owner's words survived to a committed artifact, which is what §2 asks for.

### §3 Objective and result — FILLS

**SOURCE:** objective channel `<pkg-prefix>lcoe_calc__lcoe` (`CHANNELS` map, `run_design_search.py:132-141`). Result: baseline LCOE 275.264220042 $/MWh (`run_design_search.py:112`, reproduced by the run per `plan.md` Phase 2 record); interior R optimum ≈ 15 m at LCOE ≈ 215.6 along the wall-load boundary (`plan.md`, Phase 1 result paragraph).

### §4 Constraint outcomes — PARTIAL

- Status per constraint: **SOURCE** — five verdict columns in both CSVs (`beta_ok`, `net_positive`, `recirc_ok`, `tbr_ok`, `wall_load_ok`), per point.
- `constraint_id` (qualified) and `source_local_identity`: **NO SOURCE.** `short_verdicts()` (`run_design_search.py:298`) deliberately truncates the full constraint id to its short segment before export, so the committed CSVs carry the short name only. The qualified identity existed in the store and did not survive to a committed artifact.

This is the clearest single case of what the contract adds: the fact was available and the record lost it.

### §5 Framing — FILLS BY MAPPING

The `search | sensitivity` vocabulary postdates the proof-of-life, so no artifact uses those words. The judgments are there and map without invention: study A is described as a "design-search" throughout (`plan.md`, "What this delivers"); study B is "availability sensitivity" (`plan.md`, Phase 4). Framing-as-judged is recoverable too — the Phase 1 result reports an interior optimum on R, which is a search verdict discharged.

Recorded as a mapping, not a fill: a cold reader would have to know the contract's vocabulary to make it.

### §6 Per-axis account — PARTIAL

- Search account for R and a: **SOURCE** — `plan.md` Phase 1 result: wall-load limit (4.05 MW/m²) binds above a ≈ 1.65 and is R-independent; the recirculation threshold kills the small-R·a² corner; the interior R optimum sits at ≈ 15 m; the geometric-validity mask excludes R ≤ a + 2.25.
- Sensitivity account for availability: **SOURCE** — the CAS72 `ceil` staircase, recorded as real model behavior and annotated rather than smoothed (`plan.md`, review pass 1 note 12).
- The explicit "no boundary claim is made" statement: **NO SOURCE.** Never stated in that form. The report's caveats gesture at it; the sentence the contract requires does not exist.

### §7 Axis groups — FILLS

**SOURCE:** the `AXES` map (`run_design_search.py:98-107`) gives every qualified entry key per axis; `R_TIE` (`:109`) with its docstring justification gives the one `tie`. Per-key `fan_out | tie` provenance is directly recoverable for all seven keys. The contract's §7 is a re-presentation of a structure the proof-of-life already committed.

### §8 Indicators and rulings — LARGELY NO SOURCE

- The indicator run itself, `indicators.json`, per-axis `no_constraint_response` / `constraints_reachable` values, the user's ruling, and the model-development finding per unresisted axis: **NO SOURCE.** None of this existed; Item 1's vocabulary and Item 3's tool both postdate the proof-of-life.
- The declined-axis row: **SOURCE** — `interest_rate` was proposed and declined with a stated reason (`plan.md`, "Axis compliance": the CAS71 levelization calc lacks the i≈g guard branch). §8's "including axes proposed and declined" column fills.
- The not-derivable disclosure: **NO SOURCE** as a disclosure, but its content is anticipated — review pass 1 note 5 records that the expansion completeness check is name-based only, which is the same-quantity-identity limit under a different name.

The largest gap, and the expected one. It is the epic's newest capability, not a contract defect.

### §9 Preflight results — PARTIAL

| Gate | Verdict |
|---|---|
| Declared-group key validation | **SOURCE** — mechanical check at `run_design_search.py:206-234`; `plan.md` Phase 3 records it passing |
| Suffix-sibling scan | **PARTIAL** — the check runs and its name-based limitation is disclosed (`run_design_search.py:219-220`), but no warning list is committed |
| Baseline gate against the pinned headline | **SOURCE** — `plan.md` Phase 2 record, "baseline gate exact"; pin at `run_design_search.py:112` |
| Manifest / package fingerprint match | **NO SOURCE** — no manifest existed. The nearest gate is `GlueAwareLoader`'s seal check accepting exactly {TAMPER on the two documented glue files} (`plan.md`, Phase 0 result), which is a different assertion |
| Package cleanliness | **SOURCE** — `verification_summary.json` `"package_git_clean": true` |

Four of five gates existed. The record made three of them visible, which is §9's whole point: a cold reader could see the study proceeded, not that the gates ran.

### §10 Execution route and why — FILLS

- Route and rationale: **SOURCE** — study-local direct-API (`StudyRunner` + `PreparedListStrategy`, `run_design_search.py:266-293`), forced by the package needing the `GlueAwareLoader` seal exception, which the stock CLI route cannot express (`plan.md`, Phase 0 result).
- Glue disclosure: **SOURCE, and the strongest confirmation in the dry run.** The `GLUE LEDGER` block at `run_design_search.py:27-48` (docstring) is already in §10's exact shape — per rung, what it supplies, why the model cannot, and which claims it scopes. g3 in particular states the consequence for verification in one sentence. The contract did not invent this section; it named a form that already worked.

### §11 Study definition and window provenance — FILLS

**SOURCE:** `plan.md` Phase 1 result. The scan story is complete: memoized profile integral (exact, not an approximation, because the integral depends only on non-swept inputs), coarse oracle scan, bounds chosen so the constraint boundaries sit in-frame, geometric-validity mask applied. Provenance is stated as **engineered**, and the cost of that is stated too — H1 is not claimable on an engineered window.

### §12 Cross-fingerprint correlation — FILLS AS NIL

Both studies ran at one `prepared.fingerprint` (`run_design_search.py:278`). The nil discharges by naming the condition.

### §13 Verification — FILLS

**SOURCE:** `verification_summary.json` (12 sampled rows per study, stratified by verdict combination, 5 channels, tolerance 1e-9, worst deviation 5.67e-16, verdicts re-derived) plus review pass 2's independent full re-verification (`plan.md`, implementation record). §13's second paragraph — what verification did *not* cover — fills from `glue_note` verbatim: the glue-fed CAS27 / cas28 / n_mod inputs are identical by construction on both sides and are not independently verified.

### §14 Review outcomes — FILLS

**SOURCE:** four named lenses with verdicts and dispositions, already in the contract's form — plan critique (2 blockers, 6 should-fix, 4 notes, each disposed at `plan.md:74-86`), correctness, honesty/claims, readability/visual (`plan.md`, implementation record). The pre-execution framing critique the contract requires is review pass 1. The best-supported section in the template, and the spec's `[NEED]` for named outcomes is a distillation of this.

### §15 Findings — FILLS BY EXTRACTION

The findings exist in substance and are scattered:

- model — the CAS71 levelization calc lacks the i≈g guard branch, which is why `interest_rate` could not be swept;
- model — no confinement-scaling constraint exists in the model (ISS04 named as future work);
- process — verification sampling had to be stratified by verdict combination;
- process — the dead-filler assertion had to be broadened to any-channel resurrection.

**NO SOURCE** for the contract's structure around them: no finding ids, no disposition column, no home column, no discovery log. Each of the four would need one to be filed.

### §16 Snapshot — NO SOURCE

No `snapshot.json`, no digests of the result artifacts, no tool revisions, no repo commit recorded at execution. Individual values exist scattered in the script's constants and in the store's compatibility tuple; nothing was resolved and committed as a snapshot.

### §17 What this record does not contain — FILLS BY EXTRACTION

No such section exists. Its content is spread through the report's caveats section (`report.html`, the honest-caveats block) and `plan.md`'s "Out of scope" list. The material is there; the single place a cold reader would look is not.

---

## Tally

| Verdict | Sections |
|---|---|
| Fills from a committed artifact | §2, §3, §7, §10, §11, §12 (nil), §13, §14 — 8 |
| Fills by mapping or extraction | §5, §15, §17 — 3 |
| Partial | §1, §4, §6, §9 — 4 |
| Largely or wholly no source | §8, §16 — 2 |

**No section is a structural defect.** Every NO SOURCE traces to a capability the proof-of-life predates (indicators, the manifest, the snapshot, the discovery log) or to a fact that existed and was dropped on export (§4's qualified constraint identity). None is a section that no compliant study could fill. The template's structure survives contact with the best study this project has run, so nothing in it is softened.

## B1 verdict

A cold reader working from the filled template plus `snapshot.json` recovers the study. The exercise found no fact that the two files could not hold, and it found four facts the proof-of-life *had* and lost for want of a heading — §4's qualified constraint identity, §9's gate outcomes, §17's gap list, and §15's finding homes. That is B1's claim behaving as predicted: fixed headings are what makes a fact's absence visible.

## B2 verdict — the window

**B2 holds.** The window's bounds and its `engineered` provenance are values; how the window was chosen is an argument; and the proof-of-life, with no contract telling it to, already put them in two different places — the constants at `run_design_search.py:123-125` and the scan story in `plan.md`'s Phase 1 result. The split the design worried was forced turns out to be the split the material fell into on its own. No fact landed in both halves and none landed in neither.

---

## Two-arm snapshot self-audit

Hand-constructed case, since the proof-of-life is single-arm: an A/B where `arm-sealed` runs the sealed package and `arm-adapter` runs an adapter-modified executable. The arms therefore span fingerprints — the case MF2 exists for.

| Field | Scoping | Audit |
|---|---|---|
| `window` | `arms[]` | PASS — the adapter arm's oracle scan can land on different bounds; a top-level window would silently claim otherwise |
| `strategy` | `arms[]` | PASS — a different executable admits a different proposal set |
| `effective_executable_fingerprint` | `arms[]` | PASS — this is the field that differs *by definition* in a cross-fingerprint A/B. `arm-sealed` takes the nil form (no adapter, sealed fingerprint is the identity); `arm-adapter` carries all three inputs |
| `entry_models` | `arms[]` | PASS — an adapter can change the entry-key set |
| `verification` | `arms[]` | PASS — each arm is verified against the oracle separately and has its own `summary_sha256` |
| `artifacts` | `arms[]` | PASS — separate result files per arm |
| `store_id` | `arms[]`, resolving into `stores[]` | PASS — both ids resolve; two arms spanning fingerprints have two entries, and the same-definition case has both arms naming one entry, so the tuple is stated once |
| `package.repo_commit`, `package.git_clean` | top level | PASS — study-wide; both arms run from one working tree at one commit |
| `manifest` | top level | PASS — one package, one manifest |
| `fingerprints` | top level | PASS — the map is the manifest's declared set, which is a property of the package, not of an arm. The *effective executable* fingerprint, which is arm-varying, is a different field and is correctly under `arms[]` |
| `glue_ledger` | top level | **FLAGGED — see below** |
| `tools`, `teax`, `indicators` | top level | PASS — one tool set, one teax revision, one indicator run over the package |

**One field flagged: `glue_ledger`.** In the cross-fingerprint A/B this audit constructs, glue is precisely what differs between the arms — `arm-sealed` has none and `arm-adapter` has rungs, and that difference is the *point* of the comparison. A top-level `glue_ledger` cannot express it. The design's own scoping rule ("any field that can differ between arms is arm-scoped") resolves it: `glue_ledger` belongs under `arms[]`, with the `glue_ledger_none: true` nil sibling per arm.

Recorded as a correction Phase 3 applies when it writes the full field list, not as a contract change: the rule is the design's, and applying it to this field is what the rule says to do. `design.md:258`'s illustrative sketch has `glue_ledger` at top level, which is the single-arm case reading as study-wide — the same class of miss MF2 caught, found by the same method.

No other field was found to have no correct home.
