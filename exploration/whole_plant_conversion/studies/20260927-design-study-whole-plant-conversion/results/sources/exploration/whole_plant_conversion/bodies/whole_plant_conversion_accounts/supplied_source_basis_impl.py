"""WI-098 reviewed supplied-source algebra; MW, K, MW/m2. No sustainment inference."""
import math
AUTO_IMPLEMENTED=False
INPUTS=dict(q_source_MW=2500.,deposited_heating_MW=50.,neutron_multiplier=1.2,heating_source_efficiency=.5,heating_coupling_efficiency=1.,heating_coupled_rating=50.,heating_wall_rating=100.,fusion_envelope_MW=2652.5632625175904,wall_reference=3.9788448937763854,wall_fusion_reference=2652.5632625175904,divertor_limit=10.,alpha_proxy=.2002,alpha_retention=.95,radiation_fraction=.9,divertor_peaking=9.5,divertor_area=50.)
OUTPUTS='fusion_MW reconstructed_source_MW source_residual source_qualified heating_wall_MW heating_loss_MW heating_coupled_margin heating_wall_margin wall_load divertor_load divertor_margin fusion_envelope_margin domain_supported'.split()
def calculate(x):
    if min(x['heating_source_efficiency'],x['heating_coupling_efficiency'],x['wall_fusion_reference'],x['divertor_area'])<=0:raise ValueError('source algebra domain')
    a=3.52/17.58;k=x['neutron_multiplier']*(1-a)+a
    p=(x['q_source_MW']-x['deposited_heating_MW'])/k
    h=x['deposited_heating_MW']/(x['heating_source_efficiency']*x['heating_coupling_efficiency'])
    d=x['divertor_peaking']*(1-x['radiation_fraction'])*(x['alpha_retention']*x['alpha_proxy']*p+x['deposited_heating_MW'])/x['divertor_area']
    return dict(fusion_MW=p,reconstructed_source_MW=k*p+x['deposited_heating_MW'],source_residual=k*p+x['deposited_heating_MW']-x['q_source_MW'],source_qualified=0.,heating_wall_MW=h,heating_loss_MW=h-x['deposited_heating_MW'],heating_coupled_margin=x['heating_coupled_rating']-x['deposited_heating_MW'],heating_wall_margin=x['heating_wall_rating']-h,wall_load=x['wall_reference']*p/x['wall_fusion_reference'],divertor_load=d,divertor_margin=x['divertor_limit']-d,fusion_envelope_margin=x['fusion_envelope_MW']-p,domain_supported=float(p>0 and 0<x['heating_source_efficiency']<=1 and 0<x['heating_coupling_efficiency']<=1 and x['neutron_multiplier']>0))
