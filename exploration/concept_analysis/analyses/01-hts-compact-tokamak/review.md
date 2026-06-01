# Review: HTS Compact Tokamak (Commonwealth Fusion / ARC)

**Iteration:** 1
**Date:** 2026-05-31
**Files reviewed:** analysis.md, model_setup.py
**Source documents:** 14 files

---

## Strategic Assessment

### 1. Design-Point Coherence

Clean and consistent end to end. The frontmatter selection (ARC 2015 "Conservative
Pilot" phase, paper-concept, `P_native = 233`, grounding high) is reproduced
verbatim in the top-of-body Design Point block, carried unedited into Section 5
("at its native scale of 233 MWe net"), and into `model_setup.py`
(`P_native = 233.0`, commented "copied from the analysis Design Point block").
Section 5 describes exactly *one* named plant. The 233 MWe / Qe = 3.5 / 1100 K /
~46% Brayton figures are confirmed in the primary source (arc-reactor-specifications.md
§2), and the analysis is unusually disciplined about the design-point-vs-program
hazard: it explicitly quarantines the current commercial 400 MWe Virginia ARC as a
*separate* future design point (Section 2, Challenge 2; Data Gap #1) rather than
letting program-era numbers leak into the parameters.

The one place coherence is imperfect is the interaction between `P_native = 233`
and the thermal efficiency. 233 MWe is *defined* by the 46%-efficiency
conservative-Pilot point; the FNSF/demonstrated-material point at ~40% yields 190
MWe. The model holds net electric at 233 MWe but leaves `eta_th` at the ~40%
library default (the right call under the "aspirational efficiency is not grounds
to override" contract, and the analysis reasons this out well in the
`model_setup.py` header). The residual is that the native run describes a hybrid —
233 MWe net *at* 40% — that matches neither published phase, and mildly oversizes
the thermal plant. The effect is genuinely small (the η_th sweep shows only
199.0 → 194.6 $/MWh across 40–50%, ~2%) and is disclosed via that sweep, so this
is a clarity nit, not a coherence failure. Physics-characteristic overrides are
otherwise correctly withheld: neither `eta_th` nor `eta_de` is overridden, and the
spec contains no library-default re-passing.

### 2. Override Discipline

This is the strongest dimension of the analysis, and it is exemplary. All entries
are six-field, use canonical account codes (`C220103`, `C220101`, `CAS27`,
`C220108` — all present in the library CAS22 detail; no invented `CAS22.1.3`-style
codes; the "22.1.3" string in Section 1 is correctly attributed to the pyFECONS
*source's* numbering, not used as an override account). Provenance is `derived`
for all four with the honest justification that quantity and unit price are
published-direct but the CPI escalation makes the delivered figure derived; the
CPI factor (1.33) and the arithmetic are shown in every rationale. The Section 5b
YAML and the `model_setup.py` `overrides` list carry identical accounts, values
(as expressions, e.g. `5200.0 * 1.33`), enabled flags, and provenance.

I verified every figure against Table 10–11 of the source:

- **C220103** ($5,200M): magnet/structure subtotal upper bound $5.1–5.2B; the
  $4.6B/4,350t SS316LN cage, $380M copper winding, and $100–210M REBCO tape are
  all in the table. The central thesis — that the library's conductor-length
  pricing undercounts the ARC magnet ~7–10× because it misses the structural-steel
  cage — is borne out by the model itself (native library C220103 = 989 vs override
  6,916 per module).
- **C220101** ($108.1M): first wall $4.03M + Be multiplier $4.1M + Inconel blanket
  tank $100M. Correct.
- **CAS27** ($147.5M): 958t FLiBe × $154/kg. Correct.
- **C220108** ($17.5M): the deferred-divertor placeholder. Correct.

The disabled C220108 entry is a model of override discipline: enabling it would
*lower* the account below the library default ($23.3M vs $56.3M) on the basis of an
explicitly incomplete placeholder for an undesigned subsystem, in the
non-conservative direction, while the narrative rates ARC's divertor difficulty as
"between ITER and reactor designs." Keeping it as a documented-but-disabled
candidate and routing it to Data Gap #2 as an *upward* sensitivity is exactly
right. Equally careful: the walkthrough notes correctly diagnose the $183M
inner-VV-wall figure as an OCR artifact (the $92M VV subtotal only closes with the
corrected ~$17.6M) and fold C220106 into the library default to avoid
double-counting against C220101. Enabled count (3) sits inside the stated High
archetype-fit band (0–4), and there is no un-evidenced re-passing of defaults.

### 3. Family-Delta vs Fixed Comparables

Specific, correct, and honest about confidence. Section 7 walks all four *fixed*
comparables by name with named subsystems and signed cost directions, not generic
novelty claims. The 21-spherical-tokamak-hts contrast (the only comparable with an
approved analysis) is the deepest and is accurate against that synthesis: ARC's
A=3.0 / B0=9.2 T / 23 T-peak high-field path carries a magnet-cost penalty vs
ST-E1's A=2.3 / 5.25 T path; FLiBe-immersion vs outboard liquid-Li is correctly
characterized as cost-neutral-but-risk-divergent (ARC trades beryllium + 90% Li-6
supply burden for breeding-geometry robustness); and ARC's quasi-steady operation
is correctly credited against ST-E1's pulsed thermal-storage requirement. The
28/29/33 deltas are appropriately flagged as inferred/low-confidence given the
absence of approved source data, rather than overclaimed. The closing
"reconciling compactness with high $/kWe" paragraph is a genuine strength: it
pre-empts the obvious misreading by explaining that the compactness win is a
per-unit-*fusion*-power advantage versus the low-field path that does not survive
translation to $/kWe once the structural cage and low engineering gain are costed.

### 4. Two-Knob Projection & Model Integrity

`model_setup.py` uses the four-step helper form correctly: module-level `spec`,
`P_native`, `model`, `overrides`, then
`result, result_1gw = run_native_and_1gw(...)` with no inline two-knob `forward()`
and no `# DEFAULT:` re-passes. (The one `model.forward()` call is the η_th
sensitivity sweep, a legitimate distinct purpose, not a re-implementation of the
two-knob path.) The figures transcribe faithfully: native 199.0 $/MWh /
16,092 $/kW and the 1 GWe projection 543.7 $/MWh / 51,884 $/kW match the analysis
Section 7 prose.

The projection LCOE (~544 $/MWh, ~$52/W) is extreme but *correct and coherent*
given the inputs: it is driven by the well-grounded $6.9B-per-module magnet
override compounded by stacking ~4.29 × 233 MWe modules to reach 1 GWe with no
cross-unit economy of scale. The analysis owns this explicitly rather than
treating it as a discrepancy, which is the right posture. One contract-level
subtlety worth a reader's attention (not a defect of this analysis): by design the
native reference excludes the overrides, so the native 199 $/MWh is the *bare
library* number and the headline magnet override only enters at the 1 GWe knob.
Section 7 quotes the two side by side; a half-sentence noting that native is the
un-overridden reference would prevent a reader from misreading 199 as ARC's
override-corrected native cost.

### 5. Risk, Uncertainty & Data Sufficiency

Thorough and honest. Section 2 ranks challenges by LCOE impact and correctly
identifies the structure-dominated magnet account as the critical modeling hazard.
Section 3 gives defensible per-subsystem TRL ranges (FLiBe blanket TRL 2–3,
tritium cycle 3–4, divertor 4–6 and undesigned, REBCO magnets 5–7) that are
neither inflated nor dismissive. The 11-item Data Gap inventory is appropriately
typed (proprietary / derivable / truly-unknown) and the critical gaps —
commercial-ARC parameters, divertor design, η_th materials contingency, O&M,
replacement cadence, thermal storage — are surfaced with concrete source
recommendations rather than buried. Availability is correctly flagged as the
highest-elasticity lever (the native sensitivity confirms −0.92), and the analysis
sensibly argues for modeling maintenance as scheduled FO&M per Schwartz et al.
rather than a flat de-rate. Nothing here rises to a research-blocking gap; the data
sufficiency ("Rich") rating is justified by the unusually complete 2015 cost table.

---

## Verdict

VERDICT: PROCEED

This analysis is strategically sound. Design-point coherence is clean and the
program-vs-design-point hazard is well quarantined; override discipline is
exemplary, with every enabled figure verified against the source cost table and a
textbook disabled-candidate treatment of the divertor; the family-delta is
specific, signed, and honest about confidence; the two-knob model uses the helper
correctly and the high projection LCOE is a reasoned consequence of a well-grounded
override rather than an error; and the risk/data-sufficiency treatment is thorough
and self-aware. The only items are minor clarity improvements that do not warrant a
stage1 re-run.

---

## Minor Fixes (PROCEED only)

### PA-1: Note the η_th / P_native consistency wrinkle in the native run
- **Category:** improvement
- **Severity:** minor
- **Location:** analysis.md §5 (η_th row / note) and model_setup.py header
- **Finding:** `P_native = 233` MWe is the conservative-Pilot output *at* ~46%
  efficiency, but the native model run holds 233 MWe net while using the ~40%
  library default for `eta_th` (the FNSF point is actually 190 MWe / 40%). The
  native reference therefore describes a 233 MWe / 40% hybrid that matches neither
  published phase and mildly oversizes the thermal plant. The choice to not
  override aspirational efficiency is correct and the LCOE impact is ~2% (per the
  existing sweep), but the residual mismatch is currently implicit.
- **Proposed Fix:** Add one sentence (Section 5 note or `model_setup.py` header)
  stating that net electric is held at the 233 MWe conservative-Pilot value while
  `eta_th` stays at the demonstrated-material library default, so the native
  thermal sizing is mildly conservative, with the η_th sweep bounding the effect.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-2: Clarify that native LCOE excludes the overrides
- **Category:** improvement
- **Severity:** minor
- **Location:** analysis.md §7 (reconciliation paragraph)
- **Finding:** By the two-knob contract the native reference (199 $/MWh,
  16,092 $/kW) is the bare library number; the central C220103 magnet override only
  enters the 1 GWe projection. Quoting the native and projection figures side by
  side risks a reader interpreting 199 as ARC's override-corrected native cost.
- **Proposed Fix:** Add a half-sentence noting that the native figure is the
  un-overridden library reference and that the structure-dominated magnet override
  is reflected only in the 1 GWe projection.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_
