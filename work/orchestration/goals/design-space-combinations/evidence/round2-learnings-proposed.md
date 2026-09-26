## L-009 — Four cross-plant assemblies execute on existing definitions with no definition or body change; three previously untested combinations satisfy every evaluated check

- **Evidence:** `work/active/WI-093_combination-assemblies/report.md` § 2–3; `evidence/native_runs/summary.json`, `verification-summary.json` (11 of 11), `build-hashes.json` (21 bodies prefix-only, 0 adapters).
- **Scope:** the definitions at `7cb0ae46`, assembled as flat packages of parts in the ARIES pattern.
- **Implication:** the usable design space is larger than the two plants; the reuse limit is a short list of named missing relationships (answer § 4), not a per-combination custom calculation.
- **Supersedes:** extends L-002 from an input mapping to an assembled loop with its own calculated flow.

## L-010 — Lowering the Brayton stage pressure ratio at a 500 °C source raises net electricity while failing heat removal: the objective and the requirement move in opposite directions under one choice

- **Evidence:** C-1 cases `c1-aries-ratios-reselected-ratings` (ratio 1.518: net 426.58, unmet 0) and `c1-ratio1.35-reselected-ratings` (ratio 1.35: net 575.23, unmet 278.15, heater inlet 423 → 497 K, compressor work 2,451.5 → 1,719.9).
- **Scope:** the ARIES three-stage chain fed by one 773 K loop at 2,500 kg/s.
- **Implication:** a ratio chosen on net alone would leave 8 % of the source heat unremoved; the heat-removal check is what makes that visible, so the two must be read together (single evaluations, not a factorial study).
- **Supersedes:** none.

## L-011 — Under the ARIES chain, which check a plasma profile change flips depends on the direction of the fusion-power change: reductions clear every check, an increase flips fuel processing first

- **Evidence:** C-2 cases `c2-ne0-4.2e20` and `c2-peaked-profile` (p_fus 1,941.5 and 2,013.1, 13 of 13 satisfied) against `c2-flat-temperature` (p_fus 5,047.0: fuel processing margin −4.05e21 atoms/s, helium duty −718.6, PbLi duty −1,058.4, heat removal 3,052 MW unmet; net 810 → 831 only, the compressor never limiting).
- **Scope:** the Stellaris parabolic plasma on the ARIES nominal hardware (1,400 kg/s).
- **Implication:** the cross-plant form of B3: the same downstream equipment shows the core choice's consequence in the fuel and blanket ratings, not in the cycle, because the fixed cycle stream caps what the cycle can accept. Complements L-005 (where heat removal binds first over 4.75–5.75e20 on the hollow profile).
- **Supersedes:** none.

## L-012 — (process) The stock generator renders output aliases by part path and expression-module class names by grandparent path, so several design packages in one tree must not share part names; one root part per assembly is the working shape

- **Evidence:** `evidence/generation.log` history in design § 11 (`SI_RENDERING_COLLISION`, `REGISTRY_CLASS_NAME_COLLISION`); `sysml_codegen/elaboration/project.py` `_build_output_aliases`.
- **Scope:** multi-package staged trees for `sysml-codegen generate`.
- **Implication:** wrap each assembly in a root part (the Stellaris nesting shape) and give expression attributes package-unique names; a tooling finding for the generator's owner.
- **Supersedes:** none.

## L-013 — (process) The reuse rule's prefix rewrite has two forms: the import statement and a string literal built for importlib in shared helpers; a bare commit after a pathspec add commits whatever the owner had staged

- **Evidence:** `exploration/combinations/build.py` (`forms`, reverse-rewrite assertion); trail T-005 commit note (`f720a0be` superseded by `5723dfa6`).
- **Scope:** every goal that copies bodies between packages or commits in a shared checkout.
- **Implication:** assert the reverse rewrite reproduces the source; commit with `git commit -- <paths>`.
- **Supersedes:** none.
