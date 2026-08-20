# Brief: design for "Quality Tools and Era Adapter Promotion" (RUN-STUDY Item 4)

Work item home: `.project/active/run-study-quality-tools/` — spec.md is ACCEPTED; write
design.md. This is the riskiest item in the epic: take the design time to get the seams right.

## Task

Design `scripts/study/preflight.py`, `scripts/study/verify.py`,
`exploration/stellarator_e2e/studies/era_adapter.py`, the annex, the promotion-equivalence
harness, and the negative-proof tests — to the spec's contract. The spec's Known Requirements
are settled; your job is its eight Open Questions:

1. How an executed baseline point reaches preflight (no execution in preflight, no adapter
   import). Weigh: consume an already-executed result vs a prepared-evaluator handle.
2. The identity-document seam the adapter emits (schema, name, home directory — coordinate
   with Item 3's scripts/study/schemas/ convention) and whether it also carries the glue
   ledger or the adapter emits two documents.
3. The package-owned oracle entry point (CLI on verify_stellaris.py vs shim module) and the
   manifest oracle field form (pre-authorized additive {"kind":"cli"} vs python_callable with
   a defined generic signature).
4. verify.py sampling source: StudyQuery store vs exported CSVs.
5. Exact verification_summary.json field list — Item 2's plan has now written the snapshot
   field list in full; read `.project/active/run-study-contract/plan.md` Phase 3 and the
   design's arms[].verification block; make the summary a superset.
6. Default sample size/seed and their scope (proof-of-life used K=12 per CSV, fixed seed).
7. Where the promotion-equivalence definition lives; kept as regression or retired as
   one-time evidence (retires with the adapter either way).
8. Whether preflight/verify share an internal module.

## Constraints and context

- Items 2 and 3 are implementing IN PARALLEL right now. Design against their ACCEPTED designs
  (`.project/active/run-study-contract/design.md`, `.project/active/run-study-indicators/design.md`),
  not their in-flight code. Where your design consumes their files (manifest.py, schemas),
  cite the design; the plan stage will bind to the real files once they land.
- The era teax pin: worktree /home/reid/1cfe/teax-v1-era @ fa0e06a. You may READ that worktree
  and the proof-of-life script to design the loader exception and StudyRunner route — read-only.
- Prototype where a design question genuinely needs it (e.g., can PreparedListStrategy be
  driven exactly as the proof-of-life did under the promoted structure?); throwaway probes in
  the work-item folder.
- Working voice; provenance grades carried from the spec.
