"""Cross-concept calibration of LCOE Downselect Potential scores.

Pass 2 of a two-pass scoring system. Reads Section 8 scores from all
synthesis.md files, sends them to Claude alongside the scoring rubric,
and asks for a calibrated comparison with inconsistency corrections.

Usage:
    uv run python exploration/concept_analysis/scripts/calibrate_scores.py
    uv run python exploration/concept_analysis/scripts/calibrate_scores.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ANALYSES_DIR = SCRIPT_DIR.parent / "analyses"
TEMPLATES_DIR = SCRIPT_DIR.parent / "prompt_templates"
FRAMEWORK_PATH = TEMPLATES_DIR / "config" / "lcoe_downselect_framework.md"
OUTPUT_DIR = SCRIPT_DIR.parent / "calibration"


def extract_section8(synthesis_path: Path) -> str | None:
    """Extract Section 8 (Long-Term LCOE Potential) from a synthesis.md file."""
    text = synthesis_path.read_text(encoding="utf-8")
    # Find the start of Section 8
    patterns = [
        "## 8. Long-Term LCOE Potential",
        "# Long-Term LCOE Potential",
        "## 8 Long-Term LCOE Potential",
        "Long-Term LCOE Potential (Downselect Scoring)",
    ]
    start = -1
    for pat in patterns:
        idx = text.find(pat)
        if idx != -1:
            start = idx
            break
    if start == -1:
        return None
    return text[start:]


def extract_frontmatter_field(synthesis_path: Path, field: str) -> str:
    """Extract a YAML frontmatter field from a synthesis file."""
    text = synthesis_path.read_text(encoding="utf-8")
    m = re.search(rf"^{field}:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def find_scored_concepts() -> list[dict]:
    """Find all concepts with Section 8 scores in their synthesis."""
    scored = []
    for concept_dir in sorted(ANALYSES_DIR.iterdir()):
        if not concept_dir.is_dir():
            continue
        synthesis = concept_dir / "synthesis.md"
        if not synthesis.exists():
            continue
        section8 = extract_section8(synthesis)
        if section8 is None:
            continue

        concept_name = extract_frontmatter_field(synthesis, "Concept")
        company = extract_frontmatter_field(synthesis, "Company")

        # Extract analysis Sections 2 and 3 for gate audit
        analysis = concept_dir / "analysis.md"
        challenges_text = ""
        if analysis.exists():
            full_text = analysis.read_text(encoding="utf-8")
            # Extract Section 2 (Challenges) and Section 3 (Maturity)
            s2_start = full_text.find("## 2")
            if s2_start == -1:
                s2_start = full_text.find("## 2.")
            s4_start = full_text.find("## 4")
            if s4_start == -1:
                s4_start = full_text.find("## 4.")
            if s2_start != -1 and s4_start != -1:
                challenges_text = full_text[s2_start:s4_start]
            elif s2_start != -1:
                # Take ~5000 chars from Section 2 onward
                challenges_text = full_text[s2_start:s2_start + 5000]

        scored.append({
            "id": concept_dir.name,
            "name": concept_name or concept_dir.name,
            "company": company,
            "section8": section8,
            "challenges": challenges_text,
            "synthesis_path": str(synthesis),
        })
    return scored


def build_prompt(concepts: list[dict], framework_text: str) -> str:
    """Build the calibration prompt."""
    concept_sections = []
    for c in concepts:
        section = (
            f"### {c['id']}: {c['name']} ({c['company']})\n\n"
            f"#### Section 8 Scores (from synthesis.md)\n\n"
            f"{c['section8']}\n"
        )
        if c.get("challenges"):
            section += (
                f"\n#### Analysis Sections 2–3: Challenges & Maturity "
                f"(from analysis.md — use for gate audit)\n\n"
                f"{c['challenges']}\n"
            )
        concept_sections.append(section)
    all_concepts = "\n---\n\n".join(concept_sections)

    prompt = f"""# Cross-Concept Calibration of LCOE Downselect Scores

You are performing **Pass 2** of a two-pass scoring system for long-term LCOE
potential of fusion energy concepts. In Pass 1, each concept was scored
independently by a separate Claude session. Your job is to review all scores
together and calibrate them for cross-concept consistency.

## Your Task

### Step 1: C7 Gate Audit (do this FIRST, before other criteria)

The most common Pass 1 error is **undercounting binary gates**. Each concept's
C7 justification lists its gates, but Pass 1 scorers often collapsed multiple
distinct physics requirements into a single gate, or omitted gates that peer
concepts were penalized for.

**For each concept**, do the following:

a) **List every physics or engineering milestone** that must succeed for the
   concept to produce net electricity. Be granular — if a concept requires
   (1) a novel confinement mode, (2) a novel fuel burn regime, AND (3) a
   novel energy conversion mechanism, those are THREE gates, not one.

b) **Cross-check gates against peer concepts.** If Concept A is penalized for
   "driver lifespan at rep-rate" as a binary gate, then every pulsed concept
   with a novel driver must also carry this gate (or explain why it's retired
   for that concept). Common gates that should be checked across ALL concepts:
   - Net energy gain (Q > 1 at the claimed conditions)
   - Confinement mode validity (at commercial parameters)
   - Driver/heating system at commercial rep-rate or power level
   - Energy conversion mechanism (if non-standard)
   - Fuel burn regime (if non-standard, e.g., nonthermal, aneutronic)
   - Chamber/first-wall survival at commercial conditions
   - Any claimed energy-per-event or gain that exceeds standard physics by >10×

c) **Flag undercounted gates.** If your audit finds gates that Pass 1 missed,
   list them explicitly with severity and evidence level. Recompute C7 from
   the corrected gate list using the rubric formula.

d) **Apply the floor rule strictly**: ≥3 unretired binary gates (at
   "analytically supported" or worse) → C7 = 1.0. No overrides.

### Step 2: Full Criteria Consistency Review (C1–C7)

After the gate audit, review all criteria for cross-concept consistency:

- Same physical characteristic scored differently across concepts
  (e.g., "single chamber per plant" scored as replication=3 for one IFE
  concept but replication=1 for another)
- Score inversions: concept A has strictly better attributes than B on
  a criterion but scores lower
- Unjustified spread: concepts with similar architectures scoring >1 point
  apart on a criterion without clear justification
- Criteria where the justification contradicts the score
- C4 (complexity): verify that physics coupling chains are NOT counted —
  only operational failure cascades and maintenance dependencies. Apply the
  "magic wand" test.
- C6 (capacity factor): verify scores come from the physical CF_upper
  calculation per the rubric table, with NO ad-hoc TRL adjustments
  (those belong in C7). Critically, verify that scheduled downtime
  estimates use the **replacement complexity assessment** from the rubric:
  estimate replacement duration using the four multipliers (access method,
  maintenance environment, component modularity, serial step count).
  D-T concepts with toroidal geometry and remote handling typically need
  100–200 day blanket replacement campaigns, NOT the 2–3 weeks that
  Pass 1 scorers often assume. Aneutronic concepts with direct access
  and hands-on maintenance may need only days. Self-renewing components
  (liquid walls) eliminate the replacement term entirely. This is often
  the largest correction in C6 calibration.
- Module count boost applied consistently per the rubric's
  diminishing-returns table

### Step 3: Produce calibrated scores with adjustments explained

### Step 4: Z-Score Normalization

After producing the calibrated raw score table (Part 3), compute z-score
normalized scores. For each criterion i:

```
z_i,c = (calibrated_raw_score_i,c − mean_i) / stdev_i
```

Where mean_i and stdev_i are computed across all concepts for criterion i.
Then compute the z-score composite as the mean of z-scores across all 7
criteria for each concept.

**Include a z-score table as Part 5** with the same format as Part 3 but
showing z-scores instead of raw scores. Round z-scores to 2 decimal places.
Rank by z-score composite (this is the final ranking).

The z-score composite is the authoritative ranking metric. It ensures
every criterion contributes equally regardless of its natural scale.

## Output Format

Write the output to the file specified below. Structure it as:

### Part 1: C7 Gate Audit
For each concept, produce a standardized gate table:

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| [description] | Binary/Degrading/Schedule | Demonstrated/Subscale/Analytical/Speculative | −X.X | [justification] |

Then the recalculated C7 score. Flag any concept where the gate count
changed from Pass 1.

### Part 2: Other Inconsistencies Found
For each non-C7 inconsistency:
- Which concepts and criteria are affected
- What the original scores were
- Why they are inconsistent
- What the correct relative ordering should be

### Part 3: Calibrated Score Table

A single comparison table with all concepts and all criteria:

| Criterion | [Concept 1] | [Concept 2] | ... | Notes |
|-----------|-------------|-------------|-----|-------|
| C1 | original → calibrated | ... | ... | reason for any change |
| ... | ... | ... | ... | ... |
| **Composite** | **X.X** | **X.X** | ... | |

### Part 4: Ranking by Raw Composite

Rank concepts by calibrated raw composite score. For each:
- One sentence on its strongest structural advantage
- One sentence on its most binding constraint

### Part 5: Z-Score Normalized Table and Final Ranking

Compute z-scores for each criterion across all concepts. Present as a table:

| Criterion | [Concept 1] | [Concept 2] | ... |
|-----------|-------------|-------------|-----|
| C1 (z) | +X.XX | −X.XX | ... |
| ... | ... | ... | ... |
| **Z-Composite** | **+X.XX** | **−X.XX** | ... |

Then rank by z-composite (this is the final authoritative ranking).
For each concept in the final ranking:
- One sentence on its strongest structural advantage
- One sentence on its most binding constraint
- How confident you are in the relative ranking (High/Medium/Low)
- Note any cases where the z-score ranking differs from the raw ranking and why

---

## Scoring Framework (Rubric)

{framework_text}

---

## Concept Scores from Pass 1

{all_concepts}

---

Write your calibration report to: `{{{{output_path}}}}`
"""
    return prompt


def invoke_claude(prompt: str, output_path: Path, timeout: int = 1800,
                  dry_run: bool = False) -> bool:
    """Invoke Claude headlessly with the calibration prompt."""
    if dry_run:
        prompt_path = output_path.with_suffix(".prompt.md")
        prompt_path.write_text(prompt, encoding="utf-8")
        print(f"  dry-run: prompt saved to {prompt_path}")
        return True

    # Replace output_path placeholder
    prompt = prompt.replace("{{output_path}}", str(output_path))

    cmd = [
        "claude", "-p",
        "--dangerously-skip-permissions", "--verbose",
        "--output-format", "json",
    ]

    import time
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
        print(f"  FAILED: timed out after {timeout}s")
        return False

    elapsed = time.time() - t0

    # Parse JSON output
    try:
        parsed = json.loads(result.stdout)
        if isinstance(parsed, list):
            # Verbose mode returns event list
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
        print(f"  FAILED (rc={result.returncode}, {elapsed:.0f}s)")
        if result.stderr:
            print(f"    stderr: {result.stderr[:300]}")
        return False

    # Check if Claude wrote the file directly
    if output_path.exists():
        size = len(output_path.read_text(encoding="utf-8"))
        print(f"  done ({elapsed:.0f}s, {size} chars written to {output_path.name})")
        return True

    # If not, write the response text
    if text.strip():
        output_path.write_text(text, encoding="utf-8")
        print(f"  done ({elapsed:.0f}s, {len(text)} chars)")
        return True

    print(f"  FAILED: no output generated ({elapsed:.0f}s)")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Cross-concept calibration of LCOE Downselect scores"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Save prompt without calling Claude")
    parser.add_argument("--timeout", type=int, default=1800,
                        help="Claude invocation timeout in seconds")
    args = parser.parse_args()

    # Find scored concepts
    concepts = find_scored_concepts()
    if not concepts:
        print("No concepts with Section 8 scores found.")
        sys.exit(1)

    print(f"Found {len(concepts)} scored concepts:")
    for c in concepts:
        print(f"  {c['id']}: {c['name']}")

    # Load framework
    if not FRAMEWORK_PATH.exists():
        print(f"ERROR: Framework not found at {FRAMEWORK_PATH}")
        sys.exit(1)
    framework_text = FRAMEWORK_PATH.read_text(encoding="utf-8")

    # Build prompt
    prompt = build_prompt(concepts, framework_text)
    print(f"\nPrompt size: {len(prompt):,} chars")

    # Prepare output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    output_path = OUTPUT_DIR / f"calibration_{today}.md"

    # Invoke
    print(f"\nRunning calibration...")
    ok = invoke_claude(prompt, output_path, timeout=args.timeout,
                       dry_run=args.dry_run)

    if ok and not args.dry_run:
        print(f"\nCalibration report: {output_path}")
    elif not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
