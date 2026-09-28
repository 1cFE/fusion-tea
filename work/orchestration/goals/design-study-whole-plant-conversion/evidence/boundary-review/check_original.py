"""Independent retained-evidence checks; no production imports or mutations."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
HERE = Path(__file__).resolve().parent
baseline = ROOT / 'work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/integration/baseline.json'
b = json.loads(baseline.read_text())
outputs = {k.removeprefix('stellarator_09__stellaris__'): v for k, v in b['outputs'].items()}
alpha = 3.52 / 17.58
cases = []
for source in (2500., 2800., 3000.):
    fusion = (source - 50.) / (1.2 * (1-alpha) + alpha)
    assert abs((1.2*(1-alpha)+alpha)*fusion+50-source) < 1e-9
    cases.append(dict(source_MW=source, fusion_MW=fusion,
                      divertor_peak_MW_m2=9.5*(1-.9)*(.95*.2002*fusion+50)/50,
                      tritium_burn_kg_FPY=fusion*1e6/(17.58*1.602176634e-13)*5.008267660e-27*31536000))
html = (ROOT / 'knowledge/sources/federal_reserve_bank_of_minneapolis_annual_consumer_price/raw.html').read_text()
rows = [' '.join(re.sub('<[^>]*>', ' ', row).split()).replace('&nbsp;', '') for row in re.findall(r'<tr\b[^>]*>(.*?)</tr>', html, re.S)]
cpi = [row for row in rows if re.match(r'^\s*(2004|2024|2025|2026\*)\s', row)]
report = dict(baseline_sha256=hashlib.sha256(baseline.read_bytes()).hexdigest(),
              baseline_failed_constraints={k:v for k,v in b['responses'].items() if v != 'satisfied'},
              selected_native_outputs={k:v for k,v in outputs.items() if any(t in k for t in ('conductor_current__allowable_current','conductor_current__field_extrapolated','conductor_current__margin_current','calendar__coil_life_margin','occupancy_area_margin','breeding__tbr_lower','inventory__startup_conservative_kg'))},
              source_checks=cases, retained_cpi_rows=cpi,
              limitations='Arithmetic checks on retained sources; no model execution or physical qualification. Divertor uses existing rounded0.2002 plasma alpha convention; source inversion uses3.52/17.58.')
(HERE/'original-checks.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
