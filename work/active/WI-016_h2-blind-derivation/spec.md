---
Status: active
Scale: standard
Epic: "Pipeline De-Risk & Demonstration"
Owner: reid
Created: 2026-07-04
---

# WI-016 — H2 Probe: Blind Physics Derivation

## Goal

Controlled experiment: can an agent derive good fusion physics/costing relations from the research corpus plus its own physics knowledge, WITHOUT access to the in-house costing code (1costingfe)? The costing code is the held-out answer key. A separate agent will later compare the derived relations against it. This phase produces the derivations and an instrumented process log; it does no comparison and writes no SysML.

## Firewall — read-whitelist (absolute)

The deriving agent may read ONLY:

- `knowledge/concept_research/` (the 39 concept research dossiers)
- `knowledge/sources/` (ingested source documents)
- `knowledge/SOURCE_INDEX.md`
- its own working dir `work/active/WI-016_h2-blind-derivation/`

It may NOT read anything else — not `models/`, not `archive/`, not `exploration/`, not `.project/`, not `work/` outside its dir, not `~/1cfe/1costingfe`, not `~/1cfe/sysml-codegen`, no web fetching. If any file opened quotes costing-code formulas (references to "1costingfe", "cas22.py", "tokamak.py", "physics.py" formulas, or "PyFECONS" code), the agent stops reading that passage and logs the near-miss in the process log.

Within dossiers: `model_setup.py` files contain values COMPUTED by the costing code — computed values are off-limits as derivation inputs. Source-quoted values (parameters citing papers, e.g. Sorbom 2015 ARC specs) are fine and encouraged.

## Scope — three relations, with full working shown

1. **Tokamak fusion power** P_fus(R, a, kappa, B) plus justified operating-point closures (density limit, safety factor, temperature choice, reactivity).
2. **MFE power balance**: fusion power + heating + efficiencies/parasitics -> gross/net electric, engineering Q, recirculating fraction, alpha/neutron split for D-T.
3. **Magnet/coil capital cost scaling**: physically justified scaling form, constants anchored to source-quoted data.
4. Stretch: modular-stellarator variant of the coil relation.

## Success criteria

- Every relation has: derivation chain, per-input source citation (corpus file+section, or explicit "pretraining: <reference>" declaration), validity range, and a worked ARC-class numeric example (R ~ 3.3 m) giving predicted P_fus, net electric, magnet cost.
- `process_log.md` records every search, source consulted, dead end, judgment call, pretraining fallback, and firewall near-miss.
- No costing-code formulas used as inputs; no comparison attempted.

## Deliverables

- `spec.md` (this file)
- `derivation.md`
- `process_log.md`
