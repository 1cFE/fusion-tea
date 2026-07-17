---
Status: complete
Created: 2026-07-14
Updated: '2026-07-14'
Related Artifacts:
  Spec: ./spec.md
---

> Process note: per the owner-ratified item process (handoff 2026-07-14 + checkpoint
> confirmation), the single owner checkpoint sits after `/spec-model`; design → plan →
> implement → validate → handshake proceed without a further stop. Spec approved at
> checkpoint 2026-07-14 ("confirmed on all four").

# WI-019 Design: Faithful MFE Power Balance

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — demo model-development session; §3 barred paths not read. All physics/engineering sourcing is 1costingFE @ `0254385` plus repo artifacts.

## Overview

One calc def changes: `'MFE Power Balance Calc'` gets the faithful thermal-power formula, an absolute `p_pump` input replacing the `fpcppf` fraction, a full-precision alpha fraction, and `p_sub` aligned to gross electric. Two consumers rebind (`mfe_plant.sysml`, `stellarator_plant.sysml`), and the e2e artifacts (staged copy, generated pipeline, oracle, handshake) follow. No new files, no new SysML constructs — every change stays inside patterns already proven through codegen (SV-023/024).

## Research Findings

**The algebraic collapse (spec "Key Derivation", verified twice).** In 1costingFE's DEC-free (`f_dec = 0`), non-radiation-limited (`p_input_eff = p_input`) regime, steps 4–7 of `physics.py:290-303` reduce to

```
p_th = mn·p_neutron + p_alpha + p_input + eta_p·p_pump
```

because `p_rad + p_wall = p_alpha + p_input` identically (radiated and transported charged-particle power are both recovered at the wall). Numerically verified against `onecfe_point.json`:

- Identity: `p_rad + p_wall = 25.680 + 521.321 = 547.001 = p_ash + p_input = 517.001 + 30.0` ✓
- **Full-chain check (design-phase oracle, 2026-07-14): the proposed formula reproduces all six power channels — `p_th` 2819.07, `p_the`/`p_et` 1127.63, `p_net` 1000.0, `q_eng` 8.835, `rec_frac` 0.1132 — at 3.4e-8…6.2e-8 relative**, which is the float32 precision of the reference table itself. SV-025's 1e-5 tolerance has three orders of margin.

**Recirculating sum needs no change.** `physics.py:321-323` uses `p_coils + p_pump + p_sub + p_aux + p_cool + p_cryo + p_input_eff/eta_pin`. The existing SysML sum is identical once `p_pump` is an input and given `p_input_eff = p_input` in-regime. `p_aux = p_trit + p_house` (`physics.py:294`) already matches.

**Consumer map (complete, verified by grep over `models/` and `exploration/`).**

| consumer | what it touches | change |
|---|---|---|
| `models/designs/generic_mfe/mfe_plant.sysml:129` | plant attribute `fpcppf` | becomes `p_pump : Real` [MW] |
| `models/designs/generic_mfe/mfe_plant.sysml:146` | `pb` binding `in fpcppf = fpcppf` | `in p_pump = p_pump` |
| `models/designs/stellarator_09/stellarator_plant.sysml:310-312` | `:>> fpcppf = 0.06` (archived-PyFECONS citation) | `:>> p_pump = 1.0` cited to `steady_state_stellarator.yaml:21` |
| `exploration/stellarator_e2e/models/analyses/mfe_power_balance.sysml` | staged copy, byte-identical to canonical for this file | same edit as canonical |
| `exploration/stellarator_e2e/models/designs/...` staged plant/instance | same bindings | same edits |
| `exploration/stellarator_e2e/verify_stellaris.py:20,60-73` | oracle params + formula mirror | mirror the new formula; `fpcppf=0.06` → `p_pump=1.0` |
| `exploration/stellarator_e2e/handshake_1costingfe.py:191-194` | mapping-trap block feeding `pb__fpcppf = 0.06` | `pb__p_pump = pb["p_pump"]` — `p_pump` is already in the emitted `pb_params` (verified); trap note deleted, HANDSHAKE_REPORT discrepancy 9 resolved |
| `run_stellaris.py` | no direct fpcppf reference (drives via sys_design JSON) | input JSON regenerated with the pipeline |

Nothing else in `models/` or the IFE side references `fpcppf` or the power-balance internals.

**Pipeline regeneration procedure (from CODEGEN_FINDINGS.md, unchanged):** `sysml-codegen snapshot` over `exploration/stellarator_e2e/models/` → `bridge_v11_generate.py` (V11's params-coverage gate aborts on cross-part rollups, so the direct emit path is bypassed). Needs `SYSIDE_LICENSE_KEY` from `/home/reid/1cfe/fusion-tea/.env`. teax execution uses `exploration/pipeline_spike/.venv-exec`. The two harness-glue patches (BOP input repoint, capital-rollup summation) live in the runner/handshake scripts and re-apply to the regenerated YAML as-is — the pb schema field rename (`fpcppf` → `p_pump`) flows through the regenerated sys_design JSON automatically.

## Design Decisions

**D1 — implement the collapsed form, not the literal step 4–7 chain.** The calc computes `p_th = mn·p_neutron + p_alpha + p_input + eta_p·p_pump` directly rather than materializing `p_rad`/`p_transport`/`p_wall` intermediates. Rationale: the intermediates require a `p_rad` value the model cannot yet populate (no radiation physics until handoff item 2) and a `max()` outside the codegen envelope; the collapsed form is algebraically identical in the documented regime and adds zero new physics inputs. The doc comment carries the derivation and both regime conditions (MR-WI019-4).

**D2 — `p_pump` replaces `fpcppf` in the calc's input contract.** Not "add p_pump and keep fpcppf": 1costingFE has no fpcppf, keeping both would leave a dead input, and MR-WI019-2 requires the faithful contract. The old `p_pump = fpcppf·p_the` derived attribute is deleted (it also removes a hidden p_the→p_pump coupling that 1costingFE never had).

**D3 — alpha fraction written as the expression `(3.52 / 17.58)`**, not a rounded literal. Flat literal division is static-evaluable and inside the proven envelope; it reproduces 1costingFE's `ash_frac` bit-for-bit at float64. The internal attribute keeps the name `p_alpha` (1costingFE calls it `p_ash`; noted in the doc comment, not worth a rename ripple — it is not part of the output contract).

**D4 — `p_sub = f_sub · p_et`** (was `f_sub · p_the`). Numerically identical while `p_et = p_the` (no DEC), but aligns the formula with its cited source line (`physics.py:315`) so the citation is honest.

**D5 — output contract unchanged.** Outputs remain exactly `p_th, p_the, p_et, q_eng, rec_frac, p_net` (+ the same internal attributes minus `p_pump`-as-derived). No consumer of outputs changes; only the input side ripples.

## Proposed Design

Replacement body for `'MFE Power Balance Calc'` (`models/library/analyses/mfe_power_balance.sysml`; the staged copy gets the identical edit):

```sysml
calc def 'MFE Power Balance Calc' {
    doc /*
    MFE power balance: fusion power -> net electric power, engineering Q,
    recirculating fraction. Faithful to 1costingFE mfe_forward_power_balance
    in the DEC-free, non-radiation-limited regime (see conditions below).

    Thermal power derivation (WI-019): 1costingFE step 7 is
      p_th = mn*p_neutron + p_rad + p_wall + eta_p*p_pump      (physics.py:303)
    with p_wall = p_ash + p_input_eff - p_rad at f_dec = 0
    (physics.py:290-299), so p_rad cancels and
      p_th = mn*p_neutron + p_alpha + p_input + eta_p*p_pump.
    Charged-particle power reaches the wall as radiation or transport;
    both are recovered thermally, so no radiation model is needed here.

    Validity conditions (documented regime, MR-WI019-4):
      1. f_dec = 0 — no direct energy conversion (standing WI-009
         deviation 1).
      2. p_rad - p_alpha <= p_input — non-radiation-limited, so
         p_input_eff = p_input (physics.py:290). Deep margin for D-T
         (handshake point: p_rad 25.7 vs p_alpha 517 MW). Enforcement as
         a viability constraint is deferred to the predictive-physics
         item, which introduces p_rad.

    **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py
    **Ref**: physics.py:290-328 (steps 4-14, mfe_forward_power_balance)
    **Basis**: Steady-state MFE power flow; tokamak/stellarator-generic
    */

    // === PRIMARY INPUTS ===
    in attribute p_nrl : Real;      // Fusion power [MW]
    in attribute p_input : Real;    // Plasma heating power [MW]

    // === EFFICIENCIES ===
    in attribute mn : Real;         // Neutron energy multiplier (blanket)
    in attribute eta_th : Real;     // Thermal-to-electric efficiency
    in attribute eta_p : Real;      // Pumping power capture efficiency
    in attribute eta_pin : Real;    // Input power wall-plug efficiency

    // === PUMPING / SUBSYSTEM POWER ===
    in attribute p_pump : Real;     // Primary coolant pumping power [MW]
    in attribute f_sub : Real;      // Subsystem and control fraction

    // === COIL POWER ===          (unchanged: p_tf, p_pf)
    // === COOLING POWER ===       (unchanged: p_tfcool, p_pfcool)
    // === AUXILIARY POWER ===     (unchanged: p_trit, p_house, p_cryo)

    // D-T alpha (ash) power at full precision: E_alpha/Q = 3.52/17.58.
    // Source: physics.py:32-34, physics.py:177
    attribute p_alpha : Real = (3.52 / 17.58) * p_nrl;

    // Neutron power. Source: physics.py:179
    attribute p_neutron : Real = p_nrl - p_alpha;

    // (p_cool, p_aux, p_coils aggregations unchanged)

    // Thermal power — collapsed step 7 (derivation in header doc).
    // Source: physics.py:290-303
    out attribute p_th : Real =
        mn * p_neutron + p_alpha + p_input + eta_p * p_pump;

    // Thermal electric. Source: physics.py:306
    out attribute p_the : Real = eta_th * p_th;

    // Gross electric (p_dee = 0). Source: physics.py:309
    out attribute p_et : Real = p_the;

    // Subsystem power. Source: physics.py:315 (p_sub = f_sub * p_et)
    attribute p_sub : Real = f_sub * p_et;

    // Recirculating power. Source: physics.py:321-323
    attribute recirculating : Real =
        p_coils + p_pump + p_sub + p_aux + p_cool + p_cryo
        + p_input / eta_pin;

    // q_eng, rec_frac, p_net unchanged (physics.py:324-328)
}
```

(Stencil shows the changed region; unchanged input blocks and outputs are elided with markers. The implemented file keeps them verbatim.)

**Instance binding** (`stellarator_plant.sysml`, replacing lines 310-312):

```sysml
:>> p_pump = 1.0 {    // primary coolant pumping power [MW].
    doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:21 (p_pump = 1.0) **Basis**: 1costingFE stellarator primary-coolant pumping power */
}
```

**Oracle mirror** (`verify_stellaris.py`): params dict `fpcppf=0.06` → `p_pump=1.0`; compute block mirrors the new four-term `p_th`, drops the derived `p_pump`, and sets `p_sub = f_sub * p_et`.

**Handshake mapping** (`handshake_1costingfe.py`): the trap block becomes `f"{P}pb__p_pump": pb["p_pump"]` (value 1.0 in the emitted point); the fpcppf footnote is removed from the report at re-run.

## Cross-File Bindings

| binding | file | change |
|---|---|---|
| `in p_pump = p_pump` (was `in fpcppf = fpcppf`) | `models/designs/generic_mfe/mfe_plant.sysml` `pb` block | rename both the plant attribute (line 129) and the binding (line 146) |
| `:>> p_pump = 1.0` (was `:>> fpcppf = 0.06`) | `models/designs/stellarator_09/stellarator_plant.sysml:310` | new value + new citation |
| all other `pb` bindings | both design files | unchanged |
| cost-spine aliases `p_th/p_the/p_et = pb.*` | `mfe_plant.sysml:160-162` | unchanged (output contract stable) |
| `net_electric_mw = pb.p_net` (LCOE denominator) | `mfe_plant.sysml:320` | unchanged — corrects automatically |

Dataflow stays unidirectional: fusion power → power balance → cost spine → rollup → LCOE. Removing `p_pump = fpcppf·p_the` deletes a derived-from-output coupling, so the graph gets strictly simpler.

## Validation Plan

1. **L1–L3** on canonical `models/` after the edit (`uv run agentic-mbse validate`); L1 must be 0 errors. Expected L2 noise: the usual unused-library-def warns.
2. **L6** extraction check — same constructs as before (flat attribute defaults, in/out attributes), SV-024 already covers the wiring patterns; confirm binding/constraint/redef-drop counters stay 0.
3. **Design-phase numeric oracle** (done, above): new formula vs `onecfe_point.json` power table — all channels ≤6.2e-8. This is the SV-025 result in miniature, ahead of codegen.
4. **At implementation**: regenerate snapshot → V11 bridge → `run_stellaris.py` (oracle bit-exactness at the Stellaris point) → `handshake_1costingfe.py` (SV-025 formula channels, SV-026 account-gap collapse) → IFE regression SV-023 untouched (no IFE file changes, but re-run as the standing regression) → record the new Stellaris headline.

**Expected new Stellaris design-point numbers** (hand-computed from the new formula at the WI-018 bindings, for review orientation — implementation records the executed values): `p_th` ≈ 3182 MW (was 2693, +18.2%), `p_the = p_et` ≈ 1060 MW, recirculating ≈ 274 MW, `q_eng` ≈ 3.87, `p_net` ≈ 786 MW (was 575). Power-scaled accounts rise 5–11%; LCOE falls substantially (denominator +37% vs capital +~5%). The SV-016 "Q_eng ~10–40" band question flagged in the spec materializes here: q_eng ≈ 3.9 at the Stellaris point — raise at review (band was written pre-fix, order-of-magnitude type; 1costingFE's own 1 GWe point gives 8.8).

## Validation Report

**Prototype status: PASS** (2026-07-14). The three canonical edits (library calc, `mfe_plant.sysml` rebind, `stellarator_plant.sysml` instance binding) are applied in the worktree.

- **L1 syntax: 0 errors** across all 21 model files (the hard gate).
- **L3 dataflow: pass**, 0 circular dependencies (the fpcppf→p_pump change deletes the p_the→p_pump derived coupling, as designed).
- **L4 constraints: pass** (6/6 eligible), **L5 traceability: pass** (100% documented).
- **L2 (3 issues) and L6 (105 issues) flag exactly the same items as pristine HEAD** — verified by extracting `git archive HEAD models` to scratch and validating it: identical counts, all in untouched IFE files and the documented canonical cross-part rollups (the deliberate canonical-vs-staged split, SV-024 / CODEGEN_FINDINGS). **Zero new issues introduced.**
- **Numeric formula check vs 1costingFE** (`onecfe_point.json`, Anchor A point): all six power channels match at 3.4e-8…6.2e-8 relative — the reference table's own float32 floor, 160× inside SV-025's 1e-5 tolerance.
- **Stellaris design-point check**: mirroring the OLD formula reproduces the committed headline exactly (p_th 2693.0, p_the 896.8, p_net 575.3 MW), certifying the mirror; the NEW formula gives p_th 3182.4, p_the = p_et 1059.7, recirculating 273.6, q_eng 3.873, p_net 786.1 MW — the expected-numbers table above, now computed rather than estimated.

## Implementation Checklist

1. **Library edit** — rewrite `'MFE Power Balance Calc'` per the stencil (canonical + staged copy, identical). Validate L1–L3.
2. **Consumer rebind** — `mfe_plant.sysml` attribute + binding; `stellarator_plant.sysml` `:>> p_pump = 1.0` with citation; staged design copies likewise. Validate L1–L6 across `models/`.
3. **Oracle + regen** — update `verify_stellaris.py`; regenerate snapshot + pipeline via V11 bridge; `run_stellaris.py` green (bit-exact vs oracle).
4. **Handshake** — update mapping; re-run `handshake_1costingfe.py`; check SV-025 (≤1e-5) and SV-026 (power-scaled accounts ≤0.1%); refresh `HANDSHAKE_REPORT.md` numbers and resolve discrepancies 1 and 9.
5. **Close-out** — flip SV-025/026 status; record new Stellaris headline in the work item + `.project/CURRENT_WORK.md`; raise the SV-016 band question at review.

## Risks

| risk | likelihood | impact | mitigation |
|---|---|---|---|
| A consumer of `fpcppf` outside the mapped set | low | low (L1 parse error, loud) | consumer map built by grep over `models/` + `exploration/`; L1 across the tree catches stragglers |
| Regenerated pipeline breaks harness glue (BOP repoint / rollup summation) | low | medium | glue keys off pb output names, which are unchanged; `run_stellaris.py` oracle check gates before the handshake |
| SV-016 band (Q_eng 10–40) reads as failing at q_eng ≈ 3.9 | certain to surface | low | pre-flagged; band is a pre-fix order-of-magnitude guess — owner adjusts or annotates at review, not silently edited |
| float32 reference noise pushes SV-025 past tolerance | very low | low | measured 6.2e-8 vs 1e-5 tolerance — 160× margin |
