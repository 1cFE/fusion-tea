Now I have everything I need. Let me write the gap assessment.

---

# Gap Assessment: Helical Coil Stellarator

## Overall Readiness
**Rating**: Mostly Ready

**Summary**: Helical Fusion is unusually transparent for an early-stage startup, having published a primary reactor design paper (HESTIA, AIP 2023) with construction cost and performance targets. The qualitative sections are well-supported across five sources. The main gap for LCOE is the absence of any subsystem-level cost breakdown — only the total $5B construction figure is published — and unconfirmed power conversion efficiency. These gaps are real but workable: the total cost enables a top-down LCOE estimate, and key parameters (thermal power, efficiency) are derivable with stated assumptions.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Moderate

**Available**:
- Primary reactor design paper published in a peer-reviewed journal (AIP Physics of Plasmas 30, 050601 (2023)) with top-level performance parameters, construction cost estimate, and key technology choices
- Company website with collaborative research structure (14 named areas), technology roadmap (HARUKA → KANATA → HESTIA), and milestone press releases
- 2025 milestone: HTS coil demonstrated at 40 kA / 7 T / 15 K (ANS Newswire, BusinessWire)
- NIFS heritage documentation: Oroshhi-2 platform, FFHR blanket program, sCO2 demo plan (Ishiyama & Tanaka 2019)
- Tohoku University materials paper (Nuclear Materials and Energy, March 2024) on blanket structural material
- GALOP blanket test system announcement (public press release)

**Missing**:
- Full text of AIP 2023 paper (paywalled) — abstract covers the key parameters but the body likely contains plasma parameter tables, subsystem sizing, and power balance details
- Any conference proceedings from FPA, IAEA, or SOFT that may cover HESTIA in more depth
- Investor materials or technical pitch decks (if any have been shared)
- Any system code study from NIFS applying to the HESTIA geometry (the FFHR line used the HELIOS system code)

**Gaps**:
- Full AIP 2023 paper body — `not-yet-sourced` — **important** (may contain power balance, subsystem masses, full plasma parameter set)
- Conference proceedings (FPA, IAEA Fusion Energy, SOFT) — `not-yet-sourced` — **important** (Helical Fusion/NIFS regularly present at these)
- HELIOS/PROCESS system code runs for HESTIA geometry — `not-yet-sourced` — **nice-to-have**

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- Core physics advantages are documented: no disruption risk, no current drive power, steady-state operation rationale
- Two technology "pillars" for Helix HARUKA identified: HTS magnets and integrated blanket/divertor system
- ECRH identified as sole heating mechanism (250 GHz, 1 MW CW gyrotrons, joint R&D with QST)
- Liquid metal blanket multi-function role documented: tritium breeding + first wall + neutron shield + heat removal (no separate divertor)
- Q~13 and 50 MWe target give enough to frame recirculating power fraction

**Missing**:
- Plasma confinement physics validation: confinement scaling from LHD to reactor scale is not publicly confirmed (the "factor of N" extrapolation from LHD parameters to HESTIA)
- Neoclassical transport losses in heliotron geometry at reactor scale (a well-known challenge for stellarators; Helical Fusion claims mitigation but no published data)
- Power balance table: how much ECRH power input is required at Q~13? What fraction of gross electricity is recirculated?
- Divertor heat flux handling via liquid metal flow: quantitative heat load and flow rate data
- MHD pressure drop in liquid metal loops under magnetic field (classic LM blanket challenge)

**Gaps**:
- Plasma confinement scaling validation (LHD → HESTIA) — `proprietary` / `not-yet-sourced` — **blocking** (the central physics claim; no published scaling confirmation found)
- ECRH power budget at full Q~13 operating point — `not-yet-sourced` — **important** (needed for net efficiency calculation; derivable to first order if Q is trusted)
- Liquid metal MHD and heat removal quantitative data — `not-yet-sourced` — **important** (conference papers from NIFS/GALOP team likely exist)
- Neoclassical transport loss fraction at HESTIA scale — `proprietary` / `truly-unknown` — **important** (fundamental stellarator engineering challenge)

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **HTS magnets (WISE REBCO)**: Demonstrated at 40 kA / 7 T / 15 K at conductor scale (>4 m length, 30 REBCO layers, ~3 cm cross-section) — Oct 2025 milestone. Coil manufacturing machine completed with Sugino Machine. TRL ~3-4 at conductor/coil level; full helical coil winding at HESTIA scale undemonstrated.
- **ECRH gyrotrons**: R&D stage at 250 GHz / 1 MW CW. Joint program with QST. 250 GHz is significantly above demonstrated continuous-wave high-power gyrotron frequencies (170 GHz for ITER); TRL ~2-3.
- **Liquid metal blanket**: GALOP test system validates gas-driven pump mechanism at lab scale (~4m×2m×2m). TRL ~2-3.
- **Structural material**: Tohoku University collaboration on high-Mn alumina-forming austenitic steel published (2024); material characterized but not fabricated at blanket module scale.
- **Solid pellet fueling**: Listed as collaborative research area; off-the-shelf technology from existing fusion programs.
- **Roadmap context**: Helix HARUKA (integrated demo) is at assembly-initiation stage in 2026. KANATA (pilot) targeted for 2030s.

**Missing**:
- Integrated coil winding demonstration at helical scale (a full helical coil segment, not just double-pancake test piece)
- Blanket module design with full tritium breeding ratio calculation
- Gyrotron performance data at 250 GHz (output power, efficiency, CW operation duration)
- Remote maintenance robot system (listed as collaborative research area, no milestone data)
- Vacuum vessel design and scale

**Gaps**:
- Full-scale helical coil demonstration — `proprietary` (in progress, HARUKA) — **blocking for pilot, important for analysis** (currently the single biggest engineering unknown)
- 250 GHz CW gyrotron performance data — `proprietary` / `not-yet-sourced` — **important** (needed for heating efficiency and recirculating power)
- TBR calculation for HESTIA blanket geometry — `not-yet-sourced` — **important** (NIFS has published TBR studies for FFHR; HESTIA TBR likely in full AIP paper)
- Remote maintenance system TRL — `not-yet-sourced` — **nice-to-have**

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- **REBCO tape**: Identified as primary superconductor. Proprietary WISE conductor uses stacked REBCO tapes. REBCO is commercially produced (Fujikura, SuNAM, AMSC) but at limited volumes; scale-up for two continuous multi-kilometer helical coils is a supply chain challenge.
- **Liquid metal**: Lithium-bearing metal required for tritium breeding. Specific composition unconfirmed (Li, LiPb, or other). Li-6 enrichment requirement unknown.
- **Structural steel**: High-Mn austenitic steel (non-magnetic, low-activation) — novel alloy under development; not yet commercially available.
- **Gyrotrons**: 250 GHz CW devices require specialized manufacturing; no commercial supplier currently produces at this frequency/power.
- **Funding context**: $38M raised total (including $13M Japan SBIR); modest for the scope, suggesting supply chain development is still upstream.

**Missing**:
- REBCO tape quantity estimate for HESTIA's two helical coils (length × cross-section gives tape volume; not published)
- Li-6 enrichment requirement and global supply capacity
- Low-melting-point alloy specification for WISE impregnation (determines availability and properties)
- Magnet cooling system design (cryostat, cryocoolers for 15 K operation at reactor scale)

**Gaps**:
- REBCO tape quantity for full HESTIA coil set — `derivable` (from coil geometry + conductor specs) — **important** (cost driver)
- Li-6 enrichment level and annual tritium inventory — `not-yet-sourced` — **important** (fuel cost and supply risk)
- WISE impregnation alloy identity — `proprietary` — **nice-to-have** (affects conductor performance/cost)
- Cryostat system design and scale — `not-yet-sourced` — **nice-to-have**

---

### 5. LCOE Parameter Extraction
**Coverage**: Partial

**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Total construction cost (HESTIA) | USD 5 billion | AIP 2023 abstract | medium — company estimate, no breakdown |
| Net electrical output | 50 MWe | AIP 2023 | high |
| Follow-on plant output | 100 MWe-class | AIP 2023 | high |
| Fusion gain Q | ~13 | AIP 2023 | high |
| Availability target | >80% | AIP 2023 | high |
| Maintenance cycle | ~3 months per year | AIP 2023 | high |
| Continuous burn duration | ~1 year | AIP 2023 | high |
| Magnetic field at coil center | 8 T | AIP 2023 | high |
| Major radius | ~8 m (helical coils) | Tech overview | medium |
| Heating method | ECRH, no current drive | AIP 2023 | high |
| Power conversion | sCO2 Brayton (likely) | Indirect: website + Oroshhi-2 | medium |
| sCO2 efficiency target | >50% at 800–1200 K | Ishiyama & Tanaka 2019 | medium — NIFS research target, not HESTIA-specific |
| Capacity factor (derived) | ~80% | AIP 2023 | medium |
| Fuel type | D-T, self-bred tritium | AIP 2023 | high |
| Funding raised | ~USD 38M (Dec 2025) | BusinessWire | high |

**Derived / Estimable Parameters** (not directly stated but calculable):

| Parameter | Derivation | Notes |
|-----------|-----------|-------|
| Thermal power | If η=50%, P_thermal ≈ 100 MWth; if η=40%, P_thermal ≈ 125 MWth | Depends on sCO2 efficiency assumption |
| Specific capital cost | $5B / 50 MWe = $100,000/kWe ($100/W) | Extremely high by power plant standards; driven by small scale |
| ECRH recirculating power | At Q~13: P_fusion ≈ 13×P_ECRH; if P_net=50 MWe and η=50%, rough estimate P_ECRH ≈ 10–15 MW, recirculating fraction ~20–30% | Assumes simple Q definition; actual power balance needs full paper |
| Back-of-envelope LCOE | At 8% FCR: ~$400M/yr capital + $50M/yr O&M over 350 GWh/yr → ~$130/MWh (13 c/kWh) at 50 MWe | Very high; improves sharply at 100 MWe scale |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost by subsystem (magnet, blanket, BOP, building) | proprietary | blocking for detailed model | Only total cost published |
| Thermal power output | derivable | important | Back-calculable once efficiency assumed |
| Power conversion cycle efficiency (confirmed) | not-yet-sourced | important | sCO2 strongly implied; value unconfirmed |
| ECRH total power input (MW) | not-yet-sourced | important | Determines recirculating power; may be in full AIP paper |
| O&M cost estimate | proprietary / not-yet-sourced | important | No public estimate; need analogue from FFHR studies or tokamak O&M |
| Blanket module lifetime / replacement schedule | not-yet-sourced | important | Affects O&M cost; neutron wall loading unknown |
| REBCO tape cost at production volume | not-yet-sourced | important | Major capital cost driver |
| 250 GHz gyrotron cost and efficiency | not-yet-sourced | important | Determines ECRH capital and recirculating power |
| Li-6 enrichment and annual fuel cost | not-yet-sourced | nice-to-have | Fuel cost likely small vs. capital |
| Neutron wall loading (MW/m²) | not-yet-sourced | important | Drives blanket lifetime and replacement cost |

---

## Source Recommendations

1. **Full AIP 2023 paper (Physics of Plasmas 30, 050601)** — paywalled, but likely accessible via institutional access or Sci-Hub equivalent. Expected content: plasma parameter table, power balance, subsystem sizing, TBR estimates, possibly cost breakdown detail. `not-yet-sourced` — **highest priority**.

2. **NIFS FFHR system studies** — search NIFS publications or OSTI for "FFHR-c1" or "FFHR-d1" system code studies by Sagara, Takahashi, or Goto. These form the heritage basis for HESTIA and may contain cost modeling methodology applicable by analogy. `not-yet-sourced` — `unverified — confirm existence before searching`.

3. **FPA or IAEA conference proceedings** — Helical Fusion/NIFS team likely presented at Fusion Power Associates Annual Meeting (2024, 2025) or IAEA Fusion Energy Conference. Search FPA proceedings or IAEA INIS for "Helical Fusion" or "HESTIA." `not-yet-sourced` — `unverified — confirm existence before searching`.

4. **SOFT (Symposium on Fusion Technology) proceedings** — NIFS blanket team regularly presents liquid metal blanket progress at SOFT. Relevant for GALOP quantitative data, MHD analysis, TBR calculations. `not-yet-sourced` — `unverified — confirm existence before searching`.

5. **Springer book chapter** — Source listed in dossier: "Helical Fusion Reactor Concepts" chapter from a Springer volume. May contain reactor parameter tables and cost discussion. `not-yet-sourced` — obtain via DOI `10.1007/978-3-031-17711-8_9`.

6. **HTS coil cost analogues** — For REBCO magnet cost estimation, use published HTS magnet cost studies from SPARC (Commonwealth Fusion), STEP (UKAEA), or ARPA-E GAMOW program reports. These provide $/kA-m or $/kg cost data applicable to WISE-type conductors. `derivable by analogy`.

7. **sCO2 Brayton cycle cost data** — NREL, Sandia, or DOE sCO2 pilot program reports (e.g., the NET Power plant, Echogen) provide BOP cost estimates at relevant scales. `not-yet-sourced` — applicable as analogue for energy conversion cost.

---

## Summary

**Proceed to full analysis with current sources, supplemented by targeted retrieval.**

The data state is sufficient to write a well-grounded qualitative write-up and a parameterized first-pass LCOE model. The $5B construction cost figure and >80% availability target provide anchors for top-down LCOE estimation. The Q~13 performance target and sCO2 efficiency range support a reasonable power balance derivation.

The most important gap is the absence of any subsystem-level cost breakdown — the $5B is a single number with no decomposition. A bottom-up cost model is not feasible without this, but a top-down model with sensitivity analysis is tractable. The second-priority gap is confirmed power conversion efficiency; using a range of 40–55% for sCO2 covers the uncertainty reasonably.

The Springer book chapter (DOI available) and the full AIP 2023 paper body should be attempted before finalizing the analysis, as they are the most likely sources to contain plasma parameter tables, power balance details, and possibly cost structure. All other gaps can be addressed through analogues, derivations, and explicitly stated assumptions.
