# Gap Assessment: Polywell (D-T)

## Overall Readiness
**Rating**: Significant Gaps
**Summary**: The Polywell (D-T) has a recently updated physics scaling model (Park et al. 2025, arXiv:2508.06761) that outlines a credible path to Q=10.5 in a 1.6 m cube device, but no power plant engineering design study exists. The fundamental physics performance parameter (loss reduction factor γ=0.1) is unvalidated experimentally and is an explicitly acknowledged free parameter. Capital cost, thermal conversion, and tritium breeding blanket data are absent entirely. A qualitative concept analysis can proceed with appropriate caveats, but quantitative LCOE estimation requires large analogical extrapolation and must be clearly flagged as speculative.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Partial

**Available**: The Park et al. 2025 paper (`iter-02/sources/polywell-revisited-2025-park.md`) is the primary technical source — a 34-page peer-reviewed preprint from EMC2 team members that presents updated physics models, WB-8 and WB-X experimental results, PIC simulation findings, and a Q=10.5 reactor parameter set (1.6 m cube, 4.5 T, 20 keV, ~980 MW fusion, 78 MW input, γ=0.1). The Park et al. 2015 paper (*Phys. Rev. X 5*, 021024) establishes the WB-X high-beta confinement result as the primary experimental milestone. Wikipedia (`iter-01/sources/polywell-technical-details.md`) provides a comprehensive history of WB-1 through WB-X experiments and the Rider/Nevins critiques. The FPNS talk (`iter-02/sources/emc2-fpns-talk-polywell-2023.md`) provides a near-term device specification (350 kW neutron source, $20M/24-month R&D estimate). The Fusion Report interview confirms EMC2 organizational status and their commercialization pathway via neutron sources. EMC2's website (`iter-01/sources/emc2-website-summary.md`) is minimally informative.

**Missing**: No peer-reviewed power plant engineering design study. No publicly available cost analysis from EMC2. No blanket/shielding engineering. No thermal cycle specification. No published data on electron beam injection experiments at fusion-relevant parameters (M2 and M3 mechanisms only partially validated through PIC simulation). Rogers (2018) reactor design (cited in dossier) was not captured in Phase 1a sources.

**Gaps**:
- No EMC2-published power plant design study — proprietary — blocking
- Rogers (2018) J. Fusion Energy reactor design not extracted — not-yet-sourced — important (would provide independent reactor parameter set)
- Sporer (2022) Michigan reactor analysis not extracted — not-yet-sourced — important (second independent assessment cited in dossier)
- Lynceans/EMC2 "Fork in the Road" (2021) not extracted — not-yet-sourced — nice-to-have

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**: The Park et al. 2025 paper fully documents the three essential Polywell mechanisms (M1: high-beta cusp confinement, M2: electron beam potential well, M3: electrostatic ion confinement) and the physics model built on them. It documents how MIG approach failed (WB-8) and why electron beam injection is the only viable path. PIC simulation results (ECsim, ECsim-CYL) establish the hybrid gyroradius scaling for plasma loss. The loss reduction parametrization (γ=0.1) is explicitly defined and its limitations are acknowledged. The coupling between electron beam power, potential well depth, and Q value is clearly derived (Equations 3–12). The WB-X experiment validating M1 is published. Physics challenges — the non-thermal ion distribution controversy (Rider, Nevins), the start-up power threshold (700 MW pulse needed for WB-X), and numerical instabilities at the boundary layer — are well documented.

**Missing**: The loss reduction factor γ=0.1 is a free parameter with no experimental basis at fusion-relevant conditions. M2 and M3 (potential well formation and synergistic ion loss reduction) have not been experimentally demonstrated at any conditions. The energy conversion pathway is completely absent from all sources (Park et al. 2025 mentions "naturally diverging magnetic fields at plasma-facing surfaces" for thermal management but specifies no thermal cycle). Steady-state high-beta plasma formation and sustainment has not been achieved in any device — WB-X operated for ~5 µs in burst mode with 700 MW pulse power.

**Gaps**:
- Loss reduction factor γ=0.1 is unvalidated — truly-unknown — blocking (the entire Q=10.5 projection rests on this; ±factor of 2 changes the viability conclusion)
- Energy conversion pathway / thermal cycle type — derivable (can assume Rankine ~35% as default for D-T) — important
- Steady-state high-beta plasma demonstration — truly-unknown (next experiment needed) — blocking
- PIC simulation convergence for M2/M3 with realistic mass ratios — truly-unknown (current simulations acknowledge numerical instability for beam injection case) — important

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**: TRL assessments can be drawn from Park et al. 2025 and the WB-X paper. Electron beam injectors: explicitly noted as "off-the-shelf availability of steady-state electron beam injectors in a compact footprint" with MW-class commercial systems available (TRL 7-8 for the injector technology itself). Resistive polyhedral cusp coil assembly: demonstrated through WB-8 (40 cm coil diameter, 0.7 kG) and WB-X (13.8 cm, 0.46 T) — TRL 4-5. High-beta cusp plasma formation: demonstrated in WB-X at ~5 µs burst (TRL 3-4 for pulsed; TRL 2 for steady-state). Potential well formation by electron beams at fusion-relevant density: only PIC simulation support (TRL 2). Tritium handling (generic D-T): mature from fission/ITER programs (TRL 7-8). Thermal conversion (Rankine/steam cycle): fully mature (TRL 9). Plasma diagnostics for Polywell: characterized through WB-8 and WB-X instruments.

**Missing**: Superconducting Polyhedral cusp coils at 4.5 T reactor scale — EMC2 reportedly began SC Polywell work in 2012 but no results published; this is the critical undemonstrated engineering step (TRL 2-3 for reactor-grade SC coil geometry). Start-up system for steady-state operation — WB-X start-up used 700 MW pulsed polypropylene guns (impractical for steady-state); Park et al. 2025 proposes FRC-derived plasmoid translation as a next step (TRL 3-4). Tritium breeding blanket: no design exists for the polyhedral coil geometry — concept-specific engineering challenge (TRL 1-2). First-wall/plasma-facing components under 14 MeV neutron fluence in polyhedral geometry: no design (TRL 1-2). Power recirculation electronics at 78 MW scale: derivable from industrial electron beam technology (TRL 5-6).

**Gaps**:
- Superconducting polyhedral cusp coil at reactor scale (4.5 T steady-state) — not-yet-sourced (engineering design not published) — blocking
- Steady-state plasma start-up system replacing 700 MW pulse guns — truly-unknown — important
- Tritium breeding blanket design for polyhedral geometry (coil-shadowing challenge) — truly-unknown — blocking
- First wall design for 14 MeV neutron environment in polyhedral geometry — not-yet-sourced — important

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**: The resistive copper electromagnets used in all WB-series devices are well characterized and use commercially available materials. Park et al. 2025 specifies 4.5 T steady-state boundary field, which at reactor scale implies superconducting coils (strongly implied but not stated). Boron nitride plasma-facing components (used in WB-8) are commercially available specialized ceramics. Tritium fuel supply constraints are generic to all D-T concepts — same as standard D-T fusion (CANDU-sourced tritium until breeding established). Park et al. 2025 explicitly notes 14.1 MeV neutron production at ~780 MW (80% of ~980 MW) requiring heavy neutron management — standard D-T materials engineering applies.

**Missing**: No materials specification for a reactor-grade device. Superconducting coil material choice (HTS vs LTS) is unspecified — at 4.5 T, LTS (NbTi or Nb₃Sn) is feasible but HTS enables higher-field compact variants. Blanket material not specified (Li-ceramic, FLiBe, or other). First wall material under ~3 MW/m² neutron wall load (estimated from ~780 MW over polyhedral surface area) — tungsten or SiC/SiC composites by analogy. The polyhedral coil geometry creates unique mechanical support and tritium-breeding-blanket placement challenges not addressed in any source.

**Gaps**:
- Superconducting coil material/supplier selection for reactor — derivable (follow HTS developments in CFS/Commonwealth or LTS ITER supply chain) — important
- Blanket material and geometry — not-yet-sourced / truly-unknown — blocking
- Neutron wall load quantification and first wall material — derivable from Park et al. 2025 parameters — important
- No concept-specific supply chain bottleneck identified beyond generic D-T constraints — nice-to-have

---

### 5. LCOE Parameter Extraction
**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Fusion power output | ~980 MW | Park et al. 2025 (`iter-02/sources/polywell-revisited-2025-park.md`) | m (depends on γ=0.1) |
| Q value | 10.5 | Park et al. 2025 | l (free parameter γ) |
| Recirculating input power | 78 MW (60 keV, 1.3 kA e-beams) | Park et al. 2025 | m |
| Plasma temperature | 20 keV | Park et al. 2025 | m |
| Plasma density | 1.3×10²¹ /m³ | Park et al. 2025 | m |
| Magnetic field (boundary) | 4.5 T | Park et al. 2025 | m |
| Device scale | 1.6 m cube per module | Park et al. 2025 | m |
| Bremsstrahlung loss | 15.5 MW | Park et al. 2025 | m |
| D-T fuel mix | 50:50 | Park et al. 2025 | h |
| Neutron power fraction | ~80% (~780 MW) | General D-T physics | h |
| Net electricity output | ~derivable at ~35% η → ~315 MWe gross, minus 78 MW recirc | Derivable | l |
| LCOE analog (compact D-T, ~500 MWe) | $34–54/MWh (average $43) | ARPA-E ALPHA revisit (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) | l (analog only; Polywell not among the 4 concepts) |
| CapEx analog (compact D-T, ~500 MWe) | ~$2.4/W, ~$1.2B total | ARPA-E ALPHA revisit | l (analog) |
| LCOE analog (D-T MFE tokamak, 500 MWe) | $140–550/MWh | TEA D-T MFE (`knowledge/sources/tea_dt_mfe_cost_analysis/`) | l (tokamak analog, different architecture) |
| FPNS device R&D cost | $20M / 24 months | FPNS talk (`iter-02/sources/emc2-fpns-talk-polywell-2023.md`) | m (near-term device, not power plant) |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost by CAS subsystem | proprietary / not-yet-sourced | blocking | No plant engineering design; no analogue study covers Polywell specifically |
| Thermal conversion efficiency (η_th) | derivable | important | No thermal cycle specified; Rankine ~33-38% assumed by default for D-T |
| Capacity factor | derivable | important | Park et al. 2025 asserts "high facility availability factor" from intrinsic plasma stability; no quantitative assumption |
| O&M cost | not-yet-sourced | important | No design basis; modular coil geometry may reduce maintenance cost (Park 2025 notes "easily assembled and disassembled") |
| Number of modules per plant | truly-unknown | important | No multi-module plant study; ARPA-E ALPHA used 2–4 modules for ~500 MWe |
| Tritium breeding ratio and cost | truly-unknown | blocking | No blanket design; unique polyhedral geometry creates coil-shadowing engineering challenge |
| First wall / blanket capital cost | truly-unknown | blocking | No geometry-specific design; standard D-T analog inapplicable without polyhedral blanket design |
| Loss factor γ validation | truly-unknown | blocking | Entire Q=10.5 projection rests on γ=0.1; ±factor 2 changes plant output by 2× |
| SC coil system cost | not-yet-sourced | important | 4.5 T steady-state implied; non-interlocking polyhedral geometry distinct from tokamak/stellarator |

---

## Source Recommendations

1. **Rogers (2018), "A Polywell Fusion Reactor Designed for Net Power Generation," *J. Fusion Energy* 37:1–17** — not-yet-sourced — important. Would provide an independent reactor parameter set and potentially cost/scaling analysis. Search: DOI 10.1007/s10894-017-0147-9. Confirm existence before searching — cited in dossier with full citation.

2. **Sporer (2022), "Analysis of Two Fusion Reactor Designs Based on Magnetic Electrostatic Plasma Confinement," University of Michigan** — not-yet-sourced — important. University thesis on Polywell and Lockheed CFR costing analysis. URL cited in dossier: plasmabay.engin.umich.edu. Confirm availability.

3. **Lynceans/EMC2, "The Fork in the Road to Electric Power From Fusion" (2021)** — not-yet-sourced — nice-to-have. EMC2-authored document on pathway; URL in dossier. May contain cost/commercial pathway discussion.

4. **Search OSTI for Polywell cost analysis / EMC2 DOD contract reports** — not-yet-sourced — important. The US Navy contract (N68936-09-0125, 2009–2015) likely generated classified or FOUO technical reports; unclassified portions may be findable via OSTI. Search: "Polywell" OR "WB-8" OR "WB-X" on osti.gov. `unverified — confirm existence before searching`

5. **Bussard scaling paper (IAC 2006 presentation)** — not-yet-sourced — nice-to-have. The original power scaling estimates (r⁷ fusion power scaling) are referenced but not extracted; would help document the claimed scaling basis.

**Fleet-wide source integration notes**:

- **ARPA-E ALPHA Revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): Integrated as LCOE analog for compact D-T fusion. Four concepts (Plasma-Jet MIF, Stabilized Liner Compressor, Staged Z-Pinch, Flow-Z-Pinch) are not Polywell, but they share the compact modular D-T architecture. The $34–54/MWh LCOE range and ~$2.4/W CapEx serve as a rough lower-bound analog. This downgrades the "overall LCOE estimate" gap from blocking to important for a rough order-of-magnitude estimate; it remains blocking for a subsystem-level CAS breakdown. The CAS framework (accounts 20–26) from this source is directly applicable to Polywell costing methodology.

- **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): Integrated as methodology analog. The COA structure (Account 22: reactor plant equipment including blanket, magnets, tritium handling; Account 23: Rankine turbine; Account 26: heat rejection) is applicable to Polywell's D-T BOP. The $140–550/MWh tokamak LCOE range is a conservative upper-bound analog. This source provides the thermal conversion assumption (Rankine cycle) that Park et al. 2025 leaves unspecified, downgrading the thermal cycle gap from blocking to important (can assume as default).

- **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`): Provides the historical CAS framework (accounts 20–27 direct, 90–98 indirect) applicable as a costing scaffold for any fusion power plant concept. Does not provide Polywell-specific values. Disqualified for providing concept-specific cost values, but confirmed as the methodological reference for constructing CAS estimates.

- **Progress toward fusion energy breakeven** (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`): The paper explicitly notes that the standard Lawson analysis does not apply to non-thermal plasma approaches (Section II and footnote on non-Maxwellian systems). The Polywell's non-thermal ion confinement hypothesis is outside the scope of the Wurzel/Hsu compilation. No Polywell data points appear in the Lawson parameter plots — the WB-X result demonstrated high-beta confinement but no meaningful Lawson parameter (Q~0). This is confirmed physics context: Polywell's Q=10.5 projection cannot be benchmarked against the Lawson compilation. Disqualified as a source for physics benchmark data for the Polywell; it instead confirms that Polywell's physics progress cannot be straightforwardly compared to tokamaks/ICF using the standard metric.

- **Economic studies for heavy-ion-fusion** — Disqualified: IFE driver economics (pulse rate, driver cost) are irrelevant to Polywell's steady-state electrostatic concept. Did not read.

- **A simplified economic model for inertial fusion** — Disqualified: IFE-specific (gain per shot, rep rate, target factory). Not applicable to steady-state Polywell. Did not read.

- **Energy from Inertial Fusion** — Disqualified: 1992 IFE review, not applicable. Did not read.

- **Accelerators for Inertial Fusion Energy Production** — Disqualified: IFE driver accelerator technology, not applicable. Did not read.

- **Affordable, manageable, practical and scalable (AMPS) high-yield inertial fusion** — Disqualified: IFE pulser-driven, not applicable. Did not read.

- **Commercialization of laser fusion energy** — Disqualified: laser IFE, not applicable. Did not read.

- **Overview of the Helios Design (stellarator)** — Disqualified: MFE stellarator, different confinement family. Did not read.

- **An Assessment of the Economics of Future Electric Power Generation Options (ORNL)** — Disqualified for concept-specific use: historical ORNL benchmark provides only a LCOE target band for fusion vs. competing generation, not Polywell-specific costs. The ARPA-E ALPHA revisit already provides a more relevant compact fusion LCOE anchor. Did not read.

---

## Summary

**Proceed to full analysis, with significant caveats.** The Polywell (D-T) has sufficient physics literature (primarily Park et al. 2025) to support a qualitative and partially quantitative D1+ analysis covering concept function, physics basis, experimental history, TRL assessment per subsystem, and general materials considerations. The analysis should prominently caveat that: (1) the Q=10.5 reactor projection is built on an unvalidated free parameter (γ=0.1); (2) no power plant engineering design exists; (3) LCOE estimates can only be made by analogy to compact D-T concepts (ARPA-E ALPHA range: $34–54/MWh) and should not be treated as concept-specific numbers. The three blocking LCOE gaps (capital cost structure, tritium breeding, γ validation) mean that only a rough order-of-magnitude LCOE placeholder is possible, not a defensible TEA estimate. Acquiring the Rogers (2018) and Sporer (2022) papers before final LCOE modeling would meaningfully reduce this uncertainty.

---

## Structured summary (machine-readable)

```yaml
overall_rating: "Significant Gaps"
blocking_count: 4
important_count: 7
counting_method: "all_sections_deduplicated — 4 blocking: (1) capital cost by CAS subsystem, (2) loss reduction factor gamma validation, (3) tritium breeding blanket design, (4) superconducting coil at reactor scale / steady-state high-beta demonstration (merged as one blocking gap on maturity); 7 important: thermal conversion efficiency, capacity factor, O&M cost, module count per plant, first wall/blanket materials, steady-state start-up system, SC coil material selection"
section_coverage:
  availability_of_data:       "Partial"
  system_function:            "Partial"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Poor"
```