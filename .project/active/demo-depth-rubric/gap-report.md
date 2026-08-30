# Gap Report — Initial Grading vs Depth Rubric v1

**Created:** 2026-08-30 · **Status:** Complete — scores from the fresh grading (`grading.md`), author dispositions applied (no score changes)
**Rubric:** `rubric.md@dc0f0b6d` · **Model:** `dc0f0b6d` · **Executed baseline:** package `f97f0848…`, case `stellarator-baseline-point-v1:c0000` (`exploration/stellarator_e2e/studies/20260829-p-pump-fence/results/baseline_result.json`)

## What this answers

Which parts of the model are furthest below what a serious design effort would compute, weighted by what is actually load-bearing — so the owner can pick the first maturation goal.

## Headline

The model's shape is consistent everywhere the grade looked: the **cost side is uniformly parametric (S2–S3)** — every account follows a computed engineered quantity with a source basis — while the **physics side is uniformly held (P1) outside the plasma spine**. Only one cell in the plant meets a P3 anchor: build & wall load (R2a), where a computed wall load meets a real limit that demonstrably binds. Everywhere else, what a serious study would *compute*, this model *cites*. Five cells sit two full levels below target, all physics: R2c (TBR), R3 (magnets), R5 (divertor), R7 (heat transport), R11 (availability).

## Method

Per the design-evidence research (`.project/research/20260830-141348_demo-depth-rubric-design-evidence.md` §7): no weighted composite. Each row publishes its raw evidence vector — depth gaps, cost share with denominator named, constraint role, error history with measured consequence — then falls into a transparent priority band:

- **Band A** — material rubric gap + demonstrated leverage (cost concentration, a binding/masking/unresisted feasibility role, or a prior correction with a large measured consequence).
- **Band B** — material gap + partial or indirect leverage evidence.
- **Band C** — depth gap with no measured leverage yet (a study need, not proof of unimportance).

Within a band the owner chooses. Ordering inside bands is lexicographic: largest target gap, strongest measured consequence, current cost share.

## Evidence vectors

Cost denominator is **overnight capital $16.090B** unless stated. Scores are `score→target`; bold marks gap ≥ 2.

| Row | P | S | Cost share | Constraint role | Error history / measured consequence |
|---|---|---|---|---|---|
| 1 Plasma / operating point | 2→3 | n/a | — (cost lives in rows 3/4) | `beta_ok` real fence, but field is never rewarded through confinement — the optimum drives to the lowest B beta permits (`studies/20260823-magnet-technology-ab/synthesis.md` #4) | — |
| 2 Build / FW / blanket / shield / TBR | 2a: 3→3 ✓ · 2b: 2→3 · **2c: 1→3** | 3→3 ✓ | 7.5% (blanket+shield+structure $1.209B) + $97.1M/yr CAS72 stream | `wall_load_ok` binds (353/906 points, optimum on the fence); `tbr_ok` structurally inert — held vs held, unreachable from every swept axis (`studies/20260829-p-pump-fence/synthesis.md` §4) | — |
| 3 Magnets / PS / cryo | **1→3** | 2→3 | **39.3%** (coil channel $6.323B, >50% of power-core capital) | `peak_field_ok` is held×held vs held — margin 0.0 by construction, no design response | Field errata moved magnet capital **$4.39B → $6.32B** (`studies/DISCOVERY_LOG.md`) |
| 4 Heating / CD / fueling | 1→2 | 2→2 ✓ | 1.6% ($264M) | none of its own | — |
| 5 Divertor | **1→3** | 2→2 ✓ | 0.7% capital; shares the $97.1M/yr replacement stream | none — no divertor quantity exists to constrain | — |
| 6 Vessel / vacuum | 1→2 | 2→2 ✓ | 0.7% ($107M) | none | gas-load pumping omitted by doc (`mfe_account_costs.sysml:108-138`) |
| 7 Heat transport / power balance | **1→3** | 2→3 | 1.1% direct — leverage is feasibility, not capital | `recirc_ok`/`net_positive` decide feasibility, but the dominant pumping operand is held, so coolant choices cannot push back | Held p_pump re-based 1 → 195 MW: **LCOE +21.0%** (275.264 → 333.067), fence 32 → 184 violating points, 42 unevaluable negative-net points (`studies/20260829-p-pump-fence/synthesis.md` §§1-2) |
| 8 Power conversion / BOP | 1→2 | 2→2 ✓ | 3.1% ($497M) | — | efficiency moved LCOE **13.3–23.4%** in feasible space; equipment rates ≤1.1% (`studies/20260821-power-cycle-ab/synthesis.md` §2.2) |
| 9 Buildings / site / RH | n/a | 2→3 | 4.0% buildings + 8.1% RH+installation | CAS10 land term masks negative-net points (EI-1, WI-034) — evidence-integrity, not depth | — |
| 10 Fuel / tritium | 1→2 | 1→2 | 0.6% capital; $0.54M/yr fuel | none — and **no B-2 home** (flagged in rubric) | — |
| 11 Availability / replacement | **1→3** | 2→2 ✓ | no capital channel; $97.1M/yr replacement + availability multiplies every $/MWh | `no_constraint_response` — committed twice: nothing couples availability to core life or outage (`studies/20260821-power-cycle-ab/synthesis.md` #1; re-confirmed at current pin) | — |
| 12 CAS rollup / financing / estimate quality | n/a | 2→3 | indirect+contingency+IDC $8.85B (55% of overnight) | economic assumptions move the objective without touching a physical verdict | — |

`studies/` = `exploration/stellarator_e2e/studies/`. Evidence-integrity findings EI-1/2/3 recorded in `grading.md`; none changed a score.

## Priority bands

**Band A** — material gap, demonstrated leverage:

1. **Row 7 — heat transport / power balance** (P 1→3). Strongest measured consequence in the repo: one held input moved the objective by a fifth and tripled the feasibility fence. The feasibility constraints exist but cannot resist because their dominant operand is held. **Gate:** the owner ruled `p_pump` stays held (WI-033) — a goal here explicitly reopens that ruling or works around it (parasitics, loop model feeding a *check* of the held value).
2. **Row 3 — magnets / cryo** (P 1→3, S 2→3). Largest cost concentration (39.3% of overnight) and a $1.93B single-errata swing; the peak-field "constraint" has zero design response (held×held). Physics and cost gaps close together: derive field from coil geometry/current, add a stress or current-density limit, split the 5.87 markup into winding pack / structure / cryoplant.
3. **Row 2 physics — blanket/TBR + lifetime coupling** (2c 1→3, 2b 2→3). The inert `tbr_ok` is the rubric's own type case of a constraint that cannot resist; the computed lifetime stops one step short of availability. Joins naturally with Row 11's gap (below).
4. **Row 1 — confinement closure** (P 2→3). The broadest structural gap and the explanation for the field-unrewarded pathology — but the smallest numeric gap because the spine below it is genuinely computed. **Gate:** Rung C is owner-ruled out of scope; a high ranking triggers a grounding decision, never silently authorizes the work.

**Band B** — material gap, partial or indirect leverage: Row 11 (P 1→3 — committed `no_constraint_response`, denominator leverage, but no measured error event; largely closed by the Row-2 lifetime coupling), Row 8 (P 1→2 — measured 13–23% efficiency leverage, modest target), Row 12 (S 2→3 — 55% structural weight, no uncertainty treatment).

**Band C** — gap with no measured leverage yet: Rows 5, 6, 10, 4, 9 (S). Row 5's P gap is 2 but nothing measured makes it load-bearing today; Row 10's absence is flagged in the rubric (no B-2 home) so it cannot silently vanish.

## Candidate goal areas — for the owner to pick the first maturation goal

1. **Close the primary loop (Row 7).** Compute pumping and parasitics from a loop model (flow, pressure drop) so `recirc_ok`/`net_positive` push back on coolant and geometry choices. Highest measured stakes; requires an explicit owner ruling on the held-`p_pump` decision before grounding.
2. **Make the magnets real (Row 3).** Derive peak field from coil geometry and current, add a stress/current-density limit that pushes back on coil sizing, and decompose the markup into winding pack / structure / cryoplant sub-accounts. Attacks the largest cost concentration; no standing ruling in the way.
3. **Close breeding and lifetime (Rows 2c + 2b + 11).** Compute TBR from blanket configuration so `tbr_ok` can resist; couple the already-computed core life to outage duration and availability so the capacity factor stops being a free constant. Turns two committed underdevelopment findings into working constraints in one connected area.

Confinement closure (Row 1) is deliberately listed as a gate question rather than a candidate: it is the deepest structural fix and would make Row 7 and Row 3 physics more meaningful, but it reopens an explicit owner scope ruling — worth a yes/no from the owner before any goal is grounded on it.
