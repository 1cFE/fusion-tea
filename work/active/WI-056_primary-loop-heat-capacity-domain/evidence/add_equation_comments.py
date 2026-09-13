"""Retain every exact normative expression alongside manual-required outputs."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
p=ROOT/'models/library/analyses/mfe_primary_loop.sysml'
s=p.read_text();equations={'mdot':'q_source_in * 1.0e6 / (cp_in * dT_blanket_in)','T_out':'T_in_in + dT_blanket_in','mdot_loop':'mdot / n_loops_in','dp_loop':'f_loss_in * dp_loop_ref_in * (mdot_loop / mdot_loop_ref_in) ** 2','p_loop_margin':'p_loop_in - dp_loop','r_comp':'p_loop_in / (p_loop_in - dp_loop)','T_comp_in':'T_in_in / (1.0 + (r_comp ** k_isen - 1.0) / eta_is_in)','w_fluid':'mdot * cp_in * (T_in_in - T_comp_in) / 1.0e6','p_elec':'w_fluid / eta_drive_in','q_ihx':'q_source_in + w_fluid','capacity_margin':'mdot_loop_ref_in - mdot_loop','p_pump_total':'loop_live_in * p_elec + p_pump_direct_in','q_recovered_total':'loop_live_in * w_fluid + eta_p_direct_in * p_pump_direct_in'}
for name,expr in equations.items():s=s.replace('        out attribute '+name+' : Real;',f'        // {name} = {expr};\n        out attribute {name} : Real;')
s=s.replace('        // T_comp_in =','        // k_isen = (gamma_in - 1.0) / gamma_in;\n        // T_comp_in =')
p.write_text(s);(ROOT/'exploration/stellarator_e2e/models/analyses/mfe_primary_loop.sysml').write_text(s)
