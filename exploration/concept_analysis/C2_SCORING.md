# C2: Scalability — Scoring Methodology

C2 is one of eight criteria (C1–C8) in the fusion concept scoring framework.
All scores are on a 1–5 scale where **5 = most favorable**.

## What C2 measures

C2 captures the **inherent scalability** of a confinement approach: how readily
the concept's architecture supports the power densities, plant sizes, and
operating regimes needed for cost-effective commercial deployment.

## How it is scored

**C2 is NOT scored by Claude.** It is a deterministic lookup assigned by Python
(`lib/scoring.py::detect_c2_category`) based on the concept's confinement
category. This removes judgment from a criterion where the category itself
already carries the relevant evidence.

Each concept is mapped to one of eight categories, and each category has a
fixed score:

| Category                   | Score |
|----------------------------|-------|
| Exotic / Novel             | 4.0   |
| Mirror                     | 3.5   |
| FRC / Compact Pulsed MFE   | 3.5   |
| Laser IFE                  | 3.5   |
| Pulsed MIF (liner/target)  | 3.0   |
| Conventional Tokamak       | 2.5   |
| Stellarator                | 2.5   |
| Levitated Dipole           | 2.0   |

## How the category is derived

Categories are derived **from architecture columns in `table.csv`**, not from
concept ID numbers. This keeps the classification stable across concept
renumbering. The decision rules:

| `Confinement Family` | Additional condition | Category |
|----------------------|----------------------|----------|
| MFE | `MFE Topology` = Tokamak | Conventional Tokamak |
| MFE | `MFE Topology` = Stellarator | Stellarator |
| MFE | `MFE Topology` = Open/Linear and concept slug contains "pinch" | FRC / Compact Pulsed MFE |
| MFE | `MFE Topology` = Open/Linear (otherwise) | Mirror |
| MFE | `MFE Topology` = Compact Toroid / FRC / Compact | FRC / Compact Pulsed MFE |
| MFE | `MFE Topology` = Dipole and `Magnet Type` contains "levitated" | Levitated Dipole |
| MFE | `MFE Topology` = Dipole (non-levitated) | Exotic / Novel |
| IFE | `IFE Driver` = Laser | Laser IFE |
| IFE | other driver (heavy ion beam, projectile, acoustic) | Exotic / Novel |
| MIF | `MIF Method` = FRC compression | FRC / Compact Pulsed MFE |
| MIF | any other MIF method | Pulsed MIF |
| Non-Standard | (any) | Exotic / Novel |
| (unrecognized) | — | Exotic / Novel |

Two slug-based disambiguations exist because the family/topology columns
don't separate them cleanly:

- **Z-pinch vs. mirror** — both are MFE / Open-Linear; the "pinch" check in
  the slug routes z-pinches (Zap) into the compact-pulsed bucket.
- **Levitated dipole vs. non-levitated dipole** — both are MFE / Dipole; the
  "levitated" check on `Magnet Type` separates LDX-heritage devices
  (OpenStar, Zephyr) from exotic dipoles (PoloMac).

## Why this is deterministic

Scalability is a property of the architecture, not of an individual proponent's
design choices. Two HTS tokamaks should receive the same C2 score regardless
of company-specific claims. The lookup makes that comparison consistent across
the 36+ concepts in the survey, and it isolates architectural signal from
proponent-specific narratives (which are scored elsewhere — e.g., C1, C3, C8).

## Where C2 appears in outputs

- **YAML scores block** in `synthesis.md` Section 8 — C2 is **omitted** from
  Claude's output and inserted later by Python.
- **Verified scores** (`verified_scores.json` / `.md`) — C2 appears alongside
  C1–C8 with the assigned `c2_category` for traceability.

## Reference

Full framework: [scoring_framework.md](prompt_templates/config/scoring_framework.md)
Implementation: [scoring.py](scripts/lib/scoring.py)
