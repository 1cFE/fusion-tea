---
source: "https://pmc.ncbi.nlm.nih.gov/articles/PMC6365859/"
source_type: "url"
extracted_at: "2026-03-29T20:50:40.978433+00:00"
content_hash_sha256: "a7b1a0e629b27c5e8b273efa2b666e5dad7a61c6ee342b21e52588496985b6e7"
backend: "trafilatura"
title: "Shielding materials in the compact spherical tokamak"
author: "Samuel A Humphry-Baker; George D W Smith"
---

## Abstract

Neutron shielding materials are a critical area of development for nuclear fusion technology. In the compact spherical tokamak, shielding efficiency improvements are particularly needed because of severe space constraints. The most spatially restricted component is the central column shield. It must protect the superconducting magnets from excessive radiation-induced degradation, but also from associated heating, so that energy consumption of the cryogenic systems is kept to an acceptable level. Recent simulations show that tungsten carbide and its composites form an attractive class of neutron-attenuating materials. In this paper, the key structure–property relationships of these materials are assessed, as they relate to generic materials challenges for plasma-facing materials. We first consider some fundamental materials properties of monolithic tungsten carbide including thermal transport, mechanical properties and plasma interaction. WC is found to have generally favourable properties compared to metallic tungsten shields. We then report progress on the development of a new candidate cermet material, WC-FeCr. Recent results on its accident safety, thermo-mechanical properties, and irradiation behaviour are presented. This review also highlights the need for further study, particularly in the areas of irradiation damage and hydrogen trapping.

This article is part of a discussion meeting issue ‘Fusion energy using tokamaks: can development be accelerated?’.

**Keywords:** nuclear fusion, compact spherical tokamaks, central column, plasma-facing materials, neutron shielding, tungsten carbide

## 1. Introduction

Compact fusion tokamaks have attracted recent attention because of their lower cost and shorter build time scale compared to conventional tokamak reactors [[1](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C1),[2](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C2)]. Their development is partly enabled by recent advances in our understanding of tokamak scaling laws, which have shown that the fusion power gain is only weakly dependent on the device size and rather more strongly on the level of energy confinement [[3](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C3)]. At the same time, improvements in energy confinement have been enabled by the development of high temperature superconductors (HTSs), such as yttrium barium copper oxide (YBCO). These materials have improved the achievable magnetic field strengths, allowing higher reactor power densities. They have also increased the corresponding operation temperatures and critical fields, which further enhance the viability of compact reactors. The combination of high field and small device size thus opens a promising opportunity to accelerate the development of fusion energy.

One promising technology is the compact spherical tokamak (c-ST). However, its operation poses a unique materials challenge. This challenge concerns the shielding materials that must protect the HTS tapes within the core of the central column from high energy neutron damage from the fusion plasma. The challenge is unique to the c-ST because of the slender nature of the central column compared to conventional tokamaks, which, combined with a reduction in device size, dramatically reduces the available space for shielding. Thus, the efficiency of the neutron shield defines the minimum device size and at the same time the maximum operational lifetime of the toroidal field HTS magnets. In what follows, we outline some of the design considerations for the development of highly efficient shielding materials.

### (a). Optimizing neutron attenuation

There are generally two strategies in employing materials for neutron attenuation. The first relies on heavy elements such as tungsten, which are good neutron reflectors, and the second on light elements such as carbon, which are good neutron moderators. Recent computational evidence has shown that a ceramic material based on tungsten carbide, which combines both light and heavy elements, could outperform either strategy [[4](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C4)–[7](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C7)].

In addition to optimizing the primary constituent material, shielding performance must be further optimized by judicious choice of shield coolant. Although the coolant's main function is to prevent excessive heat transfer into the superconducting core, and thus minimize loading of its cryogenic systems, it can serve the additional purpose of neutron moderation. Thus its design is a critical parameter in optimizing attenuation efficiency. Coolant design was recently investigated within the context of a small scale (185 MW fusion power) pilot plant [[3](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C3)]. A schematic of the device is shown in [figure 1](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F1)*a*. The reactor major and minor radii are 1.35 m and 0.75 m respectively, leaving 0.6 m for the central column region. A potential design for the central column region, based on calculations by Windsor *et al.* [[4](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C4)], is shown in [figure 1](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F1)*b*. Within this region is located a plasma wall gap of 0.05 m, structural elements of 0.05 m (shown in green), a superconducting core of 0.15 m (blue), a vacuum thermal gap of 0.03 m. Thus, the radial space apportioned for neutron shielding is only 0.32 m. Within this available space, Windsor *et al.* investigated the effect of varying the volume fraction of water coolant. The optimum design was composed of five concentric annular shields with a total water volume fraction of 0.168 [[4](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C4)], i.e. with each annular thickness of 5.4 cm and cooling channels of 1.25 cm. In [figure 1](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F1)*b*, the outer shield, which faces the plasma, is labelled ‘thermal shield’.

A further parameter for shield design is the possibility for secondary shielding materials on the in-board side of the shield, where average neutron energies are lower than the out-board side. The effect of secondary shields was also investigated by Windsor *et al.* [[4](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C4)]. Substituting tungsten carbide shielding layers with tungsten boride layers was found to enhance the shield efficiency. Locating one or more of these WB layers immediately adjacent to the superconducting core was optimum because of the lower average neutron energy there and the increasing cross-section for neutron capture in boron with decreasing neutron energy. In a follow up study, the authors showed that composite materials comprising mixtures of tungsten carbides and borides were also effective in enhancing neutron attenuation [[8](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C8)].

Despite recent progress in shield design, the maximum irradiation level that HTS tape can accommodate without degrading is not yet known. In fact, a limited amount of irradiation may be beneficial for tape performance. For example, in YBCO and GdBCO tapes irradiated in the range 30–50°C, the critical current density increases marginally up to moderate neutron fluences (of about 1022/m2), before degrading again at higher fluences [[9](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C9)–[11](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C11)]. The irradiation-induced change in critical current is dependent on the operating temperature. For example, for tapes irradiated to 2 × 1022/m2 an enhancement is seen at operating temperatures of 50 K or below, and a degradation at higher temperatures [[9](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C9)]. We note that this neutron fluence would correspond to approximately 40 h of continuous operation for a 32 cm WC shield, as proposed in [[8](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C8)], which predicted a fast neutron (*E* > 0.1 MeV) flux of approximately 1.4 × 1017 s−1 m−2 into the superconducting core [[8](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C8)]. However, the accuracy of this prediction is questionable, as all the studies were performed using fission reactor neutron sources [[9](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C9)–[11](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C11)]. Furthermore, the reactor neutron energies (e.g. with peaks at around 0.1 eV and 1 MeV [[11](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C11)]) do not match those of a typical fusion spectrum. Also, the irradiations were typically carried out above room temperature, instead of the cryogenic operation temperatures needed for superconducting magnet operation. Such differences in temperature will likely have a dramatic effect on damage accumulation. Although the magnitude of this effect is currently unknown, recent experimental efforts using proton beams to mimic neutron irradiation show promise for obtaining temperature-dependent data [[12](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C12)]. In the meantime, general trends can be extracted from the literature on pure metals and alloys, where the annealing temperatures for stage 1 migration of interstitial atoms are typically in the range 50–100 K [[13](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C13)]. When irradiated below these temperatures, damage from point defect accumulation becomes frozen in. It is possible that similar defect accumulation differences may exist for ReBCO, in which case, the existing fission reactor irradiation studies may provide an overly optimistic picture of irradiation damage resistance, placing an even greater imperative on shielding protection.

### (b). Generic materials challenges

Although the shield's primary function is maximizing neutron and gamma attenuation, there are more generic plasma-facing materials challenges that must be addressed in shield design. These materials challenges are covered in detail in more comprehensive works [[14](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C14)]. The challenges can be summarized in three core themes: (i) heat flux, (ii) irradiation, and (iii) plasma–surface interactions. The heat-flux challenge results from the extreme energy density within the fusion plasma, which will operate at temperatures in excess of 108 kelvin. In the first-wall and the divertor, the surface materials will experience steady-state heat-fluxes of the order of 1 and 10 MW m−2 respectively. The maximum wall loading scales inversely with thermal conductivity, *κ*, and therefore high *κ* materials are needed. More damaging, non-steady state fluxes may be experienced during plasma instabilities and so-called edge-localized modes (ELMs). These events will expose materials to an additional 1–10 MW m−2 pluses for fractions of a millisecond, which can lead to surface erosion and cracking. ELM-resistant materials must therefore have exceptional mechanical properties, as well as high *κ* values.

The second challenge of irradiation results from the 14.1 MeV neutrons released in the deuterium–tritium reaction. These high energy neutrons will lead to both displacement damage and transmutation. While the displacement damage for a research reactor such as ITER will be relatively low, perhaps less than 1 displacement per atom (dpa) during its lifetime, in a commercial spherical tokamak fusion power plant, each atom in the shield might be displaced approximately 100 times over its lifetime. These dpa levels will lead to the production of high point defect concentrations and associated micro-defects such as dislocation loops and voids. Radiation tolerant shield designs must therefore employ inherently radiation tolerant crystal structures, most probably engineered to provide large numbers of defect trapping sites such as nanoscale inclusions [[15](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C15)]. Transmutation product formation is generally dominated by low-Z populations (generally gaseous elements) and high-Z solute atoms. It is important that the radioactivity of these products is not long-lived and therefore candidate shield materials should be restricted to low-activation elements such as Ti, V, Cr, Fe, Ta, W, C and Si [[16](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C16)]. The release of the radioactive nuclides must be avoided during regular operation as well as accident scenarios. Such transmutation products will degrade materials properties. Low-Z gases such as H and He can lead to bubble formation, while high-Z solutes can cluster and/or precipitate out as second phases. This microstructural evolution will lead to loss of thermal conductivity and toughness. A potential strategy to mitigate such degradation is again via defect trapping sites.

A further plasma interaction challenge is related to implantation of ions (helium and tritium) from the fusion plasma. Helium implantation can severely modify the surface, leading to ‘dust’ formation and thus pollution of the plasma. He implantation will also embrittle the near-surface region via the formation of gas bubbles and associated structures (as mentioned above). Tritium imposes equally serious concerns over radioactive safety. To minimize tritium release its retention in the shield material must be inhibited by the selection of low solubility structures, and strategies to prevent tritium spread to other parts of the reactor must be implemented. Such strategies may rely on lowering tritium mobility within the shield.

In light of these challenges, there are some serious problems associated with metallic tungsten shields. Tungsten has a high ductile-to-brittle transition temperature (DBTT), which is only marginally below its recrystallization temperature, meaning there is only a narrow temperature window of potential use as a structural material (although there are ongoing efforts to improve its ductility, through approaches such as cold rolling [[17](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C17)]). It oxidizes catastrophically at high temperatures, which could lead to transmutation product release in potential accident scenarios. Also, forged tungsten products, which offer the best properties, are difficult to machine. Powder injection moulding processes show promise in terms of their flexibility for complex shapes, but have so far not been able to achieve the same mechanical properties as wrought material [[18](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C18)]. Tungsten carbide shields offer several advantages on these points. They can be manufactured in conjunction with ductile metallic binders in the form of a cermet. Cermets are routinely manufactured for energy extraction and machine tool applications, where they operate in harsh environments. They can be shaped relatively inexpensively prior to sintering. They have good mechanical properties, such as impressive fracture toughness, fatigue and creep resistance [[19](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C19)]. Despite their promise, such ceramic materials are yet to be exploited for tokamak fusion engineering applications.

This remainder of this article explores the issues surrounding the performance of WC ceramics and related composites. It is divided into two sections. We first detail the properties of the monolithic ceramics as they relate to the above-mention materials challenges. We then report some recent results on a candidate WC-based material, WC-FeCr. Its behaviour under accident scenarios and irradiation are described.

## 2. Monolithic ceramic shields

### (a). Properties of tungsten carbides and borides

[Table 1](https://pmc.ncbi.nlm.nih.gov#RSTA20170443TB1) reports some basic thermophysical properties of compounds in the W-C [[20](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C20)] and W-B [[21](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C21)] binary systems, alongside those of some other candidate plasma facing materials (PFMs), namely: W, C, SiC and Be. We first consider the melting points. For the binary W-B and W-C compounds these are all close to or over 3000 K, i.e. similar to SiC and W, showing their promise for reactor components experiencing very high temperatures. The densities of the W-B and W-C compounds decrease with decreasing tungsten content. For example, the densities of W2C and W2B are respectively only 11% and 17% lower than pure W, while the densities of the WC and WB are respectively about 19% and 21% lower. The most commonly studied compound in the W-C system is that of equimolar proportions. This is because of its superior stability. W2C has a relatively low formation enthalpy (−8.8 kJ mol−1) and is hence not stable below 1520 K. By contrast, all three W-B compounds are stable over a range of temperatures (except for the allotropic phase change at 2110–2170°C for WB).

#### Table 1.

| melting point (K) | density (g/cc) | density of W atoms (mol m−3) |
formation enthalpy (kJ/mol-at) | |
|---|---|---|---|---|
| W | 3695 | 19.3 | 10.5 | / |
| C | 4000(s) | 2.27 | / | / |
| SiC | 3000 | 3.21 | / | −34.7 |
| Be | 1560 | 1.85 | / | / |
W2C |
3020 | 17.2 | 9.1 | −8.8 |
| WC | 3143 | 15.6 | 8.0 | −19.7 |
W2B |
2920 | 16 | 8.5 | −21.8 |
| WB | 2938 | 15.3 | 7.0 | −31.9 |
W2B5
|
2635 | 11 | 5.2 | −27.5 |

For the W-B ceramics, very few materials property data have been collected that is relevant to fusion reactor conditions. Furthermore, the W-B shield is envisaged as a secondary shielding material, i.e. not plasma facing. Therefore, it is broadly excluded from the remainder of this article. Furthermore, other PFMs such as C, SiC and Be are excluded because of relatively poor neutron shielding capabilities.

The remainder of this article will focus exclusively on metallic W, ceramic WC and its composites. The room temperature mechanical properties of these materials are reported in [table 2](https://pmc.ncbi.nlm.nih.gov#RSTA20170443TB2). In considering strength, we report the flexural strength, which is more easily measured on brittle materials such as W and WC than ultimate tensile strength, and is less sensitive to defects. Data on pure W are taken from powder processed materials reported by Palacios *et al.* [[22](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C22)]. For binderless WC, flexural strength is typically reported to be in the range of about 0.8–1.6 GPa, depending on the grain size and sintering temperature [[23](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C23),[27](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C27)]. We take the maximum reported value. For WC-Co cermets, flexural strength is usually in the range 1–4.2 GPa [[28](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C28)], depending on grain size and Co binder content. We take an intermediate case of a coarse-grained, 10 wt% Co-binder volume fraction composite. While many of the properties, such as Young's modulus, Poisson's ratio and linear thermal expansion, are relatively similar across all materials, the key difference is the outstanding flexural strength of WC-based materials. For example, in a WC-10Co cermet it is about 3.9 GPa. This indicates exceptional thermomechanical shock resistance.

#### Table 2.

In what follows we review some properties of WC and WC-based materials relevant to their performance as neutron shields, and compare these to metallic tungsten. This discussion is organized according to the three core challenges highlighted earlier: (i) heat flux, (ii) irradiation, and (iii) plasma–surface interactions.

### (b). Heat flux

We begin with a discussion of thermal conductivity, *κ*, as this is the most critical parameter defining performance under steady state thermal loading. Such a discussion is timely because *κ*WC was recently reported to be approximately a factor of 2 higher than its historically reported value [[29](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C29)]. The temperature dependent thermal conductivities reported in recent and historical literature are shown in [figure 2](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F2). The upper limit for WC is taken from a 97% dense sample by Gubernat *et al.* [[29](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C29)]. 1 The lower limit is taken from a 90% dense sample by Fransden and Williams [

[33](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C33),

[34](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C34)]. A factor of two difference is seen, with the room temperatures conductivities of approximately 180 and approximately 90 W/m-K respectively. Our interpretation is that the differences in relative density account for the discrepancy, and that the mechanism of thermal conductivity reduction is phonon scattering at pores. Shown alongside the pure WC data are results for a coarse-grained WC-Co cermet with 10 wt% Co. This material has a very coarse grained structure, with a linear intercept grain size of 6.5 µm, which results in an impressive room temperature conductivity of 145 W/m-K [

[35](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C35)].

The main highlight of [figure 2](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F2) is that, contrary to previous reports, WC can perform similarly to pure W at room temperature when processed close to full density. For example, the conductivities for W are in the range 160–180 W/m-K [[30](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C30)–[32](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C32)]. It is possible that the thermal conductivity of WC could be further improved, since the WC samples shown still contained significant porosity (approximately 3%); however, for the remainder of this paper we consider the thermal conductivity data from Gubernat *et al.* [[29](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C29)] as a reasonable literature value for what could be routinely achievable.

We now estimate the maximum possible heat fluxes achievable in WC before surface melting occurs. We consider a semi-infinite slab of material with thickness, *d*, subjected to one-dimensional heat flow on the top-surface, while the bottom surface is kept constant at the temperature of a coolant, *T*c. Under these conditions, the maximum heat flux can be estimated using

| 2.1 |

where *T*m is the melting point and *κ* is the room temperature thermal conductivity. Using equation (2.1) the critical heat flux can be calculated for materials with the thermophysical properties reported above (see [table 1](https://pmc.ncbi.nlm.nih.gov#RSTA20170443TB1) for *T*m and [figure 2](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F2) for *κ*). For this calculation we set the plate thickness to *d* = 0.02 m and the coolant temperature *T*c = 600 K (i.e. the approximate upper limit of a pressurized water-cooled component). For WC, the critical heat flux is calculated to be 23 MW m−2. This is very close to the critical heat flux for W, which is calculated to be 27 MW m−2. The discrepancy is mainly because of the lower melting point of WC.

Under dynamic heating conditions, such as ELMs and plasma instabilities, materials may be exposed to localized heat fluxes of 1–10 MW m−2 for sub-millisecond durations of approximately 0.2–0.5 ms [[36](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C36)]. Under such conditions, the material surface will be modified by various mechanisms such as crack formation and surface melting. As surface melting was covered above—at least for steady state conditions—we here assess the propensity for surface cracking. The thermal stress resistance parameter for maximum allowable temperature difference before failure can be given by [[37](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C37)]

| 2.2 |

while the parameter for maximum allowable heat flux is

| 2.3 |

where *σ*f is the fracture stress, *E* is the Young's modulus, *ν* is the Poisson's ratio and *α* is the linear thermal expansion coefficient. *R* and *R′* can be predicted using the properties reported in [table 2](https://pmc.ncbi.nlm.nih.gov#RSTA20170443TB2). For W, WC and WC-10Co, *R′* values are 3, 9.9 and 12.8 respectively. Thus, the thermal shock parameter for maximum heat flux in WC is about a factor of 3 higher that powder metallurgy processed W, while for WC-Co, it is about a factor of 4 higher. This demonstrates a key advantage of the cermet approach.

While the creep behaviour of WC-Co has been studied at both moderate [[38](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C38)] and high [[39](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C39)] temperatures, that of the binderless WC compound has not. We therefore consider a surrogate property, high temperature hardness. [Figure 3](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F3) shows the high temperature hardness of W, WC and WC-Co. The data for pure WC are scattered, which is likely due to differences in processing conditions. For example, samples produced by Lee were hot-pressed [[43](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C43)], while materials used in Miyoshi & Hara's study were pressurelessly sintered [[44](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C44)] and therefore their samples likely had significantly higher porosity. The low hardness values reported after pressureless sintering were likely due to crushing of porosity under the indenter, rather than by deformation in the bulk material. We therefore pay more attention to the data of Lee.

It is useful to compare the hardness degradation of WC [[43](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C43)] to pure W [[40](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C40)–[42](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C42)]. At room temperature, the hardness of WC is about a factor of 8 higher than W, with hardness values of 23 and 3 GPa respectively. At higher temperatures, e.g. at 800°C, the enhancement factor increases to about 20, with hardness values of 17 and approximately 0.8 GPa respectively. WC-Co cermets [[45](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C45)] show some reduction in hardness over WC, which increases with increasing binder content and temperature. This is presumably because deformation in the binder becomes dominant above 800°C [[46](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C46)]. Despite this, even for the cermet with a binder content of 15 wt%, the hardness at 800°C is over 6 GPa, which is a factor of 10 higher than for W.

### (c). Irradiation

There is little experimental information available on the tolerance of WC-based materials to high energy neutron irradiation. Some fast-neutron (greater than 1 MeV) irradiations have been performed on pure WC at temperatures of 300–700°C [[47](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C47)]. WC was compared to four other metal carbides: TiC, ZrC, TaC and NbC. Of all candidate materials, WC performed the best in terms of cracking resistance; it received no damage or only minor damage. By contrast, the other carbides all experienced severe or minor fracturing over the range of fluences studied (up to 5 × 1025 n/m2). WC also swelled less than the other candidates, expanding in volume by a maximum of approximately 0.6%, versus 2–3% for the others.

Further insight about radiation tolerance and in particular the physics of recoil events has been gained from molecular dynamics simulations [[48](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C48),[49](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C49)]. Such recoil events induce strongly asymmetric defect populations on the two sublattices. Much higher defect populations are predicted on C sub-lattice versus the W one. The difference can be as much as 2 orders of magnitude [[48](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C48)].

Ion irradiation can also offer insight on displacement damage events. Ion-irradiation is well-studied in WC-based tooling materials since it offers a way to improve their surface mechanical properties. The subject has been reviewed extensively. In these studies, which are mostly in WC-Co, degradation of WC under ion-irradiation is generally governed by two sequential stages: (i) a hardening stage, dominated by the formation of point defects, interstitial loops and voids; and next (ii) a softening stage, dominated by crystal to amorphous phase transformations. Both processes in general lead to volume expansion.

The hardening regime is the most-studied regime in WC-based materials because of its usefulness in improving the surface wear properties. The degree of hardening depends on the microstructure (grain size and Co content) and the ion type and energy. In the case of nitrogen ion implantations, which are perhaps the most widely studied, hardness increases of around 40–50% are routinely found [[50](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C50)]. Dislocations and loops are produced [[51](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C51)] and such defects are strongly related to the orientation of the beam relative to that of the WC grains [[52](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C52)]. However it is not clear to what extent hardening is solely due to displacement damage versus hardening from the host atoms themselves (i.e. by solid solution strengthening and formation of nitride particles [[53](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C53)]). Hardening is accompanied by lattice swelling. For example, under 100 keV nitrogen implantations, the WC lattice parameter was found to swell by about 1% after a dose of 10 ions nm−2 [[54](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C54)]. Swelling is anisotropic; there is about 50–70% more strain in the *c*-axis versus the *a*-axis.

Next, we consider the amorphization or softening regime. It is useful to compare WC to other ceramic materials. In discussing this point, Burnett & Page define the critical damage level required to amorphize, which is expressed in energy per unit volume [[55](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C55)]. For ceramics, the critical damage level depends largely on the bonding type. In covalent bonded ceramics with a low degree of iconicity, such as Si and SiC, relatively low critical values are found, e.g. about 0.6–1 × 1021 and 2 × 1021 keV/cc for Si and SiC respectively [[55](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C55)]. However, in ceramics with highly ionic or metallic bonding, such Al2O3 (ionic) or indeed WC (metallic), *ρ*crit values are about 2–3 orders of magnitude larger—e.g. about 6–8 × 1023 and 3–6 × 1023 keV/cc for Al2O3 and WC [[55](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C55)]. This suggests an unusually high level of tolerance to irradiation in WC before amorphization occurs.

### (d). Plasma–surface interaction

The interaction of WC with the fusion plasma has been studied on the basis that it will form *in situ* in tokamaks containing both tungsten and graphite [[56](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C56)]. In such a scenario, hydrocarbon molecules, formed by graphite erosion, could redeposit on tungsten surfaces, forming a fine surface layer of WC. Therefore, plasma interaction with WC is relatively well studied. Below we review hydrogen ion sputtering and retention/desorption behaviour.

First, the resistance to physical sputtering is considered. The energy range of interest for physical sputtering will likely be 50–1000 eV. This is significantly lower than the core plasma temperature, which is of the order of 10 000 eV, but is reflective of the edge temperature of the plasma. [Figure 4](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F4) shows the sputtering yields of deuterons on various plasma-facing materials in the range 10–10 000 eV, as reported by Plank & Eckstein [[56](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C56)]. The WC sputtering rate is negligible below approximately 100 eV, similar to W. The sputtering rate rises significantly between 200 and 1000 eV, reaching a maximum yield of about 0.02 at 4000 eV. Compared to other candidate plasma facing materials, such as C and SiC, WC sputters much less, particularly in the low energy regime. Thus, although the sputtering rate of WC is slightly higher than W for a given energy, it is favourable compared to other candidate plasma facing materials.

There is some evidence from computational simulations of chemical sputtering of carbon from WC at relatively low energies [[57](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C57)]. Chemical sputtering is predicted to occur following amorphization of the surface layer and subsequent formation of hydrocarbon molecules. However, experimental validation is still needed to confirm this chemical sputtering mechanism. If chemical sputtering causes excessive pollution of the plasma, the WC shield can be clad with an outer layer of metallic tungsten.

A second area of importance is the retention behaviour of hydrogen isotopes in the shield. Most studies of hydrogen retention in WC have involved deuterium ions in the energy range 1–5 keV [[58](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C58)]. When irradiated at room temperature, the retained deuterium saturates at about 1022 ions m−2, after which spontaneous re-emission equilibrates with retention rate, leading to no further inventory build-up [[58](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C58)]. When the implantation temperature is increased, the fraction of retained deuterium decreases. For example, at 200°C it falls to about half its room temperature value, and at 600°C the retained value becomes negligible [[58](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C58),[59](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C59)].

[Figure 5](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F5)*a* shows the amount of retained deuterium in WC as function of fluence for 1 keV ions [[60](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C60)]. Also shown in [figure 5](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F5)*a* are comparable measurements on W, Be and Mo [[61](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C61)]. WC and W both retain a similar fraction of implanted ions, which is significantly lower than Be, but higher than Mo. [Figure 5](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F5)*b* shows examples of thermal desorption spectra (TDS) for W and WC when irradiated with 1 keV ions to 1022 ions m−2 [[60](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C60),[61](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C61)]. In the WC spectrum, four peaks are distinguishable. Peaks 1 and 2 are related to desorption of interstitial deuterium and peak 3 to desorption from vacancy-trapped deuterium. A small fraction is still retained at these temperatures and will remain bound in the material up to about 700°C. This fourth and final stage is related to deuterium bonded to carbon and accounts for only a small fraction of the total trapped inventory. It should be noted that the binding energy between deuterium atoms in the above sites is calculated to be negative [[62](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C62)], suggesting molecule formation is unfavourable.

These studies can provide some design tools toward minimizing hydrogen isotope retention. First of all, diffusion is faster in the *c*-axis of WC [[62](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C62),[63](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C63)], suggesting that strongly textured materials would enable a directional dependence to the inventory build-up. Secondly, because trapping is dominated by the presence of interstitials and vacancies, both of which are intrinsic defects caused by deviations from stoichiometry, the carbon content can and should be properly controlled.

## 3. A candidate fusion engineering material, WC-FeCr

Attention is now turned from the intrinsic properties of WC, to a possible engineering form of a WC-based material. The form we consider is a cermet, or ceramic-metal composite, whereby the ceramic phase is distributed randomly as particles, which are bound together by a small volume fraction of a ductile metallic matrix. Such materials are routinely employed in machine tools instead of monolithic ceramics primarily because of their low cost and excellent mechanical properties. Their low cost is due their ability to be densified pressurelessly; monolithic WC requires pressure-assisted sintering either by hot-pressing or spark-plasma sintering. The pressureless process allows more complicated geometries to be shaped prior to sintering, which avoids excessive machining costs. Further savings result from lowering the sintering temperature from approximately 2000°C to approximately 1400°C, because of the presence of a liquid phase. The outstanding mechanical properties result from combining a hard carbide phase with a tough metallic one. The resulting structure exhibits some of the best attributes of each—the high compressive strength and creep resistance of the carbide, and the high fracture toughness and shock resistance of the metal. The degree to which each attribute is displayed can vary dramatically depending on the key microstructural variables. We now explore these variables through a microstructure-property map.

### (a). Microstructure–property map

There are two key parameters that control the properties of a tungsten carbide cermet: (i) the mean diameter of WC grains, *d*WC; and (ii) the volume fraction of the binder phase, termed *V*Co for Co-bonded cermets. For commercially available cermets, the grain sizes are typically in the range *d*WC = 0.2–0.5 µm (ultrafine) to *d*WC > 6 µm (extra coarse) with volume fractions between *V*Co = 0.05 and *V*Co = 0.5. Spanning this microstructural space, a broad range of thermal, mechanical and neutronics properties can be achieved. Although many of these properties were reported in the previous section, a discussion of their interrelation with microstructure was not. In what follows, we review these properties in light of existing data for WC-Co, which compare well to properties of cermets with Fe-based binders [[64](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C64)].

[Figure 6](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F6) shows a schematic microstructure-property map for some fusion-relevant properties. Arrows indicate the direction in which a property will be maximized with respect to *d*WC and *V*Co. The properties are allocated in three categories: room temperature mechanical properties (labelled in roman); high temperature properties (italics) and other properties (bold).

We firstly address room temperature mechanical properties. These are strongly microstructure-dependent, varying by a factor of 2–5 across typical industrial grades. For properties related to resistance to cracking (i.e. fracture toughness and flexural strength) the arrows run bottom-left to top-right. On the other hand, the hardness arrow runs in reverse, i.e. top-right to bottom-left. [Figure 6](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F6) shows that, in general, deformation-resistant microstructures (that is, fine-grained, low binder content composites) favour higher hardness but lower fracture toughness and flexural strength, and vice versa. The most strongly microstructure dependent property (hence given the longest arrow in [figure 6](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F6)) is fracture toughness, which can vary between 5 and 27 MPa m1/2 [[28](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C28)]. The change for hardness is less pronounced but still significant, varying typically between 7 and 22 GPa [[65](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C65)]. Transverse rupture strength is represented as a bent arrow, as for fine grain sizes, or, more accurately, fine binder ligament widths. Up to about 0.4–0.7 µm, strength increases with length scale from about 1 to 3 GPa. Above that size, strength decreases dramatically, at a rate that increases with decreasing binder content [[66](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C66)]. For Young's modulus, the only relevant parameter is the binder content hence a flat line is shown. The variation is between about 700 GPa for low binder fractions and 350 GPa for *V*Co = 0.5 [[24](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C24)].

For high temperature properties (labelled in italics), arrows all point in the same direction. Furthermore, they point more or less at right angles to room temperature properties. This is because the high temperature properties are governed by transport, which is broadly controlled by the density of WC/Co interfaces. In the case of thermal conductivity, these interfaces act as phonon scattering sites, while for creep deformation, the WC/Co interfaces enable deformation by sliding and grain rotation. Thus, thermal and mass transport is optimized by processing large grained, low binder content materials. For steady state creep, its rate is most sensitive to binder-content. For example, doubling the Co volume fraction from 16 to 37 vol% can result in a factor of 60 increase in creep rate (for *d*WC = 2.2 µm, *σ* = 240 MPa and *T* = 1150°C [[39](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C39)]). The grain size dependence is less sensitive: in general, the creep rate scales with the inverse square of grain size [[39](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C39)]. For thermal transport, the microstructural sensitivity is less extreme. There is only a moderate dependence on grain size, for example, in WC-17Co, the room temperature thermal conductivity of a 9 µm material (134 W/m-K) was only 37% higher than a similarly processed 2.3 µm material (98 W/m-K) [[26](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C26)]. Binder content shows a similarly moderate dependence. For example, in a 3.5 µm material, tripling the binder content from 6 to 19 vol% caused a reduction in thermal conductivity of only 25%, from 110 to 83 W/m-K [[33](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C33)].

The remaining properties on [figure 6](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F6) are for neutron attenuation and manufacturability. Manufacturability (although not a material property *per se*) is aided when *V*Co is highest and when the *d*WC is smallest, i.e. pointing bottom-right, for the same reasons as why creep resistance points top-left (i.e. both sintering and creep occur by similar mechanisms). The situation for neutron attenuation is slightly simpler; the most significant effect will come from the binder content, since the binder metal is a poor high energy neutron attenuator. Windsor *et al.* quantified the power deposition through a set of five WC-FeCr shields, each of 5 cm thickness [[8](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C8)]. Power deposition increased by 1.7% for each additional 1 wt% of binder. There is no direct physical dependence on *d*WC, since the grain size is well below the typical phonon mean free path. An indirect effect of *d*WC is inevitable for reasons of manufacturability outlined above; larger grained materials are more difficult to densify and hence will on average contain more porosity. The effect of such porosity could be significant. For example, Windsor *et al.*'s study showed an increase in power deposition of 4.3% for each additional 1 wt% of porosity [[8](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C8)].

### (b). Development of an FeCr binder

As outlined above, commercial WC cermets usually employ Co-based metallic binders. Co is chosen primarily because of its excellent ability to densify WC. It possesses a low wetting angle on WC surfaces and has high solubility for WC when in a molten state. Co is not favoured for fusion applications because of its high activity when irradiated by high energy neutrons [[16](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C16)]. An alternative low activation binder is therefore required.

An obvious binder choice is Fe. Of the two most commonly substituted elements for WC-cermets, Ni and Fe [[67](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C67)], it has the lowest neutron activation [[16](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C16)]. It is also has the advantage of a stable bcc structure up to 912°C, making it inherently more radiation tolerant than fcc Ni. Fe-based hardmetals have been studied extensively for machine tool applications . Their mechanical properties, such as hardness and toughness, are generally comparable to WC-Co [[64](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C64)], as are properties such as thermal expansion and thermal conductivity [[68](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C68)].

The key difference in considering an Fe-based binder is difficulty with processing. Firstly, grain growth is more restricted for WC-Fe than for WC-Co [[69](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C69),[70](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C70)], because of the lower solubility in Fe for W and C. This also means densification is slower. A further challenge when processing Fe-based cermets is their tendency to form deleterious mixed-metal carbides. This phenomenon may be understood by reference to [figure 7](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F7), which shows vertical sections through the W-C-Co and W-C-Fe phase diagrams at a fixed binder content of 10 wt%. The two-phase region where WC+fcc coexist, delineated by the red circles, is much narrower in the W-C-Fe system than it is for W-C-Co. This means that in WC-Fe materials, any deviation from the desired stoichiometry is more likely to result in the precipitation of M6C or graphite, both of which have a detrimental effect on mechanical properties. Therefore the manufacture of WC-Fe cermets requires a high degree of carbon control.

In reality, a pure elemental Fe binder is unlikely to be used. Fe powders oxidize readily in air, and if fine enough can be pyrophoric [[71](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C71)]. This makes it challenging to fabricate and handle powder formed during the co-milling of WC and Fe primary powders prior to sintering. Pure Fe is also relatively prone to embrittle under irradiation [[72](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C72)]. These issues can be overcome by alloying Fe with Cr. From the literature on low activation ferritic steels, a maximum in resistance to irradiation-induced embrittlement is known to occur at Cr contents of 7–10 wt% [[73](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C73)]. Furthermore, at such Cr contents, chromia scales are known to form with an attendant reduction in oxidation rate [[74](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C74)].

### (c). Accident tolerance

The behaviour of plasma-facing materials under accident scenarios is crucial. A potential worst-case scenario could a loss-of-coolant in combination with a breach of the vacuum vessel, resulting in air ingress. Under such a scenario, the temperature of the plasma-facing materials, which will continue to self-heat from neutron activation, could reach over 1000°C, in the case of W, and hold this temperature for several days. At these temperatures, W and WC-based materials will oxidize rapidly and what is more, their oxides are volatile, meaning that dangerously toxic and radioactive materials could be released into the environment.

Recently, we have focused efforts on the oxidation of WC [[75](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C75)] and WC-FeCr [[76](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C76)]. We have systematically investigated the oxidation behaviour of monolithic WC, using material fabricated by spark-plasma-sintering (SPS). Remarkably, these materials showed improved oxidation resistance over previous studies by a factor of 10–30 [[75](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C75)]. The key difference between our materials and previous studies was an improved density enabled by the SPS process; our samples were greater than 99% theoretical density, while those processed pressurelessly were on the order 90% [[77](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C77)]. This new processing method brings the relative oxidation rates of pure W and WC to similar levels ([table 3](https://pmc.ncbi.nlm.nih.gov#RSTA20170443TB3)), while WC shows slightly improved tolerance at 1000°C [[75](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C75)]. The oxidation rate of WC-FeCr is slightly higher than pure WC at high temperatures [[76](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C76)]. For example, at 1000°C the rate constant for WC-FeCr is 87 mg/cm2-hr, versus only 27 mg/cm2-hr for pure WC.

#### Table 3.

| temperature | 600°C | 700°C | 800°C | 900°C | 1000°C |
|---|---|---|---|---|---|
| W | 0.17 | 2.1 | 11 | 16 | 69 |
| WC | 1.0 | 3.6 | 6.5 | 21 | 27 |
| WC-FeCr | 0.054 | 4.3 | 39 | 61 | 87 |

The poor oxidation resistance of WC-FeCr has motivated research into oxidation resistant coatings. A successful strategy is Si-impregnation via pack-cementation method [[76](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C76),[78](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C78)]. An overview of the phase formation during the impregnation process, and subsequent oxidation, is presented in [figure 8](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F8)*a*. After impregnation, a two-part coating forms, consisting of an FeSi2 rich outer layer and an WSi2 inner layer. The formation of an outer FeSi2 rich layer is surprising because the weight fraction of Fe in the cermet is less than 10%. Its preferential reaction with Si can be explained by the combination of its high enthalpy of mixing with Fe and rapid diffusion kinetics in the FeSi2 phase compared with WSi2 [[76](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C76)]. This separation process is favourable for oxidation resistance, since FeSi2 is able to form a passivating SiO2 outer layer. Such passivating outer layers do not form on WSi2 surfaces over the temperature range of interest (800–1200°C). Instead oxidation proceeds in an active manner to produce a mixed WO3 + SiO2 layer [[79](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C79)]. The oxidation kinetics of Si-impregnated WC-FeCr is compared to the un-coated substrate in [figure 8](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F8)*b*. The coated samples show a factor of 1000 improvement in oxidation kinetics over a broad temperature range. The protective nature of the coating fails at 1200°C, whereupon FeSi2 melts, with an attendant increase in oxidation rate. These coatings also display an enhanced hardness over the substrate beneath [[78](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C78)].

### (d). He implantation

Material degradation under He implantation is an important issue for WC-based materials, as carbon is a strong He producer under neutron irradiation. Helium ions will also be deposited into plasma-facing material surfaces as they form the ash of the plasma. Ultimately both mechanisms will embrittle the material.

[Table 4](https://pmc.ncbi.nlm.nih.gov#RSTA20170443TB4) shows the key transmutation products in WC after 1 year of neutron irradiation for a representative reactor model [[80](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C80)]. Only elements with abundancies greater than 1 in 1010 are shown. The solid products can be categorized according to whether they derive from the W- or the C-sublattice. For W, the main products are Re and Os, which form when the neutron is captured, and Hf and Ta, which form coincidentally with emission of a gas atom, usually helium. The He emission from the W sublattice is minor in comparison to He emission from the C one. The products for C are Li, Be and B. Of these, the most significant is Be, which forms via the (*n*, *α*) reaction, thus also producing the majority of He formation. Hence the quantities of Be and He are both approximately 0.02%.

#### Table 4.

| element | H | He | Li | Be | B | Hf | Ta | Re | Os |
|---|---|---|---|---|---|---|---|---|---|
| atomic number | 1 | 2 | 3 | 4 | 5 | 72 | 73 | 75 | 76 |
| molar percentage | 8.9×10−4
|
1.9×10−2
|
2.4×10−6
|
1.9×10−2
|
1.7×10−5
|
3.6×10−4
|
7.6×10−2
|
2.3×10−1
|
6.0×10−3
|

The corresponding transmutation products for the Fe92Cr8 binder are shown in [table 5](https://pmc.ncbi.nlm.nih.gov#RSTA20170443TB5). Substantial quantities of H and He are generated. The solid products can be categorized as Fe-derived and Cr-derived. Fe-derived products are mainly Co and Ni, from neutron capture, and Mn and Cr, from gas emission reactions. Of these, the most significant is Mn, which forms via the 56Fe(*n*, *p*)56Mn reaction. This reaction also accounts for the majority of H formation, hence the quantities of Mn and H are both approximately 0.1%. The level of H production is significantly higher in Fe92Cr8 than in WC (by a factor of 100). The production of He is similar in both phases.

#### Table 5.

| element | H | He | Ca | Ti | V | Mn | Co | Ni |
|---|---|---|---|---|---|---|---|---|
| atomic number | 1 | 2 | 20 | 22 | 23 | 25 | 27 | 28 |
| molar percentage | 9.9×10−2
|
1.9×10−2
|
1.2×10−7
|
2.7×10−3
|
2.1×10−2
|
9.4×10−2
|
7.2×10−5
|
2.7×10−8
|

Since He gas formation is a common issue in both the WC particles and the FeCr binder, we have recently studied He-ion irradiation in WC-FeCr [[81](https://pmc.ncbi.nlm.nih.gov#RSTA20170443C81)]. This was accomplished using *in situ* irradiation in a transmission electron microscope (TEM). We studied very high He contents, by injecting total doses of up to 50 at. % He into the TEM foils. These He levels are much higher than would be expected from neutron irradiation, hence they better simulate the effect of direct injection of He into the near-surface region from the fusion plasma. In the FeCr phase, we found a coarse array of 3 nm bubbles when irradiated at room temperature, while at 500°C the bubbles were approximately 6 nm in diameter. The situation for WC particles was very different: Bubbles were much finer, approximately 2 nm in diameter, and did not grow any coarser at higher irradiation temperatures. The study also showed some interesting surface phenomena related to the formation of secondary phases such as M6C and Cr-carbide. The formation of M6C in WC-FeCr was highlighted in [figure 7](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F7). We found that M6C and Cr-carbide phases tended to nucleate very large bubbles, approximately 20–40 nm, at their peripheries. These observations suggest that in order to improve the irradiation tolerance of these materials, the presence of these particles should be minimized.

## 4. Conclusion

High energy neutronics studies show that WC is a highly efficient neutron shielding material. Hence it shows promise for the development of the compact spherical tokamak, within which the space available for neutron shielding of the central column is limited. In this paper we review the fundamental materials properties of pure WC and WC-based cermets as they relate to generic fusion materials design challenges.

-
—
For some properties, WC and WC-cermets can dramatically exceed the performance of pure W. For example, some WC-based cermets have flexural strengths a factor of 10 higher than pure W. Furthermore, the thermal shock parameters of WC-based materials are predicted to be a factor of 3–4 higher than pure, powder-processed, W metal. High temperature creep properties are another advantage for WC, when considering its high temperature hardness. However, further study of high temperature deformation in binderless WC is needed.

-
—
A WC-FeCr cermet is proposed as a candidate fusion engineering material. The binder system FeCr is attractive because of its low-activation, good irradiation tolerance, and corrosion resistance. A Si-impregnation method has been developed, which enhances oxidation resistance by a factor of 1000 and is stable up to 1200°C.

-
—
The transmutation products of WC-FeCr have been studied. Helium is one product generated excessively, making it a priority for study. Recent results of He implantation into WC-FeCr show good resistance to bubble formation within WC, with larger bubbles forming on the interfaces of tertiary precipitates. Strategies to eliminate these precipitates are suggested.

-
—
There are some areas where an assessment is still not possible. While WC shows promising stability under ion irradiation, more detailed neutron irradiation studies are still very much needed. Furthermore, chemical sputtering at low energies is still poorly understood.


## Acknowledgements

We wish to thank Colin Windsor, Guy Morgan and David Kingham of Tokamak Energy Ltd for invaluable discussions and providing information of transmutation products. We also wish to thank Jessica Marshall and Jonathan Fair of Sandvik Hyperion for discussions and providing WC-FeCr samples. We are grateful to Elsevier Press for permission to reproduce [figure 8](https://pmc.ncbi.nlm.nih.gov#RSTA20170443F8).

## Footnotes

1

Samples with best properties contained small C and W additions to enhance densification.

## Data accessibility

This article has no additional data.

## Authors' contributions

S.A.H.-B. and G.D.W.S. conceived of the study; S.A.H.-B. drafted the manuscript; G.D.W.S. helped draft the manuscript. All authors gave final approval for publication.

## Competing interests

G.D.W.S. is a paid consultant to Tokamak Energy Ltd.

## Funding

S.A.H.-B. thanks the Imperial College Research Fellowship for financial support.

## References

-
1.Clery D.
2015.
The new shape of fusion. Science
348, 854–856. ( 10.1126/science.348.6237.854) [
[DOI](https://doi.org/10.1126/science.348.6237.854)] [[PubMed](https://pubmed.ncbi.nlm.nih.gov/25999489/)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Science&title=The%20new%20shape%20of%20fusion&author=D%20Clery&volume=348&publication_year=2015&pages=854-856&pmid=25999489&doi=10.1126/science.348.6237.854&)] -
2.Sorbom BN, et al.
2015.
ARC: a compact, high-field, fusion nuclear science facility and demonstration power plant with demountable magnets. Fusion Eng. Des.
100, 378–405. ( 10.1016/j.fusengdes.2015.07.008) [
[DOI](https://doi.org/10.1016/j.fusengdes.2015.07.008)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Fusion%20Eng.%20Des.&title=ARC:%20a%20compact,%20high-field,%20fusion%20nuclear%20science%20facility%20and%20demonstration%20power%20plant%20with%20demountable%20magnets&author=BN%20Sorbom&volume=100&publication_year=2015&pages=378-405&doi=10.1016/j.fusengdes.2015.07.008&)] -
3.Costley AE, Hugill J, Buxton PF.
2015.
On the power and size of tokamak fusion pilot plants and reactors. Nucl. Fusion
55, 033001 ( 10.1088/0029-5515/55/3/033001) [
[DOI](https://doi.org/10.1088/0029-5515/55/3/033001)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Nucl.%20Fusion&title=On%20the%20power%20and%20size%20of%20tokamak%20fusion%20pilot%20plants%20and%20reactors&author=AE%20Costley&author=J%20Hugill&author=PF%20Buxton&volume=55&publication_year=2015&pages=033001&doi=10.1088/0029-5515/55/3/033001&)] -
4.Windsor CG, Morgan JG, Buxton PF, Costley AE, Smith GDW, Sykes A.
2016.
Modelling the power deposition into a spherical tokamak fusion power plant. Nucl. Fusion
57, 036001 ( 10.1088/1741-4326/57/3/036001) [
[DOI](https://doi.org/10.1088/1741-4326/57/3/036001)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Nucl.%20Fusion&title=Modelling%20the%20power%20deposition%20into%20a%20spherical%20tokamak%20fusion%20power%20plant&author=CG%20Windsor&author=JG%20Morgan&author=PF%20Buxton&author=AE%20Costley&author=GDW%20Smith&volume=57&publication_year=2016&pages=036001&doi=10.1088/1741-4326/57/3/036001&)] -
5.Menard JE, et al.
2016.
Fusion nuclear science facilities and pilot plants based on the spherical tokamak. Nucl. Fusion
56, 106023 ( 10.1088/0029-5515/56/10/106023) [
[DOI](https://doi.org/10.1088/0029-5515/56/10/106023)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Nucl.%20Fusion&title=Fusion%20nuclear%20science%20facilities%20and%20pilot%20plants%20based%20on%20the%20spherical%20tokamak&author=JE%20Menard&volume=56&publication_year=2016&pages=106023&doi=10.1088/0029-5515/56/10/106023&)] -
6.Hong BG, Hwang Y-S, Kang J, Ono M.
2011.
Conceptual design study of a superconducting spherical tokamak reactor with a self-consistent system analysis code. Nucl. Fusion
51, 113013 ( 10.1088/0029-5515/51/11/113013) [
[DOI](https://doi.org/10.1088/0029-5515/51/11/113013)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Nucl.%20Fusion&title=Conceptual%20design%20study%20of%20a%20superconducting%20spherical%20tokamak%20reactor%20with%20a%20self-consistent%20system%20analysis%20code&author=BG%20Hong&author=Y-S%20Hwang&author=J%20Kang&author=M%20Ono&volume=51&publication_year=2011&pages=113013&doi=10.1088/0029-5515/51/11/113013&)] -
7.El-Guebaly LA.
2006.
Nuclear performance assessment of ARIES-AT. Fusion Eng. Des.
1, 99–110. ( 10.1016/j.fusengdes.2005.06.355) [
[DOI](https://doi.org/10.1016/j.fusengdes.2005.06.355)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Fusion%20Eng.%20Des.&title=Nuclear%20performance%20assessment%20of%20ARIES-AT&author=LA%20El-Guebaly&volume=1&publication_year=2006&pages=99-110&doi=10.1016/j.fusengdes.2005.06.355&)] -
8.Windsor C, Marshall JM, Morgan JG, Fair J, Smith GD, Rajczyk-Wryk A, Tarrago J.
2018.
Design of cemented tungsten carbide and boride-containing shields for a fusion power plant. Nucl. Fusion
58, 076014 ( 10.1088/1741-4326/aabdb0) [
[DOI](https://doi.org/10.1088/1741-4326/aabdb0)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Nucl.%20Fusion&title=Design%20of%20cemented%20tungsten%20carbide%20and%20boride-containing%20shields%20for%20a%20fusion%20power%20plant&author=C%20Windsor&author=JM%20Marshall&author=JG%20Morgan&author=J%20Fair&author=GD%20Smith&volume=58&publication_year=2018&pages=076014&doi=10.1088/1741-4326/aabdb0&)] -
9.Prokopec R, Fischer DX, Weber HW, Eisterer M.
2014.
Suitability of coated conductors for fusion magnets in view of their radiation response. Supercond. Sci. Technol.
28, 014005 ( 10.1088/0953-2048/28/1/014005) [
[DOI](https://doi.org/10.1088/0953-2048/28/1/014005)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Supercond.%20Sci.%20Technol.&title=Suitability%20of%20coated%20conductors%20for%20fusion%20magnets%20in%20view%20of%20their%20radiation%20response&author=R%20Prokopec&author=DX%20Fischer&author=HW%20Weber&author=M%20Eisterer&volume=28&publication_year=2014&pages=014005&doi=10.1088/0953-2048/28/1/014005&)] -
10.Jirsa M, Rameš M, Ďuran I, Viererbl L.
2018.
Effect of neutron irradiation on critical currents of REBaCuO superconducting tapes considered for magnets in fusion reactors. IEEE Trans. Appl. Supercond.
28, 1–5. ( 10.1109/TASC.2018.2804163) [
[DOI](https://doi.org/10.1109/TASC.2018.2804163)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=IEEE%20Trans.%20Appl.%20Supercond.&title=Effect%20of%20neutron%20irradiation%20on%20critical%20currents%20of%20REBaCuO%20superconducting%20tapes%20considered%20for%20magnets%20in%20fusion%20reactors&author=M%20Jirsa&author=M%20Rame%C5%A1&author=I%20%C4%8Euran&author=L%20Viererbl&volume=28&publication_year=2018&pages=1-5&doi=10.1109/TASC.2018.2804163&)] -
11.Fischer DX, Prokopec R, Emhofer J, Eisterer M.
2018.
The effect of fast neutron irradiation on the superconducting properties of REBCO coated conductors with and without artificial pinning centers. Supercond. Sci. Technol.
31, 044006 ( 10.1088/1361-6668/aaadf2) [
[DOI](https://doi.org/10.1088/1361-6668/aaadf2)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Supercond.%20Sci.%20Technol.&title=The%20effect%20of%20fast%20neutron%20irradiation%20on%20the%20superconducting%20properties%20of%20REBCO%20coated%20conductors%20with%20and%20without%20artificial%20pinning%20centers&author=DX%20Fischer&author=R%20Prokopec&author=J%20Emhofer&author=M%20Eisterer&volume=31&publication_year=2018&pages=044006&doi=10.1088/1361-6668/aaadf2&)] -
12.Sorbom BN, et al.
2016.
Determination of Radiation Damage Limits to High-Temperature Superconductors in Reactor-Relevant Conditions to Inform Compact Fusion Reactor Design. In
*26th IAEA Fusion Energy Conf. Kyoto, Japan, 17–22 October*(eds R Kaiser, SM Gonzalez de Vicente, R Kamendje), MTP/P5-35. Vienna, Austria: International Atomic Energy Agency. -
13.Wolfer WG.
2012.
Fundamental properties of defects in metals. In Comprehensive nuclear materials (ed. RJM Konings), pp. 1–45. Amsterdam, The Netherlands: Elsevier. [
[Google Scholar](https://scholar.google.com/scholar_lookup?title=Comprehensive%20nuclear%20materials&author=WG%20Wolfer&publication_year=2012&)] -
14.Linsmeier C, et al.
2017.
Development of advanced high heat flux and plasma-facing materials. Nucl. Fusion
57, 092007 ( 10.1088/1741-4326/aa6f71) [
[DOI](https://doi.org/10.1088/1741-4326/aa6f71)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Nucl.%20Fusion&title=Development%20of%20advanced%20high%20heat%20flux%20and%20plasma-facing%20materials&author=C%20Linsmeier&volume=57&publication_year=2017&pages=092007&doi=10.1088/1741-4326/aa6f71&)] -
15.Zinkle SJ, Snead LL.
2014.
Designing radiation resistance in materials for fusion energy. Ann. Rev. Mater. Res.
44, 241–267. ( 10.1146/annurev-matsci-070813-113627) [
[DOI](https://doi.org/10.1146/annurev-matsci-070813-113627)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Ann.%20Rev.%20Mater.%20Res.&title=Designing%20radiation%20resistance%20in%20materials%20for%20fusion%20energy&author=SJ%20Zinkle&author=LL%20Snead&volume=44&publication_year=2014&pages=241-267&doi=10.1146/annurev-matsci-070813-113627&)] -
16.Gilbert MR, Fleming M, Sublet J-C.
2017.
Automated inventory and material science scoping calculations under fission and fusion conditions. Nucl. Eng. Technol.
49, 1346–1353. ( 10.1016/j.net.2017.07.005) [
[DOI](https://doi.org/10.1016/j.net.2017.07.005)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Nucl.%20Eng.%20Technol.&title=Automated%20inventory%20and%20material%20science%20scoping%20calculations%20under%20fission%20and%20fusion%20conditions&author=MR%20Gilbert&author=M%20Fleming&author=J-C%20Sublet&volume=49&publication_year=2017&pages=1346-1353&doi=10.1016/j.net.2017.07.005&)] -
17.Reiser J, Hoffmann J, Jäntsch U, Klimenkov M, Bonk S, Bonnekoh C, Rieth M, Hoffmann A, Mrotzek T.
2016.
Ductilisation of tungsten (W): On the shift of the brittle-to-ductile transition (BDT) to lower temperatures through cold rolling. Int. J. Refract. Metals Hard Mater.
54, 351–369. ( 10.1016/j.ijrmhm.2015.09.001) [
[DOI](https://doi.org/10.1016/j.ijrmhm.2015.09.001)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Int.%20J.%20Refract.%20Metals%20Hard%20Mater.&title=Ductilisation%20of%20tungsten%20(W):%20On%20the%20shift%20of%20the%20brittle-to-ductile%20transition%20(BDT)%20to%20lower%20temperatures%20through%20cold%20rolling&author=J%20Reiser&author=J%20Hoffmann&author=U%20J%C3%A4ntsch&author=M%20Klimenkov&author=S%20Bonk&volume=54&publication_year=2016&pages=351-369&doi=10.1016/j.ijrmhm.2015.09.001&)] -
18.Antusch S, et al.
2015.
Mechanical and microstructural investigations of tungsten and doped tungsten materials produced via powder injection molding
Nucl. Mater. Energy
3–4, 22–31. [
[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Nucl.%20Mater.%20Energy&author=S%20Antusch&volume=3%E2%80%934&publication_year=2015&pages=22-31&)] -
19.Roebuck B, Almond EA.
1988.
Deformation and fracture processes and the physical metallurgy of WC–Co hardmetals. Int. Mater. Rev.
33, 90–112. ( 10.1179/imr.1988.33.1.90) [
[DOI](https://doi.org/10.1179/imr.1988.33.1.90)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Int.%20Mater.%20Rev.&title=Deformation%20and%20fracture%20processes%20and%20the%20physical%20metallurgy%20of%20WC%E2%80%93Co%20hardmetals&author=B%20Roebuck&author=EA%20Almond&volume=33&publication_year=1988&pages=90-112&doi=10.1179/imr.1988.33.1.90&)] -
20.Okamoto H.
2008.
CW (carbon-tungsten). J. Phase Equilib. Diff
29, 543–544. [
[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Phase%20Equilib.%20Diff&title=CW%20(carbon-tungsten)&author=H%20Okamoto&volume=29&publication_year=2008&pages=543-544&)] -
21.Nagender SVN, Rama PR.
1991.
*BW*(*boron-tungsten*). Phase diagrams of binary tungsten alloys. Calcutta, India: Indian Institute of Metals. [[Google Scholar](https://scholar.google.com/scholar_lookup?title=Phase%20diagrams%20of%20binary%20tungsten%20alloys&author=SVN%20Nagender&author=PR%20Rama&publication_year=1991&)] -
22.Palacios GT, Pastor CJI, Aguirre CMV, Martin SA, Monge MA, Muñoz A, Pareja R.
2013.
Mechanical behavior of tungsten-vanadium-lanthana alloys as function of temperature. J. Nucl. Mater.
442, S277–S281. ( 10.1016/j.jnucmat.2013.02.006) [
[DOI](https://doi.org/10.1016/j.jnucmat.2013.02.006)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Nucl.%20Mater.&title=Mechanical%20behavior%20of%20tungsten-vanadium-lanthana%20alloys%20as%20function%20of%20temperature&author=GT%20Palacios&author=CJI%20Pastor&author=CMV%20Aguirre&author=SA%20Martin&author=MA%20Monge&volume=442&publication_year=2013&pages=S277-S281&doi=10.1016/j.jnucmat.2013.02.006&)] -
23.Imasato S, Tokumoto K, Kitada T, Sakaguchi S.
1995.
Properties of ultra-fine grain binderless cemented carbide ‘RCCFN’. Int. J. Refract. Metals Hard Mater.
5, 305–312. ( 10.1016/0263-4368(95)92676-B) [
[DOI](https://doi.org/10.1016/0263-4368(95)92676-B)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Int.%20J.%20Refract.%20Metals%20Hard%20Mater.&title=Properties%20of%20ultra-fine%20grain%20binderless%20cemented%20carbide%20%E2%80%98RCCFN%E2%80%99&author=S%20Imasato&author=K%20Tokumoto&author=T%20Kitada&author=S%20Sakaguchi&volume=5&publication_year=1995&pages=305-312&doi=10.1016/0263-4368(95)92676-B&)] -
24.Jaensson BO, Sundström BO.
1972.
Determination of Young's modulus and Poisson's ratio for WC–Co alloys by the finite element method. Mater. Sci. Eng.
9, 217–222. ( 10.1016/0025-5416(72)90036-5) [
[DOI](https://doi.org/10.1016/0025-5416(72)90036-5)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Mater.%20Sci.%20Eng.&title=Determination%20of%20Young's%20modulus%20and%20Poisson's%20ratio%20for%20WC%E2%80%93Co%20alloys%20by%20the%20finite%20element%20method&author=BO%20Jaensson&author=BO%20Sundstr%C3%B6m&volume=9&publication_year=1972&pages=217-222&doi=10.1016/0025-5416(72)90036-5&)] -
25.Fang ZZ.
2005.
Correlation of transverse rupture strength of WC–Co with hardness. Int. J. Refract. Met. Hard Mater
23, 119–127. ( 10.1016/j.ijrmhm.2004.11.005) [
[DOI](https://doi.org/10.1016/j.ijrmhm.2004.11.005)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Int.%20J.%20Refract.%20Met.%20Hard%20Mater&title=Correlation%20of%20transverse%20rupture%20strength%20of%20WC%E2%80%93Co%20with%20hardness&author=ZZ%20Fang&volume=23&publication_year=2005&pages=119-127&doi=10.1016/j.ijrmhm.2004.11.005&)] -
26.Wang H, Webb T, Bitler JW.
2015.
Study of thermal expansion and thermal conductivity of cemented WC–Co composite. Int. J. Refract. Metals Hard Mater.
49, 170–177. ( 10.1016/j.ijrmhm.2014.06.009) [
[DOI](https://doi.org/10.1016/j.ijrmhm.2014.06.009)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Int.%20J.%20Refract.%20Metals%20Hard%20Mater.&title=Study%20of%20thermal%20expansion%20and%20thermal%20conductivity%20of%20cemented%20WC%E2%80%93Co%20composite&author=H%20Wang&author=T%20Webb&author=JW%20Bitler&volume=49&publication_year=2015&pages=170-177&doi=10.1016/j.ijrmhm.2014.06.009&)] -
27.Kim HT, Kim JS, Kwon YS.
2005.
Mechanical properties of binderless tungsten carbide by spark plasma sintering. In
*Science and Technology, 2005. KORUS 2005. Proceedings. The 9th Russian-Korean International Symposium on*, pp. 458–461. IEEE. -
28.Shatov AV, Ponomarev SS, Firstov SA.
2014.
1.10 - Fracture and strength of hardmetals at room temperature. In Comprehensive hard materials (ed. Sarin VK.), pp. 301–343. Oxford, UK: Elsevier. [
[Google Scholar](https://scholar.google.com/scholar_lookup?title=Comprehensive%20hard%20materials&author=AV%20Shatov&author=SS%20Ponomarev&author=SA%20Firstov&publication_year=2014&)] -
29.Gubernat A, Rutkowski P, Grabowski G, Zientara D, Gubernat A, Rutkowski P, Grabowski G, Zientara D.
2014.
Hot pressing of tungsten carbide with and without sintering additives. Int. J. Refract. Metals Hard Mater.
43, 193–199. ( 10.1016/j.ijrmhm.2013.12.002) [
[DOI](https://doi.org/10.1016/j.ijrmhm.2013.12.002)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Int.%20J.%20Refract.%20Metals%20Hard%20Mater.&title=Hot%20pressing%20of%20tungsten%20carbide%20with%20and%20without%20sintering%20additives&author=A%20Gubernat&author=P%20Rutkowski&author=G%20Grabowski&author=D%20Zientara&author=A%20Gubernat&volume=43&publication_year=2014&pages=193-199&doi=10.1016/j.ijrmhm.2013.12.002&)] -
30.Tanabe T, Eamchotchawalit C, Busabok C, Taweethavorn S, Fujitsuka M, Shikama T.
2003.
Temperature dependence of thermal conductivity in W and W-Re alloys from 300 to 1000 K. Mater. Lett.
57, 2950–2953. ( 10.1016/S0167-577X(02)01403-9) [
[DOI](https://doi.org/10.1016/S0167-577X(02)01403-9)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Mater.%20Lett.&title=Temperature%20dependence%20of%20thermal%20conductivity%20in%20W%20and%20W-Re%20alloys%20from%20300%20to%201000%E2%80%89K&author=T%20Tanabe&author=C%20Eamchotchawalit&author=C%20Busabok&author=S%20Taweethavorn&author=M%20Fujitsuka&volume=57&publication_year=2003&pages=2950-2953&doi=10.1016/S0167-577X(02)01403-9&)] -
31.Touloukian YS, Powell RW, Ho CY, Klemens PG.
1970.
*Thermal conductivity: metallic elements and alloys*Thermophysical properties of matter: the TPRC data series, vol. 1. Fort Belvoir, VA: Defense Technical Information Center. -
32.Fukuda M, Hasegawa A, Nogami S.
2018.
Thermal properties of pure tungsten and its alloys for fusion applications. Fusion Eng. Des.
132, 1–6. ( 10.1016/j.fusengdes.2018.04.117) [
[DOI](https://doi.org/10.1016/j.fusengdes.2018.04.117)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Fusion%20Eng.%20Des.&title=Thermal%20properties%20of%20pure%20tungsten%20and%20its%20alloys%20for%20fusion%20applications&author=M%20Fukuda&author=A%20Hasegawa&author=S%20Nogami&volume=132&publication_year=2018&pages=1-6&doi=10.1016/j.fusengdes.2018.04.117&)] -
33.Frandsen MV, Williams WS.
1991.
Thermal conductivity and electrical resistivity of cemented transition-metal carbides at low temperatures. J. Am. Ceram. Soc.
74, 1411–1416. ( 10.1111/j.1151-2916.1991.tb04121.x) [
[DOI](https://doi.org/10.1111/j.1151-2916.1991.tb04121.x)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Am.%20Ceram.%20Soc.&title=Thermal%20conductivity%20and%20electrical%20resistivity%20of%20cemented%20transition-metal%20carbides%20at%20low%20temperatures&author=MV%20Frandsen&author=WS%20Williams&volume=74&publication_year=1991&pages=1411-1416&doi=10.1111/j.1151-2916.1991.tb04121.x&)] -
34.Perecherla A, Williams WS.
1988.
Room-temperature thermal conductivity of cemented transition-metal carbides. J. Am. Ceram. Soc.
71, 1130–1133. ( 10.1111/j.1151-2916.1988.tb05804.x) [
[DOI](https://doi.org/10.1111/j.1151-2916.1988.tb05804.x)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Am.%20Ceram.%20Soc.&title=Room-temperature%20thermal%20conductivity%20of%20cemented%20transition-metal%20carbides&author=A%20Perecherla&author=WS%20Williams&volume=71&publication_year=1988&pages=1130-1133&doi=10.1111/j.1151-2916.1988.tb05804.x&)] -
35.Hongbo N, Qisen Z, Jianping Z, Xiao W, Yang Y.
2017.
The preparation, preparation mechanism and properties of extra coarse-grained WC–Co hardmetals. Metal Powder Rep.
72, 188–194. ( 10.1016/j.mprp.2017.01.001) [
[DOI](https://doi.org/10.1016/j.mprp.2017.01.001)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Metal%20Powder%20Rep.&title=The%20preparation,%20preparation%20mechanism%20and%20properties%20of%20extra%20coarse-grained%20WC%E2%80%93Co%20hardmetals&author=N%20Hongbo&author=Z%20Qisen&author=Z%20Jianping&author=W%20Xiao&author=Y%20Yang&volume=72&publication_year=2017&pages=188-194&doi=10.1016/j.mprp.2017.01.001&)] -
36.Pitts RA, et al.
2011.
Physics basis and design of the ITER plasma-facing components. J. Nucl. Mater.
415, S957–S964. ( 10.1016/j.jnucmat.2011.01.114) [
[DOI](https://doi.org/10.1016/j.jnucmat.2011.01.114)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Nucl.%20Mater.&title=Physics%20basis%20and%20design%20of%20the%20ITER%20plasma-facing%20components&author=RA%20Pitts&volume=415&publication_year=2011&pages=S957-S964&doi=10.1016/j.jnucmat.2011.01.114&)] -
37.Hasselman D.
1985.
Thermal stress resistance of engineering ceramics. Mater. Sci. Eng.
71, 251–264. ( 10.1016/0025-5416(85)90235-6) [
[DOI](https://doi.org/10.1016/0025-5416(85)90235-6)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Mater.%20Sci.%20Eng.&title=Thermal%20stress%20resistance%20of%20engineering%20ceramics&author=D%20Hasselman&volume=71&publication_year=1985&pages=251-264&doi=10.1016/0025-5416(85)90235-6&)] -
38.Smith JT, Wood JD.
1968.
Elevated temperature compressive creep behavior of tungsten carbide-cobalt alloys. Acta Metall.
16, 1219–1226. ( 10.1016/0001-6160(68)90003-5) [
[DOI](https://doi.org/10.1016/0001-6160(68)90003-5)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Acta%20Metall.&title=Elevated%20temperature%20compressive%20creep%20behavior%20of%20tungsten%20carbide-cobalt%20alloys&author=JT%20Smith&author=JD%20Wood&volume=16&publication_year=1968&pages=1219-1226&doi=10.1016/0001-6160(68)90003-5&)] -
39.Lay S, Vicens J, Osterstock F.
1987.
High temperature creep of WC-Co alloys. J. Mater. Sci.
22, 1310–1322. ( 10.1007/BF01233127) [
[DOI](https://doi.org/10.1007/BF01233127)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Mater.%20Sci.&title=High%20temperature%20creep%20of%20WC-Co%20alloys&author=S%20Lay&author=J%20Vicens&author=F%20Osterstock&volume=22&publication_year=1987&pages=1310-1322&doi=10.1007/BF01233127&)] -
40.Pisarenko GS, Borisenko VA, Kashtalyan YA.
1964.
The effect of temperature on the hardness and modulus of elasticity of tungsten and molybdenum (20–2700‡). Sov. Powder Metall. Met. Ceram.
1, 371–374. ( 10.1007/BF00774121) [
[DOI](https://doi.org/10.1007/BF00774121)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Sov.%20Powder%20Metall.%20Met.%20Ceram.&title=The%20effect%20of%20temperature%20on%20the%20hardness%20and%20modulus%20of%20elasticity%20of%20tungsten%20and%20molybdenum%20(20%E2%80%932700%E2%80%A1)&author=GS%20Pisarenko&author=VA%20Borisenko&author=YA%20Kashtalyan&volume=1&publication_year=1964&pages=371-374&doi=10.1007/BF00774121&)] -
41.Gibson JS-L, Roberts SG, Armstrong DE.
2015.
High temperature indentation of implanted tungsten. Mater. Sci. Eng. A
74, 380–384. ( 10.1016/j.msea.2014.12.034) [
[DOI](https://doi.org/10.1016/j.msea.2014.12.034)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Mater.%20Sci.%20Eng.%20A&title=High%20temperature%20indentation%20of%20implanted%20tungsten&author=JS-L%20Gibson&author=SG%20Roberts&author=DE%20Armstrong&volume=74&publication_year=2015&pages=380-384&doi=10.1016/j.msea.2014.12.034&)] -
42.Atkins AG, Tabor D.
1966.
Hardness and deformation properties of solids at very high temperatures. Proc. R. Soc. Lond. A
292, 441–459. ( 10.1098/rspa.1966.0146) [
[DOI](https://doi.org/10.1098/rspa.1966.0146)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Proc.%20R.%20Soc.%20Lond.%20A&title=Hardness%20and%20deformation%20properties%20of%20solids%20at%20very%20high%20temperatures&author=AG%20Atkins&author=D%20Tabor&volume=292&publication_year=1966&pages=441-459&doi=10.1098/rspa.1966.0146&)] -
43.Lee M.
1983.
High temperature hardness of tungsten carbide. Metall. Trans. A
14, 1625–1629. ( 10.1007/BF02654390) [
[DOI](https://doi.org/10.1007/BF02654390)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Metall.%20Trans.%20A&title=High%20temperature%20hardness%20of%20tungsten%20carbide&author=M%20Lee&volume=14&publication_year=1983&pages=1625-1629&doi=10.1007/BF02654390&)] -
44.Miyoshi A, Hara A.
1965.
High temperature hardness of WC, TiC, TaC, NbC and their mixed carbides. J. Jpn. Soc. Powder Powder Metall.
12, 78–84. ( 10.2497/jjspm.12.78) [
[DOI](https://doi.org/10.2497/jjspm.12.78)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Jpn.%20Soc.%20Powder%20Powder%20Metall.&title=High%20temperature%20hardness%20of%20WC,%20TiC,%20TaC,%20NbC%20and%20their%20mixed%20carbides&author=A%20Miyoshi&author=A%20Hara&volume=12&publication_year=1965&pages=78-84&doi=10.2497/jjspm.12.78&)] -
45.Milman YV, Luyckx S, Northrop IT..
1999.
Influence of temperature, grain size and cobalt content on the hardness of WC-Co alloys
Int. J. Refractory Metals Hard Materials
17, 39–44. [
[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Int.%20J.%20Refractory%20Metals%20Hard%20Materials&author=YV%20Milman&author=S%20Luyckx&author=IT.%20Northrop&volume=17&publication_year=1999&pages=39-44&)] -
46.Mari D, Bolognini S, Feusier G, Viatte T, Benoit W.
1999.
Experimental strategy to study the mechanical behaviour of hardmetals for cutting tools. Int. J. Refract. Metals Hard Mater.
17, 209–225. ( 10.1016/S0263-4368(98)00078-X) [
[DOI](https://doi.org/10.1016/S0263-4368(98)00078-X)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Int.%20J.%20Refract.%20Metals%20Hard%20Mater.&title=Experimental%20strategy%20to%20study%20the%20mechanical%20behaviour%20of%20hardmetals%20for%20cutting%20tools&author=D%20Mari&author=S%20Bolognini&author=G%20Feusier&author=T%20Viatte&author=W%20Benoit&volume=17&publication_year=1999&pages=209-225&doi=10.1016/S0263-4368(98)00078-X&)] -
47.Keilholtz GW, Moore RE, Osborne MF.
1968.
Fast-neutron effects on the carbides of titanium, zirconium, tantalum, niobium, and tungsten. Nucl. Appl.
4, 330–336. ( 10.13182/NT68-A26398) [
[DOI](https://doi.org/10.13182/NT68-A26398)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Nucl.%20Appl.&title=Fast-neutron%20effects%20on%20the%20carbides%20of%20titanium,%20zirconium,%20tantalum,%20niobium,%20and%20tungsten&author=GW%20Keilholtz&author=RE%20Moore&author=MF%20Osborne&volume=4&publication_year=1968&pages=330-336&doi=10.13182/NT68-A26398&)] -
48.Björkas C, Vörtler K, Nordlund K.
2006.
Major elemental asymmetry and recombination effects in irradiated WC. Phys. Rev. B
74, 140103 ( 10.1103/PhysRevB.74.140103) [
[DOI](https://doi.org/10.1103/PhysRevB.74.140103)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Phys.%20Rev.%20B&title=Major%20elemental%20asymmetry%20and%20recombination%20effects%20in%20irradiated%20WC&author=C%20Bj%C3%B6rkas&author=K%20V%C3%B6rtler&author=K%20Nordlund&volume=74&publication_year=2006&pages=140103&doi=10.1103/PhysRevB.74.140103&)] -
49.Träskelin P, Björkas C, Juslin N, Vörtler K, Nordlund K.
2007.
Radiation damage in WC studied with MD simulations. Nucl. Instrum. Methods Phys. Res. B
1, 614–617. ( 10.1016/j.nimb.2007.01.091) [
[DOI](https://doi.org/10.1016/j.nimb.2007.01.091)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Nucl.%20Instrum.%20Methods%20Phys.%20Res.%20B&title=Radiation%20damage%20in%20WC%20studied%20with%20MD%20simulations&author=P%20Tr%C3%A4skelin&author=C%20Bj%C3%B6rkas&author=N%20Juslin&author=K%20V%C3%B6rtler&author=K%20Nordlund&volume=1&publication_year=2007&pages=614-617&doi=10.1016/j.nimb.2007.01.091&)] -
50.Sun JS, Yan P, Sun XB, Lu G, Liu F, Ye W, Yang JQ.
1997.
Tribological properties of nitrogen ion implanted WC-Co. Wear
213, 131–134. ( 10.1016/S0043-1648(97)00165-8) [
[DOI](https://doi.org/10.1016/S0043-1648(97)00165-8)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Wear&title=Tribological%20properties%20of%20nitrogen%20ion%20implanted%20WC-Co&author=JS%20Sun&author=P%20Yan&author=XB%20Sun&author=G%20Lu&author=F%20Liu&volume=213&publication_year=1997&pages=131-134&doi=10.1016/S0043-1648(97)00165-8&)] -
51.Anderson AD, Loretto MH, Dearnaley G.
1988.
Microstructural study of ion-implanted WC–Co. Mater. Sci. Eng. A
105, 503–507. ( 10.1016/0025-5416(88)90735-5) [
[DOI](https://doi.org/10.1016/0025-5416(88)90735-5)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Mater.%20Sci.%20Eng.%20A&title=Microstructural%20study%20of%20ion-implanted%20WC%E2%80%93Co&author=AD%20Anderson&author=MH%20Loretto&author=G%20Dearnaley&volume=105&publication_year=1988&pages=503-507&doi=10.1016/0025-5416(88)90735-5&)] -
52.Baik S-I, Choi E-G, Jun J-H, Kim Y-W.
2008.
Defect structure induced by ion injection in WC–Co. Scr. Mater.
58, 614–617. ( 10.1016/j.scriptamat.2007.11.026) [
[DOI](https://doi.org/10.1016/j.scriptamat.2007.11.026)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Scr.%20Mater.&title=Defect%20structure%20induced%20by%20ion%20injection%20in%20WC%E2%80%93Co&author=S-I%20Baik&author=E-G%20Choi&author=J-H%20Jun&author=Y-W%20Kim&volume=58&publication_year=2008&pages=614-617&doi=10.1016/j.scriptamat.2007.11.026&)] -
53.Singh A, Derry TE, Luyckx SB, Sellschop JPF.
1990.
X-ray photoelectron spectroscopy of nitrogen-implanted cemented tungsten carbide (WC-Co). J. Mater. Sci. Lett.
9, 1101–1102. ( 10.1007/BF00727890) [
[DOI](https://doi.org/10.1007/BF00727890)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Mater.%20Sci.%20Lett.&title=X-ray%20photoelectron%20spectroscopy%20of%20nitrogen-implanted%20cemented%20tungsten%20carbide%20(WC-Co)&author=A%20Singh&author=TE%20Derry&author=SB%20Luyckx&author=JPF%20Sellschop&volume=9&publication_year=1990&pages=1101-1102&doi=10.1007/BF00727890&)] -
54.Karioris FG, Özkan H, Luyckx SB, Cartz L.
1990.
The stability of WC to ion bombardment. Nucl. Instrum. Methods Phys. Res. B
46, 176–179. ( 10.1016/0168-583X(90)90693-O) [
[DOI](https://doi.org/10.1016/0168-583X(90)90693-O)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Nucl.%20Instrum.%20Methods%20Phys.%20Res.%20B&title=The%20stability%20of%20WC%20to%20ion%20bombardment&author=FG%20Karioris&author=H%20%C3%96zkan&author=SB%20Luyckx&author=L%20Cartz&volume=46&publication_year=1990&pages=176-179&doi=10.1016/0168-583X(90)90693-O&)] -
55.Burnett PJ, Page TF.
1986.
Criteria for mechanical property modifications of ceramic surfaces by ion implantation. Radiat. Eff.
97, 283–296. ( 10.1080/00337578608226019) [
[DOI](https://doi.org/10.1080/00337578608226019)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Radiat.%20Eff.&title=Criteria%20for%20mechanical%20property%20modifications%20of%20ceramic%20surfaces%20by%20ion%20implantation&author=PJ%20Burnett&author=TF%20Page&volume=97&publication_year=1986&pages=283-296&doi=10.1080/00337578608226019&)] -
56.Plank H, Eckstein W.
1997.
Preferential sputtering of carbides under deuterium irradiation—a comparison between experiment and computer simulation. Nucl. Instrum. Methods Phys. Res. B
124, 23–30. ( 10.1016/S0168-583X(97)00113-4) [
[DOI](https://doi.org/10.1016/S0168-583X(97)00113-4)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Nucl.%20Instrum.%20Methods%20Phys.%20Res.%20B&title=Preferential%20sputtering%20of%20carbides%20under%20deuterium%20irradiation%E2%80%94a%20comparison%20between%20experiment%20and%20computer%20simulation&author=H%20Plank&author=W%20Eckstein&volume=124&publication_year=1997&pages=23-30&doi=10.1016/S0168-583X(97)00113-4&)] -
57.Träskelin P, Juslin N, Erhart P, Nordlund K.
2007.
Molecular dynamics simulations of hydrogen bombardment of tungsten carbide surfaces. Phys. Rev. B
75, 174113 ( 10.1103/PhysRevB.75.174113) [
[DOI](https://doi.org/10.1103/PhysRevB.75.174113)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Phys.%20Rev.%20B&title=Molecular%20dynamics%20simulations%20of%20hydrogen%20bombardment%20of%20tungsten%20carbide%20surfaces&author=P%20Tr%C3%A4skelin&author=N%20Juslin&author=P%20Erhart&author=K%20Nordlund&volume=75&publication_year=2007&pages=174113&doi=10.1103/PhysRevB.75.174113&)] -
58.Horikawa T, Tsuchiya B, Morita K.
1998.
Retention and re-emission of deuterium implanted into tungsten monocarbide. J. Nucl. Mater.
258–263, 1087–1091. ( 10.1016/S0022-3115(98)00279-7) [
[DOI](https://doi.org/10.1016/S0022-3115(98)00279-7)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Nucl.%20Mater.&title=Retention%20and%20re-emission%20of%20deuterium%20implanted%20into%20tungsten%20monocarbide&author=T%20Horikawa&author=B%20Tsuchiya&author=K%20Morita&volume=258%E2%80%93263&publication_year=1998&pages=1087-1091&doi=10.1016/S0022-3115(98)00279-7&)] -
59.Igarashi E, Nishikawa Y, Nakahata T, Yoshikawa A, Oyaidzu M, Oya Y, Okuno K.
2007.
Dependence of implantation temperature on chemical behavior of energetic deuterium implanted into tungsten carbide. J. Nucl. Mater.
363–365, 910–914. ( 10.1016/j.jnucmat.2007.01.113) [
[DOI](https://doi.org/10.1016/j.jnucmat.2007.01.113)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Nucl.%20Mater.&title=Dependence%20of%20implantation%20temperature%20on%20chemical%20behavior%20of%20energetic%20deuterium%20implanted%20into%20tungsten%20carbide&author=E%20Igarashi&author=Y%20Nishikawa&author=T%20Nakahata&author=A%20Yoshikawa&author=M%20Oyaidzu&volume=363%E2%80%93365&publication_year=2007&pages=910-914&doi=10.1016/j.jnucmat.2007.01.113&)] -
60.Kimura H, Nishikawa Y, Nakahata T, Oyaidzu M, Oya Y, Okuno K.
2006.
Chemical behavior of energetic deuterium implanted into tungsten carbide. Fusion Eng. Des.
1, 295–299. ( 10.1016/j.fusengdes.2005.09.024) [
[DOI](https://doi.org/10.1016/j.fusengdes.2005.09.024)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Fusion%20Eng.%20Des.&title=Chemical%20behavior%20of%20energetic%20deuterium%20implanted%20into%20tungsten%20carbide&author=H%20Kimura&author=Y%20Nishikawa&author=T%20Nakahata&author=M%20Oyaidzu&author=Y%20Oya&volume=1&publication_year=2006&pages=295-299&doi=10.1016/j.fusengdes.2005.09.024&)] -
61.Haasz AA, Davis JW.
1997.
Deuterium retention in beryllium, molybdenum and tungsten at high fluences. J. Nucl. Mater.
241, 1076–1081. ( 10.1016/S0022-3115(97)80197-3) [
[DOI](https://doi.org/10.1016/S0022-3115(97)80197-3)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Nucl.%20Mater.&title=Deuterium%20retention%20in%20beryllium,%20molybdenum%20and%20tungsten%20at%20high%20fluences&author=AA%20Haasz&author=JW%20Davis&volume=241&publication_year=1997&pages=1076-1081&doi=10.1016/S0022-3115(97)80197-3&)] -
62.Kong X-S, You Y-W, Liu CS, Fang QF, Chen J-L, Luo G-N.
2011.
First principles study of hydrogen behaviors in hexagonal tungsten carbide. J. Nucl. Mater.
1, 233–238. ( 10.1016/j.jnucmat.2011.07.004) [
[DOI](https://doi.org/10.1016/j.jnucmat.2011.07.004)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Nucl.%20Mater.&title=First%20principles%20study%20of%20hydrogen%20behaviors%20in%20hexagonal%20tungsten%20carbide&author=X-S%20Kong&author=Y-W%20You&author=CS%20Liu&author=QF%20Fang&author=J-L%20Chen&volume=1&publication_year=2011&pages=233-238&doi=10.1016/j.jnucmat.2011.07.004&)] -
63.Burr PA, Oliver SX.
2018.
Formation and migration of point defects in tungsten carbide: unveiling the sluggish bulk self-diffusivity of WC. J. Eur. Ceram. Soc.
39, 165–172. [
[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Eur.%20Ceram.%20Soc.&title=Formation%20and%20migration%20of%20point%20defects%20in%20tungsten%20carbide:%20unveiling%20the%20sluggish%20bulk%20self-diffusivity%20of%20WC&author=PA%20Burr&author=SX%20Oliver&volume=39&publication_year=2018&pages=165-172&)] -
64.Ojo-Kupoluyi OJ, Tahir SM, Baharudin BTHT, Hanim MAA, Anuar MS.
2016.
Mechanical properties of WC-based hardmetals bonded with iron alloys—a review. Mater. Sci. Technol.
33, 1–11. ( 10.1080/02670836.2016.1186929) [
[DOI](https://doi.org/10.1080/02670836.2016.1186929)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Mater.%20Sci.%20Technol.&title=Mechanical%20properties%20of%20WC-based%20hardmetals%20bonded%20with%20iron%20alloys%E2%80%94a%20review&author=OJ%20Ojo-Kupoluyi&author=SM%20Tahir&author=BTHT%20Baharudin&author=MAA%20Hanim&author=MS%20Anuar&volume=33&publication_year=2016&pages=1-11&doi=10.1080/02670836.2016.1186929&)] -
65.Shatov AV, Ponomarev SS, Firstov SA.
2014.
1.09 - Hardness and deformation of hardmetals at room temperature. In Comprehensive hard materials (ed. Sarin VK.), pp. 267–299. Oxford, UK: Elsevier. [
[Google Scholar](https://scholar.google.com/scholar_lookup?title=Comprehensive%20hard%20materials&author=AV%20Shatov&author=SS%20Ponomarev&author=SA%20Firstov&publication_year=2014&)] -
66.Gurland J.
1988.
New scientific approaches to development of tool materials. Int. Mater. Rev.
33, 151–166. ( 10.1179/imr.1988.33.1.151) [
[DOI](https://doi.org/10.1179/imr.1988.33.1.151)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Int.%20Mater.%20Rev.&title=New%20scientific%20approaches%20to%20development%20of%20tool%20materials&author=J%20Gurland&volume=33&publication_year=1988&pages=151-166&doi=10.1179/imr.1988.33.1.151&)] -
67.Penrice TW.
1987.
Alternative binders for hard metals. J. Mater. Shaping Technol.
5, 35–39. ( 10.1007/BF02833684) [
[DOI](https://doi.org/10.1007/BF02833684)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Mater.%20Shaping%20Technol.&title=Alternative%20binders%20for%20hard%20metals&author=TW%20Penrice&volume=5&publication_year=1987&pages=35-39&doi=10.1007/BF02833684&)] -
68.Humphry-Baker SA, Marshall JM, Smith GDW, Lee WE.
2017.
Thermophysical properties of Co-free WC-FeCr hardmetals. In Proceedings of the 19th International Plansee Seminar, Reutte, Austria, HM 19. [
[Google Scholar](https://scholar.google.com/scholar_lookup?Humphry-Baker%20SA,%20Marshall%20JM,%20Smith%20GDW,%20Lee%20WE.%202017.%20Thermophysical%20properties%20of%20Co-free%20WC-FeCr%20hardmetals.%20In%20Proceedings%20of%20the%2019th%20International%20Plansee%20Seminar,%20Reutte,%20Austria,%20HM%2019.)] -
69.Schubert WD, Fugger M, Wittmann B, Useldinger R.
2015.
Aspects of sintering of cemented carbides with Fe-based binders. Int. J. Refract. Metals Hard Mater.
49, 110–123. ( 10.1016/j.ijrmhm.2014.07.028) [
[DOI](https://doi.org/10.1016/j.ijrmhm.2014.07.028)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Int.%20J.%20Refract.%20Metals%20Hard%20Mater.&title=Aspects%20of%20sintering%20of%20cemented%20carbides%20with%20Fe-based%20binders&author=WD%20Schubert&author=M%20Fugger&author=B%20Wittmann&author=R%20Useldinger&volume=49&publication_year=2015&pages=110-123&doi=10.1016/j.ijrmhm.2014.07.028&)] -
70.Wittmann B, Schubert W-D, Lux B.
2002.
WC grain growth and grain growth inhibition in nickel and iron binder hardmetals. Int. J. Refract. Metals Hard Mater.
20, 51–60. ( 10.1016/S0263-4368(01)00070-1) [
[DOI](https://doi.org/10.1016/S0263-4368(01)00070-1)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Int.%20J.%20Refract.%20Metals%20Hard%20Mater.&title=WC%20grain%20growth%20and%20grain%20growth%20inhibition%20in%20nickel%20and%20iron%20binder%20hardmetals&author=B%20Wittmann&author=W-D%20Schubert&author=B%20Lux&volume=20&publication_year=2002&pages=51-60&doi=10.1016/S0263-4368(01)00070-1&)] -
71.Haneda K, Morrish AH.
1979.
Oxidation of aerosoled ultrafine iron particles. Nature
282, 186–188. ( 10.1038/282186a0) [
[DOI](https://doi.org/10.1038/282186a0)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Nature&title=Oxidation%20of%20aerosoled%20ultrafine%20iron%20particles&author=K%20Haneda&author=AH%20Morrish&volume=282&publication_year=1979&pages=186-188&doi=10.1038/282186a0&)] -
72.Budylkin NI, Mironova EG, Chernov VM, Krasnoselov VA, Porollo SI, Garner FA.
2008.
Neutron-induced swelling and embrittlement of pure iron and pure nickel irradiated in the BN-350 and BOR-60 fast reactors. J. Nucl. Mater.
3, 359–364. ( 10.1016/j.jnucmat.2008.01.015) [
[DOI](https://doi.org/10.1016/j.jnucmat.2008.01.015)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Nucl.%20Mater.&title=Neutron-induced%20swelling%20and%20embrittlement%20of%20pure%20iron%20and%20pure%20nickel%20irradiated%20in%20the%20BN-350%20and%20BOR-60%20fast%20reactors&author=NI%20Budylkin&author=EG%20Mironova&author=VM%20Chernov&author=VA%20Krasnoselov&author=SI%20Porollo&volume=3&publication_year=2008&pages=359-364&doi=10.1016/j.jnucmat.2008.01.015&)] -
73.Kohyama A, Hishinuma A, Gelles DS, Klueh RL, Dietz W, Ehrlich K.
1996.
Low-activation ferritic and martensitic steels for fusion application. J. Nucl. Mater.
233, 138–147. ( 10.1016/S0022-3115(96)00327-3) [
[DOI](https://doi.org/10.1016/S0022-3115(96)00327-3)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Nucl.%20Mater.&title=Low-activation%20ferritic%20and%20martensitic%20steels%20for%20fusion%20application&author=A%20Kohyama&author=A%20Hishinuma&author=DS%20Gelles&author=RL%20Klueh&author=W%20Dietz&volume=233&publication_year=1996&pages=138-147&doi=10.1016/S0022-3115(96)00327-3&)] -
74.Footner PK, Holmes DR, Mortimer D.
1967.
Oxidation of iron–chromium binary alloys. Nature
216, 54 ( 10.1038/216054a0) [
[DOI](https://doi.org/10.1038/216054a0)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Nature&title=Oxidation%20of%20iron%E2%80%93chromium%20binary%20alloys&author=PK%20Footner&author=DR%20Holmes&author=D%20Mortimer&volume=216&publication_year=1967&pages=54&doi=10.1038/216054a0&)] -
75.Humphry-Baker SA, Lee WE.
2016.
Tungsten carbide is more oxidation resistant than tungsten when processed to full density. Scr. Mater.
116, 67–70. ( 10.1016/j.scriptamat.2016.01.007) [
[DOI](https://doi.org/10.1016/j.scriptamat.2016.01.007)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Scr.%20Mater.&title=Tungsten%20carbide%20is%20more%20oxidation%20resistant%20than%20tungsten%20when%20processed%20to%20full%20density&author=SA%20Humphry-Baker&author=WE%20Lee&volume=116&publication_year=2016&pages=67-70&doi=10.1016/j.scriptamat.2016.01.007&)] -
76.Humphry-Baker SA, Peng K, Lee WE.
2017.
Oxidation resistant tungsten carbide hardmetals. Int. J. Refract. Metals Hard Mater.
66, 135–143. ( 10.1016/j.ijrmhm.2017.03.009) [
[DOI](https://doi.org/10.1016/j.ijrmhm.2017.03.009)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Int.%20J.%20Refract.%20Metals%20Hard%20Mater.&title=Oxidation%20resistant%20tungsten%20carbide%20hardmetals&author=SA%20Humphry-Baker&author=K%20Peng&author=WE%20Lee&volume=66&publication_year=2017&pages=135-143&doi=10.1016/j.ijrmhm.2017.03.009&)] -
77.Webb WW, Norton JT, Wagner C.
1956.
Oxidation studies in metal-carbon systems. J. Electrochem. Soc.
103, 112–117. ( 10.1149/1.2430239) [
[DOI](https://doi.org/10.1149/1.2430239)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Electrochem.%20Soc.&title=Oxidation%20studies%20in%20metal-carbon%20systems&author=WW%20Webb&author=JT%20Norton&author=C%20Wagner&volume=103&publication_year=1956&pages=112-117&doi=10.1149/1.2430239&)] -
78.Humphry-Baker S, Marshall J.
2018.
Structure and properties of high-hardness silicide coatings on cemented carbides for high temperature applications. Coatings
8, 247 ( 10.3390/coatings8070247) [
[DOI](https://doi.org/10.3390/coatings8070247)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Coatings&title=Structure%20and%20properties%20of%20high-hardness%20silicide%20coatings%20on%20cemented%20carbides%20for%20high%20temperature%20applications&author=S%20Humphry-Baker&author=J%20Marshall&volume=8&publication_year=2018&pages=247&doi=10.3390/coatings8070247&)] -
79.Kim H-S, Yoon J-K, Kim G-H, Doh J-M, Kwun S-I, Hong K-T.
2008.
Growth behavior and microstructure of oxide scales grown on WSi
2coating. Intermetallics 16, 360–372. ( 10.1016/j.intermet.2007.11.008) [[DOI](https://doi.org/10.1016/j.intermet.2007.11.008)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Intermetallics&title=Growth%20behavior%20and%20microstructure%20of%20oxide%20scales%20grown%20on%20WSi2%20coating&author=H-S%20Kim&author=J-K%20Yoon&author=G-H%20Kim&author=J-M%20Doh&author=S-I%20Kwun&volume=16&publication_year=2008&pages=360-372&doi=10.1016/j.intermet.2007.11.008&)] -
80.Windsor CG, Morgan JG.
2017.
Neutron and gamma flux distributions and their implications for radiation damage in the shielded superconducting core of a fusion power plant. Nucl. Fusion
57, 116032. [
[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Nucl.%20Fusion&title=Neutron%20and%20gamma%20flux%20distributions%20and%20their%20implications%20for%20radiation%20damage%20in%20the%20shielded%20superconducting%20core%20of%20a%20fusion%20power%20plant&author=CG%20Windsor&author=JG%20Morgan&volume=57&publication_year=2017&pages=116032&)] -
81.Humphry-Baker SA, Harrison RW, Greaves G, Knowles AJ, Smith GDW, Donnelly SE, Lee WE.
2018.
A candidate fusion engineering material, WC-FeCr. Scr. Mater.
155, 129–133. ( 10.1016/j.scriptamat.2018.06.027) [
[DOI](https://doi.org/10.1016/j.scriptamat.2018.06.027)] [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Scr.%20Mater.&title=A%20candidate%20fusion%20engineering%20material,%20WC-FeCr&author=SA%20Humphry-Baker&author=RW%20Harrison&author=G%20Greaves&author=AJ%20Knowles&author=GDW%20Smith&volume=155&publication_year=2018&pages=129-133&doi=10.1016/j.scriptamat.2018.06.027&)]

## Associated Data

*This section collects any data citations, data availability statements, or supplementary materials included in this article.*

### Data Availability Statement

This article has no additional data.