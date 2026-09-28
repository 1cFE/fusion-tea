"""Rebuild the public explainer's figures from recorded stellarator evidence.

Run from repository root:
  MPLCONFIGDIR=/tmp/codegen-writeup-mpl .codex-test/run python archive/write-up/sysml-codegen-assets/render_figures.py
"""
from pathlib import Path
import csv
import json
import subprocess
import textwrap

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
INK = '#152b40'
MUTED = '#52677a'
BLUE = '#2463a5'
TEAL = '#087e83'
GOLD = '#b75f1c'
BG = '#f7f9fc'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
                     'text.color': INK, 'axes.labelcolor': INK,
                     'axes.titlecolor': INK, 'xtick.color': MUTED,
                     'ytick.color': MUTED, 'svg.fonttype': 'none',
                     'savefig.facecolor': BG, 'figure.facecolor': BG})


def save(fig, name):
    fig.savefig(HERE / f'{name}.png', dpi=180, bbox_inches='tight', pad_inches=.22)
    fig.savefig(HERE / f'{name}.svg', bbox_inches='tight', pad_inches=.22)
    plt.close(fig)


def box(ax, x, y, w, h, title, body='', color=BLUE, fontsize=12):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.014,rounding_size=0.018',
                              linewidth=1.1, edgecolor=color, facecolor='white'))
    ax.text(x+.025, y+h-.045, title, va='top', fontsize=fontsize+1, color=color, weight='bold')
    if body:
        ax.text(x+.025, y+h-.105, body, va='top', fontsize=fontsize, linespacing=1.55)


def arrow(ax, start, end, color=MUTED, rad=0):
    ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=17,
                               color=color,lw=1.6,connectionstyle=f'arc3,rad={rad}'))


def overview():
    fig, ax=plt.subplots(figsize=(14,5.5)); ax.set(xlim=(0,1),ylim=(0,1)); ax.axis('off')
    ax.text(.015,.965,'One model, two kinds of iteration',fontsize=23,weight='bold')
    ax.text(.015,.88,'Stellarator component changes regenerate the program. Parameter studies reuse it.',color=MUTED)
    box(ax,.025,.39,.27,.34,'AUTHOR THE PLANT','SysML parts and connections\nMagnet, blanket, plasma, cooling\nEquations + engineering checks',fontsize=12)
    box(ax,.36,.39,.27,.34,'GENERATE THE PROGRAM','Resolve calculation inputs\nTranslate equations to Python\nWrite the TEAx connections',fontsize=12)
    box(ax,.695,.39,.27,.34,'EVALUATE A CANDIDATE','Set radius and ampere-turns\nCalculate outputs and cost\nRecord constraint results',color=TEAL,fontsize=12)
    arrow(ax,(.305,.56),(.348,.56)); arrow(ax,(.64,.56),(.683,.56))
    ax.text(.025,.245,'Change the model',weight='bold',fontsize=13,color=BLUE)
    ax.text(.025,.17,'Example: replace the blanket’s held breeding value\nwith a transport-response calculation.',fontsize=11.5,color=MUTED,va='top')
    ax.text(.695,.245,'Change the parameters',weight='bold',fontsize=13,color=TEAL)
    ax.text(.695,.17,'Example: sweep radius and coil ampere-turns\nusing the same generated package.',fontsize=11.5,color=MUTED,va='top')
    save(fig,'iteration-overview')


def component():
    fig, ax=plt.subplots(figsize=(15,15)); ax.set(xlim=(0,1),ylim=(0,1)); ax.axis('off')
    ax.text(.02,.972,'The equation, the plant inputs, and the calculated field',fontsize=21,weight='bold')
    ax.text(.02,.936,'Actual SysML excerpts • imports, documentation, and other members omitted; empty braces held documentation',color=MUTED,fontsize=10.8)

    box(ax,.025,.61,.95,.28,'CALCULATION DEFINITION — the mathematical relationship',fontsize=12)
    definition=("calc def 'Coil Set Axis Field' {\n"
                "    in attribute n_coils : Real;\n"
                "    in attribute I_coil : Real;\n"
                "    in attribute k_link : Real;\n"
                "    in attribute R0 : Real;\n"
                "    in attribute mu0 : Real default 1.25663706212e-6;\n"
                "    in attribute two_pi : Real default 6.283185307179586;\n\n"
                "    out attribute B_axis : Real = mu0 * k_link * n_coils * I_coil / (two_pi * R0);\n"
                "}")
    ax.text(.05,.815,definition,family='DejaVu Sans Mono',fontsize=11.8,va='top',linespacing=1.35)

    box(ax,.025,.20,.465,.335,'PLANT USAGE — supplies the coil values',color=TEAL,fontsize=11)
    plant=("part stellaris : 'MFE Power Plant' {\n"
           "    part :>> magnet {\n"
           "        part :>> coil {\n"
           "            :>> n_coils = 48.0 {}\n"
           "            :>> I_coil = 15400000.0 {}\n"
           "            :>> k_link = 0.7731331164622419 {}\n"
           "        }\n"
           "    }\n"
           "}")
    ax.text(.05,.464,plant,family='DejaVu Sans Mono',fontsize=10.4,va='top',linespacing=1.35)
    ax.text(.05,.286,"Inherited coil binding from 'MFE Power Plant':",fontsize=10.5,color=MUTED,va='top')
    ax.text(.05,.259,':>> R0 = plasma.R {}',family='DejaVu Sans Mono',fontsize=11.5,va='top')

    box(ax,.56,.20,.415,.335,'CALCULATION USAGE — selects those values',color=BLUE,fontsize=11)
    usage=("calc field_calc : 'Coil Set Axis Field' {\n"
           "    in n_coils = coil.n_coils;\n"
           "    in I_coil = coil.I_coil;\n"
           "    in k_link = coil.k_link;\n"
           "    in R0 = coil.R0;\n"
           "}")
    ax.text(.585,.464,usage,family='DejaVu Sans Mono',fontsize=10.4,va='top',linespacing=1.35)
    ax.text(.585,.326,"Owned by 'Magnet System'.\nmu0 and two_pi retain their defaults.",fontsize=10.8,va='top',color=MUTED,linespacing=1.6)

    box(ax,.025,.025,.95,.10,"COMPONENT ATTRIBUTE — exposes the result inside 'Magnet System'",fontsize=12)
    ax.text(.05,.056,'attribute B : Real = field_calc.B_axis;',family='DejaVu Sans Mono',fontsize=11.8,va='top')
    arrow(ax,(.77,.592),(.77,.552),BLUE)
    arrow(ax,(.505,.39),(.545,.39),TEAL)
    arrow(ax,(.77,.182),(.77,.142),BLUE)
    save(fig,'stellarator-component')



def calculation_graph():
    data=json.loads((HERE/'graph-evidence.json').read_text())
    labels={
        'radial_build':'Radial build\nCoil position', 'field_calc':'Axis field',
        'coil_length':'Coil length', 'peak_field_calc':'Peak conductor\nfield',
        'current_sizing':'Current-driven\npack sizing', 'wp_sizing':'Winding-pack\nside length',
        'wp_fit':'Pack / casing\nfit margins', 'wp_volume':'Winding-pack\nvolume',
        'material_inventory':'Material\ninventory', 'winding_procurement':'Winding quantities\nand cost',
        'conductor_current':'Conductor\ncurrent margin', 'peak_field_ok':'CHECK\nField limit',
        'reference_conductor_current_ok':'CHECK\nCurrent margin', 'wp_fit_ok':'CHECK\nPack fits casing'}
    lines=['digraph G {', 'graph [rankdir=TB, bgcolor="#f7f9fc", pad="0.3", nodesep="0.5", ranksep="0.48", splines=polyline, fontname="DejaVu Sans", fontsize=23, fontcolor="#152b40", labelloc=t, label="How magnet calculations depend on one another\n "];',
        'node [shape=box, style="rounded,filled", fillcolor="white", color="#2463a5", fontcolor="#152b40", fontname="DejaVu Sans", fontsize=17, margin="0.2,0.12", penwidth=1.3];',
        'edge [color="#708498", arrowsize=0.75, penwidth=1.3];']
    for n in data['nodes']:
        color=GOLD if n['kind']=='constraint' else TEAL if n['id']=='winding_procurement' else BLUE
        fill='#fff4e7' if n['kind']=='constraint' else '#e8f5f2' if n['id']=='winding_procurement' else 'white'
        lines.append(f'{n["id"]} [label={json.dumps(labels[n["id"]])},color="{color}",fillcolor="{fill}"];')
    pairs=set()
    for e in data['edges']:
        assert e['collapsed'] is False
        pair=e['source'],e['target']
        if pair not in pairs:
            attrs = ' [label="Tape + conductor lengths", fontname="DejaVu Sans", fontsize=11, fontcolor="#52677a"]' if pair == ('winding_procurement', 'conductor_current') else ''
            lines.append(f'{pair[0]} -> {pair[1]}{attrs};'); pairs.add(pair)
    lines.extend(['{rank=same; radial_build; field_calc;}',
                  '{rank=same; wp_fit; wp_volume;}',
                  'legend [shape=plaintext, fontsize=12, fontcolor="#52677a", label="Each arrow is an actual output-to-input binding.\nSecondary inputs and other plant branches are omitted.\nAmber boxes assess values; they do not resize the design."];',
                  'reference_conductor_current_ok -> legend [style=invis];', '}'])
    dot=HERE/'stellarator-calculation-graph.dot'; dot.write_text('\n'.join(lines)+'\n')
    for fmt in ['png','svg']:
        subprocess.run(['dot',f'-T{fmt}','-Gdpi=160',str(dot),'-o',str(HERE/f'stellarator-calculation-graph.{fmt}')],check=True)


def feasibility():
    rows=list(csv.DictReader((HERE/'feasibility-cost-map.csv').open()))
    assert len(rows)==256
    passed=[r for r in rows if r['classification']=='pass']
    failed=[r for r in rows if r['classification']=='fail']
    invalid=[r for r in rows if r['classification']=='invalid-account']
    assert (len(passed),len(failed),len(invalid))==(44,210,2)
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(14.7,7.6))
    fig.subplots_adjust(top=.76,bottom=.25,left=.065,right=.925,wspace=.22)
    fig.text(.065,.947,'Which sampled designs pass—and what do they cost?',fontsize=23,weight='bold')
    fig.text(.065,.895,'17 September model snapshot • 256 evaluations at fixed settings for the other parameters',fontsize=12.5,color=MUTED)
    for ax in [ax1,ax2]:
        ax.set_facecolor('white'); ax.grid(True,color='#e8edf3',lw=.7); ax.set_axisbelow(True)
        ax.spines[['top','right']].set_visible(False)
        ax.spines[['bottom','left']].set_color('#b3beca')
        ax.set_xlabel('Major radius (m)',labelpad=10)
        ax.set_xlim(10.43,12.23); ax.set_ylim(11.945,13.25)
    ax1.set_ylabel('Coil ampere-turns (MA-turn)',labelpad=10)
    ax1.set_title('Feasibility under the 20 modeled screens',loc='left',pad=18,fontsize=13,weight='bold')
    ax2.set_title('Cost of electricity at the same points',loc='left',pad=18,fontsize=13,weight='bold')
    xy=lambda rs,k:[float(r[k]) for r in rs]
    ax1.scatter(xy(failed,'R_m'),xy(failed,'current_MAturn'),s=30,c='#b3bdca',marker='x',linewidths=1.15,zorder=2)
    ax1.scatter(xy(passed,'R_m'),xy(passed,'current_MAturn'),s=43,c=TEAL,edgecolors='white',linewidths=.55,zorder=3)
    ax1.scatter(xy(invalid,'R_m'),xy(invalid,'current_MAturn'),s=67,facecolors='none',edgecolors=GOLD,marker='D',linewidths=1.6,zorder=4)
    norm=matplotlib.colors.Normalize(vmin=149,vmax=160)
    cmap=matplotlib.colormaps['viridis']
    ax2.scatter(xy(failed,'R_m'),xy(failed,'current_MAturn'),c=xy(failed,'LCOE_dollars_MWh'),cmap=cmap,norm=norm,s=32,marker='x',linewidths=1.5,zorder=2)
    im=ax2.scatter(xy(passed,'R_m'),xy(passed,'current_MAturn'),c=xy(passed,'LCOE_dollars_MWh'),cmap=cmap,norm=norm,s=51,edgecolors=INK,linewidths=.8,zorder=3)
    ax2.scatter(xy(invalid,'R_m'),xy(invalid,'current_MAturn'),s=67,facecolors='none',edgecolors=GOLD,marker='D',linewidths=1.6,zorder=4)
    cax=fig.add_axes([.943,.25,.014,.51]); cb=fig.colorbar(im,cax=cax); cb.set_label('Conditional LCOE ($/MWh)',labelpad=9); cb.outline.set_visible(False)
    handles=[Line2D([],[],marker='o',color='none',markerfacecolor=TEAL,markeredgecolor=TEAL,label='44 pass all screens'),
             Line2D([],[],marker='x',color='#a0acbb',linestyle='none',label='210 fail ≥1 screen'),
             Line2D([],[],marker='D',color=GOLD,markerfacecolor='none',linestyle='none',label='2 invalid power accounts')]
    fig.legend(handles=handles,loc='lower left',bbox_to_anchor=(.065,.115),frameon=False,ncol=3,fontsize=12,handletextpad=.45,columnspacing=1.65)
    fig.text(.065,.095,'Cost panel: outlined circles pass; crosses fail. Invalid power accounts are shown without a cost color.',fontsize=10.5,color=MUTED)
    fig.text(.065,.043,'Each mark is an evaluated case, not an interpolated feasible region. Historical, incomplete cost scope; later model revisions add costs and checks.',fontsize=10.5,color=MUTED)
    save(fig,'stellarator-feasibility-cost')


def comparison():
    rows=list(csv.DictReader((HERE/'magnet-sizing-comparison.csv').open()))
    fig,ax=plt.subplots(figsize=(14,7.1)); ax.set(xlim=(0,1),ylim=(0,1)); ax.axis('off')
    ax.text(.025,.96,'A design change can fix one limit and expose another',fontsize=22,weight='bold')
    ax.text(.025,.893,'Three matched cases • 15 September magnet-sizing study • same 12.7 m major radius and 15.4 MA-turn',fontsize=12,color=MUTED)
    titles=['Original inventory','Size for required current','Add casing space']
    subs=['Original casing allocation','1% physical inventory reserve','Keep current-based sizing']
    for i,r in enumerate(rows):
        x=.025+i*.329; w=.29
        box(ax,x,.25,w,.55,titles[i],color=BLUE,fontsize=13)
        ax.text(x+.024,.672,subs[i],fontsize=11,color=MUTED)
        ax.text(x+.024,.58,f'${float(r["LCOE_dollars_MWh"]):.2f}/MWh',fontsize=25,weight='bold')
        ax.text(x+.024,.52,'Conditional electricity cost',fontsize=10.5,color=MUTED)
        for j,(key,label) in enumerate([('current_status','Conductor current'),('fit_status','Pack / casing fit'),('field_status','Peak field limit')]):
            ok=r[key]=='satisfied'; y=.445-j*.065
            ax.text(x+.024,y,label,fontsize=11.5)
            ax.text(x+w-.023,y,'PASS' if ok else 'FAIL',ha='right',fontsize=11.5,weight='bold',color=TEAL if ok else GOLD)
        if i<2: arrow(ax,(x+w+.004,.56),(x+.329-.012,.56))
    ax.text(.025,.163,'All three fail the full plant check; the divertor heat-load limit remains violated in every case.',fontsize=12.5,weight='bold')
    ax.text(.025,.094,'Added conductor raises material demand and pack size. More allocated space clears fit; the radial change raises peak field.',fontsize=11.5,color=MUTED)
    ax.text(.025,.035,'Historical model costs, not current price estimates. The comparisons retain the study’s declared physical and cost assumptions.',fontsize=10.5,color=MUTED)
    save(fig,'stellarator-magnet-tradeoff')


if __name__ == '__main__':
    overview()
    component()
    calculation_graph()
    feasibility()
    comparison()
