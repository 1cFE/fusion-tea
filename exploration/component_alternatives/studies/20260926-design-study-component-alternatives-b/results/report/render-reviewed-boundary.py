"""Reproduce the reviewed fourth-submission comparison boundary (no numerical result)."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE=Path(__file__).resolve().parent
fig,ax=plt.subplots(figsize=(12,6.2))
ax.set_xlim(0,12);ax.set_ylim(0,6.2);ax.axis('off')
colors={'common':'#e9edf3','steam':'#dceff6','gas':'#fce8d5'}
def box(x,y,w,h,text,color):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.07',facecolor=colors[color],edgecolor='#344054',linewidth=1))
    ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=10,color='#17212b')
def arrow(a,b):
    ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','color':'#344054','lw':1.4})
ax.text(.15,5.88,'Selected steam offer versus tested helium Brayton offers',fontsize=16,weight='bold')
ax.text(.15,5.48,'Reviewed assembly design • conversion-subsystem cost per net MWh',fontsize=10,color='#475467')
box(.2,2.45,2.25,1.35,'Existing primary-loop model\nSame duty, hot/return\nand flow within each pair','common')
box(3.1,3.75,2.35,.85,'Bypass + helium–salt HX\nSalt pumps and inventory','steam')
box(6,3.75,2.25,.85,'Steam generator / reheat\nTurbines and generator','steam')
box(8.85,3.75,2.65,.85,'Condenser and water system\nCooling electricity counted','steam')
box(3.1,1.6,2.35,.85,'Bypass + primary–cycle HX\nMatched return and duty','gas')
box(6,1.6,2.25,.85,'Compressors / finite-UA recup.\nTurbine and generator','gas')
box(8.85,1.6,2.65,.85,'Three finite-UA gas coolers\nWater pumps + loss service','gas')
for a,b in [((2.45,3.45),(3.1,4.17)),((2.45,2.75),(3.1,2.02)),((5.45,4.17),(6,4.17)),((8.25,4.17),(8.85,4.17)),((5.45,2.02),(6,2.02)),((8.25,2.02),(8.85,2.02))]: arrow(a,b)
ax.plot([2.78,2.78],[1.12,4.97],ls='--',color='#667085',lw=1.2)
ax.text(2.9,4.9,'Compared conversion equipment and its costs →',fontsize=10,color='#344054')
ax.text(.2,.73,'Upstream reactor, fuel and primary circulation are excluded equally from the subsystem metric.',fontsize=10,color='#344054')
ax.text(.2,.32,'Source resistance, machine performance, equipment quotes and detailed loss cooling remain declared assumptions.',fontsize=9,color='#667085')
fig.tight_layout()
fig.savefig(HERE/'reviewed-comparison-boundary.svg',bbox_inches='tight')
fig.savefig(HERE/'reviewed-comparison-boundary.png',dpi=240,bbox_inches='tight')
svg = HERE / 'reviewed-comparison-boundary.svg'
svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n')
