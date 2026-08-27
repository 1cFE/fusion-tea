---
Status: completed
Scale: trivial
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-08-21
Updated: '2026-08-22'
---

# WI-031: Research round — second-arm values for the Item 6 A/B studies

Trivial-scale item: one `/research` session against admissible sources, no model change. Output: a research document in `knowledge/research/pending/` and, on approval, DI-XXX insights; each value below ends as a citation or an explicit "no source".

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — sealed; barred paths are not read. **No fallbacks [OWNER 2026-08-21]:** a value with no admissible source is reported as such, never estimated.

| value | consumer | what is needed | where to look first |
|---|---|---|---|
| sCO2 primary-coolant pumping power (`p_pump`) for a ~1 GWth helium-cooled blanket | Item 6 study 2 (arm-sco2) | MW or a fraction of thermal power, with the cycle stated | 1costingFE docs `CAS23_26_balance_of_plant.md`; concept dossiers 05 (Helios), 10, 20a/b, 21, 28; any sCO2 Brayton source ingestible via `/manage-sources` |
| arm-A `eta_th` provenance | study 2 (arm-rankine-paper vs arm-rankine-upstream) | confirm Stellaris's 1/3 is a single-element steam assumption (`stellaris-design-details.md:251`) and whether the paper states a cycle | Stellaris PDF/page images |
| fraction-of-Carnot at 4.5 K (`f_carnot_cryo`) | Item 6 study 1 (arm-nb3sn) | plant electrical power per watt at 4.5 K (ITER or W7-X cryoplant) | `cas22.py:690`, `CAS22_plant_systems.md:222-226` (capacity and cost only); W7-X cryoplant source in `09-qi-stellarator-hts/iter-02/`; ITER cryoplant power figure if ingestible |
| Nb3Sn winding-pack volume / `J_op` for a comparable coil set | study 1 (arm-nb3sn, `vol_cold_cryo`) | operating current density or winding-pack volume for an Nb3Sn stellarator or DEMO-class coil | EU DEMO / W7-X / HELIAS sources; **not** ARIES-CS |

Disposition rule: Item 6 study 2 runs after this round closes, carrying anything unsourced as a disclosed hold. WI-030 does not wait on this item.
