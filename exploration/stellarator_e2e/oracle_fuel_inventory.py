"""Independent WI-069 deterministic-delay inventory oracle.

Authority: WI-069/design.md and evidence/proposed-abi.md, released 2026-09-19.
No production implementation imports. Amounts are per fusion module, in T atoms;
kg and calendar channels are explicit conversions, not plant-module rollups.
"""
import math

DEFAULTS = dict(inventory_enabled=True, held_inventory=0.0, m_D_kg=3.3435837768e-27,
                tau_feed=1200.0, tau_process=14400.0, tau_blanket=86400.0,
                tau_extract=86400.0, tau_buffer=0.0, reserve_fraction=0.25,
                tau_reserve=86400.0, startup_extension=0.0,
                shutdown_duration=86400.0, s_per_year=31536000.0)
STOCKS = ('feed', 'plasma', 'processor', 'blanket', 'extraction', 'buffer',
          'reserve', 'working', 'total')
STARTUP = ('prefill', 'startup_deficit', 'startup_minimum',
           'startup_decay_allowance', 'startup_conservative')
RATES = ('burn', 'injection', 'exhaust', 'recycle', 'production', 'extracted',
         'recycle_loss', 'extraction_loss')
OUTPUTS = (
    *(f'{name}_{unit}' for name in STOCKS + STARTUP for unit in ('atoms', 'kg')),
    'recycle_delay_s', 'breeding_delay_s', 'startup_horizon_s', 'max_decay_residence',
    *(f'{name}_{unit}' for name in RATES for unit in ('kg_s', 'kg_day')),
    *(f'dt_{name}_{unit}' for name in ('injection', 'processor') for unit in ('kg_s', 'kg_day')),
    'decay_kg_s', 'makeup_signed_kg_s', 'external_shortfall_kg_s',
    *(f'annual_{name}_kg' for name in RATES),
    'annual_decay_kg', 'annual_makeup_signed_kg', 'annual_external_shortfall_kg',
    'calendar_processor_kg_s', 'shutdown_remaining_kg', 'shutdown_decay_loss_kg',
    'defined_flag',
)


def evaluate(**p):
    """Evaluate exact ABI input names with `_in` removed; missing keys fail closed."""
    enabled = p['enabled']
    if enabled not in (False, True, 0.0, 1.0):
        raise ValueError('inventory oracle: activation must be binary')
    out = dict.fromkeys(OUTPUTS, 0.0)
    if not enabled:
        held = p['held_inventory']
        if not math.isfinite(held) or held < 0:
            raise ValueError('inventory oracle: invalid held stock')
        out['total_atoms'] = held
        return out
    if any(not math.isfinite(value) for value in p.values()):
        raise ValueError('inventory oracle: nonfinite input')
    if p['breeding_defined'] not in (0., 1.):
        raise ValueError('inventory oracle: breeding applicability must be binary')
    for key in ('p_fus', 'q_eff', 'mev_to_joules', 'm_T_kg', 'm_D_kg', 's_per_year'):
        if p[key] <= 0:
            raise ValueError(f'inventory oracle: {key} must be positive')
    for key in ('held_inventory', 'lambda_T', 'plasma_volume', 'n_T0', 'tbr_available',
                'tau_feed', 'tau_process', 'tau_blanket', 'tau_extract', 'tau_buffer',
                'tau_reserve', 'startup_extension', 'shutdown_duration'):
        if p[key] < 0:
            raise ValueError(f'inventory oracle: negative {key}')
    for key in ('burn_fraction', 'eta_extract'):
        if not 0 < p[key] <= 1:
            raise ValueError(f'inventory oracle: invalid {key}')
    for key in ('t_recycle', 'reserve_fraction', 'availability'):
        if not 0 <= p[key] <= 1:
            raise ValueError(f'inventory oracle: invalid {key}')
    if p['G_stock'] != 0 or p['alpha_n'] <= -1:
        raise ValueError('inventory oracle: unsupported growth or density profile')
    try:
        reaction_energy = p['q_eff'] * p['mev_to_joules']
        fusion_watts = p['p_fus'] * 1e6
        shutdown_exponent = p['lambda_T'] * p['shutdown_duration']
        if not math.isfinite(reaction_energy) or reaction_energy <= 0:
            raise ValueError('inventory oracle: invalid reaction energy product')
        if not math.isfinite(fusion_watts) or not math.isfinite(shutdown_exponent):
            raise ValueError('inventory oracle: nonfinite power or shutdown exponent')
        burn = fusion_watts / reaction_energy
        if burn <= 0:
            raise ValueError('inventory oracle: positive burn underflow')
        injection = burn / p['burn_fraction']
        exhaust = injection - burn
        recycle = p['t_recycle'] * exhaust
        production = burn * p['tbr_available'] if p['breeding_defined'] else 0.
        extracted = production * p['eta_extract']
        rates = dict(zip(RATES, (burn, injection, exhaust, recycle, production,
                                extracted, (1-p['t_recycle'])*exhaust, (1-p['eta_extract'])*production)))
        stock = dict(feed=injection*p['tau_feed'],
                     plasma=p['n_T0']*p['plasma_volume']/(1+p['alpha_n']),
                     processor=exhaust*p['tau_process'], blanket=production*p['tau_blanket'],
                     extraction=production*p['tau_extract'], buffer=injection*p['tau_buffer'],
                     reserve=injection*p['reserve_fraction']*p['tau_reserve'])
        stock['working'] = math.fsum(stock[k] for k in STOCKS[:6])
        stock['total'] = stock['working'] + stock['reserve']
        recycle_delay = p['tau_process']
        breed_delay = p['tau_blanket'] + p['tau_extract']
        horizon = max(recycle_delay, breed_delay) + p['startup_extension']
        # Integrate the piecewise constant net withdrawals interval by interval.
        # This avoids using the production candidate-point expression as a mirror.
        cumulative = peak = 0.0
        edges = sorted(set((0., recycle_delay, breed_delay, horizon)))
        for left, right in zip(edges, edges[1:]):
            slope = injection - (recycle if left >= recycle_delay else 0.)
            slope -= extracted if left >= breed_delay else 0.
            cumulative += slope * (right-left)
            peak = max(peak, cumulative)
        stock['prefill'] = stock['feed'] + stock['plasma'] + stock['buffer']
        stock['startup_deficit'] = peak
        minimum = stock['prefill'] + stock['reserve'] + peak
        k = p['lambda_T'] * horizon
        if not 0 <= k < 1:
            raise ValueError('inventory oracle: decay bound requires lambda H < 1')
        allowance = k * (minimum + production*horizon)/(1-k)
        stock.update(startup_minimum=minimum, startup_decay_allowance=allowance,
                     startup_conservative=minimum+allowance)
        for name, atoms in stock.items():
            out[name+'_atoms'] = atoms
            out[name+'_kg'] = atoms*p['m_T_kg']
        out.update(recycle_delay_s=recycle_delay, breeding_delay_s=breed_delay,
                   startup_horizon_s=horizon,
                   max_decay_residence=p['lambda_T']*max(p[k] for k in (
                       'tau_feed','tau_process','tau_blanket','tau_extract','tau_buffer')),
                   defined_flag=float(p['breeding_defined']))
        for name, rate in rates.items():
            out[name+'_kg_s'] = rate*p['m_T_kg']
            out[name+'_kg_day'] = out[name+'_kg_s']*86400.
            out['annual_'+name+'_kg'] = out[name+'_kg_s']*p['availability']*p['s_per_year']
        for name, rate in (('injection',injection), ('processor',exhaust)):
            out['dt_'+name+'_kg_s'] = rate*(p['m_T_kg']+p['m_D_kg'])
            out['dt_'+name+'_kg_day'] = out['dt_'+name+'_kg_s']*86400.
        decay = stock['total']*p['lambda_T']*p['m_T_kg']
        operating = (burn + rates['recycle_loss'] - extracted)*p['m_T_kg']
        annual = (operating*p['availability']+decay)*p['s_per_year']
        passive_loss = -math.expm1(-shutdown_exponent)
        out.update(decay_kg_s=decay, makeup_signed_kg_s=operating+decay,
                   external_shortfall_kg_s=max(0.,operating+decay), annual_decay_kg=decay*p['s_per_year'],
                   annual_makeup_signed_kg=annual, annual_external_shortfall_kg=max(0.,annual),
                   calendar_processor_kg_s=out['annual_exhaust_kg']/p['s_per_year'],
                   shutdown_remaining_kg=out['total_kg']*math.exp(-shutdown_exponent),
                   shutdown_decay_loss_kg=out['total_kg']*passive_loss)
    except (OverflowError, ZeroDivisionError) as exc:
        raise ValueError('inventory oracle: invalid arithmetic') from exc
    if any(not math.isfinite(value) for value in out.values()):
        raise ValueError('inventory oracle: nonfinite arithmetic')
    return out
