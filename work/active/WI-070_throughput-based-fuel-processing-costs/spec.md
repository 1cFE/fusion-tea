---
Status: active
Scale: standard
Epic: standalone
Owner: agent
Created: 2026-09-19
Updated: 2026-09-19
---
# WI-070: Throughput-based fuel processing costs

## Contract and authority

[NEED] Make the stellarator processing-plant capital follow computed operating throughput, with applicable sources and explicit equipment/account boundaries, and integrate it into plant capital and electricity cost. The exact R10.S2 target is “Processing-plant cost follows computed throughput with source basis.” Source: `work/orchestration/goals/throughput-based-fuel-processing-costs/evidence/owner-prompt.md`, required results 1–8. S2 permits a justified aggregate; a full equipment design is not required.

[NEED] Preserve fuel losses, recovery, residence times, physical producer outputs, existing constraints/failures, the sealed holdout, historical studies and published r2. Source: same owner prompt, Limits. No merge, push, reveal, comparison replacement or formal goal closure is authorized by this item.

[AGENT] The conventional palladium-alloy cleanup/impurity-treatment and cryogenic-isotope-separation scenario was ratified by the owner on 2026-09-19 (“yes, adopt and continue”); see goal.md Owner amendment and the retained Owner ruling. It remains conditional on source-like impurities and cleaned feed below 1 ppm noncondensibles. Owner adoption is not a measured-purity or guaranteed-recovery fact. The already completed source/price reviews apply; no duplicate source search is planned.

[INHERITED] Required reading: `knowledge/holdout/aries-cs/PROTOCOL.md`, `.agentic-mbse/codex.md`, `.project/codex-test-setup.md`, `modeling_project/MODELING_PROCESS.md` and `modeling_project/REQUIREMENTS.md`. Follow MR-1 CAS ownership, MR-2 costed interfaces, MR-3 library/configuration separation, MR-4 source citations and MR-6 established patterns. Exclude all barred materials and `.project/concepts/stellarator-mbse-demo.md`.

## Acceptance requirements

| ID | Provenance | Observable outcome |
|---|---|---|
| MR-070-01 | [NEED], owner results 1–2 | The active estimate consumes the WI-069 operating D+T plasma-exhaust inlet, before recovery. It does not recompute mass balance or use annual average, T-only mass, inventory or electrical power. Disable/undefined semantics remain truthful. |
| MR-070-02 | [NEED], owner result 3; [INHERITED], approved source/price reviews | Preserve each of four historical raw capital/direct-installation rows, expenditure-year assumptions, CPI conversion, common 2.08e-5 kg D+T/s reference and 0.3 exponent. Reproduce the reviewed source-capacity and current-flow examples. Label 2025 CPI purchasing power rather than contemporary procurement cost. |
| MR-070-03 | [NEED], owner results 4–5; [INFERRED], explicit controls allocation | Replace C220500 exactly once, retain a dormant generic legacy route, expose purchased/fabricated and direct-installation sums, and reconcile shipping, tax, insurance, indirects and finance without an overlapping residual allowance. Package-local controls belong exclusively to C220500; the retained C220700 coefficient is an uncalibrated allowance for distinct supervisory/plasma functions under an explicit agent accounting convention. |
| MR-070-04 | [NEED], owner results 3,6–7; [INFERRED], interface design | Separate capacity margin, source-price multiplier and containment-date sensitivity; document module basis and finite domains, zero-flow limit and external applicability. No fabricated certified capacity or full-train redundancy. |
| MR-070-05 | [NEED], owner results 1,5 | Keep fuel purchases, startup proxy, torus vacuum/fueling and civil facilities separate. Preserve source-local controls and limited purchased containment; disclose additional plant-wide services, storage, blanket extraction/conditioning, full design/inspection, OPEX and replacements not established by this block. |
| MR-070-06 | [NEED], owner results 6–8 | Verify source rows, dimensional/limit behavior, public native off-reference flow-to-cost-to-total response, price-only physical invariance, module accounting, generic legacy parity, independent oracle coverage and affected regressions. Retain static-diagnostic deltas and native integration/study evidence. Independent review must trace actual outputs before any S2 claim. |

## Artifacts and ownership

The item owns canonical/twin model changes, generated package, independent oracle/adapter and meaningful tests. `design.md` defines architecture and domains; `evidence/proposed-abi.md` defines intended keys; `evidence/account-reconciliation.md` defines account arithmetic and unresolved scope. Coordinator owns goal records, git checkpoints, native integration and native studies. No scientific implementation begins until independent design release.

## Persistent execution checklist

- [x] Reuse reviewed sources, owner adoption, current producer trace and price example; inspect affected cost/financial consumers and generation procedure.
- [x] Write specification, architecture, proposed ABI and account reconciliation, including the explicit I&C allocation.
- [x] Obtain independent design/accounting release and resolve material findings. Goal evidence/design-review.md PASS; stock mass is per module and attached selected cost is plant-total.
- [x] Capture entering package/model/static identities and affected baseline checks; register exact normative seed additions/changes.
- [x] Implement canonical/twin calculation, costed processor ownership, stellarator configuration, account selection and installation freight exclusion.
- [x] Regenerate twice from reviewed strict seeds, preserving unrelated manual bodies; update oracle/adapter and verify all new outputs.
- [x] Complete reference, domain, off-reference, physical-preservation, generic-consumer and accounting tests; compare static diagnostics by identity.
- [x] Refresh package metadata/snapshot/census and verification records (SV-117/SV-118 passing).
- [x] Obtain independent implementation review before coordinator integration. See audit.md; candidate committed at 2a50d3ec.
- [x] Coordinator executes native integration and focused study; author repairs affected findings and supplies exact evidence for fresh R10.S grading. Integration and 20-case study at 2bae7fb7 pass; fresh independent R10.S = 2 in the goal evidence/final-review-and-grade.md.

## Source and review references

- Goal `evidence/proposed-cost-scope.md`, `proposed-price-review.md`, `source-review-r2.md`, `current-trace.md`, `interface-review.md`, and `proposed-price-example.json`. Historical status sentences in pre-adoption artifacts do not reopen the owner's later adoption.
- `knowledge/research/pending/20260919-091411_throughput-based-fuel-processing-cost-applicability.md` and `20260919-092112_conventional-reactor-fuel-processing-transfer.md`; source checkpoint 66548f14.
- Upstream audited producer 956444b5; WI-069 model/interface records and unchanged 144-test entering verification in the goal trace.

## Current status

Independent implementation audit passed; native integration returned CANDIDATE with all ten gates passing at model commit 2a50d3ec. Source/domain tests: 172 passing; affected native/oracle/accounting tests: 263 passing; family generation/ABI tests: 13 passing. Static L2/L6 failures remain explicitly classified in evidence/author-validation.md. The frozen 20-case study passes all mapped checks and fresh independent review assigns R10.S = 2. Goal closure remains owner-held; this implemented item stays at its cited path for reproducibility. The controls allocation follows goal evidence/controls-review.md; its retained coefficient is not a historically disaggregated price.
