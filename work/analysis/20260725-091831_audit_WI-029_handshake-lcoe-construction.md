# Audit — WI-029 Handshake LCOE construction: CAS70/80 + IDC (STELLARATOR-DEMO Item 4)

**Scope:** work item audit, `work/active/WI-029_handshake-lcoe-construction/`
**Commits audited:** `31161dbe` (G-8 re-baseline), `f22bd288` (implement work); stage log at `0c8740ce`
**Auditor session:** fresh — every claim reproduced from an executed run, nothing inherited from the Implementation Record
**Date:** 2026-07-25
**Overall verdict: POSITIVE.** All nine audit bars pass. Six minor findings, none affecting the criterion-3 verdict. **The criterion-3 (Anchor A) verdict MET is confirmed.**

---

## Executive summary

The item claims to finish demo criterion 3, so the audit weighted the verdict arithmetic hardest: the A-4 reconciliation was recomputed from the raw run outputs by an independently written script, not read from the report.

Everything reproduces. The handshake re-run at the pin regenerated `handshake_comparison.json` **byte-identical** to the committed baseline, and `build_verdict_report.py` regenerated `HANDSHAKE_REPORT.md` **byte-identical** to the committed one — so the artifact is demonstrably a function of the executed run, not hand-typed. The design point reproduces to the cent. The two-cause LCOE attribution was verified arithmetically from first principles and closes exactly. The CAS10 diagnosis was verified at the 1cfe source at the pin: `plant_studies_foak: 20.0` vs `plant_studies_noak: 4.0` is precisely the $16.0M, and the fix is exactly one binding value in each tree.

| bar | subject | verdict |
|---|---|---|
| 1 | Handshake A-2 table + trap-5 exactness | **POSITIVE** |
| 2 | A-4 verdict arithmetic, both channels | **POSITIVE** |
| 3 | CAS10 closure and the bounded fix | **POSITIVE** |
| 4 | CAS72 handwritten rung, guards, mirror, preservation | **POSITIVE** |
| 5 | Design point, oracle, headline attribution | **POSITIVE** |
| 6 | Two-tree mirroring, snapshot provenance, codegen adaptations | **POSITIVE** |
| 7 | G-8 commit scope; comparison logic and DCF untouched | **POSITIVE** |
| 8 | Standing bars | **POSITIVE** |
| 9 | MR-4 / MR-3 spot-check | **POSITIVE** |

**Environment verified before executing.** `sysml-codegen-wi029-pin` @ `06d95f854f30f77f1a7c93f9c0f13be878765165`; `teax-wi029-pin` @ `07eb0accd4852742a6da1820a05a4cae4fe707df`; `agentic-mbse-wi029-pin` @ `4c18d616f77e26932a8e158cefc2637db47f9b07`; `1costingfe` main checkout @ `02543850089be175ea7c28b92a8b2a4184e1637e` (== pin `0254385`, clean). Exec interpreter `~/1cfe/fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python` (Python 3.12.3) — confirming Implementation-Record Finding 2, the venv is gitignored and lives only in the main checkout. License sourced from `~/1cfe/fusion-tea/.env`. Repo tracked tree clean at `0c8740ce` (only `.orchestrate-logs/` untracked).

**PROTOCOL.** No path under `knowledge/holdout/` was read, opened, listed, or cited at any point in this audit. §3 quarantine sealed.

---

## Bar 1 — Handshake re-run and the A-2 table — POSITIVE

Executed `handshake_1costingfe.py` at the pin. Every claimed figure reproduces exactly.

| channel | 1cfe $ | model $ | rel dev | claimed | A-2 |
|---|---:|---:|---:|---|---|
| `cas71` levelized O&M | 79,003,623.96 | 79,003,632.50 | **+1.08e-07** | +1.08e-07 | PASS |
| `cas72` levelized replacement | 82,229,988.10 | 82,230,031.05 | **+5.22e-07** | +5.22e-07 | PASS |
| `cas70` = 71 + 72 | 161,233,612.06 | 161,233,663.55 | **+3.19e-07** | +3.19e-07 | PASS |
| `cas80` levelized fuel | 769,069.73 | 769,069.81 | **+1.03e-07** | +1.03e-07 | PASS |
| `cas90_1cfe` (Option ii) | 813,587,280.27 | 813,475,930.42 | **−1.37e-04** | −1.37e-04 | MISS (inherited) |
| `lcoe_1cfe` (Option ii) | 123.743011 | 123.728889 | **−1.14e-04** | −1.14e-04 | MISS (inherited) |

All four forward-computed accounts pass at 1e-6 with three-to-ten times headroom over the ~1e-7 float32 floor A-2 establishes as [HARD].

**Trap 5 — the exactness claim holds.** Executed detail line: `cas90_1cfe reconstructs from the CAS60 reported line: rel +0.00e+00`. The channel's own arithmetic is exact; the −1.37e-04 is entirely inherited. Cross-checked independently: `crf × (1 + f_idc) × overnight_gap = −0.111310 M$/yr` against the measured `cas90_1cfe` gap of `−0.111350 M$/yr` — agreeing to 3.6e-04 of the gap itself, i.e. the miss is R1-propagation to within the accounts' own float32 residue. Trap 5 also confirms `idc_factor = 1.310796 = (1+d)^(Yc/2)` unchanged and `total_capital == overnight_capital` at rel 0.00e+00, so CAS60 cannot enter the headline base. The double-count hazard is genuinely closed.

**Determinism.** `git diff` after the re-run is empty — the regenerated `handshake_comparison.json` is byte-identical to the committed G-8 baseline.

All 11 traps assert-pass (see Finding F3 on the recorded tally).

---

## Bar 2 — THE VERDICT ARITHMETIC — POSITIVE

This bar was audited by writing an independent reconciliation script (`/tmp/aud_recon.py`) that reads only `onecfe_point.json` and `handshake_comparison.json` and recomputes both channels from scratch. Results:

```
crf = 0.080586404   1 + f_idc = 1.282475   idc_factor = 1.310796   energy = 7,884,000.481 MWh/yr
R1 pump = -0.7206 M$        R2 IDC convention = +17.963853 M$/yr  (+2.208%)
gaps M$/yr:  cas90_1cfe = -0.111349858   cas70 = +0.000051486   cas80 = +0.000000080

Channel A (1cfe-form):  gap = -0.014122691   itemized = -0.014116982
                        residual = -5.709e-06 $/MWh = 4.614e-08 relative to LCOE   <= 1e-6  CLOSES

Channel B (DCF headline): gap = +2.264397289 (+1.830%)   itemized = +2.264403104
                        residual = -5.815e-06 $/MWh = 4.699e-08 relative to LCOE   <= 1e-6  CLOSES
```

Every claimed figure matches to the last printed digit: gap −0.014123 (A), gap +2.264397 with R2 +17.9639 M$/yr (B), residuals 4.61e-08 / 4.70e-08. **Both channels close, more than an order of magnitude inside the A-4 aggregate tolerance.**

**Remainder is exactly two lines.** `HANDSHAKE_REPORT.md:61-62` carries R1 and R2 and nothing else (`grep -c '^| R'` → 2). R1 = `C220106_pump` −0.7206 M$, explained-and-kept. R2 = the headline IDC convention +17.9639 M$/yr, kept per the ruled Option (ii). CAS10 closes as error; CAS72 leaves the remainder. R1's propagation factor 1.494160 predicts an overnight gap of −1.0767 M$ against the executed −1.0770 M$ — independently recomputed and confirmed.

**The report is generated, not hand-typed.** Re-ran `build_verdict_report.py`: the regenerated `HANDSHAKE_REPORT.md` is **byte-identical** to the committed file (`diff` empty). Reading the generator confirms it: it opens the two run JSONs at lines 12-13 and every number in the output is an f-string interpolation of a value read from them or derived from `target`. There is no hardcoded result anywhere in its 230 lines.

**Verdict MET follows from the ratified A-4 dual condition** — with one reading recorded honestly as Finding F1 below. Condition (2) holds outright: the remainder is fully itemized with signed magnitudes and reconciles in both channels. Condition (1) holds under the report's phrasing "every account the model carries is under A-2 **or** itemized with a signed magnitude," which is the only self-consistent reading of A-4 (see F1).

---

## Bar 3 — CAS10 — POSITIVE

**Reproduced.** Executed gate: 1cfe CAS10 = 18.500000 M$, model = 18.500000 M$, residual = 0.000000 M$, rel +7.25e-09. PASS; the owner stop condition did not fire.

**The fix is exactly one binding, both trees.** `git diff 0ddf15b9..f22bd288` over both `stellarator_plant.sysml` copies shows a single numeric change in each:

- `models/designs/stellarator_09/stellarator_plant.sysml` — `precon_fixed_base = 32000000.0` → `16000000.0`
- `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml` — identical change

Every other line in the diff is doc-comment text. No second numeric value moved anywhere in the CAS10 chain.

**The diagnosis is verified at the source, not taken on trust.** `1costingfe/src/costingfe/data/defaults/costing_constants.yaml:14-20` at the pin:

```
site_permits: 3.0    plant_studies_foak: 20.0    plant_studies_noak: 4.0
plant_permits: 2.0   plant_reports: 1.0          other_precon: 1.0
```

NOAK adders = 3 + licensing_dt 5 + 2 + **4** + 1 + 1 = **16.0 M$**; the FOAK reading substitutes 20.0 for 4.0 → 32.0. The delta is exactly $16.0M, which is precisely what the WI-025 binding carried. `costs.py:52-80` confirms the structure (`studies = cc.plant_studies_noak if noak else cc.plant_studies_foak`) and that contingency is `contingency_rate(noak) * subtotal`, zero at NOAK — so the doc amendment retiring the stale "× 1.10" FOAK note is correct and changes no number. This is a single clean error under an unambiguous basis. The stop condition was correctly not fired.

**The self-correction is what the record says and is bounded to the gate.** The Implementation Record (`plan.md:573`) states the closure gate was first coded with a dollars-absolute 1e-6 bar and corrected to the project's A-2 relative bar. Verified: the change lives in `handshake_1costingfe.py`'s gate check only. No model file carries a tolerance. The residual in M$ is 0.000000 either way — the correction changed the yardstick to the specified one, not the number. On precision, see Finding F5.

---

## Bar 4 — CAS72 handwritten rung — POSITIVE

**Both files read in full.** All three guards are present as executable code in both:

| guard | impl (`levelized_replacement_cost_impl.py`) | oracle mirror (`verify_stellaris.py:142-165`) |
|---|---|---|
| inner `max(q_n, 1e-6)` | `fluence_limit / max(q_n, 1e-6)` | `fluence_limit / max(q_n, 1e-6)` |
| `clip(·, 0.5, n·avail)` | `_clip()` = `min(max(v, lo), hi)`, jnp order | `min(max(fpy_raw, 0.5), fpy_cap)` |
| outer `max(0, ceil(n/t) − 1)` | `max(0.0, float(math.ceil(n/cal)) − 1.0)` | `max(0.0, float(math.ceil(n/cal)) − 1.0)` |

`n_rep` is computed live in both — it is a local expression, not a function parameter and not a defaulted input.

**The mirror is genuinely independent.** `verify_stellaris.py` imports only `math`. It does not import the impl, does not import the generated package, and does not read `handshake_comparison.json` or any pipeline output — it recomputes the whole plant chain from the `IN` dict of design-point bindings (`verify_stellaris.py:49`). The rel-1e-9 assert is not vacuous.

**Reproduced from an executed run:** `cas72_annual exec=95399746.500496805 oracle=95399746.500496805 reldev=0.00e+00`.

**Guard-live synthetic checks re-run — all three PASS:**

| case | guard proven live | impl | mirror | rel |
|---|---|---:|---:|---:|
| clip cap | raw FPY 4126.668 > cap 27.000 | 0.000000 | 0.000000 | 0.00e+00 |
| clip floor | raw FPY 0.07428 < floor 0.500 → n_rep 53 | 1,219,445,700.972802 | 1,219,445,700.972802 | 0.00e+00 |
| outer max | n_rep floored to 0 → cost exactly 0.0 | 0.000000 | 0.000000 | 0.00e+00 |

The floor case is load-bearing (a guard binds *and* the result is non-zero), so the agreement is a real comparison. The other two are separately asserted to saturate, not merely to agree.

**Preservation across regen — verified independently.** Copied the generated tree to `/tmp/aud_gen` and re-ran `sysml-codegen generate --from-snapshot ... --overwrite --preserve-handwritten` at pin `06d95f8`:

```
06fb1a6e37e46312ecab813241b810feea9cc56429a2cfeca6f16997d3af704c  levelized_replacement_cost_impl.py
8d23574793c34314c67b68b8e0f4ec438d3e2d9f92060eb4094a8d46c0794a9f  dt_fusion_power_impl.py
```

Both match the committed shas. The CAS72 standing hash `06fb1a6e…3af704c` and the WI-022 hash `8d2357…794a9f` are stable across a real regeneration.

**1cfe fidelity verified at source.** `economics.py:53-75` at the pin reads `s = (1+i)**(-t_replace)`, `n_rep = jnp.maximum(0.0, jnp.ceil(n/t) - 1.0)`, `pv = event_cost * s * (1 - s**n_rep)/(1 - s)`, `return pv * compute_crf(i, n)` — the impl and mirror are faithful term-for-term. `model.py:102-111` reads `jnp.clip(cc.fluence_limit(fuel) / jnp.maximum(q_n, 1e-6), 0.5, lifetime_yr * availability)` — matched exactly, including the clip ordering.

---

## Bar 5 — Design point — POSITIVE

Executed `run_stellaris_single.py`. Every anchor reproduces:

| anchor | executed | claimed |
|---|---:|---:|
| total capital $ | 16,129,706,216.036476 | 16,129,706,216.04 |
| LCOE $/MWh | 275.264220042 | 275.264220 |
| `lcoe_1cfe` $/MWh (comparison) | 269.861537710 | 269.861538 |
| p_net MW | 915.081087860 | 915.081088 (unchanged) |
| q_eng | 6.606661729 | 6.606662 (unchanged) |
| rec_frac | 0.151362373 | 0.151362 (unchanged) |

`VERDICT PARITY: PASS — headline=all_satisfied, assessed_count=5, all five == satisfied` (`beta_ok`, `net_positive`, `recirc_ok`, `tbr_ok`, `wall_load_ok`).

**Oracle 14/14, worst rel dev 4.13e-16** (bar 1e-9) — `BIT-EXACT vs oracle: PASS`. Channels: total_capital, lcoe, p_net, q_eng, rec_frac, cas20_capital, overnight_capital, cas71_annual, cas72_annual, cas70_annual, cas80_annual, annual_fuel, cas90_1cfe, lcoe_1cfe. The five WI-029 annual-cost channels and `annual_fuel` are all at exactly 0.00e+00.

**Independence confirmed** (see Bar 4) — the oracle re-derives the whole chain in pure Python from the SysML bindings and reads no pipeline output.

**Two-cause attribution verified arithmetically, not accepted.** Recomputed from first principles at the design point (energy = 8760 × 915.081088 × 1 × 0.85 = 6,813,693.780 MWh/yr):

- CAS10 component = `crf × idc_factor × 16e6 / energy` = `0.105632 × 16e6 / 6,813,693.780` = **−0.248047 $/MWh** — matches the claim exactly.
- Observed move = 275.264220042 − 258.013640 = **+17.250580 $/MWh**.
- Implied annual-cost component = 17.250580 + 0.248047 = **+17.498627 $/MWh** — matches the claim exactly.
- Back-solving the implied pre-item annual O&M from the new CAS70+CAS80 gives **$52,517,267**, which is the WI-028 unlevelized O&M line to the dollar.

That last check is the one that makes the attribution non-circular: it independently confirms the annual-cost component is exactly the replacement of the old unlevelized O&M line by CAS70+CAS80, with nothing else in it. **Two causes, no third**, confirmed.

---

## Bar 6 — Two-tree mirroring, snapshot provenance, codegen adaptations — POSITIVE

**Mirroring — region-identical, only the two sanctioned deltas.** Direct `diff` of every edited file between `models/` and the staged twin under `exploration/stellarator_e2e/models/`:

| file | result |
|---|---|
| `library/analyses/mfe_account_costs.sysml` | byte-identical (whole file) |
| `library/analyses/mfe_lcoe_dcf.sysml` | byte-identical (whole file) |
| `designs/stellarator_09/stellarator_plant.sysml` | byte-identical (whole file) |
| `designs/generic_mfe/mfe_plant.sysml` | differs only at lines 402-406 and 564 — both the known Item-10 comment blocks |

No other delta anywhere.

**Snapshot provenance = the staged tree, proven by reproduction.** Recaptured a snapshot from the absolute staged models path at pin `06d95f8` into `/tmp/aud_regen.snapshot.json` and compared against the committed `stellarator.snapshot.json`. **The only differing top-level key is `captured_at`.** `constraint_facts` compare equal; `constraint_lowering_mode` is still `applied`. A snapshot captured from the canonical tree could not reproduce the staged one byte-for-byte given the Item-10 comment deltas — so this simultaneously establishes provenance and the regen-stability standing bar.

**Codegen adaptations — spot-checked against the oracle mirror.** Two checked in detail, both value-preserving:

- **Adaptation 1** (move `p_neutron = p_fus × (1 − ash_frac)` inside `'Levelized Replacement Cost'`): the def computes `p_neutron` on `mfe_account_costs.sysml:809` with the identical expression and operand order; the oracle mirror computes `p_neutron = p_fus * (1.0 - ash_frac)` at `verify_stellaris.py:154`. `cas72_annual` grades at rel **0.00e+00**.
- **Adaptation 2** (`'Annual Cost Rollup'` producing `cas70 = cas71 + cas72` and `annual_total = cas71 + cas72 + cas80`): pure addition, same terms and order; the oracle computes `cas70_annual = cas71_annual + cas72_annual` and `annual_om = cas70_annual + cas80_annual`. Both `cas70_annual` and `cas80_annual` grade at rel **0.00e+00**.
- Spot-checked further: **adaptation 3** (`'1cfe-Form Capital Charge'`, `cas90 = crf × (overnight_cost + idc_cost)`) grades at 2.86e-16 and is separately asserted by trap 5 at rel 0.00e+00.

The `crf` promotion from plain attribute to `out` attribute is a visibility change only — it is computed from the same `discount_rate` / `operational_years` and, critically, avoids restating CRF (see Bar 7: `mfe_lcoe_dcf.sysml` is untouched).

---

## Bar 7 — G-8 — POSITIVE

- **`31161dbe` touches only the comparison JSON.** `git show --stat` → `exploration/stellarator_e2e/handshake_comparison.json | 84 ++++--`, **1 file changed**, 78 insertions / 6 deletions. Nothing else in the commit.
- **Comparison logic unchanged vs the pre-item state (`0ddf15b9`).** `handshake_1costingfe.py` diff is **139 insertions, 1 deletion**. The single deleted line is the trap-section print header (`"--- WI-028 D6 traps (A-5) ---"` → `"--- WI-028 D6 + WI-029 D4 traps (A-5) ---"`). The `rel(a, b)` helper and the row-loop machinery are byte-unchanged; the additions are channels, injected inputs, rows, the CAS10 gate and the six traps.
- **`mfe_lcoe_dcf.sysml` untouched vs the pre-item state, in both trees.** `git diff 0ddf15b9 f22bd288 --stat` over both copies is empty. This is the trap-5 and Option-(ii) requirement, and it holds structurally, not just by assertion.

---

## Bar 8 — Standing bars — POSITIVE

| bar | result |
|---|---|
| WI-022 sha256 | `8d23574793c34314c67b68b8e0f4ec438d3e2d9f92060eb4094a8d46c0794a9f` — intact, and stable across an audit-run regen |
| CAS72 impl sha256 (new standing hash) | `06fb1a6e37e46312ecab813241b810feea9cc56429a2cfeca6f16997d3af704c` — stable across regen |
| IFE Run A | LCOE **252.29996307**, f_recirc 0.04166667 — byte-exact |
| IFE Run B | LCOE **68.69020165**, f_recirc 0.08333333 — byte-exact |
| IFE Run C | raises `PipelineValidationError` on `hif_plant_pkg__hif_plant__meier_reactor_cost_calc.thermal_power_gw` — exactly the recorded skew; out-of-scope per [OWNER] ruling 2026-07-20. `git diff 0ddf15b9 f22bd288 -- exploration/ife_e2e/` is **empty**, so WI-029 provably did not cause it |
| pytest `tests/models/ -q` | **11 failed, 18 passed, 14 skipped** in 0.73s, 0 errors — the recorded tally |
| L1 | `agentic-mbse validate --level 1 models` → 22 files, **Errors 0, Warnings 0** |
| Regen stability | only `captured_at` differs (Bar 6) |
| MR-2-style grep | clean — see Bar 9 |
| SV-035 | row present at `VALIDATION_MATRIX.md:61`, status **`passing`**, 15 pipe-delimited fields matching SV-034's column count. Every executed figure in the row matches what this audit reproduced |

---

## Bar 9 — MR-4 / MR-3 spot-check — POSITIVE

**MR-3 — no concept literal in any new library def.** Read all six new calc defs in `mfe_account_costs.sysml` (`'Levelized Annual Cost'` :628, `'DT Fuel Cost'` :683, `'Levelized Replacement Cost'` :743, `'Annual Cost Rollup'` :853, `'1cfe-Form Capital Charge'` :872, `'1cfe-Form LCOE'` :899). Every concept-specific quantity — fuel chemistry, unit prices, fluence limit, replaceable-account cost, escalation rate, plant life, availability — is an `in attribute`. The only literals present are dimensionless mathematical constants and 1cfe's own guard bounds (`1e-6`, `0.5`, `8760.0`, `3600.0`, `1.0e6`). Clean.

**MR-4 — citations present and verified at the pin.** All six defs carry `**Source**` / `**Ref**` / `**Basis**` blocks. Seven new constants were traced to `1costingfe` at `0254385` and **six verified bit-exact**:

| constant | model value | 1cfe source at pin | match |
|---|---|---|---|
| `inflation_rate` (g) | 0.02 | `adapter.py:37` `inflation_rate: float = 0.02` | exact |
| `project_time` Tc | 8 (NOAK) | `costs.py:41-44` `_total_project_time` returns `construction_time` when NOAK | exact — confirms Tc = 8, not 8 + licensing |
| `fuel_cost_per_rxn` | 1.7260641119988767e-23 | `M_DEUTERIUM_KG × u_deuterium 2175.0 + M_LI6_KG × u_li6 1000.0` (`physics.py:17,21`, `costing_constants.yaml:282-283`) — recomputed = 1.7260641119988767e-23 | exact |
| `fuel_q_eff` | 17.58 | `physics.py:33` `Q_DT = 17.58` | exact |
| `mev_to_joules` | 1.6021766339999998e-13 | `physics.py:14,16` `_EV × 1e6` — recomputed = 1.6021766339999998e-13 | exact |
| `ash_frac` | 0.2002275312855518 | `E_ALPHA_DT 3.52 / Q_DT 17.58` (`physics.py:32-33`) — recomputed = 0.2002275312855518 | exact |
| `fluence_limit` | 18.0 | `costing_constants.yaml:153` `fluence_limit_dt: 18.0` | exact |
| `burn_fraction` / `fuel_recovery` | 0.05 / 0.99 | `defaults/steady_state_stellarator.yaml:64-65` | exact |

The Phase-3 `ash_frac` deviation is confirmed necessary: the def's rounded 0.2002 default would shift `q_n` by ~3.4e-05 relative, propagating through `core_lifetime_cal` into `s` — the exact constant is what keeps CAS72 under the 1e-6 A-2 bar.

**Formula citations verified against source, not just cross-referenced.** `economics.py:6-10` (CRF), `economics.py:13-50` (growing-annuity levelization: `a1 = annual_cost*(1+g)**Tc`, `pv = a1*(1-((1+g)/(1+i))**n)/(i-g)`, `return crf*pv`), `economics.py:53-75` (replacement closed form), `model.py:102-111` (the clip and inner max) — all read at the pin and all faithfully transcribed.

**Frontmatter plain.** `spec.md` frontmatter values contain no colons — the `pm close-item` crash precedent is avoided.

**Traceability matrix.** 11 rows added (3 calc defs + 8 instance bindings). See Finding F2.

---

## Findings

None of these changes the verdict. Ranked by significance.

### F1 — The verdict relies on a reading of A-4 condition (1), not its literal text *(surfaced, not a defect)*

A-4 as ratified (`.project/active/demo-anchor-acceptance-spec/spec.md:84`) states condition (1) as "**Every modeled account** … is under the A-2 per-account bar." Read literally, that fails: `installation` (−1.98e-04), `supplementary` (−6.24e-05), `idc`/CAS60 (−1.37e-04), `cas90_1cfe` and `lcoe_1cfe` are not under the bar.

`HANDSHAKE_REPORT.md` states it as "Every account the model carries is under A-2 **or itemized with a signed magnitude**." That is the only self-consistent reading of the spec — condition (2) explicitly provides for "every account that is **not** under the bar," and the A-4 Basis says a blanket bar must not "fail the whole comparison over an explained structural simplification." It also matches the [OWNER] criterion-3 ruling of 2026-07-18: the bar is *explaining*, and closing errors; full structural-gap closure is not required.

Supporting evidence that the reading is not being used to paper over anything: every misser traces to the single itemized R1 cause, each has a reconstruction trap proving its own formula exact (trap 5 at rel 0.00e+00 for `cas90_1cfe`; the installation trap at rel −3.12e-08), and the reconciliation closes in both channels at ~4.6e-08.

**Recommendation:** the owner should note at close that they are ratifying this reading. If it matters for the record, A-4(1) could be amended to read "every modeled account is under A-2 or itemized under (2)". No re-work is implied.

### F2 — Three new library calc defs have no traceability-matrix row

`'Annual Cost Rollup'`, `'1cfe-Form Capital Charge'` and `'1cfe-Form LCOE'` (`mfe_account_costs.sysml:853,872,899`) are absent from `data/traceability_matrix.csv` — `grep -c` returns 0. Only the three originally-designed defs got rows. All three carry complete `**Source**`/`**Ref**`/`**Basis**` doc comments, so MR-4 citation is satisfied; the gap is the matrix entry alone. They arrived late, as Phase-5 codegen adaptations, which explains the miss.

Relatedly, the CAS72 impl and its oracle mirror have no file-level rows — coverage is via the `'Levelized Replacement Cost'` calc_def row. The Implementation Record states this accurately (`plan.md:540`), but the Phase-6 checklist item reads "Add the impl + mirror to `data/traceability_matrix.csv`," which is only partly met.

**Recommendation:** add three rows at close. Two minutes of work; no model change.

### F3 — Recorded trap tally is 12; the actual count is 11

The Implementation Record (`plan.md:558`) and the SV-035 row both say "All twelve pass (six pre-existing WI-028 + six new WI-029)". The executed run prints and `handshake_comparison.json` stores **11** traps: five pre-existing WI-028 traps (fuel-keyed bases, plant-total/per-module + ref-power split, installation base, F-2/F-3 structural, CAS60 Option C) plus six new WI-029 traps (1, 1b, 2, 3, 4, 5). All 11 PASS. The tally is off by one on the inherited side; no trap is missing.

**Recommendation:** correct "twelve / six pre-existing" to "eleven / five pre-existing" in the plan record and the SV-035 row.

### F4 — `'Levelized Annual Cost'` drops two 1cfe guards, while CAS72 carries its guards verbatim

1cfe's `levelized_annual_cost` (`economics.py:44-48`) carries `pv_normal = a1 * (…) / (i - g + 1e-30)` and a `jnp.where(|i-g| < 1e-9, pv_equal, pv_normal)` L'Hôpital branch for `i == g`. The model's def (`mfe_account_costs.sysml:675-677`) writes `/ (interest_rate - inflation_rate)` with neither.

At the pinned points (i = 0.07, g = 0.02) both are inert and the A-2 results are unaffected — 1e-30 against 0.05 is a ~2e-29 relative perturbation. But it is the same class of guard the design's MF-1 explicitly forbade dropping on CAS72, and it is the one that goes live first in a study sweep: a sensitivity run with i ≈ g divides by ~0 and returns an infinity where 1cfe returns the finite limit.

**Recommendation:** either carry the two guards (which would route this def to the handwritten rung, as `where` is an invocation — a real cost) or record the omission explicitly in the def's doc comment as a documented divergence with its validity range. The doc comment currently claims the formula without noting the branch is absent. Worth a follow-up work item if the model is ever swept over discount rate.

### F5 — "residual 0.000000 M$" is a display rounding of 0.134 dollars

The CAS10 closure residual is `0.13404430821537971` dollars (`handshake_comparison.json` `cas10_closure.residual`), which prints as `0.000000` in M$ at six decimals. The rel figure `+7.25e-09` is stated alongside everywhere it appears, and the record explains it as 1cfe's float32 emission plus the injected `p_net = 1000.0001` residue through the sqrt land term — an order of magnitude inside A-2. Honest and disclosed; recorded only so the round phrase "residual 0.0" is not later mistaken for bit-exactness.

### F6 — One citation lacks a line number

The `inflation_rate` instance binding cites `**Ref**: adapter.py (inflation_rate = 0.02)` without a line. It is `adapter.py:37` (also `validation.py:93`). Every other new citation in the item carries line numbers. Trivial.

---

## PR-XXX / AD-XXX / MR-XXX

**MR-3** (library concept-agnostic) — PASS, evidence in Bar 9.
**MR-4** (structured citations resolving to real sources) — PASS, eight constants and four formula citations verified at the 1cfe pin; one line-number gap (F6), three matrix rows missing (F2).
**MR-WI029-1…11** — all satisfied. 1/3 (CAS71 + CAS80 forward-computed under A-2) Bar 1. 2 (CAS72 disposed — forward-computed, not remaindered) Bars 1, 4. 4 (IDC reconciliation ruled and implemented as Option ii) Bars 1, 2, 7. 5 (criterion-3 verdict in A-4 form with arithmetic shown) Bar 2. 6 (CAS10 error-to-close under the verbatim stop condition) Bar 3. 7 (region-identical both trees, snapshot from the staged tree) Bar 6. 8 (trap assertions for every new mapping) Bar 1, F3. 9 (design-point re-baseline, oracle bit-exact) Bar 5 — the spec's "total_capital unchanged" clause is correctly superseded and the supersession is recorded in three places. 10 (`handshake_comparison.json` re-baselined as its own commit, logic untouched) Bar 7. 11 (standing bars, SV-035) Bar 8.

**SV-035** — evaluated `passing`; the recorded status is consistent with everything reproduced. No status change needed beyond the F3 tally correction. Not updated via `pm update-validation` (correctly — the row contains `|`).

---

## Recommendations

**Before close (mechanical, ~10 minutes, no model change):**
1. Add three `data/traceability_matrix.csv` rows for the producer-shaping calc defs (F2).
2. Correct the trap tally 12 → 11 in `plan.md` and the SV-035 row (F3).
3. Add the line number to the `inflation_rate` citation (F6).

**At close, for the owner to note:**
4. The verdict rests on reading A-4(1) as "under A-2 or itemized under (2)" (F1). Ratify the reading, or amend A-4's wording.

**Follow-up work item (not blocking):**
5. `'Levelized Annual Cost'` omits 1cfe's `i ≈ g` guard and epsilon (F4). Either carry them or document the validity range in the def. Matters only if the model is swept over discount or escalation rate.

---

## Audit metadata

**Executed by this audit:** `handshake_1costingfe.py` (full re-run at pin), `build_verdict_report.py` (regeneration + byte-diff), `run_stellaris_single.py` (design point, oracle, guard-live), `run_anchors.py` (IFE A/B/C), `pytest tests/models/ -q`, `agentic-mbse validate --level 1 models`, `sysml-codegen snapshot` (staged tree recapture at pin), `sysml-codegen generate --preserve-handwritten` (into `/tmp/aud_gen`), plus an independently written A-4 reconciliation script.

**Files read in full:** `build_verdict_report.py`, `levelized_replacement_cost_impl.py`, `verify_stellaris.py` (oracle mirror + CAS72 region), `mfe_account_costs.sysml:620-925`, `HANDSHAKE_REPORT.md`, the WI-029 plan Implementation Record, the orchestration brief, the anchor acceptance spec (A-2/A-4/A-5).

**Baseline source:** `1costingfe` @ `0254385` — `layers/economics.py`, `layers/costs.py`, `layers/physics.py`, `model.py`, `defaults.py`, `data/defaults/costing_constants.yaml`, `data/defaults/steady_state_stellarator.yaml`, `adapter.py`.

**Thresholds:** A-2 per-account |rel dev| ≤ 1e-6 vs 1cfe float32; oracle rel ≤ 1e-9; A-4 reconciliation residual ≤ 1e-6 relative to LCOE.

**Nothing was modified in the repository by this audit.** Tracked tree is clean; the two regenerated artifacts (`handshake_comparison.json`, `HANDSHAKE_REPORT.md`) reproduced byte-identical, and the regeneration test wrote to `/tmp/aud_gen`.

**Verdict: POSITIVE — nine of nine bars. The criterion-3 (Anchor A) verdict MET is confirmed by independent reproduction.** Ready for owner `pm close-item WI-029`, ideally after the three mechanical corrections above.

ARTIFACT: work/analysis/20260725-091831_audit_WI-029_handshake-lcoe-construction.md
