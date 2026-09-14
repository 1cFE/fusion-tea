"""Read completed CLI evidence; check predeclared identities and export recoverable facts."""
import collections
import itertools
import json
import math
from pathlib import Path

from study_tools import HERE, ROOT, PACKAGE, P, EXE, GRID, cases, catalog, defaults, dump


def main():
    rows,compatibility = cases('results/grid/store.sqlite')
    assert len(rows)==108 and all(r['state']=='completed' for r in rows)
    cats = catalog()
    scans=json.loads((HERE/'results/oracle-scan.json').read_text())
    key=lambda p: tuple(p[k] for k,_ in GRID)
    scan={key(r['point']):r for r in scans}
    assert len(scan)==len(rows)
    base=json.loads((HERE/'results/baseline_result.json').read_text())['channels']
    all_channels=set(base)
    fixed=json.loads((HERE/'study-config.json').read_text())['fixed']
    checks={}
    oracle_worst=dict(relative_deviation=0.,case=None,channel=None)

    def check(name,actual,expected,row):
        assert math.isfinite(actual) and math.isfinite(expected),(name,key(row['inputs']))
        deviation=abs(actual-expected)/max(abs(actual),abs(expected),1e-300)
        error=abs(actual-expected)
        outcome=checks.setdefault(name,dict(count=0,worst_relative=0.,worst_absolute=0.,worst_case=None))
        outcome['count']+=1
        outcome['worst_absolute']=max(outcome['worst_absolute'],error)
        if deviation>outcome['worst_relative']:
            outcome.update(worst_relative=deviation,worst_case=row['candidate_id'])
        assert math.isclose(actual,expected,rel_tol=1e-9,abs_tol=1e-9),(name,row['candidate_id'],actual,expected)

    inventory_outputs=[P+'magnet__material_inventory__'+name for name in (
        'mass_copper','mass_solder','mass_steel','mass_helium','cost_copper','cost_solder',
        'cost_steel','cost_helium','material_cost','tape_volume')]
    for row in rows:
        point,out=row['inputs'],row['outputs']
        assert row['executable_fingerprint']==EXE
        assert set(out)==all_channels and len(out)==177
        assert set(row['verdicts'])==set(cats) and len(row['verdicts'])==18
        assert all(point[k]==v for k,v in fixed.items())
        ref=scan[key(point)]
        assert point==ref['point']
        assert len(ref['outputs'])==161
        for channel,value in ref['outputs'].items():
            deviation=abs(out[channel]-value)/max(abs(out[channel]),abs(value),1e-300)
            assert deviation<1e-9,(row['candidate_id'],channel,out[channel],value)
            if deviation>oracle_worst['relative_deviation']:
                oracle_worst=dict(relative_deviation=deviation,case=row['candidate_id'],channel=channel)
        for cid,status in row['verdicts'].items():
            assert status==ref['verdicts'][cid]['status'],(row['candidate_id'],cid)
        current=point[P+'magnet__coil__I_coil']/15.4e6
        radius=point[P+'plasma__R']/12.7
        q=(point[P+'magnet__winding_pack__B_max']/24.9)**.6
        volume_factor=current*radius*q
        check('grade_quantity',out[P+'magnet__conductor_grade__quantity_factor'],q,row)
        check('side_ratio',out[P+'magnet__wp_sizing__wp_side']/base[P+'magnet__wp_sizing__wp_side'],math.sqrt(current*q),row)
        check('volume_ratio',out[P+'magnet__wp_volume__vol_winding_pack']/base[P+'magnet__wp_volume__vol_winding_pack'],volume_factor,row)
        for channel in inventory_outputs:
            check('inventory_ratio:'+channel,out[channel]/base[channel],volume_factor,row)
        for name,ratio in [('tape_cost',volume_factor),('conductor_length',current*radius),('winding_fabrication_cost',current*radius)]:
            channel=P+'magnet__winding_procurement__'+name
            check(name+'_ratio',out[channel]/base[channel],ratio,row)
        stress_ratio=current*(out[P+'magnet__peak_field_calc__B_peak']/base[P+'magnet__peak_field_calc__B_peak'])/math.sqrt(current*q)
        for suffix in ('wp_stress__sigma_wp','cond_strain__eps_cond'):
            channel=P+'magnet__'+suffix
            check(suffix+'_ratio',out[channel]/base[channel],stress_ratio,row)
        energy_ratio=current**2*(out[P+'rb__r_coil_centre']/base[P+'rb__r_coil_centre'])**2/radius
        check('stored_energy_ratio',out[P+'magnet__stored_energy__W_mag']/base[P+'magnet__stored_energy__W_mag'],energy_ratio,row)
        check('casing_mass_ratio',out[P+'magnet__casing_mass__m_casing']/base[P+'magnet__casing_mass__m_casing'],energy_ratio**.78,row)
        material=sum(out[P+'magnet__material_inventory__cost_'+m] for m in ('copper','solder','steel','helium'))
        check('material_sum',out[P+'magnet__material_inventory__material_cost'],material,row)
        pack=out[P+'magnet__winding_procurement__tape_cost']+material+out[P+'magnet__winding_procurement__winding_fabrication_cost']
        check('pack_sum',out[P+'magnet__winding_procurement__cost'],pack,row)
        check('magnet_sum',out[P+'magnet__magnet_capital_rollup__capital_cost'],pack+out[P+'magnet__magnet_structure_cost__cost'],row)
        check('extra_volume_excluded',out[P+'magnet__wp_volume__vol_cold_total']-out[P+'magnet__wp_volume__vol_winding_pack'],defaults()[P+'magnet__vol_cold_cryo'],row)

    axes={}
    observed=[P+'lcoe_calc__lcoe',P+'magnet__winding_procurement__cost',P+'magnet__magnet_capital_rollup__capital_cost',
              P+'magnet__wp_sizing__wp_side',P+'magnet__wp_volume__vol_winding_pack',P+'magnet__peak_field_calc__B_peak',
              P+'magnet__wp_stress__sigma_wp',P+'magnet__winding_procurement__winding_fabrication_cost']
    for axis,values in GRID:
        grouped=collections.defaultdict(list)
        for row in rows:
            grouped[tuple(row['inputs'][k] for k,_ in GRID if k!=axis)].append(row)
        changes={channel:[] for channel in observed}
        invariant=[]
        if axis.endswith('__B_max'):
            invariant=[P+'magnet__'+suffix for suffix in ('field_calc__B_axis','peak_field_calc__B_peak','stored_energy__W_mag',
                'casing_mass__m_casing','winding_procurement__conductor_length','winding_procurement__winding_fabrication_cost',
                'winding_pack_cost__cost','magnet_cost__capital_cost')]
        if axis.endswith('__a'):
            invariant=[P+'magnet__'+suffix for suffix in ('conductor_grade__quantity_factor','wp_sizing__wp_side',
                'wp_volume__vol_winding_pack','winding_procurement__tape_cost')]
        for group in grouped.values():
            group.sort(key=lambda row:row['inputs'][axis])
            assert [r['inputs'][axis] for r in group]==values
            low,high=group[0],group[-1]
            for channel in observed:
                changes[channel].append((high['outputs'][channel]/low['outputs'][channel]-1)*100)
            for row in group[1:]:
                for channel in invariant:
                    assert row['outputs'][channel]==low['outputs'][channel],(axis,channel,row['candidate_id'])
        axes[axis]=dict(matched_groups=len(grouped),endpoint_percent_changes={k:dict(min=min(v),max=max(v)) for k,v in changes.items()},
            invariants_checked=invariant,violation_counts_by_value={str(value):{
                cid:sum(r['inputs'][axis]==value and r['verdicts'][cid]=='violated' for r in rows) for cid in cats} for value in values})
    outcomes={cid:dict(source_local_identity=entry['source_local_identity'],definition_qualified_name=entry['definition_qualified_name'],
        counts=dict(collections.Counter(r['verdicts'][cid] for r in rows)),violated_cases=[r['candidate_id'] for r in rows if r['verdicts'][cid]=='violated']) for cid,entry in cats.items()}
    extremes={channel:dict(min=min(r['outputs'][channel] for r in rows),max=max(r['outputs'][channel] for r in rows),
        min_case=min(rows,key=lambda r:r['outputs'][channel])['candidate_id'],max_case=max(rows,key=lambda r:r['outputs'][channel])['candidate_id']) for channel in observed}
    dump('results/cases.json',rows)
    dump('results/store-compatibility.json',compatibility)
    dump('results/identity-checks.json',dict(outcome='PASS',checks=checks,matched_axis_checks=axes))
    dump('results/exhaustive-oracle.json',dict(outcome='PASS',cases=108,channels_per_case=161,numeric_comparisons=108*161,
        verdict_comparisons=108*18,worst=oracle_worst,tolerance=dict(relative=1e-9,absolute=None),
        unmapped_numeric_channels=sorted(all_channels-set(scans[0]['outputs']))))
    dump('results/summary.json',dict(cases=108,states=dict(collections.Counter(r['state'] for r in rows)),
        headlines=dict(collections.Counter(r['headline'] for r in rows)),constraints=outcomes,axes=axes,extremes=extremes,
        fully_satisfied_cases=[r['candidate_id'] for r in rows if all(x=='satisfied' for x in r['verdicts'].values())]))
    print('PASS 108 cases, 17388 oracle scalar comparisons, 1944 verdicts and all declared identities')


if __name__=='__main__':
    main()
