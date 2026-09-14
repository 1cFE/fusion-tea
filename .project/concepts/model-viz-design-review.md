# Concept-Design Review: Model Visualization Tool

**Concept:** [model-viz-design.md](model-viz-design.md)
**Review File:** `.project/concepts/model-viz-design-review.md`
**Date:** 2026-09-13
**Status:** Focused re-review complete. Architecture concerns resolved; two documentation corrections remain. Review judgments are `[AGENT]`; the owner supplied the revision summary and requested verification, not final acceptance.

## Focused Re-review — 2026-09-13

**Judgment:** Sound architecture. **Verdict:** Revise, limited to the two corrections below.

Checked the revised concept against the existing findings and spot-checked the snapshot. No new architecture work or review round is needed. The original independent ponytail challenge is incorporated: the browser reads the snapshot directly, with no Python conversion or intermediate file.

| Finding | Result |
|---|---|
| M1 — input and inspection contract | Substantively resolved: defaults, missing-formula labels, and output-port reverse indexing are explicit. Correct the two wire shapes below. |
| M2 — grouping and containment | Resolved: separate source-group and occurrence identities; display parent derives from the selected mode; occurrence containers include ancestors. |
| M3 — collapse and navigation | Resolved at design level: extension named, bidirectional group edges acknowledged, hidden-target reveal specified, checks carried forward. Implementation still must demonstrate them. |
| M4 — browser-direct loading | Resolved; ponytail challenge incorporated. File input is the baseline. |
| M5 — provenance | Conflict is surfaced and overlay support remains. Agent proposals still sit under a settled heading; correct that heading below. Original overlay authority remains explicitly unresolved. |
| m1 — counts and terminology | Resolved: 150 producer bindings, 140 calc pairs, full-path source groups, design-file groups acknowledged. |
| m2 — formula honesty | Resolved. The revision's 65 documentation-bearing lists is correct: 64 use `Documentation:`, while `calendar` uses `See documentation:`. The initial review's count was too narrow. |

### Remaining corrections

1. **Projection Function → Input edge classification:** the actual parameter shape is `{kind: "node", target: "<NodeId string>"}`, not `target: {attr}`. The actual literal shape is `{kind: "literal", value: 1000.0}`, not `target: {value}`. Correct these two table cells so implementation follows the serialized data.
2. **Next-Stage Handoff:** rename “Settled here” to “Decisions and proposals,” or move the agent-grade entries outside that heading. Adding `[AGENT]` does not make an agent proposal settled. Keep the existing overlay provenance note pending owner resolution.

Both are documentation fixes. The explicit “No formula available” behavior is a reasonable architectural treatment of missing metadata; final owner acceptance of the concept remains separate. The earlier ADR recommendation is adequately addressed by the revised snapshot-boundary rationale; no ADR filing is needed here.

### Verification

Read the revised concept and checked node/literal wire shapes and documentation-list coverage directly in the same stellarator snapshot using a read-only standard-library JSON probe. No implementation or browser validation is claimed. The original evidence and challenge below are retained as the initial review record, not current open findings.

## Initial Review Record

## Fundamental Assessment

**Judgment:** Concerns

### Are we actually solving the right problem?

Yes. A modeler needs to see which calculations feed one another and inspect each calculation's direct inputs, outputs, and available implementation text. The source concept's owner statements ask for behavioral relationships and inspection; its one-hop scope does not require path tracing. Reading codegen's resolved graph is an appropriate boundary. The viewer need not resolve SysML bindings again.

The proposed reader/viewer split is viable, but the description overstates what the chosen fields guarantee. The real snapshot contains defaulted inputs outside the proposed three edge kinds and computed calculations without formula text. Grouping and collapse also change the displayed graph; their correctness needs an owner beyond the layout engine.

### Architecture verdict

Retain the snapshot-based direction and revise its contracts before decomposition. The six fundamental questions resolve as follows:

1. **Problem:** Navigation and inspection are the right semantic gap. Missing display metadata must remain visible as a gap rather than become an exemption for computed nodes.
2. **Ownership:** Codegen owns resolved computation semantics. The viewer's projection owns faithful representation, and its interaction code owns preserving relationships through collapse and selection. No upstream binding repair was identified by this review.
3. **Existing pipeline:** Syside extraction and FastAPI are not necessary for the new DAG path. The design correctly allows that path to be static. Structural migration remains a separate obligation with a different producer.
4. **Coherence:** One browser projection can provide this capability without a conversion command or another persisted format. The proposed extra JSON boundary has no identified second consumer.
5. **Abstractions:** A projection function and detail panel are necessary. A separately versioned viewer interchange format is not yet justified. Compound containers are useful, but one renderer parent cannot independently represent two containment schemes.
6. **System behavior:** The raw-edge lookup is feasible; collapse, output-port indexing, missing metadata, and overlay placement still need explicit contracts and checks.

These are bounded revisions to a useful system shape, not evidence that the whole approach needs replacement. The extra conversion step is removable scaffolding, not compensation for an upstream semantic defect; the fundamental stop condition does not apply.

## Source Problem and Evidence

### Source summaries

- [Source concept](model-viz.md): captures the behavioral graph, direct inspection, snapshot-only DAG input, structural migration, and overlay readiness; its overlay authority labels conflict internally.
- [September calc-DAG research](../research/20260912-004633_calc-dag-visualization.md): identifies the resolved snapshot and root-only calc scopes, but simplifies the input taxonomy and metadata coverage too far.
- [January visualization tools survey](../research/20260116-161342_sysml-v2-visualization-tools.md): surveys broader modeling tools; historical product prices and capabilities do not establish this viewer's feasibility.
- [January visualization strategy](../research/20260118-180847_sysmlv2-visualization-strategy.md): recommends projection and separate views, identifies binding extraction risk, and proposes Cytoscape; it predates the snapshot-based approach.
- [Design-intent README](../design-intent/README.md), [concepts](../design-intent/concepts.md), [requirements](../design-intent/requirements.md), [personas](../design-intent/personas.md), and [user stories](../design-intent/user-stories.md): describe a broader browser experience for engineers and stakeholders; these historical ambitions are context, not newly imposed requirements.
- [Historical extraction API](../design-intent/technical/extraction-api.md) and [tool research](../design-intent/technical/tool-research.md): describe structural/cost/dependency projections and renderer formats; the old strategy's `abstraction-interfaces.md` and `data-shapes.md` references have been consolidated into the extraction API.
- [POC README](../../proof_of_concept/README.md): documents an existing standalone Cytoscape shell with compound nodes, expand/collapse, and an information panel.
- [ADR index](../adr/INDEX.md): ten live decisions, none governing visualization. ADR-0003 was read in full; its lean-first ruling governs goal-control machinery, so it is precedent rather than a binding ban on a viewer adapter.
- `.project/CURRENT_WORK.md` and `CLAUDE.md`: establish project context, the two PM systems, and local tooling; the product ledger's sole promise concerns goal execution, not this viewer. No model-viz product-design sibling exists.

### Intended semantics

[INHERITED: model-viz.md, Owner's Words and Next-Stage Handoff] Direct I/O and calculation inspection are v1; data comes from snapshot JSON without a codegen import. [EXAMPLE] “how does major radius affect LCOE?” illustrates navigation; it does not make multi-hop tracing a v1 requirement. The original implementation-inspection quote survives by path to the source concept's Owner's Words section.

### Current behavior

Read-only JSON checks used `exploration/stellarator_e2e/stellarator.snapshot.json`, SHA-256 `c9f6e2a52ea69cf95dcee015496f906f705d1130bce1a529bde510299a5ce393`, nested schema `instance-graph/v3`:

| Observation | Result |
|---|---|
| Populations | 76 calcs, 292 attributes, 14 occurrences, 14 constraints |
| Source-file groups | 17; largest has 33 calcs |
| Calc input records | 150 producer, 234 node, 10 literal, 52 null edges |
| Producer identity checks | All 150 targets match a calc and an output port; 140 distinct calc pairs |
| Null-edge inputs | All 52 have a non-null `metadata.default_value` |
| Scope | Every calc has the same root occurrence scope |
| Formula coverage | 11 computed nodes have empty `calc_expressions`; 65 other nodes contain documentation text among their expression strings (count corrected during focused re-review) |
| Group meaning | 11 nodes come from design files, not analysis modules |
| Collapsed graph | Four source-group pairs have dependencies in both directions |

These measurements came from iterating calc input records, comparing producer targets to the source calc's `outputs[].port`, and grouping the exact `source_file` values. The raw snapshot remains the reproducible fixture; counts are observations, not universal acceptance constants.

Upstream serialization already writes IDs as strings and carries port metadata: [codec](../../../sysml-codegen/src/sysml_codegen/snapshot/instance_graph.py), `_input_records` at line 340 and `_calc_to_data` at line 523. Graph validation belongs upstream: [encoder](../../../sysml-codegen/src/sysml_codegen/snapshot/instance_graph.py), line 1033. The current structural extractor recurses through part usages: [visualization.py](../../proof_of_concept/extraction/visualization.py), line 292. Its [types.py](../../proof_of_concept/extraction/types.py), line 17, imports syside, so importing those types would violate the new DAG path's dependency boundary.

### Preservation evidence and limits

No implementation or browser trial was performed. Existing POC support establishes reusable code, not successful rendering of this calc graph. Zero unresolved producer references establishes referential consistency of this fixture; it does not prove complete panel contents, correct grouping, or navigable collapse. No byte-stability or regression claim substitutes for those obligations. This review checked the relevant local evidence and primary renderer/browser documentation; it did not revalidate the historical surveys' unrelated commercial-tool comparisons.

## Ponytail Challenge

A fresh subagent read the ponytail skill and applied its deletion-first ladder at ultra intensity. Its written architectural conclusion:

1. **Necessary machinery:** Snapshot loading, a small in-memory projection, graph rendering, and the detail panel. IDs are already serialized strings; Python provides no unique normalization capability.
2. **Existing machinery to delete or avoid carrying forward:** Reuse the standalone POC's page shell, graph setup, and expand/collapse extension. Remove its hardcoded fixture and structural-only controls from the DAG surface. Keep FastAPI model loading outside this static-file path.
3. **Invariant ownership:** Codegen owns semantic binding resolution and graph validity; browser projection owns faithful IDs, edges, grouping, and readable errors; interaction code owns collapse and selection.
4. **Removable abstraction:** A persisted `{nodes, edges, groups}` format adds a second contract without a second consumer. Project directly to Cytoscape elements and retain raw calc records for details.
5. **Smallest architecture:** One static page, a directly testable JavaScript projection function, a file input, and graph libraries. Keep requested overlay support and structural migration; simplify their implementation. Structural extraction may remain a separate producer when migrated.
6. **Verdict: CHALLENGE.** Remove the separate conversion command and derived JSON file from the default architecture. The 52 null edges still require explicit projection logic; deleting the file must not delete that logic.

Evidence: [codec](../../../sysml-codegen/src/sysml_codegen/snapshot/instance_graph.py), line 523; [standalone POC](../../proof_of_concept/cytoscape_demo.html), lines 153, 340, and 357; [existing types](../../proof_of_concept/extraction/types.py), line 17.

### Disposition

**Accepted by reviewer.** Recommend raw snapshot → browser projection → viewer as the default. This is an agent recommendation awaiting owner engagement, not an owner decision. A concrete second consumer could justify an export later. The accepted challenge prevents Approve until the concept incorporates it or an evidence-backed alternative resolves it. It does not remove structural migration or overlay support from scope.

## Dimensional Review

| Dimension | Assessment | Basis and recommendation |
|---|---|---|
| 1. Semantic Model | Concerns | Defaulted inputs and computed nodes are real members of the model. Define their display semantics; distinguish 150 bindings from 140 calc pairs. See M1. |
| 2. Responsibility and Invariant Ownership | Concerns | Upstream semantics are correctly owned, but renderer projection and interaction guarantees need named owners. Separate source grouping, occurrence ownership, and active display parent. See M2–M3. |
| 3. Simplification and Deletion | Concerns | Static loading is appropriate. Resolve the removable conversion step now; reuse the POC shell without importing its model loader. See M4. |
| 4. Abstraction Quality | Concerns | Calc identity and direct I/O are good abstractions. The persisted viewer schema is premature, and `parent` is overloaded. See M2 and M4. |
| 5. System Confidence | Concerns | Raw counts and a two-scope fixture do not prove visible edge preservation or hidden-target navigation. Add focused seam checks. See M3. |
| 6. Decisions and ADR Candidates | Concerns | No relevant live ADR conflict. The ungraded settled list promotes design bets, and inherited overlay authority is inconsistent. See M5. |
| 7. Comprehension | Concerns | The proposal is readable, but “every formula,” “analysis module,” and “no unowned proofs” overstate verified facts. Amend those claims rather than adding caveat sections. |

## Issues by Severity

### Critical

None. No fundamental semantic-owner inversion or need to replace the snapshot direction was established.

### Major

- **M1 — Complete the inspection contract for the actual snapshot.** The proposal's Snapshot Reader and Detail Panel sections omit null edges, port-level reverse lookup, and empty formula lists. [EXAMPLE] `fuel.s_per_fpy_in` has `edge: null` with default `31536000.0`; it is neither an unresolved producer nor an inline literal. Eleven computed nodes, including `total_capital`, have no `calc_expressions`. Keep each input and identify declared defaults explicitly; resolve node inputs against attributes; index output consumers by calc ID plus output ID. Define absent formula behavior before claiming every click exposes implementation. Recommend using an existing readable serialized expression when available and labeling its representation. If the needed text is absent, park the universal inspection claim and decide between an upstream metadata improvement and an explicitly reduced promise. Do not introduce a viewer-side SysML compiler to fill it. Verification should cover a defaulted input, a computed node, and a producer with multiple output ports.
- **M2 — Give grouping and containment separate meanings.** Viewer line 92 uses Cytoscape `parent` for source groups; Structural Overlay line 104 says parents are null today and later name occurrences. Those cannot both describe the active renderer parent. The source concept explicitly describes switching grouping modes. Preserve source-file group identity and occurrence identity, then derive one display parent for the chosen mode. Emit actual container nodes and their ancestors, using occurrence IDs rather than possibly repeated display segments. Verify two same-named subsystem instances and calcs from one source file placed in different occurrences. This is a correction to the promised overlay contract, not a request for another user-facing v1 feature. [Cytoscape compound-node documentation](https://js.cytoscape.org/#notation/compound-nodes).
- **M3 — Own collapse and selection correctness.** “Cytoscape + dagre” does not itself specify the expand/collapse behavior. The POC already uses a separate extension at `proof_of_concept/cytoscape_demo.html:16`. Name the extension or application code responsible for projecting edges to visible containers, retaining their original endpoints, and revealing a target hidden in a collapsed group before selecting it. The collapsed group graph is not a DAG: account-costs and generic-plant groups, for example, have edges both ways. Preserve these directions without implying a computational cycle. Add a collapse/expand round-trip assertion over the original port bindings and a hidden-target navigation check. Layout quality remains a separate manual trial. The extension documents meta-edges and direction handling in its [primary documentation](https://github.com/iVis-at-Bilkent/cytoscape.js-expand-collapse#elements-style).
- **M4 — Resolve the loading boundary and remove the extra file.** Opening the viewer currently requires a conversion command, while the handoff leaves direct browser reading undecided. Accept the ponytail simplification: one raw snapshot load and one in-memory projection. Choose file input as the baseline serverless route. A URL parameter naming an arbitrary local file is not a portable substitute for user-selected file access; ordinary fetch is subject to browser origin rules. Remove that promise or qualify it as an HTTP-hosted route. See [MDN's local-file explanation](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS/Errors/CORSRequestNotHttp#loading_a_local_file).
- **M5 — Repair decision provenance before this becomes downstream authority.** The design's Next-Stage Handoff marks all choices settled without grades. Snapshot input and direct I/O have owner attribution in the source; grouping, renderer choice, static serving, and follow-on timing must retain agent/inherited grades unless owner-originated evidence exists. More significantly, the source's Owner's Words calls overlay readiness an agent inference, while its handoff labels it OWNER. Record the conflict and seek the owner's resolution; do not silently downgrade or strengthen the requirement. Keep supporting the recorded overlay promise while its attribution is unresolved. Structural migration timing may be proposed as follow-on because the source explicitly allows that sequencing.

### Minor

- **m1 — Correct fixture and vocabulary claims.** Replace ~178 with the observed binding count where this fixture is meant, retain 76 as fixture data rather than a universal count, and describe groups as source-file groups because two groups come from design files. A shortened filename is a label; use the full source referent as group identity to avoid merging same-basename files.
- **m2 — Display formula metadata honestly.** Sixty-five expression lists include documentation text (count corrected during focused re-review). Do not present every entry as executable math or equate a snapshot specification with executed Python. Render available text faithfully and distinguish unavailable content; no new formula language is necessary.

## ADR Candidate Assessment

- **Snapshot JSON as the DAG boundary: reshape the rationale for not filing.** Keeping this decision in the concept may be sufficient for one small tool, but “a future agent would not plausibly re-derive the wrong thing” is unsupported. The January strategy explicitly proposed syside extraction. Carry the source's owner attribution and record why the DAG uses the resolved snapshot while the existing structural extractor has a different input. Reconsider a durable ADR when migration makes that seam live across both paths.
- **Cytoscape/dagre, browser-side projection, and follow-on migration timing: drop as ADR candidates for now.** These are local, revisable implementation or sequencing choices. Keep their reasoning in the concept with agent provenance.
- **Grouping versus occurrence ownership: reshape as an explicit concept invariant first.** Resolve M2 before deciding whether it deserves an ADR. No live ADR amendment or supersession is identified; none was filed.

## Resolutions

The owner supplied a finding-by-finding revision summary and requested a focused re-review. The checked outcomes are recorded at the top of this document. M2–M4 and m1–m2 are resolved; M1 and M5 need only the two stated documentation corrections. The accepted ponytail challenge is incorporated. No final owner acceptance or resolution of the original overlay attribution is inferred.

## Verdict

**Revise — documentation only.** Correct the two input wire shapes and the settled heading. The architecture can stand; no additional machinery or broader review is requested.
