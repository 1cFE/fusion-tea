# End-to-End Validation Plan: Concept 11 — Magnetic Mirror (D-T)

**Purpose:** Validate the full enhanced pipeline on a fresh concept (not the concept 08 development target)
**Concept:** 11-magnetic-mirror — Magnetic Mirror (D-T), Realta Fusion
**Starting state:** gap-checked (G) — has `gap_report.md` only
**Ending state:** approved (A) — full artifact set

---

## Why Concept 11

- **Different confinement family** from concept 08 (MFE Open/Linear vs MIF FRC) — tests generalization
- **Uses costingfe MIRROR mapping** (family-level, not concept-specific override) — tests the family fallback path
- **D-T fuel** (vs D-He3 for concept 08) — different fuel economics
- **6 extracted sources** — moderate data availability, rated "Significant Gaps" — realistic test case
- **No handwritten holdout** — validates the pipeline stands on its own without a comparison target

---

## Pre-Flight Check

```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py status | grep "11-magnetic-mirror"
```

- [ ] Shows `11-magnetic-mirror   Magnetic Mirror (D-T)   G`
- [ ] Directory contains only: `gap_check_prompt.md`, `gap_report.md`

---

## Step 1: Analyze

```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py analyze 11
```

### Validation Criteria

**Files produced:**
- [ ] `analysis.md` exists (expect 30–50 KB based on concept 08 baseline of 44 KB)
- [ ] `analysis_prompt.md` exists
- [ ] No `analysis_body.md` left behind (temp file should be cleaned up)

**Frontmatter (script-controlled):**
- [ ] Starts with `---`
- [ ] `ID: 11-magnetic-mirror`
- [ ] `Concept: Magnetic Mirror (D-T)`
- [ ] `Company: Realta Fusion`
- [ ] `Status: draft`
- [ ] `Created:` is today's date
- [ ] `Reuses:` is `[]` or lists specific approved concept IDs (01, 07, 08, 21 are currently approved)

**Content quality — spot-check these against sources:**
- [ ] Mentions WHAM experiment (17 T REBCO magnets, first plasma July 2024)
- [ ] Mentions Hammir pilot plant targets (Qe > 1, >50 MWe)
- [ ] Mentions MARS study as historical analogue
- [ ] Mentions dual-channel energy conversion (thermal + direct)
- [ ] Parameter table present with Source column entries including `§Section` references (not just filenames)
- [ ] At least 3 direct block quotes present (citation traceability upgrade)
- [ ] Cross-concept comparison section present (likely referencing concept 06 — Magnetic Mirror p-B11)

**State transition:**
```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py status | grep "11-magnetic-mirror"
```
- [ ] Shows `D` (drafted)

---

## Step 2: Model Setup

```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py model-setup 11
```

### Validation Criteria

**Files produced:**
- [ ] `model_setup.py` exists (expect 15–30 KB)
- [ ] `model_setup_prompt.md` exists
- [ ] `model_output.txt` exists (auto-run after generation)

**Model setup script — structural checks:**
- [ ] Imports `from costingfe import CostModel, ConfinementConcept, Fuel`
- [ ] Uses `ConfinementConcept.MIRROR` (not TOKAMAK or other)
- [ ] Uses `Fuel.DT`
- [ ] Has inline traceability comments citing analysis.md parameters
- [ ] Has `UNCERTAIN` or `HIGH UNCERTAINTY` flags on at least 2 parameters
- [ ] Includes sensitivity analysis section

**Model output — sanity checks:**
- [ ] `model_output.txt` contains "LCOE" (case-insensitive)
- [ ] LCOE value is in the 30–200 $/MWh range (sanity bounds for any fusion concept)
- [ ] Output is non-trivial (>500 bytes — not just an error message)

**Costingfe path verification:**
- [ ] Prompt references `dt_mirror.py` example (not `dhe3_pulsed_frc.py`)
- [ ] Prompt references `mfe_mirror.yaml` defaults

**State transition:**
```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py status | grep "11-magnetic-mirror"
```
- [ ] Shows `M` (model-setup)

---

## Step 3: Review

```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py review 11
```

### Validation Criteria

**Files produced:**
- [ ] `review.md` exists (expect 15–35 KB)
- [ ] `review_prompt.md` exists

**Review structure:**
- [ ] Contains `### CV-` (citation verification) findings
- [ ] Contains `### CALC-` (calculation verification) findings
- [ ] Contains `### MSA-` (model setup audit) findings
- [ ] Contains `### PA-` (proposed action) sections
- [ ] Each PA has: Category, Severity, Location, Finding, Proposed Fix, Decision (blank), User Notes (blank)

**PA parseability:**
```bash
uv run python -c "
from pathlib import Path
import sys
sys.path.insert(0, 'exploration/concept_analysis/scripts')
from run_analysis import parse_proposed_actions
text = Path('exploration/concept_analysis/analyses/11-magnetic-mirror/review.md').read_text()
pas = parse_proposed_actions(text)
print(f'{len(pas)} PAs parsed')
for pa in pas:
    print(f'  PA-{pa[\"number\"]}: {pa[\"category\"]} / {pa[\"severity\"]}')
    assert pa['decision'] == '', f'Decision should be blank, got: {pa[\"decision\"]}'
print('All PAs have blank decisions — ready for user input')
"
```
- [ ] All PAs parse successfully (no crashes)
- [ ] All Decision fields are blank
- [ ] At least 3 PAs produced (concept 08 had 8)

**Frontmatter updated on analysis.md:**
- [ ] `Review-Iterations: 1`
- [ ] `Last-Review:` is today's date
- [ ] `Review-Status: has-actions` (or `clean` if no issues found — unlikely)

**State transition:**
- [ ] Status still shows `M` (review metadata lives on analysis.md, but state requires addressed/clean for `R`)

---

## Step 4: Fill In Review Decisions

**Manual step.** Open `exploration/concept_analysis/analyses/11-magnetic-mirror/review.md` and for each `### PA-N:` section, fill in:
- `**Decision:** agree` (or `alternative` or `reject` with explanation)
- Optionally add `**User Notes:**`

### Validation Criteria
- [ ] Every PA has a non-empty Decision field
- [ ] Decisions are one of: `agree`, `alternative`, `reject`

---

## Step 5: Address Review

```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py address-review 11
```

### Validation Criteria

**Files produced/modified:**
- [ ] `address_log.md` exists — lists each PA and the action taken
- [ ] `analysis.md` modified — diff shows changes corresponding to agreed PAs
- [ ] `model_setup.py` modified if any MSA findings were agreed

**Model re-run (automatic):**
- [ ] `model_output.txt` updated (timestamp newer than before address-review)
- [ ] LCOE value still in sanity range (30–200 $/MWh) — may have changed from step 2

**Frontmatter updated on analysis.md:**
- [ ] `Review-Status: addressed`

**State transition:**
```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py status | grep "11-magnetic-mirror"
```
- [ ] Shows `R` (reviewed)

---

## Step 6: Synthesize

```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py synthesize 11
```

### Validation Criteria

**Files produced:**
- [ ] `synthesis.md` exists (expect 10–20 KB)
- [ ] `synthesis_prompt.md` exists
- [ ] No `synthesis_body.md` left behind (temp file should be cleaned up)

**Frontmatter (script-controlled):**
- [ ] `ID: 11-magnetic-mirror`
- [ ] `Concept: Magnetic Mirror (D-T)`
- [ ] `Company: Realta Fusion`
- [ ] `Type: synthesis`
- [ ] `Status: draft`
- [ ] `Created:` is today's date
- [ ] No hallucinated fields (e.g., no `Analysis-Version`)

**7 mandatory sections present:**
- [ ] `## 1. Executive Summary` — 3-5 bullets (risk, advantage, LCOE, confidence)
- [ ] `## 2. What Matters Most for LCOE` — 3-5 parameters ranked with elasticities
- [ ] `## 3. Risk Verdicts` — each challenge gets Likely/Unlikely/Genuinely uncertain
- [ ] `## 4. Structural Advantages and Disadvantages` — comparison vs D-T tokamak baseline
- [ ] `## 5. Cross-Concept Positioning` — landscape context, references other concepts
- [ ] `## 6. Modeling Confidence` — High/Medium/Low with parameter table
- [ ] `## 7. What Would Change My Mind` — 2-3 specific items

**Voice quality — the synthesis should NOT read like the analysis:**
- [ ] Contains at least 2 opinionated verdict statements (not hedged with "may" or "could")
- [ ] References specific LCOE numbers from model output
- [ ] References specific sensitivity elasticities
- [ ] Mentions mirror-specific economics (e.g., DEC revenue, simpler geometry vs tokamak, MARS heritage)

**Cross-concept context:**
- [ ] References at least one approved concept (01, 07, 08, or 21) by name or ID
- [ ] Prompt included approved prior syntheses (concept 08's synthesis.md should appear)

**State transition:**
```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py status | grep "11-magnetic-mirror"
```
- [ ] Shows `S` (synthesized)

---

## Step 7: Approve

```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py approve 11
```

### Validation Criteria

**Frontmatter updated on analysis.md:**
- [ ] `Status: approved`
- [ ] `Approved-Date:` is today's date

**Frontmatter updated on synthesis.md:**
- [ ] `Status: approved`
- [ ] `Approved-Date:` is today's date

**State transition:**
```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py status | grep "11-magnetic-mirror"
```
- [ ] Shows `A` (approved)

---

## Final State Verification

```bash
ls -la exploration/concept_analysis/analyses/11-magnetic-mirror/
```

**Complete artifact set (11 files):**
- [ ] `gap_check_prompt.md` — from prior gap-check phase
- [ ] `gap_report.md` — from prior gap-check phase
- [ ] `analysis_prompt.md` — saved prompt
- [ ] `analysis.md` — reviewed, addressed, approved analysis with citations
- [ ] `model_setup_prompt.md` — saved prompt
- [ ] `model_setup.py` — runnable LCOE model using costingfe MIRROR
- [ ] `model_output.txt` — model execution output with LCOE
- [ ] `review_prompt.md` — saved prompt
- [ ] `review.md` — structured review with filled-in PA decisions
- [ ] `address_log.md` — log of applied review changes
- [ ] `synthesis_prompt.md` — saved prompt
- [ ] `synthesis.md` — editorial synthesis with controlled frontmatter

**Additional prompt file:**
- [ ] `address_review_prompt.md` — saved prompt (13 files total)

**No leftover temp files:**
- [ ] No `analysis_body.md`
- [ ] No `synthesis_body.md`

**Status summary line:**
```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py status | tail -3
```
- [ ] Approved count increased by 1 (was 4, now 5)

---

## Gate Enforcement Regression Checks

Run these at any point to verify ordering enforcement hasn't regressed:

```bash
# Should refuse — concept 02 is only gap-checked, not reviewed
uv run python exploration/concept_analysis/scripts/run_analysis.py synthesize 02

# Should refuse — concept 02 has no analysis
uv run python exploration/concept_analysis/scripts/run_analysis.py model-setup 02

# Should refuse — concept 02 has no synthesis
uv run python exploration/concept_analysis/scripts/run_analysis.py approve 02
```

- [ ] All three refuse with helpful skip messages (not crashes)
