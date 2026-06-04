# Validation Reviews

Human-authored reviews of selected concepts' agentic-pipeline outputs, comparing each concept's `model_setup.py` (or bespoke cost model) against the primary published source or an independent reference. Each review grades the agentic synthesis (PASS / FAIL), enumerates findings, and proposes per-concept and framework-level corrective actions.

These are reference artifacts for cross-corpus reporting — not part of the pipeline run loop.

## Index

| Concept | Verdict | Headline finding |
|---|---|---|
| [07 — Pacific Fusion MagLIF](07-pacfusion-maglif-comparison.md) | **FAIL** | Wrong primary source (2006 Sandia Z-IFE vs 2025 Pacific Fusion AMPS); 35 MW driver claimed to deliver 1000 MWe net (~20× too low); 2006-dollar Z-IFE LTD costs applied as 2024-dollar Pacific Fusion IMG costs; misrouted CAS22 sub-account. |
| [11 — Realta Magnetic Mirror](11-realta-magnetic-mirror-comparison.md) | **FAIL** | 500 MWe target sourced from 1983 MARS study, not Realta; mixed parameters across incompatible Frank et al. operating points; commercial-scale BOP loads on a pilot plant; Frank-corrected LCOE = 327 $/MWh vs reported 104 $/MWh (+214%). |
| [12 — OpenStar Levitated Dipole](12-openstar-dipole-comparison.md) | **FAIL** | AI-synthesis LCOE within 25% of handwritten model by coincidence; wrong-architecture analog (SPARC tokamak coil for dipole); missing TBR closure check (Li2O blanket yields 1.1 vs required 1.33); top-down point estimates with no bottom-up audit trail. |
| [17a — Xcimer KrF Hybrid Direct Drive](17a-xcimer-hybrid-direct-drive-comparison.md) | **PASS** | `model_setup.py` within ~10% of independent reference ($132 vs $119.6/MWh). Remaining gap is framework-level: CAS220108 misclassification (IFE target factory on blanket schedule), PbLi-anchored V+B applied to FLiBe, and target-factory cost scaling with net electric rather than throughput. |

## Cross-cutting framework-level recommendations

Several findings recur across reviews and point to fixes in `1costingfe` itself rather than per-concept authoring:

- **Source-freshness check** — automated detection when the latest version of a pinned primary source has been ingested but the model is still anchored to an older version (concepts 07, 11).
- **Physics-closure checks** — Q closure for steady-state concepts (concept 11), driver closure for pulsed concepts (concept 07), TBR closure for D-T concepts (concept 12). Each is a cheap one-line invariant that would have caught a specific failure mode.
- **`cost_basis_year` parameter** — normalize historical-dollar cost overrides to the framework's current-year basis (concept 07; class affects every concept pulling pre-2024 source data).
- **CAS22 sub-account routing validation** — warn when an override's magnitude is more than ~5× the framework's auto-computed value for the same account (concept 07).
- **Branch CAS220108 on confinement family** — IFE target factory needs a different replacement schedule than the MFE divertor that shares the account ID (concept 17a; affects every IFE concept).
- **IFE V+B cost on a defensible FOAK anchor + LR** — replace the MFE-tokamak / PbLi extrapolation with an LLNL GEM (HYLIFE-class) anchor (concept 17a; affects every IFE concept).
- **Target-factory cost scaled by throughput, not net electric** — anchor on capsules-per-year (rep rate × availability × lifetime), not on net electric output (concept 17a; affects every IFE concept).
- **User-settable blanket replacement interval** — let `model_setup.py` declare e.g. `blanket_replacement_yr = 30` so developer claims (Xcimer's 30-year structural chamber) can be carried with documented uncertainty (concept 17a).
- **Dual-form BOP load API** — allow `p_cool`, `p_trit`, `p_pump` to be specified as fraction-of-P_fus rather than scalar MW so pilot-scale plants don't inherit commercial-scale BOP loads (concept 11; affects every sub-commercial concept).

## Missing artifacts

- `17a-xcimer-cost-comparison.png` — referenced in the concept 17a review but not yet committed. Generate from the cost composition data and place alongside the review.
