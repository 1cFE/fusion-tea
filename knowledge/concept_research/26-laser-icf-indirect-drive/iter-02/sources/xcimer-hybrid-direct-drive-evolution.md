---
source: "xcimer-hybrid-direct-drive-two-sided-uv.pdf"
source_type: "local_file"
extracted_at: "2026-04-04T17:11:43.949100+00:00"
content_hash_sha256: "6499135d15225c3e3c78e139f69ea9eaf18325927b6697ad9fc1602094ea2e87"
backend: "pdf_pipeline"
---

RESEARCH ARTICLE | NOVEMBER 27 2024
### **Hybrid direct drive with a two-sided ultraviolet laser**

[C. A. Thomas](javascript:;)  [; M. Tabak](javascript:;) [; N. B. Alexander](javascript:;) [; C. D. Galloway](javascript:;) [; E. M. Campbell](javascript:;) [; M. P. Farrell](javascript:;) ;
[J. L. Kline](javascript:;) [; D. S. Montgomery](javascript:;) [; M. J. Schmitt](javascript:;) [; A. R. Christopherson](javascript:;) [; A. Valys](javascript:;)

_Phys. Plasmas_ 31, 112708 (2024)

[https://doi.org/10.1063/5.0221201](https://doi.org/10.1063/5.0221201)

 [CHORUS](https://pubs.aip.org/aip/pop/article-pdf/doi/10.1063/5.0221201/20271741/112708_1_5.0221201.am.pdf)

# 

# 

View Export
# Online [] Citation

Export
Citation

**Articles You May Be Interested In**

[An industrial approach to inertial fusion energy](https://pubs.aip.org/aip/sci/article/2024/48/481102/3322695/An-industrial-approach-to-inertial-fusion-energy)

_Scilight_ (November 2024)

Exploring scenarios for enhanced fuel compression and performance on the National Ignition Facility with

machine-learning-aided design techniques

_Phys. Plasmas_ (April 2025)

First demonstration of improved yield with reduced adiabat in inertial confinement fusion implosions on the

National Ignition Facility

_Phys. Plasmas_ (December 2025)

![](images/xcimer-hybrid-direct-drive-two-sided-uv.pdf-0-3.png)

![](images/xcimer-hybrid-direct-drive-two-sided-uv.pdf-0-4.png)

# Hybrid direct drive with a two-sided ultraviolet laser

Cite as: Phys. Plasmas **31**, 112708 (2024); doi: 10.1063/5.0221201
Submitted: 30 May 2024 · Accepted: 16 October 2024 ·
Published Online: 27 November 2024

**C. A. Thomas,**<sup>1,a)</sup> **M. Tabak,**<sup>2</sup> **N. B. Alexander,**<sup>3</sup> **C. D. Galloway,**<sup>4</sup> **E. M. Campbell,**<sup>1</sup> **M. P. Farrell,**<sup>5</sup> **J. L. Kline,**<sup>6</sup> **D. S. Montgomery,**<sup>6</sup> **M. J. Schmitt,**<sup>6</sup> **A. R. Christopherson,**<sup>6</sup> and **A. Valys**<sup>6</sup>

## AFFILIATIONS

<sup>1</sup>Laboratory for Laser Energetics, University of Rochester, Rochester, New York 14623, USA
<sup>2</sup>Lawrence Livermore National Laboratory, Livermore, California 94550, USA
<sup>3</sup>General Atomics, San Diego, California 32121, USA
<sup>4</sup>Xcimer Energy, Redwood City, California 94065, USA
<sup>5</sup>MCM Consultants, San Diego, California 92127, USA
<sup>6</sup>Los Alamos National Laboratory, Los Alamos, New Mexico 87545, USA

<sup>a)</sup>Author to whom correspondence should be addressed: ctto@lle.rochester.edu

## ABSTRACT

This paper presents a "hybrid" approach to direct drive inertial confinement fusion that can exploit a high-energy gas laser with two opposed beams. The target and driver are asymmetric, much like experiments performed on the National Ignition Facility, but have been designed to benefit from scaling of their predicted compatibility with a fusion power plant. The imploded masses (and areal densities) are increased by a factor of 12 (3) relative to findings by Abu-Shawareb et al. [Phys. Rev. Lett. **129**, 075001 (2022)] and provide a path to high-gain implosions that robustly ignite. The energy division (split) between concerns such as laser imprint and cross-beam energy transfer. We discuss the rationale for a hybrid target, the methods used to control implosion symmetry, and the implication(s) for inertial fusion energy.

© 2024 Author(s). All article content, except where otherwise noted, is licensed under a Creative Commons Attribution NonCommercial-NoDerivs 4.0 International (CC BY-NC-ND) license (https://creativecommons.org/licenses/by-nc-nd/4.0/). https://doi.org/10.1063/5.0221201

## I. INTRODUCTION

Inertial confinement fusion (ICF) employs the energy of a high-velocity implosion to compress and heat (and ultimately confine) a variety of low-Z fusion fuels.<sup>1,2</sup> The most common mixture is deuterium and tritium (DT) as it has the lowest threshold (for a given dilution, the highest reactivity) and the potential to generate 340 MJ per mg of fuel. Products include alpha particles at 3.54 MeV and neutrons at 14.1 MeV. Assuming a central hotspot (hs) can be made with the densities and scale needed to stop alpha particles, or $\rho_{hs} \sim 0.3 \text{ g/cm}^3$ at temperatures of $4–5 \text{ keV}$—the propagating burn of the surrounding cold fuel (cf) can be initiated, as recently demonstrated on the National Ignition Facility (NIF).<sup>3-5</sup> ICF could lead to the commercial production of energy if the product of the driver efficiency and target gain G can be $> 10$ with the driver efficiency $\eta_D > 10\%$ and the target gain G > 100. Assuming that the wall-plug (to on-target) efficiency is $\sim$15% accounting for input energy and other subsystems, it is likely that inertial fusion energy (IFE) will require target gains $> 50$. Important metrics include the areal density of the cold fuel at its initial

radius, $\rho R_{\text{max}}$, and also during burn, $\rho R_b$. The nuclear yield can be expected to scale as $m_{DT} G_b$ and the burn fraction $\phi_b$ as $\rho R_b / (\rho R_b + 6 \langle \sigma v \rangle_b / (\sigma v)_{|T_b})^{-1}$ [or $\rho R_b \sim 3 \text{ g/cm}^2$] for $G_b \sim 3 \text{ g/cm}^2$. The areal density of the stagnated DT scales with the ratio of the kinetic energy of the implosion velocity $\propto \rho R_{\text{max}} / E_{\text{kin}}$ (see Ref. 6), and $E_{\text{kin}} = \eta_{\text{hydroeff}} \cdot \eta_{\text{abseff}}$ (accounting for laser absorption and target ablation), then the target gain. Effective strategies to maximize $G = \eta_{\text{hydroeff}} (\rho R_{\text{max}})^{2/3} / (E_{\text{laser}} / m_{\text{DT}})^{1/3} \cdot (E_{\text{kin}} / E_{\text{laser}})$ maximize $G = \eta_{\text{hydroeff}} (\rho R_{\text{max}})^{2/3} (E_{\text{laser}} / m_{\text{DT}})^{1/3}$.

The hydrodynamic implosion of a target in ICF need to put a strong emphasis on compressibility,<sup>1,7</sup> due to limitations in the hydrodynamic efficiency and areal and details in laser-target coupling. The internal energy of the DT fuel is a function of pressure and will commonly be defined by a term called the adiabat, $a_{\text{kin}} = p_i^{-} / p_F$, where $p_i$ is the pressure of the (non-degenerate) DT and it is ionized. The Fermi pressure $p_F = p_i^{-5/3}$. The adiabat of the DT is determined by the power in the laser as a function of time, and low-*a* designs ($\leq 2$) tend to have fuel layers that are particularly dense and thin and can be susceptible to a variety of hydrodynamic instabilities. For this region of parameter

## Physics of Plasmas — ARTICLE

space, it is common for ignition to be inhibited by mix (seeded by high mode imperfections in the laser and target) and premature heating of the fuel (caused by laser-plasma interactions and high-energy electrons). We can expect low adiabat implosions to eventually reach higher gains,<sup>7</sup> but requirements for stockpile stewardship-quality inertial fusion energy might still be difficult to achieve. The obvious alternative is to focus on the hydrodynamic efficiency and scale—as done here—with implosions that can couple much more energy to the DT fusion fuel.

In this paper, we present a "hybrid" approach to direct-drive ICF that can exploit a high energy laser with two opposed beams. The concept employs an ultraviolet (UV) gas laser at 248 nm that is being tested within the Milestone-Based Fusion Development Program, with the potential to reach the efficiencies quoted above, although it could also be compatible with light at other wavelengths. Rather than design for high levels of compression, the goal is to maximize the laser–target coupling in a regime that greatly relaxes the compression sprife.<sup>8–11</sup> The geometry of the system is two-sided to take advantage of a reactor with thick liquid walls (which can efficiently shield tritium and protect the structure from x-rays and neutrons) and also be compatible with a cylindrical hohlraum to shield the condensable DT fuel from the chamber environment.<sup>12–15</sup> All of these elements are useful for reducing cost. The result is termed a hybrid because it combines x-ray and laser drives in a manner that is complementary<sup>16–18</sup> and not because it uses the dimensions and pulse shapes of prior work.<sup>19</sup> In fact, this concept couples 50 kJ (or more) to the imploding fuel and enables high-adiabat implosions with a factor of 12 (11 more mass areal-density) than contemporary implosions on the NIF. Common metrics for stability and gain are substantially improved and could help to relax requirements on the target. The paper begins by introducing the principles of hybrid direct drive (HDD) and the design features used to suppress laser imprint and cross-beam energy transfer. Next, it summarizes the main elements of the reactor system that enable a two-sided driver: (1) a highly absorbing plasma atmosphere, (2) electron-conduction-limited heat, and (3) a two-sided x-ray drive. Finally, we describe the hybrid concept with detailed radiation-hydrodynamic calculations and discuss several measures of margin. The HDD target is found to benefit from efficiency and scale and high levels of coupled energy as expected, and shows promise for achieving breakeven and potentially more.

## II. LASER AND TARGET

We provide a schematic of the UV laser system in Fig. 1 and the target in Fig. 2. Long pulse KrF amplifiers with multipass or Raman and Brillouin pulse compression are used to deliver multi-Megajoule energies in the spatial and temporal patterns needed for the HDD shell.<sup>20,21</sup> This approach has almost no need for solid optics—which also helps to reduce cost—and can operate at very high efficiency, with $\geq 12\%$. By design, the system represents a departure from current practices but is particularly well-suited to IFE as upcoming papers on the laser and target fabrication will show. The energy from the driver is to be delivered as multiple stages. In the first stage, a short laser pulse (P1) burns through a thin capsule wall, heats a high-Z layer (lined capsule or hohlraum to 100 eV). Similar to experiments on the NIF, the window film and hohlraum protect the capsule from the chamber environment,<sup>22</sup> and the first pulse (and associated x-rays) ablate and shock the capsule to set the adiabat of the cryogenic fuel. The capsule itself is a

[Figure 1: (a) The laser system uses stimulated scattering processes to provide high fluences and energies in a manner that is simple and robust. (b) The full pulse is comprised of discrete segments in time, with the P2 stage having a variable laser spot size. The total energy is 4 MJ as shown, although the system is capable of 12–20 MJ.]

[Figure 2: A diagram of the hybrid target and its two stages in drive: indirect and then direct. The high-Z cavity is designed to protect the capsule from the chamber environment with materials suitable to a power plant, as well as generate a pulse of x-rays.]

deuterated plastic (CD) that is relatively easy to manufacture. The target borrows heavily from learning at the NIF<sup>16,17,23</sup> but has otherwise been adapted for two-sided illumination. To keep the blow-off of plasma inside the hohlraum relative to conventional indirect drive, the laser energy intercepting the wall is reduced to a factor of 40 per

$$\log_{10}(S_{21})$$

[Figure 3: (a) The predicted smoothing factor $S_{21}$ for asymmetries in flux as a function of angle for mode numbers 10 and 50. (b) Same for the same solutions at $r = 0.5$ and 50, but unrolled in theta for visualization. Very clearly, a thick conduction zone is needed to moderate mid modes, whereas high modes are easier to suppress.]

unit area when integrated over the full pulse. There is no need to tamp hydrodynamic motion with a high-density fill gas (for example, helium). For the second stage of the implosion, a series of short laser pulses (P2 to P7) drive the capsule directly at pressures exceeding 250 Mbar. The mass ablated by the first pulse (P1) enables this mode of operation, as we will explain. To limit laser-plasma instabilities or LPI, the wavelength of the laser is short, 0.25 μm, and the peak streaming intensity is relatively low (∼10⁻¹⁰ W/cm²). Cross-beam energy transfer is avoided by virtue of the direct-drive geometry and a smoothing profile that can follow or "zoom" with the implosion. (To maximize spectral bandwidth, the laser is capable of operating on multiple lines, but this is not planned for initial ICF experiments.) By putting the capsule at a high-*Z* cavity and staging the drive, the HDD is meant to exploit features from both indirect and direct drive and avoid many of their weaknesses: the DT fusion fuel is protected from the hot chamber background, there is no CBET (as in spherical direct drive), and the hydrodynamic efficiency is quite high (like direct drive).

Two-sided drive has additional benefits, which will be described, but may be expected to make driver optics (mostly) a challenge. The typical direct-drive target on the OMEGA or NIF laser systems needs a large number of beams (24 or 48 on OMEGA, for many implementations, 60 or many hundreds).<sup>1–4</sup> Each of these beams needs a clear path to the capsule and is a matter of optics and control systems. Spherical illumination might be preferred, but tradeoffs in systems engineering tend to motivate non-symmetric solutions. The hybrid target has only two beamlines, but several novelties still allow for good implosion symmetry. First, and most importantly, is the use of the first pulse (P1) to generate a *rim* that ablates the capsule and forms a thick plasma atmosphere. Indirect drive is very capable in this regard and can be symmetric when the ratio of the hot-return and optical radii (a capsule-to-capsule ratio) is the same value used here (∼3).<sup>45</sup> As a consequence, when the capsule is directly driven at pulses P2 to P7, the laser can be absorbed in a large volume of underdense plasma. This approach not only benefits from the coupling efficiency of direct drive for most of the laser pulse, but imbalances from the heat flux to the ablation front will always be smoothed by thermal conduction. To provide insight(s), we find it useful to introduce a model that can generate quick estimates but is also insensitive to many details. We start by assuming that electron density is approximately stationary when averaged over a single pulse (say, P2) and treat the conservation of energy as a Laplace problem. This fails to consider some important circumstances, but mainly, we seek a solution that is easy to address in 3D. If ∇ · (A∇T) = 0 and A ~ T<sup>5/2</sup>, then ∇²(T<sup>7/2</sup>) = 0. The region of interest is assumed to be spherical (3D) and exists from an inner radius of r₁ (the ablation front) to an outer radius of r₂ (outer critical density). Finally, we assume that energy is causally transferred radially to the corona. The solution of the Laplace equation is known, and it is easy to show that nonuniformities in flux *δF* at r₂ will become relative to r₁ by a factor of x(r₂/r₁)<sup>-(ℓ+2)</sup> at a Legendre mode number of ℓ. In detail, the resulting smoothing factor S_ℓ is $(2 + 1)/(\ell + 2) \cdot (r_1(\ell + 2)/r_2^{\ell + 1})^{(\ell + 2)/(\ell + 1)}$ ... as shown in Eq. (8). We might have liked to account for advection, but this is unnecessary given the benefits of thermal conduction. Returning to the implosion mode of hybrid drive, we find that r₂/r₁ will be ≥9.0 and will smooth imbalances in modes ≥50 by a factor of 10 (or more) (S ≤ 0.1). As a consequence, the conventional direct drive target has no protection when the laser is turned on, and variations in the drive will be immediately imprinted

on the ablation front (Refs. 38 and 39). In all simulations to date, the hybrid approach has been found to significantly reduce the risk of hydrodynamic instabilities, as shown in Fig. 6. Furthermore, the standard direct drive target starts with no plasma around the target and is very cold, and this results in a large chance of laser-plasma interaction. This scenario is completely avoided when using hybrid drive. In any case, the HDD could ultimately allow for implosions with lower adiabats and might also be combined with other types of beam smoothing. A related method to coat the capsule with a laser is digital and generates a thin plasma atmosphere with a laser propellant.<sup>48</sup> In the future, a hybrid target could also use a thick subcritical outer layer to tame absorption and coupling.

The smoothing model also provides benefits to modal modes  $(r_2/r_1$  ratio) lower than ideal that is common. As a consequence, the hybrid implosion will be symmetric (or has the potential to be) with a window for tuning target modes. Our calculation shows that this can be done with a limited number of beams when the incident energy has a specific time-dependent profile (a *radius*). Normally, a two-sided laser would not be compatible with direct drive. The driving energy needs to be normal to the capsule at its waist and would not be absorbed over a large solid angle. By contrast, the HDD design has a plasma atmosphere that absorbs the driver volumetrically (as described above) and by also having laser spots that cover with the implosion. To explain, we start by assuming that laser deposition must be uniform and spherically symmetric (i.e., we minimize Sr₁ along drive modes). Two opposed beams can deliver the same energy profile vs mode. If

[Figure 4: Two-dimensional simulations of direct drive experiments on the OMEGA laser. The modeling describes multiple-flight experiments that examine beam illumination in (a) the ablation front AF at shock breakout, and (b)–(d) at ablation front AF at peak density. (a) at peak density. These beams were used as laser imprint (= ~50) and the geometry of the chamber (r₂ =10, but to a lesser degree of non-uniform 3D) to the capsule and converts them. On target: (c) and (d) have been characterized in off-line measurements and are applied as a power profile to a point on direct drive capsule. For the hybrid target, we stage the drive and convert it to hybrid drive, as shown in (b) through (f), so that first high mode imprint is absorbed and smoothed before direct drive (c) is applied. Note the high level of symmetry achieved in the hybrid implosion (d) and (e). We find that the benefits of the hybrid approach can be substantial and should be tested at existing facilities including the OMEGA and the NIF.]

parameter, *s*, but the incoming intensity vs radius *I(r)* must be proportional to the plasma chord that needs to be heated. As a simple function of geometry, for a ray with impact parameter *r* < *r*₀, this requires *I(r)* ∝ [*r*₀² − *r*²]^(1/2) − [*r*₁² − *r*²]^(1/2). If *r* ≥ *r*₀, this requires *I(r)* ∝ [*r*₀² − *r*²]^(1/2). For commonly studied values of *r*₁, we find that the intensity profile must be ring-peaked and have a maximum-to-minimum intensity of ~2:1. (Of course, the energy will also be smoothed by thermal conduction.) This solution is similar to findings by Schmitt⁶ and shows there is more than one way to generate a symmetric implosion. In detail, the ideal profile will, of course, depend on the material properties, and the trajectory of the capsule in time (see Fig. 8). These issues must be accounted for in 2D calculations (as we will show) or *Zooming* tuning (in experiments). Implosions using conventional forms of indirect drive are subject to similar issues but can overcome variations in flux vs time of order 20%.<sup>31,32</sup> The hybrid target will also require tuning but should achieve adequate levels of drive uniformity, as shown in Figs. 5 and 6. To increase the likelihood of ignition further, the HDO target will also be overdense to provide "margin", which we will also discuss.

---

**FIG. 8.** The simulated density and ion temperature of the HDO target at peak compression with alpha deposition (a) burned on and (b) turned off. The symmetry of the implosion is sufficient to ignite the DT fuel with high levels of margin (which will be quantified and could be further tuned). For context, the same implosion is also shown in (c) at the scale of a NIF experiment.

---

To provide additional control of low mode symmetry, mostly as a corrective tool, the hybrid target can also be made somewhat asymmetrically thinner near the hohlraum wall. This type of asymmetry is commonly called a "shim" — a technique widely used with a variety of techniques.<sup>33</sup> To the first order, a shim is used to add or remove mass where the laser deposition is high or low. The main purpose is to make the acceleration feature of the capsule more uniform and improve the symmetry of the final assembly. To provide an example, we can consider an asymmetry in the incoming laser of order 10%, most of which is in Legendre mode 2. If the ablation pressure is assumed to scale with the local intensity as *I*^{2/3}, then an asymmetry in the mass of order 5% could be expected to compensate. Variations like these can be imposed by writing a foam with the required shape or by adding a heat source that shifts isotherms within the capsule. For reasons that were outlined previously, this approach could prove useful for tuning modes ≤ 4. The use of shims has been tested in both calculations and experiments rather extensively<sup>33</sup> and have been found to correct asymmetries to drive at high levels.

The geometry of the hybrid target and laser system has another important synergistic benefit worth noting. For various implosion schemes for laser ICF, the energy directed at the target can be redistributed by time dependent cross-beam energy transfer (CBET).<sup>34</sup> These phenomena are caused by the seeded Brillouin scattering and effectively generate gratings in plasma density that can redirect laser light and reduce predictability and have also been known to reduce laser-target coupling. CBET can be particularly troublesome if many beams overlap at high intensities in the low-density corona and are often directed along local plasma flows. By virtue of the two-sided geometry with fans of beams of a smaller with than shown in 1, the hybrid target does not excite common resonances, and little or no CBET is expected. In not a large (or smaller) focal spot in higher density plasma regions and this helps to increase efficiency.

Finally, we find that the hybrid approach is particularly complementary to excimer lasers and any strategy based on scale. If laser light at wavelength λ is incident on a planar plasma at an angle of θ, the Bremsstrahlung is *A*_*L* because the opacity decreases as *I* ~ exp(−*k*_*r*·*x*), *A*_*L* (θ) for *L* ~ ∫*Z* cos (*l*)² / *λ*² (Refs. 1 and 35). The atomic number is *Z* and the exponent is close to ~ 0.7 for absorption at density scale *L*. Relative to data using the OMEGA laser, the hybrid has values for Z, λ, and θ that together increase the size of the target enormously. The metric *L* is increased by a factor of ~40, and this leads to high levels of laser absorption (97%) and in flight kinetic energy (300 kJ/4M =3%).

For related reasons, we do not expect convective stimulated Raman or a two-plasmon-decay to pose similar problems. Most metrics for LPI risk (i.e., gain) can be assumed to increase as $I\lambda^2 l^{1/2}$. Depending on the gain per speckle and plasma dumping, respectively, the exponent $\alpha$ will have values from 2 to 3, with products $I\lambda^{2\alpha} l^{\alpha/2}$. Tests of direct drive on the NIF with 3 mm capsules are the closest surrogates to the HDD at present and tend to report high LPI ($\sim$ several %) at intensities of order $10^{15}$ W/cm² (Refs. [?], [?]). The HDD target will have a smaller value for $l$, and if the wavelength $\lambda$ is reduced from 351 nm to 248 nm, LPI risks have the potential to decrease relative to the NIF, but as these systems are very different, this type of extrapolation is highly uncertain. Historically, the benefits of shorter wavelength light have always been found to be significant. To prepare for experiments with KrF lasers at larger scales, a series of tests are in planning for existing facilities. We are also making plans to investigate the potential of ArF at 193 nm (Ref. [?]), and other short-wavelength, high-energy laser options. Changes to the ablator, including the use of materials at higher atomic number might be expected to couple P1 at a lower level of intensity efficiency. To reduce the importance of hot electrons produced by Raman or two-plasmon-decay instabilities at temperatures $\sim 50$ to $60$ keV — if preheat were to be a problem, the HDD hot electron fix is also thick (if a simple function of size) and starts at an already high ablator.

The main parameters of the hybrid hohlraum are provided in Fig. 2. The C23 capsule has an outer radius of 2165 μm and a thickness of 75 μm. To increase geometric options for eventually reaching higher fusion gains, this radius is a factor of 2 larger than experiments on the NIF. The fusion fuel is composed of a DT-wetted CD foam developed at General Atomics,³¹ having a thickness of 270 μm, and a total density of $0.3$ g/cm³ $-$ $0.3$ g/cm³ of DT. The DT-wetted CD foam is designed to the foam absorbs x-rays from the corona and would appear to increase ablator shaping and stability.³² A wetted foam should make high drive rates more practical than IFE DT ice-filled polystyrene capsules, as a liquid, and in a manner that simplifies layering and reduces the inventory of tritium.³³ A wetted CD foam preserves some unique properties in design, as discussed in Refs. [?]–[?], but these have not been explored here. The density of the DT ice at the top and the DT vapor at the center of the target is assumed to be in thermal equilibrium with the layer and is assumed at 18.3 K with a vapor density of $0.3$ mg/cm³. The mass of the DT fuel at stagnation is 7 mg and intentionally exceeds contemporary experiments by more than a factor of 10.

## III. RADIATION HYDRODYNAMIC SIMULATIONS

To demonstrate the HDD target, we have made use of the radiation hydrodynamics code HYDRA,³³ which is an advanced tool for designing and analyzing experiments in ICF. The mesh in these calculations is Eulerian. The model for the laser–plasma coupling of laser energy is a function of inverse bremsstrahlung absorption and has been reported in analysis using geometric ray optics, valid for all material properties,³⁴ and the DT-wetted foam is assumed to behave as if it were uniform in composition, as found in prior studies.³⁵ These simulations include electrons, CRE,³⁶ and nonlocal heat conduction³⁷ and have been validated against a large number of focused experiments on the NIF. They were also used to predict and analyze experiments on laser imprinting with good success³⁸ and provides a strict limit on short-scale imprinting, noted above.³⁹ Consistent with all existing targets, the calculations in this paper include physical imperfections and flaws, but future work will

consider all of the specifications that could plausibly relate to ignition and burn.

To estimate the initial x-ray impulse, we have employed a view-factor model that only requires the initial geometry of the target. The radiation source is introduced at the boundary of HYDRA and in the same manner as high-resolution calculation for indirect drive. Very conveniently, the abledo for Pb has been measured and is known to be very similar to Au.⁴⁰ To ensure the initial x-ray drive is highly symmetric, the first laser pulse (P1) has been designed to interact with baffles at the arms of the Lagendre mode P₂. The geometry of the system has also been tuned to minimize mode 2, and all higher modes are smoothed to some level. The waist of the target sees the outer laser wall, whereas the pole sees the cold hohlraum entrance hole, which is balanced with a bright ring of illumination centered on the baffles. In comparison to indirect drive experiments on the NIF, which have a longer plasma direct pointing, the initial impulse for the HDD is easy to design, as it is completely separable from the rest of the pulse. The baffles are nominally required to direct the P1 energy and to set up their interaction with pulse P1. As the baffles and laser are thin, and do not need to be optimized for the laser generation of x rays, the baffles can be made of different materials at lower density. Baffle materials will be discussed in the work to follow and use codes specific to that purpose.

To optimize the hybrid target in simulations, we note it was convenient to try and optimize pulse P1 individually, then P1 followed by P2, etc., to cumulatively build the drive. To find the best (r1) per pulse, we simply iterated through various candidates and interpolated for a round hotspot. The need for tuning is common to indirect and direct drive, and should be able to be highly leveraged in that area. In all of the results that follow, approximately 50 calculations were required per pulse (P2 to P7) for a total of 300 simulations in 2D. These calculations have been found to be largely insensitive to the exact incoming laser profiles, and also be very stable, although the design is nonoptimal. Other than design flexibility, which will also be needed in 3D, the DT ablator were not discovered by a process but were instead modeled by a team. Initial simulations will find very high anisotropy relative to contemporary data, but again, no scan or study has been done. If we were to try to use an optimized hohlraum, it would not be difficult to simulate higher gains, but that is not the purpose here. For similar reasons, we have not included a shim, but only to emphasize that it is not yet optimized. If we did use a shimless drive, we find that the incoming laser profiles would be more uniform. Other than design options related to geometry and material choices that are discussed above, the hybrid design is otherwise meridional. Similarly, we have not pursued options related to P1 that are a hybrid in nature. Obvious examples include an absorbing or "Saturn" ring³ and graded inner walls.⁴¹ These experiments in optimizing this design are not infinite—or we were to pursue higher levels of performance—a large number of options remains.

## IV. RESULTS AND FUTURE WORK

The hotspot of the hybrid target is shown in Fig. 3, and performance metrics are provided in Table I. By design, the hybrid implosion takes a longer time than experiments on the NIF, by construction from the Lawson criterion⁴² and metrics for alpha heating⁴³ by more than a factor of 3 to 4. The design is using an overall target thermonuclear yield of 256 MJ, which results in a gain of 65. Efficiency and scale have significant benefits and can be expected to relax

**TABLE I.** Design variables for the hybrid target are shown for reference. Please note that the burn-averaged pressure, temperature, and areal density, as well as the maximum convergence ratio and yield are all provided with (and without) alpha-heating.

| Laser energy | 4 (MJ) |
|---|---|
| Fraction absorbed | 97% (N/A) |
| In-flight kinetic energy | 300 (kJ) |
| Hydrodynamic efficiency | 8% (N/A) |
| Imploded DT mass | 2 (mg) |
| Peak velocity | 410 (km/s) |
| Adiabat at peak velocity | 6 (N/A) |
| In-flight aspect ratio | 48 (N/A) |
| $\langle p \rangle_{\alpha}$ | 2720(212) (Gbar) |
| $\langle T \rangle_{\alpha}$ | 46.7(4.8) (keV) |
| $\langle \rho R \rangle_{\alpha}$ | 1.60(1.23) (g/cm²) |
| $CR_{\max}$ | 20.1(28.7) (N/A) |
| $Y$ | 2360.61 (MJ) |
| Prompt fusion gain | 65 (N/A) |

requirements on symmetry and other concerns (see Figs. 3 and 4). These findings are intrinsically at an in-flight adiabat of 6, which is understood to lower fusion performance but is also meant to reduce requirements on the lasers. In general, experiments and database approach expectations on both the OMEGA and the NIF. $^{1,7,10,11}$ The in-flight aspect ratio is at a NIF convergence ratio of 13, and this also compares favorably with contemporary data. Findings are consistent with NIF implosions that ignite, since the imploded mass and areal density for the HyT are greater by a factor of 12 and 28, respectively. Assuming the hybrid-type target can be tuned, it has the potential to meet requirements at NIF, even if implosions have to operate at relatively high adiabats. It is also possible that the thermonuclear yield would be suitable for calculation in national security and stockpile stewardship. A strategy for increasing the gain might include an intermediate stage with a target with increased mass and laser energy. If we use the formula provided in the introduction, with $G \sim \eta_{\text{hydro}} \rho R_{\text{max}} v_s^{-4} (E_0 / m_0)^2 / (E_{\text{ign}} / E_{\text{DT}})^2$, we would expect an implosion at adiabat 3 and process the data at adiabat 6 to give $\sim 65 \times (11.2)^{-1} (0.5)^2 / (1)^2 \approx 200$ at laser energies $\sim 8$ MJ. These figures exclude the gain factor of either a? The surrounding cooling blanket, which is designed to boost the net gain by an additional factor of 1.2–1.5.

It is also possible for the gain to be further increased if the peak laser power and energy can be boosted. This strategy could seem counterintuitive, or even counterproductive, but should be expected for implosions at such high gains. The hybrid target has been designed to meet the criteria for ignition while still imploding, as implied in Table 1. In other words, there are tradeoffs that might still be made in gain and the probability of ignition. At present, the hybrid target reproduces the rate of kinetic to internal energy of experiments on the NIF despite an increase in the scale of $12^3 \approx 2 \times 10^3$ and achieves a convergence ratio (CR) of ~20 when it might otherwise reach 30. If we assume the criterion that $CR \propto$ (internal energy)<sup>1/4</sup> and $p \propto$ internal energy $\sim CR^4$ , then the work available to the hotspot should exceed requirements by approximately the same factor (2.1). This figure is

one way to quantify margin and the degree to which the target has been overdone. In calculations at reduced energies, the peak velocity and laser power are found to exceed the thresholds require for a factor of 1.27 and 1.54, respectively. If we were to make another comparison with the NIF, this would be equivalent to taking a diamond target that ignites at 2 MJ (Ref. 1) but instead applying 3 MJ. The hybrid target has been designed to be robust and is also be capable of very high gains. Future efforts will investigate requirements for crystal target hosts and include tolerances on the capsule, its smoothness, the thickness of various layers, and other imperfections in the incoming laser. Preliminary calculations are very promising and suggest specifications on the capsule can be greatly reduced. We will also consider adaptations for the OMEGA and the NIF, and several alternatives including fast ignition<sup>16</sup> or shock ignition.<sup>17</sup> Finally, as part of the milestone-based fusion development program, we report that tests of the Xcimer laser system have just begun and will proceed in parallel.

## ACKNOWLEDGMENTS

This work was made possible by colleagues at LLE, LLNL, LANL, General Atomics, and Xcimer and the encouragement and support of C. Keane, S. B. Regan, D. N. Mayberry, and T. J. B. Collins. This material is based upon work supported by the Department of Energy, National Nuclear Security Administration, under Awards No. DE-NA0004144 and No. DE-NA0000856, the University of Rochester, and the New York State Energy Research and Development Authority. This work was also supported by an INFUSE award with project number RA20224-01. The support of DOE does not constitute an endorsement of the views expressed in this paper. This report was prepared as an account of work sponsored by an agency of the U.S. Government. Neither the U.S. Government nor any agency thereof, nor any of their employees, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights. Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the U.S. Government or any agency thereof. The views and opinions of authors expressed herein do not necessarily state or reflect those of the U.S. Government or any agency thereof.

## AUTHOR DECLARATIONS

### Conflict of Interest

The authors have no conflicts to declare.

### Author Contributions

**C. A. Thomas**: Conceptualization (lead); Funding acquisition (lead); Writing – original draft (lead); Writing – review & editing (lead). **M. Tabak**: Conceptualization (equal); Writing – review & editing (supporting). **C. Alemán**: Conceptualization (equal); Writing – review & editing (supporting). **C. D. Galloway**: Conceptualization (equal); Funding acquisition (lead); Writing – review & editing (supporting).

**E. M. Campbell:** Conceptualization (supporting), Writing – review & editing (supporting). **M. P. Farrell:** Conceptualization (supporting), Writing – review & editing (supporting). **J. L. Kline:** Conceptualization (supporting), Writing – review & editing (supporting). **D. S. Montgomery:** Validation (supporting), Writing – review & editing (supporting). **M. J. Schmitt:** Conceptualization (supporting), Writing – review & editing (supporting). **A. B. Christopherson:** Conceptualization (supporting), Writing – review & editing (supporting). **A. Valeo:** Conceptualization (supporting), Writing – review & editing (supporting).

## DATA AVAILABILITY

The data that support the findings of this study are available from the corresponding author upon reasonable request.

## REFERENCES

¹ T. Stacibalis, L. Wood, A. Thiessen, and G. Zimmermann, *Nature* **239**, 139 (1972).

² D. Ladd, *Inertial Confinement Fusion: The Quest for Ignition and Energy Gains Using Indirect Drive* (AIP Press, New York, 1998), pp. 1–283.

³ J. Nuckolls and J. Meyer-ter-Vehn, *The Physics of Inertial Fusion: Beam Plasma Interaction, Hydrodynamics, Hot Ignition* (Oxford University Press, 2004).

⁴ E. M. Campbell and W. J. Hogan, *Plasma Phys. Controlled Fusion* **41**, B39 (1999).

⁵ M. Abu-Mosteenh, R. Azor, P. Adams, J. Adams, B. Addis, R. Aiken, P. Akinian, R. B. Akyuz, M. Agüeros, S. Aghaian *et al.*, *Phys. Rev. Lett.* **129**, 075001 (2022).

⁶ P. Patel, M. Vranjesky, V. Lobatchev, V. N. Goncharov, and R. L. McCrory, *Phys. Plasmas* **8**, 5337 (2001).

⁷ O. L. Landen, R. Benedetti, D. Blauc, T. R. Boehly, D. K. Bradley, J. A. Caggiano, D. A. Callahan, P. M. Celliers, C. J. Cerjan, D. Clark, G. W. Collins, E. L. Dewald, S. N. Dixit, T. Döppner, D. Edgell, J. Eggert, D. Farley, J. A. Frenje, V. Glebov, S. M. Glenn, S. H. Glenzer, S. W. Haan, A. Hamza, R. A. Hammer, C. A. Haynam, J. H. Herrmann, D. Hicks, D. E. Hinkel, N. Izumi, O. Hicks, D. E. Hinkel, N. Izumi, M. G. Johnson, O. S. Jones, D. H. Kalantar, R. L. Kauffman, J. D. Kilkenny, R. K. Kirkwood, J. Kiser, J. A. Krygier, G. A. Kyrala, O. Lafourtune, C. Ma, A. J. Mackinnon, A. J. MacPhee, E. Mapoles, J. L. Milovich, J. D. Moody, N. B. Meezan, P. Michel, P. Neumayer, A. Nikroo, A. Nikroo, J. Olson, K. Opachich, A. Pak, T. Parham, P. Patel, H. S. Park, J. E. Pertmore, J. Ralph, S. P. Regan, B. A. Remington, H. Rinderknecht, H. F. Robey, M. D. Rosen, J. S. Ross, R. Rygg, J. D. Salmonson, T. C. Sangster, M. B. Schneider, R. K. Spears, P. T. Springer, L. J. Suter, C. A. Thomas, R. P. J. Town, S. V. Weber, P. J. Wegner, K. Widmann, M. D. Wilke, H. Widlund, B. K. Wilson, B. V. Edwards, J. D. Lindl, L. J. Atherton, W. W. Hsing, B. J. MacGowan, B. M. V. Wontargem, and E. I. Moses, *Plasma Phys. Controlled Fusion* **54**, 124026 (2012).

⁸ M. J. Edwards, P. K. Patel, J. D. Lindl, L. J. Atherton, S. H. Glenzer, S. W. Haan, J. D. Kilkenny, O. L. Landen, E. I. Moses, A. Nikroo, R. Petrasso, T. C. Sangster, P. T. Springer, S. Batha, R. Benedetti, L. Bernstein, R. Betti, D. L. Bleuel, T. R. Boehly, D. K. Bradley, J. A. Caggiano, D. A. Callahan, P. M. Celliers, C. J. Cerjan, K. C. Chen, D. S. Clark, G. W. Collins, E. L. Dewald, L. Divol, S. Dixit, T. Doeppner, D. H. Edgell, J. E. Fair, M. Farrell, R. J. Fortner, J. Frenje, M. G. G. Johnson, S. M. Glenn, A. Hamza, S. W. Haan, R. A. Hammer, A. V. Hamza, D. R. Harding, S. P. Hatchett, N. Hein, H. W. Herrmann, D. Hicks, D. E. Hinkel, M. Hoppe, W. W. Hsing, N. Izumi, B. Jacoby, O. S. Jones, D. Kalantar, R. Kauffman, J. L. Kline, J. P. Knauer, J. A. Koch, R. J. Kyrala, K. LaFortune, S. LePane, R. Larson, S. LePape, R. Link, T. Ma, J. L. Milovich, S. Mukhin, K. Otis, T. Parham, R. Petrasso, R. Prasad, J. Ralph, M. D. Rosen, S. Ruggiero, J. Salmonson, D. Sarraf, J. D. Schnittman, M. B. Schneider, P. W. Springer, K. J. Stapef, I. Stern, G. Strozzi, L. J. Suter, C. A. Thomas, R. P. J. Town, P. Wegner, K. Widmann, M. D. Wilke, P. Wilson, H. Stoeckl, W. Stoeckl, N. Izumi, S. A. Spanos, J. M. Fischer, B. Froula, V. Glebov, S. H. Glenzer, S. H. Glenzer, H. A. Glenzer, A. Neumayer, A. Nikroo, M. G. Johnson, D. H. Kalantar, R. L. Kauffman *et al.*, *Phys. Plasmas* **20**, 070501 (2013).

⁹ A. B. Christopherson, R. Betti, J. P. Knauer, A. Bose, Z. M. Doyle, S. T. Ivancic, P. J. Farmelo, E. M. Campbell, J. Delettrez, V. Yu. Glebov, S. T. Ivancic, F. J. Marshall, C. Mileham, J. Miller, C. R. Morse, A. Shvydky, G. Stoeckl, A. A. Solodov, W. Theobald, J. D. Zuegel, M. G. Johnson, R. D. Petrasso, C. K. Li, and J. A. Frenje, *Phys. Rev. Lett.* **127**, 055001 (2021).

¹⁰ A. Thomas, E. M. Campbell, K. L. Baker, D. T. Casey, M. Hohenberger, A. L. Kritcher, B. K. Spears, S. F. Khan, C. Weber, D. S. Clark, E. L. Dewald, L. Berger, D. Strozzi, D. D. Ho, D. Clark, B. Bachmann, J. A. Benedetti, R. Bionta, P. M. Celliers, J. W. Crippen, T. Doppner, M. Eckart, D. N. Fittinghoff, J. Frenje, T. Ma, M. Million, J. R. Nagel, P. K. Patel, C. Trantham, A. Nikroo, M. Stadermann, S. Baxamusa, S. Valdugez, and J. E. Remington, *Phys. Plasmas* **27**, 112701 (2020).

¹¹ K. L. Baker, C. J. Schmitt, B. M. Haines, G. E. Kemp, C. R. Yeamans, R. E. Blue, J. W. Schmitt, A. Head, M. Farrell, P. A. Bradley, D. F. Robey, and R. J. Leeper, *Phys. Plasmas* **28**, 122704 (2021).

¹² C. A. Thomas, K. L. Baker, D. T. Casey, M. Hohenberger, A. L. Kritcher, B. K. Spears, S. A. Khan, A. Herrmann, A. Callahan *et al.*, *Phys. Plasmas* **30**, 023702 (2023).

¹³ C. Galloway and B. Valeo, "IFE pilot plant with a low cost, high energy excimer laser driver," Lawrence Livermore National Laboratory Report No. LLNL-TR-LLNL-658-9 (2022).

¹⁴ J. Nuckolls, *Physics Today* **24**(9), 70 (1982) [?].

¹⁵ V. N. Goncharov, T. C. Sangster, R. Betti, T. R. Boehly, M. J. Bonino, T. J. B. Collins, R. S. Craxton, J. A. Delettrez, D. H. Edgell, R. Epstein *et al.*, *Phys. Plasmas* **21**, 056315 (2014).

¹⁶ *E. I. Moses* (Lawrence Livermore National Laboratory (LLNL), UCID-20117, 2013).

¹⁷ W. Meier, E. Krieger, K. Kindiana, K. Shin, K. Higashi, M. Zaiki, T. Muraoichi, C. Sorge, M. Wakatani, T. Ohki *et al.*, *Fusion Technol.* **25**, 5 (1994).

¹⁸ W. Meier, E. Leferbruge, M. Monsler, and R. Bieri, *Fusion Technol.* **21**, 1 (2001).

¹⁹ J. Sethian, J. Shoreibah, and G. Yolanda, *Phys. Lett. A* **146**, 249 (1990).

²⁰ M. Nishikino, H. Shingu, N. Miyazaga, S. Ohnishi, K. Shigemori, S. Fujoka, K. Nishihara, and Y. Izawa, *Rev. Sci. Instrum.* **71**, 2483 (2000).

²¹ D. Strickland and G. Mourou, *Opt. Commun.* **56**, 219 (1985).

²² E. M. Campbell, V. N. Goncharov, T. C. Sangster, S. P. Regan, P. B. Radha, R. Betti, J. F. Myatt, D. H. Edgell, V. Y. Glebov, D. T. Casey, T. M. Guymer, C. Sorge, J. C. Thomas, D. T. Casey, J. Delettrez, D. H. Edgell *et al.* — *using a fiber fed to evaluate synometrically distributed targets (2021)*.

²³ J. I. Katzir, J. L. Lutenski, and V. Yablada, *Phys. Lett.* **A 106**, 293 (1984); *Phys. Lett.* **A 120**, 323 (1987).

²⁴ K. L. Baker, C. A. Thomas, D. T. Casey, M. G. Johnson, S. Khan, B. K. Spears, R. Nora, T. Woods, J. L. Milovich, R. L. Berger, H. Heirut *et al.*, *Phys. Rev. Lett.* **121**, 135001 (2018).

²⁵ V. Gopalaswamy, R. Betti, J. P. Knauer, N. Luciani, D. Patel, K. M. Woo, A. Bose, I. V. Igumenshchev, E. M. Campbell, K. S. Anderson, K. A. Bauer, M. J. Bonino, D. Cao, A. R. Christopherson, G. W. Collins, T. R. Collins, J. R. Davies, J. A. Delettrez, D. H. Edgell, R. Epstein, C. J. Forrest, D. H. Froula, V. Yu. Glebov, V. N. Goncharov, D. R. Harding, S. X. Hu, I. V. Igumenshchev, R. Janezic, J. H. Kelly, T. Z. Kosc, S. J. Loucks, J. A. Marozas, F. J. Marshall, R. L. McCrory, P. W. McKenty, D. D. Meyerhofer, J. F. Myatt, R. C. Nora, P. B. Radha, S. P. Regan, T. C. Sangster, P. Shaefer, W. Seka, R. W. Short, A. Shvydky, S. Skupsky, A. A. Solodov, C. Stoeckl, W. Theobald, J. Ulreich, M. D. Wittman, K. M. Woo, B. Yaakobi, and J. D. Zuegel, *Nature* **565**, 581 (2019).

²⁶ C. Gundry, V. Gopalaswamy, A. Bose, S. X. Hu, R. Betti, E. M. Campbell, S. P. Regan, S. A. McCoy, D. R. Karasik, J. Peebles, M. Tabak, and W. Theobald, *Phys. Rev. Lett.* **132**, 065104 (2024).

²⁷ R. L. Sherrill, R. L. Berger, A. A. Solodov, R. K. Bachmann, K. L. Baker *et al.*, *Phys. Rev. Lett.* **106**, 185003 (2011).

²⁸ V. Gopalaswamy, A. Lees, R. Betti, J. P. Knauer, A. Bose, I. V. Igumenshchev, E. M. Campbell, S. P. Regan, K. S. Anderson *et al.*, *Nature* **N**, 327105 (2024).

²⁹ P. B. Radha, F. J. Marshall, J. A. Marozas, A. Shvydky, I. Vela, T. R. Boehly, T. J. B. Collins, R. S. Craxton, D. H. Edgell, R. Epstein, V. Yu. Glebov, V. N. Goncharov, R. L. McCrory, P. W. McKenty, D. D. Meyerhofer, R. D. Petrasso, T. C. Sangster, W. Seka, and S. Skupsky, *Phys. Plasmas* **19**, 082704 (2012).

³⁰ M. Gatu Johnson, B. Appelbe, J. Chittenden, A. Crilly, J. Delettrez, C. Forrest, J. A. Frenje, V. Yu. Glebov, H. Sio, C. Stoeckl, and R. D. Petrasso, *Phys. Rev. Lett.* **122**, 035001 (2019).

³¹ K. L. Baker, C. A. Thomas, D. T. Casey, S. Khan, B. K. Spears, R. Nora, T. Woods, J. L. Milovich, R. L. Berger, D. Strozzi, D. D. Ho, D. Clark, O. L. Landen, O. A. Hurricane, A. Nikroo, G. Kyrala, J. L. Kline, E. L. Dewald, D. Eder, M. Stadermann, S. Baxamusa, C. Walters, M. Farrell, D. Mariscal, K. A. Bauer, S. Nagel, M. Hohenberger, and E. R. Mapoles, *Phys. Rev. Lett.* **120**, 085001 (2018).

³² K. Kadowaki, S. Iizuka, H. Kitamura, and H. Takuma, *J. Phys. D: Appl. Phys.* **19**, 441 (1986).

³³ A. L. Kritcher, R. Town, D. Bradley, D. Clark, B. Spears, O. Jones, S. Haan, P. T. Springer, J. Lindl, R. H. H. Scott, D. Callahan, M. J. Edwards, and O. L. Landen, *Phys. Plasmas* **21**, 092711 (2014).

³⁴ B. K. Spears, J. Gaffney, A. Thiagarajan, L. Yang, S. Kruse, D. Soutar, and K. Wohlbier, *Phys. Plasmas* **25**, 080901 (2018).

³⁵ O. A. Hurricane, P. K. Patel, R. Betti, D. H. Froula, S. P. Regan, S. A. Slutz, M. R. Gomez, and M. A. Sweeney, *Rev. Mod. Phys.* **95**, 025005 (2023).

³⁶ D. T. Casey, M. A. Barrios, D. A. Callahan, K. L. Baker, C. R. Weber, H. F. Robey, J. L. Milovich, V. A. Smalyuk, N. B. Meezan, S. F. Khan *et al.*, *Phys. Plasmas* **25**, 056308 (2018).

³⁷ B. K. Spears, J. Brase, P.-T. Bremer, B. Chen, J. Field, J. Gaffney, M. Kruse, J. Lewis, R. Nora, J. Thiagarajan, J. Tromp-vd Berg, B. Van Essen, K. Yoon, and W. Zhou, *Phys. Plasmas* **25**, 080901 (2018).

³⁸ O. L. Landen, J. Braun, D. I. Cottrell, D. T. Casey, A. Benedetti, N. Izumi, J. D. Salmonson, D. A. Callahan, O. A. Hurricane, and J. D. Lindl, *Phys. Plasmas* **21**, 056308 (2014).

³⁹ T. Döppner, B. Bachmann, D. A. Callahan, L. R. Benedetti, T. Bunn, J. A. Caggiano, E. M. Campbell, C. Cerjan, D. T. Casey, E. L. Dewald, L. Divol, S. N. Dixit, T. Doerner, D. H. Edgell, M. J. Edwards, J. Frenje, D. H. Froula, S. M. Glenn, G. P. Grim, S. W. Haan, A. J. Hayes-Sterbenz, H. Herrmann, D. Hinkel, W. W. Hsing, N. Izumi, O. S. Jones, S. F. Khan, J. D. Kilkenny, R. K. Kirkwood, J. Knauer, G. A. Kyrala, O. L. Landen, D. Larson, S. LePape, M. C. Liberatore, T. Ma, B. J. MacGowan, A. J. Mackinnon, P. W. McKenty, D. Meyerhofer, P. Michel, J. D. Moody, A. S. Moore, A. Nikroo, A. Pak, H. S. Park, J. Ralph, S. P. Regan, H. F. Robey, J. S. Ross, J. D. Salmonson, T. C. Sangster, S. Sepke, M. B. Schneider, D. Strozzi, K. Widmann, C. C. Widmayer, E. A. Williams, R. P. J. Town, B. Van Wonterghem, and E. I. Moses, *Phys. Rev. Lett.* **108**, 135006 (2012).

*Phys. Plasmas* **31**, 112758 (2024); doi: 10.1063/5.0233792 **31**, 112758-3

© Author(s) 2024

Physics of Plasmas ARTICLE pubs.aip.org/aip/pop

30A. L. Kritcher, A. B. Zylstra, D. A. Callahan, O. A. Hurricane, C. R. Weber, D.
S. Clark, C. V. Young, J. E. Ralph, D. T. Casey, A. Pak et al., Phys. [Rev. E 106,](https://doi.org/10.1103/PhysRevE.106.025201)
025201 (2022).
31S. D. Bhandarkar, J. E. Fair, B. J. Haid, L. J. Atherton, C. A. Thomas, J. D.
Moody, J. J. Kroll, and A. Nikroo, Report LLNL-JRNL-737820 (Lawrence
Livermore National Laboratory, Livermore, CA, 2017).
32C. A. Thomas, E. M. Campbell, K. L. Baker, D. T. Casey, M. Hohenberger, A. L.
Kritcher, B. K. Spears, S. F. Khan, R. Nora, D. T. Woods, J. L. Milovich, R. L.
Berger, D. Strozzi, D. D. Ho, D. Clark, B. Bachmann, L. R. Benedetti, R. Bionta,
P. M. Celliers, D. N. Fittinghoff, G. Grim, R. Hatarik, N. Izumi, G. Kyrala, T.
Ma, M. Millot, S. R. Nagel, P. K. Patel, C. Yeamans, A. Nikroo, M. Tabak, M. G.
[Johnson, P. L. Volegov, and S. M. Finnegan, Phys. Plasmas 27, 112712 (2020b).](https://doi.org/10.1063/5.0019191)
33C. A. Thomas, E. M. Campbell, K. L. Baker, D. T. Casey, M. Hohenberger, A. L.
Kritcher, B. K. Spears, S. F. Khan, R. Nora, D. T. Woods, J. L. Milovich, R. L.
Berger, D. Strozzi, D. D. Ho, D. Clark, B. Bachmann, L. R. Benedetti, R. Bionta,
P. M. Celliers, D. N. Fittinghoff, G. Grim, R. Hatarik, N. Izumi, G. Kyrala, T.
Ma, M. Millot, S. R. Nagel, P. K. Patel, C. Yeamans, A. Nikroo, M. Tabak, M. G.
[Johnson, P. L. Volegov, and S. M. Finnegan, Phys. Plasmas 27, 112708 (2020c).](https://doi.org/10.1063/5.0019193)
34T. R. Boehly, D. L. Brown, R. S. Craxton, R. L. Keck, J. P. Knauer, J. H. Kelly, T.
J. Kessler, S. A. Kumpan, S. J. Loucks, S. A. Letzring, F. J. Marshall, R. L.
McCrory, S. F. B. Morse, W. Seka, J. M. Soures, and C. P. Verdon, [Opt.](https://doi.org/10.1016/S0030-4018(96)00325-2)
[Commun. 133, 495 (1997).](https://doi.org/10.1016/S0030-4018(96)00325-2)
35D. Eimerl, E. M. Campbell, W. F. Krupke, J. Zweiback, W. L. Kruer, J. Marozas,
J. Zuegel, J. Myatt, J. Kelly, D. Froula et al., J. Fusion Energy 33, 476 (2014).
36S. J. Ali, P. M. Celliers, S. Haan, T. R. Boehly, N. Whiting, S. H. Baxamusa, H.
Reynolds, M. A. Johnson, J. D. Hughes, B. Watson et al., Phys. [Plasmas](https://doi.org/10.1063/1.5047943) 25,
092708 (2018).
37Y. B. Zeldovich and Y. P. Raizer, Physics of Shock Waves and HighTemperature Hydrodynamic Phenomena (Dover Publications Inc.; Mineola,
NY, 2002).
38V. N. Goncharov, S. Skupsky, T. R. Boehly, J. P. Knauer, P. McKenty, V. A.
Smalyuk, R. P. J. Town, O. V. Gotchev, R. Betti, and D. D. Meyerhofer, [Phys.](https://doi.org/10.1063/1.874028)
[Plasmas 7, 2062 (2000).](https://doi.org/10.1063/1.874028)
39R. S. Craxton, K. S. Anderson, T. R. Boehly, V. N. Goncharov, D. R. Harding, J.
P. Knauer, R. L. McCrory, P. W. McKenty, D. D. Meyerhofer, J. F. Myatt, A. J.
Schmitt, J. D. Sethian, R. W. Short, S. Skupsky, W. Theobald, W. L. Kruer, K.
Tanaka, R. Betti, T. J. B. Collins, J. A. Delettrez, S. X. Hu, J. A. Marozas, A. V.
Maximov, D. T. Michel, P. B. Radha, S. P. Regan, T. C. Sangster, W. Seka, A. A.
Solodov, J. M. Soures, C. Stoeckl, and J. D. Zuegel, Phys. [Plasmas](https://doi.org/10.1063/1.4934714) 22, 110501
(2015).
40S. X. Hu, D. T. Michel, A. K. Davis, R. Betti, P. B. Radha, E. M. Campbell, D.
[H. Froula, and C. Stoeckl, Phys. Plasmas 23, 102701 (2016).](https://doi.org/10.1063/1.4962993)
41S. X. Hu, W. Theobald, P. B. Radha, J. L. Peebles, S. P. Regan, A. Nikroo, M. J.
Bonino, D. R. Harding, V. N. Goncharov, N. Petta, T. C. Sangster, and E. M.
[Campbell, Phys. Plasmas 25, 082710 (2018).](https://doi.org/10.1063/1.5044609)
42J. L. Peebles, S. X. Hu, W. Theobald, V. N. Goncharov, N. Whiting, P. M.
Celliers, S. J. Ali, G. Duchateau, E. M. Campbell, T. R. Boehly, and S. P. Regan,
[Phys. Rev. E 99, 063208 (2019).](https://doi.org/10.1103/PhysRevE.99.063208)
43P. B. Radha, V. N. Goncharov, T. J. B. Collins, J. A. Delettrez, Y. Elbaz, V. Y.
[Glebov, R. L. Keck, D. E. Keller, J. P. Knauer, J. A. Marozas et al., Phys. Plasmas](https://doi.org/10.1063/1.1857530)
12, 032702 (2005).
44J. A. Marozas, M. Hohenberger, M. J. Rosenberg, D. Turnbull, T. J. B. Collins,
P. B. Radha, P. W. McKenty, J. D. Zuegel, F. J. Marshall, S. P. Regan et al.,
[Phys. Plasmas 25, 056314 (2018).](https://doi.org/10.1063/1.5022181)
45R. C. Shah, S. X. Hu, I. V. Igumenshchev, J. Baltazar, D. Cao, C. J. Forrest, V.
N. Goncharov, V. Gopalaswamy, D. Patel, F. Philippe, W. Theobald, and S. P.
[Regan, Phys. Rev. E 103, 023201 (2021).](https://doi.org/10.1103/PhysRevE.103.023201)
[46A. Schmitt, Appl. Phys. Lett. 44, 399 (1984).](https://doi.org/10.1063/1.94788)
47J. A. Marozas, F. J. Marshall, R. S. Craxton, I. V. Igumenshchev, S. Skupsky, M.
J. Bonino, T. J. B. Collins, R. Epstein, V. Y. Glebov, D. Jacobs-Perkins, J. P.
Knauer, R. L. McCrory, P. W. McKenty, D. D. Meyerhofer, S. G. Noyes, P. B.
Radha, T. C. Sangster, W. Seka, and V. A. Smalyuk, Phys. [Plasmas](https://doi.org/10.1063/1.2184949) 13, 056311
(2006).
48T. J. B. Collins, J. A. Marozas, K. S. Anderson, R. Betti, R. S. Craxton, J. A.
Delettrez, V. N. Goncharov, D. R. Harding, F. J. Marshall, R. L. McCrory, D. D.
Meyerhofer, P. W. McKenty, P. B. Radha, A. Shvydky, S. Skupsky, and J. D.
[Zuegel, Phys. Plasmas 19, 056308 (2012).](https://doi.org/10.1063/1.3693969)

49F. H. Seguin, C. K. Li, J. L. DeCiantis, J. A. Frenje, J. R. Rygg, R. D. Petrasso, F.
J. Marshall, V. Smalyuk, V. Y. Glebov, J. P. Knauer, T. C. Sangster, J. D.
[Kilkenny, and A. Nikroo, Phys. Plasmas 23, 032705 (2016).](https://doi.org/10.1063/1.4943883)
50F. J. Marshall, P. B. Radha, M. J. Bonino, J. A. Delettrez, R. Epstein, V. Y.
Glebov, D. R. Harding, C. Stoeckl, J. A. Frenje, M. G. Johnson, F. H.
Seguin, H. Sio, A. Zylstra, and E. Giraldez, Phys. [Plasmas](https://doi.org/10.1063/1.4940939) 23, 012711
(2016).
51D. S. Clark, C. R. Weber, V. A. Smalyuk, H. F. Robey, A. L. Kritcher, J. L.
[Milovich, and J. D. Salmonson, Phys. Plasmas 23, 072707 (2016).](https://doi.org/10.1063/1.4958812)
52E. L. Dewald, D. S. Clark, D. T. Casey, S. F. Khan, D. Mariscal, P. D. Nicola, B.
J. MacGowan, E. P. Hartouni, M. S. Rubery, C. Choate, A. Nikroo, V. A.
Smalyuk, O. L. Landen, M. Ratledge, P. Fitzsimmons, M. Farrell, M. Mauldin,
[and N. Rice, Phys. Plasmas 29, 092703 (2022).](https://doi.org/10.1063/5.0100095)
53N. Rice, M. Vu, C. Kong, M. Mauldin, A. Tambazidis, M. Hoppe, P.
Fitzsimmons, M. Farrell, D. Clark, E. Dewald, and V. Smalyuk, [Fusion](https://doi.org/10.1080/15361055.2017.1389603) Sci.
[Technol. 73, 279 (2018).](https://doi.org/10.1080/15361055.2017.1389603)
54M. Ratledge, E. D. Rio, B. Watson, N. Said, N. Rice, M. Farrell, E. Dewald, A.
[Nikroo, and D. Clark, Fusion Sci. Technol. 79, 801 (2023).](https://doi.org/10.1080/15361055.2023.2210705)
55P. McKenty, Laboratory for Laser Energetics, University of Rochester, private
communication  - unpublished experiments at the National Ignition Facility
that demonstrate shims (2024).
56P. Michel, S. H. Glenzer, L. Divol, D. K. Bradley, D. Callahan, S. Dixit, S.
Glenn, D. Hinkel, R. K. Kirkwood, J. L. Kline, W. L. Kruer, G. A. Kyrala, S. L.
Pape, N. B. Meezan, R. Town, K. Widmann, E. A. Williams, B. J. MacGowan, J.
[Lindl, and L. J. Suter, Phys. Plasmas 17, 056305 (2010).](https://doi.org/10.1063/1.3325733)
57P. B. Radha, M. Hohenberger, D. H. Edgell, J. A. Marozas, F. J. Marshall, D. T.
Michel, M. J. Rosenberg, W. Seka, A. Shvydky, T. R. Boehly et al., [Phys.](https://doi.org/10.1063/1.4946023)
[Plasmas 23, 056305 (2016).](https://doi.org/10.1063/1.4946023)
[58B. Scheiner and M. Schmitt, Phys. Plasmas 26, 024502 (2019).](https://doi.org/10.1063/1.5085122)
[59D. Montgomery, Phys. Plasmas 23, 055601 (2016).](https://doi.org/10.1063/1.4946016)
60D. Strozzi, Lawrence Livermore National Laboratory, private communication –
formulations of gain metrics (2023).
61M. Hohenberger, P. B. Radha, J. F. Myatt, S. LePape, J. A. Marozas, F. J.
Marshall, D. T. Michel, S. P. Regan, W. Seka, A. Shvydky et al., Phys. [Plasmas](https://doi.org/10.1063/1.4920958)
22, 056308 (2015).
62A. A. Solodov, M. J. Rosenberg, M. Stoeckl, A. R. Christopherson, R. Betti, P. B.
Radha, C. Stoeckl, M. Hohenberger, B. Bachmann, R. Epstein et [al., Phys.](https://doi.org/10.1103/PhysRevE.106.055204) Rev.
[E 106, 055204 (2022).](https://doi.org/10.1103/PhysRevE.106.055204)
63D. Barlow, T. Goffrey, K. Bennett, R. H. H. Scott, K. Glize, W. Theobald,
K. Anderson, A. A. Solodov, M. J. Rosenberg, M. Hohenberger, N. C.
Woolsey, P. Bradford, M. Khan, and T. D. Arber, Phys. [Plasmas](https://doi.org/10.1063/5.0097080) 29,
082704 (2022).
64S. P. Obenschain, A. J. Schmitt, J. W. Bates, M. F. Wolford, M. C. Myers, M. W.
McGeoch, M. Karasik, and J. L. Weaver, Phil. [Trans.](https://doi.org/10.1098/rsta.2020.0031) R. Soc. A 378, 20200031
(2020).
65B. Afeyan and S. Huller,€ [EPJ Web Conf. 59, 05009 (2013).](https://doi.org/10.1051/epjconf/20135905009)
66A. Solodov, Laboratory for Laser Energetics, private communication - calculations with various stopping formula (2023).
67M. J.-E. Manuel, B. Khiar, G. Rigon, B. Albertazzi, S. R. Klein, F. Kroll, F. E.
Brack, T. Michel, P. Mabey, S. Pikuz, J. C. Williams, M. Koenig, A. Casner, and
[C. C. Kuranz, Matter Radiat. Extremes 6, 026904 (2021).](https://doi.org/10.1063/5.0025374)
68V. N. Goncharov, J. P. Knauer, P. W. McKenty, P. B. Radha, T. C. Sangster, S.
Skupsky, R. Betti, R. L. McCrory, and D. D. Meyerhofer, Phys. [Plasmas](https://doi.org/10.1063/1.1562166) 10,
1906 (2003).
[69K. Anderson and R. Betti, Phys. Plasmas 11, 5 (2004).](https://doi.org/10.1063/1.1632903)
[70M. Tabak, Euro. Phys. J. D 44, 265 (2007).](https://doi.org/10.1140/epjd/e2006-00199-6)
71A. M. Schwendt, A. Nobile, P. L. Gobby, W. P. S., Jr., D. G. Colombant, J. D.
Sethian, D. T. Goodin, and G. E. Besenbruch, Fusion Sci. Technol. 43, 217
(2002).
72US DOE Office of Fusion Energy Sciences, “Inertial Fusion Energy: Report of
[the 2022 Fusion Energy Sciences Basic Research Needs Workshop,” https://science.](https://science.osti.gov/-/media/fes/pdf/workshop-reports/2023/IFE-Basic-Research-Needs-Final-Report.pdf)
[osti.gov/-/media/fes/pdf/workshop-reports/2023/IFE-Basic-Research-Needs-Final-](https://science.osti.gov/-/media/fes/pdf/workshop-reports/2023/IFE-Basic-Research-Needs-Final-Report.pdf)
[Report.pdf (2023).](https://science.osti.gov/-/media/fes/pdf/workshop-reports/2023/IFE-Basic-Research-Needs-Final-Report.pdf)
[73R. A. Sacks and D. H. Darling, Nucl. Fusion 27, 447 (1987).](https://doi.org/10.1088/0029-5515/27/3/009)
74T. J. B. Collins, J. A. Marozas, R. Betti, D. R. Harding, P. W. McKenty, P. B.
Radha, S. Skupsky, V. N. Goncharov, J. P. Knauer, and R. L. McCrory, [Phys.](https://doi.org/10.1063/1.2709859)
[Plasmas 14, 056308 (2007).](https://doi.org/10.1063/1.2709859)

Phys. Plasmas 31, 112708 (2024); doi: 10.1063/5.0221201 31, 112708-8

VC Author(s) 2024

Physics of Plasmas ARTICLE pubs.aip.org/aip/pop

75R. W. Paddock, H. Martin, R. T. Ruskov, R. H. H. Scott, W. Garbett, B. M. Haines,
A. B. Zylstra, E. M. Campbell, T. J. B. Collins, R. S. Craxton, C. A. Thomas, V. N.
Goncharov, R. Aboushelbaya, Q. S. Feng, M. W. von der Leyen, I. Ouatu, B. T.
Spiers, R. Timmis, R. H. W. Wang, and P. A. Norreys, J. [Plasma](https://doi.org/10.1017/S0022377822000265) Phys. 88,
905880314 (2022).
76S. X. Hu, L. A. Collins, V. N. Goncharov, J. D. Kress, R. L. McCrory, and S.
[Skupsky, Phys. Rev. E 92, 043104 (2015).](https://doi.org/10.1103/PhysRevE.92.043104)
77T. J. B. Collins, A. Poludnenko, A. Cunningham, and A. Frank, Phys. [Plasmas](https://doi.org/10.1063/1.1927099)

12, 062705 (2005).
78J. L. Milovich, O. S. Jones, R. L. Berger, G. E. Kemp, J. S. Oakdale, J. Biener, M.
A. Belyaev, D. A. Mariscal, S. Langer, P. A. Sterne et al., [Plasma](https://doi.org/10.1088/1361-6587/abe353) Phys.
[Controlled Fusion 63, 055009 (2021).](https://doi.org/10.1088/1361-6587/abe353)
79I. V. Igumenshchev, D. H. Edgell, V. N. Goncharov, J. A. Delettrez, A. V.
Maximov, J. F. Myatt, W. Seka, A. Shvydky, S. Skupsky, and C. Stoeckl, [Phys.](https://doi.org/10.1063/1.3532817)
[Plasmas 17, 122708 (2010).](https://doi.org/10.1063/1.3532817)
80V. N. Goncharov, O. V. Gotchev, E. Vianello, T. R. Boehly, J. P. Knauer, P. W.
McKenty, P. B. Radha, S. P. Regan, T. C. Sangster, S. Skupsky et al., [Phys.](https://doi.org/10.1063/1.2162803)
[Plasmas 13, 012702 (2006).](https://doi.org/10.1063/1.2162803)

81C. Stoeckl, R. Epstein, R. Betti, W. Bittle, J. A. Delettrez, C. J. Forrest, V. Y.
Glebov, V. N. Goncharov, D. R. Harding, I. V. Igumenshchev et al., [Phys.](https://doi.org/10.1063/1.4977918)
[Plasmas 24, 056304 (2017).](https://doi.org/10.1063/1.4977918)
82R. Nora, R. Betti, K. S. Anderson, A. Shvydky, A. Bose, K. M. Woo, A. R.
[Christopherson, J. A. Marozas, T. J. B. Collins, P. B. Radha et al., Phys. Plasmas](https://doi.org/10.1063/1.4875331)
21, 056316 (2014).
83J. S. Ross, P. Amendt, L. J. Atherton, M. Dunne, S. H. Glenzer, J. D.
Lindl, E. I. Moses, A. Nikroo, and R. Wallace, Report LLNL-JRNL588175 (2012).
[84R. S. Craxton and D. W. Jacobs-Perkins, Phys. Rev. Lett. 94, 095002 (2005).](https://doi.org/10.1103/PhysRevLett.94.095002)
85R. Betti, A. R. Christopherson, B. K. Spears, R. Nora, A. Bose, J. Howard, K. M.
[Woo, M. J. Edwards, and J. Sanz, Phys. Rev. Lett 114, 255003 (2015).](https://doi.org/10.1103/PhysRevLett.114.255003)
86M. Tabak, J. Hammer, M. E. Glinsky, W. L. Kruer, S. C. Wilks, J.
[Woodworth, E. M. Campbell, M. D. Perry, and R. J. Mason, Phys. Plasmas 1,](https://doi.org/10.1063/1.870664)
1626 (1994).
87K. S. Anderson, R. Betti, P. W. McKenty, T. J. B. Collins, M. Hohenberger, W.
Theobald, R. S. Craxton, J. A. Delettrez, M. Lafon, J. A. Marozas, R. Nora, S.
[Skupsky, and A. Shvydky, Phys. Plasmas 20, 056312 (2013).](https://doi.org/10.1063/1.4804635)

Phys. Plasmas 31, 112708 (2024); doi: 10.1063/5.0221201 31, 112708-9

VC Author(s) 2024

