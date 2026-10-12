# Independent design review: integration file-read coverage

Date: 2026-09-20. Reviewer: fresh non-author integration reviewer. Scope: pre-implementation review of `spec.md` and `design.md` in this directory against the existing integration, manifest, indicator and stock route code. No reference observations or comparison were consulted. No tests were run for this design review.

## Verdict

**PASS for implementation release, 2026-09-20.** The amended design resolves the two identity findings and states the output and receipt acceptance conditions. The approach is appropriate: the integration seam owns admission, reuses the existing static membership assertion, and observes the actual baseline route before import. One observer module is proportionate. This is design approval only; implementation acceptance remains dependent on the verification below.

## Findings

1. **Major — record the executable bytecode actually opened, or prevent its use.** `design.md:7` maps bytecode to source and checks source hashes. The package seal explicitly excludes `**/__pycache__/**` (`exploration/stellarator_e2e/generated/contracts/package_contract.json:449`). An opened cache can therefore differ without its bytes appearing in the package seal or the proposed source-only identity. Calling Python's cache validation a limitation does not account for the dependency bytes the audit hook can observe. Record and check the actual bytecode hash alongside its declared source identity, or force source execution for declared project/dependency modules. Specify behavior for sourceless bytecode. A cache hash records what executed; it does not prove equivalence to source. Add an actual cached-import test exercising changed cache bytes, plus an unchanged-cache success case.

2. **Major — extend the seam's tool identity to include its new implementation dependencies.** `scripts/integrate.py:88` explicitly lists the sources whose edits change gate meaning; `scripts/integrate.py:683` emits that digest on both success and failure. The new observer and newly imported indicator parser must join this list. Route-time source hashes alone are insufficient for failures before observation starts, or for the observer's bootstrap code. Add a focused assertion that both new dependencies appear in the returned tool identity. This can preserve the existing candidate schema.

3. **Implementation condition — output admission must mean newly created output, not any write-open.** `design.md:5` intends new run outputs, which is sound. Make the rule explicit for pre-existing files and read/write modes: append and `r+` must not turn old contents into admitted inputs, and output handling must never override a sealed package or declared source identity. Canonicalize before classifying. Test a new output written then read, a pre-existing output opened for append/read, and a sealed dependency written then read. The audit hook observes an attempted open before success, so evidence should describe write-open admission accurately rather than claiming proof of completed writes.

4. **Implementation condition — missing or invalid observation evidence cannot pass.** Gate 7 must require a fresh valid successful receipt before preflight, including when the route exits zero after catching a refusal. Retain violations when the route fails for another reason. A stale receipt in a reused output directory must not satisfy this invocation. Exercise these paths through the integration gate, not only observer unit tests.

## Accepted scope and boundaries

- Static coverage is membership, not dynamic observation. Reuse is correct: `scripts/study/indicators.py:819` already calls the assertion. The existing Gate 6 comment claiming no caller is wrong. Resolving pipeline references with `read_pipelines` catches an EntryPoint outside the manifest pin before the input is opened.
- Exact package artifacts come from the seal, while the manifest covers pipeline/input/model-contract artifacts. Broader route/scripts/teax source declarations are acceptable as an explicit dependency policy if their exact paths and initial hashes are retained. They must not be described as manifest-pinned files. Classification precedence must prevent a broad source or runtime category from weakening package seal checks.
- Runtime files hashed at first observed access provide a receipt of those bytes, not a verified installation image or proof that an earlier toolchain probe used identical bytes. Preserve that distinction. Package/source pre-execution hashes and runtime first-observation hashes have different authority.
- Hash-before-open and hash-after-execution cannot prove that the bytes hashed are the bytes consumed. Changes between hashing and the actual open, or transient changes restored before the next check, remain a time-of-check/time-of-use limit. State this in the receipt along with the already named native C, SQLite, mmap, direct-syscall, pre-opened-handle, environment and network exclusions. Integer-descriptor events must be visibly unsupported; they must not silently become declared reads.
- Subprocess refusal is a justified boundary for this cooperative single-process observer. It does not establish a sandbox. Observer deactivation before writing the receipt is sensible, but execution after deactivation is outside the claim.
- A baseline receipt covers that invocation. It does not establish read coverage for every future study point or unexecuted branch. No full-design-space file coverage claim follows from one baseline.
- **MR-7 compliant for the proposed tooling-only scope.** The design changes no quantity, binding, chosen equipment, capacity, cost consumer or selection policy. This verdict does not re-certify the scientific model. Implementation acceptance must confirm that scope remains unchanged.

## Verification needed for acceptance

Run real observer subprocess cases for declared reads, undeclared input, undeclared dependency, symlink/external escape, changed declared dependency, cached imports, output admission, and blocked subprocess creation. Add integration cases proving refusal produces no candidate and retains evidence, including caught violations and stale/missing receipts. Check the static membership gate separately. Finally run the stock live seam from the committed implementation checkpoint and cite its exact model, package and tooling identities. Public-input consumer tests alone cannot establish this gate.

## Resolutions

2026-09-20: Independently reread the author's `Review amendment` in `design.md` before implementation. Finding 1 is resolved by recording and checking actual bytecode bytes alongside their declared source, refusing sourceless project bytecode, and requiring unchanged-cache and cache-mutation tests. Finding 2 is resolved by adding both new dependencies to the seam's tool identity and testing the emitted entries.

2026-09-20: Conditions 3 and 4 are incorporated explicitly. Classification precedence preserves package/source identities, output admission requires absence at first write-open, and old append/read-write files refuse. Parent-generated invocation tokens and removal of stale receipts bind evidence to this invocation. Missing, malformed, mismatched, failed or violation-bearing receipts refuse even after a zero route exit. Tests remain required.

2026-09-20: The amendment also states baseline-only scope, distinct runtime hash authority, and TOCTOU limits. Release to implementation is approved. No implementation or test result has been reviewed yet. The reviewer owns this review file only.
