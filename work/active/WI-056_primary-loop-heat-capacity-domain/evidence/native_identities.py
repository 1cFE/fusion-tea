"""Independent identities on published native outputs, beyond parity."""
import json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent
rows=json.loads((HERE/'corrected-native.json').read_text())['cases'];P='stellarator_09__stellaris__';L=P+'primary_loop__'
base=rows['baseline']['outputs'];checks={}
for name,cp,dt in [('baseline',5193.,200.),('double_cp',10386.,200.),('double_dT',5193.,400.)]:
 o=rows[name]['outputs'];q=o[P+'source_heat__q_source'];flow=o[L+'mdot'];work=o[L+'w_fluid']
 for a,b in [(flow*cp*dt/1e6,q),(o[L+'mdot_loop']*14,flow),(o[L+'q_ihx']-q,work),(o[L+'p_elec'],work),(o[L+'q_recovered_total'],work),(o[L+'p_pump_total'],work)]:assert math.isclose(a,b,rel_tol=1e-12)
 if name!='baseline':
  assert flow==base[L+'mdot']/2
  assert o[L+'dp_loop']==base[L+'dp_loop']/4
 checks[name]={'reconstructed_heat_MW':flow*cp*dt/1e6,'flow_kg_s':flow,'pressure_loss_Pa':o[L+'dp_loop'],'fluid_work_MW':work,'relative_tolerance':1e-12}
(HERE/'native-identities.json').write_text(json.dumps(checks,indent=2)+'\n');print(checks)
