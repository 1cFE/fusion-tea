# Review: Sheared-Flow Stabilized Z-Pinch

**Iteration:** 3
**Date:** 2026-04-05
**Files reviewed:** analysis.md, model_setup.py, model_output.txt
**Source documents:** 9 files

---

## Strategic Assessment

### 1. Modeling Approach

The CAS-structured model is well-conceived and the overrides are all defensible. The three
principal substitutions — zeroing C220103 (no magnets), zeroing C220104 (no auxiliary heating),
and routing pulsed power capital into C220107 — correctly reflect the Z-pinch's structural
departure from the tokamak reference architecture. Mapping the electrode system to C220108
(replacing a target factory) is a reasonable analogue choice given the electrode's dual role as
plasma-facing component and current conductor; $15M/module is consistent with the industrial
arc-furnace analogy cited in the Engineering Paradigms paper.

The power balance arithmetic is correct and internally consistent. Cross-checks pass: gross
electric = 224.2 MWt × 0.33 = 74.0 MWe ✓; driver wall-plug = 19 MJ/s (190 MWt / Q=10) ÷
0.70 = 27.1 MW ✓; net = 74.0 − 35.1 = 38.9 ≈ 38.8 MWe ✓. The discrepancy between the
model's 38.8 MWe/module and Zap's stated "50 MWe/module" is honestly handled — the analysis
notes this is recoverable at η_th = 37% rather than the conservative 33% baseline.

One structural modeling choice deserves scrutiny: the driver cost sensitivity sweep spans 20×
in $/MJ but LCOE moves only from 22.25 to 23.74 ¢/kWh. This is arithmetically correct —
driver capital is only ~$8M/module in the baseline, a small fraction of the $737M CAS22 total.
But the model output in isolation could mislead a reader into treating pulsed power cost as a
second-order concern. The analysis text (§S4) correctly explains why this framing is wrong:
the risk is not $/MJ but component viability. The 4–6 order-of-magnitude capacitor lifetime gap
(10⁴–10⁵ shots demonstrated vs. 10⁸–10⁹ required) and the switch technology class mismatch
(6.5–15 kV commercial SiC vs. 50–200 kV Z-pinch requirement) are existential constraints that
no $/MJ sensitivity sweep can represent. This disconnect between what the model can show and
what the analysis correctly argues is real — and the analysis handles it honestly — but the
model output section lacks an inline annotation flagging the limitation.

The 4-module, NOAK baseline is a reasonable reference scenario. The conservative scenario
(Q=5, 5 Hz, costly driver → net MWe: 5, LCOE: 824 ¢/kWh) and optimistic scenario (Q=15,
cheap driver, long life → 436 MWe, 9.80 ¢/kWh) bracket the uncertainty space appropriately.

### 2. Strategic Positioning

The analysis correctly identifies the SFS Z-pinch as occupying a unique structural niche:
the only MFE concept in the portfolio with no superconducting magnets, no cryogenic plant,
and no auxiliary heating, where the dominant capital cost driver is a pulsed power system
rather than an HTS magnet system. This is not merely a design variant — it is a different
cost architecture, and the analysis frames it as such.

The cross-concept comparison with the ST-HTS (Section 7) is specific and well-calibrated.
The listed divergences (no HTS tape, no cryogenic plant, LiPb as first-wall vs. separate
blanket, 200 µs pulsed vs. 15-min inductive, multi-module vs. single-unit, rep-rate thermal
storage challenge) are all real and analytically significant. The note that eliminating HTS
magnets is "a genuine structural advantage" worth $500M–$1B in capital cost is correctly
qualified by the pulsed power supply chain substitution.

The regulatory pathway risk in Section 7 is noted but relatively briefly. The SFS Z-pinch's
deviation from the ITER reference pathway is the largest of any MFE concept in the portfolio
— no licensed analogues for a gravity-cascade LiPb first wall, pulsed 1 MA Z-pinch, or
absence of external magnetic containment. This is primarily a schedule risk (novel licensing
framework development) rather than an existential constraint, but it compounds the other
program-level risks.

The "no independent TCA exists" observation in Section 1 is important framing. This concept
has no ARIES-class study to anchor the economic projections. The analysis does not overstate
what can be derived from the available sources.

### 3. Risk and Uncertainty Framing

The risk characterization is the strongest element of this analysis. The six challenges in
Section 2 are ranked correctly by LCOE impact. The distinction between the Q gap (physics
extrapolation: 5–10× pinch lifetime from FuZE to commercial) and the rep-rate gap (engineering
extrapolation: 50× from 0.2 Hz to 10 Hz) as separately "Critical" is appropriate — these are
independent scaling challenges that must both be solved.

The supply chain section (§S4) is the single most analytically valuable contribution. Framing
the pulsed power supply chain as a "program-level constraint" comparable in schedule severity
to Q demonstration — rather than a cost-curve problem — is the correct characterization and
is well-supported by the OSTI 2025 report. The specific quantitative anchors (10,000–216,000
capacitors/plant at 4–6 year lead times; 125–250 years to build a 150-plant fleet at current
Western capacity) are sourced from an authoritative multi-institutional LLNL study, not
vendor claims. This elevates the analysis above the "assume pulsed power will scale with
capital investment" framing common in concept analyses at this stage.

TRL ratings are defensible:
- Physics basis (Q > 10 at 200 µs): TRL 2 — correct. Thermonuclear neutrons demonstrated,
  but commercial-regime physics is a multi-parameter extrapolation.
- LiPb first wall: TRL 2–3 — correct. Century has demonstrated liquid metal (bismuth) at
  0.2 Hz, but LiPb compatibility, 10 Hz dynamics, and EM coupling under Z-pinch pulses are
  all untested.
- Pulsed power driver: TRL 3 — defensible, with the important clarification that 10 Hz
  thyristor modulators are demonstrated at lab scale but the full commercial driver (capability
  gap + lifetime gap) requires new technology classes.
- Tritium breeding and extraction: TRL 2 — correct. TBR is a Monte Carlo calculation on
  the engineering design; no Z-pinch-specific breeding experiment exists.

The analysis acknowledges FuZE-3's gigapascal pressure result (November 2025) without
inflating its significance — correctly noting it advances the physics case but still leaves
the 200 µs lifetime and 1.35 MA current targets as demonstrated. This is appropriate.

Economic risks beyond technical risks are present: supply chain (pulsed power), regulatory
novelty, and D-T tritium startup inventory. The capacity factor assumption (75%) is
appropriately lower than mature nuclear (90%) and explicitly flagged as an assumption with
high uncertainty.

### 4. Data Sufficiency

The source base is the best available for this concept class. The Engineering Paradigms paper
(Thompson et al., FST 2023) is genuinely unusual for a private fusion venture — it provides
plasma parameters, blanket design rationale, driver efficiency breakdown, and Q projections in
a peer-reviewed format. Most private fusion companies at comparable TRL publish far less.
The OSTI 2025 pulsed power challenges report is a high-quality, multi-institutional source for
the supply chain constraints.

The 15 data gaps in Section 6 are correctly prioritized. The "blocking" designations are
conservative and defensible:
- Q > 10 never demonstrated: blocking ✓
- 200 µs pinch lifetime not demonstrated: blocking ✓ (same root cause as Q, but listed
  separately because the lifetime must be demonstrated before Q can even be measured)
- Capital cost entirely absent: blocking ✓ (no public estimate at any level of detail)
- Capacity factor and maintenance intervals: blocking ✓
- Rep rate 50× gap: blocking ✓
- Capacitor lifetime gap (4–6 OOM) and switch capability gap: blocking ✓

The analysis is honest about what inference chains are required (e.g., the recirculating
power fraction derivation from Q, driver efficiency, and thermal efficiency) and flags each
with uncertainty levels (LOW/MODERATE/HIGH UNCERTAINTY comments in model_setup.py).

No additional source acquisition appears necessary before proceeding to Stage 2 analysis.
The concept is at TRL 2–3 and the main data gaps are genuinely unknown (not sourced but
missing): until FuZE-A or Century demonstrates Q ≥ 1 and rep rates above 1 Hz, no public
document will close those gaps regardless of research depth.

### 5. Cross-Concept Consistency

The reuse of the tritium supply chain analysis from the ST-HTS analysis is appropriate —
both are D-T concepts targeting marginal TBR just above 1.0, and the external tritium
constraints (CANDU production, startup inventory per GWe) apply identically. The steam
Rankine baseline and the recirculating power framework are also correctly identified as shared
assumptions.

The divergences are specific and structurally significant rather than superficial. The thermal
storage observation — "100 ms between pulses rather than minutes" — correctly captures why
10 Hz pulsed operation creates fundamentally different grid integration challenges than
inductive tokamak pulses. This hasn't been explored in quantitative depth, but it's the
right observation to flag for Stage 2.

No approved prior analyses exist against which to validate shared cost constants, so
cross-concept consistency can only be checked against the ST-HTS analysis on the same branch.
Within that comparison, the analysis is consistent.

---

## Verdict

VERDICT: PROCEED

This analysis is strategically sound. The concept is correctly positioned, the risks are
honestly framed, the sources are used with appropriate skepticism, and the pulsed power supply
chain finding — sourced from the OSTI 2025 multi-institutional study — elevates this above a
standard TRL-3 "too early to know" writeup by establishing the structural nature of the
constraint. The model is internally consistent and the CAS overrides are defensible. Minor
annotation gaps in the model output and a source attribution edge case are the only issues,
neither of which affects the analytical conclusions.

---

## Minor Fixes (PROCEED only)

### PA-1: STALE marker on model_setup.py is ambiguous
- **Category:** inconsistency
- **Severity:** minor
- **Location:** `model_setup.py` line 1
- **Finding:** The file opens with `# STALE: analysis-updated-iter-3`. As written this reads
  as "this file is outdated as of iter-3." However, model_output.txt is consistent with the
  parameters in model_setup.py (driver stored energy 2.7 MJ, Q=10, 4 modules, NOAK, etc. all
  match). If the comment is a pipeline tracking tag meaning "last updated at iter-3," it should
  be clarified. If the file IS outdated relative to some iter-3 revision, the discrepancy with
  model_output.txt needs investigation.
- **Proposed Fix:** Replace the ambiguous comment with either `# Last updated: iter-3` (if
  it's a provenance tag) or investigate and reconcile if a genuine code/output mismatch exists.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-2: Driver cost sensitivity sweep needs inline clarification in model output
- **Category:** improvement
- **Severity:** minor
- **Location:** `model_output.txt` — "Driver cost [M$/MJ stored]" sensitivity block
- **Finding:** The sweep shows LCOE varies only 22.25 → 23.74 ¢/kWh across a 20× range in
  $/MJ. This is arithmetically correct (driver capital is ~$8M/module vs. $737M total CAS22),
  but a reader reviewing only the model output could incorrectly conclude pulsed power cost
  is a second-order concern. The analysis text (§S2, §S4) correctly explains the real risk is
  component viability (capacitor lifetime 4–6 OOM short; switch capability gap), not $/MJ. The
  model output section lacks a note connecting to this.
- **Proposed Fix:** Add a brief NOTE below the driver cost sensitivity block in model_output.txt
  (or model_setup.py output logic), e.g.: "NOTE: Low LCOE sensitivity to driver $/MJ does NOT
  indicate low pulsed power risk. The binding constraint is component viability (capacitor
  lifetime 4–6 OOM gap; switch capability class mismatch) — a program-level constraint
  independent of $/MJ cost. See analysis.md §S4."
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-3: Section 8 source attribution implies ST-HTS analysis is formally approved
- **Category:** inconsistency
- **Severity:** minor
- **Location:** `analysis.md` §Section 8, source #8; also §Section 7 cross-concept notes
- **Finding:** Source #8 is described as "D1+ Analysis: Spherical Tokamak - HTS (prior
  approved analysis)." As of this review, no analyses have been through formal strategic review,
  so "approved" overstates the ST-HTS analysis's status. The cross-concept comparison in
  Section 7 is still valid — the ST-HTS analysis was written and consulted — but the "approved"
  label creates a false equivalence with a future formal approval gate.
- **Proposed Fix:** Change "prior approved analysis" to "parallel concept analysis (same
  pipeline)" in the Section 8 source entry, and soften the Section 7 in-text citation from
  "[21-spherical-tokamak-hts analysis, §Section 4]" to "[parallel ST-HTS analysis, §Section 4
  — not yet formally reviewed]" or simply remove the approval qualifier.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_
