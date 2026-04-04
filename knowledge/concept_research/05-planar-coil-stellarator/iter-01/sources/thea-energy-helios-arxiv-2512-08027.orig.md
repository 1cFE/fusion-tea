# Helios Design Paper — arXiv:2512.08027

**Title**: Overview of the Helios Design: A Practical Planar Coil Stellarator Fusion Power Plant
**URL**: https://arxiv.org/html/2512.08027v1
**PDF**: https://thea.energy/wp-content/uploads/2025/12/20251210_FPP_Helios_overview_paper.pdf
**Date**: December 2025
**Authors**: Thea Energy, Inc.
**Journal**: Preprint (submitted); associated Nuclear Fusion papers published Jan 2025

## Key Technical Specifications

### Plasma & Configuration
- **Stellarator type**: Quasi-axisymmetric (QA), 2-field-period
- **Major radius**: 8 m
- **Aspect ratio**: 4.5
- **Minor radius**: 1.8 m
- **On-axis magnetic field**: 6 T
- **Volume-averaged beta**: 2.7%
- **Peak electron density**: 2.1e20 m^-3
- **Peak ion temperature**: 20 keV
- **Energy confinement time**: 1.8 s
- **Plasma volume**: 500 m^3
- **ISS04 enhancement factor**: 1.4 (reference), 1.33 (gyrokinetic)

### Power Balance
- **Fusion power**: 958 MW
- **Total thermal power**: 1,094 MW (1.1 GW)
- **Gross electric**: 438 MWe
- **Net electric to grid**: 390 MWe
- **Auxiliary/facility power**: ~48 MWe
- **Recirculating power fraction**: <3%
- **Waste heat**: 681 MW
- **Thermal conversion efficiency**: ~40.2% (42.2% of total generated)

### Heating
- **Startup**: 10 MW ECRH at 170 GHz (ITER-spec gyrotrons, X1 polarization, high-field side)
- **Ignited operation**: 1 MW ECRH for impurity control
- **Total ECRH budget**: 2.5 MW (1 MW operational + overhead)
- **No NBI** — stellarator does not require current drive

### Magnets
- **Encircling coils**: 12 large toroidal field coils (4 unique shapes)
- **Shaping coils**: 324 individually controllable planar coils
- **Max on-coil field**: 20 T
- **Material**: HTS (REBCO implied)
- **Operating temperature**: 20 K (helium cooled)
- **Designed lifetime**: 40+ years (with shielding)
- **All coils**: Planar and convex, wound in tension

### Blanket & Tritium Breeding
- **Breeder**: Pb-17Li (lead-lithium eutectic, 17% Li by atom)
- **Li-6 enrichment**: 65%
- **Blanket thickness**: 50 cm
- **Structural material**: EUROFER97 steel
- **MHD inserts**: Silicon carbide
- **Coolant**: Helium gas
- **Flow rate**: 6.6 cm/s
- **Idealized TBR**: 1.3
- **Required TBR**: 1.1
- **Startup tritium**: 1-2 kg

### Neutron Shielding (multi-layer, inside to outside)
1. Tungsten carbide (WC) — high-energy neutrons
2. Boron carbide (B4C)
3. 316L stainless steel (vacuum vessel)
4. Borated water cooling
5. Borated HDPE
6. Concrete bioshield (~2.0 m thick)

### First Wall
- **Material**: V-4Cr-4Ti vanadium alloy ("V44") with tungsten armor
- **Thickness**: 2 cm with integrated helium cooling
- **Lifetime**: 15 full-power years

### Divertor
- **Type**: Novel tokamak-like X-point divertor (first for optimized stellarator)
- **Non-resonant**, toroidally continuous
- **Target**: Tungsten (51,000 hexagonal tiles, 2.5 cm)
- **Cooling**: Helium impingement jets
- **Heat flux**: 10 MW/m^2 assumed
- **Pumping**: Turbomolecular (not cryosorption)
- **10x better** neutral compression than island divertor

### Energy Conversion
- **Cycle**: Steam Rankine
- **Steam temperature**: 635°C superheated
- **Three-stage turbines**
- **Efficiency**: ~40.2%
- **Intermediate heat exchangers**: blanket/divertor coolants → water

### Operations
- **Capacity factor**: 88%
- **Maintenance cycle**: 84 days biennial
- **Sector-based maintenance**: Entire toroidal sectors removable
- **Minimum plasma-to-coil distance**: 1.2 m

### Energetic Particle Confinement
- **Alpha loss**: 6.6% of fusion product energy
- **Code**: ASCOT5

### MHD Stability
- Most unstable mode: 1.42% of Alfvén frequency (TERPSICHORE)
- No large-scale instability in nonlinear resistive MHD (M3D-C1)
