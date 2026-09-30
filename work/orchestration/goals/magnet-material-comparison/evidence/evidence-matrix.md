# Evidence matrix and data-sufficiency finding (v1)

Goal `magnet-material-comparison`, task T-002. Coordinator synthesis of the five wave-1 evidence notes in `evidence/sources/` and the model audit `evidence/binding-audit.md`. Every value below is carried from those notes, which give the repository `file:line` and the original page, table or figure behind it; the “Note” column names the note. Wave-2 requests (T-003) are still running and will be folded in as v2. Nothing here has yet had the independent source/math check the brief requires before dependent modeling.

Classification: **D** directly supported, **Der** derived by arithmetic from supported values, **BA** bounded assumption (bound stated), **U** unavailable.

## Finding

[AGENT] **The evidence supports a useful conditional comparison over a common peak-field range of roughly 8–12 T, with REBCO near 20 K and Nb₃Sn with a 4.5 K inlet.** Both materials have a sourced field/temperature current law over that range, and each has at least one sourced construction from which conductor and winding current density follow. Refrigeration efficiency and cost are supported as ranges. The comparison cannot claim a production-average Nb₃Sn strand, a qualified insulated REBCO fusion winding at 12 T, sourced magnet cold-load magnitudes at 4.5 K, or a common-condition price pair for both materials; those enter as bounded assumptions and sensitivities.

[AGENT] **The non-superconducting construction dominates winding size, and it differs between the two sourced constructions far more than the superconductors do.** Per kiloampere of turn current, the EU DEMO Nb₃Sn winding uses about 35.7 mm² of gross winding area (10.7 mm² copper, 9.4 mm² jacket steel, 3.0 mm² superconducting strand), while the Stellaris REBCO winding uses 8.4 mm² (2.9 copper, 1.0 solder, 3.0 steel, 0.76 tape) (Der, below). Those copper and steel allowances reflect each design's own protection and structural choices, not the conductor material. A fair comparison must hold the non-superconducting construction on a stated common basis, or attribute its differences explicitly, and must test that basis as one of the consequential uncertainties.

## 1. Conductor identity and critical-current law

| Quantity | Value | Class | Note |
|---|---|---|---|
| Nb₃Sn law form | ITER form Jc = (C/B)·s(ε)·(1−t^1.52)(1−t²)·b^p(1−b)^q with printed strain function | D | nb3sn-law (Tsui eq. 6–7) |
| Nb₃Sn parameter set | BEAS II bronze-route ITER TF strand, full-range fit: p 0.489, q 1.618, C 2.227e10 A T m⁻², Ca1 226.93, Ca2 203.86, ε0,a 0.187 %, εM −0.366 %, Bc2*(0,0) 30.28 T, Tc*(0) 16.02 K | D | nb3sn-law (Tsui Table 5c) |
| Nb₃Sn basis | engineering Jc (whole strand area), 10 µV/m; measured 4.2–12 K, ≤14.5 T, strain −1.1 to +0.5 %; 4.5 K is interpolation | D | nb3sn-law |
| Nb₃Sn strain convention | εM sign differs across sources; must be fixed before evaluation | U (to resolve in check) | nb3sn-law |
| Nb₃Sn production-average law | Bottura–Bordini not captured | U | nb3sn-law (queued) |
| REBCO tape Ic, 20 K, B⊥tape | 220–270 A per 4 mm at 20 T (three samples); production average ≈198 A at 20 T | D / Der | rebco (Molodyk Fig. 1a, p. 77) |
| REBCO field shape 5–20 T at 20 K | measured curve: Ic(B)/Ic(20 T) = 2.11, 1.85, 1.61, 1.33 at 8, 10, 12, 15 T; the model's (B/20)^−0.6 gives 1.73, 1.52, 1.36, 1.19 | Der (digitized) | rebco |
| REBCO field law, alternative | Jc ∝ B^−α, α ≈ 0.55–0.75 over 0.5–19 T at T ≤ 30 K, 2015 tapes | D | rebco (Senatore) |
| REBCO temperature law | Jc ∝ exp(−T/T*), T* ≈ 17–33 K (8–19 T); ≈22 K implied for the fusion tape → about −4.5 %/K near 20 K | D form / Der value | rebco |
| REBCO tape construction | 4 mm × 56 µm (40 µm Hastelloy, ≈2.4 µm YBCO, Ag, 5 µm Cu per side) | D | rebco (Molodyk) |
| Curvature conflict | Molodyk curve steepens above ≈10 T; Senatore reports a constant power law | carried as a sensitivity, not an owner gate: both are measured laws on different tapes | rebco |

## 2. Conversion to conductor and winding pack

| Quantity | Value | Class | Note |
|---|---|---|---|
| Nb₃Sn construction A (EU DEMO R&W layer 1) | 104.95 kA at 12.04 T, sized at 6.5 K and −0.3 %; 399 × 1 mm strands, Cu:non-Cu 1; 20 % void; 68 × 37.9 mm conductor, 5 mm jacket; 1123.7 mm² total Cu; 982.7 mm² steel | D | nb3sn-winding (Demattè Table I, p. 3–4) |
| Nb₃Sn winding pack A | 142 turns in 1296 × 411 mm → 28.0 A/mm² gross; bare conductors fill 76 % | Der | nb3sn-winding |
| Nb₃Sn construction B (ITER TF) | 68 kA at 11.8 T; 900 Nb₃Sn + 522 Cu strands, 0.82 mm; 43.7 mm OD, 2 mm jacket; void ≈30 %; 45.3 A/mm² over bare conductor; ITER winding pack unavailable | D / Der / U | nb3sn-winding |
| Nb₃Sn in-cable degradation | ITER CICC effective strain −0.55 to −0.97 %; strand keeps ≈37 % of free-wire Ic; EU DEMO R&W prototype −0.27 % | D | nb3sn-winding (Breschi, Sedlak) |
| Nb₃Sn insulation | turn plus ground insulation and fillers ≈72–74 mm across the DEMO pack; turn insulation alone unavailable | BA / U | nb3sn-winding |
| REBCO winding composition | Stellaris Table 7: tape stack 9 %, copper jacket 35 %, solder 12 %, steel 36 %, helium 8 %, for 24.9 T at 20 K; insulation not listed | D | admissible `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png`; model `stellarator_plant.sysml:368-379` |
| REBCO fusion windings (no insulation) | SPARC TFMC 153 A/mm² at 20.1 T, 20 K; SPARC TF design 94 A/mm² at 23 T; area basis not stated | D | rebco (Hartwig Table I) |
| REBCO tape-to-cable degradation | not sourced | U | rebco |
| Per-kA construction areas | DEMO: gross 35.7, Cu 10.7, steel 9.4, strand 3.0 mm²/kA. Stellaris: gross 8.4, Cu 2.9, solder 1.0, steel 3.0, He 0.7, tape 0.76 mm²/kA | Der (coordinator: 1296 × 411/142/104.95; 360²/308/50 × fraction) | this matrix |

## 3. Operating margins and limits

| Quantity | Value | Class | Note |
|---|---|---|---|
| Nb₃Sn temperature margin | EU DEMO requirement Tcs ≥ 6.7 K = 4.5 K inlet + 0.7 K nuclear + 1.5 K; Demattè sizes at 6.5 K for a 2 K margin; ITER Tcs floor 5.7 K | D (two conventions, both carried) | nb3sn-winding |
| REBCO margin | current model uses an allowable operating fraction 0.8 at 20 K (its basis to be read in the model); no sourced REBCO temperature-margin criterion yet | to check | binding-audit §1 |
| Mechanical, protection, irradiation limits | not evaluated in this comparison; REBCO strain/transverse limits registered but not a matched check | limits interpretation | binding-audit; SOURCE_INDEX |

## 4. Cryogenic loads and refrigeration

| Quantity | Value | Class | Note |
|---|---|---|---|
| Carnot specific power | 65.7 W/W at 4.5 K; 14.0 W/W at 20 K; ratio 4.69 | D / Der | cryo (Strobridge Eq. 1) |
| Fraction of Carnot | one curve for 1.8–90 K: ≈19 % at 1 kW, 24 % at 10 kW, 29 % at 100 kW; “proportionally the same” losses at 10–30 K | D (graph reading ±15 %) | cryo (Strobridge Fig. 1) |
| Plant-level check | ITER 0.24 of Carnot plant-wide over mixed 4.5 K and 80 K loads; not a single-stage law | Der | cryo |
| Size variable | efficiency may track cooling capacity or compressor power; unresolved | BA (sensitivity) | cryo |
| Current-lead cold-end load | ≈47 W/kA conduction-cooled into 4.2 K, ≈46.9 W/kA at 20 K (ideal) | D / Der | cryo (Ballarino) |
| Magnet cold-load magnitudes at 4.5 K | unavailable in wave 1; the model's 20 K Stellaris load categories exist (nuclear 35.5 W/m³, joints 7.5 kW, radiation/conduction/lead inventory valid 10–30 K) | U / model-inherited | cryo; binding-audit §4 |

## 5. Cost basis

| Quantity | Value | Class | Note |
|---|---|---|---|
| REBCO tape | 80 USD/m of a 400 A (20 T, 4.2 K) tape = 200 USD/kA·m, 2016 DOE baseline | D | cost (Cooley & Pong) |
| REBCO band | 150–200 USD/kA·m, no condition stated | D (unconditioned) | cost |
| Per-kg pair, one source | Nb₃Sn 2274 EUR/kg, REBCO 8013 EUR/kg (about 2024 EUR, accelerator cost model inputs) | D | cost (HTS paper Table AI-I) |
| ITER TF Nb₃Sn strand | 2505 USD/kg (2014) if 210 t, 1052 USD/kg if 500 t | Der (ambiguous mass basis) | cost |
| Nb₃Sn accelerator strand | >20 USD/kA·m at 16 T, 4.2 K; 1.5–2 MUSD/t | D | cost |
| ITER TF cabling+jacketing, winding | 985 USD/m and 5034 USD/m of turn length (2014) | Der | cost (PROCESS Kovari) |
| 4.5 K refrigerator capital | 7940 USD/W (50 kW basis) or 5293 USD/W (75 kW), 2014 | Der | cost |
| Refrigerator capital vs input power | Strobridge C = 6000·P_in^0.7 USD (1974), 1.8–90 K, P_in installed kW | D (from triage; registered source, value to be checked) | cost; cryo |
| 20 K refrigerator capital, independent | none beyond input-power scaling; PROCESS 4.5/T factor has no basis | BA / U | cost |

## What the gaps prevent

- No production-average Nb₃Sn law: results describe a named qualified ITER TF strand, not ITER production.
- No sourced insulated REBCO fusion winding at 12 T: the REBCO winding is the Stellaris composition re-proportioned for a lower field, a stated design offer, not a qualified design.
- No common-condition price pair: conductor cost at matched duty is derived through each Ic law from differently referenced prices; the answer should use ranges and a break-even REBCO price.
- No sourced 4.5 K cold-load magnitudes: the 4.5 K and 20 K heat budgets are compared on common per-unit loads with a stated assumption; the refrigeration difference is then dominated by the Carnot ratio and cold volume.
- No mechanical, protection or irradiation evaluation: the comparison is a subsystem screening, not a qualified design.

## v2 additions from wave 2 (T-003)

Per-class notes: `evidence/sources/{rebco-winding,nb3sn-highfield,cryo-loads,cost-common}.md`.

| Quantity | Value | Class | Note |
|---|---|---|---|
| HTS protection copper requirement | 100 A/mm² in copper for TF, 120 A/mm² for CS (SPC HTS DEMO conductor requirements) | D | rebco-winding (Bruzzone, Wesche et al. 2016 Table I) |
| REBCO CICC-type conductor | SPC TF prototype 60 kA / 12 T / 5 K design; 20 strands × 16 tapes (4 × 0.1 mm); ≈35.7–37.8 kA at 12 T, 20 K (1 µV/cm); 10–20 % degradation after cycling | D / Der | rebco-winding |
| VIPER cable | Ic 31.5 kA at 10.9 T, 20 K; <5 % fabrication and 2–4 % cycling degradation | D | rebco-winding |
| Nb₃Sn high-field design | EU DEMO R&W high-grade 82.4 kA at 13.50 T, 1.5 K margin; 306 × 1.5 mm strands; 100 × 34 mm conduit; fitted strain −0.33 %; tested only to 70 kA (~12.9 T) | D / Der | nb3sn-highfield (Bruzzone CP(15)09/01) |
| Nb₃Sn practical range | EU DEMO 12 T (2018 baseline), ITER 11.8 T; no derived limit, stated 12–13 T for large coils | D | nb3sn-highfield (Mitchell roadmap) |
| Large 4.5 K refrigerator efficiency | η = 15.5·R(kW)^0.23 % of Carnot; data ≈0.01–35 kW, to 2007 | D | cryo-loads (Green 2015 Eq. 2, re-registered) |
| Large 4.5 K refrigerator capital | C ≈ 3.1·R(kW)^0.65 M$2015 | D | cryo-loads (Green Eq. 1) |
| 4 K static loads, EU DEMO | 5.9 kW: 1.3 kW radiation from 80 K shields, 4.4 kW thermal anchors, 0.2 kW shield supports (nuclear excluded) | D | cryo-loads (Končar Table 1) |
| Radiation at 20 K vs 4 K cold mass | 0.996 of the 4 K value from an 80 K shield | Der / BA | cryo-loads |
| ITER magnet loads | 11.8 kW static + 10.9 kW averaged pulsed; ≈7.4 kW deposited in TF winding packs | D / Der | cryo-loads (ITER FDR 2001) |
| Common-condition prices | Nb₃Sn strand 8.0 USD/kA·m; REBCO tape ≈80 (now), 30 (near-term), 10 (volume) USD/kA·m, all at 6 T, 4.2 K, “2021” | D (secondary for Nb₃Sn) | cost-common (Chislett-McDonald 2022) |
| Price scaling law | cost ∝ 1/Jc(B,T) of whole strand or tape (Eq. 9) | D | cost-common |

[AGENT] Wave 2 changes the finding in two ways. First, a sourced HTS protection-copper requirement (100 A/mm²) is close to the EU DEMO Nb₃Sn value (93.4 A/mm²), so a common protection basis for both materials is supported; the Stellaris winding's copper (≈340 A/mm² over its copper jacket alone, 50 kA / (421 mm² × 0.35)) is a design-specific compact choice. Second, a common-condition price pair and a Jc-scaled cost law now exist, although the Nb₃Sn value is secondary and the currency year is ambiguous; prices remain ranges and a break-even REBCO price is still the honest output. The defective wave-1 Green entry remains in the registry and must not be cited; the re-registered publisher copy supersedes it.

**Correction (2026-09-29, from the independent oracle author's note A6).** `sources/cryo-loads.md` describes 1107.9 kW as the EU DEMO shields' load. Končar Table 1 (rendered pp. 4–5) gives that as the all-component total including the 5.9 kW reaching the 4 K magnets; the shields alone are 912.6 + 189.4 = 1102.0 kW. The comparison uses 1102.0 kW; the load is common to both materials.
