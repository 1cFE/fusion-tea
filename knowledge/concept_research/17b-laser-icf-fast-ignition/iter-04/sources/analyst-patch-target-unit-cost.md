---
source: "analyst-derived"
source_type: "analyst-patch"
extracted_at: "2026-06-08T23:00:00+00:00"
author: "Mallory Snowden"
provenance_pr: "fusion-tea PR #68 (laser-IFE target cost audit)"
patch_class: "spec_override"
---

# Analyst-Derived Override: target_unit_cost = $0.80 per shot

**Why this source exists.** This is not a primary published source about Focused
Energy. It is an *analyst patch source* that captures a model parameter the
agent cannot derive from public disclosures, with the provenance, rationale,
and machine-readable directive needed for the cold-start `analyze` + model-setup
chain to regenerate the override without losing it.

The patch was originally applied directly to `model_setup.py` in PR #68 (the
laser-IFE target cost audit). Without this source, a future cold-start
`analyze --force` would re-derive `target_unit_cost` from library defaults
(or set no value at all), silently dropping a value with direct LCOE impact.

## Why a per-shot target cost is required

For a 10 Hz IFE plant operating at 80% availability over a 30-year lifetime,
the target factory must deliver approximately:

    10 Hz × 0.80 × 30 yr × 31.5e6 s/yr = 7.56 × 10⁹ capsules

`target_unit_cost` is the per-capsule manufacturing cost that, multiplied by
this throughput, sets the CAS80 annualized fuel-cycle cost contribution. With
no value, the fuel-cycle term either underflows to zero (silently understating
LCOE) or library defaults assign a generic D-T cost that doesn't reflect the
cone-in-shell complexity.

## Why $0.80 per shot for Focused Energy specifically

Focused Energy's Pearl™ target is a cone-in-shell D-T capsule (proton fast
ignition geometry), which is structurally more complex than a symmetric D-T
capsule and significantly more complex than an indirect-drive hohlraum-mounted
capsule. The cost derivation:

1. **NOAK reference.** Meier 2006 ("HYLIFE-II target factory economics") estimates
   $0.30-$0.50 per symmetric D-T capsule at NOAK rates in 2006 dollars for
   indirect-drive targets.

2. **CPI adjustment 2006 → 2024.** US CPI rose ~52% over 2006-2024
   (BLS data, 201.6 → 308.4). Mid-range $0.40 × 1.52 = $0.61 in 2024 dollars.

3. **Cone-in-shell complexity multiplier.** Norreys et al. (HiPER conceptual
   design) and Focused Energy's own technical materials describe cone-in-shell
   fabrication as substantially more complex than symmetric direct-drive
   capsules. Applying a 1.3× complexity penalty: $0.61 × 1.3 ≈ $0.80.

4. **Sensitivity.** Output is sensitive to NOAK volume assumptions. The
   uncertainty band is roughly $0.50-$1.20 per capsule. $0.80 is the central
   estimate.

## Cross-reference to analysis

This value should appear in:

- **Section 5 (LCOE-Relevant Parameters)** as a named parameter with the above
  rationale and uncertainty band.
- **`model_setup.py`** as `spec=dict(target_unit_cost=0.80, ...)`.

The value is **NOT** a CAS account override (it does not belong in the Section 5b
six-field override registry). It is a spec value that scales the CAS80 fuel-cycle
term via the model's internal target-throughput calculation.

## Model directive (machine-parseable)

When generating `model_setup.py`, the model-setup step MUST translate this
directive into the `spec=dict(...)` argument verbatim. Do not paraphrase, do not
recompute, do not omit.

```yaml
model_directives:
  spec_overrides:
    target_unit_cost: 0.80   # $/shot — cone-in-shell D-T NOAK basis
  rationale: "Meier 2006 IFE target economics, CPI-scaled to 2024, with 1.3× cone-in-shell complexity multiplier"
  provenance: "derived"
  source_anchors:
    - "Meier 2006 (HYLIFE-II target factory economics)"
    - "BLS CPI 2006-2024 (52% adjustment)"
    - "Norreys et al. HiPER conceptual design (complexity multiplier)"
  uncertainty_band: "0.50–1.20 $/shot"
```

## Sources cited

- **Meier, W. R. (2006)**. "Target factory economics for inertial fusion energy."
  HYLIFE-II program documentation, LLNL. Anchor for the NOAK per-target cost.
- **Norreys, P. A. et al.** "Fast ignition for the HiPER project." Plasma Physics
  and Controlled Fusion. Establishes cone-in-shell vs symmetric complexity delta.
- **US Bureau of Labor Statistics CPI series** (CPI-U, all items, 2006 → 2024).
  Used for the 1.52× currency adjustment.
- **Focused Energy public technical materials.** Confirms Pearl™ cone-in-shell
  geometry; no per-capsule cost has been disclosed by the company.

## Maintenance

If Focused Energy publishes a per-target cost, this source should be
**superseded** (not deleted — add a successor source citing the company
disclosure, and mark this file as historical). The agent should prefer the
direct disclosure over this analyst estimate.
