"""Write results/execution-context.json for the design-choice interactions record after execution and verification (facts read from git and the record; commands as run)."""
import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
R = ROOT / 'exploration/aries_integrated/studies/20260926-aries-design-choice-interactions'
rid = R.name
git = lambda *a: subprocess.run(['git', *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
PY = 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1'
ctx = {
    'repo_commit_at_execution': git('rev-parse', 'HEAD'),
    'uncommitted_at_execution': [l for l in git('status', '--short').splitlines()],
    'preparation_commands': [
        "python work/orchestration/goals/design-space-combinations/evidence/make-interactions-config.py",
        f".codex-test/run bash -c '{PY} python -m exploration.aries_integrated.studies.interactions_support prepare --record exploration/aries_integrated/studies/{rid} --config exploration/aries_integrated/studies/{rid}/config.json'",
        f".codex-test/run bash -c '{PY} python scripts/study/indicators.py --package exploration/aries_integrated/aries_integrated --manifest exploration/aries_integrated/studies/{rid}/manifest.json --groups exploration/aries_integrated/studies/{rid}/axes.json --out exploration/aries_integrated/studies/{rid}/indicators.json'",
        f".codex-test/run bash -c '{PY} python -m exploration.aries_integrated.studies.interactions_support baseline --record exploration/aries_integrated/studies/{rid}'",
        f".codex-test/run bash -c '{PY} python scripts/study/preflight.py gates --package exploration/aries_integrated/aries_integrated --manifest exploration/aries_integrated/studies/{rid}/manifest.json --groups exploration/aries_integrated/studies/{rid}/axes.json --identity exploration/aries_integrated/studies/{rid}/preparation/package_identity.json --baseline-result exploration/aries_integrated/studies/{rid}/preparation/baseline_result.json --out exploration/aries_integrated/studies/{rid}/preparation/preflight_results.json'",
        f".codex-test/run bash -c '{PY} python -m exploration.aries_integrated.studies.interactions_support scan --record exploration/aries_integrated/studies/{rid}'"],
    'execution_command': f".codex-test/run bash -c '{PY} python -m exploration.aries_integrated.studies.interactions_support execute --record exploration/aries_integrated/studies/{rid} --integration-return work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/integration-attempt2/integration_return.json'",
    'verification_command': f".codex-test/run bash -c '{PY} python -m scripts.study.verify --package exploration/aries_integrated/aries_integrated --manifest exploration/aries_integrated/studies/{rid}/manifest.json --identity exploration/aries_integrated/studies/{rid}/preparation/package_identity.json --store exploration/aries_integrated/studies/{rid}/results/native/{rid}.db --sample-size 52 --out exploration/aries_integrated/studies/{rid}/results/verification_summary.json'",
    'reporting_command': f".codex-test/run python -m exploration.aries_integrated.studies.interactions_reporting exploration/aries_integrated/studies/{rid}",
    'preparation_baseline': 'Two preparations: r1 (43 points) retained under preparation-r1/ after its oracle scan refused eight B3 points and showed the temperature level inert on the N base; r2 (52 points, six aliases) prepared on the same live manifest with the windows fixed by the oracle-only probe work/orchestration/goals/design-space-combinations/evidence/window-probe.txt. Native baseline point executed once into preparation/ for each preparation; six preflight gates pass on both.',
    'pre_execution_review': 'Coordinator checkpoint C-001.r1 in work/orchestration/goals/design-space-combinations/trail.md (no review trigger met; reused coverage cited); not an independent verdict.',
    'attempts': '52 started, 52 completed in one invocation; no retries. Integration candidate reused from round 2 of the reconciliation goal (same package identity, same manifest pin).'}
(R / 'results' / 'execution-context.json').write_text(json.dumps(ctx, indent=2) + '\n')
print(json.dumps({'commit': ctx['repo_commit_at_execution'], 'uncommitted': len(ctx['uncommitted_at_execution'])}))
