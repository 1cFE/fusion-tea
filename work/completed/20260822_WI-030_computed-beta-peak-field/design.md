---
Status: complete
Created: 2026-08-21
Updated: '2026-08-22'
Related Artifacts:
  Spec: ./spec.md
  Research: ../../../knowledge/research/approved/20260821-152108_wi030-computed-beta-peak-field.md
---

# WI-030 Design: Computed Beta and Conductor Peak-Field Limit

**Required Reading honored:** `knowledge/holdout/aries-cs/PROTOCOL.md`. No barred path was read in the research or in this design. Every new value traces to the Stellaris Table 2 / Table 5 / Fig. 16 images or to 1costingFE at pin `0254385`.

## Overview

Today the field `B` only prices the magnets, and the plasma beta is a number typed into the instance. This item makes two things true:

1. **Beta is computed.** A library calc takes the peak densities and temperatures of each species, the profile exponents, and the on-axis field, and returns the volume-averaged thermal beta. `beta_ok` reads that value. The typed-in `0.0276` becomes a printed cross-check in the doc.
2. **The conductor has a ceiling.** A library calc turns the on-axis field into the peak field on the winding (`B_peak = B × peak_ratio`); a library constraint asserts `B_peak ≤ B_max`. Both facts (`peak_ratio`, `B_max`) live on the magnet system and are bound per instance.

Two new calc defs, one new constraint def, two new magnet attributes, four new plant attributes, two new plant calcs, one new plant-level assert, six instance bindings, one rewired assert, one deleted attribute. Then the package is regenerated and the study capability re-pinned. Nothing in the cost or power chain moves; the headline must reproduce to the cent.

## Research Findings

Full record: `knowledge/research/approved/20260821-152108_wi030-computed-beta-peak-field.md`. What the design rests on:

- **The codegen accepts arithmetic inside a predicate; the study tools do not.** A throwaway generation with `B_axis * peak_ratio <= B_max` gave zero diagnostics and six catalog entries, but `scripts/study/indicators.py:469` and `scripts/study/verify.py:193` raise on any predicate operand that is not a plain feature reference or literal. The spec's "preflight 6/6 and verify pass" bar therefore requires the `wall_load_ok` shape: a calc computes the quantity, the constraint compares two plain formals.
- **Two rounding traps in the spec's numbers.** `peak_ratio = 2.7667` makes `9.0 × 2.7667 = 24.9003 > 24.9` (design point *violated*). With the float64 value of `24.9/9.0`, `2.7666666666666666`, the product is exactly `24.9` and the margin is `0.0`. Likewise `4.70 × 24.9/9.0 = 13.0033 > 13.0`; the exact Nb3Sn ceiling is `4.6988 T`, so the LTS check point is **4.69 T**.
- **Beta reproduces the printed value.** With electron exponent `0.596` (printed vol-av/peak pair `3.17/5.06`) and helium on the fuel exponent `0.33`: Point A `0.026834` (−2.8 % vs 2.76 %), Point B `0.028691` (+2.1 % vs 2.81 %, using B's own pair `6.89/4.21 → 0.6366`). Computed by the generated module. Helium on the electron exponent gives −3.3 %; that is the recorded tolerance. The Fig. 16 density panel independently digitizes the electron curve to `0.62` (rms 0.03); the helium curve cannot be digitized (dotted, 29 pixels).
- **Temperature exponent is shared.** The Fig. 16 temperature panel digitizes to `1.19` for electrons, D, and T alike. Spec A1: shared `alpha_T`, no separate electron value.
- **Constants.** `mu0 = 1.25663706212e-6` is the model's existing default (`mfe_magnet_cost.sysml:41`); 1costingFE carries `1.25663706127e-6` (`tokamak.py:37`, 7e-10 relative). `e_keV = 1.602176634e-16` is exact SI (`tokamak.py:36,40`), the same constant behind `E_fus`.
- **Upstream cross-check caveat.** 1costingFE's `compute_beta_N` (`tokamak.py:117-126`) is `μ0 n_e (T_e + n_i T_i)/B²`, half the standard `2 μ0 ⟨p⟩ / B²`; at the Stellaris point the half-form gives 1.34 %, so the standard form is the one the printed 2.76 % validates. The calc doc cites 1costingFE for the constants and the quantity, not for the factor.
- **Regeneration footprint (measured on the prototype).** Parameters 166 → 173, outputs 72 → 75, six constraints, zero excluded; `beta` gone from the contract; the `beta_ok` catalog id keeps its hash (`82b78aad420730d5`) because its predicate is unchanged.

## Design Decisions

Settled with the owner on 2026-08-21 (`/_my_ask_me`):

| # | decision | grade |
|---|---|---|
| D1 | **Calc-then-compare shape** for the peak-field constraint: `calc def 'Conductor Peak Field'` computes `B_peak`; `constraint def 'Conductor Peak Field Limit'` is the plain `B_peak <= B_max_in`. *Rejected:* arithmetic inside the predicate (the study tools cannot parse it; extending them is a run-study item, filed in `.project/backlog/BACKLOG.md`); the spec's plant-attribute fallback (adds a Level 6 offender, which the spec forbids). | `[AGENT]` (ratified by owner 2026-08-21) |
| D2 | **`peak_ratio` and `B_max` live on the library `'Magnet System'` part def** (AD-007), bound in the instance's `part :>> magnet {}` block; `peak_field_ok` is asserted once in the generic plant beside `net_positive` / `recirc_ok`. Entry points are `magnet__peak_ratio`, `magnet__B_max`. *Consequence:* every MFE instance states its conductor ceiling; Item 6's design table (`run-study-first-consumer/design.md:210-211`) writes the two keys bare and gets a one-line rename. *Rejected:* bare plant attributes (splits the magnet parameters across two homes); instance-only assert (the first conductor-technology constraint would be Stellaris-specific). | `[AGENT]` (ratified by owner 2026-08-21) |
| D3 | **Research report approved** without a DI; the DI ("B enters MFE physics through beta, not only cost; thermal beta from the source's peaks lands 2–3 % under the printed equilibrium beta") is minted at close, on the shipped model's numbers. | `[OWNER 2026-08-21]` |
| D4 | **Design now; implementation after the migration merge.** Ruled when the migration branch was still open. *Overtaken the same afternoon:* PR #107 merged and the item closed (`.project/completed/20260821_stellarator-model-migration/`), so implementation is unblocked. The working tree is `feat/run-study-first-consumer` with Item 6's uncommitted Phase 1 edits alongside; **WI-030 stays on this branch `[OWNER 2026-08-21]`** ("this is intended"). Item 6's design table is settled up at the end; the model is the source of truth for the key names and the 4.69 T point `[OWNER 2026-08-21]`. Re-check the verdict-identity contract as closed by the migration audit at plan time. | `[OWNER 2026-08-21]` |

Settled by the design because every reasonable answer lands in the same place (stated to the owner, not contested):

| # | decision |
|---|---|
| D5 | `peak_ratio` bound as the literal `2.7666666666666666` (= `24.9 / 9.0` in IEEE-754 double; a redefinition expression would be dropped by the pinned codegen, cf. the `G` literal at `stellarator_plant.sysml:128-131`). The doc states the pair and why the literal has 16 digits. |
| D6 | The LTS check point (SV-036, spec success criteria, Item 6) is `B = 4.69 T`, not 4.70. |
| D7 | Exponents: `alpha_n_e = 0.596` (pair-derived, digitization-corroborated); helium shares the fuel exponent `alpha_n = 0.33`; `alpha_T = 1.19` shared by all species. Tolerance recorded: helium on the electron exponent, −3.3 %. The quasineutrality-derived helium exponent (4.03, −6.3 %) is recorded in the research as outside the band, not chosen. |
| D8 | The retired `beta` study axis is replaced by a `B` axis on `stellarator_09__stellaris__magnet__B` in `tests/study/data/axes.known_answers.json`, with its known answer re-derived. |
| D9 | Formal naming follows the D-5 rule (`MODELING_PROCESS.md` § 2.2.2): every calc formal bound from a same-part attribute is suffixed `_in`; chains (`magnet.B`, `peak_field_calc.B_peak`) are named by occurrence path. Defaulted formals are declared last (migration ledger rule D13). |
| D10 | The four new plant attributes (`n_e0`, `T_e0`, `n_He0`, `alpha_n_e`) carry **no defaults**, like `n_e` and `E_fus`: a beta without them is not a beta. The existing profile attributes keep their dormant defaults; this item does not touch them. |

## Proposed Design

### Element 1 — `calc def 'Volume-Averaged Beta'` (library)

**File:** `models/library/analyses/mfe_plasma_scaling.sysml`, appended after `'Neutron Wall Load'`. Package `mfe_plasma_scaling`; `private import ScalarValues::*` already present.

**Engineering description.** Each species' pressure profile is `n_s0 T_s0 (1−ρ²)^(α_n,s + α_T)`. Over a torus-like volume with `dV/V = 2ρ dρ`, the volume average of that profile is `n_s0 T_s0 / (1 + α_n,s + α_T)` (the `u = 1−ρ²` substitution already documented in `'DT Fusion Power'`, lines 142-143). Summing over electrons, deuterium, tritium, and helium ash, converting keV to joules, and dividing by the magnetic pressure gives the volume-averaged thermal beta against the axis-averaged field:

```
beta = 2 * mu0 * e_keV * [ n_e0*T_e0/(1+alpha_n_e+alpha_T)
                         + (n_D0+n_T0)*T_i0/(1+alpha_n+alpha_T)
                         + n_He0*T_i0/(1+alpha_n+alpha_T) ] / B^2
```

Ions share `T_i0`; electrons have their own `T_e0`; the fuel and the ash share the fuel density exponent (D7); one `alpha_T` for all (A1 resolved). Tungsten (`n_W/n_e = 7.76e-6`) is negligible and omitted. Fast-particle pressure is excluded by construction: this is the thermal beta, which is why it sits 2–3 % under the printed equilibrium value.

**Parameters.**

| formal | meaning | unit | bound from (plant) |
|---|---|---|---|
| `n_e0_in` | peak electron density | m⁻³ | `n_e0` (new) |
| `T_e0_in` | peak electron temperature | keV | `T_e0` (new) |
| `n_D0_in`, `n_T0_in` | peak D, T density | m⁻³ | `n_D0`, `n_T0` (existing) |
| `n_He0_in` | peak helium-ash density | m⁻³ | `n_He0` (new) |
| `T_i0_in` | peak ion temperature | keV | `T_i0` (existing) |
| `alpha_n_in` | fuel and ash density exponent | 1 | `alpha_n` (existing) |
| `alpha_n_e_in` | electron density exponent | 1 | `alpha_n_e` (new) |
| `alpha_T_in` | temperature exponent, all species | 1 | `alpha_T` (existing) |
| `B_in` | axis-averaged on-axis field | T | `magnet.B` |
| `mu0` (default `1.25663706212e-6`) | vacuum permeability | T·m/A | library default |
| `e_keV` (default `1.602176634e-16`) | keV → J | J/keV | library default |
| **out** `beta` | volume-averaged thermal beta | 1 | → `beta_ok`, channel `beta_calc__beta` |

**Stencil** (prototype-proven; the doc block is the MR-4 text to ship):

```sysml
calc def 'Volume-Averaged Beta' {
    doc /*
    Volume-averaged thermal plasma beta [1] from peak densities, peak
    temperatures, profile exponents, and the axis-averaged field (WI-030).

      beta = 2 * mu0 * <p> / B^2
      <p>  = e_keV * Sigma_s n_s0 * T_s0 / (1 + alpha_n,s + alpha_T)   [Pa]

    over s in {electrons, D, T, He ash}: ions at T_i0, electrons at T_e0;
    fuel and ash share alpha_n, electrons carry alpha_n_e, one alpha_T for
    all species. The 1/(1 + alpha_n + alpha_T) factor is the volume average
    of (1-rho^2)^(alpha_n+alpha_T) over dV/V = 2*rho*d(rho) -- the same
    u = 1 - rho^2 substitution 'DT Fusion Power' documents. Thermal only:
    fast-particle pressure is excluded, so the value sits a few percent
    under a source's printed equilibrium beta.

    Concept-agnostic: any MFE instance with (1-rho^2)^alpha profiles binds
    its own peaks and exponents; B enters the physics here, not only the
    magnet cost (mfe_magnet_cost.sysml).

    **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py (pin 0254385);
        knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
    **Ref**: tokamak.py:36-40 (_EV exact, KEV_TO_J; MU_0 1.25663706127e-6 --
        this calc keeps the model's 1.25663706212e-6 from mfe_magnet_cost.sysml:41,
        7e-10 apart); tokamak.py:117-126 (compute_beta_N: electron + ion pressure
        over B^2 -- NOTE its mu0*n_e*(T_e + n_i T_i)/B^2 is half the standard
        2*mu0*p/B^2 used here; the printed Stellaris 2.76 % validates the
        standard form); images/page_007_eq_0.png, page_007_eq_1.png (Eqs. 2-3
        profile forms); images/page_009_table_0.png (Table 5: vol. av. beta
        2.76 % / 2.81 %, the cross-check)
    **Basis**: beta = 2*mu0*<p>/B^2 with <p> the volume-averaged thermal
        pressure of all species over (1-rho^2)^alpha profiles; MFE-generic
    */

    // peak electron density [m^-3]
    in attribute n_e0_in : Real;
    // peak electron temperature [keV]
    in attribute T_e0_in : Real;
    // peak deuterium density [m^-3]
    in attribute n_D0_in : Real;
    // peak tritium density [m^-3]
    in attribute n_T0_in : Real;
    // peak helium-ash density [m^-3]
    in attribute n_He0_in : Real;
    // peak ion temperature [keV]
    in attribute T_i0_in : Real;
    // fuel and ash density profile exponent [1]
    in attribute alpha_n_in : Real;
    // electron density profile exponent [1]
    in attribute alpha_n_e_in : Real;
    // temperature profile exponent, all species [1]
    in attribute alpha_T_in : Real;
    // axis-averaged on-axis field [T]
    in attribute B_in : Real;
    // vacuum permeability [T m/A]; declared after the bound formals (ledger D13)
    in attribute mu0 : Real default 1.25663706212e-6;
    // keV -> J (exact SI elementary charge x 1e3)
    in attribute e_keV : Real default 1.602176634e-16;

    // vol-avg electron pressure / e_keV [keV m^-3]
    attribute p_e : Real = n_e0_in * T_e0_in / (1.0 + alpha_n_e_in + alpha_T_in);
    // vol-avg fuel-ion pressure / e_keV [keV m^-3]
    attribute p_fuel : Real = (n_D0_in + n_T0_in) * T_i0_in / (1.0 + alpha_n_in + alpha_T_in);
    // vol-avg helium-ash pressure / e_keV [keV m^-3]
    attribute p_He : Real = n_He0_in * T_i0_in / (1.0 + alpha_n_in + alpha_T_in);
    // vol-avg thermal pressure [Pa]
    attribute p_avg : Real = (p_e + p_fuel + p_He) * e_keV;
    // volume-averaged thermal beta [1]
    out attribute beta : Real = 2.0 * mu0 * p_avg / (B_in ** 2);
}
```

Envelope: `+ − × ÷ **` only, no function invocation, no chains inside the body; auto-implements (`AUTO_IMPLEMENTED = True` in the prototype's stencil, no handwritten rung).

### Element 2 — `calc def 'Conductor Peak Field'` (library)

**File:** `models/library/analyses/mfe_plasma_scaling.sysml`, after Element 1. (Beside the other consumer of `B`, `mfe_magnet_cost.sysml`, was the alternative; the plasma-scaling package already holds the geometry-to-physics helpers and is where `magnet.B` is read for physics, so it goes here.)

**Engineering description.** The field on the winding pack is higher than the field on the plasma axis by a geometry factor set by the coil shape and the plasma–coil distance. For a given coil set that ratio is a fixed fact; the conductor grade only changes how much peak field it can carry. `B_peak = B_axis × peak_ratio`.

```sysml
calc def 'Conductor Peak Field' {
    doc /*
    Peak magnetic field on the winding pack [T] from the axis-averaged field
    and the coil set's peak/axis ratio (WI-030):

      B_peak = B_axis * peak_ratio

    peak_ratio is a coil-geometry fact bound per instance (Stellaris:
    24.9 T peak on the conductor at 9.0 T axis-averaged, Table 2 image);
    it is the quantity a conductor ceiling ('Conductor Peak Field Limit')
    is compared against. Kept as a calc, not an inline plant expression,
    so the product is a module-graph edge the study tooling can trace and
    no plant-level derived expression is introduced.

    **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
        /home/reid/1cfe/1costingfe/src/costingfe/defaults.py (pin 0254385)
    **Ref**: images/page_002_table_0.png (Table 2: axis av. 9.0 T, peak
        conductor 24.9 T); defaults.py:597-603 (MagnetProperties.b_max,
        "peak field ceiling at the conductor" -- the bounded quantity)
    **Basis**: peak-on-winding = axis field x coil-set ratio; MFE-generic
    */

    // axis-averaged on-axis field [T]
    in attribute B_axis_in : Real;
    // peak-on-winding / axis-averaged field ratio [1]
    in attribute peak_ratio_in : Real;
    // peak field on the conductor [T]
    out attribute B_peak : Real = B_axis_in * peak_ratio_in;
}
```

### Element 3 — `constraint def 'Conductor Peak Field Limit'` (library)

**File:** `models/library/analyses/mfe_viability.sysml`, after `'TBR Floor'`.

```sysml
constraint def 'Conductor Peak Field Limit' {
    doc /*
    Conductor-technology bound: the peak field on the winding pack must not
    exceed the conductor's field ceiling. Above it the superconductor cannot
    carry the design current (REBCO ~23 T engineering ceiling, Nb3Sn ~13 T,
    NbTi ~9 T per 1costingFE's MAGNET_TABLE). Pair with 'Conductor Peak
    Field' (mfe_plasma_scaling), which forward-computes B_peak from the
    axis field and the coil set's peak/axis ratio. B_max is bound per
    instance and is the technology lever of a magnet A/B.

    **Source**: /home/reid/1cfe/1costingfe/src/costingfe/defaults.py (pin 0254385);
        knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
    **Ref**: defaults.py:605-614 (MAGNET_TABLE b_max: rebco_hts 23.0, nb3sn 13.0,
        nbti 9.0, "engineering ceilings"); images/page_002_table_0.png (Table 2:
        24.9 T peak conductor field, the Stellaris design value)
    **Basis**: peak field on the conductor <= conductor ceiling
    */

    // peak field on the conductor [T]
    in attribute B_peak : Real;
    // conductor peak-field ceiling [T]
    in attribute B_max_in : Real;

    B_peak <= B_max_in
}
```

### Element 4 — `'Magnet System'` gains two attributes (library)

**File:** `models/library/cost_structure/mfe_power_core.sysml:85-91`, after `cost_per_kAm`. Doc block's parameter list gains two lines.

```sysml
        // peak-on-winding / axis-averaged field ratio [1] (coil-set geometry fact)
        attribute peak_ratio : Real;
        // conductor peak-field ceiling [T] (conductor technology fact)
        attribute B_max : Real;
```

### Element 5 — generic plant wiring (`models/designs/generic_mfe/mfe_plant.sysml`)

After `alpha_T` (line 182), four attributes and two calcs:

```sysml
        // Beta inputs (WI-030). No defaults: a beta without its peaks is not a beta.
        // peak electron density [m^-3]
        attribute n_e0 : Real;
        // peak electron temperature [keV]
        attribute T_e0 : Real;
        // peak helium-ash density [m^-3]
        attribute n_He0 : Real;
        // electron density profile exponent [1]
        attribute alpha_n_e : Real;

        // Volume-averaged beta (WI-030): B enters the physics here.
        calc beta_calc : 'Volume-Averaged Beta' {
            in n_e0_in = n_e0;
            in T_e0_in = T_e0;
            in n_D0_in = n_D0;
            in n_T0_in = n_T0;
            in n_He0_in = n_He0;
            in T_i0_in = T_i0;
            in alpha_n_in = alpha_n;
            in alpha_n_e_in = alpha_n_e;
            in alpha_T_in = alpha_T;
            in B_in = magnet.B;
        }

        // Peak field on the winding (WI-030).
        calc peak_field_calc : 'Conductor Peak Field' {
            in B_axis_in = magnet.B;
            in peak_ratio_in = magnet.peak_ratio;
        }
```

After `recirc_ok` (line 796), the sixth assert:

```sysml
        assert constraint peak_field_ok : 'Conductor Peak Field Limit' {
            in B_peak = peak_field_calc.B_peak;
            in B_max_in = magnet.B_max;
        }
```

The generic plant carries no Stellaris value (MR-WI030-3). `beta_ok` stays in the instance (WI-018 placement), rewired.

### Element 6 — Stellaris instance (`models/designs/stellarator_09/stellarator_plant.sysml`)

Magnet block (after `coil_markup`, line 147):

```sysml
            // Peak-on-winding / axis-averaged field ratio [1] = 24.9 / 9.0 written
            // as its IEEE-754 double so that 9.0 * peak_ratio == 24.9 exactly and
            // peak_field_ok reads margin 0.0 at the design point (2.7667 would
            // read 24.9003, violated). A redefinition expression is dropped by the
            // pinned codegen, hence the literal.
            :>> peak_ratio = 2.7666666666666666 {
                doc /* **Source**: stellaris-design-details.md **Ref**: Table 2 image (images/page_002_table_0.png: peak conductor magnetic field strength 24.9 T; axis av. magnetic field strength 9.0 T) **Basis**: Stellaris coil-set peak/axis field ratio, 24.9/9.0 */
            }
            // Conductor peak-field ceiling [T]. [OWNER 2026-08-21]: the field
            // Stellaris designs to (Table 2), not 1costingFE's REBCO engineering
            // ceiling of 23.0 T (defaults.py:611), which the Stellaris winding
            // exceeds by 1.9 T; the disagreement is disclosed, the design value
            // is bound.
            :>> B_max = 24.9 {
                doc /* **Source**: stellaris-design-details.md; /home/reid/1cfe/1costingfe/src/costingfe/defaults.py (pin 0254385) **Ref**: Table 2 image (images/page_002_table_0.png: peak conductor magnetic field strength 24.9 T); defaults.py:605-612 (MAGNET_TABLE rebco_hts b_max = 23.0, not bound -- owner ruling 2026-08-21) **Basis**: Stellaris REBCO design peak field; the HTS arm's ceiling for the Item 6 A/B */
            }
```

Profile block (after `alpha_T`, line 447):

```sysml
        // Beta referents (WI-030): electron and helium peaks from the Table 5
        // image, Point A; the electron density exponent from the printed
        // vol-av/peak pair. The computed beta (beta_calc) at this point is
        // 0.026834 vs the printed 2.76 % (-2.8 %; helium on the electron
        // exponent would give -3.3 %, the recorded tolerance) -- thermal beta,
        // fast-particle pressure excluded. Quasineutrality at the peak:
        // 2 x 1.96 + 2 x 0.56 = 5.04 ~= 5.06.
        :>> n_e0 = 5.06e20 {  // peak electron density [m^-3].
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 5 image (images/page_009_table_0.png: peak el. density 5.06e20 m^-3, Point A; the extracted text "4.55" is an extraction artifact) **Basis**: Stellaris Point-A peak electron density */
        }
        :>> T_e0 = 15.40 {    // peak electron temperature [keV].
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 5 image (images/page_009_table_0.png: peak el. temperature 15.40 keV, Point A) **Basis**: Stellaris Point-A peak electron temperature; ions at T_i0 = 14.63 */
        }
        :>> n_He0 = 0.56e20 { // peak helium-ash density [m^-3].
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 5 image (images/page_009_table_0.png: peak helium ash density 0.56e20 m^-3, Point A) **Basis**: Stellaris Point-A peak helium-ash density; shares the fuel exponent alpha_n (the Fig. 16 helium curve is dotted and cannot be digitized) */
        }
        :>> alpha_n_e = 0.596 { // electron density profile exponent [1].
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 5 image (images/page_009_table_0.png: vol.-av. el. density 3.17e20 and peak el. density 5.06e20, Point A): for n(rho) = n0*(1-rho^2)^alpha, <n>/n0 = 1/(1+alpha), so alpha = 5.06/3.17 - 1 = 0.596; corroborated by the Fig. 16 density-panel digitization (images/stellaris-high-field-quasi-isodynamic-stellarator.pdf-9-0.png, electrons: alpha = 0.62, rms log-residual 0.03, WI-022 prototype/digitize_fig16.py re-run 2026-08-21) **Basis**: electron density exponent derived from two printed numbers; Point B's pair 6.89/4.21 gives 0.637 (SV-036 override) */
        }
```

Viability block (lines 826-834, 874-877): delete the `attribute beta : Real = 0.0276 {…}` block; keep `beta_limit`; replace the `// Beta.` comment with the cross-check note:

```sysml
        // Beta (WI-030): computed by beta_calc ('Volume-Averaged Beta') from the
        // profile referents above and magnet.B. The printed Table 5 value,
        // vol. av. beta 2.76 % (Point A) / 2.81 % (Point B), is the cross-check,
        // not an input: computed 0.026834 / 0.028691 (SV-036). The former bound
        // beta = 0.0276 (analyst-patch-spec-anchors.md line 44) is retired.
        // design/optimization beta target.
        attribute beta_limit : Real = 0.05 { … unchanged … }
        …
        assert constraint beta_ok : 'Beta Limit' {
            in beta_in = beta_calc.beta;
            in beta_limit_in = beta_limit;
        }
```

### Element 7 — exploration twin

`exploration/stellarator_e2e/models/` is byte-identical to `models/` (`tests/models/test_model_family_spines.py`). Edit `models/` once, copy the five touched files into the twin with `cp`; never hand-sync.

## Cross-File Bindings

| binding (plant usage) | source | target file / element |
|---|---|---|
| `beta_calc.n_e0_in … alpha_n_e_in` | plant attributes | `mfe_plant.sysml` (new and existing profile attributes) |
| `beta_calc.B_in` | `magnet.B` | `'Magnet System'` attribute, bound in the instance |
| `peak_field_calc.B_axis_in` | `magnet.B` | same |
| `peak_field_calc.peak_ratio_in` | `magnet.peak_ratio` | `mfe_power_core.sysml` (new), bound in the instance |
| `peak_field_ok.B_peak` | `peak_field_calc.B_peak` | calc output (channel) |
| `peak_field_ok.B_max_in` | `magnet.B_max` | `mfe_power_core.sysml` (new), bound in the instance |
| `beta_ok.beta_in` (instance) | `beta_calc.beta` | calc output (channel); was the bound attribute `beta` |

Imports: `mfe_plant.sysml` already imports `mfe_plasma_scaling::*`, `mfe_viability::*`, `mfe_power_core::*`; `stellarator_plant.sysml` already imports the plant. No new imports.

Dataflow (unidirectional, no new cycle):

```
magnet.B ─┬─► magnet_cost (existing)
          ├─► beta_calc ──► beta_ok  ◄── beta_limit (instance)
          └─► peak_field_calc ──► peak_field_ok ◄── magnet.B_max (instance)
                  ▲
           magnet.peak_ratio (instance)
n_e0, T_e0, n_He0, alpha_n_e (instance) ─► beta_calc ◄─ n_D0, n_T0, T_i0, alpha_n, alpha_T (existing)
```

Beta and the peak field consume only bound facts and `magnet.B`; nothing downstream of them feeds the cost or power chain, so the headline cannot move.

## Validation Plan (SV-036)

| check | bar | how |
|---|---|---|
| Levels 1–6 | L1 = 0; L2/L6 offender lists equal to the current tree's (5 WARN, 5 ERROR, all pre-existing) | `uv run agentic-mbse validate --complete models` and the twin; diff against the baseline captured in this design |
| Generation | exit 0, zero readiness diagnostics, `runtime_contract_version 2.0.0`, six concrete constraints, zero excluded | `uv run sysml-codegen generate --models exploration/stellarator_e2e/models --output exploration/stellarator_e2e/generated --package-name stellarator_tea --overwrite --smart-regen --preserve-handwritten` |
| Contract | 173 parameters, 75 outputs; `…__beta` absent; `n_e0`, `T_e0`, `n_He0`, `alpha_n_e`, `magnet__peak_ratio`, `magnet__B_max`, `beta_calc__mu0`, `beta_calc__e_keV` present; channels `beta_calc__beta`, `peak_field_calc__B_peak` present; `beta_ok` id unchanged | read `contracts/model_contract.json` |
| Beta at Point A / B | `0.026834` (−2.8 % of 0.0276) / `0.028691` (+2.1 % of 0.0281) within ±3.5 %; oracle rel 1e-9 | `verify_stellaris.py` recompute; Point B by overriding the eleven Table-5 values (`alpha_n_e = 0.6366`) |
| Headline | LCOE 275.264220, total capital 16,129,706,216.04, p_net 915.081088, q_eng 6.606662, rec_frac 0.151362, magnet capital unchanged to the cent | `run_stellaris_single.py` anchors; `AFTER_MIGRATION_RECORD.md` § 2 |
| Verdicts | six satisfied; `peak_field_ok` margin exactly `0.0` | `run_stellaris_single.py` (`EXPECTED_VERDICTS` gains `peak_field_ok`) |
| LTS checks | `B_max = 13.0, B = 9.0` → `peak_field_ok` violated (margin −11.9); `B_max = 13.0, B = 4.69` → satisfied (+0.0243) and `beta_ok` violated (beta 0.0988) | a study point through `studies/study_route.py` on the regenerated package, or the oracle |
| Study capability | `preflight.py gates` 6/6; `verify.py` outcome pass; `uv run pytest tests/study tests/models` green; IFE census and anchors unchanged | after manifest and fixture re-pin |
| MR-3 / MR-4 | no numeric literal in the new library defs other than the two defaults; no Stellaris value in `mfe_plant.sysml`; every new binding's Ref resolves to an image or a pinned upstream line | grep + citation read at audit |

## Validation Report (prototype, 2026-08-21)

Prototype tree: the 14 MFE canonical files materialized to the session scratchpad with `tests.model_families.materialize_canonical_subset`, edited exactly as Elements 1–6 (docs abbreviated), generated with the installed pin (sysml-codegen 0.1.1 at `8a758e92`).

| check | result |
|---|---|
| `sysml-codegen generate` | **PASS** — exit 0, no readiness diagnostics, 61 modules, 5 input groups |
| Contract | **PASS** — 173 parameters, 75 outputs, `constraint_catalog` 6 concrete / 0 excluded; `stellarator_09__stellaris__beta` absent; all eight new entry points present with the expected defaults (`magnet__peak_ratio = 2.7666666666666666`, `magnet__B_max = 24.9`, `alpha_n_e = 0.596`); `beta_calc__beta` and `peak_field_calc__B_peak` channels present; `beta_ok` id `82b78aad420730d5` unchanged; `peak_field_ok` id `49c6b8228a73cac5` |
| Study tools parse the catalog | **PASS** — `scripts/study/indicators.predicate_operands` returns `('<=', [feature_ref B_peak, feature_ref B_max_in])` for `peak_field_ok` and the five existing shapes unchanged (the arithmetic-predicate spike had raised `IndicatorError` here) |
| Generated predicate | `constraint_pred_definition_mfe_viability__conductor_peak_field_limit(B_peak, B_max_in)`: `(24.9, 24.9) → satisfied, margin 0.0`; `(24.9, 13.0) → violated, −11.9`; `(12.97567, 13.0) → satisfied, +0.02433`; `(13.00333, 13.0) → violated, −0.00333` |
| Generated impls | both `AUTO_IMPLEMENTED = True`; `beta` at Point A `0.026834157382368398`, Point B `0.028690626389808137`, Point A at 4.69 T `0.09881600592704343`; `B_peak(9.0) = 24.9` exactly, `B_peak(4.69) = 12.975666666666667`, `B_peak(4.70) = 13.003333333333334` |
| `agentic-mbse validate --complete` on the prototype tree | **PASS for this item** — L1 0 errors; L2 5 WARN (the same five literal-bound `waste`/`fuel_handling`/`other_rpe` inputs); L3/L4/L5 clean; L6 5 ERROR, all pre-existing: the four capital-rollup derived expressions (`mfe_plant.sysml:423/429/540/689`) and the `.`-operator report on `preconstruction_capital` (`mfe_plant.sysml:101`), which the unmodified twin reports identically (the validator emits one such line per run; on the full `models/` tree the IFE file's line wins). Zero introduced offenders |
| Package execution | not run (teax root not configured in this session); the generated impls and predicate were executed standalone, above |

Prototype status: **PASS**. Files that will change: `models/library/analyses/mfe_plasma_scaling.sysml`, `models/library/analyses/mfe_viability.sysml`, `models/library/cost_structure/mfe_power_core.sysml`, `models/designs/generic_mfe/mfe_plant.sysml`, `models/designs/stellarator_09/stellarator_plant.sysml`, their five twins, and the package/study artifacts listed below.

## Implementation Checklist (for `/plan-model`)

1. **Library** — Elements 1–4 in `models/library/`; L1 pass; grep for literals.
2. **Plant and instance** — Elements 5–6; delete the bound `beta`; L1–L6 diff against the baseline; copy the five files to the twin; `tests/models/test_model_family_spines.py` twin test green.
3. **Regenerate** — the command above, in place, `--smart-regen --preserve-handwritten`; check the two normative handwritten impls' sha256 survive; confirm the contract facts in the Validation Plan.
4. **Oracle and runner** — `verify_stellaris.py::compute` adds `beta` and `B_peak` (closed forms); `oracle_entry.py`: `ORACLE_OUTPUT_TO_CHANNEL` gains `beta → …beta_calc__beta`, `B_peak → …peak_field_calc__B_peak`; `OPERAND_BINDINGS`: `beta_ok.beta_in` becomes `{"kind": "channel", "key": …beta_calc__beta}`, new row `peak_field_ok__<hash>` with `B_peak` (channel) and `B_max_in` (input `…magnet__B_max`); `run_stellaris_single.py::EXPECTED_VERDICTS` gains `peak_field_ok`.
5. **Manifest and fixtures** — `studies/manifest.json`: fingerprints, `indicator_inputs` digest, `baseline.verdicts` + `peak_field_ok`, `objective_catalog` + `beta_calc__beta`; `tests/study/data/axes.known_answers.json`: `beta` axis → `B` axis (D8), `axes.extras.json` if it names `beta`; re-derive every `*.expected.json` (they fail first on the old fingerprint, by design); `tests/models/data/mfe_census.json` recaptured; `stellarator.snapshot.json` recaptured.
6. **Verification** — SV-036 rows executed and recorded in `VALIDATION_MATRIX.md`; `AFTER_MIGRATION_RECORD.md`-style record of the headline and six verdicts; `preflight.py gates`, `verify.py`, `pytest tests/study tests/models`.
7. **Hand-offs** — Item 6 design table: `B_max` → `magnet__B_max`, `peak_ratio` → `magnet__peak_ratio`, LTS point 4.69 T; DI minted at close (D3).

## Risks

| risk | likelihood / impact | mitigation |
|---|---|---|
| Migration audit (SC2 verdict-identity contract, SC11) changes a package convention before implementation | medium / low | D4: re-check at plan time; the design touches no verdict-identity code, only adds a sixth row to the same shapes |
| The `beta_ok` catalog id changes on regeneration (binding changed from input to channel) | low / low | The prototype kept `82b78aad420730d5`; if it moves, `oracle_entry.py` and the manifest follow the contract, never a suffix guess |
| Float boundary at the design point (margin exactly 0.0) | settled | D5; verified on the generated predicate; any future `B ≠ 9.0` sweep point is off-boundary |
| A future MFE instance without a sensible `peak_ratio` | low / low | D2 consequence: it binds one; a planar-coil tokamak has a well-defined ratio. Recorded, not mitigated further |
| `tests/study` fixture re-derivation misses an axis that named `beta` | low / low | `test_fixture_binding` and the known-answer tests fail first on the old fingerprint; grep `beta` in `tests/study/data/` at step 5 |
| Two study tools cannot read arithmetic predicates (discovered here) | n/a for this item | Filed: `.project/backlog/BACKLOG.md` Flagged row (run-study capability) |

## Spec amendments made by this design

Recorded in `spec.md` with the date: MR-WI030-2's shape ("asserting `B_peak ≤ B_max` through `'Conductor Peak Field'`"), `peak_ratio = 2.7666666666666666`, the LTS point `B = 4.69`, and R1's resolution. `VALIDATION_MATRIX.md` SV-036 updated to match.

## Approval

**Approved by owner 2026-08-21.** Plan: `./plan.md` (five phases, on this branch per D4).
