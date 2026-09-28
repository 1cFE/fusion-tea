# Product-Lens Ledger — demo-depth-rubric

Epic: STELLARATOR-DEMO


## spec — 2026-08-30 — rev 66bbdb81 (.project/active/demo-depth-rubric/spec.md)
Point (re-derived): The four sealed ARIES-CS papers stay unread until the owner-triggered Item 7 reveal, and the clean-room split applies exactly as the owner ruled — rubric-writing exempt, model-facing sessions keep the clean room, rubric-ingested sources barred until screened clean, and the Waganer exception deferred-not-granted (concrete-scope request at need, owner rules, §6-logged). The rubric itself must cover both quality dimensions, cite every line, and be committed at a recorded `path@sha` so grading and the eventual reveal annex can rest on it.   [source: .project/concepts/stellarator-demo-maturation.md § Owner's Words + § Non-Goals + SC-1/2/6; knowledge/holdout/aries-cs/PROTOCOL.md §§2-6, grade: owner/HARD]
Falsifier: The spec licenses a path that admits sealed or barred material outside the owner's specified procedure — e.g. Waganer becoming readable without a concrete-scope §6 exception — or produces a rubric/grading that drops a required dimension, an uncited line, or the recorded `path@sha`.
Findings:
- spec-F1 [DON'T] Open question "Whether the Waganer cost-account doc is readable under the rubric exemption or still needs a §6 logged exception — the amendment text decides" relitigates a settled owner ruling: the concept's Non-Goals fix the answer (deferred, not granted; readable only via a concrete-scope request made at need, owner-ruled, §6-logged), so a blanket grant via amendment text is not an open option — .project/concepts/stellarator-demo-maturation.md § Non-Goals, [OWNER 2026-08-30] (owner) — disposition: BLOCK
- spec-F2 [DON'T] The Problem section and [HARD] requirement 2 overstate PROTOCOL: "§2/§3 as written bar demo research sessions from ARIES-CS-citing artifacts" contradicts §3's explicit rule that bibliographic citations do not taint a source — only artifacts carrying ARIES-CS-specific design or cost data are inadmissible (a pre-ARIES-CS study like STARFIRE needs no amendment at all). Safe direction, but a [HARD] line drafted from a wrong premise will shape the amendment text — knowledge/holdout/aries-cs/PROTOCOL.md §3 (agent/ratified, owner-resolved 2026-07-12) — disposition: pending (correct the two sentences; scope the amendment to what §3 actually bars)
- spec-F3 [DO] The spec commits the amendment to "barred for model-facing sessions until screened clean" but the screening mechanics — who screens, against what test, recorded where — appear nowhere, not even in Open Questions / Deferred to design, though the concept's handoff names them spec work ("how rubric-ingested sources get screened before model sessions may read them"). Without a stated mechanism the exemption can leak the clean room away through the repo — .project/concepts/stellarator-demo-maturation.md § Why This Shape (clean-room split) + § Next-Stage Handoff (INHERITED) — disposition: pending (add to the spec's deferred list or state the mechanism)
Gate: BLOCKED (spec-F1)

## Dispositions — 2026-08-30 (spec author, post-verdict)

- **spec-F1 (BLOCK, owner grade):** spec conformed to the settled [OWNER] ruling — the Waganer open-question line replaced with a settled-marker: exception path stands, rubric exemption does not cover it unless the owner says so. Flagged to the owner at spec presentation for an explicit confirm-or-override. Gate clears on the owner's word, not this edit.
- **spec-F2 (agent/ratified):** fixed — Problem and [HARD] line now state the accurate rule (data-carrying artifacts barred; citations alone do not taint), so the amendment text will be drafted from the right premise.
- **spec-F3 (INHERITED):** fixed — the amendment success criterion now names the screening-record home, and screening mechanics are listed in the deferred-to-design section.

## spec-F1 cleared — 2026-08-30

Owner ruled (option A, /_my_ask_me Q1): the rubric exemption covers Waganer; the §3 exception path stays for model-facing sessions. Concept Non-Goal and spec amended to match. Gate: CLEAR.

## Post-verdict owner rulings — 2026-08-30

- [OWNER] Rubric written by reasoning, no exemplar-study ingestion ("reason it out"); spec SC and requirements amended, ingestion criterion removed.
- [OWNER] 1costingFE closure = pin (separate admin item; concept OQ5 settled).
