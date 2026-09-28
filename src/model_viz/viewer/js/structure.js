// Pure layer: the structure view's part tree, its visible elements and their preset layout.
// No DOM, no Cytoscape (design I8). Output is plain Cytoscape element JSON.
window.ModelViz = window.ModelViz || {};

ModelViz.structure = (function () {
  const { visibleContainers } = ModelViz.view;

  // Layout constants (design § Structure layout). graph.js reads FONT_PX, LINE_H and PARENT_PAD
  // for the part stylesheet, so the packer and the drawn boxes agree.
  const constants = Object.freeze({
    FONT_PX: 12,
    LINE_H: 16,
    CHAR_W: 7.2,
    LINES: 2,
    PAD: 8,
    MIN_W: 60,
    PARENT_PAD: 12,
    LABEL_BAND: 36,
    GAP: 20,
    ROW_WIDTH: 5,
  });
  const { CHAR_W, LINE_H, LINES, PAD, MIN_W, PARENT_PAD, LABEL_BAND, GAP, ROW_WIDTH } = constants;

  function segmentText(occ) {
    return occ.segment === null ? "segment not recorded" : occ.segment;
  }

  function requireOccurrence(model, occurrenceId) {
    const occ = model.occurrences.get(occurrenceId);
    if (occ === undefined) throw new Error(`No occurrence ${occurrenceId} in the model.`);
    return occ;
  }

  // The containment path from the root, segments joined by "/" (stellaris/magnet/coil).
  function partPath(model, occurrenceId) {
    const segments = [];
    for (let occ = requireOccurrence(model, occurrenceId); occ !== undefined; occ = model.occurrences.get(occ.parentId)) {
      segments.push(segmentText(occ));
    }
    return segments.reverse().join("/");
  }

  // The owner name of a part's own usage, package_display::display_segment, or null without a package (D23).
  function usageOwner(occ) {
    return occ.packageDisplay === null ? null : `${occ.packageDisplay}::${segmentText(occ)}`;
  }

  // Part = { id, parent, occurrenceId, segment, label, path, depth, childCount, memberCount, calcCount }
  // Tree = { mode: "structure", containers: Map<pid, Part> (parents first), containerOf, idByOccurrence }
  function structuralTree(model) {
    const idByOccurrence = new Map();
    let n = 0;
    for (const occurrenceId of model.occurrences.keys()) idByOccurrence.set(occurrenceId, "p" + n++);

    const ordered = [...model.occurrences.values()].sort((a, b) => a.depth - b.depth);
    const containers = new Map();
    for (const o of ordered) {
      const isRoot = o.parentId === null;
      containers.set(idByOccurrence.get(o.occurrenceId), {
        id: idByOccurrence.get(o.occurrenceId),
        parent: isRoot ? null : idByOccurrence.get(o.parentId),
        occurrenceId: o.occurrenceId,
        segment: segmentText(o),
        label: isRoot && o.packageDisplay !== null ? usageOwner(o) : segmentText(o),
        path: partPath(model, o.occurrenceId),
        depth: o.depth,
        childCount: o.childIds.length,
        memberCount: 0,
        calcCount: o.calcKeys.length,
      });
    }
    // Deepest first, so each part's descendants are counted before its parent adds them up.
    for (const part of [...containers.values()].reverse()) {
      if (part.parent !== null) containers.get(part.parent).memberCount += part.memberCount + 1;
    }
    return { mode: "structure", containers, containerOf: new Map(), idByOccurrence };
  }

  // Parts that can be collapsed: every part with children.
  function collapsibleParts(tree) {
    return new Set([...tree.containers.values()].filter((part) => part.childCount > 0).map((part) => part.id));
  }

  // The start state on load (D16): every part with children below the root is collapsed.
  function startCollapsed(tree) {
    return new Set([...collapsibleParts(tree)].filter((id) => tree.containers.get(id).depth > 0));
  }

  function plural(count, one, many) {
    return count === 1 ? `1 ${one}` : `${count} ${many}`;
  }

  // Two lines (D15): the name, with the hidden part count when collapsed, then the direct calc count.
  function partLabel(part, isCollapsed) {
    const name = isCollapsed ? `${part.label} (${plural(part.memberCount, "part", "parts")})` : part.label;
    return `${name}\n${plural(part.calcCount, "calc", "calcs")}`;
  }

  function longestLineChars(label) {
    return Math.max(...label.split("\n").map((line) => line.length));
  }

  // A box node's size from its label (design § Structure layout).
  function boxSize(label) {
    const lines = label.split("\n").length;
    if (lines !== LINES) throw new Error(`A part box label has ${LINES} lines; this one has ${lines}.`);
    return { width: Math.max(MIN_W, longestLineChars(label) * CHAR_W + 2 * PAD), height: LINES * LINE_H + 2 * PAD };
  }

  // Part nodes for the visible parts, with box sizes and preset positions on the box nodes (D15, D26).
  function structureElements(tree, collapsed) {
    for (const id of collapsed) {
      const part = tree.containers.get(id);
      if (part === undefined) throw new Error(`No part ${id} in the structure tree.`);
      if (part.childCount === 0) throw new Error(`Part ${id} has no children, so it cannot be collapsed.`);
    }
    const elements = [];
    const sizes = new Map();
    for (const part of visibleContainers(tree, collapsed)) {
      const isCollapsed = collapsed.has(part.id);
      const label = partLabel(part, isCollapsed);
      const data = {
        id: part.id,
        kind: "part",
        occurrence_id: part.occurrenceId,
        label,
        path: part.path,
        depth: part.depth,
        calc_count: part.calcCount,
        child_count: part.childCount,
        member_count: part.memberCount,
        collapsed: isCollapsed,
      };
      if (part.parent !== null) data.parent = part.parent;
      if (part.childCount === 0 || isCollapsed) {
        const size = boxSize(label);
        data.width = size.width;
        data.height = size.height;
        sizes.set(part.id, size);
      }
      elements.push({ group: "nodes", data, selectable: false });
    }
    const { positions } = structureLayout(elements, sizes);
    for (const element of elements) {
      if (sizes.has(element.data.id)) element.position = positions[element.data.id];
    }
    return elements;
  }

  // Blocks left to right in the given order, a new row after ROW_WIDTH blocks; blocks GAP apart and
  // top-aligned, rows GAP apart. Returns each block's top-left offset and the packed extent.
  function packRows(blocks) {
    const offsets = [];
    let width = 0;
    let top = 0;
    for (let start = 0; start < blocks.length; start += ROW_WIDTH) {
      const row = blocks.slice(start, start + ROW_WIDTH);
      let left = 0;
      for (const block of row) {
        offsets.push({ x: left, y: top });
        left += block.width + GAP;
      }
      width = Math.max(width, left - GAP);
      top += Math.max(...row.map((block) => block.height)) + GAP;
    }
    return { offsets, width, height: blocks.length === 0 ? 0 : top - GAP };
  }

  // Preset positions for part nodes (D26). elements: part nodes, parents before children, in the
  // order siblings should pack. sizes: Map<id, {width, height}> for every box node; every other
  // node must have children. Returns positions (box node centres) and parents (compound box centre
  // and size, as the packer expects Cytoscape to draw it).
  function structureLayout(elements, sizes) {
    const byId = new Map();
    const childrenOf = new Map();
    const roots = [];
    for (const element of elements) {
      byId.set(element.data.id, element);
      childrenOf.set(element.data.id, []);
    }
    for (const element of elements) {
      const parent = element.data.parent;
      if (parent === undefined) roots.push(element.data.id);
      else if (!childrenOf.has(parent)) throw new Error(`Part ${element.data.id} names a parent that is not drawn: ${parent}.`);
      else childrenOf.get(parent).push(element.data.id);
    }

    // Bottom-up: each drawn part's allocated block, and for a compound its packed children.
    const blocks = new Map();
    function measure(id) {
      const kids = childrenOf.get(id);
      if (sizes.has(id)) {
        if (kids.length > 0) throw new Error(`Part ${id} has a box size and drawn children.`);
        blocks.set(id, { ...sizes.get(id) });
        return blocks.get(id);
      }
      if (kids.length === 0) throw new Error(`Part ${id} has no box size and no drawn children.`);
      const packed = packRows(kids.map(measure));
      const boxWidth = packed.width + 2 * PARENT_PAD;
      const boxHeight = packed.height + 2 * PARENT_PAD;
      // PD2: Cytoscape draws a compound's label above its box without widening the box.
      const width = Math.max(boxWidth, longestLineChars(byId.get(id).data.label) * CHAR_W);
      blocks.set(id, { width, height: LABEL_BAND + boxHeight, boxWidth, boxHeight, packed });
      return blocks.get(id);
    }

    // Top-down: place each block by its top-left corner.
    const positions = {};
    const parents = {};
    function place(id, left, top) {
      const block = blocks.get(id);
      if (block.packed === undefined) {
        positions[id] = { x: left + block.width / 2, y: top + block.height / 2 };
        return;
      }
      const boxLeft = left + (block.width - block.boxWidth) / 2;
      const boxTop = top + LABEL_BAND;
      parents[id] = { x: boxLeft + block.boxWidth / 2, y: boxTop + block.boxHeight / 2, width: block.boxWidth, height: block.boxHeight };
      childrenOf.get(id).forEach((childId, i) => {
        const offset = block.packed.offsets[i];
        place(childId, boxLeft + PARENT_PAD + offset.x, boxTop + PARENT_PAD + offset.y);
      });
    }

    const top = packRows(roots.map(measure));
    roots.forEach((id, i) => place(id, top.offsets[i].x, top.offsets[i].y));
    return { positions, parents };
  }

  // --- Part panel (D20, D23) ------------------------------------------------------------------

  // D23: a type name only when the closure is exactly one id and, after dropping the part's own usage
  // owner, the attributes have exactly one declaring owner. Otherwise null with the reason.
  function typeName(model, occurrenceId) {
    const occ = requireOccurrence(model, occurrenceId);
    if (occ.typeIds === null || occ.typeIds.length === 0) return { name: null, reason: "no type ids recorded" };
    if (occ.typeIds.length > 1) {
      return { name: null, reason: `the snapshot lists ${occ.typeIds.length} type ids and does not record which is the part's own type` };
    }
    const attrs = occ.attrIds.map((id) => model.attrs.get(id));
    if (attrs.some((attr) => attr.owner === null)) return { name: null, reason: "an attribute has no declaring owner recorded" };
    const usage = usageOwner(occ);
    const owners = [...new Set(attrs.map((attr) => attr.owner))].filter((owner) => owner !== usage);
    if (owners.length === 0) return { name: null, reason: "no attribute declared by a definition names the type" };
    if (owners.length > 1) return { name: null, reason: `attributes come from ${owners.length} declaring owners` };
    return { name: owners[0] };
  }

  // Where an alias's value comes from. Binding = {kind: "calc", calcKey, calcName, outputId, outputName|null}
  // | {kind: "attr", occurrenceId, attrNodeId, partPath, attrName|null} | {kind: "unresolved", reason, raw|null}.
  function resolveAlias(model, alias) {
    if (alias.kind === "producer") {
      const key = model.keyByNodeId.get(alias.calcNodeId);
      if (key === undefined) {
        return { kind: "unresolved", reason: "the bound calc is not in this snapshot", raw: `${alias.calcNodeId} output ${alias.outputId}` };
      }
      const calc = model.byKey.get(key);
      const output = calc.outputs.find((o) => o.outputId === alias.outputId);
      return { kind: "calc", calcKey: key, calcName: calc.name, outputId: alias.outputId, outputName: output === undefined ? null : output.name };
    }
    if (alias.kind === "node") {
      const target = model.attrs.get(alias.attrNodeId);
      if (target === undefined) return { kind: "unresolved", reason: "the bound attribute is not in this snapshot", raw: alias.attrNodeId };
      if (!model.occurrences.has(target.occurrenceId)) {
        return { kind: "unresolved", reason: "the bound attribute belongs to no part in this snapshot", raw: alias.attrNodeId };
      }
      return { kind: "attr", occurrenceId: target.occurrenceId, attrNodeId: target.nodeId, partPath: partPath(model, target.occurrenceId), attrName: target.name };
    }
    if (alias.kind === "unknown") {
      return { kind: "unresolved", reason: "bound, but the target is not recorded", raw: alias.raw === null ? null : JSON.stringify(alias.raw) };
    }
    throw new Error(`structure: alias kind ${alias.kind} has no resolver`);
  }

  const KIND_BY_BINDING = { calc: "calc-bound", attr: "attr-bound", unresolved: "unresolved" };

  // One attribute row with its value kind decided in D20's order: recorded, then binding, then no value.
  // Row = {nodeId, name|null, owner|null, sourceFile|null, sourceLine|null, kind, value, binding|null}
  function attributeRow(model, attr) {
    const binding = attr.alias === null ? null : resolveAlias(model, attr.alias);
    let kind;
    if (attr.hasValue) kind = "recorded";
    else if (binding === null) kind = "none";
    else kind = KIND_BY_BINDING[binding.kind];
    return { nodeId: attr.nodeId, name: attr.name, owner: attr.owner, sourceFile: attr.sourceFile, sourceLine: attr.sourceLine, kind, value: attr.value, binding };
  }

  // Rows grouped by declaring owner, owners in first-appearance order, rows in snapshot order.
  function ownerGroups(model, occ) {
    const usage = usageOwner(occ);
    const groups = new Map();
    for (const id of occ.attrIds) {
      const row = attributeRow(model, model.attrs.get(id));
      if (!groups.has(row.owner)) groups.set(row.owner, { owner: row.owner, ownPart: row.owner !== null && row.owner === usage, rows: [] });
      groups.get(row.owner).rows.push(row);
    }
    return [...groups.values()];
  }

  // Everything the part panel shows for one occurrence, every value kind already decided (D20).
  function partDetail(model, occurrenceId) {
    const occ = requireOccurrence(model, occurrenceId);
    return {
      occurrenceId,
      name: segmentText(occ),
      path: partPath(model, occurrenceId),
      type: typeName(model, occurrenceId),
      childCount: occ.childIds.length,
      calcs: occ.calcKeys.map((key) => ({ key, name: model.byKey.get(key).name })),
      attrCount: occ.attrIds.length,
      ownerGroups: ownerGroups(model, occ),
    };
  }

  // D22: exact path, else exact segment, else path substring; case-insensitive; tree order.
  function matchParts(tree, query) {
    const q = query.toLowerCase();
    const parts = [...tree.containers.values()];
    const exactPath = parts.filter((part) => part.path.toLowerCase() === q);
    if (exactPath.length > 0) return exactPath;
    const exactSegment = parts.filter((part) => part.segment.toLowerCase() === q);
    if (exactSegment.length > 0) return exactSegment;
    return parts.filter((part) => part.path.toLowerCase().includes(q));
  }

  return {
    constants,
    structuralTree,
    collapsibleParts,
    startCollapsed,
    boxSize,
    plural,
    structureElements,
    structureLayout,
    partPath,
    typeName,
    partDetail,
    matchParts,
  };
})();
