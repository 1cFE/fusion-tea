"""Add canonical ID column to table_v2.csv based on Phase 1a directory names."""
import csv
import shutil

# Mapping: table "Concept Name" → Phase 1a directory ID
# Built by matching company names and concept descriptions
CONCEPT_ID_MAP = {
    "HTS Compact Tokamak": "01-hts-compact-tokamak",
    "Spherical Tokamak - HTS": "21-spherical-tokamak-hts",
    "HTS Tokamak - Full HTS": "28-hts-tokamak-full-hts",
    "Negative Triangularity Tokamak": "29-negative-triangularity-tokamak",
    "State-Backed Tokamak - BEST": "33-state-backed-tokamak-best",
    "Compact Spherical Tokamak - India": "34-compact-spherical-tokamak-india",
    "Planar Coil Stellarator": "05-planar-coil-stellarator",
    "QI Stellarator - HTS": "09-qi-stellarator-hts",
    "Large-Scale Stellarator": "10-large-scale-stellarator",
    "QI Modular HTS Stellarator - Infinity Two": "20a-type-one-stellarator",
    "Compact Liquid-Wall HTS Stellarator": "20b-renaissance-stellarator",
    "Helical Coil Stellarator": "36-helical-coil-stellarator",
    "FRC w/ Direct Conversion": "08-frc-w-direct-conversion",
    "p-B11 FRC": "18-p-b11-frc",
    "Sheared-Flow Stabilized Z-Pinch": "15-sheared-flow-stabilized-z-pinch",
    "Magnetic Mirror (p-B11)": "06-magnetic-mirror",
    "Magnetic Mirror (D-T)": "11-magnetic-mirror",
    "MagLIF (D-T)": "07-maglif",
    "Magnetized Target Fusion - Pneumatic Compression (D-T)": "14-magnetized-target-fusion-pneumatic-compression",
    "Levitated Dipole (D-T)": "12-levitated-dipole",
    "Orbital Levitated Dipole (D-He3)": "19-orbital-levitated-dipole",
    # NOTE: Concept 17 was split in schema v0.2.2:
    #   Xcimer → hybrid drive (stays as 17a)
    #   Focused Energy → fast ignition (new: 17b)
    # Phase 1a dir 17-laser-icf-direct-drive contains pre-split data for both.
    "Laser ICF - Fast Ignition (D-T)": "17b-laser-icf-fast-ignition",
    "Laser ICF - Hybrid Direct Drive (D-T)": "17a-laser-icf-hybrid-drive",
    "Laser ICF - Indirect Drive (D-T)": "26-laser-icf-indirect-drive",
    "Laser ICF - NIF Commercialization (D-T)": "30-laser-icf-nif-commercialization",
    "Laser ICF - OEC Architecture (D-T)": "31-laser-icf-oec-architecture",
    "Laser ICF - French National Direct Drive (D-T)": "32-laser-icf-french-national",
    "Laser ICF - Liquid Jet Target (D-D)": "03-laser-icf-liquid-jet-target",
    "Laser ICF - p-B11 Fast Ignition": "04-laser-icf",
    "Laser ICF - Nanostructured Target (p-B11)": "23-laser-icf-nanostructured-target",
    "Projectile ICF (D-T)": "22-projectile-icf",
    "Heavy Ion Beam ICF (D-T)": "25-heavy-ion-beam-icf",
    "Acoustic ICF / Sonofusion (D-D)": "02-acoustic-icf-sonofusion",
    "Electrostatic Hybrid (D-T)": "13-electrostatic-hybrid",
    "Muon-Catalyzed Fusion (D-T)": "16-muon-catalyzed-fusion",
    "Dense Plasma Focus (p-B11)": "24-dense-plasma-focus",
    "Polywell (D-T)": "27-polywell",
    "PoloMac Magnetic Confinement": "35-polomac-magnetic-confinement",
}

INPUT = "exploration/phase_1b_v2/table_v2.csv"
OUTPUT = "exploration/concept_analysis/table.csv"

with open(INPUT, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

# Add ID as first column
new_fieldnames = ["ID"] + fieldnames

# Verify all concept names have mappings
unmapped = []
for row in rows:
    name = row["Concept Name"]
    if name not in CONCEPT_ID_MAP:
        unmapped.append(name)

if unmapped:
    print("ERROR: Unmapped concept names:")
    for name in unmapped:
        print(f"  - {name}")
    exit(1)

# Write new CSV with ID column, sorted by ID
for row in rows:
    row["ID"] = CONCEPT_ID_MAP[row["Concept Name"]]

rows.sort(key=lambda r: (
    int(''.join(c for c in r["ID"].split("-")[0] if c.isdigit())),
    r["ID"].split("-")[0]  # secondary sort for a/b suffixes
))

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=new_fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {OUTPUT}")
print(f"\nID assignments:")
for row in rows:
    print(f"  {row['ID']:45s} → {row['Concept Name']}")
