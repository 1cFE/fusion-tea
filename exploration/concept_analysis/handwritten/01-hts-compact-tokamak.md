# **D-T Tokamak Reactors: Concept Assessment for Techno-Economic Analysis**

---

## **Availability of Data**

The D-T magnetic confinement tokamak is by far the most extensively documented fusion concept. Key data sources include:

* [ARIES (ST, CS, and AT variants)](https://qedfusion.org/DOCS/bib.shtml) \- late 90s/ early 00s studies on tokamaks \+ stellarators  
* MIT’s ARC tokamak using HTS.  See ARC’s [conceptual design paper](https://www.sciencedirect.com/science/article/abs/pii/S0920379615302337) (Sorbom et al. 2015), [*Techno-economic Analysis of Deuterium-Tritium Magnetic Confinement Fusion Power Plants*](https://www.sciencedirect.com/science/article/abs/pii/S0306261925012978)  ( Araiinejad \+ Shirvan, 2025), and [Fusion economics: power density, materials and maintenance](https://cassyni.com/events/9cAmGbWrQGhaYbnkx4rLzq) (D. Whyte, 2024\)  
* Chen et al.’s CFETR [cost analysis](https://www.scribd.com/document/762574274/s10894-014-9770-x) (2015)  
* [ITER cost data](https://www.iter.org/sites/default/files/media/2025-11/rapport-financier-iter-2024-web.pdf) (less applicable for NOAK studies)  
* [PROCESS UKAEA model](https://ukaea.github.io/PROCESS/fusion-devices/spherical-tokamak/)  
* [Woodruff Scientific’s pyFECONS framework](https://arxiv.org/abs/2601.21724)   
* For Spherical Tokamaks- [Hidalgo-Salaverri et al, (2025)](https://iopscience.iop.org/article/10.1088/1741-4326/adaa01/pdf) and [Foster et al, 2024](https://scientific-publications.ukaea.uk/wp-content/uploads/Extrapolating_Costs_to_Commercial_Fusion_Power_Plants.pdf)  
* For intra-MCF comparison- [TG Brown, 2018](https://ieeexplore.ieee.org/abstract/document/8361148)

This techno-economic analysis draws on a diverse range of sources, including the only publicly available detailed cost study for China’s Fusion Engineering Test Reactor (CFETR). China’s accelerating tokamak program merits consideration, fueled by recent confinement milestones and over $6 billion in state fusion funding.  In the USA, Commonwealth Fusion Systems (CFS) is the leading private tokamak developer with nearly $3 billion in funding. While CFS hasn’t released detailed costing info, their academic counterparts at MIT’s Plasma Science & Fusion Center have published useful TEAs (Sorbom, Araiinejad, Whyte).  Lastly, the UKAEA has released useful costing and performance models, particularly as they relate to spherical tokamaks (Foster, Hidalgo-Salaverri).

## **Challenges in Capturing System Function**

While sources differ on the exact rankings, the largest LCOE drivers are generally shown to be:

1) **Reactor CAPEX** *(driven primarily by magnets, blanket/shielding, and building costs)*  
2) **Capacity factor** *(driven primarily by maintenance downtime in D-T tokamaks)*  
3) **Regulatory factors** (*higher indirect costs, increased building costs, and decreased CF)*  
4) **Discount rate** (*controls how heavily future energy throughput and cash flows are discounted relative to high upfront CAPEX)*  
5) **Lifetime replacement costs** *(high uncertainty, high potential learning rate)*  
6) **Power conversion efficiency** *(Indirectly affects reactor sizing and capital cost)*

*Honorable mention: Q\_eng affects the sizing of the reactor vessel, plasma heating/current drives, turbine/generator systems, etc. However, LCOE becomes less sensitive to Q\_eng at higher nominal gain.*

Each of these LCOE drivers carries a significant amount of uncertainty. Capacity factor depends critically on unproven FW/blanket/divertor replacement and remote-handling schemes at scale.  Q\_eng remains highly uncertain and emerges from plant-specific trade-offs in physics performance and auxiliary systems. Within the reactor vessel, blanket costs are sensitive to required tritium breeding performance, neutron damage resistance, and power conversion efficiencies– all of which remain in the experimental validation phase. HTS magnets have an underdeveloped supply chain and rapidly-evolving durability and current density limits.

Another major uncertainty is the regulatory framework. A study by Stewart & Shirvan (2022) demonstrates that applying fission-style nuclear regulation results in a 2.2× markup on fusion reactor building costs. Araiinejad’s study combines this building cost factor with higher indirect cost percentages and a reduced capacity factor, nearly doubling the overnight capital cost and quadrupling the LCOE spread. The 2023 NRC decision to regulate fusion under 10 CFR Part 30 is favorable but the detailed rulemaking remains incomplete, leaving the actual regulatory cost burden unresolved.

## **Maturity of Key Subsystems and Components**

The key subsystems of a Tokamak FPP are listed below, in order of ascending maturity. 

### **Integrated breeding blanket, TRL \~3–4**

* **Demonstrated**: Small-scale tritium breeding experiments (LIBRA/BABY series with D-T neutrons), helium-cooled pebble-bed and water-cooled lead-lithium mock-ups, neutron irradiation tests up to \~30–50 dpa in fission reactors. ITER TBM designs are in detailed engineering (Preliminary Design Review expected 2026).  
* **On paper only**: Full-scale, high-fluence, long-term integrated blanket modules operating under simultaneous neutron \+ heat \+ tritium extraction \+ structural loads.  
* **Missing at scale**: 14 MeV neutron testing at fusion-relevant fluences (150–200 dpa lifetime), industrial-scale lithium ceramic/liquid breeder fabrication, tritium extraction systems at kg/day rates, and structural materials (e.g., advanced RAFM steels or SiC composites) proven under combined fusion conditions. No facility yet provides the full environment.

### **Tritium Fuel Cycle & Extraction, TRL 4–5**

* **Demonstrated**: Lab-scale tritium handling loops, permeation barriers, and extraction from liquid/solid breeders. JET and TFTR historically handled gram quantities.  
* **On paper only**: Closed-loop, kg/day scale, self-sufficient fuel cycle with \<1% losses.  
* **Missing at scale**: Industrial tritium processing plants, low-inventory storage, and permeation-resistant materials at power-plant throughput.

### **Remote Maintenance & Remote Handling, TRL 5–6**

* **Demonstrated**: ITER remote handling prototypes and full-scale mock-ups for blanket/divertor exchange.  
* **On paper only**: Reliable, high-availability remote maintenance for a power plant operating at \>80% availability with activated components.  
* **Missing at scale**: Radiation-hardened robotics that can operate inside the vessel for years with minimal human intervention.

### **Divertor, TRL 5–7** 

* **Demonstrated**: ITER-style tungsten monoblock divertors tested at relevant heat fluxes (\>10–20 MW/m²) in facilities like WEST, GLADIS, and DTT prototypes. Detached/radiative divertor operation shown in multiple tokamaks (DIII-D, JET, AUG).  
* **On paper only**: Advanced concepts like liquid-metal or “snowflake” divertors at full power-plant scale and lifetime.  
* **Missing at scale**: Materials that survive 10–20 MW/m² steady-state \+ neutron damage for years, plus large-area manufacturing and remote-replacement systems.

### **HTS Magnets, TRL 5–8** 

* **Demonstrated**: Full-scale TF coils at 20 T (CFS SPARC prototype magnet delivered and under testing, Jan 2026). Tokamak Energy Demo4 achieved 11.8 T in full tokamak configuration (Nov 2025). Large-bore HTS coils have been tested under relevant mechanical/thermal loads.  
* **Missing at scale**: Reliable km-scale REBCO tape production with consistent Jc (\>150 MA/cm² at 20 K, 20 T), radiation-hardened insulation, and quench-protection systems for neutron environments. Structural delamination and long-term fatigue under combined high-field \+ cyclic loads still need more data. Supply chain is ramping fast but not yet at the thousands-of-km-per-year level needed for multiple plants.

### **Heating & Current Drive (NBI, ECRH, ICRH, LH), TRL 6–8**

* **Demonstrated**: MW-class gyrotrons (170 GHz), neutral beam injectors, and RF systems routinely operated on existing tokamaks (ITER injectors under construction, SPARC/EAST/JT-60SA upgrades).  
* **Missing at scale**: Continuous-wave, high-efficiency systems at the 50–100 MW level with \>50% wall-plug efficiency and long-term reliability under neutron/gamma background.

### **Vacuum Vessel & In-Vessel Structures, TRL 7–8**

* **Demonstrated**: ITER vacuum vessel sectors are being manufactured and welded at full scale. Double-wall stainless steel designs with shielding are proven in concept.  
* **Missing at scale**: the challenge is integration with blanket/divertor modules at power-plant size and neutron activation levels.

### **Cryogenics & Thermal Management, TRL 7–8**

* **Demonstrated**: Large-scale helium refrigeration plants (ITER-scale already built/tested).  
* **Missing at scale**: efficiency at 20 K (for HTS) still needs optimization.

### **Balance of Plant (Power Conversion, Turbine, Heat Rejection), TRL 8–9**

* **Demonstrated**: Conventional Rankine/Brayton/sCO₂ cycles at GW scale in fission and fossil plants.  
* **Missing at scale**: Integration with fusion-specific heat sources (pulsed vs steady-state, tritium-compatible heat exchangers, high neutron flux on primary loops).

## **Key Materials and Supply Chain Considerations**

The tokamak supply chain faces several material constraints that could gate deployment timelines.

**REBCO superconducting tape** is the most immediate bottleneck. Global REBCO production capacity is currently on the order of thousands of kilometers per year, while a single ARC-class reactor requires \>5,000 km. Scaling production by one to two orders of magnitude while reducing cost (from current prices of roughly $30–100/kA-m toward the $10/kA-m range needed for commercial viability) requires massive capital investment in tape manufacturing facilities. Key REBCO manufacturers are Shanghai Superconductor Technology, Faraday Factory Japan, and CFS.

**Tritium** is the rarest material in this supply chain. The global tritium inventory is approximately 25–30 kg, produced primarily as a byproduct of CANDU heavy-water reactors, and decays at 5.5% per year. A single D-T reactor startup requires on the order of 1 kg, and the plant must breed its own tritium during operation (TBR \> 1). As CANDU reactors age and retire, the external tritium supply will shrink. This creates a sequencing constraint: the first few fusion plants must demonstrate tritium self-sufficiency before the fleet can scale, and there is limited margin for breeding shortfalls. The tritium fuel cycle — including extraction from FLiBe, purification, storage, and accountability — involves handling a radioactive gas with extremely low tolerable release limits, adding complexity to plant design and operations.  The current market rate for Tritium is \> $35,000/kg.

**FLiBe molten salt** (Li₂BeF₄) is not currently produced at industrial scale. Beryllium, a component of FLiBe, is toxic and produced in limited quantities globally (roughly 300 tonnes/year, dominated by a single US producer, Materion Corp). Lithium enrichment for tritium breeding adds further costs, with only a few suppliers in the world producing small quantities of 90+% Li-6 (Russia and China still use a mercury-based enrichment process that is banned elsewhere). The Araiinejad study estimates that the future NOAK cost of FLiBe could be approximately $154/kg, assuming a 20% learning rate. FLiBe has a shared supply chain with certain fission concepts (i.e. Kairos Power), which could aid its economies of scale. 

**Vanadium alloys** (V-4Cr-4Ti) are an option for FPP first wall structures due to their low neutron activation properties. Vanadium is produced primarily as a byproduct of steel and titanium processing, with global production around 100,000 tonnes/year — adequate for a fleet of reactors, but the specific alloy grade (V-4Cr-4Ti with controlled impurities) has never been produced at the multi-hundred-tonne scale required for a single vacuum vessel. V-4Cr-4Ti market cost is approximately $37/kg including a 15% purity premium, but this is extrapolated from commodity metal prices rather than actual procurement of nuclear-grade alloy.

**Tungsten** for the first wall and divertor is available in adequate supply but presents manufacturing challenges — fabricating large, precisely shaped tungsten components that can withstand extreme heat loads and thermal cycling without cracking remains an active area of materials research.

## **Conclusions & Next Steps**

D-T tokamaks offer the most mature path to fusion power but still face high uncertainties such as capacity factor, magnet and blanket supply chains, and regulatory costs.  The majority of the Tokamak TEA model will focus on these high-uncertainty areas. Additionally, a simplified 1D physics model becomes necessary to keep all costing inputs self-consistent, and to allow for changes to external factors such as superconductor or blanket performance. Each costing category will receive a unique approach based on a comprehensive survey of the sources above. The latest  model structure and individual costing strategies are documented [here](https://app.vexlio.com/d/_6Ej8JkBSK67-aSrDVDvGw).  A more in-depth outline of each cost category within first-pass scope is captured [here](https://docs.google.com/document/d/1pDJpuWsWYCxshqDQ0kavFBC2pjSwrer3p_cRYsIleGA/edit?usp=sharing).

---

*Primary Sources:*

*Araiinejad, L.S. and Shirvan, K. (2025) 'Techno-economic analysis of deuterium-tritium magnetic confinement fusion power plants', Applied Energy, 401(Part B), 126567\. doi:10.1016/j.apenergy.2025.126567.*

*ARIES Team (various dates, late 1990s–early 2000s) ARIES-ST and related tokamak/stellarator conceptual design studies. University of California, San Diego / ARIES Project. Available at: https://qedfusion.org/DOCS/bib.shtml\#ARIES-ST (Accessed: March 2026).*

*Brown, T.G. (2018) 'Three confinement systems—spherical tokamak, standard tokamak, and stellarator: a comparison of key component cost elements', IEEE Transactions on Plasma Science, 46(6), pp. 2216–2230. doi:10.1109/TPS.2018.2831148. Available at: https://ieeexplore.ieee.org/abstract/document/8361148.*

*Chen, H. et al. (2015) 'Preliminary cost assessment and compare of China Fusion Engineering Test Reactor', Journal of Fusion Energy, 34(1), pp. 1–10. doi:10.1007/s10894-014-9770-x. Available at: https://www.scribd.com/document/762574274/s10894-014-9770-x.*

*Foster, J. et al. (2024) 'Extrapolating costs to commercial fusion power plants', IEEE Transactions on Plasma Science, 52(9), pp. 3772–3777. doi:10.1109/TPS.2024.3362428. Available at: https://scientific-publications.ukaea.uk/wp-content/uploads/Extrapolating\_Costs\_to\_Commercial\_Fusion\_Power\_Plants.pdf.*

*Hidalgo-Salaverri, J., Griffiths, T., Xuereb Conti, Z., Cano-Megias, P., Chacartegui, R., Bluck, M., Ayllon-Guerola, J., Mancini, A., Garcia-Munoz, M. and Viezzer, E. (2025) 'Hybrid hydrogen-electricity production using spherical tokamaks: a cost-driver sensitivity study and techno-economic analysis', Nuclear Fusion, 65, 036027\. doi:10.1088/1741-4326/adaa01. Available at: https://iopscience.iop.org/article/10.1088/1741-4326/adaa01/pdf.*

*ITER Organization (2024) Rapport financier ITER 2024\. ITER Organization. Available at: https://www.iter.org/sites/default/files/media/2025-11/rapport-financier-iter-2024-web.pdf.*

*PROCESS Development Team (UKAEA) (n.d.) PROCESS: Spherical Tokamak Model. UK Atomic Energy Authority. Available at: https://ukaea.github.io/PROCESS/fusion-devices/spherical-tokamak/ (Accessed: March 2026).*

*Sorbom, B.N. et al. (2015) 'ARC: a compact, high-field, fusion nuclear science facility and demonstration power plant with demountable magnets', Fusion Engineering and Design, 100, pp. 378–405. doi:10.1016/j.fusengdes.2015.06.001. Available at: https://www.sciencedirect.com/science/article/abs/pii/S0920379615302337.*

*Woodruff, S. (2026) 'A costing framework for fusion power plants', arXiv preprint arXiv:2601.21724. Available at: https://arxiv.org/abs/2601.21724.*

*Whyte, D. (2024) 'Fusion economics: power density, materials and maintenance'. Presentation, 12 September 2024 (MIT/UKAEA or related colloquium). \[Specific publication details not linked; cite as presentation or forthcoming work if journal-published.\]*
