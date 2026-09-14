"""verify.py: stratification, parity, re-derived verdicts, and everything failing closed.

The summary this produces is what a record's `arms[].verification` block is filled
from, so the tests hold both halves: the checks are real, and the document carries
every field the committed proof-of-life summary carried, by name or by a named
generalization.
"""

import json
import subprocess
import sys
from pathlib import Path

import jsonschema
import pytest

from scripts.study import verify

REPO_ROOT = Path(__file__).resolve().parents[2]
VERIFY = REPO_ROOT / "scripts" / "study" / "verify.py"
MANIFEST = REPO_ROOT / "exploration" / "stellarator_e2e" / "studies" / "manifest.json"
PACKAGE = REPO_ROOT / "exploration" / "stellarator_e2e" / "pkg" / "stellarator_tea"
COMMITTED_SUMMARY = (
    REPO_ROOT / "exploration" / "stellarator_e2e" / "study" / "verification_summary.json"
)

#: Every field of the committed summary, and where it survives in the promoted one.
FIELD_SURVIVAL = {
    "channels_checked": "channels_checked",
    "tolerance": "tolerance",
    "verdicts_rederived": "verdicts_rederived",
    "worst_channel_rel_dev": "worst_channel_rel_dev",
    "package_git_clean": "package.git_clean",
    "glue_note": "not_independently_verified",
    "sampled_rows_per_study": "stores[].sampling.sampled_rows",
    "sampling": "stores[].sampling.scheme",
    "seed": "stores[].sampling.seed",
}


@pytest.fixture(scope="session")
def promoted_run(stock_route_run):
    """The stock-route store plus the sealed identity document that scopes it."""
    return stock_route_run


def run_verify(promoted_run, out, *extra, expect=None):
    argv = [
        "--package", str(PACKAGE),
        "--manifest", str(MANIFEST),
        "--identity", str(promoted_run["identity"]),
        "--store", str(promoted_run["store"]),
        "--out", str(out),
        *extra,
    ]
    done = subprocess.run(
        [sys.executable, str(VERIFY), *argv],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
        env={**__import__("os").environ, "PYTHONPATH": str(promoted_run["simkit"])},
    )
    if expect is not None:
        assert done.returncode == expect, f"exit {done.returncode}\n{done.stderr}"
    return done


@pytest.fixture
def summary(promoted_run, tmp_path):
    out = tmp_path / "verification_summary.json"
    run_verify(promoted_run, out, expect=0)
    return json.loads(out.read_text())


def test_the_summary_validates_against_its_schema(summary, load_schema):
    jsonschema.validate(summary, load_schema("verification_summary.v1"))


def test_the_summary_is_a_superset_of_the_committed_field_set(summary):
    committed = json.loads(COMMITTED_SUMMARY.read_text())
    assert set(committed) == set(FIELD_SURVIVAL), "the committed summary's field set moved"
    store = summary["stores"][0]
    assert summary["channels_checked"] and summary["tolerance"] == 1e-9
    assert summary["verdicts_rederived"] is True
    assert isinstance(summary["worst_channel_rel_dev"], float)
    assert summary["package"]["git_clean"] is True
    # The field survives as data; on the stock route it is empty (SC4): nothing is fed
    # to both sides, so every compared channel is independently verified.
    assert summary["not_independently_verified"] == []
    assert store["sampling"]["sampled_rows"] >= 1
    assert store["sampling"]["scheme"] == "stratified-by-verdict-combination/v1"
    assert store["sampling"]["seed"]


def test_parity_holds_at_the_committed_order_of_magnitude(summary):
    assert summary["worst_channel_rel_dev"] < 1e-12, summary["worst_channel_rel_dev"]


def test_every_catalog_constraint_is_rederived_with_its_operand_count(summary):
    rederived = {c["source_local_identity"]: c["operands_resolved"]
                 for c in summary["constraints_rederived"]}
    assert set(rederived) == {
        "beta_ok", "net_positive", "peak_field_ok", "recirc_ok", "tbr_ok", "wall_load_ok",
        "wp_stress_ok",  # WI-035
        "sustainment_ok",  # WI-037
        "cond_strain_ok",  # WI-036: the conductor's own check, separate from the structure's
        "burn_hold_ok",  # WI-043: the lower half of the sustainment condition, p_aux_required >= 0
        # WI-045 (goal plant-closure, 2026-09-08): the loop's pressure-domain and capacity
        # fences and the cycle's fit-domain fence, all on computed operands
        "loop_pressure_ok", "loop_capacity_ok", "cycle_domain_ok",
        # WI-047 (goal plant-closure, 2026-09-08): the divertor target peak (computed) against
        # the adopted threshold -- violated at the baseline by design
        "divertor_heat_ok",
        "heating_source_positive_ok", "heating_source_upper_ok",
        "heating_couple_positive_ok", "heating_couple_upper_ok",
    }
    assert rederived["net_positive"] == 1  # the other operand is the literal 0.0
    assert rederived["burn_hold_ok"] == 1  # likewise: one computed operand against the literal 0.0
    assert all(count >= 1 for count in rederived.values())


def test_stratification_covers_every_observed_verdict_combination(summary):
    store = summary["stores"][0]
    assert store["sampling"]["strata_observed"] >= 1
    assert store["sampling"]["sampled_rows"] >= store["sampling"]["strata_observed"]


def test_stratification_is_a_floor_not_a_cap(promoted_run, tmp_path):
    """Asked for one row, every stratum still appears."""
    out = tmp_path / "summary.json"
    run_verify(promoted_run, out, "--sample-size", "1", expect=0)
    store = json.loads(out.read_text())["stores"][0]
    assert store["sampling"]["sample_size_requested"] == 1
    assert store["sampling"]["sampled_rows"] == store["sampling"]["strata_observed"]


def test_the_derived_seed_reproduces_from_the_recorded_fields(summary):
    """N2/D8: a reader holding the record can reproduce the draw."""
    store = summary["stores"][0]
    assert store["sampling"]["seed_source"] == "derived"
    expected = verify.derive_seed(store["study_id"], store["compatibility"]["digest"])
    assert store["sampling"]["seed"] == f"{expected:x}"


def test_an_explicit_seed_is_recorded_as_explicit(promoted_run, tmp_path):
    out = tmp_path / "summary.json"
    run_verify(promoted_run, out, "--seed", "beef", expect=0)
    store = json.loads(out.read_text())["stores"][0]
    assert store["sampling"] == {**store["sampling"], "seed": "beef", "seed_source": "explicit"}


def test_cas27_is_compared_and_nothing_is_undisclosed(summary):
    """The era route fed CAS27 (special materials) identically to the package and to
    the oracle and disclosed it as not independently verified. On the regenerated
    package CAS27 is computed in-package, declared as the `cas27` objective, and
    compared against the oracle's own recompute -- the disclosure list is empty and
    the comparison names the channel (stellarator-model-migration SC4)."""
    assert summary["not_independently_verified"] == []
    compared = {c["channel"]: c["objective"] for c in summary["channels_checked"]}
    P = "stellarator_09__stellaris__"
    assert compared[f"{P}special_materials_capital__special_materials_capital"] == "cas27"
    assert compared[f"{P}total_capital__total_capital"] == "total_capital"
    assert compared[f"{P}lcoe_calc__lcoe"] == "lcoe"


def test_the_command_carries_no_absolute_paths(summary):
    assert summary["command"][0] == "scripts/study/verify.py"
    for path_field in (summary["package"]["path"], summary["manifest"]["path"],
                       summary["stores"][0]["path"]):
        assert not Path(path_field).is_absolute(), path_field


def test_the_operand_bindings_digest_is_the_documented_canonicalization(summary):
    import oracle_entry

    assert summary["oracle"]["operand_bindings_digest"] == verify.bindings_digest(
        oracle_entry.operand_bindings()
    )


# ------------------------------------------------------------------- negatives


def test_a_planted_channel_deviation_fails_naming_case_and_channel(promoted_run, monkeypatch):
    import oracle_entry

    channel = "stellarator_09__stellaris__lcoe_calc__lcoe"
    real = oracle_entry.evaluate

    def skewed(point):
        out = dict(real(point))
        out[channel] *= 1.000001
        return out

    monkeypatch.setattr(oracle_entry, "evaluate", skewed)
    with pytest.raises(verify.VerifyError) as exc:
        verify.build_summary(PACKAGE, MANIFEST, promoted_run["identity"],
                             [promoted_run["store"]], 12, None, [])
    assert channel in str(exc.value) and "relative deviation" in str(exc.value)


def test_a_planted_verdict_mismatch_fails_naming_the_constraint(promoted_run, monkeypatch):
    """Flip the threshold the package's own predicate reads, so re-derivation disagrees.

    The plant must disagree with what the store records at the availability-sweep
    points (the baseline geometry), and that verdict has moved with the package:
    before WI-041 the store recorded wall_load_ok SATISFIED and the plant was 0.0;
    WI-041's source-anchored peak read 4.088 against 4.05 (VIOLATED), so the plant
    became an unreachable limit; since WI-042 the sourced helium-ash profile takes
    the peak to 3.979 against 4.05 (SATISFIED again), so the plant is 0.0 again and
    re-derivation reads violated against the store's satisfied. A plant that agrees
    with the store plants nothing (the WI-041 lesson, repeated the other way)."""
    real = verify.package_input_values

    def flipped(package_root):
        values = dict(real(package_root))
        values["stellarator_09__stellaris__wall_load_limit"] = 0.0
        return values

    monkeypatch.setattr(verify, "package_input_values", flipped)
    with pytest.raises(verify.VerifyError) as exc:
        verify.build_summary(PACKAGE, MANIFEST, promoted_run["identity"],
                             [promoted_run["store"]], 12, None, [])
    assert "wall_load_ok" in str(exc.value) and "verdict mismatch" in str(exc.value)


def test_a_missing_operand_bindings_attribute_fails_closed(promoted_run, monkeypatch):
    """Invariant 9: without published bindings the tool refuses rather than guesses."""
    import oracle_entry

    monkeypatch.delattr(oracle_entry, "operand_bindings")
    with pytest.raises(verify.VerifyError) as exc:
        verify.build_summary(PACKAGE, MANIFEST, promoted_run["identity"],
                             [promoted_run["store"]], 12, None, [])
    assert "operand_bindings" in str(exc.value) and "does not guess" in str(exc.value)


def test_an_unresolvable_binding_fails_naming_the_constraint_and_operand(
    promoted_run, monkeypatch
):
    import oracle_entry

    cid = "stellarator_09__stellaris__beta_ok__82b78aad420730d5"
    real = oracle_entry.operand_bindings

    def broken():
        table = real()
        table[cid]["beta_limit_in"] = {"kind": "input", "key": "no_such__key"}
        return table

    monkeypatch.setattr(oracle_entry, "operand_bindings", broken)
    with pytest.raises(verify.VerifyError) as exc:
        verify.build_summary(PACKAGE, MANIFEST, promoted_run["identity"],
                             [promoted_run["store"]], 12, None, [])
    assert cid in str(exc.value) and "beta_limit_in" in str(exc.value)
    assert "no_such__key" in str(exc.value)


def test_a_store_bound_to_another_identity_is_refused(promoted_run, repo_root, tmp_path):
    """Invariant 5 on real evidence: the pre-capability store carries the SEALED
    fingerprint, which the bypassing route never earned, so it is refused."""
    committed = repo_root / "exploration" / "stellarator_e2e" / "study" / "_work"
    store = committed / "availability_sweep.db"
    if not store.is_file():
        pytest.skip(f"proof-of-life store unavailable: {store}")
    with pytest.raises(verify.VerifyError) as exc:
        verify.build_summary(PACKAGE, MANIFEST, promoted_run["identity"], [store], 12, None, [])
    assert "not the gated identity" in str(exc.value)


def test_an_empty_result_is_a_broken_input_not_a_clean_pass(promoted_run, tmp_path):
    """Invariant 7 cuts the other way here: no completed cases is mechanical, not empty."""
    import shutil

    from simkit.study.store import StudyStore

    work = tmp_path / "_work"
    shutil.copytree(promoted_run["store"].parent, work)  # the evidence artifacts travel too
    db = work / promoted_run["store"].name
    store = StudyStore(db)
    store.conn.execute("UPDATE cases SET state = 'failed'")
    store.conn.commit()
    store.close()
    with pytest.raises(verify.VerifyError) as exc:
        verify.build_summary(PACKAGE, MANIFEST, promoted_run["identity"], [db], 12, None, [])
    assert "no completed cases" in str(exc.value)


def test_the_stores_are_never_written(promoted_run, tmp_path):
    import hashlib

    before = hashlib.sha256(promoted_run["store"].read_bytes()).hexdigest()
    run_verify(promoted_run, tmp_path / "summary.json", expect=0)
    assert hashlib.sha256(promoted_run["store"].read_bytes()).hexdigest() == before


@pytest.fixture(scope="module")
def operating_controls(tmp_path_factory, stock_simkit_session_path):
    """Stored native baseline, installed reserve and physical demand controls."""
    sys.path.insert(0, str(MANIFEST.parent))
    import study_route

    out = tmp_path_factory.mktemp("operating-controls")
    baseline = json.loads(MANIFEST.read_text())["baseline"]["point"]
    P = study_route.P
    proposals = [baseline, {**baseline, f"{P}heating__p_wallplug_heat": 120.0},
                 {**baseline, f"{P}plasma__f_alpha_fast": 0.96}]
    cases, db = study_route.run_points("operating-controls", proposals, out / "_work")
    assert len(cases) == 3 and all(case.state == "completed" for case in cases)
    ident = study_route.write_identity_document(study_route.PACKAGE_DIR, out / "identity.json")
    summary = verify.build_summary(PACKAGE, MANIFEST, ident, [db], 3, None, [])
    assert summary["worst_channel_rel_dev"] < 1e-9
    assert len(summary["constraints_rederived"]) == 18
    return cases, summary


def test_stored_operating_controls_preserve_procurement_and_signed_capacity(operating_controls):
    import study_route

    cases, summary = operating_controls
    P = study_route.P
    baseline = next(
        c for c in cases
        if f"{P}heating__p_wallplug_heat" not in c.inputs and f"{P}plasma__f_alpha_fast" not in c.inputs
    )
    reserve = next(c for c in cases if c.inputs.get(f"{P}heating__p_wallplug_heat") == 120)
    demand = next(c for c in cases if c.inputs.get(f"{P}plasma__f_alpha_fast") == .96)
    for name in ("coupled", "delivered", "wallplug"):
        channel = study_route.CHANNELS[f"operating_heat_{name}"]
        assert baseline.outputs[channel] == reserve.outputs[channel]
        assert demand.outputs[channel] != baseline.outputs[channel]
        assert channel in {row["channel"] for row in summary["channels_checked"]}
    assert baseline.outputs[f"{P}heating__heating_cost__cost"] == 264145000
    assert reserve.outputs[f"{P}heating__heating_cost__cost"] == 316974000
    assert demand.outputs[f"{P}heating__heating_cost__cost"] == 264145000
    assert baseline.outputs[f"{P}divertor__divheat__p_heat_operating_minus_installed"] == pytest.approx(
        -.920399212073221
    )
    assert reserve.outputs[f"{P}divertor__divheat__p_heat_operating_minus_installed"] == pytest.approx(
        -10.920399212073221
    )
    verdicts = study_route.short_verdicts(baseline)
    assert len(verdicts) == 18
    assert {name for name, status in verdicts.items() if status != "satisfied"} == {
        "divertor_heat_ok"
    }
    rows = study_route.csv_rows(cases, [])
    assert len(rows) == 3
    assert all(all(name in row for name in study_route.CHANNELS) for row in rows)


@pytest.mark.parametrize("channel", ["p_coupled", "p_delivered", "p_wallplug"])
def test_operating_channel_deviation_is_refused(promoted_run, monkeypatch, channel):
    import oracle_entry

    name = f"stellarator_09__stellaris__operating_heat__{channel}"
    evaluate = oracle_entry.evaluate

    def skewed(point):
        values = evaluate(point)
        values[name] += 1
        return values

    monkeypatch.setattr(oracle_entry, "evaluate", skewed)
    with pytest.raises(verify.VerifyError, match="relative deviation"):
        verify.build_summary(
            PACKAGE, MANIFEST, promoted_run["identity"], [promoted_run["store"]], 12, None, []
        )


@pytest.mark.parametrize("stage", ["source", "couple"])
def test_zero_efficiency_is_a_recorded_native_execution_failure(stock_simkit_path, tmp_path, stage):
    sys.path.insert(0, str(MANIFEST.parent))
    import study_route

    point = {f"{study_route.P}heating__eta_{stage}_heat"  # WI-057 (2026-09-13): the heating efficiencies live on the heating part: 0.0}
    cases, _ = study_route.run_points(f"zero-{stage}-efficiency", [point], tmp_path)
    assert len(cases) == 1
    assert cases[0].state == "execution_failed"
    with pytest.raises(study_route.RouteError):
        study_route.csv_rows(cases, [])
