# Brief: design for "Indicator Tool and Package Manifest" (RUN-STUDY Item 3)

Work item home: `.project/active/run-study-indicators/` — spec.md is ACCEPTED there; write design.md.

## Task

Design `scripts/study/indicators.py`, the `manifest.json` schema, the output JSON schema, and
the test architecture, to the spec's contract. The spec's Known Requirements and its four
recorded decisions are settled; your job is the spec's "Open Questions / Deferred to design":

1. CLI surface: how declared groups are supplied (file / args / both), multi-group invocation,
   output destination.
2. Manifest schema: exact field names, nesting, schema_version.
3. Output schema documentation form (prose / JSON Schema / both) and how Items 2 and 4 cite it.
4. Line numbers through YAML load: keep them if cheap (corrupt-artifact errors locate by
   file+line), else file+key-path per the spec's accepted weaker bar.
5. Test layout under tests/; how synthetic multi-pipeline and corrupt-artifact fixtures are
   built WITHOUT mutating the committed package (temp copies).
6. How the not-derivable statements ride in every report.
7. The indicator-input fingerprint's exact digest recipe (which files, what order, what
   canonicalization) — the tool computes it, the manifest pins it.

## Orchestrator rulings since the spec (record these in the design)

- The package annex file (runbook's package-specific companion) is authored by **Item 4**,
  not this item. Your manifest is data-only and stands alone; the annex will live beside it.
- The manifest's oracle field records the importable entry point as it exists today. Design
  the field so a later amendment to a command form is additive (e.g., a typed entry-point
  object), because Item 4's verify.py will consume this seam and may add a package-owned CLI.
- Item 2's accepted record contract snapshots your output (`indicators.json` + digest + your
  schema version) into every study record — version the output schema from v1 and include the
  schema version in the output itself.

## Constraints

- Generic tool: no stellarator name, no key prefix, no adapter import (grep-clean criterion).
- Design for the plan/implement stages to build with tests; keep the design concrete enough
  that implementation makes no architectural choices.
- Prototype only if a design question genuinely needs it (e.g., line-number retention);
  throwaway probes go in the work-item folder.
- Working voice rules; provenance grades carried from the spec.

## Read

- `.project/active/run-study-indicators/spec.md` (the contract)
- `.project/active/run-study-reachability-spike/findings.md` + `trace.py`, `cases.py` (reference)
- `.project/concepts/run-study-skill-design.md` — indicator builder, manifest, Appendix A
- `.project/active/run-study-contract/spec.md` — the record-contract seam your output feeds
