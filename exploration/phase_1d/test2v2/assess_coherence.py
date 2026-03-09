#!/usr/bin/env python3
"""Assess coherence of randomly generated fusion concepts using Claude.

Reads random_concepts.json, sends each concept to Claude for assessment
via `claude -p`, and collects structured results into assessments.json.

Adapted from test2 — uses table_corrected.csv column structure (single
Confinement Concept column, no Driver Technology).
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

DIR = Path(__file__).parent
DEFAULT_INPUT = DIR / "random_concepts.json"
DEFAULT_OUTPUT = DIR / "assessments.json"
DEFAULT_PROMPT = DIR / "test2-prompt.md"

# Columns matching the generation script
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


def format_row(concept: dict) -> str:
    """Format a concept row for insertion into the prompt."""
    lines = []
    for col in ALL_COLUMNS:
        val = concept.get(col, "N/A")
        lines.append(f"- **{col}**: {val}")
    return "\n".join(lines)


def build_prompt(template: str, concept: dict) -> str:
    """Fill the prompt template with concept data."""
    row_data = format_row(concept)
    return template.replace("{{ROW_DATA}}", row_data)


def extract_json(text: str) -> dict:
    """Extract a JSON object from text that may contain extra content."""
    # Direct parse
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass

    # Strip markdown code fences
    match = re.search(r"```(?:json)?\s*\n(.*?)\n```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Find first balanced { ... }
    start = text.find("{")
    if start >= 0:
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start : i + 1])
                    except json.JSONDecodeError:
                        break

    raise ValueError(f"Could not extract JSON from response:\n{text[:500]}...")


def call_claude(prompt: str, model: str | None = None) -> str:
    """Call claude -p and return the response text."""
    cmd = ["claude", "-p"]
    if model:
        cmd.extend(["--model", model])

    result = subprocess.run(
        cmd,
        input=prompt,
        capture_output=True,
        text=True,
        timeout=180,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"claude exited with code {result.returncode}\n"
            f"stderr: {result.stderr[:500]}"
        )

    return result.stdout


def assess_one(concept: dict, template: str, model: str | None = None) -> dict:
    """Assess a single concept and return structured result."""
    prompt = build_prompt(template, concept)
    response = call_claude(prompt, model=model)
    assessment = extract_json(response)
    return {
        "id": concept["id"],
        "exact_match": concept.get("exact_match", False),
        "concept": {col: concept[col] for col in ALL_COLUMNS},
        "assessment": assessment,
        "raw_response": response,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Assess coherence of random fusion concepts (family-conditional)"
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--prompt", type=Path, default=DEFAULT_PROMPT)
    parser.add_argument("--model", type=str, default=None, help="e.g. sonnet, haiku")
    parser.add_argument("--start", type=int, default=1, help="Start from concept ID")
    parser.add_argument("--limit", type=int, default=None, help="Max concepts to assess")
    args = parser.parse_args()

    # Load inputs
    with open(args.input) as f:
        data = json.load(f)
    concepts = data["concepts"]

    template = args.prompt.read_text()

    # Filter to requested range
    concepts = [c for c in concepts if c["id"] >= args.start]
    if args.limit:
        concepts = concepts[: args.limit]

    # Load existing results for resume support
    existing: list[dict] = []
    existing_ids: set[int] = set()
    if args.output.exists():
        with open(args.output) as f:
            existing_data = json.load(f)
        existing = existing_data.get("assessments", [])
        existing_ids = {a["id"] for a in existing}
        print(f"Loaded {len(existing)} existing assessments")

    assessments = list(existing)
    total = len(concepts)
    skipped = 0

    for i, concept in enumerate(concepts):
        if concept["id"] in existing_ids:
            skipped += 1
            continue

        seq = i + 1 - skipped
        remaining = total - skipped - seq + 1
        family = concept.get("Confinement Family", "?")
        conc = concept.get("Confinement Concept", "?")
        print(
            f"[{seq}/{total - skipped}] #{concept['id']} ({family}/{conc})...",
            end=" ",
            flush=True,
        )

        try:
            result = assess_one(concept, template, model=args.model)
            coherent = result["assessment"].get("physically_coherent", "?")
            plausible = result["assessment"].get("engineering_plausible", "?")
            novelty = result["assessment"].get("novelty", "?")
            print(f"coherent={coherent}, plausible={plausible}, novelty={novelty}")
            assessments.append(result)
        except Exception as e:
            print(f"FAILED: {e}")
            assessments.append(
                {
                    "id": concept["id"],
                    "exact_match": concept.get("exact_match", False),
                    "concept": {col: concept[col] for col in ALL_COLUMNS},
                    "assessment": None,
                    "error": str(e),
                    "raw_response": None,
                }
            )

        # Write incrementally (crash safety)
        output_data = {
            "model": args.model,
            "prompt_file": str(args.prompt),
            "method": "family-conditional sampling",
            "count": len(assessments),
            "assessments": assessments,
        }
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)

    if skipped:
        print(f"\nSkipped {skipped} already-assessed concepts")
    print(f"Done. {len(assessments)} assessments -> {args.output}")


if __name__ == "__main__":
    main()
