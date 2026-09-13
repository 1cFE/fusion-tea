"""Compare applicable driver identities with the recorded 1costingFE source revision."""
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

REFERENCE = Path('/home/reid/1cfe/1costingfe')
EXPECTED = '02543850089be175ea7c28b92a8b2a4184e1637e'
revision = subprocess.check_output(['git', '-C', str(REFERENCE), 'rev-parse', 'HEAD'], text=True).strip()
if revision != EXPECTED:
    raise RuntimeError('1costingFE reference revision changed')
sys.path.insert(0, str(REFERENCE / 'src'))
import jax
jax.config.update('jax_enable_x64', True)
from costingfe.layers.physics import pulsed_thermal_forward
from costingfe.types import Fuel

HERE = Path(__file__).resolve().parent
P = 'hif_plant_pkg__hif_plant__'
rows = []
for case in json.loads((HERE / 'results/cases.json').read_text())['cases']:
    v, outputs = case['inputs'], case['outputs']
    balance = pulsed_thermal_forward(
        p_fus=outputs[P+'lcoe_calc__fusion_power']/1e6, fuel=Fuel.DT,
        e_driver_mj=v[P+'driver__beam_energy_mj'], f_rep=v[P+'frequency'],
        mn=v[P+'chamber__blanket_energy_multiple'], eta_th=v[P+'thermal_efficiency'],
        eta_pin=v[P+'driver__efficiency'], f_rad=0, f_sub=0, p_pump=0,
        p_trit=0, p_house=0, p_cryo=0, p_target=0)
    bank = float(balance.e_stored_mj)*1e6
    # All non-driver recirculating inputs are zero in this identity-only check.
    driver = float(balance.p_et / balance.q_eng)*1e6
    assert math.isclose(bank, outputs[P+'driver__meier_cost__bank_energy_joules'], rel_tol=1e-12)
    assert math.isclose(driver, outputs[P+'lcoe_calc__driver_electric_power'], rel_tol=1e-12)
    rows.append({'role':case['role'], 'bank_energy_joules':bank, 'driver_electric_watts':driver})
paths=['src/costingfe/layers/physics.py','src/costingfe/types.py','src/costingfe/layers/cas22.py','src/costingfe/defaults.py','src/costingfe/data/defaults/pulsed_heavy_ion.yaml']
result={'revision':revision,'scope':'Bank energy and driver wall-plug power only; non-driver recirculating inputs set to zero solely to isolate that identity. No net-power or LCOE parity claim.',
        'rows':rows,'sources':[{'path':p,'sha256':hashlib.sha256((REFERENCE/p).read_bytes()).hexdigest()} for p in paths]}
(HERE/'results/1costingfe-driver-identities.json').write_text(json.dumps(result,indent=2)+'\n')
