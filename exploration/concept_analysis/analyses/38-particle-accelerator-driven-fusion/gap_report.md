# Gap Assessment: Particle Accelerator-Driven Fusion (SHINE Technologies)

## Overall Readiness
**Rating**: Significant Gaps (for power-LCOE purposes)

**Summary**: SHINE is unique in the catalog: the only **commercially operating** fusion system, with a mature commercial product line (Mo-99, Lu-177, FLARE neutron services) and NRC licensing in place. Technical *concept* documentation is good (peer-reviewed Piefer 2011, NRC license documents, Wikipedia, company FLARE materials). However, this is a commercial radioisotope producer, not a power plant — and beam-target D-T fusion has a hard physics ceiling at Q ≈ 10⁻³, two-to-three orders of magnitude below break-even. The standard LCOE framework does not apply: SHINE produces no electricity and has no design pathway to net power output. The correct economic model is cost-per-Curie of medical isotope, not $/kWh. For the catalog's power-generation TEA comparison, the LCOE result is formally ∞ — SHINE is categorically outside the power-generation competition. For its actual isotope-production business model, operational economics (beam current, electrical power consumption, facility capex, Mo-99 yield) are entirely proprietary commercial information.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Good (technical concept) / Poor (operational economics)

**Available**:
- Piefer et al. 2011 (ANL Mo-99 proceedings): peer-reviewed description of beam-target D-T architecture for isotope production.
- SHINE technology overview: FLARE specifications — 5×10¹³ D-T reactions/s, ≤300 kV beam voltage, 14.1 MeV neutrons, continuous steady-state operation.
- NRC licensing documents (ML13172A262, ML15258A372) publicly accessible.
- Wikipedia entry covering accelerator architecture, subcritical LEU assembly, NRC licensing history.
- LIBRTI commercial deployment with UKAEA (2024 press release).

**Missing**:
- Beam current (mA) — SHINE has not publicly disclosed.
- Total facility electrical power consumption.
- Mo-99 production yield per beam-hour.
- Facility capital cost.
- OPEX breakdown.

**Gaps**:
- No published beam current, electrical power, or production yield — `proprietary` — **blocking** (these define the cost-per-Ci denominator).
- No published facility capex — `proprietary` — **blocking**.
- No independent TEA of accelerator-driven fusion as a power concept (academic literature only confirms the Q ceiling) — `derivable` — nice-to-have.

---

### 2. Challenges in Capturing System Function
**Coverage**: Good (physics is well-understood) / Poor (economics)

**Available**:
- Beam-target D-T physics is thoroughly characterized: thick-target fusion probability per deuteron, Coulomb-scattering stopping range, D-T cross-section peak near 120 keV CM (~240 keV lab).
- Physics-derived effective Q in the range 10⁻³–10⁻² is robust to beam-current optimization (Q is bounded by the integrated fusion-vs-scattering cross-section ratio, not by current).
- Operational reality: SHINE is a net electricity *consumer* on grid power, by design.

**Missing**:
- Annual electrical operating cost (depends on undisclosed beam power consumption).
- Operating economics under the cost-per-Ci framework.
- Mo-99 / Lu-177 revenue model details (proprietary commercial).

**Gaps**:
- **LCOE framework does not apply** — `truly-unknown` — **blocking** (for the power-generation comparison; the meaningful question is cost-per-Ci, which requires the proprietary economics).
- **Beam power consumption** — `proprietary` — **blocking** (the recirculating-power analog for an isotope plant; sets operating cost).
- **Mo-99 production yield** — `proprietary` — **blocking** (revenue driver; sets the economic case).
- **NRC tritium possession limit and procurement logistics** — `proprietary / NRC docket` — important (binds scalability more than tritium unit cost).

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Good

**Available**:
- TRL assessments by subsystem: compact linear accelerator at ≤300 kV TRL 9 (commercially operating, industrial-class device); tritium gas target system TRL 9 (operating); subcritical LEU assembly TRL 8–9 (NRC-licensed); Mo-99 / Lu-177 extraction TRL 7–8 (operating since 2019, expanded with FLARE).
- FLARE described as "world's most powerful continuous fusion neutron system" (SHINE press release, 2024).

**Missing**:
- Scaling pathway to power-generation TRL: nothing. No published design study; this isn't a TRL gap, it's a categorical mismatch (beam-target D-T cannot reach Q ≥ 1 by physics).

**Gaps**:
- **Path to net energy is non-existent** — `truly-unknown` — **blocking** (for the power-generation comparison; this concept's TRL maturity is irrelevant because the destination isn't power).
- Lu-177 production yield and process maturity — `proprietary` — important.

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Good

**Available**:
- Tritium consumption: ~8 mg/year (derived from 5×10¹³ reactions/s rate) — operationally negligible (~$280/yr at $35,000/g). NRC possession limit is the binding constraint, not unit cost.
- Low-enriched uranium (LEU) supply: narrow but adequate qualified-supplier base (ConverDyn, Tenex) under NNSA oversight.
- Deuterium gas: commercial industrial supply, no constraint.
- Accelerator components (vacuum, ion sources, HV power supplies, beam optics): mature industrial supply (NEC, HVEE, Excelis).
- No HTS / beryllium / FLiBe required — SHINE is supply-chain-simple by virtue of not attempting plasma confinement.

**Missing**:
- Tritium possession limit at FLARE-scale operation (under NRC license amendments).

**Gaps**:
- LEU supply chain geopolitical risk (Russian supply chain) — `derivable` from NNSA reports — nice-to-have.
- Tritium possession limit at FLARE scale — `proprietary / NRC docket` — important.

---

### 5. LCOE Parameter Extraction
**Framing note**: Standard LCOE doesn't apply (SHINE is non-power). The available table below is what would be extractable *if* the catalog framework were adapted to cost-per-Ci for medical isotope production.

**Available Parameters**:

| Parameter | Value | Source | Confidence |
|---|---|---|---|
| D-T reaction rate | 5 × 10¹³ /s | SHINE FLARE materials | high |
| Beam voltage | ≤ 300 kV | SHINE / dossier | high |
| Neutron energy | 14.1 MeV | physics | high |
| Operation mode | Steady-state continuous | SHINE | high |
| Effective Q | ~10⁻³–10⁻² | thick-target physics | medium |
| Fusion power (derived) | ~141 W | derived from reaction rate | high |
| Tritium consumption | ~8 mg/yr | derived | medium |
| Net electrical output | 0 kWe | dossier (by design) | high |

**Missing Parameters**:

| Parameter | Gap Type | Criticality |
|---|---|---|
| Beam current (mA) | proprietary | blocking |
| Total facility electrical consumption | proprietary | blocking |
| Facility capital cost | proprietary | blocking |
| Mo-99 production yield | proprietary | blocking |
| Capacity factor / beam-on-time | proprietary | important |
| OPEX breakdown | proprietary | important |
| Lu-177 production rate | proprietary | important |
| Tritium NRC possession limit | proprietary / NRC | important |
| FLARE service pricing | proprietary | nice-to-have |

---

## Source Recommendations

1. **NRC public docket** (ML13172A262, ML15258A372 plus subsequent amendments) — may contain operational beam parameters, possession limits, and updated facility descriptions.
2. **Piefer et al. 2011 full text** (ANL Mo-99 symposium proceedings, not yet directly extracted) — may contain beam current and neutron yield specifications.
3. **NorthStar Medical Radioisotopes / SHINE public filings** — comparable non-reactor Mo-99 producer; facility capital cost benchmark of ~$30–150M is the publicly stated range.
4. **CNSC (Canadian NRC) NRU operational records** for analog isotope-plant OPEX structure.
5. **SHINE SEC filings or commercial disclosures** if/when the company IPOs or issues public financial statements.

---

## Summary

**Proceed to full analysis**: No — but for a categorical reason, not a data-availability one.

SHINE is the only catalog concept that does not aim for power generation. Beam-target D-T fusion has a hard physics ceiling at Q ~ 10⁻²; no engineering optimization changes the fundamental ratio. The correct framework for SHINE is cost-per-Ci of medical isotope, not $/kWh. The catalog should disposition SHINE as the "validated lower bound on D-T fusion economics at Q < 1" — useful as a calibration point but not a power-generation competitor. For the standard LCOE comparison, the disposition is LCOE = ∞ (categorical disqualification), and the framework's CrossAxisSanity tests already exclude it correctly via the Technical Feasibility floor (1.0, no-data) and the absence of any net-power architecture.

Were the catalog ever expanded to include "useful neutron flux" or "medical isotope production" as additional evaluation axes, SHINE would likely rank highly. That work is out of scope for the current power-LCOE focus.

---

## Structured summary (machine-readable)

```yaml
overall_rating: "Significant Gaps (for power-LCOE purposes)"
blocking_count: 4
important_count: 4
counting_method: "section_5_missing_parameters"
section_coverage:
  availability_of_data:       "Good (technical concept) / Poor (operational economics)"
  system_function:            "Good (physics is well-understood) / Poor (economics)"
  subsystem_maturity:         "Good"
  materials_supply_chain:     "Good"
  lcoe_parameter_extraction:  "Unknown"
```
