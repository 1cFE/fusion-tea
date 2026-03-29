---
source: "https://arxiv.org/pdf/2308.07417"
source_type: "url"
extracted_at: "2026-03-29T16:48:58.088838+00:00"
content_hash_sha256: "4eb2e3e892fa1a9d21f3eae5fbdb889c2bcb8ec08b0cf7d5fd32f53fd0b086e8"
backend: "pdf_pipeline"
---

## ULTRAFAST LASER ARCHITECTURES FOR

### QUANTUM CONTROL OF NUCLEAR FUSION

**Jake Levitt**
Cortex Fusion Systems, Inc.
New York, NY 10128
`[jakelevitt@cortexfusion.systems](mailto:jakelevitt@cortexfusion.systems)`

August 16, 2023

## **ABSTRACT**

Quantum control of nuclear fusion involves engineering quantum coherences in a nuclear wavepacket
to accelerate tunneling through the Coulomb barrier and modifying the analytic structure of the
_S_ -matrix to facilitate long-range reactive capture. We present a three-body fusion reaction which
is amenable to quantum control. The main result of the present inquiry is the discovery of an
embodied class of ultrafast laser architectures [Levitt _et al._, U.S. Patent Application No. 17/855,476
(2022)] which realize solutions to the Schrödinger equation in a logically consistent manner as to that
presented in [Saha _et al._, Mol. Phys. **110**, 9–10 (2012)]. Further, we provide some necessary (but not
necessarily sufficient) conditions for net electrical power production using the optical designs here.

**1** **Background**

**1.1** **Quantum coherences:** **tunneling through Coulombic barriers**

Progress in ultrafast laser science has delivered devices with high optical bandwidth which are capable of resonantly
exciting a coherent superposition between many molecular states [1]. In this scenario, molecular quantum dynamics are
driven by both the populations of the molecular quantum states as well as their quantum coherences, leading to various
non-classical phenomena in matter [2, 3, 4] which are, furthermore, controllable [5, 6]. In a model study of quantum
dynamics, repeated π phase-kicks to a basis state coupled with the continuum has been shown to modulate population
transfer via control over the imaginary component of coherences responsible for quantum dynamics, at first order in
perturbation theory. This yields unitary dynamics analogous to the projective quantum Zeno and anti-Zeno effects

[7]. In the unitary case, the extent to which acceleration of population transfer (anti-Zeno effect) occurs is determined
by the timing between successive operations of the phase-kick [8]. In 2012, a model of π phase-kicks operating on
a nuclear wavepacket ( _i.e.,_ a coherent superposition of nuclear rotational and vibrational states) bound in a trap with
Coulombic (MeV-scale) barriers was presented to achieve a highly accelerated tunneling escape into the continuum of
fusion products with extremely high energy efficiency [9]. This offered the first evidence that dynamics modulated by
the anti-Zeno effect could be useful in a coherent, ultrafast controlled fusion scenario involving an adequately prepared
molecule. Specifically, the chemically bound nuclei must be coupled to narrow, near-threshold resonances of fusion
products which have the same baryonic content as the molecule ( _e.g.,_ a [6] Li(D, α) [4] He fusion reaction proceeding
through the 2 [+] resonance in [8] Be; the 2 [+] resonance energy is (22.2 + i0.8)MeV and the [6] Li + D cluster breakup
threshold in [8] Be is located at 22.2798MeV above the ground state; [6] Li and D are also found chemically bonded, so
the states of the [6] LiD molecule are embedded as resonances in the [8] Be spectrum at the [6] Li + D cluster breakup
threshold energy) [10, 11, 12]. A “narrow, near-threshold resonance” refers to a resonance in the composite nucleus
which is located near a breakup threshold into charged clusters which can also chemically bind to form a molecule.
The remainder of the present inquiry will involve discussions of the overlap between molecular and resonance states in
this case, as well as the embodied mechanism which efficiently accesses the resonance starting from the molecular
states. The key result of the present work is the presentation of a class of ultrafast laser designs which realize molecular
dynamics in a logically consistent manner to that of the control protocol [9], for a molecular system which also exhibits

a non-zero, controllable overlap with a narrow, near threshold resonance in a composite nucleus formed from the
baryonic components of the molecule.

**1.2** **Embodying phase-kick control with holonomy**

Various embodiments of the π phase-kick control have been proposed [13, 14] in which there is a one-to-one correspondence between optical pulses and phase-kicks. However in the model [9], an ultrashort time between phase-kicks, of
less than half a femtosecond (fs), was required to observe tunneling acceleration through a Coulombic barrier. This
implies that repeated phase-kicks on a nuclear wavepacket must be executed by an individual fs pulse ( _i.e.,_ there must be
a one-to-many relationship between optical pulses and phase-kicks). In order to achieve this, we will consider molecular
systems in which, additionally, an intrinsic feature of the electronic structure (the ability to induce degeneracies between
two electronic surfaces with a laser) can be leveraged to realize repeated phase-kicks on a nuclear wavepacket according
to the time spacing in [9] and accessible with one additional fs control pulse following ultrafast excitation. A nuclear
wavepacket on R [2] which completes a closed loop around a degeneracy between electronic surfaces acquires a geometric
phase exactly equal to π [15, 16]. The acquisition of this geometric phase flips the sign of coherences between the basis
states of the nuclear wavepacket and the narrow, near threshold resonance, leaving unaltered the projection of the total
system wavefunction (molecule and composite nucleus) over the continuum of fusion product channels. The geometric
phase associated with degeneracies between electronic surfaces is, therefore, the same π phase-kick encountered in

[7, 8, 9]. In general, degeneracies between two electronic surfaces equip the Hermitian line bundle over the nuclear
Hilbert space ( _i.e.,_ the projective Hilbert space of nuclear wavepacket configurations on a given electronic surface in the
molecule), whose typical fiber is the U(1) Lie group, with the holonomy of the structural group of the Möbius strip
fiber bundle Z2 _⊗_ U(1) [17]. For U(1) fibers, the holonomy manifests as a _phase_ : it can therefore be used for unitary
(phase-kick) quantum control of the nuclear wavepacket.

In essence, we will have the nuclear wavepacket execute its own phase-kicks simply by evolving on an electronic
structure with degeneracies. The associated dynamics are furthermore amenable to ultrafast laser control as follows.
In the Floquet picture of quantum mechanics, light-molecule interactions are described in terms of “dressed states,”
molecular states that are shifted in energy according to the perturbational field frequency, intensity, and polarization.
The dressed states determine effective light-induced potentials with the usual topological features of multidimensional
potential energy surfaces, such as the emergence of light-induced electronic degeneracies [18] which can inherit
their positions from degeneracies in the natural electronic structure. In this regard, unitary control over the nuclear
wavepacket with holonomy is effected by applying intense laser fields, to induce degeneracies between electronic
surfaces at specific (desired) and time-dependent locations in the nuclear Hilbert space [19, 20, 21, 22, 23, 24]. Control
over the position, and emergent timing, of degeneracies in the light-renormalized electronic structure with a fs control
pulse enables execution of repeated, ultrafast phase-kicks on the nuclear wavepacket as it evolves dynamically on the
light-renormalized electronic structure following resonant excitation. In this regard, a two-pulse, phase-locked control
protocol acting on the appropriate molecule will spawn a nuclear wavepacket and then develop a severe quantum
interference pattern in the nuclear wavepacket, in correspondence with the control proposed by [9].

Separately, if the spectral width of the laser pulse used for control is smaller than that of the Frank-Condon manifold,
but much larger than the vibrational frequency, then the nuclei move during the dynamics associated with ultrafast
excitation, and the nuclear wavepacket is transformed into a squeezed state in which the quantum uncertainty of
its momentum is larger than, _i.a.,_ that of the ground vibrational state of the corresponding vibrational potential

[25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]. The laser may therefore also be used to prepare a nuclear wavepacket with
a large momentum spread around the energy of the narrow, near-threshold resonance, if the resonance is sufficiently
low-lying with respect to the molecular states so as to be accessible with multiple photons provided by the control
pulse. The trade-off here is between preparing the nuclear wavepacket in a configuration having a large overlap with
the narrow, near threshold resonance and ionizing the molecule, which prohibits any further phase-kick control of the
nuclear wavepacket.

We will see in Subsection 1.5 and Section 2 that a molecule which fulfills conditions proposed in the previous paragraphs
is the water molecule (H2O), and the fusion reaction of interest is the [16] O(2p, γ) [18] Ne reaction ( _i.e.,_ two-proton
capture by [16] O).

**1.3** **Nuclear Vertex Constants:** **long-range reactive capture**

To get a sense of the coupling between molecular states and a narrow, near-threshold resonance – starting from molecular
states with energies in the deep sub-Coulomb regime – we will employ the Nuclear Vertex Constants (NVCs) which are,
for the [16] O(2p, γ) [18] Ne fusion reaction, encoded explicitly by the overlap integral of Equation 1.5. The NVCs specify
the projection _⟨_ ψ [JM] mol [(][X][)][|][ψ] nuc [JM][(][X][)] _[⟩]_ [of the resonance wavefunction defined,] _[ e.g.,]_ [ by Equation 1.3, onto the molecular]

wavefunction defined, *e.g.*, by Equation 1.2. We consider the nuclear wavepacket in a molecule to comprise a product of charged sub-clusters unbound with respect to the strong force, but which are chemically bound. The relationship between this projection and the NVCs proceeds via the Asymptotic Normalization Coefficients (ANCs) in Equation (3) and Equation (8) of [36]. In the example system from the first paragraph, the sub-cluster wavefunction would specify the configuration of $^4$He and D when they are chemically bound in the $^6$LiD molecule, and the NVCs would provide the probability amplitude that the $2^+$ resonance in $^6$Be is formed from the asymptotic tail of the $^6$Be nuclear wavefunction overlapping with the molecular wavefunction. The NVCs are sufficient to consider in the cross section since the nuclear reaction of interest will proceed, because of the Coulomb barrier, at very large distances compared to the strong interaction radius between the clusters ($\gg$ 1fm), and the NVCs determine entirely the cross section for such a long-range reactive capture (fusion) reaction [37]. In the current inquiry we will furthermore see that in the special case (Subsection 1.5), the NVCs are amenable to the squeezing control described in (Subsection 1.2) via a renormalization of the breakdown of adiabaticity in the field. The analysis (Subsection 1.5) provides grounding evidence, via computation of an overlap integral encoding the NVCs, that a long-range $^{16}O(2p,\gamma)^{18}$Ne reactive capture reaction is possible.

## 1.4 S-matrix poles: engineering the width of narrow, near-threshold resonances

As we will see in Subsection 1.5 for the $^{16}O(2p,\gamma)^{18}$Ne fusion reaction, the width of the narrow, near-threshold resonance partially determines the ANCs, also approached by Equations (3-8) of [36]. In the current inquiry it will be necessary to consider how to engineer this resonance width to facilitate the long-range reactive capture. We will proceed as follows: the S-matrix $\mathbb{S}$ can be factored into Jost matrices [39, 40, 41]

$$\mathbb{S} = \frac{f^{(+)}(k)}{f^{(-)}(k)},\tag{1.1}$$

![](images/page_002_eq_0.png)
where $f^{\pm}(k)$ are the $K$-space representation of the Jost functions and we have defined $\mathbb{S}$ in terms of its matrix elements. We consider the poles of $\mathbb{S}$ to be the zero points of $f^{(-)}(k)$, which correspond to bound states and resonances, and in turn depend on the quantum mechanical potential for the scattering process (*e.g.*, the fusion reaction coordinate). It is then trivial to see how the analytic structure of $\mathbb{S}$ is amenable to control by strong fields. The narrow, near-threshold resonance is here interpreted as a complex pole of $\mathbb{S}$, in the second sheet of the analytic continuation of $\mathbb{S}$ to the complex plane of the momenta. In the Floquet picture of quantum mechanics, diverse $\mathbb{S}$ pole trajectories can be realized along the frequency [42, 43], intensity [44, 45, 46], and polarization [46] degrees of freedom of an applied control pulse. The control pulse can therefore access poles [47], as well as change the location of branch points in the Riemann surface of the matrix elements of $\mathbb{S}$ [48]. The NVCs are directly related to the residue of $\mathbb{S}$ at the pole via the ANCs by Equation (8) of [36] and Equation (11) of [37].

In general the NVCs are amenable to control by intense laser fields (*See, e.g.*, [48] for controlling the residue of $\mathbb{S}$ at the pole). In the case of the $^{16}O(2p,\gamma)^{18}$Ne reaction, transitions probabilities starting from molecular states are sensitive to minor changes in the position of the pole for the narrow resonance near the breakup threshold into clusters (and in fact, there is an exceptional point at the threshold [36]). Together these arguments imply that the width of the narrow, near threshold resonance can be altered to modify the NVCs, and that, in the special scenario of (Equation 1.5), the laser bandwidth and peak pulse intensity detailed in (Section 2) are sufficient to effect control of the $^{16}O(2p,\gamma)^{18}$Ne fusion reaction at the level of the analytic structure of $\mathbb{S}$.

## 1.5 Three-body system

The water molecule (H₂O) is a platform on which the $^{16}O(2p,\gamma)^{18}$Ne three-body fusion reaction [10, 11] can be assisted by making use of an ultrafast laser control protocol (Section 2) which acts on water molecules. We recognize that in the traditional context of plasma astrophysics the temperatures and densities required for such a reaction are exceedingly rare [49, 50, 51, 52, 53, 54]. Following [11], we are going to show that in the case of the $^{16}O(2p,\gamma)^{18}$Ne reaction starting from water, the cross section, as determined by an overlap integral encoding the NVCs for this reaction, is non-trivial and furthermore, amenable at the level of the analytic structure of $\mathbb{S}$ and specifically amenable to the control in [9]. Our control protocol acts on the nuclear wavepacket in a molecule and does not involve the creation of a plasma. In fact, it is a coherent process that occurs before thermalization, proceeding entirely according to Schrödinger dynamics.

The $^{18}$Ne spectrum exhibits a $3^+$ excited state resonance which is low-lying with respect to the three-body p + p + $^{16}$O cluster breakup threshold [55, 56, 57] (*i.e.*, the initial state and final state are embedded as resonances in the $^{18}$Ne spectrum at the three-body p + p + $^{16}$O cluster breakup threshold energy, which is close to the $3^+$ state), and $^{18}$Ne is itself a halo nucleus even in the ground state, comprised of the bound clusters p, p, and $^{16}$O [60]. Following [11], we will now compute the overlap between the water molecule and the $3^+$ state in $^{18}$Ne (*i.e.*, encoding the NVCs

for the $^{16}$O(2p, γ)$^{18}$Ne reaction). We note that while in [10, 11] the 3$^−$ state is identified as near-isoenergetic to the p + p +$^{16}$O three-body breakup threshold encoding the $^{18}$Ne, later more advanced spectroscopy of $^{18}$Ne places the 3$^−$ state nearly isoenergetic to the three-body breakup threshold [55, 56, 57] and the 3$^−$ state relatively far below the threshold [58]. For clarity we are taking the three-body breakup threshold energy reported in Figure (11) of [58] (4,523keV above the 0$^+$ ground state). In another commonly cited publication [59] the three-body breakup threshold is reported at 4,522keV above the ground state; in either case the values of the 3$^−$ state energy reported in [55, 56] (4,523.7 ± 2.8keV) and [57] (4,527 ± 1keV) are, within their respective systematic and statistical uncertainty of experiment, isoenergetic or nearly isoenergetic to the three-body breakup threshold.

Following [11], in order to compute the overlap between water and the 3$^−$ resonance of $^{18}$Ne, we will employ an ansatz for the nuclear wavepacket (i.e., in the water molecule, cf. nuclear wavefunction) which accounts for the Coulomb repulsion between the p + p +$^{16}$O clusters at small distances, as well as the separation between the p + p +$^{16}$O clusters when they are chemically bound in the water molecule (i.e., accounting for the geometric size of the water molecule):

$$\psi_{3^-}^{(0)}(X) = \frac{N_{\text{nm}}}{\Omega^{3/2}} e^{-\kappa_3 X} Y_3^0(\hat{q}; \hat{q}_i), \tag{1.2}$$

where the set of hypergeometrical variables $X = (\rho, \omega, \Omega, \hat{q})$ has hyperradius $\rho = \sqrt{\xi^2 + \eta^2}$ and hyperangle $\omega = \arctan(\eta/\xi)$,  $Y_3^0(\hat{q}; \hat{q}_i)$ are the Jacobi variables, the Coulomb harmonics $\psi_l^{(C)}(1, 1)$ [11, 12] with $\Omega = (\omega, \hat{q})$ denoting the five angles in X. The regular solutions of the hyperradial Schrödinger equation are $F_l$ (the regular Coulomb wavefunctions), and $Y_3^0(\hat{q}; \hat{q}_i)$ are eigenfunctions of the total angular momentum operator $l = \{l + l\} = S_l$ with $[Y_3^0]$ having associated with it  $l = 2$ (respectively, $S_l = 3$) from the p+p pair in the water molecule, and $M \in \{-l, -l + 1, ..., l\}$, $N_{\text{nm}}$ is a normalization factor and $\kappa = \sqrt{2\mu_{\text{red}}\mathcal{B}}$ is the momentum corresponding to the chemical binding energy of the clusters in the water molecule ($\varepsilon_{\text{red}} \approx -100\text{eV}$, with reduced mass $\mu = 10m_p/3\hbar$, $\eta_3 = V_3/2\kappa$ is an effective Sommerfeld parameter, where $V_3$ is obtained by averaging $V(3)$ with the angular part of $\psi_{3^-}^{(0)}[X]$.

![](images/page_003_eq_0.png)
As an ansatz for the 3$^−$ state (i.e., the wavefunction describing the composite $^{18}$Ne nucleus, cf. nuclear wavepacket in the water molecule), we will employ the asymptotic form of the Coulombic three-body breakup function normalized to the nuclear volume:

$$\psi_{3^-}^{(\text{NV})}(X) = \frac{1}{N_{\text{nm}}} \frac{F_3(\rho, \omega)}{\rho^{5/2}} Y_3^0(\hat{q}; \hat{q}_i), \tag{1.3}$$

where

$$F_3^1(\rho, \omega) = \int d\hat{q}\, d\hat{q} \exp\left\{3\hat{K}\rho - \frac{V(3)}{2K} \ln(2K\rho)\right\} Y_3^0(\hat{q}; \hat{q}_i), \tag{1.4}$$

![](images/page_003_eq_1.png)
and $K = \sqrt{E}$ is the momentum corresponding to the outgoing p + p +$^{16}$O clusters in a three-body breakup scenario starting from the 3$^−$ state of $^{18}$Ne, or equivalently the gap between the total nuclear wavepacket energy (i.e., in the water molecule, cf. nuclear wavefunction) and the 3$^−$ resonance energy.

![](images/page_003_eq_2.png)
The computed overlap [11] between these three clusters and the threshold 3$^−$ resonance in $^{18}$Ne (i.e., encoding the NVCs) is

![](images/page_003_eq_3.png)
$$\Xi = \exp\left\{-\frac{\pi}{2}\eta_{\text{eff}}^{(0)}\right\} \exp\left\{\ln[\Xi]\right\}, \tag{1.5}$$

where $\eta_{\text{eff}}^{(0)} = V_{\text{nm}}/2K$ is another effective Sommerfeld parameter with $V_{\text{nm}}$ the minimum value of the angular part $V(\Omega)$ of the total Coulomb potential. The phase S depends on $V_{\text{nm}}$ and another parameter $L = K/\kappa$ which by construction has the range $0 \leq L \leq \sqrt{V^2/\varepsilon_{\text{bind}}}$, with $\Gamma$ the partial width of the 3$^−$ resonance in the two-proton channel. The two-proton partial width of a different candidate for the $^{18}$Ne resonance was measured experimentally in [61] and [62], and relates to the magnitude of the chemical binding energy $\varepsilon_{\text{bind}}$. Considering that the one-proton partial width is the predominant contributor to the total width of the 3$^−$ state [55, 56, 57] and the experimental γ partial width of the 3$^−$ state is on the order of tens of meV [63, 64], it is likely that the two-proton partial width of the 3$^−$ state is of similar magnitude to that measured in [61, 62] (i.e., it is extremely narrow), and therefore satisfies the conditions of [12]. There exists a wide subdomain of S as a function of L for which $\text{Im}(S) > 0$ and $|\text{Im}(S)| > 3$, which implies that the overlap integral (Equation 1.5) can, or can be made to (Subsection 1.2, Subsection 1.4), increase exponentially with decreasing K. Starting from these three clusters bound by the chemical binding of water, and using the ultrafast laser control strategies described here, the 3$^−$ state of $^{18}$Ne can therefore be accessed from long range.

## 2 Optical design for facilitated tunneling and long-range reactive capture

The intramolecular quantum dynamics of water (i.e., the quantum dynamics of the nuclear wavepacket) that follow electronic excitation at the Lyman-α wavelength (121nm) are, furthermore, amenable to the phase-kick control described

in (Subsection 1.2) via the "chemical double slit" effect [66]. The effect is essentially a dynamical interference of the nuclear wavepacket with itself as it passes through two conical intersections (CIs; electronic degeneracies) belonging to the electronic structure of water (originating from degeneracies between the $\tilde{B}^1A_1$ and the $\tilde{X}^1A_1$ electronic states; on which the nuclear wavepacket is evolving in superpositions along the relaxation trajectory initiated by the exciting pulse, eliciting hundreds of nodes in the nuclear wavepacket. By manipulating the electronic structure of water with a second control pulse, various additional light-induced CIs can be realized to further develop the nuclear wavepacket quantum interference pattern toward the reactivity described in [9].

We therefore conclude that the laser-assisted $^{14}$O(2p, γ)$^{18}$Ne reaction starting from water requires a two-color, phase-locked ultrafast coherent control protocol, which prepares a nuclear wavepacket in water according to the "chemical double-slit" effect, resequences the electronic structure of water to elicit reactive quantum interference patterns in the nuclear wavepacket according to [9], and provides an optical bath of photons for pumping the nuclear wavepacket to, or closer to, the $3^-$ resonance energy (*i.e.*, taking the $K \rightarrow 0$ limit of (Equation 1.4) [1]) via multiphoton absorption by the nuclear wavepacket. A short but moderately intense field in the deep ultraviolet (DUV; on the order of $10^{10}$ W/cm²) interacts at a delay with the nuclear wavepacket in water prepared by a low-intensity vacuum ultraviolet pulse (VUV; on the order of $10^{11}$ W/cm²) to match, or nearly match, the total energy of the nuclear wavepacket with the $3^-$ resonance in $^{18}$Ne (*i.e.*, taking the $K \rightarrow 0$ limit of (Equation 1.4) [1]). The pulses also induce multiphoton absorption from, or emission to, the field, by the molecule [65], to create CIs in the laser-renormalized electronic structure (consider, *e.g.*, light-induced CIs originating from degeneracies among the light-induced potentials $D^1A_1 - \hbar\omega$ and $\tilde{X}^1A_1 + \hbar\omega$ and the $\tilde{B}^1A_1$ electronic state; all occurring below the first vertical ionization energy of water), which act as a highly augmented "chemical double slit" [66] and endow the nuclear wavepacket with a severe quantum interference pattern as a consequence of repeated phase-kicks as discussed in (Subsection 1.2). Combined these two pulses yield a sharp deviation from the exponential decay into fusion products expressed in [12], concordantly with the anti-Zeno mechanism of [9]. The delicate interplay of both multiphoton effects, guided by the delay stage [150] and the pulse shaper [configurations of Figure 1], is required to observe a reactive quantum interference pattern having the appropriate average energy and amplitude. The first laser source, needed at high intensities, produces simultaneous train of phase-locked pulses of mode-locked radiation, which are responsible for pumping a prepared nuclear wavepacket in fs-scale simultaneously to developing interferences.

$^{18}$Ne decay products (*e.g.*, via the cascade γ decay M2(97.7keV, 3$^- \rightarrow 1^-$) and E1(6.514keV, 1$^- \rightarrow 0^+$)) [55, 56, 58], followed by additional β$^+$ decays from the ground state) can then be captured and used to generate electricity.

In Figure 1 and Figure 2 we present an ultrafast laser architecture based on the bichromatic control protocol [67]. The key elements of the optical design are: initialization of the nuclear wavepacket in water under conditions observed in [66] (the "chemical double-slit") with a first pulse at the Lyman-α resonance [111], followed by laser-based manipulation of the electronic structure of water with a second pulse of a different color to generate a severe quantum interference pattern in the nuclear wavepacket, which exhibits thousands of nodes as computed in alignment with the conditions given by [9] and realized on the fs timescale with holonomy. The two pulses also prepare the nuclear wavepacket in water at, or near, the $3^-$ resonance energy of $^{18}$Ne (*i.e.*, taking the $K \rightarrow 0$ limit of (Equation 1.4) [1]). Achieved control over interferences in a parsimonious manner (*i.e.*, via the photonics described here) lends favorable energy balance to quantum-controlled fusion.

## 2.1 Configuration of the optical table

**Figure 1:** In the embodiment shown, the fusion system includes a laser source [110] and a reactor [150]. Various optical components are used to split and modify the beam generated by the laser source [110] and direct the resulting beams into the reactor [150]. In other embodiments, the fusion system may include different or additional elements. Furthermore, various elements may appear in a different manner than described. The following description is provided by way of examples of the broader principles it embodies. The laser source [110] generates an optical beam having a fundamental frequency. The laser source [110] may be an IR pulsed mode-locked oscillator, pumped with a Coherent V5 continuous wave laser, and a multi-pass ring cavity amplifier, pumped with a Photonics DM-20 Q-switched 170ns Nd:YLF laser. The output of the amplifier may be a 15mJ pulse with 1kHz repetition rate, 30fs pulse duration, and a center wavelength of 780nm. The pulses may be a Ti:sapphire. A center wavelength of 800nm on the blue side of the spectrum (*e.g.*, n≈6nm) may be selected. A beam-splitter [112] splits the beam into two portions. The first portion of the fundamental frequency beam is directed to a first harmonic frequency generator to UV light. The first portion of the fundamental frequency beam is directed to a first β-barium borate (BBO) crystal [122]. The BBO crystal [122] is 2mm-thick and is cut for type-I phase-matching (*e.g.*, θ = 40.3°, φ = 90°) for SHG. The resulting intermediate second harmonic beam may pass through a calcite plate [124] (*e.g.*, a 1mm-thick calcite crystal, θ = 41°, φ = 0°) to compensate for group velocity dispersion (GVD) and a half-wave plate [126] to make the fundamental and second harmonic the same polarization. The fundamental and second harmonic beams may be used to generate

![Figure 1: Configuration of the optical table for generation of low-intensity VUV light and moderate intensity DUV](images/tmpjhl1bppw.pdf-5-0.png)
light, with phase-locking and fs-duration pulses.

one or more additional beams of different harmonics. The fundamental and second harmonic beams are combined in
a second 100µm-thick BBO crystal {128} cut for third harmonic generation (θ = 76 _[◦]_, ϕ = 0 _[◦]_ ) in order to generate
light at 201nm via sum-frequency generation (SFG). After SFG BBO crystal {128}, high-reflectivity dielectric mirrors
for the third harmonic may be used to separate out the third harmonic from the fundamental and second harmonic. A
second beamsplitter {132} may be used to split the third harmonic beam into two portions. The second beamsplitter
{132} may be an uncoated 1mm-thick CaF2 window at 45 _[◦]_ to the beam. The first portion of the third harmonic beam
is directed to a first optical input of the reactor {150} while the second portion is directed to a second optical input
of the reactor via a DUV pulse shaper {160}. The first portion of the third harmonic beam is directed to a lens {142}
( _e.g.,_ a 30cm CaF2 lens) that focuses the DUV light of the third harmonic beam and the second portion of the the beam
having the fundamental frequency into a noble gas cell ( _e.g.,_ within the reactor {150}) to generate a fifth harmonic
VUV beam. A telescope or other optical system may be used to correct for the chromatic aberrations induced by the
lenses {142, 250}. In one embodiment, generation of the fifth harmonic ( _e.g.,_ 121nm) is achieved by non-collinear
four-wave mixing in noble gas ( _e.g.,_ argon) that satisfies the following phase-matching condition:

_⃗_ k5ω = 2 _⃗_ k3ω − _⃗_ kω (2.1)

The pressure of the noble gas cell and the phase-matching angles of the pulses may be calibrated experimentally.

The DUV pulse shaper {160} [68] manipulates the second portion of the third harmonic beam into control pulses that
generate light-induced CIs in the fuel which develop quantum interference patterns realizing the unitary phase-kick
control of tunneling [9]. A radiofrequency (RF) signal is sent to an acousto-optic modulator to generate a sound wave

![](images/page_005_eq_0.png)

![Figure 2: Configuration of the reaction chamber for bichromatic optical control of quantum tunneling with fuel deposited](images/tmpjhl1bppw.pdf-6-0.png)
to the focal volume via molecular beam, and creation of light at the Lyman-α wavelength via non-collinear four-wave
mixing.

from which the optical pulses are diffracted. This enables modifying the phase and amplitude of the different optical
frequencies to shape the DUV pulse. The RF signal can be modulated to shape the optical pulses and obtain a desired
pulse shape. Pattern-recognition or machine learning models may be used to identify the appropriate pulse shapes
which optimally realize phase-kick control with a high fusion output. In embodiments, “closed loop learning control” is
used. A measurement of the yield is performed for a collection of random pulse shapes/sequences. A collection of the
best pulse shapes is used to start a search for an optimal pulse shape/sequence using a pattern recognition algorithm.
Given that one expects a very low fusion yield for a random initial pulse, the system may be initialized with some pulse
shapes that are good first guesses given prior knowledge/experience. Any suitable observable indicative of the amount
of fusion occurring may be used to help guide the system close to the ultimate goal.

**2.2** **Reaction chamber**

**Figure 2** : In the embodiment shown, the reactor {150} includes a noble gas cell {210} and a reaction chamber {220}.
The noble gas cell {210} holds a noble gas or a mixture of noble gasses at a predetermined pressure to facilitate
generation of the fifth harmonic beam. The reaction chamber is where the pulsed optical beams interact with the fuel to
facilitate fusion. In other embodiments, the reactor {150} may be configured differently. The noble gas cell {210} is
supplied noble gas via a gas inlet {214} and maintained at a predetermined pressure. In embodiments, a few hundred
Torr, a pressure between approximately 0.1 and 1 atmosphere (76 to 760 Torr) is used. In one embodiment, the third

harmonic and fundamental frequency beams enter the noble gas cell {210} through an optical input {212} ( _e.g.,_ a
2mm-thick CaF2 window). The beams interact via non-collinear four-wave mixing to generate a fifth harmonic beam.
Insert {215} illustrates an example phase-matching condition for generation of the fifth harmonic beam. The fifth
harmonic beam passes through an optical output {216} ( _e.g.,_ a 500µm-thick CaF2 window), which is a second optical
input into the reaction chamber {220}. The reaction chamber {220} includes a molecular nozzle {222} configured to
generate a molecular beam of the fuel. In Figure 2, the molecular beam is directed to be coming directly out of the
page. The reaction chamber may be maintained at low pressure ( _e.g.,_ 10 [−][7] Torr). In one embodiment, the VUV pulse is
then reflected by a dichroic mirror {240} ( _e.g.,_ with a radius of curvature R = 268mm). The mirror may have a high
reflectivity coating of > 90% at 0 _[◦]_ for 121nm light and < 5% reflectivity for 201nm and 605nm. This enables the
residual DUV and visible radiation left over from VUV generation to be separated from the VUV. The reflected VUV
pulse is focused over the molecular nozzle {222}. The DUV reserved for the second pulse is sent through the dichroic
mirror {240} and also focused over the molecular nozzle {222} with a lens {250} ( _e.g.,_ a 30cm CaF2 lens). The VUV
pulse reflected from the dichroic mirror {240} inside the reaction chamber {220} is steered over the molecular nozzle
{222}. In one embodiment, this is done using a movable mirror mount. An example movable mirror mount is shown in
the inset {270} of the figure. The illustrated movable mirror mount includes a KF40 blank with a hole drilled through
the center of an O-ring groove set around the hole as a window holder. The KF40 window holder is connected to a KF40
bellow. Around the neck of the bellow collar there are three holes in the side where the ball tip head of a high precision
1/4”-80 Fine Hex Adjuster 20 can sit. An aluminium (or other suitable material) frame with three slots is positioned
to lock 1/4”-80 Locking Bushings with Nuts in place. This aluminium frame may be bolted in place independent of
the reaction chamber {220}. The 1/4”-80 Fine Hex Adjusters are threaded through the 1/4”-80 Locking Bushings.
When the reaction chamber {220} comes under vacuum, the bellow contracts and the 1/4”-80 Fine Hex Adjuster ball
tip heads come into contact with the holes in the collar. This acts like a Gimbal mount for the dichroic mirror {240}
and enables steering of the VUV beam. The fifth harmonic and third harmonic pulses interact with fuel molecules in
the molecular beam to facilitate fusion via the control protocol described here. The reaction chamber also includes
one or more energy extractors {230}. The energy extractors {230} interact with fusion products to extract energy. For
example, a high-efficiency scintillator/semiconductor system may be used to convert the fusion products into visible
light and then electrical energy, _etc._ It should be appreciated that any suitable energy extraction methods may be used
to capture the energy released by fusion reactions. Fusion products released isotropically from the focal volume in
the interaction region of the reactor {150} are collected by energy extractors typically configured to maximize the
surface area of the energy extractors around the full 4π solid angle within the confines imposed by other elements of the
system, at a distance according to the damage threshold of the scintillators, the radiant intensity of fusion products, and
radiation transport properties of the scintillator.

**3** **Conclusion:** **necessary (but not necessarily sufficient) conditions for net electrical power**
**production**

Assuming a < 20% scintillator efficiency and a semiconductor system at the Shockley-Quiesser limit of efficiency
(about 30%), the energy available as electrical current from the [16] O(2p, γ) [18] Ne fusion reaction is on the order of a
few hundred keV (a few million kJ/mol of water), for the decay chain presented at the beginning of Section 2. If one
starts with laser pulses having an energy of 1mJ, assuming a 1-3% laser wall-power efficiency, this requires on the order
of 10 [12] fusion events per laser pulse in order to reach parity between input and output electrical power. Supersonic
molecular beams can yield number densities on the order of 10 [16] molecules per cc (and above) [69]. With a laser
focus of 100µm, and a VUV and DUV pulse propagation path length of 1cm in the gas phase, the total focal volume is
10 [−][4] cc, so the total number of molecules in the focal volume can be about 10 [12] molecules (and above). With a VUV
conversion efficiency of 0.01% [70], one can produce on the order of 10 [12] VUV photons per laser pulse, and if all
these photons are absorbed then a fusion yield of near-unity under control achieves net electrical power production. By
engineering higher VUV conversion and laser wall-power efficiencies, lower fusion yields become required to reach
net electrical power production. Considering the tunneling efficiencies accessible under coherent control [9] and the
overlap [11], there is reasonable optimism that such a net electrical power production is possible with contemporary
bandwidth technologies.

**References**

[1] Margaret Gregory _et al._ A laboratory frame density matrix for ultrafast quantum molecular dynamics. _The Journal_
_of Chemical Physics_, 157(16), 2022.

[2] Ilya Averbukh and Naum Perelman. Fractional revivals: Universality in the long-term evolution of quantum wave
packets beyond the correspondence principle dynamics. _Physics Letters A_, 139(9):449–453, 1989.

[3] Marc Vrakking, David Villeneuve, and Albert Stolow. Observation of fractional revivals of a molecular wave
packet. _Physical Review A_, 54(1):R37, 1996.

[4] Zsolt Kis _et al._ Entangled vibrational states in polyatomic molecules. _Physical Review A_, 54(6):5110, 1996.

[5] Thomas Weinacht, Jaewook Ahn, and Philip Bucksbaum. Controlling the shape of a quantum wavefunction.
_Nature_, 397(6716):233–235, 1999.

[6] Richard Judson and Herschel Rabitz. Teaching lasers to control molecules. _Physical Review Letters_, 68(10):1500,
1992.

[7] Rajdeep Saha and Victor Batista. Tunneling under coherent control by sequences of unitary pulses. _The Journal_
_of Physical Chemistry B_, 115(18):5234–5242, 2011.

[8] Jacob (Jake) Levitt and Artur Izmaylov. Coherent control based on quantum Zeno and anti-Zeno effects: Role of
coherences and timing. _arXiv preprint arXiv:2306.08311_, 2023.

[9] Rajdeep Saha, Andreas Markmann, and Victor Batista. Tunneling through Coulombic barriers: quantum control
of nuclear fusion. _Molecular Physics_, 110(9-10):995–999, 2012.

[10] Vladimir Belyaev, Alexander Motovilov, and Werner Sandhas. Fusion reactions in molecules via nuclear threshold
resonances. _Journal of Physics G: Nuclear and Particle Physics_, 22(7):1111, 1996.

[11] Vladimir Belyaev, Alexander Motovilov, and Werner Sandhas. On the possibility of fusion reactions in water
molecules. _arXiv preprint nucl-th/9601021_, 1996.

[12] Vladimir Belyaev and Alexander Motovilov. Perturbation of embedded eigenvalue by a near-lying resonance.
_arXiv preprint nucl-th/9606012_, 1996.

[13] Luis Rego, Sabas Abuabara, and Victor Batista. Multiple unitary-pulses for coherent-control of tunnelling and
decoherence. _Journal of Modern Optics_, 54(16-17):2617–2627, 2007.

[14] Luis Rego, Lea Santos, and Victor Batista. Coherent control of quantum dynamics with sequences of unitary
phase-kick pulses. _Annual Review of Physical Chemistry_, 60:293–320, 2009.

[15] Barry Simon. Holonomy, the quantum adiabatic theorem, and Berry’s phase. _Physical Review Letters_, 51(24):2167,
1983.

[16] Michael Berry. Quantal phase factors accompanying adiabatic changes. _Proceedings of the Royal Society of_
_London_, 392(1802):45–57, 1984.

[17] Ilya Ryabinkin, Loïc Joubert-Doriol, and Artur Izmaylov. Geometric phase effects in nonadiabatic dynamics near
conical intersections. _Accounts of Chemical Research_, 50(7):1785–1793, 2017.

[18] Pablo Videla, Andreas Markmann, and Victor Batista. Floquet study of quantum control of the cis–trans
photoisomerization of rhodopsin. _Journal of Chemical Theory and Computation_, 14(3):1198–1205, 2018.

[19] Gábor Halász _et al._ Conical intersections induced by light: Berry phase and wavepacket dynamics. _Journal of_
_Physics B: Atomic, Molecular and Optical Physics_, 44(17):175102, 2011.

[20] Gábor Halász _et al._ Light-induced conical intersections: Topological phase, wave packet dynamics, and molecular
alignment. _The Journal of Physical Chemistry A_, 116(11):2636–2643, 2012.

[21] Gábor Halász _et al._ Light-induced conical intersections for short and long laser pulses: Floquet and rotating wave
approximations versus numerical exact results. _Journal of Physics B: Atomic, Molecular and Optical Physics_,
45(13):135101, 2012.

[22] Gábor Halász _et_ _al._ Nuclear-wave-packet quantum interference in the intense laser dissociation of the D [+] 2
molecule. _Physical Review A_, 88(4):043413, 2013.

[23] Gábor Halász _et al._ Influence of light-induced conical intersection on the photodissociation dynamics of D [+] 2
starting from individual vibrational levels. _The Journal of Physical Chemistry A_, 118(51):11908–11915, 2014.

[24] Gábor Halász, Péter Badankó, and Ágnes Vibók. Geometric phase of light-induced conical intersections: adiabatic
time-dependent approach. _Molecular Physics_, 116(19-20):2652–2659, 2018.

[25] József Janszky and Yu. Ya. Yushin. Squeezing via frequency jump. _Optics Communications_, 59(2):151–154,
1986.

[26] József Janszky and An. V. Vinogradov. Squeezing via one-dimensional distribution of coherent states. _Physical_
_Review Letters_, 64(23):2771, 1990.

[27] József Janszky _et_ _al._ Competition between geometrical and dynamical squeezing during a Franck-Condon
transition. _Physical Review A_, 50(1):732, 1994.

[28] Thomas Dunn _et al._ Experimental determination of the dynamics of a molecular nuclear wave packet via the
spectra of spontaneous emission. _Physical Review Letters_, 70(22):3388, 1993.

[29] Dmitri Abrashkevich, Ilya Averbukh, and Moshe Shapiro. Optimal squeezing of vibrational wave packets in
sodium dimers. _The Journal of Chemical Physics_, 101(11):9295–9302, 1994.

[30] Ilya Averbukh and Moshe Shapiro. Optimal squeezing of molecular wave packets. _Physical Review A_, 47(6):5086,
1993.

[31] Yukiyoshi Ohtsuki, Hirohiko Kono, and Yuichi Fujimura. Quantum control of nuclear wave packets by locally
designed optimal pulses. _The Journal of Chemical Physics_, 109(21):9318–9331, 1998.

[32] Ilya Grigorenko. Analytical solution for optimal squeezing of wave packet of a trapped quantum particle. _The_
_Journal of Chemical Physics_, 128(10), 2008.

[33] Jianshu Cao and Kent Wilson. A simple physical picture for quantum control of wave packet localization. _The_
_Journal of Chemical Physics_, 107(5):1441–1450, 1997.

[34] Bo Chang _et al._ Adiabatic squeezing of molecular wave packets by laser pulses. _The Journal of Chemical Physics_,
122(20), 2005.

[35] Bo Chang _et al._ Adiabatic and diabatic transformations as physical resources for wave packet squeezing. _Physical_
_Review A_, 73(1):013404, 2006.

[36] Akram Mukhamedzhanov and Robert Tribble. Connection between asymptotic normalization coefficients,
subthreshold bound states, and resonances. _Physical Review C_, 59(6):3418, 1999.

[37] Vaclav Burjan, Jaromir Mrazek, and Giuseppe D’Agata. ANC from experimental perspective. _Frontiers_ _in_
_Astronomy and Space Sciences_, 7:562466, 2020.

[38] Akram Mukhamedzhanov. Resonances in low-energy nuclear processes and nuclear astrophysics and asymptotic
normalization coefficients: a review. _The European Physical Journal A_, 59(3):43, 2023.

[39] Sergey Ershov and Sergei Rakityansky. Jost matrices for some analytically solvable potential models. _Physical_
_Review C_, 103(2):024612, 2021.

[40] Sergei Rakityansky and Nils Elander. Analytic structure of the multichannel Jost matrix for potentials with
Coulombic tails. _Journal of Mathematical Physics_, 54(12), 2013.

[41] Sergei Rakityansky and Nils Elander. Generalized effective-range expansion. _Journal of Physics A: Mathematical_
_and Theoretical_, 42(22):225302, 2009.

[42] Haggai Landa. Singularities of Floquet scattering and tunneling. _Physical Review A_, 97(4):042705, 2018.

[43] Wenjun Li and Linda Reichl. Floquet scattering through a time-periodic potential. _Physical_ _Review_ _B_,
60(23):15732, 1999.

[44] Haruhide Miyagi and Kiyohiko Someda. Unified understanding of tunneling ionization and stabilization of atomic
hydrogen in circularly and linearly polarized intense laser fields. _Physical Review A_, 82(1):013402, 2010.

[45] Haruhide Miyagi and Kiyohiko Someda. Unified view of low- and high-frequency regimes of atomic ionization in
intense laser fields. _Physical Review A_, 80(2):023416, 2009.

[46] K. Unnikrishnan. Semiclassical floquet theory of the S matrix for electromagnetic interactions. _Physical Review_
_A_, 48(6):4539, 1993.

[47] A. I. Magunov, Ingrid Rotter, and Svetlana Strakhova. Laser-induced continuum structures and double poles of
the S-matrix. _Journal of Physics B: Atomic, Molecular and Optical Physics_, 34(1):29, 2001.

[48] D. F. Martinez and Linda Reichl. Transmission properties of the oscillating δ-function potential. _Physical Review_
_B_, 64(24):245315, 2001.

[49] Leonid Grigorenko and Mikhail Zhukov Three-body resonant radiative capture reactions in astrophysics. _Physical_
_Review C_, 72(1):015803, 2005.

[50] Justyna Marganiec _et al._ Experimental study of the [15] O(2p, γ) [17] Ne cross section by Coulomb Dissociation for
the rp process. _Journal of Physics:_ _Conference Series_, 665(1):012046, 2016.

[51] Jesús Casal _et al._ Radiative capture reaction for [17] Ne formation within a full three-body model. _Physical Review_
_C_, 94(5):054622, 2016.

[52] Yulia Parfenova _et al._ From Coulomb excitation cross sections to non-resonant astrophysical rates in three-body
systems: [17] Ne case. _Physical Review C_, 98(3):034608, 2018.

[53] Leonid Grigorenko _et al._ Soft dipole mode in [17] Ne and the astrophysical 2p capture on [15] O. _Physics Letters B_,
641(3-4):254–259, 2006.

[54] Leonid Grigorenko *et al.* Asymptotic normalization coefficient method for two-proton radiative capture. *Physics Letters B*, 811:135852, 2020.

[55] Daniel Bardayan *et al.* Observation of the astrophysically important 3⁺ state in ¹⁸Ne via elastic scattering of a radioactive ¹⁷F beam from ¹H. *Physical Review Letters*, 83(1):45, 1999.

[56] Daniel Bardayan *et al.* The astrophysically important 3⁺ state in ¹⁸Ne and the $^{32}$F(p,γ)¹⁸Ne stellar rate. *Physical Review C*, 62(5):055804, 2000.

[57] Yiannis Pappattas *et al.* The $^{17}$F(p,γ)¹⁸Ne 3⁺ resonance state studied with the $^{16}$O(³He,n)¹⁸Ne reaction. *Physical Review C*, 73(2):025802, 2005.

[58] Robert Charity *et al.* Invariant-mass spectroscopy of ¹⁸Ne, ¹⁴Cl, and ¹⁰C excited states formed in neutron-transfer reactions. *Physical Review C*, 99(4):044304, 2019.

[59] Fay Ajzenberg-Selove Energy levels of light nuclei A = 18 − 20. *Nuclear Physics A*, 475(1):1–198, 1987.

[60] José Lay *et al.* Three-body structure of low-lying ¹⁸Ne states. *The European Physical Journal A*, 44:261–277, 2010.

[61] J. Gomez Del Campo *et al.* Decay of a resonance in ¹⁸Ne by the simultaneous emission of two protons. *Physical Review Letters*, 86(1):43, 2001.

[62] Giuseppe Raciti *et al.* Experimental Evidence of ²He Decay from ¹⁸Ne Excited States. *Physical Review Letters*, 100(19):192503, 2008.

[63] Daniel Bardayan *et al.* Direct measurements of (p,γ) cross-sections at astrophysical energies using radioactive beams and the Daresbury Recoil Separator. *The European Physical Journal A*, 42(3):457–460, 2009.

[64] Kelly Chipps *et al.* First Direct Measurement of the $^{17}$F(p,γ)¹⁸Ne Cross Section. *Physical Review Letters*, 102(15):152502, 2009.

[65] Shih-I Chu and Dmitry Telnov. Beyond the Floquet theorem: generalized floquet formalisms and quasienergy methods for atomic and molecular multiphoton processes in intense laser fields. *Physics Reports*, 390(1-2):1–131, 2004.

[66] Richard Dixon *et al.* Chemical "double slits": dynamical interference of photodissociation pathways in water. *Science*, 285(5431):1249–1253, 1999.

[67] Jacob (Jake) Levitt, Thomas Weinacht, and Herschel Rabitz. Fusion reactor using bichromatic optical control of quantum tunneling. U.S. Patent Application No. 17855,476, Jul. 2022.

[68] Brett Pearson and Thomas Weinacht. Shaped ultrafast laser pulses in the deep ultraviolet. *Optics Express*, 15(7):4385–4388, 2007.

[69] Uzi Even. The Even-Lavie valve as a source for high intensity supersonic beam. *EPJ Techniques and Instrumentation*, 2(1):17, 2015.

[70] Spencer Horton *et al.* Ultrafast internal conversion dynamics of highly excited pyrrole studied with VUV/UV pump probe spectroscopy. *The Journal of Chemical Physics*, 146(6):064306, 2017.