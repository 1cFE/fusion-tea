# Pre-PR Gate — feat/wi033-p-pump-rebase — 2026-08-28

**Verdict: NOT READY — one finding, owner routing decision required.** Every check except the
canonical battery is clean; the battery's 21 reds have one diagnosed cause, and it is a designed
refusal, not a defect. No fix belongs on this branch under the owner's standing fence.

## Scope

WI-033 complete: 12 commits `65780622`…`83ccd8f9` (open → C-FIX registry raw.pdf fix →
C-REG-CIS `39bd3b41` → C-REG-MOS `891b95bc` → C-MODEL `ffb22724` → C-TESTS `18a5ce86` →
C-FLIP `9f0019e8` → C-CLOSE `50ff326c` → audit `7d57f6a4` POSITIVE → close `83ccd8f9`).
41 files, +1427/−15. Item archived at `work/completed/20260828_WI-033_p-pump-rebase/`.

## Checks run

| Check | Result |
|---|---|
| Canonical battery (both env files) | **550 passed, 13 failed, 8 errors, 14 skipped** — all 21 reds in `tests/study/test_integrate_*` , single cause below |
| `tests/models` standalone | 48 passed / 13 skipped |
| `tests/research` standalone | 150 passed (includes the new PDF-URL regression test) |
| `scripts/source_registry.py verify` | 0 faults, 3 known legacy |
| `agentic-mbse status` warnings | 5 = pre-branch baseline (3 epic mismatches, 2 matrix type nits) |
| Debug artifacts / secrets in added lines | none / none |
| `.project/` paths in diff | 0 — no coding-PM items in scope; WI-033 is modeling-PM (no product-lens stage in that system, per precedent). No expected ledgers → gate satisfied vacuously |
| Large binaries | 2 intentional: registered raw PDFs (`3.7 MB` Cismondi, `0.97 MB` Moscato) — registry-authored artifacts |
| Fresh audit | POSITIVE, 9/9 checks (`work/analysis/20260828-151552_audit_WI-033_p-pump-rebase.md`) |

## The finding — mandate fence meets the live-tree integrate tests

Every red test is Item 3's integrate-seam suite. Its fixture is **the committed stellarator
package as it stands plus the live models tree** (`tests/study/test_integrate_success.py:3`,
`tests/study/conftest.py:21-23`). The seam's regeneration gate regenerates from the model on
the pin and compares to the committed package; with `p_pump` 195.0 in the model and 1.0 in the
package it returns BLOCKER `package-not-integrated` ("regenerating on the pin rewrote the
package … 5 file(s) moved"). Cascade: 8 setup errors (success fixture asserts CANDIDATE),
13 failures (tests expect CANDIDATE or a refusal at a specific later gate — 4/6/7/9 — and get
the regeneration gate first).

**This is ADR-009's designed refusal surfacing in the battery**: the seam refuses model work
that has not been regenerated and committed. The WI-033 mandate explicitly fences regeneration
out ("waits on the `integrate` seam — GSTH Item 6"), so the divergence window is owner-ruled —
but it cannot ship green. What the planning missed: Item 3's tests run the real seam against
the live tree inside the canonical battery, so the "designed detection" also reddens the gate.

## Options (owner decision)

- **(a) Ride with Item 6 — recommended.** No PR now. Item 6 runs on this branch; its integrate
  run regenerates and commits the package through the seam (exactly what the fence defers to),
  the battery goes green, one PR ships WI-033 + Item 6. Honors the fence, the seam, and the
  green-gate bar; the divergence window never exists on `main`.
- **(b) Merge now with a documented red window.** 21 known-red tests on `main` until Item 6 —
  degrades the battery for every other branch. Not recommended.
- **(c) Regenerate inside WI-033.** Violates the owner's explicit fence and bypasses the
  integrate-seam proof Item 6 exists to run. Not recommended.

## Incidents at the gate

None mechanical. The collision above is the gate doing its job; it was surfaced, not worked
around (capture-fidelity Rule 4).
