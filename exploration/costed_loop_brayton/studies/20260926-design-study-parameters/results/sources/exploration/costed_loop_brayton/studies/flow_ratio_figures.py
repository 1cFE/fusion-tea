"""Figures for study 20260926-design-study-parameters from results/readout.json: (1) the flow x ratio map on inventory I-R
with every failed and refused case marked; (2) the LCOE contribution comparison at the key cases. Writes SVG and PNG plus
the plotted data (results/figures/figure-data.json). Presentation only.

Run from the repository root: flow_ratio_figures.py <record-dir>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

CONTRIB = ['capital', 'om', 'tritium', 'deuterium', 'consumables', 'imports', 'supply', 'replacement', 'other_overhaul', 'terminal', 'salvage']
PLANT_SIDE = [c for c in CONTRIB if c not in ('tritium', 'deuterium', 'supply')]


def map_figure(ro, out):
    flows = [b['flow'] for b in ro['ir_bands']]
    ratios = [s['ratio'] for s in ro['ir_bands'][0]['ratios']]
    net = np.full((len(flows), len(ratios)), np.nan)
    status = [[None] * len(ratios) for _ in flows]
    for i, b in enumerate(ro['ir_bands']):
        for j, s in enumerate(b['ratios']):
            status[i][j] = s
            if s['status'] != 'refused':
                net[i, j] = s['net']
    fig, ax = plt.subplots(figsize=(11, 6.5))
    xi = np.arange(len(ratios)); yi = np.arange(len(flows))
    mesh = ax.pcolormesh(np.arange(len(ratios) + 1) - 0.5, np.arange(len(flows) + 1) - 0.5, np.ma.masked_invalid(net), cmap='viridis', shading='flat')
    cbar = fig.colorbar(mesh, ax=ax); cbar.set_label('net electricity, MW (evaluated cases; grey = refused by the oracle scan)')
    data = []
    for i, f in enumerate(flows):
        for j, r in enumerate(ratios):
            s = status[i][j]
            rec = {'flow': f, 'ratio': r, 'status': s['status']}
            if s['status'] == 'pass':
                ax.plot(j, i, 'o', mfc='white', mec='black', ms=7)
            elif s['status'] == 'refused':
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, color='0.85', zorder=0))
                ax.plot(j, i, '^', mfc='none', mec='0.4', ms=7)
                rec['error'] = s['error']
            else:
                rec['failed_checks'] = s['failed_checks']; rec['net'] = s['net']; rec['unmet'] = s['unmet']
                if 'checks__heat_removal_ok' in s['failed_checks']:
                    ax.plot(j, i, 'x', color='red', ms=9, mew=2)
                else:
                    ax.plot(j, i, 's', mfc='none', mec='orange', ms=9, mew=2)
            if s['status'] == 'pass':
                rec['net'] = s['net']
            data.append(rec)
    rows = ro['rows']
    def mark(case, marker, label, color):
        r = rows[case]
        ax.plot(ratios.index(r['ratio']), flows.index(r['flow']), marker, ms=16, mfc='none', mec=color, mew=2.5, label=f"{label}: {r['net']:.1f} MW")
    mark(ro['starting_point'], 'D', 'starting point 2,500 / 1.518', 'white')
    for k in ro['best_passing_band']:
        r = rows[k]; mark(k, 'D', f"best passing {r['flow']:g} / {r['ratio']:.4g}", 'cyan')
    mark(ro['electricity_only_best'], 'D', 'electricity-only best 2,500 / 1.425 (7.8 MW unmet)', 'magenta')
    ax.plot([], [], 'o', mfc='white', mec='black', label='all nine checks satisfied')
    ax.plot([], [], 'x', color='red', mew=2, label='heat removal fails (unmet source heat)')
    ax.plot([], [], 's', mfc='none', mec='orange', mew=2, label='rating screen fails (I-R compressor 3,200 MW)')
    ax.plot([], [], '^', mfc='none', mec='0.4', label='refused (nonpositive net; precooler guard at 4,000 / 1.80)')
    ax.set_xticks(xi); ax.set_xticklabels([f'{r:.4g}' for r in ratios], rotation=45)
    ax.set_yticks(yi); ax.set_yticklabels([f'{f:g}' for f in flows])
    ax.set_xlabel('equal stage pressure ratio (three compressor stages)'); ax.set_ylabel('cycle mass flow, kg/s')
    ax.set_title('Inventory I-R: net electricity over the cycle flow x stage-ratio grid, every case marked (study 20260926-design-study-parameters)')
    ax.legend(loc='upper right', fontsize=8, framealpha=0.95)
    fig.tight_layout()
    fig.savefig(out / 'flow-ratio-map.svg'); fig.savefig(out / 'flow-ratio-map.png', dpi=150)
    plt.close(fig)
    return data


def contribution_figure(ro, out):
    rows = ro['rows']
    keys = ro['key_cases']
    labels = {k: k for k in keys}
    fig, axes = plt.subplots(1, 2, figsize=(13, 6), gridspec_kw={'width_ratios': [1, 1]})
    data = {}
    for ax, parts, title in ((axes[0], CONTRIB, 'all eleven contributions (tritium purchases dominate under no-credit)'),
                             (axes[1], PLANT_SIDE, 'plant-side contributions (fuel and supply service removed)')):
        bottoms_pos = np.zeros(len(keys)); bottoms_neg = np.zeros(len(keys))
        for c in parts:
            vals = np.array([rows[k]['contributions'][c] for k in keys])
            pos = np.where(vals >= 0, vals, 0); neg = np.where(vals < 0, vals, 0)
            ax.bar(range(len(keys)), pos, bottom=bottoms_pos, label=c); ax.bar(range(len(keys)), neg, bottom=bottoms_neg)
            bottoms_pos += pos; bottoms_neg += neg
        ax.set_xticks(range(len(keys))); ax.set_xticklabels([labels[k] for k in keys], rotation=35, ha='right', fontsize=8)
        ax.set_ylabel('USD2004 per MWh'); ax.set_title(title, fontsize=10)
        for i, k in enumerate(keys):
            total = sum(rows[k]['contributions'][c] for c in parts)
            ax.text(i, total, f'{total:.0f}', ha='center', va='bottom', fontsize=8)
    axes[0].legend(fontsize=7, loc='upper right')
    for k in keys:
        data[k] = {'net_mw': rows[k]['net'], 'lcoe': rows[k]['lcoe'], 'plant_side_lcoe': rows[k]['plant_side_lcoe'], 'contributions': rows[k]['contributions'], 'overnight': rows[k]['overnight'], 'passing': rows[k]['passing']}
    fig.suptitle('LCOE contributions at the key cases (conditional absolute values; the paired deltas are the comparison)', fontsize=11)
    fig.tight_layout()
    fig.savefig(out / 'contributions.svg'); fig.savefig(out / 'contributions.png', dpi=150)
    plt.close(fig)
    return data


def main(record):
    record = Path(record)
    ro = json.load(open(record / 'results/readout.json'))
    out = record / 'results/figures'; out.mkdir(exist_ok=True)
    data = {'map': map_figure(ro, out), 'contributions': contribution_figure(ro, out)}
    (out / 'figure-data.json').write_text(json.dumps(data, indent=1, allow_nan=False) + '\n')
    print(json.dumps({'figures': sorted(p.name for p in out.iterdir())}))


if __name__ == '__main__':
    main(sys.argv[1])
