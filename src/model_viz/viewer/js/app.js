// App: owns the one mutable state object and wires page events to state changes.
window.ModelViz = window.ModelViz || {};

(function () {
  const { readSnapshot, buildModel, SnapshotError } = ModelViz.model;
  const { containerTree, visibleElements } = ModelViz.view;

  const body = document.body;
  const fileInput = document.querySelector("[data-role=snapshot-input]");
  const banner = document.querySelector("[data-role=error-banner]");
  const panelElement = document.querySelector("[data-role=panel]");
  const searchInput = document.querySelector("[data-role=search-input]");
  const searchStatus = document.querySelector("[data-role=search-status]");
  const calcNames = document.querySelector("[data-role=calc-names]");
  const modeSelect = document.querySelector("[data-role=mode-select]");
  const modelControls = document.querySelectorAll("[data-action], [data-role=search-input], [data-role=mode-select]");

  const state = { model: null, mode: modeSelect.value, tree: null, collapsed: new Set(), selected: null };

  const graph = ModelViz.graph.create(document.querySelector("[data-role=graph-pane]"), {
    onCalcTap: (key) => showCalc(key),
    onContainerTap: (id) => toggleContainer(id),
  });

  function requireModel() {
    if (state.model === null) throw new Error("No snapshot is loaded.");
  }

  function redraw() {
    graph.render(visibleElements(state.model, state.tree, state.collapsed));
    if (state.selected !== null) graph.selectCalc(state.selected);
  }

  // Show a calc's panel and select it on the graph when it is drawn.
  function showCalc(key) {
    requireModel();
    if (!state.model.byKey.has(key)) throw new Error(`No calc ${key} in the model.`);
    state.selected = key;
    graph.selectCalc(key);
    ModelViz.panel.renderPanel(panelElement, state.model, key, (target) => navigateTo(target));
  }

  // Navigation contract (design § Navigation contract, D6): open the target's collapsed
  // containers from the tree, rebuild if needed, select, zoom to at least 1.0 and centre.
  function navigateTo(key) {
    requireModel();
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
    graph.focusCalc(key);
  }

  function toggleContainer(id) {
    requireModel();
    if (!state.tree.containers.has(id)) throw new Error(`No container ${id} in the ${state.mode} tree.`);
    if (state.collapsed.has(id)) state.collapsed.delete(id);
    else state.collapsed.add(id);
    redraw();
  }

  function expandAll() {
    requireModel();
    state.collapsed = new Set();
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
    state.collapsed = new Set(state.tree.containers.keys());
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
  }

  // I6: a load attempt clears everything from the previous snapshot before validating.
  function clearLoaded() {
    Object.assign(state, { model: null, tree: null, collapsed: new Set(), selected: null });
    graph.render([]);
    ModelViz.panel.renderPlaceholder(panelElement);
    banner.hidden = true;
    banner.textContent = "";
    calcNames.replaceChildren();
    searchInput.value = "";
    searchStatus.textContent = "";
    setModelControlsEnabled(false);
  }

  function showLoadError(message) {
    banner.textContent = message;
    banner.hidden = false;
  }

  function loadText(text) {
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
    for (const calc of state.model.calcs) {
      const option = document.createElement("option");
      option.value = calc.name;
      calcNames.appendChild(option);
    }
    setModelControlsEnabled(true);
    redraw();
    return "ready";
  }

  fileInput.addEventListener("change", async () => {
    const file = fileInput.files[0];
    if (file === undefined) return;
    const text = await file.text();
    fileInput.value = "";
    body.dataset.loadState = loadText(text);
    body.dataset.loadSeq = String(Number(body.dataset.loadSeq) + 1);
  });

  document.querySelector("[data-action=expand-all]").addEventListener("click", expandAll);
  document.querySelector("[data-action=collapse-all]").addEventListener("click", collapseAll);
  document.querySelector("[data-action=fit]").addEventListener("click", () => graph.fit());
  modeSelect.addEventListener("change", () => setMode(modeSelect.value));
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
      return { mode: state.mode, collapsed: [...state.collapsed], selected: state.selected };
    },
    toggleContainer,
    expandAll,
    collapseAll,
    setMode,
    showCalc,
    navigateTo,
  };
})();
