# Retroactive H2 Capture: The Hawker 2020 Derivation Chain

**What this is.** WI-016 tests H2: "AI agents can operate a research loop — collect key input data from first-class research and process it into effective model behaviors and structures." One such loop already ran, in March 2026, without being framed as an experiment: Hawker 2020 ("A simplified economic model for inertial fusion") → source extraction → 14 economic parameters → IFE SysML calc defs → SV-008 validation. This document reconstructs that chain from the surviving artifacts. It quotes the artifact trail; it does not re-narrate from memory.

**Written retroactively on 2026-07-04.** Frozen companions `derivation.md` and `process_log.md` in this directory are the separate blind-derivation experiment and are not referenced here.

---

## 1. What the source provided

**Source**: `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md` (972 lines, extracted 2026-02-27 by the agentic-mbse pipeline; checksum in `INDEX.md` in the same directory).

The paper is unusually well-suited to this loop because it *is already a parametric model*: 14 technology-agnostic parameters, a discounted-cash-flow LCOE formula (Eqs. 2.1–2.16), and a 10-million-sample Monte Carlo with Pearson sensitivity rankings. What the extraction delivered:

- **Table 2** (output.md ~line 155): the 14 parameter names, symbols, and units. The layout partially collapsed — units for dimensionless parameters vanished into dot-leader runs, and the header row carries `~~strikethrough~~` markers.
- **Table 3** (output.md ~line 442): the load-bearing table — ranges, linear/log sampling space, and Pearson correlation coefficients for all 14 parameters. This extracted cleanly (values legible despite strikethrough headers).
- **Default values** (output.md line 567): "the default values are: availability = 70%; ..." — prose, not a table. This is where the defaults in the model come from.
- **Equations 2.1–2.16**: partially garbled in text (Eq. 2.3's piecewise cost definition at output.md ~line 391 is scrambled across lines). Equation images exist in the `images/` companion directory (5 PNGs) per the project's image-inspection protocol.

**Extraction-quality issues, known at the time and still visible:**

- 12 `~~strikethrough~~` artifacts, all on table headers and figure labels. This is the documented upstream agentic-mbse OCR limitation (recorded in project auto-memory; same count in old and new extractions).
- `INDEX.md` section summaries all read "[Summary generation failed]".
- A severe extraction collapse at output.md line 761: the entire Figure 5 / minimum-cost-design-point discussion is crushed into one garbled table row. The key numbers ($24.6/MWh example configuration) are recoverable but interleaved.
- A **citation-numbering drift** that persisted downstream: the paper's parameter table is Table 2 and the sensitivity table is Table 3, but the WI-006 spec and the SysML doc comments cite "Table 1" throughout (e.g. `models/library/cost_structure/ife_cost_parameters.sysml:23` — "Ref: Table 1 (parameter definitions), Figure 3 (sensitivity)"). The references still resolve for a human (there is only one parameter table), but they are formally wrong.

Despite the garbling, every number that entered the model — 14 ranges, 14 defaults, 14 Pearson coefficients — checks out against the legible parts of Table 3 and line 567. The extraction was lossy in presentation but not in the data actually consumed.

## 2. How the workflow processed it, stage by stage

The chain ran through the modeling PM pipeline (research → insight approval → intent → spec → design → plan/implement) across three work items. Artifact trail:

### 2a. Research and insight capture (2026-03-02)

`knowledge/research/approved/20260302-165055_ife-system-modeling-first-pass.md` — a synthesis across 7 IFE sources, of which Hawker is one. It passed the research approval gate (the `pm approve-research` mechanism) and produced five domain insights, two of which carry the Hawker content:

- **DI-005** (`knowledge/KNOWLEDGE.md`): "Hawker identifies 14 technology-agnostic parameters sufficient to characterize IFE LCOE. Top sensitivities by Pearson correlation: discount rate (+0.247), plant cost (+0.210), target cost (+0.186)..."
- **DI-003**: target cost as a unique IFE operating cost, with Hawker's +0.186 correlation and the ~$10/target threshold.

### 2b. Framework selection (2026-03-02, human artifact)

`modeling_project/intent/IFE Modeling Target Selection.md` — the decision record: "Start with a generic, driver-agnostic IFE model built around Hawker's 14-parameter LCOE framework, then instantiate it with Heavy Ion Beam (HIF) parameters." The stated reasons: parameter completeness ("the model can be fully populated from day one"), CAS mapping, reusability, and "Validation target exists: Hawker's Monte Carlo results ($25–120/MWh range) provide a direct validation benchmark." This document set the epic structure WI-006 → WI-007 → WI-008.

### 2c. WI-006 — library definitions (`work/completed/20260302_WI-006_ife-cost-structure-library/`)

- **Spec** (`spec.md`, MR-WI006-1): transcribes the full 14-parameter table — symbol, units, range, default, Pearson r — with the citation block "Ref: Table 1 (parameter definitions), Figure 3 (sensitivity rankings)". MR-WI006-3 captures the LCOE formula requirement; MR-WI006-6 requires Source/Ref/Basis on every numeric literal.
- **Design** (`design.md`): the genuinely derivational step of the chain. Hawker gives LCOE as a year-by-year DCF sum (Eq. 2.1). SysML calc defs cannot loop. The design (DD-3) converts the sum to a closed form: "Since annual costs and energy are constant within each phase, the DCF sums reduce to geometric series with present value factors: `PVF_con = (1 − (1+d)^(−Yc)) / d` ... `LCOE = (C_cap·PVF_con + C_op·PVF_op) / (E·PVF_op)`." It also consolidates Hawker's power balance to `P_e = E_d × f × (μ_th × E_b × G × μ_d − 2)` (Eqs. 2.12–2.16 combined) and notes the factor of 2 is "Hawker's explicit approximation: recirculating power ≈ 2× driver power." The design was prototyped and syside-validated before the plan phase (Validation Report: "Files created: 6 ... Checks passed!").
- **Output**: `models/library/cost_structure/ife_cost_parameters.sysml` (14 attributes of type `Economic Parameter`, each with value/min/max/sensitivity and a per-attribute Hawker citation) and `models/library/analyses/ife_lcoe.sysml` (the closed-form calc def, 14 inputs + 2 constants, 13 named intermediates).

### 2d. WI-007 — generic plant assembly (`work/completed/20260302_WI-007_generic-ife-concept-model/`)

The design's "Parameter Binding Table" maps each Hawker parameter to a physical home — 4 on the abstract driver, 1 on the target factory, 2 on the chamber, 7 at plant level — and wires all 14 into the library LCOE calc via dot notation (`design.md`, "Cross-File Bindings"). Output: `models/designs/generic_ife/ife_plant.sysml`. The plan is a requirement-by-requirement checklist against the prototype; Phase 2 records the SV-008 evaluation (Section 4 below).

### 2e. WI-008 — HIF instantiation (`work/completed/20260303_WI-008_hif-concept-instantiation/`)

Hawker's role here is the receiving framework: HIF parameters from Osiris (EIF-1992), Meier 1986, and Bangerter 2013 are bound into the 14 slots. Two agent-side reconciliations stand out:

- **Unit-convention conflict (spec risk A2, resolved in design)**: "driver energy" means bank energy in Hawker but beam-on-target energy in EIF-1992/Meier. The design resolved this by cross-checking the Osiris table: "Yield/E_d = 412/5 ≈ 82 ≈ G (matches table). If E_d were bank: G would need to be yield/(eta·E_d) = 412/1.75 = 235 ≠ 80" (`design.md`, Research Findings). Conversion adopted: `E_d_bank = E_d_beam / eta` = 14.286 MJ.
- **The Meier→Hawker bridge (DD-WI008-2)**: Meier's engineering driver-cost formula returns gamma ($/J of bank energy) so it plugs directly into Hawker's parametric slot: "gamma = 0.975e9/14.286e6 = $68.25/J". Model files: `models/designs/hif_ife/hif_driver.sysml`, `hif_plant.sysml`.

## 3. Where human judgment intervened

The loop was gated, not free-running. Documented intervention points:

1. **Framework and concept selection** — `modeling_project/intent/IFE Modeling Target Selection.md` is a human decision record choosing Hawker's framework over driver-specific bottom-up modeling and HIF over laser/pulser. The agent's research informed it; the choice was the user's.
2. **Research approval gate** — insights only reached `KNOWLEDGE.md` (DI-001–005) through the `pm approve-research` step on `knowledge/research/approved/20260302-165055_ife-system-modeling-first-pass.md`.
3. **Design approval gates** — both WI-007 and WI-008 designs end with "Status: Pending user approval" (WI-007 `design.md` Approval section; WI-008 `design.md` line 476).
4. **Dual validation approach** — WI-008 spec MR-WI008-5 records "Derives from: Epic success criteria, **user-selected** dual validation approach" — the decision to compute both Hawker LCOE and Meier COE and validate each against its own published reference (rather than each other) was a user choice.
5. **Pre-close review** — WI-008 `plan.md` line 51: "User review: After Phase 2 (before closing), user reviews verification script output and VALIDATION_MATRIX updates."
6. **Scoping** — deferrals recorded in specs (CAS22 level-3 deferred from WI-006 to WI-007; Meier efficiency formula documented as reference, not modeled; inflation adjustment documented, not applied — WI-008 spec Out of Scope).

Not found: any record of a human correcting a wrong number in the agent's transcription. The corrections that appear in the trail (the $66 LCOE estimate revised to $270, the E_d convention) were agent self-corrections during design/verification.

## 4. What validation anchored it

### SV-008 mechanics

`modeling_project/VALIDATION_MATRIX.md` SV-008: "LCOE with realistic parameters within Hawker range | reasonableness | test | $25–120/MWh with HIF design point params | order of magnitude | `scripts/verify_ife_lcoe.py` | passing".

The script mirrors `models/library/analyses/ife_lcoe.sysml` line-for-line in Python (syside can't evaluate the full calc chain — the fallback anticipated in WI-007 `plan.md`, Feasibility Concerns). Two evaluations, re-run and confirmed on 2026-07-04:

- **Hawker defaults** (f=0.2 Hz, G=500, ...): **$252.30/MWh** — outside the $25–120 range. The script's own note: "Monte Carlo center values (esp. f=0.2 Hz, delta=$10) produce a 44 MW plant — too small for capital assumptions."
- **"HIF design point"** (f=5 Hz, eta=0.25, E_d=5 MJ bank, N_d=1e9, delta=$0.50, d=0.05, mu_a=0.85): **$68.69/MWh** at a 250 MW plant — inside the range. This is what SV-008 "passing" rests on.

Be clear about what happened here: the original acceptance criterion (WI-007 spec MR-WI007-7: "LCOE with **default** parameters within Hawker's $25–120/MWh range") **failed**, and the goalpost was moved — SV-008 was re-anchored to a hand-picked realistic design point, with the failure converted into a domain insight rather than a bug. WI-007 `plan.md` Phase 2: "Result: PASS with note — formula correct, center-of-range Monte Carlo defaults produce small plant; realistic design points give expected LCOE range." That re-anchoring is defensible (the formula is correct; LCOE genuinely is nonlinear and Hawker's own reported range comes from favorable Monte Carlo outcomes, not midpoints) — but it is a validation-criteria revision, and the matrix row's "realistic parameters" wording quietly encodes it.

### The DI-006 nonlinearity discovery

The failed default check became `knowledge/KNOWLEDGE.md` DI-006: center-of-range parameter defaults do not produce center-of-range LCOE; parametric sweeps should report distribution statistics, not midpoint evaluations. This is the loop producing a genuine, reusable analysis insight from a validation surprise — arguably the strongest H2 evidence in the chain, because nothing in the source paper states it in this form.

**However, DI-006's numbers are corrupted.** The registry entry reads "LCOE=52/MWh — far above the 5-120/MWh range ... Realistic HIF parameters (f=5Hz, eta=0.25) give 8.69/MWh." Every one of those figures has lost a leading "2": the script prints **$252.30**, the range is **$25–120**, and the design point gives **$68.69** (verified by re-running `uv run python scripts/verify_ife_lcoe.py` on 2026-07-04; the WI-007 plan.md records the same correct values). As written, DI-006 is internally incoherent (8.69 is *below* the quoted range, which would defeat the check's purpose). Note the WI-016 tasking for this document itself quoted "8.69 $/MWh" — the corruption has already propagated once. The correct anchor figure is **$68.69/MWh**.

### The Osiris footnote (SV-013)

SV-008's passing design point is *not* the WI-008 Osiris plant. The actual Osiris instantiation (f=3.5 Hz, delta=$10, gamma≈$68/J) gave **$270/MWh** — WI-008 `plan.md` line 171: "NOTE: exceeds Hawker's $25-120 range due to target cost dominance at 3.5 Hz ($213/MWh of $270/MWh from targets alone). Design doc estimate of ~$66/MWh was incorrect." It passes SV-013 only under the weaker "finite positive" tolerance. The engineering-side anchor held better: SV-014, Meier COE = 4.74 ¢/kWh vs. published 5.0 (5.3% off, within ±15%).

## 5. Honest H2 assessment of this chain

### What the loop did autonomously

- **Extraction and transcription under noise**: pulled 42 correct numbers (14 ranges, defaults, sensitivities) out of a partially garbled extraction, with per-value citations that survive to the SysML doc comments.
- **Real derivation, not copying**: the closed-form DCF conversion (WI-006 DD-3) restructured Hawker's iterative formula into something the modeling tool could express, with the mathematical-equivalence argument stated.
- **Cross-source reconciliation**: caught and resolved the bank-vs-beam energy convention conflict by checking which convention reproduces the published Osiris gain (WI-008 design, risk A2) — the kind of error that would have silently wrecked the LCOE by a factor of ~3.
- **Model bridging**: the Meier-gamma calc def connects an engineering cost model to a parametric one in a single traceable element.
- **Self-correction and insight generation**: the failed default check was diagnosed correctly (nonlinearity, small-plant capital dominance) and captured as DI-006; the design's own $66 Osiris estimate was caught as wrong by its verification script.

### Where it was steered

Every consequential *choice* was human: which framework (Hawker), which concept (HIF), the dual-validation approach, and approval gates at research, design, and close. The agent operated the loop; the human aimed it. The re-anchoring of SV-008 after the default-parameter failure also passed through the user-review gate rather than being a unilateral agent move.

### What this single data point establishes — and doesn't

**Establishes**: an agent workflow can carry data from a published paper through extraction, structured requirements, a derivation step, model implementation, and numeric validation, keeping an auditable citation chain the whole way — and can convert a validation failure into a correct domain insight. The chain is reconstructible three months later from artifacts alone, which is itself part of the claim.

**Doesn't establish**:

- **Generality.** Hawker 2020 was easy mode for "collect key input data": the paper *is* a 14-parameter model with its own sensitivity analysis. The loop mostly re-hosted an existing model rather than synthesizing one from raw physics or scattered engineering data. WI-016's blind-derivation experiment (the frozen `derivation.md` in this directory) exists precisely to test the harder version.
- **Validation rigor at the reasonableness tier.** SV-008 "passing" reflects a criterion revised after failure, at a hand-picked design point; the flagship concrete plant (Osiris) misses the range and passes only "finite positive." The baseline-tier checks (SV-012, SV-014 against Meier's published values) are the honest anchors here.
- **Reliability of the downstream record.** The DI-006 digit corruption (52/8.69/5-120 for 252/68.69/25-120) sat unnoticed in the curated knowledge registry for four months and has already propagated into at least one downstream tasking. The primary artifacts (plan.md, the script) were right; the distilled summary was wrong. For H2, that cuts both ways: the loop's ground truth is recoverable, but its compressed knowledge layer needs verification passes of its own.

**Net**: one clean demonstration that the loop *can* run, with the caveats that the source was unusually loop-friendly, the human steered every fork, and the weakest links were in the summary/registry layer rather than the model itself.

---

### File pointers (one place)

| Step | Artifact |
|---|---|
| Source extraction | `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/{output.md, INDEX.md, images/}` |
| Research synthesis | `knowledge/research/approved/20260302-165055_ife-system-modeling-first-pass.md` |
| Insights | `knowledge/KNOWLEDGE.md` (DI-003, DI-005, DI-006) |
| Framework decision | `modeling_project/intent/IFE Modeling Target Selection.md` |
| Library work item | `work/completed/20260302_WI-006_ife-cost-structure-library/{spec,design,plan}.md` |
| Generic plant work item | `work/completed/20260302_WI-007_generic-ife-concept-model/{spec,design,plan}.md` |
| HIF work item | `work/completed/20260303_WI-008_hif-concept-instantiation/{spec,design,plan}.md` |
| Parameters model | `models/library/cost_structure/ife_cost_parameters.sysml` |
| LCOE model | `models/library/analyses/ife_lcoe.sysml` |
| HIF models | `models/designs/hif_ife/{hif_driver,hif_plant}.sysml` |
| Verification | `scripts/verify_ife_lcoe.py`, `scripts/verify_hif_costs.py`, `modeling_project/VALIDATION_MATRIX.md` (SV-008, SV-012–014) |
