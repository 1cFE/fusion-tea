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
