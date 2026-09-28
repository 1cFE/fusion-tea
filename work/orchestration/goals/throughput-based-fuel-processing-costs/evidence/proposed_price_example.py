"""Reviewable conditional cost example only; leaves the plant unchanged."""
import json
from pathlib import Path
from bs4 import BeautifulSoup

here=Path(__file__).resolve().parent
root=Path.cwd()
source=root/'knowledge/sources/federal_reserve_bank_of_minneapolis_annual_consumer_price/raw.html'
soup=BeautifulSoup(source.read_text(),'html.parser')
cpi={}
for row in soup.select('tr'):
    cells=[c.get_text(' ',strip=True) for c in row.select('th,td')]
    if len(cells)>1 and cells[0].isdigit():
        cpi[int(cells[0])]=float(cells[1].replace(',',''))
assert {year:cpi[year] for year in (1977,1978,1980,1982,2025)} == {1977:60.6,1978:65.2,1980:82.4,1982:96.5,2025:321.9}
flow=json.loads((here/'entering-evidence.json').read_text())['values']['fuel_cycle__inventory__dt_processor_kg_day']
ratio=flow/(2.08e-5*86400)
rows=[('transfer pumps',111000.,112000.,1977),('fuel cleanup',1000000.,70000.,1980),('cryogenic distiller',1237000.,63000.,1978),('secondary containment',182000.,30000.,1980)]
result={'status':'Proposal only; source/account review and owner adoption pending. Not an integrated model or complete plant cost.',
        'capacity_margin':1.0,'capacity_margin_basis':'No extra reserve priced; no standby train or reliability claim.',
        'flow_kg_D_plus_T_per_running_day':flow,'flow_ratio':ratio,'source_exponent':.3,
        'price_basis':'2025 CPI purchasing power, not contemporary equipment-price escalation.',
        'year_assumptions':'Installation uses capital expenditure year as proxy; containment 1978–1982 uses 1980 central scenario.',
        'rows':[]}
for name,capital,installation,year in rows:
    conversion=cpi[2025]/cpi[year]
    result['rows'].append({'function':name,'raw_capital_usd':capital,'raw_installation_usd':installation,
        'year_scenario':year,'cpi_ratio':conversion,'source_reference_capital_2025':capital*conversion,
        'source_reference_installation_2025':installation*conversion,
        'at_current_flow_capital_2025':capital*conversion*ratio**.3,
        'at_current_flow_installation_2025':installation*conversion*ratio**.3})
result['included_capital_2025']=sum(r['at_current_flow_capital_2025'] for r in result['rows'])
result['included_direct_installation_2025']=sum(r['at_current_flow_installation_2025'] for r in result['rows'])
result['included_total_2025']=result['included_capital_2025']+result['included_direct_installation_2025']
central_containment=result['rows'][-1]['at_current_flow_capital_2025']+result['rows'][-1]['at_current_flow_installation_2025']
result['containment_year_only_total_range']={str(y):result['included_total_2025']-central_containment+212000*cpi[2025]/cpi[y]*ratio**.3 for y in (1978,1982)}
result['exclusions']='Storage, additional plant-wide analysis/monitoring/control, effluent and emergency systems, blanket extraction/conditioning, buildings, fuel purchases/startup stock and other unpriced scope in proposed-cost-scope.md; included packages contain some local controls. Containment is limited purchased scope, with some source boxes supplied free; not all plant-area containment or ORNL multiplied support coverage. No LCOE impact asserted.'
(here/'proposed-price-example.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
