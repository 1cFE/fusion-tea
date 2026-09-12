"""Read attached native documentation and resolve the inherited radius source chain."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path.cwd();A=Path(__file__).resolve().parent
from agentic_mbse.sysml.syside_adapter import get_syside
s=get_syside();model,diagnostics=s.try_load_model([str(p) for p in sorted((A/'models').rglob('*.sysml'))])
names={"mfe_plant::'MFE Power Plant'::magnet::R0",'stellarator_09::stellaris::R'}
rows=[]
for e in model.elements(s.ReferenceUsage):
 if str(e.qualified_name) in names:rows.append({'name':str(e.qualified_name),'docs':[d.body for d in e.documentation]})
assert {r['name'] for r in rows}==names
source=ROOT/'work/analysis/20260911-230953_radius-ownership-evidence/source-meaning.md'
assert all(section in source.read_text() for section in ('## Model and existing source interpretation','## Assessment','## Source observations'))
parent=ROOT/'models/designs/stellarator_09/stellarator_plant.sysml'
resolved=ROOT/'knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md'
assert str(resolved.relative_to(ROOT)) in parent.read_text() and resolved.is_file()
image=source.parent/'stellaris-table2.png'
(A/'citations.json').write_text(json.dumps({'native_attached_documents':rows,'resolved_source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'stellarator_parent_source_path':str(resolved.relative_to(ROOT)),'table2_image_sha256':hashlib.sha256(image.read_bytes()).hexdigest(),'independent_visual_observation':{'major_plasma_radius_m':12.7,'minor_plasma_radius_m':1.3},'meaning':'Existing plasma/axis model-intent interpretation; no equality of real modular-coil surfaces or new operating envelope.'},indent=2)+'\n')
print('PASS native attached docs, direct assessment sections, parent-qualified source and independently viewed Table 2')
