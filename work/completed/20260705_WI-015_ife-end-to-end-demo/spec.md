---
Status: completed
Scale: standard
Epic: Pipeline De-Risk & Demonstration
Owner: reid
Created: 2026-07-05
Updated: '2026-07-05'
---

# WI-015: IFE End-to-End Demonstration — Codegen, Sweep, Viability Map

## Goal

Run the validated IFE/HIF SysML models through the full pipeline for the first time: live syside-backed extraction → sysml-codegen generation → AI implementation pass → teax execution. Anchor-check the generated LCOE against known-good values, then sweep the parameter space and visualize the feasible region under the ηG > 10 viability constraint (DI-001).

This is Item 3 of the pipeline de-risk epic. WI-013 proved the plumbing on solar_battery; this item proves it on models that matter, with a real correctness oracle.

## Scope

- **In**: live extraction of `models/library/` (foundation, cost_structure, analyses) + `models/designs/generic_ife/` + `models/designs/hif_ife/`; package generation; AI-pass implementation bodies; teax execution; anchor checks; ≥3-axis viability sweep; feasible-region figures; SV registration; demonstration write-up.
- **Out**: codegen Phase 6 (constraint emission) — constraints are evaluated harness-side per WI-014; any MFE modeling; explainer HTML (Item 5).

## Anchor table (the correctness oracle)

| Point | Parameters | Expected LCOE |
|---|---|---|
| Hawker 14-parameter defaults | per `scripts/verify_ife_lcoe.py` defaults | $252.30/MWh |
| Realistic HIF point | defaults + f=5 Hz, η=0.25, E_d=5 MJ, N_d=1e9, G=100, d=0.05, δ=$0.50, avail=0.85 | $68.69/MWh |
| WI-008 Osiris plant point (SV-013) | the `hif_plant` bindings as modeled (η=0.35, f=3.5, G=80, γ from Meier Eq. 5) | $270.12/MWh (~$270) |

All three cross-checked against `uv run python scripts/verify_ife_lcoe.py` (which mirrors `ife_lcoe.sysml` line-for-line). The Osiris value $270.12 was computed with the same function at the `hif_plant` bindings, including the Meier-derived γ = $68.247/J.

## Tolerance

**Relative 1e-6** on all three anchors. Justification: the entire model is flat floating-point arithmetic (+ − × ÷ **), so the generated code should agree to float precision — WI-013 observed exact agreement at 1e-12. 1e-6 leaves room for expression reassociation by the AI pass while still catching any wrong term, constant, or unit slip (the smallest plausible modeling error moves LCOE by ≫0.01%).

## Acceptance criteria

- [ ] Live extraction succeeds over the IFE model set (first live extraction since the license lapse, first ever of these models); any IFE-construct breakage characterized at file:line before fixes; model fixes only if trivially safe (WI-014 rider class) and listed prominently in findings
- [ ] Generated package executes through the teax executor
- [ ] All three anchors match within tolerance; any deviation investigated and explained
- [ ] Sweep over ≥3 axes (rep rate f, driver efficiency η, target gain G; optional availability), each point classified by ηG > 10 (harness-side, per WI-014 — constraints do not survive extraction) plus an LCOE-threshold overlay; grid sized for minutes
- [ ] Feasible-region figure(s), committed quality, ηG=10 knee visible; outputs in `data/ife_sweep/`
- [ ] Anchor check registered as an SV entry via `agentic-mbse pm add-validation`
- [ ] Demonstration write-up at `work/active/WI-015_ife-end-to-end-demo/demo_report.md`

## Artifact placement

- Extraction snapshot + generated package: `exploration/ife_e2e/` (mirrors `exploration/pipeline_spike/` layout)
- Sweep results (CSV) + figures (PNG): `data/ife_sweep/`
- Spec, findings, demo report: this directory
