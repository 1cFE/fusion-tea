#!/usr/bin/env python3
"""Run Test 4: Blind row assessment for 5 selected concepts.

Reads test4-prompt.md template, fills in each concept's stripped row data,
calls claude -p per concept, and saves responses.
"""

import json
import subprocess
import sys
from pathlib import Path

DIR = Path(__file__).parent
PROMPT_TEMPLATE = DIR / "test4-prompt.md"
OUTPUT = DIR / "test4_responses.json"

# 5 selected concepts — row data with Driver Technology withheld
CONCEPTS = {
    "A": {
        "Confinement Family": "MFE",
        "MFE Topology": "Stellarator",
        "IFE Driver": "N/A",
        "MIF Method": "N/A",
        "Non-Standard Mechanism": "N/A",
        "Tokamak Shape": "N/A",
        "Stellarator Type": "Modular",
        "Laser Approach": "N/A",
        "Fuel": "D-T",
        "Primary Heating": "RF (ECRH)",
        "Energy Capture": "Thermal (steam)",
        "Plasma State": "Burning",
        "Magnet Type": "HTS (3D stellarator)",
        "Tritium Breeding": "Solid ceramic breeder (HCPB)",
        "Neutron Management": "Integrated blanket/shield",
        "Operation Mode": "Steady-state",
        "Repetition Rate": "N/A",
    },
    "B": {
        "Confinement Family": "MFE",
        "MFE Topology": "Compact Toroid",
        "IFE Driver": "N/A",
        "MIF Method": "N/A",
        "Non-Standard Mechanism": "N/A",
        "Tokamak Shape": "N/A",
        "Stellarator Type": "N/A",
        "Laser Approach": "N/A",
        "Fuel": "p-B11",
        "Primary Heating": "NBI",
        "Energy Capture": "Thermal (steam)",
        "Plasma State": "Sustained",
        "Magnet Type": "Resistive",
        "Tritium Breeding": "N/A",
        "Neutron Management": "Minimal (aneutronic)",
        "Operation Mode": "Steady-state",
        "Repetition Rate": "N/A",
    },
    "C": {
        "Confinement Family": "IFE",
        "MFE Topology": "N/A",
        "IFE Driver": "Laser",
        "MIF Method": "N/A",
        "Non-Standard Mechanism": "N/A",
        "Tokamak Shape": "N/A",
        "Stellarator Type": "N/A",
        "Laser Approach": "Hybrid drive",
        "Fuel": "D-T",
        "Primary Heating": "Laser (direct drive)",
        "Energy Capture": "Thermal (unspecified)",
        "Plasma State": "Compressed",
        "Magnet Type": "N/A",
        "Tritium Breeding": "FLiBe blanket",
        "Neutron Management": "Integrated blanket/shield",
        "Operation Mode": "Pulsed",
        "Repetition Rate": "Sub-Hz",
    },
    "D": {
        "Confinement Family": "MIF",
        "MFE Topology": "N/A",
        "IFE Driver": "N/A",
        "MIF Method": "Magnetized target",
        "Non-Standard Mechanism": "N/A",
        "Tokamak Shape": "N/A",
        "Stellarator Type": "N/A",
        "Laser Approach": "N/A",
        "Fuel": "D-T",
        "Primary Heating": "Mechanical compression",
        "Energy Capture": "Thermal (steam)",
        "Plasma State": "Compressed",
        "Magnet Type": "Self-confined",
        "Tritium Breeding": "Liquid metal wall",
        "Neutron Management": "Integrated blanket/shield",
        "Operation Mode": "Pulsed",
        "Repetition Rate": "~1 Hz",
    },
    "E": {
        "Confinement Family": "Non-Standard",
        "MFE Topology": "N/A",
        "IFE Driver": "N/A",
        "MIF Method": "N/A",
        "Non-Standard Mechanism": "Plasma focus",
        "Tokamak Shape": "N/A",
        "Stellarator Type": "N/A",
        "Laser Approach": "N/A",
        "Fuel": "p-B11",
        "Primary Heating": "Electromagnetic pinch (DPF)",
        "Energy Capture": "Direct (charged particle)",
        "Plasma State": "Pinch",
        "Magnet Type": "Self-confined",
        "Tritium Breeding": "N/A",
        "Neutron Management": "Minimal (aneutronic)",
        "Operation Mode": "Pulsed",
        "Repetition Rate": "High (>10 Hz)",
    },
}

COLUMNS = [
    "Confinement Family", "MFE Topology", "IFE Driver", "MIF Method",
    "Non-Standard Mechanism", "Tokamak Shape", "Stellarator Type",
    "Laser Approach", "Fuel", "Primary Heating", "Energy Capture",
    "Plasma State", "Magnet Type", "Tritium Breeding", "Neutron Management",
    "Operation Mode", "Repetition Rate",
]


def format_row(concept: dict) -> str:
    lines = []
    for col in COLUMNS:
        val = concept.get(col, "N/A")
        lines.append(f"- **{col}**: {val}")
    return "\n".join(lines)


def build_prompt(template: str, letter: str, concept: dict) -> str:
    row_data = format_row(concept)
    return template.replace("{{CONCEPT_LETTER}}", letter).replace("{{ROW_DATA}}", row_data)


def call_claude(prompt: str, model: str | None = None) -> str:
    cmd = ["claude", "-p"]
    if model:
        cmd.extend(["--model", model])
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, timeout=180,
    )
    if result.returncode != 0:
        raise RuntimeError(f"claude exited {result.returncode}: {result.stderr[:500]}")
    return result.stdout


def main():
    model = None
    if len(sys.argv) > 1 and sys.argv[1].startswith("--model"):
        if "=" in sys.argv[1]:
            model = sys.argv[1].split("=", 1)[1]
        elif len(sys.argv) > 2:
            model = sys.argv[2]

    template = PROMPT_TEMPLATE.read_text()

    # Load existing results for resume
    results: dict[str, dict] = {}
    if OUTPUT.exists():
        with open(OUTPUT) as f:
            existing = json.load(f)
        results = {r["letter"]: r for r in existing.get("responses", [])}
        print(f"Loaded {len(results)} existing responses")

    for letter, concept in CONCEPTS.items():
        if letter in results:
            print(f"[{letter}] Already assessed, skipping")
            continue

        print(f"[{letter}] Assessing...", end=" ", flush=True)
        prompt = build_prompt(template, letter, concept)

        try:
            response = call_claude(prompt, model=model)
            results[letter] = {
                "letter": letter,
                "concept": concept,
                "response": response,
            }
            print(f"done ({len(response)} chars)")
        except Exception as e:
            print(f"FAILED: {e}")
            results[letter] = {
                "letter": letter,
                "concept": concept,
                "response": None,
                "error": str(e),
            }

        # Write incrementally
        output_data = {
            "model": model,
            "responses": [results[k] for k in sorted(results)],
        }
        with open(OUTPUT, "w") as f:
            json.dump(output_data, f, indent=2)

    print(f"\nDone. {len(results)} responses -> {OUTPUT}")


if __name__ == "__main__":
    main()
