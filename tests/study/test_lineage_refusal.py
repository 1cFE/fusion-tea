"""The concept design's unowned proof 5, on real code: drift retires the store.

The effective executable fingerprint is only worth having if something enforces it.
teax already does: ``StudyStore.create_or_open`` binds a compatibility tuple on
create and raises ``IncompatibleStore`` on mismatch. Feed it an honest identity and
the enforcement comes free — touch any of the adapter's three declared sources and
the pre-existing store refuses to resume.

The store here is built directly from the era API rather than through
``promotion_equivalence.py``'s route, deliberately: the claim under test is about
identity binding, not about how a route builds its proposals, and a test that went
through the route would fail for either reason.
"""

import json
import shutil
import sys

import pytest


@pytest.fixture
def adapter(era_simkit_path, repo_root):
    studies = repo_root / "exploration" / "stellarator_e2e" / "studies"
    for path in (str(studies), str(repo_root)):
        if path not in sys.path:
            sys.path.insert(0, path)
    import era_adapter

    return era_adapter


P = "stellarator_09__stellaris__"
TWO_POINTS = [(12.7, 1.3), (13.2, 1.35)]


def _proposal(adapter, R, a, availability=0.85):
    point = {
        f"{P}geom__R": R, f"{P}rb__R": R, f"{P}magnet__R0": R,
        f"{P}geom__a": a, f"{P}rb__a": a,
        f"{P}cas72_calc__availability": availability,
        f"{P}fuel_calc__availability": availability,
        f"{P}lcoe_calc__availability": availability,
        f"{P}lcoe_1cfe_calc__availability": availability,
    }
    return {**adapter.glue_fields(point), **point}


def _definition(adapter, package, prepared, fingerprint, proposals):
    from simkit.study.definition import StudyDefinition
    from simkit.study.identity import digest_of
    from simkit.study.policy import ObjectivePolicy
    from simkit.study.strategy import PreparedListStrategy

    return StudyDefinition(
        study_id="item4-lineage-refusal-v1",
        entry_models=prepared.entry_models,
        strategy=PreparedListStrategy(proposals),
        validate_proposal=lambda raw: {k: float(v) for k, v in raw.items()},
        policy=ObjectivePolicy(objectives=(), response_roles={}),
        executable_fingerprint=fingerprint,
        model_contract_fingerprint=digest_of(
            json.loads((package / "contracts" / "model_contract.json").read_text())
        ),
        input_schema_version="input-v1",
        evidence_schema_version=prepared.EVIDENCE_SCHEMA_VERSION,
        study_definition_fingerprint=digest_of(
            {"proposals": [sorted(p.items()) for p in proposals]}
        ),
    )


@pytest.fixture
def two_point_store(adapter, real_package_path, tmp_path):
    """A real store over two executed points, left on disk. Never unlinked."""
    from simkit.evaluation.evaluator import PreparedEvaluator
    from simkit.study.runner import StudyRunner
    from simkit.study.store import StudyStore

    package = tmp_path / "pkg"
    shutil.copytree(real_package_path, package)
    loader = adapter.loader(package, tmp_path / "link")
    prepared = PreparedEvaluator(loader, package / "pipelines" / "mfe_stellarator.yaml")
    proposals = [_proposal(adapter, R, a) for R, a in TWO_POINTS]
    definition = _definition(adapter, package, prepared, prepared.fingerprint, proposals)

    db = tmp_path / "lineage.db"
    store = StudyStore.create_or_open(db, definition.compatibility())
    store.acquire_lease()
    StudyRunner(store, definition, prepared).run()
    store.release_lease()
    store.close()
    return package, prepared, proposals, db


def _reopen(adapter, package, prepared, proposals, db, fingerprint):
    from simkit.study.store import StudyStore

    definition = _definition(adapter, package, prepared, fingerprint, proposals)
    return StudyStore.create_or_open(db, definition.compatibility())


def test_the_store_reopens_under_the_same_identity(adapter, two_point_store):
    package, prepared, proposals, db = two_point_store
    store = _reopen(adapter, package, prepared, proposals, db,
                    adapter.effective_fingerprint(package))
    store.close()


@pytest.mark.parametrize(
    "source",
    ["glue_file", "era_adapter.py", "oracle_entry.py", "verify_stellaris.py"],
)
def test_touching_a_declared_source_retires_the_store(
    source, adapter, two_point_store, tmp_path, monkeypatch, repo_root
):
    """Three declared sources plus the allowed-modified glue file — four refusals.

    The repo's own files are never edited: the digest lookup is redirected at a
    scratch copy with one byte changed, which is the same input the recipe sees.
    """
    from simkit.study.store import IncompatibleStore, StudyStore

    package, prepared, proposals, db = two_point_store
    before = adapter.effective_fingerprint(package)

    if source == "glue_file":
        target = package / "inputs" / "system_design.json"
        target.write_text(target.read_text().replace("}", ', "_probe": 1}', 1))
        after = adapter.effective_fingerprint(package)
    else:
        from scripts.study import manifest as manifest_mod

        rel = f"exploration/stellarator_e2e/studies/{source}"
        if source == "verify_stellaris.py":
            rel = "exploration/stellarator_e2e/verify_stellaris.py"
        real_sha = manifest_mod.sha256_file

        def _sha(path):
            return "0" * 64 if str(path).endswith(rel.rsplit("/", 1)[-1]) else real_sha(path)

        monkeypatch.setattr(manifest_mod, "sha256_file", _sha)
        after = adapter.effective_fingerprint(package)

    assert after != before, f"changing {source} left the effective fingerprint unmoved"
    with pytest.raises(IncompatibleStore) as exc:
        _reopen(adapter, package, prepared, proposals, db, after)
    assert before in str(exc.value) or after in str(exc.value)
    StudyStore(db).close()


def test_the_committed_package_is_untouched_by_these_tests(repo_root):
    from scripts.study import common

    common.assert_tree_clean(repo_root / "exploration" / "stellarator_e2e" / "pkg")
