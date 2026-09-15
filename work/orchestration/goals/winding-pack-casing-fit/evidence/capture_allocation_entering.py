"""Capture held entering equations at extra radial allocations; no production edits."""
import json
from pathlib import Path
from exploration.stellarator_e2e.studies import oracle_entry as oe, study_route as route
from scripts.study.verify import derive_verdict, package_input_values
H=Path(__file__).resolve().parent
# Explicit capture-only mapping to an existing independently computed oracle input.
# This key was already public in the entering native package; its oracle mapping was absent.
oe.ENTRY_KEY_TO_ORACLE_INPUT[oe.P+'magnet__coil__coil_t']='coil_t'
anchors=[('reference',{})]+[(f'oldpass{j}',{oe.P+'magnet__winding_pack__j_wp':oe.vs.IN['magnet_j_wp']*j,oe.P+'magnet__winding_pack__B_max':30.,oe.P+'magnet__coil__I_coil':17e6}) for j in (.8,1.,1.2)]
catalog=route._catalog_by_constraint_id(route.PACKAGE_DIR)
params=package_input_values(route.PACKAGE_DIR);bindings=oe.operand_bindings()
rows=[]
for anchor,point in anchors:
    for thickness in (.4,.5,.6):
        point=point|{oe.P+'magnet__coil__coil_t':thickness}
        channels=oe.evaluate(point)
        verdicts={e['source_local_identity']:('satisfied' if derive_verdict(cid,e,bindings,point,params,channels)[0] else 'violated') for cid,e in catalog.items()}
        rows.append({'id':f'alloc-{anchor}-{thickness}', 'arm':'radial-allocation','point':point,'channels':channels,'verdicts':verdicts})
(H/'entering/allocation-comparison.json').write_text(json.dumps({'revision':'55f7f82d35da3ec374a1cdc815c0c0aef3a1d3aa','scope':'Entering oracle equations; explicit capture-local mapping of existing public coil_t key, not an old-package native rerun','rows':rows},indent=2)+'\n')
print(f'Retained {len(rows)} entering radial-allocation comparisons')
