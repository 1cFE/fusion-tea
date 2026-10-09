---
Status: complete
Created: 2026-09-27
Updated: '2026-10-06'
Related Artifacts: spec.md; evidence/development-probe.py; evidence/development-followup.py
---

# WI-097: controlled exchanger comparison

## Decision

[AGENT, under delegated owner authority] Build one isolated native package with two closure modes: unchanged legacy operation and explicit primary bypass control. The controlled mode fixes the three aggregate loop returns, uses the entire installed exchanger UA, and checks both actual terminals against 30 K. It keeps the existing source, primary flows, hot caps, cycle components and equipment ratings. Compare the original exchanger inventory first, then two explicitly offered and priced smaller inventories shared by both architectures.

This design implements [the spec](spec.md). Authority and thermal provenance are in the goal's [owner supplement](../../orchestration/goals/design-study-exchanger-architecture/evidence/owner-supplement-r3.md) and [source contract](../../orchestration/goals/design-study-exchanger-architecture/evidence/r2-thermal-requirements.md). The owner delegated judgment; the exact return targets and six-terminal 30 K requirement remain agent-originated conditional engineering requirements. They are not a reconstruction of the published ARIES operating point. No production implementation or main study was performed for this design.

## Development evidence and offered equipment

The retained probes solve the full-duty cycle algebra, then solve bypass separately in each actual exchanger. A passing probe has self-consistent full-duty thermal states. A failed probe retains attempted full-duty temperatures; these are not the partial-duty operating states that the native implementation must calculate. The probes check no complete native equipment, energy or cost ledger and are not study evidence.

- [First probe](evidence/development-probe.py) and [all 2,880 results](evidence/development-probe.json): original UA and three declared smaller offers, five loads, 50 kg/s flow spacing and 0.05 split spacing. There are 73 thermal passes, all network. Every failure is retained.
- [Follow-up probe](evidence/development-followup.py) and [all 6,720 results](evidence/development-followup.json): two further declared offers, the same five loads, 10 kg/s flow spacing and 0.05 split spacing. There are 697 thermal passes, including matched passing series/network cases. These results justify implementing the control model; they do not establish continuous optima or a native architecture preference.

The first catalog missed series because its divertor UA was too large. The follow-up choice follows the explicit admissible-UA interval derived below. At source 1835.4512830147435 MW and series flow 1300 kg/s, the intervals are He [8.24699, 18.45035], PbLi [16.71687, 18.99466], and divertor [1.25773, 2.72013] MW/K. A shared offer (18, 18, 2) therefore provides a direct matching test without hiding area selection inside the model.

| Offered inventory, in He / PbLi / divertor order | Supplied areas, m² | UA at unchanged U = 1000 W/(m² K), MW/K | Offered purchase per HX, USD2004 |
|---|---|---|---|
| Original | 50,000 / 50,000 / 50,000 | 50 / 50 / 50 | 58,325,700 each |
| A: matched small | 12,000 / 12,000 / 2,000 | 12 / 12 / 2 | 58,325,700 each |
| B: matched medium | 18,000 / 18,000 / 2,000 | 18 / 18 / 2 | 58,325,700 each |

[AGENT] Freeze this limited catalog before main execution. The smaller inventories are alternative procured designs, not a retrofit that recovers the original sunk cost. No exchanger rating or other purchased component is resized by operating demand. Additional offers require a recorded study amendment rather than an implicit optimizer purchase.

At the N load, offer A's lowest passing tested flows are 1360 kg/s series and 1310 kg/s network. Offer B gives 1300 and 1260 kg/s respectively. Both have passing pairs at 1950 and 2000 MW. At 1650 MW, A has a passing pair while B has only network passes on the tested grid. Neither has a pass at 2200 MW because the required divertor hot state exceeds the unchanged cap. These are thermal probe observations only.

### Why unchanged UA fails

For a counterflow exchanger with constant heat capacities, full installed UA gives Q = UA × LMTD. If both actual terminal differences are at least a positive requirement D, their logarithmic mean is also at least D. Therefore Q ≥ UA D for any active full-UA exchanger, including a bypassed primary stream. The original divertor UA = 50 MW/K and D = 30 K require Q ≥ 1500 MW. Its fixed primary flow, target return and hot cap permit at most 329.7555 MW. These conditions cannot both hold. Reducing primary exchanger flow through bypass does not change this proof because installed UA remains active.

For a proposed full-duty state, let a = H − T_secondary,out and b = R_target − T_secondary,in. A primary hot bypass can only lower the active exchanger return below the mixed return, so a ≥ D and b ≥ D are necessary. If they hold, admissible UA lies between Q/LMTD(a,b), the no-bypass case, and Q/LMTD(a,D), the limiting cold-terminal case. This interval informed the external offer catalog. The native calculation receives the chosen area; it never receives a solved required area as purchased hardware.

## Physical and analytical structure

Each primary loop retains its total supplied flow. A fraction passes through its exchanger and the remaining hot fraction bypasses that exchanger. The streams mix before the aggregate cold-return boundary. Source deposition and the inherited recovered pump heat occur after that boundary and before the next hot inlet. Existing recovered heat enters delivered duty exactly once.

Series retains He → divertor → PbLi on the secondary side. Network retains He followed by a supplied PbLi/divertor split and ideal secondary mixing. No primary stream mixes with the secondary working fluid. The recuperator remains part of the existing cycle closure and is excluded from the new 30 K requirement.

The main controlled scenario fixes aggregate returns He 659.15 K, PbLi 724.15 K and divertor 846.15 K. Existing supplied hot caps remain 729.15 K, 1011.15 K and 973.15 K. The six approach inputs default to 30 K. Label 15 K and 45 K variants as requirement sensitivities, with both terminals changed consistently; never select the threshold from a passing result.

### Controlled branch equations

For each branch, Q is the full delivered source duty in MW, C_h = total primary flow × cp / 10⁶ in MW/K, and C_s is the actual secondary branch heat-capacity rate. UA comes from the offered area and unchanged supplied U.

[AGENT assumption] U remains constant as bypass changes the active primary flow. No U(flow), film-coefficient or hydraulic correlation is represented. This is a conditional constant-property exchanger model; conductance uncertainty at fixed purchased area belongs in labelled sensitivity cases. Bypass changes heat-capacity rate and effectiveness, never installed UA by an implicit discount.

```text
H_required = R_target + Q/C_h
H = H_required                       # attempted supplied-source operating state
C_active = (1 - f) C_h
q_cap(f) = epsilon(UA, C_active, C_s) min(C_active, C_s) max(H - T_s,in, 0)
```

Use the existing counterflow effectiveness-NTU relation with its equal-capacity limit. At each cycle evaluation, if q_cap(0) ≥ Q > 0, solve q_cap(f) = Q over 0 ≤ f < 1, then set q = Q. If q_cap(0) < Q, use f = 0 and q = q_cap(0). This is a capacity failure, with positive unmet duty; the source hot state is not silently raised to repair it. For an active transferring state:

```text
T_hx,return = H - q / [(1 - f) C_h]
R_mixed = f H + (1 - f) T_hx,return = H - q/C_h
T_s,out = T_s,in + q/C_s
hot_terminal = H - T_s,out
cold_terminal = T_hx,return - T_s,in
return_residual = R_mixed - R_target
hot_cap_margin = supplied_hot_cap - H
unmet = Q - q
```

The target is compared with the calculated mixed return; assigning the target to the return output would hide failure. The cold-terminal check uses the active exchanger outlet before mixing. The hot-terminal check uses that branch's secondary outlet before any network mixing. The full source duty determines H even when accepted heat is smaller. An over-cap H is reported and rejected, without clipping the value to manufacture a pass.

The control's mathematical domain permits f approaching one for positive duty, but never a zero active flow in a transferring state. Expose a supplied `max_bypass` input per branch, default 1.0, as an explicitly assumed unrestricted mathematical controller. Solve the required control fraction and check it against this input. A solution above a supplied limit is an inadmissible control request and fails its predicate; it is not reported as available actuator capability. Do not introduce an unpriced engineering claim that a real valve can realize every fraction. Study reporting must show required fractions and their allowance sensitivity.

For zero Q, set f = 0, q = 0 and explicit `state_defined = 0` for terminal evaluation; return and hot diagnostic identities may still be reported. For zero UA or no positive hot-to-secondary drive with positive Q, set q = 0, f = 0, report unmet Q and an invalid terminal state. Inactive/sentinel terminal values cannot satisfy active-HX requirements. These inactive fixtures are failures under this three-active-exchanger study, while remaining finite diagnostic executions.

### Coupled cycle closure and failure meanings

The controlled stage calculation belongs inside the cycle root. At each trial turbine temperature, derive the recuperated heater inlet using the existing expansion factor k and effectiveness e; evaluate the stages in the selected topology; and solve:

```text
T_heater = T_compressor,3 + e max(k T_turbine - T_compressor,3, 0)
cycle_residual = C_cycle (T_turbine - T_heater) - sum(q_branch)
```

Bracket the controlled root between the compressor outlet and the maximum of that outlet and the required primary hot states. Verify endpoint signs and convergence. Branch capability is continuous as duty becomes fully accepted; use a bracketed scalar solve. Positive inputs, finite outputs, positive heat capacities, permitted topology and 0 < split < 1 remain domain requirements. Numerical failures raise explicit errors; engineering inadequacy returns failed verdicts and diagnostic states.

Pass the root's actual accepted heat and turbine temperature into the existing turbine, shaft, generator, rejection and plant-ledger consumers. A capacity failure must reduce transferred heat and change cycle/electric outputs through those same consumers. The current unmet-heat accounting remains active. A failed return or hot-cap condition means the displayed candidate state does not establish a steady admissible source loop, even if its accepted-heat cycle ledger balances. The design does not claim a transient storage or alternate source controller for such a failure.

## Legacy mode and public interface

Use `control_mode = 0` for the unchanged legacy closure and `control_mode = 1` for the reviewed controlled equations. Preserve original legacy outputs and all 14 old verdicts exactly in mode 0. Preserve the historical package and record. New thermal verdicts may reject legacy points under the new requirements; matching old behavior is not a new thermal pass.

Keep the reviewed legacy body as a preserved implementation dependency. A new native wrapper selects it in mode 0 and calculates only added diagnostics around its outputs. Do not run an unselected controlled branch and permit its domain errors to break legacy execution. Map old `branch_return` to the original return in legacy mode and to the aggregate mixed return in controlled mode; publish `branch_hx_return` and `branch_mixed_return` explicitly in both modes. In legacy mode these are identical because f = 0.

| Quantity | Owner, role and consumers |
|---|---|
| Source power, partition and pump recovery | Existing source/coolant owners; delivered duties feed the selected closure unchanged. |
| Primary flows/cp, hot caps, cycle flow, topology, split | Supplied design or operating inputs; flow/split search remains external to model execution. |
| Selected HX areas and U | Existing equipment owners; area/U determine UA. No control-state binding changes either. |
| Offer price factors | Supplied procurement adapter inputs selected from the declared area/total-price catalog, never from runtime duty. |
| Return targets, six terminal minima, per-branch maximum bypass | New supplied conditional requirements under the exchanger owner. |
| Required hot, actual hot, active/mixed returns, active flow, bypass fraction, capability at zero bypass/solution | Native closure outputs; state diagnostics, checks and oracle verification. |
| Return residual magnitude, hot-cap margin, two terminal margins, control margin and state validity | Native check operands with explicit constraint bindings. |
| Accepted heat, unmet heat, turbine/heater temperatures and cycle residual | Existing cycle/electric/energy consumers; controlled mode changes these when transfer fails. |

Use a numerical return residual tolerance of 10⁻⁶ K and retain the established cycle heat-residual contract of 10⁻⁶ MW, subject to independent implementation verification. These are numerical solve checks, not physical relaxation of exact returns. Thermal approach and hot-cap checks compare actual margins to zero; the oracle separately verifies numerical agreement at a declared scale. Full duty, valid states, all new predicates, old equipment/energy predicates and positive net electricity are required for a candidate recommendation.

## Purchase and economic boundary

The smaller offers are below the inherited quantity estimate's 0.5–1.5 reference-area range. Keep its `cost_extrapolated` diagnostic true. Do not rename the reference area or erase that flag. For the main comparison, use the explicit retained-budget purchase assumption in the offer table, not the unsupported geometric estimate as a claim about vendor prices.

Keep global estimate mode 0. Existing native purchase arithmetic is `C_reference × price_factor × area/50000`. Encode each declared total offer price through the supplied adapter `price_factor = offered_price / (C_reference × area/50000)`. Thus factors are 1/1/1 for original, 50/12, 50/12, 25 for A, and 50/18, 50/18, 25 for B. All three inventories book 174,977,100 USD2004 in these HX accounts. The explicit prices are agent assumptions; retaining the original budget is conservative only relative to the inherited smaller-area linear extrapolation, not a real procurement guarantee. No second purchase account is added.

The inherited linear smaller-area prices are a labelled sensitivity: A totals 30,329,364 USD2004 and B totals 44,327,532 USD2004. Preserve the extrapolation qualification in that sensitivity. The existing downstream aggregation applies these purchases to direct/overnight cost, financing and lifecycle terms exactly once. The model has no dedicated HX replacement or HX-specific O&M law.

Bypass valves, bypass piping, actuation, balancing and arrangement-specific pressure losses remain unpriced conditional allowances. Existing pump powers and cycle pressure loss are held assumptions, not predictions of this new piping. The main native economic output includes the explicit HX inventory and existing plant costs; it excludes those added control/topology costs. Both arrangements use the same three-controller concept, but equality of real controller costs is not established. Report the maximum equivalent annual cost and extra electric demand that could erase a passing network advantage, including control/topology differences. Also show common controller-cost sensitivity when it changes LCOE ranking. A source load with only one passing architecture has no paired break-even result against its failed counterpart.

## Isolated implementation files

[AGENT] Use `exploration/exchanger_architecture/thermal_requirements/` and generated Python package `exchanger_architecture_thermal_tea`. Retain historical models, packages and studies untouched.

| New relative path under that root | Implementation responsibility |
|---|---|
| `models/controlled_exchanger_closure.sysml` | New selected closure interface, explicit diagnostics and thermal/control constraints; source/provenance docs and units. |
| `models/plant.sysml` | Clone saved ARIES assembly; bind selected closure and new constraints; retain equipment/cost consumers and supplied offer paths. |
| `bodies/controlled_exchanger_closure/controlled_network_heat_driven_closure_impl.py` | Native controlled stage/cycle solution and legacy dispatch. Retain legacy dependency without altering its arithmetic. |
| `build.py`, staged `input_models/`, generated package | Adapt the isolated costed-loop build pattern: exact source staging, reviewed body copying/import adaptation, generated interfaces/contracts, regeneration fixed point, snapshot/census and hash receipts. |
| `studies/oracle_entry.py` | Independent thermal/control math and full channel/predicate verification for both modes/topologies. |
| `studies/{prepare_interface.py,interface_data.py,manifest.json,study_route.py}` | New package/interface/fingerprints, full entry validation, actual predicate catalog and native evaluation route. |
| `tests/` and item `evidence/` | Unit/boundary/assembled controls, preservation comparisons, independent numerical and integration receipts. |

Reuse the existing [isolated build pattern](../../../exploration/costed_loop_brayton/build.py), [legacy body](../../../exploration/aries_integrated/native_completions/network_heat_driven_closure_impl.py) and [WI-095 controller](../../../exploration/costed_loop_brayton/bodies/loop_return_control/primary_bypass_control_impl.py) as inspected references. WI-095 provides the bypass mechanism; it does not supply this coupled three-branch implementation or network oracle. The old architecture executor points at the ARIES package and must not be reused with only a manifest path replacement. Generate schema, pipeline and contract changes from the new SysML sources.

## Independent equations and acceptance

The oracle must not call the production bypass, effectiveness helper or cycle root. Use independent branch energy balances and the counterflow LMTD relation to solve active primary capacity or outlet temperature. Use a separate bracketed cycle root and topology reconstruction. Handle equal terminal differences with the logarithmic-mean limit. Verify every actual and mixed temperature, duty, control fraction, validity flag, margin and new predicate, plus existing energy/equipment/cost channels. Rebuild operand bindings; the old oracle's 364 verified channels omit these thermal states.

At high NTU, a strictly positive actual terminal gap may be smaller than binary64 temperature subtraction can resolve. Its published difference can round to zero or a tiny negative value while heat transfer remains finite. Do not classify that state as zero transfer, refuse its verification, or reset `state_defined` merely from the rounded terminal difference. Establish the physical transfer domain from the positive hot-to-cold inlet drive, UA, active heat-capacity rates and duty; distinguish this from a genuinely nonpositive inlet drive or zero conductance.

Reconstruct such cases using an independent logarithmic-domain LMTD equation or sufficiently high precision, with precision/convergence receipts. Preserve the finite duty and resulting cycle/electric outputs. Compare reconstructed temperatures and rounded terminal outputs within declared absolute numerical tolerances, including cancellation error; reject their 30 K approach predicates using the actual reported margins. Do not widen a physical threshold or replace a finite-transfer failure with a non-transferring state. Stable verification must cover these engineering-failing original-inventory controls as well as passing offers. The bounded probe only asserts its direct binary64 LMTD identity where both terminal gaps meet 30 K; it is not evidence that direct LMTD subtraction is stable for all retained failures.

Mandatory acceptance evidence:

1. Replay saved Round 1 controls in legacy mode and compare every legacy numerical output and old verdict, including N, both former leaders, unmet-PbLi series, failed network split and original 2600 MW range extension. New verdicts remain separately visible.
2. Verify one analytic no-bypass equality fixture and one nonzero-bypass fixture. Check full-UA LMTD, both primary/secondary energy balances and mixed-return identity independently. Perturb each requirement across its boundary and show the corresponding verdict changes.
3. Exercise inadequate area, over-cap required hot, approach failure, supplied bypass-limit failure, zero UA/duty, no positive drive and split endpoints/domain refusal. Include original-UA 50 MW/K fixtures with positive duty and a true positive gap rounded to zero/tiny negative, verifying finite transfer and cycle outputs against high-precision independent reconstruction while approach checks fail. Add active-primary/secondary equal-capacity fixtures and points on both sides of that limit, checking both epsilon-NTU and LMTD limiting behavior through independent equations. Undefined states cannot pass. Inadequate conductance must change the solved cycle/net output and preserve the energy ledger through unmet duty.
4. Execute the unchanged inventory first in both modes/topologies, then representative A/B passing probe points and nearby failing points. Native all-equipment checks may narrow probe feasibility; retain that result. Demonstrate selected area/rating and procurement cost invariance to flow/split within each offered inventory.
5. Compare native purchase/lifecycle changes with independent arithmetic. Check that retained-budget offers keep HX cost equal across sizes, linear sensitivities carry the flagged extrapolation, and neither doubles the booked purchase.
6. Complete applicable installed model validation, regeneration fixed-point checks, audit and native integration seam with the new fingerprints and manifest. These are implementation gates after independent design review.

## Refined study handoff

Use common loads including 1650 MW, the exact supplied N load, 1950 MW and 2000 MW, with 2200/2300 MW retained as negative source-cap controls. Evaluate original inventory before alternatives. Main offer/topology pairs use identical source, area/price inventory, primary flows, cycle loss and non-HX equipment. Show both equal-flow paired results and independently selected best passing operation for each architecture. If both remove the same full duty at the same cycle flow, their ideal-cycle electrical output should agree; the proposed advantage is access to lower passing flow, not extra heat creation by mixing.

Follow the [Round 3 study contract](../../orchestration/goals/design-study-exchanger-architecture/evidence/r3-study-contract.md): declare a broad common flow/split scan, identify every sampled feasible component, then refine each relevant transition with explicit proposal maps and off-grid checks. Aim to bracket the leading flow boundary within 0.1 kg/s and relevant split choices within 0.001, then halve local spacing and require stability within 0.2 MW and 0.1 USD2004/MWh. A claimed advantage must exceed remaining refinement uncertainty. Check narrow feasible windows rather than assuming all thermal predicates are monotone. If the declared evaluation budget ends first, report the unresolved brackets and a tested-grid comparison. Store ties, rejected cases and neighboring failures; every final reported point must execute natively and pass independent numerical verification. The development probes remain separately labelled.

## Review boundary

This design authorizes no production edits by itself. Independent review must accept the coupled failure semantics, legacy preservation, actual-terminal checks, offer/price assumptions and independent-oracle strategy. With that review, implementation can proceed under the owner's delegated judgment. A real piping/control design, qualified procurement estimate and complete plant qualification remain beyond the supported claim; their unknown cost and electrical effects stay explicit conditional allowances.
