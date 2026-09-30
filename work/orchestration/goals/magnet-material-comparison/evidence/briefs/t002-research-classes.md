# T-002 research worker brief — class-specific parts

Each worker receives the common brief (`t002-research-common.md`) plus exactly one section below.

## nb3sn-law — request `knowledge/research/requests/REQ-MMC-NB3SN-LAW-01.json`

Evidence note: `evidence/sources/nb3sn-law.md`.

The comparison needs an Nb₃Sn strand critical-current law Jc or Ic(B, T, ε) with published parameters for a named fusion-grade strand (ITER TF-class or EU DEMO-class preferred): Bc2*(0), Tc*(0), the prefactor C, exponents p and q, the strain function and its parameters, and the fitted and measured domain. Record the electric-field criterion (0.1 or 10 µV/cm) and whether Jc is per non-copper area. Evaluate the NIST lead (https://www.nist.gov/publications/extrapolative-scaling-expression-fitting-equation-extrapolating-full-icbte-data) rather than adopting it uncritically; the Bottura–Bordini ITER parameterization and the Godeke review are the other named candidates. Record any values the source itself prints for validation, such as strand Ic at 12 T and 4.2 K. Do not compute new values; an independent checker will evaluate the law against the original.

## nb3sn-winding — request `knowledge/research/requests/REQ-MMC-NB3SN-WP-01.json`

Evidence note: `evidence/sources/nb3sn-winding.md`.

Start with the registered EU DEMO source `knowledge/sources/eu_demo_rw_tf_coil_conductor_dematte_bruzzone/` and the registered `Coil Concepts for DEMO and Next Step Reactors` entry (find it in `knowledge/SOURCE_INDEX.md`). Context: `knowledge/KNOWLEDGE.md` DI-010 (around line 77). The comparison needs, for at least one fusion Nb₃Sn conductor: strand count and diameter, Cu:non-Cu ratio, cable void fraction, jacket and insulation thickness, conductor outer dimensions, operating current, peak field, operating temperature and inlet temperature, current-sharing-temperature margin, effective strain or cabling degradation used in design, and the resulting conductor and winding-pack current densities with their denominators. ITER TF conductor data (68 kA, about 11.8 T) from open-access sources are a useful second construction.

## rebco — request `knowledge/research/requests/REQ-MMC-REBCO-01.json`

Evidence note: `evidence/sources/rebco.md`.

Start with the registered Molodyk et al. source `knowledge/sources/development_and_large_volume_production_of_extremely_high/` and the registered magneto-angular fit source (find it in `knowledge/SOURCE_INDEX.md`). The comparison needs REBCO tape Ic(B, T) at roughly 15–25 K over 8–20 T with field perpendicular to the tape (or the stated worst orientation), tape construction (width, total thickness, substrate, copper), and at least one fusion REBCO cable or winding construction with its conversion from tape to cable and winding-pack current density (for example the SPARC TF model coil, or VIPER cable) and composition. The public Robinson Research Institute HTS critical-current database (Wimbush and Strickland) is a candidate for field/temperature data; record whether its data can be captured by the registry. Context only: the current model uses 200 A per 4 mm tape at 20 K and 20 T scaled as (B/20)^−0.6; report whether sources support a law of that shape below 20 T and how Ic depends on temperature near 20 K.

## cryo — request `knowledge/research/requests/REQ-MMC-CRYO-01.json`

Evidence note: `evidence/sources/cryo.md`.

Reuse the registered ITER cryoplant pages and the context in `knowledge/KNOWLEDGE.md` DI-009 (around line 70), plus registered current-lead, insulation and cryogenic-material sources where relevant. The comparison needs refrigerator efficiency separately at 4.5 K and near 20 K (fraction of Carnot or W/W), with staging explicit; distinguish a plant-wide efficiency inferred from mixed-temperature loads from a single-temperature law. It also needs magnet cold-load categories and magnitudes (radiation per area, support conduction, nuclear heating, AC and joint losses, current leads per kA) and how they differ between 4.5 K and 20 K operation. Candidates: M. A. Green, “The cost of coolers for cooling superconducting devices at temperatures at 4.2 K, 20 K, 40 K and 77 K”, IOP Conf. Ser.: Mater. Sci. Eng. 101 (2015) 012001 (open access; it also carries refrigerator capital cost, so register it here and the cost worker will reuse it); Strobridge's NBS refrigerator survey; LHC 4.5 K refrigerator performance papers.

## cost — request `knowledge/research/requests/REQ-MMC-COST-01.json`

Evidence note: `evidence/sources/cost.md`.

Start with the registered `HTS Potential and Needs for Future Accelerator Magnets` source (REBCO 150–200 USD per kA·m) and establish at which field and temperature that kA·m is defined. The comparison needs Nb₃Sn and REBCO prices with physical purchase units, the condition defining kA·m, amount purchased, currency year and scope (strand, cable, jacketed conductor, winding, installed magnet), plus any cabling, jacketing or winding manufacturing costs, and refrigerator capital cost per unit capacity at 4.5 K and 20 K. The cryo worker is registering M. A. Green (2015) on cooler cost; reuse it if it is registered (a `duplicate` outcome is fine). Candidates: ITER conductor procurement figures, CERN HL-LHC or FCC Nb₃Sn cost targets, Snowmass/DOE HTS cost roadmaps.
