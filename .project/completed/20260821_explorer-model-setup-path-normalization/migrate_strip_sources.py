"""One-shot migration: strip the dead ``sources`` block from explorer concept JSON.

The explorer no longer stores filesystem paths to ``model_setup.py`` /
``analysis.md`` — the compute endpoint derives them from the concept_id at
request time (see explorer-model-setup-path-normalization). ``SourcePaths`` and
the ``sources`` field were removed from ``ConceptData``, so the committed
``data/*.json`` files carry a now-orphaned ``sources`` block holding
machine-absolute paths.

This rewrites each concept file through ``ConceptData`` (which drops the unknown
``sources`` key) and re-emits it with ``model_dump_json(indent=2)`` — byte-identical
to what a fresh extractor run now produces (FR-6 parity). ``sources`` was verified
to be the ONLY on-disk key absent from the current model, so nothing else is lost.

Run from the repo root:  uv run python .project/active/explorer-model-setup-path-normalization/migrate_strip_sources.py
"""

from __future__ import annotations

import glob
import sys
import warnings
from pathlib import Path

# Script lives at .project/active/<item>/; repo root is parents[3]. Put it on
# sys.path so `exploration` imports when run by file path (not -m).
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from exploration.concept_explorer.models import ConceptData  # noqa: E402

_DATA_GLOB = "exploration/concept_explorer/data/[0-9]*.json"


def main() -> None:
    files = sorted(glob.glob(_DATA_GLOB))
    rewritten = 0
    for path in files:
        text = open(path, encoding="utf-8").read()
        # The parameter_metadata UserWarning on freeform concepts is pre-existing
        # data noise, not a migration concern — silence it for a clean run log.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            concept = ConceptData.model_validate_json(text)
        open(path, "w", encoding="utf-8").write(concept.model_dump_json(indent=2))
        rewritten += 1
    print(f"rewrote {rewritten} files (stripped 'sources' block)")


if __name__ == "__main__":
    main()
