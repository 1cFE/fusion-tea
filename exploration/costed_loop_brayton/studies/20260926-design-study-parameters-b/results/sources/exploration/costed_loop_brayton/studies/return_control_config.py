"""Write the audited configuration of study 20260926-design-study-parameters-b (goal design-study-parameters, round 3): the
starting configuration, the leading alternatives and the S6 point re-evaluated on the WI-095 package (arrangement B, the
bypass fraction reported and the return checks enforced), a fine ratio ladder near the heat-removal boundary at the design
flow and at the best band's flow, the I-A starting point for the record, and the boundary family (arrangement A: the ratio
at which the exchanger is exactly matched, one per flow, solved on the oracle inside a declared bracket). Every case is a
complete input map composed on the manifest baseline; nothing is optimized inside the model.

Run from the repository root: return_control_config.py --record <record-dir>
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from exploration.costed_loop_brayton.studies import flow_ratio_config as base

STUDY_ID = '20260926-design-study-parameters-b'
QUESTION = ('On the WI-095 package (the WI-094 costed C-1 assembly with the loop return requirement enforced by an explicit primary-side '
            'bypass control): which of the round-1 leading operating points satisfy the completed loop model and with what bypass '
            'fraction (arrangement B); where the exactly matched settings lie at each flow (arrangement A, the bypass fraction at a '
            'tiny target); and how the performance and cost comparison reads on cases that satisfy the completed model. No point is '
            'optimized inside the model; the boundary ratio is a study-level root solve on the package-owned oracle with the ratio '
            'then a chosen input of the executed case.')
IR = base.INVENTORIES['ir']['values']
IA = base.INVENTORIES['ia']['values']


def design(name, flow, ratio, arm, classification, extra=None, inventory=None):
    values = {'cycle_flow': float(flow), 'stage_ratio': float(ratio)} | (inventory or {}) | (extra or {})
    return {'name': name, 'arm': arm, 'classification': classification, 'values': values}


DESIGNS = [
    design('ir-f2500-r1.5183', 2500, base.START_RATIO, 'leading', 'the starting configuration (C-1 design point) on I-R'),
    design('ir-f2250-r1.5183', 2250, base.START_RATIO, 'leading', 'best passing band (round 1)'),
    design('ir-f2750-r1.3750', 2750, 1.375, 'leading', 'best passing band (round 1)'),
    design('ir-f3000-r1.3250', 3000, 1.325, 'leading', 'third passing point (round 1)'),
    design('ir-f2500-r1.4500', 2500, 1.45, 'leading', "the screen's best passing point at the design flow (round 1)"),
    design('ir-f2500-r1.4250', 2500, 1.425, 'leading', 'the electricity-only best (round 1): heat removal fails; expected infeasible'),
    design('s6-hx75000-f2500-r1.4000', 2500, 1.40, 'leading', 'S6: the 75,000 m2 exchanger alternative at its round-1 best passing point', {'exchanger_area': 75000.0}),
    design('ia-f2500-r1.5183', 2500, base.START_RATIO, 'leading', 'the starting configuration on the ARIES-selected inventory I-A (failed selection, for the record)', inventory=IA),
] + [design(f'ir-f2500-r{r:.4f}', 2500, r, 'ladder', 'fine ratio ladder at the design flow between the round-1 grid steps 1.425 and 1.45') for r in (1.430, 1.435, 1.440, 1.445)] \
  + [design(f'ir-f2250-r{r:.4f}', 2250, r, 'ladder', 'fine ratio ladder at the best band flow between 1.50 and 1.5183') for r in (1.505, 1.510, 1.515)]

BOUNDARY = {'inventory': 'ir', 'target_bypass_fraction': 1e-6, 'flows': [2000.0, 2250.0, 2500.0, 2750.0, 3000.0, 3250.0, 3500.0, 4000.0],
            'brackets': {'2000': [1.60, 1.70], '2250': [1.50, 1.5182944859378311], '2500': [1.425, 1.45], '2750': [1.35, 1.375], '3000': [1.30, 1.325],
                         '3250': [1.25, 1.30], '3500': [1.20, 1.25], '4000': [1.20, 1.25]},
            'provenance': "brackets are the round-1 grid's last failing and first passing ratio at each flow (record 20260926-design-study-parameters, readout section 3); at 4,000 kg/s the first grid ratio 1.20 already passes, so the boundary lies below the declared window and is reported, not solved",
            'note': 'the target 1e-6 is a root-finding target just inside the feasible side (the bypass fraction is continuous and zero at the boundary), not a physical allowance'}


def config():
    return {'study_id': STUDY_ID, 'question': QUESTION, 'axes': base.AXES, 'grid_axes': {'flow_axis': 'cycle_flow', 'ratio_axis': 'stage_ratio'},
            'inventories': base.INVENTORIES, 'designs': DESIGNS, 'boundary': BOUNDARY}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', type=Path, required=True)
    args = parser.parse_args()
    args.record.mkdir(parents=True, exist_ok=True)
    with (args.record / 'config.json').open('x') as stream:
        json.dump(config(), stream, indent=1, allow_nan=False)
        stream.write('\n')
    print(json.dumps({'config': str(args.record / 'config.json'), 'designs': len(DESIGNS), 'boundary_flows': len(BOUNDARY['flows'])}))


if __name__ == '__main__':
    main()
