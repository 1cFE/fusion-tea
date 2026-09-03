# T-002 evidence — what the winding-pack stress fence should be a limit on

**Author:** the round agent, 2026-09-03. Owner ruled the cycle in session, scoped as "what is the right criterion", explicitly **not** "find a more permissive rule". Two seam runs, both `REGISTERED`. Clean room honored, with one refusal recorded in § 6.

**The short answer.** The model's single check — one computed winding-pack stress against one 800 MPa allowable — is the wrong *shape* of check, and no rule change opens the deadlock. The steel rule could defensibly be read looser than 800; the conductor stops you at almost exactly the same place. And two further limits, in directions the model does not represent at all, are far tighter.

## 1. The structural criteria have categories, and 800 MPa is not one of them

**Registered:** `knowledge/sources/coil_concepts_for_demo_and_next_step_reactors_5th_iaea_demo/` — Titus, 5th IAEA DEMO Programme Workshop, 2018 (PPPL). Verified in the extraction, not taken on a searcher's word:

- `output.md:75` — "Sm, Primary Membrane Allowable = 666 Mpa **Only based on yield** according to ITER MSDC"
- `output.md:99` — "the peak stresses in ITER are limited absolutely to **2.0Sm** … and in some cases (generally **where local plasticity may affect insulation bonding**) to **1.5Sm**"
- `output.md:468` — "Allowable TF Stress = **1GPa Peak, 666 PM**"

The governing document is the ITER Magnet Structural Design Criteria (ITER_D_2FMHHS). It is an ITER IDM document, **not publicly available** — recorded as a durable queued item in the REQ-036-02 return. Everything here reaches us second-hand through open sources, and that limitation is part of the finding.

ITER departs from ASME deliberately: because σu/σy falls to ~1.5 at cryogenic temperature, **only yield defines Sm**. So at 1000 MPa yield: **Pm = 666 MPa, Pm+Pb = 867 MPa, peak = 1000 MPa** in an insulation-bonded region, 1333 MPa otherwise.

**Which category is our operand?** It is anchored to the Stellaris Table 8 row titled *"Peak stress on WP"*, and Stellaris' own analysis resolves the radial plates and casing as separate contacting bodies rather than smearing them (raw PDF p. 24). On that reading our number is a **peak** quantity, and 800 MPa is *conservative* against a 1000 MPa peak allowable — not optimistic. The PPPL-5297 line quoted in T-001, which calls 800 MPa "optimistic", is about the **primary membrane** allowable. That is a different category, and comparing across the two was an error in T-001's reading, corrected here.

**This category identification is a reading, not a sourced statement**, and it carries the whole structural conclusion. It goes to the checkpoint reviewer as such.

## 2. But the conductor re-tightens it, at almost exactly the same place

**Registered:** `knowledge/sources/electro_mechanical_properties_of_rebco_coated_conductors/` — Barth, Mondonico & Senatore (2015), arXiv preprint of *SuST* 28 045011. This is the common authority behind **both** Stellaris' strain claim and MANTA's 700 MPa conductor limit. Verified verbatim in the extraction:

- `output.md:173` — at 4.2 K / 19 T, irreversible strain limits: Bruker 0.70–0.72%, SuNAM 0.67–0.69%, SuperPower 0.66–0.68%, Fujikura 0.55–0.57%, **SuperOx 0.45–0.47%**.
- `output.md:197` — "**Remaining below 0.4% strain, there are no discernible differences** in the samples' strain dependencies"; "the irreversible stress limits of all samples are in the **740–840 MPa** range"; "**Below 600 MPa, there are no differences** in the samples' strain dependencies of their critical currents."
- `output.md:167,173` — Fujikura and SuperOx tapes **fully de-laminate** during the measurements, splitting between the buffer stack and the REBCO layer, "indicating an interfacial weakness". Their transition to irreversibility is step-like, not gradual.

**Two things follow, and the second is uncomfortable.**

First, the demonstrably safe zone ends at **600 MPa / 0.4% strain**. Stellaris' reported winding-pack peak is "in the range of 600 MPa" and its reported HTS stack strain is below 0.2% — the design sits inside the safe zone, and its 800 MPa is a limit it does not approach.

Second, **SuperOx is the tape Stellaris specifies, and it is the weakest of the five measured** — lowest irreversible strain, and one of only two that delaminate outright in test. The margin the design relies on is the smallest in the surveyed field.

**Inference, flagged as inference and not sourced:** 316LN at 20 K has E ≈ 200 GPa, so 800 MPa corresponds to ≈ 0.40% strain. If the bonded tape stack strains with the pack, it arrives at ≈ 0.40% — just under SuperOx's 0.45% irreversible limit, about 12% margin, and at or above every limit practitioners actually enforce. Caveats that could move this by nearly a factor of two: von Mises is not uniaxial stress; a pack-level stress is not local tape stress; the soldered Cu jacket offloads the stack relative to the steel; and cooldown pre-compresses the tape by roughly −0.15%. **This is a hand calculation standing in for an FE result, and it is not a number to bind a constraint to.**

## 3. Two limits the model does not represent at all, in directions it cannot see

The conductor's mechanical limit is strongly anisotropic, and the weak direction is not close:

| direction | limit | source |
|---|---|---|
| Transverse **tension** (peel / delamination) | **3.6 MPa** measured under electromagnetic loading; 0.5 MPa (cleavage) to ~15 MPa (anvil) across methods | Lu et al. 2025, arXiv:2507.21301 — reported, **not registered** |
| Transverse **compression** | **~200 MPa** stated design limit on bare tape; 370–450 MPa for well-impregnated cable | **Registered:** `knowledge/sources/conceptual_design_of_hts_magnets_for_fusion_nuclear_science/` (Zhai, van der Laan, Connolly & Kessel, OSTI) |
| Axial tension | 740–840 MPa / 0.45–0.72% | Barth 2015, registered above |

Transverse tension is **two orders of magnitude** below the axial limit, and impregnation does not help it. A model checking one scalar against 800 MPa would pass a design that fails delamination by 200×, with nothing to indicate anything is wrong.

## 4. What comparable designs actually do — two checks, not one

Stellaris itself performs **two separate checks**: winding-pack von Mises against the 800 MPa steel limit, *and* HTS stack strain against a conductor limit (reported below 0.2%, citing Barth 2015 and Pierro 2019). Our model inherited only the first.

The same two-check pattern appears in the other open HTS designs surveyed — a stress check against the structure and a strain check against the conductor, with the structure deliberately sized so the conductor's strain criterion is met. One open study states the principle directly: HTS performance is driven by strain rather than stress, because the material is brittle.

## 5. The answer to the question that prompted this cycle

The owner asked whether a research cycle could find a better design rule. It could, and the answer is: **there is a looser reading of the steel rule, and it does not help.**

- Read as a peak-stress check, the steel allowable could defensibly be 1000 MPa rather than 800 — which at the current winding pack would let 9 of the 29 sustainment-satisfying points at p = 50 pass the stress fence instead of 0.
- But the conductor's own axial limit arrives at essentially the same place: the safe-zone boundary the measurements support is 600 MPa / 0.4% strain, and SuperOx's irreversible strain is 0.45%.
- And in transverse tension the governing limit is ~200× lower than anything currently modelled.

So the honest position is that **800 MPa is roughly the right magnitude for the wrong reason**. It is loose as a membrane allowable, conservative as a peak allowable, and coincidentally near the conductor's axial limit — which is the one that actually governs. It should not be relaxed to open a feasible region, and this task recommends it is not changed in this round at all.

**What should change is the shape of the check, not the number.** The sourced, no-FEA-required move is a second constraint on conductor strain at 0.2–0.4%, with the transverse limits recorded as a **named gap** rather than given a value. Whether that lands in this round's increment is the next task's scope decision, not this one's.

## 6. Clean-room event — a refusal, and a disclosure

**The hold-out guard refused a source.** `scripts/source_registry.py` declined arXiv:2409.01925 (a stellarator REBCO coil strain-optimization study) with `term:aries-cs matched 4x`. Nothing was written; the refusal is recorded durably in the REQ-036-03 `return.json` `queued[]` with its reason.

**Disclosure, surfaced rather than absorbed:** that paper's content — closed-form torsion and hard-way-bending strain expressions, and the 0.2%/0.4% critical-strain limits with their project attributions — was fetched by the research subagent and reached this session's context **before** the guard ran, because the guard runs at registration and the search runs before it. It is **not registered, not cited in any model artifact, and none of its numbers are used** in this evidence file's conclusions or anywhere else. The 0.2–0.4% strain range stated in § 5 rests on Barth 2015 and on Stellaris' own reported limit, both registered and independently verified, not on the refused source.

`PROTOCOL.md` §3 holds that bibliographic mentions of ARIES-CS do not taint an otherwise clean source, so the four matches may well be citations rather than data — but that is the **owner's** call through the §6 documented-exception path, not the round agent's, and the guard's refusal stands until then. Recorded here so the decision is visible rather than implicit.

**Also queued, and worth an operator fetch:** Pierro et al., IEEE TAS 29 (2019) — paywalled. It is the only identified source measuring irreversible strain *through* 20 K (4.2–40 K at 15 T), and one of the two authorities Stellaris cites. Every strain limit above is bracketed by 4.2 K and 77 K measurements rather than measured at the 20 K operating point.
