"""scoring_v2 extract CLI.

Usage:
    uv run python exploration/scoring_v2/extract.py <concept_id> <feature_name>
    uv run python exploration/scoring_v2/extract.py --bulk-taxonomy

Single-feature mode rewrites exactly one feature block in
features/{concept_id}.yaml, preserving every other field.

--bulk-taxonomy iterates every taxonomy-derived feature for every concept_id
in table.csv. Additive: never deletes existing feature files.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from exploration.scoring_v2.lib import feature_io, schema as schema_mod
from exploration.scoring_v2.lib.extractors import dispatch
from exploration.scoring_v2.lib.extractors import taxonomy as taxonomy_ext


def _today() -> str:
    return _dt.date.today().isoformat()


def extract_one(concept_id: str, feature_name: str, *, features_dir: Path) -> None:
    schema = schema_mod.load_schema()
    if feature_name not in schema:
        raise SystemExit(
            f"unknown feature {feature_name!r}; not declared in schema.yaml"
        )
    entry = schema[feature_name]
    extractor = dispatch(entry["extractor"])
    value, provenance, confidence = extractor(concept_id, feature_name, entry)
    block = {
        "value": value,
        "provenance": provenance,
        "confidence": confidence,
        "extracted_at": _today(),
    }
    meta = {
        "concept_id": concept_id,
        "name": taxonomy_ext.concept_name(concept_id),
    }
    feature_io.update_feature(concept_id, feature_name, block,
                              features_dir=features_dir, meta=meta)


def bulk_taxonomy(*, features_dir: Path) -> int:
    schema = schema_mod.load_schema()
    taxonomy_features = {n: e for n, e in schema.items() if e["extractor"] == "taxonomy"}
    if not taxonomy_features:
        return 0
    ids = taxonomy_ext.all_concept_ids()
    for cid in ids:
        meta = {"concept_id": cid, "name": taxonomy_ext.concept_name(cid)}
        doc = feature_io.read_features(cid, features_dir=features_dir)
        doc["_meta"] = meta
        for fname, entry in taxonomy_features.items():
            value, prov, conf = taxonomy_ext.extract(cid, fname, entry)
            doc[fname] = {
                "value": value,
                "provenance": prov,
                "confidence": conf,
                "extracted_at": _today(),
            }
        feature_io.write_features(cid, doc, features_dir=features_dir)
    return len(ids)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("concept_id", nargs="?")
    parser.add_argument("feature_name", nargs="?")
    parser.add_argument("--bulk-taxonomy", action="store_true",
                        help="populate every taxonomy-derived feature for every concept")
    parser.add_argument("--features-dir", type=Path, default=schema_mod.FEATURES_DIR)
    args = parser.parse_args(argv)

    args.features_dir.mkdir(parents=True, exist_ok=True)

    if args.bulk_taxonomy:
        n = bulk_taxonomy(features_dir=args.features_dir)
        print(f"wrote taxonomy features for {n} concepts to {args.features_dir}")
        return 0
    if not args.concept_id or not args.feature_name:
        parser.error("provide <concept_id> <feature_name> or --bulk-taxonomy")
    extract_one(args.concept_id, args.feature_name, features_dir=args.features_dir)
    print(f"updated {args.concept_id}.{args.feature_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
