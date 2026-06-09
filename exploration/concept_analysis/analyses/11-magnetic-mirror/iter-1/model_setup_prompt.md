# 1costingfe Model Setup: Magnetic Mirror (Realta Fusion / CoSMo)

You are generating a runnable 1costingfe model setup script for **Magnetic Mirror (Realta Fusion / CoSMo)**
(Realta Fusion). The script must run via `uv run python model_setup.py` and emit an
LCOE estimate.

## The contract in one sentence

The design point is already chosen, the 1costingFE library already carries the
default cost story, and your job is to transcribe the fixed design point into the
**three-forward helper form** and add only the **evidence-backed overrides** the
analysis already discovered — nothing else.

## Step 0: Read the Design Point block from the analysis (primary source)

**Start here.** Open `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\11-magnetic-mirror\analysis.md` and read its `## Design Point` block and
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

- Name: Hammir pilot plant — Frank et al. 2024 conservative operating point (Realta Fusion)
- Maturity: paper-concept
- P_native: 50 MWe
- Grounding: medium
- Primary sources:
  - knowledge/concept_research/11-magnetic-mirror/iter-01/sources/arxiv-2411-06644-confinement-predictions.md
  - knowledge/concept_research/11-magnetic-mirror/iter-01/sources/aps-dpp-2025-sutherland.md

(Selection fields are orchestrator-fixed from the design-point table. Copy them verbatim; you are forbidden to edit them. The quantitative description of this plant belongs in Section 5.)

### Canonical account schema (override codes must come from here)

| Account | What it costs | Applies when |
| --- | --- | --- |
| `C220101` | First wall, blanket & neutron multiplier (DT: tritium-breeding blanket; DD/aneutronic: energy-capture blanket) | always (for this archetype) |
| `C220102` | Radiation shield (sized to neutron wall loading; scales down for low-neutron fuels) | always (for this archetype) |
| `C220103` | Confinement magnets / coils (HTS-REBCO conductor + winding + cryostat) | always (for this archetype) |
| `C220104` | Supplementary plasma heating (steady-state) or primary pulsed driver (laser/accelerator/gun) | supplementary heating (NBI/ICRF/ECRH/LHCD) per installed MW |
| `C220105` | Primary structure — gravity supports, thermal shields, inter-coil structure, machine base | always (for this archetype) |
| `C220106` | Vacuum system — vessel, port extensions, cryopumps, leak detection | always (for this archetype) |
| `C220107` | Power supplies (steady-state magnet supplies / switchgear) or pulsed-power capacitor bank ($/J stored) | DC magnet power supplies and switchgear |
| `C220108` | Divertor (steady-state, W monoblock cassettes) or target factory (IFE/MIF target manufacturing) | divertor (W monoblock cassettes on CuCrZr heat sinks) |
| `C220109` | Direct energy converter (electrostatic for mirror/FRC exhaust, or inductive DEC on a pulsed driver) | only if the design point uses direct energy conversion (directed axial exhaust or an inductive DEC stage) |
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

- **Closest example (pattern to imitate):** `\home\reid\1cfe\1costingfe\examples\dt_mirror.py`
- **1costingfe README:** `\home\reid\1cfe\1costingfe\README.md`
- **Costing constants:** `\home\reid\1cfe\1costingfe\src\costingfe\data\defaults\costing_constants.yaml`

## Concept Mapping
- **ConfinementConcept:** `MIRROR`
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
"""1costingfe model: Magnetic Mirror (Realta Fusion / CoSMo) (Realta Fusion).

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
model = CostModel(concept=ConfinementConcept.MIRROR, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
#     `generic` is the library's overrides-off forward at P_native. It is BOTH the
#     writing frame for relative overrides AND the reference the framework rescales
#     against at projection time (see `_scale_overrides` in
#     1costingfe/src/costingfe/model.py). Under the headline invariant, a relative
#     override lands on `M x (the library's 1 GWe fleet cost for that account)`
#     regardless of class — the framework rescales your native-frame anchor to the
#     fleet frame by the per-account ratio fleet_cost/native_cost, so you never
#     compute that ratio yourself. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
overrides = [
    {"account": "C220103", "value": 6901.0, "enabled": True,
     "provenance": "derived", "source": "arc-reactor-specifications.md §6",
     "rationale": "156 t HTS x $44k/kg (2024 CPI) = $6,901M; library default misses HTS unit cost."},
    # Relative example (references the mandatory `generic` line above). The value
    # anchors to the account's OWN storage location, and the rationale names the
    # modular-fleet baseline (see the override-semantics policy in Rule 5):
    #   {"account": "C220101", "value": 0.70 * generic.cas22_detail["C220101"],
    #    "enabled": True, "provenance": "derived", "source": "...", "rationale":
    #    "Modular fab cuts this concept's first-wall/blanket to 70% of the library's
    #    per-module C220101 for a 1 GWe fleet of this device; the fleet then pays
    #    0.70 x n_mod x that per-module cost. Baseline: the library's modular-fleet
    #    default, NOT a conventional 1 GWe plant."},
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

   - **DIPOLE** (`MIRROR == "DIPOLE"`): do **NOT** pass
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

   - **MIF concepts** (`MIRROR ∈ {MAG_TARGET, MAGLIF,
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

   **What a relative override means at the headline — read this before authoring
   any `M * generic...` value.** The override-semantics policy below is the same
   one the analysis agent reads; it carries the single invariant, the S/U/P cost
   classes, and the modular-fleet rationale baseline.

# Override semantics and the 1 GWe headline

## The invariant (this is the whole rule)

Every concept's headline is one number: LCOE for a **1 GWe NOAK plant**, reached
by **replicating** the real `P_native` design point into a fleet of `n_mod`
identical modules (`run_native_and_1gw(...)`, `noak=True`). There is no monolithic
1 GWe machine — we never extrapolate the physics model to a single 1000 MWe
reactor we have no design basis for.

At that headline, for **every account in every class**:

    account = M × (the library's 1 GWe fleet cost for that account)

`M` is the fraction of the library's fleet answer you believe this concept should
pay. `M = 1.0` means "trust the library default"; you only write an override when
evidence says this concept departs from it. That is the entire authoring rule.

The framework guarantees this invariant regardless of *which* `generic` value you
anchor to: `_scale_overrides` (in `1costingfe/src/costingfe/model.py`) rescales
your override from the native frame to the fleet frame by the per-account ratio
`fleet_cost / native_cost`, so the headline always lands on `M × fleet_cost`. You
do **not** compute that ratio yourself — you pick the right `generic` anchor for
the account's storage shape (below) and the framework does the rest.

## The cost classes — comprehension, not three rules

The classes below explain **why** the fleet cost is what it is (so you can sanity-
check `M`) and dictate the **authoring shape** — which `generic` value you anchor
to. They do **not** introduce per-class multipliers. If you delete the table, the
invariant above still tells you what an override means; the table only tells you
*where to anchor it* and *why the fleet cost looks the way it does*.

| Class | Why the fleet cost is what it is | Authoring shape (what to anchor to) | Accounts |
|---|---|---|---|
| **S — Shared / fixed** | A site needs these **once**, however many modules it runs — the library charges them once across the fleet. That single charge *is* the amortization that gives a small machine a fair shot. | whole-plant M$ → `M * generic.costs.<rollup>` | CAS10, CAS21, CAS28, CAS40, CAS70 |
| **U — Per-unit** | One per module: `N` modules → `N` cores. The library multiplies by `n_mod`; `noak=True` credits mass-production learning as the offset for losing single-core economy of scale. | per-module M$ → `M * generic.cas22_detail["C2201xx"]` | CAS22 reactor-island sub-accounts `C2201xx`; CAS80 fuel (taught, but not overridable today — see note) |
| **P — Power-proportional** | Scales with the **total** plant power, so the value is the same whether you replicate or not. | whole-plant M$ → `M * generic.costs.<rollup>` | CAS23, CAS24, CAS25, CAS26, CAS27; plant-wide CAS22 sub-accounts `C2202xx`–`C2207xx` |

**Storage-shape footnotes (which `generic` attribute exists):**
- Only the CAS22 reactor-island sub-accounts (`C2201xx`) live under
  `generic.cas22_detail["C220xxx"]`. Everything else — CAS21, CAS23–27, CAS70,
  CAS80, and the CAS22 rollup — is a top-level attribute on `generic.costs`.
- **Taught but NOT overridable today: CAS40 (owner's costs), CAS70 (O&M), and
  CAS80 (fuel).** Overrides on these are silently dropped — e.g. a CAS80 override,
  whether absolute (`0.050`) or relative (`M * generic.costs.cas80`), leaves the
  fleet value at the library default and does **not** move the headline
  (`1cFE/1costingfe#106`; the CAS70 / CAS80 no-op is pinned by
  `1costingfe/tests/test_override_scaling_semantics.py`). They are in the class
  table so you know *why* the library prices them as it does (and so a future
  override surface lands on prepared ground) — but do **not** author an override
  against them expecting an effect. Use only codes from the canonical account
  schema you are given.

**Reading the output — how to verify a Class-U override actually scaled:**
The `print_cas_breakdown` **CAS22 sub-account detail table shows per-module M$ at
every scale** — its `native` (n_mod=1) and `1 GWe` (n_mod=200) columns are
*supposed to be identical* for a `C2201xx` row, because the per-module cost does not
change; the ×`n_mod` fleet multiplication shows up in the **`C220000` / `CAS22`
rollup**, not in the detail row. So a Class-U detail row that reads the same at
native and 1 GWe is **expected, not a scaling failure.** To confirm a Class-U
override reached the fleet, check that the **`CAS22` (or `C220000`) rollup** moved
by roughly `Δ(per-module value) × n_mod` — never infer "it didn't scale" from the
detail row alone.

## The rationale baseline (one named frame, always)

Every relative override's `rationale` answers "why is `M` what it is?" against
**one** named baseline:

> **the library's default for a fleet of this device at 1 GWe.**

Never against "a conventional 1 GWe plant" / a monolithic 1000 MWe machine — under
the always-replicate decision that baseline does not exist. Anchor the rationale
to the same frame as the value. (Citing a monolithic plant from the literature as
a *comparable* — ARC, STEP — is fine; using one as the override's *anchor
baseline* is the inconsistency this policy removes.)

A multiplier above 1.0 is legitimate: it means "this concept's account costs more
than the library's modular-fleet default" (e.g. a harder-to-build module), still
in the fleet frame — not "more than a conventional plant."

## What wrong looks like

- **Value/rationale frame mismatch.** Value reads `0.70 * generic.cas22_detail["C220101"]`
  (70% of one module's blanket) while the rationale says "70% of a conventional
  1 GWe plant's blanket." The value is per-module fleet-frame; the rationale is
  monolithic. Rewrite the rationale in the modular-fleet frame.
- **Monolithic baseline in rationale.** Any "vs a conventional / standard 1 GWe
  plant," "vs a monolithic reactor," or bare "vs library default" with no fleet
  frame. Replace with "vs the library's 1 GWe modular-fleet default."
- **Class/anchor mismatch.** Overriding a CAS22 sub-account (Class U) but anchoring
  to a top-level rollup (e.g. `C220101` valued against `generic.costs.cas21`).
  Anchor each account to its own storage location: `C2201xx` →
  `generic.cas22_detail["C2201xx"]`; top-level rollups → `generic.costs.<rollup>`.


   **Two relative-override patterns are accepted — pick the one that matches your
   account's storage shape** (the "authoring shape" column in the class table
   above): a top-level rollup anchors to `generic.costs.<rollup>`; a CAS22
   reactor-island sub-account anchors to its own `generic.cas22_detail` entry. The
   value's anchor MUST match the account you are overriding — do not override a
   sub-account while anchoring to a top-level rollup (the class/anchor mismatch the
   policy calls out).

   ```python
   # Top-level CAS rollup (Class S or P) — anchor to generic.costs.<rollup>:
   {"account": "CAS24", "value": 0.85 * generic.costs.cas24, ...}

   # CAS22 reactor-island sub-account C2201xx (Class U) — anchor to its OWN
   # cas22_detail entry (per-module M$; the framework multiplies by n_mod):
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
Write the script to: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\11-magnetic-mirror\iter-1\model_setup.py`
