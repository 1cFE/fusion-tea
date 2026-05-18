"""One-off 3D clustering analysis of fusion concepts.

Three axes:
- Technical Maturity = geo_mean(C7, C8)
- Low-Cost Potential = geo_mean(C1, C3, C4, C5, C6)
- Time to Market    = TRL-anchored years modulated by cadence, fuel, funding

Run with:
    uv run --with plotly --with scikit-learn python exploration/concept_analysis/scripts/oneoff_3d_clustering.py

Output:
    exploration/concept_analysis/oneoff_3d_clustering.html
    exploration/concept_analysis/oneoff_3d_clustering.csv

This file is intentionally standalone. Delete the .py / .html / .csv outputs
to wipe — no other code depends on it.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sklearn.cluster import KMeans

ROOT = Path(__file__).resolve().parent.parent
SCORES_DIR = ROOT / "scores"
TABLE_PATH = ROOT / "table.csv"
OUT_HTML = ROOT / "oneoff_3d_clustering.html"
OUT_CSV = ROOT / "oneoff_3d_clustering.csv"


# ---------------------------------------------------------------------------
# Funding data (best public estimates as of ~2026; rough order-of-magnitude only)
# ---------------------------------------------------------------------------
# Source: FIA Global Fusion Industry reports + public press releases. These are
# point estimates for total cumulative private capital raised through ~2026.
# For unfunded / academic / government-only projects, use $1M as a placeholder.
FUNDING_M_USD: dict[str, float] = {
    "01-hts-compact-tokamak": 2000,        # CFS (~$2B+)
    "02-acoustic-icf-sonofusion": 5,       # Sonofusion Energy — small
    "03-laser-icf-liquid-jet-target": 5,   # Cortex — small
    "04-laser-icf": 5,                     # HB11 (Australian)
    "05-planar-coil-stellarator": 30,      # Thea Energy
    "06-magnetic-mirror": 3,               # Pale Blue Fusion — small
    "07-maglif": 50,                       # Sandia/DOE-adjacent (gov programs)
    "08-frc-w-direct-conversion": 1000,    # Helion (~$577M+ since 2024 raises)
    "09-qi-stellarator-hts": 30,           # Proxima Fusion (~€30M)
    "10-large-scale-stellarator": 20,      # Gauss Fusion
    "11-magnetic-mirror": 36,              # Realta
    "12-levitated-dipole": 12,             # OpenStar Technologies (NZ$10M+)
    "13-electrostatic-hybrid": 40,         # Avalanche Energy
    "14-magnetized-target-fusion-pneumatic-compression": 350,  # General Fusion
    "15-sheared-flow-stabilized-z-pinch": 240,  # Zap Energy
    "16-muon-catalyzed-fusion": 24,        # Acceleron Fusion
    "17a-laser-icf-hybrid-drive": 100,     # Xcimer Energy
    "17b-laser-icf-fast-ignition": 15,     # Focused Energy
    "18-p-b11-frc": 1200,                  # TAE Technologies
    "19-orbital-levitated-dipole": 5,      # Zephyr / orbital LD — small/conceptual
    "20a-type-one-stellarator": 80,        # Type One Energy
    "20b-renaissance-stellarator": 18,     # Renaissance Fusion
    "21-spherical-tokamak-hts": 250,       # Tokamak Energy
    "22-projectile-icf": 90,               # First Light Fusion (note: defunct 2025)
    "23-laser-icf-nanostructured-target": 30,  # Marvel Fusion
    "24-dense-plasma-focus": 3,            # LPP Fusion
    "25-heavy-ion-beam-icf": 10,           # HIF concept (gov-adjacent / small)
    "26-laser-icf-indirect-drive": 50,     # Inertia Enterprises
    "27-polywell": 3,                      # EMC2 / polywell — defunct/small
    "28-hts-tokamak-full-hts": 30,         # Energy Singularity (~$30M)
    "29-negative-triangularity-tokamak": 50,  # Firefly / TBD
    "30-laser-icf-nif-commercialization": 50,  # Inertia / NIF commercial
    "31-laser-icf-oec-architecture": 25,   # Blue Laser Fusion
    "32-laser-icf-french-national": 10,    # GenF
    "33-state-backed-tokamak-best": 100,   # BEST (China state-backed)
    "34-compact-spherical-tokamak-india": 20,  # Pranos / India (no longer in v3 table)
    "35-polomac-magnetic-confinement": 1,  # Polomac — tiny/research
    "36-helical-coil-stellarator": 10,     # Helical Fusion (Japan)
    "37-magnetized-target-inertial-fusion-mtif": 5,  # NearStar — early stage
    "38-particle-accelerator-driven-fusion": 5,  # SHINE Technologies-adjacent
    "39-spherical-tokamak-cs-free-p-b11": 5,  # ENN p-B11 program (small public estimate)
}


# ---------------------------------------------------------------------------
# Cadence factor by architecture columns
# ---------------------------------------------------------------------------
#
# Mirrors lib/scoring.py:detect_c2_category — keep column reads and slug
# overrides in sync. Derives the cadence multiplier from Confinement Family /
# MFE Topology / IFE Driver / MIF Method / Non-Standard Mechanism so the
# lookup survives concept-ID renumbering.

# Slug overrides for cases where architecture columns alone are insufficient:
_CADENCE_SLUG_OVERRIDES: dict[str, float] = {
    # Orbital levitated dipole — much slower iteration than a ground LD
    "19-orbital-levitated-dipole": 1.30,
    # Z-pinch shares Open/Linear topology but iterates like compact pulsed MFE
    "15-sheared-flow-stabilized-z-pinch": 0.70,
}


def cadence_by_architecture(concept_id: str, info: dict[str, str]) -> float:
    """Return the cadence multiplier for a concept from its architecture row.

    Mirrors lib/scoring.py:detect_c2_category pattern; see module-level note.
    """
    if concept_id in _CADENCE_SLUG_OVERRIDES:
        return _CADENCE_SLUG_OVERRIDES[concept_id]

    family = info.get("Confinement Family", "").strip()
    topology = info.get("MFE Topology", "").strip()
    mif_method = info.get("MIF Method", "").strip()
    driver = info.get("IFE Driver", "").strip()
    mechanism = info.get("Non-Standard Mechanism", "").strip()
    tokamak_shape = info.get("Tokamak Shape", "").strip()

    if family == "MFE":
        if topology == "Tokamak":
            # Compact / spherical / negative-triangularity iterate faster than
            # standard conventional tokamaks.
            if tokamak_shape in ("Compact", "Spherical", "Negative triangularity"):
                return 1.10
            return 1.20
        if topology == "Stellarator":
            return 1.30
        if topology == "Compact Toroid":
            return 0.75
        if topology == "Open/Linear":
            return 1.00  # mirrors; Z-pinch handled via slug override above
        if topology == "Dipole":
            return 1.00  # ground levitated dipole
        return 1.50  # exotic MFE — slow

    if family == "IFE":
        if driver == "Laser":
            return 0.85
        if driver in ("Heavy ion beam", "Projectile"):
            return 0.90 if driver == "Heavy ion beam" else 0.70
        if driver == "Acoustic":
            return 1.50  # sonofusion — exotic
        return 1.40

    if family == "MIF":
        if mif_method == "FRC compression":
            return 0.75
        return 0.70  # magnetized-target / pulsed-power MIF

    # Non-Standard family
    if mechanism == "Electrostatic":
        return 1.40
    if mechanism == "Muon-catalyzed":
        return 1.50
    if mechanism == "Plasma focus":
        return 0.70
    return 1.50  # default exotic


# ---------------------------------------------------------------------------
# Fuel difficulty
# ---------------------------------------------------------------------------
FUEL_FACTOR: dict[str, float] = {
    "D-T": 1.00,
    "D-D": 1.25,
    "D-He3": 1.50,
    "p-B11": 1.90,
    "muon-D-T": 1.40,  # special-cased below
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def geo_mean(values: list[float]) -> float:
    """Geometric mean. Assumes all values > 0."""
    return math.exp(sum(math.log(v) for v in values) / len(values))


def base_years(tech_maturity: float) -> float:
    """TRL-anchored years remaining. tech_maturity in [1, 5]."""
    return 50.0 - 9.0 * tech_maturity


def ttm_score(ttm_years: float) -> float:
    """Convert TTM in years to a 1-5 score where 5 = soonest, 1 = furthest.

    Anchored at fixed thresholds so the score is stable across re-runs:
        5 years  -> score 5.0  (commercial within ~5 years)
        100 years -> score 1.0  (effectively never)
    Linear interpolation between, clamped to [1, 5].
    """
    score = 1.0 + 4.0 * (100.0 - ttm_years) / (100.0 - 5.0)
    return max(1.0, min(5.0, score))


def funding_factor(funding_m_usd: float) -> float:
    """Log-scaled funding boost. $10M→1.0; $100M→1.25; $1B→1.5; $10B→1.75."""
    if funding_m_usd <= 0.1:
        return 0.5  # ~no funding floor
    raw = 0.6 + 0.25 * math.log10(funding_m_usd / 10.0)
    return max(0.5, min(2.0, raw))


def fuel_factor_for(concept_id: str, fuel: str) -> float:
    """Look up the fuel factor, handling muon-CF as a special case."""
    if concept_id == "16-muon-catalyzed-fusion":
        return FUEL_FACTOR["muon-D-T"]
    return FUEL_FACTOR.get(fuel.strip(), 1.5)  # default for unknown / exotic


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

def load_concepts() -> dict[str, dict]:
    """Load table.csv into {id: row_dict}."""
    out = {}
    with open(TABLE_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["ID"]] = row
    return out


def load_calibrated_scores() -> list[dict]:
    return json.loads((SCORES_DIR / "calibrated_scores.json").read_text(encoding="utf-8"))["scores"]


# ---------------------------------------------------------------------------
# Build per-concept axes
# ---------------------------------------------------------------------------

def build_dataset() -> list[dict]:
    concepts = load_concepts()
    scores = load_calibrated_scores()

    rows = []
    for s in scores:
        cid = s["concept_id"]
        info = concepts.get(cid, {})
        company = info.get("Company", "")
        fuel = info.get("Fuel", "")
        family = info.get("Confinement Family", "")

        # Tech maturity = geo mean of C7, C8
        tm = geo_mean([s["C7"], s["C8"]])
        # Low-cost potential = geo mean of C1, C3, C4, C5, C6
        lcp = geo_mean([s["C1"], s["C3"], s["C4"], s["C5"], s["C6"]])

        # TTM components — cadence derived from architecture columns
        cadence = cadence_by_architecture(cid, info)
        ff = fuel_factor_for(cid, fuel)
        funding = FUNDING_M_USD.get(cid, 1.0)
        funding_boost = funding_factor(funding)

        ttm_y = base_years(tm) * cadence * ff / funding_boost
        ttm = ttm_score(ttm_y)

        rows.append({
            "concept_id": cid,
            "company": company,
            "fuel": fuel,
            "family": family,
            "C1": s["C1"], "C2": s["C2"], "C3": s["C3"], "C4": s["C4"],
            "C5": s["C5"], "C6": s["C6"], "C7": s["C7"], "C8": s["C8"],
            "tech_maturity": round(tm, 3),
            "low_cost_potential": round(lcp, 3),
            "time_to_market": round(ttm, 3),
            "ttm_years_internal": round(ttm_y, 1),  # kept for audit; not shown in plot
            "funding_M_usd": funding,
            "cadence_factor": cadence,
            "fuel_factor": ff,
            "funding_factor": round(funding_boost, 3),
        })
    return rows


# ---------------------------------------------------------------------------
# Clustering
# ---------------------------------------------------------------------------

def cluster_concepts(rows: list[dict], k: int = 4) -> list[int]:
    """K-means clustering on (TM, LCP, TTM) — all on 1-5 scale, no standardization needed."""
    X = np.array([[r["tech_maturity"], r["low_cost_potential"], r["time_to_market"]] for r in rows])
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    return km.fit_predict(X).tolist()


# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------

def render_plot(rows: list[dict], cluster_labels: list[int]) -> None:
    palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

    # Axis assignment (3D plotly: Z is vertical):
    #   X = Tech Maturity
    #   Y = Time to Market
    #   Z = Low-Cost Potential   (vertical)
    fig = go.Figure()

    # --- Drop-lines + floor shadows ---
    # Drop-lines go from each point down to the floor (Z=1, i.e. LCP=1),
    # so the (Tech Maturity, Time to Market) projection is read off the floor.
    drop_x, drop_y, drop_z = [], [], []
    shadow_x, shadow_y = [], []
    for r in rows:
        drop_x.extend([r["tech_maturity"], r["tech_maturity"], None])
        drop_y.extend([r["time_to_market"], r["time_to_market"], None])
        drop_z.extend([r["low_cost_potential"], 1, None])
        shadow_x.append(r["tech_maturity"])
        shadow_y.append(r["time_to_market"])

    fig.add_trace(go.Scatter3d(
        x=drop_x, y=drop_y, z=drop_z,
        mode="lines",
        line=dict(color="rgba(120,120,120,0.35)", width=1),
        hoverinfo="skip", showlegend=False, name="drop-lines",
    ))
    fig.add_trace(go.Scatter3d(
        x=shadow_x, y=shadow_y, z=[1] * len(shadow_x),
        mode="markers",
        marker=dict(size=4, color="rgba(120,120,120,0.45)", symbol="circle"),
        hoverinfo="skip", showlegend=False, name="floor-shadows",
    ))

    # --- Cluster traces ---
    n_clusters = max(cluster_labels) + 1
    for k in range(n_clusters):
        idxs = [i for i, c in enumerate(cluster_labels) if c == k]
        cluster_rows = [rows[i] for i in idxs]
        color = palette[k % len(palette)]
        labels = [r["concept_id"].split("-", 1)[0] for r in cluster_rows]
        customdata = [
            [r["concept_id"], r["company"], r["fuel"], r["family"],
             r["C1"], r["C7"], r["C8"]]
            for r in cluster_rows
        ]
        fig.add_trace(go.Scatter3d(
            x=[r["tech_maturity"] for r in cluster_rows],
            y=[r["time_to_market"] for r in cluster_rows],
            z=[r["low_cost_potential"] for r in cluster_rows],
            mode="markers+text",
            marker=dict(size=7, color=color, opacity=0.9,
                        line=dict(color="#222", width=0.5)),
            text=labels, textposition="top center",
            textfont=dict(size=9),
            name=f"Cluster {k}",
            customdata=customdata,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "%{customdata[1]} — %{customdata[2]} — %{customdata[3]}<br><br>"
                "Tech Maturity: %{x:.2f}<br>"
                "Time to Market: %{y:.2f}<br>"
                "Low-Cost Potential: %{z:.2f}<br><br>"
                "C1=%{customdata[4]:.1f}  C7=%{customdata[5]:.1f}  "
                "C8=%{customdata[6]:.1f}<extra></extra>"
            ),
        ))

    axis_kwargs = dict(range=[1, 5], dtick=1)
    fig.update_layout(
        title="Fusion Concepts — 3D Clustering",
        scene=dict(
            xaxis=dict(title="Tech Maturity (5 = most mature)", **axis_kwargs),
            yaxis=dict(title="Time to Market (5 = soonest)", **axis_kwargs),
            zaxis=dict(title="Low-Cost Potential (5 = lowest cost)", **axis_kwargs),
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.0)),
        ),
        annotations=[dict(
            text=("All axes on 1-5 scale (5 = best, 1 = worst). "
                  "Drag to rotate. Gray drop-lines & floor shadows show "
                  "the (Tech Maturity, Time to Market) projection."),
            xref="paper", yref="paper",
            x=0.5, y=-0.06, xanchor="center", yanchor="top",
            showarrow=False,
            font=dict(size=12, color="#555"),
        )],
        legend=dict(x=0.85, y=0.95),
        margin=dict(l=0, r=0, t=60, b=80),
        height=750,
    )
    fig.write_html(OUT_HTML, include_plotlyjs="cdn")


def write_csv(rows: list[dict], cluster_labels: list[int]) -> None:
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        fields = list(rows[0].keys()) + ["cluster"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r, c in zip(rows, cluster_labels):
            w.writerow({**r, "cluster": c})


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    rows = build_dataset()
    rows.sort(key=lambda r: -r["time_to_market"])  # best (5) first

    cluster_labels = cluster_concepts(rows, k=4)

    render_plot(rows, cluster_labels)
    write_csv(rows, cluster_labels)

    print(f"Concepts: {len(rows)}")
    print(f"Output:")
    print(f"  {OUT_HTML}")
    print(f"  {OUT_CSV}")
    print()
    print(f"{'concept':<48} {'TM':>5} {'LCP':>5} {'TTM':>5} {'cluster':>7}")
    print("-" * 80)
    for r, c in zip(rows, cluster_labels):
        print(f"{r['concept_id']:<48} {r['tech_maturity']:>5.2f} {r['low_cost_potential']:>5.2f} "
              f"{r['time_to_market']:>5.2f} {c:>7}")


if __name__ == "__main__":
    main()
