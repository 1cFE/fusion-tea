"""Replay the actual entering generated package to preserve exact boundary signs.

Prerequisite: git archive f76ec031951d7918fbfec2de23d298830941c121
exploration/stellarator_e2e/generated extracted under /tmp/wi065-entering-package.
This is an implementation regression capture, not a new parameter study.
"""
import json, os, sys
from pathlib import Path
ROOT=Path.cwd(); H=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'exploration/stellarator_e2e/studies'),str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit')]
from simkit.study.bridge import CandidateBridge
import study_route
P=study_route.P
package=Path('/tmp/wi065-entering-package/exploration/stellarator_e2e/generated')
evaluator=study_route.prepare(package,Path('/tmp/wi065-entering-negative-runtime'))
bridge=CandidateBridge(evaluator.entry_models)
rows=[]
for sized in [False,True]:
    point={P+'plasma__R':13.5,P+'plasma__a':1.5,P+'magnet__coil__I_coil':16e6}
    if sized:point|={P+'magnet__winding_pack__sizing_mode':1.,P+'magnet__coil__coil_t':.65,P+'magnet__casing__interior_y':.65}
    result=evaluator.evaluate(bridge.build(point))
    rows.append({'sized':sized,'point':point,'outputs':dict(result.outputs),'responses':dict(result.responses)})
(H/'negative-native-cases.json').write_text(json.dumps({'entering_commit':'f76ec031951d7918fbfec2de23d298830941c121','cases':rows},indent=2)+'\n')
print([(r['sized'],r['responses'][next(k for k in r['responses'] if 'reference_conductor_current_ok' in k)]) for r in rows])
