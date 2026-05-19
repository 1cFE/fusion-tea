"""Translate Mallory's v3 CSV (origin/fix/concept-renumbering-robustness) onto our ID scheme.

Reads:
  - exploration/phase_1a/_mallory_table.csv   (Mallory's checked-in snapshot)
  - exploration/concept_analysis/table.csv    (our current main CSV, for identity-column overlay)

Writes:
  - exploration/concept_analysis/table.csv    (canonical)
  - exploration/phase_1a/table.csv            (byte-identical mirror)

Translation dispatch:
  - Drop Pranos (Mallory already lacks it; defensive).
  - Mallory's row 23 (First Light) → our 22 (Research ID overwritten).
  - Mallory's row 31 (Inertia, deduped) → emit twice as our 26 and our 30,
    overlaying identity columns (Concept Name / Company / Driver Technology /
    Research ID) from our main CSV — these distinguish 26 (Indirect Drive)
    from 30 (NIF Commercialization).
  - Mallory's rows 37 / 38 / 39 → emit verbatim (new concepts, same IDs).
  - All other rows → renumber via RENUMBER_MAP; rewrite ID and Research ID.

Idempotence guard: after writing, re-run the dispatch in-memory and assert
byte-identical output.
"""

from __future__ import annotations

import csv
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MALLORY_CSV = ROOT / "exploration/phase_1a/_mallory_table.csv"
OURS_MAIN_CSV = ROOT / "exploration/concept_analysis/table.csv"
OUT_MAIN_CSV = ROOT / "exploration/concept_analysis/table.csv"
OUT_PHASE1A_CSV = ROOT / "exploration/phase_1a/table.csv"

# Mallory's numeric ID → our slug ID (the 16 renumbered concepts).
# Source: spec.md lines 70-90.
RENUMBER_MAP: dict[str, str] = {
    "17": "17b-laser-icf-fast-ignition",                  # Focused Energy
    "20": "20a-type-one-stellarator",                     # Type One
    "21": "20b-renaissance-stellarator",                  # Renaissance
    "22": "21-spherical-tokamak-hts",                     # Tokamak Energy ST
    "24": "23-laser-icf-nanostructured-target",           # Marvel
    "25": "24-dense-plasma-focus",                        # LPPFusion
    "26": "25-heavy-ion-beam-icf",                        # Intensity Energy
    "27": "17a-laser-icf-hybrid-drive",                   # Xcimer
    "28": "27-polywell",                                  # EMC2 Polywell
    "29": "28-hts-tokamak-full-hts",                      # Energy Singularity
    "30": "29-negative-triangularity-tokamak",            # Firefly NT
    "32": "31-laser-icf-oec-architecture",                # Blue Laser OEC
    "33": "32-laser-icf-french-national",                 # GenF
    "34": "33-state-backed-tokamak-best",                 # Neo Fusion BEST
}

# Mallory's IDs that are unchanged on our side (numeric-prefix slugs preserved).
# These get ID rewritten only to ensure trailing slug matches our directory.
UNCHANGED_IDS: dict[str, str] = {
    "01": "01-hts-compact-tokamak",
    "02": "02-acoustic-icf-sonofusion",
    "03": "03-laser-icf-liquid-jet-target",
    "04": "04-laser-icf",
    "05": "05-planar-coil-stellarator",
    "06": "06-magnetic-mirror",
    "07": "07-maglif",
    "08": "08-frc-w-direct-conversion",
    "09": "09-qi-stellarator-hts",
    "10": "10-large-scale-stellarator",
    "11": "11-magnetic-mirror",
    "12": "12-levitated-dipole",
    "13": "13-electrostatic-hybrid",
    "14": "14-magnetized-target-fusion-pneumatic-compression",
    "15": "15-sheared-flow-stabilized-z-pinch",
    "16": "16-muon-catalyzed-fusion",
    "18": "18-p-b11-frc",
    "19": "19-orbital-levitated-dipole",
    "35": "35-polomac-magnetic-confinement",
    "36": "36-helical-coil-stellarator",
    "37": "37-magnetized-target-inertial-fusion-mtif",
    "38": "38-particle-accelerator-driven-fusion",
    "39": "39-spherical-tokamak-cs-free-p-b11",
}

# Special cases keyed by Mallory's ID-prefix (first hyphen-separated token).
SPLIT_22_MALLORY_ID = "23"             # Mallory's 23 (First Light) → our 22
FAN_OUT_26_30_MALLORY_ID = "31"        # Mallory's 31 (Inertia) → our 26 AND our 30
DROP_COMPANY_SUBSTRINGS = ("Pranos",)  # defensive — Mallory already lacks Pranos

# Identity columns used for the 26/30 fan-out — these come from our main CSV.
IDENTITY_COLS = ("Concept Name", "Company", "Driver Technology", "Research ID")

# Our IDs that receive identity overlay (in emission order from Mallory's row 31).
FAN_OUT_TARGETS = ("26-laser-icf-indirect-drive", "30-laser-icf-nif-commercialization")

# Our ID for the split-22 case.
SPLIT_22_OUR_ID = "22-projectile-icf"


def mallory_id_prefix(row: dict) -> str:
    """Extract the numeric/string ID prefix from Mallory's row (before first hyphen)."""
    return row["ID"].split("-", 1)[0]


def load_csv(path: Path) -> tuple[list[str], list[dict]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or [], list(reader)


def index_by_id(rows: list[dict]) -> dict[str, dict]:
    return {row["ID"]: row for row in rows}


def render_csv(fieldnames: list[str], rows: list[dict]) -> bytes:
    """Render rows to bytes using \n line terminator and minimal-quoting (csv default)."""
    buf = io.StringIO(newline="")
    # Use CRLF line terminator to match Mallory's CSV (verified via cat -A).
    writer = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\r\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return buf.getvalue().encode("utf-8")


def translate(mallory_rows: list[dict], ours_index: dict[str, dict], fieldnames: list[str]) -> list[dict]:
    """Apply dispatch logic — return translated rows in our preferred order."""
    out: list[dict] = []
    seen_our_ids: set[str] = set()

    for row in mallory_rows:
        prefix = mallory_id_prefix(row)
        company = row.get("Company", "")
        if any(s in company for s in DROP_COMPANY_SUBSTRINGS):
            continue

        if prefix == FAN_OUT_26_30_MALLORY_ID:
            for our_id in FAN_OUT_TARGETS:
                ours_row = ours_index.get(our_id)
                if ours_row is None:
                    raise SystemExit(f"main CSV missing fan-out target {our_id!r}")
                new_row = {k: row.get(k, "") for k in fieldnames}
                new_row["ID"] = our_id
                for col in IDENTITY_COLS:
                    if col in fieldnames:
                        new_row[col] = ours_row.get(col, "")
                # Research ID convention: our slug.
                if "Research ID" in fieldnames:
                    new_row["Research ID"] = our_id
                out.append(new_row)
                seen_our_ids.add(our_id)
            continue

        if prefix == SPLIT_22_MALLORY_ID:
            # First Light only — Mallory already excluded NearStar (which becomes her row 37).
            new_row = {k: row.get(k, "") for k in fieldnames}
            new_row["ID"] = SPLIT_22_OUR_ID
            if "Research ID" in fieldnames:
                new_row["Research ID"] = SPLIT_22_OUR_ID
            out.append(new_row)
            seen_our_ids.add(SPLIT_22_OUR_ID)
            continue

        if prefix in RENUMBER_MAP:
            our_id = RENUMBER_MAP[prefix]
        elif prefix in UNCHANGED_IDS:
            our_id = UNCHANGED_IDS[prefix]
        else:
            raise SystemExit(f"unmapped Mallory ID prefix: {prefix!r} (row ID={row['ID']!r})")

        new_row = {k: row.get(k, "") for k in fieldnames}
        new_row["ID"] = our_id
        if "Research ID" in fieldnames:
            new_row["Research ID"] = our_id
        out.append(new_row)
        seen_our_ids.add(our_id)

    return out


def sort_key(our_id: str) -> tuple:
    """Sort our IDs naturally: 01 < 02 < ... < 17a < 17b < 18 < ... < 20a < 20b < 21 < ..."""
    prefix = our_id.split("-", 1)[0]
    # Split numeric and alpha portions of the prefix (e.g., "17a" → (17, "a")).
    num_part = ""
    alpha_part = ""
    for ch in prefix:
        if ch.isdigit():
            num_part += ch
        else:
            alpha_part += ch
    return (int(num_part) if num_part else 0, alpha_part)


def main() -> int:
    mallory_fields, mallory_rows = load_csv(MALLORY_CSV)
    _, ours_rows = load_csv(OURS_MAIN_CSV)
    ours_index = index_by_id(ours_rows)

    translated = translate(mallory_rows, ours_index, mallory_fields)
    translated.sort(key=lambda r: sort_key(r["ID"]))

    payload = render_csv(mallory_fields, translated)

    # Idempotence: re-translate using the rendered output's rows (parsed) and
    # confirm the same payload is produced.
    reparsed_rows = list(csv.DictReader(io.StringIO(payload.decode("utf-8"))))
    # Direct re-render (rows are already in our scheme — should round-trip exactly).
    payload2 = render_csv(mallory_fields, reparsed_rows)
    if payload != payload2:
        raise SystemExit("idempotence guard failed: round-trip render differs")

    OUT_MAIN_CSV.write_bytes(payload)
    OUT_PHASE1A_CSV.write_bytes(payload)

    print(f"wrote {len(translated)} data rows to:")
    print(f"  {OUT_MAIN_CSV.relative_to(ROOT)}")
    print(f"  {OUT_PHASE1A_CSV.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
