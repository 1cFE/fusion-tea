"""Plot the verified nominal architecture pair, without rerunning a model.
Run: .codex-test/run python docs/write-up/aries-study-assets/render_architecture.py
"""
from pathlib import Path
import hashlib
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / 'work/orchestration/goals/design-study-exchanger-architecture/evidence/r3-data/reporting.json'
d = json.loads(SOURCE.read_text())
pairs = [p for p in d['pairs'] if p['kind']=='matched' and p['scenario']=='main' and p['offer']=='B' and abs(p['load_MW']-1835.4512830147435)<1e-6]
assert len(pairs)==1
p = pairs[0]
assert p['series_pass'] and p['network_pass']
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
fig,axes=plt.subplots(1,3,figsize=(12,4.5),layout='constrained')
for ax,keys,title,ylabel in zip(axes,[('series_flow_kg_s','network_flow_kg_s'),('series_net_MW','network_net_MW'),('series_nonfuel_lcoe','network_nonfuel_lcoe')],['Less cycle flow','More net electricity','Lower nonfuel cost contribution'],['Cycle helium flow (kg/s)','Net electricity (MW)','USD2004 per MWh']):
    vals=[p[k] for k in keys]
    bars=ax.bar(['Series','Split network'],vals,color=['#28718e','#db7b30'],width=.6)
    ax.set_ylim(0,max(vals)*1.2)
    ax.set_title(title,loc='left',fontsize=12)
    ax.set_ylabel(ylabel)
    ax.bar_label(bars,labels=[f'{v:,.2f}' for v in vals],padding=4)
    ax.grid(axis='y',alpha=.18)
    ax.set_axisbelow(True)
fig.suptitle('Same reactor heat and selected equipment; different exchanger connections',fontsize=14)
fig.supxlabel('1,835.45 MW supplied fusion power · revised inventory B · both layouts pass the thermal contract\nCost excludes recurring fuel charges, retains initial fuel capital; additional layout costs remain unknown.',fontsize=9)
for ext in ['svg','png']:
    fig.savefig(OUT/f'architecture-nominal-pair.{ext}',dpi=170,bbox_inches='tight')
plt.close(fig)
(OUT/'architecture-figure-data.json').write_text(json.dumps({'source':str(SOURCE.relative_to(ROOT)),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'pair':p,'note':'Nonfuel excludes recurring fuel charges and retains initial fuel capital. Incremental topology costs and hydraulic effects are not established.'},indent=2)+'\n')

# Normalize generated SVG whitespace for repository diffs.
for svg in OUT.glob("architecture-nominal-pair.svg"):
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
