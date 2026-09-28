"""Write the audited configuration of study 20260926-design-study-parameters (goal design-study-parameters) and the
package's axis declaration. Everything here is declared: the flow x ratio grid (contract § 11), the two inventories
(contract § 5), the sensitivity levels (contract § 10) and the anchor rule the composer applies after the oracle scan.
No value is computed from a demand; the composer (`study_support.py`) only composes and scans.

Run from the repository root: flow_ratio_config.py --record <record-dir>   (writes <record-dir>/config.json and axes.json here)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = 'costed_loop_brayton__plant__'
STUDY_ID = '20260926-design-study-parameters'
START_FLOW = 2500.0
START_RATIO = 1.5182944859378311
FLOWS = [2000.0, 2250.0, 2500.0, 2750.0, 3000.0, 3250.0, 3500.0, 4000.0]
RATIOS = [1.20, 1.25, 1.30, 1.325, 1.35, 1.375, 1.40, 1.425, 1.45, 1.475, 1.50, START_RATIO, 1.55, 1.60, 1.70, 1.80]
# The fuel chain's stored exhaust rate at the starting point (atoms/s), from
# work/completed/20260926_WI-094_costed-loop-brayton/evidence/native_runs/c1-aries-ratios-reselected-ratings/result.json; a constant of the
# sweep because the fusion power is held equal. The balance converts it at 1e-22 MW per atom/s (about 1.79 MW).
EXHAUST_RATE = 1.7893284736432182e+22
QUESTION = ('On the costed C-1 assembly (Stellaris helium loop feeding the ARIES three-stage Brayton chain, priced inventory I-R): '
            'which cycle mass flow and equal-stage compressor pressure ratio give the most net electricity and the lowest '
            'conditional LCOE with every equipment and thermal check satisfied, which check bounds the passing region on each '
            'side, why the best passing point differs from the electricity-only best, and how the answer moves under the declared '
            'sensitivities (machine efficiency, auxiliaries, pumping law, prices, fuel convention, exchanger area). The ARIES-selected '
            'inventory I-A is evaluated at the same points as a recorded alternative. Every case is a complete input map composed '
            'on the manifest baseline; nothing is optimized; no rating is changed from a demand.')


def axis(name, keys, units, role, framing, provenance, basis, missing):
    return {'axis': name, 'keys': [{'key': P + k, 'provenance': 'fan_out'} for k in keys], 'units': units, 'role': role,
            'framing': framing, 'window_provenance': provenance, 'basis': basis, 'missing_response': missing, 'declined': False}


AXES = [
    axis('cycle_flow', ['cycle__selected_flow'], 'kg/s', 'operating', 'search', 'engineered',
         'C-1 design flow 2,500 kg/s (WI-093); window 2,000-4,000 kg/s (-20 % / +60 %) fixed by the 54-point screen (contract § 8 a, § 11).',
         'No off-design machine map: the compressors and turbine keep fixed isentropic efficiencies at every flow (S1 tests uniform offsets); the loop sits upstream and its rated flow is unchanged.'),
    axis('stage_ratio', ['compressor_1__selected_ratio', 'compressor_2__selected_ratio', 'compressor_3__selected_ratio'], '1', 'operating', 'search', 'engineered',
         'C-1 equal-stage ratio 1.5183 (the ARIES designer\'s choice); window 1.20-1.80 refined to 0.025 between 1.30 and 1.50 where the screen located the heat-removal boundary (contract § 11).',
         'One value applied to three independent chosen inputs: a declared equal-stage scenario, not a physical tie (annex § Declared ties); no off-design map (S1).'),
    axis('compressor_rating', ['compressor_capacity__selected_rating'], 'MW', 'equipment', 'sensitivity', 'sourced',
         'I-R baseline 3,200 MW (WI-093 re-selection); I-A 1,600 MW, the ARIES-selected rating (WI-090 E4 reference).',
         'A violated screen keeps its booked price; nothing is resized from a demand (MR-7).'),
    axis('turbine_rating', ['turbine_capacity__selected_rating'], 'MW', 'equipment', 'sensitivity', 'sourced',
         'I-R 7,000 MW; I-A 3,500 MW (ARIES-selected).', 'As compressor_rating.'),
    axis('generator_rating', ['generator_capacity__selected_rating'], 'MW', 'equipment', 'sensitivity', 'sourced',
         'I-R 3,600 MW; I-A 1,800 MW (ARIES-selected).', 'As compressor_rating.'),
    axis('rejection_rating', ['rejection_capacity__selected_rating'], 'MW', 'equipment', 'sensitivity', 'sourced',
         'I-R 5,000 MW; I-A 2,500 MW (ARIES-selected).', 'As compressor_rating; heat-rejection pumping is not in the balance (contract § 8 c).'),
    axis('he_duty_rating', ['he_capacity__selected_rating'], 'MW', 'equipment', 'sensitivity', 'sourced',
         'I-R 3,500 MW; I-A 1,500 MW (ARIES-selected).', 'As compressor_rating.'),
    axis('compressor_efficiency', ['compressor_1__efficiency', 'compressor_2__efficiency', 'compressor_3__efficiency'], '1', 'assumption', 'sensitivity', 'engineered',
         'ARIES 0.89; 0.85 / 0.92 span the WI-090 range (contract S1). One value applied to the three stages.',
         'A uniform offset; it cannot test a penalty that grows with distance from the design point (contract § 8 a).'),
    axis('turbine_efficiency', ['cycle__turbine_efficiency'], '1', 'assumption', 'sensitivity', 'engineered',
         'ARIES 0.93; 0.90 / 0.95 (contract S1).', 'As compressor_efficiency.'),
    axis('aux_heat', ['electrical__auxiliary_heat'], 'MW coupled', 'assumption', 'sensitivity', 'engineered',
         'ARIES register 20 MW coupled at 0.5 wall-plug efficiency (40 MW electric); x0.5 / x1.5 with the rest of the register; the labelled Stellaris-equivalent register uses 50 MW coupled (100 MW wall-plug, baseline.json).',
         'A constant of the sweep: it moves absolute net and the net-positive edge, not the ranking (contract § 6, S2).'),
    axis('aux_cryo', ['electrical__cryo'], 'MW', 'assumption', 'sensitivity', 'engineered',
         'ARIES 10 MW; x0.5 / x1.5; Stellaris-equivalent 2.14 MW (cryogenic and shield, baseline.json).', 'As aux_heat.'),
    axis('aux_fuel_base', ['electrical__fuel_base'], 'MW', 'assumption', 'sensitivity', 'engineered',
         'ARIES 5 MW; x0.5 / x1.5; 0 in the labelled Stellaris-equivalent register (no counterpart named in the contract).', 'As aux_heat.'),
    axis('aux_control', ['electrical__control'], 'MW', 'assumption', 'sensitivity', 'engineered',
         'ARIES 5 MW; x0.5 / x1.5; 0 in the labelled Stellaris-equivalent register.', 'As aux_heat.'),
    axis('aux_other', ['electrical__other_electric'], 'MW', 'assumption', 'sensitivity', 'engineered',
         'ARIES 5 MW; x0.5 / x1.5; the Stellaris-equivalent register puts its cooling-water pumping 13.02 MW here (baseline.json), the bound on the omitted heat-rejection pumping.', 'As aux_heat.'),
    axis('fuel_exhaust_term', ['electrical__fuel_exhaust'], 'atoms/s', 'convention', 'sensitivity', 'engineered',
         '0 as in C-1 (so the controls replay bit-exactly); the wired case sets it to the fuel chain\'s stored exhaust rate 1.7893e22 atoms/s, about 1.79 MW at the balance\'s 1e-22 MW per atom/s (contract § 3, S2).',
         'A disclosed constant omission of the main block.'),
    axis('pump_law_dp_ref', ['primary_loop__dp_loop_ref'], 'Pa', 'assumption', 'sensitivity', 'engineered',
         'Stellaris 329,187.19 Pa reference loop pressure drop; x0.5 / x2 (contract S3). It moves the loop pump electricity and the friction heat delivered together.',
         'The loop pump law is the Stellaris relation with its constants, not a hydraulic model (contract § 8 g).'),
    axis('equipment_price_factor', ['compressor_equipment__price_factor', 'turbine_equipment__price_factor', 'generator_equipment__price_factor',
                                    'heat_rejection_equipment__price_factor', 'he_duty_equipment__price_factor', 'he_hx__price_factor', 'conversion_services__price_factor'],
         '1', 'price', 'sensitivity', 'engineered',
         'ARIES E4 reference prices at x1; x0.5 / x1.5 on the seven priced items of the inventory (contract S4).',
         'Prices decide the USD/MWh value of a net gain and the I-R against I-A comparison, not the operating ranking.'),
    axis('rest_of_plant_price_factor', ['rest_of_plant__price_factor'], '1', 'price', 'sensitivity', 'engineered',
         'The rest-of-plant constant 2,158,230,133.33 USD2004 at x1 ([ASSUMED], contract § 6); x0.5 / x2 (S4).', 'As equipment_price_factor.'),
    axis('tritium_feed', ['fuel_inventory__annual_recovery_kg'], 'kg/year', 'convention', 'sensitivity', 'sourced',
         '0 under the no-credit convention; 100 kg/year is the ARIES E6 named-feed scenario (contract S5).',
         'Breeding is unsupported: the feed is an assumption, not a calculated capability (contract § 8 f).'),
    axis('supply_service', ['finance__supply_service_annual'], 'USD2004/year', 'convention', 'sensitivity', 'sourced',
         '0; 30 MUSD/year with the named feed (ARIES E6 convention, contract S5).', 'As tritium_feed.'),
    axis('exchanger_area', ['he_hx__selected_area'], 'm2', 'equipment', 'sensitivity', 'engineered',
         'ARIES 50,000 m2 (UA 50 MW/K at the assumed 1,000 W/m2K); 75,000 m2 is the one declared priced hardware alternative (ratio 1.5, 87,488,550 USD2004 through the same purchase law; contract § 5, S6).',
         'A labelled alternative inventory, never a point-by-point resize (MR-7).'),
]

INVENTORIES = {
    'ir': {'label': 'I-R, the re-selected inventory (WI-093 case inputs; the manifest baseline)', 'values': {}},
    'ia': {'label': 'I-A, the ARIES-selected inventory (recorded alternative)',
           'values': {'compressor_rating': 1600.0, 'turbine_rating': 3500.0, 'generator_rating': 1800.0, 'rejection_rating': 2500.0, 'he_duty_rating': 1500.0}},
}

LEVELS = [
    {'id': 's1-comp0.85', 'sensitivity': 'S1', 'values': {'compressor_efficiency': 0.85}},
    {'id': 's1-comp0.92', 'sensitivity': 'S1', 'values': {'compressor_efficiency': 0.92}},
    {'id': 's1-turb0.90', 'sensitivity': 'S1', 'values': {'turbine_efficiency': 0.90}},
    {'id': 's1-turb0.95', 'sensitivity': 'S1', 'values': {'turbine_efficiency': 0.95}},
    {'id': 's2-aux0.5', 'sensitivity': 'S2', 'scales': {'aux_heat': 0.5, 'aux_cryo': 0.5, 'aux_fuel_base': 0.5, 'aux_control': 0.5, 'aux_other': 0.5}},
    {'id': 's2-aux1.5', 'sensitivity': 'S2', 'scales': {'aux_heat': 1.5, 'aux_cryo': 1.5, 'aux_fuel_base': 1.5, 'aux_control': 1.5, 'aux_other': 1.5}},
    {'id': 's2-fuelterm', 'sensitivity': 'S2', 'values': {'fuel_exhaust_term': EXHAUST_RATE}},
    {'id': 's2-stellaris', 'sensitivity': 'S2', 'values': {'aux_heat': 50.0, 'aux_cryo': 2.14, 'aux_fuel_base': 0.0, 'aux_control': 0.0, 'aux_other': 13.02}},
    {'id': 's3-dp0.5', 'sensitivity': 'S3', 'scales': {'pump_law_dp_ref': 0.5}},
    {'id': 's3-dp2', 'sensitivity': 'S3', 'scales': {'pump_law_dp_ref': 2.0}},
    {'id': 's4-price0.5', 'sensitivity': 'S4', 'values': {'equipment_price_factor': 0.5}},
    {'id': 's4-price1.5', 'sensitivity': 'S4', 'values': {'equipment_price_factor': 1.5}},
    {'id': 's4-rest0.5', 'sensitivity': 'S4', 'values': {'rest_of_plant_price_factor': 0.5}},
    {'id': 's4-rest2', 'sensitivity': 'S4', 'values': {'rest_of_plant_price_factor': 2.0}},
    {'id': 's5-feed100', 'sensitivity': 'S5', 'values': {'tritium_feed': 100.0, 'supply_service': 30e6}},
    {'id': 's6-hx75000', 'sensitivity': 'S6', 'values': {'exchanger_area': 75000.0}},
]

COLUMNS = [{'level': 's6-hx75000', 'flow': START_FLOW, 'ratios': [r for r in RATIOS if 1.30 <= r <= START_RATIO],
            'why': 'whether the larger exchanger moves the heat-removal boundary to a lower ratio along the design-flow column'}]

ANCHOR_RULE = ('Sensitivities run at the anchors on the I-R grid: the starting point; the best passing point (the highest oracle-scanned '
               'net among I-R grid points with every check satisfied); that point\'s ratio-step-lower neighbour and flow-step-higher '
               'neighbour on the grid (contract § 10); plus the declared extra anchors below. Coinciding anchors collapse to one case. '
               'The anchors are chosen from the oracle scan before any native point runs and recorded in axis-plan.json; the native '
               'run then confirms or corrects the reading.')
EXTRA_ANCHORS = [{'label': 'screen-best-passing', 'cycle_flow': START_FLOW, 'stage_ratio': 1.45,
                  'why': "the contract's named best passing point from the 54-point screen at the design flow (contract § 5, § 8 a): kept as "
                         "an anchor so the sensitivities cover the operating claim's neighbourhood near 2,500 kg/s; the r1 scan found the "
                         "refined grid's best passing point at 2,250 kg/s / 1.5183, whose flow-step-higher neighbour is the starting point "
                         "itself, which left three distinct anchors (preparation-r1/)."}]


def config():
    return {'study_id': STUDY_ID, 'question': QUESTION, 'axes': AXES,
            'grid': {'flow_axis': 'cycle_flow', 'ratio_axis': 'stage_ratio', 'flows': FLOWS, 'ratios': RATIOS,
                     'provenance': 'engineered from the 54-point screen (evidence/screen-flow-ratio.md); contract § 11'},
            'inventories': INVENTORIES,
            'sensitivities': {'anchor_rule': ANCHOR_RULE, 'starting_point': {'cycle_flow': START_FLOW, 'stage_ratio': START_RATIO},
                              'extra_anchors': EXTRA_ANCHORS, 'levels': LEVELS, 'columns': COLUMNS}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', type=Path, required=True)
    args = parser.parse_args()
    args.record.mkdir(parents=True, exist_ok=True)
    document = config()
    with (args.record / 'config.json').open('x') as stream:
        json.dump(document, stream, indent=1, allow_nan=False)
        stream.write('\n')
    groups = {'schema_version': 'study-axis-declaration/v1',
              'groups': [{'axis': a['axis'], 'keys': a['keys'], 'note': a['basis']} for a in AXES]}
    with (HERE / 'axes.json').open('w') as stream:
        json.dump(groups, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps({'config': str(args.record / 'config.json'), 'axes': str(HERE / 'axes.json'),
                      'axes_count': len(AXES), 'grid_points': len(FLOWS) * len(RATIOS), 'levels': len(LEVELS)}))


if __name__ == '__main__':
    main()
