"""Render the checked implementation baseline, separately from unexecuted study cases."""
from pathlib import Path
import importlib.util,json,math,sys,yaml,os
ROOT=Path.cwd();E=ROOT/'work/orchestration/goals/layout-based-facilities/evidence';S=ROOT/'exploration/stellarator_e2e/studies/20260918-layout-based-facilities';PKG=ROOT/'exploration/stellarator_e2e/generated';P='stellarator_09__stellaris__'
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'exploration/stellarator_e2e/pkg'));sys.path.insert(0,str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
from scripts.study.verify import package_input_values
values=package_input_values(PKG);outputs=json.loads((ROOT/'work/active/WI-068_layout-based-facilities/evidence/baseline.json').read_text())['outputs']
bindings=yaml.safe_load((PKG/'pipelines/pipeline.yaml').read_text())['modules'][P+'buildings__layout']['inputs'];x={}
for formal,binding in bindings.items():
 reference=binding.split(' ',1)[1];v=values[reference.split('.',1)[1]] if reference.split('.',1)[0].endswith('_params') else outputs[reference.removesuffix('.root')];x[formal.removesuffix('_in')]=bool(v) if formal=='facilities_enabled_in' else v
spec=importlib.util.spec_from_file_location('facilities',PKG/'handwritten/mfe_facilities/facility_layout_impl.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);d=m.diagnostics(x)
assert all(math.isclose(v,outputs[P+'buildings__layout__'+k],rel_tol=1e-12,abs_tol=1e-9) for k,v in d['outputs'].items())
payload={'case_id':'WI068-native-implementation-baseline','inputs_from_native_bindings':x,'diagnostics':d,'scope':'Checked implementation baseline; not an executed study case.'}
(E/'baseline-layout-ledger.json').write_text(json.dumps(payload,indent=2)+'\n')

def plot(payload):
    os.environ.setdefault('MPLCONFIGDIR','/tmp/wi068-matplotlib')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle,Patch
    g=payload['diagnostics']['geometry'];fig,ax=plt.subplots(figsize=(16,8));colors={'reactor':'#355c7d','sector':'#b65f56','cooling':'#489b9a','other':'#bec9d0'}
    labels=[]
    for i,(name,rect) in enumerate(g['rectangles'].items(),1):
        x0,y0,x1,y1=rect;kind='reactor' if name=='reactor_hall' else 'sector' if name.startswith('sector') else 'cooling' if name.startswith('cooling') else 'other'
        ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,facecolor=colors[kind],edgecolor='white',lw=1))
        ax.text((x0+x1)/2,(y0+y1)/2,str(i),ha='center',va='center',fontsize=8,color='white' if kind!='other' else '#23313b')
        labels.append(f'{i:2}  {name.replace("_"," ")}')
    x0,y0,x1,y1=g['parcel_bounds'];ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,fill=False,edgecolor='#44525c',ls='--'))
    ax.set(xlim=(x0-10,x1+10),ylim=(y0-10,y1+10),xlabel='Metres',ylabel='Metres',aspect='equal')
    ax.set_title('Conceptual facility layout — calculated building footprints',loc='left',fontsize=15,pad=15)
    ax.text(1.03,1,'\n'.join(labels),transform=ax.transAxes,va='top',fontsize=8,family='monospace')
    fig.text(.07,.025,'Fixed clearances and provisional equipment envelopes are assumptions. Loads, shielding, contamination control and detailed transport are not qualified.',fontsize=9)
    fig.subplots_adjust(right=.76,bottom=.13)
    for suffix in ('svg','png'):fig.savefig(E/f'baseline-layout.{suffix}',dpi=160)
    plt.close(fig)

plot(payload)
print('Baseline plot and full diagnostic ledger match native implementation baseline')
