"""Shared figure style for the HTML write-ups in archive/write-up/.

Figures use the pages' fonts (Manrope and Fira Code, kept in fonts/) and the colors in write-up.css.
Draw each figure at the width it is shown, so its text keeps its point size on the page: a figure's plate is
the article's 64rem wide column less its padding, which is WIDE_IN inches at 96 px per inch. Save SVG with live text and embed it inline in the
page, so the browser draws the text with the page's own fonts.
"""
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONT_DIR = HERE / "fonts"

SANS = "Manrope"
MONO = "Fira Code"

# Colors from write-up.css. Figures sit on its --plate color.
INK = "#191919"
MUTED = "#5f5f5f"
RULE = "#d3cdc4"
EDGE = "#8a847b"
PLATE = "#fbfaf8"
ROLE_CALC = "#1b5f99"   # calculations and equations
ROLE_DATA = "#0b6f6a"   # values the plant supplies
ROLE_CHECK = "#95520f"  # checks and constraints
ROLE_CALC_FILL = "#ffffff"
ROLE_DATA_FILL = "#dcefed"
ROLE_CHECK_FILL = "#f6e9d8"

WIDE_IN = 10.2     # the widest a figure can be drawn, in inches
TEXT_PT = 10.5     # figure body text; about 14 px on the page
LABEL_PT = 9.0     # axis ticks, notes, legends; about 12 px
TITLE_PT = 12.0    # a figure's own title, when it has one; about 16 px


def use_matplotlib():
    """Register the write-up fonts with matplotlib and apply the shared defaults."""
    import matplotlib as mpl
    from matplotlib import font_manager

    for font in sorted(FONT_DIR.glob("*.ttf")):
        font_manager.fontManager.addfont(str(font))
    mpl.rcParams.update({
        "font.family": SANS,
        "font.monospace": [MONO],
        "font.size": TEXT_PT,
        "svg.fonttype": "none",
        "text.color": INK,
        "axes.labelcolor": INK,
        "axes.titlecolor": INK,
        "axes.edgecolor": RULE,
        "axes.titlesize": TEXT_PT,
        "axes.titleweight": "semibold",
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelsize": LABEL_PT,
        "ytick.labelsize": LABEL_PT,
        "legend.fontsize": LABEL_PT,
        "legend.frameon": False,
        "figure.facecolor": PLATE,
        "savefig.facecolor": PLATE,
    })


def graphviz_env():
    """Environment for running dot so that it finds the write-up fonts."""
    env = dict(os.environ)
    env["FONTCONFIG_FILE"] = str(FONT_DIR / "fonts.conf")
    return env
