# Thermal sensitivity and equipment study preparation

[AGENT] Prepared 2026-09-22 under T-001. This is a proposed executable study design, not a study record or numerical result. No oracle scan, evaluator call, study point, package change or commit was performed. The coordinator owns execution release after the equipment design, generated interface and verification are accepted.

## Authority and baseline

[OWNER-VERBATIM: supplemental user message, captured in goal.md] “Before ranking equipment or economic alternatives, test sensitivity to the principal thermal assumptions and connect each varied equipment capability to its selected inventory, purchase cost and applicable operating demand. Preserve the source-case failures and label the 423.1 MW case as the assumed integrated baseline.” The same brief authorizes sensitivity-only treatment of unresisted assumptions with a missing-response finding before execution.

[INHERITED] Preserve four complete canonical maps: `nominal-calculated`, `nominal-source-assumed`, `literal-Lyon-source-input`, and `literal-Raffray-accounting`, with exact existing values and source distinctions from the archived WI-089 design's A7/A8 and current author configuration files. Here the labels identify those configurations, not presumed filenames. The calculated case's historical 423.106794 MW net is the assumed integrated baseline. Reproduce its thermal/electrical channels after changes; do not retune it. Source-case failures remain evidence. New equipment assumptions extend each full map explicitly; no source case inherits another case's fusion/deposition mode by omission.

[INHERITED] Thermal assumptions remain in `work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md`, S1–S3/A1–A9. New inventory/pump assumptions belong in the author's successor design register. This proposal references those registers rather than creating competing authority. Candidate windows below are engineered diagnostic windows, not scientific qualification ranges.

## One record, ordered arms

[AGENT] Reserve `exploration/aries_integrated/studies/20260922-aries-integrated-equipment-costs/` for the round's one study, on one accepted sealed package. Use the existing direct-API `StudyRunner`/`PreparedListStrategy` route because points are coordinated full maps. The route has no runtime physical adapter. Keep all points and refusals.

1. Reproduce all four canonical configurations. The manifest pins calculated nominal; separate case evidence preserves every full constraint identity for the other three.
2. Execute the principal thermal arm below with all purchased inventories, geometries and ratings fixed. Analyze heat removal, branch temperatures, electrical output, operating demands and margins before interpreting any equipment/cost alternatives. Do not rank endpoints as designs.
3. Execute fixed-hardware density perturbations and a small selected-equipment arm. Thermal findings inform interpretation; they do not silently change point maps or hardware.
4. Report account completeness/reconciliation at those points. A comprehensive price uncertainty study and assumption-ranked cost range may require the next round. Do not stack another study in this round or call this preparation the full goal answer.

[AGENT] Initial bounded proposal: four canonical points, two endpoints per 21 principal axes (42), four thermal interaction points, two density points, and four purchased-capability points: at most 56 distinct stored points before deduplication. The interaction points cross recuperator effectiveness0.60/0.95 with PbLi hot bound961.15/1061.15K, holding all inventory fixed; this tests the competition between recuperation and primary driving temperature. Oracle-only candidate scans precede final window selection under runbook step 7 and are retained separately. If an edge refuses the supported numerical domain, retain the refusal and choose/document a valid sensitivity window without concealing an engineering failure. No full Cartesian product is proposed.

## Principal thermal axes

[AGENT] Priority here means expected consequence from the equations, not measured importance. The executor must replace this expectation with observed sensitivities. All axes are `sensitivity`. Only one row/branch changes at a time. Nominal comes from the canonical calculated map; the two endpoints accompany that shared baseline.

| Priority | Axis family and role | Candidate endpoints | Reason and missing response |
|---|---|---|---|
| 1 | Recuperator effectiveness, assumed performance at fixed source-budget hardware | 0.60, 0.95; nominal 0.80 | A3; changes heater inlet and competition among primary branches. No purchased area/pressure-loss relation; cost stays fixed and no purchased-effectiveness ranking is supported. |
| 1 | He/PbLi/divertor bulk hot limits, three independent assumed bounds | Each nominal ±50 K: 679.15/779.15, 961.15/1061.15, 923.15/1023.15 K | Engineering diagnostic around A4; controls available driving temperature. These are not qualified material limits or authorized higher-temperature hardware. |
| 1 | Cycle mass flow, operating choice | 1000, 1800 kg/s; nominal 1400 | A3; changes compressor work and exchanger capacity rates. Installed machine ratings stay fixed; machine-map support remains absent. |
| 1 | Primary mass flows, three operating choices | He1630.5/4891.5, PbLi13430/40290, divertor250/750 kg/s | A4 half/1.5 times nominal. Each must drive both heat transfer and the declared pump proxy; purchased rated flow stays fixed. Proxy support is not hydraulic qualification. |
| 1 | Primary heat-transfer coefficients U, three assumed constants at fixed area | 500, 1500 W/(m² K), nominal1000 | Author's proposed UA=U×area/1e6 with area50000m² recovers UA50MW/K. This spans UA25–75 at fixed hardware. Geometry, pressure drop and real-fluid response are unverified. |
| 2 | Neutron multiplier, assumed deposition constant | 1.00, 1.25; nominal1.16 | A1; changes source heat independently of hardware. Breeding and transport do not resist it. |
| 2 | Helium deposition fraction, assumed partition | 0.25, 0.50; nominal0.38 | Engineered interior subset of A1's 0–1; reallocates heat between differing branch capabilities. No transport qualification. |
| 2 | Radiation fraction, assumed partition | 0.10, 0.40; nominal0.25 | Engineered interior subset of A1; reallocates blanket/divertor demand. No radiation/confinement qualification. |
| 2 | Inter-coolant exchange fraction, assumed partition | 0.00, 0.06; nominal0.04 | A1; retain nonnegative-duty validity mask derived from held deposition inputs. |
| 2 | PbLi specific heat, assumed constant | 170, 220 J/(kg K); nominal190 | A4; tests primary capacity rate without purchasing inventory. Real-fluid variation is missing. |
| 2 | Common cold sink, tied operating boundary | 298.15, 318.15 K; nominal308.15 | Engineered ±10K; tie cycle cold temperature and both intercooler targets. Sink/weather/rejection equipment response beyond modeled duty is missing. |
| 2 | Cycle pressure-loss fraction, assumed operating loss | 0.02, 0.08; nominal0.045 | Engineered around S3; affects expansion. No loss-from-geometry model. |
| 2 | Turbine efficiency, assumed constant | 0.88, 0.96; nominal0.93 | Engineered diagnostic around S3; machine-map and purchase-quality response absent. |
| 2 | Common compressor efficiency, tied assumed performance | 0.84, 0.94; nominal0.89 | Engineered ±0.05; all three stages change under an explicitly declared common-assumption tie. No purchase-quality relation. |
| 2 | He pump efficiency, assumed operating performance at fixed installed rating | 0.60, 1.00; nominal0.80 | Dominant inherited pump term. With flow held nominal this isolates assumed hydraulic demand; hydraulic/MHD qualification and purchased-quality response are absent. |

[AGENT] This table contains 21 axes: six single axes in priority1 plus the three-flow and three-U families total11; priority2 adds10. Secondary sensitivities (PbLi/divertor pump calibration, recovery fractions, cryo/control/fuel coefficients, cp/gamma for helium and auxiliary heating efficiency) stay held and are explicitly untested this round. Their limits remain A2/A5. Source-case variations are separate canonical reproductions, not thermal endpoints with renamed source authority.

## Full attribute-to-entry groups

[INHERITED: current `interface_data.py` and `plant.sysml`] Each current public source attribute has one generated entry field; its downstream fan-out is inside the native graph. Define `K(owner, attribute) = aries_integrated_plant__<owner>__<attribute>` by literal concatenation. This notation expands to full keys without suffix matching. All listed keys belong to `plant_params`, except density amplitude in `plasma_integration_params`. Each singleton has provenance `fan_out`.

| Axis | Complete current key group |
|---|---|
| Recuperator | `{K(cycle, recuperator_effectiveness)}` |
| Each primary hot bound, branch b=he/pbli/divertor | `{K(heat_exchangers, b_limit)}` |
| Cycle flow | `{K(cycle, selected_flow)}` |
| Each primary flow, branch b | `{K(heat_exchangers, b_flow)}`; post-change the same operating owner must fan out to pump and HX |
| Multiplier / helium partition / radiation / exchange | Separate singletons `{K(deposition, neutron_multiplier)}`, `{K(deposition, helium_fraction)}`, `{K(deposition, radiation_fraction)}`, `{K(deposition, exchange_fraction)}` |
| PbLi cp | `{K(heat_exchangers, pbli_cp)}` |
| Common cold sink | `{K(cycle, low_temperature), K(intercooler_1, target_temperature), K(intercooler_2, target_temperature)}` |
| Pressure loss | `{K(pressure_loss, loss_fraction)}` |
| Turbine efficiency | `{K(cycle, turbine_efficiency)}` |
| Common compressor efficiency | `{K(compressor_1, efficiency), K(compressor_2, efficiency), K(compressor_3, efficiency)}` |
| Fixed-hardware density demand | `{aries_cs_plasma_integration__plasma__amplitude}` |
| Each assumed U, branch b=he/pbli/divertor | `{K(b_hx, assumed_u)}`; author's planned public keys, require emitted-interface confirmation |
| He pump efficiency | `{K(he_pump, efficiency)}`; author's planned public key |
| Selected He HX area | `{K(he_hx, selected_area)}`; author's planned public key |
| Selected He pump flow capacity | `{K(he_pump, selected_flow_capacity)}`; author's planned public key |

[AGENT] The common sink and compressor groups are declared ties by this study preparer, not a tool-inferred physical identity. Choose the first listed key as `fan_out`, remaining keys as `tie`, and record their common operating/assumption authority. Do not tie different primary coolants or independently chosen compressor ratios just because their defaults match.

[AGENT] The author supplied the planned new public paths above on2026-09-22; they cannot be declared against the old package because they do not yet exist. Confirm their actual generated entry spelling after accepted design/build. Replace old `K(heat_exchangers,b_ua)` with the selected-area/assumed-U inputs; UA becomes a derived output and retires as an axis. Old `K(deposition,b_pump)` likewise becomes a calculated EXPOSE binding from the pump owner. Do not keep simultaneous independent UA and area×U choices or operating pump demand and its proxy inputs. Extend every complete canonical map, `axes.json` and `interface_data.py` from the emitted interface. Each new source attribute should fan out internally to inventory/cost/operation; if the package instead emits separate entries for the same selected physical quantity, the group must enumerate every such field with an explicit tie. A partial group is not executable. This is a named preparation dependency, not permission to guess keys.

## Demand and selected-equipment evidence

[AGENT] Demand test: density amplitude 4.5e20 and5.5e20 around inherited5e20 m⁻³, calculated mode1, all thermal assumptions/hardware held. These are engineered ±10% perturbations, not a confinement qualification. Verify source heat, fuel throughput, net electricity and applicable capacity margins change; assert every selected quantity, area, installed rating, initial inventory and upfront purchase account is unchanged. Only declared consumption/replacement channels may change annual cost. Finite-life replacement spending may change only where a reviewed demand-to-life relation exists; otherwise schedules stay fixed.

[AGENT] Purchased equipment arm: two He exchanger areas5000/75000m² at fixed U1000, hence UA5/75MW/K, against nominal area50000; and two selected He pump rated flows at0.5/1.5 times its accepted nominal rating with operating flow3261kg/s fixed. These are explicit hypothetical selected offers, not vendor quotes. Hold every unrelated selected variable fixed. Area must change purchased area/capital and exchanger capability; rated flow must change installed inventory/cost and operating margin. Insufficient/sufficient outcomes must be established by the oracle scan, not assumed from these candidates. If a proposed pair does not bracket adequacy, document that fact and extend within the accepted design domain before fixing the window. Cost monotonicity alone cannot establish meaningful engineering response.

[AGENT] Primary flow has an author-proposed pump law `P_ref*(flow/flow_ref)^3*(eta_ref/eta)` preserving nominal156/.01/10MW. Treat it as a transparent hydraulic proxy, especially for PbLi where MHD response is unresolved. Record flow, reference flow, efficiency and reference efficiency separately from purchased rated flow. Pump power feeds electricity and recovered friction exactly once. Hardware purchase follows installed rating, never operating power. Recuperator remains fixed-budget inventory with effectiveness uncertainty; do not present that arm as purchased equipment comparison.

## Required route and verification updates before execution

- [AGENT] Regenerate reviewed `interface_data.py` entry/channel maps and full constraint catalog from accepted emitted artifacts; replace semantic/executable pins, manifest/indicator fingerprints and full canonical proposal maps. Preserve old study snapshot unchanged. Route validation requires exact full key-set equality, so omissions or retired UA/pump keys must fail before execution.
- [AGENT] Require native publication of selected areas/U/derived UA, pump operating/rated flows, operating powers/recovered heat, inventory quantities, each disjoint capital account, classified totals, annual/scheduled costs, currency/year codes, scope/support flags and account reconciliation residuals. Include all thermal channels and every new predicate identity in JSON/store and reporting metadata. Do not insert reporting arithmetic as model outputs.
- [AGENT] Extend independent `oracle_entry.py` to derive new geometry/UA, pump demand, inventories, purchase costs, annual costs and account sums from inputs. It must independently reconstruct every new predicate's operands. Current `operand_bindings()` falls through every unknown local name to balance operands; replace this with explicit supported-name mappings and rejection of unknown predicates before admitting new cost/equipment checks.
- [AGENT] Preserve independent adaptive plasma quadrature and Brent thermal closure. Add comparisons for branch transferred/unmet heat, pump/friction terms, area/UA, capital invariance under demand, and installed-rating margins. Sampling must cover every verdict combination and each new cost/coupling family, not just headline net output. Identical supplied values copied on both sides are input checks, not independent physics validation.
- [AGENT] Retain the documented absolute1e-7MW tolerance only for residual magnitude unless a reviewed new channel requires another dimensional tolerance. Do not relax tolerances to hide cost mismatch. Declare monetary tolerances in currency units and preserve exact verdict comparisons. Baseline local-name collision remains a known limitation; full capacity identities must survive stored execution and oracle verification.
- [AGENT] Run indicators on every proposed axis, including deferred/declined ones if formally proposed to that record. Record `no_constraint_response` separately from reachable paths and reuse the owner's sensitivity-only authorization with a named missing-response finding. Regenerate indicator coverage after the interface changes; old reachability is not new-package evidence.
- [AGENT] Before points: accepted design/source math coverage, strict native package identity, pinned baseline replay, package cleanliness, read coverage and all runbook preflight gates. Use the documented `.codex-test/run` environment plus the annex's TEAx import path. After points: stratified oracle verification, immutable record/snapshot with actual digests, adverse evidence, findings and limitations. No equipment/economic ranking precedes the thermal arm's interpreted evidence.
