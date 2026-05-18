> **Note:** This document uses the concept IDs from `origin/fix/concept-renumbering-robustness`. This repository kept its existing IDs — see [ID_MAPPING.md](ID_MAPPING.md) to translate.

# Fusion Concept Ontology (v0.3.0 schema)

**Generated**: 2026-05-12
**Source data**: [concept_analysis/table.csv](../concept_analysis/table.csv) with P1-P10 schema revisions applied
**Companion**: [concept_ontology_v3.png](concept_ontology_v3.png) (visual heatmap)

## Schema columns (v0.3.0)

| Column | Description | Vocabulary |
|---|---|---|
| **Fuel** | Primary fusion fuel cycle | D-T · D-D · D-He3 · p-B11 |
| **Heating Type** (P8) | MFE auxiliary heating physics; N/A for compression-driven or non-thermal concepts | ICRH · ECRH · NBI · Ohmic · combinations (e.g. `ICRH + NBI`) · `N/A (compression-driven)` · `N/A (non-thermal)` · TBD |
| **Driver Type** (P9) | Engineering subsystem that drives the fusion conditions | Magnetic · Magnetic pinch · DPSSL Laser · Gas Laser · Ion/particle beam · Mechanical/kinetic · Electrostatic · Other · TBD |
| **Energy Capture** | How fusion energy is converted to electricity (or other output) | Thermal (steam/sCO2/unspec) · Direct (inductive/charged particle) · Hybrid (thermal + direct) · N/A (non-power) · TBD |
| **Magnet Type** (P4) | Primary magnet technology for plasma confinement | HTS variants · LTS · LTS+HTS · Resistive · None · Electrostatic · N/A · TBD |
| **Blanket Config** (P3) | Blanket chemistry / architecture for tritium breeding | Liquid metal · Molten salt · Solid breeder · Other/hybrid · N/A (no tritium) · N/A (non-power) · TBD |
| **Operation Mode** | Temporal profile of fusion burn | Steady-state · Quasi-steady · Pulsed · TBD |
| **Repetition Rate** | For pulsed concepts, the frequency of fusion burn events | Sub-Hz · ~1 Hz · ~10 Hz · High (>10 Hz) · kHz · N/A (steady-state) · TBD |
| **Laser Drive Architecture** (P10) | For laser/beam IFE only: direct/indirect/hybrid drive | Direct drive · Indirect drive · Hybrid drive · N/A (non-laser concepts) |

Eliminated in v0.3.0 (per P1, P2): `Plasma State` (derivable from Confinement Concept + Operation Mode); `Neutron Management` (implied by Fuel).

---

## Concept ontology table (39 concepts)

| # | Family | Topology | Sub-type | Code | Company / Concept | Fuel | Heating Type | Driver Type | Energy Capture | Magnet Type | Blanket Config | Op Mode | Rep Rate | Laser Drive Arch. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | MFE | Tokamak | Compact | CFS | Commonwealth | D-T | ICRH | Magnetic | Thermal (steam) | HTS (wound) | Molten salt | Quasi-steady | N/A | N/A |
| 29 | MFE | Tokamak | Compact | ESN | Energy Singularity | D-T | ICRH | Magnetic | Thermal (unspec) | HTS (wound) | TBD | Steady-state | N/A | N/A |
| 22 | MFE | Tokamak | Spherical | TKE | Tokamak Energy | D-T | ECRH | Magnetic | Thermal (unspec) | HTS (wound) | Liquid metal | Quasi-steady | N/A | N/A |
| 39 | MFE | Tokamak | Spherical | ENN | ENN Energy | p-B11 | ECRH | Magnetic | Direct (charged particle) | HTS (wound) | N/A (no tritium) | Quasi-steady | N/A | N/A |
| 34 | MFE | Tokamak | Standard | BST | BEST / Neo Fusion | D-T | ICRH + ECRH + NBI | Magnetic | Thermal (unspec) | LTS+HTS | TBD | Quasi-steady | N/A | N/A |
| 30 | MFE | Tokamak | Neg-tri | FFY | Firefly | D-T | ECRH | Magnetic | Thermal (unspec) | HTS (wound) | TBD | Quasi-steady | N/A | N/A |
| 09 | MFE | Stellarator | QI | PRX | Proxima | D-T | ECRH | Magnetic | Thermal (unspec) | HTS (3D stellarator) | Liquid metal | Steady-state | N/A | N/A |
| 10 | MFE | Stellarator | QI | GAU | Gauss | D-T | ECRH | Magnetic | Thermal (unspec) | LTS+HTS | Liquid metal | Steady-state | N/A | N/A |
| 20 | MFE | Stellarator | Modular | T1E | Type One | D-T | ECRH | Magnetic | Thermal (steam) | HTS (3D stellarator) | Solid breeder | Steady-state | N/A | N/A |
| 21 | MFE | Stellarator | Modular | REN | Renaissance | D-T | NBI | Magnetic | Thermal (sCO2) | HTS (3D stellarator) | Other/hybrid | Steady-state | N/A | N/A |
| 05 | MFE | Stellarator | Planar | THE | Thea | D-T | ECRH | Magnetic | Thermal (steam) | HTS (planar array) | Liquid metal | Steady-state | N/A | N/A |
| 36 | MFE | Stellarator | Helical | HLF | Helical Fusion | D-T | ECRH | Magnetic | Thermal (sCO2) | HTS (3D stellarator) | Liquid metal | Steady-state | N/A | N/A |
| 06 | MFE | Open/Linear | Mirror | PBL | Pale Blue (p-B11) | p-B11 | ICRH | Magnetic | Direct (charged particle) | TBD | N/A (no tritium) | Steady-state | N/A | N/A |
| 11 | MFE | Open/Linear | Mirror | REA | Realta (D-T) | D-T | ICRH + NBI | Magnetic | Hybrid (thermal + direct) | HTS (wound) | Liquid metal | Steady-state | N/A | N/A |
| 15 | MFE | Open/Linear | Z-pinch | ZAP | Zap Energy | D-T | Ohmic | Magnetic pinch | Thermal (steam) | None | Liquid metal | Pulsed | ~10 Hz | N/A |
| 18 | MFE | Cmpt-Tor | FRC sust. | TAE | TAE Technologies | p-B11 | NBI | Magnetic | Thermal (steam) | Resistive | N/A (no tritium) | Steady-state | N/A | N/A |
| 12 | MFE | Dipole | Levitated | OPS | OpenStar | D-T | ICRH | Magnetic | Thermal (unspec) | HTS (levitated dipole) | Solid breeder | Quasi-steady | N/A | N/A |
| 19 | MFE | Dipole | Orbital | ZPH | Zephyr | D-He3 | ECRH | Magnetic | Direct (charged particle) | HTS (levitated dipole) | N/A (no tritium) | Steady-state | N/A | N/A |
| 35 | MFE | Dipole | Supported | PLM | PoloMac / Deutelio | D-D | TBD | TBD | Thermal (unspec) | Resistive | N/A (no tritium) | Steady-state | N/A | N/A |
| 32 | IFE | Laser | Direct | OEC | Blue Laser Fusion | D-T | N/A (compression-driven) | DPSSL Laser | Hybrid (thermal + direct) | N/A | Liquid metal | Pulsed | ~10 Hz | Direct drive |
| 33 | IFE | Laser | Direct | GNF | GenF Systems | D-T | N/A (compression-driven) | DPSSL Laser | Thermal (unspec) | N/A | Liquid metal | Pulsed | ~10 Hz | Direct drive |
| 31 | IFE | Laser | Indirect | INE | Inertia Enterprises | D-T | N/A (compression-driven) | DPSSL Laser | Thermal (steam) | N/A | Liquid metal | Pulsed | ~10 Hz | Indirect drive |
| 27 | IFE | Laser | Hybrid | XCM | Xcimer | D-T | N/A (compression-driven) | Gas Laser | Thermal (unspec) | N/A | Molten salt | Pulsed | Sub-Hz | Hybrid drive |
| 17 | IFE | Laser | Fast-ig. | FOC | Focused Energy | D-T | N/A (compression-driven) | DPSSL Laser | Thermal (steam) | N/A | Liquid metal | Pulsed | ~10 Hz | Direct drive |
| 03 | IFE | Laser | Ultrashort | COR | Cortex | D-D | N/A (compression-driven) | DPSSL Laser | TBD | N/A | N/A (no tritium) | Pulsed | kHz | Direct drive |
| 04 | IFE | Laser | Ultrashort | HB1 | HB11 Energy | p-B11 | N/A (compression-driven) | DPSSL Laser | Thermal (steam) | N/A | N/A (no tritium) | Pulsed | ~1 Hz | Direct drive |
| 24 | IFE | Laser | Ultrashort | MVL | Marvel | p-B11 | N/A (compression-driven) | DPSSL Laser | Hybrid (thermal + direct) | N/A | N/A (no tritium) | Pulsed | ~10 Hz | Direct drive |
| 23 | IFE | Projectile | — | FLF | First Light | D-T | N/A (compression-driven) | Mechanical/kinetic | Thermal (steam) | N/A | Liquid metal | Pulsed | Sub-Hz | N/A |
| 26 | IFE | Heavy ion | — | INT | Intensity Energy | D-T | N/A (compression-driven) | Ion/particle beam | Thermal (steam) | N/A | Liquid metal | Pulsed | ~10 Hz | Direct drive |
| 02 | IFE | Other | Acoustic | SON | Sonofusion | D-D | N/A (non-thermal) | Other | TBD | N/A | N/A (no tritium) | Pulsed | kHz | N/A |
| 08 | MIF | FRC | Pulsed compr. | HEL | Helion | D-He3 | N/A (compression-driven) | Magnetic | Direct (inductive) | Resistive | Other/hybrid | Pulsed | ~1 Hz | N/A |
| 14 | MIF | Mag. target | Pneumatic | GFU | General Fusion | D-T | N/A (compression-driven) | Mechanical/kinetic | Thermal (steam) | None | Liquid metal | Pulsed | ~1 Hz | N/A |
| 37 | MIF | Mag. target | Mechanical | NST | NearStar | D-D | N/A (compression-driven) | Mechanical/kinetic | Thermal (unspec) | None | TBD | Pulsed | TBD | N/A |
| 07 | MIF | Pulsed power | MagLIF | PAC | Pacific Fusion | D-T | N/A (compression-driven) | Magnetic pinch | Thermal (unspec) | None | TBD | Pulsed | Sub-Hz | N/A |
| 28 | Estatic | Polywell | — | EMC | EMC2 (Polywell) | D-T | N/A (non-thermal) | Electrostatic | Thermal (unspec) | Resistive | TBD | Steady-state | N/A | N/A |
| 13 | Estatic | IEC | — | AVL | Avalanche | D-T | N/A (non-thermal) | Electrostatic | Thermal (unspec) | Electrostatic | TBD | Steady-state | N/A | N/A |
| 25 | Other | DPF | — | LPP | LPPFusion | p-B11 | Ohmic | Magnetic pinch | Direct (charged particle) | None | N/A (no tritium) | Pulsed | High (>10 Hz) | N/A |
| 16 | Other | Muon | — | ACC | Acceleron | D-T | N/A (non-thermal) | Other | Thermal (unspec) | N/A | TBD | Steady-state | N/A | N/A |
| 38 | Other | Accelerator | — | SHI | SHINE | D-T | N/A (non-thermal) | Ion/particle beam | N/A | None | N/A (non-power) | Steady-state | N/A | N/A |

---

## Grouping summary

### By Confinement Family

| Family | Count | Concepts |
|---|---|---|
| MFE | 19 | CFS, ESN, TKE, ENN, BST, FFY, PRX, GAU, T1E, REN, THE, HLF, PBL, REA, ZAP, TAE, OPS, ZPH, PLM |
| IFE | 11 | OEC, GNF, INE, XCM, FOC, COR, HB1, MVL, FLF, INT, SON |
| MIF | 4 | HEL, GFU, NST, PAC |
| Estatic | 2 | EMC, AVL |
| Other | 3 | LPP, ACC, SHI |

### By Fuel

| Fuel | Count | Concepts |
|---|---|---|
| D-T | 27 | CFS, ESN, TKE, BST, FFY, PRX, GAU, T1E, REN, THE, HLF, REA, ZAP, OPS, OEC, GNF, INE, XCM, FOC, FLF, INT, GFU, PAC, EMC, AVL, ACC, SHI |
| D-D | 4 | PLM, COR, SON, NST |
| D-He3 | 2 | ZPH, HEL |
| p-B11 | 6 | ENN, PBL, TAE, HB1, MVL, LPP |

### By Driver Type

| Driver Type | Count | Concepts |
|---|---|---|
| Magnetic | 18 | CFS, ESN, TKE, ENN, BST, FFY, PRX, GAU, T1E, REN, THE, HLF, PBL, REA, TAE, OPS, ZPH, HEL |
| Magnetic pinch | 3 | ZAP, PAC, LPP |
| DPSSL Laser | 7 | OEC, GNF, INE, FOC, COR, HB1, MVL |
| Gas Laser | 1 | XCM |
| Ion/particle beam | 2 | INT, SHI |
| Mechanical/kinetic | 3 | FLF, GFU, NST |
| Electrostatic | 2 | EMC, AVL |
| Other | 2 | SON, ACC |
| TBD | 1 | PLM |

### By Blanket Config

| Blanket Config | Count | Concepts |
|---|---|---|
| Liquid metal | 14 | TKE, PRX, GAU, THE, HLF, REA, ZAP, OEC, GNF, INE, FOC, FLF, INT, GFU |
| Molten salt | 2 | CFS, XCM |
| Solid breeder | 2 | T1E, OPS |
| Other/hybrid | 2 | REN, HEL |
| N/A (no tritium) | 10 | ENN, PBL, TAE, ZPH, PLM, COR, HB1, MVL, SON, LPP |
| N/A (non-power) | 1 | SHI |
| TBD | 8 | ESN, BST, FFY, NST, PAC, EMC, AVL, ACC |

### By Operation Mode

| Operation Mode | Count | Concepts |
|---|---|---|
| Steady-state | 16 | ESN, PRX, GAU, T1E, REN, THE, HLF, PBL, REA, TAE, ZPH, PLM, EMC, AVL, ACC, SHI |
| Quasi-steady | 6 | CFS, TKE, ENN, BST, FFY, OPS |
| Pulsed | 17 | ZAP, OEC, GNF, INE, XCM, FOC, COR, HB1, MVL, FLF, INT, SON, HEL, GFU, NST, PAC, LPP |

### Concept code legend

| Code | Company / Concept |
|---|---|
| CFS | Commonwealth |
| ESN | Energy Singularity |
| TKE | Tokamak Energy |
| ENN | ENN Energy |
| BST | BEST / Neo Fusion |
| FFY | Firefly |
| PRX | Proxima |
| GAU | Gauss |
| T1E | Type One |
| REN | Renaissance |
| THE | Thea |
| HLF | Helical Fusion |
| PBL | Pale Blue (p-B11) |
| REA | Realta (D-T) |
| ZAP | Zap Energy |
| TAE | TAE Technologies |
| OPS | OpenStar |
| ZPH | Zephyr |
| PLM | PoloMac / Deutelio |
| OEC | Blue Laser Fusion |
| GNF | GenF Systems |
| INE | Inertia Enterprises |
| XCM | Xcimer |
| FOC | Focused Energy |
| COR | Cortex |
| HB1 | HB11 Energy |
| MVL | Marvel |
| FLF | First Light |
| INT | Intensity Energy |
| SON | Sonofusion |
| HEL | Helion |
| GFU | General Fusion |
| NST | NearStar |
| PAC | Pacific Fusion |
| EMC | EMC2 (Polywell) |
| AVL | Avalanche |
| LPP | LPPFusion |
| ACC | Acceleron |
| SHI | SHINE |
