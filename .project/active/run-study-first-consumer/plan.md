# Implementation Plan: Run-Study First Consumer (RUN-STUDY Item 6)

**Status:** In Progress — Phase 1 complete (owner-approved 2026-08-21); Phase 2 gated on WI-031
**Created:** 2026-08-21
**Last Updated:** 2026-08-21
**Branch:** `feat/run-study-first-consumer`, cut from `main` at `8d6c443b` (migration PR #107 merged 2026-08-21). One branch for all four phases; Phase 1 is a reviewable first commit.

## Source Documents
- **Spec:** `.project/active/run-study-first-consumer/spec.md`
- **Design:** `.project/active/run-study-first-consumer/design.md` ← components, decisions D1–D11, invariants I1–I9, arm tables (Appendix A)
- **Align:** `.project/active/run-study-first-consumer/align.md`
- **Modeling PM prerequisites:** `work/completed/20260822_WI-030_computed-beta-peak-field/spec.md` (modeling item), `work/completed/20260822_WI-031_research-round-item6-values/spec.md` (research round)

## The Point

The run-study capability (Items 1–5) has never been used whole. The epic's critical success factor is the owner's: **[OWNER]** "A short-prompt study reaches the proof-of-life's verification and reporting floor, and a fresh administrator can synthesize it from the committed record alone." Only a real study, invoked with a goal-only prompt, run through every runbook step, and handed cold to an administrator, proves it. This item runs two such studies on the Stellaris package: a power-cycle A/B on the current sealed package, and a magnet-technology A/B on the package regenerated after WI-030 adds a computed beta and a peak-field constraint. **[OWNER 2026-08-21]** "Item 6 should PAUSE and the modeling change should be executed through the `work/` item." The oracle runs in both studies for the last time as a study obligation: **[OWNER-VERBATIM]** "check 1 ONLY FOR THIS DEMO -- once it is demonstrated, I don't want to have to keep two sets of equations." On the way in, the study policy is ratified and moved so both records cite a stable path.

The proof is "the capability, unchanged, produces the floor." The only code this item writes is each study's definition file (`design.md#core-concept`).

## Implementation Strategy

**Phasing Rationale:** Phase 1 is everything that needs neither the package nor the `work/` items: the policy cutover (with the owner's review of the final draft), the G1 template fix, the administrator briefs. It runs first because both records cite the policy. Phase 2 is the study that needs no model change (power cycle) and runs as soon as the migration lands and WI-031's round closes; it also creates the discovery log and is the first test of the capability whole. Phase 3 is the magnet study, which resumes on WI-030's six names. Phase 4 closes. The `work/` items are not phases: they run in the modeling PM, and Phases 2–3 wait on mechanical conditions, not on promises.

**Critical Path:** policy cutover (owner review) → baseline timing → WI-031 closes → study 2 through the runbook → administrator → WI-030 closes, `main` merged → study 1 → administrator → close.

**First Proof Point:** the policy test and the template test go red on the unmodified tree and green after the cutover (Phase 1). The first *capability* proof is Phase 2's step 9: every point of the three-arm cycle study lands in one store on the stock route with the package git-clean afterward.

**Overall Validation Approach:**
- Each phase starts with a test stencil; Phases 2–3 additionally run the runbook's own fail-closed gates (preflight 6/6, `verify.py` pass, step-15 placeholder check).
- Every commit: `uv run pytest tests/study tests/models` green; `git status` clean under `exploration/stellarator_e2e/generated/`.
- No tool or runbook step is edited (`design.md#required-invariants` I1); the diff under `scripts/study/` and `runbook.md` is reviewed at each phase end for exactly the allowed changes.

---

## Phase 1: Policy cutover, template fix, briefs

### Goal
Give both records a stable policy to cite, close the G1 digest gap before a record is written, and write the two administrator briefs. Independent of the package and the `work/` items.

### Assumption Under Test
The draft policy can be ratified whole with only the two planned additions and the two dispositions, and every live citation can move in one commit without breaking the skill's tests (design B5, D8).

### Test Stencil (Write This First)
```python
# tests/study/test_policy_path.py  (NEW)
LIVE = [".claude/skills/run-study/SKILL.md", ".claude/skills/run-study/runbook.md",
        "exploration/stellarator_e2e/study/run_design_search.py"]
def test_live_files_cite_the_ratified_policy(repo_root):
    for rel in LIVE:
        text = (repo_root / rel).read_text()
        assert "modeling_project/STUDY_POLICY.md" in text, rel
        assert "demo-study-parameterization-policy" not in text, rel
def test_policy_has_axis_forces_and_rescoped_h1(repo_root):
    text = (repo_root / "modeling_project/STUDY_POLICY.md").read_text()
    assert "## 9. Axis forces and framing" in text
    assert "search-framed" in text.split("H1")[1][:600]

# tests/study/test_record_template.py  (NEW)
def test_oracle_source_digest_carries_files(repo_root):
    text = (repo_root / ".claude/skills/run-study/record-template.md").read_text()
    blocks = [b for b in text.split('"source_digest"')[1:]]
    assert len(blocks) == 2 and all('"files"' in b[:300] for b in blocks)
```

### Changes Required

**See `design.md` for:** D8 (policy mechanics), Research Findings "The policy citation surface", "The oracle digest gap (G1)", D10 (administrator briefs).

#### 1. Tests
- [x] `tests/study/test_policy_path.py`, `tests/study/test_record_template.py` — write; confirm both fail on the unmodified tree

#### 2. Policy cutover
- [x] `git mv .project/active/demo-study-parameterization-policy/policy.md modeling_project/STUDY_POLICY.md`
- [x] Header: Status "Ratified [OWNER] 2026-08-21 (Item 6 Align)"; governing frame line updated (the demo epic is on hold; the run-study capability is the consumer)
- [x] § 6 heading: drop "for Item 5"; the list is the machinery any study may use
- [x] § 7 H1: add "applies to search-framed studies; a sensitivity-framed sweep at 100% feasible is expected behavior" (concept-design `run-study-skill-design.md:113`)
- [x] New § 9 "Axis forces and framing": every proposed axis (swept or declined) carries its indicator results and a search-vs-sensitivity judgment before execution; `no_constraint_response` is a sound negative that returns to the owner with a model-development finding; indicators inform, never gate (concept `run-study-skill.md` SC-2/3, Settled; runbook steps 2–4 are the procedure, not restated)
- [x] New § 10 "Verification and the 1costingFE handshake": the oracle is a fidelity check on generated code, runs for Item 6's two studies, and leaves the study contract afterward (retirement filed at Item 6 close); the handshake is outside the study contract, used when a direct comparison is readily possible. Quote `align.md` § 3 verbatim for both.
- [x] Live citations → new path: `SKILL.md:74`, `runbook.md:9`, `run_design_search.py:13`, `.project/backlog/BACKLOG.md` (Active Work Items row: retire it), `epic_run_study_capability.md`, `CURRENT_WORK.md`, the three concept docs (one-line "moved 2026-08-21" note each), this item's spec/design/align
- [x] **Owner review checkpoint:** full `STUDY_POLICY.md` diff presented; § 10 rewritten at the owner's direction (plain: 1costingFE is the validation reference when applicable; the oracle is not a study obligation); approved 2026-08-21

#### 3. G1 template fix
- [x] `.claude/skills/run-study/record-template.md:308` and `:367`: `source_digest` carries `{recipe, digest, files: [{path, sha256}]}`; the rule-text paragraph for G1 updated to say why (`common.tool_source_digest` emits `files`)

#### 4. Administrator briefs
- [x] `.project/active/run-study-first-consumer/briefs/administer-template.md`: Item 5's `brief.md` minus the pre-capability waiver; placeholders only for the record path; states the three skill files, the read-only rule, `knowledge/holdout/` never read, one output file `synthesis.md`

### Validation
**Automated:**
- [x] `uv run pytest tests/study -q` green (the two new tests included)
- [x] `grep -rn demo-study-parameterization-policy --include=*.md --include=*.py . | grep -v "^./.project/completed\|^./.project/reports\|^./.project/research"` → only historical notes remain (the policy's own status line, the concepts' "moved" notes, the test's constant, this plan)

**Manual:**
- [x] Owner approved the policy draft 2026-08-21 (after the § 10 rewrite)
- [ ] PR opened against `main`; small enough to review in one sitting

**What We Know Works After This Phase:** both records will cite one policy at a stable path; the snapshot shape names which oracle verified a study; the administrator mechanism is ready to spawn.

---

## Phase 2: Study 2 — power-conversion cycle A/B (three arms)

### Goal
The first complete pass through the capability: intake → definition → stock route → verify → record → commit → administrator. Creates `DISCOVERY_LOG.md`.

### Gate (all mechanical; do not start without them)
- [x] Migration PR #107 merged; branch cut from `main` `8d6c443b` (2026-08-21)
- [x] `STOP_PARSER_TEAX_ROOT` HEAD is `744745f` (checked 2026-08-21)
- [x] Phase 1 committed on this branch (`dcf159d5`, owner-reviewed policy)
- [x] WI-031 research approved 2026-08-21 (`knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md`, DI-007–DI-010); study 2's two values resolved (`p_pump` cycle-independent, `eta_th` PDF-cited); design Appendix A corrected. Closing the item is the owner's (`pm close-item WI-031`).
- [x] Baseline timing (2026-08-21, stock route, warm process): `execute_baseline` 0.72 s incl. load; 19-point sweep 2.71 s → **0.14 s/point**. 3 × 948 points ≈ 7 min; a 50 × 50 × 2-arm magnet grid ≈ 12 min. No coarsening needed; proof-of-life window reused as is.

### Assumption Under Test
Design B1: the runbook, tools, and record contract carry a multi-arm study unmodified. Design B4 (fresh administrator) gets its first real test.

### Test Stencil (Write This First)
```python
# tests/study/test_records.py  (NEW; generic over every committed record directory)
RECORDS = sorted(Path("exploration/stellarator_e2e/studies").glob("2*-*/"))
@pytest.mark.parametrize("record", RECORDS, ids=lambda p: p.name)
def test_record_is_closed(record):
    snap = json.loads((record / "snapshot.json").read_text())
    stores = {s["store_id"] for s in snap["stores"]}
    assert all(a["store_id"] in stores for a in snap["arms"])
    assert "<" not in (record / "record.md").read_text()          # no placeholders
    csv_arms = {row["arm_id"] for row in csv.DictReader(open(record / "results" / "points.csv"))}
    assert csv_arms == {a["arm_id"] for a in snap["arms"]}
```

### Changes Required

**See `design.md` for:** D1–D3, D5–D6 (arms, one store, windows), D9 (manifest objective), D10 (administrator), Implementation Notes (study.py rules), Appendix A (arm table for study 2).

#### 1. Test
- [ ] `tests/study/test_records.py` — write; passes vacuously with no record, then for real after step 9

#### 2. Manifest (data-only)
- [ ] `exploration/stellarator_e2e/studies/manifest.json`: add `magnet_capital` (`stellarator_09__stellaris__magnet_cost__capital_cost`) to `objective_catalog` with a note; re-run `indicators.py --print-fingerprint` (the manifest is not in the indicator-input set, so the fingerprint is unchanged; confirm)

#### 3. The study, through the skill (execute mode)
- [ ] **Owner gives the intake** for study 2 in their own words (goal + scope only). Record it verbatim; mint `<study-id>` per `runbook.md § Naming`
- [ ] Runbook steps 1–4: record opened; `axes.json` declares R, a (proof-of-life groups) and the cycle block as a declined-as-axis, held-per-arm block with its three keys; `indicators.py` run (no subset); framing argued (search on R/a, sensitivity on the block); pre-execution critique recorded (§ 14)
- [ ] `studies/<study-id>/study.py`: arm blocks per Appendix A; `proposals()` = arms × window; `export()` with `arm_id`; imports only `study_route`
- [ ] Steps 5–6: `execute_baseline` → `preflight.py gates` 6/6 (§ 9)
- [ ] Step 7: oracle scan of the window; `arms[].window` provenance `engineered`, reused from the proof-of-life with the reason (§ 11)
- [ ] Step 8: route rationale (direct-API; coordinated block) and "glue ledger: none" (§ 10)
- [ ] Step 9: `run_points` once, one store; `git status` clean under `generated/`; § 3–4 from `StudyQuery` per arm with qualified constraint ids
- [ ] Step 10: `verify.py --store <db>` → `results/verification_summary.json`; § 13 names uncovered channels (`p_fus`) and cites `verify.py` stratified sampling as the inherited home (spec SC 10)
- [ ] Steps 11–14: framing as judged; per-arm account; review outcomes; findings with homes; `DISCOVERY_LOG.md` created, one row per finding
- [ ] Step 15: snapshot resolved (G1 `files[]` present); § 12 nil discharged ("single fingerprint"); § 17 states that the paper names no cycle; § 15 carries the DI-008 `p_pump` finding with home = WI-031 R4 item; commit

#### 4. Administrator
- [ ] `briefs/administer-<study-id>.md` from the template; spawn one `general-purpose` subagent with the brief verbatim as its entire prompt (never `fork`)
- [ ] `synthesis.md` lands in the record; commit; its "does not support" entries classified reader-miss vs contract-gap in Implementation Notes (Item 5 pattern)

### Validation
**Automated:**
- [ ] `uv run pytest tests/study tests/models -q` green, `test_records.py` included
- [ ] `preflight_results.json` 6/6; `verification_summary.json` `outcome: pass`
- [ ] `git diff --stat main -- scripts/study .claude/skills/run-study/runbook.md` → empty (I1)

**Manual:**
- [ ] § 8 shows no `no_constraint_response` axis (expected for this block) or carries the owner's ruling if one appears
- [ ] The synthesis recovers: three arms' framing, LCOE per arm, every constraint outcome by qualified id, findings traced to `results/`
- [ ] The block's effect reads as expected: `recirc_ok` fence moves with η, wall-load fence does not

**What We Know Works After This Phase:** the capability runs whole on a multi-arm study; a stranger can read the result; the discovery log exists.

---

## Phase 3: Study 1 — magnet technology A/B (REBCO vs Nb3Sn)

### Goal
The epic's named study, on the regenerated package, with the two new verdicts carving the arms' feasible regions.

### Gate
- [ ] WI-030 closed and merged to `main`; `main` merged into this branch; `model_contract.json` resolves `n_e0`, `T_e0`, `n_He0`, `alpha_n_e`, `peak_ratio`, `B_max` as parameters and `peak_field_ok` as a constraint id; `beta` absent; `beta_calc__beta` in the manifest objective catalog
- [ ] `preflight.py gates` 6/6 on the regenerated package with the re-pinned manifest (WI-030's exit criterion, re-run here)
- [ ] DI-009/DI-010 sources ingested via `/manage-sources`, or not: decides whether `f_carnot_cryo` is a citation or a hold and whether arm B's `vol_cold_cryo` is derived or held (Appendix A)

### Assumption Under Test
Design B3: the computed beta makes `beta_ok` respond to B and density, so the Nb3Sn arm's feasible region is carved by the model's verdicts, not by a hand rule. Design B2: one package, one store, no cross-fingerprint section.

### Test Stencil (Write This First)
```python
# tests/study/test_records.py gains one case-level check, generic:
def test_arms_share_one_store_when_fingerprints_agree(record):
    snap = json.loads((record / "snapshot.json").read_text())
    fps = {a["effective_executable_fingerprint"]["value"] for a in snap["arms"]}
    if len(fps) == 1:
        assert len(snap["stores"]) == 1
```

### Changes Required
**See `design.md` for:** D6–D7 (B × density window, tied fan-out), Appendix A (study 1 table), Potential Risks (24.9 T binds arm A exactly at 9.0 T).

- [ ] Owner intake for study 1, verbatim; mint `<study-id>`
- [ ] Steps 1–4 on the regenerated package: `axes.json` declares `B` (one key) and `density` (four-key tied fan-out, provenance `tie` for the scale relation); indicators run; **if any group reports `no_constraint_response`, stop and obtain the owner's ruling and file the finding before step 5**
- [ ] `studies/<study-id>/study.py`: two arm blocks per Appendix A; shared (B, density-scale) window; held values with their sources in the module docstring
- [ ] Steps 5–10 as Phase 2; step 7's oracle scan fixes the exact B and density bounds (arm B's `peak_field_ok` should bind near 4.7 T; the density floor sits below the LTS arm's beta-limited pressure)
- [ ] Steps 11–15: § 6 per arm names the binding constraints (expected: `peak_field_ok` + `beta_ok` in arm B, `wall_load_ok` in arm A at high density); § 15 cites at least one study-2 log row by `<study-id>#<n>` (spec SC 10); § 12 nil discharged; § 17 holds (`f_carnot_cryo`, `vol_cold_cryo` unless WI-031 sourced them)
- [ ] Administrator as Phase 2

### Validation
**Automated:** as Phase 2; `test_records.py` over both records.
**Manual:**
- [ ] Arm B's feasible region is non-empty and bounded by the two new verdicts; arm A's by wall load
- [ ] LCOE per arm reported with the magnet-capital channel verified by the oracle (D9)
- [ ] The synthesis recovers both arms' framing, LCOE, named outcomes, and findings

**What We Know Works After This Phase:** the magnet-technology A/B exists as an immutable record; the model rejects an LTS arm on its own verdicts.

---

## Phase 4: Close

### Goal
Discharge the epic's Item 6 criteria and leave the follow-ups where they belong.

### Changes Required
- [ ] `.project/backlog/BACKLOG.md`: row "Retire the oracle from the study contract" (runbook steps 7 and 10 gates, manifest `oracle` requirement, `verify.py` tests, `ANNEX.md § Oracle`) with the policy § 10 disposition cited
- [ ] `epic_run_study_capability.md`: Item 6 success criteria checked with evidence paths; epic criteria 1–4 and "First consumer" / "Policy disposition" marked with dates
- [ ] Candidate DI insight noted for the modeling PM ("B enters physics through beta, not only cost") — a note in WI-030's record, not filed here
- [ ] `CURRENT_WORK.md`, spec status → Complete; `/_my_audit` suggested

### Validation
- [ ] Every spec success criterion has a checkbox and an evidence path in Implementation Notes
- [ ] `uv run pytest tests/study tests/models -q` green on the final commit

---

## Environment Setup

**See CLAUDE.md for `uv` rules.** Phases 2–3:
```bash
source /home/reid/1cfe/agentic-mbse/.env                 # SYSIDE_LICENSE_KEY (model tests)
export STOP_PARSER_TEAX_ROOT=/home/reid/1cfe/teax        # HEAD must be 744745f
export STUDY_REQUIRE_TEAX=1                              # stock-route tests fail, never skip
git -C "$STOP_PARSER_TEAX_ROOT" rev-parse --short HEAD   # → 744745f, or stop
```
Study stores go under `exploration/stellarator_e2e/studies/<study-id>/_work/` (gitignored pattern to add beside `study/_work/`); the route's `link_root` must stay outside `generated/`.

---

## Risk Management

**See `design.md#potential-risks`.**

**Phase-Specific Mitigations:**
- **Phase 1**: the policy diff is presented whole before commit; the citation test makes a missed reference a red test, not a stale link.
- **Phase 2**: runtime is measured on one point before any grid; the three-arm grid is coarsened (not the window) if needed. `verify.py` samples across arms by verdict combination; if a verdict combination appears in only one arm, the record says so in § 13.
- **Phase 3**: if WI-030 lands with the R1 fallback (`B_peak` attribute), the constraint id is still `peak_field_ok`; nothing in this plan changes. If the computed beta misses the ±3.5% band, WI-030 does not close and this phase does not start.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-08-21 (owner approved the policy after one rewrite of § 10)
**Actual Changes:**
- `tests/study/test_policy_path.py` (NEW, 8 tests) and `tests/study/test_record_template.py` (NEW, 2 tests): written first; 5 failed / 4 errors on the unmodified tree, 10 pass after.
- `git mv .project/active/demo-study-parameterization-policy/policy.md modeling_project/STUDY_POLICY.md`; the empty directory removed. Header rewritten (Status "Ratified whole — [OWNER] 2026-08-21", consumers named, demo frame noted as on hold); § 3 and § 4 headings mark the ratification; § 6 heading drops "for Item 5"; § 7 H1 carries the search-framed scope and the sensitivity exemption; new § 9 "Axis forces and framing" (concept SC-2/SC-3, owner-grade, with the "indicators inform, never gate" rule and the finding obligation); new § 10 "Verification and the 1costingFE handshake" with the Align's two owner quotes verbatim and the retirement disposition.
- Live citations moved: `SKILL.md:74`, `runbook.md:9`, `run_design_search.py:13`, `.project/backlog/BACKLOG.md` (Active Work Items row struck through with the move note), `epic_run_study_capability.md` (3 sites), `CURRENT_WORK.md:41`, the three concept docs (path plus a one-line "moved 2026-08-21" note, history kept legible), this item's spec/design/align, `work/active/WI-030_…/spec.md`.
- `record-template.md:306-313` and `:371-374`: both `source_digest` blocks carry `files: [{path, sha256}]` with a comment saying why (G1).
- `briefs/administer-template.md` (NEW): Item 5's brief without the pre-capability waiver; adds the policy as vocabulary-only reading, the per-arm recovery list, and the hold-out prohibition.
- `tests/study`: 267 passed / 1 skipped with `STUDY_REQUIRE_TEAX=1`; ruff clean on the two new files.

**Issues Encountered:**
- The grep for the old path is not empty and cannot be: the policy's own status line, the concepts' "moved" notes, the test constant, and this plan all name it deliberately. The validation line now says so; the test checks the three live surfaces, which is the obligation.

**Deviations from Plan:**
- § 9 and § 10 were appended after § 8 (the append-only tripwire table) rather than renumbering; existing citations to § 7/§ 8 stay valid.
- The plan said "the rule-text paragraph for G1 updated"; the template has no separate G1 paragraph, only the in-block comment, which was extended.
- Owner review: § 10 as first drafted quoted the Align verbatim and read as confused; rewritten to the durable rules only (1costingFE is the validation reference when a direct comparison is possible and applicable, never a limit on the model; the oracle is a development check, retired from the study contract after Item 6). Test updated to the new wording.

### Phase 2 Progress (not complete) — 2026-08-21/22
**Done:** gate fully open (WI-030 landed on this branch as `ba5c9945`/`72dc7699`, so study 2 runs on the post-WI-030 package `7447efea…`, six constraints — the plan's "study 2 before WI-030" ordering is moot; both studies share one package). Record opened at `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/` with § 1–2 (owner intake verbatim, 2026-08-21), § 5 proposed, § 7, § 8 (rulings + two model-development findings), § 9 (preflight 6/6), § 10, § 11, § 14 (critique). `axes.json`, `indicators.json` (no subset), `results/{package_identity,baseline_result,preflight_results,oracle_scan}.json`, `study.py` (four arms, proposal builder, export). Seam edit: `studies/oracle_entry.py` maps the three block keys and `discount_rate` to oracle inputs. Manifest: `magnet_capital` objective added. `studies/.gitignore`: `*/_work/`.
**Owner rulings 2026-08-22:** availability and discount_rate "no sensitivity" → declined, not swept; fourth arm yes (`arm-sco2-eta-only`); econ sweeps at more geometries yes — conflicts with the first ruling; unresolved, see handoff.
**Not done:** runbook steps 9–15 (execution, verification, judgment, findings, discovery log, snapshot, commit) and the administrator. `study.py` still carries the availability / discount sweeps; remove or keep per the resolved ruling before step 9. Nothing under the record is committed.
**Handoff:** written 2026-08-22 to the OS temp dir (path in the session transcript).

### Phase 2 Completion
### Phase 3 Completion
### Phase 4 Completion

---

**Status**: Draft → In Progress → Complete
