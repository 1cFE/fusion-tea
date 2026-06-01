## Design Point

- Name: ARC 2015 Conservative Pilot phase (Sorbom et al.)
- Maturity: paper-concept
- P_native: 233 MWe
- Grounding: high
- Primary sources:
  - knowledge/concept_research/01-hts-compact-tokamak/iter-03/sources/arc-reactor-specifications.md
  - knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/arc-power-conversion-studies.md

---

## Section 1: Availability of Data

**Rating: Rich**

The HTS compact tokamak is, with the exception of large public-program tokamaks (ITER, DEMO), the best-documented private-sector fusion concept in the corpus, and the named design point — the **ARC 2015 "Conservative Pilot" phase** — is anchored to a single, unusually complete peer-reviewed conceptual design study. Sorbom et al. (2015), "ARC: a compact, high-field, fusion nuclear science facility and demonstration power plant with demountable magnets," publishes a closed plasma parameter set, a full radial build, a neutronics-derived blanket design, a magnet conductor design, and — critically for techno-economic work — a **rough materials-and-fabrication cost breakdown by subsystem in FY2014 dollars** [arc-reactor-specifications.md §6, Tables 10–11]. Very few concepts in this investigation publish any internal cost numbers; ARC publishes a subsystem-level cost table.

> "While a full costing of the ARC reactor is beyond the scope of this paper, a rough scaling based on volumes and materials prices has been performed."
> — arc-reactor-specifications.md §6 (Economics)

**Design-point-specific documentation.** The 233 MWe figure is not an analyst inference — it is the explicit net electric output of the "conservative Pilot phase" of the ARC R&D ladder:

> "In the conservative Pilot phase, the blanket outlet temperature is set at 1100 K, for a Brayton cycle efficiency of ∼46%, resulting in *Pnet* = 233 MW and *Qe* = 3.5."
> — arc-reactor-specifications.md §2

This phase shares the *same machine hardware* as the FNSF (190 MWe) and aggressive-Pilot (261 MWe) phases; the three differ only in blanket outlet temperature and therefore thermal efficiency. This means the published hardware cost table applies directly to the 233 MWe design point.

**Supporting and corroborating literature.**
- Power-conversion balance-of-plant: Colliva et al. (SSRN-4482183) independently modeled three cycles (supercritical steam Rankine, sCO₂ Brayton, He Brayton) for the ARC FNSF balance of plant, recommending the steam Rankine cycle (~46% net) and confirming the need for a molten-salt energy-storage system to buffer pulse/dwell operation [arc-power-conversion-studies.md §1–3].
- Heating system: Lin, Wright & Wukitch (J. Plasma Phys.) give the ICRF physics basis for SPARC, explicitly developed under CFS funding "for subsequent use in ARC-class devices," fixing antenna count, frequency (~120 MHz for SPARC; 50 MHz fast wave for ARC), and per-strap power handling [sparc-icrf-heating-paper.md].
- Costing methodology: Woodruff Scientific's pyFECONS framework (arXiv 2601.21724) and its CATF extension (arXiv 2602.19389) supply the GEN-IV/ARPA-E cost-account structure used by this pipeline, the magnet cost methodology (Account 22.1.3 as the dominant MFE driver), and anchor figures (O&M ≈ 60 $/kWe-yr; deuterium ≈ $2,175/kg) [arxiv-2601-21724.md §5–6].
- Comparator economics: ARIES-AT (Najmabadi et al., OSTI 20261446) provides a national-program advanced-tokamak point design with a 5 c/kWh COE and full machine parameters; Woodruff's ARPA-E ALPHA re-costing (OSTI 1820946) and the maintenance-value study of Schwartz et al. (arXiv 2405.01514) supply CAS-level and O&M/availability methodology.

**Company transparency.** CFS (founded 2018, MIT spin-out) publishes roadmap milestones, the 2021 20 T magnet demonstration, and SPARC construction progress, but has **not** published a commercial cost breakdown for the current 400 MWe ARC. The authoritative cost data is therefore the 2015 academic paper, not a company disclosure — a point that matters for interpreting the override candidates below (they are *published-figure*-grounded, not *company-disclosure*-grounded).

**Key data gaps.** (1) The divertor was explicitly "left as an open question" in the 2015 design — only a rough $17.5M placeholder exists [§6.3]. (2) The consolidated parameter table (Table 1) survives in the source only as a non-OCR'd image, so a few aggregate values (gross electric, core thermal power) are recovered from body text rather than the master table. (3) No FY2014→present escalation is provided by the source; CPI adjustment is the analyst's. (4) The current commercial ARC (400 MWe, Virginia) is a *different, larger* design point than the one selected here (see Section 2).

---

## Section 2: Challenges in Capturing System Function

Ranked by impact on the LCOE model.

**1. The magnet account is structure-dominated, not conductor-dominated (Impact: Critical).** The single most important — and most counter-intuitive — feature of ARC's cost structure is that the confinement-magnet cost is overwhelmingly *structural steel to react the magnetic forces of a 23 T peak field*, not the REBCO conductor. In the published breakdown the magnet/structure subtotal is **$5.1–5.2B fabricated**, of which the 4,350-tonne SS316LN structure alone is **$4.6B**, while all the REBCO tape is only **$100–210M** and the copper winding structure $380M [§6, Table 11]. A naïve cost model that prices HTS magnets from conductor length × $/kA-m will undercount the ARC magnet by roughly an order of magnitude. This is the central modeling hazard for the whole archetype and the principal justification for an explicit C220103 override.

**2. Design-point vs. current-program power mismatch (Impact: High, interpretive).** The fixed selection is the **2015 Sorbom 233 MWe** paper design. The *current* CFS commercial ARC is a **400 MWe** plant sited outside Richmond, Virginia, slated for the early 2030s, backed by Google/Eni/Nvidia PPAs [cfs-2025-2026-updates.md]. These are different machines (the commercial ARC has grown in both size and power and its detailed parameters are unpublished). Per the analysis contract, all Section 5 parameters describe the **233 MWe 2015 design point**; the 400 MWe program data is recorded here only to flag the contradiction and is *not* propagated into the design-point parameters or overrides. Any reader scaling this concept to its commercial pitch must treat the 400 MWe plant as out-of-scope for this dossier.

**3. Capacity-factor / component-replacement uncertainty (Impact: High).** As for all D-T tokamaks, availability is the highest-elasticity LCOE lever, and it is gated by unproven first-wall/blanket/divertor replacement cadence under 14 MeV neutron damage. ARC's design choice is distinctive and partially favorable: the FLiBe *liquid immersion* blanket plus demountable TF joints makes the entire vacuum vessel a "plug-and-play" replaceable module, with the blanket tank as the lifetime component [§3.6, §2]. This could shorten replacement outages relative to segmented solid-blanket machines — but no replacement *interval* or outage *duration* is published, so the benefit cannot be quantified. Schwartz et al. (2405.01514) show that scheduled maintenance scheduled into low-price seasons costs far less value than a flat capacity-factor penalty implies ("a plant at 80% availability with annual maintenance retains 91% of the value of a maintenance-free plant"), which argues for modeling this as scheduled FO&M rather than a flat de-rate.

**4. O&M cost structure (Impact: Moderate, and a known systematic gap).** No bottoms-up O&M breakdown (fixed vs. variable staffing, scheduled component replacement, tritium handling labor) exists for ARC. The defensible default is the pyFECONS staffing-based factor of ~60 $/kWe-yr (CAS70), giving ≈ $14M/yr at 233 MWe net, plus a scheduled blanket/first-wall replacement charge. This is a library-owned default, not an override, but it is flagged here because the absence of concept-specific O&M data is a guaranteed analytical gap.

**5. Thermal-conversion efficiency is phase-dependent and material-limited (Impact: Moderate).** The 233 MWe point assumes a 1100 K blanket outlet and ~46% Brayton efficiency — but this requires "an evolution to higher temperature materials informed by the FNSF stage" [§2]; the demonstrated-material FNSF phase yields only 190 MWe at ~40%. The thermal efficiency is thus an *aspiration contingent on materials R&D*, not a demonstrated value, and should be carried as a sensitivity parameter (η_th 40–50%) rather than a fixed input.

**6. Divertor is undesigned (Impact: Moderate).** The 2015 paper explicitly defers the divertor ("the physical divertor design was left for later study"), pricing only a $17.5M rough tungsten placeholder [§5.1, §6.3]. Heat-flux scaling places ARC's divertor difficulty "between ITER and reactor designs." This is a genuine cost-and-feasibility unknown carried as a data gap.

**7. Regulatory cost burden (Impact: Moderate, shared).** As for all D-T concepts, Stewart & Shirvan's 2.2× building-cost multiplier under fission-style regulation (cited in the handwritten exemplar) is an upper-bound scenario, unresolved pending NRC Part-30 rulemaking. Shared across the family; handled as a scenario branch on CAS21.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered least-mature first (highest risk to the LCOE model).

**FLiBe Liquid-Immersion Breeding Blanket — TRL 2–3**
- **Demonstrated**: FLiBe thermophysical properties and small-scale molten-salt loops (heritage from fission molten-salt programs and the shared Kairos Power FLiBe supply chain). Static corrosion of Inconel-class alloys in FLiBe measured at ~1.1 μm/yr at 873 K [§3.7]. MCNP neutronics gives a designed TBR ≈ 1.1 with a 1 cm tungsten first wall and 90% Li-6 enrichment [§2, §5].
- **On paper only**: Full-scale liquid-immersion blanket achieving TBR ≥ 1.1 with realistic penetrations; tritium extraction from circulating FLiBe at kg/day throughput; radiation-assisted corrosion of Inconel 718 at 1100 K (the conservative-Pilot temperature, above the ~1120 K molten-salt material-qualification ceiling noted in the paper).
- **Missing at scale**: 14 MeV neutron qualification of the first wall / vessel at fusion fluence; kg/day FLiBe tritium-extraction plant; beryllium-bearing molten-salt handling at reactor scale.

**Tritium Fuel Cycle & Extraction — TRL 3–4**
- **Demonstrated**: Gram-scale tritium handling (JET, TFTR); Li-6 breeding physics; lab-scale extraction from liquid breeders.
- **On paper only**: Closed-loop, self-sufficient cycle at TBR = 1.1 with <1% losses for a FLiBe system.
- **Missing at scale**: Industrial tritium processing at plant throughput; permeation barriers for FLiBe-facing heat exchangers; tritium accountability in the molten-salt inventory.

**Divertor — TRL 4–6 (and undesigned for ARC specifically)**
- **Demonstrated**: ITER-class tungsten monoblock divertors at >10–20 MW/m² (WEST, GLADIS); detached-divertor operation in several tokamaks.
- **On paper only**: An actual ARC divertor — the 2015 design defers it entirely [§5.1]. Heat-flux handling placed "between ITER and reactor designs."
- **Missing at scale**: W divertor surviving combined 14 MeV neutron damage + steady heat flux over a useful replacement interval; FLiBe-cooled divertor integration.

**Remote Maintenance & Remote Handling — TRL 4–6**
- **Demonstrated**: ITER full-scale remote-handling mock-ups. ARC's demountable-joint, single-piece-vessel removal concept is a design-level innovation that *reduces* handling complexity in principle.
- **On paper only**: Demountable HTS joint maintenance cycle; whole-vessel swap at >80% availability.
- **Missing at scale**: Rad-hardened robotics operating for years in-vessel; demonstrated demountable-joint re-mate under activation.

**HTS REBCO Magnets — TRL 5–7**
- **Demonstrated**: CFS 20 T large-bore TF model coil (2021); SPARC TF coils in production; REBCO engineering current density ~1000 A/mm² at 20 K demonstrated industrially (Molodyk 2021, cited in arxiv-2503-23048.md). ARC conductor design: 70 kA REBCO CICC cables, 18 demountable TF coils, ~18 GJ stored energy, winding-pack current density 44 A/mm² graded to <50% of critical [§4].
- **On paper only**: Demountable resistive-joint TF coils at ARC scale; quench protection for an 18 GJ system; full structural steel cage reacting 23 T peak field.
- **Missing at scale**: REBCO tape supply at 5,730 km/reactor (see Section 4); radiation-hardened insulation and neutron-flux qualification of REBCO to ARC's 3×10¹⁸ n/cm² coil fluence limit (~9 full-power-years of margin behind the FLiBe+TiH₂ shield, per §2).

**ICRF / LHCD Heating & Current Drive — TRL 6–8**
- **Demonstrated**: MW-class ICRF and LHCD routine on existing tokamaks; SPARC ICRF design fixes antenna count and per-strap power (≤0.5–0.6 MW/strap, ~120 MHz) under CFS funding [sparc-icrf-heating-paper.md]. ARC: 25 MW LHCD at 8 GHz + 13.6 MW ICRF fast wave at 50 MHz, driving ~63% bootstrap [§3].
- **Missing at scale**: CW, neutron-tolerant launchers at tens of MW with high wall-plug efficiency; LHCD current-drive efficiency validated at reactor density.

**Vacuum Vessel / Primary Structure — TRL 6–8**
- **Demonstrated**: ARC's double-walled Inconel 718 FLiBe-cooled vessel is only ~85 t of solid material vs >2000 t in ITER [§3.6]; Inconel fabrication is mature.
- **Missing at scale**: Integration of a thin double-wall vessel with demountable coils and 1100 K FLiBe; activation/replacement logistics.

**Balance of Plant (Brayton/Rankine + thermal storage) — TRL 7–9 (cycle) / 4–5 (storage integration)**
- **Demonstrated**: GW-scale steam Rankine / sCO₂ cycles are commercial; Colliva et al. model all three ARC cycle options [arc-power-conversion-studies.md].
- **On paper only / Missing at scale**: Molten-salt energy-storage system sized to ARC's pulse/dwell cycle (required for constant grid output, not yet sized or costed); tritium-compatible FLiBe→working-fluid heat exchangers.

---

## Section 4: Key Materials and Supply Chain Considerations

**REBCO superconducting tape — the binding supply constraint.** ARC requires **5,730 km of REBCO tape per reactor** [§6, Table 11], against a global production capacity on the order of a few thousand km/year across all manufacturers. A single ARC therefore consumes ~1–2 years of current world output. The 2015 quote was **$36–198/m** (the source notes the high end was used for the cost-feasibility total) [Table 10]; modern accelerator-magnet reviews put REBCO at **150–200 $/kA-m** with an aspirational ~3× reduction target [arxiv-2503-23048.md]. Crucially, because ARC's magnet cost is structure-dominated (§2), even large swings in REBCO price move the magnet account only modestly — the supply *quantity* (manufacturing throughput, lead time) is a bigger deployment risk than the tape *unit price*. Key producers: Shanghai Superconductor, Faraday Factory Japan, CFS's own tape effort. Shared bottleneck with every HTS comparable (21, 28).

**FLiBe molten salt (with beryllium and Li-6 enrichment).** ARC's blanket holds **~958 tonnes of FLiBe** at a 2015 unit price of **$154/kg** (≈ $147M inventory) [Table 10–11], with lithium enriched to **90% Li-6** [§5]. Three nested supply constraints: (a) FLiBe is not produced at industrial scale today (shared nascent supply chain with Kairos Power fission); (b) beryllium — a FLiBe constituent and the 1 cm neutron-multiplier layer — is produced at only ~300 t/yr globally, dominated by a single US producer (Materion), and priced at $257/kg [Table 10]; (c) 90% Li-6 enrichment capacity is globally scarce (legacy mercury-amalgam processes in Russia/China; Western alternatives pre-commercial). This stack of constraints is *more* acute than the liquid-lithium path taken by the spherical-tokamak comparable (21), which avoids beryllium.

**Tritium.** Global civilian inventory ~25–30 kg (CANDU byproduct, decaying 5.5%/yr); ~1 kg startup load; TBR = 1.1 provides thin breeding margin. Sequencing constraint shared across all D-T concepts: first plants must prove self-sufficiency before fleet scale-up. ARC's 4π immersion blanket gives a structurally simpler route to TBR ≥ 1 than the outboard-only geometries (cf. comparable 21).

**Structural steel (SS316LN) and Inconel 718.** ARC's magnet cage uses **4,350 t of SS316LN** ($9.6/kg raw, but ~$4.6B fabricated at $1.06M/t machining scaling); the vessel/blanket tank use Inconel 718 ($56/kg) [Tables 10–11]. These are commodity-available but the magnet structure's precision-fabricated mass is the dominant capital item — a manufacturing-throughput and machining-capacity question, not a raw-material-supply one.

**Tungsten (first wall + divertor).** 1 cm W first wall (3.72 t) and an undesigned W divertor; W is in adequate supply but large-area, thermal-fatigue-resistant tile fabrication remains a manufacturing challenge shared with all tokamaks. TiH₂ neutron shield (380 t, $26.4/kg) protects the coils.

---

## Section 5: Design Point Parameters

All values describe the **ARC 2015 Conservative Pilot phase** (Sorbom et al.), at its native scale of **233 MWe net**. The plasma/machine hardware is identical across the FNSF / conservative-Pilot / aggressive-Pilot phases; only the blanket outlet temperature and resulting thermal efficiency change. Cost figures are FY2014 USD as published.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| R0 (major radius) | 3.3 m | arc-reactor-specifications.md §3 (0-D design) | high | "increased from 3.2 to 3.3 m" |
| a (minor radius) | 1.13 m | arc-reactor-specifications.md §Table 7 | high | body text rounds to 1.1 m; aspect ratio 1/ε = 3 |
| elongation κ | 1.84 | arc-reactor-specifications.md §Table 7 | high | |
| aspect ratio (R0/a) | 3.0 | arc-reactor-specifications.md §3 | high | conventional aspect ratio (not spherical) |
| B0 (on-axis toroidal field) | 9.2 T | arc-reactor-specifications.md §3 | high | "fixed in the design" |
| B_peak (peak field on coil) | 23 T | arc-reactor-specifications.md §4 (Magnets) | high | "maximum field in the conductors… 23 T at the inboard midplane" — the defining high-field knob |
| Ip (plasma current) | 7.8 MA | arc-reactor-specifications.md §Table 7 | high | ACCOME gives 7.75 MA |
| fusion_power_MW | 525 MW | arc-reactor-specifications.md §3 (ACCOME design point) | high | target 500 MW; **Table 7's "143 MW" is an extraction artifact — do not use** |
| thermal_power_MW (to PCS) | ~645 MWth | arc-power-conversion-studies.md §2 | medium | FLiBe-delivered thermal power (Colliva BOP model) |
| net_electric_MWe | 233 MWe | arc-reactor-specifications.md §2 | high | = P_native; conservative-Pilot (1100 K, η≈46%, Qe=3.5) |
| thermal efficiency η_th | ~46% | arc-reactor-specifications.md §2 | medium | He Brayton at 1100 K outlet; contingent on materials R&D (FNSF demonstrates only ~40% / 190 MWe) |
| Q_engineering (Qe) | 3.5 | arc-reactor-specifications.md §2 | high | conservative-Pilot phase |
| Q_plasma (Qp) | ~13.6 | arc-reactor-specifications.md §3 | high | burning plasma (alpha-dominated) |
| p_input_MW (aux H&CD) | 38.6 MW | arc-reactor-specifications.md §3 | high | 25 MW LHCD (8 GHz) + 13.6 MW ICRF (50 MHz) |
| bootstrap fraction f_bs | ~63% | arc-reactor-specifications.md §3 | high | LHCD 1.77 MA + ICRF 1.1 MA balance |
| TBR (tritium breeding ratio) | 1.1 | arc-reactor-specifications.md §2, §5 | high | FLiBe immersion, 90% Li-6, 1 cm W first wall |
| **Concept-distinctive knob:** B_peak / compactness | 23 T peak → R0 = 3.3 m | arc-reactor-specifications.md §4 | high | high-field HTS enables ITER-class fusion power at ~⅕ ITER mass |
| REBCO tape quantity | 5,730 km | arc-reactor-specifications.md §6 (Table 11) | high | per reactor; ~1–2 yr of global supply |
| magnet stored energy | ~18 GJ | arc-reactor-specifications.md §4 | high | 70 kA REBCO CICC, 18 demountable TF coils |
| coil operating temperature | 20 K | arc-reactor-specifications.md §4 | high | sub-cooled REBCO |
| first wall | 1 cm tungsten on Inconel 718 | arc-reactor-specifications.md §5 | high | |
| neutron wall loading (blanket areal) | ~2.5 MW/m² | arc-reactor-specifications.md §3 (P_f/S_b) | medium | P_f/S_p ≈ 0.67 MW/m² over plasma surface |
| FLiBe inventory | ~958 t | arc-reactor-specifications.md §6 (Table 11) | high | channel + blanket tank + heat exchanger |
| vacuum vessel solid mass | ~85 t | arc-reactor-specifications.md §3.6 | high | vs >2000 t in ITER |

*Financial / operating-economics parameters (availability, lifetime, interest, inflation) are intentionally omitted — they are library-owned and identical across concepts by construction.*

---

## Section 5b: Override Candidates

Per-account walkthrough result. The ARC 2015 paper publishes a subsystem cost table in FY2014 USD; this is the rare case where the design-point source grounds several accounts directly. All escalations use **CPI-U FY2014→2024 ≈ 1.33** (236.7 → 313.7). Four accounts are overridden; the remaining canonical accounts (C220102 shield, C220104 heating, C220105 primary structure, C220106 vacuum, C220107 power supplies, C220110 remote handling, C220111 installation, CAS21/23/24/26, CAS70/80) are **not** overridden — either the paper gives no separable figure, the figure is small enough to sit within the library default, or the account is library-owned. Account count (4 enabled) is within the High archetype-fit band (0–4).

```yaml
overrides:
  - account: C220103
    value: 5200.0 * 1.33
    enabled: true
    provenance: derived
    source: "arc-reactor-specifications.md §6 Table 11"
    rationale: |
      Sorbom 2015 publishes a magnet/structure subtotal of $5.1-5.2B fabricated
      (FY2014). Using the upper estimate $5,200M x 1.33 (CPI-U 2014->2024) = $6,916M.
      The figure is dominated NOT by REBCO conductor ($100-210M tape + $380M copper
      winding structure) but by 4,350 t of SS316LN structural steel ($4.6B fabricated)
      reacting the 23 T peak-field forces. The library default prices HTS coils from
      conductor geometry/length and will undercount the ARC magnet by ~10x because it
      misses the structural-steel cage. This is the single largest and best-justified
      departure for the archetype. Note: the published subtotal bundles the magnet
      tension ring (~$9M) and a steel-modeled machine base that a finer breakdown would
      assign to C220105; kept here because the mass exists to react coil loads.
  - account: C220101
    value: 108.1 * 1.33
    enabled: true
    provenance: derived
    source: "arc-reactor-specifications.md §6 Table 11"
    rationale: |
      First wall (1 cm W, 3.72 t -> $4.03M fabricated) + Be neutron multiplier
      (3.82 t -> $4.1M) + Inconel 718 blanket tank structure (97.1 t -> $100M) =
      $108.1M FY2014. x 1.33 (CPI 2014->2024) = $143.8M. This prices the structural
      blanket/first-wall/multiplier from ARC's published neutronics-derived volumes,
      excluding the FLiBe fill (-> CAS27). The library default does not see ARC's
      thin-wall liquid-immersion architecture (only ~85 t total vessel solid mass).
  - account: CAS27
    value: 147.5 * 1.33
    enabled: true
    provenance: derived
    source: "arc-reactor-specifications.md §6 Table 11"
    rationale: |
      Initial FLiBe inventory: ~958 t x $154/kg = $147.5M FY2014 (channel 8.07 t +
      blanket tank 475 t + heat-exchanger loop 475 t). x 1.33 (CPI 2014->2024) =
      $196.2M. Both the quantity (958 t) and the unit price ($154/kg) are published in
      the same table, so the FY2014 figure is direct; the CPI escalation makes the
      delivered value derived. FLiBe is a special-material blanket fill distinct from
      the C220101 structure, with a beryllium- and Li-6-enrichment-driven price the
      generic special-materials default would not capture.
  - account: C220108
    value: 17.5 * 1.33
    enabled: true
    provenance: derived
    source: "arc-reactor-specifications.md §6.3"
    rationale: |
      The 2015 design defers the divertor ("left as an open question") and gives only a
      rough estimate: a 2 cm tungsten divertor over ~20% of first-wall area, ~$500k
      materials -> ~$17.5M fabricated (FY2014). x 1.33 = $23.3M. Enabled because it is
      the only ARC-grounded divertor figure, but flagged low-confidence: it is a
      placeholder for an undesigned subsystem, not a costed design (see Data Gap #2).
```

*Walkthrough notes on accounts NOT overridden:* C220102 (TiH₂ neutron shield, 380 t → $10M FY2014, ≈ $13M escalated) has a clean published figure but is small and plausibly inside the library blanket/shield default; it is recorded here as a considered-but-folded candidate rather than a fifth override, to avoid inflating the count past the evidence. C220106 (vacuum vessel: inner/outer Inconel walls + ribbing + posts, ~$80M FY2014 after correcting the inner-VV OCR artifact) is a genuine published figure but is entangled with the C220101 blanket structure in ARC's "replaceable vacuum vessel" subtotal and is left to the library default to avoid double-counting. C220104/C220107 (heating + power supplies): ARC publishes heating *power* (38.6 MW) but no heating *cost*, so the per-installed-MW library default stands.

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Commercial ARC (400 MWe, Virginia) parameters unpublished; design point is the 2015 233 MWe paper, not the program plant | S1, S2 | proprietary | important | Watch for a CFS ARC conceptual design publication; treat 400 MWe plant as a separate future design point |
| 2 | Divertor undesigned — only a $17.5M placeholder exists | S2, S3, S5b | not-yet-sourced / truly-unknown | important | Apply ITER/SPARC divertor cost scaling once an ARC divertor concept is published; carry C220108 as low-confidence |
| 3 | Thermal efficiency (46%) is contingent on unproven 1100 K blanket-outlet materials | S2, S5 | derivable | important | Sensitivity sweep η_th 40–50%; FNSF (40%/190 MWe) is the demonstrated-material floor |
| 4 | No concept-specific O&M breakdown (fixed/variable, replacement, tritium labor) | S2 | proprietary | important | Use pyFECONS 60 $/kWe-yr (CAS70) + scheduled blanket replacement; flag as default |
| 5 | Component replacement intervals & outage durations (first wall, blanket, divertor) unpublished | S2, S3 | proprietary | important | ITER blanket program + Schwartz (2405.01514) maintenance-value model; model as scheduled FO&M |
| 6 | Molten-salt energy-storage system for pulse/dwell buffering not sized or costed | S2, S3 | truly-unknown | important | CSP molten-salt TES cost analog; needs ARC pulse-length/dwell input |
| 7 | FLiBe tritium-extraction plant design & cost at kg/day throughput | S3, S4 | truly-unknown | important | Molten-salt fission extraction analogs; no fusion-scale data |
| 8 | REBCO neutron-irradiation lifetime at ARC coil fluence (3×10¹⁸ n/cm²) | S3 | truly-unknown | important | Dedicated 14 MeV irradiation campaign; ~9 FPY margin claimed but unvalidated |
| 9 | FY2014→present cost escalation not provided by source | S5b | derivable | nice-to-have | CPI-U 1.33 applied; revisit with a fusion-specific escalator if available |
| 10 | Gross electric power / core thermal power live only in non-OCR'd Table 1 image | S5 | not-yet-sourced | nice-to-have | Inspect Table 1 image (sync R2 binaries) for authoritative aggregate values |
| 11 | Li-6 enrichment supply chain for 90% enrichment at fleet scale | S4 | truly-unknown | nice-to-have | Survey Western Li-6 enrichment pilot programs |

---

## Section 7: Family-Delta vs Comparables

Fixed comparables: `21-spherical-tokamak-hts`, `28-hts-tokamak-full-hts`, `29-negative-triangularity-tokamak`, `33-state-backed-tokamak-best`. All four are MFE tokamak-family concepts; the deltas below isolate what the ARC 2015 design point does *differently* and how that moves cost. Only comparable 21 has an approved analysis in the corpus; deltas to 28/29/33 are characterized at lower confidence and flagged where source data is absent.

**vs. 21-spherical-tokamak-hts (Tokamak Energy ST-E1)** — *the best-characterized contrast.*
- **Geometry/field (magnet cost):** ARC is conventional aspect ratio (A=3.0) and high-field (B0 = 9.2 T, B_peak = 23 T); ST-E1 is spherical (A=2.3) and lower-field (B0 = 5.25 T). Direction: ARC carries a **magnet-cost penalty** — its 23 T peak field demands the $4.6B structural-steel cage that dominates C220103, whereas ST-E1's lower field reduces coil stress and conductor-performance requirements. Magnitude: ARC's magnet account is plausibly several-fold larger per coil, though ST-E1 publishes no cost to confirm.
- **Blanket (C220101/CAS27):** ARC uses 4π FLiBe immersion (TBR 1.1, but beryllium + 90% Li-6 supply burden); ST-E1 uses outboard-only liquid lithium (no beryllium, but ~50% solid-angle coverage and a unique center-stack-shielding problem ARC does not have). Direction: roughly **cost-neutral but risk-divergent** — ARC trades supply-chain complexity for breeding-geometry robustness.
- **Operation/BOP:** ARC is quasi-steady (bootstrap + LHCD); ST-E1 is explicitly pulsed and needs a thermal-storage buffer (a capital item ARC's quasi-steady design largely avoids — though ARC's *own* pulse/dwell cycle still requires the Colliva ESS, a smaller effect). Direction: **ARC advantage** on BOP storage.
- **Novel vs. shared:** REBCO tape supply chain, D-T tritium constraint, and regulatory multiplier are shared. ARC's structure-dominated magnet cost and FLiBe inventory (CAS27) are the genuine ARC-specific cost signals.

**vs. 28-hts-tokamak-full-hts (Energy Singularity)** — *the nearest neighbor.* Both are compact, high-field, all-REBCO tokamaks at conventional aspect ratio — the closest analog to ARC in the corpus (Energy Singularity's HH-class is widely described as a SPARC/ARC analog). Expected delta is **small**: a shared structure-dominated magnet cost profile and similar REBCO-supply exposure. Likely divergences are blanket chemistry and a state-influenced domestic supply chain (cheaper steel/labor), which would lower CAS21/C220103 fabrication cost. No source data for concept 28 is available in this dossier, so these deltas are **inferred, low confidence** and flagged as a data gap.

**vs. 29-negative-triangularity-tokamak (Firefly)** — Negative-triangularity geometry targets ELM-free operation and relaxed divertor heat loads at conventional aspect ratio. Relative to ARC, the plausible cost delta is concentrated in **C220108 (divertor)** and first-wall handling: NT could reduce divertor severity (a cost/risk advantage), at the price of lower confinement (larger machine per unit fusion power — a possible magnet/structure penalty). ARC's own divertor is undesigned, so this delta is **directional only, low confidence** — no NT source data is available here.

**vs. 33-state-backed-tokamak-best (Neo / ASIPP-class)** — A state-backed, conventional large tokamak (CFETR-lineage), likely LTS or LTS+HTS magnets at lower field and substantially larger scale. The dominant delta is **magnet technology and machine scale**: ARC's high-field HTS compactness is precisely the bet that ARC's authors quantify against the large low-field path — "9.2 T ARC has a fifth of the ~$24B price of the 5.3 T ITER… yet ARC matches ITER's fusion power" [§6.6]. Direction: **ARC capital-cost advantage per unit fusion power** from compactness, offset by state-backed concepts' advantages in financing cost and domestic supply (lower effective CAS21/indirects, higher achievable availability via program continuity). Quantitatively unanchored for the specific Neo design (no source data in this dossier).

---

## Section 8: Sources

1. **Sorbom, B.N. et al. (2015), "ARC: a compact, high-field, fusion nuclear science facility and demonstration power plant with demountable magnets," *Fusion Engineering and Design* 100, 378–405.** The primary design-point source. Provides the complete plasma/machine parameter set, radial build, MCNP-derived FLiBe blanket, REBCO magnet design, and — uniquely — the FY2014 subsystem cost tables (Tables 10–11) that ground all four override candidates. Found at: `knowledge/concept_research/01-hts-compact-tokamak/iter-03/sources/arc-reactor-specifications.md`.
2. **Colliva et al., "Analysis of different Power Conversion System options for ARC… Balance of Plant," SSRN-4482183.** Models steam Rankine / sCO₂ / He Brayton cycles for the ARC FNSF balance of plant; recommends steam Rankine (~46% net); confirms the molten-salt energy-storage requirement. Source of the ~645 MWth figure. Found at: `…/iter-04/sources/arc-power-conversion-studies.md`.
3. **Lin, Y., Wright, J.C., Wukitch, S.J., "Physics basis for the ICRF system of the SPARC tokamak," *J. Plasma Phys.***. CFS-funded ICRF design (antenna count, ~120 MHz, ≤0.5–0.6 MW/strap) developed for ARC-class use; grounds the heating-system maturity assessment. Found at: `…/iter-03/sources/sparc-icrf-heating-paper.md`.
4. **Woodruff, S. et al., "A Costing Framework for Fusion Power Plants" (pyFECONS), arXiv 2601.21724.** GEN-IV/ARPA-E cost-account structure, magnet-driver (22.1.3) methodology, O&M ≈ 60 $/kWe-yr, deuterium ≈ $2,175/kg. Methodological backbone for account mapping. Found at: `…/iter-04/sources/arxiv-2601-21724.md`.
5. **Woodruff, S. et al., "Extension of the Fusion Power Plant Costing Standard," arXiv 2602.19389.** CATF/IWG methodology extension (uncertainty compounding, licensing/insurance proxies); methodology only, no input values. Found at: `…/iter-04/sources/arxiv-2602-19389.md`.
6. **Najmabadi, F. et al., "ARIES-AT: An Advanced Tokamak, Advanced Technology Fusion Power Plant," OSTI 20261446.** Comparator point design: 1000 MWe, COE 5 c/kWh, 6.0 T / 11.4 T peak, PbLi/SiC blanket, 59% thermal cycle. Cross-check for tokamak cost structure. Found at: `…/iter-04/sources/osti-etdeweb-servlets-purl-20261446.md`.
7. **Woodruff Scientific, "Revisit of the 2017 Costing for Four ARPA-E ALPHA Concepts," OSTI 1820946.** Full CAS-level cost breakdown (LCOE 43 $/MWh, CapEx 2.4 $/W, O&M $48M/yr) for ~500 MWe MIF plants; methodology/cross-check, not ARC. Found at: `…/iter-04/sources/osti-servlets-purl-1820946.md`.
8. **Schwartz, J.A. et al. (2024), "Valuing maintenance strategies for fusion plants…," arXiv 2405.01514.** Grid-value model of scheduled blanket/divertor replacement; parasitic-power fractions (net = 0.85×gross), VO&M $2.07/MWh, and the key finding that scheduled maintenance costs less value than a flat availability penalty implies. Grounds O&M/availability treatment. Found at: `…/iter-04/sources/arxiv-2405-01514.md`.
9. **Bottura, L., Bordini, B. (2025), "HTS Potential and Needs for Future Accelerator Magnets," arXiv 2503.23048.** HTS/REBCO conductor cost data (150–200 $/kA-m; ~3× aspirational reduction) and 20 K cryogenics efficiency case. Accelerator-focused; used only for REBCO unit-cost context. Found at: `…/iter-04/sources/arxiv-2503-23048.md`.
10. **Fortune (Blum, Jan 2026), CFS commercial ARC update.** Current-program data: 400 MWe, Richmond VA, early-2030s, 18 TF coils, Google/Nvidia/Mitsubishi backing. Used only to flag the design-point/program power mismatch (Section 2). Found at: `…/iter-04/sources/cfs-2025-2026-updates.md`.
11. **Approved analysis: `21-spherical-tokamak-hts` (Tokamak Energy).** Cross-concept reference for the spherical-tokamak family-delta (Section 7) and for shared REBCO/tritium/regulatory assumptions. Found at: `exploration/concept_analysis/analyses/21-spherical-tokamak-hts/analysis.md`.
12. **Handwritten exemplar `01-hts-compact-tokamak.md`.** Calibration reference for D-T tokamak supply-chain figures (REBCO $30–100/kA-m, tritium ~25–30 kg / >$35,000/g, FLiBe NOAK ~$154/kg, Stewart & Shirvan 2.2× regulatory multiplier, beryllium ~300 t/yr Materion).
