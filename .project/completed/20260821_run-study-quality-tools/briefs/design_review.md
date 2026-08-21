# Brief: design review for "Quality Tools and Era Adapter Promotion" (RUN-STUDY Item 4)

Review `.project/active/run-study-quality-tools/design.md` against:
- its spec (same directory, Accepted),
- the accepted concept-design `.project/concepts/run-study-skill-design.md` (Tools, adapter,
  Required Invariants, Validation Strategy) and review C4/C5/M6/m3,
- Item 3's accepted design `.project/active/run-study-indicators/design.md` (the manifest.py /
  schemas seams it consumes),
- Item 2's delivered runbook/record contract (`.claude/skills/run-study/runbook.md`,
  `record-template.md`) — these are now IMPLEMENTED; the design's asks of them must be
  compatible with what exists,
- epic Item 4.

Fresh, skeptical review. Must-fix vs should-fix vs notes; evidence (file:line) and smallest
fix each. The design's Appendix records two probes (P1/P2) — spot-check their claims against
the probe scripts in the work-item folder if present; re-run only if cheap and read-only.

Specific questions beyond your sweep:
1. Invariant 4 (declared source set = every file that can change a glue value or accept-set):
   is the enumeration COMPLETE under the new structure? The design adds oracle_entry.py (the
   package-owned shim) through which verify calls the oracle — if the ADAPTER also reaches
   the oracle for g3 via the shim, or if the shim's mappings can change a fed value, must the
   shim be in the declared source set too? Trace who calls what for g3 in the design and rule.
2. verify.py samples via StudyQuery on the ERA teax (fa0e06a): the proof-of-life sampled CSVs,
   so per-case channel access through StudyQuery is UNPROBED on that revision. Check the era
   worktree's StudyQuery API (read-only) supports what D7 needs; if uncertain, demand a plan
   de-risk step, not faith.
3. D1 baseline_result.json: who executes the baseline point and when, and is that compatible
   with the delivered runbook's step order (preflight step 5 precedes execution step 8)? The
   design asks Item 2's runbook for a one-line precondition — is a line honestly enough?
4. D6's declined CLI + changed manifest VALUES (module=oracle_entry): is that consistent with
   Item 3's D6 ("records what exists today") given oracle_entry.py will exist by then — and
   does anything in Item 3's tests pin the current values so the change breaks them?
5. The manifest-currency gate runs against the two contract fingerprints — verify the claim
   that glue edits cannot touch either file (the glue-edited files are pipelines/*.yaml and
   inputs/system_design.json; the contracts are separate files). Is currency-vs-identity
   separation complete, or is there a stale-manifest case neither gate catches?
6. D9 no-partial-output for preflight vs the record's §9 needing pass/fail PER GATE: if
   preflight only writes on full pass, how does a failed-gate study record its preflight
   evidence? Is that consistent with Item 2's record contract (preflight results mandatory)?

Do NOT relitigate: the package_identity.json seam's existence, effective-fingerprint
machinery, adapter ownership of era facts, store sampling per se, StudyRunner-only execution.

Write your review to `.project/active/run-study-quality-tools/design-review.md`, verdict:
APPROVE / APPROVE-WITH-FIXES (list) / REJECT.
