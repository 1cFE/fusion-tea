# Independent T08 heat-transport source review

[AGENT] 2026-09-21. Focused source/boundary review of retained Raffray primary Table II p734, Figures 12/13 p736 and Table III/discussion p737. Images are `outputs-page-09.png`, `outputs-page-11.png` and `outputs-page-12.png` under `.project/active/aries-comparison-preparation/post-reveal-results/post-reveal-v1/source-evidence/retained/knowledge/holdout/aries-cs/extracted/20260920-r3/08-FST-Raffray/`. Also inspected existing `mfe_primary_loop.sysml` and its normative typed completion. No new acquisition or full-model test is claimed.

## T07 inherited disposition

[AGENT] The appended maintenance/availability section in `scientific-prerequisites.md` faithfully retains the existing single bundled-clock limitation, missing actual component replacement/outage inputs and distinction between supplied availability and predicted reliability. Its calendar/full-power-year accounting handoff is appropriate. It claims no new lifecycle execution or qualification.

## Source boundaries

- [INHERITED: Raffray Table II p734] Blanket helium inlet/first-wall outlet/module outlet are 386/430/456 degrees C; pressure is 10 MPa; total blanket/HX helium pressure drop is 0.30 MPa; total helium mass flow is 3261 kg/s. Removed heat 1192 MW explicitly includes 141 MW friction and 111 MW conducted from PbLi. Blanket helium pumping power is separately 156 MW. Friction heat and electrical pumping draw therefore must not be equated.
- [INHERITED: Table II] PbLi heat removal is 1444 MW, explicitly reduced by approximately 111 MW conducted to helium. PbLi inlet/outlet are 451/738 degrees C. The table separately lists total blanket fusion thermal power 2496 MW. Those values belong to this engineering design case; they are not automatically the final systems-study operating point.
- [AGENT derivation from Table II] Removing helium friction gives 1051 MW helium heat from other sources; additionally removing PbLi transfer gives 940 MW direct helium heating. Restoring transferred heat to PbLi gives 1555 MW. The direct branch total is 2495 MW, versus printed 2496 MW; preserve this 1-MW residual as source rounding/boundary discrepancy rather than fitting an input to eliminate it. The 111-MW transfer cancels when summing branches; 141-MW external pumping/friction contribution does not.
- [INHERITED: Figs. 12/13 and p737] Blanket helium, PbLi and divertor helium have distinct heat-exchanger paths feeding the cycle helium. The power cycle has three compressor stages, intercooling and recuperation. The 0.89 compressor efficiency in Table III is a power-cycle parameter, not evidence of blanket-circulator efficiency. Discussion explicitly adds helium friction heating to fusion thermal power and subtracts pumping power when reporting net cycle behavior.

## Existing loop compatibility

[AGENT] The existing primary-loop calculation uses `mdot=q_source/(cp*dT)` and then adds computed fluid work to produce `q_ihx=q_source+w_fluid`. Its source-heat interface explicitly excludes pump credit. Passing 1192 MW as source heat while additionally recovering fluid work double-counts the source's included friction contribution.

[AGENT] Passing 1051 MW avoids that specific double count but cannot reproduce the entire source temperature/flow set unchanged: 1192 MW divided by 3261 kg/s and 70 K implies `cp=5221.886362640733 J/(kg K)`, whereas 1051 MW implies `4604.196784509572`. These are diagnostic ratios, not independently justified property selections. In particular, do not tune cp or circulation efficiency to make a reference match. The table's temperature rise spans a heat balance that includes distributed friction, while the existing idealized circuit accounts for compressor work at a different boundary.

[AGENT] A useful bounded next increment can evaluate explicit branch heat bookkeeping and/or the existing loop under a clearly selected boundary, retaining the source-flow/temperature discrepancy. Reuse of its square-law loss relation requires an explicitly conditioned reference anchor; it does not establish ARIES hydraulics, MHD or equipment support. Supplied ratings must remain independent of required flow. No dual-coolant, Brayton, full-plant or cost qualification follows merely from a successful helium arithmetic run.

[AGENT] Author scope and design are pending. Source-derived identities above are available for that gate; implementation acceptance requires a concrete contract and native evidence.

## WI-086 source/design disposition

[AGENT] Accepted for implementation against `work/active/WI-086_aries-dual-blanket-heat-accounting/spec.md`. The contract correctly selects new two-branch bookkeeping instead of claiming unchanged hydraulic-loop transfer. One owned exchange feeds the helium addition and PbLi subtraction. Friction is an explicit thermal contribution, distinct from electrical pumping. The selected zero PbLi recovered-friction approximation is disclosed against the small source pump term. Branch duty reconstruction is not labeled independent prediction.

[AGENT] The new ledger consumes actual exposed branch duties and supplied deposits/friction. Its signed internal residual is `delivered_total-deposited_total-friction_total`. The separate report/test subtracts the printed 2496 MW from the native deposition total, retaining -1 MW without inserting the comparison target into physical evaluation. This separation preserves the discrepancy and avoids fitting to the source total.

[AGENT] Two independently supplied ratings, unchanged generic capacity screens and real asserted constraints are an appropriate limited downstream consumer. MR-7 checks must demonstrate insufficient/sufficient selected capacities and increased deposition at fixed equipment, while exchange perturbation cancels in combined duty. Undefined capability remains distinct from shortage. Finite/nonnegative input guards, refusal of negative branch duty and finite signed residuals are suitable for the algebraic contract. Final implementation acceptance still requires actual generated edges, native arithmetic/refusal/capacity evidence and scoped validation.
