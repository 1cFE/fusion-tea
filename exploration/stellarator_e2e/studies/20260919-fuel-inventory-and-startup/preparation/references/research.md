---
date: 2026-09-19
researcher: Codex fuel_sources
topic: Tritium residence inventory and external startup supply
tags: [tritium, fuel-cycle, residence, startup]
research_type: domain
---

# Tritium residence inventory and external startup supply

## Research question

[INHERITED: work/orchestration/goals/fuel-inventory-and-startup/evidence/research-brief.md] Establish admissible physical relationships and useful ranges for injection/plasma, exhaust, isotope separation/storage, blanket extraction and reserves in a steady DT plant. Preserve inherited burn fraction 0.05 and exhaust recovery 0.99. This report supports conditional inventory/startup analysis, not breeding design or equipment costing.

## Summary

- [SOURCE FACT] A compartment model can represent tritium stock and return flow using a mean residence time. Abdou et al., Eq. 3.1, explicitly includes inter-compartment flows, breeding, radioactive decay and other losses. The appropriate stock is isotope-specific.
- [SOURCE FACT] Abdou Tables 2–3 supply useful scenario brackets: fuelling 20–30 minutes; combined exhaust clean-up/isotope separation 1.3–5 hours; breeding-zone residence 0.1–1 day with a historical 10-day case; breeder extraction approximately online through 1–5 days batch-wise. These are heterogeneous design/model assumptions, not measured limits for this plant.
- [SOURCE FACT] Reserve stock covers disrupted circulating supply. It is not automatically a chosen number of days of burn consumption. Initial stock is chosen so usable storage never falls below the reserve during startup (Abdou §3.5, Eqs. 3.8–3.9).
- [AGENT] A finite startup transient and long-run adequacy are separate outputs. With a permanent steady deficit, no finite initial stock sustains indefinite operation. A startup calculation over a finite horizon must not conceal that deficit.

## Evidence and inspection

Two sources were registered through the native registry. Source identity and extraction hashes are in the request receipts. Both raw texts were screened for quarantine tokens before content inspection; no matches occurred. No excluded project concept or barred source was opened.

1. Abdou et al., *Physics and technology considerations for the deuterium–tritium fuel cycle and conditions for tritium fuel self sufficiency*, Nuclear Fusion 61 (2021) 013001, DOI 10.1088/1741-4326/abbf35. Registered extraction: `knowledge/sources/abdou_2021_dt_fuel_cycle_physics_technology_and_tritium/output.md`. Original university-hosted PDF: https://cpb-us-w2.wpmucdn.com/research.seas.ucla.edu/dist/d/39/files/2019/08/Abdou_et_al_Physics_and_Technology_Considerations_Nuclear-Fusion_V61_2021.pdf. Original raw pages 6, 9 and 11 were rendered and visually checked for Eq. 3.1, Eqs. 3.8–3.9, and Tables 1–3.
2. Lord et al., UKAEA-STEP-PR(24)12, *Fusing together a design for sustained fuelling and tritium self-sufficiency*. Registered extraction: `knowledge/sources/lord_2024_step_sustained_fuelling_and_tritium_self/output.md`. Original PDF: https://scientific-publications.ukaea.uk/wp-content/uploads/UKAEA-STEP-PR2412.PDF. This public UKAEA PDF is an annotated draft, with unresolved author comments. Its raw pages 10 and 14 (printed pages 6 and 10) were visually checked. The publication landing page points to the eventual Philosophical Transactions A article, but PMC full-text access returned a browser challenge. Treat these draft numbers as provisional; they are not adopted as plant constants.

Prior context: `knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md`, fuel section, supplies the inherited isotope-boundary and startup-accounting recommendations. No relevant fuel-cycle DI was found in `knowledge/KNOWLEDGE.md`; no insight was promoted or superseded.

## Physical relationships

[SOURCE FACT] Abdou Eq. 3.1 is `dI_i/dt = sum_j(F_ji) - (1+epsilon_i)*I_i/tau_i - lambda*I_i + S_i`, with return flow `I_i/tau_i`. It represents a well-mixed lumped compartment, not a deterministic transport delay. At steady state without loss/decay, `I_i = F_i*tau_i`. With the source's other-loss convention, `I_i = F_in/(1/tau_i + epsilon_i/tau_i + lambda)` when there is no local source. A model must keep its selected loss convention consistent; do not equate the source's epsilon to the inherited 1-r without deriving the mapping.

[AGENT] Use tritium mass throughout inventory accounting. With the inherited plasma-boundary burn definition, `F_T=B_T/f`, `U_T=F_T-B_T`, and permanent exhaust loss is `(1-r)*U_T` if that is the confirmed existing meaning. Do not introduce Abdou's separate fuelling efficiency as an additional loss or throughput multiplier unless that new boundary is explicitly modeled. Neither D-plus-T mass flow nor total molecular gas flow can replace these tritium flows.

[AGENT] A consistent outlet-loss convention for the combined exhaust processor is `dI_ex/dt=U_T-I_ex/tau_ex-lambda*I_ex`, `F_return=r*I_ex/tau_ex`, and `F_permanent_loss=(1-r)*I_ex/tau_ex`. Thus its stock is approximately `U_T*tau_ex`, before outlet recovery loss, rather than `r*U_T*tau_ex`. This is an explicit adaptation of the source compartment method. The source does not establish separate exhaust-cleanup and isotope-separation delay allocations. Plasma stock should follow the existing plasma tritium particle inventory integral if available; the 20–30-minute source time applies to fuelling equipment.

[SOURCE FACT] Abdou Eqs. 3.8–3.9 define `I_storage_min=I_reserve` and `I_reserve=F_T_injection*q*t_reserve`. Table 1 chooses `q=0.25` and `t_reserve=24 h` for analysis. These are selected interruption scenarios, not a reliability requirement. The source finds substantial stock penalties for long reserves.

[AGENT] For a given operating schedule and initially empty process compartments, solve storage alongside the return dynamics. Without storage decay, `I_initial_min = I_reserve + max_t integral_0^t(F_withdraw-F_return-F_usable_bred) ds`, bounded below by the initial reserve. Include storage decay in the dynamic equation when non-negligible. Distinguish purchased initial stock, usable reserve, transient minimum storage and working inventories. Do not add the equilibrium working inventory again to this cumulative deficit: its filling is already in the balance. For a deterministic-delay approximation, state that approximation and its startup difference from the source's mixed compartments.

## Usable ranges and transfer limits

| Function | Source evidence | Appropriate use here |
|---|---|---|
| Fuelling delivery | Abdou Table 2: 20 and 30 min | Scenario range for delivery holdup; not plasma confinement time |
| Exhaust clean-up plus isotope separation | Table 2: 1.3 h, 5 h, 0.1 day, historical 1–24 h; analysis 4 h | Use one combined delay unless separate stages have separately supported allocations; 1.3/4/5 h are useful sensitivity anchors |
| Water detritiation | Table 2: 1 or 20 h | Apply only to the diverted water-recovery stream, not all injection flow |
| Breeding zone | Table 3: 0.1–1 day from EXOTIC experiments; historical 10 days | Scenario transfer only; experiments and historical model do not qualify helium/PbLi residence |
| Tritium extraction system | Table 3: negligible online, 1 day, 1–5 days batch | Extraction performance depends on blanket/extractor technology; zero is an ideal diagnostic, not a claim of instantaneous hardware |
| Coolant purification | Table 3: historical 100 days; 10 days explicitly chosen for analysis | Applies to permeated coolant tritium only; slow recovery is not permanent loss |
| Wall/divertor retention | Table 3: 1000 s model values | No universal physical retained stock; require retained fraction and recovery mode before adoption |
| Reserve/storage | Eq. 3.9 and Table 1: 24 h at 25% disrupted circulation | Agent may choose 0/6/24 h and state q, with zero as diagnostic; storage residence is an operational stock choice |

[SOURCE FACT] Lord printed p. 6 (`output.md:138`) describes approximately 30-minute cryopump adsorption/regeneration batches, rapid bulk-fuel recycle, and a smaller stream through plasma exhaust processing and isotope adjustment. A batch period is not a mean residence time; the mean depends on capture and release scheduling. Do not add this period to Abdou's combined exhaust delay automatically. Lord printed p. 10 (`output.md:224` onward) estimates approximately 3 kg nominal steady inventory including first-wall retention and blanket holdup, plus a possible extra kilogram for startup/control buffering. These are STEP architecture estimates, not plant-scale laws. STEP uses helium-cooled liquid lithium, not the retained PbLi blanket.

## Recommended bounded model and missing evidence

[AGENT] Preserve distinct component ownership for injection, combined exhaust processing, blanket release/extraction, and usable storage. Use the source compartment ODEs or an explicitly labeled delay approximation. Link each component's incoming isotope flow to its residence stock. Use the existing achieved breeding result as the generation input and keep extraction delays separate from permanent recovery loss. Report operating, startup, interruption reserve and shutdown-decay modes separately.

[AGENT] A useful conditional scenario is 20-minute fuelling, 4-hour combined exhaust processing, 1-day breeding-zone release and 1-day extraction, with reserve varied independently. This is a declared transfer of an analysis case, not an optimum or inferred plant capability. Separate breeder zone and extraction delays to avoid counting one physical hold-up twice.

Missing: demonstrated helium/PbLi residence/extraction performance for the modeled configuration; separate exhaust-versus-isotope stage allocation; plasma particle inventory/confinement law; wall capture/release fractions and irreversible trapping; bypass/divertor gas throughput; actual startup power ramp; specific interruption contingency and available purchased stock. These gaps limit physical qualification, while mass-conservation and conditional stock calculations remain feasible. No equipment price or global tritium supply availability was established.
