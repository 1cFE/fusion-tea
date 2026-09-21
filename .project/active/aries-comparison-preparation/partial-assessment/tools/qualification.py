"""Case-scoped field applicability from the reviewed audit, not a physics test."""
from __future__ import annotations

from collections import deque

ROOTS = {
    "axis_field": {
        "module": "stellarator_09__stellaris__magnet__field_calc",
        "module_type": "mfe_magnet_field.Coil_Set_Axis_FieldModule",
        "channel": "stellarator_09__stellaris__magnet__field_calc__B_axis",
        "reason": "Field audit F1: fixed linkage is unqualified for the transferred coil geometry/current distribution.",
    },
    "peak_field": {
        "module": "stellarator_09__stellaris__magnet__peak_field_calc",
        "module_type": "mfe_plasma_scaling.Conductor_Peak_FieldModule",
        "channel": "stellarator_09__stellaris__magnet__peak_field_calc__B_peak",
        "reason": "Field audit F1/F2: transferred shape coefficients and omitted finite-pack dependence are unqualified.",
    },
}
AUDIT = ".project/active/aries-comparison-preparation/post-reveal-investigation/field-audit/audit.md"


def combine_qualifications(records):
    """Union field findings across row producers and model-definedness flags."""
    records = list(records)
    if not records:
        raise ValueError("Cannot qualify an empty set of dependencies")
    causes = {}
    for record in records:
        status = record["field_applicability"]
        if status not in ("unknown_unqualified", "unaffected_by_field_finding"):
            raise ValueError(f"Unknown field applicability: {status}")
        if (status == "unknown_unqualified") != bool(record["causes"]):
            raise ValueError("Field applicability and causes disagree")
        for cause in record["causes"]:
            causes[(cause["root"], tuple(cause["path"]))] = dict(cause)
    return {
        "field_applicability": "unknown_unqualified" if causes else "unaffected_by_field_finding",
        "causes": [causes[key] for key in sorted(causes)],
    }


def qualify(graph, diagnostic_document, contract):
    """Qualify all publications and catalog predicates for the audited request only.

    Dependencies are conservative at module granularity: every output of a
    consuming module inherits a finding, even if its internal formula could be
    independent. No numerical success, failure or scalar value certifies physics.
    """
    paths = {}
    for name, root in ROOTS.items():
        matches = [key for key, spec in graph.spec.modules.items()
                   if spec.module_type == root["module_type"]]
        if matches != [root["module"]]:
            raise ValueError(f"Missing/ambiguous pinned {name} module: {matches}")
        spec = graph.spec.modules[root["module"]]
        channels = [binding.channel_name for binding in spec.outputs.values()]
        if channels != [root["channel"]] or graph.channel_providers.get(root["channel"]) != root["module"]:
            raise ValueError(f"Pinned {name} output identity changed")
        reached = {root["module"]: [root["module"]]}
        queue = deque(reached)
        while queue:
            current = queue.popleft()
            for child in sorted(graph.adjacency[current]):
                if child not in reached:
                    reached[child] = reached[current] + [child]
                    queue.append(child)
        paths[name] = reached

    exits = [spec for spec in graph.spec.modules.values() if spec.is_exit]
    if len(exits) != 1:
        raise ValueError("Expected exactly one exit module")
    bindings = exits[0].outputs
    observations = diagnostic_document["publications"]
    if set(bindings) != set(observations):
        raise ValueError("Diagnostic publication coverage does not match graph")
    publications = {}
    for key, binding in bindings.items():
        producer = graph.channel_providers[binding.channel_name]
        observed = observations[key]
        if observed["producer"] != producer or observed["channel"] != binding.channel_name:
            raise ValueError(f"Diagnostic publication identity mismatch: {key}")
        causes = [
            {"root": name, "path": reached[producer], "reason": ROOTS[name]["reason"], "evidence": AUDIT}
            for name, reached in paths.items() if producer in reached
        ]
        publications[key] = {
            "field_applicability": "unknown_unqualified" if causes else "unaffected_by_field_finding",
            "execution_status": observed["status"],
            "producer": producer,
            "causes": causes,
        }
    predicates = {}
    for entry in contract["constraint_catalog"]["concrete_entries"]:
        key = entry["evaluation_channel"]
        constraint = entry["constraint_id"]
        if constraint in predicates:
            raise ValueError(f"Duplicate predicate: {constraint}")
        if key not in publications:
            raise ValueError(f"Missing predicate publication: {key}")
        predicates[constraint] = {**publications[key], "publication_key": key}
    return {
        "schema_version": "field-applicability/v1",
        "scope": "Retained first-forward three-input request only; findings do not mechanically certify any similarity family.",
        "dependency_granularity": "module-conservative",
        "unaffected_meaning": "Unaffected by this field finding only; scientific support is not established and other limitations remain.",
        "roots": {name: {**root, "field_applicability": "unknown_unqualified", "evidence": AUDIT}
                  for name, root in ROOTS.items()},
        "publications": publications,
        "predicates": predicates,
    }
