"""One selected gas tuple and predeclared cooler offers; development evidence only.

Additional hypothetical offer (25,25,20) MW/K is selected before this diagnostic,
with recuperator UA60 and quote62.9116 MUSD2004; no UA sizing is performed.
Existing offers (25,25,40), (30,30,50), (40,40,60) remain diagnostic alternatives.
Run from repository root with --out naming a new file.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
from types import SimpleNamespace


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--include-revised-offer', action='store_true', help='Append explicitly revised (25,25,25), UArec60, quote62.9116 MUSD2004 offer; never size UA from a root')
    args = p.parse_args()
    if args.out.exists(): p.error('output must be new')
    # Execute the unchanged calculation function AST; replace schema-only helpers.
    # Native package import requires simkit, absent from this diagnostic runtime.
    network_path = Path('exploration/costed_loop_brayton/costed_loop_brayton_tea/handwritten/integrated_heat_electricity/network_heat_driven_closure_impl.py')
    tree = ast.parse(network_path.read_text())
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name=='_reviewed_run_network_heat_driven_closure')
    def require(ok, message):
        if not ok: raise ValueError(message)
    namespace = dict(math=math,BRANCHES=('he','divertor','pbli'),require=require,
        values=lambda x:{k.removesuffix('_in'):v for k,v in x.items()},finish=lambda _,x:x)
    exec(compile(ast.Module(body=[function],type_ignores=[]),str(network_path),'exec'),namespace)
    control = load(Path(__file__).with_name('fourth-submission-control-probe.py'), 'control_probe')
    steam_path = Path('exploration/stellarator_e2e/generated/handwritten/mfe_matched_steam_cycle/matched_steam_cycle_impl.py')
    steam = load(steam_path, 'steam')
    source = json.loads(Path(__file__).with_name('fourth-submission-control-probe.json').read_text())['cases'][3]['primary']
    ratio, flow, cp, rec_ua = 1.5, 2000., 5193., 60.
    c = flow*cp/1e6
    compressor_out = 308.15*(1+(ratio**.4-1)/.89)
    eps = rec_ua/(rec_ua+c)
    inputs = dict(network_mode_in=0, pbli_split_in=.5, cold_temperature_in=compressor_out,
        flow_in=flow, cp_in=cp, gamma_in=5/3, turbine_pressure_in=4.285714285714286*ratio**3*.955,
        return_pressure_in=4.285714285714286, turbine_efficiency_in=.93, recuperator_effectiveness_in=eps)
    for b in ('he','pbli','divertor'):
        inputs.update({b+'_flow_in':source['mdot'], b+'_cp_in':cp,b+'_limit_in':source['T_out'],
            b+'_available_in':source['q_ihx'] if b=='he' else 0., b+'_ua_in':50. if b=='he' else 0.})
    gas = namespace['_reviewed_run_network_heat_driven_closure'](inputs)
    bypass_path = Path('exploration/costed_loop_brayton/bodies/loop_return_control/primary_bypass_control_impl.py')
    bypass = control.load(bypass_path, 'bypass').calculate(SimpleNamespace(ua_in=50., primary_flow_in=source['mdot'],primary_cp_in=cp,
        secondary_flow_in=flow,secondary_cp_in=cp,primary_limit_in=source['T_out'],secondary_inlet_in=gas['heater_inlet'],
        duty_in=source['q_ihx'],required_return_in=source['T_comp_in'],max_bypass_in=.5,tolerance_in=1e-6))
    turbine_out = gas['expansion_factor']*gas['turbine_temperature']
    precooler_in = turbine_out-eps*max(turbine_out-compressor_out,0)
    liquid = sorted([r for r in steam.property_tables()['saturation'] if r['phase']=='liquid'],key=lambda r:r['T'])
    h = lambda t:steam.interpolate(liquid,'T',t,'h')
    t = lambda ent:steam.interpolate(liquid,'h',ent,'T')
    e = 9.80665*20/(.8*.95)/1000
    ha = h(25)+e
    ta = t(ha)

    def cooler(hot, installed):
        cold = 35.
        q = c*(hot-cold)
        def at(out):
            mdot = 1000*q/(h(out)-ha)
            knots = [0.,q]+[(r['h']-ha)*mdot/1000 for r in liquid if ha<r['h']<h(out)]
            knots.sort()
            gaps = [cold+(hot-cold)*z/q-t(ha+1000*z/mdot) for z in knots]
            if min(gaps)<=0:raise ValueError('pinch')
            ua = sum((b-a)*(math.log(gb/ga)/(gb-ga) if gb!=ga else 1/ga)
                     for a,b,ga,gb in zip(knots,knots[1:],gaps,gaps[1:]))
            return dict(ua=ua,flow=mdot,pump_MW=mdot*e/1000,min_gap=min(gaps),out_C=out)
        lo,hi=ta+1e-7,min(hot,60.)-1e-7
        a,b=at(lo),at(hi)
        result=dict(hot_C=hot,cold_C=cold,duty_MW=q,installed_UA=installed,bracket_UA=[a['ua'],b['ua']])
        if not a['ua']<=installed<=b['ua']:
            return result|dict(state='no_root')
        for _ in range(100):
            mid=(lo+hi)/2
            state=at(mid)
            if abs(state['ua']-installed)<1e-10:break
            if state['ua']<installed:lo=mid
            else:hi=mid
        return result|dict(state='completed',solution=state,
            flow_ok=state['flow']<=100000,power_ok=state['pump_MW']<=30,duty_ok=q<=2000)
    catalogs=[]
    offers = [(25,25,20),(25,25,40),(30,30,50),(40,40,60)]
    if args.include_revised_offer: offers.append((25,25,25))
    for offer in offers:
        rows=[cooler(hot-273.15,ua) for hot,ua in zip((compressor_out,compressor_out,precooler_in),offer)]
        catalogs.append(dict(offer=offer,coolers=rows))
    result=dict(purpose=__doc__,selected_source_MW=2500,selected_ratio=ratio,selected_flow=flow,recuperator_UA=rec_ua,
        source=source,network_inputs=inputs,network=gas,primary_bypass=bypass,
        compressor_out_K=compressor_out,precooler_in_K=precooler_in,offers=catalogs,
        property_body_sha256=hashlib.sha256(steam_path.read_bytes()).hexdigest(),
        revised_offer_included=args.include_revised_offer,
        network_body_sha256=hashlib.sha256(network_path.read_bytes()).hexdigest(),
        execution_limit='Existing function AST with schema-only adapters; initial native import refused: simkit absent. Native package/schema execution unverified.')
    with args.out.open('x') as f:f.write(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(accepted=gas['accepted_heat'],available=source['q_ihx'],bypass=bypass,offers=catalogs),indent=2))


if __name__=='__main__':main()
