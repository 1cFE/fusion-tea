## **Indirect Drive Laser Inertial Confinement Fusion**

### **Qualitative Concept Write-Up**

---

**Availability of Data: Moderate (physics) / Limited (economic)**

Indirect drive Laser ICF has the most extensive publicly-available ignition physics database of any fusion concept, owing to decades of NIF experimental data.  However, there are very few independent costing analyses of inertial fusion concepts. In the private sector, Xcimer and Inertia are the best-funded players, with two very different approaches to Laser ICF. Xcimer uses a hybrid (in)direct drive configuration with two large excimer lasers, building off the Naval Research Lab’s HAPL (High Average Power Laser) program. Inertia Enterprises, a new venture with a 450M series A, plans to use one thousand solid state lasers in a scheme that relies heavily on NIF and LIFE (Laser Inertial Fusion Energy) designs.  Xcimer has released some costing and performance data in a recent [whitepaper](https://xcimer.energy/wp-content/uploads/2026/02/XEC-20260224-Commercialization-of-LFE.pdf) (joint-published with German laser manufacturer TRUMPF).  Inertia Enterprises has released very limited information on their [website](https://inertia.com/), some of which appears to be self-conflicting.*

Other laser ICF sources include UKAEA’s [PROCESS tool](https://ukaea.github.io/PROCESS/fusion-devices/inertial/), which includes high-fidelity systems models for various configurations of laser ICF.  Additionally, First Light Fusion’s Nicholas Hawker has published a [helpful framework](https://watermark02.silverchair.com/rsta.2020.0053.pdf?token=AQECAHi208BE49Ooan9kkhW_Ercy7Dm3ZL_9Cf3qfKAc485ysgAAA1IwggNOBgkqhkiG9w0BBwagggM_MIIDOwIBADCCAzQGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQM3F0lfTD2StdU0lNlAgEQgIIDBfok25UdrZRiKPNp35wdvNPJTMuEOUrCJsn7fpK4MaRnTAFVWpkFuok88U6MBkDWWvNL009Y4IEywoYXpunQWIlsjumyZETSHtfz-Dyw-yupXcxPNJXIZxTK0FNAx5CA9ikwzh7dmDsTBtE0fNvC32u0MOxvTKI9PwtF5Oi4MOqzdIDAkwOAfHQNpiY84pisM4erPv0tDrEajVH8OZ_TtmUqlkHnFDZ_NlCa9JeOE6SCDef3zqSLl-Y6f-NJVAjZPkT-oOAfQ6T_1v3oX3lfCAi6Wp7uaV8dstrE_zViRLphRAvMpCxS-FAPR2IZ3WjoGDulSccr8Swhv5412SdvmcTC6jrL_IL4uqsq3Yqe-UuSitx5OBIybiX1qYelBUkLLe_w8mG-yzThGVY8LrlpNFxB4kFCxrajN53O25doxEOR3fpY3_KWadCRTTuJuwCrow4ox07XudvmUzJwEfVOxiFvgMxiQuKGcs287F_ten1_UnOnWwqg1mCUfwNGhqRyxGoQ0w0h2RkE5qKEZEC-JdxaS_Ff7pGq-GZ6vXIqhdgtAp6KodyCAE9mZEgPc1J1vfClKbBhTKJjeH3Zx7Qqk_nsPM8ivs1WvnCwoi2EhhlAq57rMAJI5G8Zq5AgFqHIh4QefIUkaxGX0QyUM3Xh5Mu1o8A-BqG0ouY8XlTW3oOgLuMXN6wgWQK-QTCFbYMBlYozwRL6KpoiDgb6h_pwgoKbjLVB2zOQsT93wtOlIeCVTxf70noGY87pulPwjyA-UfvJyk1RMpASTM1anPKW2ig2DUrVbp8vwG1Z6qiz8fsbVtzrewZ--tPpirHfIkU1qbTVLjxnNwnfu81rD9hS6GGlMKZ4-pd5It14qxjzbeA-1q2zuYa0unPO6dMUGAn8WWXsCAgSihG86jS7zcfIQCpCw47Ln-qNb3altizwke0vKdFz1yd_CTbGQ1ZJJ4V8kC7x4DcFsT1GC3iZZCwcQ_DtozMzX0z5916BzQHzU5UvqzD_152bC3CyfA_UnWFqt8ezR3Us) for the technoeconomic analysis of inertial fusion.

Lastly, the LLNL’s own publication [GEM](https://lift.llnl.gov/resources/gem) (Generalized Economics Model) is an excel-based tool that can estimate CAPEX, LCOE, etc. for solid state laser-driven architectures.

**Challenges in Capturing System Function**

Quantifying reactor costs is significantly more difficult for Laser IFE than for tokamaks.  Tokamak sizing can be approximated by steady-state constraints on several key physical parameters such as density and temperature. An IFE chamber has multiple constraints that respond to fundamentally different combinations of inputs: neutron damage scales with average power (yield × rep rate), Evaporation limits scale with yield per shot, and chamber clearing scales with rep rate, so they can't all be satisfied by tuning a single geometric parameter. Worse, the architectural choices — thick liquid wall vs. dry wall, beamline count — completely restructure which constraints bind, meaning there's no universal sizing model that applies across IFE concepts the way NWL-based scaling applies across tokamaks.

A further challenge is modeling the liquid first wall costs (where applicable). The liquid wall is a popular choice for its architectural simplicity, as it simultaneously performs neutron shielding, tritium breeding, and heat exchange functions. Key costing components such as the FLiBe inventory and the FLiBe pump(s) are closely coupled to the chamber size and rep rate.  Plus, the pumps can be a significant contributor to the recirculating power fraction, which must be accounted for.

Some additional modeling challenges are the uncertainties around ash clearing, target manufacturability, tritium processing, and laser optics lifespan. These all have the potential to be major cost drivers, but are in the very early stages of commercialization.

---

**Key Materials and Supply Chain Considerations**

*Tritium:* covered [here](https://www.notion.so/HTS-Compact-Tokamak-D-T-2feaa1d01f248005ab39e1168123bdf2?pvs=21)

*Target Factory:* tritium plant, deuterium processing, cryoplant, CVD, finishing, etc. must be on-site to accommodate rapid manufacturing to keep up with rep rate. GEM has a bottom-up cost model for this, but there is a simpler top down approach— According to Goodin et al, 2004, targets must be <10% of the electricity they produce to be economical. For Xcimer, that would be $2.78 per target.  For Inertia, that would be $0.75 per target (their stated goal of $1 per target is ~14% of the electricity yield, assuming an average power price of 13.6c/USD)

*Laser diodes (within DPSSL):* Major scale up needed.  Inertia states that similar scaleup has already been seen for similar lasers in all devices with FaceID. Xcimer estimates a price floor at $0.02/W, and a separate [TRUMPF/LLNL study](https://lasers.llnl.gov/sites/lasers/files/2023-11/haefner-ILT-IFE-workshop-2022-1.pdf) estimates that diodes would need to achieve $0.007/W in order for Laser IFE to be economically viable.

*Capacitors (within excimer laser Marx generators):*  Xcimer is already producing these in-house, with a long term target of 0.40 USD/Joule.

---

**Maturity of Key Subsystems and Components**

Here's the ranking from least to most mature:

**Final optics survivability — TRL ~2** Each fusion pulse bathes the final focusing optics in X-rays, debris, and 14 MeV neutrons, progressively degrading them. No optics geometry or protective scheme — grazing-incidence mirrors, liquid films, or otherwise — has been validated for the fluence levels a commercial plant would deliver.

**High-rep-rate, high-efficiency laser — TRL ~2–3** NIF-class lasers are single-shot devices running at ~0.1% wall-plug efficiency; a DPSSL driver needs ~10% efficiency at 10Hz continuously. Diode-pumped solid-state and KrF gas laser concepts show promise but remain far from plant-ready hardware.

**Reaction chamber / first-wall materials — TRL ~3** The first wall must survive multi-MW/m² 14 MeV neutron loading over years of operation — a fluence environment with no analogue in existing test facilities. Candidate materials such as ODS steels and SiC composites have been studied but never qualified under prototypical IFE conditions.

**Target fabrication at scale & cost — TRL ~3** Mass-production processes for cryogenic layering, surface finish, and fill-gas handling at that throughput do not yet exist..

**Chamber clearing & debris mitigation — TRL ~4–5** After each shot, the chamber must clear debris, vapor, and shrapnel fast enough to permit the next target injection within ~100 ms. Gas jet, liquid wall, and magnetic divertor schemes have plausible physics bases but no demonstration at relevant repetition rates or pulse energies.

**Hohlraum & capsule target design — TRL ~5–6** There needs to be an order-of-magnitude improvement to NIF’s capsule gain to be commercially viable.  Additionally, hybrid direct drive architectures like Xcimer’s need to prove stable and symmetric two stage,  two-beam implosion.

---

*Table 1. Inertia Enterprise vs. Xcimer Energy Comparison*

|  | **Inertia** | **Xcimer** |
| --- | --- | --- |
| **P_net** | ~1.5 GWe (utility-scale commercial plant) | Hundreds of MWe to >1 GWe commercial; 400 MWe Athena pilot |
| **Rep Rate** | **10 Hz** | **0.25 – 1 Hz** |
| **Target Cost per Shot** | <$1 per target (mass-produced factory assembly line). "Cold" D-T, but doesn't specify how cold | Not publicly specified; liquid DT + plastic ablator (no hohlraum gold). Likely a larger capsule than Inertia |
| **Energy Yield per Shot** | **450MJ** | **>1GJ (likely ~1.6GJ)** |
| **CF** | Website states assumptions that result in 0s dwell between pulses! Structural replacements every 3-5 years | Claim no replacements needed, but the single optical chain implies less redundancy than Inertia |
| **Blanket** | Liquid lithium flowing through chamber wall pipes (breeds tritium + heat exchange); | thick-liquid FLiBe molten salt wall; near-complete neutron capture; no structural wall replacement needed |
| **Reactor Structure** | Low-cost conventional steel chamber | Low-cost conventional steel chamber |
| **# Lasers and Type** | ~1,000 modular Thunderwall DPSSL beamlines (each 10 kJ / 10 Hz) | Up to 100 Argos KrF excimer amplifier modules → combined into just 2 final beams delivered to target |
| **Laser Efficiency** | **~10%** | **5 – 7%** |
| **Laser Cost** | **$700–$1,000/J*** | **$100–$120/J FOAK; $60–$80/J NOAK** |
| **Laser Driver** | Diode-Pumped Solid-State Laser (DPSSL) — "Thunderwall" semiconductor diode beamlines; 351 nm UV | Electron-beam pumped KrF excimer laser (248 nm deep-UV) + Stimulated Raman / Brillouin Scattering NLO pulse compression |
| **Laser Lifetime** | Modular line-replaceable units; designed for high availability with standard MTBF targets | Gas gain medium does not degrade; no optics exposed to damaging fluences; long intrinsic lifetime |
| **Drive Type (Direct/Indirect/Hybrid)** | Indirect drive — laser heats hohlraum walls → x-rays compress capsule (NIF "Hybrid-E" design) | Hybrid direct-drive — brief hohlraum pulse creates uniform ablation plasma; then 2-beam direct drive with shaped intensity ring |
| **Coupling Efficiency** | **~12%** laser-to-capsule via hohlraum (same physics as NIF ignition shots); | **>50%** (from the energy on target of Athena, it looks like its 80%) |
| **Capsule Gain** | ~45X total scientific gain projected at 10 MJ scale. Since only 12% of this is absorbed by the capsule, Capsule gain = 45/.12 = 375X | >200X projected at 10 MJ scale (via ⅔ power law scaling from NIF data) |
| **Burnup Fraction** | **0.23** *(conjecture: but smaller capsule generally means lower burnup frac)* | **0.3** |
| **Q_eng** | **4X** *(recirculating power fraction = 500/2000MW)* | **~8.2X** *at 7% laser efficiency, recirculating power fraction <11-13%* |
| **Replacement Interval** | Chamber: every ~3–5 years; laser components: modular replacement as needed | No first-wall replacement (thick liquid wall); laser optics never exposed to damaging fluences |
| **Ash Clearing** | No public strategy | Gravity clears FLiBe liquid jets between shots; <10 kg FLiBe vaporized per shot; vapor vents through jet gaps; ~1 second clearing time sets rep rate ceiling |
| **Key Risks** | High gain target; incredibly high rep rate drives stringent ash clearing and target injection requirements; develop FLiBe pumps/nozzles/redox control; | Must scale KrF excimer + NLO from kJ to MJ (never done); demonstrate 2-beam symmetric implosion; develop FLiBe pumps/nozzles/redox control; |