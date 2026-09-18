# Traceable material cards for the retained HCLL transport scenario

Date: 2026-09-18. Research proposal, not qualification of a manufactured blanket. `[OWNER]` Retain helium-primary PbLi and the current radial dimensions. `[AGENT]` The choices below supply explicit representative compositions where the plant model has no neutron-material definition. Registration runs through `REQ-computed-tritium-breeding-04` and the narrow WC follow-up `REQ-computed-tritium-breeding-06`; no model changes.

## Acquired authority and inspection

King et al., *High Temperature Zirconium Alloys for Fusion Energy*, UKAEA-CCFE-PR(21)83, is registered at `knowledge/sources/high_temperature_zirconium_alloys_for_fusion_energy/`. Original PDF SHA256 is `39b05af195768acec864478bc3a968102553968bf1b4caa106c717ca6fc41a54`. The appendix occupies PDF pp.63–65 (printed pp.59–61). I visually inspected p.64's actual density/composition tables, not just extracted text. It uses OpenMC material recipes generated with neutronics-material-maker. These are published simulation cards, not independent density measurements.

PNNL-15870 Rev.2, *Compendium of Material Composition Data for Radiation Transport Modeling* (Detwiler et al., 2021), was obtained from the official LANL mirror after PNNL's direct PDF returned HTTP403. Original PDF pp.60 and 244–245 were visually inspected for boron and SS316. These are representative nuclear-transport materials; the source warns that density/composition variations occur in practice and does not quantify uncertainty. Registered source: `knowledge/sources/compendium_of_material_composition_data_for_radiation/`; original SHA256 `a34df48e1025cbd9649c8d7a635454ab57af9b0c59b5fb1faaaf4db1057dcb4b`.

## Constituent cards

Use positive fractions in the implementation; negative signs in PNNL MCNP cards denote weight-fraction syntax, not negative material amounts.

| Constituent | Density, g/cm³ | Composition and basis | Authority |
|---|---:|---|---|
| PbLi | 9.15 | Atomic Pb0.842, Li0.158; split Li into 70% Li-6 and 30% Li-7 for the proposed case | King appendix p.63 composition, Table A2 p.64 density at500°C; enrichment70% is the agent-selected source-Stellaris isotope scenario |
| EUROFER97, first wall | 7.78 | Weight fractions Fe0.8927, C0.0011, Mn0.0040, Cr0.0900, Ta0.0012, W0.0110 | King Table A1 first-wall density and structural table on p.64 |
| EUROFER97, breeder/structure | 7.80 | Same element weight fractions | King p.64 structural-material table |
| Tungsten armor | 19.0 | Element W1.0 | King Table A1; structural-material table instead uses19.3, retained as alternate |
| Helium | 0.0056 | `[AGENT]` He-4 only; pure coolant approximation | King Table A1:8MPa,500°C |
| SS316 | 8.0 | Weight fractions C0.0008, Mn0.0200, P0.00045, S0.00030, Si0.0100, Cr0.1700, Ni0.1200, Mo0.0250, Fe0.65345 | PNNL card333, PDF pp.244–245 |
| Boron | 2.37 | Atomic B-10 fraction0.199, B-11 fraction0.801 | PNNL card41, PDF p.60 |
| Tungsten carbide | 15.6 | Pure stoichiometric W:C=1:1 atomic; natural isotope compositions; no cobalt binder | ATSDR2005 Table4-2, tungsten carbide density row, citing HSDB2004; temperature unspecified |

The EUROFER and SS316 weight fractions each sum to1.000000. The PbLi total atomic composition at70% enrichment is Pb0.842, Li-6 0.1106, Li-7 0.0474. Do not use lithium16% as a weight fraction. King explicitly supplies15.8 at%, close to source Stellaris's rounded16 at%; selecting15.8% here is an agent material choice, not an assertion that their recipes are identical.

Use natural isotope abundances for elements except explicitly enriched Li and explicitly specified B. Export the expanded nuclide inventory and abundance-table identity with the run. Avoid letting nuclear-data availability silently delete an isotope: report any substitution or renormalization. King's carbon and other elements are elemental recipes; natural-abundance expansion is an implementation step.

## Mixtures and temperatures

Keep the proposal's HCLL breeder mixture80%PbLi/10%EUROFER/10%He by volume, derived from Martínez Arroyo Table3-2. Its mixture mass density is `0.8*9.15 + 0.1*7.8 + 0.1*0.0056 = 8.10056 g/cm³`. Compute nuclide number densities constituent-by-constituent, then multiply each by its volume fraction. Do not interpret80/10/10 as mass fractions. First-wall coolant/steel mixture70%EUROFER/30%He has density5.44768g/cm³ before the separate armor layer. Vessel mixture61%SS316/37%He/2%B has density4.929472g/cm³. These values are arithmetic consequences of the selected cards, not separately measured properties.

`[AGENT]` Use773.15K as the source-matched initial breeder/coolant temperature, the retained loop's500°C outlet endpoint. This amends the earlier400°C representative-temperature proposal so the first transport run can use published liquid/gas densities at their stated temperature. It changes no plant dimension or coolant technology. A400°C case remains desirable, but9.15g/cm³ is not a published400°C PbLi density. Solids' densities are representative constants; King does not provide thermal-expansion laws for them. PNNL SS316/B densities likewise carry no500°C qualification. Report that approximation and test a declared density perturbation; do not call a chosen perturbation an experimentally established uncertainty bound.

The published He density0.0056g/cm³ is not the ideal-gas result at8MPa/773.15K. Preserve it for source-reproduction work and run the equation-of-state-derived density separately if available; do not silently overwrite the published card. This discrepancy is small in total blanket mass but its neutron effect must be calculated. Distinguish material physical temperature from tabulated nuclear-data temperature and record whether interpolation or nearest-temperature selection is used.

## WC authority and scope

ATSDR2005 Table4-2 supplies15.6g/cm³ for tungsten carbide, separately from ditungsten carbide14.8g/cm³. The official government table is registered at `knowledge/sources/atsdr_tungsten_physical_and_chemical_properties_table_4_2/` (raw SHA256 `7a3c2d9d1e16d87ef04b6cf28bac696055a524e4204c83fe3f8935e0926b56ed`). It is a compiled authority citing HSDB2004, not a new primary density measurement. `[AGENT]` Apply this representative constant to pure stoichiometric WC without cobalt binder or porosity; the table gives no measurement temperature or uncertainty. The90%WC/10%He reflector and shield then have density14.04056g/cm³. A declared ±5%WC-density sensitivity is a scenario perturbation, not a measured confidence interval. Boron in the thesis vessel recipe is elemental B, not B4C.

King also offers a useful relative-response benchmark:10m spherical vacuum radius,3mm armor,27mm first wall,2m breeder,10% breeder coolant, Muir source around14.06MeV and no backing. Its published response is normalized TBR, not an absolute reference. Its simple sphere supports material-response checks; it does not validate mapping a spherical result onto the retained torus. The coordinator's integral experimental benchmark work is separate.

## Additional elemental cards for benchmark sensitivity

PNNL card189 (PDF p.160, printed p.143) gives elemental Pb density11.35g/cm³. Card192 (PDF p.161, printed p.144) gives Li density0.534g/cm³ and atom fractionsLi-6 0.0759/Li-7 0.9241. Both original pages were visually inspected and cite NIST STAR for density. These are conventional representative elemental densities, not exact OKTAVIAN experimental sample specifications. The benchmark worker received that distinction.

Cross-section interpolation between600K and900K at the physical773.15K temperature does not interpolate material density. PbLi and He retain the sourced500°C density cards; solid densities, including WC, retain their separately declared representative-constant approximation. Record both choices independently.
