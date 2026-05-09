---
name: concept-research-navigation
description: >
  Use when asking about "concept research", "dossier", "research data", "verify claim",
  "check sources", "concept sources", "companion directory", "source extraction",
  "check images", "source quality", "research directory", "iter-*/sources",
  "Haiku paraphrase", "extraction quality",
  or when navigating concept research directories, evaluating source reliability,
  verifying quantitative claims against images, or assessing data sufficiency for a concept.
  Provides methodology for working with concept research in knowledge/concept_research/.
allowed-tools: Read, Grep, Glob
user-invocable: false
---

# Concept Research Navigation

Methodology for finding, evaluating, and using concept research data in `knowledge/concept_research/`.

## Core Principle

Research data is evidence, not truth. Every source has a quality tier and an extraction method. Dossiers synthesize across sources but are not authoritative for specific claims. Individual sources are authoritative for what they contain, but text extraction is lossy — images may hold data the text doesn't. Always trace quantitative claims to the most authoritative representation available.

## Data Layout (Brief)

For full directory structure, R2 sync setup, and format details, see `knowledge/concept_research/README.md`. Minimal orientation:

- Concept directories: `knowledge/concept_research/{concept-id}/` (e.g., `11-magnetic-mirror/`)
- Start with `{concept-id}/dossier.md` for synthesized overview
- Evidence in `{concept-id}/iter-NN/sources/*.md` — check ALL iterations

## Source Discovery Protocol

To find research for a given concept:

1. **If you know the concept ID**: go to `knowledge/concept_research/{concept-id}/`
2. **If you don't**: check `knowledge/concept_research/SOURCE_INDEX.md`, or glob `knowledge/concept_research/*/dossier.md`
3. **Read `dossier.md`** for orientation — what the concept is, key parameters, which sources exist
4. **Find evidence** in `iter-NN/sources/*.md` — check ALL iterations, later ones may add new sources
5. **For each source**, check if companion directory `iter-NN/sources/{name}/` exists. Its presence indicates richer data: images, original artifacts (`raw.html`/`raw.pdf`), and extraction metrics

## Source Evaluation

Three quality tiers. How to identify and how much to trust:

| Tier | How to identify | Trust level |
|------|----------------|-------------|
| **Direct extraction** | YAML frontmatter with `source:`, `backend:`, `content_hash_sha256:` | Authoritative for what it contains. Text may be lossy — verify quantitative data against images. |
| **Haiku paraphrase** | No YAML frontmatter, starts with `# Title` directly (or is a `.orig.md` file) | Lossy summary by Haiku. Specific numbers and technical details may be wrong. Flag as unverified if citing values. |
| **Dossier** | `dossier.md` at concept root | Synthesized overview. Good for orientation. Do NOT treat as authoritative for specific numbers — trace claims to individual sources. |

**Source authority hierarchy** when sources disagree:
- Peer-reviewed paper > technical report > company website > news article > Haiku paraphrase
- Direct extraction > Haiku paraphrase (for the same underlying source)
- Later iteration > earlier iteration (for the same topic)

## Image Inspection Protocol

When you MUST read images:

1. **You see `![](images/...)` in the text** — the content (equation, figure) exists ONLY in the image
2. **You are extracting a number** for analysis or modeling — cross-check against the table image
3. **The text references a table or figure by number** ("see Table 3") — find the corresponding image
4. **Numbers don't add up** or text seems garbled — the missing data is probably in a table/figure image

**Path resolution**: refs in a source `.md` like `![](images/page_003_table_0.png)` are relative to the companion directory → `iter-NN/sources/{name}/images/page_003_table_0.png`.

**If `images/` is empty**: binaries are R2-synced. Run `./scripts/sync_research.sh pull`.

## Cross-Referencing Methodology

To verify a claim:

1. Find the claim in the dossier or analysis
2. Trace to the cited source file
3. Find the specific section/table/figure in the source
4. For quantitative values: check the companion dir `images/` for the authoritative table/figure image
5. If the source text seems incomplete, check `raw.html`/`raw.pdf` in the companion dir or fetch the original URL from YAML frontmatter

To handle contradictions:
- Note both values with their sources
- Apply the authority hierarchy (peer-reviewed > company > paraphrase)
- If both are peer-reviewed, note the discrepancy — it may reflect different assumptions or time periods
- Flag for human review if the contradiction affects a modeling decision

## Confidence Assessment

| Level | Criteria | Action |
|-------|----------|--------|
| **Well-sourced** | Value appears in a direct-extraction source with image verification | Use directly, cite the source |
| **Source-backed but unverified** | Value appears in text extraction but not cross-checked against image | Use with note: verify against source images if precision matters |
| **Paraphrase-only** | Value appears only in Haiku paraphrase (no frontmatter source) | Flag as `[unverified]`, seek better source |
| **Inferred** | Value derived from related data in sources | Flag as `[inferred]` with derivation reasoning |
| **Estimated** | Value based on analogy to similar concepts | Flag as `[estimated]` with analogue basis |

## Related Skills

- For citation formatting and the DI→PR→model traceability chain: **source-traceability**
- For SysML doc comment syntax: **sysml-conventions**
- For project directory layout beyond concept research: **project-structure**
