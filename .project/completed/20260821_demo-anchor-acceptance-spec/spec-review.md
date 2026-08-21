# Spec Review: Anchor Acceptance Bars (STELLARATOR-DEMO Item 1)

**Spec:** `.project/active/demo-anchor-acceptance-spec/spec.md`
**Contract:** `claude-pack/commands/_my_spec.md`
**Review File:** `.project/active/demo-anchor-acceptance-spec/spec-review.md`
**Date:** 2026-07-18
**Barred paths:** PROTOCOL §3 honored — no held-out or ARIES-CS-informed artifact read.

---

## Reality Check

**Sound.** The spec is about the right work item, and it is a careful piece of work. Every Anchor-A and Anchor-B number I spot-checked traces cleanly to the research doc (float32 floor −4.8e-8 / +6.23e-8 / +1.0e-7; the −31% gap $123.74 vs $85.55; the AACE Class 5 band; the p_net re-stale sequence 575→786→578→804→915). The G-8 premise conflict is surfaced and parked, not resolved. The provenance grades are mostly used correctly and the blind is mostly honored in the rationale text, not just asserted.

It does not fail Stage 0. But it has one sharp usability defect (a bar that, read literally, passes the very failure it cites as the thing to catch), one worded-three-ways bar, and one provenance-grade over-claim. All are targeted edits, not a rework. **Verdict: Revise.**

The findings below are split **must-fix** vs **nice-to-have** per the brief, each carrying a lens ID, the spec section it targets, and a concrete fix.

---

## Must-fix

### M1 · Direct claim — the per-account bar, read literally, passes large negative errors. [Lens: usability / A-2, A-4]

**Where:** A-2 title and "Applies to"; A-4 point 1; ratification table A-2 line. All say **"relative deviation ≤ 1e-6"** (or "≤ 1e-6 relative"), never *absolute value*.

**The problem:** a relative deviation is signed. `−0.206` (the f_shape trap's −20.6% failure, which this same spec cites in A-2's basis and A-5 as the archetypal real error the bar must catch) is **≤ 1e-6**. So a literal application of the bar as written *passes* a −20.6% miss. Two readers will split: one reads "deviation" as magnitude, one applies the inequality as printed. The handshake's own failure precedent is a signed negative number, so this is not hypothetical.

**Fix:** state the bar as **|relative deviation| ≤ 1e-6** (magnitude), everywhere it appears — A-2 header, A-2 applies-to, A-4 point 1, the A-2 ratification line. One word, but it is the difference between the bar working and not.

### M2 · Rewrite request — B-3's pass band is worded three non-equivalent ways. [Lens: usability / B-3]

**Where:** B-3 "Pass band" and basis. Three phrasings appear for one bar: **"same order of magnitude"**, **"leading power of ten matches"**, **"within a factor of ~3"**.

**The problem:** these are different tests and disagree near boundaries.
- *Leading power of ten matches* = `floor(log10)` equal. It **fails** a factor-1.5 pair that straddles a boundary (12 vs 8 → 10¹ vs 10⁰) and **passes** a factor-9 pair inside one decade (11 vs 99). Brittle and not monotonic in the ratio.
- *Same order of magnitude* colloquially = within a factor of 10 (ratio ∈ [0.1, 10]).
- *Within a factor of ~3* = ratio ∈ [1/3, 3].

An implementer cannot apply three tests. The ratification-table B-3 line already collapses to "within ~3×", so the intended test is probably the factor-of-3 one — but the body must say so unambiguously.

**Fix:** pick **one** operational test and delete the other two framings. Recommend: **ratio ∈ [1/3, 3]** (equivalently `|log10(model/ref)| ≤ 0.5`). Keep the geometry-direct "expected inside a factor of 2" as an explicit **non-gating note** (it already is — just make sure it does not add a fourth number to the *pass gate*). If the owner wants the looser factor-of-10 "order of magnitude," say that instead — but say exactly one thing.

### M3 · Capture-fidelity + internal contradiction — the sizing-axis exclusion is graded settled but is still owner-pending. [Lens: capture fidelity / consistency / B-5]

**Where:** B-5 second bullet, tagged **[HARD] [INHERITED]** ("This spec writes no criterion-4 sizing expectation"); ratification table B-5 line ("☐ ratify ☐ adjust"); concept criterion 4.

**The problem — two parts:**
1. **Over-graded.** The concept criterion 4 still marks the sizing→criterion-8 reallocation **"[SURFACED to owner] — this reallocation needs owner confirmation."** I found no record that the owner has since confirmed it. Grading it **[HARD]/settled** in the body turns a surfaced-pending item into a do-not-relitigate one — exactly the settled-⊆-owner-grade violation capture-fidelity §1 guards against. (The C220107 exclusion in the *same* B-5, by contrast, is genuinely forced — it is the one ARIES-CS-derived value and leaving it in makes the blind self-referential — so [HARD] is right *for that half*.)
2. **Self-contradiction.** The body calls B-5 [HARD] (settled) while the ratification table lists B-5 as a proposal the owner must ratify. A document should not present as settled the thing it is simultaneously asking the owner to ratify.

**Fix:** (a) present the sizing reallocation as **owner-confirmation-pending** (like G-8), not [HARD], until the owner rules — or cite where the reallocation was already confirmed if it was. (b) **Split the B-5 ratification line**: C220107 exclusion is mandatory [HARD] (list for visibility, not "ratify or adjust"); the sizing reallocation is the item that needs the owner's confirmation. Bundling a forced exclusion and a pending reallocation under one checkbox hides the second behind the first.

---

## Nice-to-have

### N1 · If-then — the ratio convention is unstated (but the worry is smaller than it looks). [Lens: usability / B-4, B-3]

I verified the orchestrator's suspicion. The **−50%/+100% band is inversion-invariant**: 0.5 and 2.0 are reciprocals, so the pass region [0.5, 2] is identical whether you test model/ref or ref/model. Two readers get the same pass/fail verdict *at these endpoints*. So this is not the ambiguity it first appears — worth recording plainly so it is not "fixed" into a false asymmetry.

It is still worth pinning the convention, for two reasons: (a) Item 7 must **report** a signed deviation, and the sign/magnitude it prints depends on the convention; (b) if the owner *adjusts* the band during ratification to a **non-reciprocal** pair (e.g. −30%/+100% → [0.7, 2.0]), the invariance breaks and the missing convention becomes a live ambiguity.

**Fix:** state the convention once — recommend **model/reference** (matching the handshake's `rel_dev` sense) — and have Item 7 report the **ratio**, not a signed percentage. Apply the same to B-3's factor-of-3.

### N2 · Rewrite request — "verbatim force" over-claims. [Lens: capture fidelity / A-3]

A-3 labels the criterion-3 ruling **"[OWNER] criterion-3 ruling (2026-07-18), verbatim force."** The epic records this ruling as **[OWNER]** (a paraphrase), not **[OWNER-VERBATIM]** with a quote. "Verbatim force" reads as claiming these are the owner's exact words. If it means "carry it at full force, undiluted," say that. If an actual owner quote exists, cite it; otherwise call it an [OWNER] paraphrase carried at full force. (The *content* is faithful to the epic — not amplified, not diluted — so this is wording, not substance.)

### N3 · Rewrite request — B-2 makes a pre-reveal assertion about ARIES-CS. [Lens: blind integrity / B-2]

B-2's third bullet says the model's CAS tree should cover **"the same top-level accounts ARIES-CS reports at."** That phrases a claim about ARIES-CS's structure before reveal. The claim is defensible (the CAS family is general ARIES/Starfire lineage, disclosed in the concept) — but B-1's prior-leak bar asks that the spec honor the blind **in its own text**, not just state the rule. **Fix:** reword as a model-side test — "the model's CAS tree covers the standard CAS20 (22x) + CAS10/40/50/60/70/80 accounts, so that whatever ARIES-CS reports can be matched account-to-account" — so no pre-reveal assertion about ARIES-CS is baked into the bar.

### N4 · Direct claim — A-4's reconciliation tolerance mixes relative and aggregate. [Lens: usability / A-4]

A-4 point 2 ends: "The residual LCOE gap **equals the sum of the itemized remainder to within the per-account bar**." The per-account bar is *relative* (1e-6); a sum reconciliation needs an *aggregate* tolerance. **Fix:** state the reconciliation tolerance explicitly — a dollar epsilon, or 1e-6 relative to the LCOE — distinct from the per-account 1e-6.

### N5 · Question to record — A-2 is extended to accounts whose float32 behavior isn't measured. [Lens: evidence / A-2]

A-2's 1e-6 basis is measured on the 12 formula-reproduced accounts. It then applies to "any account Items 3–4 bring under the bar" — CAS40/50/60/70/80, whose numerical paths aren't measured (research §B notes CAS70 O&M has "no jnp in line," i.e. no float32 rounding at all). This is fine — 1e-6 is a **ceiling**, so an account with less float32 noise passes more easily, and A-4's itemization absorbs any account that legitimately cannot meet it (it becomes explained remainder). **Fix:** add one sentence saying exactly that, so a reader doesn't take the measured-on-12 basis as a claim that all Item 3–4 accounts share the same floor.

### N6 · Rewrite request — the ratification "visibility" note is incomplete. [Lens: consistency / ratification package]

The note under the Anchor-A table says "(A-1 … and the ~1e-7 float32 floor are recorded as [HARD]/already-standing … listed for visibility)." But A-3 (owner ruling), A-5 (mapping-trap discipline), B-0, and B-1 are also [HARD]/[INHERITED] and deliberately excluded from ratification. **Fix:** broaden the note to say all [HARD]/[INHERITED] items are excluded from ratification (the table carries only the [AGENT-PROPOSED] items), so a reader isn't left wondering whether a bar was dropped. (I checked: the table *does* contain every [AGENT-PROPOSED] item — A-2, A-4, A-6, B-2–B-7, G-8 — so the package is complete; only the note under-explains the exclusions.)

---

## What checks out (so the owner knows what not to re-litigate)

- **Evidence tracing is clean.** Float32 floor numbers, the −31% gap decomposition, CAS22 tail ($1.094B) and CAS40/50/60 lines, the AACE Class 5 band (−30/−50 to +30/+100), the p_net re-stale sequence, and the WI-019→025 headline swings all match the research doc.
- **G-8 is handled correctly** — surfaced, parked as [OWNER DECISION PENDING], with the "keep bar as-is (blocks Items 3–4)" option honestly offered. Not resolved silently. Per capture-fidelity §4, this is right.
- **Concept faithfulness on the honesty bar** — B-0 and B-6 carry criterion 4's "a miss fails the anchor and is reported, not narrated away" with no soft language; pre-reveal commitment is explicit; the itemized-remainder acceptance faithfully operationalizes the [OWNER] criterion-3 ruling.
- **A-3 vs A-4 and B-5 vs B-6 are internally consistent** (the gap boundary matches the acceptance form; the C220107/sizing exclusions carry into B-6's conjunction).
- **Anchor-B rationales draw only from admissible bases** (model-side sensitivity + general AACE), with the one wording slip flagged in N3.

---

## Engagement Summary

**Overall take:** A strong, well-traced spec with one bar that doesn't do what it says, one bar that says three different things, and one exclusion graded as settled before the owner has settled it. None is a rework; all are targeted edits. Fix M1–M3 before ratifying, decide N1–N6 in passing.

**Here's what I need you to weigh in on:**

1. **[M1]** The per-account bar reads "relative deviation ≤ 1e-6" without absolute value — so a −20.6% error passes it literally. Confirm the intended bar is **|relative deviation| ≤ 1e-6**.
2. **[M2]** B-3's pass band is worded three non-equivalent ways. Pick one operational test — I recommend **ratio ∈ [1/3, 3]** — and keep factor-of-2 geometry-direct as a note only.
3. **[M3]** The sizing-axis exclusion is tagged [HARD]/settled, but the concept still marks that reallocation "[SURFACED to owner] — needs confirmation," and B-5 is also in the ratify table. Decide: is the sizing→criterion-8 move already confirmed (cite it) or does it ride on *this* ratification (then de-grade it from [HARD] and split the C220107 half out)?
4. **[N1]** The −50%/+100% band is inversion-invariant, so it's less ambiguous than it looks — but state the ratio convention (model/ref) anyway, so Item 7's reported sign is fixed and any adjusted band stays unambiguous.
5. **[N3]** B-2 asserts "the same accounts ARIES-CS reports at" pre-reveal. Reword to a model-side test to honor the prior-leak bar in the spec's own prose.

---

## Resolutions

*(Filled in during Stage 5 as the owner resolves each finding, keyed by ID. The spec agent reads this section to incorporate the review; the reviewer does not edit the spec.)*

---

**Verdict:** Revise
**Next Steps:** Record resolutions above, then return to the spec-agent session (or re-run `/_my_spec`) pointed at this review to incorporate M1–M3 and any accepted nice-to-haves. After the edits land, the owner ratifies the consolidated package. The reviewer does not edit the spec.

ARTIFACT: .project/active/demo-anchor-acceptance-spec/spec-review.md
