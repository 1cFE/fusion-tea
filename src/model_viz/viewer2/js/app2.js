// App: owns v2's one mutable state object and wires page events to state changes (design D41).
//
// Owner ruling 2026-09-15: the picture is laid out by dagre, left to right, and the layout is
// re-run on every expand or collapse, exactly as v1's calc graph does. The viewport rules are v1's
// too: a layout run fits, and navigation centres the target at zoom >= 1 (or fits it when it is too
// big for the pane). D32's pinned geometry and D35's "a toggle never moves the viewport" are gone.
// The panel still re-renders after every toggle and selection change (D38, A8).
window.ModelViz = window.ModelViz || {};

(function () {
  const { readSnapshot, buildModel, SnapshotError } = ModelViz.model;
  const { UNSCOPED_ID, overlayTree, collapseAllSet, overlayElements, find } = ModelViz.overlay;
  const { containerChain, containerAncestors } = ModelViz.view;
  const { plural } = ModelViz.structure;
  const panel2 = ModelViz.panel2;

  const body = document.body;
  const fileInput = document.querySelector("[data-role=snapshot-input]");
  const banner = document.querySelector("[data-role=error-banner]");
  const panelElement = document.querySelector("[data-role=panel]");
  const searchInput = document.querySelector("[data-role=search-input]");
  const searchStatus = document.querySelector("[data-role=search-status]");
  const findList = document.querySelector("[data-role=find-list]");
  const spacingInput = document.querySelector("[data-role=spacing]");
  const spacingValue = document.querySelector("[data-role=spacing-value]");
  const modelControls = document.querySelectorAll("[data-action], [data-role=search-input], [data-role=spacing]");

  // D41. selected: {kind: "calc", key} | {kind: "part", occurrenceId, partId} | null.
  // scale: the Spacing factor dagre's node and rank separations are multiplied by.
  const state = {
    model: null,
    tree: null,
    reach: null,
    elements: [],
    repOf: new Map(),
    collapsed: new Set(),
    selected: null,
    trace: null,
    scale: 1,
  };

  const graph = ModelViz.graph2.create(document.querySelector("[data-role=graph-pane]"), {
    onCalcTap: (key) => showCalc(key),
    onPartTap: (id) => tapPart(id),
    onBackgroundTap: () => clearSelection(),
  });

  const panelHandlers = {
    onCalc: (key) => navigateTo(key),
    onPart: (occurrenceId, attrNodeId) => {
      navigateToPart(occurrenceId);
      ModelViz.partPanel.revealRow(panelElement, attrNodeId);
    },
    onTogglePart: (occurrenceId) => toggleContainer(partIdFor(occurrenceId)),
    onClear: () => clearSelection(),
  };

  // The public selection: a calc by key, a part by occurrence id (the internal part id stays private).
  function publicSelection() {
    if (state.selected === null) return null;
    if (state.selected.kind === "calc") return { kind: "calc", key: state.selected.key };
    return { kind: "part", occurrenceId: state.selected.occurrenceId };
  }

  function requireModel() {
    if (state.model === null) throw new Error("No snapshot is loaded.");
  }

  function requirePart(id) {
    const part = state.tree.containers.get(id);
    if (part === undefined) throw new Error(`No part ${id} in the overlay tree.`);
    return part;
  }

  // The unscoped part (D44) has no occurrence; null names it.
  function partIdFor(occurrenceId) {
    if (occurrenceId === null && state.tree.containers.has(UNSCOPED_ID)) return UNSCOPED_ID;
    const id = state.tree.idByOccurrence.get(occurrenceId);
    if (id === undefined) throw new Error(`No part for occurrence ${occurrenceId} in the overlay tree.`);
    return id;
  }

  // The panel for the current selection (D38): the shared renderers plus v2's additions, or the placeholder.
  function renderPanel() {
    if (state.model === null || state.selected === null) {
      panel2.showPlaceholder(panelElement);
      return;
    }
    const lists = ModelViz.reach.reachLists(state.reach, currentSelection());
    if (state.selected.kind === "calc") {
      panel2.showCalcPanel(panelElement, state.model, state.selected.key, panelHandlers, lists);
    } else {
      const part = requirePart(state.selected.partId);
      panel2.showPartPanel(panelElement, state.model, part, state.collapsed.has(part.id), panelHandlers, lists);
    }
  }

  // The drawn element standing for the selection: itself, or the outermost closed part hiding it (D37).
  function selectedRepresentative() {
    if (state.selected === null) return null;
    let chain;
    if (state.selected.kind === "calc") chain = containerChain(state.tree, state.selected.key);
    else chain = [state.selected.partId, ...containerAncestors(state.tree, state.selected.partId)];
    let rep = state.selected.kind === "calc" ? state.selected.key : state.selected.partId;
    for (const id of chain) if (state.collapsed.has(id)) rep = id;
    return rep;
  }

  // The selection as the pure layer takes it (D37): its calcs and the element that carries mv-selected.
  function currentSelection() {
    if (state.selected === null) return null;
    const representative = selectedRepresentative();
    if (state.selected.kind === "calc") return { kind: "calc", key: state.selected.key, representative };
    return { kind: "part", partId: state.selected.partId, representative };
  }

  // I28: every drawn element's reach class, recomputed from the visible elements and the selection.
  function applyClasses() {
    if (state.model === null) return;
    const selection = currentSelection();
    const classMap = ModelViz.reach.classify(state.reach, state.elements, state.repOf, selection);
    graph.applyClasses(classMap, selection === null ? null : selection.representative);
  }

  // Redraw the current collapse state and re-run the layout, which fits (v1's LAYOUT.fit).
  function redraw() {
    const { elements, repOf } = overlayElements(state.model, state.tree, state.collapsed);
    state.elements = elements;
    state.repOf = repOf;
    graph.render(elements, state.scale);
    applyClasses();
  }

  // Re-run the layout, dropping whatever the modeler dragged. The collapse set and the selection stay.
  function resetLayout() {
    requireModel();
    redraw();
  }

  // The Spacing control: re-run dagre with its node and rank separations multiplied by `scale`.
  function setSpacing(scale) {
    requireModel();
    const value = Number(scale);
    if (!(value > 0)) throw new Error(`Spacing must be positive, got ${scale}.`);
    state.scale = value;
    redraw();
    renderPanel();
    showSpacing(value);
  }

  function showSpacing(value) {
    if (Number(spacingInput.value) !== value) spacingInput.value = String(value);
    spacingValue.textContent = `${value}\u00d7`;
  }

  // D36: a tap on a closed part opens it and selects it; on an open part it selects it.
  function tapPart(id) {
    requireModel();
    const part = requirePart(id);
    if (state.collapsed.delete(id)) redraw();
    selectPart(part);
  }

  function selectPart(part) {
    state.selected = { kind: "part", occurrenceId: part.occurrenceId, partId: part.id };
    applyClasses();
    renderPanel();
  }

  function showPart(occurrenceId) {
    requireModel();
    selectPart(requirePart(partIdFor(occurrenceId)));
  }

  function showCalc(key) {
    requireModel();
    if (!state.model.byKey.has(key)) throw new Error(`No calc ${key} in the model.`);
    state.selected = { kind: "calc", key };
    applyClasses();
    renderPanel();
  }

  // D36: clears the selection and any trace; changes no geometry or viewport.
  function clearSelection() {
    state.selected = null;
    state.trace = null;
    applyClasses();
    renderPanel();
  }

  // Open only the target's closed ancestors, re-lay out, select, then land the target the way v1
  // does: centred at zoom >= 1.0, or fitted when its box is too big for the pane at that zoom.
  function reveal(ancestors, select, id) {
    let opened = false;
    for (const ancestor of ancestors) opened = state.collapsed.delete(ancestor) || opened;
    if (opened) redraw();
    select();
    graph.revealNode(id);
  }

  function navigateTo(key) {
    requireModel();
    if (!state.model.byKey.has(key)) throw new Error(`No calc ${key} in the model.`);
    reveal(containerChain(state.tree, key), () => showCalc(key), key);
  }

  function navigateToPart(occurrenceId) {
    requireModel();
    const id = partIdFor(occurrenceId);
    reveal(containerAncestors(state.tree, id), () => showPart(occurrenceId), id);
  }

  // A toggle redraws at the pinned geometry and re-renders the panel (A8); the selection stays.
  function toggleContainer(id) {
    requireModel();
    requirePart(id);
    if (!state.tree.collapsible.has(id)) throw new Error(`Cannot collapse ${id}: it owns no calcs and has no children.`);
    if (state.collapsed.has(id)) state.collapsed.delete(id);
    else state.collapsed.add(id);
    redraw();
    renderPanel();
  }

  function expandAll() {
    requireModel();
    state.collapsed = new Set();
    redraw();
    renderPanel();
  }

  function collapseAll() {
    requireModel();
    state.collapsed = collapseAllSet(state.tree);
    redraw();
    renderPanel();
  }

  function fit() {
    requireModel();
    graph.fit();
  }

  // D39: one match navigates; several report the count split by kind; none says so.
  function runSearch() {
    requireModel();
    const query = searchInput.value.trim();
    if (query === "") {
      searchStatus.textContent = "";
      return;
    }
    const { parts, calcs } = find(state.model, state.tree, query);
    const total = parts.length + calcs.length;
    if (total === 0) {
      searchStatus.textContent = "no part or calc matches";
    } else if (total > 1) {
      searchStatus.textContent = `${total} matches (${plural(parts.length, "part", "parts")}, ${plural(calcs.length, "calc", "calcs")})`;
    } else {
      searchStatus.textContent = "";
      if (parts.length === 1) navigateToPart(parts[0].occurrenceId);
      else navigateTo(calcs[0].key);
    }
  }

  function setModelControlsEnabled(enabled) {
    for (const control of modelControls) control.disabled = !enabled;
  }

  // I6, I15 (R15): a load attempt clears the previous snapshot's state, panel and search before validating.
  function clearLoaded() {
    Object.assign(state, { model: null, tree: null, reach: null, elements: [], repOf: new Map(), collapsed: new Set(), selected: null, trace: null, scale: 1 });
    showSpacing(1);
    graph.render([]);
    banner.hidden = true;
    banner.textContent = "";
    findList.replaceChildren();
    searchInput.value = "";
    searchStatus.textContent = "";
    setModelControlsEnabled(false);
    renderPanel();
  }

  function showLoadError(message) {
    banner.textContent = message;
    banner.hidden = false;
  }

  function drawSnapshot(text) {
    clearLoaded();
    try {
      state.model = buildModel(readSnapshot(text));
    } catch (err) {
      if (!(err instanceof SnapshotError)) throw err;
      showLoadError(err.message);
      return "error";
    }
    state.tree = overlayTree(state.model);
    state.reach = ModelViz.reach.buildReach(state.model, state.tree);
    // The start state is v1's: every collapsible part below a root closed, so the opening picture
    // is the subsystem flow. The layout run inside redraw() fits it.
    state.collapsed = collapseAllSet(state.tree);
    for (const part of state.tree.containers.values()) {
      const option = document.createElement("option");
      option.value = part.path;
      findList.appendChild(option);
    }
    for (const calc of state.model.calcs) {
      const option = document.createElement("option");
      option.value = calc.name;
      findList.appendChild(option);
    }
    setModelControlsEnabled(true);
    redraw();
    renderPanel();
    return "ready";
  }

  function loadText(text) {
    body.dataset.loadState = drawSnapshot(text);
    body.dataset.loadSeq = String(Number(body.dataset.loadSeq) + 1);
  }

  fileInput.addEventListener("change", async () => {
    const file = fileInput.files[0];
    if (file === undefined) return;
    const text = await file.text();
    fileInput.value = "";
    loadText(text);
  });
  document.querySelector("[data-action=expand-all]").addEventListener("click", expandAll);
  document.querySelector("[data-action=collapse-all]").addEventListener("click", collapseAll);
  document.querySelector("[data-action=fit]").addEventListener("click", fit);
  document.querySelector("[data-action=reset-layout]").addEventListener("click", resetLayout);
  spacingInput.addEventListener("change", () => setSpacing(spacingInput.value));
  searchInput.addEventListener("change", runSearch);
  searchInput.addEventListener("keydown", (evt) => {
    if (evt.key === "Enter") runSearch();
  });

  clearLoaded();

  window.modelVizApp = {
    get cy() {
      return graph.cy;
    },
    get model() {
      return state.model;
    },
    get state() {
      const collapsed = [...state.collapsed];
      return {
        collapsed,
        collapsedOccurrences: collapsed.map((id) => state.tree.containers.get(id).occurrenceId),
        selected: publicSelection(),
        trace: state.trace,
        scale: state.scale,
      };
    },
    toggleContainer,
    expandAll,
    collapseAll,
    fit,
    resetLayout,
    setSpacing,
    showCalc,
    navigateTo,
    showPart,
    navigateToPart,
    clearSelection,
    loadText,
  };
})();
