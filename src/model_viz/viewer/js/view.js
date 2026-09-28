// Pure layer: containers per grouping mode and the visible elements for a collapse state.
// No DOM, no Cytoscape (design I8). Output is plain Cytoscape element JSON.
window.ModelViz = window.ModelViz || {};

ModelViz.view = (function () {
  // Container = { id, parent: id|null, label, kind, memberCount, groupPath?, occurrenceId? }
  // Tree = { mode, containers: Map<id, Container> (parents before children), containerOf: Map<calcKey, id> }
  function sourceTree(model) {
    const containers = new Map();
    const containerOf = new Map();
    for (const group of model.groups.values()) {
      containers.set(group.gid, {
        id: group.gid,
        parent: null,
        label: group.label,
        kind: group.kind,
        memberCount: 0,
        groupPath: group.path,
      });
    }
    for (const calc of model.calcs) {
      containerOf.set(calc.key, calc.sourceGroup);
      containers.get(calc.sourceGroup).memberCount += 1;
    }
    return { mode: "source", containers, containerOf };
  }

  function occurrenceTree(model) {
    // Which occurrences hold a calc, directly or through a descendant.
    const needed = new Set();
    let unscoped = false;
    for (const calc of model.calcs) {
      if (calc.occurrenceId === null || !model.occurrences.has(calc.occurrenceId)) {
        unscoped = true;
        continue;
      }
      for (let id = calc.occurrenceId; id !== null; id = model.occurrences.get(id).parentId) needed.add(id);
    }
    const idByOccurrence = new Map();
    let n = 0;
    for (const occ of model.occurrences.values()) {
      if (needed.has(occ.occurrenceId)) idByOccurrence.set(occ.occurrenceId, "o" + n++);
    }
    // Parents before children, so compound parents exist when a child is added.
    const ordered = [...idByOccurrence.keys()].sort((a, b) => model.occurrences.get(a).depth - model.occurrences.get(b).depth);
    const containers = new Map();
    for (const occurrenceId of ordered) {
      const occ = model.occurrences.get(occurrenceId);
      containers.set(idByOccurrence.get(occurrenceId), {
        id: idByOccurrence.get(occurrenceId),
        parent: occ.parentId === null ? null : idByOccurrence.get(occ.parentId),
        label: occ.segment === null ? "segment not recorded" : occ.segment,
        kind: "occurrence",
        memberCount: 0,
        occurrenceId,
      });
    }
    if (unscoped) {
      containers.set("o-unscoped", { id: "o-unscoped", parent: null, label: "unscoped", kind: "unscoped", memberCount: 0, occurrenceId: null });
    }
    const containerOf = new Map();
    for (const calc of model.calcs) {
      const direct = idByOccurrence.has(calc.occurrenceId) ? idByOccurrence.get(calc.occurrenceId) : "o-unscoped";
      containerOf.set(calc.key, direct);
    }
    const tree = { mode: "occurrence", containers, containerOf };
    for (const calc of model.calcs) {
      for (const id of containerChain(tree, calc.key)) containers.get(id).memberCount += 1;
    }
    return tree;
  }

  function containerTree(model, mode) {
    if (mode === "source") return sourceTree(model);
    if (mode === "occurrence") return occurrenceTree(model);
    throw new Error(`Unknown grouping mode: ${mode}`);
  }

  // A calc's containers from its direct container outwards.
  function containerChain(tree, calcKey) {
    if (!tree.containerOf.has(calcKey)) throw new Error(`Calc ${calcKey} has no container in the ${tree.mode} tree.`);
    const chain = [];
    for (let id = tree.containerOf.get(calcKey); id !== null; id = tree.containers.get(id).parent) chain.push(id);
    return chain;
  }

  // Container ancestors from its parent outwards.
  function containerAncestors(tree, containerId) {
    const chain = [];
    for (let id = tree.containers.get(containerId).parent; id !== null; id = tree.containers.get(id).parent) chain.push(id);
    return chain;
  }

  // The outermost collapsed container on the chain, or null when none is collapsed.
  function outermostCollapsed(chain, collapsed) {
    let found = null;
    for (const id of chain) if (collapsed.has(id)) found = id;
    return found;
  }

  // The visibility rule shared by both views (design D14, I11): a container is drawn when none of
  // its ancestors is collapsed. Returns the drawn containers in tree order (parents first).
  function visibleContainers(tree, collapsed) {
    return [...tree.containers.values()].filter((container) => outermostCollapsed(containerAncestors(tree, container.id), collapsed) === null);
  }

  function containerNode(tree, container, isCollapsed) {
    const data = {
      id: container.id,
      kind: "container",
      mode: tree.mode,
      label: isCollapsed ? `${container.label} (${container.memberCount})` : container.label,
      container_kind: container.kind,
      member_count: container.memberCount,
      collapsed: isCollapsed,
    };
    if (tree.mode === "source") data.group_path = container.groupPath;
    else data.occurrence_id = container.occurrenceId;
    if (container.parent !== null) data.parent = container.parent;
    return { group: "nodes", data, selectable: false };
  }

  function calcNode(calc, parent) {
    return {
      group: "nodes",
      data: {
        id: calc.key,
        kind: "calc",
        label: calc.name,
        node_id: calc.nodeId,
        source_group: calc.sourceGroup,
        occurrence_id: calc.occurrenceId,
        parent,
      },
      selectable: false,
    };
  }

  // The visible-edge rule (design § The visible-edge rule): each resolved binding maps to the
  // nearest visible thing at each end; equal ends vanish; equal directed ends merge into one edge.
  function visibleElements(model, tree, collapsed) {
    const elements = [];
    for (const container of visibleContainers(tree, collapsed)) {
      elements.push(containerNode(tree, container, collapsed.has(container.id)));
    }
    const repOf = new Map();
    for (const calc of model.calcs) {
      const chain = containerChain(tree, calc.key);
      const rep = outermostCollapsed(chain, collapsed);
      repOf.set(calc.key, rep === null ? calc.key : rep);
      if (rep === null) elements.push(calcNode(calc, chain[0]));
    }
    const edges = new Map();
    for (const binding of model.bindings) {
      if (!binding.resolved) continue;
      const source = repOf.get(binding.producer);
      const target = repOf.get(binding.consumer);
      if (source === target) continue;
      const id = `e:${source}>${target}`;
      if (!edges.has(id)) edges.set(id, { group: "edges", data: { id, source, target, bindings: [] }, selectable: false });
      edges.get(id).data.bindings.push(binding.id);
    }
    for (const edge of edges.values()) {
      edge.data.weight = edge.data.bindings.length;
      elements.push(edge);
    }
    return elements;
  }

  return { containerTree, containerChain, containerAncestors, visibleContainers, visibleElements };
})();
