# AACE provenance grounding check — 2026-09-16

[AGENT] Preparatory evidence for acceptance specification B-7. Goal-directory confirmation is pending; this note is not a native goal task return, completed comparison package, or independent review. No model or acceptance criterion changed.

## Raw-PDF check

[INHERITED: `.project/completed/20260821_demo-anchor-acceptance-spec/spec.md`, B-7] Check the in-repository arXiv table against its raw PDF and cite AACE 18R-97.

[AGENT] Read only the general cost-estimate-class table and nearby section on printed page 28 (zero-based PDF page 27) of `knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/arxiv-2602-19389/raw.pdf`. SHA256: `a471a9b54c22bf29c6fbc4744eb73ba63418fbbceb5519e20b006cf29fcf0c02`. The acceptance specification identifies this table as admissible. No ARIES-specific quantities were sought or read.

[AGENT] Tier-1 page extraction used `.codex-test/run python .agents/skills/pdf-analysis/scripts/extract_page.py <raw.pdf> 27 --mode markdown --output /tmp/aries-readiness-aace-table-page.md`. Visual verification used the same command with `--mode image --output /tmp/aries-readiness-aace-table-page.png`, followed by image inspection. Render SHA256: `1c649769bb0a3e2ee5d814ecbce251a7d70439ccc39132aa7762a1af7500c01e`.

[AGENT] Table 3's Class 5 row agrees with `output.md:1318–1328`: maturity 0%–2%; low range −30% to −50%; high range +30% to +100%. Its caption says 80% confidence; the footnote notes wider ranges can arise from novelty, scope ambiguity and limited data. This is a successful extraction-fidelity check, not evidence that this fusion estimate has demonstrated that confidence coverage.

## Primary-reference caveat

[AGENT] Consulted the official public sample of [AACE International Recommended Practice 18R-97, Cost Estimate Classification System—As Applied in Engineering, Procurement, and Construction for the Process Industries](https://web.aacei.org/docs/default-source/toc/toc_18r-97.pdf), revision August 7, 2020. Printed page 3, Table 1, gives the Class 5 low range as −20% to −50%, with the same +30% to +100% high range. Printed page 2 describes a guideline rather than a standard and excludes power-generating facilities. Thus the paper's table matches its extraction but is not an exact transcription of this recommended practice, and direct whole-plant AACE classification is not established.

[AGENT] This external lookup occurred during grounding before a native research request was opened. It is a provisional provenance observation; a later native task must retain the evidence and independent check under its own record rather than claiming a completed research-seam receipt. No knowledge registry or model source was mutated.

## Consequence for the comparison

[OWNER: current request; INHERITED: acceptance specification B-4/B-8] Retain model/reference [0.5, 2] exactly. [AGENT] The primary-reference caveat changes the accuracy claim's description, not those owner-preserved endpoints. Describe the band as the ratified project comparison criterion with conceptual-estimate motivation; do not represent agreement as engineering qualification, a formal AACE classification, or an empirically established 80% probability. Final independent review should verify this caveat and its treatment.
