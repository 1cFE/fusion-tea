"""Fresh reviewer: original TSV, independent midpoint integration; no author imports."""
import csv
import hashlib
import json
import math
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
E = Path(__file__).resolve().parent.parent
S = E / 'physical-research/screening'
reported = json.loads((S / 'results.json').read_text())
baseline = json.loads((E / 'entering-validation/baseline/baseline_result.json').read_text())
defaults = json.loads((ROOT / 'exploration/stellarator_e2e/generated/inputs/stellarator_plant_params.json').read_text())
prefix = 'stellarator_09__stellaris__heat_transport__'
assert defaults[prefix + 'n_loops'] == 14
qihx = baseline['channels'][prefix + 'primary_loop__q_ihx']
cs = qihx / 195
shaft = cs * 1e6 / 1560 * 9.80665 * 40 / .75 / 1e6
cold = 270 - shaft / cs
q = qihx + shaft
assert math.isclose(q, baseline['channels'][prefix + 'equipment__conversion_heat_MW'], rel_tol=1e-13)
assert math.isclose(shaft / .95, baseline['channels'][prefix + 'equipment__salt_electric_MW'], rel_tol=1e-13)
out = {'Q_IHX_MW': qihx, 'Q_SG_MW': q, 'shaft_MW': shaft, 'salt_return_C': cold, 'cases': [], 'hashes': {}}
class Table(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.row, self.cell = [], [], None
    def handle_starttag(self, tag, attrs):
        if tag == 'tr': self.row = []
        if tag in ('td', 'th'): self.cell = ''
    def handle_data(self, data):
        if self.cell is not None: self.cell += data
    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.cell is not None:
            self.row.append(self.cell.strip())
            self.cell = None
        if tag == 'tr' and len(self.row) == 14 and self.row[-1] in ('liquid', 'vapor'):
            self.rows.append(self.row)
for grid, filename in [('1K', 'nist-original-1K.tsv'), ('0.5K', 'nist-original-halfK.tsv')]:
    source = S / filename
    out['hashes'][filename] = hashlib.sha256(source.read_bytes()).hexdigest()
    with source.open() as f:
        rows = list(csv.reader(f, delimiter='\t'))[1:]
    slug = 'nist_webbook_water6_2mpa171to455c_' + ('halfk_' if grid == '0.5K' else '') + 'state_table'
    original = ROOT / 'knowledge/sources' / slug / 'raw.html'
    parser = Table()
    parser.feed(original.read_text())
    assert rows == parser.rows
    out['hashes'][slug + '/raw.html'] = hashlib.sha256(original.read_bytes()).hexdigest()
    out[grid + '_all14column_rows_match'] = len(rows)
    assert all(float(r[1]) == 6.2 for r in rows)
    rows = [(float(r[0]), float(r[5]), float(r[6]), r[-1]) for r in rows]
    for approach, author in zip((10, 20, 30), reported['cases'][grid]):
        pts = [r for r in rows if r[0] <= 465 - approach]
        h0, h3 = pts[0][1], pts[-1][1]
        flow = 1000 * q / (h3 - h0)
        ua = [0., 0., 0.]
        duties = [0., 0., 0.]
        gaps = [cold + (r[1] - h0) / (h3 - h0) * (465 - cold) - r[0] for r in pts]
        slopes = []
        entropy = 0.
        for i, (a, b) in enumerate(zip(pts, pts[1:])):
            dh, dt = b[1] - a[1], b[0] - a[0]
            section = 1 if a[3] != b[3] else (0 if a[3] == 'liquid' else 2)
            duties[section] += flow * dh / 1000
            # Independent composite midpoint quadrature, with all latent-heat substeps.
            n = 10000 if section == 1 else 64
            ua[section] += flow * dh / 1000 / n * sum(1 / (gaps[i] + (j + .5) / n * (gaps[i+1] - gaps[i])) for j in range(n))
            entropy += dh / n * sum(1 / (a[0] + 273.15 + (j + .5) / n * dt) for j in range(n))
            if dt:
                slopes.append((465 - cold) / (h3 - h0) - dt / dh)
        assert max(slopes) < 0
        assert min(gaps) == approach
        assert math.isclose(sum(duties), q, rel_tol=1e-13)
        assert math.isclose(sum(ua), author['UA_total_MW_K'], rel_tol=1e-7)
        assert abs(entropy - (pts[-1][2] - pts[0][2])) < 1e-5
        for duty, section in zip(duties, author['sections']):
            assert math.isclose(duty, section['duty_MW'], rel_tol=1e-13)
        eta = .1802 * math.log(465 - approach + 273) - .7823
        ew = flow / 1000 * (h3 - h0 - 315.15 * (pts[-1][2] - pts[0][2]))
        es = q * (1 - 315.15 * math.log((465 + 273.15) / (cold + 273.15)) / (465 - cold))
        assert 0 < q * eta < ew < es
        assert math.isclose(ew, author['water_exergy_gain_MW'], rel_tol=1e-13)
        assert author['thermal_20K_screen_satisfied'] == (approach >= 20)
        out['cases'].append({'grid': grid, 'approach_K': approach, 'duties_MW': duties, 'UA_MW_per_K': ua, 'UA_relative_error': sum(ua) / author['UA_total_MW_K'] - 1, 'min_gap_K': min(gaps), 'max_single_phase_gap_slope': max(slopes), 'water_exergy_MW': ew, 'salt_exergy_MW': es, 'fit_to_water_exergy': q * eta / ew})
(Path(__file__).parent / 'receipt.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
