# Anchor A — 1costingFE handshake: the criterion-3 verdict (A-4 form)

**Generated from an executed run** by `build_verdict_report.py`; 1costingFE commit `0254385` (pin `0254385`).
Work item WI-029 (STELLARATOR-DEMO Item 4). Supersedes the Jul-18 report wholesale.

Handshake point: stellarator DT, net_electric 1000.0 MW, availability 0.9, lifetime 30 yr, construction 8.0 yr, interest 0.07, inflation 0.02, NOAK, n_mod 1.

## Verdict

### (1) Per-account A-2 pass table (|rel dev| vs 1cfe float32, bar 1e-6)

Every modeled account at the handshake point, fed 1cfe's own inputs.

| account | CAS | 1cfe | model | rel dev | A-2 |
|---|---|---:|---:|---:|---|
| magnet | C220103 | 2,129.9527 M$ | 2,129.9527 M$ | -5.44e-10 | PASS |
| heating | C220104 | 158.4870 M$ | 158.4870 M$ | +0.00e+00 | PASS |
| divertor | C220108 | 100.7406 M$ | 100.7406 M$ | -6.49e-09 | PASS |
| blanket | C220101 | 570.4196 M$ | 570.4196 M$ | +7.29e-08 | PASS |
| shield | C220102 | 333.2815 M$ | 333.2815 M$ | +7.26e-08 | PASS |
| structure | C220105 | 25.5236 M$ | 25.5236 M$ | -4.51e-08 | PASS |
| vessel | C220106_vessel | 87.5907 M$ | 87.5907 M$ | +5.48e-08 | PASS |
| power_supplies | C220107 | 81.4013 M$ | 81.4013 M$ | +2.66e-08 | PASS |
| turbine | CAS23 | 228.7282 M$ | 228.7283 M$ | +9.02e-08 | PASS |
| electric | CAS24 | 97.4271 M$ | 97.4271 M$ | +4.40e-08 | PASS |
| heat_rejection | CAS26 | 98.8367 M$ | 98.8367 M$ | +9.99e-08 | PASS |
| misc | CAS25 | 59.3020 M$ | 59.3020 M$ | +3.55e-08 | PASS |
| remote_handling | | 151.8721 M$ | 151.8721 M$ | -3.23e-08 | PASS |
| installation | | 509.5986 M$ | 509.4977 M$ | -1.98e-04 | MISS |
| coolant | | 202.0452 M$ | 202.0452 M$ | +1.62e-08 | PASS |
| aux_cooling | | 18.9210 M$ | 18.9210 M$ | -2.92e-08 | PASS |
| waste | | 5.5254 M$ | 5.5254 M$ | +7.60e-08 | PASS |
| fuel_handling | | 120.0000 M$ | 120.0000 M$ | -5.21e-08 | PASS |
| other_rpe | | 11.5000 M$ | 11.5000 M$ | +2.86e-09 | PASS |
| inc | | 73.8488 M$ | 73.8489 M$ | +7.95e-08 | PASS |
| owner | | 41.2000 M$ | 41.2000 M$ | +3.51e-08 | PASS |
| supplementary | | 578.5841 M$ | 578.5480 M$ | -6.24e-05 | MISS |
| idc (CAS60, reported) | | 2,223.6880 M$ | 2,223.3838 M$ | -1.37e-04 | MISS |
| cas71 (levelized O&M) | | 79.0036 M$ | 79.0036 M$ | +1.08e-07 | PASS |
| cas72 (levelized repl.) | | 82.2300 M$ | 82.2300 M$ | +5.22e-07 | PASS |
| cas70 (= 71 + 72) | | 161.2336 M$ | 161.2337 M$ | +3.19e-07 | PASS |
| cas80 (levelized fuel) | | 0.7691 M$ | 0.7691 M$ | +1.03e-07 | PASS |
| cas90_1cfe (Option ii) | | 813.5873 M$ | 813.4759 M$ | -1.37e-04 | MISS |
| lcoe_1cfe (Option ii) | | 123.7430 $/MWh | 123.7289 $/MWh | -1.14e-04 | MISS |
| buildings (CAS21) [SysML fwd@1cfe-pwr] | | 619.4355 M$ | 619.4354 M$ | -7.50e-08 | PASS |
| preconstruction (CAS10) [SysML fwd@1cfe-pwr] | | 18.5000 M$ | 18.5000 M$ | +7.25e-09 | PASS |
| special_materials (CAS27) [design-input] | | 20.7879 M$ | 20.7879 M$ | +0.00e+00 | PASS |

**Newly brought under the handshake by WI-029** — all four forward-computed accounts pass:
- `cas71 (levelized O&M)` — 1cfe 79.00362 M$/yr, model 79.00363 M$/yr, rel +1.08e-07 — **PASS**
- `cas72 (levelized repl.)` — 1cfe 82.22999 M$/yr, model 82.23003 M$/yr, rel +5.22e-07 — **PASS**
- `cas70 (= 71 + 72)` — 1cfe 161.23361 M$/yr, model 161.23366 M$/yr, rel +3.19e-07 — **PASS**
- `cas80 (levelized fuel)` — 1cfe 0.76907 M$/yr, model 0.76907 M$/yr, rel +1.03e-07 — **PASS**

CAS72 is forward-computed on the WI-022 handwritten rung (the `ceil` in `n_rep` breaks the codegen arithmetic envelope), with every 1cfe guard carried verbatim in both the impl and its independent oracle mirror; the two agree at rel 0.0 and the guards are proven live on synthetic inputs. n_rep = 4 at this point, computed every run, never frozen.

### (2) Full signed-magnitude remainder itemization

| # | remainder | 1cfe | model | signed gap | reason |
|---|---|---:|---:|---:|---|
| R1 | C220106_pump (vacuum-pumping sub-account) | 0.7206 M$ | structurally absent | **-0.7206 M$** | The model's vessel calc is the shell term only. Documented WI-028 simplification, explained-and-kept. |
| R2 | headline IDC convention (Option ii) | multiplier 1.282475 (uniform-spend closed form) | multiplier 1.310796 (even-spend midpoint) | **+17.9639 M$/yr** on the annual capital charge (+2.208%) | A genuine convention choice, ruled Option (ii) by the owner 2026-07-25: the model's DCF headline convention is kept and the difference is reported, not closed. Applies to the HEADLINE channel only. |

**Closed this item, no longer remainders:**
- **CAS10 — closed AS ERROR.** One mis-set binding (`precon_fixed_base` carried FOAK `plant_studies` 20.0 in a NOAK plant). Fixed 32 M$ -> 16 M$; the model now reconstructs 1cfe's CAS10 exactly: 1cfe 18.500000 M$, model 18.500000 M$, **residual 0.000000 M$** (rel +7.25e-09, 1cfe's float32 emission and the injected p_net's own residue). The owner stop condition did not fire.
- **CAS72 — left the remainder.** Was $82.230M/yr structurally absent; now forward-computed and under A-2.

R1 is a capital-side remainder, so it propagates into every downstream capital line. Its propagation factor through the WI-028 assembly is 1.14 (installation) x [1 + CAS30 0.20x(8/6) + CAS50 shipping 0.015 + tax 0.01 + insurance 0.015x(1+0.20x(8/6))] = 1.494160, giving an overnight gap of -1.0767 M$ against the executed -1.0770 M$.

The 1cfe-form comparison channel `cas90_1cfe` misses A-2 at -1.37e-04 for exactly this reason and no other: trap 5 shows it reconstructs from the model's own overnight capital and CAS60 reported line at rel 0.0, so the formula is exact and the deviation is entirely the inherited R1 propagation.

### (3) Reconciliation arithmetic (shown, not asserted)

Two LCOE channels coexist by design under the ruled Option (ii). Both reconcile.

**Channel A — the 1cfe-form comparison channel `lcoe_1cfe`** (the like-for-like handshake compare):

```
  residual gap   = model 123.728888783  -  1cfe 123.743011475   =  -0.014122691 $/MWh

  itemized sum   = (CAS90_1cfe gap + CAS70 gap + CAS80 gap) x 1e6 / annual energy
                 = (-0.111349858 +0.000051486 +0.000000080) M$/yr x 1e6 / 7,884,000.481 MWh/yr
                 = -0.014116982 $/MWh
                 where CAS90_1cfe gap = CRF 0.080586404 x (1 + f_idc 0.282475321) x overnight gap -1.077015 M$
                       overnight gap  = -1.494160 x C220106_pump 0.720613 M$   (R1)

  residual       = -0.014122691  -  -0.014116982  =  -5.709e-06 $/MWh
                 = 4.61e-08 relative to LCOE     <= 1e-6   CLOSES
```

**Channel B — the model's DCF headline `lcoe`** (the design-point convention, unchanged):

```
  residual gap   = model 126.007408764  -  1cfe 123.743011475   =  +2.264397289 $/MWh   (+1.830%)

  itemized sum   = (IDC-convention line + CAS90_1cfe gap + CAS70 gap + CAS80 gap) x 1e6 / annual energy
                 = (+17.963853456 -0.111349858 +0.000051486 +0.000000080) M$/yr x 1e6 / 7,884,000.481 MWh/yr
                 = +2.264403104 $/MWh
                 where the IDC-convention line (R2) = CRF 0.080586404 x overnight 7,871.0726 M$ x (1.310796 - 1.282475)
                                                    = +17.963853 M$/yr = +2.278520 $/MWh (~+1.84% on LCOE)

  residual       = +2.264397289  -  +2.264403104  =  -5.815e-06 $/MWh
                 = 4.70e-08 relative to LCOE     <= 1e-6   CLOSES
```

The leftover in each channel is the float32 A-2 residue of the accounts themselves (1cfe emits float32; the model computes float64) — it is smaller than the 1e-6 aggregate tolerance by more than an order of magnitude.

### (4) Criterion-3 verdict

**MET.**

The bar (owner ruling, 2026-07-18) is *explaining* the end-to-end LCOE gap, and closing any errors found. Both halves hold at the handshake point:

- **Every account the model carries is under A-2 or itemized with a signed magnitude.** The four accounts WI-029 brought in — CAS71, CAS72, CAS70, CAS80 — all pass at 1e-6 (yes). The accounts that miss (`installation`, `supplementary`, `idc`/CAS60, `cas90_1cfe`, `lcoe_1cfe`) miss *only* by the propagation of the single itemized capital remainder R1, each with a reconstruction trap proving the formula itself is exact.
- **The remainder is fully itemized and reconciles.** Two lines: R1 C220106_pump (a modeled simplification) and R2 the headline IDC convention (a ruled choice, kept deliberately). The residual end-to-end gap equals the itemized sum in both LCOE channels, within 1e-6 relative.
- **The one error found was closed.** CAS10's +$16.0M/+86.5% divergence resolved to a single mis-set FOAK constant and now reconstructs 1cfe exactly.

No structural gap remains unexplained. There is no third state: this is met, not partially met.

### Note on the two coexisting LCOE channels

- **Headline (design point): `lcoe_calc` — the DCF core.** Keeps `idc_factor = (1+d)^(Yc/2)` = 1.310796 and `total_capital = overnight_capital` (CAS60 excluded, Item-3 Option C). This is the model's own LCOE and it is what the design-point run reports.
- **Comparison: `lcoe_1cfe` — 1costingFE's financing form.** `CRF x (overnight + CAS60)` reusing the Item-3 CAS60 reported line, over the same denominator. Compared under A-2 at the handshake point. **Not** the design-point headline.

Trap 5 asserts on every run that the headline `idc_factor` is unchanged and that `total_capital == overnight_capital`, so CAS60 cannot enter the headline capital base — the two channels cannot double-count.

### Trap table (A-5) — every new mapping asserted

| trap | result | detail |
|---|---|---|
| fuel-keyed bases (DT) | PASS | remote_handling=150, fuel=120, owner=41.2, spares=0.03, startup=40, decom=272 |
| plant-total/per-module + ref-power split (clean accounts @ 1e-6) | PASS | 8 remainder-free tail/CAS40 accounts under 1e-6 => power/ref/base mapping correct |
| installation base = 0.14*Sigma(C220101..110) [+ pump A-4] | PASS | installation reconstructs to 1cfe with +0.14*C220106_pump: rel -3.12e-08 |
| F-2/F-3 structural (cas28=5.0; cas20/cas30 reconstruct) | PASS | cas28=5.0; cas20 recon rel -2.01e-08; cas30 recon rel -1.38e-07 |
| CAS60 Option C (total==overnight, idc reported-only) | PASS | total_capital vs overnight_capital rel 0.00e+00; idc line reported separately |
| WI-029/1 levelization params (g=0.02, Tc=8 NOAK, i=0.07, n=30) + 1.439 factor | PASS | g=0.02, Tc=8.0 (NOAK, not 10), i=0.07, n=30; cas71/annual_om = 1.43905 |
| WI-029/1b handshake-point O&M base = 54.900 M$/yr (NOT the design-point 52.517) | PASS | 1cfe annual_om 54.900002 M$/yr @ p_net=1000; model 54.900002 M$/yr, rel +0.00e+00 |
| WI-029/2 CAS72 chain (set {C220101,C220108}, fluence 18.0, n_rep=4, clip inert) | PASS | q_n=3.12851 MW/m2, FPY=5.75353 in [0.5, 27.0] (clip inert), cal=6.39282, n_rep=4, cost_per_event=671.160 M$ |
| WI-029/3 fuel constants (cost_per_rxn = M_D*u_D + M_Li6*u_Li6; Q_DT=17.58; burn x1.19) | PASS | cost_per_rxn=1.726064e-23 $/rxn, q_eff=17.58, burn correction x1.1900 |
| WI-029/4 availability 0.9 injected over model 0.85 -> CAS72 cal AND LCOE denominator | PASS | cas72_calc.availability=0.9, lcoe_calc.availability=0.9, lcoe_1cfe_calc.availability=0.9 (model instance binding is 0.85) |
| WI-029/5 IDC Option (ii): cas90_1cfe = CRF*(overnight+CAS60); headline idc_factor unchanged; total_capital == overnight (CAS60 excluded) | PASS | cas90_1cfe reconstructs from the CAS60 reported line: rel +0.00e+00; headline idc_factor 1.310796 = (1+d)^(Yc/2) UNCHANGED (1cfe f_idc form is 1.282475); total_capital == overnight_capital, so CAS60 cannot enter the headline base |

---

PROTOCOL: `knowledge/holdout/aries-cs/PROTOCOL.md` §3 barred paths were not read at any stage of WI-029. The C220107 power-supplies sub-account remains the footnoted ARIES-CS-derived value in the 1costingFE lineage exception.
