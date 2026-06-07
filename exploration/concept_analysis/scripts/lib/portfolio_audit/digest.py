"""Build the cohort digest — the lead reviewer's load-bearing context payload.

``build_digest(records, manifest)`` emits one compact per-concept entry (the
schema in design.md "cohort_digest.json schema") so the Opus lead can reason
*across* the whole cohort without reading every analysis. Per concept it carries:

* record metadata (name, family, subfamily, maturity, fit_grade, p_native,
  comparables) — from the joined concept record;
* headline numbers (LCOE native/1GWe, overnight native/1GWe, the 17-account CAS
  rollup native/1GWe) — parsed from the *static* ``model_output.txt`` artifact;
* enabled cost overrides (account / provenance / value) — from the
  ``model_setup.py`` AST (no execution);
* ``import_status`` / ``model_stale`` / ``last_iter_ts`` — copied from the
  ``manifest`` so the digest is self-contained without re-importing anything.

Execution-free by construction: it reads text and parses an AST. The numbers are
the artifact's record of what was produced; when a model is stale the manifest's
``model_stale`` flag tells the lead the numbers may not reflect current code.
"""

from __future__ import annotations

import ast
import re

from lib.paths import ANALYSES_DIR
from lib.portfolio_audit.probe import CAS_COLUMNS

SCHEMA_VERSION = "1"

# model_output.txt line patterns. Keyed off the line shape (not line number) so
# the Windows-env warning preamble is ignored. Native-vs-1GWe columns:
# the headline "LCOE:" line is the 1 GWe projection; "Native LCOE =" is native.
_LCOE_1GW_RE = re.compile(r"^LCOE:\s*(-?[\d.]+)\s*\$/MWh", re.MULTILINE)
_LCOE_NATIVE_RE = re.compile(r"^Native LCOE\s*=\s*(-?[\d.]+)\s*\$/MWh", re.MULTILINE)
_OVERNIGHT_RE = re.compile(
    r"^Overnight:\s*generic\s+(-?[\d.]+)\s*\$/kW"
    r"\s+native\s+(-?[\d.]+)\s*\$/kW"
    r"\s+1\s+GWe\s+(-?[\d.]+)",
    re.MULTILINE,
)
# A CAS rollup row: "CAS22   <generic>   <native>   <1 GWe>". Sub-account rows
# ("C220103 ...") and the TOTAL row don't start with "CAS\d+", so they're skipped.
_CAS_ROW_RE = re.compile(
    r"^(CAS\d+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)", re.MULTILINE
)


def build_digest(records: list[dict], manifest: dict) -> dict:
    """Cohort digest for the ``records``, copying audited-state from ``manifest``."""
    manifest_concepts = manifest.get("concepts", {})
    return {
        "schema_version": SCHEMA_VERSION,
        "built_at": manifest.get("timestamp", ""),
        "cas_columns": list(CAS_COLUMNS),
        "concepts": {
            record["concept_id"]: _digest_entry(
                record, manifest_concepts.get(record["concept_id"], {})
            )
            for record in records
        },
    }


def _digest_entry(record: dict, manifest_state: dict) -> dict:
    concept_id = record["concept_id"]
    concept_dir = ANALYSES_DIR / concept_id
    output_path = concept_dir / "model_output.txt"
    setup_path = concept_dir / "model_setup.py"

    parsed = _parse_model_output(
        output_path.read_text(encoding="utf-8") if output_path.exists() else ""
    )
    overrides = (
        _enabled_overrides_from_ast(setup_path.read_text(encoding="utf-8"))
        if setup_path.exists()
        else []
    )
    design_point = record.get("design_point") or {}

    return {
        "id": concept_id,
        "name": record.get("concept_name", ""),
        "company": record.get("company", ""),
        "family": record.get("confinement_family", ""),
        "subfamily": record.get("confinement_subfamily", ""),
        "maturity": design_point.get("maturity_tier", ""),
        "fit_grade": record.get("fit_grade", ""),
        "p_native_mwe": _to_float(design_point.get("p_native_mwe")),
        "lcoe_native_usd_per_mwh": parsed["lcoe_native_usd_per_mwh"],
        "lcoe_1gw_usd_per_mwh": parsed["lcoe_1gw_usd_per_mwh"],
        "overnight_native_usd_per_kw": parsed["overnight_native_usd_per_kw"],
        "overnight_1gw_usd_per_kw": parsed["overnight_1gw_usd_per_kw"],
        "cas_native": parsed["cas_native"],
        "cas_1gw": parsed["cas_1gw"],
        "enabled_overrides": overrides,
        "comparables": list(record.get("comparables", [])),
        "last_iter_ts": manifest_state.get("last_iter_ts", ""),
        "model_stale": manifest_state.get("model_stale", False),
        "import_status": manifest_state.get("import_status", ""),
    }


def _parse_model_output(text: str) -> dict:
    """Pull LCOE / overnight / CAS rollups out of a ``model_output.txt`` body.

    Missing values degrade to None (ungrounded concepts print
    ``LCOE: (NOT ENOUGH DATA …)``; an absent file yields all-None). CAS rollups
    are 17-long lists in ``CAS_COLUMNS`` order, None for any column not printed.
    """
    overnight = _OVERNIGHT_RE.search(text)
    cas_native: dict[str, float] = {}
    cas_1gw: dict[str, float] = {}
    for m in _CAS_ROW_RE.finditer(text):
        cas_native[m.group(1)] = float(m.group(3))
        cas_1gw[m.group(1)] = float(m.group(4))

    return {
        "lcoe_native_usd_per_mwh": _first_float(_LCOE_NATIVE_RE, text),
        "lcoe_1gw_usd_per_mwh": _first_float(_LCOE_1GW_RE, text),
        "overnight_native_usd_per_kw": float(overnight.group(2)) if overnight else None,
        "overnight_1gw_usd_per_kw": float(overnight.group(3)) if overnight else None,
        "cas_native": [cas_native.get(col) for col in CAS_COLUMNS],
        "cas_1gw": [cas_1gw.get(col) for col in CAS_COLUMNS],
    }


def _enabled_overrides_from_ast(source: str) -> list[dict]:
    """Enabled entries of the module-level ``overrides = [...]`` list, via AST.

    Returns ``[{account, provenance, value_musd}]`` for entries with
    ``enabled: True``. ``value_musd`` is the literal value when it's a plain
    number (most overrides), or None when it's a relative expression
    (e.g. ``0.70 * generic.costs.cas21``) that the AST can't evaluate without
    running the model — the account + provenance still carry the signal. A
    syntactically broken ``model_setup.py`` yields no overrides (its import
    failure is already recorded in the manifest).
    """
    if not source.strip():
        return []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "overrides" for t in node.targets
        ):
            return _parse_override_list(node.value)
    return []


def _parse_override_list(list_node: ast.expr) -> list[dict]:
    if not isinstance(list_node, ast.List):
        return []
    out: list[dict] = []
    for elt in list_node.elts:
        if not isinstance(elt, ast.Dict):
            continue
        entry = _ast_dict_to_py(elt)
        if entry.get("enabled") is True:
            out.append({
                "account": entry.get("account"),
                "provenance": entry.get("provenance"),
                "value_musd": entry.get("value"),
            })
    return out


def _ast_dict_to_py(dict_node: ast.Dict) -> dict:
    """{str key: literal value-or-None} for an ``ast.Dict`` of an override entry."""
    out: dict = {}
    for key, value in zip(dict_node.keys, dict_node.values):
        if isinstance(key, ast.Constant) and isinstance(key.value, str):
            out[key.value] = _literal_or_none(value)
    return out


def _literal_or_none(node: ast.expr):
    """A Python literal for a constant (or negated constant) AST node, else None."""
    if isinstance(node, ast.Constant):
        return node.value
    if (
        isinstance(node, ast.UnaryOp)
        and isinstance(node.op, ast.USub)
        and isinstance(node.operand, ast.Constant)
    ):
        return -node.operand.value
    return None


def _first_float(regex: re.Pattern, text: str) -> float | None:
    m = regex.search(text)
    if not m:
        return None
    try:
        return float(m.group(1))
    except ValueError:
        return None


def _to_float(value) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
