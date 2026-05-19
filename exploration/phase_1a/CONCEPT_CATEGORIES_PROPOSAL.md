# Fusion Concept Category Revisions

**Status**: proposal — not yet reflected in seed CSV, table.csv, or dossier directories
**Author**: Mallory Snowden
**Date**: 2026-05-08
**Companion document**: [SCHEMA_REVISION_PROPOSALS.md](SCHEMA_REVISION_PROPOSALS.md) (taxonomy column revisions)

## Context

Audit of the 36-concept seed list ([initial-fusion-concepts.csv](../context/initial-fusion-concepts.csv)) and corresponding dossiers in [knowledge/concept_research/](../../knowledge/concept_research/) surfaced:

1. **Multi-company rows produce confused syntheses.** The dossier-writing pipeline assumes one concept = one architecture. When a row lumps two materially different companies, the controlled-vocabulary value is forced to fit one or the other, and the Notes fields end up flagging the conflict instead of resolving it. Several concepts in the current seed exhibit this (concepts 7, 17, 22, 26).
2. **Some splits were planned but not executed.** The 0.2.2 schema changelog at [schema.md:339](schema.md#L339) on 2026-03-08 documented row restructuring intents for concepts 17, 23, and 26 — only concept 23 fully shipped. Concept 26 was supposed to drop to Inertia-only with Xcimer moving to a hybrid-drive row; in fact concept 26 still lists both companies in [table.csv:26](table.csv#L26).
3. **Some concepts have insufficient data to be informative** (Pranos Fusion / concept 34).
4. **Some companies are out of scope** for fusion-tea's commercial-fusion focus (Fuse Energy's Apeiron I is fusion-fission hybrid, fundamentally different cost/regulatory profile).

This document captures the proposed concept-list revisions and the implementation cost of each.

---

## Summary of changes

| Action | Affected concepts |
|---|---|
| Remove (insufficient data) | 34 (Pranos / Compact Spherical Tokamak - India) |
| Remove company from row (out of scope) | 7 (drop Fuse Energy → Pacific Fusion only) |
| Split into two peer concepts (different confinement families) | 22 (FLF) + new 37 (NearStar) — peers, not sub-categories |
| Reorganize Inertia / Xcimer / Focused Energy | 17 → Focused Energy only; 26 → Xcimer only (renamed); 30 → Inertia only (absorbs 26's Inertia content) |
| Formalize a/b sub-categorization | 20a/20b (Type One / Renaissance) — both modular HTS stellarators; sub-categorization legitimate |
| Add new concepts | 38 SHINE Technologies (particle-accelerator D-T); 39 ENN Energy (spheromak p-B11) |

### Numbering convention

- **Sequential numbering** (e.g., 37, 38, 39) is used when concepts are independent peers — different confinement families, different fuels, different architectures.
- **`a`/`b` suffix** (e.g., 20a/20b) is used only when two concepts share a real parent concept and warrant sub-categorization. Currently this only applies to 20a/20b (both modular HTS stellarators with shared physics premise; differentiated by manufacturing approach and blanket architecture).
- FLF (IFE projectile) and NearStar (MIF magnetized target) cross confinement families and are therefore peers, not sub-categories. Concept 22 keeps the original number (FLF retains the "Projectile ICF" framing); NearStar gets a new sequential number (37).

**Net concept count**: 36 → 39 (+1 from 22 split into peer concepts, −1 from PRANOS removal, +1 from formalizing 20a/20b in CSV, +2 from SHINE and ENN additions; 26/30 swap-and-merge nets zero — the 26 row survives as Xcimer-only).

---

## Updated concept table

| # | Concept Name | Company | Fuel | Status |
|---|---|---|---|---|
| 01 | HTS Compact Tokamak | Commonwealth Fusion Systems | D-T | unchanged |
| 02 | Acoustic ICF / Sonofusion | Sonofusion Energy | D-D | unchanged |
| 03 | Laser ICF - Liquid Jet Target | Cortex Fusion | D-D | unchanged |
| 04 | Laser ICF (p-B11) | HB11 Energy | p-B11 | unchanged |
| 05 | Planar Coil Stellarator | Thea Energy | D-T | unchanged |
| 06 | Magnetic Mirror (p-B11) | Pale Blue | p-B11 | unchanged |
| 07 | MagLIF | Pacific Fusion | D-T | **Fuse Energy removed (out of scope)** |
| 08 | FRC w/ Direct Conversion | Helion Energy | D-He3 | unchanged |
| 09 | QI Stellarator - HTS | Proxima Fusion | D-T | unchanged |
| 10 | Large-Scale Stellarator | Gauss Fusion | D-T | unchanged |
| 11 | Magnetic Mirror (D-T) | Realta Fusion | D-T | unchanged |
| 12 | Levitated Dipole | OpenStar Technologies | D-T | unchanged |
| 13 | Electrostatic Hybrid | Avalanche Energy | D-T | unchanged |
| 14 | MTF - Pneumatic Compression | General Fusion | D-T | unchanged |
| 15 | Sheared-Flow Stabilized Z-Pinch | Zap Energy | D-T | unchanged |
| 16 | Muon-Catalyzed Fusion | Acceleron Fusion | D-T | unchanged |
| 17 | Laser ICF - Direct Drive (Fast Ignition) | Focused Energy | D-T | **Xcimer removed (moved to 26)** |
| 18 | p-B11 FRC | TAE Technologies | p-B11 | unchanged |
| 19 | Orbital Levitated Dipole | Zephyr Fusion | D-He3 | unchanged |
| 20a | Modular HTS Stellarator (QI / Infinity Two) | Type One Energy | D-T | **formalize existing dossier split** |
| 20b | Modular HTS Stellarator (laser-patterned, liquid wall) | Renaissance Fusion | D-T | **formalize existing dossier split** |
| 21 | Spherical Tokamak - HTS | Tokamak Energy | D-T | unchanged |
| 22 | Projectile ICF | First Light Fusion | D-T | **NearStar removed → new concept 37** |
| 23 | Laser ICF - Nanostructured Target | Marvel Fusion | p-B11 | unchanged |
| 24 | Dense Plasma Focus | LPPFusion | p-B11 | unchanged |
| 25 | Heavy Ion Beam ICF | Intensity Energy | D-T | unchanged |
| 26 | Laser ICF - Hybrid Direct Drive | Xcimer Energy | D-T | **renamed (was "Indirect Drive"); Inertia content moved to 30** |
| 27 | Polywell | EMC2 | D-T | unchanged |
| 28 | HTS Tokamak - Full HTS | Energy Singularity | D-T | unchanged |
| 29 | Negative Triangularity Tokamak | Firefly Fusion | D-T | unchanged |
| 30 | Laser ICF - Indirect Drive | Inertia Enterprises | D-T | **absorbs Inertia content from 26; rename — drop "NIF Commercialization" framing** |
| 31 | Laser ICF - OEC Architecture | Blue Laser Fusion | D-T | unchanged |
| 32 | Laser ICF - French National | GenF Systems | D-T | unchanged |
| 33 | State-Backed Tokamak BEST | Neo Fusion | D-T | unchanged |
| ~~34~~ | ~~Compact Spherical Tokamak - India~~ | ~~Pranos Fusion~~ | ~~D-T~~ | **REMOVED — insufficient data** |
| 35 | PoloMac Magnetic Confinement | Deutelio | (unspecified) | unchanged |
| 36 | Helical Coil Stellarator | Helical Fusion | D-T | unchanged |
| 37 | Magnetized Target Inertial Fusion (MTIF) | NearStar Fusion | D-D | **new concept — peer-split from 22** |
| 38 | Particle Accelerator-Driven Fusion | SHINE Technologies | D-T | **new concept** |
| 39 | Spherical Tokamak (CS-free, p-B11) | ENN Energy | p-B11 | **new concept** |

---

## Detail — Concept 22 split (FLF / NearStar)

The pre-split concept 22 ("Projectile ICF", First Light Fusion + NearStar Fusion) lumps two architectures that differ on every taxonomy axis except Confinement Family — and the existing dossier explicitly flags the lumping as wrong ([22-projectile-icf/dossier.md:18](../../knowledge/concept_research/22-projectile-icf/dossier.md#L18): "NearStar may warrant reclassification to a separate MIF concept row").

The two get **separate sequential concept numbers** (22 for FLF, 37 for NearStar) rather than `a`/`b` suffixes, because they cross confinement families (IFE vs MIF) and share no parent concept. The `a`/`b` convention is reserved for cases like 20a/20b where two concepts share a real parent.

### 22 — Projectile ICF (First Light Fusion)

| Aspect | Value |
|---|---|
| Confinement Family | IFE |
| Confinement Concept | Projectile ICF |
| Fuel | D-T |
| Driver | Electromagnetic launcher (>70 km/s) |
| Target | Multi-cavity amplifier; pressures to 10 TPa |
| Energy Capture | Thermal (steam) — Rankine cycle |
| Tritium Breeding / Wall | Liquid Li curtains, TBR=1.8 (independently validated by TUV SUD UK Feb 2026); 1m flowing curtains serve as combined breeder/shield |
| Operation Mode | Pulsed, sub-Hz (~0.033 Hz at 150 MW pilot; 0.1 Hz at 500 MW plant) |
| Magnet Type | None (under revised vocabulary per SCHEMA_REVISION_PROPOSALS P4) — projectile launcher contains coils, but they confine the projectile, not plasma |

Sources: First Light Fusion technology page (firstlightfusion.com), TUV SUD UK validation (Feb 2026).

### 37 — Magnetized Target Inertial Fusion / MTIF (NearStar Fusion)

| Aspect | Value |
|---|---|
| Confinement Family | **MIF** (not IFE) — fuel is magnetized during compression |
| Confinement Concept | Magnetized target (mechanical) — railgun-driven |
| Fuel | D-D primary; D-T as backup |
| Driver | Plasma armature railgun (~10 km/s) |
| Target | Magnetized fuel; molten lead first wall |
| Energy Capture | Thermal (cycle TBD) — "retrofit the heat source in traditional hydrocarbon power plants" |
| Tritium Breeding / Wall | Not specified for D-D primary; molten Pb proposed for first wall neutron protection |
| Operation Mode | Pulsed (rep rate undisclosed) |
| Magnet Type | None for plasma confinement; the railgun magnetizes the fuel itself (a distinct subsystem) |

Sources: NearStar website, plus reclassification flagged in current concept 22 dossier Notes.

### Why split

Every dossier column has different values between the two:

| Column | FLF | NearStar |
|---|---|---|
| Confinement Family | IFE | MIF |
| Confinement Concept | Projectile ICF | Magnetized target ICF |
| Fuel | D-T | D-D |
| Driver velocity | >70 km/s | ~10 km/s |
| First wall material | Flowing liquid Li | Molten Pb |
| Tritium breeding | TBR=1.8 (validated) | Unspecified |
| Magnetization | No | Yes (fuel magnetized) |

A single row cannot represent both without forcing every controlled-vocabulary value to lie about one of them.

---

## Detail — Concept 7 (MagLIF) — Fuse Energy out of scope

The pre-revision concept 7 lumps Pacific Fusion with Fuse Energy Technologies (which itself was substituted for "Europa Fusion" in the original CSV — likely a confusion with EUROfusion / F4E per [07-maglif/dossier.md:8](../../knowledge/concept_research/07-maglif/dossier.md#L8)).

**Reason for removing Fuse Energy**: their flagship design (Apeiron I) is a **fusion-fission hybrid** — MagLIF neutrons drive fission in a uranium / spent-fuel blanket, amplifying ~20 MW fusion to ~3 GW thermal ([07-maglif/dossier.md:10](../../knowledge/concept_research/07-maglif/dossier.md#L10)). This is not pure fusion. Cost-modeling assumptions (uranium blanket inventory, fission product handling, regulatory profile) are different in kind from any other concept on the list.

**Result**: concept 7 → Pacific Fusion only. Fuse Energy may warrant its own row if and when fusion-fission hybrids are considered in scope; for now, out of scope.

This also enables the Pacific-Fusion-specific magnet correction (Magnet Type → `None`) per [SCHEMA_REVISION_PROPOSALS.md P5](SCHEMA_REVISION_PROPOSALS.md), which would otherwise have been muddied by Fuse Energy's different driver subsystem.

---

## Detail — Concepts 17, 26, 30 (Xcimer / Inertia / Focused Energy)

The 0.2.2 schema changelog at [schema.md:339](schema.md#L339) documented:
> Row restructuring: concept 17 split (Xcimer → hybrid drive, Focused Energy → fast ignition); concept 23 split (Marvel-only, HB11 stays in concept 04); concept 26 now Inertia-only (Xcimer → hybrid drive row)

Only concept 23 fully shipped. Concepts 17 and 26 still lump multiple companies in [table.csv](table.csv).

### Resolution under this proposal

| Concept | Was | Becomes |
|---|---|---|
| 17 | Laser ICF - Direct Drive (**Xcimer + Focused Energy**) | Laser ICF - Direct Drive (Fast Ignition) — **Focused Energy only** |
| 26 | Laser ICF - Indirect Drive (**Inertia + Xcimer**) | Laser ICF - Hybrid Direct Drive — **Xcimer only** (renamed) |
| 30 | Laser ICF - NIF Commercialization (Inertia only) | Laser ICF - Indirect Drive — **Inertia only**, absorbs concept 26's Inertia content |

### Why this assignment

- **Xcimer's Hybrid Direct Drive (HDD)** is its own architecture — first laser pulse heats a hohlraum to generate X-rays that ablate the capsule and form a thick plasma atmosphere; subsequent pulses drive the capsule directly through this atmosphere ([Physics of Plasmas 31(11), 112708 (2024)](https://doi.org/10.1063/5.0223125)). The 0.2.2 schema added `Laser ICF (hybrid drive)` specifically for this. Xcimer should sit in concept 26 alone, with concept 26 renamed to reflect HDD.
- **Inertia Enterprises** is purely indirect-drive following NIF's Hybrid-E target heritage. Concept 30's existing dossier already covers this. Absorb concept 26's Inertia content (Thunderwall DPSSL) into concept 30's row, since they describe the same architecture.
- **Focused Energy** is fast-ignition direct drive. Concept 17 cleanly trims to Focused Energy alone.

The Xcimer dossier note in [26-laser-icf-indirect-drive/dossier.md:24](../../knowledge/concept_research/26-laser-icf-indirect-drive/dossier.md#L24) already acknowledges this: "Xcimer has evolved toward Hybrid Direct Drive (HDD) per their Physics of Plasmas publication … this may warrant reclassification in a future schema revision."

---

## Detail — Concept 34 (PRANOS) removal

| Aspect | Status |
|---|---|
| Original Selection Status | "Not Selected" in [Initial Fusion Concept Candidates.csv](../../modeling_project/intent/Initial%20Fusion%20Concept%20Candidates.csv) |
| Selection Justification | (empty in source CSV) |
| Confinement geometry | Already represented by concept 21 (Tokamak Energy spherical tokamak HTS) and concept 28 (Energy Singularity full-HTS tokamak) |
| Distinguishing feature | Geographic/political (Indian state-backed) — not a physics distinction |

Removing PRANOS does not lose any axis of the comparison set. Concept 33 (Neo Fusion / BEST) provides the state-backed comparator; concepts 21/28 provide the spherical and full-HTS tokamak variants.

---

## Detail — Concepts 20a / 20b (Type One / Renaissance)

These dossiers already exist as separate directories ([20a-type-one-stellarator](../../knowledge/concept_research/20a-type-one-stellarator/), [20b-renaissance-stellarator](../../knowledge/concept_research/20b-renaissance-stellarator/)) but the seed CSV and table.csv still carry only "concept 20: Modular HTS Stellarator (Type One Energy, Renaissance Fusion)". This proposal formalizes the split in the upstream sources.

The split is well-justified:
- **Type One Energy (Infinity Two)**: QI optimization, conventional stellarator coils, FLiBe blanket, HCPB development path
- **Renaissance Fusion**: laser-patterned HTS film on cylinders (novel manufacturing), Li-LiH liquid metal wall + Pb pebble multiplier (per [SCHEMA_REVISION_PROPOSALS P6](SCHEMA_REVISION_PROPOSALS.md))

Magnet Type, Tritium Breeding, and Driver Technology all differ between the two.

---

## Detail — Concept 38 (SHINE Technologies) — new

| Aspect | Value |
|---|---|
| Confinement Family | Electrostatic (or "Other" — particle accelerator-driven beam-target reactions don't fit cleanly in the MFE/IFE/MIF triad) |
| Confinement Concept | Particle accelerator-driven beam-target |
| Fuel | D-T |
| Driver | High-current particle accelerator → beam-on-target reactions |
| Energy Capture | N/A (current operations are non-power; medical isotope and materials irradiation focus). Future power variant TBD. |
| Tritium Breeding | N/A (non-power) |
| Operation Mode | Continuous (accelerator-driven) |
| Magnet Type | None (or N/A) |
| Funding | $1B total ([TechCrunch April 2026](https://techcrunch.com/2026/04/10/every-fusion-startup-that-has-raised-over-100m/)); $240M most recent (Feb 2026) |
| Status | Operating since 2010; demonstrated commercial neutron production for medical isotopes (Mo-99) |

### Why include

- **Demonstrated progress**: SHINE has been producing commercial fusion neutrons at scale for years. Of all companies on the list, this is one of the strongest "demonstrated progress" cases.
- **Schema already cites SHINE** at [schema.md:306](schema.md#L306) as the canonical example for `Electrostatic grid (IEC)` driver technology, but they were never added to the concept set.
- **Cost-modeling caveat**: SHINE's current revenue model is medical-isotope sales, not electricity. They don't have an LCOE in the conventional sense. Either model the future power-plant variant (significant uncertainty) or flag as `N/A (non-power)` for the comparison axes.

### Recommended implementation: pipeline re-run

No existing concept_research dossier exists. Add a new row to the seed CSV and invoke `run_concept.py --concept shine-technologies --cycles 2`.

---

## Detail — Concept 39 (ENN Energy) — new

| Aspect | Value |
|---|---|
| Confinement Family | MFE |
| Confinement Concept | **Spherical tokamak** (CS-free, ECRH-driven non-inductive current drive) |
| Fuel | p-B11 |
| Driver / Heating | ECRH (electron cyclotron resonance heating) — non-inductive current drive replaces conventional central solenoid startup |
| Energy Capture | Direct (charged particle) — implied by p-B11 |
| Tritium Breeding | N/A (no tritium in fuel cycle, per revised P3 vocabulary) |
| Operation Mode | Quasi-steady (EXL-50U sustained 1.2 T for "several seconds"; EHL-2 targets longer pulses) |
| Magnet Type | Resistive or LTS for EXL-50U; HTS proposed for production reactor (per ENN's own roadmap) |
| Status | EXL-50 commissioned 2019; EXL-50U first plasma Jan 2024 (1 MA, 1.2 T); EHL-2 targeted for 2027 (3 MA target) |
| Funding | $400M (per Fusion Energy Base) |

### Why include

- **Distinct combination not covered elsewhere**: spherical tokamak + p-B11 fuel + CS-free operation. No other concept on the list combines spherical tokamak geometry with aneutronic fuel. Concept 21 (Tokamak Energy) is spherical tokamak D-T; concepts 04 / 23 / 24 are p-B11 but use ICF / DPF / nanostructured-laser approaches, not magnetic confinement.
- **Demonstrated progress**: EXL-50U achieved 1 MA plasma with 1.2 T sustained field as of Jan 2024 — operational milestones, not just paper proposals.
- **Significant resources**: $400M direct fusion-program funding via parent gas company; ENN's "ENN's roadmap for proton-boron fusion based on spherical torus" published in Physics of Plasmas 31(6), 062507 (2024).

### Recommended implementation: pipeline re-run

No existing concept_research dossier exists. Add new row, invoke `run_concept.py --concept enn-energy-spherical-tokamak --cycles 2`. **Note**: English-language sources for ENN's fusion program may be limited; budget for additional research iterations to cover Chinese-language press releases and the ENN research site (en.ennresearch.com/researchfield/Compactfusion/).

---

## Implementation cost per change

The 20a/20b split was done **manually** — the iteration directories ([20a/iter-01/](../../knowledge/concept_research/20a-type-one-stellarator/iter-01/), [20b/iter-01/](../../knowledge/concept_research/20b-renaissance-stellarator/iter-01/)) contain only `sources/` subdirectories, not the `prompt.md` / `output.md` / `synthesis_prompt.md` artifacts that [run_concept.py:351-374](scripts/run_concept.py#L351) writes when the pipeline is actually invoked. The split was an editorial partition of the original concept 20 dossier, not a fresh research+synthesis cycle.

For the new splits proposed here, the choice is:

| Approach | What it does | Cost | When to use |
|---|---|---|---|
| **Manual partition** | Copy existing dossier, prune to one company, fix Notes | ~30 min editing per split | When source content is already adequately company-specific in the existing dossier |
| **Pipeline re-run** | Add new row to seed CSV, invoke `run_concept.py --concept <slug> --cycles 2` | ~$2-5 of `claude -p` invocations + 10-15 min wall time per concept | When the existing dossier has glaring gaps for the new isolated concept |

### Per-split recommendation

| Split | Recommended approach | Rationale |
|---|---|---|
| 22 (FLF only) | Manual partition | Existing dossier has substantial FLF-specific content (electromagnetic launcher, liquid Li wall, TBR=1.8, TUV SUD validation) |
| 37 (NearStar) | **Pipeline re-run** | NearStar's confinement family flips IFE → MIF; magnet field flips None → fuel-magnetized; fuel flips D-T → D-D primary. Fresh synthesis is warranted; fully separate dossier. |
| 26 (Xcimer-only HDD) | **Pipeline re-run** | The Hybrid Direct Drive physics is the most recent and least comprehensively researched aspect of concept 26's existing dossier. Re-run will pull the 2024 Physics of Plasmas paper and Phoenix laser hardware coverage. |
| 30 (Inertia-only, absorbs 26 content) | Manual partition | Both source dossiers (concept 26 and concept 30) already cover Inertia's Thunderwall/Hybrid-E story. Editorial merge is sufficient. |
| 17 (Focused Energy alone) | Manual partition | Trim Xcimer content; Focused Energy material remains intact. |
| 7 (Pacific Fusion only) | Manual partition | Trim Fuse Energy content; Pacific Fusion material remains intact. |
| 20a / 20b | Already done (manual) | Existing state suffices. |
| 34 (remove) | Delete | Drop the row and (optionally) archive the dossier directory. |
| 38 (SHINE — new) | **Pipeline re-run** | New concept; no prior dossier exists. |
| 39 (ENN — new) | **Pipeline re-run** | New concept; no prior dossier exists. Budget extra iterations for Chinese-language source coverage. |

---

## Implementation steps (for when ready)

1. **Update seed CSV** ([exploration/context/initial-fusion-concepts.csv](../context/initial-fusion-concepts.csv)) — remove PRANOS row; trim concept 22 to FLF only; add new rows for concept 37 (NearStar), 38 (SHINE), 39 (ENN); update concept 7 / 17 / 26 / 30 names and company columns; add 20a/20b rows (or restructure 20).
2. **Update table.csv** ([exploration/phase_1a/table.csv](table.csv)) — corresponding changes; remove the 0.2.2 changelog inconsistency.
3. **Update citations.csv** — same as above.
4. **Run pipeline re-runs** — for new dossiers (37 NearStar, 38 SHINE, 39 ENN) and reorganized concept 26 (Xcimer-only HDD). Capture new dossiers under `knowledge/concept_research/37-nearstar-mtif/`, `knowledge/concept_research/38-shine-technologies/`, `knowledge/concept_research/39-enn-energy-spheromak/`, `knowledge/concept_research/26-laser-icf-hybrid-direct-drive/` (or similar slugs).
5. **Manual partitions** — for concept 22 (trim NearStar out, leave FLF), 30 (absorb Inertia content from 26), 17 (trim Xcimer out), 7 (trim Fuse out). Edit existing dossiers; preserve Notes content where it survives the pruning.
6. **Update concept_explorer registry** ([exploration/concept_explorer/data/concept_registry.json](../concept_explorer/data/concept_registry.json)) — add rows for 37, 38, 39; remove PRANOS row.
7. **Update concept_explorer per-concept JSONs** ([exploration/concept_explorer/data/](../concept_explorer/data/)) — generate new files for 37, 38, 39; update reorganized concepts; remove PRANOS file.
8. **Re-run downstream Stage 2 cost analyses** for any of the changed concepts that have existing analyses in [exploration/concept_analysis/analyses/](../concept_analysis/analyses/).
9. **Update schema changelog** at [schema.md:333-340](schema.md#L333) with a 0.3.0 entry capturing this concept-list revision.

---

## Open questions

1. **PRANOS dossier disposition**: delete the directory, or move to an `archive/` subdirectory in case the concept becomes researchable later? The dossier holds some research even if not enough for cost modeling.

2. **Fuse Energy re-introduction policy**: if/when fusion-fission hybrids become in scope, Fuse Energy's Apeiron I is the canonical example. Worth a one-line note in the schema about the scope decision.

3. **20a/20b naming**: the current 20a directory dossier title is "QI Modular HTS Stellarator — Infinity Two (D-T)" while 20b is "Compact Liquid-Wall HTS Stellarator (D-T)". Should the seed CSV / table.csv concept names follow the dossier titles, or stay generic ("Modular HTS Stellarator")?

4. **Concept 37 (NearStar) naming**: NearStar's approach is variously called "MTIF" (Magnetized Target Inertial Fusion) and "magnetized projectile" depending on source. If MTIF, that name should be adopted in `Confinement Concept` taxonomy.

5. **SHINE classification under revised schema**: Once neutron management and plasma state are eliminated per [SCHEMA_REVISION_PROPOSALS.md](SCHEMA_REVISION_PROPOSALS.md), SHINE's accelerator-driven beam-target reactions still fit awkwardly under the schema's MFE/IFE/MIF/Electrostatic/Other family taxonomy. Likely `Other` family with custom Confinement Concept value. Confirm during re-run.

6. **ENN classification**: ENN is a spherical tokamak (per [Physics of Plasmas 31(6), 062507 (2024)](https://pubs.aip.org/aip/pop/article/31/6/062507/3297400/) and ENN's own materials), not a spheromak as some external sources (Wikipedia) report. Schema's existing `Spherical tokamak` vocabulary value covers it; the distinguishing physics (CS-free, ECRH-driven, p-B11) lives in Driver Technology + Fuel + dossier Notes.

7. **Whether to do Schema Revision and Concept Revision changes together or sequentially**: doing both in one pass means the dossiers being re-edited can apply the new column vocabulary in one go. Doing them sequentially is lower-risk but means Stage 1 dossiers will be touched twice. Recommendation: do them together, treating the schema bump (0.3.0) and concept list as a single coordinated change.

8. **Coverage gap audit**: 7 existing concepts (02 Sonofusion, 06 Pale Blue, 19 Zephyr, 25 Intensity Energy, 29 Firefly, 32 GenF Systems, 33 Neo Fusion/BEST) do not appear on Wikipedia's [List of nuclear fusion companies](https://en.wikipedia.org/wiki/List_of_nuclear_fusion_companies). Worth applying the same "insufficient data" audit that justified PRANOS removal. Some may still be in scope (e.g., Neo Fusion as a state program with significant resources despite not being VC-tracked).
