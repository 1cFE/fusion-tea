# WI-016 Blind Derivation — Tokamak Fusion Power, MFE Power Balance, Magnet Cost

Derived from the whitelisted research corpus plus declared pretraining physics only. No costing-code files were read. Citation convention: **[corpus: file, location]** for corpus material, **[pretraining: reference]** for textbook physics. The primary corpus source is the ARC design paper (Sorbom et al. 2015), extracted at `knowledge/concept_research/01-hts-compact-tokamak/iter-03/sources/arc-reactor-specifications/output.md` — abbreviated **[ARC, line N]** below.

## ARC-class anchor point (source-quoted)

All from [ARC]: R0 = 3.3 m, a = 1.13 m, κ = 1.84, B0 = 9.2 T, Ip = 7.8 MA (Table 7 image `images/page_026_table_0.png`; also lines 1396–1403); ⟨T⟩ = 13.9 keV, ⟨n20⟩ = 1.3, βN = 2.59, T0 = 27 keV, n20(0) = 1.75, p0/⟨p⟩ = 2.6 (lines 558–566); Pfus = 525 MW, Qp = 13.6 (lines 719–724, abstract); fbs = 0.63 (line 724); coupled RF = 25 MW LHCD + 13.6 MW ICRF (abstract); ICRF wall-plug 19 MW at ~70% source efficiency (lines 890–893); LH klystrons 50% efficient (line 860); Brayton ηth = 0.40 at 900 K blanket outlet, giving Pnet = 190 MW, Qe = 3 (lines 197–200); TF stored energy 18 GJ (lines 1032–1033); peak on-coil field 23 T (line 933); 5730 km of 12 mm REBCO tape, 70 kA cables of 106 tapes, 120 cables/leg, 18 TF coils (lines 1025–1095); REBCO $18–36/m 2014$ (Table 10, image-verified at `images/page_028_table_1.png`; the markdown "$198/m" at line 1542 is an OCR error); magnet structure 4350 t SS316LN, fabricated cost $4.6B at $1.06M/tonne scaling (lines 1558, 1579–1584, image `images/page_029_table_0.png`).

---

## Relation 1 — Tokamak fusion power from machine parameters

### Functional form

```
P_fus [MW] = 1.20 · C_prof · β_T² · B0⁴ · (2π² R a² κ)
```

with β_T a fraction, B0 in tesla, volumes in m³. Substituting the operating-point closures (Troyon beta + kink safety factor) gives the machine-parameter form:

```
P_fus [MW] ≈ 0.0148 · C_prof · [β_N² (1+κ²)² / q*²] · κ a⁴ B0⁴ / R
```

(β_N in conventional %·m·T/MA units, Ip in MA implied.)

### Derivation chain

**Step 1 — fusion power density.** For a 50/50 D-T plasma, n_D = n_T = n/2, so the volumetric fusion power is S = (n²/4)⟨σv⟩E_fus, with E_fus = 17.6 MeV [pretraining: Freidberg, *Plasma Physics and Fusion Energy*].

**Step 2 — quadratic reactivity closure.** Over 10–20 keV the D-T reactivity is well approximated by ⟨σv⟩ ≈ 1.1×10⁻²⁴ T² m³/s (T in keV), accurate to ~10% [pretraining: Freidberg §3; standard]. This makes S ∝ (nT)² ∝ p², which is exactly the scaling the ARC paper states as its Eq. (1): P_f/V_P ∝ ⟨p⟩² ∝ β_T² B0⁴ [ARC, lines 217–221]. The corpus confirms the form; the pretraining constant fixes the coefficient.

**Step 3 — pressure/beta link.** With T_e = T_i = T, p = 2nT and β_T = 2μ0 p/B0² [pretraining: standard definition; ARC line 244]. So nT = β_T B0²/(4μ0). Substituting into S:

```
S = (E_fus · 1.1e-24 / 4) · [β_T B0² / (4 μ0 e_keV)]²  = 1.20 β_T² B0⁴  MW/m³
```

where e_keV = 1.602×10⁻¹⁶ J/keV. Numerically: (2.819e-12 × 1.1e-24/4) / (4·μ0·1.602e-16)² = 1.20×10⁶ W/m³.

**Step 4 — volume.** Elliptical-cross-section torus: V_p = 2π² R a² κ [pretraining: geometry].

**Step 5 — profile factor.** Real profiles are peaked; C_prof ≡ ⟨S(n(r),T(r))⟩/S(⟨n⟩,⟨T⟩). Peaking gains are partly cancelled because ⟨σv⟩ grows slower than T² above ~15 keV. Calibrating to the ARC design point (below) gives C_prof ≈ 1.05; expect 1.0–1.3 generally [judgment; ARC profile data lines 558–566].

### Operating-point closures (each with basis)

1. **Troyon beta limit**: β_T = β_N Ip/(a B0), β_N ≤ 3 (ARC design margin: 2.59) [ARC Eq. (2), lines 256–263; pretraining: Troyon 1984].
2. **Kink safety factor**: q* = 5 a² B0 (1+κ²) / (2 R Ip) ≥ 2.2 (Ip in MA), i.e. Ip is capped by the kink limit [ARC Eqs. (3)–(4), lines 264–275].
3. **Greenwald density limit**: n̄20 ≤ 0.9 · Ip/(π a²) [ARC Eq. (5), line 277; pretraining: Greenwald 1988]. ARC sits at 64% of the limit [ARC, line 569], so density is a check, not the binding constraint.
4. **Elongation limit (vertical stability)**: κ ≤ 5.4 ε, valid 0.2 ≤ ε ≤ 0.55 [ARC Eq. (6), lines 281–283].
5. **Temperature choice**: ⟨T⟩ ≈ 13–14 keV minimizes the required nTτ (Lawson minimum) [ARC, line 749; pretraining: Lawson criterion].
6. **Field constraint**: B0 = B_coil,max(1 − ε − Δb/R) with Δb the inboard blanket/shield thickness — the on-coil field, not B0, is the real engineering limit [ARC Eq. (9), lines 300–302].

### Validity range

- ⟨T⟩ = 10–20 keV (quadratic reactivity window); outside it use the full Bosch-Hale form.
- Conventional aspect ratio ε ≲ 0.5; the kink formula and elongation limit are leading-order shaping approximations.
- Pure D-T, no dilution: helium ash and impurities reduce P_fus by roughly f_dil² (10–20% in steady state). ARC assumed Z_eff = 1.2 [ARC, line 317]; not corrected here.
- β_N at or below Troyon; profiles I-mode/H-mode-like (C_prof calibration).

### Worked example — ARC design point

Inputs (all source-quoted, table above): R = 3.3, a = 1.13, κ = 1.84, B0 = 9.2, Ip = 7.8, βN = 2.59.

- β_T = 2.59 × 7.8/(1.13 × 9.2) = 1.94% = 0.0194 (paper's own convention, Eq. 2)
- S = 1.20 × (0.0194)² × 9.2⁴ = 3.24 MW/m³
- V_p = 2π² × 3.3 × 1.13² × 1.84 = 153 m³
- P_fus = 3.24 × 153 × C_prof = 497 × 1.05 ≈ **522 MW** vs. source-quoted **525 MW** (−0.6% with calibrated C_prof; −5% with C_prof = 1).

Cross-check of the machine-parameter form: q* = 5×1.13²×9.2×(1+1.84²)/(2×3.3×7.8) = 5.0; then 0.0148 × [2.59² × (4.386)²/5.0²] × 1.84 × 1.13⁴ × 9.2⁴/3.3 × 1.05 ≈ 523 MW. Consistent.

**Corpus sufficiency: strong.** The corpus supplied the scaling form, every operating-limit closure, and the anchor point; pretraining supplied only the reactivity coefficient, the D-T energy, and torus geometry.

---

## Relation 2 — MFE power balance

### Functional form

```
P_alpha = P_fus/5            P_n = 4·P_fus/5                    (D-T split)
P_th    = M_n·P_n + P_alpha + P_aux,coupled                     (thermal power to cycle)
P_gross = η_th · P_th
P_recirc = P_aux,coupled/η_wp + P_cryo + P_house
P_net   = P_gross − P_recirc
Q_p     = P_fus/P_aux,coupled        Q_e = P_net/P_recirc       f_recirc = P_recirc/P_gross
```

### Derivation chain and input bases

- **Alpha/neutron split**: D-T yields 17.6 MeV shared inversely with mass between the alpha (3.52 MeV, 20%) and neutron (14.06 MeV, 80%) by momentum conservation [pretraining: Freidberg]. Alphas heat the plasma and exit as first-wall/divertor heat; neutrons deposit in the blanket.
- **Blanket energy multiplication M_n**: exothermic ⁶Li(n,α)T (+4.8 MeV) plus (n,2n) in the beryllium multiplier amplify neutron energy; M_n ≈ 1.1–1.2 for a breeding blanket [pretraining: standard blanket engineering]. Corpus support: ARC breeds TBR ≥ 1.1 with a Be multiplier and FLiBe [ARC abstract; Be multiplier in Table 11]. Consistency with ARC's published numbers (below) selects M_n ≈ 1.2.
- **Coupled auxiliary power appears twice**: it heats the plasma (so it ends up in the thermal stream) and it costs wall-plug power at efficiency η_wp. For ARC: LHCD klystrons 50% [ARC, line 860], ICRF sources ~70%, wall-plug 19 MW for 13.6 MW coupled [ARC, lines 890–893].
- **Thermal conversion η_th**: non-ideal He Brayton cycle; 0.40 at 900 K blanket outlet, 0.46 at 1100 K, 0.50 at 1200 K [ARC, lines 195–226].
- **Cryogenic load**: small for HTS at 20 K — ARC joint dissipation needs only 0.57 MW of cooling power [ARC, line 1107]; budget ~1–5 MW wall-plug. Contrast: a large modern plant carries ~70 MW total auxiliary/house load [corpus: Helios overview, `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/output.md`, line 377], so for GW-class plants P_house is not negligible.

### Validity range

- D-T only (the 4:1 split is reaction-specific). Steady-state or long-pulse machines (no pulsed-energy-storage terms). η_wp, η_th are technology choices, not physics; carry them as parameters.
- Q_e definitions vary by scope (whole-plant vs. fusion-power-core). The relation above is the fusion-power-core accounting the ARC paper uses; a whole-site Q_e is lower [ARC, lines 188–190].

### Worked example — ARC FNSF phase (η_th = 0.40)

- P_alpha = 105 MW, P_n = 420 MW (from P_fus = 525 MW)
- P_aux,coupled = 38.6 MW; wall-plug: 25/0.50 + 19 = 69 MW; + ~1 MW cryo → P_recirc ≈ 70 MW
- M_n = 1.2: P_th = 504 + 105 + 38.6 = 648 MW → P_gross = 0.40 × 648 = **259 MW** (consistent with the abstract's "200–250 MWe" class)
- P_net = 259 − 70 = **189 MW** vs. source-quoted **190 MW**
- Q_e = 189/70 = **2.7** vs. quoted 3; f_recirc = 70/259 = **0.27**; Q_p = 525/38.6 = **13.6** vs. quoted 13.6.

With the more conservative M_n = 1.1 the same accounting gives P_gross = 242 MW, P_net = 172 MW — a ±10% band that is dominated by M_n and by what house loads are counted. The paper does not state its M_n; M_n ≈ 1.2 is the value that closes its numbers.

**Corpus sufficiency: good.** Corpus gave η_th, η_wp, all power quantities, and the anchor; pretraining gave the 4:1 split and the M_n range. The one unstated corpus parameter (M_n) had to be inferred by consistency.

---

## Relation 3 — Magnet/coil capital cost scaling

### Functional form

```
C_magnet = C_conductor + C_structure

C_conductor = c_hts · L_tape,    L_tape = (2π R B0 / μ0) · ℓ_coil / I_tape(B_pk, T_op)
C_structure = c_fab · M_struct,  M_struct = k_st · ρ E_mag / σ_allow,   E_mag ≈ (B0²/2μ0)·V_field
```

### Physical justification of the scaling form

**Conductor should scale with ampere-meters.** Ampère's law fixes the total toroidal-field ampere-turns regardless of design details: N·I = 2πR B0/μ0 [pretraining: Ampère's law]. Each ampere-turn must travel the coil perimeter ℓ_coil, and HTS tape carries a current I_tape that *degrades with peak field and operating temperature*, so conductor length — and cost, since REBCO is priced per meter — is (ampere-turns × perimeter)/I_tape. This is the classical "$/kA·m" costing basis; the ARIES cost-account documentation states TF coil cost is "parametrically determined by the field strength and the current density" [corpus: `knowledge/sources/aries_cost_account_documentation/output.md`, lines 1317–1322] and PF coil cost is "proportional to field strength, current density, and perhaps some volume or stored energy" [same file, line 1475].

**Structure should scale with stored magnetic energy.** The virial theorem bounds the minimum structural mass reacting magnetic forces: M_min = ρ E_mag/σ_allow [pretraining: standard magnet engineering (virial limit)]. Real designs sit a large factor k_st above the bound (margins, discrete geometry, out-of-plane loads, gravity/seismic support). Structure cost is then mass times a fabricated-cost rate.

### Anchored constants (all corpus)

- **c_hts = $18–36/m** of 12 mm REBCO tape, 2014$ [ARC Table 10, image-verified `images/page_028_table_1.png`].
- **I_tape ≈ 660 A** at 23 T / 20 K (70 kA cable ÷ 106 tapes) [ARC, lines 1025–1095].
- **Model validation on ARC internals**: N·I = 2π×3.3×9.2/μ0 = 1.52×10⁸ A-turns; tape count = 1.52e8/660 ≈ 230,000 (paper: 106 tapes × 120 cables × 18 coils = 229,000); with the paper's 5730 km total, implied ℓ_coil = 25 m — a sensible D-coil perimeter for a ≈ 1.13 m plus blanket. The ampere-meter model reproduces the corpus tape inventory to ~1%.
- **Equivalent unit cost**: c_A = c_hts/I_tape ≈ **$27–55 per kA·m** at the ARC field/temperature point.
- **c_fab = $1.06M/tonne** fabricated-component scaling (FIRE/BPX/PCAST/ARIES-RS average, FY2014$) [ARC, line 1558]; raw SS316LN is $9.6/kg [ARC Table 10].
- **k_st (weak anchor)**: ARC stored energy 18 GJ → virial minimum ρE/σ = 7900×18e9/6.6e8 ≈ 215 t (σ_allow = 660 MPa, the ARC FEM stress level [ARC, line 1113]). ARC's magnet structure is 4350 t → k_st ≈ 20. Caveat: that mass conservatively includes the reactor base modeled as solid steel [ARC, lines 1626–1628], so k_st = 20 is an upper bracket; the physically-loaded structure is likely k_st ~ 5–10 [judgment].

### Field-dependence note

Cost rises faster than linearly in B0: ampere-meters ∝ B0·R, but I_tape falls as B_pk grows, and B_pk = B0/(1 − ε − Δb/R) [ARC Eq. (9)] — plus structure grows as B0². This is the physical reason high-field compact designs trade conductor+structure premium against smaller everything-else, which the ARC paper argues nets out favorably [ARC, lines 1639–1642].

### Validity range

- Superconducting toroidal-field-like coil sets (tokamak TF; stellarator encircling coils with modifications below). Tape price and I_tape are technology-and-date-specific — re-anchor for any other year or conductor. FOAK material+fabrication only; no learning curve, contingency, or installation. The Applied Energy TEA re-uses these same ARC quantities with learning-rate adjustments [corpus: `knowledge/sources/tea_dt_mfe_cost_analysis/output.md`, lines 310–330, 505–507], and prices auxiliary systems at $2.5/W (heating) and $1.5/W (power supplies), $300/kW cryocooling at 20 K [same file, lines 493–500] — useful companions but not part of the coil relation.

### Worked example — ARC

- L_tape = 1.52e8 × 25 m / 660 A = 5,760 km (paper: 5,730 km) → C_conductor = 5730 km × $18–36/m = **$103–206M**
- C_structure = 4350 t × $1.06M/t = **$4.6B** fabricated (materials-only $42M); magnet/structure subtotal **$5.1–5.2B** [reproduces ARC Table 11, image-verified `images/page_029_table_0.png`]
- Total magnet system ≈ **$4.8–5.4B** FOAK-fabricated, dominated (>90%) by the structure fabrication multiplier — the single most uncertain constant in this relation. On a materials basis the magnet is only ~$160–260M.

**Corpus sufficiency: good for form and conductor anchor; weak for the structure multiplier.** The corpus pins the ampere-meter scaling and tape price precisely, but the only structure-cost anchor is ARC's deliberately rough $/tonne scaling with a conservative mass. A cross-machine k_st and c_fab calibration would need ARIES systems-code mass/cost tables that are not in the extracted corpus.

---

## Stretch — modular stellarator coil relation

How the coil relation changes, from the Helios overview [corpus: `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/output.md`]:

1. **Same functional form, worse constants.** Ampere-meters and stored-energy structure still govern, but a stellarator needs a minimum plasma–coil standoff for shielding (Helios enforces 1.2 m, line 331 and abstract) and higher aspect ratio (4.5), so ℓ_coil per ampere-turn and the field-volume V_field are larger for the same plasma.
2. **Lower axis field per on-coil tesla.** Helios: 20 T on-coil supports only ~6 T on axis (the paper states 25 T on-tape would give 7.5 T on axis, line 149) — a B0/B_pk ratio ~0.3 vs. ~0.4 for ARC. Since P_fus ∝ B0⁴, this compounds: more conductor per delivered fusion watt.
3. **A 3-D complexity multiplier on fabrication.** Modular non-planar coils (NCSX, W7-X) showed cost/schedule overruns from manufacturing complexly curved coils to tight tolerance [Helios, line 49]; NCSX was cancelled mid-manufacturing. So C_structure and winding cost carry a complexity factor f_3D > 1 (order 2–5 [judgment; corpus gives direction, not magnitude]). The planar-coil architecture (12 encircling + 324 identical-pancake shaping coils, lines 147, 293–299) exists precisely to push f_3D back toward 1 and to relax tolerances via controllable shaping coils.
4. **Coil count/spares economics differ**: 324 identical shaping-coil pancakes are a manufacturing-learning play [Helios, line 299]; tokamak TF coils (12–18 units [ARIES doc, line 1297]) get no such series effect.

Net: C_stellarator-coils ≈ f_3D · [same ampere-meter + virial-structure relation] evaluated with longer ℓ_coil, larger V_field, and lower B0/B_pk. The corpus supports the form and the direction of every correction but quantifies none of the multipliers — a real insufficiency.
