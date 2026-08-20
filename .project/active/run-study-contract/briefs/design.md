# Brief: design for "Skill, Runbook, and Record Contract" (RUN-STUDY Item 2)

Work item home: `.project/active/run-study-contract/` — spec.md is ACCEPTED there; write design.md.

## Task

Design the three deliverable documents (`SKILL.md`, `runbook.md`, `record-template.md`), the
discovery-log row format, the `synthesis.md` convention, and the `.gitignore` change — to the
spec's contract. The spec's Known Requirements are settled; your job is the document
architecture and the spec's "Open Questions / Deferred to design" list:

1. Exact document layout: section order, heading text, fill-in skeleton vs checklist form.
2. Study-id convention (and how A/B arms are named within one record directory).
3. Snapshot placement: inline in record.md vs sibling snapshot.json referenced by digest.
   Weigh human readability against machine checkability; pick one and say why.
4. Framing-conditional sections: explicit "not applicable under <framing>" lines so omission
   is distinguishable from forgetting.
5. Record-path naming: skill owns it (design's assignment) or runbook step 1 — one, not both.

## Orchestrator rulings since the spec (record these in the design)

- The package annex FILE and its content are authored by **Item 4** (its content is era pin,
  oracle parameterization, glue — Item 4 material). Item 2 defines the annex LINK and the
  universal/annex split only. This supersedes the spec non-goal line that named Item 3.
- Item 3's accepted spec adds manifest facts your snapshot list references: the manifest
  carries an **indicator-input fingerprint** (tool-computed digest over the artifacts the
  trace reads) alongside the sealed executable_fingerprint and semantic_fingerprint. The
  record snapshot must carry all fingerprints the manifest declares — keep the snapshot
  field list open to "every fingerprint the manifest names" rather than a closed triple.
- Item 3's output JSON schema is versioned; the record's `indicators.json` snapshot should
  record that schema version.

## Constraints

- The runbook is universal — zero stellarator names anywhere in the three documents; package
  specifics appear only as "see the package annex" links.
- Do not write the runbook/skill/template content at design stage beyond illustrative
  skeletons — design the structure, the plan+implement stages write the documents.
- Keep judgment out of the documents' obligations: the runbook may demand "argue and record
  the framing", never "prefer search framing".
- Working voice rules apply. Provenance grades carried from the spec.

## Read

- `.project/active/run-study-contract/spec.md` (the contract)
- `.project/concepts/run-study-skill-design.md` — Core Model, Required Invariants
- `.project/active/run-study-indicators/spec.md` — the Item 3 seam (output schema, manifest)
- `.project/active/demo-proof-of-life/plan.md` — source material shape
