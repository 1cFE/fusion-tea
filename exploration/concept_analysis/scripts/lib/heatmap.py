"""Heatmap generation for calibrated LCOE Downselect scores.

Produces a standalone HTML file with:
1. Main heatmap (color-coded scores, ranked by geometric mean)
2. Filter note (C7 x C8 < 2.0 threshold)
3. Per-criterion rankings
4. LCOE vs qualitative comparison
5. Calibration adjustments table
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path


def compute_geometric_mean(scores: dict) -> float:
    """Compute geometric mean of C1-C8: (C1 * C2 * ... * C8)^(1/8)."""
    keys = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"]
    product = 1.0
    for k in keys:
        product *= scores[k]
    return product ** (1.0 / 8)


def apply_filter(scores: list[dict]) -> tuple[list[dict], list[dict]]:
    """Split concepts into ranked and filtered based on C7 x C8 threshold.

    Filter: C7 * C8 < 2.0 -> grayed out and unranked.

    Returns (ranked, filtered) where ranked is sorted by geometric mean descending.
    """
    ranked = []
    filtered = []
    for s in scores:
        s["geometric_mean"] = compute_geometric_mean(s)
        s["c7_c8_product"] = s["C7"] * s["C8"]
        if s["c7_c8_product"] < 2.0:
            filtered.append(s)
        else:
            ranked.append(s)

    ranked.sort(key=lambda x: x["geometric_mean"], reverse=True)
    return ranked, filtered


def _score_color(value: float) -> str:
    """Map a 1-5 score to an HSL color string.

    1.0 = red, 3.0 = yellow, 5.0 = green
    """
    # Clamp to [1, 5]
    v = max(1.0, min(5.0, value))
    # Map to hue: 1->0 (red), 3->60 (yellow), 5->120 (green)
    hue = (v - 1.0) * 30.0  # 0 to 120
    return f"hsl({hue:.0f}, 70%, 85%)"


def _read_lcoe_from_model(analyses_dir: Path, concept_id: str) -> str:
    """Try to read LCOE value from model_output.txt for a concept."""
    output_path = analyses_dir / concept_id / "model_output.txt"
    if not output_path.exists():
        return "N/A"
    try:
        text = output_path.read_text(encoding="utf-8")
        # Look for LCOE pattern
        m = re.search(r"LCOE[:\s]+([\d.]+)\s*\$/MWh", text)
        if m:
            return f"${m.group(1)}/MWh"
        m = re.search(r"lcoe[:\s]+([\d.]+)", text, re.IGNORECASE)
        if m:
            return f"${m.group(1)}/MWh"
    except Exception:
        pass
    return "N/A"


def generate_heatmap_html(
    calibrated_scores: list[dict],
    adjustments: list[dict],
    output_path: Path,
    analyses_dir: Path | None = None,
    concepts: list[dict] | None = None,
) -> None:
    """Generate a standalone HTML heatmap from calibrated scores.

    Sections:
    1. Main heatmap (ranked by geometric mean)
    2. Filter note
    3. Per-criterion rankings
    4. LCOE vs qualitative comparison
    5. Calibration adjustments table
    """
    ranked, filtered = apply_filter(calibrated_scores)

    # Build concept_id -> "concept_id (Company)" label lookup.
    company_by_id: dict[str, str] = {}
    if concepts:
        for c in concepts:
            company_by_id[c.get("_id", "")] = c.get("Company", "") or ""

    def _label(cid: str) -> str:
        company = company_by_id.get(cid, "")
        return f"{cid} ({company})" if company else cid

    criteria = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"]
    criteria_names = {
        "C1": "Modularization",
        "C2": "Scalability",
        "C3": "Supply Chain Learning",
        "C4": "Plant Complexity",
        "C5": "Customization Needs",
        "C6": "Upper Capacity Factor",
        "C7": "Technical Risk Evidence",
        "C8": "Data Adequacy",
    }

    # Build HTML
    html_parts = []
    html_parts.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Fusion TEA — LCOE Downselect Heatmap</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
         margin: 2rem; background: #fafafa; color: #222; }
  h1 { margin-bottom: 0.5rem; }
  h2 { margin-top: 2rem; border-bottom: 2px solid #ddd; padding-bottom: 0.3rem; }
  table { border-collapse: collapse; margin: 1rem 0; width: 100%; }
  th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: center; font-size: 0.9rem; }
  th { background: #f0f0f0; font-weight: 600; }
  td.concept { text-align: left; font-weight: 500; white-space: nowrap; }
  td.composite { font-weight: 700; }
  tr.filtered { opacity: 0.45; }
  .filter-note { background: #fff3cd; border: 1px solid #ffc107; padding: 0.8rem;
                  border-radius: 4px; margin: 1rem 0; }
  .meta { color: #666; font-size: 0.85rem; margin-bottom: 2rem; }
  .adjustment-table td { text-align: left; font-size: 0.85rem; }
</style>
</head>
<body>
<h1>Fusion TEA — LCOE Downselect Heatmap</h1>
<p class="meta">Scores 1-5 (5 = most favorable). Ranked by geometric mean of C1-C8.
Composite = (C1 &times; C2 &times; &hellip; &times; C8)<sup>1/8</sup></p>
""")

    # --- Section 1: Main heatmap ---
    html_parts.append("<h2>1. Concept Rankings</h2>")
    html_parts.append("<table>")
    html_parts.append("<tr><th>Rank</th><th>Concept</th>")
    for c in criteria:
        html_parts.append(f"<th title='{criteria_names[c]}'>{c}</th>")
    html_parts.append("<th>Composite</th></tr>")

    for rank, s in enumerate(ranked, 1):
        html_parts.append(f"<tr><td>{rank}</td><td class='concept'>{_label(s['concept_id'])}</td>")
        for c in criteria:
            color = _score_color(s[c])
            html_parts.append(f"<td style='background:{color}'>{s[c]:.1f}</td>")
        html_parts.append(f"<td class='composite'>{s['geometric_mean']:.2f}</td></tr>")

    for s in filtered:
        html_parts.append(f"<tr class='filtered'><td>—</td><td class='concept'>{_label(s['concept_id'])}</td>")
        for c in criteria:
            html_parts.append(f"<td>{s[c]:.1f}</td>")
        html_parts.append(f"<td class='composite'>{s['geometric_mean']:.2f}</td></tr>")

    html_parts.append("</table>")

    # --- Section 2: Filter note ---
    html_parts.append("<h2>2. Filter</h2>")
    html_parts.append(f"""<div class="filter-note">
<strong>Filter threshold:</strong> C7 &times; C8 &lt; 2.0<br>
<strong>{len(filtered)}</strong> concept(s) filtered (grayed out, unranked).
<strong>{len(ranked)}</strong> concept(s) ranked.
</div>""")

    # --- Section 3: Per-criterion rankings ---
    html_parts.append("<h2>3. Per-Criterion Rankings</h2>")
    html_parts.append("<table>")
    html_parts.append("<tr>")
    for c in criteria:
        html_parts.append(f"<th>{c}: {criteria_names[c]}</th>")
    html_parts.append("</tr>")

    # Sort ranked concepts by each criterion
    per_crit = {}
    for c in criteria:
        per_crit[c] = sorted(ranked, key=lambda x: x[c], reverse=True)

    max_rows = len(ranked) if ranked else 0
    for i in range(max_rows):
        html_parts.append("<tr>")
        for c in criteria:
            if i < len(per_crit[c]):
                s = per_crit[c][i]
                color = _score_color(s[c])
                html_parts.append(
                    f"<td style='background:{color};text-align:left'>"
                    f"{_label(s['concept_id'])} ({s[c]:.1f})</td>"
                )
            else:
                html_parts.append("<td></td>")
        html_parts.append("</tr>")
    html_parts.append("</table>")

    # --- Section 4: LCOE vs qualitative comparison ---
    html_parts.append("<h2>4. LCOE vs Qualitative Ranking</h2>")
    if analyses_dir:
        html_parts.append("<table>")
        html_parts.append("<tr><th>Rank</th><th>Concept</th><th>Composite</th><th>Model LCOE</th></tr>")
        for rank, s in enumerate(ranked, 1):
            lcoe = _read_lcoe_from_model(analyses_dir, s["concept_id"])
            html_parts.append(
                f"<tr><td>{rank}</td><td class='concept'>{_label(s['concept_id'])}</td>"
                f"<td>{s['geometric_mean']:.2f}</td><td>{lcoe}</td></tr>"
            )
        html_parts.append("</table>")
    else:
        html_parts.append("<p><em>No analyses directory provided — LCOE comparison unavailable.</em></p>")

    # --- Section 5: Calibration adjustments ---
    html_parts.append("<h2>5. Calibration Adjustments</h2>")
    if adjustments:
        html_parts.append("<table class='adjustment-table'>")
        html_parts.append(
            "<tr><th>Concept</th><th>Question</th><th>Criterion</th>"
            "<th>Original</th><th>Adjusted</th><th>Justification</th></tr>"
        )
        for a in adjustments:
            html_parts.append(
                f"<tr><td>{a.get('concept', '')}</td><td>{a.get('question', '')}</td>"
                f"<td>{a.get('criterion', '')}</td><td>{a.get('original', '')}</td>"
                f"<td>{a.get('adjusted', '')}</td><td>{a.get('justification', '')}</td></tr>"
            )
        html_parts.append("</table>")
    else:
        html_parts.append("<p><em>No calibration adjustments recorded.</em></p>")

    html_parts.append("</body></html>")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(html_parts), encoding="utf-8")
