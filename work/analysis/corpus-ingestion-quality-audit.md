# First Corpus Ingestion: Extraction Quality Audit

**Date:** 2026-02-09
**Auditor:** Claude (automated)
**Epic:** KNOW-DB Item 4
**Pipeline:** `scripts/zotero_ingest.py` with `--enhance` (default)

---

## Summary

| # | Source | Key | Lines | Headings | Tables | Images | Overall |
|---|--------|-----|-------|----------|--------|--------|---------|
| 1 | Hawker — Simplified economic model for inertial fusion | `LCZMWLYM` | 917 | FAIL | FAIL | PASS | **FAIL** |
| 2 | Swanson et al. — Helios stellarator design | `7E42ICWG` | 2417 | FAIL | FAIL | PASS | **FAIL** |
| 3 | Delene et al. — Economics of future electric power | `XH2I672M` | 1132 | PASS | FAIL | PASS | **CRITICAL FAIL** |
| 4 | Hsu et al. — ARPA-E ALPHA costing revisit | `6I8Z5PBZ` | 303 | FAIL | FAIL | PASS | **FAIL** |
| 5 | Waganer — ARIES cost account documentation | `HJMWLC47` | 4625 | FAIL | FAIL | PASS | **FAIL** |

**All 5 sources pass on images. All 5 fail on tables. 4 of 5 fail on headings.**

Source 3 (Delene) has a critical issue: LLM dialogue contamination from the `--enhance` pass.

---

## Detailed Findings

### Source 1: Hawker — A simplified economic model for inertial fusion

**Slug:** `a_simplified_economic_model_for_inertial_fusion`
**Zotero Key:** `LCZMWLYM`
**Document length:** 917 lines

#### Headings: FAIL

The document has a correct H2/H3 hierarchy but is **flat** — nearly all sections are H2 with only a few H3 subsections. The original paper likely uses section labels like (a), (b) which were extracted as plain text rather than nested headings.

Extracted heading structure:
```
## Abstract
## The cost of electricity
## Previous studies
## Model
## Results and discussion
  ### Correlation analysis
  ### Dependence on individual parameters
  ### Addition of gain curves
  ### Minimum cost design point
## Conclusion
## Acknowledgements and References
```

Not critically broken, but the flat hierarchy loses the original paper's sub-section structure.

#### Tables: FAIL

**3 tables severely corrupted.** The extraction converted table headers to strikethrough (`~~text~~`) and filled data cells with dot-padding instead of proper markdown table syntax.

**Example — Table 1 (line 102):**
```
~~LCOE ($/MWh)~~ ~~fexibility cost ($/MWh)~~ ~~CCS cost ($/MWh)~~
solar PV 35 +15 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
onshore wind 35 +15 . . . . . . . . . . . . . . . . . . . . . . . . . . . .
```

**Example — Table 2 (line 221):**
```
~~parameter~~ ~~symbol~~ ~~units~~
availability _μa_              . . . . . . . . . . . . . . . . . . .
blanket multiple _Eb_            . . . . . . . . . . . . . . . . . .
```

**Root cause:** The PDF uses multi-column layout with dot leaders between columns. The extractor failed to parse these as tabular data.

#### Images: PASS

5 PNG files in `images/`. All 5 referenced correctly in `full_document.md` with valid `![](images/...)` syntax. File sizes are reasonable (non-zero, properly extracted).

---

### Source 2: Swanson et al. — Overview of the Helios Design

**Slug:** `overview_of_the_helios_design_a_practical_planar_coil`
**Zotero Key:** `7E42ICWG`
**Document length:** 2417 lines

#### Headings: FAIL

The H2/H3 structure is mostly correct through Sections 1-3 (proper `## Section` / `### Subsection` nesting). However:

1. **Section 4 subsections are italicized text, not headings.** All 4.x subsections were extracted as `_4.1. Electromagnetic coil engineering_` (italic plain text) rather than `### 4.1 Electromagnetic coil engineering` (H3 headings). This affects 7 subsections:
   ```
   _4.1. Electromagnetic coil engineering_       (line 734)
   _4.2. Divertor engineering and the first wall_ (line 774)
   _4.3. Neutronics, blanket, shield, and bioshield_ (line 831)
   _4.4. Thermal cycle, power flows, and fuel cycle_ (line 895)
   _4.5. Cryostat, maintenance, and cryogenic system_ (line 968)
   _4.6. Electrical systems and power supplies_   (line 1025)
   _4.7. Instrumentation and control_             (line 1062)
   ```
   These subsections DO have corresponding `### Subsection Name` headings (e.g., `### Coil Structure and Materials` at line 736), so navigation still works — the numbered sub-labels are just missing from the heading hierarchy.

2. **Duplicate headings at section boundaries:**
   - Lines 1084-1085: Both `## 5. Conclusion` and `## Summary and Future Work` appear as separate H2 headings
   - Lines 1110-1111: Both `## 6. Acknowledgments` and `## Acknowledgments` appear

#### Tables: FAIL

The primary Global Parameters table (lines 212-236) has correct pipe-delimited structure but contains cell content artifacts:
- HTML tags: `10 MW (startup)<br><1 MW (ignited)` (line 218)
- Strikethrough in numeric values: `2.1 × 10~~20 ~~/m~~3~~` (line 223) — should be `2.1 × 10²⁰ /m³`
- Garbled text: `_fS udo_` (line 225) — should be `f_Sudo`
- Typo: "efciency" instead of "efficiency" (line 229)

#### Images: PASS

13 PNG files in `images/`. All 13 referenced correctly in `full_document.md`. Covers all figures (Helios equilibrium, architecture, POPCON, coil sets, Poincaré sections, stress analysis, Sankey diagram, etc.).

#### References: FAIL (bonus finding)

The references section (lines 1658+) has severely fragmented DOI URLs:
```
`doi:10` . `[1088/1741-4326/ada56c](https://doi.org/10.1088/1741-4326/ada56c)` .
```
DOIs were split into backtick-delimited code segments. URLs are technically present but broken across formatting boundaries.

---

### Source 3: Delene et al. — An Assessment of the Economics of Future Electric Power Generation Options

**Slug:** `an_assessment_of_the_economics_of_future_electric_power`
**Zotero Key:** `XH2I672M`
**Document length:** 1132 lines

#### CRITICAL ISSUE: LLM Dialogue Contamination

The `--enhance` pass injected **20+ instances** of LLM conversational dialogue directly into the document body. These are requests from the enhancement model asking to "see the image" to convert equations/tables — the responses were not filtered out before saving.

**Example contamination (lines 354, 392, 427, etc.):**
```
I notice you mentioned an image showing the original PDF page, but no image was
actually provided in your message. Could you please share the image or PDF so I
can see the equation you'd like converted to LaTeX?
```

```
I need to see the image to convert the equation to LaTeX. Could you please share
the image/screenshot of the original PDF page?
```

These passages are interspersed throughout the document, breaking table rows and disrupting content flow. The contamination appears at approximately **20 distinct locations** spanning ~200+ lines of injected text.

#### Headings: PASS (structure only)

The heading hierarchy is actually well-structured:
```
## ORNL/TM-1999-243
## 1. INTRODUCTION
## 2. ANALYSIS PROCEDURES
## 3. PLANT DESIGNS
## 4. COST MODELS
  ### 4.1 FINANCE COSTS
  ### 4.2 CAPITAL INVESTMENT COSTS
  ### 4.3 O&M COSTS
  ### 4.4 FUEL COSTS
  ### 4.5 DECOMMISSIONING COSTS
  ### 4.6 EMISSIONS ABATEMENT COSTS
## 5. RESULTS
## 6. DISCUSSION OF RESULTS
## 7. CONCLUSION
## REFERENCES
```

Minor issues: `## TDD 703-487-4639` (line 30) is a phone number erroneously marked as H2; `## 0 ORNL 99-1415 EFG` (line 929) is a page footer erroneously marked as H2.

#### Tables: FAIL

Tables are present but severely disrupted by LLM dialogue injections. The underlying table structure appears to use pipe-delimited markdown, but conversational text is inserted between table rows, splitting them.

**Example — Table 11, Levelized COE (around line 826):**
Table data is present but followed immediately by:
```
I need to see the image to accurately convert the equation. Could you please
share the PDF image so I can see the original formatting?
```

#### Images: PASS

13 PNG files in `images/`. All referenced correctly. File naming is consistent.

#### Recommendation

**Re-extract with `--no-enhance --force`.** The base extraction (without LLM enhancement) will produce a clean document. The LLM enhancement pass is the sole source of contamination. This is a known failure mode where the enhance model fails to process embedded images and instead outputs dialogue asking for them.

---

### Source 4: Hsu et al. — Revisit of the 2017 Costing for Four ARPA-E ALPHA Concepts

**Slug:** `revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts`
**Zotero Key:** `6I8Z5PBZ`
**Document length:** 303 lines

#### Headings: FAIL

Most headings are correct H2:
```
## Project Information
## Acknowledgements
## Executive Summary
## Principal Findings
## Cost Categories
```

However, line 82 contains a **reference citation erroneously formatted as a heading:**
```
## science facility, a credible break-in step on the path to fusion energy," Fus. Eng. Design 135B, 236 (2018);
```

This is a continuation of reference [7] (lines 79-84) that got a `##` prefix during extraction. No H3 headings exist — the document is flat.

#### Tables: FAIL

3 tables present, all with the same issues:

1. **Placeholder column headers.** All tables use `|Col1|Average|Low|High|Col5|` — the first and last columns have generic `Col1`/`Col5` placeholders instead of semantic labels (likely "Parameter" and "Units").

2. **HTML `<br>` tags in cells.** Multi-line cell content uses raw HTML instead of proper markdown:
   ```
   |Operations and Maintenance Costs<br>COM|48.2|42.0|61.3|M$/annum|
   |Decontamination and<br>Decommissioning Costs CDD|0.5|0.5|0.5|mills/kWh or<br>M$/MWh|
   ```

3. **Inconsistent column counts.** Some rows have empty trailing cells (e.g., `|Nmod|3.0|2.0|4.0||`).

**Tables affected:**
- Table 2 (lines 149-158): System parameters
- Table 3 (lines 244-279): Capital costs (~35 rows)
- Table 4 (lines 285-296): Cost of Electricity

#### Images: PASS

5 PNG files in `images/`. All referenced correctly. File sizes range from 19K to 157K (valid).

---

### Source 5: Waganer — ARIES Cost Account Documentation

**Slug:** `aries_cost_account_documentation`
**Zotero Key:** `HJMWLC47`
**Document length:** 4625 lines (largest document)

#### Headings: FAIL

The heading structure is extensive (100+ headings) and follows a logical H2/H3 hierarchy matching the ARIES cost account structure. However:

1. **Title is H2 instead of H1:** Line 5 uses `## University of California, San Diego UCSD-CER-13-01`
2. **Data table headers promoted to headings:** Line 94 `## Year IPD` and line 1746 `## $/W,` are table column headers erroneously marked as H2
3. **Spurious section-level headings from table content:** Line 1784 `## ECRF Del Power, MW 1992$,LSA 1, 2 1992$, LSA4 2009$, LSA4 Unit Cost, $/W` is a table header row marked as H2

The core section structure is correct and navigable:
```
## Purpose
## Background
## Historical Cost Escalation
## General Cost Account Information
  ### Direct and Indirect Capital Costs
  ### Spare Parts
  ### Contingency
  ### Level of Safety Assurance
## Detailed Capital Cost Accounts
## Land and Land Rights, Account 20
## Structures and Site Facilities, Account 21
  ### Site Improvements and Facilities, Account 21.01
  ### Power Core Building, Account 21.02
  ... (continues through all ARIES cost accounts)
## Special Materials, Account 27
## Indirect Costs, Accounts 91-99
## Financial Assumptions and Methodologies
## Operations and Maintenance Costs
## Scheduled Component Replacement Costs
## Fuel Cost
## Decontamination and Decommissioning
## References
## Appendix A: Recommended Cost Accounts
## Appendix B: Power Core Component and Material Cost Basis
```

#### Tables: FAIL

Mixed quality — some tables are well-formed, others severely corrupted.

**Well-formed examples:**
- Table 4, ARIES LSA Factors (lines 301-320): Clean columns with proper separators
- GDP IPD values table (lines 94-137): Clean Year/IPD columns

**Corrupted examples — multi-column cell duplication and HTML artifacts:**

Lines 86-88:
```
|measure of annual inflation.|The cost estimate bases provided in this document...|Col3|
|<br>in both the year originally...|<br>in both the year originally...|<br> <br>|
```

Lines 331-338:
```
|In 2010, the ARIES|project decided to forgo the LSA factors...|Col3|
|<br>for each subsystem and system|<br>for each subsystem and system|<br>  . If is felt...|
```

**Patterns observed:**
- `Col2`, `Col3`, `Col4` placeholder markers where cells failed to extract
- Content duplicated across multiple columns (same text in 2-4 cells)
- `<br>` HTML tags instead of proper cell breaks
- Paragraph text forced into table format when it should be plain prose

#### Images: PASS

25 PNG files in `images/`. All 25 referenced correctly in `full_document.md`. Consistent naming scheme. This is a comprehensive set covering the many figures and charts in the ARIES cost documentation.

---

## Recommendations

### Immediate Action Required

| Source | Action | Command |
|--------|--------|---------|
| 3 (Delene) | **Re-extract without enhancement** | `uv run python scripts/zotero_ingest.py --local-pdf knowledge/raw/Delene*.pdf --no-enhance --force` |

### Optional Remediation

Sources 1, 2, 4, 5 have typical PDF extraction artifacts. These documents are **usable for research and reference** despite the formatting issues — the text content, figures, and overall structure are intact. Table data can be interpreted by a human reader even with formatting artifacts.

If higher-quality tables are needed for specific downstream tasks:
- Re-extract with `--backend docling` (alternative PDF parser)
- Re-extract with `--no-enhance` to get baseline without LLM artifacts
- Manual cleanup of specific tables as needed

### Root Cause Analysis

| Issue Pattern | Affected Sources | Likely Cause |
|--------------|-----------------|--------------|
| LLM dialogue injection | Source 3 | `--enhance` model fails on embedded images, outputs conversation instead of content |
| Strikethrough headers / dot padding in tables | Source 1 | Dot-leader table format in PDF not recognized as tabular data |
| `Col1`-`Col5` placeholder headers | Sources 4, 5 | PDF table header extraction failure — column names not parsed |
| `<br>` HTML in markdown tables | Sources 4, 5 | Multi-line cell content converted to HTML instead of markdown |
| Content duplicated across table columns | Source 5 | Merged cells in PDF mis-interpreted as separate columns with same content |
| Italicized subsections instead of headings | Source 2 | PDF formatting distinction between section numbering and heading text |
| DOI fragmentation in references | Source 2 | URL tokenization error during extraction |

---

## Validation Checklist

- [x] Quality audit notes recorded for each source
- [x] Pass/fail assessed per dimension (headings, tables, images)
- [x] Root causes identified
- [x] Re-extraction recommended for critically corrupted source (Delene)
- [ ] Re-extraction of Source 3 completed
- [ ] Re-extraction re-audited
