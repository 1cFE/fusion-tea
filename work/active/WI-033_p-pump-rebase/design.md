---
Status: approved
Created: 2026-08-28
Updated: 2026-08-28
Related Artifacts:
  Spec: ./spec.md
---

> **Approved by owner 2026-08-28** ("approved, proceed to plan and implement") — including D1 (standalone registry, no seam request; flip rests on the write door, stated honestly).

# WI-033 Design — P_pump Re-base

## Overview

One attribute changes value and gains a full evidence trail. The design work is not model architecture — it is sequencing: two native seam registrations must land *before* the doc comment that cites them and *before* the runbook flip that rests on them. Everything here serves that order.

## Research Findings

- **Prototype PASS (2026-08-28, pre-approval, reverted).** `p_pump = 195.0` applied in both twins: L1 = 0 errors / 0 warnings over 22 files; L2 = the same 12 pre-existing placeholder-binding WARNs (all in `generic_mfe/mfe_plant.sysml`, the recorded baseline — none from this edit); twins byte-identical; working tree reverted clean.
- **Both source URLs are live** (HTTP 200, checked 2026-08-28):
  - Cismondi: `https://scipub.euro-fusion.org/wp-content/uploads/eurofusion/WPPMICPR17_17709_submitted-4.pdf`
  - Moscato: `https://scipub.euro-fusion.org/wp-content/uploads/eurofusion/WPBOPCPR18_20276_submitted.pdf` — the `-1` variant is **byte-identical** (both SHA-256 `75f2417ab3d005af0599251e3b81739b6bcae99c1d6ac5b1cd0116d7194ffba4`); register the unsuffixed URL. Spec Risk 1 (retrievability) is retired.
- **The registry commits natively**: `source_registry.py register` writes source dir + raw + manifest row + index block and commits them together, or leaves the tree untouched (operator guide § Registering a source, on its own). So the ancestry predicate for the flip is satisfied by commit order alone.
- **Validation route**: `uv run agentic-mbse validate models/` (the model-validation skill forbids bare `syside check`); needs `set -a; source ~/1cfe/agentic-mbse/.env; set +a` first.
- **AD constraints touched**: AD-001 only (plain `Real`, units in doc comments) — respected; no new definitions, no library change, no binding change, so AD-002…AD-007 are untouched by construction.

## Design Decisions

### D1. Both registrations run the standalone registry — no `research_seam.py` request is opened

The mandate is "register Cismondi; ingest the Moscato PDF" — two known sources at known URLs. The operator guide sanctions exactly this: *"You can use the registry on its own … to register a source you already have."* Wrapping a known-PDF fetch in a research request would re-enact the mistake the owner's framing correction names (the seam's intent is open-ended research, never "fetch a known PDF" — Item 5 handoff, § Key Discoveries), and Item 5 already refused to manufacture research ceremony.

**Consequence, stated honestly**: the flip's live evidence is two `registered` outcomes through the seam's write door. The request/return bookkeeper (`research_seam.py` open → log → close, the four-class return) has still not run end-to-end. The flip commit message and the verification record say so; GSTH Item 6's epic-evidence report should carry the same sentence.

*Rejected*: wrapping Moscato in a full seam request to exercise the four-class return (manufactured ceremony, contradicts the owner framing correction). *Rejected*: leaving the flip to the first real goal-round seam use (keeps the runbook instructing hand-registration, which the epic SC forbids and which WI-033 itself would otherwise have to follow — following it violates the SC too).

### D1a. Amendment 2026-08-28 — the write door needed a fix first `[OWNER 2026-08-28]`

The first live Cismondi call returned `capture_failed`: `source_registry.py:485` assumed every
URL capture stores `raw.html`, but the extractor saves PDF URLs as `raw.pdf`
(`agentic-mbse .../extract_cli.py:282`). Diagnosis evidence: probe extraction of the Cismondi
URL succeeded with `content_hash_sha256` identical to the 2026-04 concept-research extraction;
rollback held (registry files untouched, `verify` 0 faults). Fix (owner-ruled over the
`--local-pdf` workaround): resolve the raw artifact as whichever of `raw.html`/`raw.pdf` the
capture stored; regression test serves the fixture PDF over loopback. Downstream is
extension-agnostic (the artifact is only hashed and holdout-checked), so nothing else moves.
The commit sequence gains **C-FIX** before C-REG-CIS.

### D2. Commit order carries the proof

1. **C-REG-CIS** — registry commit, Cismondi (registry-authored).
2. **C-REG-MOS** — registry commit, Moscato (registry-authored).
3. **C-MODEL** — both twins: value + doc comment citing the registered paths from 1–2.
4. **C-TESTS** — census re-derive if (and only if) the MFE semantic fingerprint moved; nothing else.
5. **C-FLIP** — the four `GOAL_RUNBOOK.md` edits + the `goal.md` dated amendment, one commit. `git merge-base --is-ancestor C-REG-MOS C-FLIP` is the recorded predicate (C-REG-CIS is then an ancestor by transitivity).
6. **C-CLOSE** — DI-008 disposition, `verification_record.md`, SV-037 → passing.

### D3. The model edit (both twins, identical bytes)

```sysml
:>> p_pump = 195.0 {  // primary coolant pumping power [MW] -- helium-primary circulator basis (WI-033).
    doc /*
    Re-based from the 1costingFE default 1.0 MW -- a ~150x understatement for a
    helium-cooled ~3240 MWth plant (DI-008, amended 2026-08-28) -- to 6% of the
    baseline computed p_th (3238.1 MW -> 194.3), landed rounded at 195.0
    [OWNER 2026-08-28]. HELD, SETTABLE INPUT by owner ruling (goal p-pump-basis,
    trail section Goal close, Ruling 2): a computed fraction of p_th would assert a
    linearity across swept (R, a) that no source establishes, and would retire a
    study lever in two committed studies. Re-derive the scalar when the design
    point moves.
    KNOWING TRACEABILITY-FIRST CHOICE (Ruling 3): the documented lower bound is
    ~130 MW (~4% of p_th -- Moscato's near-term 8-loop design, 83-94 MW at
    2101.7 MWth; the f_uplift_cryo exclude-with-documented-bound pattern).
    Cismondi's ~150 MW (~6.3% of blanket thermal) is a preliminary figure for one
    unoptimized loop layout its own authors expect to fall (larger pipes: ~9 km
    loop -> ~3 km).
    **Source**: {REGISTERED-CISMONDI-PATH}; {REGISTERED-MOSCATO-PATH}
    **Ref**: {CISMONDI-EXTRACT}:{line} (~150 MW helium circulator, one order of
    magnitude above water ~15 MW; HCPB representative for HCLL);
    {MOSCATO-EXTRACT}:{line} (2101.7 MWth, 9 loops x 2 compressors, 6.8/7.5 MW
    -> ~131 MW total, 6.2%; near-term 8-loop 5.9/5.2 MW -> 83-94 MW, ~4%)
    **Basis**: 6% of baseline p_th = 3238.1 MW (goal p-pump-basis trail:149,
    baseline_result.json@ffa5c54c), rounded to 195.0 [OWNER 2026-08-28];
    lower bound ~130 MW documented per Ruling 3
    */
}
```

`{...}` placeholders are filled at implement from the actual registry output (`location` field) and the actual extraction line numbers — the Ref lines must be first-order re-derivable at the cited lines, the same standard the goal round applied (trail:170). If an extraction garbles a figure, check the companion `images/` per the extraction-lossy rule before citing.

### D4. Registration inputs (drafted now, verified at implement)

Titles verified against the papers' own title blocks (never filename-derived): Cismondi = "Progress in EU Breeding Blanket design and integration" (confirmed in the existing extraction's title block, 2026-08-28); Moscato = "Progress in the design development of EU DEMO HCPB PHTS" (per the research file's attribution, `:43`; re-verify against the PDF title page at implement). Draft flags:

**Cismondi** (`--url .../WPPMICPR17_17709_submitted-4.pdf`):
- `--use-for`: "Helium-primary circulator power basis for the stellarator p_pump re-base (WI-033, DI-008): ~150 MW for EU DEMO HCPB, one order of magnitude above water-cooled (~15 MW). Serves RQ-2/RQ-5."
- `--validation`: "Re-derive the ~150 MW helium circulating-power figure and the water ~15 MW comparison at their printed locations; cross-check against the existing concept-research extraction warrant lines (scipub-wp-content-uploads-eurofusion-wppmicpr17-17709.md:174)."
- `--caveat`: "EUROfusion preprint WPPMI-CPR(17) 17709, not the journal version. The 150 MW figure is preliminary for one unoptimized loop layout; the paper's own authors expect it to fall (pressure-drop reduction studies ongoing)."

**Moscato** (`--url .../WPBOPCPR18_20276_submitted.pdf`):
- `--use-for`: "Helium-primary pumping-system design basis (EU DEMO HCPB PHTS): 2101.7 MWth, 9 loops x 2 compressors at 6.8/7.5 MW (~131 MW, 6.2%); near-term 8-loop design 83-94 MW (~4%) — the documented lower bound for p_pump (WI-033, DI-008)."
- `--validation`: "Re-derive the per-compressor powers (6.8 IB / 7.5 OB MW; near-term 5.9/5.2 MW), loop count, and 2101.7 MWth at their printed tables; totals ~131 MW and 83-94 MW must reconstruct arithmetically."
- `--caveat`: "SOFT 2018 preprint (EUROfusion WPBOP-CPR(18) 20276), not the journal version. Second-order quotes of these figures already exist in knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md:43 — this registration upgrades them to first-order."

Duplicate-detection note: Cismondi's extraction under `knowledge/concept_research/31-…/` is a *concept-research* artifact, not a registry entry; the registry has no row for either source (checked: zero `SOURCE_INDEX.md`/manifest hits), so `registered` is the expected outcome for both. `duplicate` would be a stop-and-look, not a proceed.

### D5. The runbook flip and the goal amendment (one commit)

The four `GOAL_RUNBOOK.md` edits are executed exactly per the archived recipe (`.project/completed/20260828_goal-research-model-proof/design.md:231`); the `integrate` row `:258` and bullet `:265` are not touched. The flip commit message names its resting evidence: "flip rests on live registrations C-REG-CIS/C-REG-MOS (write door); the request/return bookkeeper has not yet run end-to-end."

`goal.md` (closed) gets a dated operator's-pen entry in § Amendments — no body rewrite:

> **2026-08-28 (WI-033).** The `research` seam repair (GSTH Item 2) has now been used live: Cismondi and Moscato registered natively through `scripts/source_registry.py` (commits {C-REG-CIS}/{C-REG-MOS}); `GOAL_RUNBOOK.md` § The native seams flipped per the archived Item 5 recipe. The § "The two seams that will bite" research bullet (:130) and reserved-gate 4's hand-pattern sentence describe the pre-flip state and are superseded on this point. `integrate` remains unrepaired (GSTH Item 6).

### D6. DI-008 first-order revisit

After C-REG-MOS: locate the band figures in the registered Moscato extraction at cited lines, reconstruct the totals arithmetically, cross-check tables against `images/` (extractions are lossy — equations and tables garble). Expected: figures confirm (they were quoted from this paper into the WI-031 research file). Then:
- **Confirm** → one paragraph in `verification_record.md` § DI-008 revisit; no DI edit (correction-over-accretion: a confirmation is not an amendment).
- **Moved** → dated amendment on DI-008 via the owner (surfaced first — DI amendments on owner-ruled content are not the agent's pen).

### D7. Census re-derive, only on evidence

Run `tests/models` first. If `test_mfe_census_is_the_one_captured_from_the_first_clean_package` fails on the fingerprint assert (its own message instructs the re-derive), regenerate the fixture from the fresh package per the test's procedure and commit it in C-TESTS with the old→new fingerprint recorded. If the suite is green, C-TESTS does not exist. No other fixture, package, or store is touched either way.

## Cross-File Bindings

None change. The edit is one literal in one design attribute, present identically in the two twin homes; `p_pump` flows through the existing `mfe_plant.sysml:290` binding into the power balance. No import, no new element, no library change.

## Validation Plan

| Check | Mechanism | Expected |
|---|---|---|
| Syntax + structure | `uv run agentic-mbse validate models/` | L1 0/0; L2 = the 12 pre-existing WARNs, count and locations unchanged |
| Twin identity + generation + census | `uv run python -m pytest tests/models` (env sourced) | green; census fixture re-derived iff fingerprint moved (D7) |
| Registrations | registry JSON outputs | both `registered`, exit 0; paths exist; zero hand edits to the two registry files (git authorship) |
| Flip ordering | `git merge-base --is-ancestor C-REG-MOS C-FLIP` | true |
| Flip scope | `git show C-FLIP --stat` and diff | only `GOAL_RUNBOOK.md` (4 spots) + `goal.md` § Amendments |
| Regen fence | `git status` / diff over committed packages & `exploration/stellarator_e2e/studies/` | zero diff |
| SV-037 | `pm update-validation SV-037 --status passing` at close | recorded |

## Validation Report

Prototype executed 2026-08-28 (pre-approval, reverted): value edit in both twins → **L1 PASS** (0 errors / 0 warnings, 22 files), **L2 unchanged** (12 pre-existing WARNs, none new), twins byte-identical (`cmp` clean), tree reverted to clean. Level 3+ deferred to implement (no structural change; L4–L6 untouched by a literal edit — confirmed by the WI-030 precedent that offender lists only move on structural edits).

## Implementation Checklist (plan-model input)

1. Register Cismondi → C-REG-CIS; register Moscato → C-REG-MOS (D4; expect `registered` twice).
2. First-order re-derivation of both sources' figures at cited lines (D6 prep; capture line numbers for D3's Ref fields).
3. Edit both twins per D3 with real paths/lines → validate → C-MODEL.
4. `tests/models`; census re-derive iff fingerprint moved → C-TESTS (conditional).
5. Runbook flip + goal.md amendment → C-FLIP; check ancestry predicate.
6. DI-008 disposition (confirm-note or surface for amendment), `verification_record.md`, SV-037 → passing → C-CLOSE.

## Risks

1. **Registry `duplicate` or `holdout_hit`** — not expected (no existing rows; neither source is ARIES-CS material). Either outcome is a stop-and-surface, not an improvise.
2. **Extraction garbles the warrant figures** (tables are the lossy case) → image-inspection protocol before citing; if a figure cannot be re-derived at any cited line, that half stops and surfaces (no-fallback rule).
3. **Census fingerprint ambiguity** — if the fingerprint moves but `by_entry_type` also changes (it should not — no name changes), stop: that would mean the edit did more than intended.
4. **Scope creep into `research_seam.py`** — D1 explicitly keeps the bookkeeper unexercised; any urge to "just run a request too" is manufactured ceremony, declined by design.
