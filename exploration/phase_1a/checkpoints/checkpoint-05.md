# Checkpoint 5: Laser & Non-Laser IFE

**Date**: 2026-03-07
**Concepts integrated**: Laser ICF - Direct Drive (D-T), Laser ICF - Indirect Drive (D-T), Laser ICF - NIF Commercialization (D-T), Laser ICF - OEC Architecture (D-T), Laser ICF - French National Direct Drive (D-T), Laser ICF - Liquid Jet Target (D-D), Laser ICF - p-B11 Fast Ignition, Laser ICF - Nanostructured Target (p-B11), Projectile ICF (D-T), Heavy Ion Beam ICF (D-T)
**Total concepts in table**: 31

## Table Status
- Cells filled: 351 / 384 (91.4%) — counting all 12 differentiation columns x 31 concepts, excluding N/A, TBD, and Unknown
- Cells N/A: 23
- Cells TBD/Unknown: 10 (7 TBD, 2 Unknown, 1 TBD in new batch)
- High-confidence cells: ~275 (~78% of filled) — approximate; exact count requires parsing all 372 citation rows

## Consistency Issues Found

### Vocabulary Mismatches

1. **Cortex Fusion — Neutron Management: `Heavy shielding (14 MeV)` for D-D concept.** D-D fusion produces 2.45 MeV neutrons, not 14.1 MeV. The schema value `Heavy shielding (14 MeV)` explicitly references D-T neutrons. No schema vocabulary exists for heavy shielding of 2.45 MeV D-D neutrons at high flux. The dossier correctly notes this but applies the closest available value. **Action**: Consider adding a schema value like `Heavy shielding (D-D)` or `Heavy shielding (2.45 MeV)` for D-D concepts with significant neutron flux.

   **UPDATE (2026-03-08)**: Resolved. Added `Heavy shielding (D-D)` to schema v0.2.3. Updated 3 D-D concept cells (Cortex Fusion, Sonofusion, PoloMac) from `Heavy shielding (14 MeV)` to `Heavy shielding (D-D)`.

2. **Cortex Fusion — Plasma State: `Compressed` at low confidence.** The dossier explicitly states the mechanism is non-implosion plasmonic acceleration at constant density (isochoric heating), not compression. `Compressed` is the best schema fit for IFE but is a poor description of the actual physics. No schema vocabulary captures "non-thermal laser acceleration at constant density." **Action**: Flag for schema review — may need a new value or schema note.

3. **Cortex Fusion — Tritium Breeding: `N/A (aneutronic)` for D-D fuel.** Schema explicitly lists D-D under this value ("p-B11 and pure D-D concepts"), so the vocabulary use is correct per schema. However, D-D is NOT aneutronic — 50% of reactions produce neutrons. The parenthetical "(aneutronic)" is misleading for D-D. **Action**: Consider renaming to `N/A (no tritium needed)` to cover D-D without implying aneutronic.

   **UPDATE (2026-03-08)**: Resolved. Renamed `N/A (aneutronic)` → `N/A (no tritium in fuel cycle)` in schema v0.2.3. Updated all 9 affected cells (5 p-B11 + 3 D-D + 1 D-He3) in table and citations.

### Within-Row Divergence (Multi-Company Concept Rows)

4. **Laser ICF - Direct Drive (D-T) — Xcimer vs Focused Energy.** Major divergence on:
   - **Repetition Rate**: Sub-Hz (Xcimer) vs ~10 Hz (Focused Energy) — order of magnitude difference
   - **Driver Technology**: KrF excimer (Xcimer) vs DPSSL + petawatt CPA (Focused Energy)
   - **Confinement Concept**: Xcimer is genuine direct drive (HDD variant); Focused Energy uses direct-drive compression + proton fast ignition, straddling `Laser ICF (direct drive)` and `Laser ICF (fast ignition)`
   - **Tritium Breeding**: FLiBe (Xcimer, well-documented) vs Li blanket unspecified (Focused Energy)

   The dossier recommends splitting into two rows. **Action**: Split this row — Xcimer as `Laser ICF (direct drive)` and Focused Energy as `Laser ICF (fast ignition)`.

5. **Laser ICF - Indirect Drive (D-T) — Inertia vs Xcimer.** Divergence on:
   - **Repetition Rate**: ~10 Hz (Inertia) vs Sub-Hz (Xcimer)
   - **Driver Technology**: DPSSL Thunderwall (Inertia) vs KrF excimer (Xcimer)
   - **Tritium Breeding**: Liquid Li (Inertia) vs FLiBe (Xcimer)

   Xcimer's HDD approach is increasingly distinct from NIF-style pure indirect drive. **Action**: Consider whether Xcimer needs its own concept row (potentially `Laser ICF (hybrid drive)`).

6. **Laser ICF - Nanostructured Target (p-B11) — Marvel vs HB11.** Divergence on:
   - **Energy Capture**: Hybrid thermal+direct (Marvel) vs Thermal steam (HB11)
   - **Repetition Rate**: ~10 Hz (Marvel) vs ~1 Hz (HB11)
   - **Driver Technology**: Femtosecond DPSSL on nanostructured Si targets (Marvel) vs multi-laser DPSSL array on foam targets (HB11)

   Less severe than concept 17 — both use ultrashort pulse lasers on p-B11. **Action**: Monitor; splitting may be warranted if the energy capture divergence affects cost modeling.

### Concept Overlap Between Dossiers

7. **Dossiers 26 and 30 substantially overlap.** Both cover Inertia Enterprises with `Laser ICF (indirect drive)`. Dossier 26 also includes Xcimer Energy. The table now has two nearly-identical rows for Inertia's indirect-drive concept:
   - "Laser ICF - Indirect Drive (D-T)" — Inertia + Xcimer, combined
   - "Laser ICF - NIF Commercialization (D-T)" — Inertia only, more specific

   **Action**: Consider merging into one row or retaining only the Inertia-specific row (concept 30) and moving Xcimer to the direct-drive or a hybrid-drive row.

8. **HB11 Energy appears in three concept rows.** Dossier 04 → "Laser ICF - p-B11 Fast Ignition" (HB11 as sole company), Dossier 23 → "Laser ICF - Nanostructured Target" (HB11 + Marvel). These represent different schema classifications (`fast ignition` vs `ultrashort pulse`) applied to the same company. HB11 also appears in the indirect-drive dossier 26 context.

   **Action**: Consolidate. Concept 04 and HB11's portion of concept 23 describe the same company. Recommend keeping concept 04 as HB11's standalone row and concept 23 as Marvel Fusion's standalone row.

9. **Xcimer Energy appears in three concept rows.** Direct Drive (17), Indirect Drive (26), and NIF Commercialization (30). Xcimer's HDD approach genuinely straddles direct and indirect drive.

   **Action**: After resolving overlaps, Xcimer should appear in at most two rows (direct drive + hybrid drive or direct drive only).

### Energy Capture Ambiguity — Xcimer

10. **Xcimer's power cycle is contradictory across sources.** Public website says "steam" but the ASPEN/IFE Workshop 2022 presentation and HYLIFE heritage literature describe a helium Brayton gas turbine at ~45% efficiency. Using `Thermal (unspecified)` or `Thermal (steam)` depending on context. **Action**: Resolve via full HYLIFE-III paper or direct Xcimer contact. Schema may need `Thermal (He Brayton)` vocabulary.

## Schema Assessment

### Columns That May Need Adjustment

- **Plasma State**: Always `Compressed` for all 10 IFE concepts. Does not discriminate within IFE family. Still discriminates between MFE (Burning/Sustained/Pinch), MIF (Compressed/Transient), and IFE (Compressed). Retaining is correct — it discriminates across families.

- **Magnet Type**: Always `None (IFE)` for all 10 IFE concepts. Same reasoning — discriminates across families, not within IFE. Retain.

- **Operation Mode**: Always `Pulsed` for all 10 IFE concepts. Same. Retain.

These three columns are structurally invariant within IFE but provide important cross-family discrimination. No column changes recommended.

### Vocabulary Values to Consider

- **Add `Heavy shielding (D-D)` or `Heavy shielding (2.45 MeV)`**: For D-D concepts with significant neutron flux but lower per-neutron energy than D-T. Currently only Cortex Fusion needs this, so low priority.

- **Add `Thermal (He Brayton)`**: For concepts using helium gas turbine cycle. HYLIFE heritage designs use this. Currently captured as `Thermal (unspecified)` but the specific cycle matters for cost modeling.

- **Consider `Laser ICF (hybrid drive)` confinement concept**: Xcimer's HDD is increasingly distinct from both pure direct drive and pure indirect drive. Schema Column 2 vocabulary doesn't currently include this.

- **Rename `N/A (aneutronic)` for Tritium Breeding**: Current name is misleading for D-D concepts. Suggest `N/A (no tritium in fuel cycle)` to cover both p-B11 (truly aneutronic) and D-D (neutronic but no tritium).

### Schema Stability

**Recommendation**: The schema is stable for the remaining batches. The vocabulary issues identified above are minor — they affect 1-2 cells each and don't block integration. Resolve at the next major schema revision (v0.3) rather than mid-sprint.

## Observations

### IFE Family Patterns

1. **Driver technology is the primary differentiator within IFE.** Unlike MFE where magnet type and confinement concept create the most variation, IFE concepts are differentiated primarily by their driver (laser type, projectile launcher, or ion beam accelerator) and secondarily by target physics (direct vs indirect drive, compression vs non-thermal).

2. **Repetition rate and yield-per-shot are inversely correlated.** Sub-Hz concepts (Xcimer, First Light) compensate with very high yield per shot (gain 100-1000x). ~10 Hz concepts (Inertia, BLF, Marvel, GenF) use lower per-shot energy with higher duty cycle. This trade is fundamental to IFE economics and deserves explicit treatment in Phase 1d.

3. **Blanket choices within D-T IFE cluster around FLiBe and liquid Li.** No IFE concept uses solid ceramic breeders (HCPB) — that's exclusively MFE. Liquid blankets that also serve as first-wall protection are strongly preferred for IFE's pulsed environment (repeated shocks, debris clearing).

4. **p-B11 IFE concepts uniformly claim Thermal (steam) or Hybrid despite aneutronic physics.** This is surprising — aneutronic reactions produce charged particles ideally suited for direct conversion. HB11 explicitly pivoted from direct conversion to steam. Marvel Fusion retains hybrid. TAE (p-B11 FRC, MFE) also uses steam. The steam cycle may be the pragmatic default even for aneutronic concepts.

### Commercial Status Concerns

5. **First Light Fusion pivoted away from projectile ICF** (Sep 2025 → FLARE pulsed-power liner). No active commercial pursuer remains. The row is retained for completeness but this concept is effectively orphaned.

6. **"Intensity Energy" (Heavy Ion Beam ICF) could not be verified** as an existing company despite exhaustive search including FIA 2025 survey of 53 companies. Almost certainly a placeholder. No private company pursues HIF commercially; the concept is characterized entirely from national lab studies (HIBALL, HYLIFE-II, LBNL).

7. **Cortex Fusion Systems has very low confidence overall** (low). Physics case rests on a single theoretical preprint with extraordinary claims (Q~100, 10^19 n/s). No experimental results from the company. $2.6M total funding. The concept is included for completeness but should be flagged as highly speculative.

### Overlap and De-Duplication Needed

8. **The 10 dossiers map to potentially 12-14 distinct concept rows** when company divergences within rows and overlap between rows are resolved. Recommended consolidation:
   - Merge concepts 26 + 30 into one Inertia-focused indirect-drive row
   - Split concept 17 into Xcimer (direct drive) and Focused Energy (fast ignition)
   - Split concept 23 into Marvel Fusion (ultrashort pulse) and HB11 (fast ignition, merge with concept 04)
   - Consider adding a Xcimer "hybrid drive" row

   This would yield a cleaner set with one company per row in most cases. Defer to upstream decision.

**UPDATE (2026-03-08) — Decisions made and implemented:**
- Concepts 26 + 30: **kept separate** (both Inertia indirect drive, but user wants distinct rows)
- Concept 17: **split** — Focused Energy → `Laser ICF (fast ignition)`, Xcimer → new row `Laser ICF (hybrid drive)`
- Concept 23: **split** — Marvel Fusion only (HB11 consolidated into concept 04)
- Concept 26: Xcimer removed → Inertia-only; values individualized (Liquid Li blanket, DPSSL Thunderwall)
- Schema v0.2.2: added `Laser ICF (hybrid drive)` to Column 2 vocabulary
- Table: 32 rows (was 31). Citations: 385 rows (was 372). All affected citations individualized for single-company rows.
