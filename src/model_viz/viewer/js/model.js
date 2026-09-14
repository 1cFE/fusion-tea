// Pure layer: snapshot text -> checked snapshot -> immutable model.
// No DOM, no Cytoscape (design I8).
window.ModelViz = window.ModelViz || {};

ModelViz.model = (function () {
  const EXPECTED_VERSION = "instance-graph/v3";

  // A snapshot the viewer refuses to show. The message is written for the modeler.
  class SnapshotError extends Error {
    constructor(message) {
      super(message);
      this.name = "SnapshotError";
    }
  }

  function isObject(value) {
    return value !== null && typeof value === "object" && !Array.isArray(value);
  }

  function readSnapshot(text) {
    let snap;
    try {
      snap = JSON.parse(text);
    } catch (err) {
      if (err instanceof SyntaxError) {
        throw new SnapshotError("This is not a JSON file, so it cannot be a codegen snapshot.");
      }
      throw err;
    }
    const graphRoot = isObject(snap) ? snap.instance_graph : undefined;
    const version = isObject(graphRoot) ? graphRoot.schema_version : undefined;
    if (typeof version !== "string") {
      throw new SnapshotError(
        "This JSON file is not a codegen snapshot: it has no instance_graph.schema_version."
      );
    }
    if (version !== EXPECTED_VERSION) {
      throw new SnapshotError(
        `Unsupported snapshot version: expected ${EXPECTED_VERSION}, found ${version}.`
      );
    }
    if (!isObject(graphRoot.graph) || !Array.isArray(graphRoot.graph.calcs)) {
      throw new SnapshotError(`This is a ${EXPECTED_VERSION} snapshot without a calcs list.`);
    }
    return snap;
  }

  function requireString(value, what) {
    if (typeof value !== "string") {
      throw new SnapshotError(`Snapshot field missing or not a string: ${what}.`);
    }
    return value;
  }

  function requireArray(value, what) {
    if (!Array.isArray(value)) {
      throw new SnapshotError(`Snapshot field missing or not a list: ${what}.`);
    }
    return value;
  }

  // Absent means empty; present but not a list is a load error (design Appendix C).
  function optionalArray(value, what) {
    if (value === undefined || value === null) return [];
    return requireArray(value, what);
  }

  function stringOrNull(value) {
    return typeof value === "string" ? value : null;
  }

  function groupKind(path) {
    return path.split("/").includes("designs") ? "design" : "analysis";
  }

  function baseLabel(path) {
    return path.split("/").pop().replace(/\.sysml$/, "");
  }

  // D8: base name without .sysml; when base names collide, prefix the parent directory.
  function labelGroups(paths) {
    const byBase = new Map();
    for (const path of paths) {
      const base = baseLabel(path);
      byBase.set(base, (byBase.get(base) || 0) + 1);
    }
    return paths.map((path) => {
      const base = baseLabel(path);
      if (byBase.get(base) === 1) return base;
      const parts = path.split("/");
      return parts.length > 1 ? `${parts[parts.length - 2]}/${base}` : base;
    });
  }

  function buildGroups(rawCalcs) {
    const paths = [];
    const seen = new Set();
    for (const raw of rawCalcs) {
      const path = stringOrNull(raw.source_file);
      if (path !== null && !seen.has(path)) {
        seen.add(path);
        paths.push(path);
      }
    }
    const labels = labelGroups(paths);
    const groups = new Map();
    const gidByPath = new Map();
    paths.forEach((path, i) => {
      const gid = "g" + i;
      groups.set(gid, { gid, path, label: labels[i], kind: groupKind(path) });
      gidByPath.set(path, gid);
    });
    if (rawCalcs.some((raw) => stringOrNull(raw.source_file) === null)) {
      groups.set("g-ungrouped", { gid: "g-ungrouped", path: null, label: "ungrouped", kind: "ungrouped" });
    }
    return { groups, gidByPath };
  }

  function buildOccurrences(rawOccurrences) {
    const occurrences = new Map();
    rawOccurrences.forEach((raw, i) => {
      if (!isObject(raw)) throw new SnapshotError(`Occurrence ${i} is not a record.`);
      const occurrenceId = requireString(raw.occurrence_id, `occurrences[${i}].occurrence_id`);
      if (raw.parent_id !== null && typeof raw.parent_id !== "string") {
        throw new SnapshotError(`Snapshot field not a string or null: occurrences[${i}].parent_id.`);
      }
      occurrences.set(occurrenceId, {
        occurrenceId,
        parentId: raw.parent_id,
        segment: stringOrNull(raw.display_segment),
      });
    });
    for (const occ of occurrences.values()) {
      const visited = new Set([occ.occurrenceId]);
      for (let parent = occ.parentId; parent !== null; parent = occurrences.get(parent).parentId) {
        if (!occurrences.has(parent)) {
          throw new SnapshotError(`Occurrence ${occ.occurrenceId} names a parent that is not in the snapshot: ${parent}.`);
        }
        if (visited.has(parent)) {
          throw new SnapshotError(`Occurrence ${occ.occurrenceId} is part of a parent cycle.`);
        }
        visited.add(parent);
      }
    }
    return occurrences;
  }

  function buildAttrs(rawAttrs) {
    const attrs = new Map();
    rawAttrs.forEach((raw, i) => {
      if (!isObject(raw)) throw new SnapshotError(`Attribute ${i} is not a record.`);
      const nodeId = requireString(raw.node_id, `attrs[${i}].node_id`);
      attrs.set(nodeId, {
        nodeId,
        name: stringOrNull(raw.display_name),
        hasValue: raw.value !== null && raw.value !== undefined,
        value: raw.value === undefined ? null : raw.value,
      });
    });
    return attrs;
  }

  function buildFileHashes(sources) {
    const hashes = new Map();
    const files = isObject(sources) ? optionalArray(sources.files, "sources.files") : [];
    files.forEach((raw, i) => {
      if (!isObject(raw)) throw new SnapshotError(`sources.files[${i}] is not a record.`);
      if (typeof raw.referent === "string" && typeof raw.sha256 === "string") {
        hashes.set(raw.referent, raw.sha256);
      }
    });
    return hashes;
  }

  function readFormulas(raw, where) {
    const list = optionalArray(raw.calc_expressions, `${where}.calc_expressions`);
    list.forEach((entry, j) => requireString(entry, `${where}.calc_expressions[${j}]`));
    return list.slice();
  }

  function readUnit(metadata) {
    return isObject(metadata) ? stringOrNull(metadata.unit) : null;
  }

  // One input record -> the panel's Input; producer inputs also yield a pending binding.
  function readInput(raw, where) {
    if (!isObject(raw)) throw new SnapshotError(`${where} is not a record.`);
    const name = requireString(raw.name, `${where}.name`);
    const unit = readUnit(raw.metadata);
    const edge = raw.edge;
    if (edge === null || edge === undefined) {
      const hasDefault = isObject(raw.metadata) && raw.metadata.default_value !== null && raw.metadata.default_value !== undefined;
      return { name, kind: "default", hasValue: hasDefault, value: hasDefault ? raw.metadata.default_value : null, unit };
    }
    if (isObject(edge) && edge.kind === "producer") {
      if (!isObject(edge.target)) throw new SnapshotError(`Snapshot field missing: ${where}.edge.target.`);
      return {
        name,
        kind: "producer",
        unit,
        producerNodeId: requireString(edge.target.calculation, `${where}.edge.target.calculation`),
        outputId: requireString(edge.target.output, `${where}.edge.target.output`),
      };
    }
    if (isObject(edge) && edge.kind === "node") {
      return { name, kind: "parameter", unit, attrNodeId: requireString(edge.target, `${where}.edge.target`) };
    }
    if (isObject(edge) && edge.kind === "literal") {
      const hasValue = edge.value !== null && edge.value !== undefined;
      return { name, kind: "literal", unit, hasValue, value: hasValue ? edge.value : null };
    }
    const rawKind = isObject(edge) && typeof edge.kind === "string" ? edge.kind : "(no kind)";
    return { name, kind: "unknown", unit, rawKind };
  }

  function readOutput(raw, where) {
    if (!isObject(raw)) throw new SnapshotError(`${where} is not a record.`);
    const name = requireString(raw.name, `${where}.name`);
    if (!isObject(raw.port)) throw new SnapshotError(`Snapshot field missing: ${where}.port.`);
    return { name, outputId: requireString(raw.port.output, `${where}.port.output`), unit: readUnit(raw.metadata) };
  }

  function buildModel(snap) {
    const graph = snap.instance_graph.graph;
    const rawCalcs = graph.calcs;
    // Every calc entry must be a record before any pass reads its fields (design Appendix C).
    rawCalcs.forEach((raw, i) => {
      if (!isObject(raw)) throw new SnapshotError(`Calc entry ${i} is not an object.`);
    });
    const { groups, gidByPath } = buildGroups(rawCalcs);
    const occurrences = buildOccurrences(optionalArray(graph.occurrences, "graph.occurrences"));
    const attrs = buildAttrs(optionalArray(graph.attrs, "graph.attrs"));
    const fileHashes = buildFileHashes(snap.sources);

    const calcs = [];
    const byKey = new Map();
    const keyByNodeId = new Map();
    rawCalcs.forEach((raw, i) => {
      const where = `calcs[${i}]`;
      const nodeId = requireString(raw.node_id, `${where}.node_id`);
      if (keyByNodeId.has(nodeId)) throw new SnapshotError(`Two calcs share one node_id (${where}).`);
      const key = "c" + i;
      keyByNodeId.set(nodeId, key);
      const sourceFile = stringOrNull(raw.source_file);
      const hasIr = isObject(raw.expression_ir);
      const calc = {
        key,
        nodeId,
        name: requireString(raw.display_name, `${where}.display_name`),
        sourceGroup: sourceFile === null ? "g-ungrouped" : gidByPath.get(sourceFile),
        occurrenceId: isObject(raw.scope) ? stringOrNull(raw.scope.wire) : null,
        sourceFile,
        sourceLine: Number.isInteger(raw.source_line) ? raw.source_line : null,
        formulas: readFormulas(raw, where),
        hasExpressionIr: hasIr,
        derivedFormula: hasIr ? ModelViz.formula.printExpression(raw.expression_ir) : null,
        doc: typeof raw.doc_comment === "string" && raw.doc_comment.length > 0 ? raw.doc_comment : null,
        inputs: requireArray(raw.inputs, `${where}.inputs`).map((inp, j) => readInput(inp, `${where}.inputs[${j}]`)),
        outputs: requireArray(raw.outputs, `${where}.outputs`).map((out, j) => readOutput(out, `${where}.outputs[${j}]`)),
        undeclaredOutputIds: [],
      };
      calcs.push(calc);
      byKey.set(key, calc);
    });

    // Bindings and the reverse index come from one pass over the same records.
    const bindings = [];
    const consumersOf = new Map();
    for (const calc of calcs) {
      for (const input of calc.inputs) {
        if (input.kind !== "producer") continue;
        const producer = keyByNodeId.has(input.producerNodeId) ? keyByNodeId.get(input.producerNodeId) : null;
        const binding = {
          id: "b" + bindings.length,
          consumer: calc.key,
          inputName: input.name,
          producerNodeId: input.producerNodeId,
          producer,
          outputId: input.outputId,
          resolved: producer !== null,
          outputDeclared: producer !== null && byKey.get(producer).outputs.some((o) => o.outputId === input.outputId),
        };
        input.bindingId = binding.id;
        bindings.push(binding);
        if (!binding.resolved) continue;
        const portKey = producer + "|" + input.outputId;
        if (!consumersOf.has(portKey)) consumersOf.set(portKey, []);
        consumersOf.get(portKey).push(binding.id);
        const producerCalc = byKey.get(producer);
        if (!binding.outputDeclared && !producerCalc.undeclaredOutputIds.includes(input.outputId)) {
          producerCalc.undeclaredOutputIds.push(input.outputId);
        }
      }
    }
    const bindingById = new Map(bindings.map((b) => [b.id, b]));

    return { calcs, byKey, keyByNodeId, bindings, bindingById, consumersOf, groups, occurrences, attrs, fileHashes };
  }

  return { SnapshotError, readSnapshot, buildModel };
})();
