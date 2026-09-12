"""Record attached provenance and earned native SV statuses; SV-089 stays pending."""
import json
import subprocess
from common import H, ROOT, FROZEN, dump, sha, run_logged
from agentic_mbse.sysml.syside_adapter import get_syside

syside=get_syside()
model,diagnostics=syside.try_load_model([str(p) for p in sorted((H/'models').rglob('*.sysml'))])
assert not [d for category in ('parser','sema') for d in getattr(diagnostics,category) if d.severity==syside.DiagnosticSeverity.Error]
records=[]
for e in model.elements(syside.ReferenceUsage):
    if str(e.qualified_name) in ("mfe_plant::'MFE Power Plant'::magnet::R0",'stellarator_09::stellaris::R'):
        records.append({'element':str(e.qualified_name),'kind':'ReferenceUsage','documentation':[d.body for d in e.documentation]})
assert len(records)==2 and all(r['documentation'] for r in records)
source='work/analysis/20260911-230953_radius-ownership-evidence/source-meaning.md'
raw=subprocess.check_output(['git','show','2f8856b7:'+source],cwd=ROOT)
assert raw==(ROOT/source).read_bytes()==(FROZEN/'frozen-source-meaning.md').read_bytes()
for section in ('## Model and existing source interpretation','## Assessment','## Source observations'):
    assert section in raw.decode()
image=ROOT/'work/analysis/20260911-230953_radius-ownership-evidence/stellaris-table2.png'
# Hash the retained image as inherited evidence; do not claim an independent image review.
assert sha(image)=='433306f0a4522a08a1889d8c76a3de64b51b73d148e61c33a0261c89b66eae73'
dump('citation-attachments.json',{'elements':records,'source':source,'revision':'2f8856b7','sha256':sha(ROOT/source),'retained_table2_sha256':sha(image),'source_assessment':'Inherited T-021, not independently re-reviewed','MR_links':['MR-051-01','MR-051-03','MR-051-08']})
for i in range(83,89):
    assert run_logged(f'SV-{i:03d}',['agentic-mbse','pm','update-validation',f'SV-{i:03d}','--status','passing'])==0
assert '| pending |' in next(line for line in (ROOT/'modeling_project/VALIDATION_MATRIX.md').read_text().splitlines() if line.startswith('| SV-089 |'))
print('Attached source chain verified and earned SV-083–088 recorded; SV-089 pending independent audit')
