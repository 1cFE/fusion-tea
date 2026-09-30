# Evidence note — nb3sn-highfield (REQ-MMC-NB3SN-WP-02)

Bottom line: one primary source now gives a fusion Nb₃Sn TF conductor designed above 13 T. It is the EU DEMO high-grade react-and-wind (R&W) conductor of Bruzzone et al. 2015, designed for 82.4 kA at 13.50 T with a 1.5 K temperature margin. Its full cable and conduit geometry is printed, so non-Cu and conductor current densities follow by arithmetic (305 A/mm² non-Cu, 24.2 A/mm² bare conductor). It was tested only to 70 kA at 12.35 T background, and its requirements came from a 2012 PROCESS run that the 2018 EU DEMO baseline (12 T) superseded. The roadmap (Mitchell et al. 2021) adds the EU DEMO vs ITER parameter table, a JA DEMO design point, a 118 kA / 12 T EU DEMO conductor proposal, and the ITER-2008 critical-current parameters with a margin-cost curve at 12 T. No source gives a Nb₃Sn winding-pack current density above 12.2 T.

**Premise conflict, surfaced (not resolved).** The class brief describes "EU DEMO TF about 83 kA / 13.7 T". The roadmap attributes 83 kA in 13.7 T under 800 MPa to its ref. [1], K. Tobita et al., Fusion Sci. Technol. 75 (2019) 372. That is the Japanese JA DEMO programme, not EU DEMO. The roadmap's own EU DEMO table gives 12 T maximum TF field. The EU DEMO point closest to the brief's numbers is the older 82.4 kA / 13.50 T design registered here. Anything downstream that labels 83 kA / 13.7 T as EU DEMO should be corrected or carried as JA DEMO.

## Sources

- **Registered this run.** `knowledge/sources/superconductors_for_fusion_a_roadmap_mitchell_et_al_sust/` — N. Mitchell, J. Zheng, C. Vorpahl, V. Corato, … G. Liu, "Superconductors for fusion: a roadmap", Supercond. Sci. Technol. 34 (2021) 103001, DOI 10.1088/1361-6668/ac0992. EPFL Infoscience accepted manuscript v11 (15 Mar 2021), 89 pages, https://infoscience.epfl.ch/server/api/core/bitstreams/5b1da360-8a7f-4b56-ac11-05a81fd4344e/content. A review made of short signed articles; section authors are named per row below. Stored PDF present. Manuscript page numbers equal PDF page indices.
- **Registered this run.** `knowledge/sources/design_manufacture_and_test_of_a_82_ka_react_wind_tf/` — P. Bruzzone, K. Sedlak, B. Stepanov, R. Wesche, L. Muzzi, M. Seri, L. Zani, M. Coleman, "Design, Manufacture and Test of a 82 kA React&Wind TF Conductor for DEMO", EUROfusion preprint CP(15)09/01, paper 4OrBC_04, MT-24 (Seoul, Oct 2015), https://scipub.euro-fusion.org/wp-content/uploads/2015/11/EFCP150901.pdf. 7-page preprint; PDF p.1–2 are the EUROfusion cover, so paper p.N = PDF p.N+2. Stored PDF present.
- **Pre-existing, cross-checked, not re-registered.** Demattè & Bruzzone (`knowledge/sources/eu_demo_rw_tf_coil_conductor_dematte_bruzzone/`), Sedlak et al. 2020 (`knowledge/sources/advance_in_the_conceptual_design_of_the_european_demo/`) and Breschi et al. 2017 (`knowledge/sources/performance_analysis_of_the_toroidal_field_iter_production/`), as used in `evidence/sources/nb3sn-winding.md`.

Short names below: **BR15** = Bruzzone et al. 2015; **RM** = roadmap (section author in brackets).

## Evidence table

### A — EU DEMO high-grade R&W TF conductor at 13.5 T (BR15)

| quantity | value and units | exact location | basis | measured domain | fitting domain or extrapolation | classification | original inspected |
|---|---|---|---|---|---|---|---|
| design operating field | 13.50 T | BR15 output.md:61; paper p.1 §II (PDF p.3) | high-grade (highest-field) Nb₃Sn conductor; "operating field", not stated as peak or effective | design | n/a | directly supported | PDF p.3 rendered |
| operating current | 82.4 kA | BR15 output.md:61; paper p.1 §II | per turn | design | n/a | directly supported | PDF p.3 rendered |
| temperature margin | "roughly constant" 1.5 K over the winding cross section, by six Nb₃Sn grades | BR15 output.md:31; paper p.1 abstract | temperature margin; operating temperature not printed | design | n/a | directly supported (operating temperature unavailable) | PDF p.3 rendered |
| winding layout | double-layer winding, six Nb₃Sn grades, NbTi for double layers with B ≤ 6 T | BR15 output.md:61; paper p.1 §II | TF coil | design | n/a | directly supported | PDF p.3 rendered |
| design basis | PROCESS system code run of July 2012 and 2013 CAD model | BR15 output.md:55; paper p.1 | requirement provenance | — | — | directly supported | PDF p.3 rendered |
| strand | 1.5 mm diameter, Cu:non-Cu = 1, twist 25 mm; specified Jc ≥ 1000 A/mm² at 12 T, 4.2 K; delivered average up to 15 % higher | BR15 output.md:33, :80; paper p.1 abstract, p.2 Fig. 1 | non-Cu Jc; E-criterion of the specification not printed | strand acceptance | n/a | directly supported | PDF p.3–4 rendered |
| cable | (1Cu+6+12) × 17 = 306 Nb₃Sn + 17 Cu strands; flat 11.9 × 62.6 mm; void fraction 15 % specified, ≈ 27 % as built; steel strip 40 × 0.2 mm specified, missing as built | BR15 output.md:80; paper p.2 Fig. 1 | as-built vs specification (struck-through values are the specification) | one 12 m cable | n/a | directly supported | Fig. 1 rendered at 120 dpi |
| cable with copper | 17.8 × 68.5 mm, 48 Cu wires ø 2.9 mm, RRR 500 (specified 53 × ø 3.0 mm) | BR15 output.md:80; paper p.2 Fig. 1 | segregated Cu layer | as built | n/a | directly supported | Fig. 1 rendered |
| conduit | 100 mm × 34 mm; drawing shows 100 wide, 17 per half-profile, 68.5 × 8.9 inner half-cavity, corner R3 | BR15 output.md:106; paper p.2 §II.C, Fig. 3 | bare conductor envelope, no insulation | prototype | n/a | directly supported | Fig. 3 rendered |
| bending-strain design rule | tcable ≤ 2 Rht εb = 14.3 mm, with Rht = 2 Rmin = 7.18 m and εb = ±0.1 % | BR15 output.md:71; paper p.1 §II | cable as a solid body | design | n/a | directly supported | PDF p.3 rendered |
| strain | thermal strain estimate ≈ −0.28 %; scaling-law fit ε ≈ −0.33 %; strain distribution about 0.05 % | BR15 output.md:153, :161, :171; paper p.4 §III.B, §IV | conductor effective strain from DC test fit | Left conductor, 12.35 T background, ≤ 70 kA | fit, one sample | directly supported | PDF p.6 text layer |
| effective field in test | Beff = Bbackground + 0.0084 · Iop (Iop in kA) | BR15 output.md:155; paper p.4 | EDIPO sample incl. self field and return leg | EDIPO sample only | n/a | directly supported | PDF p.6 text layer |
| test domain | DC tests at I ≤ 70 kA, 12.35 T background → Beff ≈ 12.94 T; quench above 82.1 kA when background > 5 T (termination artifact) | BR15 output.md:135, :139; paper p.3 §III | EDIPO | ≤ 70 kA, Beff ≤ 12.94 T | 82.4 kA at 13.5 T not tested | directly supported; Beff derived: 12.35 + 0.0084 × 70 = 12.94 T | PDF p.5 text layer |
| electric-field and n-index | take-off field ≈ 30 µV/m; n = 13 (about half the free strand) | BR15 output.md:157; paper p.4 | DC runs | test | n/a | directly supported | PDF p.6 text layer |
| Tcs values | plotted only (Fig. 6: Tcs at 60 kA, 12.35 T rose ≈ 0.4 K after re-termination) | BR15 output.md:139, :141 | — | — | — | unavailable as numbers (figure values not read off) | not inspected |
| non-Cu area | 270.4 mm² | derived | 306 strands | — | — | derived: 306 × π/4 × 1.5² / 2 = 270.4 mm² | — |
| non-Cu J at design | 305 A/mm² | derived | non-Cu, 82.4 kA | design | n/a | derived: 82 400 / 270.4 = 304.8 A/mm² | — |
| SC-strand J at design | 152 A/mm² | derived | whole Nb₃Sn strands, 540.7 mm² | design | n/a | derived: 82 400 / 540.7 = 152.4 A/mm² | — |
| cable-space J at design | 67.6 A/mm² | derived | 68.5 × 17.8 mm rectangle, corner radii and side channels ignored | design | n/a | derived: 82 400 / 1219.3 = 67.6 A/mm² | — |
| conductor J at design | 24.2 A/mm² | derived | bare conduit 100 × 34 mm, no insulation | prototype | n/a | derived: 82 400 / 3400 = 24.24 A/mm² | — |
| operating fraction of strand spec | 0.305 | derived | Iop / (spec Jc × non-Cu area) at 12 T, 4.2 K, not at operating conditions | — | — | derived: 82 400 / (1000 × 270.4) = 0.305 | — |
| winding pack (turns, dimensions, insulation) | not given | — | — | — | — | unavailable | — |

### B — Design points and margins in the roadmap (RM)

| quantity | value and units | exact location | basis | measured domain | fitting domain or extrapolation | classification | original inspected |
|---|---|---|---|---|---|---|---|
| EU DEMO vs ITER TF (Vorpahl & Corato) | max TF 12 T vs 11.8 T; 16 vs 18 coils; 5.3 T on axis both; R 9.1 vs 6.2 m; stored 150 vs 41 GJ; discharge τ 35 vs 11 s; centring force 850 vs 400 MN per TF | RM p.20 Table 1; table rows not found by grep in output.md (text resumes at :339) | system specification | design | n/a | directly supported | p.20 rendered |
| EU DEMO TF option #1 field headroom | R&W layer-wound graded option "capable of achieving ~20% higher field" | RM output.md:339; p.20 | versus the 12 T specification | design claim | n/a | directly supported; 14.4 T is a derived reading (12 × 1.2), not printed | p.20 rendered |
| EU DEMO ampere-turns per TF coil | 15.07 MA | derived | 2πR·B0/μ0 / 16 | — | — | derived: 9.1 × 5.3 / 2×10⁻⁷ = 241.2 MA total, / 16 = 15.07 MA; Demattè & Bruzzone give 14.9 MA per coil | — |
| JA DEMO TF conductor (Miyoshi, Banno, Saito) | 83 kA in 13.7 T under 800 MPa; ITER TF 68 kA in 11.8 T under 670 MPa | RM output.md:647; p.38 ¶1, ref. [1] = Tobita et al., Fusion Sci. Technol. 75 (2019) 372 | conductor current and field; stress basis not stated | design | n/a | directly supported as a secondary citation; primary not captured | p.38 rendered |
| strain, W&R vs R&W (Miyoshi et al.; Sedlak) | ITER TF wires under thermal strain −0.7 % to −0.5 %; R&W −0.3 %; RW ε ≈ −0.3 % vs WR ε ≈ −0.7 % | RM output.md:649 (p.38); :1043 (p.66) | thermal/axial strain in Nb₃Sn | review statement | n/a | directly supported | p.38 rendered; p.66 text layer |
| R&W vs ITER conductor test (Sedlak) | EU DEMO RW conductor, 132 mm² Nb₃Sn: Tcs = 7.42 K at 10.9 T, 68 kA; ITER TF, 238 mm² Nb₃Sn: Tcs = 6.3–6.5 K | RM output.md:1043; p.66 | SULTAN, ITER-like conditions | 10.9 T, 68 kA | n/a | directly supported; non-Cu J derived: 68 000/132 = 515 A/mm² vs 68 000/238 = 286 A/mm² (matches nb3sn-winding note, 286.1) | p.66 text layer |
| EU DEMO RW graded WP (Sedlak) | 12 layers; lowest-field layer 6.2 T needs 25 % of the Nb₃Sn of the 12.2 T layer; ~50 % saving from grading, ~73 % with strain; 222 t vs 835 t strands | RM output.md:1055; p.67 | Nb₃Sn strand mass | design | n/a | directly supported | p.67 rendered |
| high-Jc field headroom (Sedlak) | APC high-Jc strands in the highest-field layer would allow about 10 % higher field on plasma axis | RM p.68 "High-Jc Nb3Sn strands" | design claim | — | — | directly supported (qualitative) | p.68 text layer |
| 118 kA EU DEMO TF conductor (Bruzzone & Wesche) | 118 kA / 12 T R&W; 126 turns per coil; conductor ≈ 73 × 46 mm (cartoon); ITER TF 68 kA / 11.7 T, 44 mm | RM output.md:805, :815; p.48–49 Fig. 2 | proposal for reduced voltage (< 4 kV at τ = 35 s) | cartoon, not designed in detail | n/a | directly supported; J derived: 118 000 / (73 × 46) = 35.1 A/mm² bare; 126 × 118 kA = 14.87 MA per coil | p.49 rendered |
| margin definition and cost (Schild) | ΔT = Tcs − (Top + transient temperature rise); Nb₃Sn amount vs Tcs − 4.5 K at 12 T: 100 % at 0, 137 % at 1 K (printed); ≈ 116 % at 0.5 K, ≈ 169 % at 1.5 K, ≈ 217 % at 2 K (read from plot) | RM output.md:856, :860; p.51–52 Fig. 1 | ITER-2008 correlation, 4.5 K operating, 12 T peak; operating strain not printed | calculation | n/a | 137 % directly supported; other points bounded assumption (read from plot, about ±3 %) | p.52 rendered |
| ITER TF margin (Schild) | "for ITER TF conductor this margin is 0.7 K"; transient rise 0.5–1.0 K typical | RM output.md:862; p.52 | ΔT as defined above | statement | n/a | directly supported; see Gaps for how it relates to the 5.7 K Tcs floor | p.52 rendered |
| practical field range statements | large devices "12 to 13 T in coil" (Kario & ten Kate); hybrid high-Jc Nb₃Sn + NbTi "for the magnetic field less than 16T", HTS + LTS above (Zheng); CFETR TF maximum ≈ 15 T with high-Jc Nb₃Sn, ITER-grade Nb₃Sn and NbTi grades | RM output.md:721 (p.42); :263 (p.14) | descriptive, no derivation | — | — | directly supported as statements; no engineering limit is derived | p.14 rendered |
| CFETR TF winding pack | WP 805.4 (and 929.5) × 1151.4 mm, three field grades; conductor lengths 2000 / 3200 / 1700 m | RM p.14–15 Fig. 1 | no current, turns or field per grade | — | — | directly supported; current density unavailable | p.15 rendered |
| Nb₃Sn wire records (Miyoshi et al.) | RRP non-Cu Jc 3000 A/mm² at 12 T, 4.2 K; FCC prototypes ~1800 A/mm² at 14 T and ~1000 A/mm² at 16 T, 4.2 K; DT wire ~1100 A/mm² at 16 T; none meets both high Jc and low hysteresis for DEMO | RM p.38–40 | non-Cu, 4.2 K, wire only | wire tests | n/a | directly supported | p.38 rendered; p.39–40 text layer |

### C — REBCO numbers, flagged for the rebco class (not used here)

| quantity | value and units | exact location | basis | classification | original inspected |
|---|---|---|---|---|---|
| CFS tape specification | Je > 700 A/mm² at 20 K, 20 T, worst angle; ~500 km ordered mid-2019 | RM output.md:469; p.27 | engineering current density of tape | directly supported | p.27 text layer |
| Tokamak Energy Jwp | CICC-type REBCO typically Jwp < 100 A/mm²; ~75 A/mm² (CIC) vs ~350 A/mm² (stacked pancakes) for a 1.4 m, 4 T ST; target Jwp 350 A/mm² | RM output.md:593, :607 region; p.33–35 | winding pack | directly supported | p.33–35 text layer |
| NI stack test | > 24 T peak on coil at 21 K, average Jwp > 700 A/mm² (no-insulation, solder-impregnated) | RM output.md:603; p.34 | winding pack | directly supported | p.34 text layer |
| CORC | full-size CICC to 60 kA in 12 T (EDIPO, SULTAN), with degradation; CORC insert 16.77 T, > 4 kA, winding J 169 A/mm² | RM p.78 | cable and winding | directly supported | p.78 text layer |
| field and temperature regime | compact machines "25 to 30 T in coil", 20–30 K | RM output.md:721; p.42 | descriptive | directly supported | p.42 text layer |

## Equations

- **BR15 effective field** (paper p.4, text): Beff = Bbackground + 0.0084 · Iop, with Iop in kA and B in T. It is specific to the EDIPO sample geometry (self field plus return conductor). It does not transfer to a coil.
- **BR15 bending rule** (paper p.1): tcable ≤ 2 Rht εb, with Rht = 2 Rmin = 7.18 m and εb = ±0.1 %, giving 14.3 mm. This treats the cable as a solid body.
- **BR15 scaling law**: the fit uses "the scaling parameters [10], and the scaling law"; ref. [10] and the parameter values are not printed. The law is not reproducible from this source.
- **RM Schild Fig. 1, ITER-2008 correlation parameters** (p.52, figure box, exists as vector text): C = 21851, Bc20max = 29.39, Tc0max = 16.48, p = 0.556, q = 1.698, Ca1 = 45.74, Ca2 = 4.431, ε0,a = 0.00232, εmax = −0.00061. Units are not printed (C is presumably A·T, Bc20max in T, Tc0max in K). The applied strain used for the curve is not printed. The functional form is only named ("ITER-2008 critical current correlation [1]"), not written. The percentages are ratios of superconductor cross section, so they do not depend on which area C is per.
- **RM Schild heat-load relation** (p.53): P = Ec · Iop · (Iop / Ic(Top − Tcs))ⁿ, with Ec = 10 µV/m. It gives heat per unit length when operating above Tcs.
- **Current-density denominators used here**: non-Cu = strand area / (1 + Cu:non-Cu); SC strand = whole Nb₃Sn strands; cable space = rectangle inside the conduit including the Cu wires; conductor = bare conduit envelope without insulation. No winding-pack density is computed, because no winding pack is given.

## Gaps

- **No Nb₃Sn winding-pack current density above 12.2 T.** BR15 gives the conductor, not the pack; CFETR gives pack dimensions but no current. The comparison can claim sourced Nb₃Sn conductor density at 13.5 T (24.2 A/mm² bare), not a winding-pack density there.
- **13.5 T is a design point, not a demonstrated one.** BR15 reached 70 kA at Beff ≈ 12.9 T. The comparison cannot claim a tested fusion Nb₃Sn conductor above about 12.9 T from captured sources.
- **The 13.5 T EU DEMO point is superseded and PROCESS-derived.** It rests on a 2012 PROCESS run; the 2018 baseline dropped to 12 T. It shows what was designed, not what EU DEMO now specifies.
- **Operating temperature for BR15 unavailable.** It states a 1.5 K margin but no inlet temperature. Sedlak 2020 uses 4.5 K for later designs; applying it here would be a bounded assumption.
- **JA DEMO primary not captured.** The 83 kA / 13.7 T / 800 MPa point is secondary (via RM). Tobita et al. 2019 was not attempted because the capture limit (2) was spent.
- **Practical peak-field limit has no derived basis.** RM gives ranges and designer statements (12–13 T in coil for large machines; high-Jc Nb₃Sn hybrids up to 16 T; CFETR ~15 T; ~20 % EU DEMO headroom; ~10 % more with APC strands). None derives a limit. The comparison may cite these as the stated design envelope, not as a physical limit.
- **ITER TF margin definitions differ.** Schild's 0.7 K is Tcs minus (4.5 K plus transient rise). The nb3sn-winding note's 1.2 K is the 5.7 K Tcs floor minus 4.5 K. They are consistent if the transient rise is 0.5 K, inside Schild's 0.5–1.0 K range. That is a derived reading, not stated by either source.
- **Plotted Tcs values in BR15 Figs. 6 and 8 not read.** The fit strain (−0.33 %) is printed and is the usable result.

## Run

- Run directory: `knowledge/research/requests/runs/REQ-MMC-NB3SN-WP-02/20260929T231827864007/`
- Return class: **REGISTERED** (closed with adequacy `limit_reached`: 2 of 2 captures used, 2 of 5 searches).
- Registered: `knowledge/sources/superconductors_for_fusion_a_roadmap_mitchell_et_al_sust/`, `knowledge/sources/design_manufacture_and_test_of_a_82_ka_react_wind_tf/`.
- Queued for the owner: none.
- Not attempted (capture limit): Tobita et al., Fusion Sci. Technol. 75 (2019) 372 (JA DEMO primary); Bruzzone et al., "Design of Large Size, Force Flow Superconductors for DEMO TF Coils", IEEE TAS 24 (2014) 4201504 (BR15 ref. [5], likely the 13.5 T winding pack); EPFL Infoscience record 198312 from the search.
- Clean-room: the roadmap's reference list cites an "ARIES-I class" REBCO demountable-TF paper twice (Mangiarotti, output.md:1025 region). ARIES-I is a tokamak study, not ARIES-CS. Those references were not opened or used. BR15 has no ARIES mention.
