#!/usr/bin/env bash
set -euo pipefail
# Run only after independent audit and scoped candidate commit.
candidate_commit="${1:?Supply the audited WI-071 commit}"
.codex-test/run python scripts/integrate.py \
  --audited-work "work/active/WI-071_shared-fabrication-rate-for-estimate-uncertainty@${candidate_commit}" \
  --models-root exploration/stellarator_e2e/models \
  --package exploration/stellarator_e2e/generated \
  --manifest exploration/stellarator_e2e/studies/manifest.json \
  --groups tests/study/data/axes.known_answers.json \
  --census-file tests/models/data/mfe_census.json \
  --expected-semantic-fingerprint ea1555ea133db8ed7ba1c638b29ddf540ba99d811bfcf7d9ef9454b626d3a28a \
  --expected-executable-fingerprint b032da4a3971979792bc024bf9cd1a41a2d83d340bad5b59ef3e1a9aeaa77236 \
  --expected-teax-revision 8d877460ac4f6f264561d916e40c1708adb13397 \
  --route-sys-path exploration/stellarator_e2e/studies \
  --route-module study_route \
  --route-callable execute_baseline \
  --out-dir work/orchestration/goals/cost-estimate-maturity-and-uncertainty/evidence/integration
