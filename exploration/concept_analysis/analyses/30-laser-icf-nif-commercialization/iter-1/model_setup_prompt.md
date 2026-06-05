# 1costingfe Model Setup: Laser ICF NIF Commercialization (Focused Energy LIFE-class)

You are generating a runnable 1costingfe model setup script for **Laser ICF NIF Commercialization (Focused Energy LIFE-class)**
(Inertia Enterprises). The script must run via `uv run python model_setup.py` and emit an
LCOE estimate.

## The contract in one sentence

The design point is already chosen, the 1costingFE library already carries the
default cost story, and your job is to transcribe the fixed design point into the
**three-forward helper form** and add only the **evidence-backed overrides** the
analysis already discovered — nothing else.

## Step 0: Read the Design Point block from the analysis (primary source)

**Start here.** Open `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\30-laser-icf-nif-commercialization\analysis.md` and read its `## Design Point` block and
`## Section 5b: Override Candidates` block. These are your primary inputs:
- `P_native` — the design point's native net-electric power (MWe). You do **not**
  choose this; copy it.
- The Section 5 "Design Point Parameters" table — the geometry / physics / power
  inputs for the `spec` dict.
- The Section 5b Override Candidates YAML — the six-field override registry,
  transcribed verbatim into the `overrides` list.

The dossier is a *fallback* only for spec inputs the analysis did not extract — not
the primary source. The rendered Design Point and account schema for this concept,
for reference:

## Design Point

- Name: Inertia Enterprises commercial plant (1,000-beamline Thunderwall, 1.5 GWe stated)
- Maturity: paper-concept
- P_native: 1500 MWe
- Grounding: low
- Primary sources:
  - knowledge/concept_research/30-laser-icf-nif-commercialization/iter-01/sources/enr-mike-dunne-interview.md
  - knowledge/concept_research/30-laser-icf-nif-commercialization/iter-01/sources/inertia-website-technical.md
  - knowledge/concept_research/30-laser-icf-nif-commercialization/iter-01/sources/globenewswire-series-a-press-release.md

(Selection fields are orchestrator-fixed from the design-point table. Copy them verbatim; you are forbidden to edit them. The quantitative description of this plant belongs in Section 5.)

### Canonical account schema (override codes must come from here)

| Account | What it costs | Applies when |
| --- | --- | --- |
| `C220101` | First wall, blanket & neutron multiplier (DT: tritium-breeding blanket; DD/aneutronic: energy-capture blanket) | always (for this archetype) |
| `C220102` | Radiation shield (sized to neutron wall loading; scales down for low-neutron fuels) | always (for this archetype) |
| `C220104` | Supplementary plasma heating (steady-state) or primary pulsed driver (laser/accelerator/gun) | primary pulsed driver (laser/accelerator/gun) on $/J of driver energy; electrical-drive concepts cost it in C220107 |
| `C220105` | Primary structure — gravity supports, thermal shields, inter-coil structure, machine base | always (for this archetype) |
| `C220106` | Vacuum system — vessel, port extensions, cryopumps, leak detection | always (for this archetype) |
| `C220107` | Power supplies (steady-state magnet supplies / switchgear) or pulsed-power capacitor bank ($/J stored) | pulsed-power capacitor bank on $/J stored — usually the dominant driver cost for electrically-driven pulsed schemes |
| `C220108` | Divertor (steady-state, W monoblock cassettes) or target factory (IFE/MIF target manufacturing) | high-rep-rate target manufacturing factory (IFE/MIF) |
| `C220110` | Remote handling & maintenance equipment (rad-hardening tier x vessel geometry) | always (for this archetype) |
| `C220111` | Reactor-equipment installation & assembly (fraction of the CAS22 subtotal) | always (for this archetype) |
| `CAS21` | Buildings & site structures (reactor, turbine, hot cell, balance-of-plant) | always (for this archetype) |
| `CAS23` | Turbine plant equipment (thermal cycle; zero for direct-conversion / eta_th=0 plants) | zero if the design point is direct-conversion (no thermal cycle) |
| `CAS24` | Electric plant equipment (switchyard, transformers, plant distribution) | always (for this archetype) |
| `CAS26` | Heat rejection system (cooling towers, circulating water) | always (for this archetype) |
| `CAS27` | Special materials — initial reactor material inventory / blanket fill (distinct from C220101 structure) | always (for this archetype) |
| `CAS70` | Annualized O&M + scheduled component replacement (staffing-based) | always (for this archetype) |
| `CAS80` | Annualized fuel cost — consumables and enriched-isotope procurement | always (for this archetype) |

### Canonical `spec` field glossary (spec keys must come from here)

Use ONLY the canonical fields below when authoring the `spec` dict — these are
the kwargs `CostingInput` accepts for this archetype. The glossary tells you what
each field means, what unit the library expects, and which common confusions to
avoid (`p_fus` vs `p_input`, `B` vs `b_center`, kJ vs MJ, etc.). Read the
"Common confusions" block before writing `spec`.

{{canonical_spec_keys}}

## Required Reading (supporting)

- **Closest example (pattern to imitate):** `\home\reid\1cfe\1costingfe\examples\dt_tokamak.py`
- **1costingfe README:** `\home\reid\1cfe\1costingfe\README.md`
- **Costing constants:** `\home\reid\1cfe\1costingfe\src\costingfe\data\defaults\costing_constants.yaml`

## Concept Mapping
- **ConfinementConcept:** `LASER_IFE`
- **Fuel:** `DT`



## The Three-Forward Structure (emit literally, in this order)

Your script body, after the imports, is exactly these steps: `spec`, `model`,
the mandatory `generic` forward, the `overrides` registry, then one helper call
that returns `native` and `result_1gw`. Do **not** hand-roll the two-knob
`forward()` — the helper owns the overrides-on forwards and is the only accepted
shape. The three forwards are: **`generic`** (overrides off, design scale),
**`native`** (overrides on, design scale), **`result_1gw`** (overrides on, 1 GWe).
Each adjacent pair moves exactly one dimension.

```python
"""1costingfe model: Laser ICF NIF Commercialization (Focused Energy LIFE-class) (Inertia Enterprises).

Usage:
    uv run python model_setup.py              # print results
    uv run python model_setup.py | tee model_output.txt
"""
import sys
from pathlib import Path

# Make the shared three-forward helper importable regardless of where this file
# lives (concept dir or iter-N/ dir): walk up to the scripts/ root.
_SCRIPTS = next(
    p / "scripts"
    for p in Path(__file__).resolve().parents
    if (p / "scripts" / "lib" / "model_setup_helpers.py").exists()
)
sys.path.insert(0, str(_SCRIPTS))

from costingfe import ConfinementConcept, CostModel, Fuel
from lib.model_setup_helpers import (
    generic_reference, run_native_and_1gw, print_cas_breakdown,
)

# 1. Specification — design-point inputs only, at native scale.
#    Geometry / physics / power. NO library-default re-passing.
#    Use ONLY the canonical field names below (see archetype spec-key glossary
#    rendered after this block); names like B0, laser_pulse_energy_kJ,
#    rep_rate_hz, or target_gain are not in CostingInput and would be
#    silently dropped at forward() time. F7 (validator) catches this.
spec = dict(
    R0=...,        # arc-reactor-specifications.md §Geometry
    plasma_t=...,
    elon=...,
    p_input=...,   # AUXILIARY HEATING wallplug (MW), NOT fusion power
    # ... only canonical CostingInput fields the design point actually specifies
)
P_native = ...     # MWe — copied from the analysis Design Point block

# Toroidal coil-cost requirement (TOKAMAK / STELLARATOR only):
#   `plasma_t` is REQUIRED. 1costingfe's bilinear coil cost model computes
#   C220103 ∝ B × R₀ × r_coil, where r_coil = vessel_or =
#   plasma_t + blanket_t + ht_shield_t + structure_t + vessel_t. If the
#   source publishes only major radius R₀ and aspect ratio A, derive
#   `plasma_t = R₀ / A`. Leaving plasma_t unset falls back to the YAML
#   default (1.1m tokamak / 1.8m stellarator) which over-states most
#   published commercial designs.
#
# `r_bore` is silently unused for toroidal devices under the bilinear
# model (kept in YAML for backcasting compat only). Do NOT pass
# `r_bore = R₀` in spec for TOKAMAK / STELLARATOR; it's a no-op.
# Loop devices (MIRROR, FRC, DIPOLE, PULSED) still use r_bore for the
# r² coil model and must set it explicitly.

# 2. Model.
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
overrides = [
    {"account": "C220103", "value": 6901.0, "enabled": True,
     "provenance": "derived", "source": "arc-reactor-specifications.md §6",
     "rationale": "156 t HTS x $44k/kg (2024 CPI) = $6,901M; library default misses HTS unit cost."},
    # Relative example (references the mandatory `generic` line above):
    #   {"account": "C220101", "value": 0.70 * generic.costs.cas21, "enabled": True,
    #    "provenance": "derived", "source": "...", "rationale": "30% structure
    #    cost reduction from modular fab vs library default; 0.70 x library CAS21."},
    # ... one dict per Override Candidate; use overrides = [] if there are none.
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
```

## Hard Rules

1. **`model`, `generic`, `native`, `result_1gw` are module-level** (not inside a
   function or `if`-block). These are the three-forward contract: `generic`
   (forward 1, overrides off), `native` (forward 2, overrides on at design scale),
   `result_1gw` (forward 3, overrides on at 1 GWe). `result_1gw` is the
   standardized cross-concept number.
2. **Step 4 is the helper call**, exactly `native, result_1gw = run_native_and_1gw(
   model, spec=spec, overrides=overrides, p_native=P_native)`, and **`generic` is
   the mandatory standalone line** `generic = generic_reference(model, spec,
   P_native)` (Step 2b). An inline two-knob `forward(net_electric_mw=1000, ...)` is
   rejected by the contract validator. `noak=True` is the helper default — do
   **not** re-pass it.
3. **`spec` carries only design-point inputs.** Do NOT put the uniform
   financial / operating-economics parameters in `spec`: `availability`,
   `lifetime_yr`, `interest_rate`, `inflation_rate` are library-owned and MUST
   NOT appear. The helper sources `availability` / `lifetime_yr` from the library.

   **Low archetype-fit concepts: populate `spec` anyway.** When
   `Archetype-Fit: Low` (the closest available `ConfinementConcept` does
   not perfectly match the concept's architecture — e.g. modelling a p-B11
   FRC as `MIRROR` because the library has no `STEADY_FRC + PB11`
   calibration, or modelling an orbital-cycling levitated dipole as the
   stationary `DIPOLE`), still populate `spec` with the concept's
   published or inferred design-point values using the canonical-spec-key
   glossary above. Leaving `spec` empty produces the *worst possible*
   cost number — the library runs pure archetype YAML defaults at
   `P_native`, which encode "some generic mirror" or "some generic
   dipole" rather than this concept's actual machine.

   The geometry and physics fields (`R0`, `chamber_length`, `plasma_t`,
   `B`, `b_center`, `n_e`, `T_e`, `eta_p`, `p_input`, `plasma_volume`)
   are the right place to express the concept's actual scale, even when
   archetype-fit is Low. Cost-side overrides (the override registry in
   Step 3) are where you express how the library's archetype cost
   structure deviates from the concept's true cost story — that's where
   the "Low fit" caveat properly belongs.

   When mapping non-canonical concept-specific kwargs (e.g. Realta's
   `l_c`, `B_0c`, `P_NBI`) onto canonical names, document the mapping in
   inline comments and explicitly note any fields that have no canonical
   equivalent and were intentionally dropped.

   **Archetype-specific spec key blocklist (workarounds for known library
   bugs).** Some spec keys must NOT be passed for specific archetypes until
   the underlying library issue is fixed. Even if your concept's published
   design point has a value for one of these keys, **do NOT transcribe it
   into `spec`** — rely on the YAML default (which is a calibrated effective
   value, not the geometric one). Document the omission with a comment
   citing the tracker issue.

   - **DIPOLE** (`LASER_IFE == "DIPOLE"`): do **NOT** pass
     `plasma_volume`. The MFE radiation calc in `physics.py` treats
     `plasma_volume` as a uniform integrator (`P_brems ∝ n_e² × T_e^0.5 ×
     Z_eff × V`), which is calibrated for tokamak / stellarator profiles
     (200–1,000 m³, relatively flat). Dipole plasmas are highly stratified
     (Hasegawa-Mauel: `n ∝ R⁻⁴`, `T ∝ R⁻⁸ᐟ³`) with the radiating core
     <10% of the geometric volume. Passing Simpson's geometric 13,600 m³
     drives the inverse power balance to manufacture `p_fus ≈ 2,775 MW`
     and `p_input ≈ 846 MW` to compensate (vs Simpson's 667 / 44.5), and
     every CAS22 account that scales with `p_th` inflates by ~2.5×. The
     DIPOLE YAML's `plasma_volume = 200` default is an effective
     calibration value (not the geometric volume) that produces sane
     `p_fus ≈ 700 MW`. Library issue: **1cFE/1costingfe#24** (proposed
     fix: `radiation_peaking_factor` field).

   - **Power-conversion / wall-plug efficiencies are NEVER spec keys.** Across
     every archetype, the following are **not surfaced to the analyst as
     overridable** and must not appear in `spec`:
     `eta_th`, `eta_pin`, `eta_couple`, `eta_de`, `eta_dec`, `eta_p`,
     `eta_source_nbi`, `eta_source_icrf`, `eta_source_ecrh`, `eta_source_lhcd`.
     They are framework-owned defaults so cross-concept LCOE comparisons stay
     apples-to-apples. If a published design point has a value that differs
     from the library default, document it as an inline comment and accept the
     library value. To change the *global* default, update the per-archetype
     YAML or `CostingConstants` in 1costingfe — not the per-concept spec.
     This supersedes the partial strip in commit `9142788` (May 29 2026, which
     covered `eta_th`/`eta_de`/`eta_dec`/`f_dec`/`eta_pin1`/`eta_pin2` but
     missed `eta_pin`/`eta_couple`/`eta_p`/`eta_source_*`). The strict-kwarg
     validator on 1costingfe master rejects `eta_pin` outright for NBI/RF-
     heated concepts, and the canonical glossary now omits the remaining
     efficiency keys from `_archetype_fields` regardless of YAML or
     `_OPTIONAL_OVERRIDE_KEYS` membership.

   - **`p_fus` is never a spec key.** The library back-solves fusion power
     from `p_input` + plasma parameters via the inverse power balance. If
     the source publishes a fusion power, transcribe it as a documentation
     comment, do not put it in `spec` — the strict-kwarg validator rejects
     `p_fus`.

   - **MIF concepts** (`LASER_IFE ∈ {MAG_TARGET, MAGLIF,
     PLASMA_JET}`): the MIF forward path does not accept MFE/IFE-only
     kwargs. In particular `f_dec`, `p_input`, `eta_p`, `eta_pin`,
     `eta_de` are not in the MIF `forward()` signature and will be
     rejected by the strict-kwarg validator. Honor the per-archetype
     canonical glossary rendered above — it only lists kwargs the
     archetype actually consumes.
4. **No `# DEFAULT: ...` comments.** An account you don't override is already
   handled by the library — do not re-pass or annotate defaults. Cite the source
   for the values you *do* set with a normal inline comment.
5. **Overrides are six-field dicts** (`account`, `value`, `enabled`, `provenance`,
   `source`, `rationale`), `account` from the canonical schema above, `provenance`
   ∈ `{direct, derived}`, no two entries sharing an `account`. `value` may be a
   number, a constant expression (e.g. `260.0 * 1.34`), or a **relative** override
   expressed as a fraction of the library's own cost: reference the mandatory
   `generic` line. `generic` is the library's bare overrides-off answer at the
   design point — do NOT reference `native` or `result_1gw` (overrides-on; wrong
   reference frame) or `result` (the removed two-forward name); the validator
   rejects all three.

   **Two relative-override patterns are accepted**, each tied to where the
   library actually stores the value:

   ```python
   # Top-level CAS rollup (CostResult attribute):
   {"account": "C220101", "value": 0.70 * generic.costs.cas21, ...}

   # Per-account CAS22 sub-account (cas22_detail dict):
   {"account": "C220103", "value": 0.85 * generic.cas22_detail["C220103"], ...}
   ```

   The library exposes top-level CAS rollups (`cas10`, `cas21`, `cas22`, …,
   `cas70`, `cas80`, `cas90`, `total_capital`, `lcoe`, `overnight_cost`) as
   attributes on `generic.costs`. The CAS22 sub-accounts (`C220101`–`C220112`,
   plus rollup/plant-aggregate keys `C220000`, `C220200`–`C220700`) live as
   **dict keys** under `generic.cas22_detail`, **not** as attributes —
   `generic.costs.c220103` does NOT exist (the validator rejects it). Pick the
   pattern that matches the storage shape: top-level `cas21`, `cas22`, … →
   `generic.costs.<name>`; per-account `C220xxx` →
   `generic.cas22_detail["C220xxx"]`.

   **`value` is in M$ (megadollars)** — never raw dollars. The validator rejects
   any literal value above 50,000 (= $50 B per CAS account) as a raw-$ unit
   error. If you mean $20M, write `value: 20.0`, NOT `20.0e6`.

   **Derived rollup accounts are forbidden as override targets.** The library
   computes `C220111 = installation_frac × (C220101+…+C220110)` and the
   `Cxxx000` rollups as coefficient × sub-totals; overriding their rolled-up
   dollars bypasses the formula and locks a stale snapshot. To express
   "this concept assembles more simply," override the *coefficient* via
   `costing_overrides: {installation_frac: ...}`, not the C220111 dollars.
   The validator rejects C220111, C220000, C220100, C220200, C220300,
   C220400, C220500, C220600, C220700.

   **Disabled overrides MUST carry a `blocked_by` issue link.** Any entry
   with `enabled: False` must also include a 7th field `blocked_by:
   "<org>/<repo>#<issue>"` (e.g. `"1cFE/1costingfe#42"`) pointing at an open
   tracker issue. This routes library-side findings ("this account should be
   zero for dipoles," "library default is wrong") to a tracker instead of
   letting them die in the `rationale` text. The validator rejects disabled
   entries without `blocked_by`, and `blocked_by` strings that don't match
   `org/repo#NN`.

   **Every override MUST declare `cost_basis: "noak"` (strict).** The
   framework runs `noak=True` everywhere; only NOAK-vintage values compose
   correctly with that target. Any other value (`foak`,
   `conceptual_design`, `vendor_target`, `unspecified`, …) is rejected.
   If your source publishes a non-NOAK number (e.g. Sorbom 2015's
   `$1.06M/tonne` mass scaling, NIF's actual FOAK cost, a paper without
   FOAK/NOAK labels at all), you have three honest options:
   (a) **defer to the library default** — disable the override and cite a
       tracker issue in `blocked_by`;
   (b) **adjust to NOAK with documented derivation** in `rationale` (apply
       a learning-curve factor with explicit reasoning, e.g. *"$5.1B
       Sorbom 2014 × 0.2 (10× learning: REBCO conductor + structural-fab
       mass mfg, 2014→2026) = $1.02B NOAK"*) and declare `cost_basis:
       "noak"`;
   (c) **file a tracker issue** if the strict rule misses a genuine case.
   Do NOT mark `cost_basis: "noak"` to silence the validator if the
   methodological reconciliation hasn't been done in `rationale`.
6. **Power-conversion efficiencies are ENUM-driven — never in `spec`.** `eta_th`,
   `eta_de`, and `eta_dec` are the efficiencies of specific conversion hardware
   (thermal cycle, magnetic DEC, inductive DEC). They are owned by costingfe and
   determined by the concept's `PowerCycle` ENUM (for `eta_th`) and per-`ConfinementConcept`
   YAML defaults (for `eta_de` / `eta_dec`). To express a *different* value,
   add an ENUM member upstream in costingfe (a new `PowerCycle` variant, or a
   refined `ConfinementConcept`) — never override the efficiency directly in
   `spec`. A company-published "optimistic" number is NOT a reason to override
   the library default; neither is "this concept does direct conversion" (the
   correct expression is the concept's ENUM choice + `f_dec`, see Rule 6b).
   Discipline test: "to express a different efficiency, would I add an ENUM
   value upstream?" — if yes, that's the right path; if you're tempted to set
   the kwarg directly in `spec`, stop and use the ENUM instead.

6b. **`f_dec` (DEC fraction) MAY appear in `spec` with provenance.** `f_dec`
   is the *fraction of fusion power routed through DEC* — a physics+architecture
   property, not a hardware-efficiency claim. Two concepts in the same ENUM
   can legitimately differ on `f_dec` (e.g. one mirror has end-cell DEC, another
   doesn't). Override with the same six-field provenance record as any other
   override, sourced from the concept's published architecture (not from
   efficiency claims).
7. **Sweeps / sensitivity `print()` output is allowed** below the steps; only
   `generic`, `native`, and `result_1gw` are the standardized forwards. Do not add
   `scaled_headline` and do not compute sensitivities for `result_1gw`.

## Output
Write the script to: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\30-laser-icf-nif-commercialization\iter-1\model_setup.py`
