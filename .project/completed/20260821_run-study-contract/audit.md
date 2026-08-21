# Audit: Skill, Runbook, and Record Contract (RUN-STUDY Item 2)

**Verdict:** PASS-WITH-FIXES — four fixes, all small and local; none weakens a spec `[HARD]` or the substance of a `[NEED]`
**Audited:** 2026-08-19
**Branch:** `feat/stellarator-mbse-demo`
**Commit:** `1e4d4e12`
**Deliverables audited:** `.claude/skills/run-study/{SKILL.md, runbook.md, record-template.md}`, `.gitignore:24`, `.project/active/run-study-contract/{dry-run.md, coverage.md}`

---

## The Point

Three owner pains drive this item. Quality regresses "if I don't phrase my prompt just the right way that got the executing agent to do what it did." There is no reproducibility floor, because no fixed list says what a study must record. And when a finished study looks wrong, "I have no idea where to begin to improve the process for better outcomes." The fourth obligation is the seam between roles: "I prefer having sufficient structure in the artifacts from the executing study agent (e.g. context, goals, plan) so that another agent can effectively pick up the results and do the synthesis."

So: a prompt carrying only a goal and a scope must put an agent on the proof-of-life's discipline, and the record that agent commits must let a second agent with no execution memory recover the framing per axis, the LCOE result, every named constraint outcome, and every finding — each traced to a committed artifact. A fact the second agent cannot recover is a defect in this contract, not in the synthesis.

## Summary

The three documents are complete, internally consistent, spec-complete, and package-free. Every structural claim the plan makes was re-checked independently and every one held: seventeen template sections verbatim in the design's order, fourteen runbook steps each naming a real deposit, deposit coverage clean in both directions, zero package names, one `.gitignore` line with no other skill's tracking moved. The five recorded deviations are all genuinely within design scope, and the one that matters — moving `glue_ledger` under `arms[]` — is the design's own normative scoping rule (MF2) being applied against an illustrative sketch, not a design change.

Four fixes, all cosmetic or one-sentence. The one with real content is fix 3: a spec `[NEED]` clause about who owns an unrecoverable fact has no home in any delivered document.

## Product Judgment

**Is this the right piece of work?** Yes. The item builds the artifact contract between the executing agent and the interpreting agent — the exact seam the owner named — and it stops there. It writes no tool, chooses no axis, and edits no policy. The universal/annex split is real: six of fourteen steps carry an `**Annex:**` link and the other eight are executable from the runbook alone, which is what makes the runbook reusable rather than a stellarator script with the names filed off.

**Product-lens ledger gate: CLEAR.** Two blocks in `product-lens.md`. The spec block is `CLEAR` (`spec-F1`, `spec-F2` BLOCKs both resolved by citation at `:22-23`). The design block is `CLEAR-WITH-FIXES` with `design-F1` and `design-F2` must-fix — both landed and verified here: `manifest.content_used.fingerprint_names` is in the template appendix with its internal-completeness rule (`record-template.md:281-283, 376-389`), and the snapshot is arm-scoped (`:306-350`). `design-F3` was a NOTE carrying the sensitivity-framing smell forward; it is now discharged in the delivered text — `record-template.md:106-108` requires a sensitivity-framed axis to locate any constraint violation in the swept space. No block is unresolved, and no structural smell fired at this hop.

**No implementation-hop lens run was performed.** Spawning a subagent was not authorized in this session, so the ledger was scanned rather than extended. Recorded under Not checked.

## Findings

### Plan completion

All six phases complete and all phase checkboxes ticked. The only `- [ ]` remaining in `plan.md` is inside a quoted deviation note at `:476`, not an open item. No TODO, no placeholder, no stub in any deliverable — `plan.md:410`'s "[TO BE FILLED DURING IMPLEMENTATION]" is the section header immediately above six filled completion blocks.

Independent re-check of the plan's structural claims, all confirmed:

- Seventeen `## ` headings in `record-template.md`, names and order matching the design's table at `design.md:200-218` exactly. The design table's em-dash clauses are gloss (`(D5)`, `pass/fail per gate`), not heading text.
- Fourteen `### ` steps and fourteen `**Deposits:**` lines in `runbook.md`, in the design's order (`design.md:161-174`).
- Two `**Applies:**` lines, both on §6's framing-conditional subsections.
- `<pkg>` appears 1 / 2 / 12 times across skill, template, runbook — matches `plan.md:530`.
- `git ls-files .claude/skills/` returns exactly five files: the two pre-existing tracked skills plus this item's three. `.gitignore:24` is one added line after line 23.

### Spec conformance

Success criteria:

- **Goal-only execute intake works** — not verifiable here. Needs a live run. `SKILL.md:50-66` delivers the mechanism (verbatim intake, executor's additions kept separate, record path named before the runbook starts); whether an agent actually lands on the runbook from a bare goal is the first consumer study's proof. Left unticked.
- **Record-only administration works** — same. `runbook.md:227-258` delivers the sequence and the boundary. Left unticked.
- **The runbook names obligations, not decisions** — met. Read all fourteen imperatives independently of the plan's read-check. Four sentences carry the risk and all four clear the bar: step 6's "an engineered window is not a defect; an undisclosed one is" is a disclosure rule symmetric between `engineered` and `sourced`; step 7's "two routes, and no third" is spec `[HARD]` capability, and the step requires the choice to be argued without making it; step 8's "no hand-rolled sweep loop" is a lifecycle obligation; step 11's three lenses are a coverage floor. Nothing states which axis to sweep, which framing is right, or what a result means. The template is symmetric between `search` and `sensitivity` at §5, §6 and between `engineered` and `sourced` at §11.
- **The record contract is evidence-complete** — met. §3 objective and result, §4 constraints by `constraint_id` + `source_local_identity` with `satisfied | violated | indeterminate`, §9 five named gates each with a stated outcome including `did not run — <condition>`.
- **An axis nothing resists produces a finding, not just a ruling** — met. `record-template.md:133-138` makes the model-development finding a separate mandatory table and says outright the ruling does not discharge it; `runbook.md:77-88` fails closed if such an axis reaches execution with no ruling recorded.
- **Facts are snapshotted, never cited** — met. `record-template.md:236-239` and `runbook.md:198-202` both state it in the deleting-the-manifest form the spec used. The MF1 `fingerprint_names` copy is what makes it auditable from inside the record.
- **Evidence is immutable and synthesis is separate** — met in substance. Template header `:30-34` for immutability; `runbook.md:249-258` for `synthesis.md`. See fix 3 for the one clause with no home.
- **Every proof-of-life lesson has exactly one named home** — met. The routing table lives in the spec (`spec.md:107-125`), which is what the criterion asks for; the template's §15 carries the *set* of homes, not the proof-of-life's rows, per `design.md:314`. Grep for `verify.py`, `preflight.py`, `H1`, `feasible-fraction` across the three documents returns nothing.
- **`.gitignore` admits only `.claude/skills/run-study/`** — met, verified mechanically above.

Non-goals respected: no tool, no manifest schema, no annex content, no policy edit, no axis chosen. `runbook.md:9` cites the policy at its current `.project/active/` path; zero `STUDY_POLICY` or `modeling_project/` references anywhere in the three files.

The spec's three declared splits are stated in both directions, not silent — §12 names `stores[]` as the tuples' home and the snapshot names §12 back; §13 names `arms[].verification` and the snapshot's `verification` block names §13 back; §11 names `arms[].window` and the snapshot's `window` block names §11 back (`record-template.md:174-187, 326-339`). `coverage.md:30-40` records the third split (item 13 / SF1) as a counting correction against the plan's expected two, with the design's "Spec deviations surfaced" as its authority. Stated, not absorbed.

### Design conformance

Every Required Invariant checked:

| Invariant | Result |
|---|---|
| Fixed headings — seventeen, verbatim, in order | **holds** — re-derived against `design.md:200-218` |
| Every runbook step names its record deposit | **holds** — two-way pairing re-run; all seventeen sections named by at least one step, all fourteen steps deposit somewhere |
| Zero package names | **holds** — grep for stellarator/e2e/oracle names/key prefixes returns nothing |
| No judgment in obligations | **holds** — read, not grepped; see above |
| Explicit nil, all four conditional cases | **holds** — framing-conditional (`:97-104`), glue "none" (`:162-163`, `:419-424`), no-adapter (`:317-321`, `:403-407`), correlation (`:174-181`) |
| Arm scoping | **holds** — window, strategy, entry_models, effective fingerprint, verification, artifacts, glue all under `arms[]`; `stores[]` referenced by `store_id` |
| One digest direction | **holds** — §16 carries `snapshot.json`'s digest; the snapshot carries no digest of `record.md` |
| Fingerprint completeness is internal | **holds** — `fingerprint_names` copied in, rule stated, floor table at `:391-398` |
| Values/arguments split | **holds in the text** — the split is stated once, in the template header, with the window as the worked example, and each split section says "do not restate them here" |
| Role separation | **holds** — administrator reads only the record directory and does not append to the log (`runbook.md:228-232, 246-247`) |
| Append-only | **holds** — `:30-34` |
| No unreplaced tokens | **stated** — see fix 2 |
| Tracking | **holds** |

**The five recorded deviations, each checked against design scope:**

1. *Phase 1 — neighbour check run against the symlink path.* Mechanical substitution; the assertion is identical. In scope.
2. *Phase 2 — appendix demoted from `## ` to `### `, and §12's `**Applies:**` line removed.* Both correct. D5 assigns `**Applies:**` to framing-conditional sections; §12 is arm-conditional and discharges its nil in prose by naming the condition, which is what the explicit-nil rule requires. Nothing softened.
3. *Phase 3 — `fingerprint_names` written without the awaiting-confirmation marker.* The orchestrator ruling settled the dotted-path derivation and the template cites it at `:388-389`. Stated, not silent. In scope.
4. *Phase 3 — `glue_ledger` moved to `arms[]`.* **Checked against MF2 specifically.** `design.md:239` states the rule in one line: "any field that can differ between arms is arm-scoped." A sealed-versus-adapter A/B differs in exactly this field. `design.md:258`'s top-level placement sits inside a block the design labels "illustrative" at `:237`, while the scoping rule is normative and is restated as a Required Invariant at `:285`. This is the rule being applied, not a design change. It does not weaken `spec.md:94` ("glue ledger inline… with an explicit 'none'"): the ledger is still inline in the snapshot and the nil is now per arm, which is stricter.
5. *Phase 6 — the third split (item 13 / SF1) recorded rather than folded into the count.* A counting correction against a deviation the design already declared. In scope.

Also recorded and confirmed: the Phase 4 orphan fix. §15 Findings had no depositing step until step 14 was retitled and given the §15 deposit. That was a real gap found by the plan's own check, and the fix holds — §15 is deposited and the log rows join to it by `<study-id>#<n>`.

One documentation drift, no action needed: `design.md:258` still shows `glue_ledger` top-level. The sketch is labelled illustrative and the move is recorded in the plan, so the design is not lying — but a future reader diffing design against template will hit it.

### Code integrity

Not code. The document-level equivalents were checked and are clean: no obligation duplicated across two files (the study-id convention has one home, `runbook.md § Naming`, cited from `SKILL.md`), no section that restates a committed data file, and the one deliberate exception (§8's human-readable indicator statements alongside `indicators.json`) is stated in the design and honored.

Considered and cleared: `runbook.md:146` restates "sample stratified by verdict combination", a lesson the spec's routing table homes in `verify.py` (Item 4). Not a two-home violation — the runbook names the obligation the step owes and the tool enforces it, which is the routing table's own model.

---

## The fixes

**1. `tools[].revision` renames an Item 3 field while carrying the `(Item 3)` marker.** `record-template.md:353-355` writes `"revision": {"recipe": "tool-source-digest/v1", "digest": ...}` with the `(Item 3)` marker on the `revision` line. Item 3's actual field is `tool.source_digest` (`run-study-indicators/design.md:194`); `revision` is the spec's prose word (`spec.md:96`), not an Item 3 name. The template's own rule at `:246-247` says marked names "are not this contract's to rename." A snapshot writer copying from the indicator report has to translate the key. *Smallest fix:* rename the key to `source_digest`.

**2. Five nested `<...>` placeholder tokens.** `record-template.md:45, 98, 104, 147, 148` put a token inside a token — `<arm-<slug>, ... — or: single arm>`, `<yes | not applicable — <axis> is sensitivity-framed>`, `<pass | fail | did not run — <condition>>`. The design's invariant is "a committed record contains no `<...>` placeholder from the template", and the template calls an unreplaced token commit-blocking. Nesting makes the outer token's boundary ambiguous to any check narrower than "does a `<` remain", and to a human filling it. *Smallest fix:* flatten each — e.g. `**Applies:** yes — or: not applicable, this axis is sensitivity-framed`.

**3. A spec `[NEED]` clause has no home in any delivered document.** `spec.md:100`: "A fact it cannot recover is a defect in the record contract, not in the synthesis." That attribution is the entry point the owner asked for — where to begin improving the process — and grep finds it nowhere in the three files. The mechanism is delivered (the mandatory "What the record does not support" section); the sentence saying whose defect it is, is not. *Smallest fix:* one sentence in `runbook.md § synthesis.md` — a fact the administrator could not recover is a defect in the record contract, not in the synthesis.

**4. `fingerprints.indicator_inputs.files` copies the report's shape under the manifest's name.** `record-template.md:264-267` marks the block `(Item 3) fingerprints.indicator_inputs` — the manifest path, where `files` is a list of plain path strings (`run-study-indicators/design.md:151`) — but writes the richer `{path, sha256}` form from the indicator *report* (`:200-201`). The choice is right and `plan.md:463` records why; the template alone does not say so. *Smallest fix:* extend the inline comment to name the report as the shape's source.

---

## Certification

Marked in `spec.md`: success criteria 3 through 9 verified and ticked. Criteria 1 and 2 left unticked — both require a live run and neither can be verified from documents. No deliverable file was edited.

**Not checked:**

- **The fresh-administrator check**, this contract's real acceptance test. It needs a compliant record and none exists. The plan says so plainly at `:580` and this audit adds nothing to it.
- **Whether a goal-only prompt actually routes an agent onto the runbook** (SC1) and **whether administer mode produces a usable synthesis** (SC2). Both are behavioral, both need a consumer study.
- **The snapshot self-audit against a real filled `snapshot.json`.** The two-arm audit in Phases 2–3 ran against a constructed case; the shape is checked, no instance is.
- **A fresh implementation-hop product-lens run.** The existing ledger was scanned and its blocks resolved by citation; no new lens agent was spawned, because subagent use was not authorized in this session.
- **`ANNEX.md` and the six `**Annex:**` links.** The file does not exist yet (Item 4). If Item 4 moves the path, six lines in `runbook.md` need updating — flagged in `plan.md:500` and still open.
- **Item 3 field names beyond the thirteen the plan checked plus the four re-checked here.** I verified every `(Item 3)`-marked name in the appendix resolves to a real name in `run-study-indicators/design.md`; I did not verify the *semantics* of each field match Item 3's intent.
