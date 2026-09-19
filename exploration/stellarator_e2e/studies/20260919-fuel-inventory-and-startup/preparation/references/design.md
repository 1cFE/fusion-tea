# Fuel inventory and startup design

## Physical boundary and authority

[AGENT] Use nominal steady stage inventories and a deterministic-delay startup approximation. The source compartment model supports conservation and the flow×residence relation, but does not prescribe deterministic return times. Original evidence and image checks: `knowledge/research/pending/20260919-074901_fuel-inventory-residence-startup.md`; source `knowledge/sources/abdou_2021_dt_fuel_cycle_physics_technology_and_tritium/output.md`, Eq.3.1, Tables1–3 and Eqs.3.8–3.9. Retain the existing cost-derived conditional 99% isotope recovery; this design changes no loss meaning. Unmodeled wall retention, coolant permeation, detritiation, impurity/carrier streams and bypass are unresolved. They are not silently included in permanent loss or assigned zero as a qualified prediction.

## Components and stocks

[AGENT] Represent injection equipment, plasma, combined exhaust clean-up/isotope separation, breeder release, breeder extraction, and usable storage as identifiable stock occurrences under Fuel Cycle. Preserve blanket ownership of gross TBR and production inputs. Existing achieved-breeding applicability must govern interpretation of inventory involving production; invalid production must not become a physical zero. Keep generic Fuel Cycle dormant by default; enable this calculation in the stellarator. All dimensional numerical scalars use declared SI units (seconds, kilograms, atoms, rates); no dimensional inference from names is sufficient documentation.

Let B=P_fus*1e6/(Q_MeV*c_MeV_J) be T atoms/s, F=B/f, U=F−B, R=rU, L=(1−r)U, J=TBR*B and S=ηJ. The single combined processor receives U and releases R to storage and L permanently outside the usable fuel system at its outlet. Do not split its sourced total residence into invented substage times. Breeder zone and extraction each receive J nominal atoms/s; extraction efficiency acts once at the final outlet. Decay is accounted separately as a replacement demand on nominal maintained stock, not a second recovery fraction.

| Stock | Nominal T amount [atoms] | Basis |
|---|---|---|
| Feed equipment | F τ_feed | Abdou Table2 fuelling machinery residence; distinct from plasma confinement |
| Plasma | n_T0 V/(1+α_n) | Existing fuel profile n_T(ρ)=n_T0(1−ρ²)^α_n integrated over dV=2Vρdρ; require α_n>−1, V≥0, n_T0≥0 |
| Combined exhaust processor | U τ_process | Table2 combined clean-up/isotope separation, recovery loss at outlet |
| Breeder zone | J τ_blanket | Table3 zone-release assumption |
| Extraction equipment | J τ_extract | Table3 separate extraction delay, no second blanket fill |
| Usable working buffer | F τ_buffer | Explicit operating storage policy, independently declared from reserve |
| Reserve | F q τ_reserve | Source Eq.3.9 interruption definition; q is unavailable circulating fraction, not permanent loss |

[AGENT] I_work sums the first six stocks; I_total=I_work+reserve. Convert each through existing m_T. Bind computed I_total into the existing fuel calculation and breeding adequacy, preserving their formulas. The generic dormant selector may return the previous held inventory for legacy instances. For active stellarator, remove the old independent I_total input. To avoid a calc cycle, inventory derives B from the owning power/energy inputs independently of the fuel calculation that consumes its stock; verified equality must hold. Plasma exposes its own V, n_T0 and α_n interfaces. Stock occurrence amounts bind the corresponding calculation outputs; sum/output definitions remain inspectable.

## Startup condition and calculation

[AGENT] At t=0 feed equipment, plasma, working storage buffer and reserve are prefilled. The processor, breeder zone and extraction start empty. Begin ideal constant full-power operation immediately; the prefilled plasma is at its operating particle content. This avoids inventing a plasma transit residence and is not a physical ignition/ramp simulation. Recycle first arrives at τR=τ_process; bred fuel arrives at τB=τ_blanket+τ_extract. The horizon is H=max(τR,τB)+τ_extension. The extension is a declared duration after both return streams become available, useful when the operating balance is deficient.

D(t)=Ft−R max(t−τR,0)−S max(t−τB,0), evaluated at t=0, τR, τB and H. Let d=max D(t), including zero. No-decay minimum initial external amount M0 is feed stock + plasma stock + usable working buffer + reserve + d. Other stage fills are already inside d; breeder stock is produced internally. Expose d, H, M0, prefill, reserve and operating stock separately.

[AGENT] Protect initial supply against decay with conservative allowance A=k(M0+JH)/(1−k), k=λH, requiring 0≤k<1. Report M0+A as conservative startup supply, not exact minimum. Bound proof is in goal `evidence/math-precheck.md`: total plant T never exceeds initial supply plus gross breeding during H, so this allowance bounds decay including its own decay. The abstract supply boundary assumes allowance can replace decayed stock where needed; transport/availability of that replenishment is not demonstrated. Nominal residence stock ignores in-transit decay; report max(λτ_i) as a scale diagnostic rather than claiming exact transient inventory. No unsupported domain threshold is made into a physical screen.

[AGENT] Reserve is counted once and is not fuel purchased repeatedly. G_stock remains zero in this single-plant inventory scenario; active mode must reject nonzero G rather than silently omit it. A finite startup stock does not sustain an ongoing shortage indefinitely. Report signed operating makeup B+L+λI_total−S and nonnegative external shortfall separately; a negative signed value is excess available supply, not negative consumption. The required-breeding formula remains (B+L+λI_total+G)/(ηB).

## Operating capacity, calendar and shutdown

[AGENT] Export T burn/injection/exhaust/recycle/production/extraction/loss in kg/s, with kg/day running capacities for costing. Export total D+T injection and exhaust/processor inlet kg/s using equal D/T atom rates and the separately cited D atomic mass; D/T is equimolar, not equal-mass. Export helium ash atom flow as B separately if needed; do not fold it into hydrogen-isotope demand. Breeder kg/s means tritium throughput, not PbLi carrier circulation.

[AGENT] Annual running totals multiply by calendar availability times seconds/year. Calendar-average capacities equal annual amount/seconds/year and must not be used as required running capacity. Annual decay replacement is λI_total times all calendar seconds, independent of availability. Annual signed makeup is (B+L−S)*availability*seconds/year+λI_total*seconds/year. Nominal held stock persists through shutdown as a maintained design inventory; no release/ramp or drain-down is implied. Also expose passive stock remaining after a declared shutdown duration as I_total exp(−λ t_shutdown), and its decay loss, distinctly from the maintained-stock replacement policy. Use stable expm1 for small decay losses.

## Declared stellarator scenario and sensitivities

All following values are [AGENT] choices drawn from source scenarios or explicit policy; none is a measured specification of this plant. Preserve f=0.05, r=0.99 and η=1.0. Source Tables2–3 justify τ_feed=1200s (20min), τ_process=14400s (4h), τ_blanket=86400s (1d) and τ_extract=86400s (1d). Keep these last two separate. Choose working buffer τ_buffer=0s to show the minimum nominal operating stock; reserve q=0.25, τ_reserve=86400s follows the source analysis interruption case, not a reliability requirement. Set τ_extension=0s and passive shutdown demonstration=86400s. Cite D mass3.3435837768e−27kg through existing fuel_cost_per_rxn source record.

Study source scenarios: feed20/30min; combined processor1.3/4/5h; blanket0.1/1d; extraction0/1/5d (zero explicitly ideal online limit); reserve0/6/24h at q=.25, plus q=0/1 diagnostics; working buffer0/1h explicitly assumed. f=.025/.05/.10 and r=.99/.999/1 are conditional sensitivity brackets and ideal limits, not performance upgrades. Change fusion power through a supported causal density or temperature input, never sweep computed power. Include η=.95/1 as assumption sensitivity, a post-return extension to expose ongoing deficits, zero decay, passive half-life test and unsupported/nonfinite inputs in verification. No search for self-sufficiency or small stock.

## Software evidence

Use a manual library calculation if piecewise/exponential operations require it, with authoritative equations above, strict seed custody and no caller-side physical computation. Verify particle-profile integration independently, startup via time-integrated storage trajectories and event hand cases, decay-bound inequality, exact half-life, nonnegative stocks, conservation, dimensional transformations and domain refusals. Test availability changes leave installed processing capacity unchanged. Validate preserved generic behavior and old required-breeding expression at held/computed stock. Independent oracle must not import production code; compare every new native numeric output and changed existing fuel/breeding output. Full static diagnostics are retained and classified by identity against entry evidence. Independent audit and native integration precede the focused study.

## Released applicability behavior

[AGENT] The final ABI is `evidence/proposed-abi.md`. Active inventory computation publishes `defined_flag=1` only when the existing blanket production is defined. Unsupported breeding retains the inherited diagnostic execution route: nonbreeding stocks/flows still compute, production-dependent finite carriers use zero gross production for execution only, and `defined_flag=0` invalidates their physical interpretation (including total/startup/decay-derived claims). The existing breeding adequacy flag also fails. Strict invalid arithmetic, fractions, times, selectors and nonzero active G_stock raise errors rather than becoming undefined carriers. Dormant generic activation returns held_inventory through total_atoms and `defined_flag=0`; it makes no new stock/startup claim. Test these branches explicitly.
