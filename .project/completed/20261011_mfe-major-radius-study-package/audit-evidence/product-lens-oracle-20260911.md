# Independent product-lens oracle — 2026-09-11

Written before reading WORK or its diff. Sources read: `.project/product/INDEX.md` → promise 0001 Authority → owner-verbatim in `.project/concepts/goal-driven-model-development-harness.md` § Owner's Words; `README.md`; `.project/adr/INDEX.md`, ADR 0009 and ADR 0010; targeted operator-contract lines in `docs/integration_seam_operator_guide.md`. Item spec/design/plan and prior review framing have not been read.

Point: A non-builder must be able to run an operator-chosen study through documented native artifacts, with clean patterns and explicit failures that make revisiting the model possible. Source: `.project/concepts/goal-driven-model-development-harness.md` § Owner's Words (“I just want really good documentation and clean patterns so that it can be easily operated and managed by a human.”; operator “shouldn't have to be me (who built this and therefore is mostly familiar)”; “shouldn't be limited to the 'Item 6' or any other pre-defined things”). Grade: `[OWNER-VERBATIM]` for those requirements; applying them to this new study package is `[AGENT]` inference.

Falsifier: A fresh caller executes the package's documented baseline and a changed major-radius point through the supported route, but cannot obtain correctly identified outputs or diagnose refusal without builder knowledge or manual changes to parallel graph representations.

Supporting obligation: Integration must report a verified candidate only when the already-produced package is a fixed point and its execution passes meaningful verification. Source: `docs/integration_seam_operator_guide.md:3-15` (`[INHERITED]`); `.project/adr/0009-integration-is-a-fixed-point-proof.md` (active `[AGENT]` decision). Falsifier: an altered pipeline changes a consumed constraint binding yet still passes verification and produces a candidate.

Authority boundary: ADR 0010's owner carry/demo-only rulings explicitly concern the stellarator handwritten oracle. Its arithmetic-independence rationale is `[AGENT]`; it is evidence to assess this work, not an owner ruling requiring a new per-concept permanent mirror.
