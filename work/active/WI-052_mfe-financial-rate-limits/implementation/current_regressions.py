"""Current-package callers retain historical WI-050/051 fixtures unchanged."""
import importlib.util
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
_spec=importlib.util.spec_from_file_location('wi052_generation_for_regressions',Path(__file__).with_name('regenerate.py'))
_generation=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_generation)
ROOT,HERE,PRODUCTION=_generation.ROOT,_generation.HERE,_generation.PRODUCTION
seed_and_generate,hashes=_generation.seed_and_generate,_generation.hashes
materialize_canonical_subset,MFE=_generation.materialize_canonical_subset,_generation.MFE


def operating_acceptance(destination,historical):
    """Reuse the historical scenario definitions; complete today's native package."""
    destination=Path(destination);destination.mkdir(exist_ok=True)
    scratch=Path(tempfile.mkdtemp(prefix='wi052-operating-regression-'))
    models=materialize_canonical_subset(MFE,scratch/'models')
    package=seed_and_generate(scratch/'generated',models_path=models)
    ev,bridge=historical.evaluator(package,'stellarator_tea',scratch/'link')
    rows={name:historical.execute(ev,bridge,{historical.P+k:v for k,v in changes.items()}) for name,changes in historical.CASES.items()}
    inputs={}
    for p in (package/'inputs').glob('*.json'):inputs.update(json.loads(p.read_text()))
    for name,value in [('results.json',rows),('inputs.json',inputs)]:historical.dump(destination/name,value)
    (destination/'scratch.txt').write_text(str(scratch)+'\n')
    return scratch,rows,inputs


def radius_acceptance(destination,historical):
    """Run kept radius scenarios with financial tolerance only on WI-052 channels.

    Temporary driver copies use the frozen fixtures by absolute path. Baseline
    physical values and structured reports remain exact; changed financial
    scalars have the same 1e-9 tolerance independently verified by WI-052.
    """
    destination=Path(destination);destination.mkdir()
    drivers=destination/'drivers';drivers.mkdir()
    finance=json.loads((HERE/'scalar-ledger.json').read_text())['live_ordinary']
    names={r['name'] for r in finance if r['classification']=='changed finance'}
    before=hashes(PRODUCTION)
    for name in ('native','direct','standalone','cli_checks'):
        text=(historical/(name+'.py')).read_text()
        text=text.replace('Path(__file__).resolve().parent',f'Path({str(historical)!r})')
        if name=='native':
            text=text.replace("a['outputs'][k]==v if name=='baseline'",f"a['outputs'][k]==v if name=='baseline' and k not in {names!r}")
        if name=='direct':
            text=text.replace("if name=='baseline' or not isinstance(v,(int,float)):",f"if (name=='baseline' and k not in {names!r}) or not isinstance(v,(int,float)):")
            text=text.replace("scalar[k]==v if name=='baseline'",f"scalar[k]==v if name=='baseline' and k not in {names!r}")
        driver=drivers/(name+'.py');driver.write_text(text)
        command=[str(ROOT/'.codex-test/run'),'bash','-c','export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; exec .codex-test/run python "$@"','wi052',str(driver),str(destination)]
        result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
        (destination/(name+'.log')).write_text(result.stdout+result.stderr)
        assert result.returncode==0,f'{name} failed: {destination/(name+".log")}'
    assert hashes(PRODUCTION)==before
    return destination
