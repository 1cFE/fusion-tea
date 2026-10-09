# PR gate static rerun — 2026-10-08

[AGENT] Repository-wide Ruff lint and formatting still fail at gate entry `f9e1d6564d16c29c6d4e1c20f4a8920eb32cb135`. No autofix was applied. The [full default pytest rerun](20261008-pre-pr-rerun.md) passes independently, with source/evidence preservation verified. The proposed style exception is ratified by the owner on 2026-10-09; repository-wide Ruff results remain FAIL.

## Results

| Check | Baseline identical bytes | Changed existing path | New bytes or path | Total |
|---|---:|---:|---:|---:|
| Lint findings | 152,966 | 142 | 20,837 | 173,945 |
| Files needing formatting | 11,086 | 1 | 1,051 | 12,138 |

Lint affects 11,619 files; 2,362 files already satisfy formatting. A baseline-identical file has the exact Git blob of a file anywhere in remote main `f96ad312c63e8c66695971b12feab971f3ba6eb3`, including archive moves. New bytes include generated and sealed study evidence; this category does not imply permission to reformat.

Forty changed live Python files under tests, scripts and src were inspected. Ten retain 138 lint findings. The [study repair](20261008-study-consumer-repair.md) accounts for 83, the [model/code-generation repair](20261008-model-codegen-repair.md) for 51, and the [comparison repair](20261008-comparison-candidate-repair.md) for four. These are inherited findings, including unused imports, import placement after runtime-path setup, assigned lambdas and long lines. Their repair receipts report no added diagnostic signatures. The study repair preserves runtime import dependencies and arithmetic. The [earlier static review](20261006-pre-pr-static.md) documents generated and sealed evidence bindings and the mechanical cleanup already applied to new mutable material tests. This rerun does not claim that all live code or the full repository satisfies Ruff.

## Scans and merge

Added code diff lines contain no breakpoint, pdb trace, debugger statement, TODO or FIXME candidates. Added diff lines contain no private-key header or common AWS, GitHub or OpenAI token signatures. No changed credential-like file paths were found. Token values were neither printed nor retained; the signature scan cannot prove the absence of every possible secret format.

Thirty-five changed files exceed 5 MB. Twenty-seven have byte-identical baseline blobs. The eight new files are expected material integration snapshot JSON, about 5.9–6.3 MB. The prior static review identifies two byte-identical archived SQLite receipts as retained evidence. No unsuitable new oversized binary was identified. No product-lens artifact changed in this PR diff. The separately authored explorer API-gate product-lens remains outside this scope.

The dry merge against verified remote main exits zero, with virtual merged tree `9da86abb56a343d42163219accc7c540079c1f07`. No index, reference or working file was changed.

## Accepted disposition

[AGENT] Accept the recorded inherited style debt and sealed/generated evidence style findings as exceptions for this PR (ratified by owner, 2026-10-09). [OWNER-VERBATIM] “ok I accept those.” The acceptance covers the documented inherited findings, including the 138 residual findings in changed live tests, and the generated/sealed evidence findings. The complete default suite and source/evidence preservation checks pass. The branch gate is qualified with these exceptions; repository-wide Ruff checks remain FAIL with the exact counts above. This decision applies to this PR and does not change Ruff configuration or declare the files clean.

## Receipts

Runtime commands use `UV_CACHE_DIR=/tmp/fusion-tea-pre-pr-rerun uv run --no-sync ruff check . --output-format=json` and `ruff format --check .`. Logs and classifications: `/tmp/20261008-pre-pr-ruff.json`, `/tmp/20261008-pre-pr-format.log`, `/tmp/20261008-pre-pr-scan.json`. Merge receipt: `/tmp/20261008-pre-pr-merge.log`. The scan uses committed PR diff content, rather than owner-authored uncommitted changes. No holdout sources were read.
