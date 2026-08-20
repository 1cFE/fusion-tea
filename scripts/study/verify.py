#!/usr/bin/env python3
"""Sample a study's own evidence and check it against the package's independent oracle.

Three claims, and each is earned rather than asserted:

* **Every observed verdict combination is sampled.** Stratification is a floor, never
  a cap: one case per stratum first, then a seeded random fill to the sample size. A
  plain random sample can miss a small stratum entirely, and the stratum a sample
  misses is exactly the one worth looking at.
* **Named channels agree at rel < 1e-9.** The worst deviation and where it occurred
  are recorded, so "agrees" carries a number.
* **Every verdict is re-derived**, from the package's own `predicate_ir` through the
  bindings the package publishes — never from a threshold hard-coded here. A generic
  tool cannot resolve a predicate operand to a package key by name: on a real package
  one operand of five constraints resolves to nothing at all, and three others are a
  guess among three composition rules. So the package publishes the bindings and this
  tool consumes them as data. `verdicts_rederived: true` is emitted only when every
  operand of every catalog constraint resolved; anything unresolved or ambiguous is a
  mechanical failure naming the constraint and the operand. A tool that guesses is
  worse than one that refuses.

Glue honesty is mandatory output, not a comment: any input fed identically to the
package and to the oracle is named in the summary as not independently verified,
because oracle parity then verifies the package's arithmetic *given* that value.

The store is sampled, not the exported CSV: the store is the primary evidence and the
only source keyed by qualified names. Stores are opened read-only and never written.

Usage:
    verify.py --package DIR --manifest FILE --identity FILE --store FILE...
              [--sample-size N] [--seed HEX] [--out FILE]

Generic by construction: this module names no package, no key prefix, and no adapter
(Invariant 1). It imports teax and whatever module the manifest names, and nothing
else about the package.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import random
import sys
from pathlib import Path

if __package__ in (None, ""):  # invoked as a script: put the repo root on sys.path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.study import common, identity  # noqa: E402
from scripts.study import manifest as manifest_mod  # noqa: E402

SUMMARY_SCHEMA_VERSION = "study-verification-summary/v1"
SAMPLING_SCHEME = "stratified-by-verdict-combination/v1"
TOLERANCE = 1e-9
DEFAULT_SAMPLE_SIZE = 12

TOOL_SOURCE_FILES = (
    "scripts/study/common.py",
    "scripts/study/identity.py",
    "scripts/study/manifest.py",
    "scripts/study/schemas/package_identity.v1.schema.json",
    "scripts/study/schemas/verification_summary.v1.schema.json",
    "scripts/study/verify.py",
)

#: Comparison operators an `expression-ir/v1` predicate may use. An operator outside
#: this set is a mechanical failure, never a verdict taken on trust.
OPERATORS = {
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
}


class VerifyError(common.ToolError):
    """A mechanical failure. Nothing interpretive raises."""


# ------------------------------------------------------------------ the oracle


def load_oracle(loaded: manifest_mod.LoadedManifest):
    """Import the module the manifest names, and require both published surfaces."""
    block = loaded.data["oracle"]
    if block["kind"] != "python_callable":
        raise VerifyError(f"unsupported oracle kind {block['kind']!r}")
    sys_path = manifest_mod.repo_root() / block["sys_path"]
    if not sys_path.is_dir():
        raise VerifyError(
            f"the manifest's oracle sys_path does not exist: {block['sys_path']}"
        )
    if str(sys_path) not in sys.path:
        sys.path.insert(0, str(sys_path))
    try:
        module = importlib.import_module(block["module"])
    except ImportError as exc:
        raise VerifyError(
            f"cannot import the oracle module {block['module']!r} under sys_path "
            f"{block['sys_path']}: {exc}"
        ) from exc
    if not hasattr(module, block["callable"]):
        raise VerifyError(
            f"the oracle module {block['module']!r} has no attribute {block['callable']!r}"
        )
    if not hasattr(module, "operand_bindings"):
        raise VerifyError(
            f"the oracle module {block['module']!r} publishes no 'operand_bindings': verdicts "
            f"cannot be re-derived without it, and this tool does not guess bindings by name"
        )
    return module, getattr(module, block["callable"]), module.operand_bindings()


def bindings_digest(bindings: dict) -> str:
    """A stable digest of the published binding table, so a record can cite it."""
    canonical = json.dumps(bindings, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# --------------------------------------------------------------- the predicate


def feature_refs(node) -> list[dict]:
    found = []
    if isinstance(node, dict):
        if node.get("kind") == "feature_ref":
            found.append(node)
        for value in node.values():
            found += feature_refs(value)
    elif isinstance(node, list):
        for value in node:
            found += feature_refs(value)
    return found


def resolve_operand(constraint_id: str, operand: dict, bindings: dict,
                    case_inputs, package_inputs, channels) -> float:
    """One operand's value, through the published binding. Fails closed, naming both."""
    name = operand["reference"]["source_name"]
    table = bindings.get(constraint_id)
    if table is None:
        raise VerifyError(
            f"the package publishes no operand bindings for constraint {constraint_id}"
        )
    binding = table.get(name)
    if binding is None:
        raise VerifyError(
            f"{constraint_id}: operand {name!r} has no published binding"
        )
    kind, key = binding.get("kind"), binding.get("key")
    if kind == "input":
        if key in case_inputs:
            return float(case_inputs[key])
        if key in package_inputs:
            return float(package_inputs[key])
        raise VerifyError(
            f"{constraint_id}: operand {name!r} binds to input {key!r}, which is neither "
            f"swept by this case nor present in the package's inputs"
        )
    if kind == "channel":
        if key not in channels:
            raise VerifyError(
                f"{constraint_id}: operand {name!r} binds to channel {key!r}, which the "
                f"oracle did not return"
            )
        return float(channels[key])
    raise VerifyError(f"{constraint_id}: operand {name!r} has an unknown binding kind {kind!r}")


def derive_verdict(constraint_id: str, entry: dict, bindings: dict,
                   case_inputs, package_inputs, channels) -> tuple[bool, int]:
    """Re-derive one constraint from its own IR. Returns (satisfied, operands resolved)."""
    ir = json.loads(entry["predicate_ir"])
    if ir.get("kind") != "operator" or ir.get("operator") not in OPERATORS:
        raise VerifyError(
            f"{constraint_id}: predicate IR is not a comparison this tool can re-derive "
            f"(kind {ir.get('kind')!r}, operator {ir.get('operator')!r})"
        )
    operands = ir["operands"]
    if len(operands) != 2:
        raise VerifyError(
            f"{constraint_id}: expected a two-operand comparison, found {len(operands)}"
        )
    values, resolved = [], 0
    for operand in operands:
        if operand["kind"] == "literal":
            values.append(float(operand["literal"]["value"]))
        elif operand["kind"] == "feature_ref":
            values.append(resolve_operand(
                constraint_id, operand, bindings, case_inputs, package_inputs, channels
            ))
            resolved += 1
        else:
            raise VerifyError(
                f"{constraint_id}: operand kind {operand['kind']!r} cannot be re-derived"
            )
    result = OPERATORS[ir["operator"]](values[0], values[1])
    if entry.get("is_negated"):
        result = not result
    return result, resolved


# ---------------------------------------------------------------- the sampling


def compatibility_digest(store) -> tuple[str, dict]:
    """A digest over the store's compatibility row, as sorted ``key=value`` lines."""
    cursor = store.conn.execute("SELECT * FROM compatibility")
    row = cursor.fetchone()
    if row is None:
        raise VerifyError("store carries no compatibility row")
    fields = {
        description[0]: row[i]
        for i, description in enumerate(cursor.description)
        if description[0] != "singleton"
    }
    text = "\n".join(f"{key}={fields[key]}" for key in sorted(fields)) + "\n"
    return hashlib.sha256(text.encode("utf-8")).hexdigest(), fields


def derive_seed(study_id: str, digest: str) -> int:
    """The default seed, written down rather than magic, and reproducible from the record."""
    text = f"{study_id}\n{digest}\n"
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], 16)


def stratified_sample(cases, sample_size: int, seed: int):
    """One case per observed verdict combination, then a seeded random fill.

    Stratification is a floor: when the strata outnumber the sample size, every
    stratum is still represented and the sample is larger than asked for.
    """
    rng = random.Random(seed)
    strata: dict[tuple, list] = {}
    for case in cases:
        key = tuple(sorted(case.verdicts.items()))
        strata.setdefault(key, []).append(case)
    sample = [rng.choice(members) for members in strata.values()]
    chosen = {id(case) for case in sample}
    rest = [case for case in cases if id(case) not in chosen]
    fill = min(max(0, sample_size - len(sample)), len(rest))
    sample += rng.sample(rest, fill)
    return sample, len(strata)


# ------------------------------------------------------------------- the check


def package_input_values(package_root: Path) -> dict:
    values = {}
    for path in sorted((package_root / "inputs").glob("*.json")):
        data = common.read_json(path, "package inputs")
        if isinstance(data, dict):
            values.update(data)
    return values


def objective_channels(loaded: manifest_mod.LoadedManifest) -> dict[str, str]:
    return {e["channel"]: e["name"] for e in loaded.data["objective_catalog"]}


def check_case(case, evaluate, bindings, catalog_entries, objectives,
               package_inputs, identity_digest):
    """One sampled case: channels, verdicts, and identity continuity."""
    if case.executable_fingerprint != identity_digest:
        raise VerifyError(
            f"case {case.candidate_id} ran under executable fingerprint "
            f"{case.executable_fingerprint}, not the gated identity {identity_digest}"
        )
    channels = evaluate(case.inputs)
    if not isinstance(channels, dict) or not channels:
        raise VerifyError(
            f"the oracle returned no channels for case {case.candidate_id}"
        )

    binding_channels = {
        binding["key"]
        for table in bindings.values()
        for binding in table.values()
        if binding.get("kind") == "channel"
    }
    wanted = (set(objectives) | binding_channels) & set(channels)
    compared = []
    worst = (0.0, None, None, None)
    for channel in sorted(wanted):
        if channel not in case.outputs:
            continue  # the era records only single-field float channels
        deviation = common.relative_deviation(case.outputs[channel], channels[channel])
        compared.append(channel)
        if deviation > worst[0]:
            worst = (deviation, case.candidate_id, channel, case.outputs[channel])
        if deviation >= TOLERANCE:
            raise VerifyError(
                f"channel off tolerance on case {case.candidate_id}, channel {channel}: "
                f"store {case.outputs[channel]!r}, oracle {channels[channel]!r}, "
                f"relative deviation {deviation:.3e} (tolerance {TOLERANCE:g})"
            )
    if not compared:
        raise VerifyError(
            f"case {case.candidate_id}: no channel could be compared — the oracle and the "
            f"store share no named channel, so parity would mean nothing"
        )

    mismatches, rederived = [], []
    for constraint_id, recorded in sorted(case.verdicts.items()):
        entry = catalog_entries.get(constraint_id)
        if entry is None:
            raise VerifyError(
                f"case {case.candidate_id}: constraint {constraint_id} has no catalog entry, "
                f"so its verdict cannot be re-derived"
            )
        satisfied, resolved = derive_verdict(
            constraint_id, entry, bindings, case.inputs, package_inputs, channels
        )
        expected = "satisfied" if satisfied else "violated"
        rederived.append({
            "constraint_id": constraint_id,
            "source_local_identity": entry["source_local_identity"],
            "operands_resolved": resolved,
        })
        if recorded != expected:
            mismatches.append({
                "case_id": case.candidate_id,
                "constraint_id": constraint_id,
                "source_local_identity": entry["source_local_identity"],
                "recorded": recorded,
                "rederived": expected,
            })
    if mismatches:
        first = mismatches[0]
        raise VerifyError(
            f"verdict mismatch on case {first['case_id']}, constraint "
            f"{first['constraint_id']} ({first['source_local_identity']}): the store records "
            f"{first['recorded']}, re-deriving its predicate gives {first['rederived']}"
        )
    return worst, compared, rederived, channels


def verify_store(store_path: Path, package_root: Path, loaded, identity_doc,
                 evaluate, bindings, catalog_entries, sample_size, explicit_seed):
    from simkit.study.query import StudyQuery
    from simkit.study.store import StudyStore

    store = StudyStore(store_path)
    try:
        digest, fields = compatibility_digest(store)
        study_id = fields["study_id"]
        seed = explicit_seed if explicit_seed is not None else derive_seed(study_id, digest)
        cases = StudyQuery(store, package_root).cases()
    finally:
        store.close()

    completed = [c for c in cases if c.state == "completed"]
    if not completed:
        raise VerifyError(
            f"no completed cases in {manifest_mod.repo_relative_posix(store_path)}: there is "
            f"nothing to verify, which is a broken input rather than a clean pass"
        )
    sample, strata = stratified_sample(completed, sample_size, seed)

    objectives = objective_channels(loaded)
    package_inputs = package_input_values(package_root)
    identity_digest = identity_doc["identity"]["digest"]
    worst = (0.0, None, None, None)
    compared_channels: set[str] = set()
    rederived_by_id: dict[str, dict] = {}
    for case in sample:
        case_worst, compared, rederived, channels = check_case(
            case, evaluate, bindings, catalog_entries, objectives,
            package_inputs, identity_digest,
        )
        compared_channels |= set(compared)
        for entry in rederived:
            rederived_by_id[entry["constraint_id"]] = entry
        if case_worst[0] > worst[0]:
            worst = case_worst

    missing = sorted(set(catalog_entries) - set(rederived_by_id))
    if missing:
        raise VerifyError(
            "the sampled cases carry no verdict for catalog constraint(s), so "
            "verdicts_rederived cannot be claimed: " + ", ".join(missing)
        )

    return {
        "path": manifest_mod.repo_relative_posix(store_path),
        "study_id": study_id,
        "compatibility": {"digest": digest, **{k: v for k, v in sorted(fields.items())}},
        "cases_total": len(cases),
        "cases_completed": len(completed),
        "sampling": {
            "scheme": SAMPLING_SCHEME,
            "seed": f"{seed:x}",
            "seed_source": "explicit" if explicit_seed is not None else "derived",
            "sample_size_requested": sample_size,
            "strata_observed": strata,
            "sampled_rows": len(sample),
            "sampled_case_ids": [c.candidate_id for c in sample],
        },
        "worst_channel_rel_dev": worst[0],
        "worst_at": (
            {"case_id": worst[1], "channel": worst[2], "value": worst[3]}
            if worst[1] is not None else None
        ),
    }, sorted(compared_channels), list(rederived_by_id.values())


# ----------------------------------------------------------------- the summary


def build_summary(package_root: Path, manifest_path: Path, identity_path: Path,
                  store_paths: list[Path], sample_size: int, explicit_seed, argv) -> dict:
    import simkit

    loaded = manifest_mod.load(manifest_path)
    manifest_mod.assert_package_identity(loaded, package_root)
    identity_doc = identity.load(identity_path)
    identity.assert_matches(identity_doc, package_root)

    _module, evaluate, bindings = load_oracle(loaded)
    contract = common.read_json(
        package_root / "contracts" / "model_contract.json", "model contract"
    )
    catalog_entries = {
        e["constraint_id"]: e for e in contract["constraint_catalog"]["concrete_entries"]
    }

    stores, channels, rederived = [], set(), {}
    for path in store_paths:
        summary, compared, per_constraint = verify_store(
            path, package_root, loaded, identity_doc, evaluate, bindings,
            catalog_entries, sample_size, explicit_seed,
        )
        stores.append(summary)
        channels |= set(compared)
        for entry in per_constraint:
            rederived[entry["constraint_id"]] = entry

    common.assert_tree_clean(package_root)
    oracle_block = loaded.data["oracle"]
    worst = max((s["worst_channel_rel_dev"] for s in stores), default=0.0)
    objectives = objective_channels(loaded)
    return {
        "schema_version": SUMMARY_SCHEMA_VERSION,
        "tool": {
            "path": "scripts/study/verify.py",
            "source_digest": common.tool_source_digest(TOOL_SOURCE_FILES),
        },
        "command": ["scripts/study/verify.py", *argv],
        "teax": {
            "module_path": manifest_mod.repo_relative_posix(Path(simkit.__file__).parent),
            "revision": getattr(simkit, "__version__", "unrecorded"),
        },
        "package": {
            "path": manifest_mod.repo_relative_posix(package_root),
            "package_name": manifest_mod.read_package_name(package_root),
            "git_clean": True,
        },
        "identity": {
            "kind": identity_doc["identity"]["kind"],
            "digest": identity_doc["identity"]["digest"],
            "matches_preflight": True,
        },
        "manifest": {
            "path": manifest_mod.repo_relative_posix(manifest_path),
            "schema_version": loaded.data["schema_version"],
            "digest": loaded.digest,
        },
        "oracle": {
            "kind": oracle_block["kind"],
            "sys_path": oracle_block["sys_path"],
            "module": oracle_block["module"],
            "callable": oracle_block["callable"],
            "operand_bindings_digest": bindings_digest(bindings),
        },
        "stores": stores,
        "tolerance": TOLERANCE,
        "channels_checked": [
            {"channel": channel, "objective": objectives.get(channel)}
            for channel in sorted(channels)
        ],
        "verdicts_rederived": True,
        "constraints_rederived": sorted(rederived.values(), key=lambda e: e["constraint_id"]),
        "verdict_mismatches": [],
        "not_independently_verified": [
            {"rung": rung["rung"], "keys": list(rung["keys"]), "note": rung.get("note", "")}
            for rung in identity_doc["glue_ledger"]
            if not rung["independently_verified"]
        ],
        "worst_channel_rel_dev": worst,
        "outcome": "pass",
    }


# ----------------------------------------------------------------------- CLI


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="verify.py",
        description="Sample a study's evidence and check it against the package's oracle.",
    )
    parser.add_argument("--package", required=True, metavar="DIR")
    parser.add_argument("--manifest", required=True, metavar="FILE")
    parser.add_argument("--identity", required=True, metavar="FILE")
    parser.add_argument("--store", required=True, action="append", metavar="FILE",
                        help="a study store to sample (repeatable)")
    parser.add_argument("--sample-size", type=int, default=DEFAULT_SAMPLE_SIZE, metavar="N")
    parser.add_argument("--seed", metavar="HEX", help="override the derived seed")
    parser.add_argument("--out", metavar="FILE", help="write the summary here")
    return parser


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    args = build_parser().parse_args(argv)
    seed = int(args.seed, 16) if args.seed else None
    try:
        summary = build_summary(
            Path(args.package), Path(args.manifest), Path(args.identity),
            [Path(p) for p in args.store], args.sample_size, seed, argv,
        )
    except (common.ToolError, manifest_mod.ManifestError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(
        f"[verify] {len(summary['stores'])} store(s), "
        f"{sum(s['sampling']['sampled_rows'] for s in summary['stores'])} sampled rows, "
        f"{len(summary['channels_checked'])} channels at rel < {TOLERANCE:g}, "
        f"worst {summary['worst_channel_rel_dev']:.2e}, "
        f"{len(summary['constraints_rederived'])} verdicts re-derived",
        file=sys.stderr,
    )
    for rung in summary["not_independently_verified"]:
        print(f"[verify] NOT independently verified — {rung['rung']}: {rung['note']}",
              file=sys.stderr)
    if args.out:
        common.write_document(summary, Path(args.out))
    else:
        sys.stdout.write(json.dumps(summary, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
