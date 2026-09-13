"""Native parse and explicit attachment check for the revised radius usage."""
import json
from agentic_mbse.sysml.syside_adapter import get_syside
from prepare import HERE, SOURCE, inventory, protected

syside = get_syside()
files = sorted((HERE / "models").rglob("*.sysml"))
model, diagnostics = syside.try_load_model([str(path) for path in files])
errors = {
    name: [str(d) for d in getattr(diagnostics, name) if d.severity == syside.DiagnosticSeverity.Error]
    for name in ("parser", "sema")
}
attached = []
for element in model.elements(syside.AttributeUsage):
    for doc in element.documentation:
        if "[INHERITED: T-021@2f8856b7]" in doc.body:
            attached.append({"name": element.name, "qualified_name": str(element.qualified_name), "doc": doc.body})
report = {"file_count": len(files), "errors": errors, "attached_documentation": attached, "source_hashes": inventory(HERE / "models")}
(HERE / "parse.json").write_text(json.dumps(report, indent=2) + "\n")
assert len(files) == 23
assert not any(errors.values()), errors
assert len(attached) == 1 and attached[0]["name"] == "R0", attached
assert "magnet" in attached[0]["qualified_name"], attached
assert all(field in attached[0]["doc"] for field in ("Source: " + SOURCE, "Ref:", "Basis:", "2f8856b7", "## Assessment"))
before = json.loads((HERE / "protected-before.json").read_text())
after = protected()
assert before == after, "Protected file contents or symlinks changed"
(HERE / "preservation.json").write_text(json.dumps({"protected_entries": len(before), "byte_hashes_and_symlinks_unchanged": True}, indent=2) + "\n")
print("PASS: 23 native files, zero parser/semantic errors, structured doc attached to " + attached[0]["qualified_name"])
print("PASS: original evidence and protected production contents unchanged")
