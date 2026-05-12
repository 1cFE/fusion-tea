# Explainer HTML — User Feedback After v1 Rewrite

**Verdict:** rejected. The v1 rewrite (down-select.html post explainer_updates.md) abandons the framework set up in Sections 1–2 and replaces it with internal jargon, broken-promise filters, and AI-slop rhetorical constructions. Read this in full before touching anything for v2.

---

## Direct quotes from user

> I am not OK with this filter ["far-thin physics"]. this is too broad-brush and literally flies in the face of what we had fucking said before ("we don't judge winners for stage 1")

> In fact, I fucking hate "Step 1" of the triage. It doesn't fucking use the framework we painstakingly set up whatsoever.

> I have read this paragraph twice and have no fucking idea what we are trying to say [re: CATF/Woodruff aside]

> WHAT THE FUCK IS THIS LANGUAGE? what the fuck is "grammar" in this context?

> What are we talking about?? I have totally lost this fucking thread [re: "Stage 1 has first-class failure codes too"]

> I can't even finish this. I'm struggling to imagine a worse-written explainer. Spend all this effort to set up a framework, and then just throw it all away, and blabber through all these tangents and horse shit logic.

> ["LCOE floor is a four-tuple, not a single number"] THIS IS SUCH AI SLOP. THIS IS SUCH AN OVERUSED LINGUISTIC CONSTRUCT. {THIS}, NOT {THAT}. ALL THE FUCKING TIME.

---

## What the feedback actually says — structural problems

### 1. The framework is set up, then abandoned

Sections 1–2 establish a specific vocabulary: 4-stage journey, intrinsic / ecosystem-relational / ecosystem-distinct factors, Stage 1 as a **time-and-cost discount** (not a gate), F2.a / F3.a / F4.c codes. That vocabulary is the explainer's whole reason for existing.

Sections 3–4 then ignore it. The triage uses `T1 / T2 / T3` signals nobody introduced. The "grammar" sub-section introduces F1.a / F1.b / F1.c, binary/degrading sub-flavors, Layer A/B, gate-type taxonomy — five new vocabularies stacked on top of the original three, with no bridge.

The reader's experience: "I just learned this. Why are we now in a different language?"

### 2. "Far-thin physics" violates a stated commitment

Section 2 says explicitly: **we don't gate on physics.** Section 3 (Step 1 triage) then eliminates 14 of 26 concepts on `far-thin physics`. This is a Stage-1 gate. The contradiction is not subtle; it's the single largest commitment the explainer made, broken three sections later.

Fix direction: triage cannot use Stage-1 physics as an eliminator, period. If 14 concepts genuinely have no organized program, that has to be framed as something other than a physics gate — or the framework's "no Stage-1 gate" stance has to be retracted in Section 2. Pick one. Don't promise A in Section 2 and do not-A in Section 3.

### 3. Step 1 of triage doesn't use the framework

The triage signals (data sufficiency, LCOE floor, Stage-1 feasibility) are *unmotivated* from the framework. The framework gives us intrinsic / relational / distinct factors, F-codes, dominant failure mode, dominant leverage. If triage exists, it should be a *coarsening* of the framework, not a parallel filter that ignores it.

Possible reframe: "before we trace, we ask the cheap version of the trace's own question — does the concept even have a plausible path through Stage 2, Stage 3, Stage 4 economics?" The eliminators are framework-derived (e.g., "F2.a alone disqualifies — minimum-viable-plant cost is structurally unreachable at any reasonable financing structure"), not invented for triage.

Or: don't have a "triage step" at all. Just describe the procedure as "we traced 12; the other 26 didn't survive structural-signal review against the framework above." Don't dress it up as a discrete pipeline.

### 4. "Grammar" is internal jargon

"Grammar" came from `methodology_revision_v1.md` — it's how I described the qualifier system internally. It was never introduced to the reader. To the reader, "grammar" reads as either (a) a programming/parsing metaphor, or (b) writing rules, neither of which is what's meant.

If we need a word for "the structured fields a trace records," call it that. Or "trace template." Or just say "what each trace records." The reader does not need a meta-word for the field schema.

### 5. "Stage 1 has first-class failure codes too" — lost thread

This h4 has zero setup. The reader was told Stage 1 is a discount. Then suddenly: "actually Stage 1 has failure codes." The reader has no idea why we changed our mind, what the F1.a/b/c codes are for, or how they relate to F2.a et al.

The deeper issue: this is leaking the *internal methodology revision history* into the explainer. The reader doesn't need to know we changed v0 → v1. They need a coherent presentation of where we landed. The v0 framework in Section 2 ("Stage 1 is a discount") is wrong by the v1 standard we actually use — so Section 2 needs to be updated to match, or the F1 codes need to be removed.

### 6. CATF/Woodruff aside is incomprehensible

The aside crams `C = C_0 × U_mat × U_TRL × U_LR` into a paragraph with no setup of what C_0, U_mat, U_TRL, U_LR are or why anyone should care. Then it says "TRL-3 vs TRL-7 same point estimate but 3× vs 1.3× P10-P90." The reader has no context for what TRL means in this project, no context for why P10-P90 matters here, no context for why this is a CATF/Woodruff thing.

If we're going to cite a probabilistic framework, do it in one sentence: "Data-sparse concepts widen their LCOE band; they don't get eliminated." Cut the equation. Cut the TRL example. Cut the dispersion variable names.

Or: cut the whole aside. The point it's making (data-sparse concepts aren't excluded) is made elsewhere. The aside doesn't earn its space.

### 7. AI-slop rhetorical constructions

The "X, not Y" / "{this}, not {that}" pattern is everywhere in the v1 draft. Examples I can see immediately:

- "LCOE floor is a four-tuple, not a single number"
- "Spanning, not ranking"
- "Step 1 · Triage — cheap signals first" (Step 2 / Step 3 follow same shape)
- "Data sufficiency is a soft filter, not a gate"
- "Same methodology, opposite analytical artifacts"
- "Spanning axes drive picking; traces defend, not generate"
- "Picks-then-defend inversion"
- "Five concepts that, studied together, teach more than five rankings of the same axis"
- "[Triage uses cheap eliminators,] but it does not exclude..."

This pattern is a tell that the writing has not been edited for what it actually says — it leans on the rhetorical shape to feel structured without doing the work to actually be structured. **Strip every instance in v2.** If a sentence reads "X, not Y," rewrite it to say what X *is*. The "not Y" clause is doing rhetorical work, not informational work.

### 8. Tangents and "horse shit logic"

User flagged that the doc "blabbers through tangents." Specific tangents to audit:

- The "methodology-control trace" aside — internal category that doesn't help the reader.
- "Layer A can have sub-threads" — the reader doesn't yet care; this is methodology-developer talk.
- "Gate type predicts evidence requirements" h4 — orthogonal taxonomy introduced before the reader has stabilized the first taxonomy.
- "Why these two — and where Zap fits" aside — Zap is a methodology-internal concept; surfacing it confuses the worked-examples reader.
- "Methodology friction encountered (open)" aside — leaking unresolved internal frictions to a reader who came for the *result*.

The rule of thumb to apply in v2: **if a section explains why we changed our minds, cut it.** The reader does not care about the iteration history. They care about what we landed on and why it's defensible.

---

## What needs to happen in v2

### Hard requirements

1. **One framework, all the way through.** Sections 1–2 set up the vocabulary; Sections 3–4 *use* the vocabulary. No new taxonomies introduced after Section 2 unless they are presented as part of the original framework.

2. **Reconcile Stage 1.** Either:
   - **Option A:** Hold the "no Stage-1 gate" commitment. Triage cannot eliminate on physics. Concepts without an organized program get filtered for something else (no defensible cost basis, no buyer story at any stage, etc.) — and that filter is described in framework terms.
   - **Option B:** Acknowledge in Section 2 that some concepts *are* eliminated at Stage 1 — when the physics binary is unbounded enough that no Stage-2/3/4 analysis is meaningful. Make this an explicit carve-out, not a contradiction discovered three sections later.
   Pick one. Don't have both.

3. **Strip "X, not Y" constructions.** All of them. The pattern is the smell of writing that hasn't been edited. Rewrite each instance to say what the thing *is*, not what it *isn't*.

4. **Cut internal jargon that wasn't introduced.** "Grammar," "first-class," "load-bearing," "qualifier axis," "tuple," "Layer A / Layer B" (unless they earn their introduction by being demonstrably useful to the reader), "binary-terminal-economically." All of these are methodology-developer vocabulary. Either teach them properly with motivation, or use the plain phrase.

5. **No iteration history.** The reader gets the v1 framework as if it were always v1. No "the v0 grammar had this gap"; no "we initially thought X, then found Y." That belongs in `methodology_revision_v1.md`, not the explainer.

### Soft requirements (probable)

6. **Triage may not be a discrete step.** Consider folding the 26 → 12 narrowing into a single sentence in the methodology section ("of 38 candidates, 12 had enough structural signal to warrant the trace below"), then move directly to the framework's application. Avoid the visual pipeline that calls attention to a parallel-procedure feel.

7. **Worked examples should use the same vocabulary as the framework.** If F2.a is in Section 2, the worked example tags F2.a. No new "F1.a" or "Layer A" appearing in the worked examples that wasn't in the framework.

8. **The portfolio section is probably good in structure but needs language scrub.** The 5-pick cards, spanning table, coverage matrix, slot-5 defense — these are the right shapes. They need their rhetoric cleaned and any framework-vocabulary mismatches fixed.

9. **CATF/Woodruff:** either delete or compress to one sentence. Cut the equation.

10. **Open methodology frictions:** belong in the source artifacts (`methodology_findings.md`), not the explainer.

---

## Audit checklist for v2

Before declaring v2 done, the writer should be able to answer:

- [ ] Does every term used in Sections 3–6 appear in Sections 1–2, or does Sections 1–2 explicitly set up that it will be introduced later?
- [ ] Is the Stage-1 commitment in Section 2 consistent with how Stage 1 is treated in the procedure?
- [ ] Has every "X, not Y" construction been rewritten?
- [ ] Has every reference to "v0," "v1," "the original methodology," "the revised grammar," "we initially," etc. been removed?
- [ ] Are there any sections that explain *why we changed our minds* rather than presenting a single coherent methodology? Cut them.
- [ ] Read the doc aloud start to finish. Does any sentence make you ask "what?" If yes, that sentence is broken.
- [ ] Could a reader who only read Sections 1–2 predict, with rough accuracy, the procedure in Section 3? If no, the framework isn't actually doing the work it claims.

---

## What I should have done

The mistake in v1: I treated "integrate Effort A + Effort B into the HTML" as a content-merge problem. It was a *framework-coherence* problem. Effort B produced a more sophisticated grammar (F1 codes, Layer A/B, gate-type taxonomy, binary/degrading sub-flavors) that genuinely matters for the analysis but was developed *after* the explainer's framework was set. Integrating it required either:

- (a) **updating Sections 1–2 to reflect the actual framework we use**, so that Sections 3–6 are consistent with the setup; or
- (b) **stripping the v1 grammar down to what survives at framework granularity**, so the explainer doesn't introduce vocabulary the framework doesn't support.

Instead I bolted on the v1 grammar in Section 3 with apologetic prose ("the naive treatment makes Stage 1 a discount; that fails when..."). That apologetic shape *is* the iteration-history leak. The reader doesn't want to watch us re-think; they want a single defensible framework.

For v2: pick (a) or (b) before writing. If (a), Section 2 needs to introduce F1 codes, binary/degrading sub-flavors, and Layer A/B as part of the historical-evidence-by-stage frame — they need to be motivated from the empirical literature in Section 2, not invented as methodology fixes. If (b), the explainer is narrower than what the dossier currently records; that's fine — the dossier can carry richer internal vocabulary that the explainer doesn't surface.

My instinct: **(b)** is the right call. The explainer is for the reader; the dossier is for the analysis. The dossier can have F1 codes and Layer A/B; the explainer can describe the same picks without those qualifiers and still close the loop. The four richer qualifiers (F1, binary/degrading, Layer A/B, gate-type) are *useful internally* but are not load-bearing for the reader to understand which 5 concepts we picked and why.

If we go (b), Section 3 collapses substantially:
- No "grammar" section.
- No qualifier taxonomies.
- LCOE-floor stays as a single number per concept; the band visual stays but without the "engineering-bounded vs uncertainty-bounded" labels.
- Section 3 is: triage (in framework terms) → trace (in framework terms) → span → coverage check → defend slot 5. Five paragraphs, maybe.

Hard part for next iteration: deciding which path. That's a user call, not mine.
