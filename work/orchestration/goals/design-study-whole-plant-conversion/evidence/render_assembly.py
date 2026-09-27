"""Render the declared whole-plant comparison boundary; no model or accounting calculations."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = Path(__file__).resolve().parent
OUT = HERE / "figures"

def box(ax, xy, width, height, text, face, edge="#3b4854", size=10):
    patch = FancyBboxPatch(xy, width, height, boxstyle="round,pad=0.015",
                          linewidth=1.1, edgecolor=edge, facecolor=face)
    ax.add_patch(patch)
    ax.text(xy[0]+width/2, xy[1]+height/2, text, ha="center", va="center",
            fontsize=size, color="#202b33", linespacing=1.5)

def arrow(ax, start, end, text=None, color="#344d63", offset=(0,0)):
    ax.annotate("", xy=end, xytext=start,
                arrowprops={"arrowstyle":"-|>", "lw":1.6, "color":color})
    if text:
        ax.text((start[0]+end[0])/2+offset[0], (start[1]+end[1])/2+offset[1],
                text, ha="center", va="center", fontsize=9, color=color)

def render():
    OUT.mkdir(exist_ok=True)
    fig, axes = plt.subplots(1,2, figsize=(13,9), facecolor="#faf9f5")
    titles = ("Steam conversion", "Helium Brayton conversion")
    details = ("Intermediate exchangers + salt circuit\nSteam turbine, generator and pumps",
               "Helium exchangers + recuperator\nTurbine, compressors and generator")
    colors = ("#f4dfbd", "#c8e5dc")
    for ax,title,detail,color in zip(axes,titles,details,colors):
        ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
        ax.set_facecolor("#faf9f5")
        ax.text(.5,.96,title,ha="center",va="center",fontsize=17,weight="bold",color="#1e3342")
        boundary = FancyBboxPatch((.07,.16),.86,.72,boxstyle="round,pad=0.018",
                                 facecolor="none",edgecolor="#64757d",linestyle="--",linewidth=1.4)
        ax.add_patch(boundary)
        ax.text(.5,.885,"WHOLE-PLANT POWER AND COST BOUNDARY",ha="center",fontsize=9,color="#546772",bbox={"facecolor":"#faf9f5","edgecolor":"none","pad":3})
        box(ax,(.18,.72),.64,.12,"Common reactor offer\nCore, magnets, fuel, heating\nand auxiliary cooling","#dce6ef")
        arrow(ax,(.5,.72),(.5,.665),"Supplied source heat",offset=(.23,0))
        box(ax,(.18,.57),.64,.09,"Common primary helium loop\nCirculators, piping and initial stock","#dce6ef")
        arrow(ax,(.5,.57),(.5,.515),"Heat + recovered pumping work",offset=(.20,0))
        box(ax,(.18,.40),.64,.11,detail,color)
        arrow(ax,(.5,.40),(.5,.345),"Generated electricity",offset=(.23,0))
        box(ax,(.18,.25),.64,.09,"Electrical balance\nSubtract conversion and upstream loads","#ffffff")
        arrow(ax,(.5,.25),(.5,.09),"Net electricity exported",offset=(.24,0))
        ax.plot([.18,.105,.105,.18],[.285,.285,.76,.76],color="#b85b47",lw=1.4)
        arrow(ax,(.105,.76),(.18,.76),color="#b85b47")
        arrow(ax,(.105,.615),(.18,.615),color="#b85b47")
        ax.text(.09,.51,"Upstream electricity",rotation=90,ha="right",va="center",fontsize=9,color="#b85b47")
        ax.plot([.82,.875,.875],[.455,.455,.20],color="#91764b",lw=1.2)
        arrow(ax,(.875,.20),(.875,.12),color="#91764b")
        ax.text(.88,.39,"Conversion heat rejection",rotation=90,ha="left",va="center",fontsize=9,color="#91764b")
    fig.text(.5,.025,"Same reactor and source within each pair. Conversion equipment changes.\nPrimary pumping heat is recovered once; its electrical demand is subtracted once.\nCosts include capital, financing, operation, fuel, replacements and terminal costs.",
             ha="center",fontsize=10,color="#344d63",linespacing=1.5)
    fig.subplots_adjust(left=.015,right=.985,top=.98,bottom=.10,wspace=.12)
    for suffix in ("svg","png"):
        fig.savefig(OUT/f"assembly-comparison.{suffix}",dpi=180,facecolor=fig.get_facecolor())
    plt.close(fig)
if __name__ == "__main__":
    render()
