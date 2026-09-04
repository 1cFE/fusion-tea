# T-001 research return — the honest form of the wall-load check

Goal `wall-and-heating`, round 1 (`heating-chain-first`), task T-001. Written 2026-09-03 by the round agent from the two seam returns and from the registered extractions read directly. Every number below is either printed in a registered source or is arithmetic on printed numbers, shown. **Nothing is defaulted, and nothing here decides the fence's form** — that is round 2's model task, on this evidence.

Spawn prompts: `T-001_REQ-WALL-01_prompt.md`, `T-001_REQ-WALL-02_prompt.md`. Runs: `knowledge/research/requests/runs/REQ-WALL-01/20260904T035638551421/return.json`, `knowledge/research/requests/runs/REQ-WALL-02/20260904T035641288429/return.json`. Both closed `REGISTERED`, `--adequacy exhausted`.

## 1. What the model does today

`wall_load = p_fus x (1 - ash_frac) / wall_area`, with `wall_area = kappa x 4 pi^2 x R x vacuum_or` (`models/library/analyses/mfe_plasma_scaling.sysml:52`). At the Stellaris build — `R = 12.7`, `kappa = 1.0`, `a = 1.3`, `vacuum_t = 0.10` so `vacuum_or = 1.40` (`models/designs/stellarator_09/stellarator_plant.sysml:472-502`) — that is **701.926 m^2**, and the pinned baseline reads **3.105376639122585 MW/m^2** (`20260903-priced-levers/results/baseline_result.json`, channel `stellarator_09__stellaris__wall_load_calc__wall_load`).

Two things about that area matter for everything below. It is a **circular cross-section torus**, not a stellarator wall. And its radius is **wall-side** — plasma minor radius plus a 0.10 m vacuum gap — not the plasma minor radius. The second point is the one that decides whether a published shape factor transfers, and it is easy to get wrong.

The limit it is compared against is `wall_load_limit = 4.05`, the source's printed **peak** design value (`:1079-1081`). Operand and limit are not the same quantity. That is the defect this task researched.

## 2. Three admissible sources now in the repository

| source | machine | what it prints |
|---|---|---|
| Lion, Warmer, Xu, *A deterministic method for the fast evaluation and optimisation of the 3D neutron wall load for generic stellarator configurations*, Nucl. Fusion **62** (2022) 076040, CC BY 4.0 — `knowledge/sources/a_deterministic_method_for_the_fast_evaluation_and_2/` | HELIAS-3/4/5, a QA stellarator | Table 1: `R`, `a`, `S_FW`, `Q_max`, `Q_avg`, and the peaking factor `p_f = q_max / <q>` for each, all at 3 GW fusion power with the first wall placed **equidistant 30 cm from the LCFS** |
| Häußler, Warmer, Fischer, *Neutronics analyses for a stellarator power reactor based on the HELIAS concept* (ISFNT-13) — `knowledge/sources/neutronics_analyses_for_a_stellarator_power_reactor_based/` | HELIAS-5B | Table 2 at 3000 MW fusion: max/average NWL 1.936/0.953 (MCNP5+DAGMC) and 1.958/0.926 (`nflux` ray tracing), averaged over "the total plasma facing area" |
| Beidler et al., *The Helias Reactor*, IAEA-CN-77/FTP1/16 (2001) — `knowledge/sources/the_helias_reactor_beidler_et_al_iaea_cn_77_ftp1_16/` | HSR5/22, HSR4/18 | First-wall area 2600 m^2 at `R = 22`, `<a> = 1.8`; 2500 m^2 at `R = 18`, `<a> = 2.1`; average NWL "less than 1 MW/m^2" and **peak 1.7 MW/m^2** at 3000 MW fusion |

**Every one of them averages over the shaped 3D wall.** None averages over a circular torus, and none averages over the plasma surface. That is the finding that governs both candidate forms.

**Extraction sanity check, run here.** Lion's Table 1 is internally consistent: `Q_avg x S_FW` reproduces the 2400 MW of neutron power implied by 3 GW fusion at 20% alpha fraction to within 3% for all four configurations (2408, 2424, 2321, 2497 MW), and `Q_max / Q_avg` reproduces the printed `p_f` to the table's rounding (1.571 vs 1.59; 1.667 vs 1.67; 1.727 vs 1.69; 1.517 vs 1.51). The numbers hold together.

## 3. Result 1 — a peaking factor exists, and it is a property of the wall, not the plasma

Lion Table 1, unoptimised equidistant walls: **1.59** (HELIAS-3), **1.67** (HELIAS-4), **1.69** (HELIAS-5), **1.51** (QA stellarator). The paper's own summary: peaking factors "larger than 1.5–1.7 ... for several distinct stellarator devices".

The same HELIAS-5 plasma gives **1.23** and **1.12** for two *optimised* wall shapes in the same table. The peaking factor is not a plasma property to be looked up; it is a consequence of the wall you choose. Any number carried into the model must carry its wall definition with it.

Independent corroboration, different method and different wall: Häußler's HELIAS-5B gives **2.03** (MCNP) and **2.11** (ray tracing) over the CAD tungsten armour; Beidler's HSR5/22 gives 1.7 peak over an average of 2400/2600 = 0.923, i.e. **1.84**. Read together, three sources bound the unoptimised stellarator first-wall peaking factor at roughly **1.5 to 2.1**, the spread explained by wall geometry and method rather than by disagreement about physics.

## 4. Result 2 — a shaped-wall area exists too, and the two sources disagree until you fix the radius

This is the cross-check neither research session could run on its own, because each held only one source.

Both papers publish an area alongside radii for essentially the same machine line, and the naive ratio against `4 pi^2 R a` does **not** agree:

| | `R` | `a` | `S_FW` | `4 pi^2 R a` | ratio on **plasma** radius |
|---|---|---|---|---|---|
| Lion HELIAS-5 (30 cm equidistant wall) | 22.2 | 1.8 | 2110 | 1577.6 | **1.338** |
| Beidler HSR5/22 (standoff not published) | 22 | 1.8 | 2600 | 1563.3 | **1.663** |
| Beidler HSR4/18 (standoff not published) | 18 | 2.1 | 2500 | 1492.3 | **1.675** |

A 24% disagreement about the same reactor line. The explanation is not a contradiction between the sources — it is that a ratio taken against the *plasma* minor radius silently absorbs the plasma-to-wall standoff, and the two papers use different standoffs. Beidler never publishes his, so **his 1.66 cannot be transferred to the model at all**: the model's `vacuum_or` is already a wall-side radius, and applying 1.66 on top of it double-counts the gap. The REQ-WALL-02 session flagged exactly this risk in its own return; the second source is what confirms it.

Lion publishes his standoff (`D_pw = 30 cm`), so his area *can* be put on the model's own basis — the wall standoff radius `a + gap`:

| case | `4 pi^2 R (a + 0.3)` | `S_FW` | ratio on **wall-side** radius |
|---|---|---|---|
| HELIAS-3 | 1371.9 | 1720 | **1.254** |
| HELIAS-4 | 1598.1 | 2020 | **1.264** |
| HELIAS-5 | 1840.5 | 2110 | **1.146** |
| QA stellarator | 660.9 | 861 | **1.303** |

On the convention the model actually uses, stellarator shaping adds roughly **15–30%** of wall area over a circular torus of the same wall-side radius — not 66%. The four configurations agree far better on this basis than the two sources did on the plasma basis, which is itself evidence that the wall-side radius is the right comparand.

**One honest gap, stated and not papered over:** the model's standoff is `vacuum_t = 0.10 m`; Lion's is 0.30 m. A wall pulled closer to the plasma gains less area and peaks harder. Neither the factor nor the peaking figure is measured at a 0.10 m standoff by any source in hand, and no source here licenses adjusting either. Whether the model's 0.10 m gap is itself the right radial build is a separate question this task did not ask.

## 5. What this means for the two candidate forms

**Both forms now have an admissible basis, and neither is free.**

- **Computed peak against the printed peak limit.** A peaking factor exists (1.5–2.1, or 1.69 for the closest single analogue). But it is defined against a *shaped-wall* average, so applying it to the model's circular-torus average is not the same operation. Taking this form honestly means fixing the area basis at the same time — the peaking factor and the shape factor come from the same table and belong together.
- **Average operand against a sourced average limit.** Lion's `Q_avg`, Häußler's 0.953, and Beidler's "less than 1" are all published averages — but every one of them is an average over a shaped wall, so the same area correction is needed before the model's average is comparable to any of them.

The two forms converge on the same prerequisite: **the model's flat-wall area is the thing that is actually wrong**, and neither form is honest without addressing it. That is a sharper statement of the defect than the goal was grounded on, and it is a finding, not a decision.

**For scale only, not a claim, and not a proposal.** Taking Lion's HELIAS-5 pair together — shape factor 1.146 and peaking factor 1.69 — the net multiplier on a circular-torus average is 1.69/1.146 = **1.475**, which would put the pinned baseline at 3.105 x 1.475 = **4.58 against the 4.05 limit: violated**. The goal's grounding arithmetic estimated 1.41 and 4.38 from the source's own peak-to-average ratio; this refines it in the same direction. It is not a prediction — the model's standoff is 0.10 m, not 0.30 m, and the transfer is exactly what round 2 has to argue. It is recorded because `goal.md` § Invariants requires that a tighter check with a violated baseline be disclosed and explained, **never tuned away**, and because a round that walks into that result should have expected it.

## 6. Clean room

**No candidate had to be refused on ARIES-CS grounds in REQ-WALL-01.** No ARIES-CS paper or ARIES-CS-calibrated comparison surfaced; both registered extractions were grepped for `aries` before registration with zero hits.

**One refusal in REQ-WALL-02, recorded and correct:** `sciencedirect.com/science/article/pii/S0920379626003273`, "Preliminary engineering design of the first wall and X-point divertor of the **Helios** planar coil stellarator" — barred under PROTOCOL.md §3, **not fetched**, logged `rejected` with the reason.

**A hazard worth naming for every future session in this area.** *Helios* (planar-coil, barred) and *HELIAS* (the W7-X-line quasi-isodynamic reactor, admissible) differ by one letter and surface in the same result set. Both appeared in one search here. The screen held because it was applied before the fetch; the registry guard would not have helped, because it fires at registration.

## 7. Defect found — a junk registry entry an operator must remove

`knowledge/sources/a_deterministic_method_for_the_fast_evaluation_and/` (no `_2` suffix) is a **1415-byte Radware bot-check page**, not a paper. IOPscience served it to the extractor, which extracted it successfully, so nothing in the seam caught it — there was no hold-out term to scan and no capture failure to report. It is committed in `knowledge/MANIFEST.jsonl` and has a block in `knowledge/SOURCE_INDEX.md:382-392`.

The real paper is correctly registered at the `..._2` slug from the publisher PDF, and that entry's `Caveat` already names the junk slug in the index itself, so a reader who lands on either one is warned. Nothing about the research question is blocked.

**It is left in place deliberately.** `source_registry.py` has `register` and `verify` and no `unregister`, and the registry's whole contract is that four files move together or none do — hand-editing a source directory, a manifest row and an index block to undo one registration is exactly the ad-hoc surgery that contract exists to prevent. Routing around a missing operation is not this task's call. Surfaced for the owner in the trail; the tooling gap (no `unregister`, and no guard against an extractor happily extracting a bot wall) is the durable finding.

## 8. Answer to the task's question

An admissible sourced basis exists for **both** candidate honest forms, from three registered open-literature sources, none of them hold-out material. A stellarator first-wall peaking factor is real, published, and bounded at roughly 1.5–2.1 for unoptimised walls — but it is a property of the chosen wall, not of the plasma, and it is defined against a shaped-wall average. A shaped first-wall area is also published, and on the model's own wall-side radius convention it is 15–30% larger than the circular torus the model integrates over.

The finding that outranks both: **the model's circular-torus area is the defect that has to be addressed either way.** Round 2 chooses the form and argues the transfer at a 0.10 m standoff. This task hands it sources, an internal consistency check, an explained disagreement between two of them, and a scale figure that says the honest fence probably tightens.
