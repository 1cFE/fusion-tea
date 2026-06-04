# Validation Review: Concept 07 — Pacific Fusion MagLIF

**Concept**: 07-maglif (Pacific Fusion — AMPS pulser-driven MagLIF commercial FPP)
**Model under review**: [`exploration/concept_analysis/analyses/07-maglif/model_setup.py`](../exploration/concept_analysis/analyses/07-maglif/model_setup.py)
**Source pinned by the model**: [`z-ife-sand2006-7148-thermal-cycles.md`](../knowledge/concept_research/07-maglif/iter-02/sources/z-ife-sand2006-7148-thermal-cycles.md) — Sandia Z-IFE concept study, 2006 (program terminated 2007)
**Source that should be pinned**: [arXiv:2504.10680](https://arxiv.org/pdf/2504.10680) — *Affordable, manageable, practical, and scalable (AMPS) high-yield and high-gain inertial fusion*, Pacific Fusion et al., Apr 2025. Already in the research pool at [iter-03](../knowledge/concept_research/07-maglif/iter-03/sources/arxiv-2504-10680/output.md).
**Reviewer**: Mallory Snowden (with Claude assistance)
**Review date**: 2026-05-28

---

## TL;DR

Concept 07's cost model is built on a 2006 Sandia *Z-IFE* concept study and not on Pacific Fusion's own 2025 design publication — even though that publication is sitting in the same concept's iter-03 research pool. The mismatch isn't only a sourcing error: the model also extracts a *per-chamber* driver specification from the Z-IFE study and applies it to a *full-plant* net-electric target, an architectural scale mismatch the Z-IFE source itself would not endorse. The result is a 35 MW driver feeding a claimed 1000 MWe net plant — roughly 20× lower than Pacific Fusion's own published design implies. Compounding this, the file's `cost_overrides` block declares "M$ (2024$)" but loads its two largest line items directly from the 2006 Z-IFE direct-capital decomposition without escalation, and applies those Z-IFE LTD-architecture FOAK estimates as if they were Pacific Fusion IMG-architecture FOAK estimates. The main-pulser cost ($372M) is also routed to the wrong CAS22 sub-account — placed in C220104 (laser preheat) instead of C220107 (electrical pulser), which the framework would otherwise auto-compute correctly from the corrected stored energy.

---

## Human reviewer score for agentic research: **FAIL**

The agentic synthesis pipeline produced a `model_setup.py` that models the wrong reference design (Sandia Z-IFE, terminated 2007) instead of the concept it is named after (Pacific Fusion's commercial MagLIF FPP). The error compounds in five independent ways: the wrong source is pinned, the architecture is scaled inconsistently (one chamber's driver for ten chambers' output), the driver wall-plug power is off by ~20×, the capital-cost overrides are 2006-dollar Z-IFE LTD figures applied as if they were 2024-dollar Pacific Fusion IMG figures, and the main-pulser cost is routed to the wrong CAS22 sub-account (C220104 laser preheat instead of C220107 electrical pulser). Pacific Fusion's own 2025 paper (already in this concept's iter-03 source pool) was not used despite being the obvious primary reference. See *Recommended corrective actions* for fixes.

---

## Glossary (for outside readers)

| Term | What it is |
|---|---|
| **MagLIF** | Magnetized Liner Inertial Fusion — a pulsed-power IFE approach where a cylindrical metal liner compresses pre-magnetized, pre-heated D-T fuel. |
| **Driver** | The pulsed-power system that delivers energy to the liner. Specified by stored energy (MJ) and wall-plug efficiency. |
| **Q_f** | Per-shot fusion gain — yield per shot divided by driver energy delivered to the target. Pacific Fusion targets > 7 commercially. |
| **Rep rate** | Shots per second of the pulsed-power system. Steady-state power output = yield × rep rate. |
| **AMPS** | Pacific Fusion's "Affordable, Manageable, Practical, Scalable" architecture, based on IMG (Impedance-Matched Marx Generator) pulser technology. |
| **Z-IFE** | Sandia's 2006 Z-Inertial Fusion Energy concept study (SAND2006-7148). A pre-Pacific-Fusion DOE-era LTD-driven MagLIF reactor study, program terminated 2007. |

---

## Finding 1 — Wrong primary source

The model pins to a 2006 Sandia Z-IFE concept study for every load-bearing physics parameter (driver energy, rep rate, wall-plug efficiency, thermal cycle, fixed charge rate), despite the fact that Pacific Fusion's own 2025 design publication is in the same concept's research pool ([iter-03/sources/arxiv-2504-10680/](../knowledge/concept_research/07-maglif/iter-03/sources/arxiv-2504-10680/)).

The Z-IFE study uses a different driver architecture (LTD — Linear Transformer Driver), a different chamber concept (frozen-FLiBe RTL), and was the basis for a DOE program that terminated in 2007. Pacific Fusion uses IMG-class drivers and a different commercial design path. The two are not the same plant.

The model's own docstrings *acknowledge* the deviation — e.g. at [model_setup.py:111](../exploration/concept_analysis/analyses/07-maglif/model_setup.py#L111):

> *"NOTE: 0.5 Hz is NOT the 1 Hz commercial target of Pacific Fusion (arxiv-2408-15206 §7.1); it is the optimized Z-IFE published data point, chosen for calibration purposes."*

— and at [:131](../exploration/concept_analysis/analyses/07-maglif/model_setup.py#L131):

> *"NOTE: IMG architecture claims ~90% wall-plug efficiency (analysis.md §Section 5; arxiv-2408-15206 §3.2)"*

— but then keep the Z-IFE values anyway. The Pacific Fusion design point is described and then discarded as a "calibration" choice.

---

## Finding 2 — `n_mod = 1` with a full-plant net-electric target (architecture scale mismatch)

The Z-IFE 2006 study's 1000 MWe plant is **explicitly a multi-chamber architecture**:

> *"the original Z-IFE power plant design of ten chambers… Three alternatives were suggested for reducing the amount of reaction chambers needed for a 1000 MWe power plant: 1) an increase in target yield, 2) an increase in repetitive rate, or 3) both."*
> *"each [chamber] producing ~100 MWe net power for a total plant power of ~1000 MWe"*
> — SAND2006-7148, §3.1

So Z-IFE 2006 produces 1000 MWe either with **10 chambers × 100 MWe each** (original design) or with fewer chambers at proportionally higher yield and/or rep rate.

Concept 07's `model_setup.py` sets `n_mod = 1` (one chamber) but targets `NET_ELECTRIC_MW = 1000.0` (the full ten-chamber plant). It pulls the **per-chamber** driver spec from Z-IFE §3.1.1.5 (42 MJ stored, 0.5 Hz, 60% wall-plug) and ties it to the **per-plant** electric output. No configuration in SAND2006-7148 supports 1000 MWe net from one chamber operating at those driver parameters.

To deliver 1000 MWe net from one chamber at Q_f = 7 and 0.5 Hz using Z-IFE's own methodology requires a driver storing roughly **1.3 GJ** per shot, not 42 MJ — about a 30× scale-up of the cited number. The model has truncated the chamber count from 10 → 1 without adjusting either the driver scale or the per-chamber output.

---

## Finding 3 — Driver power is an order of magnitude too low

The model declares `P_DRIVER_MW = 35.0` ([model_setup.py:121](../exploration/concept_analysis/analyses/07-maglif/model_setup.py#L121)) with the comment *"42 MJ stored × 0.5 Hz / 0.60 LTD efficiency ≈ 35 MW"*. Using the user's commercial scaling from Pacific Fusion's 2025 paper:

### Source excerpt (Pacific Fusion, [arXiv:2504.10680](https://arxiv.org/pdf/2504.10680))

> *"We then introduce our Demonstration System (DS), a pulsed-power driver designed to deliver more than 60 MA and store approximately **80 MJ** of energy. The DS is designed to achieve a 1000× increase in effective performance compared to the NIF, delivering approximately 100× greater facility-level energy gain — and importantly, achieving **net facility gain, or Q_f > 1** — at just 1/10 the capital cost."*

Commercial scaling per Pacific Fusion's stated targets in the same paper: **commercial yield ≈ 816 MJ per shot at Q_f > 7**.

### Reviewer's corrected driver calculation

For a single-chamber commercial Pacific Fusion FPP delivering ~1000 MWe net:

| Quantity | Value | Basis |
|---|---|---|
| Commercial yield per shot | 816 MJ | arXiv:2504.10680 (commercial point) |
| Q_f (fusion gain per shot) | 7 | arXiv:2504.10680 (commercial point) |
| Driver delivered per shot | 816 / 7 = **117 MJ** | by definition of Q_f |
| Commercial rep rate | 5 Hz | reviewer's commercial extrapolation |
| Wall-plug efficiency (IMG-class) | 0.80 | acknowledged in model_setup.py:131 |
| **Driver wall-plug power** | **117 × 5 ÷ 0.80 ≈ 730 MW** | |
| Fusion power | 816 × 5 = **4080 MW** | |
| Net electric (≈ 0.42 × 4080 − 730 − BOP) | **~1000 MWe** | self-consistent with declared target |

The model's 35 MW driver is **~20× lower** than this corrected value. Even using Pacific Fusion's *own* more conservative 1 Hz commercial target, the corrected driver is still ~150 MW — ~4× the model's value. There is no Pacific Fusion design point in which 35 MW wall-plug drives 1000 MWe net.

### Why the framework doesn't catch this

Inside costingfe, `p_input` (the driver wall-plug load) only feeds into the *recirculating power* calculation, not the *fusion power balance*. The framework takes `NET_ELECTRIC_MW = 1000` as a hard target and back-solves whatever P_fus is needed to balance the books — in this case ~2.7 GW of fusion, implying an absurd steady-state Q_sci ≈ 76. The 35 MW driver enters only as ~58 MW of parasitic recirc load on the gross output side. No part of the framework checks whether the declared driver can physically deliver the back-solved P_fus, so the inconsistency is silently absorbed into the cost calculation.

---

## Finding 4 — Cost overrides are 2006-dollar Z-IFE FOAK figures applied as 2024-dollar Pacific Fusion FOAK figures

The `cost_overrides` block at [model_setup.py:172](../exploration/concept_analysis/analyses/07-maglif/model_setup.py#L172) declares *"All overrides in M$ (2024$)."* The actual provenance per line:

| Override | Value | Source | Actual cost-basis year |
|---|---|---|---|
| CAS21 (buildings) | $200M | Independent 2024 footprint estimate (20,000 m² × $7,000/m²) | ✓ 2024$ |
| C220104 (driver) | **$372M** | Z-IFE LTD median, SAND2006-7148 §3.1.2 | ✗ **2006$**, unescalated |
| C220101 (FW + blanket) | **$50M** | Derived from Z-IFE §3.1.2 direct-capital split | ✗ **2006$**, unescalated |
| C220600 (RTL + target factory) | $120M | 50% of costingfe's `target_factory_base = $244M` | Inherited from framework default |
| C220103 / 108 / 109 | $0 | Physical "not applicable" — no SC magnets, no divertor, no DEC | n/a |

The two load-bearing 2006-dollar lines ($372M + $50M) account for ~60% of declared direct capital. Escalating 2006 → 2024 by US CPI (1.55×) or by the more appropriate industrial Chemical Engineering Plant Cost Index (CEPCI, 1.60–1.70×) brings the driver alone to ~$575–630M and the FW + blanket to ~$80–85M. So the file understates direct capital by roughly $230–290M purely from the missing escalation.

### Sub-issue: Z-IFE LTD FOAK ≠ Pacific Fusion IMG FOAK

Even granted the 2006 → 2024 escalation as a mechanical fix, the underlying figures describe the wrong machine. SAND2006-7148's costs are for a Linear Transformer Driver in a terminated 2006–2007 DOE program. Pacific Fusion's commercial design uses Impedance-Matched Marx Generator pulsers — a different architecture with different supply chain economics. The model author's own comment on C220104 acknowledges this directly ([model_setup.py:211-213](../exploration/concept_analysis/analyses/07-maglif/model_setup.py#L211-L213)):

> *"Modern IMG architecture (Pacific Fusion DS) may be 5–10× cheaper (analysis §S2 Challenge 3; arxiv-2408-15206 §3.2.4 'cost of energy storage and switching must decrease by a factor of 5 to 10'), but no published plant-scale estimate exists."*

So two distortions point in opposite directions:
- **Escalation gap (Sub-issue A):** 2006 → 2024 should bring the costs *up* by ~50–65%.
- **Architecture transition (Sub-issue B):** Pacific Fusion's own claim says IMG costs should be *80–90% below* the LTD reference.

The two errors approximately cancel, so the LTD-2006 figure happens to land somewhere near Pacific Fusion's claimed commercial IMG cost target by accident. That is a coincidence in error directions, not a defensible methodology. Without firm Pacific Fusion published cost data, the line should either be reconciled honestly (escalate **and** substitute IMG-class figures) or flagged as "no defensible current commercial estimate" with an explicit uncertainty band rather than a point value.

### Why the framework doesn't catch this

costingfe does not expose a `cost_basis_year` parameter and does not normalize historical-dollar values in user-supplied `cost_overrides`. The `inflation_rate` parameter escalates O&M forward from operation start but does not normalize the *historical* dollar year of capital cost inputs. So `cost_overrides = {"C220104": 372.0}` flows through as $372M in the framework's assumed current-dollar basis, silently, regardless of when the source figure was published. Every concept file in the corpus that pulls cost data from a pre-2024 source has the same exposure.

---

## Finding 5 — Cost overrides routed to the wrong CAS22 sub-accounts

CAS22 sub-accounts have specific scopes for pulsed concepts ([layers/cas22.py:193-215, 232-241](../../1costingfe/src/costingfe/layers/cas22.py)):

- **C220104 (Primary Driver, pulsed)** = laser preheat for MagLIF (per the framework: `driver_maglif_per_mw × p_driver`, comment: *"Laser preheat (Z-pinch electrical in C220107)"*)
- **C220107 (Power Supplies, pulsed)** = the IMG-class main pulser, auto-computed as `c_cap_allin_per_joule × e_stored_mj` where `e_stored_mj = e_driver_mj / eta_pin` (the natural $/J basis for capacitor-based pulsers, including caps + switches + charging + buswork)

Concept 07's `cost_overrides = {"C220104": 372.0, ...}` puts the Z-IFE LTD main-pulser cost into the **laser preheat account**, while C220107 — the account that actually exists for the IMG main pulser — is left to the framework's auto-computation against whatever stored energy is implied by the (already-wrong) declared driver parameters.

### Sub-issue: laser preheat itself should be zero for Pacific Fusion's commercial design

Pacific Fusion's [Feb 2026 breakthrough update](../knowledge/concept_research/07-maglif/iter-03/sources/pacificfusion-updates-experimental-breakthrough-by-pacific/output.md) reports an experimentally-validated composite-liner target that self-magnetizes without external coils, and states the next experimental campaign will eliminate laser preheat:

> *"In the MagLIF experiments, the targets are not only pre-magnetized but also pre-heated with a laser. Even though the pre-heating laser is not destroyed on each shot, it's an added complexity. **In the next iteration of experiments, we will aim to show that we can eliminate the need for laser pre-heating in addition to pre-magnetization.**"*
> — Pacific Fusion, *Experimental results by Pacific Fusion clears major obstacle to affordable commercial fusion* (Feb 5, 2026)

Since this review is scoring Pacific Fusion's **commercial** design point (mid-2030s), the consistent assumption is that C220104 (laser preheat) is **zero** under Pacific Fusion's stated commercial architecture — not the $372M Z-IFE LTD main-pulser cost that is currently there. Until laser preheat elimination is experimentally validated, this is an aspirational architectural assumption and should be documented as such in the file's comment block.

### What the corrected configuration looks like

The two-line fix:

```python
# C220104 = 0  per Pacific Fusion's commercial roadmap: self-magnetizing composite-
#             liner target (experimentally validated Oct 2025) eliminates external
#             magnetic coils, and the next experimental campaign targets elimination
#             of laser preheat entirely. Aspirational architecture, not yet
#             experimentally validated; revert to driver_maglif_per_mw * p_laser_mw
#             if laser preheat is retained in the commercial design.
# Source: pacificfusion-updates-experimental-breakthrough-by-pacific.md (Feb 2026)
"C220104": 0.0,

# C220107: do NOT override. Allow the framework to auto-compute
#          c_cap_allin_per_joule * e_stored_mj using the corrected commercial
#          driver parameters from Findings 2 and 3 (rep_rate = 5 Hz, eta_pin = 0.80,
#          E_driver_delivered ~= 117 MJ/shot for Q_f = 7 at 816 MJ commercial yield).
#          Resulting e_stored_mj ~= 145 MJ -> C220107 ~= $73M NOAK at $0.5/J basis.
# Source: arxiv-2504-10680 (Pacific Fusion 2025 commercial design point)
# (C220107 entry omitted from cost_overrides)
```

With Findings 2 and 3 also fixed (correct rep rate, correct wall-plug efficiency, correct driver energy delivered per shot), the framework's auto-computed C220107 lands at approximately **$73M NOAK** ($0.5/J × 145 MJ stored) for the commercial single-chamber IMG main pulser — replacing the $372M misrouted override. The $0.5/J NOAK constant in costingfe is accepted as-is for this review; deeper validation of the framework's pulser cost basis is out of scope.

---

## Recommended corrective actions

### Per-concept fixes (concept 07 specifically)

1. **Repin the primary source.** Move arXiv:2504.10680 from supporting evidence to the load-bearing reference. The Sandia Z-IFE 2006 study becomes a historical comparator at most.

2. **Choose one self-consistent (n_mod, P_driver, rep_rate, yield, P_net) tuple from the Pacific Fusion paper** and lock the whole model to it. Two viable choices:
   - **Single-chamber commercial point**: 1 chamber × 1000 MWe net → ~730 MW driver (per corrected calc above), 5 Hz, 117 MJ delivered per shot at Q_f = 7.
   - **Multi-chamber pilot point**: e.g. n_mod = 4 × 250 MWe each → ~180 MW driver per chamber, 5 Hz, with appropriate per-chamber yield.

   What is not viable: 1 chamber at 35 MW driver claiming 1000 MWe net.

3. **Remove the Z-IFE-derived efficiency stack** (eta_pin = 0.60 LTD, eta_th = 0.42 Z-IFE steel chamber). Substitute Pacific Fusion's stated values (IMG ~80–90% wall-plug; thermal cycle per Pacific Fusion's chamber design).

4. **Resolve the docstring-versus-code contradiction.** Two comments in the file already say the chosen parameters are wrong for Pacific Fusion. Either the comments are right and the values need to change, or the comments need to be updated to reflect a deliberate "we are modeling Z-IFE 2006, not Pacific Fusion" intent — but in that case the concept is misnamed and the LCOE should not be presented as Pacific Fusion's number.

5. **Rebuild the cost_overrides block from current-dollar Pacific Fusion sources.** The file currently mixes one genuine 2024-dollar line (CAS21) with two unescalated 2006 Z-IFE figures (C220104, C220101) and a costingfe-default-derived figure (C220600), while claiming uniform "M$ (2024$)" basis. Two acceptable resolutions:
   - **(a)** Drop the cost_overrides for C220104 and C220101 entirely and rely on costingfe's volume-based defaults until firm Pacific Fusion IMG cost figures are published. Mark the LCOE as "lower bound — driver and chamber costs not yet pinned to Pacific Fusion IMG basis."
   - **(b)** Apply 2006 → 2024 escalation to the Z-IFE figures (CPI 1.55× or CEPCI 1.65×), retain the ±50% uncertainty band already declared, and explicitly state in the comment block that these are LTD-class FOAK estimates serving as upper bounds, not Pacific Fusion IMG estimates. Either is honest; the current state is not.

6. **Set `C220104 = 0` with a citation block.** Per Finding 5, Pacific Fusion's commercial design point eliminates laser preheat (Feb 2026 breakthrough article). The comment block must cite `pacificfusion-updates-experimental-breakthrough-by-pacific.md` and label the assumption as aspirational-architecture (composite liner self-magnetization is experimentally validated; laser preheat elimination is the stated next-campaign target, not yet validated). This makes the assumption falsifiable and documents the fallback (`driver_maglif_per_mw × p_laser_mw` ~ $10–60M) if the elimination doesn't pan out.

7. **Remove the `C220107` override entirely** (it is not present today, but ensure no future edit adds one). With Findings 2 and 3 corrected — single chamber, 5 Hz rep rate, 80% IMG wall-plug efficiency, 117 MJ delivered per shot — the framework auto-computes `e_stored_mj ≈ 145 MJ` and `C220107 ≈ $73M NOAK` at the accepted $0.5/J basis. The framework's $/J pulser cost is the right architectural fit for IMG and is left as-is for this review.

### Process fixes (framework-level)

8. **Driver closure check.** A pulsed-concept analog of the "Q closure" check recommended for concept 11: verify that *declared driver delivered energy × rep_rate × Q_f ≥ required P_fus to close the framework's back-solved power balance to within ±25%*. A one-line invariant that would have caught the n_mod scale mismatch in this concept and likely similar issues in other pulsed concepts.

9. **Source-freshness check** (same as recommended for concept 11). Pacific Fusion's primary paper has been in iter-03 since arXiv submission (Apr 2025); the model_setup.py file still pins to a 2006 source. An automated check that the latest peer-reviewed primary source per concept is being used as the load-bearing reference would have flagged this.

10. **`cost_basis_year` parameter for costingfe.** Today the framework treats every entry in `cost_overrides` as same-year dollars by default. Add a `cost_basis_year` kwarg (and optionally per-override metadata) so historical-dollar entries are normalized forward to the framework's current-year basis via CPI or CEPCI. Same hygiene as `inflation_rate` provides forward-escalation for O&M, but applied backward for historical cost-basis normalization. This would close the entire class of "pre-2024 source figure used as 2024-dollar input" bugs across the corpus in one architectural change.

11. **CAS22 sub-account routing validation.** Today the framework will silently accept a `cost_overrides` value placed in the wrong sub-account (e.g. main-pulser cost in C220104 instead of C220107) and stack it on top of the auto-computed account at no cost. Add a validation step that warns when a sub-account override's magnitude is more than (say) 5× the framework's auto-computed value for the same account in the same architecture family — strong signal of misrouting. Would have caught the C220104 vs C220107 confusion in concept 07.

---

## What this review does not address

- The interest-rate-as-fixed-charge-rate methodology error ([validation_reviews/concept-11](11-realta-magnetic-mirror-comparison.md) sets a similar template; concept 07 also exhibits the FCR-vs-cost-of-debt confusion at the 9.66% value, but that is set aside per reviewer direction).
- The NOAK/FOAK *flag* choice (concept 07 is one of four NOAK=False concepts in the corpus). Note that Finding 4 *does* address whether the supplied FOAK cost estimates are appropriate for Pacific Fusion's FOAK plant — distinct concern from the flag value.
- The inflation rate value (0.0245 project convention).
- All other concept-07 cost-model parameters not directly tied to the driver / rep rate / yield chain or to the `cost_overrides` block.

These are real but set aside for this review.

---

## Provenance

This review was produced through a multi-turn analysis comparing concept 07's `model_setup.py` against the primary Pacific Fusion publication. All numbers reproducible from:

- `exploration/concept_analysis/analyses/07-maglif/model_setup.py` (model under review)
- `knowledge/concept_research/07-maglif/iter-02/sources/z-ife-sand2006-7148-thermal-cycles/output.md` (source the model is pinned to)
- `knowledge/concept_research/07-maglif/iter-03/sources/arxiv-2504-10680/output.md` (source that should be primary)
- arXiv:2504.10680 PDF (for the 816 MJ / Q_f > 7 commercial point — reviewer's reading of the full paper, not just the trafilatura-extracted abstract)
- `1costingfe` v8faf003 (cost framework, for the implicit Q_sci = 76 back-solve at the model's declared parameters)
