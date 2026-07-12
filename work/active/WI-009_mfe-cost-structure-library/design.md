---
Status: draft
Created: 2026-07-03
Updated: 2026-07-03
Related Artifacts:
  Spec: ./spec.md
---

# WI-009: MFE Cost Structure Library — Design

**Status: in progress.** Research underway to pin the fusion-power and magnet-cost scaling relations and confirm codegen-safe SysML constructs. Sections below fill in as findings land.

## Overview

Concept-agnostic MFE library primitives: plasma scaling (R, B → fusion power), MFE power balance (→ net electric, engineering Q, recirc fraction), magnet cost scaling, the `'Magnet System'` costed component + MFE CAS22 sub-account types, MFE viability constraints, and the additive `'CAS Scope'::mfe_divergent` member. Reuses the IFE library unchanged except the enum.

## Research Findings

Three parallel investigations (2026-07-03): PyFECONS deep-dive, TEA/ARIES source analysis, and SysML construct patterns.

### SysML construct envelope (solid — no blockers)

The IFE library defines the codegen-safe envelope. Stay inside it:
- **Flat `calc def`s**: all `Real`, operators `+ - * / **`, parentheses, ~15 named intermediate `attribute x : Real = ...` lines referencing earlier names, one `return`. Float literals always written `.0` / `e`-notation. Ref: `ife_lcoe.sysml:4-126`.
- **No** `if`/`then`, **no** `sum()`/`collect`/multiplicity ops, **no** nested calc invocation inside a calc def, **no** unit/quantity types. Push viability logic into `constraint def`s, not conditionals.
- **`constraint def`**: bare boolean body, compose with `and`, defaulted inputs (`in attribute threshold : Real default 0.25;`). Ref: `fusion_cycle.sysml:29-51`.
- **Specialization + enum redefine**: `part def 'CAS22.1.3 Magnet System' :> 'CAS22 Power Core' { :>> scope = 'CAS Scope'::mfe_divergent; }` confirmed against `ife_subsystems.sysml:53,66`. Adding `mfe_divergent` to the enum is a safe additive edit (update the "Two-member" doc comment).
- **Gap to validate on first use** (WI-010, not here): the usage-level calc-chaining bind (`in x = source.ret;`) and part-level `assert constraint` are not exercised anywhere in the corpus — validate with `sysmlv2-validator` before replicating.

### Power balance (solid — portable as-is)

The archived `'MFE Power Balance Calc'` is a faithful, line-mapped port of PyFECONS `PowerBalance.py:8-50`. Contract: fusion power `p_nrl` and heating power `p_input` are **inputs**; outputs net electric, engineering Q, recirc fraction. D-T alpha fraction = **0.2002** (3.52/17.58). One documented deviation: the port drops the direct-energy-conversion term (`eta_de·p_alpha`), same as spec intent.

### 1costingfe — the authoritative source (resolves both scaling relations)

**PyFECONS was a red herring.** It is gone from the machine, but it was never needed: 1costingfe (`/home/reid/1cfe/1costingfe`, the JAX costing framework the explorer runs) already implements all three relations as concrete, tested code. We **reproduce** these in SysML and cite them — we do not call 1costingfe (per the WI-012 constraint). TEA/ARIES remain the *validation anchors*; 1costingfe is the *formula source*.

**Fusion power from R, B — exists in full** (`layers/tokamak.py`, the 0D operating-point chain; gated off in the released `forward()` which back-solves fusion power from net electric, but the code is intact and tested):
- Plasma current: `I_p = 2π·a²·κ·B / (μ₀·R·q95)` [MA] (`tokamak.py:86-91`)
- Greenwald density: `n_e = f_GW · I_p/(π·a²) · 1e20` [m⁻³] (`tokamak.py:94-99`)
- Plasma volume: `V = 2π²·R·a²·κ` (`tokamak.py:172-174`)
- Fusion power: `P_fus = 0.25 · n_e² · ⟨σv⟩(T_i) · E_fus · V · 1e-6` [MW], Bosch–Hale reactivity (`tokamak.py:102-114`, `reactivity.py:191`)
- B drives P_fus through density (n_e², via I_p). β is diagnostic only (Troyon check), not a P_fus input.

**Magnet cost from R, B — exists and is live in the release** (`layers/cas22.py`):
- Toroidal (tokamak/stellarator): `total_kAm = G · B · R0 · r_coil / (μ₀·1000)`, `G = 4π²` tokamak / `8π²` stellarator (`cas22.py:427,137-140`)
- `c220103 = total_kAm · cost_per_kAm · coil_markup` (`cas22.py:440-444`)
- Constants: REBCO $50/kAm, Nb3Sn/NbTi $7/kAm (`defaults.py:84-86`); `coil_markup` tokamak 3.09 / stellarator 5.87 (`costing_constants.yaml:73-83`). `r_coil = vessel outer radius` from the radial build (`geometry.py:114`).
- Mechanism is conductor ampere-meters (Ampère's law), linear in B, R0, r_coil. **Not** stress/stored-energy — the docstring notes an earlier r² model "exploded for large machines."

**Power balance + viability — exists** (`physics.py`, `validation.py`):
- Forward/inverse power balance mirror the archived port; `q_eng = p_et/recirc`, `rec_frac = 1/q_eng`, `p_net = (1−rec_frac)·p_et` (`physics.py:317-328`).
- Viability thresholds (`validation.py:495-517`): **hard fail** `rec_frac > 0.95` (net electric < 0); **economic warn** `rec_frac > 0.5` ("excessive parasitic load"); warn `q_sci < 2`. So the economic knee *has* a sourced value: `rec_frac ≤ 0.5`.

**Concept divergence in 1costingfe**: coil model diverges by concept (tokamak/stellarator bilinear `G·B·R0·r_coil`; mirror two-class solenoid+plug; dipole ring). Power balance diverges by *family* (steady-state vs pulsed), not concept. Stellarator has **no** 0D solver — it reuses the tokamak coil geometry (path_factor=2) and generic power balance; it is a costing variant of the tokamak. This tells us where the tokamak/stellarator split really lives: the coil geometry factor and the density closure, not the power balance.

### TEA/ARIES: validation anchors + the mass-based magnet caveat

TEA (Araiinejad & Shirvan 2025) and ARIES (Waganer 2013) contain **no** R,B→power scaling and cost magnets by **mass × $/kg**, not field — so they are not the formula source (1costingfe is). They give validation anchors and one important fidelity caveat.

| Concept | Net electric | Overnight capital | LCOE |
|---|---|---|---|
| ARIES-ST (spherical torus) | 1000 MWe | $9900/kW | — |
| ARIES-CS (stellarator) | 1000 MWe | $9700/kW | — |
| ARAI-FPP (ARC-based tokamak) | ~350 MWe | $8831–22,180/kW | $140–550/MWh |

Financial basis: discount 6%, life 30 yr, CF 0.5–0.7, 8766 h/yr. **Fidelity caveat**: ARC's real magnet cost is *structure-dominated* (a $4.6B steel cage reacting 23 T peak field), so the conductor-ampere-meter model undercounts it ~10× — which is exactly why concept 01 carries a $1030M magnet override vs. the $567M 1costingfe computes. We reproduce the conductor model (it scales correctly with R and B, which is what the sweep needs) and record structure-dominated costing as a known limitation, not chase it now.

### Design anchors (real, source-cited, in-repo) for calibration/validation

| | Tokamak — concept 01 (ARC) | Stellarator — concept 20a (Type One) |
|---|---|---|
| R0 / a / κ | 3.3 m / 1.13 m / 1.84 | 12.5 m / 1.25 m / ~1.0 |
| Aspect ratio | 3.0 | 10 |
| B0 (peak) | 9.2 T (23 T on coil) | 9.0 T |
| Fusion power | 525 MW | 800 MW |
| Net electric | 233 MWe | 350 MWe |
| β / n_e | absent / absent | 1.6% / 2.0e20 m⁻³ |
| Magnet cost | $1030M (override, Sorbom 2015) / $567M computed | $4080M computed (no source override) |

Sources: `exploration/concept_analysis/analyses/01-hts-compact-tokamak/` and `20a-type-one-stellarator/` (model_setup.py + analysis.md), citing `arc-reactor-specifications.md` (Sorbom 2015) and `cambridge-core...view.md` (JPP 2025). **Absent for both: plasma temperature in keV** — set from the 1costingfe concept spec (~15 keV optimal D-T) with a documented basis. The stellarator has no source-grounded magnet-$ anchor (analyst declined one for lack of published coil cost) — validate its magnet cost against the tokamak-calibrated coil model, not an independent anchor.

## Sourcing — Resolved (2026-07-04)

No PyFECONS restore, no external ingestion, no author-from-scratch. Every relation sources to 1costingfe (`tokamak.py`, `cas22.py`, `physics.py`, `defaults.py`) as the formula, calibrated/validated against the in-repo concept-01/20a design points and TEA/ARIES $/kW anchors. The earlier "restore vs. author" decision is void.

## Proposed Architecture

This section outlines the whole MFE model architecture — structure and behavior — and how it absorbs *different* tokamak (and stellarator) designs without rework. WI-009 delivers only the concept-agnostic library slice (marked **[WI-009]** below); WI-010 builds the plant abstractions, WI-011 the concrete designs. Presenting the whole shape first so the library's boundaries are the right ones.

### The frame: three layers, one dataflow

The model separates into three layers, and behavior flows one direction through them (no cycles — a hard rule from MODELING_PROCESS):

```
              geometry ─▶ plasma physics ─▶ power balance ─▶ costing ─▶ LCOE ─▶ viability
                (R,a,κ)      (n_e,T,V→P_fus)   (P_fus→P_net)   (B,R→$)   ($→$/MWh)  (P_net>0, rec≤0.5)
Layer 1  BEHAVIOR   ┃ concept-agnostic calc defs, library/analyses/            [WI-009]
Layer 2  STRUCTURE  ┃ costed-component part defs + CAS accounts, library/       [WI-009]
                    ┃ + the plant that composes them and binds the calcs        [WI-010]
Layer 3  CONCEPTS   ┃ concrete designs that set values + pick the closures      [WI-011]
```

**Behavior** is a pipeline of pure `calc def`s. **Structure** is a part tree whose decomposition *is* the CAS cost tree. The two meet in the plant part: it composes the physical subsystems (structure) and embeds `calc` usages (behavior) that read subsystem attributes and expose derived outputs (net electric, LCOE) — exactly the `ife_plant.sysml` idiom, one level richer.

### Layer 1 — Behavior: the calc pipeline [WI-009]

Five concept-agnostic `calc def`s in `library/analyses/`, each pure `Real`→`Real`, flat arithmetic (codegen-safe per MR-WI009-12). Reproduced from 1costingfe with citations:

1. **Geometry** — `(R, a, κ)` → plasma volume `V = 2π²·R·a²·κ`; radial build → coil radius `r_coil`. Src `tokamak.py:172`, `geometry.py:114`.
2. **Fusion power (core)** — `(n_e, T, V)` → `P_fus = 0.25·n_e²·⟨σv⟩(T)·E_fus·V`. Src `tokamak.py:102`. *Concept-agnostic* — takes density and temperature as inputs; the machine→density closure is Layer 3.
3. **Power balance** — `(P_fus, P_input, efficiencies, coil/aux/cooling powers)` → net electric, engineering Q, recirc fraction. Revive the archived port; inline D-T alpha 0.2002. Src `physics.py:317`.
4. **Coil cost** — `(G, B, R0, r_coil, $/kAm, markup)` → magnet capital via conductor ampere-meters `total_kAm = G·B·R0·r_coil/(μ₀·1000)`. Src `cas22.py:427`. `G` and `markup` are set by the concept (tokamak 4π²/3.09, stellarator 8π²/5.87) — this one calc serves both families.
5. **LCOE (DCF)** — `(capital, O&M, net electric, availability, discount, lifetime)` → `$/MWh`. Generic annuitization.

Plus **viability** as `constraint def`s: `net_electric > 0` (hard, physics) and `rec_frac ≤ 0.5` (economic, from `validation.py:512`).

Two design decisions inside Layer 1, both flagged for your eye:

- **Reactivity ⟨σv⟩(T) vs. the codegen envelope.** Bosch–Hale uses `exp()`, which is outside the proven flat `+ - * / **` set the IFE calcs stick to (MR-WI009-12). Rather than risk a codegen gap, ⟨σv⟩ enters as a **parameterized input evaluated at the design temperature** (~15 keV optimal D-T), sourced as a constant; if temperature later becomes a sweep axis, a power-law fit (`⟨σv⟩ ∝ T²` over 10–20 keV) stays inside the envelope. This keeps P_fus responsive to n_e and V (hence R and B) without an `exp()`.
- **"Reuse the IFE LCOE calc" is not literal.** `ife_lcoe.sysml` bundles IFE cost categories (driver, target, yield) *into* its DCF — it is IFE-shaped and not directly reusable for MFE. The genuinely reusable primitive is the DCF annuitization core. WI-009 adds a generic `'LCOE DCF'` calc; the IFE calc is left untouched (satisfying MR-WI009-9). This is a small, honest deviation from the spec's "reuse LCOE unchanged" wording — the reuse is the *pattern*, not the *file*.

### Layer 2 — Structure: costed components and the CAS tree [WI-009 defs, WI-010 assembly]

Physical decomposition equals cost decomposition: each subsystem `part def` specializes the CAS account it rolls up into (AD-005). The MFE-divergent power-core subsystems, new in WI-009:

```
'Costed Component'  (capital_cost)                              [exists]
└ 'CAS22 Power Core'                                            [exists]
  ├ 'CAS22.1.3 Magnet System'   (scope = mfe_divergent)   ─▶ 'Magnet System'   [WI-009]
  ├ 'CAS22.1.4 Heating & Current Drive' (mfe_divergent)   ─▶ 'Heating and CD'  [WI-009]
  └ 'CAS22.1.8 Divertor'        (mfe_divergent)           ─▶ 'Divertor'        [WI-009]
  ( 22.1.1 Blanket, 22.1.2 Shield, 22.1.5 Structure = shared, reused )
```

`'Magnet System'` carries the coil parameters (B, R0, r_coil, G, markup, $/kAm) and its `capital_cost` binds to the Layer-1 coil-cost calc. The shared accounts (CAS20–21, 23–27, 90) and `'IFE LCOE'`→ generic DCF are reused. Plant-level rollup (`capital_cost = magnet + heating + divertor + blanket + … `) lives in the plant (WI-010).

### Layer 3 — The variation mechanism: how different tokamak designs slot in [WI-010/011]

This is the part that makes the architecture serve *different* designs rather than one. A specialization hierarchy, abstract → concrete:

```
'MFE Power Plant'         (abstract; composes subsystems, binds the 5 calcs, asserts viability)
├─ 'Tokamak Plant'        (abstract; adds the Greenwald density closure n_e(I_p(R,a,κ,B,q95)),
│  │                        a current-drive subsystem, and TF/PF/CS coil topology; G=4π²)
│  ├─ 'HTS Compact Tokamak'   (ARC: R=3.3, a=1.13, κ=1.84, B=9.2, REBCO)      ← concept 01
│  ├─ 'Spherical Tokamak'     (low aspect ratio, copper-coil option)
│  └─ …any new tokamak = one more specialization
└─ 'Stellarator Plant'    (abstract; density as input/Sudo closure, NO current drive, modular coils; G=8π²)
   └─ 'HTS Modular Stellarator' (Type One: R=12.5, B=9.0)                       ← concept 20a
```

**What varies (the specialization surface)** — the only things a new design touches:
- Geometry values: R, a, κ, aspect ratio.
- Field and coil tech: B, conductor `$/kAm`, `coil_markup`, TF/PF/CS configuration.
- Operating point: q95, f_GW, design temperature, density.
- Family closure: how density is obtained (tokamak Greenwald vs. stellarator input) — the piece that makes B drive P_fus.
- Current drive: present (tokamak) or absent (stellarator) — a subsystem that is or isn't there.

**What's fixed (inherited, authored once)** — the five-stage calc pipeline, the CAS structure and rollup, the balance-of-plant, the viability constraints, and LCOE. A new tokamak design inherits all of it and redefines only its parameter values via `:>>`, plus any genuinely divergent subsystem.

**Why the B→P_fus chain still works even though P_fus is concept-agnostic**: the fusion-power calc (Layer 1) takes density as an input; the tokamak *closure* (`'Tokamak Plant'`, Layer 3) supplies `n_e` from `B` via Greenwald. So at the assembled `'HTS Compact Tokamak'`, sweeping B moves I_p → n_e → P_fus → net electric → LCOE end-to-end — which is exactly what WI-012 needs. The library stays concept-agnostic; the family closure lives one layer up. This is the deliberate seam that lets one library serve every tokamak *and* the stellarators.

### Structure ↔ behavior binding (the plant, WI-010)

The plant part is where the two halves join. Sketch of the idiom (full version is WI-010):

```sysml
part def 'MFE Power Plant' {
    part magnets   : 'Magnet System';        // structure
    part heating   : 'Heating and Current Drive';
    part divertor  : 'Divertor';
    // ... shared blanket/shield/BOP ...

    attribute R : Real;  attribute a : Real;  attribute kappa : Real;  attribute B : Real;

    calc geo  : 'Plasma Geometry'   { in R = R; in a = a; in kappa = kappa; }   // behavior
    calc pfus : 'DT Fusion Power'   { in n_e = /*closure*/; in temp = temp; in volume = geo.volume; }
    calc pb   : 'MFE Power Balance' { in p_fus = pfus.p_fus; /* ... */ }
    calc lcoe : 'LCOE DCF'          { in capital = capital_cost; in net_electric = pb.p_net; /* ... */ }

    attribute net_electric : Real = pb.p_net;
    attribute lcoe : Real = lcoe.lcoe;
    assert constraint viable : 'Net Power Positive' { in net_electric = pb.p_net; in rec_frac = pb.rec_frac; }
}
```

Note the two wiring forms — cross-calc binding (`in x = calc.ret`) and `assert constraint` — are *not* exercised anywhere in the existing corpus; the SysML-pattern research flagged them as the one gap. They belong to WI-010, and the first one written gets validated with `sysmlv2-validator` before replication.

### WI-009 deliverable boundary

WI-009 ships Layers 1–2 as reusable library pieces: the five `calc def`s, the three MFE CAS22 sub-account types + `'Magnet System'`/`'Heating and CD'`/`'Divertor'` costed components, the two viability `constraint def`s, the generic `'LCOE DCF'` calc, and the additive `'CAS Scope'::mfe_divergent`. It does **not** ship the plant, the family closures, or any concept values — those are WI-010/011. The one architectural choice WI-009 forces (and that I'll register as an AD): the density closure is *not* baked into the fusion-power calc, keeping it concept-agnostic and pushing family divergence to the plant layer.

## Validation Report

_(pending prototype — next step: stand up the five calc defs + structural defs in `.sysml` and run `syside check` / Levels 1–3)_
