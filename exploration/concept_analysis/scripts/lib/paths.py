"""Path constants for the concept analysis pipeline.

All paths are resolved relative to the concept_analysis directory.
"""

from pathlib import Path

# lib/paths.py lives at scripts/lib/paths.py
# .parent = lib/, .parent.parent = scripts/, .parent.parent.parent = concept_analysis/
CONCEPT_ANALYSIS_DIR = Path(__file__).resolve().parent.parent.parent
TABLE_PATH = CONCEPT_ANALYSIS_DIR / "table.csv"

# Item 5 upstream tables — the orchestrator's source of truth (keyed on concept_id).
TABLES_DIR = CONCEPT_ANALYSIS_DIR / "tables"
ONTOLOGY_PATH = TABLES_DIR / "ontology.csv"
ARCHETYPE_FIT_PATH = TABLES_DIR / "archetype_fit.csv"
COMPARABLES_PATH = TABLES_DIR / "comparables.csv"
DESIGN_POINT_PATH = TABLES_DIR / "design_point.csv"
# Judged-freeform discriminator; created lazily by Item 5's proposal batch.
# Missing file means "no concepts judged freeform yet" (empty set), not an error.
FREEFORM_ROUTES_PATH = TABLES_DIR / "design_point_freeform_routes.md"

ANALYSES_DIR = CONCEPT_ANALYSIS_DIR / "analyses"
HANDWRITTEN_DIR = CONCEPT_ANALYSIS_DIR / "handwritten"
TEMPLATES_DIR = CONCEPT_ANALYSIS_DIR / "prompt_templates"
BRIEF_PATH = CONCEPT_ANALYSIS_DIR / "concept_analysis_brief.md"
MEMORY_DIR = CONCEPT_ANALYSIS_DIR / "memory"

REPO_ROOT = Path(__file__).resolve().parents[4]
RESEARCH_DIR = REPO_ROOT / "knowledge" / "concept_research"
SOURCE_INDEX_PATH = REPO_ROOT / "knowledge" / "SOURCE_INDEX.md"

PHASE_1A_DIR = CONCEPT_ANALYSIS_DIR.parent / "phase_1a"
SCHEMA_PATH = PHASE_1A_DIR / "schema.md"

# 1costingfe reference paths (read-only)
COSTINGFE_DIR = Path("/home/reid/1cfe/1costingfe")
COSTINGFE_EXAMPLES_DIR = COSTINGFE_DIR / "examples"
COSTINGFE_DEFAULTS_DIR = COSTINGFE_DIR / "src" / "costingfe" / "data" / "defaults"
COSTINGFE_CONSTANTS_PATH = COSTINGFE_DEFAULTS_DIR / "costing_constants.yaml"
COSTINGFE_README_PATH = COSTINGFE_DIR / "README.md"

# Free-form model exemplar
FREEFORM_EXEMPLAR_PATH = Path("/home/reid/1cfe/tea-models/maglif/maglif_lcoe_model.py")

# Extraction output filename (matches agentic-mbse convention)
EXTRACT_OUTPUT = "output.md"
