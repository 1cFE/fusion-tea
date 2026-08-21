# Design: Skill, Runbook, and Record Contract (RUN-STUDY Item 2)

**Status:** Accepted (orchestrated review, 2026-08-19) — review fixes folded (design review 2026-08-19: MF1–MF7, SF1–SF7)
**Owner:** Reid W
**Created:** 2026-08-19
**Updated:** 2026-08-19
**Branch:** `feat/stellarator-mbse-demo` @ `573c7c79`
**Spec:** `.project/active/run-study-contract/spec.md` (Accepted)

---

## Overview

Design the file architecture for the `run-study` capability's three human-readable documents — the skill, the universal runbook, and the record template — plus the discovery-log row format, the `synthesis.md` convention, and the one-line `.gitignore` change. The content set is settled by the spec; this design fixes where each fact lives, in what shape, and under what heading.

---

## Related Artifacts

- **Spec:** `.project/active/run-study-contract/spec.md`
- **Epic:** `.project/backlog/epic_run_study_capability.md` — Item 2
- **Required Reading:**
  - `.project/concepts/run-study-skill-design.md` — Core Model, Design Principles, Required Invariants
  - `.project/concepts/run-study-skill.md` — owner-verbatim intent
  - `.project/active/demo-proof-of-life/plan.md` — validated procedural source
  - `.project/active/demo-study-parameterization-policy/policy.md` — the rulebook (Draft, current path)
- **Item 3 seam:** `.project/active/run-study-indicators/spec.md` — manifest fields, output schema versioning
- **Item 1 spike:** `.project/active/run-study-reachability-spike/findings.md`
- **Product-lens:** `.project/active/run-study-contract/product-lens.md`
- **Design review:** `.project/active/run-study-contract/design-review.md` — APPROVE-WITH-FIXES; MF1–MF7 and SF1–SF7 are folded into this revision, each marked at its landing site.
- **Decision records:** `.project/adr/` is absent — 0 entries, no index to check. `adr.sh` is also absent; the gap is noted, no ids hand-minted (same finding as `run-study-skill-design.md:84`).

---

## The Point

**[INHERITED: concept, [OWNER-VERBATIM]]** Three owner pains drive this item. Quality regresses "if I don't phrase my prompt just the right way that got the executing agent to do what it did." There is no reproducibility floor, because no fixed list says what a study must record. And when a finished study looks wrong, "I have no idea where to begin to improve the process for better outcomes."

**[INHERITED: concept, [OWNER-VERBATIM]]** The fourth obligation is the seam between roles: "I prefer having sufficient structure in the artifacts from the executing study agent (e.g. context, goals, plan) so that another agent can effectively pick up the results and do the synthesis."

So the obligation this design serves: a prompt carrying only a goal and a scope must put an agent on the proof-of-life's discipline, and the record that agent commits must let a second agent with no execution memory recover the framing per axis, the LCOE result, every named constraint outcome, and every finding — each traced to a committed artifact. A fact the second agent cannot recover is a defect in this contract.

This ladders into the RUN-STUDY epic's larger goal: study-driven model development, where a study that finds nothing pushing back on an axis produces a model-development finding rather than a heatmap.

---

## Research Findings

**The `.gitignore` mechanism is proven in this repo.** `.gitignore:21` is `.claude/skills/*`; lines 22–23 negate `browser-inspect/` and `concept-research-navigation/`, and both are tracked and present on disk. Twelve skill directories exist under `.claude/skills/`; ten are untracked. A directory-form negation is what makes git descend past the star. One added line reproduces the working pattern exactly.

**Skill file shape.** `.claude/skills/browser-inspect/SKILL.md:1-14` is the local convention: YAML frontmatter with `name`, a multi-line `description` carrying trigger phrases, `allowed-tools`, and `user-invocable`. Body is short prose with a "When to Use This" section and a numbered core workflow. Both tracked skills are single-file; `run-study` will be the first multi-file skill directory in this repo.

**Source material shape.** `.project/active/demo-proof-of-life/plan.md` carries the procedural content in three forms: numbered phases with checkboxes (lines 39–65), a review-pass block with numbered dispositions (lines 74–86), and an implementation record with per-phase result paragraphs (lines 92–103). Its review passes are already recorded as named lenses with dispositions (plan critique, correctness, honesty/claims, readability/visual), not as a count — the spec's `[NEED]` for named outcomes is a distillation of a form that already worked.

**Study directory today.** `exploration/stellarator_e2e/study/` holds `run_design_search.py`, `make_report.py`, `report.html`, two CSVs, and `verification_summary.json`. No `record.md`, no snapshot, no directory-level structure. It stays where it is as the pre-capability record (spec `[HARD]`).

**Item 3 seam, as accepted.** The manifest pins an **indicator-input fingerprint** computed over `pipelines/*.yaml`, `inputs/*.json`, `contracts/model_contract.json` as they exist on disk (`run-study-indicators/spec.md:40`), and additionally carries the sealed `executable_fingerprint` and the `semantic_fingerprint` as recorded provenance (`:42`). The indicator output JSON schema is documented and versioned as a fixed seam for Items 2 and 4 (`:33`). Both facts land in the snapshot design below.

---

## Core Concept

The record is one directory with a strict division of labor between two files: **`snapshot.json` holds resolved values and digests; `record.md` holds arguments and judgments; neither restates the other.** Everything else in this design follows from that split.

The split is the design's Principle 1 ("obligations are formal; decisions are not") applied to file boundaries. A fingerprint, a window's bounds, a store's compatibility tuple, a per-file digest — these are facts a checker should parse and a human should skim past. Why that window was chosen, why that route, what the boundary means, what the model fails to resist — these are arguments a human must read and no checker can validate. Putting them in one file forces every fact to be either awkwardly narrated or buried; putting them in two files with a stated rule means each fact has exactly one home, which is Principle 5 applied one level down.

On top of the split sit two conventions that make omission visible. **Stable heading text**: `record.md` ships as a fill-in skeleton whose headings are fixed, so a cold reader finds each fact by name and a missing fact is a missing heading, not a judgement call. **The explicit-nil rule**: every conditional obligation is discharged by content *or* by a stated nil that names the condition — "not applicable: `availability` is sensitivity-framed", "glue ledger: none", "single fingerprint — no cross-arm correlation needed". Silence never discharges anything. That one rule covers framing-conditional sections, the glue ledger's explicit "none", the no-adapter case, and cross-fingerprint correlation, so the template does not need four separate mechanisms.

The runbook sits above this as a list of obligations, each naming what it deposits into which record section. The skill sits above the runbook as an entry point that captures intake, picks the mode, names the record path, and points onward. Neither restates the other, and neither carries a judgment.

---

## Key Bets

- **B1.** A cold session can recover a study from fixed-heading prose plus one JSON file, without execution memory. *If false → administer mode is unreliable on compliant records, and `record.md` itself has to become machine-structured data, which would push the executor's arguments out of prose and lose what makes the record readable.*
- **B2.** No required record fact is genuinely both a resolved value and an argument, so the values/arguments split assigns every fact exactly one home without residue. *If false → the same fact lands in both files, drifts, and the record starts lying about itself — the failure Principle 5 exists to prevent.*
- **B3.** Fixed heading text is a strong enough structural contract that a human reader can tell a missing section from a nil-discharged one, before any linter exists. *If false → records drift structurally, cold pickup degrades study by study, and the contract needs a checker tool that no epic item currently owns.*
- **B4.** The universal/annex split the spec drew holds for a second package. Every step the runbook states without package specifics is one another package could execute. *If false → the runbook silently encodes stellarator assumptions, and the first non-stellarator study discovers them by failing.*
- **B5.** A record can be audited for completeness from inside itself — every rule the contract states can be evaluated by a reader who opens nothing outside the record directory. *If false → the fresh-administrator check cannot certify a record, and completeness rules have to be enforced upstream by a tool the executor runs, moving the guarantee out of the contract and into an unowned checker.* (Surfaced by design review; it is the bet MF1 caught this design falsifying, and the `manifest.content_used.fingerprint_names` copy is what restores it.)

---

## Key Decisions

- **D1. `record-template.md` ships as a fill-in skeleton, not a checklist.** The executor copies it to `<study-id>/record.md` and fills it in. *Rejected: a checklist the executor writes prose against (the record's structure would then depend on the executor's habits, and the fresh-administrator check would have nothing stable to find facts by).*
- **D2. Snapshot lives in a sibling `snapshot.json`; `record.md` § Snapshot carries only its filename, sha256, and schema version.** The field set is open-ended (every fingerprint the manifest names), which prose cannot enumerate; the content is digests and tuples, which is what a checker reads and a human skips. Human readability is not lost, because the *interpretive* facts a human needs — window rationale, route rationale, glue disclosure — stay in `record.md` sections of their own. *Rejected: the full snapshot inline in `record.md` (unenumerable field set, and it buries the argument sections under two pages of hashes); rejected: both, with the JSON normative and a prose summary (two copies of the same fact drift — capture-fidelity §3).* **Amended by MF2:** the snapshot is arm-scoped, not a single-arm block — see Snapshot Structure below.
- **D3. Study id is `<YYYYMMDD>-<goal-slug>`.** Date-prefixed sorts the studies directory chronologically; the slug makes it recognizable. On a same-day collision the first study is unsuffixed and subsequent ones append `-b`, `-c` (SF7). *Rejected: fingerprint-tagged (an A/B study can span fingerprints, so a single-fingerprint tag in the id would be false); rejected: slug-only (no ordering, and re-running the same goal collides).*
- **D4. A/B arms share one record directory and one `record.md`, distinguished by a stable `arm-<slug>` id used identically in record subsections, snapshot store entries, and result filenames.** The design requires the comparison to live in the record and never in a merged store; sibling directories would put the comparison outside any single record. *Rejected: one directory per arm plus a comparison directory (three records, no single cold-readable artifact).* **Amended by MF2:** every snapshot field that can differ between arms is arm-scoped, so a cross-fingerprint A/B fits the shape.
- **D5. The explicit-nil rule, one convention for every conditional obligation.** Every framing-conditional section ships present in the skeleton with a required `**Applies:**` line directly under its heading; nil discharge must name the condition. *Rejected: deleting non-applicable sections (omission and forgetting become indistinguishable); rejected: per-obligation bespoke wording (four mechanisms where one does).*
- **D6. The skill owns naming the record path; the runbook's step 1 references it.** Administer mode is *given* a record path — the same field, opposite direction — so both modes share the step and it belongs in the shared entry point. This confirms the accepted design's assignment (`run-study-skill-design.md:107`) rather than overturning it. *Rejected: runbook step 1 owning it (the runbook is execute-only; administer mode would then have a path-naming step with no home).*
- **D7. `DISCOVERY_LOG.md` is an append-only markdown table, newest row last, six columns.** Six short fields render, grep, and diff cleanly. *Rejected: one prose block per finding (the design calls it an index, not a second copy; prose invites re-stating the record).*
- **D8. `synthesis.md` is the first synthesis; later ones are `synthesis-<YYYYMMDD>-<slug>.md` and never edit a prior one.** *Rejected: appending to one `synthesis.md` (a second administrator's read of the same record is a separate opinion, not a revision of someone else's).*
- **D9. The annex is linked per step, not once globally, at the fixed path `exploration/<pkg>/studies/ANNEX.md`.** A reader then knows exactly which steps carry package-specific content. This design pins the path and the link; **Item 4 authors the file and its content** (see Orchestrator Rulings). *Rejected: one annex link in the runbook preamble (a reader cannot tell which of fifteen steps needs it).*
- **D10. `.gitignore` gains exactly one line, `!.claude/skills/run-study/`, after line 23.** *Rejected: broadening the pattern or restructuring the skill negations (spec `[HARD]`: no other skill's tracking status moves).*

---

## Orchestrator Rulings Recorded

- **The package annex file and its content are authored by Item 4**, not Item 3. Its content is the era pin, the oracle parameterization, and the glue — Item 4 material. Item 2 defines the annex **link** (D9) and the universal/annex split only. **This supersedes the spec's non-goal line at `spec.md:136`, which named Item 3 as the annex's author.** The rest of that non-goal stands: this item does not write annex content.
- **The snapshot's fingerprint field set is open, not a closed triple.** Item 3's accepted spec adds an **indicator-input fingerprint** — a tool-computed digest over the artifacts the trace reads — alongside the sealed `executable_fingerprint` and the `semantic_fingerprint` (`run-study-indicators/spec.md:40,42`). The snapshot copies every fingerprint the manifest declares, by the manifest's own name for it, so a manifest that grows a fourth fingerprint does not need this template revised. **The open set does not replace the spec's floor** (`spec.md:88`): the sealed package fingerprint, the model-contract/semantic fingerprint, and the indicator-input fingerprint are required in every snapshot regardless of what the manifest declares. Completeness beyond the floor is made checkable from inside the record by MF1's fix below.
- **Item 3's output JSON schema is versioned** (`run-study-indicators/spec.md:33`), so the snapshot's `indicators` block records that schema version alongside the file's digest.

### Spec deviations surfaced

- **`spec.md:95`'s "how it was chosen" is read as the argument half and homed in `record.md` §11**, while the window's bounds and its `engineered | sourced` provenance stay snapshot values (SF1). The spec places the whole clause inside the snapshot; splitting it follows this design's values/arguments rule, and the move is stated here rather than made silently.

---

## Architecture

Four artifacts this item authors, and the files they govern:

```
.claude/skills/run-study/          ← tracked via the one .gitignore negation
  SKILL.md          entry point, roles, mode selection, record path       (D6)
  runbook.md        ordered universal obligations; per-step annex links   (D9)
  record-template.md   the fill-in skeleton the executor copies           (D1, D5)

exploration/<pkg>/studies/
  manifest.json     Item 3 owns
  ANNEX.md          Item 4 owns; this design pins the path and the link   (D9)
  DISCOVERY_LOG.md  append-only index table; this design fixes the row    (D7)
  <study-id>/       one directory per study                               (D3)
    record.md       arguments and judgments; fixed headings
    snapshot.json   resolved values and digests                           (D2)
    indicators.json copied in from the tool, with its schema version
    results/        CSVs, report, generation script,
                    verification_summary.json                             (MF5)
    synthesis.md    administrator only; never touched by the executor     (D8)
```

**Data flow.** Intake enters at the skill and is deposited verbatim in `record.md` § Intake. Tool outputs (`indicators.json`, preflight results, `results/verification_summary.json`) enter through runbook steps; each step names its deposit section. `snapshot.json` is written once, at record commit, from resolved values — never from a live file. `record.md` § Snapshot then carries `snapshot.json`'s digest, and that is the only cross-file digest reference; `snapshot.json` never references `record.md` (a two-way digest is uncomputable).

**Role boundary.** The executor writes everything except `synthesis.md`, and is the sole writer of `DISCOVERY_LOG.md`. The administrator writes only `synthesis.md` and reads nothing outside the record directory. Neither writes the other's files. An administrator finding therefore lands in `synthesis.md`'s "what the record does not support" section and nowhere else; the discovery-log row for it is filed by whoever acts on the synthesis (MF6). This keeps the administrator boundary whole — the administrator is not even given `<pkg>`, so it could not resolve the log's path.

**Immutability and revision.** Committed evidence is never edited. A correction to `record.md` appends `## Addendum <YYYY-MM-DD>` at the end and leaves prior text intact. An addendum may correct the record's *statement* of a fact; it may never alter `snapshot.json`, `indicators.json`, or anything under `results/`. A changed snapshot value is a different study and gets a new study id.

---

## Component Overview

### `SKILL.md`

Frontmatter matching the local convention (`browser-inspect/SKILL.md:1-14`): `name`, trigger-carrying `description`, `allowed-tools`, `user-invocable: true`. Body, in order: what a study is in two sentences; the three roles (user / executor / administrator) with one line each; mode selection stated as an explicit question, not a guess; intake capture (collaborative and flexible — "study whatever you can find" through to a named parameter list, no fixed questionnaire); naming the record path; then pointers to `runbook.md`, the policy at its current path, and `scripts/study/`. Target under ~90 lines. Its failure mode is restating runbook steps; the plan stage should treat any step-shaped sentence in `SKILL.md` as a defect.

### `runbook.md`

Two ordered lists — the execute sequence and the administer sequence. Each execute step uses the same four-line micro-schema so a reader can scan the whole obligation set:

```
### <n>. <Obligation, imperative>
**Calls:** <tool path> | none
**Deposits:** record.md § <section name> [ + <artifact>]
**Fails closed when:** <mechanical condition> | nothing mechanical
**Annex:** exploration/<pkg>/studies/ANNEX.md § <topic>     ← only on package-specific steps
```

Steps, from the spec's universal list:

1. intake capture → §2
2. axis-group declaration → §7
3. indicators → §8 + `indicators.json`
4. **framing argument** — the user's ruling on any `no_constraint_response` axis with its model-development finding → §5 (first half, framing as proposed) + §8; **and its pre-execution critique verdict → §14 as a named review outcome** (MF7a, discharging `spec.md:82`)
5. preflight gates → §9
6. oracle range scan and window choice → §11 + snapshot `arms[].window`
7. route selection → §10, including the glue disclosure (MF4)
8. execution on the stock teax lifecycle → `results/`
9. verification → §13 + snapshot `arms[].verification` + `results/verification_summary.json`
10. **post-run framing judgment** — judge each axis's framing against the observed result → §5 (second half, framing as judged) (MF7b, discharging `spec.md:77`)
11. review outcomes → §14
12. report → `results/`; the report states the era pin as a reproduce prerequisite at the claim site while the pin exists (SF6)
13. snapshot and record commit → `snapshot.json` + §16
14. discovery-log rows → `DISCOVERY_LOG.md`

The administer sequence: read the record directory only → recover the fresh-administrator facts → write `synthesis.md` → state what the record does not support. It ends there. An administrator does not file a discovery-log row (MF6).

### `record-template.md`

The fill-in skeleton, with a short header explaining that it is copied to `<study-id>/record.md` and that unreplaced placeholder tokens are a commit-blocking defect. Placeholders are typed tokens (`<one-line goal, owner's words>`), never plausible-looking example values, so an unfilled field is visibly unfilled. Section order below.

### `DISCOVERY_LOG.md` row

| Date | Kind | Record | Finding | Disposition | Home |
|---|---|---|---|---|---|
| YYYY-MM-DD | `model` \| `process` | `<study-id>#<n>` | one line | one line | path, or `unrouted` |

`<study-id>#<n>` is the same id the record's Findings section uses, so log and record join without ambiguity. `Home` is never blank; `unrouted` is a stated state (and the one spec-acknowledged exception — study-specific presentation judgment — is recorded that way).

### `synthesis.md`

Header stamps the administrator, the date, and the `snapshot.json` digest it read. Sections: what the study set out to do; what it found; per-axis framing verdict; constraint structure; findings carried forward; and a mandatory **"What the record does not support"** listing every fact the administrator could not recover. That last section is the fresh-administrator check's output and is the input to record-contract improvement. `synthesis.md` may cite only paths inside the record directory.

---

## Record Section Order

Answer first, then the reasoning that qualifies it, then the machine evidence. A cold administrator reads §1–§6 and knows the study; §7–§17 are what they audit against. Mapping to the spec's mandatory content list (`spec.md:71-100`) in brackets.

| § | Heading | Spec item |
|---|---|---|
| 1 | Study header — id, package, date, executor, mode, arms | — |
| 2 | Intake | 3 |
| 3 | Objective and result | 1 |
| 4 | Constraint outcomes | 2 |
| 5 | Framing — proposed at intake, judged after the run | 6 |
| 6 | Per-axis account — framing-conditional (D5) | framing rule |
| 7 | Axis groups | 4 |
| 8 | Indicators and rulings — incl. the model-development finding per `no_constraint_response` axis | 5 |
| 9 | Preflight results — pass/fail per gate | 7 |
| 10 | Execution route and why — **including the glue disclosure** | 8, and the glue disclosure (`spec.md:94`, `:120`) |
| 11 | Study definition and window provenance — the argument | snapshot's "how it was chosen" (SF1) |
| 12 | Cross-fingerprint correlation and what it means | 9 — argument half; the tuples themselves live in snapshot `arms[].store` |
| 13 | Verification — outcome and its argument | 10 — outcome half; command, sampling scheme, tolerance live in snapshot `arms[].verification` |
| 14 | Review outcomes | 11 |
| 15 | Findings | 12 |
| 16 | Snapshot — filename, sha256, schema version | 13 |
| 17 | What this record does not contain | 14 |

§6 ships both conditional subsections present, each with its `**Applies:**` line:

```
#### <axis> — feasible structure (search framing)
**Applies:** yes | not applicable — <axis> is sensitivity-framed
```

and the sensitivity counterpart, whose content owes the observed response, an explicit statement that no boundary claim is made, and — for any constraint that goes violated anywhere in the sweep — where in the swept space it does (SF2, adopting the carried lens smell from `product-lens.md:26`). Locating a violation is a fact about the run, not a boundary claim, so it costs the sensitivity framing nothing.

§10's glue disclosure is the interpretive half of the glue ledger: what each rung supplies that the model does not, and what that means for the claims. The ledger's entries are snapshot values; §10 argues them. Glue exists only on the adapter route, which is why it belongs with the route argument that introduces it — and never in §17, which is reserved for gaps in the record itself (MF4).

Weight follows `/show-me` (**[INHERITED: concept, [OWNER] [REFERENT]]**): sections are short and adaptive; only presence is mandatory.

---

## Snapshot Structure

`snapshot.json` holds resolved values only. Shape (illustrative — the plan stage writes the field list out in full):

**Scoping rule (MF2): any field that can differ between arms is arm-scoped.** A cross-fingerprint A/B has a different executable per arm, therefore a different study definition, strategy identity, effective fingerprint, window, verification run, and result artifacts per arm. Only genuinely study-wide facts stay top-level. That one rule makes the plan's full field list derivable rather than guessed.

```jsonc
{
  "snapshot_schema_version": "1",
  "study_id": "...",
  "package": { "path": "...", "git_clean": true, "repo_commit": "..." },
  "fingerprints": { "<every name the manifest declares>": "<value>" },
  "manifest": { "digest": "...",
                "content_used": { "fingerprint_names": [ "...", ... ], ... } },
  "stores": [ { "store_id": "...", "path": "...", "compatibility_tuple": { ... } } ],
  "arms": [ { "arm_id": "arm-<slug>", "store_id": "...",
              "effective_executable_fingerprint": { "value": "...", "inputs": { ... } },
              "entry_models": { ... }, "strategy": "...",
              "window": { "bounds": ..., "provenance": "engineered|sourced" },
              "verification": { "command": "...", "tool_revision": "...",
                                "sampling_scheme": "...", "tolerance": "...",
                                "summary_sha256": "..." },
              "artifacts": [ { "path": "results/...", "sha256": "..." } ] } ],
  "glue_ledger": [ ... ],
  "tools": [ { "path": "...", "revision": "..." } ],
  "teax": { "revision": "...", "era_pin": "..." },
  "indicators": { "path": "indicators.json", "sha256": "...", "output_schema_version": "..." }
}
```

A single-arm study is the one-element case of the same shape, not a different shape.

Five rules govern it:

- **Fingerprint completeness is checkable from inside the record (MF1).** `manifest.content_used.fingerprint_names` copies in the list of fingerprint names the manifest declared, so the rule becomes internal: *every name listed there appears as a key under `fingerprints`.* The administrator can now audit completeness without opening the live manifest — which it may not do. The spec's floor holds independently: the sealed package fingerprint, the model-contract/semantic fingerprint, and the indicator-input fingerprint are present in every snapshot (`spec.md:88`; `run-study-indicators/spec.md:40,42`). The set stays open above that floor.
- **`arms[].effective_executable_fingerprint` carries its three inputs** (sealed fingerprint, digest of each allowed-modified file, adapter source digest) **or the explicit nil**: no adapter exists and the sealed fingerprint is the identity.
- **Stores are named once and referenced by id (SF5).** `stores[]` holds one entry per complete teax compatibility tuple; each arm names its `store_id`. Two arms sharing a store — the concept-design's same-definition case (`run-study-skill-design.md:129`) — reference the same entry, so the tuple is stated once and cannot drift between arms.
- **`arms[].verification` is the values half of spec item 10 (MF5)**: the command, the tool revision, the sampling scheme, the tolerance, and the digest of `results/verification_summary.json`. The outcome and what it means stay in `record.md` §13.
- **`glue_ledger` is a list, and a study with no glue states `[]` with a `glue_ledger_none: true` sibling** — the explicit-nil rule again, because an empty list and a forgotten field look identical in JSON.

Everything argued rather than resolved stays in `record.md`: the window's rationale in §11, the route's rationale and the glue disclosure in §10, the correlation's meaning in §12, the verification outcome in §13.

---

## Required Invariants

- **Values/arguments split.** `record.md` never restates content from any committed data file in the record directory — `snapshot.json`, `indicators.json`, or anything under `results/` (SF3). `record.md` § Snapshot contains a filename, a digest, and a schema version, no snapshot content. **One deliberate exception**, stated because the administrator must read `indicators.json` against a schema documented outside the record (`run-study-indicators/spec.md:33`): §8 carries the human-readable per-axis indicator statements the administrator needs, and `indicators.json` is the machine copy of the same facts.
- **One digest direction.** `record.md` references `snapshot.json` by digest; `snapshot.json` never references `record.md`.
- **Fingerprint completeness is internal.** Every name under `manifest.content_used.fingerprint_names` appears as a key under `fingerprints`, and the spec's floor (sealed, semantic, indicator-input) is present regardless.
- **Explicit nil.** Every conditional obligation is discharged by content or by a stated nil naming the condition. Silence discharges nothing.
- **Arm scoping.** Any snapshot field that can differ between arms is under `arms[]`; a store's compatibility tuple is stated once in `stores[]` and referenced by id.
- **Fixed headings.** A compliant `record.md` carries all seventeen section headings verbatim from the template, in order; addendum headings may follow the seventeenth (SF4).
- **No unreplaced tokens.** A committed record contains no `<...>` placeholder from the template.
- **Zero package names.** `SKILL.md`, `runbook.md`, and `record-template.md` contain no stellarator name, no package key prefix, and no oracle name. Grep-checkable.
- **No judgment in obligations.** No sentence in the three documents states a preference among axes, framings, routes, or results. "Argue and record the framing" is in bounds; "prefer search framing" is not.
- **Every runbook step names its record deposit.** No step exists whose output lands nowhere.
- **Role separation.** The executor never writes `synthesis.md`, and is the sole writer of `DISCOVERY_LOG.md`. The administrator writes only `synthesis.md` and reads nothing outside the record directory — including the discovery log, which it neither reads nor appends to.
- **Append-only.** `record.md` corrections are addenda; `snapshot.json`, `indicators.json`, and `results/` are never edited after commit.
- **Tracking.** `.gitignore` gains exactly one negation line; no other skill's tracking status changes.

---

## Non-Goals

- Writing the runbook, skill, or template *content* beyond the illustrative skeletons above. The plan and implement stages write the documents.
- Authoring `ANNEX.md` or any of its content — Item 4 (per the orchestrator ruling above, superseding `spec.md:136`).
- Implementing indicators, preflight, verification, the adapter, or any runner — Items 3–4.
- Defining tool CLIs, the manifest schema, the oracle seam, or the effective-fingerprint digest algorithm — Items 3–4. This design fixes only that the record *carries* them.
- Editing or ratifying the policy, including the H1 rescope — Item 6. The runbook cites the current path (`spec.md:62`, `[HARD]`).
- Building a record-contract linter. The invariants above are stated so one could be built; no epic item owns it (see Risks).
- Choosing any axis, framing, window, or route for any study.

---

## Implementation Notes

- **`.gitignore` is one line after line 23**, directory form with the trailing slash: `!.claude/skills/run-study/`. The trailing slash is what makes git descend past `.claude/skills/*`; both existing negations use it. Verify by `git check-ignore -v .claude/skills/run-study/SKILL.md` returning nothing after the edit.
- **The policy path is the *current* one** — `.project/active/demo-study-parameterization-policy/policy.md`. Citing `modeling_project/STUDY_POLICY.md` now would break on a decision Item 6 has not made.
- **Indicator vocabulary is exactly the spike-confirmed set** (`spec.md:58`, `[HARD]`): `no_constraint_response` is a sound negative; `constraints_reachable` is a possible path and never "responds"; `unresisted` is the agent's recorded judgment, never a tool output. The template's §8 wording must not blur these, and the not-derivable disclosure (monotonicity, same-quantity identity across differing key names, intra-module operand dependency) appears in every record.
- **The routing table from `spec.md:107-125` belongs in the record template's §15 guidance**, as the set of homes a finding may route to — {tool, runbook step, policy rule, skill, modeling item, research round, documented seam} — not as the proof-of-life's specific rows, which are spec history.
- **`<pkg>` and `<study-id>` are placeholders in all three documents.** A literal package name anywhere is an invariant violation, not a typo.

---

## Potential Risks

- **No mechanical enforcement of the record contract.** Every invariant above is checkable, and nothing checks them. A drifting record is caught only by the next administrator. *Mitigation for now:* the fresh-administrator check is the contract's own acceptance step, and its "what the record does not support" output reaches the discovery log through whoever acts on the synthesis (MF6). *Named for the epic:* a `record_lint.py` is the obvious home if drift shows up; no item owns it and this design does not create one on speculation.
- **Skeleton fatigue.** Seventeen sections plus an explicit-nil line on the conditional ones can read as ceremony, and a fatigued executor writes "n/a" everywhere. *Mitigation:* `/show-me` weight — sections are short and adaptive, presence is what is mandatory; and a nil must *name its condition*, which makes a lazy nil visibly inconsistent with §5's framing statement.
- **The values/arguments split has a genuine seam at the window** (bounds are a value, "how it was chosen" is an argument). B2 says the split is clean; this is the case most likely to falsify it. *Mitigation:* the split is stated once, in the template header, with the window named as the worked example.
- **Item 4's annex may want a different path.** This design pins `exploration/<pkg>/studies/ANNEX.md` so the runbook link is real. If Item 4 has cause to move it, that is a link update in one file, not a redesign — but it is a cross-item dependency the plan should flag.
- **Item 5's cold-pickup exercise is not in this run.** Its gap list may amend the record template. This contract stands on the accepted design alone (`spec.md:147`), and the template's own §17 is the channel by which those gaps arrive.

---

## Integration Strategy

`run-study` becomes the third tracked skill in `.claude/skills/` and the first multi-file one. It composes with what already exists rather than replacing it: teax keeps point execution via the two named routes; the policy stays the rulebook at its current path; `scripts/study/` tools (Items 3–4) are called by runbook steps and never by the skill directly.

The proof-of-life at `exploration/stellarator_e2e/study/` is untouched — it is the pre-capability record, and administer mode on it is expected to report missing structure rather than have it retrofitted. The first compliant record lands at `exploration/stellarator_e2e/studies/<study-id>/`, beside the manifest Item 3 creates.

Neither PM system gains state from this. Records live beside the package and outlive any work item; a work item cites a record path.

---

## Validation Approach

- **Grep gates.** Zero stellarator names, key prefixes, or oracle names across the three documents. Zero `modeling_project/STUDY_POLICY.md` references. Zero preference sentences among axes, framings, or routes (read, not grepped — the reviewer's job).
- **`.gitignore` behavior.** `git check-ignore -v` on a file under `.claude/skills/run-study/` returns nothing; the same command on a file under an untracked skill still returns line 21.
- **Deposit completeness.** Every runbook step's `**Deposits:**` line names a section that exists in the template; every template section is named by at least one runbook step or is header/nil material. A two-way check, run by reading both files side by side.
- **Spec coverage.** Each of the spec's fourteen mandatory content items maps to exactly one home — a template section, a snapshot block, or a stated split across the two (items 9 and 10 are the split cases). The table above is that map, and it is the artifact to re-check after the template is written.
- **Snapshot self-audit.** On a filled snapshot: every name under `manifest.content_used.fingerprint_names` is a key under `fingerprints`; the three floor fingerprints are present; every `arms[].store_id` resolves to a `stores[]` entry; every arm has its own window, strategy, effective fingerprint, verification block, and artifact list. Run against the two-arm case, not just the one-arm case.
- **Skeleton dry run.** Fill the template against the proof-of-life's known facts and see which sections have no source. That list is the honest gap between the pre-capability record and the contract, and it is the input to Item 5's exercise — not a reason to soften the contract.
- **Fresh-administrator check** is the real acceptance test and cannot run here: it needs a compliant record, which arrives with the first consumer study. Recorded as an unowned proof, consistent with `run-study-skill-design.md:210`.

---

## Next-Stage Handoff

**Fixed for the plan** (as corrected by design review MF1–MF7, SF1–SF7):
- Three files under `.claude/skills/run-study/`; one `.gitignore` line; record directory layout as drawn, with `verification_summary.json` under `results/`.
- The values/arguments split (D2) and the explicit-nil rule (D5) — every other convention follows from these two. The split governs `record.md` against *every* committed data file, with §8's indicator restatement as the one stated exception.
- Seventeen record sections in the stated order. Two spec items are split across homes and the plan must build both halves: item 9 (tuples in snapshot `stores[]`, correlation argument in §12) and item 10 (verification values in snapshot `arms[].verification`, outcome and argument in §13). Glue is disclosed in §10, never §17.
- **The snapshot is arm-scoped.** Any field that can differ between arms lives under `arms[]`; stores are named once in `stores[]` and referenced by id. A single-arm study is the one-element case. This is structural and settled here — not a field-naming detail for the plan.
- **Fingerprint completeness is internal**: `manifest.content_used.fingerprint_names` is copied in, the rule checks against it, and the spec's floor (sealed, semantic, indicator-input) holds regardless. The `indicators` block records Item 3's output schema version.
- Fourteen runbook execute steps as listed, including the framing step's §14 critique deposit and the post-run framing-judgment step feeding §5's second half.
- Study id `<YYYYMMDD>-<goal-slug>`, first same-day study unsuffixed; arms as `arm-<slug>` inside one record directory.
- Skill owns record-path naming (D6); runbook step 1 references it.
- Annex linked per step at `exploration/<pkg>/studies/ANNEX.md`; Item 4 authors the content.
- The administrator writes only `synthesis.md`. The executor is the sole writer of `DISCOVERY_LOG.md`.

**Open for the plan:**
- The exact wording of every step, section, and placeholder token. This design fixes structure only.
- Whether the runbook's administer sequence is a second ordered list in `runbook.md` or its own file. Start with one file; split only if the execute sequence makes it hard to read.
- The `snapshot.json` field *names* written out in full, against Item 3's manifest schema once that design lands. The scoping is fixed; only naming is open.

**De-risk first:** the skeleton dry run against the proof-of-life. It is cheap, it exercises B1 and B2 on real facts, and a section that cannot be filled from the best study this project has run is a section worth re-examining before the template is finished. Run the snapshot self-audit against a two-arm case in the same pass — MF2 was found precisely because the drawn shape was only ever checked against one arm.

---

**Next Step:** After approval → `/_my_plan`.
