# Story Outline — Closing the Loop (closed-loop.html)

Companion outline for `docs/demo/closed-loop.html`, per the html-explainer skill. Sources: `work/active/WI-015_ife-end-to-end-demo/demo_report.md` + `findings.md`, `work/active/WI-014_*/findings.md`, `work/active/WI-016_h2-blind-derivation/` (via `modeling_project/HYPOTHESIS_DOSSIER.md`), `data/ife_sweep/`.

## Opening hook

A model that has never run is a diagram. For four months the IFE SysML models produced numbers only one way: a human re-typed the formulas into a Python script (`scripts/verify_ife_lcoe.py`) and ran that instead. The formal model itself had never computed anything.

## Core insight

On 2026-07-05 the loop closed: the SysML models were mechanically turned into running Python — no human re-typing any formula — and the generated code reproduced every verified answer bit-exactly, then swept 11,505 design points to map where inertial fusion is economically viable.

## Section outline

1. **The Gap** — the hand-written oracle vs. the never-executed model; what "closing the loop" means.
2. **The Chain That Ran** — six pipeline stages (SysML → live extraction → generated Python → teax execution → anchor check → viability sweep), with the reproduce commands.
3. **The Anchor Check** — the 3-anchor table (expected vs. executed, rel. dev 0.0 against a 1e-6 tolerance); why bit-exact; expandable panel on the three model fixes and filed toolchain gaps.
4. **The Viability Map** — both sweep figures; the ηG = 10 knee, the flat basin past it, driver type setting required gain; grid stats.
5. **The Blind Derivation** (compact H2 panel) — firewalled corpus derivation matched the answer key's forms, reproduced the $1030M override to 4%, found 2 answer-key bugs.
6. **What Is Still Open** — constraints don't execute (Phase 6), cross-part wiring gap, arithmetic-only envelope, one-family H2 — honest limits, pointer to the dossier.

## Narrative arc / surprise

The surprise lands twice: the anchor agreement is not "within tolerance" but *bit-exact* (section 3), and the blind-derivation model reproduced a number the reference code can only reach by manual override (section 5).

## Closing connection

Section 6 returns to the opening: the model is no longer a diagram — it runs — but the loop closed on the easiest possible terms (flat arithmetic, constraints checked outside the generated code), and the dossier records exactly how far the claim extends.
