// Pure layer: what a selection feeds and is fed by, and the class each drawn element takes for it
// (design D37, I28, I32). No DOM, no Cytoscape.
window.ModelViz = window.ModelViz || {};

ModelViz.reach = (function () {
  // A memoised transitive closure over one direction's adjacency; producer bindings are a DAG
  // (overlayTree's ranks reject a cycle), and onPath says so loudly if that ever changes.
  function closure(edges, memo, onPath, key) {
    if (memo.has(key)) return memo.get(key);
    if (onPath.has(key)) throw new Error(`Producer bindings form a cycle through calc ${key}.`);
    onPath.add(key);
    const out = new Set();
    for (const next of edges.get(key)) {
      out.add(next);
      for (const far of closure(edges, memo, onPath, next)) out.add(far);
    }
    onPath.delete(key);
    memo.set(key, out);
    return out;
  }

  // Parts in drawn tree order: each root, then its children in their drawn order, depth first.
  function partOrder(tree) {
    const order = new Map();
    function walk(id) {
      order.set(id, order.size);
      for (const kid of tree.childrenOf.get(id)) walk(kid);
    }
    tree.rootIds.forEach(walk);
    return order;
  }

  // reach = { upstream(key), downstream(key), subtreeCalcs, bindingEnds, partOrder, calcOrder,
  //           tree, model }. Every set is a Set of calc keys.
  function buildReach(model, tree) {
    const producers = new Map(model.calcs.map((calc) => [calc.key, []]));
    const consumers = new Map(model.calcs.map((calc) => [calc.key, []]));
    const bindingEnds = new Map();
    for (const binding of model.bindings) {
      if (!binding.resolved) continue;
      producers.get(binding.consumer).push(binding.producer);
      consumers.get(binding.producer).push(binding.consumer);
      bindingEnds.set(binding.id, { producer: binding.producer, consumer: binding.consumer });
    }
    const upMemo = new Map();
    const downMemo = new Map();
    const subtreeCalcs = new Map();
    function collect(id) {
      const keys = new Set(tree.calcsOf.get(id));
      for (const kid of tree.childrenOf.get(id)) for (const key of collect(kid)) keys.add(key);
      subtreeCalcs.set(id, keys);
      return keys;
    }
    tree.rootIds.forEach(collect);
    return {
      model,
      tree,
      bindingEnds,
      subtreeCalcs,
      partOrder: partOrder(tree),
      calcOrder: new Map(model.calcs.map((calc, i) => [calc.key, i])),
      upstream: (key) => closure(producers, upMemo, new Set(), key),
      downstream: (key) => closure(consumers, downMemo, new Set(), key),
    };
  }

  // The selection's calcs S: the selected calc, or every calc in a selected part's subtree (A4a).
  function selectionCalcs(reach, selection) {
    if (selection === null) return new Set();
    if (selection.kind === "calc") return new Set([selection.key]);
    const calcs = reach.subtreeCalcs.get(selection.partId);
    if (calcs === undefined) throw new Error(`No part ${selection.partId} in the overlay tree.`);
    return new Set(calcs);
  }

  function cones(reach, selection) {
    const s = selectionCalcs(reach, selection);
    const up = new Set();
    const down = new Set();
    for (const key of s) {
      for (const far of reach.upstream(key)) up.add(far);
      for (const far of reach.downstream(key)) down.add(far);
    }
    return { s, up, down };
  }

  // D37's table, applied top to bottom, first match wins. elements: the drawn Cytoscape elements;
  // repOf: calc key -> the id of the element standing for it; selection: null, or
  // {kind: "calc", key} / {kind: "part", partId} plus `representative`, the element that carries
  // mv-selected. Returns a Map of element id -> class, with unclassed elements left out.
  function classify(reach, elements, repOf, selection) {
    const classMap = new Map();
    if (selection === null) return classMap;
    const { s, up, down } = cones(reach, selection);
    const hidden = new Map();
    for (const [key, rep] of repOf) {
      if (rep === key) continue;
      if (!hidden.has(rep)) hidden.set(rep, new Set());
      hidden.get(rep).add(key);
    }
    const some = (keys, set) => [...keys].some((key) => set.has(key));

    for (const element of elements) {
      const data = element.data;
      if (element.group === "edges") {
        let litUp = false;
        let litDown = false;
        for (const id of data.bindings) {
          const ends = reach.bindingEnds.get(id);
          const inUp = (key) => up.has(key) || s.has(key);
          const inDown = (key) => down.has(key) || s.has(key);
          if (inUp(ends.producer) && inUp(ends.consumer)) litUp = true;
          if (inDown(ends.producer) && inDown(ends.consumer)) litDown = true;
        }
        if (litUp && litDown) classMap.set(data.id, "mv-both");
        else if (litUp) classMap.set(data.id, "mv-upstream");
        else if (litDown) classMap.set(data.id, "mv-downstream");
        else classMap.set(data.id, "mv-dim");
        continue;
      }
      if (data.kind === "calc") {
        const key = data.id;
        if (up.has(key) && down.has(key)) classMap.set(key, "mv-both");
        else if (up.has(key)) classMap.set(key, "mv-upstream");
        else if (down.has(key)) classMap.set(key, "mv-downstream");
        else if (s.has(key)) classMap.set(key, "mv-member");
        else classMap.set(key, "mv-dim");
        continue;
      }
      // An open part, or a calc-less leaf (A4b), carries no class; its children are classed alone.
      if (!data.collapsed) continue;
      const held = hidden.get(data.id) || new Set();
      const inUp = some(held, up);
      const inDown = some(held, down);
      const inS = some(held, s);
      if (inUp && inDown) classMap.set(data.id, "mv-both");
      else if (inS && (inUp || inDown)) classMap.set(data.id, "mv-both");
      else if (inUp) classMap.set(data.id, "mv-upstream");
      else if (inDown) classMap.set(data.id, "mv-downstream");
      else if (inS) classMap.set(data.id, "mv-member");
      else classMap.set(data.id, "mv-dim");
    }
    // I32: the element carrying mv-selected is never dimmed.
    if (selection.representative !== undefined && classMap.get(selection.representative) === "mv-dim") {
      classMap.delete(selection.representative);
    }
    return classMap;
  }

  // The panel's reach section (D38): each direction's calcs grouped by their owning part, groups in
  // drawn tree order, calcs by rank then snapshot order. Returns {upstream, downstream}, each a list
  // of {partId, path, calcs: [model calc]}.
  function reachLists(reach, selection) {
    const { up, down } = cones(reach, selection);
    return { upstream: group(reach, up), downstream: group(reach, down) };
  }

  function group(reach, keys) {
    const byPart = new Map();
    for (const key of keys) {
      const partId = reach.tree.containerOf.get(key);
      if (!byPart.has(partId)) byPart.set(partId, []);
      byPart.get(partId).push(key);
    }
    const parts = [...byPart.keys()].sort((a, b) => reach.partOrder.get(a) - reach.partOrder.get(b));
    return parts.map((partId) => ({
      partId,
      path: reach.tree.containers.get(partId).path,
      calcs: byPart
        .get(partId)
        .sort((a, b) => reach.tree.rank.get(a) - reach.tree.rank.get(b) || reach.calcOrder.get(a) - reach.calcOrder.get(b))
        .map((key) => reach.model.byKey.get(key)),
    }));
  }

  return { buildReach, selectionCalcs, cones, classify, reachLists };
})();
