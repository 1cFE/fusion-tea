"""Detail panel criteria P1–P6, checked for every fixture calc against the raw snapshot."""

from collections import Counter

import pytest
from edge_oracle import calc_by_name, calcs, load_fixture, producer_bindings
from panel_dom import panel_dump
from viewer_harness import load_snapshot, show_calc
from viewer_snapshots import earlier_entry_ends_with_doc, unrenderable_tree, write

DERIVED_LABEL = "derived from expression structure; the snapshot has no formula text for this calc."
SECTIONS = ["location", "formula", "doc", "inputs", "outputs"]
PROVENANCE = "Lines reconstructed by codegen from the parsed model; not verbatim source text."


@pytest.fixture(scope="module")
def panels(loaded_fixture_page):
    """node_id -> the rendered panel's DOM data, one showCalc per fixture calc."""
    dumps = {}
    for calc in calcs(load_fixture()):
        show_calc(loaded_fixture_page, calc["node_id"])
        dumps[calc["node_id"]] = panel_dump(loaded_fixture_page)
    return dumps


def edge_kind(inp) -> str:
    edge = inp["edge"]
    if edge is None:
        return "default"
    return {"producer": "producer", "node": "parameter", "literal": "literal"}[edge["kind"]]


def print_ir(node) -> str:
    """Independent printer for the fixture's +, *, reference and literal trees."""
    if node["kind"] == "feature_ref":
        return node["reference"]["source_name"]
    if node["kind"] == "literal":
        value = node["literal"]["value"]
        return str(int(value)) if float(value).is_integer() else repr(value)
    parts = []
    for operand in node["operands"]:
        printed = print_ir(operand)
        if node["operator"] == "*" and operand["kind"] == "operator" and operand["operator"] == "+":
            printed = f"({printed})"
        parts.append(printed)
    return f" {node['operator']} ".join(parts)


def ir_refs(node) -> list[str]:
    if node["kind"] == "feature_ref":
        return [node["reference"]["source_name"]]
    return [ref for operand in node.get("operands", []) for ref in ir_refs(operand)]


def test_panel_sections(panels):
    snap = load_fixture()
    for calc in calcs(snap):
        dump = panels[calc["node_id"]]
        assert dump["nodeId"] == calc["node_id"]
        assert dump["header"] == calc["display_name"]
        assert dump["sections"] == SECTIONS
        assert all(dump["sectionText"][name].strip() for name in SECTIONS), calc["display_name"]
        assert dump["provenance"] == PROVENANCE


def test_formula_entries_verbatim(panels):
    with_text = [c for c in calcs(load_fixture()) if c["calc_expressions"]]
    assert len(with_text) == 66  # WI-057 (2026-09-13): feat/demo-maturation's WI-050 operating_heat (+1 calc, +3 outputs, +2 bound attributes)
    for calc in with_text:
        dump = panels[calc["node_id"]]
        entries = dump["formulaEntries"]
        assert [e["index"] for e in entries] == list(range(len(calc["calc_expressions"])))
        assert [e["text"] for e in entries] == calc["calc_expressions"], calc["display_name"]
        assert calc["doc_comment"] in dump["docText"]
        assert entries[-1]["repeat"] is True
        assert not any(e["repeat"] for e in entries[:-1])
        assert DERIVED_LABEL not in dump["sectionText"]["formula"]


def test_calendar_note(panels):
    calendar = calc_by_name(load_fixture(), "calendar")
    dump = panels[calendar["node_id"]]
    assert [e["repeat"] for e in dump["formulaEntries"]] == [True]
    assert "No formula lines recorded for this calc." in dump["sectionText"]["formula"]
    assert dump["docText"] == calendar["doc_comment"]
    # WI-057 (2026-09-13): on feat/demo-maturation several handwritten calcs carry a doc-only expression
    # list like the calendar (the remediation's WI-053..WI-055 domain work), so their panels show the same note.
    def doc_only(c):
        return len(c["calc_expressions"]) == 1 and c["calc_expressions"][0].startswith("See documentation:")
    doc_only_calcs = [c for c in calcs(load_fixture()) if c["calc_expressions"] and doc_only(c)]
    assert calendar["node_id"] in {c["node_id"] for c in doc_only_calcs}
    assert len(doc_only_calcs) == 8  # WI-057: calendar, cas71_calc, cas80_calc, idc, lcoe_calc, peak_field_calc, wp_sizing, wp_stress
    for calc in doc_only_calcs:
        assert "No formula lines recorded for this calc." in panels[calc["node_id"]]["sectionText"]["formula"]
    others = [c for c in calcs(load_fixture()) if c["calc_expressions"] and not doc_only(c)]
    assert len(others) == 58  # WI-057: 66 calcs with expressions on the merged model, minus the doc-only ones
    for calc in others:
        assert "No formula lines recorded" not in panels[calc["node_id"]]["sectionText"]["formula"]


def test_derived_formulas(panels):
    derived = [c for c in calcs(load_fixture()) if not c["calc_expressions"]]
    assert len(derived) == 11
    assert {"total_capital", "cas22_capital"} <= {c["display_name"] for c in derived}
    for calc in derived:
        dump = panels[calc["node_id"]]
        formula_text = dump["sectionText"]["formula"]
        assert DERIVED_LABEL in formula_text
        assert "No formula available" not in formula_text
        (output,) = calc["outputs"]
        assert dump["derived"] == f"{output['name']} = {print_ir(calc['expression_ir'])}"
        refs = ir_refs(calc["expression_ir"])
        positions = [dump["derived"].index(ref) for ref in refs]
        assert positions == sorted(positions), calc["display_name"]
        assert dump["formulaEntries"] == []
        assert dump["docAbsent"] is True
        assert "No documentation in the snapshot for this calc." in dump["sectionText"]["doc"]
        assert f"{calc['source_file']}:{calc['source_line']}" == dump["location"]["text"]
        assert len(dump["inputs"]) == len(calc["inputs"])
        assert len(dump["outputs"]) == len(calc["outputs"])


def test_input_kinds_and_totals(panels):
    snap = load_fixture()
    attrs = {a["node_id"]: a for a in snap["instance_graph"]["graph"]["attrs"]}
    totals = Counter()
    for calc in calcs(snap):
        rows = panels[calc["node_id"]]["inputs"]
        assert [(r["name"], r["kind"]) for r in rows] == [
            (i["name"], edge_kind(i)) for i in calc["inputs"]
        ], calc["display_name"]
        for row, inp in zip(rows, calc["inputs"]):
            totals[row["kind"]] += 1
            assert row["kind"] in row["text"]
            if row["kind"] == "literal":
                assert float(row["value"]) == inp["edge"]["value"]
            if row["kind"] == "default":
                assert float(row["value"]) == inp["metadata"]["default_value"]
            if row["kind"] == "parameter":
                attr = attrs[inp["edge"]["target"]]
                assert attr["display_name"] in row["text"]
                if attr["value"] is None:
                    assert "no value in snapshot" in row["text"] and row["hasWarning"]
                else:
                    assert str(attr["value"]) == row["value"] or float(row["value"]) == float(
                        attr["value"]
                    )
    assert totals == {"producer": 152, "parameter": 236, "literal": 10, "default": 52}  # WI-057 (2026-09-13): feat/demo-maturation's WI-050 operating_heat (+1 calc, +3 outputs, +2 bound attributes)

    fuel_handling = calc_by_name(snap, "fuel_handling")
    rows = {r["name"]: r for r in panels[fuel_handling["node_id"]]["inputs"]}
    power = rows["power"]
    assert power["kind"] == "producer" and power["linkKey"] is not None
    upstream = next(c for c in calcs(snap) if c["node_id"] == power["producerNodeId"])
    port = next(o for o in upstream["outputs"] if o["port"]["output"] == power["outputId"])
    assert upstream["display_name"] in power["text"] and port["name"] in power["text"]
    base = rows["base"]
    assert base["kind"] == "parameter" and "fuel_handling_base" in base["text"]
    assert float(base["value"]) == 120000000.0
    assert rows["ref_power"]["kind"] == "literal" and float(rows["ref_power"]["value"]) == 1000.0

    fuel = calc_by_name(snap, "fuel")
    default = {r["name"]: r for r in panels[fuel["node_id"]]["inputs"]}["s_per_fpy_in"]
    assert default["kind"] == "default" and float(default["value"]) == 31536000.0


def test_bindings_both_directions(panels):
    snap = load_fixture()
    want = Counter(producer_bindings(snap))
    assert sum(want.values()) == 152  # WI-057 (2026-09-13): feat/demo-maturation's WI-050 operating_heat (+1 calc, +3 outputs, +2 bound attributes)
    as_consumer, as_producer = Counter(), Counter()
    for calc in calcs(snap):
        me = calc["node_id"]
        dump = panels[me]
        for row in dump["inputs"]:
            if row["kind"] == "producer":
                assert not row["unresolved"]
                as_consumer[(me, row["name"], row["producerNodeId"], row["outputId"])] += 1
        for output in dump["outputs"]:
            for link in output["consumers"]:
                as_producer[(link["nodeId"], link["inputName"], me, output["outputId"])] += 1
    assert as_consumer == want
    assert as_producer == want


def test_output_consumers(panels):
    snap = load_fixture()
    consumers = Counter()
    for consumer, name, producer, output in producer_bindings(snap):
        consumers[(producer, output)] += 1
    rows = 0
    no_consumer = 0
    for calc in calcs(snap):
        dump = panels[calc["node_id"]]
        assert [(o["outputId"], o["name"]) for o in dump["outputs"]] == [
            (o["port"]["output"], o["name"]) for o in calc["outputs"]
        ]
        for output in dump["outputs"]:
            rows += 1
            assert not output["undeclared"]
            expected = consumers[(calc["node_id"], output["outputId"])]
            assert len(output["consumers"]) == expected
            assert output["noConsumer"] is (expected == 0)
            no_consumer += expected == 0
    assert rows == 158  # WI-057 (2026-09-13): feat/demo-maturation's WI-050 operating_heat (+1 calc, +3 outputs, +2 bound attributes)
    assert no_consumer == 66  # WI-057 (2026-09-13): feat/demo-maturation's WI-050 operating_heat adds two outputs nothing reads


def test_location_and_hash(panels):
    snap = load_fixture()
    hashes = {f["referent"]: f["sha256"] for f in snap["sources"]["files"]}
    for calc in calcs(snap):
        location = panels[calc["node_id"]]["location"]
        assert location["text"] == f"{calc['source_file']}:{calc['source_line']}"
        full = hashes[calc["source_file"]]
        assert full[:12] in location["hash"]
        assert location["hashTitle"] == full


def test_unrenderable_tree_synthetic(viewer_page, tmp_path):
    snap, node_id = unrenderable_tree(load_fixture())
    path = write(snap, tmp_path / "unrenderable.json")
    assert load_snapshot(viewer_page, path) == "ready"
    show_calc(viewer_page, node_id)
    dump = panel_dump(viewer_page)
    calc = next(c for c in calcs(snap) if c["node_id"] == node_id)
    assert dump["nodeId"] == node_id
    assert DERIVED_LABEL in dump["sectionText"]["formula"]
    assert "No formula available" in dump["sectionText"]["formula"]
    assert dump["derived"] is None
    assert dump["location"]["text"] == f"{calc['source_file']}:{calc['source_line']}"
    assert [r["name"] for r in dump["inputs"]] == [i["name"] for i in calc["inputs"]]
    assert [o["outputId"] for o in dump["outputs"]] == [
        o["port"]["output"] for o in calc["outputs"]
    ]


def test_doc_repeat_note_on_last_entry_only(viewer_page, tmp_path):
    """D7: an earlier entry that happens to end with the doc comment gets no repeat note."""
    snap, node_id = earlier_entry_ends_with_doc(load_fixture())
    calc = next(c for c in calcs(snap) if c["node_id"] == node_id)
    assert calc["calc_expressions"][0].endswith(calc["doc_comment"])
    assert calc["calc_expressions"][-1].endswith(calc["doc_comment"])
    path = write(snap, tmp_path / "early_doc.json")
    assert load_snapshot(viewer_page, path) == "ready"
    show_calc(viewer_page, node_id)
    entries = panel_dump(viewer_page)["formulaEntries"]
    assert [e["text"] for e in entries] == calc["calc_expressions"]
    assert [e["repeat"] for e in entries] == [False] * (len(entries) - 1) + [True]
    assert "No formula lines recorded" not in panel_dump(viewer_page)["sectionText"]["formula"]
