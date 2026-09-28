#!/usr/bin/env bash
# Runbook step 10a: generic stratified verification per arm against the package-owned oracle.
set -euo pipefail
cd /home/reid/1cfe/fusion-tea
REC=exploration/stellarator_e2e/studies/20260914-magnet-coil-realism
export PYTHONPATH=$PWD:$HOME/1cfe/teax/packages/teax-simkit:$PWD/exploration/stellarator_e2e/pkg
for arm in arm-a-transect arm-R-transect arm-matched-window; do
  uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env python scripts/study/verify.py \
    --package exploration/stellarator_e2e/pkg/stellarator_tea --manifest exploration/stellarator_e2e/studies/manifest.json \
    --identity $REC/results/package_identity.json --store $REC/results/$arm/_work/20260914-magnet-coil-realism-$arm.db \
    --sample-size 20 --out $REC/results/verification_summary-$arm.json 2>&1 | tail -3
done
echo VERIFY_DONE
