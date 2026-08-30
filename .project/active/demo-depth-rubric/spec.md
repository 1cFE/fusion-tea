# Spec: Demo Depth Rubric — Protocol Amendment, Rubric, Initial Grading

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-08-30
**Complexity:** MEDIUM
**Branch:** main

---

## Problem

The maturation concept (`.project/concepts/stellarator-demo-maturation.md`, 2026-08-30) commits the demo to a measurement loop — grade the model against a depth rubric, aim goals at the gaps, re-grade — but the yardstick does not exist. Nothing in the repo states what a systems-level fusion conceptual design study models and at what depth, so "improve toward ARIES-level quality" has no measure, goal grounding has no ranked target, and the future reveal-readiness condition has no scale to be written against.

Two owner rulings (2026-08-30, captured in the concept) shape the work: the clean-room split — rubric sessions are exempt from the clean room, model-facing research keeps it, the four sealed ARIES-CS papers stay unread until Item 7 — and no reveal or baseline comparison now. The split is not yet recorded in `knowledge/holdout/aries-cs/PROTOCOL.md`. As written, its §2/§3 block demo sessions from artifacts carrying ARIES-CS-specific data (bibliographic citations alone do not taint a source, per §3) — so a genuinely clean study is readable today, but the exemption the split grants (rubric sessions may read data-carrying sources too) and the barred-until-screened rule both need the amendment approved and logged first. That is why the amendment rides in this item as the first deliverable.

Plainly, the question this item answers: **which parts of our model are furthest below what a serious design effort would compute, so the first goal targets the worst one.**

## Success Criteria

- [x] **PROTOCOL amendment approved and logged.** *(Done 2026-08-30: applied to PROTOCOL §8, §6-logged; guard parses 9 patterns, holdout tests pass. Approval record: `amendment-draft.md`.)* Drafted for the owner, approved by them, recorded in §6: rubric sessions exempt from the clean room (Waganer included); the four sealed PDFs excluded from the exemption; any source ever ingested for rubric work barred for model-facing sessions until screened clean, the amendment naming where screening verdicts would be recorded.
- [ ] **The rubric exists, written by reasoning** — [OWNER 2026-08-30: "reason it out"] — per-subsystem depth levels on both dimensions (physics self-consistency; structural/costing depth), built from engineering reasoning against the model itself, existing repo sources, and Waganer (readable under the exemption). No new source ingestion. Each line carries its rationale, with a repo citation where one exists. Depth prescriptions only — no ARIES-CS-specific values, nothing from the sealed papers. Committed with its `path@sha` recorded.
- [ ] **The initial grading report exists**: per-subsystem, per-dimension scores, each traceable to model elements by path, plus a gap ranking crossed with study evidence (cost share, binding constraints, error history).
- [ ] **The report ends in candidate goal areas** — the top-ranked gaps, framed so the owner can pick the first maturation goal for grounding.
- [ ] **The seal held**: the PROTOCOL log shows no violations; the four sealed papers remain unread.

## Known Requirements

- **[HARD]** The four sealed ARIES-CS PDFs stay unread. The reveal is owner-triggered (PROTOCOL §6) and is not part of this item.
- **[HARD]** Until the amendment is approved and logged, PROTOCOL §2/§3 as written bar demo sessions from any artifact carrying ARIES-CS-specific data (citations alone do not taint) — no such source may be opened under the exemption before the amendment lands.
- **[HARD]** `scripts/holdout_guard.py` parses PROTOCOL §3's barred lists and refuses to answer if the parse comes out the wrong shape — the amendment must preserve §3's parseable structure.
- **[HARD]** If a source is ever ingested for rubric work (none planned), it enters `knowledge/` only through the native registration seam (`scripts/source_registry.py` / `scripts/research_seam.py`) — the one write door (GSTH Item 2).
- **[NEED]** The rubric covers both quality dimensions — **[OWNER-VERBATIM]** "both feel necessary".
- **[NEED]** The clean-room split — **[OWNER-VERBATIM]** "for rubrics I don't care about it. but for the research, yes I still want to try and maintain the clean room".
- **[NEED]** No reveal, no baseline comparison now — [OWNER 2026-08-30].
- **[NEED]** The rubric is written by reasoning, not by ingesting exemplar studies — [OWNER 2026-08-30] "reason it out". Reading a real design study stays available later, on demand, if a rubric line is contested.
- **[INHERITED: concept, Key Concept 4]** The rubric's output rule is the firewall: depth prescriptions only, never ARIES-CS-specific values.
- **[INHERITED: concept, Why This Shape]** Rubric-ingested sources are barred for model-facing sessions until screened clean.
- **[INHERITED: concept, SC-2]** Grading scores traceable to model elements by path; ranking crossed with study evidence.
- **[INFERRED]** The rubric is a repo-resident, citable artifact (home per design), so goals and the eventual Item 7 annex can cite it by `path@sha`.

## Non-Goals

- Grounding or running any maturation goal; model changes of any kind.
- The 1costingFE closure (pin-or-archive) — its own small item per the concept's decomposition; not a dependency of the rubric.
- The reveal-readiness condition — it needs the grading's output first; later trivial-scale item.
- Item 7, the sealed papers, or the ratified Anchor B bands.
- Reworking the §3 barred/admissible lists beyond what the amendment itself requires.
- Exemplar-study ingestion — deferred until a rubric line is contested or the eventual "at ARIES level" claim needs a calibrated bar; owner decides then.

## Open Questions / Deferred to design

- Rubric format: rows (and whether they must align with the ratified B-2 correspondence list), number of depth levels, level anchors, file format and home.
- (Settled — [OWNER 2026-08-30]: the rubric exemption covers the Waganer cost-account doc; rubric sessions read it freely. The §3 exception path remains in force for model-facing sessions. The amendment text encodes this.)
- Grading protocol: who authors, who grades, drift control for future re-grades.
- Rubric revision policy (concept open question 6).
- How the gap ranking presents "crossed with study evidence."
- Screening mechanics, only if a source is ever ingested for rubric work — the amendment names the rule and the record home; nothing more needed until then.

---

## Related Artifacts

- **Concept (required reading):** `.project/concepts/stellarator-demo-maturation.md`
- **Epic:** `.project/backlog/epic_stellarator_mbse_demo.md` — maturation-phase item registration pending (epic tracking update at pick-up, per the epic's home rule)
- **Protocol:** `knowledge/holdout/aries-cs/PROTOCOL.md`
- **Anchor bands (context):** `.project/completed/20260821_demo-anchor-acceptance-spec/spec.md`
- **Goal runbook (consumer):** `work/orchestration/GOAL_RUNBOOK.md`
- **Product-lens ledger:** `.project/active/demo-depth-rubric/product-lens.md`
- **Rubric + evidence map:** `.project/active/demo-depth-rubric/rubric.md`, `evidence-map.md` (design stage owner-skipped)

---

**Next Steps:** Design stage skipped — [OWNER 2026-08-30]. Execution goes straight to the rubric + grading artifacts; the owner reviews the artifacts themselves.
