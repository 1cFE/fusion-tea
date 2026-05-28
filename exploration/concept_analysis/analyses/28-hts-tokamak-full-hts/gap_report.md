# Gap Assessment: HTS Tokamak - Full HTS (D-T)

## Overall Readiness
**Rating**: Mostly Ready
**Summary**: Energy Singularity's HH70/HH170 program is well-documented at the machine-physics level, and a high-quality D-T MFE cost analog (Araiinejad & Shirvan 2025, `knowledge/sources/tea_dt_mfe_cost_analysis/`) provides a compact REBCO HTS tokamak cost framework that directly maps onto this concept. The primary blocking gaps — HH380 power plant specifications, blanket design, and neutron shielding approach — are proprietary or structurally unresolvable at the current company stage (HH380 is post-2030), but these can be handled with explicit analog assumptions derived from the fleet-wide TEA source. The analysis can proceed with clearly bounded uncertainty, drawing on the ARC/ARAI analog for LCOE parameters.

## Section Coverage

### 1. Availability of Data
**Coverage**: Partial
**Available**:
- HH70 commissioning data: major radius 0.7 m, minor radius 0.25–0.3 m, B0 = 0.6 T, Bmax = 2.5 T, 26 REBCO coils (12 TF + 6 PF + 8 CS), 1,337-second steady-state plasma demonstrated (energy-singularity-overview.md; sciencedirect pii-s092037962500537x abstract)
- HH170 targets: Q > 10, ~14 T on-axis, ~110% of SPARC field, ~70% SPARC volume, D-shaped HTS magnets targeting 25 T peak field, 2027 completion (dossier; energy-singularity-overview.md)
- Jingtian magnet: 21.7–22.4 T peak field demonstrated, IEEE TAS 2025 publication (dossier)
- Company roadmap: HH70 → HH170 → HH380 → commercialization before 2035 (energy-singularity-overview.md)
- Funding: ~$110M raised for HH70, seeking $500M for HH170 (energy-singularity-overview.md)
- D-T MFE cost analog: ARAI-FPP (ARC-derived, compact REBCO HTS, 350 MWe) with full CAS breakdown and LCOE $140–$550/MWh (`knowledge/sources/tea_dt_mfe_cost_analysis/`, Araiinejad & Shirvan 2025)
- CAS methodology: Full COA 20–27, 90–98 framework applicable to HTS tokamaks (`knowledge/sources/tea_dt_mfe_cost_analysis/`; `knowledge/sources/aries_cost_account_documentation/`)

**Missing**:
- HH380 power plant design specifications (power output, size, plant layout)
- Any company-disclosed LCOE targets (CEO statement "reduce LCOE to thermal power level or lower" is aspirational, not quantified)
- Peer-reviewed papers with plasma parameter details for HH170

**Gaps**:
- HH380 power plant specs (power output, thermal efficiency, sizing) — proprietary — **blocking**
- Detailed plasma physics parameters (temperature, density, confinement time) for HH170 — not-yet-sourced — **important**
- Chinese-language technical disclosures beyond publicly captured sources — not-yet-sourced — **nice-to-have**

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial
**Available**:
- Novel full-HTS tokamak architecture is documented at HH70 level — all coils REBCO, operating at 20 K, with demonstrated engineering feasibility (sciencedirect pii-s092037962500537x)
- AI-based plasma control is confirmed as operational on HH70 and cited as enabling steady-state (energy-singularity-overview.md; Xinhua iter-02 source)
- The closest cost analog (ARAI/ARC, `knowledge/sources/tea_dt_mfe_cost_analysis/`) uses identical magnet technology (REBCO, ~same field targets) and D-T fuel — functions as a validated template for system function modeling
- Steady-state operation confirmed vs. pulsed: eliminates pulsed-power cost issues
- Heating on HH70: ICRF confirmed as primary, electron gun for pre-ionization — no ECRH, LHCD, or NBI mentioned

**Missing**:
- Heating plan for HH170 and HH380 (ICRF alone is unlikely at higher power levels; NBI or ECRH may be required)
- Energy conversion pathway (no disclosure of thermal cycle type: steam Rankine assumed by analogy)
- Divertor design and exhaust handling strategy (standard challenge for compact high-field tokamaks)
- Recirculating power fraction (critical for net electric calculation)
- Alpha-heating fraction at Q > 10 (derivable from physics, but no company disclosure)

**Gaps**:
- Heating system design for HH170/HH380 — proprietary — **important**
- Energy conversion pathway specifics (cycle type, coolant, interface with blanket) — proprietary — **important**
- Divertor/exhaust design — proprietary — **important**
- Recirculating power fraction — derivable (from Q and heating efficiency assumptions) — **important**

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial
**Available**:
- **HTS magnets (TF/PF/CS full-REBCO)**: TRL 6 — Jingtian prototype demonstrated 21.7–22.4 T, and HH70 operated a full 26-coil set at 2.5 T. Full-power coil set for HH170 (25 T) not yet built. Analogous to CFS SPARC TFMC (20.1 T) which was TRL 5–6.
- **AI plasma control**: TRL 5–6 — demonstrated on HH70 at 1,337 seconds; not yet validated at burning plasma conditions.
- **ICRF heating**: TRL 7 — well-established on HH70 and prior tokamaks globally.
- **Steam Rankine cycle (assumed BOP)**: TRL 9 — mature technology applicable by analogy.
- **D-T fuel cycle**: TRL 4–5 — ITER program basis; Energy Singularity has not run D-T in any device.
- The TEA analog (`knowledge/sources/tea_dt_mfe_cost_analysis/`) acknowledges low TRL for "tritium handling systems, advanced heat exhaust solutions, and high-field HTS magnets" and treats NOAK as bypassing TRL constraints.

**Missing**:
- TRL assessment from Energy Singularity (no company disclosure)
- Tritium handling and breeding maturity for this specific design
- Neutron shielding / first-wall design (no disclosure — first wall will need radiation-hardened materials)
- Remote maintenance system design (no disclosure)

**Gaps**:
- Blanket/tritium breeding subsystem maturity — proprietary/TBD — **blocking**
- Neutron shielding and first-wall design maturity — proprietary/TBD — **blocking**
- Remote handling / maintenance system design — proprietary — **important**
- Tritium handling system maturity (HH380-specific) — proprietary — **important**

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial
**Available**:
- REBCO HTS tape: primary supplier identified as Shanghai Superconductor; conductor specs known (12 mm wide, 230 μm thick, 10 mm REBCO core) (energy-singularity-overview.md)
- Domestic localization rate >96% for HH70 — strong China-domestic supply chain signal (energy-singularity-overview.md; Xinhua iter-02)
- Material costs for D-T HTS tokamak from cost analog: V-4Cr-4-Ti ($37/kg), SS316 LN ($10/kg), FLiBe ($154/kg), tungsten ($29/kg), copper ($8.3/kg), REBCO tape (per ARC/ARAI study) (`knowledge/sources/tea_dt_mfe_cost_analysis/`)
- REBCO tape volume for ARC-equivalent: ~5,730 km of 70 kA cables used as analog basis (`knowledge/sources/tea_dt_mfe_cost_analysis/`)

**Missing**:
- Blanket material specification (no disclosure — lithium ceramic, WCCB, LiPb, or other unknown)
- REBCO tape production capacity at GW-scale deployment (current Shanghai Superconductor output unknown)
- Tritium supply chain for D-T operation (standard gap for all pre-burning concepts)
- Vanadium alloy or alternate structural material choice for HH380

**Gaps**:
- Blanket material and supply chain — proprietary/TBD — **blocking** (resolves only when blanket design disclosed)
- REBCO tape production scale-up pathway and cost curve for GW deployment — not-yet-sourced — **important**
- Tritium supply chain and initial inventory cost — derivable (from standard D-T fuel cycle models) — **important**
- China-specific REBCO cost vs. Western sources (affects LCOE for non-Chinese deployments) — not-yet-sourced — **nice-to-have**

---

### 5. LCOE Parameter Extraction
**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Net electric output (analog) | 350 MWe (ARAI) / 500 MWe (TEA base case) | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
| Thermal power (analog) | 1,000–1,500 MWth | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
| Thermal efficiency (assumed Rankine) | ~33% | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
| OCC (direct + indirect, D-T HTS tokamak) | $7,100–$14,900/kW | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
| Total OCC (with owner's cost) | $8,800–$22,200/kW | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
| Capacity factor (NOAK assumption) | 0.5–0.7 | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
| LCOE (NOAK D-T MFE HTS tokamak) | $140–$550/MWh | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
| Fixed O&M | $5–$12/MWh | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
| Variable O&M | $30–$170/MWh | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
| Annual equipment maintenance | $19–$63/MWh | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
| Power core replacement cost | $11–$107/MWh | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
| Decommissioning | 5% of total capital | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
| Discount rate | 6% | `knowledge/sources/tea_dt_mfe_cost_analysis/` | h |
| Plant lifetime | 30 years | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
| Magnet cost fraction (Account 22.13) | Dominant share of Account 22 | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
| REBCO tape for compact HTS tokamak | ~5,730 km of 70 kA cables (ARC basis) | `knowledge/sources/tea_dt_mfe_cost_analysis/` | l |
| Supplemental heating cost | ~$2.5/W | `knowledge/sources/tea_dt_mfe_cost_analysis/` | l |
| Cryosystem cost | ~$300/kW | `knowledge/sources/tea_dt_mfe_cost_analysis/` | l |
| Performance target (Q) | Q > 10 (HH170), commercial Q >> 10 | dossier / energy-singularity-overview.md | m |
| Operation mode | Steady-state | dossier | h |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| HH380 rated power output | proprietary | blocking | No company disclosure; must use ARC/ARAI analog (~350 MWe) with explicit caveat |
| Blanket design and TBR | proprietary | blocking | Structurally unresolvable before HH380 engineering phase; blanket type drives tritium self-sufficiency and breeding heat |
| Neutron wall loading and first-wall lifetime | proprietary | blocking | Required for replaceable-component cost and downtime estimate |
| Energy conversion cycle (coolant, turbine inlet temperature) | proprietary | important | Rankine assumed; supercritical CO2 possible for higher efficiency — affects thermal efficiency by ~5–10 pts |
| Recirculating power fraction | derivable | important | Derivable from Q and heating efficiency; ~15–25% typical for compact HTS tokamak |
| Heating power and system efficiency (HH170/HH380) | proprietary | important | Only ICRF confirmed for HH70; higher-power HH380 heating not disclosed |
| Capacity factor basis (Energy Singularity-specific) | derivable | important | Can use fleet analog (0.5–0.7) but concept-specific plasma disruption rate and maintenance cycle unknown |
| REBCO tape unit cost at production scale | not-yet-sourced | important | Cost reduction trajectory from Shanghai Superconductor not publicly available; ARC assumed $87.5/m |
| Tritium startup inventory and cost | derivable | important | Standard D-T assumption: ~5–10 kg; cost depends on CANDU/fission supply chain |
| Chinese vs. Western supply chain cost differential | not-yet-sourced | nice-to-have | >96% domestic localization may create cost advantage (or disadvantage for international deployment) |
| Indirect cost multiplier (China construction vs. US/EU) | not-yet-sourced | nice-to-have | ARAI uses US cost data; Chinese construction labor rates differ substantially |

---

## Source Recommendations

- **ARAI/ARC TEA** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): Already integrated. This is the primary cost analog for HH380 — compact REBCO HTS D-T tokamak, NOAK basis. Reduces the `blocking` classification of HH380 power specs to a bounded `important` gap once analog assumptions are made explicit.

- **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`): Already read. Provides the historical CAS framework (Accounts 20–27, 90–98) underlying the TEA analog; useful for structuring the LCOE model but adds no HTS-specific values not already in the TEA source. Explicitly disqualified as a concept-specific data source — it does not contain plasma parameters, material choices, or cost estimates relevant to Energy Singularity's machines beyond what the 2025 TEA paper already incorporates.

- **Energy Singularity HH70 commissioning paper** (Fusion Engineering and Design, 2025, doi:10.1016/j.fusengdes.2025.115341): Full text paywalled; abstract only captured in iter-03. Covers engineering design and commissioning of HH70 but not D-T blanket, power conversion, or LCOE — low priority for gap resolution. Flag as `not-yet-sourced` if full text becomes accessible; it may provide updated coil current, inductance, or plasma-facing material specs.

- **Energy Singularity HH70 magnet system paper** (Superconductivity, 2024, doi:10.1016/j.supcon.2024.100119): Paywalled. May contain additional REBCO tape cost or engineering data relevant to §4. Low-to-medium priority — search OSTI or preprint servers.

- **CFETR blanket design studies** (China Fusion Engineering Test Reactor): Energy Singularity's HH380 blanket is likely to draw on CFETR's WCCB/HCCB/LiPb work. Search OSTI or IAEA Nuclear Data Services for "CFETR blanket 2024 2025" — `not-yet-sourced`, unverified existence of public English-language design studies.

- **CFS SPARC plant study / ARC design documentation**: SPARC is the closest Western analog to HH170 (similar field, similar Q target). Published SPARC physics design papers (Ji 2022, Rodriguez-Fernandez 2022 series in Journal of Plasma Physics) may provide plasma parameter analogs derivable for HH170. Search via OSTI — `not-yet-sourced`, high-value for §3 subsystem maturity and §5 recirculating power.

- **PyFECONS** (`/home/reid/PyFECONS`): Not read for this assessment — IFE and large-MFE heritage, may not have compact HTS tokamak configurations. Applicable for CAS validation of fleet analog cost outputs but likely less direct than the already-integrated TEA source. Disqualified as a primary source for this concept without further investigation.

---

## Summary

Proceed to full D1+ analysis. The concept-scoped sources establish physics differentiation (all-REBCO coil set, 22.4 T demonstrated, Q>10 target, steady-state) and company context. The `knowledge/sources/tea_dt_mfe_cost_analysis/` fleet source provides a directly applicable NOAK cost framework for a compact REBCO HTS D-T tokamak ($140–$550/MWh LCOE, $8,800–$22,200/kW OCC, CF 0.5–0.7), which should be used as the primary LCOE basis with explicit "analog from ARC/ARAI" caveats. The three blocking gaps (HH380 specs, blanket/TBR, neutron shielding) are proprietary or structurally unresolvable before the HH380 engineering phase (~post-2030), so they should be documented as uncertainty sources that widen the LCOE range rather than treated as sourcing failures. The analysis is well-positioned to characterize both what is novel about Energy Singularity's approach and why cost uncertainty remains high.

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready"
blocking_count: 3
important_count: 5
counting_method: "deduplicated across all sections: blocking = HH380 power specs, blanket/TBR design, neutron shielding/first-wall design; important = heating plan HH170/HH380, energy conversion pathway, recirculating power fraction, capacity factor basis, REBCO scale-up cost"
section_coverage:
  availability_of_data:       "Partial"
  system_function:            "Partial"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Partial"
```