---
Status: approved
Created: 2026-08-28
Updated: 2026-08-28
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-033 Plan — P_pump Re-base

> Owner pre-approved the stage sequence 2026-08-28 ("approved, proceed to plan and implement").

## Source Documents

- `./design.md` (primary — D1–D7, prototype PASS report)
- `./spec.md` (MR-WI033-1…6, success criteria, SV-037)
- Mandate: `work/orchestration/goals/p-pump-basis/trail.md` § Goal close

## Design Summary

One literal (`p_pump` 1.0 → 195.0) plus its evidence trail, landed in commit order so proof rests on ancestry: registrations first (registry-authored commits), then the model edit citing the registered paths, then the runbook flip resting on the registrations. Design § D2 is the commit map; § D3–D6 carry the exact texts.

## Prototype Baseline

Design § Validation Report: value edit in both twins already proven — L1 0/0 over 22 files, L2 = the 12 pre-existing WARNs unchanged, twins byte-identical, reverted. No L4–L6 exposure (literal edit, no structure). No prototype files persist; Phase 2 re-applies the edit from design § D3.

## Branch

All work on `feat/wi033-p-pump-rebase` off current `main` (repo merge flow: agent pushes + opens PR, owner merges). Created in Phase 0.

## Phasing Approach

Five phases = the design's six-commit sequence, with registrations isolated first (they gate everything: doc-comment paths, flip evidence) and the conditional census step folded into the test phase. Every phase ends with a checkpoint; nothing proceeds over a red gate.

---

## Phase 0 — Branch + preflight

- [x] `git checkout -b feat/wi033-p-pump-rebase` (from clean `main`)
- [x] Commit the three PM artifacts (spec.md, design.md, plan.md, VALIDATION_MATRIX SV-037 row) — the item's paper trail lands first
- [x] `uv run python scripts/source_registry.py register --help` — confirm flag names against design § D4 before first live call
- [x] Confirm registry duplicate expectation: `grep -ci "cismondi\|moscato\|17709\|20276" knowledge/SOURCE_INDEX.md` → 0

**Gate**: branch exists; PM artifacts committed; registry interface matches D4.

**Deviation (owner-ruled 2026-08-28):** first Cismondi call returned `capture_failed` — seam
defect at `source_registry.py:485` (URL raw artifact hardcoded `raw.html`; PDF URLs store
`raw.pdf`). Fixed + regression test (`tests/research` 150 passed; targeted PDF-URL test
passed). Commit **C-FIX** precedes C-REG-CIS. Failed-attempt receipt kept at
`registry-cismondi-attempt1-capture_failed.json`. Spec § Scope Amendment / design § D1a.

## Phase 1 — Registrations (C-REG-CIS, C-REG-MOS)

Design ref: § D4 (drafted flags, verified titles), § Research Findings (URLs, hashes).

- [x] Register Cismondi: `--url .../WPPMICPR17_17709_submitted-4.pdf`, title "Progress in EU Breeding Blanket design and integration", D4 flags → expect `registered`, exit 0; keep JSON output for verification_record
- [x] Register Moscato: `--url .../WPBOPCPR18_20276_submitted.pdf` (unsuffixed; sha256 75f2417a… expected on raw), title re-verified against PDF title page, D4 flags → expect `registered`, exit 0; keep JSON
- [x] If either returns anything but `registered` → STOP, surface (design Risk 1; no improvising)
- [x] Record C-REG-CIS / C-REG-MOS commit SHAs (registry-authored commits)
- [x] First-order re-derivation, Cismondi: locate "~150MW … (~15MW)" + HCPB-representative-for-HCLL + 9km→3km in the REGISTERED extraction; note exact line numbers for D3 Ref
- [x] First-order re-derivation, Moscato: locate 2101.7 MWth; 9 loops / 2 compressors; 6.8/7.5 MW; near-term 5.9/5.2 MW; reconstruct ≈131 MW and 83–94 MW arithmetically; note line numbers; cross-check tables vs `images/` if garbled (design Risk 2: unreconstructable figure → STOP, surface)

**Gate**: two `registered` outcomes committed; all warrant figures re-derived at noted lines.

## Phase 2 — Model edit (C-MODEL)

Design ref: § D3 (full doc-comment text; fill `{...}` from Phase 1).

- [x] REFINE `models/designs/stellarator_09/stellarator_plant.sysml:502` — value 195.0 + D3 doc comment with real paths/lines
- [x] REFINE `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml:502` — identical bytes
- [x] `cmp` the two files → identical
- [x] `set -a; source ~/1cfe/agentic-mbse/.env; set +a; uv run agentic-mbse validate models/` → L1 0/0; L2 = 12 pre-existing WARNs, none new
- [x] Commit C-MODEL (both twins only)

**Gate**: validate matches prototype baseline; twins identical; commit contains exactly two files.

## Phase 3 — Tests (+ conditional C-TESTS)

Design ref: § D7.

- [x] `set -a; source ~/1cfe/agentic-mbse/.env; set +a; uv run python -m pytest tests/models`
- [x] If green → no C-TESTS; done
- [x] If ONLY the census fingerprint assert fails → re-derive `tests/models/data/mfe_census.json` per the test's own instruction; verify `by_entry_type` unchanged (names only — if it also moved, STOP: the edit did more than intended, design Risk 3); rerun suite green; commit C-TESTS (fixture only, old→new fingerprint in message)
- [x] Any other failure → STOP, surface

**Gate**: `tests/models` green; working tree clean except intended commits.

## Phase 4 — Runbook flip + goal amendment (C-FLIP)

Design ref: § D5; recipe at `.project/completed/20260828_goal-research-model-proof/design.md:231`.

- [x] `GOAL_RUNBOOK.md:256` — `research` row: drop "— **pending native repair**"; Native-return column → the native classes (registered sources, a queued candidate, or a bounded negative); question column unchanged
- [x] `:262` — "Two seams are not repaired yet" → one seam, naming `integrate`
- [x] `:264` — WI-031 hand-pattern bullet → pointer to `docs/research_seam_operator_guide.md`, `scripts/research_seam.py`, `scripts/source_registry.py`, `/research-acquire`
- [x] `:267` — closing sentence made singular
- [x] Verify `integrate` row `:258` and bullet `:265` byte-untouched in the diff
- [x] Append `goal.md` § Amendments entry per D5 text, with real C-REG SHAs
- [x] Commit C-FLIP (two files only); message names the resting evidence per D5 ("write door live; bookkeeper not yet run end-to-end")
- [x] `git merge-base --is-ancestor <C-REG-MOS> <C-FLIP>` → true (record in verification_record)

**Gate**: diff confined to the named spots; predicate true.

## Phase 5 — Close-out (C-CLOSE)

Design ref: § D6; spec § Success Criteria (all six).

- [x] DI-008 disposition: figures confirmed → paragraph in verification_record only; moved → STOP and surface to owner before any DI edit
- [x] Write `verification_record.md`: registry JSONs, re-derivation lines, validate/test outputs, ancestry predicate, regen-fence check (`git diff main --stat` shows zero touches under committed packages / `exploration/stellarator_e2e/studies/`)
- [x] Spec success criteria 1–6 checked off explicitly
- [x] `uv run agentic-mbse pm update-validation SV-037 --status passing`
- [x] Commit C-CLOSE
- [ ] Report to owner; owner sequences: PR open (+ `/_my_pre_pr` if shipping alone), then `pm close-item WI-033` after any audit they want

**Gate**: all spec criteria evidenced; SV-037 passing; branch pushed only when owner says.

---

## Validation Strategy

- Per-phase: L1/L2 via `agentic-mbse validate` after any model touch (Phase 2); full `tests/models` in Phase 3; scoped-diff checks in Phases 4–5.
- Final: verification_record aggregates every check against spec § Success Criteria; SV-037 flips to passing on that evidence.
- Not run here: package regeneration or study verification (MR-WI033-6 fence); `/audit-models` and `close-item` stay owner-sequenced.

## Feasibility Concerns

1. Registry behavior differing from the operator guide (flags, auto-commit) — Phase 0 `--help` check catches it before any live call.
2. Registry commit lands more than its four artifacts — inspect C-REG diffs before proceeding (paper trail must stay clean).
3. `tests/models` runtime includes live generation (SysIDE license required) — env sourcing is in every command line that needs it.
