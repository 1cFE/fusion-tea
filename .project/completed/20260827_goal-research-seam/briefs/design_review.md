# Brief → /_my_design_review — goal-research-seam (GSTH Item 2)

Review `.project/active/goal-research-seam/design.md` against `.project/active/goal-research-seam/spec.md` (approved). You are a fresh session; the authoring session is separate. Context: `align.md` (owner rulings), `spec-review.md` (why requirements read as they do), epic § Item 2.

The design claims empirical grounding — it says it ran `agentic-mbse extract` and verified the frontmatter-hash contract, the missing `raw.pdf` on the local-PDF path, and the `file://` rejection. **Spot-check the load-bearing code claims yourself** (`zotero_ingest.py`, `zotero_lib.py`, `extract_cli.py` line refs, `SOURCE_INDEX.md` headings, PROTOCOL.md structure): a design built on a misread of the code fails at plan time.

Review dimensions:
1. **Requirement coverage** — every R-* in the spec has a design home; every invariant in the spec's return-class table is realizable from the design's mechanisms. Check especially R-D6 (negatives *block* silent repeats — is the bookkeeper's `open`/`close` structure actually binding, or can a caller bypass it by invoking `source_registry.py` directly?), R-B9 (disk is truth), and R-A3.
2. **Contract consistency** — the registration op's own return vocabulary (it can return `DUPLICATE`) vs the spec's four seam return classes. Is the layering stated cleanly enough that the plan won't conflate them?
3. **Holdout safety** — D's `--holdout-ack` override: verify it maps to PROTOCOL.md's actual "documented-exception path" semantics and is refused for everything the protocol seals absolutely; verify fail-closed parsing is real. This is the highest-consequence area — be adversarial.
4. **Atomicity claims** — the commit order, failure ladder, and the acknowledged uncovered state (hard kill between manifest append and index insert). Is the ladder correct as stated? Is `verify` an adequate recovery path, and is it in first-build scope or deferred ambiguously (Next-Stage Handoff leaves it "open for the plan" — is that acceptable given the invariant list cites `verify`)?
5. **Compatibility** — key-tolerant manifest loaders before first non-Zotero row; Zotero batch path behavior preservation; the deliberate `--local-pdf` breaking change (D5) — sound, or does it need an owner flag?
6. **Engineering quality** — module boundaries, testability (injectable paths), the test plan's fixture strategy, anything over- or under-built against the epic's lean-first/hardening rule.

Do not read Item 1's in-flight artifacts. Deliver verdict and findings (must-fix vs advisory). End with `ARTIFACT: <path>`.
