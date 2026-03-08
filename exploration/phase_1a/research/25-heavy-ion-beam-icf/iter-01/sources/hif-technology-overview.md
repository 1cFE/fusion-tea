# Heavy Ion Fusion Technology Overview

Compiled from multiple sources during research iteration 01.

## Driver Technology

- **Accelerator type**: Linear induction accelerator (induction linac) is the US reference design. RF linac is the European approach (GSI/HIDIF).
- **Wall-plug efficiency**: 30-40% (vs 1-15% for lasers). Source: arxiv 2005.07520, multiple LBNL references.
- **Ion species**: Bismuth (Bi²⁺) chosen for HIBALL — high mass/charge ratio (~200 u/e), single isotope, easy ionization. Lead, cesium, xenon, mercury also considered.
- **Beam energy**: 3-8 MJ per shot depending on target design. HIBALL uses 10 GeV Bi²⁺ at 160 mA. HYLIFE-II uses 5 MJ per shot.
- **Modularity**: Accelerator consists of hundreds of identical induction cells, enabling factory mass production.

Source: HIBALL study (KfK-3202), LBNL HIF tutorial, arxiv 2005.07520

## Target Design

- **Direct-drive targets**: Heavy ions deposit energy volumetrically (not surface absorption like lasers). Stopping range ~0.5-1 mm.
- **Target structure**: ~4 mm radius. Outer tamper of lead or gold, aluminum pusher, thin DT fuel ice layer on inner surface.
- **Target gain**: Requirement is ~50-70 for 1 GWe plant (lower than laser ICF due to higher driver efficiency). Advanced designs predict gains of 130+ at 3.3 MJ.
- **Compression**: Fuel compressed to ~1000x solid density.

Source: Wikipedia Heavy Ion Fusion, arxiv 2005.07520, OSTI target physics papers

## Power Plant Designs

### HIBALL (Germany/US, 1985)
- Heavy Ion Beams + Lithium-Lead
- 10 GeV Bi²⁺ ions from 3 km linear accelerator
- LiPb (lithium-lead) blanket for tritium breeding (TBR ~1.195)
- 5 Hz repetition rate per chamber
- 2000 MW fusion power per chamber
- 3.8 GW net electric output
- 15% power recirculation

Source: KfK-3202, academia.edu/61216305

### HYLIFE-II (LLNL, 1990s)
- FLiBe (Li₂BeF₄) molten salt jets as coolant/blanket/shield
- 5 MJ driver energy per shot, 350 MJ yield (gain ~70)
- 6 Hz repetition rate
- Recirculating induction accelerator driver ($570M direct cost estimate)
- 940 MWe baseline, scales to 1,934 MWe
- Cost estimate: 6.5 cents/kWh baseline, 4.5 cents/kWh at 2 GW scale
- Tritium inventory: 0.5 g in molten salt, 140 g in tube wall metal
- Thick liquid wall provides 30-year chamber lifetime (no replacement)

Source: OSTI 7021072 (HYLIFE-II final report)

## Magnet Technology in Accelerator

- Superconducting quadrupole magnet arrays used for beam transport through induction cells
- These confine the beam, NOT the plasma
- Compact 3x3 superconducting quadrupole arrays designed for parallel beam transport
- LTS (NbTi/Nb₃Sn) magnets in historical designs; modern designs could use HTS

Source: ResearchGate (superconducting quadrupole array paper), IEEE Xplore

## Current Experimental Status

- LBNL HIF program: ended (was main US program)
- NDCX-II: Neutralized Drift Compression Experiment at LBNL - demonstrated beam compression
- FAIR/GSI (Germany): Heavy ion facility in Darmstadt, operating 2025+ with HIF-relevant uranium ion pulses (5×10¹¹ ions, tens of GeV, ~100 ns)
- No private company is currently known to be pursuing HIF commercially (as of 2026)

## Energy Conversion

Both major power plant designs (HIBALL, HYLIFE-II) use conventional thermal (steam Rankine) cycles. The neutron energy from DT fusion is captured in the blanket (LiPb or FLiBe), which heats a working fluid for turbine generation.

## Neutron Management

- HYLIFE-II: Thick flowing FLiBe jets provide combined tritium breeding + neutron shielding + first wall protection
- HIBALL: LiPb blanket provides breeding and shielding
- Both are "integrated blanket/shield" approaches where the liquid serves multiple functions
