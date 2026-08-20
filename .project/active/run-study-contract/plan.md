# Implementation Plan: Skill, Runbook, and Record Contract (RUN-STUDY Item 2)

**Status:** In Progress
**Created:** 2026-08-19
**Last Updated:** 2026-08-19
**Branch:** `feat/stellarator-mbse-demo`

## Source Documents

- **Spec:** `.project/active/run-study-contract/spec.md` (Accepted)
- **Design:** `.project/active/run-study-contract/design.md` (Accepted; review fixes MF1–MF7 + SF1–SF7 folded) ← component detail, section order, snapshot shape, invariants all live there
- **Item 3 design (field-name source):** `.project/active/run-study-indicators/design.md`
- **Procedural source:** `.project/active/demo-proof-of-life/plan.md`
- **Policy (cite at its current path):** `.project/active/demo-study-parameterization-policy/policy.md`

---

## The Point

One good study exists and none of what made it good is written where the next session must read it. The proof-of-life design search declared its axes at the attribute level, checked the expansion mechanically, proved the baseline point reproduces the pinned headline, verified sampled rows against an independent oracle, ran four review passes, and disclosed every value the harness supplied that the model did not. All of that lives in one finished work item's plan and one 450-line package-specific script.

Three owner pains follow. Quality regresses "if I don't phrase my prompt just the right way that got the executing agent to do what it did." There is no reproducibility floor, because no fixed list says what a study must record. And when a finished study looks wrong, "I have no idea where to begin to improve the process for better outcomes."

A fourth obligation is the seam between roles: "I prefer having sufficient structure in the artifacts from the executing study agent (e.g. context, goals, plan) so that another agent can effectively pick up the results and do the synthesis."

So what this work owes: a prompt carrying only a goal and a scope must put an agent on the proof-of-life's discipline, and the record that agent commits must let a second agent with no execution memory recover the framing per axis, the LCOE result, every named constraint outcome, and every finding — each traced to a committed artifact. **A fact the second agent cannot recover is a defect in this contract.** That is the bar every phase below is checked against.

This ladders into the RUN-STUDY epic's larger goal: study-driven model development, where a study that finds nothing pushing back on an axis produces a model-development finding rather than a heatmap.

---

## Implementation Strategy

**What this item produces:** three markdown documents under `.claude/skills/run-study/` and one line in `.gitignore`. No code. So "test-first" here means **the check comes before the document**: each phase writes its verification commands (grep gates, `git check-ignore`, two-way deposit reads) first, watches them fail on the absent or empty file, then writes the document until they pass. Where a check cannot be mechanized — "no sentence states a preference among framings" — the plan names it as a read-check with a stated reading procedure, not as a grep that pretends to cover it.

**Phasing rationale.**

1. **Tracking first, because it is five minutes and everything after it is untracked without it.** A draft template written into an ignored directory looks committed and is not.
2. **Then the de-risk the design named: the skeleton dry run.** Fill a draft template from the proof-of-life's real facts and see which sections have no source. This exercises B1 (cold recovery from fixed headings) and B2 (values/arguments split assigns every fact one home) against real material before any wording is finalized. Run the snapshot self-audit on a two-arm case in the same pass — MF2 was found precisely because the drawn shape was only checked against one arm.
3. **Then the snapshot field list**, written against Item 3's design with exact names copied, never invented. This is the one part of the work with an external dependency, and it carries a live naming seam (below) the phase must surface rather than paper over.
4. **Then the runbook**, whose deposits reference sections that by now exist and are known fillable.
5. **Then `SKILL.md`**, last of the three, because its failure mode is restating runbook steps and that is only checkable once the runbook exists.
6. **Then the contract checks and finalize**: the two-way deposit check, the spec-coverage remap, the grep gates run across all three finished files, and the dry-run gap list folded into the template.

**Critical path:** `.gitignore` → draft template → dry run → snapshot field list → runbook → skill → cross-checks.

**First proof point:** end of Phase 2. Either the proof-of-life's facts fill the seventeen sections with a short, honest gap list, or they don't — and if they don't, the template's structure is wrong while it is still cheap to change.

**Overall validation approach:** every phase ends with commands that either pass or name what failed. The three contract-wide checks (grep gates, deposit completeness, spec coverage) are re-run in Phase 6 against the final text, not trusted from the phase that wrote each file.

---

## Surfaced seam — read before Phase 3

**The design's `manifest.content_used.fingerprint_names` has no direct counterpart in Item 3's manifest schema.**

MF1's fix makes fingerprint completeness auditable from inside the record: the snapshot copies in "the list of fingerprint names the manifest declared," and the rule is *every name listed there appears as a key under `fingerprints`* (`design.md:269`).

But Item 3's manifest does not carry a flat list of fingerprint names. It carries a nested block (`.project/active/run-study-indicators/design.md:150-152`):

```jsonc
"fingerprints": {
  "indicator_inputs": {"recipe": "indicator-input-fingerprint/v1", "digest": "...", "files": [...]},
  "recorded_provenance": {"executable_fingerprint": "...", "semantic_fingerprint": "..."}}
```

So "the names the manifest declares" must be derived, not copied. **Plan's proposed resolution**, to be written into the template in Phase 3 and flagged for the owner rather than assumed settled: `fingerprint_names` holds dotted paths into the manifest's `fingerprints` block, and the snapshot's own `fingerprints` map is keyed by those same dotted paths:

```jsonc
"manifest": {"digest": "...", "schema_version": "study-package-manifest/v1",
             "content_used": {"fingerprint_names": ["indicator_inputs",
                                                    "recorded_provenance.executable_fingerprint",
                                                    "recorded_provenance.semantic_fingerprint"], ...}}
```

The MF1 rule then still holds verbatim, and the spec's floor (`spec.md:88`) maps cleanly: sealed → `recorded_provenance.executable_fingerprint`, semantic → `recorded_provenance.semantic_fingerprint`, indicator-input → `indicator_inputs`. Dependent conclusion parked: if the owner or Item 3 prefers a flat declared-names list in the manifest itself, that is a one-line manifest change and the snapshot copies it directly; the template's rule text does not change either way.

**Second flag:** Item 3's design is **Draft**, not accepted. Every field name Phase 3 copies is re-checked against that file at implement time, and any that moved is corrected there — not carried forward from this plan.

---

## Phase 1: Tracking Seam

### Goal

`.claude/skills/run-study/` exists and is trackable. One line in `.gitignore`, nothing else moves.

### Assumption Under Test

That a directory-form negation after line 23 makes git descend past `.claude/skills/*` for the new directory and changes no other skill's tracking status. The design calls this proven in-repo (`design.md:49`); this phase confirms it on the actual added line rather than by analogy.

### Check Stencil (Run This First)

```bash
# Before the edit — expect a HIT on line 21, proving the file is ignored today
git check-ignore -v .claude/skills/run-study/SKILL.md

# After the edit — expect NO output (exit 1) for the new skill...
git check-ignore -v .claude/skills/run-study/SKILL.md
# ...and still a hit on line 21 for an untracked neighbour
git check-ignore -v .claude/skills/pdf-analysis/SKILL.md

# No other skill's status moved
git status --porcelain .claude/skills/
```

### Changes Required

**See `design.md#implementation-notes`** for the exact line and the trailing-slash rationale (D10).

- [x] Capture `git status --porcelain .claude/skills/` output before the edit, as the comparison baseline
- [x] Add `!.claude/skills/run-study/` to `.gitignore` immediately after line 23
- [x] Create `.claude/skills/run-study/`

### Validation

- [x] `git check-ignore -v .claude/skills/run-study/SKILL.md` → no output
- [x] `git check-ignore -v .claude/skills/pdf-analysis/SKILL.md` → still reports `.gitignore:21`
- [x] `git diff .gitignore` → exactly one added line, zero removed
- [x] `git status --porcelain .claude/skills/` → identical to the baseline apart from the new directory

**What We Know Works After This Phase:** the tracking mechanism, on the real line, with no collateral change.

**Commits:** `.gitignore` (one line). The empty directory is not committable on its own; it lands with Phase 2's draft template.

---

## Phase 2: Skeleton Dry Run (De-Risk)

### Goal

Draft the record template's skeleton and a draft snapshot shape, fill both from the proof-of-life's real facts, and write down which sections have no source. Finalize nothing yet.

### Assumption Under Test

**B1 and B2 together.** B1: a cold reader can recover a study from fixed-heading prose plus one JSON file. B2: no required fact is genuinely both a resolved value and an argument, so every fact has exactly one home. The window is the case most likely to falsify B2 (`design.md:323`) and the dry run is where it either splits cleanly or doesn't.

Also under test: **MF2's arm scoping**, checked against a two-arm case, not just the one-arm case the shape was drawn against.

### Check Stencil (Write This First)

```
# The dry-run artifact IS the test. Its shape, written before filling anything:
#
# For each of the 17 sections:
#   §n <heading>  → SOURCE: <file:line in the proof-of-life material> | NO SOURCE: <why>
# For each drafted snapshot field:
#   <field>       → SOURCE: <where the proof-of-life recorded it> | NO SOURCE: <why>
#
# A section that fills only by inventing a fact = NO SOURCE. Filling it from
# memory of the proof-of-life session is exactly the failure this contract exists
# to prevent, and doing it here would hide the gap.
```

### Changes Required

**See `design.md#record-section-order`** for the seventeen headings and the two `**Applies:**` subsections in §6; **`design.md#snapshot-structure`** for the arm-scoping rule.

- [x] Write draft `.claude/skills/run-study/record-template.md`: seventeen headings verbatim, `**Applies:**` lines on §6's two conditional subsections, typed placeholder tokens (`<one-line goal, owner's words>`), no plausible-looking example values
- [x] Draft the snapshot shape as `design.md:241-263` draws it, with `arms[]` and `stores[]`
- [x] Fill the template against `exploration/stellarator_e2e/study/` (`verification_summary.json`, the two CSVs, `run_design_search.py`, `make_report.py`, `report.html`) plus `.project/active/demo-proof-of-life/plan.md` (phases at :39-65, review dispositions at :74-86, per-phase results at :92-103)
- [x] Record every unfillable section and field with its reason, in `.project/active/run-study-contract/dry-run.md`
- [x] **Two-arm snapshot self-audit**: hand-construct a two-arm case where the arms span fingerprints, and check that each arm carries its own `window`, `strategy`, `effective_executable_fingerprint`, `verification`, and `artifacts`; that both `store_id`s resolve into `stores[]`; and that nothing arm-varying sits at top level
- [x] Record in `dry-run.md` where the window's bounds/rationale split landed, as the B2 verdict

### Validation

- [x] Every one of the seventeen sections is either filled from a cited `file:line` or listed as NO SOURCE with a reason — no section left unaddressed
- [x] The two-arm audit produces either a clean pass or a named field that has no correct home
- [x] `dry-run.md` states the B2 verdict on the window in one sentence

**What We Know Works After This Phase:** whether the structure survives contact with the best study this project has run. Per `design.md:346`, a gap is the honest distance between the pre-capability record and the contract — it is input to Item 5, **not** a reason to soften the contract. Only a section that cannot be filled *by any compliant study* is a structural defect, and that is the finding this phase is hunting.

**Commits:** draft `record-template.md` + `dry-run.md`.

---

## Phase 3: Snapshot Field List, Written Out

### Goal

Replace the draft snapshot shape with the full field list, every externally-owned name copied from Item 3's design.

### Assumption Under Test

That Item 3's accepted seams name everything the snapshot needs, so no field has to be invented. The `fingerprint_names` seam above is the first place this is already known to strain.

### Check Stencil (Write This First)

```bash
# Every externally-owned token in the snapshot appendix must appear in Item 3's design.
# Run per token; a miss means it was invented and must be corrected or flagged.
for tok in study-indicators/v1 study-package-manifest/v1 study-axis-declaration/v1 \
           indicator-input-fingerprint/v1 tool-source-digest/v1 \
           indicator_inputs recorded_provenance executable_fingerprint semantic_fingerprint \
           objective_catalog groups_declared subset source_digest; do
  grep -qF "$tok" .project/active/run-study-indicators/design.md \
    || echo "NOT IN ITEM 3: $tok"
done
```

### Changes Required

**Home for the field list:** an appendix in `record-template.md` — "Appendix: `snapshot.json` shape." The template is where the record contract is stated, §16 stays a filename/digest/version stub per D2, and the executor reads one file rather than two. Recorded here because the design left the field list's location open.

Names to copy exactly (source: `.project/active/run-study-indicators/design.md`):

| Snapshot field | Item 3 source | Line |
|---|---|---|
| `manifest.schema_version` value `study-package-manifest/v1` | manifest schema root | `:147` |
| `fingerprints` keys (see the surfaced seam) | `fingerprints.indicator_inputs`, `fingerprints.recorded_provenance.{executable_fingerprint, semantic_fingerprint}` | `:150-152` |
| indicator-input digest + recipe id | `indicator_inputs.{recipe, digest, files}`, recipe `indicator-input-fingerprint/v1` | `:150-151`, `:162` |
| `manifest.content_used` — ties | `ties[]` as `{key, rides_with, note}` | `:154` |
| `manifest.content_used` — objective catalog | `objective_catalog[]` as `{name, channel, note}` | `:153` |
| `manifest.content_used` — baseline | `baseline.{point, headline.{channel, value}, verdicts[].{source_local_identity, expected}}` | `:155-156` |
| `manifest.content_used` — oracle | `oracle.{kind, module, callable, note}`, `kind: "python_callable"` | `:157` |
| `indicators.output_schema_version` value `study-indicators/v1` | report root `schema_version` | `:192` |
| `indicators.axis_declaration` | `{path, schema_version, digest, groups_declared, subset}`, schema `study-axis-declaration/v1` | `:203-204`, `:247` |
| `tools[].revision` for `indicators.py` | `tool.source_digest.{recipe, digest}`, recipe `tool-source-digest/v1` | `:194`, `:168` |
| package identity fields | `package.{path, package_name, semantic_fingerprint, recorded_executable_fingerprint}` | `:195-199` |

- [x] Write the appendix with the arm-scoping rule stated once at the top (`design.md:239`), then the full literal shape
- [x] Write the five snapshot rules from `design.md:267-273` as prose beneath it — internal fingerprint completeness, `effective_executable_fingerprint`'s three inputs or its nil, stores-by-id, `arms[].verification`'s value half, `glue_ledger: []` with `glue_ledger_none: true`
- [x] Record the snapshot's `indicators.axis_declaration.subset` expectation: a record-feeding run is `false` (Item 3 Invariant 11, `:135`); a snapshot carrying `subset: true` is a defective record
- [x] Write the `fingerprint_names` dotted-path resolution and mark it as the plan's proposal awaiting owner confirmation
- [x] Delete the draft shape; one home only

### Validation

- [x] The `grep -qF` loop above prints nothing
- [x] The spec's three floor fingerprints (`spec.md:88`) each map to a named snapshot key, stated in the appendix
- [x] Every `spec.md:87-98` snapshot bullet appears in the appendix or is explicitly homed in `record.md` with the section named (the SF1 window split is the only one)
- [x] Re-run Phase 2's two-arm audit against the final shape

**What We Know Works After This Phase:** the snapshot names real fields, and the one place it doesn't is flagged loudly rather than resolved silently.

**Commits:** `record-template.md` (draft body + snapshot appendix).

---

## Phase 4: `runbook.md`

### Goal

Fourteen execute steps in the four-line micro-schema, plus the administer sequence, the discovery-log row format, and the `synthesis.md` convention.

### Assumption Under Test

**B4** — the universal/annex split holds: every step states its obligation without package specifics, and what is package-specific is behind an annex link. If the runbook needs a stellarator fact to be executable, the split is in the wrong place.

### Check Stencil (Write This First)

```bash
RB=.claude/skills/run-study/runbook.md

# B4, mechanized as far as it goes: zero package specifics
grep -inE 'stellarator|stellaris|mfe_stellarator|magnet__|geom__|rb__|lcoe_calc__' $RB

# Policy path: current only
grep -n 'STUDY_POLICY' $RB          # expect nothing
grep -c 'demo-study-parameterization-policy/policy.md' $RB   # expect >= 1

# Every step deposits somewhere
grep -c '^\*\*Deposits:\*\*' $RB    # expect 14
grep -c '^### ' $RB                 # expect 14 execute steps
```

### Changes Required

**See `design.md#runbookmd`** for the micro-schema and the fourteen steps; **`design.md#discovery_logmd-row`** for the row; **`design.md#synthesismd`** for its sections.

- [x] Write the fourteen execute steps in the `**Calls:** / **Deposits:** / **Fails closed when:** / **Annex:**` schema, in the design's order
- [x] Step 4 deposits **twice**: §5 first half (framing as proposed) + §8, and its pre-execution critique verdict into §14 as a named review outcome (MF7a, discharging `spec.md:82`)
- [x] Step 10 is the post-run framing judgment feeding §5's second half (MF7b, discharging `spec.md:77`)
- [x] Step 7 carries the glue disclosure into §10 — never §17 (MF4)
- [x] Step 12's report states the era pin as a reproduce prerequisite at the claim site while the pin exists (SF6)
- [x] Annex links only on package-specific steps, at `exploration/<pkg>/studies/ANNEX.md § <topic>` (D9). Item 4 authors the content; this is the link only
- [x] Indicator vocabulary used exactly as `spec.md:58` fixes it — `no_constraint_response` sound negative, `constraints_reachable` a possible path, `unresisted` an agent judgment
- [x] `**Fails closed when:**` names only mechanical conditions; an interpretive condition never gates (`spec.md:60`)
- [x] Administer sequence as a second ordered list in the same file (per the handoff: start with one file): read the record directory only → recover the fresh-administrator facts → write `synthesis.md` → state what the record does not support. It ends there; no discovery-log row (MF6)
- [x] `synthesis.md` header + sections per `design.md:190-192`, including the mandatory "What the record does not support"
- [x] `DISCOVERY_LOG.md` six-column row format, `<study-id>#<n>` join key, `Home` never blank (`unrouted` is a stated state)
- [x] Study id convention `<YYYYMMDD>-<goal-slug>`, same-day collisions `-b`, `-c` (D3); arms as `arm-<slug>` (D4)

### Validation

- [x] All four check-stencil greps give the expected results
- [x] **Read-check for judgment**: read every step's imperative and confirm none states a preference among axes, framings, routes, or results. "Argue and record the framing" is in bounds; "prefer search framing" is not. Record the reading in the phase notes — this is not greppable
- [x] Every `**Deposits:**` target names a heading that exists in the Phase 2/3 template (first direction of the two-way check; the second direction runs in Phase 6)

**What We Know Works After This Phase:** the obligation set is complete, package-free, and lands every output somewhere.

**Commits:** `runbook.md`.

---

## Phase 5: `SKILL.md`

### Goal

The entry point: frontmatter, roles, explicit mode selection, intake capture, record-path naming, pointers out. Under ~90 lines.

### Assumption Under Test

That the skill can be useful while carrying no step. Its named failure mode is restating runbook steps (`design.md:145`).

### Check Stencil (Write This First)

```bash
SK=.claude/skills/run-study/SKILL.md
wc -l $SK                                    # expect < ~90
grep -inE 'stellarator|stellaris|magnet__'   $SK   # expect nothing
grep -n 'STUDY_POLICY' $SK                          # expect nothing
head -14 .claude/skills/browser-inspect/SKILL.md    # frontmatter convention to match
```

### Changes Required

**See `design.md#skillmd`** for the body order and `design.md:51` for the local frontmatter convention.

- [x] Frontmatter: `name`, multi-line trigger-carrying `description`, `allowed-tools`, `user-invocable: true`, matching `browser-inspect/SKILL.md:1-14`
- [x] Body: what a study is (two sentences); the three roles, one line each (`spec.md:50`); mode selection as an explicit question, never guessed; intake capture stated as collaborative and flexible — "study whatever you can find" through to a named parameter list, no fixed questionnaire; record-path naming (D6, both directions — execute names it, administer is given it); pointers to `runbook.md`, the policy at its current path, and `scripts/study/`
- [x] No `scripts/study/` tool is invoked by the skill directly (`design.md:331`)

### Validation

- [x] Check-stencil greps pass; line count under ~90
- [x] **Read-check for step-shaped sentences**: any sentence in `SKILL.md` that reads as a runbook step is a defect (`design.md:145`). Read the file against `runbook.md` and confirm zero overlap of content, only a pointer
- [x] The record path is named in exactly one of the two files — `SKILL.md` owns it, `runbook.md` step 1 references it

**What We Know Works After This Phase:** a goal-only prompt has a landing place that routes without deciding anything (spec SC1).

**Commits:** `SKILL.md`.

---

## Phase 6: Contract Checks and Finalize

### Goal

Run the design's Validation Approach across the three finished documents, fold the Phase 2 gap list into the template, and produce the spec-coverage map as a committed artifact.

### Assumption Under Test

**B3** — fixed heading text is a strong enough contract that a reader can tell a missing section from a nil-discharged one, before any linter exists. Also the last chance to catch a spec item with no home or two homes.

### Check Stencil (Write This First)

```bash
D=.claude/skills/run-study
# Grep gates across all three, final text
grep -rinE 'stellarator|stellaris|mfe_stellarator|magnet__|geom__|rb__|lcoe_calc__|verify_stellaris' $D
grep -rn 'modeling_project/STUDY_POLICY.md' $D
grep -rn '<pkg>' $D | head            # placeholders present, not literals
# Template structural contract
grep -c '^## ' $D/record-template.md  # expect 17 top-level record sections
grep -c '^\*\*Applies:\*\*' $D/record-template.md   # expect 2 (§6's subsections)
# Tracking, re-confirmed on the final tree
git check-ignore -v $D/SKILL.md $D/runbook.md $D/record-template.md   # expect nothing
git status --porcelain $D             # expect all three tracked/added
```

### Changes Required

- [ ] Fold `dry-run.md`'s findings into `record-template.md` — wording and placeholder fixes only. A section the proof-of-life could not fill is **not** removed; the contract is not softened (`design.md:346`)
- [ ] **Deposit completeness, two-way** (`design.md:343`): every runbook `**Deposits:**` names a template section that exists (Phase 4 direction, re-run on final text), **and** every template section is named by at least one runbook step or is header/nil material. Read both files side by side; record the pairing table in the phase notes
- [ ] **Spec-coverage remap** (`design.md:344`): re-derive the mapping of each of the spec's fourteen mandatory content items (`spec.md:71-100`) to exactly one home — a template section, a snapshot block, or a stated split. Items 9 and 10 are the two split cases. Write the finished map to `.project/active/run-study-contract/coverage.md`. Re-derive it from the written documents; do not copy `design.md`'s table forward, since that would only prove the design agrees with itself
- [ ] Confirm the template header states the values/arguments split once, with the window as the worked example (`design.md:323`)
- [ ] Confirm the routing homes in §15 guidance are the set `{tool, runbook step, policy rule, skill, modeling item, research round, documented seam}` — not the proof-of-life's specific rows, which are spec history (`design.md:314`)
- [ ] Confirm no unreplaced-token exception: the template says an unreplaced `<...>` in a committed record is a commit-blocking defect

### Validation

- [ ] All check-stencil commands give expected results
- [ ] `coverage.md` maps all fourteen spec items; zero items with no home; zero items with two homes except the two declared splits
- [ ] Deposit pairing table has no orphan on either side
- [ ] **Read-check, no judgment**, across all three files: zero sentences stating a preference among axes, framings, routes, or results
- [ ] Every invariant in `design.md#required-invariants` is either checked above or explicitly listed in the phase notes as "stated in the documents, unenforced" — with `record_lint.py` named as the future home and owned by no item (`design.md:321`)

**What We Know Works After This Phase:** the contract is internally consistent, spec-complete, and package-free. What still does **not** work, and is honestly out of reach here: the **fresh-administrator check**, the real acceptance test, which needs a compliant record and arrives with the first consumer study (`design.md:347`).

**Commits:** final `record-template.md`, `coverage.md`, and phase notes. `dry-run.md` stays as committed evidence of the de-risk pass.

---

## Environment Setup

No new dependencies; this item writes markdown. **See CLAUDE.md** for the `uv run` rule if any incidental script is needed. Git operations only.

---

## Risk Management

**See `design.md#potential-risks`** for the full analysis.

**Phase-specific mitigations:**

- **Phase 1** — collateral tracking change. Mitigated by capturing `git status --porcelain .claude/skills/` as a baseline *before* the edit and diffing after; `spec.md:38` is `[HARD]` that no other skill moves.
- **Phase 2** — the dry run tempts a softening of the contract when a section won't fill. Mitigated by stating the rule in the phase's own acceptance: a gap is Item 5 input, not a template edit.
- **Phase 3** — Item 3's design is Draft; field names may move. Mitigated by the `grep -qF` loop, which fails loudly on any name Item 3 does not carry, and by re-running it at implement time rather than trusting this plan's table.
- **Phase 3** — the `fingerprint_names` seam. Surfaced above with a proposed resolution and parked as owner-confirmable; not resolved silently in either direction.
- **Phase 4** — the annex path is pinned by this design (`exploration/<pkg>/studies/ANNEX.md`) but Item 4 authors the file. If Item 4 moves it, that is a one-file link update. **Flagged as a cross-item dependency** per `design.md:324`; note it in the epic when Phase 4 commits.
- **Phase 5** — skill bloat into runbook territory. Mitigated by the read-check against the finished runbook and the ~90-line target.
- **Phase 6** — nothing mechanically enforces the record contract, and this plan does not create a linter (`design.md:304`). Mitigated by naming every unenforced invariant explicitly in the phase notes, so the gap is recorded rather than assumed covered.

---

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion

**Completed:** 2026-08-19

**Changes Made:**
- `.gitignore:24` — added `!.claude/skills/run-study/` immediately after line 23. One added line, zero removed.
- Created `.claude/skills/run-study/`.

**Checks run:**
- Before the edit, `git check-ignore -v .claude/skills/run-study/SKILL.md` reported `.gitignore:21:.claude/skills/*` (exit 0) — the file was ignored.
- After the edit, the same command exits 1 with no output; `git check-ignore -v .claude/skills/run-study` reports the new `.gitignore:24` negation, which is git descending past the star as designed (D10).
- Neighbour check on three untracked skills (`pdf-analysis`, `model-validation`, `toolkit-awareness`) still reports `.gitignore:21`. No other skill's tracking status moved.
- `git status --porcelain .claude/skills/` was empty before the edit and empty after (the new directory is empty until Phase 2 writes into it), matching the baseline.

**Deviations from Plan:**
- The plan's neighbour check names `.claude/skills/pdf-analysis/SKILL.md`. That path errors with `fatal: pathspec ... is beyond a symbolic link` — every skill in this repo other than the two tracked ones is a symlink into `~/1cfe/agentic-mbse/claude/skills/`. The check was run against the symlink path itself (`.claude/skills/pdf-analysis`), which is the same assertion and does resolve. Same substitution applies to Phase 6's re-confirmation.
### Phase 2 Completion

**Completed:** 2026-08-19

**Changes Made:**
- Created draft `.claude/skills/run-study/record-template.md` — seventeen `## ` headings verbatim in the design's order, `**Applies:**` lines on §6's two conditional subsections, typed placeholder tokens throughout, no plausible-looking example values. Header states the values/arguments split with the window as the worked example, the fixed-heading rule, the explicit-nil rule, `/show-me` weight, the unreplaced-token defect, and the append-only addendum rule.
- Added the draft snapshot shape as the template's appendix, marked DRAFT and replaced in Phase 3. It lives in the appendix rather than in `dry-run.md` so that Phase 3's "delete the draft shape; one home only" does not have to edit committed evidence.
- Created `.project/active/run-study-contract/dry-run.md` — the section-by-section fill against the proof-of-life, the tally, the B1 and B2 verdicts, and the two-arm snapshot self-audit.

**Check stencil, run before the fill:** two structural counts failed on the first draft and were fixed before the fill proceeded.
- `grep -c '^## '` returned 18, not 17 — the snapshot appendix was authored at `## `. Demoted to `### ` under the `# Template guidance` heading, which also makes the appendix visibly template material rather than a record section.
- `grep -c '^**Applies:**'` returned 3, not 2 — §12 (cross-fingerprint correlation) had been given an `**Applies:**` line too. §12 is arm-conditional, not framing-conditional; its nil is discharged in prose by naming the condition, per the explicit-nil rule. `**Applies:**` is now reserved for the framing-conditional subsections, which is what D5 assigns it to.

**Dry-run outcome.** Eight sections fill from a committed artifact; three fill by mapping or extraction; four are partial; two (§8 indicators, §16 snapshot) are largely or wholly unsourced. **No section is a structural defect** — every gap traces to a capability the proof-of-life predates, or to a fact that existed and was dropped on export. Nothing in the template was softened. The clearest single case of what the contract adds is §4: `short_verdicts()` (`run_design_search.py:298`) truncated the qualified constraint id before export, so the committed CSVs carry short names only and the qualified identity was lost. §10's glue disclosure was the strongest confirmation — the script's `GLUE LEDGER` docstring block is already in §10's exact shape.

**B1 verdict.** Holds. The exercise found no fact the two files could not hold, and found four facts the proof-of-life *had* and lost for want of a heading.

**B2 verdict on the window.** Holds, and it is stated in one sentence in `dry-run.md`: the proof-of-life, with no contract telling it to, already put the bounds (`run_design_search.py:123-125`) and the scan story (`demo-proof-of-life/plan.md`, Phase 1 result) in two different places.

**Two-arm self-audit — one field flagged.** Constructed a cross-fingerprint A/B (`arm-sealed` vs `arm-adapter`). Every arm-scoped field passed and every `store_id` resolved. **`glue_ledger` has no correct home at top level**: in a sealed-vs-adapter A/B, glue is exactly what differs between the arms, and that difference is the point of the comparison. The design's own scoping rule ("any field that can differ between arms is arm-scoped") puts it under `arms[]` with a per-arm `glue_ledger_none: true` nil. `design.md:258`'s sketch shows it top-level, which the design labels illustrative while the scoping rule at `design.md:239` is normative — so this is the rule being applied, not a design change. Phase 3 writes it arm-scoped. Same class of miss as MF2, found by the same method.

**Deviations from Plan:**
- The two structural fixes above, both made in response to the check stencil rather than after it.
- Recorded, not a deviation: the proof-of-life ran two studies (grid + availability sweep), which under the contract are two records rather than two arms of one — arms are variants of the same question. `dry-run.md` states this up front so a reader coming from the proof-of-life is not surprised.
### Phase 3 Completion

**Completed:** 2026-08-19

**Changes Made:**
- Replaced the draft snapshot shape in `record-template.md`'s appendix with the full field list. Every externally-owned name is copied from `.project/active/run-study-indicators/design.md` and marked `(Item 3)` inline, so a future reader can see which names are not this contract's to rename.
- Wrote the six rules that govern the snapshot beneath it: internal fingerprint completeness with the floor table, `effective_executable_fingerprint`'s three inputs or its nil, stores-by-id, `arms[].verification` as the values half only, the arm-scoped glue ledger with its `glue_ledger_none: true` nil, and `subset: false` in any record-feeding run.
- Deleted the draft shape. One home only.

**Check stencil:** the `grep -qF` loop printed nothing — all thirteen externally-owned tokens are present in Item 3's design at implement time. Item 3's design header now reads **Accepted**, not Draft, so the plan's second flag is discharged; the field shapes were re-read at `design.md:147-157` (manifest) and `:192-204` (report) rather than trusted from the plan's table, and every one matched.

**One naming detail worth recording.** The manifest's `fingerprints.indicator_inputs.files` is a list of plain path strings, while the indicator report's `package.indicator_input_fingerprint.files` is a list of `{path, sha256}` objects. The snapshot copies the richer form, since a per-file digest is what makes the pin auditable from inside the record.

**The `fingerprint_names` seam is resolved, not parked.** The orchestrator ruled 2026-08-19 that the list is **derived at snapshot time** by flattening Item 3's manifest `fingerprints` block to dotted-path names — `indicator_inputs`, `recorded_provenance.executable_fingerprint`, `recorded_provenance.semantic_fingerprint` — with **no Item 3 manifest change**. The appendix states it that way and cites the ruling. The plan's "awaiting owner confirmation" marker is therefore not written; MF1's rule text is unchanged either way, as the plan anticipated.

**`glue_ledger` moved to `arms[]`,** carrying forward Phase 2's two-arm audit finding. `design.md:258`'s sketch shows it top-level; `design.md:239`'s scoping rule is normative and puts it under `arms[]`, because a sealed-versus-adapter A/B differs in exactly this field. The rule's `glue_ledger_none: true` nil is now per arm.

**Validation:**
- Three floor fingerprints each map to a named snapshot key, stated as a table in the appendix.
- All eleven of `spec.md:87-98`'s snapshot bullets have a home. Ten land in the appendix; the SF1 split is the only one homed across two files, and the appendix names it at the field (`window` carries bounds and provenance; "how it was chosen" is `record.md` §11).
- Two-arm audit re-run against the final shape: every arm-scoped field passes, both `store_id`s resolve, and the one field that had no correct home now has one.
- `grep -c '^## '` still 17 and `grep -c '^**Applies:**'` still 2 — the appendix sits under the template-guidance heading and does not disturb the record's structural counts.

**Deviations from Plan:**
- The plan's `- [ ] Write the fingerprint_names dotted-path resolution and mark it as the plan's proposal awaiting owner confirmation` was executed without the awaiting-confirmation marker, because the orchestrator ruling settled it. Recorded above rather than left implicit.
### Phase 4 Completion

**Completed:** 2026-08-19

**Changes Made:**
- Wrote `.claude/skills/run-study/runbook.md`: a preamble fixing the rulebook path, the record path, the annex path, what "fails closed" means, and the indicator vocabulary; fourteen execute steps in the four-line micro-schema in the design's order; the administer sequence; the `synthesis.md` convention; the `DISCOVERY_LOG.md` row; and the study-id and arm-id naming rules.
- Step 4 deposits three ways on one line: §5 (framing as proposed), §8 (rulings and the model-development findings), and §14 (the pre-execution critique verdict) — MF7a.
- Step 10 is the post-run framing judgment feeding §5's second half — MF7b — and also writes §6's per-axis account, which the judged framing is what determines.
- Step 7 carries the glue disclosure into §10 and nowhere else — MF4.
- Step 12 states the era pin as a reproduce prerequisite at the claim site, not only in a provenance footnote — SF6.
- Annex links land on the six package-specific steps only (2, 5, 6, 7, 8, 9), at `exploration/<pkg>/studies/ANNEX.md § <topic>`. Item 4 authors the content; these are links.

**Check stencil:** zero package specifics, zero `STUDY_POLICY` references, one citation of the policy at its current path, `**Deposits:**` count 14, `### ` count 14. The `### ` count came back 15 on the first write — `synthesis.md` had been given a `### ` heading inside the administer section. Demoted to `####`, which is also the right level for it: it is a convention the administer sequence uses, not an execute step.

**Deposit completeness, direction one — a real orphan found and fixed.** A script pairing every `**Deposits:**` target against the template's `## <n>. <heading>` lines found §15 Findings named by no step. Step 14 had been written as "append the discovery-log rows" and deposited only into the log, so the record's own findings register had no depositing step and the log rows would have had nothing to join to. Step 14 is now "Register the findings and append the discovery-log rows" and deposits §15 + `DISCOVERY_LOG.md`. Re-run: zero orphans in either direction. Step count stayed at fourteen.

**Read-check for judgment — the reading, recorded.** Read all fourteen imperatives against the bar "argue and record the framing is in bounds; prefer search framing is not." Four sentences were weighed and all four are obligations rather than preferences:
- Step 6, "an engineered window is not a defect; an undisclosed one is" — a rule about disclosure, and it takes no side between `engineered` and `sourced`.
- Step 7, "two routes, and no third", with a clause each on what the routes can run — capability statements, not a ranking. The step requires the choice to be argued and does not make it.
- Step 8, "no hand-rolled sweep loop" — a policy obligation about how points execute, not a preference among results.
- Step 11, "correctness, honesty, and readability are the lenses a study normally owes" — a floor on review coverage. It states no preference among axes, framings, routes, or results.
No sentence states which axis to sweep, which framing is right, which route fits, or what a result means. The preamble says so outright so a reader knows the file's stance before step 1.

**Cross-item dependency flagged.** The annex path `exploration/<pkg>/studies/ANNEX.md` is pinned by this design (D9) and Item 4 authors the file. If Item 4 moves it, six `**Annex:**` lines in one file need updating. Noted here for the epic per `design.md:324`.

**Deviations from Plan:** none beyond the two fixes above, both made in response to a check rather than after one.
### Phase 5 Completion

**Completed:** 2026-08-19

**Changes Made:**
- Wrote `.claude/skills/run-study/SKILL.md`, 77 lines. Frontmatter matches the local convention at `browser-inspect/SKILL.md:1-14` — `name`, a multi-line trigger-carrying `description`, `allowed-tools`, `user-invocable: true`. Body in the design's order: what a study is in two sentences; the three roles with one line each; mode selection stated as an explicit question with the cost of guessing wrong; intake capture as collaborative and flexible with no questionnaire; record-path naming in both directions; then pointers to `runbook.md`, `record-template.md`, the policy at its current path, and `scripts/study/`.
- The skill invokes no tool. The `scripts/study/` pointer says outright that runbook steps call them and the skill never does.

**Check stencil:** 77 lines (under the ~90 target), zero package names, zero `STUDY_POLICY` references. The skill registered cleanly in the session's skill list on write, which confirms the frontmatter parses.

**Read-check for step-shaped sentences — two overlaps found and fixed.** Read `SKILL.md` against the finished `runbook.md`:
- `SKILL.md`'s "Capture the intake" sat next to runbook step 1, then titled "Open the record and capture intake verbatim". Two files appeared to own capturing intake. The division is real and is now visible: the skill **elicits** intake from the user, the runbook **deposits** what was elicited. Step 1 is retitled "Open the record and deposit the captured intake" and now says it copies the template to the record path `SKILL.md` named.
- The study-id convention `<YYYYMMDD>-<goal-slug>` was written out in both files. It now has one home, `runbook.md § Naming`, which is also where the same-day collision rule and the arm-id rule live; `SKILL.md` mints the id by citing that home. The skill still owns the *act* of naming, per D6.

After the fixes: `SKILL.md` names no record section number, carries no deposit, calls no tool, and states no obligation the runbook states. The overlap is a pointer only.

**Record path, one owner:** `SKILL.md` names it. `runbook.md`'s preamble and step 1 reference it as already named. Both directions of D6 are stated in `SKILL.md` — execute mints it, administer is given it and confirms it.

**Deviations from Plan:** none beyond the two read-check fixes.
### Phase 6 Completion

---

**Status**: Draft → In Progress → Complete
