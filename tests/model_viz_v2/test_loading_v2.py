"""Loading (spec R15, plan L1–L2): a bad file shows v1's own banner text and draws nothing; a new
load replaces every name the previous snapshot put on the page."""

import overlay_oracle as oracle
import pytest
import viewer2_snapshots as vs
from viewer2_harness import load_snapshot, panel_placeholder, search, selected, show_calc, show_part

SNAP = oracle.load_fixture()

BAD_FILES = {
    "wrong_version": lambda: ("v2.json", vs.wrong_version(SNAP)),
    "no_version": lambda: ("no_version.json", vs.no_version(SNAP)),
    "non_json": lambda: ("picked_by_mistake.pdf", vs.non_json_bytes()),
}


def write_bad(tmp_path, name):
    file_name, content = BAD_FILES[name]()
    if isinstance(content, bytes):
        return vs.write_bytes(tmp_path, file_name, content)
    return vs.write(tmp_path, file_name, content)


def banner_text(page) -> str:
    assert page.is_visible("[data-role=error-banner]")
    return page.text_content("[data-role=error-banner]")


def assert_nothing_drawn(page) -> None:
    assert page.evaluate("() => window.modelVizApp.cy.elements().length") == 0
    assert page.evaluate("() => window.modelVizApp.model") is None
    assert selected(page) is None
    assert panel_placeholder(page) is not None
    assert page.eval_on_selector_all("datalist[data-role=find-list] option", "os => os.length") == 0


@pytest.mark.parametrize("name", list(BAD_FILES))
def test_bad_file_shows_v1s_banner(v1_page, v2_page, fixture_path, tmp_path, name):
    path = write_bad(tmp_path, name)
    assert load_snapshot(v2_page, fixture_path) == "ready"
    show_calc(v2_page, oracle.calc_id(SNAP, "geom"))
    assert load_snapshot(v1_page, path) == "error"
    assert load_snapshot(v2_page, path) == "error"
    assert banner_text(v2_page) == banner_text(v1_page)
    assert_nothing_drawn(v2_page)


def test_reload_replaces_every_name(v2_page, fixture_path, tmp_path):
    page = v2_page
    assert load_snapshot(page, fixture_path) == "ready"
    show_calc(page, oracle.calc_id(SNAP, "geom"))
    show_part(page, oracle.occ_of(SNAP, "magnet"))
    search(page, "cas")
    originals = vs.renamed_names(SNAP)
    renamed = vs.renamed(SNAP)
    assert originals.isdisjoint(vs.renamed_names(renamed))
    assert load_snapshot(page, vs.write(tmp_path, "renamed.json", renamed)) == "ready"
    assert selected(page) is None and panel_placeholder(page) is not None
    assert page.input_value("[data-role=search-input]") == ""
    assert page.text_content("[data-role=search-status]") == ""
    # The name line of every label (a calc's second line is its module tag, which comes from the
    # source path and is not renamed).
    labels = page.evaluate("() => window.modelVizApp.cy.nodes().map(n => n.data('label'))")
    words = {w for label in labels for w in label.split("\n")[0].replace("\u00b7", " ").split()}
    assert not (words & originals), words & originals
    options = set(
        page.eval_on_selector_all(
            "datalist[data-role=find-list] option", "os => os.map(o => o.value)"
        )
    )
    assert not {o for o in options if o in originals or o.split("/")[-1] in originals}
    assert vs.RENAME_PREFIX + "geom" in options
    show_calc(page, oracle.calc_id(SNAP, "geom"))
    assert page.text_content("[data-role=panel] [data-role=calc-name]") == vs.RENAME_PREFIX + "geom"
    link_texts = page.eval_on_selector_all(
        "[data-role=panel] [data-calc-key]", "ls => ls.map(l => l.textContent)"
    )
    assert link_texts and all(t.startswith(vs.RENAME_PREFIX) for t in link_texts), link_texts
    show_part(page, oracle.occ_of(SNAP, "magnet"))
    assert (
        page.text_content("[data-role=panel] [data-role=part-name]") == vs.RENAME_PREFIX + "magnet"
    )
    assert page.text_content("[data-role=panel] [data-role=part-path]").startswith(vs.RENAME_PREFIX)
