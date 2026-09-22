# T08: dual-coolant heat accounting under supplied boundaries

[INHERITED: coordinator assignment, 2026-09-21] Resolve the published heat/friction/exchange boundaries, then implement a defensible native transfer increment. [AGENT] Recommended scope is a two-branch blanket heat ledger with independently supplied heat inputs and offered exchanger duties. The existing DEMO primary-loop calculation cannot reproduce the source boundaries unchanged. A new two-branch energy-accounting component is justified; a qualified ARIES hydraulic model is not yet supported.

## Source boundary resolved

[AGENT] Directly inspected retained Raffray p734 Table II, p736 Figs12/13 and p737 Table III/discussion. Images are under `.project/active/aries-comparison-preparation/post-reveal-results/post-reveal-v1/source-evidence/retained/knowledge/holdout/aries-cs/extracted/20260920-r3/08-FST-Raffray/`, named `outputs-page-09.png`, `outputs-page-11.png` and `outputs-page-12.png`. This is the Raffray engineering thermal case. Fig14 labels fusion power 2365 MW, while the separate Lyon systems reference uses 2436 MW. Do not bind the WI-083 plasma output or the Lyon load into this engineering case and describe it as one reconstructed plant.

| Quantity | Printed/derived value MW | Interpretation |
|---|---:|---|
| Blanket fusion thermal power | 2496 | Printed Table II, independent total for a source-consistency residual |
| PbLi heat delivered from blanket | 1444 | Printed net of approximately 111 MW conducted to He |
| He heat removed | 1192 | Printed including 141 MW friction and 111 MW transferred from PbLi |
| PbLi-to-He exchange | 111 | Printed approximate internal transfer; subtract once from PbLi and add once to He |
| He friction heat | 141 | Printed addition to recovered thermal duty; not the electrical draw |
| He pumping power | 156 | Printed separately; do not add all 156 MW to the thermal duty |
| PbLi deposition before exchange | 1555 | Derived source boundary: 1444 + 111 |
| He deposition before exchange/friction | 940 | Derived source boundary: 1192 - 111 - 141 |
| Sum of derived depositions | 2495 | Leaves -1 MW against printed 2496; retain residual, do not renormalize |
| Combined delivered blanket heat | 2636 | 1444 + 1192; same as 2495 + 141 |

[AGENT] These source-derived input loads are an accounting reconstruction. Reproducing 1444 and 1192 from them is a boundary-consistency check, not an independent prediction of the duties. The 1 MW residual is compatible with rounding of integer/approximate source values but is not silently erased or used to tune a coefficient. Fig12 confirms separate blanket-He and PbLi exchangers, plus a separate divertor-He branch. T08 represents only the two blanket branches; their sum is not total heat into the Brayton cycle.

[AGENT] The source's p737 discussion explicitly adds He friction heat to fusion thermal power and subtracts pumping power in the net electrical efficiency. Its 0.89 compressor efficiency belongs to the three-stage power-cycle compressors in Table III/Fig13. It is not evidence for blanket-circulator efficiency. Likewise, Fig12's illustrative temperatures differ slightly from Table II; no cross-figure temperature reconciliation is assumed.

## Why the existing primary-loop implementation does not transfer unchanged

[AGENT] `models/library/analyses/mfe_primary_loop.sysml:4` computes flow from source heat excluding recovered pump work, then adds compression work to exchanger heat. Table II's 1192 MW already includes friction. Feeding 1192 as that source term double-counts the included work; feeding 1051 = 1192 - 141 removes it from the heat used with the printed 386/456 C coolant rise. The source's 3261 kg/s with that 70 K rise implies approximately 5222 J/(kg K) when paired with 1192 MW, not with 1051 MW. No new cp or efficiency should be fitted to make both interpretations agree.

[AGENT] The inherited pressure-loss law additionally scales a DEMO reference at fixed nominal density. It is not an ARIES pressure-drop relation, and PbLi requires distinct liquid-metal/MHD treatment. The existing helium/HITEC equipment model also has the wrong second coolant and exchanger technology. Executing either unchanged on invented transfer inputs would show algebra execution, not meaningful source qualification.

[AGENT] Reuse the genuinely generic `Offered Capacity Screen` and `Offered Equipment Capacity` from `models/library/analyses/mfe_viability.sysml:106,119`, once for each branch. Do not force the `Cooling Energy Addition` salt-input accounting or the Rankine cycle into this architecture merely to report reuse.

## Minimal build proposal

[AGENT] Add a generic `Coolant Branch Heat` calculation: `delivered_heat = deposited_heat + received_exchange - exported_exchange + recovered_friction_heat`. Inputs are finite nonnegative MW; reject a negative net thermal duty. A PbLi occurrence owns its deposition and outgoing duty; a helium occurrence owns its deposition, incoming transfer, friction heat and outgoing duty. One separately owned exchange attribute binds both the PbLi subtraction and helium addition so the internal transfer cannot diverge accidentally. No geometry, flow, cp, pump efficiency or pressure loss is manufactured.

[AGENT] Add a small two-branch ledger that consumes the actual branch duties and supplied depositions/friction and returns combined duty, deposition, recovered friction and an internal energy-conservation residual. The report/test compares native deposition against the independently printed 2496 MW total; that source total is not a physical ledger input. A supplied zero PbLi recovered-friction term is an explicit approximation to the source's omission of the very small listed 1–10 kW PbLi pumping term; it is not a claim of zero physical pumping or a complete electrical balance. Preserve the 156 MW He pumping number as separate source context; this increment does not turn its difference from 141 MW into a newly qualified motor-loss model.

[AGENT] Each branch has its own independently supplied hypothetical exchanger duty rating in MW. Suggested baseline scenario: He 1250 MW and PbLi 1500 MW, explicitly AGENT offered capabilities at assumed supported conditions, not ARIES installed equipment. The existing guarded capacity calculation compares each computed branch duty with its supplied rating and its existing executable constraint asserts adequacy. This is a necessary scalar duty screen only; no UA, pinch, materials or pressure qualification follows.

## Roles and acceptance

| Quantity | Role/authority |
|---|---|
| Branch depositions | Supplied source-derived boundary inputs 940/1555 MW; no independent nuclear-heating prediction |
| Exchange and He friction | Supplied source values 111/141 MW; perturbations are explicit scenarios |
| PbLi recovered friction | Supplied AGENT zero approximation for the printed balance; no physical zero-pump claim |
| Printed blanket total | Independent 2496 MW report/test source check, not a physical ledger input |
| Branch duty/combined duty/residuals | Calculated physical accounting |
| Offered exchanger ratings | Chosen independent hypothetical design inputs; never resized from duty |
| Applicability/support flags | Explicit conditional capability assumptions; unsupported cases remain undefined |

[AGENT] Acceptance: native generation/sealing/TEAx execution of the baseline; smaller supplied rating on each branch; increased deposition with original ratings held; changed exchange with combined heat unchanged; zero friction with duties reduced exactly once; unsupported offered conditions; and invalid nonfinite/negative inputs or negative branch duty. Independent energy arithmetic must show internal transfer cancellation and preserve the -1 MW source-total residual. Failed capacity cases leave the supplied ratings unchanged. Cost and physical exchanger adequacy are outside scope, so no cost-response claim accompanies these screens.

[AGENT] Expected semantic delta: two new elementary accounting definitions and one dual-coolant assembly; one existing capacity calculation and one existing constraint definition reused unchanged across two branches. Review source meanings, the sole exchange owner, all energy signs, the PbLi friction approximation and the distinction between source reproduction and prediction before implementation. The source images already support this bounded step; broader hydraulic or whole-cycle qualification still requires additional physical inputs. T09 conversion should follow its own reviewed contract after T08, including the separate divertor contribution and cycle states.
