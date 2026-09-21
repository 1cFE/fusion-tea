# Seven-input source review

[AGENT] Author assistance for C2, not the final independent review. Recommend three reference inputs and four explicitly held inputs. This is a partially reference-specified forward point. No model execution or modification occurred.

| Input | Suggested effective value | Disposition | Evidence |
|---|---:|---|---|
| R | 7.75 m | Reference | Lyon printed p708, Table IV |
| a | 1.70 m | Reference | Najmabadi p657, Table I; Raffray p727, Table I corroborates 1.7 m |
| n_e0 | 5.06e20 m^-3 | Held frozen default | Lyon p708 central density is not peak density; p702 Fig12 has a hollow density profile |
| T_i0 | 11.83 keV | Reference | Lyon p708 Table IV; p701 states Ti=Te; p702 Fig12 confirms temperature peaks centrally |
| I_coil | 15400000 A-turn | Held frozen default | Ku p677 gives three families with different currents; no frozen reduction rule |
| coil_t | 0.3 m | Held frozen default | Published winding depth and supporting structure are not an explicitly specified exterior coil envelope |
| interior_y | 0.4 m | Held frozen default | Published winding-pack width does not explicitly specify clear cavity including clearance |

[AGENT] All numerical findings and source/image hashes are in `suggested-input-records.json`. All cited load-bearing tables and figures were inspected as 200-DPI page images. Page-index fields in JSON are zero-based; printed page numbers are separate. Source priority follows the archived selection policy: exact revision and definition, then applicable erratum, subsystem source, overview. No external source or erratum was consulted.

## Definition judgments

[AGENT] R and a describe averaged plasma radii. The adopted values do not import the ARIES nonaxisymmetric plasma shape, volume, topology, or coil count. Lyon Table I gives an ARE aspect ratio of 4.55; the overview and engineering tables explicitly give the minor radius as 1.70/1.7 m. Ku rounds the aspect ratio to 4.5. Dividing rounded R by that rounded aspect ratio would manufacture a different minor-radius candidate, so the directly tabulated radius is preferred. These published values have no stated statistical uncertainty; retain their printed precision.

[AGENT] Lyon Table IV states central electron density 3.84e20 m^-3 and volume-average density 4.01e20 m^-3. Neither matches peak electron density. Figure 12 visibly rises away from the center. Equation (3) uses a normalization parameter named n_e0, but its printed hollow-profile factor and the central/edge naming in the adjacent prose do not establish an unambiguous peak value. No peak was inferred from an average, digitized from the chart, or derived from that ambiguous normalization. The held profile exponents also remain unchanged.

[AGENT] The central plasma temperature 11.83 keV can be admitted as peak ion temperature because the same source explicitly assumes ion and electron temperatures equal and plots a centrally peaked temperature. The density-averaged 6.55 keV is rejected for this input. This does not admit an ARIES temperature-profile override.

[AGENT] Ku p677 specifies coil currents of 10.8, 13.5, and 13.1 MA for the three coil families, with maximum winding current density about 94 MA/m². In context these are aggregate winding currents (ampere-turns), not turn currents. Lyon Table I also labels its normalized current as a maximum. The frozen contract does not identify a family or prescribe maximum/mean reduction. Selecting 13.5 MA-turn because it is largest, averaging families, or solving current from the reference field would add a selection rule after reveal. Retain the default and disclose the mismatch.

[AGENT] Raffray p744 Figure 23 gives a 0.194×0.743 m winding pack, a 0.02×0.743 m cover plate, a 0.28 m strongback, and 0.2 m intercoil structure. These are average dimensions for coils wound into an integrated toroidal supporting tube, as described on p743. Lyon p706 Table II independently lists 2 cm cover, 28 cm strongback and 16–28 cm intercoil structure. The derived radial sum 0.494 m is recorded as a candidate only. It does not explicitly define the model's single-coil exterior allocation. Likewise 0.743 m labels winding-pack and cover widths, without a clear-cavity/clearance dimension. Both inputs remain held pending an independently justified exact-definition mapping. The individual dimensions were not silently substituted for these inputs.

## Revision and conflict preservation

[AGENT] Raffray p726 explicitly warns that component analyses were performed at different times with somewhat different system parameters and were not always rerun. Its p727 Table I belongs to the three-field-period configuration but has other design-state differences from Lyon's final reference table. Consequently its coil structure dimensions establish source candidates, not automatic permission to synthesize a final-design casing. Lyon p695 introductory text mentions 24 coils whereas its p697 reference ARE table and Ku p677 describe 18 coils. This source inconsistency is preserved; coil count is outside the seven-input authorization and is not changed. Published rounding differences in aspect ratio are retained as described above.

[AGENT] The four held inputs block a fully reference-specified point claim for dependent rows. Their defaults are model assumptions, not ARIES measurements. Unsupported technology correspondence, shape, profiles, subsystem choices, and current model limitations remain active. No field, fusion power, beta, coil mass, cost, or desired output was used to tune the admitted values.
