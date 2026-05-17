---
date: 2026-05-17
researcher: Claude
topic: "Affected concepts under blanket-energy-multiplication (mn) policy"
tags: [policy, mn, blanket, iteration-backlog]
status: partially-applied
---

# Affected concepts under the `mn` policy

Policy: see `exploration/concept_analysis/prompt_templates/config/scoring_framework.md` §"Blanket energy multiplication".

- **Canonical for D-T**: `mn = 1.1` (costingfe framework default; generic Li-bearing blanket without dedicated neutron multiplier)
- **Justified deviation**: named blanket technology with a published multiplication factor *or* a physics-coupling argument. Author-judged midpoints of a stated range are **not** sufficient.

## D-T concepts with non-canonical `mn`

| Concept | Current `mn` | Action | Source quality |
|---|---|---|---|
| 09-qi-stellarator-hts | 1.20 | **DEVIATION marked** | Tier A — WCLL PbLi; `stellaris-design-details.md` Table 3, back-derived 3300/2700 ≈ 1.22 |
| 20a-type-one-stellarator | 1.15 | **needs Tier-A cite or revert** | Tier B — "HCPB+Be, 1.10–1.20 range" named-but-uncited |
| 20b-renaissance-stellarator | 1.07 | **DEVIATION marked** | Tier A — JNM 599 (2024) 155239 |
| 29-negative-triangularity-tokamak | 1.11 | **DEVIATION marked** | Tier A — `manta-reference-design.md` §5.1, FLiBe TBR=1.15 |
| 31-laser-icf-oec-architecture | 1.00 | **DEVIATION marked** | Tier A — physics coupling: Li boost already in η_th* = 0.44 |

The other 14 D-T framework concepts use the canonical `mn = 1.1`. Non-D-T concepts (D-D, D-³He, p-¹¹B) are out of scope for this pass — no canonical defined.

## Applied changes (2026-05-17)

1. Created `lib/canonical_params.py` and moved `canonical_eta_th`, `canonical_availability` out of `lib/scoring.py` (those weren't scoring concerns). Added `canonical_mn(fuel)`.
2. Added `# DEVIATION:` markers to the 4 Tier-A cases above. No values changed → no LCOE rerun needed.
3. Wrote per-concept feedback file for `20a` at `.project/research/feedback_mn/20a-type-one-stellarator.md`.
4. Added `scripts/standardize_mn.py` (mirror of the eta_th / availability scripts). Audit confirms only `20a` remains flagged.

## Applied changes (2026-05-17, continued)

5. **`20a` reverted to canonical `mn = 1.10`** (route b). Applied via `standardize_mn.py --apply`. Inline comment + docstring + `MN` constant block updated. `model_setup.py` re-run; new `model_output.txt` regenerated (LCOE 312.5 $/MWh at 350 MWe, was nominally higher under mn=1.15).

## Open follow-up

- **`20a` prose refresh**: `analysis.md` (especially the `800 × 1.15 = 920 MW` derivation around §2.1) and `synthesis.md` (lines 46, 228, 247) still cite the old `M_b=1.15`. Feedback file at `.project/research/feedback_mn/20a-type-one-stellarator.md` is the iteration-loop input. Run the analyze/synthesize stages for 20a to refresh.
- **Audit hygiene**: the regex check is for the literal token `DEVIATION:` (with colon). Use that exact form in code comments.
