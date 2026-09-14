// Pure layer: formula helpers for the detail panel. No DOM, no Cytoscape (design I8).
window.ModelViz = window.ModelViz || {};

ModelViz.formula = (function () {
  const JOINERS = { "+": " + ", "*": " * " };

  function isObject(value) {
    return value !== null && typeof value === "object" && !Array.isArray(value);
  }

  // Print an expression-ir/v1 tree built from +, *, feature references and numeric literals.
  // Returns null for the whole tree when any node is outside that set or malformed.
  function printExpression(node) {
    if (!isObject(node)) return null;
    if (node.kind === "feature_ref") {
      const name = isObject(node.reference) ? node.reference.source_name : undefined;
      return typeof name === "string" && name.length > 0 ? name : null;
    }
    if (node.kind === "literal") {
      const value = isObject(node.literal) ? node.literal.value : undefined;
      return typeof value === "number" && Number.isFinite(value) ? String(value) : null;
    }
    if (node.kind === "operator") {
      const joiner = JOINERS[node.operator];
      if (joiner === undefined || !Array.isArray(node.operands) || node.operands.length < 2) return null;
      const parts = [];
      for (const operand of node.operands) {
        const printed = printExpression(operand);
        if (printed === null) return null;
        const needsParens = node.operator === "*" && operand.kind === "operator" && operand.operator === "+";
        parts.push(needsParens ? `(${printed})` : printed);
      }
      return parts.join(joiner);
    }
    return null;
  }

  // True when a calc_expressions entry repeats a non-empty doc comment at its end
  // (codegen Finding 12 appends the doc comment into the list; design D7).
  function endsWithDoc(entry, doc) {
    return typeof doc === "string" && doc.length > 0 && typeof entry === "string" && entry.endsWith(doc);
  }

  return { printExpression, endsWithDoc };
})();
