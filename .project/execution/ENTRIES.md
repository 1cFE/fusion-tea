# Execution Facts

Append-only log of how this codebase and environment actually behave, discovered while working. Newest at the bottom.

The rules for writing an entry are in `README.md`, in this directory. Do not rewrite or reorder existing entries.

---

## [scripts/study/verify.py] 2026-09-17

**Fact:** A comparison failure exits with stderr before writing the requested `--out` summary. Check exit status before loading that file; a failed run does not emit a verification summary.
**Evidence:** `scripts/study/verify.py:556`; pre-reveal feasibility study `results/generic-verification-refusal.json`, commit `1394d43d`.
