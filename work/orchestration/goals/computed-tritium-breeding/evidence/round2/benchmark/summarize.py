"""Summarize all predeclared cases and retain numerical/data integrity checks."""
import hashlib,json,math
from pathlib import Path
import openmc
H=Path(__file__).resolve().parent
rows=json.loads((H/'results.json').read_text())
checks={'cases':len(rows),'histories':sum(r['histories'] for r in rows),'max_isotope_sum_error':max(abs(r['isotope_sum_error']) for r in rows),'assemblies':{},'data_sha256':{}}
for assembly in ('Li','PbLi'):
    group=[r for r in rows if r['assembly']==assembly]
    base=next(r for r in group if r['case']=='baseline');repeat=next(r for r in group if r['case']=='repeat')
    checks['assemblies'][assembly]={'min':min(r['total'] for r in group),'max':max(r['total'] for r in group),'max_abs_z':max(abs(r['z_diagnostic']) for r in group),'repeat_difference_combined_standard_deviations':abs(base['total']-repeat['total'])/math.hypot(base['std_dev'],repeat['std_dev']),'ideal_lithium_volume_cm3':4*math.pi/3*(60**3-(10 if assembly=='Li' else 20)**3)}
    with openmc.StatePoint(H/'runs'/f'{assembly}_baseline'/'statepoint.40.h5') as sp:
        checks['assemblies'][assembly]['global_tallies']=[{n:(str(v) if n=='name' else float(v)) for n,v in zip(sp.global_tallies.dtype.names,row)} for row in sp.global_tallies]
for p in sorted((H.parents[6]/'.codex-test/breeding-transport/data').glob('*.h5')):
    if p.stem.startswith(('Li','Pb','Fe','Cr','Ni')):
        checks['data_sha256'][p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
(H/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print('| Assembly | Case | TBR | MC standard error | C/E | Error / combined σ |')
print('|---|---|---:|---:|---:|---:|')
for r in rows:
    print(f"| {r['assembly']} | {r['case']} | {r['total']:.6f} | {r['std_dev']:.6f} | {r['C_over_E']:.4f} | {r['z_diagnostic']:.3f} |")
print(json.dumps(checks['assemblies'],indent=2))
