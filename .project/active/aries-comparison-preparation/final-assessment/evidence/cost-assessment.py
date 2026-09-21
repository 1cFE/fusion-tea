"""Replay retained cost arithmetic only; does not import or execute the plant."""
import csv, hashlib, json, math, tarfile
from pathlib import Path
BASE = Path('.project/active/aries-comparison-preparation')
OUT = BASE / 'final-assessment/evidence'
REPORT = BASE / 'partial-assessment/attempts/diagnostic-1/report.json'
ARCHIVE = BASE / 'post-reveal-preparation/package/post-reveal-v1.tar.gz'
SRC = BASE / 'post-reveal-results/post-reveal-v1/source-evidence/retained/knowledge/holdout/aries-cs/extracted/20260920-r3/08-FST-Lyon'
# Agent judgments from direct inspection of the frozen sources and retained images.
# Each entry: pricing role, account finding, specific obstacle to comparison.
notes = {
'C220103': ('installed_inventory_rollup', 'Composite REBCO tape + external pack materials + winding + conditional sheet stock + electromagnetic supports. Table III 222.884 M$ is modular coils115.960 + VF13.358 + modular structure93.535; divertor is a separate line despite its numbering.', 'REBCO versus Nb3Sn; no separately purchased VF coil set; manufacturing omissions; Table VI coil+structure209.50 excludes VF unlike Table III.'),
'C220101': ('geometry_and_selected_class', 'First wall + blanket + reflector shell volumes at600000 USD/m3 and selected3306.8890988488924 MW class; source59.347 M$ is first wall6.490 + blankets/back wall52.856 (rounding0.001).', 'Source dual He/PbLi ferritic-steel component construction and back-wall boundary do not establish correspondence to homogeneous shell/reflector allowance.'),
'C220102': ('geometry_and_selected_class', 'Hot+cold shield volumes at740000 USD/m3 and selected thermal class. Source228.627 M$ explicitly includes back wall and manifold; Table VI splits shield/back wall131.67 and manifolds96.96.', 'Model shell cost does not demonstrate the source manifold purchase or graded WC/ferritic-steel composition.'),
'C220105': ('geometry_and_selected_class', 'Nonmagnet structure shell volume at150000 USD/m3, selected gross class and residual_fraction1.0. Source Table III primary structure/support73.126 M$; Table VI primary structure61.42 M$.', 'Different primary-structure/support allocation and TableIII/TableVI cost boundaries; no justified disjoint reconstruction from model magnet supports.'),
'C220106': ('geometry_and_selected_class', 'Vessel-shell proxy at720000 USD/m3 with selected gross class. Source137.135 M$ is vacuum system AND cryostat; TableVI vessel alone60.55 M$, cryostat61.70 M$.', 'Shell excludes gas-load pump purchase and does not establish source cryostat/system scope. A similar ratio to broader account cannot validate vessel prediction.'),
'C220104': ('installed_heating_price', 'Installed ECRH equipment price, not computed operating heat demand. Source TableIII plasma heating66.427 M$; source ignition does not make startup-heating purchase zero.', 'Installed capacities/heating technology, installed scope and dated rates are not aligned; selected capacity is not a predicted sustainment requirement.'),
'C220107': ('supplied_purchase', 'Selected power-supply package86.01348274180616 M$; source70.624 M$. Frozen exclusion remains.', 'C220107 is excluded from component-cost credit; retain its contribution and disclosure in ancestors.'),
'C220108': ('supplied_purchase', 'Model divertor109.10912315593052 M$ versus source5.318 M$ (TableVI5.32 rounded).', 'Target construction/area and installed heat-removal scope are not matched; field-unaffected purchase cost does not qualify operating heat load.'),
'C220110': ('selected_class_allowance', '150 M$ toroidal remote-handling base scaled by selected1219.9981701764736 MWe class.', 'No separately resolved remote-handling value in source tables; cannot assign source22.1.10 zero because that line is electron-cyclotron startup, not handling.'),
'C220111': ('fractional_rollup', '14 percent of model reactor_equipment (powercore+remote handling).', 'No source disjoint installation line; source total-capital1.93 multiplier combines multiple indirect/finance categories and cannot supply this fraction. C220107 descendant.'),
'aux_cooling_total': ('supplied_purchase_plus_class_allowance', 'Model auxiliary3.6375780087337815 M$ plus selected cryoplant31.478692121086925 M$; source auxiliary cooling3.735 M$.', 'Source cryoplant allocation is unresolved. Near agreement of the auxiliary-only child must not be substituted for the frozen total row.'),
'waste': ('selected_class_allowance', '1.96 M$ times selected3306.8890988488924/1000 gives6.481502633743829 M$; TableIII radioactive-waste treatment6.655 M$. Broad function corresponds.', 'No verified installation/processing-capacity inventory or dated price bridge; agreement is a selected thermal-class allowance, not prediction of actual waste throughput.'),
'other_rpe': ('selected_class_allowance', '11.5 M$ times (selected850.0653006674999/1000)^0.8; source other plant equipment60.723 M$.', 'Residual-account contents not enumerated on a matched boundary; large nominal difference cannot be assigned to a particular omitted machine.'),
'instrumentation': ('selected_class_allowance', '85 M$ times (selected3306.8890988488924/3500)^0.65; frozen allocation is central/plasma supervisory controls with fuel-package-local controls elsewhere.', 'Source44.558 M$ controls boundary is not disaggregated; unchanged model coefficient is an uncalibrated residual, not a sourced split.'),
'CAS23': ('supplied_purchase', 'Selected247.46442883859593 M$ Rankine turbine/condenser/feedwater package; TableIII314.558 M$ turbine plant.', 'Steam extraction/reheat Rankine versus source helium Brayton; selected purchase is not independently calculated from transferred plant output.'),
'CAS24': ('installed_rating_price', 'Installed1219.9981701764736 MWe rating times86400 USD/MWe gives105.40784190324733 M$; source electric plant138.764 M$. Broad electric-plant function corresponds.', 'Voltage, reactive power, fault duty, equipment list and installation boundary unqualified; installed rating is independent of actual gross generation.'),
'CAS25': ('supplied_purchase', 'Selected115.93953180564217 M$ heat-rejection purchase maps by function to SOURCE27 heat rejection56.086 M$, not source25.', 'Rankine condenser/cooling-water design versus source Brayton heat rejection; matched equipment/installation boundary unavailable.'),
'CAS26': ('selected_class_allowance', 'Selected gross class times miscellaneous per-MW rate gives64.15970376958075 M$; functional mapping is SOURCE25 miscellaneous70.958 M$, not source26.', 'Miscellaneous equipment scope not enumerated; selected class and inherited rate do not predict transferred plant requirements.'),
'CAS27': ('selected_material_inventory', 'Blanket volume times0.50 times9400 kg/m3 times5 USD/kg gives17.55260411562009 M$; functional mapping is SOURCE26 special materials151.327 M$.', 'Model purchases blanket PbLi fill only. Source p709 describes59 M$ core LiPb plus an additional factor1.5 for remainder-of-plant piping; TableIII special materials cannot be treated as blanket-only inventory.'),
'CAS40': ('selected_class_allowance', '41.2 M$ times sqrt(selected850.0653006674999/1000). Owner staffing/preoperation allowance.', 'Source1.93 direct-to-capital multiplier includes owner and other categories without a disjoint owner-cost value.'),
'powercore': ('component_rollup', 'Sum of eight C220101..108 component accounts.', 'No same-boundary source value; source22.1 includes extra VF coils and impurity controls; model children have unresolved scope. Includes excluded C220107.'),
'reactor_equipment': ('component_rollup', 'powercore + remote handling =3459.8159790690637 M$; frozen source candidate22.1 total core equipment864.700 M$.', 'Source22.1 includes impurity control6.561 M$ and no disjoint remote-handling line; differing children and excluded C220107 prevent clean aggregate credit.'),
'BOP': ('component_rollup', 'CAS23+CAS24+CAS25+CAS26; selected purchases/rating/class costs.', 'No frozen same-boundary source observation; source23+24+27+25 can be summed descriptively only after retaining technology and installed-scope limitations.'),
'non_tape_materials': ('installed_inventory_price', 'External copper+solder+steel+helium; excludes tape constituents, supports and sheet stock.', 'No source disaggregation for these materials separate from Nb3Sn conductor procurement.'),
 'tape_procurement': ('installed_inventory_price', 'Supplied winding-pack tape volume divided by full composite tape section times20 USD/physical tape metre; source110.3 M$ modular-coil SC cost.', 'REBCO composite tape versus Nb3Sn conductor-system procurement; conductor manufacturing coverage and price year are unresolved.'),
'winding_operations': ('installed_inventory_price', 'Installed composite-conductor length times480 USD1990/m times334.4/130.7 times1.9. Source winding5.70 M$ in2004.', 'Transferred tokamak/nonplanar service allowance versus source modular-coil fabrication; included insulation/process steps unresolved. Existing escalation does not establish a common2004 bridge.'),
'winding_procurement': ('component_rollup', 'tape_procurement+non_tape_materials+winding_operations.', 'No identical frozen source subtotal; source modular coils116.0 M$ combines110.3+5.70 with unresolved conductor-material coverage. Do not add either parent to its children.'),
'insulation_stock': ('conditional_stock_price', 'Conditional laminate sheet-area stock purchase; cured resin already included.', 'No source stock-only insulation row; overlap with inherited winding operations unresolved; ground wrap/impregnation/labor are not priced by this line.'),
'supports_cost': ('installed_inventory_price', 'Supplied total electromagnetic support mass times18 USD/kg; source TableVI modular structure93.54 M$ (42.52 strongback+0.85 cover+50.17 intershell).', 'Conditional all-in rate/year and support geometry/manufacture differ; source p709 attributes low cost to a particular advanced fabrication technique, not demonstrated here.'),
'cryo_cost': ('supplied_purchase', 'Selected cryoplant31.478692121086925 M$, already included in aux_cooling_total.', 'No disjoint source cryoplant price; reference Nb3Sn near4 K and model REBCO cooling cannot be equated by name.'),
'aux_cooling': ('selected_class_allowance', '1100 USD/MW times selected3306.8890988488924 MW; child of aux_cooling_total.', 'No frozen reference for this child; source3.735 M$ belongs to the total-row candidate with unresolved cryoplant allocation.'),
'copper_cost': ('installed_inventory_price', 'External winding-pack copper mass times inherited2026-class rate; composite tape copper is not charged again.', 'No source external-copper disaggregation; supplier/fabrication/date qualification unavailable.'),
'solder_cost': ('installed_inventory_price', 'External solder mass times September2026 retail-stock proxy.', 'No source external-solder disaggregation or compatible bulk procurement quote.'),
'steel_cost': ('installed_inventory_price', 'External winding-pack steel mass times inherited rate, separate from electromagnetic supports.', 'No source external-steel disaggregation; rate year and fabricated coverage unresolved.'),
'helium_cost': ('installed_inventory_price', 'Ideal-gas winding helium inventory at selected conditions;2024 base escalated to estimated2026.', 'No source inventory-only helium price; different cryogenic conditions and no verified common-year bridge.'),
}
printed = dict(zip(['C220103','C220101','C220102','C220105','C220106','C220104','C220107','C220108','aux_cooling_total','waste','other_rpe','instrumentation','CAS23','CAS24','CAS25','CAS26','CAS27','reactor_equipment','tape_procurement','winding_operations','supports_cost'], [222.884,59.347,228.627,73.126,137.135,66.427,70.624,5.318,3.735,6.655,60.723,44.558,314.558,138.764,56.086,70.958,151.327,864.700,110.3,5.70,93.54]))
hashfile = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
archive_hash = hashfile(ARCHIVE)
assert archive_hash == json.loads((ARCHIVE.parent/'freeze-record.json').read_text())['sha256']
# Preserve exact frozen source excerpts and identity; no model evaluation occurs.
ranges = {
'models/designs/generic_mfe/mfe_subsystems.sysml': [(40,102),(155,246),(290,310),(535,551),(860,917),(1038,1083)],
'models/designs/generic_mfe/mfe_plant.sysml': [(475,550),(600,624)],
'models/designs/stellarator_09/stellarator_plant.sysml': [(35,45),(555,585),(660,716),(1965,1983),(1990,2020)],
'models/library/analyses/mfe_account_costs.sysml': [(1,51),(72,195),(250,277),(506,541)],
'models/library/analyses/mfe_winding_pack_cost.sysml': [(1,95)],
'models/library/structure/mfe_plant_systems.sysml': [(630,652)],
'models/library/cost_structure/mfe_power_core.sysml': [(342,368),(380,430),(467,484)],
'models/library/analyses/mfe_magnet_cost.sysml': [(152,181)],
}
frozen=[]
with tarfile.open(ARCHIVE) as tar:
    for path, rs in ranges.items():
        b=tar.extractfile(path).read(); lines=b.decode().splitlines()
        frozen.append({'archive_member':path,'sha256':hashlib.sha256(b).hexdigest(),'excerpts':[{'first_line':a,'last_line':z,'text':'\n'.join(lines[a-1:z])} for a,z in rs]})
(OUT/'cost-frozen-excerpts.json').write_text(json.dumps({'archive':str(ARCHIVE),'archive_sha256':archive_hash,'files':frozen},indent=2)+'\n')
rows=[]
for r in json.loads(REPORT.read_text())['rows']:
    if not(r['axis']=='cost' and r['role']=='calculated' and r['field_qualification']['field_applicability']=='unaffected_by_field_finding'): continue
    key=r['id']; role, finding, blocker=notes[key]; ref=r['reference']['value']; ratio=r['raw_arithmetic']/ref if ref is not None else None
    page='15' if key in ('tape_procurement','winding_operations','supports_cost') else '13'
    img=SRC/f'outputs-page-{page}.png'
    if ref is not None: assert math.isclose(ref, printed[key]*1e6, rel_tol=1e-14)
    rows.append({'id':key,'model_raw_USD':r['raw_arithmetic'],'reference_raw_printed_MUSD':printed.get(key),'reference_raw_USD':ref,'reference_currency_year':2004 if ref is not None else None,'model_currency_year':'mixed_or_unresolved; see pricing_role and account_finding','unit_factor_MUSD_to_USD':1e6 if ref is not None else None,'nominal_model_reference_ratio':ratio,'descriptive_band_position':None if ratio is None else ('within_[0.5,2]' if 0.5<=ratio<=2 else 'below_0.5' if ratio<0.5 else 'above_2'),'scientific_comparison_eligible':False,'scientific_verdict':'excluded' if key=='C220107' else 'not_established','pricing_role':role,'account_finding':finding,'specific_blocker':blocker,'money_blocker':'No verified common purchasing-power year and no frozen monetary normalization algorithm; no inflation applied.','reference_scope':r['reference']['scope'],'reference_image':str(img) if ref is not None else None,'reference_image_sha256':hashfile(img) if ref is not None else None,'reference_image_reinspected':ref is not None,'reference_printed_page':709 if page=='15' and ref is not None else 707 if ref is not None else None,'frozen_source_evidence':'cost-frozen-excerpts.json','producers':r['producers'],'original_role':r['role'],'original_comparison_status':r['comparison_status'],'independent_prediction_credit':False,'field_applicability':r['field_qualification']['field_applicability'],'aggregation_warning':'Parents and descendants overlap; do not sum the35 rows.','C220107_disclosure':key in ('C220107','powercore','reactor_equipment','C220111')})
assert len(rows)==35 and sum(r['reference_raw_USD'] is not None for r in rows)==21
assert set(notes)=={r['id'] for r in rows}
result={'schema':'final-cost-assessment/v1','authority':'AGENT assessment; owner authorizes retained revealed evidence; original bands unchanged','report':str(REPORT),'report_sha256':hashfile(REPORT),'archive_sha256':archive_hash,'criteria':[0.5,2.0],'comparison_kind':'post_reveal_descriptive; no plant run','rows':rows}
(OUT/'cost-rows.json').write_text(json.dumps(result,indent=2)+'\n')
with (OUT/'cost-rows.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows({k:json.dumps(v) if isinstance(v,(list,dict)) else v for k,v in r.items()} for r in rows)
print(json.dumps({'rows':len(rows),'reference_pairs':21,'no_reference':14,'nominal_band_counts':{s:sum(r['descriptive_band_position']==s for r in rows) for s in ['within_[0.5,2]','below_0.5','above_2']},'eligible':0,'source_images_verified':2},indent=2))
