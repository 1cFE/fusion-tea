# Spec Review: Native Research Acquisition and Registration Seam (GSTH Item 2)

**Spec:** `.project/active/goal-research-seam/spec.md`
**Contract:** `claude-pack/commands/_my_spec.md`
**Review File:** `.project/active/goal-research-seam/spec-review.md`
**Date:** 2026-08-25

---

## Reality Check

**Sound.** The spec is about the right work item, and its Problem section is materially accurate — I checked every code-facing claim in it and they hold (`append_source_index_entry` really does hardcode `Type: documentation` and leave `Use for`/`Validation` blank, `scripts/zotero_ingest.py:209-250`; `MANIFEST.jsonl` really is keyed on `zotero_key` only, `scripts/zotero_lib.py:25-36`; the PROTOCOL line cites `:27`, `:31-44`, `:56`, `:80` all resolve to the text claimed; MR-4's `Source`-must-be-a-path rule is at `modeling_project/REQUIREMENTS.md:49, :54`; the `agentic-mbse` SHA pin is genuinely test-enforced at `tests/test_dependency_provenance.py:13`).

Coverage against the epic is complete: all four Item 2 scope areas are represented, all six epic success criteria map onto spec criteria, and nothing from the epic's out-of-scope list is smuggled in. Design would not be badly misled by this spec.

The problems are real but targeted: several provenance grades over-read agent readings as owner needs, the item's *headline* capability has no stated way to be proven inside the item, and two requirement-shaped holes were left open (who supplies the index-block prose; whether the registration operation is callable outside the research surface).

---

## Audit

### Lens 1 — Faithfulness

**L1-1 · Direct claim:** **R-E1 is graded `[NEED]` but its source is an agent reading, not an owner ruling.** R-E1 says the four proofs must work without network and cites `align.md:13`. But `align.md:12` explicitly heads lines 13–16 as "Orchestrator readings recorded at Align (`[AGENT]`, unchallenged)". Under the capture-fidelity settled rule, an unchallenged agent reading is not owner-originated and is not settled — it is `[INFERRED]`, and challengeable. The spec gets this exactly right one requirement earlier (R-B4 cites "`align.md:14` `[AGENT]`" honestly inside an `[INHERITED]` grade), which makes R-E1's `[NEED]` look like a slip rather than a position. It matters: `[NEED]` would make "no network in Item 2" un-relitigable, and L4-adjacent finding **L3-1** below argues it *should* be relitigated.

**L1-2 · Direct claim:** **R-B3 is graded `[NEED]` on the wrong half of the owner's ruling.** The owner ruled on the *mechanism* (align.md:8, "delegated to design — make sure you use your judgement"), not on the requirement that every source carry a durable manifest identity. That requirement's actual source is epic Item 2 scope 2 and epic SC1 — and the epic's decomposition is `[AGENT]` ratified by the owner (`epic_goal_strategy_task_harness.md:100`), which per the absorb mapping is `[INHERITED]`, not `[NEED]`. The spec's own inline `[OWNER 2026-08-25]` marker on the deferral sentence is correct and should stay; the head grade should not be `[NEED]`.

**L1-3 · Direct claim:** **R-D1's `[HARD]` over-claims.** The requirement bundles two things: (a) enforcement must live in code because a PreToolUse hook cannot see an in-script fetch — genuinely forced, correctly `[HARD]`; and (b) enforcement happens *at two specific points*, URL/title before capture and content before write. (b) is not forced by anything. It traces verbatim to epic Item 2 scope 4 ("Enforce holdout URL/title checks before capture and content checks before any registry write"), which is `[INHERITED]`. Grading a structural choice `[HARD]` puts it beyond challenge when it's an inherited, challengeable decision.

**L1-4 · Direct claim:** **R-C3 and the Non-Goals bullet use `[OWNER 2026-08-25]` as a spec-register grade.** `[OWNER]` is a shaping-register vocabulary; the spec register is `[HARD]`/`[NEED]`/`[INFERRED]`/`[INHERITED]`, and the absorb mapping sends `[OWNER]` → `[NEED]`. R-C3 is a real, correctly-read owner ruling (align.md:9 — separate operations, explicit gate, not a session boundary, DI may follow later in the same broader workflow), so it earns `[NEED]`; it just isn't wearing the right label. Same for the reserved-gates Non-Goal.

**L1-5 · Direct claim:** **R-B6 carries a payload marker where a requirement grade belongs.** `[REFERENT: knowledge/SOURCE_INDEX.md:190-218]` correctly marks the WI-031 entries as a binding bar rather than an illustration (and I confirmed those entries do contain filled `Use for`, `Validation`, `Caveat`, and a `Source URL` line — the spec's description of them is accurate). But the requirement itself still needs a register grade, and its authority is the research doc's Recommendation 1 ("Keep the hand-written WI-031 entries as the referent"), which is agent-grade. So: `[INHERITED: research doc rec 1]` plus the `[REFERENT]` payload marker, not the marker alone.

**L1-6 · Direct claim:** **R-D3 softens the concept's obligation.** The concept says a recorded negative "**blocks** a repeat search for the same request" (`goal-driven-model-development-harness.md:114`). R-D3 renders this as "a later invocation against the same request can read it before searching." *Can read* is an affordance; *blocks* is a constraint. Two engineers will build different things from those two sentences, and the weaker one loses the property the requirement exists for. R-D3's head grade is also `[NEED]` while its own closing sentence is graded `[INHERITED: goal-driven-model-development-harness.md § Research stage]` — the requirement is inconsistent with itself about where its authority comes from.

**L1-7 · Rewrite request:** **R-E2's `[INHERITED: project testing preference]` cites nothing resolvable.** Every `[INHERITED]` item must cite its source. "Project testing preference" is a memory note, not a path. Either cite a repo artifact or regrade as `[INFERRED]`.

**L1-8 · Question to the user (advisory, and I think the spec is right):** **The concept names a research critic; the spec has no requirement for one, and no Non-Goal saying why.** `goal-driven-model-development-harness.md:114` and `:136` list a research critic (provenance, holdout disclosures, absence of paraphrased content, insight conflicts) as part of the research stage. I traced the omission and it is correct: the concept-design supersedes this, Item 1 owns "one lightweight fresh non-author checkpoint," and the epic's own resolution of `epic-plan-F2` states "This is not a critic at every native stage." But that reasoning lives nowhere in this spec, so a design agent reading the concept as Required Reading will plausibly re-add it. **Should this get one Non-Goal line recording the trace?**

### Lens 2 — Problem & Approach

**L2-1 · Question to the user:** **Nothing in the spec requires the registration operation to be invokable independently of the research surface.** The concept's user story is "As a research agent **or an operator**, I can register a URL or PDF with **one command**" (`goal-driven-model-development-harness.md:90`), and the research doc's Recommendation 1 is that `register-source` "gives `/research`, `/design-model`, and future study administers one door into `knowledge/sources/`." The spec's SC1 says "one operation," but every requirement that touches registration (R-B*) sits under a heading the acquisition surface (R-C1) owns end-to-end. A design that folds registration into the research command satisfies every written requirement and still leaves a design session or study administer hand-writing index blocks — the exact WI-031 failure this item exists to kill. **Is standalone invocability a requirement, or is the research surface the only intended caller for now?**

**L2-2 · If-then tradeoff:** **The relationship between the new operation and the existing `--local-pdf` path is undefined, and the two live requirements pull in opposite directions.** `process_local_pdf` (`scripts/zotero_ingest.py:474-521`) today registers a local PDF into `SOURCE_INDEX.md` and writes **no manifest row at all** (`append_manifest_entry` is called only from the Zotero path, `zotero_ingest.py:437`). R-B1 says "the Zotero path keeps working unchanged." R-B3 says every registered source carries a durable manifest identity. SC1 says a local PDF registers "through one operation." Those three cannot all hold for `--local-pdf` as it stands. This resolves cleanly **if** `--local-pdf` is meant to become a thin caller of the new operation (then say so, and R-B1's "unchanged" needs to scope to the *Zotero* path specifically), and awkwardly **if** the old path is meant to survive beside the new one (then the spec is knowingly leaving a second, manifest-less registration door open — which is close to the "no second registry implementation" line R-B1 draws). Which is it?

**L2-3 · Direct claim:** **The writer R-B1 extends is already half-broken, and "keeps working unchanged" would preserve the break.** `append_source_index_entry` inserts before the marker `## How MBSE Commands Use This File` (`zotero_ingest.py:239`). That heading **does not exist** in `knowledge/SOURCE_INDEX.md` — grep finds zero matches. Every call today therefore falls through to the fallback branch, prints a warning, and appends at end of file, *after* the `## How Sources Are Used` section. The research doc's P9 asserts the marker behavior as fact and the spec inherits that framing without checking. This is not fatal to the spec, but R-B1 as written ("the Zotero path keeps working unchanged") and R-E3 ("the affected knowledge-pipeline regressions still pass") both currently ratify a latent defect. The spec should decide whether fixing the insertion anchor is in scope.

**L2-4 · If-then tradeoff (small):** **`--save-source` is not uniform across the two input kinds R-B4 covers.** For a URL, `--save-source` produces a raw artifact (`extract_cli.py:277` copies the fetched PDF; `web_backend.py:514` saves raw HTML). For a **local** PDF there is no network fetch and the flag's own help text scopes it to "network-fetched content" — the raw artifact is the input file, which the existing path handles by copying to `knowledge/raw/` and hashing there (`zotero_ingest.py:489-499`). R-B4's flat "capture uses `agentic-mbse extract <url|pdf> --save-source` as it stands" reads as if one invocation shape covers both, and R-B5 then demands a raw hash for both. Harmless if design notices; a wasted debugging hour if it doesn't. Worth one clause of precision.

### Lens 3 — Pipeline Risk

**L3-1 · Question to the user — highest stakes:** **The item's headline success criterion has no stated way to be proven inside the item.** SC1 is "A URL *and* a local PDF each register through one operation…". SC7 lists the four things a no-network test must prove: duplicate, rollback, barred write, bounded negative. URL registration is not among them, and R-E1 sends live acquisition proof to Item 5. So as written, the single most important capability this item ships — URL → registered, citable, hashed source — is verified by nothing in Item 2. That is either (a) an accepted gap that should be *stated* (SC1's URL half proven in Item 5, Item 2 proves it only against a pre-fetched fixture), or (b) a reason to relitigate the no-network reading from **L1-1** — a loopback HTTP fixture or a captured raw artifact injected at the capture boundary would prove the whole chain offline. **Which?** This is the finding I'd resolve first; it changes what design builds for testability.

**L3-2 · Direct claim:** **The four return classes are never defined, and two of them are not distinguishable from the spec's text.** "Registered sources, bounded negative, operator queue, or blocker" appears in R-A3, SC6, and R-E4, and the spec requires exactly one per invocation and requires a non-builder to "read each of the four return classes and act." But nothing says what separates an *operator queue* from a *blocker*. R-D2 gives operator-queue one trigger (a source that cannot be fetched); blocker gets no definition anywhere. Two strong engineers will draw that line differently, and R-A3's "exactly one" makes the ambiguity load-bearing rather than cosmetic.

**L3-3 · Direct claim:** **R-B6 demands rich index blocks but no requirement says where the prose comes from.** `Use for` ("what the source establishes and which RQ it serves"), `Validation`, and `Caveat` are judgment text about the source's content. R-A1's request shape carries request id, value/question, consumer, gap type, priority, and where-to-look — none of which can produce that prose. The research doc's feasibility sketch names `title`, `use_for`, and optional `validation`/`caveat` as *inputs to the registration call*. Either the request shape needs those fields, or the acquiring agent supplies them at registration time and the spec should say so. As written this is a requirement-shaped hole deferred out by silence rather than by a filed Open Question.

**L3-4 · Question to the user:** **R-B6 is also not objectively checkable as stated.** "Registration produces blocks of that quality" — a test can assert `Use for` and `Validation` are non-empty (and the spec's last clause gives exactly that falsifier, which is good), but "of that quality" is not verifiable. Is the non-empty check the intended bar, with the WI-031 entries as the prose exemplar for the acquiring agent? If so, say that plainly so design doesn't try to build a quality gate.

**L3-5 · Direct claim:** **SC8 has no verification method and no matching requirement that could fail.** "A non-builder can operate the seam from its own documentation" is a strong falsifiable claim, but R-E4 — its only backing requirement — only requires the documentation to exist and cover four topics. Nothing in Item 2 puts a non-builder in front of it. Note also that SC8 is *not* one of the epic's six Item 2 criteria; it elevates an epic *deliverable* ("Operator documentation for the native research seam") to a success criterion. That may be the right call, but it is an agent-added bar and should either be graded as such or restated as something Item 2 can actually check (e.g. the documentation covers request formation, invocation, all four return classes, and the two operator actions).

**L3-6 · Question to the user (small):** **Do the upstream filings belong to this item?** Research doc Recommendation 5 says to file two upstream items now (the `approve-research` empty-list refusal; a `--register`/provenance-JSON request on `extract`). The spec's Non-Goals says only that edits inside pinned `agentic-mbse` are "an upstream filing" — it never says whether making those filings is Item 2's job. Cheap to settle either way.

**L3-7 · Question to the user (small):** **Where do this item's design decisions get filed?** Non-Goals rules out the ADR home (Item 1 owns it), while `align.md:15` says "ADR-home adoption is coordinated when this item files decisions." If design files a decision — and R-B3's deferred manifest-identity mechanism is exactly such a decision — the spec currently gives it nowhere to land. One sentence naming the interim home (or explicitly deferring the coordination to design) closes it.

### Lens 4 — Hygiene

**L4-1 · Rewrite request (minor):** `R-D2a` breaks the flat R-{section}{n} numbering used everywhere else. It reads as a late insertion, and downstream artifacts will cite it. Renumber or accept deliberately.

### Lens 5 — Reader Comprehension

**L5-1 · Rewrite request:** The four return classes (see **L3-2**) are the spine of the whole contract — they appear in the Success Criteria, in R-A3, and in the operator-documentation requirement — and the spec names them without ever defining them. A tired reader hits "exactly one of four return classes" in SC6 and has nowhere to go to learn what the fourth one is. This needs a plain two-line-per-class definition, stated once, before the requirements that depend on it.

Otherwise the voice is good: the Problem section leads with the point, the WI-031 story makes the gap concrete rather than abstract, and the Open Questions section is honest about what design still owns.

---

## Engagement Summary

**Overall take:** This is a well-grounded spec — the epic mapping is complete, the code claims check out, and the Problem section earns its length. Two things stop me approving it. First, the single capability this item exists to deliver (URL → registered source) has no stated way of being proven inside the item, because live network proof was pushed to Item 5 and no offline stand-in was named. Second, a cluster of provenance grades reads agent readings and inherited epic text as owner needs, which would make challengeable decisions un-relitigable downstream.

**Here's what I need you to weigh in on:**

1. **[L3-1]** How is URL registration proven inside Item 2? Either accept the gap explicitly (SC1's URL half is an Item 5 proof) or reopen the no-network reading and require an offline fixture that exercises the whole capture→register chain. This is the highest-stakes call in the review.
2. **[L2-1]** Must the registration operation be callable on its own — from a design session or a study administer — or is the research surface its only caller? The concept's "one command" user story says the former; the spec as written permits the latter.
3. **[L2-2, L2-3]** Settle what happens to `scripts/zotero_ingest.py --local-pdf`. It registers today with no manifest row, and the source-index writer's insertion anchor (`## How MBSE Commands Use This File`) does not exist in `SOURCE_INDEX.md`, so every write already falls through to the append-at-end fallback. "Keeps working unchanged" currently ratifies both.
4. **[L1-1, L1-2, L1-3, L1-4]** Confirm the grade corrections: R-E1 `[NEED]`→`[INFERRED]` (align.md:13 is `[AGENT]`), R-B3 `[NEED]`→`[INHERITED]` (owner ruled the mechanism deferral, not the requirement), R-D1's two-point structure `[HARD]`→`[INHERITED: epic scope 4]` (the code-enforcement half stays `[HARD]`), and R-C3's `[OWNER 2026-08-25]`→`[NEED]` with the citation kept.
5. **[L3-2, L5-1]** Define the four return classes, especially operator-queue vs blocker. R-A3 requires exactly one per invocation and R-E4 requires an operator to act on each; neither works while the boundary is undefined.
6. **[L3-3, L3-4]** Decide who supplies `Use for` / `Validation` / `Caveat` — request fields, or the acquiring agent at registration — and confirm that "non-empty" is the testable bar for R-B6 with the WI-031 entries as the prose exemplar.
7. **[L1-6]** Restore the concept's force on bounded negatives: it says a recorded negative *blocks* a repeat search, R-D3 says a later invocation *can read* it.

---

## Resolutions

Dispositioned by the orchestrator, 2026-08-25. All must-fix findings accepted; all advisory findings adopted. Spec revised in the same pass.

| Finding | Resolution |
|---|---|
| **L3-1** | **Accepted, option (b).** The no-network reading is not relitigated, but the offline proof is widened: **R-E2** requires the whole capture → holdout → register chain to run offline for both a URL input and a local PDF input, against fixtures injected at the capture boundary. SC8 states it. Item 5 owns only the *live network* proof. Fixture shape filed as an Open Question. |
| **L2-1** | **Accepted — standalone invocability is a requirement.** New **R-B0**, `[INHERITED]` from concept US-7 (`goal-driven-model-development-harness.md:90`) and research doc rec 1: registration has its own entry point; R-C1 now says the research surface *calls* it rather than owning it. New **SC2**. |
| **L2-2, L2-3** | **Accepted.** R-B1's "keeps working unchanged" is gone. The Problem section now states both verified defects (local-PDF path writes no manifest row, `zotero_ingest.py:521` vs `:437`; the `## How MBSE Commands Use This File` anchor is absent from `SOURCE_INDEX.md`, so every write falls through to append-at-end). **R-B1a** requires a manifest row for every registered source including local PDFs; **R-B1b** requires design to fix the anchor or adopt append-at-end deliberately; **R-B1c** preserves the Zotero *behavioral contract* and its regressions. |
| **L1-1** | **Accepted.** R-E1 regraded `[NEED]` → `[INFERRED]`, citing `align.md:13` as an `[AGENT]` orchestrator reading. |
| **L1-2** | **Accepted.** R-B3 regraded `[NEED]` → `[INHERITED: epic Item 2 scope 2 and epic SC1]`, with the owner's deferral of the *mechanism* kept inline as `[OWNER 2026-08-25]`. |
| **L1-3** | **Accepted.** Split: **R-D1** `[HARD]` keeps only the forced half (enforcement must live in the operation's code); **R-D2** `[INHERITED: epic Item 2 scope 4]` carries the two-point structure and is marked challengeable. |
| **L1-4** | **Accepted.** R-C3 regraded `[OWNER 2026-08-25]` → `[NEED]`, carrying the owner quote from `align.md:9` verbatim. The reserved-gates Non-Goal bullet likewise reads `[NEED]`. |
| **L1-5** | **Accepted.** R-B6 now carries `[INHERITED: research doc rec 1]` as its register grade alongside the `[REFERENT]` payload marker. |
| **L1-6** | **Accepted.** New **R-D6** `[INHERITED: goal-driven-model-development-harness.md:114]`: a recorded negative *blocks* a silent repeat — a matching request surfaces the prior negative and does not re-search without an explicit, recorded override reason. R-D5's head grade corrected to `[INHERITED]`. SC6 restated to match. |
| **L1-7** | **Accepted.** The unresolvable `[INHERITED: project testing preference]` is regraded `[INFERRED]` (now R-E4), which says outright that no repo artifact states the preference. |
| **L1-8** | **Adopted.** A decision record after the Non-Goals states that the research critic is deliberately not in this item, with the trace (concept-design review topology → Item 1's single checkpoint → epic resolution of `epic-plan-F2`) and which requirements carry its substance. Phrased as a decision record, not a prohibition. |
| **L2-4** | **Accepted.** R-B4 gains an `[INFERRED]` clause: `--save-source` is not symmetric across input kinds; for a local PDF the raw artifact is the input file copied to `knowledge/raw/` (`zotero_ingest.py:489-499`), and R-B5's raw hash must be satisfiable both ways. |
| **L3-2, L5-1** | **Accepted.** A new **§ The four return classes** section, before the requirements, defines all four with their decision boundaries. The stated line: operator queue is about a *source* (a named candidate blocked on accessibility or admissibility), blocker is about the *seam* (precondition, tooling, or contract failure, nothing established about any candidate). Mixed registered/queued invocations return `REGISTERED` with the queued candidates inside. |
| **L3-3** | **Accepted.** New **R-B7** `[INFERRED]`: the caller supplies `Use for` / `Validation` / `Caveat` at registration time, drawn from the request and the triage/instrumented record. The request shape does not carry them; registration does not invent them. |
| **L3-4** | **Accepted.** R-B6's bar is now presence and non-emptiness of `Use for`, `Validation`, `Caveat`, and `Source URL`. The uncheckable "blocks of that quality" phrasing is gone; the WI-031 entries stay as `[REFERENT]` for what the fields should say. |
| **L3-5** | **Accepted.** SC9 (was SC8) is graded `[INHERITED: epic Item 2 deliverables]` and given a verification path: a non-author walks the doc and exercises all four return classes and both operator actions. R-E6 lists what the doc must cover. |
| **L3-6** | **Adopted.** New **R-F1**: the two upstream `agentic-mbse` filings are made during implementation and are deliverables of this item. The upstream *fix* is not. |
| **L3-7** | **Adopted.** New **R-F2**: this item's durable decisions (manifest identity above all) file as ADRs in the home Item 1 establishes, coordinated at design time per `align.md:15`. This item does not create or edit that home. |
| **L4-1** | **Accepted.** Section D renumbered flat (R-D1…R-D6); the interpolated `R-D2a` is gone. Section B likewise renumbered to absorb R-B0 and R-B7. |

**Note on the reviewer's own reading:** L2-3's two code claims were re-verified independently before being written into the Problem section. Both hold — `grep` finds no `## How MBSE Commands Use This File` in `knowledge/SOURCE_INDEX.md`, and `append_manifest_entry` appears once as a call, at `zotero_ingest.py:437`, inside the Zotero path only.

---

**Verdict:** Revise

**Next Steps:** Once resolutions are recorded here, re-run `/_my_spec` (or return to the spec-agent session) and point it at this review to incorporate. The reviewer does not edit the spec. No finding requires rework of the work item itself — the scope, the epic mapping, and the Problem framing all hold.
