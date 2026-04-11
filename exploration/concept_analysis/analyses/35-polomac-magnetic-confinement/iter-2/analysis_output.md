# D1+ Analysis: PoloMac Magnetic Confinement (Deutelio)

---

## Section 1: Availability of Data

**Rating: Limited**

PoloMac is among the most thinly documented concepts in the analysis portfolio. Three source files were available; all are shallow.

**Primary technical sources:**

The foundational document is a 2014 Fusion Engineering and Design paper by F. Elio — *"Revisiting the poloidal magnetic confinement"* — which presents static 2D and 3D magnetic field analyses of the PoloMac geometry. The full text is paywalled; the extracted source contains only the introduction, section snippets, and conclusions. Despite this limitation, the snippets are sufficiently detailed for the paper's scope: the work is explicitly a magnetic design feasibility study with no plasma physics, confinement, or cost content. The paper's own conclusions state:

> "Further analyses on MHD, confinement, stability and an outline engineering design are required to assess the possibilities envisaged."
> — elio-2014-fed-poloidal-confinement.md, §Conclusions

The 2024 JTSP technical report — *"Technical Report: The Polomac approach to fusion energy"* — provides updated framing and performance claims. The extracted source contains only the abstract; the full paper body was not recovered from the journal URL. The abstract is nevertheless the most concise statement of the concept's claimed advantages and development strategy.

The Deutelio company profile is startup directory content: a 3-stage roadmap, team description, and competition results. It contains no technical specifications beyond a prototype magnet field of 0.2–0.3 T.

**Independent assessments:** None identified. An unnamed independent "fusion company tier list" cited in the company profile rates Deutelio C−. No third-party plasma physics analysis, cost study, or system code output exists in the source corpus.

**Key data gaps limiting analysis:**
- No plasma performance data (temperature, density, confinement time, triple product) at any field
- No heating method specified
- No reactor design parameters (Q, fusion power, net electric output, thermal efficiency)
- No engineering design beyond the magnetic field shape
- No cost data of any kind

The Phase 1a dossier coverage is consistent with source depth: dossier confidence is high only for confinement family, fuel, operation mode, and the magnetic tunnel driver description. All performance-relevant columns are low-confidence or unknown.

---

## Section 2: Challenges in Capturing System Function

Ranked in order of LCOE modeling impact:

**1. Recirculating power penalty — severity: blocking**

The 2014 FED paper reports copper coil power consumption of 700 MW for a plasma volume of 1300 m³:

> "The power consumption in 0.1 m thick copper coil layer reaches 700 MW, like in JET but excessive for steady operation."
> — elio-2014-fed-poloidal-confinement.md, §Coil support and supply

This is the single most important quantitative datum in the available sources. A 700 MW recirculating power draw dwarfs the net electric output of any plausible fusion power plant — a 1 GWe gross plant would have a negative recirculating fraction well below any economic viability threshold. The paper acknowledges this as excessive and implies that the solution is superconducting coils, but no superconducting coil design has been published. Until a credible superconductor path is specified with achievable field levels and coil geometry, the recirculating power cannot be estimated for a commercial design. This gap is individually sufficient to prevent any LCOE estimate.

**2. No plasma heating method specified — severity: blocking**

The dossier records primary heating as "Unknown (low confidence)." Neither paper discloses a heating scheme. This gap is especially severe because D-D fusion requires plasma ion temperatures of ~50–100 keV — substantially higher than the ~20 keV threshold for D-T — and heating power requirements scale steeply with energy confinement time. Without knowing the heating approach (NBI, ECRH, ICRH, ohmic), the auxiliary power system cannot be sized, and recirculating power fractions cannot be computed.

**3. No confinement physics validation — severity: blocking**

Historical poloidal-dipole experiments achieved "few eVs" plasma temperature and ~10¹⁶ m⁻³ density — many orders of magnitude below fusion-relevant parameters [1]. The 2014 FED paper performs only static magnetic field analysis; it explicitly defers MHD stability, confinement, and plasma physics to future work. No confinement scaling law for the PoloMac geometry has been published. Without demonstrated confinement at any relevant parameter, the plasma Q and wall-plug gain remain unconstrained.

**4. D-D fusion energy balance — severity: important**

D-D fuel is claimed as an advantage (no tritium breeding blanket needed), but it carries severe energy balance penalties. D-D reactions produce ~6x less energy per reaction than D-T, require higher plasma temperatures to ignite, and generate substantial 2.45 MeV neutrons (50% of the D-D → tritium + proton branch) plus energetic protons. Achieving breakeven on D-D in a dipole geometry is an extraordinary extrapolation from current experiments. No quantitative analysis of the D-D energy balance appears in any available source.

**5. In-vessel coil maintenance and lifetime — severity: important**

The in-vessel dipole coil, while physically supported via magnetic tunnels, will be exposed to neutron flux and plasma heat loads. No shielding scheme, materials selection, or lifetime estimate for the in-vessel coil has been published. The 2014 paper notes that coils "will be compressed against the shell structure, needing a segmentation scheme suited for assembly and maintenance" but provides no details. For any power plant design, in-vessel coil replacement cost and schedule are major capacity factor and capital cost drivers.

**6. No reactor design point — severity: important**

Without a published design point (major radius, plasma current, field strength, thermal power), all CAS-level cost estimates must be analogued from other MFE concepts. The claimed field advantage (3x weaker field than tokamak for D-T; same field as tokamak for D-D) suggests potential magnet cost reduction, but the very large plasma volume implied by the 1300 m³ figure (at ~2 T) and the unknown coil geometry prevent translation into a $/kWe estimate.

---
[1] elio-2014-fed-poloidal-confinement.md, §Past dipole experiments: "The best performances of the poloidal configurations with in-vessel rings of any type were: energy parameter beta 20–30%, plasma temperature of few eVs and densities of about 10¹⁶ m⁻³. The latter values are irrelevant when compared [to fusion conditions]."

---

**Key Differentiators vs. Conventional D-T Tokamak**

| Subsystem / Feature | PoloMac | Conventional D-T Tokamak | Classification |
|---------------------|---------|--------------------------|----------------|
| Confinement geometry | Poloidal dipole field — plasma confined by in-vessel dipole coil | Toroidal field — plasma confined by external coil set | Novel |
| Coil placement | In-vessel dipole coil, physically supported through plasma via magnetic tunnels | All superconducting coils external to the vessel | Novel |
| Fuel cycle | D-D (primary target): no tritium breeding blanket required | D-T: requires Li blanket, FLiBe, Li-6 enrichment infrastructure | Novel (if achievable) |
| Field strength | Claimed 3× weaker than tokamak for D-T equivalent; unvalidated | ~5–20 T on-axis (concept-dependent) | Claimed advantage (no design study supports this) |
| Recirculating power model | Fixed infrastructure penalty (700 MW copper; SC path unspecified) | Q-dependent plasma fraction (plasma-physics-determined) | Novel structure; penalty unresolved |
| Heating system | Unspecified; NBI or RF expected by analogy | NBI, ECRH, ICRH (well-established and sized) | Shared approach, unspecified implementation |
| Operation mode | Steady-state (explicitly claimed) | Quasi-steady to pulsed (conventional); steady-state (advanced) | Shared (claimed) |
| Power conversion | Not specified; conventional thermal cycle expected | Thermal (steam or sCO₂) | Borrowed |
| Vacuum system | Required; large vessel (~1300 m³) | Required; similar scale | Shared |
| Remote handling | Required for in-vessel coil (activated, neutron-irradiated) | Required for in-vessel components; well-developed | Shared — but more complex given tunneled in-vessel coil geometry |

**Modeling Approach Rationale**

Free-form LCOE modeling is the appropriate method for PoloMac. Standard 1costingfe parameterization requires a physics-derived design point — confinement scaling, plasma Q, reactor geometry, system code output — none of which exist for this concept. The model instead proceeds from scenario assumptions about Q and fusion power, which are fed into a CAS-structured cost framework by analogy with generic MFE plant structures.

The consequence for result interpretation is significant: all model outputs are scenario bounds, not engineering estimates. The model tests the following three propositions:

1. **Superconducting coil viability**: If the SC coil capital cost can be bounded (e.g., ≤ $300–500M for the in-vessel dipole system), and if Q ≥ 10–15 is achievable for D-D confinement, then gross LCOE could in principle reach competitive ranges at sufficient plant scale.
2. **Blanket elimination value**: The absence of a tritium breeding blanket represents a genuine capital cost reduction (estimated at $200–500M for comparable D-T MFE concepts) — but this advantage is entirely contingent on D-D ignition being achievable, which is an unresolved physics question.
3. **Recirculating power dominance**: The in-vessel coil system is the single highest-leverage parameter in any PoloMac cost model. Whether the coil is resistive (prohibitive) or superconducting (uncertain), and what maintenance interval the neutron environment imposes, will dominate LCOE more than any other design variable. The model captures this through direct sensitivity sweeps on SC coil cost and capacity factor.

These are propositions to test, not validated conclusions. The model output should be read as "conditions under which PoloMac could be competitive," not as a point estimate.

---

## Section 3: Maturity of Key Subsystems and Components

Subsystems are listed in ascending order of maturity (least mature first).

---

**Plasma Confinement and Heating — TRL 1**

- **Demonstrated**: Static magnetic field topology achievable by calculation (2D and 3D FEA only). No plasma experiment at PoloMac field levels or geometry has been conducted.
- **On paper only**: The PoloMac concept itself. MHD stability, confinement scaling, transport coefficients, and plasma performance all exist only as claims extrapolated from historical 0.1–0.3 T dipole experiments.
- **Missing at scale**: Any plasma physics validation. A heating method must be chosen and integrated. Confinement time, density, and temperature must be demonstrated at even sub-fusion conditions before ignition physics extrapolation is meaningful.

---

**In-Vessel Dipole Coil with Magnetic Tunnel Supports — TRL 2**

- **Demonstrated**: Magnetic field shaping to create plasma-free channels ("magnetic tunnels") has been demonstrated by finite element analysis. The 2014 paper proves the geometry is magnetically feasible.
- **On paper only**: Physical fabrication of the coil support system, electrical/hydraulic feed-throughs, and the segmented coil assembly. No prototype exists at any scale.
- **Missing at scale**: Structural design under combined magnetic, thermal, and neutron loads. Maintenance access scheme. Long-term neutron damage management for in-vessel coil. Radiation-hard insulation. No LDX-class experiment has approached PoloMac parameters.

---

**Superconducting Coil Path (Commercial Scale) — TRL 1–2**

- **Demonstrated**: Commercial superconductors exist (REBCO HTS, Nb₃Sn LTS), but their application to the specific PoloMac in-vessel geometry is entirely unspecified.
- **On paper only**: A design intention to use superconducting magnets at commercial scale is mentioned in the company profile but no conductor type, field target, coil geometry, or cryogenic scheme has been published.
- **Missing at scale**: Radiation-tolerant superconducting in-vessel coil at fusion-relevant neutron fluence — a problem with no established solution for any concept.

---

**D-D Plasma Heating System — TRL 1**

- **Demonstrated**: NBI and RF heating have been demonstrated in many MFE devices, but not in the PoloMac topology and not for D-D conditions. No heating system has been specified by Deutelio.
- **On paper only**: Not even on paper — no heating design exists in any available source.
- **Missing at scale**: The full heating system design, sizing, and integration with the in-vessel coil structure.

---

**Neutron Shielding and First Wall — TRL 2–3**

- **Demonstrated**: D-D neutron shielding is a mature discipline. 2.45 MeV neutrons are less damaging per unit than 14 MeV D-T neutrons but still require substantial shielding to protect the in-vessel coil and external structure.
- **On paper only**: Specific shielding design for the PoloMac geometry, including protection of the in-vessel coil from neutron flux.
- **Missing at scale**: Neutron damage evaluation for the in-vessel coil at commercial fluences. No design exists.

---

**Balance of Plant / Power Conversion — TRL 2**

- **Demonstrated**: Conventional thermal power cycles (Rankine, sCO₂) are mature for other applications.
- **On paper only**: No energy conversion design has been specified for PoloMac.
- **Missing at scale**: Integration with PoloMac heat extraction geometry. Concept is not yet at a stage where BOP design is meaningful.

---

**O&M and Availability**

No O&M data is available. Given the TRL-1 state of the plasma physics and the unsolved problem of in-vessel coil maintenance in a neutron environment, capacity factor estimates would be entirely speculative. No placeholder estimate is warranted. The in-vessel coil is structurally analogous to the levitated dipole coil challenge in 12-levitated-dipole: planned maintenance access requires precise remote handling inside an activated vessel, but in PoloMac the coil is fixed rather than levitated, which eases some operational complications while creating others (coil must be designed for removal/replacement under neutron activation).

---

## Section 4: Key Materials and Supply Chain Considerations

**Copper coils (prototype path)**

Current prototype magnets use water-cooled copper operating at 0.2–0.3 T. Copper coils are abundant and mature. However, the 700 MW steady-state power draw at 2 T and 1300 m³ plasma volume makes copper coils commercially nonviable. This is not a supply chain constraint — copper is widely available — but an engineering constraint that requires migrating to superconducting coils before any economic analysis is applicable.

**Superconductor (commercial path — unspecified)**

The company profile implies a superconducting coil path for commercial scale. Neither conductor type (REBCO HTS, Bi-2223, Nb₃Sn) nor operational field target has been specified. If REBCO HTS is chosen, the supply chain constraints identified in the 01-hts-compact-tokamak analysis apply: global REBCO production is on the order of thousands of km/year, and a large-bore in-vessel coil at fusion-relevant fields would require substantial tape length. The in-vessel geometry adds a specific complication: radiation-tolerant insulation must be compatible with the superconductor fabrication process, and no vendor currently supplies radiation-hardened HTS coils qualified for sustained neutron environments.

**Deuterium fuel**

D-D fuel is the claimed commercial design target. Deuterium is present in natural water at ~155 ppm (D/H ratio) and is separated by electrolysis or distillation at low cost (~$5,000–10,000/kg [analogue: industrial deuterium prices]). The global deuterium supply chain is mature; no supply constraint is anticipated at any fusion deployment scale. This is a genuine cost advantage versus D-T, where tritium costs >$35,000/g and must be bred.

**Tritium breeding blanket — not required for D-D**

The D-D fuel cycle eliminates the need for a lithium blanket, FLiBe, or lithium-6 enrichment. This removes several supply chain constraints that burden D-T concepts: beryllium (sole-sourced from Materion), lithium-6 enrichment (limited suppliers, environmentally sensitive processes), and molten salt processing infrastructure. This advantage is real but contingent on D-D ignition being achievable — a physics gap of the highest severity.

**Neutron shielding materials (D-D)**

D-D produces 2.45 MeV neutrons at 50% reaction yield (D+D → T+p branch produces no neutrons; D+D → He3+n branch produces 2.45 MeV neutrons). The neutron wall loading will be lower than a D-T machine of equivalent power due to lower energy per reaction and different reaction cross-sections, but shielding is still required. Tungsten and steel shielding are commercially available without supply constraints. The in-vessel coil neutron shielding presents unique geometry challenges not present in any other operating concept.

**No exotic or specialty materials identified**

The available sources contain no mention of beryllium, vanadium alloys, SiC composites, or other specialty materials. This reflects the concept's TRL-1 status rather than confirmed material choices.

---

## Section 5: LCOE-Relevant Parameters

**Available Parameters:**

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Plasma beta | 20–30% | elio-2014-fed-poloidal-confinement.md §Introduction | medium | Claimed based on historical dipole experiments; not measured in PoloMac |
| Magnetic field (coil current density) | ~2 T at 10–25 A/mm² | elio-2014-fed-poloidal-confinement.md §Magnet coils | medium | Compatible with water-cooled copper; commercial design unspecified |
| Plasma volume | 1300 m³ | elio-2014-fed-poloidal-confinement.md §Coil support and supply | medium | From the 2014 design geometry; not a power plant design point |
| Copper coil recirculating power | 700 MW | elio-2014-fed-poloidal-confinement.md §Coil support and supply | high | Acknowledged as prohibitive for steady operation |
| Prototype magnet field | 0.2–0.3 T | deutelio-company-profile.md §Technical | medium | Hydrogen plasma only; copper coils |
| Claimed D-T field advantage | 3× weaker field than tokamak | jtsp-2024-polomac-technical-report.md §Abstract | low | Unvalidated claim; no design study supports this |
| Operation mode | Steady-state | jtsp-2024-polomac-technical-report.md §Abstract | high | Explicitly stated as opposed to pulsed tokamak |
| Fuel | D-D (primary target), D-T (secondary claim) | jtsp-2024-polomac-technical-report.md §Abstract | high | D-D requires no tritium breeding |
| Historical plasma temperature | Few eV | elio-2014-fed-poloidal-confinement.md §Past dipole experiments | high | Historical experiments only — irrelevant to fusion conditions |
| Historical plasma density | ~10¹⁶ m⁻³ | elio-2014-fed-poloidal-confinement.md §Past dipole experiments | high | Historical experiments only — irrelevant to fusion conditions |
| Net electrical output | Unknown | — | — | Not stated in any source |
| Thermal efficiency | Unknown | — | — | No power conversion design exists |
| Plasma Q | Unknown | — | — | No confinement physics analysis |
| Fusion power | Unknown | — | — | No reactor design point |
| Capital cost (total plant) | [not estimable] | — | — | No design sufficient for estimation |

**Missing Parameters:**

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Plasma heating method and power | truly-unknown | blocking | No disclosure in any source; critical for recirculating power fraction |
| Plasma Q / energy gain | truly-unknown | blocking | No confinement physics analysis performed |
| Net electric output / plant size | truly-unknown | blocking | No reactor design point |
| Thermal efficiency | truly-unknown | blocking | No power conversion design |
| Recirculating power fraction (commercial) | derivable (if SC coil specified) | blocking | Currently ~700% gross at copper coil design; must drop dramatically |
| Major radius / plasma dimensions (reactor) | truly-unknown | blocking | 1300 m³ volume not tied to a power plant design point |
| In-vessel coil neutron fluence limit | truly-unknown | blocking | No shielding design; sets maintenance interval and capital cost |
| Capacity factor | truly-unknown | important | Depends on maintenance scheme, confinement reliability |
| $/kWe capital cost | truly-unknown | blocking | Cannot estimate without reactor design point |
| LCOE estimate | not-yet-estimable | blocking | Too many blocking gaps upstream |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | No plasma heating method specified | S2, S3, S5 | truly-unknown | blocking | Deutelio has not disclosed this; future publications or direct inquiry required |
| 2 | 700 MW copper coil draw — no SC coil design to resolve it | S2, S3, S5 | proprietary/truly-unknown | blocking | No commercial design published; superconducting path unspecified |
| 3 | No plasma confinement physics analysis (MHD stability, scaling) | S1, S2, S3 | truly-unknown | blocking | Would require a new plasma physics study; no data exists in public domain |
| 4 | No reactor design point (Q, major radius, thermal power) | S2, S5 | truly-unknown | blocking | Deutelio has not published a design point |
| 5 | Thermal efficiency / power conversion cycle | S3, S5 | truly-unknown | blocking | No energy conversion design disclosed |
| 6 | In-vessel coil neutron shielding and lifetime | S3, S4 | truly-unknown | blocking | Critical for maintenance schedule and capacity factor |
| 7 | Capital cost structure (any CAS level) | S5 | truly-unknown | blocking | No published cost data; concept TRL precludes estimation |
| 8 | D-D energy balance (Q, triple product requirement) | S2, S5 | derivable (with assumed confinement) | blocking | Could be estimated with a physics model; requires assumed beta, confinement time |
| 9 | O&M cost structure (fixed/variable, replacement intervals) | S3 | truly-unknown | important | No design basis for O&M modeling |
| 10 | Capacity factor / maintenance interval | S3, S5 | truly-unknown | important | Requires confinement reliability data that does not exist |
| 11 | Magnet type for commercial path (HTS/LTS/other) | S3, S4 | proprietary | important | Company profile implies SC path; no specifics published |
| 12 | D-D vs D-T target design point | S2, S5 | truly-unknown | important | Both are claimed; no quantitative comparison |
| 13 | Neutron wall loading (D-D vs D-T) | S4, S5 | derivable (if plasma power specified) | important | 2.45 MeV vs 14 MeV neutrons; requires fusion power and geometry |

---

## Section 7: Cross-Concept Notes

**Concept family**: PoloMac is an **MFE Dipole** concept. Its two nearest structural neighbors in the analysis portfolio are **12-levitated-dipole** (OpenStar Technologies, D-T) and **19-orbital-levitated-dipole** (Zephyr Fusion, D-He3). Both share the in-vessel superconducting coil structural challenge and the dipole confinement topology; neither has been approved for formal cross-referencing.

One approved prior analysis was available: **21-spherical-tokamak-hts** (Tokamak Energy). The PoloMac is architecturally distant from the spherical tokamak — different confinement topology, different fuel, different coil geometry — so direct assumption reuse is limited. The following notes capture relevant connections:

**Magnet cost context (analogue, not direct reuse)**

If Deutelio eventually specifies REBCO HTS coils for the in-vessel dipole, the supply chain constraints identified in the 01-hts-compact-tokamak exemplar apply: REBCO tape production must scale by 1–2 orders of magnitude from current ~thousands km/year to support a fleet. The in-vessel coil environment (neutron flux, limited access, cryogenic needs) adds constraints beyond what tokamak coil designs face — radiation hardening of HTS insulation is unsolved in any concept.

**Blanket and tritium elimination (divergence)**

The 21-spherical-tokamak-hts analysis treats the tritium breeding blanket (FLiBe, lithium enrichment, breeding ratio management) as a major cost and supply chain driver. For PoloMac's D-D target, this entire subsystem is eliminated. This is a genuine architectural advantage if D-D ignition is achievable — a question that cannot be answered from available data.

**Recirculating power framing (analogue)**

The HTS compact tokamak exemplar uses recirculating power fraction as a key LCOE lever (Q_eng controls plant sizing). For PoloMac, the recirculating power problem is qualitatively different: the 700 MW coil draw is a fixed infrastructure penalty rather than a plasma-physics-determined fraction. Even with superconducting coils, the cryogenic cooling and coil refrigeration loads replace the resistive loss, though at much lower absolute power. The transition from 700 MW resistive loss to ~tens of MW cryogenic load is the critical engineering milestone, but no design for this transition is documented.

**No nearest-neighbor approved analysis available**

The closest conceptual neighbors in the portfolio are both in-progress:

*12-levitated-dipole* (OpenStar Technologies, D-T, iter-3/FAIL) is also dipole-based MFE. Key architectural difference: the levitated dipole uses a magnetically floating (levitated) in-vessel superconducting coil — no physical support — whereas PoloMac uses physically supported coils passing through the plasma via magnetic tunnels. The levitated approach avoids the tunnel-breach problem but introduces magnetic levitation instability and coil retrieval complications. PoloMac's physical support approach is more mechanically robust but requires the tunnel concept to be validated. Both share the unsolved problem of an in-vessel superconducting coil in a neutron environment.

*19-orbital-levitated-dipole* (Zephyr Fusion, D-He3, gap-checked, not yet analyzed) provides a second structural comparator with two additional points of contact. First, the **fuel cycle**: both PoloMac (D-D) and the orbital dipole (D-He3) target aneutronic or reduced-neutron fuels that eliminate the tritium breeding blanket — the same capital cost advantage and the same underlying physics credibility gap (neither D-D nor D-He3 ignition has been demonstrated). Second, the **in-vessel coil challenge**: the orbital dipole uses a meter-scale HTS coil designed to be deployed in orbit (Falcon 9-class vehicle), reflecting the same premise that an in-vessel superconducting coil can survive its environment — in that case, vacuum and radiation; in PoloMac's case, neutron flux and proximity to plasma. The key divergence from PoloMac is the support mechanism: the orbital dipole is magnetically levitated (no physical penetration through the plasma), while PoloMac uses physical magnetic-tunnel supports. Both approaches are at TRL 1–2 and lack any fusion-scale demonstration.

---

## Section 8: Sources

**1. Elio, F. (2014) "Revisiting the poloidal magnetic confinement." *Fusion Engineering and Design*, 89(7–8), pp. 1454–1458. doi:10.1016/j.fusengdes.2014.03.054.**
- **Contribution**: Primary technical source. Establishes the PoloMac magnetic geometry, magnetic tunnel concept, and key quantitative constraint (700 MW copper coil power). Magnetic FEA only — no plasma physics.
- **Path**: `knowledge/concept_research/35-polomac-magnetic-confinement/iter-01/sources/elio-2014-fed-poloidal-confinement.md` (abstract + snippets; full text paywalled)

**2. Elio, F.; Elio, Fr.; Leone, M.; Fulceri, T.; Sborchia, C. (2024) "Technical Report: The Polomac approach to fusion energy." *Journal of Technical and Scientific Publications*. https://www.jtsp.eu/jtsp/article/view/32**
- **Contribution**: Most recent public statement of concept claims. States the D-T field advantage (3× weaker than tokamak), D-D no-blanket claim, and steady-state operation. Development strategy through magnetic tunnel prototype.
- **Path**: `knowledge/concept_research/35-polomac-magnetic-confinement/iter-01/sources/jtsp-2024-polomac-technical-report.md` (abstract only; full text not extracted)

**3. Deutelio AG company profile (extracted 2026-04-04)**
- **Contribution**: Establishes company stage (pre-prototype), 3-stage roadmap, prototype field strength (0.2–0.3 T), Boldbrain placement (4th, 2024), and independent C− tier rating.
- **Path**: `knowledge/concept_research/35-polomac-magnetic-confinement/iter-01/sources/deutelio-company-profile.md`
