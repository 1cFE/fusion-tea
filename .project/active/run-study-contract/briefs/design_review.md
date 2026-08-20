# Brief: design review for "Skill, Runbook, and Record Contract" (RUN-STUDY Item 2)

Review `.project/active/run-study-contract/design.md` against:
- its spec `.project/active/run-study-contract/spec.md` (accepted),
- the accepted concept-design `.project/concepts/run-study-skill-design.md` (Core Model,
  Design Principles, Required Invariants — settled, the design must conform),
- epic Item 2 (`.project/backlog/epic_run_study_capability.md`).

You are a fresh, skeptical reviewer. Deliver must-fix findings (things that would produce a
wrong or non-conformant implementation) separated from should-fix and notes. For each finding:
what's wrong, the evidence (file:line), and the smallest correct fix.

Specific questions to answer, beyond your own sweep:
1. Does every one of the spec's 14 mandatory record-content items land in exactly one of the
   17 sections, with none dropped or doubled? (Check the mapping table yourself.)
2. Is the values/arguments split residue-free for: glue (ledger vs disclosure prose — design
   line 235 routes "glue disclosure" to §17, the missing-evidence section; is that the right
   home?), window (bounds vs rationale), verification (summary vs outcome)?
3. Can a cold administrator actually execute the D2 snapshot rule — "every fingerprint the
   manifest declares, by the manifest's own name" — without reading the live manifest? (The
   administrator may read only the record directory.)
4. Does anything in the design smuggle a judgment into an obligation, or a package name into
   a universal document?
5. Is the A/B one-record-one-directory convention (D4) compatible with the concept-design's
   store rule (one store per complete compatibility tuple; correlation stated in the record)?

Do NOT relitigate: the four homes, records beside the package, snapshot-not-cite, the
explicit-nil rule's existence, Item 4 authoring the annex (orchestrator ruling), the policy
staying at its current path (Item 6 owns the move).

Write your review to `.project/active/run-study-contract/design-review.md` and end with
verdict: APPROVE, APPROVE-WITH-FIXES (list), or REJECT (reasons).
