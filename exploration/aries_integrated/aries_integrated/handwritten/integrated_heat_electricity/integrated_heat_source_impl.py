"""Reviewed source partition or explicitly supplied literal branch accounting."""
from aries_integrated.handwritten.integrated_heat_electricity.common import values, require, finish
AUTO_IMPLEMENTED = False


def _reviewed_run_integrated_heat_source(inputs):
    v = values(inputs)
    require(v['fusion_power'] > 0, 'fusion power must be positive')
    require(v['heat_mode'] in (0, 1), 'heat mode must be 0 or 1')
    require(v['neutron_multiplier'] >= 1, 'neutron multiplier must be at least one')
    for key in ('radiation_fraction', 'helium_fraction', 'exchange_fraction', 'he_recovery', 'pbli_recovery', 'divertor_recovery'):
        require(0 <= v[key] <= 1, key + ' must be in [0,1]')
    for key in ('auxiliary_heat', 'he_pump', 'pbli_pump', 'divertor_pump', 'literal_he', 'literal_pbli', 'literal_exchange', 'literal_divertor'):
        require(v[key] >= 0, key + ' must be nonnegative')
    p = v['fusion_power']
    n, a = .8*p, .2*p
    gain = (v['neutron_multiplier']-1)*n
    blanket = v['neutron_multiplier']*n + v['radiation_fraction']*a
    he, pbli = v['helium_fraction']*blanket, (1-v['helium_fraction'])*blanket
    divertor = (1-v['radiation_fraction'])*a + v['auxiliary_heat']
    exchange = v['exchange_fraction']*p
    if v['heat_mode'] == 1:
        he, pbli, divertor, exchange = (v[key] for key in ('literal_he', 'literal_pbli', 'literal_divertor', 'literal_exchange'))
    friction = {b: v[b+'_pump']*v[b+'_recovery'] for b in ('he', 'pbli', 'divertor')}
    out = dict(neutron_power=n, charged_power=a, nuclear_gain=gain, he_deposition=he,
               pbli_deposition=pbli, divertor_deposition=divertor, exchange=exchange,
               other_heat=0., source_residual=he+pbli+divertor-p-gain-v['auxiliary_heat'],
               topology_zero=0., pump_electric=sum(v[b+'_pump'] for b in friction),
               pump_recovered=sum(friction.values()))
    out.update({b+'_friction': q for b, q in friction.items()})
    return finish('integrated_heat_source', out)


from aries_integrated.modules.integrated_heat_electricity.integrated_heat_source import Integrated_Heat_SourceInput


def run_integrated_heat_source(inputs: Integrated_Heat_SourceInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float, float, float, float]:
    """Typed native adapter; delegates unchanged reviewed calculation."""
    return _reviewed_run_integrated_heat_source(inputs)
