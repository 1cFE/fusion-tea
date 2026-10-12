# Product-lens ledger

## audit — 2026-09-11 — rev 676c7308

Point (re-derived): A non-builder can operate and interpret the repaired plant through documented routes; the independent oracle carries audited held inputs while its contract remains active. [source: `.project/concepts/goal-driven-model-development-harness.md`, owner-verbatim; `.project/adr/0010-oracle-mirrors-audited-bindings.md`, owner]

Falsifier: Installed reserve silently changes operating demand, or verification compares different plants.

Findings:

- audit-F1 [DON'T] Graph expectations are duplicated between six JSON fixtures and `tests/study/test_known_answers.py:33`; the refresh caller regenerates the JSON while the Python contract needs separate review and editing. Source: an [AGENT] inference from the owner's clean-patterns requirement. Falsifier: refresh after an intended graph change and observe obsolete Python expectations fail. Disposition: `audit.md` → Product Judgment.

Fired smell: Two representations must be manually kept synchronized.

Gate: DISPOSED (audit-F1)

Resolves:

- audit-F1: DEFERRED — authority: AGENT — basis: The qualitative regression contract deliberately remains an independently reviewed expectation; refreshing native graph output must not automatically bless that contract. The repeated mechanical counts add maintenance cost, but are checked against the same native graph and cannot silently diverge. This bounded migration has rederived and checked both representations. No producer invariant or user-facing output depends on manual synchronization. Consolidating redundant mechanical expectations remains optional test cleanup, without weakening the separate qualitative assertions.

Fresh reviewer: Codex ephemeral session `01a0927f-3a41-7b80-8aa7-a3cc90b24a50`, read-only, no history fork. Full verdict and oracle-first transcript are retained in `audit-evidence/product-lens-verdict.txt` and `product-lens.jsonl`. The reviewer recommended DISPOSE-and-proceed and found no owner-grade contradiction. This is the ledger's only block; no epic gate is declared for this standalone coding item. The auditor owns the disposition above.
