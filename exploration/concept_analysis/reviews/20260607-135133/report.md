# Portfolio audit — cross-concept report

**Run:** 20260607-135133
**Cohort (3):** 01-hts-compact-tokamak (MFE/tokamak), 07-maglif (MIF/maglif), 21-spherical-tokamak-hts (MFE/spherical-tokamak)
**Status:** COMPLETE

All three import cleanly and none are marked stale, so all three were fully
auditable. Fresh probe numbers matched the digest within ~2%.

## Headline numbers (1 GWe LCOE, $/MWh)

| Concept | Family | 1GW LCOE | Overnight $/kW | CAS22 (1GW) | Overrides |
|---|---|---|---|---|---|
| 07-maglif | MIF | **102.9** | 8,242 | 3,961 | none enabled (1 disabled) |
| 01-hts-compact-tokamak | MFE | 158.9 (probe 155.2) | 13,794 | 8,035 | 1 (C220103, derived, $1030M) |
| 21-spherical-tokamak-hts | MFE | 168.4 | 12,917 | 7,618 | none |

## The bottom line

**The portfolio does not fully hang together, and the reason is the same in both
problem concepts: the reactor-plant cost — the account that dominates every
concept's LCOE — is not anchored to a real, source-traced dollar value in any of
the three.** Two of the three have a confirmed problem; the third is clean but
also runs entirely on library defaults.

At first glance the numbers look healthy. The two MFE tokamaks sit close together
(155–159 and 168, about 6% apart) and MagLIF lands sensibly below them. But that
surface coherence is misleading:

- **The tokamak cluster is partly manufactured.** 01 only lands next to its
  tokamak neighbor (21) because its biggest cost — the magnets — is pinned about
  five times *below* the very source it cites. If 01 used its cited source value,
  its 1 GWe LCOE would be about **507/MWh**, more than three times the reported
  155 and far above 21's 168. So the apparent family coherence hides the problem
  rather than confirming health. → `concepts/01-hts-compact-tokamak.md`

- **The cross-family ordering is backwards and propped up by optimism.** MagLIF —
  the least-mature approach here — comes out the *cheapest*. That ordering is not
  earned by real numbers; it floats on pricing the giant pulsed-power driver at a
  future-target $0.50/J (10–30× below the cost its own sources cite) with the one
  source-anchored driver number switched off. → `concepts/07-maglif.md`

Both problems are the same failure mode wearing two hats: where an analyst hand-
entered a number (01's magnet override) it went 5× below source; where no number
was available (07) the model quietly took the most optimistic end of the library
defaults. The one concept with neither problem (21) is the de-facto baseline, and
it too is entirely library-driven — so there is no independently grounded anchor
in this cohort to check the others against.

## Family-internal coherence

- **MFE (01, 21):** They *look* coherent — 158.9 vs 168.4, CAS22 within ~5%. But
  the coherence is not real. 21 reaches 168 on library defaults with no overrides;
  01 reaches 155 only because its magnet override suppresses the dominant cost ~5×
  below its cited source. Correct 01's magnet account to its source and the two
  tokamaks split apart by a factor of three (507 vs 168). So this family clusters
  on paper but not on substance.
- **MIF (07):** Sole member — judged on cross-family ordering and traceability
  (below), not on clustering.

## Cross-family ordering

The ordering MagLIF (103) < tokamaks (155–168) runs opposite to maturity: the
pulsed-power MIF concept is generally less proven than HTS tokamaks, yet prices
out cheapest. Some of the gap is legitimate — MagLIF has no superconducting
magnets and a simpler chamber, so a lower reactor-plant cost is expected. But the
*size* of the gap is amplified by optimistic driver pricing (see traceability).
Once the pulsed-power driver is priced at today's cost rather than the future
target, or once a realistic plant-scale target cost is used, MagLIF rises to or
past the tokamaks. The ordering is therefore not trustworthy as it stands.

None of the three numbers is implausible on its face for fusion (all in the
$100–170/MWh band, which is high but in range for first-generation fusion). The
problem is not an absurd magnitude — it's that the magnitudes are set by
optimistic or mis-sourced inputs, not by the model doing the work.

## Source traceability on the big cost drivers

This is where the cohort is weakest.

- **01 (magnets, CAS22.01.03):** The $1,030M override cites a source table
  (`arc-reactor-specifications.md` §6 Table 11) that actually publishes
  $5,100–5,200M. The model's "derived" value is reached with learning-curve
  discounts (×0.4, ×0.5, ×0.9) whose inputs appear in **no** cited source, and it
  contradicts the concept's own analysis text, which prescribes $6,916M. Three
  numbers for one account, none reconciled. **Confirmed finding.**
- **07 (pulsed-power driver, CAS22 C220107 = 55% of CAS22):** Priced at the
  library default $0.50/J, the most optimistic figure in the cited material
  (sources say ~$5/J today, $15/J at the Z-IFE design point). The one override
  that ties the driver to a real $584M source value is present but **disabled**.
  **Confirmed finding.**
- **21:** No overrides — nothing mis-sourced, but also nothing independently
  anchored; the reactor cost is whatever the library defaults produce.

## Sensitivity

- **01:** The headline rides almost entirely on the one magnet number. Across its
  plausible range the 1 GWe LCOE swings from 127 (override off) to 507 (cited
  source value), with baseline 155. A single hand-entered number moves the answer
  by more than 3×.
- **07:** Well-behaved on the physics knobs (gain ±30% → 87/145, rep rate ±30% →
  96/118), but the target-cost assumption is highly leveraged and pinned low:
  $9/shot → 103, but $90/shot → 145 and $1,000/shot → 617. A plausible plant-scale
  per-shot cost alone erases MagLIF's cost lead. Driver efficiency is flat (that
  knob doesn't feed net power), which is expected, not a flag.
- **21:** Not separately perturbed; it behaves as the library-default baseline and
  showed no anomaly in the digest.

## Concepts flagged

- **`concepts/01-hts-compact-tokamak.md`** (high) — Dominant magnet override
  ($1,030M) is ~5× below its own cited source ($5.1–5.2B) and contradicts the
  analysis text ($6,916M); at the source value the LCOE would be ~507 not 155.
- **`concepts/07-maglif.md`** (high) — Cheapest in the cohort only because the
  pulsed-power driver is priced at an aspirational $0.50/J (10–30× below cited
  cost) with the source-anchored override disabled, plus an optimistic $9/shot
  target cost; both inputs strongly move the answer.

## Concept not flagged

- **21-spherical-tokamak-hts** — No finding. It carries no overrides, its numbers
  match the probe, and it clusters where a spherical HTS tokamak should. It is the
  cleanest of the three and serves as the cohort's baseline — with the caveat that
  it, too, runs on library defaults rather than concept-specific sourced costs.

## What no concept required

No concept was skipped for staleness or import failure — all three imported and
none were stale, so every number in this report reflects live model output.
