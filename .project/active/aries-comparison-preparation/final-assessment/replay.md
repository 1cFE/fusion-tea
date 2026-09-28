# Reproduce the assessment tables

Run these commands from the repository root using the configured test-worktree interpreter. They read the retained diagnostic run, frozen package and source records. They rebuild only the final-assessment tables; no plant evaluation occurs.

```bash
.codex-test/run python .project/active/aries-comparison-preparation/final-assessment/evidence/quantity-review.py
.codex-test/run python .project/active/aries-comparison-preparation/final-assessment/evidence/cost-assessment.py
.codex-test/run python .project/active/aries-comparison-preparation/final-assessment/evidence/assemble.py
.codex-test/run python .project/active/aries-comparison-preparation/final-assessment/evidence/review-checks.py
```

The quantity builder checks inspected live definitions against the frozen archive. The cost builder checks the archive identity, source-value unit conversions and row census. The combined builder preserves all 276 original rows inside the JSON and joins separately recorded findings. The independent review script checks exact replay, original-row preservation, file hashes and frozen-model parity. A successful script verifies reporting integrity; source interpretation and scientific limits remain in the readable reviews.

The input report is `../partial-assessment/attempts/diagnostic-1/report.json`. Its original request has three supplied reference inputs and 701 held inputs. The archive is `../post-reveal-preparation/package/post-reveal-v1.tar.gz`, SHA256 `d65d6ea44517dba3d9012d06706e74fe3006247e2809f6b4bdd64edd85ab5a7a`. The diagnostic runtime and execution are unchanged and remain identified in `../partial-assessment/adoption.json`.

Source image receipts appear in `evidence/quantity-source-receipt.json`, `evidence/structure-identities.json`, and the per-row records in `evidence/cost-rows.json`. Quantities and costs preserve exact producer and source definitions. No monetary normalization beyond M$ to $ was applied. The original ratio bands and C220107 exclusion remain unchanged.

The [findings log](findings.md) is the write-up record. The [plan](plan.md) tracks completion. The [independent review](evidence/review.md) states the assessed scope. The unrelated design-choice audit remains outside this task's commits.
