# Checkpoint 1: Batches 1–2 (Tokamaks + Stellarators)

**Date**: 2026-03-07
**Concepts integrated**: 11 (6 tokamaks, 5 stellarators)
**Schema version**: 0.1

---

## Table Status

| Metric | Value |
|--------|-------|
| Total cells (11 concepts × 12 columns) | 132 |
| Cells filled (not TBD/Unknown) | 125 (94.7%) |
| Cells TBD | 5 (3.8%) |
| Cells Unknown | 2 (1.5%) |
| High confidence | 83 (62.9%) |
| Medium confidence | 33 (25.0%) |
| Low confidence | 7 (5.3%) |
| N/A (structural, Repetition Rate) | 11 |
| All rows unique | Yes |

### By Concept Maturity

| Concept | High | Med | Low | TBD/Unk | Assessment |
|---------|------|-----|-----|---------|------------|
| 05 Thea (Planar Stellarator) | 12 | 0 | 0 | 0 | Excellent |
| 01 CFS (HTS Compact Tokamak) | 10 | 1 | 0 | 0 | Excellent |
| 36 Helical Fusion | 10 | 1 | 0 | 0 | Excellent |
| 20 Type One / Renaissance | 7 | 4 | 0 | 0 | Good |
| 33 Neo Fusion (BEST) | 7 | 3 | 0 | 1 | Good |
| 21 Tokamak Energy | 7 | 4 | 0 | 0 | Good |
| 10 Gauss Fusion | 6 | 4 | 0 | 0 | Good |
| 09 Proxima Fusion | 6 | 4 | 0 | 0 | Good |
| 28 Energy Singularity | 6 | 3 | 0 | 1 | Moderate |
| 29 Firefly Fusion | 4 | 4 | 3 | 1 | Moderate-low |
| 34 Pranos Fusion | 3 | 2 | 3 | 3 | Low |

---

## Schema Issues Found

### Issue 1: Concept 20 must be split into two rows

**Severity**: High — actively hiding differentiation

Type One Energy and Renaissance Fusion are lumped into one row but diverge on **6 of 12** engineering columns:

| Column | Type One Energy | Renaissance Fusion |
|--------|----------------|-------------------|
| Primary Heating | ECRH | NNBI |
| Energy Capture | Thermal (steam) / Rankine | Thermal (sCO2) / Brayton-Rankine |
| Magnet Type | Wound HTS tape (9 T) | Laser-patterned HTS film (10-15 T) |
| Tritium Breeding | HCPB solid ceramic (TBR=1.30) | Liquid Li-LiH wall (fm=1.24) |
| Neutron Management | HCPB + backup zones | Liquid metal wall (99.99% absorption) |
| Scale | A=10, R=12.5 m | A~4, R≤4 m |

**Decision**: Split into two rows. Both share `Stellarator (modular)` confinement concept and `MFE`/`D-T`/`Burning`/`Steady-state` physics, but cost-relevant engineering is fundamentally different.

### Issue 2: No schema value for solid ceramic breeders (HCPB)

**Severity**: Medium — forces a misclassification

Type One Energy uses a Helium-Cooled Pebble Bed (HCPB) blanket — a solid ceramic breeder (Li₄SiO₄ or Li₂TiO₃). This is fundamentally different from all liquid breeder options in the schema. Currently forced into `Li blanket (unspecified)`.

**Decision**: Add `Solid ceramic breeder (HCPB)` to Column 8 (Tritium Breeding) vocabulary. This is the ITER TBM baseline and a mainstream blanket concept.

### Issue 3: "Compact tokamak" doesn't fit BEST (R=3.6 m)

**Severity**: Low-Medium — one concept affected

BEST at R=3.6 m is mid-size — nearly 2× SPARC (R=1.85 m) but smaller than ITER (R=6.2 m). The schema has no intermediate value between "Compact tokamak" (which connotes high-field/small) and the existing vocabulary.

**Decision**: Add `Tokamak` as a plain vocabulary value for conventional-scale tokamaks. `Compact tokamak` retains its meaning of high-field-enabled compact design. Reclassify BEST from `Compact tokamak` → `Tokamak`.

### Issue 4: Pulsed vs Quasi-steady boundary is ambiguous for long-pulse tokamaks

**Severity**: Low-Medium — causes inconsistency between concepts 01, 21, 29

CFS (#01) and Tokamak Energy (#21) both operate with ~15-minute burns, but CFS is classified `Quasi-steady` and TE is `Pulsed` (based on company self-description). Firefly (#29) is `Steady-state` from the CSV but the MANTA proxy suggests quasi-steady/pulsed.

Additionally, TE is `Pulsed` but has `N/A` for Repetition Rate — the schema says N/A applies to "Steady-state or quasi-steady," not Pulsed.

**Decision**: Add a clarifying note to the schema: "For pulse lengths > 5 minutes, classify as `Quasi-steady` regardless of company self-description. `Pulsed` is reserved for discrete short events (seconds or less)." This resolves all three cases:
- TE (#21): Pulsed → Quasi-steady (15+ min burns), Rep Rate stays N/A
- CFS (#01): Quasi-steady stays (correct)
- Firefly (#29): Steady-state → Quasi-steady (MANTA proxy = ~15 min)

### Issue 5: Stellarator (QI) vs Stellarator (modular) overlap

**Severity**: Low — categorization ambiguity

Concepts 09 (Proxima), 10 (Gauss), and 20 (Type One/Renaissance) are all QI-optimized and all use modular coils. Proxima and Gauss chose `(QI)`, while 20 chose `(modular)`. The distinction is emphasis (physics vs manufacturing), not a real engineering difference.

**Decision**: No vocabulary change needed. Add a note to the schema: "Use `Stellarator (QI)` when the concept's primary innovation emphasis is the physics optimization. Use `Stellarator (modular)` when the emphasis is on manufacturing/assembly approach (modular coil cassettes)." After splitting concept 20, reassess whether the new Type One row should be `(QI)` or `(modular)`.

### Issue 6: Confidence scale — "medium-high" not in schema

**Severity**: Cosmetic — one concept affected

Dossier 21 (Tokamak Energy) uses `medium-high` confidence, which isn't in the three-level schema (`high`/`medium`/`low`).

**Decision**: Normalize to three levels. `medium-high` → `high` or `medium` based on judgment. No schema change needed — enforce the existing rule.

---

## Column Discrimination Analysis

| # | Column | Unique Values | Assessment |
|---|--------|--------------|------------|
| 1 | Confinement Family | 1 (MFE) | Not discriminating — expected, all MFE batch |
| 2 | Confinement Concept | 7 | Good |
| 3 | Fuel | 1 (D-T) | Not discriminating — expected, all D-T batch |
| 4 | Primary Heating | 4 + 1 TBD | Moderate (ECRH dominates at 64%) |
| 5 | Energy Capture | 3 | Weak — "unspecified" = 55% |
| 6 | Plasma State | 1 (Burning) | Not discriminating — expected, all high-Q |
| 7 | Magnet Type | 4 + 1 Unknown | Good |
| 8 | Tritium Breeding | 5 + 4 TBD | Moderate — good spread but 36% TBD |
| 9 | Neutron Management | 2 | Weak — split correlates with disclosure level |
| 10 | Operation Mode | 3 | Moderate |
| 11 | Repetition Rate | 1 (N/A) | Not discriminating — expected, all MFE |
| 12 | Driver Technology | 11 (all unique) | Maximum discrimination |

**Assessment**: 4 non-discriminating columns (Family, Fuel, Plasma State, Rep Rate) are expected — these will differentiate when IFE/MIF/aneutronic concepts join in Batches 3-6. No columns need removal.

---

## Consistency Issues

### Within-family anomalies

1. **Firefly (#29) Operation Mode = Steady-state at medium confidence**: Contradicted by MANTA proxy (~15 min burns) and co-founder Ball's ohmic-only research (implies inductive/pulsed). Most likely should be Quasi-steady. → Corrected by Issue 4 decision above.

2. **Firefly (#29) Neutron Management = Integrated blanket/shield at low confidence**: Based entirely on MANTA proxy (FLiBe). With no Firefly disclosure, this may over-fit to a proxy. Acceptable given the alternatives, but flag as proxy-derived.

3. **Pranos (#34) has 5 TBD/Unknown/low cells**: This is an accurate reflection of a pre-concept-design company, not a research failure. No re-run needed.

4. **Tokamak Energy (#21) Rep Rate = N/A while Op Mode = Pulsed**: Inconsistent with schema rule. → Resolved by Issue 4 decision (reclassify to Quasi-steady).

### Cross-family observations

- Stellarators are much more internally consistent than tokamaks (6/12 columns identical across all 5). Differentiation concentrates on magnets, blankets, and energy capture.
- Tokamaks span all 3 operation modes — genuine engineering diversity, not error.
- Neutron Management split (Integrated vs Heavy) partly reflects disclosure level, not just engineering. Acceptable for now but integration agent should watch this pattern.

---

## Schema Changes (for v0.2)

### Vocabulary additions

| Column | Add | Rationale |
|--------|-----|-----------|
| 2. Confinement Concept | `Tokamak` | Plain value for conventional/mid-size devices (R > 3 m, not explicitly compact or spherical) |
| 8. Tritium Breeding | `Solid ceramic breeder (HCPB)` | Covers He-cooled pebble bed blankets (ITER TBM, Type One Energy). No existing value fits. |

### Vocabulary clarifications (no new values)

| Column | Clarification |
|--------|---------------|
| 2. Confinement Concept | Add note: `Stellarator (QI)` = physics emphasis; `Stellarator (modular)` = manufacturing emphasis |
| 10. Operation Mode | Add note: pulse lengths > 5 min → `Quasi-steady`, regardless of company self-description. `Pulsed` = discrete short events (seconds or less). |

### Structural changes

| Change | Rationale |
|--------|-----------|
| Split concept 20 into two rows: `20a-type-one-stellarator` and `20b-renaissance-stellarator` | 6/12 columns diverge at engineering level. Composite row hides cost-relevant differentiation. |

---

## Correction Plan

### Concepts requiring re-run after schema v0.2

| Concept | Reason | Action |
|---------|--------|--------|
| **20a (Type One Energy)** | New row from split | Run 1 cycle — dossier data already exists, synthesis agent just needs to extract Type One-specific values |
| **20b (Renaissance Fusion)** | New row from split | Run 1 cycle — dossier data already exists, synthesis agent just needs to extract Renaissance-specific values |
| **21 (Tokamak Energy)** | Op Mode Pulsed → Quasi-steady, normalize confidence scale | Manual edit to dossier (no re-run needed, data is correct) |
| **29 (Firefly)** | Op Mode Steady-state → Quasi-steady | Manual edit to dossier (proxy-based, no new data from re-run) |
| **33 (BEST)** | Confinement Concept Compact tokamak → Tokamak | Manual edit to dossier (no re-run needed) |

### Concepts NOT requiring changes

All other concepts (01, 05, 09, 10, 28, 34, 36) — no corrections needed.

### Execution sequence

1. Update `schema.md` to v0.2 (add vocabulary, add notes)
2. Manual-edit dossiers for concepts 21, 29, 33 (value corrections)
3. Split concept 20 directory and run targeted synthesis for 20a and 20b
4. Proceed to Batch 3

---

## Observations

- **The schema is holding up well.** Only 2 vocabulary additions needed after 11 concepts. No columns need removal or splitting.
- **Information density varies enormously.** CFS and Thea Energy have DOE-certified published designs; Pranos Fusion has almost nothing public. The table correctly reflects this via confidence levels rather than forcing guesses.
- **The composite row problem (concept 20) is the biggest structural issue.** Future batches should watch for this — the CSV may lump companies that should be separate rows.
- **Paywalled papers are the main barrier to higher confidence.** 3 specific papers (Stellaris/Proxima, Gauss CDR, Helical Fusion AIP) would resolve ~8 medium-confidence cells. Worth acquiring if the project needs higher confidence.
