"""The pin's source: extract it, and check the cited JavaScript in it (I1, I2, M5).

Recording reads only an extract of the pinned commit (`extract`). Before it records, the
cite tables must still match the extract's frontend (`cite_errors`), and every cited
file's blob must equal the previous recording's header (`unverified_js`). Standard
library only.
"""

from __future__ import annotations

import hashlib
import io
import subprocess
import tarfile
from collections.abc import Mapping
from pathlib import Path

from contract_text import parse
from frontend_requests import EXPLORER, JOINED_LISTS, LINKED_LISTS, REQUESTS, STATIC_JS, USAGE_SITES

SERVING_SET = "requirements-serve.txt"  # relative to a repo root
RUNTIME_PATHS = Path(__file__).resolve().parent / "runtime_paths.txt"


def runtime_paths() -> list[str]:
    """The repo directories the explorer server reads at runtime (runtime_paths.txt)."""
    lines = RUNTIME_PATHS.read_text(encoding="utf-8").splitlines()
    return [line for line in lines if line and not line.startswith("#")]


def extract(repo: Path, sha: str, dest: Path) -> list[str]:
    """Write commit `sha`'s runtime paths and serving set into a new directory `dest`.

    Runtime paths the commit doesn't have are skipped; the serving set is required (N2).
    Returns the paths written.
    """
    wanted = [*runtime_paths(), SERVING_SET]
    present = _git(repo, "ls-tree", "--name-only", sha, "--", *wanted).splitlines()
    if SERVING_SET not in present:
        raise RuntimeError(f"{sha} has no {SERVING_SET}, so its serving set is unknown")
    archive = subprocess.run(
        ["git", "-C", str(repo), "archive", "--format=tar", sha, "--", *present],
        check=True,
        capture_output=True,
    ).stdout
    dest.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(dest, filter="data")
    return present


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout


def cites() -> list[str]:
    """Every file.js:N cite in the request, join, link and usage tables, sorted."""
    sites = {site for r in REQUESTS.values() for site in (*r.fetch_sites, *r.derived_by)}
    sites |= {site for table in (JOINED_LISTS, LINKED_LISTS) for s in table.values() for site in s}
    return sorted(sites | set(USAGE_SITES))


def fetch_sites(tree: Path) -> set[str]:
    """Every line of the frontend's JavaScript and templates in `tree` that calls fetch(.

    JavaScript sites are named like the cites, relative to static/js (`index_page.js:247`);
    template sites relative to the explorer (`templates/concept.html.j2:12`).
    """
    explorer, js = tree / EXPLORER, tree / STATIC_JS
    files = [(path, path.relative_to(js).as_posix()) for path in js.rglob("*.js")]
    files += [
        (path, path.relative_to(explorer).as_posix())
        for path in (explorer / "templates").rglob("*")
        if path.is_file()
    ]
    return {
        f"{name}:{number}"
        for path, name in files
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
        if "fetch(" in line
    }


def cite_errors(tree: Path) -> list[str]:
    """Where the cite tables and the frontend in `tree` disagree (I2); empty when they agree."""
    sites = fetch_sites(tree)
    cited = {site for request in REQUESTS.values() for site in request.fetch_sites}
    errors = [f"{site}: calls fetch( but no request cites it" for site in sorted(sites - cited)]
    errors += [
        f"{site}: cited as a fetch( site, but has no fetch(" for site in sorted(cited - sites)
    ]
    for cite in cites():
        name, lines = cite.split(":")
        path = tree / STATIC_JS / name
        if not path.is_file():
            errors.append(f"{cite}: no such file")
        elif int(lines.split("-")[-1]) > len(path.read_text(encoding="utf-8").splitlines()):
            errors.append(f"{cite}: past the end of the file")
    return errors


def js_blobs(tree: Path) -> dict[str, str]:
    """Repo path -> git blob SHA of every cited JavaScript file in `tree` (M5, N6)."""
    names = sorted({cite.split(":")[0] for cite in cites()})
    return {
        (STATIC_JS / name).as_posix(): _blob_sha((tree / STATIC_JS / name).read_bytes())
        for name in names
    }


def _blob_sha(data: bytes) -> str:
    """The SHA git gives `data` as a blob, so it compares with `git rev-parse <pin>:<path>`."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def unverified_js(contract_path: Path, js: Mapping[str, str]) -> list[str]:
    """Why the cited JavaScript isn't known to match the cite tables; empty when it is.

    It is known to match when every blob equals the previous recording's header (M5).
    """
    if not contract_path.exists():
        return [f"no earlier {contract_path.name} to compare the cited JavaScript with"]
    previous = parse(contract_path.read_text(encoding="utf-8")).js
    return [
        f"{path}: blob changed since the last recording"
        for path in sorted(previous.keys() | js.keys())
        if previous.get(path) != js.get(path)
    ]


def require_own_server(tree: Path) -> None:
    """Fail unless the explorer server imports from `tree`, the pin's own code (decision 11)."""
    import exploration.concept_explorer.server as server

    if not Path(server.__file__).resolve().is_relative_to(tree):
        raise RuntimeError(
            f"recording imported {server.__file__}, not the extract's server; run it as python -I"
        )
