# Gap Assessment: Large-Scale Stellarator

Written to: `analyses/10-large-scale-stellarator/gap_report.md`

---

## Overall Readiness: **Mostly Ready**

The data is sufficient to write all five D1+ qualitative sections and build a credible first-pass LCOE model. Nothing is blocking. Here's the summary by section:

### Section-by-Section

| Section | Coverage | Key Gap | Gap Type |
|---|---|---|---|
| 1. Availability of Data | Moderate | CDR content is gated; HSR4/18 cost study not captured | not-yet-sourced / proprietary |
| 2. System Function Challenges | Partial | Power cycle type unknown; remote maintenance architecture not public | proprietary |
| 3. Subsystem Maturity | Partial | TRL data is inferrable but no Gauss self-assessment exists | proprietary |
| 4. Materials / Supply Chain | Good | HTS tape (26M m = 13–26× global annual production) is a clear bottleneck; He supply not analyzed | not-yet-sourced |
| 5. LCOE Parameters | Partial | No CAS cost breakdown; €15–18B FOAK total is the only published figure | proprietary |

### For the LCOE Model
- **What you have**: Total FOAK cost (€15–18B), power output (3 GW → 1 GW), machine geometry, supply chain quantities (35,000T SC coils, 26M m HTS), 5-year blanket replacement cycle, 40-year magnet life, steady-state operation
- **What you'll need to assume**: Blanket type (HCPB/DCLL bracket), power cycle efficiency (~33%), capacity factor (~85–90%), annual O&M from first-principles

### Two High-Value Quick Wins
1. **Read the Bongiovì 2022 HCPB paper** (confirmed URL in dossier) — power cycle efficiency and blanket thermal-hydraulics
2. **Read the CIEMAT DCLL paper** (confirmed URL in dossier) — alternative blanket TBR and thermal parameters

### Most Impactful `not-yet-sourced` Item
**HSR4/18 cost study (Beidler et al. ~2001, *Nuclear Fusion* 41)** — almost certainly contains subsystem cost fractions for the direct GIGA predecessor. This is the difference between a single-number LCOE model and a decomposed parametric one.
