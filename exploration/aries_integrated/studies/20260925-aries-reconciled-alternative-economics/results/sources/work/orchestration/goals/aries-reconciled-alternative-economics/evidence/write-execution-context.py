"""Write results/execution-context.json for the reconciled-alternative economics record after execution and verification (facts read from git and the record; commands as run)."""
import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
R = ROOT / 'exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics'
rid = R.name
git = lambda *a: subprocess.run(['git', *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
attempts = sys.argv[1] if len(sys.argv) > 1 else '64 started, 64 completed in one invocation; no retries.'
PY = 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1'
ctx = {
    'repo_commit_at_execution': git('rev-parse', 'HEAD'),
    'uncommitted_at_execution': [l for l in git('status', '--short').splitlines()],
    'preparation_commands': [
        f".codex-test/run bash -c '{PY} python -m exploration.aries_integrated.studies.alternative_economics_support prepare --record exploration/aries_integrated/studies/{rid} --config exploration/aries_integrated/studies/{rid}/config.json'",
        f".codex-test/run bash -c '{PY} python scripts/study/indicators.py --package exploration/aries_integrated/aries_integrated --manifest exploration/aries_integrated/studies/{rid}/manifest.json --groups exploration/aries_integrated/studies/{rid}/axes.json --out exploration/aries_integrated/studies/{rid}/indicators.json'",
        f".codex-test/run bash -c '{PY} python -m exploration.aries_integrated.studies.alternative_economics_support baseline --record exploration/aries_integrated/studies/{rid}'",
        f".codex-test/run bash -c '{PY} python scripts/study/preflight.py gates --package exploration/aries_integrated/aries_integrated --manifest exploration/aries_integrated/studies/{rid}/manifest.json --groups exploration/aries_integrated/studies/{rid}/axes.json --identity exploration/aries_integrated/studies/{rid}/preparation/package_identity.json --baseline-result exploration/aries_integrated/studies/{rid}/preparation/baseline_result.json --out exploration/aries_integrated/studies/{rid}/preparation/preflight_results.json'",
        f".codex-test/run bash -c '{PY} python -m exploration.aries_integrated.studies.alternative_economics_support scan --record exploration/aries_integrated/studies/{rid}'"],
    'execution_command': f".codex-test/run bash -c '{PY} python -m exploration.aries_integrated.studies.alternative_economics_support execute --record exploration/aries_integrated/studies/{rid} --integration-return work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/integration-attempt2/integration_return.json'",
    'verification_command': f".codex-test/run bash -c '{PY} python -m scripts.study.verify --package exploration/aries_integrated/aries_integrated --manifest exploration/aries_integrated/studies/{rid}/manifest.json --identity exploration/aries_integrated/studies/{rid}/preparation/package_identity.json --store exploration/aries_integrated/studies/{rid}/results/native/{rid}.db --sample-size 64 --out exploration/aries_integrated/studies/{rid}/results/verification_summary.json'",
    'reporting_command': f"uv run python -m exploration.aries_integrated.studies.alternative_economics_reporting exploration/aries_integrated/studies/{rid}",
    'preparation_baseline': 'Native baseline point executed once into preparation/ after the r1-revised 21-axis declaration; preflight on the unchanged live manifest (six absolute tolerances as re-pinned and amended in round 2 of the prior goal); the pre-revision preparation retained under preparation-r1/.',
    'pre_execution_review': 'work/orchestration/goals/aries-reconciled-alternative-economics/evidence/pre-execution-review.md (fresh reviewer; r1 FINDINGS applied; r2 verdict recorded in the goal trail, Checkpoint C-001).',
    'attempts': attempts + ' Integration candidate reused from round 2 of the prior goal (same package identity, same manifest pin).'}
(R / 'results' / 'execution-context.json').write_text(json.dumps(ctx, indent=2) + '\n')
print(json.dumps({'commit': ctx['repo_commit_at_execution'], 'uncommitted': len(ctx['uncommitted_at_execution'])}))
