"""WI-096 reviewed control admission and thermal/electric boundary algebra.

This definition has source-join and loss-join occurrences. Unused inputs are zero;
only the outputs belonging to each occurrence's declared role are consumed.
"""
import math
AUTO_IMPLEMENTED = False
INPUTS = dict(available=0., capability_open=0., raw_heat=0., feasible=0., return_residual=0.,
 primary_flow=0., exchanger_flow=0., bypass_fraction=0., pressure=0., hot_temperature=0., dp=0., loss_factor=1.1,
 total_flow_rating=4000., exchanger_flow_rating=4000., bypass_flow_rating=2000., max_bypass=.5,
 pressure_rating=8e6, temperature_rating=800., added_dp_rating=1e5,
 salt_flow=0., salt_cp=1560., salt_shaft=0., salt_electric=0., actuation=.1,
 gross_electric=0., net_shaft=0., imported_electric=0., cycle_rejection=0.)
OUTPUTS = 'converged actual_heat unremoved_heat duty_correction raw_heat_residual raw_return_residual salt_hot salt_return steam_heat bypass_flow added_dp total_flow_margin exchanger_flow_margin bypass_flow_margin bypass_fraction_margin pressure_margin temperature_margin added_dp_margin controller_capacity_ok source_adequate generator_loss motor_import_loss salt_motor_loss rejection_load'.split()

def calculate(x):
    if any(not math.isfinite(v) for v in x.values()): raise ValueError('nonfinite boundary input')
    if x['loss_factor']<=0 or x['salt_cp']<=0: raise ValueError('positive loss factor and salt cp required')
    converged=(x['feasible']==1 and x['capability_open']>=x['available'] and
               abs(x['raw_heat']-x['available'])<=1e-8 and abs(x['return_residual'])<=1e-6)
    actual=x['available'] if converged else x['raw_heat']
    hot=465. if converged else (270+actual*1e6/(x['salt_flow']*x['salt_cp']) if x['salt_flow']>0 else 0.)
    cold=270-x['salt_shaft']*1e6/(x['salt_flow']*x['salt_cp']) if x['salt_flow']>0 else 0.
    bypass=x['primary_flow']-x['exchanger_flow']
    added=x['dp']*(1-1/x['loss_factor'])
    margins=dict(total_flow_margin=x['total_flow_rating']-x['primary_flow'],
      exchanger_flow_margin=x['exchanger_flow_rating']-x['exchanger_flow'],
      bypass_flow_margin=x['bypass_flow_rating']-bypass,
      bypass_fraction_margin=x['max_bypass']-x['bypass_fraction'],
      pressure_margin=x['pressure_rating']-x['pressure'],
      temperature_margin=x['temperature_rating']-x['hot_temperature'],added_dp_margin=x['added_dp_rating']-added)
    generator=max(x['net_shaft'],0)-x['gross_electric']
    imported_loss=x['imported_electric']+min(x['net_shaft'],0.)
    motor=x['salt_electric']-x['salt_shaft']
    return dict(converged=float(converged),actual_heat=actual,unremoved_heat=x['available']-actual,
      duty_correction=actual-x['raw_heat'],raw_heat_residual=x['raw_heat']-x['available'],raw_return_residual=x['return_residual'],
      salt_hot=hot,salt_return=cold,steam_heat=actual+x['salt_shaft'],bypass_flow=bypass,added_dp=added,
      **margins,controller_capacity_ok=float(all(v>=0 for v in margins.values())),source_adequate=float(converged),
      generator_loss=generator,motor_import_loss=imported_loss,salt_motor_loss=motor,rejection_load=x['cycle_rejection']+generator+imported_loss+motor+x['actuation'])
