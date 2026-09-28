#!/usr/bin/env python3
"""Package a committed static tool with immutable provenance and checksums."""

import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile


NAME = "1cfe-scoring"
REPOSITORY = "https://github.com/1cFE/fusion-tea"
SOURCE_PATH = "tools/score_explorer/"
INCLUDE = ("index.html", "run-locally.html", "README.md", "LICENSING.md", "LICENSES", "THIRD_PARTY_NOTICES.md",
           "package_release.py", "sync_site.py", "build.py", "data", "vendor")


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default="HEAD", help="Committed source ref (default: HEAD)")
    parser.add_argument("--output-dir", type=Path, default=Path("dist"))
    args = parser.parse_args()
    root = Path(git(Path(__file__).resolve().parent, "rev-parse", "--show-toplevel").decode().strip())
    commit = git(root, "rev-parse", "--verify", f"{args.ref}^{{commit}}").decode().strip()
    if args.ref == "HEAD" and git(root, "status", "--porcelain", "--", *(SOURCE_PATH + p for p in INCLUDE)):
        parser.error("Commit changes first, or supply an explicit committed --ref.")
    payload = {}
    for pattern in INCLUDE:
        names = git(root, "ls-tree", "-r", "--name-only", commit, "--", SOURCE_PATH + pattern).decode().splitlines()
        if not names:
            parser.error(f"Missing committed release input: {SOURCE_PATH + pattern}")
        for name in names:
            payload[name[len(SOURCE_PATH):]] = git(root, "show", f"{commit}:{name}")
    for name, data in payload.items():
        if name in ("index.html", "run-locally.html", "THIRD_PARTY_NOTICES.md", "LICENSING.md") or name.startswith(("data/", "vendor/", "LICENSES/")):
            if git(root, "show", f"{commit}:docs/{name}") != data:
                parser.error(f"Committed Pages copy differs: docs/{name}")
    manifest = {
        "artifact": NAME,
        "source_repository": REPOSITORY,
        "source_commit": commit,
        "source_path": SOURCE_PATH.rstrip("/"),
        "source_url": f"{REPOSITORY}/tree/{commit}/{SOURCE_PATH}".rstrip("/"),
        "licenses": dict(code="MIT", data="CC0-1.0", text="CC-BY-4.0"),
        "license_scope": "LICENSING.md",
    }
    payload["release.json"] = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    payload["SHA256SUMS"] = "".join(
        f"{hashlib.sha256(data).hexdigest()}  {name}\n" for name, data in sorted(payload.items())
    ).encode()
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as out:
        for name, data in sorted(payload.items()):
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            out.writestr(entry, data)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    target = args.output_dir / f"{NAME}-{commit[:12]}.zip"
    target.write_bytes(archive.getvalue())
    digest = hashlib.sha256(archive.getvalue()).hexdigest()
    target.with_suffix(".zip.sha256").write_text(f"{digest}  {target.name}\n")
    print(json.dumps({"archive": str(target.resolve()), "sha256": digest, "source_commit": commit}))


if __name__ == "__main__":
    main()
