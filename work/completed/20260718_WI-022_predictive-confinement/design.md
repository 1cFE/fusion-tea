---
Status: complete
Created: 2026-07-18
Updated: '2026-07-18'
Related Artifacts:
  Spec: ./spec.md
---

> Process note: per the owner-ratified item process, the single owner checkpoint sits after
> `/spec-model`. That checkpoint ran 2026-07-18 and ratified: Option 1 (anchor-derived profile
> referents, executed blind to the fusion power), the errata fold-in (a = 1.3, V ≈ 425 into this
> item), and WI-023 for the magnet-field errata. Design → plan → implement → close proceed
> without a further stop.

# WI-022 Design: Predictive Confinement — Profile-Integrated D-T Reactivity

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — demo model-development session; §3 barred paths not read. Physics/profiles from the admissible Stellaris sources (image-verified per spec); engineering formulas from 1costingFE @ `0254385`.

## Overview

One calc def changes: `'DT Fusion Power'` (`models/library/analyses/mfe_plasma_scaling.sysml`) gains five profile inputs (peak fuel densities `n_D0`/`n_T0`, peak ion temperature `T_i0`, profile exponents `alpha_n`/`alpha_T`) and a **0D bypass contract** on the existing `sigma_v` input (now `default 0.0`). When `sigma_v > 0` the calc computes the existing 0D form exactly (`0.25·n_e²·sigma_v·E_fus·V·1e-6` — the handshake path, byte-identical by construction). When `sigma_v = 0` it computes the profile-integrated power `p_fus = n_D0·n_T0·[∫₀¹ u^{2α_n}·σv(T_i0·u^{α_T}) du]·E_fus·V·1e-6` (u = 1−ρ², dV/V = 2ρ dρ), with σv the Bosch-Hale D-T curve. The transcendental physics routes the calc to the **handwritten codegen stage** (spike-proven): auto-codegen emits a `handwritten/.../dt_fusion_power_impl.py` stub, filled with faithful Python and preserved across regen (`preserve_handwritten=True`). The pure-Python oracle mirrors the identical integral so `run_stellaris.py` guards the impl bit-exact.

The Stellaris instance binds the image-verified referents (spec, Decision C): `n_D0 = n_T0 = 1.96e20`, `T_i0 = 14.63`, `alpha_n = 0.33`, `alpha_T = 1.19`, `sigma_v = 0.0` — and, per the ratified errata fold-in (MR-WI022-8): `a = 1.3`, `f_shape = 1.003157` (targets the printed V = 425), `n_e = 3.17e20`, `wall_load_limit = 4.05`. Expected headline: p_fus ≈ 2748 MW (+1.8% vs the 2700 MW design point, prototype-confirmed); the geometry rebind also moves the radial-build volumes, wall area, and coil bore (all forward-computed from `a`, WI-021 seam).

## Research Findings

**Physics is prototype-settled** (spec + `prototype/`): the profile integral with the digitized Fig.-16 exponents reproduces the printed design point with no tuning (2747.7 MW at V = 425). All referent values image-verified; the extraction-text caption pair (1.2, 3.0) is refuted and recorded in the spec.

**Codegen seam is spike-settled** (spec §Codegen feasibility): a transcendental invocation classifies the calc `manual_required` (`calc_compat_renderer.py:76`), the package still emits, V11 params-coverage offenders stay at the 3 pre-existing rollups, the handwritten stub lists in `IMPLEMENTATION_BACKLOG.md`, and a filled impl survives regen when the bridge sets `preserve_handwritten=True` (default is False — MR-WI022-4).

**Consumer map** (grep over `models/` + `exploration/`, current at `7f0b19ea`):

| consumer | what it touches | change |
|---|---|---|
| `mfe_plasma_scaling.sysml:125-155` | `'DT Fusion Power'` calc def | profile inputs + bypass contract + Bosch-Hale intermediates + doc rewrite |
| `mfe_plant.sysml:157-165` | plant fusion attrs + `fusion` calc block | add 5 plant attributes (default 0.0) + bindings; `sigma_v` attr gets `default 0.0` |
| `stellarator_plant.sysml:268-294` | geometry bindings + shaping note | `a = 1.3`; `f_shape = 1.003157`; rewrite the WI-020 empirical-factor note (MR-WI022-8) |
| `stellarator_plant.sysml:337-384` | fusion bindings + MAPPING-TRAP doc | `n_e = 3.17e20`; `sigma_v = 0.0` + doc rewrite (MR-WI022-3); bind the 5 profile params with image citations |
| `stellarator_plant.sysml:575-577` | `wall_load_limit` | `4.95` → `4.05`, citation re-pointed to the Table 2 image |
| `models/library/analyses/mfe_viability.sysml:69` | doc reference to the phantom 4.95 row | re-point to Table 2 image (4.05) |
| staged copies under `exploration/stellarator_e2e/models/` | same files | identical edits (verify byte-identity of shared regions first, per the canonical-vs-staged split) |
| `exploration/stellarator_e2e/bridge_v11_generate.py:99` | `GenerationConfig` | add `preserve_handwritten=True` (MR-WI022-4) |
| `exploration/stellarator_e2e/generated/handwritten/...` | new impl file | fill with the faithful integral (below) |
| `exploration/stellarator_e2e/verify_stellaris.py` | oracle | mirror `sigv_dt` + the identical trapezoid integral; update IN params (a, f_shape, n_e, profile params) |
| `exploration/stellarator_e2e/run_stellaris.py` | headline asserts | V 448→425, p_fus 2144.5→computed, downstream channels re-baselined |
| `exploration/stellarator_e2e/handshake_1costingfe.py` | — | **no change** — injects `fusion__sigma_v > 0` → bypass path reproduces 1cfe's 0D point by construction (D2) |

Nothing else reads `fusion.p_fus` inputs or `geom.V`/`rb` beyond the WI-019/020/021-mapped consumers (power balance `p_nrl = fusion.p_fus`, radial-build consumers — all recompute automatically).

## Design Decisions

**D1 — extend `'DT Fusion Power'` in place; no new calc.** The profile physics is the same node in the dataflow (density/temperature → fusion power); adding a sibling "reactivity" calc would either break the handshake's `fusion__sigma_v` leaf injection (calc-to-calc binding removes the leaf) or force an effective-reactivity re-normalization detour. Extending in place keeps the consumer graph (`p_nrl = fusion.p_fus`, V11 coverage) untouched. Rejected: sibling `'Profile Reactivity'` calc feeding `sigma_v` — WI-021-style handshake trap, plus an awkward `/(0.25·n_e²)` normalization with no physical meaning in the diluted-fuel form.

**D2 — 0D bypass on `sigma_v > 0`, not a temperature inversion.** The handshake back-solves a *reactivity value*; reproducing it through the profile path would require inverting Bosch-Hale for an equivalent temperature (iterative, exactness only by convergence). The bypass keeps the injected value on the exact arithmetic path the handshake has always used: byte-identity of SV-025/026 by construction, zero handshake edits. The sentinel is explicit and documented in the calc doc (a physical reactivity is strictly positive; 0.0 unambiguously means "not supplied"). Misuse rule: if both `sigma_v > 0` and profile params are bound, the bypass wins (documented).

**D3 — discretization: trapezoidal rule in ρ, N = 200,000 intervals, pure-Python float64.** Matches the prototype (`prototype/reactivity_grid.py`) to its convergence plateau; the mild endpoint non-smoothness (u^{2α_n} at ρ = 1) converges ~N^{-1.66}, giving ≲1e-8 relative error at this N. Pure-Python `math` ops (no numpy/jax in the impl) keep the generated runtime dependency-free and make oracle mirroring exact: the oracle carries the *same function* (same operation order), and `run_stellaris.py` asserts agreement at the standing 1e-9 relative tolerance. Runtime ~0.2 s, irrelevant. T-floor guard `max(T, 1e-6 keV)` before σv (below ~0.02 keV the `exp(−3ξ)` underflows to exactly 0.0 — clean).

**D4 — the SysML expression carries the Bosch-Hale intermediates; the integral contract lives in the doc; the handwritten impl is the executable semantic.** The calc body declares `theta`, `xi`, `sigv_peak` (the true Bosch-Hale evaluation at `T_i0`, expressible with `RealFunctions::sqrt`/`exp`) and states `p_fus` from them — honest physics in the model, and the transcendental invocations are what routes the calc to `manual_required` (spike-proven). The continuous ρ-integral cannot be a closed-form expression; its contract (integrand, substitution, N, T-floor, bypass rule) is specified normatively in the calc doc comment, realized in the handwritten impl, and guarded by the oracle (MR-WI022-5). This is the owner-ratified Rung-B seam: the physics lives in the model, is executed, and is testable.

**D5 — profile inputs default 0.0 and thread as plant attributes defaulting 0.0.** Library stays concept-agnostic (MR-3): a tokamak instance binds nothing new and keeps its 0D `sigma_v` path. The WI-020 codegen gotcha (defaults don't propagate — the snapshot bakes instance bindings) is handled the same way as WI-020/021: the Stellaris instance binds **all five** profile inputs explicitly; the baked `sigma_v = 0.0` selects the profile path at run time, and the handshake's injected `fusion__sigma_v > 0` overrides it for the 1cfe point.

**D6 — geometry rebind targets the printed V = 425 via `f_shape = 1.003157` at unchanged R = 12.7.** `f_shape = 425 / (2π²·12.7·1.3²) = 425/423.6626 = 1.0031566`. The factor's meaning flips from "empirical packing reconciliation" (0.7943, built on two garbled numbers) to a ≈0.3% residual QI shaping correction against the printed volume; the WI-020 note is rewritten accordingly (correction rule — the false framing is deleted, the owner's amended ruling recorded). R stays 12.7: the Table 2 image prints 12.7, and the magnet `R0 = 12.7` stays consistent. Rejected: binding V directly (breaks the R→V chain / SV-017); moving R to 12.74 (Table 5's rounding; would touch the magnet block for a 0.3% cosmetic gain — and the magnet is WI-023's file).

## Proposed Design

### `'DT Fusion Power'` (library, canonical + staged identical)

```sysml
calc def 'DT Fusion Power' {
    doc /*
    D-T fusion power [MW] — 0D bypass or profile-integrated (WI-022).

    MODE (bypass rule): sigma_v > 0  ->  0D form (exact legacy contract):
        p_fus = 0.25 * n_e^2 * sigma_v * E_fus * V * 1e-6
    sigma_v = 0 (default)  ->  profile-integrated form:
        p_fus = n_D0*n_T0 * I * E_fus * V * 1e-6
        I = integral_0^1  u^(2*alpha_n) * sigv_dt(T_i0 * u^alpha_T) du,  u = 1 - rho^2
    with n(rho) = n0*(1-rho^2)^alpha_n, T(rho) = T0*(1-rho^2)^alpha_T (Stellaris
    Eqs. 2-3, image-verified) and dV/V = 2*rho*d(rho). The fuel term is
    n_D*n_T (diluted peak fuel densities), NOT 0.25*n_e^2.

    EXECUTABLE SEMANTIC: the Bosch-Hale curve needs exp(); this calc is
    manual_required and its generated handwritten impl is normative, guarded
    bit-exact by the oracle (verify_stellaris.py). Discretization contract:
    trapezoid in rho over [0,1], N = 200,000 intervals, T floor 1e-6 keV,
    pure-Python float64. The intermediates below state the Bosch-Hale
    evaluation at T_i0 (sigv_peak) in the model; the integral weights it
    over the profiles.
    ...Source/Ref/Basis citations...
    */

    in attribute n_e : Real;                       // vol-avg electron density [m^-3] (0D path)
    in attribute sigma_v : Real default 0.0;       // 0D-effective reactivity [m^3/s]; > 0 selects the 0D bypass
    in attribute E_fus : Real;                     // per-event D-T energy [J]
    in attribute V : Real;                         // plasma volume [m^3]

    in attribute n_D0 : Real default 0.0;          // peak D density [m^-3]
    in attribute n_T0 : Real default 0.0;          // peak T density [m^-3]
    in attribute T_i0 : Real default 1.0;          // peak ion temperature [keV]; default 1.0 (not 0)
                                                   // keeps the dormant Bosch-Hale intermediates
                                                   // defined (xi divides by theta(T_i0)); the mode
                                                   // is selected by sigma_v, never by T_i0
    in attribute alpha_n : Real default 0.0;       // density profile exponent
    in attribute alpha_T : Real default 0.0;       // temperature profile exponent

    // Bosch-Hale sigv_dt at T_i0 (reactivity.py:54-70) — the model-resident
    // statement of the reactivity curve; transcendental => manual_required.
    attribute theta : Real = T_i0 / (1.0
        - T_i0 * (1.51361e-2 + T_i0 * (4.60643e-3 + T_i0 * -1.06750e-4))
        / (1.0 + T_i0 * (7.51886e-2 + T_i0 * (1.35000e-2 + T_i0 * 1.36600e-5))));
    attribute xi : Real = ((34.3827 * 34.3827) / (4.0 * theta)) ** (1.0 / 3.0);
    attribute sigv_peak : Real = 1.17302e-9 * theta
        * RealFunctions::sqrt(xi / (1124656.0 * (T_i0 ** 3)))
        * (2.718281828459045 ** (-3.0 * xi)) * 1.0e-6;
    // e^x written as e ** x: the syside stdlib RealFunctions has sqrt but no
    // exp/ln; the sqrt invocation is the manual_required routing trigger.

    out attribute p_fus : Real = n_D0 * n_T0 * sigv_peak * E_fus * V * 1.0e-6;
    // ^ model-resident peak-form statement; the handwritten impl computes the
    //   doc-specified bypass/integral semantic and is the executable meaning.
}
```

*(Exact expression form may be adjusted at implement against the parser — the requirements are: parses at L1, carries the Bosch-Hale statement, and contains ≥1 transcendental invocation so the calc routes `manual_required`.)*

### Handwritten impl (generated `handwritten/.../dt_fusion_power_impl.py`)

```python
import math

def _sigv_dt(T):  # Bosch-Hale D-T [m^3/s]; 1costingFE reactivity.py:54-70
    T = max(T, 1e-6)
    theta = T / (1.0 - T*(1.51361e-2 + T*(4.60643e-3 + T*-1.06750e-4))
                 / (1.0 + T*(7.51886e-2 + T*(1.35000e-2 + T*1.36600e-5))))
    xi = ((34.3827**2) / (4.0*theta)) ** (1.0/3.0)
    return 1.17302e-9*theta*math.sqrt(xi/(1124656.0*T**3))*math.exp(-3.0*xi)*1e-6

def dt_fusion_power(n_e, sigma_v, E_fus, V, n_D0, n_T0, T_i0, alpha_n, alpha_T):
    if sigma_v > 0.0:                                   # 0D bypass (handshake path)
        return 0.25 * n_e**2 * sigma_v * E_fus * V * 1e-6
    N = 200_000                                         # trapezoid in rho over [0,1]
    acc = 0.0
    for i in range(N + 1):
        rho = i / N
        u = 1.0 - rho*rho
        f = (u**(2.0*alpha_n)) * _sigv_dt(T_i0 * (u**alpha_T)) * 2.0*rho
        acc += f if 0 < i < N else 0.5*f
    integral = acc / N
    return n_D0 * n_T0 * integral * E_fus * V * 1e-6
```

*(Signature/naming follows the generated stub; the oracle carries the identical `_sigv_dt` + loop so the runner's 1e-9 check is an exact-mirror guard.)*

### Instance bindings (`stellarator_plant.sysml`, staged copy identical)

Geometry (MR-WI022-8): `a = 1.3` (Table 2 image); `f_shape = 1.0031566` (printed V = 425, Table 5 image; doc rewritten — empirical-0.7943 framing deleted, amended owner ruling recorded); `n_e = 3.17e20` (Table 5 image; doc notes it is handshake/reference-only in profile mode); `wall_load_limit = 4.05` (Table 2 image; `mfe_viability.sysml` doc re-pointed).

Fusion (MR-WI022-2/3): `sigma_v = 0.0` (doc: bypass off — profile integral is the computed path; MAPPING-TRAP note rewritten: the 0D limitation is closed by this item, computed p_fus stated, garbled-text history compressed to one line); `n_D0 = 1.96e20`, `n_T0 = 1.96e20`, `T_i0 = 14.63`, `alpha_n = 0.33`, `alpha_T = 1.19` — each with Source/Ref/Basis resolving to the image files and `prototype/` digitization record.

### Generic plant (`mfe_plant.sysml`)

```sysml
attribute n_D0 : Real default 0.0;   // + n_T0, T_i0, alpha_n, alpha_T likewise
// sigma_v attribute gains default 0.0
calc fusion : 'DT Fusion Power' {
    in n_e = n_e; in sigma_v = sigma_v; in E_fus = E_fus; in V = geom.V;
    in n_D0 = n_D0; in n_T0 = n_T0; in T_i0 = T_i0;
    in alpha_n = alpha_n; in alpha_T = alpha_T;
}
```

## Cross-File Bindings

| binding | file | change |
|---|---|---|
| 5 × `in <profile> = <profile>` (new) | `mfe_plant.sysml` fusion block | plant attributes default 0.0 (D5) |
| `:>> a = 1.3`, `:>> f_shape = 1.0031566` | `stellarator_plant.sysml` | rebind + rewritten notes (D6) |
| `:>> sigma_v = 0.0` + 5 profile bindings | `stellarator_plant.sysml` | bypass off + image-cited referents |
| `:>> n_e = 3.17e20`, `wall_load_limit = 4.05` | `stellarator_plant.sysml` | extraction corrections (MR-WI022-8) |
| `in V = geom.V`, `p_nrl = fusion.p_fus` | `mfe_plant.sysml` | unchanged wiring; values move |
| handshake `fusion__sigma_v` injection | `handshake_1costingfe.py` | unchanged (bypass path, D2) |
| `preserve_handwritten=True` | `bridge_v11_generate.py:99` | new config flag (MR-WI022-4) |

Dataflow stays unidirectional: geometry → fusion → power balance → cost spine → LCOE. No new graph edges beyond the five plant-attribute inputs into the existing fusion node.

## Validation Plan

1. **L1–L3** on canonical `models/` after each edit; L1 = 0. Baseline (WI-021): L2 = 2 pre-existing IFE; L6 = 5 pre-existing (3 MFE rollups + 2 IFE). Zero new offenders.
2. **Codegen**: snapshot → V11 bridge. Expect `'DT Fusion Power'` → `manual_required`, package emits, V11 offenders stay exactly 3, backlog lists the one handwritten function. Fill impl; **regen again** and confirm the filled impl survives (MR-WI022-4 acceptance).
3. **Runner**: `run_stellaris.py` — physics spine + accounts + LCOE bit-exact vs the updated oracle at 1e-9; headline asserts re-baselined (V = 425, computed p_fus ≈ 2748, cascaded p_th/p_net/q_eng/LCOE).
4. **Handshake**: `handshake_1costingfe.py` — SV-025 channels and SV-026 account gap **byte-identical to WI-021** (D2 closure proof).
5. **Viability**: beta_ok, wall_load_ok (limit 4.05, expected ≈3.1), tbr_ok all pass at the re-baselined power. IFE regression SV-023 untouched.
6. **SV-029** recorded in `modeling_project/VALIDATION_MATRIX.md`; SV-016 flag noted at close (q_eng moves again).

## Validation Report

- Physics prototype: PASS (spec §prototype; 2747.7 MW at V = 425, +1.8% vs design point).
- Codegen-routing spike: PASS (spec §codegen feasibility; manual_required + emit + preserve).
- Calc-def stencil parse (syside 0.8.6, `try_load_model`): **PASS, zero diagnostics** — after replacing `RealFunctions::exp` (absent from the stdlib) with the e-power form; `RealFunctions::sqrt`, the nested Bosch-Hale arithmetic, and all defaulted `in` attributes resolve clean. Stencil at `scratchpad/proto_calc/dt_fusion_profile_proto.sysml` (session scratch; the canonical edit lands at implement).

## Implementation Checklist

1. **Library edit** — `'DT Fusion Power'` profile inputs + bypass doc + Bosch-Hale intermediates (canonical + staged, identical; confirm byte-identity first). L1–L3.
2. **Plant thread** — `mfe_plant.sysml` 5 attributes + bindings + `sigma_v` default (canonical + staged). L1.
3. **Instance** — geometry rebind + fusion rebind + doc rewrites + `wall_load_limit`; `mfe_viability.sysml` doc re-point (canonical + staged). L1–L6 full compare.
4. **Bridge + regen** — `preserve_handwritten=True`; snapshot + V11 bridge; verify manual_required routing + 3 offenders; fill the handwritten impl; regen; verify survival.
5. **Oracle + runner** — mirror `_sigv_dt` + integral in `verify_stellaris.py` (params: a, f_shape, n_e, profile set); update `run_stellaris.py` headline asserts; run green (bit-exact).
6. **Handshake** — re-run; SV-025/026 byte-identical vs WI-021 records.
7. **Close-out** — SV-029 passing; VALIDATION_MATRIX; STALE-BASIS annotations to new p_net; headline + residual-vs-2700 recorded in work item and `.project/CURRENT_WORK.md`; SV-016 flag; `/status` close.

## Risks

| risk | likelihood | impact | mitigation |
|---|---|---|---|
| Parser rejects an expression form (RealFunctions names, defaulted ins) | resolved | — | stencil pre-checked with syside 0.8.6: `RealFunctions::exp` does not exist in the stdlib (only sqrt/floor/round/etc.); e^x written as `2.718281828459045 ** x`; defaulted `in` attributes parse clean |
| Handwritten stub name/signature differs from D4 sketch | medium | low | adopt the generated stub's contract verbatim; oracle mirrors whatever ships |
| Oracle/impl drift over time | medium | medium | identical code blocks + runner bit-exact gate every run (MR-WI022-5); `preserve_handwritten=True` pins the impl |
| Handshake accidentally changes | very low | high | zero handshake edits; SV-025/026 byte-compare vs WI-021 records is the gate |
| Geometry rebind ripples further than mapped (magnet bore, blanket costs) | certain (intended) | medium | all consumers forward-computed (WI-021 seam); implement records executed values; magnet **B** stays WI-023 |
| Viability check fails at re-baselined power | low | high if it happened | estimated wall load 3.1 < 4.05; beta unchanged; q_eng rises; implement confirms before close |
