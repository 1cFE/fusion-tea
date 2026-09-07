# Is the stellarator minor radius a free design lever? What the admissible corpus says

> Deposited 2026-09-07 as grounding evidence for goal `minor-radius` from the investigating session's scratchpad (`sources_a/`); the PNG paths named below resolve in this directory. Written by a fresh source-reading agent under the clean room (no `knowledge/holdout/`, the barred Helios overview not opened); no repository file was modified by it.

Read-only source survey, 2026-09-07. Clean room respected: nothing under knowledge/holdout/ and nothing under knowledge/sources/overview_of_the_helios_design_* was opened. No web fetches. Stellaris table values were read from page renders of the raw PDF, never from the markdown extractions; prose passages are marked with which text they came from.

Path abbreviations used below:

- L21 = knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/output.md (Lion et al. 2021, Nucl. Fusion 61 126021). Equation images live in the images/ directory beside it. The raw PDF still exists at /tmp/claude-1000/-home-reid-1cfe-fusion-tea/cf4cbd0c-47f2-43ea-be9f-34ba243b7af5/scratchpad/lion_2021_nf_stellarator_process.pdf (an earlier session's scratchpad; I read it, wrote nothing there).
- L23 = knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/output.md (Lion PhD thesis 2023). Raw PDF at the same earlier scratchpad, lion_2023_phd_thesis_stellarator_systems_code_models.pdf.
- BEI = knowledge/sources/the_helias_reactor_beidler_et_al_iaea_cn_77_ftp1_16/output.md (Beidler et al., IAEA 2001).
- HEL = knowledge/concept_research/05-planar-coil-stellarator/iter-01/sources/thea-energy-helios-arxiv-2512-08027/output.md (Helios overview, arXiv 2512.08027 LaTeXML extraction; this is NOT the barred knowledge/sources copy).
- STX = knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf (Stellaris, Lion et al. 2025 FED). "PDF p.N" is the PDF page index; page text was pulled with pymupdf for prose and every number below was checked on a render.
- L22 = knowledge/sources/a_deterministic_method_for_the_fast_evaluation_and_2/output.md (Lion, Warmer, Xu 2022 NWL paper). NEU = knowledge/sources/neutronics_analyses_for_a_stellarator_power_reactor_based/output.md (HELIAS-5B neutronics). Both registered; both consulted for radial-build and aspect-ratio facts only.

## Q1. Is a an independent variable in stellarator-PROCESS, or does it follow R at fixed aspect ratio?

Plain answer. The code is built so that a *can* be scaled separately from the coil size, but in every published run the aspect ratio is held fixed and only R (plus B, n, T, winding pack) is iterated. A is a fixed input inherited from the reference configuration; a follows from R/A. When the minor radius is changed at fixed coil size, the code does not treat it as free: it charges the change against the plasma-coil distance through a configuration-specific factor f_geo (equation 58). There is no run in either document where a is optimised as a free variable at fixed R.

Supporting quotes.

- Scaling axes (L21:118): "We implement the systems code models in a way that they reflect extrapolations of the reference point C in the following macroscopic design parameters: the major overall size of the machine (coil and plasma size), the minor plasma radius _a_ at constant coil radius, and the total magnetic field strength on axis _B_ t." Same sentence in the thesis (L23:643).
- What is frozen (L21:120): "Note that by this prescription the coil number and the coil shapes are considered fixed by stellarator-Process and only the overall size of the coils is scaled."
- The reference point carries A (L21, section 2, the paragraph before line 118): "'Stellarator optimisation' provides a 3D MHD equilibrium and a set of corresponding, as fixed considered, coil filaments at a reference point in major radius and aspect ratio."
- The three-configuration study (L21:707): "We then run Process in optimization mode where we optimize for minimal major radius at constant aspect ratio and a required net electricity output of 1 GW ... Further, we optimize the major plasma radius and the overall magnetic field strength." Table 2 (L21:722, verified on the PDF render lion2021_p16_full.png) marks "Aspect ratio" with footnote b, "Fixed input parameter", while "Major plasma radius" carries footnote a, "Iteration parameter". Minor radius has no footnote: it is derived.
- The volume/surface scaling that a enters (eq. 5, images/lion_2021_nf_stellarator_process.pdf-0005-03.png): V = V_hat(C) (R/R_hat)(a^2/a_hat^2), S = S_hat(C) (R/R_hat)(a/a_hat).
- Thesis Helias 5 design points (L23:2010-2012, Table 4.2): optimisation vector is "B, R, n, T, coil width, winding pack composition"; a is absent. Thesis Table 4.3 (render thesis_pdfp110_full.png): Advanced R 12.5 m, a 1.02 m; Conservative R 17.1 m, a 1.39 m. Both give R/a = 12.3, the Helias 5 aspect ratio of L21 Table 2. So a moved only because R moved.
- Thesis coil-set study (L23:2338-2340, Table 4.7): "Optimised for B, R, n_e,0, T_e,0, f_ren, Winding Pack Composition and quench timings." Again no a.
- Thesis pilot-plant study (L23:2136, Fig. 4.7 caption): "a stellarator fusion pilot plant using an aspect ratio of 12.5 and with fixed device size". Results are reported in a (0.64 m, 0.72 m) but A is fixed, so these are R choices.

Reference configurations with different aspect ratios (all Helias / W7-X line; all values from L21 Table 2 on the PDF render unless noted):

| Configuration | N_fp | Coils | A | R (m) | a (m) | B_t (T) | Notes |
|---|---|---|---|---|---|---|---|
| Helias 3 | 3 | 30 | 6.36 | 13.7 | 2.16 | 5.42 | min-R optimum at 1 GWe |
| Helias 4 | 4 | 40 | 8.81 | 18.3 | 2.08 | 5.77 | "comparably small plasma-coil distance, namely 1.7 m at reference size" (L21:760) |
| Helias 5 | 5 | 50 | 12.3 | 20.7 | 1.68 | 7.07 | 1.9 m plasma-coil distance at reference size (L21:760) |
| HSR4/18 (BEI Table I, BEI:28-31) | 4 | 40 | 8.6 (18/2.1) | 18 | 2.1 | 5.0 | iota(0) 0.83, iota(a) 0.96, W_mag 80 GJ |
| HSR5/22 (BEI Table I) | 5 | 50 | 12.2 (22/1.8) | 22 | 1.8 | 5.0 | iota(0) 0.84, iota(a) 1.00, W_mag 100 GJ |
| L22 Table 1 (L22:320): HELIAS-3 / -4 / -5 / QA | | | 6.4 / 8.8 / 12.3 / 6.3 | 13.9 / 17.6 / 22.2 / 9.3 | 2.2 / 2.0 / 1.8 / 1.5 | | first wall 30 cm from LCFS in all cases |

What the corpus says changes between them:

- Coil-plasma distance: Helias 4 1.7 m vs Helias 5 1.9 m at reference size (L21:760). That is why Helias 4 ends with the largest plasma volume (1560 m3) despite the same power target.
- Masses: "Despite of the different aspect ratio and the different coil numbers, the total masses found by Process are comparable for all three devices and only increase slightly for the machine with higher aspect ratio." (L21:757-758.)
- Iota: HSR4/18 0.83 to 0.96, HSR5/22 0.84 to 1.00 (BEI:28-31). The thesis (L23:1964) characterises the whole line: "It is characterized by relatively high aspect ratios, of 6-12 [261], by the minimization of the bootstrap current and parallel MHD currents, by minimization of the Shafranov shift, by low magnetic shear and by an island divertor concept".
- Ripple / fast particles / confinement: Beidler says the reduction from 5 to 4 periods keeps "Stability limit and energy confinement times ... nearly the same" (BEI:13), that HSR4/18 has "effective helical ripple below 1%" (BEI:13, 84), and that fewer coils per period "would raise the modular ripple and the losses of highly energetic alpha particles" (BEI:39). Neither Lion paper gives A-resolved ripple or f_ren values for the three Helias configurations.
- Cost: "The configuration HSR4/18 is more compact than the 5-period HSR5/22, which also may lead to a 20% cost reduction of the reactor core." (BEI:170.) The thesis conclusion (L23:2457): "stellarators usually have a comparably large aspect ratio, which lead to, approximately linear, increased costs, compared to a design with lower aspect ratio, at the same minor radius. However, in this scenario, the large aspect ratio machine would also produce higher fusion power, which likely lead to similar levelized cost of electricity in machines with different aspect ratio."

What the corpus does NOT say. No run treats a as a free optimisation variable at fixed R. There is no "f_asp" symbol; the aspect-ratio machinery is the fixed input A plus the f_geo term of eq. 58. No source gives a rule for how iota, ripple or f_ren would change if a were scaled inside one configuration.

## Q2. What bounds the plasma-coil distance, and hence a at fixed R?

Plain answer. In stellarator-PROCESS the coil-plasma distance is a property of the coil set, scaled linearly with R and reduced when a grows at fixed coil size. It must exceed the sum of half the coil thickness, vessel, shield, blanket, first wall, SOL and a gap. Written that way it is an upper bound on a at fixed R (equivalently a lower bound on R at fixed A). A second constraint, the coil-coil toroidal gap, also scales with R alone. Both papers report that this radial-build constraint, not confinement, set the machine size in every case studied.

Constraint equations (verified on the equation images):

- Coil-coil gap, eq. 57 (images/lion_2021_nf_stellarator_process.pdf-0013-03.png): d_min(C) * R/R_hat > w_WP + w_case. Text (L21:621): "an effective parameter of the minimal distance between two central coil filaments d_min(C) ... This distance scales linearly with the major radius".
- Plasma-coil distance scaling, eq. 58 (images/lion_2021_nf_stellarator_process.pdf-0013-06.png; thesis eq. 2.91, images/lion_2023_phd_thesis_stellarator_systems_code_models.pdf-0078-03.png): d_pc = (R/R_hat) * ( f_geo(C) * a_hat * (A_hat/A - 1) + d_pc(C) ). Text (L21:634): "f_geo = d(d_pc)/da accounts for how much the plasma wall distance changes when decreasing the minor radius in the same configuration. A is the (scaled) aspect ratio and A_hat the aspect ratio at the reference point." Read plainly: at fixed R, raising a lowers A below A_hat, the bracket term goes negative, and d_pc shrinks by f_geo times the change in a.
- Radial build, eq. 59 (images/lion_2021_nf_stellarator_process.pdf-0013-09.png; thesis eq. 2.92): d_pc > d_coil/2 + d_VV + d_shield + d_blanket + d_fw + d_SOL + g_ap. Definitions (L21:637-640): d_coil is "the radial thickness of the coil (winding pack plus coil jacket and insulation)", d_shield "the thermal shield", g_ap "the left available space". Caveat in the same paragraph: "PROCESS only ensures radial build consistency along one radial line in the stellarator geometry".
- Numbers used (L21:709): "for the radial build constraint, a fixed radial component thickness of 1.15 m is assumed, including vacuum vessel, breeding zone, blanket structure mass and neutron shielding, consistent with neutronics calculations conducted in [46]. The SOL width is taken as 15 cm." Thesis Table 4.1 (render thesis_pdfp106_full.png): "Blanket & Shield Size" 1.2 m conservative, 60 cm advanced; text (L23:1998) "only 40cm blanket + 20cm shield space are assumed" for the advanced case. Thesis Table 4.7 (L23:2340): "Fix a blanket and shield size of 90cm total". Coil half-thickness comes from Table 2 (WP radial thickness 0.74-0.76 m) and Table 4.3 (0.434 / 0.649 m).
- Reference distances: Helias 4 1.7 m, Helias 5 1.9 m at reference size (L21:760). Stellaris: minimum coil-plasma distance 1.37 m to the centre filament (STX Table 3, see Q3).

Which way the bound points. Eq. 59 is a minimum on d_pc; through eq. 58, d_pc rises linearly with R and falls with a. The papers describe it as a lower bound on R at fixed A: "The major radius of all three designs are limited by the plasma-coil distance, which needs to include space for blanket and shielding and the radial extension of the coils. This we found by relaxing the radial build constraint, which resulted in significantly smaller major radii for all three machines" (L21:760). And in the summary (L21:809): "the major radius of the used devices, and thus the major cost driver of a stellarator reactor device, was consistently found to be constrained from below by the plasma-coil distance, not by lack of confinement quality." For a model that holds R and frees a, the same inequality is an upper bound on a.

Thesis confirmations. "Both designs are at the same time also limited by the coil-plasma distance, which was also found to be the case for 3 and 4 field period HELIAS-devices with lower aspect ratios" (L23:2068). Coil-set study: "the major radii of the design points strongly correlate with the free distance between coils and plasma at the reference size. The overall size of the devices is found between 18 and 26 Meters." (L23:2352.) Uncertainty study (L23:2421): "a design with coils situated 20% farther away from the plasma, together with respective improvement in confinement would result in machines at 14 Meters major radius, while designs, where the coils are situated 20% closer to the plasma ... would result into machines with 20 Meters major plasma radius." Table 4.6 (render thesis_pdfp126_full.png) samples "coil-plasma distance constraint violation (d_c-p)" over -20 % to +20 %.

Other bounds in the coil model that touch a_coil rather than a: the curvature scaling eq. 46 (images/lion_2021_nf_stellarator_process.pdf-0010-24.png), kappa_max ~ (R/R_hat) * kappa_max(C) / (1 - d_WP/(2 a_Coil)), and the coil-set inductance scaling (thesis eq. 2.82, images/lion_2023_phd_thesis_stellarator_systems_code_models.pdf-0074-12.png), L = L(C) (a_coil^2/a_coil_hat^2)(R_hat/R), "based on an ideal toroid, where a_coil is the minor average coil radius" (L23:1486). These see the coil minor radius, which is fixed once R is fixed; they do not see the plasma a.

Helios (HEL:153, 269, 341): "Helios is designed with a minimum of 1.2 m between the plasma and any part of a coil. This permits a uniform radial build." and "A minimum distance of 1.2 m between the plasma and coils is enforced. This leaves space for adequate breeding blanket and neutron shielding". Table 1 (HEL:96-140): R 8 m, A 4.5, a 1.8 m, "Minimum plasma-coil distance 1.2 m"; first wall 2 cm (HEL:323); blanket "a uniform 50-cm-thick layer" (HEL:331); shield layers WC, B4C, 316L vessel, borated water, borated HDPE (HEL:341) without per-layer thicknesses.

HELIAS-5B neutronics radial build (NEU:57-68, Tab. 1): tungsten armour 0.2 cm, first wall 2.5 cm, breeding zone 50 cm, back support structure about 10-40 cm, inner vacuum vessel 6 cm, vessel shield 20 cm, outer vessel 6 cm; "The minimum distance between the last closed flux surface of the plasma and the tungsten armor is set at 10 cm."

What the corpus does NOT say. No source prints a value for f_geo, nor a coil-bore or winding-surface radius, nor a coil-spacing rule as a function of a. The radial build is one-dimensional in the code by its own admission. Nothing states a minimum SOL width as a function of a or A.

## Q3. Stellaris: aspect ratio, radial build, coil dimensions, and whether a lower aspect ratio is available

Plain answer. Stellaris is A 9.8 (R 12.7 m, a 1.3 m). The averaged radial build from plasma edge to coil centre is about 1.50 m and the minimum coil-plasma distance to the centre filament is 1.37 m, so the build already varies around the shaping and there is no slack for a larger a at this R. The paper says smaller aspect ratio is reachable, but by finding a different configuration at the same a, which shrinks R, not by growing a inside this one.

Verified numbers (all from page renders; file names in the Files section).

- Table 2, PDF p.3 (stellaris_p03_table2.png): Minor plasma radius 1.3 m; Major plasma radius 12.7 m; Plasma aspect ratio 9.8; Plasma volume 428 m3; Plasma surface area 940 m2; Axis av. field 9.0 T; Peak conductor field 24.9 T; Peak coil current 15.4 MA; 48 coils; Stored magnetic energy 111 GJ; Peak fusion power about 2700 MW; Peak neutron wall load 4.05 MW/m2.
- Table 3, PDF p.4 (stellaris_p04_table3.png), "Main configuration parameters of Stellaris scaled to a minor radius of a = 1.3 m. Coil information provided in this table refers to the center filament.": Aspect ratio 9.8; Optimized vol. av. beta 0.03; Axis rotational transform 0.86; Edge rotational transform 0.98; Edge mirror ratio 26.66 %; Minimum coil-plasma distance 1.37 m; Minimum coil-coil separation 0.67 m; Minimum radius of curvature 0.64 m.
- Table 5, PDF p.10 (stellaris_p10_table5.png), points A and B: Minor plasma radius 1.3 m; Major plasma radius 12.74 m; Axis averaged B0 9.0 T; Aspect ratio 9.8; Plasma volume 425 m3; f_ren 1.0; Ratio tau*/tau_E 8.00; Total plasma energy 504.65 / 533.14 MJ; Confinement time 1.46 / 1.99 s.
- Fig. 34, PDF p.18 (stellaris_p18_fig34.png), "Averaged component thicknesses and gaps of the radial build. Values are only approximate, as large variations in both toroidal and poloidal directions exist.": SOL 16.6 cm, First wall 3 cm, Breeder blanket 43.1 cm, In-Vessel Shield 22 cm, Vacuum vessel 30 cm, Gap 10 cm, Magnet 25 cm to coil centre. Sum 149.7 cm.
- p.18 prose (pymupdf text, checked on stellaris_p18_full.png): "Given the varying plasma-to-coil distance across different poloidal and toroidal positions, we implement variable thicknesses for both the blanket and the shield. ... the INS thickness at various toroidal angles is shown in Fig. 32, with a minimum thickness of 100 mm and a maximum thickness of 225 mm."
- Table 8, PDF p.23 (stellaris_p23_table8.png), coils 0-5: Cross section side length 360 / 360 / 340 / 340 / 320 / 300 mm; Min. casing-to-LCFS dist. 1.06 / 1.04 / 1.05 / 1.08 / 1.11 / 1.07 m; Min. casing-to-casing dist. 11.4 / 114 / 91.4 / 135 / 326 / 475 mm; Coil mass, no casing 24.2 / 25.4 / 21.6 / 21.5 / 19.0 / 17.0 t; Peak field 24.6 / 23.1 / 22.0 / 21.0 / 21.4 / 19.5 T; Tape length no grading 807 / 847 / 721 / 717 / 636 / 567 km; Self-inductance 1.30 / 1.44 / 1.10 / 1.10 / 0.90 / 0.62 H; Total energy 110.58 GJ (2.76 GJ per coil).
- p.22 prose (pymupdf text): "For each coil, we select a square winding pack with a variable number of turns, ranging from 225 to 324 turns per coil." "Each turn is sized at 20 mm x 20 mm, with a 6 mm x 6 mm soldered tape stack embedded in a 15 mm diameter round copper former." "The winding pack orientation is chosen so that a flat face is tangential to the plasma at each point, allowing for a vacuum vessel surface that is as flat as possible and maximizing available space for the radial build while minimizing peak fields within the winding pack."

Consistency check I made, not a paper statement: the casing-to-LCFS minimum of about 1.04-1.11 m plus half a 300-360 mm winding pack is 1.2-1.3 m, and the 1.37 m centre-filament minimum sits between that and the 1.50 m average. So at the tightest poloidal location the build is already thinner than the Fig. 34 average by about 13 cm; the paper handles this by thinning the in-vessel shield locally (100 mm minimum against 225 mm maximum).

Statements on aspect ratio and on lower A.

- Intro, PDF p.2 (text): "one cannot merely scale W7-X to an economically attractive reactor size, due to a number of known limitations including high fusion-born fast particle losses [63], insufficient plasma-coil distance to fit a neutron shield and blanket at moderate machine sizes [12,64], and high turbulent transport levels".
- p.3 (text): "The underlying plasma configuration of Stellaris belongs to the class of recently proposed SQuID-configurations [71], adapted to meet the requirements of a power plant by dedicated optimization for larger coil-plasma distances."
- p.17 (text): "the limited distance between the plasma and the coils has been identified as the primary constraint on overall machine size, directly influencing the feasibility of achieving a viable reactor configuration [12]. The Stellaris concept strategically addresses this challenge. By ensuring that the coils are positioned farther away from the plasma in relative terms, this design provides greater space for tritium breeding and neutron shielding, allowing the overall reactor size to be reduced."
- p.31 (text): "use of a lower aspect ratio stellarator configuration to optimize economic viability" is listed as future work, and "stellarators with lower aspect ratios would potentially require smaller capital costs, though at the expense of overall fusion power. Appendix C shows an example".
- Appendix C, PDF p.33 (stellaris_p33_full.png): "This paper has described a QI configuration with an aspect ratio A ~ 10, corresponding to a major radius of R0 ~ 12.5 m. The major radius could be further reduced if an equivalently- or better-performing configuration at lower aspect ratio could be found. For example, a configuration with aspect ratio 6 and the same minor radius (upon which plasma confinement most directly depends) would result in a major plasma radius of R0 ~ 7.8 m. On the other hand, such a device would only 3/5 of the fusion power as the Stellaris concept demonstrated here."
- PDF p.34 (stellaris_p34_full.png): "in Fig. C.55 we compare the SQuID-configuration used in this paper with alternative plasma configurations at aspect ratios of approximately 9 and 8. ... Additionally, they are ideal-MHD stable, and allow for sufficiently distant coils. ... Neoclassical transport is found to be slightly higher in the low aspect ratio configurations, though still much lower than in W7-X". The figure legend labels them "A~9" and "A~8.5".
- p.11 (text): "inboard access ports are particularly enabled by the high aspect ratio of Stellaris, and likely cannot be replicated in a comparable tokamak at lower aspect ratio."

Extraction warning. The iter-01 markdown (knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md:290-291) prints "Maximum coil-plasma distance 1.37" and "Minimum coil-plasma distance 0.95", and its Appendix C (line 3077) reads "R = A * a = 1 m". Both are phantoms; the PDF Table 3 has a single "Minimum coil-plasma distance 1.37 m" row and Appendix C says R0 ~ 12.5 m.

What the corpus does NOT say. Stellaris never states an a-sweep, a maximum a, or an f_geo-type sensitivity. The lower-A alternatives are different SQuID configurations with their own coil sets, held at the same a; the paper does not say the existing Stellaris coil set tolerates a larger plasma.

## Q4. Aspect-ratio dependence of the transport facts

Plain answer. Only the ISS04 law carries an explicit R and a dependence, and through it an A dependence once the law is rewritten in a and A. The three Stellaris point-A facts carried into the sweep, tau*/tau_E = 8, f_suppr = 0.5 and iota = 0.92, have no A-dependence anywhere in the corpus. tau*/tau_E and f_suppr are declared assumptions; iota is a property of the configuration and is quoted only per configuration; f_ren is a fitted or assumed multiplier with no A-model.

(i) Ash particle-to-energy confinement ratio.

- Stellaris Table 4, PDF p.9 (stellaris_p09_table4.png): "tau*/tau_E 8.0"; caption "tau*/tau_i is the ratio between particle and energy confinement time (for all species)". Table 5 caption (p.10 render): "Ratios taken for tau*/tau_E are assumptions." Appendix A, PDF p.32 (text): "tau*_alpha = rho* tau_E, where we use rho* ~ 8 ... Determining reasonable values for rho*, and validity of that model in general, is a subject of active research [161,347]."
- Thesis Table 4.1 (thesis_pdfp106_full.png): tau*_He/tau_E 8 conservative, 4 advanced, for the same Helias 5 configuration; "the optimistic case refers to a scenario where improved parameters can be achieved without changing the configuration". Text (L23:1980): W7-X data "can be used to constrain the ratio tau*_He/tau_E in very weak bounds between 2 and 80 ... No direct measurement of the ratio tau*_He/tau_E is available yet in W7-X". Uncertainty studies: 6 +/- 1 (L23:2110, 2136) and a uniform 3-9 range (Table 4.6, thesis_pdfp126_full.png). L23:2044: "The ratio tau*_He/tau_E can be designed for if and only if the particle transport can be manipulated independently of the energy transport."
- Model definition (L23:860): "usually obtained by assuming a fixed ratio between helium particle confinement and plasma energy confinement time, tau*_He/tau_E."
- No A-dependence in any source. Beidler and Helios do not quote the ratio at all (Helios only: "Impurity and ash dilution is included based on an assumed fraction", HEL:175).

(ii) Helium suppression f_suppr.

- Stellaris Appendix A, PDF p.32 (text): "we introduce a new heuristic value f_suppr which is used to suppress the resulting helium density by a constant factor, n'_He = f_suppr n_He (A.6). This assumption is informed by two considerations: first, by suppression of helium ash due to a positive ambipolar radial electric field, and second, by the effect that fast particles do not slow down directly in the core, but are radially displaced due to their finite drift orbit. This effect was quantified in [110] by employing Monte-Carlo slowing down simulations in various stellarators. We capture it here heuristically by choosing a value of f_suppr = 1/2."
- The [110] mechanism in the thesis (L23:1844): "The fact that thermal helium may not deposit where it is born, would have a noticeable effect also on fusion reactor design points." The drift-orbit displacement is a fixed physical length, so it scales relative to a; the thesis says this in general for fast particles (L23:796): "f_alpha is not only dependent on the configuration C, but also on the absolute minor radius of the machine (the fast particle energy is fixed at 3.5 MeV and thus introduces a scale)". No source turns this into an a- or A-formula for f_suppr. Nothing outside Stellaris uses f_suppr.

(iii) Rotational transform.

- Stellaris Table 3 (render): axis 0.86, edge 0.98. The ISS04 law uses iota_2/3; Stellaris does not print iota_2/3 in a table I rendered (the sweep's 0.92 lies between axis and edge values but I found no printed 0.92).
- Beidler Table I: HSR4/18 0.83 to 0.96; HSR5/22 0.84 to 1.00 (BEI:28-31). Different A, nearly the same iota; consistent with iota being an optimisation target of the W7-X line, not a function of A.
- Helios Table 1 (HEL:111): iota_2/3 0.46 at A 4.5 (a QA configuration, not comparable).
- L21:187 and L23:744: iota_2/3 = iota_2/3(C), a configuration input. The island-divertor model needs the edge iota to sit at N_p k/n, so it is pinned by design, not by A.
- No source gives iota as a function of A.

(iv) ISS04 and f_ren.

- The law (eq. 9, images/lion_2021_nf_stellarator_process.pdf-0005-12.png): tau_E = 0.134 f_ren a^2.28 R0^0.64 n_e^0.54 B_t^0.84 iota_2/3^0.41 P^-0.61. Same in Stellaris eq. A.7 (PDF p.32 text). f_ren (L21:187): "a proportionality factor that measures the magnetic configuration dependent deviation from the ISS04 scaling law. In principle, f_ren is determined by C directly, although a reliable a priori method of calculating this factor is not available up to date."
- Rewritten in a and A (thesis eq. 1.27, images/lion_2023_phd_thesis_stellarator_systems_code_models.pdf-0025-02.png): tau_E^ISS04 = 0.152 a^2.79 A^0.08 n^-0.18 B^2.15 T^-1.56 iota^1.05. Text (L23:424): "by R = Aa in Equation 1.26, where A is the aspect ratio". So at fixed a, B, T and n, the explicit A exponent is 0.08, essentially nil; the whole size effect sits on a^2.79. Stellaris eq. A.8 (PDF p.32 text) is the same rewrite kept in R: a^2.72 R^0.08.
- Thesis eq. 1.24 (images/...-0023-06.png): tau ~ tau_GB f(A, iota), with the text (L23:395) "which is already hinting at aspect ratio A and rotational transform iota dependencies of the transport". Stellaris PDF p.33 (stellaris_p33_full.png): "A more careful consideration might retrieve other factors such as sensitivity in aspect ratio and iota [350], tau ~ tau_GB f(A, iota), but this was not yet retrieved from simulations or data."
- f_ren values in use: Stellaris 1.0 (Table 4, Table 5). Thesis Table 4.1: 1.4 conservative ("obtained from W7-X high performance pellet discharges", L23:1976), 1.8 advanced; Table 4.3 outcome 1.77 / 1.38; range 1.0-1.8 in Table 4.6 with "In W7-X, highest values for f_ren are obtained transiently in pellet discharges with f_ren ~1.4" (L23:2224). Helios H_ISS04 1.4 (HEL:113), 1.33 in an alternative scenario (HEL:249). Beidler: HSR5/22 tau_E required 1.62 s vs ISS95 0.96 s and LGS 1.65 s (Table II, BEI:153-166), with "Empirical scaling laws predict nearly the same confinement times for both reactor concepts" (BEI:153).
- No source models f_ren as a function of A. The nearest thing is the remark that the three Helias designs have "comparable" masses at different A (L21:757) and the QA-versus-QI contrast in the thesis uncertainty study, which is per configuration, not per A.

Related, not asked but relevant to the sweep: neoclassical 1/nu transport uses eps_eff(C), a configuration input (L21:246; thesis Table 4.1 0.01 vs 0.001), and the thesis states (L23:2050, confirmed on thesis_pdfp113_full.png) "the forces scale with peak magnetic fields, which again scale with the aspect ratio of the machine. This scaling can be understood in first order from the peak magnetic field in an ideal toroid, which scales with ~ 1/A at fixed minor radius, where A is the aspect ratio." and (L23:2429) "the ratio B_max/B_axis decreases with increasing aspect ratio".

What the corpus does NOT say. There is no A- or a-dependence for tau*/tau_E, f_suppr or iota anywhere. There is no measured or modelled f_ren(A). The A^0.08 exponent is the only quantitative aspect-ratio dependence, and it is negligible.

## Q5. Anything that prices coil bore or coil size against minor radius

Plain answer. The codes price the coils through R, B, the winding pack and the stored magnetic energy; the plasma minor radius enters only indirectly, through the radial-build inequality that forces R up. The coil minor radius a_coil does appear in three scalings (B_max, inductance, curvature) and Lion 2021's coil-set study shows the cost of a bigger coil bore directly. Beidler and Stellaris give per-coil masses and conductor lengths at a single size only.

Equations and numbers.

- Peak field on the coil, eq. 39 (images/lion_2021_nf_stellarator_process.pdf-0009-19.png): B_max(A_wp) = mu0 I N / (R - a_coil) * ( a0(C) + (R/sqrt(A_wp)) a1(C) ). Text (L21:455): "a_coil is the average minor coil radius, N the number of coils, and A_wp the cross-sectional area of the winding pack."
- Coil current scaling (L21 section 3.7, eq. 36 text at L21:437): "the scaling of the coil current with respect to B_t and R is of course linear".
- Inductance, thesis eq. 2.82: L = L(C) (a_coil^2/a_coil_hat^2)(R_hat/R).
- Curvature, eq. 46: kappa_max ~ (R/R_hat) kappa_max(C) / (1 - d_WP/(2 a_Coil)).
- Force density, eq. 42 (L21:520): scaled with j, I and coil length l from the reference values f_max(C), fbar_max(C), F_max(C).
- Structure mass, eq. 56 (images/lion_2021_nf_stellarator_process.pdf-0012-18.png): M_struct = 1.348 W_mag^0.78, "an empirical scaling law from existing machines, as described in [56]" (L21:607). W_mag = 1/2 L I^2, so through eq. 2.82 the structure mass grows with a_coil^1.56 at fixed I and R.
- Coil-set study, L21 Table 3 (L21:770-795) at fixed R 22 m, a 1.96 m: 30 / 50 / 60 coils give total coil mass 8.58e6 / 4.65e6 / 4.75e6 kg, stored energy 146 / 104 / 98.8 GJ, B_max 11.5 / 13.7 / 13.0 T. Text (L21:764): "The stored magnetic energy scales with the coil minor radius which is, approximately 20% larger in the 30 coils device." That is the one place in the corpus where a larger coil bore is priced: about 20 % more a_coil gave about 40-50 % more stored energy and roughly 80 % more coil mass, though the coil count changed at the same time.
- Helias 3/4/5 masses (L21 Table 2): total coil mass 5.91e6 / 6.84e6 / 7.61e6 kg, structure mass 1.15e7 / 1.29e7 / 1.51e7 kg, W_mag 106 / 122 / 150 GJ, with a of 2.16 / 2.08 / 1.68 m and R 13.7 / 18.3 / 20.7 m. Masses track R, not a.
- Thesis Table 4.3 (thesis_pdfp110_full.png): total coil mass 1.70e6 kg (R 12.5, a 1.02) vs 4.28e6 kg (R 17.1, a 1.39); coil support structure 1.60e6 vs 2.94e6 kg; W_mag 22.6 vs 57.0 GJ.
- Beidler (BEI:46, 184): "Weight of coil 94 t, length of SC cable 10 km per coil" for HSR4/18; "The total length of superconducting NbTi cable is 400 km and the weight about 700 t. The total weight of the super-conducting coils including the casing is 4100 t." Single size, no scaling.
- Stellaris Table 8 (stellaris_p23_table8.png): coil mass without casing 17.0-25.4 t, tape length without grading 567-847 km, per coil, at a = 1.3 m only. p.22 text: peak field "is also heavily dependent on the size of the winding pack".
- Helios (HEL:267): "quantities such as maximum field on-coil and total HTS tape length may be optimized directly". No a-scaling given.

What the corpus does NOT say. No source writes coil mass, conductor length or structure mass as an explicit function of the plasma minor radius or of the coil-plasma distance. The only a-linked cost route in the codes is eq. 58-59 forcing R, and R then drives everything through the linear current scaling and W_mag.

## Gaps

- No admissible source treats plasma a as a free variable at fixed R and fixed coil set. Every published optimum holds A and moves R.
- f_geo, the one coefficient that would tell how fast the coil-plasma distance closes as a grows, is defined (d(d_pc)/da) but never given a value for any configuration, Stellaris included.
- No source gives tau*/tau_E, f_suppr or iota as functions of A or a. tau*/tau_E and f_suppr are declared assumptions in Stellaris; the thesis calls the tau*_He/tau_E bounds from W7-X "very weak" (2 to 80).
- The only quantitative A-dependence of confinement is the A^0.08 exponent of the rewritten ISS04 law; the corpus explicitly says a tau_GB f(A, iota) correction "was not yet retrieved from simulations or data".
- Stellaris prints no iota_2/3; the 0.92 carried by the sweep was not found on any rendered table.
- The Stellaris radial build is stated as toroidally and poloidally variable ("Values are only approximate"); a one-line 1.9 m fixed stack does not reproduce the 1.37 m centre-filament minimum against the 1.50 m average.
- The thesis Tables 4.1, 4.3, 4.6 and the B_max ~ 1/A sentence are missing from the registered markdown extraction (dropped tables); I verified them on the raw thesis PDF found in an earlier session's scratchpad. If that scratchpad is cleaned, the registered source directory has no raw.pdf and those numbers become unverifiable locally.
- Beidler's Fig. 2 shows blanket and first wall in the HSR4/18 cross-section but the extraction carries no radial-build numbers for it.

## Files

All under /tmp/claude-1000/-home-reid-1cfe-fusion-tea/a12fbcb4-631e-48fb-bfe1-449a02423014/scratchpad/sources_a/ (my subdirectory only; nothing written elsewhere).

Renders from the Stellaris raw PDF:

- stellaris_p03_full.png, stellaris_p04_full.png, stellaris_p09_full.png, stellaris_p17_full.png, stellaris_p18_full.png, stellaris_p22_full.png, stellaris_p33_full.png, stellaris_p34_full.png (full pages, 110 dpi)
- stellaris_p03_table2.png (Table 2, 170 dpi)
- stellaris_p04_table3.png (Table 3, 170 dpi)
- stellaris_p09_table4.png (Table 4, 170 dpi)
- stellaris_p10_table5.png (Table 5, 170 dpi)
- stellaris_p18_fig34.png (Fig. 34 radial build, 200 dpi)
- stellaris_p23_table8.png (Table 8 coil parameters, 170 dpi)

Renders from the Lion 2021 and 2023 raw PDFs (read from /tmp/claude-1000/-home-reid-1cfe-fusion-tea/cf4cbd0c-47f2-43ea-be9f-34ba243b7af5/scratchpad/):

- lion2021_p16_full.png (journal p.15, Table 2 Helias 3/4/5)
- thesis_pdfp091_full.png (Table 3.1), thesis_pdfp106_full.png (Table 4.1), thesis_pdfp110_full.png (Table 4.3), thesis_pdfp113_full.png (B_max ~ 1/A sentence), thesis_pdfp126_full.png (Table 4.6)

Working text files:

- thesis_grep.txt (grep hits over the thesis extraction)
- stellaris_pagetext.txt (pymupdf text of selected Stellaris pages, used to locate prose only)

Equation images viewed in place (not copied): knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/images/lion_2021_nf_stellarator_process.pdf-{0005-03,0005-12,0009-19,0010-24,0012-03,0012-06,0012-18,0013-03,0013-06,0013-09,0013-10}.png and knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/images/lion_2023_phd_thesis_stellarator_systems_code_models.pdf-{0023-06,0025-02,0074-12,0078-03,0078-06}.png.
