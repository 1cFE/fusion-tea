VERDICT: FINDINGS

### F-1: C220104 (auxiliary heating) suppressed despite direct MANTA cost figure
- **Target:** Section 5b (Override Candidates)
- **Category:** analysis
- **Finding:** MANTA explicitly prices the 40 MW ICRF system at $370M (Table C1, same source table as the C220103 and C220108 overrides). The library computes $222.8M from p_input=40 — a $147M per-module gap. The analysis declines to override on the basis that ohmic-only operation might eliminate the heating system entirely, calling the requirement "genuinely uncertain." That logic conflates a scenario question (will a future design drop auxiliary heating?) with the current design-point cost (MANTA retains 40 MW ICRF at $370M). By the same reasoning, TF coils and divertor would also be "uncertain" if a future design changed them — but the analysis correctly overrides those from MANTA. The result is that the model's C220104 is $222.8M rather than either the MANTA-conservative $370M or the ohmic-only $0M; it represents neither scenario accurately, and the library value has no design-point grounding.
- **Recommendation:** Author a C220104 override at $370M (`provenance: direct`, source: manta-reference-design.md §7.1 Table C1) representing the conservative case where auxiliary heating is retained. Carry ohmic-only elimination as an explicitly named scenario branch (e.g. a disabled override at value 0.0 with a note that it applies if H_NA = 2.0 validates at reactor scale). Do not leave the account at a library regression value that doesn't correspond to either design scenario.
- **Priority:** important
