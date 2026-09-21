---
date: 2026-09-20
researcher: Codex with independent source and scientific reviewers
topic: Stellaris magnetic-field calculation qualification
research_type: source sufficiency and mathematical identifiability
tags: [stellarator, magnets, field, geometry, applicability]
---

# Stellaris magnetic-field calculation: evidence and missing inputs

## Research question

What magnetic-field calculation can be scientifically supported for the declared Stellaris-based coil family while preserving independently chosen geometry, winding packs and currents?

## Summary

- The primary paper specifies six coil families, their approximate currents/turns/pack dimensions and published field values. These scalar tables do not determine the three-dimensional current paths or finite-pack placement.
- The published peak-field calculation uses finite winding packs. The two-term source surrogate requires configuration-specific coefficients obtained by varying pack size in magnetic calculations. One reference point cannot determine both coefficients.
- Common current scaling at fixed geometry and complete geometric similarity have physically justified relative responses under a linear magnetostatic assumption. They do not establish absolute calibration or validate independent shape/pack changes.
- No identity-matched executable baseline input set has been acquired in this investigation. A newer author dataset remains a concrete unresolved lead; this is not a claim that the geometry is unavailable publicly.

## Source-supported facts

Stellaris has 48 modular coils in four periods, with six independent families and their mirrored counterparts per period. Table 8 gives different currents and square winding packs for those families. The paper describes a uniform current density across each finite pack in its three-dimensional COMSOL calculation, and explicitly states that peak field depends on pack size. The primary-PDF images are the authority because older markdown table extractions are corrupted. Locators and inspected page images are retained in `.project/active/aries-comparison-preparation/field-qualification/evidence/local-inventory.md`; the underlying primary paper is DOI 10.1016/j.fusengdes.2025.114868, PDF pp. 3–4 and 22–23. Its PDF p. 34 states that data are available on request.

Lion 2021 §3.7, Eq. 39, expresses peak field as a current/clearance factor times a bracket containing two configuration-specific terms, one varying with major radius divided by square root of pack area. The coefficients are obtained from finite-pack magnetic calculations, not from a single tabulated peak. See `knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/output.md:404–455` and the primary equation image `images/lion_2021_nf_stellarator_process.pdf-0009-19.png`.

Lion 2023 §2.3.5 defines the axis field using an arclength integral and the corresponding configuration-specific current scaling in Eqs. 2.65–2.66. It describes finite rectangular beams and a pack-size fit. See `knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/output.md:1301–1337` and the equation images ending `0067-03.png`, `0067-05.png` and `0068-03.png`. This is the method's convention; the Stellaris table's vacuum-versus-finite-pressure field convention remains to be resolved for precise reproduction.

The six Table 8 family columns cannot substitute for six controlled pack-size experiments. They describe different interacting coils with different shapes and currents in one configuration. No shared two-coefficient fit is justified by treating those columns as a pack sweep.

## Identifiability and supported scaling

Eight exact rational checks in `.project/active/aries-comparison-preparation/field-qualification/evidence/identifiability.py` demonstrate the ambiguity without evaluating a plant. Two positive coefficient pairs reproduce the same normalized reference while giving different peak responses to an independent pack change. Both reproduce proportional-current and complete-similarity scaling. The illustrative coefficients are algebraic counterexamples, not physical bounds, inferred uncertainty, or proposed parameters. The independent reviewer reproduced the complete result and inspected the equations.

Common current scaling requires preserving the full signed family-current distribution. Geometric similarity requires scaling paths, finite packs and observation locations together. Changes in plasma equilibrium or nonlinear magnetic materials require separate treatment. A one-dimensional layer sum and two scalar radii cannot certify that these conditions hold.

## Public-source search

The official public-CAD README captured at `knowledge/sources/proxima_fusion_public_simplified_stellarator_cad_models/output.md` describes a simplified scaled-W7-X model. It does not identify the published Stellaris baseline. The author dataset landing page at `knowledge/sources/coilsets_and_scripts_from_augmented_lagrangian_methods_for/output.md` identifies Zenodo 18497939 and an associated optimization publication; it does not establish the identity or sufficiency of individual archive members. Both are captured primary landing pages, not validated magnetic inputs. Bounded search and focused follow-up records are under `knowledge/research/requests/REQ-STELLARIS-FIELD-GEOMETRY-01.json` and `REQ-STELLARIS-FIELD-GEOMETRY-02.json`. Their acquisition outcomes and unresolved items must accompany any data-availability statement.

The focused follow-up registered the author's Stellaris script at a pinned revision, `knowledge/sources/author_stellaris_augmented_lagrangian_script_at_a79006b/raw.html`. The ordinary markdown extractor omitted the code, so the captured HTML's embedded `rawLines` array was decoded without execution. The derived text is `.project/active/aries-comparison-preparation/field-qualification/evidence/author-stellaris-script.txt`. Lines 6–7 describe the boundary as available on request; lines 71–113 require `tests/test_files/input.stellaris` and `tests/test_files/coils.stellaris`; lines 146–169 and 254–275 initialize and write alternative optimized coils separately. Neither original input file was acquired. The uninspected archive remains an unresolved lead, not evidence of public absence.

The associated paper was rejected by the source registry's hold-out content screen; its content was not adopted. The isolated author script was acquired through the normal registry. Three primary captures in total support the search record; none is a complete geometry/current/pack payload. No rejected paper was cropped or registered around that decision.

## Feasibility and next action

The method is feasible once the inputs exist. A defensible baseline calculation needs closed coil curves and symmetry conventions, signed family currents, finite-pack frames/dimensions/current distribution, a matching axis or reproducible axis calculation, and reference field data with convergence and peak-search conventions. The complete contract and an unsent author-data request are retained in `.project/active/aries-comparison-preparation/field-qualification/capability-contract.md` and `data-request-draft.md`.

No model equation or source range was changed. Current calculations remain unqualified approximations outside their established evidence. Do not fit coefficients to a different design's field or replace missing geometry with a drawing-derived surrogate. If only another public coil configuration is available, selecting it is an explicit new design decision.

## Knowledge status

No new domain insight is approved by this document. DI-010 and DI-011 describe earlier conductor/field relationships and calibration work; this investigation adds limits on interpreting shape and pack transfer, rather than a new conductor technology value. The proposed insight is that a single field calibration and aggregate geometry do not identify configuration-specific pack response. Research and any insight promotion remain separate from implementation acceptance.
