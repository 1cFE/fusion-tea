---
source: "https://lasers.llnl.gov/sites/lasers/files/2023-11/fuerst-idaho-IFE-workshop-2022.pdf"
source_type: "url"
extracted_at: "2026-04-20T18:05:06.576729+00:00"
content_hash_sha256: "6d5ce601333d8fa3b6caf6c7241da888b933f5799513958dbe25861fbc3a3aa7"
backend: "pdf_pipeline"
---

## **Efficient tritium extraction from PbLi: a potential IFE breeding material** 

T.F. Fuerst, C.N. Taylor, and M. Shimada 

_Fusion Safety Program, Idaho National Laboratory, Idaho Falls, ID 83415_ 

Email of corresponding author: thomas.fuerst@inl.gov 

Topical Area: Fuel Cycle 

## **Executive Summary** 

Tritium generation in the breeder blanket is a necessity for any inertial fusion energy (IFE) reactor based on deuterium-tritium fusion. Both solid and liquid breeders have been considered in IFE designs, but preference is given to pure Li due to its favorable thermophysical properties and compatibility with structural materials. However, pure Li poses as a significant safety hazard due to its propensity for severe exothermic reaction with air and water. Magnetic fusion energy (MFE) designs focus on PbLi to mitigate this hazard, but its low tritium solubility leads to higher permeation losses through piping components when compared to pure Li. Efficient tritium extraction upstream from the heat exchanger mitigates this concern and is enabled by vacuum permeator technology. Idaho National Laboratory (INL) is constructing the Tritium Extraction eXperiment (TEX), a forced-convection PbLi loop designed to evaluate the vacuum permeator technology and validate design codes. This test stand and information gained can be used to design and test vacuum permeators specifically tailored to IFE systems to achieve desired extraction efficiencies at specified temperatures and flow rates. 

## **Introduction** 

The deuterium-tritium fusion reaction provides the highest cross section at the lowest centerof-mass energy and is the favored fuel for inertial fusion energy (IFE). Deuterium is routinely enriched from water due to its natural abundance of 0.0156%. However, tritium is not a naturally abundant natural resource. Man-made tritium currently is produced in heavy water moderated reactors (HWR), such as the CANDU (CANadian Deuterium Uranium) reactor, and in tritiumproducing burnable absorption rods (TPBAR) irradiated in conventional fission reactors. Not all HWRs employ detritiation facilities for harvesting tritium. The current commercial world inventory was estimated in 2018 to be around 30–40 kg [1], and approximately 5.5% is lost annually due to radioactive decay. It is estimated that a 2.2 GWth IFE fusion reactor will require around 0.366 kg of tritium per day of operation [2]. With the fleet of CANDU reactors eventually reaching end of life around 2055, the projection of available tritium for any confinement type demonstration plant startup is uncertain [3]. While it is technically possible to produce unconstrained amounts of tritium through fission reactors, economic and political considerations make this implausible. Fusion reactors must therefore produce the tritium required for operation. 

## **Blanket Concepts** 

Nearly all tritium breeder blanket concepts to date rely on the nuclear conversion of lithium to tritium. The possible nuclear reactions are shown in Table 1. Nominally all breeder concepts will enrich the concentration of[6] Li from 7.59% natural abundance to ~80%, due to the significantly higher reaction cross section and favorable tritium production of[6] Li [4]. Neutron multipliers are also needed to increase the tritium breeding ratio of a blanket system. The most considered multipliers include beryllium and lead according to reactions in Table 1. 

Table 1. Tritium breeding reactions and relevant neutron multiplication reactions [4]. 

Potential tritium breeders are broadly classified as solid breeders or liquid breeders. Each have advantages and disadvantages. Solid breeders are typically envisioned as ceramic pebbles of Li2TiO3 or Li4SiO4 less than 1 mm diameter [5]; novel conceptions propose a 90% dense reverse ceramic foam with a continuous internal pore network [6]. In all solid breeder concepts, tritium diffuses out of the ceramic, is carried away by a helium sweep gas, and the tritium is harvested in a tritium extraction system. Liquid breeder materials have primarily included pure lithium, PbLi eutectic (17 at% Li), fluoride molten salt (FLiBe). Liquid breeders have several advantages over solid breeders. Liquids are not susceptible to neutron-induced mechanical damage as are all solid breeders. They operate in a flowing system and therefore can be continuously processed and replenished, as opposed to solid breeders, which would require batch replacement and processing. Because the lithium-6 content can be adjusted continuously, a constant tritium breeding ratio can be maintained. 

Each of the candidate liquid breeders (Li, PbLi, and FLiBe) have associated pros and cons. Table 2 highlights the thermophysical properties of these candidate liquid breeders. Pure lithium has good corrosion compatibility with structural materials and high tritium solubility which reduces tritium loss terms through the contacting metals. However, the high tritium solubility yields greater difficulty in extraction, and lithium reacts violently with air and water, posing a significant safety hazard that must be mitigated. FLiBe has a low electrical conductivity which eliminates concerns with magnetohydrodynamic pressure drop (a greater concern for MFE designs due to the presence of strong magnetic fields) and high heat capacity. However, FLiBe has a high melting point and contains Be, which while acting as a neutron multiplier, poses a health safety concern. PbLi has a low melting point, low viscosity, and a much lower chemical reactivity when compared to pure Li – reacting with only water at high temperature rather than both water and air. However, PbLi has a high density and corrosion issues with structural steels. It also has a low tritium solubility which enables easier extraction, as discussed subsequently, but can lead to excessive tritium permeation through materials. 

Various candidate tritium breeder materials have been considered in the US-based IFE design studies, but the focus is predominately on Li and FLiBe. In the 1980s researchers at Lawrence Livermore National Laboratory (LLNL) designed the first generation of the High‐Yield Lithium‐ Injection Fusion‐Energy (HYLIFE) reactor with liquid Li walls to protected chamber structural 

materials, bred tritium, and extract heat [7]. In the 1990s, the revised design, coined HYLIFE-II, replaced the liquid Li with FLiBe to reduce the fire hazard [8]. In the 2000s, LLNL researchers designed the Laser Inertial Fusion Energy (LIFE) engine where liquid Li was again selected as a coolant and breeder, but the design uses metallic tubes as the first wall material with Li flowing internally and in the trapezoidal “skin cooled” blanket [9].  An industry led design study sponsored by the Department of Energy Fusion Energy Sciences (DOE-FES) resulted in the heavy ion beam driven ORISIS with a FLiBe blanket and the laser driven SOMBRERO with solid Li2O breeder [10]. No US-based IFE designs have implemented PbLi as a breeding material, whereas PbLi is a favored MFE breeding material as highlighted by its inclusion in two ITER Test Blanket Module (TBM) programs. Europe and India are pursuing PbLi blankets as part of the ITER project, as outlined in Table 3 [11]. Note that in 2012 the US became an observer in the ITER TBM program, but planned to test a PbLi-based Dual Coolant Lead Lithium (DCLL) blanket [12]. 

Table 2. Summary of liquid breeder thermophysical properties with Li and PbLi taken from [13], FLiBe taken from [14], and tritium solubility for Li, Pb-17Li, and FLiBe from [15–17], respectively. 

Table 3. Current plans for ITER breeder blanket modules. 

## **Tritium Extraction from PbLi** 

A main concern with the use of salt (FLiBe) or liquid metal (PbLi) tritium breeding materials is the low tritium solubility drives permeation through structural materials and into secondary heat transfer fluids leading to unintentional release [2]. However, this can be addressed by placing the tritium extraction system (TES) in the hot leg of the heat transfer loop upstream of the heat exchanger as shown in Figure 1A. Tritium transport analysis for the Fusion Nuclear Science Facility (FNSF) DCLL blanket concluded that highly efficient tritium extraction reduces the tritium permeation loss rates through the primary piping [18]. However, this design requires a 

TES with high efficiency, low pressure drop, minimal thermal losses, and low capital and operating costs. 

One promising TES method for PbLi is the vacuum permeator [19]. The vacuum permeator operates via tritium permeation through a high-permeability dense-metal membrane, where a concentration gradient is established between the tritium rich PbLi on one surface of the membrane and vacuum on the other membrane surface. This simple method extracts the tritium without need for further gas separation, operates at high temperature, and can be designed to balance maximizing extraction efficiency while minimizing pressure drop. While other technologies also exist such as gas-liquid contactors, vacuum-sieve trays, and regenerable getters; vacuum permeators continue to be the preferred extraction method based on system analysis [20]. 

The vacuum permeator is also simpler than the current favored method for tritium extraction from pure Li that uses the Maroni process (Figure 1B), which was selected for use in the LIFE engine design [2,9,21]. The Maroni process [22] consist of mixing the Li containing tritium and molten Li halides salts, extracting the LiT into the halide salt, and separating the Li and the salt in a centrifugal contactor. Then the tritium containing salt is circulated to an electrolyzer, the LiT is oxidized to form T2 which is swept from the salt by sparging with Ar or He, and finally the T2 is collected on a getter material. Note that Savannah River National Laboratory (SRNL) is currently developing Li-conductor technology as an electrochemical extraction method with the goal of simplifying tritium extraction from pure Li [23]. 

![](knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/lasers-sites-lasers-files-2023-11-fuerst-idaho-ife-workshop/tmp8w4yk1vt/images/tmp8w4yk1vt.pdf-0004-04.png)

Figure 1. (A) A schematic of the primary components of the FNSF core and primary and secondary heat transfer systems. The vacuum permeator tritium extraction system in the PbLi hot leg is circled [18]. (B) Tritium extraction concept for LIFE [21]. 

The Fusion Safety Program at Idaho National Laboratory is tasked with testing blanket tritium extraction concepts, including tritium extraction from PbLi using the vacuum permeator, under the DOE-FES Blanket and Fuel Cycle program. The Tritium Extraction eXperiment is a forced convection PbLi loop currently being assembled at the Safety and Tritium Applied Research (STAR) facility for this purpose [24]. The loop is designed to be a versatile testbed to validate permeator modeling, test a wide range of permeator concepts, and examine the effects of permeator length/diameter, PbLi flow rate, temperature, and tritium concentration on tritium extraction efficiency. The loop is designed to operate at nominal isothermal temperatures up to 535ºC, and 

an overview of basic operational parameters are summarized in Table 4. An overview schematic of the loop is shown in Figure 2.  The major systems of the loop include the PbLi pump, a reverse permeator, the test section, the analysis chamber, a supply tank, and a plenum. 

The vacuum permeator tritium extraction technology may enable reconsideration of PbLi as a breeding material for IFE concepts as a safer alternative to pure Li. Data from the TEX experiment will be used to inform vacuum permeator designs. This information can be leveraged to design vacuum permeators specific to the IFE flow rate, extraction efficiency, and thermal requirements as well as serve as a testbed for the proposed designs. 

Table 4. Operational parameters for TEX. 

|al parameters for TEX.||
|---|---|
|Parameter|Value|
|Volumetric flow rate|0.5 L/s|
|Mass flow rate|4.7 kg/s|
|Permeator length|1-5 m|
|PbLi velocity in test section|≤ 4.2 m/s|
|PbLi velocity in tubing|≤ 1.3 m/s|
|Temperature|300-535ºC|
|D concentration (mol/m3)|≤ 2 x 10-2|
|Tritium capable|Yes|

![](knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/lasers-sites-lasers-files-2023-11-fuerst-idaho-ife-workshop/tmp8w4yk1vt/images/tmp8w4yk1vt.pdf-0005-05.png)

Figure 2. Current photo of the assembly TEX loop with primary PbLi contacting components installed. Labeled components include: (A) moving magnetic PbLi pump, (B) reverse permeator for hydrogen introduction, (C) vacuum analysis chamber, (D) tube furnace containing versatile test section, and (E) plenum free surface. 

## **References** 

- [1] M. Kovari, M. Coleman, I. Cristescu, R. Smith, Tritium resources available for fusion reactors, Nucl. Fusion. 58 (2017) 026010. https://doi.org/10.1088/1741-4326/aa9d25. 

- [2] S. Reyes, T. Anklam, W. Meier, P. Campbell, D. Babineau, J. Becnel, C. Taylor, J. Coons, Recent developments in IFE safety and tritium research and considerations for future nuclear fusion facilities, Fusion Engineering and Design. 109–111 (2016) 175–181. https://doi.org/10.1016/j.fusengdes.2016.03.034. 

- [3] R.J. Pearson, A.B. Antoniazzi, W.J. Nuttall, Tritium supply and use: a key issue for the development of nuclear fusion energy, Fusion Engineering and Design. 136 (2018) 1140– 1148. https://doi.org/10.1016/j.fusengdes.2018.04.090. 

- [4] M. Rubel, Fusion Neutrons: Tritium Breeding and Impact on Wall Materials and Components of Diagnostic Systems, J Fusion Energ. 38 (2019) 315–329. https://doi.org/10.1007/s10894-018-0182-1. 

- [5] G. Piazza, J. Reimann, E. Günther, R. Knitter, N. Roux, J.D. Lulewicz, Characterisation of ceramic breeder materials for the helium cooled pebble bed blanket, Journal of Nuclear Materials. 307–311 (2002) 811–816. https://doi.org/10.1016/S0022-3115(02)00983-2. 

- [6] S. Sharafat, B. Williams, N. Ghoniem, A. Ghoniem, M. Shimada, A. Ying, Development of a new cellular solid breeder for enhanced tritium production, Fusion Engineering and Design. 109–111 (2016) 119–127. https://doi.org/10.1016/j.fusengdes.2016.03.041. 

- [7] J.A. Blink, W.J. Hogam, J. Hovingh, E.R. Meier, J.H. Pitts, High-Yield Lithium-Injection Fusion-Energy (HYLIFE) reactor, Lawrence Livermore National Lab., CA (USA), 1985. https://doi.org/10.2172/6124368. 

- [8] R.W. Moir, The High‐Yield Lithium‐Injection Fusion‐Energy (HYLIFE)‐II inertial fusion energy (IFE) power plant concept and implications for IFE, Physics of Plasmas. 2 (1995) 2447–2452. https://doi.org/10.1063/1.871269. 

- [9] J.F. Latkowski, R.P. Abbott, S. Aceves, T. Anklam, A.W. Cook, J. DeMuth, L. Divol, B. El-Dasher, J.C. Farmer, D. Flowers, M. Fratoni, T. Heltemes, J. Kane, K.J. Kramer, R. Kramer, A. Lafuente, G.A. Loosmore, K.R. Morris, G.A. Moses, B. Olson, C. Pantano, S. Reyes, M. Rhodes, R. Sawicki, H. Scott, M. Tabak, S. Wilks, Chamber Design for the Laser Inertial Fusion Energy (LIFE) Engine, Fusion Science and Technology. 60 (2011) 54–60. https://doi.org/10.13182/FST10-318. 

- [10] W.R. Meier, R.L. Bieri, M.J. Monsler, C.D. Hendricks, P. Laybourne, K.R. Shillito, OSIRIS and SOMBRERO Inertial Fusion Power Plant Designs, Volume 1: Executive Summary & Overview, W.J. Schafer Associates, Inc. (US), 1992. https://doi.org/10.2172/833813. 

- [11] B.G. Hong, Overview of ITER TBM program objectives and management, International Journal of Energy Research. 42 (2018) 4–8. https://doi.org/10.1002/er.3759. 

- [12] C.P.C. Wong, M. Abdou, M. Dagher, Y. Katoh, R.J. Kurtz, S. Malang, E.P. Marriott, B.J. Merrill, K. Messadek, N.B. Morley, M.E. Sawan, S. Sharafat, S. Smolentsev, D.K. Sze, S. Willms, A. Ying, M.Z. Youssef, An overview of the US DCLL ITER-TBM program, Fusion Engineering and Design. 85 (2010) 1129–1132. https://doi.org/10.1016/j.fusengdes.2010.02.021. 

- [13] S. Malang, R. Mattas, Comparison of lithium and the eutectic lead-lithium alloy, two candidate liquid metal breeder materials for self-cooled blankets, Fusion Engineering and Design. 27 (1995) 399–406. https://doi.org/10.1016/0920-3796(95)90151-5. 

- [14] M.S. Sohal, M.A. Ebner, P. Sabharwall, P. Sharpe, Engineering Database of Liquid Salt Thermophysical and Thermochemical Properties, Idaho National Lab. (INL), Idaho Falls, ID (United States), 2010. https://doi.org/10.2172/980801. 

- [15] E. Veleckis, E.H. Van Deventer, M. Blander, Lithium-lithium hydride system, J. Phys. Chem. 78 (1974) 1933–1940. https://doi.org/10.1021/j100612a013. 

- [16] F. Reiter, Solubility and diffusivity of hydrogen isotopes in liquid Pb17Li, Fusion Engineering and Design. 14 (1991) 207–211. https://doi.org/10.1016/0920-3796(91)900039. 

- [17] P. Calderoni, P. Sharpe, M. Hara, Y. Oya, Measurement of tritium permeation in flibe (2LiF–BeF2), Fusion Engineering and Design. 83 (2008) 1331–1334. https://doi.org/10.1016/j.fusengdes.2008.05.016. 

- [18] P.W. Humrickhouse, B.J. Merrill, Tritium aspects of the fusion nuclear science facility, Fusion Engineering and Design. 135 (2018) 302–313. https://doi.org/10.1016/j.fusengdes.2017.04.099. 

- [19] P.W. Humrickhouse, B.J. Merrill, Vacuum Permeator Analysis for Extraction of Tritium from DCLL Blankets, Fusion Science and Technology. 68 (2015) 295–302. https://doi.org/10.13182/FST14-941. 

- [20] M. Utili, A. Tincani, L. Candido, L. Savoldi, R. Zanino, M. Zucchetti, D. Martelli, A. Venturini, Tritium Extraction From HCLL/WCLL/DCLL PbLi BBs of DEMO and HCLL TBS of ITER, IEEE Transactions on Plasma Science. 47 (2019) 1464–1471. https://doi.org/10.1109/TPS.2018.2886409. 

- [21] S. Reyes, T. Anklam, D. Babineau, J. Becnel, R. Davis, M. Dunne, J. Farmer, D. Flowers, K. Kramer, J. Martinez-Frias, R. Miles, C. Taylor, LIFE Tritium Processing: A Sustainable Solution for Closing the Fusion Fuel Cycle, Fusion Science and Technology. 64 (2013) 187–193. https://doi.org/10.13182/FST12-529. 

- [22] V.A. Maroni, R.D. Wolson, G.E. Staahl, Some Preliminary Considerations of A MoltenSalt Extraction Process to Remove Tritium from Liquid Lithium Fusion Reactor Blankets, Nuclear Technology. 25 (1975) 83–91. https://doi.org/10.13182/NT75-A24351. 

- [23] J.A. Teprovich, H.R. Colon Mercado, L. Olson, P. Ganesan, D. Babineau, B.L. GarciaDiaz, Electrochemical extraction of hydrogen isotopes from Li/LiT mixtures, Fusion Engineering and Design. 139 (2019) 1–6. https://doi.org/10.1016/j.fusengdes.2018.11.018. 

- [24] C.N. Taylor, T.F. Fuerst, P.W. Humrickhouse, R.J. Pawelko, M. Shimada, Conceptual Design for a Blanket Tritium Extraction Test Stand, Fusion Science and Technology. 77 (2021) 829–835. https://doi.org/10.1080/15361055.2021.1880133. 

