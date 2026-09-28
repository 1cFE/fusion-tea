# Spec: Model Visualization — Structural View

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-09-13
**Complexity:** MEDIUM
**Branch:** feat/integrated

---

## Problem

The model viewer at `src/model_viz/viewer/` shows how numbers are computed: calcs and the bindings between them. It does not show where numbers are filed: which part owns which attributes, and how parts nest. The owner's question that started this concept was about exactly that, `[OWNER-VERBATIM]` (concept § Owner's Words): "can you explain to me why we don't have any organization or structure of the models?"

- **The containment tree has no surface.** The only structural viewer is `proof_of_concept/`, which needs syside and a Python server, and is no longer the live code.
- **The calc graph's Occurrence mode is not a substitute.** It draws only occurrences that hold a calc or sit above one, and it does not list a part's attributes. On the fixture, 3 of the 23 parts own no calcs (`magnet/casing`, `magnet/coil`, `magnet/winding_pack`) and are absent from that mode. Attributes appear only as parameter inputs inside a calc's panel, never under the part that owns them.
- **The data is already loaded.** The snapshot the calc graph reads also carries the occurrence tree and every attribute scoped to each occurrence. Nothing extra has to be parsed.

This item finishes v1 of the model visualization concept. Concept Success Criterion 4 and User Story US-4 were deferred out of the calc-graph item (`.project/active/model-viz/spec.md` § Non-Goals) and land here. `[OWNER]` (concept § User Stories, US-4): "I can switch between the structural view (part containment) and the calc DAG view in the same tool, so that I can see both how numbers are organized and how they are computed."

### Premise corrections found while probing (surfaced, not resolved silently)

The brief's ruling 4 rests on three data premises. Probing the fixture showed they do not hold as stated. The requirements below follow the data; the orchestrator should confirm this reading.

1. **A part's type name is not recorded.** The brief says a part's type name "is recoverable from any attribute it owns." It is not. The attributes of 14 of the 23 parts come from more than one declaring owner (`owner_qualified_name`). For example, `blanket`'s 18 attributes come from `mfe_subsystems::Blanket` (14), `costed_component::'Costed Component'` (2) and `cas_hierarchy::'CAS Account'` (2). On the root, 6 of 77 come from `stellarator_09::stellaris`, which is the part usage itself, not a definition. `effective_type_ids` holds 1, 4 or 5 bare ids per part, with no names and nothing marking which is the direct type. Picking one owner as "the type" would be a guess. So the requirement is: show each attribute's recorded declaring owner, and show the part's type as not recorded.
2. **No units are recorded.** Attribute records have no unit field, and 0 of the 450 calc inputs carry `metadata.unit`. "Units where recorded" is empty on the fixture.
3. **Most unset values are bound, not missing.** 181 of 377 attributes have a null `value`. 155 of those are aliases (`is_alias: true`) whose `alias_target` names where the value comes from: 143 point at a calc output, 12 at another attribute. The snapshot carries no computed values. The remaining 26 null values are non-alias (`cas_code` and `account_name` on 13 parts). A blank value cell would hide the difference.

## Success Criteria

Every criterion is observable in a real browser and checkable from pytest through Python Playwright, run as `uv run python -m pytest tests/model_viz -q`. Counts are for the fixture `exploration/stellarator_e2e/stellarator.snapshot.json` at SHA-256 `8e79aa4e489e7bcf1be8e24796a77a6df3acbbf8b327b3eb6b961e96b55bf9ae` (the pin in `tests/model_viz/viewer_harness.py:13`), verified by read-only JSON probes on 2026-09-13. They are fixture facts the tests compare against a Python reading of the raw file; the viewer must not hardcode them.

**Where structure is read from.** Every structural criterion reads what the renderer is currently displaying, queried from the live page. Reading the snapshot or the page's own projection instead would pass by construction and does not satisfy the criterion.

**Fixture facts used below.** 23 occurrences: the root `stellaris` (depth 0), 18 children of the root (depth 1), and 4 at depth 2 (`blanket/first_wall`, `magnet/casing`, `magnet/coil`, `magnet/winding_pack`). 22 parent-child relations. Three parts have children: `stellaris` (18), `magnet` (3), `blanket` (1). 377 attributes, every one scoped to an occurrence that exists, every one with `source_file` and `source_line`. 77 calcs, every one scoped to an occurrence that exists; the root owns 33 directly. Per part (attributes / calcs owned directly): `stellaris` 77/33, `blanket` 18/2, `blanket/first_wall` 15/3, `buildings` 14/1, `cryoplant` 17/2, `divertor` 18/2, `electric_plant` 7/1, `fuel_cycle` 22/3, `heat_rejection` 7/1, `heat_transport` 26/2, `heating` 18/2, `magnet` 16/13, `magnet/casing` 6/0, `magnet/coil` 16/0, `magnet/winding_pack` 10/0, `misc_plant` 7/1, `plasma` 25/4, `power_supplies` 8/1, `shield` 10/1, `structure` 8/1, `turbine` 19/2, `vacuum_pumping` 4/1, `vessel` 9/1. No part has zero attributes. Within a part, attribute names are unique.

**Views and switching**

- [ ] After one snapshot load, both the calc graph view and the structural view are available. The modeler can switch between them with a page control.
- [ ] Switching views does not re-read the file. The page's load sequence counter (`data-load-seq`) does not change across any number of switches, and both views keep showing the loaded snapshot.
- [ ] Switching to the structural view and back leaves the calc graph behaving as v1 specifies. The existing `tests/model_viz` suite passes unchanged in what it asserts.
- [ ] Loading a second snapshot replaces the data in both views. Nothing from the first snapshot remains in either view or in the panel, whichever view was active during the load.
- [ ] The v1 load errors still apply in both views: a wrong `schema_version` shows the error naming expected and found versions, a JSON file without `instance_graph.schema_version` and a non-JSON file each show a clear error, and neither view renders anything, whichever view was active.

**The structural view (stellarator fixture)**

- [ ] Every occurrence renders as a part: 23 part elements, one per entry in `instance_graph.graph.occurrences`, including the 4 depth-2 parts and the 3 calc-less magnet parts.
- [ ] The rendered containment matches the snapshot: each part's displayed parent is the part for its `parent_id`, giving 22 parent-child relations, and the root has none. The depth counts read from the page are 1, 18 and 4.
- [ ] Two parts with the same `display_segment` under different parents stay separate. Checked on a synthetic copy of the fixture, because all 23 segments are distinct on the fixture.
- [ ] No calc element appears in the structural view. Each part shows, or makes reachable in one click, the number of calcs it owns directly; the values match the per-part table above, including 0 for the three magnet parts.
- [ ] **Collapse round-trip.** Starting fully expanded, for each of the 3 parts with children: collapse it, then expand it. While collapsed, the part stays visible and all of its descendants are hidden. After expanding, the visible parts and their displayed parents are identical to before the collapse.
- [ ] **Nested round-trip.** Starting fully expanded: collapse `magnet`, collapse `stellaris`, expand `stellaris`, expand `magnet`. After each step the visible parts match the rule "a part is visible when none of its ancestors is collapsed," and after the last step the view is identical to the start.

**The part panel**

- [ ] Clicking a part in the structural view opens a panel for that part. It shows: the part's name (`display_segment`), its containment path from the root (for example `stellaris/magnet/coil`), its type as "not recorded" (see Premise correction 1), its direct calc count, and its attributes.
- [ ] The panel lists exactly the attributes whose `scope.wire` equals that part's `occurrence_id`: no attribute of a child part and no attribute of another part. On the fixture, the attribute count in the panel matches the per-part table for all 23 parts, and `blanket` lists 18.
- [ ] Each attribute row shows its name, its declaring owner (`owner_qualified_name`) and its recorded source location (`source_file:source_line`). All 377 rows across the 23 panels carry a source location.
- [ ] Each attribute row shows its value truthfully. A recorded value (183 numbers, 13 strings on the fixture) appears as recorded. An alias with a null value says where its value comes from: the producing calc and output for the 143 calc-bound aliases, the target attribute for the 12 attribute-bound aliases. The 26 non-alias null values are labelled as having no value in the snapshot. No value is guessed.
- [ ] A unit is shown when the snapshot records one. On the fixture none is recorded, and no unit appears.

**Evidence**

- [ ] A Playwright screenshot of each view on the stellarator fixture is saved as evidence: the calc graph view and the structural view, the latter with at least `magnet` expanded so the depth-2 parts show.

## Known Requirements

**Owner outcomes**

- **[NEED]** A modeler can switch between the structural view (part containment) and the calc graph view in the same tool. (Concept US-4; Success Criterion 4: the structural view "is served alongside the calc DAG view".)
- **[NEED]** The code lives at `src/model_viz/`, and the structural view becomes part of it rather than staying in `proof_of_concept/`. (Concept § Next-Stage Handoff: "Code lives at `src/model_viz/`. The existing structural view migrates in.")
- **[NEED]** The structural view shows how the model is organized: the part containment tree. (Concept § Owner's Words, the owner's question quoted in Problem; US-4 "structural view (part containment)".)
- **[INHERITED: concept § Next-Stage Handoff; `.project/active/model-viz/spec.md` § Known Requirements]** Calcs drawn inside subsystem containers stay an architecture capability of the calc graph (its Occurrence grouping mode), not a feature of the structural view. This item does not change it.

**Decisions this item rests on** (agent-grade, from the orchestrator's brief `.project/active/model-viz-structural-view/briefs/spec.md`)

- **[INFERRED]** **The structural view's data comes from the snapshot, not syside.** The syside extractor and the FastAPI server are not migrated; they stay in `proof_of_concept/` as reference. (Brief ruling 1.) The concept's literal words name the syside extractor moving to `src/model_viz/extractors/structural.py`, but that wording predates the finding that the snapshot carries the containment tree. Reason: keeping syside would buy multiplicity, which this model does not use, at the cost of a Python server, a second data source and a second serving model in one page. This reads the owner's "migrates in" as "the structural view moves into the tool," not "the syside code moves"; the brief records that the owner reaffirmed on 2026-09-13 that the producer is the orchestrator's call. The owner's data-source ruling (concept § Next-Stage Handoff: "Not syside") supports the reading independently.
    - Consequence: multiplicity is shown only if the snapshot ever records it. Today it does not, and every `occurrence_index` is null.
    - Consequence: `src/model_viz/` stays without Python, because this item adds none (v1 design D12; brief ruling 8).
- **[INFERRED]** The serving model is the v1 viewer's: one static page, the snapshot picked through the file input, no server, no network request. (Brief ruling 2; v1 design § Integration Strategy.)
- **[INFERRED]** The structural view is a second view in the same page. Both views read the one loaded snapshot, and switching between them is not a reload. (Brief ruling 3.)
- **[INFERRED]** Expand and collapse in the structural view follow the v1 mechanism: the visible structure is a pure function of the snapshot and a set of collapsed parts, and the renderer draws only what that function returns. The `cytoscape-expand-collapse` extension stays rejected. (Brief ruling 6; v1 design D1.)
- **[INFERRED]** Cost attributes are ordinary attributes and appear in the part panel with the rest. There is no separate cost extraction; the POC's `costs` field came from a `generate_costs` import that no longer applies. (Brief ruling 5.)
- **[INFERRED]** Missing data is labelled, never guessed. This carries the v1 rule (v1 design Appendix C) to parts and attributes, and is why a part's type reads "not recorded" and why null values are distinguished (Premise corrections 1 and 3).
- **[INFERRED]** `proof_of_concept/README.md` is marked superseded by this item. The POC code and its tests stay as they are; the project suite does not run them today. (Brief ruling 7.)
- **[INFERRED]** `src/model_viz/README.md` describes both views and how to switch between them.

**Snapshot shapes the structural view must honour** — verified against the fixture:

- **[HARD]** Occurrences live at `instance_graph.graph.occurrences`. Each record has `occurrence_id` (string), `parent_id` (null only at the root), `display_segment`, `containment_slot`, `effective_usage_id`, `effective_type_ids` (list of bare ids that resolve to no named record in the file), `occurrence_index` (null on all 23) and `package_display` (`stellarator_09` on the root, null elsewhere).
- **[HARD]** Attributes live at `instance_graph.graph.attrs`. Each record's `scope` is `{kind: "occurrence", wire: <occurrence_id>}` (377 of 377 match an occurrence exactly). Each carries `display_name`, `value` (number, string or null), `is_alias`, `alias_target` (a producer edge `{kind: "producer", target: {calculation, output}}` or a node edge `{kind: "node", target: <attribute node_id>}`, all 155 resolving on the fixture), `owner_qualified_name`, `declaration_qn`, `value_site`, `source_file` and `source_line`. There is no unit field.
- **[HARD]** A calc's owning part is the occurrence whose `occurrence_id` equals the calc's `scope.wire` (77 of 77 match).

**Testing**

- **[HARD]** There is no `node` on this machine. Browser tests run through Python Playwright from pytest, driving Chromium from the venv. Chrome refuses ES modules on `file://`, so the page stays on classic scripts; tests reach page state through `window.modelVizApp`. (v1 design D3, D13; brief ruling 10.)

## Non-Goals

- **Layout stability when toggling.** Boxes moving on expand or collapse is a separate P3 backlog item. (Brief ruling 9.)
- **The Occurrence-mode start state and the 33 calcs on the root.** Where cost calcs should be scoped is a modeling question owned by the structural-decomposition goal, and belongs to a v2 concept revision. (Brief ruling 9.)
- **Multiplicity.** The snapshot does not record it. (Brief ruling 1.)
- **Multi-hop path tracing** is v2. (`[OWNER]`, concept § Owner's Words.)
- **Constraint nodes, attribute nodes in either graph, and model editing.** The viewer stays read-only; attributes appear in the part panel only. (Concept § Non-Goals, agent-grade.)
- **A server or a syside path.** Out of scope because the snapshot carries the tree (Known Requirements, first decision).
- **Recording type names or units upstream.** Getting codegen to emit a part's direct type name or attribute units would let the panel show them. It is out of scope because this item reads the snapshot as it is. This leaves the new view showing less than the POC did (the POC showed a type name), so it is pending the orchestrator's confirmation of Premise correction 1 and should be registered as a follow-on if confirmed.
- **Static image export and double-click zoom** from the POC are not carried. Export stays out of scope as in v1 (`.project/active/model-viz/spec.md` § Non-Goals).

## Open Questions / Deferred to design

- **The view switch.** What the control looks like, where it sits, and which toolbar controls apply to which view (Group by, Find calc, Expand all).
- **State across a switch.** Whether selection, the open panel and collapse state survive switching views.
- **Tree drawing.** Nested boxes (compound nodes) or a parent-to-child edge tree, layout direction, and the start state (fully expanded or partly collapsed).
- **Panel layout.** How attributes are ordered and grouped (by declaring owner, by value kind, by name), and how the type-not-recorded line, the declaring owners and the calc count are presented.
- **Showing `effective_type_ids` and `package_display`.** Whether the bare ids or the root's package are worth showing.
- **Cross-view links.** Whether an alias bound to a calc output, or the calc count, links into the calc graph view.
- **Code sharing.** How much of `graph.js`, `panel.js`, `view.js` and `app.js` the structural view shares, and the file layout for new scripts and tests.
- **Carrying POC vocabulary.** Whether anything from `proof_of_concept/extraction/types.py` (for example `StructuralNode`, `ContainmentEdge`, `depth`) is worth keeping as names.
- **Where screenshot evidence is written.**

---

## Related Artifacts

- **Brief:** `.project/active/model-viz-structural-view/briefs/spec.md`
- **Concept:** `.project/concepts/model-viz.md` (Success Criterion 4, US-4)
- **Concept design:** `.project/concepts/model-viz-design.md` (§ Goals, § Switching to the structural view)
- **v1 calc-graph item (closed; the deferral record and the architecture this builds on):** `.project/active/model-viz/spec.md` § Non-Goals, `.project/active/model-viz/design.md`
- **Follow-on this item delivers:** `.project/backlog/BACKLOG.md` § Flagged — don't lose, "Structural view migration into `src/model_viz/`"
- **Existing viewer:** `src/model_viz/README.md`, `src/model_viz/viewer/`, `tests/model_viz/`
- **Reference, not migrated:** `proof_of_concept/README.md`, `proof_of_concept/extraction/types.py`
- **Fixture:** `exploration/stellarator_e2e/stellarator.snapshot.json`
- **Product lens:** `.project/active/model-viz-structural-view/product-lens.md`
- **Design:** `.project/active/model-viz-structural-view/design.md` (to be created)

---

**Next Steps:** `/_my_spec_review` in a fresh session, then `/_my_design`.
