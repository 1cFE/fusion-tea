"""The built evolution page, driven in headless Chromium.

The numbers the page shows are checked against an oracle that reads each frame's snapshot straight
from git and counts for itself; it shares no code with build.py.
"""

import json

import pytest
from conftest import REPO, git

COOLING = "installed-cooling-equipment-costs"
DECOMPOSITION = "structural-decomposition"
PYTHON_ONLY = "model-evaluation-domain-readiness"


def oracle_counts(manifest: dict, sha: str) -> dict:
    snap = json.loads(git("show", f"{sha}:{manifest['snapshot_path']}"))
    graph = snap["instance_graph"]["graph"]
    return {
        "calcs": len(graph["calcs"]),
        "checks": len(graph["constraints"]),
        "parts": len(graph["occurrences"]),
        "attributes": len(graph["attrs"]),
        "source_files": len(snap["sources"]["files"]),
    }


def frame_index(built, slug: str) -> int:
    return next(i for i, f in enumerate(built["data"]["frames"]) if f.get("slug") == slug)


def show(page, index: int) -> None:
    page.evaluate("(i) => window.modelEvolution.show(i)", index)
    page.wait_for_selector(f"body[data-evo-state=ready][data-evo-frame='{index}']")


def tile_value(page, metric: str) -> int:
    return int(page.inner_text(f"[data-metric={metric}] .evo-value").replace(",", ""))


def test_the_build_leaves_the_worktree_as_it_found_it(built):
    assert built["status_after"] == built["status_before"]


def test_one_frame_per_manifest_goal_plus_the_baseline(built, manifest):
    frames = built["data"]["frames"]
    assert [f.get("slug") for f in frames[1:]] == [f["slug"] for f in manifest["frames"]]
    assert frames[0]["kind"] == "baseline"


def test_every_frames_metrics_match_the_oracle(built, manifest):
    ends = [manifest["baseline"]["sha"]] + [f["shas"][-1] for f in manifest["frames"]]
    for frame, sha in zip(built["data"]["frames"], ends):
        expected = oracle_counts(manifest, sha)
        assert {k: frame["metrics"][k] for k in expected} == expected, frame["title"]


def test_the_page_opens_on_the_baseline_with_no_file_picker(evo_page, built):
    assert evo_page.evaluate("window.modelEvolution.index") == 0
    assert not evo_page.is_visible(".toolbar .file-pick")
    assert evo_page.inner_text("[data-role=evo-position]") == f"1 / {len(built['data']['frames'])}"
    assert evo_page.is_disabled("[data-role=evo-prev]")


def test_buttons_slider_and_arrow_keys_each_move_one_frame(evo_page):
    evo_page.click("[data-role=evo-next]")
    evo_page.wait_for_selector("body[data-evo-frame='1'][data-evo-state=ready]")
    evo_page.click("[data-role=evo-reveal]")  # a focused checkbox must not swallow the arrow keys
    evo_page.keyboard.press("ArrowRight")
    evo_page.wait_for_selector("body[data-evo-frame='2'][data-evo-state=ready]")
    evo_page.keyboard.press("ArrowLeft")
    evo_page.wait_for_selector("body[data-evo-frame='1'][data-evo-state=ready]")
    evo_page.click("[data-role=evo-prev]")
    evo_page.wait_for_selector("body[data-evo-frame='0'][data-evo-state=ready]")
    evo_page.eval_on_selector("[data-role=evo-slider]", "el => { el.value = '5'; el.dispatchEvent(new Event('input')); }")
    evo_page.wait_for_selector("body[data-evo-frame='5'][data-evo-state=ready]")


@pytest.mark.parametrize("slug", [COOLING, DECOMPOSITION, PYTHON_ONLY])
def test_tiles_and_graph_follow_the_frame(evo_page, built, manifest, slug):
    index = frame_index(built, slug)
    show(evo_page, index)
    expected = oracle_counts(manifest, manifest["frames"][index - 1]["shas"][-1])
    assert {k: tile_value(evo_page, k) for k in expected} == expected
    assert evo_page.evaluate("window.modelVizApp.model.calcs.length") == expected["calcs"]
    assert evo_page.inner_text("[data-role=evo-summary] h1") == built["data"]["frames"][index]["title"]
    assert evo_page.evaluate("location.hash") == "#" + slug


def test_new_calcs_are_marked_once_their_parts_are_open(evo_page, built):
    index = frame_index(built, COOLING)
    show(evo_page, index)
    frame = built["data"]["frames"][index]
    closed_marked = evo_page.evaluate("window.modelVizApp.cy.nodes('.evo-holds-added').map(n => n.data('path'))")
    assert "stellaris/heat_transport" in closed_marked
    evo_page.click("[data-role=evo-reveal]")
    evo_page.wait_for_function("(n) => window.modelVizApp.cy.nodes('.evo-added').length === n", arg=len(frame["calcs"]["added"]))
    names = set(evo_page.evaluate("window.modelVizApp.cy.nodes('.evo-added').map(n => n.data('label').split('\\n')[0])"))
    assert names == {row["name"] for row in frame["calcs"]["added"]}


def test_a_relocation_is_shown_as_moves_not_as_adds_and_removes(built):
    frame = built["data"]["frames"][frame_index(built, DECOMPOSITION)]
    assert len(frame["calcs"]["moved"]) == 44
    assert frame["calcs"]["added"] == [] and frame["calcs"]["removed"] == []
    assert len(frame["calcs"]["changed"]) < 10  # a move alone is not an edit


def test_a_handwritten_calc_expands_to_its_python_body(evo_page, built):
    index = frame_index(built, COOLING)
    show(evo_page, index)
    frame = built["data"]["frames"][index]
    row = next(r for r in frame["calcs"]["added"] if r["name"] == "equipment")
    assert row["handwritten"]
    committed = git("show", f"{frame['after']}:{row['impl']['path']}")
    item = evo_page.locator("[data-role=evo-changes] li", has=evo_page.locator("button.evo-calc", has_text="equipment")).first
    body = item.locator("details", has_text="Python body (")
    body.locator("summary").click()
    assert body.locator("pre").text_content() == committed


def test_a_python_only_edit_is_listed_though_every_count_is_unchanged(evo_page, built):
    index = frame_index(built, PYTHON_ONLY)
    frame, previous = built["data"]["frames"][index], built["data"]["frames"][index - 1]
    assert frame["metrics"] == previous["metrics"]
    assert {row["name"] for row in frame["calcs"]["impl_only"]} >= {"conductor_current"}
    show(evo_page, index)
    assert evo_page.locator("[data-role=evo-changes] h2", has_text="Python body changed").count() == 1


def test_clicking_a_listed_calc_selects_it_in_the_graph(evo_page, built):
    show(evo_page, frame_index(built, COOLING))
    evo_page.click("[data-role=evo-changes] button.evo-calc >> text=equipment")
    evo_page.wait_for_function("() => (window.modelVizApp.state.selected || {}).kind === 'calc'")
    assert "equipment" in evo_page.inner_text("[data-role=panel] h2")


def test_a_link_to_another_goal_moves_an_open_page(evo_page, built):
    index = frame_index(built, DECOMPOSITION)
    evo_page.evaluate("(slug) => { location.hash = slug; }", DECOMPOSITION)
    evo_page.wait_for_selector(f"body[data-evo-frame='{index}'][data-evo-state=ready]")


def pane_height(page) -> float:
    return page.evaluate("document.querySelector('[data-role=graph-pane]').getBoundingClientRect().height")


def test_expand_gives_the_graph_the_window_and_keeps_the_stepping_bar(evo_page, built):
    show(evo_page, frame_index(built, COOLING))
    window_height = evo_page.viewport_size["height"]
    before = pane_height(evo_page)
    evo_page.click("[data-role=evo-expand]")
    assert pane_height(evo_page) > 0.85 * window_height > before
    assert not evo_page.is_visible("[data-role=evo-summary]")
    assert not evo_page.is_visible("[data-role=panel]")  # nothing selected: the side panel gives its width back
    assert evo_page.is_visible("[data-role=evo-slider]")
    assert "calcs: 5 new, 5 changed" in evo_page.inner_text("[data-role=evo-brief]")
    assert evo_page.evaluate("document.documentElement.scrollHeight <= window.innerHeight")  # one screen, no page scroll

    index = evo_page.evaluate("window.modelEvolution.index")
    evo_page.keyboard.press("ArrowRight")  # stepping still works while expanded
    evo_page.wait_for_selector(f"body[data-evo-frame='{index + 1}'][data-evo-state=ready]")

    key = evo_page.evaluate("window.modelVizApp.model.calcs[0].key")
    evo_page.evaluate("(k) => window.modelVizApp.navigateTo(k)", key)
    assert evo_page.is_visible("[data-role=panel]")  # a selection brings the panel back

    evo_page.keyboard.press("Escape")
    assert evo_page.is_visible("[data-role=evo-summary]")
    assert pane_height(evo_page) == pytest.approx(before, abs=2)


def test_full_screen_falls_back_to_the_full_window_view(evo_page):
    # Headless Chromium may grant or refuse full screen; either way the graph must have the window.
    evo_page.click("[data-role=evo-fullscreen]")
    evo_page.wait_for_function("() => document.documentElement.classList.contains('evo-expanded')")
    assert pane_height(evo_page) > 0.8 * evo_page.viewport_size["height"]


def test_viewer_sources_are_untouched():
    # Integration imports these dependencies into a branch which did not yet have v2.
    # Compare content with its source revision rather than requiring a clean index.
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    names = git("ls-tree", "-r", "--name-only", "6a4d241d", "--", "src/model_viz/viewer", "src/model_viz/viewer2", "src/model_viz/export.py").splitlines()
    for name in names:
        assert (root / name).read_text() == git("show", f"6a4d241d:{name}"), name
    assert (REPO / "src/model_viz/evolution/timeline.js").exists()
