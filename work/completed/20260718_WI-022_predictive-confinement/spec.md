---
Status: completed
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-07-17
Updated: '2026-07-18'
---

# WI-022: Predictive Confinement — Profile-Integrated D-T Reactivity

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — this is a stellarator-demo model-development item. The ARIES-CS hold-out is sealed; the §3 barred paths must not be read, cited, or opened. Admissible sources for this item: the Stellaris design sources under `knowledge/concept_research/09-qi-stellarator-hts/iter-01..03/sources/**` (minus the barred entries) for physics/profiles, and 1costingFE (pinned `0254385`) for the Bosch-Hale reactivity curve and engineering.

## Overview

Replace the injected 0D-effective reactivity with a **profile-integrated D-T reactivity computed live from the source's own plasma profiles**. Today the model computes fusion power the 0D way — `p_fus = 0.25·n̄²·⟨σv⟩(T_eff)·V` at a single volume-average density and one effective reactivity `sigma_v = 5.985e-23` — which yields **2144.5 MW**, below the Stellaris **2700 MW** design point (WI-020 left this gap deliberately visible). The gap is the 0D single-temperature limitation: real density and temperature profiles are peaked, concentrating fusion in the hot dense core, so a volume-average reactivity under-predicts. This item models that peaking from the Stellaris source's own profile parametrization and integrates the Bosch-Hale reactivity over the plasma volume, so the effective reactivity is **derived from sourced physics rather than injected as a 0D constant**.

This is item 2 of the demo-deepening plan (order 3→4→1→2; items 3/4/1 = WI-019/020/021 are done and committed at `7f0b19ea`). It is the last physics item; it reworks the reactivity/fusion-power head of the spine that WI-020 corrected the volume of.

**[OWNER] Approach — "lean into" the codegen handwritten stage (ratified 2026-07-17).** The transcendental physics (Bosch-Hale `exp`, the ρ-integral) is expressed in the SysML `calc def` and realized at the **handwritten codegen stage** — not reduced to an offline scalar. Auto-codegen routes a non-compilable calc to a `handwritten/*_impl.py` stub which the handwritten stage fills with faithful Python. So the reactivity physics lives *in the model*, executed and testable. (Owner, 2026-07-17: *"auto codegen doesn't support [exp], but you can still specify it as a comment within a calc def block. And it will be handled at the handwritten stage. I am tempted to lean into this direction."*) This is the Rung-B option; Rung A (Bosch-Hale live at one effective temperature, still 0D) and Rung C (full ISS04 confinement solve) were offered and set aside — A does not close the gap, C is an epic.

## Goals & Context

**Research questions served**:
- RQ-1 (MFE cost drivers) and RQ-2 (credible LCOE range): fusion power is the head of the power→cost→LCOE spine. Making it a derived output of sourced profile physics — rather than a 0D constant that under-predicts by ~26% — is a fidelity gain at the top of the chain.
- RQ-3 (shared vs. divergent structure): profile peaking is a plasma-physics property the stellarator carries; the reactivity calc becomes the concept's predictive-physics knob, with flat profiles (no peaking) as the tokamak/0D default.

**Demo context**: the Stage-3 backlog and the WI-020 close both name the 2144-vs-2700 gap as "the 0D single-temperature limitation … the target of item 2 (predictive confinement)." The `stellarator_plant.sysml` `sigma_v` doc and the instance headline doc state this explicitly. This item closes that gap *as physics*, or reports honestly how far the sourced physics closes it.

**Epic context**: edits the WI-009 library file `models/library/analyses/mfe_plasma_scaling.sysml` (`'DT Fusion Power'` calc). Consumed by WI-010 (`models/designs/generic_mfe/mfe_plant.sysml`) and the WI-018 concept-09 instance (`models/designs/stellarator_09/stellarator_plant.sysml`). Introduces the demo's first **handwritten-impl** codegen path (all prior calcs were auto-compilable).

## Current State

`models/library/analyses/mfe_plasma_scaling.sysml:153-154` computes

```
out attribute p_fus : Real = 0.25 * (n_e ** 2) * sigma_v * E_fus * V * 1.0e-6;
```

`sigma_v` is an injected input (5.985e-23 m³/s, a genuine Bosch-Hale point at T_eff ≈ 7.9 keV). Volume-average density `n_e` and one effective reactivity give `p_fus = 2144.5 MW` at the WI-020 volume (448 m³). This matches how 1costingFE computes fusion power: `reactivity.py:246` evaluates `sigv_dt(T_i)` at a single ion temperature and volume-average `n_e` — **1costingFE has no profile model**. The under-prediction is inherent to the 0D volume-average, not an error.

## What the source contains (image-verified 2026-07-18 — supersedes the text-extracted values)

The admissible Stellaris source (`knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md`) specifies a full, sourced profile model. The lossy text extraction garbled or invented most of the quantitative rows this item touches; every value below was verified against the extraction's page images (`.../stellaris-design-details/images/`), which are crops of the printed PDF and rank above the reconstructed text under the project's image-inspection protocol. Digitization and integration evidence lives in `prototype/` (this work item).

- **Profile shapes** — `T(ρ) = T₀(1−ρ²)^α_T` (Eq. 2) and `n(ρ) = n₀(1−ρ²)^α_n` (Eq. 3). Functional form image-verified (`page_007_eq_0.png`, `page_007_eq_1.png`). `[REFERENT]`
- **Profile exponents** — digitized from the Fig. 16 panels themselves (`...pdf-9-0.png` density, `...pdf-9-1.png` temperature; `prototype/digitize_fig16.py`): **α_T = 1.19** (all three species, rms log-residual 0.02) and **α_n(fuel) = 0.33** (D and T curves, rms 0.006). The text caption's "α_n = 1.2, α_T = 3.0" is refuted by the figure it captions (α_T = 3.0 predicts T(ρ=0.8) = 0.7 keV; the plotted curve shows 4.3 keV) and is recorded once here as an extraction artifact — the caption text is a bracketed reconstruction that also cites the wrong equation number. Independent corroboration of the digitized fits: the a/L_T ≈ 2.25 gradient quote (Point B, ρ=0.6, line 714) implies α_T = 1.2; the GENE/TANGO Dirichlet boundary values "4.2 / 5.2 keV at ρ = 0.8, informed by the assumed kinetic profiles of Fig. 16" (line 762) imply α_T ≈ 1.0–1.27; the Table-5 printed peak/vol-av electron pair (5.06/3.17) implies α_n(e) = 0.60, matching the digitized electron curve (0.62 — electrons are steeper than fuel because the He-ash is core-peaked). `[REFERENT]` — derived from the source's own figure, fixed blind to the fusion power.
- **Operating point Table 5 Point A (image `page_009_table_0.png`)** — peak n_D = n_T = 1.96×10²⁰ m⁻³; peak T_i = 14.63 keV (T_e0 15.40); vol-av n_e 3.17×10²⁰ (peak 5.06; peak He-ash 0.56 — quasineutrality closes at the peak: 2×1.96 + 2×0.56 ≈ 5.06); plasma volume 425 m³; fusion power **2700 MW**, independently cross-checked against the printed tritium burn rate (416.57 g/day ⇒ 2701 MW); peak fusion heating 5.51 MW/m³ (Bosch-Hale at the peak point gives 5.67 alpha; ×f_α = 0.95 from the Table-4 image → 5.39; agreement ±3%). `[REFERENT]`
- The source's own fusion power is a **profile-integrated "0.5D" power balance** (Appendix A, line 2912: `p ≡ ⟨p⟩_V ≡ ∫_V p dV`) — it integrates `n_D(ρ)·n_T(ρ)·⟨σv⟩(T(ρ))` over the peaked profiles.
- **Bosch-Hale reactivity** — `/home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py:54-70` (`sigv_dt`, the D-T curve, admissible; already cited by WI-020). `[REFERENT]` for the reactivity evaluation.
- **Prototype confirmation (`prototype/reactivity_grid.py`)** — the profile integral with the digitized exponents reproduces the design point with no tuning: **2748 MW at the source's own V = 425 m³ (+1.8% vs the printed 2700)**; 2896 MW at the model's current V = 448. The refuted caption pair would give 1165 MW. Sensitivity: α_T ∈ [1.0, 1.27] spans 3067–2632 MW at V = 425. A nonparametric integral directly over the digitized curves lands at 2888 MW (V = 425), same ballpark with coarser pixel error.

## Codegen feasibility — spike PASSED (2026-07-17)

A spike put a transcendental (`RealFunctions::sqrt`) into `'DT Fusion Power'` in an isolated scratch copy and ran the real snapshot → V11-bridge pipeline. Confirmed:
- The calc routed to `manual_required` (auto-compile classifies the invocation node as non-compilable via `calc_compat_renderer.py:76`); the package **emitted**; V11 params-coverage offenders stayed at **exactly 3** (the pre-existing cross-part rollups) — the transcendental added **zero** offenders. Non-compilable *expression* and params-*coverage* are separate axes.
- The generated `handwritten/…/dt_fusion_power_impl.py` became a `raise NotImplementedError` stub; the backlog listed it (`1 function, complexity High`); the SysML expression was captured verbatim as documentation.
- A hand-filled impl **survived a regen** when the bridge sets `preserve_handwritten=True`.

## Central Decisions — surfaced for the OWNER CHECKPOINT

The Rung-B approach is owner-ratified (above). The remaining decisions are surfaced here and parked for the checkpoint per the capture-fidelity surfacing rule; dependent design detail (calc signature, integral discretization, handshake override) is deferred to `/design-model`.

**Decision A — honest-physics vs close-the-gap (recommend honest-physics).** Per WI-020's Decision A (*"make the model accurate … we can test various inputs at the codegen phase"*), `p_fus` SHALL be whatever the profile integration of the sourced profiles computes — **an output, not tuned to 2700**. The prototype confirms the sourced integration lands within ±2% of 2700 at the source's own volume with no tuning (2748 MW at V = 425): the fuel-pair form `n_D·n_T` already carries the ash/impurity dilution, because the printed peak fuel densities are the diluted values. At the model's current V = 448 the same physics gives ≈2896 MW; that residual is the Table-2-volume question surfaced in the errata section below, not a reactivity effect. The exact figure is reported at implement. **Recommendation: honest-physics — model the profiles, report the computed p_fus, leave any residual gap visible and explained.** *Rejected alternative: fit a peaking factor to hit 2700 exactly — a back-solve, rejected under WI-020 Decision A; recorded, not to be reintroduced.*

**Decision B — handshake closure strategy (recommend flat-profile default).** Making reactivity a live computed calc removes `sigma_v` as an injectable leaf — the WI-021-style trap: `handshake_1costingfe.py` back-solves and injects `fusion__sigma_v` to force 1costingFE's 0D reference point. 1costingFE is itself 0D (single `T_i`, no profiles), so the new calc MUST reduce to the 0D result for the 1cfe reference point. Recommended pattern (mirrors WI-020's `f_shape = 1.0` default): the profile/peaking inputs default to **flat** (no peaking ⇒ the integral collapses to the 0D `0.25·n̄²·⟨σv⟩(T)·V`), so the handshake's 1cfe point is untouched and **SV-025/026 stay byte-identical**. The exact override mechanism (keep a `sigma_v` bypass on the calc vs. inject profile inputs that reproduce 1cfe's value) is a design decision. **Recommendation: flat-profile default; verify SV-025/026 byte-identical.**

**Decision C — profile inputs source (RESOLVED, owner-ratified 2026-07-18).** The profile referents are derived from the source's own primary data, fixed blind to the fusion power: **α_n = 0.33 and α_T = 1.19** (digitized Fig. 16 fits), **n_D0 = n_T0 = 1.96×10²⁰ m⁻³** and **T_i0 = 14.63 keV** (Table 5 image). Density enters as the peak fuel pair with the shape carried by α_n — the fuel term is `n_D(ρ)·n_T(ρ)`, not `0.25·n_e²` (the electron density is ash-diluted and its profile is steeper, α_n(e) ≈ 0.6, so squaring n_e would double-count ash). The Fig.-16 caption exponents in the extracted text are an extraction artifact, refuted by the figure itself (see the source section above). *Rejected alternative: adopt the caption α_T = 3.0 literally — it contradicts the figure it captions, the gradient quote, the ρ = 0.8 boundary values, and the design-point power.*

## ⚠ Surfaced extraction errata (2026-07-18) — image evidence vs committed values

Image-verifying the tables for this item exposed that the text extraction's Tables 2, 3, 4, and 5 are corrupted reconstructions: rows are garbled, and some rows are invented outright (they have no counterpart in the printed table image). Several committed model bindings rest on those text rows. Per the capture-fidelity surfacing rule, nothing here is resolved silently; items are split by authority.

**In scope for WI-022 (straight extraction corrections in the fusion head / viability block this item already rewrites):**

- `stellarator_plant.sysml` `n_e = 3.37e20` cites "Table 5 line 731" — the Table 5 image prints **3.17×10²⁰**. (With the corrected density the old 0D form would give ~1898 MW, not 2144.5 — the "visible 0D gap" was partly masked by this garble.) The profile calc supersedes the 0D use; any remaining vol-av-n_e consumer gets the corrected value and an image citation.
- `wall_load_limit = 4.95` cites "Table 5 line 748 (peak neutron wall power)" — **that row does not exist in the Table 5 image**. The real printed peak neutron wall load is **4.05 MW/m²** (Table 2 image, last row). Correct the value and re-point the citation (also in `mfe_viability.sysml`'s doc). The viability check still passes at the re-baselined power (model average wall load ≈3.2 MW/m² at V = 448).
- WI-020-era doc comments pairing sigma_v with "T_i0 = 24.6 keV" — the image prints **14.63 keV**; rewritten anyway under MR-WI022-3.

**Surfaced 2026-07-18, owner-ratified same day:**

- **Plasma volume / minor radius — [OWNER] ratified 2026-07-18: fold into WI-022.** The WI-020 ruling "target the Table-2 headline 448 m³" rested on the text row "a = 1.5, V = 448" — the Table 2 image prints **a = 1.3, V = 428**, and the Table 5 image prints **V = 425**; a circular torus at the printed radii gives 2π²·12.74·1.3² = 425 m³, so the two tables agree and the WI-020 "empirical shape factor 0.7943" reconciled one artifact against another (true shaping correction ≈ 1.01). The owner amended the WI-020 ruling: bind **a = 1.3** and target **V ≈ 425**; the WI-021 forward-computed radial build (blanket volumes, wall area, coil bore) propagates the correction automatically. In scope for this item (MR-WI022-8).
- **Magnet field — [OWNER] ratified 2026-07-18: separate follow-up item.** The magnet-cost B = 5.86 T cites "Table 3 line 289 (B₀ = 5.86)" — the Table 3 image has **no such row** (its real rows were scrambled in the text), while the Table 2 and Table 5 images both print **axis-averaged B₀ = 9.0 T**. Magnet cost is 45% of total capital. Registered as **WI-023 (magnet-field-errata-B9)**; out of scope here.
- **Surface area.** Table 2 image prints plasma surface area **940 m²**; Table 5 image prints **327 m²**. Mutually inconsistent in the source itself; the model's wall area is radial-build-computed and matches the printed average neutron wall power at ±4%, so no action — recorded only.
- **Coil conduction power (found at implement, 2026-07-18 — parked).** `p_tf = 111.0 MW` cites "Table 2 line 235 (conduction power to coils = 111 MW)" — the Table 2 image has **no such row**; the printed rows are "Number of toroidal field coils: 48" and "Stored magnetic energy: 111 GJ". The text row duplicated the 111 into a phantom power row. 111 MW of recirculating power materially affects p_net; correcting it needs a real sourced value (none identified in Table 2). Parked for owner disposition (candidate: fold into WI-023 or its own item); binding left as-is in WI-022.

## Modeling Requirements

### Functional

#### MR-WI022-1: Profile-integrated reactivity as a handwritten calc

`'DT Fusion Power'` (or a new sibling reactivity calc feeding it) SHALL compute fusion power by integrating the Bosch-Hale D-T reactivity over the sourced density and temperature profiles: `p_fus = ∫_V n_D(ρ)·n_T(ρ)·⟨σv⟩(T(ρ))·E_fus dV`, with `n(ρ)=n₀(1−ρ²)^α_n`, `T(ρ)=T₀(1−ρ²)^α_T`. The transcendental physics (Bosch-Hale `exp`, the ρ-integral) SHALL be expressed in the SysML calc def and realized in its `handwritten/*_impl.py` (the spike-proven seam). The profile/peaking inputs SHALL default to **flat** so the calc reduces to the existing 0D form when no peaking is specified.

- **Type**: Functional | **Priority**: Must | **Derives from**: RQ-1/2; [OWNER] Rung-B ratification; Decision B (flat default)
- **Validation**: SV-029; L1 parse; codegen emits the handwritten stub; run_stellaris bit-exact vs oracle

> Source: `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md` (Eqs. 2–3, image-verified `images/page_007_eq_0.png` / `page_007_eq_1.png`); Fig. 16 panels (`images/...pdf-9-0.png`, `...pdf-9-1.png`, digitized in `prototype/`); Table 5 image (`images/page_009_table_0.png`); `/home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py:54-70` (`sigv_dt` Bosch-Hale D-T)
> Basis: profile-integrated fusion reactivity; the source's own 0.5D power balance (Appendix A)

#### MR-WI022-2: Stellaris instance binds the sourced profile parameters

The concept-09 instance SHALL bind the profile exponents (α_n = 0.33, α_T = 1.19 — digitized Fig. 16 fits) and the Point-A peak fuel densities and ion temperature (n_D0 = n_T0 = 1.96×10²⁰ m⁻³, T_i0 = 14.63 keV — Table 5 image), each carrying an MR-4 citation that resolves to the image files and the digitization record in `prototype/`, with a doc comment stating these are derived from the source's own figure and printed table (a `[REFERENT]`, not an illustrative example) and that the text caption's exponents are an extraction artifact. `p_fus` becomes a computed output (Decision A); the doc SHALL state the computed value and any residual vs the 2700 MW design point plainly.

- **Type**: Functional | **Priority**: Must | **Derives from**: MR-WI022-1; Decision A/C
- **Validation**: SV-029; doc-comment inspection at review

> Source: as MR-WI022-1 (Table 5 image; digitized Fig. 16 panels)

#### MR-WI022-3: Rewrite the sigma_v / mapping-trap documentation

The instance's `sigma_v` doc and the "MAPPING TRAP (sigma_v)" note (`stellarator_plant.sysml` ~line 294, and the head-line doc) SHALL be rewritten: the 0D-injected reactivity is replaced by the profile-integrated calc; the 2144-vs-2700 gap is no longer a "visible 0D limitation handed to item 2" but is closed (or reported with an explained residual) by this item. Per the capture-fidelity correction rule, delete the now-obsolete framing rather than annotating around it.

- **Type**: Traceability / correction | **Priority**: Must | **Derives from**: capture-fidelity correction rule
- **Validation**: doc-comment inspection at review

### Constraint

#### MR-WI022-4: Handwritten-impl codegen path is preserved across regen

The demo pipeline SHALL preserve the hand-written reactivity impl across regeneration: `exploration/stellarator_e2e/bridge_v11_generate.py` SHALL set `preserve_handwritten=True` in its `GenerationConfig` (default is `False`; a regen would otherwise overwrite the impl with a fresh `NotImplementedError` stub — spike finding). The hand-written impl becomes a maintained source file guarded by the oracle (MR-WI022-5).

- **Type**: Constraint | **Priority**: Must | **Derives from**: spike finding (`_clear_output_directory` honors `preserve_handwritten`)
- **Validation**: fill impl → regen → impl body survives (spike-proven); run_stellaris executes it

#### MR-WI022-5: Oracle mirrors the impl; handshake stays closed

The pure-Python oracle (`verify_stellaris.py`) SHALL mirror the profile integral so `run_stellaris.py` asserts the generated handwritten impl bit-exact against it (the impl is no longer auto-synced to the SysML expression, so the oracle is the guard). The **Anchor A handshake SHALL remain closed with no numeric change**: with flat-profile defaults the 1costingFE 0D point is reproduced exactly — **SV-025 and SV-026 byte-identical** to WI-021.

- **Type**: Constraint | **Priority**: Must | **Derives from**: Decision B; the canonical-vs-staged split; MR-WI020-6 pattern
- **Validation**: SV-025/026 re-run byte-identical; `run_stellaris.py` oracle agreement at 1e-9

#### MR-WI022-6: Downstream consumers updated coherently

The change SHALL propagate to every consumer in the same change: the generic plant (`mfe_plant.sysml`), the codegen-adapted staged copies under `exploration/stellarator_e2e/models/`, the regenerated pipeline + handwritten impl, the oracle (`verify_stellaris.py`), and the runner headline check (`run_stellaris.py` — the p_fus/p_th/p_net/q_eng/LCOE assertions move; update to the computed values). Canonical `models/` analyses files stay byte-identical to their staged twins in the shared regions (edit both).

- **Type**: Constraint | **Priority**: Must | **Derives from**: canonical-vs-staged split (handoff)
- **Validation**: L1–L6 on canonical models; run_stellaris bit-exact

### Traceability

#### MR-WI022-7: Citations, clean-room

Every changed formula and value SHALL carry an MR-4 `Source / Ref / Basis` citation resolving to an admissible Stellaris source (profiles/physics) or to 1costingFE at `0254385` (Bosch-Hale curve). No ARIES-CS-informed source may be cited or read (PROTOCOL.md §3).

- **Type**: Traceability | **Priority**: Must | **Derives from**: MR-4; PROTOCOL.md §3
- **Validation**: citation inspection at review

#### MR-WI022-8: Geometry and viability bindings rebound to image-verified values

Per the owner-ratified errata fold-in (2026-07-18), the concept-09 instance SHALL rebind: **a = 1.3 m** (Table 2 image), **f_shape retargeted to the printed V = 425 m³** (Table 5 image; ≈1.003 at R = 12.7 — the empirical 0.7943 is deleted with its rationale docs), **n_e = 3.17×10²⁰ m⁻³** (Table 5 image), and **wall_load_limit = 4.05 MW/m²** (Table 2 image; also re-point the `mfe_viability.sysml` doc). Each rebound value carries an MR-4 citation resolving to the image file. Downstream geometry (radial build, blanket volumes, wall area, coil bore) is forward-computed from `a` (WI-021 seam) and SHALL NOT be hand-adjusted.

- **Type**: Functional / correction | **Priority**: Must | **Derives from**: [OWNER] errata ratification 2026-07-18; capture-fidelity correction rule
- **Validation**: SV-029; L1–L6; run_stellaris headline asserts at the re-baselined values; handshake byte-identical (geometry inputs are injected for the 1cfe point)

> Source: `images/page_002_table_0.png` (a = 1.3, V = 428, peak wall load 4.05); `images/page_009_table_0.png` (V = 425, vol-av n_e 3.17)

## Scope Boundaries

**In scope**
- `models/library/analyses/mfe_plasma_scaling.sysml` — profile-integrated reactivity calc (MR-WI022-1), flat default.
- `models/designs/generic_mfe/mfe_plant.sysml` — thread the profile inputs (MR-WI022-6).
- `models/designs/stellarator_09/stellarator_plant.sysml` — bind sourced profile params; rewrite the sigma_v/trap docs (MR-WI022-2/3); geometry/viability rebind (MR-WI022-8).
- `exploration/stellarator_e2e/` — staged copies, `bridge_v11_generate.py` (`preserve_handwritten=True`), the handwritten reactivity impl, regenerated pipeline, oracle + runner updates, handshake re-run (byte-identical).
- `modeling_project/VALIDATION_MATRIX.md` — SV-029 (created by this spec, status pending).

**Out of scope**
- **Rung C — ISS04 confinement solve** (predict temperature from machine parameters via Appendix A A.7/A.8, close the power balance). It carries a free ISS04 multiplier `f_ren` and an iterative balance — a separate epic, not this item. Temperature/density here are sourced inputs (Table 5), not predicted.
- Recomputing the STALE-BASIS pass-throughs (`buildings_capital`, `preconstruction_capital`, `annual_om`) at the new p_net — their annotations SHALL be updated to the new p_net, but recomputation stays the Stage-3 account-scope item.
- CAS22 tail / CAS40-60 / LCOE-construction structural gap (the −31% handshake LCOE distance) — later account-scope items, unaffected here.

## Success Criteria

1. **SV-029 (profile-integrated reactivity, computed power)**: the generated model computes `p_fus` by integrating the Bosch-Hale reactivity over the sourced profiles (α_n = 0.33, α_T = 1.19, peak fuel pair and T_i0 from the Table-5 image), executed through the **handwritten-impl** codegen path, bit-exact vs the updated oracle via `run_stellaris.py`. `p_fus` is the computed output (Decision A), reported with any residual vs 2700 MW (expected ≈2748 at the ratified V = 425, +1.8%).
2. **SV-025 and SV-026 byte-identical to WI-021** — flat-profile defaults reproduce the 1costingFE 0D point; the handshake is untouched.
3. **Validation Levels 1–6 pass** on canonical models (compare to the WI-021 baseline: L1=0; pre-existing L2/L6 counts unchanged; **zero new offenders**); IFE regression SV-023 unchanged; all three viability constraints (beta, wall load, TBR) still pass at the re-baselined power.
4. **The handwritten impl survives regen** (`preserve_handwritten=True`) and executes through teax (spike-proven mechanism; confirmed on the real pipeline at implement).
5. **The re-baselined headline** (computed p_fus and the recomputed p_th / p_net / q_eng / LCOE / total capital / account shares) is recorded in the work item and `.project/CURRENT_WORK.md`, with the 2144-vs-2700 gap noted as closed or the residual explained.

## Assumptions & Risks

1. **This re-baselines the headline** (certain, accepted): p_fus rises from 2144.5 to ≈2748 at the ratified V = 425, and the geometry rebind (a = 1.3) moves the radial-build-derived volumes, wall area, coil bore, and every downstream cost; power balance, power-scaled accounts, net electric, q_eng, LCOE all recompute. Implement produces exact numbers; design and close state them plainly.
2. **Viability holds at higher power** (medium/high): higher p_fus raises wall load. The real printed peak neutron wall load is **4.05 MW/m²** (Table 2 image; the text's "4.95" row is a phantom — see errata). At the re-baselined power the model's average wall load is ≈3.2 MW/m² (V = 448), under the corrected limit. Implement SHALL bind the corrected limit with an image citation and confirm the check passes; if the computed p_fus pushes it over, surface at the checkpoint/close (do not silently relax the limit).
3. **Flat-profile default preserves the handshake** (certain, high-if-wrong): if the default were peaked, the 1cfe 0D injection would break. MR-WI022-1 fixes the default flat; MR-WI022-5 verifies SV-025/026 byte-identical.
4. **Oracle/impl drift** (medium): the hand-written impl is no longer auto-synced to the SysML expression. The oracle is the guard (run_stellaris asserts bit-exact); `preserve_handwritten=True` keeps the impl across regen. Both are required (MR-WI022-4/5).
5. **Residual vs 2700** (low, quantified): the prototype lands +1.8% of 2700 at the ratified volume; the digitization band (α_T ∈ [1.0, 1.27]) spans roughly ±10%. This is honest physics, reported — not a defect and not to be tuned away.
6. **SV-016 band** ("Q_eng ~10–40") still open from WI-019; item 2 changes p_fus → q_eng, so it moves again. Flag at close for owner adjust/annotate; do not self-resolve.

## Traceability

**Sources**
- `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md`: Eqs. 2–3 (profile forms; image-verified `images/page_007_eq_0.png`, `page_007_eq_1.png`); Fig. 16 panels (`images/stellaris-...pdf-9-0.png` / `pdf-9-1.png`; digitized fits α_n = 0.33, α_T = 1.19 in `prototype/digitize_fig16.py` + `fig16_curves.json`); Table 5 image `images/page_009_table_0.png` (Point A peaks, vol-av n_e 3.17, V 425, 2700 MW, peak heating 5.51); Table 2 image `images/page_002_table_0.png` (a 1.3, V 428, B₀ 9.0, peak wall load 4.05); Table 4 image `images/page_008_table_0.png` (f_α = 0.95); a/L_T quote line 714; GENE/TANGO ρ = 0.8 boundary values line 762; Appendix A lines 2905–2983 (0.5D power balance, ISS04 — Rung C, out of scope).
- `/home/reid/1cfe/1costingfe` @ `0254385`: `reactivity.py:54-70` (`sigv_dt` Bosch-Hale D-T), `reactivity.py:191-246` (0D `fusion_power`, the flat-profile reference the calc must reduce to).

**Downstream impacts**: WI-010 generic plant, WI-018 instance (profile params, sigma_v/trap docs), staged e2e models + `bridge_v11_generate.py` + handwritten impl + pipeline + oracle + runner, handshake (verified byte-identical), VALIDATION_MATRIX SV-029, Stellaris headline in `.project/CURRENT_WORK.md`.

**Applicable project rules**: MR-4 (citations), MR-3 (library concept-agnostic — profile inputs default flat; the stellarator values bind in the instance), PROTOCOL.md §3 (clean-room), capture-fidelity surfacing (Decisions A–C parked for the owner) and correction (obsolete sigma_v/trap framing deleted, not annotated around).

## Related Artifacts

- Epic: `work/backlog/epic-mfe-cost-modeling.md`
- Handoff (item 2): `/tmp/handoff-20260717-133819.md`
- Prior item (WI-020, closest template — physics change at the sigma_v/fusion-power head): `work/completed/20260717_WI-020_stellarator-correct-geometry/`
- Handshake: `exploration/stellarator_e2e/HANDSHAKE_REPORT.md`
- Codegen findings: `exploration/stellarator_e2e/CODEGEN_FINDINGS.md`
- Design: `work/active/WI-022_predictive-confinement/design.md` (to be created after the owner checkpoint)
- Plan: `work/active/WI-022_predictive-confinement/plan.md` (to be created)
