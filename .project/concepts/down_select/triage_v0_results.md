# Triage v0 — applied to all 38 concepts

**Source data:** Executive summaries from `exploration/concept_analysis/analyses/{id}/synthesis.md` (36 concepts) + dossiers from `knowledge/concept_research/{id}/dossier.md` (2 concepts without synthesis: 04, 11). Pull date: 2026-05-11.

**Signal definitions** (from `decision_output_schema_v0.md` §1):
- **T1** Data sufficiency {sufficient, marginal, insufficient}: synthesis present AND specifies design parameters AND has cost basis.
- **T2** LCOE floor plausibility {<$100/MWh, $100–200, >$200}: lowest defensible number from the synthesis (scaled-to-1GWe or optimistic-scenario where stated, *not* point central).
- **T3** Stage-1 feasibility {near-gate, mid-gate, far-gate-thin}: near = burning-plasma device within ~3 years OR physics demonstrated; mid = single binary gate but credible 10-year path; far-thin = unvalidated physics regime with no organized program path.

**Verdict rule:** insufficient (any single T) OR (T2>$200 AND T3 not near) OR T3 far-thin → eliminate. Otherwise shortlist. Auto-include reserved for concepts where all three are strongly positive — none qualify on triage alone (auto-include is meant for cases like "concept X has both ignition demonstrated *and* a NOAK floor under $100" — none of the 38 have both).

---

## Surprise finding — data is more available than entry 005 estimated

Entry 005 (next-pass note) assumed "only 8 fully synthesized." Actual: **36 of 38** have full syntheses with structured executive summaries (single most important risk, advantage, LCOE ballpark, confidence verdict). Only 04-laser-icf (HB11) and 11-magnetic-mirror (Realta) lack syntheses — both have rich dossiers. **The data-availability problem is essentially solved** at the triage level. T1 will rarely fire as a sole eliminator.

This changes the methodology: T1 is mostly a no-op given current materials; T2 and T3 carry the triage. The original triage proposal over-weighted T1.

---

## Results table

| ID | Concept | T1 | T2 (LCOE floor) | T3 | Verdict | Reason |
|---|---|---|---|---|---|---|
| 01 | HTS compact tokamak (CFS ARC) | suff | 100–200 (CATF target conditional) | near | **shortlist** | already trace #1 |
| 02 | Acoustic ICF / sonofusion | marg | n/a (binary go/no-go) | far-thin | eliminate | 10⁴ K vs 10⁸ K physics gap; 9/15 blocking gaps |
| 03 | Laser ICF liquid-jet target | marg | n/a (model "meaningless") | far-thin | eliminate | Q~100 rests on single preprint with anomalous 3333 MeV/event |
| 04 | Laser ICF p-B11 (HB11) | marg | n/a | far-thin | eliminate | 4 orders of magnitude from net energy gain |
| 05 | Planar-coil stellarator (Thea) | marg | 150–241 | near | **shortlist** | physics established; cost structure unknown |
| 06 | Magnetic mirror p-B11 | marg | 40–58 speculative | far-thin | eliminate | nonthermal p-B11 never demonstrated |
| 07 | MagLIF (Pacific Fusion) | suff | 30–61 | mid | **shortlist** | rep-rate is the gate, not physics |
| 08 | FRC w/ direct conversion (Helion) | suff | 50 conditional | mid-far | **shortlist** | binary D-He3 gate but exceptionally documented |
| 09 | QI stellarator HTS (Proxima) | marg | 106–165 | near | shortlist (or merge w/ 05) | overlaps 05; 3D coil cost is the gate |
| 10 | Large-scale stellarator | marg | 213–252 | near | eliminate | floor >$200 even at optimistic NOAK |
| 11 | Magnetic mirror D-T (Realta) | marg (no synth) | unknown | mid | **shortlist** | rich dossier; WHAM operational, clear path |
| 12 | Levitated dipole | suff | 134–211 scaled | mid-far | **shortlist** | 240× confinement extrapolation but Tahi prototype 2028 |
| 13 | Electrostatic hybrid (Avalanche) | suff | 4,800 (best NOAK) | far-thin | eliminate | 100× too expensive; thermalization unrefuted |
| 14 | MTF pneumatic compression (General Fusion) | suff | 78–104 | mid | **shortlist** | LM26 demonstrates physics; pneumatic system unbuilt |
| 15 | SFS Z-pinch (Zap) | suff | 145 | far (Q-gate) | **shortlist** | already trace #2 |
| 16 | Muon-catalyzed | suff | 2,090 (net negative at stated targets) | far-thin | eliminate | physically impossible at stated parameters |
| 17a | Laser ICF hybrid drive (Xcimer) | suff | 87–111 | mid | **shortlist** | Xcimer requires gain >100× |
| 17b | Laser ICF fast ignition | marg | 67 lower bound; realistic >80 | far-thin | eliminate | proton fast ignition never demonstrated gain >1; overlap w/ 17a |
| 18 | p-B11 FRC (TAE Da Vinci) | suff | 119 baseline; range 50–740 | far (50–80× T_i extrap) | **shortlist** | aneutronic; TAE has data unlike 06 |
| 19 | Orbital levitated dipole | **insuff** | 491–11,800 | far-thin | eliminate | 2-person YC startup; no technical papers |
| 20a | Type One stellarator | marg | 150–337 scaled | near | eliminate | covered by 05/09; coil cost dominates |
| 20b | Renaissance stellarator | marg | 99–517 | far (Lawson 11× short) | eliminate | ignition target physics inconsistent with scaling |
| 21 | Spherical tokamak HTS (Tokamak Energy) | marg | 140 scaled | mid | **shortlist** | structurally distinct from 01; Demo4 validated |
| 22 | Projectile ICF | suff | 84 scaled; orphaned | n/a | eliminate | **First Light abandoned this approach Sep 2025** |
| 23 | Laser ICF nanostructured target | marg | 38 scaled | far-thin | eliminate | 4-order-of-magnitude physics gap |
| 24 | Dense plasma focus (LPP) | marg | 1.3 ¢/kWh aspirational | far-thin | eliminate | 660,000× Q improvement required |
| 25 | Heavy-ion-beam ICF | **insuff** | 92–160 | n/a | eliminate | **"no commercial company exists pursuing this"** |
| 26 | Laser ICF indirect drive | suff | 80–160 | near | **shortlist** | NIF ignition demonstrated; strongest IFE pedigree |
| 27 | Polywell (EMC2) | marg | 6.1 ¢/kWh scaled (γ=0.1) | far-thin | eliminate | γ never validated at reactor density |
| 28 | Full-HTS tokamak (China HH380) | marg | 70 scaled | mid | **shortlist** | state-backed; spans supply-chain axis |
| 29 | Negative-triangularity tokamak (Firefly/MANTA) | suff | 90–96 | mid | **shortlist** | NT divertor advantage; only L-mode validated |
| 30 | Laser ICF NIF commercialization | marg | 120–189 | near | shortlist (or merge w/ 26) | overlap w/ 26 |
| 31 | Laser ICF OEC architecture | marg | 51–52 conditional | mid-far | eliminate | overlaps 30; OEC mirror lifetime unknown |
| 32 | Laser ICF French national (GenF) | marg | 90–129 | far (TBR 3,000× short) | eliminate | TBR binary feasibility gate |
| 33 | State-backed tokamak (China BEST) | marg | 51–87 (w/ China discount) | near | shortlist (or merge w/ 28) | overlap w/ 28; spans private-vs-state axis differently |
| 34 | Compact ST India (Pranos) | **insuff** | 630 | far-thin | eliminate | founded May 2024, $417K seed, no peer pubs |
| 35 | Polomac magnetic confinement | marg | 230–950 | far-thin | eliminate | D-D physics regime no experimental precedent |
| 36 | Helical-coil stellarator (HESTIA) | marg | 1,200–1,800 | far-thin | eliminate | LCOE 10× viability ceiling |

---

## Summary

- **Shortlist (12, after merging near-duplicates):** 01, 05 *(or merge with 09)*, 07, 08, 11, 12, 14, 15, 17a, 18, 21, 26 *(or merge with 30)*, 28 *(or merge with 33)*, 29. With aggressive de-duplication: 12 concepts. With loose: 14.
- **Eliminated (24–26):** 02, 03, 04, 06, 10, 13, 16, 17b, 19, 20a, 20b, 22, 23, 24, 25, 27, 31, 32, 34, 35, 36 — plus the merged-out (one of 05/09, one of 26/30, one of 28/33).
- **No auto-includes.** The "all three strongly positive" condition is met by ~0 concepts. Auto-include is a useless category as defined.

### Eliminate-reason taxonomy (from the 26 eliminations)

| Reason | Count | Examples |
|---|---|---|
| Far-gate-thin physics (no demonstrated path) | 14 | 02, 03, 04, 06, 13, 16, 17b, 20b, 23, 24, 27, 32, 35 |
| T2 floor catastrophically high (>$300/MWh) | 5 | 10, 19, 34, 35, 36 |
| Orphaned (no active org pursuing) | 2 | 22 (First Light pivot), 25 (no company exists) |
| Insufficient documentation | 3 | 19, 25, 34 (overlap w/ orphaned) |
| Near-duplicate of stronger shortlist member | 4 | 09, 17b, 31, 30 (or 26) |

The biggest single signal is **T3 far-thin**: 14 of 26 eliminations are physics regimes with no organized program. This is what makes the 38-concept population tractable — over a third of concepts are dominated by physics gates that haven't moved in decades.

---

## Findings that change the methodology

1. **T1 is mostly a no-op given current data.** 36/38 have syntheses. Only 3 concepts (19, 25, 34) eliminate primarily on T1, and all three have other failures (T2 or T3) anyway. Recommendation: **drop T1 as a standalone signal**; fold "documentation depth" into T3 (far-thin already captures "no organized program").

2. **T3 carries the load.** 14 of 26 eliminations are far-thin physics. T3's near/mid/far-thin trichotomy is the workhorse. Need to operationalize the trichotomy more carefully — currently judgment-based.

3. **T2 floor needs a basis qualifier.** Several concepts have low LCOE *because the model assumed the binary physics gate already closed* (06, 17b, 24, 27). T2's "<$100" doesn't mean what it looks like if the floor is conditional on an unvalidated physics step. Recommendation: **T2 should be a conditional tuple**: (floor, gating-condition). Where gating-condition exists and is unvalidated, T2 should not be allowed to "save" a far-thin T3.

4. **Orphan check is a free signal.** "Company pivoted away" (22) or "no company exists" (25) is an obvious eliminator and is in the synthesis text. Add a **T4 orphan check** — binary, cheap, eliminate-only. Cost: scan synthesis for "abandoned/pivoted/no commercial company/orphaned." This catches 22 and 25 without requiring T1/T2/T3 judgment.

5. **Near-duplicate detection is the hardest call and it matters.** The shortlist contains pairs (05/09, 26/30, 28/33, 17a/17b) where deep-diving on both teaches little incremental. Triage doesn't merge these — needs a **shortlist-dedup pass** between triage and trace. This is a Part-A (set-level) concern that surfaces *before* trace work. The dossier-schema's Part-A spanning logic should have a pre-Part-B "near-duplicate collapse" step.

6. **Cohort-role becomes assignable from triage alone**, not requiring a trace. ARC (01), Helion (08), General Fusion (14), Tokamak Energy (21), Pacific Fusion (07) are all first-mover-cohort-rich (well-funded, peer-reviewed, multiple iterations). Zap (15), Realta (11), TAE (18) are first-mover-cohort-thinner. State-backed (28, 33) are a separate category. **Cohort-role can be assigned at triage and used as input to spanning** — it doesn't need to wait for trace.

---

## Recommended shortlist for tracing (12 concepts, with spanning rationale)

| # | Concept | Spanning role | Cohort role |
|---|---|---|---|
| 01 | HTS compact tokamak (ARC) | D-T MFE archetype, cohort-rich first-mover | first-mover, cohort-rich |
| 05 | Planar-coil stellarator (Thea) | stellarator archetype; modular construction extreme | first-mover, isolated |
| 07 | MagLIF (Pacific Fusion) | pulsed MIF; capital-intensive driver, no SC magnets | first-mover, cohort-thin |
| 08 | FRC + direct conversion (Helion) | D-He3 aneutronic gambit; binary fuel-cycle bet | first-mover, isolated |
| 11 | Magnetic mirror (Realta) | linear D-T geometry; structurally simpler | first-mover, cohort-thin |
| 12 | Levitated dipole | inherent disruption immunity; magnet sacrificial cost | first-mover, isolated |
| 14 | MTF pneumatic (General Fusion) | MTF + liquid metal wall; novel piston compression | first-mover, isolated |
| 15 | SFS Z-pinch (Zap) | physics-gated isolated; no SC magnets | first-mover, isolated |
| 17a | Xcimer (hybrid drive IFE) | DPSSL + FLiBe wall; mid-cost IFE | adjacent to laser-ICF cohort |
| 18 | p-B11 FRC (TAE) | aneutronic + FRC; well-documented | first-mover, cohort-thin |
| 26 | Laser ICF indirect drive | NIF-heritage IFE; strongest physics pedigree | adjacent to NIF cohort |
| 28 | Full-HTS tokamak (China HH380) | state-backed supply-chain bet | state-backed, fast-follower |

This set spans: confinement family (MFE×7, IFE×2, MIF×2, MTF×1), fuel cycle (D-T×8, D-He3×1, p-B11×2, D-D unbroached), magnet class (HTS×6, copper/none×6), driver class (steady-state×7, pulsed×5), cohort role (cohort-rich×1, cohort-thin×3, isolated×6, state-backed×1, adjacent×2).

**Concentration risk:** D-T is over-represented (8/12). That's a fair reflection of where private investment + data sufficiency live; it's not a bug.

---

## What this changes about next-pass action

The original entry-005 next-pass action ("operationalize T1/T2/T3 — single CSV") is now done. The triage table above *is* that CSV. The next *next-pass* actions in order of priority:

1. **Trace #3 = pick from shortlist by spanning need.** The most informative candidate is one of: 08-Helion (aneutronic, binary fuel-cycle bet), 14-General Fusion (MTF, liquid wall, isolated), 26-Laser ICF (NIF heritage, IFE archetype). Helion (08) is highest-spanning value because it's the only D-He3 concept and the cohort role is "first-mover, isolated" with rich documentation — a structurally new cell.
2. **Add the T4 orphan-check + T2-conditional-tuple revisions** to the triage definition; re-run is unnecessary because the 38 results don't change.
3. **Defer shortlist dedup (the 05/09, 26/30, 28/33, 17a/17b pairs)** until the spanning algorithm is exercised — these merges might be wrong in light of spanning need.
