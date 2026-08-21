"""Phase 1 adapter contract tests for extract_explorer_data.py (Item 10).

Validates the strict-consumer contract (Bet 1, Invariant 1), routing cross-check
(Bet 7, Invariant 2), pending-design-point skip (Bet 8, Invariant 5), and
asterisk_in_comparison threading (Bet 2, Invariant 4) against synthetic fixtures.

See `.project/completed/20260821_concept-rework-explorer-pilot/{spec,design,plan}.md`.
"""

from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Any

import pytest

from exploration.concept_explorer.extract_explorer_data import (
    ExtractionError,
    run_extraction,
    verify_two_knob,
)


# ---------------------------------------------------------------------------
# Fixture helper
# ---------------------------------------------------------------------------


# A self-contained model_setup.py source that mimics the costingfe surface
# (module-level model, result, result_1gw) using stdlib only — no real
# costingfe dependency. The strings `from costingfe` and `CostModel` appear
# verbatim so the run_extraction import-source heuristic flags is_costingfe=True.
_COSTINGFE_SHAPED_MODULE = """
# Synthetic costingfe-shaped model_setup for tests.
# Tokens required by the explorer's import-source heuristic:
#   from costingfe import CostModel  (commented — we don't actually import)
# CostModel
import dataclasses


@dataclasses.dataclass
class _PowerTable:
    p_net: float = 1000.0
    q_eng: float = 8.0
    rec_frac: float = 0.12


@dataclasses.dataclass
class _Costs:
    cas10: float = 10.0
    cas21: float = 50.0
    cas22: float = 200.0
    cas23: float = 80.0
    cas24: float = 30.0
    cas25: float = 10.0
    cas26: float = 5.0
    cas27: float = 8.0
    cas28: float = 3.0
    cas29: float = 40.0
    cas30: float = 30.0
    cas40: float = 20.0
    cas50: float = 10.0
    cas60: float = 50.0
    cas70: float = 5.0
    cas80: float = 3.0
    cas90: float = 2.0
    lcoe: float = 150.0
    overnight_cost: float = 5000.0
    total_capital: float = 600.0


@dataclasses.dataclass
class _Result:
    costs: _Costs
    power_table: _PowerTable
    cas22_detail: dict
    overridden: list
    params: dict


class _Model:
    def sensitivity(self, params, cost_overrides=None):
        return {
            "engineering": {"availability": -1.0},
            "financial": {"interest_rate": 0.5},
        }


model = _Model()
result = _Result(
    costs=_Costs(),
    power_table=_PowerTable(),
    cas22_detail={},
    overridden=[],
    params={"availability": 0.85, "interest_rate": 0.08},
)
result_1gw = __RESULT_1GW__
"""


_STANDALONE_SHAPED_MODULE = """
# Synthetic standalone model_setup (no costingfe import, no CostModel symbol).
# Triggers is_costingfe=False in the explorer heuristic.
import dataclasses


@dataclasses.dataclass
class Params:
    plant_availability: float = 0.85

    def compute(self):
        return {"costs": {"total_capital": 1.0}, "economics": {"lcoe_USD_per_MWh": 100.0}, "power": {"p_net": 100.0}, "cas22": {}}


params = Params()
results = params.compute()
"""


def _result_1gw_source(*, net: float = 1000.0, n_mod: float | None) -> str:
    """Generate a literal expression for the result_1gw module-level binding."""
    if n_mod is None:
        return "None"
    return (
        "_Result(costs=_Costs(), power_table=_PowerTable(), cas22_detail={}, "
        f"overridden=[], params={{'availability': 0.85, 'interest_rate': 0.08, "
        f"'net_electric_mw': {net!r}, 'n_mod': {n_mod!r}}})"
    )


def write_concept_fixture(
    analyses_dir: Path,
    *,
    concept_id: str = "99",
    status: str | None = "costingfe",
    p_native: float | None = 233,
    confinement_family: str | None = "MFE",
    include_result_1gw: bool = True,
    result_1gw_n_mod: float | None = None,
    model_setup_kind: str = "costingfe",  # "costingfe" | "standalone" | "missing"
) -> Path:
    """Write a synthetic concept dir under analyses_dir/{cid}-test/.

    `status` becomes the Comparison-Status frontmatter value (None → omit field).
    `p_native` becomes P-Native (None → omit). When `result_1gw_n_mod` is None and
    `include_result_1gw` is True, n_mod is derived as 1000/p_native (the
    contract-conforming value).
    """
    concept_dir = analyses_dir / f"{concept_id}-test-concept"
    concept_dir.mkdir(parents=True, exist_ok=True)

    fm_lines = [
        "---",
        f"ID: {concept_id}-test-concept",
        "Concept: Test Concept",
    ]
    if confinement_family is not None:
        fm_lines.append(f"Confinement-Family: {confinement_family}")
    if status is not None:
        fm_lines.append(f"Comparison-Status: {status}")
    if p_native is not None:
        fm_lines.append(f"P-Native: {p_native}")
    fm_lines.append("---")

    (concept_dir / "analysis.md").write_text(
        "\n".join(fm_lines) + "\n\nBody.\n", encoding="utf-8"
    )

    if model_setup_kind == "costingfe":
        if include_result_1gw:
            if result_1gw_n_mod is None and p_native is not None:
                # Match what model_setup_helpers.run_native_and_1gw emits:
                # max(1, int(round(1000 / p_native))).
                derived = max(1, round(1000.0 / float(p_native)))
            else:
                derived = result_1gw_n_mod
            expr = _result_1gw_source(net=1000.0, n_mod=derived)
        else:
            expr = "None"
        src = _COSTINGFE_SHAPED_MODULE.replace("__RESULT_1GW__", expr)
        (concept_dir / "model_setup.py").write_text(textwrap.dedent(src), encoding="utf-8")
    elif model_setup_kind == "standalone":
        (concept_dir / "model_setup.py").write_text(
            textwrap.dedent(_STANDALONE_SHAPED_MODULE), encoding="utf-8"
        )
    elif model_setup_kind == "missing":
        pass  # no model_setup.py
    else:
        raise ValueError(f"unknown model_setup_kind: {model_setup_kind!r}")

    return concept_dir


# ---------------------------------------------------------------------------
# Strict-consumer contract (Invariant 1, FR-3)
# ---------------------------------------------------------------------------


class TestStrictConsumer:
    def test_costingfe_missing_result_1gw_raises(self, tmp_path: Path) -> None:
        analyses_dir = tmp_path / "analyses"
        data_dir = tmp_path / "data"
        write_concept_fixture(
            analyses_dir,
            status="costingfe",
            p_native=233,
            include_result_1gw=False,
        )
        with pytest.raises(ExtractionError, match="result_1gw missing"):
            run_extraction(
                analyses_dir, data_dir, concept_filter=["99"], skip_narrative=True
            )

    def test_costingfe_asterisked_missing_result_1gw_raises(self, tmp_path: Path) -> None:
        analyses_dir = tmp_path / "analyses"
        data_dir = tmp_path / "data"
        write_concept_fixture(
            analyses_dir,
            status="costingfe-asterisked",
            p_native=1500,
            include_result_1gw=False,
        )
        with pytest.raises(ExtractionError, match="result_1gw missing"):
            run_extraction(
                analyses_dir, data_dir, concept_filter=["99"], skip_narrative=True
            )


# ---------------------------------------------------------------------------
# Two-knob verification (Invariant 1, FR-4)
# ---------------------------------------------------------------------------


class TestVerifyTwoKnob:
    def test_n_mod_mismatch_raises(self, tmp_path: Path) -> None:
        analyses_dir = tmp_path / "analyses"
        data_dir = tmp_path / "data"
        # P_native=233 → helper emits n_mod=max(1, round(1000/233))=4, but inject 5.0
        write_concept_fixture(
            analyses_dir,
            status="costingfe",
            p_native=233,
            include_result_1gw=True,
            result_1gw_n_mod=5.0,
        )
        with pytest.raises(ExtractionError, match="n_mod"):
            run_extraction(
                analyses_dir, data_dir, concept_filter=["99"], skip_narrative=True
            )

    def test_net_electric_mw_mismatch_raises(self, tmp_path: Path) -> None:
        # Build a result_1gw with net_electric_mw=500 (not 1000).
        import types

        class _R:
            params: dict[str, Any]

        r = _R()
        r.params = {"net_electric_mw": 500.0, "n_mod": 1000.0 / 233.0}
        with pytest.raises(ExtractionError, match="net_electric_mw"):
            verify_two_knob(r, p_native=233, concept_id="99")

    def test_passes_for_conforming_values(self, tmp_path: Path) -> None:
        # n_mod is the integer-rounded count the helper emits, not 1000/p_native.
        class _R:
            params: dict[str, Any] = {
                "net_electric_mw": 1000.0,
                "n_mod": 4,  # max(1, round(1000/233)) = 4
            }

        verify_two_knob(_R(), p_native=233, concept_id="99")  # no raise

    def test_p_native_zero_raises(self) -> None:
        class _R:
            params = {"net_electric_mw": 1000.0, "n_mod": 1.0}

        with pytest.raises(ExtractionError, match="P-Native"):
            verify_two_knob(_R(), p_native=0, concept_id="99")


# ---------------------------------------------------------------------------
# Routing cross-check (Invariant 2, Bet 7)
# ---------------------------------------------------------------------------


class TestRoutingCrossCheck:
    def test_costingfe_status_but_standalone_model_setup_raises(
        self, tmp_path: Path
    ) -> None:
        analyses_dir = tmp_path / "analyses"
        data_dir = tmp_path / "data"
        write_concept_fixture(
            analyses_dir,
            status="costingfe",
            p_native=233,
            model_setup_kind="standalone",
        )
        with pytest.raises(ExtractionError, match="routing disagreement"):
            run_extraction(
                analyses_dir, data_dir, concept_filter=["99"], skip_narrative=True
            )

    def test_costingfe_status_but_no_model_setup_raises(self, tmp_path: Path) -> None:
        analyses_dir = tmp_path / "analyses"
        data_dir = tmp_path / "data"
        write_concept_fixture(
            analyses_dir,
            status="costingfe",
            p_native=233,
            model_setup_kind="missing",
        )
        with pytest.raises(ExtractionError, match="routing disagreement"):
            run_extraction(
                analyses_dir, data_dir, concept_filter=["99"], skip_narrative=True
            )

    def test_freeform_deferred_but_costingfe_model_setup_raises(
        self, tmp_path: Path
    ) -> None:
        analyses_dir = tmp_path / "analyses"
        data_dir = tmp_path / "data"
        write_concept_fixture(
            analyses_dir,
            status="freeform-deferred",
            p_native=None,
            model_setup_kind="costingfe",
        )
        with pytest.raises(ExtractionError, match="routing disagreement"):
            run_extraction(
                analyses_dir, data_dir, concept_filter=["99"], skip_narrative=True
            )


# ---------------------------------------------------------------------------
# Pending-design-point skip (Invariant 5, Bet 8)
# ---------------------------------------------------------------------------


class TestPendingDesignPoint:
    def test_skipped_no_json_written(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        analyses_dir = tmp_path / "analyses"
        data_dir = tmp_path / "data"
        write_concept_fixture(
            analyses_dir,
            status="pending-design-point",
            p_native=None,
            model_setup_kind="missing",  # may not exist yet for pending rows
        )
        run_extraction(
            analyses_dir, data_dir, concept_filter=["99"], skip_narrative=True
        )
        assert not (data_dir / "99.json").exists()
        out = capsys.readouterr().out
        assert "99" in out
        assert "pending-design-point" in out

    def test_end_of_run_skip_summary_present(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        analyses_dir = tmp_path / "analyses"
        data_dir = tmp_path / "data"
        write_concept_fixture(
            analyses_dir,
            concept_id="99",
            status="pending-design-point",
            p_native=None,
            model_setup_kind="missing",
        )
        # Also need a non-skipped concept so the end-of-run summary still prints
        # without WARNING-no-concepts short-circuit.
        write_concept_fixture(
            analyses_dir,
            concept_id="98",
            status="costingfe",
            p_native=233,
        )
        run_extraction(
            analyses_dir,
            data_dir,
            concept_filter=["99", "98"],
            skip_narrative=True,
        )
        out = capsys.readouterr().out
        assert "Skipped 1 concept" in out


# ---------------------------------------------------------------------------
# Asterisk threading (Invariant 4, Bet 2)
# ---------------------------------------------------------------------------


class TestAsteriskFlag:
    def test_costingfe_asterisked_sets_flag_true(self, tmp_path: Path) -> None:
        import json

        analyses_dir = tmp_path / "analyses"
        data_dir = tmp_path / "data"
        write_concept_fixture(
            analyses_dir,
            status="costingfe-asterisked",
            p_native=1500,
        )
        run_extraction(
            analyses_dir, data_dir, concept_filter=["99"], skip_narrative=True
        )
        payload = json.loads((data_dir / "99.json").read_text())
        assert payload["asterisk_in_comparison"] is True

    def test_plain_costingfe_sets_flag_false(self, tmp_path: Path) -> None:
        import json

        analyses_dir = tmp_path / "analyses"
        data_dir = tmp_path / "data"
        write_concept_fixture(
            analyses_dir,
            status="costingfe",
            p_native=233,
        )
        run_extraction(
            analyses_dir, data_dir, concept_filter=["99"], skip_narrative=True
        )
        payload = json.loads((data_dir / "99.json").read_text())
        assert payload["asterisk_in_comparison"] is False
