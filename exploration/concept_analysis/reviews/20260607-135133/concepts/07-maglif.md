# 07-maglif — MagLIF comes out cheapest in the cohort, but only because its driver and target costs are entered at their most optimistic possible values

## The issue
MagLIF lands at $102.9/MWh at 1 GWe, the cheapest concept in the whole cohort and about 35% below the two HTS tokamaks (159 and 168). That is surprising, because MagLIF is arguably the least-proven approach here. When you look at where the cheapness comes from, it does not trace back to any real Pacific Fusion or Sandia Z dollar figures. It rests on two hopeful default assumptions in the cost library: a giant pulsed-power driver priced at a future target the sources themselves say is 10 to 30 times below today's cost, and a per-shot consumable priced at $9 per shot. Both assumptions push the number down, and both move it a lot when changed. On top of that, the model actually contains an override that would have tied the driver to a real, source-derived dollar value — and that override is switched off.

## Why it looks wrong
The reactor-plant total (CAS22) is $3,961M at 1 GWe. That is about half of what the two tokamaks cost (roughly $7,618M and $8,035M). MagLIF's native plant size is already 1,000 MWe, so none of this gap comes from scaling a small design up or down.

The single biggest piece of that reactor-plant total is the pulsed-power supplies account, C220107, at $2,184.5M — which is 55% of all of CAS22. The model gets that number by multiplying $0.50 per joule by 4,369 MJ of stored energy (`costingfe` library: `layers/cas22.py` line 457, with the coefficient in `defaults.py` line 171, labeled "NOAK all-in").

That $0.50/J is the most optimistic figure anywhere in the cited material:
- The roadmap source (Ellison et al., arxiv-2408-15206 §3.2.4) says "the cost of energy storage and switching must decrease by a factor of 5 to 10." In other words, it is not there yet.
- The analysis's own Section 4 says "current capacitor costs are ~$5/J; the target is <$0.50/J." So today's cost is about 10 times higher than the number used.
- The Z-IFE design-point source prices it at $15/J delivered to the pinch — about 30 times higher than the number used.

If you plug in those other numbers, this one account explodes. At $5/J it would be about $21.8B. At $15/J it would be about $65.5B. The model used $2.18B.

Meanwhile, `analyses/07-maglif/model_setup.py` contains exactly one override, and it is for this very account, C220107. It sets the driver to a source-derived $584M (2024 dollars) — and it is marked `"enabled": False`. So the one number that was actually tied to a real source is turned off, and the optimistic library default is what stands.

The other soft spot is the per-shot consumable. The `costingfe` file `data/defaults/pulsed_maglif.yaml` sets the target-and-liner cost at $9 per shot (a beryllium liner around $4.7 plus a steel return-current can around $5, citing Goodin 2004 / SAND2006-6590). The annual consumable account (CAS80) comes to $35.6M/yr, computed for one chamber running at 0.1 Hz — about 2.7 million shots a year. But elsewhere the analysis itself discusses a 10-chamber plant firing one shot per second, which is about 31.5 million shots a year. The annual cost is built on the smaller, single-chamber shot count.

## What the analysis says in defense
The analysis is honest and up-front about all of this. It states plainly that no plant-level cost figures could be pulled from Pacific Fusion or the other sources, so it deliberately falls back on the library defaults for every reactor-plant account, and it labels the driver unit cost and the target cost as low-confidence (Section 5b: "the library defaults stand for all accounts"). It also correctly points to repetition rate and gain as the real levers on the answer.

And part of MagLIF's lower cost is genuinely earned. It has no superconducting magnets and uses a simpler, liquid-wall chamber, so some gap below the tokamaks is exactly what you'd expect. The sensitivity numbers back up that the analysis identified the right knobs (baseline 1 GW LCOE is 102.9):
- Engineering gain q_eng, nudged ±30%: 145.3 / 86.8 — moves roughly in proportion, well-behaved.
- Repetition rate ±30%: 117.5 / 95.8; doubled it drops to 89.0, halved it rises to 137.8.
- Driver efficiency ±30%: basically flat at 102.8–103.0 — that knob doesn't feed net power here.

So the concern is not that the analysis hid anything. It's that the size of the gap below the tokamaks is inflated by pricing the driver at the rosiest end of the cited range while the realistic, source-anchored value sits disabled.

## What a human reviewer should look at next
First, decide what cost year and maturity level the whole portfolio is supposed to represent, then make the driver price match it. Look at account C220107 and the $0.50/J coefficient in the `costingfe` library (`defaults.py` line 171) against the current cost the sources cite (~$5/J) and the Z-IFE design point ($15/J). Then look at why the source-derived $584M driver override in `analyses/07-maglif/model_setup.py` is switched off — that is the one number tied to a real source, and turning it back on would change the headline a lot.

Second, check the $9/shot target cost in `pulsed_maglif.yaml` and the single-chamber shot count behind CAS80, because target cost moves the answer hard. The sensitivity run shows that target cost alone, at plant-realistic levels, is enough to erase MagLIF's lead: at $45/shot the LCOE is 121.6, at $90/shot it is 144.9, at $100/shot it is 150.1 — already above both tokamaks — and at $1,000/shot it is 616.8.

The core question for the reviewer: is MagLIF genuinely the cheapest concept in the cohort, or does it only look that way because its hardest, least-proven costs are entered at their most optimistic possible values?
