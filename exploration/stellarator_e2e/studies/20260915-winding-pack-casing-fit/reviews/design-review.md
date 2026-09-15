# Independent WI-061 source, mathematics and interface review

Date: 2026-09-15. Verdict: **PASS for the conditional design; no material design finding.** Reviewer: fresh non-author `fit_reviewer`. Reviewed preparation checkpoint `677d6d31755981f396d24155235f4a49e3ab87a8`, including geometry research, WI-061 spec/design/plan and consumer inventory. This pass does not certify implementation, generated execution, study results or manufactured fit.

## Source and interpretation

I visually inspected Stellaris original-page renders 21–23 and enlarged Figure 40, and W7-X manuscript pages 5–6. Original PDF hashes independently match the research record: Stellaris `7fd72c1242ce3a17a9c4b9a4597fcb9ff5296b942b2d8343a0b463539d8d3865`; W7-X `a92c209b6949d9c4b4ce5e9797e07f71fa92309949f7156c74a5565d7f9522c4`. Source paths and page references are in [geometry-research.md](geometry-research.md). Quarantine protocol was read before source access; no barred source was opened.

Figure 40 places the 0.5 mm sheet above the vertical 20 mm arrow. Its radial direction is horizontal and Phi direction vertical. Table 8 nevertheless gives square 360 mm sections for 324 turns. Therefore the inherited side is a nominal current-density envelope with unresolved insulation inclusion, not verified bare conductor or a fully insulated manufactured pack. The final design's x-radial/y-transverse convention agrees with the figure under its declared local alignment assumption; it deliberately differs from the research note's initial axis naming.

I accept `fx=0, fy=0.025` as an explicitly excluded-sheet continuous-pitch scenario. At 360 mm it adds 9 mm, not 8.5 mm; one sheet per cell conservatively includes an end sheet. `fy=0` remains the included-sheet alternative. Neither is a source-certified correction. W7-X supports distinct ground insulation and embedding allowances, but supplies no qualified Stellaris thickness. Whole-coil exterior spans and neighboring-coil clearance cannot determine this cavity.

## Independent arithmetic

Calculations ran through `.codex-test/run python` using direct equations independently of generated code. All lengths below are metres.

| Case | Required x/y | Cavity x/y | Margin x/y | Fit |
|---|---|---|---|---|
| Reference, excluded sheets | 0.370 / 0.379 | 0.250 / 0.400 | −0.120 / +0.021 | Fail |
| Reference, included sheets | 0.370 / 0.370 | 0.250 / 0.400 | −0.120 / +0.030 | Fail |
| Enlarged side 0.500 | 0.510 / 0.5225 | 0.250 / 0.400 | −0.260 / −0.1225 | Fail |

For a binary-exact boundary use `s=.25, r=1, T=.375, Cy=.25, w=.0625`, with all other allowances zero: both margins are exactly zero and pass. Reducing T or Cy independently by `.03125` fails only that axis. Increasing both by `.03125` passes. The nominal square-side limit is `.24`. Nonzero insulation/clearance perturbations must additionally verify the two-face convention.

## Interface and release limits

The radial build explicitly uses `coil_or=vessel_or+coil_t` and `r_coil_centre=vessel_or+coil_t/2` in `mfe_plasma_scaling.sysml:111`. Thus interpreting coil_t as an exterior local allocation is an honest additional scenario, not a measured casing. Holding it independent of sizing exposes the reference conflict. Sweeping it must retain existing field, circumference, stored-energy and economic consequences.

The planned magnet-owned calculation, physical input ownership and separate EXPOSE margins fit the existing bindings. Preservation obligations are correctly identified: eighteen original predicates plus one new predicate; complete oracle maps including coil_t; unchanged inherited seed bodies; current catalog/snapshot updates without rewriting historical evidence. Dimensions require finite positive domains, nonnegative allowances, overflow/underflow checks and deliberate errors; negative margins remain valid results. These obligations still require implementation evidence.

Accepted limits: aligned, centered rectangular envelopes at a representative local station; common nominal temperature/load configuration; no route, fillet, offset, deformation or stress certification. Procurement remains based on nominal area; additional insulation procurement is omitted. Thermal surface and stress remain their prior proxies and are not requalified by fit. No wall mass or cost is inferred from the new geometry.

Two editorial cleanups before implementation: replace remaining “bare” labels with “nominal envelope,” and remove the stale sentence saying nominal allowances remain pending research. Carry the centered-envelope assumption explicitly into model documentation. These clarify the accepted design without changing its equations or selected values.
