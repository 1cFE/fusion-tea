# Round 5 review — fresh reviewer

HEAD `d644e7a2`. Read only the brief's files, PROTOCOL § 3/§ 6 and `git log` of the run directories. Nothing run or acquired.

**Verdict: FINDINGS.** None blocking; four correct-before-use wording/count fixes. D1/D2 stay with the owner; D1 also decides whether the round-4 readings the answer cites keep standing.

## Checks

1. **Source-screen fidelity: PASS.** `BARRED_TERMS` comment, no-waiver docstring and `_input_identity_holdout_hit` (input path/URL plus caller's title) quoted correctly. PROTOCOL § 3 principle matches; § 6 makes reveal and any index registration owner-logged and records no reveal or exception for this goal. HX-01/HX-02 logs and receipts match the review; receipts touched only by `8bbb7e3c`/`620e341f`. HX-02's log states the mirror substitution; HX-01's statement is in `evidence/research-acquire-r4-return.md:25`, not the run record. D1/D2 are rulable.
2. **Dependent access held: PASS.** HX-03 searches block `aries.ucsd.edu`, `qedfusion.org`, archive.org; `registered: []`; no receipts directory; both candidates "not purchased, not fetched"; hold-out landing pages not opened.
3. **Bounded attempt: PASS.** 4/4 searches, 0 captures, `limit_reached: max_searches`; Google Scholar gap and Semantic Scholar 429s disclosed. `OPERATOR_QUEUE` is right: paywalled copies exist, so no negative.
4. **Four conclusions: PASS.** All four, qualified, in § 1, § 12 and the ledger's last bullet; § 13 carries three (no lumped-heater sentence). No contradiction; § 1 item 3 leads with "source-internal inconsistency" before its qualifier.
5. **41 MW: PASS.** § 12 "about 41 MW of the 151 MW"; 151.002 − 109.876 = 41.126 (ledger 41.125, rounding); no "most" left.
6. **Unknowns: PASS.** Each of four unknowns ties to a stated gap; closure as partially answered recommended; no new dependency. Unknown (3)'s ≈ 50 MW differs from the ledger's ≈ 60 MW; state the basis.
7. **Findings log: PASS.** No study → no rows matches the trail's convention; the outcome is in `return.json` (OPERATOR_QUEUE, `negative: null`) and the trail.
8. **Learning delta:** below.
9. **Unsupported claims:** findings 1–4.

## Findings

1. correct-before-use. Trail T-002 return: "twelve other results ... one of them a landing page for a sealed hold-out paper". The log has eleven rejected; two (ResearchGate, Academia) are landing pages of the sealed FS&T 54 paper.
2. correct-before-use. Trail round-5 result: "bounded negative ... recorded in the run's `return.json`". That file has `negative: null`; the r5 return says "no bounded negative". Write "the OPERATOR_QUEUE outcome".
3. correct-before-use. `research-acquire-r5-return.md` ends "Not committed."; the run was committed at `f01d8104`.
4. correct-before-use. Answer § 13 "last obtainable lead" for a paper not obtained; write "last lead".
5. note. Review D2's "regardless of where a copy comes from" rests on the caller's title carrying the term; the content scan is the backstop.
6. note. Add the lumped-heater sentence to § 13.

## Learning delta

- **L-015: CORRECT.** Keep the rule-home facts (no waiver; host term marks the canonical library; identity/title hits and any registration need a § 6 entry). Mark "mirror substitution is not permitted access" as the coordinator's assessment pending D1, so the learning does not pre-decide the owner.
- **L-016: ACCEPT.** HX-03 demonstrates it (locate, log `--failure`, close; nothing captured). Add: request `max_captures: 0` where the schema allows.

## Not covered

Findings log file, `run.jsonl`, `_post_capture_refusal`, the research-acquire command file, `ref15`/`malang98` reviews, PROTOCOL § 7 and frontmatter, round-4 evidence beyond one quote.

— fresh round-5 reviewer, 2026-09-25
