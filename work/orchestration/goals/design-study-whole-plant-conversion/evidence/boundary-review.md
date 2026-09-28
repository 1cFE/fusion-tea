---
Verdict: concerns
Created: 2026-09-27
Related Artifacts:
  Design: ../../../../active/WI-098_whole-plant-conversion-comparison/design.md
  Spec: ../../../../active/WI-098_whole-plant-conversion-comparison/spec.md
---

# Independent complete-boundary review — submission 1

**Verdict: FINDINGS. MR-7: unverified for the complete proposed interface; no automatic sizing was found in the declared equations.** Resolve F1–F3 before releasing this design for implementation. This review does not certify the unexecuted 48 kA offer, a complete operating reactor, or study results.

[AGENT] Fresh non-author review under [boundary-review-brief.md](boundary-review-brief.md). The coordinator submitted complete r1 and froze author edits during review. Reviewed `work/active/WI-098_whole-plant-conversion-comparison/design.md`, SHA256 `af866555a022e52a68e01b875da6fa8f71e447a0844c853313143f0c1467b4a2`, and `configuration.md`, SHA256 `fd732ba5928a668e71cf62598d5b6a3ef2b10ec79e5efe774f8e58009fc70bda`. Only this review and supporting evidence were written.

## Material findings

### F1 — Major capital-account scopes disappear

**Location:** design §5, “No old whole-plant CAS20/CAS29/CAS30/CAS50 … totals are added”; configuration initial-capital table and lifecycle table.

Avoiding old aggregate totals is correct, but the new inventory has no replacement ownership for contingency, engineering/construction indirect services, applicable freight/tax/insurance, general spares beyond the named primary/salt spares, or nonfuel commissioning. The USD200 million allowance is expressly for wider casing/support/civil/fuel extraction/storage. The USD509.888 million installation leaf is inherited core assembly. Neither has declared these missing scopes. Construction financing does not purchase engineering or construction services.

The distinction is explicit in `models/library/analyses/mfe_account_costs.sysml`: `Indirect Cost` at line332 calculates an indirect-service allowance separately from IDC; `Supplementary Cost` at line657 owns shipping, spares, tax, insurance, startup and decommissioning. `models/designs/generic_mfe/mfe_plant.sysml:570` separately owns contingency and indirect cost. The retained active WI-080 output amounts are `contingency__cost=1214126696.9785411`, `indirect__cost=3561438311.1370535`, and `supplementary__cost=779542094.1813809` dollars. Those old totals include replaced equipment and cannot be transferred wholesale; their scale shows why their remaining scopes are material.

**Required correction:** Add a disjoint disposition of every major CAS scope, including explicit zero/omitted assumptions where justified. Bind replacement accounts to selected eligible purchases and documented exclusions. Remove the old decommissioning provision when adding the terminal event, and remove replaced startup fuel/spares/freight portions individually. State whether contingency is zero under a chosen estimate convention or separately charged. Expose the resulting category sums and test that new conversion offers change only their applicable overhead bases. Do not restore the old aggregates or absorb these scopes silently into the existing USD200 million allowance.

### F2 — Source migration leaves two possible independent inputs

**Location:** configuration electrical roles, `source_basis.q_source_MW`; design §§3 and6.

The proposed table says the new source input binds `primary_loop.q_source`, but that attribute does not exist in the retained assembly. The actual binding is `models/designs/component_alternatives/plant.sysml:40`, `primary_loop.evaluate.q_source_in = blanket_source.q_source`. The design otherwise preserves predecessor public conversion fields and explicitly retires only six finance input keys. It therefore does not say whether `blanket_source.q_source` remains the sole source authority, becomes a calculated alias, or is retired and mapped to the new input. A conversion heat input differing from the fusion/fuel input would make internally consistent ledgers describe different reactors.

**Required correction:** Declare one supplied source field and the exact new calc-input bindings. List the source input's public-interface migration alongside the already explicit finance migration. Reject differing duplicate source values if a compatibility form accepts both. Add a control showing that the one selected source drives primary flow/heat, fusion/fuel demand and both branches, and that no retained independent source knob is ignored. Likewise name the actual existing current key, `magnet__coil__turn_current`, in the capture contract.

### F3 — Deuterium and lithium purchase quantities are not specified

**Location:** design §4, “Deuterium and Li6 purchases follow reaction counts and stated recovery/feedstock assumptions”; configuration fuel-account row.

The document supplies D/Li6 prices but does not state the promised recovery/feedstock equations or a lithium atomic mass. Tritium has a clear physical purchase equation; D and Li6 do not. Reusing the old combined per-reaction price would restore its shared burn/recovery multiplier while the new model separately accounts for breeding, external T and full PbLi replacement. The legacy formula expressly treats Li6 as the tritium feedstock (`stellarator_plant.sysml:1459` and `mfe_account_costs.sysml:806`); it is not automatically the desired purchase model here.

**Required correction:** State separate D and Li6 purchased-mass equations, their recovery and isotope assumptions, and the relation between annual breeder makeup and full PbLi event refill. A declared conservative proxy is acceptable if labelled and counted once. Add a fuel-conservation/accounting check when breeding, extraction efficiency and recovery change. Do not add the old aggregate DT cost.

## Conditional source and magnet interpretation

[AGENT] The owner's explicit permission to supply a common source, accept modeling assumptions and omit vendor/physical-plant qualification supports this proposed conditional comparison. No additional owner gate is required solely because 8.64 T has no reconstructed plasma operating point. The source must remain independently supplied, `source_qualified=0` must remain visible, and the result must concern this altered assumed reactor inventory rather than the original demonstrated Stellaris design.

The new offer is materially different: chosen pack side0.54 m, aspect0.19, transverse cavity1.30 m, turn current48 kA and a separately priced40/60 kW cryoplant. These are supplied design choices, not purchases inferred from demand. The field arithmetic gives8.64 T axis and23.904 T peak. The existing conductor definition permits this field within its20–24 T prediction domain while retaining its material/construction limitations. The local-fit definition explicitly does not reprice casing/supports or establish global nonplanar fit. The design correctly carries that unresolved construction scope separately and does not call the installation allowance a physical pass.

The retained50 kA probe remains inadequate: it repaired local fit/current but exceeded cold/intercept ratings and retained field extrapolation. I inspected its report and native execution route. The48 kA offer has not been executed. Its exact map, repriced inventory, native component margins, conservative nuclear envelope and downstream cryogenic/support/facility consequences remain mandatory implementation evidence. Any newly discovered material failure requires disposition before ranking; a frozen captured pass bit or an allowance cannot replace it. Capture consistency must include price rates as well as geometry/current, and retained source values must identify the exact package and baseline.

## Checks supported by the submitted design

- **Source and electricity:** The supplied heat precedes circulation recovery. The fusion inversion subtracts deposited heating and uses the exact3.52/17.58 reaction fraction. Divertor heating deliberately preserves the inherited0.2002 convention. Primary electric consumption is subtracted once while fluid work reaches the exchanger once; changing drive efficiency changes motor loss without creating recovered heat. Branch pump/control loads and gas compressor shaft work have distinct owners. The new common auxiliary-rejection offer includes upstream heat and motor losses rather than assigning them to conversion equipment silently.
- **Known source exclusions:** The independent [original check](boundary-review/original-checks.json) reproduces fusion2112.151824/2370.782660/2543.203217 MW and divertor peaks8.582493/9.517084/10.140145 MW/m² for source2500/2800/3000 MW at H50. The unchanged3000 MW primary pressure and divertor failures remain excluded. The original facility occupancy failure is only−4.55e−13 m²; numerical equality repair needs declared evidence rather than a fabricated building change.
- **Heat interfaces:** Actual exchanger return is used for cold terminal approach, while mixed return still closes the source loop. Strictly positive actual/profile gaps match the inherited conversion contract. No unsupported30 K global threshold is introduced. Existing finite-cooling/property/capacity failures remain enforced.
- **Tritium:** Annual need includes productive-time burn and unrecovered exhaust plus calendar decay of selected5 kg. Breeding/extraction is deducted once; external supply is nonnegative and excess receives no revenue. Startup purchases selected stock once, with a separate startup-adequacy test. Breeding self-sufficiency remains a separate condition. Source Table6 prints TBR1.074 and approximately10 FPY coil life; the retained1.198074/1.186146 scenarios are the model's conditional transport surrogate, not the paper's qualified breeder.
- **Finance:** One shared rate/horizon/availability and six explicit retired finance inputs prevent branch disagreement. The commissioning midpoint factor applies to initial purchases once; future event PV is added afterward. Annual costs and export energy share end-year discounting; terminal costs are discounted once. Import electricity has a separate expense and net-grid admission check. Integer calendar-year life should be enforced if implementing the written finite annual sums; fractional-horizon behavior is otherwise unspecified.
- **Lifecycle:** Coil replacements at10 FPY are included with explicit outages; blanket/divertor events follow18/qwall FPY. At A0.80 the2500/2800 MW scenarios have four blanket events and two magnet events. The stated total outage budget is4.833333 years against six available years. This is a necessary aggregate service assumption, not a detailed achievable schedule. Event horizons exclude retirement exactly, and annual replacement reserves are not also charged. Eligibility lists for overhaul and salvage must become explicit leaf membership in implementation.
- **Currency and inherited scope:** Original CPI HTML rows independently confirm2004=188.9,2025=321.9 and estimated2026=334.4. The design distinguishes hypothetical USD2025 requotes from dated CPI adjustment and retains fixed steam offer magnitudes. It avoids dormant cooling/fuel costs and old full-plant aggregate totals. That treatment is valid subject to F1's missing scope.

## Remaining gate evidence and limits

The declared insufficient/sufficient capacity tests, demand-only inventory/cost invariance, capture-map consistency, unsupported field/property cases and independent output/predicate verification are appropriate. MR-7 cannot yet be certified for the complete new interface because F2 leaves the source role migration unresolved and no new native capture/package exists. Existing selected procurement and model demand remain separated in the inspected predecessor bindings.

The source installation allowance, auxiliary-rejection package, O&M allocation and other unknown scopes are explicitly hypothetical. Their0/200/1000M or similar stress values do not establish credible uncertainty bounds. The later study contract must either justify ranges or calculate the reversal thresholds for consequential unknowns, and limit its conclusion to the supported conditional region. This condition does not replace F1's requirement for an actual complete inventory.

Coverage reused the predecessor's valid WI-096 design, accounting, numerical-repair and repaired-results reviews within their conversion-only scope. No498-case rerun was performed. Original evidence read included active WI-080 output keys, the WI-075–080 selected-design contracts/capability inputs, actual source/fuel/primary/conductor/fit/account/DCF equations, retained source Table2/Table6 images, original CPI rows and the50 kA probe. Source quarantine was respected; no external retrieval, production change or baseline mutation occurred. This is the pre-implementation design gate, not final integration or economic assurance.
