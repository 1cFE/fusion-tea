# Changelog: Orbital Levitated Dipole (D-He3) — Zephyr Fusion

## Iteration 1 — 2026-03-07

### Changes
- **Confinement Family**: New → `MFE` (high confidence) — from YC launch page + schema
- **Confinement Concept**: New → `Levitated dipole (orbital)` (high confidence) — from YC launch page
- **Fuel**: New → `D-He3` (medium confidence) — from baseline CSV + Hasegawa heritage; not explicitly confirmed on YC page
- **Primary Heating**: New → `RF (ECRH)` (low confidence) — inferred from LDX heritage only; Zephyr has not disclosed
- **Energy Capture**: New → `TBD` (low confidence) — no company disclosure; major gap
- **Plasma State**: New → `Sustained` (medium confidence) — inferred from steady-state + sub-ignition expectations
- **Magnet Type**: New → `HTS (levitated dipole)` (high confidence) — from YC launch page
- **Tritium Breeding**: New → `N/A (aneutronic)` (medium confidence) — D-He3 with no blanket; ambiguity with Self-bred (DD side)
- **Neutron Management**: New → `Reduced (D-He3)` (medium confidence) — standard D-He3 classification
- **Operation Mode**: New → `Steady-state` (high confidence) — from baseline CSV + inherent dipole physics
- **Repetition Rate**: New → `N/A` (high confidence) — steady-state concept
- **Driver Technology**: New → `Orbital HTS dipole coil (meter-scale, Falcon 9 deployable)` (high confidence)

### Sources Found
- YC launch page (primary company source)
- NASASpaceFlight forum discussion (community critique)
- Levitated dipole technical background compilation (LDX, Hasegawa, arxiv)

### Gap Assessment
- **Columns still incomplete**: Energy Capture (TBD), Primary Heating (low), Fuel (medium — unconfirmed), Tritium Breeding (medium — ambiguous), Plasma State (medium)
- **Recommendation**: Another iteration is warranted, focused on: (1) Zephyr conference presentations or ARPA-E filings for energy capture and heating details, (2) founder interviews or podcasts that might disclose fuel cycle and power conversion plans. The company is very early-stage (2 employees, no prototype) so public technical detail may remain sparse. Priority queries: "Zephyr Fusion ARPA-E", "Galen Burke fusion presentation", "Edward Hinson orbital dipole".

## Iteration 2 — 2026-03-07

### Changes
- **Energy Capture**: `TBD` (low) → `Direct (charged particle)` (low) — upgraded from TBD based on strong physics inference: D-He3 puts ~85% energy in charged particles, Hasegawa 1987 designed dipole separatrix geometry for direct conversion, no thermal infrastructure possible on orbital platform. Still low confidence as Zephyr has not confirmed.
- **Primary Heating**: Confirmed `RF (ECRH)` (low) — no change. Added detail on three plausible methods from dipole reactor literature (ECRH, ICRH, NBI) with trade-offs.
- **All other columns**: Confirmed at previous values. No upgrades or conflicts.
- **New sources**: iter-02/sources/dipole-reactor-heating-energy-conversion.md (academic reference on dipole heating/conversion), iter-02/sources/zephyr-fusion-web-sources-2026.md (comprehensive web survey confirming no new Zephyr disclosures)

### Gap Assessment
- **Columns still incomplete**: Energy Capture (low — physics inference only), Primary Heating (low — heritage inference only), Fuel (medium — unconfirmed by company), Tritium Breeding (medium — N/A vs Self-bred ambiguity), Plasma State (medium — no target Q disclosed)
- **Recommendation**: No further iterations recommended. All publicly accessible sources have been exhausted — no ARPA-E/DOE funding, patents, conference presentations, or detailed technical disclosures exist beyond the YC launch page. The remaining gaps cannot be resolved without new company disclosures. The dossier is as complete as publicly available information allows for this very early-stage (2-person, pre-prototype) company.
