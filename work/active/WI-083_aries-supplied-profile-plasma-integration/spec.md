---
Status: active
Scale: standard
Epic: ARIES model transfer experiment
Owner: transfer_physics_inventory
Created: 2026-09-21
Updated: 2026-09-21
---

# WI-083: Supplied-profile plasma integration

**Status:** source/design accepted; implementation in progress. **Date:** 2026-09-21. **Author:** transfer_physics_inventory.

## Requirements and authority

[INHERITED: owner continuation through coordinator] Implement actual forward plasma quantities from explicit supplied profiles and show reusable components through the native route. Parent owns registry and commits; this author owns only the assigned new model, case and isolated execution files. No baseline definition or original comparison changes.

- **R1 [INHERITED]:** Integrate the existing generic density equation, source sensitivity temperature family, declared species composition and normalized shell-volume measure to predict local-scenario reaction power, thermal pressure/energy and density/temperature moments. Source fusion power, beta or mean density must not set or fit a free input.
- **R2 [INHERITED]:** Preserve amplitude, edge ratio, density/temperature shape, species fractions, volume, radial-volume exponent and field as supplied choices. Explicitly distinguish the scenario's measure-weighted averages from actual ARIES volume averages.
- **R3 [INHERITED]:** Reuse the accepted density implementation and existing Bosch–Hale reaction kernel without changing their equations. Reuse `Volume-Averaged Beta` unchanged as an actual downstream native consumer of calculated thermal pressure. Count kernel reuse separately from reuse of a complete SysML definition.
- **R4 [INFERRED]:** Refuse invalid/nonfinite inputs and unsupported temperature before evaluation. Enforce mathematical parameter domains and report unsupported states separately from physical adequacy. No temperature clamp or silent profile normalization.
- **R5 [INHERITED]:** Verify native generation/execution, source interpretation, independent analytical moments/identities, quadrature convergence, kernel equivalence, scaling, field dependence and choice preservation. Complete all applicable validation levels, with any diagnosed static-check exception supported by actual execution.

## Source basis and chosen case

[INHERITED: primary sources] Use the authorized Lyon original `knowledge/holdout/aries-cs/08-FST-Lyon.pdf`: Eq. (3) p701 for density shape, Eq. (8) p713 for the temperature sensitivity family, p701 for equal ion/electron temperature, p703 for the average helium fraction and Table IV p708 for 11.83 keV/5.70 T; Table VII p716 for 444 m^3. The density and temperature source values were read directly from retained primary renders; the new Eq. (8) render is `work/orchestration/aries-transfer-experiment/evidence/review-lyon-p713.png`. Source-average helium does not prove a constant local fraction. Existing reaction-kernel authority is `1costingfe/layers/reactivity.py:54`, declaring 0.2–100 keV, and the normative generated `_sigv_dt` body; no new primary kernel qualification is claimed.

| Supplied case quantity | Value and role |
|---|---|
| Density amplitude | [AGENT] 5e20 m^-3, selected scenario coefficient; not inferred from central, peak or average source density |
| Density edge ratio and shape | [INHERITED] 0.1, p=12, q=1, h=0.66 from Eq. (3); conflicting edge/axis prose remains unresolved |
| Central ion/electron temperature | [INHERITED] 11.83 keV from Table IV with equal Ti/Te source assumption |
| Edge temperature | [AGENT] 0.2 keV selected to stay within the inherited reactivity domain; differs from the published near-edge value |
| Temperature shape | [AGENT] x=2,y=1 selected from Eq. (8)'s source sensitivity family; not the reference VMEC curve |
| Local nHe/ne | [AGENT] constant 0.0335, conditioned use of the source's 3.35% average; no ash-confinement solve |
| Fuel D fraction | [AGENT] 0.5 of D+T, explicit equal mixture |
| Impurities | [AGENT] none in this selected scenario; no iron radiation or source-composition match claim |
| Plasma volume and field | [INHERITED] 444 m^3 and 5.70 T supplied source geometry/field; not independently predicted |
| Enclosed-volume measure | [AGENT] V(rho)/V=rho^m with m=2, a homothetic-shell approximation; m remains a supplied lever |

## Equations, ownership and interface

[AGENT] One new `Supplied Profile Plasma` calculation in `models/library/analyses/supplied_profile_plasma.sysml` owns the integration. A new occurrence in `models/designs/aries_cs_transfer/plasma_integration.sysml` owns the chosen profile/species/volume/field inputs, EXPOSEs its outputs and binds pressure into the unchanged beta calc from `mfe_plasma_scaling.sysml`. Existing density definition may be instantiated at a supplied sample radius so its typed wrapper is available for direct unchanged-body reuse inside the integration; this sample is also a useful independent native interface witness. Imported libraries are staged unchanged in the isolated package.

[AGENT] Use `w(rho)=m*rho^(m-1)` on `[0,1]`, whose integral is one. Restrict the supported measure to `1<=m<=4` to exclude singular endpoints; it represents a chosen family, not an inferred 3D Jacobian. Electron density is the unchanged WI-081 relation. Temperature is Eq. (8). At each point, `nHe=fHe*ne`, `nFuel=(1-2*fHe)*ne`, `nD=fD*nFuel`, `nT=(1-fD)*nFuel`. This enforces quasineutrality for the selected electron/D/T/He mixture. Its pressure is `p=(2-fHe)*ne*T*keV_to_J`; no fast-particle pressure is included.

[AGENT] Integrate `mean_ne=integral(w*ne)`, `mean_neT=integral(w*ne*T)`, `density_weighted_T=mean_neT/mean_ne`, `mean_pressure=(2-fHe)*mean_neT*keV_to_J`, `reaction_rate=V*integral(w*nD*nT*sigvDT(T))`, `fusion_power_MW=reaction_rate*E_DT_J*1e-6`, `stored_thermal_MJ=1.5*mean_pressure*V*1e-6`. DT energy uses the existing 17.58-MeV convention and SI conversion explicitly, not a fitted value. New output `field_for_beta` preserves the supplied field exactly after validation; existing beta binds that and mean pressure. This lets the integrated domain reject nonpositive fields before the downstream calculation without inventing a second beta implementation.

[AGENT] Typed manual completion uses composite Simpson quadrature with refinement from 1024 through at most 65536 intervals. Require two consecutive refinements to change each integrated nonzero moment by at most relative 1e-6; exact zero reaction moments remain valid. Refuse if this criterion is not reached. Expose the final interval count and largest relative change as numerical evidence, not a rigorous error bound. This guards unresolved endpoint behavior without claiming uniform accuracy for all positive shape exponents. Density and reaction kernel bodies are copied from the exact accepted existing files, with only package imports adapted where necessary; their identities and any extracted function AST hashes are retained. Actual source files are not edited. Guard positive volume/field/amplitude, supported density inputs, temperature endpoints in `[0.2,100]` keV with center>=edge, positive temperature exponents, `0<=fHe<=0.5`, `0<=fD<=1`, and `1<=m<=4`. Validate every sampled temperature and finite intermediate/output. Zero fuel at fHe=0.5 or fD endpoints is supported and yields zero reaction power without zeroing electron/helium pressure.

## Verification and limits

[AGENT] Independent polynomial antiderivatives for the reference density and x=2,y=1 temperature give exact density and pressure moments under m=2. Flat-temperature and constant-density limits give analytical reaction checks. Compare kernel outputs at representative domain values to the original current implementation exactly; this proves unchanged arithmetic, not primary nuclear-data validity. Compare 2048/4096/8192 interval integrations and report actual convergence, retaining numerical tolerance separately from scientific uncertainty.

[AGENT] Through native public inputs verify: amplitude scaling makes density/pressure/energy/beta linear and fusion quadratic; changing volume scales power/energy while moments stay fixed; changing field scales beta inversely with field squared without changing pressure; D fraction symmetry and zero-fuel boundaries; altered helium and measure inputs; low/high temperature, nonfinite and other invalid inputs refuse. Confirm every chosen input remains unchanged. Four-view path: forward-evaluation requirement → density/thermal/reaction behavior → plasma-owned properties and beta consumer → calculation bindings and native checks.

[AGENT] Actual ARIES power and beta correspondence remain unverified because source normalization, VMEC temperature, physical Jacobian and local species closure are not reconstructed. The selected meaningful scenario uses several source quantities but retains stated assumptions; no ratio to published power is an accuracy pass.

## Checklist

- [x] Inspect primary density/temperature/species definitions, current kernel and downstream beta.
- [x] Record supplied choices, source limits, equations, interfaces and focused checks.
- [x] Receive independent source/design acceptance and resolve required changes.
- [ ] Implement isolated new calc/case and unchanged reuse bodies through normal generation.
- [ ] Run native forward, scaling, domain, convergence and complete scoped validation checks.
- [ ] Record final evidence, independent review and coordinator tracking handoff.
