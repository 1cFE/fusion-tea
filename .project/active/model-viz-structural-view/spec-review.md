# Spec Review: Model Visualization — Structural View

**Spec:** `.project/active/model-viz-structural-view/spec.md`
**Contract:** `claude-pack/commands/_my_spec.md`
**Brief:** `.project/active/model-viz-structural-view/briefs/spec_review.md` (orchestrator)
**Review File:** `.project/active/model-viz-structural-view/spec-review.md`
**Date:** 2026-09-13

---

## Reality Check

Sound. The spec is about the right item: the part containment view, in one page beside the calc graph, reading the snapshot. Almost every count it states is correct against the pinned bytes. The Problem section is accurate apart from one data claim. That claim is Premise correction 1, which says a part's type name is never recoverable. It is recoverable exactly for 10 of the 23 parts (M1 below). The fix is targeted, so the verdict is Revise, not Rework.

**How the counts were checked.** Read-only probes ran against `git show HEAD:exploration/stellarator_e2e/stellarator.snapshot.json`. Its SHA-256 matches the pin (`8e79aa4e…`, `tests/model_viz/viewer_harness.py:13`). Every fixture fact in the spec reproduced: 23 occurrences at depths 1/18/4, with parents `stellaris` 18, `magnet` 3 and `blanket` 1. The per-part attribute and calc table matched for all 23 parts. So did 377 attributes and 77 calcs, every scope resolving, and 377 source locations. Values split 183 numbers, 13 strings and 181 nulls. The nulls are 155 aliases (143 bound to a calc output, 12 to another attribute) plus 26 non-alias nulls (`cas_code` and `account_name` × 13). All 155 alias targets resolve, and all 143 producer targets match a named calc output. No unit is recorded on any of the 450 calc inputs or on any output. All 23 segments are distinct, and every `occurrence_index` is null. The checkout's working-tree snapshot differs from the pin (see A7).

---

## Must-fix

**M1 (L1-1) · Direct claim: Premise correction 1 is overstated. For 10 of 23 parts the direct type name follows exactly from the snapshot.**

The spec says picking a declaring owner as the type "would be a guess," and it requires every part's type to read "not recorded." That holds for 13 parts. It does not hold for the other 10.

- **What `effective_type_ids` is.** It is the part's type plus all its user-model supertypes, sorted by id string. The producer builds it as `{definition_id}` ∪ the supertypes' closures (`.venv/.../sysml_codegen/elaboration/occurrence.py:659`, used at `:982`). It sorts by wire string (`elaboration/elaborate.py:560-562`). So the order carries nothing, and the spec is right about that.
- **Why one id settles it.** If the list holds exactly one id, that id is the direct type. No supertype can be in it.
- **Why that type can be named.** An attribute scoped to the occurrence is declared either by the usage itself or by a definition in that closure. When the closure has one member, every definition-declared attribute is owned by the direct type. Its `owner_qualified_name` is therefore the type's name.
- **Which parts it covers.** Ten parts have a single-id closure. For nine of them, every attribute has the same owner:
  - `blanket/first_wall` → `mfe_radial_build_parts::'First Wall'`
  - `cryoplant` → `mfe_plant_systems::Cryoplant`
  - `fuel_cycle` → `mfe_plant_systems::'Fuel Cycle'`
  - `heat_transport` → `mfe_plant_systems::'Primary Heat Transport'`
  - `magnet/casing` → `mfe_magnet_parts::'Coil Casing'`
  - `magnet/coil` → `mfe_magnet_parts::'Modular Coil'`
  - `magnet/winding_pack` → `mfe_magnet_parts::'Winding Pack'`
  - `plasma` → `mfe_plasma::Plasma`
  - `vacuum_pumping` → `mfe_plant_systems::'Vacuum Pumping'`
- **The root is the tenth.** Its 71 definition-declared attributes come from `mfe_plant::'MFE Power Plant'`. The other 6 come from `stellarator_09::stellaris`, which is the part itself: `package_display` + `::` + `display_segment`.
- **The 13 parts where it fails.** These have 4 or 5 closure ids, and more ids than distinct owners. Blanket, for example, has 4 ids but only 3 owners. Nothing records the supertype edges, so the direct type cannot be told from its supertypes there. For those parts the spec's "not recorded" is correct.
- **Other fields hold nothing.** Per the brief's press point 1, I searched the whole file for every `effective_type_ids` and `effective_usage_id` value. No type id appears anywhere outside `occurrences`. No non-root usage id does either. `containment_slot` ids appear only inside occurrence wires and node ids. `declaration_qn`, `calc_def_qualified_name` and the calc inputs' `metadata.qualified_name` name where a feature or calc was declared, never an occurrence's type. `constraint_usages[].definition_qualified_name` names the constraint's definition. `constraints[].owner_qualified_name` names the part definition that declares the constraint. Neither names an occurrence's direct type.

**Caveat for the fix.** The rule has to tell a usage-declared attribute from a definition-declared one. On the root this is exact, as shown above. On a nested part, a usage-body attribute would carry the usage's qualified name, and the snapshot does not record that name. No such attribute exists on the fixture. So stating the rule exactly is part of the fix, not a detail to wave through.

What needs to be true:

1. The Problem section stops claiming the type is unrecoverable for all parts.
2. The requirement returns to the brief's own shape (ruling 4: "each part's type name where recoverable and 'not recorded' where not"), with the evidence rule stated. The alternative is to keep "not recorded" everywhere, but record it honestly as a choice made to avoid a producer-semantics dependency, not as a data fact.
3. The panel criterion changes to match. The fixture split is 10 named, 13 not recorded.
4. The Non-Goal "Recording type names or units upstream" is rewritten. Its "pending the orchestrator's confirmation" clause no longer applies. The loss against the POC shrinks to the 13 multi-type parts.

**M2 (L1-2) · Direct claim: the `[NEED]` "the structural view shows how the model is organized" misreads the owner's question.**

The spec says the owner's question "was about exactly that," meaning where numbers are filed. It then tags the containment tree `[NEED]` on the strength of that quote. The concept reads the other way:

- The concept's Problem Statement (`.project/concepts/model-viz.md:12`) says the containment view shows "where numbers are *filed* … not how they are *computed*. For this model, the containment tree is the least interesting dimension."
- The neighbouring verbatim line is "it only shows structure? No I/O or behavioral relationships?"
- The concept design (`.project/concepts/model-viz-design.md:21`) says "The existing structural view doesn't help."

So the question "why we don't have any organization or structure of the models?" led to the calc graph, not the containment tree. The brief carries the same reading, but only as the orchestrator's interpretation next to the verbatim quote.

The requirement itself stands. The owner-grade support for a containment view is "The existing structural view migrates in" (concept § Next-Stage Handoff, `[OWNER]`), with US-4 as the concept's restatement of it.

What needs to be true:

- The Problem section stops attributing the containment motive to that quote.
- The `[NEED]` cites the handoff line instead.
- The owner's question can stay as context, marked as the concept's framing.

This matters beyond hygiene. Capture-fidelity law 1 forbids letting a verbatim quote carry an inference the owner never made. Downstream agents would treat "the owner wants the containment tree because of this question" as settled intent.

---

## Advisories

### Lens 1 — Faithfulness

**L1-3 · Rewrite request: US-4 is graded `[OWNER]`, but the concept does not grade its user stories.** The spec cites "`[OWNER]` (concept § User Stories, US-4)". In `.project/concepts/model-viz.md:65-66`, US-4 carries no grade. The owner-grade items in the concept are in § Owner's Words and § Next-Stage Handoff. The `[NEED]` "switch between views in the same tool" is still well supported: "migrates in" plus "Code lives at `src/model_viz/`", both `[OWNER]`, imply one tool. It should cite those handoff lines, with US-4 marked `[INHERITED: concept US-4]`. The brief made the same grading, so this is a carried slip, not the spec agent's invention.

**L1-4 · Direct claim: the decision on ruling 1 is graded honestly.** It is `[INFERRED]` and cites the brief. It names the concept's literal wording (the syside extractor moving to `extractors/structural.py`, Success Criterion 4) that it departs from. It gives the reason, and it states both consequences: multiplicity, and no Python in `src/model_viz/`. The owner's reaffirmation is recorded as "the producer is the orchestrator's call," not as an owner ruling on the producer. No change needed. The brief asked for this check.

**L1-5 · Rewrite request: one `[HARD]` bundles a hard fact with a v1 design choice.** The Testing `[HARD]` bundles three facts:

- No `node` on the machine. This is hard.
- Chrome refuses ES modules on `file://`. This is hard.
- "Tests reach page state through `window.modelVizApp`." This is a v1 design decision (D13).

The third should be `[INHERITED: v1 design D13]` so design can change the test handle if it needs to. Also, the `[INFERRED]` "README describes both views" cites no source.

### Lens 2 — Problem & Approach

**L2-1 · Direct claim: the spec does separate the structural view from a relabelled Occurrence mode (press point 2).** A relabelled Occurrence mode fails four criteria:

- **Part count.** Occurrence mode omits the three calc-less magnet parts (`src/model_viz/viewer/js/view.js:28-42` keeps only calc owners and their ancestors), so it fails the 23-parts criterion.
- **Calc nodes.** Occurrence mode draws calcs, so it fails "no calc element appears."
- **Attribute panel.** Nothing in v1's panel lists a part's own attributes (`panel.js:127-132` shows attributes only as calc inputs). It fails the per-part attribute-count and row-content criteria.
- **Occurrence panel.** It fails "clicking a part opens a panel for that part," because v1 has no occurrence panel.

One route stays open. An implementer could reuse Occurrence-mode containers, include all occurrences and hide calcs. That satisfies the spec, and it is a legitimate design, not a loophole.

**L2-2 · Question to the user: should the structural view show which calc produces each bound attribute, or just name it?** The value criterion requires naming the producing calc and output for the 143 calc-bound aliases. That already makes the panel partly a computation view. Linking into the calc graph is correctly left to design (§ Open Questions, "Cross-view links"). No change is needed unless the owner wants the structural panel to stay purely about filing.

### Lens 3 — Pipeline Risk

**L3-1 · Direct claim: the unit criterion has no data path.** The criterion says "A unit is shown when the snapshot records one." The spec's own `[HARD]` shape says attribute records have "no unit field." The only unit fields in the file are `metadata.unit` on calc inputs and outputs, and all are null. So for an attribute, "records one" has no defined location. It can only be checked in the negative on the fixture, and design would have to invent a mapping, such as borrowing a consumer calc input's unit. Pick one:

- **Name the source.** For example, the unit on the calc output an alias is bound to. Add a synthetic-snapshot check.
- **Make it a Non-Goal.** State that the snapshot records no attribute units.

Leaving it as written invites two different builds.

**L3-2 · Rewrite request: the calc-count criterion is loose and redundant.** "Each part shows, or makes reachable in one click, the number of calcs it owns directly" is already fully covered by the panel criterion, which shows the calc count on click. The "or" clause adds nothing testable. Either drop it, or say what the tree itself must show if the spec wants the count visible without a click.

**L3-3 · Rewrite request: the round-trip criteria assume a fully expanded start that design owns.** Both round-trip criteria say "Starting fully expanded." The start state is deferred to design (§ Open Questions, "Tree drawing … start state"), and so is whether an Expand-all control applies to this view. The criteria stay testable if they say how the test reaches full expansion, through the page control or the test handle, regardless of the start state design picks.

**L3-4 · Rewrite request: the no-reload criterion is a weak proxy.** `data-load-seq` increments only inside the file-load path (`app.js:163`). A switch that re-parses the snapshot through another path would pass. If "not a reload" means "no second file read or parse," the criterion should also check the parse path, for example that the loaded model object is identical across switches through `window.modelVizApp`. Otherwise, say that the counter is the chosen evidence. Low risk.

**L3-5 · Question to the user: what should the panel show for a part with no attributes?** None exists on the fixture. The spec asserts "No part has zero attributes" but sets no behaviour for that case, even though the brief asked the spec to note such parts. It is a small gap, and a synthetic check would close it: the panel says the part has no attributes, and the type falls back per M1.

### Lens 4 — Hygiene

**L4-1 · Rewrite request: one Non-Goal carries process text.** "Recording type names or units upstream" reads "pending the orchestrator's confirmation … should be registered as a follow-on if confirmed." A Non-Goal is a decision record, not a pending action. The fix lands with M1. If a follow-on is wanted, register it and cite it.

**L4-2 · Direct claim: the Non-Goals pass the brief's press point 5.** Each has a reason. None is phrased as a prohibition anchored on a rejected suggestion. "A server or a syside path" is worded as out of scope with a reason, which is the good form. No change.

### Lens 5 — Reader Comprehension

No material findings. The Problem section leads with the point. The premise corrections are plain and separately numbered. The fixture-facts paragraph is dense but is reference data, not argument.

### Environment advisory

**A7 · Direct claim: the working-tree fixture has already moved off the pin.** In this checkout, `exploration/stellarator_e2e/stellarator.snapshot.json` is uncommitted and modified: SHA `19e36160…`, 399 attributes, 79 calcs. `magnet` now has 20 attributes and 15 calcs, `magnet/coil` 17 and `magnet/winding_pack` 27. This looks like the in-flight WI-040 work. Two consequences:

- The v1 suite fails at `tests/model_viz/conftest.py:43-48` in this working tree until that lands and the pin is re-probed.
- The spec's numbers will go stale when it lands.

The spec already says the tests compare against a Python reading of the raw file and that the viewer must not hardcode counts. That is the right shape. Design and plan should expect a re-pin, and the "existing suite passes unchanged" criterion should be judged against the pinned bytes.

---

## Engagement Summary

**Overall take:** A careful, well-counted spec that pins the structural view's content concretely enough that a relabelled Occurrence mode cannot pass. It overcorrects in one place: it declares part types unrecoverable across the board, when the producer's type closure names the direct type exactly for 10 parts. It also leans an owner quote toward a motive the concept records the other way.

**Here's what I need you to weigh in on:**

1. **[M1 / L1-1]** Decide the type rule. Option one: name the type where the closure has one id, per the stated rule, which covers 10 parts. Option two: keep "not recorded" for all 23, recorded as a choice rather than a data fact. Either way, the Problem section's claim, the panel criterion and the Non-Goal change.
2. **[M2 / L1-2]** Re-source the containment `[NEED]` to "The existing structural view migrates in," and stop attributing the tree to the "organization or structure" quote.
3. **[L3-1]** Units: name where an attribute's unit would be read from, or move units to Non-Goals.
4. **[L1-3, L1-5]** Regrade US-4 to `[INHERITED]` (cite the handoff's `[OWNER]` lines for the `[NEED]`), and move the `window.modelVizApp` test handle out of `[HARD]`.
5. **[L3-3, L3-4]** Tighten the round-trip start and the no-reload evidence so they do not presume design's start state or rest on a single counter.
6. **[A7]** Expect a fixture re-pin when WI-040's snapshot lands. The spec's counts are for `8e79aa4e…`.

---

## Resolutions

(None yet. Record the orchestrator's or owner's call per finding ID here, for the spec agent to incorporate.)

---

**Verdict:** Revise
**Next Steps:** Record resolutions for M1 and M2 (and any advisories taken), then return to `/_my_spec` pointed at this review. The reviewer does not edit the spec.
