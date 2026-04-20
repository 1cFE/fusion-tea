---
source: "https://www.osti.gov/servlets/purl/1178069"
source_type: "url"
extracted_at: "2026-04-20T01:07:56.163379+00:00"
content_hash_sha256: "f7454bf8759bc07061cc1e59149fa5a57eb9b19826999cfb0c51203122c26ac7"
backend: "pdf_pipeline"
---

## THEARIESADVANCEDANDCONSERVATIVE TOKAMAK POWER PLANT STUDY 

C. E. KESSEL,[a] * M. S. TILLACK,[b] F. NAJMABADI,[b] F. M. POLI,[a] K. GHANTOUS,[a] N. GORELENKOV,[a] X. R. WANG,[b] D. NAVAEI,[b] H. H. TOUDESHKI,[b] C. KOEHLY,[c] 

L. EL-GUEBALY,[d] J. P. BLANCHARD,[d] C. J. MARTIN,[d] L. MYNSBURGE,[d] 

- P. HUMRICKHOUSE,[e] M. E. RENSINK,[f] T. D. ROGNLIEN,[f] M. YODA,[g] 

- S. I. ABDEL-KHALIK,[g] M. D. HAGEMAN,[g] B. H. MILLS,[g] J. D. RADER,[g] 

D. L. SADOWSKI,[g] P. B. SNYDER,[h] H. ST. JOHN,[h] A. D. TURNBULL,[h] L. M. WAGANER,[i] S. MALANG,[j] and A. F. ROWCLIFFE[k] 

> aPrinceton Plasma Physics Laboratory, Princeton, New Jersey 

> bUniversity of California, San Diego, California 

> cKarlsruhe Institute of Technology, Karlsruhe, Germany 

> dUniversity of Wisconsin, Madison, Wisconsin 

> eIdaho National Laboratory, Idaho Falls, Idaho 

> fLawrence Livermore National Laboratory, Livermore, California 

> gGeorgia Institute of Technology, Atlanta, Georgia 

> hGeneral Atomics, La Jolla, California 

> iConsultant, 10 Worcester Court, O’Fallen, Missouri 

jFusion Nuclear Technology Consulting, Fliederweg 3, D 76351 Linkenheim-Hochstetten, Germany kRetired, Oak Ridge National Laboratory, Oak Ridge, Tennessee 

Tokamak power plants are studied with advanced and conservativedesignphilosophies toidentifytheimpacts on the resulting designs and to provide guidance to critical research needs. Incorporating updated physics understanding and using more sophisticated engineering and physics analysis, the tokamak configurations have developed a more credible basis compared with older studies. The advanced configuration assumes a self-cooled lead lithium blanket concept with SiC composite structural material with 58% thermal conversion efficiency. This plasma has a major radius of 6.25 m,atoroidalfieldof6.0 T,aq95 of4.5,a b[total] N of5.75,an H98 of 1.65, an n/nGr of 1.0, and a peak divertor heat flux of 13.7 MW/m[2] . The conservative configuration assumes a dual-coolant lead lithium blanket concept with reducedactivation ferritic martensitic steel structural material and helium coolant, achieving a thermal conversion efficiency of 45%. The plasma has a major radius of 9.75 m, a toroidal field of 8.75 T, a q95 of 8.0, a b[total] N of 2.5, an H98 of 1.25, an n/nGr of 1.3, and a peak divertor heat flux of 10 MW/m[2] . 

The divertor heat flux treatment with a narrow power scrapeoff width has driven the plasmas to larger major radius. Edge and divertor plasma simulations are targeting a basis for high radiated power fraction in the divertor, which is necessary for solutions to keep the peak heat flux in the range 10 to 15 MW/m[2] . Combinations of the advanced and conservative approaches show intermediate sizes. A new systems code using a database approach has been used and shows that the operating point is reallyan operating zonewith some rangeof plasma and engineering parameters and very similar costs of electricity. Other papers in this issue provide more detailed discussion of the work summarized here. 

## KEYWORDS: ARIES-ACT power plant, engineering and physics design, neutronics 

Note: Some figures in this paper may be in color only in the electronic version. 

## I. INTRODUCTION 

The ARIES Team has examined tokamak power plants with conservative and advanced assumptions applied to the physics and technology characteristics of the plant. These are referred to as advanced and conservative tokamaks (ACTs). Four configurations were studied. Two configurations, namely, advanced physics with advanced technology and conservative physics with conservative technology, were studied in the greatest depth with systems level analysis and both detailed physics and engineering analysis. The remaining configurations, namely, advanced physics with conservative technology and conservative physics with advanced technology, were examined with only systems level analysis. In addition, a number of extensions to the engineering and physics analysis have been included in these studies. 

As part of the detailed engineering analysis, improved approaches include history-dependent inelastic component thermomechanical modeling, transient thermomechanics to model the effects of extremely short-timescale edge-localized modes (ELMs), electromagnetic mechanical analysis of disruptions on the primary conducting structures, modeling of brittle materials in the divertor (tungsten alloys) with fracture mechanics, and threedimensional (3-D) computer-aided design (CAD) tied directly to neutronics modeling. In addition, optimizing materials for their environment in the fusion core has begun with the identification of a potential new (to fusion applications) steel alloy for the vacuum vessel that does not require postweld heat treatment like the reducedactivation ferritic martensitic (RAFM) steels. Experiments were performed at Georgia Institute of Technology to simulate the high-heat-flux He-cooled divertor concepts, demonstrating the strong trade-off of heat flux and pumping power and providing a basis for assumptions made in the power plant divertor design. 

The last tokamak power plant study performed by this team, ARIES-AT (Ref. 1), was completed in 1999. Since then, developments have occurred in both plasma physics understanding and modeling tools. The present power plant study has included analysis of edge plasma and divertor analysis with two-dimensional (2-D) plasma and fluid/kinetic neutral particles, and solutions are sought for the high power handling required in these configurations. In addition, formulations for ELM and disruption heat loading developed for ITER, based on experimental tokamak experience, were used to project the loading on the divertor and the first wall. High-fidelity heating and current drive (H/CD) models are now available and coupled to time-dependent free-boundary integrated plasma evolution simulations, which are now used as part of the physics analysis. The peeling-ballooning magnetohydrodynamic (MHD) stability was used to establish the H-mode pedestal height, and analysis has begun to examine the critical question of whether MHD instabilities due to fast 

alpha particles will lead to losses to the first wall or only to redistribution in these burning plasmas. 

The ARIES systems analysis code has been rebuilt around a new approach, utilizing a database methodology, solving for large numbers of viable operating points, and filtering them to identify attractive candidates. This has allowed the observation that there are always nearby operating points with plasma or engineering parameter changes that have only small differences in the cost of electricity (COE). This leads to the conclusion that although we choose a particular design point to analyze in detail, there are in fact other nearby points that could be viable design points, depending on the progress of plasma science and various areas of fusion technology. 

More detailed descriptions of ACT power plant engineering and physics results can be found in the accompanying papers in this issue.[2–11] 

## II. FOUR CORNERS STUDY OF ADVANCED AND CONSERVATIVE POWER PLANT FEATURES 

The advanced and conservative examination is intended to show how the overall configuration changes with the plant technical philosophy. The advanced physics is described by high normalized plasma beta (bN v 5.8), assuming wall stabilization, and high global energy confinement (H98 * 1.65). The conservative physics is described by low normalized plasma beta (bN v 2.6), assuming no wall stabilization, and lower global energy confinement (H98 * 1.25). In both cases, the lowest density relative to the Greenwald density limit is sought, although it is always equal to or greater than 1.0. In the conservative case, this ratio must exceed 1.0, as the devices become larger and the expression nGr 5 Ip/pa[2] shrinks. The advanced engineering is embodied by the choice of SiC composite structural material blanket concept using self-cooled lead lithium (SCLL), where PbLi eutectic serves as both breeder and coolant, obtaining a thermal conversion efficiency reaching *58% in a Brayton cycle. The peak heat flux in the divertor is allowed to rise to 15 MW/m[2] , roughly consistent with projections based on the experimental results.[5] The conservative engineering is embodied by the choice of a dual-coolant lead lithium (DCLL) blanket concept using RAFM steel structure with helium coolant and a PbLi eutectic as breeder and coolant. This blanket does require flow channel inserts for electrical and thermal insulation between the liquid metal and RAFM steel. This blanket concept can reach thermal conversion efficiencies of *45% with a Brayton cycle. In both cases, the divertor is helium-cooled tungsten alloy with tungsten plasma-facing armor. The conservative case has an upper limit of 10 MW/m[2] divertor peak heat flux. The four corners are illustrated in Fig. 1, as progressive trends in physics and technology, and will be described later. 

![](images/tmp0jkdh0fr.pdf-0003-02.png)

**----- Start of picture text -----**<br>
ACT3 ACT1<br>Advanced Physics Advanced Physics<br>Conservative Technology Advanced Technology<br>Four Corners Study<br>Physics<br>Conservative Physics Conservative Physics<br>Conservative Technology Advanced Technology<br>ACT2 ACT4<br>Technology<br>**----- End of picture text -----**<br>

- Fig. 1. The four corners study of tokamak power plants examines the impact of advanced or conservative assumptions in both physics and technology, referred to as ARIES-ACT1, 2, 3, and 4. 

The ‘‘conservative’’ philosophy applied here is associated with a tenth-of-a-kind power plant, as are all ARIES power plant studies, and is not intended to represent the presently established or ITER research and development (R&D) accessible plasma physics and technology. The latter focuses on what has been developed now or can credibly be envisioned in the short term (see, e.g., Ref. 12), while the former can take credit for a longer-timescale R&D program. Although it is clearly subjective, the parameters chosen to characterize the conservatism are those considered to be the least likely to reach the advanced regimes desired[2,3] ; the bN and its associated energy confinement H98, the achievable peak heat flux in the divertor, and the structural material, its operating temperature, and its associated thermal conversion efficiency. Meanwhile, other assumptions take credit for advances that were thought to be reachable in the time frame to a tenth-of-a-kind power plant, such as peak field at the toroidal field (TF) coil of 16 T for Nb3Sn superconductor,[13,14] electron cyclotron (EC) frequency sources in the range of 200 to 300 GHz (Refs. 15 and 16), operations above the Greenwald density,[17–22] and plasmafacing materials and scrape-off layer (SOL) density control[23–25] to allow effective ion cyclotron radiofrequency (ICRF) and lower hybrid (LH) H/CD. 

There are numerous other prescriptions that are common to both advanced and conservative configurations: 

1. plasma aspect ratio A 5 4.0 

2. up-down symmetric double null 

3. plasma shape, kx 5 2.2, dx 5 0.63 

4. power radiated in the divertor is 90% (Prad,div/ PSOL) 

5. 100% noninductive flattop plasma, inductive assist in ramp-up 

6. Nb3Sn superconductor for TF and poloidal field (PF) coils 

7. He-cooled tungsten alloy divertor 

8. Li15.7Pb84.3 breeder 

9. net electric power production is 1000 MW. 

The plasma aspect ratio has been examined for power plants in previous ARIES studies and has consistently been found to have a weak impact over the range 3 to 5 (Refs. 26, 27, and 28). Although the majority of present tokamaks have an aspect ratio closer to *3, credible physics advantages to lower or higher values in this range have not been established. Operating point plasma parameters will change, such as higher plasma current and lower toroidal field at the plasma for lower aspect ratio (for example); however, the critical physics areas such as MHD stability, energy confinement, high-density operation, or divertor solutions are weakly affected if at all. The double-null plasma assumption and the strong plasma shaping are related. The stronger shaping allows higher ideal beta limits,[29,30] which can be calculated, but experimentally has shown access to higher plasma density,[22] higher pedestals,[31] and even more forgiving ELM regimes.[32] The triangularity is restricted by neutron heating and damage of the TF coil and by the height of the TF coil to accommodate the outboard flux leg. To obtain higher elongation and triangularity, the X-points move closer to the plasma and do not allow strong single-null flux offsets between the active and inactive nulls. This can aggravate first-wall heating near the in-active X-point. The double null provides some reduction in heat to the divertors, but not a factor of 2 due to vertical position oscillations. The vertical stability can be designed with dedicated conducting structures in the blanket and vertical position feedback coils behind the shield.[29,33] The analysis of magnetic or other measurements for vertical position control has not been examined. The high radiating divertor solutions are being pursued in these designs, since both advanced and conservative configurations produce large heat loads with narrow power scrape-off widths.[34] The 2-D SOL plasma and neutral analysis[7] has shown both an ITER-like divertor solution and a fully detached divertor solution; the latter is stabilized by intermittent injection of impurities and requires a wide divertor slot and perpendicular target. The steady-state power plant is preferred in the ARIES studies to avoid cyclic impacts on the engineering systems, ranging from magnet structures and magnet conductor design to thermal cycling of the blanket and divertor structural materials.[35] The Nb3Sn low-temperature superconductor is chosen based on what is expected to be a well-developed program to provide a highly reliable magnet system beginning with ITER large-scale magnets,[36] the development of higher-peak-field magnets through known design optimizations,[13,14] and their continued use on DEMO facilities worldwide. Achievement of high reliability of the magnets, developed though experience on fusion facilities, is arguably of the greatest importance for power 

plant operations. The helium-cooled tungsten alloy divertor is chosen to avoid water in the fusion core for safety, to avoid low thermal performance, and to operate within fusion-relevant material temperature windows. Although tungsten alloys will require significant development, their sputtering resistance, high thermal conductivity, resistance to irradiation degradation, low hydrogen retention, and high melting temperature[37] make them among the only viable options foreseeable. The liquidmetal breeder is considered a superior breeder for power plants because of the ability to control its constituency and tritium breeding (in particular, the[6] Li enrichment) in situ, its lower reactivity with oxygen compared with pure lithium, and its high heat transfer properties. This liquid metal still requires a significantly better understanding of its thermofluid behavior[38] in the simultaneous environment of high magnetic fields, asymmetric heating, corrosion, and mass transfer, as well as the flow channel inserts that electrically and thermally insulate it from the RAFM steel conduit. 

Table I shows several parameters of the ACT designs. Focusing on the ACT1 (advanced physics/ advanced technology) and ACT2 (conservative physics/ conservative technology), the former has a major radius of 6.25 m and the latter 9.75 m. Since the plasma betas are different (b[th] N[5][4.75][in][ACT1][and][2.25][in][ACT2),][they] have compensating toroidal fields (6.0 T in ACT1 and 8.75 T in ACT2). Since in both cases the plasma is required to have 100% noninductive plasma current, the higher bootstrap current fraction (0.91) in ACT1 allows the q95 to remain low at 4.5, a value commonly achieved in present-day tokamaks. ACT2, on the other hand, has higher total plasma current and lower bootstrap current fraction (0.77), leading to a high q95 of 8.0, which is not commonly targeted on present facilities, although easily accessible by operating at lower plasma current. Both cases assumed a total wall-plug efficiency for H/CD (source, transmission, and coupling) of 0.4 (Refs. 39, 40, and 41). The use of a single value for all H/CD sources is a simplification for scanning large regions of parameter space, with the range among these sources spanning *0.25 to 0.5. This could be treated in more detail than is done here in the systems analysis. Improvements in the wall-plug efficiency can be envisioned for each of the H/CD sources [EC, neutral beam (NB), LH, and ICRF], and some of these are described in Sec. VI.A. The assumed current drive efficiency in the plasma (0.15 A/W?m[2] ) for the systems code parameter space scan is also a simplification. Ultimately, the current drive efficiencies subsequently calculated with detailed analysis ranged from 0.1 to 0.45 A/W?m[2] . For all cases examined, the recirculating electrical requirement includes a miscellaneous auxiliary function power of 32 MW, a total pumping power for He and LiPb of *1% of the total thermal power (*2% to 3% of thermal power in the He-cooled divertor), and the calculated H/CD power. In general, power plant design 

points require plasma densities near or above the Greenwald density to obtain the required level of fusion reactions. The advanced physics provides solutions down to nGr, whereas the conservative physics points require up to 1.3nGr. As noted earlier,[17–22] several tokamaks have operated at or over the Greenwald density, reaching up to 1.4 times this limit without disruptions, and obtaining H98 values of 0.8 to 1.0. The energy confinements assumed here in combination with these n/nGr values are above those demonstrated experimentally.[42] Some density peaking is assumed in all cases, with n(0)=SnT ranging from 1.3 to 1.5, since transport theory[43] predicts that peaking is inevitable under the collisionalities typical of power plant plasmas. 

The neutron wall loading values are lower than found in previous studies, which is mostly a result of the heat flux in the divertor, driving solutions to larger major radii. In all cases, a divertor heat flux calculation is used that includes a power scrape-off width from Ref. 44, combined with a highly radiative divertor solution. It is assumed that 90% of the power entering the divertor (PSOL 5 Palpha z Paux { Pbrem { Pcycl { Pline) is radiated in the divertor, leaving only 10% to be conducted to the divertor target plate. The ACT1 case has a peak divertor heat flux on the outboard target of 13.7 MW/m[2] , whereas ACT2 is constrained to a prescribed limit of 10 MW/m[2] . All cases include some argon as a core plasma impurity to provide line radiation, in addition to the cyclotron and bremsstrahlung radiation. The latter two terms dominate the core radiation loss for the power plant regime plasmas. The cyclotron loss is particularly high in the cases with high toroidal field and/or high central electron temperature, and for the systems analysis the reflection of cyclotron radiation from the first wall is taken to be 0.6. The 1.5-dimensional (1.5-D) analysis that is reported in the ACT2 physics basis paper[11] examined first-wall reflectivity of 60%, 75%, and 90%, and this core radiation loss could always be compensated by higher density and reduced argon concentration. The required H/CD power is lowest in ACT1 and highest in ACT2, as would be expected: 42.7 and 105.5 MW, respectively. The fusion plasma gains range from 25 for ACT2 to 42.5 for ACT1. The resulting engineering Qengr, defined as the ratio of net electric power over recirculating electric power (Pelec/ Precir), was highest in ACT1 at 6.6 and lowest in ACT2 at 3.1. The ACT1 power plant layout is shown in Fig. 2, indicating the primary components. The plasma cross sections for ACT1, 2, 3, and 4 are shown in Fig. 3. 

## III. DETAILED PHYSICS CHARACTERIZATION FOR ACT1 AND ACT2 

The plasma configurations identified by the systems analysis were reproduced as well as possible in 1.5-D time-dependent free-boundary simulations of the plasma evolution from early startup at Ip 5 0.5 MA to the flattop 

## TABLE I 

ACT Plasma and Plant Parameters for the Four Corners Examined from the Systems Analysis 

## ARIES ADVANCED AND CONSERVATIVE TOKAMAK POWER PLANT STUDY 

![Fig. 2. ARIES-ACT1 advanced physics and advanced technology power plant configuration.](images/tmp0jkdh0fr.pdf-0006-02.png)

![](images/tmp0jkdh0fr.pdf-0006-04.png)

**----- Start of picture text -----**<br>
5<br>4 ACT4 T3<br>3<br>2<br>ACT2<br>1 ACT1<br>0<br>4 6 8 10 12 14<br>R, m<br>Z, m<br>**----- End of picture text -----**<br>

Fig. 3. The plasma boundaries for the four corners ACT plants identified. ACT1 and ACT2 were examined in detail, whereas ACT3 and ACT4 were examined only at the systems level. 

current value and were allowed to relax over *2500 to 3000 s. Both ACT1 and ACT2 configurations were examined, and Table II shows several plasma parameters from systems analysis and from the 1.5-D analysis. The energy transport was modeled with a modified CoppiTang[45,46] formulation, to allow temperature profile variation (broad to peaked), and scaling to match the required beta. Pedestals were enforced to match the peeling-ballooning theory projections from EPED1 (Ref. 47), with *140 kPa at the pedestal density of 1.0|10[20] /m[3] for ACT1 and 185 kPa at the pedestal density of 0.65|10[20] /m[3] for 

ACT2. Here, we have assumed that the ion and electron densities are equal to the electron density and that the ion and electron pedestal temperatures are equal, Ti,ped 5 Te,ped 5 pped /(2kne,ped). The density profiles and magnitudes were prescribed, allowing some level of peaking of *1.3 to 1.4 in ACT1, and slightly higher (up to 1.55) in ACT2. Argon impurity fractions of 0.3% were used, although in ACT1 it was determined that 0.9% of neon could be substituted for core line radiation. The plasmas have strong shaping, with kx 5 2.2 and dx 5 0.625. 

For the advanced physics of ACT1, wall stabilization of the low-n kink mode was assumed. The broad pressure profile cases were high-n ballooning stable, and they were stable to the resistive wall mode with a tungsten shell on the outboard side at b/a 5 0.3 for bN 5 5.49 to 5.79 at BT 5 6.0 T. The medium-pressure case was stable to these modes at bN 5 5.28 at BT 5 6.75 T. The peakedpressure case was not stable even at bN 5 5.15 at BT 5 7.0 T and was not pursued further. The plasma triangularity was reduced to 0.63 to accommodate engineering design in the divertor, and the stabilizing wall location was determined as a function of triangularity. The fastalpha-particle MHD stability was analyzed, and although found to be unstable, the fast alphas were redistributed to a larger minor radius rather than being lost from the plasma. This result is sensitive to the central ion temperature, the fast beta, and the central safety factor. 

The H/CD systems for ACT1 are ICRF fast wave (FW) at 65 MHz and LH at 5 GHz. The on-axis current is provided by the fast wave current drive (FWCD) and the off-axis current by the lower hybrid current drive (LHCD). The analysis was performed with TORIC fullwave analysis[48] and the ray-tracing one-dimensional Fokker-Planck Lower Hybrid Simulation Code (LSC) (Ref. 49). The LH was found to be optimal if launched at 60 deg above the midplane, limited by the passive stabilizer plates for vertical stability, achieving 0.17 A/W?m[2] . The FWCD was launched from the midplane and achieved 0.45 A/W?m[2] . The total installed LH power was 40 MW and the total installed ICRF power 20 MW, although the flattop required only *5 to 10 MW. Electron cyclotron current drive (ECCD) was also examined as a possible replacement for FWCD. However, its current drive efficiency was too low, at 0.10 to 0.12 A/W?m[2] , although the flexibility to deposit ECCD from minor radii of 0.2 to 0.6 can be effectively used to modify the q-profile with *20 MW of installed power and a reduction in the fusion plasma gain from 42 to 30. Extensive scans of the launcher location and steering angle were examined to find the highest current drive efficiency combinations with GENRAY (Refs. 50 and 51). 

Detailed 2-D edge plasma and neutral simulations of the heat flux on plasma-facing components (PFCs) from exhausting core plasma have been performed for two ACT1 divertor configurations.[7] One configuration utilizes divertor plates strongly inclined with respect to the 

TABLE II 

Plasma Parameters for the Systems Code Operating Point and the 1.5-D Plasma Simulation Operating Point for ACT1 and ACT2 

poloidal magnetic flux surfaces similar to that planned for ITER and results in a partially detached divertor plasma with *75% of the power entering the divertor being radiated. The second configuration has divertor plates orthogonal to the flux surfaces with a wide slot geometry, which leads to a fully detached divertor plasma if the width of the divertor region is sufficient and is found capable of radiating w95% of the power entering the divertor. The fully detached divertor is stabilized by intermittent impurity injection (on and off) with an *1-s timescale, which was found to stop the cold zone from propagating up to the X-point. Both configurations use SOL impurity seeding to yield an acceptable peak heat flux of *12 MW/m[2] with an ITER-like divertor and *2 MW/m[2] with the fully detached divertor. The divertor side walls have v2 MW/m[2] in both cases. The simulations are performed with the UEDGE 2-D transport code[52] to model both plasma and neutral components with some 

supplementary neutral modeling performed with the DEGAS 2 Monte Carlo code.[53] 

For the conservative physics ACT2 configuration, no wall stabilization is assumed, and the resulting stable bN is j2.45 for current profiles with li(1) w 0.75 and tends to drop as li(1) decreases. The introduction of a faraway wall, located 1.35 m from the plasma, which places it behind the ring structure and shield, can allow access to bN of 2.8 to 3.25 over li(1) from 0.85 to 0.65, in combination with plasma rotation, feedback, and/or kinetic stabilization. The high H-mode pedestal was playing a strong role in the low-n stability because of the bootstrap current near the plasma edge. There is slight disagreement between the systems analysis bN values used in operating point searches reported in Table I and those identified from detailed analysis with 1.5-D plasma configurations and ideal MHD, since the systems analysis preceded the detailed calculations. 

The H/CD systems for ACT2 are primarily ICRF/FW at 95 MHz and negative-ion NBs at 1-MeV particle energy. The on-axis current drive is provided by both ICRF, 0.7 MA for 30-MW injected power, and NB, *2.7 to 3.0 MA with 65- to 80-MW injected power. The NB provides a broad current profile across the entire plasma minor radius. Since this configuration requires *4 MA of current drive, NBs are attractive from the deposition viewpoint, since they do not concentrate the driven current. Analysis was performed with the TORIC fullwave code and NUBEAM orbit following the Monte Carlo routine[54] in the TRANSP code. An examination of LH was performed with the LSC, and it was found to penetrate to a normalized minor radius of 0.65 with a broad deposition, where the electron temperature reached 15 to 17 keV. The combination of high toroidal field and low density was favorable for LH in spite of a high pedestal temperature of *9.0 keV. With no wall, up to 1.0 MA of LH could be driven with no effect on the low-n stability, but 1.5 MA or more required the faraway stabilizing wall. The use of EC was examined with TORAY (Refs. 55 and 56) and GENRAY to identify the flexibility of deposition and its current drive flexibility. Deposition from r 5 0.2 to 0.6 was established with scans of the poloidal and toroidal steering, for a range of launching locations. The q-profile could be modified with *20 MW of EC injected power, but bulk current drive, to displace NB current drive, for example, was not efficient. 

## IV. DETAILED ENGINEERING CHARACTERIZATION OF ACT1 AND ACT2 

Engineering design and analysis of ARIES-ACT1 and ACT2 were performed using the most sophisticated tools available in the areas of thermofluids, themomechanics, neutronics, and safety. The use of 3-D CAD modeling helped to establish a self-consistent configuration, to demonstrate assembly and maintenance procedures, and to provide design details for individual components in support of analysis. Complete engineering design and analysis results are reported in several papers in this issue.[2,4–6,8–10] 

## IV.B. Component Design and Analysis 

Extensive 3-D analysis was performed to assist in design and to demonstrate acceptable performance of the main power core components. Compared with earlier studies, increased emphasis was placed on inelastic behavior of materials (e.g., thermal stress relaxation, ratcheting, creep, and fracture mechanics), transient loading conditions, and coolant manifold design and fabrication. Here, we summarize very briefly the most salient features and conclusions from component design studies. 

## IV.B.1. First Wall and Blanket 

The heart of the power core is the integrated first wall and blanket, which produces the majority of high-grade heat, breeds all of the tritium fuel, and shields other components from the radiation environment. Plasma vertical position and external kink stabilizing shells are embedded in the blanket, and the whole assembly is held together within a ‘‘strongback’’ structural ring made of an alloy of RAFM steel. The blanket sectors for ACT1 and ACT2 are shown in Fig. 4, identifying primary components. Both ACT1 and ACT2 adopted liquid PbLi eutectic as both breeder and coolant. ACT1 uses the self-cooled PbLi concept with SiC composite structures, whereas ACT2 uses a dual-cooled blanket with about half of the heat removed by He in RAFM steel structures. Notably, ACT2 is the first integrated power plant study by the ARIES Team using the DCLL blanket; previous applications included a spherical torus and compact stellarator power plant. Detailed analysis was performed on the first wall and blanket, demonstrating that all design rules and material limits were met. Two novel alternative concepts were developed for ACT2: a first-wall design capable of handling a heat flux of up to 2 MW/m[2] with tungsten plugs short-circuiting the conduction path to the coolant, and a ‘‘small-module’’ DCLL design that offers potential advantages in fabrication and simplicity. For both ACT1 and ACT2, far more detail was included in the design of manifolding that takes both He and PbLi coolant from the external headers and distributes them into each cooling channel. 

## IV.B.2. Divertor 

## IV.A. Power Core Configuration and Maintenance 

The configuration of both ACT1 and ACT2 is based on a full-sector horizontal maintenance strategy.[57–59] This choice has been shown to provide the fastest change-out of in-vessel components, with the main penalty being larger TF coils to provide sufficient clearance. Each sector is self-supporting, with sector-to-sector connections but no attachment to the vacuum vessel. Gravity loads are transferred vertically through the bottom of the vessel and into support pillars. Full CAD drawings were produced, and 3-D motion studies demonstrated adequate clearances for assembly and maintenance. 

Few options are available for a divertor capable of withstanding time-averaged heat fluxes in the range of 10 to 15 MW/m[2] with acceptable radiation damage and activation characteristics. Based on our previous studies[60–62] and a growing body of international research,[63,64] we chose to use a He-cooled W-alloy divertor for both ACT1 and ACT2. The natural high operating temperature of W allows efficient utilization of the thermal power, *20% of the plant total. Several internal design options were explored, all using impinging jets to provide adequate heat transfer and to maintain all materials within their operating limits. For ACT1, the final design uses the 

![Fig. 4. Sectors for (a) ACT1 and (b) ACT2, showing the first wall and breeding blanket, the stabilizing shells, the structural ring/shield, the lower and upper manifolding for coolants, and the divertors.](images/tmp0jkdh0fr.pdf-0009-02.png)

plate-type design with slot jets throughout the majority of the divertor and circular jet arrays in a modified multijet ‘‘finger’’ design in regions where the heat flux is w8 MW/m[2] . For ACT2, a pure plate-type divertor was 

possible because of the lower peak heat fluxes. One of the most important design features of our divertor is the absence of ‘‘duplex’’ structures, in which W is bonded to steel, within the high-heat-flux region. Extensive ‘‘birthto-death’’ inelastic stress analysis was performed on the external transition joint from W alloy to the external steel piping, including a tantalum alloy interlayer and braze materials.[65] 

## IV.B.3. High-Heat-Flux Experiments 

Because of the importance of the choice of He as divertor coolant, experiments were conducted as part of this study to demonstrate acceptable performance and, in conjunction with numerical simulations, to provide semiempirical design relations for several impinging-jet concepts,[5,66] including both linear slot jets (e.g., for the plate-type and T-tube designs) and circular jet arrays (e.g., for ‘‘finger’’ designs). The experiments were carried out under ‘‘dynamically similar’’ conditions to a power plant and produced both heat transfer coefficient and pressure drop relations. The results substantiate our design choices for the specified loading conditions (up to 10 MW/m[2] in ACT2 and 13.7 MW/m[2] in ACT1) and pumping power estimates (12 MW for He in the divertor and Ppump/ Pthermal 5 2% for ACT2, and 10 MW He in the divertor and Ppump/Pthermal 5 2% for ACT1). Simulations[2] show that the pumping power is a function of the heat flux. It should be noted that the high-heat-flux region in the divertor is a small fraction of the total divertor surface being cooled, and since the pumping power is directly related to the incident heat flux, the total pumping powers are lower, which is shown in related papers.[2,10] 

## IV.B.4. Vacuum Vessel 

A novel vacuum vessel was designed and thoroughly analyzed using 3-D finite element analysis.[67] The vessel can operate at an elevated temperature of 350 u C to 500 u C and uses He as coolant; the absence of water and the high operating temperature help control tritium migration and inventory. We chose to use a low-activation 3Cr-3WV bainitic steel[68,69] that provides lower activation than Type 316 stainless steel and no need for postweld heat treatment as required for RAFM steel, which would be extremely difficult to perform. Thermomechanical analysis was performed for gravity, pressure, thermal stress, and transient electromagnetic loading conditions. 

## IV.B.5. Power Conversion 

Achieving a high thermal conversion efficiency is important not only because it directly affects the COE but also because system studies show that the design space for a tokamak power plant is significantly larger when the efficiency is high. Less demand on other systems, especially the plasma, enables a more modest plasma beta, lower peak toroidal field, and other advantages. The He 

## ARIES ADVANCED AND CONSERVATIVE TOKAMAK POWER PLANT STUDY 

Brayton cycle[70,71] was chosen for both ACT1 and ACT2 because it offers a good match to the high operating temperatures of He and PbLi coolants on the primary side. For ACT1, the structural material is SiC composite with a maximum temperature of 1000 u C, allowing the LiPb exit temperature from the blanket to be 1030 u C; the He exit temperature from the structural ring is 680 u C, and the He exit temperature from the divertor is 800 u C. For ACT2, the structural material is RAFM steel (oxide-dispersionstrengthened for higher-temperature regions such as the divertor) with a maximum temperature of 550 u C, allowing an LiPb exit temperature from the blanket of 647 u C with SiC composite flow channel inserts, a blanket He exit temperature of 470 u C, a structural ring He exit temperature of 385 u C, and a divertor He exit temperature of 720 u C. These are consistent with the predicted thermal conversion efficiencies identified in Ref. 71. The intermediate heat exchanger was designed with careful attention to the operating temperature limits of all of the components contributing to power conversion. Thermal cycle analysis predicts a thermal conversion efficiency (including cycle pumping powers but not the plant ancillary electrical equipment) of 58% for ACT1 and 45% for ACT2. 

## IV.B.6. Material Choices 

Many materials are needed within the radiation environment to satisfy all of the functions of the power core, including structures, joining materials, plasma armor, coolant and breeder, thermal and electrical insulators, connectors, conducting shells, etc. We attempted to identify attractive candidates for all of the mission-critical materials but focused our more detailed evaluations on structural materials. Further alloy development and characterization, and the development of design rules, are needed for both ACT1 and ACT2. Both designs require a W-alloy and advanced (oxide-dispersion-strengthened) RAFM steel alloy for the divertor. The ACT2 blanket relies primarily on conventional RAFM steel structures[72] (e.g., F82H or EUROFER97), whereas ACT1 depends on the development of SiC composites.[73] Of particular note is the proposed 3Cr-3WV bainitic steel alloy for the vacuum vessel. This alloy is not new but has been applied for the first time in a fusion power plant design. More details on materials assumptions and R&D needs can be found in related papers.[2,10] 

## IV.B.7. Nuclear Analysis 

Nuclear analysis[9,74] (neutronics, shielding, and activation) has a major impact on the evolution of our designs and their safety and environmental characteristics. For the nuclear analysis in ARIES-ACT1 and ACT2, state-of-the-art 3-D computational tools were utilized to determine the neutronics, shielding, and activation parameters. Essential measures that helped deliver optimal ACT designs include estimating the tritium breeding ratio 

(TBR) with higher fidelity than was previously possible; defining the radiation environment within the fusion power core in terms of accurate neutron wall load (NWL) profile; optimizing all components comprising the radial/ vertical builds, keeping in mind the activation characteristics of the preferred materials; determining the nuclear heat loads to all components, including the fine details of the blanket; and estimating the radiation damage to structural components and their service lifetimes, taking into consideration the peaking due to neutron streaming through assembly gaps. Our nuclear results reveal that both ACT1 and ACT2 designs satisfy the breeding requirements, with LiPb breeder, of 1.05 TBR with 40% 6Li enrichment (v90%), and have an energy multiplication of *1.16, with He:LiPb thermal power ratios of 27:73 for ACT1 and 49:51 for ACT2. The service lifetimes (average NWL 5 2.3 MW/m[2] ) for ACT1 of 5 full-power years (FPY) for the first wall, blanket, and divertor, 20 FPY for the structural ring, and 40 FPY for outer components were based on radiation damage considerations. The ACT2 components exhibit extended lifetimes because of lower NWL (average NWL 5 1.5 MW/m[2] ) of *8 FPY for first wall, blanket, and divertor and 40 FPY for outer components. The radial builds for ACT1 and ACT2 are developed to allow the superconducting magnets to be lifetime components (40 FPY) against superconductor damage, insulator damage, and copper stabilizer damage and to maintain the instantaneous nuclear heating v2 mW/cm[3] . In addition, the vacuum vessel is protected to allow rewelding. The presence of assembly gaps or other discontinuities that can allow neutron streaming is examined with the 3-D analysis, in particular for the structural ring and vacuum vessel, showing potential for significantly higher displacements per atom (dpa) and atomic parts per million (appm) He production in the gap locations. The component lifetimes here are determined by the peak outboard neutron fluence (or dpa), assumed here to be 180 dpa for RAFM steel or 3% burnup for SiC composite structural material, and do not include the possible effects of erosion of plasma-facing materials. These damage limits are well above any fusion-relevant neutron exposure levels, since sources are scarce, and exceed the highest fission neutron exposures to date.[75,76] The erosion of PFCs or the property degradation of redeposited materials is considered a serious lifetimelimiting phenomenon,[77] and this area should receive more attention to provide a viable engineering boundary condition. The erosion of PFCs was not addressed in this study. The actual maintenance schedule involves routine access every 12 to 18 months[58] with staggered sector change-out but could provide a means to replace the divertor more often if necessary. The impact of these effects on the first wall, divertor, and launching or other special PFCs could impact their design and maintenance approaches. The nuclear heating and decay heat analyses 

## IV.B.9. Safety Analysis

In assessing safety aspects, both ARIES-ACT1 and ACT2 employ multiple coolants and coolant loops that give rise to a number of different possible accident scenarios involving loss of flow or coolant. Helium is used as the coolant in the reactor, first wall, divertor, vacuum vessel, while LiPb cools the blanket. Water is used in the low-temperature shield outside the vacuum vessel. Because of resource limitations, a detailed safety analysis was performed only on ARIES-ACT1. Three variations of Fukushima-like scenarios were considered, involving long-term station blackout (LTSBO) or loss of forced convection in all loops (LOFA), and demonstrated that no releases from the ARIES-ACT1 power core will be expected. The LTSBO/LOFA scenario alone constitutes a design-basis accident in this scenario. We also show that the water coolant (which functions as both a neutron shield and an emergency cooling system) adequately removes decay heat in this scenario. We also considered two beyond-design-basis accidents in which the loss of power is accompanied by a loss-of-coolant accident (LOCA) in the helium and water loops, respectively. The helium LOCA does not represent an extreme for structure temperature (helium in the crystal provides another path for removal of decay heat), but it is necessary to ensure that resulting pressure increases in the cryostat do not exceed the design margin of this confinement boundary, which was demonstrated. In the third accident scenario, a water LOCA occurs during the power outage. Since the water is the primary emergency heat removal mechanism, and the intact PbLi heat transfer system still contributes considerable decay heat, this represents a worst-case scenario from the standpoint of removal of decay heat. The only mechanism for its removal is radiation through the maintenance ports to the vacuum boundary. The MELCOR model does not predict any catastrophic failures in this case, although some potentially nonconservative assumptions remain to be more thoroughly investigated.

## V. SYSTEMS ANALYSIS OF OPERATING POINTS

The systems code is used to evaluate a large number of possible operating points while satisfying physics and engineering constraints. The modeling of the plasma and plant systems is simplified to examine the integrated plant rapidly over many scenarios. A zero-dimensional code has sufficient accuracy in its representations, but ultimately an operating point or points are examined with detailed analysis outside the scope of the systems code.

The systems code can be described by its modules: physics, engineering, buildout, and costing.[31] The physics module solves for zero-dimensional power and particle balance, including expressions for the radiated powers, bootstrap current, fast-particle beta, Bosch-Hale DT fusion reactivity, up to four H&CD systems, and up to seven impurities. The plasma profiles are parabolic, modified to include a finite value at the edge. The plasma operating space is identified by scanning all critical plasma configuration variables ($R$, $B_T$, $n_0/n_e$, $A$, $\delta$, $A$, $Q$, $I_p$, $f$ profile, $n$ profile, impurity fraction, $n/n_{GW}$, $v_{bs}$, and $\tau_E^*/\tau_E$). Initially, the ranges for these parameters are chosen to be very broad, and after scanning a broad range, as attractive parameter space is identified. The resulting database will have a large number of operating points that satisfy the physics constraints, with a wide range of fusion powers. For ACT1 and ACT2, $\tau_E^*/\tau_E$ was set at 5 (different fusion enhancement; see Ref. 3), $A$ (Ref. 4) = 0.15 A/W·m² (× 10^20), $\Lambda$ (= $R/a$) was set at 4.0, and $\delta_x$ was set at 0.5 for ACT1 and 0.75 for ACT2. The plasma elongation was scanned over a range from 1.7 to 2.2 (corresponding to X-point elongations of 2.0 to 2.2), although 2.1 provided a larger operating space in ACT1 [?] and was pursued further. The plasma triangularity was made 0.575 (corresponding to an X-point value of 0.625) at the highest values consistent with engineering constraints. At first, very broad and coarse scans were done to isolate plasma major radii and toroidal fields of interest. Next, for ACT1, the major radius was scanned from 5.0 to 7.5 m, the toroidal field from 4.5 to 7.5 T, $\beta_N$ from 4 to 6, $q_{95}$ from 3.25 to 6.0, $n/n_{GW}$ from 0.8 to 1.6, $Q$ from 20 to 50, $f_{BS}$ from 0 to 0.8, $f_{He}$ (%) from 1 to 4, and $T(0)/\langle T \rangle$ from 1.9 to 2.7. For ACT2, the major radius was scanned from 5.5 to 8.0 m, the toroidal field from 5.5 to 10.5 T, $\beta_N$ from 2 to 4, $q_{95}$ from 3.5 to 9.0, $n/n_{GW}$ from 0.9 to 1.6, $Q$ from 12.5 to 40, $f_{BS}$ from 0.2 to 1.0, $f_{He}$ (%) from 1 to 4, and $T(0)/\langle T \rangle$ (peak to average temperature ratio) from 1.9 to 3.1. Once operating points that provide 1000 MW(electric) are found, these scans can be focused to identify the systems-optimal design points.

The physics points are passed through all the primary engineering constraints, including the TF coil constraint, the inboard radial build of the first wall, the blanket, the shield (adjustable to $\langle N_w \rangle$), and the vacuum vessel. The outboard radial build is also available for costing, but this region is not critical to operating point identification. Evaluations include the first-wall heat flux, the divertor heat flux, the power assumed to flow to the divertor bypass (including breakdown in blanket and divertor), the TF coil peak field, a stability criterion, and the fields in the solenoid/PF coils. A graphical user interface was developed to help visualize the design space resulting from several million system runs.[32] Historically we found that a prescreening process was valuable to reduce the

data set to a more tractable and meaningful number of points. This was accomplished using a set of filters on individual parameters. For example, net electric power output was typically filtered to accept only values between 975 and 1025 MW(electric). The database will include a wide range of plasmas with different values for fusion power, which allows one to easily scan engineering and balance-of-plant parameters such as the thermal conversion efficiency, H/CD wall-plug efficiency, or the impacts of pumping power or other electrical requirements. Different net electric power can be requested, as well as the sensitivity to assumed engineering parameters, such as the peak toroidal field at the magnet or the peak heat flux in the divertor.

Other filters are generally applied to isolate the physics points to meet some criteria, such as $\beta_N$, $H_{98}$, or $n/n_G$. Ultimately, the maximum major radius solution is sought, although this is not a hard criterion in general, and a range of radii are normally left in the database. The operating points that are left are passed through the full buildout of the plant, adding the top and bottom radial build and divertors and the outboard radial build. These are then costed based on unit costs, such as $/kA-m turn or scalings involving thermal power or other relevant parameters.

The most important observation from this database approach to systems analysis is that the idea of an optimal operating point, as one might define from an optimizer systems analysis, is not appropriate since the uncertainty in virtually all associated parameters is too high. It is seen in the database that there are a range of design points with very close COE, having different values for the toroidal field in the plasma, the beta, fusion gain, peak beat flux in the divertor, bootstrap current fraction, impurity content, and so on. For example, our knowledge of the maximum achievable toroidal field at the TF coil, or the maximum achievable beta, does not justify such a precise single operating point. Table III shows a sample of solutions found for the advanced physics and advanced technology ACT1 power plant search, each with a COE that is within 5% of the reference case. The parameter minimum or maximum is shaded for the alternate configurations, which includes the highest $\beta_N$, lowest major radius, lowest divertor peak heat flux, lowest $\beta_N$, and lowest toroidal field. The operating point is actually a space and could be identified by a set of parameter ranges, such as $R = 6.0$ to 6.75 m, $B_T = 5.25$ to 7.25 T, $\beta_N^{tot} = 4.8$ to 6.0, and $q_{pk}^{div} = 10.5$ to 14.7 MW/m². Those parameter ranges can be further prescribed by their inter-relationships, or trade-offs, such as $B_T \cdot \beta_N^{tot}$ of 5.25–5.96 to 7.25–4.77. Comparing with the table found in scenario III, if the highest peak heat flux tolerable in the divertor is ~10 MW/m², then the operating point must obtain a larger major radius, which leads to higher costs, increased H/CD and radiation loss powers, and a higher cost to accommodate the requirement.

Table IV shows a small sample of points around the conservative physics and conservative technology ACT2 configuration. The alternate cases have their COE within approximately ±4% of the reference case. This plasma operating space was strongly affected by the divertor peak heat flux and the $\beta_N^{tot}$ constraints, causing the major radius up to 9.75 m. The parameter minimum or maximum is shaded for each alternate case, including the cases with highest toroidal fusion gain, lowest divertor peak heat flux, and lowest toroidal field. The last column in the table shows the reduction in major radius from the reference case by 1.0 m when allowing

## TABLE III

*Several Nearby Operating Points for ACT1 with <5% Increase in COE from the Reference, Indicating that a Range of Plasma Parameters are Accessible.*

| | ACT1-ref | ACT1-a | ACT1-b | ACT1-c | ACT1-d | ACT1-e |
|---|---|---|---|---|---|---|
| $R$ (m) | 6.25 | 6.25 | 6.0 | 6.75 | 6.25 | 6.75 |
| $I_P$ (MA) | 10.9 | 11.3 | 11.6 | 11.5 | 11.25 | 11.3 |
| $B_T$, $B_T^{max}$ (T) | 6.0, 11.8 | 7.25, 10.2 | 7.0, 12.5 | 5.25, 11.2 | 6.0, 11.8 | 5.25, 9.05 |
| $\beta_N^{tot}$, $\beta_N^{th}$ | 4.75, 0.85 | 5.0, 0.96 | 4.5, 0.83 | 4.25, 0.82 | 4.0, 0.77 | 5.0, 0.96 |
| $H_{98}$ | 4.5 | 1.23 | 1.0 | 1.2 | 1.0 | 1.23 |
| $H_{98}$ | 1.65 | 1.62 | 1.65 | 1.65 | 1.65 | 1.52 |
| $n/n_G$ | 0.91 | 1.03 | 1.15 | 1.22 | 1.20 | 0.89 |
| $f_{BS}$ | 0.91 | 0.90 | 0.91 | 0.91 | 0.89 | 0.85 |
| $q_{pk}^{div}$ (MW/m²) | 13.7 | 12.8 | 14.7 | **10.5** | 14.0 | 0.90 |
| $f_{He}$ | 42.7 | 45.0 | 47.0 | 49.5 | 51.0 | 0.85 |
| $P_{fusion}$ (MW) | 1813 | 1919 | 2096 | 1894 | 2009 | 2012 |
| $\langle S_n \rangle$ (MW/m²) | 3.45 | 2.60 | 3.08 | 2.20 | 2.72 | 2.72 |
| $P_{electricity}$ (MW) | 115.5 | 106.8 | 106.7 | 132.1 | 132.1 | 129.4 |
| COE | 64.3 | 64.4 | 66.3 | 67.0 | 66.5 | 66.6 |

TABLE IV 

Several Nearby Operating Points for ACT2 with[+] 4% Difference in COE from the Reference, Indicating that a Range of Plasma Parameters are Accessible 

b[total] N to rise to 3.0, and the peak divertor heat flux is only slightly above our limit of 10 MW/m[2] . This increase in b[total] N is consistent with a faraway wall behind the blanket and ring structure shield, as identified in the detailed ideal MHD stability analysis. On the other hand, comparing columns one and two, if higher peak divertor heat fluxes are tolerable, then the major radius can be reduced compared with the reference case, with most other parameters very similar, and a reduced cost. The operating point range here for ACT2 would be described as R 5 9.25 to 10.0 m, BT 5 8.0 to 8.75 T, b[total] N ~ 2:6, qdiv[peak] ~ 9:0 to 14.9 MW/m[2] , and Q 5 20 to 27.5, for example, which is clearly differentiated from that for ACT1. The benefit of allowing a slightly higher b[total] N can be clearly identified with the database approach, and the implications can be examined with detailed analysis. 

Although the COE is a useful collective measure for a configuration, it does not adequately represent the operating space of possible configurations that exist, since we typically impose several constraints or limits based on what plasma physics or technology advances are considered reachable. These projections are in fact quite uncertain, and demonstrating viable configurations where these projections are both more or less aggressive provides greater credibility to the plant identification. The database approach can clarify the impact of the projections on the other plasma and engineering parameters, such as the geometry (major radius). 

## V.A. Comparison of ARIES-ACT1 and ARIES-AT 

The last tokamak power plant study performed by this team was the ARIES-AT (Ref. 1) design in 1999, and 

comparing the advanced physics and advanced technology ACT1 design point with that older design is of interest to account for the changes that have taken place. Table V provides some physics parameters of the two plants. In 1999, the power scrape-off width formulation from the physics community[80] was proportional to the SOL power in the numerator, so that as the power leaving the plasma and transporting to the divertor increased, the scrape-off width would also increase. The calculated peak heat flux in the divertor for ARIES-AT was then 5 MW/m[2] , which could be handled by a PbLi coolant and SiC composite structure, with a thin tungsten coating for resistance to sputtering. By 2002 and 2003, the formulation for the power scrape-off width had changed to having the SOL power in the denominator, causing a reduction of the power scrape-off width with increasing power. The ACT activity adopted an explicit SOL width formulation derived from Fundamenski et al.[44] for the systems analysis, and an expression for the peak divertor heat flux given by 

![](images/tmp0jkdh0fr.pdf-0013-10.png)

![](images/tmp0jkdh0fr.pdf-0013-11.png)

![](images/tmp0jkdh0fr.pdf-0013-12.png)

in combination with a high radiated power fraction (fdiv,rad 5 Pdiv,rad/PSOL 5 90%) in the divertor. The conducted power footprint areas can then be given 

TABLE V 

Parameters for the Advanced Physics and Advanced Technology Design ARIES-ACT1 and the ARIES-AT, also an Advanced Physics and Technology Plant 

*The original divertor peak heat flux was reported as 5 MW/m[2] ; this value uses the same approach as the ACT studies. 

approximately by 2p(R { a/2) lpowfyftilt for the outboard and 2p(R { a)l powfyftilt for the inboard, where fy is the poloidal flux expansion (determined from equilibria) and ftilt is the divertor target tilt angle expansion. These are reasonably accurate for the typical plasma geometries examined in the ARIES studies. The radiated power footprint areas are taken approximately as 2p(R { a/2) |(a/2)|2 on the outboard and 2p(R { a)|(a/4)|2 on the inboard, which includes the dome and sidewalls of the divertor slot. The power plants typically have power scrape-off widths of 3 to 5 mm, which provide the need for highly radiating divertor (partially to fully detached) operating regimes. Using the same formulation for ARIES-AT, the peak heat flux on the outboard divertor would be 22.6 MW/m[2] , as opposed to the original 5 MW/m[2] . Simulations with UEDGE 2-D plasma and fluid/kinetic neutral codes[7] indicate that the highly radiating regimes may be accessible either with an ITER-style strongly inclined target to obtain 75% radiated power and *12 to 13 MW/m[2] peak heat flux or with a perpendicular target and wide slot geometry divertor to obtain w95% radiated power and *2 MW/m[2] on the target and side walls. The engineering design of the divertor was also changed to He-cooled tungsten alloy utilizing plate or finger jet-impingement designs into handle the resulting heat fluxes over a range up to 10 to 15 MW/m[2] . 

Another critical parameter that was updated in the ACT studies is the wall-plug efficiency for the H/CD systems, which should include the source efficiency, the 

transmission efficiency, and any coupling to the plasma efficiency that applies. In the ARIES-AT study, this parameter was generally taken to be *0.7 to 0.75. Recent reviews of this parameter[40,41] indicate it is *0.4 for all sources (NB, EC, LH, and IC), with a range of 0.25 to 0.5, in spite of varying values for the individual contributions among the different sources. For simplicity this value is assumed in the systems analysis regardless of the H/CD scheme. This parameter, which increases the recirculating power associated with the H/CD system, and the treatment for the peak heat flux in the divertor both contribute to the larger plasma major radius for ARIESACT1 at 6.25 m compared with ARIES-AT at 5.20 m. Although both ACT1 and ARIES-AT operate at their Greenwald density limit, the ACT1 case has a 60% lower density because of the increased size of the plasma and lower plasma current. The shift to larger plasma size in ACT1, for the divertor heating, and the reduced wall-plug efficiency conspire to lower the plasma current and raise the minor radius, both making the Greenwald density lower. The larger plasma volume can compensate the lower plasma density to provide a similar fusion power, since Pfusion~ Ð nDnTSsvTEfusion dVplasma : 

The physics description of the plasma is improved by incorporating 1.5-D analysis that has limited the broadness of temperature and current profiles compared with the purely equilibrium analysis of the ARIES-AT study. The use of the peeling-ballooning pedestal constraint[17] has provided a consistent profile constraint at the plasma edge compared with the L-mode or ad hoc H-mode edge treatments in ARIES-AT. The triangularity has been lowered to accommodate engineering space and shielding requirements; however, it still remains high at 0.63. Higher-fidelity H/CD analysis using modern tools such as TORIC full wave (Ref. 17) for ICRF, NUBEAM (Ref. 21) for NB, LSC (Ref. 18) for LH, and GENRAY (Refs. 24 and 25) and TORAY (Refs. 22 and 23) for EC, has allowed more consistent configurations to be defined, with significantly better predictions for current drive efficiency than previously available. 

## V.B. The ACT3 and ACT4 Operating Points Identified 

The ACT3 advanced physics with conservative technology and ACT4 conservative physics with advanced technology configurations provide a way to view permutations on the all-advanced or all-conservative designs. ACT3 combines the high-bN and high-energy-confinement plasma with the conservative DCLL blanket concept and its thermal conversion efficiency of *45%. The major radius of this design is 8.5 m, and the corresponding peak heat flux in the divertor is 9.6 MW/m[2] with 90% radiated power fraction. The edge safety factor q95 is 4.25. The fusion power of ACT3 is similar to that of the conservative ACT2 since the thermal conversion efficiency dominates the determination of the required fusion power to generate 1000 MW of electricity. 

The ACT4 configuration combines a low-bN and lower-energy-confinement plasma with the advanced technology SiC composite blanket with a thermal conversion efficiency of *58%. The major radius of this design is 8.0 m, and the corresponding divertor peak heat flux is 8.6 MW/m[2] with 90% radiated power fraction. In this particular case, it was not difficult to find cases with low divertor peak heat flux, since the power terms are similar to those of ACT1, and the major radius is 30% larger. Its fusion power is close to that of the all-advanced ACT1 design because of its high thermal conversion efficiency. The peak toroidal field at the TF coil did reach 16 T, which we have used as a limit in these studies. The limiting criteria to keeping the plasma major radius from dropping were the TF limit of 16 T at the TF coil and the desire for higher fusion gain. For example, 7.5-m major radius plasma solutions existed with peak toroidal field at 16 T; however, the fusion gain had dropped to 17.5, so a slightly higher major radius was chosen to recover a fusion gain of 27.5. 

Both ACT3 and ACT4, which combine advanced and conservative features, demonstrate a larger major radius than ACT1 and a lower major radius than ACT2, as might be expected. Since the technology philosophy is primarily a change in the thermal conversion efficiency, the fusion powers are similar between the advanced technology (ACT1 and ACT4) and conservative technology (ACT2 and ACT3) variants. Similarly, the physics philosophy is primarily a bN-BT-q95-H98-n/nGr combination change, and ACT3 and ACT4 retain the physics parameters associated with the advanced or conservative choice. On the other hand, several parameters end up intermediate between the all-conservative and all-advanced configurations, in addition to the major radius. These include the plasma density, NWL, H/CD power, recirculating power, fusion plasma and engineering gains, and COE. Overall, these configurations show that advancing physics or technology can potentially reduce the device size and cost over an all-conservative configuration. 

In 1991, the first ARIES power plant design was completed, referred to as ARIES-I (Ref. 26), which targeted conservative physics and advanced technology. The assumption for bN was 3.2, the global energy confinement multiplier H98 was 1.49, and there was a current drive efficiency of 0.37 for ICRF/FW, a wall-plug efficiency for that H/CD system of 0.72, a SiC composite blanket with a thermal conversion efficiency of 49%, a neutron multiplication factor for heating in the blanket of 1.3, and assumptions about the pumping and auxiliary systems recirculating powers. At the time, the estimated peak heat flux in the divertor was 3.88 MW/m[2] , whereas our present analysis finds a value of 15.3 MW/m[2] , which is too high for our conservative technology assumptions and at the upper limit for our advanced technology assumptions. Table VI shows several parameters of the ARIES-ACT4 (conservative physics/advanced technology), 

ACT2 (conservative physics/conservative technology), and ARIES-I. ARIES-I obtained a smaller major radius than either of these recent ACT designs, which has been tracked down to a higher H98 assumption, a higher bN assumption, a higher wall-plug efficiency, and a high divertor peak heat flux. Better understanding and analysis shows us that the bN 5 3.2 for the profiles assumed is too high without a stabilizing shell. The strategy for externally driving current with ICRF/FW is not considered feasible since it relied on multipass absorption to distribute the current across the minor radius, and this is not experimentally observed. The current drive efficiency assumed for ICRF was close to that obtained from simulations for the ACT studies. The assumed energy confinement in ARIES-I is high relative to ACT2 and ACT4, which have conservative physics assumptions. The ARIES-I design was also attempting to take advantage of high magnetic field at the plasma and TF coil, above those now considered feasible for lowtemperature superconductors based on Nb3Sn. 

## VI. CONCLUSIONS 

The ARIES-ACT study has examined the impact of conservative and advanced physics and technology assumptions on the steady-state tokamak power plant configuration to produce 1000 MW of net electric power. The advanced characterization of high b[total] N (5.75), high H98 (1.65), and SiC composite structure SCLL blanket concept (gth 5 58%) results in a 6.25-m plasma with 11 MA of plasma current and 6.0-T toroidal field. The conservative characterization of low b[total] N (v2.60), low H98 (1.25), and RAFM steel structure DCLL blanket concept (gth 5 45%) results in a 9.75-m plasma, with 14 MA of plasma current and 8.75-T toroidal field. Both of these configurations have assumed an H/CD wall-plug efficiency of 0.4, a miscellaneous subsystems electric power requirement of 32 MW, and a pumping power requirement of *1% of the total thermal power. The peak heat flux in the divertor has employed a power scrape-off width formulation, in combination with an assumption of 90% radiated power in the divertor, which has led to larger device size, particularly compared with the previous ARIES-AT and ARIES-I design points. Detailed analysis of the edge and divertor plasma provides some support for this high-radiation power handling regime. The increased size has reduced the neutron wall loading compared with previous studies as well, allowing a 5-FPY lifetime for the ACT1 first wall and blanket and an 8-FPY lifetime for the ACT2 first wall. Both configurations utilize Li15.7Pb84.3 as liquid-metal breeder/coolant, with 40%[6] Li enrichment, reaching TBRs of 1.05. The He-cooled tungsten alloy with tungsten armor is the divertor concept for both. An up-down symmetric double-null geometry with strong shaping is also common to these configurations. 

TABLE VI 

Selected Parameters from ARIES-I, Compared with ARIES-ACT4 and ACT2 

*These parameters are generated from the present systems code to recover the ARIES-I design point, so that some of them are slightly different because of the different models. 

The ACT activity simultaneously improved and expanded the analysis approaches in both engineering and physics. Engineering activities expanded with the use of inelastic analysis on critical components such as the blanket and divertor structures, fracture analysis on the brittle tungsten components, transient analysis of ELMtype heat loading on the divertor, and electromagnetic disruption analysis of conducting structures during the current quench. The nuclear analysis has developed routine examination of 3-D CAD-based first wall, blanket, structural ring/shield, vacuum vessel, and divertor regions. The combination of similarity experiments for the highheat-flux He-tungsten divertor designs with detailed thermomechanical and computational fluid dynamics analysis was used to provide the basis for the ACT divertor designs. The physics analysis utilized timedependent free-boundary plasma simulations, with highfidelity H/CD models. Ideal MHD is expanded to include the peeling-ballooning pedestal stability and fast-alphaparticle stability. Two-dimensional edge and divertor plasma modeling with fluid and kinetic neutrals was employed to find solutions to the high power handling for ACT1. Experimental observations were used to determine the ELM and disruption thermal loading of the divertor and first wall to provide engineering analysis with some 

guidance and begin to establish power plant regime limitations for these phenomena. 

A new database systems analysis approach was employed in the ACT studies, in which a large database of viable operating points was produced, rather than a single optimized operating point based on COE, as was done previously in the ARIES studies. The new approach confirmed the expectation that there are many nearby operating points with only slightly different COEs, which exhibit variations in both plasma and engineering parameters. The conclusion is that within the uncertainty inherent in our present knowledge of achievable parameters in a fusion power plant, such as maximum toroidal field at the TF coil or maximum bN achievable, we can actually only determine a range of solutions that meet our technical criteria within a COE zone. This range allows us to see the impact of more or less aggressive assumptions. This is considered a preferable and more credible way to describe power plant visions for the future. 

## VI.A. Research and Development Needs 

The ARIES-ACT study of tokamak power plants recognizes that there are several areas that require research for these power plant configurations to be realized, and 

VOL. 67 JAN. 2015 

FUSION SCIENCE AND TECHNOLOGY 

many of these are well known and the subject of active research worldwide. Some of the newer, or underappreciated, observations are summarized here. Greater detail and motivation for many of these R&D needs can be found in the accompanying papers in this issue.[2–11] 

For the lower-bN operating space examined in ACT2, it appears that the no-wall beta limit is lower than typically assumed, 2.45 versus 3.0 to 3.5, and that access to *25% over the no-wall limit is attractive for the power plant configuration, reducing its major radius by 1 m while leaving most other parameters unchanged. This level above the no-wall beta limit is obtained on present tokamak experiments, and it is necessary to understand how the experimental regimes can be realized and sustained in steady state within the restrictions of power plants (error fields, location of feedback coils, need for nearby conductors, minimal external rotation source, and the plasma response to 3-D magnetic fields). 

The combination of targeting 100% noninductive plasma current, lower-bN operating space, and reduced wall-plug efficiencies for the H/CD (among other things) has driven the plasma edge safety factor to higher values, up to 8 in ACT2, compared with the common advanced tokamak regime on experiments in the range of 4 to 6. These types of plasmas are not routinely examined but can be accessed with lower-plasma-current operation. Understanding the operating features of these plasmas would be of interest to better project their behavior and potential for fusion power production. 

The highly radiating divertor regime is critical to the power handling for these power plants, and the validation of the simulation predictions with similar divertor geometric features (ITER-like strong target tilt or a wide slot with perpendicular target) and particle control would provide a more sound basis for projecting to nextstep facilities or would point to the need for drastically different divertor approaches. As part of this research, the simultaneous operation of high-performance core plasma with a strongly radiating divertor is needed, together with continued validation of divertor plasma/neutral models used for design. 

Operation at or near the Greenwald density is a common operating condition in power plant design studies. Tokamak experiments have exceeded this limit by 40% while maintaining reasonable, although degraded, confinement, but this is not a common operating regime. The present understanding is that the density limit is actually a pedestal density limit, that density peaking can provide n w nGr, and that access to this regime is more easily produced with core fueling than with edge fueling. However, experimentally, this regime is difficult to prototype routinely because of its impact on H/CD, its need for stringent particle control, and the limited ability of present experiments to simultaneously produce the combination of high temperature and high density typical of ITER or power plant plasmas. 

It is found that the energy release per ELM must be reduced by a factor w10 to avoid melting of a tungstenarmored divertor, with the precise level determined by the inter-ELM heat flux. The elimination of ELM-like transients may be required even if the magnitude of the energy release can be reduced significantly, since a power plant will operate for *1 year between routine maintenances and can accumulate w100 million ELMs. The impact of such high cycling and crack evolution should be understood to provide design guidance for the divertor and first-wall lifetimes. 

It is clear that for tokamaks, disruptions must be avoided, and preferably eliminated. However, in the unlikely event of such an off-normal condition, disruption mitigation is necessary to avoid a large fraction of the core plasma energy ending up on the divertors and to eliminate the production of runaway electrons. In experiments, the halo currents are reduced in magnitude as well. The electromagnetic impact of the plasma current quench remains with disruption mitigation, and the structural design of the plant must be capable of handling these loads. Simulations indicate that the layout and design of the components (vacuum vessel, ring structure, tungsten stabilizer plates, and first wall and blanket structures) in power plants may be able to tolerate these loads. However, the thermal quench in a mitigated disruption transfers the core plasma energy to the RAFM steel of the first wall, which is possibly protected locally by tungsten armor. The thermal response of a bare first wall may not be adequate for such a load, and the need for a special armor and its performance requires further analysis. 

The particle transport in the core plasma and in the SOL is poorly understood, in spite of its tremendous impact on burning plasmas, power handling in the divertor, and plasma-material interactions. Although there are several issues associated with particle behavior, the tritium fuel burnup remains a difficult parameter to accurately predict. A generous value of 10% (ITER has projected v1%) would require that *10 times the amount of tritium consumed to generate fusion power, and bred in the blanket to replace it, is being injected and exhausted from the plasma chamber. Such large tritium inventories moving through the fusion core, processing, and fueling systems should be minimized, and better predictions for the particle behavior are needed. 

The small scrape-off power widths predicted (millimeters) recently have strongly affected the power plant operating points in the ACT study, resulting in larger major radii than predicted 15 to 25 years ago,[26,28,79] when these widths were thought to be relatively large (centimeters). A specific formulation was used in the ACT studies to derive self-consistent results; however, the accurate projection of this parameter is an active area of research. It was required to radiate *75% to 90% of the power entering the divertor to meet steady-state peak heat flux limits. Better quantification both of this parameter 

and its dependences and of the impact of radiating divertor regimes on this power exhaust channel is needed. 

The materials challenges of fusion power plant design continue to pervade all aspects of plasma-material and fusion nuclear science. Development of RAFM steel and extensions of new alloys to higher operating temperature and greater radiation resistance require testing with a fusion-relevant neutron source (especially the impact of higher He generation) to provide the needed database and lifetime projections. SiC composites have still not reached the properties required for a structural material, in spite of significant developments and excellent nonnuclear and fission-irradiated performance. For nonstructural functions, such as flow channel inserts (in the core) or heat exchanger tubing (out of the core), SiC composite is a strong candidate. Tungsten and its alloys are the primary candidates for plasma-facing material, both in the divertor (armor and structural) and in some form for the first wall (armor). The nonnuclear properties of tungsten are not sufficiently well established, and the understanding of the impact of alloying for modifying its properties is very immature. The nuclear performance of tungsten in a fusion-typical neutron spectrum is also poorly understood. Although the liquid metal Li15.7Pb84.3 is considered the primary breeder option because of its flexibility and control, the eutectic’s properties of constituency and evolution in prototypical environments (magnetic field, flow rates, heat and mass transfer, with hydrogen and helium production, and in thermal cycles) are not known. The complex thermofluid behavior requires better experimental demonstration, and simulation capability must improve. 

While a better understanding of the behavior of individual materials under the influence of neutron irradiation is essential for the design and licensing of fusion power plants, it is not sufficient. To ensure safe operation of in-vessel components, we must develop predictive capability and validate component mechanical behavior under the complex environmental conditions anticipated in a fusion reactor, considering the full range of loading conditions from fabrication through heat-up and operation, including warm and cold shutdowns, power excursions, and plasma transients. Low or diminished ductility (due to neutron irradiation) is expected in several candidate materials, requiring additional effort in the development of design rules. Greatly expanded activity in this area is needed to license fusion power plants, ensure their safe operation, and predict the reliability and operating lifetime of components. Similarly, the manufacturing of these fusion core materials can require complex steps or processes that are difficult to scale up to industrial levels. Continued and further efforts in the area of material candidates with an emphasis on large-scale manufacturing are needed. 

Recognizing the range of environmental variables in the fusion core (inside and including the vacuum vessel), including neutron irradiation flux and spectrum, 

temperature, stress, magnetic field, matrix hydrogen and helium content, and corrosion/interactions, offers the potential to optimize materials to be used outside the first wall for their particular function and associated environmental features, as opposed to using materials largely developed for the first wall 14-MeV neutron flux. In the ACT study, the use of bainitic steel for the vacuum vessel was a first attempt at taking this approach. Careful design and detailed neutronics studies are required to confirm radiation damage and transmutation at locations far from the first wall (such as the vacuum vessel), and considering neutron streaming is particularly critical, to take the most advantage of less specialized and potentially more easily fabricated materials. Ultimately, the qualification of such structures could be performed without a fusion-relevant neutron source. 

Significantly better quantification of the plasmafacing loads for the design of the in-vessel components is needed, since the combined surface heat flux, particle flux, and possible transient or off-normal loading, with the volumetric neutron heating and damage, can provide a prohibitively difficult boundary condition on plasmafacing components. Accompanying this are the effects of erosion, the redeposition of eroded material with a different microstructure, and other fundamental changes to the morphology of the material surfaces. 

Power plant design must address the resolution of neutron streaming and special neutron shielding (H/CD ports) possibilities to properly account for the material impacts (high dpa or appm He in lifetime components) and design limitations. Already, analysis shows that relatively small assembly gaps (v2 cm) can significantly increase the neutron effects in structures far from the plasma. 

The lower-beta regime takes advantage of higher toroidal field to maintain the fusion power, and in some cases the peak field at the superconducting TF coil and its overall current density exceed those projected for ITER TF and central solenoid coils, 11.8 and 13 T, respectively. The further development of the ITER low-temperature superconducting cable-in-conduit conductor design to enable higher fields and current densities should be pursued for next-step fusion facilities. 

The H/CD systems are critical to the success of a steady-state power plant solution, since they provide the plasma current not provided by the bootstrap current. The efficiencies of these systems and the current drive efficiencies in the plasma give rise to a significant recirculating power in the plant power balance. Each source (EC, NB, LH, ICRF) has been demonstrated on existing tokamak experiments, and each has a range of performance achievements. Improvements in the wallplug efficiencies (source and transmission, and including coupling for LH and ICRF) are needed to reduce this recirculating power. ITER will provide important information on these sources at the tens-of-megawatts 

level, including their wall-plug and coupling efficiencies and their reliabilities. The development of these sources for the stronger fusion neutron environment and ultralongduration operation must include constructing components with fusion-relevant materials and operating at high blanket temperatures where applicable. Ultimately, the success of one source over another can change the solution space for power plants. Some recent assessments and approaches to improving these systems can be found in Refs. 81, 82, and 83. 

High thermal conversion efficiencies are important for fusion power plants to utilize the heat generated efficiently and compensate for recirculating power requirements. The high-temperature operation of the blanket and divertor requires demonstration, and the detailed development of the balance of plant components associated with a closed He Brayton cycle requires development and demonstration. References 84 and 85 examine the Brayton cycle technical aspects; however, since these systems are not common in industrial power production, they need more attention to guarantee their reliable operation at a DEMO-stage facility. 

11. C. E. KESSEL and F. M. POLI, Fusion Sci. Technol., 67, 220 (2015); http://dx.doi.org/10.13182/FST14-793. 

12. H. ZOHM et al., Nucl. Fusion, 53, 073019 (2013); http:// dx.doi.org/10.1088/0029-5515/53/7/073019. 

13. K. KIM et al., ‘‘A Preliminary Conceptual Design Study for Korean Fusion DEMO Reactor Magnet,’’ Proc. 25th IEEE Symp. Fusion Engineering (SOFE), San Francisco, California, June 10–14, 2013, IEEE (2013). 

14. L. BROMBERG et al., Fusion Eng. Des., 38, 159 (1997); http://dx.doi.org/10.1016/S0920-3796(97)00115-4. 

15. M. THUMM, IEEE Trans. Plasma Sci., 42, 590 (2014); http://dx.doi.org/10.1109/TPS.2013.2284026. 

16. T. IDEHARA and S. P. SABCHEVSKI, J. Infrared Millimeter Terahertz Waves, 33, 667 (2012); http://dx.doi.org/ 10.1007/s10762-011-9862-x. 

17. M. GREENWALD et al., Nucl. Fusion, 28, 2199 (1988); http://dx.doi.org/10.1088/0029-5515/28/12/009. 

18. J. ONGENA et al., Phys. Plasmas, 8, 2188 (2001); http:// dx.doi.org/10.1063/1.1364513. 

19. M. A. MAHDAVI et al., Nucl. Fusion, 42, 52 (2002); http://dx.doi.org/10.1088/0029-5515/42/1/308. 

## ACKNOWLEDGMENTS 

This work is partially supported by the U.S. Department of EnergycontractsDE-AC02-76CH03073,DE-AC52-07NA27344, and DE-FC02-04ER54698. 

## REFERENCES 

1. F. NAJMABADI et al., Fusion Eng. Des., 80, 3 (2006); http://dx.doi.org/10.1016/j.fusengdes.2005.11.003. 

2. M. S. TILLACK et al., Fusion Sci. Technol., 67, 49 (2015); http://dx.doi.org/10.13182/FST14-790. 

3. C. E. KESSEL et al., Fusion Sci. Technol., 67, 75 (2015); http://dx.doi.org/10.13182/FST14-795. 

20. V. V. ALIKAEV et al., Plasma Phys. Rep., 26, 991 (2000); http://dx.doi.org/10.1134/1.1331134. 

21. G. MANK et al., Phys. Rev. Lett., 85, 2312 (2000); http:// dx.doi.org/10.1103/PhysRevLett.85.2312. 

22. G. SAIBENE et al., Plasma Phys. Controlled Fusion, 44, 1769 (2002); http://dx.doi.org/10.1088/0741-3335/44/9/301. 

23. A. MESSIAEN et al., Nucl. Fusion, 50, 025026 (2010); http://dx.doi.org/10.1088/0029-5515/50/2/025026. 

24. A. EKEDAHL et al., Nucl. Fusion, 45, 351 (2005); http:// dx.doi.org/10.1088/0029-5515/45/5/005. 

25. M.-L. MAYORAL et al., AIP Conf. Proc., 933, 55 (2007); http://dx.doi.org/10.1063/1.2800548. 

26. R. W. CONN et al., Nucl. Fusion Suppl., 3, 659 (1991). 

4. X. R. WANG et al., Fusion Sci. Technol., 67, 22 (2015); http://dx.doi.org/10.13182/FST14-797. 

5. M. YODA et al., Fusion Sci. Technol., 67, 142 (2015); http://dx.doi.org/10.13182/FST14-792. 

6. J. P. BLANCHARD and C. J. MARTIN, Fusion Sci. Technol., 67, 158 (2015); http://dx.doi.org/10.13182/FST14-796. 

7. M. E. RENSINK and T. D. ROGNLIEN, Fusion Sci. Technol., 67, 125 (2015); http://dx.doi.org/10.13182/FST14-800. 

8. P. W. HUMRICKHOUSE and B. J. MERRILL, Fusion Sci. Technol., 67, 167 (2015); http://dx.doi.org/10.13182/FST14-799. 

9. L. EL-GUEBALY and L. MYNSBURGE, Fusion Sci. Technol., 67, 107 (2015); http://dx.doi.org/10.13182/FST14-791. 

10. X. R. WANG et al., Fusion Sci. Technol., 67, 193 (2015); http://dx.doi.org/10.13182/FST14-798. 

27. C. G. BATHKE and ARIES TEAM, Fusion Eng. Des., 38, 59 (1997); http://dx.doi.org/10.1016/S0920-3796(97)00112-9. 

28. F. NAJMABADI et al., Fusion Eng. Des., 80, 3 (2006); http://dx.doi.org/10.1016/j.fusengdes.2005.11.003. 

29. C. E. KESSEL et al., Fusion Eng. Des., 80, 63 (2006); http://dx.doi.org/10.1016/j.fusengdes.2005.06.350. 

30. C. M. GREENFIELD et al., Plasma Phys. Controlled Fusion, 46, B213 (2004); http://dx.doi.org/10.1088/0741-3335/ 46/12B/019. 

31. M. E. FENSTERMACHER et al., ‘‘Effect of Variation in Equilibrium Shape on ELMing H-Mode Performance in DIII-D Diverted Plasmas,’’ Proc. 18th IAEA Fusion Energy Conf., Sorrento, Italy, October 4–10, 2000; http://www-pub.iaea.org/ MTCD/publications/PDF/csp_008c/html/node67.htm (current as of Mar. 3, 2014). 

32. N. OYAMA et al., Plasma Phys. Controlled Fusion, 48, A171 (2006); http://dx.doi.org/10.1088/0741-3335/48/5A/S16. 

33. C. E. KESSEL et al., Nucl. Fusion, 41, 953 (2001); http:// dx.doi.org/10.1088/0029-5515/41/7/316. 

34. T. EICH et al., J. Nucl. Mater., 438, S72 (2013); http:// dx.doi.org/10.1016/j.jnucmat.2013.01.011. 

35. J. A. CROMWELL et al., Fusion Eng. Des., 27, 515 (1995); http://dx.doi.org/10.1016/0920-3796(95)90166-3. 

36. N. MITCHELL et al., IEEE Trans. Appl. Supercond., 22, 4200809 (2012); http://dx.doi.org/10.1109/TASC.2011.2174560. 

37. V. PHILIPPS, J. Nucl. Mater., 415, S2 (2011); http:// dx.doi.org/10.1016/j.jnucmat.2011.01.110. 

38. S. SMOLENTSEV et al., Fusion Eng. Des., 85, 1196 (2010); http://dx.doi.org/10.1016/j.fusengdes.2010.02.038. 

39. D. STORK, ‘‘Technical Challenges on the Path to DEMO,’’ presented at Int. Mtg. MFE Roadmapping in the ITER Era, Princeton Plasma Physics Laboratory, September 7–10, 2011; http://advprojects.pppl.gov/ROADMAPPING/presentations.asp (current as of Oct. 10, 2014). 

40. D. STORK, ‘‘DEMO and the Route to Fusion Power,’’ presented at 3rd Karlsruhe School Fusion Technology, Karlsruhe, Germany, September 2009; http://fire.pppl.gov/eu_ demo_Stork_FZK%20.pdf (current as of Oct. 10, 2014). 

41. P. THOMAS, ‘‘Heating and Current Drive Systems, Their Impact on Scenario/Economics (Lessons Learned from ITER Design),’’ presented at 2nd IAEA DEMO Workshop, Vienna, Austria, December 2013; http://www-naweb.iaea.org/napc/ physics/meetings/TM45256/talks/Thomas.pdf. 

42. J. A. SNIPES et al., ‘‘Multi-Machine Global Confinement and H-Mode Threshold Analysis,’’ Proc. 2002 IAEA Fusion Energy Conf., Lyon, France, October 14–19, 2002; http://wwwpub.iaea.org/MTCD/Publications/PDF/csp_019c/html/node166. htm (current as of Mar. 3, 2014). 

43. C. ANGIONI et al., Plasma Phys. Controlled Fusion, 51, 124017 (2009); http://dx.doi.org/10.1088/0741-3335/51/12/ 124017. 

44. W. FUNDAMENSKI et al., Nucl. Fusion, 45, 950 (2005); http://dx.doi.org/10.1088/0029-5515/45/8/024. 

45. W. M. TANG, Nucl. Fusion, 26, 1605 (1986); http:// dx.doi.org/10.1088/0029-5515/26/12/003. 

46. C. E. KESSEL et al., Nucl. Fusion, 47, 1274 (2007); http:// dx.doi.org/10.1088/0029-5515/47/9/026. 

47. P. B. SNYDER et al., Nucl. Fusion, 51, 103016 (2011); http://dx.doi.org/10.1088/0029-5515/51/10/103016. 

48. M. BRAMBILLA, Plasma Phys. Controlled Fusion, 41, 1 (1999); http://dx.doi.org/10.1088/0741-3335/41/1/002. 

49. D. W. IGNAT et al., Nucl. Fusion, 34, 837 (1994); http:// dx.doi.org/10.1088/0029-5515/34/6/I07. 

50. R. W. HARVEY and M. G. McCOY, ‘‘The CQL3D Fokker-Planck Code,’’ Proc. IAEA Technical Committee Advances in Simulation and Modeling of Thermonuclear Plasmas, Montreal, Quebec, Canada, June 15–18, 1992, 

USDOC/NTIS Doc. DE93002962, p. 489, U.S. Department of Energy (1993). 

51. A. SMIRNOV, R. W. HARVEY, and R. PRATER, ‘‘General Linear RF-Current Drive Calculation in Toroidal Plasma,’’ Proc. 15th Joint Workshop Electron Cyclotron Emission and Electron Cyclotron Resonance Heating, Yosemite National Park, California, March 10–13, 2008, p. 301, World Scientific (2009). 

52. T. D. ROGNLIEN and M. E. RENSINK, Fusion Eng. Des., 60, 497 (2002); http://dx.doi.org/10.1016/S0920-3796(02)00005-4. 

53. D. STOTLER and C. KARNEY, Contrib. Plasma Phys., 34, 392 (1994); http://dx.doi.org/10.1002/ctpp.2150340246. 

54. R. J. GOLDSTON et al., J. Comput. Phys, 43, 61 (1981); http://dx.doi.org/10.1016/0021-9991(81)90111-X. 

55. A. H. KRITZ et al., ‘‘Heating in Toroidal Plasmas,’’ Proc. 3rd Joint Varenna-Grenoble Int. Symp., Grenoble, 1982, Vol. 2, p. 707, CEC (1982). 

56. Y. R. LIN-LIU et al., Phys. Plasmas, 10, 4064 (2003); http://dx.doi.org/10.1063/1.1610472. 

57. S. MALANG et al., Fusion Eng. Des., 41, 377 (1998); http://dx.doi.org/10.1016/S0920-3796(98)00121-5. 

58. L. M. WAGANER et al., Fusion Eng. Des., 80, 181 (2006); http://dx.doi.org/10.1016/j.fusengdes.2005.06.353. 

59. K. TOBITA et al., Fusion Eng. Des., 86, 2730 (2011); http://dx.doi.org/10.1016/j.fusengdes.2011.03.022. 

60. M. S. TILLACK et al., Fusion Eng. Des., 86, 71 (2011); http://dx.doi.org/10.1016/j.fusengdes.2010.08.015. 

61. X. R. WANG et al., Fusion Eng. Des., 87, 732 (2012); http://dx.doi.org/10.1016/j.fusengdes.2012.02.012. 

62. X. R. WANG et al., Fusion Sci. Technol., 60, 218 (2011); http://dx.doi.org/10.13182/FST10-237. 

63. R. E. NYGREN et al., J. Nucl. Mater., 417, 451 (2011); http://dx.doi.org/10.1016/j.jnucmat.2010.12.289. 

64. S. WURSTER et al., J. Nucl. Mater., 442, S181 (2013); http://dx.doi.org/10.1016/j.jnucmat.2013.02.074. 

65. D. NAVAEI et al., Fusion Sci. Technol., 60, 233 (2011); http://dx.doi.org/10.13182/FST10-221. 

66. J. RADER et al., Fusion Sci. Technol., 64, 282 (2013); http://dx.doi.org/10.13182/FST12-544. 

67. H. H. TOUDESHKI et al., Fusion Sci. Technol., 64, 675 (2013); http://dx.doi.org/10.13182/FST12-550. 

68. N. KOMAI et al., ‘‘Development and Application of 2.25Cr-1.6W (HCM2S) Steel Large Diameter and Thick Section Pipe,’’ Advanced Heat Resistant Steels for Power Generation, p. 96, R. VISWANATHAN and J. NUTTING, Eds., Maney (1999). 

69. R. L. KLUEH et al., Int. J. Press. Vessels Pip., 84, 29 (2007); http://dx.doi.org/10.1016/j.ijpvp.2006.09.004. 

70. R. SCHLEICHER et al., Fusion Technol., 39, 823 (2001). 

71. S. A. WRIGHT, M. E. VERNON, and P. S. PICKARD, ‘‘Concept Design for a High Temperature Helium Brayton Cycle with Interstage Heating and Cooling,’’ SAND2006-4147, Sandia National Laboratories (July 2006); http://nuclear.inl.gov/ deliverables/docs/genivihc_2006_milestone_report_7_1_2006_ final.pdf (current as of Mar. 3, 2014). 

72. Q. HUANG et al., J. Nucl. Mater., 442, S2 (2013); http:// dx.doi.org/10.1016/j.jnucmat.2012.12.039. 

73. A. R. RAFFRAY et al., Fusion Eng. Des., 55, 55 (2001); http://dx.doi.org/10.1016/S0920-3796(01)00181-8. 

74. L. EL-GUEBALY et al., Fusion Sci. Technol., 64, 449 (2013); http://dx.doi.org/10.13182/FST12-523. 

75. E. GAGANIDZE and J. AKTAA, Fusion Eng. Des., 88, 118 (2013); http://dx.doi.org/10.1016/j.fusengdes.2012.11.020. 

76. L. L. SNEAD et al., J. Nucl. Mater., 417, 330 (2011); http://dx.doi.org/10.1016/j.jnucmat.2011.03.005. 

77. G. FEDERICI et al., Fusion Eng. Des., 89, 882 (2014); http://dx.doi.org/10.1016/j.fusengdes.2014.01.070. 

78. Z. DRAGOJLOVIC et al., Fusion Eng. Des., 85, 243 (2010); http://dx.doi.org/10.1016/j.fusengdes.2010.02.015. 

79. L. C. CARLSON et al., Fusion Sci. Technol., 60, 459 (2011); http://dx.doi.org/10.13182/FST10-252. 

80. A. LOARTE et al., J. Nucl. Mater., 266–269, 587 (1999); http://dx.doi.org/10.1016/S0022-3115(98)00590-X. 

81. J. PAMELA et al., Fusion Eng. Des., 84, 194 (2009); http:// dx.doi.org/10.1016/j.fusengdes.2009.02.028. 

82. E. SURREY et al., Fusion Eng. Des., 87, 373 (2012); http:// dx.doi.org/10.1016/j.fusengdes.2012.03.028. 

83. R. McADAMS et al., Rev. Sci. Instrum., 85, 02B319 (2014); http://dx.doi.org/10.1063/1.4852299. 

84. S. MALANG et al., Fusion Eng. Des., 41, 561 (1998); http://dx.doi.org/10.1016/S0920-3796(98)00220-8. 

85. R. SCHLEICHER et al., Fusion Tech., 39, 823 (2001). 

