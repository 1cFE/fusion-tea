# Brief: design review for "Indicator Tool and Package Manifest" (RUN-STUDY Item 3)

Review `.project/active/run-study-indicators/design.md` against:
- its spec `.project/active/run-study-indicators/spec.md` (accepted),
- the accepted concept-design `.project/concepts/run-study-skill-design.md` (indicator builder,
  manifest, Appendix A, Design Principles 1-2/4, Required Invariants (Tools) — settled),
- the Item 1 spike `.project/active/run-study-reachability-spike/findings.md` (R1-R12, fixture
  contract — proven behavior the design must preserve),
- epic Item 3 (`.project/backlog/epic_run_study_capability.md`).

You are a fresh, skeptical reviewer. Deliver must-fix findings (would produce a wrong or
non-conformant implementation) separated from should-fix and notes; each with evidence
(file:line) and the smallest correct fix. Verify claims against the real package artifacts
(`exploration/stellarator_e2e/pkg/stellarator_tea/`) and the probe (`probe_lineno.py`) where
they are load-bearing — run code if needed, read-only on the committed package.

Specific questions beyond your own sweep:
1. Fingerprint recipe soundness: the recipe globs `pipelines/*.yaml`, `inputs/*.json`,
   `contracts/model_contract.json` — but the reader resolves inputs files from the EntryPoint
   block's declared relative paths. Can the trace ever read a file the recipe did not digest
   (e.g., an entry ref pointing outside inputs/, or a non-.json inputs file)? If yes, that is a
   false gate — name the fix.
2. Appendix A conformance: the spec/design must use Appendix A field names exactly. Does D10's
   identity triple and the report shape keep that (additive only), or does anything rename or
   drop an Appendix A field (entry_type, sibling_candidates, constraints_reachable, bounds,
   objectives_reachable, no_constraint_response)?
3. The strict walker rejects non-standard node tags and accepts "str/map" — does the real
   pipeline YAML contain sequences or other standard tags the walker must also accept? Check
   the actual file.
4. `--group NAME` subset invocation vs the record seam: Item 2 snapshots ONE indicators.json
   covering every proposed axis. Does subset selection create a fragmented-digest hazard, and
   should the design state the full-document invocation as the record-feeding mode?
5. Gate order D8 puts the fingerprint gate before parse; the identity check reads
   package_contract.json which is NOT in the digested file set. Is that consistent and safe?
6. Invariant 5 (every catalog constraint appears in reachable/unreachable AND bounds) vs the
   spike fixture (bounds shown per-axis for reached constraints). Is the shape unambiguous?

Do NOT relitigate: declared-only membership, sound-negative semantics, data-only manifest,
the indicator-input fingerprint's existence, yaml.compose choice (probe-backed), Item 4
authoring the annex, the typed oracle object recording what exists today.

Write your review to `.project/active/run-study-indicators/design-review.md` and end with
verdict: APPROVE, APPROVE-WITH-FIXES (list), or REJECT (reasons).
