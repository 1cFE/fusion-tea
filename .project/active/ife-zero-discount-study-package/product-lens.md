# Product-lens ledger

## audit — 2026-09-11 — rev 811a611b

Point (re-derived): Carry audited model changes into reproducible, independently verifiable study inputs that a non-builder can operate. [sources: README.md § End-to-End Workflow, grade: INHERITED; docs/integration_seam_operator_guide.md and .project/adr/0009-integration-is-a-fixed-point-proof.md, grade: AGENT; .project/concepts/goal-harness-design.md § Owner’s Words, grade: OWNER]

Falsifier: A zero-discount case receives a route-adjusted answer inconsistent with generated computation, or metadata regeneration produces a different identity.

Findings:

- audit-F1 [DO] Explicitly disposition inherited manual synchronization of oracle defaults and model inputs. Smell: **Two representations must be manually kept synchronized.** Source: .project/concepts/goal-harness-design.md’s clean operating patterns (AGENT inference). Falsifier: change a held model input while leaving the oracle default unchanged. Disposition: audit.md § Product Judgment retains the independent arithmetic reference with full-input coverage and baseline parity checks. ADR-0010’s stellarator-specific owner ruling is not IFE authorization.

No new product contradiction found. Both discount factors enter required publication and independent verification. Tests cover zero and tiny signed rates across positive, negative and zero net generation. Fractional-duration verification limits are disclosed. No other code/test smells fired. The fresh lens read code; the audit agent independently executed validation.

Gate: DISPOSED (audit-F1)
