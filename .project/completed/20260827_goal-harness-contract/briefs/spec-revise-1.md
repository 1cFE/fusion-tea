Orchestrator feedback — independent spec review returned Revise (`.project/active/goal-harness-contract/spec-review.md`; read it in full). Apply these dispositions and revise spec.md:

**Must-fix, apply all four:**

1. **L3-1 (homes list).** Extend the writer-ownership requirement to every textual home that breaks under joined disposition rows: add `DISCOVERY_LOG.md:3` ("one row per finding"), `runbook.md:290-292`, and the schema table's Disposition/Home cell to the named homes. On append vs update: orchestrator disposition (execution detail, recorded here) — both owner statements are satisfied by the same mechanism: a disposition *update* is delivered as an *appended* joined row keyed `<study-id>#<n>`; the one-row-per-finding wording in the extra homes must therefore be amended in scope. State that in the spec as the reconciliation, cite both sources (design § Findings and Learning, owner-ruled C1; epic success criterion), and keep it challengeable as `[AGENT]` reconciliation of two owner texts.
2. **L1-1 (digest provenance).** Regrade the "barred row is *authority* digests" reconciliation at spec.md:42 (and the echoes at :88, :92) as `[INFERRED]` — the "authority" narrowing is design-table agent text, not the owner's P2/M4 words. Keep the digest requirement itself at :41 owner-graded, and keep the surfacing duty: if design finds the evidence digest and the hardening bar genuinely collide, surface to owner, don't resolve silently.
3. **L3-2 (live test).** Record current state: `tests/study/test_records.py:41` already guards the discovery log and only tolerates joined rows by set-comparison accident. Requirement: the consistency tests must account for and deliberately cover the joined-row shape (mechanism still design's).
4. **L3-3 (SC1 gap).** Add the missing requirement: the runbook and affected project guidance must cite the filed architecture records.

**Owner-decision flags — orchestrator dispositions, record them, don't re-ask:**
- L1-2: `[REFERENT]` stands; regrade its provenance to `[INHERITED: epic Item 1 Required Reading — "proven prose referent"]` (owner-ratified epic text, not owner-verbatim).
- L2-1/L2-3: no spec change. The estimate is epic-level `[AGENT]` ratified; checkpoint first exercised in Item 5 is the epic's own owner-dispositioned placement (F2). Note both in the spec-review disposition record if you keep one.

**Nits:** fix all four cheaply — :71 phrasing (findings are Phase-4-pending, not yet in the file), :81 vs :106 test-shape tension, the log-header's wrong runbook-section cite, and add a short framing paragraph before the 17-bullet lean-artifact list (working-voice rule: give the frame before the details).

Finish with the revised spec at the same path. ARTIFACT line when done.
