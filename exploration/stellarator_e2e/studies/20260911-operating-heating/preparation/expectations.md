# Independent pre-execution expectations

[AGENT] Deposited before any T-019 TEAx baseline or point. These equations are study acceptance expectations, independently stated from conservation and the retained accounting contract. The preliminary oracle probes selected candidate inputs; their outputs are predictions, not independently measured study results. The oracle shares no generated code, but some historical mirrored arithmetic shares statement forms, so its parity is not an independent source/engineering audit.

## Signed conversion and capacity

Let D be the signed sustained coupled demand, s=0.5 the held source efficiency, c=1 the held coupling efficiency, and H the installed electric capacity. The direct installed delivery/coupling additions remain zero. Installed delivered power is sH; installed coupled capacity is csH. Operating coupled, delivered and electric powers are D, D/c and D/(cs). The signed margin is D−csH. Capacity is satisfied when D≤csH; burn hold is satisfied when D≥0. All 18 native assertions must remain individually visible, including the four strict-positive/at-most-one efficiency assertions.

No clipping is allowed. Negative D is an invalid burn-hold diagnostic even if other thermal and economic outputs remain finite. Exactly zero means the native float equals zero. A residual within numerical tolerance but unequal to zero is near-zero. The center was declined before execution under review F2; its construction below is preliminary evidence only. The coordinated candidate at density 6.578e20 uses f*=0.9539975336025179, obtained by affine interpolation between f=0.95 and 1 at fixed density and other inputs. It lies within [0,1], and the preliminary oracle residual is −1.1368683772161603e-13 MW. The two flanking fractions differ by ±1e-5 and should give opposite signs. This is a deliberately constructed diagnostic, not a solved physical operating boundary.

The inherited generic/native exact-zero fixture in `context/inherited-boundary-results.json` is separate evidence from WI-050. It does not prove an exact-zero full stellarator case in this study. The source audit and runner are copied alongside it so a later reader can recover the scope.

## Reserve intervention

Changing H at fixed plasma and efficiencies must leave D, all operating heating powers, source heat, primary-loop flow/pressure/work, recovered heat, cycle state, gross/net power, divertor operating heat and target flux unchanged. Fuel, availability and annual operating/replacement accounts must likewise remain unchanged. The installed-capacity subtraction diagnostic and capacity assertion may change. The module-level indicator's divertor reach is not an operating response.

Heating procurement must be installed delivered MW × $5,282,900/MW. Therefore the proposed 100→120 MW reserve pair must change this account from $264,145,000 to $316,974,000. The capital change must propagate through actual named rollups and IDC/finance. No operating-energy denominator or annual-cost change is expected for this pair. Lower installed capacity can have lower modeled LCOE while failing capacity; it is not an improvement in plant feasibility.

## Demand interventions and conservation

At held installation the heating procurement account must remain exactly unchanged for every demand intervention. Other power-scaled equipment costs may change because the retained model uses design-point sizing relations. Attribute those changes explicitly; do not call them purchased heating equipment or pure running expense.

At fixed plasma solution, D=P_rad+W/tau−f_alpha*A, where A is fusion alpha power before retained-fraction loss. Thus changing only retained-alpha fraction gives ΔD=−AΔf_alpha. The divertor absorbed heat f_alpha*A+D=P_rad+W/tau is invariant for that particular intervention. Source heat uses its authored total alpha accounting and D; it need not be invariant. Density changes alter fusion, ash, confinement and radiation as well as D; their changes cannot be attributed solely to auxiliary heating.

Independently check source conservation Q_s=m_n(P_fus−P_alpha)+P_alpha+D, with P_alpha=(3.52/17.58)P_fus. Check mass flow mdot=10^6 Q_s/(c_p ΔT), per-loop flow mdot/N_loop, pressure drop f_loss Δp_ref(mdot_loop/mdot_ref)^2, compressor ratio p/(p−Δp), fluid work mdot c_p(T_in−T_comp,in)/10^6, electric pump draw W_fluid/eta_drive, and heat exchanger load Q_s+W_fluid. Check modeled recovered heat and pump totals using their held live/direct mode inputs. Check P_th=Q_s+Q_recovered, P_gross=eta_cycle P_th, and P_net=P_gross−P_recirc, where recirculation includes the computed operating heating draw and all named non-heating loads. Cycle temperature and efficiency remain constant when their held temperature inputs do.

Check divertor absorbed heat=P_alpha,retained+D, separatrix heat=absorbed−core radiation, target nonradiative heat=absorbed×(1−f_rad,total), target peak=target nonradiative×q_target,ref/P_nonrad,ref, and required-minus-installed=D−csH. Preserve the authored target threshold and report the baseline violation.

## Cost, finance and baseline bridge

For each current case, use the recorded named capital and annual accounts to calculate the annual capital numerator and annual-equivalent energy. Headline LCOE=(C_head+A)/E; comparison LCOE=(C_comp+A)/E at n_mod=1. Independently calculate CRF as the inverse finite discount-factor sum over operating years. C_head=total_capital×(1+d)^(construction_years/2)×CRF. C_comp=(overnight_capital+IDC)×CRF_annual. E=8760×P_net×calendar availability. Keep the actual capital/IDC inputs and levelized annual accounts in the evidence; never infer numerator solely by multiplying LCOE by energy.

Use the exact additive bridge from case 0 to case 1: capital contribution=(C1−C0)/E0; annual contribution=(A1−A0)/E0; energy contribution=(C1+A1)×(1/E1−1/E0). Their sum must reproduce ΔLCOE at 1e-9 relative/absolute tolerance. Report both current baseline→intervention bridges and the inherited pre-repair→current-baseline bridge as distinct evidence classes.

The inherited model audit's historical headline change is −0.340291843655 $/MWh, with capital +0.00247929168711, annual +0.00438032137948 and energy −0.347151456721. These are copied audit facts, not a rerun of the historical package. The copied attribution and independent-finance artifacts carry the actual numerators/energy and comparison LCOE. New T-019 evidence must reproduce the current pinned baseline before adopting that historical bridge as context. A dated-energy shadow remains a diagnostic; no finance convention is changed.

## Acceptance and limitations

All completed cases receive the stock verifier's full objective and predicate comparison, using all 15 executed proposals as the requested sample. This automatically covers every observed verdict combination. The additional identities above cover heating/source/loop/net/divertor and procurement/finance channels beyond the generic verifier's manifest catalog. Exact equality applies only to claimed invariances or native-zero classification; computed identities use 1e-9 relative/absolute tolerance and retain residuals.

Source efficiencies, optimistic unit coupling, empirical plasma assumptions, calendar rules and design-point cost scaling are held. Density has no sourced engineering window or added density-limit screen here. Negative-demand cases are invalid diagnostics, and the baseline is already divertor-violating. No feasible plant, optimum, engineering operating envelope, inherited plant-closure window completion or regrade is claimed. Syntax/structural validation, translation parity, independent identities and engineering coverage remain separate. Existing audit checker debt, historical-export failures and engineering omissions remain explicit in copied audits.
