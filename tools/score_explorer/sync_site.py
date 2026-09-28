#!/usr/bin/env python3
"""Copy Score Explorer runtime files to the existing GitHub Pages directory."""

import argparse
from pathlib import Path
import shutil


RUNTIME_PATHS = ("index.html", "run-locally.html", "THIRD_PARTY_NOTICES.md", "data", "vendor")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report differences without writing files")
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    target = source.parents[1] / "docs"
    differences = []
    for item in RUNTIME_PATHS:
        path = source / item
        files = sorted(p for p in path.rglob("*") if p.is_file()) if path.is_dir() else [path]
        for file in files:
            relative = file.relative_to(source)
            destination = target / relative
            if args.check:
                if not destination.is_file() or file.read_bytes() != destination.read_bytes():
                    differences.append(str(relative))
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(file, destination)
        if path.is_dir() and args.check and (target / item).is_dir():
            expected = {file.relative_to(source) for file in files}
            differences.extend(str(file.relative_to(target)) for file in (target / item).rglob("*")
                               if file.is_file() and file.relative_to(target) not in expected)
    if differences:
        parser.exit(1, "Pages copy differs: " + ", ".join(differences) + "\n")
    print("Pages copy matches Score Explorer." if args.check else "Copied Score Explorer runtime files to docs/.")


if __name__ == "__main__":
    main()
