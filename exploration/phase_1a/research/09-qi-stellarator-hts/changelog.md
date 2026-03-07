# QI Stellarator - HTS (D-T) — Changelog

## Iteration 1 — 2026-03-06

### Changes
- **All 12 columns populated from scratch** (first iteration):
  - Confinement Family: `MFE` (high)
  - Confinement Concept: `Stellarator (QI)` (high)
  - Fuel: `D-T` (high)
  - Primary Heating: `RF (ECRH)` (medium) -- inferred from W7-X heritage
  - Energy Capture: `Thermal (unspecified)` (medium) -- inferred from WCLL blanket
  - Plasma State: `Burning` (medium) -- inferred from commercial plant target
  - Magnet Type: `HTS (3D stellarator)` (high)
  - Tritium Breeding: `LiPb blanket` (high)
  - Neutron Management: `Integrated blanket/shield` (medium) -- inferred from WCLL dual-purpose design
  - Operation Mode: `Steady-state` (high)
  - Repetition Rate: `N/A` (high)
  - Driver Technology: `3D HTS stellarator coils (REBCO, 20 T)` (high)
- **19 sources consulted** across Proxima Fusion website, press releases, trade press, and technical references
- **No conflicts discovered** -- all sources consistent

### Gap Assessment
- **Columns still incomplete**: Primary Heating, Energy Capture, Plasma State, Neutron Management (all medium confidence)
- **Recommendation**: A second iteration focused on accessing the full Stellaris paper (DOI: 10.1016/j.fusengdes.2025.114868) would likely resolve all 4 medium-confidence values in one pass. If the paper remains inaccessible, conference presentations or slides from Proxima team members may provide the needed specifics. Another iteration is recommended only if the paper can be accessed; public web sources have been thoroughly searched.

## Iteration 2 — 2026-03-06

### Changes
- **No vocabulary values changed** -- all 12 columns retain their iter-1 values and confidence levels
- **Summary enriched** with quantitative power balance: 2.7 GW fusion -> ~3.1 GW thermal -> ~1 GW net electrical (~32% plant efficiency), plasma beta ~2.76%
- **Summary enriched** with RWE/Bavaria/IPP MoU (Feb 2026): Alpha demo at Garching (~EUR 2B, 2031), Stellaris commercial at Gundremmingen
- **Primary Heating notes upgraded**: Helios stellarator (ArXiv 2512.08027v1) confirms ECRH at 170 GHz for comparable QI design, strengthening inference
- **Energy Capture notes upgraded**: Helios confirms steam Rankine at 635C; Stellaris ~32% plant efficiency consistent with Rankine
- **Plasma State notes upgraded**: Helios requires only 1 MW ECRH in ignited phase, supporting burning/ignition classification
- **Neutron Management notes upgraded**: Stellaris paper scope confirmed to include comprehensive shielding analysis; Helios multi-layer shield documented for comparison
- **Operation Mode citation upgraded**: RWE MoU explicitly describes "reliably and continuously"
- **Magnet Type notes upgraded**: magnet factory with up to 1,000 jobs planned
- **8 new sources added** (KIT repository, RWE MoU PR, ANS Newswire, Helios ArXiv, Proxima W7-X blog, NEI Magazine, Fusion Energy Insights, Wikipedia)
- **No conflicts discovered** -- all sources consistent across both iterations

### Gap Assessment
- **Columns still incomplete**: Primary Heating, Energy Capture, Plasma State, Neutron Management (all medium confidence -- unchanged from iter-1)
- **Recommendation**: Further public web iteration is unlikely to help -- iter-02 performed 13 targeted searches and found no new direct statements for the 4 medium-confidence columns. The full Stellaris paper (DOI: 10.1016/j.fusengdes.2025.114868) remains the single source most likely to resolve all 4 gaps. If the paper can be obtained (institutional access, preprint, or author request), one more iteration would likely complete the dossier to high confidence. Without the paper, another web-search iteration is not recommended.
