# Design Review: Skill, Runbook, and Record Contract (RUN-STUDY Item 2)

**Design:** `.project/active/run-study-contract/design.md`
**Spec:** `.project/active/run-study-contract/spec.md` (Accepted)
**Concept-design:** `.project/concepts/run-study-skill-design.md` (Accepted — settled)
**Epic:** `.project/backlog/epic_run_study_capability.md` — Item 2
**Review File:** `.project/active/run-study-contract/design-review.md`
**Date:** 2026-08-19
**Reviewer posture:** fresh, skeptical; nothing on the do-not-relitigate list re-opened.

---

## The Point

A study today is only as good as the prompt that started it. One excellent study exists and its discipline lives in one finished work item's plan and one 450-line package-specific script. Three owner pains follow: quality regresses "if I don't phrase my prompt just the right way"; there is no reproducibility floor, because no fixed list says what a study must record; and when a finished study looks wrong, "I have no idea where to begin to improve the process for better outcomes."

The fourth obligation is the seam between two agents: "I prefer having sufficient structure in the artifacts from the executing study agent (e.g. context, goals, plan) so that another agent can effectively pick up the results and do the synthesis."

So this item's job: a prompt carrying only a goal and a scope must put an agent on the proof-of-life's discipline, and the record that agent commits must let a second agent with **no execution memory and no access to anything outside the record directory** recover the framing per axis, the LCOE result, every named constraint outcome, and every finding — each traced to a committed artifact. A fact the second agent cannot recover is a defect in this contract, not in the synthesis.

That last clause is the review's measuring stick. Most of what follows is one question asked repeatedly: *can the cold administrator actually do this from what the design specifies?*

---

## Fundamental Assessment

**Sound.** This is the right piece of work and the right approach.

The design's core move — `snapshot.json` holds resolved values, `record.md` holds arguments, neither restates the other — is the correct application of the concept-design's Principle 1 to file boundaries, and it is simple. Two conventions (fixed heading text, the explicit-nil rule) carry all four conditional-obligation cases that would otherwise need four mechanisms. Nothing here is over-engineered: three markdown files, one JSON file, one `.gitignore` line, and a table. A simpler design that still satisfies the spec does not exist — the inline-snapshot alternative was considered and rejected on stated grounds (`design.md:84`), and the rejection is right.

**Product-lens:** run inline against the same sources (ledger appended to `product-lens.md`). Gate **CLEAR-WITH-FIXES**. Two findings graded owner-authority (`design-F1`, `design-F2`) appear below as MF1 and MF2; both are field additions, not rework triggers.

**Both design-level smells examined; neither fired structurally.** The near-miss is worth naming: D2 states a completeness rule the record's only auditor cannot evaluate (MF1). That is a checkability gap, not a transfer of invariant ownership — the executor still owns it, and copying one list into the snapshot closes it. Not escalated to Rework.

**Where the design is weakest** is not its concept but its follow-through on its own invariant, *"no required fact appears in both files."* The split is stated once and then applied unevenly: compatibility tuples land in both homes, verification lands in neither cleanly, glue disclosure is routed to the section for record *gaps*, and the A/B snapshot shape cannot hold two arms. These are all the same class of defect — residue the design's own bet B2 denies — and all are small, local fixes.

---

## Answers to the Brief's Five Questions

### Q1. Do all 14 mandatory record items land in exactly one of the 17 sections?

**Yes.** I checked the map at `design.md:176-194` against `spec.md:71-100` item by item:

| Spec item | Section | |
|---|---|---|
| 1 Objective and result | §3 | ✓ |
| 2 Constraint outcomes | §4 | ✓ |
| 3 Intake | §2 | ✓ |
| 4 Axis groups | §7 | ✓ |
| 5 Indicators (+ ruling + model finding) | §8 | ✓ |
| 6 Framing | §5 | ✓ |
| 7 Preflight results | §9 | ✓ |
| 8 Execution route | §10 | ✓ |
| 9 Compatibility tuples | §12 | ✓ (but see MF3 — also in the snapshot) |
| 10 Verification | §13 | ✓ (but see MF5 — split unstated) |
| 11 Review outcomes | §14 | ✓ |
| 12 Findings | §15 | ✓ |
| 13 Snapshot | §16 | ✓ |
| 14 Missing-evidence statement | §17 | ✓ (but see MF4 — glue smuggled in) |

None dropped, none doubled. The three unmapped sections are correctly unmapped: §1 is header material, §6 discharges the spec's framing-conditional rule (`spec.md:86`), §11 carries the spec's "how it was chosen" clause. The table is sound; the defects below are in what the design says *around* it, not in the mapping.

One item the table does not carry at all: **the glue disclosure**. It appears only in prose at `design.md:235`. See MF4.

### Q2. Is the values/arguments split residue-free?

**No, on all three probes.**

- **Glue** — the ledger is a snapshot value (correct, matches `spec.md:120`), but `design.md:235` routes "the glue's disclosure" to §17, *"What this record does not contain."* Wrong home (MF4).
- **Window** — bounds and provenance are snapshot values; rationale is §11. Clean *as a split*, but it silently moves "how it was chosen" out of a field the spec put **inside** the snapshot (`spec.md:95`). The move is defensible; the silence is not (SF1).
- **Verification** — the least clean of the three. The whole of spec item 10 (command, sampling scheme, tolerance, outcome) goes to §13 prose, and the snapshot has no verification block — yet the concept-design requires "the verification command and revision" snapshotted (`run-study-skill-design.md:129`). The command and tolerance are resolved values by every criterion the design states. And `verification_summary.json` has no named home in the directory layout (MF5).

### Q3. Can a cold administrator execute the D2 snapshot rule?

**No.** "Every fingerprint the manifest declares, by the manifest's own name" (`design.md:231`) quantifies over a set that lives in the live manifest. The administrator reads nothing outside the record directory (`design.md:128`, `:249`). They can see which fingerprints *are* present; they cannot see which *should be*. A snapshot missing one is indistinguishable from a manifest that never declared it — exactly the fresh-administrator defect this contract exists to prevent (MF1).

### Q4. Does anything smuggle a judgment into an obligation, or a package name into a universal document?

**No, on both.** I swept for it specifically.

- No preference among axes, framings, routes, or results appears anywhere in the design's prescriptions. The near-misses are honest: `design.md:203`'s "sections are short and adaptive" is a weight referent carried with its grade; `design.md:271`'s indicator-vocabulary rules are definitional, not preferential; §11's heading "— the argument" describes a section's kind, not its content.
- No stellarator name, key prefix, or oracle name is prescribed into `SKILL.md`, `runbook.md`, or `record-template.md`. `<pkg>` and `<study-id>` are used consistently as placeholders and `design.md:273` makes a literal name an invariant violation rather than a typo. The one real path the documents carry — the policy at `.project/active/demo-study-parameterization-policy/policy.md` — is a repo path required by spec `[HARD]` at `spec.md:62`, not a package name.

### Q5. Is D4 compatible with the concept-design's store rule?

**In principle yes; in the drawn shape no.** One record directory holding N arms, each naming its own store's complete tuple, with the comparison in the record and never in a merged store, is exactly the concept-design's rule (`run-study-skill-design.md:129`). The `arms[]` array is the right structure. But the rest of the snapshot is single-arm: `study.entry_models`, `study.strategy`, `study.window`, and top-level `effective_executable_fingerprint` are scalars, and a cross-fingerprint A/B — the very case D3 cites to reject a fingerprint-tagged study id (`design.md:85`) — has a different executable, hence a different study definition, per arm. The shape cannot hold the epic's first consumer (MF2).

---

## Dimensional Review

### 1. Spec Compliance
**Assessment:** Concerns

The mandatory-content map is complete (Q1). The `[HARD]` items are all honored: `.gitignore` one-line negation (verified — line 21 is `.claude/skills/*`, 22–23 are the two existing negations, so "after line 23" is correct); the current policy path; the two execution routes; the indicator vocabulary; records at `exploration/<pkg>/studies/<study-id>/`.

Two `[NEED]` items are narrowed without the design saying so:
- `spec.md:95` puts "how it was chosen" in the snapshot; the design puts it in §11 (SF1).
- `spec.md:88`'s fingerprint triple is replaced by a manifest-relative open set (MF1). The set is a superset *in fact* — Item 3's manifest declares three fingerprints (`run-study-indicators/spec.md:40,42`) — but the design states no floor, so the guarantee rests on a file the record cannot see.

**Capture-fidelity:** provenance is carried well. The design marks its inherited owner-verbatim material, states the orchestrator ruling that supersedes `spec.md:136` explicitly rather than quietly, and preserves the `/show-me` `[REFERENT]` at its correct scope (record-section weight, `design.md:203`). The contrast is instructive: the design knew how to surface a supersede when it made one, which is why the two unsurfaced narrowings above read as oversights rather than as style.

One spec obligation reaches no runbook step: the pre-execution framing critique as a named review outcome (`spec.md:82`) — the exact smell the spec-hop product-lens fixed (`product-lens.md:25`) and the design drops (MF7).

### 2. Pattern Consistency
**Assessment:** Pass

The skill file shape is derived from the one local convention that exists (`browser-inspect/SKILL.md:1-14`) rather than invented. The `.gitignore` mechanism is the proven one, verified on disk. The record directory layout follows the concept-design's paths exactly. No new pattern is introduced where an existing one would serve — the fill-in-skeleton-with-fixed-headings idea is new to this repo, but it is the minimum structure the fresh-administrator check requires and D1 states its rejected alternative.

### 3. Abstraction Quality
**Assessment:** Pass

Every abstraction earns its place. Strip the values/arguments split and every fact becomes either awkwardly narrated or buried — the design says exactly this at `:64` and it is right. Strip the explicit-nil rule and omission becomes indistinguishable from forgetting. Strip fixed headings and the cold reader has nothing to find facts by. The four-line runbook micro-schema (`design.md:145-150`) is the smallest thing that makes "every step names its deposit" checkable by reading.

Seventeen sections is the one number that invites "over-engineered?" — but fourteen are spec-mandated content, one is a header, and two discharge stated rules. The count is the spec's, not the design's.

### 4. Duplication Avoidance
**Assessment:** Concerns

This is the dimension the design's own bet B2 is about, and it is where the follow-through slips. Compatibility tuples have two homes (MF3). The no-duplication invariant at `design.md:241` is scoped to `snapshot.json` vs `record.md` only, while the record directory also holds `indicators.json` and `results/` — so §8's relationship to `indicators.json` is governed by nothing (SF3). Arms sharing one store will write the same tuple twice under `arms[]` (SF5).

### 5. Data Structure Clarity
**Assessment:** Concerns

`snapshot.json`'s shape is legible and the three governing rules are stated crisply. But it is single-arm (MF2), has no verification block (MF5), and its `fingerprints` map is open with no floor and no self-check (MF1). The design says the field list is illustrative and the plan writes it out — fair for field *names*, but arm-scoping is a structural decision this stage owns, not a naming detail the plan can settle.

The `DISCOVERY_LOG.md` row is well-specified: six columns, `<study-id>#<n>` joining log to record without ambiguity, `Home` never blank with `unrouted` as a stated state.

### 6. Route Safety
**Assessment:** Pass

Read as document-routing (no HTTP surface here). Every fact has a named destination; there is no catch-all section and no silent fallback. The explicit-nil rule is precisely the anti-wildcard mechanism — silence discharges nothing. The one routing defect is a wrong destination, not an ambiguous one (MF4).

### 7. Bets & Decisions Integrity
**Assessment:** Concerns

B1–B4 are genuine claims about reality, each with a real "if false" consequence, and none is a mechanism choice in disguise. B2 is correctly identified as the load-bearing one, and the design even names the window as the case most likely to falsify it (`design.md:281`). Decisions D1–D10 each name a rejected alternative with a reason.

**Hidden bet, surfaced:** *the record can be audited for completeness from inside itself.* Every stated invariant is written as checkable, the design's validation plan calls them checkable, and the fresh-administrator check is named as the real acceptance test — but the D2 completeness rule quantifies over a file the auditor may not open. Nothing in the design states this bet, and it is the one MF1 falsifies.

**Second hidden bet, lower stakes:** *the administrator can interpret `indicators.json` from the record alone.* Its schema is versioned and documented in Item 3's territory, outside the record directory (SF3). Either §8 carries the human-readable per-axis statements, or the administrator boundary needs an explicit carve-out for a versioned schema document. The design picks neither.

Honesty is otherwise good: `design.md:279` names the unowned linter and declines to invent an item for it; `:304` records the fresh-administrator check as an unowned proof rather than claiming it.

### 8. Reader Comprehension
**Assessment:** Pass

The Core Concept section does the job in one sentence and then says everything else follows from it — and it does. The mental model (two files, one rule, two conventions on top) arrives before any mechanism. The record section table is skimmable and its ordering principle is stated plainly ("answer first, then the reasoning that qualifies it, then the machine evidence"). Terms are anchored on first use.

One comprehension defect with teeth: the glue disclosure exists only in a subordinate clause at `design.md:235` and appears in no table, no section description, and no invariant. A plan-stage reader working from the section map will not know it exists (part of MF4).

---

## Must-Fix

Each would produce a wrong or non-conformant implementation.

### MF1. The snapshot's completeness rule cannot be checked by the only reader who audits it
**What's wrong:** `design.md:231` — "Every fingerprint the manifest names appears under `fingerprints`, by the manifest's own name for it." The administrator reads nothing outside the record directory (`design.md:128`, `:249`), so the reference set is unavailable. A snapshot missing a fingerprint reads identically to a manifest that never declared one. This also silently narrows `spec.md:88`, which names three specific fingerprints as `[NEED]`.
**Evidence:** `design.md:231`; `design.md:249`; `spec.md:88`; `run-study-skill-design.md:107` (administrator boundary), `:129` ("never cites a live file").
**Smallest fix:** the snapshot already copies `manifest.content_used` (`design.md:217`). Add the manifest's declared fingerprint **name list** to that block, and restate the rule as an internal one: *every name listed under `manifest.content_used.fingerprint_names` appears as a key under `fingerprints`.* Add the spec's floor in one clause: at minimum the sealed package fingerprint, the model-contract/semantic fingerprint, and the indicator-input fingerprint. The rule then stays open to a fourth and becomes checkable from inside the record.

### MF2. The snapshot shape cannot hold a cross-fingerprint A/B
**What's wrong:** D4 puts all arms in one record directory and one `record.md`, and D3's rejection of a fingerprint-tagged study id rests on "an A/B study can span fingerprints" (`design.md:85-86`). But the snapshot at `design.md:212-227` makes `study.entry_models`, `study.strategy`, `study.window`, and top-level `effective_executable_fingerprint` study-scoped scalars. Arms that span fingerprints have a different executable — therefore a different study definition, strategy identity, and effective fingerprint — per arm. The shape cannot express the epic's first consumer (Item 6).
**Evidence:** `design.md:212-227` vs `design.md:85`, `:86`; `run-study-skill-design.md:129` (store rule); epic Item 6 scope 3–5.
**Smallest fix:** move `study.entry_models`, `study.strategy`, `study.window`, `effective_executable_fingerprint`, and the arm's `artifacts` under `arms[]`. Keep at top level only what is genuinely study-wide: `study_id`, `package`, `fingerprints`, `manifest`, `tools`, `teax`, `indicators`. State the rule in one line — *any field that can differ between arms is arm-scoped* — so the plan's full field list is derivable rather than guessed.

### MF3. Compatibility tuples have two homes
**What's wrong:** the mapping table sends spec item 9 — "the complete teax tuple of every store referenced" — to §12 in `record.md` (`design.md:189`), while `arms[].store.compatibility_tuple` holds the same tuples in `snapshot.json` (`design.md:220`). `design.md:235` implies §12 is meaning-only ("the correlation's meaning in §12"), but the heading and the map say tuples. This is the exact residue B2 denies, and it violates the design's own invariant at `:241`.
**Evidence:** `design.md:189`, `:220`, `:235`, `:241`; `spec.md:80`.
**Smallest fix:** rename §12 to the argument alone — *Cross-fingerprint correlation and what it means* — and state that the tuples themselves live in `snapshot.json` `arms[].store`, with §12 naming the boundary crossed, the constraint-matching basis, and the `predicate_ir` differences. Update the mapping-table row to read "spec item 9 — argument half; value half in snapshot".

### MF4. Glue disclosure is routed to the missing-evidence section
**What's wrong:** `design.md:235` sends "the glue's disclosure" to §17, *"What this record does not contain."* Glue is present evidence about what the *model* did not supply — a mandatory-always disclosure (`spec.md:120`) — not a gap in the record. Filing it under §17 conflates two different absences and makes the record's own gap list unreadable. It is also absent from the section map entirely (`design.md:176-194`), so a plan-stage reader working from the table drops it.
**Evidence:** `design.md:235`, `:194`, `:176-194`; `spec.md:94`, `:120`; `run-study-skill-design.md:203` (glue definition).
**Smallest fix:** route the glue's interpretive disclosure to **§10, Execution route and why** — glue exists only on the adapter route, so it belongs with the route argument that introduces it — and add it to the §10 row of the mapping table. Reserve §17 for record gaps. (A dedicated glue subsection under §11 is an acceptable alternative; what is not acceptable is §17 or prose-only.)

### MF5. Verification's values/arguments split is unstated, and its data file has no home
**What's wrong:** the whole of spec item 10 goes to §13 prose, and `snapshot.json` has no verification block — yet the concept-design requires "the verification command and revision" snapshotted (`run-study-skill-design.md:129`), and the command, sampling scheme, and tolerance are resolved values by every criterion the design applies elsewhere. Separately, `verification_summary.json` appears in the data-flow paragraph (`design.md:126`) but in no directory layout (`design.md:114-123`) and under no snapshot `artifacts` rule.
**Evidence:** `design.md:126`, `:114-123`, `:212-227`, `:190`; `spec.md:81`; `run-study-skill-design.md:129`.
**Smallest fix:** add a `verification` block to the snapshot — command, tool revision, sampling scheme, tolerance, and the digest of `verification_summary.json` — and scope §13 to the outcome and its argument. Place `verification_summary.json` under `results/` in the layout so the existing `artifacts` digest rule covers it.

### MF6. The administrator writes outside the record directory
**What's wrong:** `design.md:128` says the discovery log "is written by both — a row per finding, at the moment the finding is filed", and the administer sequence ends "file any record-contract gap as a process finding" (`design.md:152`). But `DISCOVERY_LOG.md` sits at `exploration/<pkg>/studies/`, outside the record directory, and the same paragraph plus the invariant at `:249` say the administrator "writes nothing else and reads nothing outside the record directory". The administrator cannot even resolve `<pkg>` under that boundary. Two rules, three lines apart, contradict.
**Evidence:** `design.md:128`, `:152`, `:249`, `:117`; `run-study-skill-design.md:107`, `:165`.
**Smallest fix:** pick one and state it. Recommended: the administrator's findings land in `synthesis.md`'s "what the record does not support" section only, and the discovery-log row for an administrator finding is filed by whoever acts on the synthesis. Then the boundary invariant stands unamended and `design.md:128`'s "written by both" is corrected to "written by the executor". If instead the administrator files its own row, the invariant must be restated as *reads nothing outside the record directory; writes only `synthesis.md` and appended discovery-log rows* — and the administrator must be given `<pkg>` as an input.

### MF7. Two framing obligations have no producing step
**What's wrong:** the fixed step set at `design.md:152` puts the framing argument before preflight and never revisits it. But §5 requires framing "as proposed at intake **and as judged after the run**" (`spec.md:77`, `design.md:182`), and `spec.md:82` requires the pre-execution framing critique to appear as one of §14's named review outcomes — the deposit the spec-hop product-lens explicitly fixed (`product-lens.md:25`). Neither obligation is in the step set, so under the design's own invariant "every runbook step names its record deposit" (`design.md:248`) these two sections have no producer. A runbook built to this design cannot fill them.
**Evidence:** `design.md:152`, `:182`, `:191`, `:248`, `:301`; `spec.md:77`, `:82`; `product-lens.md:25`.
**Smallest fix:** two additions to the step list. (a) The framing step deposits its pre-execution critique verdict into §14 as a named review outcome. (b) A post-run step — natural home is between verification and review outcomes — judges framing against the observed result and deposits into §5's second half.

---

## Should-Fix

- **SF1. The "how it was chosen" move is unsurfaced.** `spec.md:95` puts it inside the snapshot; `design.md:188` puts it in §11. The move is right — it is an argument — but the design surfaces its other spec deviation explicitly (`design.md:98`, superseding `spec.md:136`) and should do the same here. One line in Orchestrator Rulings or in D2: *reads `spec.md:95`'s "how it was chosen" as the argument half, homed in §11; bounds and provenance stay snapshot values.*
- **SF2. Carried lens smell not addressed.** The spec-hop product-lens handed the design one thing: sharpen the sensitivity-framing section to locate a constraint violation in the swept space (`product-lens.md:26`). `design.md:203` gives the sensitivity section the observed response and a no-boundary-claim statement only. Add "and, for any constraint that goes violated anywhere in the sweep, where in the swept space it does" — or record explicitly that the design declines it and why.
- **SF3. §8's relationship to `indicators.json` is ungoverned.** The no-duplication invariant (`design.md:241`) names only `snapshot.json` and `record.md`, but the directory also holds `indicators.json` and `results/`. Compounding it, the administrator must interpret `indicators.json` against a schema documented outside the record (`run-study-indicators/spec.md:33`). Fix: broaden the invariant to *"`record.md` never restates content from any committed data file in the record directory"*, then state the one deliberate exception — §8 carries the human-readable per-axis indicator statements the administrator needs, and `indicators.json` is the machine copy.
- **SF4. Fixed-headings invariant vs. addenda.** `design.md:244` requires "all seventeen section headings verbatim, in order"; `:130` appends `## Addendum <YYYY-MM-DD>`. A literal checker fails a corrected record. Fix: "…all seventeen, in order; addendum headings may follow the seventeenth."
- **SF5. Shared-store arms duplicate their tuple.** Under `arms[].store` (`design.md:220`), two arms sharing one store — the concept-design's same-definition case (`run-study-skill-design.md:129`) — write the identical tuple twice. Fix: state that arms sharing a store name the same store entry by id, with the tuple stated once.
- **SF6. Era pin "at the claim site" is half-routed.** `spec.md:122` routes it to package annex **and** record snapshot; the snapshot has `teax.era_pin` (`design.md:223`), but the lesson's point is that the pin surfaces as a reproduce prerequisite *where the claim is made* — the report. No runbook step or section carries that. One clause in the report step's obligation.
- **SF7. D3's collision suffix skips `-a`.** `design.md:85` appends `-b`, `-c` on same-day collision, leaving the first study unsuffixed. Workable but reads as a missing `-a`. State it: "the first same-day study is unsuffixed; subsequent ones append `-b`, `-c`."

---

## Notes

- **`.gitignore` evidence verified independently.** Line 21 is `.claude/skills/*`; 22–23 negate `browser-inspect/` and `concept-research-navigation/`. "One line after line 23", directory form with trailing slash, is exactly right, and the `git check-ignore -v` verification at `design.md:269` is the correct test.
- **Item 3 seam checked.** The manifest does declare three fingerprints (`run-study-indicators/spec.md:40,42`), so MF1's floor is satisfied in fact today. The finding stands because the *rule* does not say so and the record cannot verify it.
- **D6 correctly confirms rather than re-decides.** The skill owning record-path naming is the accepted design's assignment (`run-study-skill-design.md:107`), and the "administer mode is *given* a record path — the same field, opposite direction" argument is the right reason, not a rationalization.
- **The de-risk recommendation is good.** The skeleton dry run against the proof-of-life (`design.md:324`) exercises B1 and B2 on real facts before the template is finished. Worth keeping first in the plan.
- **Q4 sweep found nothing.** No judgment in any obligation; no package name in any universal document. Recorded here so a later reader knows it was checked, not assumed.

---

## Issues by Severity

### Critical
- MF1 — snapshot completeness rule not checkable from inside the record (Spec Compliance, Bets)
- MF2 — snapshot shape cannot hold a cross-fingerprint A/B (Data Structure Clarity)
- MF6 — administrator writes outside its stated boundary (Abstraction Quality / internal contradiction)
- MF7 — post-run framing judgment and framing-critique deposit have no producing step (Spec Compliance)

### Major
- MF3 — compatibility tuples in two homes (Duplication)
- MF4 — glue disclosure routed to the missing-evidence section and absent from the map (Route Safety, Comprehension)
- MF5 — verification split unstated; `verification_summary.json` unplaced (Data Structure Clarity)
- SF1 — unsurfaced narrowing of `spec.md:95`
- SF3 — §8 vs `indicators.json` ungoverned; administrator needs an off-record schema

### Minor
- SF2, SF4, SF5, SF6, SF7

---

## Recommendations

1. **Fix the snapshot first (MF1, MF2, MF5).** All three are edits to one block. Arm-scoping is structural and belongs to this stage, not the plan.
2. **Close the three routing defects (MF3, MF4, MF7)** and update the section-mapping table in the same pass — the table is what the plan stage will read, so a fact that is not in it does not exist.
3. **Resolve the role-boundary contradiction (MF6) explicitly**, in the invariant list rather than in prose, since the invariant is what a later checker would be built from.
4. **Then apply SF1–SF7**, none of which changes the design's shape.
5. **Keep the de-risk order as written** — skeleton dry run against the proof-of-life before the template is finished.

---

## Resolutions

*To be filled in when the owner engages with this review. Each entry records the owner's decision in their terms; the design agent reads this section to incorporate.*

---

**Overall:** Revise
**Verdict:** **APPROVE-WITH-FIXES**

Must-fix before the plan stage: **MF1** (snapshot completeness checkable from inside the record), **MF2** (arm-scope the snapshot), **MF3** (tuples in one home), **MF4** (glue disclosure out of §17 and into the map), **MF5** (verification split stated; `verification_summary.json` placed), **MF6** (administrator boundary contradiction resolved), **MF7** (post-run framing judgment and framing-critique deposit added to the step set).

Should-fix: SF1–SF7.

The core — the values/arguments split, fixed headings, and the explicit-nil rule — is right and should not be reopened. Every finding above is a local correction to that frame, not a challenge to it.

**Next Steps:** Record resolutions above, then re-run `/_my_design` (or return to the design-agent session) and point it at this review to incorporate. The reviewer does not edit the design.
