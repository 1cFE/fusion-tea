"""Reproduce WI-048 source-oracle cases and the pre-repair generated baseline.

Run from repository root with .codex-test/run python <this-file>.
Reads the approved plan commit's IFE model files; writes no historical artifact.
"""
from pathlib import Path
import os
import sys
import json
import subprocess
import tempfile

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
from sysml_codegen.cli import GenerationConfig, run_codegen
from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.bridge import CandidateBridge
from tests.model_families import IFE, canonical_path
from tests.ife_oracle import PREFIX, MUTATIONS, BOUNDARIES, source_oracle, assert_source_outputs
from scripts.verify_ife_lcoe import compute_ife_lcoe

item = Path(__file__).parent
scratch = Path(tempfile.mkdtemp(prefix='wi048-evidence-'))
package = REPO/'exploration/ife_e2e/generated'
evaluator = PreparedEvaluator(ProvisionalPackageLoader(package,'ife_tea',scratch/'new-link'),
                              package/'pipelines/pipeline.yaml',expects_constraint_report=True)
bridge = CandidateBridge(evaluator.entry_models)
records = {}
for name, overrides in (MUTATIONS | BOUNDARIES).items():
    result = evaluator.evaluate(bridge.build({PREFIX+k:v for k,v in overrides.items()}))
    records[name] = dict(overrides=overrides, outputs=dict(result.outputs), responses=dict(result.responses))
    if name in MUTATIONS:
        assert_source_outputs(result.outputs, overrides)
        expected = source_oracle(overrides)
        records[name]['independent_oracle'] = expected
        records[name]['max_relative_residual'] = max(abs(result.outputs[k]-v)/abs(v) for k,v in expected.items() if v)
old_revision = 'd953f12c'
for logical in IFE.owned:
    path = scratch/'old-models'/logical
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(subprocess.check_output(['git','show',f'{old_revision}:{canonical_path(logical).relative_to(REPO)}']))
old_package = scratch/'wi048_old'
assert run_codegen(GenerationConfig(models_path=scratch/'old-models', output_path=old_package,
                                    package_name='wi048_old', overwrite=True))
old_evaluator = PreparedEvaluator(ProvisionalPackageLoader(old_package,'wi048_old',scratch/'old-link'),
                                  old_package/'pipelines/pipeline.yaml',expects_constraint_report=True)
old = old_evaluator.evaluate(CandidateBridge(old_evaluator.entry_models).build({}))
# Explicit old inputs, including the independently held bank energy and power denominators.
old_procurement = (0.32+0.088*5)*(1.25+0.05)*(1+0.0088*(3.5-5))
old_gamma = old_procurement*1e9/(5e6/0.35)
old_oracle = compute_ife_lcoe(availability=0.9,blanket_energy_multiple=1.15,discount_rate=0.08,
    driver_cost_constant=old_gamma,driver_efficiency=0.35,driver_energy=14.286e6,
    driver_lifetime_shots=6e9,frequency=3.5,gain=80.0,om_cost_constant=65.0,
    plant_cost_constant=2000.0,target_cost_constant=10.0,thermal_efficiency=0.43,yield_cost_constant=5e6)
old_meier_capital = 1.83*(0.66*(2.054/1.67)**0.49+old_procurement+0.1)
old_meier_coe = 0.113*old_meier_capital/(0.0876*0.9*1.0)
assert abs(old.outputs[PREFIX+'lcoe_calc__lcoe']/old_oracle['lcoe_per_MWh']-1)<1e-9
assert abs(old.outputs[PREFIX+'meier_coe_calc__coe_cents_kwh']/old_meier_coe-1)<1e-9
records['pre_repair'] = dict(revision=old_revision, outputs=dict(old.outputs), responses=dict(old.responses),
                           independent_hawker=old_oracle,independent_meier=old_meier_coe)
(item/'execution-evidence.json').write_text(json.dumps(records,indent=2)+'\n')
print('Independent baseline/mutations and nine public executions passed.')
print('Old prices:',old.outputs[PREFIX+'lcoe_calc__lcoe'],old_meier_coe)
print('New prices:',records['baseline']['outputs'][PREFIX+'hawker_price__price'], records['baseline']['outputs'][PREFIX+'meier_price__price'])
print('Maximum relative oracle residual:',max(records[n]['max_relative_residual'] for n in MUTATIONS))
