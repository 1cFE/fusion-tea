---
source: "https://www.osti.gov/servlets/purl/15013230"
source_type: "url"
extracted_at: "2026-04-20T16:19:41.568250+00:00"
content_hash_sha256: "797c71720ca9b54e01bc3baa90d93bcf1e8259e31abd1302fcdd8634e9cde41c"
backend: "pdf_pipeline"
---

Preprint UCRL-JC-136601 

## **Diode-Pumped Solid State Lasers for Inertial Fusion Energy** 

_S. A. Payne, C. Bibeau, R. J. Beach, A. Bayramian, J. C. Chanteloup, C. A. Ebbers, M. A. Emanuel, C. D. Orth, J. E. Rothenberg, K. I. Schaffers, J. A. Skidmore, S. B. Sutton, L. E. Zapata, and H. T. Powell_ 

## _This article was submitted to_ 

_Fusion Power for the 21[st] Century: Science and Technology for the New Millennium, Washington, DC, October 19-21, 1999_ 

## **U.S. Department of Energy** 

Lawrence Livermore National Laboratory 

**November 15, 1999** 

Approved for public release; further dissemination unlimited 

## DISCLAIMER 

This document was prepared as an account of work sponsored by an agency of the United States Government.  Neither the United States Government nor the University of California nor any of their employees, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights. Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise, does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or the University of California.  The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States Government or the University of California, and shall not be used for advertising or product endorsement purposes. 

This is a preprint of a paper intended for publication in a journal or proceedings. Since changes may be made before publication, this preprint is made available with the understanding that it will not be cited or reproduced without the permission of the author. 

This report has been reproduced directly from the best available copy. 

Available electronically at http://www.doc.gov/bridge 

Available for a processing fee to U.S. Department of Energy And its contractors in paper from U.S. Department of Energy Office of Scientific and Technical Information P.O. Box 62 Oak Ridge, TN 37831-0062 Telephone:  (865) 576-8401 Facsimile:  (865) 576-5728 E-mail: reports@adonis.osti.gov 

Available for the sale to the public from U.S. Department of Commerce National Technical Information Service 5285 Port Royal Road Springfield, VA 22161 Telephone:  (800) 553-6847 Facsimile:  (703) 605-6900 E-mail: orders@ntis.fedworld.gov Online ordering: http://www.ntis.gov/ordering.htm 

## OR 

Lawrence Livermore National Laboratory Technical Information Department’s Digital Library http://www.llnl.gov/tid/Library.html 

# **Diode-Pumped Solid-State Lasers for Inertial Fusion Energy** 

**S. A. Payne, C. Bibeau, R. J. Beach, A. Bayramian, J. C. Chanteloup, C. A. Ebbers, M. A. Emanuel,C. D. Orth, J. E. Rothenberg, K. I. Schaffers, J. A. Skidmore, S. B. Sutton, L. E. Zapata, H. T. Powell** _**Lawrence Livermore National Laboratory 7000 east Ave. Livermore, CA 94550-9234 USA**_ 

## **Abstract** 

We have begun building the “Mercury” laser system as the first in a series of new generation diode-pumped solid-state lasers for inertial fusion research. Mercury will integrate three key technologies: diodes, crystals, and gas cooling, within a unique laser architecture that is scalable to kilojoule and megajoule energy levels for fusion energy applications. The primary near-term performance goals include 10% electrical efficiencies at 10 Hz and 100J with a 2-10 ns pulse length at 1.047 µ m wavelength. When completed, Mercury will allow rep-rated target experiments with multiple chambers for high energy density physics research. 

## **Introduction** 

The ultimate goal of ICF is to build a power plant based on laser fusion[1] . The top-level requirements for the IFE driver itself are: 

- Efficiency, > 5 % 

- Reliability, availability and maintainability, > 10[9] shots 

- Cost, < $1.5 B 

- Beam smoothness for direct drive, < 1% on-target for < 1 nsec 

- Wavelength, < 0.4 µ m 

The efficiency of the IFE driver is important, since together with the target gain and costs, it determines the recycled power needed for the driver. The reliability and cost requirements follow from the need to produce commercially attractive electric power with a minimum 30-year plant lifetime.  The beam smoothness and wavelength requirements derive from 25 years of experience in laser fusion, which have been reviewed in recent papers on direct drive[2] and indirect drive.[3] 

Gas-cooled, diode-pumped, Yb:crystal lasers are envisioned to be the next-generation ICF solid state laser system producing high energy per pulse at modest rep-rates. As a solid state laser system, this new design shares a number of common features with flashlamp-pumped glass laser systems, especially with regard to fundamental issues: multi-pass amplification, laser propagation, energy storage, extraction, wavefront distortions, frequency-conversion, and beamsmoothing. The diode-pumped solid state laser (DPSSL) approach builds on the last two decades of solid state laser development but also adds several imposing challenges -- repetition rate, reliability, and cost. Large scale flashlamp-pumped solid state lasers built for ICF studies have been optimized for the $/Joule figure-of-merit and for their ability to match the target requirements. They are inherently single-shot devices, requiring several hours to recover from thermal distortions. However, this limitation need no longer be imposed by the laser technologies conceptually assembled in the early 1980s by Krupke and Emmett.[4,5] Innovative solutions for building ICF lasers with high repetition rate and efficiency include: 

- Trading the flashlamps for large, low-cost laser diode arrays 

- Using Yb:crystals for greater energy storage and thermal conductivity than Nd:glass 

- Employing near-sonic helium for cooling of the laser slabs 

The Mercury Laser is the first step in integrating these new approaches, and in producing new capabilities for irradiating ICF targets.  The primary performance goals for the Mercury Laser are: 

- 10 Hz repetition rate 

- 10 % efficiency 

- 1.047 µ m wavelength (1 ω ) 

- 100 Joules energy @2-10 ns 

- 5x diffraction-limited beam quality 

- 10[7] shot lifetime 

When completed, Mercury (Fig. 1) will be the highest energy/pulse diode-pumped laser ever built by an order of magnitude. It is noteworthy that the 100 J energy is the same as that of the Janus Laser, which is based on flashlamp-pumped Nd:glass and originally built in 1973. In addition, the Mercury Laser will be upgradable to 3 ω generation, broad bandwidth for beam smoothing, and picosecond pulse operation. 

## **Laser architecture** 

The Mercury laser design is predicated upon employing three technological advances: efficient and reliable diodes operating at 900 nm, Yb-doped crystals that offer longer storage lifetimes than the traditional Nd-doped materials, and active cooling with near-sonic helium gas flow across the crystalline laser slabs for rep-rated operation. The system layout incorporates an oscillator, pre-amplifier, and two power amplifiers. The gas-cooled power amplifiers are fourpassed in an angular multiplexing scheme. An adaptive optic in the beamline will be used to correct for wavefront distortions incurred during amplification. 

![](images/tmpo1kv04ux.pdf-0004-14.png)

**----- Start of picture text -----**<br>
beam fiber oscil lator<br>out regenerative amplifier<br>reverser optics<br>condenser lenses<br>output<br>diagnostics<br>gas-cooled<br>amplifier hea d<br>diode<br>pump head<br>vacuum 3:1 relay<br>spatial filter telescope<br>deforma ble<br>1 meter mirror<br>**----- End of picture text -----**<br>

Fig. 1 Mercury laser schematic. 

The amplifier head will be optically pumped from both sides. The dual pumping design allows for more uniform pumping and thermal loading on the crystals. The light from the diode array light is first concentrated with a hollow lens duct[6] followed by a hollow element that homogenizes spatial profile of the pump beam. Both the duct and the homogenizer are coated on the inside with a protected silver coating. The light emerging from the output of the homogenizer is imaged onto the gain media with a set of four condenser lenses designed to minimize the spatial aberrations. The angled dichroic beam splitters allow the pump beam to pass through the 

optic and into the amplifier head while allowing the extraction beam to be reflected. We have assembled one out of four pump delivery arms as shown in Fig. 2 below. 

![](images/tmpo1kv04ux.pdf-0005-02.png)

**----- Start of picture text -----**<br>
 Diodes<br>Installed in<br>Gas-Cooled<br>Diode Array<br>Amplifier<br>Head<br>(with surrogate<br>Pump<br>glass slabs)<br>Delivery<br>Optics<br>**----- End of picture text -----**<br>

Fig. 2. Picture of one of four diode pump delivery arms. 

In order to fully test the amplifier head and pump delivery system this year, surrogate gain media (Nd:glass) were placed in the vane elements within the amplifier head. This allows us to test the pump delivery efficiency, pump light uniformity within the laser slabs, gas flow dynamics, and thermal deposition profiles. Once the Yb:S-FAP crystals are ready, we can easily switch the surrogate slabs with the crystals. This approach will allow us to test the key elements in parallel with our efforts to develop adequately large crystals. 

## **Diodes** 

A critical technology for realizing inertial fusion energy is in the cost and efficiency of laser diode arrays. Existing diode technical performance specifications do not currently meet the demanding requirements of IFE. In addition, the manufacturing costs will have to be reduced by approximately two orders of magnitude to make IFE economically viable. Together with an industrial partner, Coherent-Tutcore, we made significant progress on the development of aluminum-free 900 nm laser diode bars. We packaged, characterized and life-tested two 40-bar arrays of 900nm laser bars using this diode material as shown in Fig. 3. 

![](images/tmpo1kv04ux.pdf-0005-07.png)

**----- Start of picture text -----**<br>
140<br>120<br>100<br>80<br>minimum<br>60 Mercury power<br>lifetime requirement<br>40 requirement<br>20<br>00 5 107 1 108 1.5 108<br>Shots<br>Power (W)<br>**----- End of picture text -----**<br>

Fig. 3. Lifetest data for 900nm diode material.  The material exhibits < 20% degradation over 10[8] shots under the Mercury conditions: 750 µs, 10 Hz operation.  The power per bar is noted on the plot. 

## **Amplifier head** 

The Mercury laser amplifier head and gas cooled architecture has been designed in a modular and scalable fashion, with the laser slabs mounted in an aerodynamic vane element as depicted in Fig. 4a. The vane elements are then stacked in a manner that forms a cooling channel 

between pairs of vanes, as depicted in Fig. 4b. Gas flows over the faces of the laser slabs, in the cooling channel, to remove the waste heat generated during the lasing process.[7,8] The assembled slab and vane cassette is then inserted into the amplifier head. The first laser head assembly was fabricated and installed in the Mercury laboratory, as shown in Fig. 2. 

![](images/tmpo1kv04ux.pdf-0006-02.png)

![](images/tmpo1kv04ux.pdf-0006-03.png)

**----- Start of picture text -----**<br>
Nozzle Channel Diffuser<br>section section section<br>Helium<br>gas<br>metal Slab<br>vanes Window Edge cladding<br>**----- End of picture text -----**<br>

Fig. 4. (a) Actual vanes in assembly. (b) A schematic cross-section through the amplifier head, showing the cooling passages between vanes. 

## **Crystal growth** 

Significant progress has been made in understanding the growth characteristics and defect chemistry of Yb:S-FAP [Yb[3+] :Sr5(PO4)3F] crystals. The Mercury laser requires crystalline slabs of dimension 4 x 6 x 0.75 cm. The growth of full size crystals has been a challenge due to a number of defects, including: cloudiness in as-grown boules, bubble core defects, grain boundaries, and cracking in larger diameter boules > 4.0 cm. An effort is underway to understand each of these defects and determine a reproducible growth technique for producing high optical quality crystals. Results have produced boules with greatly reduced defects that have optical properties that nearly meet the Mercury specifications. The current plan is to produce high quality crystals of 4.5 cm diameter from which two half slabs can be cut and diffusion bonded together to make adequately large crystals for Mercury. 

## **Beam Smoothing** 

A simple scaling of beam smoothing has been established which is helpful in the analysis of prospective ICF laser drivers.  The essential result found is that the smoothing of low spatial frequency speckle relevant to direct drive is fundamentally determined by the product of the optical bandwidth and the illumination solid angle. Thus, a small bandwidth driver, by illuminating with a larger solid angle, can achieve smoothing equivalent to that of a larger bandwidth driver. By applying spectral shaping to the amplifier input and broad band frequency conversion with dual triplers, the gain narrowed bandwidth can be increased to ~1 THz for DPSSLs.  Such a laser amplifier (e.g. Mercury and its successors) is therefore promising for use as a driver in an IFE power plant.  The scaling argument assumed can be used to compare NIF, for which it is generally agreed that 1 THz bandwidth will yield adequate smoothness for direct drive ignition, to the smoothing obtained with a proposed IFE driver with diode pumped crystalline (Yb:S-FAP) gain media of the same bandwidth. One finds that for a solid angle fraction of ~5% one can obtain smoothing significantly better than that of NIF. 

## **Beyond Mercury** 

A major objective of the present effort relates to establishing the readiness of the Mercury DPSSL driver to proceed to the next stage and beyond. The reliability, availability and maintainability of the laser components should be deemed to be acceptable for a future _integrated research experiment_ or IRE (kJ-class laser coupled with average-power target chamber), and have a plausible means of attaining the driver requirements of inertial fusion energy (IFE)[9] . The specific long-term technology development areas can be summarized: 

- Increase the efficiency of the DPSSL IFE driver to between 10 to 20%. 

- Reduce the cost of laser diodes to $0.50/watt for the IRE and to $0.05-0.07/watt for IFE. 

- Devise and demonstrate a scheme to produce <1 % smooth irradiation on-target for direct-drive in 0.1-1 nsec. 

- Grow gain media with > 10 cm apertures and fabricate with suitable optical quality. 

- Demonstrate high-average-power frequency conversion with 75% efficiency and 1 THz bandwidth. 

- Produce beam quality of < 5x diffraction-limited with wavefront correction. 

- Demonstrate integrated performance of DPSSLs to assure engineering viability. 

- Develop approaches for a survivable target chamber where x-ray yields lead to significant surface ablation and where the final optic is protected from debris and x-rays. 

- Resolve the manner in which multiple apertures and beam bundles are assembled to attain the kilojoule and megajoule level. 

One possible vision of an IRE is based on a 4 kJ DPSSL composed of four 1-kJ beamlets. This DPSSL would test performance at gain-limited aperture size as well as multi-aperture bundling technique needed to scale to very high energy. Most of the uses described above, including the neutron source, could be accomplished with the 4 kJ DPSSL of an IRE. A key feature of DPSSLs is that they are quite likely to achieve the efficiency required for direct drive target (> 5%), and that they may also reach the efficiency required for indirect drive targets (1020%). Moreover, they have the inherent capability of providing the high-energy picosecond pulses needed for the advanced fast ignition approach. 

## **Summary** 

When completed Mercury will be the highest energy/pulse diode-pumped laser ever built by an order of magnitude that offers the dimension of high repetition rate (~10 Hz). It will motivate the development of rep-rated targets and diagnostic capabilities. In addition, a major objective of the Mercury laser relates to establishing the readiness of the Mercury DPSSL driver to proceed to the next stage and beyond for fusion energy.[1] 

Work performed under the auspices of the U. S. Department of Energy by UC/Lawrence Livermore National Laboratory under contract W-7405-Eng-48. 

**References:** 

> 1   W. J. Hogan, ed., Energy from Inertial Fusion (International Atomic Energy Agency, Vienna, 1995). 

> 2   S. E. Bodner, et al., Physics of Plasmas **5** 1901-1917 (1998). 

> 3   J. D. Lindl, Physics of Plasmas **2** , 3933 (1995). 

> 4  W. F. Krupke, Fusion Technol. **15** , 377 (1989). 

> 5  J. L. Emmett and W. F. Krupke., Sov. J. Quantum Electron. **13** ,1 (1983). 

> 6  R. J. Beach, Appl. Opt., **35** , 2005 (1996). 

> 7  S. B. Sutton and G. F. Albrecht, J. Appl. Phys. **69** , 1183 (1991). 

> 8  G. F. Albrecht, et al., Appl. Opt. **29** , 3079 (1990). 

> 9  C. D. Orth, S. A. Payne, and W. F. Krupke, Nuclear Fusion **36** (1), 75 (1996). 

