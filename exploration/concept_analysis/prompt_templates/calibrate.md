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

Heritage floors (lookup by concept ID prefix; D-T fuel only):

| Heritage lineage | Floor | Concept ID prefixes |
|-----------------|-------|---------------------|
| Tokamak | 4.0 | 01, 21, 28, 29, 33, 34 |
| Stellarator | 4.0 | 05, 09, 10, 20a, 20b, 36 |
| Spherical Tokamak | 3.0 | (assign if applicable) |
| Laser IFE | 3.5 | 03, 04, 17a, 17b, 26, 30, 31, 32 |
| Mirror | 2.5 | 06, 11 |
| FRC | 2.5 | 08, 18 |
| Z-pinch | 2.5 | 15 |
| magLIF | 3.0 | 07 |
| Non-heritage / alternate fuel | 1.0 | all others |

For non-D-T concepts (p-B11, D-He3, aneutronic, exotic), the floor is 1.0 — the
override fully crushes C7 as before.

**Worked examples:**
- 09-Proxima (Stellarator, 6 binaries): heritage floor = 4.0. C7_current = 4.0
  (after F-level heritage). Override → min(4.0, max(1.0, 4.0)) = 4.0. No change.
- 17a-Xcimer (Laser IFE, 7 binaries): heritage floor = 3.5. C7_current = 3.5.
  Override → min(3.5, max(1.0, 3.5)) = 3.5. No change.
- 27-Polywell (no heritage, 6 binaries hypothetical): floor = 1.0. C7_current = 3.0.
  Override → min(3.0, max(1.0, 1.0)) = 1.0. Full crush as before.

### Q3: Site-specific C5 check

For each concept, check if C5 includes site-specific adjustments (named sites,
brownfield advantages, proximity to water sources). If found, strip the adjustment
and recompute C5 from the rubric sub-factors only (thermal rejection + fuel safety).

### Q4: Sub-factor arithmetic check

For each concept:
- Recompute each criterion from its sub-factors using the framework formulas
- Flag any criterion where the reported score deviates >0.3 from the computed
  sub-factor average
- Check for double-counting between sub-factors within a criterion
- Remove any single-concept ad-hoc adjustments (bonuses or penalties not in the framework)
- Correct scores to match sub-factor arithmetic

### Q5: C7 verification

Verify that the Python-computed C7 correctly applied:
- Heritage credit floors on **F1-F7** (D-T concepts only) — the heritage floor is
  applied to every function score, not just F1-F3
- Function-level cap (any function mean <= 1.5 after heritage -> C7 capped at that value)
- Mean computation (mean of F1-F7, rounded to nearest 0.5)

If any computation appears incorrect, flag it as an informational output with the
expected value. Do NOT override Python's C7 — flag only.

### Q6: Peer consistency check

Compare C1-C8 scores within each peer group:

| Peer Group | Concepts |
|-----------|----------|
| D-T Tokamaks | 01-CFS, 21-TE, 28-ES, 29-Firefly, 33-BEST, 34-India |
| D-T Stellarators | 05-Thea, 09-Proxima, 10-Gauss, 20a-Type One, 20b-Renaissance, 36-Helical |
| D-T Mirrors | 11-Realta |
| D-T Laser IFE | 17a-Xcimer, 17b-Focused, 26-Indirect, 30-NIF, 31-Blue Laser, 32-French |
| D-T Pulsed (MIF/Z-pinch) | 07-MagLIF, 14-GF, 15-Zap |
| D-T Other | 22-FLF, 25-HIF, 12-OpenStar |
| D-He3/aneutronic FRC | 08-Helion, 18-TAE |
| p-B11 | 04-HB11, 06-CHARM, 24-DPF |
| Exotic | 02-Sonofusion, 03-Cortex, 13-Orbitron, 16-Acceleron, 19-Zephyr, 27-Polywell, 35-Polomac |

For each peer group (except Exotic, which is exempt from Q6 adjustments):
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
