---
date: 2026-05-17
researcher: Claude
topic: "Affected concepts under aggressive availability standardization"
tags: [policy, availability, iteration-backlog]
status: applied
---

# Affected concepts under the aggressive availability policy

Policy: see `exploration/concept_analysis/prompt_templates/config/scoring_framework.md` §"Plant availability".

- **Canonical for D-T MCF steady-state / quasi-steady**: `0.85`
- **Canonical for D-T pulsed (MCF / IFE / MIF)**: `0.75`
- **Justified deviation**: only when an external publication commits to a specific availability with a stated basis (Tier A). Author-reasoned midpoints within published bands (Tier B/C) must move to canonical.

## D-T MCF — steady-state / quasi-steady (canonical 0.85)

| Concept | Current | Action | Rationale |
|---|---|---|---|
| 01-hts-compact-tokamak | 0.75 | **→ 0.85** | Tier C: discretionary low end of A&S band; no published 75% target |
| 05-planar-coil-stellarator | 0.88 | **keep 0.88, document Tier-A deviation** | Helios/Thea published 88% with biennial 84-day maintenance cycle |
| 10-large-scale-stellarator | 0.88 | **keep 0.88, document Tier-A deviation** | Same Helios/Thea source |
| 11-magnetic-mirror | 0.85 | no change | Already canonical |
| 20a-type-one-stellarator | 0.87 | **→ 0.85** | Tier B: "between 85–90% MCF range, shifted toward upper half" — no published target |
| 20b-renaissance | 0.92 | **keep 0.92, document Tier-A deviation** | Renaissance Fusion disclosed; in-file uncertainty flag retained |
| 21-spherical-tokamak-hts | 0.80 | **→ 0.85** | Tier C: pulse-dwell argument cited but no published target |
| 28-hts-tokamak-full-hts | 0.80 | **→ 0.85** | Tier C: no published target for central case |
| 29-negative-triangularity-tokamak | 0.80 | **→ 0.85** | Tier C: MANTA 37% pilot, commercial 75–90% — eyeballed midpoint |
| 33-state-backed-tokamak-best | 0.80 | **→ 0.85** | Tier C: quasi-steady PFPP central case, no published number |
| 34-compact-spherical-tokamak-india | 0.80 | **→ 0.85** | Tier C: no published target |
| 36-helical-coil-stellarator | 0.83 | **→ 0.85** | Tier B: mid-range eyeball within 80–85% FPP target |

## D-T pulsed — MCF / IFE / MIF (canonical 0.75)

| Concept | Current | Action | Rationale |
|---|---|---|---|
| 07-maglif | 0.85 | **→ 0.75** | Tier C: "Z-IFE assumes 85% without explicit attribution" — not a Tier-A cite |
| 14-magnetized-target-fusion-pneumatic-compression | 0.80 | **→ 0.75** | Tier C: midpoint of analogue range, no published target |
| 17a-laser-icf-hybrid | 0.85 | **→ 0.75** | Tier C: no Focused Energy disclosure |
| 17b-laser-icf-fast-ignition | 0.75 | no change | Already canonical |
| 25-heavy-ion-beam-icf | 0.80 | **→ 0.75** | Tier C: no published target |
| 26-laser-icf-indirect-drive | 0.75 | no change | Already canonical |
| 30-laser-icf-nif-commercialization | 0.80 | **→ 0.75** | Tier C: no published commercial target (NIF is single-shot demo, but the modeled plant is commercial) |
| 31-laser-icf-oec | 0.75 | no change | Already canonical |
| 32-laser-icf-french | 0.75 | no change | Already canonical |

## Summary

- **Changes**: 11 concepts move to canonical, 3 keep Tier-A deviation with documentation, 6 already canonical.
- **Of the 11 moves**: 9 MCF go up (`0.75/0.80/0.83/0.87 → 0.85`), 4 pulsed go down (`0.80/0.85 → 0.75`). Net effect: convergence on category canonicals.
- **LCOE impact**: capital-dominated concepts scale LCOE as `1/availability`. Examples:
  - `01` LCOE drops ~12% from availability alone (0.75 → 0.85).
  - `07-maglif` LCOE rises ~13% (0.85 → 0.75).
  - `20a` LCOE rises ~2.4% (0.87 → 0.85).

## Applied changes (2026-05-17)

The standardization was applied script-driven via `exploration/concept_analysis/scripts/standardize_availability.py --apply` rather than the per-concept Claude iteration loop. **13 concepts** were standardized (not 11 — the original survey undercounted by missing `28-hts-tokamak-full-hts`'s 3 scenario-call sites, and `36-helical-coil-stellarator`'s `_AVAILABILITY` constant required a regex update). The 3 Tier-A retains (`05, 10, 20b`) were manually edited to use the `# DEVIATION:` marker template.

### Open follow-ups

1. **Display-string staleness in `model_setup.py` print blocks.** Several concepts hardcode availability percentages in print labels, `extra_note` strings, and scenario-summary tuples (e.g., `28-hts-tokamak-full-hts` lines 308/343/356 still embed `"80% avail"` in `extra_note=` strings; line ~365 lists `0.80` as a display-only tuple element). The computed LCOEs are correct (use the canonical value), but the displayed labels are stale. Manual edit pass needed.

2. **Synthesis prose drift in 13 concepts.** Each affected `synthesis.md` cites the old availability value and old LCOE in prose (e.g., `01/synthesis.md:18` reads "75% availability: $642/MWh"). Refreshing requires re-running the synthesize stage. Either accept short-term drift or schedule a synthesize-only pass.

3. **Concept 09 (qi-stellarator-hts) is partially out of scope.** Pre-marked with `# DEVIATION:` because it has a custom replacement-cost calc tied to `_AVAILABILITY_BASE = 0.88` (line 173) that explicitly "matches _SHARED below". Standardizing only the framework call would create internal drift. Follow-up: update both sites in lockstep to 0.85, or document why 09 should retain 0.88 with a Tier-A rationale.

4. **Concept 20a has secondary capital-side coupling.** Its LCOE delta (+6.4%) exceeds pure 1/avail (+2.4%) because overnight cost shifts ~+3.5% under the new availability. Direction correct, magnitude reasonable, but worth documenting so future audits don't flag it as anomalous.

5. **Non-D-T concepts unchanged.** Policy for D-D / D-³He / p-¹¹B pulsed concepts (`04, 06, 08, 23`) is not yet ratified — the helper currently returns 0.75 for any pulsed family, but `scoring_framework.md` says "Same MCF basis" for non-D-T which would imply 0.85. The script filters to `fuel == "D-T"` and skips these. Resolve as a separate policy pass.

6. **"DEFAULT-label audit" companion script.** With `canonical_availability` and `canonical_eta_th` in place, the recommendation from `.project/research/20260517-081444_model-setup-inconsistencies.md` §2 (audit script flagging silent drift) is now a ~30-line job — recommended follow-up.

## Iteration scope (deprecated — superseded by standardize_availability.py)

11 concepts need a `model_setup.py` edit + a synthesis Section 2 note. The edit pattern:

1. Replace literal `0.XX` (or `AVAILABILITY = 0.XX` constant) with `canonical_availability(family, mode, fuel)` import.
2. Update the in-line comment from "UNCERTAIN: midpoint of range" to "canonical for {category} per scoring_framework.md".
3. For the 3 Tier-A retains, replace the comment with the explicit deviation rationale (quote + source + basis).
4. Re-run that concept's analysis pipeline to refresh LCOE outputs.

Tier-A documentation template:

```python
# DEVIATION from canonical 0.85 (MCF steady-state, D-T).
# Source: <paper/disclosure>, <section>
# Basis: <published maintenance cycle / duty argument>
AVAILABILITY = 0.88
```
