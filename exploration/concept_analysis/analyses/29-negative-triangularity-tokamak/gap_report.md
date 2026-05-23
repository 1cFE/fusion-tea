# Gap Assessment: Negative Triangularity Tokamak (D-T)

## Overall Readiness
**Rating**: Mostly Ready
**Summary**: The concept is anchored by the MANTA reference design (Rutherford et al. 2024), a comprehensive published pilot plant study covering plasma physics, magnets, blanket, balance of plant, and economics. NT confinement physics is experimentally validated at DIII-D, TCV, and ASDEX Upgrade. The TEA D-T MFE cost analysis (Araiinejad & Shirvan 2025) provides a closely analogous NOAK cost framework. The primary limitation is that Firefly Fusion itself has published almost nothing — MANTA is an MIT/Columbia academic study, not Firefly's design — and the concept's commercial-scale economics remain far from competitive based on current extrapolations ($396/MWh for a scaled MANTA). A D1+ analysis is feasible using MANTA as the design proxy with explicitly stated assumptions, but cannot be attributed to Firefly specifically.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Partial

**Available**:
- CEO interview (GreyB/Scouted, `iter-01/sources/greyb-firefly-interview.md`): R=2–2.5 m, B=10–12 T, Q>5, P_fus=50–100 MW, HTS magnets commercial target
- DIII-D collaboration page (`iter-01/sources/firefly-fusion-diii-d-collaboration.md`): confirms LUCIOLE prototype with copper magnets, NT focus, DIII-D experimental partnership
- MANTA reference design (`iter-02/sources/manta-reference-design.md`): the most detailed NT tokamak pilot plant study published to date — full plasma parameters, magnet design, FLiBe blanket, ICRF heating, steam Rankine cycle, $3.4B overnight cost, Table 1 key parameters
- Balestri, Ball & Coda 2024 (`iter-01/sources/ball-balestri-ohmic-nt-paper.md`): physics basis for ohmic-only NT operation; applies MANTA, SPARC, ITER, DEMO to 0D power balance
- Vertical stability study (abstract, `iter-04/sources/arxiv-2401-15217.md`): confirms NT is less vertically stable than PT; passive stabilizing plates mitigate growth rates to ~16% of baseline
- NT EM system pre-conceptual design (abstract, `iter-04/sources/arxiv-2501-14682.md`): R₀=1m, 3T copper NT tokamak EM design using TokaMaker — relevant to Firefly's LUCIOLE scale
- Maintenance economics (abstract, `iter-04/sources/arxiv-2405-01514.md`): value of fusion plant maintenance strategies in decarbonized 2050 US grid; seasonal scheduling can increase plant value 15%
- ARIES ACT studies (`iter-04/sources/osti-servlets-purl-1127358.md`, `osti-servlets-purl-1178069.md`): advanced/conservative PT tokamak designs at ~1000 MWe scale; provide tokamak cost methodology and BOP analog
- ARIES cost account documentation (`iter-04/sources/qedfusion-lib-report-aries-act-ucsd-cer-13-01.md`): full CAS framework (accounts 20–27 direct, 90–98 indirect) from Starfire through ARIES series

**Missing**:
- Any Firefly publication on LUCIOLE design parameters (geometry, plasma performance targets, heating systems, blanket approach)
- Firefly conference presentations or FIA white paper with technical content
- Dedicated NT tokamak commercial plant study (MANTA is a pilot plant, not a commercial design)

**Gaps**:
- Firefly design parameters beyond CEO-level ballparks — proprietary — important
- NT tokamak pilot-to-commercial extrapolation relies on a single major published study (MANTA) — not-yet-sourced — important

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- NT L-mode-enhanced confinement mechanism is well-described: H98~1.44 achieved in MANTA integrated modeling (TGYRO + TGLF + CHEASE + UEDGE workflow); experimental validation shows H98~1.0 achievable on TCV and DIII-D (`manta-reference-design.md` §2, §Appendix B)
- Ballestri et al. demonstrate ohmic operation feasibility at MANTA/SPARC parameters (Q~500 Ohmic vs Q~30 with 40MW heating) (`ball-balestri-ohmic-nt-paper.md`)
- Divertor challenge quantified: MANTA achieves peak heat flux 2.8 MW/m² via ELM-free + impurity seeding (Kr) + NT geometry placing divertor at larger major radius; M₂ metric 10–20× lower than EU-DEMO (`manta-reference-design.md` §3, Table 2)
- FLiBe liquid immersion blanket integration with demountable TF coils described (`manta-reference-design.md` §5); conformal VV with FLiBe channels used to cool divertor targets
- Vertical stability challenge identified and mitigation via passive stabilizers demonstrated (abstract, `arxiv-2401-15217.md`)

**Missing**:
- Experimental demonstration of ELM-free NT operation at burning plasma parameters (nτT approaching NT pilot plant targets) — current NT experiments are far below fusion conditions
- NT-specific system code modeling: standard tokamak system codes (PROCESS, BLUEPRINT) use H-mode assumptions and may not handle NT L-mode operation correctly
- MANTA's integrated modeling uses full-physics codes (TGYRO, TGLF) — no simplified system-code-level model of NT exists for fast LCOE sensitivity scans
- Confinement degradation with impurity seeding in NT: MANTA assumes Kr seeding compatible with L-mode transport, but experimental basis is limited

**Gaps**:
- NT confinement scaling uncertainty at reactor-relevant parameters (H98 enhancement factors from TCV/DIII-D may not extrapolate to burning plasma regimes) — derivable with stated uncertainty — important
- Absence of NT-compatible system code (standard codes assume H-mode) prevents rapid parameter scans needed for cost sensitivity — truly-unknown (no NT system code yet published) — important
- Vertical stability solutions engineering at pilot-plant scale — not-yet-sourced (full paper exists but only abstract captured) — important

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **REBCO HTS TF coils (TRL 5–6)**: SPARC TFMC demonstrated 20 T at CFS; MANTA uses 11 T on-axis, well within REBCO demonstrated range. MANTA TF coil design detailed (non-insulated wound, window-pane geometry, 18 coils, max von Mises stress 600 MPa) (`manta-reference-design.md` §4)
- **ICRF heating (TRL 7–8)**: 40 MW at 110 MHz (existing high-power tetrodes); He-3 minority species. MANTA design cites frequency achievable with existing technology (`manta-reference-design.md` §2.2.1)
- **FLiBe blanket (TRL 2–3)**: liquid immersion blanket design detailed; TBR=1.15, blanket power multiplication 1.11; FLiBe chemistry management (MoF₆ dissolved for self-healing Mo barrier) specified; no reactor-scale FLiBe blanket has operated (`manta-reference-design.md` §5)
- **Tungsten first wall (TRL 7)**: 0.3 cm W PFCs described; UEDGE-predicted sputtering rate 0.0016 mm/yr from 0.315% Ne (`manta-reference-design.md` §3.1–3.2)
- **V-4Cr-4Ti vacuum vessel (TRL 3–4)**: activation 3 orders of magnitude lower than SS316LN; DPA tolerance estimated but requires experimental validation (`manta-reference-design.md` §5.3); 2 DPA/100 MW-yr average
- **Steam Rankine cycle (TRL 9)**: two-stage molten-salt heat exchange loop; standard technology selected over Brayton/supercritical Rankine (`manta-reference-design.md` §6)
- **Central solenoid (TRL 5)**: REBCO PIT-VIPER-like cables; insulated for low AC losses; PF2 minimum lifetime 890 MW-yr (~2 full-power years at 450 MW) (`manta-reference-design.md` §4.3, Table 7)

**Missing**:
- TRL of NT plasma control algorithms at pilot plant scale — LUCIOLE will validate this but doesn't exist yet
- Tritium fuel cycle maturity: MANTA models startup inventory 440g, reserve 75g; notes fuel cycle is "not fully developed or tested" (`manta-reference-design.md` §5.4); TRL 2–3 for fusion-scale tritium processing

**Gaps**:
- REBCO tape production at commercial scale (5730 km cables per ARC-class device per TEA D-T MFE cost analysis, `knowledge/sources/tea_dt_mfe_cost_analysis/output.md`) — not-yet-sourced — important
- FLiBe blanket first-of-a-kind risk: no operating precedent for molten salt lithium-beryllium blanket in fusion environment — truly-unknown (reactor-scale data doesn't exist) — important
- Tritium fuel cycle full integration at pilot plant scale — truly-unknown — important

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- **REBCO tape cost**: MANTA TF coil cost $1.5B (~44% of total overnight cost $3.4B); sensitivity: ±50% REBCO cost → ±25% overnight cost, remaining under $5B limit (`manta-reference-design.md` §7.1, Fig. 25)
- TEA D-T MFE cost analysis identifies 5730 km REBCO cable per ARC-class device; REBCO material is the single largest cost uncertainty (`knowledge/sources/tea_dt_mfe_cost_analysis/output.md` §2.2.1)
- **FLiBe**: MANTA uses FLiBe as both blanket and primary coolant; cost included in sensitivity analysis; Be supply is a concern (US strategic material)
- **Tungsten**: commercially available; W sputtering in MANTA divertor modeled as negligible (0.0016 mm/yr)
- **V-4Cr-4Ti**: MANTA identifies as low-activation VV material; limited industrial production capacity currently

**Missing**:
- REBCO production trajectory: current global capacity vs. demand from multiple ARC-class devices
- Beryllium supply chain: FLiBe contains Be; US Be reserves at Spor Mountain (Utah) are the dominant global source; strategic material with export controls
- Li-6 enrichment for tritium breeding: TBR=1.15 based on natural Li; enriched Li-6 would reduce blanket volume but requires isotope separation capacity

**Gaps**:
- REBCO supply chain bottleneck quantification for commercial deployment — not-yet-sourced — important
- Beryllium supply constraints for FLiBe blanket at scale — not-yet-sourced — important
- Li-6 enrichment supply chain — not-yet-sourced — nice-to-have

---

### 5. LCOE Parameter Extraction
**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Fusion power | 450 MW (MANTA proxy); 50–100 MW (Firefly target) | `manta-reference-design.md` Table 1; GreyB interview | m |
| Net electric power | 90 MWe (MANTA pilot) | `manta-reference-design.md` Table 1 | m |
| Electricity gain Q_E | 2.4 | `manta-reference-design.md` Table 1 | m |
| Plasma gain Q | 11.5 | `manta-reference-design.md` Table 1 | m |
| Thermal power | 530 MW total (MANTA) | `manta-reference-design.md` Table 1 | m |
| ICRF heating power | 40 MW at 110 MHz | `manta-reference-design.md` §2.2.1 | m |
| Overnight cost (pilot) | $3.4B (~$38M/MWe) | `manta-reference-design.md` §7.1 | m |
| Overnight cost (NOAK ARC-class) | $8,800–$22,200/kW for 350 MWe | `knowledge/sources/tea_dt_mfe_cost_analysis/output.md` | m |
| TF coil cost (dominant) | $1.5B (~44% of overnight) | `manta-reference-design.md` §7.1, Fig. 24 | m |
| LCOE (MANTA scaled to 550 MW, 30 yr) | $396/MWh | `manta-reference-design.md` §7.2 | l |
| LCOE analog (NOAK D-T MC tokamak) | $140–$550/MWh | `knowledge/sources/tea_dt_mfe_cost_analysis/output.md` | m |
| TF coil lifetime | 3,100±400 MW-yr (~7 yr at 450 MW) | `manta-reference-design.md` Table 7 | m |
| PF2 coil lifetime (binding) | 890±40 MW-yr (~2 full-power yr) | `manta-reference-design.md` Table 7 | m |
| Energy conversion cycle | Steam Rankine (two-stage molten salt) | `manta-reference-design.md` §6 | m |
| Tritium breeding ratio | 1.15 (min needed: 1.02) | `manta-reference-design.md` §5, Table 9 | m |
| Tritium startup inventory | 440g | `manta-reference-design.md` §5.4 | m |
| Major radius (MANTA) | 4.55 m | `manta-reference-design.md` Table 1 | h |
| Toroidal field on axis | 11 T | `manta-reference-design.md` Table 1 | h |
| Plasma current | 10 MA | `manta-reference-design.md` Table 1 | h |
| Pulse length | ~15 min inductive | `manta-reference-design.md` Table 1 | h |
| Inter-pulse length | ~2 min | `manta-reference-design.md` Table 1 | h |
| Bootstrap fraction | 18% | `manta-reference-design.md` Table 1 | m |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Thermal efficiency (cycle) | derivable | important | MANTA uses sub-critical Rankine; efficiency not explicitly stated. FLiBe outlet temperature limits cycle performance. Estimated ~25% gross; MANTA Q_E=2.4 implies ~17% net efficiency (P_net=90 / P_th=530). High-temperature Rankine or Brayton could reach 45–58% (ARIES ACT SiC/Brayton). |
| Capacity factor (commercial) | derivable | important | MANTA pilot plant limited by PF2 replacement every ~2 full-power years. Commercial plant would require extended PF lifetimes or modular replacement. No formal availability study published for NT pilot plant. |
| O&M costs (annual, commercial) | derivable | important | MANTA reports 8.5-year gross loss of $512M; magnet replacement dominates. NOAK O&M not independently estimated in any source. |
| Heating system cost breakdown | proprietary | important | MANTA ICRF 40 MW cost not itemized separately in available economic tables. Three competing hypotheses for Firefly (ECRH vs. ICRH vs. ohmic). |
| Firefly-target-scale plant economics | proprietary | important | Firefly targets R≈2–2.5m, P_fus=50–100 MW — significantly smaller than MANTA (R=4.55m, 450 MW). Direct cost scaling to smaller NT tokamak not published. |
| Decommissioning cost estimate | not-yet-sourced | nice-to-have | MANTA assumes brownfield site saving ~$400M; decommissioning cost not explicitly calculated. ARIES CAS accounts 90-98 cover this category. |
| Fuel costs (D-T acquisition) | derivable | nice-to-have | Tritium startup inventory 440g at ~$30,000/g → ~$13M; ongoing T² production (MANTA generates 1.8 kg/yr net excess). D costs negligible. |

---

## Source Recommendations

- **NT confinement scaling at reactor parameters**: The MANTA paper (`iter-02/sources/manta-reference-design.md`) cites Wilson et al. 2024 ("Characterizing the negative triangularity reactor core operating space with integrated modeling," *PPCF*) — this paper provides integrated modeling validation of NT operating space but was not ingested. Search OSTI/arXiv for NT TGYRO/integrated modeling papers from Columbia/MIT group. `unverified — confirm existence before searching`
- **Capacity factor and availability modeling**: Schwartz et al. 2024 (`iter-04/sources/arxiv-2405-01514.md`) addresses maintenance economics for fusion plants — the full paper was not read (only abstract). Ingest full paper for seasonal availability and maintenance strategy quantification.
- **REBCO supply chain**: Fusion Industry Association supply chain reports (annual) or CFS/REBCO manufacturer supply agreements would provide production capacity data. Search FIA.org for supply chain working group outputs. `unverified — confirm existence before searching`
- **NT system code**: No NT-compatible systems code appears to exist in the literature yet. This is a genuine modeling gap. The Firefly/MANTA approach requires case-by-case integrated modeling (TGYRO-class), which is computationally expensive. Flag this clearly in the analysis.
- **Beryllium supply constraints for FLiBe**: IAEA documents on Be availability and IFE literature (energy_from_inertial_fusion has Be target discussion) provide partial analog; a formal FLiBe supply chain study for fusion does not appear to exist publicly.
- **ARIES ACT cost data for BOP analog**: The two OSTI ARIES ACT sources (`osti-servlets-purl-1127358.md`, `osti-servlets-purl-1178069.md`) were read and are applicable for BOP and indirect cost structure. These are PT tokamaks at 1000 MWe scale with Nb3Sn magnets — different architecture — but turbine plant (CAS 23), electrical plant (CAS 24), and site structure (CAS 21) costs are transferable analogs. Explicitly disqualified as direct reactor core cost analog due to different scale, magnet technology (Nb3Sn vs. REBCO), and plasma regime (H-mode vs. NT L-mode).
- **ARPA-E ALPHA revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/output.md`): Read. Reports ~$43/MWh LCOE for ~500 MWe modular non-tokamak concepts (FRC, MTF, Z-pinch) under CAS framework. Not applicable as a direct tokamak cost analog — architectures differ fundamentally, and the $43/MWh optimistic figure targets commercial-scale modular concepts with very different cost structures. Disqualified as direct LCOE analog for NT tokamak pilot plant.
- **Progress toward fusion breakeven (Wurzel & Hsu)** (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/output.md`): Read. Provides TRL context for NT tokamak concept: tokamak MCF has the highest demonstrated nτT values, approaching burning plasma threshold. NT-specific data is not broken out separately from tokamak MCF (TCV/DIII-D NT plasmas are at far lower nτT than JET/ITER/SPARC targets). Useful for §3 TRL framing — confirms that NT physics at burning plasma scale is extrapolated, not demonstrated. Integrated into TRL assessments above.

---

## Summary

**Proceed to full analysis.** The MANTA reference design provides sufficient coverage to produce a high-quality D1+ analysis of the negative triangularity tokamak concept with MANTA as the explicit proxy design. The analysis should:
1. Clearly distinguish Firefly Fusion (early-stage company, no published design) from the MANTA academic pilot plant study that serves as the NT tokamak reference
2. Use the TEA D-T MFE cost analysis (Araiinejad & Shirvan 2025) for NOAK cost scaling ($140–$550/MWh LCOE range, $8,800–$22,200/kW capital) — this is the best available NOAK economic framework for an ARC-class REBCO D-T tokamak
3. Flag the NT system-code gap explicitly: standard tokamak system codes assume H-mode, not NT L-mode; cost sensitivity scans require either code adaptation or direct use of MANTA/Balestri 0D power balance
4. Note that current pilot plant economics ($396/MWh scaled-up MANTA) are far from competitive, and identify the specific engineering improvements needed (extended magnet lifetimes, higher beta, high-temperature cycle) that MANTA itself quantifies

---

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready"
blocking_count: 0
important_count: 9
counting_method: "deduplicated across all five sections: (1) NT tokamak pilot-to-commercial extrapolation limited to single study, (2) NT confinement scaling at reactor parameters, (3) NT system code absence, (4) vertical stability engineering at pilot-plant scale, (5) REBCO supply chain bottleneck, (6) FLiBe blanket TRL and operating precedent, (7) tritium fuel cycle TRL, (8) commercial-scale capacity factor, (9) Firefly-specific reactor design parameters"
section_coverage:
  availability_of_data:       "Partial"
  system_function:            "Partial"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Partial"
```