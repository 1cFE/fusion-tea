Research complete. Here's a summary of findings:

## Key Results

All 12 differentiation columns filled. Three corrections from the initial CSV:

1. **Confinement Family**: Changed `MIF` → `MFE` — Z-pinch uses self-generated magnetic fields, no external compression driver. Schema explicitly classifies Z-pinch as MFE.
2. **Published Machine/Plant?**: Changed `No` → `Yes` — the 2023 "Engineering Paradigms" paper in Fusion Science & Technology describes a 190 MWt reactor concept with specific parameters.
3. **Confinement Concept**: Confirmed as `Z-pinch (sheared-flow)` — exact schema vocabulary match.

## Column Summary

| Column | Value | Confidence |
|--------|-------|-----------|
| Confinement Family | MFE | high |
| Confinement Concept | Z-pinch (sheared-flow) | high |
| Fuel | D-T | high |
| Primary Heating | Ohmic (self-pinch) | high |
| Energy Capture | Thermal (steam) | medium |
| Plasma State | Pinch | high |
| Magnet Type | Self-confined | high |
| Tritium Breeding | LiPb blanket | high |
| Neutron Management | Integrated blanket/shield | high |
| Operation Mode | Pulsed | high |
| Repetition Rate | ~10 Hz | high |
| Driver Technology | Pulsed power (sheared-flow Z-pinch) | high |

## Only Gap: Energy Capture confidence

The "steam" cycle detail comes from a third-party blog summary of the paywalled Engineering Paradigms paper. Direct paper access would confirm. All other columns are high confidence from authoritative sources.

Outputs written to:
- `dossier.md` — full column-by-column findings with citations
- `sources/` — 4 source summary files saved
