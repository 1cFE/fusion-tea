#!/usr/bin/env python3
"""Summarize coherence assessment results from family-conditional sampling.

Computes quantitative statistics, then calls Claude for qualitative synthesis.
Compares results against the original test2 (unconditional sampling, 0% coherence).

Outputs:
  - summary.json: structured results
  - summary.md: human-readable report section
"""

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path

DIR = Path(__file__).parent
DEFAULT_INPUT = DIR / "assessments.json"
DEFAULT_JSON_OUTPUT = DIR / "summary.json"
DEFAULT_MD_OUTPUT = DIR / "summary.md"

ALL_COLUMNS = [
    "Confinement Family",
    "Confinement Concept",
    "Fuel",
    "Primary Heating",
    "Energy Capture",
    "Plasma State",
    "Magnet Type",
    "Tritium Breeding",
    "Neutron Management",
    "Operation Mode",
    "Repetition Rate",
]


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

    # Exact match analysis
    exact_matches = sum(1 for a in valid if a.get("exact_match"))
    exact_match_coherent = sum(
        1
        for a in valid
        if a.get("exact_match") and a["assessment"].get("physically_coherent")
    )
    novel_only = [a for a in valid if not a.get("exact_match")]
    novel_coherent = sum(
        1 for a in novel_only if a["assessment"].get("physically_coherent")
    )

    # Failure mode analysis
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

    # Family distribution + coherence by family
    family_counts = Counter(
        a["concept"].get("Confinement Family", "?") for a in valid
    )
    family_coherence: dict[str, dict] = {}
    for family in family_counts:
        family_valid = [
            a for a in valid if a["concept"].get("Confinement Family") == family
        ]
        fc = sum(
            1 for a in family_valid if a["assessment"].get("physically_coherent")
        )
        family_coherence[family] = {
            "count": len(family_valid),
            "coherent": fc,
            "rate": fc / len(family_valid) if family_valid else 0,
        }

    # Concept-level coherence (which concept types produced coherent results?)
    concept_coherence: dict[str, dict] = {}
    for a in valid:
        concept = a["concept"].get("Confinement Concept", "?")
        if concept not in concept_coherence:
            concept_coherence[concept] = {"count": 0, "coherent": 0}
        concept_coherence[concept]["count"] += 1
        if a["assessment"].get("physically_coherent"):
            concept_coherence[concept]["coherent"] += 1

    return {
        "total_assessed": n,
        "errored": len(errored),
        "coherent": coherent,
        "plausible": plausible,
        "coherence_rate": round(coherence_rate, 3),
        "plausibility_rate": round(plausibility_rate, 3),
        "exact_matches": exact_matches,
        "exact_match_coherent": exact_match_coherent,
        "novel_count": len(novel_only),
        "novel_coherent": novel_coherent,
        "novel_coherence_rate": round(novel_coherent / len(novel_only), 3)
        if novel_only
        else None,
        "top_constraint_pairs": [
            {
                "pair": pair,
                "count": count,
                "example_reasons": pair_reasons[pair][:2],
            }
            for pair, count in pair_counts.most_common(15)
        ],
        "novelty_distribution": dict(novelty_counts),
        "family_distribution": dict(family_counts),
        "family_coherence": family_coherence,
        "concept_coherence": concept_coherence,
    }


def build_synthesis_prompt(assessments: list[dict], stats: dict) -> str:
    """Build a prompt for Claude to produce qualitative synthesis."""

    assessment_lines = []
    for a in assessments:
        if a.get("assessment") is None:
            continue
        asmt = a["assessment"]
        concept = a["concept"]
        family = concept.get("Confinement Family", "?")
        conc_type = concept.get("Confinement Concept", "?")
        fuel = concept.get("Fuel", "?")
        heating = concept.get("Primary Heating", "?")
        energy = concept.get("Energy Capture", "?")
        exact = " [EXACT]" if a.get("exact_match") else ""

        status = "COHERENT" if asmt.get("physically_coherent") else "INCOHERENT"
        failures = "; ".join(
            f'{fr["column_a"]}={fr.get("value_a","?")} vs {fr["column_b"]}={fr.get("value_b","?")}: {fr["reason"]}'
            for fr in asmt.get("failure_reasons", [])
        )
        assessment_lines.append(
            f"#{a['id']} [{status}]{exact} {family}/{conc_type}/{fuel}/{heating}/{energy}"
            + (f" — FAILURES: {failures}" if failures else "")
            + (
                f" — Nearest: {asmt.get('nearest_concept', '?')}, Novelty: {asmt.get('novelty', '?')}"
            )
        )

    assessments_text = "\n".join(assessment_lines)

    pairs_text = "\n".join(
        f"  {p['pair']}: {p['count']} failures"
        for p in stats["top_constraint_pairs"][:10]
    )

    return f"""# Fusion Concept Design Space — Family-Conditional Coherence Analysis

You are analyzing the results of a **family-conditional** generative coherence test. This is a follow-up to a previous test that used unconditional sampling and produced **0% coherence** (0/30).

## Method Change

**Original test (test2)**: Sampled from table_v2.csv with 18 columns (decomposed confinement hierarchy). Non-confinement columns (Fuel, Primary Heating, etc.) sampled from global vocabularies. Result: 0/30 coherent — dominated by cross-family contamination (IFE heating on MFE concepts, etc.).

**This test (test2v2)**: Sampled from table_corrected.csv with a single "Confinement Concept" column. Non-confinement columns sampled from **family-conditional** vocabularies (only values observed for that family). This eliminates cross-family contamination and tests whether **within-family** columns are independent design choices.

Key change: Driver Technology (free-text) was excluded to avoid concept-specific description mismatches.

## Quantitative Results

- **Coherence rate**: {stats['coherence_rate']} ({stats['coherent']}/{stats['total_assessed']})
- **Plausibility rate**: {stats['plausibility_rate']} ({stats['plausible']}/{stats['total_assessed']})
- **Exact matches to real concepts**: {stats['exact_matches']} (of which {stats['exact_match_coherent']} coherent)
- **Novel combinations**: {stats['novel_count']} (of which {stats['novel_coherent']} coherent, rate={stats.get('novel_coherence_rate', 'N/A')})
- **Novelty distribution**: {json.dumps(stats['novelty_distribution'])}
- **Family distribution**: {json.dumps(stats['family_distribution'])}
- **Coherence by family**: {json.dumps(stats['family_coherence'], indent=2)}
- **Coherence by concept type**: {json.dumps(stats['concept_coherence'], indent=2)}

## Top Constraint Pairs (failure causes)

{pairs_text}

## All Assessments (compact)

{assessments_text}

## Your Task

Produce a qualitative synthesis comparing this test with the original (0% coherence). Sections:

### 1. Impact of Family-Conditional Sampling

How much did conditioning on family improve coherence? What does the delta tell us about where the coupling lives (cross-family vs. within-family)?

### 2. Within-Family Constraint Structure

Which within-family column pairs are still tightly coupled? Are there families where within-family sampling works well (high coherence) vs. poorly (still ~0%)?

### 3. Remaining Failure Patterns

What types of failures remain after eliminating cross-family contamination? Are they:
- **Concept-specific constraints** (e.g., stellarator can't use ohmic heating)
- **Fuel-cascade constraints** (fuel choice determines neutron management, energy capture, etc.)
- **Soft engineering preferences** (technically possible but purposeless)

### 4. Independent vs. Coupled Dimensions (Within-Family)

Within a given family, which columns can be varied freely vs. which are still correlated? How many genuine degrees of freedom exist within each family?

### 5. Novel Coherent Concepts

Did family-conditional sampling produce any novel, coherent concepts? Are they genuinely interesting or trivial variations?

### 6. Revised Verdict

Given the original test (0% unconditional) and this test (family-conditional), what is the revised structural assessment of this table? Specifically:
- Is it a classification scheme at ALL levels, or a classification scheme at the family level with some design-space character within families?
- How many true degrees of freedom exist?
- What does this imply for the AND/OR graph / pattern card design in the next phase?

Respond in markdown. Be direct and analytical. Compare explicitly with the original 0% result.
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

    return f"""## Test 2v2: Family-Conditional Generative Coherence

### Method

Sampling conditioned on Confinement Family (using `table_corrected.csv` with single Confinement Concept column). Non-confinement columns sampled from family-conditional vocabularies. Driver Technology excluded.

**Comparison**: Original test2 used unconditional sampling from `table_v2.csv` → 0/30 coherent (0%).

### Quantitative Results

| Metric | test2 (unconditional) | test2v2 (family-conditional) |
|--------|----------------------|------------------------------|
| Concepts assessed | 30 | {stats['total_assessed']} |
| Physically coherent | 0 (0%) | {stats['coherent']} ({stats['coherence_rate']:.0%}) |
| Engineering plausible | 0 (0%) | {stats['plausible']} ({stats['plausibility_rate']:.0%}) |
| Exact matches | 0 | {stats['exact_matches']} |
| Novel coherent | 0 | {stats['novel_coherent']} |

**Novelty distribution**: {json.dumps(stats['novelty_distribution'])}

### Coherence by Confinement Family

| Family | Generated | Coherent | Rate |
|--------|-----------|----------|------|
{family_rows}

### Top Constraint Pairs (remaining failures)

| Column Pair | Failures | Example Reason |
|-------------|----------|----------------|
{pairs_rows}

### Qualitative Synthesis

{synthesis}
"""


def main():
    parser = argparse.ArgumentParser(
        description="Summarize family-conditional coherence assessments"
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--md-output", type=Path, default=DEFAULT_MD_OUTPUT)
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--skip-synthesis", action="store_true")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)
    assessments = data["assessments"]

    print(f"Loaded {len(assessments)} assessments from {args.input}")

    stats = compute_stats(assessments)
    print(
        f"\nCoherence rate: {stats['coherence_rate']:.0%} "
        f"({stats['coherent']}/{stats['total_assessed']})"
    )
    print(
        f"Plausibility rate: {stats['plausibility_rate']:.0%} "
        f"({stats['plausible']}/{stats['total_assessed']})"
    )
    print(f"Exact matches: {stats['exact_matches']}")
    print(f"Novel coherent: {stats['novel_coherent']}/{stats['novel_count']}")
    print(f"Novelty: {stats['novelty_distribution']}")
    print(f"\nCoherence by family:")
    for fam, info in stats["family_coherence"].items():
        print(f"  {fam}: {info['coherent']}/{info['count']} ({info['rate']:.0%})")
    print(f"\nTop constraint pairs:")
    for p in stats["top_constraint_pairs"][:5]:
        print(f"  {p['pair']}: {p['count']} failures")

    synthesis = ""
    if not args.skip_synthesis:
        print("\nCalling Claude for qualitative synthesis...")
        prompt = build_synthesis_prompt(assessments, stats)
        synthesis = call_claude(prompt, model=args.model)
        print("Synthesis complete.")
    else:
        synthesis = "*Synthesis skipped (--skip-synthesis)*"

    summary = {"stats": stats, "synthesis": synthesis}
    with open(args.json_output, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nJSON summary -> {args.json_output}")

    md = format_markdown_report(stats, synthesis)
    with open(args.md_output, "w") as f:
        f.write(md)
    print(f"Markdown summary -> {args.md_output}")


if __name__ == "__main__":
    main()
