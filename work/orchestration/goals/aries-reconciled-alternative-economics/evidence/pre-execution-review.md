# Pre-execution review of the comparison basis and study configuration (T-004)

[AGENT] Fresh non-author review, 2026-09-25. Files read: `evidence/comparison-basis.md`; the study `config.json`; `20260922-aries-integrated-lcoe/source-evidence/source-boundary.md`; the page images `lyon-p707.png`, `lyon-p709.png`, `lyon-p716.png` (viewed); WI-091 `design.md` § "Exact financial convention and equations"; `evidence/equipment-cost-audit.md` § "Inconsistencies and proposed smallest corrections"; `REQUIREMENTS.md` § MR-7. Nothing executed; derived arithmetic recomputed with `uv run python`.

## Verdict

`FINDINGS`. Three cheap corrections before execution; no owner decision is required. The source cells are supported, the derivations are exact, § 3 is fixed, the configuration is honest, and the independent alternative takes no published total.

## Findings

1. **[correct-before-execution] Ladder attribution rule does not match the configured designs.** § 2 promises "each step's effect in the stated order" (a cumulative reading L3 → L4 → L5 → L6). The config provides one-at-a-time steps from mixed bases (L3, L4, L5 from `alt-canonical-feed100`; L6 and L7 from `alt-canonical-no-credit`; only L4+L5 is cumulative) plus the combination. Because fuel purchase dominates the no-credit numerator, a step's effect differs by base. Either add cumulative designs (L3, L3+L4, L3+L4+L5, then +L6 = L7) or amend § 2 to "one-at-a-time from the named base, plus the combination", naming the base of every step effect. Fix now so the reading rule is not chosen after results are seen.
2. **[correct-before-execution] "The published rate's nearest neighbour" is undetermined.** p709 gives no rate (only "high interest rate ... 1990s studies"). Choosing the nearest rung after execution is a relaxation route. Replace with: report the residual gap at every swept rate (0, 3, 5, 8, 10 %) and designate none as the match.
3. **[correct-before-execution] Two design names misstate their values.** `sens-om-4e+07-feed100` carries 35,000,000; `sens-om-1e+08-feed100` carries 140,000,000. Rename (e.g. `sens-om-35M`, `sens-om-140M`) so record keys do not read as 40 M and 100 M.
4. **[note] L3, L7 and L8 inherit 80,893,344 USD2004/year, which is arithmetic on 77.6 itself.** Any closure on those rungs is partly circular. The basis labels it target-derived; the reading must carry that label on every rung containing it.
5. **[note] Config cites "Lyon Table IV" for 1000 MW net.** The named images support 1000 MW through Table VII (p716, "1-GW(electric)") and the p707 constraint text; Table IV was not among the evidence I was given.
6. **[note] Dependencies on the sealed base that the named files cannot verify.** L2 has no design of its own and relies on the branch default net of 1000 MW; § 4 asserts `pbli_recovery` 0 but the config does not set it.
7. **[note] Wording against the pages.** p707 says O&M "include a factor 0.85" without the phrase cost-credit; p709 says 75 M$ "for each time", not "≈ 75". No effect on the study.

## Checks performed

**Source fidelity (§ 1).** Every `[SOURCE]` cell is supported: year-2004 dollars and 77.6 mills/kWh (p707 Table III title; p716 Table VII); 1 GW net, 1253 gross, 2436 MW fusion, 43.0 % (p716); Eq. 7 denominator `8760 P_e,net f_avail N_FPY` with 85 % availability and N_FPY = 40 full-power years (p707), 40 full-power years repeated on p709; direct × 1.93 covering construction services, engineering, owner's cost, contingencies, interest and escalation (p707); the borrowed-capital rate unstated (p709); Table III parents sum to 2619.572 (recomputed), rounded to 2620 in Table VII; fuel named as deuterium (p707); O&M 14 % with the 0.85 factor (p707); 842 t, 75 M$ per event, 14 − 1 = 13 replacements, 966 M$ replaced components (p709, p716); D&D 0.5 mills/kWh in 1992 dollars (p707).

**Derivations (§ 1, § 4).** 40/0.85 = 47.059 → 47 (39.95 FPY). Interval 2.907407/0.85 = 3.42048; n = max(0, ceil(N/τ) − 1) as WI-091 design.md line 34: 11 at 40 years, 13 at 47. 75,000,000/72,231,350 = 1.038330309484732, identical to the config. 77.6 × 0.14 × 7,446,000 = 80,893,344. 5 × 1468.361/1948.8 = 3.7673466 (config 3.7673466400 differs at the eighth figure, from unrounded neutron powers). NTU 4 → 19 (× 4.75), × 1700/1400 = 1.214, UA proxy 5.77 ≈ 5.8. Also confirmed: 6,634,398 MWh/year; 2,619,572,000 × 1.93 = 5,055,773,960; 2619.603 + 300 + 6.083 = 2925.686; 1.05³ = 1.1576; 6 events at 5 FPY; the 138.730 kg/year makeup scales from the baseline's 104.668 by exactly the neutron-power ratio 1.3272 with decay held.

**Tolerances (§ 3).** Fixed numeric thresholds (1e-9 relative, named absolute tolerances, 0.1 and 1.0 USD2004/MWh, 10 MUSD, ±15 MW inherited). The material rule demands explain, bound or mark unresolved; nothing is phrased relative to an observed residual. § 3 is sound; the only relaxation route found is finding 2, in § 2.

**Configuration honesty (§ 4, config).** All 21 axes are `framing: sensitivity` with fixed fan-out values; none derives capacity from demand (MR-7); every `diag-L*` and `diag-estimate-mode-1` classification begins "DIAGNOSTIC"; both `adverse-*` controls are present; the he-pump 3359 = operating flow is disclosed in the adverse classification (audit item 4). Every § 4 value appears in a design with the same numbers, including both-scenario coverage for tritium price and availability, the 2.0 cycle-side corner setting the four correlated factors, and the L8 rates. The recuperator, cycle-side and PbLi bounds trace to audit items 1, 2 and 6.

**Comparison discipline.** `alt-canonical-*` and `alt-unscaled-*` carry only their canonical base plus, for feed100, `new_feed` 100 and `supply_service` 30 M. No sens-* design sets `source_net_power` or any published total. `source_net_power` is set only on `diag-L1-*` and `diag-L7-*-at-our-net`.

## Not checked

The sealed input stores and what the `source_finance` branch substitutes beyond capital and denominator; the 1.49 overnight composition (1.2 × 1.2 + 0.05 is one consistent reading) and the 2,925.686 decomposition against the study record; the 0.3907 efficiency; the manifest's six absolute tolerances; the E/F register labels in WI-090/WI-091.

## Missing evidence

None that blocks execution once findings 1–3 are applied.
