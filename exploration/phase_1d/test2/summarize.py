#!/usr/bin/env python3
"""Summarize coherence assessment results.

Computes quantitative statistics from assessments.json, then calls Claude
for qualitative synthesis (constraint density matrix, pattern analysis, verdict).

Outputs:
  - summary.json: structured results
  - summary.md: human-readable report section
"""

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

DIR = Path(__file__).parent
DEFAULT_INPUT = DIR / "assessments.json"
DEFAULT_JSON_OUTPUT = DIR / "summary.json"
DEFAULT_MD_OUTPUT = DIR / "summary.md"


def call_claude(prompt: str, model: str | None = None) -> str:
    """Call claude -p and return the response text."""
    cmd = ["claude", "-p"]
    if model:
        cmd.extend(["--model", model])
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, timeout=300
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"claude exited with code {result.returncode}\nstderr: {result.stderr[:500]}"
        )
    return result.stdout


def compute_stats(assessments: list[dict]) -> dict:
    """Compute quantitative statistics from assessment results."""
    valid = [a for a in assessments if a.get("assessment") is not None]
    errored = [a for a in assessments if a.get("assessment") is None]

    n = len(valid)
    if n == 0:
        return {"error": "No valid assessments"}

    coherent = sum(1 for a in valid if a["assessment"].get("physically_coherent"))
    plausible = sum(1 for a in valid if a["assessment"].get("engineering_plausible"))

    coherence_rate = coherent / n
    plausibility_rate = plausible / n

    # Failure mode analysis: count column pairs that cause conflicts
    pair_counts: Counter = Counter()
    pair_reasons: dict[str, list[str]] = {}
    for a in valid:
        for fr in a["assessment"].get("failure_reasons", []):
            col_a = fr.get("column_a", "?")
            col_b = fr.get("column_b", "?")
            pair_key = " × ".join(sorted([col_a, col_b]))
            pair_counts[pair_key] += 1
            pair_reasons.setdefault(pair_key, []).append(fr.get("reason", ""))

    # Novelty distribution
    novelty_counts = Counter(
        a["assessment"].get("novelty", "unknown") for a in valid
    )

    # Confinement family distribution in generated set
    family_counts = Counter(
        a["concept"].get("Confinement Family", "?") for a in valid
    )

    # Coherence rate by family
    family_coherence: dict[str, dict] = {}
    for family in family_counts:
        family_valid = [a for a in valid if a["concept"].get("Confinement Family") == family]
        fc = sum(1 for a in family_valid if a["assessment"].get("physically_coherent"))
        family_coherence[family] = {
            "count": len(family_valid),
            "coherent": fc,
            "rate": fc / len(family_valid) if family_valid else 0,
        }

    return {
        "total_assessed": n,
        "errored": len(errored),
        "coherent": coherent,
        "plausible": plausible,
        "coherence_rate": round(coherence_rate, 3),
        "plausibility_rate": round(plausibility_rate, 3),
        "top_constraint_pairs": [
            {"pair": pair, "count": count, "example_reasons": pair_reasons[pair][:2]}
            for pair, count in pair_counts.most_common(15)
        ],
        "novelty_distribution": dict(novelty_counts),
        "family_distribution": dict(family_counts),
        "family_coherence": family_coherence,
    }


def build_synthesis_prompt(assessments: list[dict], stats: dict) -> str:
    """Build a prompt for Claude to produce qualitative synthesis."""

    # Compact representation of each assessment
    assessment_lines = []
    for a in assessments:
        if a.get("assessment") is None:
            continue
        asmt = a["assessment"]
        concept = a["concept"]
        family = concept.get("Confinement Family", "?")
        fuel = concept.get("Fuel", "?")
        heating = concept.get("Primary Heating", "?")
        energy = concept.get("Energy Capture", "?")

        status = "COHERENT" if asmt.get("physically_coherent") else "INCOHERENT"
        failures = "; ".join(
            f'{fr["column_a"]}={fr["value_a"]} vs {fr["column_b"]}={fr["value_b"]}: {fr["reason"]}'
            for fr in asmt.get("failure_reasons", [])
        )
        assessment_lines.append(
            f"#{a['id']} [{status}] {family}/{fuel}/{heating}/{energy}"
            + (f" — FAILURES: {failures}" if failures else "")
            + (f" — Nearest: {asmt.get('nearest_concept', '?')}" if asmt.get("physically_coherent") else "")
            + (f" — Novelty: {asmt.get('novelty', '?')}" if asmt.get("physically_coherent") else "")
        )

    assessments_text = "\n".join(assessment_lines)

    # Top constraint pairs
    pairs_text = "\n".join(
        f"  {p['pair']}: {p['count']} failures"
        for p in stats["top_constraint_pairs"][:10]
    )

    return f"""# Fusion Concept Design Space — Qualitative Synthesis

You are analyzing the results of a generative coherence test on a fusion concept morphological table. 30 random concepts were generated by sampling from the controlled vocabulary of 38 real fusion startup concepts (with structural N/A rules applied). Each was assessed for physical coherence and engineering plausibility.

## Quantitative Results

- **Coherence rate**: {stats['coherence_rate']} ({stats['coherent']}/{stats['total_assessed']})
- **Plausibility rate**: {stats['plausibility_rate']} ({stats['plausible']}/{stats['total_assessed']})
- **Novelty distribution**: {json.dumps(stats['novelty_distribution'])}
- **Family distribution**: {json.dumps(stats['family_distribution'])}
- **Coherence by family**: {json.dumps(stats['family_coherence'], indent=2)}

## Top Constraint Pairs (most frequent failure causes)

{pairs_text}

## All Assessments (compact)

{assessments_text}

## Your Task

Produce a qualitative synthesis with these sections:

### 1. Constraint Density Matrix

From the failure reasons, build a qualitative constraint density matrix for the most important column pairs. Rate each pair as: **none** (no observed or expected constraints), **weak** (rare constraints, edge cases), **moderate** (some value combinations forbidden), **strong** (most combinations forbidden — these columns are highly coupled).

Present as a markdown table. Only include pairs with weak or stronger coupling. Group by strength.

### 2. Independent vs. Coupled Dimensions

Which columns function as genuinely independent morphological dimensions (can be freely varied without breaking coherence)? Which are tightly coupled to other columns and should be thought of as correlated choices rather than independent axes?

### 3. Failure Pattern Analysis

What types of failures dominate? Are they mostly:
- **Physics incompatibilities** (fundamental: these values cannot coexist in nature)
- **Engineering mismatches** (these values could theoretically coexist but create unsolvable engineering problems)
- **Coherence gaps** (the values are individually fine but together don't describe a recognizable or purposeful concept)

### 4. Novel Coherent Concepts

If any coherent concepts were assessed as "novel" or "variant", are they genuinely interesting? Could any represent an unexplored region of the design space worth investigating?

### 5. Verdict

Based on the coherence rate, constraint structure, and failure patterns: **is this table a design space or a classification scheme?**

A *design space* would have mostly independent dimensions with a high coherence rate (>50%) — random combinations usually work, and the table captures the degrees of freedom.

A *classification scheme* would have tightly coupled dimensions with a low coherence rate (<20%) — the columns describe correlated choices that must be selected together, and the table captures observations rather than degrees of freedom.

What's the verdict, and what does it imply for building a richer representation (AND/OR graph, pattern cards)?

Respond in markdown. Be direct and analytical.
"""


def format_markdown_report(stats: dict, synthesis: str) -> str:
    """Format the final markdown report section."""
    pairs_rows = "\n".join(
        f"| {p['pair']} | {p['count']} | {p['example_reasons'][0][:80] if p['example_reasons'] else ''} |"
        for p in stats["top_constraint_pairs"][:10]
    )

    family_rows = "\n".join(
        f"| {fam} | {info['count']} | {info['coherent']} | {info['rate']:.0%} |"
        for fam, info in stats["family_coherence"].items()
    )

    return f"""## Test 2 & 3: Generative Coherence + Constraint Density

### Quantitative Results

| Metric | Value |
|--------|-------|
| Concepts assessed | {stats['total_assessed']} |
| Physically coherent | {stats['coherent']} ({stats['coherence_rate']:.0%}) |
| Engineering plausible | {stats['plausible']} ({stats['plausibility_rate']:.0%}) |
| Errored assessments | {stats['errored']} |

**Novelty distribution**: {json.dumps(stats['novelty_distribution'])}

### Coherence by Confinement Family

| Family | Generated | Coherent | Rate |
|--------|-----------|----------|------|
{family_rows}

### Top Constraint Pairs

| Column Pair | Failures | Example Reason |
|-------------|----------|----------------|
{pairs_rows}

### Qualitative Synthesis

{synthesis}
"""


def main():
    parser = argparse.ArgumentParser(description="Summarize coherence assessments")
    parser.add_argument(
        "--input", type=Path, default=DEFAULT_INPUT, help="Assessments JSON"
    )
    parser.add_argument(
        "--json-output", type=Path, default=DEFAULT_JSON_OUTPUT, help="Summary JSON output"
    )
    parser.add_argument(
        "--md-output", type=Path, default=DEFAULT_MD_OUTPUT, help="Summary markdown output"
    )
    parser.add_argument(
        "--model", type=str, default=None, help="Claude model for synthesis"
    )
    parser.add_argument(
        "--skip-synthesis", action="store_true", help="Skip Claude call, output stats only"
    )
    args = parser.parse_args()

    # Load assessments
    with open(args.input) as f:
        data = json.load(f)
    assessments = data["assessments"]

    print(f"Loaded {len(assessments)} assessments from {args.input}")

    # Compute stats
    stats = compute_stats(assessments)
    print(f"\nCoherence rate: {stats['coherence_rate']:.0%} ({stats['coherent']}/{stats['total_assessed']})")
    print(f"Plausibility rate: {stats['plausibility_rate']:.0%} ({stats['plausible']}/{stats['total_assessed']})")
    print(f"Novelty: {stats['novelty_distribution']}")
    print(f"\nTop constraint pairs:")
    for p in stats["top_constraint_pairs"][:5]:
        print(f"  {p['pair']}: {p['count']} failures")

    # Qualitative synthesis via Claude
    synthesis = ""
    if not args.skip_synthesis:
        print("\nCalling Claude for qualitative synthesis...")
        prompt = build_synthesis_prompt(assessments, stats)
        synthesis = call_claude(prompt, model=args.model)
        print("Synthesis complete.")
    else:
        synthesis = "*Synthesis skipped (--skip-synthesis)*"

    # Write JSON output
    summary = {
        "stats": stats,
        "synthesis": synthesis,
    }
    with open(args.json_output, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nJSON summary -> {args.json_output}")

    # Write markdown output
    md = format_markdown_report(stats, synthesis)
    with open(args.md_output, "w") as f:
        f.write(md)
    print(f"Markdown summary -> {args.md_output}")


if __name__ == "__main__":
    main()
