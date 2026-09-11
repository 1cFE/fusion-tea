# Plan: IFE native study package

**Status:** Approved; all work below authorized by goal T-002
**Created:** 2026-09-10

## One phase — package preparation and verification

- [ ] Implement the qualified oracle adapter and explicit predicate bindings.
- [ ] Implement the stock stored execution/baseline route with complete output/verdict checks and audited price eligibility.
- [ ] Add reproducible metadata preparation, native snapshot/census, manifest, beam/rate groups and package annex.
- [ ] Test real baseline, mutations, non-generation, verifier parity and refusal behavior; prove the audited generated package is unchanged.
- [ ] Run the existing integration procedure, resolving only package-specific preparation defects within scope; retain its native return.
- [ ] Obtain a fresh `$my-audit` certification, repair concrete findings if necessary, and return the reviewed candidate to the goal. Owner-held close/archive remains separate.

## Implementation notes

Preparation stopped before implementation: the actual IFE viability predicate contains a multiplication operand that `scripts/study/verify.py` cannot evaluate. See `prerequisite.md` and its reproducer. Repairing that shared seam is outside this item's authorized scope. Requirements and design remain for a later goal task; no package metadata, route or candidate was produced. All Python and model commands use `.codex-test/run`; no environment synchronization is authorized. Candidate promotion belongs to the goal's return decision after certification.
