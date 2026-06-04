# Validation Review: Concept 12 — OpenStar Technologies Levitated Dipole

**Concept**: 12-levitated-dipole (OpenStar Technologies — D-T levitated dipole reactor)
**Model under review**: AI-synthesis LCOE analysis (point estimates: baseline $138/MWh, optimistic $68/MWh, conservative $339/MWh)
**Reference / ground truth**: Handwritten `dipole_lcoe.py` bottom-up cost model (LCOE = $110.7/MWh at n=100, 8% discount, 5-yr construction, 85% CF, 1-yr replacement interval); component-level bill of materials from Simpson et al. material masses
**Reviewer**: Mallory Snowden (with Claude assistance)
**Review date**: 2026-05-28

---

## TL;DR

The AI synthesis for OpenStar's levitated dipole produces a baseline LCOE ($138/MWh) within ~25% of the handwritten bottom-up model ($110.7/MWh) and correctly identifies the dominant strategic risks (coil replacement workflow, financing cost, plasma confinement scaling). On those grounds the synthesis is in the right neighborhood. But it gets there by combining a wrong-architecture analog for the dominant capital line (a CFS SPARC tokamak coil at $250M used as the levitated-dipole coil cost), a missing tritium-breeding-ratio physics constraint that the handwritten model identifies as concept-gating, and an unsourced thermal-efficiency assumption — all without a bottom-up bill of materials. The LCOE-near-the-right-answer is partly coincidence: errors in opposite directions cancel.

---

## Human reviewer score for agentic research: **FAIL**

The AI synthesis produces a defensible-looking LCOE through methodology that would not survive a domain-expert audit. The error pattern is the same shape as concepts 7 and 11 — wrong-architecture analogs, missing physics constraints, top-down rather than bottom-up cost composition — even though the magnitude of the final number happens to land closer to reality than in those reviews. A reader of the AI synthesis cannot determine which line items are calibrated, which are placeholder analogs, or which physics constraints were never checked. The handwritten `dipole_lcoe.py` model is the load-bearing analysis for this concept; the AI synthesis is a complementary risk-taxonomy artifact and should not be used as the LCOE-of-record.

---

## What is being reviewed

This concept differs structurally from concepts 7 and 11 in one important way: there is no costingfe-routed `model_setup.py` for concept 12. OpenStar's levitated dipole is one of the 12 bespoke-cost-model concepts in the corpus, and its load-bearing analysis is a hand-written Python file (`dipole_lcoe.py`) that builds an LCOE from a component-level bill of materials (REBCO kA-m, shield, structure, conduit, blanket masses, etc.) sourced from published mass studies.

This review grades the **AI-synthesized LCOE analysis** that runs alongside the handwritten model. In the concept-7/11 reviews, the agentic-pipeline output was the load-bearing artifact and was graded against an external published reference. Here the agentic-pipeline output is *not* load-bearing — it is a parallel analysis — and is being graded against the project's own bottom-up handwritten model as the reference of record.

---

## Glossary (for outside readers)

| Term | What it is |
|---|---|
| **Levitated dipole** | A confinement scheme using a single levitated superconducting magnetic coil (like Jupiter's magnetosphere). OpenStar Technologies is the commercial developer; precedent experiments are LDX (MIT) and the Junior demonstrator. |
| **TBR** | Tritium Breeding Ratio — for a D-T plant, neutrons must breed at least as much tritium in the blanket as the plant consumes (TBR ≥ 1, plus margin). Levitated dipole geometry constrains achievable TBR because the levitated coil shadows part of the blanket. |
| **REBCO** | Rare-Earth Barium Copper Oxide — the high-temperature superconductor used in the coil. Cost-per-kA-m of REBCO tape is a load-bearing parameter. |
| **BOM** | Bill of Materials — itemized list of parts and their masses/quantities, multiplied by per-unit cost to give component capital. |
| **CFS SPARC** | Commonwealth Fusion Systems' compact high-field tokamak demonstrator — a *different* fusion architecture being used as the AI synthesis's analog for coil capital cost. |
| **kA-m** | Kiloamp-meter — the natural unit for REBCO cost ($/kA-m), capturing both current capacity and conductor length. |

---

## Finding 1 — Wrong-architecture analog for the dominant capital line

The AI synthesis anchors its core magnet cost at **$250M** using a CFS SPARC tokamak coil as the reference. This is the single largest assumption in the LCOE calculation by sensitivity.

The two architectures are dissimilar in every dimension that drives coil cost:

| Property | CFS SPARC | OpenStar Levitated Dipole |
|---|---|---|
| Confinement family | Compact tokamak | Single-coil dipole |
| Coil count | 18 toroidal + 6 poloidal | 1 levitated + 1 charging coil |
| Operating field | ~12 T on-axis | Lower central field, gradient-confined |
| Coil topology | Toroidal D-shape | Solenoidal ring, levitated |
| Structural environment | EM forces between TF coils; high inboard stress | Self-supporting ring under gravity + EM hover |
| Replacement workflow | Plant lifetime (no in-service replacement) | Annual or sub-annual (per handwritten model's replacement schedule) |

The handwritten `dipole_lcoe.py` model derives coil cost from first-principles BOM: REBCO kA-m × $100/kA-m (FOAK) + shield + structure + conduit + top magnet fraction, with a 20% REBCO learning rate and a documented amortization treatment. That bottom-up path produces a coil capital that is internally consistent with the dipole geometry. The AI synthesis's $250M SPARC analog is a top-down point estimate from a different architecture, with no scaling to dipole geometry, no shield-stack composition, and no replacement-workflow treatment.

This is the same wrong-architecture-analog failure mode as concept 11 (parameters from a different operating point) and concept 7 (Z-IFE LTD numbers used for Pacific Fusion IMG) — same class, different specifics.

---

## Finding 2 — Concept-gating physics constraint missing (TBR)

The handwritten analysis identifies a binding tritium-breeding-ratio constraint that the AI synthesis does not capture:

> Handwritten finding: TBR ≥ 1.33 is required under reflective tungsten neutrons in the dipole geometry, but the assumed Li2O blanket route yields TBR ≈ 1.1.

If the handwritten analysis is correct, this is concept-gating — the plant cannot close its tritium fuel cycle without either a different blanket chemistry (LiPb, FLiBe), a different neutron multiplier scheme, or an external tritium source. The AI synthesis does not mention TBR at all in its risk taxonomy, treats the Li2O blanket as a settled choice, and proceeds to LCOE without checking whether tritium balance is closed.

The structural problem this exposes is the same one concept 11 had in a different form: the AI synthesis lacks a "physics closure" pass before it begins composing LCOE. For a D-T concept, TBR closure is the closest physical analog of the Q-closure check recommended in concept 11's review. Its absence here lets the synthesis treat fuel cycle as resolved when it isn't.

---

## Finding 3 — Top-down point estimates with no bottom-up audit trail

The AI synthesis is structured as a small set of point estimates with sensitivity factors applied to each:

- Coil capital: $250M (with ±factor sensitivity)
- Annual replacement: $55M/yr (single line, no BOM)
- Thermal efficiency: 38% (no source)
- WACC: variable (sensitivity-modeled)
- Q_sci: variable (sensitivity-modeled)

The handwritten model builds each of these from a component-level bill of materials:

- Coil capital = REBCO kA-m × $/kA-m + shield mass × $/kg + structure mass × $/kg + conduit + top magnet fraction
- Replacement = 20% × core magnet cost + full blanket cost, amortized per replacement interval
- CAPEX composition explicit per category (blanket 24.7%, building 15.9%, turbine 9.2%, shield 8.1%, BoP 6.7%, REBCO 6.6%, ICRH 6.2%)

This is the difference between a *traceable* cost model (every dollar maps to a unit cost × quantity) and a *top-down* one (every dollar is anchored to an analog without per-unit decomposition). A reviewer of the AI synthesis cannot ask "what unit cost is driving the coil capital?" because there is no unit cost — there is a single point estimate inherited from an unrelated machine.

The downstream consequence is that AI-synthesis sensitivity sweeps cannot find what the handwritten model finds: the LCOE is meaningfully sensitive to REBCO learning rate (~$94/MWh swing in the handwritten model's blanket-learning-rate sweep, ~$57/MWh swing on plant power scaling). Neither of these levers is visible in the AI synthesis at all, because neither has a primary parameter exposed.

---

## Finding 4 — Selective omission of replacement and operational lines

The AI synthesis lists annual coil replacement at **$55M/yr** as its highest-sensitivity item — about half the handwritten model's $110.4M/yr total. The shortfall is roughly the *blanket* replacement line ($90.6M/yr in the handwritten model), which the AI synthesis appears to exclude entirely.

A levitated dipole's blanket faces both 14 MeV neutron flux and thermal cycling; assuming the blanket is not in the replacement schedule because the AI synthesis does not name it is a silent omission. The handwritten model treats blanket and core magnet as separately-replaced items, each with its own interval. The AI synthesis treats "replacement" as a single coil-centric line.

Other operational items that the AI synthesis is silent on but the handwritten model exposes:
- Helium ash handling in closed-field topology (no exhaust solution disclosed; concept-gating per handwritten risk notes)
- Cryogenics plant capital and operating cost (no separate line in the AI synthesis)
- Tritium plant capital and operating cost (not separately itemized)
- Remote handling and I&C (potentially $50–200M omission per handwritten risk notes)

The AI synthesis's lower LCOE point estimate is *partly* a consequence of these missing lines, not a more efficient plant. Its higher LCOE comes from a different driver (the wrong-architecture coil capital being applied at a single high analog value) — so the two errors cancel approximately, leaving the synthesis's $138/MWh in the same neighborhood as the handwritten $110.7/MWh by coincidence. The fact that the magnitudes are close does not mean the methodology is sound.

---

## Why the cost framework doesn't catch this (architecture note)

Concept 12 is one of the 12 corpus concepts that bypass costingfe entirely (per the financial-parameter audit you ran earlier — bespoke cost model, 8% interest rate convention, no `forward()` call). The framework-level consistency checks recommended for concepts 7 and 11 (Q closure, geometric closure, recirc validity, source-freshness, cost-basis-year) do not run against this concept regardless of how they are implemented in costingfe, because the framework is not on the calculation path.

This compounds the auditability problem: there is no automated check that any AI-synthesis line item is bottom-up reconcilable with the handwritten model. The only check is human review, which is what this document is.

---

## Recommended corrective actions

### Per-concept fixes (concept 12 specifically)

1. **Demote the AI synthesis from "load-bearing LCOE" to "risk taxonomy and scenario commentary"** in any aggregated score or downstream use. The handwritten `dipole_lcoe.py` is the analysis of record; the AI synthesis is supporting material that frames qualitative risk but does not produce a defensible numerical LCOE.

2. **Rebuild the AI synthesis's coil capital from the handwritten model's BOM**, not from a SPARC analog. If the synthesis is going to publish a coil-capital number, it should reference `dipole_lcoe.py`'s component-level calculation by name and use the same REBCO kA-m × $/kA-m basis, not a top-down analog.

3. **Add a TBR closure check** before publishing any D-T LCOE for the dipole. The handwritten model identifies TBR ≥ 1.33 with the assumed blanket; the AI synthesis should at minimum surface this as a concept-gating risk and refuse to publish an "optimistic" scenario without an acceptable TBR pathway.

4. **Reconcile the replacement schedule to the handwritten BOM.** The $55M/yr point estimate omits blanket replacement at minimum. Either name the items that are *not* being replaced and justify the choice, or restore the full handwritten schedule.

5. **Source the thermal efficiency assumption.** 38% is plausible for a D-T thermal-cycle plant but needs a power-conversion design citation or a documented analog. Currently it appears as an unsourced point estimate.

### Process fixes (framework / pipeline)

6. **Same source-freshness and physics-closure checks** as recommended for concepts 7 and 11, with one bespoke-cost-model-specific addition: when a concept bypasses costingfe, the AI synthesis must reference the bespoke model's bill of materials line-by-line rather than substituting top-down analogs. A consistency check at synthesis time would be: *"does every AI-synthesis line item have a matching handwritten-model line, and are the values within ±25%?"*

7. **TBR closure check for D-T concepts.** Analog of the Q closure check for steady-state concepts and the driver closure check for pulsed concepts: any AI synthesis of a D-T plant must demonstrate that the declared blanket configuration produces TBR ≥ 1.1 (or document why a lower value is acceptable). Missing this check in concept 12 is the specific failure that lets the synthesis claim an LCOE without addressing fuel-cycle closure.

8. **AI-synthesis methodology standard for bespoke-model concepts.** Today's failure mode is that the synthesis substitutes top-down analogs (SPARC coil, single replacement line) when bottom-up data exists in the bespoke model. The standard should be: if a bespoke model exists, the AI synthesis is constrained to *referencing* its line items rather than reinventing them. New analog substitutions are permissible only where the bespoke model is silent.

---

## What this review does not address

- The handwritten `dipole_lcoe.py` model's own weaknesses (heuristic Li2O blanket cost at $100k/t, no separate cryogenics or tritium plant line, no decision-tree risk framing). These are real but distinct from grading the AI synthesis.
- The 8% interest rate convention used by the bespoke model (versus the 7% costingfe default or the project-policy question raised in the corpus-wide financial-parameter audit).
- The broader question of which 12 bespoke-cost-model concepts should be migrated to costingfe and on what timeline.
- The concept-12 confinement-physics validation (Tahi confinement scaling from 26 eV to 10–20 keV) — this is a domain-physics concern that exists independent of which TEA model is graded.

These are real but set aside for this review.

---

## Provenance

- Handwritten cost model: `dipole_lcoe.py` (bottom-up BOM, Simpson et al. material masses, REBCO kA-m basis, 8% discount, 5-yr construction, 85% CF)
- AI synthesis: reviewed via the concept's prior comparison document (the prior version of this file before reformat)
- Domain reference: Simpson et al. mass studies (cited by `dipole_lcoe.py`); LDX and Junior experimental precedents for confinement scaling
- TBR analysis: per the handwritten model's risk notes (TBR ≥ 1.33 required under reflective tungsten neutrons; Li2O route yields ~1.1)

The numerical comparison between the handwritten model and the AI synthesis comes from the prior version of this file (the comparison table preserved verbatim from that source). No new computation was performed for this validation review.
