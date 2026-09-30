---
source: "https://arxiv.org/pdf/cond-mat/0608404v1"
source_type: "url"
extracted_at: "2026-09-29T23:05:55.379149+00:00"
content_hash_sha256: "1a17594bf57a447b345a5ed5fb0f64aa55a6414381304f819ffe04b856fb88df"
backend: "pdf_pipeline"
---

# A general scaling relation for the critical current density in Nb3Sn 

# A Godeke[1][,][2] ‡, B ten Haken[1] , H H J ten Kate[1] and D C Larbalestier[2] 

> 1Low Temperature Division, Faculty of Science and Technology, University of Twente, P.O. Box 217, 7500AE Enschede, The Netherlands 

> 2Applied Superconductivity Center, University of Wisconsin, 1500 Engineering Drive, Madison, Wisconsin 53706, USA 

Abstract. We review the scaling relations for the critical current density (Jc) in Nb3Sn wires and include recent findings on the variation of the upper critical field (Hc2) with temperature (T ) and A15 composition. Measurements of Hc2(T ) in inevitably inhomogeneous wires, as well as analysis of literature results, have shown that all available Hc2(T ) data can be accurately described by a single relation from the microscopic theory. This relation also holds for inhomogeneity averaged, effective, Hc2[∗][(][T][ ) results][and][can][be][approximated by][H][c2][(][t][)][/H][c2][(0)][ ∼][= 1][ −][t][1][.][52][,][with][t][ =][ T/T][c][.] Knowing Hc2[∗][(][T][ )][implies][that][also][J][c][(][T][ )][is][known.] We highlight deficiencies in the Summers/Ekin relations, which are not able to account for the correct Jc(T ) dependence. Available Jc(H) results indicate that the magnetic field dependence for all wires from µ0H =[∼] 1 T up to about 80% of the maximum Hc2 can be described with Kramer’s flux shear model, if non-linearities in Kramer plots when approaching the maximum Hc2 are attributed to A15 inhomogeneities. The strain (ǫ) dependence is introduced through a temperature and strain dependent Hc2[∗][(][T, ǫ][)][and][Ginzburg-] Landau parameter κ1(T, ǫ) and a strain dependent critical temperature Tc(ǫ). This is more consistent than the usual Ekin unification of strain and temperature dependence, which uses two separate and different dependencies on Hc2[∗][(][T][ )][and][H] c2[∗][(][ǫ][).][Using][a] correct temperature dependence and accounting for the A15 inhomogeneities leads to the remarkable simple relation Jc(H, T, ǫ)[∼] = (C/µ0H)s(ǫ)(1 − t[1][.][52] )(1 − t[2] )h[0][.][5] (1 − h)[2] , where C is a constant, s(ǫ) represents the normalized strain dependence of Hc2[∗][(0) and] h = H/Hc2[∗][(][T, ǫ][).][Finally,][a][new][relation][for][s][(][ǫ][)][is][proposed,][which][is][an][asymmetric] version of our earlier deviatoric strain model and based on the first, second and third strain invariants. The new scaling relation solves a number of much debated issues with respect to Jc scaling in Nb3Sn and is therefore of importance to the applied community, who use scaling relations to analyze magnet performance from wire results. 

PACS numbers: 74.25.Sv, 74.70.Ad, 74.81.Bd 

Submitted to: Supercond. Sci. Technol. Pre-print of Accepted Topical Review http://www.iop.org/EJ/journal/SUST 

‡ Now at Ernest Orlando Lawrence Berkeley National Laboratory, Berkeley, CA 94720 Electronic address: agodeke@lbl.gov 

## 1. Introduction 

Critical current measurements of Nb3Sn wires are commonly interpolated and extrapolated using a set of empirical relations for Jc(H, T, ǫ), generally referred to as Summers scaling [1]. Although these relations show acceptable accuracy for the description of limited data ranges [2], large discrepancies appear between the fitted values for Tc(0) and Hc2(0) and actual measurements [3]. Also at temperatures above about 13 K and for large compressive and tensile axial strains the Summers scaling is inaccurate. It is thus not suitable for precise extrapolations of measured results across a wide range. These deficiencies are generally recognized and lead to continuing discussions in the literature on improvements [2–12]. Presently, much of the interpretation of measured results and ensuing discussions remain largely empirical and the proposed relations depend, for a significant part, on the initial assumptions. A notable exception is the recent work by Oh and Kim [11, 12] who use Eliashberg theory [13,14] in their attempt to arrive at a better founded scaling formalism. 

As an alternative to empirical approaches, a series of relations resulting from microscopic theory exist for Type II superconductivity. Although the critical current cannot be related quantitatively to the microstructure, various bulk pinning force models have been developed [15–23]. These can be combined with theory on strain dependence [24–26] and the field-temperature phase boundary [27–47]. The latter have been shown to reasonably describe measurements on well defined, quasi-homogeneous laboratory samples [35,43–46,48–51]. 

It is questionable, however, whether such relations can directly describe the behavior of Nb3Sn in technical wires due to the inevitable presence of inhomogeneities. Compositional inhomogeneities result from the A15 stability range from about 18 to 25 at.% Sn [52], combined with the solid state diffusion processes during the A15 formation reaction in wires. The resulting Sn gradients have been unambiguously detected in wires by compositional analysis [53–57], property gradient measurements [54–56, 58–60] and simulations [56, 60–62]. These compositional inhomogeneities lead to significant changes in the electron-phonon interaction strength λep [63]. The interaction strength changes from the weak coupling BCS limit (λep ≪ 1) for 18 at.% Sn to λep[∼] = 1.8 for the stoichiometric composition [48, 63]. As a result, significant changes occur in Hc2(T ) with Sn concentration [48, 49, 63–67]. Since all stable A15 compositions from 18 to 25 at.% Sn are observed in wires, a distribution of properties of about 5 T ≤ µ0Hc2(0) ≤ 31 T and 6 K ≤ Tc(0) ≤ 18 K will occur over the A15 volumes [56]. In addition, it can be expected that also the strain state is far from homogeneous over the A15 volumes in a wire. These arguments render the validity of a full microscopic approach doubtful. Moreover, microscopic based relations can be relatively complex and use a significant number of parameters to describe the material involved. The main goal of this article is to find an improved scaling relation which balances the need for better founded formalisms and practical applicability to measured results in wires. As a starting point we use three central statements, which 

will be detailed further throughout the article. 

Our first statement is that the temperature dependencies Hc2(T ) and Hc(T ) (the thermodynamic critical field) are known. We showed earlier [56, 60] that the shape of Hc2(T ) is constant for all available Nb3Sn results, independent of the sample layout, morphology, A15 composition, strain state or applied critical state criterion and also holds for inhomogeneity averaged, extrapolated, Hc2[∗][(][T][)][data.] This means that the normalized temperature dependence of Hc2 can be described by a single, known function from the microscopic theory. Also Hc(T ) is known [11, 68, 69] and κ1(T ) immediately follows through κ1 = Hc2/([√] 2Hc) [29]. This approach differs from the temperature dependence in the Summers relation, in which Hc2(T ) is calculated from an estimated κ1(T ) [1]. 

Our second statement is that non-linearities, which generally appear in Kramer plots [16] when approaching the maximum Hc2 that is present in a wire, can be attributed to A15 inhomogeneities. This assumption can be validated for specific wire layouts through a combination of simulations and measurements [60, 62]. Alternatively, one can chose to fit measured non-linearities assuming a different pinning model as is often done [5, 7, 15, 70]. This will improve the quality of the fit per specific wire type when approaching the maximum Hc2, but this is also the regime where Jc becomes very low. This regime is therefore of limited interest for applications. Fitting this regime per wire type will obviously result in a reduced overall error but also in a model with significantly reduced generality. We therefore chose not to include such non-linearities in the model fit to arrive at a generally valid relation for all Nb3Sn wires, with a validity up to the regime where the effects of A15 inhomogeneity start to appear (typically from about 80% of the maximum Hc2). 

Our third statement is that the introduction of strain sensitivity occurs solely through strain induced changes in Hc2, Tc and κ1. Alternative approaches can lead to a strain dependent pre-constant in the Jc(H, T, ǫ) relation [5–7, 70], which implies that the pinning efficiency changes with strain. Although this cannot be ruled out, it can be argued that the required change in pinning efficiency of at least a factor of 2 over the relevant strain regime (below 1% axial strain) [7,70], is unrealistically large. A more reasonable approach to our opinion, is to assume that the main effect of strain is a modification of the electron-phonon interaction spectrum, which is supported by recent calculations [11,12,24–26]. This will obviously change directly Tc, Hc2 and Hc and thus κ1. We will show below how this assumption, combined with a known temperature dependence of Hc2 and Hc leads to a consistent introduction of strain and temperature effects in the Jc(H, T, ǫ) relation by stating that Hc2[∗][→][H] c2[∗][(][T, ǫ][)][and][κ][1][→][κ][1][(][T, ǫ][).] Note that this is contrary to the usual unification of strain and temperature dependence, which assumes two separate and different dependencies on Hc2[∗][(][T][)][and][H] c2[∗][(][ǫ][)][[71].] 

We will show below how these three starting points lead to a consistent, simple and accurate relation for Jc(H, T, ǫ). In Section 2, we will summarize the descriptions that are available throughout the literature and arrive at a general form for Jc(H, T, ǫ). In Section 3, we will systematically compare this general form to measurements to 

determine the resulting scaling relation. The overall accuracy will be demonstrated in Section 4 and discussed in Section 5, together with a determination of the minimal required set of measurements that are needed to fully characterize a specific wire. Our conclusions are presented in Section 6. 

## 2. The critical surface 

2.1. Magnetic field dependence 

2.1.1. Relations for the Pinning Force The magnetic field dependence of the critical current density in Nb3Sn is determined by de-pinning of the flux-line lattice and thus by the magnetic field dependence of the bulk pinning force Fp = −Jc × B. The latter depends on the microscopic de-pinning mechanism. A general description for Fp(H) results from the observation that, for a multitude of low temperature superconductors, the bulk pinning force scales according to: 

![](images/tmpe13dtjpa.pdf-0004-06.png)

as was first pointed out by Fietz and Webb [72]. In (1), h is the reduced magnetic field H/Hc2. The value for ν is often obtained by neglecting κ1 and plotting the maximum bulk pinning force against Hc2 on a double logarithmic scale. Values for ν found in this way are usually between 2 and 3 and for Nb3Sn values of 2 and 2.5 are mostly cited. However, since κ1 may change up to 50% with temperature (Section 2.2.3), its temperature dependence cannot be neglected for an accurate description of the critical surface of Nb3Sn. 

Several models for f (h) exist [16–18], but most often the Kramer version is used. Kramer derived two models for f (h), using two regimes. For the regime below the peak in f (h) he assumed that flux motion primarily occurs by de-pinning of individual fluxlines, whereas in the regime above the peak in f (h), de-pinning occurs by synchronous shear of the flux-line lattice around line pins which are too strong to be broken. The latter is referred to as the flux shear model and for this regime Kramer proposed [16]: 

![](images/tmpe13dtjpa.pdf-0004-09.png)

where C66 represents the elastic shear stiffness of the flux-line lattice, a0 is the flux-line spacing and[√] ρ represents the density of the pinning planes. In bulk Nb3Sn, the grain boundaries are the main pinning centers [73–77] and can thus be interpreted as the pinning planes yielding 1/[√] ρ = dav, the average grain size. 

One relation for the shear modulus of the flux-line lattice of a high field superconductor without paramagnetic limiting, was derived by Labusch [20]: 

![](images/tmpe13dtjpa.pdf-0004-12.png)

The flux-line spacing can be estimated by assuming a triangular flux-line lattice [68]: 

![](images/tmpe13dtjpa.pdf-0005-03.png)

Combining (2) with (3), assuming 1/[√] ρ = dav and a triangular flux-line lattice with a spacing as given by (4) results in: 

![](images/tmpe13dtjpa.pdf-0005-05.png)

Using the Kramer form therefore results in ν = 2.5 and γ = 2 in (1), if f (h) is defined as f (h) = h[0][.][5] (1 − h)[2] and (1 − a△(H)/dav) =[∼] 1, which will be validated below. Many authors indeed state ν = 2.5 [1,16,17,62,71,78]. 

Higher values for ν can be found if experimental results are described with nonKramer-like pinning. Deviating values for ν in (1) are reported by Kroeger et al. [70] who claim ν = 3.0 and by Cheggour and Hampshire [5] who state ν = 3.2. It should be noted that both studies neglect κ1 and fit the experimental results to Fp ∝ (1 − h)[3] and Fp ∝ (1 − h)[3][.][5] respectively. This choice suggests different pinning behavior. It will be explained below that such high values for the power above (1 − h) can arise when sample inhomogeneities are ignored. Here, they will be accounted for, which results in the experimentally supported assumption that Fp ∝ (1 − h)[2] , as will be discussed in more detail in Section 3.1. 

Combining (5) with the reverse definition of the Lorentz force gives (Suenaga and Welch in [79]): 

![](images/tmpe13dtjpa.pdf-0005-09.png)

In most technical wires dav is 100 to 200 nm, whereas the flux-line spacing decreases rapidly below 50 nm for magnetic fields above 1 T. Therefore a△(H)/dav ≪ 1 and Jc[0][.][5][(][µ][0][H][)][0][.][25][will][approximately][be][linear][in][H][and][can][be][referred][to][as][a][Kramer] function fK: 

![](images/tmpe13dtjpa.pdf-0005-11.png)

A linear extrapolation of (7) to Jc = 0 then yields Hc2 and the slope can be used to calculate κ1. The Kramer extrapolated critical field will be referred to as Hc2[K][to] distinguish it from a measured Hc2. 

The pinning force, as given by (5), peaks at h = 0.2 if a△(H) ≪ dav to yield the maximum pinning force: 

![](images/tmpe13dtjpa.pdf-0005-14.png)

2.1.2. Low field linearity of Kramer plots The dependence Fp ∝ (1 − h)[2] occurs when shear deformation of the flux-line lattice is the primary de-pinning mechanism as was mentioned above. This was shown experimentally by Cooley et al. [80] to be the case when the grain size is substantially larger than the flux-line spacing (dav > 2a△(H)). If the grain size is comparable to the flux-line spacing, a direct summation of individual pinning interactions between grain boundaries and flux-lines occurs, which corresponds to Fp ∝ (1−h) [20,22,80]. Plots of the Kramer function fK from (7) versus magnetic field (a ‘Kramer plot’), calculated from Jc data measured on Nb3Sn conductors, are generally linear in the ‘standard’ Jc measurement regime of about 0.2 < h < 0.6. This supports shearing of the flux-line lattice as the primary de-pinning mechanism, provided that the grain size is larger than about 100 nm [80]. Moreover, Kramer plots resulting from magnetization data on Powder-in-Tube processed wires, reacted at various temperature and time combinations, were shown to be perfectly straight down to h = 0.07 at various temperatures by Fischer [58]. Also transport Jc measurements on different bronze processed wires indicated straight Kramer plots at various temperatures down to h = 0.04 [10, 78]. Observed downward curvature when approaching lower magnetic fields can, apart from a different pinning behavior, additionally arise through self-fields generated by the large transport current densities. Accurate correction for these selfis non-trivial. 

These observations validate the application of (5) to very low fields and support the assumption that the (1 − a△/dav) term has negligible influence and can be approximated by (1 − a△/dav)[∼] = 1. Moreover, they indicate that for technical wires, which have an average grain size above 100 nm, shear deformation of the flux-line lattice apparently remains the primary de-pinning mechanism also below the maximum in Fp. The assumptions used to arrive at the Kramer model have received some criticism [21]. In practice, however, using the high magnetic field description of Kramer appears to hold for Nb3Sn wires, at least down to 1 T. 

2.1.3. Linearity of Kramer plots approaching Hc2 Above h[∼] = 0.8, non-linearities are mostly observed in Kramer plots of wire results when approaching the maximum Hc2 that is present in the wire. The pinning force function (5), combined with the approximation (1 − a△(H)/dav)[∼] = 1 is therefore often written in a more general form: 

![](images/tmpe13dtjpa.pdf-0006-05.png)

where C is a constant and p and q determine f (h). This allows for insertion of different values of p and q that implicate a different pinning behavior, but most probably originate from inhomogeneity averaging. Such different values for p and q lead to still ongoing discussion in the literature whether or not a general pinning mechanism, or f (h), can be assumed for Nb3Sn wires. 

The field dependence of the bulk pinning force as given by (9) is shown in figure 1 and combined with Kramer plots for various values of q around 2. A variation of p only influences the low field region. The aforementioned observations of perfectly straight 

![](images/tmpe13dtjpa.pdf-0007-01.png)

**----- Start of picture text -----**<br>
A general scaling relation for Nb3Sn<br>**----- End of picture text -----**<br>

Figure 1. Calculated changes with q in the field dependence of the bulk pinning force (left plot) and Kramer function (right plot). 

Kramer plots at lower magnetic fields for bronze and Powder-in-Tube processed wires, however, render strong deviations of p from 0.5 unlikely. 

A ± 25% variation in q results in a change in the maximum pinning force and its position and an up- or downward curvature in the Kramer plot for h → 1. The effect of a lowering of q, i.e. an increase of the maximum pinning force combined with a shift of its position towards higher magnetic field is identical to what has been observed experimentally through grain refinement in Powder-in-Tube wires by Cooley et al. [80]. Upward and downward tails in Kramer plots have both been observed experimentally (e.g. Ekin in [15], [60], Suenaga in [81], [82]) and have been attributed to microstructural [83] and compositional (Ekin in [15], [60], Cooley et al. [62], Suenaga and Welch in [79]) origins. A range of experimentally detectable Hc2 values could also be attributed to flux-creep and thermal activated flux-flow (e.g. the presence of an ‘irreversibility field’ in high temperature superconductors), but we find that these effects are negligibly small compared to the severe influence of compositional inhomogeneities on Hc2 [64], especially at temperatures below 20 K. 

The most convincing support for attributing curvature in Kramer plots when h → 1 to inhomogeneities is given by Cooley et al. [62], who numerically modeled the filaments in a Powder-in-Tube processed wire as concentric shells with different Sn content and thus different Hc2 and Tc. It was assumed that each composition behaves according to q = 2. An area weighted summation of the transport current density of such a system of parallel paths of variable property showed that a concave tail appears in the overall Kramer plots when the maximum available Hc2 is approached. Increasing the severity of the Sn gradient in the A15 sections increases the occurrence of such tails in otherwise linear overall Kramer plots. This parallel path model is supported by measurements on similar PIT processed wires [56,60]. Such an area weighted summation over parallel paths of lesser and better A15 quality results in a similar overall Kramer plot as for p = 0.5 and q = 2.5 in figure 1. A downward tail in Kramer plots, as is often observed in bronze processed wires, can be described with q < 2 as is shown in figure 1, thereby again implicitly assuming a different de-pinning mechanism. However, assuming a serial connection of lesser and better A15 quality regions for the more irregular filaments in bronze processed wires, also results in a downward tail in Kramer plots when h → 1, 

## A general scaling relation for Nb3Sn 

since the lower quality A15 sections will determine the overall transport properties. This argumentation is a strong indication that the curvature is not due to different de-pinning mechanisms but to inhomogeneity effects and thus that q should be 2. 

It can thus be stated that the Kramer flux-line shear model, at constant composition, is valid over nearly the full magnetic field range, i.e. up to Hc2 and down to a magnetic field where the flux-line lattice spacing becomes approximately more than half of the A15 grain size [80], which is below 1 T from (4). Non-linearities in Kramer plots when approaching the maximum present Hc2 are thus attributed to inhomogeneity averaging. The effective bulk values Hc2[∗][and][T] c[ ∗][,][as][detected][by][critical] current measurements, are weighted averages over the A15 volume, but it is not always clear how the averaging occurs. The discussion above leads to the conclusion that there is no a priori reason to deviate from Fp ∝ h[0][.][5] (1 − h)[2] , provided that the inevitable presence of A15 inhomogeneities in wires is recognized. 

## 2.2. Temperature dependence 

To come to an overall description for Jc(H, T, ǫ), the temperature dependence of the bulk pinning force is considered. In observing (9) it is clear that temperature dependence occurs through temperature dependence of Hc2 and κ1: 

![](images/tmpe13dtjpa.pdf-0008-06.png)

with h = H/Hc2(T ). It is thus required to discuss the available descriptions for Hc2(T ) and κ1(T ). For both parameters, empirical as well as microscopic alternatives are available. In the Summers relation [1] empirical forms are used. It will be shown here, how these can be replaced by alternatives with a better connection to the microscopic theory. 

2.2.1. Empirical temperature dependence First, the empirical temperature dependence of the upper critical field, as used in the Summers relation, is introduced. Based on earlier work by Suenaga in [81] and Hampshire et al. [78], Summers et al. [1] proposed an empirical relation for the temperature dependence of the upper critical field, thereby improving the correspondence between the available scaling relations and measured results: 

![](images/tmpe13dtjpa.pdf-0008-09.png)

where t = T/Tc. In this relation an empirical fit for κ1(T )/κ1(0) is inserted in κ1 = Hc2/([√] 2Hc) and Hc(t)/Hc(0) = (1 − t[2] ) is used for the temperature dependence of the thermodynamic critical field. It has to be emphasized that Hampshire et al. [78] claim a validity range only below 13.5 K for their calculated κ1(T ) values. 

2.2.2. Microscopic based Hc2(T ) An early microscopic description for the temperature dependence of the upper critical field was simultaneously derived in 1964 by Maki [28,29] and De Gennes [27,30] which, written in the De Gennes form yields the implicit relation (MDG relation): 

![](images/tmpe13dtjpa.pdf-0009-03.png)

The function uses only two parameters, namely Tc(0) (which can be measured) and the diffusion constant of the normal conducting electrons D. The diffusion constant is inversely proportional to the slope of the Hc2(T ) dependence at Tc(0) [56,60]. The other parameters are the reduced Planck constant (ℏ), the magnetic flux quantum (φ0) and the Boltzmann constant (kB). The terms ψ(x) represent the digamma function [84]. The description was derived assuming a dirty superconductor (i.e. ℓ ≪ ξ), it uses a spherical Fermi surface approximation and assumes a constant density of states at the Fermi level N(EF) and a weak electron-phonon interaction. Furthermore it assumes no paramagnetic limitation of Hc2(T ) and an absence of spin-orbit scattering. A normalized form of (12) with respect to temperature can be defined: 

![](images/tmpe13dtjpa.pdf-0009-05.png)

in which Hc2(t)MDG represents Hc2(T ) calculated using (12). 

It can be convenient for practical applications to avoid the need to solve the implicit MDG relation by replacing it with an explicit expression. An approximation of (12) for the entire temperature range yields: 

![](images/tmpe13dtjpa.pdf-0009-08.png)

This power of 1.52 is practically identical to the value of 1.5 which was found from a similar fit as (14) to (partly) extrapolated Hc2[∗][(][T][)][results][by][Cheggour][and] Hampshire [5]. A power of 1.5 was also found recently from analysis using Eliashberg theory by Oh and Kim [11]. 

Application of the full Eliashberg based formalisms is the most correct approach, since it accounts for all the electron-phonon interaction strengths. However, there are two reasons for applying only the simplest form of the microscopic descriptions [i.e. (12)] to wire results. First, since wires are inherently inhomogeneous there is no single Hc2(T ) but a distribution of properties [60]. Also, the inaccessibility of the normal state resistivity (which is a prime parameter in the microscopic theory) of the A15 in wires renders a proper connection to the theory practically impossible. Second, the use of the formal descriptions results in an increased number of parameters compared to (12). This can be avoided by implementing the additional parameters that are required for a proper connection to the microscopic theory in D [and thus in the slope at Tc(0) [60]] and Tc(0) in (12). To allow this it has to be assumed that the shape of Hc2(T ), at least to first order, remains unchanged. 

The simplest form of the microscopic descriptions, the MDG relation (12), was tested previously and found to fit Hc2(T ) for all available literature Nb3Sn results and 

measurements on a multitude of wires with very high accuracy [60]. This accuracy holds for the Orlando et al. thin film results [48] at all Sn concentrations, the Foner and McNiff single- and polycrystalline results [50,51], and the Jewell et al. bulk results [67]. The single crystals are close to stoichiometric and thus strong coupling [63] and most probably clean. The thin films and bulk samples are of varying degree of resistivity and Sn content and cover therefore a large range from approximately clean to dirty and weak to strong coupling. This leads to the conclusion that the shape of the fieldtemperature phase boundary is, within the experimental error bars, independent of the electron-phonon coupling strength (which can also be confirmed from the theory [40]), independent on whether the material is clean or dirty, and not influenced by the (unlikely [44, 48, 56, 85]) presence of PPL and spin-orbit scattering. It can thus be expected that it can be validated for the entire range of compositions that are present in wires. This is confirmed by the fact that it also holds for Kramer extrapolated, inhomogeneity averaged Hc2[K][(][T][)][results][[60].] 

2.2.3. Microscopic based κ1(T ) From the microscopic theory [41] it follows that for weak coupling superconductors in the dirty limit κ1(0)/κ1(Tc) = 1.2. In the strong coupling limit this ratio saturates at about 1.5 [41], which means that the maximum expectable change in κ1(T ) is 50% from 0 K to Tc. 

For calculation of κ1(T )/κ1(0) for a given interaction strength the nonlinear Eliashberg equations [13] will have to be solved as was done numerically by Rainer and Bergmann [41]. No general simple function for κ1(T )/κ1(0), derived directly from the electron-phonon spectrum and thus valid for all λep, can therefore be given for wires. Fortunately, a generalized function can be derived for κ1(T )/κ1(0) through κ1 = Hc2/([√] 2Hc), using the microscopic form for Hc2(T )/Hc2(0) (12) combined with the temperature dependence of Hc. 

It is well accepted that Hc(t)/Hc(0) is for all superconductors very close to (1 − t[2] ) [68]. Recent calculations based on Eliashberg theory yield Hc(t)/Hc(0) = (1 − t[2][.][17] ) [11]. The deviation from (1 − t[2] ) is measured for Nb3Sn [69] and is within about 2%. A fit to the measured Hc(t)/Hc(0) yields (1−t[2][.][07] ). For practical applications a power of 2 will thus be sufficiently accurate. Combining (12)/(13) or (14) with κ1 = Hc2/([√] 2Hc) and Hc(t)/Hc(0) = (1 − t[2] ) thus yields: 

![](images/tmpe13dtjpa.pdf-0010-06.png)

By implementing an accurate microscopic form for Hc2(T ) in the scaling relations also κ1(T ) is accurately known, rendering an empirical version redundant. 

## 2.3. Strain dependence 

2.3.1. Strain dependence in Nb3Sn wires When a Nb3Sn composite wire is subjected to longitudinal compressive strain, the critical current density, upper critical field and critical temperature reduce approximately linearly and reversibly with strain. When 

a wire is subjected to a longitudinal tensile strain, the critical parameters increase approximately proportionally and reversibly with strain until a parabolic-like peak is reached, after which the properties reduce approximately linearly with strain. The larger thermal contraction of the matrix materials compared to the thermal contraction of the Nb3Sn results in an axial pre-compression of the A15 when cooled from reaction temperature to the test temperature below 20 K. When the wire is axially loaded after cool-down, this pre-compression is minimized and Jc, Hc2 and Tc increase. The position of the maximum in the strain dependency curve appears at the point where the threedimensional deviatoric strain components in the A15 are minimal. In practice this correlates closely to the point where the axial pre-compression of the A15 is minimal. The axial pre-compression is mostly identified by ǫm, whereas the position of the minimum in the deviatoric strain components is identified as δ. Several models have been introduced in the literature to describe this behavior, ranging from polynomial fits to relations based on the Eliashberg theory. These will be discussed below. 

When an A15 lattice is deformed, its vibration modes will change. In addition, the electronic structure will be modified and therefore N(EF). It is thus reasonable to expect a strain induced variation of the electron-phonon interaction spectrum and the phonon density of states and hence, a change in the interaction constant λep. The difference between the strain sensitivity of Hc2 and Tc represents an important link to microscopic understanding since both depend differently on N(EF) and λep. It is found experimentally that [71,94]: 

![](images/tmpe13dtjpa.pdf-0011-04.png)

where the index ‘m’ indicates the values of Hc2 and Tc at the maximum of the axial strain dependency curve. The power ̟[∼] = 3, indicates that Hc2 is roughly 3 times more sensitive to strain than Tc. This was found to be valid at all temperatures (e.g. [3,4]). An attempt was made by Welch [94], following earlier work by Testardi [95–97], to explain the observed difference in strain sensitivity on the basis of the strong coupling renormalized BCS theory, using a McMillan [98] based, Allan and Dynes [99] strong coupling formulation for Tc. It was concluded that ̟[∼] = 3 cannot be explained by either a change in N(EF) or λep alone and the strain dependence should therefore be described by a combination of both. It should be pointed out, however, that McMillan based descriptions for Tc are valid for λep < 1.5 [100], whereas reported values for Nb3Sn are mostly higher [48]. It is clear, however, that improved understanding of the value for ̟ should result from exact calculations of strain induced modifications on the full electron-phonon interaction spectrum and the density of states. This might be possible through a combination of the recent efforts of Markiewicz [24–26] and Oh and Kim [11, 12]. An important conclusion drawn by Welch is that in a three-dimensional strain description the deviatoric strain components dominate the strain sensitivity of Nb3Sn and that hydrostatic components have, in comparison, a negligible effect. 

Most strain dependencies are defined through the strain dependence of the upper critical field or the critical temperature. Two general strain dependent terms will 

therefore be 

![](images/tmpe13dtjpa.pdf-0012-03.png)

under the assumption that s(ǫ) is independent of temperature and ̟[∼] = 3. 

2.3.2. Available models Five models describing the strain sensitivity of Nb3Sn can be distinguished throughout the literature. The simplest form is an introduction of hydrostatic strain though a pressure term. Although this yields a relatively simple connection to thermodynamic calculations to describe single crystal hydrostatic experiments, it is not suited for more practical systems such as wires due to the dominating deviatoric components. An empirical fit for axial deformations in wires was recently adapted by Hampshire and co-authors [6] in the form of a fourth-order polynomial. Although this will obviously result in accurate fits to experimental data, it lacks any connection to the underlying physics, and is thus not suited for the goals set out for this article. The three remaining models that have been proposed to describe experiments on wires will be discussed next in chronological order. 

The first model that was proposed to describe the strain dependence of the critical properties of Nb3Sn composite wires was the so-called power-law model, introduced by Ekin in 1980 [71]. The model was developed based on measurements using an axial pull strain device. The investigated compressive strain range was therefore limited to the thermal pre-compression of the A15, introduced by the matrix components of the wires. A power-law dependence was proposed for s(ǫ) using the extrapolated upper critical field [71]. In this power-law dependence, a different axial strain (ǫa) sensitivity is used for ǫa < 0 and for ǫa > 0. The power-law model is an empirical description that does not account for the three-dimensional nature of strain, but includes the generally observed asymmetry in axial strain experiments. Observable linearities at large compressive longitudinal strains are not accounted for and it is therefore valid over a limited strain regime. 

The second model that was proposed was the so-called deviatoric strain model. For high compressive strains Ten Haken found an approximate linear dependence of Hc2[K][on] axial strain, deviating from the power-law behavior [102, 103]. These deviations from the power-law model at large compressive axial strain values, combined with results of experiments on quasi two-dimensional Nb3Sn tape conductors [104–106] (which allow an analytical calculation of the three-dimensional strain components) led to an alternative description based on the non-hydrostatic, i.e. distortional or deviatoric strain [8,104]. In this deviatoric strain model only the second strain invariant is considered. The model is empirical, does account for the three-dimensional nature of strain and linearity at large compressive axial strains, but is symmetrical around the maximum in the strain dependency curve, and is claimed to be valid only for the compressive strain regime. 

The third model available in the literature is the so-called full invariant strain analysis [24–26]. This model is based on the assumption that the strain dependence of Tc results from the strain dependence of the phonon modes in the Nb3Sn crystal 

lattice. The model uses a full invariant strain analysis which correlates the strain dependence of Tc to strain induced changes in the phonon frequency spectrum using relations that stem from Eliashberg theory and a strain energy potential function. The main result of the full invariant model is that it is able to demonstrate the effect of the harmonic and anharmonic terms in the strain energy potential function independently. It explains how the Tc reduction due to hydrostatic strain decreases linearly with axial strain. It further explains the experimentally observed parabolic-like behavior around the maximum, the linearity for large compressive axial stain values and the asymmetry, in terms of the second and third strain invariants. For now, unfortunately, it does not include a description for Hc2[∗][(][ǫ][),][which][is][required][for][J][c][scaling.][The][latter][might][be] provided by a combination of recent promising work by Oh and Kim [11,12] and a full invariant analysis. 

2.3.3. Empirical correction to the deviatoric strain model The full invariant analysis is the most proper method available for the introduction of strain dependency of the critical properties. The resulting relations, however, remain somewhat complex compared to the empirical fits, and a complete description for Tc(ǫ) and Hc2[∗][(][ǫ][) is not fully developed] yet. It is clear that the empirical models all lack specific details in comparison to the full invariant analysis. An empirical model that accounts for three-dimensionality, linearity at large axial strain, and asymmetry, in agreement with the invariant analysis, can be obtained by assuming a simple mathematical correction to the Ten Haken deviatoric strain model [56]. Our starting point is relation (3) in [8]: 

![](images/tmpe13dtjpa.pdf-0013-04.png)

in which ǫdev represents the second deviatoric strain invariant, Cdev represents the slope in the linear regime of µ0Hc2[K][(][ǫ][dev][),][and][ǫ][0][,][d][represents][the][non-axial,][remaining][strain] components when the axial strain is zero. In axial form (18) can be written as [8,56]: 

![](images/tmpe13dtjpa.pdf-0013-06.png)

where Ca′[is a constant][and][ǫ][0][,][a][represents][the remaining strain][components,][as with][the] factor ǫ0,d in (18). To account, in the axial form of the Ten Haken model, for a stronger reduction at tensile strains, a linear term causing a reduction of Hc2[K][with][axial][strain][is] required. This can be achieved by including an additional linear term in (18): 

![](images/tmpe13dtjpa.pdf-0013-08.png)

where Cinv2 and Cinv3 are constants representing the second and third strain invariants. The term ǫ0,d now represents the initial suppression of Hc2[K][due][to][hydrostatic][strain.][A] similar route can be followed for the axial version (19), resulting in: 

![](images/tmpe13dtjpa.pdf-0013-10.png)

′ in which ǫa = ǫapplied + δ. The correction Ca2[ǫ][a][effectively][rotates][the][strain] dependency curve around its maximum. This causes the axial position of the maximum ′ ′ ′ to shift by a factor ǫsh = Ca2[ǫ][0][,][a][/][[(][C] a1[)][2][−][(][C] a2[)][2][]][0][.][5][.] For large asymmetry, δ (the axial strain at which the minimum in the deviatoric strain occurs) will then deviate significantly from the observable axial position of the maximum ǫm. In axial strain experiments it is more convenient to normalize the strain dependence function to the observable maximum, also to avoid the introduction of an additional parameter through the use of δ in combination with ǫm. The rotation around the maximum also causes the normalized form (17) to increase above 1 at the position of the maximum. This is undesirable since in scaling relations the reduction in e.g. Hc2[K][is][usually][normalized][to] the maximum observable value at the peak of the measured strain dependency curve, and not to the ‘strain free’ value since this is not accessible in an axial strain experiment. This can be prevented by re-normalizing s(ǫ) to the maximum observable critical field value. A re-normalization of s(ǫ) to the observable peak position and peak value in an axial strain experiment leads to a new axial form: 

![](images/tmpe13dtjpa.pdf-0014-03.png)

It has to be emphasized that this is an empirical correction to include the effects of the third strain invariant which, as suggested by the full invariant analysis, should be accounted for to describe asymmetry. It results in a simple description with three parameters (plus pre-strain) that accounts for the overall behavior as expected on the basis of a full invariant analysis and experimental observations. The hydrostatic strain components are included in the remaining strain term ǫ0,a and the strain induced behavior resulting from the second and third invariants is accounted for through Ca1 and Ca2 respectively. Relation (22) will be used through the remainder of this article since it is the simplest form that still accounts for the three-dimensional nature of strain and is based on an underlying physics model. Possible future, more fundamental based, strain descriptions can be easily implemented in the general scaling relation, since all strain dependence is included explicitly in s(ǫ) in terms of a change in Hc2 and/or Tc (17). 

## 2.4. Field, temperature and strain dependence of the bulk pinning force 

The strain dependence described above has to be included in the relation for the magnetic field and temperature dependent bulk pinning force (10) to arrive at a relation that can be used to inter- and extrapolate critical current measurements on wires. This 

requires the use of a strain dependent critical temperature as defined earlier by (17) and a temperature and strain dependent GL parameter and upper critical field: 

![](images/tmpe13dtjpa.pdf-0015-03.png)

Implementing this in the Kramer form of the field dependence of the bulk pinning force, i.e. (5), and assuming (1 − a△/dav)[∼] = 1 yields: 

![](images/tmpe13dtjpa.pdf-0015-05.png)

The upper critical field thus delivers a term s(ǫ)[2][.][5] acting directly on the bulk pinning force in addition to strain dependence arising through f (h) and Tc(ǫ). The strain dependence of κ1 is, however, undefined since this requires knowledge of the strain dependence of Hc which can differ from Hc2(ǫ). In addition, some strain dependence through strain induced changes of the flux-line to lattice interactions could be assumed. To arrive at an overall description, it is thus required to have knowledge of κ1(T, ǫ), and/or to introduce a strain dependent constant C(ǫ). 

2.4.1. Ekin’s unification of strain and temperature dependence In analyzing critical current versus strain data at 4.2 K Ekin [71] found that the bulk pinning force scales, in analogy to the Fietz and Webb scaling law (1), as: 

![](images/tmpe13dtjpa.pdf-0015-08.png)

where n = 1.0 ± 0.3 and the star again indicates a bulk average. The power of 1 differs from the power of 2.5 that is required for magnetic field and temperature scaling, as seen from (10). Ekin solved this inconsistency by postulating a combination in terms of explicit dependencies on temperature and strain. Neglecting the temperature and strain dependence of κ1 he proposed: 

![](images/tmpe13dtjpa.pdf-0015-10.png)

where h = H/Hc2[∗][(][T, ǫ][),][t][=][T/T] c[ ∗][(][ǫ][)][(stars][indicating][bulk][average][values),][n][∼][=][1,] ν[∼] = 2.5. Note that the third term only describes the normalized temperature dependence of the upper critical field approximated as (1−t[2] ), in which strain sensitivity occurs only through Tc[∗][(][ǫ][).][The][combination][of][strain][and][temperature][sensitivity][was][introduced] on a fully empirical basis, based on 4.2 K critical current data. This implicates, as was pointed out by Ekin, that the term C/κ1(T, ǫ)[2] in (24) has to produce a strain dependency s(ǫ)[1][.][5] to counteract the s(ǫ)[2][.][5] term arising through the strain dependent upper critical field in (24). A similar magnetic field, temperature and strain dependence is used in various forms of generalized scaling relations which, by combining (26) with Fp = −J × B, result in an overall description for the critical current density in Nb3Sn wires. 

2.4.2. Unification of the Kramer form The ratio [µ0Hc2(T, ǫ)][2][.][5] /κ1(T, ǫ)[2] in (24) can be normalized to zero temperature to express the direct strain influence on Fp (i.e. not through Tc(ǫ)) separately, so that the result only contains temperature dependence and strain dependence through Tc(ǫ). With the definitions: 

![](images/tmpe13dtjpa.pdf-0016-03.png)

![](images/tmpe13dtjpa.pdf-0016-04.png)

this leads to: 

![](images/tmpe13dtjpa.pdf-0016-06.png)

To retain consistency with Ekin’s observation that Fp(ǫ)4.2 K ∝ s(ǫ) (under the assumption that this is valid for all temperatures) it can for example be postulated that: 

![](images/tmpe13dtjpa.pdf-0016-08.png)

leading to: 

![](images/tmpe13dtjpa.pdf-0016-10.png)

Alternatively, one can define a strain dependent pre-constant C(ǫ) as will be shown below. The temperature dependencies in (27) can be empirical (e.g. (11)) or microscopic based alternatives (e.g. (12) and (15)). The discussion above is used in the scaling relations that are available throughout the literature. 

2.4.3. The Summers relation Summers et al. [1], following previous work by Hampshire et al. [78] and Ekin [71], using ǫ = ǫa, defined a strain dependent preconstant: 

![](images/tmpe13dtjpa.pdf-0016-13.png)

The power of 0.5 is introduced in (32) to retain consistency with the strain dependence of the bulk pinning force as postulated by Ekin (26). It can be shown that the Summers relation can be rewritten in a form consistent with the previous Section as: 

![](images/tmpe13dtjpa.pdf-0016-15.png)

in which the empirical temperature dependence (11) is used for b(T, Tc(ǫ)) and k(T, Tc(ǫ)). The Summers relation is thus, apart from the pre-constant, consistent 

with (31). It has finally to be quoted that Hampshire et al. stated [78], in relation to substantial inhomogeneity of their samples, that the validity of their calculated κ1(T ) results is expected to break down for T > 13.5 K. It will be shown below that this, through comparison of the Summers form (11) to the microscopic based form (15) and measured results, indeed appears to be the case. 

2.4.4. Alternative approaches The empirical bases in the relations proposed by Ekin and Summers et al., their inaccuracy, and the extensive new Jc(H, T, ǫ) data sets for wires that have become available over the past decade have evoked a re-analysis of overall scaling behavior in Nb3Sn wires. Two alternative approaches can be distinguished, focusing either on improving the strain and temperature dependent terms [4, 9], or focusing on improving the basis of the strain dependence of C/κ1(T, ǫ)[2] in (24) [5–7]. In the first approach it is stated that, since the strain dependence through the power-law function does not account for linearity at high compressive strains, it should be replaced by a function that does. This was done through a change in s(ǫ) from the power-law form to the Ten Haken form. Secondly, it was assumed that (31), and thereby the Summers version, is valid but that the empirical temperature dependencies as proposed by Summers et al. [i.e. (11)] are in error and can be improved upon. The general form (10) was chosen in [4, 9] under the condition that s(ǫ) from (17) is independent of temperature, (16) has general validity and (1 − a△(H)/dav)[∼] = 1. 

The temperature dependence in (10) is determined by the ratio [µ0Hc2(T )][ν] /κ1(T )[γ] . Four-dimensional parameter least squares fits using extensive data sets on a six different wires and highly linear Kramer plots indicated n[∼] = 1 (as stated by Ekin), p =[∼] 0.5 and q[∼] = 2 (as stated by Kramer for h > 0.2). Since the temperature dependencies of Hc2 and κ1 were fully empirical in the Summers form, both powers ν and γ were regarded as free parameters to allow for errors in the temperature dependencies. Overall least squares fits on the data sets indicated that ν[∼] = 2 and γ[∼] = 1 yielded the highest accuracy. The overall description (10) with p = 0.5, q = 2, ν = 2 and γ = 1 yielded fits to experimental data with a standard deviation of about 2% over a limited magnetic field range from 5 to 13 T, but for all temperatures (4.2 K to Tc) and all investigated compressive strains (−0.7 < ǫa < 0) [2]. It was expected that if correct dependencies for Hc2(T ) and κ1(T ) were used, that similar accurate fits would be obtained with values for ν and γ, which are consistent with Kramer’s pinning theory, i.e. ν = 2.5 and γ = 2. However, in Section 3, we will re-analyze one of these earlier data-sets with the recent new insights on inhomogeneity averaging effects and the now known temperature dependencies Hc2(T ) and κ1(T ), and show that the deviating values ν = 2 and γ = 1 are correct. 

The second approach to improve upon the Summers relation emphasizes on the different dependencies of the bulk pinning force on temperature and strain in an attempt to define a better founded combination of both dependencies. Following initial work by Kroeger et al. [70] this results in a general relation of the form [5–7]: Fp (H, T, ǫ) = A (ǫ) [µ0Hc2[∗][(][T, ǫ][)]][n][ h][p][ (1][ −][h][)][q][ ,] (34) 

in which n, p and q are free parameters and A(ǫ) is a function of strain alone. Several versions for A(ǫ) have been proposed [also including κ1(T, ǫ)] in attempts to describe strain induced modifications of the flux-line to pinning center interactions and the strain dependence of κ1. 

2.4.5. Selected general scaling relation In general it can be stated that much of the developments on overall scaling behavior remains empirical and it is unlikely that this empirical basis can be fully removed. As a final remark it should be mentioned that in a four-dimensional description with a large number of free parameters it often remains a somewhat subjective choice which parameters are fixed or allowed to vary, in addition to the choice of relationships that can be implemented. 

The overall scaling law that is proposed in this article will now be summarized. It is assumed that the critical current density scales according to (24) in the most general form: 

![](images/tmpe13dtjpa.pdf-0018-05.png)

where h = H/Hc2[∗][(][T, ǫ][),][in][which][H] c2[∗][represents][the][inhomogeneity][(bulk)][averaged] critical field at which the critical current density extrapolates to zero. The microscopic based temperature dependencies are selected for the upper critical field (13) and the GL parameter (15). This leads to the general normalized form: 

![](images/tmpe13dtjpa.pdf-0018-07.png)

where t = T/Tc[∗][(][ǫ][).][The][term][s][(][ǫ][)][ν][−][αγ][arises][from][the][strain][dependence][of][the][upper] critical field through (17) and an unknown strain dependence of the zero temperature GL parameter, defined as: 

![](images/tmpe13dtjpa.pdf-0018-09.png)

The form for s(ǫ) is chosen to be the improved deviatoric strain model (22). 

The temperature and strain dependent bulk average critical field in (36) is given by a combination of the microscopic temperature dependence (13) and the strain dependence (23): 

![](images/tmpe13dtjpa.pdf-0018-12.png)

and the strain dependence of the critical temperature is defined by (17). 

The constants p, q, ν, γ and α will have to be determined through systematic comparison to experiments, and ̟ = 3 is used in accordance with the experimental results of Ekin. Note that this approach significantly differs from the usual separation between the dependence of the bulk pinning force on Hc2[∗][(][T][)][and][H] c2[∗][(][ǫ][).][Here][this] is not assumed a priori and strain dependency is simply introduced through a strain dependent upper critical field and GL parameter. This relation will be compared to measurements in Section 3 to determine the constants and to test its validity. 

## 3. Comparison to measurements 

In this Section we will compare the general Jc(H, T, ǫ) relation (36) to earlier experimental data. Experimental details, as well as the existing data-set were described elsewhere [4, 10, 107]. The selected data-set for the renewed analysis are Jc(H, T, ǫ) results which were measured on an International Thermonuclear Experimental Reactor (ITER) type, Furukawa bronze processed wire. A more detailed description of this wire is also given elsewhere [60]. The results of this wire are selected because of the demonstrated high reproducibility, and since it was analyzed extensively in various laboratories around the world. It should be emphasized that the results for this wire are not unique, but representative for the scaling behavior for at least five other wires from various manufacturers [4,9]. Jc(H, T ) results were obtained on an ITER-type Ti-6Al-4V barrel at electric field criteria of Ec = 10[−][5] to 5 × 10[−][4] V/m. Jc(H, T, ǫ) results were obtained on a Ti-6Al-4V U-shaped bending spring at Ec = 5 × 10[−][4] V/m and on a Ti-6Al-4V circular bending spring (‘Pacman’) at Ec = 10[−][4] V/m. The ITER barrel and U-shaped bending spring samples were heat treated together, whereas the Pacman sample was heat treated separately. All data are corrected for resistive currents that run parallel to the superconductor at any voltage criterion and the self-field generated by the wire is also corrected for. These details can be found elsewhere [56]. 

First the field dependence will be analyzed in detail. This results in the values for p and q in (36), Hc2[∗][(][T][)][and][F][p max][(][T][).][Then][the][temperature][dependence][will][be] analyzed in detail and it will be shown that the Kramer/Summers form fails to describe the temperature dependence by the use of ν = 2.5 and γ = 2 in (36). The use of these constants results in a temperature dependent variation of κ1 that is significantly larger than can be expected from the microscopic theory. Next the improved temperature dependence, through the use of different values for ν and γ, will be introduced and validated. This is followed by an analysis of the strain dependence using the improved deviatoric strain model. By using correct values for ν and γ, it is not required to separate the temperature and strain dependence of the bulk pinning force. Also the strain dependence of Fp max is determined from the measurements. Finally, the minimum required data-set to determine the critical surface of an unknown wire will be discussed. 

## 3.1. Normalized bulk pinning force 

To investigate the magnetic field dependence of the bulk pinning force, each combination of temperature and strain was attributed to a unique but unknown effective upper critical field Hc2[∗][(][T, ǫ][)][and][maximum][bulk][pinning][force][F][p max][(][T, ǫ][).][The][bulk][pinning] forces were calculated from the measured critical current densities through Fp(H, T, ǫ) = |Jc(H, T, ǫ)µ0H|. Kramer plots are linear for this wire as will be shown below, indicating q = 2 and p = 0.5 as was shown in Section 2.1. To analyze consistency with these values in (9) for all temperatures and strains, a least squares fit was made to 

![Figure 2. Reduced bulk pinning force as function of reduced magnetic field for Jc(H, T ) measurements at Ec = 10[−][5] V/m (left graph) and Jc(H, T, ǫ) measurements at Ec = 5 × 10[−][4] V/m (right graph).](images/tmpe13dtjpa.pdf-0020-02.png)

Fp(H, T, ǫ)/Fp max(T, ǫ) in: 

![](images/tmpe13dtjpa.pdf-0020-05.png)

where h = H/Hc2[∗][(][T, ǫ][).][The][resulting][normalized][bulk][pinning][force][dependencies][on] reduced field are shown in figure 2. 

The left graph shows the dependence for the Jc(H, T ) measurements at all temperatures (and constant strain). The right graph shows the reduced dependencies for the Jc(H, T, ǫ) for all temperature and strain values. The fit values for Hc2[∗][(][T][)] and Fp max(T ) for the Jc(H, T ) measurements are summarized in figure 3, including a calculated dependence for Hc2[∗][(][T][)][using][the][Maki-De][Gennes][relation][(12)][with] µ0Hc2[∗][(0)][=][30][.][1][T][and][T] c[ ∗][(0)][=][16][.][7][K.][It][should][be][noted][that][these][are][at][−][0][.][15%] axial pre-compression, as will be shown in Section 4. The high value for Hc2[∗][(0)][in] comparison to a measured maximum detectable value µ0Hc2(0) = 29.3 T [60] can be explained by inhomogeneities causing a downward tail in Kramer plots thereby resulting in an overestimate of the extrapolated Hc2[∗][(0).][It][should][be][emphasized][that][this][high] value is required to accurately describe the measurements in the range h < 0.8. 

The bulk pinning force curves in figure 2 demonstrate that p = 0.5 and q = 2 indeed yield the correct magnetic field dependence for the entire investigated temperature and strain regime. Above h[∼] = 0.8 deviations can occur, but these are attributed to inhomogeneities. It should be emphasized that the observed correspondence with p = 0.5 and q = 2 is not specific for this wire, but holds for all our earlier investigated sample materials and also for ‘normally’ reacted PIT wires as demonstrated by Cooley et al. [80]. Note also that the regime above h = 0.8 can be accounted for in the fit by using deviating values for p and q. This will obviously lead to a different value for the scaling field Hc2[∗][and][scaling,][as][demonstrated][by][a][normalized][pinning][function,] 

![Figure 3. Temperature dependence of the effective upper critical field and maximum bulk pinning force as measured on the ITER barrel at Ec = 10[−][5] V/m.](images/tmpe13dtjpa.pdf-0021-02.png)

is still possible as was shown by similar analysis on the same wire by Hampshire and co-authors [108]. This will improve the accuracy of the fit above h = 0.8 at the cost of generality of the model. However, since this regime involves very low current densities that are of negligible importance to the applications, we choose to retain a general model at the cost of low current density fit accuracy. 

It is thus concluded that the field dependence is accurately described by p = 0.5 and q = 2 for all magnetic fields in the range 0.05 < h < 0.8 for all temperatures and strains. It is also observed that the Maki-De Gennes relation indeed yields an accurate description for the temperature dependence of the effective upper critical field resulting from transport critical current measurements. 

## 3.2. Temperature dependence 

The temperature dependence of the bulk pinning force can now be analyzed. The temperature dependencies for the upper critical field and the GL parameter are known. This means that only the temperature dependence of the maximum bulk pinning force has to be investigated to determine the overall temperature dependence of the bulk pinning force. The temperature dependence of the maximum bulk pinning force is determined by the values for ν and γ in (36). 

3.2.1. Incorrect temperature dependence of the Kramer/Summers form In the Kramer/Summers form ν = 2.5 and γ = 2 in (36) and (35), leading to: 

![](images/tmpe13dtjpa.pdf-0021-09.png)

![](images/tmpe13dtjpa.pdf-0021-10.png)

![](images/tmpe13dtjpa.pdf-0021-11.png)

![](images/tmpe13dtjpa.pdf-0022-02.png)

**----- Start of picture text -----**<br>
Figure 4. Temperature dependence of the GL parameter and maximum bulk pinning<br>force at Ec = 10 [−][5] V/m. The points are derived from the Jc(H, T ) characterizations<br>and the lines are the calculated dependencies using (15) (MDG) and (41). For<br>completeness, also the Summers empirical form for the GL parameter (11) is included.<br>**----- End of picture text -----**<br>

![](images/tmpe13dtjpa.pdf-0022-03.png)

There is unfortunately no direct way to extract either C or κ1(0) separately from the Jc(H, T ) results. Comparison to the measurements delivers C1, Hc2[∗][(0),][T] c[ ∗][(0),][H] c2[∗][(][T][)] and Fp max(T ) without free parameters, but κ1(0) depends on the value of C. Note that C is not a fundamental constant here because Fp is evaluated from the non-copper cross-section. 

An overall least squares fit of (40) on the measured Jc(H, T ) data, using µ0Hc2[∗][(0) =] 30.1 T and Tc[∗][(0) = 16][.][7][K,][results][in][C][1][= 42][.][8][ ×][ 10][9][AT][/][m][2][.][The][resulting][maximum] bulk pinning force according to (41) is shown in comparison to the actual data in figure 4. Significant deviations occur above 9 K, which will also be present in calculated critical current densities. 

The deviations in Fp max(T ) can be illustrated through the resulting change in κ1 with temperature. The variation in κ1 with temperature, according to the Kramer/Summers form, can be calculated through (41) by using values for Fp max(T ) and Hc2[∗][(][T][)][from][figure][3,][and][by][inserting][a][value][for][κ][1][(0).] Choosing C = 12.8 × 10[9] AT[1][.][5] m[2] as proposed by Kramer (5), results through (40) in κ1(0) = 38.6; a reasonable value compared to the literature [69]. The resulting values for κ1(T ), calculated from Fp max(T ) and Hc2[∗][(][T][)][using][(41)][are][plotted][in][figure][4,][together][with] the microscopic (15) and empirical (11) dependencies. 

The change of κ1(T ) of nearly 100% is unrealistic, since a maximum change of 20% is expected in the weak, and 50% in the strong coupling limit as discussed in Section 2.2. This is independent of the choice of C and thus κ1(0), since the calculations are normalized to κ1(0). The combination of ν = 2.5 and γ = 2 therefore results in an 

![Figure 5. Kramer plot of measured Jc(H, T ) data, including linear fits according to (7) and the overall Jc(H, T ) fit according to (40) at Ec = 10[−][5] V/m. The graph emphasizes the failure of the Kramer/Summers model to account for the correct slope at higher temperatures, which leads to significant deviations in the calculated Jc(H, T ) values.](images/tmpe13dtjpa.pdf-0023-02.png)

unrealistically large change in κ1(T ), calculated from Fp max(T ) and Hc2[∗][(][T][).] 

The Kramer function is given by (7) and the slope is therefore C/κ1(T ). The large change in κ1 with temperature thus translates to a larger change in the slope of a Kramer plot at higher temperatures. This is visualized by the Kramer plot given in figure 5. 

The overall Jc(H, T ) least squares fit is optimized at 4.2 K in this graph, to emphasize the deviations that occur at higher temperatures. The error in the overall temperature dependence in the Kramer/Summers model, through the use of ν = 2.5 and γ = 2, causes significant deviations in the slope of a Kramer plot at higher temperatures and thus in large errors in the calculated Jc(H, T ) values. 

Deviations in the Kramer fit were observed also in our earlier analysis [109, 110] and were attributed to incorrect (empirical) temperature dependencies of the effective upper critical field and the GL parameter. Now that Hc2[∗][(][T][)][and][κ][1][(][T][)][are][replaced] by microscopic based alternatives, it has to be concluded that the observable errors in Fp max(T ) stem from incorrect values for ν and γ. This is supported by the unrealistic large change in the calculated κ1 with temperature, surpassing the strong coupling limit. 

3.2.2. Improved temperature dependence In the above analysis it became clear that the temperature dependence of the bulk pinning force using ν = 2.5 and γ = 2 is incorrect. It is therefore required to determine the optimal values for both constants that yield the highest accuracy for the calculation of the temperature dependence of the maximum bulk pinning force. The Fp max(T ) data are, in the general form, described by: Fp max (T )[∼] = 0.286C[[][µ][0] κ[H] 1 (c2[∗] T[(] )[T][γ][)]][ν] 

![Figure 6. Combinations of ν and γ and the overall least squares fit error in the maximum bulk pinning force.](images/tmpe13dtjpa.pdf-0024-02.png)

![](images/tmpe13dtjpa.pdf-0024-04.png)

Relation (42) is fitted against the Fp max(T ) data from Section 3.1. Values of ν are chosen around 2.5 and the value for γ is least squares fitted. Various combinations of ν and γ are able to describe the measured Fp max(T ), each with a specific remaining overall least squares error, as plotted in figure 6. The possible combinations of ν and γ are related by γ = 0.880ν − 0.756. The overall error shows a distinct minimum of nearly zero for the combination ν = 2 and γ = 1 and these values therefore yield optimum accuracy for the temperature dependence of the maximum bulk pining force. Relation (42), using ν = 2 and γ = 1 is plotted together with the Fp max(T ) data from Section 3.1 in figure 7. The accuracy in the calculated Fp max(T ) is significantly improved compared to the use of ν = 2.5 and γ = 2 in figure 4. 

The temperature dependence of the GL parameter, resulting from Fp max(T ) and Hc2[∗][(][T][) using (42) with][ν][= 2 and][ γ][= 1 can also be calculated.][The relation between][C] and κ1(0) now differs from the Kramer form (5). The value for κ1(0) is chosen consistent with the previous analysis, i.e. κ1(0) = 38.6, leading to C = 1.81 × 10[9] AT[1][.][5] m[2] . This calculation yields a κ1(T ) as plotted in figure 7. The GL parameter now changes by about 35% which is in agreement with expectations (i.e. between 20 and 50%, see Section 2.2.3) and, moreover, follows the microscopic based description. The overall accuracy of the temperature dependence can again also be demonstrated using a Kramer plot. Using ν = 2 and γ = 1 in (36) results in an overall description: 

![](images/tmpe13dtjpa.pdf-0024-07.png)

![](images/tmpe13dtjpa.pdf-0025-02.png)

**----- Start of picture text -----**<br>
Figure 7. Improved temperature dependence of the GL parameter and maximum<br>bulk pinning force at Ec = 10 [−][5] V/m. The points are derived from Jc(H, T )<br>characterizations and the lines are the calculated dependencies using (15) (MDG) and<br>(42) with ν = 2 and γ = 1. For completeness, also the Summers empirical form for<br>the GL parameter (11) is included.<br>**----- End of picture text -----**<br>

and the linear Kramer function becomes: 

![](images/tmpe13dtjpa.pdf-0025-04.png)

Similar analysis as in the previous Section yields from the overall Jc(H, T ) least squares fit C1 = 42.6×10[9] AT/m[2] . The small difference in C1 compared to the Kramer/Summers form (42.8 × 10[9] AT/m[2] ) stems from the fact that in figure 5 the fit was optimized for the 4.2 K results, whereas now the fit is optimized over the entire temperature range. The improved functionality yields slopes that are consistent with the measured results over the entire temperature range as is seen in figure 8. The only significant deviations occur close to Hc2[∗][(][T][),][the][regime][where][non-linearities][in][Kramer][plots][originate][from] A15 inhomogeneities. 

## 3.3. Strain dependence 

Now that the magnetic field and temperature dependence are established, the strain dependence is introduced by stating that the effective upper critical field, the critical temperature and the GL parameter depend on strain. This leads through (35) to: 

![](images/tmpe13dtjpa.pdf-0025-08.png)

where Hc2[∗][(][T, ǫ][)][≡][H] c2m[∗][(][T][)][s][(][ǫ][),][T] c[ ∗][(][ǫ][)][≡][T] cm[ ∗][s][(][ǫ][)][1][/̟][and][κ][1][(][T, ǫ][)][≡][κ][1m][(][T][)][s][(][ǫ][)][α][.][It][is] assumed that ̟ = 3 since this was shown earlier to be consistent with measurements, and α has to be determined from experiment. In normalized form (45) becomes [through (36)]: 

![](images/tmpe13dtjpa.pdf-0025-10.png)

![Figure 8. Kramer plot of measured Jc(H, T ) data at Ec = 10[−][5] V/m, including linear fits according to (44) and the overall Jc(H, T ) fit according to (43). The improved overall temperature dependence using ν = 2 and γ = 1 results in an accurate description across the entire temperature range.](images/tmpe13dtjpa.pdf-0026-02.png)

where C1 = C[µ0Hc2m[∗][(0)]][2][/κ][1m][(0).] 

First the function for s(ǫ) will be determined. It will initially be assumed that α = 1, since this is consistent with Ekin’s [71] statement that Fp max(4.2 K) ∝ Hc2[∗][(][ǫ][),] as well as our earlier analysis. This choice for α has to be confirmed with experimental results. The improved and re-normalized deviatoric strain model is chosen as description for s(ǫ), i.e. relation (22). An accurate Jc(H, T, ǫ) measurement with a high strain resolution is required to determine the parameters in (22), i.e. Ca1, Ca2, ǫ0,a and ǫm. The mechanical parameters are therefore determined from a measurement on the Furukawa wire at 12 T and 4.2 K, which are measured with the required strain resolution [107], as shown in figure 9. The points are the Jc(ǫ) results at 12 T and 4.2 K at a criterion of Ec = 10[−][4] V/m. The line is calculated from (46) combined with (22) using the mechanical parameters depicted in the graph, α = 1, C1 = 47.8 kAT/mm[2] , µ0Hc2m[∗][(0) = 30][.][7][T][and][T] cm[ ∗][(0) = 16][.][8][K.] 

It should be emphasized that C1, Hc2m[∗][(0)][and][T] cm[ ∗][(0)][are][solely][used][as][fit] parameters to scale Jc. Since no field or temperature dependent measurements were performed on this specific sample they are arbitrary, but not unique, parameters resulting from a least squares fit of the 12 T, 4.2 K data points. As mentioned this sample was not heat treated together with the U-spring and barrel samples, rendering differences of a few percent in C1, Hc2m[∗][(0) and][ T] cm[ ∗][(0) possible.][In addition,][the applied] criterion of Ec = 10[−][4] V/m is higher than used for the Jc(H, T ) characterizations (Ec = 10[−][5] V/m), translating to slightly higher values for the fit parameters, since effectively Sn richer A15 sections will be probed. 

Figure 9 shows that the improved deviatoric strain model does accurately account for the measured behavior. In contrast to the original deviatoric strain model, it is able 

![Figure 9. Axial strain dependence of the critical current density at Ec = 10[−][4] V/m, 12 T and 4.2 K measured on a circular bending spring and calculated from (46) and (22) using parameters as depicted in the graph.](images/tmpe13dtjpa.pdf-0027-02.png)

to fit the entire strain curve and not just the compressive part. Note that the term Ca2 effectively tilts the calculated curve around Hc2m[∗][(][T][)][at][ǫ][a][=][0.][This][causes][the] fit values for Ca1 and ǫ0,a to change compared to the earlier model. Overall, however, (22) accurately describes the strain dependence and α = 1 in (46) appears to yield the correct strain dependence of the bulk pinning force. 

Now that s(ǫ) is confirmed to be accurate, Fp max(ǫ) ∝ s(ǫ)[2][−][α] has to be investigated to find the value for α from experiment, which can be done using earlier U-spring results. Note that experimental limitations of the U-spring only allow for a relatively high criterion of Ec = 5 × 10[−][4] V/m to be considered reliably [107]. The power 2 − α is determined by plotting the Fp max(ǫ) values from Section 3.1 versus axial strain and comparing to s(ǫ)[2][−][α] . This is demonstrated in figure 10 for 4.2 K results, yielding α = 1.0 ± 0.1, in agreement with Ekin’s result. Similar analyses for higher temperatures suggest that α might decrease with temperature. At higher temperatures, however, the Fp max(ǫ) analyses become significantly less accurate since they are based on much smaller current densities and limited data. Also inhomogeneity effects, which manifest themselves in the investigated magnetic field range at higher temperatures, complicate a more precise determination of 2−α. The results are therefore not sufficiently accurate to come to unambiguous conclusions on a possible temperature dependence of α. Moreover, strain dependency results are, for now, only available for inhomogeneous samples, rendering further speculations not very useful. With the available experimental results it can be assumed that α[∼] = 1 for all temperatures. 

It is concluded that strain dependence can be introduced in the bulk pinning force using a single dependence Fp max ∝ Hc2[∗][(][T, ǫ][)][2][, provided that][ α][ ∼][= 1 for all temperatures.] This is in contrast to the usual conclusion that Hc2[∗][(][T][)][and][H] c2[∗][(][ǫ][)][have][different] dependencies. This single function is enabled through the use of values for ν and γ that accurately agree with measured results and by including the strain dependence of 

![Figure 10. Maximum bulk pinning force as function of applied axial strain at Ec = 5 × 10[−][4] V/m and 4.2 K, measured on the U-spring.](images/tmpe13dtjpa.pdf-0028-02.png)

the GL parameter. Figure 10 implies that κ1 has a similar strain dependence as Hc2[∗][.] 

## 4. Scaling of measured results 

In the previous Sections an overall scaling function for Fp(H, T, ǫ) was postulated and confirmed by systematic analysis of the separate dependencies on magnetic field, temperature and strain. The proposed function is given by (46), with α[∼] = 1. Solving the implicit Maki-De Gennes relation can be avoided by using its approximation MDG(t) =[∼] (1 − t[1][.][52] ) which is sufficiently accurate for practical applications. Using this approximation changes the overall function to the simple form: 

![](images/tmpe13dtjpa.pdf-0028-07.png)

in which s(ǫ) is given by (22). The superconducting parameters C1, Hc2m[∗][(0) and][ T] cm[ ∗][(0)] and the deformation related parameters Ca1, Ca2, ǫ0,a and ǫm have to be determined experimentally. 

The new scaling relation can be applied to the entire existing Furukawa wire Jc(H, T, ǫ) data-set at Ec = 5 × 10[−][4] V/m which results in the mechanical and superconducting parameters given in table 1. The axial thermal pre-compression (ǫm) of 

Table 1. Parameters for the calculation of Jc(H, T, ǫ) at Ec = 5 × 10[−][4] V/m. 

Table 2. Axial thermal pre-compression in percent at T = 4.2 K for a Furukawa wire mounted on an experimental setup. 

the A15 volumes in the Furukawa wire when mounted on the specific experimental setups are given in table 2. These axial pre-compression values are low compared to a wire that is not mounted on a substrate (for which the pre-compression usually is between −0.2 and −0.4%). This is a result of the low thermal contraction of the substrate material (Ti-6Al-4V) which determines the overall thermal contraction after wire mounting and which matches the thermal contraction of Nb3Sn. Differences between the thermal precompression on the ITER barrel and the strain devices are attributed to the differences in mounting temperature of the wire (epoxy hardening at room temperature for the ITER barrel versus soldering at about 200[◦] C for the strain devices). 

## 5. Discussion 

## 5.1. Scaling accuracy 

Through systematic comparison with measured results deficiencies in existing scaling relations can be highlighted. Improvements can, however, only be made empirically through a change of the bulk pinning force dependency on both Hc2[∗][(][T][)][and][κ][1][(][T][)] simultaneously. The resulting relation describes the measurements accurately (also for a multitude of other wires) [4, 9]. The values ν = 2 and γ = 1 are similar to those found earlier [4,9,10] through minimization of the error in the overall Jc(H, T, ǫ) least squares fit. In the earlier analysis it was assumed that the deviating values for ν and γ originated from a wrong temperature dependence of Hc2 and κ1. It is now concluded that the Kramer form, which results from the Labusch [20] function for C66, is in fact not accurate. These theories have been questioned in the literature, specifically by Brandt [21] and Dew-Hughes [17], emphasizing the difficulties in understanding and modeling the flux-line to pinning site interactions. A reasonable temperature dependence description can be achieved for the combinations γ = 0.880ν − 0.756, but the overall error shows a distinct minimum at ν = 2 and γ = 1. For a proper connection to theory these values should result from a fundamental form of these interactions. At present, to our knowledge, such a model is not available. 

The validity of the new scaling relation was tested on a database derived from four samples, one of which was heat treated separately. The samples were characterized in three experimental setups. Deriving a singular parameter set for the Furukawa wire is complicated by small differences between the samples and characterization methods. A better fit to the U-spring strain results alone can, for example, be found by the use of slightly different parameters. This stems from small, for now unclear, differences between the separate samples and experiments. Ideally all measurements should be performed on a single instrument and on a single wire and at one single, low criterion. The latter is preferred to remove inaccuracies arising from parasitic current subtraction and for consistency with the more standard criterion of Ec = 10[−][5] V/m. Nevertheless, the accuracy of a very similar function (using the earlier deviatoric strain model) was investigated extensively in previous work and it was concluded that a standard deviation below 2% can be obtained [2]. The applicability of the proposed scaling function was validated for Internal-Tin wires during the ITER benchmark tests in our earlier work [9], and in unpublished analysis of Powder-in-Tube wires. 

## 5.2. Minimum required dataset 

With a scaling relation available the question arises as to what is the minimum data-set that is needed to retrieve the entire critical surface. For the temperature dependence two Hc2[∗][(][T][)][points][are][required][to][determine][the][entire][H] c2[∗][(][T][)][dependence][through][the] MDG relation. These should be determined by transport Jc measurements since these yield the correct Hc2[∗][and][ T] c[ ∗][required for scaling.][From figure 8 it is seen that preferably] at both ends of the temperature range the slope of the Kramer plot has to be determined to extrapolate to Hc2[∗][(][T][).][This is most simply done by a][ J][c][(][H][) measurement at 4.2 K at] a few magnetic field values to check for linearity and thus validate the choice of q = 2. In addition this should be done at a higher temperature, e.g. 12 K might be a good compromise between temperature range and available magnetic field in a laboratory magnet. Non-linearities above h[∼] = 0.8 should be neglected since they most probably result from inhomogeneities. The results can then be extrapolated linearly in a Kramer plot to yield Hc2[∗][(4][.][2 K) and][H] c2[∗][(12 K).][The][MDG relation][(or its approximation)][then] yields Hc2[∗][(0][, ǫ][=][ǫ][m][)][and][T] c[ ∗][(0][, ǫ][=][ǫ][m][).][J][c][(][H, T, ǫ][=][ǫ][m][)][and][C][1][are][known][through] (47) using a least squares fit to the Jc data-set. 

The strain dependence can then be determined by a 4.2 K strain measurement with sufficient strain resolution to accurately determine the mechanical parameters (e.g. as in figure 9). The magnetic field for the strain characterization should preferably be chosen such, that over the entire strain range of interest, the critical current remains above about 10 A to avoid inaccuracies at low current measurements. A comparison to the Jc(H, 4.2 K) results above will yield ǫm and Hc2m[∗][(0)][and][T] cm[ ∗][(0)][can][be][calculated.] The entire critical surface up to the magnetic field where inhomogeneity effects start to appear (i.e. h[∼] = 0.8) is then known. The characterizations should preferably be done using one sample and one instrument to avoid experimental errors. The required 

data-set can thus be summarized as follows: 

- (i) An Ic(H) measurement at 4.2 K from about 5 T up to the maximum available magnetic field (see figure 8), preferably 12 to 15 T. 

- (ii) An Ic(H) measurement at about 12 K from 1 T or as low as possible, up to the maximum available magnetic field. The selectable temperature depends on the available magnetic field range (see figure 8). 

- (iii) An Ic(ǫ) measurement at 4.2 K and at a magnetic field where the critical current remains significant (e.g. > 10 A) over the entire strain range of interest (see figure 9). 

## 6. Conclusions 

A new, generally valid scaling relation is proposed which is based on a Kramer type pinning description. A number of improvements are made in comparison to the Summers form. A first improvement is a replacement of the empirical temperature dependency for the upper critical field with a microscopic based alternative. A second improvement is to replace the empirical temperature dependence of the Ginzburg-Landau parameter by a microscopic based alternative. A third improvement is made by replacing the power-law strain dependency with a new empirical deviatoric strain description that accounts for the effects of the third strain invariant and thus for asymmetry in the axial stain dependency curve. The use of an explicit normalized strain dependence term s(ǫ) enables straightforward implementation of optional future, more fundamental based, strain descriptions in the general scaling relation. A fourth improvement involves accounting for the inhomogeneities that are present in the A15 regions in wires by recognizing that the critical current scales with a bulk, inhomogeneity averaged critical field, representing some average of the upper critical field distribution that is always present in the A15 in wires. 

A systematic comparison of measured critical current as function of magnetic field, temperature and strain with scaling relations shows that flux-line shear can be assumed to be the main de-pinning mechanism and that tails in Kramer plots can reasonably be attributed to A15 inhomogeneities. This results in a generally valid magnetic field dependence of the Kramer form, i.e. Fp ∝ h[0][.][5] (1 − h)[2] within the range 0.05 < h < 0.8. 

Through the analysis of the magnetic field and temperature dependence of the bulk pinning force it is shown that the Kramer/Summers form, i.e. Fp ∝ [Hc2[∗][(][T][)]][2][.][5][/κ][1][(][T][)][2][,] fails to describe the observed temperature dependence with sufficient accuracy. The earlier suggestion that this followed from an empirical temperature dependence of the upper critical field and the GL constant was contradicted through the use of microscopic based relations for both. The change in κ1(T ) in the Kramer/Summers form is significantly larger than 50% as is expected from microscopic theory in the strong coupling limit. The improved temperature dependence of the form Fp ∝ [Hc2[∗][(][T][)]][2][/κ][1][(][T][)][does][accurately][describe][the][measurements.][The][resulting][change][in] 

κ1(T ) follows the microscopic form and is within the strong coupling limit. The new dependency is in disagreement with existing relations for the flux-line shear modulus C66. It is suggested that the temperature dependence of C66 as given by Labusch needs to be reevaluated. 

The new temperature dependence of the bulk pinning force allows for an unambiguous introduction of the strain dependence of the bulk pinning force, without the need to include separate functions to describe the strain dependent upper critical field and temperature dependent upper critical field, as is usually done in the literature. The measurements indicate that the Ginzburg-Landau parameter has similar strain dependence as the upper critical field. 

The improved deviatoric strain model, which includes asymmetry, yields an accurate description of measured behavior. Though empirical, it is based on conclusions resulting from more fundamental approaches and it recognizes the three dimensional nature of strain. 

## Acknowledgments 

This work was supported by the Netherlands Organization for Scientific Research (NWO) through the Technology Foundation STW and by the Director, Office of Science, Office of Fusion Energy Sciences, of the U.S. Department of Energy under Contract DEAC02-05CH11231. The Furukawa wires used in this research were donated by the Japan Atomic Energy Agency (JAEA) and were characterized under contract for the ITER European Home Team. All contributions are greatly acknowledged. 

## References 

- [1] Summers L T, Guinan M W, Miller J R and Hahn P A 1991 IEEE Trans. Magn. 27 2041 

- [2] Godeke A, ten Haken B and ten Kate H H J 2002, IEEE Trans. Appl. Supercond. 12 1029 

- [3] Godeke A, Jewell M C, Golubov A A, ten Haken B and Larbalestier D C 2003 Supercond. Sci. and Techn. 16 1019 

- [4] ten Haken B, Godeke A and ten Kate H H J 1999 J. Appl. Phys. 85 3247 

- [5] Cheggour N and Hampshire D P 2002 Cryogenics 42 299 

- [6] Keys S A and Hampshire D P 2003 Supercond. Sci. Technol. 16 1097 

- [7] Cheggour N and Hampshire D P 1999 J. Appl. Phys. 86 552 

- [8] Godeke A, ten Haken B and ten Kate H H J 2002 Physica C 372-376 1295 

- [9] Godeke A, ten Haken B and ten Kate H H J 1999 IEEE Trans. Appl. Supercond. 9 161 

- [10] Godeke A, Krooshoop H J G, ten Haken B and ten Kate H H J 2001 IEEE Trans. Appl. Supercond. 11 1526 

- [11] Oh S and Kim K 2006 J. Appl. Phys. 99 033909 

- [12] Oh S and Kim K 2005 A Consistent Description of Scaling Law for Flux Pinning in Nb3Sn Strands Based on the Kramer Model Preprint submitted to IEEE Trans. Appl. Supercond. 

- [13] Eliashberg G M 1960 Zh. Eksperim. i Teor. Fiz. 38 966 [Sov. Phys. JETP 11 696] 

- [14] Scalapino D J, Schrieffer J R and Wilkins J W 1966 Phys. Rev. 148 263 

- [15] Matsushita T, Yamafuji K and Irie F (ed) 1985 Proc. Int. Symp. on Flux Pinning and Electromagnetic Properties in Superconductors (Fukuoka, Japan) (Fukuoka: Matsukuma Press) 

- [16] Kramer E J 1973 J. Appl. Phys. 44 1360 

- [17] Dew-Hughes D 1974 Phil. Mag. 30 293 

- [18] Dew-Hughes D 1987 Phil. Mag. 55B 459 

- [19] Labusch R 1969 Cryst. Lattice Defects 1 1 

- [20] Labusch R 1969 Phys. Stat. Sol. 32 439 

- [21] Brandt E H 1977 J. Low Temp. Phys. 26 709 

- [22] Campbell A M and Evetts J E 1972 Adv. Phys. 21 199 

- [23] Larkin A I and Ovchinnikov Yu N 1979 J. Low. Temp. Phys. 34 409 

- [24] Markiewicz W D 2004 Cryogenics 44, 767 

- [25] Markiewicz W D 2004 Cryogenics 44, 895 

- [26] Markiewicz W D 2005 IEEE Trans. Appl. Supercond. 15 3368 

- [27] de Gennes P G 1966 Superconductivity of Metals and Alloys New York: W.A. Benjamin 

- [28] Parks R D (ed) 1969 Superconductivity New York: Dekker 

- [29] Maki K 1964 Physics 1 127 

- [30] de Gennes P G 1964 Phys. Kondens. Materie 3 79 

- [31] Helfand E and Werthamer N R 1964 Phys. Rev. Lett. 13 686 

- [32] Helfand E and Werthamer N R 1966 Phys. Rev. 147 288 

- [33] Werthamer N R, Helfand E and Hohenberg P C 1966 Phys. Rev. 147 295 

- [34] Hohenberg P C and Werthamer N R 1967 Phys. Rev. 153 493 

- [35] Werthamer N R and McMillan W L 1967 Phys. Rev. 158 415 

- [36] Eilenberger G and Ambegaokar V 1967 Phys. Rev. 158 332 

- [37] Usadel K D 1970 Phys. Rev. Lett. 25 507 

- [38] Usadel K D 1971 Phys. Rev. B 4 99 

- [39] Bergmann G and Rainer D 1973 Z. Physik 263 59 

- [40] Rainer D, Bergmann G and Eckhardt U 1973 Phys. Rev. B 8 5324 

- [41] Rainer D and Bergmann G 1974 J. Low Temp. Phys. 14 501 

- [42] Schopohl N and Scharnberg K 1981 Physica B 107 293 

- [43] Schopohl N and Scharnberg K 1985 Physica B 135 482 

- [44] Schossmann M and Schachinger E 1986 Phys. Rev. B 33 6123 

- [45] Rieck C T, Scharnberg K and Schopohl N 1991 J. Low Temp. Phys. 84 381 

- [46] Arai M and Kita T 2004 cond-mat/0404628 

- [47] Kita T and Arai M 2005 cond-mat/0403314 

- [48] Orlando T P, McNiff Jr. E J, Foner S and Beasley M R 1979 Phys. Rev. B 19 4545 

- [49] Orlando T P, Alexander J A, Bending S J, Kwo J, Poon S J, Hammond R H, Beasley M R, McNiff Jr. E J and Foner S 1981 IEEE Trans. Magn. 17 368 

- [50] Foner S and McNiff Jr. E J 1976 Phys. Lett. 58A 318 

- [51] Foner S and McNiff Jr. E J 1981 Solid State Commun. 39 959 

- [52] Charlesworth J P, MacPhail I and Madsen P E 1970 J. Mater. Sci. 5 580 

- [53] Wu I W, Dietderich D R, Holthuis J T, Hong M, Hassenzahl W V and Morris Jr. J W 1983 J. Appl. Phys. 54 7139 

- [54] Hawes C D, Lee P J and Larbalestier D C 2000 IEEE Trans. Appl. Supercond. 10 988 

- [55] Hawes C D 2002 Investigations of the Inhomogeneity of a Powder-in-Tube Nb3Sn Conductor M.S. Thesis Univ. of Wisconsin, Madison WI, USA 

- [56] Godeke A 2005 Performance Boundaries in Nb3Sn Superconductors Ph.D. Thesis Univ. of Twente, Enschede, The Netherlands, ISBN 90-365-2224-2 

- [57] Ab¨acherli V, Uglietti D, Lezza P, Seeber B, Fl¨ukiger R, Cantoni M and Buffat P A 2005 IEEE Trans. Appl. Supercond. 15 3482 

- [58] Fischer C M 2002 Investigation of the Relationships Between Superconducting Properties and Nb3Sn Reaction Conditions in Powder-in-Tube Nb3Sn Conductors M.S. Thesis Univ. of Wisconsin, Madison WI, USA 

- [59] Fischer C M, Lee P J and Larbalestier D C 2002 Adv. Cryog. Eng. (Materials) 48 1008 

- [60] Godeke A, Jewell M C, Fisher C M, Squitieri A A, Lee P J and Larbalestier D C 2005 J. Appl. 

Phys. 97 093909 

- [61] Marken K R, Kwon S J, Lee P J and Larbalestier D C 1986 Adv. Cryog. Eng. (Materials) 32 967 

- [62] Cooley L D, Fischer C M, Lee P J and Larbalestier D C 2004 J. Appl. Phys. 96 2122 

- [63] Moore D F, Zubeck R B, Rowell J M and Beasley M R 1979 Phys. Rev. B 20 2721 

- [64] Godeke A 2006 Supercond. Sci. Technol. 19 R68 

- [65] Devantay H, Jorda J L, Decroux M, Muller J and Fl¨ukiger R 1981 J. Mat. Sci. 16 2145 

- [66] Fl¨ukiger R 1982 in: Superconductivity in d- and f-Band Metals Buckel W and Weber W (ed) Kernforschungszentrum Karlsruhe 

- [67] Jewell M C, Godeke A, Lee P J and Larbalestier D C 2004 Adv. Cryog. Eng. (Materials) 50B 474 

- [68] Tinkham M 1996 Introduction to Superconductivity, 2[nd] ed. New York: McGraw-Hill 

- [69] Guritanu V, Goldacker W, Bouquet F, Wang Y, Lortz R, Goll G and Junod A 2004 Phys. Rev. B 70 184526 

- [70] Kroeger D M, Easton D S, DasGupta A, Koch C C and Scarbrough J O 1980 J. Appl. Phys. 51 2184 

- [71] Ekin J W 1980 Cryogenics 20 611 

- [72] Fietz W A and Webb W W 1969 Phys. Rev. 178 657 

- [73] Scanlan R M, Fietz W A and Koch E F 1975 J. Appl. Phys. 46 2244 

- [74] Shaw B J 1976 J. Appl. Phys. 47 2143 

- [75] Marken K R 1986 Characterization Studies of Bronze-Process Filamentary Nb3Sn Composites Ph.D. Thesis Univ. of Wisconsin, Madison WI, USA 

- [76] Schauer W and Schelb W 1981 IEEE Trans. Magn. MAG–17, 374 

- [77] West A W and Rawlings R D 1977 J. Mat. Sci. 12 1862 

- [78] Hampshire D P, Jones H and Mitchell E W J 1985 IEEE Trans. Magn. MAG–21 289 

- [79] Suenaga M and Clark A F (ed) 1980 Filamentary A15 Superconductors New York: Plenum Press 

- [80] Cooley L D, Lee P J and Larbalestier D C 2002 Adv. Cryog. Eng. (Materials) 48B 925 

- [81] Foner S and Schwartz B B (ed) 1981 Superconductor Material Science New York: Plenum Press 

- [82] Drost E, Fl¨ukiger R and Specking W 1984 Cryogenics 24 622 

- [83] Fl¨ukiger R 1987 Atomic Ordering, Phase Stability and Superconductivity in Bulk and Filamentary A15 Type Compounds Kernforschungszentrum Karlsruhe 

- [84] Abramowitz M and Stegun I A (ed) 1965 Handbook of mathematical functions with formulas, graphs, and mathematical tables New York: Dover Publications 

- [85] Beasley M R 1982 Adv. Cryo. Eng. 28 345 

- [86] M¨uller C B and Saur E 1963 Adv. Cryo. Eng. 8 574 

- [87] Buehler W and Levinstein H J 1965 J. Appl. Phys. 36 3856 

- [88] Ekin J W 1977 IEEE Trans. Magn. MAG–13 127 

- [89] Ekin J W 1981 IEEE Trans. Magn. MAG–17 658 

- [90] Ekin J W 1984 Adv. Cryo. Eng. (Materials) 30 823 

- [91] Chu C W and Vieland L J 1974 J. Low Temp. Phys. 17 25 

- [92] McEvoy J P 1971 Physica 55 540 

- [93] Pulver M 1972 Z. Physik 257 261 

- [94] Welch D O 1980 Adv. Cryo. Eng. (Materials) 26 48 

- [95] Testardi L R 1971 Phys. Rev. B 3 95 

- [96] Testardi L R 1973 in: Physical Acoustics 10 Mason W P and Thurston R N (ed) New York: Academic Press 193 

- [97] Testardi L R 1972 Phys. Rev. B 5 4342 

- [98] McMillan W 1968 Phys. Rev. 167 331 

- [99] Allen P B and Dynes R C Phys. Rev. B 12 905 

- [100] Kresin V Z, Morawitz H and Wolf S A 1993 Mechanisms of Conventional and High Tc Superconductivity New York: Oxford University Press 

- [101] Luhman T, Suenaga M and Klamut C J 1978 Adv. Cryo. Eng. 24 325 

## A general scaling relation for Nb3Sn 

- [102] ten Haken B, Godeke A and ten Kate H H J 1995 IEEE Trans. Appl. Supercond. 5 1909 

- [103] ten Haken B, Godeke A and ten Kate H H J 1996 IEEE Trans. Magn. 32 2739 

- [104] ten Haken B 1994 Strain effects on the critical properties of high–field superconductors Ph.D. Thesis Univ. of Twente, Enschede, The Netherlands ISBN 90-9007519-4 

- [105] ten Haken B, Godeke A and ten Kate H H J 1995 Inst. Phys. Conf. Ser. 148 85 

- [106] ten Haken B, Godeke A and ten Kate H H J 1997 Adv. Cryo. Eng. (Materials) 42B 1463 

- [107] Godeke A, Dhalle M, Morelli A, Stobbelaar L, van Weeren H, van Eck H J N, Abbas W, Nijhuis A, den Ouden A and ten Haken B 2004 Rev. Sci. Instr. 75 5112 

- [108] Hampshire D P, Taylor D M, Foley P and Keys S A 2001 Characterization of Nb3Sn and Nb3Al strands for Model Coils Report DurSC0601, Durham Univ., Superconductivity Group, Durham, England 

- [109] Godeke A, Knoopers H G, Nijhuis A, Krooshoop H J G, ten Haken B and ten Kate H H J 1998 Characterization of ITER strands in the frame of the third benchmark tests Report UT-NET 98-5, Univ. of Twente, Enschede, The Netherlands 

- [110] Godeke A, Krooshoop H J G, Knoopers H G, ten Haken B and ten Kate H H J 2000 Wide temperature and field scaling relations in Nb3Sn ITER strands Report UT NET/EFDA 20005, Univ. of Twente, Enschede, The Netherlands 

