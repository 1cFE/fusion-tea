---
Status: complete
Created: 2026-07-18
Updated: '2026-07-18'
Related Artifacts:
  Spec: ./spec.md
  Alignment Brief: ../../orchestration/stale-basis-recompute.md
---

> Process note: the post-spec owner checkpoint PASSED (spec §Checkpoint Rulings, all three confirmed 2026-07-18); mechanism — CAS21 representation, placement, computation route — was delegated to this design per the standing outcomes-at-spec ruling. **No escalation triggered: the ruling-3 handshake re-derivation (D6) concludes the structure forces edits only inside `set_1cfe_inputs`'s injection map — the rollup glue at :369-371 is untouched.** All structural claims below are spike-proven (syside L1–L6 on a canonical scratch tree, snapshot + V11 bridge on a staged scratch tree — no repo file touched, no repo regen run).

# WI-025 Design: STALE-BASIS Pass-Through Recompute

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — demo model-development session; §3 barred paths not read. This item's admissible source set is 1costingFE only (`/home/reid/1cfe/1costingfe`, pin `0254385` verified clean this session); all formulas and constants re-read from `costs.py` / `costing_constants.yaml` at design.

## Overview

Three new library calc defs in `models/library/analyses/mfe_account_costs.sysml` — `'Buildings Cost'` (CAS21), `'Preconstruction Cost'` (CAS10), `'Annual OM Cost'` (CAS70) — replace the three stale literals with forward computations of the model's own powers:

```
CAS21 = fixed_base + fus_base·(p_fus·n_mod/2300) + staff_base·(p_et·n_mod/1100)^0.5
        + the_base·(p_the·n_mod/1100) + th_base·(p_th·n_mod/2500) + et_base·(p_et·n_mod/1100)
CAS10 = land_intensity·(p_net·n_mod·1000)^0.5·land_cost + fixed_precon          [pre-contingency subtotal]
CAS70 = om_ref·(p_net·n_mod/1000)^alpha + om_direct                             [unlevelized $/yr]
```

The generic plant (`mfe_plant.sysml`) gains three calc usages and eight concept-input attributes; the Stellaris instance binds the eight values (all M$→$ conversions of pinned 1costingFE constants, DT/FOAK/n_mod = 1 frozen as documented constants). The three STALE BASIS annotations retire.

Proven this session: parse/validate clean with the canonical L2–L6 offender list **exactly the 6 pre-existing** (content-identical, line-shifted); snapshot classifies all power feeds as chains and the three modules FULLY_COMPILABLE (auto-codegen, no handwritten stubs); V11 bridge reports **exactly 3 offenders** (the known rollup keys); the 1costingFE-side evaluation at the executed powers agrees with the forward forms (bit-identical for CAS21 and CAS70 at float64, 1 ulp for CAS10 — table below).

Expected headline (oracle-rollup-exact at the executed powers; actual recorded at implement, never fitted): CAS21 $640,475,006.17, CAS10 $34,391,496.77, CAS70 $52,517,269.06/yr → total **$12,638,857,665.74** (+$37.34M, +0.296%), LCOE **$203.647152/MWh** (+$2.1751), magnet share 50.03%. p_net 915.081088, q_eng 6.606662, rec_frac 0.151362, magnet capital — all unchanged (costs do not feed the power balance; denominator does not move).

## Research Findings

**Formula re-verification (this session, pin `0254385`):**

- `costs.py:83-144` (`cas21_buildings`): 18-building loop, each building linear in exactly one scaling basis via `scale_map` (:121-130). Refs: p_et/p_the ref = `ref_gross_power_mwe` 1100 (yaml:12), p_th ref 2500 and p_fus ref 2300 hardcoded (:105-106). `p_the = p_et` for a no-DEC plant (:104). Cryogenics building (14 M$, yaml:195) is SC-gated (:137) — applies (REBCO HTS). Returned **raw** (:86-88, CAS29 applies contingency once). Grouped base-cost sums re-derived from yaml:175-197 (DT column): fixed **168.5** = site_improvements 85 (:177) + fuel_storage 9 (:183) + control_room 14 (:184) + security 3.5 (:185) + maintenance 17 (:188) + site_services 5 (:189) + cryogenics 14 (:195) + assembly_hall 21 (:197); p_fus **288** = reactor_building 138 (:179) + hot_cell 104 (:180) + reactor_auxiliaries 29 (:181) + ventilation_hvac 17 (:186); staff **9** = administration (:187); p_the **58** = turbine_building (:191); p_th **26** = heat_exchanger 17 (:192) + service_water 9 (:196); p_et **29** = power_supply 17 (:193) + onsite_ac 12 (:194). Matches the spec Evidence sums exactly.
- `costs.py:52-80` (`cas10_preconstruction`): land = `land_intensity·sqrt(p_net·n_mod·ref_net)·land_cost` (0.25 acres/MWe yaml:21, $10000/acre yaml:22, ref 1000 yaml:8) + six adders: site_permits 3 (:15) + licensing_cost_dt 5 (:23) + plant_permits 2 (:18) + plant_studies_foak 20 (:16) + plant_reports 1 (:19) + other_precon 1 (:20) = **32 M$**. Contingency added at :79 — deliberately not carried (the model's CAS29 applies contingency once over the direct sum; convention preserved, MR-WI025-3).
- `costs.py:353` (`cas70_om` annual line): `om_cost(fuel)·(p_net·n_mod/ref_net)^0.5`; `om_cost_dt` 54.9 M$/yr (yaml:272). CAS71 levelization / CAS72 replacement not carried (documented Stage-3 refinements; convention preserved).
- **1costingFE runtime precision**: the cost layers use `jnp` with jax's default **float32** (no x64 enable anywhere in the repo; `mirror.py` comments confirm float32 is intentional). The exactness proof below therefore records both the float64 evaluation (same 1cfe code, x64 flag — isolates grouping error) and the float32 runtime values.

**Exactness proof (MR-WI025-2) — executed this session.** Both sides evaluated at the oracle's full-precision executed powers (p_fus 2748.0568768605704, p_th 3238.1209233754694, p_the = p_et 1078.2942674840313, p_net 915.0810878595104; unmodified oracle first reproduced the WI-024 baseline). 1cfe side ran the pinned repo's own functions (`cas21_buildings`, the `cas10_preconstruction` internals, the `costs.py:353` expression with `cc.om_cost(Fuel.DT)`) in its own uv environment, read-only:

| account | forward form (design, f64) | 1cfe own code @ f64 | agreement | 1cfe own code @ f32 (runtime) |
|---|---|---|---|---|
| CAS21 buildings [$] | 640,475,006.1657383 | 640,475,006.1657383 | **bit-identical** | 640,474,975.59 (−4.8e-8 rel, f32 rounding) |
| CAS10 subtotal [$] | 34,391,496.76962398 | 34,391,496.76962399 | 1 ulp (2e-16 rel, association order) | 34,391,496.66 (3.2e-9 rel) |
| CAS70 annual O&M [$/yr] | 52,517,269.060942635 | 52,517,269.060942635 | **bit-identical** | 52,517,269.06 (no jnp in the line) |

Cross-check: 1cfe's full `cas10_preconstruction` at f64 returned 37,830,646.45 = subtotal × 1.10 exactly (`contingency_rate(noak=False)` = 0.10), confirming the bound value is the contingency-free subtotal. The grouping is not a fit: at float64 the 6-term collapse reproduces the 18-term loop **bit for bit** at this point; the only deviations are 1cfe's own float32 runtime rounding, which the handshake's per-account comparisons already absorb for every other account.

**Snapshot/codegen mechanics (spiked on a scratch copy of the staged tree, sysml-codegen HEAD `6db3212` verified):**

- All three calc defs classify FULLY_COMPILABLE — pure `+ - * / **` arithmetic, auto-implemented (`AUTO_IMPLEMENTED = True` in all three generated impls); `IMPLEMENTATION_BACKLOG.md` still lists exactly 1 function (DT_Fusion_Power).
- Power feeds wire as **chains with no new glue**: `buildings_cost` p_et/p_the/p_th bind self-named to the plant aliases and the emitted pipeline wires them straight to `pb__p_et/p_the/p_th` channels (unlike the BOP `in power = p_the` mismatch that needs glue-1); `p_fus` wires to `fusion__p_fus.root`; `p_net` (precon, om) wires to `pb__p_net`.
- The attribute-mediated output chain works: `attribute annual_om : Real = om_cost.annual_om` + the untouched `lcoe_calc { in annual_om = annual_om; }` classifies as **chain**, and the emitted pipeline wires `lcoe_calc.annual_om ← om_cost__annual_om.root`. The settable leaf `lcoe_calc__annual_om` disappears (basis for D6).
- Generated-inputs key diff vs committed: `system_design.json` **+8** (6 `buildings_cost__*_base` at the $ values, `precon_cost__fixed_precon`, `om_cost__om_ref`), **−4** (`lcoe_calc__annual_om` designed-out; the 3 `mfe_plant__MFE_Power_Plant__p_th/p_the/p_et` glue fields are the known post-run regen-reset, re-added by runner glue — WI-023/024 record). `mfe_plant_params.json` **+13** defaulted-input leaves (refs, land constants, `om_cost__alpha`, `om_cost__om_direct`, per-calc `n_mod`), −0.
- V11 bridge: **exactly 3 offenders** (contingency `direct_subtotal`, indirect `direct_cost`, lcoe `total_capital` — the known rollup keys), bridged, package emitted. The two new computed attributes (`preconstruction_capital`, `annual_om`) do not become offenders.

**Validation baseline (canonical 22-file set, this session):** the repo baseline reproduces the recorded 6 offenders exactly (`mfe_plant.sysml:353/359/364`, `ife_plant.sysml:33/41`, `hif_plant.sysml:205`). The prototype on a canonical scratch tree yields **exactly the same 6**, content-identical, line-shifted (:353→389, :359→395, :364→400 — the WI-024 shift precedent). Level profile identical (L2: 3 pre-existing; L1/L3/L4/L5 pass).

**Known quirk, documented so implement doesn't chase it:** validating the *staged e2e subset* alone (not the gate) reports a different pre-existing error set (5, including spurious "no value or binding" on abstract-plant attributes); under the prototype the `preconstruction_capital` entry re-classes to an ADR-002 Rule-3 message (count unchanged, 5→5). This is a subset-analysis artifact — the MR-WI025-5 bar runs `validate models --complete` on the canonical set, where the offender list is exactly the 6.

**Consumers traced (grep-verified complete, matching the spec):** model + staged twin (three regions), oracle `verify_stellaris.py` (:102-108 constants, :195-210 rollup), runner `run_stellaris.py` (BUILDINGS/PRECON :93-94 → glue-2 :193; headline asserts :246-262; CAS table :281-283), `generated/inputs/system_design.json` (`lcoe_calc__annual_om`), handshake `handshake_1costingfe.py` (:243 injection; :369-371 glue reads 1cfe's own `costs_musd`, outside the injection map; :422-426 tautological pass-through rows). Nothing else reads the three accounts.

## Design Decisions

**D1 — CAS21 representation: grouped 6-term exact collapse, per-building table carried in the binding docs.** The 18-building loop collapses algebraically exactly because every building is linear in exactly one scaling basis — and the proof above shows the collapse is *bit-identical* to 1cfe's own loop at float64 at the executed point. Six concept inputs (base-cost sums, $) keep the leaf surface small, fit the codegen envelope trivially, and regenerate cleanly; MR-4 traceability is carried by the instance binding docs, each listing its member buildings with yaml line cites and the addition spelled out (the WI-024 `vol_cold` COMPUTED-doc pattern). Rejected: 18 per-building attributes — 3× the leaf surface, a scaling-basis selector per building (lookup, outside the envelope, or 18 redundant single-term calcs), no analytic gain at frozen DT; point-recompute literal — settled forward ruling, would re-stale (spec, do not reopen).

**D2 — placement: three library calc defs appended to `mfe_account_costs.sysml`; wiring in the generic plant; values in the instance.** That file's charter is exactly this ("concept-agnostic steady-state CAS account cost scalings reproducing 1costingFE per-account functions"); AD-004/AD-007 route reusable definitions to the library, and MR-3 holds because every fuel/FOAK-keyed number (base sums, licensing-bearing fixed adders, om_ref) is an undefaulted concept input bound by the instance, while calibration constants (refs 1100/2500/2300/1000, land 0.25/$10000, alpha 0.5) are defaulted inputs carrying their 1costingFE citations — the established `'Blanket Cost'` pattern. Rejected: instance-local static expressions (WI-021 CAS27 precedent) — ADR-002 forbids instance expressions on calc outputs (powers), and CAS27's expression is snapshot-baked, not pipeline-executed — these three accounts should execute as modules; a new library file — no charter reason, mfe_account_costs is their home (WI-024's new file was an analysis chain, not an account cost).

**D3 — power feeds: self-named alias bindings for p_et/p_the/p_th, dotted for p_fus and p_net; n_mod and calibration refs left as defaulted calc inputs, not plant-bound.** `in p_th = p_th` is the proven blanket_cost idiom and spike-wires directly to the pb channels with zero new glue (the BOP `in power = p_the` name-mismatch trap avoided); `in p_fus = fusion.p_fus` mirrors the wall_load binding, `in p_net = pb.p_net` mirrors lcoe_calc — both proven dotted chains. n_mod is frozen at 1 (spec ruling) and left as a per-calc defaulted input rather than bound to the plant's `n_mod` attribute: binding it would add dangling-schema coverage surface (the BOP n_mod pattern) for zero modeled benefit at n_mod = 1; the freeze is documented at the bindings. Honest cost, stated: a future multi-module concept must set three more leaves or rewire. Rejected: `in n_mod = n_mod` for symmetry with BOP — new dangling-field surface; dotted pb.* for all powers — works, but the alias idiom is the file's convention and spike-proven.

**D4 — output routing: buildings keeps its part (`:>> capital_cost = buildings_cost.cost`, the turbine idiom); `preconstruction_capital` and `annual_om` become generic-plant attributes bound to calc outputs; `lcoe_calc`'s `in annual_om = annual_om` is untouched.** The attribute-mediated chain is spike-proven (snapshot: chain; pipeline: `om_cost__annual_om.root`). `direct_capital`'s expression text is unchanged — the offender lines stay content-identical, only line-shifted. Rejected: rebinding lcoe_calc dotted to `om_cost.annual_om` (unnecessary — chain proven, and it would churn a proven block); deleting the pass-through attributes and referencing calc outputs inside `direct_capital` (changes the tracked offender line's content).

**D5 — `om_direct` additive direct term on `'Annual OM Cost'` (default 0.0).** Dual purpose: a genuine modeling affordance (a 0D concept that knows its O&M outright binds om_direct and zeroes om_ref — the WI-024 `p_direct` pattern, no conditional, so the calc stays auto-codegen), and the handshake identity path (D6). At the Stellaris point om_direct = 0.0 and the formula is exactly costs.py:353. Zero-term addition is IEEE-exact, so MR-WI025-2 exactness is unaffected. CAS21/CAS10 get no direct terms — their channels are unconsumed in the handshake (D6), so an affordance there would be unneeded structure (capture-fidelity: no accretion). Rejected: identity via ref_net_power injection to force the scale factor to 1 — requires bit-exact p_net reproduction as an assumption instead of an IEEE identity.

**D6 — handshake safety, re-derived for this structure (spec ruling 3) — SAFE WITHIN THE BAR, escalation not triggered.** Channel-by-channel trace:
- **annual_om**: the settable leaf `lcoe_calc__annual_om` disappears (spike-verified), so the injection at :243 *must* move — the forced edit, and it lands inside `set_1cfe_inputs`: replace `f"{P}lcoe_calc__annual_om": refs["annual_om_unlevelized_musd"] * M` with `f"{P}om_cost__om_ref": 0.0` (sd block) and `f"{P}om_cost__om_direct": refs["annual_om_unlevelized_musd"] * M` (mp block; defaulted-input keys are settable there — the blanket_cost__alpha precedent). The chain computes `0.0·(p_net/1000)^0.5 + v = v` — exact in IEEE arithmetic (0·finite = 0, 0 + v = v; WI-024 D7's executed identity precedent), so lcoe receives 1cfe's annual_om bit-for-bit and every downstream float matches the record.
- **buildings / preconstruction**: the new `buildings_cost__cost` / `precon_cost__cost` channels compute during the handshake passes but are **consumed by nothing there**: the rollup glue at :369-371 keeps feeding 1cfe's own `costs_musd["cas21"/"cas10"]` Python-side into `direct`, and the pass-through rows (:422-426) keep comparing 1cfe's values against themselves — still correctly labeled "tautological — fed 1cfe values". No glue edit is forced; the new base-sum leaves carry their baked instance values (which *are* 1cfe's DT constants) and are irrelevant to the report.
- **Report fields**: `handshake_comparison.json` records no injected key names and none of its row sources change → byte-identical, `git diff` empty. Bar: edits only within the injection map ✓, no comparison-logic change ✓. (Noted for a future item, not this one: the two now-computable accounts could graduate from tautological pass-through rows to real comparisons — that is a comparison-logic change and stays out of WI-025.)

**D7 — re-baselining surface (MR-WI025-4).** Oracle: drop `buildings_capital`/`preconstruction_capital`/`annual_om` from `IN`; add the eight concept inputs (+ `bldg_p_fus_ref` 2300, land/ref/alpha/om_direct defaults; p_th_ref 2500 and p_et_ref 1100 already exist in IN and are reused); compute the three accounts mirroring the generated statement forms verbatim (recorded in Research Findings — the design forward forms are already association-identical). Runner: CH gains `buildings`/`precon`/`annual_om` channels; delete the BUILDINGS/PRECON harness constants; glue-2 becomes `direct = powercore + bop + a[CH["buildings"]] + a[CH["precon"]] + SPECIAL` (the SPECIAL-harvest precedent); per-channel bit-exact checks for all three; headline comment rewritten for WI-025 and asserts retargeted (total ≈ 12.64 $B, LCOE ≈ 203.6 $/MWh, others unchanged); CAS-table rows read the channels and drop the "(pass-thru)" labels for 21/10. Regen: unfiltered snapshot + bridge (expectations above; WI-022 impl sha256 `8d2357…794a9f` content-check). Matrix: SV-032 records the executed headline (three accounts, direct/total, LCOE); SV-030/031 stand as historical records (checkpoint ruling 2). Docs: each account's doc states which powers it tracks and the preserved convention; STALE BASIS retired; instance headline block re-baselined at implement with a WI-025 history line. Staged twins mirrored per-edit-region (all three edit anchors are twin-identical — proven: the same patches applied byte-identically to both trees this session).

## Proposed Design

### 1. Library calc defs (append to `models/library/analyses/mfe_account_costs.sysml`; staged twin identical)

```sysml
calc def 'Buildings Cost' {
    doc /*
    CAS21 buildings total, raw (pre-contingency; CAS29 applies contingency
    once over the direct sum). Exact 6-term grouped collapse of the
    1costingFE 18-building loop (WI-025): every building is linear in
    exactly one scaling basis, so the loop groups into base-cost sums per
    basis. Grouping is exact linear algebra, not a fit (design-stage proof:
    bit-identical to the pinned loop at float64 at the executed powers).
    p_the = p_et for a no-DEC plant (costs.py:104) — documented where the
    instance binds. Base sums are concept inputs (fuel-keyed, MR-3);
    reference powers are 1cfe calibration constants.
      cost = fixed_base + fus_base*(p_fus*n_mod/p_fus_ref)
           + staff_base*(p_et*n_mod/p_et_ref)**0.5
           + the_base*(p_the*n_mod/p_the_ref)
           + th_base*(p_th*n_mod/p_th_ref) + et_base*(p_et*n_mod/p_et_ref)
    **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
    **Ref**: costs.py:83-144 (cas21_buildings; scale_map :121-130, refs
        :102-106, SC cryogenics gate :137); costing_constants.yaml:175-197
    **Basis**: exact linear grouping of the per-building loop (WI-025 D1)
    */

    in attribute fixed_base : Real;   // sum of fixed-basis base costs [$]
    in attribute fus_base : Real;     // sum of p_fus-scaled base costs [$]
    in attribute staff_base : Real;   // sum of staff-scaled base costs [$]
    in attribute the_base : Real;     // sum of p_the-scaled base costs [$]
    in attribute th_base : Real;      // sum of p_th-scaled base costs [$]
    in attribute et_base : Real;      // sum of p_et-scaled base costs [$]
    in attribute p_fus : Real;        // fusion power [MW]
    in attribute p_the : Real;        // thermal-electric power [MW]
    in attribute p_th : Real;         // total thermal power [MW]
    in attribute p_et : Real;         // gross electric power [MW]

    // Module count (plant-total powers). Frozen n_mod = 1 at the demo
    // design point (WI-025 checkpoint ruling 1). Source: costs.py:109-112.
    in attribute n_mod : Real default 1.0;
    // Calibration reference powers. Source: costs.py:105 (P_TH_REF=2500),
    // :106 (P_FUS_REF=2300); costing_constants.yaml:12 (ref_gross 1100,
    // used for both p_et and p_the — no-DEC).
    in attribute p_fus_ref : Real default 2300.0;
    in attribute p_the_ref : Real default 1100.0;
    in attribute p_th_ref : Real default 2500.0;
    in attribute p_et_ref : Real default 1100.0;

    out attribute cost : Real =
        fixed_base
        + fus_base * (p_fus * n_mod / p_fus_ref)
        + staff_base * (p_et * n_mod / p_et_ref) ** 0.5
        + the_base * (p_the * n_mod / p_the_ref)
        + th_base * (p_th * n_mod / p_th_ref)
        + et_base * (p_et * n_mod / p_et_ref);
}

calc def 'Preconstruction Cost' {
    doc /*
    CAS10 preconstruction PRE-CONTINGENCY subtotal: land (sqrt of
    plant-total net electric, anchored at ref_net_power) plus the fixed
    adders (permits + licensing + studies + reports + other — fuel/FOAK-
    keyed, so a concept input). costs.py:79 adds CAS10's own contingency;
    deliberately NOT carried here — the plant's CAS29 applies contingency
    once over the direct sum (convention preserved, MR-WI025-3; design-
    stage check: 1cfe full CAS10 = this subtotal x 1.10 exactly).
    **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
    **Ref**: costs.py:52-80 (cas10_preconstruction);
        costing_constants.yaml:8, :15-23
    **Basis**: CAS10 subtotal, contingency deliberately omitted (CAS29)
    */

    in attribute fixed_precon : Real;  // fixed adders, fuel/FOAK-keyed [$]
    in attribute p_net : Real;         // net electric power [MW]

    // Frozen n_mod = 1 (WI-025 ruling 1). Source: costs.py:64.
    in attribute n_mod : Real default 1.0;
    // Land calibration. Source: costing_constants.yaml:21 (0.25 acres/MWe
    // at ref), :22 ($10000/acre), :8 (ref_net_power_mwe 1000).
    in attribute land_intensity : Real default 0.25;
    in attribute land_cost : Real default 10000.0;
    in attribute ref_net_power : Real default 1000.0;

    out attribute cost : Real =
        land_intensity * (p_net * n_mod * ref_net_power) ** 0.5 * land_cost
        + fixed_precon;
}

calc def 'Annual OM Cost' {
    doc /*
    CAS70 UNLEVELIZED annual O&M: fuel-keyed staffing base (om_ref, a
    concept input) scaled by sqrt of plant-total net electric. CAS71
    inflation levelization and CAS72 scheduled replacement are documented
    Stage-3 refinements, not carried (convention preserved, MR-WI025-3).
    om_direct is an additive direct term for concepts that specify O&M
    outright (WI-024 p_direct pattern); 0 -> pure costs.py:353 formula,
    and with om_ref = 0 the calc passes om_direct through exactly (IEEE-
    exact identity, the handshake injection path — WI-025 D5/D6).
    **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
    **Ref**: costs.py:319-357 (cas70_om; annual line :353);
        costing_constants.yaml:272 (om_cost_dt 54.9), :8 (ref 1000)
    **Basis**: staffing power-law O&M, unlevelized (CAS71/72 out of scope)
    */

    in attribute om_ref : Real;        // annual O&M at ref power, fuel-keyed [$/yr]
    in attribute p_net : Real;         // net electric power [MW]

    // Frozen n_mod = 1 (WI-025 ruling 1). Source: costs.py:353.
    in attribute n_mod : Real default 1.0;
    // Source: costing_constants.yaml:8 (ref_net_power_mwe 1000).
    in attribute ref_net_power : Real default 1000.0;
    // Staffing economy-of-scale exponent. Source: costs.py:353 (** 0.5).
    in attribute alpha : Real default 0.5;
    in attribute om_direct : Real default 0.0;  // directly-specified O&M (additive)

    out attribute annual_om : Real =
        om_ref * (p_net * n_mod / ref_net_power) ** alpha + om_direct;
}
```

(Parse/validate-checked this session; all three FULLY_COMPILABLE in the snapshot spike.)

### 2. Generic plant (`models/designs/generic_mfe/mfe_plant.sysml` + staged twin, same edit regions)

- Line 98-99 region: `part buildings : 'Buildings' { :>> capital_cost = buildings_cost.cost; }` (turbine idiom) and `attribute preconstruction_capital : Real = precon_cost.cost;` — the "pass-through" comments retire; doc lines say "forward-computed (WI-025)".
- Line 394 region: `attribute annual_om : Real = om_cost.annual_om;` — comment updated (no longer "pass-through (WI-011)").
- After the misc_cost block: eight concept-input attributes + three calc usages:

```sysml
// CAS21 grouped base-cost sums [$] (WI-025 D1; instance binds — fuel-keyed).
attribute bldg_fixed_base : Real;
attribute bldg_fus_base : Real;
attribute bldg_staff_base : Real;
attribute bldg_the_base : Real;
attribute bldg_th_base : Real;
attribute bldg_et_base : Real;
calc buildings_cost : 'Buildings Cost' {
    in fixed_base = bldg_fixed_base;
    in fus_base = bldg_fus_base;
    in staff_base = bldg_staff_base;
    in the_base = bldg_the_base;
    in th_base = bldg_th_base;
    in et_base = bldg_et_base;
    in p_fus = fusion.p_fus;
    in p_the = p_the;
    in p_th = p_th;
    in p_et = p_et;
}

// CAS10 fixed preconstruction adders [$] (WI-025; instance binds — fuel/FOAK-keyed).
attribute precon_fixed_base : Real;
calc precon_cost : 'Preconstruction Cost' {
    in fixed_precon = precon_fixed_base;
    in p_net = pb.p_net;
}

// CAS70 annual O&M at reference power [$/yr] (WI-025; instance binds — fuel-keyed).
attribute om_annual_ref : Real;
calc om_cost : 'Annual OM Cost' {
    in om_ref = om_annual_ref;
    in p_net = pb.p_net;
}
```

`direct_capital`, `total_capital`, `lcoe_calc`, the rollup calcs: **untouched** (offender lines stay content-identical).

### 3. Stellaris instance (`models/designs/stellarator_09/stellarator_plant.sysml` + staged twin, same regions)

**Region :262-281 (buildings literal) →** six bindings; representative docs (full MR-4 docs at implement, this pattern):

```sysml
// CAS21 buildings — forward-computed (WI-025): buildings_cost tracks the
// model's p_fus/p_the/p_th/p_et (p_the = p_et, no DEC — costs.py:104).
// The six sums below are the exact grouped collapse of the 18-building DT
// column, cryogenics included (SC coils); DT and n_mod = 1 frozen at the
// design point. STALE BASIS retired: the old $613.65M literal was computed
// at pre-WI-019 powers (p_et 896.8 / p_th 2693.1).
:>> bldg_fixed_base = 168500000.0 {  // fixed-basis base costs [$].
    doc /* 168.5 M$ x 1e6 = site_improvements 85 + fuel_storage 9 +
    control_room 14 + security 3.5 + maintenance 17 + site_services 5 +
    cryogenics 14 (SC-gated, applies: REBCO HTS, costs.py:137) +
    assembly_hall 21 (all DT column).
    **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
    **Ref**: costing_constants.yaml:177,183-185,188-189,195,197
    **Basis**: exact grouped sum, fixed-scaling buildings (WI-025 D1) */
}
:>> bldg_fus_base = 288000000.0 {    // p_fus-scaled: reactor_building 138 + hot_cell 104 + reactor_auxiliaries 29 + ventilation_hvac 17. Ref yaml:179-181,186. }
:>> bldg_staff_base = 9000000.0 {    // staff-scaled (sqrt p_et): administration 9. Ref yaml:187; costs.py:127-129. }
:>> bldg_the_base = 58000000.0 {     // p_the-scaled: turbine_building 58. Ref yaml:191. }
:>> bldg_th_base = 26000000.0 {      // p_th-scaled: heat_exchanger 17 + service_water 9. Ref yaml:192,196. }
:>> bldg_et_base = 29000000.0 {      // p_et-scaled: power_supply 17 + onsite_ac 12. Ref yaml:193-194. }
```

**Region :594-614 (preconstruction literal) →**

```sysml
:>> precon_fixed_base = 32000000.0 {  // CAS10 fixed adders [$] (WI-025).
    doc /* 32 M$ x 1e6 = site_permits 3 + licensing_cost_dt 5 (DT frozen) +
    plant_permits 2 + plant_studies_foak 20 (FOAK frozen) + plant_reports 1
    + other_precon 1. preconstruction_capital now tracks the computed p_net
    via precon_cost (land ~ sqrt(p_net x 1000 x 1)); bound pre-contingency
    (CAS29 applies once — convention preserved). STALE BASIS retired: the
    old $33.896M literal was computed at p_net = 575.3 (WI-018).
    **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
    **Ref**: costing_constants.yaml:15-23; costs.py:52-80 (:79 contingency not carried)
    **Basis**: CAS10 fixed adders at the frozen DT/FOAK design point */
}
```

**Region :643-660 (annual_om literal) →**

```sysml
:>> om_annual_ref = 54900000.0 {  // CAS70 O&M at 1 GWe, DT [$/yr] (WI-025).
    doc /* om_cost_dt 54.9 M$/yr x 1e6. annual_om now tracks the computed
    p_net via om_cost (x sqrt(p_net/1000)); unlevelized — CAS71 inflation
    and CAS72 scheduled replacement remain documented Stage-3 refinements
    (convention preserved). STALE BASIS retired: the old $41.641M/yr
    literal was computed at p_net = 575.3 (WI-018).
    **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
    **Ref**: costing_constants.yaml:272; costs.py:319-357 (annual line :353)
    **Basis**: staffing-based DT O&M, power-law scaled, unlevelized */
}
```

**Headline doc block (:49-70)** — re-baselined at implement to the executed WI-025 numbers (expected: total $12.6389B, LCOE $203.647, magnet share 50.03%; p_net/q_eng/rec_frac unchanged); history line appended (WI-025 forward-computed the last three pass-through accounts, retiring the final STALE BASIS annotations).

### 4. Oracle + runner + handshake (`exploration/stellarator_e2e/`)

Per D6/D7. Oracle mirrors the generated statement forms verbatim (recorded above; the design forms are association-identical, verified against the emitted impls). Runner glue-2 harvests the buildings/precon channels (SPECIAL precedent); headline asserts retarget. Handshake: the one D6 injection-map edit only.

### 5. Regen (implement)

Unfiltered snapshot from the staged tree (`sysml-codegen snapshot -m <staged models> -o stellarator.snapshot.json`, NO `--design-path-filter` — WI-024 gotcha) → `bridge_v11_generate.py` (defaults; `preserve_handwritten=True`). Post-regen checks: exactly 3 bridged offenders; key diff exactly the +8/+13/−1(−4 pre-run) surface above; three new impls AUTO_IMPLEMENTED; backlog still 1 function; WI-022 `dt_fusion_power_impl.py` sha256 `8d2357…794a9f` unchanged. Known regen-resets (3 bridge keys, 4 BOP wirings, 3 glue schema fields) re-applied by runner glue on execute.

## Cross-File Bindings

| binding | file | change |
|---|---|---|
| 6 base sums + fixed_precon + om_ref | `mfe_plant.sysml` calc usages ← new plant attributes | concept inputs, instance-bound (D2) |
| `in p_fus = fusion.p_fus` | `mfe_plant.sysml` buildings_cost | dotted chain (wall_load precedent) |
| `in p_the/p_th/p_et = p_the/p_th/p_et` | `mfe_plant.sysml` buildings_cost | self-named alias chains, no glue (spike-proven) |
| `in p_net = pb.p_net` (×2) | `mfe_plant.sysml` precon_cost / om_cost | dotted chain (lcoe precedent) |
| `:>> capital_cost = buildings_cost.cost` | `mfe_plant.sysml` buildings part | turbine idiom (D4) |
| `preconstruction_capital = precon_cost.cost`, `annual_om = om_cost.annual_om` | `mfe_plant.sysml` | attribute-mediated chains (D4, spike-proven) |
| 8 instance literals with MR-4 docs | `stellarator_plant.sysml` | replaces the 3 stale literals |
| `om_cost__om_ref: 0.0` + `om_cost__om_direct: 1cfe annual_om` | `handshake_1costingfe.py` `set_1cfe_inputs` | D6 identity injection (replaces `lcoe_calc__annual_om`) |

Dataflow stays unidirectional: instance literals + pb/fusion outputs → account calcs → rollup/LCOE. No cycles (L3 pass); costs feed nothing upstream (denominator invariant by construction).

## Validation Plan

1. **L1–L6** after each phase; final gate `uv run agentic-mbse validate models --complete` on the canonical 22-file set: offender list exactly the 6 pre-existing, content-identical (mfe_plant lines shift :353→389, :359→395, :364→400), zero new. Do not gate on the staged-subset run (documented quirk above).
2. **Mirroring**: per-edit-region diff canonical vs staged for all three files (known WI-015 divergences outside the edit regions persist).
3. **Regen** per §5; the key-diff and offender/impl checks are pass/fail.
4. **Execute**: `run_stellaris.py` (exec venv `/home/reid/1cfe/fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python`) bit-exact vs the re-baselined oracle at rel 1e-9 on every channel including the three new account channels; headline at the expected values (recorded, not fitted).
5. **Handshake** under the successor bar: D6 edit only; `git diff exploration/stellarator_e2e/handshake_comparison.json` empty (SV-025/026 byte-identical).
6. **Regressions**: IFE `run_anchors.py` 252.30/68.69/270.12 $/MWh, Meier 4.735 c/kWh; pytest tally unchanged vs 11 failed / 18 passed / 14 skipped / 0 errors.
7. **Close-out**: SV-032 → executed record (three accounts, direct/total, LCOE); SV-030/031 stand; `.project/CURRENT_WORK.md` headline; owner holds close.

## Validation Report (design-stage)

- **Parse/validate: PASS** — canonical scratch tree with the full prototype: L1 = 0 over 22 files; L2/L6 offender list exactly the 6 baseline offenders, content-identical, line-shifted; level profile identical to the baseline run executed first as a control.
- **Snapshot classification: PASS** — staged scratch tree, sysml-codegen HEAD `6db3212`: three modules FULLY_COMPILABLE; buildings p_et/p_the/p_th/p_fus and precon/om p_net all chain-wired to pb/fusion channels; `lcoe_calc.annual_om` chains to `om_cost__annual_om.root`; `lcoe_calc__annual_om` leaf gone; +8/+13 new leaves at the designed values.
- **Bridge/emission: PASS** — exactly 3 V11 offenders (the known rollup keys), bridged, package emitted; three new impls AUTO_IMPLEMENTED; `IMPLEMENTATION_BACKLOG.md` still exactly 1 function.
- **Exactness (MR-WI025-2): PASS** — 1costingFE-side evaluation at the executed powers, run in the pinned checkout's own environment: CAS21 and CAS70 bit-identical to the forward forms at float64; CAS10 within 1 ulp (association); 1cfe's float32 runtime values recorded (−4.8e-8 / +3.2e-9 / 0 rel). CAS10 contingency convention re-confirmed (full = subtotal × 1.10 exactly).
- **Expected headline: computed** — oracle-rollup-exact: total $12,638,857,665.74 (+0.296%), LCOE $203.647152/MWh (+$2.1751), magnet share 50.03%; p_net/q_eng/rec_frac/magnet unchanged. Direction honest: capital and LCOE up.

## Implementation Checklist

1. **Library** — append the three calc defs to `mfe_account_costs.sysml` (canonical + staged, identical). L1–L3.
2. **Generic plant** — 8 attributes + 3 calc usages + buildings/precon/annual_om rewires (canonical + staged). L1.
3. **Instance** — replace the three regions with the 8 cited bindings; retire STALE BASIS; headline + history refresh (canonical + staged). Full canonical L1–L6 offender-list compare; mirroring diff.
4. **Regen** — unfiltered snapshot + bridge; post-regen checks per §5.
5. **Oracle + runner** — forward mirrors, channel checks, glue-2 harvest, headline retarget; execute bit-exact.
6. **Handshake** — D6 injection edit; run; empty `handshake_comparison.json` git diff; IFE + pytest regressions.
7. **Close-out** — SV-032 executed record; headline records; owner close.

## Risks

| risk | likelihood | impact | mitigation |
|---|---|---|---|
| Regen run with `--design-path-filter` → 8 spurious offenders | medium (easy to repeat) | medium | WI-024 gotcha carried forward; control: bridge must report exactly 3 before proceeding |
| sysml-codegen HEAD moves before implement | low | medium | spiked at `6db3212`; re-run the unedited-tree control if HEAD changed |
| Oracle/impl statement-form drift (bit-exactness) | low | medium | generated forms recorded here; oracle mirrors them verbatim; rel 1e-9 gate per channel |
| Implement gates on the staged-subset validation and sees the reclassified precon error | medium | low (confusion only) | quirk documented in Research Findings and Validation Plan step 1: the bar is the canonical set |
| Regen clobbers the WI-022 handwritten impl | low | high | `preserve_handwritten=True`; content-hash check post-regen |
| Handshake identity not exact | very low | high | IEEE identity (0·x = 0, 0 + v = v) + WI-024 D7 executed precedent; gate is the empty git diff |
| Future multi-module concept must touch 3 per-calc n_mod leaves | certain (accepted) | low | D3 documented trade; frozen n_mod = 1 is a spec ruling |
| q_eng still below SV-016 band | certain | — | untouched this item (denominator does not move); band is owner's |
