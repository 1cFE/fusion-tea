"""Write results/execution-context.json for the design-study-parameters record after execution (facts read from git and the record; commands as run). Adapted from the design-space-combinations goal's writer."""
import json, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
R = ROOT / 'exploration/costed_loop_brayton/studies/20260926-design-study-parameters'
rid = R.name
S = 'exploration/costed_loop_brayton/studies'
git = lambda *a: subprocess.run(['git', *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
PY = 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1'
ctx = {
    'repo_commit_at_execution': git('rev-parse', 'HEAD'),
    'uncommitted_at_execution': [l for l in git('status', '--short').splitlines()],
    'preparation_commands': [
        f".codex-test/run python {S}/flow_ratio_config.py --record {S}/{rid}",
        f".codex-test/run bash -c '{PY} python -m exploration.costed_loop_brayton.studies.study_support prepare --record {S}/{rid} --config {S}/{rid}/config.json'",
        f".codex-test/run bash -c '{PY} python scripts/study/indicators.py --package exploration/costed_loop_brayton/costed_loop_brayton_tea --manifest {S}/{rid}/manifest.json --groups {S}/{rid}/axes.json --out {S}/{rid}/indicators.json'",
        f".codex-test/run bash -c '{PY} python -m exploration.costed_loop_brayton.studies.study_support baseline --record {S}/{rid}'",
        f".codex-test/run bash -c '{PY} python scripts/study/preflight.py gates --package exploration/costed_loop_brayton/costed_loop_brayton_tea --manifest {S}/{rid}/manifest.json --groups {S}/{rid}/axes.json --identity {S}/{rid}/preparation/package_identity.json --baseline-result {S}/{rid}/preparation/baseline_result.json --out {S}/{rid}/preparation/preflight_results.json'"],
    'execution_command': f".codex-test/run bash -c '{PY} python -m exploration.costed_loop_brayton.studies.study_support execute --record {S}/{rid} --integration-return work/orchestration/goals/design-study-parameters/evidence/integration-t004/integration_return.json'",
    'verification_command': f".codex-test/run bash -c '{PY} python -m scripts.study.verify --package exploration/costed_loop_brayton/costed_loop_brayton_tea --manifest {S}/{rid}/manifest.json --identity {S}/{rid}/preparation/package_identity.json --store {S}/{rid}/results/native/{rid}.db --sample-size 272 --out {S}/{rid}/results/verification_summary.json'",
    'reporting_commands': [f".codex-test/run python {S}/flow_ratio_reporting.py {S}/{rid}", f".codex-test/run python {S}/flow_ratio_figures.py {S}/{rid}"],
    'preparation_baseline': 'Two preparations on the same live manifest (pin 53f48a7e…) and package identity: r1 (313 composed, 257 kept) retained under preparation-r1/ after its oracle scan found the refined grid\'s best passing point at 2,250 kg/s / 1.5183 with its flow-step-higher neighbour coinciding with the starting point; r2 (328 composed, 272 kept, 56 refused) adds the declared extra anchor screen-best-passing (2,500 / 1.45). indicators.json and the native baseline point (preparation/) are shared: manifest and axes are identical between r1 and r2. Six preflight gates pass.',
    'pre_execution_review': 'Coordinator checkpoint C-001.r1 in work/orchestration/goals/design-study-parameters/trail.md (no review trigger met beyond the covered integration risk; reused coverage cited); not an independent verdict.',
    'attempts': '272 started, 272 completed in one invocation; no retries. Integration candidate from T-004 (evidence/integration-t004/integration_return.json), same package identity and manifest pin.',
    'verification_outcome': 'REFUSED on one channel of one case (he_hot_bound_margin on s1-turb0.90-f2500-r1.4500, relative 1.466e-9 against the 1e-9 rule, absolute 5.3e-10 K, no declared class); every other channel of every case within the rule or its declared class; all verdicts re-derived. Owner gate G-001 (evidence/owner-gate-verification-class.md); no summary file was written by the verifier; the refusal text is evidence/t005-verify.log.'}
(R / 'results' / 'execution-context.json').write_text(json.dumps(ctx, indent=2) + '\n')
print(json.dumps({'commit': ctx['repo_commit_at_execution'], 'uncommitted': len(ctx['uncommitted_at_execution'])}))
