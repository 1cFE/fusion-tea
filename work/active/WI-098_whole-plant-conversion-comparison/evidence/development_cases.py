"""Reviewed development controls/adverse cases, using coordinator-owned migration."""
from pathlib import Path
import json,os,sys
ROOT=Path.cwd();sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
from scripts.study.verify import package_input_values
from exploration.whole_plant_conversion.studies.migrate_controls import migrate
from exploration.whole_plant_conversion.run import execute
OUT=ROOT/'work/active/WI-098_whole-plant-conversion-comparison/evidence/development-final'
PACKAGE=ROOT/'exploration/whole_plant_conversion/whole_plant_conversion_tea'
P='whole_plant_conversion__plant__'
defaults={k:float(v) for k,v in package_input_values(PACKAGE).items()}
anchors=json.loads((ROOT/'exploration/component_alternatives/studies/20260926-design-study-component-alternatives-b/matched-anchor-selection.json').read_text())['anchors']
base=migrate(anchors[0]['point'],defaults,overrides={P+'finance__availability':.8})
rows=[]
def add(name,changes=None,point=None):rows.append({'case':name,'inputs':(point or base)|{P+k:v for k,v in (changes or {}).items()}})
add('whole-baseline2500')
add('legacy-control2500',{'finance__availability':.85})
add('matched2800',point=migrate(anchors[1]['point'],defaults,overrides={P+'finance__availability':.8}))
add('matched3000-failed-source',point=migrate(anchors[2]['point'],defaults,overrides={P+'finance__availability':.8}))
add('demand-only2800',{'source_basis__q_source_MW':2800.})
for q in [50.,80.]:add('cryo-q'+str(int(q)),{'cryogenic_demand__q_nuc_W_m3':q})
for q in [10000.,13000.]:add('cryo-extra'+str(int(q)),{'cryogenic_demand__extra_cold_W':q})
add('water-property-refusal',{'water_ic1__water_inlet_C':61.})
add('actual-exchanger-crossover',{'steam_return_control__secondary_inlet':800.})
add('cryoplant-small-offer',{'cryogenic_offer__cold_rating_W':20000.,'cryogenic_offer__intercept_rating_W':30000.,'cryogenic_offer__quote_USD2025':31478692.121086925})
add('cryoplant-large-offer',{'cryogenic_offer__cold_rating_W':60000.,'cryogenic_offer__intercept_rating_W':90000.,'cryogenic_offer__quote_USD2025':94436076.36326078})
add('negative-cryo-domain',{'cryogenic_demand__extra_cold_W':-1.})
add('stock-insufficient',{'fuel_accounts__stock_kg':1.})
add('stock-sufficient',{'fuel_accounts__stock_kg':6.})
add('processing-insufficient',{'fuel_accounts__processing_capacity_kg_s':.00001,'fuel_processing_account__quote_USD2025':1e7})
add('processing-sufficient',{'fuel_accounts__processing_capacity_kg_s':.0002,'fuel_processing_account__quote_USD2025':3e7})
add('primary-pressure-insufficient',{'primary_offer__pressure_rating_Pa':100000.,'primary_circulators_account__quote_USD2025':3e8})
add('primary-pressure-sufficient',{'primary_offer__pressure_rating_Pa':400000.,'primary_circulators_account__quote_USD2025':6e8})
add('auxiliary-insufficient',{'steam_operating__auxiliary_rating_MW':100.,'auxiliary_rejection_account__quote_USD2025':3e7})
add('auxiliary-sufficient',{'steam_operating__auxiliary_rating_MW':250.,'auxiliary_rejection_account__quote_USD2025':7e7})
add('negative-whole-net',{'steam_operating__residual_MW':1000.})
add('annual-import-dominated',{'finance__availability':.001})
add('outage-budget-failure',{'finance__availability':.95})
add('capture-identity-refusal',{'supplied_core__capture_id':48002.})
add('source-path-count-mismatch',{'primary_loop__n_loops':15.})
add('fractional-horizon-refusal',{'finance__years':30.5})
add('zero-discount',{'finance__rate':0.})
add('lower-breeding',{'fuel_accounts__tbr':1.1861455810023918})
add('lower-extraction',{'fuel_accounts__extraction':.9})
add('lower-recovery',{'fuel_accounts__recycle':.98})
add('zero-T-price',{'fuel_accounts__tritium_price':0.})
add('gas-price-only',{'gas_ledger__controller_capital':2e7})
add('common-price-only',{'source_installation_allowance_account__quote_USD2025':1e9})
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'complete-defaults.json').write_text(json.dumps(defaults,indent=2)+'\n')
(OUT/'proposals.json').write_text(json.dumps({'cases':rows},indent=2)+'\n')
execute(rows,OUT/'native')
