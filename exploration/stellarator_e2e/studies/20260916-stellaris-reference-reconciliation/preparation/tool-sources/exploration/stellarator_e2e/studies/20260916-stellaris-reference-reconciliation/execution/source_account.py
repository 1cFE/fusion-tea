"""Paired supplied-source divertor account; no prediction validation."""
from pathlib import Path
import json
h=Path(__file__).resolve().parents[1]
rows=[]
for label,capture,peak,temp,diff in [('high-temperature',.99,9.5,200,1),('low-temperature',.97,5.,100,3)]:
 nonradiated=500*(1-.90);deposited=nonradiated*capture;uncaptured=nonradiated*(1-capture)
 rows.append({'case':label,'supplied':{'input_power_MW':500,'radiation_fraction':.90,'capture_fraction':capture,'peak_MW_m2':peak,'temperature_eV':temp,'diffusion_m2_s':diff},'derived':{'nonradiated_power_MW':nonradiated,'deposited_power_MW':deposited,'uncaptured_power_MW':uncaptured,'peak_equivalent_area_m2':deposited/peak},'evidence':'preparation/source-review.md, original Stellaris p15','claim':'Accounting consistency only. Supplied peak is not predicted or validated; equivalent area is not measured wetted geometry.'})
(h/'results/source-conditioned-divertor.json').write_text(json.dumps({'scope':'Separate paired source cases, not injected all-plant outputs','cases':rows},indent=2)+'\n')
