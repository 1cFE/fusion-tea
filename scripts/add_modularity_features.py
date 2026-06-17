"""One-off: write driver_architecture and chamber_size_class to IFE/MIF feature YAMLs.

Per-concept assignments locked in conversation 2026-06-17 with the user.
"""
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ROOT / "exploration" / "scoring_v2" / "features"

# (concept_id, driver_architecture, chamber_size_class)
ASSIGNMENTS = [
    # IFE
    ("02-acoustic-icf-sonofusion",        "Acoustic transducer", "small"),
    ("03-laser-icf-liquid-jet-target",    "DPSSL",               "small"),
    ("04-laser-icf",                       "DPSSL",               "small"),
    ("17a-laser-icf-hybrid-drive",        "KrF",                 "medium"),
    ("17b-laser-icf-fast-ignition",       "DPSSL",               "small"),
    ("22-projectile-icf",                  "Projectile gas gun",  "medium"),
    ("23-laser-icf-nanostructured-target", "Ultrashort-pulse",    "small"),
    ("25-heavy-ion-beam-icf",              "Heavy-ion LINAC",     "medium"),
    ("26-laser-icf-indirect-drive",        "Nd:Glass",            "large"),
    ("30-laser-icf-nif-commercialization", "DPSSL",               "large"),
    ("31-laser-icf-oec-architecture",      "Fiber laser CBC",     "large"),
    ("32-laser-icf-french-national",       "Nd:Glass",            "large"),
    # MIF
    ("07-maglif",                                         "LTD pulsed power",  "large"),
    ("08-frc-w-direct-conversion",                        "Capacitor bank",    "compact"),
    ("14-magnetized-target-fusion-pneumatic-compression", "Pneumatic piston",  "medium"),
    ("37-magnetized-target-inertial-fusion-mtif",         "Railgun",           "medium"),
]


def main():
    today = "2026-06-17"
    for cid, driver_arch, chamber_class in ASSIGNMENTS:
        f = FEATURES / f"{cid}.yaml"
        if not f.exists():
            print(f"SKIP {cid}: feature file missing")
            continue
        data = yaml.safe_load(f.read_text(encoding="utf-8"))
        data["driver_architecture"] = {
            "value": driver_arch,
            "provenance": "manual (modularity 2-slot, conversation 2026-06-17)",
            "confidence": "high",
            "extracted_at": today,
        }
        data["chamber_size_class"] = {
            "value": chamber_class,
            "provenance": "manual (modularity 2-slot, conversation 2026-06-17)",
            "confidence": "high",
            "extracted_at": today,
        }
        # YAML round-trip with sorted keys (matches existing file style)
        f.write_text(
            yaml.safe_dump(data, sort_keys=True, default_flow_style=False, allow_unicode=True),
            encoding="utf-8",
        )
        print(f"OK   {cid}: driver={driver_arch}, chamber={chamber_class}")

    # MFE / Non-Standard concepts: write N/A for both new features so they
    # have consistent schema coverage (even though the embeddings short-circuit
    # for non-IFE/MIF families).
    print()
    print("Writing N/A for non-IFE/MIF concepts:")
    ife_mif_ids = {cid for cid, _, _ in ASSIGNMENTS}
    for f in sorted(FEATURES.glob("*.yaml")):
        cid = f.stem
        if cid in ife_mif_ids:
            continue
        data = yaml.safe_load(f.read_text(encoding="utf-8"))
        family = (data.get("confinement_family") or {}).get("value")
        # Only write N/A for MFE / Non-Standard (skip non-concept files if any)
        if family not in ("MFE", "Non-Standard"):
            continue
        if "driver_architecture" not in data:
            data["driver_architecture"] = {
                "value": "N/A",
                "provenance": "manual (modularity 2-slot, MFE/Non-Standard default)",
                "confidence": "high",
                "extracted_at": today,
            }
        if "chamber_size_class" not in data:
            data["chamber_size_class"] = {
                "value": "N/A",
                "provenance": "manual (modularity 2-slot, MFE/Non-Standard default)",
                "confidence": "high",
                "extracted_at": today,
            }
        f.write_text(
            yaml.safe_dump(data, sort_keys=True, default_flow_style=False, allow_unicode=True),
            encoding="utf-8",
        )
        print(f"OK   {cid}: N/A defaults")


if __name__ == "__main__":
    main()
