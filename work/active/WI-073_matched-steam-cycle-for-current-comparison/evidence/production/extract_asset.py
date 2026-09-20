"""One-time original NIST transcription; never imported by production runtime."""
from pathlib import Path
import hashlib,json
from urllib.parse import urlsplit,parse_qs
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[5]
SOURCES={'main':'nist_webbook_water6_2mpa171to455c_halfk_state_table','extraction':'nist_water0_8mpa42to455c_matched_cycle_table','saturation':'nist_water_temperature_grid_saturation_20to60c_corrected'}
KEYS=['T','P','rho','v','u','h','s','cv','cp','sound_speed','joule_thomson','viscosity','conductivity','surface_tension']
def extract():
 asset={'schema_version':1,'authority':'Original NIST Chemistry WebBook water tables; WI-073 bounded fixed-pressure interpolation, not general water EOS','units':dict(zip(KEYS,['degC','MPa','kg/m^3','m^3/kg','kJ/kg','kJ/kg','kJ/(kg K)','kJ/(kg K)','kJ/(kg K)','m/s','K/MPa','microPa s','W/(m K)','N/m'])),'entropy_conversion':'Original J/(g K) is numerically identical to kJ/(kg K).','tables':{}}
 for name,directory in SOURCES.items():
  path=ROOT/'knowledge/sources'/directory/'raw.html';raw=path.read_bytes();soup=BeautifulSoup(raw,'html.parser'); link=next(a['href'] for a in soup.find_all('a',href=True) if 'Action=Data' in a['href'] and 'Wide=on' in a['href']); query=parse_qs(urlsplit(link).query)
  records=[];headers=[]
  for table in soup.find_all('table'):
   heading=[x.get_text(' ',strip=True) for x in table.find_all('th')]
   if not heading or not heading[0].startswith('Temperature'):continue
   if heading not in headers:headers.append(heading)
   for tr in table.find_all('tr'):
    cells=[x.get_text(' ',strip=True) for x in tr.find_all('td')]
    if len(cells)<14 or cells[-1] not in ('liquid','vapor'):continue
    row=dict(zip(KEYS,map(float,cells[:-1])));row['phase']=cells[-1];row['source_cells']=cells;records.append(row)
  phases={phase:[r for r in records if r['phase']==phase] for phase in ('liquid','vapor')}
  asset['tables'][name]={'source_path':path.relative_to(ROOT).as_posix(),'source_sha256':hashlib.sha256(raw).hexdigest(),'query_url':'https://webbook.nist.gov'+link,'query':query,'reference_state':query['RefState'][0],'original_headers':headers,'row_count':len(records),'phase_counts':{k:len(v) for k,v in phases.items()},'saturation_endpoints':{'liquid':phases['liquid'][-1],'vapor':phases['vapor'][0]} if name!='saturation' else 'Separate liquid and vapor rows at each temperature; do not merge phases.','rows':records}
 path=ROOT/'models/library/data/matched_steam_properties.json';path.write_text(json.dumps(asset,sort_keys=True,indent=2,allow_nan=False)+'\n')
 print(json.dumps({'asset':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'tables':{k:(v['row_count'],v['phase_counts']) for k,v in asset['tables'].items()}},indent=2))
if __name__=='__main__':extract()
