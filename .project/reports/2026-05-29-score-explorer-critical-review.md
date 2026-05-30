# Critical Review of Score Explorer Outcomes

**Date**: 2026-05-29
**Scope**: 39 concepts in `tools/score_explorer/data/concepts.json`, scored under
`exploration/scoring_v2/` with the equal-weight default profile.
**Author**: Critical TEA review (devil's advocate stance, claims grounded in
the diagnostics and `weights/default.yaml` lookup tables).

---

## TL;DR — The headline finding

The composite ranking is upside-down. **The seven concepts at the top of the
table (DPF, Pale Blue mirror, ENN p-B11, Helion, TAE, hb11, Marvel)
share a structural feature: their *physics* score (Technical Feasibility) is
1.0 or 2.0 — the lowest tier the framework can produce — and they ride to the
top on five or six "no-problem-because-nothing-is-built" axes.** The two
concepts with the strongest demonstrated physics (NIF-class indirect drive,
TF=5.0; CFS/Tokamak-Energy/Energy-Singularity/Firefly NT-tokamak, TF=4.0) are
ranked 10th, 18th, 19th, 20th, and 14th respectively.

The pipeline is, in effect, **penalizing concepts for having engineered an
answer to a hard problem, and rewarding concepts for not yet having one.**
This is the central pathology and almost every individual flag below is a
specific instance of it.

---

## Section 1 — Ranked list of most dubious outcomes

Each entry quotes the ranks/scores from `concepts.json` and traces the
discrepancy back to a specific lookup, missing trigger, or category error in
`weights/default.yaml`.

### #1 most dubious — LPP Fusion Dense Plasma Focus ranked #1 overall (composite 3.74)

- Scores: CF 4.5, TF **1.0**, Mod 3.67, PC **5.0**, SC **5.0**, Cust **5.0**, DA 2.0.
- DPF achieved triple product is `1e16` vs required `1.4e25` for pulsed p-B11
  — a **9-order-of-magnitude gap** (`log10_gap = 9.146`). The framework
  correctly floors TF at 1.0. Every other axis then gives this concept a
  perfect or near-perfect score, producing a composite that beats every
  tokamak in the corpus.
- **Root causes**:
  - Plant complexity = 5.0 because `subsystems_triggered = {}`. The
    `pulsed_power_thermal` trigger only fires for MIF, Z-pinch, and DPF
    families that have a thermal-capture blanket; here `blanket_config = N/A`
    and `energy_capture = Direct (charged particle)`, so the trigger is
    bypassed. A multi-MA capacitor bank with rep-rated electrode replacement
    is not a zero-complexity plant.
  - Supply chain = 5.0 because no Be/Li-6/T/V/He3/KDP/flibe is triggered.
    Electrode erosion (W/Cu/Be alloys), the capacitor-bank fleet (BaTiO3,
    polypropylene metallized film), and switching (spark gaps, thyratrons)
    are not in the bottleneck list.
  - Customization = 5.0 because `energy_capture = Direct (charged particle)`
    scores 4 and `fuel = p-B11` scores 4. Direct charged-particle capture
    from a DPF has never been demonstrated; the score rewards the *claim*.
- **Verdict**: This is the canonical example of the pathology. A concept
  9 orders of magnitude below ignition outranks NIF, CFS, and Tokamak Energy.

### #2 — Pale Blue centrifugal mirror p-B11 ranked #2 (composite 3.63)

- Scores: CF **5.0**, TF **1.0**, Mod 3.92, PC 4.5, SC **5.0**, Cust **5.0**, DA 1.0.
- TF diagnostic: `log10_gap = 6.7` (mirrors achieved 1e18 vs required 5e24
  for steady-state MFE p-B11 with alpha channeling). Floor.
- DA = 1.0 (13 blocking markers — worst-documented concept in the corpus).
- **Root cause**: the upper-CF axis fires zero penalties for a steady-state
  p-B11 mirror (no neutronic_fuel, no pulsed, no non-renewable blanket), so
  upper_cf = 5.0. The framework is not asking "*can* this concept run
  steady-state?" — it's asking "*does the concept claim* steady-state?"
  Pale Blue's steady-state operation is contingent on alpha channeling at
  fusion conditions, which has not been demonstrated. The 5.0 upper_cf is a
  free pass for an unproven physics regime.
- **Verdict**: When the worst-documented concept (DA=1.0, 13 blockers) is
  also the second-highest-ranked, something has gone wrong. The
  data-availability signal is structurally too weak to counterbalance the
  "absence of problems" gift on the other axes.

### #3 — ENN p-B11 spherical tokamak ranked #3 (composite 3.60)

- Scores: CF 5.0, TF **2.0**, Mod 3.67, PC 2.5, SC 5.0, Cust 5.0, DA 2.0.
- TF = 2.0 because the lookup uses `MFE|Spherical tokamak = 1.5e21`. That
  number is the **JT-60U/JET D-T-equivalent projected triple product** ported
  to the ST family. ENN's actual EXL-50U / EHL-2 record is not near 1.5e21.
- **Root cause**: TF inherits the achievement of the *best machine in the
  family*, not the concept itself. ENN, Tokamak Energy, CFS, Energy
  Singularity, and Firefly all share `achieved_triple_product = 1.5e21`
  regardless of their own demonstrated performance. ENN additionally gets the
  family-wide gap computed against the p-B11 MFE requirement (5e24) with
  alpha channeling assumed realistic. Pin a p-B11 cross-section onto a
  D-T-tokamak triple-product and the gap math comes out flattering.
- **Verdict**: ENN is rated higher than CFS not because ENN has better
  physics evidence, but because p-B11 fuel zeroes out two penalty axes
  (supply_chain, customization).

### #4 — Helion FRC w/ direct conversion (D-He3) at #4 (composite 3.55)

- Scores: CF 4.5, TF **2.0**, Mod **5.0**, PC **5.0**, SC 2.0, Cust 4.33, DA 2.0.
- **Root causes**:
  - Modularity = 5.0 from `MIF|FRC compression` MVS lookup of 5,
    `unit_count = 40` (presumably stated by Helion), and `magnet_driver`
    pulsed/pneumatic class. The MVS lookup gives every MIF concept a 5
    regardless of demonstrated single-pulse repeatability.
  - Plant complexity = 5.0 with `subsystems_triggered = {}`. A 1 Hz pulsed
    FRC merging at 0.1 GJ/pulse with switched 10+ MA capacitor banks has
    every "pulsed_power_thermal" hallmark, but the trigger requires a
    *thermal* capture, and Helion uses inductive direct conversion — so the
    trigger does not fire and the concept gets a perfect plant complexity.
- **Verdict**: The trigger logic conflates "thermal capture" with "complex
  plant". Helion has the most exotic pulsed-power architecture in the corpus
  and scores 5.0 on plant complexity because it bypassed the steam cycle.

### #5 — TAE p-B11 FRC at #5 (composite 3.48) with TF = 1.0

- TF correctly floors at 1.0 (FRC achieved 1e19 vs required 5e24, gap 5×10^5).
- All other axes pass: Cust 3.67, SC 5.0, PC 4.0, CF 5.0, Mod 3.67.
- **Verdict**: TAE has spent ≈$1.4B and after 25 years has not reached the
  ion temperatures required for p-B11 by 2+ orders of magnitude. A composite
  of 3.48 is generous; the framework has no mechanism for "concept has been
  attempted at scale and the gap has not closed."

### #6 — Marvel Fusion nanostructured-target ICF at #7 (composite 3.31)

- Scores: TF **1.0**, PC 2.5, SC 4.5, Cust 4.33, Mod 4.33, CF 4.5, DA 2.0.
- TF lookup: `IFE|Laser ICF (ultrashort pulse) = 1e18`. Marvel has no
  peer-reviewed measurement of compression or yield from
  nanostructured-target ultrashort pulse fusion. Inheriting the hb11 /
  HHEX-class triple-product is a categorical error.
- **Verdict**: Same pathology as ENN — concept inherits the achievement of
  the closest peer architecture even when its own demonstrated performance is
  nil. p-B11 + hybrid capture floats the rest of the axes.

### #7 — Sonofusion (acoustic ICF) at #8 (composite 3.21)

- TF = 1.0 (`no_data_floor = True` — Acoustic ICF has no peer-reviewed
  measurement). All other axes neutral-to-positive: Mod 4.67, PC 4.0, SC
  5.0, CF 3.5, Cust 2.33.
- **Verdict**: The composite of 3.21 is **higher than every steady-state
  HTS tokamak in the corpus**. A concept that lacks peer-reviewed evidence of
  fusion events outranks Commonwealth Fusion Systems. The 4.67 modularity
  score (from `IFE|Acoustic` MVS = 5) is the most indefensible single number
  in the table.

### #8 — NIF-class indirect drive (Inertia Enterprises) only ranked #10 (composite 3.02)

- TF **5.0** — the only concept in the corpus with the maximum physics
  score, justified by NIF's 2022/2024 ignition shots (gap = 0.6 — already
  below required).
- The composite is pulled down by SC 1.5 (tritium + Li-6 + V + KDP), PC 1.0
  (5 critical subsystems), Cust 1.67 (D-T + thermal).
- **The dubious thing here is the *ranking*, not the diagnostics.** The 7-
  axis equal weighting means that the *one* axis where physics has
  irrefutably been demonstrated is exactly counterweighted by six axes that
  reward "we don't have those problems because we haven't built it yet."
- **Verdict**: An equal-weighted composite that puts the only physics-validated
  concept behind nine speculative ones is a sensitivity-test failure of the
  weighting model itself. This is the single strongest argument for
  re-weighting (Physics-first preset should be the default, not a slider).

### #9 — Identical rankings for CFS, Energy Singularity, Tokamak Energy (composite ≈ 2.77 each)

- All three: TF=4.0, CF=4.0 (CFS 3.5), Mod≈3.7, PC=1.0, SC=2.0 (CFS 1.5), Cust=1.67, DA≈3-4.
- **Root cause**: The TF lookup gives all four tokamak shape variants
  (Tokamak, Compact tokamak, Spherical tokamak, Negative-triangularity
  tokamak) the *same* `1.5e21` achievement. So three radically different
  engineering programs — REBCO 20T compact (CFS), REBCO 25T compact (ESi),
  REBCO 5.25T ST (Tokamak Energy) — receive identical TF scores.
- The modularity, plant_complexity, and supply_chain axes also produce near-
  identical numbers (PC=1.0, SC=2.0) because the trigger set is dominated by
  *fuel choice* (D-T) and *family-shared subsystems* (tritium plant, remote
  maintenance, current drive, etc.).
- **Verdict**: The framework has no resolving power between near-peer
  tokamak concepts. From the pipeline's perspective, the difference between
  a 20 T REBCO compact tokamak and a 5.25 T spherical tokamak is rounding
  error. That is empirically wrong.

### #10 — NearStar MTIF (D-D, railgun) at #9 (composite 3.05) outranks NIF (#10)

- TF=1.0, PC 2.5, SC **5.0** (no Be/Li-6/T because D-D), Mod **5.0**,
  Cust 2.33.
- **Root cause**: D-D fuel gets zero supply-chain penalty even though the
  D-D branch produces 50% n + 3He at 2.45 MeV — the plant still needs a
  neutron-handling structure, just no breeder. The bottleneck list is
  fuel-vector–driven (tritium, Li-6) and does not model
  shielding/activation/vessel-replacement for high-n D-D plants. Modularity
  5.0 from `MIF|Pneumatic compression MVS=5` despite NearStar's railgun
  driver being an unproven plasma-armature variant.
- **Verdict**: A multi-km/s plasma-armature railgun firing into magnetized
  D-D targets is not a more modular industrial product than NIF; the lookup
  table says otherwise.

### #11 — Zephyr orbital levitated dipole at #15 (composite 2.81) ties Cortex liquid-jet ICF and outranks CFS

- TF=1.0 floor (`MFE|Levitated dipole (orbital) = 1e17`, gap 5×10^5).
- All upper_cf penalties bypassed (`{}`) → CF=5.0. D-He3 + direct
  conversion → Cust 4.33. He3 bottleneck → SC=2.0. PC 3.5.
- **Verdict**: An orbital fusion reactor on Falcon 9 outranking the most
  funded private fusion company is the kind of outcome that destroys the
  credibility of any composite. The framework has no penalty for "concept
  requires deployment in vacuum on a rocket".

### #12 — Firefly NTT (composite 2.88, TF=4.0) ranks #14, behind Polomac (Deutelio, composite 2.96)

- Polomac: TF=**1.0**, Cust 2.33, PC 3.5, SC 5.0, CF 4.0, Mod 2.92.
- Polomac is a magnetically-confined D-D resistive-dipole concept with
  "Unknown" primary heating and a one-line architectural description; it has
  never been built. Firefly NTT is a HTS negative-triangularity tokamak with
  a stated triple-product baseline 0.5 dex below ignition.
- **Root cause of inversion**: D-D fuel zeros the supply chain (5.0 vs 2.0)
  and customization is buoyed by no-tritium credit. Plant complexity 3.5
  (only `remote_maintenance` and `levitation_stabilization`) ignores that
  the resistive coil burns multi-GW of recirculating power.
- **Verdict**: When "I have nothing built" beats "I have a clear physics
  baseline 0.5 dex below ignition" in your composite, the composite is broken.

### #13 — Polywell (EMC2) ranked above Zap Energy SFS Z-pinch (composite 2.50 vs 2.48)

- Polywell: TF=1.0 (no measurement, floor), Mod 4.33 (`Non-Standard|IEC` MVS=5).
- Zap: TF=2.0 (achieved 1e17, gap 30,000), Mod 4.17.
- **Root cause**: Modularity lookup gives IEC a 5 by default; SFS Z-pinch
  gets `MFE|Z-pinch` MVS=4. Zap then loses on customization (D-T + thermal)
  vs Polywell (D-T + thermal — also 1.67 — so no difference) and pulls slight
  PC advantage but takes a SC hit the same as Polywell.
- **Verdict**: A concept with no peer-reviewed fusion measurement (Polywell)
  outranks one that has achieved 1e17 keV·s/m³ (Zap). The driver is a
  3-vs-4 difference in the MVS lookup table — i.e., a hand-coded prior.

### #14 — Identical "structural" tier for 7+ stellarators (composite 2.52–2.80)

- Gauss Fusion: 2.80, Proxima: 2.76, Thea: 2.66, Type One: 2.60, Helical: 2.60,
  Renaissance: 2.52. All TF=3.0, all upper_cf 3.5–4.0, all SC 2.0, all
  PC 1.0–2.0, all Cust 1.67.
- The only meaningful spread (2.52 → 2.80) is from DA (1 → 5 blocking
  markers in the gap report).
- **Verdict**: The composite cannot distinguish a HHF-class continuous-coil
  REBCO stellarator (Helical Fusion) from a laser-patterned 2D-HTS film
  stellarator (Renaissance) — the architectural choice is invisible to 6 of
  the 7 axes. Either the axes are too coarse, or there is a missing axis
  ("magnet manufacturability" / "coil topology complexity") that would
  distinguish these.

### #15 — SHINE Technologies particle accelerator (composite 2.89) is scored as a power plant

- SHINE is a beam-on-target neutron source for isotope production, not a
  fusion power plant. `blanket_config = N/A (non-power)`, `energy_capture = N/A`.
- Yet it receives composite 2.89, outranking 30 fusion-power concepts.
- **Root cause**: The framework treats it as a fusion concept because it
  produces fusion events. No axis filters "is this even attempting to make
  electricity?". Customization rescue (1.67) is the only signal it gets, and
  the composite weighted-mean still floats to ~2.9.
- **Verdict**: This concept should be either removed from the corpus or
  flagged with a `composite = N/A` for not having a power-plant intent.

---

## Section 2 — Methodological root causes (the issues that drive the
ranking inversions)

These are extracted from the per-concept evidence above, but they are
generic to the framework — fixing them would re-shuffle most of the table.

### M1. "Absence of subsystem trigger" → maximum complexity score

The plant complexity axis penalizes named subsystems. Concepts whose
architecture isn't represented in the trigger taxonomy bank the maximum
score (5.0). DPF, sonofusion, Helion FRC compression, Pale Blue mirror, and
ENN p-B11 are the standout beneficiaries. **The default for an
under-specified concept should be a *low* score (high complexity uncertainty
→ penalty), not a high one.** The current default rewards opacity.

### M2. Family-level triple-product inheritance

The TF lookup is keyed on `MFE|Tokamak` or `IFE|Laser ICF (direct drive)`
etc. — i.e., it grants the family's best demonstrated achievement to every
concept that shares the topology. CFS, ESi, Tokamak Energy, Firefly NTT all
get 1.5e21 even though only DIII-D / JET / JT-60U have measured anything
comparable. Marvel Fusion gets the hb11 baseline; ENN gets the JET-class
spherical-tokamak baseline. **TF should be concept-specific where the
concept has its own measurement, and floor where it doesn't** — currently
the framework charitably uses the family record as the baseline for
unbuilt concepts.

### M3. Fuel-driven supply-chain monoculture

Supply-chain bottlenecks are almost entirely fuel-driven: D-T triggers Li-6
+ T + (Be|V), D-He3 triggers He-3, p-B11 and D-D trigger nothing. This
collapses the axis into a 3-tier fuel proxy and gives p-B11 / D-D concepts a
1.5–3.0 point composite advantage that has nothing to do with their
demonstrated supply-chain robustness. **The axis does not represent
electrode materials, capacitor banks, REBCO tape, KDP optics for non-laser
concepts, gyrotrons, NBI, or shielding alloys** — most of which are real
bottlenecks for the speculative-fuel concepts that currently dominate the
ranking.

### M4. Customization is a 2-feature lookup that double-counts fuel

The customization axis is the average of (a) energy-capture method and
(b) fuel. Both correlate strongly with the *family*: direct conversion is
only viable for p-B11 / D-He3 / aneutronic-leaning concepts, which means
fuel is implicitly counted twice. The axis adds little independent signal
and produces a 1.67–5.0 spread that is almost perfectly rank-ordered by
fuel choice.

### M5. Modularity MVS lookup is a hand-coded prior, not a derived score

The `mvs_lookup` table assigns 3–5 to every concept based on confinement
family + topology. FRC = 4, IEC = 5, MagLIF = 5, Pneumatic compression = 5,
Acoustic = 5, Compact tokamak = 3. These priors are 50% of the modularity
score and they have no diagnostic provenance — they are author judgments
inserted as a "calibration target". The downstream effect is that Helion,
Sonofusion, NearStar, General Fusion, and EMC2 all bank modularity = 4.3–5.0
regardless of demonstrated mass-manufacturability.

### M6. Skip-and-rescale composite hides axis gaps as if they were strengths

When an axis is null (e.g., DA missing for a concept), the framework
renormalizes the remaining weights instead of imputing a penalty. This means
concepts with sparse data quietly drop axes from their composite. The DA axis
itself partially compensates (blocking-marker count), but only partially —
and the DA score-bracket (0 blockers → 5.0, 1–2 → 4.0, etc.) is graded too
generously to distinguish "well-documented" from "trivially-shallow".

### M7. Upper-CF axis ignores physics conditionality

Upper-CF rewards a concept for *being designed* steady-state, not for being
*able* to run steady-state. Pale Blue (5.0), ENN (5.0), Zephyr orbital
dipole (5.0), and TAE (5.0) all get the maximum because they claim
steady-state or quasi-steady operation in their docs. This is the *intent*,
not the *achievable*. NIF (3.5) is penalized for being pulsed even though
pulsed ICF has actually achieved ignition.

### M8. No axis represents financial / programmatic risk

The seven axes are physics + engineering + supply chain — there is no
"programmatic-credibility" axis (years in development, dollars raised, peer
review, government partnership, ARPA-E funding, milestone achievement
track record). If such an axis existed, it would re-order the table
dramatically: CFS, Helion, TAE, Tokamak Energy, Type One, NIF-inheritors
would move up; LPP, Sonofusion, Polywell, Polomac, Zephyr would move down.
The absence of this axis is the single biggest reason the pipeline
inverts the conventional ranking.

---

## Section 3 — Per-concept commentary (39 concepts)

Concepts are listed in current composite rank order. Each entry: composite,
the **single most dubious score** for that concept (with justification), and
where applicable, the **single most under-rated score**. Concepts already
discussed at length in Section 1 are summarized briefly here.

| # | Concept (company) | Composite | Most dubious score | Why |
|---|---|---|---|---|
| 1 | 24 DPF (LPPFusion) | 3.74 | PC=5.0, SC=5.0, Cust=5.0 | See §1 #1. Trigger-set bypass + lookup gifts. |
| 2 | 06 Mirror p-B11 (Pale Blue) | 3.63 | CF=5.0 with DA=1.0 | §1 #2. Steady-state alpha channeling treated as fact. |
| 3 | 39 ENN p-B11 ST | 3.60 | TF=2.0 (family inheritance) | §1 #3. Spherical-tokamak record ported to p-B11 baseline. |
| 4 | 08 Helion FRC D-He3 | 3.55 | PC=5.0, Mod=5.0 | §1 #4. Pulsed-power complexity invisible to trigger. |
| 5 | 18 TAE p-B11 FRC | 3.48 | CF=5.0 with TF=1.0 | §1 #5. 25 years, $1.4B, no temperature traction; SC=5.0 + CF=5.0 = composite 3.48. |
| 6 | 04 hb11 laser ICF p-B11 | 3.43 | TF=1.0 with composite 3.43 | TF=1.0 from `IFE|Laser ICF (fast ignition) = 1e20` vs req 1.4e25 for p-B11. Cust=3.67 + Mod=4.33 + SC=4.5 carry the composite. Same pathology as Marvel. |
| 7 | 23 Marvel nanostructured | 3.31 | TF baseline inheritance | §1 #6. No peer-reviewed yield from nanostructured-target. |
| 8 | 02 Sonofusion | 3.21 | Mod=4.67 with TF=1.0 floor | §1 #7. `IFE|Acoustic` MVS=5 is the most indefensible single value. |
| 9 | 37 NearStar MTIF (D-D, railgun) | 3.05 | SC=5.0, Mod=5.0 | §1 #10. D-D treated as supply-chain-clean despite high-neutron environment; railgun-driven Mod=5.0 is unsupported. |
| 10 | 26 NIF indirect drive (Inertia Ent.) | 3.02 | Composite ranking, not any single axis | §1 #8. Only TF=5.0 in the corpus; punished by D-T supply chain. |
| 11 | 35 Polomac (Deutelio) | 2.96 | CF=4.0 with primary_heating="Unknown" | §1 #12. Architectural description = one line; no heating spec; rated above NTT and CFS. |
| 12 | 31 BLF DPSSL direct drive | 2.92 | TF=4.75 then 1.0 PC | TF inherits NIF indirect-drive achievement via `Laser ICF (direct drive)` lookup (5e21 — assumes OMEGA-class transfer to DPSSL). Plant complexity 1.0 driven by every D-T penalty firing. |
| 13 | 38 SHINE accelerator | 2.89 | Whole composite | §1 #15. Not a power plant; should be excluded. |
| 14 | 29 Firefly NTT | 2.88 | TF=4.0 family inheritance | §1 #12. NTT-shape physics ≠ DIII-D NT triple-product. Bottoms out at PC=1.0 anyway. |
| 15= | 03 Cortex liquid-jet ICF | 2.81 | TF=1.0 (no-data floor), Mod=4.33 | `IFE|Laser (liquid jet)` MVS=4 is a prior; femtosecond plasmonic targets are unproven. |
| 15= | 19 Zephyr orbital dipole | 2.81 | CF=5.0, Cust=4.33 | §1 #11. Orbital deployment has no penalty axis. |
| 17 | 10 Gauss large stellarator | 2.80 | DA=5.0 (0 blockers) | DA bracket is too generous — "0 blockers" likely means the gap report was thorough, not that data is complete. |
| 18= | 01 CFS HTS compact tokamak | 2.77 | Composite rank vs LPP+Pale Blue | §1 #9. Most-funded private fusion company at #18. |
| 18= | 28 Energy Singularity (REBCO 25T) | 2.77 | Identical to CFS — no resolution | §1 #9. 25T vs 20T magnet is invisible to the framework. |
| 18= | 21 Tokamak Energy ST (5.25T) | 2.77 | Identical to CFS — different physics | §1 #9. ST vs compact = same score. |
| 21 | 09 Proxima QI stellarator | 2.76 | TF=3.0 from `QI stellarator = 1e20` | W7-X record ported to a TBD QI machine. |
| 22 | 07 Pacific MagLIF | 2.73 | Mod=4.92, PC=1.0 | Mod=4.92 from `MIF|MagLIF` MVS=5 + N=40 unit count is generous for a Z-machine-class architecture. |
| 23 | 32 GenF DPSSL direct drive | 2.69 | TF=4.75 inheritance | Like BLF — inherits NIF/OMEGA hybrid baseline despite being French-national-program early-stage. |
| 24 | 05 Thea planar-coil stellarator | 2.66 | TF=3.0 family inheritance | 324 shaping coils is a manufacturability problem the axes don't see. |
| 25= | 11 Realta mirror D-T | 2.63 | TF=2.0 → 4.0 jump from family | Mirror achieved 1e18; required 3e21 for D-T mirror. Bucket 2.0 is defensible but inherits mainstream-mirror physics. |
| 26= | 20a Type One stellarator | 2.60 | TF=3.0 + solid-breeder CF penalty | Solid breeder triggers non_renewable_blanket, dropping CF to 3.5; Helical Fusion (liquid metal) gets 4.0 — a 0.5 difference solely on blanket choice. |
| 26= | 36 Helical Fusion (HHF) | 2.60 | Mod=2.02 | Helical Fusion gets the *worst* modularity of any stellarator because continuous-helical-coil MVS=2 and vessel=2. Yet HF's WISE-conductor demountable design is arguably more manufacturable than Type One's modular non-planar coils. The lookup hard-codes a prior that contradicts the engineering. |
| 28 | 14 General Fusion (MTF pneumatic) | 2.58 | PC=1.0 | A 200-piston pneumatic compression rig + liquid-metal vortex actually receives PC=1.0 — every D-T penalty fires, but no penalty for the unique mechanical complexity of the GF design. The axis treats it as just-another-D-T-plant. |
| 29 | 13 Avalanche electrostatic D-T | 2.57 | Mod=4.83 with TF=1.0 (no-data) | `Non-Standard|IEC` MVS=5 + Electrostatic mag/driver=5 → modularity 4.83 for a high-voltage cathode device with no demonstrated fusion gain. |
| 30 | 17a Xcimer hybrid drive | 2.55 | TF=3.75 | `IFE|Laser ICF (hybrid drive) = 1e21` is itself a thin baseline (OMEGA-class extrapolation). Xcimer's KrF excimer architecture is a clean-slate engineering bet, not a re-use of OMEGA. |
| 31= | 20b Renaissance stellarator | 2.52 | Mod=3.0 | Laser-patterned HTS film on cylinders is genuinely novel; modularity 3.0 may be too low (or Helical Fusion's 2.02 too low; either way the spread is suspect). |
| 31= | 33 BEST (Neo Fusion, LTS+HTS) | 2.52 | Mod=2.0 | The lowest modularity score in the tokamak group — BEST is a large bespoke LTS+HTS machine, modularity 2.0 is defensible, but the framework gives the same TF=4.0 as CFS. |
| 33 | 27 Polywell (EMC2) | 2.50 | Mod=4.33 with TF=1.0 floor | §1 #13. IEC MVS=5 lookup gift. |
| 34 | 15 Zap SFS Z-pinch | 2.48 | TF=2.0 vs Polywell TF=1.0, but ranked lower | §1 #13. Zap has measured 1e17 + recent yield scaling — penalized by Mod 4.17 vs Polywell's 4.33. |
| 35 | 22 First Light projectile | 2.43 | TF=2.0 inheritance | `IFE|Projectile ICF = 1e17` is FLF's own historical demo; this one is internally consistent. But Mod 3.83 is generous. |
| 36 | 17b Focused Energy fast ignition | 2.36 | TF=2.5 | Inherits hb11 fast-ignition baseline (1e20) with -0.5 laser modifier. The negative modifier is appropriate. |
| 37 | 12 OpenStar levitated dipole D-T | 2.35 | Mod=2.75 | Mod=2.75 from `MFE|Levitated dipole` MVS=3, vessel=3, mag=3 — but D-T levitated dipole has never been considered viable due to neutron flux through the floating coil. Concept itself is dubious; the framework gives it a passable composite. |
| 38 | 25 Heavy ion ICF (Intensity Energy) | 2.33 | TF=1.0, DA=4.0 | DA=4.0 (2 blockers) is suspicious — the entire approach has had no integrated experiment; "2 blockers" likely reflects a shallow gap report. |
| 39 | 16 Muon-catalyzed (Acceleron) | 2.26 | TF=1.0 floor | Muon-catalyzed fusion is outside the Lawson framework; the framework correctly floors TF but still assigns 1.67–4.0 on every other axis, producing 2.26. A correctly-modeled muon-catalyzed concept would need its own physics axis (α-sticking ratio, muon production efficiency); none of that is represented. |

---

## Section 4 — What would move the needle (recommendations, briefly)

These follow directly from §2 root causes; they are not in scope to
implement here, but are the corrective actions implied by the analysis:

1. **Default-low when a trigger is absent.** Replace "no triggers fired →
   5.0" with "no triggers fired → 2.5 (under-specified)" for plant_complexity
   and supply_chain. Reward specificity.
2. **Concept-specific TF where measurement exists, family-floor where it
   doesn't.** Currently the framework charitably uses the family record for
   unbuilt concepts — invert this.
3. **Add a "programmatic credibility" axis** — funding-stage, milestone
   track record, peer-reviewed measurements. Weight it as much as TF.
4. **Split modularity MVS lookup into evidence-backed sub-scores** —
   currently a hand-coded prior masquerading as a derived score.
5. **Filter non-power-plant concepts** (SHINE) or mark them
   `composite = N/A`.
6. **Tighten DA bracket** — 0 blockers → 5.0 is too generous; the bracket
   should probably max at 4.0 and require explicit peer review for 5.0.
7. **Audit upper_cf for physics-conditional 5.0s** (Pale Blue, ENN, TAE,
   Zephyr) — these are intent, not achievable capacity factor.
8. **Re-weight composite as "Physics-first" by default** — equal weighting
   demonstrably inverts the ranking against TF.

---

## Appendix — Where in the framework each issue lives

| Issue | File | Line / key |
|---|---|---|
| M1 PC default-high | `weights/default.yaml` | `subsystem_complexity_weights` (no default value) |
| M1 SC default-high | `weights/default.yaml` | `bottleneck_severity_weights` (no default value) |
| M2 TF family inheritance | `weights/default.yaml` | `achieved_triple_product` lookup |
| M3 SC fuel monoculture | `weights/default.yaml` | `bottleneck_severity_weights` |
| M4 customization double-count | `weights/default.yaml` | `customization.thermal_rejection_scores` + `fuel_safety_scores` |
| M5 modularity priors | `weights/default.yaml` | `mvs_lookup`, `vessel_lookup`, `magnet_driver_lookup` |
| M6 skip-and-rescale | `score.py` | composite formula |
| M7 upper_cf intent vs achievable | `weights/default.yaml` | `operational_penalty_weights` |
| M8 missing programmatic axis | n/a | architectural |
