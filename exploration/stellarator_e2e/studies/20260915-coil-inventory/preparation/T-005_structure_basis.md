# T-005 structure basis

2026-09-15. [AGENT] Recommendation under delegated technical judgment; source facts and assumptions are separated below. No model edits or source registrations.

## Mass

[INHERITED] Lion 2021 §3.9 explicitly estimates **total coil support structure**, not casing alone: `knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/output.md:603–613`. Original `images/lion_2021_nf_stellarator_process.pdf-0012-18.png`, visually checked, prints `M_struct = 1.348 W_mag^0.78` (Eq56). It cannot establish local structural adequacy.

[INHERITED] Lion 2023 §2.3.7, `knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/output.md:1527–1541`, explicitly gives MJ and metric tonnes, but its original `images/lion_2023_phd_thesis_stellarator_systems_code_models.pdf-0076-08.png`, visually checked, prints the DIFFERENT fit `1.37 W_mag^0.76` (Eq2.89). The later fit must not be represented as confirmation of the earlier coefficient.

[AGENT] Retain the goal's Eq56 and adopt the thesis's unit convention as an explicit inference: `mass_kg = 1000 × 1.348 × (W_J/1e6)^0.78`. Coefficient dimensions are tonnes/MJ^0.78. At the unchanged111GJ anchor this gives **11,615.604t**; an equivalent anchored form uses11,615,604.483kg at111GJ. The later fit gives9,357.633t,19.4% lower: report it as model-form sensitivity, not tuning. Journal units remain indirectly supported.

[INHERITED] Stellaris printed27, visually checked in `T-004_stellaris_p27.png`, describes casings, inter-coil plates and central rings. Its63–200t values are cast-part weights; no complete counts or total mass are given. Preserve48×63t=3,024t only as the inherited casing-floor convention, never add it to the total. Cryogenic legs are not modeled in that analysis. No casing/inter-coil split is justified.

## Price and accounting

[INHERITED] WI035 design D5 carries$6/kg×3 fabrication=$18/kg from admitted1costingFE defaults. [AGENT] Use$18/kg as one transparent **all-in inherited fabricated-steel scenario**, not a validated316LN quotation; do not apply another fabrication factor. Nominal total=$209.081M; explicit rate sensitivities$9/$36 per kg give$104.540/$418.162M. These are judgment bands, not statistical confidence limits.

[AGENT] Put all electromagnetic coil supports once in CAS22.1.3. `models/library/analyses/mfe_account_costs.sysml:81–105` shows CAS22.1.5 currently mixes inter-coil supports with gravity supports, shields and base. Its formula cannot identify the overlap. Preserve its current-oracle$34.156M baseline magnitude only as a newly declared conservative **nonmagnet residual allowance**, retaining its existing scaling; expose0–100% of that allowance as accounting sensitivity. This deliberately reallocates an opaque budget and does not assert a sourced split. Cryogenic legs/base/shield coverage remains allowance-based. Alternative: retire the composite entirely and explicitly disclose these residuals unpriced; that lowers scope completeness.

## Acquisition

Native request `knowledge/research/requests/REQ-MCR-STRUCTURE-01.json`; run `runs/REQ-MCR-STRUCTURE-01/20260915T140055884498/return.json` returns BOUNDED_NEGATIVE after four searches, zero captures. No independent matching fabricated-steel rate found. This negative concerns additional acquisition; admitted mass equations remain usable with the disclosed inference. No barred source opened.
