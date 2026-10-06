"""
Policy acceptance for the WI-100 Round 2 declared case set (contract r5 section 5, design
section 6.2).

The recorded supplied design of a case, re-evaluated with the independent composite oracle
(exploration/stellarator_materials/oracle_glue.py) and no policy, must reproduce the recorded
p_fus, p_aux_required and B_peak, and must sit inside the contract's tolerances: matched fusion
power +-0.5 %, B_peak target +-0.1 T after turn rounding. The re-supplied quantities are checked
against the channels they were read from (design D18). MR-7 structure: every insufficient offer
fails its acceptance check, every generous offer passes it where the conductor is supported; the
equal-duty pairs share ampere-turns exactly; no case sets a retired or reference-prefix key.

Needs exploration/stellarator_materials/studies/cases.json (declare_cases.py writes it). Run:
.codex-test/run python -m pytest tests/study/test_stellarator_materials_policy.py -q
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
STUDIES = ROOT / "exploration" / "stellarator_materials" / "studies"
CASES = STUDIES / "cases.json"


def _load(name, path):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


op = _load("stellarator_materials_offer_policy", STUDIES / "offer_policy.py")
og = op.og

RETIRED = (
    "magnet__coil__I_coil",
    "magnet__winding_pack__j_wp",
    "magnet__winding_pack__B_grade_ref",
    "magnet__winding_pack__field_exponent",
    "magnet__winding_pack__sizing_mode",
    "magnet__winding_pack__inventory_multiplier",
    "magnet__c_support",
    "magnet__e_support",
    "magnet__casing__m_casing_ref",
    "magnet__R0",
)  # exploration/stellarator_e2e/studies/study_route.py:184-189
REL = 1e-9


@pytest.fixture(scope="module")
def data():
    if not CASES.exists():
        pytest.fail(
            f"{CASES.relative_to(ROOT)} is missing: run "
            ".codex-test/run python exploration/stellarator_materials/studies/declare_cases.py"
        )
    return json.loads(CASES.read_text())


@pytest.fixture(scope="module")
def cases(data):
    return data["cases"]


def _suffix(case):
    prefix = og.MATERIAL_PREFIXES[case["labels"]["material"]]
    return {k[len(prefix) :]: v for k, v in case["inputs"].items()}


def _is_design(case):
    return case["labels"]["offer_kind"] in ("reference", "companion") and case.get("expected")


def _design_variant(case):
    v = case["labels"]["variant"]
    return v == "none" or v in op.DESIGN_VARIANTS


def _sample(cases):
    """
    Across cells and materials: per (geometry, f_ren, material) the reference-size design, else
    the first recorded design; one companion; one design per design variant; MR-7 offers at the
    reference size.
    """
    picked, seen = [], set()
    ordered = sorted(
        cases,
        key=lambda c: ((c["labels"]["R"], c["labels"]["a"]) != op.REFERENCE_SIZE, c["case_id"]),
    )
    for c in ordered:
        lb = c["labels"]
        if not (_is_design(c) and lb["variant"] == "none" and lb["offer_kind"] == "reference"):
            continue
        key = (lb["cell_geometry"], lb["cell_f_ren"], lb["material"])
        if key not in seen:
            seen.add(key)
            picked.append(c)
    for pred in (
        lambda c: _is_design(c) and c["labels"]["offer_kind"] == "companion",
        *[
            (lambda v: lambda c: _is_design(c) and c["labels"]["variant"] == v)(v)
            for v in op.DESIGN_VARIANTS
        ],
    ):
        hit = next((c for c in cases if pred(c)), None)
        if hit is not None and hit not in picked:
            picked.append(hit)
    for kind in ("insufficient", "generous"):
        for m in op.MATERIALS:
            hit = next(
                (
                    c
                    for c in cases
                    if c["labels"]["offer_kind"] == kind
                    and c["labels"]["material"] == m
                    and (c["labels"]["R"], c["labels"]["a"]) == op.REFERENCE_SIZE
                    and c.get("expected")
                ),
                None,
            )
            if hit is not None:
                picked.append(hit)
    return picked


@pytest.fixture(scope="module")
def evaluated(cases):
    """Re-evaluate the sample with the plain oracle: no policy, no memo."""
    out = []
    for c in _sample(cases):
        out.append((c, og.evaluate_material_case(_suffix(c), c["labels"]["material"])))
    return out


# ---------------------------------------------------------------------------------------------
# Policy acceptance: reproduction and contract tolerances
# ---------------------------------------------------------------------------------------------
def test_sample_spans_cells_and_materials(evaluated):
    cells = {
        (c["labels"]["cell_geometry"], c["labels"]["cell_f_ren"], c["labels"]["material"])
        for c, _ in evaluated
    }
    assert len(cells) == 18
    assert len(evaluated) >= 20


def test_recorded_design_reevaluated_without_policy_reproduces_recorded_values(evaluated):
    for c, out in evaluated:
        ch = out["channels"]
        exp = c["expected"]
        for rec, channel in (
            ("p_fus", "plasma__fusion__p_fus"),
            ("p_aux_required", "plasma__sustain__p_aux_required"),
            ("B_peak", "magnet__peak_field_calc__B_peak"),
            ("beta", "plasma__beta_calc__beta"),
        ):
            assert ch[channel] == pytest.approx(exp[rec], rel=REL, abs=1e-12), (c["case_id"], rec)
        for channel, value in exp["channels"].items():
            assert ch[channel] == pytest.approx(value, rel=REL, abs=1e-9), (c["case_id"], channel)
        violated = sorted(k for k, s in out["verdicts"].items() if s != "satisfied")
        assert violated == exp["violated"], c["case_id"]


def test_recorded_designs_meet_the_matched_power_and_peak_field_tolerances(cases):
    """Every recorded design: matched designs within +-0.5 % of the reference p_fus;
    power-short designs
    below it; own-sized designs within +-0.1 T of the target after turn rounding."""
    matched = short = 0
    for c in cases:
        if not (_is_design(c) and _design_variant(c)):
            continue
        p_fus = c["expected"]["p_fus"]
        if c["policy"]["power_short"]:
            short += 1
            assert p_fus < op.P_FUS_MATCH * (1.0 + op.TOL_P_FUS), c["case_id"]
        else:
            matched += 1
            assert abs(p_fus / op.P_FUS_MATCH - 1.0) <= op.TOL_P_FUS, c["case_id"]
            assert abs(p_fus / op.P_FUS_MATCH - 1.0) <= op.SEARCH_REL_TOL, c["case_id"]
        if not c["labels"][
            "equal_duty"
        ]:  # equal-duty designs share the Nb3Sn turns (no target rule)
            err = c["expected"]["B_peak"] - c["labels"]["B_peak_target"]
            assert abs(err) <= op.TOL_B_PEAK, (c["case_id"], err)
    assert matched > 0 and short > 0


def test_resupplied_quantities_equal_the_channels_they_were_read_from(evaluated):
    for c, out in evaluated:
        if (
            c["labels"]["offer_kind"] not in ("reference", "companion")
            or c["labels"]["variant"] not in ("none",) + op.DESIGN_VARIANTS
        ):
            continue
        d, ch = _suffix(c), out["channels"]
        assert d["heating__p_wallplug_heat"] == op.heating_rule(
            ch["plasma__sustain__p_aux_required"]
        )
        assert d["magnet__m_support"] == pytest.approx(
            og.structure_mass_rule(ch["magnet__stored_energy__W_mag"]), rel=1e-12
        )
        assert out["checks"]["structure_mass"]["relative_residual"] == pytest.approx(0.0, abs=1e-12)
        assert (
            d["cryoplant__rated_cold_W"] == op.list_rating(ch["cryoplant__cold_stage__q_cold"])[0]
        )
        assert (
            d["cryoplant__rated_intercept_W"]
            == op.list_rating(ch["cryoplant__cold_stage__q_shield"])[0]
        )
        for key, channel in op.CLASS_MAP.items():
            assert d[key] == max(ch[channel], 0.0), (c["case_id"], key)
        for key, margin in op.SCREENED_RATINGS:
            if ch[margin.replace("__margin", "__applicable")] != 1.0:
                continue
            demand = d[key] - ch[margin]
            assert d[key] == pytest.approx(op.PACKAGE_MARGIN * demand, rel=REL, abs=1e-12), (
                c["case_id"],
                key,
            )
        for key, channel in op.OFFERED_STATES:
            assert d[key] == ch[channel], (c["case_id"], key)
        for key, channel in op.PURCHASED_MASSES:
            assert d[key] == pytest.approx(op.PACKAGE_MARGIN * ch[channel], rel=REL)
        for name, (purchase, rating) in op.PURCHASES.items():
            expected = (
                op.PIN[purchase]
                if rating is None
                else op.PIN[purchase] * (d[rating] / op.PIN[rating]) ** op.PURCHASE_EXPONENT
            )
            assert d[purchase] == pytest.approx(expected, rel=REL)
        assert c["flags"]["free_capacity"] == list(op.FREE_CAPACITY)
        # r5 (P), notes Q14: the IHX count is the smallest meeting 1.05 x required area <= installed
        # area
        # at its own duty; the cooling facilities follow it
        n = d[op.IHX_COUNT_KEY]
        req, inst = (
            ch["heat_transport__equipment__ihx_required_area"],
            ch["heat_transport__equipment__ihx_installed_area"],
        )
        assert n == int(n) >= 1 and op.PACKAGE_MARGIN * req <= inst, c["case_id"]
        floor = c["policy"]["trace"]["ihx_floor"]
        assert n == max(math.ceil(op.PACKAGE_MARGIN * n * req / inst - 1e-9), floor, 1), c[
            "case_id"
        ]
        assert floor <= n, c["case_id"]
        assert d["buildings__selected_cooling_hall_length"] == pytest.approx(
            op.PACKAGE_MARGIN * ch["buildings__layout__cooling_hall_required_length"], rel=REL
        )
        assert d["buildings__selected_cooling_annex_width"] == pytest.approx(
            op.PACKAGE_MARGIN * ch["buildings__layout__cooling_annex_required_width"], rel=REL
        )
        for state in ("clean", "dirty"):
            for kind in op.COOLING_KINDS:
                assert d[f"buildings__cooling_{state}_{kind}_positions"] == math.ceil(
                    op.PACKAGE_MARGIN * ch[f"buildings__layout__cooling_{state}_{kind}_required"]
                    - 1e-9
                )


def test_matched_designs_sit_at_the_least_heating_ladder_value(cases):
    """
    Contract r5 section 5 (P), notes Q1: among the ladder values meeting the bounds at matched
    power, the least required heating (ties to 14.63 keV), read from the recorded ladder of
    every matched design.
    """
    checked = 0
    for c in cases:
        if not (_is_design(c) and _design_variant(c)) or c["labels"]["offer_kind"] != "reference":
            continue
        trace = c["policy"]["trace"] or {}
        if trace.get("operating_point") != "matched":
            continue
        ok = [
            r
            for r in trace["ladder"]
            if r["matched"] and r.get("within_beta") and r["p_aux"] >= 0.0 and r["evaluable"]
        ]
        least = min(r["p_aux"] for r in ok)
        chosen = op.select_matched(trace["ladder"])
        assert chosen["p_aux"] == least
        d = _suffix(c)
        assert (d["plasma__T_i0"], d["plasma__n_e0"]) == (chosen["T"], chosen["n_e0"]), c["case_id"]
        assert c["labels"]["T_i0_ladder"] == chosen["T"], c["case_id"]
        checked += 1
    assert checked > 100


def test_divertor_is_carried_as_an_open_gap_with_its_flag(cases, evaluated):
    """
    Contract r5 (P), notes Q5: divertor_heat_ok never decides a status; every evaluated design
    carries divertor_pass and its margin.
    """
    for c in cases:
        if not c.get("expected"):
            continue
        assert "divertor_heat_ok" not in c["reasons"], c["case_id"]
        assert c["flags"]["divertor_pass"] == (
            "divertor_heat_ok" not in c["expected"]["violated"]
        ), c["case_id"]
    for c, out in evaluated:
        assert c["flags"]["divertor_pass"] == (out["verdicts"]["divertor_heat_ok"] == "satisfied")
        assert c["flags"]["divertor_q_target_margin"] == pytest.approx(
            out["channels"]["divertor__divheat__q_target_margin"], rel=REL, abs=1e-12
        )


def test_recorded_status_follows_contract_section7_from_the_reevaluation(evaluated):
    for c, out in evaluated:
        if c["status_expected"] == "ignited":
            assert out["channels"]["plasma__sustain__p_aux_required"] < 0.0
            continue
        trace = c["policy"]["trace"] or {}
        status, reasons = op.status_of(c["labels"]["material"], out, "reference", trace)
        assert status == c["status_expected"], c["case_id"]


def test_recorded_designs_pass_the_magnet_supply_checks_they_were_sized_for(cases):
    """
    acceptance, pack area and fit hold on every policy-sized design (never re-sized inside the
    model).
    """
    for c in cases:
        if not (_is_design(c) and _design_variant(c)):
            continue
        ch = c["expected"]["channels"]
        assert ch["magnet__conductor__acceptance_margin"] >= 0.0, c["case_id"]
        assert ch["magnet__area__fit_margin"] >= 0.0, c["case_id"]
        assert ch["magnet__wp_fit__minimum_margin"] >= 0.0, c["case_id"]


# ---------------------------------------------------------------------------------------------
# MR-7 structure
# ---------------------------------------------------------------------------------------------
def test_every_insufficient_offer_fails_its_check_and_generous_passes_where_supported(
    cases, evaluated
):
    mr7 = [c for c in cases if c["labels"]["offer_kind"] in ("insufficient", "generous")]
    assert mr7
    for c in mr7:
        base = next(b for b in cases if b["case_id"] == c["policy"]["base_case"])
        n, n0 = (
            c["inputs"][next(k for k in c["inputs"] if k.endswith("magnet__n_elements"))],
            base["inputs"][next(k for k in base["inputs"] if k.endswith("magnet__n_elements"))],
        )
        diff = {k for k in c["inputs"] if c["inputs"][k] != base["inputs"][k]}
        assert diff == {next(k for k in c["inputs"] if k.endswith("magnet__n_elements"))}, c[
            "case_id"
        ]
        if not c.get("expected"):
            continue
        violated = set(c["expected"]["violated"])
        if c["labels"]["offer_kind"] == "insufficient":
            assert n == (9 * int(n0)) // 10
            assert "magnet__acceptance_ok" in violated, c["case_id"]
        else:
            assert n == (12 * int(n0) + 9) // 10
            if c["expected"]["channels"]["magnet__conductor__status_code"] != 0.0:
                assert "magnet__acceptance_ok" not in violated, c["case_id"]
    for c, out in evaluated:
        kind = c["labels"]["offer_kind"]
        if kind == "insufficient":
            assert out["verdicts"]["magnet__acceptance_ok"] == "violated"
        elif kind == "generous" and out["channels"]["magnet__conductor__status_code"] != 0.0:
            assert out["verdicts"]["magnet__acceptance_ok"] == "satisfied"


def test_equal_duty_pairs_share_ampere_turns_exactly(cases):
    nb = {}
    for c in cases:
        lb = c["labels"]
        if (
            lb["material"] == "nb3sn"
            and lb["offer_kind"] == "reference"
            and _design_variant(c)
            and c["inputs"]
        ):
            d = _suffix(c)
            nb[
                (
                    lb["cell_geometry"],
                    lb["cell_f_ren"],
                    lb["B_peak_target"],
                    lb["R"],
                    lb["a"],
                    lb["variant"],
                )
            ] = (d["magnet__coil__reference_turns"], d["magnet__coil__turn_current"])
    pairs = 0
    for c in cases:
        lb = c["labels"]
        if not (
            lb["material"] == "rebco"
            and lb["equal_duty"]
            and lb["offer_kind"] == "reference"
            and _design_variant(c)
            and c["inputs"]
        ):
            continue
        variant = lb["variant"] if lb["variant"] != "common-P" else "none"
        key = (
            lb["cell_geometry"],
            lb["cell_f_ren"],
            lb["B_peak_target"],
            lb["R"],
            lb["a"],
            variant,
        )
        d = _suffix(c)
        turns, current = nb[key]
        assert (
            d["magnet__coil__reference_turns"] == turns
            and d["magnet__coil__turn_current"] == current
        ), c["case_id"]
        assert (
            d["magnet__coil__reference_turns"] * d["magnet__coil__turn_current"] == turns * current
        )
        pairs += 1
    assert pairs >= 9 * 7 * 3 - 5


# ---------------------------------------------------------------------------------------------
# Keys and coverage
# ---------------------------------------------------------------------------------------------
def test_no_case_sets_a_retired_removed_or_reference_prefix_key(cases):
    for c in cases:
        prefix = og.MATERIAL_PREFIXES[c["labels"]["material"]]
        for key in c["inputs"]:
            assert key.startswith(prefix), (c["case_id"], key)
            assert not key.startswith(og.REFERENCE_PREFIX)
            suffix = key[len(prefix) :]
            assert suffix not in og.REMOVED_KEYS, (c["case_id"], key)
            assert suffix not in RETIRED, (c["case_id"], key)
        if c["inputs"]:
            d = _suffix(c)
            assert set(og.REQUIRED_SUPPLIED[c["labels"]["material"]]) <= set(d), c["case_id"]
            og.resolve_material_inputs(
                d, c["labels"]["material"]
            )  # the oracle's key schema accepts it


def test_first_pass_covers_the_contract_grid(data, cases):
    points = defaultdict(set)
    for c in cases:
        lb = c["labels"]
        if lb["variant"] == "none" and lb["offer_kind"] == "reference":
            points[(lb["cell_geometry"], lb["cell_f_ren"])].add(
                (lb["material"], lb["B_peak_target"], lb["R"], lb["a"])
            )
    assert len(points) == 9
    for cell, pts in points.items():
        assert len(pts) == 7 * (
            len(op.NB3SN_FIELDS) + len(op.REBCO_EQUAL_DUTY_FIELDS) + len(op.REBCO_OWN_FIELDS)
        ), cell
    counts = data["header"]["counts"]
    assert 650 <= counts["recorded_designs"] <= 1300
    assert data["header"]["n_cases"] == len(cases)


def test_every_rebco_design_is_evaluated_at_both_contract_prices(cases):
    base = {
        c["case_id"]
        for c in cases
        if _is_design(c) and c["labels"]["material"] == "rebco" and _design_variant(c)
    }
    priced = defaultdict(set)
    for c in cases:
        if c["policy"].get("base_case") in base:
            priced[c["policy"]["base_case"]].add(c["labels"]["price_rebco"])
    for cid in base:
        assert {30.0, 10.0} <= priced[cid], cid
