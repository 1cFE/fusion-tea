"""Export one or more codegen snapshots as a single self-contained viewer HTML file.

    uv run python src/model_viz/export.py <snapshot.json> -o <out.html>
    uv run python src/model_viz/export.py --viewer v2 <snapshot.json> -o <out.html>
    uv run python src/model_viz/export.py <a.snapshot.json> <b.snapshot.json> -o <out.html>

The viewer's stylesheet, scripts and vendored libraries are inlined verbatim, each snapshot is
embedded as a JSON script element, and a small loader script loads one on open. With several
snapshots the toolbar gains a Model select that switches between them. The file needs no server
and no network. Stdlib only; src/model_viz/ is not a package (model-viz design D12).
"""

import argparse
import datetime
import html
import json
import re
import sys
from pathlib import Path

VIEWER_DIRS = {
    "v1": Path(__file__).resolve().parent / "viewer",
    "v2": Path(__file__).resolve().parent / "viewer2",
}
VIEWER_DIR = VIEWER_DIRS["v1"]
SNAPSHOT_ELEMENT_ID = "model-viz-snapshot"
STYLESHEET_LINK = re.compile(r'<link rel="stylesheet" href="([^"]+)">')
SCRIPT_TAG = re.compile(r'<script src="([^"]+)"></script>')
TITLE_TAG = re.compile(r"<title>[^<]*</title>")
BODY_END = "</body>"

LOADER = """(function () {
  const text = document.getElementById(%(element_id)s).textContent;
  window.modelVizApp.loadText(text);
  document.title = %(title)s;
  const note = document.createElement("span");
  note.className = "search-status";
  note.dataset.role = "export-note";
  note.textContent = %(note)s;
  document.querySelector(".toolbar").appendChild(note);
})();"""

MULTI_LOADER = """(function () {
  const entries = %(entries)s;
  const select = document.createElement("select");
  select.dataset.role = "snapshot-select";
  entries.forEach(function (entry, index) {
    const option = document.createElement("option");
    option.value = String(index);
    option.textContent = entry.name;
    select.appendChild(option);
  });
  const label = document.createElement("label");
  label.appendChild(document.createTextNode("Model "));
  label.appendChild(select);
  const picker = document.querySelector(".toolbar .file-pick");
  picker.parentNode.insertBefore(label, picker.nextSibling);
  const note = document.createElement("span");
  note.className = "search-status";
  note.dataset.role = "export-note";
  document.querySelector(".toolbar").appendChild(note);
  function show(index) {
    const entry = entries[index];
    window.modelVizApp.loadText(document.getElementById(entry.id).textContent);
    document.title = entry.name;
    note.textContent = entry.note;
  }
  select.addEventListener("change", function () { show(Number(select.value)); });
  show(0);
})();"""


class ExportRefused(Exception):
    """The input cannot possibly load in the viewer; nothing was written."""


def read_snapshot(path: Path) -> tuple[str, str]:
    """The snapshot's text and instance_graph.fingerprint; refuses a file that is not a snapshot."""
    try:
        text = path.read_bytes().decode("utf-8")
        snap = json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExportRefused(f"{path}: not a JSON file ({exc})") from exc
    if not isinstance(snap, dict) or "format" not in snap or "instance_graph" not in snap:
        raise ExportRefused(f"{path}: not a codegen snapshot (missing format or instance_graph)")
    graph = snap["instance_graph"]
    if not isinstance(graph, dict) or not isinstance(graph.get("fingerprint"), str):
        raise ExportRefused(f"{path}: not a codegen snapshot (no instance_graph.fingerprint)")
    return text, graph["fingerprint"]


def model_name(path: Path) -> str:
    """The file stem without the .snapshot marker: stellarator.snapshot.json -> stellarator."""
    name = path.name.removesuffix(".json")
    return name.removesuffix(".snapshot")


def escape_script_close(text: str) -> str:
    """Escape every "</script" so inlined JavaScript cannot end its own script element."""
    return re.sub(r"</(script)", r"<\\/\1", text, flags=re.IGNORECASE)


def script_literal(value) -> str:
    """A JavaScript literal for a JSON-serialisable value, safe inside an inline script."""
    return json.dumps(value).replace("</", "<\\/")


def replace_exactly_once(pattern: re.Pattern, page: str, replacement) -> str:
    result, count = pattern.subn(replacement, page)
    if count != 1:
        raise RuntimeError(
            f"viewer index.html: expected one match of {pattern.pattern}, found {count}"
        )
    return result


def inline_viewer(viewer_dir: Path) -> str:
    """index.html with its stylesheet and every script inlined verbatim."""
    page = (viewer_dir / "index.html").read_text(encoding="utf-8")

    def inline_style(match: re.Match) -> str:
        css = (viewer_dir / match.group(1)).read_text(encoding="utf-8")
        return "<style>\n" + re.sub(r"</(style)", r"<\\/\1", css, flags=re.IGNORECASE) + "</style>"

    def inline_script(match: re.Match) -> str:
        js = (viewer_dir / match.group(1)).read_text(encoding="utf-8")
        return "<script>\n" + escape_script_close(js) + "\n</script>"

    page = replace_exactly_once(STYLESHEET_LINK, page, inline_style)
    page, scripts = SCRIPT_TAG.subn(inline_script, page)
    if scripts == 0:
        raise RuntimeError("viewer index.html: no <script src> tags found to inline")
    return page


def build_loader(embeds: list[dict]) -> str:
    """The loader script for one embedded snapshot, or for several behind a Model select."""
    if len(embeds) == 1:
        one = embeds[0]
        return LOADER % {
            "element_id": script_literal(one["id"]),
            "title": script_literal(one["name"]),
            "note": script_literal(one["note"]),
        }
    entries = [{"id": e["id"], "name": e["name"], "note": e["note"]} for e in embeds]
    return MULTI_LOADER % {"entries": script_literal(entries)}


def export_page(viewer_page: str, embeds: list[dict]) -> str:
    """The inlined viewer page with every snapshot embedded, the title set and the loader
    appended. Each embed is {id, name, note, text}; the title is the first embed's name."""
    title = embeds[0]["name"]
    page = replace_exactly_once(
        TITLE_TAG, viewer_page, lambda _m: f"<title>{html.escape(title)}</title>"
    )
    tail = (
        "".join(
            f'<script type="application/json" id="{embed["id"]}">'
            + embed["text"].replace("</", "<\\/")
            + "</script>\n"
            for embed in embeds
        )
        + "<script>\n"
        + build_loader(embeds)
        + "\n</script>\n"
        + BODY_END
    )
    if page.count(BODY_END) != 1:
        raise RuntimeError("viewer index.html: expected one </body>")
    return page.replace(BODY_END, tail)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "snapshot", type=Path, nargs="+", help="one or more codegen .snapshot.json files"
    )
    parser.add_argument("-o", "--output", type=Path, required=True, help="HTML file to write")
    parser.add_argument(
        "--viewer",
        choices=sorted(VIEWER_DIRS),
        default="v1",
        help="which viewer page to inline (default: v1)",
    )
    args = parser.parse_args(argv)

    today = datetime.date.today().isoformat()
    embeds: list[dict] = []
    for index, path in enumerate(args.snapshot):
        try:
            text, fingerprint = read_snapshot(path)
        except ExportRefused as exc:
            print(f"export refused: {exc}", file=sys.stderr)
            return 1
        element_id = (
            SNAPSHOT_ELEMENT_ID if len(args.snapshot) == 1 else f"{SNAPSHOT_ELEMENT_ID}-{index}"
        )
        note = f"exported from {path.name} on {today} · fingerprint {fingerprint[:12]}"
        embeds.append({"id": element_id, "name": model_name(path), "note": note, "text": text})

    page = export_page(inline_viewer(VIEWER_DIRS[args.viewer]), embeds)
    args.output.write_text(page, encoding="utf-8")
    print(f"wrote {args.output} ({len(page.encode('utf-8')):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
