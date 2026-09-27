# Focused review of the C1 cryogenic-demand correction

**Final disposition,2026-09-27: PASS.** The objective corrections were independently verified; changed cryogenic-demand and auxiliary-sink implementation is released. See the dated verification below. The initial findings are retained as review history.

**Initial disposition: FINDINGS limited to the objective corrections below. The new cryogenic-demand equations and conditional source interpretation are accepted.** Verify the bounded corrections before releasing the changed cryogenic/sink implementation. No owner gate or new transport calculation is required. [First capture review](capture-boundary-review.md) remains unchanged.

[AGENT] Continuing independent non-author review,2026-09-27. Reviewed correction against81423599: design SHA256 `0c74301360718cab84c4364cfd489103a0797e5ab465f5d73d48acc133a6bd37`; configuration SHA256 `b50ad9dffb590409630ce1206e44e1f33b4d25a25f74204994f79dde96a1c109`. The coordinator separately identified the stale envelope and capture-status sentences. Only reviewer evidence was written.

## C1 correction accepted

The revised source paragraph correctly calls2652.563 MW a chosen study-domain ceiling. It identifies35.5 W/m³ and extra cold watts as uncertain supplied demands, assumes the selected heat scenario across the source range, and preserves zero source/transport/global-construction qualification. It asserts no unverified fusion-to-heating law.

The dynamic cold-load equation exactly reproduces the captured native terms: volume307.2600000000001 m³, cold inventory9322.57888517031 W, fixed joints7500 W, intercept41189.504334608944 W, uplift1 and the selected20/77/300 K temperatures with both Carnot fractions0.2. Cold/intercept capacities and the USD62,957,384.24217385 quote remain independent supplied hardware choices. Both heating inputs must be finite nonnegative demands; normal native domain guards should enforce that.

The independent [probe](boundary-review/check_capture_r2.py) and [receipt](boundary-review/capture-r2-checks.json) reproduce the35.5/extra0 reference cold load and refrigeration exactly at float precision. They give:

| Mean heating W/m³ | Extra cold W | Cold demand W | Cold margin W | Refrigeration MW |
|---:|---:|---:|---:|---:|
|35.5|0|27730.308885|12269.691115|2.537567042|
|50|0|32185.578885|7814.421115|2.849435942|
|80|0|41403.378885|−1403.378885|3.494681942|
|35.5|10000|37730.308885|2269.691115|3.237567042|
|35.5|13000|40730.308885|−730.308885|3.447567042|

These are independent equation checks, not new native scenario executions. The declared native tests must retain80 W/m³ and excessive-extra-heat failures, propagate refrigeration and extracted heat to the sink, propagate refrigerator electricity to export/standby economics, and prove unchanged selected capacity/inventory/quote. The configuration's clarification that gas slot9 contains inseparable stock also resolves the previous nonblocking wording note without changing its equations.

## Required objective corrections

### S1 — remove duplicate coil-drive heat from the auxiliary sink

The exact captured coil-drive electricity is0.04855663413365344 MW. It equals `(q_lead_cold8379.899951670068 + q_lead_shield32676.734181983367 + joint7500) W ×1e−6`; `joint_drive_fraction=1`. Those lead/joint heat terms already appear in the cold/intercept heat extracted by refrigeration, as defined by `mfe_cryo_inventory.sysml` and the exact native outputs.

Design§4 currently adds both coil-drive electricity and cold/intercept extracted heat to the auxiliary thermal sink. That counts the same drive heat twice. **Keep subtracting coil-drive electricity once in the net-electric ledger. Remove its separate addition to the auxiliary heat sink.** The refrigerator's contribution to that sink is `refrigeration_MW + cold_MW + intercept_W*1e−6`; all lead/joint heat is already inside that expression. Keep the other declared heating-loss, TF/fuel/house/control/residual, primary-motor-loss and auxiliary-pump terms unchanged. Baseline refrigerator heat to the sink is2.6064868550919478 MW. This corrects a thermal-ledger duplicate; it is not permission to remove coil electrical consumption.

### S2 — remove two stale claims and correct the displayed threshold

- Replace design§3's “the capture must bound all ranked fusion points and neutron heating” with the separate chosen-fusion-domain and assumed-heating-scenario conditions. The preceding wall-load surrogate remains conditional; neither condition establishes a validated nuclear-transport envelope.
- Replace §8's “No complete48 kA capture exists yet” with its current status: exact capture exists, local reviewed component checks pass at the supplied reference demand, full-plasma failures are retained, and new heating-scenario propagation/integration remains required.
- Correct the displayed no-extra-heat cold threshold from75.432600777 to **75.432601428 W/m³**. Its written equation is already correct. Do not use the rounded prose value as a numerical acceptance tolerance.

### S3 — make the hot-source multiplier's scope explicit

The retained original paper resolves the relevant scope: `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md:1662–1670` describes multiplication within the blanket and heat extractable from blanket/shield. It discusses nuclear heating of the winding packs separately at1699–1718. The native `Reactor Source Heat` equation produces the useful hot-loop source before pump recovery; its1.2 transfer to the helium/generic-build scenario is already conditional in `stellarator_plant.sysml:596`.

Record the analysis convention that **m_n=1.2 is an effective multiplier for blanket/shield hot-source heat, excluding cryogenic nuclear deposition**. Under that explicit regional accounting assumption, q_nuc/extra-cold scenarios are additional cold-region demands and do not alter the existing source/fusion/fuel inversion. They are not being counted inside hot-source heat and again at the cryogenic sink. The authority is the retained source's regional meaning plus the owner-authorized conditional transfer, not newly validated neutronics. Do not label1.2 a demonstrated total-reactor nuclear-energy multiplier or claim a new global nuclear-energy closure. No fusion correction or subtraction of cold heat from the supplied hot source is warranted under this stated convention.

## Release scope after verification

The corrected design preserves MR-7 at design level: heat demand changes while chosen magnet geometry, cryoplant40/60 kW capacity and price stay fixed. Native integration still owns full behavioral assurance. Existing source/property/current/fit/pressure/divertor requirements remain enforced independently. A failed cryogenic-demand scenario cannot rank. Once S1–S3 are applied exactly, these are objectively checkable repairs; a full repeated cost/design review is unnecessary.

## Final correction verification —2026-09-27

[AGENT] Independently inspected the corrected design/configuration diff and the exact affected paragraphs. Verified design SHA256 `c06d70170d69254469870c49bb9bd0cf74abf13f8443021e60c9cf922e8e76a8`; configuration SHA256 `8a71c411083d54b12225bdb9f594170184745f8bef574e4aab1698010c93a36b`.

- **S1 resolved:** Net electricity still subtracts coil drive once. Auxiliary rejection now uses refrigerator electricity plus extracted cold/intercept heat and excludes the duplicate coil-drive thermal term. The stated2.6064868550919478 MW reference refrigerator rejection matches the independent receipt.
- **S2 resolved:** Fusion-domain and uncertain heating conditions are separate; the validated-envelope claim is removed. The design records that the exact48 kA capture exists and that its full-plasma failures remain retained. The displayed threshold is corrected to75.432601428 W/m³; its equation is unchanged.
- **S3 resolved:** Design§3 and configuration explicitly identify1.2 as an effective blanket/shield hot-source multiplier excluding cryogenic deposition, cite the retained source's regional meaning, preserve the conditional transfer, and reject a global neutron-energy-closure claim. Cryogenic uncertainty therefore leaves the declared hot-source/fusion/fuel inversion unchanged.
- **Demand domain resolved:** Both nuclear-heating inputs are explicitly finite and nonnegative, with invalid inputs failing native domain checks. Dynamic demands reach the electricity, auxiliary-sink and standby consumers while hardware, ratings and price remain fixed.

**PASS for this corrected design and the changed cryogenic/sink implementation. MR-7 compliant at design level; native implementation and integration remain unverified by this focused review.** Native scenario execution, independent output/predicate checks and integration assurance remain required before ranking. The accepted equations did not change during these objective text/binding corrections, so the existing independent arithmetic receipt remains applicable; no broad numerical or cost rerun was needed for this disposition.
