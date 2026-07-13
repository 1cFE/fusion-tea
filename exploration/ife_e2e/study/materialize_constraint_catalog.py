"""Bridge sysml-codegen's embedded constraint catalog to teax's expected file (W4).

**Named schema gap (Appendix C surfacing, not a silent workaround):** sysml-codegen's Item 9
seals a package with the constraint catalog EMBEDDED in ``contracts/model_contract.json``
(the ``constraint_catalog`` key — see ``ConstraintCatalog`` in
``sysml_codegen.contracts.models``). teax's Item 12 (``simkit.study.config``,
``simkit.study.cli``, ``simkit.study.query._Catalog``) reads a STANDALONE
``contracts/constraint_catalog.json``, with different field names
(``usage_name``/``source_usage``/``owner_qn``/``definition_qn``/``source_form`` vs.
sysml-codegen's ``usage_qualified_name``/``definition_qualified_name``/``formal_names``).
teax's own fixture at
``teax/packages/teax-simkit/simkit/tests/evaluation/fixtures/sealed_package/package_live/
contracts/constraint_catalog.json`` is hand-authored to the shape teax's Item 12 code
expects — it was never validated against a real sysml-codegen Item 9 artifact, and this is
the first time the two sides have been run against each other. Item 9 and Item 12 do NOT
interoperate as-is. This script is fusion-tea's harness-side bridge — it does not touch
sysml-codegen or teax source (both out of this session's sandbox), so this repo's copy of
Appendix C can still "route the sweep through the study layer" as specified. The mismatch
itself is recorded for the Phase-6 reconcile, not papered over.

Only one field is genuinely synthesized (not renamed/copied): ``source_form`` is set to the
literal ``"definition_typed"`` for every record, since every constraint usage this repo's
models emit is of that form (``assert constraint <name> : '<Def>' { ... }`` — a usage typed
by a constraint definition). sysml-codegen's Item 9 output carries no explicit source-form
field to copy from.

Run:  uv run python exploration/ife_e2e/study/materialize_constraint_catalog.py <package_dir>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def materialize(package_dir: Path) -> Path:
    model_contract = json.loads((package_dir / "contracts" / "model_contract.json").read_text())
    embedded = model_contract["constraint_catalog"]
    if embedded is None:
        raise ValueError(f"{package_dir}: model_contract.json carries no constraint_catalog")

    # source_records: sysml-codegen keys by definition; teax keys by usage. This package's
    # catalog carries exactly one usage per definition today (no def reused by two usages),
    # so the definition's own short name search below is unambiguous; a future model with a
    # shared constraint def used by multiple usages would need real usage-level source data
    # sysml-codegen does not currently emit (a second, larger gap this bridge cannot close).
    source_by_def_qn = {r["definition_qualified_name"]: r for r in embedded["source_records"]}

    out_source_records = []
    out_concrete_entries = []
    for entry in embedded["concrete_entries"]:
        usage_qn = entry["usage_qualified_name"]
        usage_name = usage_qn.rsplit("::", 1)[-1]
        owner_qn = usage_qn.rsplit("::", 1)[0]

        # Recover which definition this usage was typed by via the predicate_ir's own
        # definition-scoped qualified names (every feature_ref target_qn shares the
        # definition's QN prefix) rather than assuming a 1:1 def<->usage order.
        definition_qn = None
        for def_qn in source_by_def_qn:
            if f"{def_qn}::" in entry["predicate_ir"]:
                definition_qn = def_qn
                break
        if definition_qn is None:
            raise ValueError(f"cannot recover definition for usage {usage_qn!r}")
        src = source_by_def_qn[definition_qn]

        out_source_records.append({
            "usage_name": usage_name,
            "source_form": "definition_typed",
            "membership_kind": entry["membership_kind"] or "assert",
            "is_negated": entry["is_negated"],
            "owner_qn": owner_qn,
            "definition_qn": definition_qn,
            "predicate_ir": entry["predicate_ir"],
            "source_location": None,
        })
        out_concrete_entries.append({
            "constraint_id": entry["constraint_id"],
            "source_usage": usage_name,
            "owner_instance": entry["owner_instance_path"],
            "membership_kind": entry["membership_kind"] or "assert",
            "is_negated": entry["is_negated"],
            "expected_value": entry["expected_value"],
        })

    catalog = {"source_records": out_source_records, "concrete_entries": out_concrete_entries}
    out_path = package_dir / "contracts" / "constraint_catalog.json"
    out_path.write_text(json.dumps(catalog, indent=2) + "\n")
    return out_path


if __name__ == "__main__":
    written = materialize(Path(sys.argv[1]))
    print(f"wrote {written}")
