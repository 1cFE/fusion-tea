# 01-hts-compact-tokamak — The magnet cost was cut to one-fifth of its cited source, and the model and the write-up disagree on the number

## The issue
The single biggest cost in this concept is a hand-entered magnet cost of $1,030M (cost account C220103, the toroidal and poloidal field coils). The analyst labeled it "derived" and pointed at a source table to back it up. But that source table actually lists the magnet cost at about $5,100-5,200M — roughly five times higher than the number in the model. To make matters worse, the concept's own write-up prescribes yet a third number, $6,916M. So the model, the source it cites, and the concept's own analysis text all disagree with each other on the most important number in the whole estimate.

## Why it looks wrong
The override lives in `analyses/01-hts-compact-tokamak/model_setup.py`, lines 56-100: account C220103, value $1,030M, marked enabled, provenance "derived". It cites Table 11 of `arc-reactor-specifications.md` plus a learning-curve adjustment.

The numbers don't line up:

- That cited source (`knowledge/concept_research/01-hts-compact-tokamak/iter-03/sources/arc-reactor-specifications.md`, §6 Table 11) publishes a magnet that costs about **$5,100-5,200M**: magnet structure 4,350 tonnes at $4.6B fabricated, REBCO copper structure $380M, and REBCO tape (5,730 km) at $100M-$210M. The override of $1,030M is about **one-fifth** of that figure.
- The concept's own write-up (`analyses/01-hts-compact-tokamak/analysis.md`, Section 5b) says C220103 should be 5,200 x 1.33 = **$6,916M**, and calls that "the single largest and best-justified departure." So the analysis text and the actual model number differ from each other by about **6.7 times**.
- This one account dominates the estimate. The whole native reactor-plant total (CAS22) is $2,045M, and this single magnet override ($1,030M) is about **half** of it. The library's own default for this account is $567M, so the override nearly **doubles** the default.

How the $1,030M was reached: the model takes inflation (x1.26) and then stacks three learning-curve discounts on top — REBCO tape x0.4, structural fabrication x0.5, integration x0.9 (which multiply to x0.18). That works out to roughly $6,489M x 0.18 ≈ $1,168M, then nudged down to $1,030M. The specific inputs that drive all of this — a "$10-30/m NOAK REBCO" price target, a "$200-300M per coil" sanity check, and the 0.4 / 0.5 / 0.9 multipliers — appear in **none** of the cited sources. The learning-rate numbers trace back to an unpublished internal memo. One detail stands out: the structural steel cage is about 90% of the magnet cost ($4.6B of the $5.1B), and it gets the same x0.5 "mass-manufacturing" discount as the superconductor, with no reason given for cutting the cost of commodity steel fabrication in half.

Because this one number is so large, it controls the headline answer. Swinging just this account:

- Baseline $1,030M → 1 GWe LCOE of **155.2 /MWh**
- +30% ($1,339M) → 173.6
- -30% ($721M) → 136.7
- Override off, library default ($567M) → 127.5
- At the source's own value ($6,916M) → **506.7**

So this single hand-entered number moves the concept's whole answer by more than a factor of three.

## What the analysis says in defense
The analysis is upfront that the magnet is the concept's largest cost lever, and it openly applies a learning-curve / mass-manufacturing argument to bring the first-of-a-kind ARC magnet cost down to an "Nth-of-a-kind" number. The argument is a reasonable one in principle: REBCO tape and coil fabrication should get a lot cheaper once they're built in volume rather than one-off. The write-up frames this as a deliberate, documented choice, not something hidden. The real problem isn't that they applied a discount — it's that (a) the number in the model ($1,030M) doesn't match the number the analysis text itself prescribes ($6,916M), and (b) the inputs to the discount can't be traced to any of the cited sources.

## What a human reviewer should look at next
First, reconcile the two numbers that contradict each other: the override in `analyses/01-hts-compact-tokamak/model_setup.py` (C220103 = $1,030M) versus the analysis text in Section 5b of `analysis.md` (which says $6,916M). They cannot both be right — decide which one is actually intended. Second, require the discount inputs (the $/m REBCO target, the per-coil anchor, and the 0.4 / 0.5 / 0.9 multipliers) to be backed by a source someone can cite, not an unpublished memo. Pay particular attention to whether halving the structural-steel fabrication cost can be justified at all. Because the answer swings from about 127 to about 507 /MWh across the plausible range of this one number, this is the account that decides whether the concept lands near its tokamak neighbors or far above them.
