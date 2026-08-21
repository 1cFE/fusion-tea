---
Status: completed
Scale: standard
Epic: Stellarator MBSE Full Demo
Owner: reidw
Created: 2026-07-20
Updated: '2026-08-02'
---

# WI-029 Spec — Handshake account scope: LCOE construction (CAS70/80 + IDC)

**STELLARATOR-DEMO epic Item 4. The finishing item for concept criterion 3 (Anchor A).** After it, the Anchor-A verdict is written in the A-4 form — met or honestly failed, no third state.

**Governing frame:** `.project/concepts/stellarator-mbse-demo.md`, criterion 3. Tracking home: `.project/backlog/epic_stellarator_mbse_demo.md`, Item 4. Orchestration brief: `work/orchestration/handshake-lcoe-construction.md`.

**Required Reading (every stage):** `knowledge/holdout/aries-cs/PROTOCOL.md` §3 — barred paths absolute; quarantine sealed; none read this stage.

---

## Overview

Bring the LCOE construction under the 1costingFE handshake. WI-028 rebuilt the overnight/total-capital assembly to mirror 1cfe and ruled CAS60 as a reported Option-C line. What remains is the annual-cost side of LCOE — CAS70 (levelized O&M **and** scheduled replacement), CAS80 (fuel), and the CAS90/IDC financing convention — forward-computed and reconciled to 1cfe's LCOE form at the pinned handshake point, plus a bounded closure attempt on the pre-existing CAS10 divergence. The deliverable is the **criterion-3 verdict written in the A-4 form**.

---

## Goals & Context

- **Serves:** concept criterion 3 (Anchor A handshake) — the finishing item; G-8 (account-scope form, amended in-force). Anchor spec A-2/A-3/A-4/A-5/A-6.
- **Consumes Item 3 (WI-028):** the rebuilt overnight assembly (`total_capital = overnight_capital`), the CAS60 Option-C mapping (`'IDC Closed-Form Cost'` reported line; DCF `idc_factor` left untouched *for this item to reconcile*), and the D2b staged-twin rule (binding for every `.sysml` edit here).
- **Current post-WI-028 harness** (surveyed, not inherited as fact): `handshake_comparison.json` @ `feb13ff3`; design-point headline total $16,145,706,216.04, LCOE $258.013640/MWh, p_net 915.081088, q_eng 6.606662; oracle bit-exact.

---

## Survey (pin `0254385`, re-read from 1cfe source and the model this stage)

### 1cfe LCOE construction — how the emitted point is built

`compute_lcoe(cas90, cas70, cas80, p_net, n_mod, availability)` (`economics.py:78-92`):

```
LCOE = (CAS90 + CAS70 + CAS80) * 1e6 / (8760 * p_net * n_mod * availability)   = 123.743 $/MWh
```

Emitted values (`onecfe_point.json`, costs_musd): **cas90 813.587, cas70 161.234, cas80 0.769**, total_capital 10095.838, overnight 7872.149.

**CAS90 — financial (capital) charge.** `cas90_financial = CRF(i,n) * total_capital` (`costs.py:547-556`) = CRF(0.07,30)·10095.838 = 813.587. Plain CRF; construction-period financing is carried by CAS60 (IDC), not folded into CRF here.

**CAS70 — O&M + scheduled replacement, both levelized** (`costs.py:319-437`, assembled `model.py:1548-1568`). **CAS70 = CAS71 + CAS72 = 79.004 + 82.230 = 161.234.** Two independent streams:

- **CAS71 (levelized O&M) = 79.004.** Raw annual O&M `annual_om = om_cost(DT 54.9) * (p_net·n_mod / 1000)**0.5` — this is exactly the WI-025 unlevelized $52.517M/yr (`'Annual OM Cost'`). It is then run through `levelized_annual_cost(annual_om, i, g, n, t_project)` (`economics.py:13-49`): `A1 = annual_om·(1+g)^Tc; PV = A1·(1−((1+g)/(1+i))^n)/(i−g); cas71 = CRF(i,n)·PV`. At i=0.07, g=inflation 0.02, n=30, Tc=t_project=construction_time 8 (NOAK: `_total_project_time` adds licensing_time only at FOAK, `costs.py:41-46`), the levelization factor is **cas71/annual_om = 79.004/52.517 = 1.5043**.
- **CAS72 (levelized scheduled replacement) = 82.230.** `cost_per_event = Σ(cas22_detail[k] for k in replaceable_accounts)·n_mod`, `replaceable_accounts = ("C220101","C220108")` (first-wall/blanket + divertor; `defaults.py:299`); `core_lifetime_cal = core_lifetime_FPY / availability`; `cas72 = levelized_replacement_cost(cost_per_event, core_lifetime_cal, i, n)` (`economics.py:52-74`: `s=(1+i)^(−t); n_rep=max(0, ceil(n/t)−1); pv=event·s(1−s^n_rep)/(1−s); cas72=CRF·pv`). `core_lifetime_FPY = clip(fluence_limit(fuel)/q_n, 0.5, n·availability)`, `q_n = p_neutron/firstwall_area` (`model.py:102-112, 1515-1519`). DEC-grid / cap-bank / electrode / laser terms are structural zero for a RANKINE steady-state DT stellarator (p_dee=0, not pulsed, not z-pinch/laser).

**CAS80 — levelized fuel = 0.769** (`costs.py:438-546`). DT: `cost_per_rxn = M_D_KG·u_deuterium + M_Li6_KG·u_li6`, `q_eff = Q_DT`; `annual = n_mod·p_fus·(3600·8760)·availability·cost_per_rxn/(q_eff·MEV_TO_JOULES)`; burn-fraction correction `×(1 + (1−burn)/burn·(1−recovery))`; target-consumable term = 0 (MFE); then `levelized_annual_cost(annual, i, g, n, t_project)` (same wrapper as CAS71).

### Model LCOE side (`mfe_lcoe_dcf.sysml`, wired `mfe_plant.sysml:508-606`)

`'LCOE DCF'`: `annual_capital = total_capital · idc_factor · crf`; `lcoe = (annual_capital + annual_om) / (8760·p_net·availability)`, `crf = CRF(d,N)`, **`idc_factor = (1+d)^(Yc/2) = 1.07^4 = 1.310796`** (even-spend midpoint). Instance binds `total_capital = overnight_capital` (Option C, CAS60 excluded), `annual_om = om_cost.annual_om` (the **unlevelized** $52.517M/yr), discount_rate 0.07, construction_years 8, operational_years 30, availability 0.85. **No CAS71 levelization, no CAS72, no CAS80** anywhere in the model. No `inflation_rate` input exists yet.

### The IDC convention — mechanical-vs-choice, stated precisely (do not pick — design rules it)

Both sides fold IDC into one annual capital charge, but the multiplier and the CAS60 placement differ:

- **1cfe:** `total_capital = overnight + CAS60`, `CAS60 = f_idc·overnight` with `f_idc = ((1+i)^T−1)/(i·T)−1` (uniform-spend closed form), so `CAS90 = CRF·overnight·(1+f_idc) = CRF·overnight·1.282476`.
- **model:** `annual_capital = overnight · (1+d)^(Yc/2) · CRF = CRF·overnight·1.310796`.

The multipliers differ (1.282476 vs 1.310796, ≈ +2.2% on the capital charge → ≈ +1.8% on LCOE). An end-to-end LCOE comparison in 1cfe's form requires the model's capital charge to use 1cfe's multiplier. **The mechanical-vs-choice question:** does aligning fall out mechanically from Item 3's Option-C CAS60 mapping (the `'IDC Closed-Form Cost'` line already computes `f_idc·overnight` — reuse it: a 1cfe-form CAS90 channel `= CRF·(overnight + CAS60)`), or is it a genuine convention choice because the model's *headline* LCOE keeps its DCF `(1+d)^(Yc/2)` idc_factor? Two resolutions the design must weigh with evidence:

- **(adopt-1cfe-form)** the model drops the DCF `idc_factor` and adopts 1cfe's `total_capital = overnight+CAS60`, `CAS90 = CRF·total_capital` — this changes the model's own headline LCOE convention, not just adds accounts.
- **(mapped-comparison)** the model keeps its DCF `idc_factor` for its headline LCOE and the handshake compares a *separately-computed 1cfe-form CAS90/LCOE channel* at the handshake point (a reported channel), leaving the model headline convention intact — WI-028's D4 pattern.

Because Option C deliberately left `idc_factor` untouched and the adopt-1cfe-form path changes the model's headline LCOE, this is **very likely a genuine convention choice → the reserved gate under Align ruling 3.** The design rules it with evidence and parks for owner with options if genuine; if it falls out mechanically, record and proceed. **This spec does not pick the mechanism.**

### CAS10 divergence — candidate causes (do not fix; root-cause is design/implement)

Model CAS10 = 34.5 M$ vs 1cfe c10 = 18.5 M$ at the handshake point: **+$16.0M / +86.5%** (pre-existing WI-025 basis).

- 1cfe `cas10_preconstruction` (`costs.py:52-80`): `land = 0.25·sqrt(p_net·n_mod·1000)·10000/1e6` (≈2.5) + fixed adders `site_permits 3 + licensing_dt 5 + plant_permits 2 + studies + plant_reports 1 + other_precon 1`, then `×(1+contingency_rate)`. **At the handshake point 1cfe runs NOAK:** `plant_studies_noak = 4.0`, `contingency_rate_noak = 0.0` → fixed = 16.0, CAS10 = 2.5 + 16.0 = 18.5.
- Model (`'Preconstruction Cost'` calc `mfe_account_costs.sysml:356-386`; instance `precon_fixed_base = 32.0 M$`, `stellarator_plant.sysml:632`): fixed adders bound with **`plant_studies_foak = 20.0` ("FOAK frozen")** → fixed = 32.0, land ≈ 2.5, CAS10 = 34.5.

**Leading candidate (clean single error): FOAK/NOAK studies mismatch.** `plant_studies_foak 20.0 − plant_studies_noak 4.0 = $16.0M` — matches the divergence to the dollar. The rest of the handshake stack runs NOAK (cas29 contingency = 0); the model froze the CAS10 fixed adders at FOAK studies. **Secondary thread to confirm single-error:** the WI-025 CAS10 doc asserts "1cfe full CAS10 = subtotal × 1.10 exactly" (the FOAK 0.10 contingency), so the FOAK/NOAK confusion touches both the studies term and the contingency convention note; land, licensing, permits, reports, other all agree. Design confirms the fix reconstructs 1cfe's 18.5 cleanly from a single FOAK→NOAK correction (studies 20→4) with no residual before it is treated as an error.

**Owner stop condition carried verbatim (Align ruling 4, MR-WI029-6):** *"please try (a) but stop if there is not a clear resolution"* — attempt the CAS10 error-to-close; STOP-and-surface if the divergence does not resolve to one clearly identified error (ambiguous basis, multiple candidate causes, or a fix that does not reconstruct 1cfe cleanly) → revert to explained-remainder treatment and park for owner. Do not force it.

### Classification of each LCOE-construction element

| Element | 1cfe value | Classification | Note |
|---|---|---|---|
| CAS71 levelization | 79.004 | **forward-computable** | reuse WI-025 unlevelized annual_om + closed-form `levelized_annual_cost`; new input `inflation_rate` (0.02); Tc = construction_years (NOAK) |
| CAS72 scheduled replacement | 82.230 | **forward-computable, codegen-envelope risk** | needs replaceable-account set (C220101 blanket + C220108 divertor — both modeled), core-lifetime-FPY (from modeled p_neutron/firstwall_area/fluence), replacement closed-form. **Risk: `ceil`/`clip`/`where`/`max` in `levelized_replacement_cost` + `_core_lifetime_fpy` may exceed the flat-Real codegen envelope** — if unexpressible, CAS72 becomes a signed A-4 remainder with that reason. See Surfaced-1 and Risk 1. |
| CAS80 fuel | 0.769 | **forward-computable, needs-new-inputs** | DT fuel constants (u_deuterium, u_li6, isotope masses, Q_DT, MEV_TO_JOULES, burn_fraction, fuel_recovery) + same levelization wrapper; small magnitude |
| CAS90 financial | 813.587 | **forward-computable, IDC gate** | `CRF·total_capital`; the multiplier alignment is the reserved-gate question above |
| CAS10 divergence | +16.0 (+86.5%) | **remainder-candidate / error-to-close** | FOAK/NOAK studies; Align ruling 4 with stop condition |

---

## Modeling Requirements

Requirement IDs `MR-WI029-N`. Provenance per `capture-fidelity`.

**MR-WI029-1 — CAS71 levelized O&M into LCOE. [NEED]** The model SHALL forward-compute the levelization of the WI-025 unlevelized annual O&M into 1cfe's CAS71 form (`levelized_annual_cost`, `economics.py:13-49`) at pin `0254385`, MR-4-sourced, and it SHALL come under the A-2 per-account bar (|rel dev| ≤ 1e-6 vs 1cfe float32) at the handshake point. Source: A-3 Item-4 list; `costs.py:353`, `economics.py:13-49`.

**MR-WI029-2 — CAS72 scheduled replacement disposition. [NEED]** The model SHALL account for CAS72 (1cfe $82.230M, the larger half of CAS70) explicitly: forward-compute it under A-2 if the codegen envelope can express its closed form (`levelized_replacement_cost` over the modeled replaceable accounts and core-lifetime-FPY), **or** itemize it as a signed A-4 remainder with the codegen-envelope reason stated. It SHALL NOT be silently dropped. (See Surfaced-1 — the design rules forward-compute vs remainder with evidence and parks for owner if this is a genuine scope expansion.) Source: `costs.py:359-437`, `economics.py:52-74`, `model.py:102-112`; A-4.

**MR-WI029-3 — CAS80 fuel into LCOE. [NEED]** The model SHALL forward-compute CAS80 levelized fuel (`cas80_fuel`, DT branch, `costs.py:438-546`) at pin `0254385`, MR-4-sourced, and it SHALL come under the A-2 bar at the handshake point. Source: A-3 Item-4 list.

**MR-WI029-4 — LCOE/IDC reconciliation, end-to-end. [NEED]** The design SHALL rule whether aligning the model's IDC/CAS90 convention to 1cfe's form is mechanical fall-out of the Option-C CAS60 mapping or a genuine convention choice, with evidence (the mechanical-vs-choice question is stated in the Survey). If genuine choice, it is a **reserved gate parked for owner with options** (Align ruling 3); if mechanical, recorded and proceeded. The end-to-end LCOE comparison SHALL be computed in a 1cfe-comparable form at the handshake point. This spec does not pick the mechanism. Source: Align ruling 3; WI-028 D4/D7; `economics.py:88-92`, `costs.py:547-556`.

**MR-WI029-5 — Criterion-3 verdict in the A-4 form. [HARD] [INHERITED: anchor spec A-4]** The item SHALL write the Anchor-A end-state verdict: (1) every modeled account (the WI-025/WI-028 set plus CAS71/CAS80 and, if forward-computed, CAS72) under the A-2 bar; (2) the remainder fully itemized with signed magnitudes — each non-bar account with its 1cfe value, the model value (or "structurally absent"), the signed dollar gap, and a one-line reason (closed-as-error or explained-and-kept); **the residual LCOE gap reconciling to the itemized-remainder sum within the aggregate tolerance (≤ 1e-6 relative to LCOE).** The verdict is met or honestly failed — no third state. Source: anchor spec A-4.

**MR-WI029-6 — CAS10 error-to-close attempt, with the owner stop condition. [OWNER] (Align ruling 4)** The item SHALL attempt to close the CAS10 +$16.0M/+86.5% divergence as an error, carrying the owner stop condition verbatim: **[OWNER-VERBATIM] "please try (a) but stop if there is not a clear resolution."** It SHALL STOP-and-surface (revert to explained-remainder, park for owner) if the divergence does not resolve to one clearly identified error — ambiguous basis, multiple candidate causes, or a fix that does not reconstruct 1cfe cleanly. Candidate causes are enumerated (Survey); root-causing and any fix are design/implement work, not this spec. Source: Align ruling 4; brief.

**MR-WI029-7 — Staged-twin propagation (D2b inherited). [HARD] [INHERITED: WI-028 D2b]** Every `.sysml` edit SHALL land region-identical in both trees — canonical `models/` and the staged twin `exploration/stellarator_e2e/models/` — with a staged-vs-canonical mirroring diff gate (only intended WI-029 edits + known Item-10/DEMO-NOTE divergences) before recapturing `stellarator.snapshot.json` from the staged tree. Codegen reads the staged twin; a canonical-only edit is a silent wrong result. Source: WI-028 design D2b.

**MR-WI029-8 — Trap assertions for every new mapping. [HARD] [INHERITED: A-5]** Each new field mapping introduced (levelization inputs, replaceable-account set, fuel constants, IDC multiplier) SHALL be asserted in the handshake and added to the trap table — never left to a "default handles it" assumption. Source: A-5.

**MR-WI029-9 — Design-point re-baseline. [NEED]** The design-point LCOE WILL move up (levelized O&M replaces unlevelized, CAS72 and CAS80 enter LCOE, and the IDC multiplier may change) — a re-baseline like WI-028, not a regression. `total_capital` is unchanged (Option C stands), so the headline *total* stays $16.146B; the *LCOE* re-baselines. The new headline SHALL be recorded and the oracle bit-exact bar (rel 1e-9 vs pure-Python oracle) SHALL hold at the new point. Source: G-8 amendment; WI-028 MR-WI028-9.

**MR-WI029-10 — Handshake JSON re-baseline, comparison logic untouched. [INHERITED: G-8]** `handshake_comparison.json` gains the new LCOE-construction rows and is re-baselined as a deliberate explicit commit; the comparison *logic* is untouched (only new rows and inputs). Source: G-8 amendment (account-scope items).

**MR-WI029-11 — Standing bars hold. [HARD]** All standing validation bars SHALL pass (see Success Criteria). Source: WI-028 close state.

---

## Scope Boundaries

**In scope:**
- Library calc def(s) for CAS71 levelization, CAS80 fuel, and (per MR-WI029-2 disposition) CAS72 replacement — concept-agnostic, MR-3/MR-4 (`models/library/analyses/mfe_account_costs.sysml` + staged twin).
- LCOE-side wiring in `mfe_plant.sysml` / `stellarator_plant.sysml` (both trees) consistent with the ruled IDC convention.
- Instance bindings for new bases (inflation_rate, fuel constants, replaceable-account costs) at the Stellaris instance, MR-4-cited at pin `0254385`.
- Handshake side (`emit_1cfe_point.py`, `handshake_1costingfe.py`): new CAS71/72/80/90/LCOE channels, rows, injections, trap assertions.
- CAS10 error-to-close attempt within the owner stop condition.
- The criterion-3 verdict artifact (below).

**Out of scope:**
- Changes to 1costingFE ([OWNER] non-goal — gaps filed, not fixed).
- Reading any barred artifact (PROTOCOL §3).
- Re-opening Item 3's overnight/total-capital rebuild or the CAS60 Option-C ruling.
- The comparison *logic* / machinery (fixed since `5127efa4`).

---

## The criterion-3 verdict deliverable

The item produces the **Anchor-A criterion-3 verdict artifact** — an updated `HANDSHAKE_REPORT` (or a named successor), referenced from `.project/backlog/epic_stellarator_mbse_demo.md` Item 4 / criterion 3. It SHALL contain, in the A-4 form:
1. The per-account pass table: every modeled account with its |rel dev| vs 1cfe float32 and pass/fail at A-2.
2. The signed-magnitude remainder itemization: every non-bar account (1cfe value, model value or "structurally absent", signed dollar gap, one-line reason).
3. **The reconciliation arithmetic:** the residual end-to-end LCOE gap equals the itemized-remainder sum within the aggregate tolerance (≤ 1e-6 relative to LCOE) — shown, not asserted.
4. The criterion-3 verdict statement: met or honestly failed.

---

## Success Criteria

- [ ] CAS71 levelization + CAS80 in the model's LCOE, forward-computed and MR-4-sourced, each under A-2 at the handshake point (SV-035).
- [ ] CAS72 disposed per MR-WI029-2 (forward-computed under A-2, or itemized as a signed A-4 remainder with the codegen-envelope reason) — not silently dropped.
- [ ] IDC/LCOE reconciliation ruled (mechanical or reserved-gate-parked per Align ruling 3); end-to-end LCOE compared in 1cfe-comparable form.
- [ ] CAS10 error-to-close attempted under the verbatim owner stop condition; result recorded (closed-as-error with clean reconstruction, or reverted to explained remainder and parked).
- [ ] Criterion-3 verdict written in the A-4 form with the reconciliation arithmetic shown; verdict met or honestly failed.
- [ ] Design-point headline re-baselined and recorded; oracle bit-exact rel 1e-9 at the new point; `total_capital` unchanged.
- [ ] `handshake_comparison.json` re-baselined as an explicit commit; comparison logic untouched.
- [ ] Every `.sysml` edit region-identical in both trees; mirroring diff gate clean; snapshot recaptured from the staged tree (D2b).
- [ ] Standing bars: oracle rel 1e-9; WI-022 sha256 `8d2357…794a9f` survives regen; IFE Runs A/B byte-exact (Run C out-of-scope by [OWNER] ruling 2026-07-20); pytest 11/18/14/0; L1=0, offenders = the 6 pre-existing + WI-028's design-accepted rollup-key L6 set; regen stability; MR-3/MR-4; PROTOCOL sealed; toolchain pins (sysml-codegen `06d95f8`, teax `07eb0ac`, agentic-mbse `4c18d61`, 1costingFE `0254385`) verified live at design and re-checked before every codegen/exec step (WI-028 mid-run-drift precedent).
- [ ] SV-035 registered and passing.

---

## Assumptions & Risks

1. **[Risk, medium-high — codegen envelope] CAS72's closed form uses `ceil`/`clip`/`where`/`max`.** `levelized_replacement_cost` (`n_rep = ceil(n/t)−1`) and `_core_lifetime_fpy` (`clip(fluence/q_n, 0.5, n·avail)`) are not flat-Real arithmetic. The proven envelope covers `+ − * / **` including variable exponents (`idc_factor`); `ceil`/`clip` may not lower. If they cannot be expressed, CAS72 is itemized as a signed A-4 remainder (MR-WI029-2). The design de-risks this at the first codegen checkpoint. Likelihood medium, impact medium (an $82M remainder is large but A-4-legitimate if reasoned).
2. **[Risk, medium — reserved gate] IDC convention is a genuine choice.** If ruled a choice (Align ruling 3), it parks for owner and the end-to-end verdict waits on that ruling — the design surfaces options, does not force. Likelihood medium.
3. **[Risk, low — CAS10] The FOAK/NOAK candidate does not reconstruct cleanly.** If a single FOAK→NOAK studies correction leaves residual, the owner stop condition fires and CAS10 reverts to explained remainder. Likelihood low (the $16.0M match is exact), impact low (bounded by the stop condition).
4. **[Risk, high — inherited] Staged-twin skip.** Canonical-only edits give a silent wrong result. Mitigation: D2b (MR-WI029-7).
5. **[Assumption] Handshake point is NOAK** (cas29=0, plant_studies_noak, contingency_rate_noak) — the basis for the CAS10 candidate and the CAS71/CAS80 `t_project = construction_time` levelization. Confirmed against the WI-028 reproduction; design re-confirms.

---

## Surfaced (capture-fidelity §4 — not resolved silently)

**Surfaced-1 — CAS70 is not "levelize the $52.5M/yr"; it is CAS71 + CAS72, and CAS72 ($82.23M) is the larger, entirely-unmodeled half.** The brief and epic Item 4 frame CAS70 as "the levelization step into LCOE remains" for the WI-025 unlevelized $52.5M/yr. The survey shows that $52.5M/yr is only the CAS71 *base*; the full 1cfe CAS70 = 161.234 = CAS71 79.004 (levelized O&M) + CAS72 82.230 (levelized scheduled replacement of the first-wall/blanket and divertor). CAS72 is absent from the model entirely and is ≈10.4 $/MWh of the handshake LCOE — large enough that silently omitting it would break the A-4 reconciliation. Following the recorded framing literally would drop it. **Surfaced, dependent conclusion parked:** MR-WI029-2 requires CAS72 to be handled explicitly (forward-compute or signed remainder); the design rules the disposition with evidence and — because forward-computing an $82M replacement stream materially exceeds the brief's "apply a levelization factor" framing and the Item-4 effort estimate — parks the scope question (forward-compute vs itemize-as-remainder) for owner if it is a genuine expansion. This does not block writing the spec; the A-4 forward-compute-or-itemize framework covers both outcomes.

---

## Traceability

- **1cfe formulas (pin `0254385`):** `economics.py:6-92` (CRF, levelized_annual_cost, levelized_replacement_cost, compute_lcoe), `costs.py:41-80` (_total_project_time, cas10), `costs.py:319-556` (cas70_om, cas80_fuel, cas90_financial), `model.py:102-112` (_core_lifetime_fpy), `model.py:1483-1568` (LCOE assembly), `defaults.py:299` (replaceable_accounts).
- **Model (canonical + staged twin, D2b):** `models/library/analyses/mfe_account_costs.sysml` (+ `mfe_lcoe_dcf.sysml`), `models/designs/generic_mfe/mfe_plant.sysml`, `models/designs/stellarator_09/stellarator_plant.sysml`, and their `exploration/stellarator_e2e/models/...` twins; snapshot `exploration/stellarator_e2e/stellarator.snapshot.json`.
- **Harness:** `exploration/stellarator_e2e/{emit_1cfe_point.py, handshake_1costingfe.py, handshake_comparison.json, onecfe_point.json}`.
- **Requirements:** MR-WI029-1..11; anchor spec A-2/A-3/A-4/A-5/A-6 + G-8; MR-3, MR-4; Align rulings 1–5.
- **Upstream:** WI-028 design (`work/completed/20260720_WI-028_handshake-account-scope/design.md`), Option-C / D2b / D4 / D7.

## Related Artifacts

- **Epic / criterion:** `.project/backlog/epic_stellarator_mbse_demo.md` Item 4 (criterion 3).
- **Governing concept:** `.project/concepts/stellarator-mbse-demo.md` criterion 3.
- **Brief:** `work/orchestration/handshake-lcoe-construction.md`.
- **Anchor spec:** `.project/active/demo-anchor-acceptance-spec/spec.md`.
- **Required Reading:** `knowledge/holdout/aries-cs/PROTOCOL.md` §3 (honored, none read).
- **Design / plan:** to be created (`/design-model` → `/plan-model`).
- **Validation:** SV-035 (`modeling_project/VALIDATION_MATRIX.md`).
