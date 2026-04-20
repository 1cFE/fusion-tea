---
source: "https://infoscience.epfl.ch/server/api/core/bitstreams/7d2d7b2f-6f75-4ac2-93cb-6eef8a65df82/content"
source_type: "url"
extracted_at: "2026-04-19T22:43:22.532883+00:00"
content_hash_sha256: "07a813bf8247e640ea5836bef02e03d17c90ba946b088e11b54e386d725713db"
backend: "pdf_pipeline"
---

![](images/tmpaupvkstl.pdf-0001-01.png)

Contents lists available at ScienceDirect 

## Journal of Nuclear Materials 

journal homepage: www.elsevier.com/locate/jnucmat 

![](images/tmpaupvkstl.pdf-0001-05.png)

## Compact fusion blanket using plasma facing liquid Li-LiH walls and Pb pebbles 

![](images/tmpaupvkstl.pdf-0001-07.png)

## Victor Prost[a] _[,]_[∗] , Sabine Ogier-Collin[b] _[,]_[1] , Francesco A. Volpe[a] 

> a _Renaissance Fusion, 22 Rue J.P. Timbaud, 38600 Fontaine, France_ 

> b _Ecole Polytechnique Fédérale de Lausanne (EPFL), Lausanne, Switzerland_ 

## **1. Introduction** 

Deuterium-Tritium (D-T) fusion power-plants will generate large amounts of 14.1 MeV neutrons. As an example, a 1 GWe (≃ 2.2 GWth, and ≃ 2 GW of fusion power) plant will produce 7 _._ 1 ⋅ 10[20] such neutrons per second [1,2]. Power-plants of any size will have to harness their energy and self-sufficiently breed Tritium while minimizing disadvantages such as neutron activation, neutron damage to structural materials and superconducting coils, and radioactive dose levels. Fusion blanket is tailored to fulfill these requirements of heat extraction, fuel breeding, and shielding. 

The effects of highly energetic neutrons will be especially important in magnetic confinement fusion with High Temperature Superconducting (HTS) coils, as; (1) the higher fields enabled by HTS lead to more compact designs for the same amount of power, leading to higher neutron fluxes [1,3]; (2) HTS materials such as Rare Earth Barium Copper Oxide (ReBCO) owe their superconducting properties to specific 

crystalline structures susceptible to neutron damage and consequent degradation of the critical current-density and critical field [3–5]. Additionally, (3) nuclear heating can cause hot spots and ultimately quench the superconductor [2,6]. 

The blanket concept and total radial build in a magnetic confinement reactor have a major impact on the reactor design and cost. Reducing the blanket radial build (plasma-coil distance) from 1.3 m to 1 m could reduce a 1 GWe reactor’s cost by up to 20% [1]. There are significant benefits in minimizing the blanket radial build as it reduces the peak field at the coils for a given plasma on-axis field, and lowers the structural components size [1,7]. These reductions can be achieved by a proper choice of materials and blanket layout. 

Plasma facing flowing liquid metal (LM) has been shown to enable increased wall loading constraints and reduced solid components replacement rates compared with solid first walls [8]. In addition liquid metals are an attractive option for tritium breeding and neutron shielding [9,10] in compact radial builds. Few studies have investigated 

- Corresponding author. 

- _E-mail address:_ victor.prost@renfusion.eu (V. Prost). 

> 1 (Presently at) Max Planck Institute for Plasma Physics (IPP Garching). 

https://doi.org/10.1016/j.jnucmat.2024.155239 

Received 1 December 2023; Received in revised form 11 June 2024; Accepted 16 June 2024 

Available online 19 June 2024 

0022-3115/© 2024 The Authors. Published by Elsevier B.V. This is an open access article under the CC BY license (http://creativecommons.org/licenses/by/4.0/). 

![](images/tmpaupvkstl.pdf-0002-02.png)

**Fig. 1.** Schematic of the compact stellarator fusion device with thick flowing liquid metal plasma facing walls envisioned in [1] and described in Table 1. 

**Table 1** 

Reactor parameters for a conceptual stellarator reactor design point [1], a costeffective high-field compact fusion power plant delivering 1 GWe. 

compact stellarator fusion devices [2], and none with complete liquid metal first wall. Thick liquid metal first walls could enable compact fusion blankets and radial build in stellarators while allowing for heat extraction, continuous tritium breeding and neutron shielding [1,9,10]. 

In this study we developed a simplified, 1D cylindrical model of Renaissance Fusion’s compact stellarator power-plant concept [1] (Fig. 1 and Table 1) and explored blanket materials for compact fusion radial builds in the case of thick plasma facing flowing liquid metal first walls (suspension of solid neutron multiplier pebbles in a liquid breeder bulk). The stellarator design point considered is a 1 GWe high-field compact stellarator with major radius _𝑅_ = 3.8 m, aspect ratio _𝐴_ = 4.1, and onaxis field _𝐵_ = 10.2 T. Renaissance Fusion’s reactor relies on a thick Lithium and Lithium Hydride liquid metal first wall which includes coated millimeter size solid pebbles of neutron multiplier/moderator materials. Neutron shielding and damage of the magnets and vessel structures, nuclear heat extraction, tritium breeding, and doses level were considered through neutronics simulations. This works aims to provide a first exploration of the possible compositions, layout, and material thicknesses in order to realize a compact LM first wall blanket radial build. The resulting analyses and concepts could offer the basis for the reactor conceptual design, specific thermo-fluid and magneto hydrodynamics studies, as well as in depth 3D neutronics simulations. 

The paper is organized as follows; Sec. 2 describes the reactor and blanket neutronics model along with the major underlying assumptions. Sec. 3 - 4 consider various materials, thicknesses, layout from the plasma edge to the reactor outermost wall to fulfill respectively the breeding, and neutron shielding. In Sec. 5 the material thicknesses in the resulting conceptual radial build layout are optimized to achieve the blanket requirements in the most compact form factor for Renaissance Fusion’s power plant conceptual design point. 

![](images/tmpaupvkstl.pdf-0002-10.png)

**Fig. 2.** Fusion blanket and radial build requirements. (a) Functional design requirements considered in this study, (b) French regulation radiation zoning defined in the labor code _article R4451-23_ [13], adapted from [14] with a conversion base of about 160 hours per month. 

## **2. Neutronics analysis of the fusion blanket/radial build** 

## _2.1. Design requirements and regulations_ 

The fusion blanket and radial build have to fulfill three major functions; (1) heat extraction, (2) self-sufficient tritium breeding, and (3) neutron/radiation shielding of the HTS, structures and environment (Fig. 2). In addition to these, the materials and chosen concepts should maximize energy multiplication (exothermic reactions within the blanket) and minimize radioactive waste (neutron activation, and radioactivity levels). 

In order to use fusion energy to produce electricity, the heat generated through the D-T reactions needs to be extracted from the reactor core and sent to a power conversion system. Renaissance Fusion’s reactor concept [1] aims to use a thick plasma facing liquid metal first wall at temperatures of 700-900 °C as the main heat transfer fluid towards a combined cycle power conversion system [11]. The power exhaust will be deposited as surface heat to the liquid metal first wall, however the neutrons volumetric heating must be intercepted within the liquid metal layer. The nuclear heating requirement was chosen to be ≥ 90% in the liquid metal layer in order to improve efficiency and minimize ancillary cooling systems for the cryostat and HTS magnets [1]. In addition, neutron induced reactions in the blanket can lead to additional heat thanks to exothermic processes leading to an energy multiplication factor [12], which target was set to be ≥ 1 [1]. 

Fusion power-plants require tritium self-sufficiency to sustain the D- T reactions, meaning that the Tritium Breeding Ratio (TBR) needs to be greater than 1 [6]. To ensure it, a margin must be included to account for the uncertainties of the calculation itself but also the T losses encountered in the D-T fuel cycle [6,15]. Thus, even if the calculated requirement for DEMO is TBR ≥ 1 _._ 1, the design target chosen for this study is TBR≥ 1 _._ 15. This study considers a 1D model with full coverage (the surface covered by ports will results in lossed tritium breeding) which also increases the required target TBR, which according to Hong 

![](images/tmpaupvkstl.pdf-0003-02.png)

**Fig. 3.** Simplified reactor model with concentric layers used in the neutronic simulations along with the layer function, specific target requirements, and candidate materials. 

[16] requires a additional safety margin between 1D and 3D models with reasonable TBR targets being between 1.15 an 1.5. Higher TBR would open the door to tritium economy but might lead to additional complexity in the tritium extraction cycle as well as national fusion regulations. 

A major aspect of the fusion blanket is safety, which is linked to national fusion regulations in order to ensure and demonstrate the maximum possible neutron and radiation shielding to minimize the dose levels for the workers as well as minimize the amount of activated material. In this study, the dose level was set to be below 25 μSv/h outside of the reactor building (bioshield exterior) following the French Green Zone regulation (Fig. 2b) [13]. Neutron shielding is also crucial for long term operations as it will reduce the maintenance and ensure proper function of both the HTS as well as the solid structures of the plant’s lifetime. These requirements translated into a structural damage threshold of 200 DPA (or 6.25 DPA/yr assuming 32 full power years (fpy) of operations, 40 years at 80% availability), and a 10[19] n/cm[2] maximum neutron flux threshold on the HTS coils [3]. 

## _2.2. Model description_ 

The model has been build assuming a 1D tank-like cylindrical geometry (Fig. 1 & 3), so as to be consistent with the piece-wise reactor architecture with 4 cylinders foreseen by Renaissance Fusion while enabling fast running performances during parametric optimizations and simulations. Although this work focuses on the plasma facing liquid wall design proposed by Renaissance Fusion, it provides insights that can be extrapolated to other reactor design (as in [9]). 

One cylinder of the reactor is modeled to account for the 4-field period symmetry. The cylinder has an internal radius of 1 m and a length of 6.3 m to approximate those of the reactor with a major radius _𝑅_ = 3.8 m, aspect ratio _𝐴_ =4.1, and made of 4 piece-wise cylinders. The blanket materials are modeled as concentric cylinders with parameterized thicknesses representing the radial buildup of layers around the plasma (Fig. 3). 

The reactor radial build (Fig. 3) starts with the plasma that has a radius of 1 m, followed by the thick flowing liquid metal suspension of a neutron multiplier (Pb, Be, W, Mo) in the form of enclosed solid pebbles within the liquid metal tritium breeding material (Li, LiH, FLiBe, PbLi). The solid pebbles suspended in the liquid metal breeder are envisioned as millimeter size spheres with an outer shell made of SiC or other material which should resist the high operating temperatures, be corrosion resistant and a relative electrical insulator to the liquid metal breeder [17–20]. The pebbles would be sufficiently small in size (0.1 - 5 mm) to be suspended and flow with the liquid breeder layer. To improve the properties of this blanket model, the neutron multiplier pebbles should be suspended inwards of the liquid breeder layer, facing 

the plasma. In order to simplify the distribution of suspended pebbles in the liquid breeder material, the 1D cylindrical model considered here implemented a solid uniform layer of material to represent the neutron multiplier pebbles in suspension. This assumption is challenged and discussed in this study in Section 6. 

These initial neutron multiplier and breeder layers should enable a sufficient tritium breeding ratio, heat extraction, and neutron shielding of the 5 cm thick solid vacuum vessel enclosing the plasma and liquid metal wall. Vanadium Chrome Titanium (80.5 V - 14.5 Cr - 5 Ti, in weight percentages) [21] was considered in this model for the solid vacuum vessel enclosing the flowing liquid-metal wall for its corrosion resistance and for its low activation characteristics [22]. 

An additional neutron shielding material is then added to further attenuate and absorb the neutrons before the high-field magnet (1 cm thick HTS coil sandwiched between 50 cm of structural material). Specifically, neutron flux should be maintained below 10[19] n/cm[2] over the lifetime of the coil to ensure no significant degradation of the critical current [3,5,2,23], and the nuclear heating maintained below 2 mW/cm[3] to limit the load on the cryogenic system and reduce the risk of quenches [2]. Lastly, a bioshield is including to reduce the dose rate to acceptable levels (Fig. 2). Each layer’s function, requirement and candidate material is shown in Fig. 3. The neutronics analysis and optimization were conducted to determine the material and thickness of the tritium breeding, neutron multiplier, neutron shielding and bioshield layers that would fulfill the requirements while minimizing the total radial build. 

## _2.3. Neutronics analyses_ 

Using OpenMC Python API [24] the 1D tank-like cylindrical reactor model was build using cell-based cylindrical geometries instead of meshed based to leverage the poloidal symmetry and allow for computationally lighter simulations. The plasma was modeled as an isotropic cylindrical neutron source that occupies all the interior of the innermost cylinder (Fig. 3), with a 14.1 MeV homogeneous energy source. The radial build layers were constructed using cylindrical cells with a 0.5 cm resolution to resolve the radial distribution of physical quantities. The spatial resolution was increased from 0.5 cm to 8 cm for the magnet outer structures and the bioshield to limit the computation effort for these large thickness layers. Reflective boundary conditions were imposed on both sides of the cylinder, in order to simulate toroidal axisymmetry. Neutrons escaping from the last layers are considered as lost in the nature, hence a vacuum boundary condition has been imposed on the outer side of the cylinder. The materials were defined using the _neutronics material maker_ Python library and assigned to each layers and corresponding cells. The ENDF/B-VII.1 library [25] was applied for the material cross-sections. 

![](images/tmpaupvkstl.pdf-0004-02.png)

**Fig. 4.** Macroscopic cross sections for the considered neutron multiplier (a) and tritium breeding (b) material candidates. 

OpenMC simulations were run with the following settings; fixed source mode, 10 number of batches, and 10[6] number of particles for the shielding and breeding layer analyses while 10[8] particles for the case study, and 10[10] for the bioshield simulation. For each OpenMC simulation, the following tallies were recorded: TBR, neutron multiplications, DPA, dose rates (calculated using the ICRP coefficients [26]), neutron flux, neutron spectra, and nuclear heating. The OpenMC simulation results given per neutron source were then scaled to represent the 2 GW fusion power from deuterium-tritium reactions, and the corresponding 1 _._ 78 ⋅ 10[20] neutrons per second produced in the modeled cylinder. 

The study methodology was to construct the reactor radial build from inside out and then perform local optimization and changes to improve and validate the results for the case study. 

## **3. Breeding layers analysis** 

## _3.1. Candidate material_ 

The breeding layers correspond to a thick plasma facing flowing liquid metal wall comprised of both the tritium breeding material in liquid form and neutron multiplier material in encapsulated millimetric pebbles in suspension [17,18,20]. The breeding layers ensure three main functions: achieve a TBR above 1.15, ensure a DPA _<_ 200 on the solid vacuum vessel over the lifetime of the plant, and extract the heat from fusion core with an energy multiplication factor above 1. In this study the following materials were considered for the breeding layers; (Be, Mo, Pb, W) as high energy multipliers and (FLiBe, natural Li, Li6, LiLiH, PbLi) with varying level of Li6 enrichment for liquid metal breeders [10,9]. 

Macroscopic cross sections were used to determine and down select the candidate materials (Fig. 4 & 5). Based on the cross-sections, Pb was chosen as the neutron multiplier acting also as a high Z neutron attenuator. Beryllium has a lower cross-section in the 14.1 MeV range compared to Pb and would entail increasing challenges in safety and stringent regulatory rules. Tungsten and Molybdenum could also be used instead of Pb from their increased cross-section at 14.1 MeV although it would increase the cost by several orders of magnitude. 

To ensure Tritium breeding, a high content in Lithium is needed, and traditional liquid metal blankets have focused on FLiBe [9,3], or PbLi 

![](images/tmpaupvkstl.pdf-0004-11.png)

**Fig. 5.** Macroscopic cross sections of the considered tritium breeding materials for neutron elastic scattering (a) and absorption (b). 

[27]. In this study we are investigating the use of a lithium and lithiumhydride (LiH) mixture in order to enable increased tritium breeding (especially in the 5-15 MeV range, Fig. 4b) but also increased neutron shielding (highest neutron elastic scattering, Fig. 5). The concentration of Lithium Hydride was considered to be 95% in molar percentages in the case of the Li-LiH mixture so as to conserve a unique liquid phase for operating temperatures between 700 and 900 °C [28]. The Li-LiH mixture is in a fully liquid phase starting 680 °C, with Li melting point being 180 °C and LiH at 692 °C [28–30]. In addition, a high Li6 enrichment percentage was considered to understand its impact on tritium breeding and neutron shielding performances (Fig. 4 & 5). Interestingly the increased density of LiH compared to Li, leads to an increased atomic density of Li6 in the Li (5%) - LiH (95%), 90% Li6 enriched case (6 _._ 06 ⋅ 10[22] atom/cm[3] ) compared to the pure Li6 scenario (5 _._ 35 ⋅ 10[22] atom/cm[3] ). This results in an increased macroscopic tritium breeding cross section of Li (5%) - LiH (95%), 90% Li6 enriched compared to pure Li6 (Fig. 4). Investigating materials with higher Li6 atomic densities could further improve the breeding performance of fusion blankets. 

## _3.2. Comparison of breeding layer performance_ 

For each of the investigated liquid metal materials (FLiBe, natural Li, Li6, Li-LiH, PbLi) the breeder layer thickness was increased from 10 to 65 cm with a fixed 5 cm of plasma facing Pb pebbles layer. For each case, the neutronic simulation was conducted and the resulting tritium breeding ratio, liquid metal solid vessel DPA per year of irradiation, and energy multiplication provided by the breeding layer were then calculated (Fig. 6). 

The Li-LiH mixture along with the 90% Li6 enriched Li-LiH achieved the TBR = 1.15 requirement in a smaller breeder thickness of 1618 cm compared to the other breeder materials (Fig. 6a), with 90% enriched FLiBe needing 24 cm to achieve TBR = 1.15. Similarly for energy multiplication, 90% enriched Li-LiH along with the non-enriched case achieved an energy multiplication factor above 1.0 in the smallest thickness. Considering structural damage per year, 90% enriched Li-LiH resulted in the lowest damage for the same breeder thickness, with non-enriched Li-LiH achieving the same thickness as the enriched FLiBe to meet the 6.25 DPA/fpy threshold. Li-LiH mixture with 95% LiH achieved all the requirements in the most compact breeder thick- 

![](images/tmpaupvkstl.pdf-0005-02.png)

**Fig. 6.** Comparison of required tritium breeding layer thickness based on the breeding material and Li6 enrichment to meet the TBR (a), structure damage limit (b), and energy multiplication (c) targets. A fixed multiplier Pb layer thickness of 5 cm was used for all scenarios. Line colors represent different materials and each neutronic simulation is represented by a circular marker. 

![](images/tmpaupvkstl.pdf-0005-04.png)

**Fig. 7.** Investigation of the optimal combination of Pb and Li-LiH thicknesses to fulfill the TBR (a), structure damage limit (b), and energy multiplication (c) targets while minimizing the total thickness labeled bmin. Varying shades of colors represent the chosen Pb layer thickness, and each neutronic simulation is represented by a circular marker. 

ness compared to other breeder materials, with improved performances with the Li6 enriched Li-LiH case. 

The Pb pebbles layer thickness along with the non-enriched Li-LiH breeder thickness were then varied to find the optimal thickness combination of Pb and Li-LiH that would minimize the liquid metal breeder total thickness achieving the target requirements. Combination of 6 Pb pebbles thicknesses from 1 to 20 cm and 9 Li-LiH thicknesses from 5 to 45 cm were investigated, and the corresponding TBR, liquid metal vessel structure damage, as well as the breeder energy multiplication recorded through the neutronic simulations (Fig. 7). The solid structure damage limit behind the liquid metal walls resulted to be the critical requirement, needing a minimum of 27 cm total thickness to achieve the 200 DPA target over 32 full power years. This total minimum thickness was met for both the 10 and 15 cm Pb layer thickness. Then, an energy multiplication above 1.0 was met with a minimum thickness of 26 cm for the 10 cm Pb layer thickness. Lastly, the TBR target of 1.15 was reached with a minimum thickness of 17 cm with the 5 and 10 cm Pb layer thicknesses. 

A total breeding layer of 27 cm, composed of 10 cm of Pb followed by 17 cm of non-enriched Li-LiH with 95% LiH achieves the TBR, DPA, and energy multiplication requirements. This breeding configuration will achieve a TBR ratio of 1.53 producing an excess of tritium which could compensate the loss of breeding performance linked to ports, fuel cycle efficiency, or provide additional revenue sources from excess tritium production. From the simulations carried out on the tritium breeding material, using Li 6 enriched Li-LiH could lead to a further mi- 

nor reduction in total breeding layer thickness albeit at an substantially higher cost due to the costly process of Li 6 enrichment [31]. 

## **4. Neutron shielding** 

Protecting the structures, components and environment from highly energetic neutron flux is a critical requirement for the construction and operation of a fusion plant. More specifically, the neutron shielding material placed after the liquid metal layer and the vacuum vessel has the main function of protecting the HTS magnets (coils and structure) and its thickness should be minimized to reduce the plasma-coil distance, one of the most sensitive parameters in fusion reactor’s costs based on systems models [1]. A wide range of neutron shielding material were investigated based on previous neutronic studies [3,9,32] and specifically metal hydrides which have been shown to be effective neutron moderators [32,33]. Materials macroscopic total neutron crosssections (absorption, elastic scattering...) were compared to down-select the most promising candidates and get initial insights on possible effective materials (Fig. 8). 

For each considered neutron shielding material, a neutronic simulation was conducted with the optimal breeding layers configuration found above, with varying neutron shielding material thicknesses from 0.2 to 1.5 m. The minimum shielding thickness for which the magnet structure DPA, and neutron flux limit on the coils requirements were met was recorded in Fig. 9). Metal hydrides achieved the minimum shielding thicknesses between 53-68 cm along with boron 10 and 

![](images/tmpaupvkstl.pdf-0006-02.png)

**Fig. 8.** Macroscopic neutron interaction cross sections for varying neutron shielding candidate materials. The line color represents varying materials, and the black dashed line the 14.1 MeV energy level. 

![](images/tmpaupvkstl.pdf-0006-04.png)

**Fig. 9.** Minimum neutron shielding thickness which fulfills the neutron flux, nuclear heating and structure DPA requirements of the HTS magnet (coil + structure) for each neutron shielding material candidate. 

tungsten carbide. Although Li-LiH was effective as a tritium breeding material providing some neutron shielding for the vacuum vessel, using Li-LiH specifically for neutron shielding purposes would result in required thicknesses above 1 m. Vanadium hydride achieved the smallest shielding thickness with 53 cm making it one of the most effective neutron shielding material due to its high hydrogen density and mass number [33]. 

## **5. Case study for compact power plant radial build** 

After having identified the most promising configurations for the liquid metal breeding layer as well as the neutron shielding material, a specific neutronic case study was conducted for the compact stellarator power plant case described in Table 1. In these neutronics simulations, the material layer thicknesses were refined, and a bioshield comprised of borated concrete with 30% water in volume was added to meet the target radioactivity levels for workers outside of the reactor core (Fig. 2). The nuclear heating through the radial build, TBR, energy multiplication, structural damage in DPA, neutron flux through the layers, and dose rates were recorded. 

The resulting stellarator reactor radial build that meets all the target requirement in the smallest total thickness is shown in Fig. 10. The total 

![](images/tmpaupvkstl.pdf-0006-10.png)

**Fig. 10.** Resulting radial build for the considered stellarator reactor case. 

![](images/tmpaupvkstl.pdf-0006-12.png)

**Fig. 11.** Nuclear heating throughout the blanket and neutron shielding layers. The shaded areas represent each modeled material layer, and the total nuclear heat per layer is shown in MW or % of the total nuclear heat. 

thickness from the plasma to the HTS magnet inboard structure is 91 cm, with 32 cm of flowing liquid metal walls, 5 cm of vacuum vessel thickness, and 54 cm of neutron shield. 

The flowing liquid metal plasma facing wall is comprised of 10 cm of Pb pebbles, and 22 cm of non enriched Li-LiH with 95% LiH. The Li-LiH layer thickness was increased from 17 cm to 22 cm to meet the nuclear heat extraction target discussed below. The Pb and Li-LiH layers yield a tritium breeding ratio of 1.60, energy multiplication factor of 1.07, and vacuum vessel structural damage of 4.85 dpa/fpy. In addition, the liquid metal layers intercepts 90% of the nuclear heat, 1.6 GW as shown in Fig. 11. The remaining heat is applied on the vacuum vessel (3%, 54 MW) and the neutron shield (8%, 150 MW). This nuclear heat still amounts to a substantial fraction meaning that active cooling and heat extraction will have to be implemented in these two layers to maintain stable temperatures. However, the nuclear heating on the HTS coils was significantly smaller than the target requirement of 2 mW/cm[3] , reaching 0.14 mW/cm[3] in this case study and thus lowering the load requirement on the HTS cryogenic system. 

In addition to the reduced nuclear heating on the HTS coils, the neutron flux on the HTS coils was reduced below 10[19] n/cm[2] over the lifetime of the plant (32 fpy), as shown in Fig. 12. Both the neutron flux as well as the neutron energy spectrum are reduced, meaning that fewer neutrons are escaping the reactor core, and that their energy is reduced from the original 14.1 MeV source (Fig. 12a). The neutron flux 

![](images/tmpaupvkstl.pdf-0007-02.png)

**Fig. 12.** Neutron flux results, in neutron per cm[2] per neutron source. The neutrons flux and spectrum are shown in schematic (a) with each line representing a specific position in the radial build and the line color the corresponding material layer. The neutron flux throughout the blanket and shielding layers is shown in (b), with the line color representing the total flux, and flux per energy range. The shaded areas identify the layer material. 

reduction through the layers (Fig. 12b) also highlights the reduction in energy of the neutrons as both the total neutron flux and the neutron flux per energy range are shown. The reduction of the neutron flux per layers also confirms that although the Li-LiH layer provides some neutron shielding, VH2 achieves a stronger shielding with a stronger slope in the neutron flux curve. 

Lastly, the required bioshield thickness was calculated to minimize the dose rate below the ‘Green zone’ levels for workers of 25 μSv/h outside the concrete bioshield. A 1.3 m thick bioshield was necessary to achieve the dose rate level target, and the resulting spatial dose rate levels through the reactor are shown in Fig. 13. This bioshield thickness is similar to previous neutronic studies and existing facilities sizes [2,34]. There are fewer requirements on minimizing the bioshield thickness as this concrete structure encloses all critical reactor components. As shown in the dose rate map (Fig. 13), metal hydrides are more effective for reducing the dose rate but are not as cost effective as concrete. The dose rate map (Fig. 13) also highlights that the stellarator hall will not be accessible by workers during operations as it exceeds the ‘Orange zone’ level for nuclear personnel. 

## **6. Discussion and conclusion** 

The neutronic analyses presented in this study show that the use of thick Li-LiH flowing liquid metal plasma-facing wall combined with 

![](images/tmpaupvkstl.pdf-0007-08.png)

**Fig. 13.** Dose rate variations throughout the reactor radial build. The colored dashed line represents the thresholds corresponding to the zoning regulations, and the shaded areas the corresponding material layer in the radial build. 

coated Pb pebbles in suspension allows for the conceptual design of a power-plant relevant blanket, with a total radial build under 1 m between the plasma first wall and the HTS magnets. This radial build configuration achieves a TBR of 1.53, an energy multiplication of 1.05, extracts 90% of the nuclear heat in the liquid metal layers, ensures lifetime operations for the HTS coils and solid structures, and limits the radioactivity below 25 μSv/h outside of the 1.3 m thick bioshield. 

From the various radial build requirements (Fig. 2), the most stringent constraints were the neutron shielding ones; specifically the neutron flux limit on the HTS coils and the structural DPA limit on the vacuum vessel supporting the liquid metal flow. Enabling the replacement of the vacuum vessel or the HTS coils could further reduce the radial build total thickness and improve the reactor’s total construction cost albeit at an increase in maintenance costs and lower availability. Similarly the use of Li6 enrichment would lead to some small increase in the TBR, energy multiplication, improve the neutron shielding of the liquid metal layer or lead to further thickness reduction of the blanket (Fig. 6). A detailed cost analysis, that is highly dependent of the enrichment technique used, could be performed to better estimate the optimal enrichment level, and the trade-offs in costs/revenues with the increased production of tritium, and the reduced blanket thickness. 

The assumption of a suspension of plasma facing Pb pebbles in the liquid Li-LiH wall represented as a solid layer was tested through a specific neutronic simulation were the position and model for the Pb pebbles layer was varied. Three cases were considered: the reference case of plasma facing Pb pebbles, varying volumetric mixture of Pb and Li-LiH, and having the Li-LiH layer facing the plasma with the Pb pebbles behind the Li-LiH. The minimum breeding blanket thicknesses and the Pb, Li-LiH configurations for which the heat extraction, tritium breeding, and vacuum vessel shielding requirements are fulfilled are shown in Fig. 14. Having the Li-LiH facing the plasma with the Pb pebbles behind required a 45 cm thick breeding blanket compared to the 32 cm reference case. For a homogeneous Pb pebbles and Li-LiH mixture, the minimum breeding blanket thickness was 34 cm, achieved with a 50% volumetric mix of Pb and Li-LiH. The effect of mixing between the coated Pb pebbles, the most probable scenario, and the Li-LiH liquid metal has a minor effect of the breeding blanket thickness and performance whereas the inversion of the Pb pebble layer, worst case scenario, and the Li-LiH leads to a significant increase in the required breeding blanket thickness. 

Although this work presents a simplified 1D model with layers instead of pebbles for example, it provides a promising starting point for in depth neutronic studies which would include specific neutron sources and spectra, shutdown dose rates, decay heat, as well as activation calculations. These results warrant a detailed reactor blanket design based on this configuration which would enable a future 3D neutronics simulation. 

![](images/tmpaupvkstl.pdf-0008-02.png)

**Fig. 14.** Breeding blanket minimum thickness when investigating the position of the Pb pebbles in the liquid metal layer, either fully mixed with the Li-LiH, at the surface facing the plasma or close to vacuum vessel with the Li-LiH facing the plasma. The schematic represents the minimum thickness to fulfill the heat extraction, tritium breeding, and vacuum vessel shielding requirements. The labeled reference case corresponds to the case study result from Sec. 5. 

## **CRediT authorship contribution statement** 

**Victor Prost:** Writing – review & editing, Writing – original draft, Visualization, Validation, Methodology, Investigation, Formal analysis, Data curation, Conceptualization. **Sabine Ogier-Collin:** Writing – original draft, Visualization, Software, Methodology, Investigation, Formal analysis, Data curation, Conceptualization. **Francesco A. Volpe:** Writing – review & editing, Supervision, Resources, Conceptualization. 

## **Declaration of competing interest** 

The authors declare the following financial interests/personal relationships which may be considered as potential competing interests: 

Francesco Volpe has patent #WO2023194373A1 issued to Renaissance Fusion. If there are other authors, they declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. 

## **Data availability** 

Data will be made available on request. 

## **Acknowledgement** 

The whole OpenMC development team and the Fusion Energy GitHub contributors must be thanked for their availability and prompt help in explaining the software features. We also to thank our team at Renaissance Fusion, Nicolas Louis for the stellarator schematics, Carlo Sborchia and Alan Brice Ott for their insights and review of the manuscript. 

## **References** 

- [1] V. Prost, F.A. Volpe, Economically optimized design point of high-field stellarator power-plant, Nucl. Fusion 1 (2023) 1. 

- [2] L. El-Guebaly, P. Wilson, D. Henderson, M. Sawan, G. Sviatoslavsky, T. Tautges, R. Slaybaugh, B. Kiedrowski, A. Ibrahim, C. Martin, et al., Designing aries-cs compact radial build and nuclear system: neutronics, shielding, and activation, Fusion Sci. Technol. 54 (3) (2008) 747–770. 

- [3] B. Sorbom, J. Ball, T. Palmer, F. Mangiarotti, J. Sierchio, P. Bonoli, C. Kasten, D. Sutherland, H. Barnard, C. Haakonsen, et al., Arc: a compact, high-field, fusion nuclear science facility and demonstration power plant with demountable magnets, Fusion Eng. Des. 100 (2015) 378–405. 

[4] D.X. Fischer, R. Prokopec, J. Emhofer, M. Eisterer, The effect of fast neutron irradiation on the superconducting properties of rebco coated conductors with and without artificial pinning centers, Supercond. Sci. Technol. 31 (4) (2018) 044006. 

- [5] M. Iio, M. Yoshida, T. Nakamoto, T. Ogitsu, M. Sugano, K. Suzuki, A. Idesaki, Investigation of irradiation effect on rebco coated conductors for future radiation-resistant magnet applications, IEEE Trans. Appl. Supercond. 32 (6) (2022) 1–5. 

- [6] U. Fischer, C. Bachmann, I. Palermo, P. Pereslavtsev, R. Villari, Neutronics requirements for a demo fusion power plant, Fusion Eng. Des. 98 (2015) 2134–2137. 

- [7] B. Hong, T.-H. Kim, On the optimal radial build of a normal aspect ratio tokamak fusion system, Fusion Eng. Des. 139 (2019) 148–154. 

- [8] J. You, E. Visca, T. Barrett, B. Böswirth, F. Crescenzi, F. Domptail, G. Dose, M. Fursdon, F. Gallay, H. Greuner, et al., High-heat-flux technologies for the European demo divertor targets: state-of-the-art and a review of the latest testing campaign, J. Nucl. Mater. 544 (2021) 152670. 

[9] S. Segantin, R. Testoni, M. Zucchetti, Neutronic comparison of liquid breeders for arc-like reactor blankets, Fusion Eng. Des. 160 (2020) 112013. 

- [10] M. Abdou, A. Ying, N. Morley, K. Gulec, S. Smolentsev, M. Kotschenreuther, S. Malang, S. Zinkle, T. Rognlien, P. Fogarty, et al., On the exploration of innovative concepts for fusion chamber technology, Fusion Eng. Des. 54 (2) (2001) 181–247. 

[11] F.R. Famà, G. Loreti, G. Calabrò, S. Ubertini, F.A. Volpe, A.L. Facci, An optimized power conversion system for a stellarator-based nuclear fusion power plant, Energy Convers. Manag. 276 (2023) 116572. 

- [12] K. Maki, Energy multiplication in high tritium breeding ratio blanket with front breeder zone for fusion reactors, J. Nucl. Sci. Technol. 25 (1) (1988) 72–80. 

- [13] Legifrance, Article r4451-23, https://www.legifrance.gouv.fr/codes/article_lc/ LEGIARTI000047715473, 2023. 

- [14] CNRS, Risques radioactifs et radioprotection, Cahier de prévention, 2nd edition, 2018, https://www.dgdr.cnrs.fr/SST/CNPS/guides/radioprotection.htm. 

- [15] U. Fischer, L. Boccaccini, F. Cismondi, M. Coleman, C. Day, Y. Hörstensmeyer, F. Moro, P. Pereslavtsev, Required, achievable and target tbr for the European demo, Fusion Eng. Des. 155 (2020) 111553. 

[16] B. Hong, Impact of neutronic constraints on the design and performance of a tokamak demo reactor, Fusion Eng. Des. 155 (2020) 111567. 

[17] F.A. Volpe, Lithium hydride first wall, https://patents.google.com/patent/ WO2023194373A1, Oct. 2023. 

[18] J. Fradera, S. Sádaba, F. Calvo, S. Ha, S. Merriman, P. Gordillo, J. Connell, A. Elfaraskoury, B. Echeveste, Pre-conceptual design of an encapsulated breeder commercial blanket for the step fusion reactor, Fusion Eng. Des. 172 (2021) 112909. 

- [19] E. Ishitsuka, H. Kawamura, Thermal and mechanical properties of beryllium pebbles, Fusion Eng. Des. 27 (1995) 263–268. 

[20] O. Leys, P. Waibel, J. Matthes, R. Knitter, Ceramic pebble production from the breakup of a molten laminar jet, in: Proceedings of the 29th ILASS-Europe, Paris, 2019. 

[21] B. Loomis, H. Chung, L. Nowicki, D. Smith, Effects of neutron irradiation and hydrogen on ductile-brittle transition temperatures of v-cr-ti alloys, J. Nucl. Mater. 212 (1994) 799–803. 

[22] S. Segantin, R. Testoni, M. Zucchetti, Arc reactor–neutron irradiation analysis, Fusion Eng. Des. 159 (2020) 111792. 

[23] M. Jirsa, M. Rameš, I. Duran,[ˇ] T. Entler, L. Viererbl, Critical currents in rebacuo superconducting tapes in response to neutron irradiation, Supercond. Sci. Technol. 32 (5) (2019) 055007. 

[24] P.K. Romano, N.E. Horelik, B.R. Herman, A.G. Nelson, B. Forget, K. Smith, Openmc: a state-of-the-art Monte Carlo code for research and development, Ann. Nucl. Energy 82 (2015) 90–97. 

[25] M.B. Chadwick, M. Herman, P. Obložinsk`y, M.E. Dunn, Y. Danon, A. Kahler, D.L. Smith, B. Pritychenko, G. Arbanas, R. Arcilla, et al., Endf/b-vii. 1 nuclear data for science and technology: cross sections, covariances, fission product yields and decay data, Nucl. Data Sheets 112 (12) (2011) 2887–2996. 

- [26] N. Petoussi-Henss, W. Bolch, K. Eckerman, A. Endo, N. Hertel, J. Hunt, M. Pelliccioni, H. Schlattl, M. Zankl, Conversion coefficients for radiological protection quantities for external radiation exposures, Ann. ICRP 40 (2–5) (2010) 1–257. 

[27] L. Boccaccini, G. Aiello, J. Aubert, C. Bachmann, T. Barrett, A. Del Nevo, D. Demange, L. Forest, F. Hernandez, P. Norajitra, et al., Objectives and status of eurofusion demo blanket studies, Fusion Eng. Des. 109 (2016) 1199–1206. 

- [28] W.M. Mueller, J.P. Blackledge, G.G. Libowitz, Metal Hydrides, Elsevier, 2013. 

- [29] S. Zinkle, Summary of physical properties for lithium, pb-17li, and (lif) n• bef2 coolants, in: APEX Study Meeting, Sandia National Laboratories, 1998, pp. 1–8. 

- [30] R.L. Smith, J.W. Miser, Compilation of the properties of lithium hydride, Tech. Rep., Los Alamos Scientific Laboratory, 1963. 

- [31] T. Giegerich, K. Battes, J. Schwenzer, C. Day, Development of a viable route for lithium-6 supply of demo and future fusion power plants, Fusion Eng. Des. 149 (2019) 111339. 

- [32] B. Hong, W. Cho, Neutronic analysis of effects of inboard materials on the size of a tokamak fusion reactor, Nucl. Mater. Energy 28 (2021) 101040. 

- [33] T. Tanaka, H. Muta, Y. Hishinuma, H. Tamura, T. Muroga, A. Sagara, Applicability of hydride materials for radiation shielding in helical reactor ffhr-d1, Fusion Sci. Technol. 68 (3) (2015) 705–710. 

- [34] E. ITER, Documentation series no. 24 iter technical basis, IAEA, Vienna, http:// www-pub.iaea.org/MTCD/publications/PDF/ITER-EDA-DS-24.pdf, 2002. 

