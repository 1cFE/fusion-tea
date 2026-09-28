# T-048 native preparation correction

The exact thirteen-output Python return annotation is restored, and the corrected fresh generator now uses the stock producer's smart-regeneration option. This is a native completion-signature correction. Runtime statements, guards, physical equations, SysML definitions, inputs and outputs are unchanged. Original T-047 failure, previous native receipts and the initial independent PASS remain preserved; that audit proved fresh equality under preservation mode and did not prove stock smart in-place equality.

## Cause and evidence

The integration producer invokes `sysml-codegen generate --overwrite --smart-regen --preserve-handwritten` (`scripts/integrate.py:1000`). The initial WI-056 helper passed preservation mode and left `GenerationConfig.smart_regen` at false. The completion's return annotation was shortened to `tuple[float, ...]`; the installed signature detector compares annotation strings and expects thirteen explicit float types for thirteen outputs (`sysml_codegen/generation/preservation.py:88`, `:180-187`). It therefore treated the valid runtime completion as a changed signature.

The retained scratch stock probe (`probe.py`, `stock.log`, `stock-delta.json`) reproduces the consequence: one manual completion is replaced by a generated stencil and a timestamped handwritten backup is created, changing the package contract. T-047 listed only the package-contract movement because its first regeneration gate excludes the handwritten subtree; handwritten preservation would have failed at the next gate, which was not reached. No package-contract field was hand-edited and no stock gate was bypassed.

`correct.py` changes only the return annotation and checks identical parsed syntax trees after removing that annotation for comparison. `signature-correction.json` records the exact changed seed hashes. All twelve other normative seeds remain unchanged. The generated package changes only the primary completion annotation and the resulting sealed package contract; current manifest identity follows the new executable. Snapshot and public census remain unchanged.

## Corrected producer and checks

Use `evidence/regenerate_corrected.py:seed_and_generate` with `evidence/corrected-candidate-seeds.json` and `evidence/corrected-package-hashes.json`. This new helper requires smart regeneration and preserves the same checked-source inventory, thirteen typed seeds and fresh-destination guard. The earlier helper and receipts remain frozen evidence for their earlier candidate.

- `generation-corrected.log`: two independent empty-destination smart generations match all 247 current package files exactly and preserve every corrected normative seed.
- `probe_corrected.py`, `stock-corrected.log`, `stock-corrected-delta.json`: the exact stock CLI options on a disposable copy move no file, including handwritten bodies. All 77 implementation files are preserved; none are regenerated and no backup is created.
- `focused.log/xml`: 59 primary-loop component tests pass on the corrected package. Combined with the exact runtime-AST preservation check, the correction leaves domain, zero-source, dormant, positive anchors and conservation/scaling behavior unchanged. No full model suite is repeated for an annotation-only correction.
- `metadata.json` and `derived-census.json`: current manifest package identity and pin validate, and the public census remains unchanged. Before here means the original audited T-045 candidate; the earlier initial-extraction failure is separately documented in the parent evidence.

T-049 separately owns migration of the current consumer helper and frozen receipt references, followed by focused consumer acceptance. The independent auditor must verify both corrected fresh and stock in-place behavior before coordinator integration. No integration, candidate promotion, tool patch, scientific change, source adoption or historical rewrite is performed here.
