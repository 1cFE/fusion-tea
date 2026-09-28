# Reference blanket inventory under supplied geometry

[AGENT] Three reference blanket regions now execute as connected model objects: supplied geometry determines region volume; nine material children calculate constituent mass and source-rate price; three recipe summaries and one assembly sum aggregate their outputs. The result is a partial inventory under explicit normalized geometry, not ARIES whole-component inventory or installed capital. Independent completion review accepted the bounded result; see `work/orchestration/aries-transfer-experiment/evidence/constituent-review.md`.

## Results

[AGENT] The normal case supplies a 1 m2 full-coverage midpoint-area basis to each region. Coverages and recipes come from Lyon Table II. The tapered thickness is deliberately evaluated at its two printed endpoints, not assumed to be either the source's actual mean or a probability range.

| Native case | Represented volume m3 | Known non-helium mass kg | Unmapped source-rate subtotal USD2004 | Unquantified He volume m3 |
|---|---:|---:|---:|---:|
| Lower taper, 0.25 m | 0.452222 | 3481.66299186 | 87876.662606406 | 0.03617776 |
| Upper taper, 0.543 m | 0.522542 | 4019.02874226 | 102345.242538246 | 0.04180336 |
| Double all supplied areas | 0.904444 | 6963.32598372 | 175753.325212812 | 0.07235552 |
| Double only full-region LiPb rate | 0.452222 | 3481.66299186 | 130558.624149312 | 0.03617776 |
| Zero all supplied areas | 0 | 0 | 0 | 0 |

[AGENT] Doubling area doubles all material quantities and source-rate sums while leaving thickness, recipe and unit rates unchanged. Changing one LiPb rate changes only price outputs; every volume, mass and represented-fraction output remains bit-identical. The zero-area case remains valid only when material fractions and region coverages still satisfy their respective closure rules. Source-rate totals include LiPb, which the source allocates separately to account 26; this combined subtotal is intentionally unmapped to a blanket installed-cost account.

## Native route and checks

[AGENT] Four new generic definitions implement covered layer volume, constituent inventory, a three-constituent recipe summary and a three-sector sum. One case assembly instantiates 16 calculations: three layer volumes, nine constituent inventories, three recipe summaries and one total. The represented structures are three regions containing nine material children plus an assembly total. There are no reused unchanged physical definitions in this increment. Existing parser, generator, typed-completion and TEAx machinery are reused. Four new guarded completions implement the documented identities; one small helper handles finite-domain checks.

[AGENT] The isolated build stages only the new library and design files, generates wrappers and contracts, copies the authored completions, and regenerates with `--preserve-handwritten`. The provisional loader then verifies/loads the generated package. Five real TEAx pipelines execute supported scenarios; fourteen more exercise native refusals. No caller supplies computed inventory outputs. Generated bindings connect each material to its region volume and each summary to its actual child outputs. [Build identities](evidence/build-hashes.json), [generation](evidence/generation.log), [completion/sealing](evidence/completion-generation.log), and [all outputs/inputs](evidence/results.json) are retained.

[AGENT] Independent 50-digit decimal checks compare 46 component/region/assembly values per supported case, giving 230 comparisons. Tolerances are 3e-15 relative and 1e-12 absolute. Additional checks verify exact area doubling, unchanged geometry/mass during the single-price change, and the expected price delta. The independent arithmetic is evidence for the elementary identities and bindings; it does not validate an actual ARIES geometric reconstruction.

[AGENT] Fourteen invalid cases are refused: negative area/thickness/density/rate; zero density; out-of-range coverage/material fraction; incorrect recipe closure; incorrect recipe closure with zero volume; incorrect lateral partition; incorrect partition with all areas zero; nonfinite area/density; and output overflow. Each case executes the generated native pipeline and checks that the rejection names the intended domain defect. Missing helium density and price are never passed as zero values to a constituent calculator; only helium volume is computed.

## Review corrections and static validation

[AGENT] The source/design review accepted the Table II reference scope before implementation. It corrected unsupported chronology attached to the Fig5/TableII discrepancy and clarified the alternative as deferred. The first executed candidate passed its numerical tests but lacked an aggregate lateral-partition check. Integration review caught that omission. The repaired sum consumes the three coverage fractions and rejects a sum differing from one by more than 1e-12, with no normalization and no bypass at zero volume. First-candidate outputs and its execution log remain in `evidence/results-attempt-01.json` and `evidence/execution-attempt-01.log`.

[AGENT] Full scoped validation returns exit 1: L1–L5 pass, while L6 reports 39 unsupported `.` operators, all plain EXPOSE expressions in the design. Their complete locations are in [expose-locations.txt](evidence/expose-locations.txt); the first is design line 15 and the same pattern appears on constituent and region outputs. Actual generation and all five supported native cases resolve these edges. Independent review accepted these 39 named static-tool exceptions narrowly; this is not a six-level validator pass. The generated single-output volume wrapper's scalar ABI was checked and corrected before first execution. No broad shared-model regression was needed or claimed.

## What remains unsupported

[AGENT] The detailed Table II coverage split is deliberately selected over the conflicting schematic Fig5 split; the source conflict remains. Source values and price-year interpretation were independently inspected, and [source hashes](evidence/source-hashes.txt) identify the retained PDF and rendered table. The rates price source-assumed complex machined shapes, not raw stock or full installation. The SiC/SiC alternative is not mixed into this FS/He reference assembly.

[AGENT] Actual reference totals still need LCFS/midpoint geometry and a justified mean taper/distribution. First wall, divertor hardware, second blanket, back walls, shields, manifolds, supports and installation remain outside the three-region result. Helium mass/cost need state/density and price evidence. There is no breeding, cooling, stress, replacement or LCOE result. MR-7 supplied-choice preservation is demonstrated for represented geometry, fractions and rates; no hardware sizing policy or adequacy selection occurs.

## Reproduce

```bash
.codex-test/run python exploration/aries_transfer/constituent_inventory/build.py
PYTHONPATH=/home/reid/1cfe/teax/packages/teax-simkit:/home/reid/1cfe/fusion-tea .codex-test/run python exploration/aries_transfer/constituent_inventory/run.py
.codex-test/run agentic-mbse validate --complete exploration/aries_transfer/constituent_inventory/input_models
```

[AGENT] Staging copies, import links, native run stores and bytecode are ignored. The new source, guarded completions, generated package/contracts, scripts and compact evidence are retained. Shared source files, baseline packages and the original assessment were not edited by this item.
