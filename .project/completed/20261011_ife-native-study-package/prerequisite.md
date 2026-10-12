# Prerequisite: verifier multiplication operands

[AGENT] T-002 stopped before package implementation. The existing IFE viability predicate is `(eta * gain_in) >= threshold`. `scripts/study/verify.py:176` accepts a top-level comparison but its operand loop at line 192 accepts only literal and feature-reference operands. It rejects the left multiplication node with a named VerifyError. Package metadata or operand bindings cannot change that grammar.

Reproducer: `PYTHONPATH="$PWD" .codex-test/run python .project/active/ife-native-study-package/probe_verifier.py`. It reads the actual audited IFE catalog and defaults, supplies explicit qualified bindings, and invokes the native verifier's `derive_verdict`. The captured return is `verifier-prerequisite.json`. The first invocation omitted the repository PYTHONPATH and failed to import `scripts`; the documented corrected environment produces the actual verifier refusal.

No model, generated package, shared seam, pin or study was changed. Spec/design/plan record the proposed package work, which remains unimplemented. The missing capability needs a separately scoped coding item for the shared verifier, with existing MFE predicate regression coverage and an independent audit. The model's documented multiplication expression should not be rewritten to evade verification.
