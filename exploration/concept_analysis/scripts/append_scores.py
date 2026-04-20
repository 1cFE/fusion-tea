"""Append Section 8 (LCOE Downselect Scoring) to syntheses that lack it.

Finds synthesis.md files missing Section 8, sends each to Claude with the
analysis.md, model_setup.py, and model_output.txt for context, and appends
the generated Section 8 to the existing synthesis.

Usage:
    uv run python exploration/concept_analysis/scripts/append_scores.py
    uv run python exploration/concept_analysis/scripts/append_scores.py --dry-run
    uv run python exploration/concept_analysis/scripts/append_scores.py --concepts 02 03 05
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ANALYSES_DIR = SCRIPT_DIR.parent / "analyses"
TEMPLATES_DIR = SCRIPT_DIR.parent / "prompt_templates"
FRAMEWORK_PATH = TEMPLATES_DIR / "config" / "lcoe_downselect_framework.md"


def has_section8(synthesis_path: Path) -> bool:
    """Check if a synthesis already has Section 8."""
    text = synthesis_path.read_text(encoding="utf-8")
    markers = [
        "## 8. Long-Term LCOE Potential",
        "## 8 Long-Term LCOE Potential",
        "Long-Term LCOE Potential (Downselect Scoring)",
    ]
    return any(m in text for m in markers)


def find_concepts_missing_scores(filter_ids: list[str] | None = None) -> list[dict]:
    """Find concepts with synthesis.md but no Section 8."""
    missing = []
    for concept_dir in sorted(ANALYSES_DIR.iterdir()):
        if not concept_dir.is_dir():
            continue
        cid = concept_dir.name
        if filter_ids and not any(cid.startswith(f) for f in filter_ids):
            continue
        synthesis = concept_dir / "synthesis.md"
        if not synthesis.exists():
            continue
        if has_section8(synthesis):
            continue

        # Gather context paths
        analysis = concept_dir / "analysis.md"
        model_setup = concept_dir / "model_setup.py"
        model_output = concept_dir / "model_output.txt"

        missing.append({
            "id": cid,
            "synthesis_path": synthesis,
            "analysis_path": analysis if analysis.exists() else None,
            "model_setup_path": model_setup if model_setup.exists() else None,
            "model_output_path": model_output if model_output.exists() else None,
        })
    return missing


def build_prompt(concept: dict, framework_text: str) -> str:
    """Build the Section 8 append prompt for a single concept."""
    synthesis_text = concept["synthesis_path"].read_text(encoding="utf-8")

    context_files = f"### Existing Synthesis\n\n{synthesis_text}\n"

    if concept["analysis_path"]:
        analysis_text = concept["analysis_path"].read_text(encoding="utf-8")
        # Include Sections 2-3 (challenges, maturity) and Section 5 (parameters)
        context_files += f"\n### Full Analysis\n`{concept['analysis_path']}`\n"

    if concept["model_setup_path"]:
        context_files += f"\n### Model Setup\n`{concept['model_setup_path']}`\n"

    if concept["model_output_path"]:
        model_text = concept["model_output_path"].read_text(encoding="utf-8")
        context_files += f"\n### Model Output\n```\n{model_text}\n```\n"

    prompt = f"""# Append Section 8: LCOE Downselect Scoring

You are adding Section 8 (Long-Term LCOE Potential scoring) to an existing
synthesis for concept **{concept['id']}**.

## Required Reading

Read ALL of the following before scoring:

{context_files}

## Your Task

Write ONLY Section 8 content. Do NOT repeat or modify Sections 1-7.

Score this concept on its long-term cost reduction potential using the seven
criteria defined in the LCOE Downselect Potential Framework below. C1-C6
measure how fast LCOE can improve with deployment experience. C7 measures
how likely the concept is to reach a working plant at all. Both dimensions
matter and are equally weighted.

For each criterion, provide:
- The **score** (1-5, where 5 = most favorable)
- **Sub-scores** where the framework defines them (e.g., per-CAS modularization
  mode, per-component learning rates, complexity sub-drivers, per-gate
  feasibility penalties)
- **2-3 sentences of justification** citing specific data from the analysis,
  model output, CAS breakdown, or taxonomy. Do not score without evidence.

**Important**: Do not double-count between criteria. C4 measures operational
complexity of the built plant, not physics feasibility. C6 uses the physical
availability budget, not TRL-adjusted penalties. C7 is the sole criterion
where "this might not work at all" is scored.

For C7, explicitly enumerate each feasibility gate with its severity
(binary/degrading/schedule), evidence level, and penalty calculation.

Present as a table:

| Criterion | Score | Key justification |
|-----------|-------|-------------------|
| C1: Modularization | X.X | ... |
| C2: Scalability | X.X | ... |
| C3: Supply Chain Learning | X.X | ... |
| C4: Plant Complexity | X.X | ... |
| C5: Customization Needs | X.X | ... |
| C6: Upper Capacity Factor | X.X | ... |
| C7: Technical Feasibility | X.X | ... |
| **Composite** | **X.X** | |

After the table, write a **one-paragraph verdict** interpreting the composite
score: what it means for this concept's long-term competitiveness, which
criteria are the strongest levers for improvement, and what would need to
change to materially raise the score.

## LCOE Downselect Potential Framework (Full Rubric)

{framework_text}

## Output

Write your Section 8 output (starting with the heading) to:
`{{{{output_path}}}}`
"""
    return prompt


def invoke_claude(prompt: str, output_path: Path, timeout: int = 600,
                  dry_run: bool = False) -> bool:
    """Invoke Claude headlessly."""
    if dry_run:
        prompt_path = output_path.with_suffix(".prompt.md")
        prompt_path.write_text(prompt, encoding="utf-8")
        print(f"    dry-run: prompt saved to {prompt_path.name}")
        return True

    prompt = prompt.replace("{{output_path}}", str(output_path))

    cmd = [
        "claude", "-p",
        "--dangerously-skip-permissions", "--verbose",
        "--output-format", "json",
    ]

    t0 = time.time()
    try:
        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
    except subprocess.TimeoutExpired:
        print(f"    FAILED: timed out after {timeout}s")
        return False

    elapsed = time.time() - t0

    # Parse JSON output
    try:
        parsed = json.loads(result.stdout)
        if isinstance(parsed, list):
            for event in parsed:
                if isinstance(event, dict) and event.get("type") == "result":
                    text = event.get("result", "")
                    break
            else:
                text = result.stdout
        elif isinstance(parsed, dict):
            text = parsed.get("result", result.stdout)
        else:
            text = result.stdout
    except (json.JSONDecodeError, TypeError, ValueError):
        text = result.stdout or ""

    if result.returncode != 0:
        print(f"    FAILED (rc={result.returncode}, {elapsed:.0f}s)")
        if result.stderr:
            print(f"      stderr: {result.stderr[:300]}")
        return False

    # Check if Claude wrote the file directly
    if output_path.exists():
        print(f"    done ({elapsed:.0f}s)")
        return True

    # If not, write the response text
    if text.strip():
        output_path.write_text(text, encoding="utf-8")
        print(f"    done ({elapsed:.0f}s, wrote {len(text)} chars)")
        return True

    print(f"    FAILED: empty response ({elapsed:.0f}s)")
    return False


def main():
    parser = argparse.ArgumentParser(description="Append Section 8 scores to syntheses")
    parser.add_argument("--dry-run", action="store_true", help="Save prompts without invoking Claude")
    parser.add_argument("--concepts", nargs="*", help="Filter to specific concept ID prefixes (e.g., 02 03 05)")
    args = parser.parse_args()

    framework_text = FRAMEWORK_PATH.read_text(encoding="utf-8")

    concepts = find_concepts_missing_scores(args.concepts)
    if not concepts:
        print("All syntheses already have Section 8 scores.")
        return

    print(f"Found {len(concepts)} concepts missing Section 8:")
    for c in concepts:
        print(f"  {c['id']}")

    print()
    succeeded = 0
    failed = 0

    for c in concepts:
        print(f"  [{c['id']}]")
        prompt = build_prompt(c, framework_text)

        # Write Section 8 to a temp file, then append
        section8_path = c["synthesis_path"].parent / "section8_append.md"

        ok = invoke_claude(prompt, section8_path, dry_run=args.dry_run)
        if not ok:
            failed += 1
            continue

        if args.dry_run:
            succeeded += 1
            continue

        # Append to synthesis.md
        section8_text = section8_path.read_text(encoding="utf-8").strip()
        if not section8_text:
            print(f"    FAILED: empty Section 8 output")
            failed += 1
            section8_path.unlink(missing_ok=True)
            continue

        synthesis_text = c["synthesis_path"].read_text(encoding="utf-8").rstrip()
        c["synthesis_path"].write_text(
            synthesis_text + "\n\n" + section8_text + "\n",
            encoding="utf-8",
        )
        # Clean up temp file
        section8_path.unlink(missing_ok=True)
        print(f"    appended to synthesis.md")
        succeeded += 1

    print(f"\nDone: {succeeded} succeeded, {failed} failed")


if __name__ == "__main__":
    main()
