---
date: 2026-05-17T08:14:44-07:00
researcher: Claude
topic: "Inconsistencies across concept model_setup.py files"
tags: [research, concept-analysis, costingfe, traceability]
status: complete
last_updated: 2026-05-17
---

# Research: Inconsistencies across concept `model_setup.py` files

**Research Type**: Codebase audit / cross-concept consistency

## Research Question

Find inconsistencies between the 38 `exploration/concept_analysis/analyses/*/model_setup.py` files — parameters and values that are **common across multiple model setups but use different values across them without principled justification**.

## Summary

- **Two structural classes**: 26 of 38 concepts use the `costingfe` framework; the other 12 are hand-rolled custom cost models that bypass `CostModel.forward()` entirely. Cross-concept comparison is only well-defined for the 26 framework users.
- **The most systemic inconsistency is `inflation_rate`**: 19/20 D-T framework concepts use `0.0245`, while the actual library default is **`0.02`**. The 0.0245 figure propagates from `costingfe/examples/*.py`, is uniformly labeled "DEFAULT" in concept files, and has no sourced rationale. One concept (`11-magnetic-mirror`) uses the true library default — inadvertently making it the outlier.
- **Most outlier values are principled** (sourced design figures, FOAK markers, deliberate scoring-framework standardization to `eta_th=0.35`), but a handful are weakly justified or silently drift from framework defaults: `28-hts-tokamak-full-hts` structure/vessel thicknesses, `34-india` small-plant aux-load scaling, `10-large-scale-stellarator` 10-year construction time.
- **Geometry thickness drift**: framework tokamak defaults are `structure_t=0.20, vessel_t=0.20`, stellarator defaults are `structure_t=0.15, vessel_t=0.10`. Several tokamaks (e.g., 28-hts) silently use stellarator-default thicknesses.
- **`availability` for D-T MFE concepts** spans 0.75–0.92 across nominally similar machines with no consistent principle linking the value to a physics or operations argument.
- **`mn` for D-T concepts**: 16 use 1.1 (framework default), but `20a=1.15`, `20b=1.07`, `29=1.11`, `31=1.0`. Of these, only `31-laser-icf-oec` documents a physics reason (avoiding double-counting Li breeding boost already embedded in `eta_th`).

## Detailed Findings

### 1. Framework users vs. custom models (structural inconsistency)

**26 of 38 concepts** use `costingfe.CostModel(...).forward(**kwargs)`:

`01, 03, 04, 05, 06, 07, 08, 10, 11, 14, 17a, 17b, 20a, 20b, 21, 23, 25, 26, 28, 29, 30, 31, 32, 33, 34, 36`

**12 of 38** roll their own physics + cost model and ignore `costingfe.CostModel`:

`02-acoustic-icf-sonofusion, 09-qi-stellarator-hts, 12-levitated-dipole, 13-electrostatic-hybrid, 15-sheared-flow-stabilized-z-pinch, 16-muon-catalyzed-fusion, 18-p-b11-frc, 19-orbital-levitated-dipole, 22-projectile-icf, 24-dense-plasma-focus, 27-polywell, 35-polomac-magnetic-confinement`

**Implication**: cost numbers from custom models are not directly commensurable with framework numbers (different CAS coverage, different scaling laws, hand-coded constants). Whether this matters depends on the concept-analysis goal — for ranking purposes it is a confound.

### 2. `inflation_rate` — the 0.0245 vs 0.02 puzzle

- Library default (`/home/reid/1cfe/1costingfe/src/costingfe/model.py:388`): `inflation_rate: float = 0.02`
- Project convention propagated through `costingfe/examples/*.py`: `0.0245`
- 19 of 20 D-T framework concepts use `0.0245`; one (`11-magnetic-mirror:89`) uses `0.02` and labels it "DEFAULT: standard reference" — accidentally correct relative to library, inconsistent with project.
- The lone in-code citation: `14-magnetized-target-fusion-pneumatic-compression:106` → `# DEFAULT: US CPI long-run average; framework standard`. No concept cites a specific CPI vintage, paper, or methodology.
- **This is a project convention masquerading as a library default.** Either pin `inflation_rate=0.0245` as a project constant with a sourced justification, or migrate everything to `0.02` to match the library.

### 3. Geometry-thickness drift (`structure_t`, `vessel_t`)

| Thickness | Tokamak YAML default | Stellarator YAML default |
|---|---|---|
| `structure_t` | 0.20 | 0.15 |
| `vessel_t` | 0.20 | 0.10 |

- **Tokamaks using stellarator-default thicknesses**: `28-hts-tokamak-full-hts` (`structure_t=0.15, vessel_t=0.15` — labeled `DEFAULT` in code but matches neither). `01-hts-compact-tokamak` and `21-spherical-tokamak-hts` use tokamak default 0.20/0.20 correctly. `33-best`, `34-india`, `14-MTF`, `29-neg-tri` use 0.20.
- **Stellarators using tokamak-default thicknesses**: `20b-renaissance` uses `structure_t=0.20, vessel_t=0.20` (sourced to design); `36-helical` also deviates. Default-using stellarators: `05`, `10`, `20a`.
- Numerically these are small but they directly feed CAS22 cost scaling (structure ~M$0.15/m³, vessel ~M$0.72/m³ as calibrated). Silent drift across the tokamak/stellarator default boundary is the kind of bug that survives review.

**Action**: confirm 28-hts-tokamak-full-hts's `0.15/0.15` is intentional, not a copy/paste from a stellarator template.

### 4. `eta_th=0.35` — deliberate standardization, NOT an inconsistency

Many concepts override the framework `eta_th` preset (sCO₂ Brayton ≈ 0.47) to **0.35**, with consistent rationale referencing `scoring_framework.md`:
- `01-hts-compact-tokamak:165` — `standardized from 0.46 per scoring_framework.md (Energy Capture: Thermal (steam))`
- `05-planar-coil-stellarator:77` — `standardized from 0.4 per scoring_framework.md`
- `33-best:141` — `standardized from 0.347 per scoring_framework.md`

This is principled: an apples-to-apples cross-concept comparison choice. Concepts that retain higher η_th (`11-mirror=0.55`, `20b/36=0.48`, `06-mirror=0.7`, `04-laser-icf=0.35`) appear to deviate from the framework but generally cite a different rationale (DEC blend, advanced sCO₂, p-B11 specifics). Not a true inconsistency — this is a designed override.

### 5. `availability` for D-T MFE — wide unprincipled spread

D-T MFE concepts across nominally similar steady-state machines:

| Value | Concepts |
|---|---|
| 0.75 | `01-hts-compact-tokamak, 17b-laser-icf-fast-ignition, 26-laser-icf-indirect-drive, 31-laser-icf-oec, 32-laser-icf-french` |
| 0.80 | `14-MTF, 21-st-hts, 25-heavy-ion, 28-hts-tokamak-full-hts, 29-neg-tri, 30-NIF, 33-best` |
| 0.83 | `36-helical-coil-stellarator` |
| 0.85 | `07-maglif, 11-mirror, 17a-laser-icf-hybrid` |
| 0.87 | `20a-type-one-stellarator` |
| 0.88 | `05-planar-stellarator, 10-large-stellarator` |
| 0.92 | `20b-renaissance` |

Most concepts cite Araiinejad & Shirvan (2025) 75–90% range and pick a value within it. The choice of 0.75 vs 0.80 vs 0.85 within that range is generally not principled by physics — it's a discretionary roll. The 0.92 for 20b is flagged uncertain in its own code.

**Action**: either anchor availability per concept-family with documented rationale, or sensitivity-sweep it.

### 6. `mn` for D-T concepts — small but unprincipled drift

| Value | Concepts | Rationale documented? |
|---|---|---|
| 1.1 (framework default) | 16 D-T concepts | ✓ default |
| 1.0 | `31-laser-icf-oec` | ✓ avoid double-count of embedded Li boost |
| 1.07 | `20b-renaissance` | ✓ JNM 599 (2024) sourced |
| 1.11 | `29-neg-tri` | not checked here |
| 1.15 | `20a-type-one-stellarator` | not checked here |

`31`'s rationale is exemplary (physics reason against the default). The others should at minimum carry a 1-line citation; otherwise they look like cosmetic tweaks.

### 7. `f_sub`, `p_house`, `p_pump`, `p_trit` — small-plant-scaling drift on 34-india

`34-compact-spherical-tokamak-india` (50 MWe, small) carries a coherent but unsourced "small-plant scaling" rationale across its parasitic loads:
- `p_pump=0.5` (default 1.0), `p_trit=8.0` (others 10.0), `p_house=3.0` (default 4.0), `f_sub=0.04` (default 0.03), `p_cool=8.0` (default 13.7).
- Each kwarg comment cites "UNCERTAIN: scaled for 50 MWe machine" but no scaling law or source.

`33-state-backed-tokamak-best` separately bumps `f_sub=0.04` for the inverse reason (LTS support overhead). Two different concepts arriving at 0.04 for different reasons — neither cites a third party.

**Action**: if small-plant scaling matters, codify it as a framework function rather than per-concept eyeballed kwargs.

### 8. `lifetime_yr` — two principled stellarator outliers

- `30 yr`: 19 D-T concepts (project convention).
- `40 yr`: `05-planar-coil-stellarator` (Thea Helios magnet design life, sourced) and `10-large-scale-stellarator` (Gauss Fusion GIGA "magnet and vacuum vessel design life: 40 years", sourced).

Both 40-yr cases are sourced design specs. Other stellarators (`20a`, `20b`, `36`) use 30 yr without comment. **The inconsistency is that some stellarator authors followed sourced design lifetimes and others applied a project-default — there is no shared policy.**

### 9. `construction_time_yr` — uniform spread, weak justification

| Value | Count | Concepts |
|---|---|---|
| 5.0 | 9 | mostly compact / IFE concepts |
| 6.0 (framework default) | 1 | `30-NIF` |
| 7.0 | 2 | `25-heavy-ion, 29-neg-tri` |
| 8.0 (stellarator default) | 4 | `05, 21-st-hts, 33-best, 34-india` |
| 10.0 | 4 | `10-large-stellarator, 20a, 20b, 36` |
| 4.0 | 1 | `07-maglif` |

For tokamaks specifically, `21-st-hts=8`, `28-hts-tokamak-full-hts=5`, `33-best=8`, `34-india=8`, `29-neg-tri=7`, `01=5` — values cluster but no principle distinguishes them.

### 10. Other parameter inconsistencies (less severe)

**`p_cool` for D-T MFE concepts** (framework tokamak default = 13.7):
- 13.7 used by only 1 of 12 concepts (`01-hts-compact-tokamak`)
- 15 used by 6 concepts (matches stellarator default)
- 8, 20, 22, 25 used as one-offs
- Most "tokamak" concepts have silently adopted the stellarator default.

**`p_cryo`** (framework: 0.5 tokamak / 0.8 stellarator):
- HTS concepts cluster at 0.5–2.0 (reasonable)
- LTS concepts: `28-hts-tokamak-full-hts=8`, `33-best=8` (LTS overhead, OK)
- Outliers: `10-large-stellarator=90`, `20b=35`, `05-planar=15` — all sourced to specific magnet system analyses or back-calculated from recirculating power.

**`f_dec=0.2` for `11-magnetic-mirror`**: physically justified (α-particle fraction of D-T energy), not an inconsistency.

**`p_pump=380` for `20b-renaissance`**: inferred from disclosed cycle vs net efficiency, ±50% flagged. Sourced reasoning is in-file. Outlier but defensible.

**`interest_rate=0.0966` for `07-maglif`**: sourced to SAND2006-7148 Z-IFE Fixed Charge Rate (different financial model, not directly comparable to 0.07 WACC convention).

**`noak=False`** for `05, 07, 14`: all principled FOAK first-plant scenarios with explicit comments.

### 11. The `(0)` and `R0=0.0` pattern in IFE/MIF concepts

Six laser-IFE / heavy-ion / MagLIF setups pass `R0=0.0` (no toroidal radius). This is the documented convention for non-toroidal concepts and is consistent — but worth noting because grep-style scans of "R0" inconsistencies pick it up. Not a real inconsistency.

## Code References

- Framework defaults: `/home/reid/1cfe/1costingfe/src/costingfe/model.py:380-393` (forward signature defaults)
- Concept YAMLs (steady-state): `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_{tokamak,stellarator,mirror,polywell,orbitron}.yaml`
- Concept YAMLs (pulsed): `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/pulsed_*.yaml`
- The `0.0245` example-script propagation: `/home/reid/1cfe/1costingfe/examples/*.py`
- Project standardization rationale: `exploration/concept_analysis/scoring_framework.md` (referenced by many concepts for `eta_th=0.35`)
- Worked example of model_setup pattern: `exploration/concept_analysis/analyses/33-state-backed-tokamak-best/model_setup.py:89-205` (`_SHARED_KWARGS` dict)

## Architecture Insights

- **The `_SHARED_KWARGS` dict pattern is consistent** across the 26 framework users; it makes per-concept extraction tractable (this audit pulled 56 unique kwarg names across all setups).
- **Doc-comment discipline is strong on rationale** ("DEFAULT", "UNCERTAIN ±X%", "Source: foo.md §Bar") but weak on enforcing that "DEFAULT" actually matches the library default — `28-hts-tokamak-full-hts` and the 0.0245 inflation rate are clear examples of the label diverging from the truth.
- **No automated check exists** that "DEFAULT"-labeled values actually match the costingfe library defaults. A short audit script could catch the inflation_rate drift and the structure/vessel-thickness drift mechanically.
- **`scoring_framework.md`-driven standardization (`eta_th=0.35`) is a strong design choice** that should probably be applied to availability too — values 0.75/0.80/0.85 are currently chosen per-concept without enforced policy.

## Recommendations

1. **Resolve `inflation_rate` immediately**. Either (a) document a project-specific rationale for `0.0245` and codify it as a project constant; or (b) migrate all 19 concepts to `0.02` to match the library. Update `11-magnetic-mirror` either way.
2. **Audit "DEFAULT" labels** against actual library defaults. A 20-line script (compare each kwarg value to the loaded `_eng_defaults` for the concept's family) would catch silent drift.
3. **Investigate 28-hts-tokamak-full-hts structure/vessel thicknesses**. If 0.15 is intentional, document why; if accidental, fix to 0.20.
4. **Codify small-plant scaling**. The `34-india` per-kwarg eyeballed reductions should be either a function of `net_electric_mw` in the library or an explicit, sourced project scaling law — not 5 separate "UNCERTAIN: scaled for 50 MWe" comments.
5. **Add 1-line sources to `mn` deviations** (`20a=1.15`, `20b=1.07`, `29=1.11`). If unsourced, revert to 1.1.
6. **Decide availability policy** for D-T MFE: either (a) standardize to one value (e.g., 0.80) for cross-concept comparison, or (b) require each non-default value to cite a concept-specific operations argument.
7. **Flag the 12 non-framework concepts** in any LCOE comparison output. Their cost numbers are not commensurable with the 26 framework concepts without conversion.

## Feasibility Assessment

The "DEFAULT" label audit is trivial (one afternoon). The substantive policy fixes (inflation rate convention, availability policy, small-plant scaling) require a project-level decision, not a code-level fix. The geometry-thickness audit is a quick eyeball-and-document pass over ~5 files. None of these are blocking; they are quality/traceability hygiene.

## Open Questions

1. **What is the provenance of the `0.0245` inflation rate?** Likely a historical CATF or 1costingfe author choice — the answer should be findable in 1costingfe git history or example-script commit messages.
2. **Is the 26-vs-12 framework/custom split intentional or technical-debt?** Some custom-model concepts (e.g., 27-polywell, 18-pB11-FRC) may simply predate costingfe support for their concept type, which has since been added (the recent 1costingfe pull added Polywell, FRC, etc.).
3. **Should `eta_th=0.35` standardization extend to `availability`?** The arguments are symmetric — both are heavily LCOE-driving and both currently have ad-hoc concept-by-concept values within a published range.

## Data Artifacts

Intermediate analysis files produced (not committed):
- `/tmp/concept_kwargs.json` — raw per-concept kwarg extraction
- `/tmp/resolved_kwargs.json` — same with module-level constants resolved
- `/tmp/param_breakdown.json` — pivoted view: param → {value → [concepts]}
- `/tmp/analysis_report.txt` — full per-parameter / per-fuel breakdown printout
- Extraction scripts: `/tmp/extract_kwargs.py`, `/tmp/build_comparison.py`, `/tmp/categorize_inconsistencies.py`
