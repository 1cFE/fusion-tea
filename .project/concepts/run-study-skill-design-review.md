# Concept-Design Review: run-study Capability

**Concept:** `.project/concepts/run-study-skill-design.md`
**Review File:** `.project/concepts/run-study-skill-design-review.md`
**Date:** 2026-08-19
**Status:** Closed 2026-08-19 — both rounds' dispositions applied; owner accepted the revised design directly ([OWNER] 2026-08-19, waiving a third review pass)

## Evidence Basis

- `.project/concepts/run-study-skill.md` supplies the owner-originated obligations: short-prompt execution, indicators that inform rather than gate, temporary glue, cold pickup from committed records, and durable process-improvement homes.
- `.project/concepts/study-driven-model-development.md` establishes discovery inside orchestration and the discovery log as an owner-settled deliverable. Its deterministic outer loop and full input taxonomy remain challengeable agent proposals.
- `.project/active/demo-proof-of-life/plan.md` and `exploration/stellarator_e2e/study/run_design_search.py` prove one disciplined route. They also show its exact temporary dependencies: a loader exception, two modified sealed artifacts, injected fields, explicit fan-out groups, and `PreparedListStrategy`.
- `.project/active/demo-study-parameterization-policy/policy.md` requires causal axes, complete fan-out, stock study execution, and honest model-gap reporting. It remains a draft under a temporary `.project/active/` path.
- The generated package provides qualified keys, module wiring, constraint predicates, and entry types. It still does not provide source-attribute identity. Explicit axis groups are therefore an honest fallback, not a mechanical completeness proof.
- The era teax CLI owns store creation, run/resume, compatibility, and query, but its config always builds `GridStrategy` and its loader path always constructs `ProvisionalPackageLoader` (`study/config.py:47-59,112-140`; `study/cli.py:30-43`). Coherent fan-out groups and the current package route require the direct API with `PreparedListStrategy` and `GlueAwareLoader`.
- Teax binds a store to the full compatibility tuple, including executable, model-contract, study-definition, schema, and strategy identity (`study/compatibility.py:12-21`). Cross-fingerprint comparison is caller-owned and must show the boundary it crosses (`docs/evaluation-and-study.md:226-240`).
- The current adapter accepts changed `pipelines/mfe_stellarator.yaml` and `inputs/system_design.json` but returns the seal's original executable fingerprint (`run_design_search.py:155-184`). Their current hashes differ from the sealed hashes in `package_contract.json:66,129`, while the returned fingerprint remains the value at line 150.
- `modeling_project/ARCHITECTURE.md` has no live conflict. AD-002 is relevant precedent for machine-readable metadata but supplies no current fan-out identity. `.project/adr/` and `adr.sh` remain absent, so the software ADR candidates cannot yet be filed.

## Fundamental Assessment

**Judgment:** Concerns

### Are we actually solving the right problem?

Yes. The gap is still a repeatability and evidence problem, not a missing sweep engine. A future agent needs a reliable way to choose and declare axes, see what the model can structurally resist, execute through teax, verify independently, and leave a record another agent can interpret without session memory.

The revision now keeps the important evidence classes separate:

- **Intended semantics:** indicators are facts, judgment stays with the user and agent, and the record is the cold-pickup contract.
- **Current behavior:** the only working route still combines package workarounds, prepared proposals, execution, and verification in one script.
- **Preservation evidence:** byte-equal CSVs can prove a refactor preserved that route. They cannot prove that the route has a truthful teax lineage identity or that a cross-lineage A/B comparison has matched semantics.

### Architecture verdict

The revision materially improves the design. The original C1 and C2 blockers are resolved: axis groups are explicit qualified keys with suffixes reduced to warnings, and records snapshot resolved facts instead of depending on mutable configuration. M1–M5 are also addressed in direction: `unresisted` is judgment, execution stays in teax, model findings have their own routes, mechanical failures fail closed, and the catch-all profile is split.

The design is not ready for epic decomposition because two load-bearing boundaries still contradict the platform:

1. **The temporary adapter does not own a truthful effective executable identity.** It permits changed executable inputs and returns the old sealed fingerprint. A record-level glue ledger preserves history for a reader, but teax uses the fingerprint during store open and resume. Different adapter/package behavior can therefore present as the same lineage before the record exists.
2. **The A/B store contract conflicts with itself and with teax's compatibility unit.** The record section says each arm has its own store (`run-study-skill-design.md:128-129`), while the flow puts two input-only arms in one store (`:175-176`). The actual boundary is one store per complete compatibility tuple, not merely per executable fingerprint. For two executable lineages, the record also needs an explicit constraint-correlation rule because teax does not join them.

The smallest revision is not a new runner. Give the temporary route an effective identity that covers every modified file and adapter-supplied behavior; state when the runbook uses the CLI versus a study-local direct-API definition; move adapter-specific checks back to the adapter; and make the A/B record rule use the full teax compatibility tuple. Then the four-home architecture is coherent.

## Ponytail Challenge

1. **Does it need to exist?** Yes, as a thin orchestration capability. The owner requires the skill, runbook, policy, mechanical checks, short-prompt execution, and cold-readable record. A second study framework does not need to exist because teax already owns execution and storage.
2. **Delete instead of accommodate.** Do not promote the proof-of-life's temporary loader/glue as permanent capability machinery. Freeze the historical script. Remove responsibilities from generic preflight and verification when their only implementation is package-specific. Avoid a fixed review-pass count.
3. **Invariant being compensated downstream.** Every executable input and adapter behavior that can change results must participate in the teax lineage identity. The adapter currently bypasses the seal and returns its original fingerprint. A later record cannot repair store compatibility. Complete fan-out identity still belongs upstream in the generated contract; explicit groups are only the honest fallback.
4. **Abstractions to remove or narrow.** Challenge `preflight.py`, `verify.py`, executable `manifest.py`, the adapter as a reusable component, a mandatory pass count, and speculative ADR filing. In particular, dead-filler checks belong with the adapter that owns those fillers, and a package-owned verifier should not be hidden behind an invented one-consumer protocol.
5. **Smallest sound architecture.** Keep the skill, short runbook, one stable policy, immutable record/discovery log, and one static-path tool. Use `teax-study` for true Cartesian grids and a small study-local `StudyRunner` + `PreparedListStrategy` definition for coordinated blocks. If the temporary adapter must remain, make it package-local, self-checking, and part of the effective identity. Emit possible paths, not proven positive responses.
6. **Verdict: `CHALLENGE`.** The revision improves the record and grouping boundaries, but the adapter still sits outside executable identity, the A/B store rules conflict, and positive module-level paths are described too strongly.

### Disposition

**Accepted in its central claim.** The executable-identity and A/B compatibility findings are supported directly by the adapter and teax code. They require design changes, so this re-review cannot Approve.

Several deletion recommendations are rejected with evidence:

- The adapter cannot simply be dropped while the input concept explicitly requires the capability not to depend on the timing of expected package fixes. It may remain only as temporary package-local code with a correct effective identity and deletion condition.
- Independent verification and reusable mechanical gates are owner-required quality-floor behavior. Teax does not provide oracle parity, stratified sampling, axis-group validation, or a baseline assertion. The generic tools may remain if their protocols and ownership are narrowed to those exact gaps; adapter-specific checks do not belong in them.
- A small data-only manifest is justified if it prevents the same stable package facts from being repeated across the surviving tools. The current executable `manifest.py` and its mix of package catalog with study choices should be reshaped, not assumed.
- The ADR candidates describe durable cross-component decisions. Missing filing infrastructure postpones filing; it does not erase the decisions.

The challenge to the fixed review count is accepted. The runbook should require named review outcomes and dispositions, not a ceremonial number of passes.

## Dimensional Review

### 1. Semantic Model — Concerns

Explicit axis groups, cold records, search-versus-sensitivity framing, and separate model/process findings now represent the source problem directly.

Module-level tracing is conservative. Because the tool treats every module output as depending on every module input, a positive path proves only possible reachability. Rename `constraints_responding` and `objectives_responding` to `reachable_*` or `possible_*`. `no_constraint_response` remains a sound negative only if the report explains that it is derived from absence of even a conservative path.

### 2. Responsibility and Invariant Ownership — Fail

Teax owns store lineage and resume safety, so every behavior-changing adapter input must affect the compatibility identity before a store opens. The current adapter returns the old fingerprint after permitting changed executable artifacts.

The temporary split also leaks: the adapter is the sole owner of glue, while generic `preflight.py` must know which fillers are dead and is forbidden to read the adapter (`run-study-skill-design.md:115-126,157-167`). Put those checks with the adapter or define one narrow package-owned command seam.

The policy is meant to be a durable rulebook but still lives under `.project/active/`, with permanent ownership/path deferred to epic planning (`run-study-skill-design.md:112-114,228-234`). Name the stable post-ratification owner before decomposition, even if the move occurs at Item-5 Align.

### 3. Simplification and Deletion — Concerns

Deleting the proposed generic runner is a real simplification. Keeping execution in `StudyRunner` also preserves teax's lease, resume, compatibility, and query semantics.

The remaining tool bundle is still broader than its ownership permits. Generic preflight should not contain temporary-package assertions. Verification should stay thin around a documented package-owned command and common sampling/result comparison, or remain package-owned until a second implementation proves the protocol.

### 4. Abstraction Quality — Concerns

The skill, runbook, policy, record, and indicator tool each have a distinct reason to exist. A small shared manifest can also be justified.

`manifest.py` is executable Python described as declarative. Prefer a data-only format unless executable behavior is proven necessary. Separate stable package catalog data (ties, available objective channels, oracle entry point, package identity) from per-study choices (selected objectives, baseline/window, axes).

The CLI and direct API are not interchangeable abstractions. The CLI always builds a Cartesian grid with the stock loader. Coordinated fan-out groups and the current adapter require a direct `PreparedListStrategy` definition. The runbook must select between those routes explicitly without adding a generic runner.

### 5. System Confidence — Fail

The revised proof obligations are useful, but promotion equivalence does not protect resume identity. The adapter's effective fingerprint must change whenever its allowed modified files or behavior changes.

The A/B proof also needs one rule: each arm points to the store identified by its complete compatibility tuple. Same-definition prepared blocks may share a store. Different tuples do not. Cross-fingerprint constraint comparisons must state the tracking key/name, predicate difference, and fingerprint boundary.

### 6. Decisions and ADR Candidates — Concerns

The candidates are load-bearing and their provenance is honest. No live ADR conflicts exist.

They need the revisions below before filing: effective adapter identity and CLI/API route ownership in the capability-factor decision; conservative path terminology in the indicator decision; data/temporary-code separation in the package-facts decision; and full compatibility-tuple plus correlation semantics in the record-location decision.

### 7. Comprehension — Pass

A cold reader can explain the problem, the four durable homes, and why teax remains the execution owner. The revision is explicit about limitations and proof obligations. The remaining confusion is localized to the adapter route and A/B store wording.

## Issues by Severity

### Critical

- **C4 — The adapter can falsify teax lineage identity.** It accepts changed sealed artifacts but returns the original executable fingerprint. Define an effective identity covering the original seal, actual allowed-file digests, adapter revision, and any behavior-changing supplied values/code; bind the store to it before run/resume. A record snapshot is not a substitute.
- **C5 — The A/B store contract is contradictory.** Replace “one store per executable lineage” and “each arm has its own store” with one store per full teax compatibility tuple. State when same-definition arms share a store and how two-lineage constraints are correlated across fingerprint and predicate boundaries.

### Major

- **M6 — The adapter/preflight execution boundary has no coherent owner.** Stock `teax-study` cannot inject `GlueAwareLoader` or build coordinated prepared blocks. Generic preflight cannot assert adapter-owned dead fillers while never reading the adapter. Name the direct-API route and move temporary checks to the package-local adapter or one narrow command seam.
- **M7 — The durable policy has no durable owner or path.** Resolve the post-ratification home and which epic owns the move/ratification before decomposition. A long-lived skill cannot permanently cite an active-work path that will move on close.
- **M8 — Positive static paths are overclaimed as response.** Report conservative reachability/possible paths. Reserve “responds” for executed or finer-grained evidence. Preserve the sound negative and the agent's separate `unresisted` judgment.

### Minor

- **m3 — Make the manifest data-only and split package facts from study choices.** Avoid an executable configuration module unless the spec proves it is needed.
- **m4 — Require review outcomes, not `≥3` passes.** Keep correctness, honesty, and readability obligations, but let one review satisfy multiple lenses when evidence supports it.

## ADR Candidate Assessment

- **Study capability factors into skill + runbook + policy + tools; judgment stays in the agent — keep, reshape.** Add explicit CLI-versus-direct-API route ownership and effective adapter identity. Provenance `[OWNER]` remains correct.
- **Axis groups are declared; response is derived — keep, rename.** Explicit groups and advisory suffixes are sound. Record conservative reachability, not proven positive response. Provenance `[AGENT]` remains honest.
- **Package facts split into manifest + temporary adapter; records snapshot — reshape substantially.** Keep stable data separate from temporary code, make the adapter part of effective identity, and keep its checks with it. The record remains the historical seam but cannot replace runtime compatibility.
- **Study records live beside the package; PM systems cite them — keep, amend.** Add the full compatibility tuple per referenced store and cross-fingerprint correlation semantics. Provenance `[AGENT]` remains honest.

## Resolutions

### Prior review, incorporated in the 2026-08-19 revision

- **C1 — resolved.** Axis groups are explicit qualified keys; suffixes are warnings only. Mechanical completeness remains an upstream limitation stated honestly.
- **C2 — resolved.** Records snapshot resolved facts; administrator mode reads only the record; synthesis is separate.
- **C3 — partially resolved.** The conditional one-lineage/two-lineage model is directionally correct, but C5 remains because the store wording conflicts and uses only executable identity.
- **M1–M5, m1–m2 — resolved in direction.** The revision separates fact from judgment, retains teax execution, splits finding routes, fails closed on mechanical errors, separates manifest/adapter, separates synthesis, and relocates annexes. M6 and M8 capture the remaining boundary precision.
- **Previous ponytail challenge — incorporated in part.** The mutable profile and generic runner were removed; explicit groups and immutable snapshots were adopted; surviving tools received named gaps.

### Re-review findings — resolved 2026-08-19 (second application pass)

- **C4 — accepted.** The adapter computes an effective executable fingerprint — digest of (sealed fingerprint, allowed-modified files' actual digests, adapter source) — and the study definition binds to it; store open/resume refuses on any glue or adapter change. Negative test added (touch a glue file → resume refused). Design invariant marks today's sealed-fingerprint reuse as the named defect.
- **C5 — accepted.** Store rule is one store per complete teax compatibility tuple; same-definition arms share, any tuple difference separates; cross-fingerprint correlation stated in the record (constraint matched by definition qualified name + local identity, predicate diffs disclosed, boundary named). Contradictory wording removed from both the record section and the flow.
- **M6 — accepted.** Two execution routes named (CLI for Cartesian grids on stock-loadable packages; study-local direct-API definition for coordinated blocks and the adapter route — the era CLI cannot inject a loader or build prepared blocks); dead-filler and other adapter-owned checks moved into the self-checking adapter; generic preflight keeps only generic gates.
- **M7 — accepted.** Post-ratification home named: `modeling_project/STUDY_POLICY.md` (`[AGENT]`, override at the Item-5 Align); ratification stays with the Align (demo epic); the capability epic owns the move and citation updates.
- **M8 — accepted.** Fields renamed `constraints_reachable` / `objectives_reachable`; positives described as conservative possible paths; `no_constraint_response` kept as the sound negative with its derivation explained; "responds" reserved for executed evidence.
- **m3 — accepted.** Manifest is data-only (`manifest.json`), package catalog only; per-study choices live in the study definition and record.
- **m4 — accepted.** Runbook requires named review outcomes (correctness, honesty/claims, readability) with verdicts and dispositions; one review may satisfy multiple lenses; the ≥3 count (session-plan provenance, not owner-graded) is dropped.
- **Fresh ponytail challenge — accepted in its central claim; its deletion recommendations stand dispositioned above (adapter kept as temporary package-local code under the effective identity; verification and generic gates kept at their named gaps; data-only manifest kept; ADR filing postponed, not erased).

## Verdict

**Revise**

The revision fixes the original grouping and cold-record blockers and substantially improves the architecture. It still cannot move forward while the temporary execution route can reuse a false executable identity and the A/B record gives conflicting store rules. These are narrow corrections to the current shape, not a reason to rework the capability from scratch.
