"""Require the reviewed four-point-only replacement and retained reporting brackets."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
OLD=HERE.parent.parent/'20260927-design-study-whole-plant-conversion/preparation'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
digest=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
comparison=read(HERE/'original-point-comparison.json');assert comparison['old_unique_points']==comparison['new_unique_points']==2496
assert comparison['unchanged_unique_points']==2492 and comparison['changed_point_count']==4 and comparison['changed_alias_count']==8
assert not comparison['removed_aliases'] and not comparison['added_aliases'] and not comparison['changed_anchor_groups']
assert comparison['old_alias_count']==comparison['new_alias_count']==2651
assert comparison['changed_by_family']=={'cryogenic_boundary':8}
assert all(set(r['input_differences'])=={'whole_plant_conversion__plant__cryogenic_demand__q_nuc_W_m3'} for r in comparison['changed_aliases'])
old_members={r['case']:r for r in read(OLD/'case-membership.json')['cases']};new_members={r['case']:r for r in read(HERE/'case-membership.json')['cases']}
for name,row in new_members.items():
 if row['family']!='cryogenic_boundary':assert row==old_members[name]
old_band=read(OLD/'reporting-band-plan.json');new_band=read(HERE/'reporting-band-plan.json')
for before,after in zip(old_band['brackets'],new_band['brackets']):
 assert [x['t'] for x in before['bracket']]==[x['t'] for x in after['bracket']]
 assert after['bracket'][0]['gap_USD2025_MWh']>after['target_gap_USD2025_MWh']>after['bracket'][1]['gap_USD2025_MWh']
validated=ROOT/'work/orchestration/goals/design-study-whole-plant-conversion/evidence/numerical-repair-r2-validation/cryo-native/results/cases.json'
native=read(validated)['cases'];assert {digest(r['inputs']) for r in native}==set(comparison['added_point_ids'])
assert all(r['state']=='completed' for r in native)
selection=read(HERE/'reporting-location-selection.json')
assert sha(OLD.parent/'snapshot.json')==selection['original_snapshot_sha256']
for name,expected in selection['recomputed_diagnostics'].items():assert sha(HERE/'recomputed-reporting-locations'/name)==expected
review=ROOT/'work/orchestration/goals/design-study-whole-plant-conversion/evidence/final-results-review-r2/reporting-location-disposition.md'
result=dict(status='pass',unchanged_complete_points=2492,changed_complete_points=4,changed_input='cryogenic_demand.q_nuc_W_m3 only',total_complete_points=2496,total_aliases=2651,all_noncryogenic_memberships_exactly_retained=True,all_anchors_exactly_retained=True,original_reporting_t_values_retained=True,corrected_oracle_reporting_bracket_signs_pass=True,changed_points_match_four_stock_verified_native_receipts=True,recomputed_diagnostics_preserved=True,original_snapshot_unchanged=True,disposition_review=dict(path=str(review.relative_to(ROOT)),sha256=sha(review)),proposal_sha256=sha(HERE/'proposed-points.json'))
(HERE/'selection-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
