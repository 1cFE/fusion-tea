# T-004 cryogenic sources: initial environment-limited acquisition

**2026-09-15 · [AGENT] assessment.** The native run returned `OPERATOR_QUEUE`, with no registrations. This is not evidence that the sources are unavailable. All three captures returned `extract exited 1`; no numerical coefficient is admitted or recommended from this run.

## Native evidence and diagnosis

Request: `knowledge/research/requests/REQ-MCR-CRYO-01.json`. Return: `knowledge/research/requests/runs/REQ-MCR-CRYO-01/20260915T133759624946/return.json`; the same directory retains queries, candidate notes and three receipts. Three searches and three captures were attempted. Closed with `--adequacy limit_reached`; the native return nevertheless prints `limit_reached: null`, preserved unchanged.

All invocations used `.codex-test/run` in the default sandbox. No network escalation was attempted. A bounded read-only diagnostic found `trafilatura` installed but DNS resolution of `cds.cern.ch` failed with `socket.gaierror: [Errno -3] Temporary failure in name resolution`. This establishes an environment obstacle, not the cause of every individual extraction. `scripts/source_registry.py:467–475` captures both streams but reports only stderr on failure; the installed extractor's `extract_cli.py:246,261` prints URL failures to stdout. The original detailed stdout was not retained. No seam code was changed.

## Candidate inventory: triage only

All candidates passed the protocol's identity/topic screen before fetch. External results were used only to select candidates. None was captured, so none establishes a citable quantitative result here; page-image verification remains outstanding.

| Candidate queued in native return | Intended evidence | Transfer limit requiring inspection |
|---|---|---|
| CERN, *HTS Current Leads: Performance Overview in Different Operating Modes*, `cds.cern.ch/record/1026941/files/at-2007-005.pdf` | Lead design and cooling-regime distinctions | Gas inlet temperature is not coil cold-end temperature. Need cold-end/intercept loads at the chosen operating current and cooling scheme. |
| NIST, *G-10 CR Fiberglass Epoxy*, `trc.nist.gov/cryogenics/materials/G-10%20CR%20Fiberglass%20Epoxy/G10CRFiberglassEpoxy_rev.htm` | Conditional temperature-dependent support conductivity | Material and orientation must match the support. Property curves alone supply no support heat load. |
| NASA, *Layered Thermal Insulation Systems*, `ntrs.nasa.gov/api/citations/20150018118/downloads/20150018118.pdf?attachment=true` | Insulation performance and test-condition dependence | Vacuum, layer arrangement and boundary temperatures must match; warm-to-shield performance cannot be assigned to the shield-to-coil boundary. |

## Existing evidence and missing-input options

The current instance binds only winding nuclear heat and resistive joints in its cold-load inventory (`models/designs/stellarator_09/stellarator_plant.sysml:1171`; `models/library/analyses/mfe_cryo_plant.sysml:7`). The ITER entry and DI-009 explicitly distinguish cold and warmer refrigeration duties (`knowledge/SOURCE_INDEX.md:192`; `knowledge/KNOWLEDGE.md:70`). Neither supplies Stellaris lead, radiation or support coefficients.

- **Lead topology:** admitted Stellaris extraction §2.9 describes six series-connected groups and Fig. 46 describes eight coils per group (`knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/output.md:2147,2163`). This is an image-unverified circuit-model clue, not a verified terminal count. Options: verify the original figure and adopt a stated two-terminal-per-group engineering assumption, or obtain the actual terminal design. Do not infer 96 leads from 48 coils. A terminal count still needs qualified cold-end and intercept load versus current.
- **Radiation:** obtain shield temperature, cold-facing area, emissivity/MLI construction, vacuum, seams and penetrations. Options: device drawings and matched test data, or an explicitly approved parametric engineering scenario. Keep warm-to-shield and shield-to-20 K heat separate.
- **Supports:** obtain material, orientation, count, cross-section, path length, contact assumptions and intercept temperatures. Options: a device support drawing plus material-property integration, or an approved support design scenario. NIST G10 is only a candidate material, not a selected default.
- **Wall power:** use each temperature stage's refrigeration duty and justified plant efficiency; include warmer intercept refrigeration in total wall power. A single 20 K conversion cannot silently absorb that duty. Additional nuclear heating of coil cases and cooled supports is also explicitly deferred in Stellaris §2.9 (`output.md:2182–2185`); the existing winding-only volume does not establish it.

**Recommended next action [AGENT]:** retry the same bounded request through authorized network access before deciding source adequacy. Then verify captured original pages and put the remaining device choices to the coordinator. The cryogenic chain is not yet implementable from justified inputs. Cooling-slot disposition remains in coordinator-owned `T-004_cooling_slot.md`.

## Retry 1 addendum — 2026-09-15

**[AGENT] Native result: `REGISTERED`.** Authorized elevated network operations retrieved two admissible sources. Return: `knowledge/research/requests/runs/REQ-MCR-CRYO-01/20260915T134156635935/return.json`. The original failed run remains intact. Retry used one further search (four across both attempts), two successful captures, and a precondition refusal that spent no capture. The known CERN paper remains queued after its CDS endpoint returned an Anubis HTML challenge and the departmental mirror failed DNS even with elevation. The short CERN URL redirected to that same unresolved mirror.

A premature keeper note incorrectly said the mirror PDF bytes were verified. A following native log entry corrects that statement: curl had failed and no file existed. The resulting `/tmp/T004-cern-leads.pdf` precondition receipt is an agent execution error, not an additional source for the owner to retrieve. All CERN queue entries refer to the same paper. No capture was made from challenge HTML or web search output.

### Registered evidence and original-content inspection

| Source | What it now establishes | Model transfer limit |
|---|---|---|
| `knowledge/sources/nist_g10_cr_fiberglass_epoxy_cryogenic_material_properties/` | Captured NIST table gives separate normal/warp conductivity polynomials. Original rendered table verifies equation domains of 10–300 K and 12–300 K respectively, with 5% fit error relative to data. | Usable material-property function only after support material and orientation are chosen. No support heat-load coefficient, dimensions or intercept layout follows from this source. |
| `knowledge/sources/layered_thermal_insulation_systems_for_cryogenic/` | Original NASA slide 20 gives a high-vacuum MLI design benchmark below 1 W/m², with effective conductivity below 0.1 mW/(m·K) at 300 K / 77 K, and typical layer density about 2/mm. | A design presentation benchmark, not a device qualification or a 77 K / 20 K flux. Do not apply it directly to the 20 K load or interpret its inequality as a selected nominal value. |

The NASA PDF's printed title is *Layered Thermal Insulation Systems for Industrial and Commercial Applications*, James E. Fesmire, NASA Kennedy Space Center, webinar August 26, 2015. The registration uses a descriptive cryogenic-applications title; the source identity is SHA256 `8773476b3ddab256f03703af1bf8f2384d7628a72c5fb1d35fa850a0c88d7841`. Its original download URL is preserved in registry metadata. NIST raw identity is `6992fc4a372745b3b6a852c4df75eb3f98065db9babb29599a9a2520ee113665`.

Original-content checks are retained under the retry run's `inspection/`: NASA slide 20 rendered from the downloaded PDF and NIST's registered raw HTML rendered with browser-inspect. The NIST sidecar reports missing plot/navigation assets and file-origin CORS errors; the complete static conductivity table and polynomial rendered legibly. No plot was used. No current-lead coefficient has original-page verification.

### Concrete choices still needed

1. **Terminals:** coordinator verified Stellaris original p25 (`evidence/T-004_stellaris_p25.png`), confirming six series groups of eight coils. Choose either twelve leads as an explicit two-terminal-per-group engineering assumption, or wait for a terminal drawing. Twelve is conditional; 96 is unsupported. Either route still needs a qualified lead thermal design at the selected coil current and temperature stages.
2. **Radiation:** choose device shield/cryostat geometry and insulation specification, or authorize a separately labelled parameter scenario with cold-facing area, emissivity or matched MLI performance, shield temperature, vacuum and seams. NASA's benchmark can check a selected warm shield design; it cannot fill the cold-stage coefficient.
3. **Supports:** choose a real support layout and material, or authorize an explicit engineering scenario specifying count, area/length, orientation and intercepts. If G10 is selected, the registered conductivity curve can support each segment's heat integration. It does not establish that G10 is mechanically suitable for this reactor.
4. **Refrigeration:** choose qualified stage efficiencies or explicitly retained efficiency assumptions for both the 20 K and warmer stages. Report the sum of their wall-power demands; keep unresolved case/support nuclear heat and the existing uplift disposition visible.

**Recommendation [AGENT]:** obtain the CERN paper through an accessible primary-author copy or operator retrieval, and seek device terminal/support/shield inputs before selecting numerical additions. The two registrations improve the evidence base but do not make a complete cryogenic inventory implementable. If the owner wants progress using engineering scenarios, the four choices above define what must be authorized; no scenario values were selected here. Cooling-slot choices remain coordinator-owned.
