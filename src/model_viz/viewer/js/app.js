// App: owns the one mutable state object and wires page events to state changes.
window.ModelViz = window.ModelViz || {};

(function () {
  const { readSnapshot, buildModel, SnapshotError } = ModelViz.model;
  const { containerTree, visibleElements } = ModelViz.view;
  const { structuralTree, structureElements, startCollapsed, collapsibleParts, matchParts } = ModelViz.structure;
  const STRUCTURE_LAYOUT = { name: "preset", fit: true, padding: 20 };

  const body = document.body;
  const fileInput = document.querySelector("[data-role=snapshot-input]");
  const banner = document.querySelector("[data-role=error-banner]");
  const panelElement = document.querySelector("[data-role=panel]");
  const searchInput = document.querySelector("[data-role=search-input]");
  const searchStatus = document.querySelector("[data-role=search-status]");
  const searchLabel = document.querySelector("[data-role=search-label]");
  const calcNames = document.querySelector("[data-role=calc-names]");
  const partPaths = document.querySelector("[data-role=part-paths]");
  const modeSelect = document.querySelector("[data-role=mode-select]");
  const viewSelect = document.querySelector("[data-role=view-select]");
  const modelControls = document.querySelectorAll("[data-action], [data-role=search-input], [data-role=mode-select], [data-role=view-select]");

  // The flat fields mode, tree, collapsed and selected are the calc view's state (D17);
  // structure holds the structure view's own tree, collapse set (part ids) and selected occurrence id.
  const state = {
    model: null,
    view: viewSelect.value,
    mode: modeSelect.value,
    tree: null,
    collapsed: new Set(),
    selected: null,
    structure: { tree: null, collapsed: new Set(), selected: null },
  };

  const graph = ModelViz.graph.create(document.querySelector("[data-role=graph-pane]"), {
    onCalcTap: (key) => showCalc(key),
    onContainerTap: (id) => toggleContainer(id),
    onPartTap: (id) => tapPart(id),
  });

  function requireModel() {
    if (state.model === null) throw new Error("No snapshot is loaded.");
  }

  function redraw() {
    if (state.view === "calcs") {
      graph.render(visibleElements(state.model, state.tree, state.collapsed));
      if (state.selected !== null) graph.selectNode(state.selected);
    } else {
      const { tree, collapsed, selected } = state.structure;
      graph.render(structureElements(tree, collapsed), { layout: STRUCTURE_LAYOUT });
      if (selected !== null) graph.selectNode(tree.idByOccurrence.get(selected));
    }
  }

  // D19: a tap on a part selects it and opens its panel; a tap on a collapsed part also expands it.
  // A tap never collapses anything.
  function tapPart(id) {
    requireModel();
    const part = state.structure.tree.containers.get(id);
    if (part === undefined) throw new Error(`No part ${id} in the structure tree.`);
    if (state.structure.collapsed.delete(id)) redraw();
    showPart(part.occurrenceId);
  }

  function partIdFor(occurrenceId) {
    const id = state.structure.tree.idByOccurrence.get(occurrenceId);
    if (id === undefined) throw new Error(`No part for occurrence ${occurrenceId} in the structure tree.`);
    return id;
  }

  // Show a part's panel and select it on the graph when it is drawn (D21, D27: a no-op switch in structure).
  function showPart(occurrenceId) {
    requireModel();
    setView("structure");
    const id = partIdFor(occurrenceId);
    state.structure.selected = occurrenceId;
    graph.selectNode(id);
    renderPartPanel(occurrenceId);
  }

  function renderPartPanel(occurrenceId) {
    const collapsed = state.structure.collapsed.has(partIdFor(occurrenceId));
    ModelViz.partPanel.renderPart(panelElement, state.model, occurrenceId, collapsed, {
      onCalc: (key) => navigateTo(key),
      onPart: (target, attrNodeId) => {
        navigateToPart(target);
        ModelViz.partPanel.revealRow(panelElement, attrNodeId);
      },
      onTogglePart: (target) => togglePart(target),
    });
  }

  // The panel's Collapse/Expand button (D19): toggle the shown part; it stays selected.
  function togglePart(occurrenceId) {
    toggleContainer(partIdFor(occurrenceId));
    renderPartPanel(occurrenceId);
  }

  // Navigation to a part (design § Navigation to a part): open its collapsed ancestors from the tree,
  // rebuild if needed, select, then centre at zoom 1.0 or more, or fit the part when it is too big for that.
  function navigateToPart(occurrenceId) {
    requireModel();
    setView("structure");
    const { tree, collapsed } = state.structure;
    if (!tree.idByOccurrence.has(occurrenceId)) {
      state.structure.selected = null;
      graph.clearSelection();
      ModelViz.partPanel.renderMissingPart(panelElement, occurrenceId);
      return;
    }
    const id = partIdFor(occurrenceId);
    let opened = false;
    for (let ancestor = tree.containers.get(id).parent; ancestor !== null; ancestor = tree.containers.get(ancestor).parent) {
      opened = collapsed.delete(ancestor) || opened;
    }
    if (opened) redraw();
    showPart(occurrenceId);
    if (graph.fitsPane(id, Math.max(graph.cy.zoom(), 1.0))) graph.focusNode(id);
    else graph.fitNode(id);
  }

  // Page controls that follow the active view: body[data-view], the View select, and the search
  // label with its datalist (D22, PD3).
  function showViewControls() {
    const calcs = state.view === "calcs";
    body.dataset.view = state.view;
    viewSelect.value = state.view;
    searchLabel.textContent = calcs ? "Find calc" : "Find part";
    searchInput.setAttribute("list", calcs ? "calc-names" : "part-paths");
  }

  // The active view's panel: its selection, or its placeholder when nothing is selected.
  function renderActivePanel() {
    if (state.view === "calcs" && state.selected !== null) renderCalcPanel(state.selected);
    else if (state.view === "structure" && state.structure.selected !== null) renderPartPanel(state.structure.selected);
    else renderPlaceholder();
  }

  // The active view's empty panel; with a model loaded, the structure placeholder names what no part shows.
  function renderPlaceholder() {
    if (state.view === "structure" && state.model !== null) ModelViz.partPanel.renderStructurePlaceholder(panelElement, state.model);
    else ModelViz.panel.renderPlaceholder(panelElement, state.view);
  }

  // Switch the active view (D17). A switch to the active view changes nothing (D27).
  // Each view redraws from its own collapse set and selection; the model is never re-read (D18).
  function setView(view) {
    requireModel();
    if (view !== "calcs" && view !== "structure") throw new Error(`Unknown view: ${view}`);
    if (view === state.view) return;
    state.view = view;
    showViewControls();
    modeSelect.disabled = view === "structure";
    searchInput.value = "";
    searchStatus.textContent = "";
    redraw();
    renderActivePanel();
  }

  // Show a calc's panel and select it on the graph when it is drawn (D21: from the structure view, switch first).
  function showCalc(key) {
    requireModel();
    setView("calcs");
    if (!state.model.byKey.has(key)) throw new Error(`No calc ${key} in the model.`);
    state.selected = key;
    graph.selectNode(key);
    renderCalcPanel(key);
  }

  function renderCalcPanel(key) {
    ModelViz.panel.renderPanel(panelElement, state.model, key, (target) => navigateTo(target));
  }

  // Navigation contract (design § Navigation contract, D6): open the target's collapsed
  // containers from the tree, rebuild if needed, select, zoom to at least 1.0 and centre.
  function navigateTo(key) {
    requireModel();
    setView("calcs");
    if (!state.model.byKey.has(key)) {
      state.selected = null;
      graph.clearSelection();
      ModelViz.panel.renderMissingCalc(panelElement, key);
      return;
    }
    const closed = ModelViz.view.containerChain(state.tree, key).filter((id) => state.collapsed.has(id));
    if (closed.length > 0) {
      for (const id of closed) state.collapsed.delete(id);
      redraw();
    }
    showCalc(key);
    graph.focusNode(key);
  }

  // Collapse or expand one container of the active view's tree.
  function toggleContainer(id) {
    requireModel();
    const { tree, collapsed } = state.view === "calcs" ? state : state.structure;
    if (!tree.containers.has(id)) throw new Error(`No container ${id} in the ${tree.mode} tree.`);
    if (state.view === "structure" && tree.containers.get(id).childCount === 0) throw new Error(`Cannot collapse ${id}: part has no children.`);
    if (collapsed.has(id)) collapsed.delete(id);
    else collapsed.add(id);
    redraw();
  }

  function expandAll() {
    requireModel();
    if (state.view === "calcs") state.collapsed = new Set();
    else state.structure.collapsed = new Set();
    redraw();
  }

  // A mode switch rebuilds the containers and collapses all (D5); the selection and panel stay.
  function setMode(mode) {
    requireModel();
    state.mode = mode;
    state.tree = containerTree(state.model, mode);
    state.collapsed = new Set(state.tree.containers.keys());
    redraw();
  }

  function collapseAll() {
    requireModel();
    if (state.view === "calcs") state.collapsed = new Set(state.tree.containers.keys());
    else state.structure.collapsed = collapsibleParts(state.structure.tree);
    redraw();
  }

  // Calcs whose name matches the query: exact (case-insensitive) matches first, else substrings.
  function matchCalcs(model, query) {
    const q = query.toLowerCase();
    const exact = model.calcs.filter((calc) => calc.name.toLowerCase() === q);
    return exact.length > 0 ? exact : model.calcs.filter((calc) => calc.name.toLowerCase().includes(q));
  }

  function runSearch() {
    requireModel();
    const query = searchInput.value.trim();
    if (query === "") {
      searchStatus.textContent = "";
      return;
    }
    if (state.view === "structure") {
      const parts = matchParts(state.structure.tree, query);
      if (parts.length === 1) {
        searchStatus.textContent = "";
        navigateToPart(parts[0].occurrenceId);
      } else {
        searchStatus.textContent = parts.length === 0 ? "no part matches" : `${parts.length} parts match`;
      }
      return;
    }
    const matches = matchCalcs(state.model, query);
    if (matches.length === 1) {
      searchStatus.textContent = "";
      navigateTo(matches[0].key);
    } else {
      searchStatus.textContent = matches.length === 0 ? "no calc matches" : `${matches.length} calcs match`;
    }
  }

  function setModelControlsEnabled(enabled) {
    for (const control of modelControls) control.disabled = !enabled;
    if (enabled && state.view === "structure") modeSelect.disabled = true;
  }

  // I6, I15: a load attempt clears both views' state from the previous snapshot before validating,
  // and keeps the active view.
  function clearLoaded() {
    Object.assign(state, { model: null, tree: null, collapsed: new Set(), selected: null });
    state.structure = { tree: null, collapsed: new Set(), selected: null };
    graph.render([]);
    ModelViz.panel.renderPlaceholder(panelElement, state.view);
    banner.hidden = true;
    banner.textContent = "";
    calcNames.replaceChildren();
    partPaths.replaceChildren();
    searchInput.value = "";
    searchStatus.textContent = "";
    setModelControlsEnabled(false);
  }

  function showLoadError(message) {
    banner.textContent = message;
    banner.hidden = false;
  }

  // Replace whatever is loaded with the snapshot in text; returns "ready" or "error".
  function drawSnapshot(text) {
    clearLoaded();
    try {
      state.model = buildModel(readSnapshot(text));
    } catch (err) {
      if (!(err instanceof SnapshotError)) throw err;
      showLoadError(err.message);
      return "error";
    }
    state.tree = containerTree(state.model, state.mode);
    state.collapsed = new Set(state.tree.containers.keys());
    state.structure.tree = structuralTree(state.model);
    state.structure.collapsed = startCollapsed(state.structure.tree);
    for (const calc of state.model.calcs) {
      const option = document.createElement("option");
      option.value = calc.name;
      calcNames.appendChild(option);
    }
    for (const part of state.structure.tree.containers.values()) {
      const option = document.createElement("option");
      option.value = part.path;
      partPaths.appendChild(option);
    }
    setModelControlsEnabled(true);
    redraw();
    renderPlaceholder();
    return "ready";
  }

  // Load snapshot text as the file picker does: draw it (or show the error), then record the
  // outcome and bump the load counter on the body.
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
  document.querySelector("[data-action=fit]").addEventListener("click", () => graph.fit());
  modeSelect.addEventListener("change", () => setMode(modeSelect.value));
  viewSelect.addEventListener("change", () => setView(viewSelect.value));
  searchInput.addEventListener("change", runSearch);
  searchInput.addEventListener("keydown", (evt) => {
    if (evt.key === "Enter") runSearch();
  });

  showViewControls();
  clearLoaded();

  window.modelVizApp = {
    get cy() {
      return graph.cy;
    },
    get model() {
      return state.model;
    },
    get state() {
      return {
        view: state.view,
        mode: state.mode,
        collapsed: [...state.collapsed],
        selected: state.selected,
        structure: { collapsed: [...state.structure.collapsed], selected: state.structure.selected },
      };
    },
    toggleContainer,
    expandAll,
    collapseAll,
    setMode,
    setView,
    showCalc,
    navigateTo,
    showPart,
    navigateToPart,
    loadText,
  };
})();
