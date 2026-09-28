"""WI-069 nominal fuel inventory and bounded commissioning supply.

Normative authority: WI-069/design.md and mfe_fuel_cycle::Fuel Inventory.
Deterministic delays and maintained nominal stock are conditional approximations.
"""
from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from whole_plant_conversion_tea.modules.mfe_fuel_cycle.fuel_inventory import Fuel_InventoryInput

AUTO_IMPLEMENTED = False


def run_fuel_inventory(inputs: Fuel_InventoryInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float]:
    from whole_plant_conversion_tea.schemas.fuel_inventory_output import Fuel_InventoryOutput

    p = inputs
    result = dict.fromkeys(Fuel_InventoryOutput.model_fields, 0.0)
    if not all(math.isfinite(getattr(p, name)) for name in type(p).model_fields):
        raise ValueError('Fuel inventory inputs must be finite')
    if p.enabled_in not in (False, True) or p.breeding_defined_in not in (0., 1.):
        raise ValueError('Fuel inventory flags must be exact Boolean/0/1')
    if p.held_inventory_in < 0:
        raise ValueError('Held inventory must be nonnegative')
    if not p.enabled_in:
        result['total_atoms'] = p.held_inventory_in
        return tuple(result.values())
    positive = ('p_fus_in', 'q_eff_in', 'mev_to_joules_in', 'm_T_kg_in', 'm_D_kg_in', 's_per_year_in')
    if any(getattr(p, name) <= 0 for name in positive):
        raise ValueError('Power, energy, atomic masses and calendar year must be positive')
    if not (0 < p.burn_fraction_in <= 1 and 0 < p.eta_extract_in <= 1
            and 0 <= p.t_recycle_in <= 1 and 0 <= p.reserve_fraction_in <= 1
            and 0 <= p.availability_in <= 1 and p.alpha_n_in > -1):
        raise ValueError('Fuel fraction or density profile outside its domain')
    nonnegative = ('tbr_available_in', 'lambda_T_in', 'plasma_volume_in', 'n_T0_in',
                   'tau_feed_in', 'tau_process_in', 'tau_blanket_in', 'tau_extract_in',
                   'tau_buffer_in', 'tau_reserve_in', 'startup_extension_in', 'shutdown_duration_in')
    if any(getattr(p, name) < 0 for name in nonnegative) or p.G_stock_in != 0:
        raise ValueError('Stocks, rates and times must be nonnegative; active stock growth must be zero')
    try:
        energy = p.q_eff_in * p.mev_to_joules_in
        if not math.isfinite(energy) or energy <= 0:
            raise ValueError('Invalid fusion reaction energy')
        burn = p.p_fus_in * 1e6 / energy
        if not math.isfinite(burn) or burn <= 0:
            raise ValueError('Computed burn rate must be finite and positive')
        inject = burn / p.burn_fraction_in
        exhaust = inject - burn
        recycle = p.t_recycle_in * exhaust
        loss = (1 - p.t_recycle_in) * exhaust
        production = p.tbr_available_in * burn if p.breeding_defined_in else 0.
        extracted = p.eta_extract_in * production
        extraction_loss = (1 - p.eta_extract_in) * production
        stocks = dict(feed=inject * p.tau_feed_in,
                      plasma=p.n_T0_in * p.plasma_volume_in / (1 + p.alpha_n_in),
                      processor=exhaust * p.tau_process_in,
                      blanket=production * p.tau_blanket_in,
                      extraction=production * p.tau_extract_in,
                      buffer=inject * p.tau_buffer_in,
                      reserve=inject * p.reserve_fraction_in * p.tau_reserve_in)
        stocks['working'] = sum(stocks[k] for k in ('feed', 'plasma', 'processor', 'blanket', 'extraction', 'buffer'))
        stocks['total'] = stocks['working'] + stocks['reserve']
        recycle_delay = p.tau_process_in
        breeding_delay = p.tau_blanket_in + p.tau_extract_in
        horizon = max(recycle_delay, breeding_delay) + p.startup_extension_in
        k = p.lambda_T_in * horizon
        if not math.isfinite(k) or not 0 <= k < 1:
            raise ValueError('Startup decay bound requires 0 <= lambda * horizon < 1')
        deficits = [inject * t - recycle * max(t - recycle_delay, 0.)
                    - extracted * max(t - breeding_delay, 0.)
                    for t in (0., recycle_delay, breeding_delay, horizon)]
        if not all(math.isfinite(v) for v in deficits):
            raise ValueError('Nonfinite startup trajectory')
        stocks['prefill'] = stocks['feed'] + stocks['plasma'] + stocks['buffer']
        stocks['startup_deficit'] = max(deficits)
        stocks['startup_minimum'] = stocks['prefill'] + stocks['reserve'] + stocks['startup_deficit']
        stocks['startup_decay_allowance'] = k * (stocks['startup_minimum'] + production * horizon) / (1 - k)
        stocks['startup_conservative'] = stocks['startup_minimum'] + stocks['startup_decay_allowance']
        for name, atoms in stocks.items():
            result[name + '_atoms'] = atoms
            result[name + '_kg'] = atoms * p.m_T_kg_in
        result.update(recycle_delay_s=recycle_delay, breeding_delay_s=breeding_delay,
                      startup_horizon_s=horizon,
                      max_decay_residence=p.lambda_T_in * max(p.tau_feed_in, p.tau_process_in,
                          p.tau_blanket_in, p.tau_extract_in, p.tau_buffer_in),
                      defined_flag=float(p.breeding_defined_in))
        running_seconds = p.availability_in * p.s_per_year_in
        rates = dict(burn=burn, injection=inject, exhaust=exhaust, recycle=recycle,
                     production=production, extracted=extracted, recycle_loss=loss,
                     extraction_loss=extraction_loss)
        for name, rate in rates.items():
            result[name + '_kg_s'] = rate * p.m_T_kg_in
            result[name + '_kg_day'] = rate * p.m_T_kg_in * 86400.
            result['annual_' + name + '_kg'] = rate * p.m_T_kg_in * running_seconds
        for name, rate in (('dt_injection', inject), ('dt_processor', exhaust)):
            result[name + '_kg_s'] = rate * (p.m_T_kg_in + p.m_D_kg_in)
            result[name + '_kg_day'] = result[name + '_kg_s'] * 86400.
        decay = p.lambda_T_in * stocks['total'] * p.m_T_kg_in
        signed = (burn + loss - extracted) * p.m_T_kg_in + decay
        annual = (burn + loss - extracted) * p.m_T_kg_in * running_seconds + decay * p.s_per_year_in
        shutdown_exponent = p.lambda_T_in * p.shutdown_duration_in
        if not math.isfinite(shutdown_exponent):
            raise ValueError('Shutdown decay exponent must be finite')
        shutdown_loss = -math.expm1(-shutdown_exponent) * result['total_kg']
        result.update(decay_kg_s=decay, makeup_signed_kg_s=signed,
                      external_shortfall_kg_s=max(signed, 0.), annual_decay_kg=decay * p.s_per_year_in,
                      annual_makeup_signed_kg=annual, annual_external_shortfall_kg=max(annual, 0.),
                      calendar_processor_kg_s=result['annual_exhaust_kg'] / p.s_per_year_in,
                      shutdown_remaining_kg=result['total_kg'] * math.exp(-shutdown_exponent),
                      shutdown_decay_loss_kg=shutdown_loss)
        if set(result) != set(Fuel_InventoryOutput.model_fields):
            raise ValueError('Fuel inventory output schema drift')
        if not all(math.isfinite(v) for v in result.values()):
            raise ValueError('Nonfinite fuel inventory intermediate or output')
        if any(v < 0 for name, v in result.items() if name not in ('makeup_signed_kg_s', 'annual_makeup_signed_kg')):
            raise ValueError('Negative stock or unsigned rate')
        return tuple(result.values())
    except (OverflowError, ZeroDivisionError) as error:
        raise ValueError('Fuel inventory arithmetic outside finite domain') from error
