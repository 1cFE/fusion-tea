"""Flow order (owner ruling 2026-09-15): dagre lays the picture out left to right, so every drawn
edge runs from a producer on the left to its consumer on the right. The ruling is about exactly
this — "the dagre has clear patterns your eyes can follow" — so it is asserted, not assumed.
"""

import overlay_oracle as oracle
import pytest
from viewer2_harness import backward_edges, body_boxes, toggle

SNAP = oracle.load_fixture()
MAGNET = oracle.occ_of(SNAP, "magnet")


# Closing parts merges edges, and the merged graph is not acyclic: the oracle's 116 collapse-all
# edges hold 4 cycles, so dagre has to reverse one edge in each. Fully open there are none.
BACKWARD_MAX = {"open": 0, "start": 4, "magnet": 0}


@pytest.mark.parametrize("state", ["open", "start", "magnet"])
def test_every_edge_runs_left_to_right(reset_v2, state):
    page = reset_v2
    if state == "start":
        page.click("[data-action=collapse-all]")
    if state == "magnet":
        toggle(page, oracle.identity(MAGNET))
    backward = backward_edges(page)
    print(f"{state}: {len(backward)} edges not running left to right")
    assert len(backward) <= BACKWARD_MAX[state], backward


def test_plasma_before_lcoe_column(reset_v2):
    boxes = body_boxes(reset_v2)
    plasma = boxes[oracle.identity(oracle.occ_of(SNAP, "plasma"))]
    lcoe = boxes[oracle.calc_id(SNAP, "lcoe_calc")]
    assert plasma["x2"] < lcoe["x1"]
