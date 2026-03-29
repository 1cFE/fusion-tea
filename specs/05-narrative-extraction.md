
## Purpose
Extract structured `NarrativeData` from a concept's `analysis.md` via a `claude -p` call with a structured output requirement.

## Requirements
- The extraction function calls `claude -p` with the full `analysis.md` text and the `NarrativeData` JSON schema
- The LLM is instructed to restructure and summarize existing content — not invent new content
- The response is validated via `NarrativeData.model_validate_json()` — validation failure raises, not silently degrades
- `top_risks` is capped at 5 entries, ranked by `RiskSeverity`
- `eliminated_costs` and `novel_costs` are populated only when explicitly stated or clearly implied in the analysis — not inferred
- The extraction runs before the synthesis stage, operating on `analysis.md` alone
- The output is written as the `narrative` field in the concept's JSON output

## Acceptance Criteria
- Given a valid `analysis.md`, the extraction produces a `NarrativeData` that passes `model_validate_json()`
- Given `analysis.md` text that mentions exactly 7 risks, `top_risks` contains at most 5 entries sorted by severity
- Given an analysis with no explicit mention of eliminated costs, `eliminated_costs` is an empty list
- Given a malformed or empty LLM response, the function raises with a message identifying the concept and the validation error
- The extraction prompt includes the `NarrativeData` JSON schema (via `model_json_schema()`) in the system or user message

## Interfaces
- **Function**: `extract_narrative(concept_dir: Path) -> NarrativeData` in `extract_explorer_data.py`
- **Input**: `analysis.md` path (and optionally `model_output.txt` for grounding key bets)
- **Output**: `NarrativeData` instance (see `01-data-models.md`)
- **Called by**: `06-data-extraction-pipeline.md`
- **External dependency**: `claude` CLI invoked via subprocess with `--output-format json`

## Constraints
- NEVER allow narrative extraction to silently produce empty or partial `NarrativeData` — fail loudly
- NEVER hallucinate content not present in the source `analysis.md`
- The LLM response MUST be validated against the Pydantic schema before use
- `claude -p` output format is JSON event stream — the result text is in the last event with `type: "result"`, key `"result"` (known quirk from memory)

## Out of Scope
- Narrative display (see `17-concept-profile-page.md`)
- Synthesis-stage extraction (this spec covers `analysis.md` only)
- Manual authoring of narrative fields

