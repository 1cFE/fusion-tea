# Burn control and the ignited operating point in the registered stellarator systems-code sources

Read-only research report. Local corpus only; no web access. Clean-room rule honoured: nothing under `knowledge/holdout/`, no Helios or ARIES material, and nothing under `exploration/concept_analysis/analyses/09-qi-stellarator-hts/` was opened.

Source keys used below:

- **Lion 2021** = `knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/output.md` (PROCESS stellarator version, Nucl. Fusion 2021). Equations are images under `images/`; I viewed the ones I cite.
- **Lion 2023** = `knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/output.md` (PhD thesis).
- **Beidler** = `knowledge/sources/the_helias_reactor_beidler_et_al_iaea_cn_77_ftp1_16/output.md`.
- **Stellaris-md** = `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md` (prose extraction; tables corrupted).
- **Stellaris-pdf** = `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf`, page numbers are printed page numbers. I extracted text with pymupdf and rendered pages 9 and 10 (and 200 dpi clips of Table 5, the POPCON paragraph, and the Fig. 15 caption) to PNG in this directory and read them.

Where a quote comes from the PDF, I checked it against the rendered page. Where the markdown differs from the PDF, I say so.

---

## Q1. How the systems-code papers treat the power balance at the operating point, auxiliary heating, and installed heating power

**Answer.** PROCESS (both Lion papers) enforces the 0D power balance as an *equality* constraint that the optimiser must satisfy, with `P_aux` as one term on the heating side. For reactor design points the papers add a separate *ignition* requirement, written as a constraint "Q ~ infinity", so `P_aux` at the operating point is zero by construction and the optimiser moves density, temperature, size, field and the confinement factor `f_ren` to make alpha heating exactly balance losses. Neither paper sizes installed heating power from the operating-point balance. In the one study that has an installed power at all (Lion 2023 § 4.2, a pilot plant that is *not* required to ignite), the installed auxiliary power is a fixed input that is scanned (35 MW, 45 MW), and the operating point is what the plasma reaches with that power; the "ECRH heatability" constraint (O1 cut-off) is the only heating-related constraint in the ignited runs, and it constrains density, not power.

Supporting quotes:

- Lion 2021 L164: "The 0D-transport model in Process imposes a power balance as an equality constraint,"
- Lion 2021 Eq. (6), image `images/lion_2021_nf_stellarator_process.pdf-0005-06.png`: `P_Loss =! P_heat` (the `!` over the equals sign marks a required equality).
- Lion 2021 Eq. (7), image `images/lion_2021_nf_stellarator_process.pdf-0005-08.png`: `P_Loss^conf + P_br + P_line + P_sync =! f_α P_α + f_¬α P_¬α + P_aux`.
- Lion 2021 L170: "The right-hand side includes heating from fusion alphas _Pα_ , a term of charged non-alpha particle heating _P¬α_ (e.g. in D–D fusion) and a term for auxiliary heating _P_ aux."
- Lion 2021 L211: "Equation (7) serves as equality constraint in Process."
- Lion 2021 L187 (what the solver moves to close the balance): "Instead, Process can iterate _f_ ren within user set boundaries and return a _needed_ configuration factor for the optimized power plant design point."
- Lion 2021 L118: "For the plasma design, the implemented scaling parameters are the plasma density, temperature, and the ISS04 'renormalization' factor ... The stellarator-Process version is capable of optimizing for devices by scaling these parameters as a part of the optimization vector now."
- Lion 2021 L709 (the reactor runs impose ignition, and the ECRH constraint is about *reachability*, not power): "We further impose an ECRH heated ignition point, using the prescription in subsection 3.4, and assume maximal available gyrotron frequencies of 200 GHz. ... Requiring ECRH inhabitability constrains both, the density and the magnetic field from above."
- Lion 2021 L711: "The ISS04 transport model as in section 3.2 is assumed and the 0D power balance equation including Bremsstrahlung and line-radiation terms is enforced as a constraint equation."
- Lion 2021 Table 2 (L713-L748): the output table for the three Helias design points has no auxiliary-heating or installed-heating row at all. Fusion power carries footnote c, "Parameter at a directly imposed limit/target"; density and temperature carry footnote a, "Iteration parameter".
- Lion 2023 L535: "technological limits ... typically can be written in inequality and equality constraints"; L547: "ensuring fulfilled constraints if 𝑔𝑖( **x**[∗] ) ≤0 and ℎ𝑗( **x**[∗] ) = 0 respectively".
- Lion 2023 L708: "The 0D-transport model in Process imposes a power balance as an equality constraint," and L716: "...and a term for auxiliary heating 𝑝𝑎𝑢𝑥."
- Lion 2023 L124 (what "ignition" means in this code family): "bring the fuel into a state of ignition, where the heating power by fusion reactions matches any thermal losses of the fuel. This way, the fuel 'burns' by itself without any requirement of auxiliary power input."
- Lion 2023 Table 4.2 (L2000-L2014), constraints list: "Require ignited design points, 𝑄∼∞" and "O1 ECRH ignitability".
- Lion 2023 L2018: "Still, both design points are modelled to run ignited, 𝑄∼∞."
- Lion 2023 Table 4.5 (L2194-L2222): "Ignition, 𝑄∼∞" and "Require O1-Mode ignition (at arbitrary gyrotron frequency)". Same two lines again in Table 4.7 (L2340, L2346).
- Lion 2023 L2052: "Even though a stellarator has no current drive and the design points were assumed to be ignited, they both still feature a significant recirculating power fraction of 36% and 26% respectively."
- Lion 2023 L519 (the role auxiliary heating plays in the thesis's framing): "External heating such as neutral beam injection, electron- and ion-cyclotron heating is required to ignite a stellarator plasma or to use it as a plasma state control mechanism."
- Lion 2023 L2140 (installed power is an input in the non-ignited pilot-plant study): "Figure 4.7 shows the probability distribution function of 𝑄 for a machine size, a fixed installed power and for a fixed magnetic field strength. For every set of machine parameters 𝐵, 𝑅 and 𝑃aux, the probability distribution function is obtained from 10[3] Process runs"
- Lion 2023 L2411: "Both these values correspond to an auxiliary power during operation of 45 MW. However, for all design points analysed, a higher installed heating power increased also the fusion gain, while still staying below the imposed heat flux limits. For example the 0.72 Meter minor radius and 9 Teslas magnetic field machine would barely match the 𝑄= 10 with 95% confidence at 35 MW installed power, but would do so with 45 MW."

Note on what could not be checked: Lion 2023 Table 4.3 (design-point outputs, L2022) did not extract (image only), so I cannot say whether it lists an installed heating power for the ignited Helias 5 points. Lion 2021 Table 2 did extract and has no such row.

---

## Q2. Burn control, thermal stability of the ignited burn, runaway or attractor behaviour

**Answer.** None of the three systems-code sources models burn control or thermal stability. PROCESS has no mechanism for what an over-ignited plasma does; ignition is a constraint, not a dynamic state. The closest content is (a) Lion 2023's "Cordey pass" discussion, which describes the ignition threshold as a hill in the (n, T) plane that installed heating must get the plasma over, and notes that beyond it the plasma "would ignite ... if not for" wall-load and beta limits, and (b) a one-sentence acknowledgement that ignited devices would need "respective control mechanisms". The Stellaris paper is the only source that names burn-control mechanisms, and it does so qualitatively: density control (established), confinement degradation via coil currents, tritium fraction, or ECCD (proposed), with no numbers. It also states that the temperature is expected to be limited by turbulence, i.e. by physics the 0.5D model does not contain.

Supporting quotes:

- Lion 2023 L2142: "the right peak, at higher 𝑄 values, is situated past the 'Cordey-Pass', which refers to the point in density and temperature at which the installed auxiliary heating power is sufficient to reach ignition if it were not for the exhaust and 𝛽 limit preventing this: the second peak not reaching ignition (𝑄∼∞) is due to the imposed < 2 MW/m[2] peak radiation wall load limit. ... In the middle there is the 'Cordey-Pass', which acts like a 'hill' that needs to be overcome on the way to ignition."
- Lion 2023 L2154 (Fig. 4.8 caption): "If not for the wall load limit (and eventually the 𝛽 limit, here indicated in blue), these design points would be ignited, given the imposed models."
- Lion 2023 L2162: "given the high ignition chances of such a device, it likely should be designed to be operate-able in ignition mode, in terms of wall loading and control mechanisms."
- Lion 2023 L2459: "For ignited running devices, the wall materials would need to be designed to cope with respective higher neutron and heat fluxes and respective control mechanisms would need to be developed and installed."
- Lion 2023 L2465 (Fig. 5.1 caption, how the ignition constraint behaves in the optimiser): "For a device without imposed minimal fusion power, but with imposed ignition condition, the optimised 𝑓ren always matches the imposed limit." And L2467: "This conclusion is a consequence of the requirement to limit the temperature and thus the fusion power, which is related to the imposed heat load limits on the components."
- Stellaris-pdf p.10 (left column; Stellaris-md L758 has the same passage with small wording differences): "If the chosen design point is thermally unstable, an additional control scheme or confinement degradation scheme should be employed to achieve burn-control. While density control is widely adopted in current experimental fusion devices, resilient mechanisms for temperature control are not yet well-established, but are conceptually straightforward: plasma confinement degradation can be achieved by tuning coil currents or controlling the tritium fraction in the core. Alternatively, it may be possible to use electron-cyclotron-current-drive (ECCD)-induced confinement degradation [144]. We expect the temperature to be ultimately limited by temperature gradient-driven turbulence or electromagnetic turbulence, such as kinetic ballooning modes. However, no tools or workflows currently exist to predict limits with high confidence."
- Stellaris-pdf p.10 (the GENE+TANGO check deliberately switches thermal runaway off): "To reduce any thermal runaway effects and allow for a more direct comparison of the resulting profiles, we set the power source in TANGO fix to the fusion heating profile expected at the 0.5 D design point. ... Note that by choosing fixed fusion heating profiles, the resulting profiles will change, while the heating sources are not updated."
- Stellaris-pdf p.9 (lower-power points are "easier" to burn-control): "all other operation points with 𝑃aux < 50 MW are likely feasible (e.g. an operation point with lower fusion power and lower fusion gain could be chosen, too, which would result in higher component lifetimes and easier burn-control)." Note: Stellaris-md L712 renders this as "$P_{fus} \leq 50$ MW", which is an extraction error; the PDF reads P_aux < 50 MW.
- Beidler: nothing on burn control or thermal stability (see Q5).

No source gives a number for a burn-control lever (no density excursion, no confinement-degradation factor, no time constant).

---

## Q3. What bounds high density, and how it is applied

**Answer.** Two upper bounds on density, both applied as inequalities that the optimiser may switch on. The Sudo limit `n_c^sudo [1e20 m^-3] = 0.25 P^0.5 B^0.5 a^-1 R^-0.5` (Lion 2021 Eq. 20) is optional ("can enforce this limit or multiples thereof") and both Lion papers distrust it because it ignores impurity fraction. The ECRH O1 cut-off `n_e < n_e,crit^ECRH = (m_e ε0 / e^2) ω_gyro^2, subject to ω_gyro < ω_max` (Lion 2021 Eq. 22) is a hard constraint in every reactor run and is what actually bound the Helias design points. The Stellaris paper reports both as ratios in Table 5 (`n_e0/n_O1 = 0.64`, `<n_e>_V/n_Sudo = 1.00` at point A) rather than enforcing them, and says point B exceeds Sudo. Neither bound has anything to do with burn control in the sources; they bound where a point can sit, not what an ignited point does.

Supporting quotes:

- Lion 2021 L271: "The density in stellarators devices is, at least empirically, bound by the Sudo limit [27], which accounts for excessive impurity radiation at high edge densities."
- Lion 2021 Eq. (20), image `images/lion_2021_nf_stellarator_process.pdf-0006-13.png`: `n_c^sudo [10^20 m^-3] = 0.25 P^0.5 B^0.5 a^-1 R^-0.5`.
- Lion 2021 L275: "Stellarator-Process can enforce this limit or multiples thereof. However, equation (20) was exceeded in W7-X and LHD experiments [28, 29] and is likely dependent on edge impurity concentrations which are not governed by equation (20)."
- Lion 2021 L277-L286: "There is however another density constraint, which is imposed by operational boundaries of an electron cyclotron resonance heating (ECRH) scheme ... The critical density is reached when the plasma frequency matches the electron cyclotron frequency. Thus, the central electron density _n_ e is limited to:" Eq. (22), image `images/lion_2021_nf_stellarator_process.pdf-0006-18.png`: `n_e < n_e,crit^ECRH = (m_e ε0 / e^2) ω_gyro^2, subject to: ω_gyro < ω_max`. L286: "Equation (22) is implemented as a constraint in Process and ensures that the found design point is ECRH heatable in O1 mode."
- Lion 2021 L756: "The found densities in table 2 are in line with the ECRH heating constraint as described in subsection 3.4." L760: "We further observe a relevant design restriction by the imposed ECRH constraint, mainly given by the critical O1-mode density limitation."
- Lion 2021 L752 (the constraint was dropped for the R-B scan because it is technology-sensitive): "Note that for this scan we neglected the ECRH constraint, which is very sensitive on the technological assumptions (gyrotron frequency and heating scheme)."
- Lion 2023 L812-L820: four density-limit mechanisms listed, "Fuelling (particle transport)", "Radiation (Energy transport)", "Operation limits (e.g. by heating schemes)", "MHD effects (via beta limits)".
- Lion 2023 L886: "Interestingly, although the Sudo limit is believed to capture radiational plasma collapse due to excessive line radiation, equation (2.29) is independent of the the impurity fractions." L892: "As Process enforces the energy power balance and has models for the impurity line radiation ..., one would expect that Process inherently should reassemble Sudo (𝑛∝𝑃[0.5] ) like density limit scalings. ... From this check, it is probably safe to say that Process' models already have the density limiting effects of edge and core impurity radiation."
- Lion 2023 L922: "Equation 2.32 was implemented as a constraint in and ensures that the found design point is ECRH heatable in 𝑂1− mode."
- Lion 2023 L2545: "Densities above this limit typically lead to radiation collapses and were indicated like this in the POPCON plot Figure 4.8. ... Thus the limit should not be used carelessly in a reactor-setting."
- Stellaris-pdf p.9 (Fig. 15 caption): "The dark gray line indicates the Sudo density limit [131]." Table 5 (p.10): "𝑛𝑒,0∕𝑛𝑂1 [1] 0.64 / 0.87" and "⟨𝑛𝑒⟩𝑉∕𝑛Sudo [1] 1.00 / 1.55" for points A / B; caption: "Point B would violate the 'Sudo- density limit' [131], but might still be feasible with sufficient plasma purity."

---

## Q4. The Stellaris paper: POPCON, path to the operating point, the 50 MW, ignition, burn control, density control, confinement degradation, Table 5

**Answer.** The paper's 0.5D model is the same equality balance as PROCESS (Eq. A.1 carries the same `!=` mark). The POPCON colours the (T_e0, n_i0) plane by *required* auxiliary power, and explicitly paints the region where required power is beyond the colour bar white, labelling the high-T high-n part of it as "the plasma would ignite". Point A sits on the Q = infinity contour with 0 MW auxiliary power at the operating point; the 50 MW is the minimum installed power along a start-up path that has to cross the Cordey-pass region, and the paper also uses 50 MW as the ECRH system size and says the heating is maximised between 1% and 2% volume-averaged beta on that path. The paper does not model burn control; it names density control as established, confinement degradation as a proposed fallback "if the chosen design point is thermally unstable", and says the temperature will ultimately be limited by turbulence that the model does not contain.

Verified values from the Table 5 render (Stellaris-pdf p.10, clip `table5.png` in this directory): Point A / Point B: minor radius 1.3 / 1.3 m; major radius 12.74 / 12.74 m; axis-averaged B0 9.0 / 9.0 T; aspect ratio 9.8; plasma volume 425 m^3; surface 327 m^2; f_ren 1.0; vol.-av. beta 2.76 / 2.81 %; vol.-av. electron density 3.17 / 4.21 (1e20 m^-3); peak electron density 5.06 / 6.89; peak D 1.96 / 2.60; peak T 1.96 / 2.60; peak He ash 0.56 / 0.83; n_e0/n_O1 0.64 / 0.87; <n_e>_V/n_Sudo 1.00 / 1.55; peak T_e 15.40 / 12.25 keV; peak T_i 14.63 / 11.64 keV; **Fusion gain: infinity / 182**; **Aux. power at operation point: 0 / 14.77 MW**; fusion power 2700 / 2700 MW; peak fusion heating 5.51 / 6.02 MW/m^3; P/S_LCFS (no edge radiation) 1.18 / 0.91 MW/m^2; total plasma energy 504.65 / 533.14 MJ; av. neutron wall power 2.87 / 2.87 MW/m^2; av. photon wall power 0.70 / 0.72 MW/m^2; peak triple product 3.93e21 / 5.66e21 keV s/m^3; confinement time 1.46 / 1.99 s; alpha slowing-down time 43.76 / 23.75 ms; tau*/tau_E 8.00; tritium burn rate 416.57 / 416.49 g/day; rel. tungsten fraction core 7.76 / 7.55 (1e-6).

Table 4 (Stellaris-pdf p.9, verified in render): f_ren 1.0; f_α 0.95; tau*/tau_E 8.0; f_suppr 0.5; n_W/n_i 1e-5.

The markdown table is wrong in every row I compared. Examples from Stellaris-md L718-L751: "Fusion gain [1] | 4 | 4", "Aux. power at operating point (MW) | 450 | 450", "Minor plasma radius (m) | 1.5 | 1.5", "Magnetic field at axis (T) | 5.0 | 5.0", "Peak $n_i$ temperature (keV) | 24.60 | 17.50", and a Table 4 with "$\tau^*$ | 0.95" and "$n_b/n_e$ | 0.001". Do not use the markdown tables for this paper.

Supporting quotes (Stellaris-pdf unless noted; all checked against the page render):

- p.9, model statement (Stellaris-md L675 same wording): "we chose an integrated treatment of the power balance to assess the required auxiliary power and the fusion gain. This method is sometimes referred to as a '0.5D' treatment, as we calculate with an a priori assumed profile shape, but enforce the power balance by equating the integrated loss power with the integrated heating power, rather than solving a set of transport equations."
- p.9: "where 𝑇𝑒,0 and 𝑛𝑖,0 are varied to match the integrated power balance, and 𝛼𝑇= 1.2 (a peaked profile shape) and 𝛼𝑛= 0.35 (a flat profile shape) are fixed for this study".
- p.9, confinement time: "We apply the ISS04 energy confinement time scaling law from [141], with a modification to replace the heating power by the ratio of plasma energy divided by the energy confinement time. Then, an averaged global energy confinement time is assumed: 𝜏𝐸= 𝜏ISS04 𝐸 (𝑇 , 𝐵 , 𝑎, 𝐴, 𝜄2∕3 )."
- p.9, Fig. 15 caption (full): "POPCON plot illustrating the operational space of Stellaris. The 𝑦-axis represents the on-axis ion (fuel) density 𝑛𝑖,0 = 𝑛𝐷 ,0 + 𝑛𝑇 ,0 in units of 1020 m−3, and the 𝑥-axis denotes the peak electron temperature 𝑇𝑒,0 in keV. The color gradient indicates the auxiliary power required, in MW, as shown by the color bar on the right. Contour lines depict various operational constraints and performance metrics including fusion power (𝑃fus), wall power load (𝑝wall), volume averaged plasma beta (𝛽) and fusion gain (𝑄). The red circles marks specific operating points of interest at constant fusion power, labeled by 'A' and 'B'. The red dashed line shows a possible path to reach the design point from start-up with minimized auxiliary power. The dark gray line indicates the Sudo density limit [131]. The light gray line indicates above which temperature an 'electron root' appears in the center of the plasma at 𝑇𝑖∕𝑇𝑒= 0.95. White regions correspond to areas where the auxiliary power is beyond the color bar limits and would be either inaccessible (high 𝑇, low 𝑛or high 𝑛low 𝑇) or the plasma would ignite (high 𝑇, high 𝑛)."
- p.9, the 50 MW (Stellaris-md L710 has "green dashed line"; the PDF says red): "Fig. 15 shows a scan of the peak electron temperature 𝑇𝑒,0 and the peak ion density 𝑛𝑖,0, along with the required auxiliary power to support the operation point and relevant operational constraints, in a power-output-contour (POPCON) plot. Two chosen operation points are indicated with two red circles (labeled 'A' and 'B'). The red dashed line indicates a path to reach the operation point 'A' with minimal auxiliary heating power. According to the employed model, about 50 MW of auxiliary heating power would need to be installed to reach the desired operation point."
- p.9: "although only the two operation points with the highest fusion power are shown here, the performance of the plasma equilibrium is sufficiently resilient at lower 𝛽values, indicating that all other operation points with 𝑃aux < 50 MW are likely feasible ... However, to keep the same output power of the machine, scaling should be done along lines of constant fusion power (dashed black lines in Fig. 15)."
- p.10, Table 5 caption: "Selected plasma and machine parameters for the two design points shown in Fig. 15. A-priori profiles are used according to Eq. (3). Ratios taken for 𝜏⋆∕𝜏𝐸are assumptions. 𝑛𝑂1 refers to the cut-off density of electron cyclotron resonance heating (ECRH) in the first ordinary (O1) mode. In further studies, until not otherwise stated, values for point A are taken."
- p.10, control scheme: "Compared to tokamaks, stellarators usually require very limited effort on control systems. In the case of Stellaris, the requirements are reduced to achieving density control, detachment and edge radiation control, and potentially control of the edge island locations through an array of control coils." Then the burn-control passage quoted in Q2.
- Stellaris-md L967 (ECRH system sized at the same 50 MW): "We anticipate Stellaris to operate with 50 MW of ECRH power in the plasma, necessitating approximately 6.25 MW of power to be transmitted through each port."
- Stellaris-md L999 (where on the path the heating demand peaks): "We chose a value of ⟨ _𝛽_ ⟩ _𝑉_ = 2% for the analysis here as the auxiliary heating is maximized between 1% and 2% volume averaged plasma _𝛽_, as shown in earlier in Fig. 15."
- Stellaris-md L987-L990 (heating is subordinate at the operating point): "The potential effects of a resulting skewed distribution function of the electron population caused by the heating of trapped particles at the bottom of the magnetic mirror are yet to be investigated, but may be sufficiently small when the dominant heating term is the fusion heating at the operation point."
- Stellaris-md L915 (gyrotron efficiency remark implies ECRH is not expected to run continuously in the ignited case): "making it an attractive heating solution even for steady-state applications in non-ignited plasma scenarios."
- p.32, Appendix A (Stellaris-md L2906-L2932 same text): "we restrict ourselves to a simple '0.5D' power balance, where the power balance is enforced only globally, after integration of both sides of the power balance equation. ... 𝑝loss != 𝑝heat, (A.1) ⇒𝑝rad + 𝑝conf = 𝑓𝛼𝑝𝛼+ 𝑝aux. (A.2)" and "𝑝rad + 𝑤/𝜏𝐸 = 𝑓𝛼𝐸𝛼𝑛𝐷𝑛𝑇⟨𝜎 𝑣⟩𝑇+ 𝑝aux. (A.3)".
- p.32, ISS04 rewritten in T (this is the closed form the POPCON uses): "𝜏𝐸= 0.134 𝑓ren𝑎2.28𝐵0.84𝜄0.41 2∕3 𝑛0.54 19 𝑅0.64𝑃−0.61. (A.7) ... Rewriting the heating power 𝑃in terms of temperature 𝑇, 𝑃= 𝑊∕𝜏𝐸, where 𝑊is the stored plasma energy, one arrives at 𝜏𝐸= 0.152 𝑓2.56 ren 𝑎2.72𝐵2.15𝜄1.05 2∕3 𝑛−0.18 19 𝑅0.08𝑇−1.56 keV, (A.8)".
- p.31, future work list (density control is still an open item): "density control using cryogenic pellets, including deposition profiles and effects on the device performance;"

Two things the Stellaris paper does *not* say: it never states an inequality `P_aux >= 0`, and it never says what the plasma does in the white "would ignite" region. The white region is simply not part of the operational-space plot.

---

## Q5. The HELIAS Beidler source on ignition, burn control, auxiliary heating at the operating point

**Answer.** Beidler treats ignition as a confinement-time comparison: the design point is stated at 3000 MW fusion power, a "required" tau_E is computed, and two empirical scalings are compared against it; ignition is declared possible where the scaling meets the requirement. There is no auxiliary-heating figure at the operating point, no installed heating power, and nothing on burn control or thermal stability. Alpha-particle confinement is discussed only as a prerequisite for self-sustained burn.

Supporting quotes:

- Beidler L98: "Good confinement of highly energetic alpha particles is a necessary condition for selfsustaining operation of the fusion process in a Helias reactor."
- Beidler L104: "The Helias reactor is expected to operate at high density (central electron density of 3x10[20] m[-3] ) and moderate temperature (central temperatures of 15 keV). ... At this level, 1/ ν -losses pose no threat to ignition."
- Beidler L153: "Power balance in the Helias reactor HSR5/22 has been studied by various methods: local transport calculations using the ASTRA-code and the TOTAL_P-code, and extrapolation of empirical scaling laws of stellarator confinement to reactor conditions [14]. ... The following table gives the design point at 3000 MW fusion power. Ignition, however, is possible at lower values of beta, in HSR4/18 ignition occurs at < β > = 3.2%. As shown in Table II, the empirical scaling time (LGS = LacknerGottardi scaling) meets the required confinement time, while the ISS-scaling predicts a confinement time which is too low."
- Beidler Table II (L157-L172): rows "τE (required) [s] | 1.62 | 1.6", "τE (LGS) [s] | 1.65 | 1.83", "τE (ISS95) [s] | 0.96 | 1.2", "Pbrems[MW] | 100 | 86.5", "Pfusion[MW] | 3.06 103 | 2.8 103". No heating row.
- Beidler L176: "Empirical scaling laws (LGS) predict ignition in HSR4/18, any improvement factor is not necessary."

---

## Corpus-wide grep: hits outside the five sources above

Pattern: burn control / burn-control / thermal stability / thermally stable / ignit / POPCON / auxiliary, over `knowledge/sources/*/output.md` and `knowledge/concept_research/09-qi-stellarator-hts/iter-0*/sources/*.md`, barred files excluded. One line each; none is relevant to stellarator burn control.

- `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/stellaris-paper-details.md` L710, L712, L758: a second copy of the same Stellaris prose extraction (same corrupted tables); no new content.
- `knowledge/concept_research/09-qi-stellarator-hts/iter-03/sources/analyst-patch-spec-anchors.md` L38: "**`p_input` MUST be 50 MW** (auxiliary heating wallplug), NOT fusion power." A project-internal anchor note, not a source; it treats the 50 MW as the installed/wallplug input.
- `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/pure-rest-items-item-2140562-component-file-2140561-content.md` L275-L276: "CL-auxiliary return/supply" in a cryogenic-line legend (W7-X magnet paper). Not heating.
- `knowledge/sources/coil_concepts_for_demo_and_next_step_reactors_5th_iaea_demo/output.md` L411-L423: "IGNITOR" the tokamak project name. Not relevant.
- `knowledge/sources/commercialization_of_laser_fusion_energy/output.md` (32 "ignit" hits), `accelerators_for_inertial_fusion_energy_production` (74), `affordable_manageable_practical_and_scalable_amps_high` (80), `a_simplified_economic_model_for_inertial_fusion` L415, `energy_from_inertial_fusion` L69: inertial-fusion capsule ignition. Not relevant.
- `knowledge/sources/energy_from_inertial_fusion/output.md` L135, L656: "auxiliary" = balance-of-plant power ("Auxiliary power (MW) | 55 | 43 | 15"). Not plasma heating.
- `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md` L123, `revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts` L209/L340 ("22.3 Auxiliary Cooling"), `progress_in_eu_breeding_blanket_design_and_integration` L238 ("In-Vessel auxiliary systems: NBI"), `tea_dt_mfe_cost_analysis` L174/L370/L620: cost-account uses of "auxiliary". Not relevant.
- `knowledge/sources/electro_mechanical_properties_of_rebco_coated_conductors/output.md`: "thermal stability" of REBCO conductor. Not plasma.
- `stellaris-design-details.md` L1888: "enhance thermal stability" of NI HTS coils. Not plasma.

No local source outside the five contains a burn-control model, a thermal-stability analysis of an ignited stellarator, or a POPCON.

---

## What a systems code at this fidelity does with an ignited operating point

In my own words, from the practice above.

1. The balance is an equality, always. PROCESS and the Stellaris 0.5D model both write `P_loss =! P_heat` and never an inequality on `P_aux`. `P_aux` is the closing term.
2. When the design intent is an ignited reactor, the codes add a second condition, `Q ~ infinity`, i.e. `P_aux = 0` at the operating point. The optimiser then has to find (n, T, f_ren, R, B, ...) where alpha heating equals losses exactly. Points where alpha heating would exceed losses are not "passing"; they are not solutions, because the equality with `P_aux = 0` is violated there. The Lion 2023 Fig. 5.1 observation that "the optimised f_ren always matches the imposed limit" under the ignition condition, and the statement that temperature must be limited to hold fusion power under wall-load limits, are what this looks like from inside the optimiser: the code walks along the `P_aux = 0` curve and other limits (wall load, beta, ECRH cut-off) pick the spot on it.
3. Installed heating is never derived from the operating-point balance. It is a start-up quantity: the Stellaris paper takes the peak required power along a start-up path (about 50 MW, peaking at 1 to 2% beta), and the Lion 2023 pilot-plant study takes it as a scanned input. The 50 MW inequality in the project's model is therefore a check of the wrong thing at the operating point; the papers' own operating-point check is `P_aux = 0` (ignited) or `P_aux = value <= installed` (driven, e.g. Stellaris point B at 14.77 MW).
4. Nobody at this fidelity models what an over-ignited plasma does. The Stellaris POPCON paints that region white and says the plasma "would ignite"; the Lion 2023 POPCON says the points "would be ignited, given the imposed models" and are held back only by wall-load and beta limits. Burn control is named (density control, confinement degradation) but never given a mechanism or a number in any of these sources.

Which of F1/F2/F3 this resembles:

- The sources' practice is closest to **F1 in spirit but stated as an equality, not an inequality**: the operating point is defined as the point where the balance closes with `P_aux = 0` (or a stated positive `P_aux`). A point with negative required `P_aux` is not a described operating point. If the project wants a fail-closed constraint that matches the papers, `P_aux_required >= 0` (F1) is the inequality form of what the papers do, and it is honest about the model having no burn-control mechanism. Both Lion papers and Stellaris explicitly leave the over-ignited region outside the model's operational space.
- **F2 (density control)** has textual support as a named real-world mechanism (Stellaris p.10: "density control is widely adopted"; Lion 2023 L519: heating "as a plasma state control mechanism") but no source provides a model for it, and PROCESS does not do it: PROCESS lets the optimiser move density *and* temperature *and* f_ren together, subject to the equality. Holding T fixed and lowering n until `P_aux = 0` is a defensible one-dimensional version of what the optimiser does, but it would be the project's own construction, and the sources' own warning applies: the Stellaris paper says scaling should be "along lines of constant fusion power", which lowering n at fixed T does not preserve.
- **F3 (solve for the settled temperature at fixed density)** is closest to how the Lion 2023 § 4.2 pilot-plant study is set up (fixed device, fixed installed power, plasma parameters optimised for maximum Q) and to the "Cordey pass" picture, but the sources never do it as a stability calculation, and Stellaris explicitly expects the temperature to be set by turbulence the 0.5D model lacks ("no tools or workflows currently exist to predict limits with high confidence"). F3 would produce numbers the sources cannot support.

My reading: the sources treat an ignited operating point as a constraint the solver satisfies (equality with `P_aux = 0`), not as a state the plasma falls into. That is F1's content. F2 and F3 both add a mechanism the corpus does not give.

---

## Gaps: what the local corpus does not say

- No burn-control model, transfer function, control gain, time constant, or density-excursion figure for any stellarator, in any source.
- No thermal-stability analysis of the ignited burn (no dW/dt sign, no attractor, no runaway calculation). Stellaris only mentions "thermal runaway effects" to say it suppressed them in the GENE+TANGO check.
- No source says what happens to a plasma placed at (n, T) where alpha heating exceeds losses. The Stellaris POPCON marks the region white and stops.
- How PROCESS implements "Q ~ infinity" internally (an `ignite` switch that drops `P_aux`, or a constraint on Q) is not stated in either Lion paper; only the constraint list line "Require ignited design points, 𝑄∼∞" is given.
- Whether the ignited Helias 5 design points in Lion 2023 carry an installed heating power at all: Table 4.3 did not extract (image only), so unknown from the local corpus. Lion 2021 Table 2 has no heating row.
- The Stellaris paper does not say how the 50 MW start-up path was computed (path shape, ramp assumptions), only that it is the minimum along the red dashed line and that the demand peaks between 1% and 2% beta.
- The Stellaris markdown extraction (both iter-01 and iter-02 copies) has wrong Table 4 and Table 5 values, "green" for "red" dashed line, and "P_fus <= 50 MW" for "P_aux < 50 MW". All values in this report were taken from the page render, not from the markdown.
- Beidler gives no heating power and no ignition mechanism beyond the tau_E comparison.
- Nothing in the corpus on the ITER-style or tokamak burn-control literature; if the team wants a sourced density-control lever it would have to be ingested, which this task did not permit.

Files produced in this directory: `page9.png`, `page10.png`, `table5.png`, `p9_popcon_para.png`, `p9_fig15_caption.png` (page renders used for verification), `stellaris_pdf_text.txt`, `lion2023_passages.txt`, `lion2023_clean.txt` (working extracts). No repository file was modified.
