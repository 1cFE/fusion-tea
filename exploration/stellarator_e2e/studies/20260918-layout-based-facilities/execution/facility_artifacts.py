"""Export diagnostics reconstructed from actual native case channels, then plot geometry."""
from pathlib import Path
import gzip,importlib.util,json,math,sys,shutil,os
import yaml
H=Path(__file__).resolve().parents[1];ROOT=H.parents[3];P='stellarator_09__stellaris__';R=H/'results'
sys.path.insert(0,str(ROOT/'exploration/stellarator_e2e/pkg'));sys.path.insert(0,str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')

def main():
    sys.path.insert(0,str(H));import study
    study.release()
    package=ROOT/'exploration/stellarator_e2e/generated'
    prep=H/'preparation'
    shutil.copy2(package/'pipelines/pipeline.yaml',prep/'pipeline.yaml')
    body=package/'handwritten/mfe_facilities/facility_layout_impl.py'
    shutil.copy2(body,prep/'facility_layout_impl.py')
    spec=importlib.util.spec_from_file_location('facility_diagnostics',body);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    bindings=yaml.safe_load((prep/'pipeline.yaml').read_text())['modules'][P+'buildings__layout']['inputs']
    defaults=read(prep/'resolved-defaults.json');proposals=read(prep/'proposals.json')
    def key(x):return json.dumps({k:('bool',v) if isinstance(v,bool) else ('number',float(v)) for k,v in x.items()},sort_keys=True)
    lookup={key(x['point']):x for x in proposals}
    directory=R/'facility-ledgers';directory.mkdir(exist_ok=True)
    index=[];baseline=None
    for case in read(R/'native-cases.json'):
        inputs=defaults|case['inputs'];outputs=case['outputs'];x={}
        for formal,binding in bindings.items():
            reference=binding.split(' ',1)[1]
            if reference.split('.',1)[0].endswith('_params'):
                value=inputs[reference.split('.',1)[1]]
            else:value=outputs[reference.removesuffix('.root')]
            x[formal.removesuffix('_in')]=bool(value) if formal=='facilities_enabled_in' else value
        d=module.diagnostics(x)
        for name,value in d['outputs'].items():
            assert math.isclose(value,outputs[P+'buildings__layout__'+name],rel_tol=1e-12,abs_tol=1e-9),(case['candidate_id'],name)
        meta=lookup[key(case['inputs'])]
        payload={'case_id':case['candidate_id'],'proposal_id':meta['id'],'inputs_from_native_bindings':x,'diagnostics':d,'scope':'Deterministic production diagnostic replay; scalar outputs matched to this native case. This is not independent physical verification.'}
        path=directory/(meta['id']+'.json.gz')
        with path.open('wb') as f:
            with gzip.GzipFile(fileobj=f,mode='wb',mtime=0) as z:z.write(json.dumps(payload,allow_nan=False).encode())
        index.append({'case_id':case['candidate_id'],'proposal_id':meta['id'],'file':str(path.relative_to(R)),'route_checks':d.get('geometry',{}).get('route_checks',{})})
        if meta['id']=='default14-layout':baseline=payload
    write(R/'facility-ledger-index.json',index)
    if baseline is None:baseline=next_payload(directory,index)
    plot(baseline)
    print('Exported',len(index),'case-linked diagnostic ledgers and baseline site plot')

def next_payload(directory,index):
    with gzip.open(R/index[0]['file'],'rt') as f:return json.load(f)

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
    for suffix in ('svg','png'):fig.savefig(R/f'baseline-layout.{suffix}',dpi=160)
    plt.close(fig)

if __name__=='__main__':main()
