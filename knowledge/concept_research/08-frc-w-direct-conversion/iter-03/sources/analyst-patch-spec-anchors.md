---
source: "analyst-derived"
source_type: "analyst-patch"
extracted_at: "2026-06-09T08:10:00+00:00"
author: "Mallory Snowden"
provenance_pr: "fusion-tea PR #5216006 (structural pulsed-conversion refactor for 08 + 31), #9142788 (NOAK strip), #409cf62 (cold-start re-roll under 1 GWe override-semantics policy)"
patch_class: "spec_anchor_with_enum_constraint"
---

# Analyst-Verified Spec + ENUM Constraints: Helion PULSED_FRC + Direct Conversion

**Why this source exists.** Documents the verified spec values for Helion's
Orion design point (Microsoft PPA target, 50 MWe), and critically documents
the **ENUM-owned efficiency fields** that must NOT appear in spec.

## Architectural mapping: PULSED_FRC + INDUCTIVE_DEC

The library has dedicated handling for Helion's pulsed colliding-FRC concept:
`ConfinementConcept.PULSED_FRC`. This automatically uses
`PulsedConversion.INDUCTIVE_DEC` (inductive direct energy conversion), which
carries the energy-conversion efficiency in the ENUM, not as a spec value.

**Helion's claimed 85-95% direct-conversion efficiency is NOT settable through
spec.** It would require adding a new `PulsedConversion` variant in costingfe
upstream (or overriding `eta_dec` at the cycle level, which is also
PowerCycle-ENUM-owned). The library default INDUCTIVE_DEC efficiency is used
as-is until upstream library changes ship.

## Verified spec values (transcribe verbatim)

| Parameter | Value | Source |
|-----------|-------|--------|
| `q_eng` (engineering Q) | 4.0 | Inferred from need for net gain after recirculating power; consistent with Helion's published Q claims for Orion-class |
| `f_rep` (Hz) | 1.5 | Midpoint of 1-2 Hz range — docslib-helion-arpa-e-presentation.md §Power ("50 MW at 2 Hz"); helion-website-technology.md ("possibly 2 Hz to 10 Hz") |
| `P_native` | 50.0 MWe | Microsoft PPA target — helion-prototype-generations.md §Orion; contrary-research-helion.md §Power Output |
| `ConfinementConcept` | `PULSED_FRC` | Library's pulsed colliding-FRC class |
| `Fuel` | `DHE3` | D-He3 commercial fuel target; self-breeding via DD side reactions |

## What NOT to set (ENUM-owned + non-applicable geometry)

- **`eta_dec`** — ENUM-owned by `PulsedConversion.INDUCTIVE_DEC`. NOT a spec key.
- **`eta_th`** — ENUM-owned by `PowerCycle`. NOT a spec key.
- **`B0` (compression field)** — Not directly a `forward()` parameter for PULSED_FRC;
  library derives field from stored-energy / power-balance internals.
- **`e_stored_mj` (stored energy)** — Not in spec dict; library computes from q_eng,
  f_rep, P_native via internal pulsed-power balance.
- **`R0`, `plasma_t`, `elon`** — Pulsed linear FRC geometry doesn't map to
  tokamak-style major-radius / elongation. OMIT.
- **`f_dec`** — for PULSED concepts, the `PulsedConversion` ENUM determines the
  conversion path. Do not pass.

## Architectural reasoning

Helion's pulsed colliding-FRC concept has limited published geometry. The
chamber is described as "~2× Polaris" with Polaris at "~60 ft length"
(helion-prototype-generations.md), implying Orion ~30-40 m length, ~2-3 m
diameter. Detailed R0, plasma_t, elon are not applicable (linear concept,
not toroidal) or not disclosed.

The library's PULSED_FRC class encodes Helion-class geometry assumptions via
its YAML defaults; we provide only what's sourced and let the library fill
the rest.

## Model directive (machine-parseable)

```yaml
model_directives:
  spec:
    q_eng: 4.0
    f_rep: 1.5
  P_native: 50.0
  ConfinementConcept: PULSED_FRC
  Fuel: DHE3
  do_not_set:
    - eta_dec           # ENUM-owned by PulsedConversion.INDUCTIVE_DEC
    - eta_th            # ENUM-owned by PowerCycle
    - B0                # not a PULSED_FRC forward param
    - e_stored_mj       # library computes from q_eng, f_rep
    - R0                # linear concept, not toroidal
    - plasma_t          # linear concept, not toroidal
    - elon              # linear concept, not toroidal
    - f_dec             # ENUM-owned (PulsedConversion)
  rationale: "Helion Orion 50 MWe Microsoft PPA target; PULSED_FRC class uses library YAML defaults for non-sourced geometry."
  provenance: "direct"
  upstream_blocker:
    description: "Helion's claimed 85-95% direct-conversion efficiency would need a new PulsedConversion variant in costingfe upstream — track as a 1costingfe issue, do not work around with spec key."
```

## Sources cited (already in research corpus)

- `helion-prototype-generations.md` §Orion — chamber sizing, Microsoft target
- `docslib-helion-arpa-e-presentation.md` §Power — 50 MW at 2 Hz
- `helion-website-technology.md` — 2-10 Hz rep rate range
- `contrary-research-helion.md` §Power Output — corroborating

## Maintenance

If Helion publishes specific stored-energy, compression-field, or D-He3 fuel
mix values, supersede with company source. If costingfe adds a higher-eta
PulsedConversion variant, update the upstream_blocker reference.
