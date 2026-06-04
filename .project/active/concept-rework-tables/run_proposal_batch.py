"""Run the design-point proposal prompt against a list of concepts via `claude -p`.

Saves the raw JSON response and the parsed YAML proposal next to each concept.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROMPT_TEMPLATE = ROOT / "exploration/concept_analysis/prompt_templates/design_point_proposal.md"
ONTOLOGY = ROOT / "exploration/concept_analysis/tables/ontology.csv"
ARCHETYPE_FIT = ROOT / "exploration/concept_analysis/tables/archetype_fit.csv"
PROPOSALS_DIR = ROOT / ".project/active/concept-rework-tables/proposals"


def load_concept_meta() -> dict[str, dict[str, str]]:
    with ONTOLOGY.open() as f:
        onto = {r["concept_id"]: r for r in csv.DictReader(f)}
    with ARCHETYPE_FIT.open() as f:
        fit = {r["concept_id"]: r for r in csv.DictReader(f)}
    meta = {}
    for cid, o in onto.items():
        meta[cid] = {
            "concept_id": cid,
            "concept_name": o["concept_name"],
            "confinement_subfamily": o["confinement_subfamily"],
            "fuel": o["fuel"],
            "fit_grade": fit[cid]["fit_grade"],
        }
    return meta


def build_prompt(template: str, m: dict[str, str]) -> str:
    return (
        template.replace("{concept_id}", m["concept_id"])
        .replace("{concept_name}", m["concept_name"])
        .replace("{confinement_subfamily}", m["confinement_subfamily"])
        .replace("{fuel}", m["fuel"])
        .replace("{fit_grade}", m["fit_grade"])
    )


def run_one(concept_id: str, prompt: str, model: str) -> dict:
    cmd = [
        "claude", "-p", "--output-format", "json",
        "--model", model,
        "--allowedTools", "Read,Glob,Grep",
        "--add-dir", str(ROOT),
    ]
    print(f"  invoking claude -p (model={model}) for {concept_id}...", flush=True)
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, cwd=ROOT,
    )
    if result.returncode != 0:
        print(f"  ERROR: claude returned {result.returncode}", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return {"error": "claude_failed", "stderr": result.stderr, "stdout": result.stdout}
    try:
        events = json.loads(result.stdout)
    except json.JSONDecodeError:
        # Sometimes returned as a single dict, not a list — try that.
        return {"error": "json_decode", "stdout": result.stdout[:2000]}
    return {"events": events}


def extract_yaml_block(trace_text: str) -> str | None:
    """Extract the first ```yaml ... ``` block whose content starts with `proposal:`.

    Returns the YAML body (without the fence lines), or None if no such block.
    """
    import re
    pattern = re.compile(r"```yaml\s*\n(.*?)\n```", re.DOTALL)
    for match in pattern.finditer(trace_text):
        body = match.group(1)
        if body.lstrip().startswith("proposal:"):
            return body
    return None


def extract_result_text(payload: dict) -> str | None:
    """Pull the final 'result' field out of the claude -p JSON envelope."""
    events = payload.get("events")
    if events is None:
        return None
    # `claude -p --output-format json` can return either:
    #   - a single dict with "result" key, or
    #   - a list of event dicts with the final one being type=result.
    if isinstance(events, dict):
        return events.get("result")
    if isinstance(events, list):
        for ev in reversed(events):
            if isinstance(ev, dict) and ev.get("type") == "result":
                return ev.get("result")
        # Fallback: last dict's "result" if present.
        if events and isinstance(events[-1], dict):
            return events[-1].get("result")
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("concepts", nargs="+", help="concept_id slugs to run")
    parser.add_argument("--model", default="sonnet", help="claude model (sonnet/opus/haiku)")
    args = parser.parse_args()

    PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)
    template = PROMPT_TEMPLATE.read_text()
    meta = load_concept_meta()

    for cid in args.concepts:
        if cid not in meta:
            print(f"SKIP {cid}: not in ontology.csv", file=sys.stderr)
            continue
        if meta[cid]["fit_grade"] == "None":
            print(f"SKIP {cid}: fit_grade=None (routes to freeform)", file=sys.stderr)
            continue

        print(f"=== {cid} ({meta[cid]['fit_grade']} fit) ===")
        prompt = build_prompt(template, meta[cid])
        # Save the rendered prompt for audit.
        (PROPOSALS_DIR / f"{cid}.prompt.md").write_text(prompt)

        payload = run_one(cid, prompt, args.model)
        (PROPOSALS_DIR / f"{cid}.raw.json").write_text(json.dumps(payload, indent=2))

        result_text = extract_result_text(payload)
        if result_text is None:
            print(f"  WARN: no result text extracted for {cid}")
            continue
        # Strip any preamble the LLM added before the trace heading.
        # The prompt asks it not to, but Sonnet sometimes adds narration
        # like "Let me write the proposal document." or a Write-tool fallback
        # note. We trim to the first `# Design Point Reasoning Trace` line.
        heading_marker = "# Design Point Reasoning Trace"
        idx = result_text.find(heading_marker)
        if idx > 0:
            preamble = result_text[:idx].strip()
            result_text = result_text[idx:]
            print(f"  trimmed {len(preamble)}-char preamble: {preamble[:80]!r}...")
        (PROPOSALS_DIR / f"{cid}.trace.md").write_text(result_text)
        yaml_block = extract_yaml_block(result_text)
        if yaml_block is None:
            print(f"  WARN: could not locate ```yaml proposal block in trace for {cid}")
        else:
            (PROPOSALS_DIR / f"{cid}.proposal.yaml").write_text(yaml_block)
        first_line = result_text.splitlines()[0] if result_text else ""
        preamble_ok = first_line.startswith("# Design Point Reasoning Trace")
        print(
            f"  saved → proposals/{cid}.trace.md ({len(result_text)} chars), "
            f"yaml={'yes' if yaml_block else 'NO'}, "
            f"starts-with-heading={'yes' if preamble_ok else 'NO'}"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
