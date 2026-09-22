"""Explicit passive bypass when turbine exhaust is colder than compressor outlet."""
from aries_integrated.handwritten.integrated_heat_electricity.common import values, require, finish
AUTO_IMPLEMENTED = False


def _reviewed_run_passive_recuperator(inputs):
    v = values(inputs)
    require(all(v[k] > 0 for k in ('cold_temperature','hot_temperature','flow','cp')), 'recuperator temperatures and capacity inputs must be positive')
    require(0 <= v['effectiveness'] <= 1, 'recuperator effectiveness must be in [0,1]')
    delta = v['effectiveness']*max(v['hot_temperature']-v['cold_temperature'],0.)
    return finish('passive_recuperator',dict(cold_out=v['cold_temperature']+delta,hot_out=v['hot_temperature']-delta,
                  recovered_heat=v['flow']*v['cp']*delta/1e6,bypass_active=float(v['hot_temperature']<=v['cold_temperature'])))


from aries_integrated.modules.integrated_heat_electricity.passive_recuperator import Passive_RecuperatorInput


def run_passive_recuperator(inputs: Passive_RecuperatorInput) -> tuple[float, float, float, float]:
    """Typed native adapter; delegates unchanged reviewed calculation."""
    return _reviewed_run_passive_recuperator(inputs)
