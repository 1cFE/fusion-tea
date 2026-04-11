---
source: "https://www.frontiersin.org/journals/nuclear-engineering/articles/10.3389/fnuen.2025.1683702/full"
source_type: "url"
extracted_at: "2026-04-06T05:21:02.733289+00:00"
content_hash_sha256: "489dad7291f7deb4e2bbb9aa8fc8b2ec9d1070d564312263f8989e257c51bf90"
backend: "trafilatura"
title: "Frontiers | Assessment of structural materials in compact fusion reactor design"
author: "Pettinari; Davide; Meschini; Samuele; Testoni; Raffaella"
---

## Abstract

The development of fusion energy systems demands structural components capable of withstanding extreme operational conditions, including intense neutron fluxes, high thermal and mechanical loads, and stringent requirements on neutron activation. Several structural materials have been proposed, such as nickel-based superalloys, reduced activation ferritic/martensitic steels, oxide-dispersion-strengthened alloys, SiC/SiC ceramic matrix composites, and vanadium-based alloys. While those materials have been extensively analysed for large tokamaks, no comparative studies exist on compact tokamaks. This work addresses this gap by considering an ARC-class tokamak as representative of compact design. The materials are evaluated based on the following criteria: power density deposition, absorption rate, TBR, energy multiplication factor within the breeding blanket, and displacement per atom. Numerical simulations were performed using the OpenMC Monte Carlo particle transport code to evaluate the neutronic behavior and activation characteristics of the selected structural materials. A simplified compact reactor model was developed using Constructive Solid Geometry (CSG) to enable consistent and reproducible comparisons. ODS steels and vanadium-based alloys emerged as the most promising candidates for application in compact, high-temperature fusion devices. ODS steels combine low activation with favorable performance across all evaluated metrics, offering a balanced tritium breeding capability alongside good resistance to radiation damage. Vanadium-based alloys, in turn, exhibit very low hydrogen and helium production, minimal power density deposition, facilitating heat removal from the structural material, and activation levels significantly lower than those of conventional austenitic steels. Across all materials, the simulations predict TBR values in the range of 0.90–1.25, energy multiplication factors of between 1.12 and 1.18, and first structural layer power densities of over 7 MW/m3. In the most favourable cases, the shutdown dose rates fall below natural background levels in less than 50 years.

## 1 Introduction

The development of structural materials suitable for fusion reactors has been an active field of research since the early stages of fusion energy studies. Among the various components of a fusion system, the vacuum vessel (VV) plays a central role: it provides a high-vacuum environment for the plasma, improves radiation shielding and plasma stability, acts as the primary confinement barrier for radioactivity, serves as a structural and safety-critical element in the overall reactor architecture, and provides support for in-vessel components such as the blanket and the divertor ([Ribe, 1975](https://www.frontiersin.org#B51)).

Several breeding blanket concepts were proposed in the last 40 years, initially focused on a subset of potential fusion devices (tokamaks and mirror machines) ([Smith et al., 1985b](https://www.frontiersin.org#B60)), and further worked out for fusion power plants like DEMO ([Federici et al., 2019](https://www.frontiersin.org#B19)). Although most of the designs of breeding blankets (and corresponding structural materials) are machine-dependent, the requirements and constraints on those components are generalizable and applicable to many of the novel concepts of fusion machines developed by private fusion companies ([Meschini et al., 2023b](https://www.frontiersin.org#B41)).

The performance and attractiveness of a blanket concept depend on several interrelated factors, including power production, safety, availability, tritium self-sufficiency, and overall economic viability. Concepts designed to maximise performance, such as achieving high tritium breeding ratios and thermal efficiency, or to prioritise safety through the use of low-activation materials and inherently stable coolants, often place significant demands on the choice and capabilities of structural materials. Such designs are generally associated with higher development risk due to the challenging operational conditions they impose ([Raffray et al., 2002](https://www.frontiersin.org#B49)).

In this context, the use of lithium in blanket systems imposes stringent requirements on the chemical compatibility, corrosion resistance, and mechanical integrity of structural materials, particularly under off-normal conditions such as water ingress, air ingress, or high-temperature operation. Beryllium, while serving as an effective neutron multiplier, presents additional challenges due to its toxicity, activation characteristics, and limited global availability, as noted by [Hernández and Pereslavtsev (2018)](https://www.frontiersin.org#B23). These concerns have motivated the development of advanced beryllium-based compounds, such as beryllides, which can reduce tritium retention and swelling while enabling operation at temperatures above 900 °C. In the specific case of FLiBe-based systems, corrosion is driven primarily by the fluoride chemistry of the molten salt, with beryllium acting as a reducing agent that can, in fact, mitigate some corrosion processes.

Finally, the adoption of liquid neutron multipliers such as molten lead can, in principle, avoid some of the thermo-mechanical compatibility issues associated with solid–solid interfaces, such as differential thermal expansion or contact stresses, between breeder and structural components. However, such designs inherently introduce liquid–solid interface challenges, including chemical compatibility, corrosion, and erosion under neutron irradiation, which can be more severe and require dedicated mitigation strategies. While liquid multipliers can simplify certain aspects of blanket module integration, their successful adoption critically depends on the development of structural materials capable of long-term operation in direct contact with high-temperature liquid metals.

A wide range of structural materials is observed across the various breeding blanket concepts currently under development for fusion reactors. Reduced activation ferritic/martensitic (RAFM) steels, in particular EUROFER, represent the reference structural option for most blanket designs developed in Europe and Japan ([Konishi et al., 2017](https://www.frontiersin.org#B32)). EUROFER is employed in the HCPB (Helium-Cooled Pebble Bed) ([Boccaccini et al., 2022](https://www.frontiersin.org#B9)), WCLL (Water-Cooled Lithium-Lead) ([Arena et al., 2023](https://www.frontiersin.org#B3)), HCLL (Helium-Cooled Lithium-Lead) ([Aubert et al., 2018](https://www.frontiersin.org#B5)), DCLL (Dual-Coolant Lithium-Lead), WLCB (Water-cooled Lead Ceramic Breeder) ([Zhou et al., 2021](https://www.frontiersin.org#B70)), and WCCB (Water-Cooled Ceramic Breeder) concepts ([Kawamura et al., 2024](https://www.frontiersin.org#B30)), as well as in the double-bundle WCLL variant (WCLL-db) ([Di Maio et al., 2024](https://www.frontiersin.org#B14)).

In more advanced or conceptually alternative blanket configurations, different classes of materials have been explored. Vanadium-based alloys, such as V–4Cr–4Ti, are envisioned in the liquid lithium STEP concept ([Lord et al., 2024](https://www.frontiersin.org#B37)) due to their excellent compatibility with high-temperature liquid lithium and their intrinsically low residual activation. Silicon carbide composites (SiC/SiC), known for their superior thermal performance and radiation resistance, are planned in the PbLi SCLL (Self-Cooled Lithium-Lead) blanket ([Pearson et al., 2022](https://www.frontiersin.org#B45)). Even in more particular configurations, such as encapsulated breeding blankets based on hollow spheres filled with liquid breeder, EUROFER is also envisioned for the encapsulated breeding blanket (EBB) concept for STEP ([Fradera et al., 2021](https://www.frontiersin.org#B20)).

For liquid breeder designs such as the FLiBe-LIB (Liquid Immersion Blanket), Sorbom and Kuang proposed the use of Inconel 718 as structural material in the Affordable, Robust, Compact (ARC) concept ([Sorbom et al., 2015](https://www.frontiersin.org#B61); [Kuang et al., 2018](https://www.frontiersin.org#B34)), primarily due to its availability and performance in molten salt environments. However, since Inconel 718 is not a low-activation alloy, several studies have highlighted the importance of exploring alternative structural candidates with more favorable activation characteristics ([Segantin et al., 2020](https://www.frontiersin.org#B56)).

The differentiated adoption of structural materials across the various blanket concepts reflects not only constraints related to compatibility and activation, but also the specific thermal operating conditions characteristic of each reactor. [Figure 1](https://www.frontiersin.org#F1) provides a concise and comparative overview of the main materials developed for nuclear applications, indicating for each material its maximum operating temperature and the year when the development of that material has started.

FIGURE 1

The graph also highlights four distinct temperature bands corresponding to the expected operating conditions of the ITER, DEMO, STEP EBB, and ARC tokamaks. These reference ranges allow for a quick visual assessment of which materials are thermally compatible with each reactor concept and, conversely, which materials are unsuitable under specific operational conditions.

The paper is structured as follows: [Section 2](https://www.frontiersin.org#s2) introduces the key requirements that structural materials must fulfill to be suitable for application in the vacuum vessel of a fusion reactor; [Section 3](https://www.frontiersin.org#s3) provides a comprehensive review of the most promising classes of candidate materials, outlining their fundamental physical and mechanical properties; [Section 4](https://www.frontiersin.org#s4) presents the neutronic and activation analyses performed to quantitatively assess the behavior of these materials under fusion-relevant conditions; the results are subsequently discussed in [Section 5](https://www.frontiersin.org#s5). Finally, [Section 6](https://www.frontiersin.org#s6) discusses the main achievements, the open issues, and the current technological maturity of the design described in [Section 3](https://www.frontiersin.org#s3).

The computational model employed for the neutronic and activation analyses uses as baseline an ARC-class fusion reactor configuration, which operates at high temperatures and adopts a LIB concept. The model was entirely developed using the OpenMC, a community-developed Monte Carlo neutron and photon transport code ([Romano et al., 2015](https://www.frontiersin.org#B53)). Accordingly, the structural materials tested within were selected among those considered the most suitable candidates for the vacuum vessel of such a compact, high-field tokamak.

In this context, it is important to distinguish between conventional large-scale tokamaks (e.g., ITER, DEMO), which operate at moderate magnetic fields (–6 T) and larger dimensions (major radius m), and compact high-field reactors (e.g., ARC, SPARC), characterized by stronger fields (–12 T) and smaller size (major radius –4 m). This distinction is crucial, as the neutronic environment, thermal loads, and structural material requirements can differ substantially between the two reactor classes.

## 2 Functional requirements for vacuum vessel structural materials

The operating conditions in a future fusion power plant (FPP) imposes stringent demands on structural materials, particularly those employed in the vacuum vessel. These materials are required to operate reliably under extreme thermal, mechanical, and radiological conditions, while simultaneously complying with safety, regulatory, and operational constraints. One of the primary challenges is the requirement for low activation behaviour. Structural materials must exhibit reduced long-term radioactivity to allow for safe and relatively rapid dismantling of reactor components after shutdown, without posing significant radiological hazards ([Ehrlich, 1999](https://www.frontiersin.org#B17)). This criterion substantially limits the range of allowable alloying elements and necessitates the development and qualification of novel reduced-activation materials.

In addition, many of the candidate materials still lack full nuclear qualification and are not yet supported by established industrial supply chains. The creation of a complete regulatory framework and scalable production capabilities remains a key obstacle to the commercial deployment of fusion technologies. From an engineering standpoint, the integration of complex cooling circuits, multi-material interfaces, and intricate component geometries further constrains material selection, as the materials must demonstrate excellent manufacturability and joinability.

Thermal loads in plasma-facing components (PFCs), such as tungsten tiles, can locally exceed 1000 °C ([Bolt et al., 2004](https://www.frontiersin.org#B10)), requiring materials with exceptional high-temperature stability and resistance to creep. In addition, PFCs are exposed to direct plasma interaction, which causes surface erosion and sputtering, increasing the impurity content in the plasma; this drives the need for low-sputtering-yield materials.

Structural materials, by contrast, must meet different but equally demanding requirements. In certain regions of the reactor, particularly near toroidal magnet systems, they are exposed to magnetic fields often exceeding 10T, necessitating mechanical reliability under combined mechanical and electromagnetic loads. A major challenge is the degradation caused by intense neutron irradiation: fast neutrons displace atoms from their lattice sites, inducing swelling, embrittlement, and the formation of transmutation products that can alter microstructure and mechanical properties ([Alba et al., 2022](https://www.frontiersin.org#B2)). Recent analyses have also shown that neutron-induced damage creates high-energy trapping sites for tritium, acting as a strong tritium sink with severe implications for tritium self-sufficiency ([Meschini et al., 2023a](https://www.frontiersin.org#B40); [Meschini et al., 2025](https://www.frontiersin.org#B42)).

Furthermore, in systems employing liquid breeders, structural components in direct contact with the breeder must withstand corrosion and chemical interaction specific to the breeder chemistry; for example, fluoride-induced corrosion in FLiBe, dissolution effects in Pb-Li, or severe reactivity in liquid lithium, which can critically impair their long-term mechanical integrity. In certain proposed designs, particularly compact reactor configurations ([Sorbom et al., 2015](https://www.frontiersin.org#B61)), lithium is present within molten salt mixtures that serve as both tritium breeders and cooling fluid. As a result, structural materials must maintain long-term stability in direct contact with molten salts, which are known to be highly corrosive under fusion-relevant conditions ([Sridharan and Allen, 2013](https://www.frontiersin.org#B63)). Ensuring adequate corrosion resistance in such environments is essential to prevent degradation mechanisms that could compromise the structural integrity and service lifetime of the vacuum vessel and associated components.

To address the extreme operational conditions outlined above, structural materials must satisfy a number of interdependent functional requirements. [Table 1](https://www.frontiersin.org#T1) provides a summary of the key properties that guide material selection for vacuum vessel applications, highlighting their physical meaning and importance in the context of fusion technology.

TABLE 1

| Property | Description | Relevance in fusion environment |
|---|---|---|
| Strength, ductility and toughness | Ability to withstand static and dynamic mechanical loads without failure | Ensures mechanical integrity and structural resilience under operational and accidental loads. Indicative targets: yield strength (YS) 500 MPa (RT); ultimate tensile strength (UTS) 700 MPa (RT) |
| Creep and fatigue resistance | Resistance to time-dependent deformation and cyclic damage | Critical under high-temperature operation and pulsed thermal loading typical of fusion devices |
| Helium embrittlement resistance | Tolerance to degradation caused by helium bubble formation under irradiation | Maintains ductility and prevents premature failure due to transmutation-induced gas accumulation |
| Chemical compatibility and corrosion resistance | Resistance to chemical attack from breeder and coolant materials (e.g., LiPb, FLiBe) | Ensures long-term stability when in contact with aggressive fusion-specific fluids |
| Tritium solubility | Ability of the material to absorb and retain tritium | Affects tritium retention, permeation, safety, and fuel inventory management |
| Operating temperature | Temperature range within which the material maintains acceptable structural performance | Influences design window, thermal efficiency, and determines compatibility with breeder and coolant systems |
| Radiation resistance | Stability of properties under neutron irradiation | Prevents embrittlement, swelling, and degradation of performance in reactor lifetime |
| Low activation | Tendency to generate short-lived, low-toxicity radionuclides under irradiation | Facilitates remote handling, recycling, and minimizes long-term radioactive waste |

Key material properties for structural components in fusion reactors.

Neutron irradiation produces damage through two primary mechanisms: direct atomic displacements and nuclear transmutation. Fast neutrons displace atoms via collisions that generate primary knock-on atoms (PKAs), initiating defect cascades composed of vacancies and interstitials ([Judge et al., 2013](https://www.frontiersin.org#B25)). Simultaneously, neutron capture reactions lead to the formation of impurity atoms such as helium and hydrogen via (n,) and (n,p) reactions, respectively.

## 3 Overview of candidate materials

### 3.1 Austenitic stainless steels and nickel-based alloys

These steels are characterized by an austenitic face-centered cubic (FCC) microstructure, offering excellent toughness, ductility, corrosion resistance and weldability ([Pollock and Tin, 2006](https://www.frontiersin.org#B48)). However, it is important to note that austenitic stainless steels and nickel-based alloys, despite their common FCC structure, belong to distinct families: the former are Fe-based alloys stabilized by Ni, Mn, and N, whereas the latter (e.g., Inconel, Incoloy) are Ni-rich and often precipitation-hardenable.

Unlike martensitic steels, austenitic stainless steels are not hardenable through heat treatment and are generally non-magnetic. The stable austenitic phase is achieved through the addition of alloying elements that act as austenite stabilizers, primarily nickel, but also manganese and nitrogen. Within this family, nickel-rich alloys such as those in the Incoloy series are often referred to as super austenitic stainless steels, owing to their enhanced corrosion resistance and performance in high-temperature or aggressive environments.

Other relevant austenitic materials include SS316, a molybdenum-containing stainless steel known for its resistance to pitting and crevice corrosion; Inconel 718, part of the Inconel family of precipitation-hardenable nickel-based alloys, valued for its excellent creep strength and high-temperature performance; and XM-19 (Nitronic 50), a nitrogen-strengthened alloy offering high yield strength and good corrosion resistance.

While in most alloys damage is dominated by fast neutrons, in nickel-based alloys thermal neutrons also contribute significantly due to transmutation reactions involving Ni-58 ([Griffiths et al., 2010](https://www.frontiersin.org#B22)). The production of Ni-59, followed by highly exothermic (n,), (n,p), and (n,) reactions, results in substantial displacement damage ([Greenwood and Garner, 1996](https://www.frontiersin.org#B21)). These combined effects cause hardening, swelling, and embrittlement. Lastly, despite their excellent thermo-mechanical performance, Nickel-based alloys exhibit high neutron-induced activation and swelling, which limits their use in components where low-level radioactive waste classification is a requirement.

### 3.2 Reduced activation ferritic/martensitic (RAFM) steels

RAFM (Reduced Activation Ferritic/Martensitic) steels are specifically designed to minimize nuclear activation. The formation of highly radioactive, short-lived nuclides impacts short-term management of the materials (e.g., for maintenance or component replacement and in-plant disposal), while long-lived radioisotopes must decay to acceptable levels (e.g., suitable for recycling or shallow land burial) within the timeframes defined by radioactive waste management strategies, typically within 100 years after reactor shutdown. Thus, the need for reduced activation materials.

Neutronic and safety analyses highlight the necessity of eliminating undesirable elements such as Co, Cu, Ni, Mo, and Nb, which are commonly present as impurities in conventional steels. At the same time, the concentrations of certain elements essential for maintaining the mechanical performance of RAFM steels, such as Al and N, must be carefully optimized to balance structural integrity requirements with long-term waste disposal objectives ([Tanigawa et al., 2017](https://www.frontiersin.org#B66)).

Several RAFM steels have been developed internationally to meet these demanding criteria. Notable examples include EUROFER-97 ([Rieth et al., 2003](https://www.frontiersin.org#B52)), the European reference steel for fusion applications; F82H ([Serra and Benamati, 1998](https://www.frontiersin.org#B57)), developed in Japan and extensively used as a benchmark in irradiation studies; CLAM ([Huang, 2017](https://www.frontiersin.org#B24)), the Chinese Low Activation Martensitic steel designed for future fusion reactors and RUSFER, a Russian-developed RAFM steel whose composition has been tailored to comply with low-activation guidelines, although its industrial qualification and irradiation database are still under development ([Arredondo et al., 2022](https://www.frontiersin.org#B4)).

These steels combine reduced activation behavior with good high-temperature strength, low swelling, and radiation resistance, making them strong candidates for structural components fusion machines. Nevertheless, their thermo-mechanical performance are not comparable to Nickel-based superalloys. While RAFM steels typically maintain good strength and toughness up to about 550 °C–600 °C, their creep resistance and tensile strength rapidly degrade at higher ([Kachko et al., 2022](https://www.frontiersin.org#B26)). By contrast, Ni-based superalloys exhibit superior high-temperature capability, retaining significant yield and ultimate tensile strength, as well as excellent creep resistance, well above 700 °C ([Perrut et al., 2018](https://www.frontiersin.org#B46)). This difference reflects the distinct strengthening mechanisms: solid-solution and precipitate hardening in Ni-based superalloys versus tempered martensitic microstructures in RAFM steels. As a result, RAFM steels are suitable for first-wall and blanket structures, but are generally not viable for components subjected to extreme thermal loads such as divertor or high-heat-flux structures.

### 3.3 High-strength martensitic steels (non-low activation)

High-strength martensitic steels represent a class of structural materials originally developed for advanced fission reactors and high-temperature applications, where excellent mechanical performance under irradiation is required. These steels typically exhibit high strength, good creep and fatigue resistance, and relatively low swelling under neutron flux, making them promising candidates for demanding structural roles in nuclear environments ([Lee et al., 2010](https://www.frontiersin.org#B36)).

A prominent example in this category is HT9, widely used in the context of fast reactors. HT9 has demonstrated robust performance under high-dose irradiation, with superior resistance to void swelling and good retention of mechanical properties at elevated temperatures. These characteristics make it attractive for use in fusion reactor components subjected to intense heat and stress, such as the first wall and blanket support structures ([Chen, 2013](https://www.frontiersin.org#B11)).

Other important alloys are G91 T1, G91 T2, and Steel 660, developed for high-temperature or fast reactor applications. G91 T1 and G91 T2 are martensitic steels derived from conventional Grade 91, offering good creep strength but containing activation-relevant elements such as Mo and Nb; the T2 variant undergoes a more advanced heat treatment aimed at improving long-term thermal stability and creep resistance ([Kim et al., 2014](https://www.frontiersin.org#B31)). Steel 660 (A286), a Fe–Ni–Cr-based superalloy, provides excellent high-temperature performance up to 700 °C, but its high Ni and Mo content results in significant long-lived activation ([Abdou and El-Derini, 1979](https://www.frontiersin.org#B1)).

However, these materials are not designed with reduced activation criteria in mind. Their composition often includes elements like Ni, Mo, and Nb, which upon neutron irradiation generate long-lived radioactive isotopes. As a result, despite their favorable mechanical properties, high-strength martensitic steels are generally associated with intermediate-level radioactive waste classification at end-of-life, posing challenges for remote handling, maintenance, and disposal ([Bailey et al., 2021](https://www.frontiersin.org#B8)).

Due to these activation concerns, high-strength martensitic steels are considered only for specific applications in fusion systems where low activation is not strictly required or where no better alternatives exist in terms of mechanical robustness.

### 3.4 Oxide-dispersion-strengthened (ODS) alloys

Oxide dispersion strengthened (ODS) alloys are considered promising candidates for irradiation environments due to their favorable mechanical properties and enhanced resistance to radiation damage. The dispersion of fine Y2O3 oxide particles in ODS steels has been demonstrated to play a critical role in maintaining mechanical performance and mitigating irradiation-induced swelling, primarily by acting as defect sinks and trapping radiation-induced defects ([El-Genk and Tournier, 2005](https://www.frontiersin.org#B18); [Ukai, 2012](https://www.frontiersin.org#B67)).

ODS steels, such as Eurofer ODS or CLAM-ODS, incorporate fine particles to enhance high-temperature mechanical properties and irradiation resistance. As low-activation materials, they represent a cutting-edge class of candidate materials for fusion blanket and VV applications, particularly where high creep strength and dimensional stability are required.

The dispersion of fine oxide particles in ODS steels has been demonstrated to play a critical role in maintaining mechanical performance and mitigating irradiation-induced swelling. In addition to , several other complex oxides have been identified in ODS alloys. For instance, in Al-containing ODS steels, Y–Al–O phases such as yttrium–aluminum perovskite (YAP, ), yttrium–aluminum garnet (YAG, ), and yttrium–aluminum monoclinic (YAM, ) have been reported to precipitate during processing, significantly influencing high-temperature strength and corrosion resistance ([Zhang et al., 2015](https://www.frontiersin.org#B69); [Stasiak et al., 2024](https://www.frontiersin.org#B64)). More recently, alloying additions such as Zr, Ti, or Hf have been employed to refine and stabilize the dispersion. In particular, the formation of Y–Zr–O (e.g., , ) and Y–Hf–O nanoparticles has been shown to suppress the coarsening of Y–Al–O particles and enhance tensile strength at elevated temperatures ([Ren et al., 2018](https://www.frontiersin.org#B50); [Dong et al., 2017](https://www.frontiersin.org#B15)). These findings suggest that the careful selection of oxide formers beyond can optimize the microstructure and improve the performance of ODS steels under fusion-relevant conditions.

Historically, the development of ODS alloys was strongly driven by fission applications, especially sodium fast reactors, where high creep rupture strength and swelling resistance were essential. More recently, dedicated programs have been launched for fusion and GEN-IV concepts, leading to the design of new Fe–13Cr and Fe–18Cr ferritic ODS steels with W and Ti additions ([De Carlan et al., 2009](https://www.frontiersin.org#B13)). These alloys exhibit body-centered cubic (bcc) structures, which are less prone to swelling than austenitic steels and can retain mechanical strength even above 1100 °C.

The fabrication of ODS alloys relies on mechanical alloying and consolidation techniques such as hot extrusion, which allow the dissolution of Y and O into solid solution and their re-precipitation as nanometric oxides during consolidation. This results in a homogeneous dispersion of nano-clusters below 10 nm, as confirmed by TEM investigations, and ensures excellent creep resistance, tensile strength and thermal stability ([De Carlan et al., 2009](https://www.frontiersin.org#B13)).

Despite these advantages, challenges remain for large-scale deployment: controlling oxide dispersion homogeneity, ensuring weldability and joinability, and expanding the irradiation database under 14 MeV neutron spectra are critical steps before full qualification. Current R&D activities, such as those led by CEA and European partners, are therefore focused on optimizing processing routes, improving anisotropy control, and conducting irradiation campaigns up to several tens of dpa to assess long-term behavior ([De Carlan et al., 2009](https://www.frontiersin.org#B13)).

### 3.5 SiC/SiC ceramic matrix composites (CMCs)

SiC/SiC composites are ceramic matrix composites consisting of silicon carbide (SiC) fibers, typically woven or braided, embedded within a SiC matrix. These materials are known for their excellent resistance to corrosion, thermal deformation, and fatigue.

The chemical composition of SiC/SiC composites varies depending on the specific types of fibers and matrix used. In general, the matrix is primarily composed of silicon carbide, with minor additions of other compounds such as aluminum oxide or nitrides. The SiC fibers themselves are typically made from silicon, carbon, and nitrogen.

SiC fiber-reinforced SiC matrix composites continue to be actively developed worldwide for fusion applications, due to their inherent advantages: low neutron activation, high-temperature capability, low neutron absorption, and good radiation resistance. The materials of particular interest are nuclear-grade SiC/SiC composites, which are fabricated using high-crystallinity, near-stoichiometric fibers such as Hi-Nicalon™ Type S or Tyrann™ SA, a highly crystalline SiC matrix, and carbon or multilayered carbon/SiC interphases. These composites are typically manufactured through chemical vapor infiltration (CVI) ([Katoh et al., 2014](https://www.frontiersin.org#B29)) and nano-infiltration transient eutectic phase (NITE) processes ([Katoh et al., 2002](https://www.frontiersin.org#B27)).

Nuclear-grade SiC/SiC composites have demonstrated excellent performance under neutron irradiation at elevated temperatures, particularly in terms of maintaining mechanical properties. For this reason, they are considered among the most promising candidate materials for structural components in fusion reactors.

Despite their numerous advantages, SiC/SiC composites still face several critical challenges that need to be addressed before their widespread implementation in fusion reactor environments. A deeper understanding of the effects of high-dose neutron irradiation and transmutation phenomena is essential, as these can significantly alter the microstructure and long-term performance of the material. In parallel, continued progress is required in the development of fabrication and joining technologies to enable reliable large-scale production of components with consistent quality. Furthermore, the chemical compatibility of SiC/SiC with potential coolants and breeder materials must be thoroughly evaluated to ensure material integrity during reactor operation.

### 3.6 Vanadium-based alloys

Vanadium-based alloys are considered promising structural candidates for nuclear fusion applications due to vanadium’s low activity, high thermal strength, and good resistance to radiation-induced swelling ([Sparks et al., 2022](https://www.frontiersin.org#B62)). Although the experimental database for these alloys is currently less extensive than that available for austenitic and ferritic steels, several intrinsic properties make them particularly attractive for the demanding environment of fusion energy systems.

V–4Cr–4Ti and V–15Cr–5Ti have demonstrated favorable thermo-mechanical and neutronic properties under harsh conditions, suggesting their applicability in FPPs. Their relatively low coefficient of thermal expansion and good thermal transport properties help reduce thermal stresses under intense heat loads, potentially extending component lifetime and improving wall-load tolerance. In addition, these alloys retain mechanical strength at elevated temperatures, enabling blanket operation beyond the limits of austenitic and ferritic steels ([Smith et al., 1985a](https://www.frontiersin.org#B59)).

Vanadium alloys are also inherently non-ferromagnetic and ductile, which distinguishes them from both SiC/SiC composites and RAFM steels, and makes them attractive for advanced reactor concepts with high magnetic fields. Due to their favorable compatibility with liquid metals, they have been proposed as the reference material in self-cooled Li/V blanket designs, where lithium serves both as a coolant and tritium breeder. One advantage of such configurations is the potential elimination of neutron multipliers like beryllium or lead, reducing both activation and safety concerns, and simplifying the structural design. However, these designs face major challenges such as Magnetohydrodynamic (MHD) -induced pressure drops and tritium recovery from liquid lithium ([Muroga et al., 2014](https://www.frontiersin.org#B43)).

A critical limitation associated with vanadium alloys is their high tritium solubility, which can lead to significant tritium inventory in in-vessel components, especially at high operating temperatures. This concern is further amplified by the nature of the coolant: while liquid lithium is relatively benign in terms of material compatibility and tritium inventory, it poses serious magnetohydrodynamic challenges and makes tritium extraction particularly complex. This is true for vanadium alloys, but not for many steels, where liquid lithium is highly reactive and can cause corrosion at high temperatures. Similarly, lithium is not inherently benign with respect to tritium inventory, as it can dissolve substantial amounts of tritium, particularly in its pure liquid form. Its main advantage lies instead in its high breeding capability rather than in reducing tritium retention.

In contrast, coolants such as Li–Pb, FLiBe, and helium introduce additional challenges including oxidation, corrosive attack, and nitridation, which demand robust corrosion protection strategies and permeation barriers to preserve structural integrity and enable efficient tritium management ([Muroga et al., 2014](https://www.frontiersin.org#B43)).

## 4 Modelling and analysis

### 4.1 Compact reactor model configuration

To enable a systematic and reproducible assessment of structural materials for fusion applications, a simplified yet representative Constructive Solid Geometry (CSG) is developed. The model captures the essential features of a compact fusion reactor while preserving computational tractability, making it suitable for extensive parametric analyses.

The model is developed in OpenMC ([Romano et al., 2015](https://www.frontiersin.org#B53)) to perform both neutron transport and activation analyses. For these simulations, nuclear data from the ENDF/B-VIII.0 Evaluated Nuclear Data Library ([Conlin et al., 2018](https://www.frontiersin.org#B12)) are employed to ensure consistency and reliability across all evaluated metrics.

The simulation domain is composed of a series of discrete layers, each representing a functional region of the machine, such as plasma-facing components, tritium breeder zones, structural materials, and shielding, using an ARC-like configuration as baseline. The layered geometry approximates the radial structure of an actual ARC-like design while maintaining geometric simplicity.

The simulation adopts a geometry from the repository ([Segantin, 2023](https://www.frontiersin.org#B55)), which provides a reasonably optimized configuration. A 50 cm thick breeding blanket ensures an adequate TBR, while a 30 cm shielding layer was added to effectively attenuate the remaining neutron flux.

The overall geometry is illustrated in [Figure 2](https://www.frontiersin.org#F2), which highlights the spatial arrangement and symmetry of the model. Further geometric and material specific details, including the thickness and total volume of each region are summarized in [Table 2](https://www.frontiersin.org#T2).

FIGURE 2

TABLE 2

| Region | Thickness [cm] | Volume [m3] | Material |
|---|---|---|---|
| First wall | 1.0 | 2.23 | Tungsten |
| Inner structural material | 1.5 | 3.37 | Candidate structural material |
| Cooling channel | 2.0 | 4.55 | FLiBe |
| Neutron multiplier | 1.0 | 2.29 | Beryllium |
| Outer structural material | 3.0 | 6.96 | Candidate structural material |
| Blanket | 50.0 | 133.29 | FLiBe |
| Shield | 30.0 | 95.31 | Boron carbide |

Geometric and material specifications of each region in the CSG model.

Six structural materials were selected for detailed analysis, each representative of one of the main families discussed in the previous sections and chosen based on their maximum operating temperature, which is compatible with the high-temperature environment of an ARC-like fusion reactor. Inconel 718 was chosen as a well-known high-performance alloy with proven mechanical strength and corrosion resistance at elevated temperatures ([Sorbom et al., 2015](https://www.frontiersin.org#B61)). For the class of Reduced Activation Ferritic/Martensitic (RAFM) steels, the Russian-developed RUSFER (EK-181) was selected due to its advanced development status and relevance within DEMO-oriented studies ([Bachurina et al., 2018](https://www.frontiersin.org#B6)). As a representative of high-strength martensitic steels, HT9 was included owing to its widespread use in fast reactors and its robustness under neutron irradiation ([Chen, 2013](https://www.frontiersin.org#B11)). For the oxide dispersion strengthened (ODS) steels, ODS-EUROFER was selected due to its enhanced creep strength and radiation resistance ([Zilnyk et al., 2015](https://www.frontiersin.org#B71)). The SiC/SiC composite was considered in its standard nuclear-grade formulation, offering superior high-temperature and low-activation properties ([Koyanagi et al., 2018](https://www.frontiersin.org#B33)). Finally, for the family of vanadium-based alloys, the well-characterized V–4Cr–4Ti was selected, thanks to its low neutron activation, good compatibility with liquid breeders, and promising performance under high heat fluxes ([Smith et al., 1985a](https://www.frontiersin.org#B59)).

The developed model allows for a systematic comparison of structural materials based on their DPA values, activation behavior, and neutronic indicators including TBR, EM, power deposition and light gases growth. The chemical compositions of all tested materials, summarized in [Table 3](https://www.frontiersin.org#T3), are taken from the literature ([McConn et al., 2011](https://www.frontiersin.org#B38); [Sparks et al., 2022](https://www.frontiersin.org#B62); [Zilnyk et al., 2015](https://www.frontiersin.org#B71); [Arredondo et al., 2022](https://www.frontiersin.org#B4)).

TABLE 3

| Element | Inconel 718
a |
|---|


b

a

c

a

d3]Chemical composition (wt%) of the candidate structural materials evaluated in the model.


aSource: [McConn et al. (2011)](https://www.frontiersin.org#B38).


bSource: [Arredondo et al. (2022)](https://www.frontiersin.org#B4).


cSource: [Zilnyk et al. (2015)](https://www.frontiersin.org#B71).


dSource: [Sparks et al. (2022)](https://www.frontiersin.org#B62).

### 4.2 Neutronics and activation simulations

The simulation model is designed to assess neutronic and activation-related phenomena in a compact fusion reactor configuration. The neutron source mimics D–T fusion conditions through a Muir energy Gaussian spectrum centered at 14.08 MeV. Emission is confined within a 10° cone, reflecting the fact that only a 20° toroidal segment of the machine was modeled, leveraging geometric symmetry to reduce computational cost. Neutron emission is isotropic within this sector, spanning the full solid angle. The source is spatially distributed along a circular ring of 285 cm radius located in the x–y plane at z = 0 cm. Photon transport is explicitly enabled to account for gamma-induced heating and photonic interactions in structural materials. The simulation is carried out in fixed source mode.

The source, similarly to that adopted in [Pettinari et al. (2024)](https://www.frontiersin.org#B47), [Ledda et al. (2024)](https://www.frontiersin.org#B35), was calibrated for a machine with a fusion power of 525 MW. This corresponds to a total neutron production rate of approximately , assuming D–T fusion conditions. The simulations reproduced operation at full power for 1 year.

The model includes a comprehensive tally configuration that enables the calculation of several key performance indicators for fusion blanket and structural materials. To assess the impact of structural materials on both global reactor performance and local irradiation behavior, the neutronic simulation has been designed to extract two complementary sets of metrics. On the one hand, system-level indicators, such as the tritium breeding ratio (TBR) and the energy multiplication factor (EM), are evaluated to capture the influence of the structural material on fundamental breeding and energy recovery processes. On the other hand, local, material-specific quantities, including neutron absorption rates, energy deposition, displacement per atom and shutdown dose rate, are specifically tallied within the structural regions to characterize their response under irradiation. This twofold approach enables both a global understanding of material influence on reactor performance and a detailed evaluation of their suitability for in-vessel application.

The TBR is evaluated by tracking (n,Xt) reactions on lithium isotopes (Li-6 and Li-7) within the breeding and coolant regions, with additional energy-resolved tallies to capture spectral dependence. The EM represents the ratio between the total energy deposited within the system and the initial energy released by the primary fusion neutrons. This metric provides an indication of how efficiently neutron energy is converted into heat inside the reactor, also accounting for secondary contributions such as photon interactions from radiative capture or inelastic scattering. Absorption reactions are recorded to evaluate neutron attenuation and assess the shielding effectiveness of different structural materials. In this context, the *total absorption rate* refers to all neutron-induced reactions that do not lead to the emission of secondary neutrons—this includes capture, (n,), (n,p), and other non-multiplicative channels. By quantifying these reactions, one can estimate the extent to which each material contributes to reducing the neutron flux and identify potential candidates for structural components with improved shielding characteristics. Neutron spectra are tallied using the CCFE-709 group structure in inner vacuum vessel region to investigate energy shifts, flux degradation, and how these spectral features vary depending on the structural material employed. Energy deposition is further resolved by particle type (neutrons, photons, electrons, and positrons) to evaluate the respective contribution to heating. DPA are calculated using damage-energy tallies and the NRT (Norgett-Robinson-Torrens) model ([Norgett et al., 1975](https://www.frontiersin.org#B44)), in order to estimate the level of irradiation-induced damage in structural components. The calculation procedure is described in [Pettinari et al. (2024)](https://www.frontiersin.org#B47). This quantity serves as a fundamental indicator of material degradation under neutron exposure, as it quantifies the number of atomic displacements per target atom and is directly linked to changes in microstructural stability, mechanical integrity, and long-term performance of structural materials in fusion environments. Finally, the production of gases within structural materials was assessed, with a particular focus on the accumulation of hydrogen (H) and helium (He) under neutron irradiation. These gases, primarily generated through (n,p) (n,), reactions or via transmutation of light impurities, are among the key mechanisms driving microstructural degradation in components exposed to high-energy neutrons—such as those found in fusion reactor blankets and vacuum vessels.

Helium is predominantly generated in structural materials through transmutation reactions during neutron irradiation. Being virtually insoluble in metals, tends to precipitate and form gas bubbles along grain boundaries and interfaces. This process promotes swelling and contributes to intergranular embrittlement by reducing grain cohesion and increasing the material’s susceptibility to cracking under mechanical stress ([Schroeder, 1983](https://www.frontiersin.org#B54)). A critical aspect highlighted by experimental studies is that helium atoms do not remain uniformly distributed in the lattice: instead, they preferentially migrate towards microstructural sinks such as dislocations, dislocation networks, and grain boundaries, where they nucleate bubbles. Transmission electron microscopy observations confirm that bubble nucleation is strongly favored at dislocation nodes and grain boundary steps, where stress fields enhance helium trapping and accelerate bubble growth compared to the surrounding matrix ([Singh et al., 1984](https://www.frontiersin.org#B58)). The presence of such bubbles at extended defects not only increases local swelling but also severely impairs dislocation mobility, thereby reducing creep resistance and promoting premature embrittlement of irradiated alloys.

Hydrogen, on the other hand, can induce blistering through subsurface bubble formation and enhances corrosion phenomena, particularly in aqueous or humid environments ([Sznajder et al., 2018](https://www.frontiersin.org#B65)). Additionally, hydrogen embrittlement significantly lowers both the ductility and fracture toughness of the material.

Overall, the accumulation of H and He severely impairs the material’s resistance to plastic deformation, cyclic fatigue, and creep, thereby compromising long-term performance. These effects compound with DPA, making gas production a critical factor in the functional degradation of materials under fusion-relevant conditions. For this reason, the use of low-activation materials such as Eurofer, ODS-Eurofer, SiC/SiC and vanadium-base alloys is especially advantageous, as these materials are specifically engineered to limit gas production during neutron irradiation.

In addition, OpenMC includes a built-in capability for performing shutdown dose rate calculations via the direct 1-step (D1S) method ([Valenza et al., 2001](https://www.frontiersin.org#B68); [Eade et al., 2022](https://www.frontiersin.org#B16)). This approach replaces prompt photon emission with photons originating from the radioactive decay of nuclides produced during irradiation, enabling an efficient estimation of post-shutdown gamma fields. The same coupled neutron–photon transport framework is used, making the method particularly suitable for integration with the current model setup. Using this method, the most impactful transmutation products generated in each structural material are identified, and the time evolution of the shutdown dose rate is evaluated following 1 year of full-power irradiation. This analysis enables a comparative assessment of the radiological hazard posed by each material in the post-shutdown phase, providing insight into waste classification requirements.

## 5 Results

### 5.1 TBR and EM

The first aspect investigated is the impact of different structural materials on the neutronic performance of the reactor, assessed through the TBR. In the present model, the breeding material consists of molten (FLiBe) enriched to 90% in 6Li.

[Table 4](https://www.frontiersin.org#T4) reports the TBR contributions for the structural materials under evaluation, distinguishing between tritium production in the cooling channel and blanket regions. The total TBR remains above 1 for all cases, indicating that each configuration achieves net tritium production, an essential requirement for fuel self-sufficiency in fusion systems.

TABLE 4

| Material | TBR total | Channel (6Li – 7Li) | Blanket (6Li – 7Li) | EM factor |
|---|---|---|---|---|
FLiBe (enr. 90% 6Li) | ||||
| Inconel 718 | 1.1073 | 0.2851–0.0016 | 0.8149–0.0057 | 1.1463 |
| RUSFER | 1.1513 | 0.2781–0.0017 | 0.8652–0.0063 | 1.1471 |
| HT9 | 1.2130 | 0.2923–0.0016 | 0.9133–0.0058 | 1.1637 |
| ODS-EUROFER | 1.2138 | 0.2890–0.0016 | 0.9173–0.0059 | 1.1638 |
| SiC/SiC | 1.1021 | 0.2421–0.0018 | 0.8508–0.0074 | 1.1264 |
| V-4Cr-4Ti | 1.2588 | 0.3159–0.0017 | 0.9346–0.0066 | 1.1632 |
| FLiBe (natural Li) | ||||
| Inconel 718 | 0.9071 | 0.0959–0.0146 | 0.7410–0.0556 | 1.1747 |
| RUSFER | 0.9708 | 0.1078–0.0147 | 0.7915–0.0568 | 1.1669 |
| HT9 | 1.0384 | 0.1092–0.0146 | 0.8584–0.0562 | 1.1844 |
| ODS-EUROFER | 1.0125 | 0.0982–0.0147 | 0.8426–0.0570 | 1.1840 |
| SiC/SiC | 0.9977 | 0.1006–0.0169 | 0.8076–0.0723 | 1.1338 |
| V-4Cr-4Ti | 1.0826 | 0.1078–0.0155 | 0.8949–0.0644 | 1.1851 |

Summary of tritium breeding performance and energy multiplication for different structural materials, including isotopic contributions from 6Li and 7Li.

Among the tested options, the vanadium alloy V-4Cr-4Ti achieves the highest TBR value, followed by ODS-Eurofer and HT9. Conversely, SiC/SiC yields the lowest total TBR. Although this material enhances the contribution from 7Li due to its transparency to high-energy neutrons, it reduces interactions with 6Li, by far the dominant isotope in the breeder, and thus results in a lower overall TBR. This is because the 6Li(n,t)4He reaction has a high cross section at neutron energies below 1MeV; in a SiC/SiC configuration, many neutrons retain higher energies as they traverse the structure, reducing the likelihood of interacting with 6Li and thus lowering the overall breeding performance.

Partial contributions show that 6Li breeding in the blanket is the main source of tritium, with values ranging from approximately 0.81–0.93, depending on the structural material. Again, V-4Cr-4Ti exhibits the most effective performance, while Inconel 718 gives the lowest blanket contribution. In addition, 6Li breeding in the channel region contributes between 0.22421 and 0.3159, with V-4Cr-4Ti again exhibiting the highest effectiveness. SiC/SiC consistently provides the lowest contributions from both regions.

The contribution from 7Li, both in the channel and blanket is smaller but not negligible. Channel values are generally around 0.0016–0.0018, while blanket values range from 0.0057 to 0.0074. Notably, SiC/SiC shows the highest 7Li contribution in the blanket, likely due to increased neutron penetration and subsequent activation of (n,t) reactions on 7Li.

In addition to the TBR, [Table 4](https://www.frontiersin.org#T4) also includes the EM. The results obtained for the different structural materials range from 1.1264 for SiC/SiC to 1.1638 for ODS-EUROFER, with differences of a few percentage points that remain relevant for the overall energy efficiency of the system. In particular, materials such as ODS-EUROFER, HT9, and V-4Cr-4Ti exhibit the highest EM values, indicating a greater capacity for energy multiplication. Conversely, SiC/SiC shows the lowest performance in this respect, likely due to its ceramic composition, which limits inelastic interactions with high-energy neutrons.

The EM factor is influenced by a variety of nuclear interactions. These include inelastic scattering reactions, where high-energy neutrons excite atomic nuclei in structural materials, leading to the emission of gamma rays that contribute to local energy deposition. Other important interactions are radiative captures followed by gamma emission, and, most importantly, exothermic (n,x) reactions involving specific nuclides present in the blanket region.

A key contributor to EM enhancement is the exothermic reaction6. Materials that either contain or are in close proximity to lithium-rich zones can indirectly benefit from this contribution. Additionally, heavy elements such as iron, chromium, and tungsten—typically found in ferritic-martensitic steels—exhibit significant inelastic scattering cross sections, which also contribute to local energy deposition.

In contrast, ceramic materials like SiC/SiC are composed of light elements with low inelastic scattering cross sections and do not participate in exothermic nuclear reactions with fast neutrons. As a result, their contribution to the EM factor is limited, leading to the lower values observed in the simulations.

When FLiBe with natural lithium is used as the breeding material, all structural materials exhibit a notable reduction in TBR values compared to the configuration. This drop is expected due to the significantly lower abundance (approximately ) in natural lithium, which reduces the occurrence of the reaction.

Despite the lower breeding performance, some structural materials retain relatively better TBR values. In particular, V–4Cr–4Ti shows the highest TBR (1.0826), followed by HT9 and ODS-EUROFER. These materials tend to have favorable neutron moderation and reflection properties that help maintain a sufficient thermal neutron population within the blanket. On the other hand, SiC/SiC, provides the lowest TBR (0.9977), likely due to its limited contribution to neutron slowing-down and its lower structural density.

The EM factor remains increases slightly in the natural lithium configuration. This is largely due to a higher contribution from 7 and other inelastic interactions, as well as the increased presence of radiative captures and neutron scattering events in the structural materials. Notably, the EM values for HT9 (1.1844), V–4Cr–4Ti (1.1851), and ODS-EUROFER (1.1840) are the highest among the group, highlighting their capacity to support local energy deposition through neutron interactions. In contrast, SiC/SiC again shows the lowest EM (1.1338), consistent with its limited nuclear interaction cross sections and lack of contribution to exothermic reactions.

### 5.2 Structural material response analysis

This section presents the neutronic results evaluated exclusively within the regions occupied by the structural material. These components are located in two distinct areas of the system: the inner and outer vacuum vessel. Since the inner VV is positioned closer to the plasma source, it is exposed to a significantly higher neutron flux compared to the outer region. For this reason, the analysis focuses on the inner vacuum vessel, where four key parameters are examined: the mean neutron flux, the deposited power density, the neutron absorption rate, and the DPA.

[Table 5](https://www.frontiersin.org#T5) summarizes the results for each structural material. Neutron flux values are relatively similar across the materials, with minor differences due to variations in moderation and scattering behavior. Notably, HT9 and ODS-Eurofer exhibit the highest flux levels, while SiC/SiC records the lowest.

TABLE 5

| Material | Neutron flux [n/cm2/s] | Absorption rate | Power density [MW/m3] | DPA |
|---|---|---|---|---|
| Inconel 718 | 0.066 | 12.89 | 14.09 | |
| RUSFER | 0.045 | 10.68 | 13.45 | |
| HT9 | 0.027 | 10.78 | 12.51 | |
| ODS-EUROFER | 0.028 | 10.73 | 12.68 | |
| SiC/SiC | 0.049 | 8.76 | 16.64 | |
| V-4Cr-4Ti | 0.019 | 7.58 | 15.02 |

Neutronic response parameters calculated in the inner vacuum vessel for each structural material: mean neutron flux, neutron absorption rate, deposited power density, and displacements per atom (DPA).

In terms of absorption rate, Inconel 718 shows the highest neutron capture, followed by SiC/SiC and RUSFER. V-4Cr-4Ti and HT9 have the lowest absorption values, reflecting their relatively low capture cross sections. The high absorption rate observed in Inconel 718 is primarily due to the presence of elements such as molybdenum, iron, niobium and nickel, which exhibit relatively high neutron capture cross sections. In contrast, materials like V–4Cr–4Ti and HT9 contain vanadium, chromium, and titanium—elements characterized by low absorption cross sections—leading to lower overall neutron capture.

The elevated absorption rate observed in Inconel 718 can be attributed not only to the presence of elements with intrinsically high capture cross sections, but also to the presence in Ni and Nb of strong resonance peaks in the intermediate neutron energy range (100 keV–10 MeV). These resonance structures significantly enhance the probability of neutron capture in fusion spectra dominated by high-energy neutrons.

A similar trend is observed for the deposited power density, which is highest in Inconel 718 (12.89 MW/m3) and lowest in V-4Cr-4Ti (7.58 MW/m3). This huge difference among the structural materials entails different requirements and design of the primary cooling system.

Regarding DPA, the highest values are found in SiC/SiC (DPA = 16.64) and V-4Cr-4Ti (DPA = 15.02), indicating greater susceptibility to atomic displacement damage under irradiation. Conversely, HT9 (DPA = 12.51) and ODS-Eurofer (DPA = 12.68) show the lowest DPA levels, suggesting better mechanical stability in harsh neutron environments. However, the difference is not so huge to suggest different behaviors in long-term operations of FPPs.

These results highlight the trade-offs involved in material selection: while some materials offer better shielding, reduced-activation, or power generation, others excel in radiation tolerance.

[Table 6](https://www.frontiersin.org#T6) summarizes the total hydrogen and helium production rates for the investigated structural materials, expressed in atoms per source neutron. Significant variations are observed across the different alloys, reflecting the strong dependence of gas production on the elemental composition and neutron-induced transmutation pathways.

TABLE 6

| Material | H [atoms/source neutron] | He [atoms/source neutron] |
|---|---|---|
| Inconel 718 | ||
| RUSFER | ||
| HT9 | ||
| ODS-Eurofer | ||
| SiC/SiC | ||
| V-4Cr-4Ti |

Total production rate of hydrogen and helium for the investigated structural materials.

Inconel 718 exhibits the highest total production rates for both hydrogen and helium, which is consistent with its high nickel and niobium content—elements known to enhance gas-generating (n,) and (n,p) reactions under fusion-relevant neutron spectra. Conversely, the reduced-activation ferritic-martensitic alloy V-4Cr-4Ti shows the lowest production values for both gases, confirming its favorable behavior in terms of gas-induced damage mitigation.

Interestingly, ODS-Eurofer and HT9 also display relatively low gas production, with He and H values significantly below those of Inconel and RUSFER, suggesting that optimized RAFM steels can offer a suitable balance between mechanical robustness and radiation tolerance. On the other hand, SiC/SiC, while a ceramic composite with excellent irradiation resistance and thermal properties, shows a markedly high helium production rate. This outcome stems from the presence of light elements like carbon and silicon, which contribute to gas generation through (n,) and (n,p) reactions.

These findings confirm that helium and hydrogen production in structural materials is not only sensitive to the neutron energy spectrum but also strongly governed by nuclear transmutation processes that depend on the material’s elemental makeup.

To complete the neutronic assessment of structural materials, an activation analysis has been performed, focusing on the evaluation of the shutdown dose rate. The shutdown dose rate is the product of decay gammas emitted by the radioactive nuclides generated during neutron irradiation. This parameter is crucial for understanding the radiological behavior of materials after reactor shutdown, and it plays a key role in defining the feasibility of maintenance, remote handling, and recycling strategies for reactor components.

Results are presented in terms of the maximum dose rate (in Sv/h) for each material, evaluated as a function of cooling time. [Figure 3](https://www.frontiersin.org#F3) shows the decay profile for all tested structural materials over a time span ranging from 1 s to 200 years.

FIGURE 3

Among the analyzed materials, SiC/SiC and ODS-EUROFER demonstrate the most favorable decay behavior, with their dose rates falling below the natural background threshold ([Segantin et al., 2020](https://www.frontiersin.org#B56)) in less than 50 years. This is a critical feature for waste minimization and long-term safety, as it implies these materials may qualify for out-of-plant recycling or clearance after relatively short cooling times compared to others.

V-4Cr-4Ti shows a dose rate that decreases more rapidly than that of traditional steels, such as Inconel 718, RUSFER, and HT9, but remains above natural background even after 200 years. This indicates the presence of long-lived activation products—most notably 10Be and 50V—which may complicate long-term disposal.

RUSFER and HT9 display intermediate decay profiles, with SDRs remaining several orders of magnitude above clearance levels over most of the evaluated timescale, implying the need for extended shielding or long-term storage. However, it is worth noting that after approximately 50 years, RUSFER begins to decay more rapidly than V-4Cr-4Ti, eventually reaching lower dose rate values at longer cooling times. This trend suggests a relatively favorable long-term activation behavior, which could be beneficial from a waste classification and decommissioning perspective.

Inconel 718, in contrast, exhibits the slowest decay, with dose rates persistently elevated throughout the 200-year window. This poor activation behavior, combined with its medium-high DPA and modest tritium breeding performance, confirms its limited suitability for fusion applications from a radiological standpoint.

Across all materials examined, the isotope 180W emerges consistently as a dominant contributor due to its extremely long half-life (25 years). Similarly, 50V, with a half-life on the order of 1024 years, is present in most vanadium- and steel-based alloys, and represents a persistent component of the radioactive inventory even at long cooling times.

Inconel 718 and HT9 exhibit the presence of 92Nb (T1/213 years), which forms via neutron capture on stable niobium and contributes to sustained gamma emissions over extended decay periods. HT9, ODS-Eurofer and RUSFER generate 53Mn, a radionuclide with a half-life of 15 s, which although not extremely long-lived compared to transuranics, remains relevant within the operational and intermediate-term radiological timeline.

In ceramic-based materials like SiC/SiC and vanadium-rich alloys such as V-4Cr-4Ti, 10Be and 14C appear as activation products. While 10Be (T1/212 s) decays via beta emission and can pose radiological challenges, 14C is a well-known low-energy beta emitter with significant implications for long-term environmental mobility and radioprotection.

Overall, the inventory of long-lived nuclides highlights the need to carefully evaluate structural materials not only for their neutronic and mechanical properties, but also for their activation behavior. Materials that minimize the production of high-energy gamma emitters and radiotoxic isotopes with long half-lives are preferable for reducing the post-shutdown radiological hazard and enabling more flexible handling and disposal strategies.

## 6 Discussion

To facilitate a global comparison of the structural materials evaluated, a normalized heatmap is presented in [Figure 4](https://www.frontiersin.org#F4). The plot includes five key neutronic parameters, DPA, energy multiplication factor, absorption rate, TBR, and power density, each scaled from 0 to 1 to allow direct visual comparison.

FIGURE 4

Higher normalized values indicate materials that better meet the desired criteria for application in fusion reactors, whereas lower values reflect poorer performance relative to other candidates. The normalization procedure follows a min–max approach for metrics where higher values are favorable (EM, absorption, TBR), and is inverted for those where lower values are desirable—namely, DPA, power density and hydrogen and helium production. The first two parameters are associated with radiation damage and thermal loading, respectively; thus, materials with lower DPA values exhibit greater resistance to displacement damage, while reduced power density implies lower heat deposition and potentially more manageable thermal stresses. Similarly, low hydrogen and helium production is a desirable feature, as the accumulation of these gases in structural materials under neutron irradiation is a key driver of swelling, blistering, and embrittlement.

V-4Cr-4Ti emerges as the top performer, achieving a perfect score in TBR, power density, gas production rate and near-unity in EM, indicating a highly balanced profile across all neutronic criteria. HT9 and ODS-EUROFER also show strong overall performance, particularly in EM and absorption rate, although HT9 benefits from slightly better DPA.

RUSFER, the RAFM steel alternative, achieves a moderate average score but performs consistently across all metrics without major weaknesses, suggesting it remains a well-rounded candidate.

Inconel 718, despite its excellent absorption rate, ranks lower due to its relatively high DPA and poor TBR, which limit its potential in fusion applications where low activation and high TBR are essential.

SiC/SiC exhibits a mixed performance across the evaluated metrics. On one hand, it shows high normalized values in absorption rate and power density, indicating strong local energy deposition and neutron interaction. On the other hand, it records the lowest scores in energy multiplication (EM), tritium breeding ratio (TBR), and DPA.

Taking into account the shutdown dose rate trends alongside the neutronic performance metrics, ODS-Eurofer emerges as the most promising structural material, offering a favorable balance between low activation and strong neutronic behavior. V-4Cr-4Ti ranks second, showing good overall performance despite its persistent long-term activity. Conversely, although SiC/SiC displays exceptionally low activation levels, its neutronic performance is significantly limited, particularly in terms of energy multiplication and tritium breeding potential, which undermines its viability as a primary structural candidate.

Based on the obtained results, it is also important to compare the shutdown dose rate of the investigated materials. From a neutronic standpoint, the best-performing alloys among those analyzed are V-4Cr-4Ti, ODS-Eurofer, and HT9. However, from an activation perspective, the vanadium alloy fails to reach the level of natural background radiation even after 200 years from the end of irradiation. In contrast, both SiC/SiC and ODS-Eurofer achieve this threshold, highlighting their superior long-term radiological behavior.

Although it does not reach the natural background level, the V-4Cr-4Ti alloy can still be classified as a low-activation material when compared with austenitic stainless steels and high-strength martensitic steels. RUSFER ranks as the third-best alloy in terms of residual dose levels.

Beyond normalized comparisons, additional differences emerge in absolute values. Over the reference irradiation period, DPA values ranged from 12.64 for HT9 and ODS-Eurofer to 16.64 for SiC/SiC. Such a variation is not expected to be critical from an engineering standpoint, as materials capable of tolerating the lower value are likely to withstand the higher as well. Power density shows one of the most significant spreads, with differences of up to a factor of two between materials. Nonetheless, all candidates achieve values consistent with those reported in the literature ([Bae et al., 2022](https://www.frontiersin.org#B7); [Pettinari et al., 2024](https://www.frontiersin.org#B47)) for advanced fusion blanket concepts, suggesting that adequate heat removal can be ensured with appropriately designed cooling systems.

Another key aspect is light gas production. V-4Cr-4Ti, ODS-Eurofer, and HT9 exhibit the lowest hydrogen and helium generation rates, reducing the risk of swelling, blistering, and embrittlement under prolonged irradiation, while Inconel 718 and SiC/SiC display significantly higher values, which may impact long-term microstructural stability. In particular, SiC/SiC exhibits a helium production rate approximately seven times higher than that of Inconel 718, which itself shows values about one order of magnitude greater than those of the V-4Cr-4Ti alloy. Regarding hydrogen production, Inconel 718 performs the worst among the evaluated alloys, generating roughly seven times more hydrogen than V-4Cr-4Ti. RUSFER also displays a relatively high hydrogen yield, with values about five times greater than those observed for V-4Cr-4Ti.

Overall, the combination of neutronic performance, shutdown dose rate, and detailed assessments of gas production highlights ODS-Eurofer and V-4Cr-4Ti as the strongest candidates, albeit with distinct trade-offs between long-term radiological behavior and high-temperature neutronic performance.

### 6.1 Technological maturity of structural materials

When assessing the viability of candidate structural materials for future fusion reactors, it is essential to consider not only their neutronic behavior and activation profile, but also their technological maturity. While assigning a precise TRL (Technology Readiness Level) score to each material is challenging, some general trends can still be outlined.

Within this section, we attempt to offer a qualitative evaluation of the TRL of each material, based on its adoption in existing or planned fusion devices, its industrial readiness, and the extent of experimental validation under fusion-relevant conditions. At the same time, we highlight the major technical bottlenecks that currently limit their development and integration, which could lead to significant progress in the field of structural materials for fusion.

Most candidate materials are being tested in isolated components or mock-ups rather than in integrated, reactor-like environments. This is particularly true for those materials derived from fission experience (Inconel 718, HT9) which benefit from established manufacturing and qualification pathways, but may face issues under the harsher conditions of fusion. On the other hand, more advanced low-activation materials (SiC/SiC, ODS-Eurofer, V-4Cr-4Ti) are still under intense research, with various challenges delaying their full deployment ([Katoh et al., 2007](https://www.frontiersin.org#B28); [McGuiness et al., 2025](https://www.frontiersin.org#B39)).

RUSFER occupies an intermediate position: although it shares design principles with more established materials like EUROFER, its technology readiness level remains lower due to a limited experimental database and reduced industrial validation.

## 7 Conclusion

This study underscores the multifaceted nature of structural material selection for fusion reactors, where neutronic performance, activation behavior, and technological maturity must all be carefully balanced.

Among the candidates, ODS-Eurofer emerges as the most promising option for compact, high-temperature devices, offering a favorable compromise between low activation, radiation resistance, and tritium breeding capability. Vanadium-based alloys such as V-4Cr-4Ti also demonstrate an excellent overall profile, with very favorable neutronic properties and comparatively low activation.

By contrast, high-performance alloys containing elements such as Ni, Mo, and Nb, while mechanically robust and temperature-resistant, generate significant inventories of long-lived activation products under neutron irradiation. This complicates decommissioning and long-term waste management, making activation analysis a crucial step not only for operational safety but also for end-of-life planning. Integrating waste minimization and decontamination strategies into the design phase is therefore essential for enabling practical deployment of fusion power systems.

Overall, no single material is optimal across all criteria. The findings emphasize the need for application-specific trade-offs and the further qualification of low-activation materials under fusion-relevant conditions, with particular attention to long-term mechanical integrity, gas production, and manufacturability.

It should be noted that the present analysis did not explicitly account for microstructural effects (e.g., grain size, dislocation density, precipitate distributions), which are known to influence irradiation resistance. Addressing these aspects would require a different modelling approach and is identified as a valuable direction for future coupled neutronic–mechanical studies.

## Statements

### Data availability statement

The raw data supporting the conclusions of this article will be made available by the authors, without undue reservation.

### Author contributions

DP: Writing – review and editing, Formal Analysis, Writing – original draft, Conceptualization, Methodology, Visualization, Data curation, Investigation. SM: Writing – review and editing, Supervision, Visualization, Data curation. RT: Writing – review and editing, Supervision.

### Funding

The author(s) declare that financial support was received for the research and/or publication of this article. The work of Davide Pettinari is part of the project PNRR-NGEU which has received funding from the MUR–DM 352/2022 and his PhD scholarship is co-funded by Eni S.p.A.The funder was not involved in the study design, collection, analysis, interpretation of data, the writing of this article, or the decision to submit it for publication.

### Acknowledgments

Support from CINECA for high-performance computing is acknowledged.

### Conflict of interest

The authors declare that the research was conducted in the absence of any commercial or financial relationships that could be construed as a potential conflict of interest.

### Generative AI statement

The author(s) declare that no Generative AI was used in the creation of this manuscript.

Any alternative text (alt text) provided alongside figures in this article has been generated by Frontiers with the support of artificial intelligence and reasonable efforts have been made to ensure accuracy, including review by the authors wherever possible. If you identify any issues, please contact us.

### Publisher’s note

All claims expressed in this article are solely those of the authors and do not necessarily represent those of their affiliated organizations, or those of the publisher, the editors and the reviewers. Any product that may be evaluated in this article, or claim that may be made by its manufacturer, is not guaranteed or endorsed by the publisher.

## References

1

AbdouM. A.El-DeriniZ. (1979). A comparative study of the performance and economics of advanced and conventional structural materials in fusion systems.

*J. Nucl. Mater.*85, 57–64. 10.1016/0022-3115(79)90469-02

AlbaR.IglesiasR.CerdeiraM. Á. (2022). Materials to be used in future magnetic confinement fusion reactors: a review.

*Materials*15, 6591. 10.3390/ma151965913

ArenaP.BongiovìG.CatanzaroI.CiurluiniC.CollakuA.Del NevoA.et al (2023). Design and integration of the eu-demo water-cooled lead lithium breeding blanket.

*Energies*16, 2069. 10.3390/en160420694

ArredondoR.BaldenM.Schwarz-SelingerT.HöschenT.DürbeckT.HungerK.et al (2022). Comparison experiment on the sputtering of eurofer, rusfer and clam steels by deuterium ions.

*Nucl. Mater. Energy*30, 101118. 10.1016/j.nme.2022.1011185

AubertJ.AielloG.ArenaP.BarrettT.BoccacciniL. V.BongiovìG.et al (2018). Status of the eu demo hcll breeding blanket design development.

*Fusion Eng. Des.*136, 1428–1432. 10.1016/j.fusengdes.2018.04.1336

BachurinaD.SuchkovA.KalinB.SevriukovO.FedotovI.DzhumaevP.et al (2018). Joining of tungsten with low-activation ferritic–martensitic steel and vanadium alloys for demo reactor.

*Nucl. Mater. Energy*15, 135–142. 10.1016/j.nme.2018.03.0107

BaeJ. W.PetersonE.ShimwellJ. (2022). Arc reactor neutronics multi-code validation.

*Nucl. Fusion*62, 066016. 10.1088/1741-4326/ac54508

BaileyG.VilkhivskayaO.GilbertM. (2021). Waste expectations of fusion steels under current waste repository criteria.

*Nucl. Fusion*61, 036010. 10.1088/1741-4326/abc9339

BoccacciniL.ArbeiterF.ArenaP.AubertJ.BühlerL.CristescuI.et al (2022). Status of maturation of critical technologies and systems design: breeding blanket.

*Fusion Eng. Des.*179, 113116. 10.1016/j.fusengdes.2022.11311610

BoltH.BarabashV.KraussW.LinkeJ.NeuR.SuzukiS.et al (2004). Materials for the plasma-facing components of fusion reactors.

*J. Nucl. Mater.*329, 66–73. 10.1016/j.jnucmat.2004.04.00511

ChenY. (2013). Irradiation effects of ht-9 martensitic steel.

*Nucl. Eng. Technol.*45, 311–322. 10.5516/net.07.2013.70612

ConlinJ. L.HaeckW.NeudeckerD.ParsonsD. K.WhiteM. C. (2018).

Los Alamos, NM (United States): Los Alamos National Laboratory LANL.*Release of ENDF/B-VIII. 0-based ACE data files*. Tech. Rep.13

De CarlanY.BechadeJ.-L.DubuissonP.SeranJ.-L.BillotP.BougaultA.et al (2009). Cea developments of new ferritic ods alloys for nuclear applications.

*J. Nucl. Mater.*386, 430–432. 10.1016/j.jnucmat.2008.12.15614

Di MaioP.CatanzaroI.BongiovìG.CastrovinciF.ChiovaroP.GiambroneS.et al (2024). Thermofluid-dynamic and thermal–structural assessment of the eu-demo wcll “double bundle” breeding blanket concept left outboard segment.

*Fusion Eng. Des.*202, 114335. 10.1016/j.fusengdes.2024.11433515

DongH.YuL.LiuY.LiuC.LiH.WuJ. (2017). Enhancement of tensile properties due to microstructure optimization in ods steels by zirconium addition.

*Fusion Eng. Des.*125, 402–406. 10.1016/j.fusengdes.2017.03.17016

EadeT.BradnamS.KanthP. (2022). A new novel-1-step shutdown dose rate method combining benefits from the rigorous-2-step and direct-1-step methods.

*Fusion Eng. Des.*181, 113213. 10.1016/j.fusengdes.2022.11321317

EhrlichK. (1999). The development of structural materials for fusion reactors.

*Philosophical Trans. R. Soc. Lond. Ser. A Math. Phys. Eng. Sci.*357, 595–623. 10.1098/rsta.1999.034318

El-GenkM. S.TournierJ.-M. (2005). A review of refractory metal alloys and mechanically alloyed-oxide dispersion strengthened steels for space nuclear power systems.

*J. Nucl. Mater.*340, 93–112. 10.1016/j.jnucmat.2004.10.11819

FedericiG.BoccacciniL.CismondiF.GasparottoM.PoitevinY.RicapitoI. (2019). An overview of the eu breeding blanket design strategy as an integral part of the demo design effort.

*Fusion Eng. Des.*141, 30–42. 10.1016/j.fusengdes.2019.01.14120

FraderaJ.SádabaS.CalvoF.HaS.MerrimanS.GordilloP.et al (2021). Pre-conceptual design of an encapsulated breeder commercial blanket for the STEP fusion reactor.

*Fusion Eng. Des.*172, 112909. 10.1016/j.fusengdes.2021.11290921

GreenwoodL.GarnerF. (1996). Hydrogen generation arising from the59ni (n,p) reaction and its impact on fission—fusion correlations.

*J. Nucl. Mater.*233, 1530–1534. 10.1016/S0022-3115(96)00264-422

GriffithsM.BickelG.DouglasS. (2010). Irradiation-induced embrittlement of inconel 600 flux detectors in candu reactors.

*Int. Conf. Nucl. Eng.*49330, 293–298. 10.1115/icone18-3012123

HernándezF.PereslavtsevP. (2018). First principles review of options for tritium breeder and neutron multiplier materials for breeding blankets in fusion reactors.

*Fusion Eng. Des.*137, 243–256. 10.1016/j.fusengdes.2018.09.01424

HuangQ. (2017). Status and improvement of clam for nuclear application.

*Nucl. Fusion*57, 086042. 10.1088/1741-4326/aa763f25

JudgeC. D.GriffithsM.WaltersL.WrightM.BickelG. A.WooO. T.et al (2013). “Embrittlement of nickel alloys in a CANDU* reactor environment,” in

*Effects of radiation on nuclear materials: 25th volume.*Editor T., Yamamoto (Anaheim, CA: ASTM International), 161–175. 10.1520/STP10424226

KachkoO.PuypeA.TerentyevD.BonnyG.Van RenterghemW.PetrovR. (2022). Development of rafm steels for high temperature applications guided by thermodynamic modelling.

*Nucl. Mater. Energy*32, 101211. 10.1016/j.nme.2022.10121127

KatohY.DongS.KohyamaA. (2002). Thermo-mechanical properties and microstructure of silicon carbide composites fabricated by nano-infiltrated transient eutectoid process.

*Fusion Eng. Des.*61, 723–731. 10.1016/s0920-3796(02)00180-128

KatohY.SneadL. L.Henager JrC. H.HasegawaA.KohyamaA.RiccardiB.et al (2007). Current status and critical issues for development of sic composites for fusion applications.

*J. Nucl. Mater.*367, 659–671. 10.1016/j.jnucmat.2007.03.03229

KatohY.OzawaK.ShihC.NozawaT.ShinavskiR. J.HasegawaA.et al (2014). Continuous sic fiber, cvi sic matrix composites for nuclear applications: properties and irradiation effects.

*J. Nucl. Mater.*448, 448–476. 10.1016/j.jnucmat.2013.06.04030

KawamuraY.HiroseT.GuanW.MiyoshiY.KatagiriT.WakasaA.et al (2024). Overview of progress on water cooled ceramic breeder blanket in Japan.

*Fusion Eng. Des.*201, 114260. 10.1016/j.fusengdes.2024.11426031

KimM.-C.ParkS.-G.LeeK.-H.Ho KimS.LeeB.-S. (2014). Evaluation of microstructure and mechanical properties in a thick plate of g91 steel and its weld for high temperature nuclear system.

*Curr. Nanosci.*10, 151–153. 10.2174/157341370966613110900473232

KonishiS.EnoedaM.NakamichiM.HoshinoT.YingA.SharafatS.et al (2017). Functional materials for breeding blankets—status and developments.

*Nucl. Fusion*57, 092014. 10.1088/1741-4326/aa7e4e33

KoyanagiT.KatohY.NozawaT.SneadL. L.KondoS.Henager JrC. H.et al (2018). Recent progress in the development of sic composites for nuclear fusion applications.

*J. Nucl. Mater.*511, 544–555. 10.1016/j.jnucmat.2018.06.01734

KuangA.CaoN.CreelyA. J.DennettC. A.HeclaJ.LaBombardB.et al (2018). Conceptual design study for heat exhaust management in the arc fusion pilot plant.

*Fusion Eng. Des.*137, 221–242. 10.1016/j.fusengdes.2018.09.00735

LeddaF.PettinariD.FerreroG.HartwigZ.LavianoF.MeschiniS.et al (2024). 3d neutronic analysis on compact fusion reactors: Phits-openmc cross-comparison.

*Fusion Eng. Des.*202, 114323. 10.1016/j.fusengdes.2024.11432336

LeeB.KimM.YoonJ.HongJ. (2010). Characterization of high strength and high toughness ni–mo–cr low alloy steels for nuclear application.

*Int. J. Press. Vessels Pip.*87, 74–80. 10.1016/j.ijpvp.2009.11.00137

LordM.BennettI.HarringtonC.CooperA.Lee-LaneD.CuretonA.et al (2024). Fusing together an outline design for sustained fuelling and tritium self-sufficiency.

*Philos. Trans. A*382, 20230410. 10.1098/rsta.2023.041038

McConnR. J.GeshC. J.PaghR. T.RuckerR. A.WilliamsR. I. (2011).

. Richland, WA (United States): Pacific Northwest National Laboratory PNNL.*Compendium of material composition data for radiation transport modeling*. Technical report PNNL-15870 Rev. 139

McGuinessP.PaulinI.DonikC.DobkowskaA.KubasekJ.PokornyJ.et al (2025). Recent progress in oxide-dispersion-strengthened (ods) alloys produced by additive manufacturing.

*Materiali Tehnologije*59. 10.17222/mit.2025.136440

MeschiniS.FerryS. E.Delaporte-MathurinR.WhyteD. G. (2023a). Modeling and analysis of the tritium fuel cycle for arc-and step-class dt fusion power plants.

*Nucl. Fusion*63, 126005. 10.1088/1741-4326/acf3fc41

MeschiniS.LavianoF.LeddaF.PettinariD.TestoniR.TorselloD.et al (2023b). Review of commercial nuclear fusion projects.

*Front. Energy Res.*11, 1157394. 10.3389/fenrg.2023.115739442

MeschiniS.Delaporte-MathurinR.TynanG. R.FerryS. E. (2025). Impact of trapping on tritium self-sufficiency and tritium inventories in fusion power plant fuel cycles.

*Nucl. Fusion*65, 036010. 10.1088/1741-4326/adacfa43

MurogaT.ChenJ. M.ChernovV. M.KurtzR.Le FlemM. (2014). Present status of vanadium alloys for fusion applications.

*J. Nucl. Mater.*455, 263–268. 10.1016/j.jnucmat.2014.06.02544

NorgettM.RobinsonM.TorrensI. M. (1975). A proposed method of calculating displacement dose rates.

*Nucl. Eng. Des.*33, 50–54. 10.1016/0029-5493(75)90035-745

PearsonR.BausC.KonishiS.MukaiK.D’angiòA.TakedaS. (2022). Overview of kyoto fusioneering’s scyllaⒸ(“self-cooled yuryo lithium-lead advanced”) blanket for commercial fusion reactors.

*IEEE Trans. Plasma Sci.*50, 4406–4412. 10.1109/tps.2022.321141046

PerrutM.CaronP.ThomasM.CouretA. (2018). High temperature materials for aerospace applications: Ni-based superalloys and

*γ*-tial alloys.*Comptes Rendus. Phys.*19, 657–671. 10.1016/j.crhy.2018.10.00247

PettinariD.TestoniR.ZucchettiM.ParisiM. (2024). Neutron transport and activation comparison between openmc and fispact-ii in arc-class reactor.

*Fusion Eng. Des.*209, 114713. 10.1016/j.fusengdes.2024.11471348

PollockT. M.TinS. (2006). Nickel-based superalloys for advanced turbine engines: chemistry, microstructure and properties.

*J. Propuls. Power*22, 361–374. 10.2514/1.1823949

RaffrayA.AkibaM.ChuyanovV.GiancarliL.MalangS. (2002). Breeding blanket concepts for fusion and materials requirements.

*J. Nucl. Mater.*307, 21–30. 10.1016/s0022-3115(02)01174-150

RenJ.YuL.LiuY.LiuC.LiH.WuJ. (2018). Effects of zr addition on strengthening mechanisms of al-alloyed high-cr ods steels.

*Materials*11, 118. 10.3390/ma1101011851

RibeF. (1975). Fusion reactor systems.

*Rev. Mod. Phys.*47 (7), 7–41. 10.1103/revmodphys.47.752

RiethM.SchirraM.FalkensteinA.GrafP.HegerS.KempeH.et al (2003). Eurofer 97. tensile, charpy, creep and structural tests.

53

RomanoP. K.HorelikN. E.HermanB. R.NelsonA. G.ForgetB.SmithK. (2015). OpenMC: A state-of-the-art Monte Carlo code for research and development,

*Ann. Nucl. Energy*82, 90–97. 10.1016/j.anucene.2014.07.04854

SchroederH. (1983). High temperature embrittlement of metals by helium.

*Radiat. Eff.*78, 297–314. 10.1080/0033757830820737955

SegantinS. (2023). Tokamak radiation environment.

56

SegantinS.TestoniR.ZucchettiM. (2020). Arc reactor – neutron irradiation analysis.

*Fusion Eng. Des.*159, 111792. 10.1016/j.fusengdes.2020.11179257

SerraE.BenamatiG. (1998). Hydrogen behaviour in aged low activation martensitic steel f82h for fusion reactor applications.

*Mater. Sci. Technol.*14, 573–578. 10.1179/mst.1998.14.6.57358

SinghB. N.LeffersT.GreenW.VictoriaM. (1984). Nucleation of helium bubbles on dislocations, dislocation networks and dislocations in grain boundaries during 600 mev proton irradiation of aluminium.

*J. Nucl. Mater.*125, 287–297. 10.1016/0022-3115(84)90556-759

SmithD. L.LoomisB. A.DiercksD. R. (1985a). Vanadium-base alloys for fusion reactor applications — a review.

*J. Nucl. Mater.*135, (2–3). 125–139. 10.1016/0022-3115(85)90070-460

SmithD. L.BakerC. C.SzeD. K.MorganG. D.AbdouM.PietS. J.et al (1985b). Overview of the blanket comparison and selection study.

*Fusion Technol.*8, 10–44. 10.13182/FST85-461

SorbomB.BallJ.PalmerT.MangiarottiF.SierchioJ.BonoliP.et al (2015). Arc: a compact, high-field, fusion nuclear science facility and demonstration power plant with demountable magnets.

*Fusion Eng. Des.*100, 378–405. 10.1016/j.fusengdes.2015.07.00862

SparksT.Nguyen-ManhD.ZhengP.WróbelJ. S.SobierajD.GorleyM.et al (2022). Mechanical characterisation of v-4cr-4ti alloy: tensile tests under high energy synchrotron diffraction.

*J. Nucl. Mater.*569, 153911. 10.1016/j.jnucmat.2022.15391163

SridharanK.AllenT. (2013). “Corrosion in molten salts,” in

*Molten salts chemistry*(Elsevier), 241–267.64

StasiakT.JasińskiJ. J.KurpaskaŁ.ChmurzyńskiW.ChmielewskiM.WilczopolskaM.et al (2024). Effect of sps consolidation and heat treatment on microstructure and mechanical behavior of fe–cr–al–y2o3 ods alloys with different ti and v contents.

*Archives Civ. Mech. Eng.*24, 76. 10.1007/s43452-024-00889-765

SznajderM.GeppertU.DudekM. R. (2018). Hydrogen blistering under extreme radiation conditions.

*npj Mater. Degrad.*2, 3. 10.1038/s41529-017-0024-z66

TanigawaH.GaganidzeE.HiroseT.AndoM.ZinkleS.LindauR.et al (2017). Development of benchmark reduced activation ferritic/martensitic steels for fusion energy applications.

*Nucl. Fusion*57, 092004. 10.1088/1741-4326/57/9/09200467

UkaiS. (2012). “4.08 - oxide dispersion strengthened steels,” in

*Comprehensive nuclear materials*. Editor KoningsR. J. (Oxford: Elsevier), 241–271. 10.1016/B978-0-08-056033-5.00069-068

ValenzaD.IidaH.PlentedaR.SantoroR. T. (2001). Proposal of shutdown dose estimation method by monte carlo code.

*Fusion Eng. Des.*55, 411–418. 10.1016/S0920-3796(01)00188-069

ZhangG.ZhouZ.MoK.WangP.MiaoY.LiS.et al (2015). The microstructure and mechanical properties of al-containing 9cr ods ferritic alloy.

*J. Alloys Compd.*648, 223–228. 10.1016/j.jallcom.2015.06.21470

ZhouG.LuY.HernándezF. A. (2021). A water cooled lead ceramic breeder blanket for european demo.

*Fusion Eng. Des.*168, 112397. 10.1016/j.fusengdes.2021.11239771

ZilnykK.OliveiraV.SandimH.MöslangA.RaabeD. (2015). Martensitic transformation in eurofer-97 and ods-eurofer steels: a comparative study.

*J. Nucl. Mater.*462, 360–367. 10.1016/j.jnucmat.2014.12.112

## Summary

Keywords

Nickel-based alloys, RAFM steels, high-strength martensitic steels, ODS alloys, SiC/SiC, vanadium-based alloys, OpenMC, neutron transport simulation

Citation

Pettinari D, Meschini S and Testoni R (2025) Assessment of structural materials in compact fusion reactor design. *Front. Nucl. Eng.* 4:1683702. doi: [10.3389/fnuen.2025.1683702](http://dx.doi.org/10.3389/fnuen.2025.1683702)

Received

11 August 2025

Revised

24 September 2025

Accepted

01 October 2025

Published

07 November 2025

Volume

4 - 2025

Edited by

[Bamidele Ebiwonjumi](https://loop.frontiersin.org/people/2844773/overview), Massachusetts Institute of Technology, United States

Reviewed by

[Steve Jones](https://loop.frontiersin.org/people/3174382/overview), University of Sheffield, United Kingdom

[Tomasz Stasiak](https://loop.frontiersin.org/people/3175469/overview), National Centre for Nuclear Research, Poland

Updates

Copyright

© 2025 Pettinari, Meschini and Testoni .

This is an open-access article distributed under the terms of the [Creative Commons Attribution License (CC BY)](https://creativecommons.org/licenses/by/4.0/). The use, distribution or reproduction in other forums is permitted, provided the original author(s) and the copyright owner(s) are credited and that the original publication in this journal is cited, in accordance with accepted academic practice. No use, distribution or reproduction is permitted which does not comply with these terms.

*****Correspondence: Davide Pettinari , [davide.pettinari@polito.it](mailto:davide.pettinari@polito.it)

Disclaimer

All claims expressed in this article are solely those of the authors and do not necessarily represent those of their affiliated organizations, or those of the publisher, the editors and the reviewers. Any product that may be evaluated in this article or claim that may be made by its manufacturer is not guaranteed or endorsed by the publisher.