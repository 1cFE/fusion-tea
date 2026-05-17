# Cross-Concept Score Calibration

You are performing cross-concept calibration of LCOE Downselect Potential scores.
This is Pass 2 of a two-pass scoring system. Pass 1 (per-concept scoring) is
complete. Your job is to enforce consistency across all concepts.

## Verified Scores (from Python extraction)

The following table was extracted and computed by Python. It includes:
- C1, C3, C4, C5, C8: from Claude's per-concept scoring (Pass 1)
- C2, C6: deterministic category-based assignments (Python)
- C7: computed from F1-F7 function means with heritage credit and caps (Python)
- Binary risk count per concept
- Per-concept `heritage_lineage`, `heritage_floor`, and `peer_group` derived from
  architecture (Confinement Family, topology, fuel, etc.) — use these for Q2
  binary-floor protection and Q6 peer comparisons. Do not infer lineage or peer
  group from concept IDs; the IDs have been renumbered and the per-concept
  fields above are authoritative.

**Do NOT re-extract scores from synthesis files.** Use this table as your starting point.

{{verified_scores_table}}

## Concept File Paths

When you need justification detail for a calibration question, read the synthesis
and/or analysis file at the paths below. Read on demand — do not read all files upfront.

{{concept_file_paths}}

## Calibration Questions

Apply Q1-Q7 in order. For each question, state what you checked, what you found,
and what adjustment (if any) you made. Apply all adjustments automatically — do
not ask for confirmation.

### Q1: Driver reality check

For each concept:
- If the concept has a novel monolithic driver that represents >30% of capital cost:
  **cap C1 at 3.0** (a monolithic driver cannot be modularized).
- If the driver is fusion-unique AND not factory-manufacturable:
  **cap C3 sub-factor A (learning rate) at 2.0**, then recompute C3.

### Q2: Binary/degrading classification and C7 floor

(a) **Verify classifications:** Read each concept's C7 risk matrix (in synthesis
Section 8). Ensure every cell has a binary or degrading label. Apply mandatory
binary classifications if missing:
- TBR < 1.0 for any D-T concept: binary
- Tritium extraction failure: binary
- He-3 self-breeding at scale: binary
- He-3 extraction/purification: binary
- External tritium or He-3 purchase is NOT a valid fallback for reclassification

(b) **Verify fallbacks:** For each binary risk, check if a valid fallback exists
that would reclassify it as degrading. Tritium/He-3 breeding and extraction risks
must ALWAYS remain binary — no fallback can reclassify these.

(c) **Binary count floor:** After all reclassifications, if binary risk count >= 5,
the binary count drags C7 down — but **never below the concept's heritage floor**.
A heritage-lineage D-T concept faces the same shared D-T binary risks (TBR,
tritium extraction, Li-6 supply, etc.) as every other D-T concept; the heritage
pathway acknowledges that mitigation paths exist for these shared risks. Crushing
C7 to 1.0 for a thoroughly-enumerated heritage concept punishes thoroughness, not
risk.

**Rule:** if binary risk count >= 5, set
`C7_new = min(C7_current, max(1.0, heritage_floor))`.

In words: drop C7 to the floor (heritage floor for heritage concepts, 1.0 for
non-heritage concepts), but only if doing so lowers C7 — never raise C7 with this
rule.

**Use the `heritage_floor` column in the verified scores table for each concept.**
Do not infer it from the concept ID. The lineage values that can appear are:

| Heritage lineage | Floor |
|-----------------|-------|
| Tokamak | 4.0 |
| Spherical Tokamak | 3.0 |
| Stellarator | 4.0 |
| Laser IFE | 3.5 |
| Mirror | 2.5 |
| FRC | 2.5 |
| Z-pinch | 2.5 |
| magLIF | 3.0 |
| (none) — non-D-T or no recognized lineage | 1.0 |

For non-D-T concepts (p-B11, D-He3, aneutronic, exotic), the heritage_floor is
1.0 — the override fully crushes C7 as before.

**Worked examples** (lineage is shown in the verified scores table for each):
- A D-T stellarator concept with 6 binaries: heritage_floor = 4.0,
  C7_current = 4.0. Override → min(4.0, max(1.0, 4.0)) = 4.0. No change.
- A D-T laser IFE concept with 7 binaries: heritage_floor = 3.5,
  C7_current = 3.5. Override → min(3.5, max(1.0, 3.5)) = 3.5. No change.
- A non-heritage D-T concept (e.g. polywell, muon-catalyzed) with 6 binaries:
  heritage_floor = 1.0, C7_current = 3.0. Override → min(3.0, max(1.0, 1.0))
  = 1.0. Full crush as before.

### Q3: Site-specific C5 check

For each concept, check if C5 includes site-specific adjustments (named sites,
brownfield advantages, proximity to water sources). If found, strip the adjustment
and recompute C5 from the rubric sub-factors only (thermal rejection + fuel safety).

### Q4: Sub-factor arithmetic check (MANDATORY for EVERY concept)

For **every** concept (no spot-checking — do all 35), open the synthesis and
recompute each criterion from its enumerated sub-factors. Apply corrections
**by adjusting the score in the calibrated table**, not just by flagging.

Specific checks that must be performed on every concept:

1. **C3 Sub-factor B**: Find the synthesis's bottleneck enumeration. Verify:
   - He-3 dependency uses **-1.5** (not -1.0 hard constraint)
   - Each hard constraint correctly applies -1.0
   - Each scaling constraint correctly applies -0.5
   - Each sole-source dependency correctly applies -0.25
   - Sum: `B_new = 5.0 - sum(corrected penalties)`, clamped to [1, 5]
   - Recompute `C3 = (A + B_new + C) / 3`

2. **C5 site-specific stripping**: per Q3.

3. **Sub-factor denominator sanity**: if sub-factor weights (capital shares,
   etc.) don't sum to ~100%, recompute on a normalized basis.

4. **Internal contradictions**: if the synthesis text states one C3/C4/C5 value
   in prose but the YAML reports a different value, use the YAML and flag the
   inconsistency. If both prose and YAML disagree with the sub-factor
   arithmetic, use the arithmetic.

5. **Single-concept ad-hoc adjustments**: remove any bonuses or penalties not
   in the framework.

For each correction, record an entry in the adjustments report with original
score, adjusted score, and the explicit arithmetic chain.

### Q5: C7 verification and correction

For each concept, verify the Python-computed C7. **Override C7 in the
calibrated table** (not just flag) if:

- **Evidence Tier mis-assignment**: Any cell in the C7 risk matrix has Tier
  ≥ 3 when the synthesis's own evidence summary indicates Tier 1-2 per the
  anti-leniency, time-stuck, or operating-hardware rules in
  `scoring_framework.md`. Recompute the affected F as the mean of corrected
  cell tiers, then C7 = mean(F1..F7) with heritage floor and function-level
  cap re-applied.

- **Binary mis-classification**: Any "Degrading" cell whose synthesis text
  describes a Q < 1 failure mode (i.e., zero net electricity outcome). Recount
  binaries with corrections; if count crosses ≥ 5, apply the Q2 floor crush:
  `C7_new = min(C7_recomputed, max(1.0, heritage_floor))`.

- **Function-level cap missed**: if any function score F_n ≤ 1.5 after
  corrections, C7 must equal min(mean_C7, min F).

Document each C7 override in the adjustments report with the cell-level
corrections that drove it.

Heritage credit and mean computation: if these were applied incorrectly by
Python, flag (do not override — Python owns the heritage and mean math).

### Q6: Peer consistency check

Group concepts by the `peer_group` column in the verified scores table. The
groups assigned by the extractor are:

| Peer Group | Description |
|-----------|-------------|
| D-T Tokamaks | D-T fuel + Tokamak or Spherical Tokamak lineage |
| D-T Stellarators | D-T fuel + Stellarator lineage |
| D-T Mirrors | D-T fuel + Mirror lineage |
| D-T Laser IFE | D-T fuel + Laser IFE lineage |
| D-T Pulsed (MIF/Z-pinch) | D-T fuel + Z-pinch or magLIF lineage |
| Aneutronic FRC | D-He3 or p-B11 fuel + Compact Toroid (FRC) topology |
| p-B11 | p-B11 fuel, non-FRC |
| Aneutronic | D-He3 fuel, non-FRC |
| Exotic | D-T concepts with no recognized heritage lineage, D-D concepts, and exotic/non-power |

For each peer group (except Exotic and any singleton group, which are exempt
from Q6 adjustments):
- Compute the peer median for each criterion
- Identify outliers: concepts with any criterion >= 1.0 away from the peer median
- For each outlier, read the synthesis justification
- If the gap is unjustified: adjust the score up to 1.0 toward the peer median
- If the gap reflects a genuine architectural differentiator: keep the score

### Q7: Review Q6 adjustments

Re-examine each Q6 adjustment from the previous step:
- **Revert** if the adjustment eliminates a genuine architectural differentiator
  (e.g., a concept genuinely has better modularization than its peers)
- **Keep** if the gap was truly unjustified (same architecture, similar design,
  no reason for the score difference)

Document each revert/keep decision with reasoning.

## Output Format

### Calibrated Score Table

Output the calibrated scores in this exact format (plain numbers only, no annotations):

```
| concept_id | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 |
|------------|----|----|----|----|----|----|----|----|
| 01-hts-compact-tokamak | X.X | X.X | X.X | X.X | X.X | X.X | X.X | X.X |
...
```

### Adjustments Report

After the score table, report ALL adjustments made during calibration in this format:

| Concept | Question | Criterion | Original | Adjusted | Justification |
|---------|----------|-----------|----------|----------|---------------|
| ... | Q1/Q2/Q3/Q4/Q6 | C1/C3/... | X.X | X.X | ... |

Include Q7 revert/keep decisions as separate rows.

Write the calibrated score table and adjustments report to: `{{output_path}}`
