# Implementation Plan: Visualization Options

**Status:** Draft
**Created:** 2026-01-19 02:32:08 UTC
**Last Updated:** 2026-01-19 02:32:08 UTC

## Source Documents
- **Spec:** `.project/active/visualization-options/spec.md`
- **Design:** `.project/active/visualization-options/design.md` ← See here for component details, function signatures, architecture

## Implementation Strategy

**Phasing Rationale:**
1. **Cost coloring first** - Most complex logic; validates strategy pattern early
2. **Labels second** - Simple, independent feature; quick win
3. **Tree layout last** - Most invasive (data transformation); depends on understanding how other features interact with layout changes

**Overall Validation Approach:**
- Manual testing with coffee_maker model after each phase
- Existing Python tests unchanged (data extraction not modified)
- Each phase produces visually verifiable output

---

## Phase 1: Cost Coloring Strategy System

### Goal
Replace global min/max cost coloring with percentage-of-parent strategy. Implement as swappable system per spec requirement.

**Why first:** This is the riskiest logic change. If the strategy pattern or parent lookup has issues, we discover early before adding more complexity.

### Test Approach
No automated tests for frontend JS in this POC. Validation is manual:
- Load coffee_maker model
- Enable "Color by Cost"
- Verify: panel (86% of housing) is more red than shell (14% of housing)
- Verify: root node (coffee_maker) is neutral/light color

### Changes Required

**See `design.md#4-cost-coloring-strategy-system` for:**
- Strategy enum definition
- `computeGlobalMinMax()` function
- `computePercentOfParent()` function
- Refactored `applyCostStyling()` function

**Specific file changes:**

#### 1. Add Strategy Enum and State
**File:** `proof_of_concept/web/static/index.html:312-314` (after `let expandCollapseApi = null;`)
- [x] Add `CostColorStrategy` enum object
- [x] Add `let currentCostStrategy = CostColorStrategy.PERCENT_OF_PARENT;`

#### 2. Add Strategy Functions
**File:** `proof_of_concept/web/static/index.html:~549` (before `lerpColor` function)
- [x] Add `computeGlobalMinMax(nodes, costAttr)` function
- [x] Add `computePercentOfParent(nodes, costAttr)` function

#### 3. Replace applyCostStyling
**File:** `proof_of_concept/web/static/index.html:563-593`
- [x] Replace entire `applyCostStyling` function with strategy-based version from design

### Validation

**Manual:**
- [x] Load model: `models/tests/coffee_maker`
- [x] Enable "Color by Cost" toggle
- [x] Verify root (`coffee_maker`) is light blue (neutral - no parent)
- [x] Verify `panel` is visibly more red than `shell` (86% vs 14% of housing)
- [x] Verify `brewing` and `housing` show different intensities (48% vs 30% of root)
- [x] Toggle off - all nodes return to default blue

**Regression:**
- [x] Run: `uv run pytest proof_of_concept/tests/` → All pass (33 passed)

**What We Know Works After This Phase:**
- Cost coloring strategy system is functional
- Percentage-of-parent calculation produces visible differentiation
- Strategy is swappable by changing `currentCostStrategy` constant

---

## Phase 2: Label Positioning Toggle

### Goal
Add UI toggle to switch container labels between border (default) and inside positioning.

**Why now:** Independent of other changes, low risk, delivers immediate UX improvement.

### Test Approach
Manual visual verification:
- Toggle on: container labels (brewing, housing) move to center of box
- Toggle off: labels return to top border

### Changes Required

**See `design.md#1-ui-controls` and `design.md#2-label-positioning-toggle` for:**
- HTML control markup
- `applyLabelStyle()` function

**Specific file changes:**

#### 1. Add HTML Control
**File:** `proof_of_concept/web/static/index.html:237` (after cost-styling-toggle label)
- [x] Add "Labels Inside" checkbox with label

#### 2. Add applyLabelStyle Function
**File:** `proof_of_concept/web/static/index.html:~595` (after applyCostStyling)
- [x] Add `applyLabelStyle(labelsInside)` function from design

#### 3. Update setButtonsEnabled
**File:** `proof_of_concept/web/static/index.html:488-500`
- [x] Add `document.getElementById('labels-inside-toggle').disabled = !enabled;`

#### 4. Add Event Handler
**File:** `proof_of_concept/web/static/index.html:~637` (in DOMContentLoaded, after cost toggle handler)
- [x] Add change event listener for `labels-inside-toggle`

### Validation

**Manual:**
- [x] Load model: `models/tests/coffee_maker`
- [x] Verify "Labels Inside" checkbox appears and is enabled after load
- [x] Toggle ON: `brewing` and `housing` labels move to center of their boxes
- [x] Toggle OFF: labels return to top border position
- [x] Leaf nodes (heater, pump, etc.) should be unaffected (already centered)

**Regression:**
- [x] Cost coloring still works with labels inside
- [x] Expand/collapse still works
- [x] PNG export still works

**What We Know Works After This Phase:**
- Label positioning toggle functional
- Dynamic style changes work on container nodes
- No interference with other features

---

## Phase 3: Tree Layout

### Goal
Add layout selector to switch between containment (nested boxes) and tree (edge-based hierarchy) views.

**Why last:** Most invasive change - transforms data structure, affects how other features work.

### Test Approach
Manual visual verification:
- Switch to tree: edges appear, boxes flatten, hierarchy preserved
- Switch back to containment: nested boxes restored
- Features (cost coloring, labels) work in both modes

### Changes Required

**See `design.md#3-tree-layout` and `design.md#5-edge-styling` for:**
- `transformToTreeData()` function
- `switchLayout()` function
- Edge styles
- State management (`originalElements`)

**Specific file changes:**

#### 1. Add Global State
**File:** `proof_of_concept/web/static/index.html:314` (after expandCollapseApi)
- [x] Add `let originalElements = null;`
- [x] Add `let parentLookup = new Map();` (for cost coloring in tree mode)

#### 2. Add Edge Styles to Stylesheet
**File:** `proof_of_concept/web/static/index.html:309` (before closing `]` of stylesheet array)
- [x] Add edge selector with styles from design

#### 3. Add HTML Control
**File:** `proof_of_concept/web/static/index.html:~240` (after labels-inside-toggle)
- [x] Add layout select dropdown

#### 4. Add Layout Functions
**File:** `proof_of_concept/web/static/index.html:~600` (after applyLabelStyle)
- [x] Add `transformToTreeData(elements)` function from design
- [x] Add `switchLayout(layoutType)` function from design

#### 5. Store Original Elements on Load
**File:** `proof_of_concept/web/static/index.html:529` (in loadModel, after `hideMessage()`)
- [x] Add `originalElements = data.elements;`
- [x] Add parent lookup caching

#### 6. Update computePercentOfParent for Tree Mode
**File:** `proof_of_concept/web/static/index.html` (in computePercentOfParent function)
- [x] Change `node.data('parent')` to use `parentLookup.get(node.id())` fallback

#### 7. Update setButtonsEnabled
**File:** `proof_of_concept/web/static/index.html:488-500`
- [x] Add `document.getElementById('layout-select').disabled = !enabled;`

#### 8. Add Event Handler
**File:** `proof_of_concept/web/static/index.html:~640` (in DOMContentLoaded)
- [x] Add change event listener for `layout-select`

#### 9. Reset Layout Select on Load
**File:** `proof_of_concept/web/static/index.html:529` (in loadModel success)
- [x] Add `document.getElementById('layout-select').value = 'containment';`

### Validation

**Manual - Tree Layout:**
- [ ] Load model: `models/tests/coffee_maker`
- [ ] Switch to "Tree" layout
- [ ] Verify: edges appear connecting nodes
- [ ] Verify: hierarchy is correct (coffee_maker → brewing → heater/pump/chamber)
- [ ] Verify: no nested boxes (all nodes same visual level)

**Manual - Layout Switching:**
- [ ] Switch back to "Containment"
- [ ] Verify: nested boxes restored exactly as before
- [ ] Switch between layouts multiple times - no errors

**Manual - Feature Integration:**
- [ ] In Tree mode: enable "Color by Cost" → colors still work correctly
- [ ] In Tree mode: enable "Labels Inside" → labels positioned correctly
- [ ] In Containment mode: both features still work

**Manual - Edge Cases:**
- [ ] Expand/collapse buttons: may not work in tree mode (acceptable per design risks)
- [ ] PNG export works in tree mode

**Regression:**
- [ ] `uv run pytest proof_of_concept/tests/` → All pass

**What We Know Works After This Phase:**
- Layout switching preserves data integrity
- Tree view shows correct hierarchy with edges
- Cost coloring works in both modes (via parentLookup cache)
- All features work together

---

## Environment Setup

**See CLAUDE.md for full environment rules**

Key commands:
- Run server: `uv run uvicorn proof_of_concept.web.server:app --reload`
- Run tests: `uv run pytest proof_of_concept/tests/`
- Test model path: `models/tests/coffee_maker`

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: Division by zero handled in `computePercentOfParent` with `parentCost > 0` check
- **Phase 3**: Parent lookup cached at load time to support cost coloring in tree mode
- **Phase 3**: Expand/collapse may not work in tree mode - acceptable, document in UI if needed

---

## Implementation Notes

*[TO BE FILLED DURING IMPLEMENTATION]*

### Phase 1 Completion
**Completed:** 2026-01-19
**Actual Changes:**
- Added `CostColorStrategy` enum at line 317 with `GLOBAL_MINMAX` and `PERCENT_OF_PARENT` strategies
- Added `currentCostStrategy` state variable defaulting to `PERCENT_OF_PARENT`
- Added `computeGlobalMinMax(nodes, costAttr)` function at line 559
- Added `computePercentOfParent(nodes, costAttr)` function at line 580
- Replaced `applyCostStyling` function with strategy-based version at line 615

**Issues:** None
**Deviations:** None - implementation followed design exactly

### Phase 2 Completion
**Completed:** 2026-01-19
**Actual Changes:**
- Added "Labels Inside" checkbox control in control bar at line 238
- Added `applyLabelStyle(labelsInside)` function at line 669
- Updated `setButtonsEnabled()` to enable/disable and reset labels toggle
- Added event handler for labels-inside-toggle at line 739

**Issues:** None
**Deviations:** Omitted spacer div between toggles (not needed, looks fine adjacent)

### Phase 3 Completion
**Completed:** 2026-01-19
**Actual Changes:**
- Added `originalElements` and `parentLookup` global state at line 329
- Added edge styles to stylesheet at line 313
- Added layout select dropdown in control bar at line 245
- Added `transformToTreeData()` function at line 711
- Added `switchLayout()` function at line 734
- Store original elements and build parent lookup in loadModel at line 564
- Updated `computePercentOfParent()` to use parentLookup fallback for tree mode
- Updated `setButtonsEnabled()` to manage layout-select
- Added event handler for layout-select at line 840

**Issues:** None
**Deviations:** None - implementation followed design exactly

---

**Status**: Draft → In Progress → Complete
