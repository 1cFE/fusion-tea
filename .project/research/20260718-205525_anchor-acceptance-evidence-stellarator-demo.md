---
date: 2026-07-18T20:55:25-0700
researcher: Claude
topic: "Anchor acceptance evidence for the stellarator MBSE demo (Item 1)"
tags: [research, stellarator-demo, anchor-a, anchor-b, handshake, holdout, tolerances]
status: complete
last_updated: 2026-07-18
---

# Research: Anchor acceptance evidence for the stellarator demo

**Date**: 2026-07-18T20:55:25-0700
**Researcher**: Claude
**Research Type**: Codebase / Domain (evidence consolidation)

## Research Question

Item 1 of the STELLARATOR-DEMO epic (`.project/backlog/epic_stellarator_mbse_demo.md`) writes the pass/fail bars for the demo's two validation anchors. What evidence exists in-repo to ground **(a) Anchor-A handshake tolerances** and **(b) Anchor-B hold-out expectations**, and what does that evidence support? This is the evidence base only — the spec stage proposes numbers, the owner ratifies them ([OWNER] reserved gate, 2026-07-18).

Governing frame: `.project/concepts/stellarator-mbse-demo.md`, criteria 3 (Anchor A) and 4 (Anchor B). Barred paths per `knowledge/holdout/aries-cs/PROTOCOL.md` §3 were honored — no held-out or ARIES-CS-informed artifact was read.

## Summary

- **Anchor A parity is measured and tight where the machinery is actually tested.** Every formula-reproduced account matches 1costingFE end-to-end at ~1e-7 or better; the machinery (codegen faithfulness) is proven at the ~1e-8 formula-isolation level. The binding floor is **1costingFE's own float32 runtime**, worst measured deviation −4.8e-8 (CAS21), reference power table ~1e-7. **A per-account tolerance tighter than ~1e-7 is physically unachievable** and the spec must not ask for it.
- **The Anchor-A "gap" is structural scope, not machinery error.** The current handshake reproduces 12 formula-reproduced accounts under tolerance and *injects* 1cfe's own values for the rest — a −31% LCOE gap that is entirely unmodeled account scope (CAS22 tail ~$1.09B, CAS40/50/60, LCOE construction CAS70/80). Section D lists it account-by-account: this is the boundary between "must come under tolerance after Items 3–4" and "itemized-and-explained remainder" under the [OWNER] criterion-3 ruling.
- **There is no in-repo ground truth for Anchor B by design** — the whole point of the hold-out. Expectations must be set from two admissible sources only: **(E) our own model's sensitivity** (headline LCOE swung across roughly $176–$251 under seven corrections, ~±25–30%, before any ARIES-CS contact) and **(F) general estimating-accuracy classes** (AACE Class 5 concept-stage: −30%/−50% to +30%/+100%, admissibly sourced in-repo at arXiv 2602.19389 Table 3). No "ARIES-CS is probably around X" reasoning was used or is available.
- **The mapping-trap inventory is complete and mostly enforced in code** (Section C, 14 traps). The commit pin `0254385` is asserted in code (`handshake_1costingfe.py:115`), but the pin-change *procedure* is undocumented — a spec gap.
- **One orchestrator-remembered fact is off and corrected here**: the LCOE sequence values are right but the WI attribution shifts by one (Section E) — $251 is the pre-WI-019 baseline WI-019 *replaced*, not WI-019's output.

---

## (A) Measured-parity record — Anchor A

Source of record: `exploration/stellarator_e2e/HANDSHAKE_REPORT.md`, `exploration/stellarator_e2e/handshake_comparison.json`, `modeling_project/VALIDATION_MATRIX.md` (SV entries), and the WI-019 plan implementation record.

The handshake feeds the generated SysML forward model the exact 1 GWe point 1costingFE solved for (`CostModel(STELLARATOR, DT).forward(net_electric_mw=1000, …)`, the clean `examples/dt_stellarator.py` point), and compares per-account. Three tiers of test exist, and they matter for the tolerance spec:

| Tier | What it proves | Measured parity | Where |
|---|---|---|---|
| **Pipeline vs pure-Python oracle** | codegen + teax execution is faithful to the reproduced formulas | **bit-exact, rel 1e-9** | `run_stellaris.py` / `verify_stellaris.py`; HANDSHAKE_REPORT.md:18 |
| **Formula isolation** (SysML cost formula fed 1cfe's own p_th/p_et) | the reproduced formula equals 1cfe's formula | **~1e-8**; magnet −5.4e-10; worst **−7.63e-08** (structure) | HANDSHAKE_REPORT.md:52–66; comparison.json `iso_rel` |
| **End-to-end** (SysML computes power, then costs) | the whole chain reproduces 1cfe at 1cfe's point | power channels **≤6.3e-8** (SV-025); 12 power-scaled accounts **≤1.0e-7** (SV-026) | HANDSHAKE_REPORT.md:70–83; VALIDATION_MATRIX.md:51–52 |

Per-account end-to-end relative deviations (12 formula-reproduced accounts, `handshake_comparison.json` `rel_dev`):

| account | rel dev | note |
|---|---:|---|
| magnet (C220103) | −5.4e-10 | pure float64 path; residual = mu0 constant precision |
| heating (C220104) | 0 | fixed p_ecrh, exact |
| divertor (C220108) | −6.5e-9 | (p_th/1000)^0.5 |
| blanket (C220101) | +7.3e-8 | (p_th/2500)^0.6 |
| shield (C220102) | +7.3e-8 | (p_th/2500)^0.6 |
| structure (C220105) | −4.5e-8 | (p_et/1100)^0.5; formula-iso −7.63e-8 = worst |
| vessel (C220106_vessel) | +5.5e-8 | shell only; 1cfe adds 0.72 M$ gas-load pump sub-term |
| power_supplies (C220107) | +2.7e-8 | ARIES-CS-derived base — exclude/footnote in Anchor B |
| turbine (CAS23) | +9.0e-8 | linear in p_the |
| electric (CAS24) | +4.4e-8 | linear in p_et |
| heat_rejection (CAS26) | +1.0e-7 | linear in p_th — **worst end-to-end** |
| misc (CAS25) | +3.6e-8 | linear in p_et |

**Validation entries** (`modeling_project/VALIDATION_MATRIX.md`, both `passing`):
- **SV-025** (:51): power balance reproduces the 1cfe power table on formula isolation. Threshold **rel 1e-5** (note: "reference table is JAX float32, ~1e-7 floor"). Measured **≤6.3e-8**, worst p_th/p_the/p_et +6.23e-8 (WI-019 plan.md:161).
- **SV-026** (:52): every power-scaled account deviation shrinks from −8.6…−16.4% to ≤0.1%. Threshold **0.1%**. Measured **≤1.0e-7**, worst heat_rejection +1.0e-7 (WI-019 plan.md:162).
- **SV-028** (:55, WI-021): worst formula-isolation −7.63e-08 (structure), byte-identical to WI-020.

**Note on the WI-019 correction** (why the end-to-end tier only became meaningful at WI-019): before WI-019 the SysML power balance omitted the alpha term (547 MW, ~19% of p_th), so end-to-end accounts sat at −8.6…−16.4%. WI-019 collapsed 1cfe's physics.py steps 4–7 into `p_th = mn·p_neutron + p_alpha + p_input + eta_p·p_pump`, exact in the DEC-free non-radiation-limited regime, dropping all end-to-end deviations to the float floor (HANDSHAKE_REPORT.md:70–83, 117–119).

---

## (B) Float32 tolerance-floor evidence — Anchor A

**File**: `work/completed/20260718_WI-025_stale-basis-pass-through-recompute/design.md:40-50`.

The load-bearing finding for any per-account tolerance:

> "**1costingFE runtime precision**: the cost layers use `jnp` with jax's default **float32** (no x64 enable anywhere in the repo; `mirror.py` comments confirm float32 is intentional). The exactness proof below therefore records both the float64 evaluation (same 1cfe code, x64 flag — isolates grouping error) and the float32 runtime values." (design.md:40)

The exactness-proof table (design.md:44–50), both sides at the oracle's full-precision executed powers:

| account | forward form (f64) | 1cfe code @ f64 | 1cfe code @ f32 (runtime) |
|---|---|---|---|
| CAS21 buildings [$] | 640,475,006.1657383 | bit-identical | 640,474,975.59 (**−4.8e-8 rel**) |
| CAS10 subtotal [$] | 34,391,496.76962398 | 1 ulp (2e-16 rel) | 34,391,496.66 (3.2e-9 rel) |
| CAS70 O&M [$/yr] | 52,517,269.060942635 | bit-identical | no jnp in line |

**What this establishes for the spec:**
1. The SysML forward forms are **algebraically exact** against 1cfe's formulas (f64 vs f64 is bit-identical or 1 ulp). The only source of per-account disagreement is 1cfe's *own* float32 runtime rounding.
2. The floor is **~1e-7 relative** across the account set (worst measured −4.8e-8 at CAS21; the WI-019 power table worst +6.23e-8; heat_rejection end-to-end +1.0e-7). design.md:50: "the only deviations are 1cfe's own float32 runtime rounding, which the handshake's per-account comparisons already absorb for every other account."
3. The comparison discipline is: **pipeline-vs-oracle is checked at rel 1e-9 in float64, never pipeline-vs-1cfe-f32** (WI-025 plan.md:242). The handshake compares the SysML pipeline against 1cfe's f32 runtime output, which is why per-account tolerances land at ~1e-7, not 1e-9.

**Tolerance-basis implication (for the spec to propose, owner to ratify):** a per-account pass bar of roughly **1e-6 relative** would sit comfortably above the measured ~1e-7 float32 floor with headroom, while still being tight enough that any real modeling/mapping error (which shows up at percent-scale, per Section E) fails loudly. The measured record supports a floor no tighter than ~1e-7; anything tighter tests float32 noise, not the machinery.

---

## (C) Mapping-trap inventory — Anchor A

Complete inventory of documented 1costingFE→SysML mapping traps. "Handled" means the record shows the mapping asserted in code (not hoped). Two contexts recur: the **handshake** (1cfe's 1 GWe point: B=6.0/5.0 T, vessel_or=3.5 m) and the **Stellaris instance** (design point: B=9.0 T, r_coil=3.20 m). Sources: `exploration/stellarator_e2e/handshake_1costingfe.py`, `emit_1cfe_point.py`, HANDSHAKE_REPORT.md, WI-018 spec.md:76–86, and the per-WI records.

| # | Trap | Why it's a trap | Handled |
|---|---|---|---|
| a | **Fusion power is GIVEN** | 1cfe *outputs* p_fus; SysML would recompute it | solved `sigma_v` reproduces p_fus to rel 0 (`handshake_1costingfe.py:170-178`) |
| b | **`r_coil` = 1cfe `vessel_or`** | coil bore maps to radial-build vessel-outer radius, no "coil radius" field | since WI-021, **computed** by the radial-build calc fed 1cfe's build, not injected (`handshake_1costingfe.py:196-206,286`) |
| c | **radiation `B`=5 T vs coil-cost `b_center`=6 T** | two distinct fields; magnet *cost* takes b_center | emitted separately; `magnet__B := coil["b_center"]` (NOT radiation B) (`emit_1cfe_point.py:53`, `handshake_1costingfe.py:287`) |
| d | **Money unit ×1e6 (M$→$)** | 1cfe rolls up in M$, SysML in $; magnet cost_per_kAm is the exception (fed raw) | `M=1e6` on every coefficient except magnet cost_per_kAm (`handshake_1costingfe.py:153-168,229-301`) |
| e | **coil constants G/coil_markup/cost_per_kAm** | stellarator-path constants must come from 1cfe (G=8π²≈78.957, markup 5.87, REBCO 50 $/kA·m) | emitted + bound (`emit_1cfe_point.py:53-55`, `handshake_1costingfe.py:287-289`) |
| f | **`p_coils`→`p_tf`, `p_cool`→`p_tfcool`** | SysML splits TF/PF; 1cfe has single slots | full value → TF slot, 0 → PF (`handshake_1costingfe.py:216-217`) |
| g | **`f_shape` must be 1.0** | snapshot bakes the *instance* shape 0.7943; torus point shrinks 21% if not overridden (first re-run **failed −20.6%**) | explicit `geom__f_shape := 1.0` (`handshake_1costingfe.py:188-193`, WI-020) |
| h | **`eta_pin` effective, not raw** | raw parameter is wrong; effective 0.5 needed | `eta_pin_effective` emitted (`emit_1cfe_point.py:79`, bound :210) |
| i | **`fpcppf` — RESOLVED** | pumping-power *fraction* had no 1cfe counterpart | WI-019 replaced with 1cfe's absolute `p_pump` [MW]; trap gone (HANDSHAKE_REPORT.md:125) |
| j | **`p_cryo` chain-wired (WI-024)** | leaf became a computed channel | zero the heat inputs, feed 1cfe's p_cryo via additive `cryo_elec__p_direct`, IEEE-exact (`handshake_1costingfe.py:219-227`) |
| k | **`annual_om` chain-wired (WI-025)** | leaf became a computed channel | `om_cost__om_ref=0` + `om_cost__om_direct=<1cfe O&M>` ×1e6; `0·(…)+v=v` exact (`handshake_1costingfe.py:242-301`) |
| l | **contingency rate 0 (NOAK)** | model/instance default is 0.10 | fed 0 to match the NOAK point, footnoted (`handshake_1costingfe.py:236-239`) |
| m | **vessel = C220106 shell only** | 1cfe C220106 adds 0.72 M$ gas-load pump | documented simplification, not fed (HANDSHAKE_REPORT.md:59,121) |
| n | **BOP name→CAS remap** | non-sequential: heat_rejection→cas26, misc→cas25 | remap table (`handshake_1costingfe.py:96-98`) |

Also: `rb__*` vs `geom__*` **separation** (WI-021) — codegen emits per-calc-input params, so the radial-build inputs (`rb__a/kappa/R/*_t`) are distinct keys from the plasma-path `geom__*`; the handshake overrides only `geom__*` so `rb` keeps the real geometry (WI-021 design.md:62-64).

**Spec implication:** the tolerance spec should require each mapping in this table to be **asserted in the handshake** (as most already are), not assumed. The `f_shape` trap (g) is the cautionary tale — a "default is automatic" assumption was wrong and produced a −20.6% failure until the injection was made explicit.

**Errata that touched the design point but NOT the handshake** (injected from 1cfe's refs, so Anchor A is unaffected by construction): B 5.86→9.0 T (WI-023, a phantom Table-3 text row), p_tf 111→0.0 (stored magnetic energy in GJ, not a power), recirc/cryo derivation (WI-024). Each was zero-edit on the handshake because `magnet__B`, `pb__p_tf`, `pb__p_cryo` are injected from 1cfe's own values.

---

## (D) Injected-value inventory — the gap boundary (Anchor A)

This is the boundary the criterion-3 ruling governs. The handshake reproduces the 12 formula-reproduced accounts (Section A) under tolerance. Everything below is currently **filled by injecting 1cfe's own value** or **structurally absent** — the −31% LCOE gap. Source: HANDSHAKE_REPORT.md:86–124, `handshake_comparison.json`.

**Pass-through accounts (injected → "not a real test" of the machinery):**
| account | 1cfe value | status |
|---|---:|---|
| buildings (CAS21) | $619.4 M | injected in handshake; **but forward-computed in the instance** (WI-025) |
| preconstruction (CAS10) | $18.5 M | injected in handshake; forward-computed in instance (WI-025) |
| special_materials (CAS27) | $20.8 M | injected in handshake |

*Nuance for the spec:* in the *handshake* these are injected (tautological), but the *instance model* now forward-computes CAS21/CAS10/CAS70 from powers (WI-025). So "injected in the handshake" ≠ "unmodeled" for these three.

**CAS22 tail — unmodeled, ~$1.094B at the 1 GWe point** (HANDSHAKE_REPORT.md:109; `cas22_gap_musd` = 1094.03 M$):
| line | M$ |
|---|---:|
| C220110 remote handling | 151.9 |
| C220111 installation labor | 509.6 |
| C220200 coolant | 202.0 |
| C220300 aux cooling + cryoplant | 18.9 |
| C220400 waste | 5.5 |
| C220500 fuel handling | 120.0 |
| C220600 other | 11.5 |
| C220700 I&C | 73.8 |
| (C220106 vessel gas-load pump sub-term) | 0.72 |

**Above CAS22 — unmodeled:**
| account | M$ |
|---|---:|
| CAS40 owner | 41.2 |
| CAS50 supplementary | 578.6 |
| CAS60 IDC | 2224 |

**LCOE construction differs structurally** (HANDSHAKE_REPORT.md:110–113):
- 1cfe: `LCOE = (CAS90 + CAS70 + CAS80)·1e6 / (8760·p_net·avail)`, CAS90 = CRF·total_capital, CAS70 = inflation-levelized O&M annuity, CAS80 = fuel.
- SysML: `LCOE = (total_capital·idc_factor·CRF + annual_om) / (8760·p_net·avail)` — single CRF·IDC on total capital, flat O&M, **no fuel term, no CAS70 levelization**.

**Rollup gap** (`handshake_comparison.json` `rollup`): total capital 1cfe $10.096B vs SysML $5.865B (−41.9%); LCOE 1cfe $123.74 vs SysML $85.55 (**−30.87%**). HANDSHAKE_REPORT.md:113 states this −31% is "the true structural distance, and it is the measured target for the Stage-3 account-scope items."

**The gap boundary the spec must draw** (per [OWNER] criterion-3 ruling 2026-07-18):
- **Must come under tolerance after Items 3–4**: CAS22 tail + CAS40/50/60 (Item 3), CAS70 levelization + CAS80 fuel + IDC treatment (Item 4) — these get forward-computed and sourced.
- **Itemized-and-explained remainder**: whatever 1cfe carries that the model legitimately does not (documented simplifications like the vessel gas-load pump sub-term), or 1cfe quirks filed as findings ([OWNER] non-goal: no changes to 1cfe). Full closure is **not** required; errors are closed, remainder is explained.

---

## (E) Model-side sensitivity record — admissible Anchor-B evidence

This is the strongest admissible basis for "what agreement is even achievable blind": how far **our own** headline moved under corrections, before any ARIES-CS contact. Source: WI-019→025 plan implementation records.

**Headline LCOE across the WI-019→025 run** (each an executed, oracle-bit-exact value):

| Stage | LCOE $/MWh | p_net MW | q_eng | total $B | magnet ($B / %) | correction |
|---|---:|---:|---:|---:|---|---|
| WI-018 baseline (pre-019) | **250.95** | 575.3 | — | — | — | stale starting headline |
| WI-019 | **189.13** | 786.1 | 3.87 | 10.086 | 4.392 / 43.5% | faithful power balance (alpha term) |
| WI-020 | **247.34** | 578.0 | 3.16 | 9.683 | 4.392 / 45.4% | geometry: V 564→448 via f_shape |
| WI-021 | **247.34** | — | — | 9.683 | 4.392 / 45.4% | radial build (no-op, Option 1) |
| WI-022 | **176.07** | 804.1 | 3.93 | 9.586 | 4.117 / 42.9% | profile-integrated confinement |
| WI-023 | **201.458** | 915.1 | 6.609 | 12.602 | 6.3235 / 50.18% | B 5.86→9.0 T + p_tf 111→0 |
| WI-024 | **201.472** | 915.081 | 6.6067 | 12.602 | 6.3235 / 50.2% | recirc/cryo derivation |
| WI-025 | **203.647** | 915.081 | 6.6067 | 12.639 | 6.3235 / 50.03% | account recompute (forward from powers) |

Confirmed against `run_stellaris.py:248-262` (current headline: LCOE 203.647, total $12.64B, p_net 915.081, q_eng 6.607, magnet $6.32B). Intermediate at WI-023: the B-only move (p_tf still 111) gave **$229.27**; zeroing p_tf brought it to $201.46 (WI-023 design.md:40-43).

**Correction to the orchestrator's remembered sequence** ("$251→$189→$247→$176→$201→$204 across WI-019→025"): the six *values* are right as distinct levels, but the attribution is off:
- **$251 is the pre-WI-019 (WI-018) baseline, the headline WI-019 *replaced*** — not WI-019's output ($189.13).
- **WI-021 is a no-op** (LCOE stayed $247.34), so $247 spans WI-020 and WI-021.
- **"$201" collapses WI-023 ($201.458) and WI-024 ($201.472)** — the cryo derivation moved it only +$0.014.
- **"$204" is $203.647** (WI-025), not 204.

**What this supports for Anchor B:** the LCOE range under our own corrections was **~$176–$251, roughly ±25–30% about the ~$200 center** — and magnet cost/share swung from $4.39B/43.5% to $6.32B/50% on a single field-value errata. The p_net stale-basis history alone re-staled five times: 575.3 → 786.1 → 578.0 → 804.1 → 915.1 (WI-025 brief, `work/orchestration/stale-basis-recompute.md:20`). This is direct, model-side evidence that even our *own* headline is only stable to tens of percent under legitimate modeling corrections — so a blind hold-out comparison cannot reasonably be held to better than that. It argues for **order-of-magnitude-to-factor-of-2 bands on derived quantities and rough costs**, not percent-level agreement.

---

## (F) Admissible expectation-calibration bases — Anchor B

The hold-out has **no admissible ARIES-CS-side ground truth** — that is the design. General estimating-accuracy conventions are the only external calibration, and one is admissibly sourced in-repo.

**AACE International estimate classes** — arXiv 2602.19389 ("Extension of the Fusion Power Plant Costing Standard," CATF IWG / pyFECONS methodology paper), Table 3, at `knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/arxiv-2602-19389/output.md:1318-1328` (identical copy under `07-maglif/iter-03/`). **Confirmed admissible** — not ARIES-CS-specific, not on any barred list, cites AACE as an external standard it plans to adopt.

| Class | Maturity | Purpose | Accuracy (low / high, 80% confidence) |
|---|---|---|---|
| **Class 5** | 0–2% | Screening / feasibility | **−30% to −50% / +30% to +100%** |
| Class 4 | 1–15% | Concept screening | −15% to −30% / +20% to +50% |
| Class 3 | 10–40% | Budget authorization | −10% to −20% / +10% to +30% |
| Class 2 | 30–75% | Control / bid | −5% to −15% / +5% to +20% |
| Class 1 | 65–100% | Check estimate | −3% to −10% / +3% to +15% |

Class 5 note (output.md:1328): "Class 5 ranges are often highly asymmetric and can be wider depending on novelty, scope ambiguity, and data limitations." The "accuracy range" is defined as the 80%-confidence interval — the project cone of uncertainty (output.md:1314).

Second, weaker hit: `knowledge/sources/COST_MODELING.md:411` names "AACE Class 4-5 estimates" for system-level cost data but gives **no** accuracy numbers.

**What this supports:** the stellarator model is a **conceptual-stage estimate — AACE Class 5 (or optimistically Class 4)**. The admissible band for rough per-component cost agreement is therefore roughly **−30%/−50% to +30%/+100%** (Class 5), i.e. "within a factor of ~2, asymmetric high." This is *general* estimating knowledge applied to our own estimate's maturity — it says nothing about where ARIES-CS lands, only about how wide a concept-stage estimate's own uncertainty is. Combined with Section E (our own headline moves ±25–30% under corrections), a **factor-of-2 band on component costs and a same-order-of-magnitude band on derived quantities** is the defensible pre-committed expectation to propose.

**Provenance caveat for the spec** (agent finding): the AACE table is an in-repo *dossier extraction* (pandoc from arXiv HTML), not a `SOURCE_INDEX.md`-registered primary source. The numbers match published AACE 18R-97 values, but if they become load-bearing the spec should cross-check against the raw arXiv PDF per the project's extraction-fidelity practice, and cite AACE as the general standard with this file as where it is written down in-repo.

---

## (G) Gaps and unknowns the spec stage must flag (not paper over)

1. **Anchor-B derived-quantity values do not exist yet.** The axes (structural similarity; radial-build consequences, coil mass, power flows at the ARIES-CS design point; rough per-component costs) require *evaluating the model at the ARIES-CS geometry* — that is Item 7, post-reveal. So the spec must set expectations as **band widths** (e.g. "coil mass within a factor of 2," "power flows same order of magnitude"), not point targets, because the model output at that point is unknown pre-reveal and the reference is sealed.

2. **The C220107 exclusion is mandatory for Anchor B.** power_supplies (C220107) is the one known ARIES-CS-derived 1cfe value (HANDSHAKE_REPORT.md:140; PROTOCOL §3 admissible list; concept "Why This Shape"). It must be **excluded or footnoted** in the hold-out comparison so the blind isn't self-referential. It stays *included* in Anchor A (the handshake is not the blind).

3. **Sizing axis is NOT criterion 4.** The owner's three axes were structure / optimized sizing / component cost, but sizing "cannot be tested at a fixed design point (sizing is an input there)" — reallocated to stretch criterion 8, marked **[SURFACED to owner]** in the concept (criterion 4 note). The spec must not write a criterion-4 sizing expectation; it belongs to Item 9.

4. **Per-account tolerance floor is float32 (~1e-7), not bit-exact.** Section B: the spec must set the Anchor-A per-account bar above the ~1e-7 float32 floor (≈1e-6 relative proposed, owner ratifies). Asking for tighter tests float32 noise. The pipeline-vs-oracle 1e-9 bar is a *different* test (f64) and is already met — don't conflate the two in the spec.

5. **The −31% gap boundary needs the spec to name it account-by-account.** Section D lists which accounts Items 3–4 must bring under tolerance vs the itemized-and-explained remainder. The spec must word Items 3–4's acceptance in the [OWNER] criterion-3 terms (explain what remains; close errors; full closure not required) — and should note that CAS21/CAS10/CAS70 are already forward-computed in the *instance* even though injected in the *handshake*.

6. **Commit-pin change procedure is undocumented.** The pin `0254385` is asserted in code (`handshake_1costingfe.py:115` asserts emitter output == live repo HEAD; hardcoded at `emit_1cfe_point.py:22`), but no record states how the pin is chosen or what to do when 1costingFE advances (the assert simply aborts with "commit drift"). The spec should make "record the commit and document the bump procedure" an explicit Anchor-A requirement (the concept already requires recording the commit; the *procedure* is the gap).

7. **The demo package does not yet execute constraints** (criterion 2, Item 2) — orthogonal to Item 1's bars, but the Anchor-A handshake and the constraint-verdict machinery are separate; the spec for Item 1 should not assume verdicts exist in the run report yet.

8. **Two absolute constraints inherited by every downstream handshake edit** (from `work/orchestration/stale-basis-recompute.md:24`, [OWNER] WI-024 successor bar): `handshake_1costingfe.py` may be edited **only within `set_1cfe_inputs`'s injection map** (no comparison-logic change), and `git diff exploration/stellarator_e2e/handshake_comparison.json` must be **empty** after a run. Items 3–4 change this (they add real modeled accounts, so the comparison JSON *will* move) — the spec must explicitly retire or amend this bar for Items 3–4, or those items violate a standing [OWNER] rule. **This is a premise conflict the spec must surface to the owner, not resolve silently.**

---

## Code References

- `exploration/stellarator_e2e/HANDSHAKE_REPORT.md` — the Anchor-A record (parity tables, gap itemization, mapping traps, C220107 footnote)
- `exploration/stellarator_e2e/handshake_comparison.json` — machine-readable per-account comparison + rollup + `cas22_gap_musd`
- `exploration/stellarator_e2e/handshake_1costingfe.py:105-117` — commit-pin assertion; `:153-301` — injection map (the only editable region per the successor bar)
- `exploration/stellarator_e2e/emit_1cfe_point.py:22` — hardcoded pin `0254385`; `:39,53,79` — separated-field / effective-eta emissions
- `exploration/stellarator_e2e/run_stellaris.py:248-262` — current executed headline
- `modeling_project/VALIDATION_MATRIX.md:51-55` — SV-025/026/028
- `work/completed/20260718_WI-025_.../design.md:40-50` — float32 finding + exactness proof
- `work/completed/20260714_WI-019_.../plan.md:161-169` — SV measurements + LCOE re-baseline start
- `work/completed/20260717_WI-020_.../plan.md:70-74`; `WI-021/plan.md:82-86`; `WI-022/plan.md:88`; `WI-023/plan.md:218` + design.md:40-43; `WI-024/plan.md:252`; `WI-025/plan.md:259` — the re-baseline sequence
- `work/orchestration/stale-basis-recompute.md:20,24` — p_net re-staling history; the [OWNER] successor bar
- `knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/arxiv-2602-19389/output.md:1314-1328` — AACE estimate classes (admissible)
- `knowledge/sources/COST_MODELING.md:411` — AACE classes named, no numbers

## Feasibility Assessment

Both anchors' bars are writable now with the evidence in hand:
- **Anchor A** is well-grounded — the tolerance number is bounded below by the measured float32 floor (~1e-7) and above by where real errors appear (percent-scale, Section E). The gap boundary is itemized (Section D). The only spec-authoring risk is the premise conflict in G-8 (the standing "comparison JSON must not move" bar collides with Items 3–4 adding real accounts) — surface to owner.
- **Anchor B** is grounded only by model-side sensitivity (E) and general estimating classes (F), which is exactly the admissible envelope. Expectations must be band-shaped (order-of-magnitude on derived quantities, factor-of-2 / AACE-Class-5 on rough costs), pre-committed, per-axis, with the sizing axis excluded (criterion 8) and C220107 excluded. No in-repo ARIES-CS ground truth exists to tighten these — and by the prior-leak bar, none may be sought.

## Open Questions (for the owner-ratified spec)

- **Anchor-A per-account and LCOE pass numbers** (concept OQ 1): proposed basis is ~1e-6 per formula-reproduced account (above the ~1e-7 float32 floor); LCOE bar worded per the criterion-3 ruling (explain remainder, close errors). Owner ratifies.
- **Anchor-B per-axis bands** (concept OQ 2): proposed basis is order-of-magnitude on derived quantities, factor-of-2 (AACE Class 5) on rough per-component costs, structural similarity as a qualitative checklist. Owner ratifies the exact bands.
- **The G-8 premise conflict**: does the WI-024 successor bar ("comparison JSON diff empty") get amended for Items 3–4, and how? Owner decision.
