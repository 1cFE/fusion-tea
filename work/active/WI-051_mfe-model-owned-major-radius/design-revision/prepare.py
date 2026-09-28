"""Copy the retained family and amend only the binding's documentation."""
import difflib
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = HERE.parent
ROOT = ITEM.parents[2]
SOURCE = "work/analysis/20260911-230953_radius-ownership-evidence/source-meaning.md"
OLD = """            // Major plasma/axis radius [m], owned by the containing plant.
            // Source: models/library/cost_structure/mfe_power_core.sysml; R0.
            // Basis: T-021 source-meaning assessment at 2f8856b7; WI-051.
            :>> R0 = R;"""
NEW = """            :>> R0 = R {
                doc /*
                Major plasma/axis radius [m], owned by the containing plant.

                Source: work/analysis/20260911-230953_radius-ownership-evidence/source-meaning.md
                Ref: ## Model and existing source interpretation; ## Assessment; revision 2f8856b7
                Basis: [INHERITED: T-021@2f8856b7] Existing model-intent interpretation: one shared plasma/axis scale. This does not equate real modular-coil surfaces; coil-bore and coil-centre minor radii remain distinct.
                Last Updated: 2026-09-11
                */
            }"""


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    return {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob("*")) if p.is_file() and not p.is_symlink()}


def protected():
    paths = [p for p in ITEM.rglob("*") if HERE not in p.parents and p != ITEM / "design.md"]
    for location in ("models", "exploration/stellarator_e2e/models", "exploration/stellarator_e2e/generated"):
        paths.extend((ROOT / location).rglob("*"))
    paths.extend(ROOT / "exploration/stellarator_e2e" / name for name in ("run_stellaris.py", "run_stellaris_single.py"))
    return {str(p.relative_to(ROOT)): {"symlink": str(p.readlink())} if p.is_symlink() else {"sha256": sha(p)} for p in sorted(set(paths)) if p.is_file() or p.is_symlink()}


if __name__ == "__main__":
    (HERE / "protected-before.json").write_text(json.dumps(protected(), indent=2) + "\n")
    models = HERE / "models"
    if models.exists():
        raise FileExistsError("Refusing to overwrite revision evidence")
    shutil.copytree(ITEM / "prototype/models", models)
    target = models / "designs/generic_mfe/mfe_plant.sysml"
    original = target.read_text()
    assert original.count(OLD) == 1
    target.write_text(original.replace(OLD, NEW))
    (HERE / "from-prototype.patch").write_text("".join(difflib.unified_diff(original.splitlines(True), target.read_text().splitlines(True), fromfile="a/designs/generic_mfe/mfe_plant.sysml", tofile="b/designs/generic_mfe/mfe_plant.sysml")))
    patches = []
    for path in sorted(models.rglob("*.sysml")):
        relative = path.relative_to(models)
        entering = ITEM / "prototype/entering-models" / relative
        patches.extend(difflib.unified_diff(entering.read_text().splitlines(True), path.read_text().splitlines(True), fromfile="a/" + str(relative), tofile="b/" + str(relative)))
    (HERE / "proposed.patch").write_text("".join(patches))
    old_hashes, new_hashes = inventory(ITEM / "prototype/models"), inventory(models)
    changed = [name for name in old_hashes if old_hashes[name] != new_hashes[name]]
    assert changed == ["designs/generic_mfe/mfe_plant.sysml"]
    retained = subprocess.check_output(["git", "show", "2f8856b7:" + SOURCE], cwd=ROOT)
    assert retained == (ROOT / SOURCE).read_bytes() == (ITEM / "prototype/frozen-source-meaning.md").read_bytes()
    report = {"original_prototype_commit": "66c2b5c09abcaaad99bc9587de7b3d055f454337", "original_source_hashes": old_hashes, "revised_source_hashes": new_hashes, "changed_from_original_prototype": changed, "source_meaning_revision": "2f8856b7", "source_meaning_sha256": hashlib.sha256(retained).hexdigest(), "revised_semantic_fingerprint": None, "revised_executable_fingerprint": None, "package_identity_status": "Not generated for documentation-only revision; fresh generation and re-derived identities required at implementation."}
    (HERE / "source-identity.json").write_text(json.dumps(report, indent=2) + "\n")
    print("Copied 23-file family; changed only attached radius documentation; retained source citation matches 2f8856b7.")
