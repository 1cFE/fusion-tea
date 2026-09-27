// Pure layer: the overlay tree (the part tree holding the calc graph), ranks, labels and tags, and
// the visible elements of a collapse state. No DOM, no Cytoscape (design I8, I30).
//
// Owner ruling 2026-09-15: the picture is laid out by dagre, so nothing here carries geometry any
// more. The elements this file returns are plain Cytoscape element JSON with no positions and no
// sizes; graph2.js sizes each box from its label and dagre places it.
window.ModelViz = window.ModelViz || {};

ModelViz.overlay = (function () {
  const { structuralTree, plural } = ModelViz.structure;
  const { visibleElements, containerChain } = ModelViz.view;

  const UNSCOPED_ID = "p-unscoped";

  // Longest chain of calcs feeding each calc, over resolved producer bindings (R6).
  function calcRanks(model) {
    const producers = new Map(model.calcs.map((calc) => [calc.key, new Set()]));
    for (const binding of model.bindings) if (binding.resolved) producers.get(binding.consumer).add(binding.producer);
    const rank = new Map();
    const onPath = new Set();
    function rankOf(key) {
      if (rank.has(key)) return rank.get(key);
      if (onPath.has(key)) throw new Error(`Producer bindings form a cycle through calc ${key}.`);
      onPath.add(key);
      let r = 0;
      for (const producer of producers.get(key)) r = Math.max(r, rankOf(producer) + 1);
      onPath.delete(key);
      rank.set(key, r);
      return r;
    }
    for (const calc of model.calcs) rankOf(calc.key);
    return rank;
  }

  // D31: the last segment of v1's group label, without the leading `_`-word more than half the
  // labels share; a shortened tag that collides with another group's keeps v1's full label (A4c).
  function groupTags(model) {
    const groups = [...model.groups.values()];
    const last = new Map(groups.map((g) => [g.gid, g.label.split("/").pop()]));
    const words = new Map();
    for (const tag of last.values()) {
      if (!tag.includes("_")) continue;
      const word = tag.split("_")[0];
      words.set(word, (words.get(word) || 0) + 1);
    }
    const common = [...words.entries()].find(([, n]) => n * 2 > groups.length);
    const shortened = new Map();
    for (const [gid, tag] of last) {
      const drop = common !== undefined && tag.includes("_") && tag.split("_")[0] === common[0];
      shortened.set(gid, drop ? tag.slice(common[0].length + 1) : tag);
    }
    const uses = new Map();
    for (const tag of shortened.values()) uses.set(tag, (uses.get(tag) || 0) + 1);
    return new Map(groups.map((g) => [g.gid, uses.get(shortened.get(g.gid)) === 1 ? shortened.get(g.gid) : g.label]));
  }

  // D31: a pale fill per group, by the group's index among all groups.
  function groupFills(model) {
    const gids = [...model.groups.keys()];
    return new Map(gids.map((gid, i) => [gid, `hsl(${Math.round((i * 360) / gids.length)}, 55%, 94%)`]));
  }

  // Tree = structuralTree's containers (plus p-unscoped when needed) with containerOf filled, and:
  // childrenOf (siblings by flowRank), calcsOf (snapshot order), rank, flowRank, collapsible, tags, fills.
  function overlayTree(model) {
    const base = structuralTree(model);
    const containers = new Map();
    for (const [id, part] of base.containers) containers.set(id, { ...part });
    const containerOf = new Map();
    const calcsOf = new Map([...containers.keys()].map((id) => [id, []]));
    for (const calc of model.calcs) {
      const id = base.idByOccurrence.get(calc.occurrenceId);
      if (id !== undefined) {
        containerOf.set(calc.key, id);
        calcsOf.get(id).push(calc.key);
        continue;
      }
      if (!containers.has(UNSCOPED_ID)) {
        containers.set(UNSCOPED_ID, { id: UNSCOPED_ID, parent: null, occurrenceId: null, segment: "unscoped", label: "unscoped", path: "unscoped", depth: 0, childCount: 0, memberCount: 0, calcCount: 0 });
        calcsOf.set(UNSCOPED_ID, []);
      }
      containers.get(UNSCOPED_ID).calcCount += 1;
      containerOf.set(calc.key, UNSCOPED_ID);
      calcsOf.get(UNSCOPED_ID).push(calc.key);
    }
    const rank = calcRanks(model);
    const snapshotOrder = new Map([...model.occurrences.keys()].map((occ, i) => [base.idByOccurrence.get(occ), i]));
    snapshotOrder.set(UNSCOPED_ID, snapshotOrder.size);

    const childrenOf = new Map([...containers.keys()].map((id) => [id, []]));
    for (const part of containers.values()) if (part.parent !== null) childrenOf.get(part.parent).push(part.id);
    const subtreeCalcs = new Map();
    function collect(id) {
      const keys = [...calcsOf.get(id)];
      for (const kid of childrenOf.get(id)) keys.push(...collect(kid));
      subtreeCalcs.set(id, keys);
      return keys;
    }
    const rootIds = [...containers.values()].filter((p) => p.parent === null).map((p) => p.id);
    rootIds.forEach(collect);
    const flowRank = new Map();
    for (const [id, keys] of subtreeCalcs) flowRank.set(id, keys.length === 0 ? null : keys.reduce((s, k) => s + rank.get(k), 0) / keys.length);
    const bySnapshot = (a, b) => snapshotOrder.get(a) - snapshotOrder.get(b);
    const byFlow = (a, b) => {
      const fa = flowRank.get(a);
      const fb = flowRank.get(b);
      if (fa === null || fb === null) return (fa === null) - (fb === null) || bySnapshot(a, b);
      return fa - fb || bySnapshot(a, b);
    };
    for (const kids of childrenOf.values()) kids.sort(byFlow);
    rootIds.sort(byFlow);

    for (const part of containers.values()) part.calcKeys = calcsOf.get(part.id);
    const collapsible = new Set([...containers.values()].filter((p) => p.childCount > 0 || p.calcCount > 0).map((p) => p.id));
    return {
      mode: "structure",
      containers,
      containerOf,
      idByOccurrence: base.idByOccurrence,
      childrenOf,
      calcsOf,
      rootIds,
      rank,
      flowRank,
      collapsible,
      tags: groupTags(model),
      fills: groupFills(model),
    };
  }

  // D29: Collapse all closes every collapsible part below a root; roots and p-unscoped stay open.
  function collapseAllSet(tree) {
    return new Set([...tree.collapsible].filter((id) => tree.containers.get(id).depth > 0));
  }

  function calcLabel(model, tree, key) {
    const calc = model.byKey.get(key);
    return `${calc.name}\n${tree.tags.get(calc.sourceGroup)}`;
  }

  // D30: one line, name and direct calc count.
  function openPartLabel(part) {
    return `${part.label} · ${plural(part.calcCount, "calc", "calcs")}`;
  }

  // D30: the hidden part count (every descendant, PD8) only when it is not zero, then the direct count.
  function closedPartLabel(part) {
    const hidden = part.memberCount === 0 ? "" : ` (${plural(part.memberCount, "part", "parts")})`;
    return `${part.label}${hidden}\n${plural(part.calcCount, "calc", "calcs")}`;
  }

  function leafPartLabel(part) {
    return `${part.label}\n0 calcs`;
  }

  // Each calc to itself, or to the id of the outermost closed part on its container chain.
  // The one representative rule for the element path and the class path (D29).
  function representatives(model, tree, collapsed) {
    const repOf = new Map();
    for (const calc of model.calcs) {
      let rep = null;
      for (const id of containerChain(tree, calc.key)) if (collapsed.has(id)) rep = id;
      repOf.set(calc.key, rep === null ? calc.key : rep);
    }
    return repOf;
  }

  // The visible elements of a collapse state (D29). Parents come before children; no element
  // carries a position or a size, because dagre computes both.
  function overlayElements(model, tree, collapsed) {
    for (const id of collapsed) {
      if (!tree.collapsible.has(id)) throw new Error(`Part ${id} is not collapsible in the overlay tree.`);
    }
    const elements = visibleElements(model, tree, collapsed).map((element) => {
      const data = element.data;
      if (data.kind === "container") return partElement(tree, tree.containers.get(data.id), collapsed.has(data.id));
      if (data.kind === "calc") return calcElement(model, tree, element);
      return element;
    });
    return { elements, repOf: representatives(model, tree, collapsed) };
  }

  function partElement(tree, part, isClosed) {
    const data = {
      id: part.id,
      kind: "part",
      occurrence_id: part.occurrenceId,
      path: part.path,
      depth: part.depth,
      calc_count: part.calcCount,
      child_count: part.childCount,
      member_count: part.memberCount,
      collapsed: isClosed,
    };
    if (part.parent !== null) data.parent = part.parent;
    if (!tree.collapsible.has(part.id)) Object.assign(data, { label: leafPartLabel(part), leaf: true });
    else if (isClosed) data.label = closedPartLabel(part);
    else data.label = openPartLabel(part);
    return { group: "nodes", data, selectable: false };
  }

  function calcElement(model, tree, element) {
    const key = element.data.id;
    const calc = model.byKey.get(key);
    const data = {
      ...element.data,
      label: calcLabel(model, tree, key),
      tag: tree.tags.get(calc.sourceGroup),
      fill: tree.fills.get(calc.sourceGroup),
      source_file: calc.sourceFile,
      rank: tree.rank.get(key),
    };
    return { group: "nodes", data, selectable: false };
  }

  // D39 (R14): the first non-empty step of exact part path, exact part segment, exact calc name,
  // then substring over part paths and calc names; case-insensitive. Returns {parts, calcs} of tree
  // containers and model calcs, both empty when nothing matches.
  function find(model, tree, query) {
    const q = query.trim().toLowerCase();
    const parts = [...tree.containers.values()];
    const calcs = model.calcs;
    if (q === "") return { parts: [], calcs: [] };
    const steps = [
      () => ({ parts: parts.filter((p) => p.path.toLowerCase() === q), calcs: [] }),
      () => ({ parts: parts.filter((p) => p.segment.toLowerCase() === q), calcs: [] }),
      () => ({ parts: [], calcs: calcs.filter((c) => c.name.toLowerCase() === q) }),
      () => ({ parts: parts.filter((p) => p.path.toLowerCase().includes(q)), calcs: calcs.filter((c) => c.name.toLowerCase().includes(q)) }),
    ];
    for (const step of steps) {
      const found = step();
      if (found.parts.length + found.calcs.length > 0) return found;
    }
    return { parts: [], calcs: [] };
  }

  return {
    UNSCOPED_ID,
    overlayTree,
    collapseAllSet,
    find,
    calcLabel,
    openPartLabel,
    closedPartLabel,
    leafPartLabel,
    representatives,
    overlayElements,
  };
})();
