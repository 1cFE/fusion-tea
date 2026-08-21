"""S4: a stock-route study store speaks the generic vocabulary.

D7 has ``verify.py`` sample the study store rather than the exported CSV, because the
store is the primary evidence and the only source keyed by qualified names. That rests
on an assumption about what a ``StudyQuery`` case actually carries. This test opens a
store the stock route wrote this session, read-only, and checks it; the bytes must be
unchanged afterwards.
"""

import hashlib


def _open_query(store_path, package_dir):
    from simkit.study.query import StudyQuery
    from simkit.study.store import StudyStore

    return StudyQuery(StudyStore(store_path), package_dir)


def test_the_store_speaks_the_generic_vocabulary(stock_route_run, real_package_path):
    store = stock_route_run["store"]
    before = hashlib.sha256(store.read_bytes()).hexdigest()
    cases = _open_query(store, real_package_path.resolve()).cases()
    done = [c for c in cases if c.state == "completed"]
    assert len(done) == 19, f"{len(done)} completed cases in the availability sweep"
    case = done[0]
    # Qualified entry keys and qualified channel names -- the vocabulary a generic
    # tool can consume without being told a study's short column names.
    assert any(key.count("__") >= 2 for key in case.inputs), sorted(case.inputs)[:3]
    assert any(key.count("__") >= 2 for key in case.outputs), sorted(case.outputs)[:3]
    assert case.verdicts and all(isinstance(v, str) for v in case.verdicts.values())
    assert case.executable_fingerprint
    # The catalog join D12's verdict re-derivation reads: predicate IR per verdict.
    assert set(case.catalog) == set(case.verdicts)
    assert all(view.predicate_ir for view in case.catalog.values())
    assert hashlib.sha256(store.read_bytes()).hexdigest() == before, (
        "the store was modified by a read-only open"
    )
