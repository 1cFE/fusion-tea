The checkpoint entry is written. Stopping there, as the brief requires.

## Verdict: C-001.r2 passes — no required changes

I re-derived everything rather than checking the return's working.

**All three r1 required changes are applied, and each is right.**

- **`#5`** — the sighting at `DISCOVERY_LOG.md:11` really does read `unrouted`, so the row was owed a disposition. I verified the recipe the new row offers as its next reference, and it's stronger than claimed: reconstructing `rec_frac`/`p_net` from the committed `p_fus` and `eta_th` columns reproduces the oracle exactly not just at baseline but at two off-baseline corners (R=4,a=0.8 → 0.9424/8.3; R=20,a=2.2 → 0.0572/4529.2). `declared seam` is the right kind — `upstream filing` would name an action outside this repo the round can't perform.
- **Moscato** — the figures are in the repository at `…wi031-item6-second-arm-values.md:43` (131/2101.7 = 6.2%, 83–94 MW = ~4%). Admitting them at a stated second-order grade turns the answer into a range and is the honest handling.
- **Precision** — ~6% rather than 6.279% moves the value from "above DI-008's band" to "at its top". I confirmed the arithmetic: `p_th` = 3238.12 MW, 4–6% → 129.5–194.3 held, 132.1–200.3 computed; `rec_frac` 0.1514 → 0.2659/0.3219 and 0.1160 → 0.1971/0.2368; no verdict flip at 0.5.

**The dispute goes to the round agent.** `…purl-1178069.md:157` settles it outright — "ACT1 uses the self-cooled PbLi concept… whereas ACT2 uses a dual-cooled blanket… ACT2 is the first… using the DCLL blanket." C-001.r1's parenthetical was inverted; my entry records that so it doesn't stand as fact. Nothing downstream changes.

**Two observations, not required changes.** ACT2 cools about half its blanket with helium (`:157`, He:LiPb 49:51 at `:197`) — the strongest counter to D-2, and it points the round's way, since including it would pull the floor down. And the 1% vs 2% tension the revision flagged is resolved at `:100`, which neither entry cited: ~1% is whole-plant He+LiPb, 2–3% is the divertor loop.

Citation liveness checked with `git log -1` — every cited sha is current, and nothing outside the goal directory was written. The central conclusion (1.0 MW is not defensible) survives at any precision, either end of the range, and even against ARIES-ACT's ~1%.

Nothing committed — the entry is written to `work/orchestration/goals/p-pump-basis/trail.md` for you to commit.